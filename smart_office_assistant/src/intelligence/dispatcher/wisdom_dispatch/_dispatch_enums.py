"""
智慧引擎unified调度器 - 枚举与数据结构
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

class WisdomSchool(Enum):
    """智慧学派 V6.0.0"""
    CONFUCIAN = "儒家"
    DAOIST = "道家"
    BUDDHIST = "佛家"
    SUFU = "素书"
    MILITARY = "兵法"
    LVSHI = "吕氏春秋"
    HONGMING = "辜鸿铭"
    METAPHYSICS = "术数时空"
    CIVILIZATION = "文明演化"
    CIV_WAR_ECONOMY = "文明经战"
    SCI_FI = "科幻思维"
    GROWTH = "成长思维"
    MYTHOLOGY = "神话智慧"
    LITERARY = "文学叙事"
    ANTHROPOLOGY = "人类学"
    BEHAVIOR = "行为塑造"
    SCIENCE = "科学思维"
    SOCIAL_SCIENCE = "社会科学"
    YANGMING = "王阳明xinxue"
    DEWEY = "杜威反省思维"
    TOP_METHODS = "顶级思维法"
    NATURAL_SCIENCE = "自然科学"
    CHINESE_CONSUMER = "中国社会消费文化"
    WCC = "WCC智慧演化"
    HISTORICAL_THOUGHT = "历史思想三维度"
    # V6.0 第二阶段新增学派
    PSYCHOLOGY = "心理学"                    # 心理学先驱融合（弗洛伊德/荣格/马斯洛等）
    SYSTEMS = "系统论"                       # 系统论/复杂适应系统
    MANAGEMENT = "管理学"                   # 管理学经典（德鲁克/波特等）
    ZONGHENG = "纵横家"                     # 合纵连横/外交博弈
    MOZI = "墨家"                           # 兼爱非攻/工程技术/逻辑推理
    FAJIA = "法家"                          # 法术势/制度设计/权力治理
    # V6.0 第三阶段新增学派
    ECONOMICS = "经济学"                    # 经济学智慧（亚当斯密/凯恩斯等）
    MINGJIA = "名家"                        # 名家逻辑学（公孙龙/惠施等）
    WUXING = "阴阳家"                       # 阴阳五行学派（邹衍等）
    COMPLEXITY = "复杂性科学"               # 复杂性科学（圣塔菲/复杂适应系统）
    # V6.2 社会科学智慧版新增学派
    SOCIOLOGY = "社会学"                    # 社会学三巨头：涂尔干/韦伯/马克思
    BEHAVIORAL_ECONOMICS = "行为经济学"     # 行为经济学：卡尼曼/塞勒/西奥迪尼
    COMMUNICATION = "传播学"                # 传播学：麦克卢汉/鲍德里亚/哈贝马斯
    CULTURAL_ANTHROPOLOGY = "文化人类学"    # 文化人类学：马林诺夫斯基/列维斯特劳斯/格尔茨
    POLITICAL_ECONOMICS = "政治经济学"       # 政治经济学：李斯特/凯恩斯/哈耶克
    ORGANIZATIONAL_PSYCHOLOGY = "组织心理学" # 组织心理学：阿吉里斯/舍恩/沙因
    SOCIAL_PSYCHOLOGY = "社会心理学"        # 社会心理学：米尔格拉姆/阿希/津巴多

class ProblemType(Enum):
    """问题类型 V6.0.0"""
    # 儒家
    ETHICAL = "伦理道德"
    GOVERNANCE = "组织治理"
    TALENT = "人才选用"
    CULTURE = "文化传承"
    # 道家
    STRATEGY = "战略转型"
    CRISIS = "危机处理"
    CHANGE = "变革管理"
    BALANCE = "阴阳平衡"
    TIMING = "时机judge"
    ENVIRONMENT = "环境布局"
    PATTERN = "结构格局"
    # 佛家
    MINDSET = "心态调适"
    HARMONY = "团队和谐"
    INTEREST = "利益协调"
    LONGTERM = "长期规划"
    # 素书
    LEADERSHIP = "领导decision"
    RISK = "风险管理"
    FORTUNE = "福祸评估"
    PERSONNEL = "人才recognize"
    # 兵法
    COMPETITION = "竞争strategy"
    ATTACK = "市场攻击"
    DEFENSE = "市场防御"
    NEGOTIATION = "谈判博弈"
    WAR_ECONOMY_NEXUS = "经战主链"
    STATE_CAPACITY = "国家能力"
    INSTITUTIONAL_SEDIMENTATION = "制度沉淀"
    # 吕氏春秋
    PUBLIC_INTEREST = "公私抉择"
    SEASONAL = "时令管理"
    YINYANG = "阴阳调和"
    # 科幻思维
    DIMENSION = "维度超越"
    SURVIVAL = "生存法则"
    SCALE = "尺度思维"
    # 成长思维
    GROWTH_MINDSET = "成长突破"
    REVERSE = "逆向思考"
    CLOSED_LOOP = "闭环执行"
    # 神话智慧
    CREATION_MYTH = "创世叙事"
    APOCALYPSE = "灭世危机"
    CYCLICAL = "循环哲学"
    # 文学叙事
    NARRATIVE = "叙事构建"
    RESILIENCE = "韧性评估"
    CHARACTER = "人物分析"
    # 人类学
    CROSS_CULTURE = "跨文化沟通"
    RITUAL = "仪式分析"
    CULTURAL_CHANGE = "文化变迁"
    # 行为塑造
    HABIT = "习惯设计"
    WILLPOWER = "自控力管理"
    NUDGE = "助推设计"
    # 科学思维
    SCIENTIFIC_METHOD = "科学验证"
    SYSTEM_THINKING = "系统分析"
    EVIDENCE = "证据评估"
    # 社会科学
    MARKETING = "营销strategy"
    MARKET_ANALYSIS = "市场分析"
    SOCIAL_DEVELOPMENT = "社会发展"
    # ── v3.2 新增: 营销战略首位 ──
    CONSUMER_MARKETING = "C端营销"
    BRAND_STRATEGY = "品牌战略"
    SOCIAL_STABILITY = "社会稳定"
    PSYCHOLOGICAL_INSIGHT = "心理洞察"
    # 自然科学
    PHYSICS_ANALYSIS = "物理分析"
    LIFE_SCIENCE = "生命科学"
    EARTH_SYSTEM = "地球系统"
    COSMOS_EXPLORATION = "宇宙探索"
    SCALE_CROSSING = "跨尺度思维"
    # WCC智慧演化
    META_PERSPECTIVE = "元视角升维"
    CIVILIZATION_ANALYSIS = "文明诊断"
    COSMIC_COGNITION = "宇宙认知"
    SCALE_TRANSFORMATION = "尺度转换"
    WORLDVIEW_SHIFT = "世界观转换"
    WISDOM_EVOLUTION = "智慧演化"
    TECH_EVOLUTION = "技术进化"
    # 历史思想三维度
    HISTORICAL_ANALYSIS = "历史分析"
    THOUGHT_EVOLUTION = "思想演进"
    ECONOMIC_EVOLUTION = "经济演进"
    TECH_HISTORY = "科技演进"
    CROSS_DIMENSION = "跨维度洞察"
    PARADIGM_SHIFT = "范式转换"
    # ── V6.0 第二阶段新增: 心理学ProblemType ──
    PERSONALITY_ANALYSIS = "人格分析"
    GROUP_DYNAMICS = "群体动力学"
    COGNITIVE_BIAS = "认知偏差识别"
    MOTIVATION_ANALYSIS = "动机分析"
    PSYCHOLOGICAL_ARITHMETIC = "心理运算"
    TRAUMA_HEALING = "心理创伤修复"
    SELF_ACTUALIZATION = "自我实现"
    INTERPERSONAL_RELATIONSHIP = "人际关系处理"
    # ── V6.0 第二阶段新增: 系统论ProblemType ──
    COMPLEX_SYSTEM = "复杂系统建模"
    FEEDBACK_LOOP = "反馈回路设计"
    EMERGENT_BEHAVIOR = "涌现行为预测"
    SYSTEM_EQUILIBRIUM = "系统均衡分析"
    ADAPTIVE_SYSTEM = "自适应系统优化"
    # ── V6.0 第二阶段新增: 管理学ProblemType ──
    STRATEGIC_PLANNING = "战略规划制定"
    ORGANIZATIONAL_DESIGN = "组织架构设计"
    PERFORMANCE_MANAGEMENT = "绩效管理体系"
    KNOWLEDGE_MANAGEMENT = "知识管理体系"
    CHANGE_MANAGEMENT = "变革管理实施"
    INNOVATION_MANAGEMENT = "创新管理推进"
    # ── V6.0 第二阶段新增: 纵横家ProblemType ──
    DIPLOMATIC_NEGOTIATION = "外交谈判策略"
    ALLIANCE_BUILDING = "联盟构建策略"
    POWER_BALANCE = "权力平衡博弈"
    # ── V6.0 第三阶段新增: 墨家ProblemType ──
    ENGINEERING_INNOVATION = "工程技术创新"
    COST_OPTIMIZATION = "成本效率优化"
    UNIVERSAL_BENEFIT = "普惠利益设计"
    DEFENSE_FORTIFICATION = "防御工事设计"
    LOGICAL_DEDUCTION = "逻辑推理论证"
    # ── V6.0 第三阶段新增: 法家ProblemType ──
    INSTITUTIONAL_DESIGN = "制度体系设计"
    LAW_ENFORCEMENT = "法治执行策略"
    POWER_STRUCTURING = "权力架构设计"
    REWARD_PUNISHMENT = "赏罚激励机制"
    HUMAN_NATURE_ANALYSIS = "人性利害分析"
    STATE_CONSOLIDATION = "国家集权巩固"
    # ── V6.0 第三阶段新增: 经济学ProblemType ──
    RESOURCE_ALLOCATION = "资源配置优化"
    SUPPLY_DEMAND_BALANCE = "供需平衡分析"
    ECONOMIC_INCENTIVE = "经济激励机制设计"
    MARKET_EFFICIENCY = "市场效率评估"
    INVESTMENT_DECISION = "投资决策分析"
    # ── V6.0 第三阶段新增: 名家ProblemType ──
    LOGICAL_PARADOX = "逻辑悖论分析"
    CLASSIFICATION_REFINEMENT = "名实关系辨析"
    DIALECTICAL_REASONING = "辩证推理应用"
    # ── V6.0 第三阶段新增: 阴阳家ProblemType ──
    WUXING_ANALYSIS = "五行生克分析"
    YINYANG_DIALECTICS = "阴阳辩证思维"
    SEASONAL_RHYTHM = "时节节律运用"
    COSMIC_HARMONY = "天人合一境界"
    CYCLICAL_TRANSFORMATION = "循环转化规律"
    # ── V6.0 第三阶段新增: 复杂性科学ProblemType ──
    EMERGENT_ORDER = "涌现秩序识别"
    NETWORK_DYNAMICS = "网络动力学分析"
    ADAPTIVE_EVOLUTION = "自适应演化预测"
    # ── V6.0 精细优化: 学派子领域细分ProblemType ──
    CONFUCIAN_SUB_SCHOOL = "儒家子学派应用"
    DAOIST_SUB_SCHOOL = "道家子学派应用"
    BUDDHIST_SUB_SCHOOL = "佛家子学派应用"
    MILITARY_SUB_SCHOOL = "兵法子学派应用"
    TALENT_PIPELINE = "人才梯队建设"
    ORGANIZATIONAL_CULTURE = "组织文化塑造"
    BRAND_CULTURE = "品牌文化构建"
    PHILOSOPHY_OF_MIND = "心学实践应用"
    DECISION_FRAMEWORK = "决策框架构建"
    RESOURCE_ECOLOGY = "资源生态分析"
    INNOVATION_ECOLOGY = "创新生态分析"
    # ── V6.2 社会科学智慧版ProblemType ──
    # 社会学
    SOCIAL_STRUCTURE_ANALYSIS = "社会结构分析"
    CLASS_MOBILITY = "阶层流动性分析"
    INSTITUTIONAL_SOCIOLOGY = "制度社会学分析"
    SOCIAL_STRATIFICATION = "社会分层分析"
    COLLECTIVE_ACTION = "集体行动分析"
    # 行为经济学
    COGNITIVE_BIAS_V62 = "认知偏差识别"
    DECISION_MAKING_BEHAVIOR = "决策行为分析"
    MARKET_BEHAVIOR = "市场行为预测"
    INCENTIVE_DESIGN = "激励设计分析"
    NUDGE_POLICY = "助推政策设计"
    # 传播学
    MEDIA_EFFECT = "媒介效果分析"
    PUBLIC_OPINION_FORMATION = "舆论形成分析"
    INFORMATION_CASCADE = "信息级联效应"
    DISCOURSE_ANALYSIS = "话语分析"
    INTERPERSONAL_COMMUNICATION = "人际传播分析"
    # 文化人类学
    CULTURAL_PATTERN_RECOGNITION = "文化模式识别"
    SYMBOL_SYSTEM_ANALYSIS = "符号系统分析"
    RITUAL_CONTEXT_ANALYSIS = "仪式语境分析"
    CROSS_CULTURAL_ADAPTATION = "跨文化适应分析"
    # 政治经济学
    INSTITUTIONAL_POLITICAL_ANALYSIS = "制度政治分析"
    POLICY_GAME_THEORY = "政策博弈分析"
    MARKET_REGULATION_ANALYSIS = "市场监管分析"
    PUBLIC_CHOICE = "公共选择分析"
    # 组织心理学
    ORGANIZATIONAL_CHANGE_V62 = "组织变革分析"
    LEADERSHIP_STYLE_ANALYSIS = "领导风格分析"
    TEAM_COHESION_ANALYSIS = "团队凝聚力分析"
    ORGANIZATIONAL_CULTURE_V62 = "组织文化诊断"
    # 社会心理学
    CONFORMITY_BEHAVIOR = "从众行为分析"
    AUTHORITY_OBEDIENCE = "权威服从分析"
    SOCIAL_INFLUENCE_MECHANISM = "社会影响机制"
    GROUP_THINK_ANALYSIS = "群体思维分析"

class SubSchool(Enum):
    """子学派枚举 V6.0.1 - 学派细分体系"""
    # 儒家4子学派
    MENCIUS = "孟学"
    XUNZI = "荀学"
    NEO_CONFUCIAN = "宋明理学"
    CLASSICAL = "经学"
    # 道家3子学派
    LAOZI = "老学"
    ZHUANGZI = "庄学"
    LIEZI = "列子"
    # 佛家4子学派
    CHAN = "禅宗"
    TIANTAI = "天台宗"
    HUAYAN = "华严宗"
    PURELAND = "净土宗"
    # 兵法3子学派
    SUNZI = "孙子兵法"
    WUZI = "吴子兵法"
    LIUTAO = "六韬"


SUBSCHOOL_PARENT: Dict[SubSchool, WisdomSchool] = {
    # 儒家
    SubSchool.MENCIUS: WisdomSchool.CONFUCIAN,
    SubSchool.XUNZI: WisdomSchool.CONFUCIAN,
    SubSchool.NEO_CONFUCIAN: WisdomSchool.CONFUCIAN,
    SubSchool.CLASSICAL: WisdomSchool.CONFUCIAN,
    # 道家
    SubSchool.LAOZI: WisdomSchool.DAOIST,
    SubSchool.ZHUANGZI: WisdomSchool.DAOIST,
    SubSchool.LIEZI: WisdomSchool.DAOIST,
    # 佛家
    SubSchool.CHAN: WisdomSchool.BUDDHIST,
    SubSchool.TIANTAI: WisdomSchool.BUDDHIST,
    SubSchool.HUAYAN: WisdomSchool.BUDDHIST,
    SubSchool.PURELAND: WisdomSchool.BUDDHIST,
    # 兵法
    SubSchool.SUNZI: WisdomSchool.MILITARY,
    SubSchool.WUZI: WisdomSchool.MILITARY,
    SubSchool.LIUTAO: WisdomSchool.MILITARY,
}


@dataclass
class WisdomRecommendation:
    """智慧推荐"""
    school: WisdomSchool
    confidence: float
    primary_method: str
    reasoning: str
    advice: str
    ancient_source: str
    modern_application: str

@dataclass
class FusionDecision:
    """FusionDecision结果 V7.0.0 - 神之架构V4部门调度"""
    timestamp: datetime
    problem_type: ProblemType
    primary_school: WisdomSchool
    secondary_schools: List[WisdomSchool]
    # ── v2.1.0 部门调度字段 ──
    dispatch_department: Optional[str] = None          # 主调度部门名
    dispatch_departments: List[str] = field(default_factory=list)  # 所有参与部门
    department_routing: str = ""                        # 部门路由说明
    # ── 学派输入（v6.1合并：25学派统一为dict，key=WisdomSchool.value） ──
    school_inputs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    # ── 决策输出 ──
    final_decision: str = ""
    reasoning_chain: List[str] = field(default_factory=list)
    risk_warnings: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    overall_score: float = 0.0
    ethics_score: float = 0.0
    wisdom_score: float = 0.0
    strategy_score: float = 0.0
    growth_score: float = 0.0
