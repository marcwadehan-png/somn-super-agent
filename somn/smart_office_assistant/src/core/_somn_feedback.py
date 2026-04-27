"""
__all__ = [
    'record_user_feedback',
]

SomnCore 反馈管道模块
提取自 somn_core.py 原 L3254-L4403 段，专注反馈闭环与学习写入。
依赖注入模式：通过回调函数参数接收 engine_self 的工具能力。
"""

import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from ._somn_utils import clamp_unit_score, resolve_reinforcement_action, extract_strategy_combo

logger = logging.getLogger(__name__)

# =============================================================================
# 反馈管道初始化
# =============================================================================

def _get_feedback_pipeline(engine_self) -> Any:
    """懒加载反馈管道,unified接住显式/隐式反馈."""
    if getattr(engine_self, "_feedback_pipeline_unavailable", False):
        return None

    if getattr(engine_self, "_feedback_pipeline", None) is not None:
        return engine_self._feedback_pipeline

    try:
        from ...neural_memory.feedback_pipeline import FeedbackPipeline

        engine_self._feedback_pipeline = FeedbackPipeline(
            str(engine_self.base_path / "data" / "learning" / "feedback_pipeline")
        )
        return engine_self._feedback_pipeline
    except Exception as exc:
        engine_self._feedback_pipeline_unavailable = True
        logger.warning(f"反馈管道init失败,已跳过本轮反馈整合: {exc}")
        return None

def _get_reinforcement_trigger(engine_self) -> Any:
    """懒加载强化学习触发器,避免init阶段硬依赖."""
    if getattr(engine_self, "_reinforcement_feedback_unavailable", False):
        return None

    if getattr(engine_self, "_reinforcement_trigger", None) is not None:
        return engine_self._reinforcement_trigger

    try:
        from ...neural_memory.reinforcement_trigger import ReinforcementTrigger

        engine_self._reinforcement_trigger = ReinforcementTrigger(
            str(engine_self.base_path / "data" / "learning")
        )
        return engine_self._reinforcement_trigger
    except Exception as exc:
        engine_self._reinforcement_feedback_unavailable = True
        logger.warning(f"强化学习触发器init失败,已跳过本轮反馈写回: {exc}")
        return None

def _get_roi_tracker(engine_self) -> Any:
    """懒加载 ROI 追踪器,让执行效率/收益信号也能进入主链."""
    if getattr(engine_self, "_roi_tracker_unavailable", False):
        return None

    if getattr(engine_self, "_roi_tracker", None) is not None:
        return engine_self._roi_tracker

    try:
        from ...neural_memory.roi_tracker import ROITracker

        engine_self._roi_tracker = ROITracker(
            str(engine_self.base_path / "data" / "learning")
        )
        return engine_self._roi_tracker
    except Exception as exc:
        engine_self._roi_tracker_unavailable = True
        logger.warning(f"ROI 追踪器init失败,已跳过本轮 ROI 信号整合: {exc}")
        return None

# =============================================================================
# 序列化辅助
# =============================================================================

def _serialize_feedback_item(feedback: Any) -> Dict[str, Any]:
    """把反馈对象转成可落盘/可回传结构."""
    return {
        "feedback_id": getattr(feedback, "feedback_id", ""),
        "task_id": getattr(feedback, "task_id", ""),
        "task_type": getattr(feedback, "task_type", ""),
        "strategy": getattr(feedback, "strategy", ""),
        "signal": getattr(getattr(feedback, "signal", None), "name", "NEUTRAL"),
        "reward_value": getattr(feedback, "reward_value", 0.0),
        "raw_type": getattr(feedback, "raw_type", ""),
        "raw_value": getattr(feedback, "raw_value", None),
        "timestamp": getattr(feedback, "timestamp", ""),
        "session_id": getattr(feedback, "session_id", ""),
        "user_id": getattr(feedback, "user_id", "default"),
    }

