# Claw SOUL驱动行为引擎
# v3.1.0

from __future__ import annotations
from typing import Any

__all__ = [
    "DecisionPriority",
    "SoulDrivenDecision",
    "ValueFilter",
    "DisciplineEngine",
    "ResponseStyleEngine",
    "SoulBehaviorEngine",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'DecisionPriority':
        from ._soul_driver import DecisionPriority
        return DecisionPriority
    if name == 'SoulDrivenDecision':
        from ._soul_driver import SoulDrivenDecision
        return SoulDrivenDecision
    if name == 'ValueFilter':
        from ._soul_driver import ValueFilter
        return ValueFilter
    if name == 'DisciplineEngine':
        from ._soul_driver import DisciplineEngine
        return DisciplineEngine
    if name == 'ResponseStyleEngine':
        from ._soul_driver import ResponseStyleEngine
        return ResponseStyleEngine
    if name == 'SoulBehaviorEngine':
        from ._soul_driver import SoulBehaviorEngine
        return SoulBehaviorEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
