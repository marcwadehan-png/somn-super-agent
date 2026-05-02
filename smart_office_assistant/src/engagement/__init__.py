"""
用户参与与留存模块 [v22.0 — 合并 strategy_engine]
User Engagement System - 毫秒级启动

本模块提供健康、透明的用户参与和留存机制：
- 价值强化系统（成就/里程碑）
- 自然参与机制（提醒/个性化）
- 用户成功导向（目标追踪）
- 策略管理与执行规划（合并升级）

核心理念:通过真实价值建立长期关系,而非心理操控

[v22.0 合并] strategy_engine → strategy_manager + execution_planner
[v22.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v22.0.0
日期: 2026-05-01
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # 价值强化
    from .value_reinforcement import ValueReinforcementSystem, Achievement, Milestone
    # 自然参与
    from .natural_engagement import NaturalEngagementSystem, Reminder, Personalization
    # 用户成功
    from .user_success import UserSuccessSystem, Goal, ProgressTracker
    # 策略管理
    from .strategy_manager import (
        StrategyEngine, StrategyGoal, Strategy, ActionPlan,
        StrategyGoalPriority, StrategyGoalStatus,
        create_strategy_engine,
    )
    # 执行规划
    from .execution_planner import (
        ExecutionPlanner, Task, Resource,
        PlannerTaskStatus, TaskPriority,
        create_execution_planner,
    )


def __getattr__(name: str) -> Any:
    """[v22.0 优化] 延迟加载 - 毫秒级启动"""

    # 价值强化
    if name in ('ValueReinforcementSystem', 'Achievement', 'Milestone'):
        from . import value_reinforcement as _m
        return getattr(_m, name)

    # 自然参与
    elif name in ('NaturalEngagementSystem', 'Reminder', 'Personalization'):
        from . import natural_engagement as _m
        return getattr(_m, name)

    # 用户成功
    elif name in ('UserSuccessSystem', 'Goal', 'ProgressTracker'):
        from . import user_success as _m
        return getattr(_m, name)

    # 策略管理（v22.0 合并）
    elif name in (
        'StrategyEngine', 'StrategyGoal', 'Strategy', 'ActionPlan',
        'StrategyGoalPriority', 'StrategyGoalStatus',
        'create_strategy_engine',
    ):
        from . import strategy_manager as _m
        return getattr(_m, name)

    # 执行规划（v22.0 合并）
    elif name in (
        'ExecutionPlanner', 'Task', 'Resource',
        'PlannerTaskStatus', 'TaskPriority',
        'create_execution_planner',
    ):
        from . import execution_planner as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'engagement' has no attribute '{name}'")


__all__ = [
    # 价值强化
    "ValueReinforcementSystem", "Achievement", "Milestone",
    # 自然参与
    "NaturalEngagementSystem", "Reminder", "Personalization",
    # 用户成功
    "UserSuccessSystem", "Goal", "ProgressTracker",
    # 策略管理（v22.0 合并自 strategy_engine）
    "StrategyEngine", "StrategyGoal", "Strategy", "ActionPlan",
    "StrategyGoalPriority", "StrategyGoalStatus",
    "create_strategy_engine",
    # 执行规划（v22.0 合并自 strategy_engine）
    "ExecutionPlanner", "Task", "Resource",
    "PlannerTaskStatus", "TaskPriority",
    "create_execution_planner",
]

__version__ = "22.0.0"
