"""
__all__ = [
    'build_candidate_strategies',
    'build_strategy_context',
    'build_strategy_learning_guidance',
    'build_strategy_plan',
    'build_workflow_reference_base',
    'contains_any',
    'generate_structured_strategy',
    'rank_strategy_candidates',
    'run_parallel_strategy_generation',
]

SomnCore 策略设计模块
策略学习引导，工作流基准、候选策略构建与排序。
"""

import json
import hashlib
import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════
# 策略学习引导
# ══════════════════════════════════════════════════════

def build_strategy_learning_guidance(
    get_reinforcement_trigger_fn,
    get_roi_tracker_fn,
    clamp_fn,
) -> Dict[str, Any]:
    """在strategy设计前读取历史 Q 表/ROI,让默认strategy选择更稳."""
    rl_trigger = get_reinforcement_trigger_fn()
    roi_tracker = get_roi_tracker_fn()

    q_values = rl_trigger.get_q_values() if rl_trigger else {}
    best_action, best_q = rl_trigger.get_best_action() if rl_trigger else (None, 0.5)
    best_strategy_roi = roi_tracker.get_strategy_roi(best_action) if roi_tracker and best_action else {}
    best_sample_count = int(best_strategy_roi.get("sample_count", 0) or 0)
    best_confidence = clamp_fn(
        max(
            rl_trigger.get_action_confidence(best_action) if rl_trigger and best_action else 0.0,
            min(1.0, best_sample_count / 20.0) if best_sample_count > 0 else 0.0,
        ),
        0.0,
    )
    degraded_q = round(0.5 + (float(best_q or 0.5) - 0.5) * best_confidence, 4)
    baseline_raw = roi_tracker.get_baseline() if roi_tracker else {}

    baseline_confidence = clamp_fn((baseline_raw or {}).get("confidence"), 0.0)

    top_actions: List[Dict[str, Any]] = []
    if q_values and rl_trigger:
        for action, q_value in sorted(q_values.items(), key=lambda item: item[1], reverse=True)[:3]:
            strategy_roi = roi_tracker.get_strategy_roi(action) if roi_tracker else {}
            sample_count = int(strategy_roi.get("sample_count", 0) or 0)
            action_confidence = clamp_fn(
                max(
                    rl_trigger.get_action_confidence(action),
                    min(1.0, sample_count / 20.0) if sample_count > 0 else 0.0,
                ),
                0.0,
            )
            degraded_value = round(0.5 + (float(q_value or 0.5) - 0.5) * action_confidence, 4)
            top_actions.append({
                "action": action,
                "q_value": round(float(q_value or 0.5), 4),
                "degraded_q": degraded_value,
                "confidence": action_confidence,
                "sample_count": sample_count,
            })

    if not q_values:
        mode = "cold_start_default"
        preferred_action = "balanced_exploration"
        note = "暂无历史 Q 表与 ROI 样本,默认采用稳健探索:先拆成可验证小步,保留回退,避免单strategy重押."
        planning_policy = [
            "优先可验证,可回退的步骤拆分",
            "先探索再收敛,不把偶发结果误当最优strategy",
            "保留显式评估metrics,为后续学习积累样本",
        ]
    elif best_action and best_confidence < 0.35:
        mode = "confidence_degraded"
        preferred_action = best_action
        note = (
            f"历史存在但样本不足,{best_action} 的置信度仅 {best_confidence:.2f};"
            f"其 Q 值已向 0.5 退化为 {degraded_q:.3f},仅作为弱引导,仍需保留探索与兜底."
        )
        planning_policy = [
            "参考历史最优动作,但不要做强绑定",
            "通过多方案并行或小样本试探继续积累数据",
            "对低置信度strategy保留兜底执行路径",
        ]
    else:
        mode = "history_guided"
        preferred_action = best_action or "balanced_exploration"
        note = (
            f"历史样本已具备一定稳定性,可优先复用 {preferred_action};"
            f"当前置信度 {best_confidence:.2f},退化后参考值 {degraded_q:.3f}."
        )
        planning_policy = [
            "优先复用已验证动作,同时保留少量探索空间",
            "围绕高 ROI 动作安排更多关键步骤",
            "持续记录显式反馈,避免strategy老化后失真",
        ]

    baseline_dict = {
        "avg_efficiency": round(float((baseline_raw or {}).get("avg_efficiency", 0.5) or 0.5), 4),
        "avg_quality": round(float((baseline_raw or {}).get("avg_quality", 0.5) or 0.5), 4),
        "adopt_rate": round(float((baseline_raw or {}).get("adopt_rate", 0.5) or 0.5), 4),
        "avg_roi": round(float((baseline_raw or {}).get("avg_roi", 0.0) or 0.0), 4),
    }

    return {
        "mode": mode,
        "preferred_action": preferred_action,
        "best_action": best_action or "",
        "best_q": round(float(best_q or 0.5), 4),
        "degraded_q": degraded_q,
        "confidence": round(best_confidence, 4),
        "baseline_confidence": round(baseline_confidence, 4),
        "baseline": baseline_dict,
        "top_actions": top_actions,
        "planning_policy": planning_policy,
        "prompt_bias": note,
    }

