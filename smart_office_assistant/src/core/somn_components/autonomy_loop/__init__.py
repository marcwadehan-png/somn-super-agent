"""自治闭环模块 - 提供自主学习和目标追踪能力"""

from __future__ import annotations
from typing import Any

__all__ = ['GoalManager', 'ReflectionEngine']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'GoalManager':
        from .goals import GoalManager
        return GoalManager
    if name == 'ReflectionEngine':
        from .reflection import ReflectionEngine
        return ReflectionEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
