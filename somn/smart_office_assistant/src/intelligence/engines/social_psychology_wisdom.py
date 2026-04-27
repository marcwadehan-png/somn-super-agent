"""
__all__ = [
    'get_social_psychology_wisdom',
    'query_social_psychology_by_problem',
    'get_conformity_analysis',
    'get_authority_insight',
    'get_social_influence_guidance',
]

社会心理学智慧核心模块 v1.0
Social Psychology Wisdom Core Module

核心人物：米尔格拉姆、阿希、津巴多
核心思想：服从权威、从众效应、社会影响力

版本: V1.0
创建: 2026-04-24
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SocialPsychologyDomain(Enum):
    """社会心理学应用领域"""
    CONFORMITY = "从众效应"              # 群体压力与从众
    AUTHORITY_OBEDIENCE = "权威服从"      # 对权威的服从
    SOCIAL_INFLUENCE = "社会影响"        # 说服与影响策略
    GROUP_DYNAMICS = "群体动力"           # 群体行为与决策
    SELF_PRESENTATION = "自我呈现"        # 社会角色与自我
    PROSOCIAL = "亲社会行为"              # 利他、合作与社会公正


@dataclass
class SocialPsychologySageProfile:
    """社会心理学贤者画像"""
    name: str
    era: str
    nationality: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[SocialPsychologyDomain, int]


@dataclass
class SocialPsychologyResult:
    """社会心理学智慧查询结果"""
    sage_name: str
    problem: str
    behavioral_insights: Dict[str, str]
    influence_strategies: List[str]
    recommendations: List[str]
    confidence: float


class SocialPsychologyWisdomCore:
    """
    社会心理学智慧核心

    提供从众效应、权威服从、社会影响的智慧
    """

    def __init__(self):
        self._sages: Dict[str, SocialPsychologySageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化社会心理学贤者数据"""

        # 斯坦利·米尔格拉姆 (Stanley Milgram)
        self._sages["米尔格拉姆"] = SocialPsychologySageProfile(
            name="米尔格拉姆",
            era="20世纪中叶",
            nationality="美国",
            core_theories=[
                "服从权威",
                "电击实验",
                "代理自动性",
                "社会链接",
            ],
            methodology=[
                "实验研究——通过控制实验揭示社会行为规律",
                "情境力量——关注情境而非性格决定行为",
                "社会联结分析——分析服从行为的社会基础",
            ],
            wisdom_laws=[
                "普通人在权威命令下会伤害他人——情境力量比性格更能预测行为",
                "代理自动性——当他人承担责任时，我们更易服从",
                "渐进式承诺——从小到大逐步增加服从程度",
                "距离效应——物理和社会距离影响服从程度",
            ],
            domain_strength={
                SocialPsychologyDomain.CONFORMITY: 7,
                SocialPsychologyDomain.AUTHORITY_OBEDIENCE: 10,
                SocialPsychologyDomain.SOCIAL_INFLUENCE: 9,
                SocialPsychologyDomain.GROUP_DYNAMICS: 8,
                SocialPsychologyDomain.SELF_PRESENTATION: 6,
                SocialPsychologyDomain.PROSOCIAL: 7,
            },
        )

        # 所罗门·阿希 (Solomon Asch)
        self._sages["阿希"] = SocialPsychologySageProfile(
            name="阿希",
            era="20世纪中叶",
            nationality="美国",
            core_theories=[
                "从众实验",
                "信息性社会影响",
                "规范性社会影响",
                "群体压力",
            ],
            methodology=[
                "从众实验——控制群体情境观察个体反应",
                "从众类型区分——信息性vs规范性影响",
                "促进独立性——识别打破从众的条件",
            ],
            wisdom_laws=[
                "群体压力能扭曲个体判断——多数人的意见会压倒个人感知",
                "信息性社会影响——当情境模糊时，我们依赖他人判断",
                "规范性社会影响——我们从众是因为害怕被拒绝",
                "一致性是关键——哪怕只有3个人也能产生巨大从众压力",
            ],
            domain_strength={
                SocialPsychologyDomain.CONFORMITY: 10,
                SocialPsychologyDomain.AUTHORITY_OBEDIENCE: 7,
                SocialPsychologyDomain.SOCIAL_INFLUENCE: 10,
                SocialPsychologyDomain.GROUP_DYNAMICS: 9,
                SocialPsychologyDomain.SELF_PRESENTATION: 8,
                SocialPsychologyDomain.PROSOCIAL: 6,
            },
        )

        # 菲利普·津巴多 (Philip Zimbardo)
        self._sages["津巴多"] = SocialPsychologySageProfile(
            name="津巴多",
            era="20世纪后半叶至今",
            nationality="美国",
            core_theories=[
                "斯坦福监狱实验",
                "时间观理论",
                "英雄想象",
                "情境vs性格",
            ],
            methodology=[
                "情境实验——在模拟情境中观察行为变化",
                "时间透视——从时间观角度理解行为",
                "英雄培训——培养面对情境压力的勇气",
            ],
            wisdom_laws=[
                "情境决定行为——善恶取决于情境而非性格",
                "角色塑造行为——当我们扮演某个角色时，会内化角色行为",
                "去个性化——群体中个人身份感减弱，易产生极端行为",
                "英雄需要培育——识别和培养潜在的英雄行为",
            ],
            domain_strength={
                SocialPsychologyDomain.CONFORMITY: 9,
                SocialPsychologyDomain.AUTHORITY_OBEDIENCE: 9,
                SocialPsychologyDomain.SOCIAL_INFLUENCE: 8,
                SocialPsychologyDomain.GROUP_DYNAMICS: 10,
                SocialPsychologyDomain.SELF_PRESENTATION: 10,
                SocialPsychologyDomain.PROSOCIAL: 9,
            },
        )

    def get_social_psychology_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> SocialPsychologyResult:
        """
        获取社会心理学智慧

        Args:
            problem: 待分析的社会心理问题
            context: 上下文

        Returns:
            社会心理学智慧分析结果
        """
        context = context or {}
        domain = self._classify_problem_domain(problem)
        sage_name = self._select_best_sage(domain)
        sage = self._sages[sage_name]

        return SocialPsychologyResult(
            sage_name=sage_name,
            problem=problem,
            behavioral_insights=self._analyze_behavior(problem, sage),
            influence_strategies=self._design_influence(problem, sage),
            recommendations=self._generate_recommendations(sage, domain),
            confidence=0.86,
        )

    def query_social_psychology_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询社会心理学智慧"""
        result = self.get_social_psychology_wisdom(problem)
        return [{
            "sage": result.sage_name,
            "behavioral_insights": result.behavioral_insights,
            "influence_strategies": result.influence_strategies,
            "recommendations": result.recommendations,
        }]

    def get_conformity_analysis(self, conformity_type: str) -> Dict[str, str]:
        """获取从众分析"""
        return {
            "阿希视角": "群体压力能扭曲个体判断——从众源于信息性和规范性社会影响",
            "津巴多视角": "去个性化增加从众——匿名性降低自我约束",
            "米尔格拉姆视角": "代理自动性使个体停止独立判断——让渡责任给权威",
        }

    def get_authority_insight(self, authority_type: str) -> str:
        """获取权威服从洞察"""
        return "米尔格拉姆的服从实验：普通人在权威命令下会做出伤害他人的行为。这提醒我们：制度和流程设计需要内置防止滥用的机制，个人需要保持独立判断的勇气。"

    def get_social_influence_guidance(self, influence_type: str) -> str:
        """获取社会影响指导"""
        return "津巴多的社会影响分析：有效的社会影响需要考虑情境力量——改变情境比改变个人更有效。同时，培养独立思考的能力和勇气，是抵御不良社会影响的关键。"

    def _classify_problem_domain(self, problem: str) -> SocialPsychologyDomain:
        """分类问题领域"""
        if any(k in problem for k in ["从众", "群体压力", "一致", "多数"]):
            return SocialPsychologyDomain.CONFORMITY
        elif any(k in problem for k in ["服从", "权威", "命令", "指令"]):
            return SocialPsychologyDomain.AUTHORITY_OBEDIENCE
        elif any(k in problem for k in ["影响", "说服", "改变态度", "社会影响"]):
            return SocialPsychologyDomain.SOCIAL_INFLUENCE
        elif any(k in problem for k in ["群体", "团队决策", "群体思维", "去个性化"]):
            return SocialPsychologyDomain.GROUP_DYNAMICS
        elif any(k in problem for k in ["自我", "角色", "身份", "自我呈现"]):
            return SocialPsychologyDomain.SELF_PRESENTATION
        elif any(k in problem for k in ["利他", "合作", "公正", "亲社会"]):
            return SocialPsychologyDomain.PROSOCIAL
        return SocialPsychologyDomain.SOCIAL_INFLUENCE

    def _analyze_behavior(self, problem: str, sage: SocialPsychologySageProfile) -> Dict[str, str]:
        """分析行为"""
        return {
            "情境因素": "米尔格拉姆：情境力量比性格更能预测行为",
            "群体影响": "阿希：多数人意见会产生强大压力",
            "角色效应": "津巴多：角色会塑造行为而非仅反映性格",
        }

    def _design_influence(self, problem: str, sage: SocialPsychologySageProfile) -> List[str]:
        """设计影响策略"""
        return [
            "社会认同：利用目标群体的参照群体",
            "权威效应：合法权威的建议更有影响力",
            "一致性：强调与先前承诺的一致性",
            "稀缺性：稀缺资源激发更强烈的获取欲望",
        ]

    def _select_best_sage(self, domain: SocialPsychologyDomain) -> str:
        """选择最合适的社会心理学家"""
        scores = {name: sage.domain_strength.get(domain, 5) for name, sage in self._sages.items()}
        return max(scores, key=scores.get)

    def _generate_recommendations(self, sage: SocialPsychologySageProfile, domain: SocialPsychologyDomain) -> List[str]:
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
_ENGINE: Optional[SocialPsychologyWisdomCore] = None


def get_social_psychology_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> SocialPsychologyResult:
    """获取社会心理学智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SocialPsychologyWisdomCore()
    return _ENGINE.get_social_psychology_wisdom(problem, context)


def query_social_psychology_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询社会心理学智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SocialPsychologyWisdomCore()
    return _ENGINE.query_social_psychology_by_problem(problem)


def get_conformity_analysis(conformity_type: str) -> Dict[str, str]:
    """获取从众分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SocialPsychologyWisdomCore()
    return _ENGINE.get_conformity_analysis(conformity_type)


def get_authority_insight(authority_type: str) -> str:
    """获取权威服从洞察"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SocialPsychologyWisdomCore()
    return _ENGINE.get_authority_insight(authority_type)


def get_social_influence_guidance(influence_type: str) -> str:
    """获取社会影响指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SocialPsychologyWisdomCore()
    return _ENGINE.get_social_influence_guidance(influence_type)