# ══════════════════════════════════════════════════════
# 工作流基准
# ══════════════════════════════════════════════════════

def build_workflow_reference_base(
    requirement_doc: Dict[str, Any],
    industry: str,
    stage: str,
) -> str:
    """为strategy排序generate稳定的工作流参考基准."""
    structured_requirement = requirement_doc.get("structured_requirement", {}) if isinstance(requirement_doc, dict) else {}
    signature_payload = {
        "task_id": requirement_doc.get("task_id", "") if isinstance(requirement_doc, dict) else "",
        "industry": industry or "general",
        "stage": stage or "growth",
        "objective": structured_requirement.get("objective", "") if isinstance(structured_requirement, dict) else "",
        "constraints": structured_requirement.get("constraints", []) if isinstance(structured_requirement, dict) else [],
        "metrics": sorted((structured_requirement.get("metrics", {}) or {}).keys()) if isinstance(structured_requirement, dict) else [],
    }
    signature_text = json.dumps(signature_payload, ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha1(signature_text.encode("utf-8")).hexdigest()[:12]

    objective = str(signature_payload.get("objective") or signature_payload.get("task_id") or "general_strategy")
    objective_key = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "_", objective.lower()).strip("_")[:24] or "general_strategy"
    industry_key = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "_", str(industry or "general").lower()).strip("_") or "general"
    stage_key = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "_", str(stage or "growth").lower()).strip("_") or "growth"
    return f"wfref::{industry_key}::{stage_key}::{objective_key}::{digest}"

# ══════════════════════════════════════════════════════
# 候选策略构建
# ══════════════════════════════════════════════════════

