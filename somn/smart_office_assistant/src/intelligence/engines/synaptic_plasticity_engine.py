"""
__all__ = [
    'activate',
    'apply_stdp',
    'co_activate',
    'compute_delta',
    'connect',
    'get_association_strength',
    'get_effective_weight',
    'get_plasticity_report',
    'get_top_connections',
    'oja_update',
    'receive_reward',
    'reinforce',
    'reset_synapse',
    'set_arousal',
    'set_attention',
    'set_dopamine',
    'synapse_homeostasis',
    'to_dict',
    'update_weight',
    'weaken',
]

神经突触可塑性引擎 v1.0
Synaptic Plasticity Engine

核心功能:
1. Hebbian学习 (Hebbian Learning) - "同时放电的神经元连接在一起"
2. STDP (Spike-Timing Dependent Plasticity) - 脉冲时序依赖可塑性
3. BCM规则 (Bienenstock-Cooper-Munro) - 滑动阈值竞争学习
4. 短时程可塑性 - 抑制(depression)与易化(facilitation)
5. 突触稳态 - 维持连接强度的长期稳定
6. 三因子学习规则 - Hebbian × 预测误差 × 神经调制

神经科学→AI系统mapping:
  突触权重 → 模块间协作强度/记忆关联强度
  LTP/LTD → 强化/弱化知识关联
  STDP → 基于时间关联的学习
  短时程可塑性 → 工作记忆中的新鲜度管理
  突触稳态 → 防止记忆过度强化或过度遗忘

v1.0.0 神经科学数学基础增强版
"""

import json
import math
import random
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from loguru import logger

# ============================================================
# 第一节: 突触连接模型
# ============================================================

@dataclass
class Synapse:
    """
    突触连接 - 模拟模块间/知识间的关联
    
    对应Ch.7突触通道模型:
    - AMPA: 快速兴奋性 (权重快速变化)
    - NMDA: 慢速兴奋性 (权重缓慢积累,具有coincidence detection)
    - GABA: 抑制性 (负权重,约束连接)
    """
    pre_id: str           # 前神经元/模块ID
    post_id: str          # 后神经元/模块ID
    weight: float = 0.5   # 突触权重 [0, 1]
    
    # 突触类型
    synapse_type: str = "amga"  # ampa/nmda/gaba
    
    # 短时程可塑性
    depression: float = 0.0      # 抑制因子 (0=正常, 1=完全抑制)
    facilitation: float = 0.0    # 易化因子 (0=正常, 1=最大易化)
    
    # 稳态参数
    target_weight: float = 0.5   # 目标权重 (突触稳态)
    homeostatic_rate: float = 0.001  # 稳态调节速率
    
    # 使用统计
    activation_count: int = 0
    last_activated: Optional[str] = None
    co_activation_count: int = 0  # 前后同时激活次数
    
    # STDP追踪
    pre_last_fire: float = -1000.0  # 前神经元上次放电时间
    post_last_fire: float = -1000.0 # 后神经元上次放电时间
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'pre_id': self.pre_id,
            'post_id': self.post_id,
            'weight': round(self.weight, 4),
            'type': self.synapse_type,
            'depression': round(self.depression, 4),
            'facilitation': round(self.facilitation, 4),
            'target_weight': round(self.target_weight, 4),
            'activation_count': self.activation_count,
            'co_activation_count': self.co_activation_count
        }

# ============================================================
# 第二节: Hebbian学习规则
# ============================================================

