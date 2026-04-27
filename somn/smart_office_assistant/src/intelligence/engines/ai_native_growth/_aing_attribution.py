# -*- coding: utf-8 -*-
"""归因分析器 - AttributionAnalyzer类

__all__ = [
    'analyze',
]

支持多种归因模型:
- first_touch: 首次接触归因
- last_touch: 末次接触归因
- linear: 线性归因
- time_decay: 时间衰减归因
- data_driven: 数据驱动归因
"""

import logging
from typing import Dict, List, Callable

from ._aing_enums import AttributionResult

logger = logging.getLogger(__name__)

class AttributionAnalyzer:
    """归因分析器"""
    
    def __init__(self):
        self.attribution_models: Dict[str, Callable] = {
            "first_touch": self._first_touch_attribution,
            "last_touch": self._last_touch_attribution,
            "linear": self._linear_attribution,
            "time_decay": self._time_decay_attribution,
            "data_driven": self._data_driven_attribution
        }
    
    def analyze(
        self,
        customer_journeys: List[List[Dict]],
        conversions: List[Dict],
        model: str = "data_driven"
    ) -> List[AttributionResult]:
        """执行归因分析"""
        if model not in self.attribution_models:
            model = "last_touch"
        
        return self.attribution_models[model](customer_journeys, conversions)
    
    def _first_touch_attribution(
        self,
        journeys: List[List[Dict]],
        conversions: List[Dict]
    ) -> List[AttributionResult]:
        """首次接触归因"""
        touchpoint_counts: Dict[str, int] = {}
        touchpoint_revenue: Dict[str, float] = {}
        
        for journey, conversion in zip(journeys, conversions):
            if journey and conversion:
                first_touch = journey[0].get("channel", "unknown")
                touchpoint_counts[first_touch] = touchpoint_counts.get(first_touch, 0) + 1
                touchpoint_revenue[first_touch] = touchpoint_revenue.get(first_touch, 0) + conversion.get("revenue", 0)
        
        total_conversions = sum(touchpoint_counts.values())
        
        return [
            AttributionResult(
                touchpoint=tp,
                attributed_conversions=count,
                attributed_revenue=touchpoint_revenue.get(tp, 0),
                attribution_percentage=count / total_conversions * 100 if total_conversions > 0 else 0,
                model_type="first_touch"
            )
            for tp, count in touchpoint_counts.items()
        ]
    
    def _last_touch_attribution(
        self,
        journeys: List[List[Dict]],
        conversions: List[Dict]
    ) -> List[AttributionResult]:
        """末次接触归因"""
        touchpoint_counts: Dict[str, int] = {}
        touchpoint_revenue: Dict[str, float] = {}
        
        for journey, conversion in zip(journeys, conversions):
            if journey and conversion:
                last_touch = journey[-1].get("channel", "unknown")
                touchpoint_counts[last_touch] = touchpoint_counts.get(last_touch, 0) + 1
                touchpoint_revenue[last_touch] = touchpoint_revenue.get(last_touch, 0) + conversion.get("revenue", 0)
        
        total_conversions = sum(touchpoint_counts.values())
        
        return [
            AttributionResult(
                touchpoint=tp,
                attributed_conversions=count,
                attributed_revenue=touchpoint_revenue.get(tp, 0),
                attribution_percentage=count / total_conversions * 100 if total_conversions > 0 else 0,
                model_type="last_touch"
            )
            for tp, count in touchpoint_counts.items()
        ]
    
    def _linear_attribution(
        self,
        journeys: List[List[Dict]],
        conversions: List[Dict]
    ) -> List[AttributionResult]:
        """线性归因(平均分配)"""
        touchpoint_counts: Dict[str, float] = {}
        touchpoint_revenue: Dict[str, float] = {}
        
        for journey, conversion in zip(journeys, conversions):
            if journey and conversion:
                weight = 1.0 / len(journey)
                revenue_share = conversion.get("revenue", 0) * weight
                
                for touchpoint in journey:
                    channel = touchpoint.get("channel", "unknown")
                    touchpoint_counts[channel] = touchpoint_counts.get(channel, 0) + weight
                    touchpoint_revenue[channel] = touchpoint_revenue.get(channel, 0) + revenue_share
        
        total = sum(touchpoint_counts.values())
        
        return [
            AttributionResult(
                touchpoint=tp,
                attributed_conversions=int(count),
                attributed_revenue=touchpoint_revenue.get(tp, 0),
                attribution_percentage=count / total * 100 if total > 0 else 0,
                model_type="linear"
            )
            for tp, count in touchpoint_counts.items()
        ]
    
    def _time_decay_attribution(
        self,
        journeys: List[List[Dict]],
        conversions: List[Dict]
    ) -> List[AttributionResult]:
        """时间衰减归因"""
        touchpoint_counts: Dict[str, float] = {}
        touchpoint_revenue: Dict[str, float] = {}
        
        for journey, conversion in zip(journeys, conversions):
            if journey and conversion:
                # 越近的接触点权重越高
                n = len(journey)
                total_weight = sum(2 ** i for i in range(n))
                
                for i, touchpoint in enumerate(journey):
                    channel = touchpoint.get("channel", "unknown")
                    weight = (2 ** i) / total_weight
                    
                    touchpoint_counts[channel] = touchpoint_counts.get(channel, 0) + weight
                    touchpoint_revenue[channel] = touchpoint_revenue.get(channel, 0) + conversion.get("revenue", 0) * weight
        
        total = sum(touchpoint_counts.values())
        
        return [
            AttributionResult(
                touchpoint=tp,
                attributed_conversions=int(count),
                attributed_revenue=touchpoint_revenue.get(tp, 0),
                attribution_percentage=count / total * 100 if total > 0 else 0,
                model_type="time_decay"
            )
            for tp, count in touchpoint_counts.items()
        ]
    
    def _data_driven_attribution(
        self,
        journeys: List[List[Dict]],
        conversions: List[Dict]
    ) -> List[AttributionResult]:
        """数据驱动归因(使用Shapley值简化版)"""
        # 简化实现:基于各渠道在转化路径中的出现频率
        touchpoint_counts: Dict[str, int] = {}
        touchpoint_revenue: Dict[str, float] = {}
        
        for journey, conversion in zip(journeys, conversions):
            if journey and conversion:
                # 统计每个渠道在路径中的出现
                channels_in_journey = set(t.get("channel", "unknown") for t in journey)
                weight = 1.0 / len(channels_in_journey)
                
                for channel in channels_in_journey:
                    touchpoint_counts[channel] = touchpoint_counts.get(channel, 0) + weight
                    touchpoint_revenue[channel] = touchpoint_revenue.get(channel, 0) + conversion.get("revenue", 0) * weight
        
        total = sum(touchpoint_counts.values())
        
        return [
            AttributionResult(
                touchpoint=tp,
                attributed_conversions=int(count),
                attributed_revenue=touchpoint_revenue.get(tp, 0),
                attribution_percentage=count / total * 100 if total > 0 else 0,
                model_type="data_driven"
            )
            for tp, count in touchpoint_counts.items()
        ]
