# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_binary_structure',
    'analyze_cosmogony_cycle',
    'analyze_hero_journey',
    'compare_myths_cross_culturally',
    'get_deity_system_analysis',
    'identify_myth_archetype',
    'provide_mythological_wisdom',
    'quick_binary_analysis',
    'quick_cycle_analysis',
    'quick_hero_journey',
    'quick_myth_analyze',
]

中国神话智慧引擎 v1.0.0
Mythology Wisdom Engine

基于中国神话体系深度学习文档v2.0(博士研究级)构建
将中国神话的深层结构,叙事模型,宇宙观转化为AI可用的智慧能力

核心能力:
1. 创世叙事模型 - 从混沌到秩序的宇宙generate框架
2. 循环宇宙观 - 混沌→创世→秩序→失衡→灭世→混沌的循环模型
3. 结构主义分析 - 列维-斯特劳斯二元对立框架
4. 英雄旅程mapping - 坎贝尔模型的中国神话mapping
5. 比较神话学 - 跨文明创世叙事对比
6. 三神系并行分析 - 帝俊系/黄帝系/太一系的并行解读
7. 神话层累recognize - 顾颉刚"层累造成古史"的辨伪能力
8. 少数民族宇宙观 - 多元创世叙事的多样性思维

版本: v1.0.0
日期: 2026-04-02
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

# ==================== 核心枚举 ====================

class MythCategory(Enum):
    """神话类别"""
    COSMOGONY = "创世神话"       # 宇宙起源:盘古开天,混沌分化
    ANTHROPOGENY = "人类起源"     # 人类诞生:女娲造人
    ESCHATOLOGY = "灭世神话"      # 世界末日:共工触山,大洪水
    HEROIC = "英雄神话"          # 英雄传奇:后羿射日,夸父逐日,精卫填海
    TRANSFORMATION = "化生神话"   # 物我转化:盘古化生万物
    FLOOD = "洪水神话"           # 洪水灭世与重生:鲧禹治水
    CELESTIAL = "天体神话"        # 日月星辰:嫦娥奔月,牛郎织女
    CULTURE = "文化英雄"         # 文明创造:伏羲画卦,神农尝百草

class MythDeitySystem(Enum):
    """神系归属"""
    DIJUN = "帝俊系"             # 殷商-东夷:帝俊,羲和,常羲
    HUANGDI = "黄帝系"           # 周族-中原:黄帝,颛顼,帝喾,尧舜
    TAIYI = "太一系"             # 楚地:东皇太一,大司命,少司命
    DAOIST = "道教神系"          # 后世整合:三清,玉皇,西王母
    FOLK = "民间神系"            # 地方信仰:城隍,土地,妈祖

class MythStructure(Enum):
    """神话深层结构(列维-斯特劳斯式分析)"""
    CHAOS_ORDER = "混沌vs秩序"     # 盘古开天
    NATURE_CULTURE = "自然vs文化"   # 大禹治水
    RAW_COOKED = "生vs熟"          # 燧人取火
    MALE_FEMALE = "男vs女"          # 伏羲女娲
    LIFE_DEATH = "生vs死"          # 后羿嫦娥
    SKY_EARTH = "天vs地"           # 共工触不周山
    SELF_OTHER = "自我vs他者"      # 夸父逐日

class HeroJourneyStage(Enum):
    """英雄旅程阶段(坎贝尔模型)"""
    ORDINARY_WORLD = "日常世界"
    CALL_TO_ADVENTURE = "冒险召唤"
    REFUSAL_OF_CALL = "拒绝召唤"
    MEETING_MENTOR = "遇见导师"
    CROSSING_THRESHOLD = "跨越阈限"
    TESTS_ALLIES_ENEMIES = "考验,盟友,敌人"
    APPROACH = "接近深渊"
    ORDEAL = "严峻考验"
    REWARD = "获得奖赏"
    ROAD_BACK = "回归之路"
    RESURRECTION = "复活"
    RETURN_WITH_ELIXIR = "携万灵药归来"

# ==================== 数据类 ====================

@dataclass
class MythAnalysisResult:
    """神话分析结果"""
    myth_name: str
    category: MythCategory
    source_texts: List[str]         # 原始文献出处
    academic_debates: List[str]     # 学术争鸣
    structural_analysis: str        # 结构分析
    modern_application: str         # 现代应用
    cross_cultural_links: List[str] # 跨文明链接
    confidence: float = 0.8

@dataclass
class CosmogonyModel:
    """创世模型"""
    phase: str                      # 阶段名称
    description: str                # 描述
    chinese_myth_reference: str     # 中国神话对应
    cross_cultural_parallels: Dict[str, str]  # 跨文明对应
    philosophical_meaning: str      # 哲学含义

