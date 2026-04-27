__all__ = [
    'analyze_situation',
    'compare_and_recommend',
    'explain_wisdom',
    'get_quote',
    'get_wisdom_by_book',
]

# -*- coding: utf-8 -*-
"""ClassicWisdomCore - 兼容层（含全部核心类方法）

此文件为兼容层，实际逻辑委托给子模块。
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from ._cwc_types import (
    WisdomAnalysis,
    SanguoAnalysis,
    ShuihuAnalysis,
    XiyouAnalysis,
    HonglouAnalysis,
    ComprehensiveAdvice,
    BOOK_NAMES,
    THEME_KEYWORDS,
    DEFAULT_THEMES
)
from ._cwc_sanguo import get_sanguo_wisdom
from ._cwc_shuihu import get_shuihu_wisdom
from ._cwc_xiyou import get_xiyou_wisdom
from ._cwc_honglou import get_honglou_wisdom
from ._cwc_analytics import (
    analyze_sanguo,
    analyze_shuihu,
    analyze_xiyou,
    analyze_honglou,
    generate_comprehensive_advice,
    get_wisdom_by_book,
    get_quote,
    compare_and_recommend,
    explain_wisdom
)

class ClassicWisdomEngine:
    """
    四大名著智慧引擎

    将中国古典四大名著的核心智慧转化为可操作的AI决策建议，
    为现代商业决策提供古典智慧的指引。
    """

    def __init__(self):
        """初始化四大名著智慧引擎，加载所有知识库。"""
        self.version = "v1.0.0"
        self.initialized = True
        self._init_sanguo_wisdom()
        self._init_shuihu_wisdom()
        self._init_xiyou_wisdom()
        self._init_honglou_wisdom()

    def _init_sanguo_wisdom(self):
        """初始化三国演义智慧库"""
        self.sanguo_wisdom = get_sanguo_wisdom()

    def _init_shuihu_wisdom(self):
        """初始化水浒传智慧库"""
        self.shuihu_wisdom = get_shuihu_wisdom()

    def _init_xiyou_wisdom(self):
        """初始化西游记智慧库"""
        self.xiyou_wisdom = get_xiyou_wisdom()

    def _init_honglou_wisdom(self):
        """初始化红楼梦智慧库"""
        self.honglou_wisdom = get_honglou_wisdom()

    def analyze_situation(self, situation: str) -> Dict[str, Any]:
        """
        分析给定情形,调用四大名著智慧进行分析

        Args:
            situation: 情形描述

        Returns:
            综合分析结果
        """
        results = {
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "situation": situation,
            "sanguo_analysis": self._analyze_sanguo(situation),
            "shuihu_analysis": self._analyze_shuihu(situation),
            "xiyou_analysis": self._analyze_xiyou(situation),
            "honglou_analysis": self._analyze_honglou(situation),
            "comprehensive_advice": self._generate_comprehensive_advice(situation)
        }
        return results

    def _analyze_sanguo(self, situation: str) -> Dict[str, Any]:
        """三国视角分析"""
        return analyze_sanguo(situation)

    def _analyze_shuihu(self, situation: str) -> Dict[str, Any]:
        """水浒视角分析"""
        return analyze_shuihu(situation)

    def _analyze_xiyou(self, situation: str) -> Dict[str, Any]:
        """西游视角分析"""
        return analyze_xiyou(situation)

    def _analyze_honglou(self, situation: str) -> Dict[str, Any]:
        """红楼视角分析"""
        return analyze_honglou(situation)

    def _generate_comprehensive_advice(self, situation: str) -> Dict[str, Any]:
        """生成综合建议"""
        return generate_comprehensive_advice(situation)

    def get_wisdom_by_book(self, book: str) -> Dict[str, Any]:
        """
        获取特定名著的智慧库

        Args:
            book: "三国"/"水浒"/"西游"/"红楼"

        Returns:
            该名著的智慧库
        """
        return get_wisdom_by_book(book)

    def get_quote(self, book: str, category: str = "core") -> str:
        """
        获取四大名著经典语录

        Args:
            book: "三国"/"水浒"/"西游"/"红楼"
            category: "core"/"leadership"/"wisdom"

        Returns:
            经典语录
        """
        return get_quote(book, category)

    def compare_and_recommend(self, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        使用四大名著智慧比较选项并给出推荐

        Args:
            options: 选项列表

        Returns:
            推荐结果
        """
        return compare_and_recommend(options)

    def explain_wisdom(self, topic: str) -> Dict[str, Any]:
        """
        解释四大名著中关于特定主题的智慧

        Args:
            topic: 主题

        Returns:
            解释结果
        """
        return explain_wisdom(topic)

# 兼容层：模块级函数和常量
def _match_themes(situation: str, book: str) -> List[str]:
    """匹配主题关键词"""
    keywords = THEME_KEYWORDS.get(book, {})
    matched = []
    for theme, cases in keywords.items():
        for case in cases:
            if case.lower() in situation.lower():
                matched.append(theme)
                break
    return matched

def _get_recommend_sanguo_case(matched_themes: List[str]) -> Dict[str, Any]:
    """获取推荐的三国案例"""
    from ._cwc_sanguo import get_recommend_sanguo_case
    return get_recommend_sanguo_case(matched_themes)

def _get_recommend_shuihu_case(matched_themes: List[str]) -> Dict[str, Any]:
    """获取推荐的水浒案例"""
    from ._cwc_shuihu import get_recommend_shuihu_case
    return get_recommend_shuihu_case(matched_themes)

def _summarize_sanguo_wisdom(matched_themes: List[str]) -> str:
    """总结三国智慧"""
    from ._cwc_sanguo import summarize_sanguo_wisdom
    return summarize_sanguo_wisdom(matched_themes)

def _summarize_shuihu_wisdom(matched_themes: List[str]) -> str:
    """总结水浒智慧"""
    from ._cwc_shuihu import summarize_shuihu_wisdom
    return summarize_shuihu_wisdom(matched_themes)

def _generate_sanguo_actions(matched_themes: List[str]) -> List[str]:
    """生成三国视角的行动建议"""
    from ._cwc_sanguo import generate_sanguo_actions
    return generate_sanguo_actions(matched_themes)

def _generate_shuihu_actions(matched_themes: List[str]) -> List[str]:
    """生成水浒视角的行动建议"""
    from ._cwc_shuihu import generate_shuihu_actions
    return generate_shuihu_actions(matched_themes)

def _get_relationship_management(self) -> List[str]:
    """获取关系管理建议"""
    return [
        "真诚待人--袭人的温柔和顺",
        "保持距离--晴雯的心比天高",
        "平衡利益--平儿的善良周全",
        "知恩图报--刘姥姥的智慧"
    ]

def _get_relationship_warnings(self) -> List[str]:
    """获取关系警示"""
    return [
        "警惕'王熙凤式'精明--机关算尽,反误卿卿性命",
        "避免'晴雯式'锋芒--木秀于林,风必摧之",
        "不要'迎春式'软弱--老实人容易被欺负"
    ]
