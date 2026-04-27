"""
Social Psychology Cluster - 社会心理学学派集群 v1.0

V1.0社会科学智慧版 - 社会心理学集群
基于阿伦森、米尔格拉姆、津巴多等社会心理学大师

适用问题类型:
- ATTITUDE_CHANGE: 态度改变机制
- PERSUASION_MECHANISM: 说服机制
- GROUP_INFLUENCE: 群体影响
- SELF_PERCEPTION: 自我知觉
- SOCIAL_IDENTITY: 社会认同
"""

from typing import List, Dict, Optional, Any
from .._cloning_base import SageCloning, CloningTier
from .._cloning_types import (
    CloningProfile, CloningIdentity, CapabilityVector, WisdomLaw,
    AnalysisResult, DecisionOption, DecisionResult, AdviceResult,
    AssessmentResult, ConsultationMethod
)


class SocialPsychologyCluster(SageCloning):
    """
    社会心理学学派集群
    
    整合阿伦森、米尔格拉姆、津巴多等社会心理学大师
    """

    def __init__(self, profile: Optional[CloningProfile] = None):
        super().__init__(profile)
        self.identity = CloningIdentity(
            name="社会心理学集群",
            name_pinyin="Shehui Xinlixue Jiqun",
            era="现代",
            era_range="20世纪至今",
            title="学派集群",
            school="SOCIAL_PSYCHOLOGY",
            position="社会心理学家",
            department="礼部",
            biography="整合阿伦森、米尔格拉姆、津巴多等社会心理学大师",
            core_thoughts=["认知失调理论", "从众研究", "服从实验", "说服双路径模型"]
        )
        self.tier = CloningTier.TIER_2_CLUSTER

    def get_consultation_method(self) -> ConsultationMethod:
        return ConsultationMethod.SYNTHESIS

    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        社会心理学分析
        
        从态度改变、说服机制、群体影响等角度分析
        """
        query_lower = query.lower()
        context = context or {}

        frameworks = []
        key_insights = []

        # 认知失调理论
        if any(kw in query_lower for kw in ["态度", "信念", "矛盾", "attitude", "belief", "dissonance"]):
            frameworks.append({
                "name": "认知失调理论（费斯廷格）",
                "description": "当行为与信念不一致时，产生心理不适，驱动态度改变",
                "application": "分析为何某些信息难以被接受"
            })
            key_insights.append("减少认知失调的动机往往强于理性说服")

        # 从众实验
        if any(kw in query_lower for kw in ["群体", "社会", "从众", "group", "social", "conformity"]):
            frameworks.append({
                "name": "从众研究（阿希）",
                "description": "约75%的人在群体压力下会从众，即使明显错误",
                "application": "识别可能导致集体盲从的情境"
            })
            key_insights.append("群体决策需要机制来保护少数意见")

        # 服从实验
        if any(kw in query_lower for kw in ["服从", "权威", "authority", "obedience", "compliance"]):
            frameworks.append({
                "name": "服从研究（米尔格拉姆）",
                "description": "65%的普通人在权威命令下会对他人造成伤害",
                "application": "反思权威对个体行为的影响"
            })
            key_insights.append("不要低估权威对普通人行为的塑造能力")

        # 说服的双路径模型
        if any(kw in query_lower for kw in ["说服", "影响", "改变", "persuade", "influence", "change"]):
            frameworks.append({
                "name": "精细加工可能性模型（ELM）",
                "description": "中央路径(理性论证) vs 边缘路径(感性暗示)",
                "application": "根据受众特征选择说服路径"
            })
            key_insights.append("高涉入受众适合中央路径，低涉入受众适合边缘路径")

        # 社会认同理论
        if any(kw in query_lower for kw in ["认同", "身份", "群体", "identity", "group", "belonging"]):
            frameworks.append({
                "name": "社会认同理论（ Tajfel & Turner）",
                "description": "个体的自我概念部分来源于群体成员身份",
                "application": "理解群体认同如何影响行为"
            })
            key_insights.append("人们倾向于支持自己群体的利益")

        # 旁观者效应
        if any(kw in query_lower for kw in ["责任", "紧急", "帮助", "responsibility", "emergency", "help"]):
            frameworks.append({
                "name": "旁观者效应（达利 & 拉塔内）",
                "description": "他人在场时，个体提供帮助的概率降低",
                "application": "设计促进个体行动的机制"
            })
            key_insights.append("分散责任会显著降低行动意愿")

        return AnalysisResult(
            query=query,
            frameworks=frameworks,
            key_insights=key_insights,
            recommendations=self._generate_recommendations(frameworks),
            confidence=0.88
        )

    def decide(self, options: List[DecisionOption], criteria: Optional[Dict[str, float]] = None) -> DecisionResult:
        """
        社会心理学决策框架
        """
        if not options:
            return DecisionResult(
                recommended=None,
                reasoning="无决策选项提供",
                confidence=0.0,
                alternative_options=[]
            )

        criteria = criteria or {"social_acceptance": 1.0, "persuasion": 1.0, "engagement": 1.0}
        scored_options = []

        for opt in options:
            social = getattr(opt, 'social_acceptance', 0.5)
            persuasion = getattr(opt, 'persuasion_power', 0.5)
            engagement = getattr(opt, 'social_engagement', 0.5)
            score = (social * criteria.get("social_acceptance", 1.0) +
                     persuasion * criteria.get("persuasion", 1.0) +
                     engagement * criteria.get("engagement", 1.0)) / sum(criteria.values())
            scored_options.append((opt, score))

        best_opt, best_score = max(scored_options, key=lambda x: x[1])

        return DecisionResult(
            recommended=best_opt,
            reasoning=f"基于社会心理学评分: {best_opt.description}",
            confidence=0.82,
            alternative_options=[opt for opt, _ in scored_options if opt != best_opt]
        )

    def advise(self, context: AdviceResult, situation: Dict[str, Any]) -> AdviceResult:
        """
        社会心理学建议
        """
        key_warnings = []
        key_recommendations = []

        if situation.get("group_decision"):
            key_warnings.append("群体决策需要防止极化和从众偏差")
            key_recommendations.append("引入魔鬼代言人角色挑战主流意见")

        if situation.get("authority"):
            key_warnings.append("警惕权威对判断的不当影响")

        if situation.get("persuasion"):
            key_recommendations.append("高可信度信源+有力论据是说服的关键组合")

        context.warnings.extend(key_warnings)
        context.recommendations.extend(key_recommendations)
        return context

    def assess(self, subject: Any, criteria: List[str]) -> AssessmentResult:
        """
        社会心理学评估
        """
        bias_check = []

        if hasattr(subject, 'description'):
            desc = subject.description.lower()
            if "大家" in desc or "everyone" in desc or "所有人都" in desc:
                bias_check.append("所有人表述可能高估社会一致性")
            if "明显" in desc or "clearly" in desc:
                bias_check.append("明显的表述可能低估了问题的复杂性")

        return AssessmentResult(
            subject=str(subject),
            criteria=criteria,
            scores={c: 0.7 for c in criteria},
            bias_analysis=bias_check,
            overall_score=0.7,
            recommendations=[
                "考虑社会情境对行为的放大效应",
                "设计减少从众偏差的机制"
            ]
        )


def get_cluster() -> SocialPsychologyCluster:
    """获取社会心理学集群实例"""
    return SocialPsychologyCluster()
