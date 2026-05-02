"""
NeuralMemory — 统一记忆接口 S1.0
==================================

[NeuralMemory 架构定位]
本接口是 NeuralMemory（三层神经记忆架构）的核心管理工具——
即记忆仓库（藏书阁 ImperialLibrary）的管理工具。

桥接 NeuralMemorySystem V3 与 SuperNeuralMemory V5 的统一接口，
并深度集成藏书阁（ImperialLibrary）作为记忆仓库。

功能:
- 统一 add_memory/retrieve_memory 接口
- V3/V5 双系统协调
- 类型自动转换
- [v2.0] 藏书阁作为统一记忆仓库（CellRecord 格式）
- [v2.0] MemoryTier ↔ MemoryGrade 自动映射
- [v2.0] 知识库(DomainNexus) 桥接查询

版本: S1.0
更新: 2026-04-29
"""

import logging
import threading
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum

from .memory_types import MemoryTier, MemoryType, MemoryStatus

logger = logging.getLogger("Somn.NeuralMemory.UnifiedInterface")

# v7.1 FastBoot: 类型导入缓存 — 避免每次 add_memory 都做 __import__
_cached_library_types = None  # MemoryGrade, MemorySource, MemoryCategory
_cached_tier_to_grade = None  # tier_to_grade 函数


