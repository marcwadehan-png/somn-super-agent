"""
__all__ = [
    'add_oscillator',
    'compute_order_parameter',
    'detect_sync_clusters',
    'evaluate',
    'get_interaction_function',
    'get_phase_order',
    'get_report',
    'get_sync_report',
    'reset_phase',
    'set_coupling',
    'set_rhythm_mode',
    'step',
    'strengthen_connection',
    'to_dict',
    'weaken_connection',
]

神经相位同步协调器 v1.0
Phase Synchronization Coordinator



核心功能:
1. 相位响应曲线 (PRC) - 模块对输入的时间敏感性
2. Kuramoto耦合模型 - 多模块同步协调
3. Winfree脉冲耦合 - 事件驱动的模块协调
4. 相位重置 - 任务切换时的状态管理
5. 脑节律模拟 - θ(学习)/α(抑制)/β(主动)/γ(绑定)节律
6. 同步簇检测 - recognize协同工作的模块组

神经科学→AI系统mapping:
  神经振荡器 → 智能体各功能模块
  相位 → 模块当前工作周期位置
  频率 → 模块处理速率
  耦合强度 → 模块间协作强度
  同步 → 多模块协调工作
  锁相 → 稳定的协作节律
  脑节律 → 不同认知模式的工作节律

v5.1.0 神经科学数学基础增强版
"""

import math
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from loguru import logger

# ============================================================
# 第一节: 相位响应曲线 (PRC)
# ============================================================

class PRCType(Enum):
    """PRC类型"""
    TYPE_I = "type_i"    # I型: 始终非负,刺激总是促进下一个放电
    TYPE_II = "type_ii"  # II型: 有正有负,晚期刺激可能延迟

@dataclass
class PhaseResponseCurve:
    """
    相位响应曲线 (Phase Response Curve)
    
    Ch.8核心概念: PRC描述了在振荡周期的不同时刻给予刺激时,
    下一个放电时间的变化量.
    
    PRC(φ) = Δφ = (T_new - T_old) / T_old
    其中 φ ∈ [0, 2π) 是刺激到达时的相位
    
    I型PRC (连续放电器):
    - PRC(φ) ≥ 0 对所有φ
    - 正弦耦合器容易产生同步
    
    II型PRC (不连续放电器):
    - PRC(φ) 有正有负
    - 晚期刺激会延迟下一个放电
    - 可能产生反相振荡
    """
    prc_type: PRCType = PRCType.TYPE_II
    
    # II型PRC参数
    phase_advance_peak: float = 0.0    # 最大提前的相位 (弧度)
    phase_advance_width: float = 1.0   # 提前区域的宽度 (弧度)
    phase_delay_peak: float = -0.3     # 最大延迟的相位 (弧度)
    phase_delay_width: float = 1.5     # 延迟区域的宽度 (弧度)
    
    def evaluate(self, stimulus_phase: float) -> float:
        """
        评估给定相位下的相位响应
        
        Args:
            stimulus_phase: 刺激到达时的相位 [0, 2π)
            
        Returns:
            相位变化 Δφ (弧度)
        """
        phi = stimulus_phase % (2 * math.pi)
        
        if self.prc_type == PRCType.TYPE_I:
            # I型: PRC ≈ sin(φ) 简化模型
            return 0.2 * math.sin(phi)
        else:
            # II型: 早期促进(提前), 晚期抑制(延迟)
            # 促进区域: 0 到 π
            advance = self.phase_advance_peak * math.exp(
                -((phi - self.phase_advance_width) ** 2) / (2 * 0.5 ** 2)
            )
            # 延迟区域: π 到 2π
            delay = self.phase_delay_peak * math.exp(
                -((phi - (self.phase_advance_width + math.pi)) ** 2) / (2 * 0.8 ** 2)
            )
            return advance + delay
    
    def get_interaction_function(self, coupling_strength: float, 
                                 n_samples: int = 64) -> List[float]:
        """
        计算相互作用函数 H(φ) = (1/T) ∫ Z(t) · I(t+φ) dt
        
        简化为: H(φ) ≈ coupling_strength × PRC(φ) × cos(φ)
        
        用于Kuramoto模型中的耦合项
        """
        H = []
        for i in range(n_samples):
            phi = 2 * math.pi * i / n_samples
            prc_val = self.evaluate(phi)
            H.append(coupling_strength * prc_val * math.cos(phi))
        return H

# ============================================================
# 第二节: 神经振荡器
# ============================================================

