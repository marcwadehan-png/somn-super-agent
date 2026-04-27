# -*- coding: utf-8 -*-
"""诗词分析引擎 - 中级分析模块：意象、情感、主题"""
import re
from typing import Dict, List, Any
from collections import Counter

__all__ = [
    'analyze_emotion',
    'analyze_imagery',
    'analyze_theme',
]

class IntermediateAnalyzer:
    """中级分析器：意象、情感、主题"""

    def __init__(self, imagery_library: Dict, theme_library: Dict):
        self.imagery_library = imagery_library
        self.theme_library = theme_library

    # ----- 意象分析 -----

    def analyze_imagery(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词imagery"""
        imagery_results = {
            "natural_imagery": [],
            "human_imagery": [],
            "combined_imagery": []
        }

        for imagery_type, imageries in self.imagery_library.items():
            for imagery_word, info in imageries.items():
                if imagery_word in poem_text:
                    if imagery_type == "自然imagery":
                        imagery_results["natural_imagery"].append({
                            "word": imagery_word,
                            "type": imagery_type,
                            "emotion": info["情感"],
                            "frequency": info["频率"]
                        })
                    elif imagery_type == "人文imagery":
                        imagery_results["human_imagery"].append({
                            "word": imagery_word,
                            "type": imagery_type,
                            "emotion": info["情感"],
                            "frequency": info.get("frequency", 0.5)
                        })

        imagery_results["combined_imagery"] = self._analyze_imagery_combination(
            imagery_results["natural_imagery"],
            imagery_results["human_imagery"]
        )

        total_imagery = len(imagery_results["natural_imagery"]) + len(imagery_results["human_imagery"])
        total_words = len(re.findall(r'[\u4e00-\u9fff]+', poem_text))
        imagery_results["imagery_density"] = total_imagery / total_words if total_words > 0 else 0

        return imagery_results

    def _analyze_imagery_combination(self, natural_imagery: List[Dict], human_imagery: List[Dict]) -> List[Dict]:
        """分析imagery组合"""
        combinations = []

        for natural in natural_imagery[:3]:
            for human in human_imagery[:3]:
                common_emotions = set(natural["emotion"]) & set(human["emotion"])
                if common_emotions:
                    combinations.append({
                        "natural": natural["word"],
                        "human": human["word"],
                        "common_emotions": list(common_emotions),
                        "combination_strength": len(common_emotions) / max(len(natural["emotion"]), len(human["emotion"]))
                    })

        return combinations

    # ----- 情感分析 -----

    def analyze_emotion(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词情感"""
        emotion_keywords = {
            "喜悦": ["喜", "乐", "欢", "笑", "欣"],
            "忧愁": ["愁", "忧", "悲", "哀", "伤"],
            "豪迈": ["豪", "壮", "雄", "刚", "猛"],
            "思念": ["思", "念", "怀", "想", "忆"],
            "孤独": ["孤", "独", "寂", "寞", "寥"],
            "闲适": ["闲", "适", "悠", "淡", "静"]
        }

        emotion_counts = {emotion: 0 for emotion in emotion_keywords}

        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                emotion_counts[emotion] += poem_text.count(keyword)

        total_emotion_words = sum(emotion_counts.values())
        emotion_intensity = {}

        for emotion, count in emotion_counts.items():
            if total_emotion_words > 0:
                intensity = count / total_emotion_words
            else:
                intensity = 0

            emotion_intensity[emotion] = {
                "count": count,
                "intensity": intensity,
                "level": self._get_emotion_level(intensity)
            }

        main_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if total_emotion_words > 0 else "中性"

        return {
            "emotion_distribution": emotion_intensity,
            "main_emotion": main_emotion,
            "emotion_complexity": len([e for e in emotion_counts.values() if e > 0]) / len(emotion_counts)
        }

    def _get_emotion_level(self, intensity: float) -> str:
        """get情感强度等级"""
        if intensity == 0:
            return "无"
        elif intensity < 0.1:
            return "微弱"
        elif intensity < 0.3:
            return "中等"
        elif intensity < 0.5:
            return "强烈"
        else:
            return "极强烈"

    # ----- 主题分析 -----

    def analyze_theme(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词主题"""
        theme_scores = {}

        for theme, keywords in self.theme_library.items():
            score = 0
            for keyword in keywords:
                score += poem_text.count(keyword) * 2

            theme_scores[theme] = {
                "score": score,
                "keywords_found": [kw for kw in keywords if kw in poem_text]
            }

        main_theme = max(theme_scores.items(), key=lambda x: x[1]["score"])[0] if theme_scores else "其他"

        return {
            "theme_scores": theme_scores,
            "main_theme": main_theme,
            "theme_purity": self._calculate_theme_purity(theme_scores)
        }

    def _calculate_theme_purity(self, theme_scores: Dict[str, Dict]) -> float:
        """计算主题纯度"""
        total_score = sum(theme["score"] for theme in theme_scores.values())
        if total_score == 0:
            return 0

        max_score = max(theme["score"] for theme in theme_scores.values())
        return max_score / total_score
