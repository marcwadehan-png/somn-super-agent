"""
__all__ = [
    'to_dict',
]

叙事智能引擎 - 类型定义
拆分自 narrative_intelligence_engine.py
"""
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class NarrativeMode(Enum):
    """叙事模式 - 路遥式 vs 莫言式"""
    LINEAR_ASCENT = "linear_ascent"           # 路遥式线性上升叙事
    CIRCULAR_DESTINY = "circular_destiny"     # 莫言式循环宿命叙事
    MULTI_VOICE = "multi_voice"               # 莫言式多声部叙事
    REALIST_WARMTH = "realist_warmth"         # 路遥式温情现实主义
    GROTESQUE_TRUTH = "grotesque_truth"       # 莫言式荒诞真实主义
    DUAL_LIGHT_DARK = "dual_light_dark"       # 光暗交织 - synthesize两种传统

class NarrativeElementType(Enum):
    """叙事元素类型"""
    PROTAGONIST = "protagonist"      # 主角/核心角色
    CONFLICT = "conflict"            # 冲突/矛盾
    TURNING_POINT = "turning_point"  # 转折点
    CLIMAX = "climax"                # 高潮
    RESOLUTION = "resolution"        # 解决
    SETTING = "setting"              # 场景/环境
    THEME = "theme"                  # 主题
    SYMBOL = "symbol"                # 象征
    SUFFERING = "suffering"          # 苦难
    ASCENT = "ascent"                # 奋斗/上升
    ABSURDITY = "absurdity"          # 荒诞

class EmotionalTone(Enum):
    """情感基调"""
    HOPE = "hope"                    # 希望(路遥主调)
    DESPAIR = "despair"              # 绝望
    STRUGGLE = "struggle"            # 奋斗(路遥核心)
    IRONY = "irony"                  # 讽刺(莫言常见)
    WARMTH = "warmth"                # 温情(路遥characteristics)
    CRUELTY = "cruelty"              # 残酷(莫言characteristics)
    REBELLION = "rebellion"          # 反抗
    RESIGNATION = "resignation"      # 认命
    SUBVERSION = "subversion"        # 颠覆(莫言characteristics)
    ELEVATION = "elevation"          # 升华(路遥characteristics)

@dataclass
class NarrativeElement:
    """叙事元素"""
    id: str
    element_type: NarrativeElementType
    content: str
    emotional_tone: EmotionalTone
    importance: float = 0.8  # 重要性 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "element_type": self.element_type.value,
            "content": self.content,
            "emotional_tone": self.emotional_tone.value,
            "importance": self.importance,
            "metadata": self.metadata
        }

@dataclass
class NarrativeStructure:
    """叙事结构"""
    mode: NarrativeMode
    elements: List[NarrativeElement]
    title: str = ""
    theme: str = ""
    arc_type: str = "rise"  # rise/fall/rise_fall/circular
    emotional_curve: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "mode": self.mode.value,
            "title": self.title,
            "theme": self.theme,
            "arc_type": self.arc_type,
            "elements": [e.to_dict() for e in self.elements],
            "emotional_curve": self.emotional_curve
        }

@dataclass
class NarrativeAnalysis:
    """叙事分析结果"""
    analysis_id: str
    analysis_type: str
    narrative_structure: NarrativeStructure
    insights: List[str]
    recommendations: List[str]
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "analysis_id": self.analysis_id,
            "analysis_type": self.analysis_type,
            "narrative_structure": self.narrative_structure.to_dict(),
            "insights": self.insights,
            "recommendations": self.recommendations,
            "confidence": self.confidence,
            "created_at": self.created_at
        }

# ============================================================
# 核心分析器
# ============================================================

