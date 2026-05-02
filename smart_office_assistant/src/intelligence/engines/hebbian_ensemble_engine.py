# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_learning',
    'bcm',
    'cluster',
    'competitive_step',
    'compute_activation',
    'compute_output',
    'cooperative_update',
    'create_hebbian_engine',
    'create_som',
    'extract_features',
    'find_bmu',
    'get_hebbian_insights',
    'get_weight_matrix',
    'hebbian',
    'lateral_inhibition',
    'learn_association',
    'learn_patterns',
    'map_input',
    'oja',
    'recall_association',
    'stdp',
    'train',
    'train_step',
]

Hebbian协同学习引擎 v1.0.0
=======================

协同学习系统

核心来源:
- Hebbian Learning Rule
- Self-Organizing Maps (SOM)

核心思想:
1. Hebbian学习规则 - 同时激活的神经元连接加强
2. 竞争学习 - 神经元之间的竞争
3. 协同学习 - 合作实现功能
4. 拓扑保持 - 保持输入空间的拓扑结构

@author: Somn AI
@version: 1.0.0
@date: 2026-04-02
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)
from enum import Enum
import heapq

class LearningRule(Enum):
    """学习规则类型"""
    HEBBIAN = "hebbian"                    # 经典Hebb规则
    OJA = "oja"                           # Oja规则(归一化)
    BCM = "bcm"                           # Bienenstock-Cooper-Munro规则
    anti_HEBBIAN = "anti_hebbian"          # 反Hebb规则
    STDP = "stdp"                         # 时序依赖可塑性

@dataclass
class Neuron:
    """神经元"""
    neuron_id: str
    weights: np.ndarray                   # 突触权重
    bias: float = 0.0
    activation: float = 0.0
    output: float = 0.0
    position: Tuple[int, int] = (0, 0)   # 在网络中的位置
    
    def compute_activation(self, inputs: np.ndarray) -> float:
        """计算激活"""
        self.activation = np.dot(self.weights, inputs) + self.bias
        return self.activation
    
    def compute_output(self, activation_function: Callable = None) -> float:
        """计算输出"""
        if activation_function:
            self.output = activation_function(self.activation)
        else:
            self.output = self.activation
        return self.output

@dataclass
class Synapse:
    """突触连接"""
    from_neuron: str
    to_neuron: str
    weight: float = 0.0
    last_activation: float = 0.0
    is_plastic: bool = True

class HebbianLearningRule:
    """Hebbian学习规则实现"""
    
    @staticmethod
    def hebbian(
        pre_activation: float,
        post_activation: float,
        current_weight: float,
        learning_rate: float,
        max_weight: float = 1.0
    ) -> float:
        """经典Hebb规则
        
        Δw = η * pre * post
        
        问题:权重可能无限增长
        """
        delta_w = learning_rate * pre_activation * post_activation
        new_weight = current_weight + delta_w
        return np.clip(new_weight, -max_weight, max_weight)
    
    @staticmethod
    def oja(
        pre_activation: float,
        post_activation: float,
        current_weight: float,
        learning_rate: float,
        decay: float = 0.01
    ) -> float:
        """Oja规则
        
        Δw = η * pre * post - η * α * w * post^2
        
        优点:自动归一化
        """
        delta_w = learning_rate * pre_activation * post_activation
        delta_w -= learning_rate * decay * current_weight * (post_activation ** 2)
        return current_weight + delta_w
    
    @staticmethod
    def bcm(
        pre_activation: float,
        post_activation: float,
        current_weight: float,
        learning_rate: float,
        theta: float = 0.0
    ) -> float:
        """BCM规则
        
        Δw = η * pre * post * (post - θ)
        
        优点:阈值依赖,可塑性与活动相关
        """
        delta_w = learning_rate * pre_activation * post_activation * (post_activation - theta)
        return current_weight + delta_w
    
    @staticmethod
    def stdp(
        pre_spike: float,
        post_spike: float,
        time_diff: float,
        current_weight: float,
        learning_rate: float = 0.01
    ) -> float:
        """时序依赖可塑性(STDP)
        
        Δw = A+ * exp(-|Δt|/τ+) if Δt > 0 (LTP)
        Δw = -A- * exp(|Δt|/τ-) if Δt < 0 (LTD)
        """
        if time_diff > 0:  # pre before post: LTP
            delta_w = learning_rate * np.exp(-abs(time_diff) / 20) * pre_spike * post_spike
        else:  # post before pre: LTD
            delta_w = -learning_rate * np.exp(-abs(time_diff) / 20) * pre_spike * post_spike
        
        return current_weight + delta_w

