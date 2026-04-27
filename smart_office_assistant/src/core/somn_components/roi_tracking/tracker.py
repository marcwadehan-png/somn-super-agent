"""
__all__ = [
    'clamp_unit_score',
    'estimate_task_quality',
    'normalize_roi_ratio',
    'resolve_estimated_minutes',
    'trend_bias',
]

ROI追踪器 - 提供投入产出比追踪能力
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ROITracker:
    """ROI追踪器封装类"""

    def __init__(self, roi_tracker=None):
        self._tracker = roi_tracker

    @staticmethod
    def clamp_unit_score(value: float, default: float = 0.5) -> float:
        """把分值限制在 0~1"""
        return max(0.0, min(1.0, value if value is not None else default))

    @staticmethod
    def estimate_task_quality(record: Any) -> float:
        """把执行记录粗折算为质量分"""
        status = str(getattr(record, 'status', '') or '').lower()
        base_score = {"completed": 0.86, "failed": 0.22, "blocked": 0.35}.get(status, 0.5)
        retry_penalty = min(0.24, max(0, int(getattr(record, 'attempts', 0) or 0) - 1) * 0.08)
        result = getattr(record, 'result', {}) or {}
        tool_attempts = 1
        if isinstance(result, dict):
            try:
                tool_attempts = int(result.get("tool_attempts") or 1)
            except (TypeError, ValueError):
                tool_attempts = 1
        tool_penalty = min(0.1, max(0, tool_attempts - 1) * 0.05)
        error_penalty = 0.08 if getattr(record, 'last_error', None) and status != "completed" else 0.0
        return ROITracker.clamp_unit_score(base_score - retry_penalty - tool_penalty - error_penalty)

    @staticmethod
    def resolve_estimated_minutes(record: Any, execution_config: Dict[str, Any] = None) -> float:
        """尽量从任务参数或执行配置中推断预估耗时"""
        if execution_config:
            try:
                minutes = float(execution_config.get("estimated_minutes") or 0)
                if minutes > 0:
                    return round(minutes, 2)
            except (TypeError, ValueError):
                pass
        return 5.0

    @staticmethod
    def normalize_roi_ratio(value: Any, default: float = 0.5) -> float:
        """把 ROI ratio 平滑压到 0~1"""
        try:
            ratio = float(value)
        except (TypeError, ValueError):
            return ROITracker.clamp_unit_score(default, 0.5)

        clipped = max(-1.0, min(1.0, ratio))
        normalized = 0.5 + clipped * 0.25
        if ratio > 1.0:
            normalized += min(0.25, (ratio - 1.0) * 0.05)
        return ROITracker.clamp_unit_score(normalized, default)

    @staticmethod
    def trend_bias(trend: Any) -> float:
        """给 ROI 趋势一个小幅偏置"""
        trend_key = str(trend or "").lower()
        return {"improving": 0.05, "declining": -0.05}.get(trend_key, 0.0)
