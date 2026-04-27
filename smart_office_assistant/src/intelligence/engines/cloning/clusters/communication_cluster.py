"""
Communication Cluster - 传播学学派集群 v1.0

V6.2社会科学智慧版 - 传播学集群
基于拉斯韦尔、卢因、麦克卢汉等传播学大师

适用问题类型:
- MEDIA_EFFECTS: 媒介效果分析
- MESSAGE_DESIGN: 信息设计
- AUDIENCE_ANALYSIS: 受众分析
- PROPAGANDA_PATTERN: 宣传模式
- PUBLIC_OPINION: 公共舆论
"""

from typing import List, Dict, Optional, Any
from .._cloning_base import SageCloning, CloningTier
from .._cloning_types import (
    CloningProfile, CloningIdentity, CapabilityVector, WisdomLaw,
    AnalysisResult, DecisionOption, DecisionResult, AdviceResult,
    AssessmentResult, ConsultationMethod
)


class CommunicationCluster(SageCloning):
    """
    传播学学派集群
    
    整合拉斯韦尔、卢因、麦克卢汉、霍夫兰等大师的传播理论
    """

    def __init__(self, profile: Optional[CloningProfile] = None):
        super().__init__(profile)
        self.identity = CloningIdentity(
            name="传播学集群",
            name_pinyin="Chuanboxue Jiqun",
            era="现代",
            era_range="20世纪至今",
            title="学派集群",
            school="COMMUNICATION",
            position="传播学家",
            department="礼部",
            biography="整合拉斯韦尔、卢因、麦克卢汉、霍夫兰等大师的传播理论",
            core_thoughts=["5W模型", "媒介效果理论", "两级传播", "框架理论"]
        )
        self.tier = CloningTier.TIER_2_CLUSTER

    def get_consultation_method(self) -> ConsultationMethod:
        return ConsultationMethod.SYNTHESIS

    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        传播学分析
        
        从5W模型、媒介效果、受众分析等角度分析传播问题
        """
        query_lower = query.lower()
        context = context or {}

        frameworks = []
        key_insights = []

        # 拉斯韦尔5W模型
        if any(kw in query_lower for kw in ["传播", "沟通", "宣传", "communication", "message", "campaign"]):
            frameworks.append({
                "name": "拉斯韦尔5W模型",
                "description": "Who(传播者) → Says What(信息) → In Which Channel(媒介) → To Whom(受众) → With What Effect(效果)",
                "application": "分解传播过程，识别每个环节的优化点"
            })
            key_insights.append("传播效果取决于传播者可信度、信息编码质量、媒介适配性和受众接收度")

        # 媒介效果理论
        if any(kw in query_lower for kw in ["媒介", "媒体", "渠道", "media", "channel", "platform"]):
            frameworks.append({
                "name": "媒介效果理论",
                "description": "从魔弹论→有限效果论→强大效果论的演变",
                "application": "评估目标媒介的实际影响力范围"
            })
            key_insights.append("不同媒介对不同受众群体的渗透率和影响力差异显著")

        # 受众分析
        if any(kw in query_lower for kw in ["受众", "观众", "用户", "audience", "user", "target"]):
            frameworks.append({
                "name": "受众分析框架",
                "description": "基于人口统计特征、心理特征、行为特征的细分方法",
                "application": "识别核心受众和潜在受众群体"
            })
            key_insights.append("精准传播比泛化传播效果提升3-5倍")

        # 两级传播
        if any(kw in query_lower for kw in ["影响", "扩散", "传播", "influence", "spread", "viral"]):
            frameworks.append({
                "name": "两级传播理论（拉扎斯菲尔德）",
                "description": "信息经由意见领袖传递给普通受众",
                "application": "识别和激活关键意见领袖(KOL)"
            })
            key_insights.append("意见领袖是信息扩散的关键节点")

        # 框架效应
        if any(kw in query_lower for kw in ["框架", "叙事", "framing", "narrative", "story"]):
            frameworks.append({
                "name": "框架理论（戈夫曼）",
                "description": "信息如何被组织和呈现，影响受众解读",
                "application": "设计有效的传播框架"
            })
            key_insights.append("同一信息的不同框架可以产生截然不同的传播效果")

        return AnalysisResult(
            query=query,
            frameworks=frameworks,
            key_insights=key_insights,
            recommendations=self._generate_recommendations(frameworks),
            confidence=0.85
        )

    def decide(self, options: List[DecisionOption], criteria: Optional[Dict[str, float]] = None) -> DecisionResult:
        """
        传播学决策框架
        """
        if not options:
            return DecisionResult(
                recommended=None,
                reasoning="无决策选项提供",
                confidence=0.0,
                alternative_options=[]
            )

        criteria = criteria or {"reach": 1.0, "engagement": 1.0, "credibility": 1.0}

        # 基于传播效果的评分
        scored_options = []
        for opt in options:
            reach = getattr(opt, 'reach', 0.5)
            engagement = getattr(opt, 'engagement', 0.5)
            credibility = getattr(opt, 'credibility', 0.5)
            score = (reach * criteria.get("reach", 1.0) +
                     engagement * criteria.get("engagement", 1.0) +
                     credibility * criteria.get("credibility", 1.0)) / sum(criteria.values())
            scored_options.append((opt, score))

        best_opt, best_score = max(scored_options, key=lambda x: x[1])

        return DecisionResult(
            recommended=best_opt,
            reasoning=f"基于传播效果综合评分: {best_opt.description}",
            confidence=0.8,
            alternative_options=[opt for opt, _ in scored_options if opt != best_opt]
        )

    def advise(self, context: AdviceResult, situation: Dict[str, Any]) -> AdviceResult:
        """
        传播学建议
        """
        key_recommendations = []

        if situation.get("multi_platform"):
            key_recommendations.append("跨平台传播需保持核心信息一致，但表达形式适配各平台")

        if situation.get("crisis_comm"):
            key_recommendations.append("危机传播原则：第一时间、坦诚态度、持续更新")

        if situation.get("stakeholder"):
            key_recommendations.append("利益相关者传播需分层管理，核心受众优先")

        context.recommendations.extend(key_recommendations)
        return context

    def assess(self, subject: Any, criteria: List[str]) -> AssessmentResult:
        """
        传播学评估
        """
        bias_check = []

        if hasattr(subject, 'message'):
            msg = subject.message
            if len(msg) > 1000:
                bias_check.append("信息过长可能导致核心信息被稀释")
            if "!" in msg or "!!" in msg:
                bias_check.append("过度感叹号可能损害信息可信度")

        return AssessmentResult(
            subject=str(subject),
            criteria=criteria,
            scores={c: 0.7 for c in criteria},
            bias_analysis=bias_check,
            overall_score=0.7,
            recommendations=[
                "确保信息简洁有力",
                "适配目标受众的认知习惯"
            ]
        )


def get_cluster() -> CommunicationCluster:
    """获取传播学集群实例"""
    return CommunicationCluster()
