"""
__all__ = [
    'add_item',
    'allocate',
    'allocate_attention',
    'apply',
    'available',
    'boost_item',
    'compute',
    'create_attention_system',
    'gate_attention',
    'get_attention_weights',
    'get_item_rate',
    'get_normalized_rate',
    'get_statistics',
    'get_top_attended',
    'inhibit_item',
    'quick_attend',
    'reallocate',
    'release',
    'release_attention',
    'schedule',
    'sigmoid',
    'simulate_attention_shift',
    'update',
    'update_rate',
    'visualize_attention',
]

发放率注意力分配系统 v1.0
Firing Rate Attention System v1.0

核心概念mapping:
- 发放率 → 知识/任务的激活强度
- 注意力资源分配 → 计算资源调度
- 竞争抑制 → 选择性激活
- 侧抑制 → 概念间的竞争

作者: Somn AI System
日期: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math
from collections import defaultdict

class AttentionType(Enum):
    """注意力类型"""
    SPARSE = "sparse"              # 稀疏注意力
    DIVISIBLE = "divisible"        # 可分注意力
    SELECTIVE = "selective"       # 选择性注意
    SUSTAINED = "sustained"        # 持续注意
    ALTERNATING = "alternating"    # 交替注意

@dataclass
class AttentionResource:
    """注意力资源"""
    total_capacity: float = 100.0   # 总容量
    current_load: float = 0.0       # 当前负载
    allocated_items: Dict[str, float] = field(default_factory=dict)  # 已分配项
    
    def available(self) -> float:
        """可用资源"""
        return max(0, self.total_capacity - self.current_load)
    
    def allocate(self, item_id: str, amount: float) -> bool:
        """分配资源"""
        if amount > self.available():
            return False
        self.allocated_items[item_id] = amount
        self.current_load += amount
        return True
    
    def release(self, item_id: str):
        """释放资源"""
        if item_id in self.allocated_items:
            self.current_load -= self.allocated_items[item_id]
            del self.allocated_items[item_id]

@dataclass
class FiringRateItem:
    """发放率项目 - 知识/任务的激活表示"""
    item_id: str
    name: str
    
    # 发放率参数
    base_rate: float = 10.0          # 基础发放率 (Hz)
    current_rate: float = 0.0        # 当前发放率
    max_rate: float = 100.0         # 最大发放率
    
    # 时间常数
    tau_on: float = 20.0            # 激活时间常数 (ms)
    tau_off: float = 50.0           # 抑制时间常数 (ms)
    
    # 适应
    adaptation: float = 0.0         # 适应水平
    adaptation_rate: float = 0.01   # 适应速率
    
    # 竞争
    competitive_threshold: float = 0.5  # 竞争阈值
    lateral_inhibition: float = 0.1    # 侧抑制强度
    
    # 统计
    activation_count: int = 0
    last_activation: Optional[datetime] = None
    
    def update_rate(self, input_current: float, dt: float = 1.0):
        """更新发放率"""
        # 适应调节
        adaptation_factor = 1.0 / (1 + self.adaptation)
        
        # 简单的LIFstyle更新
        if input_current > self.competitive_threshold:
            # 激活
            dr = (self.base_rate * input_current * adaptation_factor - self.current_rate) / self.tau_on
        else:
            # 抑制
            dr = -self.current_rate / self.tau_off
        
        self.current_rate = max(0, min(self.max_rate, self.current_rate + dr * dt))
        
        # 更新适应
        if self.current_rate > self.base_rate:
            self.adaptation += self.adaptation_rate * (self.current_rate - self.base_rate)
        
        # 适应恢复
        self.adaptation *= (1 - 0.001 * dt)
        
        # 更新统计
        if self.current_rate > self.base_rate * 0.5:
            self.activation_count += 1
            self.last_activation = datetime.now()
    
    def get_normalized_rate(self) -> float:
        """get归一化发放率"""
        return self.current_rate / self.max_rate if self.max_rate > 0 else 0

class WinnerTakeAll:
    """
    赢者通吃网络 - 选择性注意力的神经机制
    
    基于竞争学习的原理:
    1. 所有单元竞争
    2. 最强单元获胜
    3. 获胜单元抑制其他单元
    """
    
    def __init__(self, k: int = 1, inhibition_strength: float = 0.1):
        """
        Args:
            k: 赢者数量
            inhibition_strength: 抑制强度
        """
        self.k = k
        self.inhibition_strength = inhibition_strength
        self.activations: Dict[str, float] = {}
    
    def compute(self, items: List[Tuple[str, float]], 
                threshold: float = 0.0) -> List[str]:
        """
        计算赢者
        
        Args:
            items: [(id, activation), ...]
            threshold: 激活阈值
            
        Returns:
            List[str]: 赢者的ID列表
        """
        # 更新激活
        for item_id, activation in items:
            if item_id not in self.activations:
                self.activations[item_id] = 0
            
            # 侧抑制: 其他单元的激活会抑制当前单元
            inhibition = sum(
                max(0, other_act - activation) 
                for other_id, other_act in items 
                if other_id != item_id
            ) * self.inhibition_strength
            
            self.activations[item_id] = max(0, activation - inhibition)
        
        # 选择赢者
        sorted_items = sorted(
            [(id, act) for id, act in self.activations.items() if act > threshold],
            key=lambda x: x[1],
            reverse=True
        )
        
        return [item[0] for item in sorted_items[:self.k]]

class LateralInhibition:
    """
    侧抑制网络 - 增强对比度和选择性
    
    原理: 相邻神经元相互抑制,增强对比
    """
    
    def __init__(self, inhibition_matrix: Optional[np.ndarray] = None):
        self.inhibition_matrix = inhibition_matrix
    
    def apply(self, activations: np.ndarray) -> np.ndarray:
        """应用侧抑制"""
        if self.inhibition_matrix is None:
            # 自动generate: 邻域抑制
            n = len(activations)
            inh = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    if i != j:
                        dist = abs(i - j)
                        inh[i, j] = math.exp(-dist / 2) * 0.1
            self.inhibition_matrix = inh
        
        # 抑制
        inhibition = np.dot(self.inhibition_matrix, activations)
        return np.maximum(0, activations - inhibition * 0.1)

class AttentionGate:
    """
    注意力门控 - 基于门控机制的注意力控制
    
    类比LSTM的门控机制:
    - Input gate: 控制新信息的流入
    - Forget gate: 控制旧信息的保留
    - Output gate: 控制输出
    """
    
    def __init__(self, hidden_dim: int = 64):
        self.hidden_dim = hidden_dim
        
        # 简化的门控参数
        self.input_weight = 0.3
        self.forget_weight = 0.2
        self.output_weight = 0.4
    
    def compute(self, current_state: float, 
                new_input: float,
                previous_memory: float = 0.0) -> Tuple[float, float]:
        """
        计算门控
        
        Returns:
            (output, new_memory)
        """
        # 简化的sigmoid门控
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        
        # Input gate
        input_gate = sigmoid(self.input_weight * new_input)
        
        # Forget gate
        forget_gate = sigmoid(self.forget_weight * previous_memory)
        
        # Output gate
        output_gate = sigmoid(self.output_weight * (forget_gate * previous_memory + 
                                                      input_gate * new_input))
        
        # New memory
        new_memory = forget_gate * previous_memory + input_gate * new_input
        
        # Output
        output = output_gate * new_memory
        
        return output, new_memory

class FiringRateAttentionSystem:
    """
    发放率注意力分配系统
    
    整合<Theoretical Neuroscience>的核心理论:
    1. 发放率模型 - 知识激活强度
    2. 竞争机制 - 赢者通吃
    3. 侧抑制 - 增强对比
    4. 注意力门控 - 资源分配
    5. 适应机制 - 避免饱和
    """
    
    def __init__(self, total_capacity: float = 100.0):
        self.items: Dict[str, FiringRateItem] = {}
        self.resources = AttentionResource(total_capacity=total_capacity)
        
        # 竞争网络
        self.wta = WinnerTakeAll(k=1, inhibition_strength=0.2)
        self.lateral_inhibition = LateralInhibition()
        
        # 注意力门控
        self.gate = AttentionGate()
        
        # 时间追踪
        self.time = 0
        self.dt = 1.0  # ms
        
        # 历史记录
        self.activation_history: Dict[str, List[float]] = defaultdict(list)
        
    def add_item(self, item_id: str, name: str,
                base_rate: float = 10.0,
                priority: float = 0.5) -> FiringRateItem:
        """添加注意力项目"""
        item = FiringRateItem(
            item_id=item_id,
            name=name,
            base_rate=base_rate,
            competitive_threshold=1.0 - priority
        )
        self.items[item_id] = item
        return item
    
    def allocate_attention(self, item_id: str, amount: float) -> bool:
        """分配注意力资源"""
        if item_id not in self.items:
            return False
        return self.resources.allocate(item_id, amount)
    
    def release_attention(self, item_id: str):
        """释放注意力资源"""
        self.resources.release(item_id)
    
    def update(self, inputs: Dict[str, float], dt: Optional[float] = None):
        """
        更新所有项目的发放率
        
        Args:
            inputs: {item_id: input_current}
            dt: 时间步长
        """
        dt = dt or self.dt
        
        # 计算竞争输入
        item_activations = []
        for item_id, item in self.items.items():
            input_current = inputs.get(item_id, 0)
            
            # 添加侧抑制效应
            lateral_effect = 0
            for other_id, other_item in self.items.items():
                if other_id != item_id:
                    diff = other_item.current_rate - item.current_rate
                    if diff > 0:
                        lateral_effect += item.lateral_inhibition * diff
            
            # 竞争调节后的输入
            competitive_input = input_current - lateral_effect
            
            # 更新发放率
            item.update_rate(competitive_input, dt)
            
            item_activations.append((item_id, item.current_rate))
        
        # 赢者通吃: 增强获胜者
        winners = self.wta.compute(item_activations, threshold=5.0)
        if winners:
            winner_id = winners[0]
            if winner_id in self.items:
                self.items[winner_id].current_rate *= 1.2  # 增强20%
        
        # 记录历史
        for item_id, item in self.items.items():
            self.activation_history[item_id].append(item.current_rate)
            # 限制历史长度
            if len(self.activation_history[item_id]) > 1000:
                self.activation_history[item_id] = self.activation_history[item_id][-1000:]
        
        self.time += dt
    
    def get_attention_weights(self) -> Dict[str, float]:
        """get注意力权重"""
        total = sum(item.current_rate for item in self.items.values())
        if total == 0:
            return {kid: 0 for kid in self.items}
        
        return {
            kid: item.current_rate / total 
            for kid, item in self.items.items()
        }
    
    def get_top_attended(self, k: int = 5) -> List[Tuple[str, float]]:
        """get前k个最被注意的项目"""
        weights = self.get_attention_weights()
        sorted_items = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:k]
    
    def get_item_rate(self, item_id: str) -> float:
        """get项目的发放率"""
        if item_id not in self.items:
            return 0
        return self.items[item_id].current_rate
    
    def get_normalized_rate(self, item_id: str) -> float:
        """get归一化发放率"""
        if item_id not in self.items:
            return 0
        return self.items[item_id].get_normalized_rate()
    
    def inhibit_item(self, item_id: str, amount: float = 0.5):
        """抑制某个项目"""
        if item_id in self.items:
            self.items[item_id].current_rate *= (1 - amount)
    
    def boost_item(self, item_id: str, amount: float = 0.5):
        """增强某个项目"""
        if item_id in self.items:
            self.items[item_id].current_rate *= (1 + amount)
    
    def gate_attention(self, item_id: str, 
                      new_input: float,
                      previous_memory: float = 0.0) -> Tuple[float, float]:
        """使用门控机制处理注意力"""
        if item_id not in self.items:
            return 0, 0
        
        item = self.items[item_id]
        return self.gate.compute(
            item.current_rate,
            new_input,
            previous_memory
        )
    
    def simulate_attention_shift(self, 
                                from_item: str,
                                to_item: str,
                                duration: int = 100) -> Dict[str, List[float]]:
        """
        模拟注意力转移
        
        Args:
            from_item: 原注意项目
            to_item: 目标项目
            duration: 持续时间(ms)
            
        Returns:
            转移过程的发放率变化
        """
        history = {from_item: [], to_item: []}
        
        for t in range(0, duration, int(self.dt)):
            # 输入: 逐渐降低from_item, 逐渐提高to_item
            progress = t / duration
            
            inputs = {
                from_item: 1.0 * (1 - progress),
                to_item: 0.2 * progress
            }
            
            self.update(inputs)
            
            if from_item in self.items:
                history[from_item].append(self.items[from_item].current_rate)
            if to_item in self.items:
                history[to_item].append(self.items[to_item].current_rate)
        
        return history
    
    def get_statistics(self) -> Dict[str, Any]:
        """get统计信息"""
        rates = [item.current_rate for item in self.items.values()]
        
        return {
            'num_items': len(self.items),
            'total_rate': sum(rates),
            'mean_rate': np.mean(rates) if rates else 0,
            'max_rate': max(rates) if rates else 0,
            'resource_usage': self.resources.current_load / self.resources.total_capacity,
            'available_resources': self.resources.available(),
            'top_attended': self.get_top_attended(3)
        }
    
    def visualize_attention(self) -> Dict[str, Any]:
        """可视化注意力分布"""
        weights = self.get_attention_weights()
        
        return {
            'weights': weights,
            'bars': [
                {'item': kid, 'weight': w, 'rate': self.items[kid].current_rate}
                for kid, w in sorted(weights.items(), key=lambda x: x[1], reverse=True)
                if kid in self.items
            ],
            'winners': self.wta.compute(
                [(k, v.current_rate) for k, v in self.items.items()],
                threshold=5.0
            )
        }

class AttentionScheduler:
    """
    注意力调度器 - 动态分配注意力资源
    
    基于<Theoretical Neuroscience>的信息论原理:
    - 有限资源必须有效分配
    - 优先处理高信息量项目
    """
    
    def __init__(self, attention_system: FiringRateAttentionSystem):
        self.attention = attention_system
        
        # 调度参数
        self.reallocation_interval = 50  # 重分配间隔 (ms)
        self.min_attention = 5.0        # 最小注意力
        self.priority_decay = 0.95       # 优先级衰减
    
    def schedule(self, tasks: List[Dict[str, Any]], 
                current_time: float) -> Dict[str, float]:
        """
        调度注意力
        
        Args:
            tasks: 任务列表 [{id, priority, estimated_time}, ...]
            current_time: 当前时间
            
        Returns:
            {item_id: allocated_attention}
        """
        if not tasks:
            return {}
        
        # 按优先级排序
        sorted_tasks = sorted(tasks, key=lambda x: x.get('priority', 0), reverse=True)
        
        # 计算优先级权重
        total_priority = sum(t.get('priority', 1) for t in sorted_tasks)
        available = self.attention.resources.available()
        
        allocations = {}
        
        for task in sorted_tasks:
            task_id = task['id']
            
            # 优先级比例分配
            weight = task.get('priority', 1) / total_priority if total_priority > 0 else 0
            amount = max(self.min_attention, available * weight)
            
            # 检查是否可分配
            if self.attention.allocate(task_id, amount):
                allocations[task_id] = amount
                available -= amount
        
        return allocations
    
    def reallocate(self) -> Dict[str, float]:
        """重分配注意力"""
        # 收集所有项目的当前权重
        current_weights = self.attention.get_attention_weights()
        
        # 计算应该分配的量
        allocations = {}
        available = self.attention.resources.available()
        
        for item_id, weight in current_weights.items():
            if weight > 0.1:  # 只保留超过10%注意力的项目
                amount = available * weight
                if self.attention.allocate(item_id, amount):
                    allocations[item_id] = amount
        
        return allocations

# ============ 便捷函数 ============

def create_attention_system(capacity: float = 100.0) -> FiringRateAttentionSystem:
    """创建注意力系统"""
    return FiringRateAttentionSystem(total_capacity=capacity)

def quick_attend(item_id: str, intensity: float = 0.8) -> float:
    """快速分配注意力"""
    system = create_attention_system()
    system.add_item(item_id, item_id)
    system.update({item_id: intensity})
    return system.get_item_rate(item_id)

# ============ 示例使用 ============

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
