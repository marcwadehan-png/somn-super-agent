"""
__all__ = [
    'cancel_task',
    'emit_event',
    'generate_report',
    'get_all_tasks',
    'get_pending_tasks',
    'get_running_tasks',
    'get_statistics',
    'get_task',
    'is_due',
    'pause_task',
    'register_callback',
    'register_event_handler',
    'resume_task',
    'schedule_conditional',
    'schedule_once',
    'schedule_periodic',
    'should_run',
    'start',
    'stop',
    'to_dict',
]

自主调度器 - Autonomous Scheduler

实现智能体的自主运行能力:
- 定期检查与触发
- 任务调度与优先级
- 周期性任务管理
- 事件驱动响应
- 资源分配与冲突解决
"""

import json
import uuid
import asyncio
import threading
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Coroutine
from dataclasses import dataclass, field
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from loguru import logger

class SchedulerTaskStatus(Enum):
    """自主调度器任务状态（区别于其他模块的TaskStatus）"""
    SCHEDULED = "scheduled"      # 已调度
    RUNNING = "running"          # 执行中
    COMPLETED = "completed"      # 已完成
    FAILED = "failed"            # 失败
    CANCELLED = "cancelled"      # 已取消
    SKIPPED = "skipped"          # 已跳过

class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 1    # 关键 - 立即执行
    HIGH = 2        # 高 - 优先执行
    MEDIUM = 3      # 中 - 正常执行
    LOW = 4         # 低 - 空闲时执行

class TaskType(Enum):
    """任务类型"""
    ONCE = "once"                    # 一次性任务
    PERIODIC = "periodic"            # 周期性任务
    EVENT_DRIVEN = "event_driven"    # 事件驱动
    CONDITIONAL = "conditional"      # 条件触发

