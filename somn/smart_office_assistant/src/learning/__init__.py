"""
智能学习系统 [v1.0 延迟加载优化]
Learning System - 毫秒级启动

子目录结构:
  core/   - 核心协调与调度 (coordinator, smart_scheduler)
  engine/ - 具体学习引擎 (smart_learning_engine, local_data_learner, ppt_style_learner)
  neural/ - 自适应与神经网络学习 (adaptive_learning_coordinator)
  test/   - 测试用例

[v1.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v1.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # engine/smart_learning_engine
    from .engine.smart_learning_engine import (
        SmartLearningEngine, KnowledgeItem, KnowledgeQuality,
        RelevanceLevel, DecisionType, LearningDecision, create_knowledge_item,
    )
    # engine/ppt_style_learner
    from .engine.ppt_style_learner import (
        PPTStyleLearner, DesignPrinciple, ColorScheme,
        LayoutPattern, create_principle, create_color_scheme, create_layout_pattern,
    )
    # core/coordinator
    from .core.coordinator import (
        LearningCoordinator, LearningTask, LearningPriority,
        TaskStatus, EngineStatus, create_coordinator,
    )
    # core/smart_scheduler
    from .core.smart_scheduler import (
        SmartScheduler, SchedulingStrategy, ResourceState,
        ResourceMetrics, EngineMetrics, create_scheduler,
    )
    # engine/local_data_learner
    from .engine.local_data_learner import (
        LocalDataLearner, FileType, FileCategory,
        FileInfo, LearningResult, create_local_learner,
    )
    # neural/adaptive_learning_coordinator
    from .neural.adaptive_learning_coordinator import (
        AdaptiveLearningCoordinator, LearningStage, LearningStrategy,
        LearningTaskProfile, LearningPlan, AdaptiveScheduler,
        LearningHistory, KnowledgeGraph, LearningMonitor,
    )


def __getattr__(name: str) -> Any:
    """[v1.0 优化] 延迟加载 - 毫秒级启动"""

    # engine/smart_learning_engine
    if name in ('SmartLearningEngine', 'KnowledgeItem', 'KnowledgeQuality',
                'RelevanceLevel', 'DecisionType', 'LearningDecision', 'create_knowledge_item'):
        from .engine import smart_learning_engine as _m
        return getattr(_m, name)

    # engine/ppt_style_learner
    elif name in ('PPTStyleLearner', 'DesignPrinciple', 'ColorScheme',
                  'LayoutPattern', 'create_principle', 'create_color_scheme', 'create_layout_pattern'):
        from .engine import ppt_style_learner as _m
        return getattr(_m, name)

    # core/coordinator
    elif name in ('LearningCoordinator', 'LearningTask', 'LearningPriority',
                  'TaskStatus', 'EngineStatus', 'create_coordinator'):
        from .core import coordinator as _m
        return getattr(_m, name)

    # core/smart_scheduler
    elif name in ('SmartScheduler', 'SchedulingStrategy', 'ResourceState',
                  'ResourceMetrics', 'EngineMetrics', 'create_scheduler'):
        from .core import smart_scheduler as _m
        return getattr(_m, name)

    # engine/local_data_learner
    elif name in ('LocalDataLearner', 'FileType', 'FileCategory',
                  'FileInfo', 'LearningResult', 'create_local_learner'):
        from .engine import local_data_learner as _m
        return getattr(_m, name)

    # neural/adaptive_learning_coordinator
    elif name in ('AdaptiveLearningCoordinator', 'LearningStage', 'LearningStrategy',
                  'LearningTaskProfile', 'LearningPlan', 'AdaptiveScheduler',
                  'LearningHistory', 'KnowledgeGraph', 'LearningMonitor'):
        from .neural import adaptive_learning_coordinator as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'learning' has no attribute '{name}'")


__all__ = [
    # engine/smart_learning_engine
    'SmartLearningEngine', 'KnowledgeItem', 'KnowledgeQuality',
    'RelevanceLevel', 'DecisionType', 'LearningDecision', 'create_knowledge_item',
    # engine/ppt_style_learner
    'PPTStyleLearner', 'DesignPrinciple', 'ColorScheme',
    'LayoutPattern', 'create_principle', 'create_color_scheme', 'create_layout_pattern',
    # core/coordinator
    'LearningCoordinator', 'LearningTask', 'LearningPriority',
    'TaskStatus', 'EngineStatus', 'create_coordinator',
    # core/smart_scheduler
    'SmartScheduler', 'SchedulingStrategy', 'ResourceState',
    'ResourceMetrics', 'EngineMetrics', 'create_scheduler',
    # engine/local_data_learner
    'LocalDataLearner', 'FileType', 'FileCategory',
    'FileInfo', 'LearningResult', 'create_local_learner',
    # neural/adaptive_learning_coordinator
    'AdaptiveLearningCoordinator', 'LearningStage', 'LearningStrategy',
    'LearningTaskProfile', 'LearningPlan', 'AdaptiveScheduler',
    'LearningHistory', 'KnowledgeGraph', 'LearningMonitor',
]
