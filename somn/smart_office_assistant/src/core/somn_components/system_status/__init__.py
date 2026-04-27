"""系统状态模块 - 提供状态监控能力"""

from __future__ import annotations
from typing import Any

__all__ = ['SystemMonitor']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'SystemMonitor':
        from .monitor import SystemMonitor
        return SystemMonitor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
