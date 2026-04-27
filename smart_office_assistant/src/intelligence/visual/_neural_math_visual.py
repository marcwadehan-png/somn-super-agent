# -*- coding: utf-8 -*-
"""
NeuralMathVisual - 神经数学视觉系统
====================================

D. 神经数学视觉系统 (V7.0)

包含:
- D.1 神经几何: 格式塔原理
- D.2 Gabor特征提取
- D.3 SOM自组织映射

版本: v1.0.0
创建: 2026-04-24
"""

from __future__ import annotations

import math
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import numpy as np

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# D.1 神经几何 - 格式塔原理
# ═══════════════════════════════════════════════════════════════

@dataclass
class GestaltPrinciple:
    """格式塔原则"""
    name: str
    description: str
    weight: float = 1.0
    applicable: bool = True


class GestaltGeometry:
    """
    格式塔神经几何。
    
    实现格式塔心理学原理，用于视觉模式识别：
    - 接近律：空间接近的元素被视为整体
    - 相似律：相似的元素被视为整体
    - 连续律：沿连续路径的元素被视为整体
    - 闭合律：倾向于填补缺失形成完整图形
    - 图形-背景：区分前景图形和背景
    
    版本: v1.0.0
    """

    PRINCIPLES = [
        GestaltPrinciple("proximity", "接近律：距离近的元素形成整体", 0.9),
        GestaltPrinciple("similarity", "相似律：相似特征形成整体", 0.85),
        GestaltPrinciple("continuity", "连续律：沿连续路径形成整体", 0.8),
        GestaltPrinciple("closure", "闭合律：倾向于填补缺失", 0.75),
        GestaltPrinciple("figure_ground", "图形-背景分离", 0.7),
        GestaltPrinciple("symmetry", "对称性：对称元素形成整体", 0.65),
    ]

    def __init__(self):
        self.active_principles = {p.name: p for p in self.PRINCIPLES}

    def detect_groups(
        self,
        points: List[Tuple[float, float]],
        similarity_threshold: float = 0.5,
    ) -> List[List[int]]:
        """
        基于格式塔原则检测元素分组。
        
        Args:
            points: 点坐标列表 [(x, y), ...]
            similarity_threshold: 相似度阈值
            
        Returns:
            分组索引列表 [[group1_indices], [group2_indices], ...]
        """
        if len(points) < 2:
            return [list(range(len(points)))]
        
        n = len(points)
        groups = []
        used = set()
        
        # 接近律分组
        proximity_groups = self._group_by_proximity(points)
        
        for group in proximity_groups:
            if len(group) > 1:
                groups.append(group)
                used.update(group)
        
        # 未分组的点单独处理
        for i in range(n):
            if i not in used:
                groups.append([i])
        
        return groups

    def _group_by_proximity(
        self,
        points: List[Tuple[float, float]],
    ) -> List[List[int]]:
        """基于接近律分组"""
        if len(points) < 2:
            return [[i] for i in range(len(points))]
        
        # 计算平均距离作为阈值
        distances = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                d = self._distance(points[i], points[j])
                distances.append(d)
        
        threshold = sum(distances) / len(distances) if distances else 1.0
        
        # Union-Find聚类
        parent = list(range(len(points)))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if self._distance(points[i], points[j]) < threshold:
                    union(i, j)
        
        # 收集分组
        groups_dict: Dict[int, List[int]] = {}
        for i in range(len(points)):
            root = find(i)
            if root not in groups_dict:
                groups_dict[root] = []
            groups_dict[root].append(i)
        
        return list(groups_dict.values())

    def _distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """欧几里得距离"""
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def compute_closure_score(self, contour: List[Tuple[float, float]]) -> float:
        """
        计算闭合度分数。
        
        Args:
            contour: 轮廓点序列
            
        Returns:
            闭合度分数 [0, 1]
        """
        if len(contour) < 3:
            return 0.0
        
        # 起点和终点距离
        start_end_dist = self._distance(contour[0], contour[-1])
        
        # 轮廓总长度
        total_length = sum(
            self._distance(contour[i], contour[(i + 1) % len(contour)])
            for i in range(len(contour))
        )
        
        # 闭合度 = 1 - (开口距离 / 周长)
        closure = max(0, 1 - start_end_dist / (total_length + 1e-6))
        
        return closure

    def detect_symmetry(
        self,
        points: List[Tuple[float, float]],
    ) -> Tuple[float, Optional[Tuple[float, float]]]:
        """
        检测对称性。
        
        Returns:
            (对称分数, 对称轴方向角)
        """
        if len(points) < 3:
            return 0.0, None
        
        # 计算中心
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
        center = (cx, cy)
        
        # 计算各点到中心的角度
        angles: Dict[float, List[Tuple[float, float]]] = {}
        for p in points:
            angle = math.atan2(p[1] - cy, p[0] - cx)
            rounded = round(angle, 2)
            if rounded not in angles:
                angles[rounded] = []
            angles[rounded].append(p)
        
        # 对称轴 = 有成对点的角度
        paired = sum(1 for angles_list in angles.values() if len(angles_list) >= 2)
        
        symmetry_score = paired / len(points) if points else 0.0
        
        return symmetry_score, None

    def separate_figure_ground(
        self,
        image: List[List[float]],
        threshold: float = 0.5,
    ) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """
        分离图形和背景。
        
        Args:
            image: 二值化图像矩阵
            threshold: 阈值
            
        Returns:
            (figure_points, ground_points)
        """
        figure = []
        ground = []
        
        for y, row in enumerate(image):
            for x, val in enumerate(row):
                if val >= threshold:
                    figure.append((x, y))
                else:
                    ground.append((x, y))
        
        return figure, ground

    def get_active_principles(self) -> List[str]:
        """获取激活的原则列表"""
        return [p.name for p in self.PRINCIPLES if p.applicable]


