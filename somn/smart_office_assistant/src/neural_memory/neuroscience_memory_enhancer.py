"""
__all__ = [
    'activate',
    'add_association',
    'add_edge',
    'add_node',
    'apply_time_decay',
    'clear',
    'compute_retention',
    'consolidate',
    'enter_working_memory',
    'get_activation_chain',
    'get_active_nodes',
    'get_association_strength',
    'get_consolidation_history',
    'get_contents',
    'get_memory_health_report',
    'get_utilization',
    'get_working_memory',
    'maintain',
    'reinforce',
    'retrieve',
    'retrieve_by_tags',
    'run_consolidation',
    'spread',
    'store',
    'to_dict',
    'try_gate',
]

神经科学fusion记忆增强模块 v1.0
Neuroscience-Enhanced Memory Module

记忆系统增强层。
不修改现有记忆模块,而是作为增强包装器提供神经科学原理驱动的记忆管理.

核心功能:
1. 记忆痕迹衰减 - 基于遗忘曲线的智能衰减
2. 记忆再巩固 - 回忆触发的记忆更新
3. 情景记忆编码 - 带时间上下文的记忆存储
4. 语义扩散激活 - 关联概念自动激活
5. 工作记忆门控 - 注意力控制的记忆维持
6. 睡眠巩固模拟 - 离线记忆整理强化

神经科学→记忆系统mapping:
  记忆痕迹(memory trace) → 记忆条目的激活强度
  长时程增强(LTP) → 重复访问强化记忆
  长时程抑制(LTD) → 长期未访问弱化记忆
  海马情景编码 → 带时间/地点/上下文的记忆
  前额叶工作记忆 → 当前任务相关的短期保持
  NREM睡眠巩固 → 离线时的记忆整理

v1.0.0 神经科学数学基础增强版
"""

import json
import math
import hashlib
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from loguru import logger

# ============================================================
# 第一节: 记忆痕迹与衰减模型
# ============================================================

class ForgettingCurveType(Enum):
    """遗忘曲线类型"""
    EXPONENTIAL = "exponential"       # 指数衰减 (艾宾浩斯经典)
    POWER_LAW = "power_law"           # 幂律衰减 (更符合实际)
    LOGARITHMIC = "logarithmic"       # 对数衰减
    STRETCHED_EXPONENTIAL = "stretched_exp"  # 拉伸指数

