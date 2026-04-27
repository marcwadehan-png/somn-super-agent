"""
__all__ = [
    'build_evaluation_report',
    'build_level_signal',
    'run_llm_evaluation',
]

SomnCore 评估与 ROI 追踪模块
提取自 somn_core.py 原 L3786-L4056 及 L4530-L4715 段，专注 ROI 追踪与主链自评。
依赖注入模式：通过回调函数参数接收 engine_self 的工具能力。
"""

import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from ._somn_utils import (
    resolve_reinforcement_action,
    extract_strategy_combo,
    resolve_estimated_minutes,
)

logger = logging.getLogger(__name__)

# =============================================================================
# ROI 追踪核心
# =============================================================================

def _estimate_task_quality_score(record: Any, clamp_fn: Callable = None) -> float:
    """把执行记录粗折算为 ROI 可消费的质量分."""
    if clamp_fn is None:
        clamp_fn = lambda v, d=0.0: round(max(0.0, min(1.0, float(v) if v is not None else float(d))), 4)

    status = str(getattr(record, "status", "") or "").lower()
    base_score = {
        "completed": 0.86,
        "failed": 0.22,
        "blocked": 0.35,
    }.get(status, 0.5)
    retry_penalty = min(0.24, max(0, int(getattr(record, "attempts", 0) or 0) - 1) * 0.08)
    tool_attempts = 1
    result = getattr(record, "result", None)
    if isinstance(result, dict):
        try:
            tool_attempts = int(result.get("tool_attempts") or 1)
        except (TypeError, ValueError):
            tool_attempts = 1
    tool_penalty = min(0.1, max(0, tool_attempts - 1) * 0.05)
    error_penalty = 0.08 if getattr(record, "last_error", None) and status != "completed" else 0.0
    return clamp_fn(base_score - retry_penalty - tool_penalty - error_penalty, 0.5)

def _track_roi_task_start(
    engine_self,
    workflow_task_id: str,
    record: Any,
    execution_config: Dict[str, Any],
    get_roi_tracker_fn: Callable = None,
    resolve_action_fn: Callable = None,
    resolve_minutes_fn: Callable = None,
) -> None:
    """在任务真正开跑时,把 ROI 投入侧也一起记账."""
    if get_roi_tracker_fn is None:
        get_roi_tracker_fn = lambda s: getattr(s, "_roi_tracker", None)
    if resolve_action_fn is None:
        resolve_action_fn = resolve_reinforcement_action
    if resolve_minutes_fn is None:
        resolve_minutes_fn = resolve_estimated_minutes

    roi_tracker = get_roi_tracker_fn(engine_self)
    if roi_tracker is None:
        return

    roi_task_id = f"{workflow_task_id}::{getattr(record, 'task_name', 'unknown')}"
    if roi_task_id in getattr(roi_tracker, "_active_tasks", {}):
        return

    try:
        roi_tracker.track_task_start(
            task_id=roi_task_id,
            task_type="workflow_execution",
            strategy=resolve_action_fn(record),
            estimated_minutes=resolve_minutes_fn(record, execution_config),
            workflow_id=workflow_task_id,
            scope="task",
        )
    except Exception as exc:
        logger.warning(f"ROI 起始追踪跳过 {roi_task_id}: {exc}")

