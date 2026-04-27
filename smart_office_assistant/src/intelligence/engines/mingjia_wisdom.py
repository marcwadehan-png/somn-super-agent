"""
__all__ = [
    'get_mingjia_wisdom',
    'query_mingjia_by_problem',
    'get_concept_analysis',
    'get_logical_reasoning',
    'get_relative_thinking',
]

名家智慧核心模块 v1.0
Mingjia School Wisdom Core Module

中国古代名家（3人）：惠施、公孙龙、桓团
核心思想：合同异、离坚白、白马非马、正名理论

版本: v1.0
创建: 2026-04-10
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class MingjiaDomain(Enum):
    """名家应用领域"""
    CONCEPT_ANALYSIS = "概念分析"         # 澄清概念是解决问题的第一步
    LOGICAL_REASONING = "逻辑推理"         # 严密逻辑是论辩的武器
    RELATIVE_THINKING = "相对思维"         # 从事物不同角度看问题
    NAME_REALITY_DISTINCTION = "名实区分"   # 语言与实在是不同层面
    DEBATE_METHOD = "论辩方法"            # 辩论可以澄清思想


@dataclass
class MingjiaSageProfile:
    """名家贤者画像"""
    name: str
    era: str
    years: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[MingjiaDomain, int]
    logical_ability: int  # 逻辑能力 1-10
    historical_impact: int


@dataclass
class MingjiaWisdomResult:
    """名家智慧查询结果"""
    sage_name: str
    problem: str
    concept_analysis: Dict[str, str]
    logical_structure: str
    relative_insight: str
    recommendations: List[str]
    name_reality_guidance: str
    confidence: float


class MingjiaWisdomCore:
    """
    名家智慧核心

    提供概念分析、逻辑推理、名实区分的智慧查询
    """

    def __init__(self):
        self._sages: Dict[str, MingjiaSageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化名家贤者数据"""
        # 惠施
        self._sages["惠施"] = MingjiaSageProfile(
            name="惠施",
            era="战国",
            years="约前370-前310",
            core_theories=[
                "合同异",
                "历物之意",
                "实用主义",
            ],
            methodology=[
                "相对性思维——从事物不同角度看有不同性质",
                "实用验证——知识必须有用",
                "论辩澄清——通过辩论深化认识",
            ],
            wisdom_laws=[
                "相对性是认识事物的方式——事物从不同角度看有不同性质",
                "辩论是发现真理的方法——通过辩论可以深化认识",
                "实用是检验知识的标准——知识必须有用",
            ],
            domain_strength={
                MingjiaDomain.CONCEPT_ANALYSIS: 8,
                MingjiaDomain.LOGICAL_REASONING: 9,
                MingjiaDomain.RELATIVE_THINKING: 10,
                MingjiaDomain.NAME_REALITY_DISTINCTION: 7,
                MingjiaDomain.DEBATE_METHOD: 9,
            },
            logical_ability=9,
            historical_impact=8,
        )

        # 公孙龙
        self._sages["公孙龙"] = MingjiaSageProfile(
            name="公孙龙",
            era="战国",
            years="约前320-前250",
            core_theories=[
                "离坚白",
                "白马非马",
                "正名理论",
            ],
            methodology=[
                "概念分析——对概念进行细致的分析",
                "逻辑论证——运用严密的逻辑推理",
                "名实区分——强调名实相符",
            ],
            wisdom_laws=[
                "语言与实在是不同层面——名与实不可混为一谈",
                "概念分析是哲学的基础——澄清概念是解决问题的第一步",
                "逻辑严密是论辩的武器——公孙龙是逻辑学的先驱",
            ],
            domain_strength={
                MingjiaDomain.CONCEPT_ANALYSIS: 10,
                MingjiaDomain.LOGICAL_REASONING: 10,
                MingjiaDomain.RELATIVE_THINKING: 7,
                MingjiaDomain.NAME_REALITY_DISTINCTION: 10,
                MingjiaDomain.DEBATE_METHOD: 10,
            },
            logical_ability=10,
            historical_impact=8,
        )

        # 桓团
        self._sages["桓团"] = MingjiaSageProfile(
            name="桓团",
            era="战国",
            years="战国时期",
            core_theories=[
                "名辩之术",
                "概念辨析",
                "逻辑论证",
            ],
            methodology=[
                "辩论术——通过辩论来阐明观点",
                "概念辨析——对概念进行细致辨析",
            ],
            wisdom_laws=[
                "辩论可以澄清思想——通过辩论可以深化认识",
                "名家思想是逻辑学的先声——中国古代的逻辑学传统",
                "论辩是学术进步的方式——百家争鸣推动思想创新",
            ],
            domain_strength={
                MingjiaDomain.CONCEPT_ANALYSIS: 8,
                MingjiaDomain.LOGICAL_REASONING: 8,
                MingjiaDomain.RELATIVE_THINKING: 7,
                MingjiaDomain.NAME_REALITY_DISTINCTION: 7,
                MingjiaDomain.DEBATE_METHOD: 8,
            },
            logical_ability=8,
            historical_impact=6,
        )

    def get_mingjia_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> MingjiaWisdomResult:
        """
        获取名家智慧

        Args:
            problem: 待解决的问题
            context: 上下文

        Returns:
            名家智慧分析结果
        """
        context = context or {}

        # 分析问题领域
        domain = self._classify_problem_domain(problem)

        # 概念分析
        concept = self._get_concept_analysis(problem)

        # 逻辑结构
        logic = self._get_logical_structure(problem, domain)

        # 相对性洞察
        relative = self._get_relative_insight(problem)

        # 选择贤者
        sage_name = self._select_best_sage(domain)
        sage = self._sages[sage_name]

        return MingjiaWisdomResult(
            sage_name=sage_name,
            problem=problem,
            concept_analysis=concept,
            logical_structure=logic,
            relative_insight=relative,
            recommendations=self._generate_recommendations(sage, domain),
            name_reality_guidance=self._get_name_reality_guidance(problem),
            confidence=0.82,
        )

    def query_mingjia_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询名家智慧"""
        result = self.get_mingjia_wisdom(problem)
        return [
            {
                "sage": result.sage_name,
                "concept_analysis": result.concept_analysis,
                "logical_structure": result.logical_structure,
                "relative_insight": result.relative_insight,
                "recommendations": result.recommendations,
            }
        ]

    def get_concept_analysis(self, concept: str) -> Dict[str, str]:
        """获取概念分析"""
        return {
            "概念定义": f"对'{concept}'的精确定义是什么？",
            "名实关系": f"'{concept}'这个名称与实际所指是否完全对应？",
            "相对性": f"从不同角度看待'{concept}'会有什么不同理解？",
            "边界条件": f"'{concept}'的适用边界在哪里？什么情况下不再适用？",
        }

    def get_logical_reasoning(self, problem: str) -> str:
        """获取逻辑推理指导"""
        return "公孙龙的逻辑：先明确概念，再进行严密的推理论证。白马非马的精髓在于：'白马'与'马'在概念上是不同的——前者是特定颜色加一般马形，后者是一般马形。"

    def get_relative_thinking(self, perspective: str) -> str:
        """获取相对思维指导"""
        return f"从{perspective}角度看问题，同一事物会有不同性质。惠施的'合同异'告诉我们：相同中蕴含差异，差异中蕴含相同。"

    def _classify_problem_domain(self, problem: str) -> MingjiaDomain:
        """分类问题领域"""
        if any(k in problem for k in ["概念", "定义", "澄清", "区分"]):
            return MingjiaDomain.CONCEPT_ANALYSIS
        elif any(k in problem for k in ["逻辑", "推理", "论证", "推断"]):
            return MingjiaDomain.LOGICAL_REASONING
        elif any(k in problem for k in ["相对", "不同角度", "看法", "视角"]):
            return MingjiaDomain.RELATIVE_THINKING
        elif any(k in problem for k in ["名实", "名称", "实质", "表象"]):
            return MingjiaDomain.NAME_REALITY_DISTINCTION
        elif any(k in problem for k in ["辩论", "论辩", "说服", "论证"]):
            return MingjiaDomain.DEBATE_METHOD
        return MingjiaDomain.CONCEPT_ANALYSIS

    def _get_concept_analysis(self, problem: str) -> Dict[str, str]:
        """获取概念分析"""
        return {
            "问题核心概念": "这个问题涉及的核心概念是什么？",
            "概念边界": "这个概念的边界在哪里？",
            "名与实": "概念名称与实际所指是否一致？",
            "相同与差异": "这个概念与相近概念有何相同和不同？",
        }

    def _get_logical_structure(self, problem: str, domain: MingjiaDomain) -> str:
        """获取逻辑结构"""
        structures = {
            MingjiaDomain.CONCEPT_ANALYSIS: "先澄清概念，再分析关系，最后得出结论。公孙龙的方法：先明确'名'，再考察'实'，最后判断名实是否相符。",
            MingjiaDomain.LOGICAL_REASONING: "严密的三段论推理：大前提、小前提、结论。惠施的方法：从已知推未知，从个别到一般。",
            MingjiaDomain.RELATIVE_THINKING: "惠施合同异：从相同中找差异，从差异中找相同。没有绝对的同，也没有绝对的异。",
            MingjiaDomain.NAME_REALITY_DISTINCTION: "名实相符是判断标准。公孙龙：白马非马——'白马'是颜色+形状的具体概念，'马'是一般概念，两者不等同。",
            MingjiaDomain.DEBATE_METHOD: "桓团论辩术：先立论，再反驳，最后综合。辩论的目标是澄清而非取胜。",
        }
        return structures.get(domain, "先明概念，后行推理，最终综合")

    def _get_relative_insight(self, problem: str) -> str:
        """获取相对性洞察"""
        return "惠施的'合同异'：事物从不同角度看有不同性质。合同异强调同一性，离坚白强调差异性。理解两者的辩证关系，是处理复杂问题的关键。"

    def _select_best_sage(self, domain: MingjiaDomain) -> str:
        """选择最合适的贤者"""
        scores = {name: sage.domain_strength.get(domain, 5) for name, sage in self._sages.items()}
        return max(scores, key=scores.get)

    def _generate_recommendations(self, sage: MingjiaSageProfile, domain: MingjiaDomain) -> List[str]:
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

    def _get_name_reality_guidance(self, problem: str) -> str:
        """获取名实指导"""
        return "公孙龙'白马非马'论的意义：语言（名）与实际（实）之间存在张力。在解决问题时，先要明确概念的内涵和外延，避免名实混淆导致的逻辑错误。"


# 全局单例
_ENGINE: Optional[MingjiaWisdomCore] = None


def get_mingjia_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> MingjiaWisdomResult:
    """获取名家智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = MingjiaWisdomCore()
    return _ENGINE.get_mingjia_wisdom(problem, context)


def query_mingjia_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询名家智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = MingjiaWisdomCore()
    return _ENGINE.query_mingjia_by_problem(problem)


def get_concept_analysis(concept: str) -> Dict[str, str]:
    """获取概念分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = MingjiaWisdomCore()
    return _ENGINE.get_concept_analysis(concept)


def get_logical_reasoning(problem: str) -> str:
    """获取逻辑推理指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = MingjiaWisdomCore()
    return _ENGINE.get_logical_reasoning(problem)


def get_relative_thinking(perspective: str) -> str:
    """获取相对思维指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = MingjiaWisdomCore()
    return _ENGINE.get_relative_thinking(perspective)
