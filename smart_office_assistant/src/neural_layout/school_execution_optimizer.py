"""
__all__ = [
    'get_optimization_stats',
    'get_school_execution_optimizer',
    'optimize',
]

学派层输出 → 执行层优化模块

将智慧学派的输出转化为优化的执行策略
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio

class SchoolType(Enum):
    """智慧学派类型"""
    CONFUCIAN = "CONFUCIAN"           # 儒家
    TAOIST = "TAOIST"                 # 道家
    BUDDHIST = "BUDDHIST"             # 佛家
    SUNZI = "SUNZI"                   # 孙子兵法
    SUFU = "SUFU"                     # 素书
    YANGMING = "YANGMING"             # 王阳明心学
    DEWEY = "DEWEY"                   # 杜威反省思维
    TOP_METHODS = "TOP_METHODS"       # 顶级思维法
    PSYCHOLOGY = "PSYCHOLOGY"         # 心理营销
    SCIENCE = "SCIENCE"               # 自然科学

class ExecutionStrategy(Enum):
    """执行策略类型"""
    SEQUENTIAL = "sequential"         # 顺序执行
    PARALLEL = "parallel"             # 并行执行
    ADAPTIVE = "adaptive"             # 自适应执行
    ITERATIVE = "iterative"           # 迭代执行

@dataclass
class SchoolOutput:
    """学派输出"""
    school: SchoolType
    recommendation: str
    confidence: float
    action_items: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

@dataclass
class OptimizedExecutionPlan:
    """优化的执行计划"""
    plan_id: str
    original_schools: List[SchoolType]
    execution_strategy: ExecutionStrategy
    steps: List[Dict]
    estimated_success_rate: float
    risk_assessment: Dict
    created_at: datetime = field(default_factory=datetime.now)

class SchoolExecutionOptimizer:
    """
    学派执行优化器
    
    将多个智慧学派的输出融合为优化的执行计划：
    1. 学派输出解析与标准化
    2. 多学派融合决策
    3. 执行策略生成
    4. 风险评估与缓解
    """
    
    # 学派特征映射
    SCHOOL_CHARACTERISTICS = {
        SchoolType.CONFUCIAN: {
            "strengths": ["伦理决策", "关系协调", "长期规划"],
            "execution_style": "SEQUENTIAL",
            "risk_tolerance": "low"
        },
        SchoolType.TAOIST: {
            "strengths": ["顺势而为", "灵活应变", "资源优化"],
            "execution_style": "ADAPTIVE",
            "risk_tolerance": "medium"
        },
        SchoolType.BUDDHIST: {
            "strengths": ["内心平静", "专注当下", "情绪管理"],
            "execution_style": "SEQUENTIAL",
            "risk_tolerance": "low"
        },
        SchoolType.SUNZI: {
            "strengths": ["战略规划", "竞争分析", "战术执行"],
            "execution_style": "ADAPTIVE",
            "risk_tolerance": "high"
        },
        SchoolType.SUFU: {
            "strengths": ["道德判断", "人才识别", "危机预警"],
            "execution_style": "SEQUENTIAL",
            "risk_tolerance": "low"
        },
        SchoolType.YANGMING: {
            "strengths": ["知行合一", "良知判断", "实践导向"],
            "execution_style": "ITERATIVE",
            "risk_tolerance": "medium"
        },
        SchoolType.DEWEY: {
            "strengths": ["反思迭代", "经验学习", "问题解决"],
            "execution_style": "ITERATIVE",
            "risk_tolerance": "medium"
        },
        SchoolType.TOP_METHODS: {
            "strengths": ["第一性原理", "系统思维", "模型应用"],
            "execution_style": "PARALLEL",
            "risk_tolerance": "high"
        },
        SchoolType.PSYCHOLOGY: {
            "strengths": ["用户洞察", "行为预测", "动机分析"],
            "execution_style": "ADAPTIVE",
            "risk_tolerance": "medium"
        },
        SchoolType.SCIENCE: {
            "strengths": ["实验验证", "数据分析", "假设检验"],
            "execution_style": "ITERATIVE",
            "risk_tolerance": "low"
        }
    }
    
    def __init__(self):
        self._optimization_history: List[OptimizedExecutionPlan] = []
        self._performance_metrics: Dict[str, float] = {}
    
    def optimize(self, school_outputs: List[SchoolOutput], 
                 context: Optional[Dict] = None) -> OptimizedExecutionPlan:
        """
        优化学派输出为执行计划
        
        Args:
            school_outputs: 多个学派的输出
            context: 执行上下文
            
        Returns:
            优化的执行计划
        """
        if not school_outputs:
            return self._create_empty_plan()
        
        # 1. 分析学派组合特征
        school_combo = self._analyze_school_combination(school_outputs)
        
        # 2. 选择执行策略
        execution_strategy = self._select_execution_strategy(school_combo)
        
        # 3. 生成执行步骤
        steps = self._generate_execution_steps(school_outputs, execution_strategy)
        
        # 4. 风险评估
        risk_assessment = self._assess_risks(school_outputs, steps)
        
        # 5. 计算预期成功率
        success_rate = self._estimate_success_rate(school_outputs, risk_assessment)
        
        plan = OptimizedExecutionPlan(
            plan_id=f"plan_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            original_schools=[s.school for s in school_outputs],
            execution_strategy=execution_strategy,
            steps=steps,
            estimated_success_rate=success_rate,
            risk_assessment=risk_assessment
        )
        
        self._optimization_history.append(plan)
        return plan
    
    def _analyze_school_combination(self, outputs: List[SchoolOutput]) -> Dict:
        """分析学派组合特征"""
        schools = [o.school for o in outputs]
        
        # 计算组合特征
        total_confidence = sum(o.confidence for o in outputs)
        avg_confidence = total_confidence / len(outputs) if outputs else 0
        
        # 分析风格冲突
        styles = set()
        for school in schools:
            char = self.SCHOOL_CHARACTERISTICS.get(school, {})
            styles.add(char.get("execution_style", "SEQUENTIAL"))
        
        return {
            "school_count": len(schools),
            "avg_confidence": avg_confidence,
            "style_diversity": len(styles),
            "styles": list(styles),
            "has_conflict": len(styles) > 2
        }
    
    def _select_execution_strategy(self, combo: Dict) -> ExecutionStrategy:
        """选择执行策略"""
        styles = combo.get("styles", [])
        
        # 根据学派风格选择策略
        if "PARALLEL" in styles and combo.get("avg_confidence", 0) > 0.7:
            return ExecutionStrategy.PARALLEL
        elif "ITERATIVE" in styles:
            return ExecutionStrategy.ITERATIVE
        elif "ADAPTIVE" in styles:
            return ExecutionStrategy.ADAPTIVE
        else:
            return ExecutionStrategy.SEQUENTIAL
    
    def _generate_execution_steps(self, outputs: List[SchoolOutput],
                                  strategy: ExecutionStrategy) -> List[Dict]:
        """生成执行步骤"""
        steps = []
        
        # 按置信度排序
        sorted_outputs = sorted(outputs, key=lambda x: x.confidence, reverse=True)
        
        if strategy == ExecutionStrategy.SEQUENTIAL:
            # 顺序执行：按优先级排列
            for i, output in enumerate(sorted_outputs):
                steps.append({
                    "step_id": f"step_{i+1}",
                    "school": output.school.value,
                    "action": output.recommendation,
                    "confidence": output.confidence,
                    "action_items": output.action_items,
                    "dependencies": [f"step_{i}"] if i > 0 else [],
                    "execution_mode": "sequential"
                })
        
        elif strategy == ExecutionStrategy.PARALLEL:
            # 并行执行：分组并行
            groups = self._group_for_parallel_execution(sorted_outputs)
            for group_idx, group in enumerate(groups):
                for output in group:
                    steps.append({
                        "step_id": f"step_{group_idx}_{output.school.value}",
                        "school": output.school.value,
                        "action": output.recommendation,
                        "confidence": output.confidence,
                        "action_items": output.action_items,
                        "group": group_idx,
                        "dependencies": [],
                        "execution_mode": "parallel"
                    })
        
        elif strategy == ExecutionStrategy.ITERATIVE:
            # 迭代执行：循环优化
            for i, output in enumerate(sorted_outputs):
                steps.append({
                    "step_id": f"step_{i+1}",
                    "school": output.school.value,
                    "action": output.recommendation,
                    "confidence": output.confidence,
                    "action_items": output.action_items,
                    "iteration": True,
                    "feedback_loop": True,
                    "execution_mode": "iterative"
                })
        
        else:  # ADAPTIVE
            # 自适应：动态调整
            steps.append({
                "step_id": "step_adaptive",
                "schools": [o.school.value for o in sorted_outputs],
                "actions": [o.recommendation for o in sorted_outputs],
                "selector": "context_aware",
                "execution_mode": "adaptive"
            })
        
        return steps
    
    def _group_for_parallel_execution(self, outputs: List[SchoolOutput]) -> List[List[SchoolOutput]]:
        """为并行执行分组"""
        # 简单分组：每2-3个学派一组
        groups = []
        current_group = []
        
        for output in outputs:
            current_group.append(output)
            if len(current_group) >= 2:
                groups.append(current_group)
                current_group = []
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def _assess_risks(self, outputs: List[SchoolOutput], steps: List[Dict]) -> Dict:
        """风险评估"""
        risks = []
        
        # 风格冲突风险
        schools = [o.school for o in outputs]
        risk_tolerance_levels = []
        for school in schools:
            char = self.SCHOOL_CHARACTERISTICS.get(school, {})
            risk_tolerance_levels.append(char.get("risk_tolerance", "medium"))
        
        if len(set(risk_tolerance_levels)) > 1:
            risks.append({
                "type": "style_conflict",
                "level": "medium",
                "description": "学派风险容忍度不一致可能导致执行冲突"
            })
        
        # 低置信度风险
        low_confidence = [o for o in outputs if o.confidence < 0.5]
        if low_confidence:
            risks.append({
                "type": "low_confidence",
                "level": "high" if len(low_confidence) > 1 else "medium",
                "description": f"{len(low_confidence)}个学派置信度低于阈值"
            })
        
        # 步骤复杂度风险
        if len(steps) > 5:
            risks.append({
                "type": "complexity",
                "level": "medium",
                "description": "执行步骤较多，可能增加失败概率"
            })
        
        return {
            "risks": risks,
            "risk_count": len(risks),
            "highest_level": max([r["level"] for r in risks], key=lambda x: {"low": 1, "medium": 2, "high": 3}.get(x, 0)) if risks else "low"
        }
    
    def _estimate_success_rate(self, outputs: List[SchoolOutput], 
                               risk_assessment: Dict) -> float:
        """估计成功率"""
        if not outputs:
            return 0.0
        
        # 基础成功率 = 平均置信度
        base_rate = sum(o.confidence for o in outputs) / len(outputs)
        
        # 根据风险调整
        risk_penalty = {
            "low": 0.0,
            "medium": 0.1,
            "high": 0.2
        }.get(risk_assessment.get("highest_level", "low"), 0.0)
        
        # 学派数量奖励（适度多样性有益）
        diversity_bonus = min(len(outputs) * 0.02, 0.1)
        
        success_rate = base_rate - risk_penalty + diversity_bonus
        return max(0.0, min(1.0, success_rate))
    
    def _create_empty_plan(self) -> OptimizedExecutionPlan:
        """创建空计划"""
        return OptimizedExecutionPlan(
            plan_id=f"plan_empty_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            original_schools=[],
            execution_strategy=ExecutionStrategy.SEQUENTIAL,
            steps=[],
            estimated_success_rate=0.0,
            risk_assessment={"risks": [], "risk_count": 0, "highest_level": "low"}
        )
    
    def get_optimization_stats(self) -> Dict:
        """获取优化统计"""
        if not self._optimization_history:
            return {"total_plans": 0}
        
        total = len(self._optimization_history)
        avg_success_rate = sum(p.estimated_success_rate for p in self._optimization_history) / total
        
        strategy_counts = {}
        for plan in self._optimization_history:
            strategy = plan.execution_strategy.value
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return {
            "total_plans": total,
            "avg_success_rate": avg_success_rate,
            "strategy_distribution": strategy_counts,
            "recent_plans": [
                {
                    "plan_id": p.plan_id,
                    "strategy": p.execution_strategy.value,
                    "success_rate": p.estimated_success_rate,
                    "risk_level": p.risk_assessment.get("highest_level", "low")
                }
                for p in self._optimization_history[-5:]
            ]
        }

# 全局优化器实例
_optimizer: Optional[SchoolExecutionOptimizer] = None

def get_school_execution_optimizer() -> SchoolExecutionOptimizer:
    """获取学派执行优化器"""
    global _optimizer
    if _optimizer is None:
        _optimizer = SchoolExecutionOptimizer()
    return _optimizer
