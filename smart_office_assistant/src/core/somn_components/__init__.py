# -*- coding: utf-8 -*-
"""
Somn Components - SomnCore 模块化拆分产物

已拆分的子包:
- semantic_memory: 语义记忆 (分析器 + 用户管理)
- routing: 路由调度 (并行分析 + 路由决策)
- roi_tracking: ROI追踪
- feedback_learning: 反馈学习 (管道 + 强化学习)
- memory_context: 记忆上下文 (检索 + 缓存)
- autonomy_loop: 自治闭环 (目标 + 自省)
- task_execution: 任务执行 (编排器)
- reinforcement: 强化学习 (Q学习器 + 动作解析)
- llm_utils: LLM工具 (JSON解析)
- system_status: 系统监控
"""

from __future__ import annotations
from typing import Any

__all__ = [
    # 语义记忆
    'SemanticAnalyzer',
    'SemanticMemoryManager',
    # 路由调度
    'RouterDispatcher',
    # ROI追踪
    'ROITracker',
    # 反馈学习
    'FeedbackPipeline',
    'ReinforcementLearner',
    # 记忆上下文
    'MemoryRetriever',
    'SearchCache',
    # 自治闭环
    'GoalManager',
    'ReflectionEngine',
    # 任务执行
    'TaskOrchestrator',
    # 强化学习
    'QLearner',
    'ActionResolver',
    # LLM工具
    'LLMParser',
    # 系统监控
    'SystemMonitor',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'SemanticAnalyzer':
        from .semantic_memory import SemanticAnalyzer
        return SemanticAnalyzer
    if name == 'SemanticMemoryManager':
        from .semantic_memory import SemanticMemoryManager
        return SemanticMemoryManager
    if name == 'RouterDispatcher':
        from .routing import RouterDispatcher
        return RouterDispatcher
    if name == 'ROITracker':
        from .roi_tracking import ROITracker
        return ROITracker
    if name == 'FeedbackPipeline':
        from .feedback_learning import FeedbackPipeline
        return FeedbackPipeline
    if name == 'ReinforcementLearner':
        from .feedback_learning import ReinforcementLearner
        return ReinforcementLearner
    if name == 'MemoryRetriever':
        from .memory_context import MemoryRetriever
        return MemoryRetriever
    if name == 'SearchCache':
        from .memory_context import SearchCache
        return SearchCache
    if name == 'GoalManager':
        from .autonomy_loop import GoalManager
        return GoalManager
    if name == 'ReflectionEngine':
        from .autonomy_loop import ReflectionEngine
        return ReflectionEngine
    if name == 'TaskOrchestrator':
        from .task_execution import TaskOrchestrator
        return TaskOrchestrator
    if name == 'QLearner':
        from .reinforcement import QLearner
        return QLearner
    if name == 'ActionResolver':
        from .reinforcement import ActionResolver
        return ActionResolver
    if name == 'LLMParser':
        from .llm_utils import LLMParser
        return LLMParser
    if name == 'SystemMonitor':
        from .system_status import SystemMonitor
        return SystemMonitor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
