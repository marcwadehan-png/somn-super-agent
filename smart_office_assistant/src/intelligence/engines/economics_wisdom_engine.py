"""
__all__ = [
    'EconomicsWisdomEngine',
]

经济学智慧引擎 v1.0
Economics School Wisdom Engine V1.0

提供经济学智慧的决策支持，整合古典经济学与现代经济学思想。

版本: v1.0
创建: 2026-04-23
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class EconomicsDomain(Enum):
    """经济学应用领域"""
    RESOURCE_ALLOCATION = "资源配置"          # 稀缺资源的最优配置
    SUPPLY_DEMAND = "供需分析"                 # 供给需求平衡
    INCENTIVE_DESIGN = "激励机制"              # 经济激励设计
    MARKET_ANALYSIS = "市场分析"               # 市场效率与竞争
    INVESTMENT = "投资决策"                    # 投资分析与风险管理


@dataclass
class EconomicsWisdomResult:
    """经济学智慧分析结果"""
    problem_type: str
    analysis: str
    recommendations: List[str]
    economic_insight: str
    confidence: float


class EconomicsWisdomCore:
    """
    经济学智慧核心

    整合亚当·斯密、凯恩斯、马歇尔等经济学大师的智慧。
    """

    def __init__(self):
        self._principles = self._initialize_principles()

    def _initialize_principles(self) -> Dict[str, Dict[str, Any]]:
        """初始化经济学原则"""
        return {
            "invisible_hand": {
                "name": "看不见的手",
                "sage": "亚当·斯密",
                "core_text": "个人追求私利时，在适当制度下可促进社会利益",
                "explanation": "自由市场在价格机制引导下自动配置资源",
                "application": "减少不必要的政府干预，让市场机制发挥作用"
            },
            "demand_supply": {
                "name": "供需定律",
                "sage": "阿尔弗雷德·马歇尔",
                "core_text": "价格由供需关系决定",
                "explanation": "需求随价格下降而增加，供给随价格上升而增加",
                "application": "定价策略、市场预测、资源配置"
            },
            "marginal_utility": {
                "name": "边际效用",
                "sage": "威廉·斯坦利·杰文斯",
                "core_text": "理性人比较边际成本与边际收益做决策",
                "explanation": "最后一单位消费带来的满足感决定价值",
                "application": "最优产量决策、消费组合优化"
            },
            "keynesian_multiplier": {
                "name": "乘数效应",
                "sage": "约翰·梅纳德·凯恩斯",
                "core_text": "政府支出可产生数倍于自身的经济增长",
                "explanation": "初始支出引发连锁消费反应，放大经济效果",
                "application": "财政政策、刺激经济增长"
            },
            "opportunity_cost": {
                "name": "机会成本",
                "sage": "弗里德里希·冯·维塞尔",
                "core_text": "选择某一方案而放弃的最佳替代方案价值",
                "explanation": "资源有限，必须权衡取舍",
                "application": "投资决策、资源分配、项目评估"
            },
            "comparative_advantage": {
                "name": "比较优势",
                "sage": "大卫·李嘉图",
                "core_text": "各国应专业化生产具有比较优势的产品",
                "explanation": "即使一国在所有产品上都不占优势，专业化仍有收益",
                "application": "国际贸易、区域分工、企业战略"
            },
            "time_preference": {
                "name": "时间偏好",
                "sage": "欧根·冯·庞巴维克",
                "core_text": "人们普遍偏好现在而非未来",
                "explanation": "未来收益需要贴现，贴现率反映时间偏好",
                "application": "利率理论、投资回报要求、储蓄决策"
            },
        }

    def get_wisdom(self, principle_name: str) -> Optional[Dict[str, Any]]:
        """获取经济学智慧原则"""
        return self._principles.get(principle_name)

    def analyze_resource_allocation(self, context: Dict[str, Any]) -> EconomicsWisdomResult:
        """分析资源配置问题"""
        insight = self._principles["invisible_hand"]
        return EconomicsWisdomResult(
            problem_type="RESOURCE_ALLOCATION",
            analysis="稀缺资源应通过价格机制引导配置",
            recommendations=[
                "建立清晰的价格信号",
                "减少配置中的行政干预",
                "允许资源向高效领域流动"
            ],
            economic_insight=insight["explanation"],
            confidence=0.85
        )

    def analyze_supply_demand(self, context: Dict[str, Any]) -> EconomicsWisdomResult:
        """分析供需平衡问题"""
        insight = self._principles["demand_supply"]
        return EconomicsWisdomResult(
            problem_type="SUPPLY_DEMAND_BALANCE",
            analysis="供需平衡是市场稳定的基础",
            recommendations=[
                "识别供需弹性差异",
                "关注边际变化而非总量",
                "预判价格调整的连锁反应"
            ],
            economic_insight=insight["explanation"],
            confidence=0.88
        )

    def analyze_incentive(self, context: Dict[str, Any]) -> EconomicsWisdomResult:
        """分析激励机制设计"""
        insight = self._principles["marginal_utility"]
        return EconomicsWisdomResult(
            problem_type="ECONOMIC_INCENTIVE",
            analysis="激励机制设计需考虑边际效应",
            recommendations=[
                "设计激励时关注边际成本收益",
                "避免激励扭曲和道德风险",
                "保持激励的一致性和可预期性"
            ],
            economic_insight=insight["explanation"],
            confidence=0.82
        )

    def analyze_market_efficiency(self, context: Dict[str, Any]) -> EconomicsWisdomResult:
        """分析市场效率"""
        insights = [self._principles["invisible_hand"], self._principles["comparative_advantage"]]
        return EconomicsWisdomResult(
            problem_type="MARKET_EFFICIENCY",
            analysis="市场效率取决于竞争程度和信息充分性",
            recommendations=[
                "促进公平竞争",
                "提高信息透明度",
                "减少不必要的进入壁垒"
            ],
            economic_insight="比较优势理论解释了分工如何提升整体效率",
            confidence=0.84
        )

    def analyze_investment(self, context: Dict[str, Any]) -> EconomicsWisdomResult:
        """分析投资决策"""
        insights = [self._principles["opportunity_cost"], self._principles["time_preference"]]
        return EconomicsWisdomResult(
            problem_type="INVESTMENT_DECISION",
            analysis="投资决策需权衡机会成本和时间价值",
            recommendations=[
                "比较投资与最佳替代方案的回报",
                "考虑资金的时间价值和风险溢价",
                "关注边际投资回报而非平均回报"
            ],
            economic_insight="机会成本是理性决策的关键约束",
            confidence=0.86
        )


class EconomicsWisdomEngine:
    """
    经济学智慧引擎主类

    提供完整的经济学智慧决策支持。
    """

    def __init__(self):
        self.core = EconomicsWisdomCore()

    def get_wisdom(self, principle_name: str) -> Optional[Dict[str, Any]]:
        """获取经济学智慧"""
        return self.core.get_wisdom(principle_name)

    def solve(self, problem_type: str, context: Optional[Dict[str, Any]] = None) -> EconomicsWisdomResult:
        """
        根据问题类型解决经济学问题

        Args:
            problem_type: 问题类型（RESOURCE_ALLOCATION/SUPPLY_DEMAND_BALANCE等）
            context: 上下文信息

        Returns:
            经济学智慧分析结果
        """
        context = context or {}

        if problem_type == "RESOURCE_ALLOCATION":
            return self.core.analyze_resource_allocation(context)
        elif problem_type == "SUPPLY_DEMAND_BALANCE":
            return self.core.analyze_supply_demand(context)
        elif problem_type == "ECONOMIC_INCENTIVE":
            return self.core.analyze_incentive(context)
        elif problem_type == "MARKET_EFFICIENCY":
            return self.core.analyze_market_efficiency(context)
        elif problem_type == "INVESTMENT_DECISION":
            return self.core.analyze_investment(context)
        else:
            return EconomicsWisdomResult(
                problem_type=problem_type,
                analysis="经济学视角分析",
                recommendations=["综合考虑成本收益", "权衡长期短期影响"],
                economic_insight="理性决策需要系统经济学分析",
                confidence=0.70
            )

    def get_all_wisdoms(self) -> List[Dict[str, Any]]:
        """获取所有经济学智慧"""
        return list(self.core._principles.values())
