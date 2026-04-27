"""
自主智能体核心 [v21.0 延迟加载优化]
Autonomous Agent Core - 毫秒级启动

实现真正的智能体五大核心能力:
1. 目标系统 (Goal System) - 目标设定/分解/追踪
2. 自主调度器 (Autonomous Scheduler) - 定期检查/触发action
3. 执行-观察-反思闭环 (Execution-Reflection Loop)
4. 持续状态管理 (Persistent State Manager)
5. 价值驱动decision系统 (Value-Driven Decision System)

[v21.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

v21.0.0 - 自主智能体架构
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .goal_system import GoalSystem, Goal, GoalStatus, GoalPriority
    from .autonomous_scheduler import AutonomousScheduler, ScheduledTask
    from .reflection_engine import ReflectionEngine, ExecutionRecord
    from .state_manager import StateManager, AgentState
    from .value_system import ValueSystem, Value, Decision


def __getattr__(name: str) -> Any:
    """[v21.0 优化] 延迟加载 - 毫秒级启动"""

    # Goal System
    if name in ('GoalSystem', 'Goal', 'GoalStatus', 'GoalPriority'):
        from . import goal_system as _m
        return getattr(_m, name)

    # Autonomous Scheduler
    elif name in ('AutonomousScheduler', 'ScheduledTask'):
        from . import autonomous_scheduler as _m
        return getattr(_m, name)

    # Reflection Engine
    elif name in ('ReflectionEngine', 'ExecutionRecord'):
        from . import reflection_engine as _m
        return getattr(_m, name)

    # State Manager
    elif name in ('StateManager', 'AgentState'):
        from . import state_manager as _m
        return getattr(_m, name)

    # Value System
    elif name in ('ValueSystem', 'Value', 'Decision'):
        from . import value_system as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'autonomous_core' has no attribute '{name}'")


__all__ = [
    'GoalSystem', 'Goal', 'GoalStatus', 'GoalPriority',
    'AutonomousScheduler', 'ScheduledTask',
    'ReflectionEngine', 'ExecutionRecord',
    'StateManager', 'AgentState',
    'ValueSystem', 'Value', 'Decision'
]
