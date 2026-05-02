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
    路径A: SomnOrchestrator 编排路由(FAST/HOME模式).
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
                f"编排模式:{cuisine_mode}",
                f"响应质量:{quality_stars:.1f}/5",
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
        f"编排模式:{cuisine_mode}\n"
        f"模型调用数:{len(teachers)}\n"
        f"处理耗时:{cooking_time}ms\n"
        f"响应质量:{quality_stars:.1f}/5"
    )

    import logging
    logging.info(
        f"[路由A完成] 模式={cuisine_mode} | "
        f"模型={len(teachers)}个 | 耗时={cooking_time}ms | 质量={quality_stars:.1f}/5"
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


# ═══════════════════════════════════════════════════════════════════
# [v1.1.0] SageDispatch / DivineReason / 天枢八层管道 路由
# ═══════════════════════════════════════════════════════════════════

def _module_run_sage_dispatch_route(
    somn_core,
    requirement: Dict,
    options: Dict,
) -> Dict:
    """
    路径E: SageDispatch 贤者调度路由.

    通过12调度器智能分配问题到最合适的处理流程:
    SD-P1 问题调度 → SD-R1 推理监管 → SD-F2 四级总控 → ...
    """
    import logging
    description = requirement.get("raw_description", "")
    structured_req = requirement.get("structured_requirement", {})
    routing = requirement.get("routing_decision", {})
    dispatcher_id = routing.get("dispatcher_id", "SD-F2")

    content = ""
    dispatch_meta = {}
    try:
        result = somn_core.dispatch_problem(
            problem=description,
            dispatcher_id=dispatcher_id,
        )
        # DispatchResponse → 提取内容
        if hasattr(result, 'response'):
            content = result.response
        elif hasattr(result, 'result') and isinstance(result.result, dict):
            content = result.result.get('response', '')
            dispatch_meta = {k: v for k, v in result.result.items() if k != 'response'}
        elif isinstance(result, dict):
            content = result.get('response', result.get('result', ''))
            dispatch_meta = {k: v for k, v in result.items() if k not in ('response', 'result')}
        else:
            content = str(result)
    except Exception as e:
        logging.warning(f"[路由E] SageDispatch调用失败: {e}")
        content = f"(SageDispatch调度失败: {e})"

    strategy = {
        "task_id": f"strat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "structured_strategy": {
            "overview": content[:300] if content else "(SageDispatch调度)",
            "core_actions": [],
            "success_metrics": {},
        },
        "learning_mode": "sage_dispatch",
        "dispatcher_id": dispatcher_id,
    }

    execution = {
        "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "execution_summary": {
            "total_tasks": 1,
            "completed": 1,
            "failed": 0,
            "success_ratio": 1.0,
        },
        "sage_dispatch_result": {"content": content, "meta": dispatch_meta},
        "task_results": [{
            "task_name": "sage_dispatch",
            "status": "completed",
            "result": {"content": content},
        }],
    }

    evaluation = {
        "evaluation_summary": {
            "overall_score": 0.8,
            "key_findings": [f"SageDispatch调度(调度器={dispatcher_id})"],
        },
        "roi_signal": {"task_recorded": False, "route": "sage_dispatch"},
    }

    reflection = f"[SageDispatch路由反思] 通过{dispatcher_id}调度处理."

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }


