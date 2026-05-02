"""
Growth + Industry → Pan-Wisdom Tree 整合桥接模块
==============================================
将 Growth Engine 和 Industry Engine 有价值内容接入 Pan-Wisdom Tree，
对 Pan-Wisdom Tree 实现升级。

整合内容（提炼自源板块）：
  1. GrowthPhase 增长阶段（5个）
  2. GrowthLevers 增长杠杆 / AARRR 框架（5个）
  3. StrategyType 战略类型（7个）
  4. GrowthStrategyEngine 核心方法签名
  5. IndustryType 行业类型（15个）
  6. BusinessModel 商业模式（6个）
  7. IndustryProfile 数据结构
  8. 八卦增长框架（BaGuaGrowthEngine）

升级 Pan-Wisdom Tree：
  - 新增 WisdomSchool.GROWTH_STRATEGY = "增长战略"
  - 新增 ProblemType: GROWTH_STRATEGY / INDUSTRY_ADAPTATION / GROWTH_DIAGNOSIS
  - 新增关键词映射和学派推荐映射
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

# ════════════════════════════════════════════════════════════════
#  Section 1：从 Growth Engine 提炼
# ════════════════════════════════════════════════════════════════


class GrowthPhase(Enum):
    """增长阶段（提炼自 growth_strategy.py）"""
    SEED = "seed"            # 种子期：0→1
    STARTUP = "startup"        # 启动期：找到PMF
    GROWTH = "growth"          # 增长期：快速扩张
    EXPANSION = "expansion"    # 扩张期：市场拓展
    MATURITY = "maturity"      # 成熟期：精细化运营


class GrowthLevers(Enum):
    """增长杠杆 / AARRR 框架（提炼自 growth_strategy.py）"""
    ACQUISITION = "acquisition"   # 获客
    ACTIVATION = "activation"     # 激活
    RETENTION = "retention"       # 留存
    REVENUE = "revenue"           # 变现
    REFERRAL = "referral"         # 推荐


class StrategyType(Enum):
    """战略类型（提炼自 growth_strategy.py）"""
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
    """增长指标（提炼自 growth_strategy.py）"""
    name: str
    current_value: float
    target_value: float
    unit: str
    timeframe: str
    priority: str = "high"

    @property
    def gap(self) -> float:
        return self.target_value - self.current_value

    @property
    def growth_rate_needed(self) -> float:
        if self.current_value == 0:
            return float("inf")
        return (self.target_value - self.current_value) / self.current_value * 100


@dataclass
class GrowthStrategyTemplate:
    """增长战略模板（提炼自 growth_strategy.py _init_strategy_templates）"""
    id: str
    name: str
    primary_levers: List[str]
    key_strategies: List[str]
    key_metrics: List[str]
    benchmarks: Dict[str, str]
    industry: str = "general"


# 内置战略模板库（提炼自 growth_strategy.py）
STRATEGY_TEMPLATES: List[GrowthStrategyTemplate] = [
    GrowthStrategyTemplate(
        id="saas_b2b",
        name="SaaS B2B 增长战略",
        primary_levers=["acquisition", "retention", "revenue"],
        key_strategies=["content_marketing", "sdr_outbound", "product_led_growth", "customer_success"],
        key_metrics=["MRR", "ARR", "Churn Rate", "LTV", "CAC", "NRR"],
        benchmarks={"ltv_cac_ratio": "> 3", "cac_payback": "< 12个月", "gross_margin": "> 70%", "nrr": "> 110%", "monthly_churn": "< 2%"},
        industry="saas_b2b",
    ),
    GrowthStrategyTemplate(
        id="saas_b2c",
        name="SaaS B2C 增长战略",
        primary_levers=["acquisition", "activation", "retention"],
        key_strategies=["viral_loop", "content_seo", "referral_program", "push_notification"],
        key_metrics=["DAU", "MAU", "Retention D1/D7/D30", "ARPU"],
        benchmarks={"d1_retention": "> 40%", "d7_retention": "> 20%", "d30_retention": "> 10%", "freemium_conversion": "2-5%", "monthly_churn": "< 5%"},
        industry="saas_b2c",
    ),
    GrowthStrategyTemplate(
        id="ecommerce",
        name="电商增长战略",
        primary_levers=["acquisition", "revenue", "retention"],
        key_strategies=["paid_ads", "seo", "email_marketing", "loyalty_program"],
        key_metrics=["GMV", "Conversion Rate", "AOV", "Repeat Purchase Rate", "ROAS"],
        benchmarks={"conversion_rate": "2-4%", "roas": "> 3", "repeat_rate": "> 30%"},
        industry="ecommerce",
    ),
    GrowthStrategyTemplate(
        id="fintech",
        name="金融科技增长战略",
        primary_levers=["acquisition", "activation", "revenue"],
        key_strategies=["compliance_first", "trust_building", "referral_incentive"],
        key_metrics=["AUM", "Transaction Volume", "Activation Rate", "Fraud Rate"],
        benchmarks={"activation_rate": "> 60%"},
        industry="fintech",
    ),
    GrowthStrategyTemplate(
        id="content_media",
        name="内容媒体增长战略",
        primary_levers=["acquisition", "retention", "referral"],
        key_strategies=["content_quality", "algorithm_recommendation", "community_building"],
        key_metrics=["DAU", "Time on Site", "Content Engagement Rate", "Share Rate"],
        benchmarks={"engagement_rate": "> 2%"},
        industry="content_media",
    ),
]


@dataclass
class GrowthFormula:
    """增长公式（提炼自 growth_strategy.py _init_growth_formulas）"""
    id: str
    formula: str
    description: str
    examples: Dict[str, str] = field(default_factory=dict)


# 内置增长公式库
GROWTH_FORMULAS: List[GrowthFormula] = [
    GrowthFormula(
        id="aarr",
        formula="Revenue = Acquisition × Activation × Retention × Referral × Revenue",
        description="海盗指标框架，每个环节提升10% = 整体提升61%",
        examples={"每个环节基准": "100→110: 整体 100→161"},
    ),
    GrowthFormula(
        id="north_star",
        formula="North Star Metric = f(用户价值 × 使用频率 × 用户数量)",
        description="北极星指标：反映核心用户价值交付的单一最重要指标",
        examples={"facebook": "DAU", "airbnb": "预订夜晚数", "slack": "活跃频道消息数"},
    ),
    GrowthFormula(
        id="viral_coefficient",
        formula="K = 邀请数 × 转化率",
        description="病毒系数 K > 1：指数增长；K = 1：线性增长；K < 1：依赖外部获客",
        examples={"target": "K > 0.5 即有显著病毒效应"},
    ),
    GrowthFormula(
        id="ltv_cac",
        formula="LTV/CAC = (ARPU × Gross Margin / Churn) / CAC",
        description="单位经济效益，LTV/CAC > 3 说明获客经济可持续",
        examples={"benchmark": "> 3"},
    ),
]


# ════════════════════════════════════════════════════════════════
#  Section 2：从 Industry Engine 提炼
# ════════════════════════════════════════════════════════════════


class IndustryType(Enum):
    """行业类型（提炼自 industry_profiles/_ip_types.py，15个行业）"""
    # 原有4个
    SAAS_B2B = "saas_b2b"
    SAAS_B2C = "saas_b2c"
    ECOMMERCE = "ecommerce"
    FINTECH = "fintech"
    # Month 1 新增5个
    HEALTHCARE = "health_care"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"
    TRAVEL = "travel"
    FOOD_BEVERAGE = "food_beverage"
    # Month 2 新增5个
    AI_TECH = "ai_tech"
    NEW_ENERGY = "new_energy"
    LUXURY = "luxury"
    SPORTS_FITNESS = "sports_fitness"
    PET = "pet"
    # Month 3 新增2个
    CONTENT_GAMING = "content_gaming"
    LOCAL_LIFE = "local_life"


class BusinessModel(Enum):
    """商业模式（提炼自 industry_profiles/_ip_types.py）"""
    SUBSCRIPTION = "subscription"
    TRANSACTION = "transaction"
    ADVERTISING = "advertising"
    FREEMIUM = "freemium"
    ENTERPRISE = "enterprise"
    COMMISSION = "commission"
    HYBRID = "hybrid"


@dataclass
class IndustryProfile:
    """行业画像（提炼自 industry_profiles/_ip_types.py 和 _ip_v1.py）"""
    industry_type: IndustryType
    name: str
    name_en: str
    description: str
    sub_types: List[str] = field(default_factory=list)
    business_models: List[BusinessModel] = field(default_factory=list)
    key_characteristics: List[str] = field(default_factory=list)
    growth_drivers: List[str] = field(default_factory=list)
    key_metrics: List[str] = field(default_factory=list)
    benchmarks: Dict[str, str] = field(default_factory=dict)
    typical_challenges: List[str] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    special_attributes: Dict[str, Any] = field(default_factory=dict)


# 内置行业画像库（提炼自 industry_profiles/_ip_v1.py）
INDUSTRY_PROFILES: Dict[str, IndustryProfile] = {}


def _init_industry_profiles() -> Dict[str, IndustryProfile]:
    """初始化行业画像库"""
    return {
        "saas_b2b": IndustryProfile(
            industry_type=IndustryType.SAAS_B2B,
            name="SaaS B2B",
            name_en="SaaS B2B",
            description="面向企业的软件即服务",
            sub_types=["CRM", "ERP", "HRM", "营销SaaS", "协同办公"],
            business_models=[BusinessModel.SUBSCRIPTION, BusinessModel.ENTERPRISE],
            key_characteristics=["长销售周期", "高客单价", "多决策者", "强服务属性", "网络效应有限"],
            growth_drivers=["产品主导增长(PLG)", "销售驱动", "客户成功扩张", "生态合作"],
            key_metrics=["MRR/ARR", "CAC", "LTV", "NRR", "Logo Churn", "Revenue Churn"],
            benchmarks={"ltv_cac_ratio": "> 3", "cac_payback": "< 12个月", "gross_margin": "> 70%", "nrr": "> 110%", "monthly_churn": "< 2%"},
            typical_challenges=["获客成本高", "销售周期长", "客户成功难度大", "产品复杂度高"],
            best_practices=["建立产品主导增长(PLG)体系", "投资内容营销建立思想领导力", "构建客户成功团队", "设计灵活的定价strategy"],
            tags=["B2B", "订阅制", "企业服务", "高客单价"],
            special_attributes={"high_touch": True, "long_sales_cycle": True},
        ),
        "saas_b2c": IndustryProfile(
            industry_type=IndustryType.SAAS_B2C,
            name="SaaS B2C",
            name_en="SaaS B2C",
            description="面向消费者的软件即服务",
            sub_types=["工具类", "效率类", "娱乐类", "健康类"],
            business_models=[BusinessModel.FREEMIUM, BusinessModel.SUBSCRIPTION],
            key_characteristics=["低客单价", "高用户量", "短决策周期", "强产品体验", "病毒传播潜力"],
            growth_drivers=["病毒式增长", "内容营销", "应用商店优化", "付费获客"],
            key_metrics=["MAU/DAU", "留存率", "付费转化率", "ARPU", "病毒系数K"],
            benchmarks={"d1_retention": "> 40%", "d7_retention": "> 20%", "d30_retention": "> 10%", "freemium_conversion": "2-5%", "monthly_churn": "< 5%"},
            typical_challenges=["留存难度大", "获客成本高", "付费转化低", "用户注意力分散"],
            best_practices=["设计病毒传播机制", "优化首次体验", "建立推送strategy", "A/B测试驱动优化"],
            tags=["B2C", "免费增值", "消费级", "病毒传播"],
            special_attributes={"viral_potential": True, "low_price": True},
        ),
    }


INDUSTRY_PROFILES = _init_industry_profiles()


# ════════════════════════════════════════════════════════════════
#  Section 3：从 BaGua Growth Engine 提炼
# ════════════════════════════════════════════════════════════════


class BaGua(Enum):
    """八卦枚举（提炼自 bagua_growth_engine.py）"""
    QIAN = ("乾", "☰", "天", "健", "战略规划", "刚健进取")
    DUI = ("兑", "☱", "泽", "悦", "销售转化", "商务谈判")
    LI = ("离", "☲", "火", "丽", "品牌公关", "客户服务")
    ZHEN = ("震", "☳", "雷", "动", "变革创新", "危机应对")
    XUN = ("巽", "☴", "风", "入", "营销传播", "渠道渗透")
    KAN = ("坎", "☵", "水", "陷", "风险管理", "财务管理")
    GEN = ("艮", "☶", "山", "止", "核心竞争力", "专业壁垒")
    KUN = ("坤", "☷", "地", "顺", "团队建设", "企业文化")

    def __init__(self, name_cn, symbol, element, virtue, domain1, action):
        self.name_cn = name_cn
        self.symbol = symbol
        self.element = element
        self.virtue = virtue
        self.domain1 = domain1
        self.action = action


# 八卦-商业映射（提炼自 bagua_growth_engine.py）
BAGUA_BUSINESS_MAP: Dict[str, Dict] = {
    "乾": {"domains": ["战略规划", "领导力", "品牌定位"], "strengths": ["战略眼光", "领导力强"]},
    "坤": {"domains": ["团队建设", "企业文化", "客户关系"], "strengths": ["团队稳定", "客户忠诚"]},
    "震": {"domains": ["变革创新", "危机应对", "市场突破"], "strengths": ["创新能力", "危机处理"]},
    "巽": {"domains": ["营销传播", "渠道渗透", "品牌传播"], "strengths": ["传播能力", "渠道布局"]},
    "坎": {"domains": ["风险管理", "财务管理", "产品迭代"], "strengths": ["风险意识", "财务稳健"]},
    "离": {"domains": ["客户服务", "品牌公关", "用户体验"], "strengths": ["客户口碑", "品牌美誉"]},
    "艮": {"domains": ["核心竞争力", "专业壁垒", "稳定发展"], "strengths": ["专业深度", "竞争壁垒"]},
    "兑": {"domains": ["商务谈判", "合作共赢", "销售转化"], "strengths": ["沟通能力", "转化率"]},
}


# ════════════════════════════════════════════════════════════════
#  Section 4：整合接口 — 接入 Pan-Wisdom Tree
# ════════════════════════════════════════════════════════════════


def get_growth_recommendation(problem_text: str, top_n: int = 3) -> List[Dict]:
    """
    根据问题文本，返回增长战略推荐（供 Pan-Wisdom Tree 调用）

    Args:
        problem_text: 问题描述
        top_n: 返回前N个推荐

    Returns:
        [{"template": ..., "confidence": ..., "reasoning": ...}, ...]
    """
    text = problem_text.lower()
    results = []

    for tpl in STRATEGY_TEMPLATES:
        score = 0.0
        for kw in tpl.name:
            if kw.lower() in text:
                score += 1.0
        if score > 0:
            results.append({
                "template": tpl,
                "confidence": min(0.95, 0.3 + score * 0.15),
                "source": "GrowthStrategyEngine",
            })

    # 按置信度排序
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results[:top_n]


def get_industry_profile(industry_id: str) -> Optional[IndustryProfile]:
    """获取行业画像（供 Pan-Wisdom Tree 调用）"""
    return INDUSTRY_PROFILES.get(industry_id)


def search_industry_profiles(query: str) -> List[IndustryProfile]:
    """搜索行业画像（供 Pan-Wisdom Tree 调用）"""
    query_lower = query.lower()
    results = []
    for profile in INDUSTRY_PROFILES.values():
        if (query_lower in profile.name.lower()
                or query_lower in profile.description.lower()
                or any(query_lower in tag.lower() for tag in profile.tags)):
            results.append(profile)
    return results


def get_bagua_analysis(problem_text: str) -> Optional[Dict]:
    """
    八卦增长分析（供 Pan-Wisdom Tree 调用）
    返回主导卦象和分析结果
    """
    text = problem_text
    scores = {bg.name: 0.0 for bg in BaGua}
    # 关键词匹配
    keyword_map = {
        "乾": ["战略", "领导", "规划", "定位"],
        "坤": ["团队", "文化", "客户关系", "运营"],
        "震": ["变革", "创新", "危机", "突破"],
        "巽": ["营销", "传播", "渠道", "渗透"],
        "坎": ["风险", "财务", "迭代", "合规"],
        "离": ["品牌", "服务", "体验", "公关"],
        "艮": ["核心", "壁垒", "稳定", "专业"],
        "兑": ["谈判", "合作", "转化", "销售"],
    }
    for bagua_name, keywords in keyword_map.items():
        for kw in keywords:
            if kw in text:
                scores[bagua_name] += 1.0

    # 找出主导卦
    dominant = max(scores, key=scores.get)
    if scores[dominant] == 0:
        return None

    info = BAGUA_BUSINESS_MAP.get(dominant, {})
    return {
        "dominant_bagua": dominant,
        "symbol": BaGua[dominant].symbol,
        "domains": info.get("domains", []),
        "strengths": info.get("strengths", []),
        "score": scores[dominant],
    }


def get_growth_formula(formula_id: str) -> Optional[GrowthFormula]:
    """获取增长公式（供 Pan-Wisdom Tree 调用）"""
    for f in GROWTH_FORMULAS:
        if f.id == formula_id:
            return f
    return None


def list_growth_templates() -> List[GrowthStrategyTemplate]:
    """列出所有增长战略模板"""
    return STRATEGY_TEMPLATES


def list_industry_profiles() -> List[IndustryProfile]:
    """列出所有行业画像"""
    return list(INDUSTRY_PROFILES.values())


# 模块版本
__version__ = "1.0.0"
__source__ = "Growth Engine + Industry Engine (提炼整合)"
