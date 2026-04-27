"""
__all__ = [
    'analyze_pattern',
    'apply',
    'compute',
    'convolve',
    'create_neural_coding_system',
    'create_tuning_curve',
    'encode',
    'encode_knowledge',
    'get_receptive_field_response',
    'get_response',
    'get_statistics',
    'instantaneous_rate',
    'quick_encode',
    'retrieve',
    'spike_count_rate',
    'time_average_rate',
]

神经编码核心系统 v1.0
Neural Encoding Core System v1.0

核心概念mapping:
- 发放率(Firing Rate) → 知识激活强度
- 调谐曲线(Tuning Curve) → 知识选择函数
- 反向相关(STA) → 知识触发模式
- LN模型 → 编码-激活级联

作者: Somn AI System
日期: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math
from collections import defaultdict
import hashlib

class TuningCurveType(Enum):
    """调谐曲线类型"""
    GAUSSIAN = "gaussian"              # 高斯调谐
    COSINE = "cosine"                  # 余弦调谐
    LINEAR = "linear"                  # 线性调谐
    SIGMOID = "sigmoid"                # S型调谐
    HUBEL_WIESEL = "hubel_wiesel"     # Hubel-Wiesel型

@dataclass
class NeuralActivity:
    """神经活动模式 - 对应脉冲序列"""
    timestamp: float
    intensity: float          # 激活强度 (对应发放率)
    pattern_id: str           # 模式标识
    receptive_field: Optional[Dict[str, Any]] = None  # 感受野参数
    noise: float = 0.0       # 噪声水平
    
    def __post_init__(self):
        if self.noise > 0:
            # 添加泊松噪声
            self.intensity = max(0, self.intensity + np.random.poisson(self.noise * self.intensity))

@dataclass
class ReceptiveField:
    """感受野 - 描述知识对特定刺激的响应模式"""
    stimulus_dimension: str           # 刺激维度
    preferred_value: Any              # 最优值
    bandwidth: float                  # 带宽
    sensitivity: float = 1.0          # 敏感性
    curve_type: TuningCurveType = TuningCurveType.GAUSSIAN
    
    def get_response(self, stimulus: Any) -> float:
        """计算对刺激的响应 - 基于调谐曲线"""
        if self.curve_type == TuningCurveType.GAUSSIAN:
            return self._gaussian_response(stimulus)
        elif self.curve_type == TuningCurveType.COSINE:
            return self._cosine_response(stimulus)
        elif self.curve_type == TuningCurveType.SIGMOID:
            return self._sigmoid_response(stimulus)
        else:
            return self._linear_response(stimulus)
    
    def _gaussian_response(self, stimulus: float) -> float:
        """高斯调谐响应"""
        diff = float(stimulus) - float(self.preferred_value)
        return self.sensitivity * math.exp(-(diff ** 2) / (2 * self.bandwidth ** 2))
    
    def _cosine_response(self, stimulus: float) -> float:
        """余弦调谐响应"""
        diff = float(stimulus) - float(self.preferred_value)
        return self.sensitivity * max(0, math.cos(diff))
    
    def _sigmoid_response(self, stimulus: float) -> float:
        """S型调谐响应"""
        x = (float(stimulus) - float(self.preferred_value)) / self.bandwidth
        return self.sensitivity / (1 + math.exp(-x))
    
    def _linear_response(self, stimulus: float) -> float:
        """线性调谐响应"""
        return self.sensitivity * (float(stimulus) - float(self.preferred_value))

@dataclass
class TuningCurve:
    """调谐曲线 - 描述神经元对刺激的平均响应"""
    curve_id: str
    curve_type: TuningCurveType
    parameters: Dict[str, float]
    
    # 高斯参数
    peak_response: float = 1.0        # 峰值响应
    preferred_stimulus: float = 0.0   # 最优刺激
    width: float = 1.0                # 宽度
    
    def compute(self, stimulus: float) -> float:
        """计算给定刺激下的响应"""
        if self.curve_type == TuningCurveType.GAUSSIAN:
            return self._gaussian(stimulus)
        elif self.curve_type == TuningCurveType.COSINE:
            return self._cosine(stimulus)
        elif self.curve_type == TuningCurveType.HUBEL_WIESEL:
            return self._hubel_wiesel(stimulus)
        else:
            return self._linear(stimulus)
    
    def _gaussian(self, s: float) -> float:
        """高斯调谐曲线: f(s) = f_max * exp(-(s-s0)^2 / 2σ^2)"""
        d = s - self.preferred_stimulus
        return self.peak_response * math.exp(-(d ** 2) / (2 * self.width ** 2))
    
    def _cosine(self, s: float) -> float:
        """余弦调谐曲线"""
        d = s - self.preferred_stimulus
        return self.peak_response * max(0, math.cos(d * math.pi / 180))
    
    def _linear(self, s: float) -> float:
        """线性调谐"""
        return max(0, self.peak_response * s / self.width)
    
    def _hubel_wiesel(self, s: float) -> float:
        """Hubel-Wiesel型 - 方向选择调谐"""
        # 简化的方向调谐
        angle = s * math.pi / 180
        preferred_angle = self.preferred_stimulus * math.pi / 180
        return self.peak_response * (math.cos(angle - preferred_angle) ** 2)

class LinearFilterKernel:
    """
    线性滤波器核 - 对应反向相关中的滤波器K(τ)
    实现: r_est(t) = ∫K(τ)s(t-τ)dτ
    """
    
    def __init__(self, kernel_type: str = "exp", tau: float = 10.0, dt: float = 1.0):
        """
        init线性滤波器
        
        Args:
            kernel_type: 核类型 ('exp', 'gabor', 'dog')
            tau: 时间常数 (ms)
            dt: 时间步长
        """
        self.kernel_type = kernel_type
        self.tau = tau
        self.dt = dt
        self.kernel = self._build_kernel()
    
    def _build_kernel(self) -> np.ndarray:
        """构建滤波器核"""
        t = np.arange(-3 * self.tau, 3 * self.tau, self.dt)
        
        if self.kernel_type == "exp":
            # 指数核: K(t) = (1/τ) * exp(-t/τ) for t > 0
            kernel = np.zeros_like(t, dtype=float)
            mask = t >= 0
            kernel[mask] = (1 / self.tau) * np.exp(-t[mask] / self.tau)
            
        elif self.kernel_type == "gabor":
            # Gabor核: 用于时空characteristics提取
            sigma = self.tau / 3
            kernel = np.exp(-t**2 / (2 * sigma**2)) * np.cos(2 * np.pi * t / self.tau)
            
        elif self.kernel_type == "dog":
            # 差分高斯核: 用于边缘检测
            sigma1 = self.tau / 2
            sigma2 = self.tau
            kernel = np.exp(-t**2 / (2 * sigma1**2)) - 0.5 * np.exp(-t**2 / (2 * sigma2**2))
        
        else:
            kernel = np.exp(-np.abs(t) / self.tau)
        
        return kernel
    
    def apply(self, signal: np.ndarray) -> float:
        """应用滤波器"""
        if len(signal) < len(self.kernel):
            # 零填充
            signal = np.pad(signal, (0, len(self.kernel) - len(signal)))
        return np.sum(self.kernel * signal[-len(self.kernel):])
    
    def convolve(self, signal: np.ndarray) -> np.ndarray:
        """卷积运算"""
        return np.convolve(signal, self.kernel, mode='same')

class LNModel:
    """
    LN模型 (Linear-Nonlinear Model) - 神经编码的级联模型
    对应: Stimulus → [Linear Filter] → [Nonlinearity] → Response
    
    这是<Theoretical Neuroscience>中描述神经编码的基本模型
    """
    
    def __init__(self, linear_filter: LinearFilterKernel, 
                 nonlinearity: str = "relu"):
        self.linear_filter = linear_filter
        self.nonlinearity = nonlinearity
        self._init_nonlinearity()
    
    def _init_nonlinearity(self):
        """init非线性函数"""
        self.nl_functions = {
            "relu": lambda x: max(0, x),
            "threshold_linear": lambda x: max(0, min(1, x)),
            "sigmoid": lambda x: 1 / (1 + math.exp(-x)),
            "power": lambda x: max(0, x) ** 0.3,
            "exponential": lambda x: math.exp(min(10, max(-10, x)))
        }
        self.nl_func = self.nl_functions.get(self.nonlinearity, self.nl_functions["relu"])
    
    def encode(self, stimulus: np.ndarray) -> float:
        """
        编码刺激
        
        流程:
        1. 线性滤波: L(t) = ∫K(τ)s(t-τ)dτ
        2. 非线性变换: r(t) = f(L(t))
        """
        # Step 1: 线性滤波
        linear_response = self.linear_filter.convolve(stimulus)
        
        # Step 2: 非线性变换
        if isinstance(linear_response, np.ndarray):
            response = np.array([self.nl_func(x) for x in linear_response])
        else:
            response = self.nl_func(linear_response)
        
        return response

@dataclass
class SpikeTriggeredAverage:
    """
    脉冲触发平均 (STA) - 反向相关方法
    STA(τ) = (1/N) * Σ[s(t_i - τ)]
    
    用于分析什么刺激模式触发神经元响应
    """
    tau_range: Tuple[float, float] = (-100, 0)  # 时间延迟范围 (ms)
    bin_size: float = 1.0  # 时间bin大小
    
    def compute(self, spikes: List[float], stimuli: np.ndarray, 
                sample_rate: float = 1000) -> np.ndarray:
        """
        计算脉冲触发平均
        
        Args:
            spikes: 脉冲发放时间列表
            stimuli: 刺激信号数组
            sample_rate: 采样率
            
        Returns:
            STA: 脉冲触发平均曲线
        """
        # 计算tau范围
        max_lag = int(abs(self.tau_range[0]) * sample_rate / 1000)
        min_lag = int(abs(self.tau_range[1]) * sample_rate / 1000)
        
        # initSTA
        n_bins = max_lag - min_lag
        if n_bins <= 0:
            return np.array([])
        
        sta = np.zeros(n_bins)
        count = 0
        
        for spike_time in spikes:
            spike_idx = int(spike_time * sample_rate)
            
            for i, lag in enumerate(range(-max_lag, -min_lag)):
                idx = spike_idx + lag
                if 0 <= idx < len(stimuli):
                    sta[i] += stimuli[idx]
                    count += 1
        
        if count > 0:
            sta /= (count / n_bins)  # 归一化
        
        return sta

@dataclass
class FiringRateModel:
    """
    发放率模型 - 基于神经编码理论的知识激活模型
    
    三种发放率定义 (对应<Theoretical Neuroscience>Ch1):
    1. 瞬时发放率 r(t)
    2. 脉冲计数发放率 r(t,t+Δ)
    3. 时间平均发放率 r
    """
    
    def __init__(self, base_rate: float = 10.0, 
                 time_constant: float = 20.0):
        """
        Args:
            base_rate: 基础发放率 (Hz)
            time_constant: 膜时间常数 (ms)
        """
        self.base_rate = base_rate
        self.time_constant = time_constant
    
    def instantaneous_rate(self, current: float, v_rest: float = -70,
                          v_threshold: float = -55) -> float:
        """
        计算瞬时发放率
        
        基于LIF模型简化:
        r(t) = max(0, (V(t) - V_rest) / (V_th - V_rest))
        """
        if current <= v_rest:
            return 0
        
        rate = self.base_rate * (current - v_rest) / (v_threshold - v_rest)
        return max(0, min(rate, self.base_rate * 2))  # 限制在合理范围
    
    def spike_count_rate(self, spike_times: List[float], 
                         window: Tuple[float, float]) -> float:
        """
        计算脉冲计数发放率
        
        r(T) = N_T / T
        """
        count = sum(1 for t in spike_times if window[0] <= t <= window[1])
        duration = window[1] - window[0]
        return count / duration if duration > 0 else 0
    
    def time_average_rate(self, spike_times: List[float], 
                          total_time: float) -> float:
        """
        计算时间平均发放率
        
        r = (1/T) * 总脉冲数
        """
        return len(spike_times) / total_time if total_time > 0 else 0

class NeuralEncoder:
    """
    神经编码器 - 将知识编码为神经活动模式
    
    基于<Theoretical Neuroscience>的神经编码理论
    实现:
    1. 调谐曲线编码 - 知识的选择性响应
    2. LN模型编码 - 线性-非线性级联
    3. 发放率编码 - 激活强度计算
    """
    
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        self.tuning_curves: Dict[str, TuningCurve] = {}
        self.ln_models: Dict[str, LNModel] = {}
        self.firing_rate_model = FiringRateModel()
        self.linear_filters: Dict[str, LinearFilterKernel] = {}
        
    def create_tuning_curve(self, concept_id: str, 
                           preferred_value: float,
                           peak_response: float = 1.0,
                           width: float = 1.0,
                           curve_type: TuningCurveType = TuningCurveType.GAUSSIAN) -> TuningCurve:
        """
        为概念创建调谐曲线
        
        这模拟了神经元对特定刺激属性的选择性响应
        例如:
        - 知识类型调谐
        - 领域调谐
        - 优先级调谐
        """
        curve = TuningCurve(
            curve_id=concept_id,
            curve_type=curve_type,
            parameters={
                'preferred': preferred_value,
                'peak': peak_response,
                'width': width
            },
            peak_response=peak_response,
            preferred_stimulus=preferred_value,
            width=width
        )
        self.tuning_curves[concept_id] = curve
        return curve
    
    def encode_knowledge(self, knowledge: Dict[str, Any],
                        stimuli: Optional[np.ndarray] = None) -> NeuralActivity:
        """
        编码知识为神经活动模式
        
        Args:
            knowledge: 知识条目
            stimuli: 可选的刺激信号
            
        Returns:
            NeuralActivity: 神经活动模式
        """
        # 提取知识的characteristics值
        feature_value = self._extract_feature(knowledge)
        
        # get或创建调谐曲线
        concept_id = knowledge.get('id', 'default')
        if concept_id not in self.tuning_curves:
            self.create_tuning_curve(concept_id, feature_value)
        
        curve = self.tuning_curves[concept_id]
        
        # 计算基础响应 (调谐曲线)
        base_response = curve.compute(feature_value)
        
        # 如果有刺激信号,应用LN模型
        if stimuli is not None:
            if concept_id not in self.ln_models:
                self.ln_models[concept_id] = LNModel(
                    LinearFilterKernel(kernel_type="exp", tau=20),
                    nonlinearity="relu"
                )
            ln_response = self.ln_models[concept_id].encode(stimuli)
            if isinstance(ln_response, np.ndarray):
                ln_response = np.mean(ln_response)
            base_response *= (1 + ln_response)
        
        # 添加泊松噪声
        noise_level = 0.1 * base_response
        response_with_noise = max(0, base_response + np.random.normal(0, noise_level))
        
        # 计算发放率
        firing_rate = self.firing_rate_model.instantaneous_rate(response_with_noise)
        
        return NeuralActivity(
            timestamp=datetime.now().timestamp(),
            intensity=firing_rate,
            pattern_id=concept_id,
            receptive_field=curve.parameters,
            noise=noise_level
        )
    
    def _extract_feature(self, knowledge: Dict[str, Any]) -> float:
        """从知识中提取characteristics值"""
        # synthesize多个维度计算characteristics值
        priority = knowledge.get('priority', 5) / 10.0
        relevance = knowledge.get('relevance', 0.5)
        freshness = knowledge.get('freshness', 1.0)
        
        # synthesizecharacteristics
        feature = (priority * 0.3 + relevance * 0.4 + freshness * 0.3)
        return feature
    
    def get_receptive_field_response(self, concept_id: str, 
                                     stimulus: Any) -> float:
        """get感受野响应"""
        if concept_id not in self.tuning_curves:
            return 0
        
        curve = self.tuning_curves[concept_id]
        return curve.compute(float(stimulus))

class NeuralCodingKnowledgeSystem:
    """
    神经编码知识系统 - 基于计算神经科学的知识表示与检索
    
    整合<Theoretical Neuroscience>的核心理论:
    1. 神经编码 (Neural Encoding) - 知识如何被编码
    2. 发放率 (Firing Rate) - 知识激活强度
    3. 调谐曲线 (Tuning Curve) - 知识的选择性
    4. LN模型 - 编码级联
    5. 反向相关 (Reverse Correlation) - 模式recognize
    """
    
    def __init__(self, embedding_dim: int = 384):
        self.encoder = NeuralEncoder(embedding_dim)
        self.activities: List[NeuralActivity] = []
        self.sta = SpikeTriggeredAverage()
        
        # 知识索引
        self.knowledge_index: Dict[str, Dict[str, Any]] = {}
        
        # 统计
        self.total_encodings = 0
        self.total_retrievals = 0
        
    def encode(self, knowledge: Dict[str, Any], 
               stimuli: Optional[np.ndarray] = None) -> str:
        """
        编码知识
        
        Args:
            knowledge: 知识条目,包含:
                - id: 知识ID
                - content: 知识内容
                - priority: 优先级 (1-10)
                - relevance: 相关性 (0-1)
                - freshness: 新鲜度 (0-1)
            stimuli: 可选的刺激信号
            
        Returns:
            str: 活动模式ID
        """
        # 编码知识
        activity = self.encoder.encode_knowledge(knowledge, stimuli)
        
        # 存储
        self.activities.append(activity)
        self.knowledge_index[knowledge['id']] = {
            'knowledge': knowledge,
            'activity': activity,
            'encoded_at': datetime.now().isoformat()
        }
        
        self.total_encodings += 1
        return activity.pattern_id
    
    def retrieve(self, query: Any, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        检索知识 - 基于发放率和调谐曲线
        
        使用发放率模型计算知识激活强度,
        按强度排序返回top_k结果
        """
        results = []
        
        for kid, item in self.knowledge_index.items():
            activity = item['activity']
            knowledge = item['knowledge']
            
            # 计算查询的响应
            response = self.encoder.get_receptive_field_response(
                kid, 
                self._query_to_value(query)
            )
            
            # synthesize评分: 发放率 + 调谐响应
            score = (activity.intensity * 0.5 + response * 0.5)
            
            results.append({
                'knowledge_id': kid,
                'knowledge': knowledge,
                'activity': activity,
                'score': score,
                'response': response
            })
        
        # 按评分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        self.total_retrievals += 1
        
        return results[:top_k]
    
    def _query_to_value(self, query: Any) -> float:
        """将查询转换为characteristics值"""
        if isinstance(query, (int, float)):
            return float(query)
        elif isinstance(query, dict):
            return query.get('feature_value', 0.5)
        elif isinstance(query, str):
            # 简单的字符串哈希
            return float(int(hashlib.md5(query.encode()).hexdigest(), 16) % 100) / 100
        else:
            return 0.5
    
    def analyze_pattern(self, pattern_id: str) -> Dict[str, Any]:
        """分析神经活动模式"""
        pattern_activities = [a for a in self.activities if a.pattern_id == pattern_id]
        
        if not pattern_activities:
            return {}
        
        intensities = [a.intensity for a in pattern_activities]
        
        return {
            'pattern_id': pattern_id,
            'count': len(pattern_activities),
            'mean_intensity': np.mean(intensities),
            'std_intensity': np.std(intensities),
            'max_intensity': max(intensities),
            'min_intensity': min(intensities)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """get系统统计"""
        if not self.activities:
            return {
                'total_encodings': 0,
                'total_retrievals': 0,
                'avg_intensity': 0,
                'patterns': {}
            }
        
        all_intensities = [a.intensity for a in self.activities]
        
        return {
            'total_encodings': self.total_encodings,
            'total_retrievals': self.total_retrievals,
            'avg_intensity': np.mean(all_intensities),
            'std_intensity': np.std(all_intensities),
            'max_intensity': max(all_intensities),
            'patterns': {
                pid: self.analyze_pattern(pid)
                for pid in set(a.pattern_id for a in self.activities)
            }
        }

# ============ 便捷函数 ============

def create_neural_coding_system(embedding_dim: int = 384) -> NeuralCodingKnowledgeSystem:
    """创建神经编码知识系统"""
    return NeuralCodingKnowledgeSystem(embedding_dim)

def quick_encode(knowledge: Dict[str, Any], 
                 priority: int = 5,
                 relevance: float = 0.5,
                 freshness: float = 1.0) -> NeuralActivity:
    """快速编码"""
    system = create_neural_coding_system()
    knowledge.update({
        'priority': priority,
        'relevance': relevance,
        'freshness': freshness
    })
    system.encode(knowledge)
    return system.activities[-1]

# ============ 示例使用 ============

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
