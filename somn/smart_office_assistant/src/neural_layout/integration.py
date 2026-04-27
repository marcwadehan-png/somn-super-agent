"""
__all__ = [
    'get_network_status',
    'get_neural_integration',
    'initialize',
    'integrate_with_agent_core',
    'integrate_with_somn_core',
    'process',
    'process_with_neural_layout',
    'trace_module_path',
]

神经网络布局集成模块

将神经网络布局集成到Somn主系统
"""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from .global_neural_bridge import GlobalNeuralBridge, get_global_neural_bridge
from .network_layout_manager import NetworkLayoutManager
from .neural_network import NeuralNetwork
from .signal import Signal, SignalType, SignalPriority

class NeuralLayoutIntegration:
    """
    神经网络布局集成器
    
    将神经网络布局无缝集成到Somn系统的入口点
    """
    
    def __init__(self):
        self.bridge = get_global_neural_bridge()
        self._initialized = False
    
    def initialize(self) -> bool:
        """初始化神经网络布局集成"""
        if self._initialized:
            return True
        
        success = self.bridge.setup_global_bridge()
        self._initialized = success
        return success
    
    def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        """
        通过神经网络布局处理输入
        
        这是集成后的主处理入口
        """
        if not self._initialized:
            self.initialize()
        
        # 构建完整的输入
        full_input = {
            "data": input_data,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # 通过神经网络处理
        result = self.bridge.process_through_network(full_input)
        
        return {
            "output": result,
            "neural_pathway": result.get("network_activation", {}).get("pathway", []),
            "activated_modules": list(result.get("module_outputs", {}).keys()),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_network_status(self) -> Dict:
        """获取网络状态"""
        if not self._initialized:
            return {"initialized": False}
        
        return self.bridge.get_bridge_status()
    
    def trace_module_path(self, start: str, end: str) -> Optional[List[str]]:
        """追踪模块间路径"""
        if not self._initialized:
            return None
        
        return self.bridge.trace_signal_path(start, end)

# 全局集成实例
_neural_integration: Optional[NeuralLayoutIntegration] = None

def get_neural_integration() -> NeuralLayoutIntegration:
    """获取神经网络布局集成实例"""
    global _neural_integration
    if _neural_integration is None:
        _neural_integration = NeuralLayoutIntegration()
    return _neural_integration

def process_with_neural_layout(input_data: Any, context: Optional[Dict] = None) -> Dict:
    """
    使用神经网络布局处理数据
    
    这是对外提供的便捷函数
    """
    integration = get_neural_integration()
    return integration.process(input_data, context)

# 与现有系统的集成点
def integrate_with_somn_core(somn_core_instance):
    """
    与SomnCore集成
    
    将神经网络布局注入到SomnCore中
    """
    integration = get_neural_integration()
    integration.initialize()
    
    # 将神经网络布局添加到SomnCore
    somn_core_instance.neural_layout = integration
    
    return True

def integrate_with_agent_core(agent_core_instance):
    """
    与AgentCore集成
    
    将神经网络布局注入到AgentCore中
    """
    integration = get_neural_integration()
    integration.initialize()
    
    # 将神经网络布局添加到AgentCore
    agent_core_instance.neural_layout = integration
    
    return True
