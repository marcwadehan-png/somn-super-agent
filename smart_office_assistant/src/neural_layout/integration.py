"""
神经网络布局集成模块 v2.0

将神经网络布局集成到 Somn 主系统的真实入口。
被 _somn_ensure.py 的 ensure_neural_layout() 调用，
绑定 SomnCore 实例，使 GlobalNeuralBridge 的 6 个桥接真正干活。

v2.0 变更：
- 不再是空壳包装器
- 真实绑定 SomnCore → GlobalNeuralBridge
- 提供路由级入口 process_neural_layout_route()
- 供 API 层和前端查询 get_neural_status()
"""

__all__ = [
    'NeuralLayoutIntegration',
    'get_neural_integration',
    'initialize_neural_layout',
    'process_with_neural_layout',
    'get_neural_status',
]

from typing import Any, Dict, Optional
from datetime import datetime
import logging
import threading

logger = logging.getLogger(__name__)


class NeuralLayoutIntegration:
    """
    神经网络布局集成器 v2.0

    职责：
    1. 绑定 SomnCore 到 GlobalNeuralBridge（6 个真实处理器）
    2. 对外提供 process() 路由级处理入口
    3. 提供状态查询供 API/前端消费
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> 'NeuralLayoutIntegration':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._somn_core = None
        self._bridge = None
        self._init_time = None
        self._initialized = False

    def initialize(self, somn_core=None) -> bool:
        """
        初始化神经网络布局集成 — 绑定真实 SomnCore

        Args:
            somn_core: SomnCore 实例。如果为 None，使用延迟绑定。

        Returns:
            bool: 初始化是否成功
        """
        if self._initialized:
            return True

        try:
            # 导入并绑定桥接
            from .global_neural_bridge import get_global_neural_bridge, bind_somn_core

            self._bridge = get_global_neural_bridge()

            if somn_core is not None:
                self._somn_core = somn_core
                bind_somn_core(somn_core)
            else:
                # 仅初始化布局（不绑定 SomnCore，后续可调用 bind_somn_core）
                self._bridge.setup_global_bridge(somn_core=None)

            self._initialized = True
            self._init_time = datetime.now().isoformat()
            logger.info(
                f"[NeuralLayout] 集成完成, "
                f"somn_core={'已绑定' if self._somn_core else '延迟'}"
            )
            return True

        except Exception as e:
            logger.error(f"[NeuralLayout] 初始化失败: {e}")
            return False

    def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        """
        通过神经网络布局处理输入

        数据流: 用户输入 → 神经网络信号传播 → 6桥接并行调用真实模块 → 汇总结果

        Args:
            input_data: 输入数据（字符串或字典）
            context: 上下文信息

        Returns:
            包含激活路径、各模块输出、统计信息的字典
        """
        if not self._initialized:
            if not self.initialize():
                return {"status": "error", "message": "NeuralLayout 未初始化"}

        # 标准化输入
        if isinstance(input_data, str):
            full_input = {"query": input_data, "context": context or {}}
        elif isinstance(input_data, dict):
            full_input = {**input_data, "context": context or input_data.get("context", {})}
        else:
            full_input = {"data": str(input_data), "context": context or {}}

        full_input["timestamp"] = datetime.now().isoformat()

        # 通过桥接全链路处理
        result = self._bridge.process_through_network(full_input)

        # 提取关键信息供调用方使用
        module_outputs = result.get("module_outputs", {})
        activation = result.get("activation", {})

        # 找出成功调用的真实模块
        active_bridges = [
            name for name, out in module_outputs.items()
            if isinstance(out, dict) and out.get("real") is True
        ]

        # 提取 AgentCore 的路由决策
        agent_output = module_outputs.get("agent_core", {})
        route_decision = agent_output.get("route", "unknown") if isinstance(agent_output, dict) else None

        return {
            "status": "success",
            "route_decision": route_decision,
            "active_bridges": active_bridges,
            "module_outputs": module_outputs,
            "pathway": activation.get("pathway", []) if isinstance(activation, dict) else [],
            "processing_time_ms": result.get("processing_time_ms", 0),
            "timestamp": datetime.now().isoformat(),
        }

    def get_status(self) -> Dict[str, Any]:
        """获取神经网络布局集成状态（供 API/前端消费）"""
        if not self._initialized or self._bridge is None:
            return {
                "initialized": False,
                "somn_core_bound": False,
                "init_time": None,
            }

        bridge_status = self._bridge.get_bridge_status()
        return {
            "initialized": True,
            "somn_core_bound": self._somn_core is not None,
            "init_time": self._init_time,
            "bridges": bridge_status.get("bridge_names", []),
            "bridge_count": bridge_status.get("bridges_registered", 0),
            "stats": bridge_status.get("stats", {}),
            "layout_status": bridge_status.get("layout_status", {}),
        }

    def bind_somn_core_later(self, somn_core) -> None:
        """延迟绑定 SomnCore（用于 SomnCore 实例晚于 neural_layout 创建的场景）"""
        self._somn_core = somn_core
        if self._bridge is not None:
            from .global_neural_bridge import bind_somn_core
            bind_somn_core(somn_core)
            logger.info("[NeuralLayout] SomnCore 延迟绑定完成")


# ─── 全局单例 ───

_integration_instance: Optional[NeuralLayoutIntegration] = None


def get_neural_integration() -> NeuralLayoutIntegration:
    """获取神经网络布局集成实例（全局单例）"""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = NeuralLayoutIntegration()
    return _integration_instance


def initialize_neural_layout(somn_core=None) -> NeuralLayoutIntegration:
    """
    便捷函数：初始化神经网络布局并绑定 SomnCore

    Args:
        somn_core: SomnCore 实例

    Returns:
        NeuralLayoutIntegration 实例
    """
    integration = get_neural_integration()
    integration.initialize(somn_core=somn_core)
    return integration


def process_with_neural_layout(input_data: Any, context: Optional[Dict] = None) -> Dict:
    """
    便捷函数：使用神经网络布局处理数据

    Args:
        input_data: 输入（字符串或字典）
        context: 上下文

    Returns:
        处理结果字典
    """
    integration = get_neural_integration()
    return integration.process(input_data, context)


def get_neural_status() -> Dict[str, Any]:
    """便捷函数：获取神经网络布局状态"""
    integration = get_neural_integration()
    return integration.get_status()
