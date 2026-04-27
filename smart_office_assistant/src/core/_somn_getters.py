"""
__all__ = [
    'run_get_feedback_pipeline',
    'run_get_reinforcement_trigger',
    'run_get_roi_tracker',
]

SomnCore 懒加载 getter 委托模块
处理 _get_feedback_pipeline, _get_reinforcement_trigger, _get_roi_tracker
"""

import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

def run_get_feedback_pipeline(core) -> Optional[Any]:
    """懒加载反馈管道,unified接住显式/隐式反馈."""
    if core._feedback_pipeline_unavailable:
        return None

    if core._feedback_pipeline is not None:
        return core._feedback_pipeline

    try:
        from ..neural_memory.feedback_pipeline import FeedbackPipeline

        core._feedback_pipeline = FeedbackPipeline(
            str(core.base_path / "data" / "learning" / "feedback_pipeline")
        )
        return core._feedback_pipeline
    except Exception as exc:
        core._feedback_pipeline_unavailable = True
        logger.warning(f"反馈管道init失败,已跳过本轮反馈整合: {exc}")
        return None

def run_get_reinforcement_trigger(core) -> Optional[Any]:
    """懒加载强化学习触发器,避免init阶段硬依赖."""
    if core._reinforcement_feedback_unavailable:
        return None

    if core._reinforcement_trigger is not None:
        return core._reinforcement_trigger

    try:
        from ..neural_memory.reinforcement_trigger import ReinforcementTrigger

        core._reinforcement_trigger = ReinforcementTrigger(str(core.base_path / "data" / "learning"))
        return core._reinforcement_trigger
    except Exception as exc:
        core._reinforcement_feedback_unavailable = True
        logger.warning(f"强化学习触发器init失败,已跳过本轮反馈写回: {exc}")
        return None

def run_get_roi_tracker(core) -> Optional[Any]:
    """懒加载 ROI 追踪器,让执行效率/收益信号也能进入主链."""
    if core._roi_tracker_unavailable:
        return None

    if core._roi_tracker is not None:
        return core._roi_tracker

    try:
        from ..neural_memory.roi_tracker import ROITracker

        core._roi_tracker = ROITracker(str(core.base_path / "data" / "learning"))
        return core._roi_tracker
    except Exception as exc:
        core._roi_tracker_unavailable = True
        logger.warning(f"ROI 追踪器init失败,已跳过本轮 ROI 信号整合: {exc}")
        return None
