"""神经元智慧网络 - 数据类定义"""



__all__ = [
    'WisdomSignal',
    'Synapse',
    'WisdomNeuron',
    'NetworkPathway',
    'NeuronWisdomResult',
]
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from ._nwn_enums import NeuronState

@dataclass
class WisdomSignal:
    """智慧信号"""
    source_neuron: str           # 源神经元ID
    signal_type: str              # 信号类型:input/propagated/feedback
    content: Any                  # 信号内容
    intensity: float              # 信号强度 0-1
    confidence: float             # 置信度 0-1
    semantic_tags: Set[str]       # 语义标签
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Synapse:
    """突触连接"""
    source: str                  # 源神经元ID
    target: str                  # 目标神经元ID
    weight: float                # 连接权重 0-1
    plasticity: float            # 可塑性(学习率)
    last_activation: datetime    # 上次激活时间
    activation_count: int = 0     # 激活次数

@dataclass
class WisdomNeuron:
    """智慧神经元"""
    neuron_id: str               # 神经元唯一标识
    wisdom_school: str           # 所属智慧学派
    keywords: List[str]          # 触发关键词
    problem_types: List[str]     # 擅长的问题类型
    state: NeuronState = NeuronState.DORMANT
    activation_threshold: float = 0.3  # 激活阈值
    current_signal: Optional[WisdomSignal] = None
    
    # 内部状态
    input_signals: List[WisdomSignal] = field(default_factory=list)
    output_signals: List[WisdomSignal] = field(default_factory=list)
    accumulated_activation: float = 0.0
    
    # 元信息
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NetworkPathway:
    """网络通路"""
    pathway_id: str
    neurons: List[str]           # 通路上的神经元序列
    primary_type: str             # 主要类型
    efficiency: float = 1.0      # 通路效率

@dataclass
class NeuronWisdomResult:
    """神经元智慧分析结果"""
    task_id: str
    query: str
    
    # 激活的神经元
    activated_neurons: List[str]
    neuron_states: Dict[str, NeuronState]
    activation_levels: Dict[str, float]
    
    # 各学派输出
    school_outputs: Dict[str, Dict[str, Any]]
    
    # 融合结果
    fused_analysis: Dict[str, Any]
    integrated_wisdom: str
    
    # 网络信息
    pathway_used: List[str]
    synergy_score: float          # 协同度
    consensus_score: float       # 共识度
    
    # 质量metrics
    confidence: float
    coverage: float              # 覆盖面
    depth: float                # 深度
    
    timestamp: datetime = field(default_factory=datetime.now)
