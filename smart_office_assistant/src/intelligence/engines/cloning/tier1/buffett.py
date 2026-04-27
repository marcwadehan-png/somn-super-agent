# -*- coding: utf-8 -*-
"""
巴菲特 Cloning - Tier 1 核心独立Cloning

沃伦·巴菲特（1930-），投资大师，伯克希尔·哈撒韦CEO。
核心思想：价值投资、能力圈、护城河、长期主义、安全边际。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class BuffettCloning(SageCloning):
    """巴菲特Cloning - 户部·理财司"""

    def __init__(self):
        profile = SageProfile(
            name="巴菲特",
            name_en="Warren Buffett",
            era="20-21世纪",
            years="1930-",
            school="价值投资",
            tier=CloningTier.TIER1_CORE,
            position="户部·理财司",
            department="户部",
            title="奥马哈先知·投资大师",
            biography="美国投资家、企业家、慈善家，伯克希尔·哈撒韦公司董事长兼CEO。以价值投资理念闻名于世，长期位居全球富豪榜前列。将格雷厄姆的安全边际理论与费雪的成长股理论融合，形成独特的投资哲学。",
            core_works=["《巴菲特致股东的信》"],
            capability={
                "strategic_vision": 10, "execution": 9, "innovation": 7,
                "leadership": 9, "influence": 10, "cross_domain": 8,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "能力圈 —— 只投资你真正理解的东西",
            "安全边际 —— 以远低于内在价值的价格买入",
            "护城河 —— 寻找具有持久竞争优势的企业",
            "长期主义 —— 我最喜欢的持有期是永远",
            "别人贪婪我恐惧 —— 逆向思维是超额收益的来源",
        ]
        self._methodologies = [
            "价值评估法 —— DCF模型+比较分析",
            "护城河分析 —— 品牌/成本/网络/转换/规模五种护城河",
            "能力圈检查 —— 诚实评估自己是否真的理解",
            "逆向思维法 —— 别人恐惧时贪婪，别人贪婪时恐惧",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["投资", "理财", "资金", "回报"]):
            perspective = "从价值投资的核心理念出发"
            insight = ("'投资的第一条原则是不要亏钱，第二条原则是永远不要忘记第一条。'"
                      "价值投资的本质是以低于内在价值的价格买入好公司。")
            recs = [
                "评估内在价值——这家公司值多少钱？",
                "检查护城河——它的竞争优势能持续多久？",
                "留足安全边际——即使判断失误也不会亏太多",
                "确认在能力圈内——你真的理解这门生意吗？",
            ]
        elif any(w in problem for w in ["决策", "选择", "风险"]):
            perspective = "从'能力圈+安全边际'的决策框架出发"
            insight = ("好的决策不在于你能多准确地预测未来，"
                      "而在于你在不确定中如何保护自己。")
            recs = [
                "明确自己的能力边界——不懂的不碰",
                "留足安全边际——为不确定预留缓冲",
                "长期视角——不要因为短期波动改变决策",
                "独立思考——不要随大流",
            ]
        elif any(w in problem for w in ["商业模式", "竞争", "护城河"]):
            perspective = "从'经济护城河'的分析框架出发"
            insight = ("'一家真正伟大的公司必须有一条坚固的'护城河'来保护其高回报。'"
                      "护城河有五种：品牌、成本优势、网络效应、转换成本、规模效应。")
            recs = [
                "品牌——用户愿意为这个品牌付溢价吗？",
                "成本——它的成本结构是否比对手低？",
                "网络——用户越多价值越大吗？",
                "转换——用户换用的成本高吗？",
                "规模——规模大是否带来成本优势？",
            ]
        else:
            perspective = "从巴菲特的长期主义哲学出发"
            insight = ("'如果你不愿意拥有一只股票10年，那就不要考虑拥有它10分钟。'"
                      "长远看，价值决定价格。")
            recs = [
                "以10年为周期思考问题",
                "关注长期价值而非短期价格",
                "简单优于复杂——避开你不懂的东西",
                "耐心是最好的策略",
            ]

        return AnalysisResult(
            sage_name="巴菲特",
            school="价值投资",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            confidence=0.91,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["安全", "保守", "稳健", "长期"]):
                score += 2.0
                reasons.append("安全边际第一，长期持有")
            if any(w in opt for w in ["价值", "内在", "基本面"]):
                score += 2.0
                reasons.append("以价值而非价格做判断")
            if any(w in opt for w in ["投机", "短线", "追涨"]):
                score -= 3.0
                reasons.append("投机是赌博，不是投资")
            if any(w in opt for w in ["能力圈", "熟悉", "理解"]):
                score += 1.5
                reasons.append("能力圈内，确定性高")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="巴菲特",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"价值投资评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["能力圈", "安全边际", "护城河"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "巴菲特说：'Rule No. 1: Never lose money. "
            "Rule No. 2: Never forget Rule No. 1.' "
            "在做任何决策之前，先评估最坏的情况。"
            "如果最坏的情况你能承受，而且长期来看有价值，那就做。"
            "记住：'别人贪婪我恐惧，别人恐惧我贪婪。' "
            "当所有人都看好时，反而要谨慎；当所有人都悲观时，也许是机会。"
        )
__all__ = ['BuffettCloning']
