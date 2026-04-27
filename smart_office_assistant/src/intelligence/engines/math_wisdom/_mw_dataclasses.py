"""数学智慧核心 - 数据类定义"""



__all__ = [
    'SequenceAnalysis',
    'GraphAnalysis',
    'ProbabilityAnalysis',
    'OptimizationResult',
    'MathWisdomInsight',
]
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple

from ._mw_enums import SequenceType, GraphType, OptimizationGoal

@dataclass
class SequenceAnalysis:
    """数列分析结果"""
    sequence_type: SequenceType
    pattern_description: str
    next_value: Optional[float] = None
    confidence: float = 0.0
    
    # 数列参数
    first_term: Optional[float] = None
    common_diff: Optional[float] = None  # 等差公差
    common_ratio: Optional[float] = None  # 等比公比
    
    # 预测值
    predictions: List[float] = field(default_factory=list)
    
    # 模型参数
    model_params: Dict[str, Any] = field(default_factory=dict)
    
    # 评估metrics
    r_squared: float = 0.0  # 决定系数
    rmse: float = 0.0  # 均方根误差
    mape: float = 0.0  # 平均绝对百分比误差

@dataclass
class GraphAnalysis:
    """图分析结果"""
    graph_type: GraphType
    node_count: int
    edge_count: int
    density: float = 0.0
    
    # 连通性
    is_connected: bool = False
    connected_components: int = 0
    
    # 中心性
    centrality: Dict[str, float] = field(default_factory=dict)
    
    # 最短路径
    shortest_paths: Dict[Tuple[str, str], float] = field(default_factory=dict)
    
    # 社区检测
    communities: List[List[str]] = field(default_factory=list)

@dataclass
class ProbabilityAnalysis:
    """概率分析结果"""
    prior_probability: float = 0.0
    likelihood: float = 0.0
    posterior_probability: float = 0.0
    
    # 信息论metrics
    entropy: float = 0.0
    mutual_information: float = 0.0
    kl_divergence: float = 0.0
    
    # 贝叶斯推断
    credible_interval: Tuple[float, float] = (0.0, 1.0)
    bayes_factor: float = 1.0

@dataclass
class OptimizationResult:
    """优化结果"""
    goal: OptimizationGoal
    optimal_value: float
    optimal_choice: Any = None
    
    # 方案比较
    alternatives: List[Tuple[Any, float]] = field(default_factory=list)
    
    # 分析
    sensitivity: Dict[str, float] = field(default_factory=dict)
    constraints_satisfied: bool = True

@dataclass
class MathWisdomInsight:
    """数学智慧洞察"""
    insight_type: str
    title: str
    description: str
    mathematical_basis: str
    application_scenario: str
    confidence: float = 0.0
    recommendations: List[str] = field(default_factory=list)
