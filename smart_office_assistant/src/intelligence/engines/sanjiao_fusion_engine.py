# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_situation',
    'cultivate_three_in_one',
    'fuse_wisdom',
    'get_life_guidance',
    'get_wisdom_by_topic',
    'make_decision',
    'select_traditions',
]

三教合一fusion引擎 v1.0.0
Sanjiao Fusion Engine

儒释道三家智慧fusiondecision系统

核心理念:
- 以儒治世 - 入世担当,伦理秩序
- 以道治身 - 顺应自然,修身养性  
- 以佛治心 - 超越执着,内心解脱

fusion原则:
1. 功能互补 - 三家各有所长,相互补充
2. 情境适配 - 根据情境选择最适合的智慧
3. 层次递进 - 从入世到出世,从修身到修心
4. 和而不同 - 尊重差异,寻求共识

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

# 导入三家智慧核心
from .ru_wisdom_unified import RuWisdomCore, ConfucianClassic, FiveChang
from .dao_wisdom_core import DaoWisdomCore, DaoDeJingCore, YinYangPrinciple
from .buddha_wisdom_core import BuddhaWisdomCore, FourNobleTruths, EightfoldPath

class WisdomTradition(Enum):
    """智慧传统"""
    RU = "儒家"      # 入世之道
    DAO = "道家"     # 自然之道
    BUDDHA = "佛家"  # 解脱之道

class LifeDomain(Enum):
    """人生领域"""
    SOCIAL = "社会"      # 社会关系
    CAREER = "事业"      # 职业发展
    FAMILY = "家庭"      # 家庭关系
    PERSONAL = "个人"    # 个人修养
    SPIRITUAL = "精神"   # 精神追求
    HEALTH = "健康"      # 身心健康

class DecisionLevel(Enum):
    """decision层次"""
    STRATEGIC = "战略"    # 长远规划
    TACTICAL = "战术"     # 中期执行
    OPERATIONAL = "操作"  # 日常操作
    EMERGENCY = "应急"    # 紧急应对

@dataclass
class SanjiaoDecision:
    """三教合一decision结构"""
    primary_tradition: WisdomTradition      # 主要智慧传统
    secondary_traditions: List[WisdomTradition]  # 辅助智慧传统
    domain: LifeDomain                       # 应用领域
    level: DecisionLevel                     # decision层次
    
    # 三家建议
    ru_advice: Dict[str, Any]                # 儒家建议
    dao_advice: Dict[str, Any]               # 道家建议
    buddha_advice: Dict[str, Any]            # 佛家建议
    
    # fusion建议
    integrated_advice: str                   # fusion后的synthesize建议
    action_plan: List[str]                   # action计划
    
    # 评估
    suitability_scores: Dict[str, float]     # 适用性评分
    confidence: float                        # 置信度
    
    # 元信息
    reasoning: str                           # 推理过程
    warnings: List[str]                      # 警示
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SanjiaoPersona:
    """三教合一修行者人格"""
    # 儒家修养
    ren_level: float = 0.5      # 仁
    yi_level: float = 0.5       # 义
    li_level: float = 0.5       # 礼
    zhi_level: float = 0.5      # 智
    xin_level: float = 0.5      # 信
    
    # 道家修养
    wuwei_level: float = 0.5    # 无为
    ziran_level: float = 0.5    # 自然
    yin_yang_balance: float = 0.5  # 阴阳平衡
    
    # 佛家修养
    mindfulness_level: float = 0.5   # 正念
    compassion_level: float = 0.5    # 慈悲
    wisdom_level: float = 0.5        # 智慧
    
    # synthesize修养
    overall_level: int = 5      # synthesize层级(1-10)
    dominant_tradition: Optional[WisdomTradition] = None  # 主导传统

