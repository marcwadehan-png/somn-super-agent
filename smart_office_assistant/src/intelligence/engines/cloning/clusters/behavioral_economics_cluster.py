"""
Behavioral Economics Cluster - 行为经济学学派集群 v1.0

V6.2社会科学智慧版 - 行为经济学集群
基于西蒙有限理性、卡尼曼前景理论、塞勒助推理论

适用问题类型:
- HEURISTIC_BIAS: 启发式偏差分析
- NUDGE_DESIGN: 助推设计
- LOSS_AVERSION: 损失厌恶
- PROSPECT_THEORY: 前景理论
- TIME_INCONSISTENCY: 时间不一致性
"""

from typing import List, Dict, Optional, Any
from .._cloning_base import SageCloning, CloningTier
from .._cloning_types import (
    CloningProfile, CloningIdentity, CapabilityVector, WisdomLaw,
    AnalysisResult, DecisionOption, DecisionResult, AdviceResult,
    AssessmentResult, ConsultationMethod, ClusterResult
)


class BehavioralEconomicsCluster(SageCloning):
    """
    行为经济学学派集群
    
    整合西蒙、卡尼曼、塞勒、特沃斯基等大师的思想框架
    """

    def __init__(self, profile: Optional[CloningProfile] = None):
        super().__init__(profile)
        # 设置身份信息
        self.identity = CloningIdentity(
            name="行为经济学集群",
            name_pinyin="Xingwei Jingjixue Jiqun",
            era="现代",
            era_range="20世纪至今",
            title="学派集群",
            school="BEHAVIORAL_ECONOMICS",
            position="行为经济学家",
            department="户部",
            biography="整合西蒙、卡尼曼、塞勒、特沃斯基等大师的思想框架",
            core_thoughts=["有限理性理论", "前景理论", "助推理论", "双曲贴现"]
        )
        self.tier = CloningTier.TIER_2_CLUSTER

    def get_consultation_method(self) -> ConsultationMethod:
        return ConsultationMethod.SYNTHESIS

    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        行为经济学分析
        
        从有限理性、认知偏差、决策启发式等角度分析问题
        """
        query_lower = query.lower()
        context = context or {}

        # 分析框架
        frameworks = []
        key_insights = []

        # 有限理性分析
        if any(kw in query_lower for kw in ["决策", "选择", "判断", "decision", "choice"]):
            frameworks.append({
                "name": "有限理性理论（西蒙）",
                "description": "人类决策受限于认知能力和信息获取，只能追求满意解而非最优解",
                "application": "评估当前决策的理性边界和可改进空间"
            })
            key_insights.append("决策者的有限理性是设计系统和流程的关键约束")

        # 损失厌恶分析
        if any(kw in query_lower for kw in ["损失", "风险", "收益", "loss", "risk", "gain"]):
            frameworks.append({
                "name": "前景理论（卡尼曼）",
                "description": "人们对损失的敏感度是同等收益的2倍（损失厌恶系数≈2）",
                "application": "评估方案的损失框架对决策者吸引力的影响"
            })
            key_insights.append("损失框架比收益框架更具说服力（但需谨慎使用）")

        # 锚定效应
        if any(kw in query_lower for kw in ["定价", "估值", "谈判", "price", "value", "negotiate"]):
            frameworks.append({
                "name": "锚定效应（特沃斯基）",
                "description": "初始信息（锚点）对后续判断产生系统性偏差",
                "application": "识别可能被锚定效应影响的决策点"
            })
            key_insights.append("先发制人的信息设置可以影响后续判断")

        # 助推设计
        if any(kw in query_lower for kw in ["设计", "引导", "推动", "design", "nudge", "guide"]):
            frameworks.append({
                "name": "助推理论（塞勒）",
                "description": "通过选择架构的正向改变，在不强制限制的情况下引导行为",
                "application": "设计促进更好决策的环境和选项"
            })
            key_insights.append("好的默认选项是最有效的助推手段")

        # 时间不一致性
        if any(kw in query_lower for kw in ["延迟", "未来", "承诺", "delay", "future", "commitment"]):
            frameworks.append({
                "name": "双曲贴现（时间不一致）",
                "description": "人类对即时奖励的偏好远强于未来奖励（延迟折扣）",
                "application": "设计克服即时偏好的机制"
            })
            key_insights.append("承诺机制和预承诺策略可以对抗时间不一致性")

        return AnalysisResult(
            query=query,
            frameworks=frameworks,
            key_insights=key_insights,
            recommendations=self._generate_recommendations(frameworks),
            confidence=0.85
        )

    def decide(self, options: List[DecisionOption], criteria: Optional[Dict[str, float]] = None) -> DecisionResult:
        """
        行为经济学决策框架
        
        考虑认知偏差和启发式的影响
        """
        if not options:
            return DecisionResult(
                recommended=None,
                reasoning="无决策选项提供",
                confidence=0.0,
                alternative_options=[]
            )

        criteria = criteria or {"rationality": 1.0, "practicality": 1.0}
        adjusted_scores = []

        for opt in options:
            # 应用行为经济学调整
            base_score = opt.expected_value * opt.probability if hasattr(opt, 'expected_value') else 0.5
            bias_adjustment = 1.0

            # 检查损失厌恶
            if opt.framing == "loss":
                bias_adjustment *= 1.2  # 损失框架提升评分
            elif opt.framing == "gain":
                bias_adjustment *= 0.9  # 收益框架降低评分

            adjusted_score = base_score * bias_adjustment
            adjusted_scores.append((opt, adjusted_score))

        # 选择调整后最优
        best_opt, best_score = max(adjusted_scores, key=lambda x: x[1])

        return DecisionResult(
            recommended=best_opt,
            reasoning=f"基于行为经济学调整框架: {best_opt.description}",
            confidence=0.8,
            alternative_options=[opt for opt, _ in adjusted_scores if opt != best_opt]
        )

    def advise(self, context: AdviceResult, situation: Dict[str, Any]) -> AdviceResult:
        """
        行为经济学建议
        
        提供考虑认知偏差的建议
        """
        key_warnings = []

        # 常见偏差警告
        if situation.get("time_pressure"):
            key_warnings.append("时间压力下更易出现启发式偏差，建议引入决策检查清单")

        if situation.get("high_stakes"):
            key_warnings.append("高风险决策更易受确认偏误影响，建议引入反对声音")

        if situation.get("emotional"):
            key_warnings.append("情绪状态下决策需警惕情绪启发式偏差")

        context.warnings.extend(key_warnings)
        return context

    def assess(self, subject: Any, criteria: List[str]) -> AssessmentResult:
        """
        行为经济学评估
        
        从认知偏差角度评估方案
        """
        bias_check = []

        # 检查常见偏差
        if hasattr(subject, 'description'):
            desc_lower = subject.description.lower()
            if "免费" in desc_lower or "free" in desc_lower:
                bias_check.append("免费效应：可能高估免费选项的实际价值")
            if any(w in desc_lower for w in ["保证", "保证", "guarantee"]):
                bias_check.append("乐观偏差：可能低估风险")

        return AssessmentResult(
            subject=str(subject),
            criteria=criteria,
            scores={c: 0.7 for c in criteria},  # 默认评分
            bias_analysis=bias_check,
            overall_score=0.7,
            recommendations=[
                "建议引入独立审查机制",
考虑使用预先承诺策略减少即时偏好影响
            ]
        )


def get_cluster() -> BehavioralEconomicsCluster:
    """获取行为经济学集群实例"""
    return BehavioralEconomicsCluster()
