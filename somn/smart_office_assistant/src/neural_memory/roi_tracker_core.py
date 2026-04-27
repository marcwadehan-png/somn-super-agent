# -*- coding: utf-8 -*-
"""ROI 追踪器核心 - 兼容层 (v1.0)

__all__ = [
    'get_baseline',
    'get_period_roi',
    'get_recent_feedbacks',
    'get_strategy_combo_roi',
    'get_strategy_roi',
    'get_workflow_roi',
    'record_interaction',
    'record_user_feedback',
    'record_validation_result',
    'track_task_complete',
    'track_task_start',
    'track_workflow_completion',
]

重构后主文件仅保留向后兼容导入和 Thin Delegation。
子模块: _roi_collection / _roi_analysis / _roi_calculation /
       _roi_utils / _roi_storage
"""

import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import asdict
import statistics

from .roi_types import MetricCategory, FeedbackSource, ROIRecord, PeriodROI

# ── 子模块导入 ──────────────────────────────────────────
from ._roi_collection import (
    track_task_start_impl,
    record_interaction_impl,
    track_task_complete_impl,
    record_user_feedback_impl,
    record_validation_result_impl,
    track_workflow_completion_impl,
)
from ._roi_analysis import (
    get_period_roi_impl,
    get_strategy_roi_impl,
    get_workflow_roi_impl,
    get_strategy_combo_roi_impl,
    get_recent_feedbacks_impl,
    get_baseline_impl,
)
from ._roi_calculation import (
    quantify_output_impl,
    quantify_input_impl,
    calculate_roi_impl,
    calculate_efficiency_impl,
    aggregate_feedback_impl,
    update_record_feedback_impl,
    infer_category_impl,
    calculate_trend_impl,
    calculate_validation_confidence_impl,
)
from ._roi_utils import (
    normalize_strategy_combo_impl,
    build_strategy_combo_id_impl,
    build_roi_summary_impl,
    aggregate_scope_metrics_impl,
    get_current_period_impl,
    parse_period_impl,
)
from ._roi_storage import (
    serialize_record_impl,
    deserialize_record_impl,
    save_record_impl,
    load_records_impl,
)

