"""
__all__ = [
    'execute',
    'get_history',
    'get_main_chain_scheduler',
    'get_status',
]

主线统一调度器 v1.0
Main Chain Unified Scheduler

功能：
1. 统一调度三种运行模式：串联、并形、交叉
2. 智能选择运行模式
3. 协调 ParallelRouter 和 CrossWeaver
4. 提供统一的主线执行接口

运行模式：
- 串联运转（Serial）：WisdomDispatcher -> GlobalScheduler -> ThinkingEngine
- 并形运转（Parallel）：ParallelRouter 多路并发
- 交叉运转（Cross）：CrossWeaver 网状交叉

适用场景：
- 所有主线任务执行
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
import threading
import time
import uuid

logger = logging.getLogger(__name__)

class RunMode(Enum):
    """运行模式"""
    SERIAL = "serial"           # 串联运转
    PARALLEL = "parallel"       # 并形运转
    CROSS = "cross"            # 交叉运转
    AUTO = "auto"              # 自动选择

@dataclass
class ChainContext:
    """主线上下文"""
    context_id: str
    user_input: str
    task_type: str
    wisdom_mode: RunMode = RunMode.AUTO
    depth: str = "normal"
    trace: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ChainResult:
    """主线结果"""
    result_id: str
    success: bool
    mode: RunMode
    output: Any
    serial_output: Any = None
    parallel_output: Any = None
    cross_output: Any = None
    execution_time: float = 0.0
    nodes_executed: List[str] = field(default_factory=list)
    trace: List[Dict] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

class MainChainScheduler:
    """
    主线统一调度器

    功能：
    1. 统一调度三种运行模式
    2. 智能选择最优运行模式
    3. 协调 ParallelRouter 和 CrossWeaver
    4. 提供执行追踪和结果聚合

    主线定位：
    - 所有主线任务的统一入口
    - 协调串联/并形/交叉三种运转
    """

    def __init__(self):
        self._router = None
        self._weaver = None
        self._lock = threading.Lock()
        self._initialized = False

        # 运行历史
        self._history: List[ChainResult] = []

        logger.info("MainChainScheduler 初始化完成")

    def _ensure_init(self):
        """确保依赖组件已初始化"""
        if self._initialized:
            return

        with self._lock:
            if self._initialized:
                return

            try:
                from .parallel_router import get_parallel_router
                from .cross_weaver import get_cross_weaver

                self._router = get_parallel_router()
                self._weaver = get_cross_weaver()

                self._initialized = True
                logger.info("主链依赖组件初始化完成")

            except ImportError as e:
                logger.warning(f"主链组件导入失败: {e}，将使用降级模式")

    def execute(self, context: ChainContext) -> ChainResult:
        """
        执行主线任务

        Args:
            context: 主线上下文

        Returns:
            ChainResult: 主线结果
        """
        start_time = time.time()
        result_id = f"chain_{uuid.uuid4().hex[:8]}"

        self._ensure_init()

        logger.info(f"主线执行开始: {result_id}, 模式: {context.wisdom_mode.value}")

        # 确定运行模式
        mode = self._determine_mode(context)

        result: ChainResult

        # 根据模式执行
        if mode == RunMode.SERIAL:
            result = self._execute_serial(context)
        elif mode == RunMode.PARALLEL:
            result = self._execute_parallel(context)
        elif mode == RunMode.CROSS:
            result = self._execute_cross(context)
        else:
            # 组合模式：先串联，再并形，最后交叉
            result = self._execute_combined(context)

        result.result_id = result_id
        result.mode = mode
        result.execution_time = time.time() - start_time

        # 记录历史
        self._history.append(result)

        logger.info(f"主线执行完成: {result_id}, 耗时: {result.execution_time:.2f}s, 模式: {mode.value}")

        return result

    def _determine_mode(self, context: ChainContext) -> RunMode:
        """确定运行模式"""
        if context.wisdom_mode != RunMode.AUTO:
            return context.wisdom_mode

        # 基于任务类型自动选择
        task_type = context.task_type.lower()
        user_input = context.user_input.lower()

        # 简单策略分析
        if any(kw in user_input for kw in ["并行", "同时", "多个", "并发", "一起"]):
            return RunMode.PARALLEL

        if any(kw in user_input for kw in ["交叉", "反馈", "反思", "闭环", "进化"]):
            return RunMode.CROSS

        if any(kw in user_input for kw in ["策略", "分析", "决策", "方案"]):
            return RunMode.SERIAL

        # 默认串联
        return RunMode.SERIAL

    def _execute_serial(self, context: ChainContext) -> ChainResult:
        """执行串联运转"""
        trace = []
        nodes_executed = []

        # 步骤1: WisdomDispatcher
        wisdom_output = self._call_wisdom_dispatcher(context.user_input)
        trace.append({
            "node": "wisdom_dispatcher",
            "output": str(wisdom_output)[:100],
            "timestamp": datetime.now().isoformat()
        })
        nodes_executed.append("wisdom_dispatcher")

        # 步骤2: GlobalScheduler
        scheduler_output = self._call_global_scheduler(wisdom_output, context)
        trace.append({
            "node": "global_scheduler",
            "output": str(scheduler_output)[:100],
            "timestamp": datetime.now().isoformat()
        })
        nodes_executed.append("global_scheduler")

        # 步骤3: ThinkingEngine
        thinking_output = self._call_thinking_engine(scheduler_output, context)
        trace.append({
            "node": "thinking_engine",
            "output": str(thinking_output)[:100],
            "timestamp": datetime.now().isoformat()
        })
        nodes_executed.append("thinking_engine")

        return ChainResult(
            result_id="",
            success=True,
            mode=RunMode.SERIAL,
            output=thinking_output,
            serial_output={
                "wisdom": wisdom_output,
                "scheduler": scheduler_output,
                "thinking": thinking_output
            },
            nodes_executed=nodes_executed,
            trace=trace,
            insights=["串联运转完成"]
        )

    def _execute_parallel(self, context: ChainContext) -> ChainResult:
        """执行并形运转"""
        self._ensure_init()

        # 使用 ParallelRouter 执行
        if self._router:
            router_result = self._router.execute_main_chain_parallel({
                "user_input": context.user_input,
                "task_type": context.task_type
            })

            nodes_executed = [r.module_key for r in router_result.results if r.success]

            return ChainResult(
                result_id="",
                success=router_result.successful_tasks > 0,
                mode=RunMode.PARALLEL,
                output=router_result.to_dict() if hasattr(router_result, 'to_dict') else router_result,
                parallel_output=router_result,
                nodes_executed=nodes_executed,
                insights=router_result.insights if hasattr(router_result, 'insights') else []
            )

        # 降级：使用占位实现
        return self._execute_serial(context)

    def _execute_cross(self, context: ChainContext) -> ChainResult:
        """执行交叉运转"""
        self._ensure_init()

        # 先执行串联获取初始输出
        serial_result = self._execute_serial(context)

        # 使用 CrossWeaver 执行交叉
        if self._weaver:
            cross_result = self._weaver.execute_main_chain_cross(
                serial_result.output,
                {"hints": [context.user_input]}
            )

            return ChainResult(
                result_id="",
                success=True,
                mode=RunMode.CROSS,
                output=cross_result.final_output,
                serial_output=serial_result.output,
                cross_output=cross_result,
                nodes_executed=serial_result.nodes_executed + cross_result.evolved_modules,
                trace=serial_result.trace,
                insights=cross_result.insights
            )

        return serial_result

    def _execute_combined(self, context: ChainContext) -> ChainResult:
        """执行组合运转（串联 -> 并形 -> 交叉）"""
        # 阶段1: 串联
        serial_result = self._execute_serial(context)

        # 阶段2: 并形
        parallel_result = self._execute_parallel(context)

        # 阶段3: 交叉
        cross_result = self._execute_cross(context)

        return ChainResult(
            result_id="",
            success=True,
            mode=RunMode.AUTO,
            output=cross_result.output,
            serial_output=serial_result.serial_output,
            parallel_output=parallel_result.parallel_output,
            cross_output=cross_result.cross_output,
            nodes_executed=list(set(
                serial_result.nodes_executed +
                parallel_result.nodes_executed +
                cross_result.nodes_executed
            )),
            trace=serial_result.trace,
            insights=serial_result.insights + parallel_result.insights + cross_result.insights
        )

    # ── 节点调用 ───────────────────────────────────────────

    def _call_wisdom_dispatcher(self, query: str) -> Dict:
        """调用智慧调度器"""
        try:
            from ..intelligence.wisdom_dispatcher import WisdomDispatcher
            dispatcher = WisdomDispatcher()
            result = dispatcher.dispatch(query)
            return result
        except Exception as e:
            logger.warning(f"WisdomDispatcher 调用失败: {e}")
            return {"error": "智慧调度降级", "fallback": True}

    def _call_global_scheduler(self, wisdom_output: Any, context: ChainContext) -> Dict:
        """调用全局调度器"""
        try:
            from ..intelligence.global_wisdom_scheduler import GlobalWisdomScheduler
            scheduler = GlobalWisdomScheduler()
            result = scheduler.schedule({
                "query": context.user_input,
                "wisdom_output": wisdom_output
            })
            return result
        except Exception as e:
            logger.warning(f"GlobalScheduler 调用失败: {e}")
            return {"error": "全局调度降级", "fallback": True}

    def _call_thinking_engine(self, scheduler_output: Any, context: ChainContext) -> Dict:
        """调用思维融合引擎"""
        try:
            from ..intelligence.thinking_method_engine import ThinkingMethodFusionEngine
            engine = ThinkingMethodFusionEngine()
            result = engine.fuse({
                "scheduler_output": scheduler_output,
                "context": context.metadata
            })
            return result
        except Exception as e:
            logger.warning(f"ThinkingEngine 调用失败: {e}")
            return {"error": "思维引擎降级", "fallback": True}

    # ── 状态查询 ───────────────────────────────────────────

    def get_status(self) -> Dict:
        """获取调度器状态"""
        self._ensure_init()

        return {
            "initialized": self._initialized,
            "history_count": len(self._history),
            "router_available": self._router is not None,
            "weaver_available": self._weaver is not None,
            "recent_results": len(self._history[-10:]) if self._history else 0
        }

    def get_history(self, limit: int = 20) -> List[Dict]:
        """获取执行历史"""
        results = self._history[-limit:]
        return [
            {
                "result_id": r.result_id,
                "success": r.success,
                "mode": r.mode.value,
                "execution_time": r.execution_time,
                "nodes_count": len(r.nodes_executed)
            }
            for r in results
        ]

# ── 全局实例 ─────────────────────────────────────────────────

_scheduler: Optional[MainChainScheduler] = None
_scheduler_lock = threading.Lock()

def get_main_chain_scheduler() -> MainChainScheduler:
    """获取全局主线调度器实例"""
    global _scheduler
    if _scheduler is None:
        with _scheduler_lock:
            if _scheduler is None:
                _scheduler = MainChainScheduler()
    return _scheduler

# ── 使用示例 ─────────────────────────────────────────────────

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

    # 创建上下文
    context = ChainContext(
        context_id="test_001",
        user_input="分析公司增长策略",
        task_type="growth_strategy",
        wisdom_mode=RunMode.AUTO
    )

    # 执行主线
    result = scheduler.execute(context)

    logger.info(f"结果ID: {result.result_id}")
    logger.info(f"成功: {result.success}")
    logger.info(f"模式: {result.mode.value}")
    logger.info(f"耗时: {result.execution_time:.2f}s")
    logger.info(f"执行节点: {result.nodes_executed}")
    logger.info(f"洞察: {result.insights}")
