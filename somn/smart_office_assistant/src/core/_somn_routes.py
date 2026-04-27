"""
SomnCore 路由处理器提取模块 (_somn_routes.py)
瘦委托: 所有路由方法已提取为模块级函数，SomnCore 保留委托包装。
"""

from typing import Dict, Any
from datetime import datetime

def _module_run_orchestrator_route(
    somn_core,
    requirement: Dict,
    autonomy_context: Dict,
    options: Dict,
) -> Dict:
    """
    路径A: SomnOrchestrator 直答路由(快手菜/家常菜).
    委托自 SomnCore._run_orchestrator_route().
    """
    description = requirement.get("raw_description", "")
    routing = requirement.get("routing_decision", {})
    cuisine_mode = routing.get("cuisine_mode", "home")
    structured_req = requirement.get("structured_requirement", {})
    context_str = structured_req.get("objective", "")

    wisdom_analysis = requirement.get("wisdom_analysis", {})
    if wisdom_analysis and isinstance(wisdom_analysis, dict):
        insights = wisdom_analysis.get("insights", [])
        if insights:
            context_str += "\n智慧洞察:" + ";".join(insights[:3])

    # 构建 MenuRequest
    try:
        from ..tool_layer.somn_orchestrator import MenuRequest
        menu_req = MenuRequest(
            dish_name=description,
            hunger_level={
                "fast": "light",
                "home": "normal",
                "feast": "hungry"
            }.get(cuisine_mode, "normal"),
            dining_mode=cuisine_mode,
            ingredients_available=context_str,
        )
    except Exception as e:
        import logging
        logging.warning(f"MenuRequest 构建失败: {e}")
        return _module_run_local_llm_route(somn_core, requirement, options)

    if somn_core.somn_orchestrator is None:
        return _module_run_local_llm_route(somn_core, requirement, options)

    try:
        orch_response = somn_core.somn_orchestrator.serve(menu_req)
        content = orch_response.content
        teachers = orch_response.teachers_consulted
        cooking_time = orch_response.cooking_time_ms
        quality_stars = orch_response.quality_stars
        chef_notes = orch_response.chef_notes
    except Exception as e:
        import logging
        logging.warning(f"SomnOrchestrator 调用失败: {e}")
        return _module_run_local_llm_route(somn_core, requirement, options)

    strategy = {
        "task_id": f"strat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "structured_strategy": {
            "overview": content[:300] if content else "(编排器直答)",
            "core_actions": [],
            "success_metrics": {},
        },
        "learning_mode": cuisine_mode,
        "teachers_consulted": teachers,
        "cooking_time_ms": cooking_time,
    }

    execution = {
        "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "execution_summary": {
            "total_tasks": 1,
            "completed": 1,
            "failed": 0,
            "success_ratio": 1.0,
        },
        "orchestrator_result": {
            "content": content,
            "cuisine_mode": cuisine_mode,
            "quality_stars": quality_stars,
            "chef_notes": chef_notes,
            "teachers_consulted": teachers,
            "cooking_time_ms": cooking_time,
        },
        "task_results": [{
            "task_name": "orchestrator_direct",
            "status": "completed",
            "result": {"content": content},
        }],
    }

    evaluation = {
        "evaluation_summary": {
            "overall_score": quality_stars / 5.0 if quality_stars else 0.7,
            "key_findings": [
                f"烹饪模式:{cuisine_mode}",
                f"质量星级:{quality_stars:.1f}⭐",
                chef_notes
            ] if chef_notes else [],
        },
        "roi_signal": {
            "task_recorded": False,
            "route": "orchestrator",
        },
    }

    reflection = (
        f"[编排器路由反思]\n"
        f"路由decision:{routing.get('reasoning', 'N/A')}\n"
        f"复杂度:{routing.get('complexity', 0):.2f}({routing.get('cuisine_level', 'N/A')})\n"
        f"烹饪模式:{cuisine_mode}\n"
        f"请教老师数:{len(teachers)}\n"
        f"烹饪耗时:{cooking_time}ms\n"
        f"质量星级:{quality_stars:.1f}⭐"
    )

    import logging
    logging.info(
        f"[路由A完成] 模式={cuisine_mode} | "
        f"老师={len(teachers)}位 | 耗时={cooking_time}ms | 质量={quality_stars:.1f}⭐"
    )

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }

