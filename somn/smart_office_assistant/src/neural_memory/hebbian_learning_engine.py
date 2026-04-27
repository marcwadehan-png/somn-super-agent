"""
__all__ = [
    'add_concept',
    'add_synapse',
    'clear_history',
    'compute_energy',
    'create_hebbian_engine',
    'export_network',
    'get_associated_concepts',
    'get_association_strength',
    'get_concept',
    'get_effective_activity',
    'get_network_statistics',
    'learn',
    'propagate',
    'recall',
    'store_pattern',
    'strengthen_association',
    'to_dict',
    'update_adaptation',
    'weaken_association',
]

Hebbian关联学习引擎 v1.0
Hebbian Learning Engine v1.0

核心概念mapping:
- Hebb规则 "Cells that fire together, wire together" → 概念关联强化
- STDP时序依赖可塑性 → 学习顺序感知
- 协方差学习 → 反馈调节
- BCM规则 → 动态阈值调整

作者: Somn AI System
日期: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math
from collections import defaultdict
import json

class LearningRule(Enum):
    """学习规则类型"""
    HEBBIAN = "hebbian"                    # 标准Hebb规则
    COVARIANCE = "covariance"              # 协方差学习
    BCM = "bcm"                           # BCM规则
    STDP = "stdp"                         # 时序依赖可塑性
    ANTI_HEBBIAN = "anti_hebbian"         # 反Hebb规则
    COMPETITIVE = "competitive"           # 竞争学习

@dataclass
class Synapse:
    """突触 - 概念之间的连接"""
    source_id: str                        # 源概念ID
    target_id: str                        # 目标概念ID
    weight: float = 0.0                   # 突触权重
    last_update: datetime = field(default_factory=datetime.now)
    
    # 可塑性参数
    eligibility_trace: float = 0.0       # 适任性痕迹 (用于STDP)
    pre_activity: float = 0.0            # 突触前活动
    post_activity: float = 0.0           # 突触后活动
    
    # 历史记录
    update_history: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'weight': self.weight,
            'last_update': self.last_update.isoformat(),
            'eligibility_trace': self.eligibility_trace
        }

@dataclass
class ConceptNode:
    """概念节点 - 对应神经元"""
    concept_id: str                       # 概念ID
    name: str                             # 概念名称
    activity: float = 0.0                 # 当前活动水平 (0-1)
    base_activity: float = 0.5            # 基础活动水平
    
    # 适应参数
    threshold: float = 0.5               # 激活阈值
    adaptation: float = 0.0              # 适应变量
    
    # 统计
    activation_count: int = 0            # 激活次数
    last_activation: Optional[datetime] = None
    
    def get_effective_activity(self) -> float:
        """get有效活动 = 基础活动 - 适应"""
        return max(0, min(1, self.activity - self.adaptation))
    
    def update_adaptation(self, dt: float = 0.1):
        """更新适应 (基于LIF模型的适应机制)"""
        self.adaptation += 0.01 * self.activity * dt
        self.adaptation *= (1 - 0.001 * dt)  # 缓慢恢复

@dataclass
class HebbianLearningResult:
    """Hebbian学习结果"""
    source_id: str
    target_id: str
    old_weight: float
    new_weight: float
    delta_weight: float
    learning_rule: LearningRule
    pre_activity: float
    post_activity: float
    timestamp: datetime

class HebbianLearningEngine:
    """
    Hebbian关联学习引擎
    
    实现<Theoretical Neuroscience>Ch8中的核xinxue习规则
    """
    
    def __init__(self, 
                 learning_rate: float = 0.01,
                 default_rule: LearningRule = LearningRule.COVARIANCE):
        self.learning_rate = learning_rate
        self.default_rule = default_rule
        
        # 网络结构
        self.concepts: Dict[str, ConceptNode] = {}
        self.synapses: Dict[Tuple[str, str], Synapse] = {}
        
        # 统计
        self.mean_activity: Dict[str, float] = defaultdict(lambda: 0.5)
        self.activity_history: Dict[str, List[float]] = defaultdict(list)
        
        # STDP参数
        self.stdp_tau_plus = 20.0
        self.stdp_tau_minus = 20.0
        self.stdp_a_plus = 0.01
        self.stdp_a_minus = 0.012
        
        # BCM参数
        self.bcm_threshold = 0.5
        self.bcm_sliding_window = 100
        
        # 学习历史
        self.learning_history: List[HebbianLearningResult] = []
        
    def add_concept(self, concept_id: str, name: str, 
                   base_activity: float = 0.5) -> ConceptNode:
        """添加概念节点"""
        node = ConceptNode(
            concept_id=concept_id,
            name=name,
            base_activity=base_activity,
            activity=base_activity
        )
        self.concepts[concept_id] = node
        return node
    
    def get_concept(self, concept_id: str) -> Optional[ConceptNode]:
        """get概念节点"""
        return self.concepts.get(concept_id)
    
    def add_synapse(self, source_id: str, target_id: str,
                   initial_weight: float = 0.0) -> Synapse:
        """添加突触连接"""
        synapse = Synapse(
            source_id=source_id,
            target_id=target_id,
            weight=initial_weight
        )
        self.synapses[(source_id, target_id)] = synapse
        return synapse
    
    def learn(self, source_id: str, target_id: str,
              pre_activity: Optional[float] = None,
              post_activity: Optional[float] = None,
              learning_rule: Optional[LearningRule] = None,
              delta_time: Optional[float] = None) -> HebbianLearningResult:
        """执行一次学习"""
        source = self.concepts.get(source_id)
        target = self.concepts.get(target_id)
        
        if source is None or target is None:
            raise ValueError(f"概念不存在: {source_id} or {target_id}")
        
        synapse_key = (source_id, target_id)
        if synapse_key not in self.synapses:
            self.add_synapse(source_id, target_id)
        synapse = self.synapses[synapse_key]
        
        x = pre_activity if pre_activity is not None else source.get_effective_activity()
        y = post_activity if post_activity is not None else target.get_effective_activity()
        
        synapse.pre_activity = x
        synapse.post_activity = y
        
        old_weight = synapse.weight
        rule = learning_rule or self.default_rule
        
        if rule == LearningRule.HEBBIAN:
            delta_w = self._hebbian_rule(x, y)
        elif rule == LearningRule.COVARIANCE:
            delta_w = self._covariance_rule(x, y)
        elif rule == LearningRule.BCM:
            delta_w = self._bcm_rule(x, y)
        elif rule == LearningRule.STDP:
            delta_w = self._stdp_rule(delta_time or 0)
        elif rule == LearningRule.ANTI_HEBBIAN:
            delta_w = self._anti_hebbian_rule(x, y)
        else:
            delta_w = self._hebbian_rule(x, y)
        
        synapse.weight = max(-1, min(1, synapse.weight + delta_w))
        synapse.last_update = datetime.now()
        
        if rule == LearningRule.STDP:
            synapse.eligibility_trace = synapse.weight
        
        self._update_statistics(source_id, x, target_id, y)
        
        result = HebbianLearningResult(
            source_id=source_id,
            target_id=target_id,
            old_weight=old_weight,
            new_weight=synapse.weight,
            delta_weight=synapse.weight - old_weight,
            learning_rule=rule,
            pre_activity=x,
            post_activity=y,
            timestamp=datetime.now()
        )
        
        self.learning_history.append(result)
        return result
    
    def _hebbian_rule(self, x: float, y: float) -> float:
        """标准Hebb规则: Δw = η × x × y"""
        return self.learning_rate * x * y
    
    def _covariance_rule(self, x: float, y: float) -> float:
        """协方差学习: Δw = η × (x - x̄) × (y - ȳ)"""
        x_mean = self.mean_activity.get('default', 0.5)
        y_mean = self.mean_activity.get('default', 0.5)
        return self.learning_rate * (x - x_mean) * (y - y_mean)
    
    def _bcm_rule(self, x: float, y: float) -> float:
        """BCM规则: Δw = η × x × y × (y - θ)"""
        y_effective = max(0, y - self.bcm_threshold)
        return self.learning_rate * x * y_effective * y
    
    def _stdp_rule(self, delta_time: float) -> float:
        """时序依赖可塑性 (STDP)"""
        if delta_time > 0:
            return self.stdp_a_plus * math.exp(-delta_time / self.stdp_tau_plus)
        else:
            return -self.stdp_a_minus * math.exp(delta_time / self.stdp_tau_minus)
    
    def _anti_hebbian_rule(self, x: float, y: float) -> float:
        """反Hebb规则: Δw = -η × x × y"""
        return -self.learning_rate * x * y
    
    def _update_statistics(self, source_id: str, x: float,
                          target_id: str, y: float):
        """更新统计信息"""
        self.activity_history[source_id].append(x)
        self.activity_history[target_id].append(y)
        
        max_history = 1000
        for kid in self.activity_history:
            if len(self.activity_history[kid]) > max_history:
                self.activity_history[kid] = self.activity_history[kid][-max_history:]
        
        for kid, history in self.activity_history.items():
            self.mean_activity[kid] = np.mean(history[-self.bcm_sliding_window:])
    
    def propagate(self, source_id: str, steps: int = 3) -> Dict[str, float]:
        """传播活动"""
        for node in self.concepts.values():
            node.activity = 0
        
        if source_id in self.concepts:
            self.concepts[source_id].activity = 1.0
        
        for step in range(steps):
            new_activities = {}
            
            for target_id, node in self.concepts.items():
                total_input = 0
                for (src, tgt), synapse in self.synapses.items():
                    if tgt == target_id:
                        src_activity = self.concepts[src].activity
                        total_input += src_activity * synapse.weight
                
                new_activities[target_id] = self._activation(total_input)
            
            for kid, activity in new_activities.items():
                self.concepts[kid].activity = activity
        
        return {kid: node.activity for kid, node in self.concepts.items()}
    
    def _activation(self, x: float) -> float:
        """激活函数"""
        return max(0, min(1, x))
    
    def get_association_strength(self, concept_a: str, concept_b: str) -> float:
        """get两个概念之间的关联强度"""
        forward = self.synapses.get((concept_a, concept_b))
        backward = self.synapses.get((concept_b, concept_a))
        
        w1 = forward.weight if forward else 0
        w2 = backward.weight if backward else 0
        
        return (w1 + w2) / 2
    
    def get_associated_concepts(self, concept_id: str, 
                               min_weight: float = 0.1,
                               top_k: int = 10) -> List[Tuple[str, float]]:
        """get与给定概念关联的概念"""
        associations = []
        
        for (src, tgt), synapse in self.synapses.items():
            if abs(synapse.weight) < min_weight:
                continue
            
            if src == concept_id:
                associations.append((tgt, synapse.weight))
            elif tgt == concept_id:
                associations.append((src, synapse.weight))
        
        associations.sort(key=lambda x: abs(x[1]), reverse=True)
        return associations[:top_k]
    
    def strengthen_association(self, concept_a: str, concept_b: str,
                               strength: float = 0.1) -> Synapse:
        """强化两个概念之间的关联"""
        synapse = self.synapses.get((concept_a, concept_b))
        if synapse is None:
            synapse = self.add_synapse(concept_a, concept_b)
        
        synapse.weight = min(1, synapse.weight + strength)
        return synapse
    
    def weaken_association(self, concept_a: str, concept_b: str,
                          strength: float = 0.1) -> Synapse:
        """弱化两个概念之间的关联"""
        synapse = self.synapses.get((concept_a, concept_b))
        if synapse is None:
            synapse = self.add_synapse(concept_a, concept_b)
        
        synapse.weight = max(-1, synapse.weight - strength)
        return synapse
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """get网络统计"""
        weights = [s.weight for s in self.synapses.values()]
        
        return {
            'num_concepts': len(self.concepts),
            'num_synapses': len(self.synapses),
            'total_learning': len(self.learning_history),
            'weight_mean': np.mean(weights) if weights else 0,
            'weight_std': np.std(weights) if weights else 0,
            'weight_max': max(weights) if weights else 0,
            'weight_min': min(weights) if weights else 0,
            'positive_weights': sum(1 for w in weights if w > 0),
            'negative_weights': sum(1 for w in weights if w < 0)
        }
    
    def export_network(self) -> Dict:
        """导出网络结构"""
        return {
            'concepts': {
                kid: {
                    'name': node.name,
                    'activity': node.activity,
                    'base_activity': node.base_activity,
                    'activation_count': node.activation_count
                }
                for kid, node in self.concepts.items()
            },
            'synapses': [s.to_dict() for s in self.synapses.values()],
            'statistics': self.get_network_statistics()
        }
    
    def clear_history(self):
        """清除学习历史"""
        self.learning_history = []

class AttractorMemory:
    """吸引子记忆系统 - 基于Hopfield网络的联想记忆"""
    
    def __init__(self, dimension: int = 100):
        self.dimension = dimension
        self.weights = np.zeros((dimension, dimension))
        self.attractors: Dict[str, np.ndarray] = {}
        self.energy_history: List[float] = []
    
    def store_pattern(self, pattern_id: str, pattern: np.ndarray):
        """存储模式到吸引子"""
        if len(pattern) != self.dimension:
            pattern = self._resize_pattern(pattern)
        
        pattern = pattern / (np.linalg.norm(pattern) + 1e-10)
        self.attractors[pattern_id] = pattern
        
        for i in range(self.dimension):
            for j in range(self.dimension):
                if i != j:
                    self.weights[i, j] += pattern[i] * pattern[j]
    
    def recall(self, probe: np.ndarray, 
               iterations: int = 10) -> Tuple[str, float]:
        """回忆"""
        if len(probe) != self.dimension:
            probe = self._resize_pattern(probe)
        
        state = probe.copy()
        
        for _ in range(iterations):
            new_state = np.zeros_like(state)
            
            for i in range(self.dimension):
                h = np.dot(self.weights[i], state)
                new_state[i] = 1 if h > 0 else -1
            
            state = new_state
            
            for pid, attractor in self.attractors.items():
                if np.array_equal(state, attractor):
                    return pid, 1.0
        
        best_match = None
        best_similarity = 0
        
        for pid, attractor in self.attractors.items():
            similarity = np.dot(state, attractor) / self.dimension
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = pid
        
        return best_match, best_similarity if best_match else 0
    
    def compute_energy(self, state: np.ndarray) -> float:
        """计算能量函数"""
        energy = -0.5 * np.sum(self.weights * np.outer(state, state))
        self.energy_history.append(energy)
        return energy
    
    def _resize_pattern(self, pattern: np.ndarray) -> np.ndarray:
        """调整模式大小"""
        resized = np.zeros(self.dimension)
        n = min(len(pattern), self.dimension)
        resized[:n] = pattern[:n]
        return resized

def create_hebbian_engine(learning_rate: float = 0.01) -> HebbianLearningEngine:
    """创建Hebbian学习引擎"""
    return HebbianLearningEngine(learning_rate)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
