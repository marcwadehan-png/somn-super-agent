"""
__all__ = [
    'init_education',
    'init_food_beverage',
    'init_healthcare',
    'init_month1_profiles',
    'init_real_estate',
    'init_travel',
]

Month 1 新增行业画像 (5个行业)
"""

from typing import Dict
from ._ip_types import IndustryType, IndustryProfile, BusinessModel

def init_healthcare() -> IndustryProfile:
    """医疗健康行业"""
    return IndustryProfile(
        industry_type=IndustryType.HEALTHCARE,
        name="医疗健康",
        name_en="Healthcare",
        description="医疗健康服务与产品",
        sub_types=["互联网医疗", "医药电商", "健康管理", "医疗器械"],
        business_models=[BusinessModel.TRANSACTION, BusinessModel.SUBSCRIPTION, BusinessModel.COMMISSION],
        key_characteristics=[
            "强监管合规",
            "专业门槛高",
            "用户信任关键",
            "decision周期长",
            "效果导向"
        ],
        growth_drivers=[
            "医生资源整合",
            "患者教育",
            "服务标准化",
            "口碑传播"
        ],
        key_metrics=[
            "患者get成本",
            "复诊率",
            "处方转化率",
            "合规评分",
            "患者满意度"
        ],
        benchmarks={
            "patient_acquisition_cost": "< 500元",
            "return_visit_rate": "> 40%",
            "prescription_conversion": "> 25%",
            "compliance_score": "> 90",
            "patient_satisfaction": "> 4.2"
        },
        typical_challenges=[
            "监管政策变化",
            "医生资源稀缺",
            "用户隐私保护",
            "医疗责任风险"
        ],
        best_practices=[
            "建立专业医生团队",
            "完善质控体系",
            "患者教育先行",
            "合规优先运营"
        ],
        tags=["医疗", "健康", "监管", "专业"],
        special_attributes={
            "regulated": True,
            "professional": True,
            "trust_critical": True,
            "high_barrier": True
        }
    )

def init_education() -> IndustryProfile:
    """教育培训行业"""
    return IndustryProfile(
        industry_type=IndustryType.EDUCATION,
        name="教育培训",
        name_en="Education",
        description="教育培训服务",
        sub_types=["K12", "职业教育", "语言培训", "素质教育"],
        business_models=[BusinessModel.SUBSCRIPTION, BusinessModel.TRANSACTION],
        key_characteristics=[
            "强季节性",
            "效果导向",
            "口碑重要",
            "续费关键",
            "师资依赖"
        ],
        growth_drivers=[
            "教学效果提升",
            "口碑传播",
            "课程创新",
            "OMOfusion"
        ],
        key_metrics=[
            "完课率",
            "续费率",
            "转介绍率",
            "学习效果",
            "师资满意度"
        ],
        benchmarks={
            "completion_rate": "> 70%",
            "renewal_rate": "> 60%",
            "referral_rate": "> 30%",
            "learning_outcome": "> 80%",
            "teacher_satisfaction": "> 4.0"
        },
        typical_challenges=[
            "政策监管趋严",
            "获客成本高",
            "师资流失",
            "效果难以量化"
        ],
        best_practices=[
            "注重教学效果",
            "建立口碑体系",
            "OMO模式fusion",
            "师资培养计划"
        ],
        tags=["教育", "培训", "季节性", "效果"],
        special_attributes={
            "seasonal": True,
            "outcome_focused": True,
            "word_of_mouth": True
        }
    )

