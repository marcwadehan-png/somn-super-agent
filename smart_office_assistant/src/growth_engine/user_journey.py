"""
__all__ = [
    'analyze_funnel',
    'export_journey',
    'generate_optimization_plan',
    'get_journey_stages',
    'identify_friction_points',
    'identify_wow_moments',
    'map_journey',
]

用户旅程mapping器 - User Journey Mapper
基于增长方法论,实现用户旅程分析与优化
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class JourneyStage(Enum):
    """用户旅程阶段"""
    AWARENESS = "awareness"         # 认知
    INTEREST = "interest"           # 兴趣
    CONSIDERATION = "consideration" # 考虑
    CONVERSION = "conversion"       # 转化
    ONBOARDING = "onboarding"       # 激活
    ENGAGEMENT = "engagement"       # 参与
    RETENTION = "retention"         # 留存
    ADVOCACY = "advocacy"           # 推荐

class TouchpointType(Enum):
    """触点类型"""
    AD = "ad"                       # 广告
    SEARCH = "search"               # 搜索
    SOCIAL = "social"               # 社交媒体
    EMAIL = "email"                 # 邮件
    WEBSITE = "website"             # 网站
    APP = "app"                     # 应用
    CONTENT = "content"             # 内容
    REFERRAL = "referral"           # 推荐
    CUSTOMER_SERVICE = "customer_service"  # 客服
    COMMUNITY = "community"         # 社区

@dataclass
class Touchpoint:
    """触点"""
    id: str
    name: str
    type: TouchpointType
    stage: JourneyStage
    
    # 触点属性
    description: str
    channel: str
    
    # 效果数据
    traffic: int = 0
    conversion_rate: float = 0.0
    satisfaction: float = 0.0  # 0-1
    
    # 用户行为
    avg_time_spent: int = 0  # 秒
    bounce_rate: float = 0.0
    
    # 优化建议
    pain_points: List[str] = field(default_factory=list)
    improvement_opportunities: List[str] = field(default_factory=list)

@dataclass
class JourneyStep:
    """旅程步骤"""
    id: str
    stage: JourneyStage
    name: str
    description: str
    
    # 用户目标
    user_goal: str
    user_emotion: str  # 用户情绪
    
    # 触点
    touchpoints: List[Touchpoint] = field(default_factory=list)
    
    # 关键行为
    key_actions: List[str] = field(default_factory=list)
    
    # 流失点
    drop_off_rate: float = 0.0
    drop_off_reasons: List[str] = field(default_factory=list)
    
    # 成功标准
    success_criteria: List[str] = field(default_factory=list)

@dataclass
class UserJourney:
    """用户旅程"""
    id: str
    name: str
    persona_id: str
    persona_name: str
    
    # 旅程步骤
    steps: List[JourneyStep] = field(default_factory=list)
    
    # 整体metrics
    total_conversion_rate: float = 0.0
    avg_journey_time: int = 0  # 分钟
    
    # 关键洞察
    friction_points: List[Dict] = field(default_factory=list)
    wow_moments: List[Dict] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class FunnelAnalysis:
    """漏斗分析"""
    stage_name: str
    users_in: int
    users_out: int
    conversion_rate: float
    avg_time: int  # 分钟
    drop_off_reasons: List[str] = field(default_factory=list)
    optimization_suggestions: List[str] = field(default_factory=list)

class UserJourneyMapper:
    """
    用户旅程mapping器
    
    核心功能:
    1. 旅程mapping - 绘制完整用户旅程
    2. 触点分析 - recognize关键触点
    3. 漏斗分析 - 量化各阶段转化
    4. 摩擦点recognize - 发现流失原因
    5. 优化建议 - generate改进方案
    """
    
    def __init__(self):
        self.journey_templates = self._init_journey_templates()
        self.touchpoint_benchmarks = self._init_touchpoint_benchmarks()
        
    def _init_journey_templates(self) -> Dict:
        """init旅程模板"""
        return {
            "saas_b2b": {
                "stages": [
                    {
                        "stage": "awareness",
                        "name": "认知阶段",
                        "user_goal": "了解解决方案",
                        "touchpoints": ["content_marketing", "seo", "social_media", "events"]
                    },
                    {
                        "stage": "consideration",
                        "name": "考虑阶段",
                        "user_goal": "评估产品是否适合",
                        "touchpoints": ["website", "demo_request", "case_studies", "pricing_page"]
                    },
                    {
                        "stage": "conversion",
                        "name": "转化阶段",
                        "user_goal": "完成购买/注册",
                        "touchpoints": ["signup_flow", "sales_call", "pricing_page", "checkout"]
                    },
                    {
                        "stage": "onboarding",
                        "name": "激活阶段",
                        "user_goal": "完成首次价值体验",
                        "touchpoints": ["product_tour", "welcome_email", "in_app_guidance", "support"]
                    },
                    {
                        "stage": "retention",
                        "name": "留存阶段",
                        "user_goal": "持续获得价值",
                        "touchpoints": ["product_usage", "customer_success", "community", "feature_updates"]
                    },
                    {
                        "stage": "advocacy",
                        "name": "推荐阶段",
                        "user_goal": "分享成功经验",
                        "touchpoints": ["referral_program", "testimonials", "case_studies", "community"]
                    }
                ]
            },
            "ecommerce": {
                "stages": [
                    {
                        "stage": "awareness",
                        "name": "认知",
                        "user_goal": "发现商品",
                        "touchpoints": ["ads", "social", "search", "influencer"]
                    },
                    {
                        "stage": "interest",
                        "name": "兴趣",
                        "user_goal": "了解商品详情",
                        "touchpoints": ["product_page", "reviews", "videos", "live_stream"]
                    },
                    {
                        "stage": "consideration",
                        "name": "考虑",
                        "user_goal": "比较和decision",
                        "touchpoints": ["comparison", "reviews", "qa", "coupons"]
                    },
                    {
                        "stage": "conversion",
                        "name": "转化",
                        "user_goal": "完成购买",
                        "touchpoints": ["cart", "checkout", "payment", "confirmation"]
                    },
                    {
                        "stage": "retention",
                        "name": "留存",
                        "user_goal": "再次购买",
                        "touchpoints": ["order_tracking", "customer_service", "loyalty_program", "recommendations"]
                    }
                ]
            }
        }
    
    def _init_touchpoint_benchmarks(self) -> Dict:
        """init触点基准数据"""
        return {
            "landing_page": {
                "bounce_rate": {"excellent": "< 30%", "good": "30-50%", "average": "> 50%"},
                "conversion_rate": {"excellent": "> 5%", "good": "2-5%", "average": "< 2%"},
                "avg_time": {"excellent": "> 3min", "good": "1-3min", "average": "< 1min"}
            },
            "signup_flow": {
                "completion_rate": {"excellent": "> 70%", "good": "50-70%", "average": "< 50%"},
                "time_to_complete": {"excellent": "< 2min", "good": "2-5min", "average": "> 5min"}
            },
            "onboarding": {
                "activation_rate": {"excellent": "> 60%", "good": "40-60%", "average": "< 40%"},
                "time_to_aha": {"excellent": "< 1day", "good": "1-3days", "average": "> 3days"}
            },
            "checkout": {
                "abandonment_rate": {"excellent": "< 60%", "good": "60-70%", "average": "> 70%"},
                "conversion_rate": {"excellent": "> 40%", "good": "25-40%", "average": "< 25%"}
            }
        }
    
    def map_journey(
        self,
        persona_id: str,
        persona_name: str,
        industry: str = "saas_b2b",
        custom_stages: Optional[List[Dict]] = None
    ) -> UserJourney:
        """
        mapping用户旅程
        
        Args:
            persona_id: 用户画像ID
            persona_name: 用户画像名称
            industry: 行业类型
            custom_stages: 自定义阶段(可选)
        
        Returns:
            UserJourney
        """
        # get模板
        template = self.journey_templates.get(industry, self.journey_templates["saas_b2b"])
        stages_config = custom_stages or template["stages"]
        
        steps = []
        step_counter = 0
        
        for stage_config in stages_config:
            step_counter += 1
            stage = JourneyStage(stage_config["stage"])
            
            # 创建触点
            touchpoints = []
            for tp_name in stage_config.get("touchpoints", []):
                tp = Touchpoint(
                    id=f"tp_{step_counter}_{len(touchpoints)+1:02d}",
                    name=tp_name,
                    type=self._infer_touchpoint_type(tp_name),
                    stage=stage,
                    description=f"{stage_config['name']}阶段的{tp_name}触点",
                    channel=self._infer_channel(tp_name)
                )
                touchpoints.append(tp)
            
            # 创建步骤
            step = JourneyStep(
                id=f"step_{step_counter:02d}",
                stage=stage,
                name=stage_config["name"],
                description=f"用户在{stage_config['name']}的行为路径",
                user_goal=stage_config.get("user_goal", ""),
                user_emotion=self._infer_emotion(stage),
                touchpoints=touchpoints,
                key_actions=self._infer_key_actions(stage),
                success_criteria=self._infer_success_criteria(stage)
            )
            steps.append(step)
        
        journey = UserJourney(
            id=f"journey_{persona_id}_{datetime.now().strftime('%Y%m%d')}",
            name=f"{persona_name}的用户旅程",
            persona_id=persona_id,
            persona_name=persona_name,
            steps=steps
        )
        
        logger.info(f"用户旅程mapping完成: {journey.id}, {len(steps)} 个阶段")
        return journey
    
    def _infer_touchpoint_type(self, name: str) -> TouchpointType:
        """推断触点类型"""
        mapping = {
            "ad": TouchpointType.AD,
            "ads": TouchpointType.AD,
            "search": TouchpointType.SEARCH,
            "seo": TouchpointType.SEARCH,
            "social": TouchpointType.SOCIAL,
            "social_media": TouchpointType.SOCIAL,
            "email": TouchpointType.EMAIL,
            "website": TouchpointType.WEBSITE,
            "app": TouchpointType.APP,
            "content": TouchpointType.CONTENT,
            "referral": TouchpointType.REFERRAL,
            "support": TouchpointType.CUSTOMER_SERVICE,
            "community": TouchpointType.COMMUNITY
        }
        return mapping.get(name.lower(), TouchpointType.WEBSITE)
    
    def _infer_channel(self, touchpoint_name: str) -> str:
        """推断渠道"""
        channel_mapping = {
            "ad": "付费广告",
            "ads": "付费广告",
            "search": "搜索引擎",
            "seo": "自然搜索",
            "social": "社交媒体",
            "social_media": "社交媒体",
            "email": "邮件营销",
            "website": "官网",
            "app": "应用内",
            "content": "内容营销",
            "referral": "口碑推荐"
        }
        return channel_mapping.get(touchpoint_name.lower(), "其他")
    
    def _infer_emotion(self, stage: JourneyStage) -> str:
        """推断用户情绪"""
        emotion_map = {
            JourneyStage.AWARENESS: "好奇",
            JourneyStage.INTEREST: "兴趣",
            JourneyStage.CONSIDERATION: "谨慎",
            JourneyStage.CONVERSION: "期待/焦虑",
            JourneyStage.ONBOARDING: "困惑/兴奋",
            JourneyStage.ENGAGEMENT: "满足",
            JourneyStage.RETENTION: "习惯",
            JourneyStage.ADVOCACY: "自豪"
        }
        return emotion_map.get(stage, "中性")
    
    def _infer_key_actions(self, stage: JourneyStage) -> List[str]:
        """推断关键行为"""
        actions_map = {
            JourneyStage.AWARENESS: ["看到广告", "搜索信息", "点击链接"],
            JourneyStage.INTEREST: ["浏览内容", "查看详情", "比较选项"],
            JourneyStage.CONSIDERATION: ["阅读评价", "咨询客服", "试用产品"],
            JourneyStage.CONVERSION: ["填写表单", "完成支付", "确认订单"],
            JourneyStage.ONBOARDING: ["完成注册", "首次使用", "完成引导"],
            JourneyStage.ENGAGEMENT: ["定期使用", "探索功能", "参与互动"],
            JourneyStage.RETENTION: ["持续使用", "升级服务", "复购"],
            JourneyStage.ADVOCACY: ["分享体验", "推荐他人", "撰写评价"]
        }
        return actions_map.get(stage, [])
    
    def _infer_success_criteria(self, stage: JourneyStage) -> List[str]:
        """推断成功标准"""
        criteria_map = {
            JourneyStage.AWARENESS: ["品牌认知度提升", "流量增长"],
            JourneyStage.INTEREST: ["页面停留时间", "内容互动率"],
            JourneyStage.CONSIDERATION: ["试用申请数", "咨询量"],
            JourneyStage.CONVERSION: ["转化率", "客单价"],
            JourneyStage.ONBOARDING: ["激活率", "首次价值体验时间"],
            JourneyStage.ENGAGEMENT: ["使用频率", "功能采用率"],
            JourneyStage.RETENTION: ["留存率", "复购率"],
            JourneyStage.ADVOCACY: ["NPS", "推荐转化率"]
        }
        return criteria_map.get(stage, [])
    
    def analyze_funnel(self, journey: UserJourney, actual_data: Dict) -> List[FunnelAnalysis]:
        """
        漏斗分析
        
        Args:
            journey: 用户旅程
            actual_data: 实际数据 {stage_name: {users_in, users_out, ...}}
        
        Returns:
            漏斗分析结果列表
        """
        funnel_results = []
        
        for i, step in enumerate(journey.steps):
            stage_data = actual_data.get(step.stage.value, {})
            
            users_in = stage_data.get("users_in", 1000)
            users_out = stage_data.get("users_out", users_in * 0.8)
            
            conversion_rate = users_out / users_in if users_in > 0 else 0
            
            # 分析流失原因
            drop_off_reasons = self._analyze_drop_off_reasons(step, conversion_rate)
            
            # generate优化建议
            suggestions = self._generate_funnel_suggestions(step, conversion_rate)
            
            analysis = FunnelAnalysis(
                stage_name=step.name,
                users_in=users_in,
                users_out=int(users_out),
                conversion_rate=conversion_rate,
                avg_time=stage_data.get("avg_time", 0),
                drop_off_reasons=drop_off_reasons,
                optimization_suggestions=suggestions
            )
            funnel_results.append(analysis)
        
        # 更新旅程数据
        journey.total_conversion_rate = funnel_results[-1].conversion_rate if funnel_results else 0
        
        logger.info(f"漏斗分析完成: {len(funnel_results)} 个阶段")
        return funnel_results
    
    def _analyze_drop_off_reasons(self, step: JourneyStep, conversion_rate: float) -> List[str]:
        """分析流失原因"""
        reasons = []
        
        if conversion_rate < 0.3:
            reasons.append("转化门槛过高")
        
        if step.stage == JourneyStage.ONBOARDING and conversion_rate < 0.5:
            reasons.append("激活流程复杂")
            reasons.append("价值传递不清晰")
        
        if step.stage == JourneyStage.CONVERSION and conversion_rate < 0.4:
            reasons.append("价格敏感")
            reasons.append("信任度不足")
        
        if not reasons:
            reasons.append("需要更多数据诊断")
        
        return reasons
    
    def _generate_funnel_suggestions(self, step: JourneyStep, conversion_rate: float) -> List[str]:
        """generate漏斗优化建议"""
        suggestions = []
        
        if conversion_rate < 0.3:
            suggestions.append(f"简化{step.name}流程,减少步骤")
            suggestions.append("增加进度指示器,降低用户焦虑")
        
        if step.stage == JourneyStage.ONBOARDING:
            suggestions.append("优化首次体验,快速展示价值")
            suggestions.append("增加互动引导,降低学习成本")
        
        if step.stage == JourneyStage.CONVERSION:
            suggestions.append("优化定价展示,增加信任背书")
            suggestions.append("简化支付流程,支持多种支付方式")
        
        if step.stage == JourneyStage.RETENTION:
            suggestions.append("建立用户健康度评分,主动干预")
            suggestions.append("个性化推荐,提升相关性")
        
        return suggestions
    
    def identify_friction_points(self, journey: UserJourney, funnel_data: List[FunnelAnalysis]) -> List[Dict]:
        """
        recognize摩擦点
        
        Args:
            journey: 用户旅程
            funnel_data: 漏斗分析数据
        
        Returns:
            摩擦点列表
        """
        friction_points = []
        
        for i, analysis in enumerate(funnel_data):
            if analysis.conversion_rate < 0.5:
                friction = {
                    "stage": analysis.stage_name,
                    "severity": "high" if analysis.conversion_rate < 0.3 else "medium",
                    "conversion_rate": f"{analysis.conversion_rate*100:.1f}%",
                    "drop_off_count": analysis.users_in - analysis.users_out,
                    "reasons": analysis.drop_off_reasons,
                    "suggestions": analysis.optimization_suggestions,
                    "priority": "immediate" if analysis.conversion_rate < 0.3 else "short_term"
                }
                friction_points.append(friction)
        
        # 更新旅程
        journey.friction_points = friction_points
        
        return friction_points
    
    def identify_wow_moments(self, journey: UserJourney) -> List[Dict]:
        """recognize惊喜时刻"""
        wow_moments = []
        
        # 基于旅程阶段recognize潜在的惊喜时刻
        wow_opportunities = {
            JourneyStage.ONBOARDING: {
                "moment": "首次价值体验",
                "description": "用户完成首次关键行为,感受到产品价值",
                "optimization": "缩短到Aha时刻的时间"
            },
            JourneyStage.ENGAGEMENT: {
                "moment": "超预期体验",
                "description": "产品功能超出用户预期",
                "optimization": "在关键节点提供额外价值"
            },
            JourneyStage.ADVOCACY: {
                "moment": "分享成就感",
                "description": "用户因使用产品获得成就,愿意分享",
                "optimization": "设计可分享的成就里程碑"
            }
        }
        
        for step in journey.steps:
            if step.stage in wow_opportunities:
                wow = wow_opportunities[step.stage]
                wow_moments.append({
                    "stage": step.name,
                    "moment": wow["moment"],
                    "description": wow["description"],
                    "optimization": wow["optimization"]
                })
        
        journey.wow_moments = wow_moments
        return wow_moments
    
    def generate_optimization_plan(self, journey: UserJourney) -> Dict:
        """generate优化计划"""
        plan = {
            "journey_id": journey.id,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_steps": len(journey.steps),
                "friction_points_count": len(journey.friction_points),
                "wow_moments_count": len(journey.wow_moments)
            },
            "immediate_actions": [],
            "short_term_actions": [],
            "long_term_actions": []
        }
        
        # 立即action:高优先级摩擦点
        for friction in journey.friction_points:
            if friction.get("priority") == "immediate":
                plan["immediate_actions"].append({
                    "target": friction["stage"],
                    "action": f"优化{friction['stage']}转化,当前转化率{friction['conversion_rate']}",
                    "expected_impact": "提升整体转化率20%+",
                    "suggestions": friction["suggestions"][:2]
                })
        
        # 短期action:中等优先级
        for friction in journey.friction_points:
            if friction.get("priority") == "short_term":
                plan["short_term_actions"].append({
                    "target": friction["stage"],
                    "action": f"改善{friction['stage']}体验",
                    "suggestions": friction["suggestions"][:2]
                })
        
        # 长期action:惊喜时刻优化
        for wow in journey.wow_moments:
            plan["long_term_actions"].append({
                "target": wow["stage"],
                "action": f"打造{wow['moment']}",
                "description": wow["optimization"]
            })
        
        return plan
    
    def export_journey(self, journey: UserJourney, format: str = "yaml") -> str:
        """导出用户旅程"""
        journey_data = {
            "id": journey.id,
            "name": journey.name,
            "persona": {
                "id": journey.persona_id,
                "name": journey.persona_name
            },
            "steps": [
                {
                    "id": step.id,
                    "stage": step.stage.value,
                    "name": step.name,
                    "user_goal": step.user_goal,
                    "user_emotion": step.user_emotion,
                    "touchpoints": [
                        {
                            "name": tp.name,
                            "type": tp.type.value,
                            "channel": tp.channel
                        }
                        for tp in step.touchpoints
                    ],
                    "key_actions": step.key_actions,
                    "drop_off_rate": step.drop_off_rate,
                    "success_criteria": step.success_criteria
                }
                for step in journey.steps
            ],
            "friction_points": journey.friction_points,
            "wow_moments": journey.wow_moments,
            "total_conversion_rate": journey.total_conversion_rate,
            "created_at": journey.created_at
        }
        
        if format == "yaml":
            return yaml.dump(journey_data, allow_unicode=True, default_flow_style=False)
        else:
            return json.dumps(journey_data, ensure_ascii=False, indent=2)
    
    def get_journey_stages(self) -> List[str]:
        """get用户旅程阶段列表"""
        return [stage.value for stage in JourneyStage]
