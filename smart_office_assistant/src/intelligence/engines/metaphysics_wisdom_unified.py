# -*- coding: utf-8 -*-
"""
术数时空智慧unified入口 v1.0.0
Metaphysics Wisdom Unified

整合:
- 中国传统术数核心(阴阳,五行,天干,地支,生肖,八字)
- 风水环境认知模块
- 道家阴阳分析能力(作为补充视角)

定位:
把传统术数知识转化成系统可复用的"结构recognize + 时机judge + 环境优化"能力.

版本:v1.0.0
更新:2026-04-02
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .traditional_metaphysics_core import TraditionalMetaphysicsCore, get_traditional_metaphysics_core
from .fengshui_environment_engine import FengShuiEnvironmentEngine, get_fengshui_environment_engine

try:
    from .dao_wisdom_core import DaoWisdomCore
except ImportError:  # pragma: no cover - 降级兼容
    DaoWisdomCore = None  # type: ignore

class MetaphysicsWisdomUnified:
    """术数时空智慧unified入口"""

    def __init__(self):
        self.core = get_traditional_metaphysics_core()
        self.fengshui = get_fengshui_environment_engine()
        self.dao_core = DaoWisdomCore() if DaoWisdomCore else None
        self.name = "MetaphysicsWisdomUnified"
        self.version = "v1.0.0"

    def analyze_comprehensive(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """synthesize分析入口"""
        problem = scenario.get("problem") or scenario.get("topic") or "术数时空synthesize分析"

        element_input = (
            scenario.get("element_weights")
            or scenario.get("factors")
            or scenario.get("keywords")
            or problem
        )
        wuxing = self.core.analyze_wuxing_balance(element_input)

        bazi_result = None
        pillars = scenario.get("pillars") or scenario.get("bazi")
        if isinstance(pillars, dict):
            try:
                bazi_result = self.core.interpret_bazi(pillars)
            except Exception as exc:
                bazi_result = {"error": f"八字结构解析失败:{exc}"}

        zodiac_result = None
        zodiacs = scenario.get("zodiacs") or scenario.get("生肖")
        if isinstance(zodiacs, (list, tuple)):
            zodiac_result = self.core.analyze_zodiac_pattern(zodiacs)

        environment_result = None
        environment = scenario.get("environment") or scenario.get("layout")
        if isinstance(environment, dict):
            business_type = scenario.get("business_type")
            if business_type:
                environment_result = self.fengshui.analyze_business_space(business_type, environment)
            else:
                environment_result = self.fengshui.analyze_layout(environment)

        dao_result = None
        if self.dao_core:
            dao_result = self.dao_core.analyze_yin_yang(
                problem,
                self._derive_yin_yang_factors(problem, scenario),
            )

        synthesis = self._build_synthesis(problem, wuxing, bazi_result, zodiac_result, environment_result, dao_result)
        action_plan = self._build_action_plan(wuxing, bazi_result, environment_result, dao_result)

        return {
            "system": self.name,
            "version": self.version,
            "problem": problem,
            "wuxing_analysis": wuxing,
            "bazi_analysis": bazi_result,
            "zodiac_analysis": zodiac_result,
            "environment_analysis": environment_result,
            "yin_yang_analysis": dao_result,
            "summary": synthesis,
            "recommendation": synthesis,
            "action": synthesis,
            "action_plan": action_plan,
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """协调器通用接口"""
        return self.analyze_comprehensive(input_data)

    def _derive_yin_yang_factors(self, problem: str, scenario: Dict[str, Any]) -> Dict[str, float]:
        explicit = scenario.get("yin_yang_factors")
        if isinstance(explicit, dict) and explicit:
            return {str(key): float(value) for key, value in explicit.items()}

        factors = {
            "增长扩张": 1.0 if any(word in problem for word in ["增长", "扩张", "突破", "加速"]) else 0.0,
            "稳定沉淀": 1.0 if any(word in problem for word in ["稳定", "沉淀", "积累", "守住"]) else 0.0,
            "主动进攻": 1.0 if any(word in problem for word in ["抢占", "进攻", "推进", "竞争"]) else 0.0,
            "回收内控": 1.0 if any(word in problem for word in ["风控", "收缩", "治理", "节流"]) else 0.0,
        }
        return {key: value for key, value in factors.items() if value > 0}

    def _build_synthesis(
        self,
        problem: str,
        wuxing: Dict[str, Any],
        bazi_result: Optional[Dict[str, Any]],
        zodiac_result: Optional[Dict[str, Any]],
        environment_result: Optional[Dict[str, Any]],
        dao_result: Optional[Dict[str, Any]],
    ) -> str:
        parts = [
            f'围绕"{problem}",当前结构主轴落在{wuxing["strongest"]},短板落在{wuxing["weakest"]}.',
            f'五行judge为"{wuxing["state"]}",适合先稳住{wuxing["strongest"]}优势,再针对{wuxing["weakest"]}补位.',
        ]

        if bazi_result and not bazi_result.get("error"):
            insight = bazi_result.get("insight", {})
            parts.append(
                f"八字结构侧显示日主为{insight.get('day_master', '未知')}{insight.get('day_master_element', '')},judge为'{insight.get('strength_state', '中和')}',用神倾向可参考{','.join(insight.get('useful_elements', []))}."
            )
        if zodiac_result:
            parts.append(zodiac_result.get("recommendation", ""))
        if environment_result:
            parts.append(
                f"环境结构评分{environment_result.get('overall_score', 0)},等级为{environment_result.get('grade', '未评估')},优先关注{','.join(environment_result.get('warnings', []))}."
            )
        if dao_result:
            parts.append(f"阴阳层面呈现'{dao_result.get('state', '中和')}',建议:{dao_result.get('advice', '')}")

        return " ".join(part for part in parts if part)

    def _build_action_plan(
        self,
        wuxing: Dict[str, Any],
        bazi_result: Optional[Dict[str, Any]],
        environment_result: Optional[Dict[str, Any]],
        dao_result: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        plan = {
            "主攻轴": f"以{wuxing['strongest']}为当前主攻方向",
            "补位轴": f"以{wuxing['weakest']}为风险补位方向",
            "五行建议": wuxing.get("recommendations", []),
        }

        if bazi_result and not bazi_result.get("error"):
            plan["八字建议"] = bazi_result.get("insight", {}).get("key_suggestions", [])
        if environment_result:
            plan["风水建议"] = environment_result.get("recommendations", [])
        if dao_result:
            plan["阴阳建议"] = [dao_result.get("advice", "")]
        return plan

_default_unified: Optional[MetaphysicsWisdomUnified] = None

def get_metaphysics_wisdom_unified() -> MetaphysicsWisdomUnified:
    """get术数时空智慧unified入口"""
    global _default_unified
    if _default_unified is None:
        _default_unified = MetaphysicsWisdomUnified()
    return _default_unified

def quick_metaphysics_analyze(problem: str, **kwargs: Any) -> Dict[str, Any]:
    """快速分析接口"""
    payload = {"problem": problem, **kwargs}
    return get_metaphysics_wisdom_unified().analyze_comprehensive(payload)

__all__ = [
    "MetaphysicsWisdomUnified",
    "get_metaphysics_wisdom_unified",
    "quick_metaphysics_analyze",
]