def _serialize_reinforcement_updates(updates: List[Any]) -> List[Dict[str, Any]]:
    return [
        {
            "action": update.action,
            "reward": update.reward,
            "q_value_before": update.q_value_before,
            "q_value_after": update.q_value_after,
            "n_samples": update.n_samples,
            "timestamp": update.timestamp,
            "source": update.source,
        }
        for update in updates
    ]

# =============================================================================
# 反馈构建
# =============================================================================

def _build_workflow_feedback_entries(
    engine_self,
    workflow_task_id: str,
    task_records: List[Any],
) -> List[Dict[str, Any]]:
    """把任务执行状态翻译成反馈管道可消费的原始反馈."""
    entries: List[Dict[str, Any]] = []
    for record in task_records:
        if record.status not in {"completed", "failed", "blocked"}:
            continue

        base_feedback = {
            "task_id": f"{workflow_task_id}::{record.task_name}",
            "task_type": "workflow_execution",
            "strategy": resolve_reinforcement_action(record),
            "session_id": workflow_task_id,
            "user_id": "system",
            "timestamp": record.completed_at or datetime.now().isoformat(),
        }

        if record.status == "completed":
            entries.append({**base_feedback, "type": "adoption", "value": "采纳"})
            if record.attempts > 1:
                entries.append({
                    **base_feedback,
                    "type": "correction",
                    "value": -min(1.0, (record.attempts - 1) / 5.0),
                })
        elif record.status == "failed":
            entries.append({**base_feedback, "type": "rejection", "value": -1.0})
        else:
            entries.append({**base_feedback, "type": "correction", "value": -0.4})

    return entries

