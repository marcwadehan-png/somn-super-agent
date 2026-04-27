# -*- coding: utf-8 -*-
"""图表生成器 - 类型定义模块"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

class ChartType(Enum):
    """图表类型枚举"""

    # 基础图表
    BAR = "bar"  # 柱状图
    COLUMN = "column"  # 条形图
    LINE = "line"  # 折线图
    PIE = "pie"  # 饼图
    SCATTER = "scatter"  # 散点图
    AREA = "area"  # 面积图

    # 组合图表
    STACKED_BAR = "stacked_bar"  # 堆叠柱状图
    GROUPED_BAR = "grouped_bar"  # 分组柱状图
    DUAL_AXIS = "dual_axis"  # 双轴图

    # 特殊图表
    HEATMAP = "heatmap"  # 热力图
    TREEMAP = "treemap"  # 树状图
    SUNBURST = "sunburst"  # 旭日图
    FUNNEL = "funnel"  # 漏斗图
    GAUGE = "gauge"  # 仪表盘
    RADAR = "radar"  # 雷达图

    # 时间序列
    TIMELINE = "timeline"  # 时间线图
    CANDLESTICK = "candlestick"  # K线图
    OHLC = "ohlc"  # OHLC图

    # 地理空间
    MAP = "map"  # 地图
    CHOROPLETH = "choropleth"  # 分级统计图

    # 表格
    TABLE = "table"  # 表格

class ChartLibrary(Enum):
    """图表库枚举"""
    PLOTLY = "plotly"  # Plotly - 交互式
    MATPLOTLIB = "matplotlib"  # Matplotlib - 静态

@dataclass
class ChartConfig:
    """图表配置"""

    chart_type: ChartType
    library: ChartLibrary = ChartLibrary.PLOTLY
    title: str = ""
    width: int = 800
    height: int = 600
    theme: str = "plotly_white"
    interactive: bool = True

    # 数据配置
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    color_column: Optional[str] = None
    size_column: Optional[str] = None
    group_column: Optional[str] = None
    parent_column: Optional[str] = None

    # 样式配置
    color_palette: List[str] = field(default_factory=list)
    show_legend: bool = True
    show_grid: bool = True
    show_annotations: bool = False

    # 交互配置
    hover_mode: str = "closest"
    enable_selection: bool = True

    # 导出配置
    output_format: str = "png"
    scale: float = 1.0

@dataclass
class DataFeature:
    """数据characteristics"""

    has_time_series: bool = False
    is_categorical: bool = False
    is_numerical: bool = False
    is_comparison: bool = False
    is_distribution: bool = False
    is_correlation: bool = False
    is_part_to_whole: bool = False
    is_hierarchical: bool = False
    data_volume: str = "small"
    variable_count: int = 1
    observation_count: int = 0

    # 新增字段
    time_columns: List[str] = field(default_factory=list)
    numeric_columns: List[str] = field(default_factory=list)
    categorical_columns: List[str] = field(default_factory=list)
    missing_ratio: float = 0.0
    unique_ratio: float = 0.0

@dataclass
class ChartRecommendation:
    """图表推荐结果"""

    chart_type: ChartType
    confidence: float
    library: ChartLibrary
    reason: str
    config: ChartConfig
