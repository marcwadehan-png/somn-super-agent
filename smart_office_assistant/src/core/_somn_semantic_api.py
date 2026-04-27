"""
语义记忆 API 层 - SomnCore 语义记忆方法委托
将语义记忆相关操作封装为独立的模块级函数
"""

import re
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# 核心语义分析
# ─────────────────────────────────────────────────────────────────────────────

def _module_run_semantic_analysis(
    somn_core,
    description: str,
    context: Dict = None,
) -> Dict[str, Any]:
    """
    运行语义分析 -- 理解用户输入的真实意图与关键词mapping(多用户版)

    多用户支持:
    - 从 context 中获取 user_id 进行用户隔离
    - 每个用户有独立的语义记忆空间
    - 支持千人千面的个性化理解
    """
    if not somn_core.semantic_memory:
        return {"enabled": False}

    try:
        # 1. 确定用户ID(多用户支持)
        user_id = None
        session_ctx = ""
        if context:
            user_id = context.get("user_id") or context.get("current_user")
            session_ctx = context.get("session_context", "") or ""

        # 2. 语义理解(传入用户ID)
        semantic_context = somn_core.semantic_memory.process_input(
            description,
            user_id=user_id,
            session_context=session_ctx,
        )

        # 3. 如需澄清,返回澄清信息(但不阻塞主链)
        clarification_needed = semantic_context.needs_clarification
        clarification_question = ""
        if clarification_needed and semantic_context.clarification_question:
            clarification_question = semantic_context.clarification_question

        # 4. 学习高频词mapping(多用户隔离)
        inferred = semantic_context.inferred_intent
        if inferred and inferred != "unknown":
            somn_core.semantic_memory.learn_from_input(
                description,
                inferred,
                user_id=user_id,
            )

        # 5. 构建结果(包含用户信息)
        result = {
            "enabled": True,
            "user_id": semantic_context.user_id,
            "raw_input": semantic_context.raw_input,
            "keywords": semantic_context.keywords_extracted or [],
            "inferred_intent": inferred or "unknown",
            "intent_confidence": semantic_context.intent_confidence or 0.0,
            "reasoning_chain": semantic_context.reasoning_chain or [],
            "clarification_needed": clarification_needed,
            "clarification_question": clarification_question,
            "matched_mappings": semantic_context.matched_mappings or [],
            "memory_summary": semantic_context.memory_summary or "",
        }
        return result

    except Exception as exc:
        logger.warning(f"语义分析异常: {exc}")
        return {"enabled": False, "error": str(exc)}

def _module_summarize_understanding(
    somn_core,
    description: str,
    context: Dict = None,
) -> str:
    """生成语义理解摘要"""
    semantic_result = _module_run_semantic_analysis(somn_core, description, context)
    if not semantic_result.get("enabled"):
        return f"理解输入: {description}"

    inferred = semantic_result.get("inferred_intent", "")
    keywords = semantic_result.get("keywords", [])
    confidence = semantic_result.get("intent_confidence", 0)

    parts = [f"意图: {inferred} (置信度 {confidence:.0%})"]
    if keywords:
        parts.append(f"关键词: {', '.join(keywords[:5])}")
    return " | ".join(parts)

# ─────────────────────────────────────────────────────────────────────────────
# 语义反馈
# ─────────────────────────────────────────────────────────────────────────────

def _module_record_semantic_feedback(
    somn_core,
    description: str,
    inferred_intent: str,
    user_rating: float,
    user_id: str = None,
) -> Dict[str, Any]:
    """
    记录语义理解反馈 -- 用于持续改进关键词-语义mapping(多用户版)

    Args:
        description: 原始描述
        inferred_intent: 推测意图
        user_rating: 用户评分 (1-5)
        user_id: 用户ID(可选)

    Returns:
        是否成功
    """
    if not somn_core.semantic_memory:
        return {"success": False, "reason": "semantic_memory_unavailable"}

    try:
        if user_rating >= 4.0:
            somn_core.semantic_memory.learn_from_input(
                description,
                inferred_intent,
                user_id=user_id,
            )
            logger.info(f"[语义反馈] 高质量映射已学习: '{description}' -> {inferred_intent}")
            return {"success": True, "learned": True}

        elif user_rating <= 2.0:
            somn_core.semantic_memory.forget_mapping(
                description,
                inferred_intent,
                user_id=user_id,
            )
            logger.info(f"[语义反馈] 错误映射已遗忘: '{description}' -/-> {inferred_intent}")
            return {"success": True, "forgotten": True}

        return {"success": True, "learned": False}

    except AttributeError:
        # semantic_memory 可能没有 forget_mapping 方法
        if user_rating >= 4.0:
            somn_core.semantic_memory.learn_from_input(
                description,
                inferred_intent,
                user_id=user_id,
            )
            return {"success": True, "learned": True}
        return {"success": True, "learned": False}
    except Exception as exc:
        logger.warning(f"语义反馈记录失败: {exc}")
        return {"success": False, "reason": str(exc)}

# ─────────────────────────────────────────────────────────────────────────────
# 语义统计与报告
# ─────────────────────────────────────────────────────────────────────────────

