# -*- coding: utf-8 -*-
"""
孙武 Cloning - Tier 1 核心独立Cloning

孙武（前545-前470），兵圣，著有《孙子兵法》十三篇。
核心思想：知己知彼、不战而屈人之兵、兵者诡道、出奇制胜。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class SunWuCloning(SageCloning):
    """孙武Cloning - 兵部尚书"""

    def __init__(self):
        profile = SageProfile(
            name="孙武",
            name_en="Sun Wu (Sun Tzu)",
            era="春秋末期",
            years="前545-前470",
            school="兵家",
            tier=CloningTier.TIER1_CORE,
            position="兵部尚书",
            department="兵部",
            title="兵圣·东方兵学鼻祖",
            biography="春秋末期齐国人，著有《孙子兵法》十三篇，被译成20多种语言。以三万吴军破三十万楚军的柏举之战奠定兵圣地位。其军事思想超越时代，被广泛应用于商业、政治、体育等领域。",
            core_works=["《孙子兵法》"],
            capability={
                "strategic_vision": 10, "execution": 10, "innovation": 9,
                "leadership": 9, "influence": 10, "cross_domain": 9,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "知彼知己，百战不殆 —— 信息是决策的前提",
            "不战而屈人之兵 —— 最高战略是让对手放弃抵抗",
            "兵者诡道也 —— 真实意图必须隐藏",
            "出奇制胜 —— 正合奇胜，以常规吸引，以非常规决胜",
            "兵贵神速 —— 速度是最大的竞争优势",
        ]
        self._methodologies = [
            "五事七计法 —— 道、天、地、将、法五要素评估",
            "虚实分析法 —— 避实击虚，攻其必救",
            "态势分析法 —— 奇正相生，循环无穷",
            "成本收益法 —— 因粮于敌，以战养战",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["竞争", "对手", "市场", "商战"]):
            perspective = "从'知己知彼、不战而胜'的竞争战略出发"
            insight = ("竞争的最高境界不是消灭对手，而是让对手无法与你竞争。"
                      "先确保'不可被战胜'（立于不败之地），再寻找'可胜之机'。")
            recs = [
                "先做SWOT：己方实力、敌方实力、战场环境、可用资源",
                "找到对手的'虚'——薄弱环节或认知盲区",
                "确保己方'不可被战胜'——构建护城河",
                "设计'奇'——对手意想不到的差异化策略",
            ]
        elif any(w in problem for w in ["决策", "选择", "方案"]):
            perspective = "从'庙算'的决策分析方法出发"
            insight = ("'多算胜，少算不胜，而况于无算乎！' "
                      "决策之前，必须充分计算各种可能性。")
            recs = [
                "五事七计：目的正当吗？天时地利如何？人才到位吗？制度健全吗？",
                "计算投入产出比——'日费千金，然后十万之师举矣'",
                "预判对手反应——'攻其无备，出其不意'",
                "准备多套方案——'正合'为明面，'奇'为底牌",
            ]
        elif any(w in problem for w in ["团队", "执行", "效率"]):
            perspective = "从'令之以文，齐之以武'的治军之道出发"
            insight = ("团队管理的核心是'令素行以教其民'——平时养成良好习惯，"
                      "关键时刻才能令行禁止。")
            recs = [
                "赏罚分明——'赏罚孰明'是团队战斗力的关键",
                "知人善任——'将者，智信仁勇严也'",
                "信息通畅——'不用乡导者，不能得地利'",
                "保持机动——'兵之情主速，乘人之不及'",
            ]
        else:
            perspective = "从《孙子兵法》的系统思维出发"
            insight = ("任何问题都可以类比为'用兵'——目标明确、知己知彼、"
                      "避实击虚、出奇制胜、速战速决。")
            recs = [
                "明确'道'——目标是否正当、团队是否同心",
                "评估'天地'——外部环境和时机",
                "锻造'将'——找到合适的人执行",
                "制定'法'——制度、流程、标准",
            ]

        return AnalysisResult(
            sage_name="孙武",
            school="兵家",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["兵者国之大事，不可轻启"],
            confidence=0.93,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["不战", "和解", "共赢", "妥协"]):
                score += 1.5
                reasons.append("不战而屈人之兵，上策")
            if any(w in opt for w in ["奇", "创新", "意外", "差异化"]):
                score += 2.0
                reasons.append("出奇制胜，以正合以奇胜")
            if any(w in opt for w in ["速", "快", "敏捷"]):
                score += 1.0
                reasons.append("兵贵神速")
            if any(w in opt for w in ["消耗", "持久", "拖延"]):
                score -= 2.0
                reasons.append("久暴师则国用不足，持久战是下策")
            if any(w in opt for w in ["正面对抗", "硬碰硬"]):
                score -= 1.0
                reasons.append("以正合可，但需配以奇胜")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="孙武",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"兵圣评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["知彼知己", "不战而屈人之兵", "出奇制胜"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "兵者，国之大事，死生之地，存亡之道，不可不察也。"
            "你当前的情况需要用'五事七计'来系统分析："
            "一、'道'——你的目标是否正义、团队是否同心？"
            "二、'天'——外部环境和时机如何？"
            "三、'地'——你在什么位置、有什么资源？"
            "四、'将'——执行的人能力如何？"
            "五、'法'——组织、制度、流程是否健全？"
            "记住：'胜可知，而不可为'——胜利的条件可以创造，但不能强求。"
        )
__all__ = ['SunWuCloning']
