# -*- coding: utf-8 -*-
"""图表生成器包

模块化重构后的图表自动生成引擎

子模块:
    _cg_core: 核心接口
    _cg_types: 类型定义
    _cg_analyzer: 数据分析
    _cg_recommender: 推荐器
    _cg_plotly: Plotly生成器
    _cg_matplotlib: Matplotlib生成器
"""

from ._cg_core import ChartGenerator
from ._cg_types import ChartType, ChartLibrary, ChartConfig, DataFeature, ChartRecommendation
from ._cg_analyzer import DataAnalyzer
from ._cg_recommender import ChartRecommender
from ._cg_plotly import PlotlyChartGenerator
from ._cg_matplotlib import MatplotlibChartGenerator

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
