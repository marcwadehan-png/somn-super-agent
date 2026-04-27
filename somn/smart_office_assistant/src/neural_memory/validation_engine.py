"""
__all__ = [
    'create_validation_plan',
    'execute_validation',
    'format_validation_report',
]

验证引擎
Validation Engine
"""

import json
import yaml
from pathlib import Path
from src.core.paths import LEARNING_DIR
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class ValidationType(Enum):
    """验证类型"""
    EXPERIMENTAL = "实验验证"      # A/B测试,随机对照实验
    QUASI_EXPERIMENTAL = "准实验验证"  # 自然实验,断点回归
    OBSERVATIONAL = "观察验证"     # 大数据分析,相关性研究
    QUALITATIVE = "定性验证"       # 深度访谈,案例研究
    THEORETICAL = "理论验证"       # 学术理论支撑

class ValidationStatus(Enum):
    """验证状态"""
    PENDING = "待验证"
    IN_PROGRESS = "验证中"
    VALIDATED = "已验证"
    FALSIFIED = "已证伪"
    PARTIALLY_VALIDATED = "部分验证"
    NEEDS_REVISION = "需修正"

@dataclass
class ValidationPlan:
    """验证计划"""
    plan_id: str
    hypothesis_id: str
    validation_type: ValidationType
    sample_size: int
    duration: str
    metrics: List[str]
    control_variables: List[str]
    success_criteria: Dict
    created_at: str

@dataclass
class ValidationResult:
    """验证结果"""
    result_id: str
    plan_id: str
    hypothesis_id: str
    status: ValidationStatus
    confidence_before: float
    confidence_after: float
    evidence: List[Dict]
    effect_size: float
    statistical_significance: float
    limitations: List[str]
    next_steps: List[str]
    created_at: str