class BrainRhythm(Enum):
    """脑节律类型"""
    DELTA = "delta"    # 0.5-4 Hz: 深度睡眠
    THETA = "theta"    # 4-8 Hz: 学习与记忆
    ALPHA = "alpha"    # 8-12 Hz: 抑制控制
    BETA = "beta"      # 12-30 Hz: 主动思考
    GAMMA = "gamma"    # 30-100 Hz: 注意力绑定

@dataclass
class RhythmInfo:
    """脑节律信息"""
    name: str
    frequency: float    # Hz
    description: str
    cognitive_mode: str  # 对应认知模式
    duration_ms: float = 0.0  # 周期时长 (ms)
    
    def __post_init__(self):
        if self.duration_ms == 0 and self.frequency > 0:
            self.duration_ms = 1000.0 / self.frequency

# 预定义脑节律
BRAIN_RHYTHMS = {
    BrainRhythm.DELTA: RhythmInfo("δ", 2.0, "深度睡眠/无意识处理", "rest"),
    BrainRhythm.THETA: RhythmInfo("θ", 6.0, "学习记忆/情景编码", "learning"),
    BrainRhythm.ALPHA: RhythmInfo("α", 10.0, "抑制无关信息/注意力筛选", "filtering"),
    BrainRhythm.BETA: RhythmInfo("β", 20.0, "主动思考/decision执行", "active"),
    BrainRhythm.GAMMA: RhythmInfo("γ", 40.0, "多模块绑定/characteristics整合", "binding"),
}

@dataclass
class NeuralOscillator:
    """
    神经振荡器 - 模拟智能体功能模块的工作节律
    
    每个模块都有自然的振荡频率(处理速率)和当前相位(工作周期位置)
    
    动力学: dθ_i/dt = ω_i + Σ K_ij · H(θ_j - θ_i) + noise
    """
    id: str
    name: str
    
    # 振荡参数
    natural_frequency: float = 1.0  # 自然频率 (Hz)
    current_phase: float = 0.0      # 当前相位 [0, 2π)
    
    # PRC
    prc: PhaseResponseCurve = field(default_factory=PhaseResponseCurve)
    
    # 状态
    is_active: bool = True
    coupling_strength: float = 0.5  # 与其他振荡器的平均耦合强度
    
    # 节律模式
    rhythm: BrainRhythm = BrainRhythm.BETA
    
    # 历史追踪
    phase_history: List[float] = field(default_factory=list)
    fire_times: List[float] = field(default_factory=list)
    max_history: int = 500
    
    # 时间追踪
    _time: float = 0.0
    
    def step(self, dt: float, external_perturbation: float = 0.0,
             noise_level: float = 0.01) -> bool:
        """
        推进一个时间步
        
        Args:
            dt: 时间步长 (秒)
            external_perturbation: 外部扰动
            noise_level: 噪声水平
            
        Returns:
            是否在本步跨越了2π(即完成了一个周期/发放)
        """
        # 角速度 (rad/s)
        omega = 2 * math.pi * self.natural_frequency
        
        # 噪声
        noise = random.gauss(0, noise_level * 2 * math.pi)
        
        # 更新相位
        old_phase = self.current_phase
        self.current_phase += (omega + external_perturbation + noise) * dt
        self._time += dt
        
        # 检测周期完成 (跨越2π)
        fired = False
        if self.current_phase >= 2 * math.pi:
            fired = True
            self.current_phase = self.current_phase % (2 * math.pi)
            self.fire_times.append(self._time)
            if len(self.fire_times) > 100:
                self.fire_times.pop(0)
        
        # 记录历史
        self.phase_history.append(self.current_phase)
        if len(self.phase_history) > self.max_history:
            self.phase_history.pop(0)
        
        return fired
    
    def get_phase_order(self) -> float:
        """get相位顺序参数 (0=任意, 1=完全锁相)"""
        return math.cos(self.current_phase)
    
    def reset_phase(self, new_phase: float = 0.0):
        """重置相位"""
        self.current_phase = new_phase % (2 * math.pi)
        self.phase_history.clear()
        self.fire_times.clear()
        self._time = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'frequency': self.natural_frequency,
            'phase': round(self.current_phase, 3),
            'rhythm': self.rhythm.value,
            'is_active': self.is_active,
            'fire_count': len(self.fire_times)
        }

# ============================================================
# 第三节: Kuramoto耦合模型
# ============================================================

@dataclass
class SyncCluster:
    """同步簇"""
    cluster_id: int
    member_ids: List[str]
    avg_frequency: float
    phase_coherence: float  # Kuramoto序参量
    representative_rhythm: str

