# -*- coding: utf-8 -*-
"""图表生成器 - 核心接口模块"""
from typing import Optional, Tuple, Union, Dict, List
from ._cg_types import ChartType, ChartLibrary, ChartConfig, ChartRecommendation
from ._cg_recommender import ChartRecommender
from ._cg_plotly import PlotlyChartGenerator
from ._cg_matplotlib import MatplotlibChartGenerator

__all__ = [
    'generate_chart',
    'recommend_chart',
]

class ChartGenerator:
    """图表generate器 - unified接口"""

    def __init__(self, preferred_library: ChartLibrary = ChartLibrary.PLOTLY):
        """
        init图表generate器

        Args:
            preferred_library: 首选图表库
        """
        self.preferred_library = preferred_library
        self.recommender = ChartRecommender()
        self.plotly_generator = PlotlyChartGenerator()
        self.matplotlib_generator = MatplotlibChartGenerator()

    def generate_chart(
        self,
        data: Union[Dict, List[Dict]],
        chart_type: Optional[ChartType] = None,
        library: Optional[ChartLibrary] = None,
        title: str = "",
        **kwargs
    ) -> Tuple[str, ChartRecommendation]:
        """
        generate图表

        Args:
            data: 数据
            chart_type: 图表类型(可选,自动推荐)
            library: 图表库(可选,默认使用首选库)
            title: 图表标题
            **kwargs: 其他配置参数

        Returns:
            (图表文件路径, 推荐结果)
        """
        # 推荐图表类型
        if not chart_type:
            recommendations = self.recommender.recommend(data)
            if not recommendations:
                raise ValueError("无法推荐图表类型")
            recommendation = recommendations[0]
            chart_type = recommendation.chart_type
            if not library:
                library = recommendation.library
        else:
            recommendation = ChartRecommendation(
                chart_type=chart_type,
                confidence=1.0,
                library=library or self.preferred_library,
                reason="用户指定",
                config=ChartConfig(chart_type=chart_type, library=library or self.preferred_library)
            )

        # 创建配置
        config = recommendation.config
        config.title = title or config.title

        # 应用其他配置参数
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)

        # 根据图表库生成
        if library == ChartLibrary.MATPLOTLIB or config.library == ChartLibrary.MATPLOTLIB:
            filepath = self.matplotlib_generator.generate(data, config)
        else:
            filepath = self.plotly_generator.generate(data, config)

        return filepath, recommendation

    def recommend_chart(self, data: Union[Dict, List[Dict]]) -> List[ChartRecommendation]:
        """
        推荐图表类型

        Args:
            data: 数据

        Returns:
            推荐结果列表
        """
        return self.recommender.recommend(data)
