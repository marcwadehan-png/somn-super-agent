"""
Organizational Psychology Cluster - 组织心理学学派集群 v1.0

V6.2社会科学智慧版 - 组织心理学集群
基于沙因、勒温、阿吉里斯等组织心理学大师

适用问题类型:
- ORGANIZATIONAL_CULTURE: 组织文化诊断
- GROUP_DYNAMICS: 群体动力学
- LEADERSHIP_STYLE: 领导风格评估
- WORK_MOTIVATION: 工作动机分析
- CONFLICT_RESOLUTION: 冲突解决
"""

from typing import List, Dict, Optional, Any
from .._cloning_base import SageCloning, CloningTier
from .._cloning_types import (
    CloningProfile, CloningIdentity, CapabilityVector, WisdomLaw,
    AnalysisResult, DecisionOption, DecisionResult, AdviceResult,
    AssessmentResult, ConsultationMethod
)


class OrganizationalPsychologyCluster(SageCloning):
    """
    组织心理学学派集群
    
    整合沙因、勒温、阿吉里斯等组织心理学大师
    """

    def __init__(self, profile: Optional[CloningProfile] = None):
        super().__init__(profile)
        self.identity = CloningIdentity(
            name="组织心理学集群",
            name_pinyin="Zuzhi Xinlixue Jiqun",
            era="现代",
            era_range="20世纪至今",
            title="学派集群",
            school="ORGANIZATIONAL_PSYCHOLOGY",
            position="组织心理学家",
            department="吏部",
            biography="整合沙因、勒温、阿吉里斯等组织心理学大师",
            core_thoughts=["组织文化三层次", "群体动力学", "行动研究", "建设性冲突"]
        )
        self.tier = CloningTier.TIER_2_CLUSTER

    def get_consultation_method(self) -> ConsultationMethod:
        return ConsultationMethod.SYNTHESIS

    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        组织心理学分析
        
        从组织文化、群体动力、领导风格等角度分析
        """
        query_lower = query.lower()
        context = context or {}

        frameworks = []
        key_insights = []

        # 组织文化三层次
        if any(kw in query_lower for kw in ["文化", "氛围", "culture", "atmosphere", "climate"]):
            frameworks.append({
                "name": "组织文化三层次（沙因）",
                "description": "人工制品(可见) → 价值观(倡导) → 基本假设(深层)",
                "application": "诊断组织文化的真实状态"
            })
            key_insights.append("表层文化可能掩盖深层的基本假设")

        # 群体动力学
        if any(kw in query_lower for kw in ["团队", "群体", "team", "group", "collaboration"]):
            frameworks.append({
                "name": "群体动力学（勒温）",
                "description": "群体行为由个体特征、群体动力和环境共同决定",
                "application": "分析团队效能的影响因素"
            })
            key_insights.append("群体规范对个体行为的影响往往超过个体理性")

        # 行动研究
        if any(kw in query_lower for kw in ["变革", "干预", "change", "intervention", "improvement"]):
            frameworks.append({
                "name": "行动研究（勒温）",
                "description": "研究即行动，行动即研究（小步快跑、持续迭代）",
                "application": "设计组织变革方案"
            })
            key_insights.append("小规模实验比大规模推倒重来更有效")

        # 领导力理论
        if any(kw in query_lower for kw in ["领导", "管理", "leader", "leadership", "management"]):
            frameworks.append({
                "name": "领导力情境理论（菲德勒）",
                "description": "有效的领导风格取决于情境因素",
                "application": "评估领导风格与情境的匹配度"
            })
            key_insights.append("没有万能的领导风格，关键是匹配情境")

        # 建设性冲突
        if any(kw in query_lower for kw in ["冲突", "矛盾", "dispute", "conflict", "tension"]):
            frameworks.append({
                "name": "建设性冲突理论",
                "description": "适度的认知冲突可以提升决策质量",
                "application": "管理冲突从破坏性到建设性"
            })
            key_insights.append("避免冲突不等于解决冲突，只是延迟爆发")

        return AnalysisResult(
            query=query,
            frameworks=frameworks,
            key_insights=key_insights,
            recommendations=self._generate_recommendations(frameworks),
            confidence=0.85
        )

    def decide(self, options: List[DecisionOption], criteria: Optional[Dict[str, float]] = None) -> DecisionResult:
        """
        组织心理学决策框架
        """
        if not options:
            return DecisionResult(
                recommended=None,
                reasoning="无决策选项提供",
                confidence=0.0,
                alternative_options=[]
            )

        criteria = criteria or {"people_impact": 1.0, "engagement": 1.0, "sustainability": 1.0}
        scored_options = []

        for opt in options:
            people_impact = getattr(opt, 'people_impact', 0.5)
            engagement = getattr(opt, 'employee_engagement', 0.5)
            sustainability = getattr(opt, 'org_sustainability', 0.5)
            score = (people_impact * criteria.get("people_impact", 1.0) +
                     engagement * criteria.get("engagement", 1.0) +
                     sustainability * criteria.get("sustainability", 1.0)) / sum(criteria.values())
            scored_options.append((opt, score))

        best_opt, best_score = max(scored_options, key=lambda x: x[1])

        return DecisionResult(
            recommended=best_opt,
            reasoning=f"基于组织心理学评分: {best_opt.description}",
            confidence=0.8,
            alternative_options=[opt for opt, _ in scored_options if opt != best_opt]
        )

    def advise(self, context: AdviceResult, situation: Dict[str, Any]) -> AdviceResult:
        """
        组织心理学建议
        """
        key_recommendations = []

        if situation.get("team_building"):
            key_recommendations.append("团队建设应关注心理安全感，让成员敢于表达")

        if situation.get("change_management"):
            key_recommendations.append("变革管理需要关注员工的心理过渡期")

        if situation.get("leadership"):
            key_recommendations.append("领导者应平衡任务导向与人际导向")

        context.recommendations.extend(key_recommendations)
        return context

    def assess(self, subject: Any, criteria: List[str]) -> AssessmentResult:
        """
        组织心理学评估
        """
        return AssessmentResult(
            subject=str(subject),
            criteria=criteria,
            scores={c: 0.7 for c in criteria},
            bias_analysis=[],
            overall_score=0.7,
            recommendations=[
                "关注员工的心理感受和体验",
                "建立持续反馈的机制"
            ]
        )


def get_cluster() -> OrganizationalPsychologyCluster:
    """获取组织心理学集群实例"""
    return OrganizationalPsychologyCluster()