@dataclass
class ScheduledTask:
    """调度任务定义"""
    # 基本信息
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    
    # 任务类型
    task_type: TaskType = TaskType.ONCE
    
    # 执行函数
    func: Optional[Callable] = field(default=None, repr=False)
    func_name: str = ""  # 用于序列化存储
    
    # 调度参数
    scheduled_at: Optional[datetime] = None           # 计划执行时间
    interval_seconds: Optional[int] = None            # 周期任务间隔
    condition: Optional[Callable[[], bool]] = None    # 条件函数
    condition_desc: str = ""                          # 条件描述
    
    # 状态
    status: SchedulerTaskStatus = SchedulerTaskStatus.SCHEDULED
    priority: TaskPriority = TaskPriority.MEDIUM
    
    # 执行记录
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    max_runs: Optional[int] = None  # 最大执行次数(None表示无限)
    
    # 结果
    last_result: Any = None
    last_error: Optional[str] = None
    
    # 元数据
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """转换为字典(用于存储)"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'task_type': self.task_type.value,
            'func_name': self.func_name,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'interval_seconds': self.interval_seconds,
            'condition_desc': self.condition_desc,
            'status': self.status.value,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat(),
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'run_count': self.run_count,
            'max_runs': self.max_runs,
            'last_error': self.last_error,
            'context': self.context,
            'tags': self.tags
        }
    
    def is_due(self) -> bool:
        """检查任务是否到期"""
        if self.status not in [SchedulerTaskStatus.SCHEDULED, SchedulerTaskStatus.COMPLETED]:
            return False
        
        now = datetime.now()
        
        if self.task_type == TaskType.ONCE:
            return self.scheduled_at and now >= self.scheduled_at
        
        elif self.task_type == TaskType.PERIODIC:
            if self.max_runs and self.run_count >= self.max_runs:
                return False
            return self.next_run and now >= self.next_run
        
        elif self.task_type == TaskType.CONDITIONAL:
            if self.condition:
                return self.condition()
            return False
        
        return False
    
    def should_run(self) -> bool:
        """检查任务是否应该执行"""
        if self.status == SchedulerTaskStatus.CANCELLED:
            return False
        
        if self.max_runs and self.run_count >= self.max_runs:
            return False
        
        return self.is_due()

class AutonomousScheduler:
    """
    自主调度器 - 管理智能体的自主任务调度
    
    核心功能:
    1. 任务注册与调度
    2. 周期性任务管理
    3. 条件触发任务
    4. 优先级队列
    5. 并发控制
    6. 执行监控
    """
    
    def __init__(
        self,
        storage_path: str = "data/scheduler",
        check_interval: int = 10,  # 检查间隔(秒)
        max_concurrent: int = 3    # 最大并发任务数
    ):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.check_interval = check_interval
        self.max_concurrent = max_concurrent
        
        # 任务存储
        self._tasks: Dict[str, ScheduledTask] = {}
        self._task_queue: List[str] = []  # 按优先级排序的任务ID队列
        
        # 执行控制
        self._running = False
        self._scheduler_thread: Optional[threading.Thread] = None
        self._executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self._running_tasks: Dict[str, Any] = {}  # 正在执行的任务
        self._save_lock = threading.Lock()  # 保护 _save_tasks 防止并发写入
        self._state_lock = threading.Lock()  # 保护 _tasks/_task_queue/_running_tasks 状态一致性

        # 回调函数注册表
        self._callbacks: Dict[str, Callable] = {}
        
        # 事件处理器
        self._event_handlers: Dict[str, List[Callable]] = {}
        
        # 加载已有任务
        self._load_tasks()
        
        logger.info(f"自主调度器init完成,检查间隔: {check_interval}s,最大并发: {max_concurrent}")
    
    def _load_tasks(self):
        """加载已有任务（空文件/损坏JSON时优雅降级，不影响启动）"""
        tasks_file = self.storage_path / "tasks.json"
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if not content:
                    logger.info("tasks.json 为空，初始化为空任务列表")
                    self._save_tasks()
                    return
                data = json.loads(content)
                for task_data in data.get('tasks', []):
                    task = ScheduledTask(
                        id=task_data['id'],
                        name=task_data['name'],
                        description=task_data.get('description', ''),
                        task_type=TaskType(task_data['task_type']),
                        func_name=task_data.get('func_name', ''),
                        scheduled_at=datetime.fromisoformat(task_data['scheduled_at']) if task_data.get('scheduled_at') else None,
                        interval_seconds=task_data.get('interval_seconds'),
                        condition_desc=task_data.get('condition_desc', ''),
                        status=SchedulerTaskStatus(task_data.get('status', 'scheduled')),
                        priority=TaskPriority(task_data.get('priority', 3)),
                        created_at=datetime.fromisoformat(task_data['created_at']),
                        last_run=datetime.fromisoformat(task_data['last_run']) if task_data.get('last_run') else None,
                        next_run=datetime.fromisoformat(task_data['next_run']) if task_data.get('next_run') else None,
                        run_count=task_data.get('run_count', 0),
                        max_runs=task_data.get('max_runs'),
                        last_error=task_data.get('last_error'),
                        context=task_data.get('context', {}),
                        tags=task_data.get('tags', [])
                    )
                    self._tasks[task.id] = task
                logger.info(f"已加载 {len(self._tasks)} 个调度任务")
            except json.JSONDecodeError as e:
                logger.warning(f"tasks.json 格式损坏 ({e})，初始化为空任务列表")
                self._save_tasks()
            except Exception as e:
                logger.warning(f"加载任务失败 ({e})，初始化为空任务列表")
                self._save_tasks()
    
    def _save_tasks(self):
        """保存任务到存储（线程安全）"""
        with self._save_lock:
            tasks_file = self.storage_path / "tasks.json"
            try:
                data = {
                    'updated_at': datetime.now().isoformat(),
                    'tasks': [task.to_dict() for task in self._tasks.values()]
                }
                with open(tasks_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"保存任务失败: {e}")
    
    # ========== 任务注册 ==========
    
    def register_callback(self, name: str, func: Callable):
        """注册回调函数"""
        self._callbacks[name] = func
        logger.debug(f"注册回调函数: {name}")
    
    def schedule_once(
        self,
        name: str,
        func: Callable,
        scheduled_at: datetime,
        priority: TaskPriority = TaskPriority.MEDIUM,
        description: str = "",
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> ScheduledTask:
        """
        调度一次性任务
        
        Args:
            name: 任务名称
            func: 执行函数
            scheduled_at: 计划执行时间
            priority: 优先级
            description: 描述
            context: 上下文
            tags: 标签
        
        Returns:
            调度任务对象
        """
        task = ScheduledTask(
            name=name,
            description=description,
            task_type=TaskType.ONCE,
            func=func,
            func_name=func.__name__,
            scheduled_at=scheduled_at,
            priority=priority,
            context=context or {},
            tags=tags or []
        )
        
        self._tasks[task.id] = task
        self._update_queue()
        self._save_tasks()
        
        logger.info(f"调度一次性任务: [{task.id}] {name} @ {scheduled_at}")
        return task
    
    def schedule_periodic(
        self,
        name: str,
        func: Callable,
        interval_seconds: int,
        priority: TaskPriority = TaskPriority.MEDIUM,
        start_at: Optional[datetime] = None,
        max_runs: Optional[int] = None,
        description: str = "",
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> ScheduledTask:
        """
        调度周期性任务
        
        Args:
            name: 任务名称
            func: 执行函数
            interval_seconds: 执行间隔(秒)
            priority: 优先级
            start_at: 开始时间(默认立即)
            max_runs: 最大执行次数
            description: 描述
            context: 上下文
            tags: 标签
        
        Returns:
            调度任务对象
        """
        next_run = start_at or datetime.now()
        
        task = ScheduledTask(
            name=name,
            description=description,
            task_type=TaskType.PERIODIC,
            func=func,
            func_name=func.__name__,
            interval_seconds=interval_seconds,
            next_run=next_run,
            priority=priority,
            max_runs=max_runs,
            context=context or {},
            tags=tags or []
        )
        
        self._tasks[task.id] = task
        self._update_queue()
        self._save_tasks()
        
        logger.info(f"调度周期性任务: [{task.id}] {name} 每{interval_seconds}秒")
        return task
    
    def schedule_conditional(
        self,
        name: str,
        func: Callable,
        condition: Callable[[], bool],
        condition_desc: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        max_runs: Optional[int] = None,
        description: str = "",
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> ScheduledTask:
        """
        调度条件触发任务
        
        Args:
            name: 任务名称
            func: 执行函数
            condition: 条件函数(返回True时触发)
            condition_desc: 条件描述
            priority: 优先级
            max_runs: 最大执行次数
            description: 描述
            context: 上下文
            tags: 标签
        
        Returns:
            调度任务对象
        """
        task = ScheduledTask(
            name=name,
            description=description,
            task_type=TaskType.CONDITIONAL,
            func=func,
            func_name=func.__name__,
            condition=condition,
            condition_desc=condition_desc,
            priority=priority,
            max_runs=max_runs,
            context=context or {},
            tags=tags or []
        )
        
        self._tasks[task.id] = task
        self._update_queue()
        self._save_tasks()
        
        logger.info(f"调度条件任务: [{task.id}] {name} 当: {condition_desc}")
        return task
    
    def _update_queue(self):
        """更新任务队列(按优先级排序)"""
        with self._state_lock:
            # get所有待执行的任务
            pending = [
                task for task in self._tasks.values()
                if task.status in [SchedulerTaskStatus.SCHEDULED, SchedulerTaskStatus.COMPLETED]
            ]
            
            # 按优先级和时间排序
            pending.sort(key=lambda t: (t.priority.value, t.next_run or datetime.max))
            
            self._task_queue = [task.id for task in pending]
    
    # ========== 调度控制 ==========
    
    def start(self):
        """启动调度器"""
        if self._running:
            logger.warning("调度器已在运行")
            return
        
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self._scheduler_thread.start()
        
        logger.info("自主调度器已启动")
    
    def stop(self):
        """停止调度器"""
        if not self._running:
            return
        
        self._running = False
        
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        
        self._executor.shutdown(wait=False)
        
        logger.info("自主调度器已停止")
    
    def _scheduler_loop(self):
        """调度器主循环"""
        logger.info("调度器主循环开始")
        
        while self._running:
            try:
                self._check_and_execute()
            except Exception as e:
                # 解释器退出时RuntimeError属预期，直接停止循环
                if not self._running or "interpreter shutdown" in str(e).lower() or "after" in str(e).lower():
                    logger.info("调度器检测到退出信号，停止调度")
                    break
                logger.error(f"调度循环错误: {e}")
            
            # 等待下一次检查
            for _ in range(self.check_interval):
                if not self._running:
                    break
                import time
                time.sleep(1)
        
        logger.info("调度器主循环结束")
    
    def _check_and_execute(self):
        """检查并执行任务"""
        # get当前可执行的任务
        with self._state_lock:
            due_tasks = []
            for task_id in self._task_queue:
                task = self._tasks.get(task_id)
                if task and task.should_run():
                    due_tasks.append(task)
            available_slots = self.max_concurrent - len(self._running_tasks)
        
        # 按优先级排序
        due_tasks.sort(key=lambda t: t.priority.value)
        
        # 执行到期的任务(考虑并发限制)
        for task in due_tasks[:available_slots]:
            self._execute_task(task)
    
    def _execute_task(self, task: ScheduledTask):
        """执行任务"""
        if task.id in self._running_tasks:
            return
        
        # 检查是否有回调函数
        func = task.func
        if not func and task.func_name in self._callbacks:
            func = self._callbacks[task.func_name]
        
        if not func:
            # 孤儿任务（跨进程无法还原函数引用），从列表中移除以避免重复警告
            logger.warning(f"任务 [{task.id}] 没有可执行的函数，已从调度器移除")
            task.status = SchedulerTaskStatus.FAILED
            task.last_error = "No executable function (orphaned)"
            # 从 _tasks 移除并更新队列
            if task.id in self._tasks:
                del self._tasks[task.id]
            self._update_queue()
            self._save_tasks()
            return
        
        # 提交执行（解释器退出时RuntimeError，直接跳过）
        task.status = SchedulerTaskStatus.RUNNING
        task.last_run = datetime.now()

        try:
            future = self._executor.submit(self._run_task_wrapper, task, func)
            self._running_tasks[task.id] = future
        except RuntimeError:
            task.status = SchedulerTaskStatus.SCHEDULED
            logger.warning(f"解释器退出，跳过任务 [{task.id}] {task.name}")
            return

        logger.info(f"开始执行任务: [{task.id}] {task.name}")
    
    def _run_task_wrapper(self, task: ScheduledTask, func: Callable):
        """任务执行包装器"""
        try:
            # 执行函数
            result = func(**task.context)
            
            # 更新任务状态
            task.last_result = result
            task.run_count += 1
            
            if task.task_type == TaskType.PERIODIC and (not task.max_runs or task.run_count < task.max_runs):
                # 周期性任务,计算下次执行时间
                task.next_run = datetime.now() + timedelta(seconds=task.interval_seconds)
                task.status = SchedulerTaskStatus.SCHEDULED
            else:
                task.status = SchedulerTaskStatus.COMPLETED
            
            logger.info(f"任务完成: [{task.id}] {task.name}")
            
        except Exception as e:
            task.status = SchedulerTaskStatus.FAILED
            task.last_error = "任务执行失败"
            logger.error(f"任务失败: [{task.id}] {task.name} - {e}")
        
        finally:
            # 清理
            with self._state_lock:
                if task.id in self._running_tasks:
                    del self._running_tasks[task.id]
            
            self._update_queue()
            self._save_tasks()
    
    # ========== 任务管理 ==========
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self._tasks.get(task_id)
        if not task:
            return False
        
        task.status = SchedulerTaskStatus.CANCELLED
        self._update_queue()
        self._save_tasks()
        
        logger.info(f"取消任务: [{task_id}] {task.name}")
        return True
    
    def pause_task(self, task_id: str) -> bool:
        """暂停任务"""
        task = self._tasks.get(task_id)
        if not task:
            return False
        
        task.status = SchedulerTaskStatus.SCHEDULED
        task.context['paused'] = True
        self._save_tasks()
        
        logger.info(f"暂停任务: [{task_id}] {task.name}")
        return True
    
    def resume_task(self, task_id: str) -> bool:
        """恢复任务"""
        task = self._tasks.get(task_id)
        if not task:
            return False
        
        task.status = SchedulerTaskStatus.SCHEDULED
        task.context.pop('paused', None)
        self._update_queue()
        self._save_tasks()
        
        logger.info(f"恢复任务: [{task_id}] {task.name}")
        return True
    
    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """get任务"""
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[ScheduledTask]:
        """get所有任务"""
        return list(self._tasks.values())
    
    def get_pending_tasks(self) -> List[ScheduledTask]:
        """get待处理任务"""
        return [t for t in self._tasks.values() if t.status == SchedulerTaskStatus.SCHEDULED]
    
    def get_running_tasks(self) -> List[ScheduledTask]:
        """get运行中任务"""
        return [t for t in self._tasks.values() if t.status == SchedulerTaskStatus.RUNNING]
    
    # ========== 事件处理 ==========
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """注册事件处理器"""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
        logger.debug(f"注册事件处理器: {event_type}")
    
    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """触发事件"""
        logger.debug(f"触发事件: {event_type}")
        
        handlers = self._event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"事件处理器错误 [{event_type}]: {e}")
    
    # ========== 统计与报告 ==========
    
    def get_statistics(self) -> Dict[str, Any]:
        """get调度器统计"""
        total = len(self._tasks)
        by_status = {status.value: 0 for status in SchedulerTaskStatus}
        for task in self._tasks.values():
            by_status[task.status.value] += 1
        
        return {
            'total_tasks': total,
            'running': len(self._running_tasks),
            'by_status': by_status,
            'is_running': self._running,
            'check_interval': self.check_interval,
            'max_concurrent': self.max_concurrent
        }
    
    def generate_report(self) -> str:
        """generate调度器报告"""
        stats = self.get_statistics()
        
        report = f"""
# 自主调度器报告

## 运行状态
- 调度器运行中: {'是' if stats['is_running'] else '否'}
- 检查间隔: {stats['check_interval']}秒
- 最大并发: {stats['max_concurrent']}

## 任务统计
- 总任务数: {stats['total_tasks']}
- 运行中: {stats['running']}
- 已调度: {stats['by_status'].get('scheduled', 0)}
- 已完成: {stats['by_status'].get('completed', 0)}
- 失败: {stats['by_status'].get('failed', 0)}
- 已取消: {stats['by_status'].get('cancelled', 0)}

## 运行中任务
"""
        for task in self.get_running_tasks():
            report += f"- [{task.id}] {task.name} (已运行: {task.last_run})\n"
        
        report += "\n## 即将执行的任务\n"
        pending = self.get_pending_tasks()[:10]
        for task in sorted(pending, key=lambda t: t.next_run or datetime.max):
            next_run = task.next_run.strftime('%Y-%m-%d %H:%M:%S') if task.next_run else "待定"
            report += f"- [{task.id}] {task.name} @ {next_run}\n"
        
        return report