def build_candidate_strategies(
    requirement_doc: Dict[str, Any],
    reinforcement_guidance: Dict[str, Any],
    workflow_reference_base: str,
) -> List[Dict[str, Any]]:
    """构建待排序的候选strategy集合."""
    structured_requirement = requirement_doc.get("structured_requirement", {}) if isinstance(requirement_doc, dict) else {}
    objective = str(structured_requirement.get("objective", "") or "")
    constraints = structured_requirement.get("constraints", []) if isinstance(structured_requirement, dict) else []
    if isinstance(constraints, str):
        constraints = [constraints]
    metrics = structured_requirement.get("metrics", {}) if isinstance(structured_requirement, dict) else {}
    objective_text = " ".join([
        objective,
        " ".join(str(item) for item in constraints),
        " ".join(str(key) for key in (metrics or {}).keys()),
    ]).lower()

    def contains_any(keywords):
        return any(kw in objective_text for kw in keywords)

    risk_sensitive = contains_any(["稳", "风险", "安全", "合规", "预算", "成本", "回退", "约束", "稳定"])
    growth_or_breakthrough = contains_any(["增长", "突破", "创新", "破局", "拉新", "竞争", "差异", "扩张"])
    complex_problem = len(constraints) >= 3 or contains_any(["复杂", "协同", "组合", "多目标", "系统"])
    preferred_action = str((reinforcement_guidance or {}).get("preferred_action") or "balanced_exploration")
    top_actions = [
        str(item.get("action"))
        for item in (reinforcement_guidance or {}).get("top_actions", [])
        if isinstance(item, dict) and item.get("action")
    ]

    combo_seed = []
    for action in [preferred_action, *top_actions, "balanced_exploration", "conservative_execution", "high_creativity_attack"]:
        if action and action not in combo_seed:
            combo_seed.append(action)
        if len(combo_seed) >= 3:
            break
    if len(combo_seed) < 2:
        combo_seed.extend(["balanced_exploration", "conservative_execution"])
    combo_seed = [item for index, item in enumerate(combo_seed) if item and item not in combo_seed[:index]][:3]

    templates = [
        {
            "action": "balanced_exploration",
            "label": "稳健探索",
            "strategy_combo": ["balanced_exploration"],
            "alignment_score": 0.62 + (0.06 if complex_problem else 0.02),
            "selection_bias": 0.08 if (reinforcement_guidance or {}).get("mode") == "cold_start_default" else 0.03,
            "risk_penalty": 0.04,
            "execution_style": "先探索后收敛,优先拿到可验证样本",
        },
        {
            "action": "conservative_execution",
            "label": "保守执行",
            "strategy_combo": ["conservative_execution"],
            "alignment_score": 0.58 + (0.12 if risk_sensitive else 0.0) + (0.04 if len(constraints) >= 2 else 0.0),
            "selection_bias": 0.05 if risk_sensitive else 0.0,
            "risk_penalty": 0.02,
            "execution_style": "优先稳定性,风险隔离与确定性交付",
        },
        {
            "action": "high_creativity_attack",
            "label": "高创造突击",
            "strategy_combo": ["high_creativity_attack"],
            "alignment_score": 0.54 + (0.14 if growth_or_breakthrough else 0.0),
            "selection_bias": 0.04 if growth_or_breakthrough else 0.0,
            "risk_penalty": 0.11,
            "execution_style": "优先拉开差异化,接受更高试错波动",
        },
        {
            "action": "multi_strategy_combo",
            "label": "组合拳协同",
            "strategy_combo": combo_seed,
            "alignment_score": 0.57 + (0.1 if complex_problem else 0.03),
            "selection_bias": 0.04 if complex_problem else 0.0,
            "risk_penalty": 0.07 + max(0, len(combo_seed) - 2) * 0.02,
            "execution_style": "把高价值动作组合成组合拳,换取更高上限",
        },
        {
            "action": "fallback_safe_mode",
            "label": "兜底安全模式",
            "strategy_combo": ["fallback_safe_mode"],
            "alignment_score": 0.48 + (0.12 if risk_sensitive else 0.0),
            "selection_bias": 0.03 if len(constraints) >= 3 else 0.0,
            "risk_penalty": 0.0,
            "execution_style": "优先保证不失控,再逐步恢复优化",
        },
    ]

    known_actions = {item["action"] for item in templates}
    if preferred_action and preferred_action not in known_actions:
        templates.append({
            "action": preferred_action,
            "label": f"历史优选::{preferred_action}",
            "strategy_combo": [preferred_action],
            "alignment_score": 0.58,
            "selection_bias": 0.06 if (reinforcement_guidance or {}).get("mode") == "history_guided" else 0.03,
            "risk_penalty": 0.04,
            "execution_style": "直接复用历史高收益动作,但保留兜底路径",
        })

    candidates = []
    for template in templates:
        combo = [item for item in template.get("strategy_combo", []) if item]
        action = str(template.get("action") or "balanced_exploration")
        workflow_reference_id = f"{workflow_reference_base}::{action}"
        candidates.append({
            **template,
            "strategy_combo": combo or [action],
            "workflow_reference_base": workflow_reference_base,
            "workflow_reference_id": workflow_reference_id,
            "goal": objective,
            "constraints": constraints,
            "preferred": action == preferred_action,
            "historical_hint": action in top_actions or action == preferred_action,
        })
    return candidates

# ══════════════════════════════════════════════════════
# 策略排序
# ══════════════════════════════════════════════════════

