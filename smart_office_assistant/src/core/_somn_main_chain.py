"""
SomnCore 主链核心方法委托模块 (_somn_main_chain.py)
提取 run_agent_task 和 analyze_requirement 方法体，减少主文件行数。

所有函数接受 self(SomnCore 实例) 作为第一参数，通过 self 访问实例属性。
"""
from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .somn_core import SomnCore

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# 1. analyze_requirement 主体
# ─────────────────────────────────────────────────────────

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [v2.0 重构] 快车道前置路由模式常量（提取为模块级常量）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_FAST_LANE_PATTERNS = {
    "greeting": r"^(你好|您好|hello|hi|嗨|在吗|在嘛|早上好|下午好|晚上好|hi|hey|你好呀|哈喽)[\s,.!?。！？]*$",
    "thanks": r"^(谢谢|感谢|多谢|thanks|thank you|谢了|多谢啦)[\s,.!?。！？]*$",
    "simple_ack": r"^(好的|好的吧|行|ok|okay|好|NO|yes|yep|yep|收到|明白|知道了|了解)[\s,.!?。！？]*$",
    "bye": r"^(再见|拜拜|bye|晚安|下次见|回头见|走了)[\s,.!?。！？]*$",
    "status_query": r"^(状态|status|怎么样|如何|还好吗|最近如何)[\s,.!?。！？]*$",
    "help_query": r"^(help|帮助|能做什么|有什么用|功能|菜单|命令)[\s,.!?。！？]*$",
    "simple_calc": r"^[\d\s\+\-\*\/\(\)\.]+$",
    "definition_query": r"^(什么是|什么叫|定义|是啥|是神马)[\s\S]{0,30}$",
    "time_query": r"^(现在几点了?|今天几号|今天是|现在时间|当前时间)[\s,.!?。！？]*$",
    "weather_query": r"^(天气|气温|下雨|晴天)[\s,.!?。！？]*$",
}

def _is_fast_lane(description: str) -> tuple:
    """[单一职责] 快速判断是否走快车道。返回 (is_fast, reason, category)"""
    import re
    text = description.strip()
    if len(text) > 150:
        return (False, None, None)
    for category, pattern in _FAST_LANE_PATTERNS.items():
        if re.match(pattern, text, re.IGNORECASE):
            return (True, category, category)
    if len(text.split()) <= 5 and not any(k in text for k in ["分析", "研究", "报告", "生成", "创建", "查找", "查询", "优化", "设计", "比较", "评估", "预测"]):
        return (True, "simple_text", "simple_chat")
    return (False, None, None)

def _build_fast_lane_response(description: str, fast_reason: str, fast_category: str) -> Dict[str, Any]:
    """[单一职责] 构建快车道快速响应文档"""
    return {
        "_fast_lane": True,
        "_fast_reason": fast_reason,
        "task_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "raw_description": description,
        "industry": "general",
        "parsed_requirement": {
            "objective": description[:120],
            "task_type": "simple_chat",
            "deliverable": "直接回复",
        },
        "structured_requirement": {
            "objective": description[:120],
            "task_type": "simple_chat",
            "priority": "low",
        },
        "feasibility_assessment": {"overall_score": 1.0, "feasibility": "high"},
        "search_context": [],
        "memory_context": {"answer": "", "confidence": 0.0},
        "metaphysics_analysis": {"triggered": False},
        "wisdom_analysis": {"triggered": False, "insights": [], "activated_schools": []},
        "semantic_analysis": {"enabled": False, "inferred_intent": fast_category},
        "persona_voice": {},
        "recommendations": [],
        "routing_decision": {
            "route": "local_llm_fallback",
            "complexity": 0.1,
            "reason": f"fast_lane_{fast_reason}",
        },
        "created_at": datetime.now().isoformat(),
    }

def _init_timeout_guard(self: "SomnCore") -> tuple:
    """[单一职责] 初始化全局超时守护器，返回 (guard, chain_start)"""
    import time as _time
    from .timeout_guard import create_timeout_guard
    _guard = None
    try:
        _guard = create_timeout_guard(
            request_id=f"req_{datetime.now().strftime('%H%M%S%f')}",
            timeout=120.0,
        )
    except Exception as e:
        logger.warning(f"[主链路] TimeoutGuard创建失败(降级为无保护模式): {e}")
    _chain_start = _time.monotonic()
    return (_guard, _chain_start)