def _track_roi_task_completion(
    engine_self,
    workflow_task_id: str,
    record: Any,
    get_roi_tracker_fn: Callable = None,
    estimate_quality_fn: Callable = None,
) -> Optional[str]:
    """在任务收束时把效率/收益结果写入 ROITracker."""
    if get_roi_tracker_fn is None:
        get_roi_tracker_fn = lambda s: getattr(s, "_roi_tracker", None)
    if estimate_quality_fn is None:
        estimate_quality_fn = _estimate_task_quality_score

    roi_tracker = get_roi_tracker_fn(engine_self)
    if roi_tracker is None:
        return None

    roi_task_id = f"{workflow_task_id}::{getattr(record, 'task_name', 'unknown')}"
    if roi_task_id not in getattr(roi_tracker, "_active_tasks", {}):
        return None

    outcome = {
        "completed": getattr(record, "status", "") == "completed",
        "quality_score": estimate_quality_fn(record),
        "adopted": getattr(record, "status", "") == "completed",
        "error_count": max(0, int(getattr(record, "attempts", 0) or 0) - 1) + (1 if getattr(record, "status", "") == "failed" else 0),
        "outputs": {
            "tool": getattr(record, "tool", ""),
            "task_name": getattr(record, "task_name", ""),
        },
    }
    try:
        return roi_tracker.track_task_complete(roi_task_id, outcome)
    except Exception as exc:
        logger.warning(f"ROI 完成追踪跳过 {roi_task_id}: {exc}")
        return None

def _track_roi_workflow_completion(
    engine_self,
    workflow_task_id: str,
    task_records: List[Any],
    execution_report: Dict[str, Any],
    get_roi_tracker_fn: Callable = None,
    extract_combo_fn: Callable = None,
) -> Dict[str, Any]:
    """在工作流收束时,把任务级 ROI 向上聚合到 workflow / strategy_combo."""
    if get_roi_tracker_fn is None:
        get_roi_tracker_fn = lambda s: getattr(s, "_roi_tracker", None)
    if extract_combo_fn is None:
        extract_combo_fn = lambda recs: extract_strategy_combo(recs, resolve_reinforcement_action)

    roi_tracker = get_roi_tracker_fn(engine_self)
    if roi_tracker is None:
        return {
            "status": "tracker_unavailable",
            "workflow_id": workflow_task_id,
            "workflow_record_id": "",
            "strategy_combo_record_id": "",
        }

    strategy_combo = execution_report.get("strategy_combo") or extract_combo_fn(task_records)
    execution_summary = execution_report.get("execution_summary", {}) if isinstance(execution_report, dict) else {}
    outcome = {
        "completed": int(execution_summary.get("completed", 0) or 0),
        "failed": int(execution_summary.get("failed", 0) or 0),
        "blocked": int(execution_summary.get("blocked", 0) or 0),
        "success_ratio": float(execution_summary.get("success_ratio", 0.0) or 0.0),
        "strategy_combo": strategy_combo,
    }
    try:
        return roi_tracker.track_workflow_completion(
            workflow_id=workflow_task_id,
            outcome=outcome,
            strategy_combo=strategy_combo,
        )
    except Exception as exc:
        logger.warning(f"工作流 ROI 聚合跳过 {workflow_task_id}: {exc}")
        return {
            "status": "aggregation_error",
            "workflow_id": workflow_task_id,
            "workflow_record_id": "",
            "strategy_combo_record_id": "",
            "reason": str(exc),
            "strategy_combo": strategy_combo,
        }

# =============================================================================
# ROI 信号构建
# =============================================================================

def _normalize_roi_ratio(value: Any, default: float = 0.5, clamp_fn: Callable = None) -> float:
    """把 ROI ratio 平滑压到 0~1,避免短任务把收益比放大失真."""
    if clamp_fn is None:
        clamp_fn = lambda v, d=0.5: round(max(0.0, min(1.0, float(v) if v is not None else float(d))), 4)

    try:
        ratio = float(value)
    except (TypeError, ValueError):
        return clamp_fn(default, 0.5)

    clipped = max(-1.0, min(1.0, ratio))
    normalized = 0.5 + clipped * 0.25
    if ratio > 1.0:
        normalized += min(0.25, (ratio - 1.0) * 0.05)
    return clamp_fn(normalized, default)

def _roi_trend_bias(trend: Any) -> float:
    """给 ROI 趋势一个小幅偏置,防止趋势信息丢失."""
    trend_key = str(trend or "").lower()
    return {
        "improving": 0.05,
        "declining": -0.05,
    }.get(trend_key, 0.0)

