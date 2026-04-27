"""
__all__ = [
    'get_sociology_wisdom',
    'query_sociology_by_problem',
    'get_social_structure_analysis',
    'get_group_behavior_insight',
    'get_social_mobility_guidance',
]

社会学智慧核心模块 v1.0
Sociology Wisdom Core Module

社会学三巨头：涂尔干、韦伯、马克思
核心思想：社会事实、理解社会学、历史唯物主义

版本: V1.0
创建: 2026-04-24
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SociologyDomain(Enum):
    """社会学应用领域"""
    SOCIAL_STRUCTURE = "社会结构"           # 社会阶层、组织、制度分析
    GROUP_BEHAVIOR = "群体行为"             # 集体行动、群体动力学
    SOCIAL_MOBILITY = "社会流动"             # 阶层流动、社会流动分析
    INSTITUTIONAL_ANALYSIS = "制度分析"     # 社会制度、规则分析
    SOCIAL_CHANGE = "社会变迁"              # 社会转型、变革分析
    CULTURAL_ANALYSIS = "文化分析"          # 社会文化、价值观分析


@dataclass
class SociologySageProfile:
    """社会学贤者画像"""
    name: str
    era: str
    nationality: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[SociologyDomain, int]


@dataclass
class SociologyWisdomResult:
    """社会学智慧查询结果"""
    sage_name: str
    problem: str
    social_structure: Dict[str, str]
    group_dynamics: str
    institutional_insight: str
    recommendations: List[str]
    confidence: float


class SociologyWisdomCore:
    """
    社会学智慧核心

    提供社会结构、群体行为、社会流动的智慧分析
    """

    def __init__(self):
        self._sages: Dict[str, SociologySageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化社会学贤者数据"""

        # 涂尔干 (Émile Durkheim)
        self._sages["涂尔干"] = SociologySageProfile(
            name="涂尔干",
            era="19世纪末-20世纪初",
            nationality="法国",
            core_theories=[
                "社会事实",
                "集体意识",
                "社会分工",
                "社会团结",
                "失范理论",
            ],
            methodology=[
                "社会事实研究——将社会现象作为客观事物来研究",
                "社会整合分析——个人与社会的关系",
                "集体意识分析——社会共享的信仰和价值观",
            ],
            wisdom_laws=[
                "社会事实先于个体——个人的行为和思想受社会事实制约",
                "集体意识塑造个体——社会共享的价值观影响个人选择",
                "社会分工促进团结——相互依赖是社会凝聚力的基础",
                "失范导致越轨——规范缺失时社会问题增加",
            ],
            domain_strength={
                SociologyDomain.SOCIAL_STRUCTURE: 10,
                SociologyDomain.GROUP_BEHAVIOR: 8,
                SociologyDomain.SOCIAL_MOBILITY: 7,
                SociologyDomain.INSTITUTIONAL_ANALYSIS: 9,
                SociologyDomain.SOCIAL_CHANGE: 8,
                SociologyDomain.CULTURAL_ANALYSIS: 8,
            },
        )

        # 马克斯·韦伯 (Max Weber)
        self._sages["韦伯"] = SociologySageProfile(
            name="韦伯",
            era="19世纪末-20世纪初",
            nationality="德国",
            core_theories=[
                "理解社会学",
                "理性化",
                "科层制",
                "社会行动",
                "理想类型",
            ],
            methodology=[
                "理解行动者主观意义——从行动者视角理解社会行为",
                "理想类型分析——建立分析概念模型",
                "多因素因果分析——社会现象的多重原因",
            ],
            wisdom_laws=[
                "理解是社会学的基础——理解行动者的主观意义比客观观察更重要",
                "理性化是现代社会的特征——目的理性行动日益主导",
                "科层制是理性化的组织形式——效率与控制的矛盾",
                "社会地位的多维性——阶级、身份、权力是不同维度",
            ],
            domain_strength={
                SociologyDomain.SOCIAL_STRUCTURE: 9,
                SociologyDomain.GROUP_BEHAVIOR: 9,
                SociologyDomain.SOCIAL_MOBILITY: 10,
                SociologyDomain.INSTITUTIONAL_ANALYSIS: 10,
                SociologyDomain.SOCIAL_CHANGE: 9,
                SociologyDomain.CULTURAL_ANALYSIS: 8,
            },
        )

        # 卡尔·马克思 (Karl Marx)
        self._sages["马克思"] = SociologySageProfile(
            name="马克思",
            era="19世纪",
            nationality="德国",
            core_theories=[
                "历史唯物主义",
                "阶级斗争",
                "意识形态",
                "剩余价值",
                "上层建筑",
            ],
            methodology=[
                "历史分析——从历史发展中理解社会结构",
                "阶级分析——社会分为统治阶级和被统治阶级",
                "经济基础决定上层建筑——物质生产方式塑造社会制度",
            ],
            wisdom_laws=[
                "社会存在决定社会意识——物质生活制约精神生活",
                "阶级斗争是历史动力——社会变革源于阶级矛盾",
                "意识形态是统治工具——统治阶级用意识形态维护统治",
                "生产力与生产关系的矛盾——技术进步导致社会变革",
            ],
            domain_strength={
                SociologyDomain.SOCIAL_STRUCTURE: 10,
                SociologyDomain.GROUP_BEHAVIOR: 7,
                SociologyDomain.SOCIAL_MOBILITY: 8,
                SociologyDomain.INSTITUTIONAL_ANALYSIS: 8,
                SociologyDomain.SOCIAL_CHANGE: 10,
                SociologyDomain.CULTURAL_ANALYSIS: 9,
            },
        )

    def get_sociology_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> SociologyWisdomResult:
        """
        获取社会学智慧

        Args:
            problem: 待分析的社会问题
            context: 上下文

        Returns:
            社会学智慧分析结果
        """
        context = context or {}

        # 分析问题领域
        domain = self._classify_problem_domain(problem)

        # 选择最合适的贤者
        sage_name = self._select_best_sage(domain)
        sage = self._sages[sage_name]

        return SociologyWisdomResult(
            sage_name=sage_name,
            problem=problem,
            social_structure=self._analyze_social_structure(problem, sage),
            group_dynamics=self._analyze_group_dynamics(problem, sage),
            institutional_insight=self._analyze_institutions(problem, sage),
            recommendations=self._generate_recommendations(sage, domain),
            confidence=0.85,
        )

    def query_sociology_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询社会学智慧"""
        result = self.get_sociology_wisdom(problem)
        return [{
            "sage": result.sage_name,
            "social_structure": result.social_structure,
            "group_dynamics": result.group_dynamics,
            "institutional_insight": result.institutional_insight,
            "recommendations": result.recommendations,
        }]

    def get_social_structure_analysis(self, structure_type: str) -> Dict[str, str]:
        """获取社会结构分析"""
        analyses = {
            "阶层": "社会阶层分析：上、中、下阶层的资源分配和机会结构",
            "组织": "社会组织分析：正式组织与非正式群体的结构和功能",
            "制度": "社会制度分析：制度如何规范社会行为和维护社会秩序",
        }
        return {
            "分析类型": analyses.get(structure_type, "综合社会结构分析"),
            "涂尔干视角": "社会结构是客观存在的外在事实，塑造个体行为",
            "韦伯视角": "社会结构是多维的：阶级、身份、权力三个维度",
            "马克思视角": "社会结构是阶级关系的反映，经济基础决定上层建筑",
        }

    def get_group_behavior_insight(self, group_type: str) -> str:
        """获取群体行为洞察"""
        return f"从社会学视角看{group_type}：群体行为受集体意识、规范、价值观的深刻影响。涂尔干的集体意识理论揭示：个体在群体中会产生超越个人的社会力量。"

    def get_social_mobility_guidance(self, mobility_type: str) -> str:
        """获取社会流动指导"""
        return "韦伯的社会流动分析：向上流动需要资源、机会和社会网络。结构性障碍（制度歧视）和文化障碍（身份认同）都会影响社会流动。"

    def _classify_problem_domain(self, problem: str) -> SociologyDomain:
        """分类问题领域"""
        if any(k in problem for k in ["阶层", "结构", "组织", "制度", "社会分层"]):
            return SociologyDomain.SOCIAL_STRUCTURE
        elif any(k in problem for k in ["群体", "集体", "大众", "从众", "群体行为"]):
            return SociologyDomain.GROUP_BEHAVIOR
        elif any(k in problem for k in ["流动", "晋升", "上升", "下沉", "代际"]):
            return SociologyDomain.SOCIAL_MOBILITY
        elif any(k in problem for k in ["规范", "规则", "法律", "制度设计"]):
            return SociologyDomain.INSTITUTIONAL_ANALYSIS
        elif any(k in problem for k in ["变革", "转型", "变迁", "革命", "改革"]):
            return SociologyDomain.SOCIAL_CHANGE
        elif any(k in problem for k in ["文化", "价值观", "信仰", "意识形态"]):
            return SociologyDomain.CULTURAL_ANALYSIS
        return SociologyDomain.SOCIAL_STRUCTURE

    def _analyze_social_structure(self, problem: str, sage: SociologySageProfile) -> Dict[str, str]:
        """分析社会结构"""
        return {
            "问题核心": "分析问题涉及的社会结构因素",
            "涂尔干视角": "社会结构是独立于个人的客观存在，塑造个体行为模式",
            "韦伯视角": "社会结构是多维的：经济（阶级）、社会（身份）、政治（权力）",
            "马克思视角": "社会结构是阶级关系的体现，统治阶级控制生产资料",
        }

    def _analyze_group_dynamics(self, problem: str, sage: SociologySageProfile) -> str:
        """分析群体动力学"""
        return "涂尔干的集体意识理论：群体成员共享的信仰和情感形成集体意识，塑造个体行为。群体凝聚力来自集体意识，而非单纯个人利益。"

    def _analyze_institutions(self, problem: str, sage: SociologySageProfile) -> str:
        """分析制度"""
        return "韦伯的科层制理论：制度是理性化的产物，提供可预期的行为框架。但科层制也可能导致非人格化、效率与公平的矛盾。"

    def _select_best_sage(self, domain: SociologyDomain) -> str:
        """选择最合适的社会学家"""
        scores = {name: sage.domain_strength.get(domain, 5) for name, sage in self._sages.items()}
        return max(scores, key=scores.get)

    def _generate_recommendations(self, sage: SociologySageProfile, domain: SociologyDomain) -> List[str]:
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
_ENGINE: Optional[SociologyWisdomCore] = None


def get_sociology_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> SociologyWisdomResult:
    """获取社会学智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SociologyWisdomCore()
    return _ENGINE.get_sociology_wisdom(problem, context)


def query_sociology_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询社会学智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SociologyWisdomCore()
    return _ENGINE.query_sociology_by_problem(problem)


def get_social_structure_analysis(structure_type: str) -> Dict[str, str]:
    """获取社会结构分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SociologyWisdomCore()
    return _ENGINE.get_social_structure_analysis(structure_type)


def get_group_behavior_insight(group_type: str) -> str:
    """获取群体行为洞察"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SociologyWisdomCore()
    return _ENGINE.get_group_behavior_insight(group_type)


def get_social_mobility_guidance(mobility_type: str) -> str:
    """获取社会流动指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SociologyWisdomCore()
    return _ENGINE.get_social_mobility_guidance(mobility_type)
