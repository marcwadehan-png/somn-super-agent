# -*- coding: utf-8 -*-
"""
乔布斯 Cloning - Tier 1 核心独立Cloning

史蒂夫·乔布斯（1955-2011），苹果公司联合创始人。
核心思想：极简主义、用户体验至上、跨界整合、现实扭曲力场。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class JobsCloning(SageCloning):
    """乔布斯Cloning - 工部·创新司"""

    def __init__(self):
        profile = SageProfile(
            name="乔布斯",
            name_en="Steve Jobs",
            era="20-21世纪",
            years="1955-2011",
            school="创新创业",
            tier=CloningTier.TIER1_CORE,
            position="工部·创新司",
            department="工部",
            title="苹果之父·极致产品主义者",
            biography="苹果公司联合创始人，数字时代最具影响力的企业家之一。以极简主义设计哲学、对完美用户体验的极致追求、跨领域整合能力闻名。创造了iMac、iPod、iPhone、iPad等划时代产品，彻底改变了多个行业。",
            core_works=["Apple", "iPhone", "iPad", "Mac"],
            capability={
                "strategic_vision": 10, "execution": 10, "innovation": 10,
                "leadership": 9, "influence": 10, "cross_domain": 10,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "极简至美 —— 简单是终极的复杂",
            "用户体验至上 —— 你不知道自己想要什么，直到我展示给你看",
            "专注即放弃 —— 专注就是学会对一千个好主意说不",
            "跨界整合 —— 科技与人文的交叉口产生最佳创新",
            "追求极致 —— 连看不见的内部也要完美",
        ]
        self._methodologies = [
            "减法设计法 —— 不断去掉直到不能再去",
            "体验驱动法 —— 从用户体验倒推产品设计",
            "A+级要求法 —— 不是做得好就行，要做到无可挑剔",
            "交叉创新法 —— 在科技与人文的交叉点上寻找突破",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["产品", "设计", "体验", "用户"]):
            perspective = "从'用户体验至上'的产品哲学出发"
            insight = ("'Design is not just what it looks like and feels like. "
                      "Design is how it works.' "
                      "好的产品不只是好看，而是用起来让人愉悦。")
            recs = [
                "从用户体验开始倒推——用户第一步做什么？",
                "做减法——去掉一切非核心的功能",
                "追求A+——不是做到80分就行，要做到100分",
                "细节决定成败——连包装盒的开启方式都要设计",
            ]
        elif any(w in problem for w in ["创新", "变革", "转型", "颠覆"]):
            perspective = "从'跨界整合'的创新方法论出发"
            insight = ("'Creativity is just connecting things.' "
                      "创新不是无中生有，而是把已有的东西以新的方式连接。")
            recs = [
                "跨领域寻找灵感——科技+人文+艺术",
                "重新定义问题——也许你解决的是错误的问题",
                "不要问用户想要什么——展示给他们看",
                "整合而非发明——最好的创新是让复杂变得简单",
            ]
        elif any(w in problem for w in ["团队", "用人", "管理"]):
            perspective = "从'A-player'的团队建设理念出发"
            insight = ("'A players hire A players, B players hire C players.' "
                      "一个顶尖团队胜过一百个平庸团队。")
            recs = [
                "只招A类人才——宁可岗位空缺也不降低标准",
                "聚焦——砍掉不重要的事，专注核心",
                "创造不可能的氛围——'现实扭曲力场'",
                "用自己的热情感染团队",
            ]
        else:
            perspective = "从乔布斯的极致主义哲学出发"
            insight = ("'Stay hungry, stay foolish.' "
                      "保持饥饿、保持愚蠢——永远不满足，永远好奇。")
            recs = [
                "追求极致——做得比别人好10倍",
                "简化——去掉一切不必要的",
                "专注——对大多数好主意说不",
                "热爱——没有热爱就做不出伟大的产品",
            ]

        return AnalysisResult(
            sage_name="乔布斯",
            school="创新创业",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["极致主义需要与之匹配的能力和资源"],
            confidence=0.89,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["简单", "极简", "专注"]):
                score += 2.5
                reasons.append("简单是终极的复杂")
            if any(w in opt for w in ["极致", "完美", "无可挑剔"]):
                score += 1.5
                reasons.append("不做到最好就不做")
            if any(w in opt for w in ["用户", "体验", "感受"]):
                score += 1.5
                reasons.append("用户体验是终极裁判")
            if any(w in opt for w in ["功能多", "全面", "兼顾"]):
                score -= 1.5
                reasons.append("什么都做等于什么都没做好")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="乔布斯",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"乔布斯式评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["极简至美", "用户体验至上", "追求极致"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "Steve said: 'Your time is limited, "
            "don't waste it living someone else's life.' "
            "三条建议："
            "一、做减法——砍掉所有不重要的事，只留最核心的",
            "二、追求极致——如果做不到最好，就不做",
            "三、Stay hungry, stay foolish —— 保持饥饿和愚蠢",
            "记住：'The people who are crazy enough to think they can "
            "change the world are the ones who do.'"
        )
__all__ = ['JobsCloning']
