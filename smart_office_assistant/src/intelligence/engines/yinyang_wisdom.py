"""
__all__ = [
    'get_yinyang_wisdom',
    'query_yinyang_by_problem',
    'get_macro_strategy',
    'analyze_cyclical_pattern',
    'get_tianren感应_guidance',
]

阴阳家智慧核心模块 v1.0
Yinyang School Wisdom Core Module

中国古代阴阳家（2人）：邹衍、邹奭
核心思想：阴阳五行、大九州说、五德终始、天人感应

版本: v1.0
创建: 2026-04-10
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class YinyangDomain(Enum):
    """阴阳家应用领域"""
    MACRO_STRATEGY = "宏观战略"        # 从宇宙宏观角度思考
    CYCLICAL_DEVELOPMENT = "循环发展"   # 五行相生相克
    TIANREN_INDUCTION = "天人感应"      # 人与自然相互感应
    HISTORICAL_CYCLES = "历史循环"      # 五德终始解释朝代更替
    GEOGRAPHIC_VISION = "地理视野"        # 大九州说


@dataclass
class YinyangSageProfile:
    """阴阳家贤者画像"""
    name: str
    era: str
    years: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[YinyangDomain, int]  # 1-10 各领域专长
    historical_impact: int


@dataclass
class YinyangWisdomResult:
    """阴阳家智慧查询结果"""
    sage_name: str
    problem: str
    core_insight: str
    five_elements_analysis: Dict[str, str]  # 五行分析
    cyclical_insight: str
    recommendations: List[str]
    macro_recommendation: str
    confidence: float


class YinyangWisdomCore:
    """
    阴阳家智慧核心

    提供阴阳五行、天人感应、历史循环的智慧查询
    """

    def __init__(self):
        self._sages: Dict[str, YinyangSageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化阴阳家贤者数据"""
        # 邹衍
        self._sages["邹衍"] = YinyangSageProfile(
            name="邹衍",
            era="战国",
            years="约前305-前240",
            core_theories=[
                "阴阳五行",
                "大九州说",
                "五德终始",
                "天人感应",
            ],
            methodology=[
                "宏观视野——从宇宙宏观角度思考问题",
                "类比推理——以自然规律类比社会规律",
                "历史循环——以五行相胜解释历史发展规律",
            ],
            wisdom_laws=[
                "宏观视野是智慧的高度——站得高才能看得远",
                "循环发展是自然规律——历史有规律但也在循环",
                "天人合一是东方智慧核心——人与自然是一个整体",
                "类比是认识复杂事物的方法——从已知推未知",
                "地理视野决定思想格局——大九州说拓展了世界观念",
            ],
            domain_strength={
                YinyangDomain.MACRO_STRATEGY: 10,
                YinyangDomain.CYCLICAL_DEVELOPMENT: 10,
                YinyangDomain.TIANREN_INDUCTION: 9,
                YinyangDomain.HISTORICAL_CYCLES: 10,
                YinyangDomain.GEOGRAPHIC_VISION: 10,
            },
            historical_impact=10,
        )

        # 邹奭
        self._sages["邹奭"] = YinyangSageProfile(
            name="邹奭",
            era="战国",
            years="战国齐人",
            core_theories=[
                "阴阳五行",
                "名辩之术",
                "稷下学术",
            ],
            methodology=[
                "传承发展——在邹衍基础上继续发展",
                "学术论辩——在稷下学宫进行学术辩论",
            ],
            wisdom_laws=[
                "传承是发展的基础——在前人基础上继续发展",
                "稷下学宫是百家争鸣的平台——学术自由是思想繁荣的保障",
                "论辩是学术进步的方式——百家争鸣推动思想创新",
            ],
            domain_strength={
                YinyangDomain.MACRO_STRATEGY: 7,
                YinyangDomain.CYCLICAL_DEVELOPMENT: 8,
                YinyangDomain.TIANREN_INDUCTION: 7,
                YinyangDomain.HISTORICAL_CYCLES: 7,
                YinyangDomain.GEOGRAPHIC_VISION: 7,
            },
            historical_impact=7,
        )

    def get_yinyang_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> YinyangWisdomResult:
        """
        获取阴阳家智慧

        Args:
            problem: 待解决的问题
            context: 上下文

        Returns:
            阴阳家智慧分析结果
        """
        context = context or {}

        # 分析问题领域
        domain = self._classify_problem_domain(problem)

        # 五行分析
        five_elements = self._five_elements_analysis(problem, domain)

        # 循环洞察
        cyclical = self._get_cyclical_insight(problem, domain)

        # 推荐贤者
        sage_name = self._select_best_sage(domain)

        sage = self._sages[sage_name]
        recommendations = self._generate_recommendations(problem, sage, domain)

        return YinyangWisdomResult(
            sage_name=sage_name,
            problem=problem,
            core_insight=self._get_core_insight(sage, domain),
            five_elements_analysis=five_elements,
            cyclical_insight=cyclical,
            recommendations=recommendations,
            macro_recommendation=self._get_macro_recommendation(domain, five_elements),
            confidence=0.82,
        )

    def query_yinyang_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询阴阳家智慧"""
        result = self.get_yinyang_wisdom(problem)
        return [
            {
                "sage": result.sage_name,
                "insight": result.core_insight,
                "five_elements": result.five_elements_analysis,
                "cyclical": result.cyclical_insight,
                "recommendations": result.recommendations,
            }
        ]

    def get_macro_strategy(self, context: Dict[str, Any]) -> str:
        """获取宏观战略建议"""
        problem = context.get("problem", "")
        domain = self._classify_problem_domain(problem)
        five_elements = self._five_elements_analysis(problem, domain)
        return self._get_macro_recommendation(domain, five_elements)

    def analyze_cyclical_pattern(self, situation: str) -> Dict[str, str]:
        """分析循环规律"""
        five_elements = {
            "木": "生发、创新、新兴事物",
            "火": "鼎盛、繁荣、扩张",
            "土": "转化、沉淀、积累",
            "金": "收敛、肃杀、改革",
            "水": "潜伏、孕育、回归",
        }
        return five_elements

    def get_tianren感应_guidance(self, context: Dict[str, Any]) -> Dict[str, str]:
        """获取天人感应指导"""
        return {
            "principle": "人与自然相互感应，顺应自然者昌，逆自然者亡",
            "application": "在决策时考虑天时地利人和三者关系",
            "method": "春夏养阳，秋冬养阴；顺之则昌，逆之则亡",
        }

    def _classify_problem_domain(self, problem: str) -> YinyangDomain:
        """分类问题领域"""
        if any(k in problem for k in ["战略", "宏观", "全局", "长远", "规划"]):
            return YinyangDomain.MACRO_STRATEGY
        elif any(k in problem for k in ["循环", "周期", "规律", "历史", "趋势"]):
            return YinyangDomain.CYCLICAL_DEVELOPMENT
        elif any(k in problem for k in ["天人", "自然", "环境", "和谐"]):
            return YinyangDomain.TIANREN_INDUCTION
        elif any(k in problem for k in ["朝代", "兴衰", "更替", "变革"]):
            return YinyangDomain.HISTORICAL_CYCLES
        elif any(k in problem for k in ["地理", "空间", "格局", "视野"]):
            return YinyangDomain.GEOGRAPHIC_VISION
        return YinyangDomain.MACRO_STRATEGY

    def _five_elements_analysis(self, problem: str, domain: YinyangDomain) -> Dict[str, str]:
        """五行分析"""
        return {
            "相生": "木生火（火热文明）、火生土（土化沉淀）、土生金（金收敛）、金生水（水潜伏）、水生木（木生发）",
            "相克": "木克土（生长破土）、土克水（水来土掩）、水克火（火遇水灭）、火克金（烈火熔金）、金克木（刀斧伐木）",
            "当前态势": "根据问题性质判断所处五行阶段，选择相生或相克策略",
        }

    def _get_cyclical_insight(self, problem: str, domain: YinyangDomain) -> str:
        """获取循环洞察"""
        cyclical_map = {
            YinyangDomain.MACRO_STRATEGY: "宏观战略需要顺应历史循环规律，在正确的时间做正确的事",
            YinyangDomain.CYCLICAL_DEVELOPMENT: "五行相生相克揭示了事物发展的循环规律，把握规律就能预知趋势",
            YinyangDomain.TIANREN_INDUCTION: "天人感应体现了人与自然的深层联系，顺应自然是最高智慧",
            YinyangDomain.HISTORICAL_CYCLES: "五德终始揭示了朝代更替的规律，任何兴盛都有衰落之时",
            YinyangDomain.GEOGRAPHIC_VISION: "大九州说拓展视野，提醒我们从更广阔的角度认识世界",
        }
        return cyclical_map.get(domain, "阴阳平衡是宇宙的根本规律")

    def _select_best_sage(self, domain: YinyangDomain) -> str:
        """选择最合适的贤者"""
        if self._sages["邹衍"].domain_strength.get(domain, 0) >= self._sages["邹奭"].domain_strength.get(domain, 0):
            return "邹衍"
        return "邹奭"

    def _get_core_insight(self, sage: YinyangSageProfile, domain: YinyangDomain) -> str:
        """获取核心洞察"""
        law_map = {
            YinyangDomain.MACRO_STRATEGY: "宏观视野是智慧的高度——站得高才能看得远",
            YinyangDomain.CYCLICAL_DEVELOPMENT: "循环发展是自然规律——历史有规律但也在循环",
            YinyangDomain.TIANREN_INDUCTION: "天人合一是东方智慧核心——人与自然是一个整体",
            YinyangDomain.HISTORICAL_CYCLES: "五德终始揭示了朝代更替的规律",
            YinyangDomain.GEOGRAPHIC_VISION: "地理视野决定思想格局——大九州说拓展了世界观念",
        }
        return law_map.get(domain, sage.wisdom_laws[0])

    def _generate_recommendations(self, problem: str, sage: YinyangSageProfile, domain: YinyangDomain) -> List[str]:
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

    def _get_macro_recommendation(self, domain: YinyangDomain, five_elements: Dict[str, str]) -> str:
        """获取宏观建议"""
        recommendations = {
            YinyangDomain.MACRO_STRATEGY: "从宏观视野审视当前问题，顺应历史发展趋势，在正确的时间做正确的事",
            YinyangDomain.CYCLICAL_DEVELOPMENT: "五行循环揭示了事物发展的规律：当前处于什么阶段？应当促进还是抑制？",
            YinyangDomain.TIANREN_INDUCTION: "天人感应提醒我们顺应自然规律，在决策时考虑天时地利人和的配合",
            YinyangDomain.HISTORICAL_CYCLES: "五德终始揭示了兴衰更替的规律：当前的繁荣处于五德中的哪一阶段？",
            YinyangDomain.GEOGRAPHIC_VISION: "拓展视野，从更宏观的角度认识当前问题，避免只见树木不见森林",
        }
        return recommendations.get(domain, "阴阳平衡是根本，顺应规律是智慧")


# 全局单例
_ENGINE: Optional[YinyangWisdomCore] = None


def get_yinyang_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> YinyangWisdomResult:
    """获取阴阳家智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = YinyangWisdomCore()
    return _ENGINE.get_yinyang_wisdom(problem, context)


def query_yinyang_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询阴阳家智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = YinyangWisdomCore()
    return _ENGINE.query_yinyang_by_problem(problem)


def get_macro_strategy(context: Dict[str, Any]) -> str:
    """获取宏观战略建议"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = YinyangWisdomCore()
    return _ENGINE.get_macro_strategy(context)


def analyze_cyclical_pattern(situation: str) -> Dict[str, str]:
    """分析循环规律"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = YinyangWisdomCore()
    return _ENGINE.analyze_cyclical_pattern(situation)


def get_tianren感应_guidance(context: Dict[str, Any]) -> Dict[str, str]:
    """获取天人感应指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = YinyangWisdomCore()
    return _ENGINE.get_tianren感应_guidance(context)
