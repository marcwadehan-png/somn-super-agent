"""
自治学习 API 层 - SomnCore 自治学习闭环方法委托
封装目标管理、经验库、任务复盘等自治学习相关操作
"""

import re
import json
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# 自治存储读写
# ─────────────────────────────────────────────────────────────────────────────

def _module_read_json_store(somn_core, file_path: Path, default: Any) -> Any:
    """读取本地 JSON 存储,不存在时自动init."""
    if not file_path.exists():
        _module_write_json_store(somn_core, file_path, default)
        return default.copy() if isinstance(default, list) else dict(default) if isinstance(default, dict) else default
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logger.warning(f"读取自治存储失败 ({file_path.name}): {e}，使用默认值")
        return default.copy() if isinstance(default, list) else dict(default) if isinstance(default, dict) else default

def _module_write_json_store(somn_core, file_path: Path, data: Any):
    """写入本地 JSON 存储."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def _module_ensure_autonomy_stores(somn_core):
    """确保自治闭环所需的本地存储存在（带 double-check）"""
    if somn_core._autonomy_stores_ready:
        return
    try:
        _module_read_json_store(somn_core, somn_core.goal_store_path, [])
        _module_read_json_store(somn_core, somn_core.experience_store_path, [])
        _module_read_json_store(somn_core, somn_core.reflection_store_path, [])
        somn_core._autonomy_stores_ready = True
    except Exception as e:
        logger.error(f"自治存储初始化失败: {e}")
        somn_core._autonomy_stores_ready = True

# ─────────────────────────────────────────────────────────────────────────────
# 目标与经验管理
# ─────────────────────────────────────────────────────────────────────────────

def _module_extract_similarity_terms(somn_core, text: str) -> List[str]:
    """提取用于经验召回的关键词."""
    if not text:
        return []
    candidates = list(somn_core._extract_keywords(text))
    candidates.extend(re.findall(r"[A-Za-z0-9_\-]{2,}", text.lower()))
    seen = set()
    ordered = []
    for term in candidates:
        normalized = str(term).strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered

def _module_make_goal_id(somn_core, objective: str) -> str:
    """基于目标文本生成稳定 goal_id."""
    normalized = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "_", objective.strip().lower())
    normalized = normalized.strip("_") or datetime.now().strftime("goal_%Y%m%d_%H%M%S")
    return normalized[:48]

# ─────────────────────────────────────────────────────────────────────────────
# 任务记忆
# ─────────────────────────────────────────────────────────────────────────────

def _module_record_task_memory(
    somn_core,
    title: str,
    description: str,
    confidence_score: int,
    scenarios: List[str],
):
    """写回神经记忆系统."""
    try:
        somn_core._ensure_layers()
        somn_core.neural_system.record_research_finding({
            "title": title,
            "description": description,
            "source_type": "SomnCore",
            "source_detail": "统一智能体主链",
            "confidence_score": confidence_score,
            "scenarios": scenarios,
            "value_types": ["执行闭环"],
        })
    except Exception as exc:
        logger.warning(f"记忆写入失败: {str(exc)}")

# ─────────────────────────────────────────────────────────────────────────────
# 核心: 自主复盘与学习闭环
# ─────────────────────────────────────────────────────────────────────────────

def _module_generate_autonomy_reflection(
    somn_core,
    requirement: Dict[str, Any],
    execution: Dict[str, Any],
    evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    任务完成后自动形成自治复盘.
    生成可操作的改进建议，并更新经验库与目标体系。
    """
    execution_summary = execution.get("execution_summary", {}) if isinstance(execution, dict) else {}
    eval_summary = evaluation.get("evaluation_summary", {}) if isinstance(evaluation, dict) else {}

    overall = eval_summary.get("overall_score", 0.5)
    completed = int(execution_summary.get("completed", 0) or 0)
    failed = int(execution_summary.get("failed", 0) or 0)
    total = completed + failed
    success_ratio = completed / total if total > 0 else 0.0

    llm_judgment = {}
    try:
        prompt = (
            f"任务: {requirement.get('raw_description', '')}\n"
            f"完成情况: {completed}/{total} 任务成功\n"
            f"整体评分: {overall:.2f}\n"
            f"请分析: 1) 主要成功因素 2) 主要不足 3) 改进建议 4) 是否可复用的动作"
        )
        response = somn_core._call_llm_for_json(
            prompt=prompt,
            system_prompt=(
                "你是一个任务复盘专家。请分析任务执行情况，"
                "返回JSON格式的复盘报告，包含: success_factors, failure_reasons, "
                "improvement_suggestions, reusable_actions, suggested_next_task"
            ),
            fallback=None,
        )
        if response:
            llm_judgment = response
    except Exception as exc:
        logger.debug(f"自治复盘 LLM 调用失败: {exc}")

    reflection = {
        "task_id": requirement.get("task_id", ""),
        "overall_score": overall,
        "success_ratio": success_ratio,
        "completed": completed,
        "failed": failed,
        "execution_summary": execution_summary,
        "evaluation_summary": eval_summary,
        "llm_judgment": llm_judgment,
    }

    if llm_judgment:
        reflection.update({
            "success_factors": llm_judgment.get("success_factors", []),
            "failure_reasons": llm_judgment.get("failure_reasons", []),
            "improvement_suggestions": llm_judgment.get("improvement_suggestions", []),
            "reusable_actions": llm_judgment.get("reusable_actions", []),
            "suggested_next_task": llm_judgment.get("suggested_next_task", "继续下一轮执行"),
        })
    else:
        reflection.update({
            "success_factors": ["任务执行完成"] if overall >= 0.6 else [],
            "failure_reasons": ["执行效果未达预期"] if overall < 0.6 else [],
            "improvement_suggestions": ["优化执行策略"] if overall < 0.6 else ["保持当前策略"],
            "reusable_actions": [],
            "suggested_next_task": "继续下一轮执行",
        })

    return reflection

