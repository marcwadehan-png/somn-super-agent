"""
unified学习协调器
Unified Learning Coordinator

职责:
1. unified管理所有学习引擎
2. 智能调度学习任务
3. 优先级管理
4. 资源优化
5. 进度监控
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 添加项目路径
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__)

logger = logging.getLogger(__name__)

class LearningPriority(Enum):
    """学习优先级"""
    P0_CRITICAL = 0  # 关键 - 最高优先级
    P1_HIGH = 1      # 高 - 重要任务
    P2_MEDIUM = 2    # 中 - 常规任务
    P3_LOW = 3       # 低 - 补充任务

class LearningTaskStatus(Enum):
    """学习系统任务状态（区别于其他模块的TaskStatus）"""
    PENDING = "pending"           # 待执行
    QUEUED = "queued"             # 已排队
    IN_PROGRESS = "in_progress"    # 执行中
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 失败
    CANCELLED = "cancelled"       # 已取消

@dataclass
class LearningTask:
    """学习任务"""
    task_id: str
    engine_type: str              # 引擎类型: local_data, neural_memory, smart_learning, etc.
    priority: LearningPriority
    status: LearningTaskStatus = LearningTaskStatus.PENDING

    # 任务内容
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 执行信息
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None

    # 评分
    relevance_score: float = 0.5  # 相关性 0-1
    confidence_score: float = 0.5  # 置信度 0-1
    estimated_time: float = 5.0    # 预计耗时(分钟)

    def calculate_priority_score(self) -> float:
        """
        计算任务优先级评分

        评分算法:
        score = priority_weight * 0.4 +
                relevance * 0.3 +
                confidence * 0.2 +
                (1/estimated_time) * 0.1
        """
        priority_weight = 1.0 - (self.priority.value / 4.0)  # P0=1.0, P3=0.25

        return (priority_weight * 0.4 +
                self.relevance_score * 0.3 +
                self.confidence_score * 0.2 +
                (1.0 / max(self.estimated_time, 0.1)) * 0.1)

@dataclass
class EngineStatus:
    """引擎状态"""
    engine_name: str
    is_active: bool = True
    task_count: int = 0
    success_rate: float = 1.0
    avg_execution_time: float = 0.0
    last_execution: Optional[str] = None

class LearningCoordinator:
    """
    unified学习协调器

    核心功能:
    1. 任务队列管理
    2. 智能调度
    3. 资源管理
    4. 引擎管理
    5. 进度监控
    """

    def __init__(self, max_workers: int = 4):
        """init协调器"""
        self.max_workers = max_workers

        # 任务队列
        self.task_queue: List[LearningTask] = []
        self.completed_tasks: List[LearningTask] = []
        self.failed_tasks: List[LearningTask] = []

        # 引擎注册表
        self.engines: Dict[str, Any] = {}
        self.engine_status: Dict[str, EngineStatus] = {}

        # 学习引擎实例
        self.engine_instances: Dict[str, Any] = {}

        # 线程锁
        self.queue_lock = threading.Lock()
        self.status_lock = threading.Lock()

        # 数据目录
        self.data_dir = Path("data/learning/unified")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = self.data_dir / "progress.json"
        self.report_file = self.data_dir / "daily_report.json"

        # 统计信息
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_learning_time": 0.0,
            "engine_stats": {}
        }

        # 加载进度
        self._load_progress()

    def register_engine(self, name: str, engine_class, config: Optional[Dict] = None):
        """
        注册学习引擎

        Args:
            name: 引擎名称
            engine_class: 引擎类
            config: 配置参数
        """
        try:
            # 实例化引擎
            if config:
                engine_instance = engine_class(**config)
            else:
                engine_instance = engine_class()

            self.engines[name] = engine_class
            self.engine_instances[name] = engine_instance
            self.engine_status[name] = EngineStatus(engine_name=name)

            logger.info(f"成功注册学习引擎: {name}")
            return True

        except Exception as e:
            logger.error(f"注册引擎 {name} 失败: {e}")
            return False

    def submit_task(self, task: LearningTask) -> str:
        """
        提交学习任务

        Args:
            task: 学习任务

        Returns:
            任务ID
        """
        with self.queue_lock:
            self.task_queue.append(task)
            self.task_queue.sort(key=lambda t: t.calculate_priority_score(), reverse=True)
            self.stats["total_tasks"] += 1

        logger.info(f"任务已提交: {task.task_id} (优先级: {task.priority.name})")
        return task.task_id

    def submit_tasks_batch(self, tasks: List[LearningTask]) -> List[str]:
        """
        批量提交任务

        Args:
            tasks: 任务列表

        Returns:
            任务ID列表
        """
        task_ids = []
        with self.queue_lock:
            self.task_queue.extend(tasks)
            self.task_queue.sort(key=lambda t: t.calculate_priority_score(), reverse=True)
            self.stats["total_tasks"] += len(tasks)
            task_ids = [t.task_id for t in tasks]

        logger.info(f"批量提交 {len(tasks)} 个任务")
        return task_ids

    def get_next_task(self) -> Optional[LearningTask]:
        """get下一个待执行任务"""
        with self.queue_lock:
            for task in self.task_queue:
                if task.status == LearningTaskStatus.PENDING:
                    return task
        return None

    def execute_task(self, task: LearningTask) -> Dict[str, Any]:
        """
        执行单个学习任务

        Args:
            task: 学习任务

        Returns:
            执行结果
        """
        task.status = LearningTaskStatus.IN_PROGRESS
        task.started_at = datetime.now().isoformat()

        engine_instance = self.engine_instances.get(task.engine_type)
        if not engine_instance:
            error_msg = f"引擎 {task.engine_type} 未注册"
            task.error = error_msg
            task.status = LearningTaskStatus.FAILED
            self.failed_tasks.append(task)
            return {"success": False, "error": error_msg}

        try:
            # 调用引擎的 learn 方法
            if hasattr(engine_instance, 'learn'):
                result = engine_instance.learn(task.data)
            elif hasattr(engine_instance, 'process'):
                result = engine_instance.process(task.data)
            elif hasattr(engine_instance, 'analyze'):
                result = engine_instance.analyze(task.data)
            else:
                # 默认调用
                result = engine_instance(task.data)

            task.result = result
            task.status = LearningTaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()

            # 更新引擎状态
            with self.status_lock:
                status = self.engine_status[task.engine_type]
                status.task_count += 1
                status.last_execution = task.completed_at

            # 更新统计
            self.completed_tasks.append(task)
            self.stats["completed_tasks"] += 1

            logger.info(f"任务执行成功: {task.task_id}")
            return {"success": True, "result": result}

        except Exception as e:
            error_msg = f"任务执行失败"
            task.error = error_msg
            task.status = LearningTaskStatus.FAILED

            # 更新引擎状态
            with self.status_lock:
                status = self.engine_status[task.engine_type]
                status.task_count += 1

            # 更新统计
            self.failed_tasks.append(task)
            self.stats["failed_tasks"] += 1

            logger.error(f"任务执行失败: {task.task_id} - {error_msg}")
            return {"success": False, "error": error_msg}

    def run(self, max_tasks: Optional[int] = None) -> Dict[str, Any]:
        """
        运行学习协调器

        Args:
            max_tasks: 最大执行任务数,None表示执行全部

        Returns:
            执行统计
        """
        logger.info(f"启动学习协调器,最大并发: {self.max_workers}")

        executed_count = 0
        results = {
            "success": 0,
            "failed": 0,
            "total": 0,
            "start_time": datetime.now().isoformat(),
            "end_time": None
        }

        import time as _time
        _coord_start = _time.monotonic()
        _TASK_TIMEOUT = 30.0  # [v9.0] 单个任务超时（秒）
        _COORD_TIMEOUT = 90.0  # [v9.0] 整个协调过程超时（秒）

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            _stale_futures = []  # 超时但仍在运行的future引用

            while True:
                # 检查是否达到最大任务数
                if max_tasks and executed_count >= max_tasks:
                    break
                
                # [v9.0] 检查协调总时间超时
                if (_time.monotonic() - _coord_start) > _COORD_TIMEOUT:
                    logger.warning(
                        f"[学习协调器] 总耗时超过{_COORD_TIMEOUT:.0f}s，"
                        f"停止获取新任务(已执行{executed_count}个)"
                    )
                    break

                # get下一个任务
                task = self.get_next_task()
                if not task:
                    break

                # 提交任务
                future = executor.submit(self.execute_task, task)
                futures.append(future)
                executed_count += 1

            # 等待所有任务完成（带单任务超时保护）
            for future in as_completed(futures):
                try:
                    # [v9.0] 对单个future施加超时，防止一个卡住的任务阻塞整个批次
                    result = future(timeout=_TASK_TIMEOUT)
                    if result["success"]:
                        results["success"] += 1
                    else:
                        results["failed"] += 1
                except Exception as e:
                    logger.error(f"任务执行异常: {e}")
                    results["failed"] += 1

        results["total"] = executed_count
        results["end_time"] = datetime.now().isoformat()

        # 保存进度
        self._save_progress()

        logger.info(f"学习协调器完成: 成功 {results['success']}, 失败 {results['failed']}")
        return results

    def get_status(self) -> Dict[str, Any]:
        """get协调器状态"""
        with self.queue_lock:
            pending_count = sum(1 for t in self.task_queue if t.status == LearningTaskStatus.PENDING)
            in_progress_count = sum(1 for t in self.task_queue if t.status == LearningTaskStatus.IN_PROGRESS)

        return {
            "pending_tasks": pending_count,
            "in_progress_tasks": in_progress_count,
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "engines": {
                name: {
                    "is_active": status.is_active,
                    "task_count": status.task_count,
                    "success_rate": status.success_rate
                }
                for name, status in self.engine_status.items()
            },
            "statistics": self.stats
        }

    def _load_progress(self):
        """加载进度 [v1.0 已实现]"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 恢复统计信息
                if 'statistics' in data:
                    for key, value in data['statistics'].items():
                        if key in self.stats:
                            self.stats[key] = value

                # 恢复引擎状态
                if 'engines' in data:
                    for name, engine_data in data['engines'].items():
                        if name in self.engine_status:
                            status = self.engine_status[name]
                            status.task_count = engine_data.get('task_count', 0)
                            status.success_rate = engine_data.get('success_rate', 0.0)
                            status.last_execution = engine_data.get('last_execution', None)

                logger.info(f"进度已恢复: {self.progress_file}")
                logger.info(f"  统计: {self.stats}")
            except Exception as e:
                logger.warning(f"加载进度失败: {e}")

    def _save_progress(self):
        """保存进度"""
        try:
            data = {
                "statistics": self.stats,
                "engines": {
                    name: {
                        "task_count": status.task_count,
                        "success_rate": status.success_rate,
                        "last_execution": status.last_execution
                    }
                    for name, status in self.engine_status.items()
                },
                "timestamp": datetime.now().isoformat()
            }

            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"保存进度失败: {e}")

    def generate_report(self) -> Dict[str, Any]:
        """generate学习报告"""
        report = {
            "summary": {
                "total_tasks": self.stats["total_tasks"],
                "completed_tasks": self.stats["completed_tasks"],
                "failed_tasks": self.stats["failed_tasks"],
                "success_rate": self.stats["completed_tasks"] / max(self.stats["total_tasks"], 1)
            },
            "engines": {},
            "recent_tasks": [],
            "timestamp": datetime.now().isoformat()
        }

        # 引擎统计
        for name, status in self.engine_status.items():
            report["engines"][name] = {
                "task_count": status.task_count,
                "success_rate": status.success_rate,
                "last_execution": status.last_execution
            }

        # 最近任务
        report["recent_tasks"] = [
            {
                "task_id": t.task_id,
                "engine_type": t.engine_type,
                "status": t.status.value,
                "completed_at": t.completed_at
            }
            for t in self.completed_tasks[-10:]
        ]

        # 保存报告
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report

# 便捷函数
def create_coordinator(max_workers: int = 4) -> LearningCoordinator:
    """创建学习协调器"""
    return LearningCoordinator(max_workers=max_workers)

__all__ = [
    'LearningPriority', 'TaskStatus', 'LearningTask', 'EngineStatus',
    'LearningCoordinator', 'create_coordinator',
]

# [修复] TaskStatus在__all__中声明但未定义，补充向后兼容别名
TaskStatus = None  # type: ignore  # 占位，防止导入时报AttributeError
