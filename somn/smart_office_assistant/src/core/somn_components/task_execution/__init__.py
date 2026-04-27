# -*- coding: utf-8 -*-
"""
任务执行模块 - Task Execution
负责任务编排、路由决策、缓存管理、回滚等
"""

from __future__ import annotations
from typing import Any

__all__ = ['TaskOrchestrator']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'TaskOrchestrator':
        from .orchestrator import TaskOrchestrator
        return TaskOrchestrator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