class HebbianRule:
    """
    Hebbian学习规则
    
    经典公式: Δw = η · x_pre · x_post
    其中:
    - η: 学习率
    - x_pre: 前神经元激活值
    - x_post: 后神经元激活值
    
    扩展版本(Oja规则,带归一化):
    Δw = η · x_pre · (x_post - w · x_pre)
    """
    
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
    
    def compute_delta(self, pre_activation: float, 
                      post_activation: float, 
                      weight: float) -> float:
        """计算Hebbian权重变化"""
        if pre_activation < 0.1 or post_activation < 0.1:
            return 0.0
        # Oja规则: 带权重衰减防止无限增长
        delta = self.learning_rate * pre_activation * (post_activation - weight * pre_activation)
        return delta
    
    def oja_update(self, pre_activation: float, 
                   post_activation: float,
                   weight: float) -> float:
        """Oja归一化更新"""
        delta = self.compute_delta(pre_activation, post_activation, weight)
        return max(0, min(1, weight + delta))

# ============================================================
# 第三节: STDP学习规则
# ============================================================

class STDPRule:
    """
    脉冲时序依赖可塑性 (Spike-Timing Dependent Plasticity)
    
    核心原理 (Ch.7延伸 + Dayan Ch.8):
    - 如果前神经元在后神经元之前放电 → LTP (长时程增强)
    - 如果后神经元在前神经元之前放电 → LTD (长时程抑制)
    
    STDP窗口函数:
    Δw = A₊ · exp(-Δt/τ₊)   if Δt > 0 (pre before post → LTP)
    Δw = -A₋ · exp(Δt/τ₋)   if Δt < 0 (post before pre → LTD)
    
    其中 Δt = t_post - t_pre
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # STDP时间常数 (毫秒)
        self.tau_plus = self.config.get('tau_plus', 20.0)   # LTP时间窗口
        self.tau_minus = self.config.get('tau_minus', 20.0)  # LTD时间窗口
        
        # 幅度
        self.A_plus = self.config.get('A_plus', 0.005)    # LTP幅度
        self.A_minus = self.config.get('A_minus', 0.0045) # LTD幅度 (略小于A_plus以支持稳定性)
        
        # 学习率
        self.learning_rate = self.config.get('learning_rate', 1.0)
    
    def compute_delta(self, pre_fire_time: float, 
                      post_fire_time: float) -> float:
        """
        计算STDP权重变化
        
        Args:
            pre_fire_time: 前神经元放电时间 (秒)
            post_fire_time: 后神经元放电时间 (秒)
        """
        delta_t = (post_fire_time - pre_fire_time) * 1000  # 转为毫秒
        
        if abs(delta_t) > 100:  # 超过100ms的间隔不考虑
            return 0.0
        
        if delta_t > 0:
            # pre在post之前 → LTP
            delta_w = self.A_plus * math.exp(-delta_t / self.tau_plus)
        else:
            # post在pre之前 → LTD
            delta_w = -self.A_minus * math.exp(delta_t / self.tau_minus)
        
        return delta_w * self.learning_rate
    
    def apply_stdp(self, synapse: Synapse, 
                   current_time: float,
                   is_pre_fire: bool = False,
                   is_post_fire: bool = False) -> float:
        """
        对突触应用STDP更新
        
        Args:
            synapse: 突触连接
            current_time: 当前时间 (秒)
            is_pre_fire: 前神经元是否正在放电
            is_post_fire: 后神经元是否正在放电
        """
        delta_w = 0.0
        
        if is_pre_fire:
            # 前放电,检查与后放电的时间差
            if synapse.post_last_fire > 0:
                delta_w = self.compute_delta(current_time, synapse.post_last_fire)
            synapse.pre_last_fire = current_time
            
        elif is_post_fire:
            # 后放电,检查与前放电的时间差
            if synapse.pre_last_fire > 0:
                delta_w = self.compute_delta(synapse.pre_last_fire, current_time)
            synapse.post_last_fire = current_time
        
        # 更新权重
        new_weight = max(0, min(1, synapse.weight + delta_w))
        synapse.weight = new_weight
        
        return delta_w

# ============================================================
# 第四节: BCM规则 (滑动阈值)
# ============================================================

class BCMRule:
    """
    BCM规则 (Bienenstock-Cooper-Munro)
    
    核心思想 (Dayan & Abbott Ch.8):
    Δw = η · x_post · (x_post - θ_M) · x_pre
    
    其中 θ_M 是滑动修改阈值:
    - 如果post激活高于阈值 → LTP
    - 如果post激活低于阈值 → LTD
    - 阈值根据post的历史激活水平动态调整
    
    θ_M = E[x_post²]  (post激活的均方)
    
    BCM规则解决了Hebbian学习的关键问题:
    防止"赢者通吃"--所有权重都增长到饱和
    引入竞争--只有"有用的"连接被增强
    """
    
    def __init__(self, learning_rate: float = 0.001):
        self.learning_rate = learning_rate
        self.theta_m = 0.5  # 初始修改阈值
        self.theta_update_rate = 0.01  # 阈值更新速率
        self.post_activation_history: List[float] = []
        self.max_history = 1000
    
    def compute_delta(self, pre_activation: float, 
                      post_activation: float) -> float:
        """计算BCM权重变化"""
        if pre_activation < 0.05:
            return 0.0
        
        # 记录post激活历史
        self.post_activation_history.append(post_activation ** 2)
        if len(self.post_activation_history) > self.max_history:
            self.post_activation_history.pop(0)
        
        # 更新滑动阈值
        if self.post_activation_history:
            self.theta_m = self.theta_update_rate * np.mean(self.post_activation_history) + \
                          (1 - self.theta_update_rate) * self.theta_m
        
        # BCM规则
        delta_w = self.learning_rate * post_activation * (post_activation - self.theta_m) * pre_activation
        
        return delta_w
    
    def update_weight(self, pre_activation: float, 
                      post_activation: float, weight: float) -> float:
        """更新权重"""
        delta = self.compute_delta(pre_activation, post_activation)
        return max(0, min(1, weight + delta))

# ============================================================
# 第五节: 短时程可塑性
# ============================================================

@dataclass
class ShortTermPlasticityParams:
    """短时程可塑性参数 (Tsodyks-Markram模型)"""
    # 抑制 (depression)
    use_factor: float = 0.5       # 使用率 (每次脉冲消耗的可用资源比例)
    recovery_rate: float = 0.2    # 资源恢复速率
    
    # 易化 (facilitation)
    facilitation_rate: float = 0.5  # 易化积累速率
    facilitation_decay: float = 0.1  # 易化衰减速率
    
    # 初始值
    initial_R: float = 1.0   # 初始可用资源

class ShortTermPlasticityEngine:
    """
    短时程可塑性引擎 (Tsodyks-Markram模型)
    
    对应Ch.7短时程可塑性:
    - 抑制(Depression): 反复激活导致突触响应减弱
      → 对应: 重复使用同一记忆时效果递减
    - 易化(Facilitation): 反复激活导致突触响应增强
      → 对应: 上下文预热后响应加速
    
    动力学方程:
    dR/dt = (1-R)/τ_rec - u·R·δ(t-t_spike)  (资源恢复)
    du/dt = -u/τ_fac + U·(1-u)·δ(t-t_spike)  (易化积累)
    
    有效突触权重: w_eff = R · u · w_base
    """
    
    def __init__(self, params: Optional[ShortTermPlasticityParams] = None):
        self.params = params or ShortTermPlasticityParams()
        
        # 各突触的短时程状态
        self.synapse_states: Dict[str, Dict[str, float]] = {}
    
    def _get_state(self, synapse_key: str) -> Dict[str, float]:
        """get或创建突触状态"""
        if synapse_key not in self.synapse_states:
            self.synapse_states[synapse_key] = {
                'R': self.params.initial_R,  # 可用资源
                'u': 0.0,                     # 使用概率
                'last_activation': 0.0        # 上次激活时间
            }
        return self.synapse_states[synapse_key]
    
    def activate(self, synapse_key: str, current_time: float = 0.0) -> float:
        """
        激活突触,返回有效权重倍率
        
        Args:
            synapse_key: 突触标识
            current_time: 当前时间
            
        Returns:
            有效权重倍率 (考虑短时程可塑性后的实际权重/base_weight)
        """
        state = self._get_state(synapse_key)
        
        # 1. 计算时间衰减 (资源恢复 + 易化衰减)
        dt = current_time - state['last_activation']
        if dt > 0:
            state['R'] += (1 - state['R']) * self.params.recovery_rate * dt
            state['u'] *= math.exp(-self.params.facilitation_decay * dt)
        
        # 2. 脉冲到达: 消耗资源 + 积累易化
        release = state['u'] * state['R']
        state['R'] -= state['u'] * state['R']  # 消耗资源
        state['u'] += self.params.facilitation_rate * (1 - state['u'])  # 易化
        
        # 3. 恢复一些资源 (模拟快速回收)
        state['R'] = max(0.1, state['R'] + self.params.use_factor * self.params.recovery_rate)
        
        state['last_activation'] = current_time
        
        return release
    
    def get_effective_weight(self, synapse_key: str, base_weight: float,
                             current_time: float = 0.0) -> float:
        """get考虑短时程可塑性后的有效权重"""
        stp_factor = self.activate(synapse_key, current_time)
        return base_weight * stp_factor
    
    def reset_synapse(self, synapse_key: str):
        """重置突触状态"""
        if synapse_key in self.synapse_states:
            self.synapse_states[synapse_key] = {
                'R': self.params.initial_R,
                'u': 0.0,
                'last_activation': 0.0
            }

# ============================================================
# 第六节: 三因子学习规则
# ============================================================

class ThreeFactorRule:
    """
    三因子学习规则 (Three-Factor Learning Rule)
    
    扩展Hebbian: Δw = η · pre · post · modulator
    
    第三因子(调制因子):
    - 多巴胺(Dopamine)信号 → 奖励预测误差 (TD error)
    - 乙酰胆碱(ACh) → 注意力/新奇度
    - 去甲肾上腺素(NE) → 唤醒/紧急程度
    
    mapping到智能体系统:
    - 多巴胺 → 用户满意度/任务完成度
    - ACh → 任务重要性/注意力权重
    - NE → 紧急度/时间压力
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.base_learning_rate = self.config.get('learning_rate', 0.01)
        
        # 调制因子状态
        self.dopamine_level = 0.0   # 奖励预测误差 [-1, 1]
        self.ach_level = 0.5        # 注意力水平 [0, 1]
        self.ne_level = 0.0         # 唤醒水平 [0, 1]
    
    def set_dopamine(self, reward_prediction_error: float):
        """设置多巴胺水平 (奖励预测误差)"""
        self.dopamine_level = max(-1, min(1, reward_prediction_error))
    
    def set_attention(self, importance: float):
        """设置注意力水平 (ACh模拟)"""
        self.ach_level = max(0, min(1, importance))
    
    def set_arousal(self, urgency: float):
        """设置唤醒水平 (NE模拟)"""
        self.ne_level = max(0, min(1, urgency))
    
    def compute_delta(self, pre_activation: float, 
                      post_activation: float) -> float:
        """计算三因子权重变化"""
        # 基础Hebbian项
        hebbian = pre_activation * post_activation
        
        # 调制因子乘积
        # 多巴胺: 正RPE增强学习,负RPE逆转学习
        dopamine_factor = 0.5 + 0.5 * self.dopamine_level
        
        # ACh: 注意力门控
        ach_factor = self.ach_level
        
        # NE: 紧急度增强
        ne_factor = 1.0 + 0.5 * self.ne_level
        
        # 三因子规则
        delta_w = self.base_learning_rate * hebbian * dopamine_factor * ach_factor * ne_factor
        
        return delta_w
    
    def receive_reward(self, actual: float, predicted: float):
        """接收奖励,更新多巴胺水平"""
        rpe = actual - predicted  # 奖励预测误差
        self.set_dopamine(rpe)

