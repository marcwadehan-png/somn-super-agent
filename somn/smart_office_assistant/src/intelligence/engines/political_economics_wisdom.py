"""
__all__ = [
    'get_political_economics_wisdom',
    'query_political_economics_by_problem',
    'get_institutional_analysis',
    'get_policy_game_insight',
    'get_regulatory_analysis',
]

政治经济学智慧核心模块 v1.0
Political Economics Wisdom Core Module

核心人物：李斯特、凯恩斯、哈耶克
核心思想：国家资本主义、宏观经济学奥地利学派

版本: V1.0
创建: 2026-04-24
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class PoliticalEconomicsDomain(Enum):
    """政治经济学应用领域"""
    INSTITUTIONAL_ANALYSIS = "制度分析"         # 制度变迁与设计
    POLICY_GAME = "政策博弈"                   # 政策制定与博弈
    REGULATORY = "政府监管"                    # 政府监管与市场
    TRADE_POLICY = "贸易政策"                  # 国际贸易政策
    INDUSTRIAL_POLICY = "产业政策"              # 产业扶持与发展
    MONETARY_POLICY = "货币政策"               # 货币政策与调控


@dataclass
class PoliticalEconomicsSageProfile:
    """政治经济学贤者画像"""
    name: str
    era: str
    nationality: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[PoliticalEconomicsDomain, int]


@dataclass
class PoliticalEconomicsResult:
    """政治经济学智慧查询结果"""
    sage_name: str
    problem: str
    institutional_insight: str
    policy_recommendations: List[str]
    stakeholder_analysis: Dict[str, str]
    recommendations: List[str]
    confidence: float


class PoliticalEconomicsWisdomCore:
    """
    政治经济学智慧核心

    提供制度分析、政策博弈、监管分析的智慧
    """

    def __init__(self):
        self._sages: Dict[str, PoliticalEconomicsSageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化政治经济学贤者数据"""

        # 弗里德里希·李斯特 (Friedrich List)
        self._sages["李斯特"] = PoliticalEconomicsSageProfile(
            name="李斯特",
            era="19世纪",
            nationality="德国",
            core_theories=[
                "国家经济学",
                "幼稚产业保护",
                "生产力理论",
                "关税保护",
            ],
            methodology=[
                "历史分析——从德国经济发展历史出发",
                "生产力分析——强调生产能力而非财富积累",
                "保护主义——幼稚产业需要国家保护才能成长",
            ],
            wisdom_laws=[
                "国家是经济发展的主体——自由市场需要国家引导",
                "幼稚产业需要保护——新兴产业在发展初期需要关税保护",
                "生产力是财富之源——生产能力比现有财富更重要",
                "时机至关重要——保护性政策应在适当时机退出",
            ],
            domain_strength={
                PoliticalEconomicsDomain.INSTITUTIONAL_ANALYSIS: 8,
                PoliticalEconomicsDomain.POLICY_GAME: 7,
                PoliticalEconomicsDomain.REGULATORY: 8,
                PoliticalEconomicsDomain.TRADE_POLICY: 10,
                PoliticalEconomicsDomain.INDUSTRIAL_POLICY: 10,
                PoliticalEconomicsDomain.MONETARY_POLICY: 6,
            },
        )

        # 约翰·梅纳德·凯恩斯 (John Maynard Keynes)
        self._sages["凯恩斯"] = PoliticalEconomicsSageProfile(
            name="凯恩斯",
            era="20世纪前半叶",
            nationality="英国",
            core_theories=[
                "宏观经济学",
                "有效需求",
                "政府干预",
                "流动性陷阱",
            ],
            methodology=[
                "总量分析——关注整体经济运行而非个体行为",
                "短期视角——经济危机的解决需要短期干预",
                "政府干预——市场失灵时需要政府刺激需求",
            ],
            wisdom_laws=[
                "有效需求决定产出——总需求不足导致经济衰退",
                "流动性陷阱——低利率政策在严重衰退时失效",
                "政府支出乘数效应——政府投资可放大经济刺激效果",
                "心理预期影响经济——动物精神影响投资和消费决策",
            ],
            domain_strength={
                PoliticalEconomicsDomain.INSTITUTIONAL_ANALYSIS: 7,
                PoliticalEconomicsDomain.POLICY_GAME: 9,
                PoliticalEconomicsDomain.REGULATORY: 9,
                PoliticalEconomicsDomain.TRADE_POLICY: 7,
                PoliticalEconomicsDomain.INDUSTRIAL_POLICY: 8,
                PoliticalEconomicsDomain.MONETARY_POLICY: 10,
            },
        )

        # 弗里德里希·哈耶克 (Friedrich Hayek)
        self._sages["哈耶克"] = PoliticalEconomicsSageProfile(
            name="哈耶克",
            era="20世纪",
            nationality="奥地利/英国",
            core_theories=[
                "自发秩序",
                "价格信号",
                "知识分散",
                "自由主义",
            ],
            methodology=[
                "演化视角——制度是长期演化的结果",
                "知识分析——分散知识是市场效率的基础",
                "批判理性主义——理性有限，设计能力受限",
            ],
            wisdom_laws=[
                "自发秩序——市场是自发形成的协调机制，不是设计的产物",
                "价格包含信息——价格传递分散知识，协调万千经济活动",
                "理性有限——人类理性无法设计复杂社会系统",
                "自由是前提——自由是经济效率和社会进步的基础",
            ],
            domain_strength={
                PoliticalEconomicsDomain.INSTITUTIONAL_ANALYSIS: 10,
                PoliticalEconomicsDomain.POLICY_GAME: 8,
                PoliticalEconomicsDomain.REGULATORY: 8,
                PoliticalEconomicsDomain.TRADE_POLICY: 9,
                PoliticalEconomicsDomain.INDUSTRIAL_POLICY: 6,
                PoliticalEconomicsDomain.MONETARY_POLICY: 8,
            },
        )

    def get_political_economics_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> PoliticalEconomicsResult:
        """
        获取政治经济学智慧

        Args:
            problem: 待分析的政策问题
            context: 上下文

        Returns:
            政治经济学智慧分析结果
        """
        context = context or {}
        domain = self._classify_problem_domain(problem)
        sage_name = self._select_best_sage(domain)
        sage = self._sages[sage_name]

        return PoliticalEconomicsResult(
            sage_name=sage_name,
            problem=problem,
            institutional_insight=self._analyze_institutions(problem, sage),
            policy_recommendations=self._generate_policy_recommendations(problem, sage),
            stakeholder_analysis=self._analyze_stakeholders(problem, sage),
            recommendations=self._generate_recommendations(sage, domain),
            confidence=0.86,
        )

    def query_political_economics_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询政治经济学智慧"""
        result = self.get_political_economics_wisdom(problem)
        return [{
            "sage": result.sage_name,
            "institutional_insight": result.institutional_insight,
            "policy_recommendations": result.policy_recommendations,
            "stakeholder_analysis": result.stakeholder_analysis,
            "recommendations": result.recommendations,
        }]

    def get_institutional_analysis(self, institution_type: str) -> Dict[str, str]:
        """获取制度分析"""
        return {
            "哈耶克视角": "制度是自发演化的结果，而非理性设计的产物——设计者无法预见所有后果",
            "凯恩斯视角": "制度设计需要考虑短期稳定性——市场失灵时需要政府干预",
            "李斯特视角": "发展中国家需要保护性制度——幼稚产业需要国家引导才能成长",
        }

    def get_policy_game_insight(self, policy_type: str) -> str:
        """获取政策博弈洞察"""
        return "凯恩斯的政策博弈理论：政策制定者在设计干预措施时需要考虑多重目标——经济增长、充分就业、物价稳定、国际平衡。政策效果取决于实施的时机和力度。"

    def get_regulatory_analysis(self, regulatory_type: str) -> str:
        """获取监管分析"""
        return "哈耶克的监管悖论：过度监管会破坏市场的自发秩序，但缺乏监管又会导致市场失灵。有效的监管应该维护竞争而非取代市场——保护游戏规则而非干预游戏结果。"

    def _classify_problem_domain(self, problem: str) -> PoliticalEconomicsDomain:
        """分类问题领域"""
        if any(k in problem for k in ["制度", "规则", "体制", "改革"]):
            return PoliticalEconomicsDomain.INSTITUTIONAL_ANALYSIS
        elif any(k in problem for k in ["政策", "博弈", "决策", "制定"]):
            return PoliticalEconomicsDomain.POLICY_GAME
        elif any(k in problem for k in ["监管", "管制", "政府", "行政"]):
            return PoliticalEconomicsDomain.REGULATORY
        elif any(k in problem for k in ["贸易", "关税", "出口", "进口"]):
            return PoliticalEconomicsDomain.TRADE_POLICY
        elif any(k in problem for k in ["产业", "扶持", "补贴", "发展"]):
            return PoliticalEconomicsDomain.INDUSTRIAL_POLICY
        elif any(k in problem for k in ["货币", "利率", "通胀", "信贷"]):
            return PoliticalEconomicsDomain.MONETARY_POLICY
        return PoliticalEconomicsDomain.POLICY_GAME

    def _analyze_institutions(self, problem: str, sage: PoliticalEconomicsSageProfile) -> str:
        """分析制度"""
        return "哈耶克的自发秩序理论：制度是无数个体互动长期演化的结果，而非任何单一设计者能够完全掌控。有效的制度应该保护个人自由，允许自发协调。"

    def _generate_policy_recommendations(self, problem: str, sage: PoliticalEconomicsSageProfile) -> List[str]:
        """生成政策建议"""
        return [
            "时机分析：政策干预需要在正确的时间窗口内实施",
            "力度把控：政策力度应与问题严重程度相匹配",
            "退出机制：政策设计应包含明确的退出条件和时间表",
            "预期管理：政策效果部分取决于市场预期",
        ]

    def _analyze_stakeholders(self, problem: str, sage: PoliticalEconomicsSageProfile) -> Dict[str, str]:
        """分析利益相关者"""
        return {
            "受益者": "政策获益群体分析",
            "受损者": "政策受损群体分析",
            "议价能力": "各利益相关者的议价能力和影响力",
            "联盟构建": "利益联盟的形成与瓦解",
        }

    def _select_best_sage(self, domain: PoliticalEconomicsDomain) -> str:
        """选择最合适的政治经济学家"""
        scores = {name: sage.domain_strength.get(domain, 5) for name, sage in self._sages.items()}
        return max(scores, key=scores.get)

    def _generate_recommendations(self, sage: PoliticalEconomicsSageProfile, domain: PoliticalEconomicsDomain) -> List[str]:
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
_ENGINE: Optional[PoliticalEconomicsWisdomCore] = None


def get_political_economics_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> PoliticalEconomicsResult:
    """获取政治经济学智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = PoliticalEconomicsWisdomCore()
    return _ENGINE.get_political_economics_wisdom(problem, context)


def query_political_economics_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询政治经济学智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = PoliticalEconomicsWisdomCore()
    return _ENGINE.query_political_economics_by_problem(problem)


def get_institutional_analysis(institution_type: str) -> Dict[str, str]:
    """获取制度分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = PoliticalEconomicsWisdomCore()
    return _ENGINE.get_institutional_analysis(institution_type)


def get_policy_game_insight(policy_type: str) -> str:
    """获取政策博弈洞察"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = PoliticalEconomicsWisdomCore()
    return _ENGINE.get_policy_game_insight(policy_type)


def get_regulatory_analysis(regulatory_type: str) -> str:
    """获取监管分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = PoliticalEconomicsWisdomCore()
    return _ENGINE.get_regulatory_analysis(regulatory_type)
