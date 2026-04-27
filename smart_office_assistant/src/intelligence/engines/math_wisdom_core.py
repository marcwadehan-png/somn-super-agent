"""
Math Wisdom Core - 数学智慧核心模块 (兼容层)
============================================

重构后主文件仅保留向后兼容导入。
子模块:
  math_wisdom/_mw_enums.py     - 枚举定义
  math_wisdom/_mw_dataclasses.py - 数据类定义
  math_wisdom/_mw_sequence.py  - 数列分析引擎
  math_wisdom/_mw_graph.py     - 图论分析引擎
  math_wisdom/_mw_combinatorial.py - 组合优化引擎
  math_wisdom/_mw_probability.py - 离散概率引擎
  math_wisdom/_mw_core.py      - 数学智慧核心引擎
"""

from .math_wisdom import (
    SequenceType,
    GraphType,
    TrendType,
    OptimizationGoal,
    SequenceAnalysis,
    GraphAnalysis,
    ProbabilityAnalysis,
    OptimizationResult,
    MathWisdomInsight,
    SequenceAnalyzer,
    GraphAnalyzer,
    CombinatorialOptimizer,
    DiscreteProbabilityEngine,
    MathWisdomCore,
)

__all__ = [
    'MathWisdomCore',
    'SequenceAnalyzer',
    'GraphAnalyzer',
    'CombinatorialOptimizer',
    'DiscreteProbabilityEngine',
    'SequenceType',
    'GraphType',
    'TrendType',
    'OptimizationGoal',
    'SequenceAnalysis',
    'GraphAnalysis',
    'ProbabilityAnalysis',
    'OptimizationResult',
    'MathWisdomInsight',
]
