"""
具体学习引擎模块
Concrete learning engines
"""

from .smart_learning_engine import (
    SmartLearningEngine,
    KnowledgeItem,
    KnowledgeQuality,
    RelevanceLevel,
    DecisionType,
    LearningDecision,
    create_knowledge_item
)
from .local_data_learner import (
    LocalDataLearner,
    FileType,
    FileCategory,
    FileInfo,
    LearningResult,
    create_local_learner
)
from .ppt_style_learner import (
    PPTStyleLearner,
    DesignPrinciple,
    ColorScheme,
    LayoutPattern,
    create_principle,
    create_color_scheme,
    create_layout_pattern
)

__all__ = [
    # smart_learning_engine
    'SmartLearningEngine',
    'KnowledgeItem',
    'KnowledgeQuality',
    'RelevanceLevel',
    'DecisionType',
    'LearningDecision',
    'create_knowledge_item',
    # local_data_learner
    'LocalDataLearner',
    'FileType',
    'FileCategory',
    'FileInfo',
    'LearningResult',
    'create_local_learner',
    # ppt_style_learner
    'PPTStyleLearner',
    'DesignPrinciple',
    'ColorScheme',
    'LayoutPattern',
    'create_principle',
    'create_color_scheme',
    'create_layout_pattern',
]