def init_real_estate() -> IndustryProfile:
    """房地产行业"""
    return IndustryProfile(
        industry_type=IndustryType.REAL_ESTATE,
        name="房地产",
        name_en="Real Estate",
        description="房地产交易与服务",
        sub_types=["新房", "二手房", "租房", "商业地产"],
        business_models=[BusinessModel.COMMISSION, BusinessModel.TRANSACTION],
        key_characteristics=[
            "高客单价",
            "decision周期长",
            "地域性强",
            "政策敏感",
            "低频高值"
        ],
        growth_drivers=[
            "房源质量",
            "经纪人服务",
            "线上化体验",
            "金融服务"
        ],
        key_metrics=[
            "线索转化率",
            "带看率",
            "成交周期",
            "客单价",
            "经纪人产能"
        ],
        benchmarks={
            "lead_conversion": "> 3%",
            "showing_rate": "> 40%",
            "deal_cycle": "< 60天",
            "avg_deal_value": "> 200万",
            "agent_productivity": "> 6单/年"
        },
        typical_challenges=[
            "市场波动大",
            "获客成本高",
            "经纪人管理",
            "政策不确定性"
        ],
        best_practices=[
            "房源真实保障",
            "经纪人赋能",
            "线上线下fusion",
            "金融服务闭环"
        ],
        tags=["房产", "高客单", "低频", "地域"],
        special_attributes={
            "high_value": True,
            "low_frequency": True,
            "local_focus": True,
            "policy_sensitive": True
        }
    )

def init_travel() -> IndustryProfile:
    """旅游出行行业"""
    return IndustryProfile(
        industry_type=IndustryType.TRAVEL,
        name="旅游出行",
        name_en="Travel & Hospitality",
        description="旅游出行服务",
        sub_types=["OTA", "酒店", "景区", "交通"],
        business_models=[BusinessModel.COMMISSION, BusinessModel.TRANSACTION],
        key_characteristics=[
            "强季节性",
            "体验导向",
            "价格敏感",
            "冲动消费",
            "分享属性"
        ],
        growth_drivers=[
            "产品创新",
            "内容种草",
            "会员体系",
            "社交传播"
        ],
        key_metrics=[
            "预订转化率",
            "复购率",
            "客单价",
            "NPS",
            "分享率"
        ],
        benchmarks={
            "booking_conversion": "> 5%",
            "repeat_rate": "> 25%",
            "aov": "> 2000元",
            "nps": "> 40",
            "share_rate": "> 15%"
        },
        typical_challenges=[
            "季节性波动",
            "获客成本高",
            "库存管理",
            "服务质量控制"
        ],
        best_practices=[
            "个性化推荐",
            "内容营销",
            "会员忠诚计划",
            "社交裂变"
        ],
        tags=["旅游", "出行", "季节性", "体验"],
        special_attributes={
            "seasonal": True,
            "experience_focused": True,
            "social_sharing": True
        }
    )

def init_food_beverage() -> IndustryProfile:
    """餐饮美食行业"""
    return IndustryProfile(
        industry_type=IndustryType.FOOD_BEVERAGE,
        name="餐饮美食",
        name_en="Food & Beverage",
        description="餐饮服务",
        sub_types=["连锁餐饮", "外卖", "茶饮", "烘焙"],
        business_models=[BusinessModel.TRANSACTION, BusinessModel.SUBSCRIPTION],
        key_characteristics=[
            "本地属性强",
            "高频消费",
            "口味依赖",
            "服务体验",
            "口碑传播"
        ],
        growth_drivers=[
            "产品创新",
            "门店扩张",
            "外卖增长",
            "会员体系"
        ],
        key_metrics=[
            "翻台率",
            "客单价",
            "复购率",
            "获客成本",
            "外卖占比"
        ],
        benchmarks={
            "turnover_rate": "> 3次/天",
            "aov": "> 50元",
            "repeat_rate": "> 40%",
            "cac": "< 30元",
            "delivery_ratio": "> 30%"
        },
        typical_challenges=[
            "租金成本高",
            "人员流动大",
            "食品安全",
            "同质化竞争"
        ],
        best_practices=[
            "标准化运营",
            "会员营销",
            "外卖优化",
            "品牌差异化"
        ],
        tags=["餐饮", "本地", "高频", "服务"],
        special_attributes={
            "local_focus": True,
            "high_frequency": True,
            "service_critical": True
        }
    )

def init_month1_profiles() -> Dict[IndustryType, IndustryProfile]:
    """初始化Month 1行业画像"""
    return {
        IndustryType.HEALTHCARE: init_healthcare(),
        IndustryType.EDUCATION: init_education(),
        IndustryType.REAL_ESTATE: init_real_estate(),
        IndustryType.TRAVEL: init_travel(),
        IndustryType.FOOD_BEVERAGE: init_food_beverage(),
    }
