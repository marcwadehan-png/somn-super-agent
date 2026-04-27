"""
__all__ = [
    'MingjiaWisdomEngine',
]

名家智慧引擎 v1.0
Mingjia School Wisdom Engine V1.0

中国古代名家（惠施、公孙龙、桓团）的逻辑与辩证智慧。

版本: v1.0
创建: 2026-04-23
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class MingjiaDomain(Enum):
    """名家应用领域"""
    CONCEPT_ANALYSIS = "概念分析"
    LOGICAL_REASONING = "逻辑推理"
    RELATIVE_THINKING = "相对思维"
    NAME_REALITY_DISTINCTION = "名实区分"
    DIALECTICAL_REASONING = "辩证推理"


@dataclass
class MingjiaWisdomResult:
    """名家智慧分析结果"""
    problem_type: str
    analysis: str
    paradox_insight: str
    logical_structure: str
    recommendations: List[str]
    confidence: float


class MingjiaWisdomCore:
    """
    名家智慧核心

    提供概念分析、逻辑悖论、名实区分的智慧。
    """

    def __init__(self):
        self._sages = self._initialize_sages()

    def _initialize_sages(self) -> Dict[str, Dict[str, Any]]:
        """初始化名家贤者"""
        return {
            "惠施": {
                "name": "惠施",
                "era": "战国",
                "years": "约前370-前310",
                "core_theories": ["合同异", "历物之意", "相对性思维"],
                "wisdom_laws": [
                    "事物从不同角度看有不同性质",
                    "知识必须有用才是真知",
                    "通过辩论可以深化认识"
                ]
            },
            "公孙龙": {
                "name": "公孙龙",
                "era": "战国",
                "years": "约前320-前250",
                "core_theories": ["离坚白", "白马非马", "正名理论"],
                "wisdom_laws": [
                    "名与实不可混为一谈",
                    "澄清概念是解决问题的第一步",
                    "逻辑严密是论辩的武器"
                ]
            },
            "桓团": {
                "name": "桓团",
                "era": "战国",
                "years": "战国时期",
                "core_theories": ["名辩之术", "概念辨析", "逻辑论证"],
                "wisdom_laws": [
                    "辩论是阐明观点的方法",
                    "概念辨析需要细致深入"
                ]
            }
        }

    def analyze_paradox(self, problem: str, context: Optional[Dict[str, Any]] = None) -> MingjiaWisdomResult:
        """分析逻辑悖论"""
        return MingjiaWisdomResult(
            problem_type="LOGICAL_PARADOX",
            analysis="通过公孙龙'白马非马'的逻辑分析，可以发现概念与实体的差异",
            paradox_insight="悖论揭示了概念的边界和语言的局限",
            logical_structure="设定前提→推演矛盾→澄清概念→得出结论",
            recommendations=[
                "识别问题中的隐含前提",
                "检验概念的边界条件",
                "区分语言描述与实体本质"
            ],
            confidence=0.85
        )

    def analyze_classification(self, problem: str, context: Optional[Dict[str, Any]] = None) -> MingjiaWisdomResult:
        """分析名实关系（分类）"""
        return MingjiaWisdomResult(
            problem_type="CLASSIFICATION_REFINEMENT",
            analysis="惠施的'合同异'提供了分类的相对性视角",
            paradox_insight="分类标准不同，结果也不同",
            logical_structure="确定分类标准→分析同类与异类→考察名实对应",
            recommendations=[
                "明确分类的维度和标准",
                "考察分类的名实相符性",
                "理解'合同异'的相对性"
            ],
            confidence=0.83
        )

    def analyze_dialectical_reasoning(self, problem: str, context: Optional[Dict[str, Any]] = None) -> MingjiaWisdomResult:
        """分析辩证推理"""
        return MingjiaWisdomResult(
            problem_type="DIALECTICAL_REASONING",
            analysis="名家的论辩方法提供了多角度辩证的思维框架",
            paradox_insight="对立统一是推理深化的动力",
            logical_structure="提出论点→对立论证→综合深化→达成更高层次认识",
            recommendations=[
                "主动寻找对立观点",
                "通过论辩检验和完善论点",
                "追求更高层次的综合认识"
            ],
            confidence=0.82
        )


class MingjiaWisdomEngine:
    """
    名家智慧引擎主类
    """

    def __init__(self):
        self.core = MingjiaWisdomCore()

    def get_wisdom(self, sage_name: Optional[str] = None) -> Dict[str, Any]:
        """获取名家智慧"""
        if sage_name:
            return self.core._sages.get(sage_name, {})
        return self.core._sages

    def solve(self, problem_type: str, context: Optional[Dict[str, Any]] = None) -> MingjiaWisdomResult:
        """
        根据问题类型解决名家问题

        Args:
            problem_type: 问题类型（LOGICAL_PARADOX/CLASSIFICATION_REFINEMENT等）
            context: 上下文信息

        Returns:
            名家智慧分析结果
        """
        context = context or {}
        problem = context.get("problem", "")

        if problem_type == "LOGICAL_PARADOX":
            return self.core.analyze_paradox(problem, context)
        elif problem_type == "CLASSIFICATION_REFINEMENT":
            return self.core.analyze_classification(problem, context)
        elif problem_type == "DIALECTICAL_REASONING":
            return self.core.analyze_dialectical_reasoning(problem, context)
        else:
            return MingjiaWisdomResult(
                problem_type=problem_type,
                analysis="名家视角分析",
                paradox_insight="概念分析是深入理解的第一步",
                logical_structure="分析→论证→综合",
                recommendations=["澄清概念", "检验逻辑", "多角度思考"],
                confidence=0.70
            )

    def get_all_wisdoms(self) -> List[Dict[str, Any]]:
        """获取所有名家智慧"""
        return list(self.core._sages.values())
