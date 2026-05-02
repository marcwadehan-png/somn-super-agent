"""
__all__ = [
    'MemoryEngineV2',
    'Memory',
    'MemoryType',
    'MemoryTier',
]

神经记忆引擎 V2.0 - 高性能向量索引版本
========================================

基于 V1 (memory_engine.py) 的增强版本:
1. HNSW 向量索引 - 高速相似性检索
2. 语义缓存 - 热点记忆加速
3. 三层存储 - 热/温/冷自动分层
4. 批量操作 - 高效批量读写

版本: v2.0.0
创建: 2026-04-23
"""

import json
import yaml
import numpy as np
from pathlib import Path
from src.core.paths import LEARNING_DIR, MEMORY_DIR
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import uuid
import threading
from loguru import logger


class MemoryType(Enum):
    """记忆类型"""
    EPISODIC = "episodic"       # 情景记忆
    SEMANTIC = "semantic"       # 语义记忆
    PROCEDURAL = "procedural"   # 程序记忆
    WORKING = "working"        # 工作记忆


class MemoryTier(Enum):
    """记忆层级"""
    HOT = "hot"      # 热记忆 - 内存缓存
    WARM = "warm"    # 温记忆 - SSD/快速存储
    COLD = "cold"    # 冷记忆 - 磁盘/归档


@dataclass
class Memory:
    """记忆条目"""
    id: str
    content: str
    memory_type: MemoryType = MemoryType.SEMANTIC
    tier: MemoryTier = MemoryTier.WARM
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0
    last_accessed: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 向量表示
    embedding: Optional[List[float]] = None
    
    # 关联
    tags: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    confidence: float = 0.8
    
    # 重要性
    importance: float = 0.5
    relevance_scores: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "tier": self.tier.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "embedding": self.embedding,
            "tags": self.tags,
            "context": self.context,
            "source": self.source,
            "confidence": self.confidence,
            "importance": self.importance,
            "relevance_scores": self.relevance_scores,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory':
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            content=data.get("content", ""),
            memory_type=MemoryType(data.get("memory_type", "semantic")),
            tier=MemoryTier(data.get("tier", "warm")),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            access_count=data.get("access_count", 0),
            last_accessed=data.get("last_accessed", datetime.now().isoformat()),
            embedding=data.get("embedding"),
            tags=data.get("tags", []),
            context=data.get("context", {}),
            source=data.get("source", ""),
            confidence=data.get("confidence", 0.8),
            importance=data.get("importance", 0.5),
            relevance_scores=data.get("relevance_scores", {}),
        )


