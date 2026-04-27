"""
三十六计兵法策略引擎 - 兼容层
================================

此文件为兼容层，实际逻辑已拆分到 military_strategy/ 子包中。
旧导入路径完全兼容。

版本: v1.0.0
日期: 2026-04-08
"""

from .military_strategy import (
    MilitaryStrategyEngine,
    StrategyCategory,
    StrategyType,
    StrategyInfo,
    StrategyApplication,
    SituationAnalyzer,
    StrategyDatabase,
    StrategySelector,
)

__all__ = [
    'MilitaryStrategyEngine',
    'StrategyCategory',
    'StrategyType',
    'StrategyInfo',
    'StrategyApplication',
    'SituationAnalyzer',
    'StrategyDatabase',
    'StrategySelector',
]