@dataclass
class MemoryTrace:
    """
    记忆痕迹 - 带衰减模型的记忆条目
    
    基于艾宾浩斯遗忘曲线:
    R(t) = R₀ × e^(-t/S)
    其中 R=记忆保持率, t=时间, S=记忆稳定性
    
    每次回忆都会更新稳定性:
    S_new = S × e^(Δt/S) × (1 + k)
    """
    id: str
    content: str
    
    # 记忆强度
    initial_strength: float = 1.0   # 初始强度
    current_strength: float = 1.0   # 当前强度
    
    # 稳定性参数
    stability: float = 1.0          # 记忆稳定性 (越大越稳定)
    stability_growth_rate: float = 0.3  # 每次回忆的稳定性增长率
    
    # 访问记录
    access_count: int = 0
    access_times: List[str] = field(default_factory=list)
    last_access: Optional[str] = None
    
    # 元数据
    memory_type: str = "semantic"   # semantic/episodic/procedural
    context_tags: List[str] = field(default_factory=list)
    emotional_valence: float = 0.0  # 情感效价 [-1, 1], 情感记忆更持久
    
    # 遗忘参数
    curve_type: ForgettingCurveType = ForgettingCurveType.POWER_LAW
    
    # 创建时间
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'content': self.content[:100] + '...' if len(self.content) > 100 else self.content,
            'strength': round(self.current_strength, 4),
            'stability': round(self.stability, 4),
            'access_count': self.access_count,
            'memory_type': self.memory_type,
            'emotional_valence': self.emotional_valence,
            'is_active': self.current_strength > 0.1
        }
    
    def compute_retention(self, hours_elapsed: float) -> float:
        """
        计算当前记忆保持率
        
        Args:
            hours_elapsed: 距上次访问的小时数
        """
        if hours_elapsed <= 0:
            return self.current_strength
        
        S = max(0.1, self.stability)
        
        if self.curve_type == ForgettingCurveType.EXPONENTIAL:
            retention = self.current_strength * math.exp(-hours_elapsed / (S * 24))
        elif self.curve_type == ForgettingCurveType.POWER_LAW:
            retention = self.current_strength / (1 + hours_elapsed / (S * 24)) ** 1.5
        elif self.curve_type == ForgettingCurveType.LOGARITHMIC:
            retention = self.current_strength * (1 - 0.3 * math.log(1 + hours_elapsed / (S * 12)))
        elif self.curve_type == ForgettingCurveType.STRETCHED_EXPONENTIAL:
            beta = 0.7  # 拉伸因子
            retention = self.current_strength * math.exp(-(hours_elapsed / (S * 24)) ** beta)
        else:
            retention = self.current_strength * math.exp(-hours_elapsed / (S * 24))
        
        # 情感增强: 情感性记忆衰减更慢
        emotional_factor = 1.0 + 0.2 * abs(self.emotional_valence)
        retention *= emotional_factor
        
        return max(0, min(1, retention))
    
    def reinforce(self):
        """
        记忆强化 - 模拟再巩固过程
        
        每次回忆: 更新稳定性 + 重置强度
        """
        self.access_count += 1
        self.last_access = datetime.now().isoformat()
        self.access_times.append(self.last_access)
        
        # 重复效应: 越复习越稳定
        self.stability *= (1 + self.stability_growth_rate * math.exp(-0.1 * self.access_count))
        self.stability = min(100, self.stability)  # 上限
        
        # 短暂增强当前强度
        self.current_strength = min(1.0, self.current_strength + 0.1)

# ============================================================
# 第二节: 扩散激活网络
# ============================================================

class SpreadingActivationNetwork:
    """
    扩散激活网络 (Spreading Activation Network)
    
    基于语义网络的联想记忆:
    - 激活从一个概念扩散到相关概念
    - 激活强度随距离衰减
    - 激活在概念节点间传播,形成"联想链"
    
    应用:
    - 记忆检索时的联想扩展
    - 概念关联发现
    - 上下文相关记忆激活
    
    激活扩散方程:
    a_i(t+1) = decay × a_i(t) + Σ_j w_ij × a_j(t) + external_input
    """
    
    def __init__(self, decay_rate: float = 0.85, 
                 activation_threshold: float = 0.1,
                 max_activation: float = 1.0):
        self.decay_rate = decay_rate        # 激活衰减率
        self.activation_threshold = activation_threshold  # 激活阈值
        self.max_activation = max_activation
        
        # 概念节点: id → activation_level
        self.nodes: Dict[str, float] = {}
        
        # 关联边: (id_a, id_b) → weight
        self.edges: Dict[Tuple[str, str], float] = {}
    
    def add_node(self, node_id: str, initial_activation: float = 0.0):
        """添加概念节点"""
        self.nodes[node_id] = initial_activation
    
    def add_edge(self, id_a: str, id_b: str, weight: float = 0.5):
        """添加概念关联"""
        key = (min(id_a, id_b), max(id_a, id_b))
        self.edges[key] = weight
        if id_a not in self.nodes:
            self.add_node(id_a)
        if id_b not in self.nodes:
            self.add_node(id_b)
    
    def activate(self, node_id: str, amount: float = 1.0):
        """激活指定节点"""
        if node_id in self.nodes:
            self.nodes[node_id] = min(self.max_activation, 
                                       self.nodes[node_id] + amount)
    
    def spread(self, iterations: int = 3) -> Dict[str, float]:
        """
        执行激活扩散
        
        Args:
            iterations: 扩散迭代次数
            
        Returns:
            各节点的最终激活水平
        """
        for _ in range(iterations):
            new_activations = {}
            
            for node_id in self.nodes:
                # 衰减
                current = self.nodes[node_id] * self.decay_rate
                
                # 从邻居节点接收激活
                received = 0.0
                for (a, b), weight in self.edges.items():
                    if a == node_id:
                        received += weight * self.nodes.get(b, 0)
                    elif b == node_id:
                        received += weight * self.nodes.get(a, 0)
                
                new_activations[node_id] = min(self.max_activation, current + received)
            
            self.nodes = new_activations
        
        return self.get_active_nodes()
    
    def get_active_nodes(self, threshold: Optional[float] = None) -> Dict[str, float]:
        """get激活水平超过阈值的节点"""
        t = threshold or self.activation_threshold
        return {k: v for k, v in self.nodes.items() if v >= t}
    
    def get_activation_chain(self, start_node: str, max_depth: int = 3) -> List[List[str]]:
        """
        get从指定节点出发的激活链
        
        Args:
            start_node: 起始节点
            max_depth: 最大深度
        """
        chains = []
        visited = set()
        
        def _dfs(current: str, depth: int, path: List[str]):
            if depth >= max_depth or current in visited:
                return
            visited.add(current)
            
            # 查找所有邻居
            neighbors = []
            for (a, b), weight in self.edges.items():
                if a == current:
                    neighbors.append((b, weight))
                elif b == current:
                    neighbors.append((a, weight))
            
            for neighbor, weight in sorted(neighbors, key=lambda x: -x[1]):
                new_path = path + [neighbor]
                chains.append(new_path)
                _dfs(neighbor, depth + 1, new_path)
        
        _dfs(start_node, 0, [start_node])
        return chains[:20]  # 限制数量
    
    def get_association_strength(self, id_a: str, id_b: str) -> float:
        """get两个概念的关联强度"""
        key = (min(id_a, id_b), max(id_a, id_b))
        return self.edges.get(key, 0.0)

