"""
__all__ = [
    'generate_roi_report',
]

ROI 报告生成 - 独立报告函数与洞察生成
ROI Report Generation - Standalone report functions and insight generation
"""

from datetime import datetime
from dataclasses import asdict
from typing import Dict, List, Any

from .roi_types import PeriodROI
from .roi_tracker_core import ROITracker

def generate_roi_report(tracker: ROITracker = None,
                        period: str = None) -> Dict[str, Any]:
    """
    generateROI分析报告(供每日学习系统使用)

    Returns:
        完整的ROI分析报告
    """
    if tracker is None:
        tracker = ROITracker()

    period_roi = tracker.get_period_roi(period)
    baseline = tracker.get_baseline()

    # get所有strategy表现
    strategies = {}
    for record in tracker._records:
        if str(record.scope or "task") != "task":
            continue
        s = record.strategy_used
        if s and s not in strategies:
            strategies[s] = tracker.get_strategy_roi(s)

    return {
        "report_id": f"ROI_RPT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generated_at": datetime.now().isoformat(),
        "period": period_roi.period,
        "period_summary": asdict(period_roi),
        "baseline": baseline,
        "strategy_rankings": sorted(
            strategies.values(),
            key=lambda x: x.get("q_value", 0),
            reverse=True
        ) if strategies else [],
        "key_insights": _generate_insights(period_roi, baseline, strategies),
    }

def _generate_insights(period_roi: PeriodROI, baseline: Dict,
                       strategies: Dict) -> List[str]:
    """generate关键洞察"""
    insights = []

    if period_roi.tasks_completed > 0:
        insights.append(f"本周期完成任务 {period_roi.tasks_completed} 个")

    if period_roi.time_saved_minutes > 60:
        insights.append(f"累计节省 {period_roi.time_saved_minutes/60:.1f} 小时")

    if period_roi.efficiency_trend == "improving":
        insights.append("效率呈上升趋势")
    elif period_roi.efficiency_trend == "declining":
        insights.append("效率有所下滑,建议分析原因")

    if strategies:
        best = max(strategies.values(), key=lambda x: x.get("q_value", 0))
        worst = min(strategies.values(), key=lambda x: x.get("q_value", 0))
        insights.append(f"最优strategy: {best.get('strategy', 'N/A')} (Q={best.get('q_value', 0):.3f})")
        if best.get("q_value", 0) - worst.get("q_value", 0) > 0.2:
            insights.append(f"strategy差异显著,最优vs最差差距 {best.get('q_value', 0) - worst.get('q_value', 0):.3f}")

    return insights