def _run_semantic_layer(
    self: "SomnCore",
    description: str,
    context: Dict,
    _guard: Any,
    _chain_start: float,
) -> tuple:
    """[单一职责] 语义理解层，返回 (semantic_analysis, primary_industry)"""
    import time as _time
    from ._somn_semantic_api import _module_run_semantic_analysis
    
    def _quick_timeout_check(label: str) -> bool:
        if _guard is not None and _guard.ctx.is_expired():
            logger.warning(f"[主链路] {label}: 全局已超时(T+{_time.monotonic()-_chain_start:.1f}s)")
            return True
        return False
    
    if _quick_timeout_check("语义分析"):
        return ({"_timeout": True, "_elapsed": round(_time.monotonic() - _chain_start, 2),
                 "raw_description": description, "reason": "global_timeout_before_semantic"}, None)
    
    semantic_analysis = _module_run_semantic_analysis(self, description, context)
    
    if _guard is not None:
        try:
            _guard.check_and_degrade()
        except Exception as e:
            logger.debug(f"[主链路] TimeoutGuard降级检查跳过: {e}")
    
    self._ensure_layers()
    matched_industries = self.industry_kb.match_industry(description)
    primary_industry = matched_industries[0] if matched_industries else None
    
    return (semantic_analysis, primary_industry)

def _run_phase1_parallel(
    self: "SomnCore",
    description: str,
    primary_industry: Any,
    context: Dict,
    _guard: Any,
) -> tuple:
    """[单一职责] Phase1三路并行：LLM解析、网络搜索、记忆查询"""
    from ._somn_analysis import (
        _module_parse_requirement,
        _module_structure_requirement,
        _module_search_context_info_safe,
        _module_build_local_fallback_context,
    )
    
    extra_ctx = context or {}
    executor = self._get_analysis_executor()
    
    future_parse = executor.submit(_module_parse_requirement, self, description, extra_ctx)
    future_search = executor.submit(
        _module_search_context_info_safe, self, description, primary_industry, timeout=3.0
    )
    future_memory = executor.submit(self._query_memory_context, description)
    
    _SEARCH_TIMEOUT = 4.0
    _LLM_TIMEOUT = 15.0
    _MEMORY_TIMEOUT = 5.0
    
    parsed_requirement = self._safe_future_result(
        future_parse, _LLM_TIMEOUT,
        fallback={
            "objective": description[:120],
            "task_type": "general_analysis",
            "deliverable": "结构化分析结果",
            "constraints": [], "inputs_needed": [],
            "success_definition": "形成可执行输出",
            "metrics": {}, "timeline": "未指定",
            "priority": "medium", "risk_points": [],
            "raw_text": description,
        },
        label="LLM解析"
    )
    search_results = self._safe_future_result(
        future_search, _SEARCH_TIMEOUT,
        fallback=_module_build_local_fallback_context(description, self._extract_keywords),
        label="网络搜索"
    )
    memory_context = self._safe_future_result(
        future_memory, _MEMORY_TIMEOUT,
        fallback={"answer": "", "confidence": 0.0, "evidence_chain": ["记忆查询超时"]},
        label="记忆查询"
    )
    
    if _guard is not None:
        try:
            _guard.check_and_degrade()
        except Exception as e:
            logger.debug(f"[主链路] TimeoutGuard降级检查跳过: {e}")
    
    structured_req = _module_structure_requirement(
        self, parsed_requirement, search_results, extra_ctx, memory_context
    )
    
    return (parsed_requirement, search_results, memory_context, structured_req)

