# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_chinese_consumer_culture',
    'analyze_consumption_culture',
    'get_chinese_consumer_culture_engine',
    'get_chinese_cultural_guidance',
    'get_cultural_guidance',
    'get_wisdom_summary',
]

中国社会消费文化智慧引擎 v1.0.0
Chinese Consumer Culture Wisdom Engine
=====================================

基于对中国社会结构,消费文化,价值观的系统研究,
为AI提供中国社会本土化认知与decision支持.

核心研究成果(来源:<中国社会消费文化特色深度研究报告_v2>):
1. 儒家二元消费伦理:节俭 vs 仪式性投入
2. 关系面子机制:面子驱动消费 vs 面子约束消费
3. 符号身份建构:身份表达 vs 消费异化
4. 差序格局消费:关系亲疏影响消费decision
5. 家庭本位decision:代际利益优先于个体满足

版本:v1.0.0
日期:2026-04-04
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ConsumerCultureTheme(Enum):
    """消费文化主题"""
    # 儒家二元伦理
    CONFUCIAN_FRUGALITY = "节俭伦理"      # 日常消费的节俭原则
    CONFUCIAN_RITUAL = "仪式性消费"        # 婚礼,节日,礼品的仪式消费
    
    # 关系与面子
    RELATIONSHIP_BOUNDARY = "关系边界"     # 差序格局中的消费边界
    FACE_MOTIVATION = "面子驱动"           # 面子作为消费动力
    FACE_CONSTRAINT = "面子约束"           # 面子限制消费行为
    
    # 符号与身份
    IDENTITY_EXPRESSION = "身份表达"       # 消费作为身份符号
    SYMBOLIC_CONSUMPTION = "符号消费"     # 品牌,logo背后的符号意义
    CONSUMER_ALIENATION = "消费异化"       # 被消费符号奴役
    
    # 家庭与代际
    FAMILY_CENTERED = "家庭本位"           # 以家庭利益为中心的消费decision
    INTERGENERATIONAL_SUPPORT = "代际支持"  # 子女/父母的经济支持模式
    
    # 数字消费
    DIGITAL_CONSUMPTION = "数字消费"       # 直播电商,社交消费
    EMOTIONAL_ECOHOMY = "情绪经济"        # 为情绪价值付费
    
    # 文化自信
    CULTURAL_CONSUMPTION = "文化消费"     # 国潮,传统文化相关消费
    NATIONAL_IDENTITY = "民族认同消费"     # 爱国情怀与消费的结合

class ConsumptionScene(Enum):
    """消费场景"""
    DAILY_LIVING = "日常生活"      # 柴米油盐日常开支
    CELEBRATION = "庆典仪式"        # 婚礼,寿宴,节日
    GIFT_EXCHANGE = "人情往来"      # 送礼,人情红包
    STATUS_DISPLAY = "身份展示"     # 车,房,包,表
    FAMILY_EDUCATION = "家庭支出"   # 子女教育,家庭投资
    HEALTH_WELLNESS = "健康养生"   # 保健品,医疗
    ENTERTAINMENT = "娱乐休闲"      # 旅游,游戏,娱乐
    DIGITAL_LIFESTYLE = "数字生活"   # 会员,短视频,知识付费

@dataclass
class FaceMechanism:
    """面子机制分析"""
    face_drivers: List[str]           # 面子驱动因素
    face_constraints: List[str]       # 面子约束因素
    face_investment_level: float      # 面子投资程度 (0-1)
    face_risk_awareness: float        # 面子风险意识 (0-1)

@dataclass
class SymbolicIdentity:
    """符号身份分析"""
    identity_needs: List[str]         # 身份认同需求
    symbol_preferences: List[str]      # 符号偏好(品牌/品类)
    alienation_risk: float            # 异化风险 (0-1)
    authentic_expression: str         # 真实表达建议

