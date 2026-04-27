"""数学智慧核心 - 枚举定义"""

from enum import Enum

class SequenceType(Enum):
    """数列类型"""
    ARITHMETIC = "arithmetic"           # 等差数列
    GEOMETRIC = "geometric"             # 等比数列
    FIBONACCI = "fibonacci"             # 斐波那契数列
    POLYNOMIAL = "polynomial"           # 多项式数列
    EXPONENTIAL = "exponential"        # 指数数列
    LOGARITHMIC = "logarithmic"        # 对数数列
    UNKNOWN = "unknown"                  # 未知类型

class GraphType(Enum):
    """图类型"""
    DIRECTED = "directed"               # 有向图
    UNDIRECTED = "undirected"           # 无向图
    WEIGHTED = "weighted"               # 加权图
    TREE = "tree"                       # 树
    DAG = "dag"                         # 有向无环图
    BIPARTITE = "bipartite"            # 二部图
    COMPLETE = "complete"              # 完全图

class TrendType(Enum):
    """趋势类型"""
    LINEAR_GROWTH = "linear_growth"     # 线性增长(等差)
    EXPONENTIAL_GROWTH = "exponential_growth"  # 指数增长(等比)
    GOLDEN_GROWTH = "golden_growth"     # 黄金增长(斐波那契)
    DECAYING = "decaying"               # 衰减
    FLUCTUATING = "fluctuating"         # 波动
    STABLE = "stable"                   # 稳定

class OptimizationGoal(Enum):
    """优化目标"""
    MAXIMIZE = "maximize"               # 最大化
    MINIMIZE = "minimize"               # 最小化
    BALANCE = "balance"                 # 平衡
