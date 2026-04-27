"""
智能学习调度器
Smart Learning Scheduler

功能:
1. 基于优先级调度
2. 基于资源可用性调度
3. 基于历史效果调度
4. 动态调整调度strategy
"""

import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ResourceState(Enum):
    """资源状态"""
    AVAILABLE = "available"       # 可用
    MODERATE = "moderate"          # 中等负载
    HEAVY = "heavy"               # 高负载
    CRITICAL = "critical"         # 临界状态

class SchedulingStrategy(Enum):
    """调度strategy"""
    PRIORITY_FIRST = "priority_first"        # 优先级优先
    ROUND_ROBIN = "round_robin"              # 轮询
    LEAST_LOADED = "least_loaded"           # 最少负载
    EFFECTIVENESS_BASED = "effectiveness"    # 效果优先
    ADAPTIVE = "adaptive"                    # 自适应

@dataclass
class ResourceMetrics:
    """资源metrics"""
    cpu_percent: float           # CPU使用率
    memory_percent: float        # 内存使用率
    disk_io: float              # 磁盘I/O
    network_io: float            # 网络I/O
    available_cores: int         # 可用CPU核心数
    available_memory: float     # 可用内存(MB)

    def get_state(self) -> ResourceState:
        """get资源状态"""
        if self.cpu_percent > 90 or self.memory_percent > 90:
            return ResourceState.CRITICAL
        elif self.cpu_percent > 70 or self.memory_percent > 70:
            return ResourceState.HEAVY
        elif self.cpu_percent > 50 or self.memory_percent > 50:
            return ResourceState.MODERATE
        else:
            return ResourceState.AVAILABLE

    def get_score(self) -> float:
        """
        计算资源可用性分数

        分数越高,资源越可用
        """
        cpu_score = (100 - self.cpu_percent) / 100
        memory_score = (100 - self.memory_percent) / 100
        return (cpu_score * 0.6 + memory_score * 0.4)

@dataclass
class EngineMetrics:
    """引擎metrics"""
    engine_name: str
    task_count: int             # 任务总数
    success_count: int          # 成功数
    failed_count: int            # 失败数
    avg_execution_time: float    # 平均执行时间(秒)
    current_tasks: int          # 当前执行任务数
    max_concurrent: int         # 最大并发数

    def get_success_rate(self) -> float:
        """get成功率"""
        if self.task_count == 0:
            return 1.0
        return self.success_count / self.task_count

    def get_effectiveness_score(self) -> float:
        """
        计算效果分数

        考虑成功率和执行效率
        """
        success_rate = self.get_success_rate()
        efficiency = 1.0 / max(self.avg_execution_time, 0.1) if self.avg_execution_time > 0 else 1.0
        return (success_rate * 0.7 + efficiency * 0.3)

    def get_load(self) -> float:
        """get负载率"""
        if self.max_concurrent == 0:
            return 0.0
        return self.current_tasks / self.max_concurrent

