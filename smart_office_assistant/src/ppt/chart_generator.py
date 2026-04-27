# -*- coding: utf-8 -*-
"""
图表自动生成引擎 [兼容层]

本文件已被模块化拆分，核心代码已迁移至 ppt/chart_generator/ 包。

使用方式:
    from src.ppt.chart_generator import (
        ChartGenerator,
        ChartType,
        ChartLibrary,
        ChartConfig,
        DataFeature,
        ChartRecommendation
    )

拆分后的包结构:
    chart_generator/
        __init__.py        - 包导出
        _cg_core.py       - 核心接口
        _cg_types.py      - 类型定义
        _cg_analyzer.py   - 数据分析
        _cg_recommender.py - 推荐器
        _cg_plotly.py     - Plotly生成器
        _cg_matplotlib.py - Matplotlib生成器
"""

# 向后兼容导入
from src.ppt.chart_generator import (
    ChartGenerator,
    ChartType,
    ChartLibrary,
    ChartConfig,
    DataFeature,
    ChartRecommendation,
    DataAnalyzer,
    ChartRecommender,
    PlotlyChartGenerator,
    MatplotlibChartGenerator,
)

__all__ = [
    "ChartGenerator",
    "ChartType",
    "ChartLibrary",
    "ChartConfig",
    "DataFeature",
    "ChartRecommendation",
    "DataAnalyzer",
    "ChartRecommender",
    "PlotlyChartGenerator",
    "MatplotlibChartGenerator",
]
