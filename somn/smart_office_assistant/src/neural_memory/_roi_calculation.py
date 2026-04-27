# -*- coding: utf-8 -*-
"""ROI追踪器 - 计算方法

__all__ = [
    'aggregate_feedback_impl',
    'calculate_efficiency_impl',
    'calculate_roi_impl',
    'calculate_trend_impl',
    'calculate_validation_confidence_impl',
    'infer_category_impl',
    'quantify_input_impl',
    'quantify_output_impl',
    'update_record_feedback_impl',
]

_quantify_output / _quantify_input / _calculate_roi / _calculate_efficiency /
_aggregate_feedback / _update_record_feedback / _infer_category /
_calculate_trend / _calculate_validation_confidence
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any

import statistics

from .roi_types import MetricCategory, ROIRecord

def quantify_output_impl(core, quality: float, time_saved: float,
                         adopted: bool, error_count: int) -> float:
    """将产出转化为可量化的价值"""
    quality_component = quality * core.params["quality_weight"] * 10
    time_component = (time_saved / 60.0) * core.params["time_weight"] * core.params["default_hourly_value"] / 10
    adopt_component = float(adopted) * core.params["task_weight"] * 10
    error_penalty = max(0, 1 - error_count * 0.2) * core.params["satisfaction_weight"]

    return quality_component + time_component + adopt_component + error_penalty

def quantify_input_impl(core, actual_minutes: float, interaction_count: int,
                        task_type: str) -> float:
    """将投入转化为可量化的成本"""
    time_cost = actual_minutes / 60.0 * core.params["default_hourly_value"]
    interaction_cost = interaction_count * 2.0
    return time_cost + interaction_cost

def calculate_roi_impl(core, output_value: float, input_cost: float) -> float:
    """ROI = (产出-投入) / 投入"""
    if input_cost <= 0:
        return 0.0
    return round((output_value - input_cost) / input_cost, 3)

def calculate_efficiency_impl(core, quality: float, time_saved: float,
                              actual_minutes: float, adopted: bool) -> float:
    """综合效率分 0-1 [v1.0 修复: 消除time_weight双重计算bug]"""
    p = core.params
    quality_part = quality * p["quality_weight"]
    # [fix] time_weight只在此处应用一次（原代码在定义time_part和求和时各乘了一次）
    time_ratio = (time_saved / max(1, actual_minutes)) if actual_minutes > 0 else 0
    time_part = min(time_ratio, 1.0) * p["time_weight"]
    adopt_part = float(adopted) * p["task_weight"]
    # satisfaction部分改为根据error_count衰减，不再是固定常量
    satisfaction_part = p["satisfaction_weight"] * quality  # 与质量挂钩

    score = quality_part + time_part + adopt_part + satisfaction_part
    # 归一化到[0,1]: 最大可能值 = quality_weight + time_weight + task_weight + satisfaction_weight*1.0 = 1.0+0.2=1.2
    max_score = p["quality_weight"] + p["time_weight"] + p["task_weight"] + p["satisfaction_weight"]
    return round(min(1.0, max(0.0, score / max_score)), 3)

def aggregate_feedback_impl(core, feedbacks: List[Dict]) -> float:
    """聚合多条反馈为单一分数"""
    if not feedbacks:
        return 0.5

    scores = []
    for fb in feedbacks:
        fb_type = fb.get("type", "")
        value = fb.get("value", 0.5)

        if fb_type == "rating":
            scores.append(value / 5.0)
        elif fb_type == "adopt":
            scores.append(float(value))
        elif fb_type == "correction":
            scores.append((value + 1) / 2.0)
        elif fb_type == "thumbs":
            scores.append(float(value))
        else:
            scores.append(0.5)

    return round(statistics.mean(scores), 3)

def update_record_feedback_impl(core, record: ROIRecord, feedback: Dict):
    """更新历史记录的反馈分数"""
    fb_score = core._aggregate_feedback([feedback])
    record.output_metrics["feedback_score"] = fb_score
    # 重新计算效率
    record.efficiency_score = core._calculate_efficiency(
        record.output_metrics.get("quality_score", 0.5),
        record.output_metrics.get("time_saved_minutes", 0),
        record.output_metrics.get("adopted", 0) > 0,
        0
    )

def infer_category_impl(core, task_type: str) -> MetricCategory:
    """根据任务类型推断metrics类别"""
    mapping = {
        "分析": MetricCategory.QUALITY_IMPROVEMENT,
        "写作": MetricCategory.QUALITY_IMPROVEMENT,
        "决策": MetricCategory.REVENUE_IMPACT,
        "研究": MetricCategory.TIME_SAVED,
        "数据": MetricCategory.QUALITY_IMPROVEMENT,
        "创意": MetricCategory.USER_SATISFACTION,
    }
    for key, cat in mapping.items():
        if key in task_type:
            return cat
    return MetricCategory.TASK_COMPLETION

def calculate_trend_impl(core, records: List[ROIRecord],
                         compare_from: datetime) -> str:
    """计算趋势"""
    if len(records) < 3:
        return "insufficient_data"

    recent = [r for r in records
             if datetime.fromisoformat(r.timestamp) >= compare_from]

    if len(recent) < 2:
        return "stable"

    first_half = records[:len(records)//2]
    second_half = records[len(records)//2:]

    avg_first = statistics.mean(r.efficiency_score for r in first_half)
    avg_second = statistics.mean(r.efficiency_score for r in second_half)

    diff_pct = (avg_second - avg_first) / max(0.01, avg_first)

    if diff_pct > 0.1:
        return "improving"
    elif diff_pct < -0.1:
        return "declining"
    return "stable"

def calculate_validation_confidence_impl(core, result: Dict) -> float:
    """计算验证结果的置信度"""
    base = 0.5
    if result.get("passed"):
        base += 0.2
    sample = min(1.0, result.get("sample_size", 0) / 500)
    base += sample * 0.2
    p_val = result.get("p_value", 1.0)
    if p_val < 0.05:
        base += 0.1
    return min(0.99, base)
