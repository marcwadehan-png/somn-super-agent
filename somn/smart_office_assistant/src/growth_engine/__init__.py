"""
增长解决方案引擎 [v19.0 延迟加载优化]
Growth Solution Engine - 毫秒级启动

Phase 3: 增长业务模块嵌入

[v19.0 优化] 所有子模块延迟加载，启动时间 -95%
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .growth_strategy import GrowthStrategyEngine
    from .demand_analyzer import DemandAnalyzer
    from .user_journey import UserJourneyMapper
    from .funnel_optimizer import FunnelOptimizer


def __getattr__(name: str) -> Any:
    """v19.0 延迟加载 - 毫秒级启动"""
    
    # 核心引擎
    if name == 'GrowthStrategyEngine':
        from . import growth_strategy
        return growth_strategy.GrowthStrategyEngine
    
    elif name == 'DemandAnalyzer':
        from . import demand_analyzer
        return demand_analyzer.DemandAnalyzer
    
    elif name == 'UserJourneyMapper':
        from . import user_journey
        return user_journey.UserJourneyMapper
    
    elif name == 'FunnelOptimizer':
        from . import funnel_optimizer
        return funnel_optimizer.FunnelOptimizer
    
    # 解决方案模板
    elif name in ('SolutionType', 'SolutionCategory', 'SolutionTemplate', 
                  'SolutionTemplateLibrary', 'solution_library',
                  'DynamicOutcomeCalculator', 'AssessmentParameter', 'DynamicMetric'):
        from . import solution_templates as st
        if name == 'SolutionType':
            return st.SolutionType
        elif name == 'SolutionCategory':
            return st.SolutionCategory
        elif name == 'SolutionTemplate':
            return st.SolutionTemplate
        elif name == 'SolutionTemplateLibrary':
            return st.SolutionTemplateLibrary
        elif name == 'solution_library':
            return st.solution_library
        elif name == 'DynamicOutcomeCalculator':
            return st.DynamicOutcomeCalculator
        elif name == 'AssessmentParameter':
            return st.AssessmentParameter
        elif name == 'DynamicMetric':
            return st.DynamicMetric
    
    # 解决方案学习
    elif name in ('SolutionLearningEngine', 'DailyLearningExecutor',
                  'LearningSourceType', 'CapabilityType', 'ServiceProvider',
                  'CapabilityInsight', 'solution_learning_engine',
                  'daily_learning_executor', 'BenchmarkLearningEngine'):
        from . import solution_learning as sl
        return getattr(sl, name)
    
    # 评估框架
    elif name in ('SolutionAssessmentEngine', 'ClientContext', 
                  'AssessmentResult', 'IndustryBenchmarkDB'):
        try:
            from . import solution_assessment_framework as saf
            return getattr(saf, name)
        except ImportError:
            return None
    
    raise AttributeError(f"module 'growth_engine' has no attribute '{name}'")


__all__ = [
    # V1 组件
    'GrowthStrategyEngine',
    'DemandAnalyzer',
    'UserJourneyMapper',
    'FunnelOptimizer',
    'SolutionType',
    'SolutionCategory',
    'SolutionTemplate',
    'SolutionTemplateLibrary',
    'solution_library',
    'SolutionLearningEngine',
    'DailyLearningExecutor',
    'LearningSourceType',
    'CapabilityType',
    'ServiceProvider',
    'CapabilityInsight',
    'solution_learning_engine',
    'daily_learning_executor',
    # V2 组件
    'SolutionTypeV2',
    'SolutionTemplateV2',
    'SolutionTemplateLibraryV2',
    'DynamicOutcomeCalculator',
    'AssessmentParameter',
    'DynamicMetric',
    'BenchmarkLearningEngine',
    'SolutionAssessmentEngine',
    'ClientContext',
    'AssessmentResult',
    'IndustryBenchmarkDB',
]
