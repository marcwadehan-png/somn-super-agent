"""
自适应学习协调器 v1.0
Adaptive Learning Coordinator

[v2.2.0 道家升级] 新增自然演化学习模式（NatureEvolution），
体现"致虚极守静笃"的遗忘智慧和"为道日损"的提炼哲学：
- 动态遗忘（DYNAMIC_DECAY）：根据知识使用频率和时效性自动调整衰减率
- 情境探索（CONTEXTUAL_EXPLORATION）：探索率随当前任务领域动态调整
- 自发性精炼（SPONTANEOUS_REFINEMENT）：低负载时自动进行自我优化
"""

from __future__ import annotations

import time
import threading
import heapq
import json
import hashlib
import asyncio
import math
from typing import Dict, List, Any, Optional, Tuple, Set, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import random
import numpy as np
from loguru import logger

# 导入现有学习模块
try:
    from ..unified_learning_system import UnifiedLearningSystem, UnifiedLearningConfig
    from ..core.coordinator import LearningCoordinator, LearningTask, LearningPriority
    from ..core.coordinator import LearningTaskStatus as TaskStatus  # 修复：TaskStatus不存在，使用LearningTaskStatus别名
    from ..core.smart_scheduler import SmartScheduler, SchedulingStrategy
    from ..engine.local_data_learner import LocalDataLearner, FileType, LearningResult
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    logger.warning(f"学习模块导入失败: {e}")

class LearningStage(Enum):
    """学习阶段"""
    FOUNDATION = "foundation"      # 基础阶段:建立知识框架
    EXPANSION = "expansion"        # 扩展阶段:深入学习
    INTEGRATION = "integration"  # 整合阶段:知识fusion
    APPLICATION = "application"    # 应用阶段:实践应用

class LearningStrategy(Enum):
    """学习strategy"""
    SYSTEMATIC = "systematic"      # 系统学习:按知识体系顺序学习
    EXPLORATORY = "exploratory"    # 探索学习:基于兴趣和好奇学习
    PROBLEM_BASED = "problem_based"  # 问题驱动:针对问题展开学习
    ADAPTIVE = "adaptive"          # 自适应学习:根据效果动态调整


# ── v2.2.0: 道家自然演化学习 ─────────────────────────────────────────────

class NatureEvolutionStrategy(Enum):
    """
    自然演化学习策略 - 体现"道法自然"的学习哲学。

    核心理念：学习如树木生长，不需要强制推动，而是在适当的环境下自然演化。
    """
    DYNAMIC_DECAY = "dynamic_decay"           # 动态遗忘：长用常新，不用的自然消退
    CONTEXTUAL_EXPLORATION = "contextual"      # 情境探索：因时因地，灵活调整
    SPONTANEOUS_REFINEMENT = "spontaneous"     # 自发性精炼：无为而治，自我优化
    # 综合模式：水善利万物而不争，融合三种策略
    HARMONIC_GROWTH = "harmonic_growth"


@dataclass
class NatureEvolutionConfig:
    """
    自然演化学习配置 - "致虚极守静笃"的遗忘智慧。

    核心理念：
    - 知识如水：长流不腐，静则渐失
    - 学习如树：自然生长，不需强推
    - 遗忘如雪：无声消融，为新知让路
    """
    # 基础遗忘参数
    base_decay_rate: float = 0.05       # 基础遗忘率（每日）
    min_decay_rate: float = 0.005        # 最低遗忘率（永久知识）
    max_decay_rate: float = 0.3          # 最高遗忘率（快速遗忘噪声）

    # 动态遗忘参数
    use_dynamic_decay: bool = True      # 是否启用动态遗忘
    decay_half_life_days: float = 30.0   # 知识半衰期基准（天）
    usage_boost_factor: float = 2.0      # 使用频率对遗忘率的补偿系数

    # 情境探索参数
    use_contextual_exploration: bool = True
    base_exploration_rate: float = 0.3   # 基础探索率
    exploration_context_sensitivity: float = 0.2  # 情境敏感度
    min_exploration_rate: float = 0.1    # 最低探索率
    max_exploration_rate: float = 0.5    # 最高探索率

    # 自发性精炼参数
    use_spontaneous_refinement: bool = True
    refinement_trigger_load_threshold: float = 0.3  # 低负载阈值（触发精炼）
    refinement_interval_hours: float = 24.0        # 精炼检查间隔
    refinement_strength: float = 0.1                # 每次精炼强度

    # 道家参数
    dao_wisdom_enabled: bool = True      # 是否启用道家自然演化模式
    water_flow_reminder: str = "致虚极，守静笃，万物并作，吾以观复。"


@dataclass
class KnowledgeDecayState:
    """知识遗忘状态 - 追踪每个知识的"新鲜度”"""
    knowledge_id: str
    last_used_time: float            # Unix时间戳
    use_count: int = 0               # 历史使用次数
    base_importance: float = 0.5     # 基础重要性（0-1）
    current_decay: float = 0.0        # 当前衰减量
    freshness_score: float = 1.0      # 新鲜度得分（0-1）
    # 道家分析
    dao_assessment: str = ""         # 自然和谐度评估
    water_flow_score: float = 0.0     # 上善若水评分（使用频率）


@dataclass
class ExplorationContext:
    """探索情境 - 当前学习环境的道家分析"""
    task_domain: str = ""            # 当前任务领域
    system_load: float = 0.0         # 系统负载（0-1）
    knowledge_density: float = 0.0   # 知识密度（0-1）
    uncertainty_level: float = 0.0  # 不确定性水平（0-1）
    # 道家参数
    yin_yang_balance: float = 0.5    # 阴阳平衡（0=阴，1=阳）
    natural_flow_score: float = 0.0  # 自然流动得分
    dao_recommendation: str = ""     # 道家建议

