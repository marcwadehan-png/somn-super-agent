# -*- coding: utf-8 -*-
"""图表生成器 - 推荐器模块"""
import logging
import os
from typing import Dict, List, Optional, Union
import pandas as pd
import yaml
from ._cg_types import ChartType, ChartLibrary, ChartConfig, DataFeature, ChartRecommendation
from ._cg_analyzer import DataAnalyzer

__all__ = [
    'recommend',
]

logger = logging.getLogger(__name__)

class ChartRecommender:
    """图表类型推荐器 - 基于数据characteristics推荐最佳图表"""

    def __init__(self, knowledge_base_path: Optional[str] = None):
        self.rules = self._load_recommendation_rules(knowledge_base_path)

    def _load_recommendation_rules(self, path: Optional[str]) -> List[Dict]:
        """加载推荐规则"""
        if path and self._file_exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            return self._default_rules()

    def _default_rules(self) -> List[Dict]:
        """默认推荐规则"""
        return [
            {"pattern": "time_series", "chart_type": ChartType.LINE, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "时间序列数据使用折线图展示趋势"},
            {"pattern": "comparison", "chart_type": ChartType.BAR, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "比较多个类别使用柱状图"},
            {"pattern": "distribution", "chart_type": ChartType.BAR, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "分布数据使用柱状图或直方图"},
            {"pattern": "part_to_whole", "chart_type": ChartType.PIE, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "部分与整体关系使用饼图"},
            {"pattern": "correlation", "chart_type": ChartType.SCATTER, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "相关关系使用散点图"},
            {"pattern": "hierarchical", "chart_type": ChartType.TREEMAP, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "层次数据使用树状图"},
            {"pattern": "multi_series_time", "chart_type": ChartType.LINE, "library": ChartLibrary.PLOTLY, "priority": 2, "reason": "多系列时间数据使用折线图"},
            {"pattern": "ranked_data", "chart_type": ChartType.BAR, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "排名数据使用条形图"},
            {"pattern": "composition", "chart_type": ChartType.STACKED_BAR, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "组合数据使用堆叠柱状图"},
            {"pattern": "change_over_time", "chart_type": ChartType.AREA, "library": ChartLibrary.PLOTLY, "priority": 2, "reason": "随时间变化使用面积图"},
            {"pattern": "geographic", "chart_type": ChartType.MAP, "library": ChartLibrary.PLOTLY, "priority": 1, "reason": "地理数据使用地图"},
            {"pattern": "multivariate", "chart_type": ChartType.RADAR, "library": ChartLibrary.PLOTLY, "priority": 2, "reason": "多变量数据使用雷达图"},
        ]

    def _file_exists(self, path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(path)

    def recommend(self, data: Union[Dict, List[Dict], pd.DataFrame], user_preference: Optional[ChartType] = None) -> List[ChartRecommendation]:
        """推荐图表类型"""
        analyzer = DataAnalyzer()
        feature = analyzer.analyze_data(data)

        recommendations = []

        for rule in self.rules:
            if self._match_pattern(feature, rule["pattern"]):
                confidence = self._calculate_confidence(feature, rule)
                config = self._generate_config(feature, rule)

                recommendation = ChartRecommendation(
                    chart_type=rule["chart_type"],
                    confidence=confidence,
                    library=rule["library"],
                    reason=rule["reason"],
                    config=config
                )
                recommendations.append(recommendation)

        if user_preference:
            for rec in recommendations:
                if rec.chart_type == user_preference:
                    rec.confidence = min(1.0, rec.confidence + 0.2)

        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        return recommendations

    def _match_pattern(self, feature: DataFeature, pattern: str) -> bool:
        """匹配数据模式"""
        pattern_map = {
            "time_series": feature.has_time_series,
            "comparison": feature.is_comparison,
            "distribution": feature.is_distribution,
            "part_to_whole": feature.is_part_to_whole,
            "correlation": feature.is_correlation,
            "hierarchical": feature.is_hierarchical,
            "multi_series_time": feature.has_time_series and feature.is_comparison,
            "ranked_data": feature.is_categorical,
            "composition": feature.is_categorical and feature.is_comparison,
            "change_over_time": feature.has_time_series,
            "geographic": False,
            "multivariate": feature.variable_count > 2
        }
        return pattern_map.get(pattern, False)

    def _calculate_confidence(self, feature: DataFeature, rule: Dict) -> float:
        """计算置信度"""
        base_confidence = 0.75
        priority_factor = 1.0 if rule["priority"] == 1 else 0.85

        volume_factor = 1.0
        if feature.data_volume == "small":
            volume_factor = 0.95
        elif feature.data_volume == "large":
            volume_factor = 0.90

        quality_factor = 1.0
        if feature.missing_ratio > 0.3:
            quality_factor = 0.7
        elif feature.missing_ratio > 0.1:
            quality_factor = 0.9

        uniqueness_factor = 1.0
        if feature.unique_ratio < 0.5:
            uniqueness_factor = 0.95

        match_factor = self._calculate_match_factor(feature, rule["pattern"])

        confidence = base_confidence * priority_factor * volume_factor * quality_factor * uniqueness_factor * match_factor
        return min(1.0, confidence)

    def _calculate_match_factor(self, feature: DataFeature, pattern: str) -> float:
        """计算模式匹配度"""
        match_scores = {
            "time_series": 1.0 if feature.has_time_series else 0.0,
            "comparison": min(1.0, len(feature.numeric_columns) / 5),
            "distribution": 1.0 if (len(feature.numeric_columns) >= 1 and len(feature.categorical_columns) >= 1) else 0.6,
            "part_to_whole": 1.0 if feature.is_part_to_whole else 0.0,
            "correlation": min(1.0, len(feature.numeric_columns) / 4),
            "hierarchical": 1.0 if feature.is_hierarchical else 0.0,
            "multi_series_time": 1.0 if (feature.has_time_series and len(feature.numeric_columns) > 1) else 0.0,
            "ranked_data": 0.9 if feature.is_categorical else 0.7,
            "composition": 1.0 if (feature.is_categorical and len(feature.numeric_columns) > 1) else 0.6,
            "change_over_time": 0.9 if feature.has_time_series else 0.0,
            "geographic": 0.5,
            "multivariate": min(1.0, feature.variable_count / 5)
        }
        return match_scores.get(pattern, 0.7)

    def _generate_config(self, feature: DataFeature, rule: Dict) -> ChartConfig:
        """generate图表配置"""
        return ChartConfig(
            chart_type=rule["chart_type"],
            library=rule["library"],
            interactive=(rule["library"] == ChartLibrary.PLOTLY)
        )
