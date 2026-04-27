"""
__all__ = [
    'get_communication_wisdom',
    'query_communication_by_problem',
    'get_media_theory_analysis',
    'get_public_opinion_insight',
    'get_message_design_guidance',
]

传播学智慧核心模块 v1.0
Communication Wisdom Core Module

核心人物：麦克卢汉、鲍德里亚、哈贝马斯
核心思想：媒介即讯息、拟象理论、交往理性

版本: V6.2
创建: 2026-04-24
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class CommunicationDomain(Enum):
    """传播学应用领域"""
    MEDIA_THEORY = "媒介理论"              # 媒介形式与影响
    PUBLIC_OPINION = "舆论形成"            # 舆论生成与演变
    MESSAGE_DESIGN = "信息设计"            # 传播内容与策略
    CRISIS_COMMUNICATION = "危机传播"      # 危机公关与应对
    INTERPERSONAL = "人际传播"              # 面对面沟通
    ORGANIZATIONAL = "组织传播"            # 组织内部沟通


@dataclass
class CommunicationSageProfile:
    """传播学贤者画像"""
    name: str
    era: str
    nationality: str
    core_theories: List[str]
    methodology: List[str]
    wisdom_laws: List[str]
    domain_strength: Dict[CommunicationDomain, int]


@dataclass
class CommunicationWisdomResult:
    """传播学智慧查询结果"""
    sage_name: str
    problem: str
    media_analysis: str
    message_strategy: List[str]
    audience_insight: Dict[str, str]
    recommendations: List[str]
    confidence: float


class CommunicationWisdomCore:
    """
    传播学智慧核心

    提供媒介理论、舆论分析、信息设计的智慧
    """

    def __init__(self):
        self._sages: Dict[str, CommunicationSageProfile] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """初始化传播学贤者数据"""

        # 马歇尔·麦克卢汉 (Marshall McLuhan)
        self._sages["麦克卢汉"] = CommunicationSageProfile(
            name="麦克卢汉",
            era="20世纪中叶",
            nationality="加拿大",
            core_theories=[
                "媒介即讯息",
                "媒介即按摩",
                "冷媒介与热媒介",
                "地球村",
                "感官比率",
            ],
            methodology=[
                "媒介形式分析——关注媒介本身而非内容",
                "感官比率分析——媒介如何改变感知模式",
                "技术决定论——媒介塑造社会结构",
            ],
            wisdom_laws=[
                "媒介即讯息——媒介的形式比内容更有影响力",
                "媒介即按摩——媒介不仅传递信息，还『按摩』我们的感官",
                "热媒介与冷媒介——高清晰度媒介与低清晰度媒介的差异",
                "地球村——电子媒介使世界变小，形成全球社区",
            ],
            domain_strength={
                CommunicationDomain.MEDIA_THEORY: 10,
                CommunicationDomain.PUBLIC_OPINION: 7,
                CommunicationDomain.MESSAGE_DESIGN: 8,
                CommunicationDomain.CRISIS_COMMUNICATION: 7,
                CommunicationDomain.INTERPERSONAL: 6,
                CommunicationDomain.ORGANIZATIONAL: 6,
            },
        )

        # 让·鲍德里亚 (Jean Baudrillard)
        self._sages["鲍德里亚"] = CommunicationSageProfile(
            name="鲍德里亚",
            era="20世纪后半叶",
            nationality="法国",
            core_theories=[
                "拟象理论",
                "超现实",
                "消费社会",
                "内爆",
                "仿真",
            ],
            methodology=[
                "符号学分析——符号如何建构意义",
                "拟象分析——模拟如何取代现实",
                "消费批判——消费社会的符号逻辑",
            ],
            wisdom_laws=[
                "拟象比现实更真实——符号建构的『超现实』成为主导",
                "消费社会是符号社会——消费的是意义而非物品本身",
                "内爆消解差异——媒介使不同领域融合，边界消失",
                "仿真替代现实——模拟成为真实的替代品",
            ],
            domain_strength={
                CommunicationDomain.MEDIA_THEORY: 10,
                CommunicationDomain.PUBLIC_OPINION: 9,
                CommunicationDomain.MESSAGE_DESIGN: 8,
                CommunicationDomain.CRISIS_COMMUNICATION: 8,
                CommunicationDomain.INTERPERSONAL: 5,
                CommunicationDomain.ORGANIZATIONAL: 6,
            },
        )

        # 尤尔根·哈贝马斯 (Jürgen Habermas)
        self._sages["哈贝马斯"] = CommunicationSageProfile(
            name="哈贝马斯",
            era="20世纪后半叶至今",
            nationality="德国",
            core_theories=[
                "公共领域",
                "交往理性",
                "话语伦理学",
                "生活世界与系统",
                "批判理论",
            ],
            methodology=[
                "话语分析——通过理性对话达成共识",
                "公共领域分析——公民自由讨论的空间",
                "交往行为理论——理解与共识的达成机制",
            ],
            wisdom_laws=[
                "公共领域是民主的基础——公民自由讨论形成公共意见",
                "交往理性追求共识——通过平等对话达成相互理解",
                "话语伦理强调程序正义——正确话语程序比结果更重要",
                "生活世界与系统的张力——系统殖民化威胁生活世界",
            ],
            domain_strength={
                CommunicationDomain.MEDIA_THEORY: 7,
                CommunicationDomain.PUBLIC_OPINION: 10,
                CommunicationDomain.MESSAGE_DESIGN: 9,
                CommunicationDomain.CRISIS_COMMUNICATION: 9,
                CommunicationDomain.INTERPERSONAL: 10,
                CommunicationDomain.ORGANIZATIONAL: 10,
            },
        )

    def get_communication_wisdom(self, problem: str, context: Optional[Dict[str, Any]] = None) -> CommunicationWisdomResult:
        """
        获取传播学智慧

        Args:
            problem: 待解决的传播问题
            context: 上下文

        Returns:
            传播学智慧分析结果
        """
        context = context or {}

        # 分析问题领域
        domain = self._classify_problem_domain(problem)

        # 选择最合适的贤者
        sage_name = self._select_best_sage(domain)
        sage = self._sages[sage_name]

        return CommunicationWisdomResult(
            sage_name=sage_name,
            problem=problem,
            media_analysis=self._analyze_media(problem, sage),
            message_strategy=self._design_message_strategy(problem, sage),
            audience_insight=self._analyze_audience(problem, sage),
            recommendations=self._generate_recommendations(sage, domain),
            confidence=0.85,
        )

    def query_communication_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询传播学智慧"""
        result = self.get_communication_wisdom(problem)
        return [{
            "sage": result.sage_name,
            "media_analysis": result.media_analysis,
            "message_strategy": result.message_strategy,
            "audience_insight": result.audience_insight,
            "recommendations": result.recommendations,
        }]

    def get_media_theory_analysis(self, media_type: str) -> Dict[str, str]:
        """获取媒介理论分析"""
        return {
            "麦克卢汉视角": "媒介的形式比内容更重要——不同的媒介形式塑造不同的感知模式",
            "鲍德里亚视角": "当代媒介创造超现实——拟象比真实更有影响力",
            "哈贝马斯视角": "媒介应服务于公共领域的建设——促进理性讨论",
        }

    def get_public_opinion_insight(self, opinion_type: str) -> str:
        """获取舆论洞察"""
        return "哈贝马斯的公共领域理论：健康的公共舆论形成于自由、开放的讨论空间。舆论领袖、议程设置、框架效应都会影响舆论形成过程。"

    def get_message_design_guidance(self, guidance_type: str) -> str:
        """获取信息设计指导"""
        return "有效的传播信息设计需要考虑：受众特征、媒介特性、信息框架。麦克卢汉提醒我们：媒介形式本身就是一种信息，选择正确的媒介与设计正确的内容同样重要。"

    def _classify_problem_domain(self, problem: str) -> CommunicationDomain:
        """分类问题领域"""
        if any(k in problem for k in ["媒介", "媒体", "渠道", "平台", "形式"]):
            return CommunicationDomain.MEDIA_THEORY
        elif any(k in problem for k in ["舆论", "公众", "意见", "观点", "态度"]):
            return CommunicationDomain.PUBLIC_OPINION
        elif any(k in problem for k in ["信息", "内容", "文案", "故事", "叙事"]):
            return CommunicationDomain.MESSAGE_DESIGN
        elif any(k in problem for k in ["危机", "公关", "应对", "突发", "紧急"]):
            return CommunicationDomain.CRISIS_COMMUNICATION
        elif any(k in problem for k in ["人际", "对话", "沟通", "交流", "谈话"]):
            return CommunicationDomain.INTERPERSONAL
        elif any(k in problem for k in ["组织", "企业", "内部", "员工", "管理"]):
            return CommunicationDomain.ORGANIZATIONAL
        return CommunicationDomain.MESSAGE_DESIGN

    def _analyze_media(self, problem: str, sage: CommunicationSageProfile) -> str:
        """分析媒介"""
        return "麦克卢汉的媒介即讯息理论：媒介形式本身塑造接收者的感知方式，而不仅仅是传递内容。选择正确的媒介是成功传播的第一步。"

    def _design_message_strategy(self, problem: str, sage: CommunicationSageProfile) -> List[str]:
        """设计信息策略"""
        return [
            "明确核心信息：单一、清晰、可记忆",
            "选择合适框架：收益框架vs损失框架，根据情境选择",
            "考虑媒介特性：不同媒介适合不同类型的信息",
            "受众画像分析：理解目标受众的信息处理模式",
        ]

    def _analyze_audience(self, problem: str, sage: CommunicationSageProfile) -> Dict[str, str]:
        """分析受众"""
        return {
            "认知特点": "受众使用启发式快速处理信息",
            "社会影响": "社会认同和权威原则影响接受度",
            "情感因素": "情感诉求与理性诉求的平衡",
        }

    def _select_best_sage(self, domain: CommunicationDomain) -> str:
        """选择最合适的传播学家"""
        scores = {name: sage.domain_strength.get(domain, 5) for name, sage in self._sages.items()}
        return max(scores, key=scores.get)

    def _generate_recommendations(self, sage: CommunicationSageProfile, domain: CommunicationDomain) -> List[str]:
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
_ENGINE: Optional[CommunicationWisdomCore] = None


def get_communication_wisdom(problem: str, context: Optional[Dict[str, Any]] = None) -> CommunicationWisdomResult:
    """获取传播学智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = CommunicationWisdomCore()
    return _ENGINE.get_communication_wisdom(problem, context)


def query_communication_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询传播学智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = CommunicationWisdomCore()
    return _ENGINE.query_communication_by_problem(problem)


def get_media_theory_analysis(media_type: str) -> Dict[str, str]:
    """获取媒介理论分析"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = CommunicationWisdomCore()
    return _ENGINE.get_media_theory_analysis(media_type)


def get_public_opinion_insight(opinion_type: str) -> str:
    """获取舆论洞察"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = CommunicationWisdomCore()
    return _ENGINE.get_public_opinion_insight(opinion_type)


def get_message_design_guidance(guidance_type: str) -> str:
    """获取信息设计指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = CommunicationWisdomCore()
    return _ENGINE.get_message_design_guidance(guidance_type)