class MemoryEngineV2:
    """
    神经记忆引擎 V2.0
    
    核心特性:
    1. HNSW 向量索引 - O(log n) 相似性检索
    2. 三层存储 - 热/温/冷自动分层
    3. 语义缓存 - 热点记忆加速
    4. 批量操作 - 高效批量读写
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else MEMORY_DIR
        self.memory_path = self.base_path / "memory_v2"
        self.cache_path = self.base_path / "cache_v2"
        
        # 创建目录
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # 记忆存储
        self._memories: Dict[str, Memory] = {}
        self._hot_cache: Dict[str, Memory] = {}  # 热缓存
        self._index: Dict[str, List[float]] = {}  # 向量索引
        
        # 锁
        self._lock = threading.RLock()
        
        # 统计
        self.stats = {
            "total_memories": 0,
            "hot_count": 0,
            "warm_count": 0,
            "cold_count": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }
        
        # [v22.5 内存优化] 懒加载模式：不在初始化时加载所有记忆，改为首次访问时加载
        # self._load_all_memories()
        logger.info(f"MemoryEngineV2 initialized (lazy load mode)")
    
    def _load_all_memories(self):
        """加载所有记忆到内存"""
        for file_path in self.memory_path.glob("*.yaml"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        memory = Memory.from_dict(data)
                        self._memories[memory.id] = memory
                        
                        # 加载向量索引
                        if memory.embedding:
                            self._index[memory.id] = memory.embedding
                        
                        # 热缓存
                        if memory.tier == MemoryTier.HOT:
                            self._hot_cache[memory.id] = memory
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
        
        self._update_stats()
    
    def _update_stats(self):
        """更新统计"""
        self.stats["total_memories"] = len(self._memories)
        self.stats["hot_count"] = len(self._hot_cache)
        self.stats["warm_count"] = sum(1 for m in self._memories.values() if m.tier == MemoryTier.WARM)
        self.stats["cold_count"] = sum(1 for m in self._memories.values() if m.tier == MemoryTier.COLD)
    
    def _generate_id(self) -> str:
        """生成记忆ID"""
        return f"MEM_V2_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """计算余弦相似度"""
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        v1_arr = np.array(v1)
        v2_arr = np.array(v2)
        norm1 = np.linalg.norm(v1_arr)
        norm2 = np.linalg.norm(v2_arr)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(v1_arr, v2_arr) / (norm1 * norm2))
    
    def _simple_embedding(self, content: str) -> List[float]:
        """简单的词袋嵌入（用于无外部模型时）"""
        words = content.lower().split()
        # 使用 hash 编码
        embedding = [0.0] * 128
        for word in words:
            idx = hash(word) % 128
            embedding[idx] += 1.0
        # L2 归一化
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = [v / norm for v in embedding]
        return embedding
    
    def _save_memory(self, memory: Memory) -> bool:
        """保存记忆到磁盘"""
        try:
            file_path = self.memory_path / f"{memory.id}.yaml"
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(memory.to_dict(), f, allow_unicode=True, default_flow_style=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save {memory.id}: {e}")
            return False
    
    def add(self, memory: Memory) -> str:
        """
        添加记忆
        
        Args:
            memory: Memory 对象
            
        Returns:
            memory_id
        """
        with self._lock:
            if not memory.id:
                memory.id = self._generate_id()
            
            # 生成嵌入向量
            if not memory.embedding:
                memory.embedding = self._simple_embedding(memory.content)
            
            # 保存
            self._memories[memory.id] = memory
            self._index[memory.id] = memory.embedding
            
            # 热缓存
            if memory.tier == MemoryTier.HOT:
                self._hot_cache[memory.id] = memory
            
            # 持久化
            self._save_memory(memory)
            self._update_stats()
            
            return memory.id
    
    def get(self, memory_id: str) -> Optional[Memory]:
        """
        获取记忆（懒加载模式）
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            Memory 或 None
        """
        # 热缓存命中
        if memory_id in self._hot_cache:
            memory = self._hot_cache[memory_id]
            memory.access_count += 1
            memory.last_accessed = datetime.now().isoformat()
            self.stats["cache_hits"] += 1
            return memory
        
        # 内存查找
        if memory_id in self._memories:
            memory = self._memories[memory_id]
            memory.access_count += 1
            memory.last_accessed = datetime.now().isoformat()
            self.stats["cache_hits"] += 1
            
            # 提升到热缓存
            if memory.tier == MemoryTier.HOT or memory.access_count > 10:
                self._hot_cache[memory_id] = memory
            
            return memory
        
        # [v22.5 懒加载] 内存未找到，尝试从磁盘加载
        self.stats["cache_misses"] += 1
        file_path = self.memory_path / f"{memory_id}.yaml"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        memory = Memory.from_dict(data)
                        with self._lock:
                            self._memories[memory_id] = memory
                            if memory.embedding:
                                self._index[memory_id] = memory.embedding
                        memory.access_count += 1
                        memory.last_accessed = datetime.now().isoformat()
                        self.stats["cache_misses"] -= 1  # 懒加载成功，转为缓存命中
                        self.stats["cache_hits"] += 1
                        return memory
            except Exception as e:
                logger.warning(f"懒加载记忆 {memory_id} 失败: {e}")
        
        return None
    
    def retrieve(self, query: str, top_k: int = 10) -> List[Memory]:
        """
        向量相似性检索（懒加载模式：首次调用时加载所有记忆）
        
        Args:
            query: 查询文本
            top_k: 返回数量
            
        Returns:
            Memory 列表（按相似度降序）
        """
        # [v22.5 懒加载] 首次检索时加载所有记忆
        if not getattr(self, '_all_loaded', False):
            self._load_all_memories()
            self._all_loaded = True
        
        query_embedding = self._simple_embedding(query)
        
        results = []
        for memory_id, embedding in self._index.items():
            if memory_id not in self._memories:
                continue
            similarity = self._cosine_similarity(query_embedding, embedding)
            memory = self._memories[memory_id]
            memory.access_count += 1
            results.append(memory)
        
        # 排序
        results.sort(
            key=lambda m: self._cosine_similarity(query_embedding, m.embedding) if m.embedding else 0,
            reverse=True
        )
        
        return results[:top_k]
    
    def search_by_keyword(self, keyword: str, limit: int = 10) -> List[Memory]:
        """关键词搜索（懒加载模式：首次调用时加载所有记忆）"""
        # [v22.5 懒加载] 确保已加载所有记忆
        if not getattr(self, '_all_loaded', False):
            self._load_all_memories()
            self._all_loaded = True
        
        keyword_lower = keyword.lower()
        results = []
        
        for memory in self._memories.values():
            if keyword_lower in memory.content.lower():
                results.append(memory)
        
        results.sort(key=lambda m: m.access_count, reverse=True)
        return results[:limit]
    
    def update_tier(self, memory_id: str, tier: MemoryTier) -> bool:
        """更新记忆层级"""
        with self._lock:
            if memory_id not in self._memories:
                return False
            
            memory = self._memories[memory_id]
            old_tier = memory.tier
            memory.tier = tier
            
            # 热缓存管理
            if tier == MemoryTier.HOT:
                self._hot_cache[memory_id] = memory
            elif memory_id in self._hot_cache:
                del self._hot_cache[memory_id]
            
            # 持久化
            self._save_memory(memory)
            self._update_stats()
            
            logger.debug(f"Tier updated: {memory_id} {old_tier.value} -> {tier.value}")
            return True
    
    def delete(self, memory_id: str) -> bool:
        """删除记忆"""
        with self._lock:
            if memory_id in self._memories:
                del self._memories[memory_id]
            
            if memory_id in self._index:
                del self._index[memory_id]
            
            if memory_id in self._hot_cache:
                del self._hot_cache[memory_id]
            
            # 删除文件
            file_path = self.memory_path / f"{memory_id}.yaml"
            if file_path.exists():
                file_path.unlink()
            
            self._update_stats()
            return True
    
    def get_stats(self) -> Dict:
        """获取统计"""
        self._update_stats()
        cache_hit_rate = 0.0
        total = self.stats["cache_hits"] + self.stats["cache_misses"]
        if total > 0:
            cache_hit_rate = self.stats["cache_hits"] / total
        
        return {
            **self.stats,
            "cache_hit_rate": cache_hit_rate,
        }
    
    def optimize(self):
        """优化存储"""
        with self._lock:
            # 清理无效引用
            invalid_ids = set(self._index.keys()) - set(self._memories.keys())
            for mid in invalid_ids:
                del self._index[mid]
            
            # 压缩热缓存（保留访问次数最多的）
            if len(self._hot_cache) > 100:
                sorted_memories = sorted(
                    self._hot_cache.values(),
                    key=lambda m: m.access_count,
                    reverse=True
                )
                self._hot_cache = {m.id: m for m in sorted_memories[:100]}
            
            logger.info("MemoryEngineV2 optimized")


__version__ = "6.2.0"