def rank_strategy_candidates(
    candidates: List[Dict[str, Any]],
    reinforcement_guidance: Dict[str, Any],
    workflow_reference_base: str,
    get_reinforcement_trigger_fn,
    get_roi_tracker_fn,
    clamp_fn,
) -> Dict[str, Any]:
    """按 Q 值 + task/workflow/combo ROI synthesize排序候选strategy."""
    if not candidates:
        fallback_action = str((reinforcement_guidance or {}).get("preferred_action") or "balanced_exploration")
        fallback = {
            "action": fallback_action,
            "label": fallback_action,
            "strategy_combo": [fallback_action],
            "workflow_reference_base": workflow_reference_base,
            "workflow_reference_id": f"{workflow_reference_base}::{fallback_action}",
            "final_score": 0.5,
            "reasoning": ["候选集为空,使用默认稳健探索兜底"],
        }
        return {
            "candidate_rankings": [fallback],
            "chosen_strategy": fallback,
            "rejected_strategies": [],
            "selector_summary": {
                "mode": (reinforcement_guidance or {}).get("mode", "unknown"),
                "selected_action": fallback_action,
                "selection_margin": 0.0,
                "total_candidates": 1,
            },
            "workflow_reference_id": fallback.get("workflow_reference_id", workflow_reference_base),
        }

    rl_trigger = get_reinforcement_trigger_fn()
    roi_tracker = get_roi_tracker_fn()
    q_values = rl_trigger.get_q_values() if rl_trigger else {}
    baseline = (reinforcement_guidance or {}).get("baseline", {}) if isinstance(reinforcement_guidance, dict) else {}
    baseline_efficiency = clamp_fn(baseline.get("avg_efficiency"), 0.5)
    baseline_confidence = clamp_fn((reinforcement_guidance or {}).get("baseline_confidence"), 0.0)
    mode = str((reinforcement_guidance or {}).get("mode") or "cold_start_default")
    preferred_action = str((reinforcement_guidance or {}).get("preferred_action") or "balanced_exploration")

    ranked = []
    for candidate in candidates:
        action = str(candidate.get("action") or "balanced_exploration")
        combo = [item for item in candidate.get("strategy_combo", []) if item]
        workflow_reference_id = str(candidate.get("workflow_reference_id") or f"{workflow_reference_base}::{action}")

        action_q_raw = float(q_values.get(action, 0.5) or 0.5)
        if action in q_values:
            action_confidence = clamp_fn(
                rl_trigger.get_action_confidence(action) if rl_trigger else 0.0,
                0.0,
            )
        else:
            action_confidence = 0.0

        if action == preferred_action and mode != "cold_start_default":
            action_q_score = clamp_fn(
                0.5 + (action_q_raw - 0.5) * max(action_confidence, clamp_fn((reinforcement_guidance or {}).get("confidence"), 0.0)),
                baseline_efficiency,
            )
        else:
            action_q_score = clamp_fn(
                0.5 + (action_q_raw - 0.5) * action_confidence,
                baseline_efficiency,
            )

        strategy_roi_raw = roi_tracker.get_strategy_roi(action) if roi_tracker else {"status": "no_data"}
        strategy_roi_score = clamp_fn(strategy_roi_raw.get("avg_efficiency_score"), baseline_efficiency)
        strategy_sample_count = int(strategy_roi_raw.get("sample_count", 0) or 0)

        workflow_roi_raw = roi_tracker.get_workflow_roi(workflow_reference_id) if roi_tracker else {"status": "no_data"}
        if workflow_roi_raw.get("status") == "no_data" and workflow_reference_base:
            workflow_roi_raw = roi_tracker.get_workflow_roi(workflow_reference_base) if roi_tracker else {"status": "no_data"}
        workflow_roi_score = clamp_fn(workflow_roi_raw.get("avg_efficiency_score"), baseline_efficiency)

        combo_roi_raw = (
            roi_tracker.get_strategy_combo_roi(strategy_combo=combo)
            if roi_tracker and len(combo) >= 2
            else {"status": "no_data"}
        )
        combo_roi_score = clamp_fn(combo_roi_raw.get("avg_efficiency_score"), baseline_efficiency)

        aggregate_confidence = clamp_fn(
            max(
                action_confidence,
                min(1.0, strategy_sample_count / 20.0) if strategy_sample_count > 0 else 0.0,
                float(strategy_roi_raw.get("confidence", 0.0) or 0.0),
                float(workflow_roi_raw.get("confidence", 0.0) or 0.0),
                float(combo_roi_raw.get("confidence", 0.0) or 0.0),
                baseline_confidence,
            ),
            0.0,
        )
        alignment_score = clamp_fn(candidate.get("alignment_score"), 0.55)
        selection_bias = float(candidate.get("selection_bias", 0.0) or 0.0)
        if mode == "history_guided" and action == preferred_action:
            selection_bias += 0.04
        elif mode == "confidence_degraded" and action == preferred_action:
            selection_bias += 0.02
        elif mode == "cold_start_default" and action == "balanced_exploration":
            selection_bias += 0.03

        final_score = clamp_fn(
            action_q_score * 0.35
            + strategy_roi_score * 0.2
            + workflow_roi_score * 0.15
            + combo_roi_score * 0.15
            + alignment_score * 0.1
            + aggregate_confidence * 0.05
            + selection_bias
            - float(candidate.get("risk_penalty", 0.0) or 0.0),
            baseline_efficiency,
        )

        reasoning = [
            f"Q({action})={action_q_score:.3f}",
            f"taskROI={strategy_roi_score:.3f}/{strategy_sample_count}样本",
            f"workflowROI={workflow_roi_score:.3f}",
            f"comboROI={combo_roi_score:.3f}",
            f"alignment={alignment_score:.3f}",
            f"confidence={aggregate_confidence:.3f}",
        ]
        if selection_bias:
            reasoning.append(f"bias={selection_bias:+.3f}")
        risk_penalty = float(candidate.get("risk_penalty", 0.0) or 0.0)
        if risk_penalty:
            reasoning.append(f"risk_penalty={risk_penalty:.3f}")

        ranked.append({
            **candidate,
            "q_value": round(action_q_raw, 4),
            "q_score": round(action_q_score, 4),
            "task_roi_score": round(strategy_roi_score, 4),
            "workflow_roi_score": round(workflow_roi_score, 4),
            "combo_roi_score": round(combo_roi_score, 4),
            "sample_count": strategy_sample_count,
            "confidence": round(aggregate_confidence, 4),
            "final_score": round(final_score, 4),
            "score_breakdown": {
                "q_score": round(action_q_score, 4),
                "task_roi_score": round(strategy_roi_score, 4),
                "workflow_roi_score": round(workflow_roi_score, 4),
                "combo_roi_score": round(combo_roi_score, 4),
                "alignment_score": round(alignment_score, 4),
                "confidence": round(aggregate_confidence, 4),
                "selection_bias": round(selection_bias, 4),
                "risk_penalty": round(risk_penalty, 4),
            },
            "reasoning": reasoning,
        })

    ranked.sort(
        key=lambda item: (
            float(item.get("final_score", 0.0) or 0.0),
            float(item.get("confidence", 0.0) or 0.0),
            int(item.get("sample_count", 0) or 0),
        ),
        reverse=True,
    )
    chosen_strategy = ranked[0]
    runner_up_score = float(ranked[1].get("final_score", 0.0) or 0.0) if len(ranked) > 1 else 0.0
    selector_summary = {
        "mode": mode,
        "preferred_action": preferred_action,
        "selected_action": chosen_strategy.get("action", ""),
        "selected_label": chosen_strategy.get("label", ""),
        "selection_margin": round(float(chosen_strategy.get("final_score", 0.0) or 0.0) - runner_up_score, 4),
        "total_candidates": len(ranked),
        "baseline_efficiency": baseline_efficiency,
        "baseline_confidence": baseline_confidence,
        "top_actions": (reinforcement_guidance or {}).get("top_actions", []),
    }
    return {
        "candidate_rankings": ranked,
        "chosen_strategy": chosen_strategy,
        "rejected_strategies": ranked[1:],
        "selector_summary": selector_summary,
        "workflow_reference_id": chosen_strategy.get("workflow_reference_id", workflow_reference_base),
    }

