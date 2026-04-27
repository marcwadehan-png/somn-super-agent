# -*- coding: utf-8 -*-
"""
__all__ = [
    'evaluate_action',
    'get_classic_guidance',
    'get_path',
    'get_ru_core',
    'get_three_guides',
    'make_decision',
]

儒家智慧核心 v1.0.1 (兼容版)
Ru Wisdom Core - Simplified Compatible Version

版本:v1.0.1
更新:2026-04-03
说明:从 ru_wisdom_unified.py 提取的核心类,恢复 ru_wisdom_core 接口兼容

由于 ru_wisdom_core 被删除后导致依赖链断裂,创建此兼容版本.
核心功能已迁移至 ru_wisdom_unified.py,此文件仅用于向后兼容.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class ConfucianClassic(Enum):
    """儒家经典"""
    ANALECTS = "论语"          # 孔子言行
    MENCIUS = "孟子"           # 仁政王道
    GREAT_LEARNING = "大学"    # 修身齐家
    DOCTRINE_MEAN = "中庸"     # 中庸之道
    BOOK_OF_DOCUMENTS = "尚书"  # 圣王治国
    BOOK_OF_SONGS = "诗经"     # 诗教
    BOOK_OF_RITES = "礼记"     # 礼乐
    BOOK_OF_CHANGES = "易经"   # 变易
    CLASSIC_PIETY = "孝经"     # 孝道
    SPRING_AUTUMN = "春秋"     # 褒贬

class FiveChang(Enum):
    """五常"""
    REN = "仁"    # 仁爱
    YI = "义"    # 正义
    LI = "礼"    # 礼仪
    ZHI = "智"    # 智慧
    XIN = "信"    # 诚信

class GreatLearning:
    """
    大学之道
    止于至善 - 目标
    定静安虑得 - 方法
    """
    
    @staticmethod
    def get_path(stage: str) -> str:
        paths = {
            "know": "知止而后有定",
            "settle": "定而后能静",
            "calm": "静而后能安",
            "peace": "安而后能虑",
            "attain": "虑而后能得"
        }
        return paths.get(stage, "")
    
    @staticmethod
    def get_three_guides() -> Dict[str, str]:
        return {
            "格物": "穷究事物之理",
            "致知": "获得知识智慧",
            "诚意": "意念真诚不欺",
            "正心": "心态端正不偏",
            "修身": "修养自身品德",
            "齐家": "治理家庭伦理",
            "治国": "治理邦国政务",
            "平天下": "平定天下苍生"
        }

@dataclass
class ConfucianDecision:
    """儒家decision结构"""
    classic: ConfucianClassic
    principle: str
    reasoning: str
    action: str
    warnings: List[str] = field(default_factory=list)
    expected_outcome: str = ""
    confidence: float = 0.8
    fivechang_scores: Dict[str, float] = field(default_factory=dict)

@dataclass  
class ConfucianPersona:
    """儒家人格"""
    ren_level: float = 0.5   # 仁
    yi_level: float = 0.5    # 义
    li_level: float = 0.5    # 礼
    zhi_level: float = 0.5   # 智
    xin_level: float = 0.5   # 信
    learning_level: float = 0.5  # 学
    self_cultivation: float = 0.5  # 修身
    

class RuWisdomCore:
    """
    儒家智慧核心
    整合十经五常,提供儒学智慧支持
    """
    
    def __init__(self):
        self.name = "儒家智慧核心"
        self.version = "1.0.1"
        self.classics = [c.value for c in ConfucianClassic]
        
    def get_classic_guidance(self, classic: ConfucianClassic, situation: str) -> Dict[str, Any]:
        """get经典指导"""
        guidance_map = {
            ConfucianClassic.ANALECTS: {
                "core": "仁",
                "key_quote": "己欲立而立人,己欲达而达人",
                "method": "忠恕之道"
            },
            ConfucianClassic.MENCIUS: {
                "core": "义",
                "key_quote": "舍生取义",
                "method": "反求诸己"
            },
            ConfucianClassic.GREAT_LEARNING: {
                "core": "修身",
                "key_quote": "自天子以至于庶人,壹是皆以修身为本",
                "method": "格物致知"
            },
            ConfucianClassic.DOCTRINE_MEAN: {
                "core": "中",
                "key_quote": "不偏之谓中,不易之谓庸",
                "method": "执两用中"
            }
        }
        return guidance_map.get(classic, {"core": "儒", "key_quote": "仁义礼智", "method": "修身"})
    
    def evaluate_action(self, action: str, context: Dict) -> ConfucianDecision:
        """评估action"""
        classic = ConfucianClassic.ANALECTS
        return ConfucianDecision(
            classic=classic,
            principle="仁义礼智信",
            reasoning="以儒家五常为标准评估",
            action=action,
            expected_outcome="符合儒学道德标准"
        )
    
    def make_decision(self, situation: Dict) -> ConfucianDecision:
        """儒家decision"""
        problem = situation.get("problem", "")
        
        if "仁" in problem or "爱" in problem:
            return self._ren_decision(situation)
        elif "义" in problem or "正" in problem:
            return self._yi_decision(situation)
        elif "礼" in problem or "规范" in problem:
            return self._li_decision(situation)
        else:
            return self._general_decision(situation)
    
    def _ren_decision(self, situation: Dict) -> ConfucianDecision:
        return ConfucianDecision(
            classic=ConfucianClassic.ANALECTS,
            principle="仁",
            reasoning="孔子曰:仁者爱人.应以仁爱之心待人",
            action="推己及人,己欲立而立人",
            expected_outcome="建立和谐人际关系"
        )
    
    def _yi_decision(self, situation: Dict) -> ConfucianDecision:
        return ConfucianDecision(
            classic=ConfucianClassic.MENCIUS,
            principle="义",
            reasoning="孟子曰:舍生取义.应明辨是非善恶",
            action="义以为上,见利思义",
            expected_outcome="保持正直品格"
        )
    
    def _li_decision(self, situation: Dict) -> ConfucianDecision:
        return ConfucianDecision(
            classic=ConfucianClassic.BOOK_OF_RITES,
            principle="礼",
            reasoning="礼者,天地之序也.应恭敬谨慎",
            action="克己复礼,恭敬不如",
            expected_outcome="建立良好秩序"
        )
    
    def _general_decision(self, situation: Dict) -> ConfucianDecision:
        return ConfucianDecision(
            classic=ConfucianClassic.GREAT_LEARNING,
            principle="修身",
            reasoning="大学之道,在明明德,在亲民,在止于至善",
            action="格物致知,诚意正心",
            expected_outcome="完善自身品德"
        )

# 全局单例
_ru_core_instance = None

def get_ru_core() -> RuWisdomCore:
    """get儒家核心单例"""
    global _ru_core_instance
    if _ru_core_instance is None:
        _ru_core_instance = RuWisdomCore()
    return _ru_core_instance
