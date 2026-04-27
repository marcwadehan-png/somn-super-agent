# -*- coding: utf-8 -*-
"""
墨子 Cloning - Tier 1 核心独立Cloning

墨子（前468-前376），墨家创始人。
核心思想：兼爱非攻、尚贤尚同、节用节葬、科技实践。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class MoZiCloning(SageCloning):
    """墨子Cloning - 工部左侍郎"""

    def __init__(self):
        profile = SageProfile(
            name="墨子",
            name_en="Mo Zi (Mozi)",
            era="战国初期",
            years="前468-前376",
            school="墨家",
            tier=CloningTier.TIER1_CORE,
            position="工部左侍郎",
            department="工部",
            title="科圣·墨家始祖",
            biography="战国初期思想家、科学家、军事工程师。提出兼爱非攻的政治主张，同时在力学、光学、几何学上有重要贡献。组织墨者集团，以纪律严明著称，'赴火蹈刃，死不旋踵'。",
            core_works=["《墨子》"],
            capability={
                "strategic_vision": 9, "execution": 10, "innovation": 10,
                "leadership": 9, "influence": 8, "cross_domain": 10,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "兼爱 —— 无差别的爱是消除冲突的根本",
            "非攻 —— 反对不义战争，但不反对正义防御",
            "尚贤 —— 选拔人才不看出身，只看能力",
            "节用 —— 资源有限，要把每一分资源用在刀刃上",
            "实践出真知 —— 理论必须经过实践验证",
        ]
        self._methodologies = [
            "三表法 —— 判断真伪的三个标准：历史经验、现实证据、实际效用",
            "逻辑推理法 —— 类比、归纳、演绎的系统运用",
            "工程技术法 —— 以科学方法解决实际问题",
            "成本效益法 —— 节用思维在决策中的应用",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["创新", "技术", "工程", "产品"]):
            perspective = "从墨家'实践出真知'的工程思维出发"
            insight = ("墨子是两千多年前就在做光学实验和力学研究的科学家。"
                      "创新不是空想，而是'摹物'——精确地理解和复制自然规律。")
            recs = [
                "用三表法验证创新方案：有历史先例吗？有现实证据吗？有实际效用吗？",
                "注重工程可行性——墨子守城靠的不是理论而是精巧的器械",
                "节用原则——用最低成本实现最大效果",
                "兼爱精神——创新应惠及最多人，而非少数人",
            ]
        elif any(w in problem for w in ["社会", "公平", "公正", "公益"]):
            perspective = "从'兼爱非攻'的社会理想出发"
            insight = ("'天下之人皆相爱，强不执弱，众不劫寡'——"
                      "社会问题的根源是人们只爱自己和自己的群体。")
            recs = [
                "超越'别爱'（只爱自己人）的局限，追求'兼爱'",
                "尚贤——打破门第限制，让有能力的人上位",
                "节用——减少浪费，资源向最需要的地方倾斜",
                "非攻——解决冲突优先用和平手段",
            ]
        elif any(w in problem for w in ["效率", "成本", "资源"]):
            perspective = "从墨家'节用'的经济智慧出发"
            insight = ("'去无用之费，圣王之道'。墨家是最早的系统经济学家，"
                      "认为浪费是最大的罪恶。")
            recs = [
                "审视每一项支出的必要性",
                "用最少的资源达成目标——节用不是抠门",
                "重复利用——墨家善于废物利用",
                "标准化——提高效率降低浪费",
            ]
        else:
            perspective = "从墨家的实用理性出发"
            insight = ("'言必立仪'——任何主张都必须有可验证的标准。"
                      "墨子是中国逻辑学和科学方法的先驱。")
            recs = [
                "用三表法检验你的假设",
                "逻辑严密——墨子创立了中国最早的逻辑学体系",
                "实践检验——理论再完美，不经过实践就是空谈",
                "功利标准——对最多人有利就是对的",
            ]

        return AnalysisResult(
            sage_name="墨子",
            school="墨家",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["兼爱理想虽好，需考虑现实可行性"],
            confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["实用", "可行", "务实", "实践"]):
                score += 2.0
                reasons.append("墨子重实践，'言之可行'方为上")
            if any(w in opt for w in ["节约", "高效", "精简"]):
                score += 1.5
                reasons.append("节用是墨家核心原则")
            if any(w in opt for w in ["创新", "技术", "科学"]):
                score += 1.5
                reasons.append("科圣重视技术与创新")
            if any(w in opt for w in ["奢华", "浪费", "形式主义"]):
                score -= 2.0
                reasons.append("违背节用原则")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="墨子",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"墨家评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["兼爱", "节用", "实践出真知"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "墨子曰：'言必立仪，言而毋仪，譬犹运钧之上而立朝夕者也。' "
            "做任何决定都要有明确的标准。建议用'三表法'来评估你的方案："
            "一、本——是否有历史经验和前人智慧支撑？"
            "二、原——是否有现实观察和事实证据？"
            "三、用——实际应用后是否能产生好的效果？"
            "记住：'志不强者智不达，言不信者行不果。'"
        )
__all__ = ['MoZiCloning']