class CompetitiveMechanism:
    """竞争机制 - 实现神经元之间的竞争"""
    
    def __init__(self, k: int = 1):
        """
        Args:
            k: 胜出的神经元数量
        """
        self.k = k
    
    def competitive_step(
        self,
        neurons: List[Neuron],
        inputs: np.ndarray
    ) -> List[Neuron]:
        """竞争步骤
        
        计算所有神经元的激活,保留top-k
        """
        # 计算激活
        activations = []
        for neuron in neurons:
            act = neuron.compute_activation(inputs)
            activations.append((act, neuron))
        
        # 排序并选出胜出者
        activations.sort(key=lambda x: x[0], reverse=True)
        winners = activations[:self.k]
        
        # 标记胜出者
        winner_ids = {n.neuron_id for _, n in winners}
        for neuron in neurons:
            neuron.is_winner = neuron.neuron_id in winner_ids
        
        return [n for _, n in winners]
    
    def lateral_inhibition(
        self,
        neurons: List[Neuron],
        sigma: float = 1.0
    ) -> np.ndarray:
        """侧抑制 - 增强胜出者,抑制邻近
        
        Args:
            neurons: 神经元列表
            sigma: 抑制范围
            
        Returns:
            抑制系数矩阵
        """
        n = len(neurons)
        inhibition = np.zeros((n, n))
        
        for i, n1 in enumerate(neurons):
            for j, n2 in enumerate(neurons):
                if i == j:
                    inhibition[i, j] = 1.0  # 自身不抑制
                else:
                    dist = np.sqrt(
                        (n1.position[0] - n2.position[0])**2 +
                        (n1.position[1] - n2.position[1])**2
                    )
                    # 高斯抑制
                    inhibition[i, j] = np.exp(-dist**2 / (2 * sigma**2))
        
        return inhibition

class CooperativeMechanism:
    """协同机制 - 实现神经元之间的合作"""
    
    def __init__(self, sigma: float = 2.0):
        """
        Args:
            sigma: 合作范围
        """
        self.sigma = sigma
    
    def cooperative_update(
        self,
        neurons: List[Neuron],
        winners: List[Neuron],
        learning_rate: float
    ) -> None:
        """协同更新 - 胜出者的邻近神经元也获得学习"""
        for neuron in neurons:
            for winner in winners:
                dist = np.sqrt(
                    (neuron.position[0] - winner.position[0])**2 +
                    (neuron.position[1] - winner.position[1])**2
                )
                
                # 高斯邻域函数
                neighbor_factor = np.exp(-dist**2 / (2 * self.sigma**2))
                
                # 调整学习率
                effective_lr = learning_rate * neighbor_factor
                neuron.learning_rate_adjusted = effective_lr