def _clamp_unit_score(value: Any, default: float = 0.0) -> float:
    """把分值限制在 0~1,避免异常评估污染反馈."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = float(default)
    return round(max(0.0, min(1.0, score)), 4)

def _score_to_rating_value(score: float) -> float:
    """把 0~1 分数折算为 feedback_pipeline 可消费的 1~5 评分."""
    return round(1.0 + _clamp_unit_score(score, 0.5) * 4.0, 2)

def _task_outcome_anchor(task_status: str) -> float:
    """把任务状态mapping为评估反馈的基准锚点."""
    return {
        "completed": 1.0,
        "failed": 0.0,
        "blocked": 0.2,
    }.get(str(task_status or "").lower(), 0.5)

def _build_evaluation_feedback_entries(
    engine_self,
    execution_report: Dict[str, Any],
    evaluation_report: Dict[str, Any],
    clamp_fn: Callable = None,
    score_to_rating_fn: Callable = None,
    task_outcome_anchor_fn: Callable = None,
    build_roi_signal_fn: Callable = None,
    resolve_fn: Callable = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """把效果评估结果折算成可学习反馈,让奖励不只看 completed/failed."""
    if clamp_fn is None:
        clamp_fn = _clamp_unit_score
    if score_to_rating_fn is None:
        score_to_rating_fn = _score_to_rating_value
    if task_outcome_anchor_fn is None:
        task_outcome_anchor_fn = _task_outcome_anchor
    if resolve_fn is None:
        resolve_fn = resolve_reinforcement_action

    evaluation_summary = evaluation_report.get("evaluation_summary", {}) if isinstance(evaluation_report, dict) else {}
    detailed_metrics = evaluation_report.get("detailed_metrics", {}) if isinstance(evaluation_report, dict) else {}
    execution_summary = execution_report.get("execution_summary", {}) if isinstance(execution_report, dict) else {}

    overall_score = clamp_fn(
        evaluation_summary.get("overall_score"),
        execution_summary.get("success_ratio", 0.0),
    )
    completion = clamp_fn(
        detailed_metrics.get("completion"),
        execution_summary.get("success_ratio", overall_score),
    )
    quality = clamp_fn(detailed_metrics.get("quality"), overall_score)
    robustness = clamp_fn(detailed_metrics.get("robustness"), overall_score)
    composite_score = clamp_fn(
        overall_score * 0.35 + completion * 0.25 + quality * 0.25 + robustness * 0.15,
        overall_score,
    )

    task_results = execution_report.get("task_results", []) if isinstance(execution_report.get("task_results", []), list) else []
    if not task_results:
        task_results = [{
            "task_name": "workflow_summary",
            "tool": "workflow_evaluation",
            "parameters": {
                "strategy": execution_report.get("based_on_strategy") or execution_report.get("task_id", "workflow_summary")
            },
            "status": "completed" if overall_score >= 0.6 else "failed",
            "success": overall_score >= 0.6,
        }]

    roi_signal = {}
    if build_roi_signal_fn:
        roi_signal = build_roi_signal_fn({
            **execution_report,
            "task_results": task_results,
        })
    timestamp = evaluation_report.get("evaluated_at", datetime.now().isoformat())
    session_id = evaluation_report.get("task_id") or f"eval::{execution_report.get('task_id', 'unknown')}"
    raw_feedbacks: List[Dict[str, Any]] = []
    action_scores: List[Dict[str, Any]] = []
    workflow_roi_score = clamp_fn(
        (roi_signal.get("workflow_level", {}) or {}).get("roi_score"),
        roi_signal.get("baseline", {}).get("avg_efficiency", 0.5),
    )
    combo_roi_score = clamp_fn(
        (roi_signal.get("strategy_combo_level", {}) or {}).get("roi_score"),
        workflow_roi_score,
    )

    for task_result in task_results:
        action = resolve_fn(task_result)
        task_status = task_result.get("status") or ("completed" if task_result.get("success") else "failed")
        base_action_score = clamp_fn(
            (composite_score + task_outcome_anchor_fn(task_status)) / 2.0,
            composite_score,
        )
        roi_action_signal = (roi_signal.get("actions", {}) or {}).get(action, {})
        roi_score = clamp_fn(
            roi_action_signal.get("roi_score"),
            roi_signal.get("baseline", {}).get("avg_efficiency", 0.5),
        )
        action_score = clamp_fn(
            base_action_score * 0.7
            + roi_score * 0.15
            + workflow_roi_score * 0.075
            + combo_roi_score * 0.075,
            base_action_score,
        )
        rating_value = score_to_rating_fn(action_score)

        raw_feedbacks.append({
            "task_id": f"{execution_report.get('task_id', 'execution')}::{task_result.get('task_name', 'task')}::evaluation",
            "task_type": "workflow_evaluation",
            "strategy": action,
            "type": "rating",
            "value": rating_value,
            "session_id": session_id,
            "user_id": "system",
            "timestamp": timestamp,
        })
        action_scores.append({
            "task_name": task_result.get("task_name", "task"),
            "action": action,
            "task_status": task_status,
            "base_action_score": base_action_score,
            "roi_score": roi_score,
            "workflow_roi_score": workflow_roi_score,
            "combo_roi_score": combo_roi_score,
            "action_score": action_score,
            "rating_value": rating_value,
            "roi_signal": roi_action_signal,
        })

    return raw_feedbacks, {
        "overall_score": overall_score,
        "detailed_metrics": {
            "completion": completion,
            "quality": quality,
            "robustness": robustness,
        },
        "composite_score": composite_score,
        "roi_signal": roi_signal,
        "action_scores": action_scores,
    }

# =============================================================================
# 反馈提交
# =============================================================================

def _apply_reinforcement_inputs(
    engine_self,
    rl_inputs: List[Dict[str, Any]],
    get_reinforcement_trigger_fn: Callable = None,
) -> List[Dict[str, Any]]:
    """把反馈管道路由出的奖励信号写入强化学习 Q 表."""
    if get_reinforcement_trigger_fn is None:
        get_reinforcement_trigger_fn = lambda s: _get_reinforcement_trigger(s)

    rl_trigger = get_reinforcement_trigger_fn(engine_self)
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

    serialized_updates = _serialize_reinforcement_updates(updates)
    if serialized_updates:
        logger.info(f"强化学习写回完成,共更新 {len(serialized_updates)} 个动作")
    return serialized_updates

def _submit_feedback_entries(
    engine_self,
    raw_feedbacks: List[Dict[str, Any]],
    get_feedback_pipeline_fn: Callable = None,
    apply_reinforcement_fn: Callable = None,
) -> Dict[str, Any]:
    """提交一批反馈到 FeedbackPipeline,并继续路由到强化学习."""
    if get_feedback_pipeline_fn is None:
        get_feedback_pipeline_fn = lambda s: _get_feedback_pipeline(s)
    if apply_reinforcement_fn is None:
        apply_reinforcement_fn = lambda s, r: _apply_reinforcement_inputs(s, r)

    result = {
        "feedback_pipeline": {
            "received": 0,
            "synced": 0,
            "errors": 0,
            "feedback_ids": [],
        },
        "normalized_feedbacks": [],
        "reinforcement_inputs": [],
        "reinforcement_updates": [],
    }
    if not raw_feedbacks:
        return result

    feedback_pipeline = get_feedback_pipeline_fn(engine_self)
    if feedback_pipeline is None:
        return result

    recent_feedbacks = []
    feedback_ids: List[str] = []
    for raw_feedback in raw_feedbacks:
        feedback_id = feedback_pipeline.receive_feedback(raw_feedback)
        if not feedback_id:
            continue
        feedback_ids.append(feedback_id)
        matched_feedback = next(
            (fb for fb in reversed(getattr(feedback_pipeline, "_pending", []) or []) if fb.feedback_id == feedback_id),
            None,
        )
        if matched_feedback is not None:
            recent_feedbacks.append(matched_feedback)

    if not feedback_ids:
        return result

    sync_stats = feedback_pipeline.sync_to_roi_tracker()
    reinforcement_inputs = feedback_pipeline.route_to_reinforcement(recent_feedbacks)
    result["feedback_pipeline"] = {
        "received": len(recent_feedbacks),
        "synced": int(sync_stats.get("synced", 0)),
        "errors": int(sync_stats.get("errors", 0)),
        "feedback_ids": feedback_ids,
    }
    result["normalized_feedbacks"] = [
        _serialize_feedback_item(feedback)
        for feedback in recent_feedbacks
    ]
    result["reinforcement_inputs"] = [
        {
            "action": item.get("action", ""),
            "reward": float((item.get("outcome") or {}).get("reward", 0.0)),
            "feedback_count": int((item.get("outcome") or {}).get("feedback_count", 0)),
            "success": bool((item.get("outcome") or {}).get("success", False)),
        }
        for item in reinforcement_inputs
    ]
    result["reinforcement_updates"] = apply_reinforcement_fn(engine_self, reinforcement_inputs)
    return result

# =============================================================================
# 主链反馈入口
# =============================================================================

def _record_workflow_feedback(
    engine_self,
    task_id: str,
    strategy_plan: Dict,
    task_records: List[Any],
    state_history: List[Dict[str, Any]],
    rollback_results: List[Dict[str, Any]],
    execution_config: Dict[str, Any],
    read_json_store_fn: Callable = None,
    write_json_store_fn: Callable = None,
) -> Dict[str, Any]:
    """
    执行阶段 PDCA 反馈记录器.

    闭环机制:
    - P(Plan): 从 strategy_plan 提取计划节点
    - D(Do): 记录每个任务的实际执行结果
    - C(Check): 对比 plan vs actual,记录偏差
    - A(Act): generate改进建议,回写到经验库
    """
    planned_tasks = set(strategy_plan.get("planned_tasks", []))
    completed_tasks = {r.task_name for r in task_records if r.status == "completed"}
    failed_tasks = {r.task_name for r in task_records if r.status == "failed"}
    blocked_tasks = {r.task_name for r in task_records if r.status == "blocked"}

    # Check: 计划 vs 实际偏差分析
    on_plan = planned_tasks & completed_tasks
    off_plan = planned_tasks - completed_tasks  # 计划但未完成
    extra_done = completed_tasks - planned_tasks  # 计划外完成

    # 状态转换效率分析
    total_retries = sum(r.attempts - 1 for r in task_records)

    # Act: generate改进建议
    lessons = []
    suggestions = []

    if failed_tasks:
        lessons.append(f"失败任务: {', '.join(failed_tasks)}")
        suggestions.append("排查失败任务的依赖关系与前置条件")
    if blocked_tasks:
        lessons.append(f"阻塞任务: {', '.join(blocked_tasks)}")
        suggestions.append("优化任务依赖拓扑,消除循环依赖")
    if rollback_results:
        lessons.append(f"触发回滚 {len(rollback_results)} 次")
        suggestions.append("增强任务前置校验,减少回滚风险")
    if completed_tasks:
        lessons.append(f"完成 {len(completed_tasks)}/{len(planned_tasks)} 个计划任务")
        suggestions.append("复用成功执行路径,固化到可复用动作库")

    if not lessons:
        lessons.append("工作流无执行记录,请检查输入strategy计划")

    # 计算工作流质量metrics
    total = len(task_records)
    success_ratio = len(completed_tasks) / total if total > 0 else 0.0
    workflow_quality = success_ratio * 0.7 + (1 - total_retries / max(total, 1)) * 0.3

    workflow_metrics = {
        "task_id": task_id,
        "planned": len(planned_tasks),
        "completed": len(completed_tasks),
        "failed": len(failed_tasks),
        "blocked": len(blocked_tasks),
        "on_plan": len(on_plan),
        "off_plan": len(off_plan),
        "extra_done": len(extra_done),
        "total_retries": total_retries,
        "rollback_count": len(rollback_results),
        "success_ratio": round(success_ratio, 4),
        "workflow_quality": round(workflow_quality, 4),
        "lessons_learned": lessons,
        "improvement_suggestions": suggestions[:3],
    }

    # 回写到经验库(关键:让后续调用可复用)
    if read_json_store_fn is None or write_json_store_fn is None:
        return workflow_metrics

    try:
        experience_record = {
            "task_id": task_id,
            "task_description": strategy_plan.get("task_description", task_id),
            "task_type": strategy_plan.get("task_type", "workflow_execution"),
            "keywords": list(planned_tasks)[:10],
            "overall_score": round(workflow_quality, 2),
            "lessons_learned": lessons,
            "reusable_actions": suggestions,
            "state_transitions": state_history[-20:] if state_history else [],
            "execution_metrics": {
                "success_ratio": workflow_metrics["success_ratio"],
                "retry_count": total_retries,
                "rollback_count": len(rollback_results),
            },
        }
        experiences = read_json_store_fn(getattr(engine_self, "experience_store_path", None), [])
        experiences.append(experience_record)
        experiences = experiences[-100:]
        write_json_store_fn(getattr(engine_self, "experience_store_path", None), experiences)
        logger.info(f"[闭环] 工作流反馈已写入经验库: {task_id} (quality={workflow_quality:.2f})")
    except Exception as exc:
        logger.warning(f"[闭环] 经验库写入失败: {exc}")

    return workflow_metrics

def _record_learning_feedback(
    engine_self,
    workflow_task_id: str,
    task_records: List[Any],
    build_workflow_entries_fn: Callable = None,
    submit_feedback_fn: Callable = None,
) -> Dict[str, Any]:
    """主链反馈入口:执行反馈先入管道,再进强化学习."""
    if build_workflow_entries_fn is None:
        build_workflow_entries_fn = lambda sid, recs: _build_workflow_feedback_entries(engine_self, sid, recs)
    if submit_feedback_fn is None:
        submit_feedback_fn = lambda f: _submit_feedback_entries(engine_self, f)

    raw_feedbacks = build_workflow_entries_fn(workflow_task_id, task_records)
    learning_feedback = submit_feedback_fn(raw_feedbacks)
    learning_feedback["feedback_tasks"] = len(
        [record for record in task_records if record.status in {"completed", "failed", "blocked"}]
    )
    return learning_feedback

def _record_evaluation_learning_feedback(
    engine_self,
    execution_report: Dict[str, Any],
    evaluation_report: Dict[str, Any],
    build_eval_entries_fn: Callable = None,
    submit_feedback_fn: Callable = None,
) -> Dict[str, Any]:
    """把效果评估折算成第二层质量反馈,继续回写强化学习."""
    if build_eval_entries_fn is None:
        build_eval_entries_fn = lambda er, ev: _build_evaluation_feedback_entries(
            engine_self, er, ev,
            clamp_fn=_clamp_unit_score,
            score_to_rating_fn=_score_to_rating_value,
            task_outcome_anchor_fn=_task_outcome_anchor,
        )
    if submit_feedback_fn is None:
        submit_feedback_fn = lambda f: _submit_feedback_entries(engine_self, f)

    raw_feedbacks, score_model = build_eval_entries_fn(execution_report, evaluation_report)
    learning_feedback = submit_feedback_fn(raw_feedbacks)
    learning_feedback["feedback_tasks"] = len(raw_feedbacks)
    learning_feedback["score_model"] = score_model
    return learning_feedback

def record_user_feedback(
    engine_self,
    task_id: str,
    strategy: str,
    feedback_type: str,
    value: Any,
    task_type: str = "workflow_execution",
    user_id: str = "default",
    session_id: str = "",
    submit_feedback_fn: Callable = None,
) -> Dict[str, Any]:
    """供主链外部调用的显式反馈入口,支持评分/采纳/corrective即时进入学习闭环."""
    if not task_id or not strategy or not feedback_type:
        return {
            "accepted": False,
            "reason": "task_id,strategy,feedback_type 不能为空",
            "feedback_pipeline": {"received": 0, "synced": 0, "errors": 0, "feedback_ids": []},
            "normalized_feedbacks": [],
            "reinforcement_inputs": [],
            "reinforcement_updates": [],
        }

    if submit_feedback_fn is None:
        submit_feedback_fn = lambda f: _submit_feedback_entries(engine_self, f)

    feedback_result = submit_feedback_fn([
        {
            "task_id": task_id,
            "task_type": task_type,
            "strategy": strategy,
            "type": feedback_type,
            "value": value,
            "session_id": session_id or task_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
        }
    ])
    feedback_result["accepted"] = feedback_result["feedback_pipeline"]["received"] > 0
    feedback_result["task_id"] = task_id
    feedback_result["strategy"] = strategy
    feedback_result["feedback_type"] = feedback_type
    return feedback_result

def _module_record_validation_learning(
    somn_core,
    execution_report: Dict[str, Any],
    evaluation_report: Dict[str, Any],
) -> None:
    """将验证学习事件写入 neural_system.learning."""
    try:
        summary = execution_report.get("execution_summary", {})
        validation_result = {
            "original_confidence": 0.5,
            "passed": evaluation_report.get("evaluation_summary", {}).get("overall_score", 0) >= 0.6,
            "sample_size": max(1, int(summary.get("total_tasks", 0))),
            "effect_size": evaluation_report.get("evaluation_summary", {}).get("overall_score", 0),
            "p_value": max(0.01, 1 - evaluation_report.get("evaluation_summary", {}).get("overall_score", 0))
        }
        somn_core._ensure_layers()
        event = somn_core.neural_system.learning.learn_from_validation(
            hypothesis_id=f"strategy_{execution_report.get('based_on_strategy')}",
            validation_result=validation_result
        )
        somn_core.neural_system.learning.save_learning_event(event)
    except Exception as exc:
        logger.warning(f"⚠️ 学习事件写入失败: {str(exc)}")

