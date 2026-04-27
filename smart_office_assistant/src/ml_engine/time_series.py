"""
__all__ = [
    'auto_forecast',
    'forecast',
    'get_growth_rate',
    'get_last_n',
    'get_trend',
    'to_dict',
]

时序预测引擎 - 增长趋势与metrics预测
支持: 线性趋势,移动平均,指数平滑,季节性分解
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

class ForecastMethod(Enum):
    """预测方法"""
    LINEAR = "linear"                     # 线性回归
    MOVING_AVERAGE = "moving_average"     # 移动平均
    EXPONENTIAL = "exponential"           # 指数平滑
    SEASONAL = "seasonal"                 # 季节性分解
    HOLT_WINTERS = "holt_winters"         # Holt-Winters三次指数平滑

class MetricType(Enum):
    """metrics类型"""
    DAU = "dau"                 # 日活跃用户
    MAU = "mau"                 # 月活跃用户
    REVENUE = "revenue"         # 营收
    CONVERSION = "conversion"   # 转化率
    CHURN = "churn"             # 流失率
    ACQUISITION = "acquisition" # 新增用户
    RETENTION = "retention"     # 留存率
    ENGAGEMENT = "engagement"   # 参与度

@dataclass
class TimeSeriesData:
    """时序数据"""
    metric_type: MetricType
    timestamps: List[str]         # ISO格式时间列表
    values: List[float]           # 对应数值
    unit: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        assert len(self.timestamps) == len(self.values), "时间戳和数值长度必须一致"
    
    def get_last_n(self, n: int) -> 'TimeSeriesData':
        """get最近N个数据点"""
        return TimeSeriesData(
            metric_type=self.metric_type,
            timestamps=self.timestamps[-n:],
            values=self.values[-n:],
            unit=self.unit
        )
    
    def get_growth_rate(self) -> Optional[float]:
        """计算增长率(最近两期对比)"""
        if len(self.values) < 2 or self.values[-2] == 0:
            return None
        return (self.values[-1] - self.values[-2]) / self.values[-2]
    
    def get_trend(self, window: int = 7) -> str:
        """judge趋势方向"""
        if len(self.values) < window:
            return "insufficient_data"
        recent = self.values[-window:]
        slope = self._calculate_slope(recent)
        if slope > 0.02:
            return "upward"
        elif slope < -0.02:
            return "downward"
        return "stable"
    
    def _calculate_slope(self, values: List[float]) -> float:
        n = len(values)
        if n < 2:
            return 0
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        if denominator == 0 or y_mean == 0:
            return 0
        return (numerator / denominator) / y_mean  # 标准化斜率

@dataclass
class ForecastResult:
    """预测结果"""
    metric_type: MetricType
    method: ForecastMethod
    historical: TimeSeriesData
    forecast_values: List[float]
    forecast_timestamps: List[str]
    confidence_intervals: List[Tuple[float, float]] = field(default_factory=list)  # (lower, upper)
    accuracy_metrics: Dict[str, float] = field(default_factory=dict)
    trend: str = "stable"
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    forecasted_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'metric_type': self.metric_type.value,
            'method': self.method.value,
            'forecast_values': [round(v, 4) for v in self.forecast_values],
            'forecast_timestamps': self.forecast_timestamps,
            'confidence_intervals': [
                {'lower': round(lo, 4), 'upper': round(hi, 4)}
                for lo, hi in self.confidence_intervals
            ],
            'accuracy_metrics': {k: round(v, 4) for k, v in self.accuracy_metrics.items()},
            'trend': self.trend,
            'insights': self.insights,
            'recommendations': self.recommendations,
            'forecasted_at': self.forecasted_at
        }

class TimeSeriesForecaster:
    """时序预测器"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
    
    def forecast(self, data: TimeSeriesData, periods: int = 7,
                 method: ForecastMethod = ForecastMethod.EXPONENTIAL) -> ForecastResult:
        """预测未来N期数值"""
        if method == ForecastMethod.LINEAR:
            return self._forecast_linear(data, periods)
        elif method == ForecastMethod.MOVING_AVERAGE:
            return self._forecast_moving_average(data, periods)
        elif method == ForecastMethod.EXPONENTIAL:
            return self._forecast_exponential(data, periods)
        elif method == ForecastMethod.SEASONAL:
            return self._forecast_seasonal(data, periods)
        elif method == ForecastMethod.HOLT_WINTERS:
            return self._forecast_holt_winters(data, periods)
        else:
            return self._forecast_exponential(data, periods)
    
    def auto_forecast(self, data: TimeSeriesData, periods: int = 7) -> ForecastResult:
        """自动选择最优预测方法"""
        # 根据数据characteristics选择方法
        n = len(data.values)
        
        if n < 7:
            method = ForecastMethod.LINEAR
        elif n < 14:
            method = ForecastMethod.MOVING_AVERAGE
        elif self._has_seasonality(data):
            method = ForecastMethod.HOLT_WINTERS
        else:
            method = ForecastMethod.EXPONENTIAL
        
        return self.forecast(data, periods, method)
    
    def _forecast_linear(self, data: TimeSeriesData, periods: int) -> ForecastResult:
        """线性回归预测"""
        values = data.values
        n = len(values)
        
        # 计算线性回归参数
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # 计算残差标准差
        residuals = [v - (slope * i + intercept) for i, v in enumerate(values)]
        std_residual = math.sqrt(sum(r**2 for r in residuals) / max(n-2, 1))
        
        # generate预测值
        forecasts = [max(0, slope * (n + i) + intercept) for i in range(periods)]
        
        # generate时间戳
        timestamps = self._generate_timestamps(data.timestamps[-1], periods)
        
        # 置信区间 (95%)
        ci = [(max(0, f - 1.96 * std_residual), f + 1.96 * std_residual) for f in forecasts]
        
        # 计算R²
        ss_total = sum((v - y_mean) ** 2 for v in values)
        ss_residual = sum(r ** 2 for r in residuals)
        r_squared = 1 - (ss_residual / ss_total) if ss_total > 0 else 0
        
        return ForecastResult(
            metric_type=data.metric_type,
            method=ForecastMethod.LINEAR,
            historical=data,
            forecast_values=forecasts,
            forecast_timestamps=timestamps,
            confidence_intervals=ci,
            accuracy_metrics={'r_squared': r_squared, 'mae': sum(abs(r) for r in residuals) / n},
            trend='upward' if slope > 0 else ('downward' if slope < 0 else 'stable'),
            insights=self._generate_insights(data, forecasts, slope),
            recommendations=self._generate_recommendations(data, forecasts, slope)
        )
    
    def _forecast_moving_average(self, data: TimeSeriesData, periods: int,
                                  window: int = 7) -> ForecastResult:
        """移动平均预测"""
        values = data.values
        window = min(window, len(values))
        
        # 计算移动平均
        ma = sum(values[-window:]) / window
        
        # 简单趋势
        recent_growth = self._calc_recent_growth(values, window)
        
        forecasts = []
        current = ma
        for _ in range(periods):
            current = current * (1 + recent_growth * 0.5)  # 平滑趋势
            forecasts.append(max(0, current))
        
        timestamps = self._generate_timestamps(data.timestamps[-1], periods)
        
        std = self._calc_std(values[-window:])
        ci = [(max(0, f - 1.96 * std), f + 1.96 * std) for f in forecasts]
        
        slope = forecasts[-1] - forecasts[0] if periods > 1 else 0
        
        return ForecastResult(
            metric_type=data.metric_type,
            method=ForecastMethod.MOVING_AVERAGE,
            historical=data,
            forecast_values=forecasts,
            forecast_timestamps=timestamps,
            confidence_intervals=ci,
            accuracy_metrics={'window': window},
            trend='upward' if slope > 0 else ('downward' if slope < 0 else 'stable'),
            insights=self._generate_insights(data, forecasts, slope),
            recommendations=self._generate_recommendations(data, forecasts, slope)
        )
    
    def _forecast_exponential(self, data: TimeSeriesData, periods: int,
                               alpha: float = 0.3) -> ForecastResult:
        """指数平滑预测(Holt双参数)"""
        values = data.values
        n = len(values)
        
        # init
        level = values[0]
        trend_init = (values[-1] - values[0]) / (n - 1) if n > 1 else 0
        beta = 0.1
        
        # 迭代更新
        levels = [level]
        trends = [trend_init]
        
        for i in range(1, n):
            prev_level = levels[-1]
            prev_trend = trends[-1]
            
            new_level = alpha * values[i] + (1 - alpha) * (prev_level + prev_trend)
            new_trend = beta * (new_level - prev_level) + (1 - beta) * prev_trend
            
            levels.append(new_level)
            trends.append(new_trend)
        
        # 预测
        last_level = levels[-1]
        last_trend = trends[-1]
        
        forecasts = [max(0, last_level + (i + 1) * last_trend) for i in range(periods)]
        
        # 计算MAE(训练集)
        fitted = [levels[i] + trends[i] for i in range(n-1)]
        mae = sum(abs(values[i+1] - fitted[i]) for i in range(len(fitted))) / len(fitted)
        
        timestamps = self._generate_timestamps(data.timestamps[-1], periods)
        ci = [(max(0, f - 1.96 * mae), f + 1.96 * mae) for f in forecasts]
        
        slope = last_trend
        
        return ForecastResult(
            metric_type=data.metric_type,
            method=ForecastMethod.EXPONENTIAL,
            historical=data,
            forecast_values=forecasts,
            forecast_timestamps=timestamps,
            confidence_intervals=ci,
            accuracy_metrics={'mae': mae, 'alpha': alpha, 'beta': beta},
            trend='upward' if slope > 0 else ('downward' if slope < 0 else 'stable'),
            insights=self._generate_insights(data, forecasts, slope),
            recommendations=self._generate_recommendations(data, forecasts, slope)
        )
    
    def _forecast_seasonal(self, data: TimeSeriesData, periods: int) -> ForecastResult:
        """季节性分解预测(简化版STL)"""
        values = data.values
        n = len(values)
        period = 7  # 假设周期为7天
        
        if n < period * 2:
            return self._forecast_exponential(data, periods)
        
        # 简单季节分解
        seasonal_factors = []
        for i in range(period):
            season_values = [values[j] for j in range(i, n, period)]
            factor = sum(season_values) / (len(season_values) * (sum(values) / n)) if sum(values) > 0 else 1.0
            seasonal_factors.append(factor)
        
        # 去季节化趋势
        deseasonalized = [values[i] / seasonal_factors[i % period] if seasonal_factors[i % period] != 0 else values[i]
                         for i in range(n)]
        
        # 线性趋势
        x_mean = (n - 1) / 2
        y_mean = sum(deseasonalized) / n
        num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(deseasonalized))
        den = sum((i - x_mean) ** 2 for i in range(n))
        slope = num / den if den != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # 重新加入季节性
        forecasts = []
        for i in range(periods):
            trend_val = slope * (n + i) + intercept
            seasonal = seasonal_factors[(n + i) % period]
            forecasts.append(max(0, trend_val * seasonal))
        
        timestamps = self._generate_timestamps(data.timestamps[-1], periods)
        std = self._calc_std(values)
        ci = [(max(0, f - 1.96 * std * 0.5), f + 1.96 * std * 0.5) for f in forecasts]
        
        return ForecastResult(
            metric_type=data.metric_type,
            method=ForecastMethod.SEASONAL,
            historical=data,
            forecast_values=forecasts,
            forecast_timestamps=timestamps,
            confidence_intervals=ci,
            accuracy_metrics={'seasonal_period': period},
            trend='upward' if slope > 0 else ('downward' if slope < 0 else 'stable'),
            insights=self._generate_insights(data, forecasts, slope),
            recommendations=self._generate_recommendations(data, forecasts, slope)
        )
    
    def _forecast_holt_winters(self, data: TimeSeriesData, periods: int) -> ForecastResult:
        """Holt-Winters三次指数平滑(含季节性)"""
        return self._forecast_seasonal(data, periods)
    
    def _has_seasonality(self, data: TimeSeriesData, period: int = 7) -> bool:
        """检测是否有季节性"""
        values = data.values
        if len(values) < period * 2:
            return False
        
        # 简单自相关检验
        autocorr = self._autocorrelation(values, period)
        return autocorr > 0.5
    
    def _autocorrelation(self, values: List[float], lag: int) -> float:
        """计算自相关系数"""
        n = len(values)
        if n <= lag:
            return 0
        mean = sum(values) / n
        
        numerator = sum((values[i] - mean) * (values[i + lag] - mean) for i in range(n - lag))
        denominator = sum((v - mean) ** 2 for v in values)
        
        return numerator / denominator if denominator != 0 else 0
    
    def _calc_recent_growth(self, values: List[float], window: int) -> float:
        """计算近期增长率"""
        if len(values) < 2:
            return 0
        recent = values[-window:]
        if len(recent) < 2 or recent[0] == 0:
            return 0
        return (recent[-1] - recent[0]) / (recent[0] * len(recent))
    
    def _calc_std(self, values: List[float]) -> float:
        """计算标准差"""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
        return math.sqrt(variance)
    
    def _generate_timestamps(self, last_ts: str, periods: int) -> List[str]:
        """generate预测时间戳"""
        try:
            last_date = datetime.fromisoformat(last_ts[:10])
        except Exception:
            last_date = datetime.now()
        
        return [
            (last_date + timedelta(days=i+1)).strftime('%Y-%m-%d')
            for i in range(periods)
        ]
    
    def _generate_insights(self, data: TimeSeriesData, forecasts: List[float], slope: float) -> List[str]:
        """generate预测洞察"""
        insights = []
        current = data.values[-1]
        future = forecasts[-1]
        
        change_pct = (future - current) / current * 100 if current > 0 else 0
        
        if change_pct > 20:
            insights.append(f"预计{len(forecasts)}天后增长 {change_pct:.1f}%,增势强劲")
        elif change_pct > 5:
            insights.append(f"预计{len(forecasts)}天后增长 {change_pct:.1f}%,保持正向趋势")
        elif change_pct < -20:
            insights.append(f"⚠️ 预计{len(forecasts)}天后下降 {abs(change_pct):.1f}%,需警惕")
        elif change_pct < -5:
            insights.append(f"预计{len(forecasts)}天后下降 {abs(change_pct):.1f}%,趋势走弱")
        else:
            insights.append(f"预计{len(forecasts)}天后变化不大({change_pct:+.1f}%),趋势平稳")
        
        # 历史增长率
        hist_growth = data.get_growth_rate()
        if hist_growth is not None:
            insights.append(f"近期增长率: {hist_growth*100:+.1f}%")
        
        return insights
    
    def _generate_recommendations(self, data: TimeSeriesData, forecasts: List[float], slope: float) -> List[str]:
        """generate预测建议"""
        current = data.values[-1]
        future_avg = sum(forecasts) / len(forecasts) if forecasts else current
        
        if future_avg > current * 1.1:
            return ["当前增长势头良好,保持核心strategy不变", "考虑适度扩大投入放大效果"]
        elif future_avg < current * 0.9:
            return ["metrics存在下滑风险,建议深入分析原因", "立即启动诊断分析,制定干预计划"]
        else:
            return ["趋势平稳,关注行业变化寻找突破机会", "考虑开展A/B测试探索增长新方向"]
