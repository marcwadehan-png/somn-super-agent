"""
上下文与记忆 API 层 - SomnCore 上下文查询与记忆方法委托
封装上下文查询、记忆记录等操作
"""

import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime
import json
import re

if TYPE_CHECKING:
    from .somn_core import SomnCore

logger = logging.getLogger(__name__)

def _module_query_memory_context(somn_core, requirement: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """从记忆系统查询相关上下文."""
    memory_type = context.get("memory_type", "all")
    max_results = context.get("max_results", 5)
    user_id = context.get("user_id", "default")

    results: Dict[str, List[Dict[str, Any]]] = {}
    session_id = getattr(somn_core, "_session_id", "default")

    # 查询神经记忆
    if memory_type in ("all", "neural"):
        try:
            neural = somn_core.neural_memory
            if neural is not None:
                neural_results = neural.search_memories(requirement, user_id=user_id, limit=max_results)
                if neural_results:
                    results["neural"] = neural_results[:max_results]
        except Exception as exc:
            logger.debug(f"神经记忆查询跳过: {exc}")

    # 查询语义记忆
    if memory_type in ("all", "semantic") and somn_core.semantic_memory:
        try:
            semantic_results = somn_core.semantic_memory.search(
                requirement,
                user_id=user_id,
                limit=max_results,
            )
            if semantic_results:
                results["semantic"] = semantic_results[:max_results]
        except Exception as exc:
            logger.debug(f"语义记忆查询跳过: {exc}")

    # 查询知识图谱
    if memory_type in ("all", "knowledge"):
        try:
            kg = somn_core.knowledge_graph
            if kg is not None:
                kg_results = kg.query(requirement, max_results=max_results)
                if kg_results:
                    results["knowledge"] = kg_results[:max_results]
        except Exception as exc:
            logger.debug(f"知识图谱查询跳过: {exc}")

    return {
        "requirement": requirement,
        "memory_type": memory_type,
        "session_id": session_id,
        "user_id": user_id,
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }

def _module_build_local_fallback_context(somn_core, context: Dict[str, Any]) -> Dict[str, Any]:
    """当外部记忆系统不可用时,构建本地回退上下文."""
    context_type = context.get("type", "general")
    fallback: Dict[str, Any] = {
        "type": context_type,
        "mode": "local_fallback",
        "timestamp": datetime.now().isoformat(),
    }
    if hasattr(somn_core, "current_industry") and somn_core.current_industry:
        ind = somn_core.current_industry
        fallback["industry"] = ind.value if hasattr(ind, "value") else str(ind)
    if hasattr(somn_core, "_session_id") and somn_core._session_id:
        fallback["session_id"] = somn_core._session_id
    return fallback

def _module_record_task_memory(somn_core, requirement: str, strategy: Any, execution: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
    """把一次任务执行的关键信息写入记忆."""
    memory_result: Dict[str, Any] = {"recorded": False, "memory_type": []}

    # 写入神经记忆
    try:
        neural = somn_core.neural_memory
        if neural is not None:
            memory_data = {
                "requirement": requirement,
                "strategy": strategy if isinstance(strategy, str) else str(strategy),
                "execution": execution,
                "evaluation": evaluation,
                "timestamp": datetime.now().isoformat(),
            }
            neural_id = neural.add_experience(
                requirement=requirement,
                memory_type="task_execution",
                content=memory_data,
                tags=["task", "execution"],
            )
            if neural_id:
                memory_result["recorded"] = True
                memory_result["memory_type"].append("neural")
                memory_result["neural_id"] = neural_id
    except Exception as exc:
        logger.debug(f"神经记忆写入跳过: {exc}")

    # 写入语义记忆
    if somn_core.semantic_memory:
        try:
            semantic_id = somn_core.semantic_memory.add(
                text=f"{requirement} | {strategy}",
                memory_type="task_execution",
                user_id="default",
                metadata={
                    "execution_summary": str(execution.get("execution_summary", {}))[:200],
                    "evaluation_score": str(evaluation.get("overall_score", "N/A")),
                },
            )
            if semantic_id:
                memory_result["recorded"] = True
                memory_result["memory_type"].append("semantic")
                memory_result["semantic_id"] = semantic_id
        except Exception as exc:
            logger.debug(f"语义记忆写入跳过: {exc}")

    return memory_result

def _module_persist_agent_run(somn_core, task_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """持久化 agent 运行记录."""
    result = {"success": False, "path": ""}
    try:
        run_dir = somn_core.base_path / "data" / "learning" / "agent_runs"
        run_dir.mkdir(parents=True, exist_ok=True)
        run_file = run_dir / f"{task_id}.json"
        with open(run_file, "w", encoding="utf-8") as f:
            json.dump(context, f, ensure_ascii=False, indent=2)
        result = {"success": True, "path": str(run_file)}
    except Exception as exc:
        logger.warning(f"Agent 运行持久化失败: {exc}")
        result["error"] = str(exc)
    return result

def _module_call_llm_for_json(somn_core, prompt: str, system_hint: str = "", retry: int = 3) -> Dict[str, Any]:
    """调用 LLM 获取结构化 JSON 响应（v17.0 LLM缓存层激活）。
    
    同会话内，相同 prompt + system_hint 的 LLM 调用直接复用结果，
    避免重复请求。以 prompt 前256字符的 SHA256 作为缓存键。
    """
    import hashlib
    import time as _time
    
    # ━━ LLM 缓存层：检查是否已有缓存命中 ━━
    cache = getattr(somn_core, "_llm_result_cache", {})
    cache_lock = getattr(somn_core, "_llm_result_cache_lock", None)
    cache_ttl = getattr(somn_core, "_LLM_CACHE_TTL", 600.0)
    cache_max = getattr(somn_core, "_LLM_CACHE_MAX_ENTRIES", 200)
    prefix_len = getattr(somn_core, "_LLM_CACHE_PROMPT_PREFIX", 256)
    
    if cache and cache_lock is not None:
        prompt_prefix = prompt[:prefix_len] if prompt else ""
        cache_key = hashlib.sha256(
            (prompt_prefix + "|||" + (system_hint or "")).encode()
        ).hexdigest()[:32]
        
        with cache_lock:
            if cache_key in cache:
                entry = cache[cache_key]
                age = _time.time() - entry.get("_cached_at", 0)
                if age < cache_ttl:
                    logger.info(f"[LLM缓存命中] {cache_key[:8]}... TTL剩余{age:.0f}s")
                    return entry.get("result", {})
                else:
                    del cache[cache_key]
    
    # ━━ 缓存未命中，执行实际 LLM 调用 ━━
    for attempt in range(retry):
        try:
            # [v1.0.0] 优先使用A/B双模型左右大脑调度
            dual_service = getattr(somn_core, 'dual_model_service', None)
            llm_to_use = dual_service or somn_core.llm_service
            if llm_to_use is None:
                break
            # 构建对话消息
            system_msg = system_hint or ""
            user_msg = prompt
            model_param = None if dual_service else "local-default"
            response = llm_to_use.chat(
                user_msg,
                model=model_param,
                system_prompt=system_msg if system_msg else None,
                temperature=0.3,
                max_tokens=2000,
            )
            response_text = response.content if response else None
            if response_text:
                parsed = _module_extract_json_payload(somn_core, response_text)
                if parsed:
                    # ━━ 写入缓存 ━━
                    if cache and cache_lock is not None:
                        with cache_lock:
                            if len(cache) >= cache_max:
                                oldest_keys = sorted(
                                    cache.keys(),
                                    key=lambda k: cache[k].get("_cached_at", 0)
                                )[:cache_max // 4]
                                for k in oldest_keys:
                                    del cache[k]
                            cache[cache_key] = {
                                "result": parsed,
                                "_cached_at": _time.time(),
                                "_prompt_prefix": prompt[:64],
                            }
                    return parsed
        except Exception as exc:
            logger.debug(f"LLM JSON 调用尝试 {attempt+1} 失败: {exc}")
    return {}

def _module_extract_json_payload(somn_core, text: str) -> Optional[Dict[str, Any]]:
    """从文本中提取 JSON 对象."""
    if not text:
        return None
    # 尝试直接解析
    try:
        return json.loads(text)
    except Exception as e:
        logger.debug(f"JSON解析失败: {e}")
    # 尝试提取 ```json ... ``` 块
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception as e:
            logger.debug(f"JSON块解析失败: {e}")
    # 尝试提取第一个 { ... }
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception as e:
            logger.debug(f"JSON提取失败: {e}")
    return None