def _module_run_local_llm_route(
    somn_core,
    requirement: Dict,
    options: Dict,
) -> Dict:
    """
    路径B: 本地 LLM 直答路由(编排器不可用时的 fallback).
    委托自 SomnCore._run_local_llm_route().
    """
    description = requirement.get("raw_description", "")
    structured_req = requirement.get("structured_requirement", {})
    objective = structured_req.get("objective", description)

    content = ""
    # [v1.0.0] 优先使用A/B双模型左右大脑调度，自动切换
    dual_service = getattr(somn_core, 'dual_model_service', None)
    llm_to_use = dual_service or somn_core.llm_service
    if llm_to_use:
        try:
            system_prompt = (
                "你是 Somn,一个不被刻意定义的超级智能体.\n"
                "核心原则:直接简洁有洞察力,结果导向,融入 Somn 智慧(儒/道/佛/兵/xinxue),数据驱动.\n"
                "style:不说废话,开门见山,有洞见有深度."
            )
            # 双模型: model=None 启动A/B自动调度; 直接指定model则走单模型
            model_param = None if dual_service else "local-default"
            response = llm_to_use.chat(
                objective or description,
                model=model_param,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.3,
            )
            content = response.content
        except Exception as e:
            import logging
            logging.warning(f"本地 LLM 调用失败: {e}")
            content = "(本地模型不可用,请检查配置)"
    else:
        content = "(本地模型服务未连接)"

    strategy = {
        "task_id": f"strat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "structured_strategy": {
            "overview": content[:300] if content else "(本地 LLM 直答)",
            "core_actions": [],
            "success_metrics": {},
        },
        "learning_mode": "local_fallback",
    }

    execution = {
        "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "execution_summary": {
            "total_tasks": 1,
            "completed": 1,
            "failed": 0,
            "success_ratio": 1.0,
        },
        "local_llm_result": {"content": content},
        "task_results": [{
            "task_name": "local_llm_direct",
            "status": "completed",
            "result": {"content": content},
        }],
    }

    evaluation = {
        "evaluation_summary": {
            "overall_score": 0.6,
            "key_findings": ["本地 LLM 直答模式"],
        },
        "roi_signal": {
            "task_recorded": False,
            "route": "local_llm",
        },
    }

    reflection = "[本地 LLM 路由反思]编排器不可用,回退到本地模型直答."

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }

def _module_run_wisdom_route(
    somn_core,
    requirement: Dict,
) -> Dict:
    """
    路径C: 智慧板块直答路由(无本地 LLM 时的 fallback).
    委托自 SomnCore._run_wisdom_route().
    """
    description = requirement.get("raw_description", "")
    structured_req = requirement.get("structured_requirement", {})

    # 构建完整context以传递上下文信息
    wisdom_context = {
        "raw_description": description,
        "objective": structured_req.get("objective", ""),
        "industry": requirement.get("industry", "general"),
        "task_type": structured_req.get("task_type", "general_analysis"),
        "constraints": structured_req.get("constraints", []),
        "metrics": structured_req.get("metrics", {}),
    }

    content = ""
    somn_core._ensure_wisdom_layers()
    if somn_core.super_wisdom:
        try:
            result = somn_core.super_wisdom.analyze(
                query_text=description,
                context=wisdom_context,
                threshold=0.25,
                max_schools=6,
            )
            parts = []
            if result.primary_insight:
                parts.append(result.primary_insight)
            if result.secondary_insights:
                parts.append("多维视角:" + ";".join(result.secondary_insights[:3]))
            content = "\n\n".join(parts)
        except Exception as e:
            import logging
            logging.warning(f"智慧板块调用失败: {e}")
            content = "(智慧板块不可用)"
    else:
        content = "(智慧板块未init)"

    strategy = {
        "task_id": f"strat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "structured_strategy": {
            "overview": content[:300] if content else "(智慧板块直答)",
            "core_actions": [],
            "success_metrics": {},
        },
        "learning_mode": "wisdom_only",
    }

    execution = {
        "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "execution_summary": {
            "total_tasks": 1,
            "completed": 1,
            "failed": 0,
            "success_ratio": 1.0,
        },
        "wisdom_result": {"content": content},
        "task_results": [{
            "task_name": "wisdom_direct",
            "status": "completed",
            "result": {"content": content},
        }],
    }

    evaluation = {
        "evaluation_summary": {
            "overall_score": 0.65,
            "key_findings": ["智慧板块直答模式"],
        },
        "roi_signal": {
            "task_recorded": False,
            "route": "wisdom_only",
        },
    }

    reflection = "[智慧路由反思]仅使用智慧板块直答,无执行层."

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }
