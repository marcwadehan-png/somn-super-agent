"""
__all__ = [
    'analyze_narrative_structure',
    'assess_narrative_quality',
    'build_persona_depth',
    'compute_emotional_resonance',
    'diagnose_dilemma',
    'generate_growth_narrative',
    'generate_story_elements',
    'generate_turning_point',
]

Narrative Intelligence Engine - 叙事智能引擎 (v6.0 兼容层)
fusion莫言,路遥文学叙事结构的多维度分析能力

版本: v6.0.0
创建: 2026-03-31
拆分: 2026-04-07
拆分后子模块:
  _nie_types.py   - 枚举/数据类
  _nie_analyzer.py - 增长叙事分析器
  _nie_persona.py  - 人物画像构建器
  _nie_advisor.py  - 故事驱动增长顾问
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# ── 子模块类（延迟导入）──────────────────────────────────
_nie_types_module     = None
_nie_analyzer_module  = None
_nie_persona_module   = None
_nie_advisor_module   = None

def _lazy_import():
    global _nie_types_module, _nie_analyzer_module, _nie_persona_module, _nie_advisor_module
    if _nie_types_module is None:
        from . import _nie_types
        from . import _nie_analyzer
        from . import _nie_persona
        from . import _nie_advisor
        _nie_types_module    = _nie_types
        _nie_analyzer_module = _nie_analyzer
        _nie_persona_module  = _nie_persona
        _nie_advisor_module  = _nie_advisor

# ── Re-export 所有公共符号（兼容旧导入路径）───────────────
def __getattr__(name):
    _lazy_import()
    for m in [_nie_types_module, _nie_analyzer_module,
              _nie_persona_module, _nie_advisor_module]:
        if hasattr(m, name):
            return getattr(m, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# ── 枚举/数据类直接引用 ──────────────────────────────────
from ._nie_types import (
    NarrativeMode,
    NarrativeElementType,
    EmotionalTone,
    NarrativeElement,
    NarrativeStructure,
    NarrativeAnalysis,
)

# ── 主门面类 ─────────────────────────────────────────────
from ._nie_analyzer   import GrowthNarrativeAnalyzer
from ._nie_persona    import PersonaDepthBuilder
from ._nie_advisor    import StoryDrivenGrowthAdvisor

class NarrativeIntelligenceEngine:
    """
    叙事智能引擎 - 门面类 (Facade)
    协调 GrowthNarrativeAnalyzer / PersonaDepthBuilder / StoryDrivenGrowthAdvisor
    """

    def __init__(self):
        self.analyzer  = GrowthNarrativeAnalyzer()
        self.builder   = PersonaDepthBuilder()
        self.advisor   = StoryDrivenGrowthAdvisor()

    def analyze_narrative_structure(
        self, description: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """分析叙事结构"""
        result = self.analyzer.analyze_growth_narrative(
            business_context={"description": description, **(context or {})}
        )
        return result.to_dict() if hasattr(result, "to_dict") else result

    def build_persona_depth(
        self, user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """构建人物画像"""
        return self.builder.build_deep_persona(basic_persona=user_profile)

    def generate_growth_narrative(
        self, strategy: Dict[str, Any],
        user_profile: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """生成增长叙事"""
        personas = [user_profile] if user_profile else []
        return self.advisor.generate_story_strategy(
            business_context={"strategy": strategy, "personas": personas}
        )

    def diagnose_dilemma(
        self, problem_description: str
    ) -> Dict[str, Any]:
        """困境诊断（路遥苦难意识+莫言荒诞视角）"""
        result = self.analyzer.analyze_growth_narrative(
            business_context={"description": problem_description, "dilemma_mode": True}
        )
        return result.to_dict() if hasattr(result, "to_dict") else result

    def generate_turning_point(
        self, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """转折点设计"""
        analysis = self.analyzer.analyze_growth_narrative(
            business_context=context if isinstance(context, dict) and "description" in context else {"description": str(context)}
        )
        title = analysis.narrative_title if hasattr(analysis, "narrative_title") else "转折时刻"
        return {
            "turning_point": title,
            "analysis": analysis.to_dict() if hasattr(analysis, "to_dict") else analysis,
        }

    def generate_story_elements(
        self, theme: str,
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """生成叙事元素"""
        analysis = self.analyzer.analyze_growth_narrative(
            business_context={"description": theme, "theme_mode": True}
        )
        title = analysis.narrative_title if hasattr(analysis, "narrative_title") else f"{theme}叙事"
        return [
            {"element": title, "type": "theme"} for _ in range(count)
        ]

    def compute_emotional_resonance(
        self, content: str,
        target_profile: Dict[str, Any]
    ) -> float:
        """情感共鸣计算"""
        analysis = self.analyzer.analyze_growth_narrative(
            business_context={"description": content}
        )
        confidence = analysis.confidence if hasattr(analysis, "confidence") else 0.5
        emotional_alignment = target_profile.get("emotional_preference", "") in content
        return min(1.0, confidence + (0.2 if emotional_alignment else 0.0))

    def assess_narrative_quality(
        self, narrative: Dict[str, Any]
    ) -> Dict[str, Any]:
        """叙事质量评估"""
        content = narrative.get("content", "")
        structure_score = 0.5 if narrative.get("structure") else 0.3
        confidence = len(content) / 1000.0 if content else 0.0
        return {
            "quality_score": min(1.0, structure_score + confidence),
            "structure_score": structure_score,
            "confidence": confidence,
        }
