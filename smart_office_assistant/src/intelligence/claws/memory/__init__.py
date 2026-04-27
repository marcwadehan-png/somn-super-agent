# Claw动态格子记忆系统
# 版本: v3.3.0

from __future__ import annotations
from typing import Any

__all__ = [
    # 动态格子
    "CellType",
    "LearnDepth",
    "CellMeta",
    "CellContent",
    "CellsIndex",
    "ActivationLog",
    "DynamicMemorySystem",
    # 学习引擎
    "LongTermMemory",
    "CorrelationEngine",
    "OnDemandCreator",
    "LearningEngine",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'CellType':
        from ._dynamic_cells import CellType
        return CellType
    if name == 'LearnDepth':
        from ._dynamic_cells import LearnDepth
        return LearnDepth
    if name == 'CellMeta':
        from ._dynamic_cells import CellMeta
        return CellMeta
    if name == 'CellContent':
        from ._dynamic_cells import CellContent
        return CellContent
    if name == 'CellsIndex':
        from ._dynamic_cells import CellsIndex
        return CellsIndex
    if name == 'ActivationLog':
        from ._dynamic_cells import ActivationLog
        return ActivationLog
    if name == 'DynamicMemorySystem':
        from ._dynamic_cells import DynamicMemorySystem
        return DynamicMemorySystem
    if name == 'LongTermMemory':
        from ._learning_engine import LongTermMemory
        return LongTermMemory
    if name == 'CorrelationEngine':
        from ._learning_engine import CorrelationEngine
        return CorrelationEngine
    if name == 'OnDemandCreator':
        from ._learning_engine import OnDemandCreator
        return OnDemandCreator
    if name == 'LearningEngine':
        from ._learning_engine import LearningEngine
        return LearningEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")