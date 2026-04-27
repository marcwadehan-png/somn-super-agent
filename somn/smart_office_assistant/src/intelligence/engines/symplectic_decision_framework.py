# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_constraints',
    'analyze_phase_structure',
    'canonical_transform',
    'compute_action',
    'compute_manifold_curvature',
    'compute_optimal_trajectory',
    'create_symplectic_framework',
    'evolve_decision',
    'from_vector',
    'get_decision_gradient',
    'get_symplectic_insights',
    'hamilton_equations',
    'harmonic_oscillator_hamiltonian',
    'initialize_state',
    'leapfrog',
    'measure_uncertainty',
    'quadratic_hamiltonian',
    'set_hamiltonian',
    'symplectic_map',
    'to_vector',
    'verlet',
]

辛几何decision框架 v1.0.0
===================

辛几何decision框架

核心来源:
- 辛几何(Symplectic Geometry):描述相空间的几何结构
- 哈密顿力学:物理系统的几何形式化
- 视觉皮层的辛结构模型(Citti, Sarti, Petitot)

核心理论:
1. 辛形式保持:相空间体积守恒(Liouville定理)
2. 哈密顿向量场:decision动力学的几何描述
3. 辛mapping:保持辛结构的变换
4. 母函数:generate辛mapping的势函数

核心思想:
- decision状态 = 广义坐标 + 广义动量
- decision演化 = 哈密顿方程
- 最优decision = 辛流上的测地线

@author: Somn AI
@version: 1.0.0
@date: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import math

class DecisionPhase(Enum):
    """decision相位"""
    POSITION = "position"         # 位置/状态
    MOMENTUM = "momentum"         # 动量/趋势
    HAMILTONIAN = "hamiltonian"  # 能量/目标函数
    TRAJECTORY = "trajectory"     # 轨迹/路径

@dataclass
class PhaseSpacePoint:
    """相空间点
    
    decision状态的辛几何表示
    """
    q: np.ndarray           # 广义坐标(位置)
    p: np.ndarray           # 广义动量(趋势)
    t: float = 0.0         # 时间
    
    def to_vector(self) -> np.ndarray:
        """转换为向量"""
        return np.concatenate([self.q, self.p])
    
    @classmethod
    def from_vector(cls, vec: np.ndarray) -> 'PhaseSpacePoint':
        """从向量创建"""
        n = len(vec) // 2
        return cls(q=vec[:n], p=vec[n:])
    
    def canonical_transform(self, M: np.ndarray) -> 'PhaseSpacePoint':
        """正则变换"""
        # M必须是辛矩阵 (M^T * J * M = J)
        J = self._symplectic_matrix(len(self.q))
        if np.allclose(M.T @ J @ M, J):
            new_vec = M @ self.to_vector()
            return PhaseSpacePoint.from_vector(new_vec)
        else:
            raise ValueError("Transformation matrix must be symplectic")
    
    @staticmethod
    def _symplectic_matrix(n: int) -> np.ndarray:
        """创建辛矩阵J"""
        J = np.zeros((2*n, 2*n))
        J[:n, n:] = np.eye(n)
        J[n:, :n] = -np.eye(n)
        return J

@dataclass
class HamiltonianSystem:
    """哈密顿系统
    
    decision动力学的基本框架
    """
    name: str
    H: Callable[[np.ndarray, float], float]  # 哈密顿量函数
    dHdq: Callable[[np.ndarray, float], np.ndarray]  # ∂H/∂q
    dHdp: Callable[[np.ndarray, float], np.ndarray]  # ∂H/∂p
    
    def hamilton_equations(
        self,
        state: PhaseSpacePoint,
        dt: float = 0.01
    ) -> PhaseSpacePoint:
        """哈密顿方程
        
        dq/dt = ∂H/∂p
        dp/dt = -∂H/∂q
        
        Args:
            state: 当前状态
            dt: 时间步长
            
        Returns:
            下一状态
        """
        q, p = state.q, state.p
        t = state.t
        
        # 计算偏导数
        dq = self.dHdp(q, p, t)
        dp = -self.dHdq(q, p, t)
        
        # 更新状态
        new_q = q + dq * dt
        new_p = p + dp * dt
        
        return PhaseSpacePoint(q=new_q, p=new_p, t=t + dt)
    
    def compute_action(
        self,
        trajectory: List[PhaseSpacePoint]
    ) -> float:
        """计算作用量
        
        S = ∫ L dt = ∫ (p·dq - H dt)
        
        Args:
            trajectory: 轨迹点列表
            
        Returns:
            作用量
        """
        action = 0.0
        
        for i in range(len(trajectory) - 1):
            state1 = trajectory[i]
            state2 = trajectory[i + 1]
            
            # p·dq
            dq = state2.q - state1.q
            p_avg = (state1.p + state2.p) / 2
            action += np.dot(p_avg, dq)
            
            # -H dt
            dt = state2.t - state1.t
            H_avg = (self.H(state1.q, state1.p, state1.t) + 
                    self.H(state2.q, state2.p, state2.t)) / 2
            action -= H_avg * dt
        
        return action