def _build_fallback_evaluation(
    execution_report: Dict[str, Any],
    criteria: Dict[str, Any],
) -> Dict[str, Any]:
    """构造兜底评估（无 LLM 时使用）."""
    summary = execution_report.get("execution_summary", {})
    success_ratio = float(summary.get("success_ratio", 0.0))
    total_tasks = int(summary.get("total_tasks", 0))
    failed = int(summary.get("failed", 0))
    quality = max(0.2, min(0.95, success_ratio - failed * 0.05 + (0.05 if total_tasks > 0 else 0)))
    robustness = max(0.2, min(0.95, 0.9 - failed * 0.1))
    score = max(0.0, min(1.0, (success_ratio * 0.5) + (quality * 0.3) + (robustness * 0.2)))

    key_findings = [f"任务成功率为 {round(success_ratio * 100, 1)}%"]
    if failed:
        key_findings.append(f"仍有 {failed} 个任务失败,需要下一轮修正")
    if criteria:
        key_findings.append("评估已参考外部标准要求")

    recommendations = []
    if failed:
        recommendations.append("优先处理失败任务的参数与工具匹配问题")
    if total_tasks == 0:
        recommendations.append("当前没有产出可执行任务,需要先加强任务规划")
    if not recommendations:
        recommendations.append("可以基于本轮结果继续细化执行任务")

    return {
        "overall_score": round(score, 4),
        "key_findings": key_findings,
        "detailed_metrics": {
            "completion": round(success_ratio, 4),
            "quality": round(quality, 4),
            "robustness": round(robustness, 4)
        },
        "recommendations": recommendations,
        "lessons_learned": ["真实执行结果必须回写到后续规划,而不是停留在模板阶段"]
    }

