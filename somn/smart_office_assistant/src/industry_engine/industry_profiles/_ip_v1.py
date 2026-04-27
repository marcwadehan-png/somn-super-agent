"""
v1.0原有行业画像 (4个行业)
"""

from typing import Dict
from ._ip_types import IndustryType, IndustryProfile, BusinessModel

__all__ = [
    'init_ecommerce',
    'init_fintech',
    'init_saas_b2b',
    'init_saas_b2c',
    'init_v1_profiles',
]

def init_saas_b2b() -> IndustryProfile:
    """SaaS B2B行业"""
    return IndustryProfile(
        industry_type=IndustryType.SAAS_B2B,
        name="SaaS B2B",
        name_en="SaaS B2B",
        description="面向企业的软件即服务",
        sub_types=["CRM", "ERP", "HRM", "营销SaaS", "协同办公"],
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
        ],
        tags=["B2B", "订阅制", "企业服务", "高客单价"],
        special_attributes={"high_touch": True, "long_sales_cycle": True}
    )

def init_saas_b2c() -> IndustryProfile:
    """SaaS B2C行业"""
    return IndustryProfile(
        industry_type=IndustryType.SAAS_B2C,
        name="SaaS B2C",
        name_en="SaaS B2C",
        description="面向消费者的软件即服务",
        sub_types=["工具类", "效率类", "娱乐类", "健康类"],
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
        ],
        tags=["B2C", "免费增值", "消费级", "病毒传播"],
        special_attributes={"viral_potential": True, "low_price": True}
    )

def init_ecommerce() -> IndustryProfile:
    """电商行业"""
    return IndustryProfile(
        industry_type=IndustryType.ECOMMERCE,
        name="电商",
        name_en="E-commerce",
        description="在线零售和交易平台",
        sub_types=["synthesize电商", "垂直电商", "社交电商", "跨境电商"],
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
        ],
        tags=["交易", "零售", "平台", "复购"],
        special_attributes={"transaction_focused": True, "logistics_dependent": True}
    )

def init_fintech() -> IndustryProfile:
    """金融科技行业"""
    return IndustryProfile(
        industry_type=IndustryType.FINTECH,
        name="金融科技",
        name_en="Fintech",
        description="金融服务科技化",
        sub_types=["支付", "借贷", "理财", "保险科技"],
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
        ],
        tags=["金融", "监管", "信任", "安全"],
        special_attributes={"regulated": True, "trust_critical": True}
    )

def init_v1_profiles() -> Dict[IndustryType, IndustryProfile]:
    """初始化v1.0原有行业画像"""
    return {
        IndustryType.SAAS_B2B: init_saas_b2b(),
        IndustryType.SAAS_B2C: init_saas_b2c(),
        IndustryType.ECOMMERCE: init_ecommerce(),
        IndustryType.FINTECH: init_fintech(),
    }
