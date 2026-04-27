# -*- coding: utf-8 -*-
"""
__all__ = [
    'get_parallel_execution_engine',
    'ProgressTracker',
    'ResultCollector',
    'ParallelExecutionEngine',
]

并行执行引擎 v2.0
在 parallel_router 基础上新增：
1. 实时进度追踪 - ProgressTracker
2. 结果回收机制 - ResultCollector
3. 汇总优化反馈 - ParallelExecutionEngine
"""

import asyncio
import logging
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

from .parallel_router import (
    ParallelMode, RouteStrategy, RouteConfig,
    ParallelTask, ParallelResult, AggregatedResult,
    ModuleRegistry, get_parallel_router
)

logger = logging.getLogger(__name__)


class TaskPhase(Enum):
    """任务阶段"""
    PENDING = "pending"          # 等待分发
    DISPATCHED = "dispatched"    # 已分发
    RUNNING = "running"          # 执行中
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"            # 执行失败
    CANCELLED = "cancelled"      # 已取消


class ProgressLevel(Enum):
    """进度详细程度"""
    SUMMARY = "summary"          # 仅统计
    DETAILED = "detailed"        # 含阶段
    FULL = "full"                # 含预计时间


@dataclass
class TaskProgress:
    """单个任务进度"""
    task_id: str
    module_key: str
    phase: TaskPhase = TaskPhase.PENDING
    progress_percent: float = 0.0     # 0.0 ~ 1.0
    current_step: str = ""             # 当前阶段描述
    steps_total: int = 1
    steps_completed: int = 0
    started_at: Optional[str] = None
    estimated_remaining_sec: float = 0.0
    result: Any = None
    error: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "module_key": self.module_key,
            "phase": self.phase.value,
            "progress_percent": round(self.progress_percent * 100, 1),
            "current_step": self.current_step,
            "steps": f"{self.steps_completed}/{self.steps_total}",
            "estimated_remaining_sec": round(self.estimated_remaining_sec, 1),
            "started_at": self.started_at,
            "error": self.error
        }