# ══════════════════════════════════════════════════════
# Strategy Context 构建
# ══════════════════════════════════════════════════════

def build_strategy_context(
    requirement_doc: Dict[str, Any],
    industry: str,
    stage: str,
    metrics: Dict[str, Any],
    autonomy_context: Dict[str, Any],
    metaphysics_analysis: Dict[str, Any],
    wisdom_analysis: Dict[str, Any],
    playbooks: List[Any],
    triggered_rules: List[Any],
    reinforcement_guidance: Dict[str, Any],
    strategy_selector: Dict[str, Any],
    workflow_reference_base: str,
) -> Dict[str, Any]:
    """构建 strategy_context，供 LLM strategy 生成使用."""
    chosen_strategy = strategy_selector.get("chosen_strategy", {})
    structured_req = requirement_doc.get("structured_requirement", {})

    return {
        "industry": industry,
        "stage": stage,
        "objective": structured_req.get("objective"),
        "metrics": metrics,
        "constraints": structured_req.get("constraints", []),
        "context": {
            "playbooks": [getattr(p, "name", "") for p in playbooks[:3]],
            "rule_recommendations": [getattr(r, "actions_taken", []) for r in triggered_rules[:5]],
            "experience_hints": autonomy_context.get("strategy_hints", []),
            "current_goal": autonomy_context.get("current_goal", {}),
            "similar_experiences": requirement_doc.get("experience_context", [])[:3],
            "metaphysics_summary": metaphysics_analysis.get("summary", ""),
            "metaphysics_action_plan": metaphysics_analysis.get("action_plan", {}),
            "metaphysics_trigger_reason": metaphysics_analysis.get("trigger_reason", []),
            "wisdom_insights": wisdom_analysis.get("insights", []),
            "wisdom_schools": wisdom_analysis.get("activated_schools", []),
            "wisdom_recommendations": wisdom_analysis.get("recommendations", []),
            "thinking_method": wisdom_analysis.get("thinking_method", ""),
            "reinforcement_guidance": reinforcement_guidance,
            "planning_policy": reinforcement_guidance.get("planning_policy", []),
            "historical_action_bias": reinforcement_guidance.get("prompt_bias", ""),
            "candidate_rankings": strategy_selector.get("candidate_rankings", []),
            "selected_learning_strategy": chosen_strategy,
            "selected_strategy_combo": chosen_strategy.get("strategy_combo", []),
            "rejected_strategies": strategy_selector.get("rejected_strategies", []),
            "strategy_selector_summary": strategy_selector.get("selector_summary", {}),
            "workflow_reference_id": strategy_selector.get("workflow_reference_id", workflow_reference_base),
        }
    }

