"""
__all__ = [
    'diagnose_business',
    'evaluate_strategy',
    'export_plan',
    'gap',
    'generate_growth_plan',
    'growth_rate_needed',
    'list_templates',
]

增长strategy引擎 - Growth Strategy Engine
基于超级智能体理念
实现完整的增长strategygenerate,评估与优化能力
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class GrowthPhase(Enum):
    """增长阶段"""
    SEED = "seed"           # 种子期:0-1 阶段
    STARTUP = "startup"     # 启动期:找到PMF
    GROWTH = "growth"       # 增长期:快速扩张
    EXPANSION = "expansion" # 扩张期:市场拓展
    MATURITY = "maturity"   # 成熟期:精细化运营

class GrowthLevers(Enum):
    """增长杠杆"""
    ACQUISITION = "acquisition"   # 获客
    ACTIVATION = "activation"     # 激活
    RETENTION = "retention"       # 留存
    REVENUE = "revenue"           # 变现
    REFERRAL = "referral"         # 推荐
    # AARRR 框架

class StrategyType(Enum):
    """strategy类型"""
    CONTENT = "content"           # 内容增长
    CHANNEL = "channel"           # 渠道增长
    PRODUCT = "product"           # 产品增长
    COMMUNITY = "community"       # 社区增长
    PARTNERSHIP = "partnership"   # 合作增长
    VIRAL = "viral"               # 病毒增长
    PAID = "paid"                 # 付费增长
    SEO = "seo"                   # SEO增长

@dataclass
class GrowthMetric:
    """增长metrics"""
    name: str
    current_value: float
    target_value: float
    unit: str
    timeframe: str  # e.g., "30天", "季度"
    priority: str = "high"  # high/medium/low
    
    @property
    def gap(self) -> float:
        return self.target_value - self.current_value
    
    @property
    def growth_rate_needed(self) -> float:
        if self.current_value == 0:
            return float('inf')
        return (self.target_value - self.current_value) / self.current_value * 100

@dataclass
class GrowthStrategy:
    """增长strategy"""
    id: str
    name: str
    strategy_type: StrategyType
    growth_lever: GrowthLevers
    description: str
    
    # 核心要素
    target_audience: str
    core_value_proposition: str
    key_actions: List[str]
    success_metrics: List[str]
    
    # 资源评估
    effort_level: str  # low/medium/high
    impact_level: str  # low/medium/high
    time_to_result: str  # e.g., "2周", "1个月", "3个月"
    cost_estimate: str  # low/medium/high
    
    # 优先级评分 (1-10)
    priority_score: float = 5.0
    confidence: float = 0.7
    
    # 执行计划
    phases: List[Dict] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class GrowthPlan:
    """增长计划"""
    id: str
    business_context: Dict
    growth_phase: GrowthPhase
    primary_goal: str
    time_horizon: str
    
    strategies: List[GrowthStrategy] = field(default_factory=list)
    metrics: List[GrowthMetric] = field(default_factory=list)
    
    # 执行路线图
    roadmap: List[Dict] = field(default_factory=list)
    
    # 资源分配
    resource_allocation: Dict = field(default_factory=dict)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

class GrowthStrategyEngine:
    """
    增长strategy引擎
    
    核心功能:
    1. 业务诊断与阶段recognize
    2. 增长机会发现
    3. strategy矩阵generate
    4. 优先级排序
    5. 执行计划制定
    6. 效果预测
    """
    
    def __init__(self):
        self.strategy_templates = self._init_strategy_templates()
        self.industry_benchmarks = self._init_industry_benchmarks()
        self.growth_formulas = self._init_growth_formulas()
        
    def _init_strategy_templates(self) -> Dict:
        """initstrategy模板库"""
        return {
            "saas_b2b": {
                "primary_levers": ["acquisition", "retention", "revenue"],
                "key_strategies": ["content_marketing", "sdr_outbound", "product_led_growth", "customer_success"],
                "key_metrics": ["MRR", "ARR", "Churn Rate", "LTV", "CAC", "NRR"],
                "benchmarks": {"churn_rate": "< 2%/月", "nrr": "> 110%", "ltv_cac": "> 3"}
            },
            "saas_b2c": {
                "primary_levers": ["acquisition", "activation", "retention"],
                "key_strategies": ["viral_loop", "content_seo", "referral_program", "push_notification"],
                "key_metrics": ["DAU", "MAU", "Retention D1/D7/D30", "ARPU"],
                "benchmarks": {"d1_retention": "> 40%", "d7_retention": "> 20%", "d30_retention": "> 10%"}
            },
            "ecommerce": {
                "primary_levers": ["acquisition", "revenue", "retention"],
                "key_strategies": ["paid_ads", "seo", "email_marketing", "loyalty_program"],
                "key_metrics": ["GMV", "Conversion Rate", "AOV", "Repeat Purchase Rate", "ROAS"],
                "benchmarks": {"conversion_rate": "2-4%", "roas": "> 3", "repeat_rate": "> 30%"}
            },
            "marketplace": {
                "primary_levers": ["acquisition", "activation", "referral"],
                "key_strategies": ["supply_growth", "demand_growth", "matching_optimization"],
                "key_metrics": ["GMV", "Take Rate", "Supply/Demand Balance", "Liquidity"],
                "benchmarks": {"take_rate": "10-30%"}
            },
            "content_media": {
                "primary_levers": ["acquisition", "retention", "referral"],
                "key_strategies": ["content_quality", "algorithm_recommendation", "community_building"],
                "key_metrics": ["DAU", "Time on Site", "Content Engagement Rate", "Share Rate"],
                "benchmarks": {"engagement_rate": "> 2%"}
            },
            "fintech": {
                "primary_levers": ["acquisition", "activation", "revenue"],
                "key_strategies": ["compliance_first", "trust_building", "referral_incentive"],
                "key_metrics": ["AUM", "Transaction Volume", "Activation Rate", "Fraud Rate"],
                "benchmarks": {"activation_rate": "> 60%"}
            }
        }
    
    def _init_industry_benchmarks(self) -> Dict:
        """init行业基准数据"""
        return {
            "user_acquisition": {
                "email_open_rate": {"excellent": "> 30%", "good": "20-30%", "average": "10-20%"},
                "landing_page_conversion": {"excellent": "> 5%", "good": "2-5%", "average": "1-2%"},
                "ctr_display_ads": {"excellent": "> 0.5%", "good": "0.2-0.5%", "average": "< 0.2%"}
            },
            "user_retention": {
                "d1_retention": {"excellent": "> 50%", "good": "40-50%", "average": "< 40%"},
                "monthly_churn": {"excellent": "< 2%", "good": "2-5%", "average": "> 5%"}
            },
            "monetization": {
                "freemium_conversion": {"excellent": "> 5%", "good": "2-5%", "average": "< 2%"},
                "trial_to_paid": {"excellent": "> 25%", "good": "15-25%", "average": "< 15%"}
            }
        }
    
    def _init_growth_formulas(self) -> Dict:
        """init增长公式"""
        return {
            "aarrr": {
                "formula": "Revenue = Acquisition × Activation × Retention × Referral × Revenue",
                "description": "海盗metrics框架,每个环节10%提升 = 整体61%提升",
                "levers": ["acquisition", "activation", "retention", "referral", "revenue"]
            },
            "north_star": {
                "formula": "North Star Metric = f(用户价值 × 使用频率 × 用户数量)",
                "description": "北极星metrics:反映核心用户价值交付的单一最重要metrics",
                "examples": {
                    "facebook": "DAU",
                    "airbnb": "预订夜晚数",
                    "slack": "活跃频道消息数",
                    "spotify": "听歌时长"
                }
            },
            "growth_accounting": {
                "formula": "净增用户 = 新增用户 + 复活用户 - 流失用户",
                "description": "增长会计:理解用户净增的三个来源"
            },
            "viral_coefficient": {
                "formula": "K = 邀请数 × 转化率",
                "description": "病毒系数 K > 1: 指数增长, K = 1: 线性增长, K < 1: 依赖外部获客",
                "target": "K > 0.5 即有显著病毒效应"
            },
            "ltv_cac": {
                "formula": "LTV/CAC = (ARPU × Gross Margin / Churn) / CAC",
                "description": "单位经济效益,LTV/CAC > 3 说明获客经济可持续",
                "target": "> 3"
            }
        }
    
    def diagnose_business(self, business_info: Dict) -> Dict:
        """
        业务诊断
        
        Args:
            business_info: {
                "industry": "saas_b2b",
                "stage": "growth",
                "monthly_revenue": 100000,
                "user_count": 5000,
                "growth_rate": 0.15,
                "main_challenges": ["高流失率", "获客成本高"],
                "current_metrics": {...}
            }
        
        Returns:
            诊断报告
        """
        industry = business_info.get("industry", "unknown")
        stage = business_info.get("stage", "growth")
        challenges = business_info.get("main_challenges", [])
        current_metrics = business_info.get("current_metrics", {})
        
        # recognize增长阶段
        growth_phase = self._identify_growth_phase(business_info)
        
        # 找出关键瓶颈
        bottlenecks = self._identify_bottlenecks(challenges, current_metrics, industry)
        
        # 增长机会矩阵
        opportunities = self._identify_opportunities(business_info, bottlenecks)
        
        # 行业对标
        benchmarks = self.industry_benchmarks
        template = self.strategy_templates.get(industry, self.strategy_templates.get("saas_b2b"))
        
        diagnosis = {
            "growth_phase": growth_phase.value,
            "bottlenecks": bottlenecks,
            "opportunities": opportunities,
            "recommended_focus": self._recommend_focus(growth_phase, bottlenecks),
            "industry_template": template,
            "key_growth_formulas": list(self.growth_formulas.keys()),
            "diagnosis_time": datetime.now().isoformat()
        }
        
        logger.info(f"业务诊断完成: 阶段={growth_phase.value}, 瓶颈数量={len(bottlenecks)}")
        return diagnosis
    
    def _identify_growth_phase(self, business_info: Dict) -> GrowthPhase:
        """recognize增长阶段"""
        revenue = business_info.get("monthly_revenue", 0)
        growth_rate = business_info.get("growth_rate", 0)
        user_count = business_info.get("user_count", 0)
        
        if revenue < 10000 or user_count < 100:
            return GrowthPhase.SEED
        elif revenue < 100000 or growth_rate < 0.1:
            return GrowthPhase.STARTUP
        elif growth_rate > 0.2:
            return GrowthPhase.GROWTH
        elif growth_rate > 0.1:
            return GrowthPhase.EXPANSION
        else:
            return GrowthPhase.MATURITY
    
    def _identify_bottlenecks(self, challenges: List[str], metrics: Dict, industry: str) -> List[Dict]:
        """recognize增长瓶颈"""
        bottlenecks = []
        
        # 基于挑战描述recognize
        challenge_mapping = {
            "流失": {"lever": "retention", "severity": "high"},
            "留存": {"lever": "retention", "severity": "high"},
            "获客": {"lever": "acquisition", "severity": "high"},
            "转化": {"lever": "activation", "severity": "medium"},
            "付费": {"lever": "revenue", "severity": "high"},
            "推荐": {"lever": "referral", "severity": "medium"},
            "品牌": {"lever": "acquisition", "severity": "medium"},
            "成本": {"lever": "revenue", "severity": "high"},
        }
        
        for challenge in challenges:
            for keyword, info in challenge_mapping.items():
                if keyword in challenge:
                    bottleneck = {
                        "area": info["lever"],
                        "description": challenge,
                        "severity": info["severity"],
                        "suggested_actions": self._get_quick_wins(info["lever"])
                    }
                    if not any(b["area"] == info["lever"] for b in bottlenecks):
                        bottlenecks.append(bottleneck)
        
        # 基于metricsrecognize
        if metrics:
            churn_rate = metrics.get("churn_rate", 0)
            if churn_rate > 0.05:
                bottlenecks.append({
                    "area": "retention",
                    "description": f"月流失率 {churn_rate*100:.1f}% 超过警戒线5%",
                    "severity": "critical",
                    "suggested_actions": ["用户访谈", "优化Onboarding", "建立流失预警"]
                })
            
            cac = metrics.get("cac", 0)
            ltv = metrics.get("ltv", 0)
            if cac > 0 and ltv > 0 and ltv / cac < 3:
                bottlenecks.append({
                    "area": "unit_economics",
                    "description": f"LTV/CAC = {ltv/cac:.1f},低于健康值3",
                    "severity": "high",
                    "suggested_actions": ["优化获客渠道", "提升LTV", "降低CAC"]
                })
        
        return bottlenecks
    
    def _identify_opportunities(self, business_info: Dict, bottlenecks: List[Dict]) -> List[Dict]:
        """发现增长机会"""
        opportunities = []
        industry = business_info.get("industry", "")
        growth_rate = business_info.get("growth_rate", 0)
        
        # 基于行业的机会
        industry_opportunities = {
            "saas_b2b": [
                {"name": "产品主导增长(PLG)", "potential": "high", "description": "通过产品体验驱动用户自主传播"},
                {"name": "内容营销SEO", "potential": "medium", "description": "建立思想领导力,降低获客成本"},
                {"name": "客户成功扩张", "potential": "high", "description": "通过NPS提升和用户成功实现净留存>100%"}
            ],
            "ecommerce": [
                {"name": "私域流量运营", "potential": "high", "description": "建立微信生态私域,降低复购成本"},
                {"name": "直播带货", "potential": "high", "description": "通过直播电商提升转化和客单价"},
                {"name": "会员体系", "potential": "medium", "description": "建立积分/等级体系提升复购率"}
            ]
        }
        
        industry_ops = industry_opportunities.get(industry, [
            {"name": "用户分层运营", "potential": "high", "description": "基于RFM分层,差异化运营strategy"},
            {"name": "渠道矩阵优化", "potential": "medium", "description": "多渠道测试,找到最优获客渠道组合"}
        ])
        
        opportunities.extend(industry_ops)
        
        # 基于瓶颈的机会
        for bottleneck in bottlenecks:
            if bottleneck["area"] == "retention":
                opportunities.append({
                    "name": "用户成功体系建设",
                    "potential": "high",
                    "description": "主动干预濒临流失用户,建立健康度评分"
                })
        
        # 低增长率时的机会
        if growth_rate < 0.1:
            opportunities.append({
                "name": "增长黑客实验",
                "potential": "high",
                "description": "通过快速A/B测试找到增长突破口,每周迭代"
            })
        
        return opportunities
    
    def _get_quick_wins(self, lever: str) -> List[str]:
        """get快速见效的action"""
        quick_wins = {
            "acquisition": ["优化落地页转化率", "开启内容营销", "启动推荐计划"],
            "activation": ["优化Onboarding流程", "减少注册摩擦", "设置引导教程"],
            "retention": ["设置流失预警", "优化邮件召回", "建立用户社区"],
            "revenue": ["优化定价结构", "增加付费节点", "优化付费引导"],
            "referral": ["设计裂变机制", "优化分享奖励", "建立口碑体系"]
        }
        return quick_wins.get(lever, ["深入分析数据", "用户访谈", "A/B测试"])
    
    def _recommend_focus(self, phase: GrowthPhase, bottlenecks: List[Dict]) -> List[str]:
        """推荐核心聚焦点"""
        phase_focus = {
            GrowthPhase.SEED: ["产品市场契合度验证", "核心用户留存"],
            GrowthPhase.STARTUP: ["可复制的获客渠道", "提升激活率"],
            GrowthPhase.GROWTH: ["规模化获客", "优化转化漏斗", "降低CAC"],
            GrowthPhase.EXPANSION: ["新市场拓展", "产品扩展", "平台化"],
            GrowthPhase.MATURITY: ["精细化运营", "提升LTV", "防守市场份额"]
        }
        
        focuses = phase_focus.get(phase, [])
        
        # 根据瓶颈补充
        critical_bottlenecks = [b for b in bottlenecks if b.get("severity") in ["critical", "high"]]
        for bottleneck in critical_bottlenecks[:2]:
            focus = f"解决{bottleneck['area']}瓶颈: {bottleneck['description'][:30]}..."
            focuses.append(focus)
        
        return focuses[:5]
    
    def generate_growth_plan(
        self, 
        business_info: Dict,
        diagnosis: Optional[Dict] = None,
        time_horizon: str = "3个月"
    ) -> GrowthPlan:
        """
        generate完整增长计划
        
        Args:
            business_info: 业务信息
            diagnosis: 业务诊断结果(可选,没有则自动诊断)
            time_horizon: 时间周期
        
        Returns:
            GrowthPlan
        """
        if not diagnosis:
            diagnosis = self.diagnose_business(business_info)
        
        # generate计划ID
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 确定增长阶段
        growth_phase = GrowthPhase(diagnosis.get("growth_phase", "growth"))
        
        # generatestrategy组合
        strategies = self._generate_strategies(business_info, diagnosis)
        
        # 设置关键metrics
        metrics = self._define_metrics(business_info, growth_phase)
        
        # generate路线图
        roadmap = self._build_roadmap(strategies, time_horizon)
        
        # 资源分配建议
        resource_allocation = self._allocate_resources(strategies)
        
        plan = GrowthPlan(
            id=plan_id,
            business_context=business_info,
            growth_phase=growth_phase,
            primary_goal=business_info.get("primary_goal", "提升增长速率"),
            time_horizon=time_horizon,
            strategies=strategies,
            metrics=metrics,
            roadmap=roadmap,
            resource_allocation=resource_allocation
        )
        
        logger.info(f"增长计划generate完成: {plan_id}, strategy数={len(strategies)}")
        return plan
    
    def _generate_strategies(self, business_info: Dict, diagnosis: Dict) -> List[GrowthStrategy]:
        """generatestrategy组合"""
        strategies = []
        industry = business_info.get("industry", "saas_b2b")
        bottlenecks = diagnosis.get("bottlenecks", [])
        opportunities = diagnosis.get("opportunities", [])
        
        # 基于瓶颈generate应对strategy
        strategy_counter = 0
        for bottleneck in bottlenecks[:3]:
            lever = bottleneck.get("area", "acquisition")
            strategy_counter += 1
            
            strategy = GrowthStrategy(
                id=f"strategy_{strategy_counter:03d}",
                name=f"{lever}优化strategy",
                strategy_type=StrategyType.PRODUCT,
                growth_lever=GrowthLevers(lever) if lever in [e.value for e in GrowthLevers] else GrowthLevers.ACQUISITION,
                description=f"针对{bottleneck['description']}的专项优化",
                target_audience=business_info.get("target_audience", "核心用户"),
                core_value_proposition=f"解决{lever}瓶颈,提升整体增长效率",
                key_actions=bottleneck.get("suggested_actions", []),
                success_metrics=self._get_lever_metrics(lever),
                effort_level="medium",
                impact_level="high",
                time_to_result="4-6周",
                cost_estimate="medium",
                priority_score=8.0 if bottleneck.get("severity") == "critical" else 6.0,
                confidence=0.75,
                risks=["执行不到位", "资源不足"]
            )
            strategies.append(strategy)
        
        # 基于机会generate增长strategy
        for opportunity in opportunities[:3]:
            strategy_counter += 1
            
            strategy = GrowthStrategy(
                id=f"strategy_{strategy_counter:03d}",
                name=opportunity.get("name", "增长机会strategy"),
                strategy_type=StrategyType.CHANNEL,
                growth_lever=GrowthLevers.ACQUISITION,
                description=opportunity.get("description", ""),
                target_audience=business_info.get("target_audience", "潜在用户"),
                core_value_proposition=opportunity.get("description", ""),
                key_actions=self._get_strategy_actions(opportunity.get("name", "")),
                success_metrics=["转化率", "获客成本", "新增用户数"],
                effort_level="medium",
                impact_level=opportunity.get("potential", "medium"),
                time_to_result="1-3个月",
                cost_estimate="medium",
                priority_score=7.0 if opportunity.get("potential") == "high" else 5.0,
                confidence=0.65,
            )
            strategies.append(strategy)
        
        # 按优先级排序
        strategies.sort(key=lambda s: s.priority_score, reverse=True)
        
        return strategies[:6]  # 最多6个核心strategy
    
    def _get_lever_metrics(self, lever: str) -> List[str]:
        """get杠杆对应的关键metrics"""
        lever_metrics = {
            "acquisition": ["新增用户数", "CAC", "渠道ROI", "流量转化率"],
            "activation": ["激活率", "首次关键行为完成率", "Onboarding完成率"],
            "retention": ["次日留存", "月留存", "流失率", "复购率"],
            "revenue": ["ARPU", "付费转化率", "LTV", "GMV"],
            "referral": ["病毒系数K值", "分享率", "邀请转化率"],
            "unit_economics": ["LTV/CAC", "毛利率", "回收周期"]
        }
        return lever_metrics.get(lever, ["DAU", "MAU", "收入"])
    
    def _get_strategy_actions(self, strategy_name: str) -> List[str]:
        """根据strategy名get执action作"""
        action_templates = {
            "产品主导增长": ["设计产品内病毒传播点", "优化免费到付费转化路径", "建立产品使用数据分析"],
            "内容营销SEO": ["关键词研究与内容规划", "产出高质量行业内容", "建立外链strategy"],
            "私域流量运营": ["搭建微信生态矩阵", "设计私域用户旅程", "建立分层运营SOP"],
            "直播带货": ["选品strategy制定", "主播培训与内容规划", "直播数据监控优化"],
            "用户成功体系建设": ["定义用户健康度评分", "建立流失预警模型", "制定主动干预SOP"],
            "增长黑客实验": ["建立实验假设清单", "设计A/B测试框架", "定义成功metrics与停止条件"]
        }
        
        # 模糊匹配
        for key, actions in action_templates.items():
            if any(keyword in strategy_name for keyword in key.split()):
                return actions
        
        return ["深入分析现状", "制定具体方案", "小规模测试", "规模化推广"]
    
    def _define_metrics(self, business_info: Dict, phase: GrowthPhase) -> List[GrowthMetric]:
        """定义关键metrics"""
        metrics = []
        current_metrics = business_info.get("current_metrics", {})
        
        # 北极星metrics
        north_star_examples = {
            GrowthPhase.SEED: ("早期用户使用天数", 0.3, 0.7, "比例"),
            GrowthPhase.STARTUP: ("月活跃用户", 1000, 5000, "人"),
            GrowthPhase.GROWTH: ("月营收增长率", 0.15, 0.25, "比例"),
            GrowthPhase.EXPANSION: ("市场占有率", 0.05, 0.1, "比例"),
            GrowthPhase.MATURITY: ("净收入留存率NRR", 1.0, 1.2, "比例")
        }
        
        ns_name, ns_current, ns_target, ns_unit = north_star_examples.get(
            phase, ("月活用户", 1000, 5000, "人")
        )
        
        metrics.append(GrowthMetric(
            name=ns_name,
            current_value=current_metrics.get("north_star", ns_current),
            target_value=ns_target,
            unit=ns_unit,
            timeframe="3个月",
            priority="high"
        ))
        
        # AARRR metrics
        aarrr_metrics = [
            ("新增用户(get)", "acquisition", 100, 300, "人/月"),
            ("激活率(激活)", "activation_rate", 0.4, 0.6, "比例"),
            ("月留存率(留存)", "retention_rate", 0.7, 0.85, "比例"),
            ("ARPU(变现)", "arpu", 50, 100, "元"),
        ]
        
        for name, key, default_current, default_target, unit in aarrr_metrics:
            metrics.append(GrowthMetric(
                name=name,
                current_value=current_metrics.get(key, default_current),
                target_value=default_target,
                unit=unit,
                timeframe="3个月",
                priority="medium"
            ))
        
        return metrics
    
    def _build_roadmap(self, strategies: List[GrowthStrategy], time_horizon: str) -> List[Dict]:
        """构建执行路线图"""
        # 解析时间周期
        weeks = 12  # 默认3个月
        if "个月" in time_horizon:
            months = int(time_horizon.replace("个月", ""))
            weeks = months * 4
        elif "周" in time_horizon:
            weeks = int(time_horizon.replace("周", ""))
        
        roadmap = []
        
        # 第一阶段: 诊断与快速验证 (1-2周)
        roadmap.append({
            "phase": 1,
            "name": "诊断与快速验证",
            "duration": "第1-2周",
            "objectives": ["完成数据埋点", "设定基线metrics", "启动关键实验"],
            "strategies": [s.id for s in strategies[:2] if s.priority_score >= 7],
            "deliverables": ["现状诊断报告", "实验设计文档", "数据看板"]
        })
        
        # 第二阶段: 核心优化 (3-6周)
        roadmap.append({
            "phase": 2,
            "name": "核心优化执行",
            "duration": f"第3-{min(6, weeks//2)}周",
            "objectives": ["执行Top3核心strategy", "持续数据监控", "快速迭代优化"],
            "strategies": [s.id for s in strategies[:4]],
            "deliverables": ["周度进展报告", "A/B测试结果", "优化decision日志"]
        })
        
        # 第三阶段: 规模化 (后半段)
        if weeks > 8:
            roadmap.append({
                "phase": 3,
                "name": "规模化推广",
                "duration": f"第{weeks//2+1}-{weeks}周",
                "objectives": ["规模化成功strategy", "建立增长飞轮", "系统化SOP"],
                "strategies": [s.id for s in strategies],
                "deliverables": ["增长SOP手册", "季度复盘报告", "下季度计划"]
            })
        
        return roadmap
    
    def _allocate_resources(self, strategies: List[GrowthStrategy]) -> Dict:
        """资源分配建议"""
        # 计算各杠杆权重
        lever_weights = {}
        for strategy in strategies:
            lever = strategy.growth_lever.value
            weight = strategy.priority_score
            lever_weights[lever] = lever_weights.get(lever, 0) + weight
        
        total_weight = sum(lever_weights.values()) or 1
        
        # 转换为百分比
        allocation = {}
        for lever, weight in lever_weights.items():
            allocation[lever] = round(weight / total_weight * 100, 1)
        
        return {
            "budget_allocation": allocation,
            "headcount_priority": [s.growth_lever.value for s in strategies[:3]],
            "recommendation": f"建议优先投入前3个核心strategy,占总资源的70%"
        }
    
    def evaluate_strategy(self, strategy: GrowthStrategy, results: Dict) -> Dict:
        """
        评估strategy执行效果
        
        Args:
            strategy: strategy对象
            results: 实际执行结果
        
        Returns:
            评估报告
        """
        evaluation = {
            "strategy_id": strategy.id,
            "strategy_name": strategy.name,
            "evaluation_time": datetime.now().isoformat(),
            "metrics_comparison": [],
            "overall_score": 0,
            "recommendations": []
        }
        
        # metrics对比
        for metric in strategy.success_metrics:
            target = results.get(f"{metric}_target", 0)
            actual = results.get(metric, 0)
            
            if target > 0:
                achievement_rate = actual / target
                evaluation["metrics_comparison"].append({
                    "metric": metric,
                    "target": target,
                    "actual": actual,
                    "achievement_rate": f"{achievement_rate*100:.1f}%",
                    "status": "达标" if achievement_rate >= 0.9 else "待改善"
                })
        
        # synthesize评分
        if evaluation["metrics_comparison"]:
            achieved = sum(
                1 for m in evaluation["metrics_comparison"] 
                if m["status"] == "达标"
            )
            evaluation["overall_score"] = achieved / len(evaluation["metrics_comparison"]) * 10
        
        # 建议
        if evaluation["overall_score"] >= 8:
            evaluation["recommendations"].append("strategy效果显著,建议规模化推广")
        elif evaluation["overall_score"] >= 5:
            evaluation["recommendations"].append("strategy有效但有提升空间,建议优化关键环节")
        else:
            evaluation["recommendations"].append("strategy效果不达预期,建议深入分析原因,考虑调整方向")
        
        return evaluation
    
    def export_plan(self, plan: GrowthPlan, format: str = "yaml") -> str:
        """导出增长计划"""
        plan_data = {
            "id": plan.id,
            "business_context": plan.business_context,
            "growth_phase": plan.growth_phase.value,
            "primary_goal": plan.primary_goal,
            "time_horizon": plan.time_horizon,
            "strategies": [
                {
                    "id": s.id,
                    "name": s.name,
                    "type": s.strategy_type.value,
                    "lever": s.growth_lever.value,
                    "description": s.description,
                    "key_actions": s.key_actions,
                    "success_metrics": s.success_metrics,
                    "priority_score": s.priority_score,
                    "effort": s.effort_level,
                    "impact": s.impact_level,
                    "time_to_result": s.time_to_result
                }
                for s in plan.strategies
            ],
            "metrics": [
                {
                    "name": m.name,
                    "current": m.current_value,
                    "target": m.target_value,
                    "unit": m.unit,
                    "timeframe": m.timeframe,
                    "gap": m.gap,
                    "growth_rate_needed": f"{m.growth_rate_needed:.1f}%"
                }
                for m in plan.metrics
            ],
            "roadmap": plan.roadmap,
            "resource_allocation": plan.resource_allocation,
            "created_at": plan.created_at
        }
        
        if format == "yaml":
            return yaml.dump(plan_data, allow_unicode=True, default_flow_style=False)
        else:
            return json.dumps(plan_data, ensure_ascii=False, indent=2)
    
    def list_templates(self) -> List[str]:
        """列出所有strategy模板"""
        return list(self.strategy_templates.keys())
