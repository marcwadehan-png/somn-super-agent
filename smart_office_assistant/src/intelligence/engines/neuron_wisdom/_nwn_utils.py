"""神经元智慧网络 - 工具函数"""

from typing import Any, Dict, Optional

from ._nwn_network import NeuronWisdomNetwork

# 单例实例
__all__ = [
    'analyze_wisdom_network',
    'create_neuron_wisdom_network',
    'get_neuron_wisdom_network',
    'reset_network',
]

_network_instance: Optional[NeuronWisdomNetwork] = None

def create_neuron_wisdom_network() -> NeuronWisdomNetwork:
    """创建神经元智慧网络"""
    return NeuronWisdomNetwork()

def get_neuron_wisdom_network() -> NeuronWisdomNetwork:
    """获取单例网络实例"""
    global _network_instance
    if _network_instance is None:
        _network_instance = create_neuron_wisdom_network()
    return _network_instance

def reset_network():
    """重置网络(用于测试)"""
    global _network_instance
    _network_instance = None

def analyze_wisdom_network(query: str, threshold: float = 0.3) -> Dict[str, Any]:
    """
    快速分析函数
    
    Args:
        query: 用户查询
        threshold: 激活阈值
        
    Returns:
        分析结果字典
    """
    network = get_neuron_wisdom_network()
    activations = network.activate_network(query)
    activated = network.get_activated_neurons(activations, threshold)
    insights = network.get_network_insights(activations)
    
    return {
        "activations": activations,
        "activated_neurons": activated,
        "insights": insights
    }
