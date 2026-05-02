"""
__all__ = [
    'add_custom_task',
    'create_unified_system',
    'get_status',
    'start_learning',
    'stop_learning',
]

unified学习系统
Unified Learning System

整合所有学习引擎的unified入口

功能:
1. unified管理所有学习维度
2. 智能调度学习任务
3. 本地资料深度学习
4. 知识质量评估与择优
5. 学习效果追踪
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import time
import threading

# 添加项目路径
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__)

from src.learning.core.coordinator import LearningCoordinator, LearningTask, LearningPriority, TaskStatus

from src.learning.engine.local_data_learner import LocalDataLearner, FileType, LearningResult
from src.learning.core.smart_scheduler import SmartScheduler, create_scheduler, SchedulingStrategy
from src.learning.engine.smart_learning_engine import SmartLearningEngine

logger = logging.getLogger(__name__)

@dataclass
class UnifiedLearningConfig:
    """unified学习配置"""
    # 学习目标
    target_drive: str = "E:"              # 目标盘符
    max_concurrent_tasks: int = 4         # 最大并发任务数
    max_files_per_batch: int = 100        # 每批最大文件数

    # 调度配置
    scheduling_strategy: str = "adaptive"  # 调度strategy
    learning_interval: int = 5            # 学习间隔(分钟)

    # 学习配置
    enable_local_learning: bool = True    # 启用本地资料学习
    enable_neural_learning: bool = True   # 启用神经记忆学习
    enable_smart_learning: bool = True    # 启用智能学习

    # 优先级配置
    codebase_priority: int = 0           # 代码库学习优先级
    knowledge_priority: int = 1          # 知识库学习优先级
    config_priority: int = 2             # 配置文件学习优先级
    other_priority: int = 3              # 其他文件学习优先级

class UnifiedLearningSystem:
    """
    unified学习系统

    核心功能:
    1. unified管理 - 协调所有学习引擎
    2. 智能调度 - 基于优先级和资源调度
    3. 深度学习 - 本地资料深度学习
    4. 质量保证 - 智能评估和择优
    5. 效果追踪 - 持续优化学习strategy
    """

    def __init__(self, config: Optional[UnifiedLearningConfig] = None):
        """
        initunified学习系统

        Args:
            config: 学习配置
        """
        self.config = config or UnifiedLearningConfig()

        # init组件
        self.coordinator = LearningCoordinator(max_workers=self.config.max_concurrent_tasks)
        self.scheduler = create_scheduler(self.config.scheduling_strategy)
        self.local_learner = LocalDataLearner(target_drive=self.config.target_drive)
        self.smart_learning_engine = SmartLearningEngine()

        # 学习状态
        self.is_running = False
        self.learning_thread: Optional[threading.Thread] = None

        # 数据目录
        self.data_dir = Path("data/learning/unified")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.data_dir / "config.json"
        self.status_file = self.data_dir / "status.json"

        # 加载配置
        self._load_config()

        # init引擎
        self._initialize_engines()

        logger.info("unified学习系统init完成")

    def _initialize_engines(self):
        """init学习引擎"""
        # 注册本地资料学习引擎
        self.coordinator.register_engine(
            name="local_data",
            engine_class=LocalDataLearner,
            config={"target_drive": self.config.target_drive}
        )

        # 注册智能学习引擎
        self.coordinator.register_engine(
            name="smart_learning",
            engine_class=SmartLearningEngine,
            config={}
        )

        logger.info("学习引擎注册完成")

    def start_learning(self, continuous: bool = False):
        """
        启动学习

        Args:
            continuous: 是否持续学习
        """
        if self.is_running:
            logger.warning("学习系统已在运行")
            return

        self.is_running = True

        if continuous:
            # 持续学习模式
            self.learning_thread = threading.Thread(
                target=self._continuous_learning_loop,
                daemon=True
            )
            self.learning_thread.start()
            logger.info(f"启动持续学习,间隔: {self.config.learning_interval}分钟")
        else:
            # 单次学习模式
            self._single_learning()

    def stop_learning(self):
        """停止学习"""
        self.is_running = False
        if self.learning_thread:
            self.learning_thread.join(timeout=10)
        logger.info("学习已停止")

    def _continuous_learning_loop(self):
        """持续学习循环"""
        while self.is_running:
            try:
                # 执行一轮学习
                self._single_learning()

                # 等待指定时间
                for _ in range(self.config.learning_interval * 60):
                    if not self.is_running:
                        return
                    time.sleep(1)

            except Exception as e:
                logger.error(f"学习循环异常: {e}")
                time.sleep(60)  # 异常后等待1分钟

    def _single_learning(self):
        """单次学习"""
        logger.info("=" * 80)
        logger.info("开始学习周期")
        logger.info("=" * 80)

        try:
            # 第一步:扫描本地资料
            if self.config.enable_local_learning:
                self._scan_and_learn_local_data()

            # 第二步:执行待处理任务
            self._execute_pending_tasks()

            # 第三步:generate学习报告
            self._generate_learning_report()

            # 第四步:保存状态
            self._save_status()

            logger.info("学习周期完成")

        except Exception as e:
            logger.error(f"学习周期失败: {e}", exc_info=True)

    def _scan_and_learn_local_data(self):
        """扫描并学习本地数据"""
        logger.info("开始扫描本地资料...")

        # 扫描文件(限制数量)
        file_infos = self.local_learner.scan_directory(
            max_files=self.config.max_files_per_batch,
            file_types={
                FileType.CODE,
                FileType.KNOWLEDGE,
                FileType.CONFIG,
                FileType.TEXT
            }
        )

        logger.info(f"扫描完成,找到 {len(file_infos)} 个文件")

        # 为每个文件创建学习任务
        tasks = []
        for file_info in file_infos[:50]:  # 限制任务数量
            # 确定优先级
            if file_info.file_category.value == "codebase":
                priority = LearningPriority(self.config.codebase_priority)
            elif file_info.file_category.value == "knowledge":
                priority = LearningPriority(self.config.knowledge_priority)
            elif file_info.file_category.value == "config":
                priority = LearningPriority(self.config.config_priority)
            else:
                priority = LearningPriority(self.config.other_priority)

            # 创建任务
            task = LearningTask(
                task_id=f"local_{file_info.path.replace(':', '_').replace('/', '_').replace('\\', '_')}",
                engine_type="local_data",
                priority=priority,
                data={"file_path": file_info.path},
                metadata={
                    "file_type": file_info.file_type.value,
                    "file_category": file_info.file_category.value,
                    "size": file_info.size
                },
                estimated_time=0.1  # 预估耗时
            )

            tasks.append(task)

        # 批量提交任务
        if tasks:
            task_ids = self.coordinator.submit_tasks_batch(tasks)
            logger.info(f"提交 {len(task_ids)} 个学习任务")

    def _execute_pending_tasks(self):
        """执行待处理任务"""
        logger.info("执行待处理任务...")

        # 运行协调器
        results = self.coordinator.run(max_tasks=50)

        logger.info(f"任务执行完成: 成功 {results['success']}, 失败 {results['failed']}")

    def _generate_learning_report(self):
        """generate学习报告"""
        logger.info("generate学习报告...")

        # get协调器状态
        status = self.coordinator.get_status()

        # get学习统计
        local_stats = self.local_learner.get_statistics()

        # generate报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tasks": status["pending_tasks"] + status["in_progress_tasks"] + status["completed_tasks"],
                "pending_tasks": status["pending_tasks"],
                "in_progress_tasks": status["in_progress_tasks"],
                "completed_tasks": status["completed_tasks"],
                "failed_tasks": status["failed_tasks"]
            },
            "local_learning": {
                "total_files": local_stats["total_files"],
                "learned_files": local_stats["learned_files"],
                "failed_files": local_stats["failed_files"],
                "total_size_mb": round(local_stats["total_size"] / (1024 * 1024), 2)
            },
            "engines": status["engines"],
            "statistics": status["statistics"],
            "scheduling": self.scheduler.get_scheduling_statistics()
        }

        # 保存报告
        report_file = self.data_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"学习报告已保存: {report_file}")
        return report

    def _save_status(self):
        """保存状态"""
        status = {
            "is_running": self.is_running,
            "config": {
                "target_drive": self.config.target_drive,
                "max_concurrent_tasks": self.config.max_concurrent_tasks,
                "learning_interval": self.config.learning_interval
            },
            "coordinator_status": self.coordinator.get_status(),
            "scheduler_stats": self.scheduler.get_scheduling_statistics(),
            "local_learner_stats": self.local_learner.get_statistics(),
            "timestamp": datetime.now().isoformat()
        }

        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)

    def _load_config(self):
        """加载配置 [v1.0 已实现]"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 应用配置到各组件
                if 'target_drive' in data:
                    self.config.target_drive = data['target_drive']
                if 'max_concurrent_tasks' in data:
                    self.config.max_concurrent_tasks = data['max_concurrent_tasks']
                if 'learning_interval' in data:
                    self.config.learning_interval = data['learning_interval']
                if 'scheduling_strategy' in data:
                    self.config.scheduling_strategy = data['scheduling_strategy']

                # 学习开关
                if 'enable_local_learning' in data:
                    self.config.enable_local_learning = data['enable_local_learning']
                if 'enable_neural_learning' in data:
                    self.config.enable_neural_learning = data['enable_neural_learning']
                if 'enable_smart_learning' in data:
                    self.config.enable_smart_learning = data['enable_smart_learning']

                # 优先级配置
                if 'codebase_priority' in data:
                    self.config.codebase_priority = data['codebase_priority']
                if 'knowledge_priority' in data:
                    self.config.knowledge_priority = data['knowledge_priority']
                if 'config_priority' in data:
                    self.config.config_priority = data['config_priority']
                if 'other_priority' in data:
                    self.config.other_priority = data['other_priority']

                # 批量配置
                if 'max_files_per_batch' in data:
                    self.config.max_files_per_batch = data['max_files_per_batch']

                logger.info(f"配置已加载: {self.config}")
            except Exception as e:
                logger.warning(f"加载配置失败: {e}")

    def get_status(self) -> Dict[str, Any]:
        """get系统状态"""
        return {
            "is_running": self.is_running,
            "config": {
                "target_drive": self.config.target_drive,
                "max_concurrent_tasks": self.config.max_concurrent_tasks,
                "learning_interval": self.config.learning_interval
            },
            "coordinator": self.coordinator.get_status(),
            "scheduler": self.scheduler.get_scheduling_statistics(),
            "local_learner": self.local_learner.get_statistics(),
            "timestamp": datetime.now().isoformat()
        }

    def add_custom_task(self, task: LearningTask) -> str:
        """添加自定义学习任务"""
        task_id = self.coordinator.submit_task(task)
        logger.info(f"自定义任务已添加: {task_id}")
        return task_id

# 便捷函数
def create_unified_system(target_drive: str = "E:",
                          max_concurrent: int = 4,
                          continuous: bool = False) -> UnifiedLearningSystem:
    """
    创建unified学习系统

    Args:
        target_drive: 目标盘符
        max_concurrent: 最大并发数
        continuous: 是否持续学习

    Returns:
        unified学习system_instance
    """
    config = UnifiedLearningConfig(
        target_drive=target_drive,
        max_concurrent_tasks=max_concurrent
    )

    system = UnifiedLearningSystem(config)

    if continuous:
        system.start_learning(continuous=True)

    return system

# 主程序
