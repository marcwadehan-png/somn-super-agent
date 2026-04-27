"""
__all__ = [
    'check_cache',
    'clear',
    'evict_stale',
    'get_stats',
    'jaccard_similarity',
    'make_cache_key',
    'normalize_for_cache',
    'put_cache',
]

搜索缓存 - 提供搜索结果缓存能力
"""

import hashlib
import logging
import threading
import time
from typing import Dict, Any, Optional, List, Set

logger = logging.getLogger(__name__)

class SearchCache:
    """搜索缓存封装类"""

    def __init__(self, ttl: float = 300.0, similarity_threshold: float = 0.5):
        """
        Args:
            ttl: 缓存有效期（秒）
            similarity_threshold: Jaccard 相似度阈值
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_lock = threading.Lock()
        self._ttl = ttl
        self._similarity_threshold = similarity_threshold

    def normalize_for_cache(self, text: str) -> str:
        """
        标准化文本用于缓存 key 生成

        Args:
            text: 原始文本

        Returns:
            标准化后的文本
        """
        import re
        # 去标点、归一化空白、转小写
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.lower().strip()

    def make_cache_key(self, description: str) -> str:
        """
        生成缓存键

        Args:
            description: 搜索描述

        Returns:
            缓存键
        """
        normalized = self.normalize_for_cache(description)
        return hashlib.md5(normalized.encode()).hexdigest()

    def jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """
        计算两个集合的 Jaccard 相似度

        Args:
            set1: 集合1
            set2: 集合2

        Returns:
            相似度 0~1
        """
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0

    def check_cache(self, description: str) -> Optional[List[Dict[str, Any]]]:
        """
        查询搜索缓存：精确命中或语义相似命中

        Args:
            description: 原始搜索描述

        Returns:
            命中的搜索结果列表，None表示未命中
        """
        with self._cache_lock:
            now = time.time()
            cache_key = self.make_cache_key(description)

            # 精确命中
            if cache_key in self._cache:
                entry = self._cache[cache_key]
                if now - entry["timestamp"] < self._ttl:
                    logger.info(f"[搜索缓存] 精确命中 {cache_key[:16]}...")
                    return entry["results"]
                else:
                    del self._cache[cache_key]

            # 语义相似命中
            desc_terms = set(self.normalize_for_cache(description).split())
            for key, entry in list(self._cache.items()):
                if now - entry["timestamp"] >= self._ttl:
                    del self._cache[key]
                    continue

                cached_terms = set(entry.get("terms", []))
                similarity = self.jaccard_similarity(desc_terms, cached_terms)
                if similarity >= self._similarity_threshold:
                    logger.info(f"[搜索缓存] 语义命中 {key[:16]}... (相似度 {similarity:.2f})")
                    return entry["results"]

            return None

    def put_cache(self, description: str, results: List[Dict[str, Any]]):
        """
        写入搜索缓存

        Args:
            description: 原始搜索描述
            results: 搜索结果
        """
        with self._cache_lock:
            cache_key = self.make_cache_key(description)
            terms = set(self.normalize_for_cache(description).split())

            self._cache[cache_key] = {
                "results": results,
                "timestamp": time.time(),
                "terms": terms,
            }

            logger.info(f"[搜索缓存] 写入 {cache_key[:16]} ({len(results)} 条)")

    def evict_stale(self) -> int:
        """
        清理过期缓存条目

        Returns:
            清理的条目数
        """
        with self._cache_lock:
            now = time.time()
            stale_keys = [
                key for key, entry in self._cache.items()
                if now - entry["timestamp"] >= self._ttl
            ]
            for key in stale_keys:
                del self._cache[key]

            if stale_keys:
                logger.info(f"[搜索缓存] 清理 {len(stale_keys)} 条过期缓存")

            return len(stale_keys)

    def clear(self):
        """清空缓存"""
        with self._cache_lock:
            self._cache.clear()
            logger.info("[搜索缓存] 已清空")

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        with self._cache_lock:
            return {
                "size": len(self._cache),
                "ttl": self._ttl,
                "similarity_threshold": self._similarity_threshold,
            }
