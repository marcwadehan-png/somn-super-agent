"""
__all__ = [
    'activate',
    'add_incoming_synapse',
    'add_outgoing_synapse',
    'get_activation_history',
    'get_connected_neurons',
    'get_stats',
    'process',
    'remove_synapse',
    'reset',
    'to_dict',
]

神经元节点定义
神经网络的基本单元
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable, Set
import uuid
import threading

from .signal import Signal, SignalType, SignalBatch, SignalPriority
from .synapse_connection import SynapseConnection, ConnectionType

class NeuronType(Enum):
    """神经元类型"""
    INPUT = auto()          # 输入神经元 (感知层)
    HIDDEN = auto()         # 隐藏神经元 (处理层)
    OUTPUT = auto()         # 输出神经元 (输出层)
    WISDOM = auto()         # 智慧神经元 (学派层)
    MEMORY = auto()         # 记忆神经元
    CONTROL = auto()        # 控制神经元
    FEEDBACK = auto()       # 反馈神经元

class NeuronState(Enum):
    """神经元状态"""
    DORMANT = auto()        # 休眠
    ACTIVE = auto()         # 活跃
    EXCITED = auto()        # 兴奋
    INHIBITED = auto()      # 抑制
    PLASTIC = auto()        # 可塑
    REFRACTORY = auto()     # 不应期

@dataclass
class NeuronProfile:
    """神经元画像"""
    capabilities: List[str] = field(default_factory=list)      # 能力列表
    keywords: List[str] = field(default_factory=list)          # 关键词
    problem_types: List[str] = field(default_factory=list)     # 处理问题类型
    input_schema: Optional[Dict] = None                        # 输入模式
    output_schema: Optional[Dict] = None                       # 输出模式
    avg_processing_time: float = 0.0                           # 平均处理时间
    success_rate: float = 1.0                                  # 成功率

class NeuronNode(ABC):
    """
    神经元节点基类
    
    所有功能模块的神经元化封装
    """
    
    def __init__(
        self,
        neuron_id: str,
        neuron_type: NeuronType,
        name: str = "",
        description: str = ""
    ):
        self.neuron_id = neuron_id
        self.neuron_type = neuron_type
        self.name = name or neuron_id
        self.description = description
        
        # 状态
        self.state = NeuronState.DORMANT
        self.activation_level = 0.0         # 激活水平 (0.0 - 1.0)
        self.threshold = 0.5                # 激活阈值
        
        # 连接
        self.incoming_synapses: Dict[str, SynapseConnection] = {}
        self.outgoing_synapses: Dict[str, SynapseConnection] = {}
        
        # 信号处理
        self.input_buffer: List[Signal] = []
        self.output_buffer: List[Signal] = []
        self.received_signals: int = 0
        self.emitted_signals: int = 0
        
        # 画像
        self.profile = NeuronProfile()
        
        # 统计
        self.activation_count = 0
        self.last_activation: Optional[datetime] = None
        self.total_processing_time = 0.0
        
        # 线程安全
        self._lock = threading.RLock()
        
        # 元数据
        self.metadata: Dict[str, Any] = {}
        self.created_at = datetime.now()
    
    @abstractmethod
    def process(self, signal: Signal) -> Optional[Signal]:
        """
        处理输入信号
        
        Args:
            signal: 输入信号
            
        Returns:
            输出信号，如果无输出则返回None
        """
        pass
    
    def activate(self, signal: Signal) -> List[Signal]:
        """
        激活神经元
        
        Args:
            signal: 输入信号
            
        Returns:
            输出信号列表
        """
        with self._lock:
            # 更新状态
            self.state = NeuronState.ACTIVE
            self.activation_level = min(1.0, self.activation_level + signal.strength)
            self.received_signals += 1
            
            # 记录时间
            start_time = datetime.now()
            
            # 处理信号
            try:
                output = self.process(signal)
            except Exception as e:
                # 处理错误
                output = Signal(
                    source_id=self.neuron_id,
                    signal_type=SignalType.ERROR,
                    data={"error": "操作失败"},
                    strength=0.1,
                    priority=SignalPriority.HIGH
                )
            
            # 计算处理时间
            processing_time = (datetime.now() - start_time).total_seconds()
            self.total_processing_time += processing_time
            
            # 更新统计
            self.activation_count += 1
            self.last_activation = datetime.now()
            
            # 构建输出信号列表
            outputs = []
            if output:
                output.add_trace(self.neuron_id)
                outputs.append(output)
                self.emitted_signals += 1
            
            # 通过传出突触传递信号
            for synapse in self.outgoing_synapses.values():
                transmitted = synapse.transmit(signal)
                if transmitted:
                    outputs.append(transmitted)
            
            # 更新状态
            if self.activation_level < self.threshold:
                self.state = NeuronState.DORMANT
            
            return outputs
    
    def add_incoming_synapse(self, synapse: SynapseConnection) -> None:
        """添加入连接"""
        with self._lock:
            self.incoming_synapses[synapse.synapse_id] = synapse
    
    def add_outgoing_synapse(self, synapse: SynapseConnection) -> None:
        """添加出连接"""
        with self._lock:
            self.outgoing_synapses[synapse.synapse_id] = synapse
    
    def remove_synapse(self, synapse_id: str) -> bool:
        """移除连接"""
        with self._lock:
            if synapse_id in self.incoming_synapses:
                del self.incoming_synapses[synapse_id]
                return True
            if synapse_id in self.outgoing_synapses:
                del self.outgoing_synapses[synapse_id]
                return True
            return False
    
    def get_connected_neurons(self) -> Set[str]:
        """获取连接的神经元ID集合"""
        connected = set()
        for s in self.outgoing_synapses.values():
            connected.add(s.target_id)
        for s in self.incoming_synapses.values():
            connected.add(s.source_id)
        return connected
    
    def get_activation_history(self, window: int = 10) -> List[Dict]:
        """获取激活历史"""
        return [{
            "timestamp": self.last_activation.isoformat() if self.last_activation else None,
            "level": self.activation_level,
            "state": self.state.name
        }]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        avg_time = (self.total_processing_time / self.activation_count 
                   if self.activation_count > 0 else 0)
        return {
            "neuron_id": self.neuron_id,
            "neuron_type": self.neuron_type.name,
            "state": self.state.name,
            "activation_level": round(self.activation_level, 4),
            "threshold": self.threshold,
            "activation_count": self.activation_count,
            "received_signals": self.received_signals,
            "emitted_signals": self.emitted_signals,
            "avg_processing_time": round(avg_time, 4),
            "incoming_connections": len(self.incoming_synapses),
            "outgoing_connections": len(self.outgoing_synapses),
            "last_activation": self.last_activation.isoformat() if self.last_activation else None
        }
    
    def reset(self) -> None:
        """重置神经元状态"""
        with self._lock:
            self.state = NeuronState.DORMANT
            self.activation_level = 0.0
            self.input_buffer.clear()
            self.output_buffer.clear()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "neuron_id": self.neuron_id,
            "name": self.name,
            "neuron_type": self.neuron_type.name,
            "state": self.state.name,
            "description": self.description,
            "stats": self.get_stats(),
            "profile": {
                "capabilities": self.profile.capabilities,
                "keywords": self.profile.keywords,
                "problem_types": self.profile.problem_types
            }
        }

class InputNeuron(NeuronNode):
    """输入神经元 - 接收外部输入"""
    
    def __init__(self, neuron_id: str, name: str = "", description: str = "") -> None:
        super().__init__(neuron_id, NeuronType.INPUT, name, description)
        self.threshold = 0.1  # 输入神经元阈值较低
    
    def process(self, signal: Signal) -> Optional[Signal]:
        """处理输入信号 - 主要进行格式化和验证"""
        # 输入神经元主要传递信号，添加元数据
        output = signal.copy_with(
            source_id=self.neuron_id,
            metadata={"input_processed": True, "input_neuron": self.name}
        )
        return output

class OutputNeuron(NeuronNode):
    """输出神经元 - 产生最终输出"""
    
    def __init__(self, neuron_id: str, name: str = "", description: str = "") -> None:
        super().__init__(neuron_id, NeuronType.OUTPUT, name, description)
        self.output_history: List[Dict] = []
    
    def process(self, signal: Signal) -> Optional[Signal]:
        """处理输出信号 - 格式化最终输出"""
        # 记录输出历史
        self.output_history.append({
            "timestamp": datetime.now().isoformat(),
            "data": signal.data,
            "strength": signal.strength
        })
        
        # 输出神经元添加最终标记
        output = signal.copy_with(
            source_id=self.neuron_id,
            metadata={"final_output": True, "output_neuron": self.name}
        )
        return output

class WisdomNeuron(NeuronNode):
    """智慧神经元 - 封装智慧学派"""
    
    def __init__(
        self,
        neuron_id: str,
        school_id: str,
        name: str = "",
        description: str = ""
    ) -> None:
        super().__init__(neuron_id, NeuronType.WISDOM, name, description)
        self.school_id = school_id
        self.wisdom_cache: Dict[str, Any] = {}
        self.threshold = 0.3
    
    def process(self, signal: Signal) -> Optional[Signal]:
        """处理智慧请求"""
        # 从信号中提取查询
        query = signal.data.get("query", "") if isinstance(signal.data, dict) else str(signal.data)
        
        # 这里可以调用实际的智慧学派处理逻辑
        # 目前返回模拟结果
        wisdom_result = {
            "school_id": self.school_id,
            "query": query,
            "insights": [f"{self.name}智慧洞察"],
            "confidence": signal.strength
        }
        
        return signal.copy_with(
            source_id=self.neuron_id,
            data=wisdom_result,
            metadata={"wisdom_processed": True, "school": self.school_id}
        )

class MemoryNeuron(NeuronNode):
    """记忆神经元 - 处理记忆相关操作"""
    
    def __init__(self, neuron_id: str, name: str = "", description: str = "") -> None:
        super().__init__(neuron_id, NeuronType.MEMORY, name, description)
        self.memory_cache: Dict[str, Any] = {}
        self.threshold = 0.2
    
    def process(self, signal: Signal) -> Optional[Signal]:
        """处理记忆操作"""
        operation = signal.metadata.get("memory_operation", "query")
        
        if operation == "store":
            # 存储记忆
            key = signal.metadata.get("memory_key", str(uuid.uuid4()))
            self.memory_cache[key] = signal.data
            result = {"stored": True, "key": key}
        elif operation == "retrieve":
            # 检索记忆
            key = signal.metadata.get("memory_key")
            result = {"retrieved": self.memory_cache.get(key), "key": key}
        else:
            # 查询记忆
            result = {"cache_size": len(self.memory_cache)}
        
        return signal.copy_with(
            source_id=self.neuron_id,
            data=result,
            metadata={"memory_processed": True, "operation": operation}
        )