@dataclass
class SymplecticIntegrator:
    """辛积分器
    
    保持辛结构的数值积分方法
    """
    
    @staticmethod
    def leapfrog(
        system: HamiltonianSystem,
        state: PhaseSpacePoint,
        dt: float,
        n_steps: int = 1
    ) -> PhaseSpacePoint:
        """蛙跳算法(半步跳算法)
        
        优点:保持辛结构,长期稳定
        
        Args:
            system: 哈密顿系统
            state: 初始状态
            dt: 时间步长
            n_steps: 步数
            
        Returns:
            最终状态
        """
        q, p = state.q.copy(), state.p.copy()
        t = state.t
        
        for _ in range(n_steps):
            # 半步更新动量
            p_half = p - 0.5 * dt * system.dHdq(q, p, t)
            
            # 全步更新坐标
            q_new = q + dt * system.dHdp(q, p_half, t)
            
            # 半步更新动量
            p_new = p_half - 0.5 * dt * system.dHdq(q_new, p_half, t + dt)
            
            q, p = q_new, p_new
            t += dt
        
        return PhaseSpacePoint(q=q, p=p, t=t)
    
    @staticmethod
    def verlet(
        system: HamiltonianSystem,
        state: PhaseSpacePoint,
        dt: float,
        n_steps: int = 1
    ) -> PhaseSpacePoint:
        """Stormer-Verlet算法
        
        Args:
            system: 哈密顿系统
            state: 初始状态
            dt: 时间步长
            n_steps: 步数
            
        Returns:
            最终状态
        """
        q, p = state.q.copy(), state.p.copy()
        t = state.t
        
        for _ in range(n_steps):
            # 计算加速度
            a = -system.dHdq(q, p, t)
            
            # Velocity Verlet
            p_new = p + 0.5 * dt * a
            q_new = q + dt * system.dHdp(q, p_new, t)
            a_new = -system.dHdq(q_new, p_new, t + dt)
            p_new = p_new + 0.5 * dt * a_new
            
            q, p = q_new, p_new
            t += dt
        
        return PhaseSpacePoint(q=q, p=p, t=t)

