"""
__all__ = [
    'init_ai_tech',
    'init_luxury',
    'init_month2_profiles',
    'init_new_energy',
    'init_pet',
    'init_sports_fitness',
]

Month 2 新增行业画像 (5个行业)
"""

from typing import Dict
from ._ip_types import IndustryType, IndustryProfile, BusinessModel

def init_ai_tech() -> IndustryProfile:
    """AI科技行业"""
    return IndustryProfile(
        industry_type=IndustryType.AI_TECH,
        name="AI科技",
        name_en="AI Technology",
        description="人工智能技术与应用",
        sub_types=["大模型", "AI应用", "AI基础设施", "AI服务"],
        business_models=[BusinessModel.SUBSCRIPTION, BusinessModel.TRANSACTION, BusinessModel.FREEMIUM],
        key_characteristics=[
            "技术迭代快",
            "研发投入大",
            "场景落地难",
            "人才稀缺",
            "生态竞争"
        ],
        growth_drivers=[
            "技术创新",
            "场景落地",
            "生态建设",
            "API经济"
        ],
        key_metrics=[
            "模型调用量",
            "API收入",
            "客户留存",
            "技术迭代速度",
            "人才密度"
        ],
        benchmarks={
            "api_calls": "> 100万/日",
            "api_revenue": "> 100万/月",
            "customer_retention": "> 80%",
            "iteration_cycle": "< 2周",
            "talent_density": "> 50%"
        },
        typical_challenges=[
            "技术商业化",
            "算力成本高",
            "数据get难",
            "监管不确定"
        ],
        best_practices=[
            "快速迭代",
            "场景聚焦",
            "生态合作",
            "开源strategy"
        ],
        tags=["AI", "技术", "创新", "前沿"],
        special_attributes={
            "emerging": True,
            "tech_driven": True,
            "high_rnd": True
        }
    )

def init_new_energy() -> IndustryProfile:
    """新能源汽车行业"""
    return IndustryProfile(
        industry_type=IndustryType.NEW_ENERGY,
        name="新能源汽车",
        name_en="New Energy Vehicle",
        description="新能源汽车及相关服务",
        sub_types=["整车", "充电", "零部件", "出行服务"],
        business_models=[BusinessModel.TRANSACTION, BusinessModel.SUBSCRIPTION],
        key_characteristics=[
            "资本密集",
            "政策驱动",
            "技术迭代",
            "品牌重要",
            "服务生态"
        ],
        growth_drivers=[
            "产品创新",
            "渠道扩张",
            "服务生态",
            "品牌塑造"
        ],
        key_metrics=[
            "试驾转化率",
            "订单量",
            "交付周期",
            "客户满意度",
            "充电网络覆盖"
        ],
        benchmarks={
            "test_drive_conversion": "> 20%",
            "monthly_orders": "> 1000",
            "delivery_cycle": "< 4周",
            "csat": "> 4.5",
            "charging_coverage": "> 100城"
        },
        typical_challenges=[
            "供应链稳定",
            "充电基础设施",
            "品牌认知",
            "售后服务"
        ],
        best_practices=[
            "直营模式",
            "用户社区",
            "OTA升级",
            "服务闭环"
        ],
        tags=["新能源", "汽车", "资本密集", "政策"],
        special_attributes={
            "capital_intensive": True,
            "policy_driven": True,
            "brand_critical": True
        }
    )

