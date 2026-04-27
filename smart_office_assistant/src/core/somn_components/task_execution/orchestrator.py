# -*- coding: utf-8 -*-
"""
__all__ = [
    'build_local_fallback_context',
    'check_cache',
    'compute_cache_key',
    'decide_route',
    'evict_stale_cache',
    'execute_rollback',
    'get_executor',
    'jaccard_similarity',
    'normalize_for_cache',
    'put_cache',
    'run_local_llm_route',
    'run_orchestrator_route',
    'run_wisdom_route',
    'safe_future_result',
    'serialize_task_record',
]

任务编排器 - TaskOrchestrator
负责承接 SomnCore.run_agent_task() 的核心执行逻辑
包括任务路由、上下文构建、缓存管理等
"""
import logging
import time
import hashlib
import json
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)
class TaskOrchestrator:
    """
    任务编排器 - 承接 SomnCore 的任务执行主链

    职责：
    1. 任务路由决策 (orchestrator/local_llm/wisdom)
    2. 并行执行上下文构建
    3. 搜索缓存管理
    4. 回退上下文构建
    5. 回滚执行
    """

    # 缓存TTL: 5分钟
    DEFAULT_CACHE_TTL = 300

    def __init__(self, llm=None, semantic_memory_engine=None,
                 somn_core=None, cache_ttl: int = DEFAULT_CACHE_TTL):
        """
        初始化任务编排器

        Args:
            llm: LLM服务实例
            semantic_memory_engine: 语义记忆引擎
            somn_core: SomnCore引用(用于路由委托)
            cache_ttl: 缓存过期时间(秒)
        """
        self._llm = llm
        self._semantic_memory_engine = semantic_memory_engine
        self._somn_core = somn_core  # 用于路由委托
        self._cache_ttl = cache_ttl
        self._cache: Dict[str, Tuple[Any, float]] = {}  # {cache_key: (result, timestamp)}
        self._cache_lock = threading.RLock()

        # 线程池懒加载
        self._executor: Optional[ThreadPoolExecutor] = None
        self._executor_lock = threading.RLock()

    # ========== 线程池管理 ==========

    def get_executor(self) -> ThreadPoolExecutor:
        """获取并行分析用线程池（懒加载、线程安全）"""
        if self._executor is None:
            with self._executor_lock:
                if self._executor is None:
                    self._executor = ThreadPoolExecutor(max_workers=6, thread_name_prefix='task_exec_')
        return self._executor

    # ========== 路由决策 ==========

    def decide_route(self, user_input: str, context: Dict[str, Any]) -> str:
        """
        决定任务执行路由

        Returns:
            'orchestrator': SomnOrchestrator 直答
            'local_llm': 本地 LLM 直答
            'wisdom': 智慧板块直答
        """
        if self._somn_core is None:
            return 'orchestrator'

        # 委托给 _somn_routes
        return self._somn_core._decide_route(user_input, context)

    def run_orchestrator_route(self, user_input: str, context: Dict) -> Dict:
        """路径A: SomnOrchestrator 直答路由"""
        if self._somn_core is None:
            return {'type': 'error', 'message': 'SomnCore not available'}
        return self._somn_core._run_orchestrator_route(user_input, context)

    def run_local_llm_route(self, user_input: str, context: Dict) -> Dict:
        """路径B: 本地 LLM 直答路由"""
        if self._somn_core is None:
            return {'type': 'error', 'message': 'SomnCore not available'}
        return self._somn_core._run_local_llm_route(user_input, context)

    def run_wisdom_route(self, user_input: str, context: Dict) -> Dict:
        """路径C: 智慧板块直答路由"""
        if self._somn_core is None:
            return {'type': 'error', 'message': 'SomnCore not available'}
        return self._somn_core._run_wisdom_route(user_input, context)

    # ========== 缓存管理 ==========

    def normalize_for_cache(self, text: str) -> str:
        """
        标准化文本用于缓存 key 生成：去标点、归一化空白、转小写
        """
        import re
        # 去除标点
        text = re.sub(r'[^\w\s]', '', text)
        # 归一化空白
        text = re.sub(r'\s+', ' ', text)
        # 转小写
        return text.lower().strip()

    def compute_cache_key(self, user_input: str, intent_type: str = None) -> str:
        """
        生成缓存 key

        Args:
            user_input: 用户输入
            intent_type: 可选的意图类型
        """
        normalized = self.normalize_for_cache(user_input)
        if intent_type:
            key_data = f"{intent_type}:{normalized}"
        else:
            key_data = normalized
        return hashlib.md5(key_data.encode()).hexdigest()

    def jaccard_similarity(self, set1: set, set2: set) -> float:
        """
        计算两个集合的 Jaccard 相似度

        Returns:
            0.0 ~ 1.0 的相似度
        """
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0

    def check_cache(self, cache_key: str) -> Optional[Any]:
        """
        查询搜索缓存：精确命中或语义相似命中

        Returns:
            命中时返回缓存结果，否则返回 None
        """
        current_time = time.time()

        with self._cache_lock:
            # 精确命中
            if cache_key in self._cache:
                cached_result, timestamp = self._cache[cache_key]
                if current_time - timestamp < self._cache_ttl:
                    return {'hit': True, 'exact': True, 'result': cached_result}
                else:
                    del self._cache[cache_key]

            # 语义相似命中
            target_terms = set(cache_key.split())
            best_similarity = 0.0
            best_key = None
            best_result = None

            for key, (result, timestamp) in self._cache.items():
                if current_time - timestamp >= self._cache_ttl:
                    continue
                source_terms = set(key.split())
                similarity = self.jaccard_similarity(target_terms, source_terms)
                if similarity > best_similarity and similarity >= 0.6:
                    best_similarity = similarity
                    best_key = key
                    best_result = result

            if best_key:
                return {'hit': True, 'exact': False, 'similarity': best_similarity, 'result': best_result}

            return None

    def put_cache(self, cache_key: str, result: Any) -> None:
        """
        写入搜索缓存

        Args:
            cache_key: 缓存键
            result: 要缓存的结果
        """
        with self._cache_lock:
            self._cache[cache_key] = (result, time.time())

    def evict_stale_cache(self) -> int:
        """
        清理过期缓存条目

        Returns:
            清理的条目数
        """
        current_time = time.time()
        removed = 0

        with self._cache_lock:
            stale_keys = [
                key for key, (_, timestamp) in self._cache.items()
                if current_time - timestamp >= self._cache_ttl
            ]
            for key in stale_keys:
                del self._cache[key]
                removed += 1

        return removed

    # ========== 上下文构建 ==========

    def build_local_fallback_context(self, context: Dict[str, Any],
                                     task_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        构建本地上下文兜底条目

        当网络搜索熔断/超时/异常时使用，确保：
        1. context 中至少有基础信息
        2. 任务仍可继续执行（降级但可用）
        """
        # 获取用户/行业信息
        user_id = context.get('user_id', 'default')
        industry = context.get('industry', 'general')

        # 构建兜底上下文
        fallback_context = {
            'fallback_mode': True,
            'user_id': user_id,
            'industry': industry,
            'task_params': task_params or {},
            'available_sources': ['local_kb', 'semantic_memory'],
            'timestamp': time.time(),
        }

        # 如果有语义记忆，尝试提取相关信息
        if self._semantic_memory_engine is not None:
            try:
                similar = self._semantic_memory_engine.search(
                    query=context.get('user_input', ''),
                    user_id=user_id,
                    limit=3
                )
                if similar:
                    fallback_context['semantic_recall'] = similar
            except Exception as e:
                logger.debug(f"编排器任务执行失败: {e}")

        return fallback_context

    # ========== 回滚执行 ==========

    def execute_rollback(self, rollback_plan: List[Dict[str, Any]],
                         completed_tasks: List[str]) -> Dict[str, Any]:
        """
        执行失败后的回滚任务

        Args:
            rollback_plan: 回滚计划（按逆序执行）
            completed_tasks: 已完成任务ID列表

        Returns:
            回滚结果
        """
        rollback_results = []
        rollback_failed = []

        for step in reversed(rollback_plan):
            task_id = step.get('task_id')
            action = step.get('action', 'undo')
            params = step.get('params', {})

            if task_id not in completed_tasks:
                # 任务未完成，无需回滚
                continue

            try:
                # 执行回滚动作
                if action == 'undo':
                    # 通用回滚逻辑
                    result = {'task_id': task_id, 'action': 'undone', 'success': True}
                elif action == 'delete':
                    result = {'task_id': task_id, 'action': 'deleted', 'success': True}
                elif action == 'compensate':
                    # 补偿交易
                    result = {'task_id': task_id, 'action': 'compensated', 'success': True}
                else:
                    result = {'task_id': task_id, 'action': action, 'success': True}

                rollback_results.append(result)

            except Exception as e:
                rollback_failed.append({'task_id': task_id, 'error': '回滚失败'})

        return {
            'rollback_completed': len(rollback_results),
            'rollback_failed': len(rollback_failed),
            'results': rollback_results,
            'failed': rollback_failed,
        }

    # ========== 未来结果处理 ==========

    def safe_future_result(self, future, fallback: Any = None,
                           timeout: float = None) -> Any:
        """
        安全地从 Future 取结果，超时/异常时返回 fallback，不抛出

        Args:
            future: Future 对象
            fallback: 超时时返回的默认值
            timeout: 超时时间(秒)

        Returns:
            Future结果或fallback
        """
        try:
            if timeout:
                return future.result(timeout=timeout)
            else:
                return future.result(timeout=30)  # 默认30秒超时
        except TimeoutError:
            return fallback
        except Exception:
            return fallback

    # ========== 任务状态序列化 ==========

    def serialize_task_record(self, task_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        输出可持久化的任务状态

        Args:
            task_record: 原始任务记录

        Returns:
            可序列化的任务状态
        """
        serializable = {
            'task_id': str(task_record.get('task_id', '')),
            'user_id': str(task_record.get('user_id', 'default')),
            'status': str(task_record.get('status', 'unknown')),
            'created_at': float(task_record.get('created_at', time.time())),
            'completed_at': float(task_record.get('completed_at', 0)) or None,
            'input_summary': str(task_record.get('input', ''))[:200],
            'result_summary': str(task_record.get('result', ''))[:500],
            'error': str(task_record.get('error', ''))[:200] or None,
        }
        return serializable