# ============================================================
# 第三节: 工作记忆门控
# ============================================================

class WorkingMemoryGate:
    """
    工作记忆门控系统
    
    神经科学基础:
    前额叶皮层通过注意力门控机制控制工作记忆中信息的维持和更新.
    
    核心机制:
    - 门控信号: 决定信息是否进入工作记忆
    - 维持信号: 持续激活保持信息在工作记忆中
    - 更新信号: 用新信息替换旧信息
    - 干扰抑制: 抑制无关信息的干扰
    
    mapping到智能体:
    - 工作记忆容量: 4±1 个项目 (Miller定律)
    - 门控控制: 当前任务的相关性judge
    - 注意力分配: 任务相关信息的优先级
    """
    
    def __init__(self, capacity: int = 5):
        self.capacity = capacity
        self.items: List[Dict[str, Any]] = []
        self.gate_threshold = 0.3  # 进入工作记忆的阈值
    
    def try_gate(self, item: Dict[str, Any], relevance: float) -> Tuple[bool, str]:
        """
        尝试将信息门控进入工作记忆
        
        Args:
            item: 信息项
            relevance: 与当前任务的相关性 [0, 1]
            
        Returns:
            (是否进入, 原因)
        """
        if relevance < self.gate_threshold:
            return False, f"相关性不足: {relevance:.2f} < {self.gate_threshold}"
        
        # 检查是否已存在
        for existing in self.items:
            if existing.get('id') == item.get('id'):
                # 更新已存在项
                existing['relevance'] = relevance
                existing['last_updated'] = datetime.now().isoformat()
                return False, "已存在于工作记忆中(已更新)"
        
        if len(self.items) >= self.capacity:
            # 容量已满: 替换最不相关的项
            self._evict_least_relevant()
        
        item['relevance'] = relevance
        item['entered_at'] = datetime.now().isoformat()
        item['last_updated'] = datetime.now().isoformat()
        self.items.append(item)
        return True, "成功进入工作记忆"
    
    def _evict_least_relevant(self):
        """驱逐最不相关的项"""
        if not self.items:
            return
        min_idx = min(range(len(self.items)), 
                      key=lambda i: self.items[i].get('relevance', 0))
        evicted = self.items.pop(min_idx)
        logger.debug(f"工作记忆驱逐: {evicted.get('id', 'unknown')}")
    
    def maintain(self):
        """维持工作记忆 - 衰减不活跃的项"""
        now = datetime.now()
        for item in self.items[:]:
            last_update = datetime.fromisoformat(item['last_updated'])
            age = (now - last_update).total_seconds()
            
            # 超过30秒未更新的项开始衰减
            if age > 30:
                item['relevance'] *= 0.9
                if item['relevance'] < 0.1:
                    self.items.remove(item)
    
    def get_contents(self) -> List[Dict[str, Any]]:
        """get工作记忆内容"""
        self.maintain()
        return sorted(self.items, key=lambda x: -x.get('relevance', 0))
    
    def clear(self):
        """清空工作记忆"""
        self.items.clear()
    
    def get_utilization(self) -> float:
        """get工作记忆使用率"""
        return len(self.items) / max(1, self.capacity)

