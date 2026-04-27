"""
__all__ = [
    'ComplexityWisdomEngine',
]

复杂性科学智慧引擎 v1.0
Complexity Science School Wisdom Engine V1.0

复杂性科学（圣塔菲研究所、复杂适应系统）的智慧集成。

版本: v1.0
创建: 2026-04-23
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ComplexityDomain(Enum):
    """复杂性科学应用领域"""
    EMERGENT_ORDER = "涌现秩序"              # 简单规则产生复杂行为
    NETWORK_DYNAMICS = "网络动力学"         # 网络结构与动态演化
    ADAPTIVE_SYSTEM = "自适应系统"           # 系统适应与进化
    COMPLEXITY_THEORY = "复杂性理论"         # 复杂系统的基本规律
    SELF_ORGANIZATION = "自组织理论"         # 系统自组织演化


@dataclass
class ComplexityWisdomResult:
    """复杂性科学智慧分析结果"""
    problem_type: str
    analysis: str
    complexity_insight: str
    system_dynamics: str
    recommendations: List[str]
    confidence: float


class ComplexityWisdomCore:
    """
    复杂性科学智慧核心

    整合圣塔菲研究所Murray Gell-Mann、Stuart Kauffman等复杂性科学家的智慧。
    """

    def __init__(self):
        self._principles = self._initialize_principles()

    def _initialize_principles(self) -> Dict[str, Dict[str, Any]]:
        """初始化复杂性科学原则"""
        return {
            "emergence": {
                "name": "涌现",
                "sage": "Murray Gell-Mann",
                "core_text": "复杂系统的整体行为不能简单地从部件行为预测",
                "explanation": "简单规则的局部交互产生意想不到的全局模式",
                "application": "识别涌现信号、理解系统层级、在涌现中寻找机会"
            },
            "adaptation": {
                "name": "适应性",
                "sage": "Stuart Kauffman",
                "core_text": "复杂系统在秩序与混沌的边缘运行最佳",
                "explanation": "系统需要足够的连接以产生复杂性，但不要太连接以至于锁定",
                "application": "在稳定与创新间保持平衡、避免过度优化、保持系统弹性"
            },
            "networks": {
                "name": "网络结构",
                "sage": "Duncan Watts / Steven Strogatz",
                "core_text": "小世界网络和无尺度网络是复杂系统的常见结构",
                "explanation": "网络的拓扑结构决定了信息传播和系统响应的方式",
                "application": "优化网络结构以提高鲁棒性和效率、理解信息传播路径"
            },
            "self_organization": {
                "name": "自组织",
                "sage": "Ilya Prigogine",
                "core_text": "开放系统可以通过自组织达到更高的有序状态",
                "explanation": "远离平衡态的系统可以通过能量耗散形成有序结构",
                "application": "创造系统自组织的条件、利用正负反馈机制"
            },
            "sensitivity": {
                "name": "初始条件敏感",
                "sage": "Edward Lorenz",
                "core_text": "对初始条件的敏感依赖（蝴蝶效应）",
                "explanation": "微小的变化可以导致巨大的差异（混沌）",
                "application": "关注初始条件的微小变化、承认预测的有限性"
            },
            "fitness_landscape": {
                "name": "适应度景观",
                "sage": "Stuart Kauffman",
                "core_text": "适应度景观的崎岖性决定了进化的路径",
                "explanation": "系统可能被困在局部最优，需要随机性来探索全局最优",
                "application": "引入随机性跳出局部最优、构建更平滑的适应度景观"
            }
        }

    def get_wisdom(self, principle_name: str) -> Optional[Dict[str, Any]]:
        """获取复杂性科学智慧"""
        return self._principles.get(principle_name)

    def analyze_emergent_order(self, problem: str, context: Optional[Dict[str, Any]] = None) -> ComplexityWisdomResult:
        """分析涌现秩序"""
        insight = self._principles["emergence"]
        return ComplexityWisdomResult(
            problem_type="EMERGENT_ORDER",
            analysis="涌现是复杂性系统的核心特征——整体大于部分之和",
            complexity_insight=insight["explanation"],
            system_dynamics="局部交互→信息传递→模式形成→涌现出现",
            recommendations=[
                "从局部规则推演可能的涌现模式",
                "设计促进有益涌现的激励机制",
                "监控涌现信号，早期识别系统演化方向"
            ],
            confidence=0.86
        )

    def analyze_network_dynamics(self, problem: str, context: Optional[Dict[str, Any]] = None) -> ComplexityWisdomResult:
        """分析网络动力学"""
        insight = self._principles["networks"]
        return ComplexityWisdomResult(
            problem_type="NETWORK_DYNAMICS",
            analysis="网络结构决定了系统功能的边界和可能性",
            complexity_insight=insight["explanation"],
            system_dynamics="节点连接→网络形成→信息/影响传播→网络效应",
            recommendations=[
                "识别系统中的关键节点和桥梁",
                "理解信息在网络中的传播路径",
                "利用网络效应放大系统功能"
            ],
            confidence=0.84
        )

    def analyze_adaptive_evolution(self, problem: str, context: Optional[Dict[str, Any]] = None) -> ComplexityWisdomResult:
        """分析自适应演化"""
        insights = [self._principles["adaptation"], self._principles["fitness_landscape"]]
        return ComplexityWisdomResult(
            problem_type="ADAPTIVE_EVOLUTION",
            analysis="系统在秩序与混沌边缘具有最大的适应性和创新能力",
            complexity_insight=insights[0]["explanation"],
            system_dynamics="探索→选择→适应→再探索的循环演化",
            recommendations=[
                "保持系统在稳定与变化之间的张力",
                "引入适度随机性以探索新可能性",
                "构建反馈机制加速系统适应"
            ],
            confidence=0.85
        )

    def get_all_wisdoms(self) -> List[Dict[str, Any]]:
        """获取所有复杂性科学智慧"""
        return list(self._principles.values())


class ComplexityWisdomEngine:
    """
    复杂性科学智慧引擎主类

    提供复杂性科学视角的决策支持。
    """

    def __init__(self):
        self.core = ComplexityWisdomCore()

    def get_wisdom(self, principle_name: str) -> Optional[Dict[str, Any]]:
        """获取复杂性科学智慧"""
        return self.core.get_wisdom(principle_name)

    def solve(self, problem_type: str, context: Optional[Dict[str, Any]] = None) -> ComplexityWisdomResult:
        """
        根据问题类型解决复杂性科学问题

        Args:
            problem_type: 问题类型（EMERGENT_ORDER/NETWORK_DYNAMICS等）
            context: 上下文信息

        Returns:
            复杂性科学智慧分析结果
        """
        context = context or {}
        problem = context.get("problem", "")

        if problem_type == "EMERGENT_ORDER":
            return self.core.analyze_emergent_order(problem, context)
        elif problem_type == "NETWORK_DYNAMICS":
            return self.core.analyze_network_dynamics(problem, context)
        elif problem_type == "ADAPTIVE_EVOLUTION":
            return self.core.analyze_adaptive_evolution(problem, context)
        else:
            return ComplexityWisdomResult(
                problem_type=problem_type,
                analysis="复杂性科学视角分析",
                complexity_insight="复杂系统的行为不能简单地从部件行为预测",
                system_dynamics="局部→全局→反馈→演化",
                recommendations=["识别系统层级", "关注涌现信号", "保持适应性"],
                confidence=0.70
            )

    def get_all_wisdoms(self) -> List[Dict[str, Any]]:
        """获取所有复杂性科学智慧"""
        return self.core.get_all_wisdoms()
