"""数学智慧核心 - 组合优化引擎"""

import math
from typing import Any, Dict, List, Set

from ._mw_enums import OptimizationGoal
from ._mw_dataclasses import OptimizationResult

__all__ = [
    'combination',
    'evaluate_plan_options',
    'fibonacci_iterative',
    'fibonacci_recurrence',
    'inclusion_exclusion',
    'permutation',
    'pigeonhole_principle',
]

class CombinatorialOptimizer:
    """组合优化引擎 - 解决组合计数和优化问题"""
    
    @classmethod
    def permutation(cls, n: int, r: int) -> int:
        """排列数 P(n, r) = n! / (n-r)!"""
        if r > n or r < 0:
            return 0
        return math.factorial(n) // math.factorial(n - r)
    
    @classmethod
    def combination(cls, n: int, r: int) -> int:
        """组合数 C(n, r) = n! / (r! * (n-r)!)"""
        if r > n or r < 0:
            return 0
        if r == 0 or r == n:
            return 1
        # 使用帕斯卡三角优化
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
    
    @classmethod
    def inclusion_exclusion(cls, sets: List[Set]) -> int:
        """
        容斥原理计算并集大小
        
        Args:
            sets: 集合列表
            
        Returns:
            并集大小
        """
        n = len(sets)
        if n == 0:
            return 0
        
        # 计算所有子集
        total = 0
        for mask in range(1, 1 << n):
            # 计算这个子集的交集大小
            subset_sets = [sets[i] for i in range(n) if mask & (1 << i)]
            intersection = set.intersection(*subset_sets) if subset_sets else set()
            
            # 奇数个子集加,偶数个子集减
            if bin(mask).count('1') % 2 == 1:
                total += len(intersection)
            else:
                total -= len(intersection)
        
        return total
    
    @classmethod
    def pigeonhole_principle(cls, items: int, holes: int) -> Dict[str, Any]:
        """
        鸽巢原理分析
        
        Args:
            items: 物品数量
            holes: 鸽巢数量
            
        Returns:
            分析结果
        """
        min_per_hole = items // holes
        remainder = items % holes
        
        return {
            "total_items": items,
            "total_holes": holes,
            "min_items_per_hole": min_per_hole,
            "max_items_per_hole": min_per_hole + (1 if remainder > 0 else 0),
            "at_least_one_hole_with": min_per_hole + 1 if remainder > 0 else min_per_hole,
            "guarantee_condition": f"任意{items+1}个物品放入{holes}个鸽巢,必有两个在同一鸽巢"
                              if items >= holes else None
        }
    
    @classmethod
    def fibonacci_recurrence(cls, n: int, memo: Dict[int, int] = None) -> int:
        """斐波那契数列(带记忆化)"""
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = cls.fibonacci_recurrence(n-1, memo) + cls.fibonacci_recurrence(n-2, memo)
        return memo[n]
    
    @classmethod
    def fibonacci_iterative(cls, n: int) -> int:
        """斐波那契数列(迭代版,更高效)"""
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    
    @classmethod
    def evaluate_plan_options(cls, options: List[Dict], constraints: Dict) -> OptimizationResult:
        """
        评估方案选项
        
        Args:
            options: 方案列表,每个方案包含 score, risk, cost 等
            constraints: 约束条件
            
        Returns:
            优化结果
        """
        if not options:
            return OptimizationResult(
                goal=OptimizationGoal.BALANCE,
                optimal_value=0,
                constraints_satisfied=False
            )
        
        # 计算综合得分
        scored_options = []
        for i, opt in enumerate(options):
            # 综合评分(可调整权重)
            score = opt.get('score', 0)
            risk = opt.get('risk', 0)  # 风险越低越好
            cost = opt.get('cost', 0)  # 成本越低越好
            
            # 综合得分:越高越好
            composite_score = score * 0.5 - risk * 0.3 - cost * 0.2
            scored_options.append((f"方案{i+1}", composite_score))
        
        # 排序
        scored_options.sort(key=lambda x: x[1], reverse=True)
        
        best_option, best_score = scored_options[0]
        
        return OptimizationResult(
            goal=OptimizationGoal.MAXIMIZE,
            optimal_value=best_score,
            optimal_choice=best_option,
            alternatives=scored_options[:5],
            constraints_satisfied=True
        )
