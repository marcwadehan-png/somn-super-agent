"""
__all__ = [
    'assess_task_routing',
    'check',
    'clamp_unit_score',
    'clear',
    'estimate_task_quality_score',
    'evict_stale',
    'extract_json_payload',
    'extract_keywords',
    'extract_similarity_terms',
    'extract_strategy_combo',
    'jaccard_similarity',
    'make_goal_id',
    'make_key',
    'normalize',
    'normalize_for_cache',
    'normalize_roi_ratio',
    'put',
    'read_json_store',
    'resolve_estimated_minutes',
    'resolve_reinforcement_action',
    'roi_trend_bias',
    'score_to_rating_value',
    'task_outcome_anchor',
]

SomnCore 工具函数模块
所有静态方法、纯函数、缓存逻辑集中管理。
"""

import re
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from ._somn_constants import (
    SEARCH_CACHE_TTL,
    LLM_CACHE_TTL,
    LLM_CACHE_MAX_ENTRIES,
    LLM_CACHE_PROMPT_PREFIX,
    SEARCH_SIMILARITY_THRESHOLD,
    TASK_STATUS_BASE_SCORE,
    ROI_DEFAULT_ESTIMATED_MINUTES,
    ROI_BASELINE,
    CHAIN_EVAL_WEIGHTS,
    ROUTING_MODE_MAP,
    ROUTING_COMPLEXITY_SIMPLE,
    ROUTING_COMPLEXITY_MEDIUM,
)

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════
# 文本处理工具
# ══════════════════════════════════════════════════════

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

def extract_similarity_terms(text: str, existing_keywords_fn=None) -> List[str]:
    """提取用于经验召回的关键词."""
    if not text:
        return []

    candidates = list(existing_keywords_fn(text) if existing_keywords_fn else extract_keywords(text))
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

def normalize_for_cache(text: str) -> str:
    """标准化文本用于缓存 key 生成：去标点、归一化空白、转小写."""
    t = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text.lower())
    return re.sub(r'\s+', ' ', t).strip()

def jaccard_similarity(set_a: set, set_b: set) -> float:
    """计算两个集合的 Jaccard 相似度."""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0

def make_goal_id(objective: str) -> str:
    """基于目标文本generate稳定 goal_id."""
    normalized = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "_", objective.strip().lower())
    normalized = normalized.strip("_") or datetime.now().strftime("goal_%Y%m%d_%H%M%S")
    return normalized[:48]

# ══════════════════════════════════════════════════════
# 搜索缓存管理
# ══════════════════════════════════════════════════════

class SearchCacheManager:
    """同会话搜索结果缓存管理器."""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = None  # 由外部 SomnCore 实例传入

    def normalize(self, text: str) -> str:
        return normalize_for_cache(text)

    def check(self, description: str, now: datetime,
              extract_fn, lock) -> Optional[List[Dict[str, Any]]]:
        """查询搜索缓存：精确命中或语义相似命中."""
        norm_desc = normalize_for_cache(description)
        new_keywords = set(extract_fn(description))

        with lock:
            # 先尝试精确命中
            exact_key = hashlib.md5(norm_desc[:80].encode()).hexdigest()[:12]
            if exact_key in self._cache:
                entry = self._cache[exact_key]
                age = (now - entry["timestamp"]).total_seconds()
                if age < SEARCH_CACHE_TTL:
                    logger.info(f"搜索缓存精确命中 (age={age:.0f}s)")
                    return entry["results"]
                else:
                    del self._cache[exact_key]

            # 再尝试语义相似命中
            for cached_key, entry in list(self._cache.items()):
                age = (now - entry["timestamp"]).total_seconds()
                if age >= SEARCH_CACHE_TTL:
                    del self._cache[cached_key]
                    continue
                cached_keywords = entry.get("keywords", set())
                if new_keywords and cached_keywords:
                    sim = jaccard_similarity(new_keywords, cached_keywords)
                    if sim >= SEARCH_SIMILARITY_THRESHOLD:
                        logger.info(f"搜索缓存语义命中 (similarity={sim:.2f}, age={age:.0f}s)")
                        return entry["results"]

        return None

    def put(self, description: str, results: List[Dict[str, Any]],
            extract_fn, now: datetime, lock) -> None:
        """写入搜索缓存."""
        if not results:
            return
        norm_desc = normalize_for_cache(description)
        key = hashlib.md5(norm_desc[:80].encode()).hexdigest()[:12]
        keywords = set(extract_fn(description))

        with lock:
            self._cache[key] = {
                "results": results,
                "keywords": keywords,
                "timestamp": now,
                "description_preview": description[:60],
            }
            # 防止缓存无限膨胀
            if len(self._cache) > 50:
                sorted_keys = sorted(
                    self._cache.keys(),
                    key=lambda k: self._cache[k]["timestamp"]
                )
                for old_key in sorted_keys[:10]:
                    del self._cache[old_key]

    def evict_stale(self, now: datetime, lock) -> None:
        """清理过期缓存条目."""
        with lock:
            stale_keys = [
                k for k, v in self._cache.items()
                if (now - v["timestamp"]).total_seconds() >= SEARCH_CACHE_TTL
            ]
            for k in stale_keys:
                del self._cache[k]

