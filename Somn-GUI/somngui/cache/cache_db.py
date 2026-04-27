"""
Somn GUI - 本地缓存数据库
SQLite 持久化缓存，支持 KV 存储、对象缓存、TTL 过期
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CacheDB:
    """本地缓存数据库"""

    def __init__(self, db_path: str = "cache_data/cache.db"):
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[Any] = None  # v1.0.0: 避免顶层 sqlite3 导入
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        import sqlite3  # v1.0.0: 延迟导入
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS kv_cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                ttl REAL DEFAULT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
        """)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS obj_cache (
                id TEXT PRIMARY KEY,
                category TEXT DEFAULT '',
                data TEXT NOT NULL,
                ttl REAL DEFAULT NULL,
                created_at REAL NOT NULL
            )
        """)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS pending_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method TEXT NOT NULL,
                path TEXT NOT NULL,
                body TEXT DEFAULT '',
                created_at REAL NOT NULL,
                retry_count INTEGER DEFAULT 0
            )
        """)
        self._conn.commit()

    # ── KV 缓存 ──

    def get(self, key: str) -> Optional[Any]:
        """获取KV缓存值"""
        self._cleanup_expired("kv_cache")
        row = self._conn.execute(
            "SELECT value, ttl, updated_at FROM kv_cache WHERE key = ?",
            (key,)
        ).fetchone()
        if row is None:
            return None
        value, ttl, updated = row
        if ttl and (time.time() - updated) > ttl:
            self._conn.execute("DELETE FROM kv_cache WHERE key = ?", (key,))
            self._conn.commit()
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """设置KV缓存值"""
        now = time.time()
        serialized = json.dumps(value, ensure_ascii=False, default=str)
        self._conn.execute("""
            INSERT OR REPLACE INTO kv_cache (key, value, ttl, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (key, serialized, ttl, now, now))
        self._conn.commit()

    def delete(self, key: str):
        """删除KV缓存"""
        self._conn.execute("DELETE FROM kv_cache WHERE key = ?", (key,))
        self._conn.commit()

    # ── 对象缓存 ──

    def get_object(self, obj_id: str, category: str = "") -> Optional[dict]:
        """获取对象缓存"""
        self._cleanup_expired("obj_cache")
        row = self._conn.execute(
            "SELECT data, ttl, created_at FROM obj_cache WHERE id = ? AND category = ?",
            (obj_id, category)
        ).fetchone()
        if row is None:
            return None
        data, ttl, created = row
        if ttl and (time.time() - created) > ttl:
            self._conn.execute(
                "DELETE FROM obj_cache WHERE id = ? AND category = ?",
                (obj_id, category)
            )
            self._conn.commit()
            return None
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return None

    def set_object(self, obj_id: str, data: dict, category: str = "", ttl: Optional[float] = None):
        """设置对象缓存"""
        serialized = json.dumps(data, ensure_ascii=False, default=str)
        self._conn.execute("""
            INSERT OR REPLACE INTO obj_cache (id, category, data, ttl, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (obj_id, category, serialized, ttl, time.time()))
        self._conn.commit()

    # ── 离线请求队列 ──

    def add_pending_request(self, method: str, path: str, body: str = ""):
        """添加待处理请求"""
        self._conn.execute("""
            INSERT INTO pending_requests (method, path, body, created_at, retry_count)
            VALUES (?, ?, ?, ?, 0)
        """, (method, path, body, time.time()))
        self._conn.commit()

    def get_pending_requests(self, limit: int = 50) -> list:
        """获取待处理请求列表"""
        rows = self._conn.execute(
            "SELECT id, method, path, body, created_at FROM pending_requests ORDER BY created_at LIMIT ?",
            (limit,)
        ).fetchall()
        return [
            {"id": r[0], "method": r[1], "path": r[2], "body": r[3], "created_at": r[4]}
            for r in rows
        ]

    def remove_pending_request(self, req_id: int):
        """移除已处理的请求"""
        self._conn.execute("DELETE FROM pending_requests WHERE id = ?", (req_id,))
        self._conn.commit()

    def clear_pending_requests(self):
        """清空所有待处理请求"""
        self._conn.execute("DELETE FROM pending_requests")
        self._conn.commit()

    # ── 清理 ──

    def _cleanup_expired(self, table: str):
        """清理过期条目 (TTL=NULL 表示永不过期，不会被清理)"""
        if table not in ("kv_cache", "obj_cache"):
            return
        now = time.time()
        self._conn.execute(
            f"DELETE FROM {table} WHERE ttl IS NOT NULL AND (created_at + ttl) < ?",
            (now,)
        )
        self._conn.commit()

    def clear_all(self):
        """清空所有缓存"""
        for table in ("kv_cache", "obj_cache", "pending_requests"):
            self._conn.execute(f"DELETE FROM {table}")
        self._conn.commit()

    def stats(self) -> dict:
        """缓存统计"""
        kv_count = self._conn.execute("SELECT COUNT(*) FROM kv_cache").fetchone()[0]
        obj_count = self._conn.execute("SELECT COUNT(*) FROM obj_cache").fetchone()[0]
        pending_count = self._conn.execute("SELECT COUNT(*) FROM pending_requests").fetchone()[0]
        db_size = self._db_path.stat().st_size if self._db_path.exists() else 0
        return {
            "kv_entries": kv_count,
            "obj_entries": obj_count,
            "pending_requests": pending_count,
            "db_size_bytes": db_size,
            "db_size_mb": round(db_size / 1024 / 1024, 2),
        }

    def close(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()
            self._conn = None