# ══════════════════════════════════════════════════════
# 并行策略生成
# ══════════════════════════════════════════════════════

def run_parallel_strategy_generation(
    requirement_doc: Dict[str, Any],
    strategy_context: Dict[str, Any],
    run_unified_fn,
    llm_service,
    get_executor_fn,
    timeout: float = 20.0,
) -> tuple:
    """
    并行执行 unified_enhancement 和 LLM generate_strategy。
    返回 (unified_enhancement, llm_strategy)。
    """
    unified_holder: List[Any] = [None]
    llm_strategy_holder: List[Any] = [None]

    def _run_unified_safe():
        try:
            unified_holder[0] = run_unified_fn(
                requirement_doc=requirement_doc,
                strategy_context=strategy_context,
            )
        except Exception as e:
            logger.warning(f"[并行strategy] unified_enhancement 失败: {e}")
            unified_holder[0] = {"triggered": False, "modules_activated": [], "enhancement_insights": [], "source": "error"}

    def _run_llm_strategy_safe():
        try:
            llm_strategy_holder[0] = llm_service.generate_strategy(strategy_context)
        except Exception as e:
            logger.warning(f"[并行strategy] generate_strategy 失败: {e}")
            llm_strategy_holder[0] = {"strategy_text": "", "context": strategy_context}

    executor = get_executor_fn()
    f_unified = executor.submit(_run_unified_safe)
    f_llm = executor.submit(_run_llm_strategy_safe)

    for f in [f_unified, f_llm]:
        try:
            f.result(timeout=timeout)
        except Exception as e:
            logger.debug(f"并行策略设计超时: {e}")
    unified_enhancement = unified_holder[0] or {"triggered": False, "modules_activated": [], "enhancement_insights": [], "source": "none"}
    llm_strategy = llm_strategy_holder[0] or {"strategy_text": "", "context": strategy_context}
    return unified_enhancement, llm_strategy

# ══════════════════════════════════════════════════════
# Strategy Plan 构建
# ══════════════════════════════════════════════════════

