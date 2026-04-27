"""
__all__ = [
    'archive',
    'delete',
    'from_dict',
    'generate_memory_id',
    'get_all_tags',
    'get_memory_statistics',
    'get_recent_memories',
    'get_stats',
    'record',
    'retrieve',
    'search',
    'to_dict',
    'update',
]

Memory Engine - 记忆管理引擎
Memory Management Engine

管理记忆的存储、检索和生命周期
"""

import json
import yaml
from pathlib import Path
from src.core.paths import LEARNING_DIR, MEMORY_DIR
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
from loguru import logger

class MemoryType(Enum):
    """记忆类型"""
    EPISODIC = "episodic"      # 情景记忆 - 具体事件和经历
    SEMANTIC = "semantic"      # 语义记忆 - 知识和概念
    PROCEDURAL = "procedural"  # 程序记忆 - 技能和操作
    WORKING = "working"       # 工作记忆 - 当前任务相关

class MemoryStatus(Enum):
    """记忆状态"""
    ACTIVE = "active"         # 活跃
    INACTIVE = "inactive"     # 不活跃
    ARCHIVED = "archived"     # 已归档
    DELETED = "deleted"      # 已删除

@dataclass
class Memory:
    """记忆条目"""
    id: str
    content: str
    memory_type: MemoryType = MemoryType.SEMANTIC
    status: MemoryStatus = MemoryStatus.ACTIVE

    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0
    last_accessed: str = field(default_factory=lambda: datetime.now().isoformat())

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
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
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
            status=MemoryStatus(data.get("status", "active")),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            access_count=data.get("access_count", 0),
            last_accessed=data.get("last_accessed", datetime.now().isoformat()),
            tags=data.get("tags", []),
            context=data.get("context", {}),
            source=data.get("source", ""),
            confidence=data.get("confidence", 0.8),
            importance=data.get("importance", 0.5),
            relevance_scores=data.get("relevance_scores", {}),
        )

