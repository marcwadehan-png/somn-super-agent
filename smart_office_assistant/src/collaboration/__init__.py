"""
协作模块 [v21.0 延迟加载优化]
Collaboration Module - 毫秒级启动

核心理念:
1. 集体智慧:多个用户的智慧大于单个用户
2. 资源共享:知识,经验,模板共享
3. 协同工作:实时协作,共同完成任务
4. 代际传承:知识从老用户传递给新用户

模块组成:
1. user_manager - 用户管理器
2. collaboration_engine - 协作引擎
3. (更多模块待添加)

[v21.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v21.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .user_manager import (
        UserManager, User, Session, Permission,
        PermissionManager, UserRole, UserStatus
    )
    from .collaboration_engine import (
        CollaborationEngine, Document, Change,
        ChangeType, Lock, ConflictResolver
    )


def __getattr__(name: str) -> Any:
    """[v21.0 优化] 延迟加载 - 毫秒级启动"""

    # user_manager
    if name in ('UserManager', 'User', 'Session', 'Permission',
                'PermissionManager', 'UserRole', 'UserStatus'):
        from . import user_manager as _m
        return getattr(_m, name)

    # collaboration_engine
    elif name in ('CollaborationEngine', 'Document', 'Change',
                  'ChangeType', 'Lock', 'ConflictResolver'):
        from . import collaboration_engine as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'collaboration' has no attribute '{name}'")


__version__ = '21.0.0'
__all__ = [
    'UserManager', 'User', 'Session', 'Permission',
    'PermissionManager', 'UserRole', 'UserStatus',
    'CollaborationEngine', 'Document', 'Change',
    'ChangeType', 'Lock', 'ConflictResolver'
]