@dataclass
class ExecutionProgress:
    """整体执行进度"""
    execution_id: str
    total_tasks: int
    started_at: str
    completed_tasks: int = 0
    failed_tasks: int = 0
    running_tasks: int = 0
    pending_tasks: int = 0

    # 进度计算
    @property
    def overall_progress(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.completed_tasks / self.total_tasks

    # 预计剩余时间（秒）
    estimated_remaining_sec: float = 0.0

    # 各任务进度详情
    task_progress_map: Dict[str, TaskProgress] = field(default_factory=dict)

    def get_summary(self) -> Dict:
        """获取进度摘要"""
        return {
            "execution_id": self.execution_id,
            "total": self.total_tasks,
            "completed": self.completed_tasks,
            "failed": self.failed_tasks,
            "running": self.running_tasks,
            "pending": self.pending_tasks,
            "overall_progress": round(self.overall_progress * 100, 1),
            "estimated_remaining_sec": round(self.estimated_remaining_sec, 1)
        }

    def to_dict(self) -> Dict:
        """完整字典"""
        return {
            **self.get_summary(),
            "started_at": self.started_at,
            "task_details": {k: v.to_dict() for k, v in self.task_progress_map.items()}
        }


class ProgressTracker:
    """
    进度追踪器

    职责：
    1. 实时追踪每个子任务的进度
    2. 计算整体执行进度
    3. 估算剩余时间
    4. 提供进度回调通知
    """

    def __init__(self, total_tasks: int, progress_callback: Optional[Callable] = None):
        self.total_tasks = total_tasks
        self.progress_callback = progress_callback

        self._lock = threading.RLock()
        self._execution_id = f"exec_{uuid.uuid4().hex[:12]}"
        self._started_at = datetime.now().isoformat()

        # 各任务进度
        self._task_progress: Dict[str, TaskProgress] = {}
        # 执行开始时间
        self._start_times: Dict[str, float] = {}

    def create_task(self, task_id: str, module_key: str, steps_total: int = 1) -> TaskProgress:
        """创建任务进度追踪"""
        progress = TaskProgress(
            task_id=task_id,
            module_key=module_key,
            steps_total=steps_total
        )
        with self._lock:
            self._task_progress[task_id] = progress
        return progress

    def dispatch(self, task_id: str):
        """标记任务已分发"""
        with self._lock:
            if task_id in self._task_progress:
                p = self._task_progress[task_id]
                p.phase = TaskPhase.DISPATCHED
                self._notify()

    def start(self, task_id: str):
        """标记任务开始执行"""
        with self._lock:
            if task_id in self._task_progress:
                p = self._task_progress[task_id]
                p.phase = TaskPhase.RUNNING
                p.started_at = datetime.now().isoformat()
                self._start_times[task_id] = time.time()
                self._notify()

    def update(self, task_id: str, progress_percent: float,
               current_step: str = "", steps_completed: int = None):
        """更新任务进度"""
        with self._lock:
            if task_id in self._task_progress:
                p = self._task_progress[task_id]
                p.progress_percent = max(0.0, min(1.0, progress_percent))
                if current_step:
                    p.current_step = current_step
                if steps_completed is not None:
                    p.steps_completed = steps_completed
                # 估算剩余时间
                self._estimate_remaining(task_id, p)
                self._notify()

    def complete(self, task_id: str, result: Any = None):
        """标记任务完成"""
        with self._lock:
            if task_id in self._task_progress:
                p = self._task_progress[task_id]
                p.phase = TaskPhase.COMPLETED
                p.progress_percent = 1.0
                p.result = result
                self._notify()

    def fail(self, task_id: str, error: str):
        """标记任务失败"""
        with self._lock:
            if task_id in self._task_progress:
                p = self._task_progress[task_id]
                p.phase = TaskPhase.FAILED
                p.error = error
                self._notify()

    def _estimate_remaining(self, task_id: str, progress: TaskProgress):
        """估算剩余时间"""
        if task_id in self._start_times and progress.progress_percent > 0.01:
            elapsed = time.time() - self._start_times[task_id]
            # 剩余比例 / 已完成比例 * 已用时间
            remaining_ratio = (1.0 - progress.progress_percent) / progress.progress_percent
            progress.estimated_remaining_sec = elapsed * remaining_ratio

    def _notify(self):
        """触发进度回调"""
        if self.progress_callback:
            try:
                self.progress_callback(self.get_progress())
            except Exception as e:
                logger.debug(f"进度回调失败: {e}")

    def get_progress(self) -> ExecutionProgress:
        """获取当前整体进度"""
        with self._lock:
            completed = sum(1 for p in self._task_progress.values()
                          if p.phase == TaskPhase.COMPLETED)
            failed = sum(1 for p in self._task_progress.values()
                        if p.phase == TaskPhase.FAILED)
            running = sum(1 for p in self._task_progress.values()
                         if p.phase == TaskPhase.RUNNING)
            pending = self.total_tasks - completed - failed - running

            # 整体估算剩余时间 = 所有运行中任务的平均剩余时间
            running_progresses = [p.estimated_remaining_sec
                                for p in self._task_progress.values()
                                if p.phase == TaskPhase.RUNNING]
            avg_remaining = sum(running_progresses) / len(running_progresses) if running_progresses else 0

            return ExecutionProgress(
                execution_id=self._execution_id,
                total_tasks=self.total_tasks,
                started_at=self._started_at,
                completed_tasks=completed,
                failed_tasks=failed,
                running_tasks=running,
                pending_tasks=pending,
                estimated_remaining_sec=avg_remaining,
                task_progress_map=dict(self._task_progress)
            )

    def get_task_result(self, task_id: str) -> Optional[Any]:
        """获取已完成任务的结果"""
        with self._lock:
            if task_id in self._task_progress:
                return self._task_progress[task_id].result
        return None

    def get_all_results(self) -> Dict[str, Any]:
        """获取所有已完成任务的结果"""
        with self._lock:
            return {
                task_id: p.result
                for task_id, p in self._task_progress.items()
                if p.phase == TaskPhase.COMPLETED and p.result is not None
            }


class ResultCollector:
    """
    结果回收器

    职责：
    1. 收集子任务执行结果
    2. 验证结果完整性
    3. 持久化结果
    4. 去重与版本管理
    """

    def __init__(self, persist_callback: Optional[Callable] = None):
        self.persist_callback = persist_callback
        self._lock = threading.RLock()
        self._results: Dict[str, ParallelResult] = {}
        self._versions: Dict[str, int] = {}  # 结果版本
        self._metadata: Dict[str, Dict] = {}  # 额外元数据

    def collect(self, result: ParallelResult, metadata: Dict = None) -> bool:
        """
        回收单个结果

        Returns:
            True: 新结果
            False: 重复结果（已存在同task_id）
        """
        with self._lock:
            is_new = result.task_id not in self._results
            self._results[result.task_id] = result
            if metadata:
                self._metadata[result.task_id] = metadata

            # 版本递增
            if result.task_id in self._versions:
                self._versions[result.task_id] += 1
            else:
                self._versions[result.task_id] = 1

            # 持久化回调
            if is_new and self.persist_callback:
                try:
                    self.persist_callback(result, metadata)
                except Exception as e:
                    logger.debug(f"持久化回调失败: {e}")

            return is_new

    def get_result(self, task_id: str) -> Optional[ParallelResult]:
        """获取单个结果"""
        with self._lock:
            return self._results.get(task_id)

    def get_all_results(self) -> List[ParallelResult]:
        """获取所有结果"""
        with self._lock:
            return list(self._results.values())

    def get_successful_results(self) -> List[ParallelResult]:
        """获取成功结果"""
        with self._lock:
            return [r for r in self._results.values() if r.success]

    def get_failed_results(self) -> List[ParallelResult]:
        """获取失败结果"""
        with self._lock:
            return [r for r in self._results.values() if not r.success]

    def get_stats(self) -> Dict:
        """获取回收统计"""
        with self._lock:
            results = list(self._results.values())
            return {
                "total_collected": len(results),
                "successful": sum(1 for r in results if r.success),
                "failed": sum(1 for r in results if not r.success),
                "total_execution_time": sum(r.execution_time for r in results),
                "avg_execution_time": sum(r.execution_time for r in results) / len(results) if results else 0
            }


class ParallelExecutionEngine:
    """
    并行执行引擎 v2.0

    在 parallel_router 基础上整合：
    1. 进度追踪 - ProgressTracker
    2. 结果回收 - ResultCollector
    3. 汇总优化反馈

    执行流程：
    分发任务 → 进度追踪 → 结果回收 → 汇总优化 → 反馈迭代
    """

    def __init__(self,
                 config: Optional[RouteConfig] = None,
                 progress_callback: Optional[Callable] = None,
                 persist_callback: Optional[Callable] = None,
                 optimize_callback: Optional[Callable] = None):
        self.config = config or RouteConfig()
        self.router = get_parallel_router()

        # 进度追踪
        self.progress_callback = progress_callback
        self._tracker: Optional[ProgressTracker] = None

        # 结果回收
        self.persist_callback = persist_callback
        self.collector = ResultCollector(persist_callback=persist_callback)

        # 优化回调
        self.optimize_callback = optimize_callback

        # 执行历史（用于优化）
        self._execution_history: List[AggregatedResult] = []
        self._history_lock = threading.RLock()

    def execute(self,
                tasks: List[ParallelTask],
                track_progress: bool = True,
                collect_results: bool = True) -> AggregatedResult:
        """
        执行并行任务（带进度追踪与结果回收）

        Args:
            tasks: 并行任务列表
            track_progress: 是否启用进度追踪
            collect_results: 是否启用结果回收

        Returns:
            AggregatedResult: 聚合结果（包含优化洞察）
        """
        if not tasks:
            return AggregatedResult(
                total_tasks=0, successful_tasks=0, failed_tasks=0,
                results=[], total_time=0.0,
                strategy_used=self.config.strategy,
                mode_used=self.config.mode
            )

        logger.info(f"ParallelExecutionEngine 开始执行: {len(tasks)} 个任务")

        # 初始化进度追踪
        if track_progress:
            self._tracker = ProgressTracker(
                total_tasks=len(tasks),
                progress_callback=self.progress_callback
            )
            for task in tasks:
                self._tracker.create_task(task.task_id, task.module_key)

        start_time = time.time()
        results: List[ParallelResult] = []

        # 执行模式选择
        if self.config.mode == ParallelMode.THREAD:
            results = self._execute_with_tracking(tasks, track_progress)
        elif self.config.mode == ParallelMode.ASYNC:
            results = asyncio.run(self._execute_async_with_tracking(tasks, track_progress))
        else:
            if len(tasks) > 3:
                results = self._execute_with_tracking(tasks, track_progress)
            else:
                results = self._execute_sequential_with_tracking(tasks, track_progress)

        # 结果回收
        if collect_results:
            for result in results:
                self.collector.collect(result)
                # 进度追踪同步
                if track_progress and self._tracker:
                    if result.success:
                        self._tracker.complete(result.task_id, result.output)
                    else:
                        self._tracker.fail(result.task_id, result.error or "Unknown error")

        total_time = time.time() - start_time

        # 聚合结果
        aggregated = self._aggregate_with_optimization(results, total_time)

        # 保存历史用于优化
        self._save_to_history(aggregated)

        logger.info(
            f"ParallelExecutionEngine 完成: "
            f"{aggregated.successful_tasks}/{aggregated.total_tasks} 成功, "
            f"耗时 {total_time:.2f}s"
        )

        return aggregated

    def _execute_with_tracking(self,
                               tasks: List[ParallelTask],
                               track: bool) -> List[ParallelResult]:
        """线程池执行（带进度追踪）"""
        results = []
        max_workers = min(self.config.max_concurrent, len(tasks))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures: Dict[Future, ParallelTask] = {}

            for task in tasks:
                if track and self._tracker:
                    self._tracker.dispatch(task.task_id)
                future = executor.submit(
                    self._execute_task_with_progress,
                    task,
                    self.config.timeout,
                    track
                )
                futures[future] = task

            for future in futures:
                task = futures[future]
                try:
                    result = future.result(timeout=self.config.timeout * len(tasks))
                    results.append(result)
                except Exception as e:
                    results.append(ParallelResult(
                        task_id=task.task_id,
                        module_key=task.module_key,
                        success=False,
                        error="执行失败"
                    ))

        return results

    def _execute_task_with_progress(self,
                                    task: ParallelTask,
                                    timeout: float,
                                    track: bool) -> ParallelResult:
        """执行单个任务（带进度更新）"""
        start_time = time.time()

        try:
            if track and self._tracker:
                self._tracker.start(task.task_id)
                self._tracker.update(task.task_id, 0.3, "开始执行")

            handler = self.router.registry.get(task.module_key)
            if not handler:
                raise ValueError(f"模块未注册: {task.module_key}")

            if track and self._tracker:
                self._tracker.update(task.task_id, 0.5, "处理中")

            output = handler(**task.params)
            execution_time = time.time() - start_time

            if track and self._tracker:
                self._tracker.update(task.task_id, 0.9, "完成中")

            self.router.registry.update_performance(task.module_key, True, execution_time)

            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=True,
                output=output,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.router.registry.update_performance(task.module_key, False, execution_time)

            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=False,
                error="执行失败",
                execution_time=execution_time
            )

    async def _execute_async_with_tracking(self,
                                           tasks: List[ParallelTask],
                                           track: bool) -> List[ParallelResult]:
        """异步执行（带进度追踪）"""
        semaphore = asyncio.Semaphore(self.config.max_concurrent)

        async def limited_exec(task: ParallelTask):
            async with semaphore:
                return await self._execute_async_task_with_progress(task, track)

        results = await asyncio.gather(
            *[limited_exec(t) for t in tasks],
            return_exceptions=True
        )

        processed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed.append(ParallelResult(
                    task_id=tasks[i].task_id,
                    module_key=tasks[i].module_key,
                    success=False,
                    error=str(result)
                ))
            else:
                processed.append(result)
        return processed

    async def _execute_async_task_with_progress(self,
                                               task: ParallelTask,
                                               track: bool) -> ParallelResult:
        """异步执行单个任务"""
        start_time = time.time()

        try:
            if track and self._tracker:
                self._tracker.start(task.task_id)

            handler = self.router.registry.get(task.module_key)
            if not handler:
                raise ValueError(f"模块未注册: {task.module_key}")

            if asyncio.iscoroutinefunction(handler):
                output = await handler(**task.params)
            else:
                output = handler(**task.params)

            execution_time = time.time() - start_time
            self.router.registry.update_performance(task.module_key, True, execution_time)

            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=True,
                output=output,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.router.registry.update_performance(task.module_key, False, execution_time)
            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=False,
                error="执行失败",
                execution_time=execution_time
            )

    def _execute_sequential_with_tracking(self,
                                          tasks: List[ParallelTask],
                                          track: bool) -> List[ParallelResult]:
        """顺序执行（带进度追踪）"""
        results = []
        for task in tasks:
            result = self._execute_task_with_progress(task, self.config.timeout, track)
            results.append(result)
        return results

    def _aggregate_with_optimization(self,
                                    results: List[ParallelResult],
                                    total_time: float) -> AggregatedResult:
        """聚合结果（带优化洞察）"""
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        # 基础聚合（复用 router 逻辑）
        insights = self.router._extract_insights(successful)
        conflicts = self.router._detect_conflicts(successful)

        # 优化洞察
        optimization_insights = self._generate_optimization_insights(results, total_time)
        insights.extend(optimization_insights)

        # 执行优化回调
        if self.optimize_callback:
            try:
                optimization_action = self.optimize_callback(results, optimization_insights)
                if optimization_action:
                    insights.append(f"优化建议: {optimization_action}")
            except Exception as e:
                logger.debug(f"优化回调失败: {e}")

        return AggregatedResult(
            total_tasks=len(results),
            successful_tasks=len(successful),
            failed_tasks=len(failed),
            results=results,
            total_time=total_time,
            strategy_used=self.config.strategy,
            mode_used=self.config.mode,
            insights=insights,
            conflicts=conflicts
        )

    def _generate_optimization_insights(self,
                                       results: List[ParallelResult],
                                       total_time: float) -> List[str]:
        """生成优化洞察"""
        insights = []

        if not results:
            return insights

        # 1. 性能洞察
        total_execution = sum(r.execution_time for r in results)
        avg_execution = total_execution / len(results)
        max_execution = max(r.execution_time for r in results)

        if max_execution > avg_execution * 2:
            slow_modules = [r.module_key for r in results
                         if r.execution_time > avg_execution * 1.5]
            insights.append(f"性能瓶颈: {slow_modules} 执行时间较长，建议优化或降级")

        # 2. 成功率洞察
        success_rate = len([r for r in results if r.success]) / len(results)
        if success_rate < 0.8:
            failed_modules = [r.module_key for r in results if not r.success]
            insights.append(f"成功率偏低({success_rate:.0%}): {failed_modules} 需要检查")

        # 3. 并行效率洞察
        if len(results) > 1:
            # 理想时间 = 最长单任务时间
            ideal_time = max(r.execution_time for r in results)
            overhead_ratio = total_time / ideal_time if ideal_time > 0 else 1
            if overhead_ratio > 1.5:
                insights.append(f"并行开销较大(开销率: {overhead_ratio:.1f}x)，考虑减少并发数")

        return insights

    def _save_to_history(self, aggregated: AggregatedResult):
        """保存到历史（用于后续优化）"""
        with self._history_lock:
            self._execution_history.append(aggregated)
            # 只保留最近100条
            if len(self._execution_history) > 100:
                self._execution_history.pop(0)

    def get_execution_summary(self) -> Dict:
        """获取执行摘要"""
        progress = self._tracker.get_progress() if self._tracker else None
        collector_stats = self.collector.get_stats()

        return {
            "progress": progress.get_summary() if progress else None,
            "collector_stats": collector_stats,
            "history_count": len(self._execution_history)
        }

    def get_progress(self) -> Optional[ExecutionProgress]:
        """获取当前进度"""
        return self._tracker.get_progress() if self._tracker else None


# ── 全局实例 ──────────────────────────────────────────────────

_parallel_execution_engine: Optional[ParallelExecutionEngine] = None
_engine_lock = threading.Lock()


def get_parallel_execution_engine(
    config: Optional[RouteConfig] = None,
    progress_callback: Optional[Callable] = None,
    persist_callback: Optional[Callable] = None,
    optimize_callback: Optional[Callable] = None
) -> ParallelExecutionEngine:
    """获取并行执行引擎单例"""
    global _parallel_execution_engine
    if _parallel_execution_engine is None:
        with _engine_lock:
            if _parallel_execution_engine is None:
                _parallel_execution_engine = ParallelExecutionEngine(
                    config=config,
                    progress_callback=progress_callback,
                    persist_callback=persist_callback,
                    optimize_callback=optimize_callback
                )
    return _parallel_execution_engine