def _build_roi_signal_snapshot(
    engine_self,
    execution_report: Dict[str, Any],
    get_roi_tracker_fn: Callable = None,
    clamp_fn: Callable = None,
    normalize_roi_fn: Callable = None,
    trend_bias_fn: Callable = None,
    resolve_action_fn: Callable = None,
    extract_combo_fn: Callable = None,
) -> Dict[str, Any]:
    """把 ROITracker 里的效率/收益数据整理成评估层可直接消费的结构."""
    if get_roi_tracker_fn is None:
        get_roi_tracker_fn = lambda s: getattr(s, "_roi_tracker", None)
    if clamp_fn is None:
        clamp_fn = lambda v, d=0.0: round(max(0.0, min(1.0, float(v) if v is not None else float(d))), 4)
    if normalize_roi_fn is None:
        normalize_roi_fn = _normalize_roi_ratio
    if trend_bias_fn is None:
        trend_bias_fn = _roi_trend_bias
    if resolve_action_fn is None:
        resolve_action_fn = resolve_reinforcement_action
    if extract_combo_fn is None:
        extract_combo_fn = lambda recs: extract_strategy_combo(recs, resolve_action_fn)

    roi_tracker = get_roi_tracker_fn(engine_self)
    baseline = {
        "avg_efficiency": 0.5,
        "avg_quality": 0.5,
        "adopt_rate": 0.5,
        "avg_roi_ratio": 0.0,
        "roi_return_score": 0.5,
        "confidence": 0.0,
    }
    empty_level = {
        "has_data": False,
        "sample_count": 0,
        "avg_efficiency": baseline["avg_efficiency"],
        "avg_quality": baseline["avg_quality"],
        "adoption_rate": baseline["adopt_rate"],
        "avg_roi_ratio": baseline["avg_roi_ratio"],
        "roi_return_score": baseline["roi_return_score"],
        "roi_score": baseline["avg_efficiency"],
        "confidence": baseline["confidence"],
        "trend": "no_data",
        "last_used": "",
    }
    if roi_tracker is None:
        return {
            "available": False,
            "tracker_records": 0,
            "baseline": baseline,
            "actions": {},
            "workflow_level": {**empty_level, "workflow_id": execution_report.get("task_id", "")},
            "strategy_combo_level": {**empty_level, "strategy_combo": execution_report.get("strategy_combo", []), "strategy_combo_id": ""},
        }

    baseline_raw = roi_tracker.get_baseline() or {}
    baseline = {
        "avg_efficiency": clamp_fn(baseline_raw.get("avg_efficiency"), 0.5),
        "avg_quality": clamp_fn(baseline_raw.get("avg_quality"), 0.5),
        "adopt_rate": clamp_fn(baseline_raw.get("adopt_rate"), 0.5),
        "avg_roi_ratio": round(float(baseline_raw.get("avg_roi", 0.0) or 0.0), 4),
        "roi_return_score": normalize_roi_fn(baseline_raw.get("avg_roi"), 0.5, clamp_fn),
        "confidence": clamp_fn(baseline_raw.get("confidence"), 0.0),
    }

    def build_level_signal(raw_signal: Dict[str, Any], extra: Dict[str, Any] = None) -> Dict[str, Any]:
        extra = extra or {}
        has_data = raw_signal.get("status") != "no_data"
        avg_efficiency = clamp_fn(raw_signal.get("avg_efficiency_score"), baseline["avg_efficiency"])
        avg_quality = clamp_fn(raw_signal.get("avg_quality"), baseline["avg_quality"])
        adoption_rate = clamp_fn(raw_signal.get("adoption_rate"), baseline["adopt_rate"])
        avg_roi_ratio = round(float(raw_signal.get("avg_roi_ratio", baseline["avg_roi_ratio"]) or baseline["avg_roi_ratio"]), 4)
        roi_return_score = normalize_roi_fn(avg_roi_ratio, baseline["roi_return_score"], clamp_fn)
        success_ratio = clamp_fn(raw_signal.get("success_ratio"), adoption_rate)
        roi_score = clamp_fn(
            avg_efficiency * 0.35
            + avg_quality * 0.2
            + adoption_rate * 0.15
            + roi_return_score * 0.15
            + success_ratio * 0.1
            + trend_bias_fn(raw_signal.get("trend")),
            baseline["avg_efficiency"],
        )
        return {
            "has_data": has_data,
            "sample_count": int(raw_signal.get("sample_count", 0) or 0) if has_data else 0,
            "task_record_count": int(raw_signal.get("task_record_count", 0) or 0),
            "avg_efficiency": avg_efficiency,
            "avg_quality": avg_quality,
            "adoption_rate": adoption_rate,
            "avg_roi_ratio": avg_roi_ratio,
            "roi_return_score": roi_return_score,
            "roi_score": roi_score,
            "confidence": clamp_fn(raw_signal.get("confidence"), baseline["confidence"]),
            "success_ratio": success_ratio,
            "trend": raw_signal.get("trend", "no_data" if not has_data else "stable"),
            "last_used": raw_signal.get("last_used", ""),
            **extra,
        }

    task_results = execution_report.get("task_results", []) if isinstance(execution_report.get("task_results", []), list) else []
    actions: Dict[str, Any] = {}
    for task_result in task_results:
        action = resolve_action_fn(task_result)
        if action in actions:
            continue

        strategy_roi = roi_tracker.get_strategy_roi(action) or {}
        has_data = strategy_roi.get("status") != "no_data"
        avg_efficiency = clamp_fn(strategy_roi.get("avg_efficiency_score"), baseline["avg_efficiency"])
        avg_quality = clamp_fn(strategy_roi.get("avg_quality"), baseline["avg_quality"])
        adoption_rate = clamp_fn(strategy_roi.get("adoption_rate"), baseline["adopt_rate"])
        avg_roi_ratio = round(float(strategy_roi.get("avg_roi_ratio", baseline["avg_roi_ratio"]) or baseline["avg_roi_ratio"]), 4)
        roi_return_score = normalize_roi_fn(avg_roi_ratio, baseline["roi_return_score"], clamp_fn)
        roi_score = clamp_fn(
            avg_efficiency * 0.4
            + avg_quality * 0.2
            + adoption_rate * 0.2
            + roi_return_score * 0.2
            + trend_bias_fn(strategy_roi.get("trend")),
            baseline["avg_efficiency"],
        )
        actions[action] = {
            "has_data": has_data,
            "sample_count": int(strategy_roi.get("sample_count", 0) or 0) if has_data else 0,
            "avg_efficiency": avg_efficiency,
            "avg_quality": avg_quality,
            "adoption_rate": adoption_rate,
            "avg_roi_ratio": avg_roi_ratio,
            "roi_return_score": roi_return_score,
            "roi_score": roi_score,
            "confidence": clamp_fn(strategy_roi.get("confidence"), baseline["confidence"]),
            "trend": strategy_roi.get("trend", "no_data" if not has_data else "stable"),
            "last_used": strategy_roi.get("last_used", ""),
        }

    workflow_id = execution_report.get("task_id", "")
    strategy_combo = execution_report.get("strategy_combo") or extract_combo_fn(task_results)
    workflow_signal_raw = roi_tracker.get_workflow_roi(workflow_id) if workflow_id else {"status": "no_data"}
    combo_signal_raw = roi_tracker.get_strategy_combo_roi(strategy_combo=strategy_combo) if strategy_combo else {"status": "no_data"}

    return {
        "available": True,
        "tracker_records": len(getattr(roi_tracker, "_records", [])),
        "baseline": baseline,
        "actions": actions,
        "workflow_level": build_level_signal(workflow_signal_raw, {"workflow_id": workflow_id}),
        "strategy_combo_level": build_level_signal(
            combo_signal_raw,
            {
                "strategy_combo": strategy_combo,
                "strategy_combo_id": combo_signal_raw.get("strategy_combo_id", ""),
            },
        ),
    }

