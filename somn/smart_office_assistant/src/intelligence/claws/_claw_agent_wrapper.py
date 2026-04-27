# -*- coding: utf-8 -*-
"""
_claw_agent_wrapper.py - Claw独立子Agent化包装层
=================================================

将763个Claw包装为可独立运行的Task子Agent。

核心能力:
1. 异步启动 - 非阻塞立即返回任务ID
2. 会话隔离 - 每个子Agent独立上下文
3. Task生命周期管理 - 追踪状态/结果/错误
4. 嵌套调度支持 - 子Agent可继续调度其他Claw

用法:
    >>> wrapper = ClawAgentWrapper("孔子")
    >>> task_id = await wrapper.spawn("什么是仁？")
    >>> # 立即返回task_id，后续可查询状态
    >>> status = wrapper.get_task_status(task_id)
    >>> result = await wrapper.wait_result(task_id)

版本: v1.0.0
创建: 2026-04-24
"""

from __future__ import annotations

import asyncio
import logging
import uuid
import time
from typing import Dict, Optional, Any, Callable, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# Task状态枚举
# ═══════════════════════════════════════════════════════════════

class TaskStatus(Enum):
    """Task生命周期状态"""
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    CANCELLED = "cancelled"  # 已取消
    TIMEOUT = "timeout"      # 超时


# ═══════════════════════════════════════════════════════════════
# Task信息数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class AgentTaskInfo:
    """Task执行信息"""
    task_id: str
    claw_name: str
    query: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    # 执行结果
    result: Optional[str] = None
    error: Optional[str] = None
    success: bool = False
    confidence: float = 0.0
    elapsed_seconds: float = 0.0
    steps_count: int = 0
    
    # 嵌套调度
    nested_tasks: List[str] = field(default_factory=list)
    
    # 回调
    callbacks: List[Callable] = field(default_factory=list)
    
    # asyncio.Task引用
    _async_task: Optional[asyncio.Task] = None


@dataclass
class SpawnOptions:
    """spawn选项"""
    background: bool = True           # 是否后台执行
    timeout: Optional[float] = None   # 超时秒数（None=继承默认值）
    priority: int = 1                # 优先级（越小越高）
    enable_nested: bool = True       # 是否允许嵌套调度
    on_complete: Optional[Callable] = None  # 完成回调
    on_error: Optional[Callable] = None       # 错误回调
    on_progress: Optional[Callable] = None    # 进度回调 (step, total_steps)


# ═══════════════════════════════════════════════════════════════
# ClawAgentWrapper - 核心包装类
# ═══════════════════════════════════════════════════════════════