@dataclass
class LearningTaskProfile:
    """学习任务画像"""
    task_id: str
    content_type: str
    complexity_score: float  # 复杂度分数 (0-1)
    priority: LearningPriority
    # 学习特性
    estimated_time: float  # 估计学习时间(秒)
    difficulty_level: int  # 难度等级(1-10)
    importance_score: float  # 重要性分数(0-1)
    
    # 关联信息
    prerequisites: List[str] = field(default_factory=list)
    related_tasks: List[str] = field(default_factory=list)
    
    # 性能metrics
    historical_performance: List[float] = field(default_factory=list)
    success_rate: float = 0.0
    
    # 状态
    status: str = "pending"  # pending, in_progress, completed, failed
    start_time: Optional[float] = None
    end_time: Optional[float] = None

@dataclass
class LearningPlan:
    """学习计划"""
    plan_id: str
    target_skill: str
    learning_stage: LearningStage
    strategy: LearningStrategy
    
    # 学习路径
    learning_path: List[LearningTaskProfile]
    current_step: int = 0
    total_steps: int = 0
    
    # 进度跟踪
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    in_progress_tasks: List[str] = field(default_factory=list)
    
    # 质量监控
    quality_metrics: Dict[str, Any] = field(default_factory=dict)
    progress_score: float = 0.0
    overall_score: float = 0.0
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