class SelfOrganizingMap:
    """自组织mapping (SOM)
    
    基于Hebbian学习的拓扑保持mapping
    
    特点:
    1. 竞争学习 - 找出最佳匹配单元(BMU)
    2. 协同学习 - 邻域函数
    3. 适应学习 - 权重更新
    4. 拓扑保持 - 保持输入空间的拓扑结构
    """
    
    def __init__(
        self,
        width: int,
        height: int,
        input_dim: int,
        sigma: float = 3.0,
        learning_rate: float = 0.5
    ):
        """initSOM
        
        Args:
            width: 网格宽度
            height: 网格高度
            input_dim: 输入维度
            sigma: 初始邻域半径
            learning_rate: 初始学习率
        """
        self.width = width
        self.height = height
        self.input_dim = input_dim
        
        # init神经元
        self.neurons = []
        for i in range(height):
            for j in range(width):
                neuron = Neuron(
                    neuron_id=f"n_{i}_{j}",
                    weights=np.random.randn(input_dim) * 0.1,
                    position=(i, j)
                )
                self.neurons.append(neuron)
        
        # 搜索mapping
        self.neuron_map = {n.neuron_id: n for n in self.neurons}
        
        # 学习参数
        self.initial_sigma = sigma
        self.sigma = sigma
        self.initial_lr = learning_rate
        self.learning_rate = learning_rate
        
        # 时间常数
        self.time_constant = 1000
        self.iteration = 0
        
        # 量化误差
        self.quantization_error: List[float] = []
    
    def find_bmu(self, input_vec: np.ndarray) -> Neuron:
        """找到最佳匹配单元(BMU)
        
        Args:
            input_vec: 输入向量
            
        Returns:
            BMU神经元
        """
        best_neuron = self.neurons[0]
        best_distance = float('inf')
        
        for neuron in self.neurons:
            dist = np.linalg.norm(neuron.weights - input_vec)
            if dist < best_distance:
                best_distance = dist
                best_neuron = neuron
        
        return best_neuron
    
    def train_step(self, input_vec: np.ndarray) -> float:
        """训练一步
        
        Args:
            input_vec: 输入向量
            
        Returns:
            量化误差
        """
        self.iteration += 1
        
        # 更新学习参数
        self.sigma = self.initial_sigma * np.exp(-self.iteration / self.time_constant)
        self.learning_rate = self.initial_lr * np.exp(-self.iteration / self.time_constant)
        
        # 找到BMU
        bmu = self.find_bmu(input_vec)
        
        # 计算量化误差
        quantization_error = np.linalg.norm(bmu.weights - input_vec)
        self.quantization_error.append(quantization_error)
        
        # 更新权重
        for neuron in self.neurons:
            # 计算与BMU的距离
            dist = np.linalg.norm(
                np.array(neuron.position) - np.array(bmu.position)
            )
            
            # 邻域函数
            neighborhood = np.exp(-dist**2 / (2 * self.sigma**2))
            
            # 权重更新
            delta_w = self.learning_rate * neighborhood * (input_vec - neuron.weights)
            neuron.weights += delta_w
        
        return quantization_error
    
    def train(
        self,
        data: np.ndarray,
        epochs: int,
        batch_size: int = 1
    ) -> Dict[str, List[float]]:
        """训练SOM
        
        Args:
            data: 训练数据 (n_samples, input_dim)
            epochs: 训练轮数
            batch_size: 批次大小
            
        Returns:
            训练统计
        """
        n_samples = data.shape[0]
        errors = []
        
        for epoch in range(epochs):
            epoch_errors = []
            
            # 打乱数据
            indices = np.random.permutation(n_samples)
            
            for i in indices[:batch_size]:
                error = self.train_step(data[i])
                epoch_errors.append(error)
            
            avg_error = np.mean(epoch_errors)
            errors.append(avg_error)
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch+1}/{epochs}, Avg Error: {avg_error:.4f}")
        
        return {"quantization_error": errors}
    
    def map_input(self, input_vec: np.ndarray) -> Tuple[int, int]:
        """将输入mapping到SOM上的位置
        
        Args:
            input_vec: 输入向量
            
        Returns:
            SOM上的位置
        """
        bmu = self.find_bmu(input_vec)
        return bmu.position
    
    def get_weight_matrix(self) -> np.ndarray:
        """get权重矩阵"""
        weights = np.zeros((self.height, self.width, self.input_dim))
        
        for neuron in self.neurons:
            i, j = neuron.position
            weights[i, j] = neuron.weights
        
        return weights

