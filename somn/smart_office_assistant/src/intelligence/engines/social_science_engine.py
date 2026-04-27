"""
__all__ = [
    'analyze',
    'get_available_domains',
    'get_model_count',
]

社会科学fusion智慧引擎 v1.0
Social Science Fusion Wisdom Engine

fusion三篇博士级深度学习文档:
- 市场营销学深度学习文档(853行,8部分,30+模型)
- 市场经济学深度学习文档(1411行,10部分,35+模型)
- 社会发展学深度学习文档(1662行,9部分,40+理论)

核心能力:
1. 市场营销分析 - STP战略/4P/7P/CBBE品牌/AARRR增长/RFM
2. 市场经济分析 - 供需均衡/弹性/市场结构/博弈论/行为经济学
3. 社会发展分析 - 社会分层/现代化理论/依附论/世界体系/风险社会
4. 跨域fusion - 营销×经济×社会三维度交叉分析

版本: v1.0
日期: 2026-04-02
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class SocialScienceDomain(Enum):
    """社会科学子领域"""
    MARKETING = "市场营销"
    ECONOMICS = "市场经济学"
    SOCIAL_DEVELOPMENT = "社会发展学"
    CROSS_DOMAIN = "跨域fusion"

class MarketStructure(Enum):
    """市场结构类型"""
    PERFECT_COMPETITION = "完全竞争"
    MONOPOLISTIC_COMPETITION = "垄断竞争"
    OLIGOPOLY = "寡头垄断"
    MONOPOLY = "垄断"

@dataclass
class MarketingInsight:
    """营销洞察"""
    stp_strategy: str = ""           # STP战略建议
    four_p_mix: Dict[str, str] = field(default_factory=dict)  # 4P/7P组合
    brand_strategy: str = ""         # 品牌strategy
    digital_funnel: str = ""         # 数字营销漏斗
    growth_metrics: Dict[str, str] = field(default_factory=dict)  # 增长metrics
    consumer_insight: str = ""       # 消费者洞察
    ancient_source: str = ""         # 古典理论来源
    modern_application: str = ""     # 现代应用mapping

@dataclass
class EconomicInsight:
    """经济分析洞察"""
    supply_demand: str = ""          # 供需分析
    market_structure: str = ""       # 市场结构
    elasticity: str = ""             # 弹性分析
    game_theory: str = ""            # 博弈论分析
    behavioral_econ: str = ""        # 行为经济学
    welfare_analysis: str = ""       # 福利分析
    ancient_source: str = ""
    modern_application: str = ""

@dataclass
class SocialDevelopmentInsight:
    """社会发展洞察"""
    development_stage: str = ""      # 发展阶段judge
    inequality: str = ""             # 不平等分析
    social_mobility: str = ""        # 社会流动性
    modernization_path: str = ""     # 现代化路径
    risk_assessment: str = ""        # 风险社会评估
    policy_suggestion: str = ""      # 政策建议
    ancient_source: str = ""
    modern_application: str = ""

@dataclass
class SocialScienceAnalysis:
    """社会科学synthesize分析结果"""
    domain: SocialScienceDomain
    primary_insight: str
    marketing: Optional[MarketingInsight] = None
    economic: Optional[EconomicInsight] = None
    social: Optional[SocialDevelopmentInsight] = None
    cross_domain_synthesis: str = ""
    action_items: List[str] = field(default_factory=list)
    risk_warnings: List[str] = field(default_factory=list)
    confidence: float = 0.0

class SocialScienceWisdomEngine:
    """
    社会科学fusion智慧引擎

    整合市场营销学,市场经济学,社会发展学三大领域,
    为增长解决方案提供社会科学维度的深度分析.
    """

    def __init__(self):
        self._marketing_models = self._init_marketing_models()
        self._economic_models = self._init_economic_models()
        self._social_theories = self._init_social_theories()

    # ============================================================
    # init:知识库
    # ============================================================

    def _init_marketing_models(self) -> Dict[str, Dict]:
        """init营销模型知识库"""
        return {
            "stp": {
                "name": "STP战略框架",
                "creator": "菲利普·科特勒",
                "components": ["市场细分(Segmentation)", "目标市场(Targeting)", "市场定位(Positioning)"],
                "segmentation_bases": ["地理", "人口统计", "心理", "行为"],
                "description": "营销战略的核心框架,从市场细分到精准定位"
            },
            "four_p": {
                "name": "4P营销组合",
                "components": ["产品(Product)", "价格(Price)", "渠道(Place)", "促销(Promotion)"],
                "evolution": "4P → 4C → 4R → 4V",
                "description": "营销组合的经典框架,产品/价格/渠道/促销"
            },
            "seven_p": {
                "name": "7P服务营销",
                "components": ["产品", "价格", "渠道", "促销", "人员(People)", "过程(Process)", "物理证据(Physical Evidence)"],
                "description": "服务业营销扩展模型"
            },
            "cbbe": {
                "name": "凯勒CBBE品牌资产模型",
                "components": ["品牌知名度", "品牌意义", "品牌反应", "品牌共鸣"],
                "description": "基于顾客心智的品牌资产构建四步金字塔"
            },
            "aarrr": {
                "name": "AARRR增长模型",
                "components": ["get(Acquisition)", "激活(Activation)", "留存(Retention)", "变现(Revenue)", "推荐(Referral)"],
                "description": "海盗metrics增长模型,覆盖用户全生命周期"
            },
            "rfm": {
                "name": "RFM客户分群模型",
                "components": ["最近购买(Recency)", "购买频率(Frequency)", "购买金额(Monetary)"],
                "description": "基于消费行为的客户价值分群"
            },
            "blue_ocean": {
                "name": "蓝海战略",
                "framework": "消除-减少-创造-提升(ERRC)",
                "description": "跳出竞争,创造无人争抢的市场空间"
            },
            "porter_strategy": {
                "name": "波特竞争战略",
                "options": ["成本领先", "差异化", "集中化"],
                "description": "三种基本竞争战略选择"
            },
            "consumer_decision": {
                "name": "消费者decision五阶段",
                "stages": ["问题认知", "信息搜索", "方案评估", "购买decision", "购后行为"],
                "description": "消费者购买decision的完整流程"
            },
            "customer_journey": {
                "name": "客户旅程地图",
                "stages": ["认知", "考虑", "购买", "使用", "忠诚"],
                "description": "客户全触点体验管理"
            },
            "service_dominant_logic": {
                "name": "服务主导逻辑(S-D Logic)",
                "core": "价值由使用者和生产者共同创造",
                "description": "Vargo & Lusch,从商品交换转向服务共创"
            },
        }

    def _init_economic_models(self) -> Dict[str, Dict]:
        """init经济学模型知识库"""
        return {
            "supply_demand": {
                "name": "供需均衡理论",
                "core": "Qd = Qs 时市场出清",
                "description": "市场价格由供给和需求两股力量共同决定"
            },
            "elasticity": {
                "name": "弹性理论",
                "types": ["需求价格弹性(Ed)", "需求收入弹性(Ei)", "供给价格弹性(Es)", "交叉弹性(Exy)"],
                "description": "衡量经济变量之间的敏感程度"
            },
            "market_structure": {
                "name": "市场结构理论",
                "types": ["完全竞争", "垄断竞争", "寡头垄断", "完全垄断"],
                "description": "不同市场结构下的企业行为与效率分析"
            },
            "game_theory": {
                "name": "博弈论",
                "concepts": ["纳什均衡", "占优strategy", "囚徒困境", "古诺模型", "伯特兰模型"],
                "description": "strategy互动中的理性decision分析"
            },
            "behavioral_economics": {
                "name": "行为经济学",
                "theories": ["有限理性(西蒙)", "前景理论(卡尼曼)", "助推理论(泰勒)"],
                "description": "对理性经济人假设的修正,揭示真实decision偏差"
            },
            "information_economics": {
                "name": "信息经济学",
                "concepts": ["逆向选择(阿克洛夫)", "道德风险", "信号传递(斯宾塞)", "委托代理"],
                "description": "信息不对称对市场效率的影响"
            },
            "welfare_economics": {
                "name": "福利经济学",
                "concepts": ["帕累托最优", "消费者剩余", "生产者剩余", "无谓损失"],
                "theorems": ["福利经济学第一定理", "福利经济学第二定理"],
                "description": "市场效率与社会福利的评估框架"
            },
            "production_cost": {
                "name": "生产与成本理论",
                "functions": ["柯布-道格拉斯(C-D)", "CES", "Leontief"],
                "concepts": ["边际报酬递减", "规模经济", "机会成本"],
                "description": "企业生产decision与成本结构分析"
            },
            "macro_ad_as": {
                "name": "AD-AS模型",
                "components": ["总需求(AD)", "短期总供给(SRAS)", "长期总供给(LRAS)"],
                "description": "宏观经济总量分析与政策效应评估"
            },
            "international_trade": {
                "name": "国际贸易理论",
                "theories": ["绝对优势(斯密)", "比较优势(李嘉图)", "新贸易理论"],
                "description": "贸易模式与全球化效应分析"
            },
        }

    def _init_social_theories(self) -> Dict[str, Dict]:
        """init社会发展理论知识库"""
        return {
            "modernization": {
                "name": "现代化理论",
                "representatives": ["罗斯托(经济成长阶段)", "英格尔斯(人的现代化)", "帕森斯(AGIL)"],
                "stages": ["传统社会", "起飞前提", "起飞", "成熟", "大众消费", "追求质量"],
                "description": "社会从传统向现代转型的线性发展理论"
            },
            "dependency": {
                "name": "依附理论",
                "representatives": ["普雷维什", "弗兰克", "卡多佐", "桑托斯"],
                "core": "第三世界不发展是资本主义世界体系依附关系的产物",
                "description": "对现代化理论的批判,强调结构性依附"
            },
            "world_systems": {
                "name": "世界体系理论",
                "creator": "沃勒斯坦",
                "structure": ["中心(Core)", "半边缘(Semi-periphery)", "边缘(Periphery)"],
                "description": "全球层面的结构性不平等与发展动态"
            },
            "social_stratification": {
                "name": "社会分层理论",
                "approaches": ["马克思(阶级)", "韦伯(多元分层)", "功能主义 vs 冲突论"],
                "metrics": ["基尼系数", "洛伦兹曲线", "皮凯蒂 r>g"],
                "description": "社会不平等的结构化分析"
            },
            "social_mobility": {
                "name": "社会流动理论",
                "types": ["代际流动", "代内流动", "垂直流动", "水平流动"],
                "mechanisms": ["人力资本", "社会资本", "制度机制", "市场机制"],
                "description": "社会地位变迁的规律与机制"
            },
            "risk_society": {
                "name": "风险社会理论",
                "creator": "贝克",
                "core": "工业社会→风险社会,人为风险取代自然风险",
                "description": "现代性反思与风险治理新范式"
            },
            "anomie": {
                "name": "失范理论",
                "creator": "涂尔干",
                "core": "社会规范失去效力,整合出现危机",
                "description": "社会快速变迁中的规范真空与整合危机"
            },
            "social_capital": {
                "name": "社会资本理论",
                "representatives": ["普特南", "科尔曼"],
                "types": ["认知型(信任/规范)", "结构型(网络)", "桥接型 vs 粘结型"],
                "description": "信任,网络与规范对社会协作的促进作用"
            },
            "community_gesellschaft": {
                "name": "共同体与社会",
                "creator": "滕尼斯",
                "types": ["共同体(Gemeinschaft) - 血缘/情感/传统", "社会(Gesellschaft) - 利益/契约/理性"],
                "description": "社会关系类型的经典二分法"
            },
            "ecological_modernization": {
                "name": "生态现代化理论",
                "core": "经济发展与环境改善可以兼容",
                "description": "可持续发展与绿色转型的理论基础"
            },
        }

    # ============================================================
    # 核心分析方法
    # ============================================================

    def analyze(self, user_input: str, context: Optional[Dict] = None) -> SocialScienceAnalysis:
        """
        社会科学synthesize分析入口

        Args:
            user_input: 用户输入的问题/场景
            context: 上下文信息(行业,客户信息等)

        Returns:
            SocialScienceAnalysis: synthesize分析结果
        """
        ctx = context or {}
        industry = ctx.get("industry", "")
        problem_type = self._detect_problem_type(user_input)

        # 根据问题类型路由到对应分析
        if problem_type == "marketing":
            insight = self._marketing_analysis(user_input, ctx)
            return SocialScienceAnalysis(
                domain=SocialScienceDomain.MARKETING,
                primary_insight=insight.stp_strategy or insight.brand_strategy,
                marketing=insight,
                action_items=self._extract_marketing_actions(insight),
                risk_warnings=self._extract_marketing_risks(insight),
                confidence=0.85
            )
        elif problem_type == "economic":
            insight = self._economic_analysis(user_input, ctx)
            return SocialScienceAnalysis(
                domain=SocialScienceDomain.ECONOMICS,
                primary_insight=insight.supply_demand or insight.market_structure,
                economic=insight,
                action_items=self._extract_economic_actions(insight),
                risk_warnings=self._extract_economic_risks(insight),
                confidence=0.82
            )
        elif problem_type == "social":
            insight = self._social_analysis(user_input, ctx)
            return SocialScienceAnalysis(
                domain=SocialScienceDomain.SOCIAL_DEVELOPMENT,
                primary_insight=insight.development_stage or insight.modernization_path,
                social=insight,
                action_items=self._extract_social_actions(insight),
                risk_warnings=self._extract_social_risks(insight),
                confidence=0.80
            )
        else:
            # 跨域fusion分析
            return self._cross_domain_analysis(user_input, ctx)

    def _detect_problem_type(self, text: str) -> str:
        """检测问题类型"""
        marketing_keywords = ["营销", "品牌", "客户", "市场定位", "推广", "广告", "增长", "留存",
                              "转化", "私域", "营销组合", "STP", "4P", "品牌资产"]
        economic_keywords = ["价格", "供需", "成本", "竞争", "垄断", "定价", "弹性", "市场结构",
                             "博弈", "均衡", "利润", "税收", "贸易"]
        social_keywords = ["社会", "发展", "不平等", "贫困", "城市化", "教育", "福利", "风险",
                           "全球化", "分层", "流动", "现代化", "乡村振兴"]

        text_lower = text.lower()
        m_score = sum(1 for kw in marketing_keywords if kw in text_lower)
        e_score = sum(1 for kw in economic_keywords if kw in text_lower)
        s_score = sum(1 for kw in social_keywords if kw in text_lower)

        scores = {"marketing": m_score, "economic": e_score, "social": s_score}
        max_type = max(scores, key=scores.get)
        return max_type if scores[max_type] > 0 else "cross"

    # ============================================================
    # 市场营销分析
    # ============================================================

    def _marketing_analysis(self, user_input: str, ctx: Dict) -> MarketingInsight:
        """市场营销深度分析"""
        insight = MarketingInsight()

        # STP战略分析
        insight.stp_strategy = self._generate_stp_strategy(user_input, ctx)

        # 4P/7P组合建议
        insight.four_p_mix = self._generate_four_p_mix(user_input, ctx)

        # 品牌战略
        insight.brand_strategy = self._generate_brand_strategy(user_input, ctx)

        # 数字营销漏斗
        insight.digital_funnel = self._generate_digital_funnel(user_input, ctx)

        # 增长metrics
        insight.growth_metrics = self._generate_growth_metrics(ctx)

        # 消费者洞察
        insight.consumer_insight = self._generate_consumer_insight(user_input, ctx)

        # 古典理论来源
        insight.ancient_source = "科特勒<营销管理>第19版 + 凯勒<战略品牌管理>第5版"
        insight.modern_application = "整合STP→4P→CBBE→AARRR全链路营销战略"

        return insight

    def _generate_stp_strategy(self, text: str, ctx: Dict) -> str:
        """generateSTP战略建议"""
        industry = ctx.get("industry", "通用")

        return (
            f"[STP战略分析 - {industry}行业]\n"
            "▎市场细分(Segmentation):\n"
            "  - 地理细分:一/二/三线城市差异;区域消费习惯\n"
            "  - 人口统计:年龄(Z世代/千禧/银发),收入层级,家庭结构\n"
            "  - 心理细分:价值观导向(品质/性价比/环保/社交认同),生活方式\n"
            "  - 行为细分:购买频率,品牌忠诚度,使用场景,价格敏感度\n"
            "▎目标市场(Targeting)建议:\n"
            "  - 评估标准:细分市场规模,增长潜力,竞争强度,企业资源匹配\n"
            "  - 推荐strategy:选择性专业化(2-3个高价值细分市场)\n"
            "▎市场定位(Positioning)框架:\n"
            "  - 定位语句:对于[目标群体],我们的[品牌]是[品类],它[核心利益],因为[差异化理由]\n"
            "  - 定位地图:在[价格]×[品质]维度建立差异化位置\n"
        )

    def _generate_four_p_mix(self, text: str, ctx: Dict) -> Dict[str, str]:
        """generate4P/7P营销组合建议"""
        return {
            "产品(Product)": "核心产品→形式产品→期望产品→延伸产品→潜在产品五层次分析",
            "价格(Price)": "基于价值感知的定价strategy;参考需求价格弹性Edjudge调价空间",
            "渠道(Place)": "全渠道(Omni-channel)布局;线上(电商+私域)+线下(体验店+经销)",
            "促销(Promotion)": "整合营销传播(IMC);认知→兴趣→考虑→购买→忠诚全漏斗",
            "人员(People)": "员工作为品牌大使;服务接触点管理;客户旅程地图优化",
            "过程(Process)": "服务蓝图设计;等待时间管理;标准化+个性化平衡",
            "物理证据(Physical Evidence)": "品牌视觉系统(VIS);数字化触点体验;环境氛围设计"
        }

    def _generate_brand_strategy(self, text: str, ctx: Dict) -> str:
        """generate品牌战略建议"""
        return (
            "[CBBE品牌资产构建四步模型]\n"
            "① 品牌recognize(Identity):建立品牌认知深度与广度\n"
            "② 品牌含义(Meaning):建立品牌绩效+品牌Imagery\n"
            "③ 品牌反应(Response):引导品牌judge+品牌感受\n"
            "④ 品牌共鸣(Resonance):行为忠诚+态度依附+社区认同+主动介入\n\n"
            "品牌定位三角:\n"
            "  ┌──────────┐\n"
            "  │ 品牌是什么 │ ← 理性利益点\n"
            "  │ 代表什么  │ ← 情感价值点\n"
            "  │ 用户关系  │ ← 品牌人格\n"
            "  └──────────┘"
        )

    def _generate_digital_funnel(self, text: str, ctx: Dict) -> str:
        """generate数字营销漏斗建议"""
        return (
            "[AARRR增长漏斗]\n"
            "get(Acquisition) → 激活(Activation) → 留存(Retention) → 变现(Revenue) → 推荐(Referral)\n\n"
            "关键metrics:\n"
            "  - CAC(客户get成本)= 营销总支出 / 新客户数\n"
            "  - LTV/CLV(客户终身价值)= ARPU × 客户生命周期\n"
            "  - LTV:CAC ≥ 3:1 为健康比值\n"
            "  - NPS(净推荐值)= 推荐者% - 贬损者%\n\n"
            "私域运营四步:沉淀→分层→运营→转化"
        )

    def _generate_growth_metrics(self, ctx: Dict) -> Dict[str, str]:
        """generate增长metrics体系"""
        return {
            "CAC": "营销总支出/新客户数 - 控制获客成本",
            "LTV": "ARPU × 生命周期 - 提升客户终身价值",
            "NPS": "推荐者%-贬损者% - 衡量口碑健康度",
            "留存率": "(期末-新增)/期初 - 核心增长引擎",
            "营销ROI": "(收入-成本)/成本 - 衡量营销效率",
            "RFM": "最近购买/频率/金额 - 客户价值分群"
        }

    def _generate_consumer_insight(self, text: str, ctx: Dict) -> str:
        """generate消费者洞察"""
        return (
            "[消费者行为分析框架]\n"
            "decision五阶段:问题认知→信息搜索→方案评估→购买decision→购后行为\n"
            "影响因素四维:文化(价值观/亚文化)→社会(参照群/家庭)→个人(年龄/职业/生活方式)→心理(动机/知觉/学习)\n"
            "VALS生活方式细分:创新者/思考者/信仰者/成就者/奋斗者/体验者/制造者/生存者\n"
            "行为经济学修正:参照依赖,损失厌恶(λ≈2.5),双曲贴现,助推设计"
        )

    # ============================================================
    # 市场经济分析
    # ============================================================

    def _economic_analysis(self, user_input: str, ctx: Dict) -> EconomicInsight:
        """市场经济学深度分析"""
        insight = EconomicInsight()

        insight.supply_demand = self._analyze_supply_demand(user_input, ctx)
        insight.market_structure = self._analyze_market_structure(user_input, ctx)
        insight.elasticity = self._analyze_elasticity(user_input, ctx)
        insight.game_theory = self._analyze_game_theory(user_input, ctx)
        insight.behavioral_econ = self._analyze_behavioral_econ(user_input, ctx)
        insight.welfare_analysis = self._analyze_welfare(user_input, ctx)

        insight.ancient_source = "曼昆<经济学原理>+ 平狄克<微观经济学>+ 范里安<现代观点>"
        insight.modern_application = "供需均衡分析 + 市场结构judge + 行为经济学助推 + 福利评估"

        return insight

    def _analyze_supply_demand(self, text: str, ctx: Dict) -> str:
        """供需分析"""
        return (
            "[供需均衡分析]\n"
            "均衡条件:Qd = Qs\n"
            "需求定律:P↑ → Qd↓(反向关系)\n"
            "供给定律:P↑ → Qs↑(同向关系)\n\n"
            "价格变动影响矩阵:\n"
            "          需求↑  需求↓  供给↑  供给↓\n"
            "均衡价格:  ↑     ↓     ↓     ↑\n"
            "均衡数量:  ↑     ↓     ↑     ↓\n\n"
            "消费者剩余(CS) = 意愿支付 - 实际支付\n"
            "生产者剩余(PS) = 实际获得 - 生产成本\n"
            "社会总福利 = CS + PS"
        )

    def _analyze_market_structure(self, text: str, ctx: Dict) -> str:
        """市场结构分析"""
        return (
            "[市场结构四类型分析]\n"
            "┌─────────────┬──────────┬──────────┬──────────┬──────────┐\n"
            "│ 维度        │ 完全竞争 │ 垄断竞争 │ 寡头垄断 │ 完全垄断 │\n"
            "├─────────────┼──────────┼──────────┼──────────┼──────────┤\n"
            "│ 厂商数量    │ 众多     │ 众多     │ 少数     │ 一家     │\n"
            "│ 产品差异    │ 无       │ 有       │ 有/无    │ 无替代品 │\n"
            "│ 进入壁垒    │ 无       │ 低       │ 高       │ 极高     │\n"
            "│ 定价能力    │ 接受者   │ 有限     │ 相互依存 │ 制定者   │\n"
            "│ P vs MC     │ P=MC     │ P>MC     │ P>MC     │ P>>MC    │\n"
            "│ 效率        │ 最优     │ 轻微损失 │ 中等损失 │ 最大损失 │\n"
            "└─────────────┴──────────┴──────────┴──────────┴──────────┘\n\n"
            "博弈论补充(寡头竞争):\n"
            "  - 古诺模型:产量竞争 → 行业产量 = 垄断产量的n/(n+1)\n"
            "  - 伯特兰模型:价格竞争 → P=MC(竞争价格)\n"
            "  - 斯塔克伯格:领导-跟随 → 先动优势"
        )

    def _analyze_elasticity(self, text: str, ctx: Dict) -> str:
        """弹性分析"""
        return (
            "[弹性分析框架]\n"
            "需求价格弹性 Ed = (ΔQ/Q)/(ΔP/P)\n"
            "  Ed=0 完全无弹性(必需品)| 0<Ed<1 缺乏弹性(食品)\n"
            "  Ed=1 单位弹性 | 1<Ed<∞ 富有弹性(奢侈品)| Ed=∞ 完全弹性\n\n"
            "弹性与收益关系:\n"
            "  Ed>1:降价→总收入增加(薄利多销有效)\n"
            "  Ed<1:提价→总收入增加(刚需品可提价)\n"
            "  Ed=1:价格变动不影响总收入\n\n"
            "交叉弹性 Exy > 0:替代品 | Exy < 0:互补品"
        )

    def _analyze_game_theory(self, text: str, ctx: Dict) -> str:
        """博弈论分析"""
        return (
            "[博弈论分析框架]\n"
            "核心概念:参与人,strategy,支付,信息,结果\n"
            "纳什均衡:每人strategy都是对他人strategy的最优反应\n"
            "囚徒困境:个体理性→集体非理性,合作困境\n\n"
            "应用场景:\n"
            "  - 价格战分析:伯特兰均衡→竞相降价→利润归零\n"
            "  - 卡特尔稳定性:欺骗动机→合作瓦解\n"
            "  - 信号博弈:教育作为能力信号(斯宾塞模型)\n"
            "  - 委托-代理:激励机制设计解决道德风险"
        )

    def _analyze_behavioral_econ(self, text: str, ctx: Dict) -> str:
        """行为经济学分析"""
        return (
            "[行为经济学三大核心]\n"
            "1. 有限理性(西蒙):满意化原则替代最优化\n"
            "2. 前景理论(卡尼曼):\n"
            "   - 参照依赖:收益/损失相对于参照点\n"
            "   - 损失厌恶:等量损失的痛苦>等量收益的快乐(λ≈2.5)\n"
            "   - 敏感性递减:离参照点越远,边际变化越小\n"
            "3. 助推理论(泰勒&桑斯坦):\n"
            "   - 默认选项,社会规范,简化decision,承诺机制,及时反馈\n\n"
            "应用:定价锚定,稀缺性暗示,社会证明,框架效应"
        )

    def _analyze_welfare(self, text: str, ctx: Dict) -> str:
        """福利分析"""
        return (
            "[福利经济学分析]\n"
            "帕累托最优:任何改变都不能在不损害他人的情况下使任何人更好\n"
            "福利第一定理:完全竞争均衡→帕累托最优(效率保障)\n"
            "福利第二定理:帕累托最优配置→可通过市场竞争实现(公平+效率)\n\n"
            "市场失灵四类型:\n"
            "  1. 垄断 → P>MC,无谓损失(DWL)\n"
            "  2. 外部性 → 私人成本≠社会成本(庇古税/科斯定理)\n"
            "  3. 公共物品 → 免费搭车问题\n"
            "  4. 信息不对称 → 逆向选择+道德风险\n\n"
            "阿罗不可能定理:不存在满足所有投票人偏好的社会选择机制"
        )

    # ============================================================
    # 社会发展分析
    # ============================================================

    def _social_analysis(self, user_input: str, ctx: Dict) -> SocialDevelopmentInsight:
        """社会发展深度分析"""
        insight = SocialDevelopmentInsight()

        insight.development_stage = self._assess_development_stage(user_input, ctx)
        insight.inequality = self._analyze_inequality(user_input, ctx)
        insight.social_mobility = self._analyze_social_mobility(user_input, ctx)
        insight.modernization_path = self._assess_modernization_path(user_input, ctx)
        insight.risk_assessment = self._assess_social_risks(user_input, ctx)
        insight.policy_suggestion = self._generate_policy_suggestions(user_input, ctx)

        insight.ancient_source = "沃勒斯坦<现代世界体系>+ 森<以自由看待发展>+ 贝克<风险社会>"
        insight.modern_application = "现代化理论→依附论→世界体系→风险社会→数字社会 全谱分析"

        return insight

    def _assess_development_stage(self, text: str, ctx: Dict) -> str:
        """评估发展阶段"""
        return (
            "[罗斯托经济成长六阶段模型]\n"
            "① 传统社会 → 生产力受限,家族纽带\n"
            "② 起飞前提 → 技术引进,制度变革,精英主导\n"
            "③ 起飞 → 工业革命,主导部门,资本积累,10%+增长率\n"
            "④ 成熟 → 技术复杂化,出口升级,福利国家\n"
            "⑤ 大众消费 → 耐用消费品,白领扩大,服务业主导\n"
            "⑥ 追求质量 → 后物质主义,环境质量,生活品质\n\n"
            "替代框架:\n"
            "  - 依附理论:关注结构性依附与去依附路径\n"
            "  - 世界体系:中心/半边缘/边缘的结构位置\n"
            "  - 钱纳里模式:按人均GDPjudge工业化阶段"
        )

    def _analyze_inequality(self, text: str, ctx: Dict) -> str:
        """不平等分析"""
        return (
            "[社会不平等分析框架]\n"
            "度量工具:\n"
            "  - 基尼系数:0=完全平等,1=完全不平等\n"
            "  - 洛伦兹曲线:实际分配 vs 完全平等线\n"
            "  - 皮凯蒂 r>g:资本收益率>经济增长率→不平等自然扩大\n"
            "  - 阿玛蒂亚·森 MPI:多维贫困(健康+教育+生活水平)\n\n"
            "分层理论:\n"
            "  - 马克思:生产资料占有→阶级对立\n"
            "  - 韦伯:阶级(经济)+党派(政治)+身份群体(社会) 三维分层\n"
            "  - 功能主义 vs 冲突论:分层是激励必要 vs 特权固化\n\n"
            "社会排斥五维度:经济/社会/政治/文化/空间"
        )

    def _analyze_social_mobility(self, text: str, ctx: Dict) -> str:
        """社会流动性分析"""
        return (
            "[社会流动机制分析]\n"
            "类型:代际流动(跨代)vs 代内流动(个人生命周期)\n"
            "方向:垂直流动(上/下)vs 水平流动(平移)\n\n"
            "四大流动机制:\n"
            "  1. 人力资本:教育→技能→职业地位\n"
            "  2. 社会资本:社会网络→信息桥接→机会get(普特南/科尔曼)\n"
            "  3. 制度机制:公务员考试/遗产税/教育公平政策\n"
            "  4. 市场机制:劳动力市场结构→职业变迁→产业升级\n\n"
            "社会资本维度:\n"
            "  - 认知型:信任,互惠规范,共同价值观\n"
            "  - 结构型:社会网络,参与渠道,信息网络\n"
            "  - 桥接型(bridging) vs 粘结型(bonding):弱联系带来新机会"
        )

    def _assess_modernization_path(self, text: str, ctx: Dict) -> str:
        """评估现代化路径"""
        return (
            "[现代化路径评估]\n"
            "经典现代化理论(线性路径):\n"
            "  传统→现代,西方模式普适\n\n"
            "依附理论批判:\n"
            "  殖民历史→依附结构→贸易条件恶化→去依附\n"
            "  经典依附论(普雷维什/弗兰克) vs 依附发展论(卡多佐)\n\n"
            "世界体系定位:\n"
            "  中心(技术密集/高工资) | 半边缘(过渡/缓冲) | 边缘(初级产品/低工资)\n\n"
            "后发展理论(多元路径):\n"
            "  - 批判线性发展观\n"
            "  - 福柯:发展作为话语(知识-权力关系)\n"
            "  - 萨义德:东方主义批判\n"
            "  - 米尔斯:社会学想象力(个人困扰↔公共议题)"
        )

    def _assess_social_risks(self, text: str, ctx: Dict) -> str:
        """社会风险评估"""
        return (
            "[风险社会分析框架(贝克)]\n"
            "工业社会 → 风险社会\n"
            "characteristics:\n"
            "  - 人为风险取代自然风险\n"
            "  - 全球性风险(气候/疫情/金融)\n"
            "  - 风险分配不同于财富分配(向下集中)\n"
            "  - 制度反思性增强\n\n"
            "涂尔干失范理论:\n"
            "  快速变迁→规范真空→整合危机\n\n"
            "风险治理范式:\n"
            "  - 预防原则(预防优于补救)\n"
            "  - 韧性思维(系统适应+灾后恢复)\n"
            "  - 参与式治理(利益相关者参与)"
        )

    def _generate_policy_suggestions(self, text: str, ctx: Dict) -> str:
        """generate政策建议"""
        return (
            "[发展政策建议框架]\n"
            "社会metrics体系:\n"
            "  - GDP补充:HDI(健康+教育+收入)+ 幸福指数 + SDGs\n"
            "  - MPI多维贫困:健康/教育/生活水平三维测量\n\n"
            "福利国家三类型(艾斯平-安德森):\n"
            "  - 社会民主主义(北欧):高税收高福利,普遍主义\n"
            "  - 保守主义(德国):俾斯麦模式,职业分层\n"
            "  - 自由主义(美国):市场主导,有限福利\n\n"
            "中国语境:\n"
            "  - 五位一体:经济+政治+文化+社会+生态文明\n"
            "  - 乡村振兴:产业/人才/文化/生态/组织 五个振兴\n"
            "  - 双碳目标:2030碳达峰 + 2060碳中和"
        )

    # ============================================================
    # 跨域fusion分析
    # ============================================================

    def _cross_domain_analysis(self, user_input: str, ctx: Dict) -> SocialScienceAnalysis:
        """跨域fusion分析"""
        marketing = self._marketing_analysis(user_input, ctx)
        economic = self._economic_analysis(user_input, ctx)
        social = self._social_analysis(user_input, ctx)

        synthesis = (
            "[社会科学三维fusion分析]\n\n"
            f"▎营销维度:{marketing.stp_strategy[:80]}...\n"
            f"▎经济维度:{economic.supply_demand[:80]}...\n"
            f"▎社会维度:{social.development_stage[:80]}...\n\n"
            "▎跨域fusion洞察:\n"
            "  1. 营销×经济:弹性分析指导定价strategy;博弈论指导竞争strategy\n"
            "  2. 营销×社会:社会资本增强品牌传播;现代化阶段决定消费升级路径\n"
            "  3. 经济×社会:不平等影响消费结构;风险社会改变需求模式\n"
            "  4. 三维合一:用市场机制实现社会价值,用社会洞察驱动商业创新\n"
        )

        actions = (
            self._extract_marketing_actions(marketing) +
            self._extract_economic_actions(economic) +
            self._extract_social_actions(social) +
            ["建立营销-经济-社会三维分析仪表盘", "定期评估市场结构与社会变迁的交互影响"]
        )

        risks = (
            self._extract_marketing_risks(marketing) +
            self._extract_economic_risks(economic) +
            self._extract_social_risks(social)
        )

        return SocialScienceAnalysis(
            domain=SocialScienceDomain.CROSS_DOMAIN,
            primary_insight=synthesis,
            marketing=marketing,
            economic=economic,
            social=social,
            cross_domain_synthesis=synthesis,
            action_items=actions[:10],
            risk_warnings=risks[:8],
            confidence=0.78
        )

    # ============================================================
    # 辅助方法
    # ============================================================

    def _extract_marketing_actions(self, insight: MarketingInsight) -> List[str]:
        return [
            "完成STP分析,明确1-3个目标细分市场",
            "建立4P/7P营销组合矩阵",
            "搭建CBBE品牌资产四步金字塔",
            "部署AARRR增长漏斗,监控CAC/LTV/NPS",
            "构建RFM客户分群,实施差异化运营"
        ]

    def _extract_marketing_risks(self, insight: MarketingInsight) -> List[str]:
        return [
            "市场定位模糊导致差异化失败",
            "过度依赖单一渠道(渠道风险集中)",
            "品牌延伸损害核心品牌价值",
            "忽视行为经济学偏差导致定价失准"
        ]

    def _extract_economic_actions(self, insight: EconomicInsight) -> List[str]:
        return [
            "评估所在行业的市场结构类型与竞争强度",
            "计算核心产品的需求价格弹性,制定最优定价",
            "recognize信息不对称问题,建立信号机制",
            "评估外部性影响,考虑内部化strategy"
        ]

    def _extract_economic_risks(self, insight: EconomicInsight) -> List[str]:
        return [
            "误判市场结构导致竞争strategy失效",
            "忽视行为偏差假设理性经济人导致预测偏差",
            "外部性未被内部化造成社会福利损失"
        ]

    def _extract_social_actions(self, insight: SocialDevelopmentInsight) -> List[str]:
        return [
            "评估目标市场社会阶层结构与消费分层",
            "recognize社会流动障碍,设计包容性产品strategy",
            "关注数字鸿沟,确保产品可及性",
            "建立社会风险评估机制,预防声誉风险"
        ]

    def _extract_social_risks(self, insight: SocialDevelopmentInsight) -> List[str]:
        return [
            "忽视社会不平等导致市场strategy失效",
            "文化敏感性不足引发品牌危机",
            "风险社会背景下意外事件影响放大"
        ]

    def get_available_domains(self) -> List[str]:
        """返回可用的分析域"""
        return [d.value for d in SocialScienceDomain]

    def get_model_count(self) -> Dict[str, int]:
        """返回各领域模型数量"""
        return {
            "市场营销": len(self._marketing_models),
            "市场经济学": len(self._economic_models),
            "社会发展学": len(self._social_theories),
            "总计": len(self._marketing_models) + len(self._economic_models) + len(self._social_theories)
        }
