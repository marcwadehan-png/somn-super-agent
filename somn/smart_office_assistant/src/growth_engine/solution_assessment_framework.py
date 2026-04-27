"""
solution_assessment_framework - 向后兼容层
本文件已拆分为 solution_assessment_framework/ 子包
所有内容已迁移至子包，请直接导入子包：
    from src.growth_engine.solution_assessment_framework import SolutionAssessmentEngine
    from src.growth_engine import assess_solution_for_client, quick_assessment

（原有 import 路径继续兼容）
"""

from src.growth_engine.solution_assessment_framework import (
    AssessmentFactorType,
    PainPointType,
    ClientContext,
    AssessmentFactor,
    DynamicOutcomeRange,
    AssessmentResult,
    IndustryBenchmarkDB,
    SolutionAssessmentEngine,
    assess_solution_for_client,
    quick_assessment,
    get_assessment_engine,
)

__all__ = [
    "AssessmentFactorType",
    "PainPointType",
    "ClientContext",
    "AssessmentFactor",
    "DynamicOutcomeRange",
    "AssessmentResult",
    "IndustryBenchmarkDB",
    "SolutionAssessmentEngine",
    "assess_solution_for_client",
    "quick_assessment",
    "get_assessment_engine",
]
