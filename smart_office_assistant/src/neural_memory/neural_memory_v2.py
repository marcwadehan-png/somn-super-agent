# -*- coding: utf-8 -*-
"""
NeuralMemory v6.2.0 - 三层神经记忆架构
========================================

[品牌定位]
NeuralMemory 是 Somn 的三层神经记忆系统，由以下核心概念构成：

  三层记忆架构 (书架)      — 记忆的分层存储体系
  藏书阁 (记忆仓库)         — ImperialLibrary，记忆的持久化仓库
  NeuralMemory (管理工具)   — 本门面类，仓库的统一操作入口
  藏书阁工作人员 (主管)      — LibraryStaffRegistry，Claw贤者职务架构
  学习系统 (管理制度)       — LearningReplayBuffer，出入库管理体系
  知识域格子 (知识库)       — DomainNexus，与记忆系统打通

架构角色：
  用户/外部系统
       │
       ▼
  ┌─────────────┐
  │ NeuralMemory │ ◄── 本文件（三层神经记忆架构的统一门面）
  └──┬────┬─────┘
     │    │
     ├──► ImperialLibrary (藏书阁 - 记忆仓库)
     ├──► SemanticEncoder (语义编码器 - 向量生成)
     ├──► LearningReplayBuffer (学习回放 - 出入库管理制度)
     ├──► LibraryStaffRegistry (藏书阁工作人员 - Claw贤者职务架构)
     └──► LibraryKnowledgeBridge (知识库桥接 - DomainNexus)

核心能力：
1. 记忆入库 → 自动语义编码 + 跨域关联 + 分级
2. 语义检索 → 向量相似度排序
3. 经验回放 → 从历史中提取模式供学习
4. 权限控制 → 分级访问（READ_ONLY ~ ADMIN）

版本: v2.2.0
创建: 2026-04-28
更新: 2026-04-29 (LazyLoader重构 + LRU内存管理)
"""

from __future__ import annotations

import time
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# 快速加载模块
from .neural_memory_fast_load import LazyLoader, LoadStrategy

logger = logging.getLogger(__name__)

# ── 网络搜索增强（懒加载） ──
_NEURAL_WEB: Optional[Any] = None


def _get_neural_web():
    """获取NeuralMemoryWeb实例（懒加载）"""
    global _NEURAL_WEB
    if _NEURAL_WEB is None:
        try:
            # 使用绝对路径导入
            import sys
            from pathlib import Path
            kc_path = Path(__file__).resolve().parents[2].parent / "knowledge_cells"
            if str(kc_path.parent) not in sys.path:
                sys.path.insert(0, str(kc_path.parent))
            from knowledge_cells.web_integration import NeuralMemoryWeb
            _NEURAL_WEB = NeuralMemoryWeb()
        except ImportError as e:
            logger.warning(f"[NeuralMemory] Web integration not available: {e}")
            return None
    return _NEURAL_WEB


# ═══════════════════════════════════════════════════════════════
#  数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class MemoryRecord:
    """统一记忆记录（对外暴露的简化接口）"""
    def __init__(
        self,
        id: str,
        title: str = "",
        content: str = "",
        tags: Optional[List[str]] = None,
        embedding: Optional[List[float]] = None,
        score: float = 0.0,
        grade: str = "",
        tier: str = "",
        source: str = "",
        created_at: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
        memory_type: str = "",
        encoding: Optional[List[float]] = None,  # 向后兼容
    ):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags or []
        self.embedding = embedding or encoding  # 兼容 encoding 参数
        self.score = score
        self.grade = grade
        self.tier = tier
        self.source = source
        self.created_at = created_at if created_at is not None else time.time()
        self.metadata = metadata or {}
        self.memory_type = memory_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "embedding_dim": len(self.embedding) if self.embedding else 0,
            "score": self.score,
            "grade": self.grade,
            "tier": self.tier,
            "source": self.source,
            "memory_type": self.memory_type,
        }


@dataclass
class SearchResult:
    """检索结果"""
    record: MemoryRecord
    similarity: float = 0.0
    rank: int = 0

    def to_dict(self) -> Dict[str, Any]:
        d = self.record.to_dict()
        d["similarity"] = round(self.similarity, 4)
        d["rank"] = self.rank
        return d


