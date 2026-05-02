# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_image',
    'build_feature_maps',
    'convolve',
    'create_gabor_system',
    'create_orientation_histogram',
    'detect_corners',
    'detect_edges',
    'extract_features',
    'filter_image',
    'get_energy',
    'get_filter_count',
    'get_gabor_insights',
    'get_response_at',
    'get_responses_at',
    'get_texture_descriptor',
    'get_tuned_response',
    'match_features',
]

Gabor多尺度characteristics系统 v1.0.0
=======================

视觉characteristics系统

核心来源:
- Gabor函数: 复正弦调制的高斯函数
- 方位选择性与空间频率选择性

Gabor函数数学形式:
G(x,y;θ,σ,ω,γ) = exp(-(x'² + γ²y'²)/(2σ²)) * exp(iωx')

优点:
1. 在空间和频率域都具有良好的局部化性质
2. 可以捕捉不同方位和频率的characteristics
3. 与视觉皮层简单细胞的响应高度吻合

@author: Somn AI
@version: 1.0.0
@date: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import math

class FrequencySelectivity(Enum):
    """频率选择性"""
    LOW = "low"         # 低频(粗尺度)
    MEDIUM = "medium"   # 中频
    HIGH = "high"      # 高频(细尺度)

@dataclass
class GaborParameters:
    """Gabor函数参数"""
    theta: float = 0.0              # 方位角
    sigma: float = 1.0              # 高斯标准差
    omega: float = 0.5              # 空间频率
    gamma: float = 0.5              # 空间纵横比
    phase: float = 0.0              # 相位
    amplitude: float = 1.0          # 振幅

@dataclass
class FeatureResponse:
    """characteristics响应"""
    feature_id: str
    position: Tuple[int, int]
    orientation: float
    scale: int
    response: float
    phase: float
    confidence: float = 1.0

class GaborFilter:
    """Gabor滤波器
    
    实现Gabor函数的卷积核
    """
    
    def __init__(
        self,
        size: int = 21,
        params: GaborParameters = None
    ):
        """initGabor滤波器
        
        Args:
            size: 核大小(必须是奇数)
            params: Gabor参数
        """
        self.size = size if size % 2 == 1 else size + 1
        self.params = params or GaborParameters()
        self.kernel = self._create_kernel()
    
    def _create_kernel(self) -> np.ndarray:
        """创建Gabor核"""
        center = self.size // 2
        x = np.arange(self.size) - center
        y = np.arange(self.size) - center
        X, Y = np.meshgrid(x, y)
        
        # 旋转坐标
        theta = self.params.theta
        X_rot = X * np.cos(theta) + Y * np.sin(theta)
        Y_rot = -X * np.sin(theta) + Y * np.cos(theta)
        
        # 高斯包络
        gamma = self.params.gamma
        sigma = self.params.sigma
        gaussian = np.exp(-(X_rot**2 + gamma**2 * Y_rot**2) / (2 * sigma**2))
        
        # 复正弦调制
        omega = self.params.omega
        phase = self.params.phase
        sinusoid = np.exp(1j * (omega * X_rot + phase))
        
        # Gabor核
        kernel = self.params.amplitude * gaussian * sinusoid
        
        return kernel
    
    def convolve(self, image: np.ndarray) -> np.ndarray:
        """卷积运算
        
        Args:
            image: 输入图像
            
        Returns:
            卷积结果(复数)
        """
        from scipy.signal import convolve2d
        return convolve2d(image, self.kernel, mode='same')
    
    def get_response_at(
        self,
        image: np.ndarray,
        position: Tuple[int, int]
    ) -> complex:
        """get特定位置的响应"""
        h, w = image.shape
        cx, cy = position
        
        # 边界检查
        half_size = self.size // 2
        x_start = max(0, cx - half_size)
        x_end = min(w, cx + half_size + 1)
        y_start = max(0, cy - half_size)
        y_end = min(h, cy + half_size + 1)
        
        # 提取局部区域
        local = image[y_start:y_end, x_start:x_end]
        
        # 提取对应核区域
        kx_start = max(0, half_size - cx)
        ky_start = max(0, half_size - cy)
        kx_end = self.size - max(0, (cx + half_size + 1) - w)
        ky_end = self.size - max(0, (cy + half_size + 1) - h)
        
        kernel_local = self.kernel[ky_start:ky_end, kx_start:kx_end]
        
        if local.size > 0 and kernel_local.size > 0:
            return np.sum(local * kernel_local)
        return 0j
    
    def get_energy(self, image: np.ndarray) -> np.ndarray:
        """计算能量响应(幅度平方)"""
        response = self.convolve(image)
        return np.abs(response) ** 2

class GaborFilterBank:
    """Gabor滤波器组
    
    generate和管理多个Gabor滤波器,覆盖不同的方位和尺度
    """
    
    def __init__(
        self,
        n_orientations: int = 8,
        n_scales: int = 5,
        base_sigma: float = 1.0,
        base_frequency: float = 0.5
    ):
        """init滤波器组
        
        Args:
            n_orientations: 方位数量
            n_scales: 尺度数量
            base_sigma: 基础高斯尺度
            base_frequency: 基础空间频率
        """
        self.n_orientations = n_orientations
        self.n_scales = n_scales
        self.base_sigma = base_sigma
        self.base_frequency = base_frequency
        
        self.filters: List[GaborFilter] = []
        self._create_filter_bank()
    
    def _create_filter_bank(self):
        """创建滤波器组"""
        orientations = np.linspace(0, np.pi, self.n_orientations, endpoint=False)
        
        for scale in range(self.n_scales):
            sigma = self.base_sigma * (2 ** scale)
            omega = self.base_frequency / (2 ** scale)
            
            for theta in orientations:
                params = GaborParameters(
                    theta=theta,
                    sigma=sigma,
                    omega=omega,
                    gamma=0.5
                )
                
                size = max(21, int(6 * sigma) | 1)  # 确保奇数
                gabor_filter = GaborFilter(size=size, params=params)
                
                self.filters.append(gabor_filter)
    
    def get_filter_count(self) -> int:
        """get滤波器数量"""
        return len(self.filters)
    
    def filter_image(self, image: np.ndarray) -> List[np.ndarray]:
        """对图像应用所有滤波器
        
        Args:
            image: 输入图像
            
        Returns:
            各滤波器的响应列表
        """
        responses = []
        for gabor_filter in self.filters:
            response = gabor_filter.get_energy(image)
            responses.append(response)
        return responses
    
    def get_responses_at(
        self,
        image: np.ndarray,
        position: Tuple[int, int]
    ) -> List[FeatureResponse]:
        """get特定位置的响应
        
        Args:
            image: 输入图像
            position: 位置
            
        Returns:
            响应列表
        """
        responses = []
        orientations = np.linspace(0, np.pi, self.n_orientations, endpoint=False)
        
        idx = 0
        for scale in range(self.n_scales):
            for theta_idx, theta in enumerate(orientations):
                filter_response = self.filters[idx].get_response_at(image, position)
                idx += 1
                
                responses.append(FeatureResponse(
                    feature_id=f"f_{scale}_{theta_idx}",
                    position=position,
                    orientation=theta,
                    scale=scale,
                    response=np.abs(filter_response),
                    phase=np.angle(filter_response),
                    confidence=1.0
                ))
        
        return responses
    
    def get_tuned_response(
        self,
        image: np.ndarray,
        position: Tuple[int, int]
    ) -> Tuple[float, float, int]:
        """get调谐响应(最大响应)
        
        Returns:
            (最佳响应, 最佳方位, 最佳尺度)
        """
        responses = self.get_responses_at(image, position)
        
        if not responses:
            return 0.0, 0.0, 0
        
        best = max(responses, key=lambda r: r.response)
        return best.response, best.orientation, best.scale

class MultiScaleFeatureSystem:
    """多尺度characteristics系统
    
    整合Gabor滤波器组,实现多尺度characteristics提取
    """
    
    def __init__(
        self,
        n_orientations: int = 8,
        n_scales: int = 5
    ):
        """init"""
        self.name = "MultiScaleFeatureSystem"
        self.version="6.2.0"
        
        self.filter_bank = GaborFilterBank(
            n_orientations=n_orientations,
            n_scales=n_scales
        )
        
        # characteristics存储
        self.features: List[FeatureResponse] = []
        
        # characteristics图
        self.feature_maps: Dict[str, np.ndarray] = {}
    
    def extract_features(
        self,
        image: np.ndarray,
        stride: int = 1,
        threshold: float = 0.1
    ) -> List[FeatureResponse]:
        """提取characteristics
        
        Args:
            image: 输入图像
            stride: 采样步长
            threshold: 响应阈值
            
        Returns:
            显著characteristics列表
        """
        self.features = []
        h, w = image.shape[:2]
        
        positions = []
        for y in range(0, h, stride):
            for x in range(0, w, stride):
                positions.append((x, y))
        
        # get所有响应
        all_responses = self.filter_bank.filter_image(image)
        
        # 提取显著characteristics
        orientations = np.linspace(0, np.pi, self.filter_bank.n_orientations, endpoint=False)
        
        for y in range(0, h, stride):
            for x in range(0, w, stride):
                max_response = 0
                best_orientation = 0
                best_scale = 0
                
                idx = 0
                for scale in range(self.filter_bank.n_scales):
                    for theta_idx in range(self.filter_bank.n_orientations):
                        response = all_responses[idx][y, x]
                        idx += 1
                        
                        if response > max_response:
                            max_response = response
                            best_orientation = orientations[theta_idx]
                            best_scale = scale
                
                if max_response > threshold:
                    feature = FeatureResponse(
                        feature_id=f"feature_{len(self.features)}",
                        position=(x, y),
                        orientation=best_orientation,
                        scale=best_scale,
                        response=max_response,
                        phase=0.0,
                        confidence=min(1.0, max_response)
                    )
                    self.features.append(feature)
        
        return self.features
    
    def build_feature_maps(self, image: np.ndarray):
        """构建characteristics图"""
        h, w = image.shape[:2]
        orientations = np.linspace(0, np.pi, self.filter_bank.n_orientations, endpoint=False)
        
        self.feature_maps = {
            "magnitude": np.zeros((h, w)),
            "orientation": np.zeros((h, w)),
            "scale": np.zeros((h, w))
        }
        
        all_responses = self.filter_bank.filter_image(image)
        
        for y in range(h):
            for x in range(w):
                max_response = 0
                best_orientation = 0
                best_scale = 0
                
                idx = 0
                for scale in range(self.filter_bank.n_scales):
                    for theta_idx in range(self.filter_bank.n_orientations):
                        response = all_responses[idx][y, x]
                        idx += 1
                        
                        if response > max_response:
                            max_response = response
                            best_orientation = orientations[theta_idx]
                            best_scale = scale
                
                self.feature_maps["magnitude"][y, x] = max_response
                self.feature_maps["orientation"][y, x] = best_orientation
                self.feature_maps["scale"][y, x] = best_scale
    
    def detect_edges(
        self,
        image: np.ndarray,
        threshold: float = 0.2
    ) -> np.ndarray:
        """边缘检测
        
        使用Gaborcharacteristics检测边缘
        
        Args:
            image: 输入图像
            threshold: 阈值
            
        Returns:
            边缘图
        """
        self.build_feature_maps(image)
        
        # 计算梯度
        magnitude = self.feature_maps["magnitude"]
        orientation = self.feature_maps["orientation"]
        
        h, w = magnitude.shape
        edges = np.zeros((h, w))
        
        # 非最大抑制
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                theta = orientation[y, x]
                
                # 计算相邻像素
                cos_t = np.cos(theta)
                sin_t = np.sin(theta)
                
                # 沿梯度方向插值
                weight = np.abs(cos_t) if np.abs(cos_t) > np.abs(sin_t) else np.abs(sin_t)
                
                neighbor1 = magnitude[y + int(round(sin_t)), x + int(round(cos_t))]
                neighbor2 = magnitude[y - int(round(sin_t)), x - int(round(cos_t))]
                
                if magnitude[y, x] > neighbor1 and magnitude[y, x] > neighbor2:
                    edges[y, x] = magnitude[y, x]
        
        # 阈值化
        edges = edges / (edges.max() + 1e-6)
        edges = (edges > threshold).astype(float)
        
        return edges
    
    def detect_corners(
        self,
        image: np.ndarray,
        window_size: int = 5
    ) -> List[Tuple[int, int]]:
        """角点检测
        
        使用多尺度Gaborcharacteristics检测角点
        
        Args:
            image: 输入图像
            window_size: 窗口大小
            
        Returns:
            角点位置列表
        """
        self.build_feature_maps(image)
        
        h, w = self.feature_maps["magnitude"].shape
        corners = []
        
        magnitude = self.feature_maps["magnitude"]
        
        for y in range(window_size, h - window_size):
            for x in range(window_size, w - window_size):
                window = magnitude[y-window_size:y+window_size+1, 
                                  x-window_size:x+window_size+1]
                
                # Harris角点检测
                if len(window.shape) == 2:
                    Ix = np.diff(window, axis=1)
                    Iy = np.diff(window, axis=0)
                    
                    Ixx = Ix**2
                    Iyy = Iy**2
                    Ixy = Ix * Iy
                    
                    Sxx = np.sum(Ixx)
                    Syy = np.sum(Iyy)
                    Sxy = np.sum(Ixy)
                    
                    det = Sxx * Syy - Sxy**2
                    trace = Sxx + Syy
                    
                    if trace > 0:
                        R = det - 0.04 * trace**2
                        
                        if R > 0.1 * magnitude.max():
                            corners.append((x, y))
        
        return corners
    
    def create_orientation_histogram(
        self,
        image: np.ndarray,
        n_bins: int = 36
    ) -> np.ndarray:
        """创建方位直方图
        
        Args:
            image: 输入图像
            n_bins: 直方图bins数
            
        Returns:
            方位直方图
        """
        self.build_feature_maps(image)
        
        orientation_map = self.feature_maps["orientation"]
        magnitude_map = self.feature_maps["magnitude"]
        
        histogram = np.zeros(n_bins)
        bin_width = np.pi / n_bins
        
        h, w = orientation_map.shape
        for y in range(h):
            for x in range(w):
                theta = orientation_map[y, x]
                mag = magnitude_map[y, x]
                
                bin_idx = int(theta / bin_width) % n_bins
                histogram[bin_idx] += mag
        
        # 归一化
        if histogram.sum() > 0:
            histogram = histogram / histogram.sum()
        
        return histogram
    
    def match_features(
        self,
        features1: List[FeatureResponse],
        features2: List[FeatureResponse],
        max_distance: float = 10.0,
        orientation_tolerance: float = 0.1
    ) -> List[Tuple[FeatureResponse, FeatureResponse]]:
        """characteristics匹配
        
        匹配两组characteristics
        
        Args:
            features1: 第一组characteristics
            features2: 第二组characteristics
            max_distance: 最大位置距离
            orientation_tolerance: 方位容差
            
        Returns:
            匹配对列表
        """
        matches = []
        
        for f1 in features1:
            best_match = None
            best_score = float('inf')
            
            for f2 in features2:
                # 位置距离
                pos_dist = np.sqrt(
                    (f1.position[0] - f2.position[0])**2 +
                    (f1.position[1] - f2.position[1])**2
                )
                
                # 方位差异
                ori_diff = abs(f1.orientation - f2.orientation)
                ori_diff = min(ori_diff, np.pi - ori_diff)
                
                # 计算匹配分数
                score = pos_dist + 10 * ori_diff
                
                if pos_dist < max_distance and ori_diff < orientation_tolerance:
                    if score < best_score:
                        best_score = score
                        best_match = f2
            
            if best_match:
                matches.append((f1, best_match))
        
        return matches

class GaborFeatureSystem:
    """Gaborcharacteristics系统主类
    
    提供unified的接口访问Gaborcharacteristics功能
    """
    
    def __init__(
        self,
        n_orientations: int = 8,
        n_scales: int = 5
    ):
        """init"""
        self.name = "GaborFeatureSystem"
        self.version="6.2.0"
        
        self.multi_scale = MultiScaleFeatureSystem(
            n_orientations=n_orientations,
            n_scales=n_scales
        )
    
    def analyze_image(
        self,
        image: np.ndarray,
        extract_edges: bool = True,
        extract_corners: bool = True,
        create_histogram: bool = True
    ) -> Dict[str, Any]:
        """分析图像
        
        Args:
            image: 输入图像
            extract_edges: 是否提取边缘
            extract_corners: 是否提取角点
            create_histogram: 是否创建直方图
            
        Returns:
            分析结果
        """
        results = {}
        
        # 提取characteristics
        features = self.multi_scale.extract_features(image)
        results["n_features"] = len(features)
        
        # 构建characteristics图
        self.multi_scale.build_feature_maps(image)
        
        # 边缘检测
        if extract_edges:
            edges = self.multi_scale.detect_edges(image)
            results["edges"] = edges
            results["n_edges"] = int(np.sum(edges > 0))
        
        # 角点检测
        if extract_corners:
            corners = self.multi_scale.detect_corners(image)
            results["corners"] = corners
            results["n_corners"] = len(corners)
        
        # 方位直方图
        if create_histogram:
            hist = self.multi_scale.create_orientation_histogram(image)
            results["orientation_histogram"] = hist
        
        # characteristics图
        results["feature_maps"] = self.multi_scale.feature_maps
        
        return results
    
    def get_texture_descriptor(
        self,
        image: np.ndarray,
        cell_size: int = 8
    ) -> np.ndarray:
        """纹理描述符
        
        使用Gaborcharacteristics创建纹理描述符
        
        Args:
            image: 输入图像
            cell_size: 单元格大小
            
        Returns:
            纹理描述符
        """
        h, w = image.shape[:2]
        
        descriptors = []
        
        for y in range(0, h - cell_size + 1, cell_size):
            for x in range(0, w - cell_size + 1, cell_size):
                cell = image[y:y+cell_size, x:x+cell_size]
                
                # 计算该单元格的Gaborcharacteristics
                responses = self.multi_scale.filter_bank.filter_image(cell)
                
                # 统计characteristics
                cell_descriptor = []
                for response in responses:
                    cell_descriptor.append(np.mean(response))
                    cell_descriptor.append(np.std(response))
                
                descriptors.append(cell_descriptor)
        
        return np.array(descriptors)

# ==================== 工厂函数 ====================

def create_gabor_system(
    n_orientations: int = 8,
    n_scales: int = 5
) -> GaborFeatureSystem:
    """创建Gaborcharacteristics系统"""
    return GaborFeatureSystem(n_orientations, n_scales)

def get_gabor_insights() -> List[str]:
    """getGaborcharacteristics的关键洞见"""
    return [
        "Gabor函数完美模拟视觉皮层简单细胞的感受野",
        "方位选择性:神经元对特定方向的边缘/条纹响应最强",
        "空间频率选择性:不同尺度检测不同粒度的characteristics",
        "多尺度整合:从小尺度细节到大尺度轮廓",
        "Gabor滤波器组提供完备的空间-频率表示",
        "相位的稳定性可用于形状recognize"
    ]

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
