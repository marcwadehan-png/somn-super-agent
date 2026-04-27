"""反馈学习模块 - 提供反馈收集和强化学习能力"""

from __future__ import annotations
from typing import Any

__all__ = ['FeedbackPipeline', 'ReinforcementLearner']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'FeedbackPipeline':
        from .pipeline import FeedbackPipeline
        return FeedbackPipeline
    if name == 'ReinforcementLearner':
        from .reinforcement import ReinforcementLearner
        return ReinforcementLearner
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
