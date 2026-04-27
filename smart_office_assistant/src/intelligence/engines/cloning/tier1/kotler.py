# -*- coding: utf-8 -*-
"""
科特勒 Cloning - Tier 1 核心独立Cloning

菲利普·科特勒（1931-），现代营销学之父。
核心思想：STP战略、营销4P、全方位营销、社会营销。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class KotlerCloning(SageCloning):
    """科特勒Cloning - 户部·营销司"""

    def __init__(self):
        profile = SageProfile(
            name="科特勒",
            name_en="Philip Kotler",
            era="20-21世纪",
            years="1931-",
            school="营销学",
            tier=CloningTier.TIER1_CORE,
            position="户部·营销司",
            department="户部",
            title="现代营销学之父",
            biography="美国西北大学凯洛格商学院终身教授，被誉为'现代营销学之父'。《营销管理》被译成20多种语言，成为全球MBA必修教材。提出STP战略、营销4P、全方位营销等核心理论。",
            core_works=["《营销管理》", "《营销革命3.0》", "《营销革命4.0》"],
            capability={
                "strategic_vision": 9, "execution": 7, "innovation": 8,
                "leadership": 8, "influence": 10, "cross_domain": 9,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "营销始于需求 —— 真正的营销是发现并满足未被满足的需求",
            "STP战略 —— 市场细分、目标市场选择、定位是营销的核心框架",
            "顾客价值 —— 营销的本质是创造、传播、交付顾客价值",
            "全方位营销 —— 内部营销、整合营销、关系营销、绩效营销缺一不可",
            "社会责任 —— 营销不仅是商业活动，也是社会进步的驱动力",
        ]
        self._methodologies = [
            "STP分析法 —— Segment-Target-Position",
            "4P框架法 —— Product-Price-Place-Promotion",
            "顾客旅程法 —— 从认知到忠诚的全链路设计",
            "SWOT+PEST分析法 —— 系统化环境分析",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["市场", "竞争", "定位", "品牌"]):
            perspective = "从STP+4P的营销战略出发"
            insight = ("营销的核心问题是：你是谁？你为谁服务？你如何与众不同？"
                      "定位不是你对自己说什么，而是你在顾客心智中占据什么位置。")
            recs = [
                "Segmentation：你的市场可以怎么分？哪个细分最有价值？",
                "Targeting：选择最有利可图的细分市场聚焦",
                "Positioning：用一句话说清楚你和竞争对手的区别",
                "4P优化：产品/价格/渠道/推广是否一致地传递你的定位？",
            ]
        elif any(w in problem for w in ["用户", "客户", "需求", "体验"]):
            perspective = "从'以客户为中心'的营销理念出发"
            insight = ("'营销不是让你找到聪明的办法去卖东西，"
                      "而是帮你创造值得被买的东西。'")
            recs = [
                "深入理解目标客户的真实需求——不仅仅是表面需求",
                "设计顾客价值主张——你为客户解决什么问题？",
                "管理客户体验——从接触点到忠诚度的全链路",
                "建立客户关系——从交易型到关系型",
            ]
        elif any(w in problem for w in ["增长", "扩展", "发展"]):
            perspective = "从全方位营销的增长路径出发"
            insight = ("增长不是单维度的，需要从产品、渠道、传播、"
                      "客户关系四个维度同时发力。")
            recs = [
                "产品维度——产品线延伸、产品创新",
                "渠道维度——新渠道开发、全渠道整合",
                "传播维度——内容营销、口碑传播",
                "客户维度——客户获取、留存、价值提升",
            ]
        else:
            perspective = "从营销管理的系统思维出发"
            insight = ("营销不是一个部门的工作，而是整个企业的核心职能。"
                      "真正的营销是让推销变得不必要。")
            recs = [
                "先做市场调研——数据驱动决策",
                "明确目标客户——不要试图服务所有人",
                "建立品牌——品牌是最持久的竞争优势",
                "测量效果——营销是科学不是艺术",
            ]

        return AnalysisResult(
            sage_name="科特勒",
            school="营销学",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            confidence=0.90,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["客户", "用户", "需求", "价值"]):
                score += 2.0
                reasons.append("以客户为中心是营销的核心")
            if any(w in opt for w in ["品牌", "定位", "差异化"]):
                score += 1.5
                reasons.append("定位是竞争战略的核心")
            if any(w in opt for w in ["数据", "测量", "分析"]):
                score += 1.0
                reasons.append("营销是科学，需要数据支撑")
            if any(w in opt for w in ["价格战", "打折", "补贴"]):
                score -= 1.5
                reasons.append("降价是最简单的也是最危险的竞争手段")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="科特勒",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"营销学之父评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["STP战略", "顾客价值", "全方位营销"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "科特勒说：'The best way to predict the future is to create it.' "
            "营销不是让你找到聪明的办法去推销已有产品，"
            "而是帮你创造值得被买的产品。"
            "建议从三个问题开始："
            "一、你的目标客户是谁？他们的核心需求是什么？"
            "二、你能为他们创造什么独特的价值？"
            "三、你怎么让他们知道并信任这个价值？"
            "记住：做得好（产品）+ 说得好（传播）+ 买得到（渠道）= 营销成功。"
        )
__all__ = ['KotlerCloning']
