# -*- coding: utf-8 -*-
"""
数字大脑模块
Digital Brain Module

三个维度强化打通 + 两个外部打通 = 可迭代、会进化、会成长的智能核心

模块结构:
- digital_brain_core: 核心引擎
- digital_brain_integration: 系统集成桥接
- _somn_digital_brain_api: SomnCore深度集成API

版本: V1.1.0
创建: 2026-04-23
更新: 2026-04-23 [v1.1.0] 新增Somn集成API
"""

from __future__ import annotations
from typing import Any

__version__ = "1.0.0"
__author__ = "Somn Team"

__all__ = [
    # 核心
    'DigitalBrainCore',
    'BrainConfig',
    'BrainState',
    'BrainThought',
    'BrainEvolution',
    'BrainHealth',
    'MemoryLevel',
    'get_digital_brain',
    'shutdown_digital_brain',

    # 集成
    'MemoryBridgeConfig',
    'MemoryLibraryBridge',
    'MemorySyncDirection',
    'WisdomBridgeConfig',
    'WisdomMemoryBridge',
    'SomnIntegrationConfig',
    'SomnDigitalBrainIntegrator',
    'create_digital_brain_integration',

    # Somn集成API [v1.1.0]
    'DigitalBrainSomnConfig',
    'DigitalBrainSomnIntegrator',
    'ThroughResult',
    'create_digital_brain_somn_integrator',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    # 核心组件
    if name == 'DigitalBrainCore':
        from .digital_brain_core import DigitalBrainCore
        return DigitalBrainCore
    if name == 'BrainConfig':
        from .digital_brain_core import BrainConfig
        return BrainConfig
    if name == 'BrainState':
        from .digital_brain_core import BrainState
        return BrainState
    if name == 'BrainThought':
        from .digital_brain_core import BrainThought
        return BrainThought
    if name == 'BrainEvolution':
        from .digital_brain_core import BrainEvolution
        return BrainEvolution
    if name == 'BrainHealth':
        from .digital_brain_core import BrainHealth
        return BrainHealth
    if name == 'MemoryLevel':
        from .digital_brain_core import MemoryLevel
        return MemoryLevel
    if name == 'get_digital_brain':
        from .digital_brain_core import get_digital_brain
        return get_digital_brain
    if name == 'shutdown_digital_brain':
        from .digital_brain_core import shutdown_digital_brain
        return shutdown_digital_brain
    # 集成桥接
    if name == 'MemoryBridgeConfig':
        from .digital_brain_integration import MemoryBridgeConfig
        return MemoryBridgeConfig
    if name == 'MemoryLibraryBridge':
        from .digital_brain_integration import MemoryLibraryBridge
        return MemoryLibraryBridge
    if name == 'MemorySyncDirection':
        from .digital_brain_integration import MemorySyncDirection
        return MemorySyncDirection
    if name == 'WisdomBridgeConfig':
        from .digital_brain_integration import WisdomBridgeConfig
        return WisdomBridgeConfig
    if name == 'WisdomMemoryBridge':
        from .digital_brain_integration import WisdomMemoryBridge
        return WisdomMemoryBridge
    if name == 'SomnIntegrationConfig':
        from .digital_brain_integration import SomnIntegrationConfig
        return SomnIntegrationConfig
    if name == 'SomnDigitalBrainIntegrator':
        from .digital_brain_integration import SomnDigitalBrainIntegrator
        return SomnDigitalBrainIntegrator
    if name == 'create_digital_brain_integration':
        from .digital_brain_integration import create_digital_brain_integration
        return create_digital_brain_integration
    # Somn集成API
    if name == 'DigitalBrainSomnConfig':
        from ._somn_digital_brain_api import DigitalBrainSomnConfig
        return DigitalBrainSomnConfig
    if name == 'DigitalBrainSomnIntegrator':
        from ._somn_digital_brain_api import DigitalBrainSomnIntegrator
        return DigitalBrainSomnIntegrator
    if name == 'ThroughResult':
        from ._somn_digital_brain_api import ThroughResult
        return ThroughResult
    if name == 'create_digital_brain_somn_integrator':
        from ._somn_digital_brain_api import create_digital_brain_somn_integrator
        return create_digital_brain_somn_integrator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
