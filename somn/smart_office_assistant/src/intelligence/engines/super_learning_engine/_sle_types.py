"""
__all__ = [
    'avg_execution_time',
    'is_overloaded',
    'load_score',
    'success_rate',
    'update',
    'update_by_capability',
]

超级学习引擎类型定义
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class LearningCapability(Enum):
    """学习能力类型"""
    INSTANCE_LEARNING = "instance_learning"      # 实例学习
    VALIDATION_LEARNING = "validation_learning"  # 验证学习
    ERROR_LEARNING = "error_learning"            # 错误学习
    ASSOCIATION_LEARNING = "association_learning"# 关联学习
    TRANSFER_LEARNING = "transfer_learning"      # 迁移学习
    REINFORCEMENT_LEARNING = "reinforcement_learning"  # 强化学习
    LOCAL_DATA_LEARNING = "local_data_learning"  # 本地数据学习
    NEURAL_LEARNING = "neural_learning"          # 神经记忆学习
    SMART_LEARNING = "smart_learning"            # 智能学习
    CONTINUOUS_LEARNING = "continuous_learning"  # 持续学习
    META_LEARNING = "meta_learning"              # 元学习 - 学会如何学习
    NARRATIVE_LEARNING = "narrative_learning"    # 叙事学习 [v1.0.0 文学智能增强]

@dataclass
class LearningRequest:
    """学习请求"""
    capability: LearningCapability  # 学习能力类型
    input_data: Any                  # 输入数据
    request_id: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5                 # 优先级(1-10)
    timeout: Optional[float] = None   # 超时时间(秒); None 时回退到引擎默认配置
    
    def __post_init__(self):
        if not self.request_id:
            self.request_id = f"learning_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        if self.input_data is None:
            self.input_data = {}

@dataclass
class LearningResult:
    """学习结果"""
    capability: LearningCapability
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    request_id: str = ""
    confidence: float = 0.0
    execution_time: float = 0.0
    engine_used: str = ""
    error: Optional[str] = None
    next_actions: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class LearningStats:
    """学习统计摘要."""
    total_requests: int = 0
    successful_requests: int = 0
    total_execution_time: float = 0.0
    capability_breakdown: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        if self.total_requests <= 0:
            return 0.0
        return self.successful_requests / self.total_requests

    @property
    def avg_execution_time(self) -> float:
        if self.total_requests <= 0:
            return 0.0
        return self.total_execution_time / self.total_requests

    def update(self, success: bool, execution_time: float) -> None:
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        self.total_execution_time += execution_time

    def update_by_capability(
        self,
        capability: LearningCapability,
        success: bool,
        execution_time: float
    ) -> None:
        capability_name = capability.value
        bucket = self.capability_breakdown.setdefault(
            capability_name,
            {
                "total_requests": 0,
                "successful_requests": 0,
                "total_execution_time": 0.0,
            }
        )
        bucket["total_requests"] += 1
        if success:
            bucket["successful_requests"] += 1
        bucket["total_execution_time"] += execution_time

@dataclass
class EngineLoadInfo:
    """引擎负载与可用性信息."""
    name: str = ""
    active_tasks: int = 0
    queue_size: int = 0
    avg_response_time: float = 0.0
    available: bool = True

    @property
    def load_score(self) -> float:
        return round(min(1.0, (self.active_tasks + self.queue_size) / 30), 2)

    @property
    def is_overloaded(self) -> bool:
        return self.load_score > 0.8