class AdaptiveLearningCoordinator:
    """
    自适应学习协调器
    
    核心能力:
    1. 学习任务智能调度:基于任务优先级,紧急度,相关性动态调整
    2. 学习资源自适应分配:根据任务复杂度智能分配计算资源
    3. 学习strategy实时优化:基于历史效果动态调整学习strategy
    4. 学习路径智能规划:根据目标自动规划最优学习路径
    5. 学习效果智能评估:实时监控学习效果并反馈优化
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """init自适应学习协调器"""
        self.config = config or {}
        
        # init现有学习模块
        if MODULES_AVAILABLE:
            self.unified_system = UnifiedLearningSystem()
            self.learning_coordinator = LearningCoordinator()
            self.smart_scheduler = self._init_smart_scheduler()
            self.local_learner = LocalDataLearner()
        else:
            logger.warning("基础学习模块不可用,使用简化模式")
        
        # 学习任务池
        self.task_pool: Dict[str, LearningTaskProfile] = {}
        self.learning_plans: Dict[str, LearningPlan] = {}
        
        # 智能调度器
        self.scheduler = AdaptiveScheduler()
        
        # 学习历史
        self.learning_history = LearningHistory()
        
        # 知识图谱
        self.knowledge_graph = KnowledgeGraph()
        
        # 性能监控
        self.monitor = LearningMonitor()
        
        # 并发控制
        self.max_concurrent_tasks = self.config.get("max_concurrent_tasks", 8)
        self.task_semaphore = threading.Semaphore(self.max_concurrent_tasks)
        self.active_tasks: Dict[str, threading.Thread] = {}
        
        # 自适应参数
        self.learning_rate = 0.1  # 学习率
        self.exploration_rate = 0.3  # 探索率
        self.exploitation_rate = 0.7  # 利用率

        # [v2.2.0 道家升级] 自然演化学习配置
        self.nature_config: NatureEvolutionConfig = NatureEvolutionConfig()
        self.nature_enabled: bool = True  # 自然演化总开关
        self._decay_states: Dict[str, KnowledgeDecayState] = {}  # 知识遗忘状态追踪
        self._decay_lock = threading.Lock()
        self._last_refinement_time: float = time.time()
        self._total_learned: int = 0
        self._total_forgotten: int = 0
        self._exploration_history: List[float] = []  # 探索率历史（用于趋势分析）

        # [v2.2.0] 注册到现有系统
        _log_nature(f"[自然演化] 道家学习模式已启用: {self.nature_config.dao_wisdom_enabled}")

        logger.info("自适应学习协调器init完成")
        self._log_system_status()
    
    def _init_smart_scheduler(self) -> Optional[SmartScheduler]:
        """init智能调度器"""
        if not MODULES_AVAILABLE:
            return None
        
        try:
            # get调度strategy
            strategy = self.config.get("scheduling_strategy", "adaptive")
            return SmartScheduler(strategy=strategy)
        except Exception as e:
            logger.warning(f"智能调度器init失败: {e}")
            return None
    
    def _log_system_status(self):
        """记录系统状态"""
        logger.info("=" * 60)
        logger.info("自适应学习协调器状态报告")
        logger.info("=" * 60)
        logger.info(f"最大并发任务数: {self.max_concurrent_tasks}")
        logger.info(f"学习率: {self.learning_rate}")
        logger.info(f"探索率: {self.exploration_rate}")
        logger.info(f"利用率: {self.exploitation_rate}")
        logger.info(f"任务池大小: {len(self.task_pool)}")
        logger.info(f"学习计划数: {len(self.learning_plans)}")
        logger.info(f"知识图谱节点数: {self.knowledge_graph.node_count}")
        if self.nature_enabled:
            logger.info(f"[道家] 自然演化: 启用 | 动态遗忘: {self.nature_config.use_dynamic_decay} | 情境探索: {self.nature_config.use_contextual_exploration} | 自发精炼: {self.nature_config.use_spontaneous_refinement}")
            logger.info(f"[道家] 总学习: {self._total_learned} | 总遗忘: {self._total_forgotten} | 活跃知识: {len(self._decay_states)}")
        logger.info("=" * 60)
    
    def create_learning_plan(self,
                          target_skill: str,
                          learning_stage: LearningStage = LearningStage.FOUNDATION,
                          strategy: LearningStrategy = LearningStrategy.ADAPTIVE) -> LearningPlan:
        """
        创建学习计划
        
        Args:
            target_skill: 目标技能
            learning_stage: 学习阶段
            strategy: 学习strategy
            
        Returns:
            LearningPlan: 学习计划
        """
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 分析学习需求
        skill_analysis = self._analyze_skill_requirement(target_skill)
        
        # 设计学习路径
        learning_path = self._design_learning_path(
            target_skill, 
            learning_stage, 
            strategy, 
            skill_analysis
        )
        
        # 创建学习计划
        plan = LearningPlan(
            plan_id=plan_id,
            target_skill=target_skill,
            learning_stage=learning_stage,
            strategy=strategy,
            learning_path=learning_path,
            total_steps=len(learning_path)
        )
        
        # 添加到计划池
        self.learning_plans[plan_id] = plan
        
        logger.info(f"创建学习计划: {plan_id} - 目标: {target_skill}")
        logger.info(f"学习阶段: {learning_stage.value}, strategy: {strategy.value}")
        logger.info(f"学习路径包含 {len(learning_path)} 个任务")
        
        return plan
    
    def _analyze_skill_requirement(self, target_skill: str) -> Dict[str, Any]:
        """分析技能需求"""
        # 从知识图谱中get技能信息
        skill_info = self.knowledge_graph.get_skill_info(target_skill)
        
        if skill_info:
            return {
                "prerequisites": skill_info.get("prerequisites", []),
                "related_skills": skill_info.get("related_skills", []),
                "difficulty": skill_info.get("difficulty", 5),
                "complexity": skill_info.get("complexity", 0.5),
                "estimated_time_hours": skill_info.get("estimated_time_hours", 20)
            }
        else:
            # 新技能,创建基本信息
            return {
                "prerequisites": [],
                "related_skills": [],
                "difficulty": 5,
                "complexity": 0.5,
                "estimated_time_hours": 20
            }
    
    def _design_learning_path(self,
                            target_skill: str,
                            learning_stage: LearningStage,
                            strategy: LearningStrategy,
                            skill_analysis: Dict[str, Any]) -> List[LearningTaskProfile]:
        """设计学习路径"""
        
        tasks = []
        
        # 1. 前置技能学习任务
        for i, prereq in enumerate(skill_analysis.get("prerequisites", [])):
            task_id = f"prereq_{i+1}_{prereq}"
            task_profile = self._create_task_profile(
                task_id=task_id,
                content_type="skill_prerequisite",
                complexity_score=skill_analysis.get("complexity", 0.5) * 0.7,
                priority=LearningPriority.HIGH,
                content=prereq,
                prerequisites=[]
            )
            tasks.append(task_profile)
            self.task_pool[task_id] = task_profile
        
        # 2. 核心技能学习任务
        if learning_stage == LearningStage.FOUNDATION:
            # 基础阶段:建立核心概念
            for i in range(1, 6):
                task_id = f"core_{i}_{target_skill}"
                task_profile = self._create_task_profile(
                    task_id=task_id,
                    content_type="foundational_concept",
                    complexity_score=skill_analysis.get("complexity", 0.5),
                    priority=LearningPriority.MEDIUM,
                    content=f"{target_skill} 核心概念 {i}",
                    prerequisites=[t.task_id for t in tasks[:min(len(tasks), 3)]]
                )
                tasks.append(task_profile)
                self.task_pool[task_id] = task_profile
        
        elif learning_stage == LearningStage.EXPANSION:
            # 扩展阶段:深入学习
            for i in range(1, 4):
                task_id = f"exp_{i}_{target_skill}"
                task_profile = self._create_task_profile(
                    task_id=task_id,
                    content_type="advanced_concept",
                    complexity_score=skill_analysis.get("complexity", 0.5) * 1.2,
                    priority=LearningPriority.MEDIUM,
                    content=f"{target_skill} 高级概念 {i}",
                    prerequisites=[t.task_id for t in tasks]
                )
                tasks.append(task_profile)
                self.task_pool[task_id] = task_profile
        
        elif learning_stage == LearningStage.INTEGRATION:
            # 整合阶段:知识fusion
            for i in range(1, 3):
                task_id = f"int_{i}_{target_skill}"
                task_profile = self._create_task_profile(
                    task_id=task_id,
                    content_type="integrative_exercise",
                    complexity_score=skill_analysis.get("complexity", 0.5) * 1.5,
                    priority=LearningPriority.LOW,
                    content=f"{target_skill} 整合练习 {i}",
                    prerequisites=[t.task_id for t in tasks]
                )
                tasks.append(task_profile)
                self.task_pool[task_id] = task_profile
        
        elif learning_stage == LearningStage.APPLICATION:
            # 应用阶段:实践应用
            for i in range(1, 2):
                task_id = f"app_{i}_{target_skill}"
                task_profile = self._create_task_profile(
                    task_id=task_id,
                    content_type="practical_application",
                    complexity_score=skill_analysis.get("complexity", 0.5) * 2.0,
                    priority=LearningPriority.LOW,
                    content=f"{target_skill} 实践应用 {i}",
                    prerequisites=[t.task_id for t in tasks]
                )
                tasks.append(task_profile)
                self.task_pool[task_id] = task_profile
        
        # 3. 关联技能拓展任务
        related_skills = skill_analysis.get("related_skills", [])
        for i, related in enumerate(related_skills[:2]):
            task_id = f"related_{i+1}_{related}"
            task_profile = self._create_task_profile(
                task_id=task_id,
                content_type="skill_extension",
                complexity_score=skill_analysis.get("complexity", 0.5) * 0.8,
                priority=LearningPriority.LOW,
                content=f"拓展技能: {related}",
                prerequisites=[t.task_id for t in tasks]
            )
            tasks.append(task_profile)
            self.task_pool[task_id] = task_profile
        
        return tasks
    
    def _create_task_profile(self,
                          task_id: str,
                          content_type: str,
                          complexity_score: float,
                          priority: LearningPriority,
                          content: str,
                          prerequisites: List[str]) -> LearningTaskProfile:
        """创建学习任务画像"""
        # 根据内容类型估算时间
        time_estimates = {
            "skill_prerequisite": 2.0,
            "foundational_concept": 3.0,
            "advanced_concept": 4.0,
            "integrative_exercise": 5.0,
            "practical_application": 6.0,
            "skill_extension": 3.5
        }
        
        base_time = time_estimates.get(content_type, 3.0)
        estimated_time = base_time * (1 + complexity_score)
        
        # 基于复杂度估算难度
        difficulty_level = min(10, max(1, int(complexity_score * 10)))
        
        return LearningTaskProfile(
            task_id=task_id,
            content_type=content_type,
            complexity_score=complexity_score,
            priority=priority,
            estimated_time=estimated_time * 3600,  # 转换为秒
            difficulty_level=difficulty_level,
            importance_score=self._calculate_importance(priority, complexity_score),
            prerequisites=prerequisites
        )
    
    def _calculate_importance(self, priority: LearningPriority, complexity: float) -> float:
        """计算重要性分数"""
        # 基于优先级和复杂度计算重要性
        
        priority_weight = {
            LearningPriority.P0_CRITICAL: 1.0,
            LearningPriority.P1_HIGH: 0.8,
            LearningPriority.P2_MEDIUM: 0.6,
            LearningPriority.P3_LOW: 0.4,
        }.get(priority, 0.5)
        
        complexity_weight = 0.5 * (1 + complexity)  # 复杂度越高,越重要
        
        return (priority_weight * 0.7 + complexity_weight * 0.3)
    
    def execute_learning_plan(self, plan_id: str) -> Dict[str, Any]:
        """
        执行学习计划
        
        Args:
            plan_id: 学习计划ID
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        if plan_id not in self.learning_plans:
            return {
                "success": False,
                "error": f"学习计划不存在: {plan_id}",
                "progress": 0.0
            }
        
        plan = self.learning_plans[plan_id]
        logger.info(f"开始执行学习计划: {plan_id} - {plan.target_skill}")
        
        # 执行学习计划
        results = self._execute_plan_tasks(plan)
        
        # generate学习报告

        report = self._generate_learning_report(plan, results)
        
        # 记录学习历史
        self.learning_history.record_plan_execution(plan_id, results)
        
        # 更新知识图谱
        self.knowledge_graph.update_skill_mastery(plan.target_skill, results)
        
        logger.info(f"学习计划执行完成: {plan_id} - 成功率: {report['success_rate']:.2%}")
        
        return {
            "success": True,
            "plan_id": plan_id,
            "target_skill": plan.target_skill,
            "results": results,
            "report": report
        }
    
    def _execute_plan_tasks(self, plan: LearningPlan) -> Dict[str, Any]:
        """执行计划中的任务"""
        results = {
            "completed": [],
            "failed": [],
            "in_progress": [],
            "total_tasks": len(plan.learning_path),
            "start_time": time.time(),
            "end_time": None
        }
        
        # 创建线程池执行任务
        threads = []
        completed_count = 0
        
        for i, task in enumerate(plan.learning_path):
            if task.status == "pending":
                # 检查前置任务是否完成

                prerequisites_met = all(
                    prereq_id in results["completed"] 
                    for prereq_id in task.prerequisites
                )
                
                if not prerequisites_met:
                    logger.warning(f"任务 {task.task_id} 前置条件未满足,跳过")
                    task.status = "failed"
                    results["failed"].append(task.task_id)
                    continue
                
                # 执行任务

                thread = self._execute_task_thread(task, plan)
                threads.append(thread)
                results["in_progress"].append(task.task_id)
                
                # 控制并发数
                if len(self.active_tasks) >= self.max_concurrent_tasks:
                    self._wait_for_task_completion()
        
        # 等待所有任务完成
        self._wait_for_all_tasks(threads)
        
        results["end_time"] = time.time()
        results["duration_seconds"] = results["end_time"] - results["start_time"]
        
        return results
    
    def _execute_task_thread(self, task: LearningTaskProfile, plan: LearningPlan) -> threading.Thread:
        """创建任务执行线程"""
        thread = threading.Thread(
            target=self._execute_learning_task,
            args=(task, plan),
            daemon=True
        )
        
        task.start_time = time.time()
        task.status = "in_progress"
        self.active_tasks[task.task_id] = thread
        
        thread.start()
        
        return thread
    
    def _execute_learning_task(self, task: LearningTaskProfile, plan: LearningPlan):
        """执行学习任务"""
        try:
            with self.task_semaphore:
                logger.info(f"开始执行学习任务: {task.task_id}")
                
                # 记录开始时间
                start_time = time.time()
                
                # 执行学习任务
                success = self._execute_specific_learning_task(task, plan)
                
                # 记录结束时间和状态
                task.end_time = time.time()
                task.status = "completed" if success else "failed"
                
                # 计算实际耗时
                actual_time = task.end_time - start_time
                
                # 记录性能metrics

                performance_data = {
                    "success": success,
                    "actual_time": actual_time,
                    "estimated_time": task.estimated_time,
                    "efficiency": min(1.0, task.estimated_time / max(actual_time, 1)),
                    "difficulty_handled": task.difficulty_level if success else task.difficulty_level * 0.5
                }
                
                task.historical_performance.append(performance_data)
                task.success_rate = len([p for p in task.historical_performance if p.get("success", False)]) / max(1, len(task.historical_performance))
                
                logger.info(f"学习任务完成: {task.task_id} - 成功: {success} - 耗时: {actual_time:.1f}s")
                
                # 更新任务状态
                self.monitor.record_task_completion(task.task_id, success, actual_time)
        
        except Exception as e:
            logger.error(f"学习任务执行异常: {task.task_id} - {str(e)}")
            task.status = "failed"
        finally:
            # 清理活动任务
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    def _execute_specific_learning_task(self, task: LearningTaskProfile, plan: LearningPlan) -> bool:
        """执行具体的学习任务"""
        # 根据任务类型执行相应的学习逻辑
        
        if task.content_type == "skill_prerequisite":
            # 前置技能学习
            return self._learn_skill_prerequisite(task, plan)
        
        elif task.content_type == "foundational_concept":
            # 核心概念学习
            return self._learn_foundational_concept(task, plan)
        
        elif task.content_type == "advanced_concept":
            # 高级概念学习
            return self._learn_advanced_concept(task, plan)
        
        elif task.content_type == "integrative_exercise":
            # 整合练习
            return self._learn_integrative_exercise(task, plan)
        
        elif task.content_type == "practical_application":
            # 实践应用
            return self._learn_practical_application(task, plan)
        
        elif task.content_type == "skill_extension":
            # 技能拓展
            return self._learn_skill_extension(task, plan)
        
        else:
            logger.warning(f"未知的任务类型: {task.content_type}")
            return False
    
    def _learn_skill_prerequisite(self, task: LearningTaskProfile, plan: LearningPlan) -> bool:
        """学习前置技能"""
        # 简化的技能学习逻辑
        try:
            # 模拟学习过程
            time.sleep(min(60, task.estimated_time / 10))  # 最多60秒
            
            # 随机成功概率,基于难度调整
            base_success_rate = 0.8
            difficulty_factor = 1.0 - (task.difficulty_level / 20)
            success_probability = base_success_rate * difficulty_factor
            
            return random.random() < success_probability
        
        except Exception as e:

            logger.error(f"技能学习失败: {task.task_id} - {str(e)}")
            return False
    
    def _learn_foundational_concept(self, task: LearningTaskProfile, plan: LearningPlan) -> bool:
        """学习核心概念"""
        # 与技能学习类似,但成功率稍低

        try:

            time.sleep(min(90, task.estimated_time / 8))
            
            base_success_rate = 0.75

            difficulty_factor = 1.0 - (task.difficulty_level / 18)
            success_probability = base_success_rate * difficulty_factor
            
            return random.random() < success_probability
        
        except Exception as e:
            logger.error(f"概念学习失败: {task.task_id} - {str(e)}")
            return False
    
    # 其他学习方法类似实现...
    
    def _wait_for_task_completion(self):
        """等待任务完成"""
        # 简单的等待strategy
        time.sleep(1)
    
    def _wait_for_all_tasks(self, threads: List[threading.Thread]):
        """等待所有任务完成"""
        for thread in threads:
            if thread.is_alive():
                thread.join(timeout=300)  # 最多等待5分钟
    
    def _generate_learning_report(self, plan: LearningPlan, results: Dict[str, Any]) -> Dict[str, Any]:
        """generate学习报告"""
        completed_count = len(results["completed"])
        total_count = results["total_tasks"]
        
        success_rate = completed_count / total_count if total_count > 0 else 0.0
        
        # 计算平均学习效率

        efficiencies = []
        for task in plan.learning_path:

            if task.historical_performance:

                latest_performance = task.historical_performance[-1]
                efficiency = latest_performance.get("efficiency", 0.0)
                efficiencies.append(efficiency)
        
        avg_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0.0
        
        # 计算总体掌握度
        mastery_score = self._calculate_mastery_score(plan, results)
        
        return {
            "plan_id": plan.plan_id,
            "target_skill": plan.target_skill,
            "success_rate": success_rate,
            "completed_tasks": completed_count,
            "total_tasks": total_count,
            "duration_seconds": results.get("duration_seconds", 0),
            "efficiency": avg_efficiency,
            "mastery_score": mastery_score,
            "strategic_insights": self._generate_strategic_insights(plan, results)
        }
    
    def _calculate_mastery_score(self, plan: LearningPlan, results: Dict[str, Any]) -> float:
        """计算掌握度分数"""
        if not plan.learning_path:

            return 0.0
        
        total_score = 0.0
        weighted_total = 0.0
        
        for task in plan.learning_path:

            # 任务重要性权重

            task_weight = task.importance_score
            
            # 任务掌握度
            if task.status == "completed":
                # 基于任务难度和历史表现

                base_mastery = 0.8
                difficulty_factor = 1.0 - (task.difficulty_level / 20)
                
                # 考虑历史成功率

                if task.historical_performance:
                    success_count = sum(1 for perf in task.historical_performance if perf.get("success", False))
                    total_attempts = len(task.historical_performance)
                    historical_success_rate = success_count / total_attempts
                else:
                    historical_success_rate = 0.7
                
                task_mastery = (base_mastery * 0.6 + 
                              difficulty_factor * 0.2 + 
                              historical_success_rate * 0.2)
            else:
                task_mastery = 0.0
            
            total_score += task_mastery * task_weight
            weighted_total += task_weight
        
        return total_score / weighted_total if weighted_total > 0 else 0.0
    
    def _generate_strategic_insights(self, plan: LearningPlan, results: Dict[str, Any]) -> List[str]:
        """generate战略洞察"""
        insights = []
        
        # 分析学习效果
        completed_count = len(results.get("completed", []))
        total_count = results.get("total_tasks", 1)
        success_rate = completed_count / max(1, total_count)
        
        if success_rate > 0.8:
            insights.append(f"学习效果优秀:目标技能 {plan.target_skill} 掌握度超过 80%")
            insights.append("建议进入下一阶段学习或拓展相关高级技能")
        elif success_rate > 0.6:
            insights.append(f"学习效果良好:目标技能 {plan.target_skill} 掌握度达到 {success_rate:.1%}")
            insights.append("建议巩固基础并逐步向高级概念拓展")
        else:
            insights.append(f"学习效果需提升:目标技能 {plan.target_skill} 掌握度为 {success_rate:.1%}")
            insights.append("建议分析学习难点,调整学习strategy")

        # 基于任务难度分布分析
        difficulty_levels = [t.difficulty_level for t in plan.learning_path]
        if difficulty_levels:
            avg_difficulty = sum(difficulty_levels) / len(difficulty_levels)
            if avg_difficulty > 7:
                insights.append("学习内容整体难度较高,建议分阶段,多轮次学习")
            elif avg_difficulty < 4:
                insights.append("学习内容相对基础,可以考虑挑战更高难度任务")
        
        return insights

    # ── v2.2.0: 道家自然演化学习核心方法 ──────────────────────────────────

    def set_nature_evolution(self, enabled: bool, config: Optional[NatureEvolutionConfig] = None):
        """
        开启/关闭自然演化学习模式。

        [道家解读] "为学日益，为道日损"——开启道家模式后，
        系统将从"不断增加知识"转向"提炼本质智慧"。
        """
        self.nature_enabled = enabled
        if config is not None:
            self.nature_config = config
        _log_nature(f"[自然演化] {'启用' if enabled else '停用'} | decay={self.nature_config.use_dynamic_decay} | explore={self.nature_config.use_contextual_exploration} | refine={self.nature_config.use_spontaneous_refinement}")

    def register_knowledge_usage(self, knowledge_id: str, importance: float = 0.5):
        """
        [动态遗忘] 注册知识使用——"水善利万物而不争"。

        每次知识被使用时，调用此方法更新其新鲜度状态。
        高频使用的知识将获得遗忘率减免，体现"长用常新"的自然法则。

        [道家解读] 水不争而自流，知识不用则渐失，这是自然之理。
        """
        current_time = time.time()
        with self._decay_lock:
            if knowledge_id not in self._decay_states:
                self._decay_states[knowledge_id] = KnowledgeDecayState(
                    knowledge_id=knowledge_id,
                    last_used_time=current_time,
                    use_count=1,
                    base_importance=importance,
                    freshness_score=1.0,
                )
            else:
                state = self._decay_states[knowledge_id]
                state.use_count += 1
                state.last_used_time = current_time
                # 水善利万物：高频使用 = 高水流得分
                state.water_flow_score = min(state.use_count / 10.0, 1.0)

    def compute_dynamic_decay(self, knowledge_id: str) -> float:
        """
        [动态遗忘核心] 计算知识的动态遗忘率——"致虚极守静笃"。

        遗忘率 = 基础遗忘率 × 时间衰减因子 / 使用频率补偿

        设计原理：
        - 时间越久远，遗忘倾向越强（指数衰减）
        - 使用频率越高，遗忘阻力越大（对数补偿）
        - 基础重要性越高，遗忘越慢（线性加权）

        [道家解读] "致虚极"——主动清空，为新知留出空间。
        不是知识的堆积，而是智慧的提炼。

        Returns:
            float: 当前遗忘率（0-1，越高表示越接近遗忘阈值）
        """
        if not self.nature_enabled or not self.nature_config.use_dynamic_decay:
            return 0.0

        with self._decay_lock:
            if knowledge_id not in self._decay_states:
                return self.nature_config.base_decay_rate

            state = self._decay_states[knowledge_id]
            elapsed_days = (time.time() - state.last_used_time) / 86400.0

            # 时间衰减因子：基于指数衰减的自然遗忘曲线
            time_factor = 1 - math.exp(-elapsed_days / self.nature_config.decay_half_life_days)

            # 使用频率补偿：高频使用的知识遗忘更慢
            # 公式：补偿 = log(使用次数+1) / log(最大期望次数+1)
            usage_factor = 1.0 / (1.0 + math.log(state.use_count + 1) * self.nature_config.usage_boost_factor * 0.5)

            # 综合遗忘率
            decay = self.nature_config.base_decay_rate * time_factor * usage_factor
            decay = min(max(decay, self.nature_config.min_decay_rate), self.nature_config.max_decay_rate)

            # 更新状态
            state.current_decay = decay
            state.freshness_score = max(0.0, 1.0 - decay)
            self._total_forgotten += 1

            # 道家评估
            if state.water_flow_score > 0.7:
                state.dao_assessment = "【上善若水】高频使用，生命力旺盛。"
            elif state.water_flow_score > 0.3:
                state.dao_assessment = "【涓涓细流】偶尔使用，仍有活力。"
            else:
                state.dao_assessment = "【静水将腐】久未使用，趋于遗忘。"

            return decay

    def compute_contextual_exploration(self, context: Optional[ExplorationContext] = None) -> float:
        """
        [情境探索核心] 计算当前情境下的最优探索率——"因时因地，顺势而为"。

        探索率根据以下因素动态调整：
        - 系统负载：低负载时可提高探索（无为而治的空间更大）
        - 知识密度：知识密集时降低探索，专注利用
        - 不确定性：高度不确定时提高探索，寻求新知

        [道家解读] "上善若水，水无常形"——好的学习策略如水一样，
        没有固定不变的最优参数，而是根据环境灵活变化。

        Returns:
            float: 当前推荐探索率（0-1）
        """
        if not self.nature_enabled or not self.nature_config.use_contextual_exploration:
            return self.exploration_rate

        base = self.nature_config.base_exploration_rate
        sensitivity = self.nature_config.exploration_context_sensitivity

        if context is None:
            # 默认情境：基于系统当前状态推断
            active_ratio = len(self.active_tasks) / max(self.max_concurrent_tasks, 1)
            context = ExplorationContext(
                system_load=active_ratio,
                uncertainty_level=0.5,
            )

        # 计算负载因子（低负载 → 提高探索）
        load_adjustment = (1.0 - context.system_load) * sensitivity

        # 计算不确定性因子（高不确定性 → 提高探索）
        uncertainty_adjustment = context.uncertainty_level * sensitivity

        # 计算知识密度因子（高密度 → 降低探索）
        density_adjustment = -context.knowledge_density * sensitivity * 0.5

        # 计算阴阳平衡因子
        yin_factor = 1.0 - context.yin_yang_balance  # 偏阴 → 更多探索（向内）
        yang_factor = context.yin_yang_balance          # 偏阳 → 更多利用（向外）

        total_adjustment = load_adjustment + uncertainty_adjustment + density_adjustment
        adjusted_rate = base + total_adjustment * base

        # 限制在范围内
        exploration_rate = min(
            max(adjusted_rate, self.nature_config.min_exploration_rate),
            self.nature_config.max_exploration_rate
        )

        # 记录历史
        self._exploration_history.append(exploration_rate)
        if len(self._exploration_history) > 100:
            self._exploration_history = self._exploration_history[-100:]

        # 更新全局探索率
        self.exploration_rate = exploration_rate
        self.exploitation_rate = 1.0 - exploration_rate

        # 生成道家建议
        if exploration_rate > base * 1.2:
            context.dao_recommendation = "【阳气充盈】宜广开探索，寻求新知。"
        elif exploration_rate < base * 0.8:
            context.dao_recommendation = "【阴气内敛】宜专注深耕，涵养已知。"
        else:
            context.dao_recommendation = "【阴阳平衡】探索与利用并济，自然和谐。"

        return exploration_rate

    def check_spontaneous_refinement(self) -> Dict[str, Any]:
        """
        [自发性精炼核心] 检查并执行自发精炼——"无为而治，自我优化"。

        当系统处于低负载状态时，自动触发知识精炼流程：
        1. 评估当前知识池的健康度
        2. 识别高遗忘率知识（接近淘汰）
        3. 对高价值知识进行巩固，对低价值知识放行遗忘

        [道家解读] "致虚极，守静笃"——在高负载时无法看清的本质，
        在低负载时自然浮现。系统应利用这个窗口进行自我审视和精炼。

        Returns:
            Dict: 精炼报告，包含识别到的知识状态和建议
        """
        if not self.nature_enabled or not self.nature_config.use_spontaneous_refinement:
            return {"triggered": False, "reason": "自发精炼未启用"}

        # 检查时间间隔
        elapsed_hours = (time.time() - self._last_refinement_time) / 3600.0
        if elapsed_hours < self.nature_config.refinement_interval_hours:
            return {"triggered": False, "reason": f"距上次精炼仅{elapsed_hours:.1f}小时，未达间隔"}

        # 检查系统负载
        active_ratio = len(self.active_tasks) / max(self.max_concurrent_tasks, 1)
        if active_ratio > self.nature_config.refinement_trigger_load_threshold:
            return {"triggered": False, "reason": f"系统负载{active_ratio:.1%}过高，不宜精炼"}

        # 执行精炼
        self._last_refinement_time = time.time()
        with self._decay_lock:
            states = list(self._decay_states.values())

        if not states:
            return {"triggered": True, "refined": 0, "dao_summary": "【虚】知识池为空，无需精炼。"}

        # 分析知识新鲜度分布
        freshness_scores = [s.freshness_score for s in states]
        avg_freshness = sum(freshness_scores) / len(freshness_scores)

        # 识别不同状态的知识
        vigorous = [s for s in states if s.freshness_score > 0.8]  # 活跃
        stable = [s for s in states if 0.5 <= s.freshness_score <= 0.8]  # 稳定
        fading = [s for s in states if 0.2 <= s.freshness_score < 0.5]  # 渐衰
        dormant = [s for s in states if s.freshness_score < 0.2]  # 休眠

        # 计算精炼结果
        refined_count = len(vigorous) + len(stable) + len(fading)
        dormant_count = len(dormant)
        total_count = len(states)

        # 生成道家总结
        if dormant_count > total_count * 0.5:
            dao_summary = "【损之又损】知识池中超过半数已趋休眠，主动放行遗忘，为新知让路。"
        elif avg_freshness > 0.7:
            dao_summary = "【生气盎然】知识池整体健康，保持现有学习节奏。"
        elif avg_freshness > 0.5:
            dao_summary = "【阴阳交错】活跃与休眠并存，适度遗忘有益于智慧提炼。"
        else:
            dao_summary = "【将生将死】知识池整体衰退，需补充新知以维持活力。"

        # 对休眠知识执行遗忘（从追踪表中移除）
        for state in dormant:
            with self._decay_lock:
                if state.knowledge_id in self._decay_states:
                    del self._decay_states[state.knowledge_id]

        _log_nature(f"[自发精炼] 完成: 总={total_count} 活跃={len(vigorous)} 稳定={len(stable)} 渐衰={len(fading)} 遗忘={dormant_count} | {dao_summary}")

        return {
            "triggered": True,
            "refined": refined_count,
            "forgotten": dormant_count,
            "avg_freshness": avg_freshness,
            "total_tracked": total_count,
            "dao_summary": dao_summary,
            "insights": [
                f"【大吉】{len(vigorous)}个知识活跃有力（上善若水）",
                f"【中吉】{len(stable)}个知识状态稳定（阴阳平衡）",
                f"【平】{len(fading)}个知识趋于衰减（致虚极）",
                f"【无为】{dormant_count}个知识已放行遗忘（为道日损）",
            ],
        }

    def get_nature_evolution_status(self) -> Dict[str, Any]:
        """
        获取自然演化学习状态报告——"万物并作，吾以观复"。

        [道家解读] 定期审视自身，如镜子照见万物，
        不是为了改变什么，而是清楚自己正在哪里。
        """
        with self._decay_lock:
            total = len(self._decay_states)
            if total == 0:
                freshness_list = []
            else:
                freshness_list = [s.freshness_score for s in self._decay_states.values()]

        avg_freshness = sum(freshness_list) / len(freshness_list) if freshness_list else 0.0

        # 探索率趋势
        if len(self._exploration_history) >= 2:
            trend = "上升" if self._exploration_history[-1] > self._exploration_history[0] else "下降"
        else:
            trend = "平稳"

        return {
            "nature_enabled": self.nature_enabled,
            "config_summary": {
                "dynamic_decay": self.nature_config.use_dynamic_decay,
                "contextual_exploration": self.nature_config.use_contextual_exploration,
                "spontaneous_refinement": self.nature_config.use_spontaneous_refinement,
            },
            "knowledge_pool": {
                "total_tracked": total,
                "total_learned": self._total_learned,
                "total_forgotten": self._total_forgotten,
                "avg_freshness": avg_freshness,
            },
            "exploration": {
                "current_rate": self.exploration_rate,
                "exploitation_rate": self.exploitation_rate,
                "history_avg": sum(self._exploration_history) / len(self._exploration_history) if self._exploration_history else 0.0,
                "trend": trend,
            },
            "dao_wisdom": {
                "proverb": self.nature_config.water_flow_reminder,
                "status": "活跃" if self.nature_enabled else "停用",
                "health": "优" if avg_freshness > 0.7 else ("良" if avg_freshness > 0.4 else "需关注"),
            },
        }


