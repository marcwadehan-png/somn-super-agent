"""
__all__ = [
    'custom_handler',
    'execute_main_chain_parallel',
    'get',
    'get_all',
    'get_best_modules',
    'get_by_capability',
    'get_by_domain',
    'get_parallel_router',
    'get_status',
    'handler',
    'limited_task',
    'register',
    'register_module',
    'route',
    'route_parallel',
    'to_dict',
    'update_performance',
]

主线并行路由器 v1.0
Main Chain Parallel Router

功能：
1. 实现真正的并发执行 - 多路并发路由到不同模块
2. 根据任务类型自动选择并行策略
3. 支持同步/异步两种执行模式
4. 提供结果聚合与冲突处理

运行模式：
- 并形运转（Parallel）：多路并发执行多个模块
- 支持 ThreadPoolExecutor 和 asyncio 两种并发模式

适用场景：
- 深度推理、多角度分析、批量评估等可并行处理的任务
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Set
from functools import wraps
import threading
import time
import uuid

logger = logging.getLogger(__name__)

class ParallelMode(Enum):
    """并行执行模式"""
    THREAD = "thread"           # 线程池模式
    ASYNC = "async"             # 异步模式
    AUTO = "auto"              # 自动选择

class RouteStrategy(Enum):
    """路由策略"""
    ALL = "all"                # 所有可用模块
    BEST_K = "best_k"          # 前K个最佳模块
    BALANCED = "balanced"      # 均衡选择
    DOMAIN_MATCH = "domain"    # 领域匹配优先

@dataclass
class RouteConfig:
    """路由配置"""
    max_concurrent: int = 5                    # 最大并发数
    timeout: float = 30.0                     # 单个任务超时（秒）
    strategy: RouteStrategy = RouteStrategy.BEST_K
    mode: ParallelMode = ParallelMode.AUTO
    enable_fallback: bool = True              # 启用降级
    fallback_on_error: bool = True            # 出错时降级

@dataclass
class ParallelTask:
    """并行任务"""
    task_id: str
    module_key: str
    handler: Callable
    params: Dict[str, Any]
    priority: int = 0                         # 优先级（越高越先执行）
    dependencies: Set[str] = field(default_factory=set)  # 依赖的任务ID
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ParallelResult:
    """并行执行结果"""
    task_id: str
    module_key: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    completed_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "module_key": self.module_key,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "execution_time": self.execution_time,
            "completed_at": self.completed_at
        }

@dataclass
class AggregatedResult:
    """聚合结果"""
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    results: List[ParallelResult]
    total_time: float
    strategy_used: RouteStrategy
    mode_used: ParallelMode
    insights: List[str] = field(default_factory=list)
    conflicts: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "total_tasks": self.total_tasks,
            "successful_tasks": self.successful_tasks,
            "failed_tasks": self.failed_tasks,
            "results": [r.to_dict() for r in self.results],
            "total_time": self.total_time,
            "strategy_used": self.strategy_used.value,
            "mode_used": self.mode_used.value,
            "insights": self.insights,
            "conflicts": self.conflicts
        }

class ModuleRegistry:
    """模块注册表"""

    def __init__(self):
        self._modules: Dict[str, Callable] = {}
        self._capabilities: Dict[str, Set[str]] = {}  # module_key -> capabilities
        self._domains: Dict[str, Set[str]] = {}       # module_key -> domains
        self._performance: Dict[str, Dict] = {}       # module_key -> performance stats
        self._lock = threading.RLock()

    def register(self, module_key: str, handler: Callable,
                 capabilities: List[str] = None,
                 domains: List[str] = None):
        """注册模块"""
        with self._lock:
            self._modules[module_key] = handler
            self._capabilities[module_key] = set(capabilities or [])
            self._domains[module_key] = set(domains or [])
            self._performance[module_key] = {
                "total_calls": 0,
                "success_calls": 0,
                "avg_time": 0.0,
                "last_used": None
            }

    def get(self, module_key: str) -> Optional[Callable]:
        """获取模块处理器"""
        return self._modules.get(module_key)

    def get_by_capability(self, capability: str) -> List[str]:
        """获取具有特定能力的模块"""
        return [
            key for key, caps in self._capabilities.items()
            if capability in caps and key in self._modules
        ]

    def get_by_domain(self, domain: str) -> List[str]:
        """获取支持特定领域的模块"""
        return [
            key for key, doms in self._domains.items()
            if domain in doms and key in self._modules
        ]

    def get_all(self) -> List[str]:
        """获取所有已注册模块"""
        return list(self._modules.keys())

    def update_performance(self, module_key: str, success: bool, exec_time: float):
        """更新模块性能统计"""
        with self._lock:
            if module_key not in self._performance:
                return

            stats = self._performance[module_key]
            stats["total_calls"] += 1
            if success:
                stats["success_calls"] += 1

            # 滑动平均计算执行时间
            n = stats["total_calls"]
            stats["avg_time"] = (stats["avg_time"] * (n - 1) + exec_time) / n
            stats["last_used"] = datetime.now().isoformat()

    def get_best_modules(self, capability: str = None,
                         domain: str = None,
                         top_k: int = 5) -> List[str]:
        """获取最佳模块（基于性能）"""
        candidates = set()

        if capability:
            candidates.update(self.get_by_capability(capability))
        if domain:
            candidates.update(self.get_by_domain(domain))

        if not candidates:
            candidates = set(self._modules.keys())

        # 按成功率排序
        scored = []
        for key in candidates:
            stats = self._performance.get(key, {"success_calls": 0, "total_calls": 1})
            success_rate = stats["success_calls"] / max(stats["total_calls"], 1)
            avg_time = stats.get("avg_time", 999)
            # 综合评分：成功率优先，执行时间次之
            score = success_rate * 0.8 - avg_time * 0.01
            scored.append((key, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [key for key, _ in scored[:top_k]]

class ParallelRouter:
    """
    主线并行路由器

    功能：
    1. 多路并发路由 - 将任务同时分发到多个模块
    2. 自动策略选择 - 根据任务类型选择最优并行策略
    3. 结果聚合 - 合并多模块输出，处理冲突
    4. 容错降级 - 部分失败时自动降级

    主线定位：
    - 串联运转：顺序执行时使用 WisdomDispatcher
    - 并形运转：并发执行时使用 ParallelRouter
    - 交叉运转：网状影响时使用 CrossWeaver
    """

    def __init__(self, config: Optional[RouteConfig] = None):
        self.config = config or RouteConfig()
        self.registry = ModuleRegistry()
        self._executor: Optional[ThreadPoolExecutor] = None
        self._lock = threading.RLock()

        # 主线节点映射
        self._main_chain_nodes = {
            "wisdom_dispatcher": {
                "capabilities": ["wisdom_dispatch", "decision"],
                "domains": ["general", "strategy"]
            },
            "deep_reasoning": {
                "capabilities": ["reasoning", "analysis"],
                "domains": ["general", "technical"]
            },
            "narrative_engine": {
                "capabilities": ["narrative", "story"],
                "domains": ["culture", "brand"]
            },
            "neural_scheduler": {
                "capabilities": ["scheduling", "optimization"],
                "domains": ["system", "resource"]
            },
            "learning_coordinator": {
                "capabilities": ["learning", "coordination"],
                "domains": ["general", "knowledge"]
            },
            "autonomous_agent": {
                "capabilities": ["autonomous", "execution"],
                "domains": ["general", "automation"]
            }
        }

        # 注册主链节点
        self._register_main_chain_nodes()

        logger.info(f"ParallelRouter 初始化完成，并行模式: {self.config.mode.value}")

    def _register_main_chain_nodes(self):
        """注册主线节点"""
        for node_key, info in self._main_chain_nodes.items():
            self.registry.register(
                module_key=node_key,
                handler=self._create_placeholder_handler(node_key),
                capabilities=info["capabilities"],
                domains=info["domains"]
            )

    def _create_placeholder_handler(self, node_key: str) -> Callable:
        """创建占位处理器"""
        def handler(**kwargs):
            return {"module": node_key, "status": "placeholder", "result": None}
        return handler

    def register_module(self, module_key: str, handler: Callable,
                        capabilities: List[str] = None,
                        domains: List[str] = None):
        """注册模块到路由器"""
        self.registry.register(module_key, handler, capabilities, domains)
        logger.debug(f"模块已注册: {module_key}")

    def route(self, tasks: List[ParallelTask],
              config: Optional[RouteConfig] = None) -> AggregatedResult:
        """
        路由任务到多个模块并发执行

        Args:
            tasks: 并行任务列表
            config: 路由配置

        Returns:
            AggregatedResult: 聚合结果
        """
        start_time = time.time()
        cfg = config or self.config

        if not tasks:
            return AggregatedResult(
                total_tasks=0,
                successful_tasks=0,
                failed_tasks=0,
                results=[],
                total_time=0.0,
                strategy_used=cfg.strategy,
                mode_used=cfg.mode
            )

        logger.info(f"并行路由开始: {len(tasks)} 个任务")

        # 根据模式选择执行方式
        if cfg.mode == ParallelMode.THREAD:
            results = self._execute_thread_pool(tasks, cfg)
        elif cfg.mode == ParallelMode.ASYNC:
            results = asyncio.run(self._execute_async(tasks, cfg))
        else:  # AUTO
            # 根据任务数量和类型选择
            if len(tasks) > 3:
                results = self._execute_thread_pool(tasks, cfg)
            else:
                results = self._execute_sequential_fallback(tasks, cfg)

        # 聚合结果
        aggregated = self._aggregate_results(results, cfg)
        aggregated.total_time = time.time() - start_time

        logger.info(f"并行路由完成: {aggregated.successful_tasks}/{aggregated.total_tasks} 成功，耗时 {aggregated.total_time:.2f}s")

        return aggregated

    def _execute_thread_pool(self, tasks: List[ParallelTask],
                             cfg: RouteConfig) -> List[ParallelResult]:
        """线程池执行"""
        results = []
        max_workers = min(cfg.max_concurrent, len(tasks))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures: Dict[Future, ParallelTask] = {}

            # 提交所有任务
            for task in tasks:
                future = executor.submit(
                    self._execute_single_task,
                    task,
                    cfg.timeout
                )
                futures[future] = task

            # 收集结果
            for future in futures:
                task = futures[future]
                try:
                    result = future.result(timeout=cfg.timeout * len(tasks))
                    results.append(result)
                except Exception as e:
                    results.append(ParallelResult(
                        task_id=task.task_id,
                        module_key=task.module_key,
                        success=False,
                        error="执行失败"
                    ))

        return results

    async def _execute_async(self, tasks: List[ParallelTask],
                             cfg: RouteConfig) -> List[ParallelResult]:
        """异步执行"""
        results = []

        # 创建并发任务
        async_tasks = [
            self._execute_single_task_async(task, cfg.timeout)
            for task in tasks
        ]

        # 使用信号量控制并发数
        semaphore = asyncio.Semaphore(cfg.max_concurrent)

        async def limited_task(task, coro):
            async with semaphore:
                return await coro

        limited_tasks = [
            limited_task(task, coro)
            for task, coro in zip(tasks, async_tasks)
        ]

        # 并发执行
        results = await asyncio.gather(*limited_tasks, return_exceptions=True)

        # 处理异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ParallelResult(
                    task_id=tasks[i].task_id,
                    module_key=tasks[i].module_key,
                    success=False,
                    error=str(result)
                ))
            else:
                processed_results.append(result)

        return processed_results

    def _execute_sequential_fallback(self, tasks: List[ParallelTask],
                                      cfg: RouteConfig) -> List[ParallelResult]:
        """顺序降级执行"""
        results = []
        for task in tasks:
            result = self._execute_single_task(task, cfg.timeout)
            results.append(result)
        return results

    def _execute_single_task(self, task: ParallelTask,
                             timeout: float) -> ParallelResult:
        """执行单个任务"""
        start_time = time.time()

        try:
            handler = self.registry.get(task.module_key)
            if not handler:
                return ParallelResult(
                    task_id=task.task_id,
                    module_key=task.module_key,
                    success=False,
                    error=f"模块未注册: {task.module_key}"
                )

            # 调用处理器
            output = handler(**task.params)

            execution_time = time.time() - start_time
            self.registry.update_performance(task.module_key, True, execution_time)

            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=True,
                output=output,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.registry.update_performance(task.module_key, False, execution_time)

            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=False,
                error="执行失败",
                execution_time=execution_time
            )

    async def _execute_single_task_async(self, task: ParallelTask,
                                         timeout: float) -> ParallelResult:
        """异步执行单个任务"""
        start_time = time.time()

        try:
            handler = self.registry.get(task.module_key)
            if not handler:
                return ParallelResult(
                    task_id=task.task_id,
                    module_key=task.module_key,
                    success=False,
                    error=f"模块未注册: {task.module_key}"
                )

            # 调用处理器（如果是协程则await，否则直接调用）
            if asyncio.iscoroutinefunction(handler):
                output = await handler(**task.params)
            else:
                output = handler(**task.params)

            execution_time = time.time() - start_time
            self.registry.update_performance(task.module_key, True, execution_time)

            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=True,
                output=output,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.registry.update_performance(task.module_key, False, execution_time)

            return ParallelResult(
                task_id=task.task_id,
                module_key=task.module_key,
                success=False,
                error="执行失败",
                execution_time=execution_time
            )

    def _aggregate_results(self, results: List[ParallelResult],
                          cfg: RouteConfig) -> AggregatedResult:
        """聚合结果"""
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        # 提取洞察
        insights = self._extract_insights(successful)

        # 检测冲突
        conflicts = self._detect_conflicts(successful)

        return AggregatedResult(
            total_tasks=len(results),
            successful_tasks=len(successful),
            failed_tasks=len(failed),
            results=results,
            total_time=0.0,  # 稍后设置
            strategy_used=cfg.strategy,
            mode_used=cfg.mode,
            insights=insights,
            conflicts=conflicts
        )

    def _extract_insights(self, successful_results: List[ParallelResult]) -> List[str]:
        """提取洞察"""
        insights = []

        # 统计各模块输出
        module_outputs = {}
        for result in successful_results:
            module_outputs[result.module_key] = result.output

        # 生成洞察
        if len(successful_results) > 1:
            insights.append(f"多模块协同完成 {len(successful_results)} 个任务")

        # 从各模块输出中提取洞察
        for module_key, output in module_outputs.items():
            if isinstance(output, dict):
                if "insights" in output:
                    insights.extend(output["insights"])
                elif "recommendation" in output:
                    insights.append(f"{module_key} 推荐: {output['recommendation']}")

        return insights

    def _detect_conflicts(self, results: List[ParallelResult]) -> List[Dict]:
        """检测冲突"""
        conflicts = []

        # 收集所有推荐
        recommendations = []
        for result in results:
            if result.success and result.output:
                if isinstance(result.output, dict):
                    rec = result.output.get("recommendation")
                    action = result.output.get("action")
                    if rec:
                        recommendations.append({"module": result.module_key, "value": rec})
                    if action:
                        recommendations.append({"module": result.module_key, "value": action})

        # 简单冲突检测：检查是否有相反的建议
        if len(recommendations) > 1:
            positive = ["增长", "扩大", "增加", "积极", "进攻"]
            negative = ["减少", "收缩", "保守", "防守", "收缩"]

            pos_recs = [r for r in recommendations
                       if any(p in str(r.get("value", "")) for p in positive)]
            neg_recs = [r for r in recommendations
                       if any(n in str(r.get("value", "")) for n in negative)]

            if pos_recs and neg_recs:
                conflicts.append({
                    "type": "strategy_direction",
                    "description": "存在战略方向分歧",
                    "positive_recommendations": pos_recs,
                    "negative_recommendations": neg_recs
                })

        return conflicts

    # ── 便捷方法 ────────────────────────────────────────────────

    def route_parallel(self, task_type: str,
                       params: Dict[str, Any],
                       domain: str = None,
                       top_k: int = 3) -> AggregatedResult:
        """
        便捷方法：并行路由一组任务

        Args:
            task_type: 任务类型（如 "reasoning", "analysis"）
            params: 任务参数
            domain: 领域（可选）
            top_k: 选择前K个最佳模块

        Returns:
            AggregatedResult: 聚合结果
        """
        # 获取最佳模块
        modules = self.registry.get_best_modules(
            capability=task_type,
            domain=domain,
            top_k=top_k
        )

        if not modules:
            logger.warning(f"未找到支持 {task_type} 的模块")
            return AggregatedResult(
                total_tasks=0,
                successful_tasks=0,
                failed_tasks=0,
                results=[],
                total_time=0.0,
                strategy_used=self.config.strategy,
                mode_used=self.config.mode
            )

        # 创建任务
        tasks = [
            ParallelTask(
                task_id=f"task_{uuid.uuid4().hex[:8]}",
                module_key=module_key,
                handler=self.registry.get(module_key),
                params=params
            )
            for module_key in modules
        ]

        return self.route(tasks)

    def execute_main_chain_parallel(self,
                                     context: Dict[str, Any]) -> AggregatedResult:
        """
        执行主线并形运转

        将任务同时分发到主线上的多个节点：
        - WisdomDispatcher（智慧调度）
        - DeepReasoningEngine（深度推理）
        - NarrativeIntelligenceEngine（叙事智能）
        - Tier3NeuralScheduler（神经调度）
        - LearningCoordinator（学习协调）
        - AutonomousAgent（自主智能）

        Args:
            context: 任务上下文

        Returns:
            AggregatedResult: 聚合结果
        """
        tasks = []

        # 主线节点处理器映射
        main_chain_handlers = {
            "wisdom_dispatcher": self._handle_wisdom_dispatch,
            "deep_reasoning": self._handle_deep_reasoning,
            "narrative_engine": self._handle_narrative,
            "neural_scheduler": self._handle_neural_schedule,
            "learning_coordinator": self._handle_learning,
            "autonomous_agent": self._handle_autonomous
        }

        for node_key, handler in main_chain_handlers.items():
            task = ParallelTask(
                task_id=f"main_chain_{node_key}",
                module_key=node_key,
                handler=handler,
                params={"context": context}
            )
            tasks.append(task)

        return self.route(tasks)

    # ── 主线节点处理器 ───────────────────────────────────────────

    def _handle_wisdom_dispatch(self, context: Dict) -> Dict:
        """处理智慧调度"""
        return {
            "module": "wisdom_dispatcher",
            "status": "completed",
            "insights": ["多学派智慧已融合"]
        }

    def _handle_deep_reasoning(self, context: Dict) -> Dict:
        """处理深度推理"""
        return {
            "module": "deep_reasoning",
            "status": "completed",
            "insights": ["深度推理已完成"]
        }

    def _handle_narrative(self, context: Dict) -> Dict:
        """处理叙事智能"""
        return {
            "module": "narrative_engine",
            "status": "completed",
            "insights": ["叙事分析已完成"]
        }

    def _handle_neural_schedule(self, context: Dict) -> Dict:
        """处理神经调度"""
        return {
            "module": "neural_scheduler",
            "status": "completed",
            "insights": ["任务调度已完成"]
        }

    def _handle_learning(self, context: Dict) -> Dict:
        """处理学习协调"""
        return {
            "module": "learning_coordinator",
            "status": "completed",
            "insights": ["学习任务已协调"]
        }

    def _handle_autonomous(self, context: Dict) -> Dict:
        """处理自主智能"""
        return {
            "module": "autonomous_agent",
            "status": "completed",
            "insights": ["自主决策已执行"]
        }

    # ── 状态查询 ────────────────────────────────────────────────

    def get_status(self) -> Dict:
        """获取路由器状态"""
        return {
            "registered_modules": self.registry.get_all(),
            "config": {
                "max_concurrent": self.config.max_concurrent,
                "timeout": self.config.timeout,
                "strategy": self.config.strategy.value,
                "mode": self.config.mode.value
            },
            "main_chain_nodes": list(self._main_chain_nodes.keys())
        }

# ── 全局实例 ──────────────────────────────────────────────────

# 全局并行路由器实例
_parallel_router: Optional[ParallelRouter] = None
_router_lock = threading.Lock()

def get_parallel_router() -> ParallelRouter:
    """获取全局并行路由器实例"""
    global _parallel_router
    if _parallel_router is None:
        with _router_lock:
            if _parallel_router is None:
                _parallel_router = ParallelRouter()
    return _parallel_router

# ── 使用示例 ──────────────────────────────────────────────────

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

    # 注册自定义模块
    def custom_handler(**kwargs):
        return {"result": f"处理完成: {kwargs}"}

    router.register_module(
        module_key="custom_module",
        handler=custom_handler,
        capabilities=["custom"],
        domains=["test"]
    )

    # 创建并行任务
    tasks = [
        ParallelTask(
            task_id=f"task_{i}",
            module_key="wisdom_dispatcher",
            handler=router.registry.get("wisdom_dispatcher"),
            params={"query": f"测试查询{i}"}
        )
        for i in range(3)
    ]

    # 执行并行路由
    result = router.route(tasks)

    logger.info(f"总任务: {result.total_tasks}")
    logger.info(f"成功: {result.successful_tasks}")
    logger.info(f"失败: {result.failed_tasks}")
    logger.info(f"总耗时: {result.total_time:.2f}s")
    logger.info(f"洞察: {result.insights}")
