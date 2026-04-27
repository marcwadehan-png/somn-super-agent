"""
__all__ = [
    'analyze',
    'analyze_demand',
    'analyze_funnel',
    'diagnose_business',
    'generate_growth_plan',
    'generate_next_steps',
    'map_user_journey',
    'narrative_analysis',
]

Somn 分析方法 - 从 somn.py 拆分
包含 analyze() 及各分析子方法
"""

import logging
from typing import Dict, List

from src.industry_engine import IndustryType

logger = logging.getLogger(__name__)

def analyze(self, request):
    """
    执行分析
    """
    from src.somn_legacy._types import AnalysisResult
    import time

    start_time = time.time()

    request_id = f"analysis_{request.created_at()}"
    logger.info(f"开始分析: {request.request_type} [ID: {request_id}]")

    try:
        if request.request_type == "growth_plan":
            result_data = generate_growth_plan(self, request)
        elif request.request_type == "demand_analysis":
            result_data = analyze_demand(self, request)
        elif request.request_type == "funnel_analysis":
            result_data = analyze_funnel(self, request)
        elif request.request_type == "journey_mapping":
            result_data = map_user_journey(self, request)
        elif request.request_type == "business_diagnosis":
            result_data = diagnose_business(self, request)
        elif request.request_type == "narrative_analysis":
            result_data = narrative_analysis(self, request)
        else:
            raise ValueError(f"未知的请求类型: {request.request_type}")

        execution_time = time.time() - start_time

        result = AnalysisResult(
            request_id=request_id,
            request_type=request.request_type,
            status="success",
            data=result_data,
            execution_time=execution_time,
            next_steps=generate_next_steps(request.request_type, result_data)
        )

        logger.info(f"分析完成: {request.request_type} [耗时: {execution_time:.2f}s]")
        return result

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"分析失败: {str(e)}")

        return AnalysisResult(
            request_id=request_id,
            request_type=request.request_type,
            status="failed",
            data={"error": "操作失败"},
            execution_time=execution_time,
            next_steps=["检查输入参数", "联系技术支持"]
        )

def generate_growth_plan(self, request) -> Dict:
    """generate增长计划"""
    business_context = request.business_context

    # 咨询推理链预检
    reasoning_precheck = {}
    if self.reasoning_engine:
        try:
            reasoning_precheck = self.reasoning_engine.consult_solution(
                solution_type="growth_plan",
                problem_context={
                    "industry": business_context.get("industry", ""),
                    "description": str(business_context.get("main_challenges", [])),
                    "stage": business_context.get("stage", ""),
                    "goals": business_context.get("growth_target", ""),
                },
                client_info=business_context
            )
        except Exception as e:
            logger.warning(f"增长计划推理预检失败: {e}")

    # 业务诊断
    diagnosis = self.growth_engine.diagnose_business(business_context)

    # generate增长计划
    plan = self.growth_engine.generate_growth_plan(
        business_info=business_context,
        diagnosis=diagnosis,
        time_horizon=request.time_horizon
    )

    # 行业适配
    industry_str = request.industry or business_context.get("industry", "saas_b2b")
    try:
        industry = IndustryType(industry_str)
        adapted_strategies = []
        for strategy in plan.strategies:
            strategy_dict = {
                "id": strategy.id,
                "name": strategy.name,
                "description": strategy.description,
                "key_actions": strategy.key_actions,
                "success_metrics": strategy.success_metrics
            }
            adapted = self.industry_adapter.adapt_strategy(strategy_dict, industry, business_context)
            adapted_strategies.append(adapted)

        industry_recommendations = self.industry_adapter.generate_industry_recommendations(
            industry, business_context
        )
    except ValueError:
        adapted_strategies = []
        industry_recommendations = []

    return {
        "plan_id": plan.id,
        "growth_phase": plan.growth_phase.value,
        "primary_goal": plan.primary_goal,
        "time_horizon": plan.time_horizon,
        "diagnosis": diagnosis,
        "strategies": adapted_strategies or [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "key_actions": s.key_actions,
                "success_metrics": s.success_metrics,
                "priority_score": s.priority_score
            }
            for s in plan.strategies
        ],
        "metrics": [
            {
                "name": m.name,
                "current": m.current_value,
                "target": m.target_value,
                "gap": m.gap
            }
            for m in plan.metrics
        ],
        "roadmap": plan.roadmap,
        "industry_recommendations": industry_recommendations,
        "reasoning_precheck": reasoning_precheck
    }

def analyze_demand(self, request) -> Dict:
    """分析需求"""
    business_context = request.business_context
    data_sources = business_context.get("data_sources", [])
    report = self.demand_analyzer.analyze(business_context, data_sources)

    return {
        "report_id": report.id,
        "summary": {
            "total_signals": len(report.signals),
            "total_demands": len(report.demands),
            "personas_count": len(report.personas)
        },
        "key_insights": report.key_insights,
        "prioritized_demands": [
            {
                "rank": i+1,
                "name": d.name,
                "priority_score": round(d.priority_score, 2),
                "urgency": d.urgency.value
            }
            for i, d in enumerate(report.prioritized_demands[:10])
        ],
        "user_personas": [
            {"name": p.name, "description": p.description}
            for p in report.personas
        ],
        "opportunities": report.opportunities,
        "recommendations": report.recommendations
    }

