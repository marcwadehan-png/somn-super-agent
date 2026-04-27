# Claw激活与调度系统
# 版本: v1.0.0

from __future__ import annotations
from typing import Any

__all__ = [
    "ActivationPriority",
    "ClawActivationState",
    "CorrelationComputer",
    "ActivationScheduler",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'ActivationPriority':
        from ._claw_activation import ActivationPriority
        return ActivationPriority
    if name == 'ClawActivationState':
        from ._claw_activation import ClawActivationState
        return ClawActivationState
    if name == 'CorrelationComputer':
        from ._claw_activation import CorrelationComputer
        return CorrelationComputer
    if name == 'ActivationScheduler':
        from ._claw_activation import ActivationScheduler
        return ActivationScheduler
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")