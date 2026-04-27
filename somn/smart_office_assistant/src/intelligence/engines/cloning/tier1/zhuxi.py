# -*- coding: utf-8 -*-
"""
朱熹 Cloning - Tier 1 核心独立Cloning

朱熹（1130-1200），理学集大成者。
核心思想：存天理灭人欲、格物致知、理一分殊、循序渐进。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class ZhuXiCloning(SageCloning):
    """朱熹Cloning - 礼部尚书"""

    def __init__(self):
        profile = SageProfile(
            name="朱熹",
            name_en="Zhu Xi",
            era="南宋",
            years="1130-1200",
            school="理学",
            tier=CloningTier.TIER1_CORE,
            position="礼部尚书",
            department="礼部",
            title="理学集大成者·朱子",
            biography="南宋哲学家、教育家，理学思想集大成者。注释《四书》成为科举标准教材，影响中国思想界七百余年。构建了'理气论'的完整哲学体系，提出'格物致知'的认识论和'存天理灭人欲'的修养论。",
            core_works=["《四书章句集注》", "《朱子语类》"],
            capability={
                "strategic_vision": 8, "execution": 7, "innovation": 8,
                "leadership": 8, "influence": 10, "cross_domain": 8,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "格物致知 —— 通过研究具体事物来获得普遍真理",
            "存天理灭人欲 —— 克制过度的欲望，回归合理",
            "理一分殊 —— 核心原理相同，具体应用各有不同",
            "循序渐进 —— 学习和做事必须按步骤来",
            "知行相须 —— 知是行的前提，行是知的完成",
        ]
        self._methodologies = [
            "格物法 —— 逐一研究具体事物，积累到量变产生质变",
            "读书法 —— 熟读精思，虚心涵泳，切己体察",
            "居敬法 —— 保持内心的敬畏和专注",
            "分类法 —— '理一分殊'，按类别归约问题",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["学习", "教育", "知识", "研究"]):
            perspective = "从'格物致知'的治学方法论出发"
            insight = ("'即凡天下之物，莫不因其已知之理而益穷之，以求至乎其极。'"
                      "学习是一个不断深入研究、由表及里的过程。")
            recs = [
                "从具体案例入手——'今日格一物，明日格一物'",
                "深入到极致——'用力之久，而一旦豁然贯通'",
                "理论与实践结合——'知行相须，如目无足不行，足无目不见'",
                "保持敬畏之心——'敬'是学习的前提",
            ]
        elif any(w in problem for w in ["制度", "体系", "规范", "标准"]):
            perspective = "从'理一分殊'的系统思维出发"
            insight = ("万事万物都有其'理'（规律），虽然表现形式不同，"
                      "但底层原理相通。找到'一理'，就能应对'万殊'。")
            recs = [
                "先找到问题的本质规律（理一）",
                "再根据具体情况灵活应用（分殊）",
                "建立规范体系——'存天理'",
                "去除不合理部分——'灭人欲'中的过度和扭曲",
            ]
        else:
            perspective = "从理学的系统分析框架出发"
            insight = ("'宇宙之间，一理而已。' 用系统的、分类的、"
                      "循序渐进的方法来分析问题。")
            recs = [
                "分解问题为具体可研究的子问题",
                "逐一深入——格物",
                "寻找共同规律——致知",
                "按步骤推进——循序渐进",
            ]

        return AnalysisResult(
            sage_name="朱熹",
            school="理学",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["理学可能流于繁琐，需把握本质"],
            confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["系统", "全面", "规范", "标准"]):
                score += 2.0
                reasons.append("理一分殊，系统完备")
            if any(w in opt for w in ["渐进", "逐步", "稳妥"]):
                score += 1.5
                reasons.append("循序渐进，不可躐等")
            if any(w in opt for w in ["深入", "研究", "细致"]):
                score += 1.0
                reasons.append("格物致知，深入本质")
            if any(w in opt for w in ["冲动", "草率", "冒险"]):
                score -= 2.0
                reasons.append("浮躁是格物的大敌")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="朱熹",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"理学评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["格物致知", "理一分殊", "循序渐进"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "朱子曰：'读书之法，在循序而渐进，熟读而精思。' "
            "做任何事情都和学习一样：先打基础，再深入，"
            "最后达到融会贯通。不要急于求成——"
            "'勿助长也，拔苗者非徒无益，而又害之。'"
        )
__all__ = ['ZhuXiCloning']