def _module_run_divine_reason_route(
    somn_core,
    requirement: Dict,
    options: Dict,
) -> Dict:
    """
    路径F: DivineReason 统一推理路由.

    4合1推理引擎(GoT+LongCoT+ToT+ReAct)深度推理。
    """
    import logging
    description = requirement.get("raw_description", "")
    structured_req = requirement.get("structured_requirement", {})
    routing = requirement.get("routing_decision", {})
    reasoning_mode = routing.get("reasoning_mode", "DIVINE")

    content = ""
    reason_meta = {}
    try:
        result = somn_core.divine_reason(
            problem=description,
            mode=reasoning_mode,
            context={
                "objective": structured_req.get("objective", ""),
                "industry": requirement.get("industry", "general"),
                "task_type": structured_req.get("task_type", ""),
            },
        )
        # ReasoningResult → 提取内容
        if hasattr(result, 'final_answer'):
            content = result.final_answer
            reason_meta = {
                "mode": getattr(result, 'mode', reasoning_mode),
                "insights_count": len(getattr(result, 'insights', [])),
                "recommendations_count": len(getattr(result, 'recommendations', [])),
            }
        elif isinstance(result, dict):
            content = result.get('final_answer', result.get('answer', ''))
            reason_meta = {k: v for k, v in result.items() if k not in ('final_answer', 'answer')}
        else:
            content = str(result)
    except Exception as e:
        logging.warning(f"[路由F] DivineReason调用失败: {e}")
        content = f"(DivineReason推理失败: {e})"

    strategy = {
        "task_id": f"strat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "structured_strategy": {
            "overview": content[:300] if content else "(DivineReason推理)",
            "core_actions": [],
            "success_metrics": {},
        },
        "learning_mode": "divine_reason",
        "reasoning_mode": reasoning_mode,
    }

    execution = {
        "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "execution_summary": {
            "total_tasks": 1,
            "completed": 1,
            "failed": 0,
            "success_ratio": 1.0,
        },
        "divine_reason_result": {"content": content, "meta": reason_meta},
        "task_results": [{
            "task_name": "divine_reason",
            "status": "completed",
            "result": {"content": content},
        }],
    }

    evaluation = {
        "evaluation_summary": {
            "overall_score": 0.85,
            "key_findings": [f"DivineReason推理(模式={reasoning_mode})"],
        },
        "roi_signal": {"task_recorded": False, "route": "divine_reason"},
    }

    reflection = f"[DivineReason路由反思] 通过{reasoning_mode}模式推理."

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }


def _module_run_tianshu_pipeline_route(
    somn_core,
    requirement: Dict,
    options: Dict,
) -> Dict:
    """
    路径G: 天枢八层管道路由 (TianShu).

    L1输入→L2 NLP→L3 分类→L4 分流→L5 推理(+知识库)→L6 论证→L7 输出→L8 优化
    """
    import logging
    description = requirement.get("raw_description", "")
    structured_req = requirement.get("structured_requirement", {})
    routing = requirement.get("routing_decision", {})
    complexity = routing.get("complexity", 0.5)

    # 根据复杂度选择管道等级
    if complexity >= 0.8:
        from knowledge_cells.eight_layer_pipeline import ProcessingGrade
        grade = ProcessingGrade.SUPER
    elif complexity >= 0.5:
        from knowledge_cells.eight_layer_pipeline import ProcessingGrade
        grade = ProcessingGrade.DEEP
    else:
        from knowledge_cells.eight_layer_pipeline import ProcessingGrade
        grade = ProcessingGrade.BASIC

    content = ""
    pipeline_meta = {}
    try:
        result = somn_core.process_through_pipeline(
            input_text=description,
            grade=grade,
        )
        # PipelineResult → 提取内容
        if hasattr(result, 'final_output'):
            content = result.final_output
            pipeline_meta = {
                "grade": getattr(result, 'grade', str(grade)),
                "layers_completed": getattr(result, 'layers_completed', 8),
            }
        elif isinstance(result, dict):
            content = result.get('final_output', result.get('response', ''))
            pipeline_meta = {k: v for k, v in result.items() if k not in ('final_output', 'response')}
        else:
            content = str(result)
    except Exception as e:
        logging.warning(f"[路由G] 天枢管道调用失败: {e}")
        content = f"(天枢管道处理失败: {e})"

    strategy = {
        "task_id": f"strat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "structured_strategy": {
            "overview": content[:300] if content else "(天枢八层管道)",
            "core_actions": [],
            "success_metrics": {},
        },
        "learning_mode": "tianshu_pipeline",
        "pipeline_grade": str(grade),
    }

    execution = {
        "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "execution_summary": {
            "total_tasks": 1,
            "completed": 1,
            "failed": 0,
            "success_ratio": 1.0,
        },
        "tianshu_pipeline_result": {"content": content, "meta": pipeline_meta},
        "task_results": [{
            "task_name": "tianshu_pipeline",
            "status": "completed",
            "result": {"content": content},
        }],
    }

    evaluation = {
        "evaluation_summary": {
            "overall_score": 0.85,
            "key_findings": [f"天枢八层管道(等级={grade})"],
        },
        "roi_signal": {"task_recorded": False, "route": "tianshu_pipeline"},
    }

    reflection = f"[天枢管道路由反思] 通过{grade}等级八层处理."

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }


