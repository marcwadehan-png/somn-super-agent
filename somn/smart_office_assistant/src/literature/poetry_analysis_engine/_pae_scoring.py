# -*- coding: utf-8 -*-
"""诗词分析引擎 - 评分模块：综合评分"""
from typing import Dict, Any
from ._pae_types import PoetryAnalysisResult

__all__ = [
    'calculate_comprehensive_score',
]

class PoetryScorer:
    """诗词评分器"""

    def calculate_comprehensive_score(self, result: PoetryAnalysisResult) -> Dict[str, float]:
        """计算synthesize评分"""
        scores = {
            "technical_score": self._calculate_technical_score(result),
            "artistic_score": self._calculate_artistic_score(result),
            "influence_score": self._calculate_influence_score(result),
            "overall_score": 0.0
        }

        weights = {"technical": 0.3, "artistic": 0.4, "influence": 0.3}
        scores["overall_score"] = (
            scores["technical_score"] * weights["technical"] +
            scores["artistic_score"] * weights["artistic"] +
            scores["influence_score"] * weights["influence"]
        )

        return scores

    def _calculate_technical_score(self, result: PoetryAnalysisResult) -> float:
        """计算技术评分"""
        rhyme_score = result.basic_analysis.get("rhyme", {}).get("rhyme_pattern_score", 0.5)
        structure_score = result.basic_analysis.get("structure", {}).get("structure_quality", 0.5)
        language_score = result.basic_analysis.get("language", {}).get("language_richness", 0.5)

        return (rhyme_score + structure_score + language_score) / 3.0

    def _calculate_artistic_score(self, result: PoetryAnalysisResult) -> float:
        """计算艺术评分"""
        if not result.intermediate_analysis:
            return 0.5

        imagery_score = result.intermediate_analysis.get("imagery", {}).get("imagery_quality", 0.5)
        emotion_score = result.intermediate_analysis.get("emotion", {}).get("emotional_depth", 0.5)
        theme_score = result.intermediate_analysis.get("theme", {}).get("theme_depth", 0.5)

        return (imagery_score + emotion_score + theme_score) / 3.0

    def _calculate_influence_score(self, result: PoetryAnalysisResult) -> float:
        """计算影响力评分"""
        if not result.advanced_analysis:
            return 0.5

        style_score = result.advanced_analysis.get("style", {}).get("style_significance", 0.5)
        influence_score = result.advanced_analysis.get("influence", {}).get("influence_strength", 0.5)
        innovation_score = result.advanced_analysis.get("innovation", {}).get("overall_innovation_score", 0.5)

        return (style_score + influence_score + innovation_score) / 3.0
