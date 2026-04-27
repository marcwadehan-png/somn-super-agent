# -*- coding: utf-8 -*-
"""AI原生增长策略 - 枚举与数据类

__all__ = [
    'projected_value',
    'time_to_target',
    'to_dict',
]

包含:
- GrowthPattern: 增长模式枚举
- GrowthMetric: 增长指标数据类
- GrowthStrategy: 增长策略数据类
- GrowthExperiment: 增长实验数据类
- AttributionResult: 归因结果数据类
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime

class GrowthPattern(Enum):
    """AI原生增长模式"""
    VIRAL_LOOP = "viral_loop"              # 病毒式传播
    NETWORK_EFFECTS = "network_effects"    # 网络效应
    DATA_FLYWHEEL = "data_flywheel"        # 数据飞轮
    AGENT_ECOSYSTEM = "agent_ecosystem"    # 智能体生态
    AUTONOMOUS_EVOLUTION = "autonomous_evolution"  # 自主进化
    COMPOUND_INTELLIGENCE = "compound_intelligence"  # 复合智能

@dataclass
class GrowthMetric:
    """增长metrics"""
    name: str
    current_value: float
    target_value: float
    growth_rate: float  # 日增长率
    timestamp: datetime = field(default_factory=datetime.now)
    
    def projected_value(self, days: int) -> float:
        """预测未来值"""
        return self.current_value * ((1 + self.growth_rate) ** days)
    
    def time_to_target(self) -> Optional[int]:
        """计算达到目标所需天数"""
        if self.growth_rate <= 0 or self.current_value >= self.target_value:
            return None
        import math
        days = math.log(self.target_value / self.current_value) / math.log(1 + self.growth_rate)
        return int(days)

@dataclass
class GrowthStrategy:
    """增长strategy"""
    id: str
    name: str
    pattern: GrowthPattern
    description: str
    implementation_steps: List[Dict]
    required_resources: Dict[str, Any]
    expected_outcomes: Dict[str, float]
    risk_factors: List[str]
    success_metrics: List[str]
    is_active: bool = False
    experiment_id: Optional[str] = None  # 关联的实验ID
    variant_name: Optional[str] = None   # A/B测试变体名称
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "pattern": self.pattern.value,
            "description": self.description,
            "implementation_steps": self.implementation_steps,
            "required_resources": self.required_resources,
            "expected_outcomes": self.expected_outcomes,
            "risk_factors": self.risk_factors,
            "success_metrics": self.success_metrics,
            "is_active": self.is_active,
            "experiment_id": self.experiment_id,
            "variant_name": self.variant_name
        }

@dataclass
class GrowthExperiment:
    """增长实验"""
    id: str
    name: str
    hypothesis: str
    control_variant: GrowthStrategy
    treatment_variants: List[GrowthStrategy]
    success_criteria: Dict[str, Any]
    duration_days: int
    sample_size: int
    status: str = "pending"  # pending, running, completed, cancelled
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    results: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "hypothesis": self.hypothesis,
            "control_variant": self.control_variant.to_dict(),
            "treatment_variants": [v.to_dict() for v in self.treatment_variants],
            "success_criteria": self.success_criteria,
            "duration_days": self.duration_days,
            "sample_size": self.sample_size,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "results": self.results
        }

@dataclass
class AttributionResult:
    """归因分析结果"""
    touchpoint: str
    attributed_conversions: int
    attributed_revenue: float
    attribution_percentage: float
    model_type: str  # first_touch, last_touch, linear, time_decay, data_driven
    
    def to_dict(self) -> Dict:
        return {
            "touchpoint": self.touchpoint,
            "attributed_conversions": self.attributed_conversions,
            "attributed_revenue": self.attributed_revenue,
            "attribution_percentage": self.attribution_percentage,
            "model_type": self.model_type
        }

# 类型别名，方便使用
ExperimentVariant = GrowthStrategy
