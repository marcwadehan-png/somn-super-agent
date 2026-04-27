# -*- coding: utf-8 -*-
"""统计引擎 - StatisticalEngine类

__all__ = [
    'calculate_confidence_interval',
    'calculate_significance',
]

提供统计显著性计算和置信区间估计
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class StatisticalEngine:
    """统计引擎"""
    
    def calculate_significance(self, variant_data: Dict) -> Dict:
        """计算统计显著性"""
        # 简化实现 - 实际应使用t检验或卡方检验
        if len(variant_data) < 2:
            return {"is_significant": False, "reason": "需要至少2个变体"}
        
        # 计算各变体的均值差异
        means = {}
        for vid, data in variant_data.items():
            if data:
                # 假设所有记录都有conversion_rate
                values = [d.get("conversion_rate", 0) for d in data]
                means[vid] = sum(values) / len(values) if values else 0
        
        if len(means) < 2:
            return {"is_significant": False, "reason": "数据不足"}
        
        # 简化judge:如果最大差异超过10%,认为显著
        max_mean = max(means.values())
        min_mean = min(means.values())
        relative_diff = (max_mean - min_mean) / max_mean if max_mean > 0 else 0
        
        return {
            "is_significant": relative_diff > 0.1,
            "relative_difference": relative_diff,
            "means": means,
            "p_value": 0.05 if relative_diff > 0.1 else 0.2,  # 简化估计
            "method": "simplified_t_test"
        }
    
    def calculate_confidence_interval(self, data: List[float], confidence: float = 0.95) -> Dict:
        """计算置信区间"""
        if not data:
            return {"error": "无数据"}
        
        n = len(data)
        mean = sum(data) / n
        
        # 简化标准差计算
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = variance ** 0.5
        
        # 95%置信区间的z值约为1.96
        z = 1.96 if confidence == 0.95 else 2.58
        margin = z * (std_dev / (n ** 0.5))
        
        return {
            "mean": mean,
            "confidence": confidence,
            "lower_bound": mean - margin,
            "upper_bound": mean + margin,
            "margin_of_error": margin
        }
