"""
解决方案学习引擎 V1+V2 合并版 - 模块化包

原 solution_learning.py 已拆分为子模块
"""

from __future__ import annotations
from typing import Any

__all__ = [
    # V2 基准学习
    'LearningSourceType',
    'BenchmarkDataPoint',
    'IndustryBenchmarkUpdate',
    'BenchmarkLearningEngine',
    # V1 学习引擎
    'CapabilityType',
    'ServiceProvider',
    'CapabilityInsight',
    'LearningSession',
    'SolutionLearningEngine',
    # 工具
    'safe_yaml_load',
    'safe_yaml_dump',
    '_enum_to_str',
    # 执行器
    'DailyLearningExecutor',
    # 集成
    'integrate_with_template_library',
    # 全局实例
    'solution_learning_engine',
    'daily_learning_executor',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    # V2 基准学习
    if name == 'LearningSourceType':
        from ._sl_v2_enums import LearningSourceType
        return LearningSourceType
    if name == 'BenchmarkDataPoint':
        from ._sl_v2_dataclasses import BenchmarkDataPoint
        return BenchmarkDataPoint
    if name == 'IndustryBenchmarkUpdate':
        from ._sl_v2_dataclasses import IndustryBenchmarkUpdate
        return IndustryBenchmarkUpdate
    if name == 'BenchmarkLearningEngine':
        from ._sl_v2_engine import BenchmarkLearningEngine
        return BenchmarkLearningEngine
    # V1 学习引擎
    if name == 'CapabilityType':
        from ._sl_v1_enums import CapabilityType
        return CapabilityType
    if name == 'ServiceProvider':
        from ._sl_v1_dataclasses import ServiceProvider
        return ServiceProvider
    if name == 'CapabilityInsight':
        from ._sl_v1_dataclasses import CapabilityInsight
        return CapabilityInsight
    if name == 'LearningSession':
        from ._sl_v1_dataclasses import LearningSession
        return LearningSession
    if name == 'SolutionLearningEngine':
        from ._sl_v1_engine import SolutionLearningEngine
        return SolutionLearningEngine
    # 工具函数
    if name == 'safe_yaml_load':
        from ._sl_utils import safe_yaml_load
        return safe_yaml_load
    if name == 'safe_yaml_dump':
        from ._sl_utils import safe_yaml_dump
        return safe_yaml_dump
    if name == '_enum_to_str':
        from ._sl_utils import _enum_to_str
        return _enum_to_str
    # 执行器
    if name == 'DailyLearningExecutor':
        from ._sl_executor import DailyLearningExecutor
        return DailyLearningExecutor
    # 集成
    if name == 'integrate_with_template_library':
        from ._sl_integration import integrate_with_template_library
        return integrate_with_template_library
    # 全局实例
    if name == 'solution_learning_engine':
        from ._sl_globals import solution_learning_engine
        return solution_learning_engine
    if name == 'daily_learning_executor':
        from ._sl_globals import daily_learning_executor
        return daily_learning_executor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
