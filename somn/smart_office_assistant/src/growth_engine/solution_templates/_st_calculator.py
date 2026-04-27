"""动态效果计算器模块"""

from typing import Dict, List, Any

from ._st_enums import SolutionType
from ._st_dataclasses import DynamicMetric
from ._st_library import SolutionTemplateLibraryV2

__all__ = [
    'calculate_outcomes',
]

class DynamicOutcomeCalculator:
    """动态效果计算器"""
    
    def __init__(self, template_library: SolutionTemplateLibraryV2):
        self.library = template_library
    
    def calculate_outcomes(self, 
                          solution_type: SolutionType,
                          client_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算动态预期效果
        
        Args:
            solution_type: 解决方案类型
            client_params: 客户参数值
            
        Returns:
            计算结果
        """
        template = self.library.get_template(solution_type)
        if not template:
            return {"error": "解决方案类型不存在"}
        
        results = {
            "solution_name": template.name,
            "client_params": client_params,
            "outcomes": [],
            "validation": {}
        }
        
        # get执行能力因子(核心)
        execution_score = client_params.get("execution_capability", 5.0)
        execution_factor = self._calculate_execution_factor(execution_score)
        
        # 计算每个动态metrics
        for metric in template.dynamic_metrics:
            outcome = self._calculate_metric(metric, client_params, execution_factor)
            results["outcomes"].append(outcome)
        
        # 验证评估准确性
        results["validation"] = self._validate_outcomes(results["outcomes"])
        
        return results
    
    def _calculate_execution_factor(self, execution_score: float) -> float:
        """
        计算执行能力因子
        
        核心原则: 专业团队最多达到理想状态的70%
        执行能力1-10分,对应实现率50%-90%
        """
        # 线性mapping: 1分->50%, 10分->90%
        return 0.5 + (execution_score - 1) / 9 * 0.4
    
    def _calculate_metric(self, 
                         metric: DynamicMetric,
                         client_params: Dict,
                         execution_factor: float) -> Dict:
        """计算单个metrics"""
        # get行业基准
        industry = client_params.get("industry", "default")
        baseline = metric.industry_baselines.get(industry, 
                    metric.industry_baselines.get("default", 
                    {"low": 10, "typical": 30, "high": 50}))
        
        # 计算调整因子
        adjustment = 1.0
        for factor_name, weight in metric.factor_weights.items():
            factor_value = self._get_factor_value(factor_name, client_params)
            # 加权平均
            adjustment += (factor_value - 1.0) * weight
        
        # 应用执行能力折扣
        final_low = baseline["low"] * adjustment * execution_factor * 0.85
        final_high = baseline["high"] * adjustment * execution_factor * 1.15
        final_typical = baseline["typical"] * adjustment * execution_factor
        
        return {
            "metric_id": metric.metric_id,
            "metric_name": metric.metric_name,
            "unit": metric.unit,
            "industry_baseline": baseline,
            "calculated_range": {
                "low": round(final_low, 1),
                "typical": round(final_typical, 1),
                "high": round(final_high, 1)
            },
            "adjustment_factor": round(adjustment, 2),
            "execution_factor": round(execution_factor, 2),
            "assessment_notes": metric.assessment_notes
        }
    
    def _get_factor_value(self, factor_name: str, client_params: Dict) -> float:
        """get因子值"""
        factor_calculators = {
            "execution_capability": lambda p: 0.5 + (p.get("execution_capability", 5) - 1) / 9 * 0.4,
            "content_capability": lambda p: 0.6 + (p.get("content_capability", 5) - 1) / 9 * 0.5,
            "team_size": lambda p: min(1.3, 0.8 + p.get("team_size", 5) / 50),
            "avg_order_value": lambda p: min(1.4, 0.8 + p.get("avg_order_value", 100) / 500),
            "monthly_budget": lambda p: min(1.5, 0.7 + p.get("monthly_budget", 10) / 100),
            "has_live_streaming_team": lambda p: 1.3 if p.get("has_live_streaming_team") else 1.0,
            "pain_point_match": lambda p: 1.2,  # 简化处理
            "industry": lambda p: 1.0,  # 已在基准中体现
            "current_retention_rate": lambda p: 1.1 if p.get("current_retention_rate", 50) < 30 else 0.95,
            "purchase_frequency": lambda p: min(1.3, 0.9 + p.get("purchase_frequency", 5) / 50),
        }
        
        calculator = factor_calculators.get(factor_name, lambda p: 1.0)
        return calculator(client_params)
    
    def _validate_outcomes(self, outcomes: List[Dict]) -> Dict:
        """
        验证评估准确性
        
        规则:
        - 实现率<80%: 评估过高
        - 实现率>120%: 评估过低
        - 80%-120%: 评估合理
        """
        validation = {
            "status": "valid",
            "issues": [],
            "recommendations": []
        }
        
        for outcome in outcomes:
            calculated = outcome["calculated_range"]["typical"]
            baseline = outcome["industry_baseline"]["typical"]
            
            if baseline > 0:
                ratio = calculated / baseline
                
                if ratio < 0.8:
                    validation["issues"].append({
                        "metric": outcome["metric_name"],
                        "issue": "评估过高",
                        "ratio": round(ratio, 2),
                        "message": f"预期效果仅为行业基准的{ratio*100:.0f}%,可能存在评估过高"
                    })
                    validation["status"] = "over_estimated"
                elif ratio > 1.2:
                    validation["issues"].append({
                        "metric": outcome["metric_name"],
                        "issue": "评估过低",
                        "ratio": round(ratio, 2),
                        "message": f"预期效果为行业基准的{ratio*100:.0f}%,可能存在评估过低"
                    })
                    if validation["status"] == "valid":
                        validation["status"] = "under_estimated"
        
        # generate建议
        if validation["status"] == "over_estimated":
            validation["recommendations"].append("建议重新评估客户执行能力,或调整预期目标")
        elif validation["status"] == "under_estimated":
            validation["recommendations"].append("客户条件较好,可考虑设定更具挑战性的目标")
        else:
            validation["recommendations"].append("评估结果合理,可按计划推进")
        
        return validation
