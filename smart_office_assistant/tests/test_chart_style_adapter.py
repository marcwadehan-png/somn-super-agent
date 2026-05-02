"""
图表样式适配器单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

import pytest
from ppt.chart_style_adapter import ChartStyleAdapter, ChartStyle



class TestChartStyleAdapter:
    """图表样式适配器测试"""

    def test_business_theme(self):
        """测试商务主题"""
        adapter = ChartStyleAdapter(theme="business")
        style = adapter.adapt_style("bar", 10)

        assert style.font_family == "Arial"
        assert style.show_legend is True
        assert style.show_grid is True
        assert len(style.color_palette) > 0

    def test_tech_theme(self):
        """测试科技主题"""
        adapter = ChartStyleAdapter(theme="tech")
        style = adapter.adapt_style("line", 20)

        assert style.font_family == "Helvetica"
        assert style.show_legend is True
        assert style.background_color == "#f8f9fa"

    def test_education_theme(self):
        """测试教育主题"""
        adapter = ChartStyleAdapter(theme="education")
        style = adapter.adapt_style("pie", 5)

        assert style.font_family == "Verdana"
        assert style.font_size == 13
        assert style.show_grid is True

    def test_creative_theme(self):
        """测试创意主题"""
        adapter = ChartStyleAdapter(theme="creative")
        style = adapter.adapt_style("scatter", 15)

        assert style.font_family == "Segoe UI"
        assert style.show_grid is False
        assert style.line_width == 3

    def test_minimal_theme(self):
        """测试极简主题"""
        adapter = ChartStyleAdapter(theme="minimal")
        style = adapter.adapt_style("line", 10)

        assert style.font_family == "Inter"
        assert style.show_legend is False
        assert style.line_width == 1.5

    def test_font_size_adaptation(self):
        """测试字体大小自适应"""
        adapter = ChartStyleAdapter(theme="business")

        # 小数据集
        style_small = adapter.adapt_style("bar", 10)
        # 大数据集
        style_large = adapter.adapt_style("bar", 60)

        assert style_large.font_size <= style_small.font_size

    def test_marker_size_adaptation(self):
        """测试标记大小自适应"""
        adapter = ChartStyleAdapter(theme="business")

        # 小数据集
        style_small = adapter.adapt_style("scatter", 30)
        # 大数据集
        style_large = adapter.adapt_style("scatter", 120)

        assert style_large.marker_size < style_small.marker_size

    def test_legend_adaptation(self):
        """测试图例自适应"""
        adapter = ChartStyleAdapter(theme="business")

        # 少量数据
        style_few = adapter.adapt_style("pie", 5)
        # 大量数据
        style_many = adapter.adapt_style("pie", 20)

        # 大量数据时应该隐藏图例
        assert style_many.show_legend is False

    def test_grid_adaptation(self):
        """测试网格自适应"""
        adapter = ChartStyleAdapter(theme="business")

        # 饼图不显示网格
        style_pie = adapter.adapt_style("pie", 5)
        assert style_pie.show_grid is False

        # 柱状图显示网格
        style_bar = adapter.adapt_style("bar", 5)
        assert style_bar.show_grid is True

    def test_color_palette_expansion(self):
        """测试颜色调色板扩展"""
        adapter = ChartStyleAdapter(theme="business")

        # 请求数量多于基础调色板
        style = adapter.adapt_style("pie", 20)

        assert len(style.color_palette) >= 20

    def test_custom_style(self):
        """测试自定义样式"""
        adapter = ChartStyleAdapter(theme="business")

        custom_config = {
            "font_family": "CustomFont",
            "font_size": 16,
            "line_width": 4.0,
            "background_color": "#ffffff",
            "color_palette": ["#FF0000", "#00FF00", "#0000FF"]
        }

        style = adapter.get_custom_style(custom_config)

        assert style.font_family == "CustomFont"
        assert style.font_size == 16
        assert style.line_width == 4.0
        assert style.color_palette == ["#FF0000", "#00FF00", "#0000FF"]

    def test_invalid_theme(self):
        """测试无效主题"""
        adapter = ChartStyleAdapter(theme="invalid")

        # 应该回退到默认商务主题
        style = adapter.adapt_style("bar", 10)

        assert style is not None
        assert style.font_family == "Arial"  # 商务主题的默认字体

    def test_line_width_adaptation(self):
        """测试线宽自适应"""
        adapter = ChartStyleAdapter(theme="business")

        style_line = adapter.adapt_style("line", 10)
        style_scatter = adapter.adapt_style("scatter", 10)

        # 散点图的线宽应该更细
        assert style_scatter.line_width < style_line.line_width


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