class SymplecticDecisionFramework:
    """辛几何decision框架
    
    辛几何decision系统
    
    核心思想:
    1. decision状态 → 相空间点
    2. decision演化 → 哈密顿动力学
    3. 最优decision → 辛流上的测地线
    4. decision不确定性 → 相空间体积(Liouville定理)
    
    应用场景:
    1. 多目标decision的相空间表示
    2. decision路径的辛几何优化
    3. decision不确定性的几何量化
    """
    
    def __init__(self, n_dimensions: int = 3):
        """init
        
        Args:
            n_dimensions: decision空间维度
        """
        self.name = "SymplecticDecisionFramework"
        self.version = "1.0.0"
        
        self.n_dims = n_dimensions
        
        # 辛矩阵
        self.J = PhaseSpacePoint._symplectic_matrix(n_dimensions)
        
        # 当前decision状态
        self.current_state: Optional[PhaseSpacePoint] = None
        
        # decision历史
        self.decision_history: List[PhaseSpacePoint] = []
        
        # 哈密顿系统
        self.hamiltonian_system: Optional[HamiltonianSystem] = None
        
        # 积分器
        self.integrator = SymplecticIntegrator()
    
    def set_hamiltonian(
        self,
        H_func: Callable[[np.ndarray, np.ndarray, float], float],
        dHdq_func: Callable[[np.ndarray, np.ndarray, float], np.ndarray],
        dHdp_func: Callable[[np.ndarray, np.ndarray, float], np.ndarray],
        name: str = "DecisionHamiltonian"
    ):
        """设置哈密顿量
        
        Args:
            H_func: 哈密顿量函数 H(q, p, t)
            dHdq_func: ∂H/∂q
            dHdp_func: ∂H/∂p
            name: 系统名称
        """
        self.hamiltonian_system = HamiltonianSystem(
            name=name,
            H=H_func,
            dHdq=dHdq_func,
            dHdp=dHdp_func
        )
    
    def initialize_state(
        self,
        q0: np.ndarray,
        p0: np.ndarray
    ) -> PhaseSpacePoint:
        """initdecision状态
        
        Args:
            q0: 初始位置(decision变量值)
            p0: 初始动量(decision趋势)
            
        Returns:
            相空间点
        """
        self.current_state = PhaseSpacePoint(q=q0, p=p0, t=0.0)
        self.decision_history = [self.current_state]
        return self.current_state
    
    def evolve_decision(
        self,
        dt: float,
        n_steps: int = 1,
        integrator: str = "leapfrog"
    ) -> PhaseSpacePoint:
        """演化decision
        
        根据哈密顿动力学演化decision状态
        
        Args:
            dt: 时间步长
            n_steps: 步数
            integrator: 积分器类型 ('leapfrog' 或 'verlet')
            
        Returns:
            最终状态
        """
        if self.hamiltonian_system is None:
            raise ValueError("Hamiltonian system not set")
        
        if self.current_state is None:
            raise ValueError("State not initialized")
        
        state = self.current_state
        
        for _ in range(n_steps):
            if integrator == "leapfrog":
                state = self.integrator.leapfrog(
                    self.hamiltonian_system, state, dt
                )
            else:
                state = self.integrator.verlet(
                    self.hamiltonian_system, state, dt
                )
            
            self.decision_history.append(state)
        
        self.current_state = state
        return state
    
    def compute_optimal_trajectory(
        self,
        initial_state: PhaseSpacePoint,
        final_time: float,
        dt: float = 0.01
    ) -> List[PhaseSpacePoint]:
        """计算最优轨迹
        
        变分原理:作用量极值的轨迹
        
        Args:
            initial_state: 初始状态
            final_time: 终止时间
            dt: 时间步长
            
        Returns:
            最优轨迹
        """
        if self.hamiltonian_system is None:
            raise ValueError("Hamiltonian system not set")
        
        trajectory = [initial_state]
        state = initial_state
        t = 0.0
        
        n_steps = int(final_time / dt)
        
        for _ in range(n_steps):
            state = self.integrator.leapfrog(
                self.hamiltonian_system, state, dt
            )
            trajectory.append(state)
            t += dt
        
        return trajectory
    
    def measure_uncertainty(self) -> float:
        """测量decision不确定性
        
        基于Liouville定理:相空间体积守恒
        不确定性 = 相空间体积
        
        Returns:
            不确定性度量
        """
        if not self.decision_history:
            return 0.0
        
        # 计算相空间分布
        q_values = np.array([s.q for s in self.decision_history])
        p_values = np.array([s.p for s in self.decision_history])
        
        # 计算体积(协方差行列式)
        q_cov = np.cov(q_values.T) + np.eye(self.n_dims) * 1e-6
        p_cov = np.cov(p_values.T) + np.eye(self.n_dims) * 1e-6
        
        # 体积估计
        volume = np.sqrt(np.linalg.det(q_cov) * np.linalg.det(p_cov))
        
        return volume
    
    def symplectic_map(
        self,
        M: np.ndarray
    ) -> PhaseSpacePoint:
        """辛mapping
        
        保持辛结构的变换
        
        Args:
            M: 辛矩阵
            
        Returns:
            变换后的状态
        """
        if self.current_state is None:
            raise ValueError("State not initialized")
        
        return self.current_state.canonical_transform(M)
    
    def get_decision_gradient(self) -> Tuple[np.ndarray, np.ndarray]:
        """getdecision梯度
        
        Returns:
            (位置梯度, 动量梯度)
        """
        if self.current_state is None or self.hamiltonian_system is None:
            return np.zeros(self.n_dims), np.zeros(self.n_dims)
        
        q, p = self.current_state.q, self.current_state.p
        t = self.current_state.t
        
        dq = self.hamiltonian_system.dHdp(q, p, t)
        dp = -self.hamiltonian_system.dHdq(q, p, t)
        
        return dq, dp
    
    def analyze_phase_structure(self) -> Dict[str, Any]:
        """分析相空间结构
        
        Returns:
            相空间分析结果
        """
        if not self.decision_history:
            return {"error": "No history"}
        
        q_values = np.array([s.q for s in self.decision_history])
        p_values = np.array([s.p for s in self.decision_history])
        
        return {
            "n_points": len(self.decision_history),
            "q_mean": np.mean(q_values, axis=0),
            "q_std": np.std(q_values, axis=0),
            "p_mean": np.mean(p_values, axis=0),
            "p_std": np.std(p_values, axis=0),
            "uncertainty": self.measure_uncertainty(),
            "trajectory_length": len(self.decision_history),
            "time_span": self.decision_history[-1].t - self.decision_history[0].t
        }

