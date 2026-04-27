# -*- coding: utf-8 -*-
"""
主链执行引擎
提供并行和串行执行能力
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# 从parallel_execution_engine导入实际类
from src.main_chain.parallel_execution_engine import (
    ParallelExecutionEngine,
    TaskPhase,
    ProgressLevel,
    TaskProgress,
    ExecutionProgress,
    ProgressTracker,
    ResultCollector,
    get_parallel_execution_engine,
)

__all__ = [
    "ExecutionEngine",
    "ParallelExecutionEngine",
    "ExecutionTask",
    "ExecutionResult",
    "TaskPhase",
    "ProgressLevel",
    "TaskProgress",
    "ExecutionProgress",
    "get_execution_engine",
    "get_parallel_execution_engine",
]


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionTask:
    """执行任务"""
    task_id: str
    name: str
    func: Optional[Callable] = None
    args: tuple = ()
    kwargs: dict = None
    priority: int = 0
    timeout: Optional[float] = None
    status: TaskStatus = TaskStatus.PENDING
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


@dataclass
class ExecutionResult:
    """执行结果"""
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    duration: float = 0.0


class ExecutionEngine:
    """
    执行引擎 (ParallelExecutionEngine的别名)
    提供统一的任务执行接口
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._engine = None
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            self._engine = ParallelExecutionEngine()
            logger.info("ExecutionEngine initialized")
    
    def execute(self, task: ExecutionTask) -> ExecutionResult:
        """执行单个任务"""
        try:
            if task.func:
                import time
                start = time.time()
                result = task.func(*task.args, **task.kwargs)
                duration = time.time() - start
                return ExecutionResult(
                    task_id=task.task_id,
                    success=True,
                    result=result,
                    duration=duration
                )
            return ExecutionResult(
                task_id=task.task_id,
                success=False,
                error="No function specified"
            )
        except Exception as e:
            return ExecutionResult(
                task_id=task.task_id,
                success=False,
                error="执行失败"
            )
    
    def execute_batch(self, tasks: List[ExecutionTask]) -> List[ExecutionResult]:
        """批量执行任务"""
        return [self.execute(task) for task in tasks]
    
    def execute_parallel(self, tasks: List[ExecutionTask]) -> List[ExecutionResult]:
        """并行执行任务"""
        return self._engine.execute_parallel(tasks) if hasattr(self._engine, 'execute_parallel') else self.execute_batch(tasks)


def get_execution_engine() -> ExecutionEngine:
    """获取执行引擎单例"""
    return ExecutionEngine()