def init_luxury() -> IndustryProfile:
    """奢侈品行业"""
    return IndustryProfile(
        industry_type=IndustryType.LUXURY,
        name="奢侈品",
        name_en="Luxury Goods",
        description="奢侈品零售与服务",
        sub_types=["箱包", "腕表", "珠宝", "时装"],
        business_models=[BusinessModel.TRANSACTION],
        key_characteristics=[
            "品牌至上",
            "稀缺性",
            "高客单价",
            "体验重要",
            "情感连接"
        ],
        growth_drivers=[
            "品牌故事",
            "VIP服务",
            "限量strategy",
            "数字化转型"
        ],
        key_metrics=[
            "品牌认知度",
            "VIP转化率",
            "复购率",
            "客单价",
            "品牌溢价"
        ],
        benchmarks={
            "brand_awareness": "> 60%",
            "vip_conversion": "> 15%",
            "repeat_rate": "> 35%",
            "aov": "> 10000元",
            "brand_premium": "> 200%"
        },
        typical_challenges=[
            "假货问题",
            "年轻化转型",
            "电商平衡",
            "文化差异"
        ],
        best_practices=[
            "品牌传承",
            "稀缺营销",
            "VIP体验",
            "数字化谨慎"
        ],
        tags=["奢侈品", "品牌", "高端", "体验"],
        special_attributes={
            "brand_critical": True,
            "premium_focus": True,
            "experience_focused": True
        }
    )

def init_sports_fitness() -> IndustryProfile:
    """运动健身行业"""
    return IndustryProfile(
        industry_type=IndustryType.SPORTS_FITNESS,
        name="运动健身",
        name_en="Sports & Fitness",
        description="运动健身服务",
        sub_types=["健身房", "运动APP", "装备", "赛事"],
        business_models=[BusinessModel.SUBSCRIPTION, BusinessModel.TRANSACTION],
        key_characteristics=[
            "社区属性",
            "效果导向",
            "习惯养成",
            "社交传播",
            "内容驱动"
        ],
        growth_drivers=[
            "内容社区",
            "社交激励",
            "数据追踪",
            "IP打造"
        ],
        key_metrics=[
            "活跃率",
            "续费率",
            "课程完成率",
            "社交分享率",
            "社区互动"
        ],
        benchmarks={
            "active_rate": "> 40%",
            "renewal_rate": "> 50%",
            "completion_rate": "> 60%",
            "share_rate": "> 20%",
            "community_engagement": "> 30%"
        },
        typical_challenges=[
            "用户坚持难",
            "获客成本高",
            "教练管理",
            "同质化竞争"
        ],
        best_practices=[
            "游戏化设计",
            "社区运营",
            "数据可视化",
            "KOL合作"
        ],
        tags=["运动", "健身", "社区", "健康"],
        special_attributes={
            "community_focus": True,
            "outcome_focused": True,
            "habit_forming": True
        }
    )

def init_pet() -> IndustryProfile:
    """宠物经济行业"""
    return IndustryProfile(
        industry_type=IndustryType.PET,
        name="宠物经济",
        name_en="Pet Economy",
        description="宠物相关产品与服务",
        sub_types=["宠物食品", "医疗", "用品", "服务"],
        business_models=[BusinessModel.TRANSACTION, BusinessModel.SUBSCRIPTION],
        key_characteristics=[
            "情感消费",
            "高频复购",
            "品质敏感",
            "社区活跃",
            "拟人化趋势"
        ],
        growth_drivers=[
            "品质升级",
            "服务创新",
            "社区运营",
            "内容种草"
        ],
        key_metrics=[
            "复购率",
            "客单价",
            "会员渗透率",
            "社区活跃度",
            "内容互动"
        ],
        benchmarks={
            "repeat_rate": "> 60%",
            "aov": "> 200元",
            "member_penetration": "> 40%",
            "community_activity": "> 35%",
            "content_engagement": "> 25%"
        },
        typical_challenges=[
            "品牌忠诚度",
            "产品质量",
            "服务标准化",
            "监管趋严"
        ],
        best_practices=[
            "品质保障",
            "情感营销",
            "会员体系",
            "社区建设"
        ],
        tags=["宠物", "情感", "复购", "社区"],
        special_attributes={
            "emotional_connection": True,
            "high_frequency": True,
            "community_focus": True
        }
    )

def init_month2_profiles() -> Dict[IndustryType, IndustryProfile]:
    """初始化Month 2行业画像"""
    return {
        IndustryType.AI_TECH: init_ai_tech(),
        IndustryType.NEW_ENERGY: init_new_energy(),
        IndustryType.LUXURY: init_luxury(),
        IndustryType.SPORTS_FITNESS: init_sports_fitness(),
        IndustryType.PET: init_pet(),
    }
