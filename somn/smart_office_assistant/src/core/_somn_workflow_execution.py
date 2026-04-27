"""
__all__ = [
    'build_execution_report',
    'build_fallback_execution_tasks',
    'build_task_records',
    'evaluate_dependency_state',
    'execute_rollback',
    'execute_task',
    'extract_strategy_combo',
    'parse_execution_tasks',
    'resolve_reinforcement_action',
    'run_workflow_state_machine',
    'serialize_task_record',
    'transition_task_state',
]

SomnCore 工作流执行模块
任务解析、执行、依赖评估、回滚等逻辑。
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

def parse_execution_tasks(strategy_plan: Dict, tool_registry, llm_service,
                         call_llm_fn, build_fallback_fn) -> List[Dict[str, Any]]:
    """把strategy转为工具任务列表."""
    tools = tool_registry.describe_tools()
    fallback_tasks = build_fallback_fn(strategy_plan)

    prompt = f"""
你是 Somn 的任务规划器.请把strategy拆成工具调用任务,只输出 JSON 数组.
每个元素结构:
{{
  "task_name": "任务名",
  "tool": "工具ID",
  "parameters": {{"参数名": "参数值"}},
  "expected_output": "预期输出",
  "depends_on": ["前置任务名"],
  "max_retries": 0,
  "rollback_tasks": [
    {{"tool": "工具ID", "parameters": {{"参数名": "参数值"}}, "expected_output": "回滚结果"}}
  ]
}}

要求:
1. tool 只能从给定工具中选择.
2. parameters 必须是对象.
3. 如果没有数值数据,不要编造 data_stats 的输入.
4. 只有确有必要时才设置 depends_on / rollback_tasks / max_retries.
5. 优先产出真正能执行的任务.

