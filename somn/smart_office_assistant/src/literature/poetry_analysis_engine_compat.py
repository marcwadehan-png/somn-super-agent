# -*- coding: utf-8 -*-
"""
诗词智能分析引擎 v1.0.0 [兼容层]

本文件已被模块化拆分，核心代码已迁移至 poetry_analysis_engine/ 包。
请使用新的导入方式:

    from src.literature.poetry_analysis_engine import (
        PoetryAnalysisEngine,
        PoetryAnalysisLevel,
        PoetryStyle,
        PoetryAnalysisResult
    )

原始文件: poetry_analysis_engine.py (987行)
拆分时间: 2026-04-08
"""

# 兼容层 - 从包中重新导出所有公开接口
from src.literature.poetry_analysis_engine import (
    PoetryAnalysisLevel,
    PoetryStyle,
    PoetryAnalysisResult,
    PoetryResourceLoader,
    BasicAnalyzer,
    IntermediateAnalyzer,
    AdvancedAnalyzer,
    PoetryScorer,
    PoetryComparator,
)

# 核心引擎类（向后兼容）
from src.literature.poetry_analysis_engine._pae_core import PoetryAnalysisEngine

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
