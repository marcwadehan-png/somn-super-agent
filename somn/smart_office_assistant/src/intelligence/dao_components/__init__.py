# -*- coding: utf-8 -*-
"""
Dao Components - 道家智慧模块化拆分产物

已拆分的子模块:
- philosophy: 道德经、庄子哲学
- decision: 太极决策、增长战略
"""

from __future__ import annotations
from typing import Any

__all__ = [
    'DeJingPhilosophy',
    'ZhuangziPhilosophy',
    'TaiJiDecision',
    'GrowthStrategy',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'DeJingPhilosophy':
        from .philosophy import DeJingPhilosophy
        return DeJingPhilosophy
    if name == 'ZhuangziPhilosophy':
        from .philosophy import ZhuangziPhilosophy
        return ZhuangziPhilosophy
    if name == 'TaiJiDecision':
        from .decision import TaiJiDecision
        return TaiJiDecision
    if name == 'GrowthStrategy':
        from .decision import GrowthStrategy
        return GrowthStrategy
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