@dataclass
class ConfucianBinaryEthics:
    """儒家二元消费伦理"""
    frugality_score: float            # 节俭程度 (0-1)
    ritual_investment: float           # 仪式性投入程度 (0-1)
    balance_point: str                # 平衡点描述
    tension_description: str          # 内在张力描述

@dataclass
class FamilyCenteredDecision:
    """家庭本位decision"""
    family_first_score: float          # 家庭优先程度 (0-1)
    intergenerational_weight: float    # 代际利益权重 (0-1)
    decision_makers: List[str]        # decision参与者
    family_harmony_consideration: float  # 家庭和谐考量 (0-1)

@dataclass
class ConsumerCultureAnalysis:
    """消费文化分析结果"""
    # 儒家二元伦理
    confucian_ethics: ConfucianBinaryEthics
    
    # 面子机制
    face_mechanism: FaceMechanism
    
    # 符号身份
    symbolic_identity: SymbolicIdentity
    
    # 家庭本位
    family_centered: FamilyCenteredDecision
    
    # 适用主题
    dominant_themes: List[ConsumerCultureTheme]
    
    # 文化洞察
    cultural_insights: List[str]
    
    # decision建议
    strategic_advice: List[str]
    
    # 风险提示
    risk_warnings: List[str]
    
    # 置信度
    confidence: float