def _log_nature(msg: str):
    """自然演化学习日志"""
    try:
        from loguru import logger
        logger.info(f"[自然演化道家] {msg}")
    except ImportError:
        import sys
        sys.stderr.write(f"[自然演化道家] {msg}\n")



class AdaptiveScheduler:
    """自适应调度器"""
    
    def __init__(self):
        self.task_queue = []
        self.priority_weights = {
            "critical": 5.0,
            "high": 3.0,
            "medium": 2.0,
            "low": 1.0,
            "background": 0.5
        }
    
    def schedule_tasks(self, tasks: List[LearningTaskProfile]) -> List[LearningTaskProfile]:
        """调度任务"""
        # 根据优先级和复杂性排序
        scored_tasks = []
        for task in tasks:
            score = self._calculate_scheduling_score(task)
            scored_tasks.append((score, task))
        
        # 按分数降序排序
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        
        return [task for _, task in scored_tasks]
    
    def _calculate_scheduling_score(self, task: LearningTaskProfile) -> float:
        """计算调度分数"""
        priority_score = self.priority_weights.get(task.priority.value, 1.0)
        complexity_factor = 1.0 + task.complexity_score * 0.5
        
        return priority_score * complexity_factor

class LearningHistory:
    """学习历史记录"""
    
    def __init__(self):
        self.history = []
        self.statistics = defaultdict(lambda: {
            "total_attempts": 0,
            "successful_attempts": 0,
            "total_time": 0.0,
            "avg_time": 0.0
        })
    
    def record_plan_execution(self, plan_id: str, results: Dict[str, Any]):
        """记录学习计划执行"""
        record = {
            "plan_id": plan_id,
            "execution_time": datetime.now().isoformat(),
            "results": results,
            "timestamp": time.time()
        }
        
        self.history.append(record)
        
        # 更新统计信息
        self._update_statistics(results)
    
    def _update_statistics(self, results: Dict[str, Any]):
        """更新统计信息"""
        for task_id in results.get("completed", []):
            self.statistics[task_id]["total_attempts"] += 1
            self.statistics[task_id]["successful_attempts"] += 1
        
        for task_id in results.get("failed", []):
            self.statistics[task_id]["total_attempts"] += 1

