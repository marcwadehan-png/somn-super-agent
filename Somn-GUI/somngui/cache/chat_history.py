# -*- coding: utf-8 -*-
"""Somn GUI - 对话历史持久化

SQLite 存储对话记录，支持：
- 按会话分组保存对话
- 历史会话列表加载
- 对话内容全文搜索
- 会话管理（删除、重命名、导出）
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

from loguru import logger


class ChatHistoryDB:
    """对话历史数据库"""

    def __init__(self, db_path: str | Path = "cache_data/chat_history.db"):
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[Any] = None  # v1.0.0: 避免顶层 sqlite3 导入
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        import sqlite3  # v1.0.0: 延迟导入
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")

        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL DEFAULT '',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                message_count INTEGER DEFAULT 0,
                is_pinned INTEGER DEFAULT 0
            )
        """)

        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'agent', 'system')),
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
        """)

        # 全文搜索虚拟表
        self._conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
                content,
                content='messages',
                content_rowid='id',
                tokenize='unicode61'
            )
        """)

        # FTS 触发器：插入时同步
        self._conn.execute("""
            CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
                INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
            END
        """)

        # FTS 触发器：删除时同步
        self._conn.execute("""
            CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
                INSERT INTO messages_fts(messages_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
            END
        """)

        # FTS 触发器：更新时同步
        self._conn.execute("""
            CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages BEGIN
                INSERT INTO messages_fts(messages_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
                INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
            END
        """)

        self._conn.commit()
        logger.debug(f"对话历史数据库已初始化: {self._db_path}")

    # ── 会话管理 ──

    def create_session(self, session_id: str, title: str = "") -> dict:
        """创建新会话"""
        now = time.time()
        if not title:
            title = f"对话 {datetime.now().strftime('%m/%d %H:%M')}"
        self._conn.execute("""
            INSERT OR IGNORE INTO sessions (id, title, created_at, updated_at, message_count)
            VALUES (?, ?, ?, ?, 0)
        """, (session_id, title, now, now))
        self._conn.commit()
        return {"id": session_id, "title": title, "created_at": now}

    def get_session(self, session_id: str) -> Optional[dict]:
        """获取会话信息"""
        row = self._conn.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
        return dict(row) if row else None

    def list_sessions(
        self, limit: int = 50, offset: int = 0,
        pinned_first: bool = True
    ) -> List[dict]:
        """获取会话列表"""
        order = "is_pinned DESC, updated_at DESC" if pinned_first else "updated_at DESC"
        rows = self._conn.execute(
            f"SELECT * FROM sessions ORDER BY {order} LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
        return [dict(r) for r in rows]

    def update_session_title(self, session_id: str, title: str):
        """更新会话标题"""
        self._conn.execute(
            "UPDATE sessions SET title = ?, updated_at = ? WHERE id = ?",
            (title, time.time(), session_id)
        )
        self._conn.commit()

    def update_session_timestamp(self, session_id: str):
        """更新会话最后活跃时间"""
        self._conn.execute(
            "UPDATE sessions SET updated_at = ? WHERE id = ?",
            (time.time(), session_id)
        )
        self._conn.commit()

    def pin_session(self, session_id: str, pinned: bool = True):
        """置顶/取消置顶会话"""
        self._conn.execute(
            "UPDATE sessions SET is_pinned = ? WHERE id = ?",
            (int(pinned), session_id)
        )
        self._conn.commit()

    def delete_session(self, session_id: str):
        """删除会话及其所有消息"""
        self._conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        self._conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        self._conn.commit()

    def get_session_count(self) -> int:
        """获取总会话数"""
        row = self._conn.execute("SELECT COUNT(*) FROM sessions").fetchone()
        return row[0]

    # ── 消息管理 ──

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: dict | None = None
    ) -> int:
        """添加消息到会话，返回消息 ID"""
        now = time.time()
        meta_json = json.dumps(metadata or {}, ensure_ascii=False, default=str)
        cursor = self._conn.execute("""
            INSERT INTO messages (session_id, role, content, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, role, content, now, meta_json))

        # 更新会话统计
        self._conn.execute("""
            UPDATE sessions SET
                updated_at = ?,
                message_count = message_count + 1
            WHERE id = ?
        """, (now, session_id))
        self._conn.commit()

        # 自动从首条用户消息生成标题
        if role == "user":
            self._auto_title(session_id, content)

        return cursor.lastrowid

    def get_messages(
        self,
        session_id: str,
        limit: int = 200,
        offset: int = 0
    ) -> List[dict]:
        """获取会话消息列表"""
        rows = self._conn.execute(
            "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC LIMIT ? OFFSET ?",
            (session_id, limit, offset)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_message_count(self, session_id: str) -> int:
        """获取会话消息数"""
        row = self._conn.execute(
            "SELECT COUNT(*) FROM messages WHERE session_id = ?",
            (session_id,)
        ).fetchone()
        return row[0]

    def search_messages(
        self,
        query: str,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[dict]:
        """全文搜索消息"""
        if session_id:
            rows = self._conn.execute("""
                SELECT m.* FROM messages m
                JOIN messages_fts fts ON m.id = fts.rowid
                WHERE messages_fts MATCH ? AND m.session_id = ?
                ORDER BY m.timestamp DESC LIMIT ?
            """, (query, session_id, limit)).fetchall()
        else:
            rows = self._conn.execute("""
                SELECT m.* FROM messages m
                JOIN messages_fts fts ON m.id = fts.rowid
                WHERE messages_fts MATCH ?
                ORDER BY m.timestamp DESC LIMIT ?
            """, (query, limit)).fetchall()
        return [dict(r) for r in rows]

    # ── 批量操作 ──

    def export_session(self, session_id: str) -> Optional[dict]:
        """导出完整会话（用于备份）"""
        session = self.get_session(session_id)
        if not session:
            return None
        messages = self.get_messages(session_id, limit=10000)
        return {
            "session": session,
            "messages": messages,
            "exported_at": time.time(),
        }

    def import_session(self, data: dict) -> str:
        """导入会话"""
        session = data.get("session", {})
        session_id = session.get("id", f"imported_{int(time.time())}")
        title = session.get("title", "导入的对话")

        self.create_session(session_id, title)

        for msg in data.get("messages", []):
            self._conn.execute("""
                INSERT INTO messages (session_id, role, content, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session_id,
                msg.get("role", "system"),
                msg.get("content", ""),
                msg.get("timestamp", time.time()),
                json.dumps(msg.get("metadata", {}), ensure_ascii=False, default=str),
            ))

        count = len(data.get("messages", []))
        self._conn.execute(
            "UPDATE sessions SET message_count = ? WHERE id = ?",
            (count, session_id)
        )
        self._conn.commit()
        return session_id

    # ── 清理 ──

    def delete_old_sessions(self, days: int = 90):
        """删除超过 N 天的非置顶会话"""
        cutoff = time.time() - days * 86400
        # 先获取要删除的 session_id
        rows = self._conn.execute(
            "SELECT id FROM sessions WHERE updated_at < ? AND is_pinned = 0",
            (cutoff,)
        ).fetchall()
        ids = [r["id"] for r in rows]
        if not ids:
            return 0

        placeholders = ",".join("?" * len(ids))
        self._conn.execute(
            f"DELETE FROM messages WHERE session_id IN ({placeholders})", ids
        )
        self._conn.execute(
            f"DELETE FROM sessions WHERE id IN ({placeholders})", ids
        )
        self._conn.commit()
        return len(ids)

    def vacuum(self):
        """压缩数据库"""
        self._conn.execute("VACUUM")

    def stats(self) -> dict:
        """统计信息"""
        sessions = self._conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        messages = self._conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        db_size = self._db_path.stat().st_size if self._db_path.exists() else 0
        return {
            "sessions": sessions,
            "messages": messages,
            "db_size_bytes": db_size,
            "db_size_mb": round(db_size / 1024 / 1024, 2),
        }

    # ── 内部方法 ──

    def _auto_title(self, session_id: str, first_user_msg: str):
        """从首条用户消息自动生成会话标题"""
        # 仅在标题还是默认值时更新
        row = self._conn.execute(
            "SELECT message_count FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if not row:
            return
        # v1.0.0: 避免顶层 sqlite3 导入，用鸭子类型判断 Row
        try:
            count = row["message_count"] if hasattr(row, 'keys') else row[0]
        except (IndexError, KeyError):
            count = 1
        if count != 1:
            return  # 不是第一条消息，不更新标题

        # 截取前 30 字符作为标题
        title = first_user_msg.strip().replace("\n", " ")[:30]
        if len(first_user_msg.strip()) > 30:
            title += "..."
        self.update_session_title(session_id, title)

    def close(self):
        """关闭数据库"""
        if self._conn:
            self._conn.close()
            self._conn = None
