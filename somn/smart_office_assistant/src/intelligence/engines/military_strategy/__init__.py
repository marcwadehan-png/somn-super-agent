"""
三十六计兵法策略引擎包
==================

包含完整的三十六计智慧系统，支持形势分析、计谋选择和策略建议。

使用示例:
    from military_strategy import MilitaryStrategyEngine

    engine = MilitaryStrategyEngine()
    advice = engine.get_strategy_advice(situation)
"""

from __future__ import annotations
from typing import Any

__all__ = [
    'StrategyCategory',
    'StrategyType',
    'StrategyInfo',
    'StrategyApplication',
    'MilitaryStrategyEngine',
    'SituationAnalyzer',
    'StrategyDatabase',
    'StrategySelector'
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'StrategyCategory':
        from ._ms_enums import StrategyCategory
        return StrategyCategory
    if name == 'StrategyType':
        from ._ms_enums import StrategyType
        return StrategyType
    if name == 'StrategyInfo':
        from ._ms_dataclasses import StrategyInfo
        return StrategyInfo
    if name == 'StrategyApplication':
        from ._ms_dataclasses import StrategyApplication
        return StrategyApplication
    if name == 'SituationAnalyzer':
        from ._ms_situation import SituationAnalyzer
        return SituationAnalyzer
    if name == 'StrategyDatabase':
        from ._ms_database import StrategyDatabase
        return StrategyDatabase
    if name == 'StrategySelector':
        from ._ms_selector import StrategySelector
        return StrategySelector
    if name == 'MilitaryStrategyEngine':
        from ._ms_engine import MilitaryStrategyEngine
        return MilitaryStrategyEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