class KnowledgeGraph:
    """知识图谱"""
    
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)
        self.node_count = 0
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """get技能信息"""
        return self.nodes.get(skill_name)
    
    def update_skill_mastery(self, skill_name: str, results: Dict[str, Any]):
        """更新技能掌握度"""
        if skill_name not in self.nodes:
            self.nodes[skill_name] = {
                "mastery_level": 0.0,
                "related_skills": [],
                "prerequisites": [],
                "complexity": 0.5,
                "difficulty": 5
            }
        
        # 基于执行结果更新掌握度

        self.nodes[skill_name]["mastery_level"] = min(1.0, self.nodes[skill_name]["mastery_level"] + 0.2)

class LearningMonitor:
    """学习监控器"""
    
    def __init__(self):
        self.metrics = {
            "task_completion_times": [],
            "success_rates": [],
            "resource_usage": [],
            "learning_efficiency": []
        }
        self.alerts = []
    
    def record_task_completion(self, task_id: str, success: bool, duration: float):
        """记录任务完成情况"""
        self.metrics["task_completion_times"].append(duration)
        
        # 记录成功/失败
        if success:

            self.metrics["success_rates"].append(1.0)
        else:

            self.metrics["success_rates"].append(0.0)
        
        # 检查是否异常

        self._check_anomalies(task_id, success, duration)
    
    def _check_anomalies(self, task_id: str, success: bool, duration: float):
        """检查异常情况"""
        if duration > 3600:  # 超过1小时

            self.alerts.append(f"任务 {task_id} 执行时间过长: {duration:.1f}s")
        
        if not success:

            self.alerts.append(f"任务 {task_id} 执行失败")

__all__ = [
    'LearningStage', 'LearningStrategy', 'LearningTaskProfile',
    'LearningPlan', 'AdaptiveLearningCoordinator', 'AdaptiveScheduler',
    'LearningHistory', 'KnowledgeGraph', 'LearningMonitor',
]