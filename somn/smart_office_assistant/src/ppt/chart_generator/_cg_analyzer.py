# -*- coding: utf-8 -*-
"""图表生成器 - 数据分析模块"""
import traceback
import logging
from typing import Union, Dict, List
import pandas as pd
from ._cg_types import DataFeature

__all__ = [
    'analyze_data',
]

logger = logging.getLogger(__name__)

class DataAnalyzer:
    """数据分析器 - 提取数据characteristics"""

    @staticmethod
    def analyze_data(data: Union[Dict, List[Dict], pd.DataFrame]) -> DataFeature:
        """
        分析数据characteristics

        Args:
            data: 数据(字典,列表或DataFrame)

        Returns:
            数据characteristics对象
        """
        try:
            if isinstance(data, pd.DataFrame):
                df = data.copy()
            elif isinstance(data, dict):
                df = pd.DataFrame(data)
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                raise ValueError(f"不支持的数据类型: {type(data)}")
        except Exception as e:
            logger.error(f"数据转换失败: {e}\n{traceback.format_exc()}")
            raise ValueError(f"数据转换失败: {e}") from e

        feature = DataFeature()
        feature.observation_count = len(df)
        feature.variable_count = len(df.columns)

        # judge数据量
        if len(df) < 30:
            feature.data_volume = "small"
        elif len(df) < 500:
            feature.data_volume = "medium"
        else:
            feature.data_volume = "large"

        # 分析每列类型
        time_columns = []
        numeric_columns = []
        categorical_columns = []

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                time_columns.append(col)
                feature.has_time_series = True
            elif df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col])
                    time_columns.append(col)
                    feature.has_time_series = True
                except Exception:
                    if df[col].nunique() < min(20, len(df) * 0.3):
                        categorical_columns.append(col)
                        feature.is_categorical = True
            elif pd.api.types.is_numeric_dtype(df[col]):
                numeric_columns.append(col)
                feature.is_numerical = True

        feature.time_columns = time_columns
        feature.numeric_columns = numeric_columns
        feature.categorical_columns = categorical_columns

        # 检测比较关系
        if len(numeric_columns) > 1:
            feature.is_comparison = True

        # 检测分布关系
        if len(numeric_columns) >= 1 and len(categorical_columns) >= 1:
            feature.is_distribution = True

        # 检测部分与整体关系
        if len(numeric_columns) >= 1 and len(categorical_columns) >= 1 and len(df) <= 15:
            feature.is_part_to_whole = True

        # 检测相关关系
        if len(numeric_columns) >= 2:
            feature.is_correlation = True

        # 检测层次关系
        if len(categorical_columns) >= 2:
            feature.is_hierarchical = True

        # 计算数据质量metrics
        feature.missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        feature.unique_ratio = df.nunique().sum() / (len(df) * len(df.columns))

        logger.debug(f"数据characteristics分析完成: {feature}")
        return feature
