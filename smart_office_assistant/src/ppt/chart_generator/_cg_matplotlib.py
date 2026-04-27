# -*- coding: utf-8 -*-
"""图表生成器 - Matplotlib生成器模块"""
import os
import logging
from typing import Union
import pandas as pd
from ._cg_types import ChartConfig, ChartType

__all__ = [
    'generate',
]

logger = logging.getLogger(__name__)

class MatplotlibChartGenerator:
    """Matplotlib图表generate器"""

    def __init__(self):
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            self.plt = plt
            self.sns = sns
            self.available = True
        except ImportError:
            logger.warning("Matplotlib未安装")
            self.available = False

    def generate(self, data: Union[dict, list, pd.DataFrame], config: ChartConfig) -> str:
        """generate图表"""
        if not self.available:
            raise ImportError("Matplotlib未安装,请先安装: pip install matplotlib")

        df = self._to_dataframe(data)
        self.sns.set_theme(style="whitegrid")

        if config.chart_type == ChartType.BAR:
            return self._generate_bar(df, config)
        elif config.chart_type == ChartType.LINE:
            return self._generate_line(df, config)
        elif config.chart_type == ChartType.PIE:
            return self._generate_pie(df, config)
        elif config.chart_type == ChartType.SCATTER:
            return self._generate_scatter(df, config)
        else:
            raise ValueError(f"不支持的图表类型: {config.chart_type}")

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
        fig, ax = self.plt.subplots(figsize=(config.width / 100, config.height / 100))

        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1]

        ax.bar(df[x_col], df[y_col])
        ax.set_title(config.title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

        return self._save_chart(fig, config)

    def _generate_line(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate折线图"""
        fig, ax = self.plt.subplots(figsize=(config.width / 100, config.height / 100))

        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1]

        ax.plot(df[x_col], df[y_col])
        ax.set_title(config.title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

        return self._save_chart(fig, config)

    def _generate_pie(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate饼图"""
        fig, ax = self.plt.subplots(figsize=(config.width / 100, config.height / 100))

        names_col = config.x_column or df.columns[0]
        values_col = config.y_column or df.columns[1]

        ax.pie(df[values_col], labels=df[names_col], autopct='%1.1f%%')
        ax.set_title(config.title)

        return self._save_chart(fig, config)

    def _generate_scatter(self, df: pd.DataFrame, config: ChartConfig) -> str:
        """generate散点图"""
        fig, ax = self.plt.subplots(figsize=(config.width / 100, config.height / 100))

        x_col = config.x_column or df.columns[0]
        y_col = config.y_column or df.columns[1]

        ax.scatter(df[x_col], df[y_col])
        ax.set_title(config.title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

        return self._save_chart(fig, config)

    def _save_chart(self, fig, config: ChartConfig) -> str:
        """保存图表"""
        output_dir = "outputs/charts"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"chart_{config.chart_type.value}_{hash(str(fig))}.png"
        filepath = os.path.join(output_dir, filename)

        fig.savefig(filepath, dpi=100 * config.scale, bbox_inches='tight')
        self.plt.close(fig)

        logger.info(f"图表已保存: {filepath}")
        return filepath
