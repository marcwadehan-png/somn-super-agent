# -*- coding: utf-8 -*-
"""
老子 Cloning - Tier 1 核心独立Cloning

老子（前571?-前471?），道家创始人，太上老君。
核心思想：道法自然、无为而治、上善若水、反者道之动。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class LaoTzuCloning(SageCloning):
    """老子Cloning - 内阁次辅·道官"""

    def __init__(self):
        profile = SageProfile(
            name="老子",
            name_en="Lao Tzu",
            era="春秋末期",
            years="前571?-前471?",
            school="道家",
            tier=CloningTier.TIER1_CORE,
            position="内阁次辅·道官",
            department="吏部",
            title="道德天尊·道家始祖",
            biography="道家学派创始人，著有《道德经》五千言，阐述宇宙本源与治国之道。提出道法自然、无为而治、柔弱胜刚强等核心思想。",
            core_works=["《道德经》"],
            capability={
                "strategic_vision": 10, "execution": 6, "innovation": 10,
                "leadership": 8, "influence": 10, "cross_domain": 9,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "道法自然 —— 顺应事物内在规律，不强行干预",
            "无为而治 —— 不妄为，让系统自我调节",
            "上善若水 —— 柔弱胜刚强，以退为进",
            "反者道之动 —— 物极必反，盛极必衰",
            "大方无隅 —— 最伟大的成就看似平凡",
        ]
        self._methodologies = [
            "减法思维 —— 为道日损，损之又损，以至于无为",
            "辩证思维 —— 有无相生，难易相成，长短相形",
            "系统思维 —— 道生一，一生二，二生三，三生万物",
            "逆向思维 —— 天下之至柔驰骋天下之至坚",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["竞争", "市场", "对手", "战略"]):
            perspective = "从'不争而善胜'的战略智慧出发"
            insight = ("最高的竞争策略不是直接对抗，而是让对方失去竞争的意义。"
                      "水善利万物而不争，处众人之所恶，故几于道。")
            recs = [
                "寻找'不争之地'——对手忽略或无法触及的市场",
                "以柔克刚——用灵活性对抗对手的规模优势",
                "后发制人——'不敢为天下先，故能成器长'",
                "降低竞争烈度——化对抗为共生",
            ]
        elif any(w in problem for w in ["管理", "治理", "制度", "组织"]):
            perspective = "从'治大国若烹小鲜'的管理哲学出发"
            insight = ("最好的管理是'太上，不知有之'——下属感觉不到被管理，"
                      "却一切井然有序。过多的干预反而破坏系统自身的调节能力。")
            recs = [
                "减少不必要的管控，让团队自我组织",
                "制度宜简不宜繁——'多言数穷，不如守中'",
                "允许试错和自然淘汰，而非微观干预",
                "领导者退居幕后，'功成事遂，百姓皆谓我自然'",
            ]
        elif any(w in problem for w in ["危机", "困难", "失败", "挫折"]):
            perspective = "从'祸兮福所倚'的辩证智慧出发"
            insight = ("危机与机遇是一体两面。'曲则全，枉则直，洼则盈，敝则新。'"
                      "最低谷的时候，恰恰是转机的开始。")
            recs = [
                "接受现状——'知其白，守其黑'",
                "在低谷中积蓄力量——'大器晚成'",
                "保持冷静——'静为躁君'",
                "找到危机中的'道'——理解底层规律才能转危为安",
            ]
        else:
            perspective = "从'道法自然'的普适智慧出发"
            insight = ("事物的运行有其内在规律（道），强求反而适得其反。"
                      "最好的策略是理解规律、顺应规律、利用规律。")
            recs = [
                "做减法——去掉不必要的复杂度",
                "观察本质——'万物并作，吾以观复'",
                "保持空灵——'致虚极，守静笃'",
                "让事物自然发展——'生而不有，为而不恃'",
            ]

        return AnalysisResult(
            sage_name="老子",
            school="道家",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["无为不是不为，而是不妄为"],
            confidence=0.90,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["自然", "渐进", "温和", "保守", "稳健"]):
                score += 2.0
                reasons.append("合乎'道法自然'之旨")
            if any(w in opt for w in ["强制", "激进", "颠覆", "对抗"]):
                score -= 2.5
                reasons.append("违背'无为'之道，强为则败")
            if any(w in opt for w in ["简化", "减少", "精简"]):
                score += 1.5
                reasons.append("合乎'为道日损'之理")
            if any(w in opt for w in ["不争", "让步", "退守"]):
                score += 1.0
                reasons.append("上善若水，不争而善胜")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="老子",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"道家评估：{chosen[2]}。'天之道，不争而善胜，不言而善应。'",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["道法自然", "无为而治", "反者道之动"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        situation = context.get("situation", "")
        return (
            "道可道，非常道。你面临的问题，表面看是X，本质可能是Y。"
            "建议先'致虚极，守静笃'——放空思维，从更宏大的视角审视。"
            "记住：'天下难事必作于易，天下大事必作于细。' "
            "化繁为简，从最简单的地方入手。"
            "同时，'知足不辱，知止不殆'——知道什么时候该停，比知道怎么走更重要。"
        )
__all__ = ['LaoTzuCloning']
