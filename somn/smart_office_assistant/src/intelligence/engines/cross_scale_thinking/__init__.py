"""跨尺度统一思维引擎 - 包初始化"""
# 优先从主文件导入（包含完整实现）

from __future__ import annotations
from typing import Any

__all__ = [
    'CrossScaleThinkingEngine',
    'ScaleLevel',
    'EmergenceType',
    'ScaleInfo',
    'EmergenceExample',
    'SCALE_HIERARCHY',
    'EMERGENCE_EXAMPLES',
    'FINE_TUNED_CONSTANTS',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'CrossScaleThinkingEngine':
        from ..cross_scale_thinking_engine import CrossScaleThinkingEngine
        return CrossScaleThinkingEngine
    if name == 'ScaleLevel':
        from ..cross_scale_thinking_engine import ScaleLevel
        return ScaleLevel
    if name == 'EmergenceType':
        from ..cross_scale_thinking_engine import EmergenceType
        return EmergenceType
    if name == 'ScaleInfo':
        from ..cross_scale_thinking_engine import ScaleInfo
        return ScaleInfo
    if name == 'EmergenceExample':
        from ..cross_scale_thinking_engine import EmergenceExample
        return EmergenceExample
    if name == 'SCALE_HIERARCHY':
        from ..cross_scale_thinking_engine import SCALE_HIERARCHY
        return SCALE_HIERARCHY
    if name == 'EMERGENCE_EXAMPLES':
        from ..cross_scale_thinking_engine import EMERGENCE_EXAMPLES
        return EMERGENCE_EXAMPLES
    if name == 'FINE_TUNED_CONSTANTS':
        from ..cross_scale_thinking_engine import FINE_TUNED_CONSTANTS
        return FINE_TUNED_CONSTANTS
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