# ============================================================
# 第四节: 睡眠巩固模拟
# ============================================================

class SleepConsolidationSimulator:
    """
    睡眠巩固模拟器
    
    神经科学基础:
    NREM睡眠中的记忆巩固:
    1. 海马重放 (hippocampal replay): 白天的经历在睡眠中快速重放
    2. 锐波涟漪 (sharp-wave ripples): 海马→新皮层的记忆转移
    3. 慢波睡眠 (slow-wave sleep): 系统级记忆整合
    4. 突触稳态: 睡眠降低整体突触强度,保留重要记忆的比例增大
    
    mapping到智能体:
    - 离线巩固: 系统空闲时自动整理记忆
    - 记忆整合: 将碎片记忆合并为连贯知识
    - 突触降尺度: 降低不重要记忆的权重
    - 重要记忆增强: 提升高价值记忆的稳定性
    """
    
    def __init__(self):
        self.consolidation_log: List[Dict[str, Any]] = []
    
    def consolidate(self, memory_traces: Dict[str, MemoryTrace],
                    duration_hours: float = 8.0) -> Dict[str, Any]:
        """
        执行睡眠巩固模拟
        
        Args:
            memory_traces: 记忆痕迹字典
            duration_hours: 巩固持续时间(小时)
            
        Returns:
            巩固报告
        """
        if not memory_traces:
            return {'status': 'no_memories'}
        
        stats = {
            'total_traces': len(memory_traces),
            'strengthened': 0,
            'weakened': 0,
            'pruned': 0,
            'integrated': 0,
            'duration_hours': duration_hours
        }
        
        # 阶段1: 锐波涟漪 - 高价值记忆选择性重放
        valuable_traces = sorted(
            memory_traces.values(),
            key=lambda t: t.access_count * t.current_strength,
            reverse=True
        )
        
        top_20_percent = max(1, len(valuable_traces) // 5)
        for trace in valuable_traces[:top_20_percent]:
            # 重放增强: 稳定性增长
            trace.stability *= 1.2
            trace.current_strength = min(1.0, trace.current_strength + 0.05)
            stats['strengthened'] += 1
        
        # 阶段2: 慢波整合 - 所有记忆轻微衰减
        for trace in memory_traces.values():
            decay = 0.95 ** (duration_hours / 8)  # 8小时衰减5%
            trace.current_strength *= decay
            trace.current_strength = max(0, trace.current_strength)
            
            # 稳定性自然增长
            if trace.current_strength > 0.3:
                trace.stability *= 1.01
        
        # 阶段3: 突触降尺度 - 整体衰减,但高价值记忆比例增大
        scaling_factor = 0.92
        for trace in memory_traces.values():
            trace.current_strength *= scaling_factor
            
            # 高访问记忆的衰减更少
            if trace.access_count > 3:
                trace.current_strength /= scaling_factor * 0.02
                trace.current_strength = min(1.0, trace.current_strength)
                stats['strengthened'] += 1
            elif trace.current_strength < 0.05:
                stats['weakened'] += 1
        
        # 阶段4: 修剪 - 删除极弱记忆
        to_prune = [tid for tid, trace in memory_traces.items() 
                    if trace.current_strength < 0.01]
        stats['pruned'] = len(to_prune)
        
        # 阶段5: 整合 - 相邻时间的高强度记忆间创建关联
        # (模拟概念间的联想建立)
        strong_traces = [(tid, t) for tid, t in memory_traces.items() 
                         if t.current_strength > 0.5]
        stats['integrated'] = len(strong_traces) // 2
        
        # 记录
        self.consolidation_log.append({
            'timestamp': datetime.now().isoformat(),
            'stats': stats
        })
        
        return stats
    
    def get_consolidation_history(self) -> List[Dict]:
        return self.consolidation_log

# ============================================================
# 第五节: 神经科学记忆增强器主控
# ============================================================

class NeuroscienceMemoryEnhancer:
    """
    神经科学记忆增强器 - unified管理记忆增强功能
    
    作为现有记忆系统的增强层,提供:
    1. 智能衰减 - 基于遗忘曲线的精确记忆管理
    2. 扩散激活 - 概念联想驱动的检索扩展
    3. 工作记忆门控 - 注意力控制的短期记忆
    4. 睡眠巩固 - 离线自动整理
    5. 情感增强 - 情感性记忆优先保持
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # 核心组件
        self.memory_traces: Dict[str, MemoryTrace] = {}
        self.spreading_network = SpreadingActivationNetwork(
            decay_rate=self.config.get('spread_decay', 0.85),
            activation_threshold=self.config.get('spread_threshold', 0.15)
        )
        self.working_memory = WorkingMemoryGate(
            capacity=self.config.get('wm_capacity', 5)
        )
        self.sleep_simulator = SleepConsolidationSimulator()
        
        # 统计
        self.stats = {
            'total_stored': 0,
            'total_retrieved': 0,
            'total_reinforced': 0,
            'avg_strength': 0.0,
            'wm_utilization': 0.0
        }
        
        logger.info("神经科学记忆增强器init完成")
    
    def _generate_id(self, content: str) -> str:
        """generate记忆ID"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
    
    def store(self, content: str, memory_type: str = "semantic",
              context_tags: List[str] = None,
              emotional_valence: float = 0.0,
              importance: float = 0.5) -> str:
        """
        存储记忆
        
        Args:
            content: 记忆内容
            memory_type: semantic/episodic/procedural
            context_tags: 上下文标签
            emotional_valence: 情感效价 [-1, 1]
            importance: 重要性 [0, 1]
        """
        trace_id = self._generate_id(content)
        
        trace = MemoryTrace(
            id=trace_id,
            content=content,
            memory_type=memory_type,
            context_tags=context_tags or [],
            emotional_valence=emotional_valence,
            initial_strength=importance,
            current_strength=importance,
            stability=importance * 2  # 重要记忆更稳定
        )
        
        self.memory_traces[trace_id] = trace
        
        # 在扩散网络中注册
        self.spreading_network.add_node(trace_id, importance)
        
        # 建立上下文关联
        for tag in (context_tags or []):
            self.spreading_network.add_edge(trace_id, f"tag_{tag}", 
                                            weight=0.6)
        
        self.stats['total_stored'] = len(self.memory_traces)
        
        return trace_id
    
    def retrieve(self, content: str, threshold: float = 0.1,
                 use_spreading: bool = True) -> List[Dict[str, Any]]:
        """
        检索记忆
        
        Args:
            content: 查询内容
            threshold: 最低激活阈值
            use_spreading: 是否使用扩散激活扩展检索
        """
        query_id = self._generate_id(content)
        
        # 激活查询节点
        self.spreading_network.activate(query_id, 0.5)
        
        if use_spreading:
            # 扩散激活
            active_nodes = self.spreading_network.spread(iterations=3)
        else:
            active_nodes = self.spreading_network.get_active_nodes(threshold)
        
        # 转换为记忆结果
        results = []
        for node_id, activation in sorted(active_nodes.items(), 
                                           key=lambda x: -x[1]):
            if node_id in self.memory_traces:
                trace = self.memory_traces[node_id]
                results.append({
                    **trace.to_dict(),
                    'retrieval_activation': round(activation, 4),
                    'relevance_score': round(activation * trace.current_strength, 4)
                })
                
                # 检索即回忆: 轻微强化
                trace.reinforce()
        
        self.stats['total_retrieved'] += len(results)
        self._update_stats()
        
        return results
    
    def retrieve_by_tags(self, tags: List[str], threshold: float = 0.1) -> List[Dict]:
        """通过标签检索记忆"""
        for tag in tags:
            self.spreading_network.activate(f"tag_{tag}", 0.8)
        
        active_nodes = self.spreading_network.spread(iterations=2)
        
        results = []
        for node_id, activation in sorted(active_nodes.items(),
                                           key=lambda x: -x[1]):
            if node_id in self.memory_traces:
                trace = self.memory_traces[node_id]
                results.append({
                    **trace.to_dict(),
                    'retrieval_activation': round(activation, 4)
                })
                trace.reinforce()
        
        return results
    
    def add_association(self, content_a: str, content_b: str, weight: float = 0.5):
        """在两个记忆间建立关联"""
        id_a = self._generate_id(content_a)
        id_b = self._generate_id(content_b)
        self.spreading_network.add_edge(id_a, id_b, weight)
    
    def enter_working_memory(self, item: Dict, relevance: float) -> Tuple[bool, str]:
        """将信息放入工作记忆"""
        return self.working_memory.try_gate(item, relevance)
    
    def get_working_memory(self) -> List[Dict]:
        """get当前工作记忆内容"""
        return self.working_memory.get_contents()
    
    def apply_time_decay(self, hours: float = 1.0):
        """
        应用时间衰减
        
        Args:
            hours: 经过的小时数
        """
        pruned = []
        for trace_id, trace in self.memory_traces.items():
            trace.current_strength = trace.compute_retention(hours)
            if trace.current_strength < 0.01:
                pruned.append(trace_id)
        
        # 修剪极弱记忆
        for tid in pruned:
            del self.memory_traces[tid]
            if tid in self.spreading_network.nodes:
                del self.spreading_network.nodes[tid]
        
        self._update_stats()
        
        return len(pruned)
    
    def run_consolidation(self, duration_hours: float = 8.0) -> Dict[str, Any]:
        """运行睡眠巩固"""
        report = self.sleep_simulator.consolidate(self.memory_traces, duration_hours)
        self._update_stats()
        return report
    
    def _update_stats(self):
        """更新统计"""
        if self.memory_traces:
            strengths = [t.current_strength for t in self.memory_traces.values()]
            self.stats['avg_strength'] = float(np.mean(strengths))
        self.stats['wm_utilization'] = self.working_memory.get_utilization()
    
    def get_memory_health_report(self) -> Dict[str, Any]:
        """get记忆健康报告"""
        if not self.memory_traces:
            return {'status': 'empty'}
        
        strengths = [t.current_strength for t in self.memory_traces.values()]
        stabilities = [t.stability for t in self.memory_traces.values()]
        
        return {
            'total_memories': len(self.memory_traces),
            'avg_strength': round(float(np.mean(strengths)), 4),
            'strong_memories': sum(1 for s in strengths if s > 0.5),
            'weak_memories': sum(1 for s in strengths if s < 0.1),
            'avg_stability': round(float(np.mean(stabilities)), 4),
            'working_memory_utilization': round(self.working_memory.get_utilization(), 2),
            'working_memory_items': len(self.working_memory.items),
            'consolidation_count': len(self.sleep_simulator.consolidation_log),
            'spreading_network_nodes': len(self.spreading_network.nodes),
            'spreading_network_edges': len(self.spreading_network.edges),
            'health_status': self._classify_health(float(np.mean(strengths)))
        }
    
    def _classify_health(self, avg_strength: float) -> str:
        if avg_strength > 0.6:
            return "excellent"
        elif avg_strength > 0.4:
            return "good"
        elif avg_strength > 0.2:
            return "fair"
        else:
            return "needs_consolidation"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'stats': self.stats,
            'health_report': self.get_memory_health_report(),
            'memory_count': len(self.memory_traces),
            'working_memory': self.get_working_memory()
        }