class DecisionGeometryAnalyzer:
    """decision几何分析器
    
    分析decision问题的几何结构
    """
    
    def __init__(self):
        self.name = "DecisionGeometryAnalyzer"
    
    def analyze_constraints(
        self,
        constraints: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """分析约束的几何结构
        
        Args:
            constraints: 约束列表
            
        Returns:
            几何分析结果
        """
        analysis = {
            "n_constraints": len(constraints),
            "equality": [],
            "inequality": [],
            "geometric_types": []
        }
        
        for c in constraints:
            c_type = c.get("type", "unknown")
            
            if c_type == "equality":
                analysis["equality"].append(c)
            else:
                analysis["inequality"].append(c)
            
            # recognize几何类型
            if "linear" in c.get("form", ""):
                analysis["geometric_types"].append("hyperplane")
            elif "quadratic" in c.get("form", ""):
                analysis["geometric_types"].append("quadratic_surface")
            else:
                analysis["geometric_types"].append("general")
        
        return analysis
    
    def compute_manifold_curvature(
        self,
        trajectory: List[PhaseSpacePoint]
    ) -> float:
        """计算流形曲率
        
        Args:
            trajectory: 轨迹点
            
        Returns:
            平均曲率
        """
        if len(trajectory) < 3:
            return 0.0
        
        curvatures = []
        
        for i in range(1, len(trajectory) - 1):
            q_prev = trajectory[i-1].q
            q_curr = trajectory[i].q
            q_next = trajectory[i+1].q
            
            # 曲率计算
            v1 = q_curr - q_prev
            v2 = q_next - q_curr
            
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            
            if norm_v1 > 1e-6 and norm_v2 > 1e-6:
                cos_angle = np.dot(v1, v2) / (norm_v1 * norm_v2)
                angle = np.arccos(np.clip(cos_angle, -1, 1))
                curvatures.append(angle)
        
        return np.mean(curvatures) if curvatures else 0.0

def create_symplectic_framework(n_dims: int = 3) -> SymplecticDecisionFramework:
    """创建辛几何decision框架"""
    return SymplecticDecisionFramework(n_dims=n_dims)

def get_symplectic_insights() -> List[str]:
    """get辛几何的关键洞见"""
    return [
        "辛几何描述相空间的几何结构:位置+动量",
        "哈密顿方程是decision动力学的几何形式",
        "辛积分保持相空间体积(Liouville定理)",
        "decision不确定性 = 相空间体积",
        "最优decision轨迹 = 辛流上的测地线",
        "正则变换保持辛结构"
    ]

# ==================== 预设哈密顿量 ====================

def quadratic_hamiltonian(
    q: np.ndarray,
    p: np.ndarray,
    t: float,
    A: np.ndarray = None,
    mass: float = 1.0
) -> float:
    """二次哈密顿量
    
    H = p²/2m + V(q)
    
    Args:
        q: 位置
        p: 动量
        t: 时间
        A: 势能矩阵
        mass: 质量
        
    Returns:
        哈密顿量值
    """
    kinetic = np.sum(p**2) / (2 * mass)
    
    if A is not None:
        potential = 0.5 * q @ A @ q
    else:
        potential = 0.0
    
    return kinetic + potential

def harmonic_oscillator_hamiltonian(
    q: np.ndarray,
    p: np.ndarray,
    t: float,
    k: float = 1.0,
    mass: float = 1.0
) -> float:
    """谐振子哈密顿量
    
    H = p²/2m + kq²/2
    
    Args:
        q: 位置
        p: 动量
        t: 时间
        k: 弹簧常数
        mass: 质量
        
    Returns:
        哈密顿量值
    """
    return np.sum(p**2) / (2 * mass) + 0.5 * k * np.sum(q**2)

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