class SanjiaoFusionEngine:
    """
    三教合一fusion引擎
    
    将儒释道三家智慧fusion,提供全面的decision支持:
    1. 情境分析 - 分析decision情境的characteristics
    2. 智慧选择 - 选择最适合的智慧传统
    3. fusion建议 - synthesize三家智慧给出建议
    4. 层次递进 - 从入世到出世的多层次建议
    """
    
    def __init__(self):
        """init三教合一fusion引擎"""
        self.name = "SanjiaoFusionEngine"
        self.version="6.2.0"
        
        # init三家智慧核心
        self.ru_core = RuWisdomCore()
        self.dao_core = DaoWisdomCore()
        self.buddha_core = BuddhaWisdomCore()
        
        # 领域-传统mapping
        self.domain_tradition_map = {
            LifeDomain.SOCIAL: {
                "primary": WisdomTradition.RU,
                "secondary": [WisdomTradition.DAO, WisdomTradition.BUDDHA],
                "reasoning": "社会关系以儒家伦理为核心,道家提供处世智慧,佛家培养慈悲心"
            },
            LifeDomain.CAREER: {
                "primary": WisdomTradition.RU,
                "secondary": [WisdomTradition.DAO],
                "reasoning": "事业发展以儒家进取精神为主,道家提供顺势而为的智慧"
            },
            LifeDomain.FAMILY: {
                "primary": WisdomTradition.RU,
                "secondary": [WisdomTradition.BUDDHA],
                "reasoning": "家庭关系以儒家孝道为核心,佛家培养包容心"
            },
            LifeDomain.PERSONAL: {
                "primary": WisdomTradition.DAO,
                "secondary": [WisdomTradition.RU, WisdomTradition.BUDDHA],
                "reasoning": "个人修养以道家自然无为为核心,儒家提供修身方法,佛家培养内心平静"
            },
            LifeDomain.SPIRITUAL: {
                "primary": WisdomTradition.BUDDHA,
                "secondary": [WisdomTradition.DAO],
                "reasoning": "精神追求以佛家解脱为核心,道家提供自然之道"
            },
            LifeDomain.HEALTH: {
                "primary": WisdomTradition.DAO,
                "secondary": [WisdomTradition.BUDDHA],
                "reasoning": "身心健康以道家养生为核心,佛家提供心理调节"
            }
        }
        
        # 层次-传统mapping
        self.level_tradition_map = {
            DecisionLevel.STRATEGIC: {
                "primary": WisdomTradition.DAO,
                "secondary": [WisdomTradition.RU],
                "reasoning": "战略规划需要道家长远眼光,儒家提供目标导向"
            },
            DecisionLevel.TACTICAL: {
                "primary": WisdomTradition.RU,
                "secondary": [WisdomTradition.DAO],
                "reasoning": "战术执行以儒家积极作为为主,道家提供灵活应变"
            },
            DecisionLevel.OPERATIONAL: {
                "primary": WisdomTradition.RU,
                "secondary": [WisdomTradition.DAO],
                "reasoning": "日常操作以儒家规范为主,道家提供简化方法"
            },
            DecisionLevel.EMERGENCY: {
                "primary": WisdomTradition.DAO,
                "secondary": [WisdomTradition.BUDDHA],
                "reasoning": "应急处理需要道家冷静和佛家平常心"
            }
        }
        
        # fusion原则
        self.fusion_principles = [
            "功能互补 - 三家各有所长,相互补充",
            "情境适配 - 根据情境选择最适合的智慧",
            "层次递进 - 从入世到出世,从修身到修心",
            "和而不同 - 尊重差异,寻求共识",
            "因时制宜 - 根据时代需求调整重点",
            "因地制宜 - 根据具体情况灵活运用"
        ]
    
    def analyze_situation(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析decision情境
        
        Args:
            situation: 情境描述
            
        Returns:
            情境分析结果
        """
        analysis = {
            "domain": None,
            "level": None,
            "urgency": 0.0,
            "complexity": 0.0,
            "emotional_intensity": 0.0,
            "social_impact": 0.0,
            "long_term_impact": 0.0
        }
        
        # recognize领域
        if situation.get("family_related"):
            analysis["domain"] = LifeDomain.FAMILY
        elif situation.get("career_related"):
            analysis["domain"] = LifeDomain.CAREER
        elif situation.get("social_related"):
            analysis["domain"] = LifeDomain.SOCIAL
        elif situation.get("spiritual_related"):
            analysis["domain"] = LifeDomain.SPIRITUAL
        elif situation.get("health_related"):
            analysis["domain"] = LifeDomain.HEALTH
        else:
            analysis["domain"] = LifeDomain.PERSONAL
        
        # recognize层次
        if situation.get("emergency"):
            analysis["level"] = DecisionLevel.EMERGENCY
        elif situation.get("long_term"):
            analysis["level"] = DecisionLevel.STRATEGIC
        elif situation.get("medium_term"):
            analysis["level"] = DecisionLevel.TACTICAL
        else:
            analysis["level"] = DecisionLevel.OPERATIONAL
        
        # 评估characteristics
        analysis["urgency"] = situation.get("urgency", 0.5)
        analysis["complexity"] = situation.get("complexity", 0.5)
        analysis["emotional_intensity"] = situation.get("emotional_intensity", 0.5)
        analysis["social_impact"] = situation.get("social_impact", 0.5)
        analysis["long_term_impact"] = situation.get("long_term_impact", 0.5)
        
        return analysis
    
    def select_traditions(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        选择适用的智慧传统
        
        Args:
            analysis: 情境分析结果
            
        Returns:
            传统选择结果
        """
        domain = analysis["domain"]
        level = analysis["level"]
        
        # 基于领域选择
        domain_map = self.domain_tradition_map.get(domain, {
            "primary": WisdomTradition.RU,
            "secondary": [WisdomTradition.DAO, WisdomTradition.BUDDHA]
        })
        
        # 基于层次调整
        level_map = self.level_tradition_map.get(level, {
            "primary": WisdomTradition.RU,
            "secondary": [WisdomTradition.DAO]
        })
        
        # synthesize选择
        primary = domain_map["primary"]
        secondary = list(set(domain_map["secondary"] + level_map["secondary"]))
        
        # 计算适用性评分
        suitability_scores = {
            "儒家": 0.0,
            "道家": 0.0,
            "佛家": 0.0
        }
        
        # 儒家适用性
        if analysis["social_impact"] > 0.6:
            suitability_scores["儒家"] += 0.3
        if analysis["domain"] in [LifeDomain.SOCIAL, LifeDomain.CAREER, LifeDomain.FAMILY]:
            suitability_scores["儒家"] += 0.3
        if analysis["level"] in [DecisionLevel.TACTICAL, DecisionLevel.OPERATIONAL]:
            suitability_scores["儒家"] += 0.2
        
        # 道家适用性
        if analysis["long_term_impact"] > 0.6:
            suitability_scores["道家"] += 0.3
        if analysis["level"] == DecisionLevel.STRATEGIC:
            suitability_scores["道家"] += 0.3
        if analysis["urgency"] > 0.7:
            suitability_scores["道家"] += 0.2
        
        # 佛家适用性
        if analysis["emotional_intensity"] > 0.6:
            suitability_scores["佛家"] += 0.3
        if analysis["domain"] == LifeDomain.SPIRITUAL:
            suitability_scores["佛家"] += 0.3
        if analysis["complexity"] > 0.7:
            suitability_scores["佛家"] += 0.2
        
        return {
            "primary": primary,
            "secondary": secondary,
            "suitability_scores": suitability_scores,
            "reasoning": f"基于{domain.value}领域和{level.value}层次,选择{primary.value}为主要智慧传统"
        }
    
    def fuse_wisdom(self, situation: Dict[str, Any], 
                   tradition_selection: Dict[str, Any]) -> Dict[str, Any]:
        """
        fusion三家智慧
        
        Args:
            situation: 情境描述
            tradition_selection: 传统选择结果
            
        Returns:
            fusion后的智慧建议
        """
        # get三家建议
        ru_advice = self._get_ru_advice(situation)
        dao_advice = self._get_dao_advice(situation)
        buddha_advice = self._get_buddha_advice(situation)
        
        # 根据主次整合
        primary = tradition_selection["primary"]
        
        if primary == WisdomTradition.RU:
            integrated = self._integrate_ru_primary(ru_advice, dao_advice, buddha_advice)
        elif primary == WisdomTradition.DAO:
            integrated = self._integrate_dao_primary(dao_advice, ru_advice, buddha_advice)
        else:  # BUDDHA
            integrated = self._integrate_buddha_primary(buddha_advice, ru_advice, dao_advice)
        
        return {
            "ru_advice": ru_advice,
            "dao_advice": dao_advice,
            "buddha_advice": buddha_advice,
            "integrated_advice": integrated["advice"],
            "action_plan": integrated["actions"],
            "key_insight": integrated["insight"]
        }
    
    def _get_ru_advice(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """get儒家建议"""
        return {
            "principle": "仁义礼智信",
            "approach": "积极入世,承担责任",
            "key_value": "以仁爱之心处理人际关系,以礼仪规范行为",
            "action": "修身齐家治国平天下,从自我修养做起",
            "quote": "己欲立而立人,己欲达而达人"
        }
    
    def _get_dao_advice(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """get道家建议"""
        return {
            "principle": "道法自然",
            "approach": "顺应自然,无为而治",
            "key_value": "以柔克刚,以退为进",
            "action": "致虚极,守静笃,顺应事物发展规律",
            "quote": "人法地,地法天,天法道,道法自然"
        }
    
    def _get_buddha_advice(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """get佛家建议"""
        return {
            "principle": "四圣谛八正道",
            "approach": "看破放下,内心解脱",
            "key_value": "慈悲为怀,智慧觉悟",
            "action": "修习正念,断除执着,培养慈悲心",
            "quote": "应无所住而生其心"
        }
    
    def _integrate_ru_primary(self, ru: Dict, dao: Dict, buddha: Dict) -> Dict[str, Any]:
        """以儒家为主整合"""
        return {
            "advice": f"以儒家'{ru['principle']}'为核心,融入道家'{dao['key_value']}'的灵活,借鉴佛家'{buddha['key_value']}'的慈悲",
            "actions": [
                f"1. 儒家:{ru['action']}",
                f"2. 道家:{dao['action']}",
                f"3. 佛家:{buddha['action']}",
                "4. fusion:以仁爱之心积极作为,同时顺应规律,保持内心平静"
            ],
            "insight": "入世担当,顺势而为,内心平和"
        }
    
    def _integrate_dao_primary(self, dao: Dict, ru: Dict, buddha: Dict) -> Dict[str, Any]:
        """以道家为主整合"""
        return {
            "advice": f"以道家'{dao['principle']}'为核心,融入儒家'{ru['key_value']}'的伦理,借鉴佛家'{buddha['key_value']}'的超脱",
            "actions": [
                f"1. 道家:{dao['action']}",
                f"2. 儒家:{ru['action']}",
                f"3. 佛家:{buddha['action']}",
                "4. fusion:顺应自然规律,承担社会责任,保持内心自由"
            ],
            "insight": "道法自然,和而不同,无为而无不为"
        }
    
    def _integrate_buddha_primary(self, buddha: Dict, ru: Dict, dao: Dict) -> Dict[str, Any]:
        """以佛家为主整合"""
        return {
            "advice": f"以佛家'{buddha['principle']}'为核心,融入儒家'{ru['key_value']}'的入世,借鉴道家'{dao['key_value']}'的自然",
            "actions": [
                f"1. 佛家:{buddha['action']}",
                f"2. 儒家:{ru['action']}",
                f"3. 道家:{dao['action']}",
                "4. fusion:以慈悲心入世,以智慧心顺应,以平等心超越"
            ],
            "insight": "悲智双运,随缘不变,内心解脱"
        }
    
    def make_decision(self, situation: Dict[str, Any], 
                     persona: Optional[SanjiaoPersona] = None) -> SanjiaoDecision:
        """
        基于三教合一智慧做出decision
        
        Args:
            situation: decision情境
            persona: 修行者人格(可选)
            
        Returns:
            三教合一decision结果
        """
        if persona is None:
            persona = SanjiaoPersona()
        
        # 分析情境
        analysis = self.analyze_situation(situation)
        
        # 选择传统
        tradition_selection = self.select_traditions(analysis)
        
        # fusion智慧
        fused_wisdom = self.fuse_wisdom(situation, tradition_selection)
        
        # generate警示
        warnings = []
        if analysis["urgency"] > 0.8:
            warnings.append("情况紧急,需冷静应对")
        if analysis["complexity"] > 0.8:
            warnings.append("情况复杂,需synthesize考虑")
        if analysis["emotional_intensity"] > 0.8:
            warnings.append("情绪波动大,需先平静内心")
        
        return SanjiaoDecision(
            primary_tradition=tradition_selection["primary"],
            secondary_traditions=tradition_selection["secondary"],
            domain=analysis["domain"],
            level=analysis["level"],
            ru_advice=fused_wisdom["ru_advice"],
            dao_advice=fused_wisdom["dao_advice"],
            buddha_advice=fused_wisdom["buddha_advice"],
            integrated_advice=fused_wisdom["integrated_advice"],
            action_plan=fused_wisdom["action_plan"],
            suitability_scores=tradition_selection["suitability_scores"],
            confidence=0.85,
            reasoning=tradition_selection["reasoning"],
            warnings=warnings
        )
    
    def get_life_guidance(self, stage: str) -> Dict[str, Any]:
        """
        get人生阶段指导
        
        Args:
            stage: 人生阶段(青年/中年/老年)
            
        Returns:
            三教合一的人生指导
        """
        guidance = {
            "青年": {
                "儒家": "修身齐家,立志向学,积极进取",
                "道家": "顺应自然,不急于求成,保持谦逊",
                "佛家": "培养正念,减少欲望,积累善业",
                "fusion": "以儒家进取精神立业,以道家谦逊态度处世,以佛家正念修心"
            },
            "中年": {
                "儒家": "治国平天下,承担社会责任,传承文化",
                "道家": "知止不殆,功成身退,保持平衡",
                "佛家": "看破名利,减少执着,培养慈悲",
                "fusion": "以儒家担当精神做事,以道家平衡智慧处世,以佛家慈悲心怀人"
            },
            "老年": {
                "儒家": "传承智慧,教育后人,完成人生使命",
                "道家": "返璞归真,顺应生死,与自然合一",
                "佛家": "放下一切,内心解脱,往生净土",
                "fusion": "以儒家传承精神育人,以道家自然态度面对生死,以佛家解脱智慧超越"
            }
        }
        return guidance.get(stage, guidance["中年"])
    
    def get_wisdom_by_topic(self, topic: str) -> Dict[str, str]:
        """
        按主题get三家智慧
        
        Args:
            topic: 主题
            
        Returns:
            三家智慧
        """
        wisdom_map = {
            "成功": {
                "儒家": "修身齐家治国平天下,内圣外王",
                "道家": "无为而无不为,功成身退",
                "佛家": "应无所住而生其心,不执着于成功"
            },
            "人际关系": {
                "儒家": "己所不欲,勿施于人;仁者爱人",
                "道家": "上善若水,水利万物而不争",
                "佛家": "慈悲喜舍,平等看待一切众生"
            },
            "压力": {
                "儒家": "天将降大任于斯人也,必先苦其心志",
                "道家": "致虚极,守静笃,顺应自然",
                "佛家": "一切有为法,如梦幻泡影,看破放下"
            },
            "decision": {
                "儒家": "三思而后行,谋定而后动",
                "道家": "以正治国,以奇用兵,顺势而为",
                "佛家": "正见为首,如目导行,智慧decision"
            },
            "修养": {
                "儒家": "吾日三省吾身,修身齐家",
                "道家": "致虚极,守静笃,返璞归真",
                "佛家": "诸恶莫作,众善奉行,自净其意"
            }
        }
        return wisdom_map.get(topic, {
            "儒家": "仁义礼智信",
            "道家": "道法自然",
            "佛家": "慈悲智慧"
        })
    
    def cultivate_three_in_one(self) -> Dict[str, Any]:
        """
        三教合一修行指南
        
        Returns:
            修行指南
        """
        return {
            "核心理念": "以儒治世,以道治身,以佛治心",
            "修行次第": [
                "1. 儒家基础 - 修身齐家,建立伦理基础",
                "2. 道家进阶 - 顺应自然,提升生命境界",
                "3. 佛家圆满 - 内心解脱,达到智慧圆满"
            ],
            "日常实践": {
                "早晨": "儒家 - 立志向学,规划一天",
                "白天": "儒家 - 积极作为,承担责任",
                "傍晚": "道家 - 顺应自然,保持平衡",
                "夜晚": "佛家 - 反思修行,培养正念"
            },
            "终极目标": "内圣外王,道法自然,涅槃解脱"
        }

# ============================================================
# 使用示例
# ============================================================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
