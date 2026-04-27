# -*- coding: utf-8 -*-
"""诗词分析引擎 - 基础分析模块：韵律、结构、语言"""
import re
import numpy as np
from typing import Dict, List, Any

__all__ = [
    'analyze_language',
    'analyze_rhyme',
    'analyze_structure',
]

class BasicAnalyzer:
    """基础分析器：韵律、结构、语言"""

    def __init__(self, rhyme_rules: Dict[str, List[str]]):
        self.rhyme_rules = rhyme_rules

    # ----- 韵律分析 -----

    def analyze_rhyme(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词韵律"""
        lines = poem_text.strip().split('\n')
        rhyme_scheme = []

        for line in lines:
            if line.strip():
                last_char = line.strip()[-1]
                rhyme_scheme.append(last_char)

        rhyme_pattern = self._detect_rhyme_pattern(rhyme_scheme)

        return {
            "rhyme_scheme": rhyme_scheme,
            "rhyme_pattern": rhyme_pattern,
            "lines_count": len(lines),
            "characters_count": sum(len(line) for line in lines)
        }

    def _detect_rhyme_pattern(self, rhyme_scheme: List[str]) -> str:
        """检测押韵模式"""
        if len(rhyme_scheme) < 2:
            return "单行无韵"

        unique_chars = set(rhyme_scheme)
        if len(unique_chars) == 1:
            return "一韵到底"
        elif len(unique_chars) == 2:
            return "双韵交替"
        else:
            return "多韵变换"

    # ----- 结构分析 -----

    def analyze_structure(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词结构"""
        lines = poem_text.strip().split('\n')

        line_lengths = [len(line.strip()) for line in lines if line.strip()]

        structure_features = {
            "total_lines": len(lines),
            "avg_line_length": np.mean(line_lengths) if line_lengths else 0,
            "std_line_length": np.std(line_lengths) if len(line_lengths) > 1 else 0,
            "max_line_length": max(line_lengths) if line_lengths else 0,
            "min_line_length": min(line_lengths) if line_lengths else 0,
            "line_length_variation": len(set(line_lengths)) / len(line_lengths) if line_lengths else 0
        }

        structure_features["poem_type"] = self._identify_poem_type(lines, line_lengths)

        return structure_features

    def _identify_poem_type(self, lines: List[str], line_lengths: List[int]) -> str:
        """recognize诗体"""
        if len(lines) == 4 and all(5 <= length <= 7 for length in line_lengths):
            return "五言绝句" if all(length == 5 for length in line_lengths) else "七言绝句"
        elif len(lines) == 8 and all(5 <= length <= 7 for length in line_lengths):
            return "五言律诗" if all(length == 5 for length in line_lengths) else "七言律诗"
        elif any(len(line.strip().split()) > 2 for line in lines):
            return "词"
        else:
            return "古体诗"

    # ----- 语言分析 -----

    def analyze_language(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词语言characteristics"""
        from collections import Counter

        words = re.findall(r'[\u4e00-\u9fff]+', poem_text)
        word_freq = Counter(words)

        language_features = {
            "total_words": len(words),
            "unique_words": len(word_freq),
            "lexical_diversity": len(word_freq) / len(words) if words else 0,
            "most_common_words": word_freq.most_common(10),
            "classical_words_count": self._count_classical_words(words)
        }

        return language_features

    def _count_classical_words(self, words: List[str]) -> int:
        """统计文言词汇数量"""
        classical_words = {"之", "乎", "者", "也", "矣", "焉", "哉", "兮", "尔", "汝"}
        return sum(1 for word in words if word in classical_words)
