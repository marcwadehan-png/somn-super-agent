"""
__all__ = [
    'add',
    'add_trace',
    'copy_with',
    'filter_by_priority',
    'filter_by_type',
    'get_total_strength',
    'merge',
    'to_dict',
]

神经信号定义
神经网络中传递的信号
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional
import uuid

class SignalType(Enum):
    """信号类型"""
    DATA = auto()           # 数据信号
    CONTROL = auto()        # 控制信号
    FEEDBACK = auto()       # 反馈信号
    ERROR = auto()          # 错误信号
    WISDOM = auto()         # 智慧信号
    MEMORY = auto()         # 记忆信号
    LEARNING = auto()       # 学习信号
    ACTIVATION = auto()     # 激活信号
    INHIBITION = auto()     # 抑制信号

class SignalPriority(Enum):
    """信号优先级"""
    CRITICAL = 0    # 紧急
    HIGH = 1        # 高
    NORMAL = 2      # 正常
    LOW = 3         # 低
    BACKGROUND = 4  # 后台

@dataclass
class Signal:
    """
    神经信号
    
    在神经网络中传递的基本信息单元
    """
    source_id: str                              # 源神经元ID
    signal_type: SignalType                     # 信号类型
    data: Any                                   # 信号数据
    strength: float = 1.0                       # 信号强度 (0.0 - 1.0)
    priority: SignalPriority = SignalPriority.NORMAL  # 优先级
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))  # 信号ID
    timestamp: datetime = field(default_factory=datetime.now)  # 时间戳
    metadata: Dict[str, Any] = field(default_factory=dict)     # 元数据
    trace: List[str] = field(default_factory=list)             # 传播路径
    
    def add_trace(self, neuron_id: str):
        """添加传播路径记录"""
        self.trace.append(neuron_id)
    
    def copy_with(
        self,
        source_id: Optional[str] = None,
        signal_type: Optional[SignalType] = None,
        data: Any = None,
        strength: Optional[float] = None,
        priority: Optional[SignalPriority] = None,
        metadata: Optional[Dict] = None
    ) -> 'Signal':
        """创建信号的副本，可修改指定字段"""
        new_signal = Signal(
            source_id=source_id or self.source_id,
            signal_type=signal_type or self.signal_type,
            data=data if data is not None else self.data,
            strength=strength or self.strength,
            priority=priority or self.priority,
            metadata={**self.metadata, **(metadata or {})}
        )
        new_signal.trace = self.trace.copy()
        return new_signal
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "signal_id": self.signal_id,
            "source_id": self.source_id,
            "signal_type": self.signal_type.name,
            "data": self._serialize_data(),
            "strength": round(self.strength, 4),
            "priority": self.priority.name,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "trace": self.trace
        }
    
    def _serialize_data(self) -> Any:
        """序列化数据"""
        if isinstance(self.data, (str, int, float, bool, type(None))):
            return self.data
        elif isinstance(self.data, dict):
            return {k: str(v)[:100] for k, v in self.data.items()}
        elif isinstance(self.data, list):
            return [str(item)[:50] for item in self.data[:10]]
        else:
            return str(self.data)[:200]

@dataclass
class SignalBatch:
    """信号批次"""
    signals: List[Signal] = field(default_factory=list)
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    def add(self, signal: Signal):
        """添加信号"""
        self.signals.append(signal)
    
    def merge(self, other: 'SignalBatch'):
        """合并批次"""
        self.signals.extend(other.signals)
    
    def filter_by_type(self, signal_type: SignalType) -> List[Signal]:
        """按类型过滤"""
        return [s for s in self.signals if s.signal_type == signal_type]
    
    def filter_by_priority(self, min_priority: SignalPriority) -> List[Signal]:
        """按优先级过滤"""
        return [s for s in self.signals if s.priority.value <= min_priority.value]
    
    def get_total_strength(self) -> float:
        """获取总强度"""
        return sum(s.strength for s in self.signals)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "batch_id": self.batch_id,
            "signal_count": len(self.signals),
            "created_at": self.created_at.isoformat(),
            "signals": [s.to_dict() for s in self.signals[:10]]  # 只显示前10个
        }
