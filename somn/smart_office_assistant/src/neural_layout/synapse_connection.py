"""
__all__ = [
    'get_stats',
    'strengthen',
    'to_dict',
    'transmit',
    'update_weight',
    'weaken',
]

突触连接定义
神经元之间的连接
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, Optional
import uuid

from .signal import Signal, SignalType

class ConnectionType(Enum):
    """连接类型"""
    EXCITATORY = auto()     # 兴奋性连接 (增强信号)
    INHIBITORY = auto()     # 抑制性连接 (减弱信号)
    MODULATORY = auto()     # 调制性连接 (调节信号)
    RECURRENT = auto()      # 递归连接 (反馈回路)
    GAP_JUNCTION = auto()   # 间隙连接 (直接传递)

@dataclass
class SynapseConnection:
    """
    突触连接
    
    连接两个神经元的通道，具有权重和可塑性
    """
    source_id: str                              # 源神经元ID
    target_id: str                              # 目标神经元ID
    connection_type: ConnectionType = ConnectionType.EXCITATORY
    weight: float = 1.0                         # 连接权重
    delay: float = 0.0                          # 信号延迟(秒)
    synapse_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    # 可塑性
    plasticity_enabled: bool = True             # 是否启用可塑性
    learning_rate: float = 0.01                 # 学习率
    last_update: Optional[datetime] = None      # 最后更新时间
    
    # 统计
    transmission_count: int = 0                 # 传输次数
    success_count: int = 0                      # 成功次数
    total_strength_transmitted: float = 0.0     # 传输的总强度
    
    def transmit(self, signal: Signal) -> Optional[Signal]:
        """
        传递信号
        
        Args:
            signal: 输入信号
            
        Returns:
            传递后的信号，如果信号被阻断则返回None
        """
        self.transmission_count += 1
        
        # 根据连接类型处理信号
        if self.connection_type == ConnectionType.EXCITATORY:
            new_strength = signal.strength * self.weight
        elif self.connection_type == ConnectionType.INHIBITORY:
            new_strength = signal.strength * (1.0 - self.weight)
        elif self.connection_type == ConnectionType.MODULATORY:
            new_strength = signal.strength * (0.5 + 0.5 * self.weight)
        else:
            new_strength = signal.strength
        
        # 信号太弱则阻断
        if new_strength < 0.01:
            return None
        
        self.success_count += 1
        self.total_strength_transmitted += new_strength
        
        # 创建传递后的信号
        transmitted = signal.copy_with(
            source_id=self.source_id,
            strength=new_strength
        )
        transmitted.add_trace(self.synapse_id)
        
        return transmitted
    
    def update_weight(self, delta: float) -> None:
        """更新权重 (Hebbian学习)"""
        if not self.plasticity_enabled:
            return
        
        self.weight = max(0.0, min(2.0, self.weight + delta * self.learning_rate))
        self.last_update = datetime.now()
    
    def strengthen(self, amount: float = 0.1) -> None:
        """增强连接"""
        self.update_weight(amount)
    
    def weaken(self, amount: float = 0.1) -> None:
        """减弱连接"""
        self.update_weight(-amount)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        success_rate = (
            self.success_count / self.transmission_count 
            if self.transmission_count > 0 else 0
        )
        return {
            "synapse_id": self.synapse_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "connection_type": self.connection_type.name,
            "weight": round(self.weight, 4),
            "delay": self.delay,
            "transmission_count": self.transmission_count,
            "success_rate": round(success_rate, 4),
            "avg_strength": round(
                self.total_strength_transmitted / self.success_count 
                if self.success_count > 0 else 0, 4
            )
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "synapse_id": self.synapse_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "connection_type": self.connection_type.name,
            "weight": self.weight,
            "delay": self.delay,
            "plasticity_enabled": self.plasticity_enabled,
            "stats": self.get_stats()
        }
