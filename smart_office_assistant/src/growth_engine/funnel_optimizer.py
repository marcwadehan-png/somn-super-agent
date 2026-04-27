"""
__all__ = [
    'analyze_stage',
    'build_funnel',
    'export_experiments',
    'export_funnel',
    'generate_experiments',
    'get_funnel_stages',
    'predict_impact',
]

漏斗优化器 - Funnel Optimizer
基于增长方法论,实现漏斗分析与优化
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class FunnelStage(Enum):
    """漏斗阶段"""
    TRAFFIC = "traffic"             # 流量
    VISITOR = "visitor"             # 访客
    LEAD = "lead"                   # 线索
    MQL = "mql"                     # 营销合格线索
    SQL = "sql"                     # 销售合格线索
    OPPORTUNITY = "opportunity"     # 商机
    CUSTOMER = "customer"           # 客户
    ACTIVATED = "activated"         # 激活用户
    RETAINED = "retained"           # 留存用户
    REFERRER = "referrer"           # 推荐用户

@dataclass
class FunnelMetrics:
    """漏斗metrics"""
    stage: FunnelStage
    stage_name: str
    
    # 用户数量
    users: int
    
    # 转化数据
    conversion_rate: float  # 相对于上一阶段
    drop_off_count: int
    drop_off_rate: float
    
    # 时间数据
    avg_time_to_convert: int  # 分钟
    
    # 价值数据
    avg_value: float = 0.0
    total_value: float = 0.0
    
    # 基准对比
    benchmark_rate: float = 0.0
    vs_benchmark: float = 0.0  # 与基准的差异百分比

@dataclass
class Funnel:
    """漏斗"""
    id: str
    name: str
    description: str
    
    # 漏斗阶段
    stages: List[FunnelMetrics] = field(default_factory=list)
    
    # 整体metrics
    overall_conversion_rate: float = 0.0  # 整体转化率
    total_users_in: int = 0
    total_users_out: int = 0
    
    # 问题recognize
    bottlenecks: List[Dict] = field(default_factory=list)
    opportunities: List[Dict] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class OptimizationExperiment:
    """优化实验"""
    id: str
    name: str
    description: str
    
    # 目标
    target_stage: str
    target_metric: str
    current_value: float
    target_value: float
    
    # 实验设计
    hypothesis: str
    variations: List[Dict]  # A/B测试变体
    
    # 预期效果
    expected_lift: float  # 预期提升百分比
    confidence: float  # 置信度
    
    # 资源
    effort: str  # low/medium/high
    duration: str  # 实验周期
    
    # 优先级
    priority_score: float = 0.0
    
    status: str = "planned"  # planned/running/completed/cancelled

class FunnelOptimizer:
    """
    漏斗优化器
    
    核心功能:
    1. 漏斗构建 - 定义和构建漏斗
    2. 漏斗分析 - 量化各阶段表现
    3. 瓶颈recognize - 发现转化瓶颈
    4. 实验设计 - generate优化实验
    5. 效果预测 - 预测优化效果
    """
    
    def __init__(self):
        self.funnel_templates = self._init_funnel_templates()
        self.benchmarks = self._init_benchmarks()
        
    def _init_funnel_templates(self) -> Dict:
        """init漏斗模板"""
        return {
            "saas_conversion": {
                "name": "SaaS转化漏斗",
                "stages": [
                    {"stage": "traffic", "name": "流量", "benchmark": 1.0},
                    {"stage": "visitor", "name": "访客", "benchmark": 0.5},
                    {"stage": "lead", "name": "线索", "benchmark": 0.1},
                    {"stage": "mql", "name": "MQL", "benchmark": 0.05},
                    {"stage": "sql", "name": "SQL", "benchmark": 0.02},
                    {"stage": "opportunity", "name": "商机", "benchmark": 0.01},
                    {"stage": "customer", "name": "客户", "benchmark": 0.005}
                ]
            },
            "ecommerce_purchase": {
                "name": "电商购买漏斗",
                "stages": [
                    {"stage": "traffic", "name": "流量", "benchmark": 1.0},
                    {"stage": "visitor", "name": "访客", "benchmark": 0.8},
                    {"stage": "lead", "name": "加购", "benchmark": 0.15},
                    {"stage": "opportunity", "name": "结算", "benchmark": 0.08},
                    {"stage": "customer", "name": "成交", "benchmark": 0.04}
                ]
            },
            "product_growth": {
                "name": "产品增长漏斗",
                "stages": [
                    {"stage": "traffic", "name": "新用户", "benchmark": 1.0},
                    {"stage": "visitor", "name": "注册", "benchmark": 0.3},
                    {"stage": "activated", "name": "激活", "benchmark": 0.15},
                    {"stage": "retained", "name": "留存", "benchmark": 0.08},
                    {"stage": "referrer", "name": "推荐", "benchmark": 0.02}
                ]
            },
            "content_conversion": {
                "name": "内容转化漏斗",
                "stages": [
                    {"stage": "traffic", "name": "曝光", "benchmark": 1.0},
                    {"stage": "visitor", "name": "点击", "benchmark": 0.05},
                    {"stage": "lead", "name": "阅读", "benchmark": 0.02},
                    {"stage": "mql", "name": "互动", "benchmark": 0.005},
                    {"stage": "customer", "name": "转化", "benchmark": 0.001}
                ]
            }
        }
    
    def _init_benchmarks(self) -> Dict:
        """init行业基准"""
        return {
            "saas_b2b": {
                "visitor_to_lead": {"excellent": "> 10%", "good": "5-10%", "average": "< 5%"},
                "lead_to_mql": {"excellent": "> 50%", "good": "30-50%", "average": "< 30%"},
                "mql_to_sql": {"excellent": "> 40%", "good": "25-40%", "average": "< 25%"},
                "sql_to_customer": {"excellent": "> 25%", "good": "15-25%", "average": "< 15%"},
                "overall_conversion": {"excellent": "> 2%", "good": "1-2%", "average": "< 1%"}
            },
            "ecommerce": {
                "add_to_cart_rate": {"excellent": "> 15%", "good": "10-15%", "average": "< 10%"},
                "cart_to_checkout": {"excellent": "> 60%", "good": "40-60%", "average": "< 40%"},
                "checkout_to_purchase": {"excellent": "> 50%", "good": "30-50%", "average": "< 30%"},
                "overall_conversion": {"excellent": "> 4%", "good": "2-4%", "average": "< 2%"}
            },
            "saas_b2c": {
                "signup_rate": {"excellent": "> 30%", "good": "15-30%", "average": "< 15%"},
                "activation_rate": {"excellent": "> 60%", "good": "40-60%", "average": "< 40%"},
                "d1_retention": {"excellent": "> 50%", "good": "35-50%", "average": "< 35%"},
                "d7_retention": {"excellent": "> 25%", "good": "15-25%", "average": "< 15%"}
            }
        }
    
    def build_funnel(
        self,
        funnel_type: str,
        actual_data: Dict[str, int],
        custom_stages: Optional[List[Dict]] = None
    ) -> Funnel:
        """
        构建漏斗
        
        Args:
            funnel_type: 漏斗类型 (saas_conversion/ecommerce_purchase/product_growth/content_conversion)
            actual_data: 实际数据 {stage_name: user_count}
            custom_stages: 自定义阶段(可选)
        
        Returns:
            Funnel
        """
        # get模板
        template = self.funnel_templates.get(funnel_type, self.funnel_templates["saas_conversion"])
        stages_config = custom_stages or template["stages"]
        
        stages = []
        prev_users = None
        
        for i, stage_config in enumerate(stages_config):
            stage = FunnelStage(stage_config["stage"])
            stage_name = stage_config["name"]
            
            # get实际用户数
            users = actual_data.get(stage.value, actual_data.get(stage_name, 0))
            
            # 计算转化数据
            if prev_users and prev_users > 0:
                conversion_rate = users / prev_users
                drop_off_count = prev_users - users
                drop_off_rate = drop_off_count / prev_users
            else:
                conversion_rate = 1.0 if i == 0 else 0.0
                drop_off_count = 0
                drop_off_rate = 0.0
            
            # 基准对比
            benchmark = stage_config.get("benchmark", 0.5)
            vs_benchmark = (conversion_rate - benchmark) / benchmark * 100 if benchmark > 0 else 0
            
            metrics = FunnelMetrics(
                stage=stage,
                stage_name=stage_name,
                users=users,
                conversion_rate=conversion_rate,
                drop_off_count=drop_off_count,
                drop_off_rate=drop_off_rate,
                avg_time_to_convert=0,  # 可由外部传入
                benchmark_rate=benchmark,
                vs_benchmark=vs_benchmark
            )
            stages.append(metrics)
            prev_users = users
        
        # 计算整体metrics
        total_in = stages[0].users if stages else 0
        total_out = stages[-1].users if stages else 0
        overall_rate = total_out / total_in if total_in > 0 else 0
        
        funnel = Funnel(
            id=f"funnel_{funnel_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=template["name"],
            description=f"基于{funnel_type}模板构建的转化漏斗",
            stages=stages,
            overall_conversion_rate=overall_rate,
            total_users_in=total_in,
            total_users_out=total_out
        )
        
        # recognize瓶颈和机会
        funnel.bottlenecks = self._identify_bottlenecks(funnel)
        funnel.opportunities = self._identify_opportunities(funnel)
        
        logger.info(f"漏斗构建完成: {funnel.id}, {len(stages)} 个阶段")
        return funnel
    
    def _identify_bottlenecks(self, funnel: Funnel) -> List[Dict]:
        """recognize瓶颈"""
        bottlenecks = []
        
        for i, stage in enumerate(funnel.stages):
            if i == 0:
                continue  # 跳过第一阶段
            
            # judge是否为瓶颈
            is_bottleneck = False
            severity = "low"
            
            # 转化率低于基准20%以上
            if stage.vs_benchmark < -20:
                is_bottleneck = True
                severity = "high"
            elif stage.vs_benchmark < -10:
                is_bottleneck = True
                severity = "medium"
            
            # 转化率绝对值过低
            if stage.conversion_rate < 0.1:
                is_bottleneck = True
                severity = "high"
            
            if is_bottleneck:
                bottleneck = {
                    "stage": stage.stage_name,
                    "stage_value": stage.stage.value,
                    "conversion_rate": f"{stage.conversion_rate*100:.1f}%",
                    "benchmark": f"{stage.benchmark_rate*100:.1f}%",
                    "vs_benchmark": f"{stage.vs_benchmark:+.1f}%",
                    "drop_off_count": stage.drop_off_count,
                    "severity": severity,
                    "priority": "immediate" if severity == "high" else "short_term"
                }
                bottlenecks.append(bottleneck)
        
        return bottlenecks
    
    def _identify_opportunities(self, funnel: Funnel) -> List[Dict]:
        """recognize机会"""
        opportunities = []
        
        for i, stage in enumerate(funnel.stages):
            if i == 0:
                continue
            
            # 接近基准但还有提升空间
            if -10 <= stage.vs_benchmark < 0:
                opportunity = {
                    "stage": stage.stage_name,
                    "current_rate": f"{stage.conversion_rate*100:.1f}%",
                    "target_rate": f"{stage.benchmark_rate*100:.1f}%",
                    "potential_users": int(stage.users * (stage.benchmark_rate / stage.conversion_rate - 1)) if stage.conversion_rate > 0 else 0,
                    "type": "close_gap",
                    "effort": "medium"
                }
                opportunities.append(opportunity)
            
            # 超过基准,可以进一步优化
            elif stage.vs_benchmark > 10:
                opportunity = {
                    "stage": stage.stage_name,
                    "current_rate": f"{stage.conversion_rate*100:.1f}%",
                    "performance": "above_benchmark",
                    "insight": "该阶段表现优异,可研究成功因素复制到其他阶段",
                    "type": "best_practice",
                    "effort": "low"
                }
                opportunities.append(opportunity)
        
        # 整体优化机会
        if funnel.overall_conversion_rate < 0.01:
            opportunities.append({
                "stage": "整体",
                "current_rate": f"{funnel.overall_conversion_rate*100:.2f}%",
                "target_rate": "1%+",
                "type": "overall_optimization",
                "priority": "high",
                "effort": "high"
            })
        
        return opportunities
    
    def analyze_stage(
        self,
        funnel: Funnel,
        stage_value: str,
        detailed_data: Optional[Dict] = None
    ) -> Dict:
        """
        深度分析单个阶段
        
        Args:
            funnel: 漏斗对象
            stage_value: 阶段标识
            detailed_data: 详细数据
        
        Returns:
            阶段分析报告
        """
        # 找到对应阶段
        stage_metrics = None
        for s in funnel.stages:
            if s.stage.value == stage_value:
                stage_metrics = s
                break
        
        if not stage_metrics:
            return {"error": f"阶段 {stage_value} 不存在"}
        
        analysis = {
            "stage": stage_metrics.stage_name,
            "metrics": {
                "users": stage_metrics.users,
                "conversion_rate": f"{stage_metrics.conversion_rate*100:.1f}%",
                "drop_off_rate": f"{stage_metrics.drop_off_rate*100:.1f}%",
                "drop_off_count": stage_metrics.drop_off_count,
                "vs_benchmark": f"{stage_metrics.vs_benchmark:+.1f}%"
            },
            "performance_rating": self._rate_performance(stage_metrics),
            "diagnosis": self._diagnose_stage(stage_metrics, detailed_data),
            "recommendations": self._recommend_for_stage(stage_metrics)
        }
        
        return analysis
    
    def _rate_performance(self, metrics: FunnelMetrics) -> str:
        """评级阶段表现"""
        if metrics.vs_benchmark > 10:
            return "优秀"
        elif metrics.vs_benchmark > -10:
            return "良好"
        elif metrics.vs_benchmark > -20:
            return "待改善"
        else:
            return "需重点关注"
    
    def _diagnose_stage(self, metrics: FunnelMetrics, detailed_data: Optional[Dict]) -> List[str]:
        """诊断阶段问题"""
        diagnoses = []
        
        if metrics.conversion_rate < 0.1:
            diagnoses.append(f"转化率过低 ({metrics.conversion_rate*100:.1f}%),存在严重流失")
        
        if metrics.vs_benchmark < -20:
            diagnoses.append(f"显著低于行业基准 ({metrics.vs_benchmark:+.1f}%),竞争力不足")
        
        if metrics.drop_off_count > metrics.users * 2:
            diagnoses.append("流失用户数量远超转化用户,需优化用户体验")
        
        if not diagnoses:
            diagnoses.append("该阶段表现正常,可继续监控")
        
        return diagnoses
    
    def _recommend_for_stage(self, metrics: FunnelMetrics) -> List[str]:
        """generate阶段优化建议"""
        recommendations = []
        stage = metrics.stage
        
        if stage == FunnelStage.VISITOR:
            recommendations.extend([
                "优化落地页加载速度",
                "提升首屏内容吸引力",
                "优化CTA按钮文案和位置"
            ])
        elif stage == FunnelStage.LEAD:
            recommendations.extend([
                "简化表单字段",
                "增加社交证明",
                "提供有价值的内容交换"
            ])
        elif stage == FunnelStage.MQL:
            recommendations.extend([
                "建立评分模型筛选高质量线索",
                "个性化 nurture 流程",
                "增加互动触点"
            ])
        elif stage == FunnelStage.CUSTOMER:
            recommendations.extend([
                "优化定价页面",
                "增加信任背书",
                "简化购买流程"
            ])
        elif stage == FunnelStage.ACTIVATED:
            recommendations.extend([
                "优化 onboarding 流程",
                "快速展示核心价值",
                "减少首次使用摩擦"
            ])
        
        return recommendations[:3]
    
    def generate_experiments(
        self,
        funnel: Funnel,
        max_experiments: int = 5
    ) -> List[OptimizationExperiment]:
        """
        generate优化实验
        
        Args:
            funnel: 漏斗对象
            max_experiments: 最大实验数量
        
        Returns:
            实验列表
        """
        experiments = []
        exp_counter = 0
        
        # 基于瓶颈generate实验
        for bottleneck in funnel.bottlenecks[:3]:
            exp_counter += 1
            
            experiment = self._create_experiment_for_bottleneck(bottleneck, exp_counter)
            experiments.append(experiment)
        
        # 基于机会generate实验
        for opportunity in funnel.opportunities[:2]:
            if len(experiments) >= max_experiments:
                break
            
            exp_counter += 1
            experiment = self._create_experiment_for_opportunity(opportunity, exp_counter)
            experiments.append(experiment)
        
        # 按优先级排序
        experiments.sort(key=lambda e: e.priority_score, reverse=True)
        
        logger.info(f"generate {len(experiments)} 个优化实验")
        return experiments
    
    def _create_experiment_for_bottleneck(self, bottleneck: Dict, counter: int) -> OptimizationExperiment:
        """为瓶颈创建实验"""
        stage = bottleneck["stage"]
        severity = bottleneck.get("severity", "medium")
        
        # 根据严重程度确定参数
        if severity == "high":
            expected_lift = 0.30
            confidence = 0.7
            effort = "high"
            duration = "4周"
        elif severity == "medium":
            expected_lift = 0.20
            confidence = 0.6
            effort = "medium"
            duration = "2-3周"
        else:
            expected_lift = 0.10
            confidence = 0.5
            effort = "low"
            duration = "1-2周"
        
        # 计算优先级分数
        priority_score = expected_lift * confidence * (2 if severity == "high" else 1)
        
        return OptimizationExperiment(
            id=f"exp_{counter:03d}",
            name=f"优化{stage}转化",
            description=f"针对{stage}阶段转化率低的问题进行优化",
            target_stage=stage,
            target_metric="conversion_rate",
            current_value=float(bottleneck["conversion_rate"].replace("%", "")) / 100,
            target_value=float(bottleneck["conversion_rate"].replace("%", "")) / 100 * (1 + expected_lift),
            hypothesis=f"通过优化{stage}的用户体验,可以提升转化率{expected_lift*100:.0f}%",
            variations=[
                {"name": "对照组", "description": "当前版本"},
                {"name": "实验组", "description": "优化版本"}
            ],
            expected_lift=expected_lift,
            confidence=confidence,
            effort=effort,
            duration=duration,
            priority_score=priority_score
        )
    
    def _create_experiment_for_opportunity(self, opportunity: Dict, counter: int) -> OptimizationExperiment:
        """为机会创建实验"""
        stage = opportunity["stage"]
        opp_type = opportunity.get("type", "general")
        
        return OptimizationExperiment(
            id=f"exp_{counter:03d}",
            name=f"提升{stage}表现",
            description=f"把握{stage}阶段的优化机会",
            target_stage=stage,
            target_metric="conversion_rate",
            current_value=float(opportunity.get("current_rate", "0%").replace("%", "")) / 100,
            target_value=float(opportunity.get("target_rate", "0%").replace("%", "")) / 100,
            hypothesis=f"通过针对性优化,达到行业基准水平",
            variations=[
                {"name": "对照组", "description": "当前版本"},
                {"name": "实验组", "description": "优化版本"}
            ],
            expected_lift=0.15,
            confidence=0.6,
            effort=opportunity.get("effort", "medium"),
            duration="2-3周",
            priority_score=0.5
        )
    
    def predict_impact(
        self,
        funnel: Funnel,
        improvements: Dict[str, float]
    ) -> Dict:
        """
        预测优化效果
        
        Args:
            funnel: 漏斗对象
            improvements: 各阶段预期提升 {stage_value: improvement_rate}
        
        Returns:
            预测结果
        """
        # 计算当前各阶段用户数
        current_users = {s.stage.value: s.users for s in funnel.stages}
        
        # 应用提升
        predicted_users = current_users.copy()
        for stage_value, improvement in improvements.items():
            if stage_value in predicted_users:
                # 找到该阶段在漏斗中的位置
                for i, s in enumerate(funnel.stages):
                    if s.stage.value == stage_value and i > 0:
                        prev_stage = funnel.stages[i-1]
                        new_conversion = s.conversion_rate * (1 + improvement)
                        predicted_users[stage_value] = int(prev_stage.users * new_conversion)
        
        # 计算整体影响
        current_final = funnel.stages[-1].users if funnel.stages else 0
        predicted_final = predicted_users.get(funnel.stages[-1].stage.value, current_final)
        
        overall_lift = (predicted_final - current_final) / current_final if current_final > 0 else 0
        
        return {
            "current_final_users": current_final,
            "predicted_final_users": predicted_final,
            "absolute_increase": predicted_final - current_final,
            "overall_lift": f"{overall_lift*100:.1f}%",
            "stage_impacts": [
                {
                    "stage": s.stage_name,
                    "current": current_users.get(s.stage.value, 0),
                    "predicted": predicted_users.get(s.stage.value, 0),
                    "improvement": improvements.get(s.stage.value, 0)
                }
                for s in funnel.stages
            ]
        }
    
    def export_funnel(self, funnel: Funnel, format: str = "yaml") -> str:
        """导出漏斗"""
        funnel_data = {
            "id": funnel.id,
            "name": funnel.name,
            "description": funnel.description,
            "summary": {
                "total_users_in": funnel.total_users_in,
                "total_users_out": funnel.total_users_out,
                "overall_conversion_rate": f"{funnel.overall_conversion_rate*100:.2f}%"
            },
            "stages": [
                {
                    "stage": s.stage.value,
                    "name": s.stage_name,
                    "users": s.users,
                    "conversion_rate": f"{s.conversion_rate*100:.1f}%",
                    "drop_off_count": s.drop_off_count,
                    "drop_off_rate": f"{s.drop_off_rate*100:.1f}%",
                    "vs_benchmark": f"{s.vs_benchmark:+.1f}%"
                }
                for s in funnel.stages
            ],
            "bottlenecks": funnel.bottlenecks,
            "opportunities": funnel.opportunities,
            "created_at": funnel.created_at
        }
        
        if format == "yaml":
            return yaml.dump(funnel_data, allow_unicode=True, default_flow_style=False)
        else:
            return json.dumps(funnel_data, ensure_ascii=False, indent=2)
    
    def export_experiments(self, experiments: List[OptimizationExperiment], format: str = "yaml") -> str:
        """导出实验计划"""
        exp_data = {
            "experiments": [
                {
                    "id": e.id,
                    "name": e.name,
                    "description": e.description,
                    "target": {
                        "stage": e.target_stage,
                        "metric": e.target_metric,
                        "current": f"{e.current_value*100:.1f}%",
                        "target": f"{e.target_value*100:.1f}%"
                    },
                    "hypothesis": e.hypothesis,
                    "expected_lift": f"{e.expected_lift*100:.0f}%",
                    "confidence": f"{e.confidence*100:.0f}%",
                    "effort": e.effort,
                    "duration": e.duration,
                    "priority_score": round(e.priority_score, 2),
                    "status": e.status
                }
                for e in experiments
            ],
            "summary": {
                "total_experiments": len(experiments),
                "high_priority": len([e for e in experiments if e.priority_score > 0.5]),
                "total_expected_impact": f"{sum(e.expected_lift for e in experiments)*100:.0f}%"
            }
        }
        
        if format == "yaml":
            return yaml.dump(exp_data, allow_unicode=True, default_flow_style=False)
        else:
            return json.dumps(exp_data, ensure_ascii=False, indent=2)
    
    def get_funnel_stages(self) -> List[str]:
        """get漏斗阶段列表"""
        return [stage.value for stage in FunnelStage]
