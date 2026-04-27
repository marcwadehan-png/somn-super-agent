"""
统一记忆接口 V1.0
================

桥接 NeuralMemorySystem V3 与 SuperNeuralMemory V5 的统一接口。

功能:
- 统一 add_memory/retrieve_memory 接口
- V3/V5 双系统协调
- 类型自动转换

版本: v1.0.0
创建: 2026-04-23
"""

from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum

from .memory_types import MemoryTier, MemoryType, MemoryStatus


@dataclass
class UnifiedMemoryEntry:
    """统一记忆条目"""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    tier: MemoryTier = MemoryTier.WORKING
    memory_type: MemoryType = MemoryType.EPISODIC
    status: MemoryStatus = MemoryStatus.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    access_count: int = 0
    importance: float = 0.5


@dataclass
class UnifiedMemoryQuery:
    """统一记忆查询"""
    query_text: str
    query_embedding: Optional[List[float]] = None
    top_k: int = 10
    tier_filter: Optional[MemoryTier] = None
    type_filter: Optional[MemoryType] = None
    metadata_filter: Optional[Dict[str, Any]] = None


@dataclass
class UnifiedMemoryResult:
    """统一记忆结果"""
    entries: List[UnifiedMemoryEntry]
    total_count: int
    query_time_ms: float
    source: str  # "v3", "v5", or "merged"