class ChineseConsumerCultureEngine:
    """
    中国社会消费文化智慧引擎
    
    基于社会学,人类学,心理学理论研究,
    提供中国社会本土化的消费文化分析框架.
    
    三维分析框架:
    ┌────────────────────────────────────────────────────────┐
    │            中国消费文化"深层语法"                        │
    ├────────────────────────────────────────────────────────┤
    │  1. 儒家二元消费伦理:节俭 vs 仪式性投入                │
    │     - 日常消费:勤俭持家                               │
    │     - 仪式场合:倾力以赴                               │
    │                                                        │
    │  2. 关系面子机制:驱动 vs 约束                         │
    │     - 面子驱动:身份展示,社交地位                      │
    │     - 面子约束:量入为出,避免炫耀                      │
    │                                                        │
    │  3. 符号身份建构:表达 vs 异化                         │
    │     - 真实需求:身份表达,价值认同                       │
    │     - 异化风险:被符号奴役,消费焦虑                    │
    └────────────────────────────────────────────────────────┘
    """

    def __init__(self):
        self.name = "ChineseConsumerCultureEngine"
        self.version="6.2.0"
        
        # 面子投资阈值(超过则触发风险提示)
        self.face_investment_threshold = 0.7
        
        # 异化风险阈值
        self.alienation_risk_threshold = 0.6
        
        # 消费场景与文化主题mapping
        self.scene_theme_map = {
            ConsumptionScene.DAILY_LIVING: [
                ConsumerCultureTheme.CONFUCIAN_FRUGALITY,
                ConsumerCultureTheme.FAMILY_CENTERED
            ],
            ConsumptionScene.CELEBRATION: [
                ConsumerCultureTheme.CONFUCIAN_RITUAL,
                ConsumerCultureTheme.FACE_MOTIVATION
            ],
            ConsumptionScene.GIFT_EXCHANGE: [
                ConsumerCultureTheme.RELATIONSHIP_BOUNDARY,
                ConsumerCultureTheme.FACE_CONSTRAINT,
                ConsumerCultureTheme.FAMILY_CENTERED
            ],
            ConsumptionScene.STATUS_DISPLAY: [
                ConsumerCultureTheme.FACE_MOTIVATION,
                ConsumerCultureTheme.SYMBOLIC_CONSUMPTION,
                ConsumerCultureTheme.CONSUMER_ALIENATION
            ],
            ConsumptionScene.FAMILY_EDUCATION: [
                ConsumerCultureTheme.FAMILY_CENTERED,
                ConsumerCultureTheme.INTERGENERATIONAL_SUPPORT,
                ConsumerCultureTheme.IDENTITY_EXPRESSION
            ],
            ConsumptionScene.HEALTH_WELLNESS: [
                ConsumerCultureTheme.FAMILY_CENTERED,
                ConsumerCultureTheme.DIGITAL_CONSUMPTION
            ],
            ConsumptionScene.ENTERTAINMENT: [
                ConsumerCultureTheme.EMOTIONAL_ECOHOMY,
                ConsumerCultureTheme.DIGITAL_CONSUMPTION
            ],
            ConsumptionScene.DIGITAL_LIFESTYLE: [
                ConsumerCultureTheme.DIGITAL_CONSUMPTION,
                ConsumerCultureTheme.EMOTIONAL_ECOHOMY,
                ConsumerCultureTheme.CULTURAL_CONSUMPTION
            ]
        }
        
        # 文化洞察库
        self.cultural_insights_lib = {
            ConsumerCultureTheme.CONFUCIAN_FRUGALITY: [
                "节俭是儒家伦理的核心美德,但并非绝对禁止消费",
                "关键在于'当用不省,当省不用'的智慧平衡",
                "日常消费的克制为仪式场合的慷慨积蓄资源"
            ],
            ConsumerCultureTheme.CONFUCIAN_RITUAL: [
                "婚礼红包数额反映关系亲疏和面子水平",
                "仪式性消费是社会关系确认和强化的重要仪式",
                "投入程度受社会规范和关系网络的隐性约束"
            ],
            ConsumerCultureTheme.RELATIONSHIP_BOUNDARY: [
                "费孝通'差序格局':以己为中心,波纹向外递减",
                "消费decision受关系亲疏的隐性影响",
                "边界感模糊导致人情负担加重"
            ],
            ConsumerCultureTheme.FACE_MOTIVATION: [
                "面子是中国社会重要的社会资本",
                "面子投资可带来社会认可和关系维护",
                "但过度追求面子导致炫耀性消费和攀比"
            ],
            ConsumerCultureTheme.FACE_CONSTRAINT: [
                "面子同时也是消费行为的隐性约束",
                "避免'露富','炫耀'成为重要的社会规范",
                "'枪打出头鸟'的文化心理制约极端消费"
            ],
            ConsumerCultureTheme.IDENTITY_EXPRESSION: [
                "消费是身份建构的重要手段",
                "通过消费选择展示自我认同和社会位置",
                "Z世代尤其重视消费的个性化表达"
            ],
            ConsumerCultureTheme.SYMBOLIC_CONSUMPTION: [
                "品牌溢价背后是符号价值的购买",
                "符号消费满足社会认同和群体归属需求",
                "凡勃伦效应:价格越高越有人买"
            ],
            ConsumerCultureTheme.CONSUMER_ALIENATION: [
                "被消费符号奴役,失去真实需求judge",
                "'种草','拔草'循环制造消费焦虑",
                "警惕将自我价值与消费能力挂钩"
            ],
            ConsumerCultureTheme.FAMILY_CENTERED: [
                "家庭利益往往优先于个人偏好",
                "子女教育是家庭消费的绝对优先项",
                "代际支持是中国家庭的重要功能"
            ],
            ConsumerCultureTheme.INTERGENERATIONAL_SUPPORT: [
                "'六个钱包'购房现象体现代际资源整合",
                "父母往往为子女倾尽所有",
                "反哺式养老也体现了代际义务"
            ],
            ConsumerCultureTheme.DIGITAL_CONSUMPTION: [
                "直播电商利用情感共鸣创造消费冲动",
                "'OMG买它'背后是情感操控的边界问题",
                "碎片化娱乐消费成为时间消费主流"
            ],
            ConsumerCultureTheme.EMOTIONAL_ECOHOMY: [
                "为'情绪价值'付费成为新消费趋势",
                "解压玩具,治愈系消费兴起",
                "孤独经济催生陪伴型消费"
            ],
            ConsumerCultureTheme.CULTURAL_CONSUMPTION: [
                "国潮崛起体现文化自信",
                "汉服,古风,国风消费体现身份认同",
                "但警惕'文化自信'被商业收编"
            ],
            ConsumerCultureTheme.NATIONAL_IDENTITY: [
                "爱国情怀与消费选择产生关联",
                "民族品牌获得情感溢价",
                "需警惕将消费选择与爱国绑定"
            ]
        }
        
        # 风险提示库
        self.risk_warning_lib = {
            ConsumerCultureTheme.FACE_MOTIVATION: [
                "面子消费可能导致超支和攀比",
                "警惕'婚不起','节不过'的人情负担"
            ],
            ConsumerCultureTheme.SYMBOLIC_CONSUMPTION: [
                "品牌崇拜可能导致消费主义陷阱",
                "真正的身份认同不应依赖物质符号"
            ],
            ConsumerCultureTheme.CONSUMER_ALIENATION: [
                "直播带货的紧迫感制造冲动消费",
                "警惕'买它'文化对理性消费的侵蚀"
            ],
            ConsumerCultureTheme.DIGITAL_CONSUMPTION: [
                "数字消费的时间成本往往被低估",
                "会员订阅的累积费用值得关注"
            ],
            ConsumerCultureTheme.NATIONAL_IDENTITY: [
                "爱国消费不应成为道德绑架的工具",
                "理性消费与爱国并不矛盾"
            ]
        }
        
        # strategy建议库
        self.strategic_advice_lib = {
            "节俭与仪式平衡": [
                "日常消费保持理性克制",
                "重要仪式场合可适度投入",
                "避免两者错位(日常奢侈,仪式吝啬)"
            ],
            "面子管理": [
                "面子是社会资本,但非越多越好",
                "量力而行,避免打肿脸充胖子",
                "真正的面子来自于内在品格"
            ],
            "符号与真实": [
                "区分'我想要的'和'符号告诉我的'",
                "消费应服务于真实生活需求",
                "警惕被广告和KOL定义自我"
            ],
            "家庭与个体": [
                "在家庭责任与个人发展间寻找平衡",
                "代际支持应是双向的,可持续的",
                "避免过度牺牲导致自身发展受限"
            ],
            "数字消费": [
                "设置数字消费预算和冷静期",
                "警惕直播带货的情感操控",
                "时间成本也是消费成本"
            ]
        }

    def analyze_consumption_culture(
        self,
        scenario: str,
        target_audience: Optional[Dict[str, Any]] = None,
        cultural_context: Optional[str] = None
    ) -> ConsumerCultureAnalysis:
        """
        分析消费文化characteristics
        
        Args:
            scenario: 消费场景描述
            target_audience: 目标受众characteristics
                - age_group: 年龄群体(Z世代/小镇青年/中产/银发等)
                - income_level: 收入水平
                - location: 地域
                - family_status: 家庭状况
            cultural_context: 文化背景描述
            
        Returns:
            消费文化分析结果
        """
        # recognize消费场景
        scene = self._identify_scene(scenario)
        
        # get相关主题
        themes = self.scene_theme_map.get(scene, [])
        
        # generate儒家二元伦理分析
        confucian_ethics = self._analyze_confucian_ethics(scene, target_audience)
        
        # generate面子机制分析
        face_mechanism = self._analyze_face_mechanism(scene, target_audience)
        
        # generate符号身份分析
        symbolic_identity = self._analyze_symbolic_identity(scene, target_audience)
        
        # generate分庭本位分析
        family_centered = self._analyze_family_centered(scene, target_audience)
        
        # 收集文化洞察
        insights = self._collect_insights(themes)
        
        # generatestrategy建议
        advice = self._generate_strategic_advice(scene, themes, target_audience)
        
        # recognize风险提示
        warnings = self._identify_risks(face_mechanism, symbolic_identity, themes)
        
        return ConsumerCultureAnalysis(
            confucian_ethics=confucian_ethics,
            face_mechanism=face_mechanism,
            symbolic_identity=symbolic_identity,
            family_centered=family_centered,
            dominant_themes=themes,
            cultural_insights=insights,
            strategic_advice=advice,
            risk_warnings=warnings,
            confidence=0.85
        )

    def _identify_scene(self, scenario: str) -> ConsumptionScene:
        """recognize消费场景"""
        scenario_lower = scenario.lower()
        
        scene_keywords = {
            ConsumptionScene.DAILY_LIVING: ["日常", "柴米油盐", "买菜", "超市", "生活"],
            ConsumptionScene.CELEBRATION: ["婚礼", "寿宴", "满月", "节日", "过年", "中秋"],
            ConsumptionScene.GIFT_EXCHANGE: ["送礼", "红包", "人情", "礼物"],
            ConsumptionScene.STATUS_DISPLAY: ["豪车", "名表", "奢侈品", "房子", "面子"],
            ConsumptionScene.FAMILY_EDUCATION: ["教育", "培训", "学区房", "留学"],
            ConsumptionScene.HEALTH_WELLNESS: ["健康", "养生", "医疗", "保险"],
            ConsumptionScene.ENTERTAINMENT: ["旅游", "娱乐", "游戏", "电影"],
            ConsumptionScene.DIGITAL_LIFESTYLE: ["会员", "直播", "短视频", "知识付费"]
        }
        
        for scene, keywords in scene_keywords.items():
            if any(kw in scenario_lower for kw in keywords):
                return scene
        
        return ConsumptionScene.DAILY_LIVING

    def _analyze_confucian_ethics(
        self,
        scene: ConsumptionScene,
        audience: Optional[Dict]
    ) -> ConfucianBinaryEthics:
        """分析儒家二元消费伦理"""
        # 根据场景judge节俭与仪式投入程度
        if scene in [ConsumptionScene.CELEBRATION, ConsumptionScene.GIFT_EXCHANGE]:
            frugality = 0.3
            ritual = 0.8
        elif scene in [ConsumptionScene.STATUS_DISPLAY, ConsumptionScene.DIGITAL_LIFESTYLE]:
            frugality = 0.5
            ritual = 0.6
        else:
            frugality = 0.7
            ritual = 0.4
        
        # 年龄群体调节
        if audience and "age_group" in audience:
            if audience["age_group"] == "Z世代":
                frugality *= 0.8
                ritual *= 1.1
            elif audience["age_group"] == "银发":
                frugality *= 1.2
                ritual *= 0.9
        
        return ConfucianBinaryEthics(
            frugality_score=min(frugality, 1.0),
            ritual_investment=min(ritual, 1.0),
            balance_point="日常消费节俭克制,仪式场合适度投入,张力在于边界判定",
            tension_description="儒家伦理允许仪式性奢侈,但反对日常性挥霍;然而边界模糊易导致攀比"
        )

    def _analyze_face_mechanism(
        self,
        scene: ConsumptionScene,
        audience: Optional[Dict]
    ) -> FaceMechanism:
        """分析面子机制"""
        # 面子驱动因素
        face_drivers = []
        # 面子约束因素
        face_constraints = []
        
        if scene == ConsumptionScene.CELEBRATION:
            face_drivers = [
                "社会关系确认需要",
                "家族荣耀的表达",
                "宾客数量的社会信号"
            ]
            face_constraints = [
                "宾客礼金的隐性规范",
                "经济承受力的现实约束"
            ]
        elif scene == ConsumptionScene.GIFT_EXCHANGE:
            face_drivers = [
                "关系维护的必要投入",
                "回礼的礼尚往来"
            ]
            face_constraints = [
                "'礼轻情意重'的传统观念",
                "关系深浅决定投入多少"
            ]
        elif scene == ConsumptionScene.STATUS_DISPLAY:
            face_drivers = [
                "身份地位的展示需求",
                "社交媒体的放大效应",
                "攀比心理的驱动"
            ]
            face_constraints = [
                "'枪打出头鸟'的文化警示",
                "经济实力的真实限制"
            ]
        else:
            face_constraints = [
                "日常消费不宜张扬",
                "'财不露白'的传统智慧"
            ]
        
        # 计算面子投资水平
        investment = 0.5
        if scene in [ConsumptionScene.CELEBRATION, ConsumptionScene.STATUS_DISPLAY]:
            investment = 0.75
        
        return FaceMechanism(
            face_drivers=face_drivers,
            face_constraints=face_constraints,
            face_investment_level=investment,
            face_risk_awareness=0.6 if investment > 0.7 else 0.8
        )

    def _analyze_symbolic_identity(
        self,
        scene: ConsumptionScene,
        audience: Optional[Dict]
    ) -> SymbolicIdentity:
        """分析符号身份建构"""
        identity_needs = []
        symbol_preferences = []
        alienation_risk = 0.3
        
        if scene == ConsumptionScene.STATUS_DISPLAY:
            identity_needs = [
                "社会地位确认",
                "群体归属认同",
                "自我价值证明"
            ]
            symbol_preferences = [
                "奢侈品品牌",
                "豪华车",
                "高端房产"
            ]
            alienation_risk = 0.7
        elif scene == ConsumptionScene.DIGITAL_LIFESTYLE:
            identity_needs = [
                "个性化表达",
                "兴趣圈层认同",
                "生活态度展示"
            ]
            symbol_preferences = [
                "潮流品牌",
                "小众设计师",
                "国潮文化"
            ]
            alienation_risk = 0.5
        elif scene == ConsumptionScene.ENTERTAINMENT:
            identity_needs = [
                "生活品质追求",
                "休闲方式展示",
                "生活方式认同"
            ]
            alienation_risk = 0.4
        
        return SymbolicIdentity(
            identity_needs=identity_needs,
            symbol_preferences=symbol_preferences,
            alienation_risk=alienation_risk,
            authentic_expression="区分真实需求与符号诱惑,问自己:没有logo我还想要吗?"
        )

    def _analyze_family_centered(
        self,
        scene: ConsumptionScene,
        audience: Optional[Dict]
    ) -> FamilyCenteredDecision:
        """分析家庭本位decision"""
        family_first = 0.7
        intergenerational = 0.6
        
        if scene == ConsumptionScene.FAMILY_EDUCATION:
            family_first = 0.95
            intergenerational = 0.8
        elif scene == ConsumptionScene.CELEBRATION:
            family_first = 0.85
            intergenerational = 0.7
        
        decision_makers = ["主要decision者"]
        if intergenerational > 0.5:
            decision_makers.append("家庭成员协商")
        
        return FamilyCenteredDecision(
            family_first_score=family_first,
            intergenerational_weight=intergenerational,
            decision_makers=decision_makers,
            family_harmony_consideration=0.8
        )

    def _collect_insights(self, themes: List[ConsumerCultureTheme]) -> List[str]:
        """收集文化洞察"""
        insights = []
        for theme in themes:
            if theme in self.cultural_insights_lib:
                insights.extend(self.cultural_insights_lib[theme][:2])
        return list(set(insights))[:5]

    def _generate_strategic_advice(
        self,
        scene: ConsumptionScene,
        themes: List[ConsumerCultureTheme],
        audience: Optional[Dict]
    ) -> List[str]:
        """generatestrategy建议"""
        advice = []
        
        # 通用建议
        advice.extend(self.strategic_advice_lib.get("节俭与仪式平衡", []))
        
        # 场景特定建议
        if ConsumerCultureTheme.FACE_MOTIVATION in themes:
            advice.extend(self.strategic_advice_lib.get("面子管理", []))
        if ConsumerCultureTheme.SYMBOLIC_CONSUMPTION in themes:
            advice.extend(self.strategic_advice_lib.get("符号与真实", []))
        if ConsumptionScene.DIGITAL_LIFESTYLE == scene:
            advice.extend(self.strategic_advice_lib.get("数字消费", []))
        
        # 年龄群体建议
        if audience and "age_group" in audience:
            if audience["age_group"] == "Z世代":
                advice.append("Z世代应警惕'精致穷'陷阱,在消费自由与长期财务健康间取得平衡")
            elif audience["age_group"] == "小镇青年":
                advice.append("小镇青年品质觉醒是趋势,但需警惕攀比消费和超前消费")
            elif audience["age_group"] == "中产":
                advice.append("中产消费陷阱:维持体面与真实需求之间的边界容易模糊")
            elif audience["age_group"] == "银发":
                advice.append("银发群体应警惕保健品诈骗和情感操控型消费")
        
        return advice[:6]

    def _identify_risks(
        self,
        face: FaceMechanism,
        symbolic: SymbolicIdentity,
        themes: List[ConsumerCultureTheme]
    ) -> List[str]:
        """recognize风险提示"""
        warnings = []
        
        # 面子风险
        if face.face_investment_level > self.face_investment_threshold:
            warnings.append("面子投资过高,需警惕攀比和超支风险")
        
        # 异化风险
        if symbolic.alienation_risk > self.alienation_risk_threshold:
            warnings.append("符号消费异化风险较高,需警惕被消费符号奴役")
        
        # 主题特定风险
        for theme in themes:
            if theme in self.risk_warning_lib:
                warnings.extend(self.risk_warning_lib[theme])
        
        return list(set(warnings))[:4]

    def get_cultural_guidance(
        self,
        topic: str,
        perspective: str = "neutral"
    ) -> Dict[str, Any]:
        """
        get文化指导
        
        Args:
            topic: 主题(如:婚礼消费,送礼,人情等)
            perspective: 视角(neutral/critical/adaptive)
            
        Returns:
            文化指导建议
        """
        topic_lower = topic.lower()
        
        # 婚礼消费
        if "婚礼" in topic or "结婚" in topic:
            return {
                "cultural_norm": "婚礼是中国最重要的仪式性消费之一,承载家族荣耀和社会关系确认",
                "regional_variation": "各地彩礼,婚宴标准差异巨大,需考虑地域因素",
                "strategic_advice": [
                    "根据关系网络确定宾客规模和红包标准",
                    "面子投入应量力而行,避免'婚不起'",
                    "寻找个性化表达与传统规范的平衡点"
                ],
                "risk_warning": "警惕婚礼消费的内卷和攀比陷阱"
            }
        
        # 送礼人情
        if "送礼" in topic or "人情" in topic:
            return {
                "cultural_norm": "人情是中国社会关系维护的核心机制,礼尚往来是基本原则",
                "regional_variation": "各地人情标准不同,一线城市压力更大",
                "strategic_advice": [
                    "建立人情消费预算,避免入不敷出",
                    "关系深浅决定礼金厚薄",
                    "学会拒绝超出承受范围的人情要求"
                ],
                "risk_warning": "人情负担已成为重要社会问题,需理性对待"
            }
        
        # 子女教育
        if "教育" in topic or "学区房" in topic:
            return {
                "cultural_norm": "子女教育是中国家庭消费的绝对优先项,望子成龙是普遍心理",
                "regional_variation": "一线城市教育竞争最为激烈,教育军备竞赛严重",
                "strategic_advice": [
                    "教育投入需考虑家庭承受能力",
                    "警惕'教育焦虑'驱动的非理性消费",
                    "情感陪伴比物质投入更重要"
                ],
                "risk_warning": "过度教育投资可能挤占其他家庭需求和发展空间"
            }
        
        # 养老
        if "养老" in topic:
            return {
                "cultural_norm": "中国养老以家庭为主,养儿防老仍是主流观念",
                "regional_variation": "城市老年人更多依赖社保和积蓄,农村依赖子女",
                "strategic_advice": [
                    "提前规划养老资金,减轻子女负担",
                    "鼓励父母发展兴趣爱好,减少对子女的情感依赖",
                    "平衡自身发展与反哺责任"
                ],
                "risk_warning": "警惕保健品诈骗和以养老为名的情感操控"
            }
        
        # 默认回应
        return {
            "cultural_norm": "中国文化强调关系,面子和仪式,消费decision往往超越个人偏好",
            "strategic_advice": [
                "考虑社会关系网络的隐性影响",
                "在文化规范与个人需求间寻找平衡",
                "警惕过度迎合社会期待而失去自我"
            ]
        }

    def get_wisdom_summary(self) -> str:
        """get智慧总结"""
        return """
╔══════════════════════════════════════════════════════════════════════╗
║           中国社会消费文化智慧 · 核心框架                               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  [三维分析框架]                                                      ║
║                                                                      ║
║  1. 儒家二元消费伦理                                                   ║
║     ┌─────────────────────────────────────────┐                      ║
║     │  节俭 ────────── 仪式性投入              │                      ║
║     │   ↓                ↓                     │                      ║
║     │  日常消费        婚礼/节日/人情            │                      ║
║     │  勤俭持家        倾力以赴                  │                      ║
║     └─────────────────────────────────────────┘                      ║
║                                                                      ║
║  2. 关系面子机制                                                       ║
║     ┌─────────────────────────────────────────┐                      ║
║     │  面子驱动 ────── 面子约束                 │                      ║
║     │   ↓                ↓                     │                      ║
║     │  身份展示        量入为出                  │                      ║
║     │  社会地位        避免炫耀                  │                      ║
║     └─────────────────────────────────────────┘                      ║
║                                                                      ║
║  3. 符号身份建构                                                       ║
║     ┌─────────────────────────────────────────┐                      ║
║     │  身份表达 ────── 消费异化                 │                      ║
║     │   ↓                ↓                     │                      ║
║     │  价值认同        被符号奴役                │                      ║
║     │  群体归属        消费焦虑                  │                      ║
║     └─────────────────────────────────────────┘                      ║
║                                                                      ║
║  [文化基因]                                                          ║
║  · 差序格局:关系亲疏决定消费边界                                       ║
║  · 家庭本位:代际利益优先于个体满足                                     ║
║  · 名分秩序:角色决定消费权限                                          ║
║                                                                      ║
║  [decision智慧]                                                          ║
║  · 当用不省,当省不用                                                  ║
║  · 量力而行,不打肿脸充胖子                                            ║
║  · 区分真实需求与符号诱惑                                              ║
║  · 在面子与里子间取得平衡                                              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """

# 全局实例
_chinese_consumer_culture_engine = None

def get_chinese_consumer_culture_engine() -> ChineseConsumerCultureEngine:
    """get全局实例"""
    global _chinese_consumer_culture_engine
    if _chinese_consumer_culture_engine is None:
        _chinese_consumer_culture_engine = ChineseConsumerCultureEngine()
    return _chinese_consumer_culture_engine

# 兼容函数
def analyze_chinese_consumer_culture(
    scenario: str,
    target_audience: Optional[Dict[str, Any]] = None
) -> ConsumerCultureAnalysis:
    """便捷函数:分析中国消费文化"""
    engine = get_chinese_consumer_culture_engine()
    return engine.analyze_consumption_culture(scenario, target_audience)

def get_chinese_cultural_guidance(
    topic: str,
    perspective: str = "neutral"
) -> Dict[str, Any]:
    """便捷函数:get文化指导"""
    engine = get_chinese_consumer_culture_engine()
    return engine.get_cultural_guidance(topic, perspective)

# 别名
ChineseConsumerCultureWisdomEngine = ChineseConsumerCultureEngine