# ══════════════════════════════════════════════════════
# LLM 缓存管理
# ══════════════════════════════════════════════════════

class LLMCacheManager:
    """同会话 LLM 结果缓存管理器."""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def make_key(self, prompt: str, system_prompt: str) -> str:
        return hashlib.sha256(
            (prompt[:LLM_CACHE_PROMPT_PREFIX] + "|||" + (system_prompt or "")).encode("utf-8")
        ).hexdigest()

    def check(self, cache_key: str, now: datetime) -> Optional[Any]:
        """查询缓存命中."""
        entry = self._cache.get(cache_key)
        if entry is not None:
            age = (now - entry["ts"]).total_seconds()
            if age < LLM_CACHE_TTL:
                logger.debug(f"[LLM缓存] 命中 (age={age:.0f}s)")
                return entry["result"]
            else:
                del self._cache[cache_key]
        return None

    def put(self, cache_key: str, result: Any, now: datetime) -> None:
        """写入 LLM 缓存."""
        self._cache[cache_key] = {
            "result": result,
            "ts": now,
        }
        # 超出容量时驱逐最旧条目
        if len(self._cache) > LLM_CACHE_MAX_ENTRIES:
            oldest_key = min(self._cache, key=lambda k: self._cache[k]["ts"])
            del self._cache[oldest_key]

    def clear(self) -> None:
        """清空缓存."""
        self._cache.clear()

# ══════════════════════════════════════════════════════
# JSON 存储工具
# ══════════════════════════════════════════════════════

def read_json_store(file_path: Path, default: Any) -> Any:
    """读取本地 JSON 存储,不存在时自动初始化."""
    if not file_path.exists():
        _write_json_store_impl(file_path, default)
        return default.copy() if isinstance(default, list) else dict(default) if isinstance(default, dict) else default
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        _write_json_store_impl(file_path, default)
        return default.copy() if isinstance(default, list) else dict(default) if isinstance(default, dict) else default

def _write_json_store_impl(file_path: Path, data: Any) -> None:
    """写入本地 JSON 存储."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# ══════════════════════════════════════════════════════
# JSON 解析工具
# ══════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════
# 评分与归一化工具
# ══════════════════════════════════════════════════════

def clamp_unit_score(value: Any, default: float = 0.0) -> float:
    """把分值限制在 0~1,避免异常评估污染反馈."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = float(default)
    return round(max(0.0, min(1.0, score)), 4)

def score_to_rating_value(score: float) -> float:
    """把 0~1 分数折算为 feedback_pipeline 可消费的 1~5 评分."""
    return round(1.0 + clamp_unit_score(score, 0.5) * 4.0, 2)

def task_outcome_anchor(task_status: str) -> float:
    """把任务状态mapping为评估反馈的基准锚点."""
    return TASK_STATUS_BASE_SCORE.get(str(task_status or "").lower(), 0.5)

def estimate_task_quality_score(record, clamp_fn) -> float:
    """把执行记录粗折算为 ROI 可消费的质量分."""
    status = str(record.status or "").lower()
    base_score = TASK_STATUS_BASE_SCORE.get(status, 0.5)
    retry_penalty = min(0.24, max(0, int(record.attempts or 0) - 1) * 0.08)
    tool_attempts = 1
    if isinstance(record.result, dict):
        try:
            tool_attempts = int(record.result.get("tool_attempts") or 1)
        except (TypeError, ValueError):
            tool_attempts = 1
    tool_penalty = min(0.1, max(0, tool_attempts - 1) * 0.05)
    error_penalty = 0.08 if record.last_error and status != "completed" else 0.0
    return clamp_fn(base_score - retry_penalty - tool_penalty - error_penalty, 0.5)

