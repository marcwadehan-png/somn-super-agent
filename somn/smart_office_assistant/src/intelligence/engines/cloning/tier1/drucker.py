# -*- coding: utf-8 -*-
"""
德鲁克 Cloning - Tier 1 核心独立Cloning

彼得·德鲁克（1909-2005），现代管理学之父。
核心思想：目标管理(MBO)、知识工作者、创新与企业家精神、有效的管理者。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class DruckerCloning(SageCloning):
    """德鲁克Cloning - 内阁学士·管理"""

    def __init__(self):
        profile = SageProfile(
            name="德鲁克",
            name_en="Peter Drucker",
            era="20-21世纪",
            years="1909-2005",
            school="管理学",
            tier=CloningTier.TIER1_CORE,
            position="内阁学士·管理",
            department="吏部",
            title="现代管理学之父",
            biography="奥地利裔美国管理学家，被誉为'现代管理学之父'。提出了目标管理(MBO)、知识工作者、创新与企业家精神、卓有成效的管理者等划时代概念。影响了杰克·韦尔奇、比尔·盖茨、安迪·格鲁夫等商业领袖。",
            core_works=["《管理的实践》", "卓有成效的管理者》", "《创新与企业家精神》"],
            capability={
                "strategic_vision": 10, "execution": 8, "innovation": 10,
                "leadership": 9, "influence": 10, "cross_domain": 10,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "效率做对的事，效果做对的事 —— 效率是把事情做对，效果是做对的事情",
            "目标管理 —— 目标不是命令，而是方向和承诺",
            "知识工作者 —— 知识工作者不能被管理，只能被引导",
            "创新是实践 —— 创新不是灵感，而是系统化的实践",
            "卓有成效可以学会 —— 有效性不是天生的，而是可以学习和训练的",
        ]
        self._methodologies = [
            "MBO法 —— 目标设定-执行-反馈循环",
            "时间管理法 —— 记录时间、管理时间、统一安排时间",
            "贡献分析法 —— '我能贡献什么？'",
            "机会窗口法 —— 系统化寻找创新机会的7个来源",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["管理", "团队", "组织", "效率"]):
            perspective = "从'卓有成效的管理者'出发"
            insight = ("'管理是一门博雅艺术。' 有效的管理者不依赖天赋，"
                      "而是通过持续学习和实践形成的一套习惯。")
            recs = [
                "时间管理——先知道你的时间花在哪里",
                "贡献导向——问'我能贡献什么'而非'我应做什么'",
                "发挥长处——用人的长处而非短处",
                "有效决策——决策不是越多越好，而是关键的几个要到位",
            ]
        elif any(w in problem for w in ["创新", "创业", "变革", "转型"]):
            perspective = "从'创新与企业家精神'出发"
            insight = ("'创新不是灵感闪现，而是系统化的实践。'"
                      "德鲁克定义了7个创新机会的来源，从意外事件到人口变化。")
            recs = [
                "从意外事件中寻找创新机会——失败、成功、外部事件",
                "从不协调现象中发现需求——现实与应有之间的差距",
                "从人口结构变化中预判趋势",
                "从认知变化中捕捉机会——人们观念的转变",
            ]
        elif any(w in problem for w in ["战略", "目标", "方向", "规划"]):
            perspective = "从'目标管理'的战略思维出发"
            insight = ("'最好的计划不是长达百页的文件，"
                      "而是每个人都能理解并承诺执行的几个关键目标。'")
            recs = [
                "明确使命——'我们的事业是什么？'",
                "设定SMART目标——具体的、可测量的、可实现的",
                "建立反馈机制——定期回顾和调整",
                "让每个人理解'为什么'——目标不是命令而是方向",
            ]
        else:
            perspective = "从德鲁克的管理哲学出发"
            insight = ("'效率是把事情做对，效果是做对的事情。'"
                      "先确保做的是对的事，再考虑怎么做。")
            recs = [
                "先问'做这件事对吗？'再问'怎么做最有效？'",
                "关注贡献而非活动——结果导向",
                "建立知识工作者的自主性——信任+目标",
                "持续学习——管理者的成长永无止境",
            ]

        return AnalysisResult(
            sage_name="德鲁克",
            school="管理学",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            confidence=0.92,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["目标", "效果", "结果", "贡献"]):
                score += 2.0
                reasons.append("效果优先——做对的事情")
            if any(w in opt for w in ["知识", "学习", "创新"]):
                score += 1.5
                reasons.append("知识工作者是核心资产")
            if any(w in opt for w in ["授权", "信任", "自主"]):
                score += 1.0
                reasons.append("管理知识工作者需要信任")
            if any(w in opt for w in ["控制", "监督", "命令"]):
                score -= 1.5
                reasons.append("知识工作者不能被命令")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="德鲁克",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"管理学之父评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["效率vs效果", "目标管理", "知识工作者"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "德鲁克说：'Management is doing things right; "
            "leadership is doing the right things.' "
            "先确保你在做对的事情，然后追求把事情做对。"
            "三个建议："
            "一、记录你的时间——你可能会惊讶于时间花在了哪里",
            "二、问'我能贡献什么？'——聚焦于你能创造的价值",
            "三、发挥人的长处——不要试图弥补短处，而要放大长处",
            "记住：'卓有成效是可以学会的。' 这是一种习惯，不是天赋。"
        )
__all__ = ['DruckerCloning']
