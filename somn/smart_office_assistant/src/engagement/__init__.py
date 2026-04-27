"""
用户参与与留存模块 [v1.0 延迟加载优化]
User Engagement System - 毫秒级启动

本模块提供健康,透明的用户参与和留存机制:
- 价值强化系统
- 自然参与机制
- 用户成功导向

核心理念:通过真实价值建立长期关系,而非心理操控

[v1.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v1.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .value_reinforcement import ValueReinforcementSystem, Achievement, Milestone
    from .natural_engagement import NaturalEngagementSystem, Reminder, Personalization
    from .user_success import UserSuccessSystem, Goal, ProgressTracker


def __getattr__(name: str) -> Any:
    """[v1.0 优化] 延迟加载 - 毫秒级启动"""

    # value_reinforcement
    if name in ('ValueReinforcementSystem', 'Achievement', 'Milestone'):
        from . import value_reinforcement as _m
        return getattr(_m, name)

    # natural_engagement
    elif name in ('NaturalEngagementSystem', 'Reminder', 'Personalization'):
        from . import natural_engagement as _m
        return getattr(_m, name)

    # user_success
    elif name in ('UserSuccessSystem', 'Goal', 'ProgressTracker'):
        from . import user_success as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'engagement' has no attribute '{name}'")


__all__ = [
    # 价值强化
    "ValueReinforcementSystem", "Achievement", "Milestone",
    # 自然参与
    "NaturalEngagementSystem", "Reminder", "Personalization",
    # 用户成功
    "UserSuccessSystem", "Goal", "ProgressTracker",
]

__version__ = "21.0.0"
