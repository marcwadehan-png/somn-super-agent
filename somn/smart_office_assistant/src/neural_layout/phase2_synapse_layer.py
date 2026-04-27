"""
__all__ = [
    'batch_connect',
    'connect',
    'connect_layers',
    'connect_to_layer',
    'create_layer',
    'create_layer_connection_manager',
    'disconnect',
    'find_path',
    'get_all_layers',
    'get_all_neurons',
    'get_layer',
    'get_neuron',
    'get_stats',
    'get_topology',
    'prune_weak_connections',
    'register_layer',
    'register_neuron',
    'route_signal',
    'strengthen_pathway',
    'unregister_neuron',
    'weaken_pathway',
]

Phase 2: 突触连接层构建
层间连接与动态路由系统
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable, Set, Tuple, Union
import uuid
import threading
import heapq

from .signal import Signal, SignalType, SignalBatch, SignalPriority
from .synapse_connection import SynapseConnection, ConnectionType
from .phase1_neuron_standardization import (
    StandardizedNeuron, ActivationContext, ActivationResult, ActivationMode
)

class LayerType(Enum):
    """层类型"""
    INPUT = "input"           # 输入层
    PERCEPTION = "perception" # 感知层
    CORE = "core"             # 核心层
    WISDOM = "wisdom"         # 智慧层
    MEMORY = "memory"         # 记忆层
    OUTPUT = "output"         # 输出层
    FEEDBACK = "feedback"     # 反馈层

class RoutingStrategy(Enum):
    """路由策略"""
    DIRECT = auto()           # 直接路由
    BROADCAST = auto()        # 广播
    WEIGHTED = auto()         # 加权路由
    CONDITIONAL = auto()      # 条件路由
    ADAPTIVE = auto()         # 自适应路由
    SHORTEST_PATH = auto()    # 最短路径
    LOAD_BALANCED = auto()    # 负载均衡

@dataclass
class LayerConfig:
    """层配置"""
    layer_type: LayerType
    layer_id: str
    description: str = ""
    
    # 路由配置
    routing_strategy: RoutingStrategy = RoutingStrategy.DIRECT
    default_connection_type: ConnectionType = ConnectionType.EXCITATORY
    
    # 性能配置
    max_connections_per_neuron: int = 100
    default_weight: float = 1.0
    default_delay: float = 0.0
    
    # 可塑性配置
    plasticity_enabled: bool = True
    learning_rate: float = 0.01
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RoutingDecision:
    """路由决策"""
    source_id: str
    target_id: str
    strategy: RoutingStrategy
    priority: float
    estimated_latency_ms: float
    path_quality: float  # 0.0 - 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class SynapseLayer:
    """
    突触连接层
    
    管理特定层内的神经元连接，提供：
    - 层内神经元管理
    - 层间连接构建
    - 动态路由决策
    - 连接可塑性调整
    """
    
    def __init__(self, config: LayerConfig):
        self.config = config
        self.layer_id = config.layer_id
        self.layer_type = config.layer_type
        
        # 神经元集合
        self.neurons: Dict[str, StandardizedNeuron] = {}
        
        # 连接集合
        self.synapses: Dict[str, SynapseConnection] = {}
        
        # 路由表
        self.routing_table: Dict[str, List[str]] = {}  # source -> [targets]
        self.routing_weights: Dict[Tuple[str, str], float] = {}  # (source, target) -> weight
        self._synapse_lookup: Dict[Tuple[str, str], SynapseConnection] = {}  # 快速查找: (source, target) -> synapse
        
        # 性能统计
        self.stats = {
            "total_synapses": 0,
            "total_routes": 0,
            "avg_path_length": 0.0,
            "routing_decisions": 0,
            "successful_routes": 0
        }
        
        # 线程安全
        self._lock = threading.RLock()
        
        # 路由缓存
        self._route_cache: Dict[str, List[RoutingDecision]] = {}
        self._cache_ttl_seconds = 60
        self._cache_timestamps: Dict[str, datetime] = {}
    
    # ============ 神经元管理 ============
    
    def register_neuron(self, neuron: StandardizedNeuron) -> bool:
        """注册神经元到层"""
        with self._lock:
            if neuron.neuron_id in self.neurons:
                return False
            
            self.neurons[neuron.neuron_id] = neuron
            self.routing_table[neuron.neuron_id] = []
            return True
    
    def unregister_neuron(self, neuron_id: str) -> bool:
        """从层注销神经元"""
        with self._lock:
            if neuron_id not in self.neurons:
                return False
            
            # 断开所有连接
            neuron = self.neurons[neuron_id]
            for synapse_id in list(neuron._incoming_synapses.keys()):
                self.disconnect(synapse_id)
            for synapse_id in list(neuron._outgoing_synapses.keys()):
                self.disconnect(synapse_id)
            
            del self.neurons[neuron_id]
            del self.routing_table[neuron_id]
            
            # 清理路由表中的引用
            for source_id, targets in list(self.routing_table.items()):
                if neuron_id in targets:
                    targets.remove(neuron_id)
            
            return True
    
    def get_neuron(self, neuron_id: str) -> Optional[StandardizedNeuron]:
        """获取神经元"""
        return self.neurons.get(neuron_id)
    
    def get_all_neurons(self) -> List[StandardizedNeuron]:
        """获取所有神经元"""
        return list(self.neurons.values())
    
    # ============ 连接管理 ============
    
    def connect(
        self,
        source_id: str,
        target_id: str,
        connection_type: Optional[ConnectionType] = None,
        weight: Optional[float] = None,
        delay: Optional[float] = None
    ) -> Optional[SynapseConnection]:
        """创建层内连接"""
        with self._lock:
            if source_id not in self.neurons or target_id not in self.neurons:
                return None
            
            source = self.neurons[source_id]
            target = self.neurons[target_id]
            
            # 使用默认配置
            conn_type = connection_type or self.config.default_connection_type
            conn_weight = weight if weight is not None else self.config.default_weight
            conn_delay = delay if delay is not None else self.config.default_delay
            
            # 创建突触
            synapse = SynapseConnection(
                source_id=source_id,
                target_id=target_id,
                connection_type=conn_type,
                weight=conn_weight,
                delay=conn_delay,
                plasticity_enabled=self.config.plasticity_enabled,
                learning_rate=self.config.learning_rate
            )
            
            # 注册连接
            self.synapses[synapse.synapse_id] = synapse
            source.add_outgoing_synapse(synapse)
            target.add_incoming_synapse(synapse)
            
            # 更新路由表
            if source_id not in self.routing_table:
                self.routing_table[source_id] = []
            self.routing_table[source_id].append(target_id)
            
            # 更新权重表
            self.routing_weights[(source_id, target_id)] = conn_weight
            
            # 更新快速查找表
            self._synapse_lookup[(source_id, target_id)] = synapse
            
            self.stats["total_synapses"] += 1
            
            # 清除缓存
            self._invalidate_cache()
            
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
            
            # 更新路由表
            if source and synapse.target_id in self.routing_table.get(synapse.source_id, []):
                self.routing_table[synapse.source_id].remove(synapse.target_id)
            
            # 更新权重表
            self.routing_weights.pop((synapse.source_id, synapse.target_id), None)
            
            # 移除快速查找表
            self._synapse_lookup.pop((synapse.source_id, synapse.target_id), None)
            
            del self.synapses[synapse_id]
            self.stats["total_synapses"] -= 1
            
            # 清除缓存
            self._invalidate_cache()
            
            return True
    
    def batch_connect(
        self,
        connections: List[Tuple[str, str, Optional[ConnectionType], Optional[float]]]
    ) -> List[Optional[SynapseConnection]]:
        """批量创建连接
        
        Args:
            connections: 连接列表，每项为 (source_id, target_id, type, weight)
            
        Returns:
            List[Optional[SynapseConnection]]: 创建的突触连接列表
        """
        results: List[Optional[SynapseConnection]] = []
        for conn in connections:
            source_id, target_id = conn[0], conn[1]
            conn_type = conn[2] if len(conn) > 2 else None
            weight = conn[3] if len(conn) > 3 else None
            
            synapse = self.connect(source_id, target_id, conn_type, weight)
            results.append(synapse)
        
        return results
    
    # ============ 动态路由 ============
    
    def route_signal(
        self,
        source_id: str,
        signal: Signal,
        strategy: Optional[RoutingStrategy] = None
    ) -> List[Tuple[str, Signal]]:
        """路由信号到目标神经元
        
        Args:
            source_id: 源神经元ID
            signal: 要路由的信号
            strategy: 路由策略，默认为层的默认策略
            
        Returns:
            List[Tuple[str, Signal]]: 目标ID和传输后信号的列表
        """
        with self._lock:
            use_strategy = strategy or self.config.routing_strategy
            
            # 获取路由决策
            decisions = self._make_routing_decisions(source_id, signal, use_strategy)
            
            results: List[Tuple[str, Signal]] = []
            for decision in decisions:
                # O(1) 突触查找
                synapse = self._synapse_lookup.get((decision.source_id, decision.target_id))
                
                if synapse:
                    transmitted = synapse.transmit(signal)
                    if transmitted:
                        results.append((decision.target_id, transmitted))
            
            self.stats["routing_decisions"] += 1
            if results:
                self.stats["successful_routes"] += 1
            
            return results
    
    def _make_routing_decisions(
        self,
        source_id: str,
        signal: Signal,
        strategy: RoutingStrategy
    ) -> List[RoutingDecision]:
        """生成路由决策"""
        
        # 检查缓存
        cache_key = f"{source_id}:{strategy.name}:{signal.signal_type.name}"
        if cache_key in self._route_cache:
            cache_time = self._cache_timestamps.get(cache_key)
            if cache_time and (datetime.now() - cache_time).seconds < self._cache_ttl_seconds:
                return self._route_cache[cache_key]
        
        decisions = []
        potential_targets = self.routing_table.get(source_id, [])
        
        if strategy == RoutingStrategy.DIRECT:
            # 直接路由到所有连接的目标
            for target_id in potential_targets:
                weight = self.routing_weights.get((source_id, target_id), 1.0)
                decisions.append(RoutingDecision(
                    source_id=source_id,
                    target_id=target_id,
                    strategy=strategy,
                    priority=weight,
                    estimated_latency_ms=10.0,
                    path_quality=1.0
                ))
        
        elif strategy == RoutingStrategy.BROADCAST:
            # 广播到层内所有神经元
            for target_id in self.neurons.keys():
                if target_id != source_id:
                    decisions.append(RoutingDecision(
                        source_id=source_id,
                        target_id=target_id,
                        strategy=strategy,
                        priority=1.0,
                        estimated_latency_ms=10.0,
                        path_quality=1.0
                    ))
        
        elif strategy == RoutingStrategy.WEIGHTED:
            # 按权重排序路由
            weighted_targets = []
            for target_id in potential_targets:
                weight = self.routing_weights.get((source_id, target_id), 0.0)
                weighted_targets.append((target_id, weight))
            
            # 按权重排序
            weighted_targets.sort(key=lambda x: x[1], reverse=True)
            
            for target_id, weight in weighted_targets:
                decisions.append(RoutingDecision(
                    source_id=source_id,
                    target_id=target_id,
                    strategy=strategy,
                    priority=weight,
                    estimated_latency_ms=10.0,
                    path_quality=weight
                ))
        
        elif strategy == RoutingStrategy.CONDITIONAL:
            # 条件路由
            for target_id in potential_targets:
                # 检查条件（简化实现）
                condition_met = self._evaluate_routing_condition(source_id, target_id, signal)
                if condition_met:
                    weight = self.routing_weights.get((source_id, target_id), 1.0)
                    decisions.append(RoutingDecision(
                        source_id=source_id,
                        target_id=target_id,
                        strategy=strategy,
                        priority=weight,
                        estimated_latency_ms=10.0,
                        path_quality=1.0
                    ))
        
        elif strategy == RoutingStrategy.ADAPTIVE:
            # 自适应路由 - 基于历史性能
            for target_id in potential_targets:
                # 计算自适应分数
                base_weight = self.routing_weights.get((source_id, target_id), 1.0)
                
                # 获取目标神经元统计
                target = self.neurons.get(target_id)
                if target:
                    stats = target.get_stats()
                    success_rate = stats.get("successful_activations", 0) / max(1, stats.get("total_activations", 1))
                    adaptive_score = base_weight * success_rate
                else:
                    adaptive_score = base_weight
                
                decisions.append(RoutingDecision(
                    source_id=source_id,
                    target_id=target_id,
                    strategy=strategy,
                    priority=adaptive_score,
                    estimated_latency_ms=10.0,
                    path_quality=adaptive_score
                ))
            
            # 按自适应分数排序
            decisions.sort(key=lambda x: x.priority, reverse=True)
        
        # 缓存决策
        self._route_cache[cache_key] = decisions
        self._cache_timestamps[cache_key] = datetime.now()
        
        return decisions
    
    def _evaluate_routing_condition(
        self,
        source_id: str,
        target_id: str,
        signal: Signal
    ) -> bool:
        """评估路由条件"""
        # 简化实现：基于信号强度和类型
        if signal.strength < 0.1:
            return False
        
        # 可以扩展更多条件逻辑
        return True
    
    def _invalidate_cache(self) -> None:
        """使路由缓存失效"""
        self._route_cache.clear()
        self._cache_timestamps.clear()
    
    # ============ 层间连接 ============
    
    def connect_to_layer(
        self,
        target_layer: 'SynapseLayer',
        source_neurons: Optional[List[str]] = None,
        target_neurons: Optional[List[str]] = None,
        connection_type: ConnectionType = ConnectionType.EXCITATORY,
        weight: float = 1.0
    ) -> List[SynapseConnection]:
        """连接到目标层
        
        注意：这是跨层连接的概念接口，实际连接需要在网络层面管理
        
        Args:
            target_layer: 目标层
            source_neurons: 源神经元ID列表，None表示全部
            target_neurons: 目标神经元ID列表，None表示全部
            connection_type: 连接类型
            weight: 连接权重
            
        Returns:
            List[SynapseConnection]: 创建的虚拟连接列表
        """
        connections = []
        
        sources = source_neurons or list(self.neurons.keys())
        targets = target_neurons or list(target_layer.neurons.keys())
        
        # 这里只返回连接配置，实际连接由网络层管理
        for source_id in sources:
            for target_id in targets:
                # 创建虚拟连接记录
                synapse = SynapseConnection(
                    source_id=f"{self.layer_id}:{source_id}",
                    target_id=f"{target_layer.layer_id}:{target_id}",
                    connection_type=connection_type,
                    weight=weight
                )
                connections.append(synapse)
        
        return connections
    
    # ============ 可塑性调整 ============
    
    def strengthen_pathway(
        self,
        source_id: str,
        target_id: str,
        amount: float = 0.1
    ) -> bool:
        """增强通路"""
        with self._lock:
            # 查找对应的突触
            for synapse in self.synapses.values():
                if synapse.source_id == source_id and synapse.target_id == target_id:
                    synapse.strengthen(amount)
                    self.routing_weights[(source_id, target_id)] = synapse.weight
                    return True
            return False
    
    def weaken_pathway(
        self,
        source_id: str,
        target_id: str,
        amount: float = 0.1
    ) -> bool:
        """减弱通路"""
        with self._lock:
            for synapse in self.synapses.values():
                if synapse.source_id == source_id and synapse.target_id == target_id:
                    synapse.weaken(amount)
                    self.routing_weights[(source_id, target_id)] = synapse.weight
                    return True
            return False
    
    def prune_weak_connections(self, threshold: float = 0.1) -> int:
        """剪枝弱连接"""
        with self._lock:
            to_remove = []
            
            for synapse_id, synapse in self.synapses.items():
                if synapse.weight < threshold:
                    to_remove.append(synapse_id)
            
            for synapse_id in to_remove:
                self.disconnect(synapse_id)
            
            return len(to_remove)
    
    # ============ 查询接口 ============
    
    def get_stats(self) -> Dict[str, Any]:
        """获取层统计"""
        with self._lock:
            success_rate = (
                self.stats["successful_routes"] / max(1, self.stats["routing_decisions"])
            )
            
            return {
                "layer_id": self.layer_id,
                "layer_type": self.layer_type.value,
                "neuron_count": len(self.neurons),
                "synapse_count": len(self.synapses),
                "routing_strategy": self.config.routing_strategy.name,
                "routing_success_rate": round(success_rate, 4),
                **self.stats
            }
    
    def get_topology(self) -> Dict[str, Any]:
        """获取层拓扑"""
        with self._lock:
            return {
                "layer_id": self.layer_id,
                "layer_type": self.layer_type.value,
                "neurons": [
                    {
                        "neuron_id": n.neuron_id,
                        "name": n.name,
                        "type": n.neuron_type
                    }
                    for n in self.neurons.values()
                ],
                "connections": [
                    {
                        "source": s.source_id,
                        "target": s.target_id,
                        "type": s.connection_type.name,
                        "weight": round(s.weight, 4)
                    }
                    for s in self.synapses.values()
                ]
            }
    
    def find_path(
        self,
        start_id: str,
        end_id: str,
        max_depth: int = 10
    ) -> Optional[List[str]]:
        """查找层内路径
        
        Args:
            start_id: 起始神经元ID
            end_id: 目标神经元ID
            max_depth: 最大搜索深度
            
        Returns:
            Optional[List[str]]: BFS搜索找到的路径，不存在则返回None
        """
        if start_id not in self.neurons or end_id not in self.neurons:
            return None
        
        # BFS
        from collections import deque
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        
        while queue:
            current_id, path = queue.popleft()
            
            if current_id == end_id:
                return path
            
            if len(path) >= max_depth:
                continue
            
            for target_id in self.routing_table.get(current_id, []):
                if target_id not in visited:
                    visited.add(target_id)
                    queue.append((target_id, path + [target_id]))
        
        return None

class LayerConnectionManager:
    """
    层连接管理器
    
    管理多个层之间的连接
    """
    
    def __init__(self):
        self.layers: Dict[str, SynapseLayer] = {}
        self.inter_layer_connections: Dict[str, SynapseConnection] = {}
        self._lock = threading.RLock()
    
    def register_layer(self, layer: SynapseLayer) -> None:
        """注册层"""
        with self._lock:
            self.layers[layer.layer_id] = layer
    
    def connect_layers(
        self,
        source_layer_id: str,
        target_layer_id: str,
        source_neurons: Optional[List[str]] = None,
        target_neurons: Optional[List[str]] = None,
        connection_type: ConnectionType = ConnectionType.EXCITATORY,
        weight: float = 1.0
    ) -> List[SynapseConnection]:
        """连接两个层
        
        Args:
            source_layer_id: 源层ID
            target_layer_id: 目标层ID
            source_neurons: 源神经元列表，None表示全部
            target_neurons: 目标神经元列表，None表示全部
            connection_type: 连接类型
            weight: 权重
            
        Returns:
            List[SynapseConnection]: 创建的突触连接列表
        """
        with self._lock:
            source_layer = self.layers.get(source_layer_id)
            target_layer = self.layers.get(target_layer_id)
            
            if not source_layer or not target_layer:
                return []
            
            connections = []
            sources = source_neurons or list(source_layer.neurons.keys())
            targets = target_neurons or list(target_layer.neurons.keys())
            
            for source_id in sources:
                for target_id in targets:
                    synapse = SynapseConnection(
                        source_id=f"{source_layer_id}:{source_id}",
                        target_id=f"{target_layer_id}:{target_id}",
                        connection_type=connection_type,
                        weight=weight
                    )
                    self.inter_layer_connections[synapse.synapse_id] = synapse
                    connections.append(synapse)
            
            return connections
    
    def get_layer(self, layer_id: str) -> Optional[SynapseLayer]:
        """获取层"""
        return self.layers.get(layer_id)
    
    def get_all_layers(self) -> List[SynapseLayer]:
        """获取所有层"""
        return list(self.layers.values())

# ============ 工厂函数 ============

def create_layer(
    layer_type: LayerType,
    layer_id: str,
    description: str = "",
    routing_strategy: RoutingStrategy = RoutingStrategy.DIRECT
) -> SynapseLayer:
    """创建突触层"""
    config = LayerConfig(
        layer_type=layer_type,
        layer_id=layer_id,
        description=description,
        routing_strategy=routing_strategy
    )
    return SynapseLayer(config)

def create_layer_connection_manager() -> LayerConnectionManager:
    """创建层连接管理器"""
    return LayerConnectionManager()
