"""
__all__ = [
    'module_extract_keywords',
    'module_jaccard_similarity',
    'module_normalize_for_cache',
    'module_safe_future_result',
    'module_safe_industry_type',
]

执行与任务 API 层 - SomnCore 任务执行与结果处理方法委托
封装任务执行、回滚、序列化等操作
"""

import logging
import re
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .somn_core import SomnCore, WorkflowTaskRecord

logger = logging.getLogger(__name__)

# ── 静态方法（不需要 somn_core）─────────────────────────────

def module_normalize_for_cache(text: str) -> str:
    """标准化文本用于缓存 key 生成."""
    t = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text.lower())
    return re.sub(r'\s+', ' ', t).strip()

def module_jaccard_similarity(set_a: set, set_b: set) -> float:
    """计算两个集合的 Jaccard 相似度."""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0

def module_safe_future_result(future, timeout: float, fallback: Any, label: str = "") -> Any:
    """安全地从 Future 取结果，超时/异常时返回 fallback."""
    from concurrent.futures import TimeoutError as FuturesTimeoutError
    try:
        return future.result(timeout=timeout)
    except FuturesTimeoutError:
        logger.warning(f"[{label}] 超时 ({timeout}s)，使用 fallback")
        return fallback
    except Exception as exc:
        logger.warning(f"[{label}] 异常: {exc}，使用 fallback")
        return fallback

def module_safe_industry_type(value: Any) -> Optional[str]:
    """把任意值安全转换为 IndustryType."""
    if value is None:
        return None
    try:
        from src.industry_engine import IndustryType
        if isinstance(value, IndustryType):
            return value
        if isinstance(value, str):
            upper = value.strip().upper()
            for it in IndustryType:
                if it.name == upper or it.value == upper:
                    return it
            return IndustryType.SAAS_B2B  # 默认值改为有效值
        return IndustryType.SAAS_B2B
    except Exception:
        return None

def module_extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """从文本中提取关键词."""
    if not text:
        return []
    try:
        words = re.findall(r'[\w\u4e00-\u9fff]{2,}', text.lower())
        stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', 'that', 'the', 'is', 'in', 'it', 'to', 'and', 'of', 'a', 'for', 'on', 'with', 'as', 'by', 'at', 'from'}
        filtered = [w for w in words if w not in stopwords and len(w) > 1]
        from collections import Counter
        counter = Counter(filtered)
        return [w for w, _ in counter.most_common(max_keywords)]
    except Exception:
        return []

# ── 实例方法（需要 somn_core）───────────────────────────────

def _module_serialize_task_record(somn_core, record: Any) -> Dict[str, Any]:
    """输出可持久化的任务状态."""
    if record is None:
        return {}
    if isinstance(record, dict):
        return record
    result_data = getattr(record, "result", None) or {}
    return {
        "task_name": getattr(record, "task_name", ""),
        "tool": getattr(record, "tool", ""),
        "parameters": getattr(record, "parameters", {}),
        "expected_output": getattr(record, "expected_output", ""),
        "depends_on": getattr(record, "depends_on", []),
        "rollback_tasks": getattr(record, "rollback_tasks", []),
        "max_retries": getattr(record, "max_retries", 3),
        "status": getattr(record, "status", ""),
        "attempts": getattr(record, "attempts", 0),
        "started_at": getattr(record, "started_at", ""),
        "completed_at": getattr(record, "completed_at", ""),
        "success": getattr(record, "status", "") == "completed",
        "last_error": getattr(record, "last_error", ""),
        "tool_attempts": result_data.get("tool_attempts") if isinstance(result_data, dict) else None,
        "result": result_data.get("result") if isinstance(result_data, dict) and result_data.get("success") else None,
        "error": result_data.get("error") if isinstance(result_data, dict) and not result_data.get("success") else None,
        "timestamp": result_data.get("timestamp") if isinstance(result_data, dict) else None,
    }

def _module_execute_rollback(somn_core, record: Any, state_history: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """执行失败后的回滚任务."""
    rollback_tasks = getattr(record, "rollback_tasks", []) or []
    if not rollback_tasks:
        return None

    rollback_entries = []
    for rollback_task in rollback_tasks:
        rollback_tool = rollback_task.get("tool")
        rollback_params = rollback_task.get("parameters", {})
        rollback_result = somn_core.tool_registry.execute_tool(rollback_tool, rollback_params)
        rollback_entries.append({
            "tool": rollback_tool,
            "parameters": rollback_params,
            "expected_output": rollback_task.get("expected_output", ""),
            "success": rollback_result.get("success", False),
            "result": rollback_result.get("result") if rollback_result.get("success") else None,
            "error": rollback_result.get("error") if not rollback_result.get("success") else None,
            "timestamp": rollback_result.get("timestamp", datetime.now().isoformat())
        })

    rollback_success = all(entry.get("success") for entry in rollback_entries)
    state_history.append({
        "task_name": getattr(record, "task_name", ""),
        "from": getattr(record, "status", ""),
        "to": getattr(record, "status", ""),
        "note": f"触发回滚: {'成功' if rollback_success else '部分失败'}",
        "timestamp": datetime.now().isoformat()
    })
    return {
        "task_name": getattr(record, "task_name", ""),
        "rollback_success": rollback_success,
        "rollback_entries": rollback_entries
    }

def _module_execute_task(somn_core, task: Dict[str, Any]) -> Dict[str, Any]:
    """执行单个任务."""
    tool_id = task.get("tool")
    parameters = task.get("parameters", {})
    result = somn_core.tool_registry.execute_tool(tool_id, parameters)
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
