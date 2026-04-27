# -*- coding: utf-8 -*-
"""
儒家智慧fusion核心 v1.0.0
========================

整合儒家十经智慧的unified入口

整合模块:
- RuWisdomCore - 儒家智慧核心
- SelfCultivationSystem - 修身齐家系统
- ZhongYongEngine - 中庸decision引擎
- WuchangEthicsEvaluator - 五常伦理评估器
- DeZhiPlanner - 德治战略规划器
- YiChangeManager - 易变风险管理器

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional

from .ru_wisdom_core import (
    RuWisdomCore,
    ConfucianClassic,
    FiveChang,
    GreatLearning,
    ConfucianDecision,
    ConfucianPersona,
    get_ru_core
)

from .self_cultivation_system import (
    SelfCultivationSystem,
    CultivationLevel,
    CultivationStep,
    CultivationProgress,
    get_cultivation_system
)

from .zhongyong_engine import (
    ZhongYongEngine,
    BalanceState,
    ExtremeType,
    ZhongYongDecision,
    get_zhongyong_engine
)

from .wuchang_ethics import (
    WuchangEthicsEvaluator,
    WuchangAssessment,
    get_wuchang_evaluator
)

from .de_zhi_planner import (
    DeZhiPlanner,
    GovernanceLevel,
    StrategyType,
    DeZhiStrategy,
    get_de_zhi_planner
)

from .yi_change_manager import (
    YiChangeManager,
    YinYang,
    ChangePhase,
    YiRiskAssessment,
    get_yi_change_manager
)

class UnifiedConfucianWisdom:
    """
    儒家智慧unified入口

    ┌─────────────────────────────────────────────────────────────┐
    │                    儒家智慧fusion体系 v1.0.0                    │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │   ┌─────────────────────────────────────────────────────┐   │
    │   │              儒学十经智慧核心                          │   │
    │   │  论语·孟子·大学·中庸·尚书·诗经·礼记·易经·孝经·春秋   │   │
    │   └─────────────────────────────────────────────────────┘   │
    │                           ↓                               │
    │   ┌────────────┬────────────┬────────────┬────────────┐    │
    │   │ 修身系统   │ 中庸引擎   │ 五常评估   │ 德治规划   │    │
    │   │ 大学八条   │ 不偏不倚   │ 仁义礼智信 │ 任贤明德   │    │
    │   └────────────┴────────────┴────────────┴────────────┘    │
    │                           ↓                               │
    │              ┌─────────────────────┐                      │
    │              │   易变风险管理器     │                      │
    │              │  穷则变·通则久     │                      │
    │              └─────────────────────┘                      │
    │                           ↓                               │
    │   ┌─────────────────────────────────────────────────────┐   │
    │   │              decision输出:德才兼备·中庸之道              │   │
    │   └─────────────────────────────────────────────────────┘   │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    核心功能:
    - comprehensive_assessment() - synthesize儒学评估
    - make_integrated_decision() - 整合decision
    - get_confucian_guidance() - get儒学指导
    """

    def __init__(self):
        """init儒家智慧fusion系统"""
        self.name = "UnifiedConfucianWisdom"
        self.version = "v1.0.0"

        # init各子系统
        self.ru_core = get_ru_core()
        self.cultivation_system = get_cultivation_system()
        self.zhongyong_engine = get_zhongyong_engine()
        self.wuchang_evaluator = get_wuchang_evaluator()
        self.de_zhi_planner = get_de_zhi_planner()
        self.yi_change_manager = get_yi_change_manager()

        # 整合的经典语录
        self.classic_quotes = {
            "论语": "己所不欲,勿施于人.",
            "孟子": "民为贵,社稷次之,君为轻.",
            "大学": "大学之道,在明明德,在亲民,在止于至善.",
            "中庸": "极高明而道中庸.",
            "尚书": "皇天无亲,唯德是辅.",
            "诗经": "关关雎鸠,在河之洲.",
            "礼记": "礼之用,和为贵.",
            "易经": "穷则变,变则通,通则久.",
            "孝经": "夫孝,德之本也.",
            "春秋": "名不正则言不顺,言不顺则事不成."
        }

    def comprehensive_assessment(self, subject: Dict) -> Dict[str, Any]:
        """
        synthesize儒学评估

        Args:
            subject: 评估对象,包含:
                - type: 类型 (person/action/organization)
                - data: 相关数据

        Returns:
            synthesize儒学评估结果
        """
        subject_type = subject.get("type", "action")
        data = subject.get("data", {})

        # 儒家核心评估
        ru_assessment = self.ru_core.assess_situation(data)

        # 五常伦理评估
        if subject_type == "person":
            wuchang_result = self.wuchang_evaluator.evaluate_person(
                data.get("traits", []),
                data.get("behaviors", [])
            )
        else:
            wuchang_result = self.wuchang_evaluator.evaluate_action(
                str(data)
            )

        # 中庸平衡评估
        zhongyong_result = self.zhongyong_engine.assess_situation_zhongyong(data)

        # 易变风险评估
        if "stability" in data or "momentum" in data:
            yi_result = self.yi_change_manager.assess_risk(data)
        else:
            yi_result = None

        # synthesize评分
        overall_score = self._calculate_overall_score(
            ru_assessment, wuchang_result, zhongyong_result
        )

        return {
            "subject_type": subject_type,
            "ru_assessment": ru_assessment,
            "wuchang_assessment": wuchang_result,
            "zhongyong_assessment": zhongyong_result,
            "yi_assessment": yi_result,
            "overall_score": overall_score,
            "classic_recommendation": self._get_recommendation(overall_score),
            "quotes": self._get_relevant_quotes(ru_assessment)
        }

    def _calculate_overall_score(self, ru: Dict, wuchang: Any,
                                  zhongyong: Dict) -> float:
        """计算synthesize评分"""
        ru_score = ru.get("overall_score", 0.7)
        wuchang_score = wuchang.total_score if hasattr(wuchang, 'total_score') else 0.7
        zhongyong_score = zhongyong.get("score", 0.5)

        return (ru_score * 0.4 + wuchang_score * 0.35 + zhongyong_score * 0.25)

    def _get_recommendation(self, score: float) -> str:
        """get推荐"""
        if score >= 0.85:
            return "上上之选:德才兼备,儒学典范,宜大力推广"
        elif score >= 0.75:
            return "上等之选:道德优良,可堪大任"
        elif score >= 0.6:
            return "中等之选:基本合格,需要加强修养"
        elif score >= 0.45:
            return "下等之选:有所不足,需要改进提升"
        else:
            return "不及格:背离儒学之道,需要深刻反省"

    def _get_relevant_quotes(self, ru_assessment: Dict) -> List[str]:
        """get相关语录"""
        quotes = []
        if "lunyu_perspective" in ru_assessment:
            quotes.append(ru_assessment["lunyu_perspective"].get("quote", ""))

        quotes.append(self.classic_quotes["论语"])

        return list(set(quotes))[:3]

    def make_integrated_decision(self, decision_context: Dict) -> Dict[str, Any]:
        """
        整合儒学decision

        Args:
            decision_context: decision上下文

        Returns:
            整合decision结果
        """
        # 儒家decision
        ru_decision = self.ru_core.make_decision(decision_context)

        # 中庸平衡评估
        options = decision_context.get("options", [])
        zhongyong_decision = self.zhongyong_engine.evaluate_balance(options)

        # 五常伦理评估
        action = decision_context.get("action", "")
        wuchang_result = self.wuchang_evaluator.evaluate_action(action)

        # 德治战略(如适用)
        if decision_context.get("type") == "strategy":
            de_strategy = self.de_zhi_planner.plan_strategy(
                decision_context,
                decision_context.get("goal", "")
            )
        else:
            de_strategy = None

        # synthesizejudge
        final_recommendation = self._synthesize_decision(
            ru_decision, zhongyong_decision, wuchang_result
        )

        return {
            "ru_decision": {
                "principle": ru_decision.primary_principle,
                "action": ru_decision.action,
                "quote": ru_decision.wisdom_source
            },
            "zhongyong_decision": {
                "balance_score": zhongyong_decision.balance_score,
                "state": zhongyong_decision.balance_state.value,
                "recommendation": zhongyong_decision.recommendation
            },
            "wuchang_assessment": {
                "total_score": wuchang_result.total_score,
                "primary_strength": wuchang_result.primary_strength,
                "overall_judgment": wuchang_result.overall_judgment
            },
            "de_strategy": de_strategy,
            "final_recommendation": final_recommendation
        }

    def _synthesize_decision(self, ru: Any, zhongyong: Any,
                              wuchang: Any) -> str:
        """synthesize_decision建议"""
        recommendations = []

        # 儒家建议
        recommendations.append(ru.action)

        # 中庸建议
        if zhongyong.balance_score >= 0.7:
            recommendations.append(zhongyong.recommendation)

        # 五常建议
        if wuchang.total_score >= 0.7:
            recommendations.append("符合五常伦理")

        return ";".join(recommendations)

    def get_confucian_guidance(self, context_type: str) -> Dict[str, Any]:
        """
        get儒学指导

        Args:
            context_type: 指导类型 (cultivation/decision/ethics/strategy)

        Returns:
            儒学指导
        """
        if context_type == "cultivation":
            return self.cultivation_system.get_guidance()

        elif context_type == "decision":
            return {
                "quote": self.classic_quotes["中庸"],
                "advice": "执其两端,用其中于民",
                "principles": {
                    "仁": "仁者爱人",
                    "义": "义者宜也",
                    "礼": "礼者理也",
                    "智": "智者知也",
                    "信": "信者诚也"
                }
            }

        elif context_type == "ethics":
            return self.wuchang_evaluator.get_wuchang_wisdom()

        elif context_type == "strategy":
            return {
                "quote": self.classic_quotes["尚书"],
                "advice": "皇天无亲,唯德是辅",
                "strategies": {
                    "任贤": "任官惟贤材",
                    "明德": "黾勉求之",
                    "惠民": "民之所欲",
                    "修身": "正人正己"
                }
            }

        else:
            return {
                "quote": self.classic_quotes["论语"],
                "advice": "学而时习之,不亦说乎"
            }

    def get_system_info(self) -> Dict[str, Any]:
        """get系统信息"""
        return {
            "name": self.name,
            "version": self.version,
            "sub_systems": [
                "RuWisdomCore (儒家智慧核心)",
                "SelfCultivationSystem (修身齐家)",
                "ZhongYongEngine (中庸decision)",
                "WuchangEthicsEvaluator (五常伦理)",
                "DeZhiPlanner (德治战略)",
                "YiChangeManager (易变风险)"
            ],
            "supported_classics": list(self.classic_quotes.keys()),
            "quote": "儒学十经,道统传承."
        }

# 全局实例
_unified_confucian_wisdom: Optional[UnifiedConfucianWisdom] = None

def get_unified_confucian_wisdom() -> UnifiedConfucianWisdom:
    """get儒家智慧fusionsystem_instance"""
    global _unified_confucian_wisdom
    if _unified_confucian_wisdom is None:
        _unified_confucian_wisdom = UnifiedConfucianWisdom()
    return _unified_confucian_wisdom

# 导出
__all__ = [
    # 子系统
    'RuWisdomCore',
    'SelfCultivationSystem',
    'ZhongYongEngine',
    'WuchangEthicsEvaluator',
    'DeZhiPlanner',
    'YiChangeManager',
    'UnifiedConfucianWisdom',
    # 枚举
    'ConfucianClassic',
    'FiveChang',
    'GreatLearning',
    'CultivationLevel',
    'CultivationStep',
    'BalanceState',
    'ExtremeType',
    'GovernanceLevel',
    'StrategyType',
    'YinYang',
    'ChangePhase',
    # get函数
    'get_ru_core',
    'get_cultivation_system',
    'get_zhongyong_engine',
    'get_wuchang_evaluator',
    'get_de_zhi_planner',
    'get_yi_change_manager',
    'get_unified_confucian_wisdom'
]
