"""
Neuron Wisdom Network - 神经元智慧网络
======================================

将43个智慧学派用神经网络的逻辑连接成一个超级智慧融合系统

子模块:
  _nwn_enums.py    - 枚举定义
  _nwn_dataclasses.py - 数据类定义
  _nwn_schools.py  - 智慧学派定义
  _nwn_network.py  - 神经元网络核心类
  _nwn_utils.py    - 工具函数
"""

from ._nwn_enums import NeuronState
from ._nwn_dataclasses import (
    WisdomSignal,
    Synapse,
    WisdomNeuron,
    NetworkPathway,
    NeuronWisdomResult,
)
from ._nwn_network import NeuronWisdomNetwork
from ._nwn_utils import (
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
