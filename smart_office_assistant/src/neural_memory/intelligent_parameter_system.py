"""
__all__ = [
    'adjust_parameters',
    'evaluate',
    'get_adjustment_summary',
    'record_learning_result',
    'should_trigger',
]

智能参数调整系统 - Intelligent Parameter Adjustment System
根据学习洞察自动调整参数,实现持续优化

核心机制:
1. 参数监控 - 跟踪所有执行参数
2. 效能评估 - 评估参数的实际效果
3. 反馈学习 - 根据结果反馈调整参数
4. 约束管理 - 保证参数在合理范围内
5. 版本历史 - 记录参数演进

参数调整维度:
- 阈值调整 (Threshold Tuning)
- 权重优化 (Weight Optimization)
- 目标调整 (Target Adjustment)
- 质量标准 (Quality Standard)
- 时间配置 (Time Configuration)
"""

import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging
import math

logger = logging.getLogger(__name__)

class ParameterType(Enum):
    """参数类型"""
    THRESHOLD = "阈值"       # 触发阈值
    WEIGHT = "权重"         # 优先级权重
    TARGET = "目标"         # 学习目标
    QUALITY = "质量"        # 质量标准
    TIME = "时间"           # 时间限制

class AdjustmentDirection(Enum):
    """调整方向"""
    INCREASE = "增加"       # 向上调整
    DECREASE = "减少"       # 向下调整
    STABILIZE = "稳定"      # 保持稳定
    OPTIMIZE = "优化"       # 优化

@dataclass
class ParameterSnapshot:
    """参数快照"""
    timestamp: datetime
    parameters: Dict[str, Any]
    performance_metrics: Dict[str, float]
    source: str                           # 来源 (manual/auto/system)
    notes: Optional[str] = None

@dataclass
class ParameterHistory:
    """参数历史"""
    parameter_name: str
    old_value: Any
    new_value: Any
    adjusted_at: datetime
    reason: str                           # 调整原因
    direction: AdjustmentDirection
    impact: Optional[str] = None          # 调整影响
    session_id: Optional[str] = None      # 关联的学习会话

@dataclass
class PerformanceMetrics:
    """性能metrics"""
    # 数据相关
    data_points_collected: int            # 收集数据点数
    valid_data_ratio: float               # 有效数据比例
    average_quality: float                # 平均质量分
    authority_distribution: Dict[str, float]  # 权威性分布
    
    # 学习相关
    patterns_discovered: int              # 发现模式数
    insights_generated: int               # generate洞察数
    learning_effectiveness: float         # 学习效率
    
    # 资源相关
    execution_time: float                 # 执行时间 (秒)
    resource_efficiency: float            # 资源效率
    error_rate: float                     # 错误率
    
    # synthesize
    overall_score: float                  # synthesize评分 (0-1)
    satisfaction_level: str               # 满意度 (poor/fair/good/excellent)

class PerformanceEvaluator:
    """性能评估器"""
    
    @staticmethod
    def evaluate(learning_results: Dict[str, Any]) -> PerformanceMetrics:
        """
        评估学习性能
        
        Args:
            learning_results: 学习结果
                - data_points: 收集的数据点列表
                - execution_time: 执行时间
                - errors: 错误列表
                - patterns: 发现的模式
                - insights: generate的洞察
                
        Returns:
            性能metrics
        """
        data_points = learning_results.get("data_points", [])
        patterns = learning_results.get("patterns", [])
        insights = learning_results.get("insights", [])
        exec_time = learning_results.get("execution_time", 0)
        errors = learning_results.get("errors", [])
        
        # 计算数据相关metrics
        total_points = len(data_points)
        valid_points = len([p for p in data_points if p.get("has_source", True)])
        valid_ratio = valid_points / total_points if total_points > 0 else 0
        avg_quality = sum(p.get("quality", 0.5) for p in data_points) / total_points if total_points > 0 else 0
        
        # 权威性分布
        authority_dist = {}
        for p in data_points:
            auth = p.get("authority", "general")
            authority_dist[auth] = authority_dist.get(auth, 0) + 1
        
        # 学习相关metrics
        patterns_count = len(patterns)
        insights_count = len(insights)
        learning_efficiency = (patterns_count + insights_count) / max(1, exec_time) * 100
        
        # 资源相关metrics
        error_rate = len(errors) / max(1, exec_time)
        resource_efficiency = (valid_ratio * avg_quality) / max(1, exec_time / 100)
        
        # synthesize评分
        overall = (
            valid_ratio * 0.3 +           # 数据有效性 30%
            avg_quality * 0.25 +          # 数据质量 25%
            min(1.0, learning_efficiency / 10) * 0.2 +  # 学习效率 20%
            (1 - min(1.0, error_rate)) * 0.15 +  # 错误率 15%
            min(1.0, resource_efficiency / 100) * 0.1   # 资源效率 10%
        )
        
        # 满意度等级
        if overall >= 0.85:
            satisfaction = "excellent"
        elif overall >= 0.70:
            satisfaction = "good"
        elif overall >= 0.55:
            satisfaction = "fair"
        else:
            satisfaction = "poor"
        
        return PerformanceMetrics(
            data_points_collected=total_points,
            valid_data_ratio=valid_ratio,
            average_quality=avg_quality,
            authority_distribution=authority_dist,
            patterns_discovered=patterns_count,
            insights_generated=insights_count,
            learning_effectiveness=learning_efficiency,
            execution_time=exec_time,
            resource_efficiency=resource_efficiency,
            error_rate=error_rate,
            overall_score=overall,
            satisfaction_level=satisfaction,
        )

