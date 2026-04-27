"""
知识库系统 - Knowledge Base System
管理结构化知识,支持自动索引和检索
"""

import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import threading

from loguru import logger

@dataclass
class KnowledgeEntry:
    """知识条目"""
    id: str
    title: str
    content: str
    category: str
    source: str  # 来源文件或URL
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    tags: List[str]
    embedding_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'source': self.source,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata,
            'tags': self.tags,
            'embedding_id': self.embedding_id
        }

@dataclass
class Concept:
    """概念/知识点"""
    id: str
    name: str
    definition: str
    related_concepts: List[str]
    examples: List[str]
    category: str
    confidence: float  # 置信度

class KnowledgeBase:
    """
    知识库系统
    - 文档索引与管理
    - 概念提取与关联
    - 语义检索
    - 知识图谱构建
    """
    
    def __init__(self, data_path: str = "data/knowledge"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # SQLite 数据库
        self.db_path = self.data_path / "knowledge.db"
        self._init_database()
        
        # 文件索引缓存
        self.file_index: Dict[str, Dict[str, Any]] = {}
        self._load_file_index()
        
        # 线程锁
        self._lock = threading.RLock()
        
        logger.info("知识库系统init完成")
    
    def _init_database(self):
        """init数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            # 知识条目表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_entries (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT,
                    source TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    metadata TEXT,
                    tags TEXT,
                    embedding_id TEXT
                )
            """)
            
            # 概念表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS concepts (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    definition TEXT,
                    related_concepts TEXT,
                    examples TEXT,
                    category TEXT,
                    confidence REAL
                )
            """)
            
            # 知识关系表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_relations (
                    id TEXT PRIMARY KEY,
                    source_id TEXT,
                    target_id TEXT,
                    relation_type TEXT,
                    strength REAL,
                    metadata TEXT
                )
            """)
            
            # 创建索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kb_category ON knowledge_entries(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kb_source ON knowledge_entries(source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_concept_name ON concepts(name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_relation_source ON knowledge_relations(source_id)")
            
            conn.commit()
    
    def _load_file_index(self):
        """加载文件索引"""
        index_path = self.data_path / "file_index.json"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                self.file_index = json.load(f)
    
    def _save_file_index(self):
        """保存文件索引"""
        index_path = self.data_path / "file_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(self.file_index, f, ensure_ascii=False, indent=2)
    
    def add_knowledge(
        self,
        title: str,
        content: str,
        category: str = "general",
        source: str = "",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedding_id: Optional[str] = None
    ) -> str:
        """
        添加知识条目
        
        Returns:
            知识条目ID
        """
        with self._lock:
            entry_id = hashlib.md5(f"{title}_{source}_{datetime.now()}".encode()).hexdigest()
            now = datetime.now()
            
            entry = KnowledgeEntry(
                id=entry_id,
                title=title,
                content=content,
                category=category,
                source=source,
                created_at=now,
                updated_at=now,
                metadata=metadata or {},
                tags=tags or [],
                embedding_id=embedding_id
            )
            
            # 保存到数据库
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO knowledge_entries 
                    (id, title, content, category, source, created_at, updated_at, metadata, tags, embedding_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        entry.id,
                        entry.title,
                        entry.content,
                        entry.category,
                        entry.source,
                        entry.created_at.isoformat(),
                        entry.updated_at.isoformat(),
                        json.dumps(entry.metadata, ensure_ascii=False),
                        json.dumps(entry.tags, ensure_ascii=False),
                        entry.embedding_id
                    )
                )
                conn.commit()
            
            logger.debug(f"添加知识条目: {title}")
            return entry_id
    
    def update_knowledge(
        self,
        entry_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """更新知识条目"""
        with self._lock:
            # get现有条目
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT * FROM knowledge_entries WHERE id = ?", (entry_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return False
                
                # 构建更新语句
                updates = []
                params = []
                
                if title is not None:
                    updates.append("title = ?")
                    params.append(title)
                if content is not None:
                    updates.append("content = ?")
                    params.append(content)
                if category is not None:
                    updates.append("category = ?")
                    params.append(category)
                if tags is not None:
                    updates.append("tags = ?")
                    params.append(json.dumps(tags, ensure_ascii=False))
                if metadata is not None:
                    existing_meta = json.loads(row[7]) if row[7] else {}
                    existing_meta.update(metadata)
                    updates.append("metadata = ?")
                    params.append(json.dumps(existing_meta, ensure_ascii=False))
                
                updates.append("updated_at = ?")
                params.append(datetime.now().isoformat())
                params.append(entry_id)
                
                sql = f"UPDATE knowledge_entries SET {', '.join(updates)} WHERE id = ?"
                conn.execute(sql, params)
                conn.commit()
            
            logger.debug(f"更新知识条目: {entry_id}")
            return True
    
    def search_knowledge(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[KnowledgeEntry]:
        """
        搜索知识库
        
        Args:
            query: 搜索关键词
            category: 按分类筛选
            tags: 按标签筛选
            limit: 返回数量
        
        Returns:
            知识条目列表
        """
        with sqlite3.connect(self.db_path) as conn:
            sql = "SELECT * FROM knowledge_entries WHERE 1=1"
            params = []
            
            if query:
                sql += " AND (title LIKE ? OR content LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%"])
            
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            sql += " ORDER BY updated_at DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                entry = KnowledgeEntry(
                    id=row[0],
                    title=row[1],
                    content=row[2],
                    category=row[3],
                    source=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    updated_at=datetime.fromisoformat(row[6]),
                    metadata=json.loads(row[7]) if row[7] else {},
                    tags=json.loads(row[8]) if row[8] else [],
                    embedding_id=row[9]
                )
                results.append(entry)
            
            return results
    
    def add_concept(
        self,
        name: str,
        definition: str,
        category: str = "general",
        related_concepts: Optional[List[str]] = None,
        examples: Optional[List[str]] = None,
        confidence: float = 1.0
    ) -> str:
        """添加概念定义"""
        concept_id = hashlib.md5(name.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO concepts 
                (id, name, definition, related_concepts, examples, category, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    concept_id,
                    name,
                    definition,
                    json.dumps(related_concepts or [], ensure_ascii=False),
                    json.dumps(examples or [], ensure_ascii=False),
                    category,
                    confidence
                )
            )
            conn.commit()
        
        logger.debug(f"添加概念: {name}")
        return concept_id
    
    def get_concept(self, name: str) -> Optional[Concept]:
        """get概念定义"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM concepts WHERE name = ?", (name,)
            )
            row = cursor.fetchone()
            
            if row:
                return Concept(
                    id=row[0],
                    name=row[1],
                    definition=row[2],
                    related_concepts=json.loads(row[3]) if row[3] else [],
                    examples=json.loads(row[4]) if row[4] else [],
                    category=row[5],
                    confidence=row[6]
                )
        return None
    
    def index_file(
        self,
        file_path: str,
        content: str,
        file_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        索引文件到知识库
        
        Returns:
            知识条目ID
        """
        file_path = Path(file_path)
        file_hash = hashlib.md5(content.encode()).hexdigest()
        
        # 检查文件是否已索引
        if str(file_path) in self.file_index:
            existing = self.file_index[str(file_path)]
            if existing.get('hash') == file_hash:
                logger.debug(f"文件已索引且未变更: {file_path}")
                return existing['entry_id']
        
        # 创建知识条目
        title = file_path.stem
        category = file_type.lower()
        
        entry_id = self.add_knowledge(
            title=title,
            content=content,
            category=category,
            source=str(file_path),
            metadata={
                'file_hash': file_hash,
                'file_size': len(content),
                'file_type': file_type,
                **(metadata or {})
            }
        )
        
        # 更新文件索引
        self.file_index[str(file_path)] = {
            'entry_id': entry_id,
            'hash': file_hash,
            'indexed_at': datetime.now().isoformat(),
            'file_type': file_type
        }
        self._save_file_index()
        
        logger.info(f"索引文件: {file_path}")
        return entry_id
    
    def get_categories(self) -> List[str]:
        """get所有分类"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT DISTINCT category FROM knowledge_entries WHERE category IS NOT NULL"
            )
            return [row[0] for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict[str, int]:
        """get知识库统计"""
        with sqlite3.connect(self.db_path) as conn:
            kb_count = conn.execute(
                "SELECT COUNT(*) FROM knowledge_entries"
            ).fetchone()[0]
            
            concept_count = conn.execute(
                "SELECT COUNT(*) FROM concepts"
            ).fetchone()[0]
            
            relation_count = conn.execute(
                "SELECT COUNT(*) FROM knowledge_relations"
            ).fetchone()[0]
        
        return {
            'knowledge_entries': kb_count,
            'concepts': concept_count,
            'relations': relation_count,
            'indexed_files': len(self.file_index)
        }

    def export_knowledge(self, output_path: str, format: str = "json"):
        """导出知识库"""
        output_path = Path(output_path)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM knowledge_entries")
            entries = []
            for row in cursor.fetchall():
                entries.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'category': row[3],
                    'source': row[4],
                    'created_at': row[5],
                    'updated_at': row[6],
                    'metadata': json.loads(row[7]) if row[7] else {},
                    'tags': json.loads(row[8]) if row[8] else []
                })
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
        
        logger.info(f"导出知识库到: {output_path}")
        return output_path

# ───────────────────────────────────────────────────────────────
# 模块导出
# ───────────────────────────────────────────────────────────────
__all__ = [
    'KnowledgeEntry',
    'Concept',
    'KnowledgeBase',
]
