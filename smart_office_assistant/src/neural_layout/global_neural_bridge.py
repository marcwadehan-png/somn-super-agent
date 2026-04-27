"""
__all__ = [
    'agent_core_handler',
    'autonomy_handler',
    'get_bridge_status',
    'get_global_neural_bridge',
    'learning_handler',
    'memory_handler',
    'process_through_network',
    'setup_global_bridge',
    'somn_core_handler',
    'trace_signal_path',
    'wisdom_dispatcher_handler',
]

全局神经桥梁

将神经网络布局与Somn现有系统打通，实现全链路串联

V2.0: 支持真实模块处理器绑定 + 模拟降级
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from datetime import datetime
import threading
import uuid
import logging

logger = logging.getLogger(__name__)

from .signal import Signal, SignalType, SignalPriority
from .synapse_connection import SynapseConnection, ConnectionType
from .neuron_node import NeuronNode, NeuronType, NeuronState
from .neural_network import NeuralNetwork
from .network_layout_manager import NetworkLayoutManager

# 可选的真实模块引用（延迟导入）
_real_modules: Dict[str, Any] = {}


def bind_real_module(module_name: str, instance: Any) -> None:
    """绑定真实模块实例到桥梁
    
    Args:
        module_name: 模块名称 (agent_core/somn_core/wisdom_dispatcher/memory_system/learning_system/autonomy_system)
        instance: 模块实例
    """
    _real_modules[module_name] = instance
    logger.info(f"[GlobalNeuralBridge] 已绑定真实模块: {module_name} ({type(instance).__name__})")


def unbind_real_module(module_name: str) -> None:
    """解绑真实模块实例"""
    if module_name in _real_modules:
        del _real_modules[module_name]
        logger.info(f"[GlobalNeuralBridge] 已解绑模块: {module_name}")


def get_bound_modules() -> Dict[str, str]:
    """获取已绑定的模块列表
    
    Returns:
        {module_name: class_name} 字典
    """
    return {k: type(v).__name__ for k, v in _real_modules.items()}


class GlobalNeuralBridge:
    """
    全局神经桥梁
    
    连接神经网络布局与Somn系统的各个模块：
    1. AgentCore 集成
    2. SomnCore 集成
    3. 智慧调度集成
    4. 记忆系统集成
    5. 学习系统集成
    6. 自主系统集成
    
    V2.0: 支持绑定真实模块实例，降级使用模拟处理器
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'GlobalNeuralBridge':
        """单例模式实现"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        """初始化全局神经桥梁"""
        if self._initialized:
            return
        
        self.layout_manager = NetworkLayoutManager()
        self.bridges: Dict[str, Callable[[Signal], Signal]] = {}  # 模块桥接函数
        self.module_handlers: Dict[str, Any] = {}  # 实际模块处理器
        self._initialized = True
        self._setup_lock = threading.Lock()
        self._real_bindings: Dict[str, bool] = {}  # 记录哪些桥接使用了真实模块
    
    def setup_global_bridge(self, bind_real: bool = True) -> bool:
        """设置全局桥梁
        
        初始化神经网络布局并注册各模块桥接
        
        Args:
            bind_real: 是否尝试绑定真实模块
            
        Returns:
            bool: 设置是否成功
        """
        with self._setup_lock:
            # 1. 初始化神经网络布局
            if not self.layout_manager.initialize_global_layout():
                return False
            
            # 2. 注册各模块桥接
            self._register_agent_core_bridge()
            self._register_somn_core_bridge()
            self._register_wisdom_bridge()
            self._register_memory_bridge()
            self._register_learning_bridge()
            self._register_autonomy_bridge()
            
            return True
    
    def _try_get_real_handler(self, module_name: str) -> Optional[Any]:
        """尝试获取真实模块处理器"""
        return _real_modules.get(module_name)
    
    def _register_agent_core_bridge(self) -> None:
        """注册AgentCore桥接"""
        def agent_core_handler(signal: Signal) -> Signal:
            data = signal.data
            
            # 尝试使用真实模块
            real = self._try_get_real_handler("agent_core")
            if real and hasattr(real, 'process_input'):
                try:
                    query = data.get("query", data) if isinstance(data, dict) else str(data)
                    result = real.process_input(query, data if isinstance(data, dict) else None)
                    return signal.copy_with(
                        source_id="neuron_agent_core",
                        data={
                            "processed_by": "AgentCore (real)",
                            "result": str(result)[:500],
                            "status": "success",
                            "timestamp": datetime.now().isoformat(),
                        },
                        metadata={"bridge": "agent_core", "real": True}
                    )
                except Exception as e:
                    logger.warning(f"[Bridge] AgentCore 真实调用失败，降级到模拟: {e}")
            
            # 模拟处理
            result = {
                "processed_by": "AgentCore (simulated)",
                "input": str(data)[:200],
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
            return signal.copy_with(
                source_id="neuron_agent_core",
                data=result,
                metadata={"bridge": "agent_core", "real": False}
            )
        
        self.bridges["agent_core"] = agent_core_handler
        
        # 绑定到神经元
        neuron = self.layout_manager.network.neurons.get("neuron_agent_core")
        if neuron and hasattr(neuron, 'function_handler'):
            neuron.function_handler = lambda data: agent_core_handler(
                Signal("input", SignalType.DATA, data)
            ).data
    
    def _register_somn_core_bridge(self) -> None:
        """注册SomnCore桥接"""
        def somn_core_handler(signal: Signal) -> Signal:
            data = signal.data
            
            # 尝试使用真实模块
            real = self._try_get_real_handler("somn_core")
            if real and hasattr(real, 'analyze_requirement'):
                try:
                    query = data.get("query", data) if isinstance(data, dict) else str(data)
                    result = real.analyze_requirement(query)
                    return signal.copy_with(
                        source_id="neuron_somn_core",
                        data={
                            "processed_by": "SomnCore (real)",
                            "result": str(result)[:500],
                            "capabilities": real.get_capabilities() if hasattr(real, 'get_capabilities') else [],
                            "timestamp": datetime.now().isoformat(),
                        },
                        metadata={"bridge": "somn_core", "real": True}
                    )
                except Exception as e:
                    logger.warning(f"[Bridge] SomnCore 真实调用失败，降级到模拟: {e}")
            
            # 模拟SomnCore处理
            result = {
                "processed_by": "SomnCore (simulated)",
                "input": str(data)[:200],
                "capabilities": [
                    "analysis", "strategy", "execution",
                    "evaluation", "learning"
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            return signal.copy_with(
                source_id="neuron_somn_core",
                data=result,
                metadata={"bridge": "somn_core", "real": False}
            )
        
        self.bridges["somn_core"] = somn_core_handler
        
        neuron = self.layout_manager.network.neurons.get("neuron_somn_core")
        if neuron and hasattr(neuron, 'function_handler'):
            neuron.function_handler = lambda data: somn_core_handler(
                Signal("input", SignalType.DATA, data)
            ).data
    
    def _register_wisdom_bridge(self) -> None:
        """注册智慧调度桥接"""
        def wisdom_dispatcher_handler(signal: Signal) -> Signal:
            data = signal.data
            query = data.get("query", "") if isinstance(data, dict) else str(data)
            
            # 尝试使用真实模块
            real = self._try_get_real_handler("wisdom_dispatcher")
            if real and hasattr(real, 'dispatch'):
                try:
                    dispatch_result = real.dispatch(query)
                    selected_schools = []
                    if isinstance(dispatch_result, dict):
                        selected_schools = dispatch_result.get("selected_schools", [])
                    elif isinstance(dispatch_result, list):
                        selected_schools = [str(s) for s in dispatch_result[:5]]
                    
                    return signal.copy_with(
                        source_id="neuron_wisdom_dispatcher",
                        data={
                            "processed_by": "WisdomDispatcher (real)",
                            "query": query,
                            "selected_schools": selected_schools,
                            "school_count": len(selected_schools),
                            "timestamp": datetime.now().isoformat(),
                        },
                        metadata={"bridge": "wisdom_dispatcher", "real": True}
                    )
                except Exception as e:
                    logger.warning(f"[Bridge] WisdomDispatcher 真实调用失败，降级到模拟: {e}")
            
            # 模拟智慧分发
            selected_schools = self._select_wisdom_schools(query)
            
            result = {
                "processed_by": "WisdomDispatcher (simulated)",
                "query": query,
                "selected_schools": selected_schools,
                "school_count": len(selected_schools),
                "timestamp": datetime.now().isoformat()
            }
            
            return signal.copy_with(
                source_id="neuron_wisdom_dispatcher",
                data=result,
                metadata={"bridge": "wisdom_dispatcher", "schools": selected_schools, "real": False}
            )
        
        self.bridges["wisdom_dispatcher"] = wisdom_dispatcher_handler
        
        neuron = self.layout_manager.network.neurons.get("neuron_wisdom_dispatcher")
        if neuron and hasattr(neuron, 'function_handler'):
            neuron.function_handler = lambda data: wisdom_dispatcher_handler(
                Signal("input", SignalType.DATA, data)
            ).data
    
    def _select_wisdom_schools(self, query: str) -> List[str]:
        """根据查询选择智慧学派"""
        schools = []
        query_lower = query.lower()
        
        keywords_map = {
            "CONFUCIAN": ["仁", "礼", "德", "道德", "伦理"],
            "TAOIST": ["道", "自然", "无为", "阴阳"],
            "BUDDHIST": ["佛", "心", "悟", "禅", "空"],
            "SUNZI": ["兵", "战", "略", "谋", "策"],
            "SUFU": ["素书", "德", "义", "仁"],
            "YANGMING": ["心学", "知行合一", "良知"],
            "DEWEY": ["思维", "反省", "教育"],
            "TOP_METHODS": ["思维", "模型", "第一性原理"],
            "PSYCHOLOGY": ["心理", "消费者", "营销"],
            "SCIENCE": ["科学", "实验", "验证"],
        }
        
        for school, keywords in keywords_map.items():
            if any(kw in query_lower for kw in keywords):
                schools.append(school)
        
        if not schools:
            schools = ["CONFUCIAN", "TAOIST", "TOP_METHODS"]
        
        return schools[:5]
    
    def _register_memory_bridge(self) -> None:
        """注册记忆系统桥接"""
        def memory_handler(signal: Signal) -> Signal:
            operation = signal.metadata.get("memory_operation", "query")
            
            # 尝试使用真实模块
            real = self._try_get_real_handler("memory_system")
            if real:
                try:
                    if operation == "store" and hasattr(real, 'store'):
                        key = real.store(signal.data)
                        result = {"stored": True, "key": key}
                    elif operation == "retrieve" and hasattr(real, 'retrieve'):
                        result = {"retrieved": real.retrieve(signal.data)}
                    elif operation == "query" and hasattr(real, 'query'):
                        result = {"results": real.query(signal.data)}
                    else:
                        result = {"operation": operation, "real_module": True}
                    
                    return signal.copy_with(
                        source_id="neuron_neural_memory",
                        data=result,
                        metadata={"bridge": "memory_system", "real": True}
                    )
                except Exception as e:
                    logger.warning(f"[Bridge] MemorySystem 真实调用失败，降级到模拟: {e}")
            
            # 模拟记忆操作
            if operation == "store":
                result = {"stored": True, "key": str(uuid.uuid4())[:8]}
            elif operation == "retrieve":
                result = {"retrieved": None, "found": False}
            else:
                result = {"operation": operation, "status": "unknown"}
            
            return signal.copy_with(
                source_id="neuron_neural_memory",
                data=result,
                metadata={"bridge": "memory_system", "real": False}
            )
        
        self.bridges["memory_system"] = memory_handler
        
        neuron = self.layout_manager.network.neurons.get("neuron_neural_memory")
        if neuron and hasattr(neuron, 'function_handler'):
            neuron.function_handler = lambda data: memory_handler(
                Signal("input", SignalType.DATA, data)
            ).data
    
    def _register_learning_bridge(self) -> None:
        """注册学习系统桥接"""
        def learning_handler(signal: Signal) -> Signal:
            data = signal.data
            
            # 尝试使用真实模块
            real = self._try_get_real_handler("learning_system")
            if real:
                try:
                    if hasattr(real, 'learn'):
                        real.learn(data)
                        result = {"learned": True}
                    elif hasattr(real, 'record_feedback'):
                        real.record_feedback(data)
                        result = {"feedback_recorded": True}
                    else:
                        result = {"processed": True}
                    
                    return signal.copy_with(
                        source_id="neuron_learning_coord",
                        data={
                            "processed_by": "LearningCoordinator (real)",
                            **result,
                            "timestamp": datetime.now().isoformat(),
                        },
                        metadata={"bridge": "learning_system", "real": True}
                    )
                except Exception as e:
                    logger.warning(f"[Bridge] LearningSystem 真实调用失败，降级到模拟: {e}")
            
            # 模拟学习处理
            result = {
                "processed_by": "LearningCoordinator (simulated)",
                "learning_type": data.get("type", "general") if isinstance(data, dict) else "general",
                "feedback_recorded": True,
                "q_values_updated": True,
                "timestamp": datetime.now().isoformat()
            }
            
            return signal.copy_with(
                source_id="neuron_learning_coord",
                data=result,
                metadata={"bridge": "learning_system", "real": False}
            )
        
        self.bridges["learning_system"] = learning_handler
        
        neuron = self.layout_manager.network.neurons.get("neuron_learning_coord")
        if neuron and hasattr(neuron, 'function_handler'):
            neuron.function_handler = lambda data: learning_handler(
                Signal("input", SignalType.DATA, data)
            ).data
    
    def _register_autonomy_bridge(self) -> None:
        """注册自主系统桥接"""
        def autonomy_handler(signal: Signal) -> Signal:
            data = signal.data
            
            # 尝试使用真实模块
            real = self._try_get_real_handler("autonomy_system")
            if real:
                try:
                    if hasattr(real, 'plan_and_execute'):
                        result = real.plan_and_execute(data)
                    elif hasattr(real, 'execute'):
                        result = real.execute(data)
                    else:
                        result = {"processed": True}
                    
                    return signal.copy_with(
                        source_id="neuron_autonomous_agent",
                        data={
                            "processed_by": "AutonomousAgent (real)",
                            **result,
                            "timestamp": datetime.now().isoformat(),
                        },
                        metadata={"bridge": "autonomy_system", "real": True}
                    )
                except Exception as e:
                    logger.warning(f"[Bridge] AutonomySystem 真实调用失败，降级到模拟: {e}")
            
            # 模拟自主处理
            result = {
                "processed_by": "AutonomousAgent (simulated)",
                "autonomy_level": "high",
                "actions_planned": [
                    "analyze_context",
                    "select_strategy",
                    "execute_action",
                    "monitor_result"
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            return signal.copy_with(
                source_id="neuron_autonomous_agent",
                data=result,
                metadata={"bridge": "autonomy_system", "real": False}
            )
        
        self.bridges["autonomy_system"] = autonomy_handler
        
        neuron = self.layout_manager.network.neurons.get("neuron_autonomous_agent")
        if neuron and hasattr(neuron, 'function_handler'):
            neuron.function_handler = lambda data: autonomy_handler(
                Signal("input", SignalType.DATA, data)
            ).data
    
    def process_through_network(self, input_data: Any) -> Dict[str, Any]:
        """通过网络处理输入
        
        完整的全链路处理流程
        """
        # 1. 激活主链路（集成 Phase4 + Phase3）
        activation_result = self.layout_manager.activate_main_chain(input_data)
        
        # 2. 收集各模块输出
        module_outputs = {}
        for bridge_name, bridge_func in self.bridges.items():
            try:
                signal = Signal("input", SignalType.DATA, input_data)
                result = bridge_func(signal)
                module_outputs[bridge_name] = result.data
            except Exception as e:
                module_outputs[bridge_name] = {"error": "操作失败"}
        
        # 3. 整合结果
        return {
            "network_activation": activation_result,
            "module_outputs": module_outputs,
            "network_state": self.layout_manager.get_layout_status(),
            "phase_status": self.layout_manager.get_phase_status(),
            "bound_modules": get_bound_modules(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_bridge_status(self) -> Dict[str, Any]:
        """获取桥梁状态"""
        return {
            "initialized": self._initialized,
            "bridges_registered": len(self.bridges),
            "bridge_names": list(self.bridges.keys()),
            "bound_real_modules": get_bound_modules(),
            "layout_status": self.layout_manager.get_layout_status(),
            "phase_status": self.layout_manager.get_phase_status(),
        }
    
    def trace_signal_path(self, start_module: str, end_module: str) -> Optional[List[str]]:
        """追踪信号路径"""
        return self.layout_manager.find_optimal_path(start_module, end_module)

# 全局实例
def get_global_neural_bridge() -> GlobalNeuralBridge:
    """获取全局神经桥梁实例（单例）"""
    return GlobalNeuralBridge()