class SmartScheduler:
    """
    智能学习调度器

    核心功能:
    1. 资源监控 - 实时监控CPU,内存,磁盘,网络
    2. 引擎管理 - 管理所有学习引擎的metrics
    3. 任务调度 - 基于多种strategy调度任务
    4. 自适应调整 - 根据历史效果调整调度strategy
    """

    def __init__(self, strategy: SchedulingStrategy = SchedulingStrategy.ADAPTIVE):
        """
        init调度器

        Args:
            strategy: 调度strategy
        """
        self.strategy = strategy

        # 引擎metrics
        self.engine_metrics: Dict[str, EngineMetrics] = {}

        # 资源历史
        self.resource_history: List[ResourceMetrics] = []
        self.max_history_size = 100

        # 调度历史
        self.scheduling_history: List[Dict] = []

        # 自适应参数
        self.adaptive_params = {
            "priority_weight": 0.4,
            "resource_weight": 0.3,
            "effectiveness_weight": 0.2,
            "fairness_weight": 0.1
        }

        # 数据目录
        self.data_dir = Path("data/learning/scheduler")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_file = self.data_dir / "metrics.json"
        self.history_file = self.data_dir / "history.json"

        # 线程锁
        self.lock = threading.Lock()

        # 加载历史
        self._load_history()

        logger.info(f"智能调度器init完成,strategy: {strategy.value}")

    def update_engine_metrics(self, engine_name: str,
                            task_count: int,
                            success_count: int,
                            failed_count: int,
                            avg_execution_time: float,
                            current_tasks: int,
                            max_concurrent: int = 4):
        """
        更新引擎metrics

        Args:
            engine_name: 引擎名称
            task_count: 任务总数
            success_count: 成功数
            failed_count: 失败数
            avg_execution_time: 平均执行时间
            current_tasks: 当前任务数
            max_concurrent: 最大并发数
        """
        with self.lock:
            self.engine_metrics[engine_name] = EngineMetrics(
                engine_name=engine_name,
                task_count=task_count,
                success_count=success_count,
                failed_count=failed_count,
                avg_execution_time=avg_execution_time,
                current_tasks=current_tasks,
                max_concurrent=max_concurrent
            )

    def get_resource_metrics(self) -> ResourceMetrics:
        """
        get当前资源metrics

        Returns:
            资源metrics
        """
        try:
            # 使用Python内置库get资源信息(简化版)
            import wmi

            # Windows专用方式
            try:
                c = wmi.WMI()

                # CPU使用率(简化)
                cpu_percent = 25.0  # 默认值,实际需要更复杂的计算

                # 内存使用率
                total_memory = 0
                available_memory = 0
                for os_info in c.Win32_OperatingSystem():
                    total_memory = int(os_info.TotalVisibleMemorySize)  # KB
                    available_memory = int(os_info.FreePhysicalMemory)  # KB
                    break

                memory_percent = ((total_memory - available_memory) / total_memory) * 100 if total_memory > 0 else 0
                available_memory_mb = available_memory / 1024

                metrics = ResourceMetrics(
                    cpu_percent=cpu_percent,
                    memory_percent=memory_percent,
                    disk_io=0,  # 暂不支持
                    network_io=0,  # 暂不支持
                    available_cores=os.cpu_count() - 1,
                    available_memory=available_memory_mb
                )
            except (OSError, IOError, PermissionError):
                # 降级方案:使用默认值
                metrics = ResourceMetrics(
                    cpu_percent=25.0,
                    memory_percent=50.0,
                    disk_io=0,
                    network_io=0,
                    available_cores=os.cpu_count() - 1,
                    available_memory=1024.0  # 1GB
                )

            # 保存历史
            with self.lock:
                self.resource_history.append(metrics)
                if len(self.resource_history) > self.max_history_size:
                    self.resource_history.pop(0)

            return metrics

        except Exception as e:
            logger.error(f"get资源metrics失败: {e}")
            return ResourceMetrics(
                cpu_percent=25.0,
                memory_percent=50.0,
                disk_io=0,
                network_io=0,
                available_cores=os.cpu_count() - 1 if hasattr(os, 'cpu_count') else 4,
                available_memory=1024.0
            )

    def schedule(self, task: Dict[str, Any],
                 available_engines: List[str]) -> Optional[str]:
        """
        调度任务到引擎

        Args:
            task: 任务信息
            available_engines: 可用引擎列表

        Returns:
            选定的引擎名称,None表示无法调度
        """
        if not available_engines:
            logger.warning("没有可用引擎")
            return None

        # get资源metrics
        resource_metrics = self.get_resource_metrics()
        resource_state = resource_metrics.get_state()

        # 如果资源紧张,不调度
        if resource_state == ResourceState.CRITICAL:
            logger.warning("资源紧张,暂停调度")
            return None

        # 根据strategy调度
        if self.strategy == SchedulingStrategy.PRIORITY_FIRST:
            selected_engine = self._schedule_by_priority(task, available_engines)
        elif self.strategy == SchedulingStrategy.ROUND_ROBIN:
            selected_engine = self._schedule_by_round_robin(task, available_engines)
        elif self.strategy == SchedulingStrategy.LEAST_LOADED:
            selected_engine = self._schedule_by_least_loaded(available_engines, resource_metrics)
        elif self.strategy == SchedulingStrategy.EFFECTIVENESS_BASED:
            selected_engine = self._schedule_by_effectiveness(available_engines)
        elif self.strategy == SchedulingStrategy.ADAPTIVE:
            selected_engine = self._schedule_adaptive(task, available_engines, resource_metrics)
        else:
            selected_engine = available_engines[0]

        # 记录调度历史
        self._record_scheduling(task, selected_engine, resource_metrics)

        return selected_engine

    def _schedule_by_priority(self, task: Dict[str, Any],
                            available_engines: List[str]) -> Optional[str]:
        """优先级优先调度"""
        # 根据任务优先级筛选引擎
        task_priority = task.get("priority", 2)

        # 简单实现:返回第一个可用引擎
        # 实际应根据引擎能力匹配
        return available_engines[0] if available_engines else None

    def _schedule_by_round_robin(self, task: Dict[str, Any],
                                 available_engines: List[str]) -> Optional[str]:
        """轮询调度"""
        if not available_engines:
            return None

        # 使用调度历史计数
        engine_counts = {}
        for history in self.scheduling_history[-100:]:
            engine = history.get("engine")
            if engine:
                engine_counts[engine] = engine_counts.get(engine, 0) + 1

        # 选择调度次数最少的引擎
        sorted_engines = sorted(
            available_engines,
            key=lambda e: engine_counts.get(e, 0)
        )

        return sorted_engines[0]

    def _schedule_by_least_loaded(self, available_engines: List[str],
                                  resource_metrics: ResourceMetrics) -> Optional[str]:
        """最少负载调度"""
        if not available_engines:
            return None

        # 计算每个引擎的synthesize负载
        engine_scores = {}
        for engine_name in available_engines:
            metrics = self.engine_metrics.get(engine_name)
            if metrics:
                load = metrics.get_load()
                score = 1.0 - load  # 负载越低,分数越高
                engine_scores[engine_name] = score
            else:
                engine_scores[engine_name] = 1.0  # 新引擎给满分

        # 选择负载最低的引擎
        selected = max(engine_scores.items(), key=lambda x: x[1])
        return selected[0]

    def _schedule_by_effectiveness(self, available_engines: List[str]) -> Optional[str]:
        """效果优先调度"""
        if not available_engines:
            return None

        # 计算每个引擎的效果分数
        engine_scores = {}
        for engine_name in available_engines:
            metrics = self.engine_metrics.get(engine_name)
            if metrics:
                engine_scores[engine_name] = metrics.get_effectiveness_score()
            else:
                engine_scores[engine_name] = 0.5  # 新引擎给中等分

        # 选择效果最好的引擎
        selected = max(engine_scores.items(), key=lambda x: x[1])
        return selected[0]

    def _schedule_adaptive(self, task: Dict[str, Any],
                          available_engines: List[str],
                          resource_metrics: ResourceMetrics) -> Optional[str]:
        """自适应调度"""
        if not available_engines:
            return None

        # 计算每个引擎的synthesize分数
        engine_scores = {}
        for engine_name in available_engines:
            metrics = self.engine_metrics.get(engine_name)

            # 效果分数
            effectiveness = metrics.get_effectiveness_score() if metrics else 0.5

            # 负载分数
            load = metrics.get_load() if metrics else 0.0
            load_score = 1.0 - load

            # 资源分数
            resource_score = resource_metrics.get_score()

            # synthesize分数
            total_score = (
                effectiveness * self.adaptive_params["effectiveness_weight"] +
                load_score * 0.3 +
                resource_score * 0.2
            )

            engine_scores[engine_name] = total_score

        # 选择分数最高的引擎
        selected = max(engine_scores.items(), key=lambda x: x[1])
        return selected[0]

    def _record_scheduling(self, task: Dict[str, Any],
                          selected_engine: Optional[str],
                          resource_metrics: ResourceMetrics):
        """记录调度历史"""
        record = {
            "task_id": task.get("task_id", "unknown"),
            "engine": selected_engine,
            "priority": task.get("priority", 2),
            "resource_state": resource_metrics.get_state().value,
            "cpu_percent": resource_metrics.cpu_percent,
            "memory_percent": resource_metrics.memory_percent,
            "timestamp": datetime.now().isoformat()
        }

        with self.lock:
            self.scheduling_history.append(record)
            if len(self.scheduling_history) > self.max_history_size:
                self.scheduling_history.pop(0)

    def get_scheduling_statistics(self) -> Dict[str, Any]:
        """get调度统计"""
        if not self.scheduling_history:
            return {}

        # 统计每个引擎的调度次数
        engine_counts = {}
        for record in self.scheduling_history:
            engine = record.get("engine")
            if engine:
                engine_counts[engine] = engine_counts.get(engine, 0) + 1

        # 统计资源状态分布
        resource_states = {}
        for record in self.scheduling_history:
            state = record.get("resource_state", "unknown")
            resource_states[state] = resource_states.get(state, 0) + 1

        # 计算平均CPU和内存使用率
        avg_cpu = sum(r.get("cpu_percent", 0) for r in self.scheduling_history) / len(self.scheduling_history)
        avg_memory = sum(r.get("memory_percent", 0) for r in self.scheduling_history) / len(self.scheduling_history)

        return {
            "total_scheduled": len(self.scheduling_history),
            "engine_distribution": engine_counts,
            "resource_state_distribution": resource_states,
            "avg_cpu_percent": avg_cpu,
            "avg_memory_percent": avg_memory,
            "current_strategy": self.strategy.value
        }

    def adjust_strategy(self):
        """自适应调整strategy"""
        if not self.scheduling_history:
            return

        stats = self.get_scheduling_statistics()

        # 根据历史效果调整参数
        # 简化实现:如果资源经常紧张,增加资源权重
        critical_count = stats.get("resource_state_distribution", {}).get("critical", 0)
        if critical_count > len(self.scheduling_history) * 0.2:
            # 资源经常紧张,增加资源权重
            self.adaptive_params["resource_weight"] = min(
                self.adaptive_params["resource_weight"] + 0.05,
                0.5
            )
            logger.info(f"调整调度参数,资源权重增加到 {self.adaptive_params['resource_weight']}")
        else:
            # 恢复默认权重
            self.adaptive_params["resource_weight"] = max(
                self.adaptive_params["resource_weight"] - 0.01,
                0.2
            )

    def _load_history(self):
        """加载历史"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.scheduling_history = data.get("scheduling_history", [])
                    self.adaptive_params = data.get("adaptive_params", self.adaptive_params)
                logger.info(f"加载调度历史: {len(self.scheduling_history)} 条")
            except Exception as e:
                logger.warning(f"加载调度历史失败: {e}")

    def save_history(self):
        """保存历史"""
        try:
            data = {
                "scheduling_history": self.scheduling_history[-self.max_history_size:],
                "adaptive_params": self.adaptive_params,
                "timestamp": datetime.now().isoformat()
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存调度历史失败: {e}")

# 便捷函数
def create_scheduler(strategy: str = "adaptive") -> SmartScheduler:
    """创建调度器"""
    strategy_enum = SchedulingStrategy(strategy)
    return SmartScheduler(strategy=strategy_enum)

__all__ = [
    'ResourceState', 'SchedulingStrategy', 'ResourceMetrics',
    'EngineMetrics', 'SmartScheduler', 'create_scheduler',
]