# ============================================================
# 第七节: 突触可塑性引擎主控
# ============================================================

class SynapticPlasticityEngine:
    """
    突触可塑性引擎 - unified管理所有学习规则
    
    整合:
    1. Hebbian规则 - 基础关联学习
    2. STDP规则 - 时序依赖学习
    3. BCM规则 - 竞争学习
    4. 短时程可塑性 - 工作记忆管理
    5. 三因子规则 - 奖励调制的强化学习
    6. 突触稳态 - 长期稳定性
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # 学习规则
        self.hebbian = HebbianRule(learning_rate=self.config.get('hebbian_lr', 0.01))
        self.stdp = STDPRule(self.config.get('stdp_config', {}))
        self.bcm = BCMRule(learning_rate=self.config.get('bcm_lr', 0.001))
        self.three_factor = ThreeFactorRule()
        self.short_term = ShortTermPlasticityEngine()
        
        # 突触连接存储
        self.synapses: Dict[str, Synapse] = {}
        
        # 统计
        self.stats = {
            'total_updates': 0,
            'ltp_count': 0,
            'ltd_count': 0,
            'avg_weight': 0.0
        }
        
        logger.info("突触可塑性引擎init完成")
    
    def _synapse_key(self, pre_id: str, post_id: str) -> str:
        """generate突触键"""
        return f"{pre_id}→{post_id}"
    
    def connect(self, pre_id: str, post_id: str, 
                initial_weight: float = 0.5,
                synapse_type: str = "amga") -> Synapse:
        """
        建立突触连接
        
        Args:
            pre_id: 前神经元/模块ID
            post_id: 后神经元/模块ID
            initial_weight: 初始权重
            synapse_type: 突触类型 (amga/nmda/gaba)
        """
        key = self._synapse_key(pre_id, post_id)
        synapse = Synapse(
            pre_id=pre_id,
            post_id=post_id,
            weight=initial_weight,
            synapse_type=synapse_type
        )
        self.synapses[key] = synapse
        return synapse
    
    def co_activate(self, pre_id: str, post_id: str,
                    pre_activation: float = 1.0,
                    post_activation: float = 1.0,
                    learning_rule: str = "hebbian") -> float:
        """
        同时激活前后神经元 → 触发学习
        
        Args:
            pre_id: 前神经元
            post_id: 后神经元
            pre_activation: 前激活值
            post_activation: 后激活值
            learning_rule: 学习规则 (hebbian/stdp/bcm/three_factor)
            
        Returns:
            权重变化量
        """
        key = self._synapse_key(pre_id, post_id)
        
        # 自动创建连接
        if key not in self.synapses:
            self.connect(pre_id, post_id)
        
        synapse = self.synapses[key]
        synapse.activation_count += 1
        synapse.co_activation_count += 1
        synapse.last_activated = datetime.now().isoformat()
        
        delta_w = 0.0
        
        if learning_rule == "hebbian":
            old_weight = synapse.weight
            synapse.weight = self.hebbian.oja_update(pre_activation, post_activation, synapse.weight)
            delta_w = synapse.weight - old_weight
            
        elif learning_rule == "bcm":
            old_weight = synapse.weight
            synapse.weight = self.bcm.update_weight(pre_activation, post_activation, synapse.weight)
            delta_w = synapse.weight - old_weight
            
        elif learning_rule == "three_factor":
            old_weight = synapse.weight
            delta_w = self.three_factor.compute_delta(pre_activation, post_activation)
            synapse.weight = max(0, min(1, synapse.weight + delta_w))
            
        elif learning_rule == "stdp":
            delta_w = self.stdp.apply_stdp(
                synapse, 
                datetime.now().timestamp(),
                is_pre_fire=True,
                is_post_fire=True
            )
        
        # 突触稳态: 缓慢回归目标权重
        homeostatic_delta = self.synapse_homeostasis(synapse)
        delta_w += homeostatic_delta
        
        # 更新统计
        self.stats['total_updates'] += 1
        if delta_w > 0:
            self.stats['ltp_count'] += 1
        else:
            self.stats['ltd_count'] += 1
        
        return delta_w
    
    def synapse_homeostasis(self, synapse: Synapse) -> float:
        """
        突触稳态调节
        
        原理: 如果权重偏离目标值太远,施加缓慢的回归力
        Δw_homeo = -rate * (w - w_target)
        """
        deviation = synapse.weight - synapse.target_weight
        return -synapse.homeostatic_rate * deviation
    
    def get_effective_weight(self, pre_id: str, post_id: str,
                             current_time: float = 0.0) -> float:
        """
        get有效权重 (考虑短时程可塑性)
        """
        key = self._synapse_key(pre_id, post_id)
        if key not in self.synapses:
            return 0.0
        
        synapse = self.synapses[key]
        stp_key = key
        
        if current_time == 0.0:
            current_time = datetime.now().timestamp()
        
        stp_factor = self.short_term.activate(stp_key, current_time % 1000)
        return synapse.weight * stp_factor
    
    def get_association_strength(self, id_a: str, id_b: str) -> float:
        """get两个概念/模块间的关联强度"""
        key_ab = self._synapse_key(id_a, id_b)
        key_ba = self._synapse_key(id_b, id_a)
        
        w_ab = self.synapses[key_ab].weight if key_ab in self.synapses else 0.0
        w_ba = self.synapses[key_ba].weight if key_ba in self.synapses else 0.0
        
        return max(w_ab, w_ba)
    
    def reinforce(self, pre_id: str, post_id: str, amount: float = 0.1):
        """手动强化连接 (LTP)"""
        key = self._synapse_key(pre_id, post_id)
        if key in self.synapses:
            self.synapses[key].weight = min(1.0, self.synapses[key].weight + amount)
    
    def weaken(self, pre_id: str, post_id: str, amount: float = 0.1):
        """手动弱化连接 (LTD)"""
        key = self._synapse_key(pre_id, post_id)
        if key in self.synapses:
            self.synapses[key].weight = max(0.0, self.synapses[key].weight - amount)
    
    def get_top_connections(self, n: int = 10, 
                            source: Optional[str] = None) -> List[Dict]:
        """get权重最高的连接"""
        connections = []
        for key, synapse in self.synapses.items():
            if source and synapse.pre_id != source and synapse.post_id != source:
                continue
            connections.append({
                'key': key,
                'pre': synapse.pre_id,
                'post': synapse.post_id,
                'weight': synapse.weight,
                'type': synapse.synapse_type,
                'activations': synapse.activation_count,
                'co_activations': synapse.co_activation_count
            })
        
        connections.sort(key=lambda x: x['weight'], reverse=True)
        return connections[:n]
    
    def get_plasticity_report(self) -> Dict[str, Any]:
        """get可塑性报告"""
        if not self.synapses:
            return {'total_synapses': 0}
        
        weights = [s.weight for s in self.synapses.values()]
        return {
            'total_synapses': len(self.synapses),
            'avg_weight': float(np.mean(weights)),
            'max_weight': float(np.max(weights)),
            'min_weight': float(np.min(weights)),
            'weight_std': float(np.std(weights)),
            'total_updates': self.stats['total_updates'],
            'ltp_count': self.stats['ltp_count'],
            'ltd_count': self.stats['ltd_count'],
            'ltp_ratio': self.stats['ltp_count'] / max(1, self.stats['total_updates']),
            'dopamine_level': self.three_factor.dopamine_level,
            'attention_level': self.three_factor.ach_level,
            'bcm_threshold': self.bcm.theta_m,
            'top_connections': self.get_top_connections(5)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'synapses': {k: v.to_dict() for k, v in self.synapses.items()},
            'plasticity_report': self.get_plasticity_report()
        }