def _module_run_slide_forge_route(
    somn_core,
    requirement: Dict,
    options: Dict,
) -> Dict:
    """
    路由H: SlideForge 智能幻灯片生成路由.

    当用户明确指定输出类型为PPT/PDF时触发：
    1. 提取原始内容（description）
    2. 调用 PPTService.generate_ppt() 生成幻灯片
    3. 可选美化 + LLM自主学习
    4. 返回PPT文件路径

    工作流：
    用户明确输出类型为幻灯片 → SlideForge强化 → 高质量PPT产出
                                              ↓
                                  LLM自主学习（风格/美化/排版）
                                              ↓
                                      NeuralMemory持久化
    """
    import logging
    import time
    from pathlib import Path

    logger = logging.getLogger(__name__)
    description = requirement.get("raw_description", "")
    structured_req = requirement.get("structured_requirement", {})
    routing = requirement.get("routing_decision", {})
    cuisine_mode = routing.get("cuisine_mode", "feast")

    slide_file_path = ""
    slide_meta = {}
    error_msg = ""

    # 确定主题
    theme = options.get("theme", "business")

    # 确定输出路径
    output_dir = options.get("output_dir") or str(Path.cwd() / "outputs")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = str(Path(output_dir) / f"slide_forge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx")

    start = time.perf_counter()
    try:
        # 获取开物(Kaiwu) KaiwuService
        try:
            from smart_office_assistant.src.kaiwu import KaiwuService
            service = KaiwuService(theme=theme, enable_learning=True, enable_charts=True)
        except ImportError:
            service = None
            error_msg = "开物(Kaiwu)模块不可用（python-pptx未安装）"

        if service:
            # 检测用户是否要求美化
            beautify = not options.get("no_beautify", False)

            slide_file_path = service.generate_ppt(
                content=description,
                format=None,
                output_path=output_path,
                beautify=beautify,
                auto_charts=True
            )

            elapsed_ms = (time.perf_counter() - start) * 1000
            slide_meta = {
                "theme": theme,
                "beautified": beautify,
                "elapsed_ms": round(elapsed_ms, 2),
                "file_size_bytes": Path(slide_file_path).stat().st_size if Path(slide_file_path).exists() else 0,
            }

    except Exception as e:
        error_msg = str(e)
        logger.error(f"[SlideForge路由] 幻灯片生成失败: {e}")

    # 构建strategy
    content_summary = description[:200] + "..." if len(description) > 200 else description
    strategy = {
        "task_id": f"strat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "structured_strategy": {
            "overview": f"SlideForge强化输出：{content_summary}",
            "core_actions": ["内容提取", "幻灯片生成", "设计美化"] if not error_msg else ["内容提取", "幻灯片生成"],
            "success_metrics": {"file_path": slide_file_path},
        },
        "learning_mode": "slide_forge",
        "cuisine_mode": cuisine_mode,
    }

    # 构建execution
    if error_msg:
        execution = {
            "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "execution_summary": {
                "total_tasks": 1,
                "completed": 0,
                "failed": 1,
                "success_ratio": 0.0,
            },
            "slide_forge_result": {
                "success": False,
                "error": error_msg,
            },
            "task_results": [{
                "task_name": "slide_forge",
                "status": "failed",
                "result": {"error": error_msg},
            }],
        }
        evaluation_score = 0.1
    else:
        execution = {
            "task_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "execution_summary": {
                "total_tasks": 1,
                "completed": 1,
                "failed": 0,
                "success_ratio": 1.0,
            },
            "slide_forge_result": {
                "success": True,
                "file_path": slide_file_path,
                "meta": slide_meta,
            },
            "task_results": [{
                "task_name": "slide_forge",
                "status": "completed",
                "result": {"file_path": slide_file_path, "meta": slide_meta},
            }],
        }
        evaluation_score = 0.9

    evaluation = {
        "evaluation_summary": {
            "overall_score": evaluation_score,
            "key_findings": [
                f"SlideForge生成{'成功' if not error_msg else '失败: ' + error_msg}",
                f"主题={theme}",
                f"文件={slide_file_path}",
            ],
        },
        "roi_signal": {"task_recorded": False, "route": "slide_forge"},
    }

    reflection = (
        f"[SlideForge路由反思] {'成功生成幻灯片' if not error_msg else '幻灯片生成失败: ' + error_msg}，"
        f"主题={theme}，文件已保存至{slide_file_path}。"
        if not error_msg
        else f"[SlideForge路由反思] 幻灯片生成失败，原因：{error_msg}。"
    )

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }


