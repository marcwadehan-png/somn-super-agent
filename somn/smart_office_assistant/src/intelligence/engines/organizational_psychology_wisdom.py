"""
__all__ = [
    'get_organizational_psychology_wisdom',
    'query_org_psychology_by_problem',
    'get_org_change_analysis',
    'get_leadership_insight',
    'get_team_dynamics_guidance',
]

组织心理学智慧核心模块 v1.0
Organizational Psychology Wisdom Core Module

核心人物：阿吉里斯、舍恩、沙因
核心思想：行动科学、组织学习、权变理论

版本: V1.0
创建: 2026-04-24
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class OrganizationalPsychologyDomain(Enum):
    """组织心理学应用领域"""
    ORG_CHANGE = "组织变革"                # 组织变革与管理
    LEADERSHIP = "领导力"                 # 领导风格与发展
    TEAM_DYNAMICS = "团队动力学"          # 团队建设与协作
    ORG_LEARNING = "组织学习"             # 组织学习与知识管理
    CULTURE_ANALYSIS = "组织文化"         # 组织文化诊断
    CONFLICT_RESOLUTION = "冲突解决"       # 组织冲突管理


@dataclass
class OrganizationalPsychologySageProfile:
    """组织心理学贤者画像"""
    name: str
    era: str
    nationality: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[OrganizationalPsychologyDomain, int]


@dataclass
class OrganizationalPsychologyResult:
    """组织心理学智慧查询结果"""
    sage_name: str
    problem: str
    diagnostic_insights: Dict[str, str]
    intervention_strategies: List[str]
    recommendations: List[str]
    confidence: float


class OrganizationalPsychologyWisdomCore:
    """
    组织心理学智慧核心

    提供组织变革、领导力、团队动力的智慧
    """

    def __init__(self):
        self._sages: Dict[str, OrganizationalPsychologySageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化组织心理学贤者数据"""

        # 克里斯·阿吉里斯 (Chris Argyris)
        self._sages["阿吉里斯"] = OrganizationalPsychologySageProfile(
            name="阿吉里斯",
            era="20世纪后半叶至今",
            nationality="美国",
            core_theories=[
                "行动科学",
                "单环/双环学习",
                "组织防卫",
                "推论阶梯",
            ],
            methodology=[
                "行动研究——在实践中研究和改进",
                "左手栏技术——揭示未被表达的假设",
                "反思性实践——从行动中学习",
            ],
            wisdom_laws=[
                "组织防卫阻碍学习——保护性的组织行为阻碍真实学习和变革",
                "单环学习vs双环学习——仅调整行为是不够的，需要改变心智模式",
                "说一套做一套——组织中公开的理论与实行的理论存在差距",
                "推论导致盲区——基于未检验假设的行动会产生非预期后果",
            ],
            domain_strength={
                OrganizationalPsychologyDomain.ORG_CHANGE: 9,
                OrganizationalPsychologyDomain.LEADERSHIP: 8,
                OrganizationalPsychologyDomain.TEAM_DYNAMICS: 7,
                OrganizationalPsychologyDomain.ORG_LEARNING: 10,
                OrganizationalPsychologyDomain.CULTURE_ANALYSIS: 8,
                OrganizationalPsychologyDomain.CONFLICT_RESOLUTION: 9,
            },
        )

        # 唐纳德·舍恩 (Donald Schön)
        self._sages["舍恩"] = OrganizationalPsychologySageProfile(
            name="舍恩",
            era="20世纪后半叶",
            nationality="美国",
            core_theories=[
                "反思性实践",
                "行动中的知识",
                "专业主义危机",
                "情境学习",
            ],
            methodology=[
                "实践反思——从专业实践行动中提取知识",
                "情境学习——在真实情境中培养能力",
                "行动中反思——边做边思考边改进",
            ],
            wisdom_laws=[
                "行动中反思——专业人士在行动中进行即时反思",
                "专业知识在行动里——知识嵌入在专业实践中，难以形式化",
                "情境学习——能力的培养需要在真实情境中练习",
                "专业主义危机——形式化的专业知识难以应对复杂情境",
            ],
            domain_strength={
                OrganizationalPsychologyDomain.ORG_CHANGE: 7,
                OrganizationalPsychologyDomain.LEADERSHIP: 7,
                OrganizationalPsychologyDomain.TEAM_DYNAMICS: 8,
                OrganizationalPsychologyDomain.ORG_LEARNING: 10,
                OrganizationalPsychologyDomain.CULTURE_ANALYSIS: 7,
                OrganizationalPsychologyDomain.CONFLICT_RESOLUTION: 8,
            },
        )

        # 埃德加·沙因 (Edgar Schein)
        self._sages["沙因"] = OrganizationalPsychologySageProfile(
            name="沙因",
            era="20世纪后半叶至今",
            nationality="美国",
            core_theories=[
                "组织文化",
                "过程咨询",
                "职业锚",
                "谦逊询问",
            ],
            methodology=[
                "文化层次分析——人工制品、价值观、基本假设",
                "过程咨询——通过关系和对话帮助客户成长",
                "文化变革——从底层假设开始改变",
            ],
            wisdom_laws=[
                "文化是根本——深层假设决定了表层行为和人工制品",
                "过程即内容——关系和对话方式本身就是组织文化",
                "谦逊询问——真正帮助需要放下专家姿态",
                "文化变革缓慢——基本假设难以一夜改变",
            ],
            domain_strength={
                OrganizationalPsychologyDomain.ORG_CHANGE: 10,
                OrganizationalPsychologyDomain.LEADERSHIP: 10,
                OrganizationalPsychologyDomain.TEAM_DYNAMICS: 9,
                OrganizationalPsychologyDomain.ORG_LEARNING: 8,
                OrganizationalPsychologyDomain.CULTURE_ANALYSIS: 10,
                OrganizationalPsychologyDomain.CONFLICT_RESOLUTION: 9,
            },
        )

    def get_organizational_psychology_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> OrganizationalPsychologyResult:
        """
        获取组织心理学智慧

        Args:
            problem: 待分析的组织问题
            context: 上下文

        Returns:
            组织心理学智慧分析结果
        """
        context = context or {}
        domain = self._classify_problem_domain(problem)
        sage_name = self._select_best_sage(domain)
        sage = self._sages[sage_name]

        return OrganizationalPsychologyResult(
            sage_name=sage_name,
            problem=problem,
            diagnostic_insights=self._diagnose_issue(problem, sage),
            intervention_strategies=self._design_intervention(problem, sage),
            recommendations=self._generate_recommendations(sage, domain),
            confidence=0.87,
        )

    def query_org_psychology_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询组织心理学智慧"""
        result = self.get_organizational_psychology_wisdom(problem)
        return [{
            "sage": result.sage_name,
            "diagnostic_insights": result.diagnostic_insights,
            "intervention_strategies": result.intervention_strategies,
            "recommendations": result.recommendations,
        }]

    def get_org_change_analysis(self, change_type: str) -> Dict[str, str]:
        """获取组织变革分析"""
        return {
            "沙因视角": "组织变革需要从基本假设开始——表层改变不等于深层变革",
            "阿吉里斯视角": "组织变革需要打破防卫机制——双环学习比单环学习更重要",
            "舍恩视角": "变革发生在行动中——边做边反思边调整",
        }

    def get_leadership_insight(self, leadership_type: str) -> str:
        """获取领导力洞察"""
        return "沙因的领导力理论：领导者的首要任务是塑造和维护组织文化。在危机时刻，领导者的真实行为比言语更能传达组织价值观。谦逊询问而非专家姿态更能建立信任。"

    def get_team_dynamics_guidance(self, dynamics_type: str) -> str:
        """获取团队动力学指导"""
        return "阿吉里斯的团队动力学分析：高效团队能够进行公开的讨论，即使涉及敏感话题。团队需要打破防卫机制，建立信任，才能实现真正的双环学习。"

    def _classify_problem_domain(self, problem: str) -> OrganizationalPsychologyDomain:
        """分类问题领域"""
        if any(k in problem for k in ["变革", "转型", "改革", "变革管理"]):
            return OrganizationalPsychologyDomain.ORG_CHANGE
        elif any(k in problem for k in ["领导", "管理者", "管理风格", "指导"]):
            return OrganizationalPsychologyDomain.LEADERSHIP
        elif any(k in problem for k in ["团队", "协作", "合作", "团队建设"]):
            return OrganizationalPsychologyDomain.TEAM_DYNAMICS
        elif any(k in problem for k in ["学习", "知识", "培训", "发展"]):
            return OrganizationalPsychologyDomain.ORG_LEARNING
        elif any(k in problem for k in ["文化", "价值观", "氛围", "风格"]):
            return OrganizationalPsychologyDomain.CULTURE_ANALYSIS
        elif any(k in problem for k in ["冲突", "矛盾", "争议", "分歧"]):
            return OrganizationalPsychologyDomain.CONFLICT_RESOLUTION
        return OrganizationalPsychologyDomain.ORG_CHANGE

    def _diagnose_issue(self, problem: str, sage: OrganizationalPsychologySageProfile) -> Dict[str, str]:
        """诊断问题"""
        return {
            "表层问题": "问题表象",
            "深层原因": "阿吉里斯：可能存在组织防卫机制",
            "变革阻力": "沙因：基本假设未改变，变革难以持续",
        }

    def _design_intervention(self, problem: str, sage: OrganizationalPsychologySageProfile) -> List[str]:
        """设计干预策略"""
        return [
            "过程咨询：关注关系和对话方式，而非仅关注内容",
            "反思性实践：鼓励在行动中进行即时反思",
            "双环学习：挑战基本假设，而非仅调整行为",
            "文化干预：从人工制品到价值观再到基本假设",
        ]

    def _select_best_sage(self, domain: OrganizationalPsychologyDomain) -> str:
        """选择最合适的组织心理学家"""
        scores = {name: sage.domain_strength.get(domain, 5) for name, sage in self._sages.items()}
        return max(scores, key=scores.get)

    def _generate_recommendations(self, sage: OrganizationalPsychologySageProfile, domain: OrganizationalPsychologyDomain) -> List[str]:
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
_ENGINE: Optional[OrganizationalPsychologyWisdomCore] = None


def get_organizational_psychology_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> OrganizationalPsychologyResult:
    """获取组织心理学智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = OrganizationalPsychologyWisdomCore()
    return _ENGINE.get_organizational_psychology_wisdom(problem, context)


def query_org_psychology_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询组织心理学智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = OrganizationalPsychologyWisdomCore()
    return _ENGINE.query_org_psychology_by_problem(problem)


def get_org_change_analysis(change_type: str) -> Dict[str, str]:
    """获取组织变革分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = OrganizationalPsychologyWisdomCore()
    return _ENGINE.get_org_change_analysis(change_type)


def get_leadership_insight(leadership_type: str) -> str:
    """获取领导力洞察"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = OrganizationalPsychologyWisdomCore()
    return _ENGINE.get_leadership_insight(leadership_type)


def get_team_dynamics_guidance(dynamics_type: str) -> str:
    """获取团队动力学指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = OrganizationalPsychologyWisdomCore()
    return _ENGINE.get_team_dynamics_guidance(dynamics_type)
