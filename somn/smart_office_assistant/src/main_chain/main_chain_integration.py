"""
__all__ = [
    'build_chain_context',
    'cross_weaver',
    'determine_mode',
    'execute',
    'execute_cross',
    'execute_parallel',
    'execute_serial',
    'get_main_chain_integration',
    'get_monitor_report',
    'get_status',
    'parallel_router',
    'scheduler',
]

主线组件集成模块
将 ParallelRouter、CrossWeaver、MainChainScheduler 接入 SomnCore
支持串联/并形/交叉三种运行模式

配置支持：
- 默认使用硬编码配置
- 如需使用外部配置，在初始化时传入 config_loader
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

# 尝试导入配置加载器
try:
    from .config_loader import get_main_chain_config, MainChainConfig
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    MainChainConfig = None

class ChainRunMode(Enum):
    """主线运行模式"""
    SERIAL = "serial"       # 串联：顺序执行
    PARALLEL = "parallel"   # 并形：多路并发
    CROSS = "cross"          # 交叉：网状反馈
    AUTO = "auto"           # 自动：根据任务特征选择

@dataclass
class ChainContext:
    """主线执行上下文"""
    context_id: str
    task_id: str
    task_type: str
    user_input: str
    wisdom_mode: ChainRunMode = ChainRunMode.AUTO
    complexity: float = 0.5
    multi_dimensional: bool = False
    reflection_needed: bool = False
    parallel_nodes: List[str] = field(default_factory=list)
    cross_signals: List[Dict] = field(default_factory=list)
    execution_trace: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ChainExecutionResult:
    """主线执行结果"""
    success: bool
    mode: ChainRunMode
    record_id: str = None  # 监控记录ID
    strategy: Dict[str, Any] = None
    execution: Dict[str, Any] = None
    evaluation: Dict[str, Any] = None
    cross_results: Dict[str, Any] = None
    parallel_results: Dict[str, Any] = None
    execution_trace: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: str = None

class MainChainIntegration:
    """
    主线集成器
    负责将 ParallelRouter、CrossWeaver、MainChainScheduler 接入 SomnCore
    提供统一的主线执行入口

    v1.0 新增：
    - ParallelExecutionEngine（进度追踪/结果回收/汇总优化）
    """

    def __init__(self):
        self._parallel_router = None
        self._cross_weaver = None
        self._scheduler = None
        self._initialized = False
        self._default_mode = ChainRunMode.AUTO
        # 监控器
        self._monitor = None
        # v1.0: 并行执行引擎（进度追踪/结果回收/汇总优化）
        self._execution_engine = None

    @property
    def parallel_router(self):
        """延迟加载 ParallelRouter"""
        if self._parallel_router is None:
            try:
                from ..main_chain.parallel_router import get_parallel_router
                self._parallel_router = get_parallel_router()
                logger.info("[主线集成] ParallelRouter 加载成功")
            except Exception as e:
                logger.warning(f"[主线集成] ParallelRouter 加载失败: {e}")
        return self._parallel_router

    @property
    def cross_weaver(self):
        """延迟加载 CrossWeaver"""
        if self._cross_weaver is None:
            try:
                from ..main_chain.cross_weaver import get_cross_weaver
                self._cross_weaver = get_cross_weaver()
                logger.info("[主线集成] CrossWeaver 加载成功")
            except Exception as e:
                logger.warning(f"[主线集成] CrossWeaver 加载失败: {e}")
        return self._cross_weaver

    @property
    def scheduler(self):
        """延迟加载 MainChainScheduler"""
        if self._scheduler is None:
            try:
                from ..main_chain.main_chain_scheduler import MainChainScheduler, RunMode
                self._scheduler = MainChainScheduler()
                logger.info("[主线集成] MainChainScheduler 加载成功")
            except Exception as e:
                logger.warning(f"[主线集成] MainChainScheduler 加载失败: {e}")
        return self._scheduler

    @property
    def execution_engine(self):
        """延迟加载 ParallelExecutionEngine（v1.0 进度追踪/结果回收/汇总优化）"""
        if self._execution_engine is None:
            try:
                from ..main_chain.parallel_execution_engine import get_parallel_execution_engine
                self._execution_engine = get_parallel_execution_engine(
                    progress_callback=self._on_progress_update,
                    optimize_callback=self._on_optimization_needed
                )
                logger.info("[主线集成] ParallelExecutionEngine v1.0 加载成功")
            except Exception as e:
                logger.warning(f"[主线集成] ParallelExecutionEngine 加载失败: {e}")
        return self._execution_engine

    def determine_mode(self, requirement: Dict[str, Any]) -> ChainRunMode:
        """
        根据需求特征确定运行模式

        决策规则:
        - 复杂度 >= 0.7 → PARALLEL (多路并发)
        - 反射/反馈关键词 → CROSS (交叉反馈)
        - 复杂度 >= 0.5 → SERIAL (标准串联)
        - 默认 → AUTO
        """
        routing = requirement.get("routing_decision", {})
        complexity = routing.get("complexity", 0.5)
        route = routing.get("route", "full_workflow")

        # 关键词检测
        description = requirement.get("raw_description", "").lower()
        wisdom_analysis = requirement.get("wisdom_analysis", {})

        reflection_keywords = ["反思", "复盘", "反馈", "回顾", "改进", "优化", "评估", "分析"]
        parallel_keywords = ["多维度", "多方面", "同时", "并行", "并发", "全面", "综合"]
        cross_keywords = ["影响", "关联", "反馈", "循环", "迭代", "持续"]

        has_reflection = any(kw in description for kw in reflection_keywords)
        has_parallel = any(kw in description for kw in parallel_keywords)
        has_cross = any(kw in description for kw in cross_keywords)

        # 路由决策影响
        if route in ["orchestrator"] and complexity < 0.3:
            return ChainRunMode.SERIAL  # 快手菜模式用串联

        # 复杂度决策
        if complexity >= 0.7 or has_parallel:
            return ChainRunMode.PARALLEL

        if has_reflection or has_cross:
            return ChainRunMode.CROSS

        if complexity >= 0.5:
            return ChainRunMode.SERIAL

        return ChainRunMode.AUTO

    def build_chain_context(
        self,
        requirement: Dict[str, Any],
        task_type: str = None,
        user_input: str = None
    ) -> ChainContext:
        """从需求构建主线上下文"""
        routing = requirement.get("routing_decision", {})
        complexity = routing.get("complexity", 0.5)
        mode = self.determine_mode(requirement)

        # 提取多维度信息
        multi_dimensional = complexity >= 0.6
        reflection_needed = complexity >= 0.4

        return ChainContext(
            context_id=requirement.get("task_id", "unknown"),
            task_id=requirement.get("task_id", "unknown"),
            task_type=task_type or requirement.get("task_type", "general"),
            user_input=user_input or requirement.get("raw_description", ""),
            wisdom_mode=mode,
            complexity=complexity,
            multi_dimensional=multi_dimensional,
            reflection_needed=reflection_needed,
            metadata={
                "routing": routing,
                "industry": requirement.get("industry"),
                "stage": requirement.get("stage")
            }
        )

    def execute_parallel(
        self,
        context: ChainContext,
        initial_output: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """执行并形模式（v1.0 集成进度追踪/结果回收/汇总优化）"""
        if self.parallel_router is None:
            logger.warning("[主线集成] ParallelRouter 不可用，回退到串联模式")
            return {"mode": "serial_fallback", "reason": "router_unavailable"}

        try:
            # v1.0: 优先使用 ParallelExecutionEngine
            if self.execution_engine is not None:
                return self._execute_with_engine(context, initial_output)

            # 降级：使用原有的 parallel_router
            return self._execute_with_router(context, initial_output)

        except Exception as e:
            logger.error(f"[主线集成] 并形执行失败: {e}")
            return {"mode": "parallel", "success": False, "error": "并行执行失败"}

    def _execute_with_engine(self,
                            context: ChainContext,
                            initial_output: Dict[str, Any]) -> Dict[str, Any]:
        """使用 ParallelExecutionEngine 执行（v1.0）"""
        from ..main_chain.parallel_execution_engine import ParallelTask, RouteConfig, ParallelMode

        # 构建任务
        tasks = []
        main_chain_nodes = [
            "wisdom_dispatcher", "deep_reasoning", "narrative_engine",
            "neural_scheduler", "learning_coordinator", "autonomous_agent"
        ]

        handler_map = {
            "wisdom_dispatcher": self.parallel_router._handle_wisdom_dispatch,
            "deep_reasoning": self.parallel_router._handle_deep_reasoning,
            "narrative_engine": self.parallel_router._handle_narrative,
            "neural_scheduler": self.parallel_router._handle_neural_schedule,
            "learning_coordinator": self.parallel_router._handle_learning,
            "autonomous_agent": self.parallel_router._handle_autonomous,
        }

        parallel_context = {
            "task_id": context.task_id,
            "task_type": context.task_type,
            "complexity": context.complexity,
            "initial_output": initial_output
        }

        for node_key in main_chain_nodes:
            task = ParallelTask(
                task_id=f"main_chain_{node_key}_{context.task_id}",
                module_key=node_key,
                handler=handler_map.get(node_key, lambda **kw: {"module": node_key}),
                params={"context": parallel_context}
            )
            tasks.append(task)

        # 使用引擎执行（带进度追踪/结果回收/汇总优化）
        result = self.execution_engine.execute(tasks, track_progress=True, collect_results=True)

        # 将 AggregatedResult 转换为字典
        result_dict = {
            "total_tasks": result.total_tasks,
            "successful_tasks": result.successful_tasks,
            "failed_tasks": result.failed_tasks,
            "total_nodes": result.successful_tasks,
            "total_time": result.total_time,
            "insights": result.insights,
            "conflicts": result.conflicts,
            # v1.0 新增：进度与结果回收信息
            "progress": self.execution_engine.get_progress().get_summary() if self.execution_engine.get_progress() else None,
            "collector_stats": self.execution_engine.collector.get_stats(),
        }

        logger.info(
            f"[主线集成] 并形执行完成(v1.0) "
            f"成功:{result.successful_tasks}/{result.total_tasks} "
            f"耗时:{result.total_time:.2f}s "
            f"洞察:{len(result.insights)}条"
        )

        return {
            "mode": "parallel_v2",
            "success": result.successful_tasks > 0,
            "results": result_dict
        }

    def _execute_with_router(self,
                            context: ChainContext,
                            initial_output: Dict[str, Any]) -> Dict[str, Any]:
        """使用原有 ParallelRouter 执行（降级路径）"""
        parallel_context = {
            "task_id": context.task_id,
            "task_type": context.task_type,
            "complexity": context.complexity,
            "multi_dimensional": context.multi_dimensional,
            "initial_output": initial_output
        }

        # 调用并行路由器
        result = self.parallel_router.execute_main_chain_parallel(parallel_context)

        # 将 AggregatedResult 转换为字典
        if hasattr(result, 'successful_tasks'):
            result_dict = {
                "total_tasks": result.total_tasks,
                "successful_tasks": result.successful_tasks,
                "failed_tasks": result.failed_tasks,
                "total_nodes": result.successful_tasks,
                "insights": result.insights
            }
        else:
            result_dict = {"total_tasks": 0, "successful_tasks": 0, "failed_tasks": 0, "total_nodes": 0, "insights": []}

        logger.info(f"[主线集成] 并形执行完成，{result_dict.get('total_nodes', 0)} 个节点")
        return {
            "mode": "parallel",
            "success": True,
            "results": result_dict
        }

    def _on_progress_update(self, progress):
        """进度更新回调"""
        logger.debug(
            f"[进度] {progress.completed_tasks}/{progress.total_tasks} "
            f"({progress.overall_progress*100:.0f}%) "
            f"剩余:{progress.estimated_remaining_sec:.0f}s"
        )

    def _on_optimization_needed(self, results, insights):
        """优化建议回调"""
        if insights:
            logger.info(f"[优化] 生成 {len(insights)} 条优化洞察")
            for insight in insights:
                logger.debug(f"  - {insight}")

    def execute_cross(
        self,
        context: ChainContext,
        initial_output: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """执行交叉模式"""
        if self.cross_weaver is None:
            logger.warning("[主线集成] CrossWeaver 不可用，跳过交叉执行")
            return {"mode": "cross_skipped", "reason": "weaver_unavailable"}

        try:
            # 执行交叉织网
            result = self.cross_weaver.execute_main_chain_cross(
                initial_output or {},
                {
                    "task_id": context.task_id,
                    "task_type": context.task_type,
                    "reflection_needed": context.reflection_needed
                }
            )

            # 将 CrossResult 转换为字典
            if hasattr(result, 'total_signals'):
                result_dict = {
                    "total_signals": result.total_signals,
                    "total_modules": result.total_modules,
                    "modules_evolved": result.modules_evolved,
                    "feedback_signals": []  # CrossResult 暂无此字段
                }
            else:
                result_dict = {"total_signals": 0, "total_modules": 0, "modules_evolved": 0, "feedback_signals": []}

            logger.info(f"[主线集成] 交叉执行完成，{result_dict.get('total_signals', 0)} 个信号")
            return {
                "mode": "cross",
                "success": True,
                "results": result_dict
            }
        except Exception as e:
            logger.error(f"[主线集成] 交叉执行失败: {e}")
            return {"mode": "cross", "success": False, "error": "交叉执行失败"}

    def execute_serial(
        self,
        context: ChainContext
    ) -> Dict[str, Any]:
        """执行串联模式（标准主线）"""
        return {
            "mode": "serial",
            "success": True,
            "nodes_executed": ["wisdom_dispatcher", "global_scheduler", "thinking_engine"]
        }

    def execute(
        self,
        requirement: Dict[str, Any],
        initial_output: Dict[str, Any] = None
    ) -> ChainExecutionResult:
        """
        统一执行入口
        根据上下文自动选择运行模式
        """
        # 构建上下文
        context = self.build_chain_context(requirement)

        logger.info(f"[主线集成] 执行模式: {context.wisdom_mode.value}, "
                    f"复杂度: {context.complexity}, "
                    f"任务ID: {context.task_id}")

        # 初始化监控器
        if self._monitor is None:
            try:
                from .main_chain_monitor import get_main_chain_monitor
                self._monitor = get_main_chain_monitor()
            except Exception as e:
                logger.debug(f"执行策略失败: {e}")

        # 开始执行追踪
        record_id = None
        if self._monitor:
            nodes = self._get_nodes_for_mode(context.wisdom_mode)
            record_id = self._monitor.start_execution(
                context.task_id,
                context.wisdom_mode.value,
                nodes
            )

        # 根据模式执行
        if context.wisdom_mode == ChainRunMode.PARALLEL:
            result = self.execute_parallel(context, initial_output)
        elif context.wisdom_mode == ChainRunMode.CROSS:
            result = self.execute_cross(context, initial_output)
        else:  # SERIAL or AUTO
            result = self.execute_serial(context)

        # 结束执行追踪
        if self._monitor and record_id:
            signals = 0
            modules_evolved = 0
            if context.wisdom_mode == ChainRunMode.PARALLEL:
                signals = result.get("results", {}).get("total_tasks", 0)
            elif context.wisdom_mode == ChainRunMode.CROSS:
                signals = result.get("results", {}).get("total_signals", 0)
                modules_evolved = result.get("results", {}).get("modules_evolved", 0)

            self._monitor.end_execution(
                record_id,
                state="success" if result.get("success") else "failed",
                signals=signals,
                modules_evolved=modules_evolved,
                error=result.get("error")
            )

        # 记录执行追踪
        context.execution_trace.append({
            "timestamp": datetime.now().isoformat(),
            "mode": context.wisdom_mode.value,
            "result": result
        })

        return ChainExecutionResult(
            success=result.get("success", True),
            mode=context.wisdom_mode,
            record_id=record_id,
            parallel_results=result if context.wisdom_mode == ChainRunMode.PARALLEL else None,
            cross_results=result if context.wisdom_mode == ChainRunMode.CROSS else None,
            execution_trace=context.execution_trace,
            metadata={
                "complexity": context.complexity,
                "task_type": context.task_type,
                "determination_reason": self._get_mode_reason(context)
            }
        )

    def _get_nodes_for_mode(self, mode: ChainRunMode) -> List[str]:
        """获取模式对应的执行节点"""
        if mode == ChainRunMode.PARALLEL:
            return ["wisdom_dispatcher", "deep_reasoning", "narrative_engine",
                    "neural_scheduler", "learning_coordinator", "autonomous_agent"]
        elif mode == ChainRunMode.CROSS:
            return ["neural_memory", "reinforcement_trigger", "roi_tracker", "feedback_loop"]
        else:
            return ["wisdom_dispatcher", "global_scheduler", "thinking_engine"]

    def _get_mode_reason(self, context: ChainContext) -> str:
        """获取模式决策原因"""
        reasons = []
        if context.complexity >= 0.7:
            reasons.append(f"复杂度{context.complexity}>=0.7")
        if context.multi_dimensional:
            reasons.append("多维度任务")
        if context.reflection_needed:
            reasons.append("需要反思")
        return "; ".join(reasons) or "默认决策"

    def get_status(self) -> Dict[str, Any]:
        """获取主线集成器状态"""
        status = {
            "initialized": self._initialized,
            "parallel_router_available": self.parallel_router is not None,
            "cross_weaver_available": self.cross_weaver is not None,
            "scheduler_available": self.scheduler is not None,
            "default_mode": self._default_mode.value,
            # v1.0: 执行引擎
            "execution_engine_v2": self.execution_engine is not None
        }

        # 添加监控器状态
        if self._monitor:
            health = self._monitor.get_chain_health()
            summary = self._monitor.get_execution_summary()
            status["monitor"] = {
                "health": health,
                "total_executions": summary["total_executions"],
                "success_rate": summary["success_rate"]
            }

        # v1.0: 执行引擎状态
        if self.execution_engine:
            engine_summary = self.execution_engine.get_execution_summary()
            status["execution_engine"] = engine_summary

        return status

    def get_monitor_report(self) -> str:
        """获取监控报告"""
        if self._monitor is None:
            return "监控器未启用"
        return self._monitor.generate_report()

# 全局单例
_main_chain_integration: Optional[MainChainIntegration] = None

def get_main_chain_integration() -> MainChainIntegration:
    """获取主线集成器单例"""
    global _main_chain_integration
    if _main_chain_integration is None:
        _main_chain_integration = MainChainIntegration()
    return _main_chain_integration