def build_strategy_plan(
    task_id: str,
    requirement_doc: Dict[str, Any],
    industry: str,
    stage: str,
    llm_strategy: Dict[str, Any],
    structured_strategy: Dict[str, Any],
    reinforcement_guidance: Dict[str, Any],
    strategy_selector: Dict[str, Any],
    workflow_reference_base: str,
    metaphysics_analysis: Dict[str, Any],
    wisdom_analysis: Dict[str, Any],
    unified_enhancement: Dict[str, Any],
    playbooks: List[Any],
    triggered_rules: List[Any],
    industry_profile: Any,
    autonomy_context: Dict[str, Any],
) -> Dict[str, Any]:
    """构建最终的 strategy_plan 字典."""
    chosen_strategy = strategy_selector.get("chosen_strategy", {})

    if isinstance(structured_strategy, dict):
        structured_strategy.setdefault("selected_learning_strategy", chosen_strategy)
        structured_strategy.setdefault("strategy_combo", chosen_strategy.get("strategy_combo", []))
        structured_strategy.setdefault("candidate_rankings", strategy_selector.get("candidate_rankings", [])[:3])
        structured_strategy.setdefault("workflow_reference_id", strategy_selector.get("workflow_reference_id", workflow_reference_base))

    return {
        "task_id": task_id,
        "based_on_requirement": requirement_doc.get("task_id"),
        "industry": industry,
        "stage": stage,
        "strategy_overview": llm_strategy.get("strategy_text", ""),
        "structured_strategy": structured_strategy,
        "reinforcement_guidance": reinforcement_guidance,
        "candidate_rankings": strategy_selector.get("candidate_rankings", []),
        "chosen_strategy": chosen_strategy,
        "rejected_strategies": strategy_selector.get("rejected_strategies", []),
        "strategy_selector_summary": strategy_selector.get("selector_summary", {}),
        "workflow_reference_base": workflow_reference_base,
        "workflow_reference_id": strategy_selector.get("workflow_reference_id", workflow_reference_base),
        "strategy_combo": chosen_strategy.get("strategy_combo", []),
        "metaphysics_analysis": metaphysics_analysis,
        "wisdom_analysis": wisdom_analysis,
        "unified_enhancement": unified_enhancement,
        "applicable_playbooks": [p.to_dict() for p in playbooks[:3]] if playbooks else [],
        "rule_based_insights": [
            {
                "rule_id": getattr(r, "rule_id", ""),
                "actions": getattr(r, "actions_taken", []),
                "confidence": getattr(r, "confidence", 0.0)
            }
            for r in triggered_rules
        ],
        "industry_profile": industry_profile.to_dict() if industry_profile and hasattr(industry_profile, "to_dict") else {},
        "autonomy_context": autonomy_context,
        "generated_at": __import__("datetime").datetime.now().isoformat(),
    }

# ══════════════════════════════════════════════════════
# 结构化策略生成
# ══════════════════════════════════════════════════════

