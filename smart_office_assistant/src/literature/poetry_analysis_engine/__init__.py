# -*- coding: utf-8 -*-
"""诗词分析引擎包

模块化重构后的诗词智能分析引擎

子模块:
    _pae_core: 核心引擎类
    _pae_types: 类型定义
    _pae_basic: 基础分析（韵律、结构、语言）
    _pae_resources: 资源加载
    _pae_intermediate: 中级分析（意象、情感、主题）
    _pae_advanced: 高级分析（风格、影响、创新性）
    _pae_scoring: 评分
    _pae_comparison: 比较分析
"""

from ._pae_core import PoetryAnalysisEngine
from ._pae_types import PoetryAnalysisLevel, PoetryStyle, PoetryAnalysisResult
from ._pae_resources import PoetryResourceLoader
from ._pae_basic import BasicAnalyzer
from ._pae_intermediate import IntermediateAnalyzer
from ._pae_advanced import AdvancedAnalyzer
from ._pae_scoring import PoetryScorer
from ._pae_comparison import PoetryComparator

__all__ = [
    "PoetryAnalysisLevel",
    "PoetryStyle",
    "PoetryAnalysisResult",
    "PoetryResourceLoader",
    "BasicAnalyzer",
    "IntermediateAnalyzer",
    "AdvancedAnalyzer",
    "PoetryScorer",
    "PoetryComparator",
]
