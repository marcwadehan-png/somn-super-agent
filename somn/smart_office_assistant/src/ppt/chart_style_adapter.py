"""
__all__ = [
    'adapt_style',
    'get_custom_style',
]

图表样式自适应模块 - 根据数据和主题自动调整图表样式
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ChartStyle:
    """图表样式配置"""
    color_palette: List[str]
    font_family: str
    font_size: int
    line_width: float
    marker_size: float
    background_color: str
    grid_color: str
    text_color: str
    show_legend: bool
    show_grid: bool
    hover_mode: str

class ChartStyleAdapter:
    """图表样式适配器"""

    def __init__(self, theme: str = "business"):
        """
        init样式适配器

        Args:
            theme: 主题 (business, tech, education, creative, minimal)
        """
        self.theme = theme
        self.style_themes = self._load_style_themes()

    def _load_style_themes(self) -> Dict[str, Dict]:
        """加载样式主题"""
        return {
            "business": {
                "color_palette": [
                    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
                ],
                "font_family": "Arial",
                "font_size": 12,
                "line_width": 2.5,
                "marker_size": 8,
                "background_color": "#ffffff",
                "grid_color": "#e0e0e0",
                "text_color": "#333333",
                "show_legend": True,
                "show_grid": True,
                "hover_mode": "closest"
            },
            "tech": {
                "color_palette": [
                    "#00d2ff", "#3a7bd5", "#00f260", "#0575e6",
                    "#f09819", "#edde5d", "#b92b27", "#1565C0"
                ],
                "font_family": "Helvetica",
                "font_size": 11,
                "line_width": 2,
                "marker_size": 6,
                "background_color": "#f8f9fa",
                "grid_color": "#dee2e6",
                "text_color": "#212529",
                "show_legend": True,
                "show_grid": True,
                "hover_mode": "x"
            },
            "education": {
                "color_palette": [
                    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A",
                    "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
                ],
                "font_family": "Verdana",
                "font_size": 13,
                "line_width": 3,
                "marker_size": 10,
                "background_color": "#ffffff",
                "grid_color": "#f0f0f0",
                "text_color": "#2c3e50",
                "show_legend": True,
                "show_grid": True,
                "hover_mode": "unified"
            },
            "creative": {
                "color_palette": [
                    "#FF6B6B", "#C44569", "#F8B500", "#FF6348",
                    "#7BED9F", "#70A1FF", "#5352ED", "#FF4757"
                ],
                "font_family": "Segoe UI",
                "font_size": 12,
                "line_width": 3,
                "marker_size": 9,
                "background_color": "#ffffff",
                "grid_color": "#f5f5f5",
                "text_color": "#333333",
                "show_legend": True,
                "show_grid": False,
                "hover_mode": "closest"
            },
            "minimal": {
                "color_palette": [
                    "#2d3436", "#636e72", "#b2bec3", "#dfe6e9",
                    "#00b894", "#00cec9", "#0984e3", "#6c5ce7"
                ],
                "font_family": "Inter",
                "font_size": 11,
                "line_width": 1.5,
                "marker_size": 5,
                "background_color": "#ffffff",
                "grid_color": "#e8e8e8",
                "text_color": "#2d3436",
                "show_legend": False,
                "show_grid": True,
                "hover_mode": "x"
            },
            "financial": {
                "color_palette": [
                    "#e74c3c", "#27ae60", "#f39c12", "#3498db",
                    "#9b59b6", "#1abc9c", "#e67e22", "#34495e"
                ],
                "font_family": "Arial",
                "font_size": 11,
                "line_width": 2,
                "marker_size": 6,
                "background_color": "#ffffff",
                "grid_color": "#ecf0f1",
                "text_color": "#2c3e50",
                "show_legend": True,
                "show_grid": True,
                "hover_mode": "closest"
            }
        }

    def adapt_style(
        self,
        chart_type: str,
        data_size: int,
        theme: Optional[str] = None
    ) -> ChartStyle:
        """
        自适应调整图表样式

        Args:
            chart_type: 图表类型
            data_size: 数据量大小
            theme: 主题(可选,覆盖默认主题)

        Returns:
            图表样式配置
        """
        # 使用指定主题或默认主题
        selected_theme = theme or self.theme
        theme_config = self.style_themes.get(selected_theme, self.style_themes["business"])

        # 根据图表类型和数据量调整样式
        adapted_style = ChartStyle(
            color_palette=self._adapt_color_palette(theme_config["color_palette"], data_size, chart_type),
            font_family=theme_config["font_family"],
            font_size=self._adapt_font_size(theme_config["font_size"], data_size),
            line_width=self._adapt_line_width(theme_config["line_width"], chart_type),
            marker_size=self._adapt_marker_size(theme_config["marker_size"], data_size),
            background_color=theme_config["background_color"],
            grid_color=theme_config["grid_color"],
            text_color=theme_config["text_color"],
            show_legend=self._adapt_legend(theme_config["show_legend"], data_size),
            show_grid=self._adapt_grid(theme_config["show_grid"], chart_type),
            hover_mode=theme_config["hover_mode"]
        )

        logger.debug(f"样式自适应完成: {chart_type}, 主题: {selected_theme}")
        return adapted_style

    def _adapt_color_palette(
        self,
        base_palette: List[str],
        data_size: int,
        chart_type: str
    ) -> List[str]:
        """自适应调整颜色配置"""
        # 对于饼图,通常使用不同颜色
        if chart_type in ["pie", "sunburst", "treemap"]:
            if data_size > len(base_palette):
                # 循环扩展颜色
                return base_palette * (data_size // len(base_palette) + 1)
            return base_palette[:data_size]

        # 对于其他图表,根据数据系列数量调整
        elif chart_type in ["line", "bar", "scatter"]:
            if data_size > len(base_palette):
                # 使用插值generate更多颜色
                return self._generate_color_gradient(base_palette, data_size)
            return base_palette[:data_size]

        # 默认返回基础调色板
        return base_palette

    def _generate_color_gradient(
        self,
        base_palette: List[str],
        size: int
    ) -> List[str]:
        """generate颜色渐变"""
        # 简单实现:循环基础颜色
        return (base_palette * ((size // len(base_palette)) + 1))[:size]

    def _adapt_font_size(self, base_size: int, data_size: int) -> int:
        """自适应调整字体大小"""
        # 数据量大时减小字体
        if data_size > 50:
            return max(base_size - 2, 8)
        elif data_size > 20:
            return base_size - 1
        return base_size

    def _adapt_line_width(self, base_width: float, chart_type: str) -> float:
        """自适应调整线宽"""
        # 某些图表类型使用更细的线
        if chart_type in ["line", "area"]:
            return base_width
        elif chart_type in ["scatter"]:
            return base_width * 0.8
        return base_width

    def _adapt_marker_size(self, base_size: float, data_size: int) -> float:
        """自适应调整标记大小"""
        # 数据量大时减小标记
        if data_size > 100:
            return base_size * 0.6
        elif data_size > 50:
            return base_size * 0.8
        return base_size

    def _adapt_legend(self, base_show: bool, data_size: int) -> bool:
        """自适应调整图例显示"""
        # 数据项过多时隐藏图例
        if data_size > 15:
            return False
        return base_show

    def _adapt_grid(self, base_show: bool, chart_type: str) -> bool:
        """自适应调整网格显示"""
        # 某些图表类型默认不显示网格
        if chart_type in ["pie", "sunburst", "treemap", "funnel"]:
            return False
        return base_show

    def get_custom_style(
        self,
        custom_config: Dict[str, Any]
    ) -> ChartStyle:
        """
        get自定义样式

        Args:
            custom_config: 自定义配置字典

        Returns:
            图表样式配置
        """
        base_theme = self.style_themes.get(self.theme, self.style_themes["business"])

        return ChartStyle(
            color_palette=custom_config.get("color_palette", base_theme["color_palette"]),
            font_family=custom_config.get("font_family", base_theme["font_family"]),
            font_size=custom_config.get("font_size", base_theme["font_size"]),
            line_width=custom_config.get("line_width", base_theme["line_width"]),
            marker_size=custom_config.get("marker_size", base_theme["marker_size"]),
            background_color=custom_config.get("background_color", base_theme["background_color"]),
            grid_color=custom_config.get("grid_color", base_theme["grid_color"]),
            text_color=custom_config.get("text_color", base_theme["text_color"]),
            show_legend=custom_config.get("show_legend", base_theme["show_legend"]),
            show_grid=custom_config.get("show_grid", base_theme["show_grid"]),
            hover_mode=custom_config.get("hover_mode", base_theme["hover_mode"])
        )
