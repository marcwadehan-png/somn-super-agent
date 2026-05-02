"""
__all__ = [
    'assess_solution_v2',
    'get_solution_details',
    'get_solution_recommendations',
    'list_all_solutions',
]

Somn 解决方案方法 - 从 somn.py 拆分
包含 get_solution_recommendations, assess_solution_v2, get_solution_details, list_all_solutions
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def get_solution_recommendations(
    self,
    industry: str,
    stage: str,
    scale: str,
    goals: List[str],
    enable_reasoning: bool = True,
    client_info: Dict = None
) -> Dict:
    """get解决方案推荐"""
    recommendations = self.solution_library.recommend_solutions(
        industry=industry,
        stage=stage,
        scale=scale,
        goals=goals
    )

    client_info = client_info or {}

    reasoning_results = {}
    if enable_reasoning and self.reasoning_engine:
        problem_context = {
            "industry": industry,
            "stage": stage,
            "scale": scale,
            "goals": goals,
        }

        for rec in recommendations:
            sol_type = rec.get("solution_type", "")
            try:
                reasoning = self.reasoning_engine.consult_solution(
                    solution_type=sol_type,
                    problem_context=problem_context,
                    client_info=client_info
                )
                reasoning_results[sol_type] = reasoning
                rec["reasoning_confidence"] = reasoning.get("confidence", 0)
                rec["reasoning_suggestions"] = reasoning.get("suggestions", [])
                rec["reasoning_summary"] = reasoning.get("summary", "")[:200]
            except Exception as e:
                logger.warning(f"解决方案 {sol_type} 推理失败: {e}")
                rec["reasoning_confidence"] = None
                rec["reasoning_error"] = "推理失败"

        for rec in recommendations:
            base_score = rec.get("score", 0)
            reasoning_conf = rec.get("reasoning_confidence", 0.5)
            if reasoning_conf is not None:
                rec["composite_score"] = round(base_score * reasoning_conf * 10, 2)
            else:
                rec["composite_score"] = base_score

        recommendations.sort(key=lambda x: x.get("composite_score", 0), reverse=True)

    result = {
        "industry": industry,
        "stage": stage,
        "scale": scale,
        "goals": goals,
        "recommendations": recommendations,
        "total_solutions": len(recommendations),
        "top_recommendations": recommendations[:3] if recommendations else [],
        "reasoning_enabled": enable_reasoning and self.reasoning_engine is not None,
    }

    if reasoning_results:
        result["reasoning_details"] = reasoning_results

    return result

def assess_solution_v2(self, solution_type: str, client_info: Dict) -> Dict:
    """V2 解决方案深度评估(含咨询推理链)"""
    result = {"solution_type": solution_type}

    if self.solution_engine_v2:
        try:
            report = self.solution_engine_v2.assess_solution(solution_type, client_info)
            result["v2_assessment"] = {
                "solution_name": report.solution_name,
                "success_probability": report.success_probability,
                "expected_outcomes": report.expected_outcomes,
                "risk_factors": report.risk_factors,
                "implementation_suggestions": report.implementation_suggestions,
                "assessment_quality": report.assessment_quality,
                "customized_goals": report.customized_goals,
                "validation_result": report.validation_result,
                "alternative_solutions": report.alternative_solutions,
            }
        except Exception as e:
            result["v2_assessment_error"] = "评估失败"
    else:
        result["v2_assessment"] = {"message": "V2引擎未启用"}

    if self.reasoning_engine:
        try:
            reasoning = self.reasoning_engine.consult_solution(
                solution_type=solution_type,
                problem_context={"industry": client_info.get("industry", "")},
                client_info=client_info
            )
            result["reasoning"] = reasoning

            v2_prob = result.get("v2_assessment", {}).get("success_probability", 0.5)
            reasoning_conf = reasoning.get("confidence", 0.5)
            result["composite_assessment"] = {
                "v2_probability": v2_prob,
                "reasoning_confidence": reasoning_conf,
                "combined_score": round(v2_prob * reasoning_conf, 2),
                "level": "high" if (v2_prob * reasoning_conf > 0.5) else
                        "medium" if (v2_prob * reasoning_conf > 0.3) else "low"
            }
        except Exception as e:
            result["reasoning_error"] = "推理失败"
    else:
        result["reasoning"] = {"message": "推理引擎未启用"}

    return result

def get_solution_details(self, solution_type: str) -> Dict:
    """get解决方案详情"""
    from src.growth_engine import SolutionType

    try:
        sol_type = SolutionType(solution_type)
        template = self.solution_library.get_template(sol_type)

        if not template:
            return {"error": f"未找到解决方案: {solution_type}"}

        return {
            "solution_id": template.solution_id,
            "name": template.name,
            "type": template.solution_type.value,
            "category": template.category.value,
            "description": template.description,
            "applicable_industries": template.applicable_industries,
            "applicable_stages": template.applicable_stages,
            "core_strategies": template.core_strategies,
            "implementation_steps": template.implementation_steps,
            "key_metrics": template.key_metrics,
            "expected_outcomes": template.expected_outcomes,
            "case_studies": template.case_studies,
            "common_pitfalls": template.common_pitfalls,
            "recommended_tools": template.recommended_tools
        }
    except ValueError:
        return {"error": f"无效的解决方案类型: {solution_type}"}

def list_all_solutions(self) -> Dict:
    """列出所有可用解决方案"""
    templates = self.solution_library.list_templates()

    return {
        "total_count": len(templates),
        "solutions": [
            {
                "type": t.solution_type.value,
                "name": t.name,
                "category": t.category.value,
                "description": t.description[:100] + "..."
            }
            for t in templates
        ]
    }