@dataclass
class NeuralMemoryStats:
    """系统统计"""
    total_memories: int = 0
    total_replays: int = 0
    buffer_size: int = 0
    encoder_dimension: int = 0
    uptime_seconds: float = 0.0
    last_operation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_memories": self.total_memories,
            "total_replays": self.total_replays,
            "buffer_size": self.buffer_size,
            "encoder_dimension": self.encoder_dimension,
            "uptime_seconds": round(self.uptime_seconds, 1),
            "last_operation": self.last_operation,
        }


# ═══════════════════════════════════════════════════════════════
#  核心类：NeuralMemory (Facade)
# ═══════════════════════════════════════════════════════════════


class NeuralMemory:
    """
    神经记忆系统 v2.0 — 统一入口 (Facade 模式)

    将以下子系统整合为一个一致的高层 API：

    | 子系统 | 文件位置 | 职责 |
    |--------|---------|------|
    | ImperialLibrary | wisdom_dispatch/_imperial_library.py | 记忆存储/检索/持久化 |
    | SemanticEncoder | wisdom_dispatch/_semantic_encoder.py | 语义向量编码 |
    | LearningReplayBuffer | neural_memory/learning_replay_buffer.py | 经验回放/学习 |
    | StaffRegistry | wisdom_dispatch/_library_staff_registry.py | 权限管理 |
    | KnowledgeBridge | wisdom_dispatch/_library_knowledge_bridge.py | 知识库桥接 |

    使用方式::

        nm = NeuralMemory()

        # 入库
        rec = nm.store(
            title="用户留存优化实验",
            content="7日留存率从32%提升至41%",
            tags=["retention", "growth"],
            source="CLAW_EXECUTION",
        )

        # 检索
        results = nm.search("如何提升用户留存", top_k=5)
        for r in results:
            print(f"{r.record.title} sim={r.similarity:.3f}")

        # 经验回放
        batch = nm.get_replay_batch(batch_size=10)
        for entry in batch.entries:
            print(f"经验: {entry.content[:50]}")

        # 统计
        stats = nm.get_stats()
        print(f"总记忆数: {stats.total_memories}")
    """

    def __init__(self, use_fast_load: bool = True):
        """
        初始化 NeuralMemory v2.2.0。
        
        Args:
            use_fast_load: 是否使用快速加载模式（默认True）
                          True: 毫秒级启动，组件懒加载 + LRU内存管理
                          False: 兼容旧行为（同步预加载）
        """
        self._start_time = time.time()
        self._operation_count = 0
        self._use_fast_load = use_fast_load

        # ── 子组件（延迟初始化） ──
        self._library = None          # ImperialLibrary (兼容模式)
        self._encoder = None           # SemanticEncoder (兼容模式)
        self._replay_buffer = None     # LearningReplayBuffer (兼容模式)
        self._staff_registry = None    # LibraryStaffRegistry
        self._knowledge_bridge = None  # LibraryKnowledgeBridge
        self._components_loaded = set()  # 追踪已加载的组件

        # ── 网络搜索增强 ──
        self._neural_web = None      # NeuralMemoryWeb (懒加载)

        # ── LazyLoader 管理（快速加载模式） ──
        self._loaders: Dict[str, LazyLoader] = {}
        self._component_order: List[str] = []  # LRU访问顺序
        self._max_loaded = 3  # 最多同时加载3个组件
        
        if self._use_fast_load:
            self._init_lazy_loaders()
            logger.info("[NeuralMemory] v2.2 快速加载模式（LazyLoader + LRU）")
        else:
            # 兼容模式：同步预加载
            self._init_library(eager=True)
            self._init_encoder(eager=True)
            self._init_replay_buffer(eager=True)
            logger.info("[NeuralMemory] v2.2 初始化完成（预加载模式）")
    
    def _init_lazy_loaders(self):
        """初始化 LazyLoader 管理组件（v2.2.0 新增）"""
        # ImperialLibrary - 懒加载
        self._loaders["library"] = LazyLoader(
            "library",
            self._create_library,
            LoadStrategy.LAZY,
        )
        
        # SemanticEncoder - 懒加载
        self._loaders["encoder"] = LazyLoader(
            "encoder",
            self._create_encoder,
            LoadStrategy.LAZY,
        )
        
        # LearningReplayBuffer - 按需加载
        self._loaders["replay_buffer"] = LazyLoader(
            "replay_buffer",
            self._create_replay_buffer,
            LoadStrategy.ON_DEMAND,
        )
        
        # StaffRegistry - 按需加载
        self._loaders["staff_registry"] = LazyLoader(
            "staff_registry",
            self._create_staff_registry,
            LoadStrategy.ON_DEMAND,
        )
        
        # KnowledgeBridge - 按需加载
        self._loaders["knowledge_bridge"] = LazyLoader(
            "knowledge_bridge",
            self._create_knowledge_bridge,
            LoadStrategy.ON_DEMAND,
        )
    
    def _create_library(self):
        """工厂方法：创建 ImperialLibrary"""
        from intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        return ImperialLibrary()
    
    def _create_encoder(self):
        """工厂方法：创建 SemanticEncoder"""
        from intelligence.dispatcher.wisdom_dispatch._semantic_encoder import get_semantic_encoder
        return get_semantic_encoder()
    
    def _create_replay_buffer(self):
        """工厂方法：创建 LearningReplayBuffer"""
        from neural_memory.learning_replay_buffer import get_replay_buffer
        return get_replay_buffer()
    
    def _create_staff_registry(self):
        """工厂方法：创建 LibraryStaffRegistry"""
        from intelligence.dispatcher.wisdom_dispatch._library_staff_registry import get_staff_registry
        registry = get_staff_registry()
        registry.ensure_initialized()
        return registry
    
    def _create_knowledge_bridge(self):
        """工厂方法：创建 LibraryKnowledgeBridge"""
        from intelligence.dispatcher.wisdom_dispatch._library_knowledge_bridge import get_knowledge_bridge
        return get_knowledge_bridge()
    
    def _update_lru(self, component_name: str):
        """LRU淘汰策略：更新访问顺序，超过限制时淘汰最旧组件"""
        if not self._use_fast_load:
            return
        
        # 更新访问顺序
        if component_name in self._component_order:
            self._component_order.remove(component_name)
        self._component_order.append(component_name)
        
        # LRU淘汰
        while len(self._component_order) > self._max_loaded:
            oldest = self._component_order.pop(0)
            if oldest in self._loaders:
                self._loaders[oldest].unload()
                logger.debug(f"[NeuralMemory] LRU淘汰组件: {oldest}")
    
    def _get_loader(self, name: str) -> Optional[LazyLoader]:
        """获取指定组件的 LazyLoader"""
        return self._loaders.get(name)

    # ═════════════════════════════════════════════════════════
    #  兼容模式：预加载方法（use_fast_load=False 时使用）
    # ═════════════════════════════════════════════════════════

    def _init_library(self, eager: bool = False):
        """初始化皇家藏书阁（兼容模式）"""
        if self._library is not None:
            return self._library
        
        try:
            from intelligence.dispatcher.wisdom_dispatch._imperial_library import (
                ImperialLibrary,
            )
            self._library = ImperialLibrary()
            self._components_loaded.add("library")
            logger.info("[NeuralMemory] 藏书阁初始化成功")
            return self._library
        except Exception as e:
            logger.warning(f"[NeuralMemory] 藏书阁初始化失败: {e}")
            return None

    def _init_encoder(self, eager: bool = False):
        """初始化语义编码器（兼容模式）"""
        if self._encoder is not None:
            return self._encoder
        
        try:
            from intelligence.dispatcher.wisdom_dispatch._semantic_encoder import (
                get_semantic_encoder,
            )
            self._encoder = get_semantic_encoder()
            self._components_loaded.add("encoder")
            logger.info(
                f"[NeuralMemory] 语义编码器初始化成功 (dim={self._encoder.dimension})"
            )
            return self._encoder
        except Exception as e:
            logger.warning(f"[NeuralMemory] 语义编码器初始化失败: {e}")
            return None

    def _init_replay_buffer(self, eager: bool = False):
        """初始化学习回放缓冲区（兼容模式）"""
        if self._replay_buffer is not None:
            return self._replay_buffer
        
        try:
            from neural_memory.learning_replay_buffer import (
                get_replay_buffer,
            )
            self._replay_buffer = get_replay_buffer()
            self._components_loaded.add("replay_buffer")
            logger.info("[NeuralMemory] 回放缓冲区初始化成功")
            return self._replay_buffer
        except Exception as e:
            logger.warning(f"[NeuralMemory] 回放缓冲区初始化失败: {e}")
            return None

    def _get_staff_registry(self):
        """懒加载权限注册表（兼容模式）"""
        if self._use_fast_load:
            loader = self._loaders.get("staff_registry")
            if loader:
                self._update_lru("staff_registry")
                return loader.get()
            return None
        
        if self._staff_registry is None:
            try:
                from intelligence.dispatcher.wisdom_dispatch._library_staff_registry import (
                    get_staff_registry,
                )
                self._staff_registry = get_staff_registry()
                self._staff_registry.ensure_initialized()
            except Exception as e:
                logger.warning(f"[NeuralMemory] 权限注册表加载失败: {e}")
        return self._staff_registry

    def _get_knowledge_bridge(self):
        """懒加载知识库桥接器（兼容模式）"""
        if self._use_fast_load:
            loader = self._loaders.get("knowledge_bridge")
            if loader:
                self._update_lru("knowledge_bridge")
                return loader.get()
            return None
        
        if self._knowledge_bridge is None:
            try:
                from intelligence.dispatcher.wisdom_dispatch._library_knowledge_bridge import (
                    get_knowledge_bridge,
                )
                self._knowledge_bridge = get_knowledge_bridge()
            except Exception as e:
                logger.warning(f"[NeuralMemory] 知识库桥接器加载失败: {e}")
        return self._knowledge_bridge

    # ═════════════════════════════════════════════════════════
    #  核心能力：懒加载触发器
    # ═════════════════════════════════════════════════════════

    @property
    def library(self):
        """懒加载藏书阁（使用 LazyLoader + LRU）"""
        if self._use_fast_load:
            loader = self._loaders.get("library")
            if loader:
                self._update_lru("library")
                return loader.get()
            return None
        # 兼容模式
        if self._library is None:
            self._init_library(eager=True)
        return self._library

    @property
    def encoder(self):
        """懒加载编码器（使用 LazyLoader + LRU）"""
        if self._use_fast_load:
            loader = self._loaders.get("encoder")
            if loader:
                self._update_lru("encoder")
                return loader.get()
            return None
        # 兼容模式
        if self._encoder is None:
            self._init_encoder(eager=True)
        return self._encoder

    @property
    def replay_buffer(self):
        """懒加载回放缓冲区（使用 LazyLoader + LRU）"""
        if self._use_fast_load:
            loader = self._loaders.get("replay_buffer")
            if loader:
                self._update_lru("replay_buffer")
                return loader.get()
            return None
        # 兼容模式
        if self._replay_buffer is None:
            self._init_replay_buffer(eager=True)
        return self._replay_buffer

    @property
    def neural_web(self):
        """懒加载网络搜索增强（NeuralMemoryWeb）"""
        if self._neural_web is None:
            self._neural_web = _get_neural_web()
        return self._neural_web

    # ═════════════════════════════════════════════════════════
    #  预热和状态管理
    # ═════════════════════════════════════════════════════════

    def preload(self, components: Optional[List[str]] = None):
        """
        预加载指定组件（v2.2.0 使用 LazyLoader）
        
        Args:
            components: 要预加载的组件列表，如 ["library", "encoder", "replay_buffer"]
                      None=全部核心组件
        """
        if not self._use_fast_load:
            # 兼容模式：直接初始化
            if components is None:
                components = ["library", "encoder"]
            for comp in components:
                if comp == "library":
                    self._init_library(eager=True)
                elif comp == "encoder":
                    self._init_encoder(eager=True)
                elif comp == "replay_buffer":
                    self._init_replay_buffer(eager=True)
            return
        
        # 快速加载模式：使用 LazyLoader.preload()
        if components is None:
            components = ["library", "encoder"]
        
        for comp in components:
            if comp in self._loaders:
                self._loaders[comp].preload()
                self._update_lru(comp)

    def get_load_status(self) -> Dict[str, Any]:
        """
        获取加载状态（v2.2.0 适配 LazyLoader）
        
        Returns:
            各组件的加载状态
        """
        components_status = {}
        
        # 检查核心组件
        for name in ["library", "encoder", "replay_buffer", "staff_registry", "knowledge_bridge"]:
            if self._use_fast_load and name in self._loaders:
                # 快速加载模式：检查 LazyLoader
                loader = self._loaders[name]
                components_status[name] = {
                    "loaded": loader.is_loaded(),
                    "load_time_ms": loader.get_load_time() * 1000,
                    "strategy": loader.strategy,
                }
            else:
                # 兼容模式：检查实例变量
                instance = getattr(self, f"_{name}", None)
                components_status[name] = {
                    "loaded": instance is not None,
                    "loaded_at_init": name in self._components_loaded,
                }
        
        return {
            "version": "v6.2.0",
            "fast_load_mode": self._use_fast_load,
            "startup_time_ms": (time.time() - self._start_time) * 1000,
            "lru_order": self._component_order.copy() if hasattr(self, '_component_order') else [],
            "max_loaded": self._max_loaded if hasattr(self, '_max_loaded') else 0,
            "components": components_status,
        }

    # ═════════════════════════════════════════════════════════
    #  核心能力：记忆 CRUD
    # ═════════════════════════════════════════════════════════

    def store(
        self,
        content: str,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        source: str = "NEURAL_MEMORY",
        category: str = "LEARNING_INSIGHT",
        wing_name: str = "LEARN",
        shelf: str = "experiments",
        operator: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[MemoryRecord]:
        """
        存储一条记忆（自动语义编码 + 跨域关联 + 分级）。

        Args:
            content: 记忆内容 (必填)
            title: 记忆标题 (可选，默认从content提取)
            tags: 标签列表
            source: 来源类型（MemorySource 枚举名）
            category: 分类（MemoryCategory 枚举名）
            wing_name: 分馆名称（LibraryWing 枚举名）
            shelf: 书架名称
            operator: 操作者
            metadata: 额外元数据

        Returns:
            MemoryRecord 或 None
        """
        # 自动从 content 提取 title
        if title is None:
            title = content[:50] + ("..." if len(content) > 50 else "")
        
        # 懒加载藏书阁（如果尚未加载）
        library = self.library
        if library is None:
            logger.error("[NeuralMemory] store 失败：藏书阁未初始化")
            return None

        try:
            # 解析枚举
            wing = self._resolve_wing(wing_name)
            source_enum = self._resolve_source(source)
            category_enum = self._resolve_category(category)

            # ── 网络搜索：获取相关背景知识 ──
            web_knowledge = None
            if self.neural_web and self.neural_web.should_search(content):
                try:
                    web_result = self.neural_web.search_for_memory(
                        content=content,
                        tags=tags,
                        max_results=3
                    )
                    if web_result.get("success") and web_result.get("results"):
                        web_knowledge = web_result["results"]
                        logger.info(f"[NeuralMemory] Web search found {len(web_knowledge)} related items")
                except Exception as e:
                    logger.warning(f"[NeuralMemory] Web search failed: {e}")

            # ── 构建增强元数据 ──
            enhanced_metadata = metadata or {}
            if web_knowledge:
                enhanced_metadata["_web_knowledge"] = web_knowledge
                enhanced_metadata["_web_enhanced"] = True

            # 入库（内部会自动编码+关联+分级）
            cell = library.submit_cell(
                title=title,
                content=content,
                wing=wing,
                shelf=shelf,
                source=source_enum,
                category=category_enum,
                tags=tags or [],
                reporting_system="neural_memory_v2",
                metadata=enhanced_metadata,
                operator=operator,
            )

            # 转换为统一的 MemoryRecord
            rec = MemoryRecord(
                id=cell.id,
                title=cell.title,
                content=cell.content,
                tags=list(cell.tags),
                embedding=cell.semantic_embedding,
                score=cell.value_score,
                grade=cell.grade.value if hasattr(cell.grade, 'value') else str(cell.grade),
                tier=getattr(cell, 'tier', '') or '',
                source=source,
                created_at=cell.created_at,
                metadata={
                    "wing": wing.name if hasattr(wing, 'name') else str(wing),
                    "shelf": shelf,
                    "cross_references": list(cell.cross_references) if hasattr(cell, 'cross_references') else [],
                },
            )

            self._operation_count += 1
            logger.info(
                f"[NeuralMemory] store OK: {rec.id} "
                f"(score={rec.score:.2f}, grade={rec.grade})"
            )
            return rec

        except Exception as e:
            logger.error(f"[NeuralMemory] store 异常: {e}")
            return None

    def search(
        self,
        query: str,
        top_k: int = 10,
        tags: Optional[List[str]] = None,
        min_score: float = 0.0,
    ) -> List[SearchResult]:
        """
        语义检索记忆（支持关键词 + 向量相似度混合排序）。

        Args:
            query: 查询文本
            top_k: 返回数量
            tags: 标签过滤
            min_score: 最低价值评分

        Returns:
            SearchResult 列表（按相关性降序）
        """
        # 懒加载藏书阁
        library = self.library
        if library is None:
            logger.error("[NeuralMemory] search 失败：藏书阁未初始化")
            return []

        results = []
        try:
            # 1. 从藏书阁查询（关键词/标签匹配）
            cells = library.query_cells(
                keyword=query,
                tags=tags,
                limit=top_k * 3,  # 多取一些做重排
            )

            # 1.5 如果关键词搜索无结果，fallback 到全量查询 + 语义精排
            if not cells:
                cells = library.query_cells(
                    tags=tags,
                    limit=top_k * 5,  # 多取一些供语义排序
                )

            # 2. 如果有编码器，用向量相似度精排
            encoder = self.encoder
            if encoder:
                qvec = encoder.encode(query)
                scored = []
                for cell in cells:
                    cvec = getattr(cell, 'semantic_embedding', None)
                    if cvec and isinstance(cvec, list):
                        sim = encoder.similarity(qvec, cvec)
                    else:
                        sim = 0.0  # 无向量时退化为关键词匹配

                    scored.append((cell, sim))

                # 按相似度排序
                scored.sort(key=lambda x: -x[1])

                for rank, (cell, sim) in enumerate(scored[:top_k]):
                    if cell.value_score >= min_score:
                        results.append(SearchResult(
                            record=self._cell_to_record(cell),
                            similarity=sim,
                            rank=rank + 1,
                        ))
            else:
                # 无编码器时直接按 value_score 排序
                for rank, cell in enumerate(cells[:top_k]):
                    if cell.value_score >= min_score:
                        results.append(SearchResult(
                            record=self._cell_to_record(cell),
                            similarity=float(cell.value_score),
                            rank=rank + 1,
                        ))

            self._operation_count += 1
            logger.info(
                f"[NeuralMemory] search '{query[:30]}...' → {len(results)} 条结果"
            )
            return results

        except Exception as e:
            logger.error(f"[NeuralMemory] search 异常: {e}")
            return []

    def search_with_web(
        self,
        query: str,
        top_k: int = 10,
        tags: Optional[List[str]] = None,
        min_score: float = 0.0,
    ) -> Dict[str, Any]:
        """
        增强语义检索（本地 + 网络搜索融合）

        当本地结果不足或包含时间敏感关键词时，自动补充网络搜索结果。

        Args:
            query: 查询文本
            top_k: 返回数量
            tags: 标签过滤
            min_score: 最低价值评分

        Returns:
            {
                "local_results": List[SearchResult],  # 本地记忆结果
                "web_results": List[Dict],           # 网络搜索结果
                "web_enhanced": bool,                # 是否启用了网络增强
                "query": str,
            }
        """
        # 先执行本地搜索
        local_results = self.search(query, top_k=top_k, tags=tags, min_score=min_score)

        result = {
            "local_results": local_results,
            "web_results": [],
            "web_enhanced": False,
            "query": query,
        }

        # 检查是否需要网络搜索增强
        if not self.neural_web or not self.neural_web.should_search(query):
            return result

        # 如果本地结果少，补充网络搜索
        if len(local_results) < 3:
            try:
                web_result = self.neural_web.search_for_memory(
                    content=query,
                    tags=tags,
                    max_results=5
                )
                if web_result.get("success") and web_result.get("results"):
                    result["web_results"] = web_result["results"]
                    result["web_enhanced"] = True
                    logger.info(f"[NeuralMemory] Web enhanced: {len(web_result['results'])} items")
            except Exception as e:
                logger.warning(f"[NeuralMemory] Web search failed: {e}")

        return result

    def get(self, memory_id: str) -> Optional[MemoryRecord]:
        """获取单条记忆"""
        library = self.library
        if library is None:
            return None
        try:
            cell = library.get_cell(memory_id)
            if cell:
                return self._cell_to_record(cell)
        except Exception as e:
            logger.error(f"[NeuralMemory] get 异常: {e}")
        return None

    def delete(self, memory_id: str, operator: str = "") -> bool:
        """删除一条记忆"""
        library = self.library
        if library is None:
            return False
        try:
            ok = library.delete_cell(memory_id, operator=operator)
            if ok:
                self._operation_count += 1
            return ok
        except Exception as e:
            logger.error(f"[NeuralMemory] delete 异常: {e}")
            return False

    # ═════════════════════════════════════════════════════════
    #  核心能力：语义编码
    # ═════════════════════════════════════════════════════════

    def encode(self, text: str) -> Optional[List[float]]:
        """对文本进行语义编码，返回向量。"""
        encoder = self.encoder
        if encoder is None:
            return None
        try:
            return encoder.encode(text)
        except Exception as e:
            logger.error(f"[NeuralMemory] encode 异常: {e}")
            return None

    def similarity(
        self, text_a: str, text_b: str, method: str = "cosine"
    ) -> float:
        """计算两段文本的语义相似度。"""
        encoder = self.encoder
        if encoder is None:
            return 0.0
        try:
            vec_a = encoder.encode(text_a)
            vec_b = encoder.encode(text_b)
            return encoder.similarity(vec_a, vec_b, method=method)
        except Exception as e:
            logger.error(f"[NeuralMemory] similarity 异常: {e}")
            return 0.0

    # ═════════════════════════════════════════════════════════
    #  核心能力：学习回放
    # ═════════════════════════════════════════════════════════

    def get_replay_batch(
        self, batch_size: int = 16, balanced: bool = True
    ):
        """
        获取一批经验回放数据（供学习系统使用）。

        Returns:
            ReplayBatch 或 None
        """
        rb = self.replay_buffer
        if rb is None:
            return None
        try:
            return rb.get_replay_batch(
                batch_size=batch_size, balanced=balanced
            )
        except Exception as e:
            logger.error(f"[NeuralMemory] get_replay_batch 异常: {e}")
            return None

    def add_replay_entry(self, entry) -> bool:
        """手动添加一条经验到回放缓冲区。"""
        rb = self.replay_buffer
        if rb is None:
            return False
        try:
            return rb.add_entry(entry)
        except Exception as e:
            logger.error(f"[NeuralMemory] add_replay_entry 异常: {e}")
            return False

    def extract_from_library(self, force: bool = False) -> int:
        """从藏书阁提取高价值记忆填充回放缓冲区。"""
        rb = self.replay_buffer
        lib = self.library
        if rb is None or lib is None:
            return 0
        try:
            return rb.extract_from_library(
                library=lib, force=force
            )
        except Exception as e:
            logger.error(f"[NeuralMemory] extract_from_library 异常: {e}")
            return 0

    # ═════════════════════════════════════════════════════════
    #  核心能力：跨域关联
    # ═════════════════════════════════════════════════════════

    def find_related(self, memory_id: str, max_results: int = 10) -> List[MemoryRecord]:
        """查找与指定记忆相关的其他记忆（基于标签/语义）。"""
        library = self.library
        if library is None:
            return []
        try:
            cell = library.get_cell(memory_id)
            if not cell or not cell.tags:
                return []

            related_cells = library.query_cells(
                tags=list(cell.tags), limit=max_results + 1
            )
            return [
                self._cell_to_record(c)
                for c in related_cells
                if c.id != memory_id
            ][:max_results]
        except Exception as e:
            logger.error(f"[NeuralMemory] find_related 异常: {e}")
            return []

    def get_cross_domain_links(self, memory_id: str) -> List[str]:
        """获取记忆的跨域引用 ID 列表。"""
        library = self.library
        if library is None:
            return []
        try:
            cell = library.get_cell(memory_id)
            if cell and hasattr(cell, 'cross_references'):
                return list(cell.cross_references)
        except Exception as e:
            logger.error(f"[NeuralMemory] get_cross_domain_links 异常: {e}")
        return []

    # ═════════════════════════════════════════════════════════
    #  核心能力：权限 & 管理
    # ═════════════════════════════════════════════════════════

    def check_permission(self, actor: str, action: str = "read") -> bool:
        """检查操作权限。"""
        registry = self._get_staff_registry()
        if registry is None:
            return True  # 无权限系统时默认允许
        try:
            return registry.check_permission(actor, action)
        except AttributeError:
            # 兼容旧版 API
            write_names = getattr(registry, 'list_all_names_with_write', lambda: set())()
            if action in ("write", "delete", "admin"):
                return actor in write_names
            return True
        except Exception:
            return True

    def get_stats(self) -> NeuralMemoryStats:
        """获取系统统计信息。"""
        stats = NeuralMemoryStats()
        stats.uptime_seconds = time.time() - self._start_time

        lib = self.library
        if lib:
            lib_stats = getattr(lib, '_stats', {})
            stats.total_memories = lib_stats.get("total_records", 0)

        rb = self.replay_buffer
        if rb:
            buf_stats = rb.get_statistics()
            stats.buffer_size = buf_stats.get("buffer_size", 0)
            stats.total_replays = buf_stats.get("total_replays", 0)

        enc = self.encoder
        if enc:
            stats.encoder_dimension = enc.dimension

        stats.last_operation = f"第{self._operation_count}次操作"

        return stats

    # ═════════════════════════════════════════════════════════
    #  内部辅助方法
    # ═════════════════════════════════════════════════════════

    @staticmethod
    def _cell_to_record(cell) -> MemoryRecord:
        """将 CellRecord 转换为 MemoryRecord"""
        return MemoryRecord(
            id=cell.id,
            title=cell.title,
            content=cell.content,
            tags=list(cell.tags),
            embedding=cell.semantic_embedding if hasattr(cell, 'semantic_embedding') else None,
            score=cell.value_score,
            grade=cell.grade.value if hasattr(cell.grade, 'value') else str(cell.grade),
            tier=getattr(cell, 'tier', '') or '',
            source=cell.source.value if hasattr(cell.source, 'value') else str(cell.source),
            created_at=getattr(cell, 'created_at', time.time()),
            metadata={"cross_references": list(getattr(cell, 'cross_references', []))},
        )

    @staticmethod
    def _resolve_wing(name: str):
        """解析分馆枚举"""
        from intelligence.dispatcher.wisdom_dispatch._imperial_library import LibraryWing
        try:
            return LibraryWing[name.upper()]
        except KeyError:
            return LibraryWing.LEARN

    @staticmethod
    def _resolve_source(name: str):
        """解析来源枚举"""
        from intelligence.dispatcher.wisdom_dispatch._imperial_library import MemorySource
        try:
            return MemorySource[name.upper()]
        except KeyError:
            return MemorySource.NEURAL_MEMORY

    @staticmethod
    def _resolve_category(name: str):
        """解析分类枚举"""
        from intelligence.dispatcher.wisdom_dispatch._imperial_library import MemoryCategory
        try:
            return MemoryCategory[name.upper()]
        except KeyError:
            return MemoryCategory.LEARNING_INSIGHT

    def __repr__(self) -> str:
        stats = self.get_stats()
        return (
            f"NeuralMemory(v2.2.0) memories={stats.total_memories} "
            f"buffer={stats.buffer_size} dim={stats.encoder_dimension}"
        )


# ═══════════════════════════════════════════════════════════════
#  全局单例
# ═══════════════════════════════════════════════════════════════

_global_instance: Optional[NeuralMemory] = None


def get_neural_memory() -> NeuralMemory:
    """获取 NeuralMemory 全局单例"""
    global _global_instance
    if _global_instance is None:
        _global_instance = NeuralMemory()
    return _global_instance


__all__ = [
    'NeuralMemory',
    'MemoryRecord',
    'SearchResult',
    'NeuralMemoryStats',
    'get_neural_memory',
]
