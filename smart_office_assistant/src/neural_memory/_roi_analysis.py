# -*- coding: utf-8 -*-
"""ROI追踪器 - 分析接口

__all__ = [
    'get_baseline_impl',
    'get_period_roi_impl',
    'get_recent_feedbacks_impl',
    'get_strategy_combo_roi_impl',
    'get_strategy_roi_impl',
    'get_workflow_roi_impl',
]

get_period_roi / get_strategy_roi / get_workflow_roi /
get_strategy_combo_roi / get_recent_feedbacks / get_baseline
"""

from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import statistics

from .roi_types import PeriodROI

def get_period_roi_impl(core, period: str = None) -> PeriodROI:
    """获取指定周期的ROI汇总"""
    if period is None:
        period = core._get_current_period()

    start_date, end_date = core._parse_period(period)

    records = [r for r in core._records
               if start_date <= datetime.fromisoformat(r.timestamp) <= end_date]

    if not records:
        return PeriodROI(
            period=period,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )

    # 汇总计算
    total_time = sum(r.input_metrics.get("actual_minutes", 0) for r in records)
    total_cost = sum(r.input_metrics.get("cost_estimate", 0) for r in records)
    total_saved = sum(r.output_metrics.get("time_saved_minutes", 0) for r in records)
    tasks_completed = sum(1 for r in records if r.output_metrics.get("adopted", 0) > 0)
    quality_avg = statistics.mean(r.output_metrics.get("quality_score", 0.5) for r in records)

    # ROI比率
    output_total = sum(r.output_metrics.get("output_value", 0) for r in records)
    roi_ratio = core._calculate_roi(output_total, max(0.1, total_cost))

    # 趋势判断
    trend = core._calculate_trend(records, start_date)

    # 置信区间
    if len(records) >= core.params["min_records_for_confidence"]:
        scores = [r.efficiency_score for r in records]
        mean = statistics.mean(scores)
        stdev = statistics.stdev(scores) if len(scores) > 1 else 0
        conf_band = (max(0, mean - 1.96 * stdev), min(1, mean + 1.96 * stdev))
        avg_confidence = statistics.mean(r.confidence for r in records)
        # 更新记录置信度
        for r in records:
            r.confidence = avg_confidence
    else:
        conf_band = (0.0, 1.0)

    return PeriodROI(
        period=period,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        total_time_invested_minutes=total_time,
        total_cost_estimate=total_cost,
        tasks_completed=tasks_completed,
        tasks_quality_avg=quality_avg,
        time_saved_minutes=total_saved,
        overall_roi_ratio=roi_ratio,
        efficiency_trend=trend,
        confidence_band=conf_band,
        records=[asdict(r) for r in records],
    )

def get_strategy_roi_impl(core, strategy: str) -> Dict[str, Any]:
    """获取特定strategy的ROI表现"""
    records = [
        r for r in core._records
        if r.strategy_used == strategy and str(r.scope or "task") == "task"
    ]
    summary = core._build_roi_summary(records)
    if summary.get("status") == "no_data":
        return {"status": "no_data", "strategy": strategy}
    return {
        **summary,
        "strategy": strategy,
        "q_value": round(summary.get("avg_efficiency_score", 0.5), 3),
    }

def get_workflow_roi_impl(core, workflow_id: str) -> Dict[str, Any]:
    """获取某个工作流级别的 ROI 聚合结果"""
    records = [
        r for r in core._records
        if r.workflow_id == workflow_id and str(r.scope or "task") == "workflow"
    ]
    summary = core._build_roi_summary(records)
    if summary.get("status") == "no_data":
        return {"status": "no_data", "workflow_id": workflow_id, "scope": "workflow"}
    return {**summary, "workflow_id": workflow_id, "scope": "workflow"}

def get_strategy_combo_roi_impl(core,
                               strategy_combo_id: str = "",
                               strategy_combo: Optional[List[str]] = None) -> Dict[str, Any]:
    """获取某个strategy组合级别的 ROI 聚合结果"""
    combo = core._normalize_strategy_combo(strategy_combo)
    combo_id = strategy_combo_id or core._build_strategy_combo_id(combo)
    records = [
        r for r in core._records
        if str(r.scope or "task") == "strategy_combo"
        and (r.strategy_combo_id == combo_id or (combo and core._normalize_strategy_combo(r.strategy_combo) == combo))
    ]
    summary = core._build_roi_summary(records)
    if summary.get("status") == "no_data":
        return {
            "status": "no_data",
            "scope": "strategy_combo",
            "strategy_combo_id": combo_id,
            "strategy_combo": combo,
        }
    return {
        **summary,
        "scope": "strategy_combo",
        "strategy_combo_id": combo_id,
        "strategy_combo": combo or summary.get("strategy_combo", []),
    }

def get_recent_feedbacks_impl(core, task_id: str = None,
                             limit: int = 20) -> List[Dict]:
    """获取最近反馈"""
    all_feedbacks = []
    for fb_list in core._feedback_cache.values():
        if task_id is None or fb_list[0].get("task_id") == task_id:
            all_feedbacks.extend(fb_list)

    # 合并历史记录中的反馈
    for record in core._records:
        fb_score = record.output_metrics.get("feedback_score", 0)
        if fb_score > 0:
            all_feedbacks.append({
                "type": "historical",
                "value": fb_score,
                "timestamp": record.timestamp,
                "task_type": record.task_type,
                "strategy": record.strategy_used,
            })

    all_feedbacks.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return all_feedbacks[:limit]

def get_baseline_impl(core) -> Dict[str, float]:
    """获取基线metrics"""
    task_records = [r for r in core._records if str(r.scope or "task") == "task"]
    if len(task_records) < core.params["min_records_for_confidence"]:
        return {
            "avg_efficiency": 0.5,
            "avg_roi": 1.0,
            "adopt_rate": 0.5,
            "avg_quality": 0.5,
            "confidence": 0.0,
            "note": f"数据不足({len(task_records)}/{core.params['min_records_for_confidence']}),使用默认值"
        }

    recent = task_records[-core.params["min_records_for_confidence"]:]
    return {
        "avg_efficiency": statistics.mean(r.efficiency_score for r in recent),
        "avg_roi": statistics.mean(r.roi_ratio for r in recent),
        "adopt_rate": statistics.mean(r.output_metrics.get("adopted", 0) for r in recent),
        "avg_quality": statistics.mean(r.output_metrics.get("quality_score", 0.5) for r in recent),
        "confidence": statistics.mean(r.confidence for r in recent),
        "note": f"基于最近{len(recent)}条任务级记录"
    }
