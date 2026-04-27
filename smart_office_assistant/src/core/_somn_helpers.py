"""
__all__ = [
    'clamp_unit_score',
    'extract_json_payload',
    'extract_keywords',
    'extract_strategy_combo',
    'resolve_reinforcement_action',
    'safe_industry_type',
]

SomnCore 工具方法 - 纯函数/简单方法委托
从 somn_core.py 拆分的工具方法集合
"""

import hashlib
import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

def extract_json_payload(text: str) -> Any:
    """从模型文本中提取 JSON."""
    if not text:
        return None

    candidates = []
    fenced_match = re.search(r"```json\s*(.*?)```", text, re.S | re.I)
    if fenced_match:
        candidates.append(fenced_match.group(1).strip())

    candidates.append(text.strip())

    object_match = re.search(r"(\{.*\})", text, re.S)
    if object_match:
        candidates.append(object_match.group(1).strip())

    array_match = re.search(r"(\[.*\])", text, re.S)
    if array_match:
        candidates.append(array_match.group(1).strip())

    for candidate in candidates:
        try:
            return json.loads(candidate)
        except Exception:
            continue
    return None

def safe_industry_type(industry: Optional[str]) -> Optional[Any]:
    """安全转换行业枚举."""
    if not industry or industry == "general":
        return None
    try:
        from src.industry_engine import IndustryType
        return IndustryType(industry)
    except Exception:
        return None

def extract_keywords(text: str) -> List[str]:
    """提取关键词"""
    growth_keywords = [
        "增长", "获客", "留存", "转化", "变现", "推荐",
        "用户", "流量", "渠道", "营销", "运营",
        "strategy", "方案", "优化", "提升", "降低",
        "DAU", "MAU", "GMV", "ROI", "LTV", "CAC",
        "电商", "SaaS", "内容", "社交", "金融", "智能体"
    ]
    return [kw for kw in growth_keywords if kw in text]

def clamp_unit_score(value: Any, default: float = 0.0) -> float:
    """把分值限制在 0~1,避免异常评估污染反馈."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = float(default)
    return round(max(0.0, min(1.0, score)), 4)

def resolve_reinforcement_action(record: Any) -> str:
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

def extract_strategy_combo(task_entries: List[Any]) -> List[str]:
    """从任务记录中提取本次工作流实际使用的strategy组合."""
    combo: List[str] = []
    seen = set()
    for entry in task_entries or []:
        action = resolve_reinforcement_action(entry)
        if not action or action in seen:
            continue
        seen.add(action)
        combo.append(action)
    return combo
