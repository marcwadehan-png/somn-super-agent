# ClawContext - 完整上下文能力
# 版本: v4.1.0

from __future__ import annotations
from typing import Any

__all__ = [
    # 上下文
    "ContextLevel",
    "SystemContext",
    "SessionContext",
    "UserContext",
    "ClawContext",
    "ClawContextContainer",
    # 环境变量
    "PREFIX_CLAW",
    "PREFIX_OPENCLAW",
    "EnvConfigItem",
    "CLAW_ENV_CONFIG",
    "ClawEnvironment",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    # 上下文
    if name == 'ContextLevel':
        from ._claw_context import ContextLevel
        return ContextLevel
    if name == 'SystemContext':
        from ._claw_context import SystemContext
        return SystemContext
    if name == 'SessionContext':
        from ._claw_context import SessionContext
        return SessionContext
    if name == 'UserContext':
        from ._claw_context import UserContext
        return UserContext
    if name == 'ClawContext':
        from ._claw_context import ClawContext
        return ClawContext
    if name == 'ClawContextContainer':
        from ._claw_context import ClawContextContainer
        return ClawContextContainer
    # 环境变量
    if name == 'PREFIX_CLAW':
        from ._claw_environment import PREFIX_CLAW
        return PREFIX_CLAW
    if name == 'PREFIX_OPENCLAW':
        from ._claw_environment import PREFIX_OPENCLAW
        return PREFIX_OPENCLAW
    if name == 'EnvConfigItem':
        from ._claw_environment import EnvConfigItem
        return EnvConfigItem
    if name == 'CLAW_ENV_CONFIG':
        from ._claw_environment import CLAW_ENV_CONFIG
        return CLAW_ENV_CONFIG
    if name == 'ClawEnvironment':
        from ._claw_environment import ClawEnvironment
        return ClawEnvironment
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")