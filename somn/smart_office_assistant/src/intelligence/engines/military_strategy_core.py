"""
兵法策略引擎 - 兼容层
重导出到子包以支持向后兼容
"""

# 从子包重新导出所有公共API
from .military_strategy import (
    StrategyCategory,
    StrategyType,
    StrategyInfo,
    StrategyApplication,
    MilitaryStrategyEngine,
    SituationAnalyzer,
    StrategyDatabase,
    StrategySelector,
)

__all__ = [
    'StrategyCategory',
    'StrategyType',
    'StrategyInfo',
    'StrategyApplication',
    'MilitaryStrategyEngine',
    'SituationAnalyzer',
    'StrategyDatabase',
    'StrategySelector',
]