@dataclass
class UnifiedMemoryEntry:
    """统一记忆条目
    
    [v2.0] 增加藏书阁深度绑定：
    - grade: 藏书阁分级（甲乙丙丁）
    - cell_id: 藏书阁 CellRecord ID（如果已入库）
    - source_system: 来源系统标记
    """
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
    # v2.0: 藏书阁绑定字段
    grade: Optional[str] = None           # 甲/乙/丙/丁（自动从 tier 映射）
    cell_id: Optional[str] = None         # 藏书阁格位ID
    wing: Optional[str] = None            # 分馆
    shelf: Optional[str] = None           # 书架
    associated_claw: Optional[str] = None  # 关联Claw贤者
    cross_references: List[str] = field(default_factory=list)  # 跨域引用
    source_system: str = "unified"        # v3 / v5 / library / knowledge


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
    NeuralMemory 统一记忆接口 V2.0
    
    协调 V3 NeuralMemorySystem、V5 SuperNeuralMemory 和 藏书阁(ImperialLibrary)，
    提供 NeuralMemory（三层神经记忆架构）的统一记忆存取接口。
    
    [v2.0 架构定位]
    本接口是 NeuralMemory 的核心管理工具——即记忆仓库（藏书阁）的管理工具：
    - add_memory → 入库（通过学习系统制度）
    - retrieve_memory → 出库查询
    - 知识库桥接 → DomainNexus 查询通道
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._v3_system = None
        self._v5_system = None
        self._library = None          # v2.0: 藏书阁实例
        self._knowledge_bridge = None  # v2.0: 知识库桥接器
        self._initialized = False
    
    def _get_library(self):
        """延迟加载藏书阁 — 支持多种导入路径"""
        if self._library is None:
            # 路径1: 相对导入 (src包内)
            try:
                from ..intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
                self._library = ImperialLibrary()
                return self._library
            except (ImportError, AttributeError):
                pass
            # 路径2: 绝对导入
            try:
                from src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
                self._library = ImperialLibrary()
                return self._library
            except ImportError:
                pass
            # 路径3: sys.path 查找
            try:
                import importlib
                mod = importlib.import_module("intelligence.dispatcher.wisdom_dispatch._imperial_library")
                self._library = mod.ImperialLibrary()
                return self._library
            except Exception:
                pass
        return self._library
    
    def _get_knowledge_bridge(self):
        """延迟加载知识库桥接器 — 支持多种导入路径"""
        if self._knowledge_bridge is None:
            # 路径1: 相对导入 (src包内)
            try:
                from ..intelligence.dispatcher.wisdom_dispatch._library_knowledge_bridge import LibraryKnowledgeBridge
                self._knowledge_bridge = LibraryKnowledgeBridge()
                return self._knowledge_bridge
            except (ImportError, AttributeError):
                pass
            # 路径2: 绝对导入
            try:
                from src.intelligence.dispatcher.wisdom_dispatch._library_knowledge_bridge import LibraryKnowledgeBridge
                self._knowledge_bridge = LibraryKnowledgeBridge()
                return self._knowledge_bridge
            except ImportError:
                pass
            # 路径3: DomainNexus直接桥接（最可靠的路径）
            try:
                from knowledge_cells.domain_nexus import get_nexus
                self._knowledge_bridge = _DomainNexusBridgeAdapter(get_nexus())
                return self._knowledge_bridge
            except ImportError:
                pass
        return self._knowledge_bridge
    
    async def initialize(self):
        """初始化三系统（V3 + V5 + 藏书阁）"""
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
        
        # v2.0: 初始化藏书阁
        lib = self._get_library()
        if lib:
            logger.info("藏书阁(记忆仓库)初始化成功")
        
        kb = self._get_knowledge_bridge()
        if kb:
            logger.info("知识库桥接器(DomainNexus)初始化成功")
        
        self._initialized = True
    
    async def add_memory(
        self,
        content: str,
        tier: MemoryTier = MemoryTier.WORKING,
        memory_type: MemoryType = MemoryType.EPISODIC,
        metadata: Optional[Dict[str, Any]] = None,
        operator: str = "",          # v2.0: 操作者（用于藏书阁权限）
        submit_to_library: bool = True,  # v2.0: 是否同时入库藏书阁
    ) -> str:
        """
        添加记忆
        
        [v2.0] 执行流程：
        1. 根据 tier 写入 V3 或 V5 神经记忆系统（书架）
        2. 若 submit_to_library=True，同时提交到藏书阁（记忆仓库）
        3. 自动映射 tier → grade，写入 CellRecord
        
        Args:
            content: 记忆内容
            tier: 记忆层级（书架位置）
            memory_type: 记忆类型
            metadata: 元数据
            operator: 操作者名称（Claw贤者）
            submit_to_library: 是否入库藏书阁
            
        Returns:
            记忆ID（若入库藏书阁则返回 cell_id）
        """
        await self.initialize()
        metadata = metadata or {}
        
        # Step 1: 写入神经记忆系统（V3/V5）
        memory_id = ""
        if tier in (MemoryTier.ETERNAL, MemoryTier.ARCHIVED, MemoryTier.LONG_TERM):
            if self._v5_system:
                memory_id = await self._add_to_v5(content, tier, metadata)
        else:
            if self._v3_system:
                memory_id = await self._add_to_v3(content, tier, memory_type, metadata)
        
        # Step 2: [v2.0] 同时入库藏书阁（记忆仓库）
        if submit_to_library:
            lib = self._get_library()
            if lib:
                try:
                    # v7.1 FastBoot: 缓存类型导入 — 首次导入后复用
                    global _cached_library_types, _cached_tier_to_grade
                    
                    if _cached_library_types is None:
                        # 多路径尝试导入藏书阁类型
                        for import_func in [
                            lambda: __import__('src.intelligence.dispatcher.wisdom_dispatch._imperial_library',
                                                fromlist=['MemoryGrade', 'MemorySource', 'MemoryCategory']),
                            lambda: __import__('smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library',
                                                fromlist=['MemoryGrade', 'MemorySource', 'MemoryCategory']),
                        ]:
                            try:
                                mod = import_func()
                                _cached_library_types = (
                                    mod.MemoryGrade, mod.MemorySource, mod.MemoryCategory
                                )
                                break
                            except Exception:
                                continue
                        if _cached_library_types is None:
                            _cached_library_types = (None, None, None)
                    
                    if _cached_tier_to_grade is None:
                        for import_func2 in [
                            lambda: __import__('src.neural_memory.memory_types', fromlist=['tier_to_grade']),
                            lambda: __import__('smart_office_assistant.src.neural_memory.memory_types', fromlist=['tier_to_grade']),
                            lambda: __import__('neural_memory.memory_types', fromlist=['tier_to_grade']),
                        ]:
                            try:
                                mod2 = import_func2()
                                _cached_tier_to_grade = mod2.tier_to_grade
                                break
                            except Exception:
                                continue
                    
                    MemoryGrade, MemorySource, MemoryCategory = _cached_library_types
                    tier_to_grade = _cached_tier_to_grade

                    if not all([MemoryGrade, MemorySource, MemoryCategory, tier_to_grade]):
                        logger.debug("[统一接口] 藏书阁类型导入不完整，跳过入库")
                    else:
                        # tier → grade 自动映射
                        grade_str = tier_to_grade(tier)
                        grade = MemoryGrade(grade_str)

                        # 内容分类映射
                        cat_map = {
                            MemoryType.EPISODIC: MemoryCategory.RESULT,
                            MemoryType.SEMANTIC: MemoryCategory.CONCLUSION,
                            MemoryType.PROCEDURAL: MemoryCategory.STRATEGY,
                        }
                        category = cat_map.get(memory_type, MemoryCategory.RESULT)

                        # 提交到藏书阁
                        cell_id = lib.submit_cell(
                            title=metadata.get("title", content[:30]),
                            content=content,
                            source=MemorySource.SYSTEM,
                            category=category,
                            grade=grade,
                            operator=operator or "统一记忆接口",
                            tags=metadata.get("tags", []),
                            metadata=metadata,
                        )
                        logger.info(f"[统一接口] 记忆已入库藏书阁: {cell_id}")
                        return cell_id  # 优先返回藏书阁ID
                except Exception as e:
                    logger.warning(f"[统一接口] 藏书阁入库失败（继续）: {e}")
        
        if not memory_id:
            raise RuntimeError("无可用的记忆系统，且藏书阁入库失败")
        return memory_id
    
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
        query: Union[str, UnifiedMemoryQuery],
        include_library: bool = True,   # v2.0: 是否查询藏书阁
        include_knowledge: bool = False,  # v2.0: 是否查询知识库
    ) -> UnifiedMemoryResult:
        """
        检索记忆
        
        [v2.0] 执行流程：
        1. V3/V5 神经记忆检索
        2. 藏书阁 CellRecord 查询（若 include_library）
        3. 知识库 DomainNexus 查询（若 include_knowledge）
        4. 合并去重，统一返回 UnifiedMemoryEntry 列表
        
        Args:
            query: 查询文本或查询对象
            include_library: 是否查询藏书阁
            include_knowledge: 是否查询知识库
            
        Returns:
            统一检索结果
        """
        await self.initialize()
        
        import time as _time
        start_time = _time.time()
        
        # 统一查询格式
        if isinstance(query, str):
            unified_query = UnifiedMemoryQuery(query_text=query)
        else:
            unified_query = query
        
        results = []
        source = "merged"
        
        # 1. V3/V5 神经记忆检索
        results.extend(await self._retrieve_neural(unified_query))
        
        # 2. [v2.0] 藏书阁检索
        if include_library:
            lib_results = await self._retrieve_from_library(unified_query)
            results.extend(lib_results)
            if lib_results:
                source = "library_merged"
        
        # 3. [v2.0] 知识库(DomainNexus) 检索
        if include_knowledge:
            kb_results = await self._retrieve_from_knowledge(unified_query)
            results.extend(kb_results)
            if kb_results:
                source = "knowledge_merged"
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            if r.id not in seen:
                seen.add(r.id)
                unique_results.append(r)
        
        # 排序：藏书阁记录优先，然后按重要性降序
        unique_results.sort(key=lambda x: (x.source_system == "library", x.importance), reverse=True)
        unique_results = unique_results[:unified_query.top_k]
        
        query_time = (_time.time() - start_time) * 1000
        
        return UnifiedMemoryResult(
            entries=unique_results,
            total_count=len(unique_results),
            query_time_ms=query_time,
            source=source
        )
    
    async def _retrieve_neural(self, query: UnifiedMemoryQuery) -> List[UnifiedMemoryEntry]:
        """V3/V5 神经记忆检索，不足时调用 LLM 增强"""
        results = []
        
        if self._v3_system and not query.tier_filter:
            v3_results = await self._retrieve_from_v3(query)
            results.extend(v3_results)
        elif self._v3_system and query.tier_filter in (
            MemoryTier.HOT, MemoryTier.WARM, MemoryTier.COLD,
            MemoryTier.WORKING, MemoryTier.EPISODIC
        ):
            v3_results = await self._retrieve_from_v3(query)
            results.extend(v3_results)
        
        if self._v5_system and query.tier_filter in (
            MemoryTier.ETERNAL, MemoryTier.ARCHIVED, MemoryTier.LONG_TERM,
            None
        ):
            v5_results = await self._retrieve_from_v5(query)
            results.extend(v5_results)
        
        # [v7.0] 当检索结果不足时，调用 enhance_with_llm 优化查询
        if len(results) < query.top_k // 2:
            try:
                enhanced = enhance_with_llm(
                    prompt=f"请扩展以下查询关键词，生成3个相关搜索词：{query.query_text}",
                    context="NeuralMemory retrieve fallback",
                )
                if enhanced and enhanced != query.query_text[:200]:
                    logger.info(f"[统一接口] LLM增强查询: {enhanced[:100]}")
                    # 使用增强后的文本重新检索 V3（如果可用）
                    if self._v3_system:
                        enhanced_query = UnifiedMemoryQuery(
                            query_text=enhanced,
                            top_k=query.top_k - len(results),
                        )
                        extra = await self._retrieve_from_v3(enhanced_query)
                        results.extend(extra)
            except Exception as e:
                logger.warning(f"[统一接口] LLM增强检索失败（继续使用原始结果）: {e}")
        
        return results
    
    async def _retrieve_from_library(self, query: UnifiedMemoryQuery) -> List[UnifiedMemoryEntry]:
        """[v2.0] 从藏书阁检索"""
        lib = self._get_library()
        if not lib:
            return []
        
        try:
            cells = lib.query_cells(
                keyword=query.query_text,
                limit=query.top_k,
                grade=None,  # 全部分级
            )
            
            entries = []
            from src.neural_memory.memory_types import auto_assign_tier
            for cell in cells:
                
                entries.append(UnifiedMemoryEntry(
                    id=cell.id,
                    content=cell.content,
                    importance=cell.value_score,
                    metadata={
                        "grade": cell.grade.value,
                        "wing": cell.wing.value,
                        "shelf": cell.shelf,
                        "source": cell.source.value,
                        "category": cell.category.value,
                        "access_count": cell.access_count,
                        **cell.metadata,
                    },
                    tier=getattr(cell, 'tier', None) or MemoryTier.WORKING,
                    grade=cell.grade.value,
                    cell_id=cell.id,
                    wing=cell.wing.value,
                    shelf=cell.shelf,
                    associated_claw=cell.associated_claw,
                    cross_references=list(cell.cross_references or []),
                    access_count=cell.access_count,
                    source_system="library",
                ))
            return entries
        except Exception as e:
            logger.warning(f"[统一接口] 藏书阁检索失败: {e}")
            return []
    
    async def _retrieve_from_knowledge(self, query: UnifiedMemoryQuery) -> List[UnifiedMemoryEntry]:
        """[v2.0] 从知识库(DomainNexus)检索"""
        kb = self._get_knowledge_bridge()
        if not kb:
            return []
        
        try:
            results = kb.search_by_content(query.query_text, limit=query.top_k)
            entries = []
            for item in results:
                entries.append(UnifiedMemoryEntry(
                    id=f"kb_{item.get('cell_id', 'unknown')}",
                    content=item.get("content", ""),
                    metadata={"category": item.get("category"), "tags": list(item.get("tags", []))},
                    tier=MemoryTier.EPISODIC,
                    source_system="knowledge",
                    importance=0.6 + (item.get("activation_count", 0) * 0.01),
                ))
            return entries
        except Exception as e:
            logger.warning(f"[统一接口] 知识库检索失败: {e}")
            return []
    
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
        """获取三系统统计信息"""
        await self.initialize()
        
        stats = {
            'v3_available': self._v3_system is not None,
            'v5_available': self._v5_system is not None,
            'library_available': self._library is not None,      # v2.0
            'knowledge_bridge_available': self._knowledge_bridge is not None,  # v2.0
            'initialized': self._initialized
        }
        
        if self._v3_system:
            try:
                stats['v3_stats'] = await self._v3_system.get_stats()
            except Exception as e:
                logger.warning(f"[统一接口] 获取V3统计失败: {e}")
        
        if self._v5_system:
            try:
                stats['v5_stats'] = self._v5_system.get_stats()
            except Exception as e:
                logger.warning(f"[统一接口] 获取V5统计失败: {e}")
        
        # v2.0: 藏书阁统计
        lib = self._get_library()
        if lib:
            try:
                stats['library_stats'] = lib.get_statistics()
            except Exception as e:
                logger.warning(f"[统一接口] 获取藏书阁统计失败: {e}")
        
        # v2.0: 知识库统计
        kb = self._get_knowledge_bridge()
        if kb:
            try:
                stats['knowledge_stats'] = kb.get_stats()
            except Exception as e:
                logger.warning(f"[统一接口] 获取知识库统计失败: {e}")
        
        return stats
    
    async def get_memory(self, memory_id: str) -> Optional[UnifiedMemoryEntry]:
        """
        按ID获取单条记忆
        
        依次查找: V3 → V5 → 藏书阁，返回首个匹配结果。
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            匹配的 UnifiedMemoryEntry，未找到返回 None
        """
        await self.initialize()
        
        # 1. 尝试 V3 系统
        if self._v3_system:
            try:
                results = await self._v3_system.retrieve_memory(query_text=memory_id, top_k=1)
                for r in results:
                    if r.get('id') == memory_id:
                        return UnifiedMemoryEntry(
                            id=r.get('id', ''),
                            content=r.get('content', ''),
                            metadata=r.get('metadata', {}),
                            tier=MemoryTier.WORKING,
                            memory_type=MemoryType.EPISODIC,
                            source_system="v3",
                        )
            except Exception as e:
                logger.warning(f"[统一接口] V3 get_memory 查询失败: {e}")
        
        # 2. 尝试 V5 系统
        if self._v5_system:
            try:
                from ..intelligence.engines._super_neural_memory import MemoryQuery
                v5_query = MemoryQuery(query_text=memory_id, top_k=1)
                v5_results = await self._v5_system.query(v5_query)
                for r in v5_results:
                    if r.entry_id == memory_id:
                        return UnifiedMemoryEntry(
                            id=r.entry_id or '',
                            content=r.content,
                            metadata=r.metadata,
                            tier=MemoryTier.LONG_TERM,
                            memory_type=MemoryType.SEMANTIC,
                            source_system="v5",
                        )
            except Exception as e:
                logger.warning(f"[统一接口] V5 get_memory 查询失败: {e}")
        
        # 3. 尝试藏书阁
        lib = self._get_library()
        if lib:
            try:
                cell = lib.get_cell(memory_id)
                if cell:
                    return UnifiedMemoryEntry(
                        id=cell.id,
                        content=cell.content,
                        importance=cell.value_score,
                        metadata={
                            "grade": cell.grade.value,
                            "wing": cell.wing.value,
                            "shelf": cell.shelf,
                        },
                        tier=getattr(cell, 'tier', None) or MemoryTier.WORKING,
                        grade=cell.grade.value,
                        cell_id=cell.id,
                        wing=cell.wing.value,
                        shelf=cell.shelf,
                        source_system="library",
                    )
            except Exception as e:
                logger.warning(f"[统一接口] 藏书阁 get_memory 查询失败: {e}")
        
        return None
    
    async def delete_memory(self, memory_id: str, reason: str = "") -> Dict[str, Any]:
        """
        按ID删除记忆
        
        尝试从 V3、V5、藏书阁三系统中删除指定记忆。
        
        Args:
            memory_id: 记忆ID
            reason: 删除原因（用于审计）
            
        Returns:
            删除结果 {"deleted_from": [...], "errors": [...]}
        """
        await self.initialize()
        
        deleted_from = []
        errors = []
        
        # 1. 尝试 V3 删除
        if self._v3_system:
            try:
                if hasattr(self._v3_system, 'delete_memory'):
                    await self._v3_system.delete_memory(memory_id)
                    deleted_from.append("v3")
                else:
                    logger.debug(f"[统一接口] V3 系统不支持 delete_memory")
            except Exception as e:
                errors.append(f"v3: {e}")
                logger.warning(f"[统一接口] V3 delete_memory 失败: {e}")
        
        # 2. 尝试 V5 删除
        if self._v5_system:
            try:
                if hasattr(self._v5_system, 'delete_memory'):
                    await self._v5_system.delete_memory(memory_id)
                    deleted_from.append("v5")
                else:
                    logger.debug(f"[统一接口] V5 系统不支持 delete_memory")
            except Exception as e:
                errors.append(f"v5: {e}")
                logger.warning(f"[统一接口] V5 delete_memory 失败: {e}")
        
        # 3. 尝试藏书阁删除
        lib = self._get_library()
        if lib:
            try:
                if hasattr(lib, 'remove_cell'):
                    lib.remove_cell(memory_id, reason=reason)
                    deleted_from.append("library")
                elif hasattr(lib, 'archive_cell'):
                    lib.archive_cell(memory_id, reason=reason or "统一接口删除")
                    deleted_from.append("library(archived)")
                else:
                    logger.debug(f"[统一接口] 藏书阁不支持 remove_cell/archive_cell")
            except Exception as e:
                errors.append(f"library: {e}")
                logger.warning(f"[统一接口] 藏书阁 delete_memory 失败: {e}")
        
        return {
            "memory_id": memory_id,
            "deleted_from": deleted_from,
            "errors": errors,
            "success": len(errors) == 0,
            "reason": reason,
        }
    
    async def query_knowledge_base(self, query_text: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        [v2.0] 独立查询知识库(DomainNexus)。
        
        这是记忆系统（记忆仓库）调用知识库系统的标准通道：
        - 记忆仓库可以随时查看/调用 DomainNexus
        """
        kb = self._get_knowledge_bridge()
        if not kb:
            return []
        return kb.search_by_content(query_text, limit=top_k)
    
    async def manage_knowledge_cell(
        self, action: str, cell_id: str, **kwargs
    ) -> Dict[str, Any]:
        """
        [v2.0] 知识库管理操作（藏书阁工作人员专用）。
        
        Args:
            action: create / update / archive / iterate / search
            cell_id: 目标格子ID
            **kwargs: 操作参数（content, tags, operator 等）
            
        Returns:
            操作结果
        """
        kb = self._get_knowledge_bridge()
        if not kb:
            return {"error": "知识库桥接器不可用"}
        
        operator = kwargs.get("operator", "")
        
        if action == "create":
            record = kb.create_cell(
                cell_id=cell_id,
                title=kwargs["title"],
                content=kwargs["content"],
                category=kwargs.get("category", "A"),
                tags=kwargs.get("tags"),
                operator=operator,
            )
            return {"action": "created", "cell_id": cell_id, "record": record}
        
        elif action == "update":
            record = kb.update_cell(
                cell_id=cell_id,
                content=kwargs.get("content"),
                tags=kwargs.get("tags"),
                operator=operator,
                iteration_note=kwargs.get("iteration_note"),
            )
            return {"action": "updated", "cell_id": cell_id}
        
        elif action == "archive":
            result = kb.archive_cell(cell_id, reason=kwargs["reason"], operator=operator)
            return result
        
        elif action == "iterate":
            record = kb.iterate_cell(cell_id, iteration_note=kwargs["iteration_note"], operator=operator)
            return {"action": "iterated", "cell_id": cell_id}
        
        else:
            return {"error": f"未知操作: {action}"}


# ─────────────────────────────────────────────────────────────────────────────
# 便捷函数
# ─────────────────────────────────────────────────────────────────────────────

_global_interface: Optional[UnifiedMemoryInterface] = None
_global_interface_lock = threading.Lock()


async def get_unified_memory() -> UnifiedMemoryInterface:
    """获取全局统一记忆接口（线程安全双重检查锁）"""
    global _global_interface
    if _global_interface is None:
        with _global_interface_lock:
            if _global_interface is None:
                _global_interface = UnifiedMemoryInterface()
    return _global_interface


# ─────────────────────────────────────────────────────────────────────────────
# v7.0 DomainNexus 桥接适配器 — 当 LibraryKnowledgeBridge 不可用时使用
# ─────────────────────────────────────────────────────────────────────────────

class _DomainNexusBridgeAdapter:
    """
    DomainNexus 桥接适配器

    当原 LibraryKnowledgeBridge 不可用时，使用 DomainNexus 作为知识库后端。
    提供统一的 search_by_content / create_cell / update_cell / get_stats 接口。
    """

    def __init__(self, nexus):
        self._nexus = nexus

    def search_by_content(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索知识内容"""
        result = self._nexus.query(query)
        cells = result.get("relevant_cells", [])
        return [
            {
                "cell_id": c.get("cell_id", ""),
                "title": c.get("name", ""),
                "content": c.get("summary", ""),
                "tags": c.get("tags", []),
                "source": "domain_nexus",
            }
            for c in cells[:limit]
        ]

    def create_cell(self, cell_id, title, content, category="A", tags=None, operator=""):
        """创建知识格子"""
        tags = tags or []
        new_id = self._nexus.cell_manager.create_cell(title, set(tags), content)
        return {"cell_id": new_id or cell_id, "created": new_id is not None}

    def update_cell(self, cell_id, content=None, tags=None, operator="", iteration_note=""):
        """更新知识格子"""
        updated = False
        if content:
            try:
                updated = self._nexus.cell_manager.enrich_cell(cell_id, {"summary": content})
            except Exception as e:
                logger.warning(f"[桥接适配器] 更新cell失败: {e}")
                updated = False
        if tags:
            try:
                updated = self._nexus.cell_manager.enrich_cell(cell_id, {"new_tags": set(tags)}) or updated
            except Exception as e:
                logger.warning(f"[桥接适配器] 更新cell标签失败: {e}")
        return {"cell_id": cell_id, "updated": updated}

    def archive_cell(self, cell_id: str, reason: str = "", operator: str = "") -> Dict[str, Any]:
        """
        归档知识格子
        
        DomainNexus 原生不支持归档，通过 enrich_cell 写入归档标记模拟。
        """
        try:
            cell = self._nexus.cell_manager.cells.get(cell_id)
            if not cell:
                return {"error": f"格子 {cell_id} 不存在", "archived": False}
            # 写入归档标记到摘要
            archive_mark = f"[已归档] {reason}" if reason else "[已归档]"
            self._nexus.cell_manager.enrich_cell(cell_id, {
                "summary": f"{archive_mark} — {cell.summary}" if cell.summary else archive_mark,
            })
            return {"cell_id": cell_id, "archived": True, "reason": reason}
        except Exception as e:
            logger.warning(f"[桥接适配器] 归档cell失败: {e}")
            return {"error": str(e), "archived": False}

    def iterate_cell(self, cell_id: str, iteration_note: str = "", operator: str = "") -> Dict[str, Any]:
        """
        迭代知识格子
        
        通过 enrich_cell 丰富格子内容，模拟迭代操作。
        """
        try:
            cell = self._nexus.cell_manager.cells.get(cell_id)
            if not cell:
                return {"error": f"格子 {cell_id} 不存在", "iterated": False}
            # 将迭代记录作为新洞见写入
            insight = f"[迭代 {operator or '系统'}] {iteration_note}"
            result = self._nexus.cell_manager.enrich_cell(cell_id, {
                "new_insights": [insight],
            })
            return {"cell_id": cell_id, "iterated": result, "iteration_note": iteration_note}
        except Exception as e:
            logger.warning(f"[桥接适配器] 迭代cell失败: {e}")
            return {"error": str(e), "iterated": False}

    def get_stats(self) -> Dict[str, Any]:
        """获取知识库统计"""
        return self._nexus.get_status()


# ─────────────────────────────────────────────────────────────────────────────
# v7.0 LLM增强 — 记忆系统的 LLM 调用支持
# ─────────────────────────────────────────────────────────────────────────────

def enhance_with_llm(prompt: str, context: str = "") -> str:
    """
    记忆系统 LLM 增强

    为记忆编码、检索优化提供 LLM 语义分析能力。
    使用 llm_rule_layer 统一接口。

    Args:
        prompt: 分析提示
        context: 上下文信息

    Returns:
        LLM 分析结果（或规则回退结果）
    """
    try:
        import sys
        from pathlib import Path
        project_root = Path(__file__).resolve().parents[3]  # somn/
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from knowledge_cells.llm_rule_layer import call_module_llm
        return call_module_llm("NeuralMemory", prompt, fallback_func=lambda p, **_: p[:200])
    except ImportError:
        return prompt[:200]


__all__ = [
    'UnifiedMemoryEntry',
    'UnifiedMemoryQuery',
    'UnifiedMemoryResult',
    'UnifiedMemoryInterface',
    'get_unified_memory',
    'enhance_with_llm',
]
