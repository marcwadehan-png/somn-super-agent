"""
__all__ = [
    'check_circuit_breaker',
    'clear_llm_cache',
    'clear_search_cache',
    'get_analysis_executor',
    'get_cache_stats',
    'get_circuit_breaker_state',
    'record_search_failure',
    'record_search_success',
    'shutdown_executor',
    'submit_analysis_task',
]

路由调度器 - 提供任务路由选择和并行分析能力

从 SomnCore 路由和并行分析相关方法提取
"""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class RouterDispatcher:
    """任务路由调度器"""

    def __init__(self):
        """初始化路由调度器"""
        self._analysis_executor: Optional[ThreadPoolExecutor] = None
        self._analysis_executor_lock = threading.Lock()

        # 网络搜索熔断器状态
        self._search_circuit_breaker: Dict[str, Any] = {
            "state": "closed",
            "consecutive_failures": 0,
            "failure_threshold": 3,
            "recovery_timeout": 30.0,
            "last_failure_time": None,
        }

        # 同会话搜索结果缓存
        self._search_result_cache: Dict[str, Dict[str, Any]] = {}
        self._search_result_cache_lock = threading.Lock()
        self._SEARCH_CACHE_TTL = 300.0
        self._SEARCH_SIMILARITY_THRESHOLD = 0.5

        # LLM 结果缓存
        self._llm_result_cache: Dict[str, Dict[str, Any]] = {}
        self._llm_result_cache_lock = threading.Lock()
        self._LLM_CACHE_TTL = 600.0
        self._LLM_CACHE_MAX_ENTRIES = 200
        self._LLM_CACHE_PROMPT_PREFIX = 256

    def get_analysis_executor(self) -> ThreadPoolExecutor:
        """获取并行分析用线程池（懒加载、线程安全）"""
        if self._analysis_executor is None:
            with self._analysis_executor_lock:
                if self._analysis_executor is None:
                    self._analysis_executor = ThreadPoolExecutor(
                        max_workers=3, thread_name_prefix="somn_analysis"
                    )
        return self._analysis_executor

    def submit_analysis_task(self, func, *args, **kwargs) -> Future:
        """提交分析任务到线程池"""
        executor = self.get_analysis_executor()
        return executor.submit(func, *args, **kwargs)

    def shutdown_executor(self):
        """关闭线程池"""
        if self._analysis_executor:
            self._analysis_executor.shutdown(wait=True)
            self._analysis_executor = None

    def get_circuit_breaker_state(self) -> str:
        """获取熔断器状态"""
        return self._search_circuit_breaker["state"]

    def record_search_failure(self):
        """记录搜索失败"""
        self._search_circuit_breaker["consecutive_failures"] += 1
        if self._search_circuit_breaker["consecutive_failures"] >= self._search_circuit_breaker["failure_threshold"]:
            self._search_circuit_breaker["state"] = "open"
            import time
            self._search_circuit_breaker["last_failure_time"] = time.time()
            logger.warning("[熔断器] 搜索连续失败，熔断器打开")

    def record_search_success(self):
        """记录搜索成功"""
        if self._search_circuit_breaker["state"] == "half_open":
            self._search_circuit_breaker["state"] = "closed"
            self._search_circuit_breaker["consecutive_failures"] = 0
            logger.info("[熔断器] 搜索恢复，熔断器关闭")

    def check_circuit_breaker(self) -> bool:
        """
        检查熔断器状态

        Returns:
            True 表示可以通过，False 表示熔断
        """
        state = self._search_circuit_breaker["state"]
        if state == "closed":
            return True
        if state == "open":
            import time
            last_failure = self._search_circuit_breaker.get("last_failure_time")
            if last_failure and (time.time() - last_failure) > self._search_circuit_breaker["recovery_timeout"]:
                self._search_circuit_breaker["state"] = "half_open"
                logger.info("[熔断器] 进入半开状态")
                return True
            return False
        # half_open 状态允许通过
        return True

    def clear_search_cache(self):
        """清理搜索缓存"""
        with self._search_result_cache_lock:
            self._search_result_cache.clear()

    def clear_llm_cache(self):
        """清理LLM缓存"""
        with self._llm_result_cache_lock:
            self._llm_result_cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        with self._search_result_cache_lock:
            search_size = len(self._search_result_cache)
        with self._llm_result_cache_lock:
            llm_size = len(self._llm_result_cache)
        return {
            "search_cache_size": search_size,
            "llm_cache_size": llm_size,
            "circuit_breaker_state": self._search_circuit_breaker["state"],
            "consecutive_failures": self._search_circuit_breaker["consecutive_failures"],
        }