# =============================================================================
# 主链自评机制
# =============================================================================

def _evaluate_main_chain_performance(
    requirement: Dict[str, Any],
    strategy: Dict[str, Any],
    execution: Dict[str, Any],
    evaluation: Dict[str, Any],
    reflection: Dict[str, Any],
) -> Dict[str, Any]:
    """
    主链元认知自评:对本次运行的全链路质量打分,并给出改进建议.
    """
    exec_summary = execution.get("execution_summary", {})
    eval_summary = evaluation.get("evaluation_summary", {})

    # 理解深度
    structured = requirement.get("structured_requirement", {})
    understanding_score = min(1.0, (
        (1.0 if structured.get("objective") else 0) +
        (0.5 if structured.get("constraints") else 0) +
        (0.5 if structured.get("task_type") else 0) +
        (0.3 if structured.get("success_definition") else 0)
    ) / 2.5)

    # strategy有效性
    strategy_nodes = strategy.get("strategy_nodes", [])
    strategy_score = min(1.0, (
        min(len(strategy_nodes) / 5.0, 1.0) * 0.4 +
        (0.6 if strategy.get("risk_analysis") else 0)
    ))

    # 执行完成度
    total_tasks = exec_summary.get("total_tasks", 0)
    completed_tasks = exec_summary.get("completed", 0)
    execution_score = exec_summary.get("success_ratio", 0.0) if total_tasks > 0 else 0.0

    # 结果质量
    quality_score = eval_summary.get("overall_score", 0.0)

    # 学习有效性
    lessons = reflection.get("lessons_learned", [])
    reusable = reflection.get("reusable_actions", [])
    learning_score = min(1.0, len(lessons) / 3.0 * 0.5 + len(reusable) / 3.0 * 0.5)

    # 闭环完整性
    chain_completeness = sum([
        bool(requirement.get("task_id")),
        bool(strategy.get("task_id")),
        bool(execution.get("task_id")),
        bool(evaluation.get("evaluation_summary")),
        bool(reflection.get("lessons_learned")),
    ]) / 5.0

    weights = {
        "understanding": 0.15,
        "strategy": 0.20,
        "execution": 0.30,
        "quality": 0.20,
        "learning": 0.10,
        "completeness": 0.05,
    }
    total_score = sum([
        understanding_score * weights["understanding"],
        strategy_score * weights["strategy"],
        execution_score * weights["execution"],
        quality_score * weights["quality"],
        learning_score * weights["learning"],
        chain_completeness * weights["completeness"],
    ])

    if total_score >= 0.85:
        grade = "A+"
    elif total_score >= 0.75:
        grade = "A"
    elif total_score >= 0.65:
        grade = "B"
    elif total_score >= 0.50:
        grade = "C"
    else:
        grade = "D"

    suggestions = []
    if understanding_score < 0.6:
        suggestions.append("[理解]需求解析粒度不够细,建议补充约束条件和成功定义")
    if strategy_score < 0.6:
        suggestions.append("[strategy]strategy节点偏少或风险分析不足,建议深化strategy设计")
    if execution_score < 0.6:
        suggestions.append("[执行]任务完成率偏低,检查依赖关系和资源分配")
    if quality_score < 0.6:
        suggestions.append("[质量]评估得分不高,需提升交付物的具体性和可落地性")
    if learning_score < 0.4:
        suggestions.append("[学习]经验沉淀不足,建议强化可复用动作的提取")
    if chain_completeness < 0.8:
        suggestions.append("[闭环]部分阶段输出缺失,需确保每步都有实质结果")

    performance_report = {
        "total_score": round(total_score, 4),
        "grade": grade,
        "dimensions": {
            "understanding": {"score": round(understanding_score, 4), "weight": weights["understanding"], "label": "理解深度"},
            "strategy": {"score": round(strategy_score, 4), "weight": weights["strategy"], "label": "strategy有效性"},
            "execution": {"score": round(execution_score, 4), "weight": weights["execution"], "label": "执行完成度"},
            "quality": {"score": round(quality_score, 4), "weight": weights["quality"], "label": "结果质量"},
            "learning": {"score": round(learning_score, 4), "weight": weights["learning"], "label": "学习有效性"},
            "completeness": {"score": round(chain_completeness, 4), "weight": weights["completeness"], "label": "闭环完整性"},
        },
        "execution_snapshot": {
            "tasks_total": total_tasks,
            "tasks_completed": completed_tasks,
            "success_ratio": exec_summary.get("success_ratio", 0.0),
        },
        "suggestions": suggestions,
        "timestamp": datetime.now().isoformat(),
    }

    logger.info(
        f"[主链自评] score={total_score:.2f} grade={grade} "
        f"(理解={understanding_score:.2f} strategy={strategy_score:.2f} "
        f"执行={execution_score:.2f} 质量={quality_score:.2f})"
    )
    return performance_report

