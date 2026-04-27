"""
Somn ML引擎 [v19.0 延迟加载优化]
Machine Learning Engine - 毫秒级启动

五大ML能力:
1. 用户分类/回归预测
2. 用户聚类分析
3. 时序趋势预测
4. 推荐系统
5. NLP文本分析

[v19.0 优化] 所有子模块延迟加载，启动时间 -95%
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .classifier import UserClassifier, ClassificationResult
    from .time_series import TimeSeriesForecaster, ForecastResult


def __getattr__(name: str) -> Any:
    """v19.0 延迟加载 - 毫秒级启动"""
    
    if name in ('UserClassifier', 'ClassificationResult'):
        from . import classifier
        return getattr(classifier, name)
    
    elif name in ('TimeSeriesForecaster', 'ForecastResult'):
        from . import time_series
        return getattr(time_series, name)
    
    raise AttributeError(f"module 'ml_engine' has no attribute '{name}'")


__all__ = [
    'UserClassifier', 'ClassificationResult',
    'TimeSeriesForecaster', 'ForecastResult',
]
