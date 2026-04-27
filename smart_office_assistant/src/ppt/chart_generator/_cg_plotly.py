# -*- coding: utf-8 -*-
"""图表生成器 - Plotly生成器模块"""
import os
import time
import logging
from typing import Union
import pandas as pd
from ._cg_types import ChartConfig, ChartType

__all__ = [
    'generate',
]

logger = logging.getLogger(__name__)

class PlotlyChartGenerator:
    """Plotly图表generate器"""

    def __init__(self):
        try:
            import plotly.graph_objects as go
            import plotly.express as px
            self.go = go
            self.px = px
            self.available = True
        except ImportError:
            logger.warning("Plotly未安装,使用Matplotlib作为备选")
            self.available = False

    def generate(self, data: Union[dict, list, pd.DataFrame], config: ChartConfig) -> str:
        """generate图表"""
        if not self.available:
            raise ImportError("Plotly未安装,请先安装: pip install plotly")

        df = self._to_dataframe(data)

        try:
            if config.chart_type == ChartType.BAR:
                return self._generate_bar(df, config)
            elif config.chart_type == ChartType.COLUMN:
                return self._generate_column(df, config)
            elif config.chart_type == ChartType.LINE:
                return self._generate_line(df, config)
            elif config.chart_type == ChartType.PIE:
                return self._generate_pie(df, config)
            elif config.chart_type == ChartType.SCATTER:
                return self._generate_scatter(df, config)
            elif config.chart_type == ChartType.AREA:
                return self._generate_area(df, config)
            elif config.chart_type == ChartType.STACKED_BAR:
                return self._generate_stacked_bar(df, config)
            elif config.chart_type == ChartType.GROUPED_BAR:
                return self._generate_grouped_bar(df, config)
            elif config.chart_type == ChartType.DUAL_AXIS:
                return self._generate_dual_axis(df, config)
            elif config.chart_type == ChartType.HEATMAP:
                return self._generate_heatmap(df, config)
            elif config.chart_type == ChartType.TREEMAP:
                return self._generate_treemap(df, config)
            elif config.chart_type == ChartType.SUNBURST:
                return self._generate_sunburst(df, config)
            elif config.chart_type == ChartType.FUNNEL:
                return self._generate_funnel(df, config)
            elif config.chart_type == ChartType.GAUGE:
                return self._generate_gauge(df, config)
            elif config.chart_type == ChartType.RADAR:
                return self._generate_radar(df, config)
            else:
                logger.warning(f"暂不支持的图表类型: {config.chart_type},使用柱状图代替")
                return self._generate_bar(df, config)
        except Exception as e:
            logger.error(f"generate图表失败: {e}")
            raise

    def _to_dataframe(self, data: Union[dict, list, pd.DataFrame]) -> pd.DataFrame:
        """转换为DataFrame"""
        if isinstance(data, pd.DataFrame):
            return data
        elif isinstance(data, dict):
            return pd.DataFrame(data)
        elif isinstance(data, list):
            return pd.DataFrame(data)
        else:
            raise ValueError(f"不支持的数据类型: {type(data)}")

    def _generate_bar(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate柱状图"""
        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]

        fig = self.px.bar(df, x=x_col, y=y_col, color=config.color_column, title=config.title,
                          width=config.width, height=config.height, text_auto=True)

        fig.update_traces(hovertemplate='<b>%{x}</b><br>%{y:,.2f}<extra></extra>')

        if config.show_grid:
            fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='rgba(0,0,0,0)')

        return self._save_chart(fig, config)

    def _generate_column(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate条形图"""
        y_col = config.x_column or df.columns[0]
        x_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]

        fig = self.px.bar(df, x=x_col, y=y_col, orientation='h', color=config.color_column,
                          title=config.title, width=config.width, height=config.height, text_auto=True)

        if config.show_grid:
            fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='rgba(0,0,0,0)')

        return self._save_chart(fig, config)

    def _generate_line(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate折线图"""
        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1]

        fig = self.px.line(df, x=x_col, y=y_col, color=config.color_column,
                          title=config.title, width=config.width, height=config.height)

        return self._save_chart(fig, config)

    def _generate_pie(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate饼图"""
        names_col = config.x_column or df.columns[0]
        values_col = config.y_column or df.columns[1]

        fig = self.px.pie(df, names=names_col, values=values_col, title=config.title,
                         width=config.width, height=config.height)

        return self._save_chart(fig, config)

    def _generate_scatter(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate散点图"""
        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]

        fig = self.px.scatter(df, x=x_col, y=y_col, color=config.color_column, size=config.size_column,
                             title=config.title, width=config.width, height=config.height,
                             trendline="ols" if len(df) > 2 else None)

        return self._save_chart(fig, config)

    def _generate_area(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate面积图"""
        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]

        fig = self.px.area(df, x=x_col, y=y_col, color=config.color_column,
                          title=config.title, width=config.width, height=config.height)

        return self._save_chart(fig, config)

    def _generate_stacked_bar(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate堆叠柱状图"""
        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]
        color_col = config.color_column or (df.columns[2] if len(df.columns) > 2 else None)

        fig = self.px.bar(df, x=x_col, y=y_col, color=color_col, title=config.title,
                         width=config.width, height=config.height, text_auto=True)
        fig.update_layout(barmode='stack')

        return self._save_chart(fig, config)

    def _generate_grouped_bar(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate分组柱状图"""
        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]
        color_col = config.color_column or (df.columns[2] if len(df.columns) > 2 else None)

        fig = self.px.bar(df, x=x_col, y=y_col, color=color_col, title=config.title,
                         width=config.width, height=config.height, text_auto=True, barmode='group')

        return self._save_chart(fig, config)

    def _generate_dual_axis(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate双轴图"""
        from plotly.subplots import make_subplots

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        x_col = config.x_column or df.columns[0]
        y1_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]
        y2_col = df.columns[2] if len(df.columns) > 2 else df.columns[1]

        fig.add_trace(self.go.Scatter(x=df[x_col], y=df[y1_col], name=y1_col, mode='lines+markers'), secondary_y=False)
        fig.add_trace(self.go.Bar(x=df[x_col], y=df[y2_col], name=y2_col), secondary_y=True)

        fig.update_xaxes(title_text=x_col)
        fig.update_yaxes(title_text=y1_col, secondary_y=False)
        fig.update_yaxes(title_text=y2_col, secondary_y=True)

        fig.update_layout(title=config.title, width=config.width, height=config.height)

        return self._save_chart(fig, config)

    def _generate_heatmap(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate热力图"""
        fig = self.px.imshow(df, title=config.title, width=config.width, height=config.height)
        return self._save_chart(fig, config)

    def _generate_treemap(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate树状图"""
        names_col = config.x_column or df.columns[0]
        values_col = config.y_column or df.columns[1]

        fig = self.px.treemap(df, path=[names_col], values=values_col,
                             title=config.title, width=config.width, height=config.height)

        return self._save_chart(fig, config)

    def _generate_sunburst(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate旭日图"""
        names_col = config.x_column or df.columns[0]
        values_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]
        parent_col = getattr(config, 'parent_column', None) or (df.columns[2] if len(df.columns) > 2 else None)

        if parent_col:
            fig = self.px.sunburst(df, names=names_col, values=values_col, parents=df[parent_col],
                                  title=config.title, width=config.width, height=config.height)
        else:
            fig = self.px.sunburst(df, names=names_col, values=values_col,
                                  title=config.title, width=config.width, height=config.height)

        return self._save_chart(fig, config)

    def _generate_funnel(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate漏斗图"""
        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]

        fig = self.px.funnel(df, x=y_col, y=x_col, title=config.title,
                            width=config.width, height=config.height)

        return self._save_chart(fig, config)

    def _generate_gauge(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate仪表盘"""
        y_col = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]
        value = df[y_col].iloc[-1] if len(df) > 0 else 0
        max_val = df[y_col].max() if len(df) > 0 else 100

        fig = self.go.Figure(self.go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': config.title},
            gauge={
                'axis': {'range': [None, max_val]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, max_val * 0.33], 'color': "lightgray"},
                    {'range': [max_val * 0.33, max_val * 0.66], 'color': "gray"},
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_val * 0.9}
            }
        ))

        fig.update_layout(width=config.width, height=config.height)
        return self._save_chart(fig, config)

    def _generate_radar(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate雷达图"""
        categories = config.x_column or df.columns[0]
        values = config.y_column or df.columns[1] if len(df.columns) > 1 else df.columns[0]

        fig = self.go.Figure()
        fig.add_trace(self.go.Scatterpolar(r=df[values], theta=df[categories], fill='toself', name=config.title))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title=config.title,
            width=config.width,
            height=config.height
        )

        return self._save_chart(fig, config)

    def _save_chart(self, fig, config: ChartConfig) -> str:
        """保存图表"""
        output_dir = "outputs/charts"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = int(time.time() * 1000)
        safe_title = config.title.replace(' ', '_').replace('/', '_')[:50] if config.title else 'chart'
        filename = f"{safe_title}_{config.chart_type.value}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)

        try:
            try:
                fig.write_image(filepath, scale=config.scale, engine="kaleido")
            except Exception as e:
                logger.warning(f"Kaleido引擎失败: {e},尝试备用方法")
                try:
                    fig.write_image(filepath, scale=config.scale)
                except Exception as e2:
                    logger.error(f"PNG保存失败: {e2}")
                    html_filepath = filepath.replace('.png', '.html')
                    try:
                        fig.write_html(html_filepath)
                        logger.warning(f"已保存为HTML格式: {html_filepath}")
                        filepath = html_filepath
                    except Exception as e3:
                        logger.error(f"HTML保存也失败: {e3}")
                        raise RuntimeError(f"图表保存失败: {e3}") from e3

            logger.info(f"图表已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"图表保存过程出错: {e}")
            raise
