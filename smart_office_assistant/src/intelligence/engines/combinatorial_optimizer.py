"""
组合优化评估模块 - Combinatorial Optimization & Evaluation Module
============================================================

基于组合数学的方案评估与优化decision引擎

v6.0.0 新增功能:
- 排列组合计算:P(n,r), C(n,r), 多重集排列
- 容斥原理:复杂集合运算,约束满足
- 鸽巢原理:下界估计,保证性分析
- 斐波那契应用:递推优化,黄金分割decision
- 方案评估:多目标优化,约束规划

核心能力:
1. 组合计数 - 精确计算可行方案数
2. 约束分析 - 基于容斥原理的约束处理
3. 下界估计 - 鸽巢原理的性能下界
4. 方案排序 - 多准则decision分析
"""

import math
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from itertools import combinations, permutations
import numpy as np

class EvaluationMetric(Enum):
    """评估metrics"""
    SCORE = "score"                     # synthesize得分
    RISK = "risk"                       # 风险评估
    COST = "cost"                       # 成本
    TIME = "time"                       # 时间
    QUALITY = "quality"                 # 质量
    SATISFACTION = "satisfaction"       # 满意度

class ConstraintType(Enum):
    """约束类型"""
    HARD = "hard"                       # 硬约束(必须满足)
    SOFT = "soft"                       # 软约束(尽量满足)
    OPTIONAL = "optional"                # 可选约束

@dataclass
class PlanOption:
    """方案选项"""
    id: str
    name: str
    description: str
    
    # 多维度评估
    metrics: Dict[EvaluationMetric, float] = field(default_factory=dict)
    
    # 约束满足情况
    constraints_satisfied: Dict[str, bool] = field(default_factory=dict)
    constraint_score: float = 1.0  # 约束满足度 0-1
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CombinationAnalysis:
    """组合分析结果"""
    total_combinations: int = 0          # 总组合数
    valid_combinations: int = 0          # 有效组合数
    
    # 计数分析
    permutation_count: int = 0
    combination_count: int = 0
    
    # 约束分析
    constraint_satisfying: int = 0        # 满足约束的数量
    constraint_violating: int = 0        # 违反约束的数量
    
    # 概率分析
    success_probability: float = 0.0
    
    # 边界
    upper_bound: Optional[int] = None    # 上界
    lower_bound: Optional[int] = None    # 下界

@dataclass
class EvaluationResult:
    """评估结果"""
    plan: PlanOption
    
    # synthesize评分
    overall_score: float = 0.0
    
    # 分项得分
    component_scores: Dict[str, float] = field(default_factory=dict)
    
    # 排名
    rank: int = 0
    percentile: float = 0.0
    
    # 评估详情
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

@dataclass
class OptimizationResult:
    """优化结果"""
    optimal_plan: Optional[PlanOption] = None
    optimal_score: float = 0.0
    
    # 所有方案排名
    rankings: List[EvaluationResult] = field(default_factory=list)
    
    # 优化分析
    analysis: CombinationAnalysis = None
    
    # 建议
    recommendations: List[str] = field(default_factory=list)
    
    # 风险评估
    risk_assessment: Dict[str, float] = field(default_factory=dict)

