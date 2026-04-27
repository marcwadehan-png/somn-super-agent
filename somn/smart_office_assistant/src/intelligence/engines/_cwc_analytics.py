# -*- coding: utf-8 -*-
"""四大名著智慧引擎 - 分析逻辑模块"""

from datetime import datetime
from typing import Dict, List, Any

from ._cwc_types import THEME_KEYWORDS, DEFAULT_THEMES
from ._cwc_sanguo import (
    get_sanguo_wisdom,
    generate_sanguo_actions,
)

__all__ = [
    'analyze_honglou',
    'analyze_sanguo',
    'analyze_shuihu',
    'analyze_xiyou',
    'compare_and_recommend',
    'explain_wisdom',
    'generate_comprehensive_advice',
    'get_quote',
    'get_wisdom_by_book',
]

from ._cwc_shuihu import (
    get_shuihu_wisdom,
    get_recommend_shuihu_case,
    summarize_shuihu_wisdom,
    generate_shuihu_actions
)
from ._cwc_xiyou import (
    get_xiyou_wisdom,
    get_recommend_xiyou_case,
    summarize_xiyou_wisdom,
    generate_xiyou_actions
)
from ._cwc_honglou import (
    get_honglou_wisdom,
    get_recommend_honglou_case,
    summarize_honglou_wisdom,
    generate_honglou_actions
)

def analyze_sanguo(situation: str) -> Dict[str, Any]:
    """三国视角分析"""
    matched = _match_themes(situation, "三国")
    if not matched:
        matched = ["战略规划"]

    return {
        "matched_themes": matched,
        "recommended_case": get_recommend_sanguo_case(matched),
        "wisdom_summary": summarize_sanguo_wisdom(matched),
        "action_suggestions": generate_sanguo_actions(matched)
    }

def analyze_shuihu(situation: str) -> Dict[str, Any]:
    """水浒视角分析"""
    matched = _match_themes(situation, "水浒")
    if not matched:
        matched = ["团队建设"]

    return {
        "matched_themes": matched,
        "recommended_case": get_recommend_shuihu_case(matched),
        "wisdom_summary": summarize_shuihu_wisdom(matched),
        "action_suggestions": generate_shuihu_actions(matched)
    }

def analyze_xiyou(situation: str) -> Dict[str, Any]:
    """西游视角分析"""
    matched = _match_themes(situation, "西游")
    if not matched:
        matched = ["成长与修行"]

    return {
        "matched_themes": matched,
        "recommended_case": get_recommend_xiyou_case(matched),
        "wisdom_summary": summarize_xiyou_wisdom(matched),
        "action_suggestions": generate_xiyou_actions(matched)
    }

def analyze_honglou(situation: str) -> Dict[str, Any]:
    """红楼视角分析"""
    matched = _match_themes(situation, "红楼")
    if not matched:
        matched = ["组织管理"]

    return {
        "matched_themes": matched,
        "recommended_case": get_recommend_honglou_case(matched),
        "wisdom_summary": summarize_honglou_wisdom(matched),
        "action_suggestions": generate_honglou_actions(matched)
    }

def generate_comprehensive_advice(situation: str) -> Dict[str, Any]:
    """生成综合建议"""
    sanguo = analyze_sanguo(situation)
    shuihu = analyze_shuihu(situation)
    xiyou = analyze_xiyou(situation)
    honglou = analyze_honglou(situation)

    sanguo_advice = sanguo["action_suggestions"][0] if sanguo["action_suggestions"] else ""
    shuihu_advice = shuihu["action_suggestions"][0] if shuihu["action_suggestions"] else ""
    xiyou_advice = xiyou["action_suggestions"][0] if xiyou["action_suggestions"] else ""
    honglou_advice = honglou["action_suggestions"][0] if honglou["action_suggestions"] else ""

    final_recommendation = (
        f"综合四大名著智慧，建议："
        f"(1) {sanguo_advice}；"
        f"(2) {shuihu_advice}；"
        f"(3) {xiyou_advice}；"
        f"(4) {honglou_advice}。"
    )

    return {
        "sanguo_advice": sanguo_advice,
        "shuihu_advice": shuihu_advice,
        "xiyou_advice": xiyou_advice,
        "honglou_advice": honglou_advice,
        "final_recommendation": final_recommendation
    }

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

