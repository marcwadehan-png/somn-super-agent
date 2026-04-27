"""global_wisdom_scheduler base: enums & dataclasses v1.0"""
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field, asdict, is_dataclass
from datetime import datetime
from enum import Enum
import logging
import uuid

__all__ = [
    'get_callback',
    'get_engine',
    'has_engine',
    'list_registered',
    'register_engine',
]

logger = logging.getLogger(__name__)

class SchedulerMode(Enum):
    SINGLE = "single"
    MULTI = "multi"
    FUSION = "fusion"
    AUTO = "auto"

class WisdomOutputFormat(Enum):
    BRIEF = "brief"
    STANDARD = "standard"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"

@dataclass
class SchedulerConfig:
    mode: SchedulerMode = SchedulerMode.AUTO
    output_format: WisdomOutputFormat = WisdomOutputFormat.STANDARD
    max_activated_schools: int = 5
    activation_threshold: float = 0.25
    enable_propagation: bool = True
    enable_learning: bool = True
    max_wait_time: float = 12.0  # [v1.0 去阻塞] 调度最大等待时间（秒），超时返回部分结果

    def to_dict(self) -> dict:
        """序列化为字典，用于配置缓存"""
        return {
            "mode": self.mode.value,
            "output_format": self.output_format.value,
            "max_activated_schools": self.max_activated_schools,
            "activation_threshold": self.activation_threshold,
            "enable_propagation": self.enable_propagation,
            "enable_learning": self.enable_learning,
            "max_wait_time": self.max_wait_time,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SchedulerConfig":
        """从字典恢复，用于配置缓存加载"""
        return cls(
            mode=SchedulerMode(data.get("mode", "auto")),
            output_format=WisdomOutputFormat(data.get("output_format", "standard")),
            max_activated_schools=data.get("max_activated_schools", 5),
            activation_threshold=data.get("activation_threshold", 0.25),
            enable_propagation=data.get("enable_propagation", True),
            enable_learning=data.get("enable_learning", True),
            max_wait_time=data.get("max_wait_time", 12.0),
        )
    fusion_method: str = "adaptive"

@dataclass
class WisdomQuery:
    query_id: str
    query_text: str
    context: Dict[str, Any] = field(default_factory=dict)
    problem_types: List[str] = field(default_factory=list)
    required_schools: List[str] = field(default_factory=list)
    excluded_schools: List[str] = field(default_factory=list)
    config: SchedulerConfig = field(default_factory=SchedulerConfig)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SchoolOutput:
    school_id: str
    school_name: str
    activation_level: float
    output: Dict[str, Any]
    confidence: float
    processing_time: float
    insights: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

@dataclass
class ScheduledResult:
    query_id: str
    query_text: str
    success: bool
    activated_schools: List[SchoolOutput]
    fused_wisdom: Dict[str, Any]
    integrated_insight: str
    network_insights: Dict[str, Any]
    synergy_score: float
    coverage: float
    confidence: float
    diversity: float
    processing_time: float
    timestamp: datetime = field(default_factory=datetime.now)
    # [v1.0 性能监控] 各阶段耗时（秒）
    step_times: Dict[str, float] = field(default_factory=dict)
    # [v1.0 性能监控] 缓存统计
    cache_stats: Dict[str, int] = field(default_factory=dict)
    # [v1.0 性能监控] 超时/跳过的学派数量
    timeout_count: int = 0

class WisdomEngineRegistry:
    def __init__(self):
        self._engines: Dict[str, Any] = {}
        self._callbacks: Dict[str, Callable] = {}
        self._initialized = False

    def register_engine(self, school_id: str, engine: Any, callback: Optional[Callable] = None):
        self._engines[school_id] = engine
        if callback:
            self._callbacks[school_id] = callback
        logger.info(f"已注册智慧引擎: {school_id}")

    def get_engine(self, school_id: str) -> Optional[Any]:
        return self._engines.get(school_id)

    def get_callback(self, school_id: str) -> Optional[Callable]:
        return self._callbacks.get(school_id)

    def has_engine(self, school_id: str) -> bool:
        return school_id in self._engines

    def list_registered(self) -> List[str]:
        return list(self._engines.keys())