class CombinatorialOptimizer:
    """
    组合优化评估引擎
    
    提供基于组合数学的方案评估和优化decision能力
    """
    
    # 黄金分割常数
    GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
    
    @classmethod
    def permutation_count(cls, n: int, r: int = None) -> int:
        """
        排列数计算
        
        P(n, r) = n! / (n-r)!
        
        Args:
            n: 总元素数
            r: 选取元素数,默认全部
            
        Returns:
            排列数
        """
        if r is None:
            r = n
        if r > n or n < 0 or r < 0:
            return 0
        return math.factorial(n) // math.factorial(n - r)
    
    @classmethod
    def combination_count(cls, n: int, r: int) -> int:
        """
        组合数计算
        
        C(n, r) = n! / (r! × (n-r)!)
        
        Args:
            n: 总元素数
            r: 选取元素数
            
        Returns:
            组合数
        """
        if r > n or n < 0 or r < 0:
            return 0
        if r == 0 or r == n:
            return 1
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
    
    @classmethod
    def multinomial_coefficient(cls, n: int, *parts: int) -> int:
        """
        多项式系数
        
        C(n; k1, k2, ..., km) = n! / (k1! × k2! × ... × km!)
        
        Args:
            n: 总数
            *parts: 各部分数量
            
        Returns:
            多项式系数
        """
        if sum(parts) != n:
            return 0
        return math.factorial(n) // math.prod(math.factorial(k) for k in parts)
    
    @classmethod
    def inclusion_exclusion_count(cls, sets: List[Set]) -> int:
        """
        容斥原理计算并集大小
        
        |A₁ ∪ A₂ ∪ ... ∪ Aₙ| = Σ|Aᵢ| - Σ|Aᵢ ∩ Aⱼ| + Σ|Aᵢ ∩ Aⱼ ∩ Aₖ| - ...
        
        Args:
            sets: 集合列表
            
        Returns:
            并集大小
        """
        n = len(sets)
        if n == 0:
            return 0
        
        total = 0
        
        # 遍历所有非空子集
        for mask in range(1, 1 << n):
            # 计算子集中的元素
            subset_sets = [sets[i] for i in range(n) if mask & (1 << i)]
            intersection = set.intersection(*subset_sets)
            
            # 加或减
            bits = bin(mask).count('1')
            if bits % 2 == 1:
                total += len(intersection)
            else:
                total -= len(intersection)
        
        return total
    
    @classmethod
    def pigeonhole_estimate(cls, n_items: int, n_holes: int, guarantee: float = 1.0) -> Dict[str, Any]:
        """
        鸽巢原理估计
        
        Args:
            n_items: 物品数
            n_holes: 鸽巢数
            guarantee: 保证概率(0-1)
            
        Returns:
            估计结果
        """
        base_per_hole = n_items // n_holes
        remainder = n_items % n_holes
        
        return {
            "minimum_items_per_hole": base_per_hole,
            "maximum_items_per_hole": base_per_hole + (1 if remainder > 0 else 0),
            "holes_with_extra": remainder,
            "items_needed_for_guarantee": n_holes + 1,  # n+1个物品放入n个巢
            "guaranteed_collision": n_items > n_holes
        }
    
    @classmethod
    def fibonacci_growth(cls, n: int, a1: float = 1, a2: float = 1) -> float:
        """
        斐波那契数列计算
        
        Fₙ = Fₙ₋₁ + Fₙ₋₂
        
        Args:
            n: 项数
            a1: 第一项
            a2: 第二项
            
        Returns:
            第n项的值
        """
        if n <= 0:
            return 0
        if n == 1:
            return a1
        if n == 2:
            return a2
        
        a, b = a1, a2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b
    
    @classmethod
    def golden_ratio_decision(cls, option1: Tuple[str, float], 
                              option2: Tuple[str, float]) -> Dict[str, Any]:
        """
        黄金分割decision
        
        使用黄金分割比例进行两难抉择
        
        Args:
            option1: (选项名, 得分)
            option2: (选项名, 得分)
            
        Returns:
            decision结果
        """
        name1, score1 = option1
        name2, score2 = option2
        
        total = score1 + score2
        if total == 0:
            return {"decision": "平局", "ratio": 0.5}
        
        ratio1 = score1 / total
        
        # 黄金分割点
        golden_point = 1 / cls.GOLDEN_RATIO
        
        if ratio1 > golden_point:
            decision = name1
            confidence = (ratio1 - golden_point) / (1 - golden_point)
        else:
            decision = name2
            confidence = (golden_point - ratio1) / golden_point
        
        return {
            "decision": decision,
            "confidence": confidence,
            "score_ratio": ratio1,
            "golden_point": golden_point,
            "recommendation": f"推荐{decision},置信度{confidence:.1%}"
        }
    
    @classmethod
    def evaluate_plan(cls, plan: PlanOption, 
                     weights: Dict[EvaluationMetric, float] = None,
                     constraints: List[Tuple[str, Callable]] = None) -> EvaluationResult:
        """
        评估单个方案
        
        Args:
            plan: 方案
            weights: metrics权重
            constraints: 约束条件列表
            
        Returns:
            评估结果
        """
        if weights is None:
            weights = {
                EvaluationMetric.SCORE: 0.4,
                EvaluationMetric.RISK: 0.2,
                EvaluationMetric.COST: 0.2,
                EvaluationMetric.QUALITY: 0.2
            }
        
        # 计算分项得分
        component_scores = {}
        for metric, weight in weights.items():
            score = plan.metrics.get(metric, 0)
            component_scores[metric.value] = score * weight
        
        # synthesize得分
        overall_score = sum(component_scores.values())
        
        # 约束满足度调整
        constraint_score = plan.constraint_score
        overall_score *= constraint_score
        
        # recognize优缺点
        strengths = []
        weaknesses = []
        warnings = []
        
        for metric, score in plan.metrics.items():
            if score > 0.8:
                strengths.append(f"{metric.value}表现优秀({score:.1%})")
            elif score < 0.4:
                weaknesses.append(f"{metric.value}需要提升({score:.1%})")
        
        # 检查约束警告
        for name, satisfied in plan.constraints_satisfied.items():
            if not satisfied:
                warnings.append(f"未满足约束: {name}")
        
        return EvaluationResult(
            plan=plan,
            overall_score=overall_score,
            component_scores=component_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            warnings=warnings
        )
    
    @classmethod
    def optimize_plans(cls, plans: List[PlanOption],
                      weights: Dict[EvaluationMetric, float] = None,
                      top_k: int = None) -> OptimizationResult:
        """
        优化方案选择
        
        Args:
            plans: 方案列表
            weights: metrics权重
            top_k: 返回前k个方案
            
        Returns:
            优化结果
        """
        if not plans:
            return OptimizationResult(recommendations=["无可用方案"])
        
        # 评估每个方案
        evaluations = []
        for plan in plans:
            eval_result = cls.evaluate_plan(plan, weights)
            evaluations.append(eval_result)
        
        # 排序
        evaluations.sort(key=lambda x: x.overall_score, reverse=True)
        
        # 设置排名
        for i, eval_result in enumerate(evaluations):
            eval_result.rank = i + 1
            eval_result.percentile = (len(evaluations) - i) / len(evaluations)
        
        # 组合分析
        analysis = CombinationAnalysis(
            total_combinations=len(plans),
            valid_combinations=len([e for e in evaluations if e.overall_score > 0]),
            constraint_satisfying=len([p for p in plans if p.constraint_score > 0.8]),
            constraint_violating=len([p for p in plans if p.constraint_score < 0.5])
        )
        
        # generate建议
        recommendations = []
        if evaluations:
            best = evaluations[0]
            recommendations.append(f"最优方案: {best.plan.name},得分{best.overall_score:.2f}")
            
            if best.weaknesses:
                recommendations.append(f"改进方向: {', '.join(best.weaknesses[:2])}")
        
        # 风险评估
        risk_assessment = {
            "average_score": np.mean([e.overall_score for e in evaluations]),
            "score_variance": np.var([e.overall_score for e in evaluations]),
            "best_vs_worst_gap": evaluations[0].overall_score - evaluations[-1].overall_score if evaluations else 0
        }
        
        return OptimizationResult(
            optimal_plan=evaluations[0].plan if evaluations else None,
            optimal_score=evaluations[0].overall_score if evaluations else 0,
            rankings=evaluations[:top_k] if top_k else evaluations,
            analysis=analysis,
            recommendations=recommendations,
            risk_assessment=risk_assessment
        )
    
    @classmethod
    def sensitivity_analysis(cls, plan: PlanOption,
                            metric_changes: Dict[EvaluationMetric, float]) -> Dict[str, float]:
        """
        敏感性分析
        
        分析各metrics变化对synthesize得分的影响
        
        Args:
            plan: 方案
            metric_changes: metrics变化量(百分比)
            
        Returns:
            敏感性分析结果
        """
        base_score = sum(plan.metrics.values()) / len(plan.metrics)
        sensitivities = {}
        
        for metric, change_pct in metric_changes.items():
            original = plan.metrics.get(metric, 0)
            new = original * (1 + change_pct)
            
            # 假设等权重
            new_avg = (sum(plan.metrics.values()) - original + new) / len(plan.metrics)
            
            sensitivities[metric.value] = (new_avg - base_score) / base_score if base_score > 0 else 0
        
        return sensitivities
    
    @classmethod
    def scenario_analysis(cls, base_plan: PlanOption,
                         scenarios: Dict[str, Dict[EvaluationMetric, float]]) -> Dict[str, OptimizationResult]:
        """
        场景分析
        
        分析不同场景下的方案表现
        
        Args:
            base_plan: 基础方案
            scenarios: 场景字典 {场景名: {metrics: 值}}
            
        Returns:
            各场景分析结果
        """
        results = {}
        
        for scenario_name, metric_overrides in scenarios.items():
            # 创建场景方案
            scenario_plan = PlanOption(
                id=base_plan.id + f"_{scenario_name}",
                name=f"{base_plan.name}_{scenario_name}",
                description=base_plan.description,
                metrics={**base_plan.metrics, **metric_overrides}
            )
            
            # 评估
            eval_result = cls.evaluate_plan(scenario_plan)
            results[scenario_name] = OptimizationResult(
                optimal_plan=scenario_plan,
                optimal_score=eval_result.overall_score,
                rankings=[eval_result],
                recommendations=[f"场景{scenario_name}得分: {eval_result.overall_score:.2f}"]
            )
        
        return results
    
    @classmethod
    def resource_allocation_optimize(cls, resources: Dict[str, float],
                                    tasks: List[Tuple[str, Dict[str, float]]],
                                    objective: str = "max") -> Dict[str, Any]:
        """
        资源分配优化(简化版)
        
        Args:
            resources: 可用资源 {资源名: 数量}
            tasks: 任务列表 [(任务名, {所需资源: 数量})]
            objective: "max"最大化任务数,"min"最小化资源使用
            
        Returns:
            分配结果
        """
        if objective == "max":
            # 贪心选择能完成的任务
            allocated = []
            remaining = resources.copy()
            
            for task_name, requirements in sorted(tasks, key=lambda x: sum(x[1].values())):
                can_allocate = True
                for resource, amount in requirements.items():
                    if remaining.get(resource, 0) < amount:
                        can_allocate = False
                        break
                
                if can_allocate:
                    allocated.append(task_name)
                    for resource, amount in requirements.items():
                        remaining[resource] -= amount
            
            return {
                "allocated_tasks": allocated,
                "task_count": len(allocated),
                "remaining_resources": remaining,
                "utilization": sum(sum(t[1].values()) for t in tasks) / sum(resources.values())
            }
        
        return {"allocated_tasks": [], "task_count": 0}

