"""
Math Wisdom Core - 数学智慧核心模块
====================================

基于离散数学与数列数学的智能分析与决策支持系统

子模块:
  _mw_enums.py     - 枚举定义
  _mw_dataclasses.py - 数据类定义
  _mw_sequence.py  - 数列分析引擎
  _mw_graph.py     - 图论分析引擎
  _mw_combinatorial.py - 组合优化引擎
  _mw_probability.py - 离散概率引擎
  _mw_core.py      - 数学智慧核心引擎
"""

from __future__ import annotations
from typing import Any

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


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'SequenceType':
        from ._mw_enums import SequenceType
        return SequenceType
    if name == 'GraphType':
        from ._mw_enums import GraphType
        return GraphType
    if name == 'TrendType':
        from ._mw_enums import TrendType
        return TrendType
    if name == 'OptimizationGoal':
        from ._mw_enums import OptimizationGoal
        return OptimizationGoal
    if name == 'SequenceAnalysis':
        from ._mw_dataclasses import SequenceAnalysis
        return SequenceAnalysis
    if name == 'GraphAnalysis':
        from ._mw_dataclasses import GraphAnalysis
        return GraphAnalysis
    if name == 'ProbabilityAnalysis':
        from ._mw_dataclasses import ProbabilityAnalysis
        return ProbabilityAnalysis
    if name == 'OptimizationResult':
        from ._mw_dataclasses import OptimizationResult
        return OptimizationResult
    if name == 'MathWisdomInsight':
        from ._mw_dataclasses import MathWisdomInsight
        return MathWisdomInsight
    if name == 'SequenceAnalyzer':
        from ._mw_sequence import SequenceAnalyzer
        return SequenceAnalyzer
    if name == 'GraphAnalyzer':
        from ._mw_graph import GraphAnalyzer
        return GraphAnalyzer
    if name == 'CombinatorialOptimizer':
        from ._mw_combinatorial import CombinatorialOptimizer
        return CombinatorialOptimizer
    if name == 'DiscreteProbabilityEngine':
        from ._mw_probability import DiscreteProbabilityEngine
        return DiscreteProbabilityEngine
    if name == 'MathWisdomCore':
        from ._mw_core import MathWisdomCore
        return MathWisdomCore
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
