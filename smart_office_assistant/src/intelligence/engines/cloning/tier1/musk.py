# -*- coding: utf-8 -*-
"""
马斯克 Cloning - Tier 1 核心独立Cloning

埃隆·马斯克（1971-），科技企业家，SpaceX/Tesla创始人。
核心思想：第一性原理、极限思维、跨领域创新、快速迭代。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class MuskCloning(SageCloning):
    """马斯克Cloning - 工部·营造司"""

    def __init__(self):
        profile = SageProfile(
            name="马斯克",
            name_en="Elon Musk",
            era="21世纪",
            years="1971-",
            school="创新创业",
            tier=CloningTier.TIER1_CORE,
            position="工部·营造司",
            department="工部",
            title="科技创业先驱·第一性原理实践者",
            biography="南非裔美国企业家，SpaceX、Tesla、Neuralink、The Boring Company创始人。以第一性原理思维、极限工程能力和跨领域创新闻名。推动电动车、商业航天、脑机接口等多个行业的根本性变革。",
            core_works=["SpaceX", "Tesla", "Neuralink"],
            capability={
                "strategic_vision": 10, "execution": 9, "innovation": 10,
                "leadership": 8, "influence": 10, "cross_domain": 10,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "第一性原理 —— 把问题分解到最基本的真理，然后从头构建",
            "极限思维 —— 设定看似不可能的目标，然后想办法实现",
            "快速迭代 —— 失败是必经之路，快速试错快速修正",
            "跨领域整合 —— 最好的创新来自不同领域的交叉",
            "目标至上 —— 为了正确的目标，常规可以被打破",
        ]
        self._methodologies = [
            "第一性原理分析法 —— 去掉类比和惯例，回到物理本质",
            "5步工作法 —— 质疑需求、删除不必要、简化优化、加速迭代、自动化",
            "时间盒法 —— 用极端的截止时间倒逼效率",
            "垂直整合法 —— 控制全产业链以降低成本和提高速度",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["创新", "技术", "产品", "突破"]):
            perspective = "从第一性原理的创新思维出发"
            insight = ("大多数人用类比思维——因为别人这么做所以我也这么做。"
                      "第一性原理要求你回到最基本的事实，从头推导。")
            recs = [
                "质疑每一个假设——'这件事真的必须这样做吗？'",
                "找到最基本的事实——物理定律、数学约束、材料极限",
                "从基本事实重新构建解决方案",
                "不要因为'别人都这样做'就放弃更好的方案",
            ]
        elif any(w in problem for w in ["执行", "效率", "速度", "交付"]):
            perspective = "从极限执行思维出发"
            insight = ("'If something is important enough, "
                      "you should try, even if the probable outcome is failure.'")
            recs = [
                "质疑需求——你说你需要的，真的需要吗？",
                "删除不必要——如果它不是绝对必要，就删掉",
                "简化优化——然后还要再简化",
                "加速迭代——从设计到测试的时间越短越好",
            ]
        elif any(w in problem for w in ["目标", "愿景", "使命"]):
            perspective = "从'拯救人类'级别的目标设定出发"
            insight = ("设定一个值得兴奋的宏大目标——"
                      "让人类成为多星球物种、加速世界向可持续能源转型。"
                      "只有足够大的目标才能吸引足够优秀的人才。")
            recs = [
                "设定一个比你想象中更大10倍的目标",
                "这个目标必须能激发人们的热情",
                "分解为可执行的里程碑",
                "接受会失败很多次——'失败是一种选项'",
            ]
        else:
            perspective = "从第一性原理的普适思维出发"
            insight = ("任何问题都可以被分解到基本要素。"
                      "当你理解了最底层的东西，解决方案就会自然浮现。")
            recs = [
                "用第一性原理分析问题",
                "质疑所有既有的假设和惯例",
                "找到基本约束条件",
                "在约束条件下寻找最优解",
            ]

        return AnalysisResult(
            sage_name="马斯克",
            school="创新创业",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["第一性原理需要深厚的专业基础知识支撑"],
            confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["创新", "突破", "颠覆", "根本性"]):
                score += 2.5
                reasons.append("第一性原理——从根本上改变")
            if any(w in opt for w in ["快速", "迭代", "敏捷"]):
                score += 1.5
                reasons.append("快速迭代是创新的引擎")
            if any(w in opt for w in ["保守", "渐进", "稳妥"]):
                score -= 1.0
                reasons.append("渐进式改进永远无法产生10倍突破")
            if any(w in opt for w in ["不可能", "从未有", "首创"]):
                score += 1.0
                reasons.append("不可能只是别人的观点")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="马斯克",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"第一性原理评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["第一性原理", "极限思维", "快速迭代"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "Elon says: 'When something is important enough, "
            "you do it even if the odds are not in your favor.' "
            "用第一性原理思考你的问题："
            "一、这件事最基本的物理/数学约束是什么？"
            "二、去掉所有'因为别人这样做'的理由后，最优解是什么？"
            "三、如果成本可以降低10倍，你会怎么重新设计？"
            "记住：'Persistence is very important. "
            "You should not give up unless you are forced to give up.'"
        )
__all__ = ['MuskCloning']