def get_wisdom_by_book(book: str) -> Dict[str, Any]:
    """获取特定名著的智慧库"""
    wisdom_map = {
        "三国": get_sanguo_wisdom,
        "水浒": get_shuihu_wisdom,
        "西游": get_xiyou_wisdom,
        "红楼": get_honglou_wisdom
    }

    getter = wisdom_map.get(book)
    if getter:
        return getter()
    return {}

def get_quote(book: str, category: str = "core") -> str:
    """获取四大名著经典语录"""
    quotes = {
        "三国": {
            "core": "天下大势,分久必合,合久必分.",
            "leadership": "勿以恶小而为之,勿以善小而不为.--刘备",
            "wisdom": "谋事在人,成事在天.--诸葛亮"
        },
        "水浒": {
            "core": "逼上梁山,官逼民反.",
            "leadership": "他时若遂凌云志,敢笑黄巢不丈夫!--宋江",
            "wisdom": "赤日炎炎似火烧,野田禾稻半枯焦."
        },
        "西游": {
            "core": "敢问路在何方?路在脚下.",
            "leadership": "紧箍咒--制度约束的必要性",
            "wisdom": "山高自有客行路,水深自有渡船人."
        },
        "红楼": {
            "core": "满纸荒唐言,一把辛酸泪.",
            "leadership": "机关算尽太聪明,反误了卿卿性命.--王熙凤",
            "wisdom": "假作真时真亦假,无为有处有还无."
        }
    }

    book_quotes = quotes.get(book, quotes["三国"])
    return book_quotes.get(category, book_quotes["core"])

def compare_and_recommend(options: List[Dict[str, Any]]) -> Dict[str, Any]:
    """使用四大名著智慧比较选项并给出推荐"""
    if not options:
        return {"error": "没有提供选项"}

    return {
        "recommended_option": options[0] if options else None,
        "reasoning": {
            "三国视角": "从战略高度评估--是否顺应大势?",
            "水浒视角": "从团队角度评估--是否有利于团队?",
            "西游视角": "从成长角度评估--是否有助于修炼?",
            "红楼视角": "从人情角度评估--是否符合人性?"
        },
        "quote": get_quote("三国", "wisdom")
    }

def explain_wisdom(topic: str) -> Dict[str, Any]:
    """解释四大名著中关于特定主题的智慧"""
    theme_explanations = {
        "领导力": {
            "三国": "曹操的唯才是举、刘备的仁德服人、诸葛亮的鞠躬尽瘁",
            "水浒": "宋江的招安悲剧--领导愿景决定团队命运",
            "西游": "唐僧的愿景领导艺术",
            "红楼": "王熙凤的管理才能与探春的改革尝试"
        },
        "团队": {
            "三国": "蜀汉五虎将--各有所长的团队配置",
            "水浒": "梁山108将--互补型团队的典范与教训",
            "西游": "取经团队--完美的角色互补",
            "红楼": "贾府兴衰--团队凝聚力的重要性"
        },
        "战略": {
            "三国": "隆中对--战略规划的经典案例",
            "水浒": "招安决策--战略失误的深刻教训",
            "西游": "九九八十一难--分阶段战略执行",
            "红楼": "探春改革--组织内部的战略调整"
        }
    }

    explanations = {}
    for theme, book_wisdom in theme_explanations.items():
        if theme.lower() in topic.lower() or any(
            book.lower() in topic.lower() for book in ["三国", "水浒", "西游", "红楼"]
        ):
            explanations[theme] = book_wisdom

    if not explanations:
        explanations["通用智慧"] = {
            "三国": "天下大势,分久必合,合久必分",
            "水浒": "逼上梁山--理想与现实的冲突",
            "西游": "敢问路在何方?路在脚下",
            "红楼": "假作真时真亦假,无为有处有还无"
        }

    return explanations
