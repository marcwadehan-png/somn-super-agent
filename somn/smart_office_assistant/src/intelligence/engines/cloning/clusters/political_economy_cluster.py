"""
Political Economy Cluster - 政治经济学学派集群 v1.0

V1.0社会科学智慧版 - 政治经济学集群
基于凯恩斯、布坎南、诺斯等政治经济学大师

适用问题类型:
- POWER_STRUCTURE: 权力结构分析
- INTEREST_GROUP: 利益集团博弈
- PUBLIC_POLICY: 公共政策评估
- REGULATORY_FRAMEWORK: 监管框架设计
- GOVERNANCE_PATTERN: 治理模式选择
"""

from typing import List, Dict, Optional, Any
from .._cloning_base import SageCloning, CloningTier
from .._cloning_types import (
    CloningProfile, CloningIdentity, CapabilityVector, WisdomLaw,
    AnalysisResult, DecisionOption, DecisionResult, AdviceResult,
    AssessmentResult, ConsultationMethod
)


class PoliticalEconomyCluster(SageCloning):
    """
    政治经济学学派集群
    
    整合凯恩斯、布坎南、诺斯等大师的政治经济学思想
    """

    def __init__(self, profile: Optional[CloningProfile] = None):
        super().__init__(profile)
        self.identity = CloningIdentity(
            name="政治经济学集群",
            name_pinyin="Zhengzhi Jingjixue Jiqun",
            era="现代",
            era_range="18世纪至今",
            title="学派集群",
            school="POLITICAL_ECONOMICS",
            position="政治经济学家",
            department="户部",
            biography="整合凯恩斯、布坎南、诺斯等大师的政治经济学思想",
            core_thoughts=["公共选择理论", "制度经济学", "国家理论", "利益集团理论"]
        )
        self.tier = CloningTier.TIER_2_CLUSTER

    def get_consultation_method(self) -> ConsultationMethod:
        return ConsultationMethod.DEBATE

    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        政治经济学分析
        
        从权力结构、利益博弈、制度变迁等角度分析
        """
        query_lower = query.lower()
        context = context or {}

        frameworks = []
        key_insights = []

        # 公共选择理论
        if any(kw in query_lower for kw in ["政策", "政府", "监管", "policy", "government", "regulation"]):
            frameworks.append({
                "name": "公共选择理论（布坎南）",
                "description": "政府官员和政治人物也是追求自身利益的经济人",
                "application": "分析政策的实际受益者和决策动机"
            })
            key_insights.append("好的制度设计可以约束官僚自利行为")

        # 制度经济学
        if any(kw in query_lower for kw in ["制度", "规则", "institution", "rules", "system"]):
            frameworks.append({
                "name": "制度经济学（诺斯）",
                "description": "制度决定交易成本，影响经济绩效",
                "application": "评估制度变迁的成本和收益"
            })
            key_insights.append("制度是经济发展的核心变量")

        # 国家理论
        if any(kw in query_lower for kw in ["国家", "权力", "authority", "power", "state"]):
            frameworks.append({
                "name": "国家理论（诺斯）",
                "description": "国家有两个目的：界定产权和收取租金",
                "application": "分析国家行为的双重动机"
            })
            key_insights.append("国家的激励结构决定了政策走向")

        # 利益集团
        if any(kw in query_lower for kw in ["利益", "集团", "lobby", "interest", "group"]):
            frameworks.append({
                "name": "利益集团理论",
                "description": "不同利益集团通过游说、献金等方式影响政策",
                "application": "识别相关利益集团及其影响力"
            })
            key_insights.append("政策往往是利益集团博弈的结果")

        # 权力结构
        if any(kw in query_lower for kw in ["权力", "控制", "支配", "power", "control", "dominance"]):
            frameworks.append({
                "name": "权力结构分析",
                "description": "谁有权力、权力的来源、权力的运用方式",
                "application": "绘制权力结构和影响力网络"
            })
            key_insights.append("理解权力结构是改变现状的前提")

        return AnalysisResult(
            query=query,
            frameworks=frameworks,
            key_insights=key_insights,
            recommendations=self._generate_recommendations(frameworks),
            confidence=0.85
        )

    def decide(self, options: List[DecisionOption], criteria: Optional[Dict[str, float]] = None) -> DecisionResult:
        """
        政治经济学决策框架
        """
        if not options:
            return DecisionResult(
                recommended=None,
                reasoning="无决策选项提供",
                confidence=0.0,
                alternative_options=[]
            )

        criteria = criteria or {"feasibility": 1.0, "equity": 1.0, "stability": 1.0}
        scored_options = []

        for opt in options:
            feasibility = getattr(opt, 'political_feasibility', 0.5)
            equity = getattr(opt, 'distributional_equity', 0.5)
            stability = getattr(opt, 'system_stability', 0.5)
            score = (feasibility * criteria.get("feasibility", 1.0) +
                     equity * criteria.get("equity", 1.0) +
                     stability * criteria.get("stability", 1.0)) / sum(criteria.values())
            scored_options.append((opt, score))

        best_opt, best_score = max(scored_options, key=lambda x: x[1])

        return DecisionResult(
            recommended=best_opt,
            reasoning=f"基于政治经济学评分: {best_opt.description}",
            confidence=0.78,
            alternative_options=[opt for opt, _ in scored_options if opt != best_opt]
        )

    def advise(self, context: AdviceResult, situation: Dict[str, Any]) -> AdviceResult:
        """
        政治经济学建议
        """
        key_warnings = []

        if situation.get("reform"):
            key_warnings.append("制度变迁存在路径依赖，既得利益者会抵制改革")

        if situation.get("coalition"):
            key_warnings.append("建立改革联盟需要识别各方利益交汇点")

        context.warnings.extend(key_warnings)
        return context

    def assess(self, subject: Any, criteria: List[str]) -> AssessmentResult:
        """
        政治经济学评估
        """
        return AssessmentResult(
            subject=str(subject),
            criteria=criteria,
            scores={c: 0.7 for c in criteria},
            bias_analysis=[],
            overall_score=0.7,
            recommendations=[
                "考虑政策的政治可行性和可持续性",
                "评估各利益相关方的反应"
            ]
        )


def get_cluster() -> PoliticalEconomyCluster:
    """获取政治经济学集群实例"""
    return PoliticalEconomyCluster()
