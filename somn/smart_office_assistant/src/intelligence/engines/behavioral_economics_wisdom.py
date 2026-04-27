"""
__all__ = [
    'get_behavioral_economics_wisdom',
    'query_be_by_problem',
    'get_nudge_design',
    'get_cognitive_bias_analysis',
    'get_decision_architecture',
]

行为经济学智慧核心模块 v1.0
Behavioral Economics Wisdom Core Module

核心人物：卡尼曼、特瑟、福勒
核心思想：有限理性、助推设计、损失厌恶

版本: V1.0
创建: 2026-04-24
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class BehavioralEconomicsDomain(Enum):
    """行为经济学应用领域"""
    NUDGE_DESIGN = "助推设计"            # 选择架构与助推
    COGNITIVE_BIAS = "认知偏差"          # 偏见与启发式思维
    LOSS_AVERSION = "损失厌恶"           # 损失与收益的不对称性
    PRESENT_BIAS = "当下偏差"            # 双曲贴现与即时满足
    SOCIAL_PREFERENCE = "社会偏好"        # 公平、互惠、利他
    MENTAL_ACCOUNTING = "心理账户"        # 心理账户理论


@dataclass
class BehavioralEconomicsSageProfile:
    """行为经济学贤者画像"""
    name: str
    era: str
    nationality: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[BehavioralEconomicsDomain, int]


@dataclass
class BehavioralEconomicsResult:
    """行为经济学智慧查询结果"""
    sage_name: str
    problem: str
    cognitive_biases: List[str]
    nudge_suggestions: List[str]
    decision_architecture: str
    recommendations: List[str]
    confidence: float


class BehavioralEconomicsWisdomCore:
    """
    行为经济学智慧核心

    提供认知偏差分析、助推设计、决策架构的智慧
    """

    def __init__(self):
        self._sages: Dict[str, BehavioralEconomicsSageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化行为经济学贤者数据"""

        # 丹尼尔·卡尼曼 (Daniel Kahneman)
        self._sages["卡尼曼"] = BehavioralEconomicsSageProfile(
            name="卡尼曼",
            era="21世纪",
            nationality="以色列/美国",
            core_theories=[
                "前景理论",
                "系统一/系统二",
                "锚定效应",
                "可得性启发",
                "过度自信",
            ],
            methodology=[
                "实验经济学方法——通过实验验证理论",
                "认知偏差系统分类——识别系统性思维错误",
                "损失厌恶分析——理解收益与损失的不对称性",
            ],
            wisdom_laws=[
                "有限理性是人的本质——人们并非完全理性的经济人",
                "损失比收益更有影响力——损失带来的痛苦是等量收益快乐的2倍",
                "锚定效应塑造判断——初始信息强烈影响后续判断",
                "系统一主导日常决策——快速、直觉性思维是默认模式",
            ],
            domain_strength={
                BehavioralEconomicsDomain.NUDGE_DESIGN: 9,
                BehavioralEconomicsDomain.COGNITIVE_BIAS: 10,
                BehavioralEconomicsDomain.LOSS_AVERSION: 10,
                BehavioralEconomicsDomain.PRESENT_BIAS: 8,
                BehavioralEconomicsDomain.SOCIAL_PREFERENCE: 7,
                BehavioralEconomicsDomain.MENTAL_ACCOUNTING: 8,
            },
        )

        # 理查德·塞勒 (Richard Thaler)
        self._sages["塞勒"] = BehavioralEconomicsSageProfile(
            name="塞勒",
            era="21世纪",
            nationality="美国",
            core_theories=[
                "助推理论",
                "心理账户",
                "票赋效应",
                "跨期选择",
                "利他偏好",
            ],
            methodology=[
                "助推设计——通过选择架构引导行为而不限制选择",
                "自由家长式主义——在保护与自由间取得平衡",
                "助推组合——多种微小干预的协同效应",
            ],
            wisdom_laws=[
                "助推是默认选项的艺术——改变选择架构而非限制选择",
                "心理账户影响决策——人们按心理分类处理财务决策",
                "票赋效应——人们对拥有的物品估值高于未拥有时",
                "默认选项的力量——多数人接受默认选项",
            ],
            domain_strength={
                BehavioralEconomicsDomain.NUDGE_DESIGN: 10,
                BehavioralEconomicsDomain.COGNITIVE_BIAS: 9,
                BehavioralEconomicsDomain.LOSS_AVERSION: 8,
                BehavioralEconomicsDomain.PRESENT_BIAS: 9,
                BehavioralEconomicsDomain.SOCIAL_PREFERENCE: 8,
                BehavioralEconomicsDomain.MENTAL_ACCOUNTING: 10,
            },
        )

        # 罗伯特·西奥迪尼 (Robert Cialdini)
        self._sages["西奥迪尼"] = BehavioralEconomicsSageProfile(
            name="西奥迪尼",
            era="21世纪",
            nationality="美国",
            core_theories=[
                "影响力六原则",
                "互惠",
                "社会认同",
                "承诺与一致",
                "权威",
                "稀缺",
            ],
            methodology=[
                "说服心理学——理解他人顺从的心理机制",
                "原则归纳——将说服策略系统化为可操作原则",
                "情境分析——不同情境下影响力策略的差异",
            ],
            wisdom_laws=[
                "互惠是社会粘合剂——人们倾向于回报他人的好意",
                "社会认同指引行为——人们参考他人行为做决策",
                "承诺驱动一致——公开承诺会提高后续行动可能性",
                "稀缺创造渴望——稀缺资源激发更强烈的获取欲望",
            ],
            domain_strength={
                BehavioralEconomicsDomain.NUDGE_DESIGN: 9,
                BehavioralEconomicsDomain.COGNITIVE_BIAS: 8,
                BehavioralEconomicsDomain.LOSS_AVERSION: 7,
                BehavioralEconomicsDomain.PRESENT_BIAS: 7,
                BehavioralEconomicsDomain.SOCIAL_PREFERENCE: 10,
                BehavioralEconomicsDomain.MENTAL_ACCOUNTING: 6,
            },
        )

    def get_behavioral_economics_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> BehavioralEconomicsResult:
        """
        获取行为经济学智慧

        Args:
            problem: 待解决的行为问题
            context: 上下文

        Returns:
            行为经济学智慧分析结果
        """
        context = context or {}

        # 分析问题领域
        domain = self._classify_problem_domain(problem)

        # 选择最合适的贤者
        sage_name = self._select_best_sage(domain)
        sage = self._sages[sage_name]

        return BehavioralEconomicsResult(
            sage_name=sage_name,
            problem=problem,
            cognitive_biases=self._identify_cognitive_biases(problem, sage),
            nudge_suggestions=self._design_nudges(problem, sage),
            decision_architecture=self._design_decision_architecture(problem, sage),
            recommendations=self._generate_recommendations(sage, domain),
            confidence=0.88,
        )

    def query_be_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询行为经济学智慧"""
        result = self.get_behavioral_economics_wisdom(problem)
        return [{
            "sage": result.sage_name,
            "cognitive_biases": result.cognitive_biases,
            "nudge_suggestions": result.nudge_suggestions,
            "decision_architecture": result.decision_architecture,
            "recommendations": result.recommendations,
        }]

    def get_nudge_design(self, nudge_type: str) -> Dict[str, str]:
        """获取助推设计指南"""
        return {
            "默认选项": "将期望行为设为默认选项，利用默认偏误",
            "框架效应": "相同信息不同表述导致不同选择，正面框架更有效",
            "社会认同": "展示他人行为，利用从众心理",
            "承诺机制": "利用一致性原理，促使用户做出并坚持承诺",
        }

    def get_cognitive_bias_analysis(self, bias_type: str) -> str:
        """获取认知偏差分析"""
        return "卡尼曼的系统一/系统二理论：系统一是快速、直觉的思维模式，容易产生认知偏差；系统二是缓慢、理性的思维模式，但需要更多努力。设计干预时，应考虑如何引导系统一朝向正确方向。"

    def get_decision_architecture(self, architecture_type: str) -> str:
        """获取决策架构设计"""
        return "塞勒的助推理论：有效的选择架构应该在不限制自由的前提下，引导人们做出更好决策。关键是理解人们的心理偏差，并设计能够克服这些偏差的干预措施。"

    def _classify_problem_domain(self, problem: str) -> BehavioralEconomicsDomain:
        """分类问题领域"""
        if any(k in problem for k in ["助推", "选择架构", "引导", "设计", "默认"]):
            return BehavioralEconomicsDomain.NUDGE_DESIGN
        elif any(k in problem for k in ["偏差", "偏见", "启发", "直觉", "错误"]):
            return BehavioralEconomicsDomain.COGNITIVE_BIAS
        elif any(k in problem for k in ["损失", "风险", "收益", "不对称"]):
            return BehavioralEconomicsDomain.LOSS_AVERSION
        elif any(k in problem for k in ["即时", "延迟", "耐心", "自律", "当下"]):
            return BehavioralEconomicsDomain.PRESENT_BIAS
        elif any(k in problem for k in ["公平", "互惠", "利他", "合作", "信任"]):
            return BehavioralEconomicsDomain.SOCIAL_PREFERENCE
        elif any(k in problem for k in ["账户", "预算", "分类", "金钱"]):
            return BehavioralEconomicsDomain.MENTAL_ACCOUNTING
        return BehavioralEconomicsDomain.NUDGE_DESIGN

    def _identify_cognitive_biases(self, problem: str, sage: BehavioralEconomicsSageProfile) -> List[str]:
        """识别认知偏差"""
        return [
            "锚定效应：初始信息可能过度影响判断",
            "确认偏误：倾向于寻找支持已有信念的信息",
            "过度自信：系统性地高估自己的判断准确性",
        ]

    def _design_nudges(self, problem: str, sage: BehavioralEconomicsSageProfile) -> List[str]:
        """设计助推"""
        return [
            "默认选项：将期望行为设为默认，利用默认偏误",
            "社会认同：展示目标群体的期望行为",
            "简化信息：减少认知负担，让正确选择更容易",
            "承诺机制：促使用户做出公开承诺",
        ]

    def _design_decision_architecture(self, problem: str, sage: BehavioralEconomicsSageProfile) -> str:
        """设计决策架构"""
        return "有效的决策架构需要理解目标群体的心理偏差。塞勒的助推原则：助推应该易于理解和接受，不应显著增加决策成本，且应该可逆。"

    def _select_best_sage(self, domain: BehavioralEconomicsDomain) -> str:
        """选择最合适的行为经济学家"""
        scores = {name: sage.domain_strength.get(domain, 5) for name, sage in self._sages.items()}
        return max(scores, key=scores.get)

    def _generate_recommendations(self, sage: BehavioralEconomicsSageProfile, domain: BehavioralEconomicsDomain) -> List[str]:
        """生成建议"""
        laws = sage.wisdom_laws
        recommendations = []
        for law in laws[:3]:
            if "——" in law:
                key, value = law.split("——", 1)
                recommendations.append(f"{key}：{value}")
            else:
                recommendations.append(law)
        return recommendations


# 全局单例
_ENGINE: Optional[BehavioralEconomicsWisdomCore] = None


def get_behavioral_economics_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> BehavioralEconomicsResult:
    """获取行为经济学智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = BehavioralEconomicsWisdomCore()
    return _ENGINE.get_behavioral_economics_wisdom(problem, context)


def query_be_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询行为经济学智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = BehavioralEconomicsWisdomCore()
    return _ENGINE.query_be_by_problem(problem)


def get_nudge_design(nudge_type: str) -> Dict[str, str]:
    """获取助推设计指南"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = BehavioralEconomicsWisdomCore()
    return _ENGINE.get_nudge_design(nudge_type)


def get_cognitive_bias_analysis(bias_type: str) -> str:
    """获取认知偏差分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = BehavioralEconomicsWisdomCore()
    return _ENGINE.get_cognitive_bias_analysis(bias_type)


def get_decision_architecture(architecture_type: str) -> str:
    """获取决策架构设计"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = BehavioralEconomicsWisdomCore()
    return _ENGINE.get_decision_architecture(architecture_type)
