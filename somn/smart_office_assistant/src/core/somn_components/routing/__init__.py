"""路由调度模块 - 提供任务路由选择能力"""

from __future__ import annotations
from typing import Any

__all__ = ['RouterDispatcher']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'RouterDispatcher':
        from .dispatcher import RouterDispatcher
        return RouterDispatcher
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
