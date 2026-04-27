"""V2 数据类定义"""



__all__ = [
    'BenchmarkDataPoint',
    'IndustryBenchmarkUpdate',
]
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ._sl_v2_enums import LearningSourceType

@dataclass
class BenchmarkDataPoint:
    """基准数据点"""
    metric_name: str                 # metrics名称
    industry: str                    # 行业
    value_low: float                 # 低值
    value_typical: float             # 典型值
    value_high: float                # 高值
    
    # 数据来源
    source_provider: str             # 数据来源服务商
    source_type: LearningSourceType
    source_url: Optional[str] = None
    
    # 数据质量
    confidence: float = 0.7          # 置信度
    sample_size: Optional[int] = None  # 样本量
    data_date: Optional[str] = None  # 数据时间
    
    # 上下文
    context: Dict = field(default_factory=dict)  # 额外上下文
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class IndustryBenchmarkUpdate:
    """行业基准更新记录"""
    update_id: str
    solution_type: str               # 解决方案类型
    industry: str                    # 行业
    metric_name: str                 # metrics名称
    
    # 旧值
    old_baseline: Dict
    
    # 新值
    new_baseline: Dict
    
    # 变更原因
    change_reason: str
    data_points: List[BenchmarkDataPoint]  # 支撑数据点
    
    # 验证状态
    validation_status: str = "pending"  # pending/verified/rejected
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