def _run_phase2_parallel(
    self: "SomnCore",
    description: str,
    structured_req: Dict,
    parsed_requirement: Dict,
    primary_industry: Any,
    context: Dict,
    _guard: Any,
) -> tuple:
    """[单一职责] Phase2四路fan-out：智慧分析、形而上学、可行性、路由"""
    from .timeout_guard import should_skip_heavy_ops
    from ._somn_analysis import (
        _module_assess_feasibility,
        _module_assess_task_routing,
    )
    
    _wisdom_analysis_holder: List[Any] = [None]
    _metaphysics_holder: List[Any] = [None]
    _feasibility_holder: List[Any] = [None]
    _routing_holder: List[Any] = [None]
    _parallel_errors: List[str] = []
    
    _skip_heavy = should_skip_heavy_ops(_guard)
    if _skip_heavy:
        logger.warning(f"[主链路] Phase 2 跳过重度操作(全局T+{_guard.ctx.elapsed:.1f}s)")
        return (
            {"triggered": False, "insights": [], "activated_schools": [], "recommendations": [], "thinking_method": "", "source": "skipped_timeout"},
            {"triggered": False, "_skipped": True},
            {"overall_score": 0.5, "feasibility": "unknown", "_skipped": True},
            {"route": "full_workflow", "complexity": 0.6, "_skipped": True},
        )
    
    def _run_wisdom_safe():
        try:
            _wisdom_analysis_holder[0] = self._run_wisdom_analysis(description, structured_req, context or {})
        except Exception as e:
            _parallel_errors.append(f"wisdom:{e}")
            _wisdom_analysis_holder[0] = {"triggered": False, "insights": [], "activated_schools": [], "recommendations": [], "thinking_method": "", "source": "error"}
    
    def _run_metaphysics_safe():
        try:
            _metaphysics_holder[0] = self._maybe_run_metaphysics_analysis(
                description=description, extra_context=context or {}, parsed_requirement=parsed_requirement, primary_industry=primary_industry,
            )
        except Exception as e:
            _parallel_errors.append(f"metaphysics:{e}")
            _metaphysics_holder[0] = {"triggered": False}
    
    def _run_feasibility_safe():
        try:
            _feasibility_holder[0] = _module_assess_feasibility(structured_req, primary_industry)
        except Exception as e:
            _parallel_errors.append(f"feasibility:{e}")
            _feasibility_holder[0] = {"overall_score": 0.5, "feasibility": "unknown"}
    
    def _run_routing_safe():
        try:
            _routing_holder[0] = _module_assess_task_routing(self, description, structured_req, context or {})
        except Exception as e:
            _parallel_errors.append(f"routing:{e}")
            _routing_holder[0] = {"route": "full_workflow", "complexity": 0.6}
    
    _phase2_executor = self._get_analysis_executor()
    _f2_wisdom = _phase2_executor.submit(_run_wisdom_safe)
    _f2_meta = _phase2_executor.submit(_run_metaphysics_safe)
    _f2_feas = _phase2_executor.submit(_run_feasibility_safe)
    _f2_route = _phase2_executor.submit(_run_routing_safe)
    
    _PHASE2_TIMEOUT = 12.0
    for _f in [_f2_wisdom, _f2_meta, _f2_feas, _f2_route]:
        try:
            _f.result(timeout=_PHASE2_TIMEOUT)
        except Exception as e:
            logger.debug(f"并行分析超时: {e}")
    
    if _parallel_errors:
        logger.warning(f"[并行分析] 部分环节异常: {_parallel_errors}")
    
    return (
        _wisdom_analysis_holder[0] or {"triggered": False, "insights": [], "activated_schools": [], "recommendations": [], "thinking_method": "", "source": "none"},
        _metaphysics_holder[0] or {"triggered": False},
        _feasibility_holder[0] or {"overall_score": 0.5},
        _routing_holder[0] or {"route": "full_workflow", "complexity": 0.6},
    )

