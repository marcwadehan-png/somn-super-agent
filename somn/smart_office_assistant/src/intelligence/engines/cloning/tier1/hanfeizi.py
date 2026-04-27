# -*- coding: utf-8 -*-
"""
韩非子 Cloning - Tier 1 核心独立Cloning

韩非（前280-前233），法家集大成者。
核心思想：法术势三位一体、以法治国、人性本恶、赏罚分明。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class HanFeiZiCloning(SageCloning):
    """韩非子Cloning - 刑部尚书"""

    def __init__(self):
        profile = SageProfile(
            name="韩非子",
            name_en="Han Fei Zi",
            era="战国末期",
            years="前280-前233",
            school="法家",
            tier=CloningTier.TIER1_CORE,
            position="刑部尚书",
            department="刑部",
            title="法家集大成者",
            biography="战国末期韩国贵族，师从荀子，融合商鞅的'法'、申不害的'术'、慎到的'势'，形成完整的法家思想体系。其理论被秦王嬴政实践，助秦国统一六国。",
            core_works=["《韩非子》"],
            capability={
                "strategic_vision": 9, "execution": 10, "innovation": 8,
                "leadership": 8, "influence": 9, "cross_domain": 7,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "法术势结合 —— 制度(法)、权术(术)、权威(势)缺一不可",
            "以法治国 —— 规则面前人人平等，去除人为干预",
            "人性趋利避害 —— 制度设计必须基于对人性的清醒认知",
            "赏罚分明 —— 重赏重罚，让违规成本远大于收益",
            "循名责实 —— 职位与实际能力匹配，言与行一致",
        ]
        self._methodologies = [
            "利益分析法 —— 从人的趋利避害本性出发分析行为",
            "制度设计法 —— 设计让'坏人'也无法做坏事的制度",
            "权责匹配法 —— 循名责实，名实相符",
            "二柄法 —— 赏罚二柄，两手都要硬",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["管理", "制度", "规则", "治理"]):
            perspective = "从'法术势'三位一体的制度设计出发"
            insight = ("好的制度不需要圣人执行——它应该让普通人也能做好，"
                      "让坏人做不了坏事。制度设计的核心是'二柄'：赏和罚。")
            recs = [
                "明确规则并公开透明——'法莫如显'",
                "赏罚必须坚决执行——'信赏必罚'",
                "去掉'人情'干扰——制度不应因人而异",
                "建立监督机制——'术'用于防止权力被滥用",
            ]
        elif any(w in problem for w in ["激励", "绩效", "考核"]):
            perspective = "从'二柄'——赏罚权术出发"
            insight = ("激励的本质是利益的精准调控。'赏厚而信，罚重而必'——"
                      "奖励要足够有吸引力且及时兑现，惩罚要足够严厉且必然执行。")
            recs = [
                "设计让努力>偷懒的激励结构",
                "让违规成本远大于违规收益",
                "赏罚标准明确、公开、不可随意更改",
                "赏罚执行要快速，延迟会降低效果",
            ]
        elif any(w in problem for w in ["用人", "人才", "招聘", "选拔"]):
            perspective = "从'循名责实'的人才管理出发"
            insight = ("'宰相必起于州部，猛将必发于卒伍'——"
                      "人才要从基层实战中选拔，而非空降。能力要和职位匹配。")
            recs = [
                "以实际成果衡量人才，不看简历和学历",
                "言必信，行必果——说到的必须做到",
                "职位与能力匹配——大材小用浪费，小材大用灾难",
                "建立能上能下的机制，避免论资排辈",
            ]
        else:
            perspective = "从法家的现实主义分析框架出发"
            insight = ("不要指望人性的善良，要基于人性的现实来设计解决方案。"
                      "'法之所加，智者弗能辞，勇者弗敢争'——制度的力量超越个人。")
            recs = [
                "假设最坏情况，设计兜底方案",
                "用制度而非道德约束行为",
                "利益驱动是最可靠的驱动力",
                "权力必须受到制约——'势'需要'术'来平衡",
            ]

        return AnalysisResult(
            sage_name="韩非子",
            school="法家",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["法家之术过于冷酷，需以儒家仁义调和"],
            confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["制度", "规则", "标准", "流程"]):
                score += 2.0
                reasons.append("以法治之，制度是根本")
            if any(w in opt for w in ["人情", "关系", "感情", "道德"]):
                score -= 1.5
                reasons.append("人情不可恃，制度才可靠")
            if any(w in opt for w in ["赏罚", "激励", "考核"]):
                score += 1.5
                reasons.append("明赏罚，二柄在手")
            if any(w in opt for w in ["放权", "自治", "宽松"]):
                score -= 1.0
                reasons.append("权不可失，势不可弱")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="韩非子",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"法家评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["法术势结合", "以法治国", "循名责实"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "韩非曰：'千里之堤，毁于蚁穴。' 问题的根源往往在细节。"
            "建议从'法术势'三个维度审视："
            "一、'法'——有没有明确的规则？规则是否被执行？"
            "二、'术'——有没有有效的监督机制？信息是否通畅？"
            "三、'势'——你的权威是否足够？资源是否到位？"
            "记住：'爱多者则法不立，威寡者则下侵上。' "
            "过度的仁慈会削弱制度，威信不足则会被架空。"
        )
__all__ = ['HanFeiZiCloning']
