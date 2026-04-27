"""
解决方案模板库 V2 - 动态评估版本
基于客户实际情况的动态效果评估,替代固定预期值

原文件已拆分为 solution_templates/ 子包
此文件仅作向后兼容使用
"""

from .solution_templates import (
    SolutionType,
    SolutionCategory,
    AssessmentParameter,
    DynamicMetric,
    SolutionTemplateV2,
    SolutionTemplateLibraryV2,
    DynamicOutcomeCalculator,
    solution_library_v2,
    outcome_calculator,
    quick_calculate,
)

__all__ = [
    'SolutionType',
    'SolutionCategory',
    'AssessmentParameter',
    'DynamicMetric',
    'SolutionTemplateV2',
    'SolutionTemplateLibraryV2',
    'DynamicOutcomeCalculator',
    'solution_library_v2',
    'outcome_calculator',
    'quick_calculate',
]
