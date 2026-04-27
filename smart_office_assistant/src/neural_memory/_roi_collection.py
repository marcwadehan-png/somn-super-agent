# -*- coding: utf-8 -*-
"""ROI追踪器 - 采集接口

__all__ = [
    'record_interaction_impl',
    'record_user_feedback_impl',
    'record_validation_result_impl',
    'track_task_complete_impl',
    'track_task_start_impl',
    'track_workflow_completion_impl',
]

track_task_start / record_interaction / track_task_complete /
record_user_feedback / record_validation_result / track_workflow_completion
"""

from datetime import datetime
from typing import Dict, List, Optional, Any

from .roi_types import MetricCategory, FeedbackSource, ROIRecord

def track_task_start_impl(core, task_id: str, task_type: str,
                         strategy: str = "", estimated_minutes: float = 0.0,
                         workflow_id: str = "", scope: str = "task",
                         strategy_combo_id: str = "",
                         strategy_combo: Optional[List[str]] = None) -> str:
    """记录任务开始"""
    core._active_tasks[task_id] = {
        "task_type": task_type,
        "strategy": strategy,
        "estimated_minutes": estimated_minutes,
        "start_time": datetime.now(),
        "interactions": [],
        "workflow_id": workflow_id,
        "scope": scope or "task",
        "strategy_combo_id": strategy_combo_id,
        "strategy_combo": core._normalize_strategy_combo(strategy_combo),
    }
    return task_id

def record_interaction_impl(core, task_id: str, interaction_type: str,
                            duration_seconds: float = 0,
                            metadata: Dict = None) -> bool:
    """记录任务进行中的交互事件"""
    if task_id not in core._active_tasks:
        return False

    core._active_tasks[task_id]["interactions"].append({
        "type": interaction_type,
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration_seconds,
        "metadata": metadata or {}
    })
    return True

def track_task_complete_impl(core, task_id: str,
                             outcome: Dict[str, Any]) -> Optional[str]:
    """记录任务完成"""
    if task_id not in core._active_tasks:
        return None

    start_data = core._active_tasks.pop(task_id)

    # 计算投入
    start_time = start_data["start_time"]
    actual_minutes = (datetime.now() - start_time).total_seconds() / 60.0
    interaction_count = len(start_data["interactions"])

    estimated = start_data.get("estimated_minutes", actual_minutes)
    time_saved = max(0, estimated - actual_minutes)

    # 计算产出
    quality = outcome.get("quality_score", 0.5)
    adopted = outcome.get("adopted", False)
    error_count = outcome.get("error_count", 0)

    # 产出量化
    output_value = core._quantify_output(
        quality=quality,
        time_saved=time_saved,
        adopted=adopted,
        error_count=error_count
    )

    # 投入量化
    input_cost = core._quantify_input(
        actual_minutes=actual_minutes,
        interaction_count=interaction_count,
        task_type=start_data["task_type"]
    )

    # ROI计算
    roi_ratio = core._calculate_roi(output_value, input_cost)
    efficiency_score = core._calculate_efficiency(
        quality, time_saved, actual_minutes, adopted
    )

    # 查找关联反馈
    feedbacks = core._feedback_cache.pop(task_id, [])
    feedback_score = core._aggregate_feedback(feedbacks)

    # 创建记录
    record_id = f"ROI_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    record = ROIRecord(
        record_id=record_id,
        timestamp=datetime.now().isoformat(),
        category=core._infer_category(start_data["task_type"]),
        source=FeedbackSource.USER_IMPLICIT,
        input_metrics={
            "actual_minutes": actual_minutes,
            "interaction_count": interaction_count,
            "estimated_minutes": estimated,
            "cost_estimate": input_cost,
        },
        output_metrics={
            "quality_score": quality,
            "time_saved_minutes": time_saved,
            "adopted": float(adopted),
            "error_count": error_count,
            "output_value": output_value,
            "feedback_score": feedback_score,
        },
        roi_ratio=roi_ratio,
        efficiency_score=efficiency_score,
        confidence=0.5,
        task_type=start_data["task_type"],
        strategy_used=start_data["strategy"],
        workflow_id=start_data.get("workflow_id", ""),
        scope=str(start_data.get("scope", "task") or "task"),
        strategy_combo_id=start_data.get("strategy_combo_id", ""),
        strategy_combo=core._normalize_strategy_combo(start_data.get("strategy_combo", [])),
    )

    core._records.append(record)
    core._save_record(record)
    return record_id

def record_user_feedback_impl(core, task_id: str, feedback: Dict[str, Any]) -> bool:
    """记录用户反馈"""
    if "type" not in feedback:
        return False

    if task_id not in core._feedback_cache:
        core._feedback_cache[task_id] = []

    fb_entry = {
        **feedback,
        "timestamp": datetime.now().isoformat(),
    }
    core._feedback_cache[task_id].append(fb_entry)

    # 同时更新历史记录的反馈分数
    for record in reversed(core._records):
        if record.task_type == feedback.get("task_type", ""):
            core._update_record_feedback(record, feedback)
            break

    return True

