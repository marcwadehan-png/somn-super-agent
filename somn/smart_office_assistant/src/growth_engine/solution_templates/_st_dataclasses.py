"""数据类定义模块"""



__all__ = [
    'AssessmentParameter',
    'DynamicMetric',
    'SolutionTemplateV2',
]
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from ._st_enums import SolutionType, SolutionCategory

@dataclass
class AssessmentParameter:
    """评估参数定义"""
    param_name: str                     # 参数名称
    param_type: str                     # 类型: float/int/str/bool/list
    description: str                    # 描述
    required: bool = True               # 是否必填
    default_value: Any = None           # 默认值
    valid_range: Optional[Tuple] = None # 有效范围
    options: Optional[List] = None      # 可选值列表

@dataclass
class DynamicMetric:
    """动态metrics定义"""
    metric_id: str                      # metricsID
    metric_name: str                    # metrics名称
    unit: str                           # 单位: %/倍/元/个
    
    # 基准区间(按行业细分)
    industry_baselines: Dict[str, Dict] = field(default_factory=dict)
    
    # 计算公式(可选,用于复杂metrics)
    calculation_formula: Optional[str] = None
    
    # 影响因素权重
    factor_weights: Dict[str, float] = field(default_factory=dict)
    
    # 评估说明
    assessment_notes: str = ""

@dataclass
class SolutionTemplateV2:
    """解决方案模板 V2 - 支持动态评估"""
    solution_id: str
    solution_type: SolutionType
    name: str
    category: SolutionCategory
    description: str
    
    # 适用条件(用于初步筛选)
    applicable_industries: List[str] = field(default_factory=list)
    applicable_stages: List[str] = field(default_factory=list)
    applicable_scales: List[str] = field(default_factory=list)
    
    # 评估参数定义(客户需要提供的信息)
    required_parameters: List[AssessmentParameter] = field(default_factory=list)
    
    # 动态metrics定义(预期效果)
    dynamic_metrics: List[DynamicMetric] = field(default_factory=list)
    
    # 核心strategy(保持原有结构)
    core_strategies: List[Dict] = field(default_factory=list)
    
    # 执行步骤
    implementation_steps: List[Dict] = field(default_factory=list)
    
    # 所需资源
    required_resources: Dict = field(default_factory=dict)
    
    # 常见陷阱
    common_pitfalls: List[str] = field(default_factory=list)
    
    # 工具推荐
    recommended_tools: List[str] = field(default_factory=list)
    
    # 最佳实践案例
    case_studies: List[Dict] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "2.0"
