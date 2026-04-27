"""solution_assessment_framework 基础模块 - enums + dataclasses + 行业基准"""
# 本文件内容由 solution_assessment_framework.py 拆分而来

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

__all__ = [
    'calculate_impact',
    'calculate_range',
    'get_all_metrics',
    'get_benchmark',
]

class AssessmentFactorType(Enum):
    """评估因子类型"""
    INDUSTRY = "industry"
    SCALE = "scale"
    STAGE = "stage"
    PAIN_POINT = "pain_point"
    HISTORICAL_PERFORMANCE = "historical"
    EXECUTION_CAPABILITY = "execution"
    MARKET_ENVIRONMENT = "market"

class PainPointType(Enum):
    """痛点类型"""
    HIGH_CAC = "high_cac"
    LOW_RETENTION = "low_retention"
    LOW_CONVERSION = "low_conversion"
    LOW_EFFICIENCY = "low_efficiency"
    BRAND_WEAK = "brand_weak"
    DATA_SILO = "data_silo"
    POOR_EXPERIENCE = "poor_experience"
    SCALING_DIFFICULTY = "scaling_difficulty"

@dataclass
class ClientContext:
    """客户上下文 - 深度需求分析结果"""
    industry: str
    sub_industry: Optional[str] = None
    company_scale: str = "medium"
    development_stage: str = "growth"
    annual_revenue: Optional[float] = None
    avg_order_value: Optional[float] = None
    business_model: Optional[str] = None
    main_channels: List[str] = field(default_factory=list)
    historical_metrics: Dict[str, float] = field(default_factory=dict)
    historical_growth_rate: Optional[float] = None
    primary_pain_points: List[PainPointType] = field(default_factory=list)
    pain_point_severity: Dict[str, int] = field(default_factory=dict)
    team_size: Optional[int] = None
    execution_capability_score: float = 5.0
    budget_range: Optional[str] = None
    market_competition_level: str = "medium"
    market_growth_rate: Optional[float] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class AssessmentFactor:
    """评估因子"""
    factor_type: AssessmentFactorType
    factor_name: str
    weight: float
    impact_direction: str = "positive"
    base_multiplier: float = 1.0
    adjustment_range: Tuple[float, float] = (0.5, 1.5)

    def calculate_impact(self, context_value: Any) -> float:
        return self.base_multiplier

@dataclass
class DynamicOutcomeRange:
    """动态效果区间"""
    metric_name: str
    industry_baseline_low: float
    industry_baseline_high: float
    industry_baseline_typical: float
    client_adjustment_factors: Dict[str, float] = field(default_factory=dict)
    execution_discount: float = 0.7
    calculated_range: Optional[Tuple[float, float]] = None
    confidence_level: float = 0.7

    def calculate_range(self, context: ClientContext) -> Tuple[float, float]:
        base_low = self.industry_baseline_low
        base_high = self.industry_baseline_high
        adjustment = 1.0
        for factor_name, factor_value in self.client_adjustment_factors.items():
            adjustment *= factor_value
        execution_factor = context.execution_capability_score / 10 * self.execution_discount
        final_low = base_low * adjustment * execution_factor * 0.8
        final_high = base_high * adjustment * execution_factor * 1.2
        self.calculated_range = (final_low, final_high)
        return self.calculated_range

