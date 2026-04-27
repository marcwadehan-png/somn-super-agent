# -*- coding: utf-8 -*-
"""诗词分析引擎 - 比较模块：诗词比较分析"""
from typing import Dict, List, Any
from ._pae_types import PoetryAnalysisResult

__all__ = [
    'compare_poems',
]

class PoetryComparator:
    """诗词比较器"""

    def compare_poems(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> Dict[str, Any]:
        """比较两首诗词"""
        comparison = {
            "basic_comparison": self._compare_basic_features(poem1, poem2),
            "style_comparison": self._compare_styles(poem1, poem2),
            "similarity_score": self._calculate_similarity_score(poem1, poem2),
            "influence_relationship": self._assess_influence_relationship(poem1, poem2)
        }

        return comparison

    def _compare_basic_features(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> Dict[str, Any]:
        """比较基础characteristics"""
        return {
            "line_count_difference": abs(
                poem1.basic_analysis.get("structure", {}).get("total_lines", 0) -
                poem2.basic_analysis.get("structure", {}).get("total_lines", 0)
            ),
            "avg_length_difference": abs(
                poem1.basic_analysis.get("structure", {}).get("avg_line_length", 0) -
                poem2.basic_analysis.get("structure", {}).get("avg_line_length", 0)
            ),
            "rhyme_pattern_similarity": self._compare_rhyme_patterns(poem1, poem2)
        }

    def _compare_rhyme_patterns(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> float:
        """比较韵律模式"""
        return 0.5

    def _compare_styles(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> Dict[str, Any]:
        """比较style"""
        style1 = poem1.advanced_analysis.get("style", {}) if poem1.advanced_analysis else {}
        style2 = poem2.advanced_analysis.get("style", {}) if poem2.advanced_analysis else {}

        return {
            "style_similarity": self._calculate_style_similarity(style1, style2),
            "common_features": self._find_common_style_features(style1, style2)
        }

    def _calculate_style_similarity(self, style1: Dict, style2: Dict) -> float:
        """计算style相似度"""
        if not style1 or not style2:
            return 0.5

        style1_type = style1.get("detected_style", "")
        style2_type = style2.get("detected_style", "")

        return 1.0 if style1_type == style2_type else 0.3

    def _find_common_style_features(self, style1: Dict, style2: Dict) -> List[str]:
        """寻找共同style_features"""
        return []

    def _calculate_similarity_score(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> float:
        """计算相似度评分"""
        basic_similarity = 1.0 - (self._compare_basic_features(poem1, poem2)["line_count_difference"] / 50)
        style_similarity = self._compare_styles(poem1, poem2)["style_similarity"]

        return (basic_similarity + style_similarity) / 2.0

    def _assess_influence_relationship(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> Dict[str, Any]:
        """评估影响关系"""
        return {
            "possible_influence": self._check_possible_influence(poem1, poem2),
            "influence_direction": self._determine_influence_direction(poem1, poem2),
            "influence_strength": 0.5
        }

    def _check_possible_influence(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> bool:
        """检查可能的直接影响"""
        return False

    def _determine_influence_direction(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> str:
        """确定影响方向"""
        if "唐代" in poem1.dynasty and "宋代" in poem2.dynasty:
            return "poem1→poem2"
        elif "宋代" in poem1.dynasty and "唐代" in poem2.dynasty:
            return "poem2→poem1"
        else:
            return "未知"