# ═══════════════════════════════════════════════════════════════
# D.2 Gabor特征提取
# ═══════════════════════════════════════════════════════════════

@dataclass
class GaborKernel:
    """Gabor核"""
    sigma: float = 3.0      # 高斯包络标准差
    lambd: float = 10.0    # 波长
    gamma: float = 0.5      # 空间纵横比
    psi: float = 0         # 相位偏移
    orientation: float = 0  # 方向角 (弧度)


class GaborFeatureExtractor:
    """
    Gabor特征提取器。
    
    Gabor函数是人类视觉系统在简单细胞层面的数学模型，
    在纹理分析、边缘检测、方向选择等方面表现优异。
    
    Gabor函数:
    g(x,y) = exp(-(x'^2 + γ²y'^2) / 2σ²) * cos(2πx'/λ + ψ)
    其中:
        x' = x*cos(θ) + y*sin(θ)
        y' = -x*sin(θ) + y*cos(θ)
    
    版本: v1.0.0
    """

    def __init__(self, num_orientations: int = 8, num_scales: int = 5):
        self.num_orientations = num_orientations
        self.num_scales = num_scales
        
        # 生成不同尺度和方向的核
        self._kernels = self._create_kernels()

    def _create_kernels(self) -> List[GaborKernel]:
        """创建Gabor核库"""
        kernels = []
        
        orientations = [
            i * math.pi / self.num_orientations
            for i in range(self.num_orientations)
        ]
        
        scales = [
            1.0 * (1.5 ** s)
            for s in range(self.num_scales)
        ]
        
        for lambd in scales:
            for theta in orientations:
                kernels.append(GaborKernel(
                    sigma=lambd / 2,
                    lambd=lambd,
                    gamma=0.5,
                    orientation=theta,
                ))
        
        return kernels

    def create_kernel(self, kernel: GaborKernel, size: int = 21) -> np.ndarray:
        """
        创建单个Gabor核矩阵。
        
        Args:
            kernel: Gabor核参数
            size: 核大小（必须是奇数）
            
        Returns:
            Gabor核矩阵
        """
        half = size // 2
        gabor = np.zeros((size, size))
        
        sigma = kernel.sigma
        lambd = kernel.lambd
        gamma = kernel.gamma
        psi = kernel.psi
        theta = kernel.orientation
        
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        
        for y in range(size):
            for x in range(size):
                # 坐标变换
                x_prime = (x - half) * cos_theta + (y - half) * sin_theta
                y_prime = -(x - half) * sin_theta + (y - half) * cos_theta
                
                # Gabor函数
                exponent = -(x_prime**2 + gamma**2 * y_prime**2) / (2 * sigma**2)
                gabor[y, x] = math.exp(exponent) * math.cos(
                    2 * math.pi * x_prime / lambd + psi
                )
        
        return gabor

    def apply_kernel(
        self,
        image: np.ndarray,
        kernel: np.ndarray,
    ) -> np.ndarray:
        """
        对图像应用Gabor核。
        
        使用卷积运算。
        """
        from scipy import signal
        
        # 使用scipy卷积
        result = signal.convolve2d(
            image,
            kernel,
            mode='same',
            boundary='symm'
        )
        
        return result

    def extract_features(
        self,
        image: np.ndarray,
        normalize: bool = True,
    ) -> Dict[str, np.ndarray]:
        """
        提取Gabor特征。
        
        Args:
            image: 输入图像 (H x W)
            normalize: 是否归一化
            
        Returns:
            特征字典 {"orientation_0": feature_map, ...}
        """
        features = {}
        
        for i, kernel_def in enumerate(self._kernels):
            kernel = self.create_kernel(kernel_def)
            response = self.apply_kernel(image, kernel)
            
            if normalize:
                # L2归一化
                norm = np.linalg.norm(response)
                if norm > 1e-6:
                    response = response / norm
            
            features[f"orient_{int(kernel_def.orientation * 180 / math.pi):03d}_scale_{i // self.num_orientations}"] = response
        
        return features

    def extract_direction_energy(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """
        提取各方向能量。
        
        Args:
            image: 输入图像
            
        Returns:
            方向能量向量 (num_orientations,)
        """
        energy = np.zeros(self.num_orientations)
        
        for i, kernel_def in enumerate(self._kernels):
            kernel = self.create_kernel(kernel_def)
            response = self.apply_kernel(image, kernel)
            
            # 能量 = 响应平方的均值
            energy[i % self.num_orientations] += np.mean(response ** 2)
        
        # 归一化
        total = np.sum(energy)
        if total > 1e-6:
            energy = energy / total
        
        return energy

    def detect_edges(
        self,
        image: np.ndarray,
        threshold: float = 0.1,
    ) -> np.ndarray:
        """
        使用Gabor特征检测边缘。
        
        Returns:
            边缘图
        """
        # 水平和垂直方向的Gabor核
        h_kernel = self.create_kernel(GaborKernel(orientation=0))
        v_kernel = self.create_kernel(GaborKernel(orientation=math.pi / 2))
        
        # 应用核
        h_response = self.apply_kernel(image, h_kernel)
        v_response = self.apply_kernel(image, v_kernel)
        
        # 计算边缘强度
        edges = np.sqrt(h_response ** 2 + v_response ** 2)
        
        # 二值化
        edges = (edges > threshold).astype(float)
        
        return edges

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "num_orientations": self.num_orientations,
            "num_scales": self.num_scales,
            "total_kernels": len(self._kernels),
        }


