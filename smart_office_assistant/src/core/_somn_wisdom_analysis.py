"""
__all__ = [
    'maybe_run_metaphysics_analysis',
    'run_unified_enhancement',
    'run_wisdom_analysis',
]

SomnCore 智慧层分析模块
智慧分析入口与统一协调器增强逻辑。
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

def run_wisdom_analysis(
    description: str,
    structured_req: Dict[str, Any],
    context: Dict[str, Any],
    ensure_fn,
    super_wisdom,
    global_wisdom,
    thinking_engine,
) -> Dict[str, Any]:
    """
    默认智慧分析:在需求分析阶段自动运行,激活对应智慧学派与思维方法.

    优先链: SuperWisdomCoordinator → GlobalWisdomScheduler → ThinkingMethodEngine
    任一成功即返回,全部失败则返回空壳(不阻断主链).
    """
    empty = {
        "triggered": False,
        "insights": [],
        "activated_schools": [],
        "recommendations": [],
        "thinking_method": "",
        "source": "none",
    }

    query_text = description
    if structured_req.get("objective"):
        query_text = f"{description} {structured_req['objective']}"

    # 1) SuperWisdomCoordinator
    ensure_fn()
    if super_wisdom is not None:
        try:
            result = super_wisdom.analyze(
                query_text=query_text,
                context=context,
                threshold=0.25,
                max_schools=6,
            )
            schools = []
            insights = []
            recommendations = []

            if hasattr(result, "activated_schools"):
                schools = [getattr(s, "name", str(s)) for s in (result.activated_schools or [])]
                primary = getattr(result, "primary_insight", "") or ""
                secondary = list(getattr(result, "secondary_insights", []) or [])
                insights = [primary] + secondary if primary else secondary
                recommendations = list(getattr(result, "action_recommendations", []) or [])
            elif isinstance(result, dict):
                schools = result.get("activated_schools", [])
                insights = [result.get("primary_insight", "")] + result.get("secondary_insights", [])
                recommendations = result.get("action_recommendations", [])

            if schools or insights:
                logger.info(f"[智慧层] SuperWisdomCoordinator 激活学派: {schools[:4]}")
                return {
                    "triggered": True,
                    "insights": insights[:6],
                    "activated_schools": schools[:8],
                    "recommendations": recommendations[:4],
                    "thinking_method": getattr(result, "thinking_method", "") if hasattr(result, "thinking_method") else "",
                    "source": "super_wisdom_coordinator",
                }
        except Exception as e:
            logger.warning(f"[智慧层] SuperWisdomCoordinator 调用失败: {e}")

    # 2) GlobalWisdomScheduler
    if global_wisdom is not None:
        try:
            from ..intelligence.global_wisdom_scheduler import WisdomQuery
            query = WisdomQuery(text=query_text, context=context, threshold=0.25, max_schools=5)
            result = global_wisdom.schedule(query)

            schools = []
            insights = []
            if hasattr(result, "school_results"):
                schools = [getattr(sr, "school_name", "") for sr in (result.school_results or [])]
                for sr in (result.school_results or []):
                    insight = getattr(sr, "insight", "") or getattr(sr, "summary", "")
                    if insight:
                        insights.append(insight)
            elif isinstance(result, dict):
                schools = result.get("schools", [])
                insights = result.get("insights", [])

            if schools or insights:
                logger.info(f"[智慧层] GlobalWisdomScheduler 激活学派: {schools[:4]}")
                return {
                    "triggered": True,
                    "insights": insights[:6],
                    "activated_schools": schools[:8],
                    "recommendations": [],
                    "thinking_method": "",
                    "source": "global_wisdom_scheduler",
                }
        except Exception as e:
            logger.warning(f"[智慧层] GlobalWisdomScheduler 调用失败: {e}")

    # 3) ThinkingMethodEngine
    if thinking_engine is not None:
        try:
            result = None
            for method in ["analyze", "think", "process"]:
                if hasattr(thinking_engine, method):
                    result = getattr(thinking_engine, method)(query_text)
                    break

            if result:
                insights = []
                method_name = ""
                if isinstance(result, dict):
                    insights = result.get("insights", result.get("conclusions", []))
                    method_name = result.get("method", "")
                elif hasattr(result, "insights"):
                    insights = list(result.insights or [])
                    method_name = getattr(result, "method", "")

                if insights:
                    logger.info(f"[智慧层] ThinkingMethodEngine 已激活,方法: {method_name}")
                    return {
                        "triggered": True,
                        "insights": insights[:4],
                        "activated_schools": [],
                        "recommendations": [],
                        "thinking_method": method_name,
                        "source": "thinking_method_engine",
                    }
        except Exception as e:
            logger.warning(f"[智慧层] ThinkingMethodEngine 调用失败: {e}")

    return empty

def run_unified_enhancement(
    requirement_doc: Dict[str, Any],
    strategy_context: Dict[str, Any],
    ensure_fn,
    unified_coordinator,
) -> Dict[str, Any]:
    """
    unified智慧协同增强:在strategy设计阶段对需求做多模块 ensemble 分析.

    使用 UnifiedIntelligenceCoordinator 的 ensemble strategy激活所有适配学派,
    把协同洞察注入strategy上下文,丰富strategy建议质量.
    """
    empty = {"triggered": False, "modules_activated": [], "enhancement_insights": [], "source": "none"}

    ensure_fn()
    if unified_coordinator is None:
        return empty

    try:
        from ..intelligence.unified_intelligence_coordinator import TaskType, TaskContext

        task_type_str = requirement_doc.get("structured_requirement", {}).get("task_type", "general_analysis")
        type_mapping = {
            "growth_analysis": TaskType.GROWTH_PLANNING,
            "strategy": TaskType.STRATEGIC_DECISION,
            "strategy_planning": TaskType.STRATEGIC_DECISION,
            "creative": TaskType.TACTICAL_EXECUTION,
            "creative_thinking": TaskType.TACTICAL_EXECUTION,
            "problem_solving": TaskType.PROBLEM_SOLVING,
            "risk": TaskType.RISK_ASSESSMENT,
            "risk_assessment": TaskType.RISK_ASSESSMENT,
            "general_analysis": TaskType.STRATEGIC_DECISION,
        }
        task_type = type_mapping.get(task_type_str, TaskType.STRATEGY_PLANNING)

        input_data = {
            "description": requirement_doc.get("raw_description", ""),
            "objective": requirement_doc.get("structured_requirement", {}).get("objective", ""),
            "industry": requirement_doc.get("industry", "general"),
            "metrics": requirement_doc.get("structured_requirement", {}).get("metrics", {}),
            "strategy_context": strategy_context,
        }

        ctx = TaskContext(
            session_id=requirement_doc.get("task_id", ""),
            user_intent=requirement_doc.get("raw_description", ""),
            domain=requirement_doc.get("industry", "general"),
        )

        result = unified_coordinator.execute_task(task_type, input_data, ctx)

        modules = []
        insights = []
        if hasattr(result, "modules_used"):
            modules = list(result.modules_used or [])
        elif isinstance(result, dict):
            modules = result.get("modules_used", [])

        if hasattr(result, "primary_output"):
            primary = result.primary_output
            if isinstance(primary, str) and primary:
                insights.append(primary)
            elif isinstance(primary, dict):
                combined = primary.get("combined_insights", "") if isinstance(primary, dict) else ""
                if combined:
                    insights.append(combined)
                wisdoms = primary.get("wisdom_sources", []) if isinstance(primary, dict) else []
                if wisdoms:
                    insights.append(f"fusion {len(wisdoms)} 个智慧系统:{', '.join(wisdoms[:4])}")
        elif isinstance(result, dict):
            insights = result.get("insights", result.get("content", []))
            if isinstance(insights, str):
                insights = [insights] if insights else []

        logger.info(f"[strategy增强] UnifiedIntelligenceCoordinator 激活模块: {modules[:4]}")
        return {
            "triggered": True,
            "modules_activated": modules[:8],
            "enhancement_insights": insights[:6] if isinstance(insights, list) else [str(insights)][:6],
            "task_type_used": task_type.value if hasattr(task_type, "value") else str(task_type),
            "source": "unified_intelligence_coordinator",
        }
    except Exception as e:
        logger.warning(f"[strategy增强] UnifiedIntelligenceCoordinator 调用失败: {e}")
        return empty

def maybe_run_metaphysics_analysis(
    description: str,
    extra_context: Optional[Dict[str, Any]] = None,
    parsed_requirement: Optional[Dict[str, Any]] = None,
    primary_industry: Optional[Any] = None,
) -> Dict[str, Any]:
    """按需触发术数时空分析,避免对普通任务无差别介入."""
    extra_context = extra_context or {}
    parsed_requirement = parsed_requirement or {}

    keyword_groups = {
        "environment": ["环境", "布局", "空间", "办公室", "工位", "风水", "朝向", "动线", "采光", "通风"],
        "timing": ["时机", "节奏", "窗口", "周期", "推进", "火候", "节拍", "阶段"],
        "structure": ["结构", "平衡", "配置", "协同", "关系", "阴阳", "五行", "补位", "主攻"],
    }

    text_parts = [
        description,
        parsed_requirement.get("objective", ""),
        " ".join(parsed_requirement.get("constraints", [])),
        " ".join(parsed_requirement.get("keywords", [])),
    ]
    search_text = " ".join(part for part in text_parts if part)

    trigger_reason = []
    for reason, keywords in keyword_groups.items():
        if any(keyword in search_text for keyword in keywords):
            trigger_reason.append(reason)

    context_keys = {str(key) for key in extra_context.keys()}
    if {"environment", "layout", "business_type", "element_weights", "pillars", "bazi", "zodiacs", "生肖"} & context_keys:
        trigger_reason.append("context_payload")

    trigger_reason = list(dict.fromkeys(trigger_reason))
    if not trigger_reason:
        return {"triggered": False, "trigger_reason": [], "summary": "", "action_plan": {}}

    payload: Dict[str, Any] = {}
    for key in [
        "element_weights", "factors", "keywords", "pillars", "bazi", "zodiacs", "生肖",
        "environment", "layout", "business_type", "yin_yang_factors",
    ]:
        if key in extra_context and extra_context.get(key) is not None:
            payload[key] = extra_context.get(key)

    if "layout" in payload and "environment" not in payload:
        payload["environment"] = payload["layout"]

    if parsed_requirement.get("keywords") and "keywords" not in payload:
        payload["keywords"] = parsed_requirement.get("keywords")

    if primary_industry is not None and "business_type" not in payload:
        payload["business_type"] = getattr(primary_industry, "value", str(primary_industry))

    try:
        from ..intelligence.metaphysics_wisdom_unified import quick_metaphysics_analyze
        result = quick_metaphysics_analyze(description, **payload)
        result["triggered"] = True
        result["trigger_reason"] = trigger_reason
        result["input_payload"] = payload
        return result
    except Exception as e:
        return {
            "triggered": True,
            "trigger_reason": trigger_reason,
            "error": "操作失败",
            "summary": "",
            "action_plan": {},
            "input_payload": payload,
        }