def _record_validation_learning(
    engine_self,
    execution_report: Dict[str, Any],
    evaluation_report: Dict[str, Any],
    ensure_layers_fn: Callable = None,
) -> None:
    try:
        if ensure_layers_fn is None:
            ensure_fn = getattr(engine_self, "_ensure_layers", None)
            if ensure_fn:
                ensure_fn()
        summary = execution_report.get("execution_summary", {})
        validation_result = {
            "original_confidence": 0.5,
            "passed": evaluation_report.get("evaluation_summary", {}).get("overall_score", 0) >= 0.6,
            "sample_size": max(1, int(summary.get("total_tasks", 0))),
            "effect_size": evaluation_report.get("evaluation_summary", {}).get("overall_score", 0),
            "p_value": max(0.01, 1 - evaluation_report.get("evaluation_summary", {}).get("overall_score", 0))
        }
        neural_system = getattr(engine_self, "neural_system", None)
        if neural_system is None:
            return
        learning = getattr(neural_system, "learning", None)
        if learning is None:
            return
        event = learning.learn_from_validation(
            hypothesis_id=f"strategy_{execution_report.get('based_on_strategy')}",
            validation_result=validation_result
        )
        learning.save_learning_event(event)
    except Exception as exc:
        logger.warning(f"⚠️ 学习事件写入失败: {str(exc)}")