class ParameterAdjustmentRule:
    """参数调整规则"""
    
    def __init__(self,
                 parameter_name: str,
                 metric_trigger: Tuple[str, float, str],  # (metric, threshold, condition)
                 adjustment: Tuple[AdjustmentDirection, float, Tuple[float, float]],  # (direction, magnitude, bounds)
                 priority: int = 1):
        """
        init调整规则
        
        Args:
            parameter_name: 参数名称
            metric_trigger: (metrics名, 阈值, 条件) - 条件: gt/lt/eq
            adjustment: (方向, 幅度, 范围)
            priority: 优先级 (1=高)
        """
        self.parameter_name = parameter_name
        self.metric_name = metric_trigger[0]
        self.trigger_threshold = metric_trigger[1]
        self.trigger_condition = metric_trigger[2]  # "gt", "lt", "eq"
        
        self.direction = adjustment[0]
        self.magnitude = adjustment[1]
        self.min_bound, self.max_bound = adjustment[2]
        self.priority = priority
    
    def should_trigger(self, metrics: Dict[str, float]) -> bool:
        """检查是否应该触发调整"""
        metric_value = metrics.get(self.metric_name, 0)
        
        if self.trigger_condition == "gt":
            return metric_value > self.trigger_threshold
        elif self.trigger_condition == "lt":
            return metric_value < self.trigger_threshold
        elif self.trigger_condition == "eq":
            return abs(metric_value - self.trigger_threshold) < 0.01
        
        return False

