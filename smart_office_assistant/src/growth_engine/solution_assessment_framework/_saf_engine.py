"""solution_assessment_framework 评估引擎模块 - SolutionAssessmentEngine"""
# 本文件内容由 solution_assessment_framework.py 拆分而来

from typing import Dict, List

from ._saf_base import (
    AssessmentFactorType, PainPointType,
    ClientContext, AssessmentFactor, DynamicOutcomeRange, AssessmentResult,
    IndustryBenchmarkDB
)

__all__ = [
    'analyze_client_needs',
    'assess_solution',
    'calculate_adjustment_factors',
    'compare_assessment_scenarios',
]
from ._saf_goals import (
    generate_private_domain_goals, generate_membership_goals,
    generate_digital_operation_goals, generate_douyin_goals,
    generate_xiaohongshu_goals, generate_crm_goals, generate_generic_goals
)

class SolutionAssessmentEngine:
    """解决方案评估引擎"""

    def __init__(self):
        self.benchmark_db = IndustryBenchmarkDB()
        self.assessment_factors = self._init_factors()

    def _init_factors(self) -> Dict[AssessmentFactorType, AssessmentFactor]:
        return {
            AssessmentFactorType.INDUSTRY: AssessmentFactor(
                factor_type=AssessmentFactorType.INDUSTRY, factor_name="行业因子",
                weight=0.25, base_multiplier=1.0, adjustment_range=(0.7, 1.3)
            ),
            AssessmentFactorType.SCALE: AssessmentFactor(
                factor_type=AssessmentFactorType.SCALE, factor_name="规模因子",
                weight=0.15, base_multiplier=1.0, adjustment_range=(0.8, 1.2)
            ),
            AssessmentFactorType.STAGE: AssessmentFactor(
                factor_type=AssessmentFactorType.STAGE, factor_name="发展阶段因子",
                weight=0.15, base_multiplier=1.0, adjustment_range=(0.8, 1.3)
            ),
            AssessmentFactorType.PAIN_POINT: AssessmentFactor(
                factor_type=AssessmentFactorType.PAIN_POINT, factor_name="痛点匹配因子",
                weight=0.20, base_multiplier=1.0, adjustment_range=(0.6, 1.4)
            ),
            AssessmentFactorType.EXECUTION_CAPABILITY: AssessmentFactor(
                factor_type=AssessmentFactorType.EXECUTION_CAPABILITY, factor_name="执行能力因子",
                weight=0.25, base_multiplier=0.7, adjustment_range=(0.5, 0.9)
            ),
        }

    def analyze_client_needs(self, client_info: Dict) -> ClientContext:
        context = ClientContext(
            industry=client_info.get("industry", "未知"),
            sub_industry=client_info.get("sub_industry"),
            company_scale=client_info.get("scale", "medium"),
            development_stage=client_info.get("stage", "growth"),
            annual_revenue=client_info.get("annual_revenue"),
            avg_order_value=client_info.get("avg_order_value"),
            business_model=client_info.get("business_model"),
            main_channels=client_info.get("main_channels", []),
            team_size=client_info.get("team_size"),
            execution_capability_score=client_info.get("execution_score", 5.0),
            budget_range=client_info.get("budget_range"),
        )
        pain_points_raw = client_info.get("pain_points", [])
        context.primary_pain_points = self._identify_pain_points(pain_points_raw)
        context.pain_point_severity = self._assess_pain_severity(pain_points_raw)
        context.historical_metrics = client_info.get("historical_metrics", {})
        context.historical_growth_rate = client_info.get("historical_growth_rate")
        return context

    def _identify_pain_points(self, pain_points_raw: List[str]) -> List[PainPointType]:
        mapping = {
            "获客成本": PainPointType.HIGH_CAC, "获客难": PainPointType.HIGH_CAC,
            "流量贵": PainPointType.HIGH_CAC, "留存": PainPointType.LOW_RETENTION,
            "复购": PainPointType.LOW_RETENTION, "流失": PainPointType.LOW_RETENTION,
            "转化": PainPointType.LOW_CONVERSION, "成交": PainPointType.LOW_CONVERSION,
            "效率": PainPointType.LOW_EFFICIENCY, "人效": PainPointType.LOW_EFFICIENCY,
            "品牌": PainPointType.BRAND_WEAK, "知名度": PainPointType.BRAND_WEAK,
            "数据": PainPointType.DATA_SILO, "孤岛": PainPointType.DATA_SILO,
            "体验": PainPointType.POOR_EXPERIENCE, "服务": PainPointType.POOR_EXPERIENCE,
            "规模": PainPointType.SCALING_DIFFICULTY, "复制": PainPointType.SCALING_DIFFICULTY,
        }
        identified = []
        for pain in pain_points_raw:
            for keyword, pain_type in mapping.items():
                if keyword in pain:
                    identified.append(pain_type)
                    break
        return list(set(identified))

    def _assess_pain_severity(self, pain_points_raw: List[str]) -> Dict[str, int]:
        severity = {}
        for pain in pain_points_raw:
            score = 5
            if "严重" in pain or "非常" in pain:
                score += 3
            if "急需" in pain or "迫切" in pain:
                score += 2
            if "影响" in pain or "导致" in pain:
                score += 1
            severity[pain] = min(10, score)
        return severity

    def calculate_adjustment_factors(self, context: ClientContext,
                                     solution_type: str) -> Dict[str, float]:
        factors = {}
        factors["industry"] = self._calculate_industry_factor(context, solution_type)
        factors["scale"] = self._calculate_scale_factor(context)
        factors["stage"] = self._calculate_stage_factor(context, solution_type)
        factors["pain_point"] = self._calculate_pain_point_factor(context, solution_type)
        factors["execution"] = self._calculate_execution_factor(context)
        factors["historical"] = self._calculate_historical_factor(context)
        return factors

    def _calculate_industry_factor(self, context: ClientContext,
                                   solution_type: str) -> float:
        industry_effectiveness = {
            "private_domain": {"美妆": 1.2, "母婴": 1.15, "电商": 1.1, "零售": 1.0},
            "membership": {"航空": 1.2, "酒店": 1.15, "餐饮": 1.1, "零售": 1.05},
            "xiaohongshu": {"美妆": 1.3, "母婴": 1.25, "食品": 1.15},
            "douyin": {"服装": 1.2, "美妆": 1.15, "食品": 1.1},
        }
        return industry_effectiveness.get(solution_type, {}).get(context.industry, 1.0)

    def _calculate_scale_factor(self, context: ClientContext) -> float:
        return {"small": 0.9, "medium": 1.0, "large": 1.1}.get(context.company_scale, 1.0)

    def _calculate_stage_factor(self, context: ClientContext,
                                solution_type: str) -> float:
        stage_solution_fit = {
            "startup": {
                "viral_growth": 1.3, "content_marketing": 1.2,
                "douyin": 1.2, "xiaohongshu": 1.15,
            },
            "growth": {
                "private_domain": 1.2, "membership": 1.15, "digital_operation": 1.1,
            },
            "mature": {
                "digital_transformation": 1.2, "data_driven": 1.15, "membership": 1.1,
            },
        }
        return stage_solution_fit.get(context.development_stage, {}).get(solution_type, 1.0)

    def _calculate_pain_point_factor(self, context: ClientContext,
                                     solution_type: str) -> float:
        solution_pain_mapping = {
            "private_domain": [PainPointType.HIGH_CAC, PainPointType.LOW_RETENTION],
            "membership": [PainPointType.LOW_RETENTION, PainPointType.LOW_CONVERSION],
            "digital_operation": [PainPointType.LOW_EFFICIENCY, PainPointType.DATA_SILO],
            "crm": [PainPointType.LOW_EFFICIENCY, PainPointType.DATA_SILO],
            "douyin": [PainPointType.HIGH_CAC, PainPointType.BRAND_WEAK],
            "xiaohongshu": [PainPointType.BRAND_WEAK, PainPointType.HIGH_CAC],
        }
        relevant_pains = solution_pain_mapping.get(solution_type, [])
        matched_pains = [p for p in context.primary_pain_points if p in relevant_pains]
        if not matched_pains:
            return 0.9
        match_ratio = len(matched_pains) / len(relevant_pains) if relevant_pains else 0
        return 0.9 + (match_ratio * 0.3)

    def _calculate_execution_factor(self, context: ClientContext) -> float:
        execution_score = context.execution_capability_score
        return 0.5 + (execution_score - 1) / 9 * 0.4

    def _calculate_historical_factor(self, context: ClientContext) -> float:
        h = context.historical_growth_rate
        if h is None:
            return 1.0
        if h < 0:
            return 0.85
        elif h < 20:
            return 0.95
        elif h < 50:
            return 1.05
        else:
            return 1.15

    def assess_solution(self, solution_type: str,
                       client_info: Dict) -> AssessmentResult:
        context = self.analyze_client_needs(client_info)
        adjustment_factors = self.calculate_adjustment_factors(context, solution_type)
        benchmarks = self.benchmark_db.get_all_metrics(solution_type, context.industry)

        outcome_ranges = []
        for metric_name, benchmark in benchmarks.items():
            dynamic_range = DynamicOutcomeRange(
                metric_name=metric_name,
                industry_baseline_low=benchmark["low"],
                industry_baseline_high=benchmark["high"],
                industry_baseline_typical=benchmark["typical"],
                client_adjustment_factors=adjustment_factors,
                execution_discount=adjustment_factors.get("execution", 0.7)
            )
            dynamic_range.calculate_range(context)
            outcome_ranges.append(dynamic_range)

        customized_goals = self._generate_customized_goals(
            solution_type, context, adjustment_factors
        )
        customized_metrics = self._generate_customized_metrics(
            solution_type, context, outcome_ranges
        )

        result = AssessmentResult(
            solution_type=solution_type, client_context=context,
            customized_goals=customized_goals, customized_metrics=customized_metrics,
            outcome_ranges=outcome_ranges,
            success_probability=self._calculate_success_probability(context, adjustment_factors)
        )
        result.validation_result = self._validate_assessment(result)
        return result

    def _generate_customized_goals(self, solution_type: str,
                                   context: ClientContext,
                                   factors: Dict[str, float]) -> List[Dict]:
        goals = []
        health_score = self._calculate_business_health_score(context)
        potential_score = self._calculate_growth_potential_score(context, factors)
        combined_score = (health_score + potential_score) / 2
        ambition_level = "保守" if combined_score < 4 else "稳健" if combined_score < 7 else "进取"

        goal_map = {
            "private_domain": generate_private_domain_goals,
            "membership": generate_membership_goals,
            "digital_operation": generate_digital_operation_goals,
            "douyin": generate_douyin_goals,
            "xiaohongshu": generate_xiaohongshu_goals,
            "crm": generate_crm_goals,
        }
        gen_fn = goal_map.get(solution_type)
        if gen_fn:
            goals = gen_fn(context, factors, health_score, potential_score, ambition_level)
        else:
            goals = generate_generic_goals(context, factors, health_score, potential_score, ambition_level)

        goals.sort(key=lambda x: x["priority"])
        return goals

    def _calculate_business_health_score(self, context: ClientContext) -> float:
        score = 5.0
        if context.historical_growth_rate is not None:
            if context.historical_growth_rate > 50:
                score += 2.0
            elif context.historical_growth_rate > 20:
                score += 1.0
            elif context.historical_growth_rate < 0:
                score -= 1.5
        industry_avg_aov = {
            "美妆": 300, "母婴": 200, "食品": 100, "服装": 250, "3C": 1000, "家居": 500, "零售": 150
        }
        avg_aov = industry_avg_aov.get(context.industry, 200)
        if context.avg_order_value:
            if context.avg_order_value > avg_aov * 1.5:
                score += 1.5
            elif context.avg_order_value < avg_aov * 0.5:
                score -= 0.5
        stage_scores = {"startup": 0, "growth": 1.0, "mature": 0.5}
        score += stage_scores.get(context.development_stage, 0)
        if context.annual_revenue and context.team_size:
            revenue_per_capita = context.annual_revenue / context.team_size
            if revenue_per_capita > 100:
                score += 1.0
            elif revenue_per_capita < 30:
                score -= 0.5
        return min(10, max(1, score))

    def _calculate_growth_potential_score(self, context: ClientContext,
                                          factors: Dict[str, float]) -> float:
        score = 5.0
        if context.market_growth_rate:
            if context.market_growth_rate > 30:
                score += 2.0
            elif context.market_growth_rate > 15:
                score += 1.0
        competition_impact = {"low": 1.0, "medium": 0, "high": -1.0}
        score += competition_impact.get(context.market_competition_level, 0)
        score += (context.execution_capability_score - 5) * 0.3
        score += (factors.get("pain_point", 1.0) - 1.0) * 2
        return min(10, max(1, score))

    def _generate_customized_metrics(self, solution_type: str,
                                     context: ClientContext,
                                     outcome_ranges: List[DynamicOutcomeRange]) -> List[Dict]:
        metrics = []
        for outcome in outcome_ranges:
            metric = {
                "name": outcome.metric_name,
                "target_range": outcome.calculated_range,
                "industry_baseline": (outcome.industry_baseline_low, outcome.industry_baseline_high),
                "confidence": outcome.confidence_level,
            }
            if context.avg_order_value and "ltv" in outcome.metric_name.lower():
                metric["context_note"] = f"基于客单价¥{context.avg_order_value:.0f}计算"
            metrics.append(metric)
        return metrics

    def _calculate_success_probability(self, context: ClientContext,
                                       factors: Dict[str, float]) -> float:
        execution_score = factors.get("execution", 0.7)
        pain_match = factors.get("pain_point", 1.0)
        base_probability = 0.6
        adjusted = base_probability * (execution_score / 0.7) * pain_match
        return min(0.95, max(0.3, adjusted))

    def _validate_assessment(self, result: AssessmentResult) -> Dict:
        validation = {"status": "valid", "issues": [], "recommendations": []}
        for outcome in result.outcome_ranges:
            if outcome.calculated_range:
                low, high = outcome.calculated_range
                typical = outcome.industry_baseline_typical
                achievement_ratio = ((low + high) / 2) / typical if typical > 0 else 1.0
                if achievement_ratio < 0.8:
                    validation["issues"].append(
                        f"{outcome.metric_name}: 预期效果({achievement_ratio*100:.0f}%)显著低于行业基准,"
                        f"可能存在评估过高风险"
                    )
                    validation["status"] = "over_estimated"
                elif achievement_ratio > 1.2:
                    validation["issues"].append(
                        f"{outcome.metric_name}: 预期效果({achievement_ratio*100:.0f}%)显著高于行业基准,"
                        f"可能存在评估过低风险"
                    )
                    validation["status"] = "under_estimated"
        if validation["status"] == "over_estimated":
            validation["recommendations"].append("建议重新评估客户执行能力,或调整预期目标")
        elif validation["status"] == "under_estimated":
            validation["recommendations"].append("客户条件较好,可考虑设定更具挑战性的目标")
        return validation

    def compare_assessment_scenarios(self, solution_type: str,
                                     client_info: Dict,
                                     scenarios: List[Dict]) -> Dict:
        comparisons = []
        for scenario in scenarios:
            scenario_name = scenario.get("name", "未命名场景")
            scenario_client_info = {**client_info, **scenario.get("adjustments", {})}
            result = self.assess_solution(solution_type, scenario_client_info)
            comparisons.append({
                "scenario": scenario_name,
                "success_probability": result.success_probability,
                "outcome_ranges": [
                    {"metric": o.metric_name, "range": o.calculated_range}
                    for o in result.outcome_ranges
                ],
                "validation": result.validation_result
            })
        return {
            "solution_type": solution_type,
            "scenarios": comparisons,
            "recommendation": self._generate_scenario_recommendation(comparisons)
        }

    def _generate_scenario_recommendation(self, comparisons: List[Dict]) -> str:
        best = max(comparisons, key=lambda x: x["success_probability"])
        return (
            f"基于分析,'{best['scenario']}'场景下成功概率最高"
            f"({best['success_probability']*100:.0f}%)."
            f"建议优先保障该场景下的资源配置."
        )