class HebbianEnsembleEngine:
    """Hebbian协同学习引擎
    
    整合多种Hebbian学习机制,实现协同学习
    
    应用场景:
    1. 模式recognize - 学习输入模式
    2. characteristics提取 - 自动发现显著characteristics
    3. 聚类分析 - 数据聚类
    4. 联想记忆 - 关联学习
    """
    
    def __init__(self):
        """init引擎"""
        self.name = "HebbianEnsembleEngine"
        self.version="6.2.0"
        
        # 学习规则
        self.learning_rule = HebbianLearningRule()
        
        # 竞争机制
        self.competitive = CompetitiveMechanism(k=1)
        
        # 协同机制
        self.cooperative = CooperativeMechanism(sigma=2.0)
        
        # SOM实例
        self.som: Optional[SelfOrganizingMap] = None
        
        # 突触权重历史
        self.synapse_history: List[Synapse] = []
        
        # 学习统计
        self.stats = {
            "iterations": 0,
            "avg_weight": [],
            "coherence": []
        }
    
    def create_som(
        self,
        width: int = 10,
        height: int = 10,
        input_dim: int = 10
    ) -> SelfOrganizingMap:
        """创建自组织mapping"""
        self.som = SelfOrganizingMap(
            width=width,
            height=height,
            input_dim=input_dim,
            sigma=3.0,
            learning_rate=0.5
        )
        return self.som
    
    def learn_patterns(
        self,
        patterns: np.ndarray,
        epochs: int = 100,
        learning_rule: LearningRule = LearningRule.OJA
    ) -> Dict[str, Any]:
        """学习输入模式
        
        Args:
            patterns: 输入模式 (n_patterns, pattern_dim)
            epochs: 训练轮数
            learning_rule: 学习规则
            
        Returns:
            学习结果
        """
        if self.som is None:
            input_dim = patterns.shape[1]
            self.create_som(width=10, height=10, input_dim=input_dim)
        
        # 训练
        training_stats = self.som.train(patterns, epochs)
        
        # 学习权重矩阵
        weight_matrix = self.som.get_weight_matrix()
        
        return {
            "weight_matrix": weight_matrix,
            "training_stats": training_stats,
            "final_error": training_stats["quantization_error"][-1] if training_stats["quantization_error"] else 0
        }
    
    def learn_association(
        self,
        pattern_a: np.ndarray,
        pattern_b: np.ndarray,
        n_neurons: int = 100,
        epochs: int = 100
    ) -> np.ndarray:
        """学习两个模式之间的关联
        
        Args:
            pattern_a: 模式A
            pattern_b: 模式B
            n_neurons: 神经元数量
            epochs: 训练轮数
            
        Returns:
            学习后的关联权重矩阵
        """
        n_a = len(pattern_a)
        n_b = len(pattern_b)
        
        # init权重
        weights = np.random.randn(n_a, n_b) * 0.01
        
        for _ in range(epochs):
            # Hebbian更新
            for i in range(n_a):
                for j in range(n_b):
                    rule = self.learning_rule.oja if LearningRule.OJA else self.learning_rule.hebbian
                    weights[i, j] = rule(
                        pattern_a[i],
                        pattern_b[j],
                        weights[i, j],
                        learning_rate=0.01
                    )
        
        return weights
    
    def recall_association(
        self,
        pattern_a: np.ndarray,
        weights: np.ndarray
    ) -> np.ndarray:
        """回忆关联 - 从模式A回忆模式B
        
        Args:
            pattern_a: 模式A
            weights: 关联权重
            
        Returns:
            回忆的模式B
        """
        return np.dot(pattern_a, weights)
    
    def extract_features(
        self,
        data: np.ndarray,
        n_features: int = 10
    ) -> np.ndarray:
        """characteristics提取
        
        使用Hebbian学习提取显著characteristics
        
        Args:
            data: 输入数据
            n_features: characteristics数量
            
        Returns:
            提取的characteristics
        """
        if self.som is None:
            self.create_som(width=n_features, height=1, input_dim=data.shape[1])
        
        # 训练SOM
        self.som.train(data, epochs=100)
        
        # 提取主成分
        weight_matrix = self.som.get_weight_matrix()
        
        # 对每个characteristics神经元计算平均激活
        features = []
        for i in range(n_features):
            feature_weights = weight_matrix[:, i, :].reshape(-1, data.shape[1])
            feature = np.mean(feature_weights, axis=0)
            features.append(feature)
        
        return np.array(features)
    
    def cluster(
        self,
        data: np.ndarray,
        n_clusters: int = 5
    ) -> np.ndarray:
        """聚类分析
        
        使用竞争Hebbian学习进行聚类
        
        Args:
            data: 输入数据
            n_clusters: 聚类数
            
        Returns:
            每个样本的聚类标签
        """
        if self.som is None:
            self.create_som(width=n_clusters, height=1, input_dim=data.shape[1])
        
        # 训练
        self.som.train(data, epochs=50)
        
        # 分配聚类标签
        labels = []
        for i in range(len(data)):
            pos = self.som.map_input(data[i])
            label = pos[1] % n_clusters  # 使用列位置作为标签
            labels.append(label)
        
        return np.array(labels)
    
    def analyze_learning(self) -> Dict[str, Any]:
        """分析学习结果"""
        if self.som is None:
            return {"error": "No SOM trained"}
        
        # 计算权重统计
        all_weights = np.array([n.weights for n in self.som.neurons])
        
        return {
            "avg_weight_norm": np.mean(np.linalg.norm(all_weights, axis=1)),
            "weight_variance": np.var(all_weights),
            "avg_quantization_error": np.mean(self.som.quantization_error) if self.som.quantization_error else 0,
            "n_neurons": len(self.som.neurons),
            "n_iterations": self.som.iteration
        }

# ==================== 工厂函数 ====================

def create_hebbian_engine() -> HebbianEnsembleEngine:
    """创建Hebbian协同学习引擎"""
    return HebbianEnsembleEngine()

def create_som(
    width: int = 10,
    height: int = 10,
    input_dim: int = 10
) -> SelfOrganizingMap:
    """创建自组织mapping"""
    return SelfOrganizingMap(width, height, input_dim)

def get_hebbian_insights() -> List[str]:
    """getHebbian学习的关键洞见"""
    return [
        "一起放电的神经元,连接在一起 (Hebb, 1949)",
        "竞争学习选出最佳匹配单元",
        "协同学习使邻近神经元也参与学习",
        "拓扑保持mapping:输入空间拓扑在输出空间保持",
        "Oja规则实现自动归一化",
        "BCM规则实现阈值依赖的可塑性",
        "STDP:时序依赖的突触可塑性"
    ]

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