def resolve_estimated_minutes(record, execution_config: Dict[str, Any]) -> float:
    """尽量从任务参数或执行配置中推断 ROI 所需的预估耗时."""
    if isinstance(record, dict):
        parameters = record.get("parameters", {}) if isinstance(record.get("parameters", {}), dict) else {}
    else:
        parameters = record.parameters if isinstance(record.parameters, dict) else {}

    config = execution_config if isinstance(execution_config, dict) else {}
    candidates = [
        parameters.get("estimated_minutes"),
        parameters.get("estimated_duration_minutes"),
        parameters.get("time_budget_minutes"),
        config.get("estimated_minutes"),
        config.get("default_estimated_minutes"),
        config.get("time_budget_minutes"),
    ]
    for value in candidates:
        try:
            minutes = float(value)
        except (TypeError, ValueError):
            continue
        if minutes > 0:
            return round(minutes, 2)
    return ROI_DEFAULT_ESTIMATED_MINUTES

# ══════════════════════════════════════════════════════
# ROI 工具
# ══════════════════════════════════════════════════════

def normalize_roi_ratio(value: Any, default: float = 0.5) -> float:
    """把 ROI ratio 平滑压到 0~1."""
    try:
        ratio = float(value)
    except (TypeError, ValueError):
        return clamp_unit_score(default, 0.5)
    clipped = max(-1.0, min(1.0, ratio))
    normalized = 0.5 + clipped * 0.25
    if ratio > 1.0:
        normalized += min(0.25, (ratio - 1.0) * 0.05)
    return clamp_unit_score(normalized, default)

def roi_trend_bias(trend: Any) -> float:
    """给 ROI 趋势一个小幅偏置."""
    trend_key = str(trend or "").lower()
    return {"improving": 0.05, "declining": -0.05}.get(trend_key, 0.0)

# ══════════════════════════════════════════════════════
# 路由分析工具
# ══════════════════════════════════════════════════════

def assess_task_routing(description: str, structured_req: Dict, context: Dict,
                        extract_kw_fn=None) -> Dict[str, Any]:
    """
    评估任务复杂度,决定路由路径.
    见 somn_core.py 完整注释。
    """
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

    deep_keywords = ["研究", "深度", "论证", "报告", "analysis", "strategy", "方案", "全面"]
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

    if complexity < ROUTING_COMPLEXITY_SIMPLE:
        route = "orchestrator"
        cuisine_mode = "fast"
        cuisine_level = "simple"
        reasoning = "简单任务,本地模型快速响应(FAST模式)"
    elif complexity < ROUTING_COMPLEXITY_MEDIUM:
        route = "orchestrator"
        cuisine_mode = "home"
        cuisine_level = "medium"
        reasoning = "中等任务,本地+云端协同(HOME模式)"
    else:
        route = "full_workflow"
        cuisine_mode = "feast"
        cuisine_level = "complex"
        reasoning = "复杂任务,完整工作流执行(FEAST模式)"

    user_mode_override = context.get("dining_mode") or context.get("cuisine_mode") or context.get("learning_mode")
    if user_mode_override and user_mode_override in ROUTING_MODE_MAP:
        route, cuisine_mode, cuisine_level, reasoning = ROUTING_MODE_MAP[user_mode_override]

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
    }
    return result

# ══════════════════════════════════════════════════════
# 强化学习动作解析
# ══════════════════════════════════════════════════════

def resolve_reinforcement_action(record) -> str:
    """
    把执行记录或任务结果mapping为可复用的强化学习动作标识.
    纯函数版本，接受 record 参数而非 self。
    """

    if isinstance(record, dict):
        parameters = record.get("parameters", {}) if isinstance(record.get("parameters", {}), dict) else {}
        tool = record.get("tool")
        task_name = record.get("task_name", "unknown")
    else:
        parameters = getattr(record, "parameters", {}) or {}
        if not isinstance(parameters, dict):
            parameters = {}
        tool = getattr(record, "tool", "")
        task_name = getattr(record, "task_name", "unknown")

    for key in ("strategy", "strategy_name", "plan", "scenario", "workflow"):
        value = parameters.get(key)
        if value:
            return str(value)
    if tool:
        return f"tool::{tool}"
    return f"task::{task_name}"

def extract_strategy_combo(task_entries, resolve_fn=None) -> List[str]:
    """从任务记录中提取本次工作流实际使用的strategy组合."""
    if resolve_fn is None:
        resolve_fn = resolve_reinforcement_action

    combo: List[str] = []
    seen = set()
    for entry in task_entries or []:
        action = resolve_fn(entry)
        if not action or action in seen:
            continue
        seen.add(action)
        combo.append(action)
    return combo
