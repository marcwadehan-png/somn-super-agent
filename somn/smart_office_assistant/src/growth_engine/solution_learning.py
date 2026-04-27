"""
解决方案学习引擎 V1+V2 合并版
V1: SolutionLearningEngine - 服务商信息收集与能力提取
V2: BenchmarkLearningEngine - 从服务商数据中提取行业基准

原文件已拆分为 solution_learning/ 子包
此文件仅作向后兼容使用
"""

from .solution_learning import (
    # V2 基准学习
    LearningSourceType,
    BenchmarkDataPoint,
    IndustryBenchmarkUpdate,
    BenchmarkLearningEngine,
    # V1 学习引擎
    CapabilityType,
    ServiceProvider,
    CapabilityInsight,
    LearningSession,
    SolutionLearningEngine,
    # 工具
    safe_yaml_load,
    safe_yaml_dump,
    _enum_to_str,
    # 执行器
    DailyLearningExecutor,
    # 集成
    integrate_with_template_library,
    # 全局实例
    solution_learning_engine,
    daily_learning_executor,
)

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
