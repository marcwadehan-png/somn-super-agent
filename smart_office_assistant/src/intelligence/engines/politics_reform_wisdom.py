"""
__all__ = [
    'get_political_reform_wisdom',
    'query_reformer_by_problem',
    'get_reform_strategy',
    'assess_governance_capacity',
    'get_cadres_management_wisdom',
    'get_fiscal_reform_guidance',
    'analyze_reform_risk',
]

政治改革家智慧核心模块 v1.0
Political Reformers Wisdom Core Module

中国古代~90位政治改革家和帝王的智慧蒸馏
涵盖：先秦(11人)、秦汉(16人)、三国两晋(5人)、唐代(11人)、宋代(9人)、明代(9人)、晚清(4人)、帝王篇(14人)

核心贡献:
- 治理能力(Governance): 制度改革与国家管理
- 变法魄力(Reform Courage): 推动变革的决心
- 民本意识(People-Centered): 以民为本的思想
- 组织管理(Organization): 人事与制度管理
- 危机应对(Crisis Response): 应对突发情况
- 外交智慧(Diplomatic): 外交与联盟策略

版本: v1.0
更新: 2026-04-10
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

# 懒加载改革策略数据
from ._reformers_data import get_strategy_data

class ReformEra(Enum):
    """改革时代分类"""
    PRE_QIN = "先秦"           # 前11世纪-前221
    QIN_HAN = "秦汉"           # 前221-220
    THREE_KINGDOMS = "三国两晋"  # 220-420
    TANG = "唐代"              # 618-907
    SONG = "宋代"              # 960-1279
    MING = "明代"              # 1368-1644
    LATE_QING = "晚清"         # 1840-1912
    EMPEROR = "帝王篇"         # 帝王

class ReformDomain(Enum):
    """改革领域分类"""
    ADMIN = "行政改革"           # 官制、组织管理
    FISCAL = "财政改革"         # 税收、盐铁、货币
    LEGAL = "法治改革"           # 法律、制度
    LAND = "土地改革"           # 均田、限田
    MILITARY = "军事改革"        # 兵制、练兵
    DIPLOMATIC = "外交改革"      # 和亲、联盟
    CULTURAL = "文化改革"        # 儒术、科举
    PERSONNEL = "人事改革"       # 人才、选拔

class ProblemType(Enum):
    """问题类型"""
    REFORM_PUSH = "推进改革"      # 如何推动改革
    CADRES_MGMT = "干部管理"      # 官吏选拔考核
    FISCAL_POLICY = "财政政策"    # 税收理财
    CRISIS_RESPONSE = "危机应对"    # 处理突发事件
    DIPLOMATIC = "外交策略"      # 联盟与博弈
    STABILITY = "社会稳定"        # 维稳与民生
    CENTRALIZATION = "中央集权"   # 权力集中
    LEGAL = "法治改革"           # 法律制度建设

@dataclass
class ReformerProfile:
    """改革家档案"""
    name: str                    # 姓名
    era: str                     # 年代
    dynasty: str                 # 朝代
    title: str                   # 官职
    historical_status: str       # 历史地位
    
    # 核心思想体系
    core_thoughts: List[str]     # 核心思想列表
    reform_achievements: List[str]  # 改革成就
    
    # 智慧蒸馏
    wisdom_distillation: List[str]  # 提炼的智慧法则
    
    # 六大能力维度(1-10分)
    governance: int = 0          # 治理能力
    reform_courage: int = 0       # 变法魄力
    people_centered: int = 0     # 民本意识
    organization: int = 0        # 组织管理
    crisis_response: int = 0     # 危机应对
    diplomatic: int = 0          # 外交智慧
    
    # 专业领域
    domains: List[ReformDomain] = field(default_factory=list)
    
    # 适用问题类型
    applicable_problems: List[ProblemType] = field(default_factory=list)
    
    # 代表名言
    quote: str = ""
    quote_source: str = ""

@dataclass
class ReformStrategy:
    """改革策略"""
    strategy_name: str           # 策略名称
    source_sages: List[str]      # 来源人物
    reasoning: str               # 推理过程
    action_plan: List[str]       # 行动计划
    risk_factors: List[str]      # 风险因素
    expected_outcome: str         # 预期结果
    historical_cases: List[str]  # 历史案例

class PoliticalReformWisdomCore:
    """
    政治改革家智慧核心引擎
    
    从~90位中国古代政治改革家和帝王中提炼智慧
    提供: 改革策略、干部管理、财政改革、危机应对、外交博弈等智慧
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self._reformers = self._init_reformers()
        self._strategy_map = self._init_strategy_map()
    
    def _init_reformers(self) -> Dict[str, ReformerProfile]:
        """初始化改革家数据库"""
        return {
            # ==================== 先秦改革家(11人) ====================
            "管仲": ReformerProfile(
                name="管仲", era="前645年", dynasty="春秋·齐国", title="齐国相国",
                historical_status="春秋五霸之首的奠基者，中国古代改革变法的先驱",
                core_thoughts=[
                    "相地而衰征", "官山海", "以法治国", 
                    "通货积财", "尊王攘夷"
                ],
                reform_achievements=[
                    "行政改革(建立县制)", "经济改革(盐铁官营)",
                    "军事改革(寓兵于农)", "外交改革(尊王攘夷)"
                ],
                wisdom_distillation=[
                    "以法治国是现代治理的基石",
                    "相地衰征是因地制宜的体现",
                    "通货积财是经济发展优先的思维",
                    "尊王攘夷是大局观的表达",
                    "寓兵于农是资源整合的智慧"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=10, crisis_response=10, diplomatic=10,
                domains=[ReformDomain.ADMIN, ReformDomain.FISCAL, ReformDomain.MILITARY, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.FISCAL_POLICY, ProblemType.DIPLOMATIC],
                quote="仓廪实而知礼节，衣食足而知荣辱",
                quote_source="管仲"
            ),
            "晏婴": ReformerProfile(
                name="晏婴", era="前500年", dynasty="春秋·齐国", title="齐国名相",
                historical_status="以廉洁勤政著称",
                core_thoughts=["廉政爱民", "节俭治国", "以和为贵", "诤臣敢言"],
                reform_achievements=["推动齐国廉政建设", "促进外交和平"],
                wisdom_distillation=[
                    "廉政爱民是政治伦理的核心",
                    "节俭治国是财政智慧",
                    "诤臣敢言是谏言文化的体现",
                    "和而不同是处理关系的智慧"
                ],
                governance=9, reform_courage=7, people_centered=10,
                organization=8, crisis_response=9, diplomatic=10,
                domains=[ReformDomain.ADMIN, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.CADRES_MGMT, ProblemType.DIPLOMATIC],
                quote="智者千虑，必有一失；愚者千虑，必有一得",
                quote_source="晏婴"
            ),
            "子产": ReformerProfile(
                name="子产", era="前522年", dynasty="春秋·郑国", title="郑国名相",
                historical_status="子产改革的开创者",
                core_thoughts=["宽猛相济", "作封洫", "作丘赋", "铸刑书"],
                reform_achievements=[
                    "经济改革(均田定赋)", "政治改革(公布成文法)",
                    "军事改革(丘赋制度)"
                ],
                wisdom_distillation=[
                    "宽猛相济是治国艺术的体现",
                    "作封洫是土地改革的先河",
                    "铸刑书是法治公开的鼻祖",
                    "改革需要勇气和智慧并存"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=9, crisis_response=9, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.LEGAL, ReformDomain.LAND],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.LEGAL],
                quote="苟利社稷，死生以之",
                quote_source="子产"
            ),
            "百里奚": ReformerProfile(
                name="百里奚", era="前621年", dynasty="春秋·秦国", title="秦国名相",
                historical_status="帮助秦穆公称霸",
                core_thoughts=["任贤使能", "教化为本", "德政为先"],
                reform_achievements=["推动秦国人才制度改革", "促进经济发展"],
                wisdom_distillation=[
                    "任贤使能是人才治国的核心",
                    "教化为本是长远治理的思维",
                    "德政是先感化后管理的智慧"
                ],
                governance=9, reform_courage=8, people_centered=8,
                organization=10, crisis_response=8, diplomatic=9,
                domains=[ReformDomain.ADMIN, ReformDomain.PERSONNEL],
                applicable_problems=[ProblemType.CADRES_MGMT],
                quote=""
            ),
            "范蠡": ReformerProfile(
                name="范蠡", era="前536-前448年", dynasty="春秋·越国", title="越王勾践谋臣",
                historical_status="功成身退的典范",
                core_thoughts=["功成身退", "知止不殆", "计然之策", "顺势而为"],
                reform_achievements=["辅佐勾践灭吴", "后经商致富"],
                wisdom_distillation=[
                    "功成身退是自我保护智慧的极致",
                    "知止不殆是知道边界的智慧",
                    "计然之策是经济智慧的经典",
                    "顺势而为是适应变化的思维"
                ],
                governance=10, reform_courage=9, people_centered=8,
                organization=10, crisis_response=10, diplomatic=10,
                domains=[ReformDomain.ADMIN, ReformDomain.FISCAL, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.CRISIS_RESPONSE, ProblemType.DIPLOMATIC],
                quote="飞鸟尽，良弓藏；狡兔死，走狗烹",
                quote_source="范蠡"
            ),
            "吕不韦": ReformerProfile(
                name="吕不韦", era="前235年", dynasty="战国·卫国", title="秦国相国",
                historical_status="主持编纂《吕氏春秋》",
                core_thoughts=["奇货可居", "杂家思想", "编纂春秋"],
                reform_achievements=["辅佐异人(秦庄襄王)", "推动秦国文化发展"],
                wisdom_distillation=[
                    "奇货可居是投资思维的体现",
                    "杂家思想是整合思维的表达",
                    "编纂春秋是文化积累的伟业"
                ],
                governance=9, reform_courage=8, people_centered=7,
                organization=9, crisis_response=8, diplomatic=10,
                domains=[ReformDomain.ADMIN, ReformDomain.CULTURAL],
                applicable_problems=[ProblemType.REFORM_PUSH],
                quote="言之凿凿，百不失一",
                quote_source="吕不韦"
            ),
            # ==================== 秦汉改革家 ====================
            "萧何": ReformerProfile(
                name="萧何", era="前193年", dynasty="西汉", title="汉初三杰·丞相",
                historical_status="西汉开国丞相",
                core_thoughts=["约法三章", "镇国家抚百姓", "收秦图籍"],
                reform_achievements=["制定汉朝法律制度", "推荐韩信"],
                wisdom_distillation=[
                    "约法三章是简约治理的智慧",
                    "收秦图籍是保护知识资源的远见",
                    "镇国家抚百姓是稳定优先的思维"
                ],
                governance=10, reform_courage=9, people_centered=9,
                organization=10, crisis_response=9, diplomatic=7,
                domains=[ReformDomain.ADMIN, ReformDomain.LEGAL],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.STABILITY],
                quote="非刘氏而王，天下共击之",
                quote_source="萧何"
            ),
            "曹参": ReformerProfile(
                name="曹参", era="前190年", dynasty="西汉", title="西汉丞相",
                historical_status="萧何之后的丞相",
                core_thoughts=["萧规曹随", "清静无为", "与民休息"],
                reform_achievements=["延续萧何政策", "促进社会稳定"],
                wisdom_distillation=[
                    "萧规曹随是制度延续的智慧",
                    "清静无为是避免过度干预的思维",
                    "与民休息是恢复期治理的正确选择"
                ],
                governance=9, reform_courage=5, people_centered=10,
                organization=9, crisis_response=8, diplomatic=7,
                domains=[ReformDomain.ADMIN],
                applicable_problems=[ProblemType.STABILITY],
                quote="载其清静，民以宁一",
                quote_source="曹参"
            ),
            "张良": ReformerProfile(
                name="张良", era="前186年", dynasty="西汉", title="汉初三杰·谋臣",
                historical_status="西汉开国谋臣",
                core_thoughts=["运筹帷幄", "以柔克刚", "功成身退"],
                reform_achievements=["辅佐刘邦建立汉朝", "制定战略"],
                wisdom_distillation=[
                    "运筹帷幄是战略规划能力的体现",
                    "以柔克刚是柔性策略的智慧",
                    "功成身退是自我保全的方法"
                ],
                governance=10, reform_courage=7, people_centered=8,
                organization=9, crisis_response=10, diplomatic=10,
                domains=[ReformDomain.DIPLOMATIC, ReformDomain.MILITARY],
                applicable_problems=[ProblemType.CRISIS_RESPONSE, ProblemType.DIPLOMATIC],
                quote="运筹策于帷帐之中，决胜于千里之外",
                quote_source="张良"
            ),
            "贾谊": ReformerProfile(
                name="贾谊", era="前168年", dynasty="西汉", title="西汉政论家",
                historical_status="西汉初期著名政论家，改革先驱",
                core_thoughts=["过秦论", "削弱藩王", "重农抑商", "改正朔易服色"],
                reform_achievements=["提出削弱诸侯、改革制度的建议"],
                wisdom_distillation=[
                    "过秦论是以史为鉴的典范",
                    "揭示了得民心者得天下",
                    "削弱藩王是中央集权的关键"
                ],
                governance=8, reform_courage=10, people_centered=9,
                organization=7, crisis_response=8, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.MILITARY],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.CENTRALIZATION],
                quote="前事不忘，后事之师",
                quote_source="贾谊"
            ),
            "晁错": ReformerProfile(
                name="晁错", era="前154年", dynasty="西汉", title="御史大夫",
                historical_status="削藩策提出者",
                core_thoughts=["削藩策", "移民实边", "重农贵粟", "更改法令"],
                reform_achievements=["推行削藩策", "引起七国之乱"],
                wisdom_distillation=[
                    "削藩策是中央集权的必然选择",
                    "改革需要时机和策略",
                    "移民实边是边疆战略的智慧",
                    "以身殉道是改革者的悲剧"
                ],
                governance=9, reform_courage=10, people_centered=8,
                organization=8, crisis_response=7, diplomatic=7,
                domains=[ReformDomain.ADMIN, ReformDomain.FISCAL, ReformDomain.MILITARY],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.CENTRALIZATION],
                quote="粟者，王者大用，政之本务",
                quote_source="晁错"
            ),
            "霍光": ReformerProfile(
                name="霍光", era="前68年", dynasty="西汉", title="大司马大将军",
                historical_status="汉昭帝辅政大臣，废立皇帝",
                core_thoughts=["辅政摄政", "拥立宣帝"],
                reform_achievements=["辅政期间延续昭帝政策", "推进盐铁官营"],
                wisdom_distillation=[
                    "辅政摄政是过渡期治理的智慧",
                    "权力集中需要监督机制",
                    "拥立明君是长远考虑"
                ],
                governance=9, reform_courage=8, people_centered=7,
                organization=10, crisis_response=9, diplomatic=7,
                domains=[ReformDomain.ADMIN],
                applicable_problems=[ProblemType.STABILITY, ProblemType.CRISIS_RESPONSE],
                quote=""
            ),
            "魏相": ReformerProfile(
                name="魏相", era="前59年", dynasty="西汉", title="西汉名相",
                historical_status="以直言敢谏著称",
                core_thoughts=["直言极谏", "整饬吏治", "抑兼并"],
                reform_achievements=["整饬吏治", "减轻百姓负担"],
                wisdom_distillation=[
                    "直言极谏是谏臣精神的体现",
                    "抑兼并是维护社会公平的改革",
                    "整饬吏治是廉政建设的基础"
                ],
                governance=9, reform_courage=8, people_centered=10,
                organization=9, crisis_response=8, diplomatic=7,
                domains=[ReformDomain.ADMIN, ReformDomain.PERSONNEL],
                applicable_problems=[ProblemType.CADRES_MGMT],
                quote=""
            ),
            "汲黯": ReformerProfile(
                name="汲黯", era="前112年", dynasty="西汉", title="淮南王相",
                historical_status="以直言敢谏著称",
                core_thoughts=["直言极谏", "清静无为", "内不讳"],
                reform_achievements=["直言批评朝政弊端"],
                wisdom_distillation=[
                    "直言极谏是谏臣精神的最高体现",
                    "清静无为是道家治理智慧",
                    "内不讳需要君主的包容"
                ],
                governance=8, reform_courage=8, people_centered=10,
                organization=7, crisis_response=7, diplomatic=7,
                domains=[ReformDomain.ADMIN],
                applicable_problems=[ProblemType.CADRES_MGMT],
                quote=""
            ),
            # ==================== 三国两晋改革家 ====================
            "诸葛亮": ReformerProfile(
                name="诸葛亮", era="181-234年", dynasty="蜀汉", title="蜀汉丞相",
                historical_status="中国历史上最著名的政治家、军事家",
                core_thoughts=["隆中对", "依法治蜀", "安居平五路", "北伐中原"],
                reform_achievements=["治蜀成就斐然", "推行法治", "整顿吏治", "发展经济"],
                wisdom_distillation=[
                    "隆中对是战略规划的典范",
                    "依法治蜀是法治精神的体现",
                    "鞠躬尽瘁是责任感的最高表达",
                    "知其不可而为之是使命感的体现"
                ],
                governance=10, reform_courage=10, people_centered=10,
                organization=10, crisis_response=10, diplomatic=10,
                domains=[ReformDomain.ADMIN, ReformDomain.LEGAL, ReformDomain.MILITARY, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.CRISIS_RESPONSE, ProblemType.DIPLOMATIC, ProblemType.CADRES_MGMT],
                quote="鞠躬尽瘁，死而后已",
                quote_source="诸葛亮"
            ),
            "谢安": ReformerProfile(
                name="谢安", era="320-385年", dynasty="东晋", title="东晋名相",
                historical_status="淝水之战的决策者",
                core_thoughts=["镇以和简", "淝水之战", "东山再起"],
                reform_achievements=["稳定东晋政权", "取得淝水之战胜利"],
                wisdom_distillation=[
                    "镇以和简是稳定时期治理的智慧",
                    "淝水之战是危机决策的典范",
                    "东山再起是蛰伏与爆发的智慧"
                ],
                governance=10, reform_courage=8, people_centered=9,
                organization=10, crisis_response=10, diplomatic=9,
                domains=[ReformDomain.ADMIN, ReformDomain.MILITARY],
                applicable_problems=[ProblemType.CRISIS_RESPONSE],
                quote=""
            ),
            "苏绰": ReformerProfile(
                name="苏绰", era="498-546年", dynasty="西魏", title="度支尚书",
                historical_status="六条诏书的制定者",
                core_thoughts=["六条诏书", "官制改革", "均田制"],
                reform_achievements=["制定六条诏书", "推进西魏改革"],
                wisdom_distillation=[
                    "六条诏书是系统性改革的纲领",
                    "官制改革是组织优化的关键",
                    "均田制是土地改革的先河"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=10, crisis_response=9, diplomatic=7,
                domains=[ReformDomain.ADMIN, ReformDomain.LAND, ReformDomain.FISCAL],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.FISCAL_POLICY],
                quote=""
            ),
            # ==================== 唐代改革家 ====================
            "房玄龄": ReformerProfile(
                name="房玄龄", era="579-648年", dynasty="唐代", title="尚书左仆射",
                historical_status="唐太宗重要辅臣，凌烟阁二十四功臣之首",
                core_thoughts=["辅佐太宗", "善于用人", "综务式法"],
                reform_achievements=["辅佐太宗制定典章制度"],
                wisdom_distillation=[
                    "善于用人是领导力的核心",
                    "综务式法是高效行政的方法",
                    "辅佐太宗是君臣配合的典范"
                ],
                governance=10, reform_courage=8, people_centered=9,
                organization=10, crisis_response=9, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.PERSONNEL],
                applicable_problems=[ProblemType.CADRES_MGMT],
                quote="孜孜奉国，知无不为",
                quote_source="房玄龄"
            ),
            "杜如晦": ReformerProfile(
                name="杜如晦", era="585-630年", dynasty="唐代", title="尚书右仆射",
                historical_status="与房玄龄并称房杜",
                core_thoughts=["房谋杜断", "决断如流", "运筹帷幄"],
                reform_achievements=["辅佐太宗，参与贞观之治"],
                wisdom_distillation=[
                    "房谋杜断是分工协作的典范",
                    "决断如流是决策效率的体现",
                    "运筹帷幄是战略能力的表达"
                ],
                governance=10, reform_courage=7, people_centered=8,
                organization=9, crisis_response=10, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.CRISIS_RESPONSE],
                quote=""
            ),
            "魏征": ReformerProfile(
                name="魏征", era="580-643年", dynasty="唐代", title="郑公·谏议大夫",
                historical_status="以直言敢谏著称",
                core_thoughts=["直言极谏", "兼听则明", "以史为鉴", "水能载舟亦能覆舟"],
                reform_achievements=["以谏言影响太宗决策", "促进贞观之治"],
                wisdom_distillation=[
                    "直言极谏是谏臣精神的最高体现",
                    "兼听则明是避免偏见的智慧",
                    "水能载舟是民本思想的经典表达",
                    "以史为鉴是学习历史的方法"
                ],
                governance=9, reform_courage=9, people_centered=10,
                organization=8, crisis_response=9, diplomatic=8,
                domains=[ReformDomain.ADMIN],
                applicable_problems=[ProblemType.CADRES_MGMT],
                quote="兼听则明，偏信则暗",
                quote_source="魏征"
            ),
            "狄仁杰": ReformerProfile(
                name="狄仁杰", era="630-700年", dynasty="武周", title="凤阁鸾台平章事",
                historical_status="武周时期名相，杰出政治家",
                core_thoughts=["仁者无敌", "断案如神", "举贤任能", "维护李唐"],
                reform_achievements=["辅佐武则天治理天下", "推荐多位贤才"],
                wisdom_distillation=[
                    "仁者无敌是仁政的信念",
                    "断案如神是专业能力的体现",
                    "举贤任能是人才政治的智慧",
                    "维护李唐是长远战略的考量"
                ],
                governance=10, reform_courage=8, people_centered=10,
                organization=9, crisis_response=10, diplomatic=9,
                domains=[ReformDomain.ADMIN, ReformDomain.PERSONNEL, ReformDomain.LEGAL],
                applicable_problems=[ProblemType.CRISIS_RESPONSE, ProblemType.CADRES_MGMT],
                quote="庙堂之上，朽木为官；殿陛之间，禽兽食禄",
                quote_source="狄仁杰"
            ),
            "姚崇": ReformerProfile(
                name="姚崇", era="650-721年", dynasty="唐代", title="紫微令·宰相",
                historical_status="辅佐玄宗开创开元盛世",
                core_thoughts=["十事要说", "灭蝗救灾", "推行法治", "整饬吏治"],
                reform_achievements=["辅佐玄宗进行政治改革"],
                wisdom_distillation=[
                    "十事要是系统性改革的纲领",
                    "灭蝗救灾是务实应对危机的体现",
                    "整饬吏治是廉政建设的基础"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=10, crisis_response=10, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.LEGAL, ReformDomain.PERSONNEL],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.CRISIS_RESPONSE, ProblemType.CADRES_MGMT],
                quote=""
            ),
            "宋璟": ReformerProfile(
                name="宋璟", era="663-737年", dynasty="唐代", title="宰相",
                historical_status="与姚崇并称姚宋",
                core_thoughts=["守法持正", "整顿吏治", "革除弊政", "以身作则"],
                reform_achievements=["延续姚崇改革", "稳定政局"],
                wisdom_distillation=[
                    "守法持正是法治精神的体现",
                    "整顿吏治是干部管理的关键",
                    "革除弊政是持续改进的思维",
                    "以身作则是领导力的基础"
                ],
                governance=10, reform_courage=9, people_centered=9,
                organization=10, crisis_response=9, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.PERSONNEL],
                applicable_problems=[ProblemType.CADRES_MGMT],
                quote=""
            ),
            "刘晏": ReformerProfile(
                name="刘晏", era="715-780年", dynasty="唐代", title="吏部尚书",
                historical_status="唐代著名理财家",
                core_thoughts=["理财改革", "榷盐法", "常平法", "以简驭繁"],
                reform_achievements=["改革唐代财政制度", "增加国家收入"],
                wisdom_distillation=[
                    "理财改革是经济管理能力的体现",
                    "榷盐法是政府干预经济的典型",
                    "常平法是价格稳定机制的先河",
                    "以简驭繁是化繁为简的智慧"
                ],
                governance=10, reform_courage=10, people_centered=8,
                organization=9, crisis_response=9, diplomatic=7,
                domains=[ReformDomain.FISCAL],
                applicable_problems=[ProblemType.FISCAL_POLICY],
                quote=""
            ),
            "杨炎": ReformerProfile(
                name="杨炎", era="727-781年", dynasty="唐代", title="门下侍郎",
                historical_status="创行两税法",
                core_thoughts=["两税法", "量出制入", "简化税制"],
                reform_achievements=["推行两税法", "改革唐代税收制度"],
                wisdom_distillation=[
                    "两税法是税收制度史上的重大改革",
                    "量出制入是财政管理方法的创新",
                    "简化税制是便民利民的体现"
                ],
                governance=9, reform_courage=10, people_centered=8,
                organization=9, crisis_response=8, diplomatic=7,
                domains=[ReformDomain.FISCAL],
                applicable_problems=[ProblemType.FISCAL_POLICY],
                quote=""
            ),
            # ==================== 宋代改革家 ====================
            "包拯": ReformerProfile(
                name="包拯", era="999-1061年", dynasty="北宋", title="枢密副使",
                historical_status="包青天的原型",
                core_thoughts=["清正廉洁", "执法如山", "为民请命", "刚正不阿"],
                reform_achievements=["整顿吏治", "打击贪腐"],
                wisdom_distillation=[
                    "清正廉洁是政治伦理的底线",
                    "执法如山是法治精神的体现",
                    "为民请命是民本思想的实践",
                    "刚正不阿是人格独立的表达"
                ],
                governance=9, reform_courage=9, people_centered=10,
                organization=9, crisis_response=8, diplomatic=7,
                domains=[ReformDomain.ADMIN, ReformDomain.LEGAL],
                applicable_problems=[ProblemType.CADRES_MGMT, ProblemType.LEGAL],
                quote="廉者，民之表也；贪者，民之贼也",
                quote_source="包拯"
            ),
            "寇准": ReformerProfile(
                name="寇准", era="961-1023年", dynasty="北宋", title="宰相",
                historical_status="抗辽功臣",
                core_thoughts=["抗辽守土", "力主抵抗", "直言极谏", "澶渊之盟"],
                reform_achievements=["促成澶渊之盟", "稳定宋辽关系"],
                wisdom_distillation=[
                    "抗辽守土是民族气节的体现",
                    "力主抵抗是战略定力的表达",
                    "澶渊之盟是务实外交的选择"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=9, crisis_response=10, diplomatic=10,
                domains=[ReformDomain.MILITARY, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.CRISIS_RESPONSE, ProblemType.DIPLOMATIC],
                quote="主忧臣辱，主辱臣死",
                quote_source="寇准"
            ),
            "王安石": ReformerProfile(
                name="王安石", era="1021-1086年", dynasty="北宋", title="参知政事",
                historical_status="主持熙宁变法",
                core_thoughts=[
                    "天变不足畏", "祖宗不足法", "人言不足恤",
                    "青苗法", "募役法", "农田水利法", "市易法", "方田均税法"
                ],
                reform_achievements=["主持熙宁变法", "进行全面改革"],
                wisdom_distillation=[
                    "天变不足畏是理性主义的态度",
                    "祖宗不足法是改革精神的体现",
                    "人言不足恤是坚定改革的意志",
                    "新法体系是系统性改革的典范"
                ],
                governance=10, reform_courage=10, people_centered=8,
                organization=10, crisis_response=8, diplomatic=7,
                domains=[ReformDomain.ADMIN, ReformDomain.FISCAL, ReformDomain.LAND, ReformDomain.LEGAL],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.FISCAL_POLICY, ProblemType.LEGAL],
                quote="天变不足畏，祖宗不足法，人言不足恤",
                quote_source="王安石"
            ),
            "虞允文": ReformerProfile(
                name="虞允文", era="1110-1174年", dynasty="南宋", title="督视江淮军马",
                historical_status="采石之战大捷",
                core_thoughts=["文臣知兵", "以少胜多", "激励士气", "保卫长江"],
                reform_achievements=["指挥采石之战", "击退金军"],
                wisdom_distillation=[
                    "文臣知兵是通才领导的体现",
                    "以少胜多是危机应对的典范",
                    "激励士气是领导力的核心"
                ],
                governance=9, reform_courage=10, people_centered=9,
                organization=9, crisis_response=10, diplomatic=8,
                domains=[ReformDomain.MILITARY],
                applicable_problems=[ProblemType.CRISIS_RESPONSE],
                quote=""
            ),
            # ==================== 明代改革家 ====================
            "张居正": ReformerProfile(
                name="张居正", era="1525-1582年", dynasty="明代", title="首辅",
                historical_status="万历初期首辅，著名改革家",
                core_thoughts=["一条鞭法", "考成法", "整饬吏治", "重用循吏"],
                reform_achievements=["推行一条鞭法", "考成法等改革措施"],
                wisdom_distillation=[
                    "一条鞭法是税收制度重大改革",
                    "考成法是绩效考核的先河",
                    "整饬吏治是干部管理的核心",
                    "人亡政息是改革的悲剧"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=10, crisis_response=9, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.FISCAL, ReformDomain.PERSONNEL],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.FISCAL_POLICY, ProblemType.CADRES_MGMT],
                quote="法所当加，虽贵近不宥；意有所纵，虽疏贱必旌",
                quote_source="张居正"
            ),
            "海瑞": ReformerProfile(
                name="海瑞", era="1514-1587年", dynasty="明代", title="南京右都御史",
                historical_status="海青天的原型",
                core_thoughts=["清正廉洁", "刚正不阿", "直言极谏", "节俭治国"],
                reform_achievements=["清廉政治", "打击贪腐"],
                wisdom_distillation=[
                    "清正廉洁是政治伦理的底线",
                    "刚正不阿是人格独立的表达",
                    "刚极易折是清官困境"
                ],
                governance=8, reform_courage=9, people_centered=10,
                organization=8, crisis_response=7, diplomatic=6,
                domains=[ReformDomain.ADMIN, ReformDomain.LEGAL],
                applicable_problems=[ProblemType.CADRES_MGMT],
                quote="粉身碎骨全不怕，要留清白在人间",
                quote_source="海瑞"
            ),
            "于谦": ReformerProfile(
                name="于谦", era="1398-1457年", dynasty="明代", title="兵部尚书",
                historical_status="北京保卫战的英雄",
                core_thoughts=["保卫北京", "社稷为重君为轻", "刚正不阿", "廉洁奉公"],
                reform_achievements=["组织北京保卫战", "挽救明朝"],
                wisdom_distillation=[
                    "社稷为重君为轻是民本思想的体现",
                    "北京保卫战是危机应对的典范",
                    "功高震主遭迫害是忠臣悲剧"
                ],
                governance=10, reform_courage=10, people_centered=10,
                organization=10, crisis_response=10, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.MILITARY],
                applicable_problems=[ProblemType.CRISIS_RESPONSE],
                quote="粉骨碎身浑不怕，要留清白在人间",
                quote_source="于谦"
            ),
            # ==================== 晚清改革家 ====================
            "林则徐": ReformerProfile(
                name="林则徐", era="1785-1850年", dynasty="清代", title="钦差大臣",
                historical_status="民族英雄",
                core_thoughts=["虎门销烟", "睁眼看世界", "师敌之长技", "严禁鸦片"],
                reform_achievements=["领导禁烟运动", "抵抗英国侵略"],
                wisdom_distillation=[
                    "虎门销烟是民族尊严的体现",
                    "睁眼看世界是开放精神的先声",
                    "师敌之长技是务实学习的智慧"
                ],
                governance=10, reform_courage=10, people_centered=10,
                organization=9, crisis_response=10, diplomatic=9,
                domains=[ReformDomain.ADMIN, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.CRISIS_RESPONSE, ProblemType.DIPLOMATIC],
                quote="苟利国家生死以，岂因祸福避趋之",
                quote_source="林则徐"
            ),
            "曾国藩": ReformerProfile(
                name="曾国藩", era="1811-1872年", dynasty="清代", title="两江总督",
                historical_status="洋务运动领袖",
                core_thoughts=["洋务运动", "以儒治国", "编练新军", "师夷长技"],
                reform_achievements=["领导洋务运动", "创办安庆内军械所"],
                wisdom_distillation=[
                    "洋务运动是近代化改革的先声",
                    "师夷长技是开放学习的体现",
                    "中体西用是改革局限"
                ],
                governance=10, reform_courage=9, people_centered=9,
                organization=10, crisis_response=10, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.MILITARY],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.CRISIS_RESPONSE],
                quote="天下之至柔，驰骋天下之至坚",
                quote_source="曾国藩"
            ),
            "左宗棠": ReformerProfile(
                name="左宗棠", era="1812-1885年", dynasty="清代", title="陕甘总督",
                historical_status="收复新疆",
                core_thoughts=["收复新疆", "洋务运动", "塞防论"],
                reform_achievements=["收复新疆", "参与洋务运动"],
                wisdom_distillation=[
                    "收复新疆是维护国家统一的壮举",
                    "塞防论是国防战略的智慧",
                    "边疆建设是长远投资"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=10, crisis_response=10, diplomatic=8,
                domains=[ReformDomain.MILITARY, ReformDomain.DIPLOMATIC],
                applicable_problems=[ProblemType.CRISIS_RESPONSE, ProblemType.DIPLOMATIC],
                quote=""
            ),
            "张之洞": ReformerProfile(
                name="张之洞", era="1837-1909年", dynasty="清代", title="体仁阁大学士",
                historical_status="洋务运动后期领袖",
                core_thoughts=["中学为体西学为用", "实业救国", "创办工厂", "兴办新学"],
                reform_achievements=["推动洋务运动后期发展"],
                wisdom_distillation=[
                    "中学为体西学为用是文化整合的智慧",
                    "实业救国是经济现代化的先声",
                    "体用之争延续至今"
                ],
                governance=10, reform_courage=10, people_centered=9,
                organization=10, crisis_response=9, diplomatic=8,
                domains=[ReformDomain.ADMIN, ReformDomain.FISCAL],
                applicable_problems=[ProblemType.REFORM_PUSH, ProblemType.FISCAL_POLICY],
                quote="旧学为体，新学为用",
                quote_source="张之洞"
            ),
        }
    
    def _init_strategy_map(self) -> Dict[str, ReformStrategy]:
        """初始化改革策略库（懒加载）"""
        raw_data = get_strategy_data()
        return {
            name: ReformStrategy(**data) 
            for name, data in raw_data.items()
        }
    
    def get_reformer(self, name: str) -> Optional[ReformerProfile]:
        """获取改革家档案"""
        return self._reformers.get(name)
    
    def query_reformers_by_domain(self, domain: ReformDomain) -> List[ReformerProfile]:
        """按领域查询改革家"""
        return [r for r in self._reformers.values() if domain in r.domains]
    
    def query_reformers_by_problem(self, problem: ProblemType) -> List[ReformerProfile]:
        """按问题类型查询相关改革家"""
        return [r for r in self._reformers.values() if problem in r.applicable_problems]
    
    def get_top_reformers(self, capability: str, top_n: int = 5) -> List[Tuple[str, ReformerProfile]]:
        """获取某项能力最强的改革家"""
        capability_map = {
            "governance": "governance",
            "reform_courage": "reform_courage",
            "people_centered": "people_centered",
            "organization": "organization",
            "crisis_response": "crisis_response",
            "diplomatic": "diplomatic"
        }
        attr = capability_map.get(capability, "governance")
        sorted_reformers = sorted(
            self._reformers.items(),
            key=lambda x: getattr(x[1], attr),
            reverse=True
        )
        return sorted_reformers[:top_n]
    
    def get_reform_strategy(self, strategy_type: str) -> Optional[ReformStrategy]:
        """获取改革策略"""
        return self._strategy_map.get(strategy_type)
    
    def get_strategy_recommendation(self, problem: ProblemType) -> List[ReformStrategy]:
        """根据问题推荐改革策略"""
        mapping = {
            ProblemType.REFORM_PUSH: ["激进改革", "渐进改革"],
            ProblemType.CADRES_MGMT: ["人才治国"],
            ProblemType.FISCAL_POLICY: ["财政改革"],
            ProblemType.CRISIS_RESPONSE: ["危机应对"],
            ProblemType.DIPLOMATIC: ["外交博弈"],
            ProblemType.STABILITY: ["渐进改革"],
            ProblemType.CENTRALIZATION: ["激进改革"],
        }
        strategy_names = mapping.get(problem, [])
        return [self._strategy_map[s] for s in strategy_names if s in self._strategy_map]
    
    def assess_governance_capacity(self, context: Dict) -> Dict:
        """评估治理能力"""
        assessment = {
            "stability": context.get("stability", 5),
            "reform_pressure": context.get("reform_pressure", 5),
            "cadres_quality": context.get("cadres_quality", 5),
            "fiscal_health": context.get("fiscal_health", 5),
            "public_support": context.get("public_support", 5),
        }
        overall = sum(assessment.values()) / len(assessment)
        
        if overall >= 8:
            recommendation = "时机成熟，可以推进改革"
        elif overall >= 5:
            recommendation = "需要先巩固基础，再图改革"
        else:
            recommendation = "当前形势严峻，需先稳定局面"
        
        return {
            "assessment": assessment,
            "overall_score": overall,
            "recommendation": recommendation
        }
    
    def analyze_reform_risk(self, reformer_name: str) -> Dict:
        """分析改革者风险"""
        reformer = self._reformers.get(reformer_name)
        if not reformer:
            return {"error": "未找到该改革者"}
        
        risk_factors = []
        
        # 改革魄力过高可能导致激进
        if reformer.reform_courage >= 9:
            risk_factors.append("变法魄力过高，可能过于激进")
        
        # 民本意识不足可能导致失败
        if reformer.people_centered < 8:
            risk_factors.append("民本意识不足，可能失去民心")
        
        # 外交能力不足可能在外部压力下失败
        if reformer.diplomatic < 8:
            risk_factors.append("外交智慧不足，可能应对不了外部压力")
        
        # 危机应对能力不足
        if reformer.crisis_response < 8:
            risk_factors.append("危机应对能力不足")
        
        return {
            "reformer": reformer_name,
            "risk_factors": risk_factors if risk_factors else ["风险相对可控"],
            "overall_capacity": {
                "governance": reformer.governance,
                "reform_courage": reformer.reform_courage,
                "people_centered": reformer.people_centered,
                "organization": reformer.organization,
                "crisis_response": reformer.crisis_response,
                "diplomatic": reformer.diplomatic
            }
        }
    
    def get_wisdom_summary(self) -> Dict:
        """获取智慧总纲"""
        return {
            "core_principles": [
                "以民为本：得民心者得天下",
                "以法治国：制度比人治更可靠",
                "任贤使能：人才是治国的根本",
                "改革魄力：变法图强是历史规律",
                "以史为鉴：读史使人明智",
                "知进退：功成身退是自我保全"
            ],
            "reform_lessons": [
                "改革需要时机，急躁往往失败",
                "改革者需要核心团队支持",
                "改革需要赢得民心",
                "改革需要考虑后续执行",
                "改革者往往下场不佳"
            ],
            "cadres_management": [
                "任人唯贤，不拘一格",
                "德才兼备，以德为先",
                "用人不疑，疑人不用",
                "形成人才梯队"
            ],
            "fiscal_wisdom": [
                "理财是治国之本",
                "开源节流，量入为出",
                "藏富于民，民富国强"
            ]
        }


# ==================== 单例模式 ====================
_ENGINE_INSTANCE: Optional[PoliticalReformWisdomCore] = None

def get_political_reform_wisdom() -> PoliticalReformWisdomCore:
    """获取政治改革家智慧核心引擎实例"""
    global _ENGINE_INSTANCE
    if _ENGINE_INSTANCE is None:
        _ENGINE_INSTANCE = PoliticalReformWisdomCore()
    return _ENGINE_INSTANCE