class ParameterAdjustmentSystem:
    """智能参数调整系统"""
    
    def __init__(self):
        """init系统"""
        self.current_parameters: Dict[str, Any] = {}
        self.parameter_history: List[ParameterHistory] = []
        self.performance_snapshots: List[ParameterSnapshot] = []
        self.adjustment_rules: List[ParameterAdjustmentRule] = []
        self.parameter_constraints: Dict[str, Tuple[float, float]] = {}
        
        # init默认规则
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """init默认调整规则"""
        self.adjustment_rules = [
            # 如果数据质量很高,降低阈值
            ParameterAdjustmentRule(
                "local_data_threshold",
                ("average_quality", 0.85, "gt"),
                (AdjustmentDirection.DECREASE, 0.2, (1, 10)),
                priority=1
            ),
            
            # 如果有效数据比例低,增加网络目标
            ParameterAdjustmentRule(
                "network_data_target",
                ("valid_data_ratio", 0.70, "lt"),
                (AdjustmentDirection.INCREASE, 1.3, (3, 30)),
                priority=1
            ),
            
            # 如果学习效率低,增加执行时间
            ParameterAdjustmentRule(
                "max_execution_time",
                ("learning_effectiveness", 2.0, "lt"),
                (AdjustmentDirection.INCREASE, 1.2, (60, 2400)),
                priority=2
            ),
            
            # 如果错误率高,降低网络数据目标
            ParameterAdjustmentRule(
                "network_data_target",
                ("error_rate", 0.05, "gt"),
                (AdjustmentDirection.DECREASE, 0.8, (3, 30)),
                priority=2
            ),
            
            # 如果资源效率高,增加广度
            ParameterAdjustmentRule(
                "research_breadth",
                ("resource_efficiency", 5.0, "gt"),
                (AdjustmentDirection.INCREASE, 1.1, (0.5, 2.0)),
                priority=3
            ),
        ]
        
        # 设置参数约束
        self.parameter_constraints = {
            "local_data_threshold": (1, 20),
            "network_data_target": (3, 50),
            "cross_trigger_threshold": (1, 15),
            "data_quality_threshold": (0.3, 0.95),
            "max_execution_time": (60, 3600),
            "local_priority_weight": (0.0, 1.0),
            "network_priority_weight": (0.0, 1.0),
        }
    
    def record_learning_result(self,
                               results: Dict[str, Any],
                               current_params: Dict[str, Any]) -> PerformanceMetrics:
        """记录学习结果并评估性能"""
        metrics = PerformanceEvaluator.evaluate(results)
        
        # 保存快照
        snapshot = ParameterSnapshot(
            timestamp=datetime.now(),
            parameters=current_params.copy(),
            performance_metrics={
                "data_points": metrics.data_points_collected,
                "valid_ratio": metrics.valid_data_ratio,
                "avg_quality": metrics.average_quality,
                "patterns": metrics.patterns_discovered,
                "insights": metrics.insights_generated,
                "efficiency": metrics.learning_effectiveness,
                "exec_time": metrics.execution_time,
                "overall_score": metrics.overall_score,
            },
            source="learning_execution",
        )
        self.performance_snapshots.append(snapshot)
        
        logger.info(f"学习结果记录: 性能评分 {metrics.overall_score:.2f} ({metrics.satisfaction_level})")
        
        return metrics
    
    def adjust_parameters(self,
                         current_params: Dict[str, Any],
                         metrics: PerformanceMetrics,
                         aggressive: bool = False) -> Tuple[Dict[str, Any], List[ParameterHistory]]:
        """
        根据性能metrics调整参数
        
        Args:
            current_params: 当前参数
            metrics: 性能metrics
            aggressive: 是否使用激进调整
            
        Returns:
            (调整后的参数, 调整历史)
        """
        adjusted_params = current_params.copy()
        adjustments = []
        
        # 将metrics转换为字典格式
        metrics_dict = {
            "average_quality": metrics.average_quality,
            "valid_data_ratio": metrics.valid_data_ratio,
            "learning_effectiveness": metrics.learning_effectiveness,
            "error_rate": metrics.error_rate,
            "resource_efficiency": metrics.resource_efficiency,
        }
        
        # 按优先级处理规则
        triggered_rules = []
        for rule in self.adjustment_rules:
            if rule.should_trigger(metrics_dict):
                triggered_rules.append(rule)
        
        # 排序 (优先级从高到低)
        triggered_rules.sort(key=lambda r: r.priority)
        
        # 执行调整
        for rule in triggered_rules:
            old_value = adjusted_params.get(rule.parameter_name)
            
            if old_value is None:
                continue
            
            # 计算新值
            new_value = self._calculate_adjusted_value(
                old_value,
                rule.direction,
                rule.magnitude,
                aggressive
            )
            
            # 应用约束
            if rule.parameter_name in self.parameter_constraints:
                min_val, max_val = self.parameter_constraints[rule.parameter_name]
                new_value = max(min_val, min(max_val, new_value))
            
            # 只有在值改变时才记录
            if new_value != old_value:
                adjusted_params[rule.parameter_name] = new_value
                
                adjustment = ParameterHistory(
                    parameter_name=rule.parameter_name,
                    old_value=old_value,
                    new_value=new_value,
                    adjusted_at=datetime.now(),
                    reason=f"metrics {rule.metric_name} = {metrics_dict.get(rule.metric_name, 0):.2f} "
                           f"{'>' if rule.trigger_condition == 'gt' else '<' if rule.trigger_condition == 'lt' else '='} "
                           f"{rule.trigger_threshold}",
                    direction=rule.direction,
                )
                adjustments.append(adjustment)
                self.parameter_history.append(adjustment)
                
                logger.info(f"参数调整: {rule.parameter_name} "
                           f"{old_value} → {new_value} ({rule.direction.value})")
        
        return adjusted_params, adjustments
    
    def _calculate_adjusted_value(self,
                                 current_value: Any,
                                 direction: AdjustmentDirection,
                                 magnitude: float,
                                 aggressive: bool) -> Any:
        """计算调整后的值"""
        if isinstance(current_value, (int, float)):
            if direction == AdjustmentDirection.INCREASE:
                adjustment = magnitude
                if aggressive:
                    adjustment *= 1.5
                return current_value * adjustment
            
            elif direction == AdjustmentDirection.DECREASE:
                adjustment = magnitude
                if aggressive:
                    adjustment *= 1.5
                return current_value / adjustment
            
            else:
                return current_value
        
        elif isinstance(current_value, str):
            # 字符串参数的调整 (如研究深度)
            depth_levels = ["shallow", "medium", "deep"]
            if current_value in depth_levels:
                current_idx = depth_levels.index(current_value)
                
                if direction == AdjustmentDirection.INCREASE:
                    new_idx = min(len(depth_levels) - 1, current_idx + 1)
                elif direction == AdjustmentDirection.DECREASE:
                    new_idx = max(0, current_idx - 1)
                else:
                    new_idx = current_idx
                
                return depth_levels[new_idx]
        
        return current_value
    
    def get_adjustment_summary(self) -> Dict:
        """get调整总结"""
        if not self.parameter_history:
            return {"adjustments_count": 0, "message": "暂无参数调整"}
        
        # 统计调整类型
        direction_count = {}
        for adj in self.parameter_history:
            direction = adj.direction.value
            direction_count[direction] = direction_count.get(direction, 0) + 1
        
        # 统计被调整最多的参数
        param_count = {}
        for adj in self.parameter_history:
            param = adj.parameter_name
            param_count[param] = param_count.get(param, 0) + 1
        
        most_adjusted = max(param_count.items(), key=lambda x: x[1]) if param_count else None
        
        return {
            "total_adjustments": len(self.parameter_history),
            "adjustment_directions": direction_count,
            "most_adjusted_parameter": most_adjusted[0] if most_adjusted else None,
            "adjustment_frequency": most_adjusted[1] if most_adjusted else 0,
            "latest_adjustment": {
                "parameter": self.parameter_history[-1].parameter_name,
                "from": self.parameter_history[-1].old_value,
                "to": self.parameter_history[-1].new_value,
                "timestamp": self.parameter_history[-1].adjusted_at.isoformat(),
            } if self.parameter_history else None,
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
