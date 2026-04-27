"""
Neuron Wisdom Network - 神经元智慧网络 (兼容层)
===============================================

重构后主文件仅保留向后兼容导入。
子模块:
  neuron_wisdom/_nwn_enums.py    - 枚举定义
  neuron_wisdom/_nwn_dataclasses.py - 数据类定义
  neuron_wisdom/_nwn_schools.py  - 智慧学派定义
  neuron_wisdom/_nwn_network.py  - 神经元网络核心类
  neuron_wisdom/_nwn_utils.py    - 工具函数
"""

from .neuron_wisdom import (
    NeuronState,
    WisdomSignal,
    Synapse,
    WisdomNeuron,
    NetworkPathway,
    NeuronWisdomResult,
    NeuronWisdomNetwork,
    create_neuron_wisdom_network,
    get_neuron_wisdom_network,
    reset_network,
    analyze_wisdom_network,
)

__all__ = [
    'NeuronState',
    'WisdomSignal',
    'Synapse',
    'WisdomNeuron',
    'NetworkPathway',
    'NeuronWisdomResult',
    'NeuronWisdomNetwork',
    'create_neuron_wisdom_network',
    'get_neuron_wisdom_network',
    'reset_network',
    'analyze_wisdom_network',
]
