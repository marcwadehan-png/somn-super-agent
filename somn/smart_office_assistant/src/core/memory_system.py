"""
记忆系统 - Memory System
实现短期记忆,长期记忆和向量检索
"""

import logging
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from loguru import logger

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    chromadb = None
    Settings = None
    CHROMADB_AVAILABLE = False

logger = logging.getLogger(__name__)

# [v9.0 优化] 全局延迟加载控制
_CHROMADB_INITIALIZED = False
@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    memory_type: str  # 'short_term', 'long_term', 'episodic', 'semantic'
    timestamp: datetime
    importance: float  # 0.0 - 1.0
    context: Dict[str, Any]
    tags: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """将记忆条目转换为字典
        
        Returns:
            Dict[str, Any]: 包含所有字段的字典，datetime字段转为ISO格式
        """
        return {
            'id': self.id,
            'content': self.content,
            'memory_type': self.memory_type,
            'timestamp': self.timestamp.isoformat(),
            'importance': self.importance,
            'context': self.context,
            'tags': self.tags
        }

class MemorySystem:
    """
    智能记忆系统
    - 短期记忆:当前会话的上下文
    - 长期记忆:持久化存储的重要信息
    - 向量检索:基于语义相似度的记忆检索 [懒加载]

    [v9.0 优化] ChromaDB 默认不加载，按需启用以加速启动
    """

    def __init__(self, data_path: str = "data/memory", enable_vector: bool = False):
        """
        初始化记忆系统

        Args:
            data_path: 数据存储路径
            enable_vector: 是否启用向量检索(默认False，加速启动)
        """
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)

        # 短期记忆(内存中)
        self.short_term_memory: List[MemoryEntry] = []
        self.short_term_limit = 50

        # SQLite 数据库(长期记忆元数据)
        self.db_path = self.data_path / "memory.db"
        self._init_sqlite()

        # [v9.0 优化] ChromaDB 向量数据库 - 默认懒加载
        self.chroma_client = None
        self.collection = None
        self._vector_enabled = enable_vector  # 标记向量功能状态

        # 只有明确启用时才加载ChromaDB
        if enable_vector and CHROMADB_AVAILABLE:
            self._init_vector_db()
        elif CHROMADB_AVAILABLE:
            logger.info("记忆系统init完成(SQLite模式)，向量检索已就绪(按需启用)")
        else:
            logger.warning("chromadb 未安装,记忆系统将以 SQLite 模式降级运行")
    
    def close(self):
        """
        关闭并清理资源
        """
        try:
            # 清理ChromaDB资源
            if hasattr(self, 'chroma_client'):
                self.chroma_client = None
            
            # SQLite连接会自动关闭(使用with语句)
            logger.info("记忆系统资源已清理")
        except Exception as e:
            logger.error(f"清理记忆系统资源失败: {e}")
    
    def __del__(self):
        """析构时自动清理"""
        self.close()
    
    def _init_vector_db(self):
        """[v9.0 优化] 延迟初始化ChromaDB向量数据库"""
        global _CHROMADB_INITIALIZED
        if _CHROMADB_INITIALIZED:
            return
        try:
            if not CHROMADB_AVAILABLE:
                logger.warning("ChromaDB未安装，向量检索功能不可用")
                return

            self.chroma_client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=str(self.data_path / "vector_db")
            ))
            self.collection = self.chroma_client.get_or_create_collection(
                name="memories",
                metadata={"hnsw:space": "cosine"}
            )
            self._vector_enabled = True
            _CHROMADB_INITIALIZED = True
            logger.info("ChromaDB向量数据库加载完成")
        except Exception as e:
            logger.warning(f"ChromaDB加载失败: {e}，向量检索功能不可用")
            self._vector_enabled = False

    def enable_vector_search(self):
        """[v9.0 优化] 按需启用向量检索功能"""
        if not self._vector_enabled:
            self._init_vector_db()
        return self._vector_enabled

    def _init_sqlite(self):
        """init SQLite 数据库（修复版：添加timeout参数）"""
        with sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    importance REAL NOT NULL,
                    context TEXT,
                    tags TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_type ON memories(memory_type)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)
            """)
            conn.commit()
    
    def add_memory(
        self,
        content: str,
        memory_type: str = "short_term",
        importance: float = 0.5,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        embedding: Optional[List[float]] = None
    ) -> str:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要程度 (0-1)
            context: 上下文信息
            tags: 标签列表
            embedding: 向量嵌入(可选)
        
        Returns:
            记忆ID
        """
        memory_id = f"{memory_type}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        entry = MemoryEntry(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            timestamp=datetime.now(),
            importance=importance,
            context=context or {},
            tags=tags or []
        )
        
        # 短期记忆直接存入内存
        if memory_type == "short_term":
            self.short_term_memory.append(entry)
            self._trim_short_term_memory()
        
        # 长期记忆持久化存储
        if memory_type in ["long_term", "episodic", "semantic"]:
            self._persist_memory(entry)
            
            # 添加到向量数据库
            if embedding and self.collection is not None:
                self.collection.add(
                    ids=[memory_id],
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[{
                        "type": memory_type,
                        "importance": importance,
                        "timestamp": entry.timestamp.isoformat()
                    }]
                )
        
        logger.debug(f"添加记忆: {memory_id} (类型: {memory_type})")
        return memory_id
    
    def _trim_short_term_memory(self):
        """修剪短期记忆,保持容量限制"""
        if len(self.short_term_memory) > self.short_term_limit:
            # 按重要性和时间排序,移除最不重要的
            self.short_term_memory.sort(
                key=lambda x: (x.importance, x.timestamp),
                reverse=True
            )
            removed = self.short_term_memory[self.short_term_limit:]
            self.short_term_memory = self.short_term_memory[:self.short_term_limit]
            
            # 重要的短期记忆转为长期记忆
            for entry in removed:
                if entry.importance > 0.7:
                    entry.memory_type = "long_term"
                    self._persist_memory(entry)
    
    def _persist_memory(self, entry: MemoryEntry):
        """持久化记忆到 SQLite"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO memories 
                (id, content, memory_type, timestamp, importance, context, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.id,
                    entry.content,
                    entry.memory_type,
                    entry.timestamp.isoformat(),
                    entry.importance,
                    json.dumps(entry.context, ensure_ascii=False),
                    json.dumps(entry.tags, ensure_ascii=False)
                )
            )
            conn.commit()
    
    def search_memories(
        self,
        query: str = "",
        memory_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
        embedding: Optional[List[float]] = None
    ) -> List[MemoryEntry]:
        """
        搜索记忆
        
        Args:
            query: 文本查询
            memory_type: 按类型筛选
            tags: 按标签筛选
            limit: 返回数量限制
            embedding: 向量查询(可选)
        
        Returns:
            记忆条目列表
        """
        results = []
        
        # 1. 搜索短期记忆
        if memory_type is None or memory_type == "short_term":
            for entry in self.short_term_memory:
                if query.lower() in entry.content.lower():
                    if tags is None or any(tag in entry.tags for tag in tags):
                        results.append(entry)
        
        # 2. 向量相似度搜索(如果有 embedding) - [v9.0 优化] 按需加载
        if embedding and self.collection is not None:
            try:
                vector_results = self.collection.query(
                    query_embeddings=[embedding],
                    n_results=limit,
                    where={"type": memory_type} if memory_type else None
                )
                # 将向量搜索结果合并到results [修复上下文丢失问题]
                if vector_results and vector_results.get("ids"):
                    for i, vid in enumerate(vector_results.get("ids", [[]])[0]):
                        if i >= len(vector_results.get("documents", [[]])[0]):
                            break
                        doc = vector_results.get("documents", [[]])[0][i]
                        dist = vector_results.get("distances", [[]])[0][i] if vector_results.get("distances") and i < len(vector_results.get("distances", [[]])[0]) else 1.0
                        meta = vector_results.get("metadatas", [{}])[0][i] if vector_results.get("metadatas") and i < len(vector_results.get("metadatas", [{}])) else {}
                        
                        # 计算相似度 (cosine distance转similarity)
                        similarity = 1.0 - dist if dist is not None else 0.5
                        
                        # 从SQLite获取完整记录或创建新条目
                        entry = MemoryEntry(
                            id=vid,
                            content=doc,
                            memory_type=meta.get("type", "vector"),
                            timestamp=datetime.now(),
                            importance=similarity,
                            context=meta,
                            tags=[]
                        )
                        results.append(entry)
            except Exception as e:
                logger.debug(f"向量搜索失败: {e}")
        
        # 3. SQLite 搜索长期记忆
        with sqlite3.connect(self.db_path) as conn:
            sql = "SELECT * FROM memories WHERE 1=1"
            params = []
            
            if memory_type and memory_type != "short_term":
                sql += " AND memory_type = ?"
                params.append(memory_type)
            
            if query:
                sql += " AND content LIKE ?"
                params.append(f"%{query}%")
            
            if tags:
                placeholders = ','.join('?' * len(tags))
                sql += f" AND tags LIKE '%' || ? || '%'"
                params.extend(tags)
            
            sql += " ORDER BY importance DESC, timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            
            for row in rows:
                entry = MemoryEntry(
                    id=row[0],
                    content=row[1],
                    memory_type=row[2],
                    timestamp=datetime.fromisoformat(row[3]),
                    importance=row[4],
                    context=json.loads(row[5]) if row[5] else {},
                    tags=json.loads(row[6]) if row[6] else []
                )
                results.append(entry)
        
        return results[:limit]
    
    def get_recent_context(self, n: int = 5) -> str:
        """get最近的上下文记忆"""
        recent = self.short_term_memory[-n:] if len(self.short_term_memory) >= n else self.short_term_memory
        return "\n".join([f"[{e.timestamp.strftime('%H:%M')}] {e.content}" for e in recent])
    
    def consolidate_memories(self):
        """
        记忆整合:将相关的短期记忆合并为长期记忆
        定期运行以优化记忆存储
        """
        logger.info("开始记忆整合...")
        
        # 找出高重要性的短期记忆
        important_memories = [
            e for e in self.short_term_memory 
            if e.importance > 0.8
        ]
        
        for entry in important_memories:
            entry.memory_type = "long_term"
            self._persist_memory(entry)
            self.short_term_memory.remove(entry)
        
        logger.info(f"整合了 {len(important_memories)} 条记忆到长期存储")
    
    def forget_memory(self, memory_id: str) -> bool:
        """删除特定记忆"""
        # 从短期记忆中删除
        self.short_term_memory = [
            e for e in self.short_term_memory if e.id != memory_id
        ]
        
        # 从长期记忆中删除
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
        
        # 从向量数据库删除
        try:
            if self.collection is not None:
                self.collection.delete(ids=[memory_id])
        except Exception as e:
            logger.debug(f"向量删除失败: {e}")
        
        logger.debug(f"删除记忆: {memory_id}")
        return True
    
    def get_stats(self) -> Dict[str, int]:
        """get记忆统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT memory_type, COUNT(*) FROM memories GROUP BY memory_type"
            )
            stats = dict(cursor.fetchall())
        
        stats['short_term'] = len(self.short_term_memory)
        return stats

# ───────────────────────────────────────────────────────────────
# 模块导出
# ───────────────────────────────────────────────────────────────
__all__ = [
    'MemoryEntry',
    'MemorySystem',
]
