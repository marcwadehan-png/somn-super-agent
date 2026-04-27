# -*- coding: utf-8 -*-
"""
强化学习模块 - Reinforcement Learning
负责Q值学习、动作映射、反馈应用等
"""

from __future__ import annotations
from typing import Any

__all__ = ['QLearner', 'ActionResolver']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'QLearner':
        from .q_learner import QLearner
        return QLearner
    if name == 'ActionResolver':
        from .q_learner import ActionResolver
        return ActionResolver
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
