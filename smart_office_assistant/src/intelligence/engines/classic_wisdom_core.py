# -*- coding: utf-8 -*-
"""ClassicWisdomCore - 兼容层

重构后主文件仅保留向后兼容导入。
子模块: _cwc_types / _cwc_sanguo / _cwc_shuihu / _cwc_xiyou / _cwc_honglou
       _cwc_analyzer / _cwc_team / _cwc_relations
"""

from typing import Dict, Any, Optional

from ._cwc_analyzer import (
    ClassicWisdomEngine,
)

# 单例获取函数
_SINGLETON = None

def get_classic_wisdom_engine():
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = ClassicWisdomEngine()
    return _SINGLETON

def analyze_with_classic_wisdom(situation: str) -> Dict[str, Any]:
    return get_classic_wisdom_engine().analyze_situation(situation)

def get_strategic_advice(context: Dict[str, Any]) -> Dict[str, Any]:
    return get_classic_wisdom_engine().make_strategic_decision(context)

def explain_topic(topic: str) -> Dict[str, Any]:
    return get_classic_wisdom_engine().analyze_situation(topic)

def get_wisdom_by_book(book: str, theme: Optional[str] = None) -> Dict[str, Any]:
    return get_classic_wisdom_engine().analyze_situation(
        theme or "general"
    )

def get_quote(book: str) -> Dict[str, Any]:
    engine = get_classic_wisdom_engine()
    wisdom_map = {
        "sanguo": engine.sanguo_wisdom,
        "shuihu": engine.shuihu_wisdom,
        "xiyou": engine.xiyou_wisdom,
        "honglou": engine.honglou_wisdom,
    }
    kb = wisdom_map.get(book.lower())
    if not kb:
        return {"quote": "", "author": "", "book": ""}
    keys = list(kb.keys())
    if not keys:
        return {"quote": "", "author": "", "book": ""}
    import random
    key = random.choice(keys)
    return {
        "quote": key,
        "author": book.title(),
        "book": book,
    }

def compare_and_recommend(book1: str, book2: str) -> Dict[str, Any]:
    return {
        "book1": book1,
        "book2": book2,
        "recommendation": "各有所长，建议结合使用",
    }

def explain_wisdom(book: str, topic: str) -> Dict[str, Any]:
    return analyze_with_classic_wisdom(topic)

ClassicWisdomCore = ClassicWisdomEngine
ClassicStrategy = None

__all__ = [
    "ClassicWisdomEngine", "ClassicWisdomCore", "ClassicStrategy",
    "get_classic_wisdom_engine", "analyze_with_classic_wisdom",
    "get_strategic_advice", "explain_topic",
    "get_wisdom_by_book", "get_quote",
    "compare_and_recommend", "explain_wisdom",
]