class ValidationEngine:
    """神经记忆系统 - 验证引擎"""
    
    def __init__(self, base_path: str = None):
        from src.core.paths import MEMORY_DIR
        self.base_path = Path(base_path) if base_path else MEMORY_DIR / "validation"
        self.validation_path = self.base_path / "validation"
        
        # 创建必要的目录
        self.validation_path.mkdir(parents=True, exist_ok=True)
        
        # 验证参数
        self.params = {
            "significance_level": 0.05,   # 显著性水平
            "min_sample_size": 100,       # 最小样本量
            "min_effect_size": 0.2,       # 最小效应量
            "confidence_threshold": 0.85  # 高置信度阈值
        }
        
        # 证据等级权重
        self.evidence_weights = {
            ValidationType.EXPERIMENTAL: 1.0,
            ValidationType.QUASI_EXPERIMENTAL: 0.85,
            ValidationType.OBSERVATIONAL: 0.70,
            ValidationType.QUALITATIVE: 0.55,
            ValidationType.THEORETICAL: 0.40
        }
    
    def create_validation_plan(self, hypothesis: Dict, 
                               validation_type: ValidationType = None) -> ValidationPlan:
        """
        创建验证计划
        
        Args:
            hypothesis: 待验证假设 {假设ID, 假设内容, 置信度, 相关研究}
            validation_type: 验证类型(自动推断)
            
        Returns:
            验证计划
        """
        # 自动推断验证类型
        if not validation_type:
            validation_type = self._infer_validation_type(hypothesis)
        
        # generate计划ID
        plan_id = f"VAL_PLAN_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 根据假设内容generate验证参数
        sample_size = self._determine_sample_size(hypothesis, validation_type)
        duration = self._determine_duration(validation_type)
        metrics = self._extract_metrics(hypothesis)
        control_variables = self._identify_control_variables(hypothesis)
        success_criteria = self._define_success_criteria(hypothesis)
        
        plan = ValidationPlan(
            plan_id=plan_id,
            hypothesis_id=hypothesis.get("假设ID", ""),
            validation_type=validation_type,
            sample_size=sample_size,
            duration=duration,
            metrics=metrics,
            control_variables=control_variables,
            success_criteria=success_criteria,
            created_at=datetime.now().isoformat()
        )
        
        # 保存计划
        self._save_validation_plan(plan)
        
        return plan
    
    def execute_validation(self, plan: ValidationPlan, 
                          data: Dict) -> ValidationResult:
        """
        执行验证
        
        Args:
            plan: 验证计划
            data: 验证数据 {实验组, 对照组, 样本量, ...}
            
        Returns:
            验证结果
        """
        # 根据验证类型选择验证方法
        if plan.validation_type == ValidationType.EXPERIMENTAL:
            return self._validate_experiment(plan, data)
        elif plan.validation_type == ValidationType.QUASI_EXPERIMENTAL:
            return self._validate_quasi_experiment(plan, data)
        elif plan.validation_type == ValidationType.OBSERVATIONAL:
            return self._validate_observation(plan, data)
        elif plan.validation_type == ValidationType.QUALITATIVE:
            return self._validate_qualitative(plan, data)
        else:
            return self._validate_theoretical(plan, data)
    
    def _validate_experiment(self, plan: ValidationPlan, 
                            data: Dict) -> ValidationResult:
        """实验验证(A/B测试)"""
        result_id = f"VAL_RESULT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 提取数据
        experimental_group = data.get("实验组", {})
        control_group = data.get("对照组", {})
        
        # 计算效应
        exp_mean = experimental_group.get("均值", 0)
        ctrl_mean = control_group.get("均值", 0)
        exp_std = experimental_group.get("标准差", 1)
        ctrl_std = control_group.get("标准差", 1)
        exp_n = experimental_group.get("样本量", 0)
        ctrl_n = control_group.get("样本量", 0)
        
        # 计算效应量 (Cohen's d)
        pooled_std = ((exp_n - 1) * exp_std ** 2 + (ctrl_n - 1) * ctrl_std ** 2) / (exp_n + ctrl_n - 2)
        pooled_std = pooled_std ** 0.5 if pooled_std > 0 else 1
        effect_size = abs(exp_mean - ctrl_mean) / pooled_std if pooled_std > 0 else 0
        
        # 简化的显著性检验(假设使用t检验)
        # t = (mean1 - mean2) / (pooled_std * sqrt(1/n1 + 1/n2))
        import math
        se = pooled_std * math.sqrt(1/exp_n + 1/ctrl_n) if exp_n > 0 and ctrl_n > 0 else 1
        t_stat = (exp_mean - ctrl_mean) / se if se > 0 else 0
        
        # 简化的p值计算(近似)
        # 自由度
        df = exp_n + ctrl_n - 2
        # 简化处理:使用正态近似
        p_value = self._approximate_p_value(t_stat)
        
        # 确定验证状态
        if p_value < self.params["significance_level"]:
            if effect_size >= self.params["min_effect_size"]:
                status = ValidationStatus.VALIDATED
            else:
                status = ValidationStatus.PARTIALLY_VALIDATED
        else:
            status = ValidationStatus.NEEDS_REVISION
        
        # 置信度更新
        evidence_weight = self.evidence_weights[ValidationType.EXPERIMENTAL]
        confidence_change = effect_size * (1 - p_value) * evidence_weight
        
        # get原置信度
        original_confidence = data.get("原置信度", 0.5)
        new_confidence = min(1.0, original_confidence + confidence_change)
        
        # 构建证据
        evidence = [
            {
                "类型": "实验证据",
                "来源": "A/B测试",
                "样本量": exp_n + ctrl_n,
                "效应量": effect_size,
                "p值": p_value,
                "证据强度": evidence_weight
            }
        ]
        
        # 局限性
        limitations = []
        if exp_n + ctrl_n < self.params["min_sample_size"]:
            limitations.append("样本量不足")
        if effect_size < self.params["min_effect_size"]:
            limitations.append("效应量较小")
        if "随机化" not in data:
            limitations.append("随机化可能不充分")
        
        # 下一步建议
        next_steps = []
        if status == ValidationStatus.VALIDATED:
            next_steps.append("可以推广应用")
            next_steps.append("建议进行长期追踪")
        elif status == ValidationStatus.PARTIALLY_VALIDATED:
            next_steps.append("建议扩大样本量")
            next_steps.append("探索效应的边界条件")
        else:
            next_steps.append("需要修正假设")
            next_steps.append("考虑替代解释")
        
        result = ValidationResult(
            result_id=result_id,
            plan_id=plan.plan_id,
            hypothesis_id=plan.hypothesis_id,
            status=status,
            confidence_before=original_confidence,
            confidence_after=new_confidence,
            evidence=evidence,
            effect_size=effect_size,
            statistical_significance=p_value,
            limitations=limitations,
            next_steps=next_steps,
            created_at=datetime.now().isoformat()
        )
        
        # 保存结果
        self._save_validation_result(result)
        
        return result
    
    def _validate_quasi_experiment(self, plan: ValidationPlan, 
                                   data: Dict) -> ValidationResult:
        """准实验验证"""
        result_id = f"VAL_RESULT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 简化的准实验分析
        effect_estimate = data.get("效应估计", 0)
        confidence_interval = data.get("置信区间", (0, 0))
        confounders_controlled = data.get("控制的混淆变量", [])
        
        # 效应量评估
        effect_size = abs(effect_estimate)
        
        # 置信区间宽度(效应不确定性)
        ci_width = confidence_interval[1] - confidence_interval[0]
        uncertainty = ci_width / 2 if ci_width > 0 else 0.5
        
        # 验证状态
        evidence_weight = self.evidence_weights[ValidationType.QUASI_EXPERIMENTAL]
        
        if effect_size >= self.params["min_effect_size"] and uncertainty < 0.5:
            status = ValidationStatus.VALIDATED
        elif effect_size >= self.params["min_effect_size"] * 0.5:
            status = ValidationStatus.PARTIALLY_VALIDATED
        else:
            status = ValidationStatus.NEEDS_REVISION
        
        # 置信度更新
        original_confidence = data.get("原置信度", 0.5)
        confidence_change = effect_size * evidence_weight * (1 - uncertainty)
        new_confidence = min(1.0, original_confidence + confidence_change)
        
        evidence = [
            {
                "类型": "准实验证据",
                "来源": data.get("方法", "自然实验"),
                "效应估计": effect_estimate,
                "置信区间": confidence_interval,
                "控制的混淆变量": confounders_controlled,
                "证据强度": evidence_weight
            }
        ]
        
        limitations = ["非随机实验,可能存在未控制的混淆"]
        if len(confounders_controlled) < 3:
            limitations.append("控制的混淆变量较少")
        
        next_steps = ["建议进行敏感性分析", "探索工具变量的有效性"]
        
        result = ValidationResult(
            result_id=result_id,
            plan_id=plan.plan_id,
            hypothesis_id=plan.hypothesis_id,
            status=status,
            confidence_before=original_confidence,
            confidence_after=new_confidence,
            evidence=evidence,
            effect_size=effect_size,
            statistical_significance=uncertainty,
            limitations=limitations,
            next_steps=next_steps,
            created_at=datetime.now().isoformat()
        )
        
        self._save_validation_result(result)
        
        return result
    
    def _validate_observation(self, plan: ValidationPlan, 
                              data: Dict) -> ValidationResult:
        """观察验证"""
        result_id = f"VAL_RESULT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        correlation = data.get("相关系数", 0)
        sample_size = data.get("样本量", 0)
        
        # 相关系数转换为效应量
        effect_size = abs(correlation)
        
        # 确定状态
        evidence_weight = self.evidence_weights[ValidationType.OBSERVATIONAL]
        
        if abs(correlation) >= 0.5 and sample_size >= self.params["min_sample_size"]:
            status = ValidationStatus.PARTIALLY_VALIDATED
        elif abs(correlation) >= 0.3:
            status = ValidationStatus.PARTIALLY_VALIDATED
        else:
            status = ValidationStatus.NEEDS_REVISION
        
        # 置信度更新(观察证据权重较低)
        original_confidence = data.get("原置信度", 0.5)
        confidence_change = effect_size * evidence_weight * 0.5
        new_confidence = min(1.0, original_confidence + confidence_change)
        
        evidence = [{
            "类型": "观察证据",
            "来源": "数据分析",
            "样本量": sample_size,
            "相关系数": correlation,
            "证据强度": evidence_weight
        }]
        
        limitations = ["相关性不等于因果性", "可能存在遗漏变量偏差"]
        if sample_size < self.params["min_sample_size"]:
            limitations.append("样本量不足")
        
        next_steps = ["设计实验验证因果关系", "进行更严格的统计控制"]
        
        result = ValidationResult(
            result_id=result_id,
            plan_id=plan.plan_id,
            hypothesis_id=plan.hypothesis_id,
            status=status,
            confidence_before=original_confidence,
            confidence_after=new_confidence,
            evidence=evidence,
            effect_size=effect_size,
            statistical_significance=1 - abs(correlation),
            limitations=limitations,
            next_steps=next_steps,
            created_at=datetime.now().isoformat()
        )
        
        self._save_validation_result(result)
        
        return result
    
    def _validate_qualitative(self, plan: ValidationPlan, 
                              data: Dict) -> ValidationResult:
        """定性验证"""
        result_id = f"VAL_RESULT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 定性数据分析
        interviews = data.get("访谈数", 0)
        themes = data.get("主题", [])
        agreement_rate = data.get("一致率", 0)
        
        # 效应评估(基于一致性)
        effect_size = agreement_rate
        
        evidence_weight = self.evidence_weights[ValidationType.QUALITATIVE]
        
        if agreement_rate >= 0.7 and interviews >= 10:
            status = ValidationStatus.PARTIALLY_VALIDATED
        else:
            status = ValidationStatus.NEEDS_REVISION
        
        original_confidence = data.get("原置信度", 0.5)
        confidence_change = agreement_rate * evidence_weight * 0.5
        new_confidence = min(1.0, original_confidence + confidence_change)
        
        evidence = [{
            "类型": "定性证据",
            "来源": "深度访谈",
            "访谈数": interviews,
            "主要发现": themes[:3] if len(themes) > 3 else themes,
            "一致率": agreement_rate,
            "证据强度": evidence_weight
        }]
        
        limitations = ["定性证据,无法推断因果关系", "可能存在访谈者偏差"]
        if interviews < 10:
            limitations.append("访谈样本较小")
        
        next_steps = ["设计定量研究验证", "扩大定性研究样本"]
        
        result = ValidationResult(
            result_id=result_id,
            plan_id=plan.plan_id,
            hypothesis_id=plan.hypothesis_id,
            status=status,
            confidence_before=original_confidence,
            confidence_after=new_confidence,
            evidence=evidence,
            effect_size=effect_size,
            statistical_significance=agreement_rate,
            limitations=limitations,
            next_steps=next_steps,
            created_at=datetime.now().isoformat()
        )
        
        self._save_validation_result(result)
        
        return result
    
    def _validate_theoretical(self, plan: ValidationPlan, 
                              data: Dict) -> ValidationResult:
        """理论验证"""
        result_id = f"VAL_RESULT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 理论支撑分析
        theories = data.get("支撑理论", [])
        logical_consistency = data.get("逻辑一致性", 0.5)
        empirical_predictions = data.get("可检验预测", [])
        
        effect_size = logical_consistency
        evidence_weight = self.evidence_weights[ValidationType.THEORETICAL]
        
        if len(theories) >= 2 and logical_consistency >= 0.8:
            status = ValidationStatus.PARTIALLY_VALIDATED
        else:
            status = ValidationStatus.NEEDS_REVISION
        
        original_confidence = data.get("原置信度", 0.5)
        confidence_change = logical_consistency * evidence_weight * 0.3
        new_confidence = min(1.0, original_confidence + confidence_change)
        
        evidence = [{
            "类型": "理论证据",
            "来源": "学术理论",
            "支撑理论": theories,
            "逻辑一致性": logical_consistency,
            "可检验预测": empirical_predictions,
            "证据强度": evidence_weight
        }]
        
        limitations = ["缺乏实证数据支持", "需要转化为可检验的假设"]
        
        next_steps = ["设计实验验证", "收集实证数据"]
        
        result = ValidationResult(
            result_id=result_id,
            plan_id=plan.plan_id,
            hypothesis_id=plan.hypothesis_id,
            status=status,
            confidence_before=original_confidence,
            confidence_after=new_confidence,
            evidence=evidence,
            effect_size=effect_size,
            statistical_significance=logical_consistency,
            limitations=limitations,
            next_steps=next_steps,
            created_at=datetime.now().isoformat()
        )
        
        self._save_validation_result(result)
        
        return result
    
    def _infer_validation_type(self, hypothesis: Dict) -> ValidationType:
        """推断验证类型"""
        # 根据假设内容推断最佳验证方法
        
        content = str(hypothesis.get("假设内容", "")).lower()
        
        if "导致" in content or "因果" in content:
            return ValidationType.EXPERIMENTAL
        elif "相关" in content or "关联" in content:
            return ValidationType.OBSERVATIONAL
        elif "感觉" in content or "体验" in content:
            return ValidationType.QUALITATIVE
        elif "理论" in content or "机制" in content:
            return ValidationType.THEORETICAL
        else:
            return ValidationType.EXPERIMENTAL  # 默认实验验证
    
    def _determine_sample_size(self, hypothesis: Dict, 
                               validation_type: ValidationType) -> int:
        """确定样本量"""
        base_sizes = {
            ValidationType.EXPERIMENTAL: 500,
            ValidationType.QUASI_EXPERIMENTAL: 1000,
            ValidationType.OBSERVATIONAL: 2000,
            ValidationType.QUALITATIVE: 30,
            ValidationType.THEORETICAL: 0
        }
        return base_sizes.get(validation_type, 100)
    
    def _determine_duration(self, validation_type: ValidationType) -> str:
        """确定验证周期"""
        durations = {
            ValidationType.EXPERIMENTAL: "2-4周",
            ValidationType.QUASI_EXPERIMENTAL: "1-3个月",
            ValidationType.OBSERVATIONAL: "1-6个月",
            ValidationType.QUALITATIVE: "2-4周",
            ValidationType.THEORETICAL: "即时"
        }
        return durations.get(validation_type, "未知")
    
    def _extract_metrics(self, hypothesis: Dict) -> List[str]:
        """提取验证metrics"""
        # 从假设中提取关键metrics
        content = str(hypothesis.get("假设内容", ""))
        
        metrics = []
        if "转化" in content:
            metrics.append("转化率")
        if "停留" in content:
            metrics.append("停留时长")
        if "购买" in content:
            metrics.append("购买率")
        if "满意" in content:
            metrics.append("满意度评分")
        
        return metrics if metrics else ["主要效果metrics"]
    
    def _identify_control_variables(self, hypothesis: Dict) -> List[str]:
        """recognize控制变量"""
        return ["时间", "地点", "用户群体"]
    
    def _define_success_criteria(self, hypothesis: Dict) -> Dict:
        """定义成功标准"""
        return {
            "最小效应量": self.params["min_effect_size"],
            "显著性水平": self.params["significance_level"],
            "置信度提升": 0.15
        }
    
    def _approximate_p_value(self, t_stat: float) -> float:
        """近似计算p值(简化版)"""
        import math
        
        # 使用正态近似
        # |t| > 1.96 对应 p < 0.05
        # |t| > 2.58 对应 p < 0.01
        
        abs_t = abs(t_stat)
        
        if abs_t >= 3.0:
            return 0.001
        elif abs_t >= 2.58:
            return 0.01
        elif abs_t >= 1.96:
            return 0.05
        elif abs_t >= 1.64:
            return 0.10
        else:
            return 0.20
    
    def _save_validation_plan(self, plan: ValidationPlan):
        """保存验证计划"""
        plan_file = self.validation_path / f"{plan.plan_id}.yaml"
        
        plan_data = {
            "计划ID": plan.plan_id,
            "假设ID": plan.hypothesis_id,
            "验证类型": plan.validation_type.value,
            "样本量": plan.sample_size,
            "验证周期": plan.duration,
            "验证metrics": plan.metrics,
            "控制变量": plan.control_variables,
            "成功标准": plan.success_criteria,
            "创建时间": plan.created_at
        }
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            yaml.dump(plan_data, f, allow_unicode=True, default_flow_style=False)
    
    def _save_validation_result(self, result: ValidationResult):
        """保存验证结果"""
        result_file = self.validation_path / f"{result.result_id}.yaml"
        
        result_data = {
            "结果ID": result.result_id,
            "计划ID": result.plan_id,
            "假设ID": result.hypothesis_id,
            "验证状态": result.status.value,
            "原置信度": result.confidence_before,
            "新置信度": result.confidence_after,
            "证据": result.evidence,
            "效应量": result.effect_size,
            "统计显著性": result.statistical_significance,
            "局限性": result.limitations,
            "下一步": result.next_steps,
            "创建时间": result.created_at
        }
        
        with open(result_file, 'w', encoding='utf-8') as f:
            yaml.dump(result_data, f, allow_unicode=True, default_flow_style=False)
    
    def format_validation_report(self, result: ValidationResult) -> str:
        """格式化验证报告"""
        # 状态mapping
        status_labels = {
            ValidationStatus.VALIDATED: "✅ 已验证",
            ValidationStatus.FALSIFIED: "❌ 已证伪",
            ValidationStatus.PARTIALLY_VALIDATED: "🔶 部分验证",
            ValidationStatus.NEEDS_REVISION: "⚠️ 需要修正",
            ValidationStatus.PENDING: "⏳ 待验证",
            ValidationStatus.IN_PROGRESS: "🔄 验证中"
        }
        
        report = f"""
## 验证结果报告

### 基本信息
- 假设ID: {result.hypothesis_id}
- 验证状态: {status_labels.get(result.status, result.status.value)}
- 验证时间: {result.created_at}

### 置信度变化
- 验证前: {result.confidence_before:.2f}
- 验证后: {result.confidence_after:.2f}
- 变化: {'+' if result.confidence_after > result.confidence_before else ''}{result.confidence_after - result.confidence_before:.2f}

### 效应评估
- 效应量: {result.effect_size:.3f}
- 统计显著性: p = {result.statistical_significance:.3f}

### 证据详情
"""
        for i, ev in enumerate(result.evidence, 1):
            report += f"\n{i}. **{ev.get('类型', '证据')}**\n"
            for key, value in ev.items():
                if key != "类型":
                    report += f"   - {key}: {value}\n"
        
        if result.limitations:
            report += "\n### 局限性\n"
            for lim in result.limitations:
                report += f"- {lim}\n"
        
        if result.next_steps:
            report += "\n### 下一步建议\n"
            for step in result.next_steps:
                report += f"- {step}\n"
        
        return report

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
