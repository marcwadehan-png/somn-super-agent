"""
图表生成器单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

import pytest
import pandas as pd
import numpy as np
from ppt.chart_generator import (

    ChartGenerator, ChartType, ChartLibrary,
    DataAnalyzer, ChartRecommender, DataFeature
)


class TestDataAnalyzer:
    """数据分析器测试"""

    def test_analyze_time_series_data(self):
        """测试时间序列数据分析"""
        data = {
            "date": pd.date_range("2024-01-01", periods=12, freq="M"),
            "value": [100, 120, 150, 180, 200, 220, 240, 260, 280, 300, 320, 340]
        }
        feature = DataAnalyzer.analyze_data(data)

        assert feature.has_time_series is True
        assert feature.is_numerical is True
        assert feature.observation_count == 12

    def test_analyze_categorical_data(self):
        """测试分类数据分析"""
        data = {
            "category": ["A", "B", "C", "D", "E"],
            "value": [10, 20, 30, 40, 50]
        }
        feature = DataAnalyzer.analyze_data(data)

        assert feature.is_categorical is True
        assert feature.is_part_to_whole is True
        assert len(feature.categorical_columns) > 0

    def test_analyze_comparison_data(self):
        """测试比较数据分析"""
        data = {
            "category": ["A", "B", "C", "D", "E"],
            "value1": [10, 20, 30, 40, 50],
            "value2": [15, 25, 35, 45, 55],
            "value3": [20, 30, 40, 50, 60]
        }
        feature = DataAnalyzer.analyze_data(data)

        assert feature.is_comparison is True
        assert len(feature.numeric_columns) > 1

    def test_analyze_correlation_data(self):
        """测试相关性数据分析"""
        np.random.seed(42)
        data = {
            "x": np.random.randn(100),
            "y": np.random.randn(100),
            "z": np.random.randn(100)
        }
        feature = DataAnalyzer.analyze_data(data)

        assert feature.is_correlation is True
        assert len(feature.numeric_columns) >= 2

    def test_data_volume_classification(self):
        """测试数据量分类"""
        # 小数据集
        small_data = {"value": list(range(20))}
        small_feature = DataAnalyzer.analyze_data(small_data)
        assert small_feature.data_volume == "small"

        # 中等数据集
        medium_data = {"value": list(range(100))}
        medium_feature = DataAnalyzer.analyze_data(medium_data)
        assert medium_feature.data_volume == "medium"

        # 大数据集
        large_data = {"value": list(range(600))}
        large_feature = DataAnalyzer.analyze_data(large_data)
        assert large_feature.data_volume == "large"


class TestChartRecommender:
    """图表推荐器测试"""

    def test_time_series_recommendation(self):
        """测试时间序列推荐"""
        data = {
            "date": pd.date_range("2024-01-01", periods=12, freq="M"),
            "value": list(range(12))
        }
        recommender = ChartRecommender()
        recommendations = recommender.recommend(data)

        assert len(recommendations) > 0
        assert recommendations[0].confidence > 0.7
        # 时间序列应该推荐折线图
        assert ChartType.LINE in [r.chart_type for r in recommendations]

    def test_comparison_recommendation(self):
        """测试比较推荐"""
        data = {
            "category": ["A", "B", "C", "D"],
            "value1": [10, 20, 30, 40],
            "value2": [15, 25, 35, 45]
        }
        recommender = ChartRecommender()
        recommendations = recommender.recommend(data)

        assert len(recommendations) > 0
        # 比较数据应该推荐柱状图或分组柱状图
        chart_types = [r.chart_type for r in recommendations]
        assert ChartType.BAR in chart_types or ChartType.GROUPED_BAR in chart_types

    def test_part_to_whole_recommendation(self):
        """测试部分与整体推荐"""
        data = {
            "category": ["A", "B", "C", "D", "E"],
            "value": [10, 20, 30, 40, 50]
        }
        recommender = ChartRecommender()
        recommendations = recommender.recommend(data)

        # 部分与整体应该推荐饼图
        chart_types = [r.chart_type for r in recommendations]
        assert ChartType.PIE in chart_types

    def test_confidence_calculation(self):
        """测试置信度计算"""
        data = {
            "category": ["A", "B", "C"],
            "value": [10, 20, 30]
        }
        recommender = ChartRecommender()
        recommendations = recommender.recommend(data)

        for rec in recommendations:
            assert 0 <= rec.confidence <= 1
            assert rec.reason is not None
            assert rec.config is not None

    def test_user_preference_influence(self):
        """测试用户偏好影响"""
        data = {
            "date": pd.date_range("2024-01-01", periods=6, freq="M"),
            "value": list(range(6))
        }
        recommender = ChartRecommender()
        
        # 不带偏好
        recommendations1 = recommender.recommend(data)
        
        # 带偏好
        recommendations2 = recommender.recommend(data, user_preference=ChartType.BAR)
        
        # 带偏好的BAR图置信度应该更高
        bar_rec1 = next((r for r in recommendations1 if r.chart_type == ChartType.BAR), None)
        bar_rec2 = next((r for r in recommendations2 if r.chart_type == ChartType.BAR), None)
        
        if bar_rec1 and bar_rec2:
            assert bar_rec2.confidence >= bar_rec1.confidence


class TestChartGenerator:
    """图表生成器测试"""

    @pytest.mark.skip(reason="需要安装plotly")
    def test_basic_chart_generation(self):
        """测试基本图表生成"""
        generator = ChartGenerator()
        data = {
            "x": ["A", "B", "C", "D"],
            "y": [10, 20, 30, 40]
        }

        filepath, recommendation = generator.generate_chart(
            data=data,
            title="测试图表"
        )

        assert filepath is not None
        assert recommendation is not None
        assert recommendation.confidence > 0

    @pytest.mark.skip(reason="需要安装plotly")
    def test_chart_type_specification(self):
        """测试指定图表类型"""
        generator = ChartGenerator()
        data = {
            "x": ["A", "B", "C"],
            "y": [10, 20, 30]
        }

        filepath, recommendation = generator.generate_chart(
            data=data,
            chart_type=ChartType.PIE,
            title="饼图"
        )

        assert recommendation.chart_type == ChartType.PIE

    @pytest.mark.skip(reason="需要安装plotly")
    def test_library_selection(self):
        """测试图表库选择"""
        generator = ChartGenerator(preferred_library=ChartLibrary.PLOTLY)
        data = {
            "x": ["A", "B", "C"],
            "y": [10, 20, 30]
        }

        filepath, recommendation = generator.generate_chart(
            data=data,
            library=ChartLibrary.PLOTLY,
            title="Plotly图表"
        )

        assert recommendation.library == ChartLibrary.PLOTLY


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
