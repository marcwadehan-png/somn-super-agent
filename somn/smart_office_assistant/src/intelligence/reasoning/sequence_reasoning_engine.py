"""
数列推理引擎 - Sequence Reasoning Engine
=========================================

基于数列数学的深度推理引擎,支持企业增长趋势预测和优化decision

v1.0.0 新增功能:
- 数列模式recognize:自动recognize等差,等比,斐波那契等模式
- 增长预测:基于历史数据预测未来趋势
- 级数分析:收敛性分析,级数求和
- 递推求解:自动建立和求解递推关系
- 优化推理:基于数列理论的优化strategy

核心推理模式:
1. 趋势外推推理 - 基于数列增长模式预测
2. 周期分析推理 - 基于傅里叶/季节性分解
3. 收敛分析推理 - 基于级数收敛理论
4. 优化推理 - 基于数列极值的优化strategy
"""

import math
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
from collections import deque

from ..engines.math_wisdom_core import (
    SequenceAnalyzer, SequenceType, SequenceAnalysis,
    MathWisdomCore, MathWisdomInsight, TrendType
)

class SequenceReasoningMode(Enum):
    """数列推理模式"""
    TREND_EXTRAPOLATION = "trend_extrapolation"     # 趋势外推
    CYCLE_ANALYSIS = "cycle_analysis"              # 周期分析
    CONVERGENCE_ANALYSIS = "convergence_analysis"  # 收敛分析
    OPTIMIZATION = "optimization"                  # 优化推理
    RECURRENCE_SOLVING = "recurrence_solving"     # 递推求解
    COMPARATIVE = "comparative"                    # 比较推理

@dataclass
class TrendPrediction:
    """趋势预测结果"""
    short_term: List[float] = field(default_factory=list)    # 短期预测(1-3期)
    medium_term: List[float] = field(default_factory=list)  # 中期预测(4-12期)
    long_term: List[float] = field(default_factory=list)    # 长期预测(12+期)
    
    confidence: float = 0.0
    pattern_type: SequenceType = SequenceType.UNKNOWN
    pattern_description: str = ""
    
    # 关键metrics
    growth_rate: float = 0.0           # 增长率
    doubling_time: Optional[float] = None  # 倍增时间
    saturation_point: Optional[float] = None  # 饱和点
    
    # 风险评估
    volatility: float = 0.0
    confidence_interval: Tuple[float, float] = (0.0, 0.0)

@dataclass
class CycleAnalysis:
    """周期分析结果"""
    period: int = 0                      # 周期长度
    amplitude: float = 0.0               # 振幅
    phase: float = 0.0                   # 相位
    
    # 分解
    trend_component: List[float] = field(default_factory=list)
    seasonal_component: List[float] = field(default_factory=list)
    residual_component: List[float] = field(default_factory=list)
    
    # 置信度
    confidence: float = 0.0
    seasonality_strength: float = 0.0

@dataclass
class ConvergenceAnalysis:
    """收敛分析结果"""
    is_convergent: bool = False
    is_divergent: bool = False
    
    limit: Optional[float] = None        # 极限值
    convergence_rate: str = ""           # 收敛速度描述
    
    # 级数分析
    series_type: str = ""                # 级数类型
    sum_if_convergent: Optional[float] = None  # 和(如果收敛)
    
    # 收敛条件
    convergence_condition: str = ""
    radius_of_convergence: Optional[float] = None  # 收敛半径

@dataclass
class SequenceReasoningResult:
    """数列推理结果"""
    reasoning_id: str
    mode: SequenceReasoningMode
    
    # 输入
    input_data: List[float]
    context: Dict[str, Any]
    
    # 输出
    success: bool
    answer: str
    confidence: float
    
    # 分析结果
    trend_prediction: Optional[TrendPrediction] = None
    cycle_analysis: Optional[CycleAnalysis] = None
    convergence_analysis: Optional[ConvergenceAnalysis] = None
    
    # 推理过程
    reasoning_steps: List[Dict[str, Any]] = field(default_factory=list)
    mathematical_basis: str = ""
    
    # 建议
    recommendations: List[str] = field(default_factory=list)

