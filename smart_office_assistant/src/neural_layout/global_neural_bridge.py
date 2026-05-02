"""
全局神经桥梁 v3.0

将神经网络布局与 Somn 系统的真实模块打通，实现全链路串联。

v3.0 变更：
- 绑定真实 SomnCore 模块（不再走模拟降级）
- 通过 NetworkLayoutManager.register_function_handler() 注入真实处理器
- 6 个桥接全部对接真实模块方法
- 提供 process_through_network() 完整链路处理
- 提供 get_neural_status() 状态查询
"""

__all__ = [
    'GlobalNeuralBridge',
    'get_global_neural_bridge',
    'bind_somn_core',
    'get_bound_modules',
]

from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
import threading
import logging
import time

logger = logging.getLogger(__name__)


class GlobalNeuralBridge:
    """
    全局神经桥梁 v3.0 — 真实模块绑定

    连接神经网络布局与 Somn 系统的各个模块：
    1. AgentCore → SomnCore.analyze_requirement()
    2. SomnCore → SomnCore.get_capabilities()
    3. WisdomDispatcher → SomnCore.super_wisdom.analyze()
    4. NeuralMemory → SomnCore._query_memory_context()
    5. LearningCoordinator → SomnCore.learning_coordinator
    6. AutonomousAgent → SomnCore.autonomous_agent
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> 'GlobalNeuralBridge':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        # 延迟导入避免循环
        self._layout_manager = None
        self._somn_core = None
        self._bridge_handlers: Dict[str, Callable] = {}
        self._initialized = False
        self._setup_lock = threading.Lock()
        self._stats = {
            "total_queries": 0,
            "bridge_calls": {},
            "errors": 0,
            "avg_latency_ms": 0.0,
        }

    @property
    def layout_manager(self):
        """延迟加载 NetworkLayoutManager"""
        if self._layout_manager is None:
            from .network_layout_manager import NetworkLayoutManager
            self._layout_manager = NetworkLayoutManager()
        return self._layout_manager

    def setup_global_bridge(self, somn_core=None) -> bool:
        """
        设置全局桥梁 — 绑定真实模块到神经网络

        Args:
            somn_core: SomnCore 实例，如为 None 则延迟绑定

        Returns:
            bool: 设置是否成功
        """
        with self._setup_lock:
            if somn_core is not None:
                self._somn_core = somn_core

            # 1. 初始化神经网络布局
            lm = self.layout_manager
            if not lm.initialized:
                if not lm.initialize_global_layout():
                    logger.error("[GlobalNeuralBridge] 神经网络布局初始化失败")
                    return False

            # 2. 注册真实功能处理器
            self._register_agent_core_handler()
            self._register_somn_core_handler()
            self._register_wisdom_handler()
            self._register_memory_handler()
            self._register_learning_handler()
            self._register_autonomy_handler()

            self._initialized = True
            logger.info(
                f"[GlobalNeuralBridge] v3.0 就绪: "
                f"{len(self._bridge_handlers)} 个真实处理器已绑定, "
                f"somn_core={'已绑定' if self._somn_core else '延迟'}"
            )
            return True

    def bind_somn_core(self, somn_core) -> None:
        """绑定/更新 SomnCore 实例，重新注册处理器"""
        self._somn_core = somn_core
        if self._initialized:
            self._register_agent_core_handler()
            self._register_somn_core_handler()
            self._register_wisdom_handler()
            self._register_memory_handler()
            self._register_learning_handler()
            self._register_autonomy_handler()
            logger.info(f"[GlobalNeuralBridge] SomnCore 已重新绑定: {type(somn_core).__name__}")

    def _safe_call(self, bridge_name: str, fn: Callable, *args, **kwargs) -> Any:
        """安全调用处理器，记录统计"""
        start = time.time()
        try:
            result = fn(*args, **kwargs)
            elapsed = (time.time() - start) * 1000
            self._stats["bridge_calls"][bridge_name] = \
                self._stats["bridge_calls"].get(bridge_name, 0) + 1
            # 滚动平均延迟
            total = self._stats["total_queries"]
            self._stats["avg_latency_ms"] = (
                (self._stats["avg_latency_ms"] * total + elapsed) / (total + 1)
            )
            self._stats["total_queries"] += 1
            return result
        except Exception as e:
            self._stats["errors"] += 1
            logger.warning(f"[Bridge:{bridge_name}] 调用失败: {e}")
            return None

    # ─── 真实模块处理器注册 ───

    def _register_agent_core_handler(self) -> None:
        """注册 AgentCore → SomnCore.analyze_requirement()"""
        def handler(data: Any) -> Any:
            core = self._somn_core
            if core is None:
                return {"status": "no_somn_core", "bridge": "agent_core"}

            query = data.get("query", data) if isinstance(data, dict) else str(data)
            context = data.get("context", {}) if isinstance(data, dict) else None

            result = self._safe_call("agent_core", core.analyze_requirement, query, context)
            if result is None:
                return {"status": "error", "bridge": "agent_core"}

            # 提取关键信息
            routing = result.get("routing_decision", {})
            return {
                "status": "success",
                "bridge": "agent_core",
                "real": True,
                "route": routing.get("route", "unknown"),
                "complexity": routing.get("complexity", 0),
                "task_id": result.get("task_id", ""),
                "timestamp": datetime.now().isoformat(),
            }

        self._bridge_handlers["agent_core"] = handler
        lm = self.layout_manager
        lm.register_function_handler("AgentCore", handler)

    def _register_somn_core_handler(self) -> None:
        """注册 SomnCore → SomnCore.get_capabilities()"""
        def handler(data: Any) -> Any:
            core = self._somn_core
            if core is None:
                return {"status": "no_somn_core", "bridge": "somn_core"}

            caps = self._safe_call("somn_core", core.get_capabilities)
            if caps is None:
                return {"status": "error", "bridge": "somn_core"}

            return {
                "status": "success",
                "bridge": "somn_core",
                "real": True,
                "capabilities": caps,
                "timestamp": datetime.now().isoformat(),
            }

        self._bridge_handlers["somn_core"] = handler
        lm = self.layout_manager
        lm.register_function_handler("SomnCore", handler)

    def _register_wisdom_handler(self) -> None:
        """注册 WisdomDispatcher → SomnCore.super_wisdom.analyze()"""
        def handler(data: Any) -> Any:
            core = self._somn_core
            if core is None:
                return {"status": "no_somn_core", "bridge": "wisdom_dispatcher"}

            query = data.get("query", data) if isinstance(data, dict) else str(data)
            context = data.get("context", {}) if isinstance(data, dict) else {}

            # 确保智慧层已加载
            core._ensure_wisdom_layers()
            if core.super_wisdom is None:
                return {"status": "wisdom_not_loaded", "bridge": "wisdom_dispatcher"}

            result = self._safe_call("wisdom_dispatcher", core.super_wisdom.analyze,
                                      query_text=query, context=context,
                                      threshold=0.25, max_schools=6)
            if result is None:
                return {"status": "error", "bridge": "wisdom_dispatcher"}

            return {
                "status": "success",
                "bridge": "wisdom_dispatcher",
                "real": True,
                "primary_insight": getattr(result, 'primary_insight', ''),
                "schools": getattr(result, 'activated_schools', []),
                "timestamp": datetime.now().isoformat(),
            }

        self._bridge_handlers["wisdom_dispatcher"] = handler
        lm = self.layout_manager
        lm.register_function_handler("WisdomDispatcher", handler)

    def _register_memory_handler(self) -> None:
        """注册 MemorySystem → SomnCore._query_memory_context()"""
        def handler(data: Any) -> Any:
            core = self._somn_core
            if core is None:
                return {"status": "no_somn_core", "bridge": "memory_system"}

            query = data.get("query", data) if isinstance(data, dict) else str(data)
            operation = data.get("operation", "query") if isinstance(data, dict) else "query"

            if operation == "query":
                result = self._safe_call("memory_system", core._query_memory_context, query)
                if result is None:
                    return {"status": "error", "bridge": "memory_system"}
                return {
                    "status": "success",
                    "bridge": "memory_system",
                    "real": True,
                    "confidence": result.get("confidence", 0.0),
                    "has_evidence": bool(result.get("evidence_chain")),
                    "timestamp": datetime.now().isoformat(),
                }
            elif operation == "store":
                # 通过 neural_system 写入
                core._ensure_layers()
                if core.neural_system:
                    title = data.get("title", "neural_bridge_store") if isinstance(data, dict) else "neural_bridge_store"
                    desc = data.get("description", query) if isinstance(data, dict) else query
                    self._safe_call("memory_system", core._record_task_memory,
                                    title, desc, 80, ["neural_bridge"])
                    return {"status": "success", "bridge": "memory_system", "real": True}
                return {"status": "no_neural_system", "bridge": "memory_system"}
            else:
                return {"status": "unknown_operation", "bridge": "memory_system", "operation": operation}

        self._bridge_handlers["memory_system"] = handler
        lm = self.layout_manager
        lm.register_function_handler("NeuralMemorySystem", handler)

    def _register_learning_handler(self) -> None:
        """注册 LearningCoordinator → SomnCore.learning_coordinator"""
        def handler(data: Any) -> Any:
            core = self._somn_core
            if core is None:
                return {"status": "no_somn_core", "bridge": "learning_system"}

            core._ensure_learning_coordinator()
            if core.learning_coordinator is None:
                return {"status": "not_initialized", "bridge": "learning_system"}

            # 获取学习统计
            try:
                stats = getattr(core.learning_coordinator, 'get_statistics', lambda: {})()
                return {
                    "status": "success",
                    "bridge": "learning_system",
                    "real": True,
                    "stats": stats,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                return {"status": "error", "bridge": "learning_system", "error": str(e)}

        self._bridge_handlers["learning_system"] = handler
        lm = self.layout_manager
        lm.register_function_handler("LearningCoordinator", handler)

    def _register_autonomy_handler(self) -> None:
        """注册 AutonomousAgent → SomnCore.autonomous_agent"""
        def handler(data: Any) -> Any:
            core = self._somn_core
            if core is None:
                return {"status": "no_somn_core", "bridge": "autonomy_system"}

            core._ensure_autonomous_agent()
            if core.autonomous_agent is None:
                return {"status": "not_initialized", "bridge": "autonomy_system"}

            # 获取自主目标
            try:
                goals = getattr(core.autonomous_agent, 'goal_system', None)
                ready = []
                if goals:
                    ready = [
                        {"id": g.id, "title": g.title, "status": g.status}
                        for g in (goals.get_ready_goals() if hasattr(goals, 'get_ready_goals') else [])
                    ]
                return {
                    "status": "success",
                    "bridge": "autonomy_system",
                    "real": True,
                    "ready_goals": ready[:5],
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                return {"status": "error", "bridge": "autonomy_system", "error": str(e)}

        self._bridge_handlers["autonomy_system"] = handler
        lm = self.layout_manager
        lm.register_function_handler("AutonomousAgent", handler)

    # ─── 核心处理接口 ───

    def process_through_network(self, input_data: Any) -> Dict[str, Any]:
        """
        通过神经网络处理输入 — 真实全链路

        数据流: input_user → neuron_agent_core → neuron_somn_core →
                neuron_super_wisdom → neuron_wisdom_dispatcher → (22学派) →
                neuron_thinking_fusion → neuron_deep_reasoning → neuron_narrative_intel →
                output_response

        Returns:
            包含激活结果、各模块输出、处理统计的字典
        """
        start_time = time.time()

        # 1. 激活主链路（神经网络传播）
        activation_result = self.layout_manager.activate_main_chain(input_data)

        # 2. 并行调用各桥接模块
        module_outputs = {}
        for bridge_name, handler in self._bridge_handlers.items():
            try:
                result = handler(input_data)
                module_outputs[bridge_name] = result
            except Exception as e:
                module_outputs[bridge_name] = {"error": str(e)}

        processing_time_ms = (time.time() - start_time) * 1000

        return {
            "status": "success",
            "activation": activation_result,
            "module_outputs": module_outputs,
            "bridge_stats": dict(self._stats),
            "network_state": self.layout_manager.get_layout_status(),
            "phase_status": self.layout_manager.get_phase_status(),
            "processing_time_ms": round(processing_time_ms, 2),
            "timestamp": datetime.now().isoformat(),
        }

    def get_bridge_status(self) -> Dict[str, Any]:
        """获取桥梁状态"""
        return {
            "initialized": self._initialized,
            "somn_core_bound": self._somn_core is not None,
            "bridges_registered": len(self._bridge_handlers),
            "bridge_names": list(self._bridge_handlers.keys()),
            "stats": dict(self._stats),
            "layout_status": self.layout_manager.get_layout_status(),
            "phase_status": self.layout_manager.get_phase_status(),
        }

    def trace_signal_path(self, start_module: str, end_module: str) -> Optional[List[str]]:
        """追踪信号路径"""
        return self.layout_manager.find_optimal_path(start_module, end_module)

    def get_neural_status(self) -> Dict[str, Any]:
        """获取神经网络完整状态（供 API/前端使用）"""
        return {
            "bridge": self.get_bridge_status(),
            "layout": self.layout_manager.get_layout_status(),
            "phases": self.layout_manager.get_phase_status(),
            "execution_history": self.layout_manager.get_execution_history(limit=10),
            "stats": dict(self._stats),
        }


# ─── 全局单例 ───

_bridge_instance: Optional[GlobalNeuralBridge] = None
_bridge_lock = threading.Lock()


def get_global_neural_bridge() -> GlobalNeuralBridge:
    """获取全局神经桥梁实例（线程安全单例）"""
    global _bridge_instance
    if _bridge_instance is None:
        with _bridge_lock:
            if _bridge_instance is None:
                _bridge_instance = GlobalNeuralBridge()
    return _bridge_instance


def bind_somn_core(somn_core) -> GlobalNeuralBridge:
    """
    便捷函数：获取桥梁并绑定 SomnCore

    Args:
        somn_core: SomnCore 实例

    Returns:
        GlobalNeuralBridge 实例
    """
    bridge = get_global_neural_bridge()
    bridge.setup_global_bridge(somn_core=somn_core)
    return bridge


def get_bound_modules() -> Dict[str, str]:
    """获取已绑定的模块列表"""
    bridge = get_global_neural_bridge()
    return {
        name: "active" for name in bridge._bridge_handlers
    }
