"""
__all__ = [
    'generate_segment_report',
    'get_at_risk_users',
    'predict',
    'predict_batch',
    'segment_users',
    'to_dict',
    'to_rfm',
    'to_vector',
]

用户分类器 - 基于用户characteristics预测行为/价值/流失
支持: 高价值用户recognize,流失预警,转化预测,用户分层
"""

import json
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from src.core.paths import ML_CLASSIFIER_DIR
from collections import Counter

class ClassificationTask(Enum):
    """分类任务"""
    CHURN_PREDICTION = "churn_prediction"         # 流失预测
    VALUE_SEGMENTATION = "value_segmentation"      # 价值分层
    CONVERSION_PREDICTION = "conversion_prediction" # 转化预测
    ACTIVATION_PREDICTION = "activation_prediction" # 激活预测
    UPGRADE_PREDICTION = "upgrade_prediction"       # 升级预测

class UserSegment(Enum):
    """用户分层(RFM模型)"""
    CHAMPIONS = "champions"               # 冠军用户:高R高F高M
    LOYAL = "loyal"                       # 忠诚用户:高F高M
    POTENTIAL_LOYAL = "potential_loyal"   # 潜力用户:高R中F
    NEW_CUSTOMERS = "new_customers"       # 新用户:高R低F低M
    PROMISING = "promising"              # 有前途:中R低F
    NEED_ATTENTION = "need_attention"    # 需关注:中R中F中M
    ABOUT_TO_SLEEP = "about_to_sleep"   # 即将沉默:低R中F中M
    AT_RISK = "at_risk"                  # 高风险:低R高F高M
    CANT_LOSE = "cant_lose"             # 不能失去:低R高M
    HIBERNATING = "hibernating"          # 冬眠:低R低F低M
    LOST = "lost"                        # 流失:极低R低F低M

@dataclass
class UserFeatures:
    """用户characteristics向量"""
    user_id: str
    # 基础characteristics
    recency_days: float = 0        # 最近一次活跃距今天数
    frequency: float = 0           # 活跃频次
    monetary: float = 0            # 消费金额
    
    # 行为characteristics
    session_count: float = 0       # 会话数
    avg_session_duration: float = 0 # 平均会话时长(分钟)
    page_views: float = 0          # 页面浏览量
    feature_usage_depth: float = 0 # 功能使用深度(0-1)
    social_actions: float = 0      # 社交行为次数(分享/评论等)
    
    # 产品characteristics
    account_age_days: float = 0    # 账龄(天)
    plan_tier: int = 0             # 套餐级别(0=免费 1=基础 2=高级 3=企业)
    integrations_count: int = 0    # 集成功能数
    team_size: int = 0             # 团队规模
    
    # 衍生characteristics
    engagement_score: float = 0    # 参与度评分(0-1)
    health_score: float = 0        # 账户健康度(0-1)
    
    extra_features: Dict[str, float] = field(default_factory=dict)
    
    def to_vector(self) -> List[float]:
        """转换为characteristics向量"""
        return [
            self.recency_days, self.frequency, self.monetary,
            self.session_count, self.avg_session_duration, self.page_views,
            self.feature_usage_depth, self.social_actions,
            self.account_age_days, self.plan_tier, self.integrations_count,
            self.team_size, self.engagement_score, self.health_score,
            *list(self.extra_features.values())
        ]
    
    def to_rfm(self) -> Tuple[float, float, float]:
        """返回RFM值(已标准化到1-5)"""
        # 标准化recency: 越小越好
        r_score = max(1, min(5, 5 - self.recency_days / 30))
        f_score = max(1, min(5, self.frequency / 4))
        m_score = max(1, min(5, self.monetary / 200))
        return r_score, f_score, m_score