工具清单:{json.dumps(tools, ensure_ascii=False)}
strategy:{json.dumps(strategy_plan.get('structured_strategy', {}), ensure_ascii=False)}
"""

    candidate = call_llm_fn(
        prompt=prompt,
        system_prompt="你是任务规划器,只输出合法 JSON 数组.",
        fallback=fallback_tasks
    )

    task_list = candidate if isinstance(candidate, list) else candidate.get("tasks", []) if isinstance(candidate, dict) else []
    validated_tasks: List[Dict[str, Any]] = []
    for task in task_list:
        if not isinstance(task, dict):
            continue
        tool_id = task.get("tool")
        if tool_id not in tool_registry.tools:
            continue
        parameters = task.get("parameters", {})
        if not isinstance(parameters, dict):
            parameters = {}
        if tool_id.startswith("llm_") and "model" not in parameters:
            parameters["model"] = llm_service.get_default_model()

        depends_on = task.get("depends_on", [])
        if isinstance(depends_on, str):
            depends_on = [depends_on]
        elif not isinstance(depends_on, list):
            depends_on = []

        rollback_tasks = task.get("rollback_tasks") or task.get("rollback") or []
        if isinstance(rollback_tasks, dict):
            rollback_tasks = [rollback_tasks]
        elif not isinstance(rollback_tasks, list):
            rollback_tasks = []
        normalized_rollbacks = []
        for rollback_task in rollback_tasks:
            if not isinstance(rollback_task, dict):
                continue
            rollback_tool = rollback_task.get("tool")
            if rollback_tool not in tool_registry.tools:
                continue
            rollback_parameters = rollback_task.get("parameters", {})
            if not isinstance(rollback_parameters, dict):
                rollback_parameters = {}
            if rollback_tool.startswith("llm_") and "model" not in rollback_parameters:
                rollback_parameters["model"] = llm_service.get_default_model()
            normalized_rollbacks.append({
                "tool": rollback_tool,
                "parameters": rollback_parameters,
                "expected_output": rollback_task.get("expected_output", "")
            })

        max_retries = task.get("max_retries", 0)
        try:
            max_retries = max(0, int(max_retries))
        except (TypeError, ValueError):
            max_retries = 0

        validated_tasks.append({
            "task_name": task.get("task_name", tool_id),
            "tool": tool_id,
            "parameters": parameters,
            "expected_output": task.get("expected_output", ""),
            "depends_on": [str(item) for item in depends_on if item],
            "max_retries": max_retries,
            "rollback_tasks": normalized_rollbacks
        })

    return validated_tasks or fallback_tasks

def build_fallback_execution_tasks(strategy_plan: Dict, llm_service) -> List[Dict[str, Any]]:
    """无法可靠解析时的兜底执行任务."""
    strategy_text = strategy_plan.get("strategy_overview", "")
    structured = strategy_plan.get("structured_strategy", {})
    return [
        {
            "task_name": "generate执行清单",
            "tool": "llm_chat",
            "parameters": {
                "prompt": (
                    "请把以下strategy整理成一份可执行清单,按优先级输出:\n\n"
                    f"概述:{strategy_text}\n\n结构化strategy:{json.dumps(structured, ensure_ascii=False)}"
                ),
                "model": llm_service.get_default_model(),
                "temperature": 0.2,
                "max_tokens": 2000,
                "system_prompt": "你是执行清单generate器,请输出分点可执行步骤."
            },
            "expected_output": "优先级执行清单",
            "depends_on": [],
            "max_retries": 0,
            "rollback_tasks": []
        }
    ]

def build_task_records(tasks: List[Dict[str, Any]], execution_config: Dict[str, Any]):
    """将计划任务转为可追踪的状态机记录."""
    from ._somn_types import WorkflowTaskRecord

    records = []
    default_retries = execution_config.get("task_max_retries", execution_config.get("max_retries", 0))
    try:
        default_retries = max(0, int(default_retries))
    except (TypeError, ValueError):
        default_retries = 0

    used_names = set()
    for index, task in enumerate(tasks, start=1):
        task_name = str(task.get("task_name") or f"task_{index}")
        if task_name in used_names:
            task_name = f"{task_name}_{index}"
        used_names.add(task_name)

        depends_on = task.get("depends_on", [])
        if isinstance(depends_on, str):
            depends_on = [depends_on]
        elif not isinstance(depends_on, list):
            depends_on = []

        max_retries = task.get("max_retries", default_retries)
        try:
            max_retries = max(0, int(max_retries))
        except (TypeError, ValueError):
            max_retries = default_retries

        rollback_tasks = task.get("rollback_tasks", [])
        if isinstance(rollback_tasks, dict):
            rollback_tasks = [rollback_tasks]
        elif not isinstance(rollback_tasks, list):
            rollback_tasks = []

        records.append(WorkflowTaskRecord(
            task_name=task_name,
            tool=str(task.get("tool", "")),
            parameters=task.get("parameters", {}) if isinstance(task.get("parameters", {}), dict) else {},
            expected_output=str(task.get("expected_output", "")),
            depends_on=[str(item) for item in depends_on if item],
            rollback_tasks=[item for item in rollback_tasks if isinstance(item, dict)],
            max_retries=max_retries
        ))
    return records

def evaluate_dependency_state(record, task_lookup) -> Dict[str, str]:
    """judge任务依赖是否满足."""
    if not record.depends_on:
        return {"status": "ready"}

    unresolved = []
    for dependency in record.depends_on:
        dependency_record = task_lookup.get(dependency)
        if dependency_record is None:
            return {"status": "blocked", "reason": f"前置任务不存在: {dependency}"}
        if dependency_record.status in {"failed", "blocked"}:
            return {"status": "blocked", "reason": f"前置任务未成功: {dependency} ({dependency_record.status})"}
        if dependency_record.status != "completed":
            unresolved.append(dependency)

    if unresolved:
        return {"status": "waiting", "reason": f"等待前置任务完成: {', '.join(unresolved)}"}
    return {"status": "ready"}

def transition_task_state(record, new_state: str,
                          state_history: List[Dict[str, Any]], note: str = "") -> None:
    """记录任务状态流转."""
    previous_state = record.status
    record.status = new_state
    state_history.append({
        "task_name": record.task_name,
        "from": previous_state,
        "to": new_state,
        "note": note,
        "timestamp": datetime.now().isoformat()
    })

def serialize_task_record(record) -> Dict[str, Any]:
    """输出可持久化的任务状态."""
    result = record.result or {}
    return {
        "task_name": record.task_name,
        "tool": record.tool,
        "parameters": record.parameters,
        "expected_output": record.expected_output,
        "depends_on": record.depends_on,
        "rollback_tasks": record.rollback_tasks,
        "max_retries": record.max_retries,
        "status": record.status,
        "attempts": record.attempts,
        "started_at": record.started_at,
        "completed_at": record.completed_at,
        "success": record.status == "completed",
        "last_error": record.last_error,
        "tool_attempts": result.get("tool_attempts"),
        "result": result.get("result") if result.get("success") else None,
        "error": result.get("error") if not result.get("success") else None,
        "timestamp": result.get("timestamp")
    }

def execute_task(task: Dict[str, Any], tool_registry, timeout: float = 300.0) -> Dict[str, Any]:
    """执行单个任务（修复版：添加超时保护）"""
    import sys
    from pathlib import Path
    
    # 确保 timeout_utils 在 sys.path 中
    src_root = Path(__file__).resolve().parent.parent
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))
    
    from timeout_utils import run_with_timeout, TimeoutException
    
    tool_id = task.get("tool")
    parameters = task.get("parameters", {})
    
    # 使用超时保护执行任务
    def _do_execute():
        return tool_registry.execute_tool(tool_id, parameters)
    
    try:
        result = run_with_timeout(_do_execute, timeout=timeout, description=f"任务执行({tool_id})")
    except TimeoutException as e:
        logger.error(f"任务 {task.get('task_name')} 执行超时（{timeout}s）: {e}")
        result = {
            "success": False,
            "error": f"任务执行超时（{timeout}秒）",
            "attempts": 1,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"任务 {task.get('task_name')} 执行失败: {e}")
        result = {
            "success": False,
            "error": str(e),
            "attempts": 1,
            "timestamp": datetime.now().isoformat()
        }
    
    return {
        "task_name": task.get("task_name"),
        "tool": tool_id,
        "parameters": parameters,
        "expected_output": task.get("expected_output", ""),
        "success": result.get("success", False),
        "result": result.get("result") if result.get("success") else None,
        "error": result.get("error") if not result.get("success") else None,
        "tool_attempts": result.get("attempts", 1),
        "timestamp": result.get("timestamp", datetime.now().isoformat())
    }

def execute_rollback(record, tool_registry, state_history: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """执行失败后的回滚任务."""
    if not record.rollback_tasks:
        return None

    rollback_entries = []
    for rollback_task in record.rollback_tasks:
        rollback_tool = rollback_task.get("tool")
        rollback_parameters = rollback_task.get("parameters", {})
        rollback_result = tool_registry.execute_tool(rollback_tool, rollback_parameters)
        rollback_entries.append({
            "tool": rollback_tool,
            "parameters": rollback_parameters,
            "expected_output": rollback_task.get("expected_output", ""),
            "success": rollback_result.get("success", False),
            "result": rollback_result.get("result") if rollback_result.get("success") else None,
            "error": rollback_result.get("error") if not rollback_result.get("success") else None,
            "timestamp": rollback_result.get("timestamp", datetime.now().isoformat())
        })

    rollback_success = all(entry.get("success") for entry in rollback_entries)
    state_history.append({
        "task_name": record.task_name,
        "from": record.status,
        "to": record.status,
        "note": f"触发回滚: {'成功' if rollback_success else '部分失败'}",
        "timestamp": datetime.now().isoformat()
    })

    return {
        "task_name": record.task_name,
        "rollback_success": rollback_success,
        "rollback_entries": rollback_entries
    }

def resolve_reinforcement_action(record) -> str:
    """把执行记录或任务结果mapping为可复用的强化学习动作标识."""
    if isinstance(record, dict):
        parameters = record.get("parameters", {}) if isinstance(record.get("parameters", {}), dict) else {}
        tool = record.get("tool")
        task_name = record.get("task_name", "unknown")
    else:
        parameters = record.parameters if isinstance(record.parameters, dict) else {}
        tool = getattr(record, "tool", "")
        task_name = getattr(record, "task_name", "unknown")

    for key in ("strategy", "strategy_name", "plan", "scenario", "workflow"):
        value = parameters.get(key)
        if value:
            return str(value)
    if tool:
        return f"tool::{tool}"
    return f"task::{task_name}"

def extract_strategy_combo(task_entries, resolve_fn) -> List[str]:
    """从任务记录中提取本次工作流实际使用的strategy组合."""
    combo = []
    seen = set()
    for entry in task_entries or []:
        action = resolve_fn(entry)
        if not action or action in seen:
            continue
        seen.add(action)
        combo.append(action)
    return combo

# ══════════════════════════════════════════════════════
# 工作流状态机执行
# ══════════════════════════════════════════════════════

def run_workflow_state_machine(
    task_records: List,
    execution_config: Dict[str, Any],
    tool_registry,
    task_id: str,
    eval_dep_fn,
    transition_fn,
    track_roi_start_fn,
    execute_task_fn,
    track_roi_completion_fn,
    execute_rollback_fn,
    intermediate_results_collector: Optional[callable] = None,
) -> tuple:
    """
    工作流状态机主循环：依赖感知调度 + 失败回滚。
    返回 (task_records, state_history, rollback_results, failed_count)。
    intermediate_results_collector: 可选回调函数，用于收集中间结果。
    """
    from datetime import datetime as dt

    task_lookup = {record.task_name: record for record in task_records}
    state_history: List[Dict[str, Any]] = []
    rollback_results: List[Dict[str, Any]] = []
    failed_count = 0

    # [v9.0] 防止无限循环：最大迭代次数上限
    _MAX_WORKFLOW_ITERATIONS = len(task_records) * 3 + 10  # 每个任务最多重试3次 + 缓冲
    _iteration = 0
    _workflow_start_time = time.monotonic() if hasattr(time, 'monotonic') else time.time()
    _WORKFLOW_TIMEOUT = 120.0  # 工作流绝对超时2分钟

    while True:
        _iteration += 1
        
        # [v9.0] 安全退出条件1：超过最大迭代次数
        if _iteration > _MAX_WORKFLOW_ITERATIONS:
            logger.warning(
                f"[工作流调度] 达到最大迭代次数({_MAX_WORKFLOW_ITERATIONS})，"
                f"强制退出。当前失败数={failed_count}, 总任务={len(task_records)}"
            )
            for record in task_records:
                if record.status not in ("completed", "failed", "blocked"):
                    transition_fn(record, "blocked", state_history,
                                  f"达到迭代上限({_MAX_WORKFLOW_ITERATIONS})")
            break
        
        # [v9.0] 安全退出条件2：总时间超时
        _elapsed = (time.monotonic() if hasattr(time, 'monotonic') else time.time()) - _workflow_start_time
        if _elapsed > _WORKFLOW_TIMEOUT:
            logger.warning(f"[工作流调度] 总耗时超时({_elapsed:.0f}s>{_WORKFLOW_TIMEOUT:.0f}s)，强制退出")
            for record in task_records:
                if record.status not in ("completed", "failed", "blocked"):
                    transition_fn(record, "blocked", state_history,
                                  f"工作流超时({_elapsed:.0f}s)")
            break

        runnable = []
        active_exists = False

        for record in task_records:
            if record.status in {"completed", "failed", "blocked"}:
                continue

            active_exists = True
            dependency_state = eval_dep_fn(record, task_lookup)
            if dependency_state["status"] == "blocked":
                transition_fn(record, "blocked", state_history, dependency_state.get("reason", "前置条件阻塞"))
                continue
            if dependency_state["status"] == "ready":
                runnable.append(record)

        if not active_exists:
            break

        if not runnable:
            for record in task_records:
                if record.status == "queued":
                    transition_fn(record, "blocked", state_history, "无可执行任务,可能存在循环依赖或前置结果未满足")
            break

        for record in runnable:
            record.attempts += 1
            record.started_at = record.started_at or dt.now().isoformat()
            transition_fn(record, "running", state_history, f"第 {record.attempts} 次执行")
            track_roi_start_fn(task_id, record, execution_config)

            result = execute_task_fn(record.to_dict(), tool_registry)
            record.result = result
            record.last_error = result.get("error")

            # 收集中间结果
            if intermediate_results_collector is not None:
                intermediate_results_collector(result)

            if result.get("success"):
                record.completed_at = dt.now().isoformat()
                transition_fn(record, "completed", state_history)
                track_roi_completion_fn(task_id, record)
                continue

            if record.attempts <= record.max_retries:
                transition_fn(record, "queued", state_history, f"执行失败,准备重试: {record.last_error}")
                continue

            record.completed_at = dt.now().isoformat()
            transition_fn(record, "failed", state_history, record.last_error or "执行失败")
            track_roi_completion_fn(task_id, record)
            failed_count += 1

            rollback_result = execute_rollback_fn(record, tool_registry, state_history)
            if rollback_result:
                rollback_results.append(rollback_result)

    return task_records, state_history, rollback_results, failed_count

# ══════════════════════════════════════════════════════
# 执行报告构建
# ══════════════════════════════════════════════════════

def build_execution_report(
    task_id: str,
    strategy_plan: Dict,
    tasks: List[Dict],
    task_records: List,
    state_history: List[Dict],
    rollback_results: List[Dict],
    execution_config: Dict,
    started_at: str,
    strategy_combo: List[str],
) -> Dict[str, Any]:
    """构建执行报告字典."""
    from datetime import datetime as dt

    task_results = [serialize_task_record(record) for record in task_records]
    completed_count = len([record for record in task_records if record.status == "completed"])
    blocked_count = len([record for record in task_records if record.status == "blocked"])

    return {
        "task_id": task_id,
        "based_on_strategy": strategy_plan.get("task_id"),
        "planned_tasks": tasks,
        "execution_summary": {
            "total_tasks": len(tasks),
            "completed": completed_count,
            "failed": len([record for record in task_records if record.status == "failed"]),
            "blocked": blocked_count,
            "success_ratio": round(completed_count / len(tasks), 4) if tasks else 0.0
        },
        "task_results": task_results,
        "strategy_combo": strategy_combo,
        "state_history": state_history,
        "rollback_results": rollback_results,
        "execution_config": execution_config,
        "started_at": started_at,
        "completed_at": dt.now().isoformat()
    }
