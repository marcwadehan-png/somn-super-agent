"""
__all__ = [
    'activate_pathway',
    'connect',
    'dfs',
    'disconnect',
    'emit_signal',
    'find_path',
    'get_active_pathways',
    'get_layered_structure',
    'get_network_topology',
    'get_neuron_stats',
    'register_neuron',
    'reset_network',
    'route_signal',
    'to_dict',
    'unregister_neuron',
]

神经网络核心
全局神经网络布局的实现
"""

from typing import Any, Dict, List, Optional, Callable, Set, Tuple
from datetime import datetime
from collections import deque
import threading
import uuid
import time

from .signal import Signal, SignalType, SignalBatch, SignalPriority
from .synapse_connection import SynapseConnection, ConnectionType
from .neuron_node import (
    NeuronNode, NeuronType, NeuronState,
    InputNeuron, OutputNeuron, WisdomNeuron, MemoryNeuron
)

class NeuralNetwork:
    """
    神经网络 - 全局功能布局的核心
    
    管理所有神经元节点和突触连接，形成神经网络状态布局
    """
    
    def __init__(self, network_id: str = "somn_global"):
        self.network_id = network_id
        self.created_at = datetime.now()
        
        # 神经元集合
        self.neurons: Dict[str, NeuronNode] = {}
        self.neurons_by_type: Dict[NeuronType, Set[str]] = {
            neuron_type: set() for neuron_type in NeuronType
        }
        
        # 突触连接
        self.synapses: Dict[str, SynapseConnection] = {}
        
        # 信号路由
        self.signal_router: Dict[str, List[str]] = {}  # source -> targets
        
        # 网络状态
        self.is_running = False
        self.signal_queue: deque = deque()
        self.processed_signals = 0
        self.dropped_signals = 0
        
        # 网络统计
        self.network_stats = {
            "total_activations": 0,
            "total_signals": 0,
            "peak_concurrent_signals": 0,
            "avg_signal_latency": 0.0
        }
        
        # 线程安全
        self._lock = threading.RLock()
        self._processing_thread: Optional[threading.Thread] = None
        
        # 回调
        self.on_signal_processed: Optional[Callable] = None
        self.on_neuron_activated: Optional[Callable] = None
    
    def register_neuron(self, neuron: NeuronNode) -> bool:
        """注册神经元"""
        with self._lock:
            if neuron.neuron_id in self.neurons:
                return False
            
            self.neurons[neuron.neuron_id] = neuron
            self.neurons_by_type[neuron.neuron_type].add(neuron.neuron_id)
            return True
    
    def unregister_neuron(self, neuron_id: str) -> bool:
        """注销神经元"""
        with self._lock:
            if neuron_id not in self.neurons:
                return False
            
            neuron = self.neurons[neuron_id]
            self.neurons_by_type[neuron.neuron_type].discard(neuron_id)
            
            # 断开所有连接
            for synapse_id in list(neuron.incoming_synapses.keys()):
                self.disconnect(synapse_id)
            for synapse_id in list(neuron.outgoing_synapses.keys()):
                self.disconnect(synapse_id)
            
            del self.neurons[neuron_id]
            return True
    
    def connect(
        self,
        source_id: str,
        target_id: str,
        connection_type: ConnectionType = ConnectionType.EXCITATORY,
        weight: float = 1.0,
        delay: float = 0.0
    ) -> Optional[SynapseConnection]:
        """创建突触连接"""
        with self._lock:
            if source_id not in self.neurons or target_id not in self.neurons:
                return None
            
            source = self.neurons[source_id]
            target = self.neurons[target_id]
            
            synapse = SynapseConnection(
                source_id=source_id,
                target_id=target_id,
                connection_type=connection_type,
                weight=weight,
                delay=delay
            )
            
            self.synapses[synapse.synapse_id] = synapse
            source.add_outgoing_synapse(synapse)
            target.add_incoming_synapse(synapse)
            
            # 更新路由表
            if source_id not in self.signal_router:
                self.signal_router[source_id] = []
            self.signal_router[source_id].append(target_id)
            
            return synapse
    
    def disconnect(self, synapse_id: str) -> bool:
        """断开连接"""
        with self._lock:
            if synapse_id not in self.synapses:
                return False
            
            synapse = self.synapses[synapse_id]
            source = self.neurons.get(synapse.source_id)
            target = self.neurons.get(synapse.target_id)
            
            if source:
                source.remove_synapse(synapse_id)
            if target:
                target.remove_synapse(synapse_id)
            
            del self.synapses[synapse_id]
            return True
    
    def emit_signal(
        self,
        source_id: str,
        signal_type: SignalType,
        data: Any,
        strength: float = 1.0,
        priority: SignalPriority = SignalPriority.NORMAL,
        metadata: Optional[Dict] = None
    ) -> List[Signal]:
        """
        从指定神经元发射信号
        
        Args:
            source_id: 源神经元ID
            signal_type: 信号类型
            data: 信号数据
            strength: 信号强度
            priority: 优先级
            metadata: 元数据
            
        Returns:
            产生的所有信号列表
        """
        with self._lock:
            if source_id not in self.neurons:
                return []
            
            source = self.neurons[source_id]
            
            # 创建信号
            signal = Signal(
                source_id=source_id,
                signal_type=signal_type,
                data=data,
                strength=strength,
                priority=priority,
                metadata=metadata or {}
            )
            
            # 激活源神经元
            outputs = source.activate(signal)
            
            self.network_stats["total_signals"] += 1
            self.processed_signals += len(outputs)
            
            return outputs
    
    def route_signal(self, signal: Signal) -> List[Signal]:
        """路由信号到目标神经元"""
        with self._lock:
            outputs = []
            
            # 获取路由目标
            targets = self.signal_router.get(signal.source_id, [])
            
            for target_id in targets:
                if target_id in self.neurons:
                    target = self.neurons[target_id]
                    result = target.activate(signal)
                    outputs.extend(result)
            
            return outputs
    
    def activate_pathway(
        self,
        start_id: str,
        signal_type: SignalType,
        data: Any,
        max_depth: int = 5
    ) -> List[Dict]:
        """
        激活一条通路
        
        Args:
            start_id: 起始神经元ID
            signal_type: 信号类型
            data: 信号数据
            max_depth: 最大传播深度
            
        Returns:
            通路激活记录
        """
        if start_id not in self.neurons:
            return []
        
        pathway_log = []
        current_signals = self.emit_signal(start_id, signal_type, data)
        depth = 0
        
        while current_signals and depth < max_depth:
            next_signals = []
            
            for signal in current_signals:
                outputs = self.route_signal(signal)
                next_signals.extend(outputs)
                
                pathway_log.append({
                    "depth": depth,
                    "source": signal.source_id,
                    "type": signal.signal_type.name,
                    "targets": [s.source_id for s in outputs]
                })
            
            current_signals = next_signals
            depth += 1
        
        return pathway_log
    
    def get_network_topology(self) -> Dict:
        """获取网络拓扑结构"""
        with self._lock:
            return {
                "network_id": self.network_id,
                "neuron_count": len(self.neurons),
                "synapse_count": len(self.synapses),
                "neurons_by_type": {
                    neuron_type.name: len(neuron_ids)
                    for neuron_type, neuron_ids in self.neurons_by_type.items()
                },
                "connections": [
                    {
                        "source": s.source_id,
                        "target": s.target_id,
                        "type": s.connection_type.name,
                        "weight": s.weight
                    }
                    for s in self.synapses.values()
                ]
            }
    
    def get_neuron_stats(self) -> Dict[str, Dict]:
        """获取所有神经元统计"""
        with self._lock:
            return {
                neuron_id: neuron.get_stats()
                for neuron_id, neuron in self.neurons.items()
            }
    
    def get_active_pathways(self) -> List[List[str]]:
        """获取活跃通路"""
        with self._lock:
            pathways = []
            visited = set()
            
            def dfs(current_id: str, path: List[str]):
                if current_id in visited or len(path) > 10:
                    return
                
                path.append(current_id)
                neuron = self.neurons.get(current_id)
                
                if neuron and neuron.state in [NeuronState.ACTIVE, NeuronState.EXCITED]:
                    pathways.append(path.copy())
                
                for synapse in neuron.outgoing_synapses.values():
                    dfs(synapse.target_id, path)
                
                path.pop()
            
            for neuron_id in self.neurons:
                dfs(neuron_id, [])
            
            return pathways
    
    def reset_network(self):
        """重置整个网络"""
        with self._lock:
            for neuron in self.neurons.values():
                neuron.reset()
            
            self.signal_queue.clear()
            self.processed_signals = 0
            self.dropped_signals = 0
            self.network_stats = {
                "total_activations": 0,
                "total_signals": 0,
                "peak_concurrent_signals": 0,
                "avg_signal_latency": 0.0
            }
    
    def find_path(
        self,
        start_id: str,
        end_id: str,
        max_depth: int = 10
    ) -> Optional[List[str]]:
        """查找两个神经元之间的路径"""
        if start_id not in self.neurons or end_id not in self.neurons:
            return None
        
        # BFS
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        
        while queue:
            current_id, path = queue.popleft()
            
            if current_id == end_id:
                return path
            
            if len(path) >= max_depth:
                continue
            
            neuron = self.neurons[current_id]
            for synapse in neuron.outgoing_synapses.values():
                if synapse.target_id not in visited:
                    visited.add(synapse.target_id)
                    queue.append((synapse.target_id, path + [synapse.target_id]))
        
        return None
    
    def get_layered_structure(self) -> List[List[str]]:
        """获取分层结构"""
        with self._lock:
            layers = []
            
            # 第一层：输入神经元
            input_layer = list(self.neurons_by_type[NeuronType.INPUT])
            if input_layer:
                layers.append(input_layer)
            
            # 中间层：隐藏神经元
            hidden_layer = list(self.neurons_by_type[NeuronType.HIDDEN])
            if hidden_layer:
                layers.append(hidden_layer)
            
            # 智慧层
            wisdom_layer = list(self.neurons_by_type[NeuronType.WISDOM])
            if wisdom_layer:
                layers.append(wisdom_layer)
            
            # 记忆层
            memory_layer = list(self.neurons_by_type[NeuronType.MEMORY])
            if memory_layer:
                layers.append(memory_layer)
            
            # 输出层
            output_layer = list(self.neurons_by_type[NeuronType.OUTPUT])
            if output_layer:
                layers.append(output_layer)
            
            return layers
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        with self._lock:
            return {
                "network_id": self.network_id,
                "created_at": self.created_at.isoformat(),
                "neurons": [
                    neuron.to_dict() for neuron in self.neurons.values()
                ],
                "topology": self.get_network_topology(),
                "stats": self.network_stats
            }
