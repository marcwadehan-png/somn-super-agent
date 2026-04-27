# -*- coding: utf-8 -*-
"""诗词分析引擎 - 高级分析模块：风格、影响、创新性"""
import re
import numpy as np
from typing import Dict, List, Any

__all__ = [
    'analyze_influence',
    'analyze_innovation',
    'analyze_style',
]

class AdvancedAnalyzer:
    """高级分析器：风格、影响、创新性"""

    def __init__(self, author_style_library: Dict, imagery_library: Dict):
        self.author_style_library = author_style_library
        self.imagery_library = imagery_library

    # ----- 风格分析 -----

    def analyze_style(self, poem_text: str, author: str) -> Dict[str, Any]:
        """分析诗词style"""
        author_style = self.author_style_library.get(author, {})

        style_features = {
            "author_known_style": author_style.get("style", "未知"),
            "detected_style": self._detect_style_from_text(poem_text),
            "style_consistency": self._calculate_style_consistency(poem_text, author_style),
            "stylistic_features": self._extract_stylistic_features(poem_text)
        }

        return style_features

    def _detect_style_from_text(self, poem_text: str) -> str:
        """从文本中检测style"""
        if any(word in poem_text for word in ["豪", "壮", "雄", "刚"]):
            return "豪放"
        elif any(word in poem_text for word in ["婉", "柔", "细", "愁"]):
            return "婉约"
        elif any(word in poem_text for word in ["清", "淡", "雅", "静"]):
            return "清新"
        else:
            return "多样"

    def _calculate_style_consistency(self, poem_text: str, author_style: Dict) -> float:
        """计算style一致性"""
        if not author_style:
            return 0.5

        preferred_imagery = author_style.get("imagery_preference", [])
        if not preferred_imagery:
            return 0.5

        found_count = sum(1 for imagery in preferred_imagery if imagery in poem_text)
        return found_count / len(preferred_imagery)

    def _extract_stylistic_features(self, poem_text: str) -> Dict[str, Any]:
        """提取style_features"""
        return {
            "sentence_length_variation": self._calculate_sentence_length_variation(poem_text),
            "classical_word_ratio": self._calculate_classical_word_ratio(poem_text),
            "imagery_concentration": self._calculate_imagery_concentration(poem_text),
            "emotional_intensity_variation": self._calculate_emotional_variation(poem_text)
        }

    def _calculate_sentence_length_variation(self, poem_text: str) -> float:
        """计算句子长度变化"""
        lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
        lengths = [len(line) for line in lines]
        if len(lengths) < 2:
            return 0
        return np.std(lengths) / np.mean(lengths)

    def _calculate_classical_word_ratio(self, poem_text: str) -> float:
        """计算文言词汇比例"""
        words = re.findall(r'[\u4e00-\u9fff]+', poem_text)
        if not words:
            return 0

        classical_words = {"之", "乎", "者", "也", "矣", "焉", "哉", "兮"}
        classical_count = sum(1 for word in words if word in classical_words)
        return classical_count / len(words)

    def _calculate_imagery_concentration(self, poem_text: str) -> float:
        """计算imagery集中度"""
        all_imagery = []
        for imageries in self.imagery_library.values():
            for imagery_word in imageries.keys():
                if imagery_word in poem_text:
                    all_imagery.append(imagery_word)

        unique_imagery = len(set(all_imagery))
        total_words = len(re.findall(r'[\u4e00-\u9fff]+', poem_text))

        return unique_imagery / total_words if total_words > 0 else 0

    def _calculate_emotional_variation(self, poem_text: str) -> float:
        """计算情感变化"""
        return 0.5

    # ----- 影响分析 -----

    def analyze_influence(self, poem_text: str, author: str) -> Dict[str, Any]:
        """分析诗词影响"""
        return {
            "potential_influences": self._find_potential_influences(poem_text, author),
            "influence_scope": self._estimate_influence_scope(author),
            "historical_significance": self._assess_historical_significance(author)
        }

    def _find_potential_influences(self, poem_text: str, author: str) -> List[str]:
        """寻找潜在影响源"""
        tang_authors = ["李白", "杜甫", "王维"]
        song_authors = ["苏轼", "辛弃疾", "李清照"]

        if author in tang_authors:
            return ["汉魏诗歌", "六朝诗风"]
        elif author in song_authors:
            return ["唐代诗歌", "五代词风"]
        else:
            return ["传统诗歌"]

    def _estimate_influence_scope(self, author: str) -> str:
        """估计影响范围"""
        major_authors = ["李白", "杜甫", "苏轼", "辛弃疾", "李清照"]
        if author in major_authors:
            return "全国性影响"
        else:
            return "区域性影响"

    def _assess_historical_significance(self, author: str) -> float:
        """评估历史意义"""
        significance_scores = {
            "李白": 0.95, "杜甫": 0.96, "王维": 0.85,
            "苏轼": 0.92, "辛弃疾": 0.88, "李清照": 0.90
        }
        return significance_scores.get(author, 0.7)

    # ----- 创新性分析 -----

    def analyze_innovation(self, poem_text: str, author: str) -> Dict[str, Any]:
        """分析诗词创新性"""
        return {
            "form_innovation": self._assess_form_innovation(poem_text),
            "language_innovation": self._assess_language_innovation(poem_text),
            "theme_innovation": self._assess_theme_innovation(poem_text),
            "overall_innovation_score": self._calculate_overall_innovation(poem_text, author)
        }

    def _assess_form_innovation(self, poem_text: str) -> float:
        """评估形式创新"""
        lines = poem_text.strip().split('\n')
        if len(lines) > 8:
            return 0.7
        else:
            return 0.5

    def _assess_language_innovation(self, poem_text: str) -> float:
        """评估语言创新"""
        unique_phrases = self._find_unique_phrases(poem_text)
        return min(len(unique_phrases) * 0.2, 0.9)

    def _find_unique_phrases(self, poem_text: str) -> List[str]:
        """寻找独特表达"""
        return []

    def _assess_theme_innovation(self, poem_text: str) -> float:
        """评估主题创新"""
        traditional_themes = ["山水", "田园", "离别", "爱情", "怀古"]
        theme_words = sum(1 for theme in traditional_themes if theme in poem_text)
        return 1.0 - (theme_words / len(traditional_themes))

    def _calculate_overall_innovation(self, poem_text: str, author: str) -> float:
        """计算整体创新性评分"""
        form_score = self._assess_form_innovation(poem_text)
        language_score = self._assess_language_innovation(poem_text)
        theme_score = self._assess_theme_innovation(poem_text)

        return (form_score + language_score + theme_score) / 3.0
