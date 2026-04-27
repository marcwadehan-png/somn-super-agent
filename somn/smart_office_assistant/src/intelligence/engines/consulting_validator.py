"""
增长咨询智能验证引擎 v1.0
Growth Consulting Intelligence Validator v1.0

拆分后版本:
- _cv_types.py: 枚举与数据结构
- _cv_research.py: 五维调研完整性检查器
- _cv_reasoning.py: 六步战略推理验证器
- _cv_antipattern.py: 反模式检测器
- _cv_scorer.py: 方案质量评分器
- _cv_core.py: 核心控制器

版本: v1.0
日期: 2026-04-08
"""

# 类型定义
from ._cv_types import (
    ResearchDimension,
    ReasoningStep,
    AntiPatternType,
    SeverityLevel,
    QualityDimension,
    ResearchCheckItem,
    ContradictionDetection,
    AntiPatternDetection,
    QualityScoreDetail,
    ValidationIssue,
    ConsultingValidationResult,
)

# 核心类
from ._cv_core import ConsultingValidator

# 向后兼容别名
ConsultingValidatorV1 = ConsultingValidator

__all__ = [
    # 枚举
    'ResearchDimension',
    'ReasoningStep',
    'AntiPatternType',
    'SeverityLevel',
    'QualityDimension',
    # 数据类
    'ResearchCheckItem',
    'ContradictionDetection',
    'AntiPatternDetection',
    'QualityScoreDetail',
    'ValidationIssue',
    'ConsultingValidationResult',
    # 验证器
    'ConsultingValidator',
    'ConsultingValidatorV1',
]