class ClawAgentWrapper:
    """
    Claw到Task子Agent的桥接层。
    
    将Claw包装为可独立运行的异步子Agent：
    1. 非阻塞启动（spawn）
    2. 状态追踪（get_status/wait_result）
    3. 会话隔离（独立ClawContext）
    4. 嵌套调度（nested spawn）
    
    用法:
        # 基本用法
        >>> wrapper = ClawAgentWrapper("孔子")
        >>> task_id = await wrapper.spawn("什么是仁？")
        >>> result = await wrapper.wait_result(task_id)
        
        # 带选项
        >>> task_id = await wrapper.spawn(
        ...     "分析当前经济形势",
        ...     options=SpawnOptions(timeout=300, background=False)
        ... )
    """
    
    # 默认超时配置（与GlobalClawScheduler对齐）
    DEFAULT_TIMEOUT = 120.0
    MAX_NESTED_DEPTH = 3
    
    def __init__(
        self,
        claw_name: str,
        max_concurrent: int = 5,
        nested_enabled: bool = True,
    ):
        """
        Args:
            claw_name: Claw名称
            max_concurrent: 最大并发Task数
            nested_enabled: 是否允许嵌套调度
        """
        self.claw_name = claw_name
        self._nested_enabled = nested_enabled
        self._max_concurrent = max_concurrent
        
        # Task管理
        self._tasks: Dict[str, AgentTaskInfo] = {}
        self._semaphore = asyncio.Semaphore(max_concurrent)
        
        # Claw实例（懒加载）
        self._claw = None
        self._claw_loaded = False
        
        # 线程池（用于同步环境）
        self._thread_pool: Optional[ThreadPoolExecutor] = None
        
        # 嵌套深度追踪
        self._nested_depth: int = 0
        
        logger.info(f"[ClawAgentWrapper] 初始化: {claw_name}")
    
    # ═════════════════════════════════════════════════════════
    # Claw加载
    # ═════════════════════════════════════════════════════════
    
    async def _ensure_claw_loaded(self) -> Any:
        """确保Claw已加载"""
        if self._claw_loaded and self._claw is not None:
            return self._claw
        
        from ._claw_architect import create_claw
        
        try:
            self._claw = await create_claw(self.claw_name)
            self._claw_loaded = True
            logger.info(f"[ClawAgentWrapper] {self.claw_name} Claw加载成功")
            return self._claw
        except Exception as e:
            logger.error(f"[ClawAgentWrapper] {self.claw_name} Claw加载失败: {e}")
            raise
    
    def _ensure_claw_loaded_sync(self) -> Any:
        """同步版本Claw加载（使用线程池）"""
        if self._claw_loaded and self._claw is not None:
            return self._claw

        from ._claw_architect import create_claw

        try:
            # 使用现有事件循环在后台线程执行
            loop = asyncio.new_event_loop()
            self._claw = loop.run_until_complete(create_claw(self.claw_name))
            self._claw_loaded = True
            loop.close()
            return self._claw
        except Exception as e:
            logger.error(f"[ClawAgentWrapper] {self.claw_name} Claw加载失败(同步): {e}")
            raise
    
    # ═════════════════════════════════════════════════════════
    # 核心：Spawn（异步启动）
    # ═════════════════════════════════════════════════════════
    
    async def spawn(
        self,
        query: str,
        options: Optional[SpawnOptions] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        异步启动Claw子Agent（非阻塞）。
        
        立即返回task_id，Task在后台异步执行。
        
        Args:
            query: 任务内容
            options: spawn选项
            context: 额外上下文
            
        Returns:
            task_id: 任务标识符
        """
        options = options or SpawnOptions()
        task_id = f"claw_task_{uuid.uuid4().hex[:12]}"
        
        # 创建TaskInfo
        task_info = AgentTaskInfo(
            task_id=task_id,
            claw_name=self.claw_name,
            query=query,
            status=TaskStatus.PENDING,
        )
        
        if options.on_complete or options.on_error:
            # 分别注册完成和错误回调
            if options.on_complete:
                task_info.callbacks.append(options.on_complete)
            if options.on_error:
                task_info.callbacks.append(options.on_error)
        
        self._tasks[task_id] = task_info
        
        # 创建asyncio.Task执行
        async_task = asyncio.create_task(
            self._execute_task(task_id, query, options, context)
        )
        task_info._async_task = async_task
        
        logger.info(
            f"[ClawAgentWrapper] Task启动: {task_id} -> {self.claw_name}"
        )
        
        return task_id
    
    async def _execute_task(
        self,
        task_id: str,
        query: str,
        options: SpawnOptions,
        context: Optional[Dict[str, Any]],
    ) -> None:
        """内部：执行Task"""
        task_info = self._tasks.get(task_id)
        if not task_info:
            return

        start_time = time.monotonic()
        warning_issued = False  # 超时警告标志

        async with self._semaphore:
            task_info.status = TaskStatus.RUNNING
            task_info.started_at = datetime.now().isoformat()

            timeout = options.timeout or self.DEFAULT_TIMEOUT
            warning_threshold = timeout * 0.8  # 80%时发警告

            try:
                # 确保Claw已加载
                claw = await self._ensure_claw_loaded()

                # 构建执行上下文
                exec_context = self._build_context(context, task_id)

                # 执行ReAct闭环（带超时保护）
                result = await asyncio.wait_for(
                    claw.process(query, exec_context),
                    timeout=timeout,
                )

                # 更新结果
                task_info.result = result.final_answer
                task_info.success = result.success
                task_info.confidence = 1.0
                task_info.steps_count = len(result.steps) if result.steps else 0

                if result.success:
                    task_info.status = TaskStatus.COMPLETED
                else:
                    task_info.status = TaskStatus.FAILED
                    task_info.error = result.reason

            except asyncio.TimeoutError:
                task_info.status = TaskStatus.TIMEOUT
                task_info.error = f"Task超时({timeout}s)"
                logger.warning(
                    f"[ClawAgentWrapper] Task超时: {task_id} -> {self.claw_name} "
                    f"(elapsed={time.monotonic() - start_time:.2f}s)"
                )

            except Exception as e:
                task_info.status = TaskStatus.FAILED
                task_info.error = "操作失败"[:200]
                logger.error(
                    f"[ClawAgentWrapper] Task异常: {task_id} -> {self.claw_name}: {e}"
                )

            finally:
                task_info.completed_at = datetime.now().isoformat()
                task_info.elapsed_seconds = time.monotonic() - start_time

                # 执行完成/错误回调
                for cb in task_info.callbacks:
                    try:
                        if asyncio.iscoroutinefunction(cb):
                            await cb(task_info)
                        else:
                            cb(task_info)
                    except Exception as e:
                        logger.debug(f"[ClawAgentWrapper] 回调执行失败: {e}")

                logger.info(
                    f"[ClawAgentWrapper] Task完成: {task_id} -> {self.claw_name} "
                    f"({task_info.status.value}, {task_info.elapsed_seconds:.2f}s)"
                )
    
    def _build_context(
        self,
        base_context: Optional[Dict[str, Any]],
        task_id: str,
    ) -> Dict[str, Any]:
        """构建执行上下文"""
        context = base_context or {}
        
        # 添加Task元信息
        context["_task_id"] = task_id
        context["_claw_name"] = self.claw_name
        context["_nested_enabled"] = self._nested_enabled
        
        return context
    
    # ═════════════════════════════════════════════════════════
    # 嵌套调度
    # ═════════════════════════════════════════════════════════
    
    async def spawn_nested(
        self,
        query: str,
        target_claw: Optional[str] = None,
        options: Optional[SpawnOptions] = None,
    ) -> str:
        """
        嵌套spawn（在Task执行中调度其他Claw）。
        
        Args:
            query: 嵌套任务内容
            target_claw: 目标Claw（None=使用当前Claw）
            options: spawn选项
            
        Returns:
            嵌套Task ID
            
        Raises:
            RuntimeError: 如果嵌套调度被禁用或超过最大深度
        """
        if not self._nested_enabled:
            raise RuntimeError("嵌套调度已禁用")
        
        if self._nested_depth >= self.MAX_NESTED_DEPTH:
            raise RuntimeError(f"嵌套深度超限({self.MAX_NESTED_DEPTH})")
        
        self._nested_depth += 1
        
        try:
            target = target_claw or self.claw_name
            wrapper = ClawAgentWrapper(
                target,
                nested_enabled=False,  # 防止无限嵌套
            )
            return await wrapper.spawn(query, options)
        finally:
            self._nested_depth -= 1
    
    # ═════════════════════════════════════════════════════════
    # 状态查询
    # ═════════════════════════════════════════════════════════
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """获取Task状态"""
        task_info = self._tasks.get(task_id)
        return task_info.status if task_info else None
    
    def get_task_info(self, task_id: str) -> Optional[AgentTaskInfo]:
        """获取完整Task信息"""
        return self._tasks.get(task_id)
    
    def is_running(self, task_id: str) -> bool:
        """检查Task是否运行中"""
        status = self.get_task_status(task_id)
        return status == TaskStatus.RUNNING
    
    def is_complete(self, task_id: str) -> bool:
        """检查Task是否完成（成功/失败/超时/取消）"""
        status = self.get_task_status(task_id)
        return status in (
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.TIMEOUT,
            TaskStatus.CANCELLED,
        )
    
    def list_active_tasks(self) -> List[str]:
        """列出运行中的Task ID"""
        return [
            tid for tid, info in self._tasks.items()
            if info.status == TaskStatus.RUNNING
        ]
    
    def list_all_tasks(self) -> List[str]:
        """列出所有Task ID"""
        return list(self._tasks.keys())
    
    # ═════════════════════════════════════════════════════════
    # 结果获取
    # ═════════════════════════════════════════════════════════
    
    async def wait_result(
        self,
        task_id: str,
        timeout: Optional[float] = None,
    ) -> AgentTaskInfo:
        """
        等待Task完成并返回结果。
        
        Args:
            task_id: 任务ID
            timeout: 等待超时（秒）
            
        Returns:
            AgentTaskInfo: 包含完整执行信息
            
        Raises:
            asyncio.TimeoutError: 等待超时
            KeyError: Task不存在
        """
        task_info = self._tasks.get(task_id)
        if not task_info:
            raise KeyError(f"Task不存在: {task_id}")
        
        if task_info.status in (
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.TIMEOUT,
            TaskStatus.CANCELLED,
        ):
            return task_info
        
        # 等待asyncio.Task完成
        if task_info._async_task:
            await asyncio.wait_for(
                task_info._async_task,
                timeout=timeout,
            )
        
        return task_info
    
    async def get_result(
        self,
        task_id: str,
    ) -> Optional[str]:
        """
        获取Task结果（非阻塞）。
        
        Returns:
            结果字符串，或None（如果未完成）
        """
        task_info = self._tasks.get(task_id)
        if not task_info:
            return None
        
        if task_info.status == TaskStatus.COMPLETED:
            return task_info.result
        
        return None
    
    # ═════════════════════════════════════════════════════════
    # Task控制
    # ═════════════════════════════════════════════════════════
    
    async def cancel_task(self, task_id: str) -> bool:
        """
        取消Task。

        Returns:
            是否成功取消
        """
        task_info = self._tasks.get(task_id)
        if not task_info:
            return False

        if task_info.status == TaskStatus.RUNNING:
            if task_info._async_task and not task_info._async_task.done():
                task_info._async_task.cancel()
                try:
                    await task_info._async_task
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    logger.debug(f"pass失败: {e}")

            task_info.status = TaskStatus.CANCELLED
            task_info.completed_at = datetime.now().isoformat()
            return True

        # 可以取消PENDING状态的Task
        if task_info.status == TaskStatus.PENDING:
            task_info.status = TaskStatus.CANCELLED
            task_info.completed_at = datetime.now().isoformat()
            return True

        return False
    
    def clear_completed(self) -> int:
        """
        清理已完成的Task信息。
        
        Returns:
            清理的Task数量
        """
        completed_ids = [
            tid for tid, info in self._tasks.items()
            if info.status in (
                TaskStatus.COMPLETED,
                TaskStatus.FAILED,
                TaskStatus.TIMEOUT,
                TaskStatus.CANCELLED,
            )
        ]
        
        for tid in completed_ids:
            del self._tasks[tid]
        
        return len(completed_ids)
    
    # ═════════════════════════════════════════════════════════
    # 统计
    # ═════════════════════════════════════════════════════════
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        status_counts = {}
        for info in self._tasks.values():
            status_counts[info.status.value] = \
                status_counts.get(info.status.value, 0) + 1
        
        return {
            "claw_name": self.claw_name,
            "total_tasks": len(self._tasks),
            "status_counts": status_counts,
            "active_count": len(self.list_active_tasks()),
            "nested_depth": self._nested_depth,
        }


# ═══════════════════════════════════════════════════════════════
# ClawAgentPool - 多Claw统一管理池
# ═══════════════════════════════════════════════════════════════

class ClawAgentPool:
    """
    多Claw Agent统一管理池。
    
    管理多个ClawAgentWrapper，支持：
    1. 按名称获取/创建Wrapper
    2. 批量spawn
    3. 统一状态监控
    
    用法:
        >>> pool = ClawAgentPool()
        >>> task1 = await pool.spawn("孔子", "什么是仁？")
        >>> task2 = await pool.spawn("老子", "什么是道？")
        >>> results = await pool.wait_all([task1, task2])
    """
    
    def __init__(self, max_per_claw: int = 5):
        """
        Args:
            max_per_claw: 每个Claw最大并发数
        """
        self._max_per_claw = max_per_claw
        self._wrappers: Dict[str, ClawAgentWrapper] = {}
        self._global_tasks: Dict[str, str] = {}  # task_id -> claw_name
    
    def get_wrapper(self, claw_name: str) -> ClawAgentWrapper:
        """获取或创建ClawAgentWrapper"""
        if claw_name not in self._wrappers:
            self._wrappers[claw_name] = ClawAgentWrapper(
                claw_name,
                max_concurrent=self._max_per_claw,
            )
        return self._wrappers[claw_name]
    
    async def spawn(
        self,
        claw_name: str,
        query: str,
        options: Optional[SpawnOptions] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Spawn Task到指定Claw。
        
        Returns:
            task_id
        """
        wrapper = self.get_wrapper(claw_name)
        task_id = await wrapper.spawn(query, options, context)
        self._global_tasks[task_id] = claw_name
        return task_id
    
    async def spawn_batch(
        self,
        tasks: List[Dict[str, str]],  # [{"claw_name": "...", "query": "..."}, ...]
        options: Optional[SpawnOptions] = None,
    ) -> List[str]:
        """
        批量Spawn（并发执行）。

        Args:
            tasks: Task列表
            options: 通用选项

        Returns:
            task_id列表
        """
        if not tasks:
            return []

        # 并发spawn
        coros = [
            self.spawn(task["claw_name"], task["query"], options)
            for task in tasks
        ]
        task_ids = await asyncio.gather(*coros, return_exceptions=True)

        # 过滤异常
        return [
            tid if isinstance(tid, str) else None
            for tid in task_ids
        ]
    
    def get_task_info(self, task_id: str) -> Optional[AgentTaskInfo]:
        """获取Task信息"""
        claw_name = self._global_tasks.get(task_id)
        if claw_name:
            wrapper = self._wrappers.get(claw_name)
            if wrapper:
                return wrapper.get_task_info(task_id)
        return None
    
    async def wait_all(
        self,
        task_ids: List[str],
        timeout: Optional[float] = None,
    ) -> List[AgentTaskInfo]:
        """
        等待所有Task完成。
        
        Args:
            task_ids: Task ID列表
            timeout: 总体超时
            
        Returns:
            AgentTaskInfo列表
        """
        coros = []
        for tid in task_ids:
            claw_name = self._global_tasks.get(tid)
            if claw_name:
                wrapper = self._wrappers.get(claw_name)
                if wrapper:
                    coros.append(wrapper.wait_result(tid))
        
        if coros:
            results = await asyncio.wait_for(
                asyncio.gather(*coros, return_exceptions=True),
                timeout=timeout,
            )
            return [r for r in results if isinstance(r, AgentTaskInfo)]
        
        return []
    
    def get_pool_stats(self) -> Dict[str, Any]:
        """获取池统计"""
        return {
            "total_claws": len(self._wrappers),
            "total_tasks": len(self._global_tasks),
            "wrappers": {
                name: wrapper.get_stats()
                for name, wrapper in self._wrappers.items()
            },
        }


# ═══════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════

# 全局池实例
_global_pool: Optional[ClawAgentPool] = None


def get_global_agent_pool() -> ClawAgentPool:
    """获取全局ClawAgentPool单例"""
    global _global_pool
    if _global_pool is None:
        _global_pool = ClawAgentPool()
    return _global_pool


async def spawn_claw_task(
    claw_name: str,
    query: str,
    options: Optional[SpawnOptions] = None,
) -> str:
    """
    全局快捷函数：Spawn单个Claw Task。
    
    用法:
        >>> task_id = await spawn_claw_task("孔子", "什么是仁？")
        >>> pool = get_global_agent_pool()
        >>> info = await pool.wait_result(task_id)
    """
    pool = get_global_agent_pool()
    return await pool.spawn(claw_name, query, options)


async def spawn_multi_claw_tasks(
    tasks: List[Dict[str, str]],
    max_concurrent: int = 5,
) -> List[str]:
    """
    全局快捷函数：批量Spawn多Claw Task。
    
    Args:
        tasks: [{"claw_name": "...", "query": "..."}, ...]
        max_concurrent: 每个Claw最大并发
        
    Returns:
        task_id列表
    """
    pool = get_global_agent_pool()
    pool._max_per_claw = max_concurrent
    return await pool.spawn_batch(tasks)


# ═══════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════

__all__ = [
    # 状态枚举
    "TaskStatus",
    # 数据类
    "AgentTaskInfo",
    "SpawnOptions",
    # 核心类
    "ClawAgentWrapper",
    "ClawAgentPool",
    # 便捷函数
    "get_global_agent_pool",
    "spawn_claw_task",
    "spawn_multi_claw_tasks",
]
