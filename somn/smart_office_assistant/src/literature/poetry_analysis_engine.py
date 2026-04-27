# -*- coding: utf-8 -*-
"""
诗词智能分析引擎 v1.0.0 [兼容层]

本文件已被模块化拆分，核心代码已迁移至 poetry_analysis_engine/ 包。
如需使用完整功能，请从包中导入 PoetryAnalysisEngine。

拆分后的包结构:
    poetry_analysis_engine/
        __init__.py         - 包导出
        _pae_core.py        - 核心引擎类
        _pae_types.py       - 类型定义
        _pae_resources.py    - 资源加载
        _pae_basic.py       - 基础分析
        _pae_intermediate.py - 中级分析
        _pae_advanced.py     - 高级分析
        _pae_scoring.py      - 评分
        _pae_comparison.py   - 比较分析

使用方式:
    from src.literature.poetry_analysis_engine import (
        PoetryAnalysisEngine,
        PoetryAnalysisLevel,
        PoetryStyle,
        PoetryAnalysisResult
    )
"""

# 向后兼容导入
from src.literature.poetry_analysis_engine._pae_core import PoetryAnalysisEngine
from src.literature.poetry_analysis_engine._pae_types import (
    PoetryAnalysisLevel,
    PoetryStyle,
    PoetryAnalysisResult,
)
from src.literature.poetry_analysis_engine._pae_resources import PoetryResourceLoader
from src.literature.poetry_analysis_engine._pae_basic import BasicAnalyzer
from src.literature.poetry_analysis_engine._pae_intermediate import IntermediateAnalyzer
from src.literature.poetry_analysis_engine._pae_advanced import AdvancedAnalyzer
from src.literature.poetry_analysis_engine._pae_scoring import PoetryScorer
from src.literature.poetry_analysis_engine._pae_comparison import PoetryComparator

__all__ = [
    "PoetryAnalysisEngine",
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
