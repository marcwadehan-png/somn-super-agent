# -*- coding: utf-8 -*-
"""
王阳明 Cloning - Tier 1 核心独立Cloning

王阳明（1472-1529），心学集大成者。
核心思想：知行合一、致良知、心即理、事上磨练。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class WangYangMingCloning(SageCloning):
    """王阳明Cloning - 内阁学士·心官"""

    def __init__(self):
        profile = SageProfile(
            name="王阳明",
            name_en="Wang Yang Ming",
            era="明代",
            years="1472-1529",
            school="心学",
            tier=CloningTier.TIER1_CORE,
            position="内阁学士·心官",
            department="内阁/礼部",
            title="心学集大成者·阳明先生",
            biography="明代思想家、军事家、教育家。龙场悟道后创立心学体系，提出'致良知'和'知行合一'。平定宁王之乱、剿灭盗匪，文治武功兼备。其思想深刻影响了中国、日本、朝鲜的近代化进程。",
            core_works=["《传习录》", "《大学问》"],
            capability={
                "strategic_vision": 9, "execution": 10, "innovation": 10,
                "leadership": 10, "influence": 10, "cross_domain": 9,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "知行合一 —— 知是行的主意，行是知的功夫",
            "致良知 —— 每个人心中都有天理，只需发现它",
            "心即理 —— 心外无理，心外无物",
            "事上磨练 —— 真正的成长只能在实践中获得",
            "破心中贼 —— 最难战胜的是自己内心的私欲",
        ]
        self._methodologies = [
            "良知判断法 —— 遇事第一反应往往是良知的声音",
            "知行循环法 —— 行中知，知中行，互相促进",
            "事上磨练法 —— 不脱离实际，在困难中成长",
            "四句教法 —— 无善无恶心之体，有善有恶意之动",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["执行", "拖延", "行动", "落地"]):
            perspective = "从'知行合一'的实践哲学出发"
            insight = ("'知而不行，只是未知。' 拖延的本质不是懒，"
                      "而是你的'知'还不够深入——你没有真正理解做这件事的意义。")
            recs = [
                "问自己：我真的理解做这件事的意义吗？",
                "从最小可行动作开始——'事上磨练'",
                "消除'心中贼'——恐惧、怀疑、完美主义",
                "每完成一步就增强一分良知（信心）",
            ]
        elif any(w in problem for w in ["决策", "选择", "迷茫", "困惑"]):
            perspective = "从'致良知'的内在智慧出发"
            insight = ("'良知者，心之本体，即前所谓恒照者也。'"
                      "你的内心其实已经知道答案，只是被私欲遮蔽了。")
            recs = [
                "安静下来，倾听内心的第一反应",
                "去掉功利心——'存天理，灭人欲'",
                "用'四句教'审视：这事本身对不对？我的动机纯不纯？",
                "不要过度分析，过度分析是'知'被遮蔽的表现",
            ]
        elif any(w in problem for w in ["领导", "管理", "影响力"]):
            perspective = "从'致良知'的领导哲学出发"
            insight = ("'种树者必培其根，种德者必养其心。'"
                      "领导力的根本是领导者的内心修养。")
            recs = [
                "以身作则——你的行为比你的话更有影响力",
                "信任下属的良知——不要过度管控",
                "在事上磨练团队——给挑战而非给答案",
                "去除'心中贼'——管理者的私欲是组织最大的风险",
            ]
        else:
            perspective = "从心学的普适智慧出发"
            insight = ("'你未看此花时，此花与汝心同归于寂；"
                      "你来看此花时，则此花颜色一时明白起来。' "
                      "问题因你而起，也因你而终。")
            recs = [
                "回归内心——答案在你心里，不在外面",
                "知行合一——想通了的就去做",
                "事上磨练——在实践中验证和深化认知",
                "破心中贼——先战胜自己的恐惧和私欲",
            ]

        return AnalysisResult(
            sage_name="王阳明",
            school="心学",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["良知不可滥用，需以实践验证"],
            confidence=0.91,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["实践", "行动", "执行", "落地"]):
                score += 2.5
                reasons.append("知行合一，行之方为真知")
            if any(w in opt for w in ["良知", "良心", "正道", "初心"]):
                score += 2.0
                reasons.append("致良知，此心光明")
            if any(w in opt for w in ["等待", "观望", "研究"]):
                score -= 1.5
                reasons.append("知而不行，只是未知")
            if any(w in opt for w in ["磨练", "挑战", "困难"]):
                score += 1.0
                reasons.append("事上磨练，愈挫愈勇")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="王阳明",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"心学评估：{chosen[2]}。'此心光明，亦复何言。'",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["知行合一", "致良知", "事上磨练"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "阳明先生曰：'知之真切笃实处即是行，行之明觉精察处即是知。'"
            "你不需要想清楚了再行动——在行动中自然会想清楚。"
            "'破山中贼易，破心中贼难。' 你面临的真正障碍不是外在的，"
            "而是内心的恐惧、犹豫、私欲。直面它们，你就能突破。"
            "记住：'无善无恶心之体，有善有恶意之动，知善知恶是良知，"
            "为善去恶是格物。' 这就是全部的智慧。"
        )
__all__ = ['WangYangMingCloning']
