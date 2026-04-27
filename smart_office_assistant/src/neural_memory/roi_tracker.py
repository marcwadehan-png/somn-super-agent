"""
ROI效果追踪系统 - 兼容层
ROI Tracker - Compatibility Layer

原始模块拆分后，此文件保留所有公共符号的向后兼容导出。
新代码应直接导入拆分后的子模块:
  - roi_types: MetricCategory, FeedbackSource, ROIRecord, PeriodROI
  - roi_tracker_core: ROITracker
  - roi_reports: generate_roi_report, _generate_insights
"""

from .roi_types import (
    MetricCategory,
    FeedbackSource,
    ROIRecord,
    PeriodROI,
)
from .roi_tracker_core import ROITracker
from .roi_reports import generate_roi_report, _generate_insights

__all__ = [
    "MetricCategory",
    "FeedbackSource",
    "ROIRecord",
    "PeriodROI",
    "ROITracker",
    "generate_roi_report",
    "_generate_insights",
]