def analyze_funnel(self, request) -> Dict:
    """分析漏斗"""
    business_context = request.business_context
    funnel_type = business_context.get("funnel_type", "saas_conversion")
    actual_data = business_context.get("funnel_data", {})

    funnel = self.funnel_optimizer.build_funnel(funnel_type, actual_data)
    experiments = self.funnel_optimizer.generate_experiments(funnel)

    return {
        "funnel_id": funnel.id,
        "funnel_name": funnel.name,
        "summary": {
            "total_users_in": funnel.total_users_in,
            "total_users_out": funnel.total_users_out,
            "overall_conversion_rate": f"{funnel.overall_conversion_rate*100:.2f}%"
        },
        "stages": [
            {
                "stage": s.stage.value,
                "name": s.stage_name,
                "users": s.users,
                "conversion_rate": f"{s.conversion_rate*100:.1f}%",
                "vs_benchmark": f"{s.vs_benchmark:+.1f}%"
            }
            for s in funnel.stages
        ],
        "bottlenecks": funnel.bottlenecks,
        "opportunities": funnel.opportunities,
        "experiments": [
            {
                "id": e.id,
                "name": e.name,
                "target_stage": e.target_stage,
                "expected_lift": f"{e.expected_lift*100:.0f}%",
                "priority_score": round(e.priority_score, 2)
            }
            for e in experiments[:5]
        ]
    }

def map_user_journey(self, request) -> Dict:
    """mapping用户旅程"""
    business_context = request.business_context
    persona_id = business_context.get("persona_id", "default")
    persona_name = business_context.get("persona_name", "典型用户")
    industry = business_context.get("industry", "saas_b2b")

    journey = self.journey_mapper.map_journey(
        persona_id=persona_id,
        persona_name=persona_name,
        industry=industry
    )

    optimization_plan = self.journey_mapper.generate_optimization_plan(journey)

    return {
        "journey_id": journey.id,
        "persona": {
            "id": journey.persona_id,
            "name": journey.persona_name
        },
        "steps": [
            {
                "stage": step.stage.value,
                "name": step.name,
                "user_goal": step.user_goal,
                "user_emotion": step.user_emotion,
                "touchpoints": [tp.name for tp in step.touchpoints],
                "key_actions": step.key_actions
            }
            for step in journey.steps
        ],
        "friction_points": journey.friction_points,
        "wow_moments": journey.wow_moments,
        "optimization_plan": optimization_plan
    }

def diagnose_business(self, request) -> Dict:
    """诊断业务"""
    business_context = request.business_context
    diagnosis = self.growth_engine.diagnose_business(business_context)

    industry_str = request.industry or business_context.get("industry", "saas_b2b")
    try:
        industry = IndustryType(industry_str)
        metrics = business_context.get("current_metrics", {})
        context = {"growth_stage": business_context.get("stage", "growth")}
        scenario_analysis = self.industry_adapter.identify_scenario(
            industry, metrics, context
        )
    except ValueError:
        scenario_analysis = None

    return {
        "diagnosis": diagnosis,
        "scenario_analysis": scenario_analysis,
        "recommended_focus": diagnosis.get("recommended_focus", []),
        "opportunities": diagnosis.get("opportunities", [])
    }

def narrative_analysis(self, request) -> Dict:
    """叙事分析 [v1.0.0]"""
    business_context = request.business_context

    if hasattr(self, 'narrative_engine'):
        try:
            narrative_result = self.narrative_engine.analyze_brand_narrative(
                brand_info=business_context,
                focus=request.specific_focus
            )
        except Exception as e:
            narrative_result = {"error": "操作失败"}
    else:
        narrative_result = {"message": "叙事智能引擎未启用"}

    return {
        "narrative_analysis": narrative_result,
        "brand_context": business_context,
        "analysis_type": "narrative_intelligence",
        "literary_sources": ["莫言: 多声部叙事", "路遥: 苦难意识与线性叙事"],
        "recommendations": [
            "构建多视角品牌叙事体系",
            "设计品牌叙事弧线(起承转合)",
            "通过真实困境建立情感连接",
            "将品牌增长融入人文叙事"
        ]
    }

def generate_next_steps(request_type: str, result_data: Dict) -> List[str]:
    """generate后续action建议"""
    steps_map = {
        "growth_plan": [
            "根据优先级开始执行Top3strategy",
            "建立数据监控看板追踪关键metrics",
            "每周回顾进展并调整计划",
            "记录学习并反馈到系统中"
        ],
        "demand_analysis": [
            "优先解决高优先级需求",
            "深入调研Top3需求的用户场景",
            "制定需求实现路线图",
            "建立需求收集的持续机制"
        ],
        "funnel_analysis": [
            "立即启动高优先级瓶颈的优化实验",
            "建立漏斗监控机制",
            "每两周评估实验结果",
            "将成功经验复制到其他阶段"
        ],
        "journey_mapping": [
            "优先解决摩擦点问题",
            "设计惊喜时刻的具体方案",
            "建立用户反馈收集机制",
            "定期更新用户旅程图"
        ],
        "narrative_analysis": [
            "根据叙事分析结果构建品牌叙事框架",
            "从多视角(用户/创始人/行业/社会)丰富品牌故事",
            "设计叙事内容发布节奏和传播strategy",
            "定期收集用户情感反馈优化叙事方向"
        ],
    }
    return steps_map.get(request_type, [])
