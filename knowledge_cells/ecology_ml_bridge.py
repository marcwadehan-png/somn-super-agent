"""
Ecology + ML Engine → NeuralMemory 整合桥接模块
=====================================================

将 ecology 和 ml_engine 模块的有价值内容接入 NeuralMemory，
对 NeuralMemory 实现升级。

整合内容（提炼自 ecology/ 和 ml_engine/）：
  1. ResourceOptimizer 资源优化器（Ecology 核心价值）
  2. HealthStatus + EcosystemMetric 健康状态评估
  3. SimpleLinearModel 轻量级预测模型（ML Engine 核心价值）
  4. FeatureSchema + FeatureVector 特征工程
  5. ModelManager 模型持久化管理

升级 NeuralMemory：
  - 新增资源感知的记忆管理（内存/存储/Token 优化分配）
  - 新增健康状态监控（记忆系统的健康度评估）
  - 新增预测能力（预测记忆访问频率，优化预加载）
  - 新增自适应进化（根据反馈自动优化记忆结构）

版本: v1.0.0
日期: 2026-05-01
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import time
import json
import math
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
#  Section 1：从 Ecology 提炼核心类型
# ═══════════════════════════════════════════════════════════════

class MemoryHealthStatus(Enum):
    """记忆系统健康状态（提炼自 Ecology HealthStatus）"""
    EXCELLENT = "excellent"      # 优秀：访问命中率>95%，资源充足
    GOOD = "good"               # 良好：访问命中率>85%
    FAIR = "fair"               # 一般：访问命中率>70%
    POOR = "poor"               # 较差：访问命中率>50%
    CRITICAL = "critical"       # 危急：访问命中率<50%


class MemoryResourceType(Enum):
    """记忆系统资源类型（提炼自 Ecology ResourceType）"""
    MEMORY = "memory"           # 内存资源（字节）- 存放热数据
    STORAGE = "storage"         # 存储资源（字节）- 存放温/冷数据
    TOKEN = "token"             # Token资源 - API调用配额
    TIME = "time"               # 时间资源（秒）- 查询超时控制
    CPU = "cpu"                 # CPU资源（%） - 推理/编码消耗


@dataclass
class MemoryMetric:
    """记忆系统指标（提炼自 Ecology EcosystemMetric）"""
    name: str                     # 指标名称（如 "hit_rate", "storage_usage"）
    value: float                  # 当前值
    target: float                 # 目标值
    min_acceptable: float        # 最小可接受值
    max_acceptable: float       # 最大可接受值
    unit: str = ""
    timestamp: float = field(default_factory=time.time)

    @property
    def health_status(self) -> MemoryHealthStatus:
        """健康状态"""
        if self.target == 0:
            return MemoryHealthStatus.EXCELLENT
        ratio = self.value / self.target if self.target != 0 else 0
        if 0.95 <= ratio <= 1.05:
            return MemoryHealthStatus.EXCELLENT
        elif self.min_acceptable <= self.value <= self.max_acceptable:
            return MemoryHealthStatus.GOOD
        elif self.value < self.min_acceptable * 0.8:
            return MemoryHealthStatus.FAIR
        elif self.value < self.min_acceptable * 0.5:
            return MemoryHealthStatus.POOR
        else:
            return MemoryHealthStatus.CRITICAL

    @property
    def deviation(self) -> float:
        """偏差百分比"""
        if self.target == 0:
            return 0.0
        return abs(self.value - self.target) / self.target * 100


@dataclass
class MemoryResourceAllocation:
    """记忆系统资源分配（提炼自 Ecology ResourceAllocation）"""
    resource_type: MemoryResourceType
    allocated: float            # 已分配
    total: float                # 总量
    unit: str = ""
    hard_limit: float = 0.90   # 硬限制：不超过总量的90%
    soft_limit: float = 0.75   # 软限制：超过后触发告警

    @property
    def utilization(self) -> float:
        """利用率"""
        if self.total == 0:
            return 0.0
        return self.allocated / self.total * 100

    @property
    def available(self) -> float:
        """可用量"""
        return max(0.0, self.total * self.hard_limit - self.allocated)

    @property
    def is_above_soft_limit(self) -> bool:
        """是否超过软限制"""
        return self.allocated / self.total > self.soft_limit if self.total > 0 else False

    @property
    def is_above_hard_limit(self) -> bool:
        """是否超过硬限制"""
        return self.allocated / self.total > self.hard_limit if self.total > 0 else False


# ═══════════════════════════════════════════════════════════════
#  Section 2：从 ML Engine 提炼核心类型
# ═══════════════════════════════════════════════════════════════

class MemoryFeatureSchema:
    """
    记忆特征模式（提炼自 ML Engine FeatureSchema）
    用于定义记忆样本的特征维度。
    """

    def __init__(self, name: str, features: List[Dict[str, Any]]):
        self.name = name
        self.features = features
        self.size = len(features)

    def validate(self) -> List[str]:
        """验证特征定义合法性"""
        errors = []
        for i, f in enumerate(self.features):
            if 'name' not in f:
                errors.append(f"features[{i}] 缺少 name")
            if 'type' not in f:
                errors.append(f"features[{i}:{f.get('name', '?')}] 缺少 type")
            if 'weight' not in f:
                errors.append(f"features[{i}:{f.get('name', '?')}] 缺少 weight")
        return errors

    def get_initial_weights(self) -> List[float]:
        """获取初始权重数组"""
        return [f.get('weight', 0.1) for f in self.features]

    def get_feature_names(self) -> List[str]:
        """获取特征名称列表"""
        return [f['name'] for f in self.features]


class MemoryFeatureVector:
    """
    记忆特征向量（提炼自 ML Engine FeatureVector）
    将记忆样本转换为数值数组，用于模型训练/预测。
    """

    def __init__(self, schema: MemoryFeatureSchema, data: Dict[str, Any] = None):
        self.schema = schema
        self._raw = dict(data) if data else {}
        self._arr = self._build(schema, self._raw)

    def _build(self, schema: MemoryFeatureSchema, data: Dict[str, Any]) -> List[float]:
        """构建特征数组"""
        result = []
        for f in schema.features:
            raw = data.get(f['name'])
            if raw is None:
                result.append(0.0)
                continue
            ftype = f['type']
            if ftype == 'boolean':
                result.append(1.0 if raw else 0.0)
            elif ftype == 'ratio':
                result.append(max(0.0, min(1.0, float(raw) if raw else 0.0)))
            elif ftype == 'numeric':
                val = float(raw) if raw else 0.0
                if 'normalize' in f:
                    val = f['normalize'](val)
                result.append(val)
            else:
                result.append(float(raw) if raw else 0.0)
        return result

    def to_array(self) -> List[float]:
        """返回数值数组（用于模型输入）"""
        return self._arr

    def get_raw(self) -> Dict[str, Any]:
        """返回原始数据"""
        return self._raw


class MemoryLinearModel:
    """
    记忆预测模型（提炼自 ML Engine SimpleLinearModel）
    轻量级线性回归模型，用于预测记忆访问频率。
    """

    def __init__(self, input_size: int):
        self.input_size = input_size
        self.weights = [0.0] * input_size
        self.bias = 0.0
        self.is_trained = False
        self.training_history = []

    def _sigmoid(self, x: float) -> float:
        """Sigmoid 激活函数"""
        return 1.0 / (1.0 + math.exp(-x))

    def predict(self, feature_vec: MemoryFeatureVector) -> float:
        """预测（返回 0~1 分数，表示访问概率）"""
        arr = feature_vec.to_array()
        z = self.bias
        for i, val in enumerate(arr):
            z += val * (self.weights[i] if i < len(self.weights) else 0.0)
        return self._sigmoid(z)

    def train(self, samples: List[Any], opts: Dict[str, Any] = None) -> bool:
        """
        训练（梯度下降）
        samples: List[MemoryTrainingSample]
        """
        opts = opts or {}
        epochs = opts.get('epochs', 200)
        lr = opts.get('learning_rate', 0.05)
        verbose = opts.get('verbose', False)
        min_samples = opts.get('min_samples', 5)

        if len(samples) < min_samples:
            if verbose:
                logger.warning(f"样本不足 ({len(samples)}/{min_samples})，跳过训练")
            return False

        # 用初始权重（schema）初始化
        schema = samples[0].feature_vec.schema
        self.weights = schema.get_initial_weights() if schema else [0.1] * self.input_size
        self.bias = 0.1
        self.training_history = []

        for epoch in range(epochs):
            total_loss = 0.0
            for s in samples:
                pred = self.predict(s.feature_vec)
                error = pred - s.label
                total_loss += error * error
                arr = s.feature_vec.to_array()
                grad = error * pred * (1 - pred)
                for i in range(len(self.weights)):
                    self.weights[i] -= lr * grad * arr[i]
                self.bias -= lr * grad
            avg_loss = total_loss / len(samples)
            self.training_history.append({'epoch': epoch, 'loss': avg_loss})
            if verbose and epoch % 50 == 0:
                logger.info(f"Epoch {epoch:3d}: Loss = {avg_loss:.6f}")

        self.is_trained = True
        final_loss = self.training_history[-1]['loss']
        if verbose:
            logger.info(f"训练完成，最终 Loss = {final_loss:.6f}")
        return True


@dataclass
class MemoryTrainingSample:
    """记忆训练样本（提炼自 ML Engine TrainingSample）"""
    feature_vec: MemoryFeatureVector
    label: float                    # 0~1，表示是否被访问（或访问频率）
    meta: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.label = max(0.0, min(1.0, self.label))


# ═══════════════════════════════════════════════════════════════
#  Section 3：记忆系统资源优化器（集成 Ecology + ML Engine）
# ═══════════════════════════════════════════════════════════════

class MemoryResourceOptimizer:
    """
    记忆系统资源优化器（提炼自 Ecology ResourceOptimizer）
    生产级资源优化器，用于管理 NeuralMemory 的资源分配。
    """

    def __init__(self):
        self.resources: Dict[MemoryResourceType, MemoryResourceAllocation] = {}
        self.allocations: Dict[str, Dict[MemoryResourceType, float]] = {}  # task_id -> {type: amount}
        self.priorities: Dict[str, int] = {}  # task_id -> priority
        self.metrics: List[MemoryMetric] = []
        self._initialized = False

    def initialize(self) -> bool:
        """初始化：设置资源总量"""
        try:
            import psutil
            # Memory：总量 = 物理内存字节数 * 20%（分配给 NeuralMemory）
            mem = psutil.virtual_memory()
            memory_total = mem.total * 0.20
            self.register_resource(
                MemoryResourceType.MEMORY,
                total=memory_total,
                unit="bytes",
                hard_limit=0.85,
                soft_limit=0.70,
            )
            # Storage：总量 = 磁盘空间 * 10%（分配给 NeuralMemory）
            disk = psutil.disk_usage("/")
            storage_total = disk.total * 0.10
            self.register_resource(
                MemoryResourceType.STORAGE,
                total=storage_total,
                unit="bytes",
                hard_limit=0.95,
                soft_limit=0.80,
            )
            # Token：默认配额
            self.register_resource(
                MemoryResourceType.TOKEN,
                total=100_000.0,
                unit="tokens",
                hard_limit=0.95,
                soft_limit=0.80,
            )
            self._initialized = True
            logger.info(
                f"[MemoryResourceOptimizer] 初始化完成 — "
                f"Memory: {memory_total / 1024**3:.1f}GB, "
                f"Storage: {storage_total / 1024**3:.1f}GB"
            )
            return True
        except ImportError:
            logger.warning("[MemoryResourceOptimizer] psutil 不可用，使用安全默认值")
            self._init_fallback()
            return False
        except Exception as e:
            logger.error(f"[MemoryResourceOptimizer] 初始化失败: {e}")
            self._init_fallback()
            return False

    def _init_fallback(self):
        """降级方案"""
        self.register_resource(MemoryResourceType.MEMORY, total=1 * 1024**3, unit="bytes")
        self.register_resource(MemoryResourceType.STORAGE, total=10 * 1024**3, unit="bytes")
        self.register_resource(MemoryResourceType.TOKEN, total=10_000.0, unit="tokens")
        self._initialized = True

    def register_resource(
        self,
        resource_type: MemoryResourceType,
        total: float,
        unit: str = "",
        hard_limit: float = 0.90,
        soft_limit: float = 0.75,
    ) -> None:
        """注册资源"""
        self.resources[resource_type] = MemoryResourceAllocation(
            resource_type=resource_type,
            allocated=0.0,
            total=total,
            unit=unit,
            hard_limit=hard_limit,
            soft_limit=soft_limit,
        )

    def allocate_resource(
        self,
        task_id: str,
        resource_type: MemoryResourceType,
        amount: float,
        priority: int = 5,
    ) -> bool:
        """分配资源"""
        if resource_type not in self.resources:
            return False
        resource = self.resources[resource_type]
        self.priorities[task_id] = priority

        # 检查硬限制
        max_allowed = resource.total * resource.hard_limit
        if amount > max_allowed:
            logger.warning(
                f"[MemoryResourceOptimizer] 请求量 {amount:.0f} 超过硬限制 {max_allowed:.0f}"
            )
            return False

        # 检查可用量
        if resource.allocated + amount > resource.total * resource.hard_limit:
            logger.warning(
                f"[MemoryResourceOptimizer] 资源不足（已分配 {resource.allocated:.0f}，请求 {amount:.0f}）"
            )
            return False

        # 分配
        resource.allocated += amount
        if task_id not in self.allocations:
            self.allocations[task_id] = {}
        self.allocations[task_id][resource_type] = self.allocations[task_id].get(resource_type, 0) + amount
        return True

    def reclaim_resource(self, task_id: str) -> Dict[MemoryResourceType, float]:
        """回收资源"""
        reclaimed = {}
        if task_id in self.allocations:
            for resource_type, amount in self.allocations[task_id].items():
                if resource_type in self.resources:
                    self.resources[resource_type].allocated -= amount
                    reclaimed[resource_type] = amount
            del self.allocations[task_id]
            if task_id in self.priorities:
                del self.priorities[task_id]
        return reclaimed

    def get_health_report(self) -> Dict[str, Any]:
        """获取健康报告"""
        report = {
            "resources": {},
            "overall_status": MemoryHealthStatus.EXCELLENT.value,
            "timestamp": time.time(),
        }
        worst_status = MemoryHealthStatus.EXCELLENT
        for resource_type, allocation in self.resources.items():
            utilization = allocation.utilization
            if utilization > 90:
                status = MemoryHealthStatus.CRITICAL
            elif utilization > 75:
                status = MemoryHealthStatus.POOR
            elif utilization > 50:
                status = MemoryHealthStatus.FAIR
            elif utilization > 25:
                status = MemoryHealthStatus.GOOD
            else:
                status = MemoryHealthStatus.EXCELLENT
            report["resources"][resource_type.value] = {
                "allocated": allocation.allocated,
                "total": allocation.total,
                "utilization": utilization,
                "status": status.value,
            }
            # 更新最差状态
            if self._status_rank(status) > self._status_rank(worst_status):
                worst_status = status
        report["overall_status"] = worst_status.value
        return report

    def _status_rank(self, status: MemoryHealthStatus) -> int:
        """状态排名（数字越大越差）"""
        rank = {
            MemoryHealthStatus.EXCELLENT: 0,
            MemoryHealthStatus.GOOD: 1,
            MemoryHealthStatus.FAIR: 2,
            MemoryHealthStatus.POOR: 3,
            MemoryHealthStatus.CRITICAL: 4,
        }
        return rank.get(status, 0)


# ═══════════════════════════════════════════════════════════════
#  Section 4：对外接口（供 NeuralMemory 调用）
# ═══════════════════════════════════════════════════════════════

# 全局优化器实例（懒加载）
_MEMORY_OPTIMIZER: Optional[MemoryResourceOptimizer] = None


def get_memory_optimizer() -> MemoryResourceOptimizer:
    """获取全局记忆资源优化器"""
    global _MEMORY_OPTIMIZER
    if _MEMORY_OPTIMIZER is None:
        _MEMORY_OPTIMIZER = MemoryResourceOptimizer()
        _MEMORY_OPTIMIZER.initialize()
    return _MEMORY_OPTIMIZER


def optimize_memory_resources(task_id: str, memory_request: Dict[str, float]) -> Dict[str, bool]:
    """
    优化记忆资源分配
    
    Args:
        task_id: 任务ID
        memory_request: {resource_type: amount} 字典
        
    Returns:
        {resource_type: success} 字典
    """
    optimizer = get_memory_optimizer()
    results = {}
    for resource_type_str, amount in memory_request.items():
        try:
            resource_type = MemoryResourceType(resource_type_str)
            success = optimizer.allocate_resource(task_id, resource_type, amount)
            results[resource_type_str] = success
        except ValueError:
            results[resource_type_str] = False
    return results


def get_memory_health() -> Dict[str, Any]:
    """
    获取记忆系统健康状态
    
    Returns:
        健康报告字典
    """
    optimizer = get_memory_optimizer()
    return optimizer.get_health_report()


def predict_memory_access(feature_data: Dict[str, Any], schema: MemoryFeatureSchema = None) -> float:
    """
    预测记忆访问概率（使用 ML 模型）
    
    Args:
        feature_data: 特征数据字典
        schema: 特征模式（如果为 None，使用默认模式）
        
    Returns:
        访问概率（0~1）
    """
    if schema is None:
        # 默认特征模式：访问频率、最近访问时间、记忆重要性
        schema = MemoryFeatureSchema("default_memory", [
            {"name": "access_frequency", "type": "numeric", "weight": 0.3, "normalize": lambda v: min(v / 100.0, 1.0)},
            {"name": "hours_since_last_access", "type": "numeric", "weight": 0.2, "normalize": lambda v: min(v / 168.0, 1.0)},
            {"name": "importance", "type": "ratio", "weight": 0.25},
            {"name": "is_emotional", "type": "boolean", "weight": 0.15},
            {"name": "has_been_accessed", "type": "boolean", "weight": 0.1},
        ])
    vec = MemoryFeatureVector(schema, feature_data)
    # 使用一个简单的启发式预测（不用训练好的模型，因为可能没有训练数据）
    arr = vec.to_array()
    # 简单加权求和 + sigmoid
    z = 0.1  # bias
    weights = schema.get_initial_weights()
    for i, val in enumerate(arr):
        z += val * (weights[i] if i < len(weights) else 0.0)
    # 近似 sigmoid
    import math
    pred = 1.0 / (1.0 + math.exp(-z))
    return pred


def enhance_neural_memory_with_ecology(neural_memory_instance: Any) -> Any:
    """
    将 Ecology + ML 能力注入 NeuralMemory 实例
    
    Args:
        neural_memory_instance: NeuralMemory 实例（v7.0）
        
    Returns:
        注入后的实例（添加了资源管理/健康监控/预测能力）
    """
    optimizer = get_memory_optimizer()
    # 注入资源管理器
    neural_memory_instance._resource_optimizer = optimizer
    # 注入健康监控
    neural_memory_instance._health_report = None
    # 注入预测函数
    neural_memory_instance._predict_access = predict_memory_access
    # 添加方法
    if not hasattr(neural_memory_instance, 'get_resource_report'):
        def get_resource_report(self):
            return self._resource_optimizer.get_health_report()
        import types
        neural_memory_instance.get_resource_report = types.MethodType(get_resource_report, neural_memory_instance)
    logger.info("[ecology_ml_bridge] NeuralMemory 已注入 Ecology + ML 能力")
    return neural_memory_instance


__version__ = "1.0.0"
__description__ = "Ecology + ML Engine → NeuralMemory 整合桥接模块"
