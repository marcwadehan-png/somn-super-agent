"""
__all__ = [
    'build_level_signal',
]

ROI 与反馈 API 层 - SomnCore ROI追踪与反馈处理方法委托
封装 ROI 追踪、质量评估、反馈构建等操作
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

def _module_clamp_unit_score(score: float, default: float = 0.5) -> float:
    try:
        val = float(score)
    except (TypeError, ValueError):
        return max(0.0, min(1.0, default))
    return max(0.0, min(1.0, val))

def _module_normalize_roi_ratio(somn_core, value: Any, default: float = 0.5) -> float:
    try:
        ratio = float(value)
    except (TypeError, ValueError):
        return _module_clamp_unit_score(default, 0.5)
    clipped = max(-1.0, min(1.0, ratio))
    normalized = 0.5 + clipped * 0.25
    if ratio > 1.0:
        normalized += min(0.25, (ratio - 1.0) * 0.05)
    return _module_clamp_unit_score(normalized, default)

def _module_roi_trend_bias(somn_core, trend: Any) -> float:
    trend_key = str(trend or "").lower()
    return {"improving": 0.05, "declining": -0.05}.get(trend_key, 0.0)

def _module_resolve_reinforcement_action(somn_core, record: Any) -> str:
    if not record:
        return "unknown"
    tool = getattr(record, "tool", None) or (record.get("tool") if isinstance(record, dict) else None)
    task_name = getattr(record, "task_name", None) or (record.get("task_name") if isinstance(record, dict) else None)
    action = getattr(record, "action", None) or (record.get("action") if isinstance(record, dict) else None)
    if tool and tool not in ("unknown", "workflow_evaluation"):
        return tool
    if task_name and task_name not in ("workflow_summary", ""):
        return str(task_name)
    if action:
        return str(action)
    return "default_action"

def _module_resolve_estimated_minutes(somn_core, record: Any, execution_config: Dict[str, Any]) -> Optional[float]:
    if isinstance(record, dict):
        params = record.get("parameters", {}) or {}
        if isinstance(params, dict):
            minutes = params.get("estimated_minutes")
            if minutes is not None:
                try:
                    return float(minutes)
                except (TypeError, ValueError):
                    pass
    if isinstance(execution_config, dict):
        minutes = execution_config.get("estimated_minutes")
        if minutes is not None:
            try:
                return float(minutes)
            except (TypeError, ValueError):
                pass
    if isinstance(record, dict):
        task_name = str(record.get("task_name", "")).lower()
        if any(k in task_name for k in ["research", "分析", "研究", "深度"]):
            return 15.0
        if any(k in task_name for k in ["create", "build", "生成", "创建"]):
            return 10.0
        if any(k in task_name for k in ["search", "find", "搜索", "查找"]):
            return 3.0
    return 5.0

def _module_extract_strategy_combo(somn_core, task_entries: List[Any]) -> List[str]:
    combo: List[str] = []
    seen = set()
    for entry in task_entries or []:
        action = _module_resolve_reinforcement_action(somn_core, entry)
        if not action or action in seen:
            continue
        seen.add(action)
        combo.append(action)
    return combo

def _module_estimate_task_quality_score(somn_core, record: Any) -> float:
    status = str(getattr(record, "status", None) or (record.get("status") if isinstance(record, dict) else "") or "").lower()
    base_score = {"completed": 0.86, "failed": 0.22, "blocked": 0.35}.get(status, 0.5)
    attempts = getattr(record, "attempts", None) or (record.get("attempts") if isinstance(record, dict) else None) or 0
    retry_penalty = min(0.24, max(0, int(attempts) - 1) * 0.08)
    tool_attempts = 1
    result = getattr(record, "result", None) or (record.get("result") if isinstance(record, dict) else None)
    if isinstance(result, dict):
        try:
            tool_attempts = int(result.get("tool_attempts") or 1)
        except (TypeError, ValueError):
            tool_attempts = 1
    tool_penalty = min(0.1, max(0, tool_attempts - 1) * 0.05)
    last_error = getattr(record, "last_error", None) or (record.get("last_error") if isinstance(record, dict) else None)
    error_penalty = 0.08 if last_error and status != "completed" else 0.0
    return _module_clamp_unit_score(base_score - retry_penalty - tool_penalty - error_penalty, 0.5)

def _module_task_outcome_anchor(somn_core, task_status: str) -> float:
    return {"completed": 1.0, "failed": 0.0, "blocked": 0.2}.get(str(task_status or "").lower(), 0.5)

def _module_score_to_rating_value(somn_core, score: float) -> float:
    return round(1.0 + _module_clamp_unit_score(score, 0.5) * 4.0, 2)

def _module_track_roi_task_start(somn_core, workflow_task_id: str, record: Any, execution_config: Dict[str, Any]) -> None:
    roi_tracker = somn_core._get_roi_tracker()
    if roi_tracker is None:
        return
    task_name = getattr(record, "task_name", None) or (record.get("task_name") if isinstance(record, dict) else "unknown")
    roi_task_id = f"{workflow_task_id}::{task_name}"
    if roi_task_id in getattr(roi_tracker, "_active_tasks", {}):
        return
    try:
        roi_tracker.track_task_start(
            task_id=roi_task_id,
            task_type="workflow_execution",
            strategy=_module_resolve_reinforcement_action(somn_core, record),
            estimated_minutes=_module_resolve_estimated_minutes(somn_core, record, execution_config),
            workflow_id=workflow_task_id,
            scope="task",
        )
    except Exception as exc:
        logger.warning(f"ROI 起始追踪跳过 {roi_task_id}: {exc}")

def _module_track_roi_task_completion(somn_core, workflow_task_id: str, record: Any) -> Optional[str]:
    roi_tracker = somn_core._get_roi_tracker()
    if roi_tracker is None:
        return None
    task_name = getattr(record, "task_name", None) or (record.get("task_name") if isinstance(record, dict) else "unknown")
    roi_task_id = f"{workflow_task_id}::{task_name}"
    if roi_task_id not in getattr(roi_tracker, "_active_tasks", {}):
        return None
    status = getattr(record, "status", None) or (record.get("status") if isinstance(record, dict) else "")
    attempts = getattr(record, "attempts", None) or (record.get("attempts") if isinstance(record, dict) else None) or 0
    outcome = {
        "completed": status == "completed",
        "quality_score": _module_estimate_task_quality_score(somn_core, record),
        "adopted": status == "completed",
        "error_count": max(0, int(attempts) - 1) + (1 if status == "failed" else 0),
        "outputs": {"tool": getattr(record, "tool", None) or (record.get("tool") if isinstance(record, dict) else ""), "task_name": task_name},
    }
    try:
        return roi_tracker.track_task_complete(roi_task_id, outcome)
    except Exception as exc:
        logger.warning(f"ROI 完成追踪跳过 {roi_task_id}: {exc}")
        return None

def _module_track_roi_workflow_completion(somn_core, workflow_task_id: str, task_records: List[Any], execution_report: Dict[str, Any]) -> Dict[str, Any]:
    roi_tracker = somn_core._get_roi_tracker()
    if roi_tracker is None:
        return {"status": "tracker_unavailable", "workflow_id": workflow_task_id, "workflow_record_id": "", "strategy_combo_record_id": ""}
    strategy_combo = execution_report.get("strategy_combo") or _module_extract_strategy_combo(somn_core, task_records)
    execution_summary = execution_report.get("execution_summary", {}) if isinstance(execution_report, dict) else {}
    outcome = {
        "completed": int(execution_summary.get("completed", 0) or 0),
        "failed": int(execution_summary.get("failed", 0) or 0),
        "blocked": int(execution_summary.get("blocked", 0) or 0),
        "success_ratio": float(execution_summary.get("success_ratio", 0.0) or 0.0),
        "strategy_combo": strategy_combo,
    }
    try:
        return roi_tracker.track_workflow_completion(workflow_id=workflow_task_id, outcome=outcome, strategy_combo=strategy_combo)
    except Exception as exc:
        logger.warning(f"工作流 ROI 聚合跳过 {workflow_task_id}: {exc}")
        return {"status": "aggregation_error", "workflow_id": workflow_task_id, "workflow_record_id": "", "strategy_combo_record_id": "", "reason": str(exc), "strategy_combo": strategy_combo}

def _module_build_roi_signal_snapshot(somn_core, execution_report: Dict[str, Any]) -> Dict[str, Any]:
    roi_tracker = somn_core._get_roi_tracker()
    baseline_defaults = {"avg_efficiency": 0.5, "avg_quality": 0.5, "adopt_rate": 0.5, "avg_roi_ratio": 0.0, "roi_return_score": 0.5, "confidence": 0.0}
    empty_level = {**{k: 0.5 for k in baseline_defaults}, "has_data": False, "sample_count": 0, "trend": "no_data", "last_used": ""}
    if roi_tracker is None:
        return {"available": False, "tracker_records": 0, "baseline": baseline_defaults, "actions": {}, "workflow_level": {**empty_level, "workflow_id": execution_report.get("task_id", "")}, "strategy_combo_level": {**empty_level, "strategy_combo": [], "strategy_combo_id": ""}}

    baseline_raw = roi_tracker.get_baseline() or {}
    baseline = {
        "avg_efficiency": _module_clamp_unit_score(baseline_raw.get("avg_efficiency"), 0.5),
        "avg_quality": _module_clamp_unit_score(baseline_raw.get("avg_quality"), 0.5),
        "adopt_rate": _module_clamp_unit_score(baseline_raw.get("adopt_rate"), 0.5),
        "avg_roi_ratio": round(float(baseline_raw.get("avg_roi", 0.0) or 0.0), 4),
        "roi_return_score": _module_normalize_roi_ratio(somn_core, baseline_raw.get("avg_roi"), 0.5),
        "confidence": _module_clamp_unit_score(baseline_raw.get("confidence"), 0.0),
    }

    def build_level_signal(raw_signal, extra=None):
        extra = extra or {}
        has_data = raw_signal.get("status") != "no_data"
        avg_efficiency = _module_clamp_unit_score(raw_signal.get("avg_efficiency_score"), baseline["avg_efficiency"])
        avg_quality = _module_clamp_unit_score(raw_signal.get("avg_quality"), baseline["avg_quality"])
        adoption_rate = _module_clamp_unit_score(raw_signal.get("adoption_rate"), baseline["adopt_rate"])
        avg_roi_ratio = round(float(raw_signal.get("avg_roi_ratio", baseline["avg_roi_ratio"]) or baseline["avg_roi_ratio"]), 4)
        roi_return_score = _module_normalize_roi_ratio(somn_core, avg_roi_ratio, baseline["roi_return_score"])
        success_ratio = _module_clamp_unit_score(raw_signal.get("success_ratio"), adoption_rate)
        roi_score = _module_clamp_unit_score(
            avg_efficiency * 0.35 + avg_quality * 0.2 + adoption_rate * 0.15 + roi_return_score * 0.15 + success_ratio * 0.1 + _module_roi_trend_bias(somn_core, raw_signal.get("trend")),
            baseline["avg_efficiency"],
        )
        return {"has_data": has_data, "sample_count": int(raw_signal.get("sample_count", 0) or 0) if has_data else 0, "task_record_count": int(raw_signal.get("task_record_count", 0) or 0), "avg_efficiency": avg_efficiency, "avg_quality": avg_quality, "adoption_rate": adoption_rate, "avg_roi_ratio": avg_roi_ratio, "roi_return_score": roi_return_score, "roi_score": roi_score, "confidence": _module_clamp_unit_score(raw_signal.get("confidence"), baseline["confidence"]), "success_ratio": success_ratio, "trend": raw_signal.get("trend", "no_data" if not has_data else "stable"), "last_used": raw_signal.get("last_used", ""), **extra}

    task_results = execution_report.get("task_results", []) if isinstance(execution_report.get("task_results", []), list) else []
    actions: Dict[str, Any] = {}
    for task_result in task_results:
        action = _module_resolve_reinforcement_action(somn_core, task_result)
        if action in actions:
            continue
        strategy_roi = roi_tracker.get_strategy_roi(action) or {}
        has_data = strategy_roi.get("status") != "no_data"
        avg_efficiency = _module_clamp_unit_score(strategy_roi.get("avg_efficiency_score"), baseline["avg_efficiency"])
        avg_quality = _module_clamp_unit_score(strategy_roi.get("avg_quality"), baseline["avg_quality"])
        adoption_rate = _module_clamp_unit_score(strategy_roi.get("adoption_rate"), baseline["adopt_rate"])
        avg_roi_ratio = round(float(strategy_roi.get("avg_roi_ratio", baseline["avg_roi_ratio"]) or baseline["avg_roi_ratio"]), 4)
        roi_return_score = _module_normalize_roi_ratio(somn_core, avg_roi_ratio, baseline["roi_return_score"])
        roi_score = _module_clamp_unit_score(avg_efficiency * 0.4 + avg_quality * 0.2 + adoption_rate * 0.2 + roi_return_score * 0.2 + _module_roi_trend_bias(somn_core, strategy_roi.get("trend")), baseline["avg_efficiency"])
        actions[action] = {"has_data": has_data, "sample_count": int(strategy_roi.get("sample_count", 0) or 0) if has_data else 0, "avg_efficiency": avg_efficiency, "avg_quality": avg_quality, "adoption_rate": adoption_rate, "avg_roi_ratio": avg_roi_ratio, "roi_return_score": roi_return_score, "roi_score": roi_score, "confidence": _module_clamp_unit_score(strategy_roi.get("confidence"), baseline["confidence"]), "trend": strategy_roi.get("trend", "no_data" if not has_data else "stable"), "last_used": strategy_roi.get("last_used", "")}

    workflow_id = execution_report.get("task_id", "")
    strategy_combo = execution_report.get("strategy_combo") or _module_extract_strategy_combo(somn_core, task_results)
    workflow_signal_raw = roi_tracker.get_workflow_roi(workflow_id) if workflow_id else {"status": "no_data"}
    combo_signal_raw = roi_tracker.get_strategy_combo_roi(strategy_combo=strategy_combo) if strategy_combo else {"status": "no_data"}
    return {"available": True, "tracker_records": len(getattr(roi_tracker, "_records", [])), "baseline": baseline, "actions": actions, "workflow_level": build_level_signal(workflow_signal_raw, {"workflow_id": workflow_id}), "strategy_combo_level": build_level_signal(combo_signal_raw, {"strategy_combo": strategy_combo, "strategy_combo_id": combo_signal_raw.get("strategy_combo_id", "")})}

def _module_serialize_feedback_item(somn_core, feedback: Any) -> Dict[str, Any]:
    def _g(obj, name, default=None):
        return getattr(obj, name, default) if hasattr(obj, name) else default
    signal = _g(feedback, "signal", None)
    return {"feedback_id": _g(feedback, "feedback_id", ""), "task_id": _g(feedback, "task_id", ""), "task_type": _g(feedback, "task_type", ""), "strategy": _g(feedback, "strategy", ""), "signal": _g(signal, "name", "NEUTRAL") if signal else "NEUTRAL", "reward_value": _g(feedback, "reward_value", 0.0), "raw_type": _g(feedback, "raw_type", ""), "raw_value": _g(feedback, "raw_value", None), "timestamp": _g(feedback, "timestamp", ""), "session_id": _g(feedback, "session_id", ""), "user_id": _g(feedback, "user_id", "default")}

def _module_serialize_reinforcement_updates(updates: List[Any]) -> List[Dict[str, Any]]:
    def _g(obj, name, default=None):
        return getattr(obj, name, default) if hasattr(obj, name) else default
    return [{"action": _g(u, "action", ""), "reward": _g(u, "reward", 0.0), "q_value_before": _g(u, "q_value_before", 0.0), "q_value_after": _g(u, "q_value_after", 0.0), "n_samples": _g(u, "n_samples", 0), "timestamp": _g(u, "timestamp", ""), "source": _g(u, "source", "")} for u in updates]

def _module_build_workflow_feedback_entries(somn_core, workflow_task_id: str, task_records: List[Any]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    timestamp = datetime.now().isoformat()
    for record in task_records or []:
        task_name = getattr(record, "task_name", None) or (record.get("task_name") if isinstance(record, dict) else "task")
        status = getattr(record, "status", None) or (record.get("status") if isinstance(record, dict) else "")
        action = _module_resolve_reinforcement_action(somn_core, record)
        quality_score = _module_estimate_task_quality_score(somn_core, record)
        rating_value = _module_score_to_rating_value(somn_core, quality_score)
        entries.append({"task_id": f"{workflow_task_id}::{task_name}::execution", "task_type": "workflow_execution", "strategy": action, "type": "rating", "value": rating_value, "session_id": workflow_task_id, "user_id": "system", "timestamp": timestamp})
    return entries

def _module_build_evaluation_feedback_entries(somn_core, execution_report: Dict[str, Any], evaluation_report: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    evaluation_summary = evaluation_report.get("evaluation_summary", {}) if isinstance(evaluation_report, dict) else {}
    detailed_metrics = evaluation_report.get("detailed_metrics", {}) if isinstance(evaluation_report, dict) else {}
    execution_summary = execution_report.get("execution_summary", {}) if isinstance(execution_report, dict) else {}
    overall_score = _module_clamp_unit_score(evaluation_summary.get("overall_score"), execution_summary.get("success_ratio", 0.0))
    completion = _module_clamp_unit_score(detailed_metrics.get("completion"), execution_summary.get("success_ratio", overall_score))
    quality = _module_clamp_unit_score(detailed_metrics.get("quality"), overall_score)
    robustness = _module_clamp_unit_score(detailed_metrics.get("robustness"), overall_score)
    composite_score = _module_clamp_unit_score(overall_score * 0.35 + completion * 0.25 + quality * 0.25 + robustness * 0.15, overall_score)
    task_results = execution_report.get("task_results", []) if isinstance(execution_report.get("task_results", []), list) else []
    if not task_results:
        task_results = [{"task_name": "workflow_summary", "tool": "workflow_evaluation", "parameters": {"strategy": execution_report.get("based_on_strategy") or execution_report.get("task_id", "workflow_summary")}, "status": "completed" if overall_score >= 0.6 else "failed", "success": overall_score >= 0.6}]
    roi_signal = _module_build_roi_signal_snapshot(somn_core, {**execution_report, "task_results": task_results})
    timestamp = evaluation_report.get("evaluated_at", datetime.now().isoformat())
    session_id = evaluation_report.get("task_id") or f"eval::{execution_report.get('task_id', 'unknown')}"
    raw_feedbacks: List[Dict[str, Any]] = []
    action_scores: List[Dict[str, Any]] = []
    workflow_roi_score = _module_clamp_unit_score((roi_signal.get("workflow_level", {}) or {}).get("roi_score"), roi_signal.get("baseline", {}).get("avg_efficiency", 0.5))
    combo_roi_score = _module_clamp_unit_score((roi_signal.get("strategy_combo_level", {}) or {}).get("roi_score"), workflow_roi_score)
    for task_result in task_results:
        action = _module_resolve_reinforcement_action(somn_core, task_result)
        task_status = task_result.get("status") or ("completed" if task_result.get("success") else "failed")
        base_action_score = _module_clamp_unit_score((composite_score + _module_task_outcome_anchor(somn_core, task_status)) / 2.0, composite_score)
        roi_action_signal = (roi_signal.get("actions", {}) or {}).get(action, {})
        roi_score = _module_clamp_unit_score(roi_action_signal.get("roi_score"), roi_signal.get("baseline", {}).get("avg_efficiency", 0.5))
        action_score = _module_clamp_unit_score(base_action_score * 0.7 + roi_score * 0.15 + workflow_roi_score * 0.075 + combo_roi_score * 0.075, base_action_score)
        rating_value = _module_score_to_rating_value(somn_core, action_score)
        raw_feedbacks.append({"task_id": f"{execution_report.get('task_id', 'execution')}::{task_result.get('task_name', 'task')}::evaluation", "task_type": "workflow_evaluation", "strategy": action, "type": "rating", "value": rating_value, "session_id": session_id, "user_id": "system", "timestamp": timestamp})
        action_scores.append({"task_name": task_result.get("task_name", "task"), "action": action, "task_status": task_status, "base_action_score": base_action_score, "roi_score": roi_score, "workflow_roi_score": workflow_roi_score, "combo_roi_score": combo_roi_score, "action_score": action_score, "rating_value": rating_value, "roi_signal": roi_action_signal})
    return raw_feedbacks, {"overall_score": overall_score, "detailed_metrics": {"completion": completion, "quality": quality, "robustness": robustness}, "composite_score": composite_score, "roi_signal": roi_signal, "action_scores": action_scores}

def _module_apply_reinforcement_inputs(somn_core, rl_inputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rl_trigger = somn_core._get_reinforcement_trigger()
    if rl_trigger is None or not rl_inputs:
        return []
    applied = 0
    for rl_input in rl_inputs:
        action = str(rl_input.get("action", "") or "").strip()
        reward = float((rl_input.get("outcome") or {}).get("reward", 0.0))
        if not action:
            continue
        rl_trigger.push_feedback(action=action, reward=reward)
        applied += 1
    if applied == 0:
        return []
    try:
        updates = rl_trigger.trigger_update(force=True)
    except Exception as exc:
        logger.warning(f"强化学习更新跳过: {exc}")
        return []
    return _module_serialize_reinforcement_updates(updates)

def _module_submit_feedback_entries(somn_core, raw_feedbacks: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = {"feedback_pipeline": {"received": 0, "synced": 0, "errors": 0, "feedback_ids": []}, "normalized_feedbacks": [], "reinforcement_inputs": [], "reinforcement_updates": []}
    if not raw_feedbacks:
        return result
    feedback_pipeline = somn_core._get_feedback_pipeline()
    if feedback_pipeline is None:
        return result
    recent_feedbacks = []
    feedback_ids: List[str] = []
    for raw_feedback in raw_feedbacks:
        feedback_id = feedback_pipeline.receive_feedback(raw_feedback)
        if not feedback_id:
            continue
        feedback_ids.append(feedback_id)
        matched = next((fb for fb in reversed(getattr(feedback_pipeline, "_pending", [])) if getattr(fb, "feedback_id", "") == feedback_id), None)
        if matched is not None:
            recent_feedbacks.append(matched)
    if not feedback_ids:
        return result
    sync_stats = feedback_pipeline.sync_to_roi_tracker()
    reinforcement_inputs = feedback_pipeline.route_to_reinforcement(recent_feedbacks)
    result["feedback_pipeline"] = {"received": len(recent_feedbacks), "synced": int(sync_stats.get("synced", 0)), "errors": int(sync_stats.get("errors", 0)), "feedback_ids": feedback_ids}
    result["normalized_feedbacks"] = [_module_serialize_feedback_item(somn_core, fb) for fb in recent_feedbacks]
    result["reinforcement_inputs"] = [{"action": item.get("action", ""), "reward": float((item.get("outcome") or {}).get("reward", 0.0)), "feedback_count": int((item.get("outcome") or {}).get("feedback_count", 0)), "success": bool((item.get("outcome") or {}).get("success", False))} for item in reinforcement_inputs]
    result["reinforcement_updates"] = _module_apply_reinforcement_inputs(somn_core, reinforcement_inputs)
    return result
