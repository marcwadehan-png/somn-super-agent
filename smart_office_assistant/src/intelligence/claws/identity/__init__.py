# Claw IDENTITY驱动路由引擎
# v3.2.0

from __future__ import annotations
from typing import Any

__all__ = [
    "RouteTarget",
    "IdentityDrivenRouter",
    "SkillsTriggerMatcher",
    "CollaborationRoleAssigner",
    "IdentityRouterEngine",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'RouteTarget':
        from ._identity_router import RouteTarget
        return RouteTarget
    if name == 'IdentityDrivenRouter':
        from ._identity_router import IdentityDrivenRouter
        return IdentityDrivenRouter
    if name == 'SkillsTriggerMatcher':
        from ._identity_router import SkillsTriggerMatcher
        return SkillsTriggerMatcher
    if name == 'CollaborationRoleAssigner':
        from ._identity_router import CollaborationRoleAssigner
        return CollaborationRoleAssigner
    if name == 'IdentityRouterEngine':
        from ._identity_router import IdentityRouterEngine
        return IdentityRouterEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
