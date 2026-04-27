"""数学智慧核心 - 数列分析引擎"""

import math
from typing import List, Optional

from ._mw_enums import SequenceType
from ._mw_dataclasses import SequenceAnalysis

__all__ = [
    'analyze_sequence',
    'predict_future',
]

class SequenceAnalyzer:
    """数列分析引擎 - 识别数列模式并进行预测"""
    
    # 黄金分割常数
    GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
    GOLDEN_CONJUGATE = (1 - math.sqrt(5)) / 2
    
    @classmethod
    def analyze_sequence(cls, data: List[float]) -> SequenceAnalysis:
        """
        分析数列并识别模式
        
        Args:
            data: 历史数据序列
            
        Returns:
            SequenceAnalysis: 数列分析结果
        """
        if len(data) < 3:
            return SequenceAnalysis(
                sequence_type=SequenceType.UNKNOWN,
                pattern_description="数据点不足,无法进行分析"
            )
        
        # 尝试识别数列类型
        # 1. 检查等差数列
        arith_result = cls._check_arithmetic(data)
        if arith_result:
            return arith_result
        
        # 2. 检查等比数列
        geo_result = cls._check_geometric(data)
        if geo_result:
            return geo_result
        
        # 3. 检查斐波那契数列
        fib_result = cls._check_fibonacci(data)
        if fib_result:
            return fib_result
        
        # 4. 检查指数增长
        exp_result = cls._check_exponential(data)
        if exp_result:
            return exp_result
        
        # 5. 多项式拟合
        return cls._polynomial_fit(data)
    
    @classmethod
    def _check_arithmetic(cls, data: List[float]) -> Optional[SequenceAnalysis]:
        """检查是否为等差数列"""
        diffs = [data[i+1] - data[i] for i in range(len(data)-1)]
        
        # 检查差值是否相等
        if len(set(diffs)) == 1:
            d = diffs[0]
            a1 = data[0]
            
            # 预测下一个值
            next_val = data[-1] + d
            
            # 计算拟合度
            predictions = [a1 + d * i for i in range(len(data))]
            r2 = cls._calculate_r_squared(data, predictions)
            
            return SequenceAnalysis(
                sequence_type=SequenceType.ARITHMETIC,
                pattern_description=f"等差数列,首项a₁={a1:.2f},公差d={d:.2f}",
                next_value=next_val,
                confidence=r2,
                first_term=a1,
                common_diff=d,
                predictions=predictions,
                model_params={"formula": f"aₙ = {a1} + (n-1)×{d}"},
                r_squared=r2
            )
        return None
    
    @classmethod
    def _check_geometric(cls, data: List[float]) -> Optional[SequenceAnalysis]:
        """检查是否为等比数列"""
        if any(v == 0 for v in data):
            return None
            
        ratios = [data[i+1] / data[i] for i in range(len(data)-1)]
        
        # 检查比值是否相等
        if len(set(round(r, 6) for r in ratios)) == 1:
            q = ratios[0]
            a1 = data[0]
            
            # 预测下一个值
            next_val = data[-1] * q
            
            # 计算拟合度
            predictions = [a1 * (q ** i) for i in range(len(data))]
            r2 = cls._calculate_r_squared(data, predictions)
            
            return SequenceAnalysis(
                sequence_type=SequenceType.GEOMETRIC,
                pattern_description=f"等比数列,首项a₁={a1:.2f},公比q={q:.4f}",
                next_value=next_val,
                confidence=r2,
                first_term=a1,
                common_ratio=q,
                predictions=predictions,
                model_params={
                    "formula": f"aₙ = {a1} × {q}^(n-1)",
                    "growth_rate": (q - 1) * 100
                },
                r_squared=r2
            )
        return None
    
    @classmethod
    def _check_fibonacci(cls, data: List[float]) -> Optional[SequenceAnalysis]:
        """检查是否为斐波那契类型数列"""
        if len(data) < 4:
            return None
        
        # 计算相邻比值
        ratios = [data[i+1] / data[i] for i in range(1, len(data)-1)]
        avg_ratio = sum(ratios) / len(ratios)
        
        # 检查是否符合斐波那契增长(接近黄金分割)
        if abs(avg_ratio - cls.GOLDEN_RATIO) < 0.2:
            # 使用闭式公式预测
            n = len(data)
            
            # 拟合参数
            F = [cls.GOLDEN_RATIO ** i - cls.GOLDEN_CONJUGATE ** i for i in range(n)]
            F = [f / math.sqrt(5) for f in F]
            
            # 最小二乘拟合
            scale = sum(d * f for d, f in zip(data, F)) / sum(f * f for f in F)
            
            # 预测
            next_n = n
            next_val = scale * (cls.GOLDEN_RATIO ** next_n - cls.GOLDEN_CONJUGATE ** next_n) / math.sqrt(5)
            
            predictions = [scale * (cls.GOLDEN_RATIO ** i - cls.GOLDEN_CONJUGATE ** i) / math.sqrt(5) 
                         for i in range(n)]
            r2 = cls._calculate_r_squared(data, predictions)
            
            return SequenceAnalysis(
                sequence_type=SequenceType.FIBONACCI,
                pattern_description=f"斐波那契型增长,黄金比例收敛≈{cls.GOLDEN_RATIO:.4f}",
                next_value=next_val,
                confidence=r2,
                first_term=scale / math.sqrt(5),
                model_params={
                    "formula": "Fₙ = (φⁿ - ψⁿ) / √5",
                    "golden_ratio": cls.GOLDEN_RATIO,
                    "scale_factor": scale
                },
                predictions=predictions,
                r_squared=r2
            )
        return None
    
    @classmethod
    def _check_exponential(cls, data: List[float]) -> Optional[SequenceAnalysis]:
        """检查是否为指数增长"""
        if any(v <= 0 for v in data):
            return None
        
        # 对数变换后检查是否为线性
        log_data = [math.log(v) for v in data]
        
        # 检查对数变换后的线性度
        arith_result = cls._check_arithmetic(log_data)
        if arith_result and arith_result.r_squared > 0.95:
            # 恢复参数
            a1 = math.exp(arith_result.first_term)
            r = math.exp(arith_result.common_diff)
            
            next_val = data[-1] * r
            
            predictions = [a1 * (r ** i) for i in range(len(data))]
            r2 = cls._calculate_r_squared(data, predictions)
            
            return SequenceAnalysis(
                sequence_type=SequenceType.EXPONENTIAL,
                pattern_description=f"指数增长,初始值={a1:.2f},增长率={(r-1)*100:.2f}%",
                next_value=next_val,
                confidence=r2,
                first_term=a1,
                common_ratio=r,
                predictions=predictions,
                model_params={
                    "formula": f"aₙ = {a1:.2f} × {r:.4f}^(n-1)",
                    "doubling_time": math.log(2) / math.log(r) if r > 1 else None
                },
                r_squared=r2
            )
        return None
    
    @classmethod
    def _polynomial_fit(cls, data: List[float]) -> SequenceAnalysis:
        """多项式拟合"""
        n = len(data)
        
        # 尝试二次多项式
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(data) / n
        
        # 线性拟合
        numerator = sum((x[i] - x_mean) * (data[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # 预测
        predictions = [slope * i + intercept for i in range(n)]
        r2 = cls._calculate_r_squared(data, predictions)
        
        return SequenceAnalysis(
            sequence_type=SequenceType.POLYNOMIAL,
            pattern_description=f"线性趋势,斜率={slope:.4f}",
            next_value=slope * n + intercept,
            confidence=r2,
            model_params={"slope": slope, "intercept": intercept},
            predictions=predictions,
            r_squared=r2
        )
    
    @classmethod
    def _calculate_r_squared(cls, actual: List[float], predicted: List[float]) -> float:
        """计算决定系数R²"""
        n = len(actual)
        if n == 0:
            return 0
        
        y_mean = sum(actual) / n
        ss_tot = sum((y - y_mean) ** 2 for y in actual)
        ss_res = sum((actual[i] - predicted[i]) ** 2 for i in range(n))
        
        if ss_tot == 0:
            return 1.0 if ss_res == 0 else 0.0
        
        return 1 - ss_res / ss_tot
    
    @classmethod
    def predict_future(cls, data: List[float], steps: int = 5) -> List[float]:
        """预测未来N个值"""
        analysis = cls.analyze_sequence(data)
        
        if analysis.sequence_type == SequenceType.ARITHMETIC:
            predictions = []
            last_val = data[-1]
            d = analysis.common_diff
            for _ in range(steps):
                last_val += d
                predictions.append(last_val)
            return predictions
        
        elif analysis.sequence_type == SequenceType.GEOMETRIC:
            predictions = []
            last_val = data[-1]
            q = analysis.common_ratio
            for _ in range(steps):
                last_val *= q
                predictions.append(last_val)
            return predictions
        
        elif analysis.sequence_type == SequenceType.FIBONACCI:
            # 使用指数近似
            scale = analysis.model_params.get("scale_factor", 1)
            n = len(data)
            predictions = []
            for i in range(steps):
                val = scale * (cls.GOLDEN_RATIO ** (n + i) - cls.GOLDEN_CONJUGATE ** (n + i)) / math.sqrt(5)
                predictions.append(val)
            return predictions
        
        # 线性外推
        n = len(data)
        slope = (data[-1] - data[0]) / (n - 1) if n > 1 else 0
        predictions = [data[-1] + slope * (i + 1) for i in range(steps)]
        return predictions