@dataclass
class AssessmentResult:
    """评估结果"""
    solution_type: str
    client_context: ClientContext
    customized_goals: List[Dict] = field(default_factory=list)
    customized_metrics: List[Dict] = field(default_factory=list)
    outcome_ranges: List[DynamicOutcomeRange] = field(default_factory=list)
    assessment_quality_score: float = 0.0
    risk_factors: List[str] = field(default_factory=list)
    success_probability: float = 0.7
    validation_result: Optional[Dict] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class IndustryBenchmarkDB:
    """行业基准数据库"""

    def __init__(self):
        self.benchmarks = self._init_benchmarks()

    def _init_benchmarks(self) -> Dict:
        return {
            "private_domain": {
                "电商": {
                    "cac_reduction": {"low": 15, "typical": 30, "high": 50},
                    "ltv_lift": {"low": 20, "typical": 50, "high": 100},
                    "conversion_rate": {"low": 5, "typical": 10, "high": 20},
                },
                "零售": {
                    "cac_reduction": {"low": 10, "typical": 25, "high": 40},
                    "ltv_lift": {"low": 15, "typical": 40, "high": 80},
                    "conversion_rate": {"low": 3, "typical": 8, "high": 15},
                },
                "美妆": {
                    "cac_reduction": {"low": 20, "typical": 35, "high": 55},
                    "ltv_lift": {"low": 30, "typical": 60, "high": 120},
                    "conversion_rate": {"low": 8, "typical": 15, "high": 25},
                },
                "母婴": {
                    "cac_reduction": {"low": 15, "typical": 30, "high": 45},
                    "ltv_lift": {"low": 25, "typical": 50, "high": 100},
                    "conversion_rate": {"low": 5, "typical": 12, "high": 20},
                },
            },
            "membership": {
                "零售": {
                    "penetration_rate": {"low": 20, "typical": 40, "high": 60},
                    "arpu_lift": {"low": 1.5, "typical": 3.0, "high": 5.0},
                    "retention_lift": {"low": 10, "typical": 25, "high": 50},
                },
                "餐饮": {
                    "penetration_rate": {"low": 25, "typical": 50, "high": 70},
                    "arpu_lift": {"low": 1.3, "typical": 2.5, "high": 4.0},
                    "retention_lift": {"low": 15, "typical": 30, "high": 55},
                },
                "航空": {
                    "penetration_rate": {"low": 30, "typical": 55, "high": 75},
                    "arpu_lift": {"low": 2.0, "typical": 4.0, "high": 6.0},
                    "retention_lift": {"low": 20, "typical": 35, "high": 60},
                },
            },
            "digital_operation": {
                "全行业": {
                    "efficiency_lift": {"low": 30, "typical": 80, "high": 150},
                    "automation_rate": {"low": 40, "typical": 70, "high": 90},
                    "decision_speed": {"low": 2, "typical": 5, "high": 10},
                },
            },
            "douyin": {
                "全品类": {
                    "gmv_growth": {"low": 50, "typical": 200, "high": 800},
                    "roi": {"low": 1.5, "typical": 3.0, "high": 5.0},
                    "follower_growth": {"low": 5, "typical": 30, "high": 100},
                },
            },
            "xiaohongshu": {
                "美妆": {
                    "engagement_rate": {"low": 3, "typical": 8, "high": 15},
                    "conversion_rate": {"low": 1, "typical": 4, "high": 10},
                },
                "母婴": {
                    "engagement_rate": {"low": 4, "typical": 10, "high": 18},
                    "conversion_rate": {"low": 2, "typical": 5, "high": 12},
                },
                "食品": {
                    "engagement_rate": {"low": 5, "typical": 12, "high": 20},
                    "conversion_rate": {"low": 3, "typical": 6, "high": 15},
                },
            },
            "crm": {
                "B2B": {
                    "sales_efficiency": {"low": 20, "typical": 40, "high": 60},
                    "win_rate": {"low": 15, "typical": 30, "high": 50},
                    "sales_cycle_reduction": {"low": 10, "typical": 25, "high": 40},
                },
                "SaaS": {
                    "sales_efficiency": {"low": 25, "typical": 45, "high": 65},
                    "win_rate": {"low": 20, "typical": 35, "high": 55},
                    "sales_cycle_reduction": {"low": 15, "typical": 30, "high": 45},
                },
            },
        }

    def get_benchmark(self, solution_type: str, industry: str, metric: str) -> Dict:
        solution_data = self.benchmarks.get(solution_type, {})
        industry_data = solution_data.get(industry, solution_data.get("全行业", {}))
        return industry_data.get(metric, {"low": 10, "typical": 30, "high": 50})

    def get_all_metrics(self, solution_type: str, industry: str) -> Dict:
        solution_data = self.benchmarks.get(solution_type, {})
        return solution_data.get(industry, solution_data.get("全行业", {}))