def _build_requirement_doc(
    ctx: Any,
    task_id: str,
    description: str,
    primary_industry: Any,
    parsed_requirement: Dict,
    structured_req: Dict,
    feasibility: Dict,
    search_results: List,
    memory_context: Dict,
    metaphysics_analysis: Dict,
    wisdom_analysis: Dict,
    semantic_analysis: Dict,
    persona_voice: Dict,
    recommendations: List,
    routing_decision: Dict,
    _guard: Any,
) -> Dict[str, Any]:
    """[单一职责] 构建需求分析文档"""
    requirement_doc = {
        "task_id": task_id,
        "raw_description": description,
        "industry": primary_industry.value if primary_industry else "general",
        "parsed_requirement": parsed_requirement,
        "structured_requirement": structured_req,
        "feasibility_assessment": feasibility,
        "search_context": search_results,
        "memory_context": memory_context,
        "metaphysics_analysis": metaphysics_analysis,
        "wisdom_analysis": wisdom_analysis,
        "semantic_analysis": semantic_analysis,
        "persona_voice": persona_voice,
        "recommendations": recommendations,
        "routing_decision": routing_decision,
        "created_at": ctx.started_at
    }
    
    if _guard is not None:
        try:
            requirement_doc["_timeout_guard"] = {
                "elapsed_s": round(_guard.ctx.elapsed, 2),
                "level": _guard.ctx.level.value,
                "degradation_steps": len(_guard.ctx.degradation_steps),
                "is_expired": _guard.ctx.is_expired(),
            }
            if _guard.ctx.is_expired():
                requirement_doc["_status"] = "timeout_degraded"
            elif _guard.ctx.level.value != "normal":
                requirement_doc["_status"] = f"degraded_{_guard.ctx.level.value}"
            else:
                requirement_doc["_status"] = "normal"
        except Exception as e:
            logger.warning(f"[主链路] 状态标记更新失败: {e}")
    
    ctx.outputs = requirement_doc
    ctx.status = "completed"
    ctx.completed_at = datetime.now().isoformat()
    
    return requirement_doc

