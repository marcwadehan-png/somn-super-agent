"""
策略引擎模块 [v21.0 延迟加载优化]
Strategy Engine - 毫秒级启动

功能:目标分解, 策略生成, 执行规划

[v21.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v21.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .strategy_core import StrategyEngine, Goal, Strategy, ActionPlan
    from .execution_planner import ExecutionPlanner, Task, Resource


def __getattr__(name: str) -> Any:
    """[v21.0 优化] 延迟加载 - 毫秒级启动"""

    if name in ('StrategyEngine', 'Goal', 'Strategy', 'ActionPlan'):
        from . import strategy_core as _m
        return getattr(_m, name)
    elif name in ('ExecutionPlanner', 'Task', 'Resource'):
        from . import execution_planner as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'strategy_engine' has no attribute '{name}'")


__all__ = [
    'StrategyEngine', 'Goal', 'Strategy', 'ActionPlan',
    'ExecutionPlanner', 'Task', 'Resource'
]