class MemoryEngine:
    """
    神经记忆系统 - 记忆管理引擎

    核心功能:
    1. 记忆存储 - 保存记忆条目到YAML文件
    2. 记忆检索 - 按类型/标签/内容检索
    3. 记忆更新 - 更新记忆内容和状态
    4. 记忆删除 - 软删除/归档记忆
    5. 记忆统计 - 记忆使用统计
    """

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else LEARNING_DIR
        self.memory_path = self.base_path / "memory"
        self.findings_path = self.base_path / "findings"

        # 创建必要的目录
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.findings_path.mkdir(parents=True, exist_ok=True)

        # 记忆缓存
        self._memory_cache: Dict[str, Memory] = {}
        self._cache_loaded = False

        # 记忆类型mapping
        self.memory_types = {
            "finding": "finding",
            "value": "value",
            "dimension": "dimension",
            "strategy": "strategy",
            "validation": "validation",
            "feedback": "feedback",
            "method": "method",
            "failure": "failure"
        }

        logger.info(f"MemoryEngine initialized at {self.base_path}")

    def generate_memory_id(self) -> str:
        """generate记忆ID"""
        now = datetime.now()
        date_str = now.strftime("%Y_%m_%d")

        # 查找当日已有记忆数量
        today_memories = list(self.memory_path.glob(f"MEM_{date_str}_*.yaml"))
        sequence = len(today_memories) + 1

        return f"MEM_{date_str}_{sequence:03d}"

    def _load_memory_file(self, memory_id: str) -> Optional[Memory]:
        """从文件加载记忆"""
        file_path = self.memory_path / f"{memory_id}.yaml"
        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data:
                    return Memory.from_dict(data)
        except Exception as e:
            logger.warning(f"Failed to load memory {memory_id}: {e}")

        return None

    def _save_memory_file(self, memory: Memory) -> bool:
        """保存记忆到文件"""
        file_path = self.memory_path / f"{memory.id}.yaml"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(memory.to_dict(), f, allow_unicode=True, default_flow_style=False)
            # 更新缓存
            self._memory_cache[memory.id] = memory
            return True
        except Exception as e:
            logger.error(f"Failed to save memory {memory.id}: {e}")
            return False

    def record(self, content: str, memory_type: str = "general",
               tags: List[str] = None, context: Dict = None,
               source: str = "", confidence: float = 0.8,
               importance: float = 0.5) -> str:
        """
        记录新记忆

        Args:
            content: 记忆内容
            memory_type: 记忆类型
            tags: 标签列表
            context: 上下文信息
            source: 来源
            confidence: 置信度
            importance: 重要性

        Returns:
            记忆ID
        """
        memory_id = self.generate_memory_id()

        memory = Memory(
            id=memory_id,
            content=content,
            memory_type=MemoryType.SEMANTIC,
            status=MemoryStatus.ACTIVE,
            tags=tags or [],
            context=context or {},
            source=source,
            confidence=confidence,
            importance=importance,
        )

        self._save_memory_file(memory)
        logger.info(f"Recorded memory: {memory_id}")

        return memory_id

    def retrieve(self, memory_id: str, max_retries: int = 2) -> Optional[Memory]:
        """
        检索记忆 [v10.1 重试优化]

        Args:
            memory_id: 记忆ID
            max_retries: 最大重试次数（针对I/O错误）

        Returns:
            Memory对象或None
        """
        import time as _time
        from src.utils.retry_utils import get_circuit_breaker

        cb = get_circuit_breaker(f"memory-{memory_id[:8]}", failure_threshold=3, recovery_timeout=60.0)
        last_error: Optional[Exception] = None

        # 先查缓存（不走I/O，不需要重试）
        if memory_id in self._memory_cache:
            memory = self._memory_cache[memory_id]
            memory.access_count += 1
            memory.last_accessed = datetime.now().isoformat()
            return memory

        # 从文件加载（I/O操作，可能失败）
        for _attempt in range(1, max_retries + 1):
            if not cb.is_available():
                logger.warning(f"[记忆-{memory_id[:8]}] 熔断器 OPEN，跳过检索")
                return None

            try:
                memory = self._load_memory_file(memory_id)
                if memory:
                    self._memory_cache[memory_id] = memory
                    memory.access_count += 1
                    memory.last_accessed = datetime.now().isoformat()
                    self._save_memory_file(memory)
                    cb.record_success()
                return memory
            except Exception as e:
                last_error = e
                cb.record_failure()
                if _attempt < max_retries:
                    _delay = 0.5 * (2 ** (_attempt - 1))
                    logger.warning(
                        f"[记忆-{memory_id[:8]}] 第{_attempt}次读取失败: {e}，"
                        f"{_delay:.1f}s后重试..."
                    )
                    _time.sleep(_delay)
                else:
                    logger.warning(f"[记忆-{memory_id[:8]}] 检索失败（已达最大重试）: {e}")

        return None

    def search(self, query: str = None, memory_type: str = None,
               tags: List[str] = None, limit: int = 10) -> List[Memory]:
        """
        搜索记忆 [v10.1 重试优化]

        Args:
            query: 搜索关键词
            memory_type: 记忆类型过滤
            tags: 标签过滤
            limit: 返回数量限制

        Returns:
            Memory列表（失败时返回空列表，不阻塞主流程）
        """
        import time as _time
        from src.utils.retry_utils import get_circuit_breaker

        cb = get_circuit_breaker("memory-search", failure_threshold=5, recovery_timeout=30.0)

        for _attempt in range(1, 3):
            if not cb.is_available():
                logger.warning("[记忆搜索] 熔断器 OPEN，返回空结果")
                return []

            try:
                return self._search_impl(query, memory_type, tags, limit)
            except Exception as e:
                cb.record_failure()
                if _attempt < 2:
                    _delay = 1.0 * (2 ** (_attempt - 1))
                    logger.warning(f"[记忆搜索] 第{_attempt}次失败: {e}，{_delay:.1f}s后重试...")
                    _time.sleep(_delay)
                else:
                    logger.warning(f"[记忆搜索] 失败（已达最大重试）: {e}")

        return []

    def _search_impl(self, query, memory_type, tags, limit) -> List[Memory]:
        """搜索的实际实现（无重试，由 search() 调用）"""
        results = []

        for file_path in self.memory_path.glob("*.yaml"):
            try:
                memory = self._load_memory_file(file_path.stem)
            except Exception:
                continue
            if not memory:
                continue

            # 类型过滤
            if memory_type and memory.memory_type.value != memory_type:
                continue

            # 标签过滤
            if tags and not any(tag in memory.tags for tag in tags):
                continue

            # 关键词过滤
            if query and query.lower() not in memory.content.lower():
                continue

            results.append(memory)

        # 按访问频率和重要性排序
        results.sort(key=lambda m: (m.access_count * m.importance), reverse=True)

        return results[:limit]

    def update(self, memory_id: str, **kwargs) -> bool:
        """
        更新记忆

        Args:
            memory_id: 记忆ID
            **kwargs: 要更新的字段

        Returns:
            是否成功
        """
        memory = self.retrieve(memory_id)
        if not memory:
            return False

        # 更新字段
        for key, value in kwargs.items():
            if hasattr(memory, key):
                setattr(memory, key, value)

        memory.updated_at = datetime.now().isoformat()

        return self._save_memory_file(memory)

    def delete(self, memory_id: str, soft: bool = True) -> bool:
        """
        删除记忆

        Args:
            memory_id: 记忆ID
            soft: 是否软删除(仅标记状态)

        Returns:
            是否成功
        """
        memory = self.retrieve(memory_id)
        if not memory:
            return False

        if soft:
            memory.status = MemoryStatus.DELETED
            return self._save_memory_file(memory)
        else:
            # 硬删除
            file_path = self.memory_path / f"{memory_id}.yaml"
            try:
                file_path.unlink()
                self._memory_cache.pop(memory_id, None)
                return True
            except Exception as e:
                logger.error(f"Failed to delete memory {memory_id}: {e}")
                return False

    def archive(self, memory_id: str) -> bool:
        """归档记忆"""
        return self.update(memory_id, status=MemoryStatus.ARCHIVED)

    def get_stats(self) -> Dict:
        """get记忆统计"""
        return self.get_memory_statistics()

    def get_memory_statistics(self) -> Dict:
        """get记忆统计（别名，兼容neural_system调用）"""
        total = 0
        by_type = {}
        by_status = {}

        for file_path in self.memory_path.glob("*.yaml"):
            memory = self._load_memory_file(file_path.stem)
            if not memory:
                continue

            total += 1

            # 按类型统计
            type_key = memory.memory_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1

            # 按状态统计
            status_key = memory.status.value
            by_status[status_key] = by_status.get(status_key, 0) + 1

        return {
            "total_memories": total,
            "by_type": by_type,
            "by_status": by_status,
            "cache_size": len(self._memory_cache)
        }

    def get_recent_memories(self, limit: int = 10) -> List[Memory]:
        """get最近的记忆"""
        memories = []
        for file_path in sorted(self.memory_path.glob("*.yaml"),
                                key=lambda p: p.stat().st_mtime,
                                reverse=True)[:limit]:
            memory = self._load_memory_file(file_path.stem)
            if memory:
                memories.append(memory)
        return memories

    def get_all_tags(self) -> List[str]:
        """get所有标签"""
        tags = set()
        for file_path in self.memory_path.glob("*.yaml"):
            memory = self._load_memory_file(file_path.stem)
            if memory and memory.tags:
                tags.update(memory.tags)
        return sorted(list(tags))
