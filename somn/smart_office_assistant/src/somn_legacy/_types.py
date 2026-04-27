"""
Somn 类型定义 - 从 somn.py 拆分
包含 SomnConfig, AnalysisRequest, AnalysisResult
"""



__all__ = [
    'SomnConfig',
    'AnalysisRequest',
    'AnalysisResult',
]
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from src.industry_engine import IndustryType

@dataclass
class SomnConfig:
    """Somn配置"""
    # 功能开关
    enable_web_search: bool = True
    enable_ml_engine: bool = True
    enable_knowledge_graph: bool = True
    enable_neural_memory: bool = True
    enable_narrative_intelligence: bool = True  # [v1.0.0] 叙事智能

    # 加载优化配置 [v1.0]
    enable_preload: bool = True           # 是否启用预加载
    preload_delay: float = 2.0         # 启动后延迟N秒开始预加载
    parallel_preload: bool = True        # 是否并行预加载
    eager_load_layers: List[str] = field(default_factory=lambda: ['1'])  # 立即加载的层

    # 行业设置
    default_industry: IndustryType = IndustryType.SAAS_B2B

    # 输出设置
    output_format: str = "yaml"
    verbose: bool = True

@dataclass
class AnalysisRequest:
    """分析请求"""
    request_type: str  # growth_plan / demand_analysis / funnel_analysis / journey_mapping
    business_context: Dict

    # 可选参数
    industry: Optional[str] = None
    time_horizon: str = "3个月"
    specific_focus: Optional[str] = None

@dataclass
class AnalysisResult:
    """分析结果"""
    request_id: str
    request_type: str
    status: str  # success / partial / failed

    # 结果数据
    data: Dict

    # 元数据
    execution_time: float
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # 建议的后续action
    next_steps: List[str] = field(default_factory=list)
