"""
__all__ = [
    'adapt_strategy',
    'compare_industries',
    'export_profile',
    'generate_industry_recommendations',
    'get_adapter',
    'get_applicable_rules',
    'get_industry_profile',
    'identify_scenario',
]

行业适配引擎 - Industry Adapter
实现行业差异化strategy和场景适配
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class IndustryType(Enum):
    """行业类型"""
    SAAS_B2B = "saas_b2b"
    SAAS_B2C = "saas_b2c"
    ECOMMERCE = "ecommerce"
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    MARKETPLACE = "marketplace"
    CONTENT_MEDIA = "content_media"
    GAMING = "gaming"

class BusinessModel(Enum):
    """商业模式"""
    SUBSCRIPTION = "subscription"       # 订阅制
    TRANSACTION = "transaction"         # 交易抽成
    ADVERTISING = "advertising"         # 广告
    FREEMIUM = "freemium"               # 免费增值
    ENTERPRISE = "enterprise"           # 企业销售

@dataclass
class IndustryProfile:
    """行业画像"""
    industry_type: IndustryType
    name: str
    description: str
    
    # 商业模式
    business_models: List[BusinessModel] = field(default_factory=list)
    
    # 关键characteristics
    key_characteristics: List[str] = field(default_factory=list)
    
    # 增长驱动因素
    growth_drivers: List[str] = field(default_factory=list)
    
    # 关键metrics
    key_metrics: List[str] = field(default_factory=list)
    
    # 行业基准
    benchmarks: Dict = field(default_factory=dict)
    
    # 典型挑战
    typical_challenges: List[str] = field(default_factory=list)
    
    # 最佳实践
    best_practices: List[str] = field(default_factory=list)

@dataclass
class AdaptationRule:
    """适配规则"""
    id: str
    industry: IndustryType
    context: str  # 适用场景
    
    # 规则内容
    condition: str  # 触发条件
    action: str  # 执action作
    
    # 优先级和权重
    priority: int = 5  # 1-10
    weight: float = 1.0
    
    # 元数据
    description: str = ""
    examples: List[str] = field(default_factory=list)

class IndustryAdapter:
    """
    行业适配引擎
    
    核心功能:
    1. 行业画像管理 - 维护各行业characteristics和基准
    2. strategy适配 - 根据行业调整strategy
    3. 规则引擎 - 行业特定规则执行
    4. 场景recognize - recognize当前业务场景
    5. 差异化建议 - generate行业专属建议
    """
    
    def __init__(self):
        self.industry_profiles = self._init_industry_profiles()
        self.adaptation_rules = self._init_adaptation_rules()
        
    def _init_industry_profiles(self) -> Dict[IndustryType, IndustryProfile]:
        """init行业画像"""
        profiles = {}
        
        # SaaS B2B
        profiles[IndustryType.SAAS_B2B] = IndustryProfile(
            industry_type=IndustryType.SAAS_B2B,
            name="SaaS B2B",
            description="面向企业的软件即服务",
            business_models=[BusinessModel.SUBSCRIPTION, BusinessModel.ENTERPRISE],
            key_characteristics=[
                "长销售周期",
                "高客单价",
                "多decision者",
                "强服务属性",
                "网络效应有限"
            ],
            growth_drivers=[
                "产品主导增长(PLG)",
                "销售驱动",
                "客户成功扩张",
                "生态合作"
            ],
            key_metrics=[
                "MRR/ARR",
                "CAC",
                "LTV",
                "NRR",
                "Logo Churn",
                "Revenue Churn"
            ],
            benchmarks={
                "ltv_cac_ratio": "> 3",
                "cac_payback": "< 12个月",
                "gross_margin": "> 70%",
                "nrr": "> 110%",
                "monthly_churn": "< 2%"
            },
            typical_challenges=[
                "获客成本高",
                "销售周期长",
                "客户成功难度大",
                "产品复杂度高"
            ],
            best_practices=[
                "建立产品主导增长(PLG)体系",
                "投资内容营销建立思想领导力",
                "构建客户成功团队",
                "设计灵活的定价strategy"
            ]
        )
        
        # SaaS B2C
        profiles[IndustryType.SAAS_B2C] = IndustryProfile(
            industry_type=IndustryType.SAAS_B2C,
            name="SaaS B2C",
            description="面向消费者的软件即服务",
            business_models=[BusinessModel.FREEMIUM, BusinessModel.SUBSCRIPTION],
            key_characteristics=[
                "低客单价",
                "高用户量",
                "短decision周期",
                "强产品体验",
                "病毒传播潜力"
            ],
            growth_drivers=[
                "病毒式增长",
                "内容营销",
                "应用商店优化",
                "付费获客"
            ],
            key_metrics=[
                "MAU/DAU",
                "留存率",
                "付费转化率",
                "ARPU",
                "病毒系数K"
            ],
            benchmarks={
                "d1_retention": "> 40%",
                "d7_retention": "> 20%",
                "d30_retention": "> 10%",
                "freemium_conversion": "2-5%",
                "monthly_churn": "< 5%"
            },
            typical_challenges=[
                "留存难度大",
                "获客成本高",
                "付费转化低",
                "用户注意力分散"
            ],
            best_practices=[
                "设计病毒传播机制",
                "优化首次体验",
                "建立推送strategy",
                "A/B测试驱动优化"
            ]
        )
        
        # 电商
        profiles[IndustryType.ECOMMERCE] = IndustryProfile(
            industry_type=IndustryType.ECOMMERCE,
            name="电商",
            description="在线零售和交易平台",
            business_models=[BusinessModel.TRANSACTION, BusinessModel.ADVERTISING],
            key_characteristics=[
                "交易导向",
                "价格敏感",
                "物流依赖",
                "库存管理",
                "复购重要"
            ],
            growth_drivers=[
                "流量get",
                "转化率优化",
                "客单价提升",
                "复购率提升"
            ],
            key_metrics=[
                "GMV",
                "转化率",
                "AOV",
                "复购率",
                "CAC",
                "ROAS"
            ],
            benchmarks={
                "conversion_rate": "2-4%",
                "cart_abandonment": "< 70%",
                "aov_growth": "> 5%/月",
                "repeat_purchase": "> 30%",
                "roas": "> 3"
            },
            typical_challenges=[
                "获客成本高",
                "价格竞争激烈",
                "物流成本上升",
                "用户忠诚度低"
            ],
            best_practices=[
                "优化购物流程",
                "建立会员体系",
                "个性化推荐",
                "多渠道整合"
            ]
        )
        
        # 金融科技
        profiles[IndustryType.FINTECH] = IndustryProfile(
            industry_type=IndustryType.FINTECH,
            name="金融科技",
            description="金融服务科技化",
            business_models=[BusinessModel.TRANSACTION, BusinessModel.SUBSCRIPTION],
            key_characteristics=[
                "强监管",
                "高信任要求",
                "安全敏感",
                "数据驱动",
                "合规优先"
            ],
            growth_drivers=[
                "产品创新",
                "用户体验",
                "信任建立",
                "生态合作"
            ],
            key_metrics=[
                "AUM",
                "交易量",
                "用户资产",
                "风控metrics",
                "合规评分"
            ],
            benchmarks={
                "activation_rate": "> 60%",
                "fraud_rate": "< 0.1%",
                "csat": "> 4.0",
                "kyc_completion": "> 80%"
            },
            typical_challenges=[
                "监管合规",
                "用户信任建立",
                "风控管理",
                "数据安全"
            ],
            best_practices=[
                "合规优先设计",
                "透明化沟通",
                "渐进式信任建立",
                "强风控体系"
            ]
        )
        
        return profiles
    
    def _init_adaptation_rules(self) -> List[AdaptationRule]:
        """init适配规则"""
        rules = []
        
        # SaaS B2B 规则
        rules.extend([
            AdaptationRule(
                id="saas_b2b_001",
                industry=IndustryType.SAAS_B2B,
                context="获客strategy",
                condition="销售周期 > 3个月",
                action="采用ABM(基于账户的营销)strategy,聚焦高价值目标客户",
                priority=9,
                description="长销售周期下需要精准营销"
            ),
            AdaptationRule(
                id="saas_b2b_002",
                industry=IndustryType.SAAS_B2B,
                context="定价strategy",
                condition="客单价 > 1万元/年",
                action="采用价值定价,提供定制化方案",
                priority=8,
                description="高客单价需要价值证明"
            ),
            AdaptationRule(
                id="saas_b2b_003",
                industry=IndustryType.SAAS_B2B,
                context="留存strategy",
                condition="NRR < 100%",
                action="建立客户成功团队,主动干预健康度下降客户",
                priority=10,
                description="负净留存是严重警告信号"
            )
        ])
        
        # SaaS B2C 规则
        rules.extend([
            AdaptationRule(
                id="saas_b2c_001",
                industry=IndustryType.SAAS_B2C,
                context="增长strategy",
                condition="病毒系数K < 0.3",
                action="设计产品内病毒传播点,优化分享体验",
                priority=9,
                description="低病毒系数需要主动优化"
            ),
            AdaptationRule(
                id="saas_b2c_002",
                industry=IndustryType.SAAS_B2C,
                context="留存strategy",
                condition="D7留存 < 20%",
                action="优化Onboarding,快速展示核心价值",
                priority=10,
                description="早期留存是产品健康的关键metrics"
            )
        ])
        
        # 电商规则
        rules.extend([
            AdaptationRule(
                id="ecom_001",
                industry=IndustryType.ECOMMERCE,
                context="转化优化",
                condition="购物车放弃率 > 70%",
                action="优化结算流程,增加信任背书,提供多种支付方式",
                priority=9,
                description="高放弃率是电商核心问题"
            ),
            AdaptationRule(
                id="ecom_002",
                industry=IndustryType.ECOMMERCE,
                context="复购strategy",
                condition="复购率 < 20%",
                action="建立会员体系,个性化推荐,定期促销活动",
                priority=8,
                description="低复购需要建立长期关系"
            )
        ])
        
        # 金融科技规则
        rules.extend([
            AdaptationRule(
                id="fintech_001",
                industry=IndustryType.FINTECH,
                context="获客strategy",
                condition="KYC完成率 < 60%",
                action="简化KYC流程,渐进式信息收集,提供清晰指引",
                priority=10,
                description="KYC是金融科技的关键转化点"
            ),
            AdaptationRule(
                id="fintech_002",
                industry=IndustryType.FINTECH,
                context="信任建立",
                condition="新用户注册7天内未交易",
                action="发送教育内容,提供小额体验机会,展示安全保障",
                priority=8,
                description="信任建立是金融科技的核心挑战"
            )
        ])
        
        return rules
    
    def get_industry_profile(self, industry: IndustryType) -> Optional[IndustryProfile]:
        """get行业画像"""
        return self.industry_profiles.get(industry)
    
    def get_applicable_rules(
        self,
        industry: IndustryType,
        context: Optional[str] = None
    ) -> List[AdaptationRule]:
        """get适用的适配规则"""
        rules = [r for r in self.adaptation_rules if r.industry == industry]
        
        if context:
            rules = [r for r in rules if r.context == context]
        
        # 按优先级排序
        rules.sort(key=lambda r: r.priority, reverse=True)
        
        return rules
    
    def adapt_strategy(
        self,
        strategy: Dict,
        industry: IndustryType,
        business_context: Dict
    ) -> Dict:
        """
        适配strategy到特定行业
        
        Args:
            strategy: 原始strategy
            industry: 目标行业
            business_context: 业务上下文
        
        Returns:
            适配后的strategy
        """
        profile = self.get_industry_profile(industry)
        if not profile:
            logger.warning(f"未找到行业画像: {industry}")
            return strategy
        
        adapted = strategy.copy()
        
        # 应用行业特定调整
        adaptations = []
        
        # 1. 调整strategy重点
        if industry == IndustryType.SAAS_B2B:
            adaptations.append({
                "type": "emphasis_shift",
                "description": "强化销售支持和客户成功",
                "changes": ["增加销售赋能内容", "建立客户成功里程碑"]
            })
        elif industry == IndustryType.SAAS_B2C:
            adaptations.append({
                "type": "emphasis_shift",
                "description": "强化产品体验和病毒传播",
                "changes": ["优化首次体验", "设计分享激励"]
            })
        elif industry == IndustryType.ECOMMERCE:
            adaptations.append({
                "type": "emphasis_shift",
                "description": "强化转化和复购",
                "changes": ["优化购物流程", "建立会员体系"]
            })
        
        # 2. 调整metrics
        adapted["key_metrics"] = profile.key_metrics[:5]
        
        # 3. 调整时间预期
        if industry == IndustryType.SAAS_B2B:
            adapted["time_to_result"] = "3-6个月"
        elif industry == IndustryType.SAAS_B2C:
            adapted["time_to_result"] = "4-8周"
        
        # 4. 应用适配规则
        applicable_rules = self.get_applicable_rules(industry)
        for rule in applicable_rules[:3]:
            adaptations.append({
                "type": "rule_application",
                "rule_id": rule.id,
                "description": rule.description,
                "action": rule.action
            })
        
        adapted["industry_adaptations"] = adaptations
        adapted["target_industry"] = industry.value
        adapted["industry_benchmarks"] = profile.benchmarks
        
        return adapted
    
    def identify_scenario(
        self,
        industry: IndustryType,
        metrics: Dict,
        context: Dict
    ) -> Dict:
        """
        recognize业务场景
        
        Args:
            industry: 行业类型
            metrics: 当前metrics
            context: 业务上下文
        
        Returns:
            场景recognize结果
        """
        profile = self.get_industry_profile(industry)
        
        scenarios = []
        
        # 基于metricsrecognize场景
        if industry == IndustryType.SAAS_B2B:
            if metrics.get("cac_payback_months", 0) > 18:
                scenarios.append({
                    "name": "获客成本危机",
                    "severity": "high",
                    "description": "获客成本回收周期过长,需要优化获客渠道或提升客单价"
                })
            
            if metrics.get("nrr", 100) < 100:
                scenarios.append({
                    "name": "负净留存",
                    "severity": "critical",
                    "description": "客户流失超过扩张,业务不可持续"
                })
        
        elif industry == IndustryType.SAAS_B2C:
            if metrics.get("d7_retention", 0) < 0.15:
                scenarios.append({
                    "name": "早期留存危机",
                    "severity": "high",
                    "description": "用户快速流失,产品价值传递不清晰"
                })
            
            if metrics.get("viral_coefficient", 0) < 0.2:
                scenarios.append({
                    "name": "增长依赖付费",
                    "severity": "medium",
                    "description": "缺乏有机增长,获客成本高"
                })
        
        elif industry == IndustryType.ECOMMERCE:
            if metrics.get("conversion_rate", 0) < 0.01:
                scenarios.append({
                    "name": "转化率极低",
                    "severity": "high",
                    "description": "流量无法转化为销售,需优化购物体验"
                })
            
            if metrics.get("repeat_purchase_rate", 0) < 0.15:
                scenarios.append({
                    "name": "复购率低",
                    "severity": "medium",
                    "description": "用户一次性购买,缺乏长期价值"
                })
        
        # 基于上下文recognize场景
        stage = context.get("growth_stage", "")
        if stage == "early":
            scenarios.append({
                "name": "早期增长",
                "severity": "low",
                "description": "处于早期阶段,重点是找到PMF"
            })
        elif stage == "scaling":
            scenarios.append({
                "name": "规模化挑战",
                "severity": "medium",
                "description": "快速增长中,需要建立可复制的增长体系"
            })
        
        return {
            "industry": industry.value,
            "identified_scenarios": scenarios,
            "primary_scenario": scenarios[0] if scenarios else None,
            "recommended_focus": self._recommend_focus(scenarios, industry)
        }
    
    def _recommend_focus(self, scenarios: List[Dict], industry: IndustryType) -> List[str]:
        """推荐关注重点"""
        if not scenarios:
            return ["持续监控核心metrics", "优化用户体验"]
        
        focuses = []
        
        # 优先处理高严重度场景
        critical = [s for s in scenarios if s.get("severity") == "critical"]
        high = [s for s in scenarios if s.get("severity") == "high"]
        
        for s in critical:
            focuses.append(f"[紧急]{s['name']}: {s['description'][:30]}...")
        
        for s in high[:2]:
            focuses.append(f"[重要]{s['name']}: {s['description'][:30]}...")
        
        # 行业特定建议
        profile = self.get_industry_profile(industry)
        if profile and profile.growth_drivers:
            focuses.append(f"[长期]关注核心增长驱动: {profile.growth_drivers[0]}")
        
        return focuses[:5]
    
    def generate_industry_recommendations(
        self,
        industry: IndustryType,
        business_context: Dict
    ) -> List[Dict]:
        """generate行业专属建议"""
        profile = self.get_industry_profile(industry)
        if not profile:
            return []
        
        recommendations = []
        
        # 1. 基准对比建议
        metrics = business_context.get("metrics", {})
        for metric_name, benchmark in profile.benchmarks.items():
            current_value = metrics.get(metric_name)
            if current_value is not None:
                recommendations.append({
                    "type": "benchmark",
                    "metric": metric_name,
                    "current": current_value,
                    "benchmark": benchmark,
                    "recommendation": f"优化{metric_name}至行业基准水平"
                })
        
        # 2. 最佳实践建议
        for practice in profile.best_practices[:3]:
            recommendations.append({
                "type": "best_practice",
                "description": practice,
                "priority": "high"
            })
        
        # 3. 适用规则建议
        rules = self.get_applicable_rules(industry)
        for rule in rules[:3]:
            recommendations.append({
                "type": "adaptation_rule",
                "rule_id": rule.id,
                "context": rule.context,
                "action": rule.action,
                "priority": rule.priority
            })
        
        return recommendations
    
    def compare_industries(
        self,
        industries: List[IndustryType]
    ) -> Dict:
        """对比多个行业"""
        comparison = {
            "industries": [],
            "similarities": [],
            "differences": []
        }
        
        profiles = [self.get_industry_profile(i) for i in industries]
        profiles = [p for p in profiles if p]
        
        for profile in profiles:
            comparison["industries"].append({
                "type": profile.industry_type.value,
                "name": profile.name,
                "key_metrics": profile.key_metrics[:3],
                "growth_drivers": profile.growth_drivers[:2]
            })
        
        # 找出相似性
        all_drivers = set()
        for p in profiles:
            all_drivers.update(p.growth_drivers)
        
        for driver in all_drivers:
            count = sum(1 for p in profiles if driver in p.growth_drivers)
            if count > 1:
                comparison["similarities"].append({
                    "aspect": "增长驱动",
                    "item": driver,
                    "shared_by": count
                })
        
        return comparison
    
    def export_profile(self, industry: IndustryType, format: str = "yaml") -> str:
        """导出行业画像"""
        profile = self.get_industry_profile(industry)
        if not profile:
            return ""
        
        data = {
            "industry": profile.industry_type.value,
            "name": profile.name,
            "description": profile.description,
            "business_models": [bm.value for bm in profile.business_models],
            "key_characteristics": profile.key_characteristics,
            "growth_drivers": profile.growth_drivers,
            "key_metrics": profile.key_metrics,
            "benchmarks": profile.benchmarks,
            "typical_challenges": profile.typical_challenges,
            "best_practices": profile.best_practices
        }
        
        if format == "yaml":
            return yaml.dump(data, allow_unicode=True, default_flow_style=False)
        else:
            return json.dumps(data, ensure_ascii=False, indent=2)
    
    def get_adapter(self, industry_str: str):
        """get行业适配器(简化版,返回行业配置)"""
        try:
            industry = IndustryType(industry_str)
            return self.get_industry_profile(industry)
        except ValueError:
            return None
