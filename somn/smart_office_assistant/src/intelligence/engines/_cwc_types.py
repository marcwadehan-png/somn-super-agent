# -*- coding: utf-8 -*-
"""四大名著智慧引擎 - 类型定义"""

from typing import Dict, List, Any, TypedDict

class WisdomAnalysis(TypedDict, total=False):
    """智慧分析结果"""
    version: str
    timestamp: str
    situation: str
    sanguo_analysis: Dict[str, Any]
    shuihu_analysis: Dict[str, Any]
    xiyou_analysis: Dict[str, Any]
    honglou_analysis: Dict[str, Any]
    comprehensive_advice: Dict[str, Any]

class SanguoAnalysis(TypedDict, total=False):
    """三国分析结果"""
    matched_themes: List[str]
    recommended_case: Dict[str, Any]
    wisdom_summary: str
    action_suggestions: List[str]

class ShuihuAnalysis(TypedDict, total=False):
    """水浒分析结果"""
    matched_themes: List[str]
    recommended_case: Dict[str, Any]
    wisdom_summary: str
    action_suggestions: List[str]

class XiyouAnalysis(TypedDict, total=False):
    """西游分析结果"""
    matched_themes: List[str]
    recommended_case: Dict[str, Any]
    wisdom_summary: str
    action_suggestions: List[str]

class HonglouAnalysis(TypedDict, total=False):
    """红楼分析结果"""
    matched_themes: List[str]
    recommended_case: Dict[str, Any]
    wisdom_summary: str
    action_suggestions: List[str]

class ComprehensiveAdvice(TypedDict, total=False):
    """综合建议"""
    sanguo_advice: str
    shuihu_advice: str
    xiyou_advice: str
    honglou_advice: str
    final_recommendation: str

# 四大名著名称常量
BOOK_NAMES = ["三国", "水浒", "西游", "红楼"]

# 主题关键词映射
THEME_KEYWORDS = {
    "三国": {
        "竞争": ["赤壁之战", "官渡之战", "以少胜多"],
        "人才": ["三顾茅庐", "唯才是举", "知人善任"],
        "战略": ["隆中对", "三分天下", "联吴抗曹"],
        "领导": ["曹操", "刘备", "孙权", "领导艺术"]
    },
    "水浒": {
        "团队": ["聚义", "排座次", "梁山"],
        "困境": ["逼上梁山", "被逼", "困境"],
        "义气": ["兄弟", "义气", "忠诚"],
        "领导": ["宋江", "晁盖", "领导力"]
    },
    "西游": {
        "成长": ["取经", "修行", "成长", "修炼"],
        "团队": ["唐僧", "悟空", "八戒", "团队协作"],
        "挑战": ["八十一难", "妖魔", "困难"],
        "坚持": ["信念", "坚持", "不放弃"]
    },
    "红楼": {
        "组织": ["管理", "家族", "企业", "组织"],
        "人物": ["王熙凤", "探春", "领导力"],
        "兴衰": ["繁荣", "衰落", "周期", "兴亡"],
        "人际关系": ["关系", "情感", "人际"]
    }
}

# 默认主题（当无匹配时使用）
DEFAULT_THEMES = {
    "三国": "战略规划",
    "水浒": "团队建设",
    "西游": "成长与修行",
    "红楼": "组织管理"
}