class ROITracker:
    """
    ROI效果追踪器 (v1.0 委托层)

    建立效果数据采集管道,将每次strategy执行的结果量化,
    为强化学习引擎提供真实世界的反馈数据.
    """

    def __init__(self, base_path: str = None):
        from src.core.paths import LEARNING_DIR
        self.base_path = Path(base_path) if base_path else LEARNING_DIR / "roi_tracker"
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.records_path = self.base_path / "records"
        self.reports_path = self.base_path / "reports"
        self.records_path.mkdir(exist_ok=True)
        self.reports_path.mkdir(exist_ok=True)

        # 内存索引
        self._records: List[ROIRecord] = []
        self._active_tasks: Dict[str, Dict] = {}
        self._feedback_cache: Dict[str, List[Dict]] = {}

        # 加载历史记录
        self._load_records()

        # ROI计算参数
        self.params = {
            "min_records_for_confidence": 5,
            "baseline_period_days": 30,
            "default_hourly_value": 200.0,
            "quality_weight": 0.3,
            "time_weight": 0.3,
            "satisfaction_weight": 0.2,
            "task_weight": 0.2,
        }

    # ==================== 采集接口 ====================

    def track_task_start(self, task_id: str, task_type: str,
                         strategy: str = "", estimated_minutes: float = 0.0,
                         workflow_id: str = "", scope: str = "task",
                         strategy_combo_id: str = "",
                         strategy_combo: Optional[List[str]] = None) -> str:
        """记录任务开始 -- 委托自 _roi_collection."""
        return track_task_start_impl(
            self, task_id, task_type, strategy, estimated_minutes,
            workflow_id, scope, strategy_combo_id, strategy_combo)

    def record_interaction(self, task_id: str, interaction_type: str,
                          duration_seconds: float = 0,
                          metadata: Dict = None) -> bool:
        """记录任务交互 -- 委托自 _roi_collection."""
        return record_interaction_impl(self, task_id, interaction_type, duration_seconds, metadata)

    def track_task_complete(self, task_id: str,
                           outcome: Dict[str, Any]) -> Optional[str]:
        """记录任务完成 -- 委托自 _roi_collection."""
        return track_task_complete_impl(self, task_id, outcome)

    def record_user_feedback(self, task_id: str, feedback: Dict[str, Any]) -> bool:
        """记录用户反馈 -- 委托自 _roi_collection."""
        return record_user_feedback_impl(self, task_id, feedback)

    def record_validation_result(self, hypothesis_id: str, result: Dict[str, Any]) -> Optional[str]:
        """记录验证结果 -- 委托自 _roi_collection."""
        return record_validation_result_impl(self, hypothesis_id, result)

    def track_workflow_completion(self,
                                 workflow_id: str,
                                 outcome: Dict[str, Any],
                                 strategy_combo: Optional[List[str]] = None,
                                 strategy_combo_id: str = "") -> Dict[str, Any]:
        """聚合工作流ROI -- 委托自 _roi_collection."""
        return track_workflow_completion_impl(
            self, workflow_id, outcome, strategy_combo, strategy_combo_id)

    # ==================== 分析接口 ====================

    def get_period_roi(self, period: str = None) -> PeriodROI:
        """获取周期ROI -- 委托自 _roi_analysis."""
        return get_period_roi_impl(self, period)

    def get_strategy_roi(self, strategy: str) -> Dict[str, Any]:
        """获取策略ROI -- 委托自 _roi_analysis."""
        return get_strategy_roi_impl(self, strategy)

    def get_workflow_roi(self, workflow_id: str) -> Dict[str, Any]:
        """获取工作流ROI -- 委托自 _roi_analysis."""
        return get_workflow_roi_impl(self, workflow_id)

    def get_strategy_combo_roi(self,
                               strategy_combo_id: str = "",
                               strategy_combo: Optional[List[str]] = None) -> Dict[str, Any]:
        """获取策略组合ROI -- 委托自 _roi_analysis."""
        return get_strategy_combo_roi_impl(self, strategy_combo_id, strategy_combo)

    def get_recent_feedbacks(self, task_id: str = None,
                            limit: int = 20) -> List[Dict]:
        """获取最近反馈 -- 委托自 _roi_analysis."""
        return get_recent_feedbacks_impl(self, task_id, limit)

    def get_baseline(self) -> Dict[str, float]:
        """获取基线 -- 委托自 _roi_analysis."""
        return get_baseline_impl(self)

    # ==================== 私有方法 ====================

    def _quantify_output(self, quality: float, time_saved: float,
                         adopted: bool, error_count: int) -> float:
        return quantify_output_impl(self, quality, time_saved, adopted, error_count)

    def _quantify_input(self, actual_minutes: float, interaction_count: int,
                        task_type: str) -> float:
        return quantify_input_impl(self, actual_minutes, interaction_count, task_type)

    def _calculate_roi(self, output_value: float, input_cost: float) -> float:
        return calculate_roi_impl(self, output_value, input_cost)

    def _calculate_efficiency(self, quality: float, time_saved: float,
                              actual_minutes: float, adopted: bool) -> float:
        return calculate_efficiency_impl(self, quality, time_saved, actual_minutes, adopted)

    def _aggregate_feedback(self, feedbacks: List[Dict]) -> float:
        return aggregate_feedback_impl(self, feedbacks)

    def _update_record_feedback(self, record: ROIRecord, feedback: Dict):
        return update_record_feedback_impl(self, record, feedback)

    def _infer_category(self, task_type: str) -> MetricCategory:
        return infer_category_impl(self, task_type)

    def _calculate_trend(self, records: List[ROIRecord],
                         compare_from: datetime) -> str:
        return calculate_trend_impl(self, records, compare_from)

    def _calculate_validation_confidence(self, result: Dict) -> float:
        return calculate_validation_confidence_impl(self, result)

    def _normalize_strategy_combo(self, strategy_combo: Optional[List[str]]) -> List[str]:
        return normalize_strategy_combo_impl(self, strategy_combo)

    def _build_strategy_combo_id(self, strategy_combo: Optional[List[str]]) -> str:
        return build_strategy_combo_id_impl(self, strategy_combo)

    def _build_roi_summary(self, records: List[ROIRecord]) -> Dict[str, Any]:
        return build_roi_summary_impl(self, records)

    def _aggregate_scope_metrics(self, records: List[ROIRecord]) -> Dict[str, Any]:
        return aggregate_scope_metrics_impl(self, records)

    def _get_current_period(self) -> str:
        return get_current_period_impl(self)

    def _parse_period(self, period: str) -> Tuple[datetime, datetime]:
        return parse_period_impl(self, period)

    def _serialize_record(self, record: ROIRecord) -> Dict[str, Any]:
        return serialize_record_impl(self, record)

    def _deserialize_record(self, data: Dict[str, Any]) -> ROIRecord:
        return deserialize_record_impl(self, data)

    def _save_record(self, record: ROIRecord):
        return save_record_impl(self, record)

    def _load_records(self):
        return load_records_impl(self)