def _module_store_autonomy_learning(
    somn_core,
    requirement: Dict[str, Any],
    strategy: Dict[str, Any],
    execution: Dict[str, Any],
    evaluation: Dict[str, Any],
    reflection: Dict[str, Any],
    current_goal: Dict[str, Any],
) -> Dict[str, Any]:
    """
    写回长期目标、经验库和任务复盘到本地 JSON 存储.
    """
    # 类型保护：各参数可能是 str/dict/None
    if not isinstance(requirement, dict):
        requirement = {"raw_description": str(requirement) if requirement else "", "objective": str(requirement) if requirement else ""}
    if not isinstance(strategy, dict):
        strategy = {"strategy_overview": str(strategy) if strategy else ""}
    if not isinstance(execution, dict):
        execution = {"execution_summary": {"success_ratio": 0.0}}
    if not isinstance(evaluation, dict):
        evaluation = {"evaluation_summary": {"overall_score": 0.5}}
    if not isinstance(reflection, dict):
        reflection = {"reflection_text": str(reflection) if reflection else "", "reusable_actions": [], "lessons_learned": [], "suggested_next_task": "继续下一轮执行"}
    if not isinstance(current_goal, dict):
        current_goal = {"goal_id": "", "completed_tasks": [], "status": "active"}

    _module_ensure_autonomy_stores(somn_core)

    now = datetime.now().isoformat()

    # 1. 更新目标进度
    goals = _module_read_json_store(somn_core, somn_core.goal_store_path, [])
    updated_goal = dict(current_goal)

    goal_score = evaluation.get("evaluation_summary", {}).get("overall_score", 0.5)
    task_id = requirement.get("task_id", "")
    completed_tasks = updated_goal.get("completed_tasks", [])
    if task_id and task_id not in completed_tasks:
        completed_tasks.append(task_id)
    updated_goal.update({
        "completed_tasks": completed_tasks,
        "total_score": round(goal_score, 4),
        "last_task_time": now,
    })
    updated_goal["status"] = "active"

    goal_id = updated_goal.get("goal_id")
    if goal_id:
        goals = [g for g in goals if g.get("goal_id") != goal_id]
    goals.append(updated_goal)
    goals = goals[-30:]
    _module_write_json_store(somn_core, somn_core.goal_store_path, goals)

    # 2. 更新经验库
    experiences = _module_read_json_store(somn_core, somn_core.experience_store_path, [])
    execution_summary = execution.get("execution_summary", {}) if isinstance(execution, dict) else {}
    eval_summary = evaluation.get("evaluation_summary", {}) if isinstance(evaluation, dict) else {}
    score = eval_summary.get("overall_score", 0.5)
    success_ratio = float(execution_summary.get("success_ratio", 0.0) or 0.0)

    experience_entry = {
        "goal_id": updated_goal.get("goal_id"),
        "description": requirement.get("raw_description", ""),
        "objective": requirement.get("structured_requirement", {}).get("objective", ""),
        "industry": requirement.get("industry", "general"),
        "task_type": requirement.get("structured_requirement", {}).get("task_type", "general_analysis"),
        "keywords": _module_extract_similarity_terms(
            somn_core,
            " ".join([
                requirement.get("raw_description", ""),
                requirement.get("structured_requirement", {}).get("objective", "")
            ])
        ),
        "overall_score": round(score, 4),
        "success_ratio": round(success_ratio, 4),
        "reusable_actions": reflection.get("reusable_actions", []),
        "lessons_learned": reflection.get("lessons_learned", []),
        "next_focus": reflection.get("suggested_next_task", "继续下一轮执行"),
        "created_at": now,
    }
    experiences.append(experience_entry)
    experiences = experiences[-50:]
    _module_write_json_store(somn_core, somn_core.experience_store_path, experiences)

    # 3. 更新复盘记录
    reflections = _module_read_json_store(somn_core, somn_core.reflection_store_path, [])
    reflection_entry = dict(reflection)
    reflection_entry["strategy_overview"] = strategy.get("strategy_overview", "")
    reflection_entry["execution_summary"] = execution.get("execution_summary", {})
    reflection_entry["created_at"] = now
    reflections.append(reflection_entry)
    reflections = reflections[-50:]
    _module_write_json_store(somn_core, somn_core.reflection_store_path, reflections)

    # 4. 写回神经记忆系统
    _module_record_task_memory(
        somn_core,
        title=f"自主复盘 {requirement.get('task_id')}",
        description=json.dumps({
            "goal_id": updated_goal.get("goal_id"),
            "score": score,
            "next_actions": reflection.get("next_actions", [])[:3],
            "reusable_actions": reflection.get("reusable_actions", [])[:3],
        }, ensure_ascii=False),
        confidence_score=int(score * 100) if score > 0 else 60,
        scenarios=["自治复盘", updated_goal.get("task_type", "general_analysis")],
    )

    return updated_goal
