"""ROI追踪模块 - 提供投入产出比追踪能力"""

from __future__ import annotations
from typing import Any

__all__ = ['ROITracker']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'ROITracker':
        from .tracker import ROITracker
        return ROITracker
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