def _generate_next_iteration(
    requirement: Dict[str, Any],
    strategy: Dict[str, Any],
    execution: Dict[str, Any],
    evaluation: Dict[str, Any],
    reflection: Dict[str, Any] = None,
    autonomy_context: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """generate下一轮动作建议."""
    reflection = reflection or {}
    autonomy_context = autonomy_context or {}
    score = evaluation.get("evaluation_summary", {}).get("overall_score", 0.0)
    summary = execution.get("execution_summary", {})
    if score < 0.6:
        focus = "先修执行失败点,再进入下一轮"
    elif summary.get("total_tasks", 0) <= 1:
        focus = "扩充任务层执行深度,把strategy拆得更细"
    else:
        focus = "保留有效strategy,继续增强评估与学习闭环"

    next_candidates = reflection.get("next_actions") or evaluation.get("recommendations", [])[:3]
    current_goal = autonomy_context.get("current_goal", {})
    return {
        "focus": focus,
        "priority_actions": evaluation.get("recommendations", [])[:3],
        "next_step_candidates": next_candidates[:3],
        "memory_writeback": True,
        "goal_id": current_goal.get("goal_id"),
        "goal_progress": current_goal.get("progress", 0.0),
        "suggested_next_task": reflection.get("suggested_next_task") or requirement.get("structured_requirement", {}).get("deliverable", "进入下一轮执行")
    }

# ══════════════════════════════════════════════════════
# LLM 评估
# ══════════════════════════════════════════════════════

def run_llm_evaluation(
    execution_report: Dict[str, Any],
    evaluation_criteria: Dict[str, Any],
    call_llm_fn: callable,
    build_fallback_fn: callable,
) -> Dict[str, Any]:
    """
    使用 LLM 对执行报告进行评估。
    返回原始 LLM 评估结果（含 fallback 填充）。
    """
    import json

    fallback = build_fallback_fn(execution_report, evaluation_criteria or {})
    prompt = f"""
你是 Somn 的执行评估器.请基于下面执行报告输出 JSON,不要输出其他解释.
JSON 结构:
{{
  "overall_score": 0-1 之间的小数,
  "key_findings": ["..."],
  "detailed_metrics": {{"completion": 0-1, "quality": 0-1, "robustness": 0-1}},
  "recommendations": ["..."],
  "lessons_learned": ["..."]
}}

评估标准:{json.dumps(evaluation_criteria or {}, ensure_ascii=False)}
执行摘要:{json.dumps(execution_report.get('execution_summary', {}), ensure_ascii=False)}
任务结果:{json.dumps(execution_report.get('task_results', []), ensure_ascii=False)}
"""
    return call_llm_fn(
        prompt=prompt,
        system_prompt="你是严谨的本地执行评估器,只输出合法 JSON.",
        fallback=fallback
    )

def build_evaluation_report(
    task_id: str,
    execution_report: Dict[str, Any],
    llm_evaluation: Dict[str, Any],
    fallback: Dict[str, Any],
) -> Dict[str, Any]:
    """构建评估报告字典."""
    return {
        "task_id": task_id,
        "based_on_execution": execution_report.get("task_id"),
        "evaluation_summary": {
            "overall_score": float(llm_evaluation.get("overall_score", fallback.get("overall_score"))),
            "key_findings": llm_evaluation.get("key_findings", fallback.get("key_findings"))
        },
        "detailed_metrics": llm_evaluation.get("detailed_metrics", fallback.get("detailed_metrics")),
        "recommendations": llm_evaluation.get("recommendations", fallback.get("recommendations")),
        "lessons_learned": llm_evaluation.get("lessons_learned", fallback.get("lessons_learned")),
        "evaluated_at": datetime.now().isoformat()
    }
