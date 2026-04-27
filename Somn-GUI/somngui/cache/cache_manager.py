"""
Somn GUI - 缓存管理器
统一缓存入口: KV缓存 + 对象缓存 + 预加载 + 离线缓存
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from .cache_db import CacheDB

logger = logging.getLogger(__name__)


class CacheManager:
    """缓存管理器 - 统一缓存入口"""

    def __init__(self, config: dict = None):
        cache_cfg = (config or {}).get("cache", {})
        self._db_path = cache_cfg.get("db_path", "cache_data/cache.db")
        self._default_ttl = cache_cfg.get("default_ttl", 1800)
        self._knowledge_ttl = cache_cfg.get("knowledge_ttl", 86400)
        self._config_ttl = cache_cfg.get("config_ttl", 0)
        self._status_ttl = cache_cfg.get("status_ttl", 300)

        self._db: Optional[CacheDB] = None  # 延迟初始化
        self._preloaded = False
        self._offline_mode = False

    @property
    def db(self) -> CacheDB:
        if self._db is None:
            self._db = CacheDB(self._db_path)
        return self._db

    @property
    def is_offline(self) -> bool:
        return self._offline_mode

    def set_offline(self, offline: bool):
        """设置离线模式"""
        self._offline_mode = offline
        logger.info(f"{'进入' if offline else '退出'}离线模式")

    # ── 通用缓存接口 ──

    def get(self, key: str) -> Optional[Any]:
        return self.db.get(key)

    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        self.db.set(key, value, ttl=ttl or self._default_ttl)

    def get_cached_response(self, cache_key: str) -> Optional[dict]:
        """获取缓存的API响应"""
        return self.db.get(cache_key)

    def cache_response(self, cache_key: str, response: dict, ttl: Optional[float] = None):
        """缓存API响应"""
        if response.get("success"):
            self.db.set(cache_key, response, ttl=ttl or self._default_ttl)

    # ── 预加载 ──

    async def preload_data(self, backend_client=None):
        """预加载高频数据"""
        if self._preloaded:
            return

        logger.info("开始预加载缓存数据...")

        if backend_client:
            try:
                # 预加载: 系统配置 (TTL=None 表示永不过期)
                config_resp = await backend_client.get("/config")
                if config_resp.get("success"):
                    self.db.set("preloaded:config", config_resp["data"], ttl=None)
                    logger.info("  [OK] 系统配置")

                # 预加载: 系统状态
                status_resp = await backend_client.get("/status")
                if status_resp.get("success"):
                    self.db.set("preloaded:status", status_resp["data"], ttl=self._status_ttl)
                    logger.info("  [OK] 系统状态")

                # 预加载: 学派列表
                schools_resp = await backend_client.get("/wisdom/schools")
                if schools_resp.get("success"):
                    self.db.set("preloaded:schools", schools_resp["data"], ttl=self._knowledge_ttl)
                    logger.info("  [OK] 智慧学派列表")

                # 预加载: 知识库索引
                kb_resp = await backend_client.get("/knowledge?page_size=100")
                if kb_resp.get("success"):
                    self.db.set("preloaded:knowledge_index", kb_resp["data"], ttl=self._knowledge_ttl)
                    logger.info("  [OK] 知识库索引")

            except Exception as e:
                logger.warning(f"预加载部分失败: {e}")

        self._preloaded = True
        logger.info("预加载完成")

    def get_preloaded(self, key: str) -> Optional[dict]:
        """获取预加载数据"""
        return self.db.get(f"preloaded:{key}")

    # ── 离线缓存 ──

    def queue_request(self, method: str, path: str, body: str = ""):
        """将请求加入离线队列"""
        if self._offline_mode:
            self.db.add_pending_request(method, path, body)
            logger.info(f"离线请求已入队: {method} {path}")

    async def replay_pending(self, backend_client) -> int:
        """重放离线请求队列"""
        pending = self.db.get_pending_requests()
        replayed = 0
        for req in pending:
            try:
                body = req.get("body", "")
                json_body = json.loads(body) if body else None
                resp = await backend_client.post(req["path"], json_data=json_body)
                if resp.get("success"):
                    self.db.remove_pending_request(req["id"])
                    replayed += 1
            except Exception as e:
                logger.warning(f"重放失败 [{req['id']}]: {e}")
        if replayed > 0:
            logger.info(f"已重放 {replayed} 个离线请求")
        return replayed

    def get_pending_count(self) -> int:
        """获取待处理请求数"""
        return self.db.stats().get("pending_requests", 0)

    # ── 管理 ──

    def stats(self) -> dict:
        return self.db.stats()

    def clear_all(self):
        self.db.clear_all()
        self._preloaded = False
        logger.info("缓存已清空")

    def close(self):
        if self._db:
            self._db.close()
            self._db = None