def _module_get_semantic_memory_stats(
    somn_core,
    user_id: str = None,
) -> Dict[str, Any]:
    """
    获取语义记忆统计(多用户版)

    Args:
        user_id: 用户ID(可选,不传则返回全局统计)
    """
    if not somn_core.semantic_memory:
        return {
            "enabled": False,
            "total_mappings": 0,
            "users": [],
        }

    try:
        if user_id:
            return {
                "enabled": True,
                "user_id": user_id,
                "total_mappings": getattr(somn_core.semantic_memory, "get_mapping_count", lambda uid=None: 0)(user_id),
            }
        else:
            # 全局统计
            mapping_count = getattr(somn_core.semantic_memory, "get_mapping_count", lambda uid=None: 0)(None)
            users = getattr(somn_core.semantic_memory, "list_users", lambda: [])()
            return {
                "enabled": True,
                "total_mappings": mapping_count,
                "users": users,
            }
    except Exception as exc:
        logger.warning(f"语义记忆统计获取失败: {exc}")
        return {"enabled": False, "error": str(exc)}

def _module_get_semantic_memory_report(
    somn_core,
    user_id: str = None,
) -> str:
    """获取语义记忆报告(多用户版)"""
    if not somn_core.semantic_memory:
        return "语义记忆引擎未启用"
    return somn_core.semantic_memory.generate_memory_report(user_id=user_id)

# ─────────────────────────────────────────────────────────────────────────────
# 多用户管理接口
# ─────────────────────────────────────────────────────────────────────────────

def _module_register_semantic_user(somn_core, user_id: str) -> bool:
    """注册新用户语义记忆空间"""
    if not somn_core.semantic_memory:
        return False
    return somn_core.semantic_memory.register_user(user_id)

def _module_switch_semantic_user(somn_core, user_id: str) -> bool:
    """切换当前语义记忆用户"""
    if not somn_core.semantic_memory:
        return False
    return somn_core.semantic_memory.switch_user(user_id)

def _module_list_semantic_users(somn_core) -> List[Dict[str, Any]]:
    """列出所有语义记忆用户"""
    if not somn_core.semantic_memory:
        return []
    return somn_core.semantic_memory.list_users()

def _module_export_user_semantic_data(
    somn_core,
    user_id: str,
) -> Optional[Dict[str, Any]]:
    """导出用户语义数据(GDPR合规)"""
    if not somn_core.semantic_memory:
        return None
    return somn_core.semantic_memory.export_user_data(user_id)

# ─────────────────────────────────────────────────────────────────────────────
# 缓存与相似度
# ─────────────────────────────────────────────────────────────────────────────

def _module_check_search_cache(
    somn_core,
    description: str,
) -> Optional[List[Dict[str, Any]]]:
    """
    查询搜索缓存：精确命中或语义相似命中.
    Returns:
        命中时返回缓存的搜索结果列表，否则返回 None.
    """
    import hashlib
    now = datetime.now()

    def _normalize_for_cache(text: str) -> str:
        t = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text.lower())
        return re.sub(r'\s+', ' ', t).strip()

    def _jaccard_similarity(set_a: set, set_b: set) -> float:
        if not set_a and not set_b:
            return 1.0
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    norm_desc = _normalize_for_cache(description)
    new_keywords = set(somn_core._extract_keywords(description))

    with somn_core._search_result_cache_lock:
        # 先尝试精确命中
        exact_key = hashlib.md5(norm_desc[:80].encode()).hexdigest()[:12]
        if exact_key in somn_core._search_result_cache:
            entry = somn_core._search_result_cache[exact_key]
            age = (now - entry["timestamp"]).total_seconds()
            if age < somn_core._SEARCH_CACHE_TTL:
                logger.info(f"搜索缓存精确命中 (age={age:.0f}s)")
                return entry["results"]
            else:
                del somn_core._search_result_cache[exact_key]

        # 再尝试语义相似命中
        for cached_key, entry in list(somn_core._search_result_cache.items()):
            age = (now - entry["timestamp"]).total_seconds()
            if age >= somn_core._SEARCH_CACHE_TTL:
                del somn_core._search_result_cache[cached_key]
                continue

            cached_keywords = entry.get("keywords", set())
            if new_keywords and cached_keywords:
                sim = _jaccard_similarity(new_keywords, cached_keywords)
                if sim >= somn_core._SEARCH_SIMILARITY_THRESHOLD:
                    logger.info(f"搜索缓存语义命中 (similarity={sim:.2f}, age={age:.0f}s)")
                    return entry["results"]

    return None

def _module_put_search_cache(
    somn_core,
    description: str,
    results: List[Dict[str, Any]],
) -> None:
    """写入搜索缓存."""
    import hashlib

    def _normalize_for_cache(text: str) -> str:
        t = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text.lower())
        return re.sub(r'\s+', ' ', t).strip()

    if not results:
        return
    norm_desc = _normalize_for_cache(description)
    key = hashlib.md5(norm_desc[:80].encode()).hexdigest()[:12]
    keywords = set(somn_core._extract_keywords(description))

    with somn_core._search_result_cache_lock:
        somn_core._search_result_cache[key] = {
            "results": results,
            "keywords": keywords,
            "timestamp": datetime.now(),
            "description_preview": description[:60],
        }
        # 防止缓存无限膨胀：保留最近 50 条
        if len(somn_core._search_result_cache) > 50:
            sorted_keys = sorted(
                somn_core._search_result_cache.keys(),
                key=lambda k: somn_core._search_result_cache[k]["timestamp"],
            )
            for old_key in sorted_keys[:10]:
                del somn_core._search_result_cache[old_key]

def _module_evict_stale_search_cache(somn_core) -> None:
    """清理过期缓存条目."""
    now = datetime.now()
    with somn_core._search_result_cache_lock:
        stale_keys = [
            k for k, v in somn_core._search_result_cache.items()
            if (now - v["timestamp"]).total_seconds() >= somn_core._SEARCH_CACHE_TTL
        ]
        for k in stale_keys:
            del somn_core._search_result_cache[k]
        if stale_keys:
            logger.debug(f"清理过期搜索缓存: {len(stale_keys)} 条")
