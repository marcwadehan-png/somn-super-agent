"""
解决方案模板库 V2 - 模块化包

原 solution_templates.py 已拆分为子模块
"""

from __future__ import annotations
from typing import Any

__all__ = [
    # 枚举
    'SolutionType',
    'SolutionCategory',
    # 数据类
    'AssessmentParameter',
    'DynamicMetric',
    'SolutionTemplateV2',
    # 核心类
    'SolutionTemplateLibraryV2',
    'DynamicOutcomeCalculator',
    # 便捷接口
    'solution_library_v2',
    'outcome_calculator',
    'quick_calculate',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'SolutionType':
        from ._st_enums import SolutionType
        return SolutionType
    if name == 'SolutionCategory':
        from ._st_enums import SolutionCategory
        return SolutionCategory
    if name == 'AssessmentParameter':
        from ._st_dataclasses import AssessmentParameter
        return AssessmentParameter
    if name == 'DynamicMetric':
        from ._st_dataclasses import DynamicMetric
        return DynamicMetric
    if name == 'SolutionTemplateV2':
        from ._st_dataclasses import SolutionTemplateV2
        return SolutionTemplateV2
    if name == 'SolutionTemplateLibraryV2':
        from ._st_library import SolutionTemplateLibraryV2
        return SolutionTemplateLibraryV2
    if name == 'DynamicOutcomeCalculator':
        from ._st_calculator import DynamicOutcomeCalculator
        return DynamicOutcomeCalculator
    if name == 'solution_library_v2':
        from ._st_utils import solution_library_v2
        return solution_library_v2
    if name == 'outcome_calculator':
        from ._st_utils import outcome_calculator
        return outcome_calculator
    if name == 'quick_calculate':
        from ._st_utils import quick_calculate
        return quick_calculate
    # V1 兼容别名
    if name == 'SolutionTemplateLibrary':
        from ._st_library import SolutionTemplateLibraryV2
        return SolutionTemplateLibraryV2
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