class KuramotoCoupler:
    """
    Kuramoto耦合器 - 多模块同步协调
    
    Ch.8核心方程:
    dθ_i/dt = ω_i + (K/N) Σ_{j=1}^N sin(θ_j - θ_i)
    
    Kuramoto序参量 (衡量同步程度):
    r · e^(iψ) = (1/N) Σ_{j=1}^N e^(iθ_j)
    
    其中:
    - r ∈ [0, 1]: 0=完全异步, 1=完全同步
    - ψ: 平均相位
    - K: 全局耦合强度
    
    同步转变:
    - K < K_c: 系统异步 (r ≈ 0)
    - K > K_c: 系统突然同步 (r > 0)
    - K_c = 2 / (π·g(0)) 其中g(ω)是频率分布
    
    mapping到智能体:
    - 同步 = 多模块协调完成复杂任务
    - 反相 = 模块间互补工作 (如E-I)
    - 不同步 = 独立工作模式
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # 振荡器集合
        self.oscillators: Dict[str, NeuralOscillator] = {}
        
        # 耦合矩阵
        self.coupling_matrix: Dict[str, Dict[str, float]] = {}
        
        # 全局耦合强度
        self.global_coupling = self.config.get('global_coupling', 0.3)
        
        # 同步历史
        self.sync_history: List[float] = []
        self.max_history = 200
    
    def add_oscillator(self, osc: NeuralOscillator):
        """添加振荡器"""
        self.oscillators[osc.id] = osc
        # init耦合矩阵
        if osc.id not in self.coupling_matrix:
            self.coupling_matrix[osc.id] = {}
        for other_id in self.oscillators:
            if other_id != osc.id:
                if other_id not in self.coupling_matrix[osc.id]:
                    self.coupling_matrix[osc.id][other_id] = self.global_coupling
                if osc.id not in self.coupling_matrix[other_id]:
                    self.coupling_matrix[other_id][osc.id] = self.global_coupling
    
    def set_coupling(self, osc_a: str, osc_b: str, strength: float):
        """设置两个振荡器间的耦合强度"""
        if osc_a in self.coupling_matrix:
            self.coupling_matrix[osc_a][osc_b] = strength
        if osc_b in self.coupling_matrix:
            self.coupling_matrix[osc_b][osc_a] = strength
    
    def step(self, dt: float = 0.01, noise_level: float = 0.01) -> Dict[str, Any]:
        """
        推进Kuramoto系unified个时间步
        
        dθ_i/dt = ω_i + Σ_j K_ij · sin(θ_j - θ_i)
        """
        N = len(self.oscillators)
        if N == 0:
            return {}
        
        new_phases = {}
        fires = {}
        
        for osc_id, osc in self.oscillators.items():
            if not osc.is_active:
                new_phases[osc_id] = osc.current_phase
                continue
            
            # 计算耦合项
            coupling_sum = 0.0
            if osc_id in self.coupling_matrix:
                for other_id, K_ij in self.coupling_matrix[osc_id].items():
                    if other_id in self.oscillators:
                        other_phase = self.oscillators[other_id].current_phase
                        coupling_sum += K_ij * math.sin(other_phase - osc.current_phase)
            
            # 归一化
            coupling_sum /= N
            
            # PRC调节
            prc_modulation = 0.0
            if N > 1:
                avg_phase = self._get_mean_phase()
                prc_modulation = osc.prc.evaluate(osc.current_phase - avg_phase) * 0.1
            
            # 推进
            fired = osc.step(dt, coupling_sum + prc_modulation, noise_level)
            fires[osc_id] = fired
            new_phases[osc_id] = osc.current_phase
        
        # 计算序参量
        order_param, mean_phase = self.compute_order_parameter()
        self.sync_history.append(order_param)
        if len(self.sync_history) > self.max_history:
            self.sync_history.pop(0)
        
        return {
            'order_parameter': order_param,
            'mean_phase': mean_phase,
            'fires': fires,
            'oscillators': {oid: o.to_dict() for oid, o in self.oscillators.items()}
        }
    
    def _get_mean_phase(self) -> float:
        """get平均相位"""
        if not self.oscillators:
            return 0.0
        phases = [o.current_phase for o in self.oscillators.values() if o.is_active]
        if not phases:
            return 0.0
        return math.atan2(np.mean(np.sin(phases)), np.mean(np.cos(phases)))
    
    def compute_order_parameter(self) -> Tuple[float, float]:
        """
        计算Kuramoto序参量
        
        r · e^(iψ) = (1/N) Σ e^(iθ_j)
        """
        phases = [o.current_phase for o in self.oscillators.values() if o.is_active]
        N = len(phases)
        if N == 0:
            return 0.0, 0.0
        
        # 复数平均
        real_sum = sum(math.cos(p) for p in phases) / N
        imag_sum = sum(math.sin(p) for p in phases) / N
        
        r = math.sqrt(real_sum ** 2 + imag_sum ** 2)
        psi = math.atan2(imag_sum, real_sum)
        
        return r, psi
    
    def detect_sync_clusters(self, threshold: float = 0.8) -> List[SyncCluster]:
        """
        检测同步簇 - 哪些模块正在同步工作
        
        基于相位差: |θ_i - θ_j| < threshold 的模块组
        """
        active_osc = [(oid, osc) for oid, osc in self.oscillators.items() if osc.is_active]
        if len(active_osc) < 2:
            return []
        
        # 构建相位邻近图
        visited = set()
        clusters = []
        cluster_id = 0
        
        for oid, osc in active_osc:
            if oid in visited:
                continue
            
            # BFS寻找相位邻近的振荡器
            cluster_members = [oid]
            queue = [oid]
            visited.add(oid)
            
            while queue:
                current = queue.pop(0)
                for other_oid, other_osc in active_osc:
                    if other_oid in visited:
                        continue
                    phase_diff = abs(self.oscillators[current].current_phase - 
                                    other_osc.current_phase)
                    phase_diff = min(phase_diff, 2 * math.pi - phase_diff)
                    if phase_diff < threshold:
                        visited.add(other_oid)
                        cluster_members.append(other_oid)
                        queue.append(other_oid)
            
            # 计算簇的相干性
            if len(cluster_members) >= 2:
                cluster_phases = [self.oscillators[mid].current_phase for mid in cluster_members]
                N_c = len(cluster_phases)
                r_c = math.sqrt(
                    (sum(math.cos(p) for p in cluster_phases) / N_c) ** 2 +
                    (sum(math.sin(p) for p in cluster_phases) / N_c) ** 2
                )
                avg_freq = np.mean([self.oscillators[mid].natural_frequency for mid in cluster_members])
                
                # 确定代表节律
                rhythms = [self.oscillators[mid].rhythm.value for mid in cluster_members]
                from collections import Counter
                dominant_rhythm = Counter(rhythms).most_common(1)[0][0]
                
                clusters.append(SyncCluster(
                    cluster_id=cluster_id,
                    member_ids=cluster_members,
                    avg_frequency=avg_freq,
                    phase_coherence=r_c,
                    representative_rhythm=dominant_rhythm
                ))
                cluster_id += 1
        
        return clusters
    
    def get_sync_report(self) -> Dict[str, Any]:
        """get同步报告"""
        order_param, mean_phase = self.compute_order_parameter()
        clusters = self.detect_sync_clusters()
        
        # 历史同步质量
        avg_sync = float(np.mean(self.sync_history)) if self.sync_history else 0.0
        
        return {
            'order_parameter': round(order_param, 4),
            'mean_phase': round(mean_phase, 4),
            'avg_sync_quality': round(avg_sync, 4),
            'sync_status': self._classify_sync(order_param),
            'active_oscillators': len([o for o in self.oscillators.values() if o.is_active]),
            'total_oscillators': len(self.oscillators),
            'sync_clusters': [
                {
                    'id': c.cluster_id,
                    'members': c.member_ids,
                    'coherence': round(c.phase_coherence, 4),
                    'rhythm': c.representative_rhythm
                } for c in clusters
            ]
        }
    
    def _classify_sync(self, r: float) -> str:
        """分类同步状态"""
        if r > 0.9:
            return "strong_sync"      # 强同步 - 模块高度协调
        elif r > 0.7:
            return "partial_sync"     # 部分同步 - 有协调趋势
        elif r > 0.4:
            return "weak_sync"        # 弱同步 - 轻微协调
        else:
            return "desynchronized"   # 去同步 - 各自独立

# ============================================================
# 第四节: 相位同步协调器主控
# ============================================================

class PhaseSynchronizationCoordinator:
    """
    神经相位同步协调器
    
    管理智能体系统中所有功能模块的工作节律协调:
    
    标准模块配置:
    - reasoning (β 20Hz): 推理模块 - 主动思考
    - memory (θ 6Hz): 记忆模块 - 学习编码
    - creativity (γ 40Hz): 创造性模块 - characteristics绑定
    - execution (β 20Hz): 执行模块 - 主动操作
    - monitoring (α 10Hz): 监控模块 - 抑制控制
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.kuramoto = KuramotoCoupler(self.config.get('kuramoto_config'))
        self._init_default_oscillators()
        self.step_count = 0
        
        logger.info("神经相位同步协调器init完成")
        logger.info(f"  振荡器数量: {len(self.kuramoto.oscillators)}")
    
    def _init_default_oscillators(self):
        """init默认功能振荡器"""
        defaults = [
            ("reasoning", "推理引擎", 20.0, BrainRhythm.BETA, PRCType.TYPE_I),
            ("memory", "记忆系统", 6.0, BrainRhythm.THETA, PRCType.TYPE_II),
            ("creativity", "创造性引擎", 40.0, BrainRhythm.GAMMA, PRCType.TYPE_I),
            ("execution", "执行引擎", 20.0, BrainRhythm.BETA, PRCType.TYPE_I),
            ("monitoring", "元认知监控", 10.0, BrainRhythm.ALPHA, PRCType.TYPE_II),
            ("learning", "学习系统", 6.0, BrainRhythm.THETA, PRCType.TYPE_II),
        ]
        
        for osc_id, name, freq, rhythm, prc_type in defaults:
            prc = PhaseResponseCurve(prc_type=prc_type)
            osc = NeuralOscillator(
                id=osc_id,
                name=name,
                natural_frequency=freq,
                prc=prc,
                rhythm=rhythm,
                current_phase=random.uniform(0, 2 * math.pi)
            )
            self.kuramoto.add_oscillator(osc)
    
    def step(self, dt: float = 0.01, noise_level: float = 0.005) -> Dict[str, Any]:
        """推进一个时间步"""
        self.step_count += 1
        result = self.kuramoto.step(dt, noise_level)
        result['step_count'] = self.step_count
        return result
    
    def set_rhythm_mode(self, mode: str):
        """
        设置脑节律模式
        
        Args:
            mode: 认知模式
            - "focused": 高β+γ, 聚焦执行
            - "learning": 高θ+α, 学习编码
            - "creative": 高γ+低β, 创新探索
            - "resting": 高α+δ, 休息待机
        """
        rhythm_presets = {
            "focused": {
                "reasoning": (25.0, True), "execution": (25.0, True),
                "creativity": (35.0, True), "monitoring": (12.0, True),
                "memory": (4.0, True), "learning": (4.0, True),
            },
            "learning": {
                "reasoning": (15.0, True), "execution": (10.0, True),
                "creativity": (20.0, True), "monitoring": (10.0, True),
                "memory": (8.0, True), "learning": (8.0, True),
            },
            "creative": {
                "reasoning": (12.0, True), "execution": (8.0, True),
                "creativity": (45.0, True), "monitoring": (6.0, True),
                "memory": (6.0, True), "learning": (6.0, True),
            },
            "resting": {
                "reasoning": (5.0, False), "execution": (3.0, False),
                "creativity": (8.0, False), "monitoring": (10.0, True),
                "memory": (4.0, False), "learning": (4.0, False),
            },
        }
        
        if mode not in rhythm_presets:
            logger.warning(f"未知节律模式: {mode}")
            return
        
        preset = rhythm_presets[mode]
        for osc_id, (freq, active) in preset.items():
            if osc_id in self.kuramoto.oscillators:
                self.kuramoto.oscillators[osc_id].natural_frequency = freq
                self.kuramoto.oscillators[osc_id].is_active = active
        
        # 设置模块间的耦合强度
        if mode == "focused":
            # 聚焦模式: 强耦合推理-执行
            self.kuramoto.set_coupling("reasoning", "execution", 0.8)
            self.kuramoto.set_coupling("reasoning", "creativity", 0.3)
        elif mode == "creative":
            # 创新模式: 强耦合记忆-创造
            self.kuramoto.set_coupling("memory", "creativity", 0.8)
            self.kuramoto.set_coupling("creativity", "learning", 0.6)
        elif mode == "learning":
            # 学习模式: 强耦合记忆-学习
            self.kuramoto.set_coupling("memory", "learning", 0.9)
            self.kuramoto.set_coupling("learning", "monitoring", 0.5)
        
        logger.info(f"脑节律模式切换为: {mode}")
    
    def strengthen_connection(self, module_a: str, module_b: str):
        """加强两个模块间的耦合"""
        self.kuramoto.set_coupling(module_a, module_b, 
                                   min(1.0, self.kuramoto.global_coupling + 0.3))
    
    def weaken_connection(self, module_a: str, module_b: str):
        """减弱两个模块间的耦合"""
        self.kuramoto.set_coupling(module_a, module_b,
                                   max(0.0, self.kuramoto.global_coupling - 0.3))
    
    def get_report(self) -> Dict[str, Any]:
        """get协调器报告"""
        return self.kuramoto.get_sync_report()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'step_count': self.step_count,
            'oscillators': {oid: o.to_dict() for oid, o in self.kuramoto.oscillators.items()},
            'sync_report': self.get_report()
        }