# ==================== 辅助函数 ====================

def calculate_entropy(probabilities: List[float]) -> float:
    """
    计算信息熵
    
    H = -Σ p(x) × log₂(p(x))
    """
    h = 0.0
    for p in probabilities:
        if p > 0:
            h -= p * math.log2(p)
    return h

def calculate_gini_impurity(probabilities: List[float]) -> float:
    """
    计算基尼不纯度
    
    G = 1 - Σ p(x)²
    """
    return 1 - sum(p ** 2 for p in probabilities)

def calculate_information_gain(parent_probs: List[float],
                               children_probs: List[List[float]]) -> float:
    """
    计算信息增益
    
    IG = H(parent) - Σ wᵢ × H(childᵢ)
    """
    parent_entropy = calculate_entropy(parent_probs)
    
    total_samples = sum(sum(p) for p in children_probs)
    
    weighted_entropy = 0.0
    for child in children_probs:
        if sum(child) > 0:
            child_probs = [p / sum(child) for p in child]
            weight = sum(child) / total_samples
            weighted_entropy += weight * calculate_entropy(child_probs)
    
    return parent_entropy - weighted_entropy

# ==================== 导出 ====================

__all__ = [
    'CombinatorialOptimizer',
    'PlanOption',
    'CombinationAnalysis',
    'EvaluationMetric',
    'EvaluationResult',
    'OptimizationResult',
    'ConstraintType',
    'calculate_entropy',
    'calculate_gini_impurity',
    'calculate_information_gain',
]