def generate_structured_strategy(
    requirement_doc: Dict[str, Any],
    industry_profile: Any,
    playbooks: List[Any],
    rule_results: List[Any],
    stage: str,
    strategy_ranking: Optional[Dict[str, Any]] = None,
    call_llm_fn: Optional[callable] = None,
    somn_core_instance: Any = None,  # [v1.0.0] 用于情绪研究框架整合
) -> Dict[str, Any]:
    """
    生成结构化策略。
    支持直接返回（无 LLM 时）或通过 LLM 生成。
    [v1.0.0] 整合情绪研究体系框架指导
    """
    import json

    structured_requirement = requirement_doc.get("structured_requirement", {})
    metaphysics_analysis = requirement_doc.get("metaphysics_analysis") or {}
    strategy_ranking = strategy_ranking or {}
    chosen_strategy = strategy_ranking.get("chosen_strategy", {}) if isinstance(strategy_ranking, dict) else {}

    fallback_principles = ["先明确目标", "先打通主链", "先做可验证闭环"]
    if metaphysics_analysis.get("triggered") and not metaphysics_analysis.get("error"):
        fallback_principles.append("环境,时机与结构因素同步纳入decision")
    if chosen_strategy.get("action"):
        fallback_principles.append(f"学习排序器建议优先采用 {chosen_strategy.get('action')}")

    fallback_risk_controls = list(requirement_doc.get("feasibility_assessment", {}).get("mitigations", []))
    if metaphysics_analysis.get("triggered") and not metaphysics_analysis.get("error"):
        fallback_risk_controls.append("执行过程中同步校准环境布局,推进节奏与补位动作")

    # [v1.0.0] 获取情绪研究框架指导
    emotion_framework_guidance = {}
    try:
        if somn_core_instance and hasattr(somn_core_instance, '_emotion_research_validate'):
            from ._somn_emotion_research import build_strategy_with_framework
            raw_description = requirement_doc.get("raw_description", "")
            validation_result = requirement_doc.get("context", {}).get("_emotion_framework_validation", {})
            emotion_framework_guidance = build_strategy_with_framework(raw_description, validation_result)
            logger.info(f"[情绪研究框架] 策略指导已生成: {len(emotion_framework_guidance.get('framework_based_strategy', {}).get('research_dimensions', {}))}个维度")
    except Exception as e:
        logger.warning(f"[情绪研究框架] 策略指导生成失败(不影响主流程): {e}")

    # [v1.0.0] 将情绪研究框架原则融入fallback原则
    enhanced_principles = fallback_principles.copy()
    if emotion_framework_guidance.get("design_principles"):
        enhanced_principles.extend(emotion_framework_guidance["design_principles"][:3])
    
    # [v1.0.0] 将神经科学洞察融入风险管控
    enhanced_risk_controls = fallback_risk_controls.copy()
    if emotion_framework_guidance.get("neuroscience_insights"):
        enhanced_risk_controls.extend([f"[神经科学] {insight}" for insight in emotion_framework_guidance["neuroscience_insights"][:2]])
    if emotion_framework_guidance.get("risk_control_points"):
        enhanced_risk_controls.extend(emotion_framework_guidance["risk_control_points"][:2])

    fallback = {
        "overview": f'围绕目标"{structured_requirement.get("objective", "")}"建立单主链执行方案.',
        "strategy_principles": enhanced_principles,
        "core_actions": [
            {
                "name": "建立主链任务定义",
                "objective": "把需求,strategy,执行,评估打通",
                "expected_effect": "形成可复用任务闭环"
            }
        ],
        "execution_steps": [
            {
                "step": 1,
                "name": "拆解任务",
                "goal": "产出可执行步骤",
                "required_tools": ["llm_chat"],
                "expected_output": "步骤清单"
            }
        ],
        "success_metrics": structured_requirement.get("metrics", {}),
        "risk_controls": enhanced_risk_controls,
        "selected_learning_strategy": chosen_strategy,
        "candidate_rankings": strategy_ranking.get("candidate_rankings", [])[:3] if isinstance(strategy_ranking, dict) else [],
        "workflow_reference_id": strategy_ranking.get("workflow_reference_id", "") if isinstance(strategy_ranking, dict) else "",
        # [v1.0.0] 新增情绪研究框架元数据
        "_emotion_framework_meta": {
            "validation_coverage": emotion_framework_guidance.get("framework_based_strategy", {}).get("validation", {}).get("coverage_score", 0),
            "matched_intersections": emotion_framework_guidance.get("framework_based_strategy", {}).get("validation", {}).get("matched_intersections", []),
            "neuroscience_insights_count": len(emotion_framework_guidance.get("neuroscience_insights", [])),
            "ai_applications_count": len(emotion_framework_guidance.get("ai_application_suggestions", [])),
        } if emotion_framework_guidance else None,
    }

    # 如果没有 LLM 调用函数，直接返回 fallback
    if call_llm_fn is None:
        return fallback

    prompt = f"""
你是 Somn 的strategy规划器.请基于输入generate JSON,不要输出其他文字.
JSON 结构:
{{
  "overview": "总体strategy概述",
  "strategy_principles": ["原则1"],
  "core_actions": [
    {{"name": "动作名", "objective": "动作目标", "expected_effect": "预期效果"}}
  ],
  "execution_steps": [
    {{"step": 1, "name": "步骤名称", "goal": "步骤目标", "required_tools": ["llm_chat"], "expected_output": "输出物"}}
  ],
  "success_metrics": {{"metrics": "目标值"}},
  "risk_controls": ["风险控制措施"],
  "selected_learning_strategy": {{"action": "strategy动作", "final_score": 0.0}},
  "candidate_rankings": [{{"action": "候选strategy", "final_score": 0.0}}],
  "workflow_reference_id": "工作流参考ID"
}}

需求:{json.dumps(structured_requirement, ensure_ascii=False)}
阶段:{stage}
行业画像:{json.dumps(industry_profile.to_dict(), ensure_ascii=False) if industry_profile and hasattr(industry_profile, 'to_dict') else '{}'}
可用 playbooks:{json.dumps([p.to_dict() for p in playbooks[:3]], ensure_ascii=False) if playbooks else '[]'}
规则结果:{json.dumps([{"rule_id": getattr(r, 'rule_id', ''), "actions": getattr(r, 'actions_taken', [])} for r in rule_results], ensure_ascii=False)}
学习排序器:{json.dumps({"chosen_strategy": chosen_strategy, "candidate_rankings": strategy_ranking.get("candidate_rankings", [])[:3] if isinstance(strategy_ranking, dict) else [], "selector_summary": strategy_ranking.get("selector_summary", {}) if isinstance(strategy_ranking, dict) else {}}, ensure_ascii=False)}
术数时空输入:{json.dumps({"triggered": metaphysics_analysis.get("triggered", False), "summary": metaphysics_analysis.get("summary", ""), "action_plan": metaphysics_analysis.get("action_plan", {}), "trigger_reason": metaphysics_analysis.get("trigger_reason", [])}, ensure_ascii=False)}
"""

    return call_llm_fn(
        prompt=prompt,
        system_prompt="你是strategy规划器,只输出合法 JSON.",
        fallback=fallback
    )