def record_validation_result_impl(core, hypothesis_id: str, result: Dict[str, Any]) -> Optional[str]:
    """记录系统验证结果"""
    record_id = f"ROI_VAL_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    # 将验证结果转化为ROI记录
    output_value = 1.0 if result["passed"] else 0.0
    if result["passed"]:
        output_value += min(0.5, result.get("effect_size", 0) * 0.5)

    input_cost = result.get("sample_size", 100) / 10.0

    record = ROIRecord(
        record_id=record_id,
        timestamp=datetime.now().isoformat(),
        category=MetricCategory.QUALITY_IMPROVEMENT,
        source=FeedbackSource.SYSTEM_VALIDATION,
        input_metrics={"validation_runs": 1, "sample_size": result.get("sample_size", 0)},
        output_metrics={
            "passed": float(result["passed"]),
            "effect_size": result.get("effect_size", 0),
            "p_value": result.get("p_value", 1.0),
        },
        roi_ratio=core._calculate_roi(output_value, max(0.1, input_cost)),
        efficiency_score=output_value,
        confidence=core._calculate_validation_confidence(result),
        task_type=f"validation_{hypothesis_id}",
    )

    core._records.append(record)
    core._save_record(record)
    return record_id

def track_workflow_completion_impl(core,
                                  workflow_id: str,
                                  outcome: Dict[str, Any],
                                  strategy_combo: Optional[List[str]] = None,
                                  strategy_combo_id: str = "") -> Dict[str, Any]:
    """将同一工作流下的任务级 ROI 聚合为工作流级 / strategy组合级 ROI"""
    if not workflow_id:
        return {
            "status": "invalid_workflow_id",
            "workflow_id": workflow_id,
            "workflow_record_id": "",
            "strategy_combo_record_id": "",
        }

    child_records = [
        record for record in core._records
        if record.workflow_id == workflow_id and str(record.scope or "task") == "task"
    ]
    if not child_records:
        return {
            "status": "no_task_records",
            "workflow_id": workflow_id,
            "workflow_record_id": "",
            "strategy_combo_record_id": "",
            "task_record_count": 0,
        }

    combo = core._normalize_strategy_combo(strategy_combo or outcome.get("strategy_combo", []))
    combo_id = strategy_combo_id or core._build_strategy_combo_id(combo)
    aggregated = core._aggregate_scope_metrics(child_records)

    workflow_record_id = f"ROI_WF_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    workflow_record = ROIRecord(
        record_id=workflow_record_id,
        timestamp=datetime.now().isoformat(),
        category=MetricCategory.TASK_COMPLETION,
        source=FeedbackSource.COMPARATIVE,
        input_metrics=aggregated["input_metrics"],
        output_metrics={
            **aggregated["output_metrics"],
            "completed_tasks": int(outcome.get("completed", aggregated["completed_tasks"])),
            "failed_tasks": int(outcome.get("failed", aggregated["failed_tasks"])),
            "blocked_tasks": int(outcome.get("blocked", aggregated["blocked_tasks"])),
            "success_ratio": round(float(outcome.get("success_ratio", aggregated["success_ratio"]) or aggregated["success_ratio"]), 4),
        },
        roi_ratio=aggregated["roi_ratio"],
        efficiency_score=aggregated["efficiency_score"],
        confidence=aggregated["confidence"],
        task_type="workflow_execution",
        strategy_used=combo_id or "workflow::aggregate",
        notes=f"workflow aggregation from {len(child_records)} task records",
        workflow_id=workflow_id,
        scope="workflow",
        strategy_combo_id=combo_id,
        strategy_combo=combo,
    )
    core._records.append(workflow_record)
    core._save_record(workflow_record)

    combo_record_id = ""
    if len(combo) >= 2:
        combo_record_id = f"ROI_SC_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        combo_record = ROIRecord(
            record_id=combo_record_id,
            timestamp=datetime.now().isoformat(),
            category=MetricCategory.TASK_COMPLETION,
            source=FeedbackSource.COMPARATIVE,
            input_metrics=aggregated["input_metrics"],
            output_metrics={
                **aggregated["output_metrics"],
                "completed_tasks": int(outcome.get("completed", aggregated["completed_tasks"])),
                "failed_tasks": int(outcome.get("failed", aggregated["failed_tasks"])),
                "blocked_tasks": int(outcome.get("blocked", aggregated["blocked_tasks"])),
                "success_ratio": round(float(outcome.get("success_ratio", aggregated["success_ratio"]) or aggregated["success_ratio"]), 4),
                "combo_size": len(combo),
            },
            roi_ratio=aggregated["roi_ratio"],
            efficiency_score=aggregated["efficiency_score"],
            confidence=aggregated["confidence"],
            task_type="strategy_combo_execution",
            strategy_used=combo_id,
            notes=f"strategy combo aggregation from {len(child_records)} task records",
            workflow_id=workflow_id,
            scope="strategy_combo",
            strategy_combo_id=combo_id,
            strategy_combo=combo,
        )
        core._records.append(combo_record)
        core._save_record(combo_record)

    return {
        "status": "ok",
        "workflow_id": workflow_id,
        "workflow_record_id": workflow_record_id,
        "strategy_combo_record_id": combo_record_id,
        "task_record_count": len(child_records),
        "strategy_combo": combo,
        "strategy_combo_id": combo_id,
    }
