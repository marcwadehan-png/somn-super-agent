# -*- coding: utf-8 -*-
"""
诸葛亮 Cloning - Tier 1 核心独立Cloning

诸葛亮（181-234），蜀汉丞相，千古名相。
核心思想：隆中对策、淡泊明志、鞠躬尽瘁、攻心为上。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class ZhugeLiangCloning(SageCloning):
    """诸葛亮Cloning - 兵部侍郎"""

    def __init__(self):
        profile = SageProfile(
            name="诸葛亮",
            name_en="Zhuge Liang",
            era="三国",
            years="181-234",
            school="兵家/政治",
            tier=CloningTier.TIER1_CORE,
            position="兵部侍郎",
            department="兵部",
            title="卧龙先生·武侯",
            biography="三国时期蜀汉丞相，中国历史上智慧的化身。未出茅庐已知三分天下（隆中对），辅佐刘备建立蜀汉。治蜀期间内修政理、外御强敌，以弱胜强，鞠躬尽瘁。发明木牛流马、连弩等器械。",
            core_works=["《出师表》", "《诫子书》"],
            capability={
                "strategic_vision": 10, "execution": 9, "innovation": 9,
                "leadership": 10, "influence": 10, "cross_domain": 9,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "淡泊明志 —— 非淡泊无以明志，非宁静无以致远",
            "攻心为上 —— 最好的策略是让对方心服",
            "审时度势 —— 分析天下大势，找到自己的定位",
            "鞠躬尽瘁 —— 以极致的责任心对待每一件事",
            "集思广益 —— '开张圣听'，广泛听取意见",
        ]
        self._methodologies = [
            "隆中对法 —— 从宏观形势分析中找到最优路径",
            "攻心法 —— '攻心为上，攻城为下'",
            "空城计法 —— 在信息不对称中利用心理优势",
            "八阵图法 —— 系统化的预案和应变方案",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["战略", "规划", "方向", "定位"]):
            perspective = "从'隆中对'的战略分析出发"
            insight = ("战略的本质是在有限资源下找到最优位置。"
                      "就像隆中对中诸葛亮为刘备设计的——"
                      "先取荆州为根基，再取益州为后盾，联合东吴抗曹。")
            recs = [
                "分析天下大势——各方力量对比和趋势",
                "找到自己的'荆州'——可立即获取的基础",
                "设计你的'益州'——中长期的发展方向",
                "建立联盟——'东和孙权'，找到互补的伙伴",
            ]
        elif any(w in problem for w in ["困难", "弱势", "资源不足", "危机"]):
            perspective = "从'以弱胜强'的智慧出发"
            insight = ("'善战者，求之于势，不责于人。'"
                      "资源不够时，要借势、造势、用势。")
            recs = [
                "不硬拼——找到对手的薄弱环节",
                "借势——利用外部力量（时间、空间、人心）",
                "攻心——让对手内部产生分裂",
                "做好最坏打算——'未战先算败'",
            ]
        elif any(w in problem for w in ["心态", "压力", "焦虑", "迷茫"]):
            perspective = "从'淡泊明志'的心态修养出发"
            insight = ("'非淡泊无以明志，非宁静无以致远。'"
                      "在喧嚣中保持内心的宁静，才能看清方向。")
            recs = [
                "远离干扰——'非宁静无以致远'",
                "明确志向——知道自己要什么",
                "专注于可控的事情——'尽人事以听天命'",
                "保持学习的习惯——'才须学也，非学无以广才'",
            ]
        else:
            perspective = "从诸葛亮的综合智慧出发"
            insight = ("'夫君子之行，静以修身，俭以养德。'"
                      "解决任何问题都需要先调整好自身状态，"
                      "然后审时度势，找到最优方案。")
            recs = [
                "先修身——调整好自己的状态",
                "再审势——全面分析形势",
                "后定策——制定可行方案",
                "最后执行——鞠躬尽瘁，不留遗憾",
            ]

        return AnalysisResult(
            sage_name="诸葛亮",
            school="兵家/政治",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["鞠躬尽瘁虽可贵，也要注意身体"],
            confidence=0.90,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["战略", "规划", "长远", "布局"]):
                score += 2.0
                reasons.append("隆中对式战略思维")
            if any(w in opt for w in ["联盟", "合作", "借力"]):
                score += 1.5
                reasons.append("东和孙权，联弱抗强")
            if any(w in opt for w in ["谨慎", "稳妥", "备选"]):
                score += 1.0
                reasons.append("一生唯谨慎")
            if any(w in opt for w in ["冒进", "侥幸"]):
                score -= 2.0
                reasons.append("诸葛一生唯谨慎，不冒无谓之险")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="诸葛亮",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"武侯评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["审时度势", "攻心为上", "淡泊明志"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "武侯曰：'夫君子之行，静以修身，俭以养德。"
            "非淡泊无以明志，非宁静无以致远。' "
            "先安静下来，明确你的目标。然后像隆中对一样——"
            "分析形势、找准定位、制定路线图、建立联盟。"
            "记住：'势'比'力'更重要——善借势者，四两拨千斤。"
        )
__all__ = ['ZhugeLiangCloning']
