"""
主线架构包 [v1.0 延迟加载优化]
Main Chain Architecture Package - 毫秒级启动

包含：
- ParallelRouter: 并形路由器
- ParallelExecutionEngine v1.0: 并行执行引擎（进度追踪/结果回收/汇总优化）
- CrossWeaver: 交叉织网器
- MainChainScheduler: 主线调度器
- MainChainIntegration: 主线集成器
- MainChainMonitor: 主线监控器

使用方式：
    from src.main_chain import get_parallel_router, get_parallel_execution_engine
    from src.main_chain import MainChainIntegration, MainChainMonitor

[v1.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本：v1.0.0
日期：2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # ParallelRouter
    from .parallel_router import (
        ParallelRouter, ParallelMode, RouteStrategy, RouteConfig,
        ParallelTask, ParallelResult, AggregatedResult, ModuleRegistry, get_parallel_router,
    )
    # ParallelExecutionEngine v1.0
    from .parallel_execution_engine import (
        ParallelExecutionEngine, ProgressTracker, ResultCollector,
        TaskPhase, ProgressLevel, TaskProgress, ExecutionProgress,
        get_parallel_execution_engine,
    )
    # CrossWeaver
    from .cross_weaver import (
        CrossWeaver, FeedbackType, CrossAxis, CrossLink,
        CrossSignal, CrossResult, CrossGraph, get_cross_weaver,
    )
    # MainChainScheduler
    from .main_chain_scheduler import (
        MainChainScheduler, RunMode, ChainContext, ChainResult,
        get_main_chain_scheduler,
    )
    # MainChainIntegration
    from .main_chain_integration import (
        MainChainIntegration, ChainRunMode, ChainExecutionResult,
        get_main_chain_integration,
    )
    # MainChainMonitor
    from .main_chain_monitor import (
        MainChainMonitor, ExecutionState, ExecutionRecord,
        NodeMetrics, get_main_chain_monitor,
    )


def __getattr__(name: str) -> Any:
    """[v1.0 优化] 延迟加载 - 毫秒级启动"""

    # ParallelRouter
    if name in ('ParallelRouter', 'ParallelMode', 'RouteStrategy', 'RouteConfig',
                'ParallelTask', 'ParallelResult', 'AggregatedResult', 'ModuleRegistry', 'get_parallel_router'):
        from . import parallel_router as _m
        return getattr(_m, name)

    # ParallelExecutionEngine v1.0
    elif name in ('ParallelExecutionEngine', 'ProgressTracker', 'ResultCollector',
                  'TaskPhase', 'ProgressLevel', 'TaskProgress', 'ExecutionProgress',
                  'get_parallel_execution_engine'):
        from . import parallel_execution_engine as _m
        return getattr(_m, name)

    # CrossWeaver
    elif name in ('CrossWeaver', 'FeedbackType', 'CrossAxis', 'CrossLink',
                  'CrossSignal', 'CrossResult', 'CrossGraph', 'get_cross_weaver'):
        from . import cross_weaver as _m
        return getattr(_m, name)

    # MainChainScheduler
    elif name in ('MainChainScheduler', 'RunMode', 'ChainContext', 'ChainResult',
                  'get_main_chain_scheduler'):
        from . import main_chain_scheduler as _m
        return getattr(_m, name)

    # MainChainIntegration
    elif name in ('MainChainIntegration', 'ChainRunMode', 'ChainExecutionResult',
                  'get_main_chain_integration'):
        from . import main_chain_integration as _m
        return getattr(_m, name)

    # MainChainMonitor
    elif name in ('MainChainMonitor', 'ExecutionState', 'ExecutionRecord',
                  'NodeMetrics', 'get_main_chain_monitor'):
        from . import main_chain_monitor as _m
        return getattr(_m, name)

    # ExecutionEngine (别名)
    elif name in ('ExecutionEngine',):
        from . import execution_engine as _m
        return getattr(_m, name)

    # Config loader
    elif name in ('MainChainConfig', 'get_main_chain_config'):
        try:
            from . import config_loader as _m
            return getattr(_m, name)
        except ImportError:
            raise AttributeError(f"module 'main_chain' has no attribute '{name}' (config_loader unavailable)")

    raise AttributeError(f"module 'main_chain' has no attribute '{name}'")


# 包版本
__version__ = "21.0.0"

# 公开 API（保持向后兼容）
__all__ = [
    # ParallelRouter
    "ParallelRouter", "ParallelMode", "RouteStrategy", "RouteConfig",
    "ParallelTask", "ParallelResult", "AggregatedResult", "ModuleRegistry", "get_parallel_router",
    # ParallelExecutionEngine v1.0
    "ParallelExecutionEngine", "ProgressTracker", "ResultCollector",
    "TaskPhase", "ProgressLevel", "TaskProgress", "ExecutionProgress", "get_parallel_execution_engine",
    # ExecutionEngine (别名)
    "ExecutionEngine",
    # CrossWeaver
    "CrossWeaver", "FeedbackType", "CrossAxis", "CrossLink",
    "CrossSignal", "CrossResult", "CrossGraph", "get_cross_weaver",
    # MainChainScheduler
    "MainChainScheduler", "RunMode", "ChainContext", "ChainResult", "get_main_chain_scheduler",
    # MainChainIntegration
    "MainChainIntegration", "ChainRunMode", "ChainExecutionResult", "get_main_chain_integration",
    # MainChainMonitor
    "MainChainMonitor", "ExecutionState", "ExecutionRecord", "NodeMetrics", "get_main_chain_monitor",
    # Config
    "MainChainConfig", "get_main_chain_config",
]
