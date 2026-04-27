# -*- coding: utf-8 -*-
"""AI原生增长策略包 - AINativeGrowthStrategies

整合多种AI原生增长模式:
- 数据飞轮 (AIDataFlywheel)
- 智能体网络效应 (AgentNetworkEffects)
- 复合智能 (CompoundIntelligence)
- 增长实验框架 (GrowthExperimentFramework)
- 统计引擎 (StatisticalEngine)
- 归因分析器 (AttributionAnalyzer)
- AI原生增长引擎 (AINativeGrowthEngine)

架构: Facade + 子模块委托模式
"""

from __future__ import annotations
from typing import Any

__all__ = [
    # 枚举与数据类
    "GrowthPattern",
    "GrowthMetric",
    "GrowthStrategy",
    "GrowthExperiment",
    "AttributionResult",
    "ExperimentVariant",
    # 子系统
    "AIDataFlywheel",
    "AgentNetworkEffects",
    "CompoundIntelligence",
    "GrowthExperimentFramework",
    "StatisticalEngine",
    "AttributionAnalyzer",
    # 主引擎
    "AINativeGrowthEngine",
    # 便捷函数
    "analyze_growth_opportunity",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'GrowthPattern':
        from ._aing_enums import GrowthPattern
        return GrowthPattern
    if name == 'GrowthMetric':
        from ._aing_enums import GrowthMetric
        return GrowthMetric
    if name == 'GrowthStrategy':
        from ._aing_enums import GrowthStrategy
        return GrowthStrategy
    if name == 'GrowthExperiment':
        from ._aing_enums import GrowthExperiment
        return GrowthExperiment
    if name == 'AttributionResult':
        from ._aing_enums import AttributionResult
        return AttributionResult
    if name == 'ExperimentVariant':
        from ._aing_enums import ExperimentVariant
        return ExperimentVariant
    if name == 'AIDataFlywheel':
        from ._aing_data_flywheel import AIDataFlywheel
        return AIDataFlywheel
    if name == 'AgentNetworkEffects':
        from ._aing_network import AgentNetworkEffects
        return AgentNetworkEffects
    if name == 'CompoundIntelligence':
        from ._aing_compound import CompoundIntelligence
        return CompoundIntelligence
    if name == 'GrowthExperimentFramework':
        from ._aing_experiment import GrowthExperimentFramework
        return GrowthExperimentFramework
    if name == 'StatisticalEngine':
        from ._aing_stats import StatisticalEngine
        return StatisticalEngine
    if name == 'AttributionAnalyzer':
        from ._aing_attribution import AttributionAnalyzer
        return AttributionAnalyzer
    if name == 'AINativeGrowthEngine':
        from ._aing_engine import AINativeGrowthEngine
        return AINativeGrowthEngine
    if name == 'analyze_growth_opportunity':
        from ._aing_engine import analyze_growth_opportunity
        return analyze_growth_opportunity
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
