"""
__all__ = [
    'end_execution',
    'generate_report',
    'get_chain_health',
    'get_execution_summary',
    'get_full_status',
    'get_main_chain_monitor',
    'get_mode_distribution',
    'get_node_status',
    'record_node_call',
    'start_execution',
    'success_rate',
]

主线监控与可视化模块
提供执行追踪、性能监控和状态可视化功能
"""

import time
import threading
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict

class ExecutionState(Enum):
    """执行状态"""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"

class RunMode(Enum):
    """运行模式"""
    SERIAL = "serial"
    PARALLEL = "parallel"
    CROSS = "cross"

@dataclass
class ExecutionRecord:
    """执行记录"""
    record_id: str
    task_id: str
    mode: str
    started_at: str
    completed_at: Optional[str] = None
    duration_ms: float = 0.0
    state: str = "running"
    nodes_executed: List[str] = field(default_factory=list)
    signals_sent: int = 0
    modules_evolved: int = 0
    success: bool = False
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NodeMetrics:
    """节点指标"""
    node_id: str
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_duration_ms: float = 0.0
    avg_duration_ms: float = 0.0
    last_called: Optional[str] = None

    @property
    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.successful_calls / self.total_calls

class MainChainMonitor:
    """
    主线监控器

    功能：
    1. 执行追踪 - 记录每次执行的详细信息
    2. 性能监控 - 统计节点调用和执行时间
    3. 状态可视化 - 提供执行状态概览
    4. 历史记录 - 保存执行历史供分析
    """

    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self._lock = threading.RLock()
        self._records: List[ExecutionRecord] = []
        self._current_execution: Optional[Dict[str, Any]] = None
        self._node_metrics: Dict[str, NodeMetrics] = {}
        self._mode_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {
            "total": 0, "success": 0, "failed": 0
        })

    def start_execution(
        self,
        task_id: str,
        mode: str,
        nodes: List[str] = None
    ) -> str:
        """开始执行追踪"""
        with self._lock:
            record_id = f"exec_{int(time.time() * 1000)}"
            record = ExecutionRecord(
                record_id=record_id,
                task_id=task_id,
                mode=mode,
                started_at=datetime.now().isoformat(),
                nodes_executed=nodes or []
            )
            self._current_execution = {"record_id": record_id, "record": record}
            return record_id

    def end_execution(
        self,
        record_id: str,
        state: str = "success",
        signals: int = 0,
        modules_evolved: int = 0,
        error: str = None,
        metadata: Dict = None
    ):
        """结束执行追踪"""
        with self._lock:
            if self._current_execution and self._current_execution["record_id"] == record_id:
                record = self._current_execution["record"]
                record.completed_at = datetime.now().isoformat()
                record.state = state
                record.success = state == "success"
                record.signals_sent = signals
                record.modules_evolved = modules_evolved
                record.error = error
                record.metadata = metadata or {}

                # 计算执行时间
                start = datetime.fromisoformat(record.started_at)
                end = datetime.fromisoformat(record.completed_at)
                record.duration_ms = (end - start).total_seconds() * 1000

                # 保存记录
                self._records.append(record)
                if len(self._records) > self.max_history:
                    self._records.pop(0)

                # 更新统计
                self._mode_stats[record.mode]["total"] += 1
                if state == "success":
                    self._mode_stats[record.mode]["success"] += 1
                else:
                    self._mode_stats[record.mode]["failed"] += 1

                self._current_execution = None

    def record_node_call(
        self,
        node_id: str,
        duration_ms: float,
        success: bool
    ):
        """记录节点调用"""
        with self._lock:
            if node_id not in self._node_metrics:
                self._node_metrics[node_id] = NodeMetrics(node_id=node_id)

            metrics = self._node_metrics[node_id]
            metrics.total_calls += 1
            metrics.total_duration_ms += duration_ms
            metrics.avg_duration_ms = metrics.total_duration_ms / metrics.total_calls
            metrics.last_called = datetime.now().isoformat()

            if success:
                metrics.successful_calls += 1
            else:
                metrics.failed_calls += 1

    def get_execution_summary(self) -> Dict[str, Any]:
        """获取执行摘要"""
        with self._lock:
            total = len(self._records)
            success = sum(1 for r in self._records if r.success)
            failed = sum(1 for r in self._records if not r.success and r.state == "failed")

            # 计算平均执行时间
            durations = [r.duration_ms for r in self._records if r.duration_ms > 0]
            avg_duration = sum(durations) / len(durations) if durations else 0

            return {
                "total_executions": total,
                "success_count": success,
                "failed_count": failed,
                "partial_count": total - success - failed,
                "success_rate": success / total if total > 0 else 0,
                "avg_duration_ms": round(avg_duration, 2),
                "mode_stats": dict(self._mode_stats),
                "recent_executions": [
                    {
                        "task_id": r.task_id,
                        "mode": r.mode,
                        "state": r.state,
                        "duration_ms": round(r.duration_ms, 2)
                    }
                    for r in self._records[-5:]
                ]
            }

    def get_node_status(self) -> List[Dict[str, Any]]:
        """获取节点状态"""
        with self._lock:
            return [
                {
                    "node_id": m.node_id,
                    "total_calls": m.total_calls,
                    "success_rate": round(m.success_rate * 100, 1),
                    "avg_duration_ms": round(m.avg_duration_ms, 2),
                    "last_called": m.last_called
                }
                for m in self._node_metrics.values()
            ]

    def get_mode_distribution(self) -> Dict[str, int]:
        """获取模式分布"""
        with self._lock:
            return {mode: stats["total"] for mode, stats in self._mode_stats.items()}

    def get_chain_health(self) -> Dict[str, Any]:
        """获取链路健康状态"""
        with self._lock:
            total = len(self._records)
            if total == 0:
                return {
                    "health": "unknown",
                    "message": "暂无执行记录",
                    "recent_success_rate": 0.0,
                    "total_executions": 0,
                    "avg_duration_ms": 0.0
                }

            recent = self._records[-10:] if len(self._records) >= 10 else self._records
            recent_success = sum(1 for r in recent if r.success)
            recent_rate = recent_success / len(recent)

            if recent_rate >= 0.9:
                health = "healthy"
                message = "运行良好"
            elif recent_rate >= 0.7:
                health = "warning"
                message = "存在部分失败"
            else:
                health = "critical"
                message = "失败率较高"

            return {
                "health": health,
                "message": message,
                "recent_success_rate": round(recent_rate * 100, 1),
                "total_executions": total,
                "avg_duration_ms": round(
                    sum(r.duration_ms for r in self._records) / total, 2
                ) if total > 0 else 0
            }

    def generate_report(self) -> str:
        """生成监控报告"""
        summary = self.get_execution_summary()
        health = self.get_chain_health()
        nodes = self.get_node_status()
        modes = self.get_mode_distribution()

        report = []
        report.append("=" * 60)
        report.append("主线监控报告")
        report.append("=" * 60)
        report.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        report.append("\n【链路健康】")
        report.append(f"  状态: {health['health']}")
        report.append(f"  消息: {health['message']}")
        report.append(f"  近10次成功率: {health['recent_success_rate']}%")

        report.append("\n【执行统计】")
        report.append(f"  总执行次数: {summary['total_executions']}")
        report.append(f"  成功: {summary['success_count']}")
        report.append(f"  失败: {summary['failed_count']}")
        report.append(f"  成功率: {summary['success_rate'] * 100:.1f}%")
        report.append(f"  平均耗时: {summary['avg_duration_ms']:.2f}ms")

        report.append("\n【模式分布】")
        for mode, count in modes.items():
            report.append(f"  {mode}: {count} 次")

        if nodes:
            report.append("\n【节点状态】")
            for node in sorted(nodes, key=lambda x: x["total_calls"], reverse=True)[:5]:
                report.append(f"  {node['node_id']}: {node['total_calls']} 次调用, "
                           f"{node['success_rate']}% 成功率")

        report.append("\n" + "=" * 60)
        return "\n".join(report)

    def get_full_status(self) -> Dict[str, Any]:
        """获取完整状态"""
        return {
            "execution_summary": self.get_execution_summary(),
            "chain_health": self.get_chain_health(),
            "node_status": self.get_node_status(),
            "mode_distribution": self.get_mode_distribution(),
            "current_execution": self._current_execution is not None
        }

# 全局单例
_main_chain_monitor: Optional[MainChainMonitor] = None

def get_main_chain_monitor() -> MainChainMonitor:
    """获取主线监控器单例"""
    global _main_chain_monitor
    if _main_chain_monitor is None:
        _main_chain_monitor = MainChainMonitor()
    return _main_chain_monitor
