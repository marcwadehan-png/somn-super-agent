"""
ROI 类型定义 - 指标类别、反馈来源、记录结构
ROI Types - Metric categories, feedback sources, record structures
"""

from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

class MetricCategory(Enum):
    """metrics类别"""
    TIME_SAVED = "time_saved"           # 时间节省
    TASK_COMPLETION = "task_completion" # 任务完成
    QUALITY_IMPROVEMENT = "quality"     # 质量提升
    COST_REDUCTION = "cost_reduction"   # 成本降低
    REVENUE_IMPACT = "revenue_impact"  # 收入影响
    USER_SATISFACTION = "satisfaction"  # 用户满意度

class FeedbackSource(Enum):
    """反馈来源"""
    USER_EXPLICIT = "user_explicit"     # 用户明确评价(评分/点赞/采纳)
    USER_IMPLICIT = "user_implicit"    # 用户隐式行为(停留时长/复购/沉默)
    SYSTEM_VALIDATION = "system_validation"  # 系统验证结果
    COMPARATIVE = "comparative"         # 对比分析(与历史基线对比)

@dataclass
class ROIRecord:
    """ROI记录"""
    record_id: str
    timestamp: str
    category: MetricCategory
    source: FeedbackSource

    # 投入侧
    input_metrics: Dict[str, float]  # 投入了什么 {时间投入, 资源消耗, ...}

    # 产出侧
    output_metrics: Dict[str, float]  # 产出是什么 {任务完成, 质量提升, ...}

    # 计算结果
    roi_ratio: float = 0.0
    efficiency_score: float = 0.0
    confidence: float = 0.5

    # 关联上下文
    task_type: str = ""
    strategy_used: str = ""
    notes: str = ""
    workflow_id: str = ""
    scope: str = "task"  # task | workflow | strategy_combo | validation
    strategy_combo_id: str = ""
    strategy_combo: List[str] = field(default_factory=list)

@dataclass
class PeriodROI:
    """周期ROI汇总"""
    period: str  # e.g. "2026-W14" 或 "2026-04"
    start_date: str
    end_date: str

    # 投入汇总
    total_time_invested_minutes: float = 0.0
    total_cost_estimate: float = 0.0

    # 产出汇总
    tasks_completed: int = 0
    tasks_quality_avg: float = 0.0
    time_saved_minutes: float = 0.0

    # ROImetrics
    overall_roi_ratio: float = 0.0
    efficiency_trend: str = "stable"  # improving / declining / stable
    confidence_band: Tuple[float, float] = (0.0, 0.0)  # 置信区间

    # 明细
    records: List[Dict] = field(default_factory=list)
__all__ = ['MetricCategory', 'FeedbackSource']
