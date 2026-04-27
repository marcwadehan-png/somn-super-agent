# -*- coding: utf-8 -*-
"""ROI追踪器 - 工具方法

__all__ = [
    'aggregate_scope_metrics_impl',
    'build_roi_summary_impl',
    'build_strategy_combo_id_impl',
    'get_current_period_impl',
    'normalize_strategy_combo_impl',
    'parse_period_impl',
]

_normalize_strategy_combo / _build_strategy_combo_id / _build_roi_summary /
_aggregate_scope_metrics / _get_current_period / _parse_period
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

import statistics

from .roi_types import ROIRecord

def normalize_strategy_combo_impl(core, strategy_combo: Optional[List[str]]) -> List[str]:
    """归一化strategy组合,去空值,去重并保持原顺序"""
    if not strategy_combo:
        return []

    raw_items = strategy_combo if isinstance(strategy_combo, list) else [strategy_combo]
    normalized = []
    seen = set()
    for item in raw_items:
        value = str(item or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    return normalized

def build_strategy_combo_id_impl(core, strategy_combo: Optional[List[str]]) -> str:
    """为strategy组合构建稳定 ID"""
    normalized = core._normalize_strategy_combo(strategy_combo)
    if not normalized:
        return ""
    return "combo::" + "||".join(sorted(normalized))

def build_roi_summary_impl(core, records: List[ROIRecord]) -> Dict[str, Any]:
    """对一组 ROIRecord 做统一聚合"""
    if not records:
        return {"status": "no_data", "sample_count": 0}

    scores = [r.efficiency_score for r in records]
    rois = [r.roi_ratio for r in records]
    adopted = [r.output_metrics.get("adopted", 0) for r in records]
    qualities = [r.output_metrics.get("quality_score", 0.5) for r in records]
    success_ratios = [r.output_metrics.get("success_ratio", r.output_metrics.get("adopted", 0.5)) for r in records]
    task_record_counts = [r.output_metrics.get("task_record_count", 0) for r in records if r.output_metrics.get("task_record_count") is not None]

    summary = {
        "sample_count": len(records),
        "avg_efficiency_score": round(statistics.mean(scores), 3),
        "avg_roi_ratio": round(statistics.mean(rois), 3),
        "adoption_rate": round(statistics.mean(adopted), 3),
        "avg_quality": round(statistics.mean(qualities), 3),
        "confidence": round(statistics.mean(r.confidence for r in records), 3),
        "last_used": max(r.timestamp for r in records),
        "trend": core._calculate_trend(records, datetime.now() - timedelta(days=7)),
        "success_ratio": round(statistics.mean(success_ratios), 3),
        "task_record_count": int(max(task_record_counts)) if task_record_counts else len(records),
    }

    latest = max(records, key=lambda item: item.timestamp)
    if latest.workflow_id:
        summary["workflow_id"] = latest.workflow_id
    if latest.strategy_combo_id:
        summary["strategy_combo_id"] = latest.strategy_combo_id
    if latest.strategy_combo:
        summary["strategy_combo"] = core._normalize_strategy_combo(latest.strategy_combo)
    return summary

def aggregate_scope_metrics_impl(core, records: List[ROIRecord]) -> Dict[str, Any]:
    """把多条任务级记录汇总为更高层级可复用的 ROI metrics"""
    total_actual_minutes = sum(float(r.input_metrics.get("actual_minutes", 0) or 0) for r in records)
    total_interactions = sum(float(r.input_metrics.get("interaction_count", 0) or 0) for r in records)
    total_estimated_minutes = sum(float(r.input_metrics.get("estimated_minutes", 0) or 0) for r in records)
    total_cost = sum(float(r.input_metrics.get("cost_estimate", 0) or 0) for r in records)
    total_time_saved = sum(float(r.output_metrics.get("time_saved_minutes", 0) or 0) for r in records)
    total_output_value = sum(float(r.output_metrics.get("output_value", 0) or 0) for r in records)
    total_errors = sum(int(r.output_metrics.get("error_count", 0) or 0) for r in records)
    completed_tasks = sum(1 for r in records if float(r.output_metrics.get("adopted", 0) or 0) > 0)
    failed_tasks = sum(1 for r in records if float(r.output_metrics.get("adopted", 0) or 0) <= 0)
    success_ratio = round(completed_tasks / len(records), 4) if records else 0.0
    avg_quality = statistics.mean(float(r.output_metrics.get("quality_score", 0.5) or 0.5) for r in records)
    roi_ratio = core._calculate_roi(total_output_value, max(0.1, total_cost))
    efficiency_score = core._calculate_efficiency(
        quality=avg_quality,
        time_saved=total_time_saved,
        actual_minutes=max(1.0, total_actual_minutes),
        adopted=success_ratio >= 0.5,
    )
    confidence = round(min(1.0, max(
        statistics.mean(float(r.confidence or 0) for r in records),
        len(records) / max(1.0, float(core.params["min_records_for_confidence"]))
    )), 3)

    return {
        "input_metrics": {
            "actual_minutes": round(total_actual_minutes, 4),
            "interaction_count": round(total_interactions, 4),
            "estimated_minutes": round(total_estimated_minutes, 4),
            "cost_estimate": round(total_cost, 4),
        },
        "output_metrics": {
            "quality_score": round(avg_quality, 4),
            "time_saved_minutes": round(total_time_saved, 4),
            "adopted": round(success_ratio, 4),
            "error_count": total_errors,
            "output_value": round(total_output_value, 4),
            "task_record_count": len(records),
        },
        "roi_ratio": roi_ratio,
        "efficiency_score": efficiency_score,
        "confidence": confidence,
        "success_ratio": success_ratio,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "blocked_tasks": 0,
    }

def get_current_period_impl(core) -> str:
    """获取当前周期标识"""
    now = datetime.now()
    return f"{now.year}-W{now.isocalendar()[1]:02d}"

def parse_period_impl(core, period: str) -> Tuple[datetime, datetime]:
    """解析周期为起止日期"""
    if "-W" in period:
        year, week = period.split("-W")
        year, week = int(year), int(week)
        # ISO周起始
        jan4 = datetime(year, 1, 4)
        start = jan4 + timedelta(weeks=week - 1, days=-jan4.weekday())
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    else:
        # 月份
        year, month = period.split("-")
        year, month = int(year), int(month)
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(year, month + 1, 1) - timedelta(seconds=1)
    return start, end
