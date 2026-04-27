"""
SomnCore 分析辅助方法提取模块 (_somn_analysis.py)
瘦委托: 分析流程相关方法已提取为模块级函数。
"""

import json
import hashlib
import re
import logging
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from concurrent.futures import TimeoutError as FuturesTimeoutError

logger = logging.getLogger(__name__)

# ── 复用主模块中的工具函数（间接引用）────────────────────────
# 注意：这些函数依赖 somn_core 实例，模块级函数通过 somn_core 参数访问
# 不能在此直接 import somn_core，避免循环依赖

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 需求解析
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _module_parse_requirement(
    somn_core,
    description: str,
    extra_context: Dict[str, Any],
) -> Dict[str, Any]:
    """解析需求描述，优先用本地 LLM 输出结构化 JSON。"""
    fallback = {
        "objective": description[:120],
        "task_type": "general_analysis",
        "deliverable": "结构化分析结果",
        "constraints": [],
        "inputs_needed": [],
        "success_definition": "形成可执行输出",
        "metrics": {},
        "timeline": extra_context.get("timeline", "未指定"),
        "priority": extra_context.get("priority", "medium"),
        "risk_points": []
    }

    prompt = f"""
请解析以下任务需求,并只输出 JSON:
{{
  "objective": "任务核心目标",
  "task_type": "任务类别",
  "deliverable": "预期交付物",
  "constraints": ["约束1"],
  "inputs_needed": ["需要的输入"],
  "success_definition": "什么算完成",
  "metrics": {{"metrics名": "目标值"}},
  "timeline": "时间要求",
  "priority": "high/medium/low",
  "risk_points": ["潜在风险"]
}}

任务描述:{description}
额外上下文:{json.dumps(extra_context, ensure_ascii=False)}
"""
    parsed = somn_core._call_llm_for_json(
        prompt=prompt,
        system_prompt="你是需求解析器,只输出合法 JSON.",
        fallback=fallback
    )
    parsed["raw_text"] = description
    return parsed

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 上下文搜索（含熔断 + 缓存）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _module_search_context_info(
    somn_core,
    description: str,
    industry: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    """搜索上下文信息，失败时返回空列表。"""
    try:
        keywords = somn_core._extract_keywords(description)
        from src.data_layer.web_search import SearchQuery, SearchIntent
        query = SearchQuery(
            keywords=keywords[:5] if keywords else [description[:20] or "Somn"],
            intent=SearchIntent.MARKET_RESEARCH,
            max_results=5
        )
        session = somn_core.web_search.search(query)
        return [
            {
                "title": getattr(result, "title", ""),
                "snippet": getattr(result, "snippet", ""),
                "source": getattr(getattr(result, "source", ""), "value", getattr(result, "source", ""))
            }
            for result in session.results[:5]
        ]
    except Exception as exc:
        return [{"title": "search_unavailable", "snippet": str(exc), "source": "local"}]

def _module_build_local_fallback_context(description: str, extract_keywords_fn) -> List[Dict[str, Any]]:
    """构建本地上下文兜底条目。"""
    keywords = extract_keywords_fn(description)
    keyword_str = ", ".join(keywords) if keywords else description[:60]
    return [
        {
            "title": "[本地上下文] 关键词匹配",
            "snippet": f"基于用户输入提取的关键词: {keyword_str}。"
                       f"网络搜索不可用，当前仅依赖本地知识库与记忆系统提供支持。",
            "source": "local_fallback",
            "keywords": keywords,
            "fallback_reason": "search_timeout_or_unavailable",
        },
        {
            "title": "[本地上下文] Somn 智慧体系就绪",
            "snippet": "智慧调度、思维方法融合、行业知识库、记忆检索等本地能力正常可用，"
                       "可独立完成分析任务。",
            "source": "local_fallback",
            "keywords": [],
            "fallback_reason": "search_timeout_or_unavailable",
        }
    ]

def _module_search_context_info_safe(
    somn_core,
    description: str,
    industry=None,
    timeout: float = 3.0,
) -> List[Dict[str, Any]]:
    """
    带超时熔断 + 会话缓存复用的网络搜索包装器.
    三层防护：1. 同会话缓存命中 2. 3s 熔断 3. Circuit Breaker
    """
    import logging

    # ── 第一层：同会话缓存查询 ──
    somn_core._evict_stale_search_cache()
    cached = somn_core._check_search_cache(description)
    if cached is not None:
        return cached

    # ── 第二层：熔断器检查 ──
    cb = somn_core._search_circuit_breaker
    if cb["consecutive_failures"] >= cb["failure_threshold"]:
        if cb["state"] == "open":
            elapsed = (datetime.now() - cb["last_failure_time"]).total_seconds()
            if elapsed < cb["recovery_timeout"]:
                logger.info(f"网络搜索熔断器: OPEN（连续失败 {cb['consecutive_failures']} 次），"
                            f"距离恢复还有 {cb['recovery_timeout'] - elapsed:.0f}s，直接走本地兜底")
                return _module_build_local_fallback_context(
                    description, somn_core._extract_keywords
                )
            else:
                cb["state"] = "half_open"
                logger.info("网络搜索熔断器: HALF_OPEN，尝试恢复探测")

    # ── 带超时执行搜索 ──
    result_holder: List[Any] = []
    error_holder: List[Exception] = []

    def _do_search():
        try:
            result_holder.append(_module_search_context_info(somn_core, description, industry))
        except Exception as exc:
            error_holder.append(exc)

    search_thread = threading.Thread(target=_do_search, daemon=True, name="search_circuit")
    search_thread.start()
    search_thread.join(timeout=timeout)

    if search_thread.is_alive():
        logger.warning(f"网络搜索 3s 熔断触发，跳过等待，使用本地上下文兜底")
        cb["consecutive_failures"] += 1
        cb["last_failure_time"] = datetime.now()
        if cb["consecutive_failures"] >= cb["failure_threshold"]:
            cb["state"] = "open"
            logger.warning(f"网络搜索熔断器: 进入 OPEN 状态（连续 {cb['consecutive_failures']} 次失败）")
        else:
            cb["state"] = "closed"
        return _module_build_local_fallback_context(description, somn_core._extract_keywords)

    if error_holder:
        logger.warning(f"网络搜索异常: {error_holder[0]}，使用本地上下文兜底")
        cb["consecutive_failures"] += 1
        cb["last_failure_time"] = datetime.now()
        if cb["consecutive_failures"] >= cb["failure_threshold"]:
            cb["state"] = "open"
        return _module_build_local_fallback_context(description, somn_core._extract_keywords)

    result = result_holder[0] if result_holder else []

    if result and result[0].get("title") == "search_unavailable":
        logger.warning(f"网络搜索返回不可用: {result[0].get('snippet', '')}")
        cb["consecutive_failures"] += 1
        cb["last_failure_time"] = datetime.now()
        if cb["consecutive_failures"] >= cb["failure_threshold"]:
            cb["state"] = "open"
        return _module_build_local_fallback_context(description, somn_core._extract_keywords)

    # ── 搜索成功 ──
    somn_core._put_search_cache(description, result)
    if cb["state"] == "half_open":
        logger.info("网络搜索熔断器: HALF_OPEN 探测成功，恢复为 CLOSED")
    cb["consecutive_failures"] = 0
    cb["state"] = "closed"
    return result

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 结构化 & 评估
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _module_structure_requirement(
    somn_core,
    parsed: Dict[str, Any],
    search_results: List[Dict[str, Any]],
    extra_context: Dict[str, Any],
    memory_context: Dict[str, Any],
) -> Dict[str, Any]:
    """结构化需求。"""
    objective = parsed.get("objective") or parsed.get("raw_text", "")[:120]
    constraints = parsed.get("constraints", [])
    inputs_needed = parsed.get("inputs_needed", [])
    metrics = parsed.get("metrics", {})
    risk_points = parsed.get("risk_points", [])

    return {
        "objective": objective,
        "task_type": parsed.get("task_type", "general_analysis"),
        "deliverable": parsed.get("deliverable", "结构化输出"),
        "success_definition": parsed.get("success_definition", "形成明确,可复用的结果"),
        "keywords": somn_core._extract_keywords(parsed.get("raw_text", "")),
        "constraints": constraints,
        "inputs_needed": inputs_needed,
        "metrics": metrics,
        "timeline": parsed.get("timeline") or extra_context.get("timeline", "未指定"),
        "priority": parsed.get("priority") or extra_context.get("priority", "medium"),
        "risk_points": risk_points,
        "context_from_search": search_results,
        "memory_evidence": memory_context.get("evidence_chain", []),
        "memory_answer": memory_context.get("answer", "")
    }

def _module_assess_feasibility(
    structured_req: Dict[str, Any],
    industry: Optional[Any] = None,
) -> Dict[str, Any]:
    """基于需求完整度与约束密度评估可行性。"""
    objective_score = 0.2 if structured_req.get("objective") else 0.0
    deliverable_score = 0.15 if structured_req.get("deliverable") else 0.0
    metrics_score = 0.15 if structured_req.get("metrics") else 0.05
    timeline_score = 0.1 if structured_req.get("timeline") and structured_req.get("timeline") != "未指定" else 0.05
    context_score = 0.15 if structured_req.get("context_from_search") else 0.05
    memory_score = 0.1 if structured_req.get("memory_evidence") else 0.03
    missing_inputs_penalty = min(0.2, 0.03 * len(structured_req.get("inputs_needed", [])))
    constraints_penalty = min(0.15, 0.02 * len(structured_req.get("constraints", [])))

    overall = objective_score + deliverable_score + metrics_score + timeline_score + context_score + memory_score
    overall = max(0.15, min(0.95, overall - missing_inputs_penalty - constraints_penalty))

    technical = max(0.2, min(0.95, overall + 0.05 - constraints_penalty))
    resource = max(0.2, min(0.95, overall - missing_inputs_penalty))
    market = max(0.2, min(0.95, overall + (0.05 if industry else 0.0)))

    risks = list(structured_req.get("risk_points", []))
    if structured_req.get("inputs_needed"):
        risks.append("关键输入仍不完整,执行阶段可能需要补采集")
    if structured_req.get("timeline") == "未指定":
        risks.append("时间边界不清晰,可能影响任务优先级和完成标准")

    mitigations = []
    if structured_req.get("inputs_needed"):
        mitigations.append("先补齐最低必要输入,再进入深执行")
    if not structured_req.get("metrics"):
        mitigations.append("先定义成功metrics,避免后续评估失真")
    if not mitigations:
        mitigations.append("可以进入执行阶段,但建议保留复盘检查点")

    return {
        "overall_feasible": overall >= 0.55,
        "overall_score": round(overall, 4),
        "technical_feasibility": round(technical, 4),
        "resource_feasibility": round(resource, 4),
        "market_feasibility": round(market, 4),
        "risks": risks,
        "mitigations": mitigations
    }

def _module_assess_task_routing(
    somn_core,
    description: str,
    structured_req: Dict,
    context: Dict,
) -> Dict[str, Any]:
    """
    评估任务复杂度，决定路由路径 -- v14.0.0.
    复杂度 < 0.35 → orchestrator(fast); < 0.55 → orchestrator(home); else → full_workflow.
    """
    import logging

    semantic_hints = structured_req.get("_semantic_hints", {}) if "_semantic_hints" in structured_req else {}
    intent = semantic_hints.get("inferred_intent", "")
    intent_conf = semantic_hints.get("intent_confidence", 0.0)
    task_type = structured_req.get("task_type", "")
    objective = structured_req.get("objective", description)
    constraints = structured_req.get("constraints", [])

    text = description.strip()
    text_len = len(text)
    text_len_score = min(text_len / 500, 1.0)

    action_keywords = ["帮我", "给我", "generate", "制定", "执行", "完成", "创建", "分析", "评估"]
    has_action = any(kw in text for kw in action_keywords)
    action_score = 0.3 if has_action else 0.0

    execution_keywords = ["执行", "落地", "实施", "操作", "完成", "跑", "运行"]
    has_execution = any(kw in text for kw in execution_keywords)
    execution_score = 0.3 if has_execution else 0.0

    deep_keywords = ["研究", "深度", "论证", "报告", "分析", "strategy", "方案", "全面"]
    has_deep = any(kw in text for kw in deep_keywords)
    deep_score = 0.2 if has_deep else 0.0

    constraint_score = min(len(constraints) * 0.05, 0.2)
    intent_bonus = 0.1 if intent_conf > 0.8 and intent in ("question", "chat") else 0.0
    intent_penalty = 0.3 if intent in ("chat", "greeting", "simple_question") else 0.0

    raw_complexity = (
        text_len_score * 0.15 +
        action_score +
        execution_score +
        deep_score +
        constraint_score -
        intent_bonus -
        intent_penalty
    )
    complexity = max(0.0, min(1.0, raw_complexity))

    if complexity < 0.35:
        route = "orchestrator"
        cuisine_mode = "fast"
        cuisine_level = "simple"
        reasoning = "简单任务,本地模型快速响应(快手菜)"
    elif complexity < 0.55:
        route = "orchestrator"
        cuisine_mode = "home"
        cuisine_level = "medium"
        reasoning = "中等任务,本地+云端老师辅助(家常菜)"
    else:
        route = "full_workflow"
        cuisine_mode = "feast"
        cuisine_level = "complex"
        reasoning = "复杂任务,完整工作流执行(大餐)"

    # 用户显式指定优先
    user_mode_override = context.get("dining_mode") or context.get("cuisine_mode") or context.get("learning_mode")
    if user_mode_override:
        mode_map = {
            "fast": ("orchestrator", "fast", "simple", "用户指定快手菜模式"),
            "home": ("orchestrator", "home", "medium", "用户指定家常菜模式"),
            "feast": ("full_workflow", "feast", "complex", "用户指定大餐模式"),
            "direct": ("orchestrator", "fast", "simple", "用户指定直接模式"),
            "preview": ("orchestrator", "home", "medium", "用户指定预习模式"),
            "review": ("orchestrator", "home", "medium", "用户指定复习模式"),
            "democratic": ("full_workflow", "feast", "complex", "用户指定民主模式"),
        }
        if user_mode_override in mode_map:
            route, cuisine_mode, cuisine_level, reasoning = mode_map[user_mode_override]

    orchestrator_available = somn_core.somn_orchestrator is not None
    cloud_hub_available = somn_core.cloud_model_hub is not None

    if route == "orchestrator" and not orchestrator_available:
        if somn_core.llm_service:
            route = "local_llm_fallback"
            reasoning += "(编排器不可用,回退到本地 LLM)"
        else:
            route = "wisdom_only"
            reasoning += "(无本地 LLM,仅使用智慧板块)"

    result = {
        "route": route,
        "cuisine_mode": cuisine_mode,
        "cuisine_level": cuisine_level,
        "complexity": round(complexity, 3),
        "complexity_signals": {
            "text_length_score": round(text_len_score, 3),
            "action_score": action_score,
            "execution_score": execution_score,
            "deep_score": deep_score,
            "constraint_score": round(constraint_score, 3),
            "intent_bonus": intent_bonus,
            "intent_penalty": intent_penalty,
        },
        "reasoning": reasoning,
        "semantic_intent": intent,
        "intent_confidence": intent_conf,
        "task_type": task_type,
        "orchestrator_available": orchestrator_available,
        "cloud_hub_available": cloud_hub_available,
        "teacher_student_available": somn_core.teacher_student_engine is not None,
    }

    logger.info(
        f"[路由decision] 复杂度={complexity:.2f}({cuisine_level}) | "
        f"路由={route} | 烹饪={cuisine_mode} | 推理={reasoning}"
    )
    return result

def _module_generate_recommendations(
    structured_req: Dict[str, Any],
    feasibility: Dict[str, Any],
    metaphysics_analysis: Optional[Dict[str, Any]] = None,
    wisdom_analysis: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """生成建议。"""
    recommendations = []
    if structured_req.get("inputs_needed"):
        recommendations.append("优先补齐输入项,减少执行时的猜测成本")
    if not structured_req.get("metrics"):
        recommendations.append("先把成功metrics量化,否则后续评估只能做弱judge")
    if feasibility.get("overall_score", 0) < 0.65:
        recommendations.append("先做一轮小范围验证,再扩大执行范围")
    if metaphysics_analysis and metaphysics_analysis.get("triggered"):
        if metaphysics_analysis.get("error"):
            recommendations.append("检测到环境/时机类诉求,但术数时空分析未成功返回,建议先补齐场景结构信息后重试")
        else:
            recommendations.append("环境/时机/结构因素已自动纳入术数时空分析,执行时同步按主攻轴与补位轴推进")
    if wisdom_analysis and wisdom_analysis.get("recommendations"):
        for rec in wisdom_analysis["recommendations"][:2]:
            if rec and rec not in recommendations:
                recommendations.append(f"[智慧洞察] {rec}")
    recommendations.append("执行时保留任务级结果和异常,便于复盘写回记忆")
    return recommendations

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. run_agent_task 辅助方法
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _module_retrieve_similar_experiences(
    somn_core,
    description: str,
    limit: int = 3,
) -> List[Dict[str, Any]]:
    """
    从本地经验库召回相似任务（TF-IDF + 余弦相似度）。
    """
    from ._somn_tfidf import _ensure_experience_index

    experiences = somn_core._read_json_store(somn_core.experience_store_path, [])
    if not experiences:
        return []

    idx = _ensure_experience_index(experiences)
    raw_results = idx.search(description, top_k=limit * 3)

    task_id_to_idx = {exp.get("task_id", str(i)): i for i, exp in enumerate(experiences)}
    scored = []
    seen_ids = set()

    for (task_id, tfidf_score) in raw_results:
        if task_id in seen_ids:
            continue
        exp = next(
            (exp for exp in experiences if exp.get("task_id") == task_id),
            None,
        )
        if exp is None:
            continue
        seen_ids.add(task_id)
        candidate = dict(exp)
        quality_bonus = float(exp.get("overall_score", 0.0)) * 0.25
        candidate["similarity_score"] = round(tfidf_score * 0.75 + quality_bonus, 4)
        candidate["tfidf_score"] = tfidf_score
        scored.append(candidate)

    scored.sort(key=lambda x: x.get("similarity_score", 0.0), reverse=True)
    return scored[:limit]

def _module_upsert_long_term_goal(
    somn_core,
    requirement: Dict[str, Any],
) -> Dict[str, Any]:
    """把当前任务 mapping 到长期目标对象。"""
    from ._somn_types import LongTermGoalRecord

    structured = requirement.get("structured_requirement", {})
    objective = structured.get("objective") or requirement.get("raw_description", "")[:80] or "默认目标"
    goals = somn_core._read_json_store(somn_core.goal_store_path, [])
    goal_id = somn_core._make_goal_id(objective)
    now = datetime.now().isoformat()

    existing = next((goal for goal in goals if goal.get("goal_id") == goal_id), None)
    if existing:
        existing["objective"] = objective
        existing["success_definition"] = structured.get("success_definition", existing.get("success_definition", "形成稳定可复用结果"))
        existing["priority"] = structured.get("priority", existing.get("priority", "medium"))
        existing["constraints"] = structured.get("constraints", existing.get("constraints", []))
        existing["task_type"] = structured.get("task_type", existing.get("task_type", "general_analysis"))
        existing["updated_at"] = now
        somn_core._write_json_store(somn_core.goal_store_path, goals)
        return existing

    record = LongTermGoalRecord(
        goal_id=goal_id,
        objective=objective,
        success_definition=structured.get("success_definition", "形成稳定可复用结果"),
        priority=structured.get("priority", "medium"),
        constraints=structured.get("constraints", []),
        task_type=structured.get("task_type", "general_analysis"),
        last_run_task_id=requirement.get("task_id")
    ).to_dict()
    goals.append(record)
    somn_core._write_json_store(somn_core.goal_store_path, goals)
    return record

def _module_build_autonomy_context(
    current_goal: Dict[str, Any],
    experience_context: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """整理自治上下文，供 strategy 和复盘阶段复用。"""
    strategy_hints = []
    for item in experience_context:
        if item.get("overall_score", 0.0) < 0.6:
            continue
        for action in item.get("reusable_actions", [])[:2]:
            if action not in strategy_hints:
                strategy_hints.append(action)
        for lesson in item.get("lessons_learned", [])[:1]:
            hint = f"复用经验:{lesson}"
            if hint not in strategy_hints:
                strategy_hints.append(hint)

    return {
        "current_goal": current_goal,
        "similar_experiences": experience_context,
        "strategy_hints": strategy_hints[:5]
    }