@dataclass
class BinaryOpposition:
    """二元对立结构"""
    pole_a: str
    pole_b: str
    mediator: str                   # 调解者
    resolution: str                 # 解决方式
    myth_example: str
    business_application: str

@dataclass
class HeroJourneyMapping:
    """英雄旅程mapping"""
    hero_name: str
    journey_stages: Dict[HeroJourneyStage, str]
    tragic_element: str             # 悲剧性元素
    cultural_significance: str
    modern_leadership_lesson: str

# ==================== 核心引擎 ====================

class MythologyWisdomEngine:
    """
    中国神话智慧引擎 v1.0.0
    
    基于博士研究级中国神话体系,提供:
    - 创世叙事的结构分析
    - 循环宇宙观的战略思维
    - 二元对立的商业应用
    - 英雄旅程的领导力mapping
    - 比较神话学的跨文化洞察
    """

    def __init__(self):
        self.version = "v1.0.0"
        self._init_cosmogony_models()
        self._init_binary_oppositions()
        self._init_hero_journeys()
        self._init_creation_myths_comparison()
        self._init_deity_systems()
        self._init_myth_archetypes()
        logger.info(f"神话智慧引擎 {self.version} init完成")

    # ==================== 创世叙事模型 ====================

    def _init_cosmogony_models(self):
        """init创世叙事模型库"""
        self.cosmogony_phases = [
            CosmogonyModel(
                phase="混沌",
                description="万物未分,无形无象的原初状态",
                chinese_myth_reference="天地混沌如鸡子,盘古生其中(三五历纪)",
                cross_cultural_parallels={
                    "希腊": "卡俄斯(Chaos)--虚空",
                    "北欧": "金伦加鸿沟(Ginnungagap)",
                    "苏美尔": "提亚玛特(Tiamat)--原初海洋",
                    "印度": "无(Asat)--非存在"
                },
                philosophical_meaning="创新前的蓄能期,变革前的酝酿期"
            ),
            CosmogonyModel(
                phase="开辟",
                description="混沌分化,天地初判",
                chinese_myth_reference="阳清为天,阴浊为地(三五历纪)",
                cross_cultural_parallels={
                    "印度": "原人普鲁沙被分割(梨俱吠陀)",
                    "北欧": "尤弥尔被分割为天地",
                    "苏美尔": "马尔杜克分割提亚玛特"
                },
                philosophical_meaning="战略决断期,破局action"
            ),
            CosmogonyModel(
                phase="化生",
                description="创世者身体化为万物",
                chinese_myth_reference="气成风云,声为雷霆...盘古在其中(五运历年记)",
                cross_cultural_parallels={
                    "印度": "普鲁沙之口为婆罗门,手为刹帝利...",
                    "北欧": "尤弥尔之颅为天空,牙齿为岩石",
                    "中国": "盘古左眼为日,右眼为月..."
                },
                philosophical_meaning="资源分配期,价值创造"
            ),
            CosmogonyModel(
                phase="秩序建立",
                description="神祇确立天地秩序",
                chinese_myth_reference="女娲炼五色石补天,断鳌足以立四极(淮南子)",
                cross_cultural_parallels={
                    "苏美尔": "恩利尔分配天地",
                    "希腊": "宙斯建立奥林匹斯秩序",
                    "北欧": "奥丁建立阿斯加德"
                },
                philosophical_meaning="制度建设期,流程规范"
            ),
            CosmogonyModel(
                phase="失衡",
                description="秩序被打破,灾难降临",
                chinese_myth_reference="共工怒触不周山,天柱折,地维绝(淮南子)",
                cross_cultural_parallels={
                    "北欧": "诸神黄昏(Ragnarök)",
                    "印度": "迦罗纪末日(Kali Yuga)",
                    "基督教": "末日审判"
                },
                philosophical_meaning="危机预警,熵增趋势"
            ),
            CosmogonyModel(
                phase="重治",
                description="英雄/神祇恢复秩序",
                chinese_myth_reference="禹治洪水,通轘辕山,化为熊(山海经)",
                cross_cultural_parallels={
                    "苏美尔": "乌塔纳庇什提建方舟",
                    "希腊": "丢卡利翁抛石造人",
                    "希伯来": "诺亚方舟"
                },
                philosophical_meaning="危机处理,韧性重建"
            ),
        ]

    def _init_binary_oppositions(self):
        """init二元对立结构库"""
        self.binary_oppositions = [
            BinaryOpposition(
                pole_a="天(秩序/阳/刚)",
                pole_b="地(混沌/阴/柔)",
                mediator="不周山/天柱",
                resolution="女娲炼石补天",
                myth_example="共工触不周山 → 女娲补天",
                business_application="组织架构断裂 → 制度修补与流程重建"
            ),
            BinaryOpposition(
                pole_a="人(文化/农业/秩序)",
                pole_b="洪水(自然/毁灭/混沌)",
                mediator="鲧/禹",
                resolution="禹疏导而非堵塞",
                myth_example="鲧堵水失败 → 禹疏导成功",
                business_application="传统控制模式失败 → 敏捷灵活的疏导strategy"
            ),
            BinaryOpposition(
                pole_a="十日并出(过度/失衡)",
                pole_b="万物焦枯(衰败/毁灭)",
                mediator="后羿",
                resolution="射九留一",
                myth_example="十日并出 → 后羿射日",
                business_application="过度扩张/多头并进 → 聚焦核心,砍掉冗余"
            ),
            BinaryOpposition(
                pole_a="男(阳/理性/创造)",
                pole_b="女(阴/直觉/化育)",
                mediator="交尾图(婚姻/结合)",
                resolution="阴阳和合,万物化生",
                myth_example="伏羲女娲人首蛇身交尾",
                business_application="不同能力/视角的团队协作产生创新"
            ),
            BinaryOpposition(
                pole_a="永生(超越/神)",
                pole_b="死亡(有限/人)",
                mediator="不死药",
                resolution="嫦娥奔月,永生伴随孤独",
                myth_example="后羿求不死药 → 嫦娥独吞奔月",
                business_application="过度追求完美/不朽可能代价巨大"
            ),
        ]

    def _init_hero_journeys(self):
        """init英雄旅程mapping库"""
        self.hero_journeys = {
            "后羿": HeroJourneyMapping(
                hero_name="后羿",
                journey_stages={
                    HeroJourneyStage.ORDINARY_WORLD: "天神射手,与嫦娥居于人间",
                    HeroJourneyStage.CALL_TO_ADVENTURE: "十日并出,民不聊生",
                    HeroJourneyStage.CROSSING_THRESHOLD: "张弓射日",
                    HeroJourneyStage.ORDEAL: "射九日,杀猰貐,凿齿,九婴,大风,封豨,修蛇",
                    HeroJourneyStage.REWARD: "万民拥戴,成为英雄",
                    HeroJourneyStage.ROAD_BACK: "失去天神身份,无法返回天界",
                    HeroJourneyStage.RESURRECTION: "求不死药,欲重获永生",
                    HeroJourneyStage.RETURN_WITH_ELIXIR: "药被嫦娥所吞,英雄以悲剧收场",
                },
                tragic_element="英雄解决了外在问题,却无法解决内在困境--力能射日,却留不住妻子",
                cultural_significance="中国悲剧英雄的原型:个人能力与社会命运的永恒张力",
                modern_leadership_lesson="解决技术问题后,需关注团队/家庭/精神层面的需求"
            ),
            "鲧禹": HeroJourneyMapping(
                hero_name="鲧→禹(父子接力)",
                journey_stages={
                    HeroJourneyStage.ORDINARY_WORLD: "洪水滔天,百姓流离",
                    HeroJourneyStage.CALL_TO_ADVENTURE: "帝命鲧治水",
                    HeroJourneyStage.ORDEAL: "鲧窃息壤,九年无功,殛于羽山",
                    HeroJourneyStage.RETURN_WITH_ELIXIR: "禹承父业,改堵为疏,十三年功成",
                },
                tragic_element="父亲以失败和死亡为儿子铺路--代际牺牲",
                cultural_significance="中国文化中'前人栽树,后人乘凉'的原型",
                modern_leadership_lesson="允许试错,前人失败的经验是后人成功的基石"
            ),
            "夸父": HeroJourneyMapping(
                hero_name="夸父",
                journey_stages={
                    HeroJourneyStage.ORDINARY_WORLD: "夸父与日逐走",
                    HeroJourneyStage.CALL_TO_ADVENTURE: "入日(追赶太阳)",
                    HeroJourneyStage.ORDEAL: "渴,欲得饮,饮于河渭不足",
                    HeroJourneyStage.REWARD: "邓林(手杖化为桃林,荫庇后人)",
                },
                tragic_element="目标过大导致失败,但失败本身创造了价值",
                cultural_significance="知其不可而为之的中国精神",
                modern_leadership_lesson="即便目标暂时无法达成,过程本身就是价值创造"
            ),
            "精卫": HeroJourneyMapping(
                hero_name="精卫",
                journey_stages={
                    HeroJourneyStage.ORDINARY_WORLD: "女娃游于东海,溺而不返",
                    HeroJourneyStage.CALL_TO_ADVENTURE: "化精卫鸟,常衔西山之木石",
                    HeroJourneyStage.ORDEAL: "以微弱之力填大海--永不放弃",
                    HeroJourneyStage.RETURN_WITH_ELIXIR: "精神不朽,成为坚持的象征",
                },
                tragic_element="最微小的力量对抗最庞大的存在",
                cultural_significance="中国神话中最纯粹的'不屈服'精神",
                modern_leadership_lesson="小企业/个人面对巨头,坚持本身就是意义"
            ),
        }

    def _init_creation_myths_comparison(self):
        """init创世神话比较数据库"""
        self.creation_myths_comparison = {
            "盘古化生": {
                "source": "<五运历年记>(三国·徐整)",
                "method": "身体化生",
                "details": {
                    "气": "风云", "声": "雷霆", "左眼": "日", "右眼": "月",
                    "四肢": "四极", "躯干": "五岳", "血液": "江河",
                    "筋脉": "地理", "肌肉": "田土", "发髭": "星辰",
                    "皮毛": "草木", "齿骨": "金石", "精髓": "珠玉",
                    "汗流": "雨泽", "身中诸虫": "黎甿"
                }
            },
            "普鲁沙化生": {
                "source": "<梨俱吠陀>原人赞歌(印度)",
                "method": "祭祀分割",
                "details": {
                    "口": "婆罗门(祭司)", "双臂": "刹帝利(武士/王)",
                    "大腿": "吠舍(农商)", "双脚": "首陀罗(奴仆)",
                    "心": "月亮", "眼睛": "太阳", "气息": "风",
                    "脐": "空界", "头": "天", "脚": "地"
                }
            },
            "尤弥尔化生": {
                "source": "<诗体埃达>(北欧)",
                "method": "诸神分割",
                "details": {
                    "颅": "天空", "脑": "云", "血": "海洋",
                    "骨": "山", "牙齿": "岩石", "头发": "树木",
                    "睫毛": "米德加尔德(人界)"
                }
            },
        }

    def _init_deity_systems(self):
        """init三神系并行体系"""
        self.deity_systems = {
            MythDeitySystem.DIJUN.value: {
                "origin": "殷商-东夷文明",
                "evidence": "甲骨文'高祖夋'(帝俊),祭祀频次仅次于祖乙",
                "core_deities": ["帝俊(高祖夋)", "羲和(日母)", "常羲(月母)", "禺彊"],
                "worldview": "日神崇拜,天文历法驱动",
                "decline_reason": "周族取代商朝,黄帝系成为正统,帝俊被分化为帝喾/舜等",
                "academic_views": [
                    "王国维:帝俊即帝喾(<殷卜辞中所见先公先王考>)",
                    "郭沫若:帝俊为东方民族至上神",
                    "袁珂:帝俊为上古最高神,后世的帝喾,尧,舜均从其分化"
                ]
            },
            MythDeitySystem.HUANGDI.value: {
                "origin": "周族-中原文明",
                "evidence": "<史记·五帝本纪>系统化",
                "core_deities": ["黄帝", "颛顼", "帝喾", "尧", "舜"],
                "worldview": "人文主义,政治伦理驱动",
                "decline_reason": "成为正统史学,神话被历史化",
                "academic_views": [
                    "顾颉刚:五帝谱系为后人层累建构",
                    "钱穆:黄帝传说经历了从神到人的历史化过程"
                ]
            },
            MythDeitySystem.TAIYI.value: {
                "origin": "楚地文明",
                "evidence": "<楚辞·九歌>东皇太一,郭店楚简<太一生水>",
                "core_deities": ["东皇太一", "大司命", "少司命", "云中君", "湘君湘夫人"],
                "worldview": "宇宙generate论(太一→水→天地→神明→阴阳→四时)",
                "decline_reason": "秦灭楚,汉武帝独尊儒术后楚文化边缘化",
                "academic_views": [
                    "李学勤:太一生水是中国最早的宇宙generate论",
                    "庞朴:太一代表了南方楚文化独特的宇宙观"
                ]
            },
        }

    def _init_myth_archetypes(self):
        """init神话原型库"""
        self.myth_archetypes = {
            "创世者": {
                "examples": ["盘古", "女娲"],
                "pattern": "自我牺牲→万物generate",
                "business_mapping": "创始人精神,从零到一"
            },
            "救世者": {
                "examples": ["后羿", "禹"],
                "pattern": "接受使命→面对考验→拯救苍生(可能悲剧收场)",
                "business_mapping": "危机管理,转型领导者"
            },
            "殉道者": {
                "examples": ["鲧", "夸父", "精卫"],
                "pattern": "明知不可为而为之→失败但精神不朽",
                "business_mapping": "创新先驱,先行者"
            },
            "叛逆者": {
                "examples": ["共工", "刑天"],
                "pattern": "挑战现有秩序→被镇压但永不屈服",
                "business_mapping": "颠覆式创新者"
            },
            "转化者": {
                "examples": ["嫦娥", "禹(化为熊)"],
                "pattern": "形态/身份转变→获得新存在但付出代价",
                "business_mapping": "组织转型,个人成长"
            },
        }

    # ==================== 核心接口 ====================

    def analyze_cosmogony_cycle(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        创世循环分析
        
        将商业/项目情境mapping到"混沌→开辟→化生→秩序→失衡→重治"六阶段循环,
        recognize当前所处阶段并提供智慧建议.
        
        Args:
            business_context: 包含 situation, challenges, goals 等的上下文字典
            
        Returns:
            包含阶段recognize,智慧建议,跨文明参考的分析结果
        """
        situation = business_context.get("situation", "")
        challenges = business_context.get("challenges", "")
        goals = business_context.get("goals", "")

        # 基于关键词的阶段recognize
        phase_scores = {}
        phase_keywords = {
            "混沌": ["迷茫", "不确定", "混乱", "无方向", "未开始", "探索", "模糊"],
            "开辟": ["决断", "启动", "突破", "打破", "新开始", "破局", "创始"],
            "化生": ["扩展", "增长", "多元化", "资源分配", "快速", "爆发"],
            "秩序": ["规范", "制度", "流程", "稳定", "成熟", "规模化"],
            "失衡": ["危机", "风险", "失控", "衰减", "竞争", "问题", "瓶颈"],
            "重治": ["转型", "改革", "调整", "修复", "重建", "复苏", "优化"],
        }

        combined_text = f"{situation} {challenges} {goals}"
        for phase, keywords in phase_keywords.items():
            score = sum(1 for kw in keywords if kw in combined_text)
            phase_scores[phase] = score

        # 确定当前阶段
        current_phase_name = max(phase_scores, key=phase_scores.get) if max(phase_scores.values()) > 0 else "混沌"
        
        # 查找对应模型
        current_phase = None
        next_phase = None
        for i, phase_model in enumerate(self.cosmogony_phases):
            if phase_model.phase == current_phase_name:
                current_phase = phase_model
                next_phase = self.cosmogony_phases[(i + 1) % len(self.cosmogony_phases)]
                break

        # 构建建议
        advice_map = {
            "混沌": "蓄能期:不要急于action,充分调研,理解全局,积蓄势能.混沌不是坏事--它是所有可能性并存的阶段.",
            "开辟": "破局期:需要果敢决断.像盘古开天一样,一刀劈开混沌.关键是找准切入点,不要面面俱到.",
            "化生": "扩张期:像盘古化生万物一样,将核心能力分解为多元价值输出.注意资源不要过度分散.",
            "秩序": "巩固期:建立制度和规范.像女娲立四极一样,确保系统稳定.但警惕过度规范化扼杀创新.",
            "失衡": "危机期:像共工触山一样,秩序可能被打破.不要恐慌--失衡是循环的一部分.关键是recognize失衡的根本原因.",
            "重治": "重建期:像大禹治水一样,不要重复鲧的错误--堵不如疏.用疏导替代控制,用灵活替代刚性.",
        }

        result = {
            "analysis_type": "创世循环分析",
            "current_phase": current_phase_name,
            "phase_description": current_phase.description if current_phase else "未recognize",
            "next_phase": next_phase.phase if next_phase else "循环",
            "mythological_reference": current_phase.chinese_myth_reference if current_phase else "",
            "cross_cultural_parallels": current_phase.cross_cultural_parallels if current_phase else {},
            "philosophical_meaning": current_phase.philosophical_meaning if current_phase else "",
            "wisdom_advice": advice_map.get(current_phase_name, "审视全局,找到破局点"),
            "cycle_position": f"{current_phase_name} → {next_phase.phase if next_phase else '混沌'}",
        }

        return result

    def analyze_binary_structure(self, problem: str, context: str = "") -> Dict[str, Any]:
        """
        二元对立结构分析
        
        用列维-斯特劳斯结构主义方法分析问题中的深层二元对立,
        找到调解者并提出解决框架.
        
        Args:
            problem: 问题描述
            context: 补充上下文
            
        Returns:
            包含对立结构,调解strategy,神话参考的分析结果
        """
        combined = f"{problem} {context}"

        # 问题域匹配
        matched_oppositions = []
        for opp in self.binary_oppositions:
            # 简单关键词匹配
            relevance = 0
            for concept in [opp.pole_a, opp.pole_b, opp.resolution]:
                if any(c in combined for c in concept.split("/")):
                    relevance += 1
            # 问题类型匹配
            if "扩张" in combined or "增长" in combined or "砍" in combined:
                if "十日" in opp.myth_example or "聚焦" in opp.business_application:
                    relevance += 3
            if "危机" in combined or "问题" in combined or "失控" in combined:
                if "洪水" in opp.myth_example or "失衡" in opp.pole_b:
                    relevance += 3
            if "制度" in combined or "规范" in combined or "架构" in combined:
                if "不周山" in opp.myth_example or "秩序" in opp.pole_a:
                    relevance += 3
            if "团队" in combined or "协作" in combined or "多元" in combined:
                if "伏羲" in opp.myth_example or "阴阳" in opp.resolution:
                    relevance += 3
            if "完美" in combined or "过度" in combined or "代价" in combined:
                if "嫦娥" in opp.myth_example or "永生" in opp.pole_a:
                    relevance += 3

            if relevance > 0:
                matched_oppositions.append((opp, relevance))

        matched_oppositions.sort(key=lambda x: x[1], reverse=True)

        results = []
        for opp, score in matched_oppositions[:3]:
            results.append({
                "opposition": f"{opp.pole_a} vs {opp.pole_b}",
                "mediator": opp.mediator,
                "resolution": opp.resolution,
                "myth_example": opp.myth_example,
                "business_application": opp.business_application,
                "relevance_score": score,
                "structural_insight": f"核心矛盾在于{opp.pole_a}与{opp.pole_b}之间的张力."
                                      f"神话给出的解决方案是{opp.resolution}--"
                                      f"对应到现实:{opp.business_application}"
            })

        return {
            "analysis_type": "二元对立结构分析",
            "method": "列维-斯特劳斯结构主义",
            "problem": problem,
            "matched_structures": results,
            "general_advice": "每个难题的背后都是一组深层二元对立.找到调解者(第三条路),比在两极之间选择更有智慧." if not results else None,
        }

    def analyze_hero_journey(self, scenario: str) -> Dict[str, Any]:
        """
        英雄旅程分析
        
        将给定情境mapping到坎贝尔英雄旅程模型,参考中国神话中的英雄原型,
        提供领导力建议和风险预警.
        
        Args:
            scenario: 情境描述
            
        Returns:
            包含英雄mapping,旅程阶段,风险预警的分析结果
        """
        # 匹配英雄原型
        best_hero = None
        best_score = 0
        for name, journey in self.hero_journeys.items():
            score = 0
            if any(kw in scenario for kw in ["危机", "拯救", "外部挑战", "技术"]):
                score += 2 if name == "后羿" else 1
            if any(kw in scenario for kw in ["接手", "前任失败", "改革", "接力"]):
                score += 2 if name == "鲧禹" else 1
            if any(kw in scenario for kw in ["不可能", "挑战巨头", "小团队", "创业"]):
                score += 2 if name in ["夸父", "精卫"] else 1
            if score > best_score:
                best_score = score
                best_hero = name

        if best_hero is None:
            best_hero = "后羿"  # 默认

        journey = self.hero_journeys[best_hero]
        
        return {
            "analysis_type": "英雄旅程分析",
            "hero_model": best_hero,
            "hero_significance": journey.cultural_significance,
            "journey_stages": {stage.value: desc for stage, desc in journey.journey_stages.items()},
            "tragic_element": journey.tragic_element,
            "modern_lesson": journey.modern_leadership_lesson,
            "risk_warning": journey.tragic_element.replace("英雄", "领导者"),
            "archetype_mapping": {
                archetype_name: info["pattern"] + " → " + info["business_mapping"]
                for archetype_name, info in self.myth_archetypes.items()
                if any(kw in scenario for kw in info["business_mapping"])
            }
        }

    def compare_myths_cross_culturally(self, theme: str) -> Dict[str, Any]:
        """
        比较神话学分析
        
        对指定主题进行跨文明比较,揭示人类普遍的叙事模式和文化差异.
        
        Args:
            theme: 比较主题(如"创世""洪水""英雄""灭世")
            
        Returns:
            跨文明比较结果
        """
        comparisons = {
            "创世": {
                "core_question": "世界从何而来?",
                "pattern": "从混沌中分化出秩序",
                "cultures": self.creation_myths_comparison,
                "universal_structure": "原初状态 → 分裂/牺牲 → 万物generate → 秩序建立",
                "key_difference": "中国:创世者独自完成,死后化生;印度:通过祭祀分割;北欧:诸神协作分割",
                "chinese_uniqueness": "盘古故事中,创世者是孤独的--没有神命令他,他自发地开辟天地.这反映了中国文化中'自强不息'的精神内核."
            },
            "洪水": {
                "core_question": "人类如何面对灭顶之灾?",
                "pattern": "洪水毁灭 → 少数幸存 → 重建文明",
                "cultures": {
                    "中国": "鲧堵→禹疏,人定胜天",
                    "苏美尔": "乌塔纳庇什提建方舟",
                    "希伯来": "诺亚方舟,神选救赎",
                    "印度": "摩奴受鱼警告建船",
                    "希腊": "丢卡利翁抛石造人"
                },
                "universal_structure": "神怒/天灾 → 预警 → 生存 → 重生",
                "key_difference": "中国:靠人的努力疏导(禹);西方:靠神的恩典拯救(诺亚)",
                "chinese_uniqueness": "中国洪水神话强调'人'的力量--禹不是靠神力,而是靠智慧和毅力.这体现了中国文化的现世主义取向."
            },
            "灭世": {
                "core_question": "世界如何终结?",
                "pattern": "秩序崩塌 → 混沌回归 → 可能重生",
                "cultures": {
                    "中国": "共工触山(局部)+道教劫运(循环)",
                    "北欧": "诸神黄昏(Ragnarök)--诸神与怪物同归于尽",
                    "印度": "迦罗纪末日--湿婆毁灭→梵天重创",
                    "基督教": "末日审判--善恶最终对决"
                },
                "universal_structure": "道德沦丧 → 秩序崩塌 → 最终对决 → 新纪元",
                "key_difference": "北欧:彻底毁灭不可逆;中国/印度:循环重生;基督教:线性终结",
                "chinese_uniqueness": "中国灭世观是'循环'的--道教五劫(龙汉→延康→赤明→开皇→上皇)是宇宙节律的一部分,不是终极终结."
            }
        }

        theme_key = None
        for key in comparisons:
            if key in theme:
                theme_key = key
                break

        if theme_key is None:
            theme_key = "创世"

        comp = comparisons[theme_key]
        return {
            "analysis_type": "比较神话学分析",
            "theme": theme_key,
            "core_question": comp["core_question"],
            "universal_pattern": comp["pattern"],
            "cultural_comparisons": comp["cultures"],
            "universal_structure": comp["universal_structure"],
            "key_cultural_difference": comp["key_difference"],
            "chinese_uniqueness": comp["chinese_uniqueness"],
        }

    def identify_myth_archetype(self, entity: str, context: str = "") -> Dict[str, Any]:
        """
        神话原型recognize
        
        recognize给定实体(人/组织/项目)最接近的神话原型,
        提供基于原型的行为预测和建议.
        
        Args:
            entity: 实体描述
            context: 上下文
            
        Returns:
            原型分析结果
        """
        combined = f"{entity} {context}"
        
        archetype_scores = {}
        archetype_keywords = {
            "创世者": ["创始", "开创", "从零", "第一", "先驱", "白手起家"],
            "救世者": ["拯救", "危机", "扭转", "复兴", "关键", "核心"],
            "殉道者": ["失败", "牺牲", "坚持", "不为", "独行", "代价"],
            "叛逆者": ["颠覆", "打破", "挑战", "反叛", "冲突", "对抗"],
            "转化者": ["转型", "变化", "蜕变", "重生", "成长", "升级"],
        }

        for archetype, keywords in archetype_keywords.items():
            score = sum(1 for kw in keywords if kw in combined)
            archetype_scores[archetype] = score

        best_archetype = max(archetype_scores, key=archetype_scores.get) if max(archetype_scores.values()) > 0 else None

        if best_archetype and best_archetype in self.myth_archetypes:
            info = self.myth_archetypes[best_archetype]
            return {
                "entity": entity,
                "primary_archetype": best_archetype,
                "examples": info["examples"],
                "pattern": info["pattern"],
                "business_mapping": info["business_mapping"],
                "wisdom": f"你的处境类似神话中的{info['examples'][0]}."
                          f"核心模式是'{info['pattern']}'."
                          f"在商业中对应:{info['business_mapping']}",
                "warning": self._get_archetype_warning(best_archetype),
            }

        return {"entity": entity, "primary_archetype": "未recognize", "suggestion": "提供更多上下文以recognize神话原型"}

    def get_deity_system_analysis(self, organization_type: str) -> Dict[str, Any]:
        """
        三神系组织分析
        
        将组织文化mapping到中国三套并行神系(帝俊系/黄帝系/太一系),
        recognize组织文化的深层结构和发展方向.
        
        Args:
            organization_type: 组织类型描述
            
        Returns:
            神系分析结果
        """
        combined = organization_type.lower()

        system_scores = {}
        system_keywords = {
            MythDeitySystem.DIJUN.value: ["创新", "技术", "天文", "数据", "精密", "崇拜", "创始人"],
            MythDeitySystem.HUANGDI.value: ["传统", "规范", "制度", "流程", "政治", "伦理", "稳定"],
            MythDeitySystem.TAIYI.value: ["哲学", "宇宙", "自然", "自由", "艺术", "思想", "精神"],
        }

        for system, keywords in system_keywords.items():
            score = sum(1 for kw in keywords if kw in combined)
            system_scores[system] = score

        primary_system = max(system_scores, key=system_scores.get) if max(system_scores.values()) > 0 else MythDeitySystem.HUANGDI.value

        system_info = self.deity_systems.get(primary_system, {})

        return {
            "organization_type": organization_type,
            "primary_deity_system": primary_system,
            "system_info": system_info,
            "wisdom": f"你的组织类似{system_info.get('origin', '')}文明."
                      f"其核心characteristics是'{system_info.get('worldview', '')}'."
                      f"历史上的教训:{system_info.get('decline_reason', '')}",
            "academic_views": system_info.get("academic_views", []),
            "evolution_suggestion": "强大的文明/组织需要能够fusion多种神系--帝俊系的创新能力+黄帝系的制度规范+太一系的精神深度."
        }

    def provide_mythological_wisdom(self, question: str) -> Dict[str, Any]:
        """
        神话智慧synthesize查询
        
        根据问题自动选择最合适的分析方法,提供synthesize神话智慧.
        
        Args:
            question: 问题描述
            
        Returns:
            synthesize智慧分析结果
        """
        results = {}

        # strategy选择
        if any(kw in question for kw in ["阶段", "周期", "循环", "当前", "位置", "处于"]):
            results["cycle_analysis"] = self.analyze_cosmogony_cycle({"situation": question})
        if any(kw in question for kw in ["矛盾", "冲突", "对立", "两难", "vs", "还是"]):
            results["structure_analysis"] = self.analyze_binary_structure(question)
        if any(kw in question for kw in ["领导", "英雄", "成长", "挑战", "困难"]):
            results["hero_analysis"] = self.analyze_hero_journey(question)
        if any(kw in question for kw in ["对比", "比较", "中西", "跨文化", "其他文明"]):
            results["comparative"] = self.compare_myths_cross_culturally(question)
        if any(kw in question for kw in ["原型", "类型", "像谁", "类似"]):
            results["archetype"] = self.identify_myth_archetype(question)

        # 如果没有明确触发任何分析器,执行全量分析
        if not results:
            results["cycle_analysis"] = self.analyze_cosmogony_cycle({"situation": question})
            results["structure_analysis"] = self.analyze_binary_structure(question)
            results["hero_analysis"] = self.analyze_hero_journey(question)

        results["meta"] = {
            "engine": f"MythologyWisdomEngine {self.version}",
            "knowledge_source": "中国神话体系深度学习文档v2.0(博士研究级)",
            "core_literature": ["山海经", "楚辞", "淮南子", "三五历纪", "五运历年记", "楚帛书", "甲骨文"],
            "academic_methods": ["文献溯源", "考古印证", "学术争鸣辨析", "比较神话学", "结构主义分析"],
            "timestamp": datetime.now().isoformat(),
        }

        return results

    # ==================== 辅助方法 ====================

    def _get_archetype_warning(self, archetype: str) -> str:
        """get原型风险预警"""
        warnings = {
            "创世者": "注意:创世者往往在建立秩序后失去存在意义.提前规划'后盘古时代'的传承方案.",
            "救世者": "注意:救世者常常以悲剧收场(如后羿).解决外在问题后,不要忽视内在需求.",
            "殉道者": "注意:殉道者的价值往往在死后才被认可.确保你的坚持有可持续的资源支撑.",
            "叛逆者": "注意:叛逆者面临被镇压的风险.找到建设性的表达方式,而非纯粹的对抗.",
            "转化者": "注意:每次转化都有不可逆的代价(如嫦娥失去人间生活).权衡收益与代价.",
        }
        return warnings.get(archetype, "认识自己的原型,才能超越自己的原型.")

# ==================== 便捷函数 ====================

def quick_myth_analyze(question: str) -> Dict[str, Any]:
    """快速神话智慧分析"""
    engine = MythologyWisdomEngine()
    return engine.provide_mythological_wisdom(question)

def quick_cycle_analysis(situation: str) -> Dict[str, Any]:
    """快速创世循环分析"""
    engine = MythologyWisdomEngine()
    return engine.analyze_cosmogony_cycle({"situation": situation})

def quick_binary_analysis(problem: str) -> Dict[str, Any]:
    """快速二元对立分析"""
    engine = MythologyWisdomEngine()
    return engine.analyze_binary_structure(problem)

def quick_hero_journey(scenario: str) -> Dict[str, Any]:
    """快速英雄旅程分析"""
    engine = MythologyWisdomEngine()
    return engine.analyze_hero_journey(scenario)