# ═══════════════════════════════════════════════════════════════
# D.3 SOM自组织映射
# ═══════════════════════════════════════════════════════════════

class SOMNode:
    """SOM节点"""
    def __init__(self, weights: np.ndarray):
        self.weights = weights.copy()
        self.position: Tuple[int, int] = (0, 0)


class SelfOrganizingMap:
    """
    自组织映射 (Self-Organizing Map, SOM)。
    
    SOM是一种无监督神经网络，通过竞争学习将高维输入映射到
    低维（通常是2D）网格，同时保持拓扑结构。
    
    算法:
    1. 初始化权重
    2. 找最佳匹配单元(BMU)
    3. 更新BMU及其邻域的权重
    4. 重复直到收敛
    
    版本: v1.0.0
    """

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        input_dim: int = 784,
        learning_rate: float = 0.5,
        sigma: float = 2.0,  # 邻域初始半径
    ):
        self.width = width
        self.height = height
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.sigma = sigma
        
        # 初始化节点
        self.nodes: List[List[SOMNode]] = []
        for y in range(height):
            row = []
            for x in range(width):
                # 随机初始化权重
                weights = np.random.randn(input_dim) * 0.1
                node = SOMNode(weights)
                node.position = (x, y)
                row.append(node)
            self.nodes.append(row)
        
        # 训练状态
        self._iterations = 0
        self._training = False

    def _find_bmu(self, input_vec: np.ndarray) -> Tuple[int, int]:
        """找到最佳匹配单元"""
        min_dist = float('inf')
        bmu = (0, 0)
        
        for y in range(self.height):
            for x in range(self.width):
                dist = np.linalg.norm(input_vec - self.nodes[y][x].weights)
                if dist < min_dist:
                    min_dist = dist
                    bmu = (x, y)
        
        return bmu

    def _neighborhood_function(
        self,
        bmu: Tuple[int, int],
        node_pos: Tuple[int, int],
        sigma: float,
    ) -> float:
        """计算邻域函数（高斯邻域）"""
        dx = bmu[0] - node_pos[0]
        dy = bmu[1] - node_pos[1]
        dist_sq = dx**2 + dy**2
        
        return math.exp(-dist_sq / (2 * sigma**2))

    def _decay_function(self, initial: float, iteration: int, max_iter: int) -> float:
        """衰减函数"""
        return initial * math.exp(-iteration / (max_iter * 0.3))

    def train(
        self,
        data: np.ndarray,
        iterations: int = 1000,
        verbose: bool = False,
    ) -> None:
        """
        训练SOM。
        
        Args:
            data: 训练数据 (N x input_dim)
            iterations: 迭代次数
            verbose: 是否输出进度
        """
        self._training = True
        n_samples = len(data)
        
        for it in range(iterations):
            if not self._training:
                break
            
            # 衰减学习率和邻域半径
            lr = self._decay_function(self.learning_rate, it, iterations)
            sigma = self._decay_function(self.sigma, it, iterations)
            
            # 随机选择一个样本
            idx = np.random.randint(n_samples)
            input_vec = data[idx]
            
            # 找BMU
            bmu = self._find_bmu(input_vec)
            
            # 更新BMU及其邻域
            for y in range(self.height):
                for x in range(self.width):
                    node = self.nodes[y][x]
                    
                    # 邻域权重
                    neighbor_weight = self._neighborhood_function(bmu, (x, y), sigma)
                    
                    # 更新权重
                    delta = lr * neighbor_weight * (input_vec - node.weights)
                    node.weights += delta
            
            self._iterations = it + 1
            
            if verbose and (it + 1) % 100 == 0:
                logger.info(f"SOM training: {it + 1}/{iterations} iterations")
        
        self._training = False
        if verbose:
            logger.info(f"SOM training completed: {self._iterations} iterations")

    def stop_training(self) -> None:
        """停止训练"""
        self._training = False

    def map_vector(self, input_vec: np.ndarray) -> Tuple[int, int]:
        """
        将输入向量映射到SOM网格位置。
        
        Returns:
            网格坐标 (x, y)
        """
        return self._find_bmu(input_vec)

    def map_vectors_batch(self, data: np.ndarray) -> List[Tuple[int, int]]:
        """
        批量映射。
        
        Returns:
            坐标列表
        """
        return [self.map_vector(vec) for vec in data]

    def get_node_at(self, x: int, y: int) -> Optional[SOMNode]:
        """获取指定位置的节点"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.nodes[y][x]
        return None

    def get_u_matrix(self) -> np.ndarray:
        """
        计算U-Matrix（统一距离矩阵）。
        
        U-Matrix显示每个节点与其邻居之间的距离，
        可用于可视化聚类边界。
        
        Returns:
            U-Matrix (height x width)
        """
        u_matrix = np.zeros((self.height, self.width))
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if (dx, dy) != (0, 0):
                                dist = np.linalg.norm(
                                    self.nodes[y][x].weights - 
                                    self.nodes[ny][nx].weights
                                )
                                neighbors.append(dist)
                
                u_matrix[y, x] = np.mean(neighbors) if neighbors else 0
        
        return u_matrix

    def cluster(
        self,
        threshold: float = None,
    ) -> np.ndarray:
        """
        简单聚类（基于U-Matrix）。
        
        Returns:
            聚类标签矩阵
        """
        u_matrix = self.get_u_matrix()
        
        if threshold is None:
            # 使用中位数作为阈值
            threshold = np.median(u_matrix)
        
        # 二值化
        labels = (u_matrix > threshold).astype(int)
        
        return labels

    def get_quantization_error(self, data: np.ndarray) -> float:
        """
        计算量化误差。
        
        Args:
            data: 测试数据
            
        Returns:
            平均量化误差
        """
        errors = []
        
        for vec in data:
            bmu = self.map_vector(vec)
            node = self.nodes[bmu[1]][bmu[0]]
            error = np.linalg.norm(vec - node.weights)
            errors.append(error)
        
        return np.mean(errors)

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "width": self.width,
            "height": self.height,
            "total_nodes": self.width * self.height,
            "input_dim": self.input_dim,
            "iterations": self._iterations,
            "training": self._training,
        }


# ═══════════════════════════════════════════════════════════════
# 神经数学视觉系统入口
# ═══════════════════════════════════════════════════════════════

class NeuralMathVisualSystem:
    """
    神经数学视觉系统。
    
    整合格式塔、Gabor和SOM三大组件。
    
    版本: v1.0.0
    """

    def __init__(self):
        self.gestalt = GestaltGeometry()
        self.gabor = GaborFeatureExtractor(num_orientations=6, num_scales=4)
        self.som: Optional[SelfOrganizingMap] = None

    def init_som(self, width: int = 10, height: int = 10, input_dim: int = 64) -> None:
        """初始化SOM"""
        self.som = SelfOrganizingMap(width, height, input_dim)

    def process_visual(
        self,
        image: np.ndarray,
        task: str = "all",
    ) -> Dict[str, Any]:
        """
        处理视觉任务。
        
        Args:
            image: 输入图像
            task: "all" | "gestalt" | "gabor" | "som"
            
        Returns:
            处理结果
        """
        results = {}
        
        if task in ("all", "gestalt"):
            # 格式塔分析
            if len(image.shape) == 2:
                binary = (image > 0.5).astype(float)
                figure, ground = self.gestalt.separate_figure_ground(binary.tolist())
                results["gestalt"] = {
                    "num_figure_points": len(figure),
                    "num_ground_points": len(ground),
                    "active_principles": self.gestalt.get_active_principles(),
                }
        
        if task in ("all", "gabor"):
            # Gabor特征
            if len(image.shape) == 2:
                features = self.gabor.extract_features(image, normalize=True)
                direction_energy = self.gabor.extract_direction_energy(image)
                results["gabor"] = {
                    "num_features": len(features),
                    "dominant_orientation": int(np.argmax(direction_energy)),
                    "direction_energy": direction_energy.tolist(),
                }
        
        if task in ("all", "som") and self.som is not None:
            # SOM映射
            flat = image.flatten()
            # 调整维度
            if len(flat) < self.som.input_dim:
                flat = np.pad(flat, (0, self.som.input_dim - len(flat)))
            elif len(flat) > self.som.input_dim:
                flat = flat[:self.som.input_dim]
            
            position = self.som.map_vector(flat)
            results["som"] = {
                "mapped_position": position,
                "stats": self.som.get_stats(),
            }
        
        return results

    def get_stats(self) -> Dict:
        """获取系统统计"""
        return {
            "gestalt_active": len(self.gestalt.get_active_principles()),
            "gabor": self.gabor.get_stats(),
            "som_initialized": self.som is not None,
            "som": self.som.get_stats() if self.som else None,
        }