class SequenceReasoningEngine:
    """
    数列推理引擎
    
    提供基于数列数学的深度推理能力,
    支持企业增长预测,周期分析,收敛judge等场景
    """
    
    def __init__(self):
        self.sequence_analyzer = SequenceAnalyzer()
        self.math_wisdom = MathWisdomCore()
        
        # 推理历史
        self.reasoning_history: deque = deque(maxlen=100)
    
    def reason(self, problem: str, data: List[float], 
               mode: SequenceReasoningMode = SequenceReasoningMode.TREND_EXTRAPOLATION,
               context: Optional[Dict[str, Any]] = None) -> SequenceReasoningResult:
        """
        核心推理方法
        
        Args:
            problem: 问题描述
            data: 输入数据序列
            mode: 推理模式
            context: 上下文信息
            
        Returns:
            SequenceReasoningResult: 推理结果
        """
        context = context or {}
        reasoning_id = f"seq_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 记录推理步骤
        steps = []
        
        # 步骤1:数据预处理
        steps.append({
            "step": 1,
            "action": "data_preprocessing",
            "description": f"接收输入数据,共{len(data)}个数据点",
            "result": f"数据范围: [{min(data):.2f}, {max(data):.2f}]"
        })
        
        # 步骤2:模式recognize
        analysis = self.sequence_analyzer.analyze_sequence(data)
        steps.append({
            "step": 2,
            "action": "pattern_recognition",
            "description": f"recognize到模式: {analysis.sequence_type.value}",
            "result": analysis.pattern_description
        })
        
        # 步骤3:根据模式执行推理
        if mode == SequenceReasoningMode.TREND_EXTRAPOLATION:
            result = self._trend_extrapolation_reasoning(data, analysis, context)
        elif mode == SequenceReasoningMode.CYCLE_ANALYSIS:
            result = self._cycle_analysis_reasoning(data, context)
        elif mode == SequenceReasoningMode.CONVERGENCE_ANALYSIS:
            result = self._convergence_reasoning(data, context)
        elif mode == SequenceReasoningMode.OPTIMIZATION:
            result = self._optimization_reasoning(data, analysis, context)
        elif mode == SequenceReasoningMode.RECURRENCE_SOLVING:
            result = self._recurrence_reasoning(data, context)
        else:
            result = self._comparative_reasoning(data, analysis, context)
        
        result.reasoning_steps = steps
        result.reasoning_id = reasoning_id
        
        # 添加到历史
        self.reasoning_history.append(result)
        
        return result
    
    def _trend_extrapolation_reasoning(self, data: List[float],
                                      analysis: SequenceAnalysis,
                                      context: Dict[str, Any]) -> SequenceReasoningResult:
        """趋势外推推理"""
        
        # generate预测
        short_term = self.sequence_analyzer.predict_future(data, 3)
        medium_term = self.sequence_analyzer.predict_future(data, 12)
        
        # 计算增长率
        if len(data) >= 2:
            growth_rate = (data[-1] - data[0]) / data[0] if data[0] != 0 else 0
        else:
            growth_rate = 0
        
        # 计算波动性
        returns = [data[i+1]/data[i] if data[i] != 0 else 0 for i in range(len(data)-1)]
        volatility = np.std(returns) if len(returns) > 1 else 0
        
        # 构建预测结果
        trend_prediction = TrendPrediction(
            short_term=short_term[:3],
            medium_term=medium_term[3:],
            confidence=analysis.confidence,
            pattern_type=analysis.sequence_type,
            pattern_description=analysis.pattern_description,
            growth_rate=growth_rate,
            volatility=volatility,
            confidence_interval=(min(short_term) * 0.9, max(short_term) * 1.1)
        )
        
        # 添加倍增时间(如果是指数增长)
        if analysis.sequence_type == SequenceType.GEOMETRIC and analysis.common_ratio > 1:
            trend_prediction.doubling_time = math.log(2) / math.log(analysis.common_ratio)
        
        # generate答案和建议
        answer = self._generate_trend_answer(data, trend_prediction)
        recommendations = self._generate_trend_recommendations(trend_prediction)
        
        return SequenceReasoningResult(
            reasoning_id="",
            mode=SequenceReasoningMode.TREND_EXTRAPOLATION,
            input_data=data,
            context=context,
            success=True,
            answer=answer,
            confidence=analysis.confidence,
            trend_prediction=trend_prediction,
            mathematical_basis=f"基于{analysis.sequence_type.value}数列模型的趋势外推",
            recommendations=recommendations
        )
    
    def _cycle_analysis_reasoning(self, data: List[float],
                                   context: Dict[str, Any]) -> SequenceReasoningResult:
        """周期分析推理"""
        
        # 简单的周期检测
        n = len(data)
        if n < 4:
            return SequenceReasoningResult(
                reasoning_id="",
                mode=SequenceReasoningMode.CYCLE_ANALYSIS,
                input_data=data,
                context=context,
                success=False,
                answer="数据点不足,无法进行周期分析",
                confidence=0.0,
                recommendations=["建议收集至少12个周期的数据"]
            )
        
        # 使用自相关检测周期
        period = self._detect_period(data)
        
        # 分离趋势和季节性(简化)
        trend_component = self._extract_trend(data)
        seasonal_component = [d - t for d, t in zip(data, trend_component)]
        residual_component = [d - t - s for d, t, s in zip(data, trend_component, seasonal_component)]
        
        # 计算振幅
        amplitude = max(seasonal_component) - min(seasonal_component)
        
        cycle_analysis = CycleAnalysis(
            period=period,
            amplitude=amplitude,
            trend_component=trend_component[:n],
            seasonal_component=seasonal_component,
            residual_component=residual_component,
            confidence=0.7 if period > 0 else 0.3,
            seasonality_strength=amplitude / (max(data) - min(data)) if max(data) != min(data) else 0
        )
        
        answer = f"检测到周期为{period},振幅为{amplitude:.2f}"
        recommendations = [
            f"数据呈现{period}期周期模式",
            "建议考虑季节性调整",
            "可以利用周期进行预测"
        ]
        
        return SequenceReasoningResult(
            reasoning_id="",
            mode=SequenceReasoningMode.CYCLE_ANALYSIS,
            input_data=data,
            context=context,
            success=True,
            answer=answer,
            confidence=cycle_analysis.confidence,
            cycle_analysis=cycle_analysis,
            mathematical_basis="自相关分析检测周期性",
            recommendations=recommendations
        )
    
    def _convergence_reasoning(self, data: List[float],
                               context: Dict[str, Any]) -> SequenceReasoningResult:
        """收敛分析推理"""
        
        # 检查收敛性
        if len(data) < 3:
            return SequenceReasoningResult(
                reasoning_id="",
                mode=SequenceReasoningMode.CONVERGENCE_ANALYSIS,
                input_data=data,
                context=context,
                success=False,
                answer="数据不足",
                confidence=0.0
            )
        
        # 计算最近几项的变化趋势
        recent_changes = [abs(data[i+1] - data[i]) for i in range(len(data)-3, len(data)-1)]
        
        # judge收敛
        is_converging = all(recent_changes[i] >= recent_changes[i+1] for i in range(len(recent_changes)-1))
        
        # 估计极限
        if is_converging:
            limit = data[-1]
            convergence_rate = "快速收敛" if max(recent_changes) < 0.01 else "缓慢收敛"
        else:
            limit = None
            convergence_rate = "发散或振荡"
        
        convergence_analysis = ConvergenceAnalysis(
            is_convergent=is_converging,
            is_divergent=not is_converging,
            limit=limit,
            convergence_rate=convergence_rate,
            series_type="离散数据序列"
        )
        
        answer = f"{'收敛' if is_converging else '发散'},极限估计: {limit:.2f if limit else 'N/A'}"
        recommendations = [
            f"序列{'趋向稳定' if is_converging else '持续变化'}",
            "关注收敛速度以预测稳定时间"
        ]
        
        return SequenceReasoningResult(
            reasoning_id="",
            mode=SequenceReasoningMode.CONVERGENCE_ANALYSIS,
            input_data=data,
            context=context,
            success=True,
            answer=answer,
            confidence=0.8,
            convergence_analysis=convergence_analysis,
            mathematical_basis="数列收敛性判别:单调有界收敛,夹逼收敛",
            recommendations=recommendations
        )
    
    def _optimization_reasoning(self, data: List[float],
                                analysis: SequenceAnalysis,
                                context: Dict[str, Any]) -> SequenceReasoningResult:
        """优化推理"""
        
        # 寻找极值点
        max_val = max(data)
        min_val = min(data)
        max_idx = data.index(max_val)
        min_idx = data.index(min_val)
        
        # judge趋势
        recent_trend = sum(data[-3:]) / 3 - sum(data[-6:-3]) / 3 if len(data) >= 6 else 0
        
        # generate优化建议
        recommendations = []
        
        if analysis.sequence_type == SequenceType.ARITHMETIC:
            if analysis.common_diff > 0:
                recommendations.append("当前处于线性增长阶段,建议继续执行")
                recommendations.append(f"保持当前增长量,每期+{analysis.common_diff:.2f}")
            else:
                recommendations.append("当前处于线性下降阶段,需要调整strategy")
        elif analysis.sequence_type == SequenceType.GEOMETRIC:
            if analysis.common_ratio > 1:
                recommendations.append("当前处于指数增长阶段,注意增长天花板")
            else:
                recommendations.append("当前处于指数衰减阶段,需要新增长点")
        else:
            if recent_trend > 0:
                recommendations.append("近期趋势向好,建议维持现状")
            else:
                recommendations.append("近期趋势下降,需要分析原因")
        
        answer = f"最大值: {max_val:.2f} (第{max_idx+1}期),最小值: {min_val:.2f} (第{min_idx+1}期)"
        
        return SequenceReasoningResult(
            reasoning_id="",
            mode=SequenceReasoningMode.OPTIMIZATION,
            input_data=data,
            context=context,
            success=True,
            answer=answer,
            confidence=analysis.confidence,
            mathematical_basis="数列极值分析:最值,趋势,边际分析",
            recommendations=recommendations
        )
    
    def _recurrence_reasoning(self, data: List[float],
                              context: Dict[str, Any]) -> SequenceReasoningResult:
        """递推关系推理"""
        
        if len(data) < 3:
            return SequenceReasoningResult(
                reasoning_id="",
                mode=SequenceReasoningMode.RECURRENCE_SOLVING,
                input_data=data,
                context=context,
                success=False,
                answer="数据不足,无法建立递推关系",
                confidence=0.0
            )
        
        # 尝试一阶递推
        first_order_diffs = [data[i+1] - data[i] for i in range(len(data)-1)]
        
        # 检查一阶递推的常数性
        first_order_const = len(set(round(d, 6) for d in first_order_diffs)) == 1
        
        # 尝试二阶递推
        second_order_diffs = [first_order_diffs[i+1] - first_order_diffs[i] 
                             for i in range(len(first_order_diffs)-1)]
        second_order_const = len(set(round(d, 6) for d in second_order_diffs)) == 1
        
        recurrence_type = "unknown"
        recurrence_formula = ""
        
        if first_order_const:
            recurrence_type = "一阶线性递推"
            d = first_order_diffs[0]
            recurrence_formula = f"aₙ = aₙ₋₁ + {d:.4f}"
        elif second_order_const:
            recurrence_type = "二阶线性递推"
            d1 = first_order_diffs[-1]
            d2 = second_order_diffs[0]
            recurrence_formula = f"aₙ = 2aₙ₋₁ - aₙ₋₂ + {d2:.4f}"  # 简化
        
        # 预测
        predictions = []
        if first_order_const:
            current = data[-1]
            d = first_order_diffs[0]
            for _ in range(5):
                current += d
                predictions.append(current)
        elif second_order_const:
            current = data[-1]
            prev = data[-2]
            for _ in range(5):
                next_val = 2 * current - prev + second_order_diffs[0]
                prev, current = current, next_val
                predictions.append(current)
        
        answer = f"递推类型: {recurrence_type}\n递推公式: {recurrence_formula}"
        
        return SequenceReasoningResult(
            reasoning_id="",
            mode=SequenceReasoningMode.RECURRENCE_SOLVING,
            input_data=data,
            context=context,
            success=True,
            answer=answer,
            confidence=0.8 if recurrence_type != "unknown" else 0.3,
            mathematical_basis=f"递推关系分析:{recurrence_type}",
            recommendations=[
                f"预测值: {[f'{p:.2f}' for p in predictions[:3]]}",
                "递推关系可用于中短期预测"
            ]
        )
    
    def _comparative_reasoning(self, data: List[float],
                               analysis: SequenceAnalysis,
                               context: Dict[str, Any]) -> SequenceReasoningResult:
        """比较推理 - 对比不同数列模式"""
        
        # 计算各种模式的拟合度
        patterns = []
        
        # 等差
        arith = self.sequence_analyzer._check_arithmetic(data)
        if arith:
            patterns.append(("等差数列", arith.r_squared, arith.pattern_description))
        
        # 等比
        geo = self.sequence_analyzer._check_geometric(data)
        if geo:
            patterns.append(("等比数列", geo.r_squared, geo.pattern_description))
        
        # 斐波那契
        fib = self.sequence_analyzer._check_fibonacci(data)
        if fib:
            patterns.append(("斐波那契", fib.r_squared, fib.pattern_description))
        
        # 按拟合度排序
        patterns.sort(key=lambda x: x[1], reverse=True)
        
        best_pattern = patterns[0] if patterns else ("未知", 0, "")
        
        answer = f"最佳匹配: {best_pattern[0]} (R²={best_pattern[1]:.4f})\n"
        answer += f"描述: {best_pattern[2]}"
        
        recommendations = [
            f"数据显示{best_pattern[0]}characteristics",
            f"置信度: {best_pattern[1]*100:.1f}%"
        ]
        
        return SequenceReasoningResult(
            reasoning_id="",
            mode=SequenceReasoningMode.COMPARATIVE,
            input_data=data,
            context=context,
            success=True,
            answer=answer,
            confidence=best_pattern[1],
            mathematical_basis="多模式对比分析,选择最佳拟合模型",
            recommendations=recommendations
        )
    
    def _detect_period(self, data: List[float]) -> int:
        """检测周期(简化版)"""
        n = len(data)
        
        # 简化的周期检测:检查相邻差异的重复
        for period in range(2, n // 2):
            is_periodic = True
            for i in range(n - period):
                if abs(data[i] - data[i + period]) > 0.1 * abs(max(data) - min(data)):
                    is_periodic = False
                    break
            if is_periodic:
                return period
        
        return 0
    
    def _extract_trend(self, data: List[float]) -> List[float]:
        """提取趋势分量(简单移动平均)"""
        window = min(5, len(data) // 4)
        if window < 2:
            return data
        
        result = []
        for i in range(len(data)):
            start = max(0, i - window)
            end = min(len(data), i + window + 1)
            result.append(sum(data[start:end]) / (end - start))
        
        return result
    
    def _generate_trend_answer(self, data: List[float], 
                               prediction: TrendPrediction) -> str:
        """generate趋势答案"""
        latest = data[-1]
        next_val = prediction.short_term[0] if prediction.short_term else latest
        
        change = ((next_val - latest) / latest * 100) if latest != 0 else 0
        
        answer = f"当前值: {latest:.2f}\n"
        answer += f"预测下期: {next_val:.2f} ({change:+.1f}%)\n"
        answer += f"趋势类型: {prediction.pattern_description}\n"
        
        if prediction.doubling_time:
            answer += f"倍增时间: {prediction.doubling_time:.1f}期\n"
        
        return answer
    
    def _generate_trend_recommendations(self, prediction: TrendPrediction) -> List[str]:
        """generate趋势建议"""
        recommendations = []
        
        if prediction.pattern_type == SequenceType.ARITHMETIC:
            recommendations.append("线性增长,建议保持稳定strategy")
        elif prediction.pattern_type == SequenceType.GEOMETRIC:
            recommendations.append("指数增长,注意天花板效应")
        elif prediction.pattern_type == SequenceType.FIBONACCI:
            recommendations.append("斐波那契增长,健康的递进模式")
        
        if prediction.volatility > 0.2:
            recommendations.append("波动性较高,建议关注稳定性")
        
        return recommendations
    
    def batch_analyze(self, data_sets: Dict[str, List[float]]) -> Dict[str, TrendPrediction]:
        """
        批量分析多个数据序列
        
        Args:
            data_sets: 数据集字典 {"序列名": [数据序列]}
            
        Returns:
            分析结果字典
        """
        results = {}
        
        for name, data in data_sets.items():
            analysis = self.sequence_analyzer.analyze_sequence(data)
            short_term = self.sequence_analyzer.predict_future(data, 3)
            
            growth_rate = (data[-1] - data[0]) / data[0] if data[0] != 0 else 0
            
            results[name] = TrendPrediction(
                short_term=short_term,
                confidence=analysis.confidence,
                pattern_type=analysis.sequence_type,
                pattern_description=analysis.pattern_description,
                growth_rate=growth_rate
            )
        
        return results
    
    def compare_scenarios(self, scenarios: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        比较多个场景的增长趋势
        
        Args:
            scenarios: 场景字典 {"场景名": [数据序列]}
            
        Returns:
            比较分析结果
        """
        analyses = {}
        
        for name, data in scenarios.items():
            analysis = self.sequence_analyzer.analyze_sequence(data)
            short_term = self.sequence_analyzer.predict_future(data, 5)
            
            analyses[name] = {
                "pattern": analysis.sequence_type.value,
                "confidence": analysis.confidence,
                "latest": data[-1] if data else 0,
                "predicted_5": short_term[-1] if short_term else 0,
                "growth_rate": (data[-1] - data[0]) / data[0] if len(data) > 1 and data[0] != 0 else 0
            }
        
        # 找出最优场景
        best_scenario = max(analyses.items(), 
                          key=lambda x: x[1]["confidence"] * x[1]["growth_rate"])
        
        return {
            "analyses": analyses,
            "best_scenario": best_scenario[0],
            "recommendation": f"推荐场景: {best_scenario[0]}"
        }

# ==================== 导出 ====================

__all__ = [
    'SequenceReasoningEngine',
    'SequenceReasoningMode',
    'SequenceReasoningResult',
    'TrendPrediction',
    'CycleAnalysis',
    'ConvergenceAnalysis',
]
