"""autonomous_evolution_engine 基础模块 - enums + dataclasses"""
# 本文件内容由 autonomous_evolution_engine.py 拆分而来

import logging
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional
from dataclasses import dataclass, field

__all__ = [
    'get_degrading_modules',
    'get_weak_modules',
    'is_critical',
    'is_healthy',
]

logger = logging.getLogger(__name__)

class EvolutionStage(Enum):
    """进化阶段"""
    OBSERVATION = auto()      # 观察阶段
    ANALYSIS = auto()         # 分析阶段
    PLANNING = auto()         # 规划阶段
    EXECUTION = auto()        # 执行阶段
    VALIDATION = auto()       # 验证阶段
    ROLLBACK = auto()         # 回滚阶段

class EvolutionType(Enum):
    """进化类型"""
    STRATEGY_OPTIMIZATION = "strategy_optimization"    # strategy优化
    KNOWLEDGE_EXPANSION = "knowledge_expansion"        # 知识扩展
    ARCHITECTURE_ADJUSTMENT = "architecture_adjustment"  # 架构调整
    PERFORMANCE_TUNING = "performance_tuning"          # 性能调优
    QUALITY_IMPROVEMENT = "quality_improvement"        # 质量提升
    PREDICTIVE_MAINTENANCE = "predictive_maintenance"  # 预测性维护
    MULTI_OBJECTIVE_OPTIMIZATION = "multi_objective"   # 多目标优化

@dataclass
class EvolutionPlan:
    """进化计划"""
    evolution_id: str
    evolution_type: EvolutionType
    target_module: str
    current_state: Dict
    desired_state: Dict
    action_sequence: List[Dict]
    rollback_plan: List[Dict]
    expected_improvement: Dict
    risk_level: str  # low, medium, high
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"  # pending, executing, completed, failed, rolled_back
    priority: int = 5  # 1-10, 数字越小优先级越高
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他计划ID
    estimated_duration_minutes: int = 60
    actual_results: Dict = field(default_factory=dict)
    lessons_learned: List[str] = field(default_factory=list)

@dataclass
class SystemHealth:
    """系统健康状态"""
    overall_score: float  # 0-100
    module_health: Dict[str, float]
    performance_metrics: Dict[str, float]
    quality_metrics: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.now)
    trend: str = "stable"  # improving, stable, degrading
    predictions: Dict = field(default_factory=dict)  # 预测性metrics
    anomaly_alerts: List[Dict] = field(default_factory=list)  # 异常告警

    def is_healthy(self) -> bool:
        return self.overall_score >= 80

    def is_critical(self) -> bool:
        return self.overall_score < 60

    def get_weak_modules(self) -> List[str]:
        return [m for m, s in self.module_health.items() if s < 70]

    def get_degrading_modules(self) -> List[str]:
        """get健康度下降的模块"""
        degrading = []
        for module, score in self.module_health.items():
            if module in self.predictions.get("previous_scores", {}):
                prev_score = self.predictions["previous_scores"][module]
                if score < prev_score - 5:  # 下降超过5分
                    degrading.append({
                        "module": module,
                        "current": score,
                        "previous": prev_score,
                        "drop": prev_score - score
                    })
        return degrading
