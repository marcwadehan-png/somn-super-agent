"""solution_assessment_framework 包 - Facade + 向后兼容导出"""
# 本文件内容由 solution_assessment_framework.py 拆分而来

from __future__ import annotations
from typing import Any, Dict, List

__all__ = [
    "AssessmentFactorType", "PainPointType",
    "ClientContext", "AssessmentFactor", "DynamicOutcomeRange", "AssessmentResult",
    "IndustryBenchmarkDB",
    "SolutionAssessmentEngine",
    "assess_solution_for_client", "quick_assessment", "get_assessment_engine",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name in ('AssessmentFactorType', 'PainPointType', 'ClientContext',
                'AssessmentFactor', 'DynamicOutcomeRange', 'AssessmentResult',
                'IndustryBenchmarkDB'):
        from ._saf_base import (
            AssessmentFactorType, PainPointType,
            ClientContext, AssessmentFactor, DynamicOutcomeRange, AssessmentResult,
            IndustryBenchmarkDB
        )
        mapping = {
            'AssessmentFactorType': AssessmentFactorType,
            'PainPointType': PainPointType,
            'ClientContext': ClientContext,
            'AssessmentFactor': AssessmentFactor,
            'DynamicOutcomeRange': DynamicOutcomeRange,
            'AssessmentResult': AssessmentResult,
            'IndustryBenchmarkDB': IndustryBenchmarkDB,
        }
        return mapping[name]
    if name == 'SolutionAssessmentEngine':
        from ._saf_engine import SolutionAssessmentEngine
        return SolutionAssessmentEngine
    if name == 'assess_solution_for_client':
        def assess_solution_for_client(solution_type: str, client_info: Dict[str, Any]) -> Dict[str, Any]:
            """便捷函数: 评估解决方案对特定客户的适用性"""
            from ._saf_engine import SolutionAssessmentEngine
            engine = SolutionAssessmentEngine()
            result = engine.assess_solution(solution_type, client_info)
            return {
                "solution_type": result.solution_type,
                "client_industry": result.client_context.industry,
                "customized_goals": result.customized_goals,
                "customized_metrics": result.customized_metrics,
                "outcome_ranges": [
                    {
                        "metric": o.metric_name,
                        "expected_range": o.calculated_range,
                        "industry_baseline": (o.industry_baseline_low, o.industry_baseline_high),
                    }
                    for o in result.outcome_ranges
                ],
                "success_probability": result.success_probability,
                "validation": result.validation_result,
                "assessment_quality": result.assessment_quality_score
            }
        return assess_solution_for_client
    if name == 'quick_assessment':
        def quick_assessment(solution_name: str, industry: str,
                            pain_points: List[str], execution_score: float = 5.0) -> Dict[str, Any]:
            """快速评估函数"""
            from ._saf_engine import SolutionAssessmentEngine
            engine = SolutionAssessmentEngine()
            result = engine.assess_solution(solution_name, {
                "industry": industry,
                "pain_points": pain_points,
                "execution_score": execution_score,
                "scale": "medium",
                "stage": "growth"
            })
            return {
                "solution_type": result.solution_type,
                "client_industry": result.client_context.industry,
                "success_probability": result.success_probability,
            }
        return quick_assessment
    if name == 'get_assessment_engine':
        def get_assessment_engine() -> Any:
            """获取评估引擎实例"""
            from ._saf_engine import SolutionAssessmentEngine
            return SolutionAssessmentEngine()
        return get_assessment_engine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