@dataclass
class ClassificationResult:
    """分类结果"""
    user_id: str
    task: ClassificationTask
    prediction: str                # 预测类别
    probability: float             # 预测概率/置信度
    risk_score: float              # 风险评分(0=低风险 1=高风险)
    segment: Optional[UserSegment] = None  # 用户分层
    feature_importance: Dict[str, float] = field(default_factory=dict)
    explanations: List[str] = field(default_factory=list)  # 预测解释
    recommended_actions: List[str] = field(default_factory=list)
    model_version: str = "1.0.0"
    predicted_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'task': self.task.value,
            'prediction': self.prediction,
            'probability': round(self.probability, 4),
            'risk_score': round(self.risk_score, 4),
            'segment': self.segment.value if self.segment else None,
            'feature_importance': {k: round(v, 4) for k, v in self.feature_importance.items()},
            'explanations': self.explanations,
            'recommended_actions': self.recommended_actions,
            'model_version': self.model_version,
            'predicted_at': self.predicted_at
        }

class UserClassifier:
    """用户分类器"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else ML_CLASSIFIER_DIR
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 模型配置
        self.models: Dict[str, Dict] = {}
        self.training_history: List[Dict] = []
        
        # RFM分层阈值配置
        self.rfm_thresholds = {
            'r_high': 4.0, 'r_low': 2.5,
            'f_high': 4.0, 'f_low': 2.5,
            'm_high': 4.0, 'm_low': 2.5
        }
        
        # init模型
        self._init_models()
    
    def _init_models(self):
        """init分类模型(规则+统计方法)"""
        self.models = {
            ClassificationTask.CHURN_PREDICTION: {
                'type': 'rule_based',
                'thresholds': {
                    'high_risk_recency': 30,      # 超过30天未登录=高风险
                    'high_risk_frequency_drop': 0.5,  # 频次下降50%=高风险
                    'medium_risk_recency': 14,
                    'engagement_floor': 0.2
                }
            },
            ClassificationTask.VALUE_SEGMENTATION: {
                'type': 'rfm',
                'method': 'quintile'
            },
            ClassificationTask.CONVERSION_PREDICTION: {
                'type': 'logistic',
                'key_features': ['engagement_score', 'session_count', 'feature_usage_depth']
            }
        }
    
    def predict(self, features: UserFeatures, 
                task: ClassificationTask = ClassificationTask.CHURN_PREDICTION) -> ClassificationResult:
        """预测单个用户"""
        
        if task == ClassificationTask.CHURN_PREDICTION:
            return self._predict_churn(features)
        elif task == ClassificationTask.VALUE_SEGMENTATION:
            return self._predict_value_segment(features)
        elif task == ClassificationTask.CONVERSION_PREDICTION:
            return self._predict_conversion(features)
        else:
            return self._predict_general(features, task)
    
    def predict_batch(self, features_list: List[UserFeatures],
                      task: ClassificationTask) -> List[ClassificationResult]:
        """批量预测"""
        return [self.predict(f, task) for f in features_list]
    
    def segment_users(self, features_list: List[UserFeatures]) -> Dict[str, List[str]]:
        """用户分层(RFM)"""
        segments: Dict[str, List[str]] = {seg.value: [] for seg in UserSegment}
        
        for features in features_list:
            result = self._predict_value_segment(features)
            if result.segment:
                segments[result.segment.value].append(features.user_id)
        
        return {k: v for k, v in segments.items() if v}  # 只返回非空分层
    
    def get_at_risk_users(self, features_list: List[UserFeatures],
                          risk_threshold: float = 0.7) -> List[ClassificationResult]:
        """get高风险流失用户"""
        at_risk = []
        for features in features_list:
            result = self._predict_churn(features)
            if result.risk_score >= risk_threshold:
                at_risk.append(result)
        
        # 按风险分从高到低排序
        return sorted(at_risk, key=lambda x: x.risk_score, reverse=True)
    
    def _predict_churn(self, features: UserFeatures) -> ClassificationResult:
        """预测流失风险(规则+评分模型)"""
        model = self.models[ClassificationTask.CHURN_PREDICTION]
        thresholds = model['thresholds']
        
        # 多因素评分
        risk_factors = {}
        
        # 1. 活跃度因素(权重最高)
        if features.recency_days > thresholds['high_risk_recency']:
            risk_factors['long_inactive'] = min(1.0, features.recency_days / 60)
        elif features.recency_days > thresholds['medium_risk_recency']:
            risk_factors['somewhat_inactive'] = 0.4
        else:
            risk_factors['recently_active'] = -0.3  # 负分=降低风险
        
        # 2. 参与度因素
        if features.engagement_score < thresholds['engagement_floor']:
            risk_factors['low_engagement'] = 0.5
        elif features.engagement_score > 0.7:
            risk_factors['high_engagement'] = -0.4
        
        # 3. 频次因素
        if features.frequency < 2:
            risk_factors['low_frequency'] = 0.35
        
        # 4. 账户健康度
        if features.health_score < 0.3:
            risk_factors['poor_health'] = 0.4
        
        # 5. 功能使用深度
        if features.feature_usage_depth < 0.2:
            risk_factors['shallow_usage'] = 0.25
        
        # synthesize评分
        risk_score = min(1.0, max(0.0, 
            0.5 + sum(risk_factors.values())
        ))
        
        churn = risk_score >= 0.6
        
        # generate解释
        explanations = []
        if risk_factors.get('long_inactive', 0) > 0.3:
            explanations.append(f"已 {int(features.recency_days)} 天未活跃")
        if risk_factors.get('low_engagement', 0) > 0:
            explanations.append(f"参与度较低({features.engagement_score:.1%})")
        if risk_factors.get('low_frequency', 0) > 0:
            explanations.append(f"使用频次低({features.frequency:.0f}次/月)")
        if risk_factors.get('shallow_usage', 0) > 0:
            explanations.append(f"功能使用较浅({features.feature_usage_depth:.1%})")
        
        # 推荐action
        actions = []
        if risk_score > 0.7:
            actions = ["立即发送个性化挽回邮件", "提供专属续费优惠", "安排客户成功经理主动联系"]
        elif risk_score > 0.5:
            actions = ["推送使用技巧通知", "提供功能引导教程", "邀请参加用户反馈调研"]
        else:
            actions = ["定期发送价值报告", "推荐高级功能尝试"]
        
        # characteristics重要性
        feature_importance = {
            'recency': 0.35,
            'engagement_score': 0.25,
            'frequency': 0.20,
            'health_score': 0.12,
            'feature_usage_depth': 0.08
        }
        
        return ClassificationResult(
            user_id=features.user_id,
            task=ClassificationTask.CHURN_PREDICTION,
            prediction='churn' if churn else 'retain',
            probability=risk_score if churn else 1 - risk_score,
            risk_score=risk_score,
            feature_importance=feature_importance,
            explanations=explanations,
            recommended_actions=actions
        )
    
    def _predict_value_segment(self, features: UserFeatures) -> ClassificationResult:
        """预测价值分层(RFM模型)"""
        r, f, m = features.to_rfm()
        th = self.rfm_thresholds
        
        # RFM分层规则
        if r >= th['r_high'] and f >= th['f_high'] and m >= th['m_high']:
            segment = UserSegment.CHAMPIONS
        elif r >= th['r_high'] and f >= th['f_high']:
            segment = UserSegment.LOYAL
        elif r >= th['r_high'] and f < th['f_low']:
            segment = UserSegment.NEW_CUSTOMERS
        elif r >= th['r_high']:
            segment = UserSegment.POTENTIAL_LOYAL
        elif f >= th['f_high'] and m >= th['m_high'] and r < th['r_low']:
            segment = UserSegment.AT_RISK
        elif m >= th['m_high'] and r < th['r_low']:
            segment = UserSegment.CANT_LOSE
        elif r < th['r_low'] and f < th['f_low'] and m < th['m_low']:
            segment = UserSegment.LOST if features.recency_days > 90 else UserSegment.HIBERNATING
        elif r < th['r_low']:
            segment = UserSegment.ABOUT_TO_SLEEP
        else:
            segment = UserSegment.NEED_ATTENTION
        
        # 价值评分 (0-1)
        value_score = (r * 0.35 + f * 0.35 + m * 0.30) / 5.0
        
        # 分层专属建议
        segment_actions = {
            UserSegment.CHAMPIONS: ["邀请成为品牌大使", "提供VIP专属权益", "内测新功能"],
            UserSegment.LOYAL: ["推荐升级更高套餐", "提供年付优惠", "建立专属沟通渠道"],
            UserSegment.AT_RISK: ["发送个性化挽留活动", "提供续费激励", "了解使用痛点"],
            UserSegment.CANT_LOSE: ["最高优先级人工介入", "提供专属优惠", "深度了解需求"],
            UserSegment.NEW_CUSTOMERS: ["强化onboarding流程", "推送功能引导", "设置阶段性目标"],
            UserSegment.LOST: ["低成本再营销尝试", "提供回归礼包"],
            UserSegment.NEED_ATTENTION: ["提供使用指导", "激活沉睡功能", "推送成功案例"]
        }
        
        return ClassificationResult(
            user_id=features.user_id,
            task=ClassificationTask.VALUE_SEGMENTATION,
            prediction=segment.value,
            probability=value_score,
            risk_score=1 - value_score,
            segment=segment,
            feature_importance={'recency': 0.35, 'frequency': 0.35, 'monetary': 0.30},
            explanations=[f"RFM评分: R={r:.1f} F={f:.1f} M={m:.1f}"],
            recommended_actions=segment_actions.get(segment, ["持续跟踪用户状态"])
        )
    
    def _predict_conversion(self, features: UserFeatures) -> ClassificationResult:
        """预测转化概率(逻辑回归简化版)"""
        # 关键characteristics加权
        weights = {
            'engagement_score': 0.30,
            'session_count': 0.25,
            'feature_usage_depth': 0.20,
            'frequency': 0.15,
            'social_actions': 0.10
        }
        
        # 标准化characteristics值
        normalized = {
            'engagement_score': features.engagement_score,
            'session_count': min(1.0, features.session_count / 20),
            'feature_usage_depth': features.feature_usage_depth,
            'frequency': min(1.0, features.frequency / 10),
            'social_actions': min(1.0, features.social_actions / 5)
        }
        
        # Sigmoid计算
        linear_combination = sum(
            weights[k] * normalized[k] for k in weights
        )
        # Sigmoid函数
        prob = 1 / (1 + math.exp(-5 * (linear_combination - 0.5)))
        
        actions = []
        if prob >= 0.7:
            actions = ["发送升级邀请", "提供限时优惠", "展示高级功能价值"]
        elif prob >= 0.4:
            actions = ["推送成功案例", "触发试用提示", "建立参照物对比"]
        else:
            actions = ["继续培育engagement", "提供价值教育内容"]
        
        return ClassificationResult(
            user_id=features.user_id,
            task=ClassificationTask.CONVERSION_PREDICTION,
            prediction='will_convert' if prob >= 0.5 else 'will_not_convert',
            probability=prob,
            risk_score=1 - prob,
            feature_importance=weights,
            explanations=[
                f"参与度: {features.engagement_score:.1%}",
                f"功能使用深度: {features.feature_usage_depth:.1%}"
            ],
            recommended_actions=actions
        )
    
    def _predict_general(self, features: UserFeatures, task: ClassificationTask) -> ClassificationResult:
        """通用预测"""
        score = features.engagement_score
        return ClassificationResult(
            user_id=features.user_id,
            task=task,
            prediction='positive' if score > 0.5 else 'negative',
            probability=score,
            risk_score=1 - score
        )
    
    def generate_segment_report(self, features_list: List[UserFeatures]) -> Dict[str, Any]:
        """generate分层报告"""
        segments = self.segment_users(features_list)
        at_risk = self.get_at_risk_users(features_list, 0.65)
        
        total = len(features_list)
        
        return {
            'total_users': total,
            'segment_distribution': {
                seg: {'count': len(ids), 'pct': round(len(ids)/total*100, 1)}
                for seg, ids in segments.items()
            },
            'at_risk_count': len(at_risk),
            'at_risk_pct': round(len(at_risk)/total*100, 1),
            'top_risk_users': [r.user_id for r in at_risk[:10]],
            'recommendations': {
                'high_priority': [
                    f"立即跟进 {len(at_risk)} 个高风险流失用户",
                    f"重点激活 {len(segments.get('hibernating', []))} 个冬眠用户"
                ],
                'medium_priority': [
                    f"培育 {len(segments.get('potential_loyal', []))} 个潜力用户",
                    f"维系 {len(segments.get('champions', []))} 个冠军用户"
                ]
            },
            'generated_at': datetime.now().isoformat()
        }
