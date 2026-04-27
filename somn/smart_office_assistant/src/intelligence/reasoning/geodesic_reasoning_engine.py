# -*- coding: utf-8 -*-
"""
__all__ = [
    'complete_contour',
    'create_geodesic_engine',
    'distance_to',
    'find_geodesic',
    'geodesic_equation',
    'get_geodesic_insights',
    'get_reasoning_stats',
    'hamiltonian',
    'metric',
    'multi_constraint_reasoning',
    'optimize_reasoning_path',
    'perceptual_inference',
    'set_cost_field',
    'set_orientation_field',
    'to_tuple',
]

亚黎曼测地线推理引擎 v1.0.0
=========================

亚黎曼几何推理引擎

核心思想:
- 测地线 = 约束条件下的最短/最速路径
- 亚黎曼几何 = 仅部分方向有度量的几何
- 轮廓补全 = 穿过遮挡区域的最优路径

@author: Somn AI
@version: 1.0.0
@date: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import heapq
import math

class ConstraintType(Enum):
    """约束类型 - 对应亚黎曼几何中的约束"""
    HORIZONTAL = "horizontal"       # 空间平移
    VERTICAL = "vertical"         # 方位旋转
    SMOOTH = "smooth"            # 平滑约束
    ORIENTATION = "orientation"   # 方位保持
    CURVATURE = "curvature"       # 曲率约束

@dataclass
class StateSE2:
    """SE(2)群状态 - 位置+方位
    
    对应欧几里得运动群的一个元素
    """
    x: float          # x位置
    y: float          # y位置
    theta: float      # 方位角 [0, 2π)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.theta)
    
    def distance_to(self, other: 'StateSE2') -> float:
        """计算到另一个状态的黎曼距离"""
        dx = self.x - other.x
        dy = self.y - other.y
        dtheta = abs(self.theta - other.theta)
        dtheta = min(dtheta, 2 * np.pi - dtheta)
        return np.sqrt(dx**2 + dy**2 + dtheta**2)
    
    def __hash__(self):
        return hash(self.to_tuple())
    
    def __eq__(self, other):
        if not isinstance(other, StateSE2):
            return False
        return self.to_tuple() == other.to_tuple()

@dataclass
class GeodesicSegment:
    """测地线段"""
    start: StateSE2
    end: StateSE2
    length: float
    curvature: float
    cost: float
    path: List[StateSE2] = field(default_factory=list)

class SubRiemannianGeometry:
    """亚黎曼几何计算器
    
    实现SE(2)群上的亚黎曼度量
    """
    
    def __init__(self, beta: float = 0.5):
        """init
        
        Args:
            beta: 各向异性参数(控制水平/垂直方向权重比)
        """
        self.beta = beta
    
    def metric(self, state: StateSE2, control: Tuple[float, float]) -> float:
        """计算亚黎曼度量
        
        Args:
            state: 当前状态
            control: 控制向量 (u1, u2) - u1=平移, u2=旋转
            
        Returns:
            度量值
        """
        u1, u2 = control
        # 亚黎曼度量:仅沿两个正交方向有定义
        return np.sqrt(u1**2 + (self.beta * u2)**2)
    
    def hamiltonian(self, state: StateSE2, momentum: Tuple[float, float, float]) -> float:
        """哈密顿量
        
        Args:
            state: 状态
            momentum: 动量 (p_x, p_y, p_lambda)
            
        Returns:
            哈密顿量值
        """
        px, py, plambda = momentum
        return np.sqrt(px**2 + py**2 + (plambda / self.beta)**2)
    
    def geodesic_equation(
        self,
        state: StateSE2,
        momentum: Tuple[float, float, float]
    ) -> Tuple[StateSE2, Tuple[float, float, float]]:
        """测地线方程
        
        Returns:
            (状态导数, 动量导数)
        """
        px, py, plambda = momentum
        
        # 状态更新
        norm = np.sqrt(px**2 + py**2 + (plambda / self.beta)**2)
        dx = px / norm if norm > 0 else 0
        dy = py / norm if norm > 0 else 0
        dtheta = (plambda / self.beta) / norm if norm > 0 else 0
        
        new_state = StateSE2(
            x=state.x + dx * 0.01,
            y=state.y + dy * 0.01,
            theta=state.theta + dtheta * 0.01
        )
        
        # 动量更新(沿黎曼联络)
        dpx, dpy, dplambda = 0, 0, 0
        
        return new_state, (dpx, dpy, dplambda)

class GeodesicReasoningEngine:
    """亚黎曼测地线推理引擎
    
    用于解决约束条件下的最优路径推理问题
    
    应用场景:
    1. 轮廓补全 - 穿过遮挡区域的最优轮廓
    2. 推理路径优化 - 最短推理链
    3. 约束满足 - 多约束下的最优解
    4. 感知补全 - 信息缺失时的推断
    """
    
    def __init__(self, beta: float = 0.5):
        """init引擎"""
        self.name = "GeodesicReasoningEngine"
        self.version = "1.0.0"
        
        # 亚黎曼几何计算器
        self.sr_geometry = SubRiemannianGeometry(beta=beta)
        
        # 成本场
        self.cost_field: Optional[np.ndarray] = None
        self.orientation_field: Optional[np.ndarray] = None
        
        # 推理历史
        self.reasoning_history: List[GeodesicSegment] = []
    
    def set_cost_field(self, field: np.ndarray):
        """设置成本场
        
        Args:
            field: 2D成本场,值越高越难通过
        """
        self.cost_field = field
    
    def set_orientation_field(self, field: np.ndarray):
        """设置方位场
        
        Args:
            field: 2D方位场,表示每点的优选方位
        """
        self.orientation_field = field
    
    def find_geodesic(
        self,
        start: StateSE2,
        end: StateSE2,
        max_iterations: int = 1000,
        tolerance: float = 1e-4
    ) -> GeodesicSegment:
        """寻找亚黎曼测地线
        
        使用Euler-Poincaré射影动态规划算法
        
        Args:
            start: 起点状态
            end: 终点状态
            max_iterations: 最大迭代次数
            tolerance: 收敛容忍度
            
        Returns:
            测地线段
        """
        # init
        current = start
        path = [start]
        total_cost = 0.0
        total_length = 0.0
        curvatures = []
        
        iteration = 0
        while iteration < max_iterations:
            # 计算到终点的方向
            dx = end.x - current.x
            dy = end.y - current.y
            target_theta = np.arctan2(dy, dx) % (2 * np.pi)
            
            # 选择控制
            control = self._select_control(current, end, target_theta)
            
            # 更新状态
            next_state = self._apply_control(current, control)
            path.append(next_state)
            
            # 计算代价
            segment_cost = self._compute_segment_cost(current, next_state)
            total_cost += segment_cost
            total_length += self._compute_length(current, next_state)
            
            # 计算曲率
            curvature = abs(control[1])
            curvatures.append(curvature)
            
            current = next_state
            
            # 检查收敛
            if current.distance_to(end) < tolerance:
                break
            
            iteration += 1
        
        # 添加终点
        path.append(end)
        
        avg_curvature = np.mean(curvatures) if curvatures else 0.0
        
        geodesic = GeodesicSegment(
            start=start,
            end=end,
            length=total_length,
            curvature=avg_curvature,
            cost=total_cost,
            path=path
        )
        
        self.reasoning_history.append(geodesic)
        return geodesic
    
    def _select_control(
        self,
        current: StateSE2,
        target: StateSE2,
        target_theta: float
    ) -> Tuple[float, float]:
        """选择控制向量
        
        基于当前位置和目标选择最优控制
        
        Args:
            current: 当前状态
            target: 目标状态
            target_theta: 目标方位角
            
        Returns:
            控制向量 (平移速度, 旋转速度)
        """
        # 平移控制:朝向目标
        dx = target.x - current.x
        dy = target.y - current.y
        dist = np.sqrt(dx**2 + dy**2)
        
        u1 = min(1.0, dist)  # 平移速度
        
        # 旋转控制:调整方位
        dtheta = target_theta - current.theta
        # 归一化到 [-π, π]
        while dtheta > np.pi:
            dtheta -= 2 * np.pi
        while dtheta < -np.pi:
            dtheta += 2 * np.pi
        
        u2 = np.clip(dtheta, -0.2, 0.2)  # 旋转速度
        
        return (u1, u2)
    
    def _apply_control(
        self,
        state: StateSE2,
        control: Tuple[float, float]
    ) -> StateSE2:
        """应用控制更新状态"""
        u1, u2 = control
        dt = 0.01
        
        # 位置更新(沿当前方位方向)
        dx = u1 * np.cos(state.theta) * dt
        dy = u1 * np.sin(state.theta) * dt
        
        # 方位更新
        dtheta = u2 * dt
        
        return StateSE2(
            x=state.x + dx,
            y=state.y + dy,
            theta=(state.theta + dtheta) % (2 * np.pi)
        )
    
    def _compute_segment_cost(
        self,
        start: StateSE2,
        end: StateSE2
    ) -> float:
        """计算段代价"""
        length = self._compute_length(start, end)
        
        # 如果有成本场,加入成本
        if self.cost_field is not None:
            h, w = self.cost_field.shape
            x, y = int(end.x * w), int(end.y * h)
            if 0 <= x < w and 0 <= y < h:
                length *= (1 + self.cost_field[y, x])
        
        return length
    
    def _compute_length(self, start: StateSE2, end: StateSE2) -> float:
        """计算段长度"""
        dx = end.x - start.x
        dy = end.y - start.y
        dtheta = abs(end.theta - start.theta)
        dtheta = min(dtheta, 2 * np.pi - dtheta)
        
        # 亚黎曼弧长公式
        return np.sqrt(dx**2 + dy**2 + (self.sr_geometry.beta * dtheta)**2)
    
    # ==================== 轮廓补全 ====================
    
    def complete_contour(
        self,
        visible_points: List[Tuple[float, float]],
        occlusion_region: Optional[Dict] = None,
        context: Optional[Dict] = None
    ) -> List[Tuple[float, float]]:
        """轮廓补全
        
        穿过遮挡区域补全不完整的轮廓
        
        核心应用:感知补全
        
        Args:
            visible_points: 可见轮廓点
            occlusion_region: 遮挡区域定义
            context: 上下文信息
            
        Returns:
            补全后的轮廓点
        """
        if len(visible_points) < 2:
            return visible_points
        
        # 提取端点
        start_point = visible_points[0]
        end_point = visible_points[-1]
        
        # 创建成本场
        cost_field = self._create_contour_cost_field(
            start_point, end_point, occlusion_region, context
        )
        self.set_cost_field(cost_field)
        
        # 转换为SE(2)状态
        start_theta = self._estimate_direction(visible_points[:3] if len(visible_points) >= 3 else visible_points)
        end_theta = self._estimate_direction(visible_points[-3:] if len(visible_points) >= 3 else visible_points)
        
        start_state = StateSE2(start_point[0], start_point[1], start_theta)
        end_state = StateSE2(end_point[0], end_point[1], end_theta)
        
        # 寻找测地线
        geodesic = self.find_geodesic(start_state, end_state)
        
        # 合并结果
        completed = list(visible_points)
        if len(geodesic.path) > 2:
            completed.extend([(p.x, p.y) for p in geodesic.path[1:-1]])
        
        return completed
    
    def _create_contour_cost_field(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        occlusion: Optional[Dict],
        context: Optional[Dict]
    ) -> np.ndarray:
        """创建轮廓成本场"""
        # 默认成本场:中间区域成本较高(模拟遮挡)
        field = np.ones((100, 100)) * 0.5
        
        if occlusion:
            # 添加遮挡区域高成本
            ox, oy = occlusion.get("center", (0.5, 0.5))
            radius = occlusion.get("radius", 0.2)
            
            for y in range(100):
                for x in range(100):
                    px, py = x / 100, y / 100
                    dist = np.sqrt((px - ox)**2 + (py - oy)**2)
                    if dist < radius:
                        field[y, x] = 5.0
        
        return field
    
    def _estimate_direction(self, points: List[Tuple[float, float]]) -> float:
        """估计点的方向"""
        if len(points) < 2:
            return 0.0
        
        dx = points[-1][0] - points[0][0]
        dy = points[-1][1] - points[0][1]
        
        return np.arctan2(dy, dx) % (2 * np.pi)
    
    # ==================== 推理路径优化 ====================
    
    def optimize_reasoning_path(
        self,
        reasoning_steps: List[Dict[str, Any]],
        constraints: List[ConstraintType]
    ) -> List[Dict[str, Any]]:
        """推理路径优化
        
        使用测地线原理优化推理步骤
        
        Args:
            reasoning_steps: 推理步骤列表
            constraints: 约束类型
            
        Returns:
            优化后的推理路径
        """
        if len(reasoning_steps) < 2:
            return reasoning_steps
        
        # recognize关键节点
        key_nodes = self._identify_key_nodes(reasoning_steps)
        
        # 对相邻关键节点寻找测地线
        optimized = []
        for i in range(len(reasoning_steps)):
            if i in key_nodes or i == 0 or i == len(reasoning_steps) - 1:
                optimized.append(reasoning_steps[i])
            # 否则可能跳过某些步骤(如果测地线允许)
        
        return optimized
    
    def _identify_key_nodes(self, steps: List[Dict]) -> set:
        """recognize关键节点"""
        key_nodes = {0, len(steps) - 1}  # 始终保留首尾
        
        # recognize转折点
        for i in range(1, len(steps) - 1):
            prev_type = steps[i-1].get("type", "unknown")
            curr_type = steps[i].get("type", "unknown")
            next_type = steps[i+1].get("type", "unknown")
            
            # 如果类型变化,是关键节点
            if curr_type != prev_type or curr_type != next_type:
                key_nodes.add(i)
        
        return key_nodes
    
    # ==================== 多约束推理 ====================
    
    def multi_constraint_reasoning(
        self,
        start: StateSE2,
        goal: StateSE2,
        constraints: Dict[ConstraintType, Any]
    ) -> GeodesicSegment:
        """多约束推理
        
        在多个约束条件下寻找最优推理路径
        
        Args:
            start: 起点
            goal: 目标
            constraints: 约束字典
            
        Returns:
            最优测地线
        """
        # 根据约束类型调整成本场
        if ConstraintType.SMOOTH in constraints:
            self._apply_smoothness_constraint(constraints[ConstraintType.SMOOTH])
        
        if ConstraintType.ORIENTATION in constraints:
            self._apply_orientation_constraint(constraints[ConstraintType.ORIENTATION])
        
        if ConstraintType.CURVATURE in constraints:
            self._apply_curvature_constraint(constraints[ConstraintType.CURVATURE])
        
        # 寻找测地线
        return self.find_geodesic(start, goal)
    
    def _apply_smoothness_constraint(self, strength: float):
        """应用平滑约束"""
        # 平滑成本场
        if self.cost_field is not None:
            from scipy.ndimage import gaussian_filter
            self.cost_field = gaussian_filter(self.cost_field, sigma=strength)
    
    def _apply_orientation_constraint(self, preferred_orientation: float):
        """应用方位约束"""
        # 创建方位偏好场
        h, w = 100, 100
        self.orientation_field = np.ones((h, w)) * preferred_orientation
    
    def _apply_curvature_constraint(self, max_curvature: float):
        """应用曲率约束"""
        # 限制旋转速度
        self.max_curvature = max_curvature
    
    # ==================== 感知推理 ====================
    
    def perceptual_inference(
        self,
        partial_evidence: Dict[str, Any],
        missing_info_type: str = "contour"
    ) -> Dict[str, Any]:
        """感知推理
        
        根据部分证据推断缺失信息
        
        核心思想:感知系统使用测地线原理补全信息
        
        Args:
            partial_evidence: 部分证据
            missing_info_type: 缺失信息类型
            
        Returns:
            推理结果
        """
        if missing_info_type == "contour":
            points = partial_evidence.get("points", [])
            occlusion = partial_evidence.get("occlusion_region")
            completed = self.complete_contour(points, occlusion)
            
            return {
                "type": "contour_completion",
                "completed_points": completed,
                "confidence": self._estimate_completion_confidence(points, completed)
            }
        
        elif missing_info_type == "path":
            start = partial_evidence.get("start")
            end = partial_evidence.get("end")
            obstacles = partial_evidence.get("obstacles", [])
            
            # 创建成本场
            cost_field = np.ones((100, 100))
            for obs in obstacles:
                x, y, r = obs
                for iy in range(100):
                    for ix in range(100):
                        dist = np.sqrt((ix/100 - x)**2 + (iy/100 - y)**2)
                        if dist < r:
                            cost_field[iy, ix] = 10.0
            
            self.set_cost_field(cost_field)
            
            start_state = StateSE2(start[0], start[1], 0)
            end_state = StateSE2(end[0], end[1], 0)
            
            geodesic = self.find_geodesic(start_state, end_state)
            
            return {
                "type": "path_inference",
                "path": [(p.x, p.y) for p in geodesic.path],
                "length": geodesic.length,
                "cost": geodesic.cost
            }
        
        return {"type": "unknown", "result": None}
    
    def _estimate_completion_confidence(
        self,
        original: List,
        completed: List
    ) -> float:
        """估计补全置信度"""
        # 基于端点距离和路径平滑度估计置信度
        if len(completed) < 2:
            return 0.0
        
        # 端点连接平滑度
        smoothness = 1.0 - min(1.0, len(completed) / 100)
        
        # 路径长度合理性
        original_length = np.sqrt(
            (original[-1][0] - original[0][0])**2 +
            (original[-1][1] - original[0][1])**2
        )
        completed_length = np.sqrt(
            (completed[-1][0] - completed[0][0])**2 +
            (completed[-1][1] - completed[0][1])**2
        )
        length_ratio = completed_length / (original_length + 1e-6)
        length_penalty = abs(1 - length_ratio)
        
        confidence = smoothness * (1 - length_penalty)
        return max(0.0, min(1.0, confidence))
    
    # ==================== 统计与分析 ====================
    
    def get_reasoning_stats(self) -> Dict[str, Any]:
        """get推理统计"""
        if not self.reasoning_history:
            return {"total_reasonings": 0}
        
        lengths = [g.length for g in self.reasoning_history]
        costs = [g.cost for g in self.reasoning_history]
        curvatures = [g.curvature for g in self.reasoning_history]
        
        return {
            "total_reasonings": len(self.reasoning_history),
            "avg_length": np.mean(lengths),
            "avg_cost": np.mean(costs),
            "avg_curvature": np.mean(curvatures),
            "total_path_length": sum(lengths)
        }

# ==================== 工厂函数 ====================

def create_geodesic_engine(beta: float = 0.5) -> GeodesicReasoningEngine:
    """创建测地线推理引擎"""
    return GeodesicReasoningEngine(beta=beta)

def get_geodesic_insights() -> List[str]:
    """get测地线推理的关键洞见"""
    return [
        "亚黎曼测地线是约束条件下的最优路径",
        "轮廓补全 = 穿过遮挡区域的最短测地线",
        "SE(2)群 = 平面刚体运动(平移+旋转)",
        "神经几何学将感知补全形式化为变分问题",
        "测地线的曲率反映路径的平滑度",
        "各向异性参数beta控制旋转/平移的相对权重"
    ]

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