def _module_run_neural_layout_route(
    somn_core,
    requirement: Dict,
    options: Dict,
) -> Dict:
    """
    路由 neural_layout: 神经网络布局全链路处理.

    通过 GlobalNeuralBridge 的 6 个桥接并行调用真实模块，
    同时激活神经网络信号传播路径。

    数据流: input_user → AgentCore(路由分析) → SomnCore(能力查询) →
            WisdomDispatcher(学派分析) → MemorySystem(记忆检索) →
            LearningSystem(学习统计) → AutonomySystem(自主目标)
    """
    description = requirement.get("raw_description", "")
    routing = requirement.get("routing_decision", {})
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    start = time.perf_counter()
    try:
        # 确保 neural_layout 已初始化
        somn_core._ensure_neural_layout()

        from src.neural_layout.integration import get_neural_integration
        integration = get_neural_integration()

        # 调用神经网络全链路处理
        result = integration.process(description, context=routing)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        active_bridges = result.get("active_bridges", [])
        route_decision = result.get("route_decision", "unknown")
        module_outputs = result.get("module_outputs", {})

        # 构建 strategy
        strategy = {
            "task_id": f"strat_{timestamp}",
            "structured_strategy": {
                "overview": f"NeuralLayout全链路处理: {description[:100]}",
                "core_actions": [f"桥接激活: {', '.join(active_bridges)}"],
                "route_decision": route_decision,
                "neural_pathway": result.get("pathway", []),
            },
            "learning_mode": "neural_layout",
            "cuisine_mode": routing.get("cuisine_mode", "home"),
        }

        # 构建 execution
        execution = {
            "task_id": f"exec_{timestamp}",
            "execution_summary": {
                "total_tasks": len(active_bridges),
                "completed": len(active_bridges),
                "failed": 0,
                "success_ratio": 1.0 if active_bridges else 0.0,
            },
            "neural_layout_result": {
                "active_bridges": active_bridges,
                "route_decision": route_decision,
                "processing_time_ms": elapsed_ms,
                "module_outputs": {
                    k: {kk: vv for kk, vv in v.items() if kk != "timestamp"}
                    for k, v in module_outputs.items()
                    if isinstance(v, dict)
                },
            },
            "task_results": [
                {
                    "task_name": bridge,
                    "status": "completed",
                    "result": module_outputs.get(bridge, {}),
                }
                for bridge in active_bridges
            ],
        }

        # 构建 evaluation
        evaluation = {
            "evaluation_summary": {
                "overall_score": 0.8 if active_bridges else 0.1,
                "key_findings": [
                    f"NeuralLayout全链路处理完成",
                    f"激活桥接: {', '.join(active_bridges) or '无'}",
                    f"路由决策: {route_decision}",
                    f"处理耗时: {elapsed_ms}ms",
                ],
            },
            "roi_signal": {"task_recorded": False, "route": "neural_layout"},
        }

        reflection = (
            f"[NeuralLayout路由反思] 全链路处理完成，"
            f"激活{len(active_bridges)}个桥接({', '.join(active_bridges) or '无'})，"
            f"路由={route_decision}，耗时={elapsed_ms}ms。"
        )

    except Exception as e:
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        import logging
        logging.getLogger(__name__).error(f"[NeuralLayout路由] 处理失败: {e}")

        strategy = {
            "task_id": f"strat_{timestamp}",
            "structured_strategy": {
                "overview": f"NeuralLayout处理失败: {description[:100]}",
                "core_actions": [],
            },
            "learning_mode": "neural_layout",
        }
        execution = {
            "task_id": f"exec_{timestamp}",
            "execution_summary": {
                "total_tasks": 1,
                "completed": 0,
                "failed": 1,
                "success_ratio": 0.0,
            },
            "neural_layout_result": {
                "error": str(e),
                "processing_time_ms": elapsed_ms,
            },
            "task_results": [{
                "task_name": "neural_layout",
                "status": "failed",
                "result": {"error": str(e)},
            }],
        }
        evaluation = {
            "evaluation_summary": {
                "overall_score": 0.0,
                "key_findings": [f"NeuralLayout处理失败: {str(e)}"],
            },
            "roi_signal": {"task_recorded": False, "route": "neural_layout"},
        }
        reflection = f"[NeuralLayout路由反思] 处理失败: {e}"

    return {
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "reflection": reflection,
    }