class UnifiedMemoryInterface:
    """
    统一记忆接口
    
    协调 V3 NeuralMemorySystem 和 V5 SuperNeuralMemory，
    提供统一的记忆存取接口。
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._v3_system = None
        self._v5_system = None
        self._initialized = False
    
    async def initialize(self):
        """初始化双系统"""
        if self._initialized:
            return
        
        try:
            # 初始化 V3 系统
            from .neural_memory_system_v3 import NeuralMemorySystemV3
            self._v3_system = NeuralMemorySystemV3(self.config.get('v3_config'))
            logger.info("V3 记忆系统初始化成功")
        except Exception as e:
            logger.warning(f"V3 系统初始化失败: {e}")
            self._v3_system = None
        
        try:
            # 初始化 V5 系统
            from ..intelligence.engines._super_neural_memory import get_super_memory
            self._v5_system = get_super_memory()
            logger.info("V5 超级记忆系统初始化成功")
        except Exception as e:
            logger.warning(f"V5 系统初始化失败: {e}")
            self._v5_system = None
        
        self._initialized = True
    
    async def add_memory(
        self,
        content: str,
        tier: MemoryTier = MemoryTier.WORKING,
        memory_type: MemoryType = MemoryType.EPISODIC,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            tier: 记忆层级
            memory_type: 记忆类型
            metadata: 元数据
            
        Returns:
            记忆ID
        """
        await self.initialize()
        
        # 根据层级选择目标系统
        if tier in (MemoryTier.ETERNAL, MemoryTier.ARCHIVED, MemoryTier.LONG_TERM):
            # 长期记忆 -> V5
            if self._v5_system:
                return await self._add_to_v5(content, tier, metadata)
        
        # 工作/情景记忆 -> V3
        if self._v3_system:
            return await self._add_to_v3(content, tier, memory_type, metadata)
        
        raise RuntimeError("无可用的记忆系统")
    
    async def _add_to_v3(
        self,
        content: str,
        tier: MemoryTier,
        memory_type: MemoryType,
        metadata: Optional[Dict[str, Any]]
    ) -> str:
        """添加到 V3 系统"""
        # 转换类型
        tier_map = {
            MemoryTier.HOT: "hot",
            MemoryTier.WARM: "warm",
            MemoryTier.COLD: "cold",
            MemoryTier.WORKING: "working",
            MemoryTier.EPISODIC: "episodic",
        }
        v3_tier = tier_map.get(tier, "working")
        
        result = await self._v3_system.add_memory(
            content=content,
            tier=v3_tier,
            memory_type=memory_type.value,
            metadata=metadata or {}
        )
        return result.get('memory_id', '')
    
    async def _add_to_v5(
        self,
        content: str,
        tier: MemoryTier,
        metadata: Optional[Dict[str, Any]]
    ) -> str:
        """添加到 V5 系统"""
        from ..intelligence.engines._super_neural_memory import MemoryEntry, MemorySource
        
        entry = MemoryEntry(
            content=content,
            source=MemorySource.SYSTEM,
            metadata=metadata or {}
        )
        
        if tier == MemoryTier.ETERNAL:
            entry.metadata['eternal'] = True
        
        return await self._v5_system.add_memory(entry)
    
    async def retrieve_memory(
        self,
        query: Union[str, UnifiedMemoryQuery]
    ) -> UnifiedMemoryResult:
        """
        检索记忆
        
        Args:
            query: 查询文本或查询对象
            
        Returns:
            检索结果
        """
        await self.initialize()
        
        import time
        start_time = time.time()
        
        # 统一查询格式
        if isinstance(query, str):
            unified_query = UnifiedMemoryQuery(query_text=query)
        else:
            unified_query = query
        
        results = []
        source = "merged"
        
        # V3 检索
        if self._v3_system and not unified_query.tier_filter:
            v3_results = await self._retrieve_from_v3(unified_query)
            results.extend(v3_results)
        elif self._v3_system and unified_query.tier_filter in (
            MemoryTier.HOT, MemoryTier.WARM, MemoryTier.COLD,
            MemoryTier.WORKING, MemoryTier.EPISODIC
        ):
            v3_results = await self._retrieve_from_v3(unified_query)
            results.extend(v3_results)
        
        # V5 检索（长期记忆）
        if self._v5_system and unified_query.tier_filter in (
            MemoryTier.ETERNAL, MemoryTier.ARCHIVED, MemoryTier.LONG_TERM,
            None
        ):
            v5_results = await self._retrieve_from_v5(unified_query)
            results.extend(v5_results)
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            if r.id not in seen:
                seen.add(r.id)
                unique_results.append(r)
        
        # 排序
        unique_results.sort(key=lambda x: x.importance, reverse=True)
        unique_results = unique_results[:unified_query.top_k]
        
        query_time = (time.time() - start_time) * 1000
        
        return UnifiedMemoryResult(
            entries=unique_results,
            total_count=len(unique_results),
            query_time_ms=query_time,
            source=source
        )
    
    async def _retrieve_from_v3(self, query: UnifiedMemoryQuery) -> List[UnifiedMemoryEntry]:
        """从 V3 系统检索"""
        try:
            results = await self._v3_system.retrieve_memory(
                query_text=query.query_text,
                top_k=query.top_k
            )
            
            entries = []
            for r in results:
                entries.append(UnifiedMemoryEntry(
                    id=r.get('id', ''),
                    content=r.get('content', ''),
                    metadata=r.get('metadata', {}),
                    tier=MemoryTier.WORKING,
                    memory_type=MemoryType.EPISODIC
                ))
            return entries
        except Exception as e:
            logger.warning(f"V3 检索失败: {e}")
            return []
    
    async def _retrieve_from_v5(self, query: UnifiedMemoryQuery) -> List[UnifiedMemoryEntry]:
        """从 V5 系统检索"""
        try:
            from ..intelligence.engines._super_neural_memory import MemoryQuery
            
            v5_query = MemoryQuery(
                query_text=query.query_text,
                top_k=query.top_k
            )
            
            results = await self._v5_system.query(v5_query)
            
            entries = []
            for r in results:
                entries.append(UnifiedMemoryEntry(
                    id=r.entry_id or '',
                    content=r.content,
                    metadata=r.metadata,
                    tier=MemoryTier.LONG_TERM,
                    memory_type=MemoryType.SEMANTIC
                ))
            return entries
        except Exception as e:
            logger.warning(f"V5 检索失败: {e}")
            return []
    
    async def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        await self.initialize()
        
        stats = {
            'v3_available': self._v3_system is not None,
            'v5_available': self._v5_system is not None,
            'initialized': self._initialized
        }
        
        if self._v3_system:
            try:
                stats['v3_stats'] = await self._v3_system.get_stats()
            except Exception:
                pass  # stats['v3_stats'] = await self._v3_system.get_stats()失败时静默忽略
        
        if self._v5_system:
            try:
                stats['v5_stats'] = self._v5_system.get_stats()
            except Exception:
                pass  # stats['v5_stats'] = self._v5_system.get_stats()失败时静默忽略
        
        return stats


# ─────────────────────────────────────────────────────────────────────────────
# 便捷函数
# ─────────────────────────────────────────────────────────────────────────────

_global_interface: Optional[UnifiedMemoryInterface] = None


async def get_unified_memory() -> UnifiedMemoryInterface:
    """获取全局统一记忆接口"""
    global _global_interface
    if _global_interface is None:
        _global_interface = UnifiedMemoryInterface()
    return _global_interface


__all__ = [
    'UnifiedMemoryEntry',
    'UnifiedMemoryQuery',
    'UnifiedMemoryResult',
    'UnifiedMemoryInterface',
    'get_unified_memory',
]
