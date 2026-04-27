# -*- coding: utf-8 -*-
"""
Claw子智能体模块 - 每个贤者的独立实例
版本: v1.0.0

核心文件:
- _claw_architect.py  - 架构定义
- _claws_runtime.py - 运行时
- _claws_coordinator.py - 协作调度
- __init__.py - 导出
"""

from __future__ import annotations
from typing import Any

__all__ = [
    "ClawConfig", "ClawStatus", "SageClaw", "ClawFactory",
    "ClawRuntime", "ClawInstance", "get_coordinator"
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'ClawConfig':
        from ._claw_architect import ClawConfig
        return ClawConfig
    if name == 'ClawStatus':
        from ._claw_architect import ClawStatus
        return ClawStatus
    if name == 'SageClaw':
        from ._claw_architect import SageClaw
        return SageClaw
    if name == 'ClawFactory':
        from ._claw_architect import ClawFactory
        return ClawFactory
    if name == 'ClawRuntime':
        from ._claws_runtime import ClawRuntime
        return ClawRuntime
    if name == 'ClawInstance':
        from ._claws_runtime import ClawInstance
        return ClawInstance
    if name == 'get_coordinator':
        from ._claws_coordinator import get_coordinator
        return get_coordinator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