def _module_run_analyze_requirement(
    self: "SomnCore",
    description: str,
    context: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    需求分析 standalone 实现 [v18.0 单一职责重构版].
    
    职责链:
    1. 快车道检测 → 快速响应
    2. 超时守护初始化
    3. 语义理解层
    4. Phase1三路并行
    5. Phase2四路fan-out
    6. 结果整合
    """
    import time as _time
    from .timeout_guard import should_skip_heavy_ops
    from ._somn_types import SomnContext
    from ._somn_analysis import _module_generate_recommendations
    
    # Step 1: 快车道检测
    is_fast, fast_reason, fast_category = _is_fast_lane(description)
    if is_fast:
        logger.info(f"⚡ [快车道] 检测到简单请求({fast_reason})，跳过完整分析链路")
        return _build_fast_lane_response(description, fast_reason, fast_category)
    
    # Step 2: 超时守护初始化
    _guard, _chain_start = _init_timeout_guard(self)
    if context is None:
        context = {}
    context["_timeout_guard"] = _guard
    
    # 情绪研究框架校验
    try:
        from ._somn_emotion_research import validate_requirement_with_framework
        framework_validation = validate_requirement_with_framework(description, context)
        logger.info(f"[情绪研究框架] 校验完成: coverage={framework_validation.get('coverage_score', 0):.2f}, valid={framework_validation.get('is_valid', False)}")
        context["_emotion_framework_validation"] = framework_validation
        if not framework_validation.get("is_valid", True) and framework_validation.get("recommendations"):
            logger.warning(f"⚠️ [情绪研究框架] 改进建议: {framework_validation['recommendations'][:2]}")
    except Exception as e:
        logger.warning(f"[情绪研究框架] 校验失败(不影响主流程): {e}")
    
    # 初始化上下文
    task_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ctx = SomnContext(task_id=task_id, task_type="requirement_analysis", inputs={"description": description, "context": context})
    self.contexts[task_id] = ctx
    logger.debug(f"🔍 开始需求分析 [{task_id}]")
    
    # Step 3: 语义理解层
    semantic_analysis, primary_industry = _run_semantic_layer(self, description, context, _guard, _chain_start)
    if semantic_analysis.get("_timeout"):
        return semantic_analysis
    ctx.industry = primary_industry.value if primary_industry else None
    
    # Step 4: Phase1三路并行
    parsed_requirement, search_results, memory_context, structured_req = _run_phase1_parallel(
        self, description, primary_industry, context, _guard
    )
    
    # 人设场景识别
    persona_voice: Dict[str, Any] = {}
    self._ensure_wisdom_layers()
    if self.persona:
        try:
            persona_output = self.persona.generate_voice_output(description)
            persona_voice = {
                "scene": persona_output["scenario"],
                "voice_mode": persona_output["voice_mode"],
                "wisdom_sources": persona_output["wisdom_sources"],
                "tone_markers": persona_output["tone_markers"],
                "voice_description": persona_output["voice_description"],
            }
            logger.info(f"🎭 人设场景匹配: {persona_output['scenario']} | 声线: {persona_output['voice_mode']}")
        except Exception as e:
            logger.warning(f"人设场景recognize失败: {e}")
    
    if semantic_analysis.get("enabled"):
        structured_req["_semantic_hints"] = {
            "inferred_intent": semantic_analysis.get("inferred_intent"),
            "intent_confidence": semantic_analysis.get("intent_confidence"),
            "keywords": semantic_analysis.get("keywords", []),
            "understanding_summary": semantic_analysis.get("understanding_summary", ""),
            "clarification_needed": semantic_analysis.get("clarification_needed", False),
            "clarification_question": semantic_analysis.get("clarification_question", ""),
        }
    
    # Step 5: Phase2四路fan-out
    wisdom_analysis, metaphysics_analysis, feasibility, routing_decision = _run_phase2_parallel(
        self, description, structured_req, parsed_requirement, primary_industry, context, _guard
    )
    
    # Step 6: 结果整合
    recommendations = _module_generate_recommendations(structured_req, feasibility, metaphysics_analysis, wisdom_analysis)
    
    requirement_doc = _build_requirement_doc(
        ctx, task_id, description, primary_industry,
        parsed_requirement, structured_req, feasibility,
        search_results, memory_context, metaphysics_analysis,
        wisdom_analysis, semantic_analysis, persona_voice,
        recommendations, routing_decision, _guard
    )
    
    self._record_task_memory(
        title=f"需求分析 {task_id}",
        description=json.dumps({
            "description": description,
            "objective": structured_req.get("objective"),
            "constraints": structured_req.get("constraints", []),
            "task_type": structured_req.get("task_type"),
            "semantic_intent": semantic_analysis.get("inferred_intent", "unknown"),
            "semantic_keywords": semantic_analysis.get("keywords", []),
            "semantic_confidence": semantic_analysis.get("intent_confidence", 0.0)
        }, ensure_ascii=False),
        confidence_score=int(feasibility.get("overall_score", 0.7) * 100),
        scenarios=[structured_req.get("task_type", "需求分析")]
    )
    
    _total_elapsed = round(_time.monotonic() - _chain_start, 2)
    logger.info(f"✅ 需求分析完成 [{task_id}] ({_total_elapsed}s)")
    return requirement_doc

# ─────────────────────────────────────────────────────────
# 2. run_agent_task 主体 [v2.0 单一职责重构]
# ─────────────────────────────────────────────────────────

def _init_task_timeout_guard(self: "SomnCore") -> tuple:
    """[单一职责] 初始化任务级超时守护器，返回 (guard, task_start)"""
    import time as _time
    from .timeout_guard import create_timeout_guard
    _task_guard = None
    _task_start = _time.monotonic()
    try:
        _task_guard = create_timeout_guard(
            request_id=f"task_{datetime.now().strftime('%H%M%S%f')}",
            timeout=240.0,
        )
    except Exception as e:
        logger.warning(f"[主链路] 任务级TimeoutGuard创建失败(降级为无保护模式): {e}")
    return (_task_guard, _task_start)

def _inject_main_chain_integration(
    self: "SomnCore",
    requirement: Dict,
) -> Any:
    """[单一职责] 主线集成：动态模式选择与结果注入"""
    self._ensure_main_chain()
    main_chain_result = None
    if self._main_chain_integration is not None:
        try:
            main_chain_result = self._main_chain_integration.execute(requirement)
            if main_chain_result:
                requirement["main_chain"] = {
                    "mode": main_chain_result.mode.value,
                    "success": main_chain_result.success,
                    "metadata": main_chain_result.metadata
                }
                logger.info(f"[主线集成] 运行模式: {main_chain_result.mode.value}")
        except Exception as e:
            logger.warning(f"[主线集成] 执行失败: {e}")
    return main_chain_result

def _execute_route_D_full_workflow(
    self: "SomnCore",
    description: str,
    requirement: Dict,
    options: Dict,
    evaluation_criteria: Dict,
    autonomy_context: Dict,
    main_chain_result: Any,
    _task_guard: Any,
    _task_start: float,
) -> tuple:
    """[单一职责] 路由D：完整工作流（FEAST模式）含超时保护"""
    import time as _time
    from .timeout_guard import should_skip_heavy_ops
    
    def _task_timeout_check(label: str) -> bool:
        if _task_guard is not None and _task_guard.ctx.is_expired():
            logger.warning(f"[主链路] 任务级超时(T+{_time.monotonic()-_task_start:.1f}s) in {label}")
            return True
        return False
    
    logger.info(f"[路由D] 完整工作流(FEAST模式): {description[:50]}...")
    
    # 并形模式：并行增强
    parallel_output = None
    if (main_chain_result and
            main_chain_result.mode.value == "parallel" and
            main_chain_result.parallel_results):
        parallel_output = main_chain_result.parallel_results.get("results", {})
        if parallel_output:
            requirement["parallel_insights"] = parallel_output.get("insights", [])
            logger.info(f"[主线集成] 并形增强洞察: {len(parallel_output.get('insights', []))} 条")
    
    # 策略设计（超时检查）
    if _task_timeout_check("策略设计"):
        strategy = {"_timeout_fallback": True, "timeout_route": "design_strategy"}
        execution = {"_timeout_fallback": True}
    else:
        strategy = self.design_strategy(requirement, options=options)
    
    # 工作流执行（超时检查）
    if not strategy.get("_timeout_fallback") and not _task_timeout_check("工作流执行"):
        execution = self.execute_workflow(strategy, execution_config=options)
    else:
        execution = {"_timeout_fallback": True}
        logger.warning(f"[主链路] execute_workflow 跳过(任务级超时)")
    
    # 交叉模式：交叉反馈
    if (main_chain_result and
            main_chain_result.mode.value == "cross" and
            self._main_chain_integration is not None):
        if _task_timeout_check("交叉反馈"):
            logger.warning(f"[主链路] 交叉反馈跳过(任务级超时)")
        else:
            try:
                cross_result = self._main_chain_integration.execute_cross(
                    self._main_chain_integration.build_chain_context(requirement),
                    {"strategy": strategy, "execution": execution, "requirement": requirement}
                )
                if cross_result.get("success"):
                    cross_data = cross_result.get("results", {})
                    if cross_data:
                        requirement["cross_feedback"] = cross_data.get("feedback_signals", [])
                        logger.info(f"[主线集成] 交叉反馈信号: {len(cross_data.get('feedback_signals', []))} 个")
            except Exception as e:
                logger.warning(f"[主线集成] 交叉反馈执行失败: {e}")
    
    # 评估与反思（超时检查）
    if _task_timeout_check("评估"):
        evaluation = {"_timeout_fallback": True}
    else:
        evaluation = self.evaluate_results(execution, evaluation_criteria=evaluation_criteria)
    
    if _task_timeout_check("反思生成"):
        reflection_text = {"_timeout_fallback": True, "reflection_text": "[任务级超时，反思生成跳过]"}
    else:
        reflection_text = self._generate_autonomy_reflection(
            requirement, strategy, execution, evaluation, autonomy_context
        )
    
    return (strategy, execution, evaluation, reflection_text)

def _normalize_reflection(reflection_text: Any) -> Dict[str, Any]:
    """[单一职责] 反思结果归一化"""
    if isinstance(reflection_text, dict):
        return reflection_text
    return {
        "reflection_text": str(reflection_text) if reflection_text else "",
        "reusable_actions": [],
        "lessons_learned": [],
        "suggested_next_task": "继续下一轮执行",
        "next_actions": [],
    }

def _build_final_report(
    requirement: Dict,
    strategy: Dict,
    execution: Dict,
    evaluation: Dict,
    reflection: Dict,
    autonomy_context: Dict,
    routing: Dict,
    main_chain_result: Any,
    description: str,
    current_goal: Any,
) -> Dict[str, Any]:
    """[单一职责] 构建最终报告"""
    from ._somn_evaluation import _generate_next_iteration as _module_generate_next_iteration
    
    return {
        "task_id": requirement["task_id"],
        "description": description,
        "requirement": requirement,
        "strategy": strategy,
        "execution": execution,
        "evaluation": evaluation,
        "autonomy_context": autonomy_context,
        "reflection": reflection,
        "routing_info": routing,
        "main_chain_info": {
            "mode": main_chain_result.mode.value if main_chain_result else "serial",
            "success": main_chain_result.success if main_chain_result else True,
            "parallel_enabled": main_chain_result.mode.value == "parallel" if main_chain_result else False,
            "cross_enabled": main_chain_result.mode.value == "cross" if main_chain_result else False
        },
        "next_iteration": _module_generate_next_iteration(
            requirement, strategy, execution, evaluation,
            reflection=reflection, autonomy_context=autonomy_context
        ),
        "generated_at": datetime.now().isoformat()
    }

def _module_run_agent_task(
    self: "SomnCore",
    description: str,
    context: Optional[Dict[str, Any]] = None,
    options: Optional[Dict[str, Any]] = None,
    evaluation_criteria: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    [v18.0] unified智能体任务主链 [单一职责重构版].
    
    职责链:
    1. 任务级超时守护初始化
    2. 需求分析与快车道检测
    3. 主线集成（LearningCoordinator + AutonomousAgent + MainChain）
    4. 路由分发（4种路由模式）
    5. 结果归一化与最终处理
    """
    import time as _time
    from .timeout_guard import should_skip_heavy_ops
    from ._somn_analysis import (
        _module_retrieve_similar_experiences,
        _module_upsert_long_term_goal,
        _module_build_autonomy_context,
    )
    from ._somn_evaluation import (
        _evaluate_main_chain_performance as _module_eval_main_chain,
        _generate_next_iteration as _module_generate_next_iteration,
    )

    # Step 1: 任务级超时守护初始化
    _task_guard, _task_start = _init_task_timeout_guard(self)
    self._ensure_runtime()
    context = context or {}
    options = options or {}
    context["_timeout_guard"] = _task_guard

    # Step 2: 需求分析（含快车道检测）
    experience_context = _module_retrieve_similar_experiences(self, description)
    requirement_context = dict(context)
    requirement_context["experience_context"] = experience_context
    requirement = self.analyze_requirement(description, context=requirement_context)
    
    if requirement.get("_fast_lane"):
        logger.info(f"⚡ [快车道] 直接执行路由: {requirement.get('routing_decision', {}).get('route', 'local_llm_fallback')}")
        route = requirement.get("routing_decision", {}).get("route", "local_llm_fallback")
        if route == "local_llm_fallback":
            return self._run_local_llm_route(requirement, options or {})
    
    current_goal = _module_upsert_long_term_goal(self, requirement)
    autonomy_context = _module_build_autonomy_context(current_goal, experience_context)
    requirement["autonomy_context"] = autonomy_context
    routing = requirement.get("routing_decision", {})
    route = routing.get("route", "full_workflow")

    # Step 3: 主线集成
    self._ensure_learning_coordinator()
    if self.learning_coordinator is not None:
        try:
            from ..learning.coordinator import LearningTask, LearningPriority
            task = LearningTask(
                task_id=requirement.get("task_id", "unknown"),
                engine_type="wisdom_analysis",
                priority=LearningPriority.P2_MEDIUM,
                data={"description": description, "requirement": requirement, "routing": routing}
            )
            self.learning_coordinator.add_task(task)
            logger.info(f"[学习协调] 任务 {task.task_id} 已加入学习队列")
        except Exception as e:
            logger.warning(f"[学习协调] 任务加入队列失败: {e}")

    self._ensure_autonomous_agent()
    if self.autonomous_agent is not None:
        try:
            ready_goals = self.autonomous_agent.goal_system.get_ready_goals()
            if ready_goals:
                logger.info(f"[自主智能] {len(ready_goals)} 个目标准备就绪")
                requirement["ready_goals"] = [{"id": g.id, "title": g.title, "status": g.status} for g in ready_goals[:3]]
        except Exception as e:
            logger.warning(f"[自主智能] 目标检查失败: {e}")

    main_chain_result = _inject_main_chain_integration(self, requirement)

    # Step 4: 路由分发
    if route == "orchestrator":
        logger.info(f"[路由A] SomnOrchestrator {routing.get('cuisine_mode')} 模式: {description[:50]}...")
        orch_result = self._run_orchestrator_route(requirement, autonomy_context, options)
        strategy = orch_result.get("strategy", {}) or {}
        execution = orch_result.get("execution", {}) or {}
        evaluation = orch_result.get("evaluation", {}) or {}
        reflection_text = orch_result.get("reflection", "") or ""

    elif route == "local_llm_fallback":
        logger.info(f"[路由B] 本地 LLM 直答: {description[:50]}...")
        llm_result = self._run_local_llm_route(requirement, options)
        strategy = llm_result.get("strategy", {}) or {}
        execution = llm_result.get("execution", {}) or {}
        evaluation = llm_result.get("evaluation", {}) or {}
        reflection_text = llm_result.get("reflection", "") or ""

    elif route == "wisdom_only":
        logger.info(f"[路由C] 智慧板块直答: {description[:50]}...")
        wisdom_result = self._run_wisdom_route(requirement)
        strategy = wisdom_result.get("strategy", {}) or {}
        execution = wisdom_result.get("execution", {}) or {}
        evaluation = wisdom_result.get("evaluation", {}) or {}
        reflection_text = wisdom_result.get("reflection", "") or ""

    elif route == "sage_dispatch":
        logger.info(f"[路由E] SageDispatch贤者调度: {description[:50]}...")
        from ._somn_routes import _module_run_sage_dispatch_route
        sage_result = _module_run_sage_dispatch_route(self, requirement, options)
        strategy = sage_result.get("strategy", {}) or {}
        execution = sage_result.get("execution", {}) or {}
        evaluation = sage_result.get("evaluation", {}) or {}
        reflection_text = sage_result.get("reflection", "") or ""

    elif route == "divine_reason":
        logger.info(f"[路由F] DivineReason统一推理: {description[:50]}...")
        from ._somn_routes import _module_run_divine_reason_route
        reason_result = _module_run_divine_reason_route(self, requirement, options)
        strategy = reason_result.get("strategy", {}) or {}
        execution = reason_result.get("execution", {}) or {}
        evaluation = reason_result.get("evaluation", {}) or {}
        reflection_text = reason_result.get("reflection", "") or ""

    elif route == "tianshu_pipeline":
        logger.info(f"[路由G] 天枢八层管道: {description[:50]}...")
        from ._somn_routes import _module_run_tianshu_pipeline_route
        pipeline_result = _module_run_tianshu_pipeline_route(self, requirement, options)
        strategy = pipeline_result.get("strategy", {}) or {}
        execution = pipeline_result.get("execution", {}) or {}
        evaluation = pipeline_result.get("evaluation", {}) or {}
        reflection_text = pipeline_result.get("reflection", "") or ""

    elif route == "ppt_generate":
        logger.info(f"[路由PPT] PPT子系统强化处理: {description[:50]}...")
        from ._somn_routes import _module_run_ppt_route
        ppt_result = _module_run_ppt_route(self, requirement, options)
        strategy = ppt_result.get("strategy", {}) or {}
        execution = ppt_result.get("execution", {}) or {}
        evaluation = ppt_result.get("evaluation", {}) or {}
        reflection_text = ppt_result.get("reflection", "") or ""

    elif route == "neural_layout":
        logger.info(f"[路由NL] NeuralLayout神经网络布局: {description[:50]}...")
        from ._somn_routes import _module_run_neural_layout_route
        nl_result = _module_run_neural_layout_route(self, requirement, options)
        strategy = nl_result.get("strategy", {}) or {}
        execution = nl_result.get("execution", {}) or {}
        evaluation = nl_result.get("evaluation", {}) or {}
        reflection_text = nl_result.get("reflection", "") or ""

    else:
        strategy, execution, evaluation, reflection_text = _execute_route_D_full_workflow(
            self, description, requirement, options, evaluation_criteria,
            autonomy_context, main_chain_result, _task_guard, _task_start
        )

    # Step 5: 结果归一化与最终处理
    reflection = _normalize_reflection(reflection_text)
    updated_goal = self._store_autonomy_learning(
        requirement, strategy, execution, evaluation, reflection, current_goal
    )
    autonomy_context["current_goal"] = updated_goal

    final_report = _build_final_report(
        requirement, strategy, execution, evaluation, reflection,
        autonomy_context, routing, main_chain_result, description, current_goal
    )

    run_path = self._persist_agent_run(final_report)
    final_report["run_file"] = str(run_path)
    final_report["main_chain_performance"] = _module_eval_main_chain(
        requirement=requirement, strategy=strategy, execution=execution,
        evaluation=evaluation, reflection=reflection,
    )

    return final_report
