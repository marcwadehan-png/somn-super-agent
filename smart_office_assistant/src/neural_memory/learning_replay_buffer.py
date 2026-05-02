# -*- coding: utf-8 -*-
"""
NeuralMemory — 学习经验回放缓冲区 v1.0
learning_replay_buffer.py

[NeuralMemory 架构定位]
本模块是 NeuralMemory（三层神经记忆架构）中「学习系统」的核心组件。
学习系统是记忆仓库（藏书阁）出入库的管理制度和体系：
- 入库方向（已有）：LearningPipeline → 藏书阁 submit_cell
- 出库方向（本模块新增）：藏书阁 → 学习系统的经验回读

功能：
  - 从藏书阁提取高价值记忆作为学习样本
  - 经验重放(Experience Replay)：定期回读历史记忆强化学习
  - 跨域知识迁移：从知识库(DomainNexus)抽取模式到记忆仓库
  - 失败案例回放：从低分记忆中提取教训

流程：
  藏书阁 CellRecord → ReplayEntry → LearningPipeline 策略选择 → 记忆更新

版本: v1.0.0
创建: 2026-04-28
"""

from __future__ import annotations

import logging
import time
import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
#  数据结构
# ═══════════════════════════════════════════════════════════════


class ReplaySource(Enum):
    """经验来源"""
    LIBRARY_HIGH_VALUE = auto()     # 藏书阁高分记忆
    LIBRARY_RECENT = auto()         # 最近入库的记忆
    LIBRARY_LOW_SCORE = auto()      # 低分记忆（失败案例）
    KNOWLEDGE_CELL = auto()         # 知识库格子
    CROSS_DOMAIN = auto()           # 跨域关联记忆
    REVIEW_PROMOTION = auto()       # 审查提升的记忆
    EXPIRED_EPISODIC = auto()       # 过期情景记忆（回收前）


@dataclass
class ReplayEntry:
    """单条经验回放条目
    
    将藏书阁 CellRecord 或知识库 KnowledgeCell 转换为学习可用的格式。
    """
    entry_id: str                    # 唯一ID
    source: ReplaySource             # 来源类型
    source_cell_id: str              # 原始 CellRecord/Cell ID
    content: str                     # 核心内容（摘要）
    full_content: str = ""           # 完整内容
    grade: str = ""                  # 甲/乙/丙/丁
    tier: str = ""                   # MemoryTier 名称
    value_score: float = 0.5         # 原始价值评分
    importance_weight: float = 1.0   # 回放重要性权重
    lesson_type: str = ""            # 教训类型: success / failure / pattern / anomaly
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    replay_count: int = 0            # 已回放次数
    last_replayed: float = 0.0       # 上次回放时间
    is_consumed: bool = False        # 是否已被消费（学习过）


@dataclass
class ReplayBatch:
    """一批经验回放数据（供 LearningPipeline 使用）"""
    batch_id: str
    entries: List[ReplayEntry]
    total_entries: int
    high_value_count: int            # 高价值条目数
    failure_count: int               # 失败案例数
    cross_domain_count: int          # 跨域条目数
    source_distribution: Dict[str, int]
    created_at: float = field(default_factory=time.time)


@dataclass
class ReplayConfig:
    """回放缓冲区配置"""
    max_size: int = 500              # 缓冲区最大容量
    min_replay_interval_hours: float = 1.0  # 最小回放间隔（小时）
    high_value_ratio: float = 0.3    # 高价值记忆占比
    failure_ratio: float = 0.15      # 失败案例占比
    cross_domain_ratio: float = 0.1  # 跨域占比
    recent_days: int = 7             # 近期记忆天数窗口
    enable_auto_extract: bool = True # 自动从藏书阁提取
    extract_batch_size: int = 20     # 每批提取数量
    decay_factor: float = 0.9        # 权重衰减因子（每次回放后）


# ═══════════════════════════════════════════════════════════════
#  核心类：LearningReplayBuffer
# ═══════════════════════════════════════════════════════════════


class LearningReplayBuffer:
    """
    学习经验回放缓冲区。
    
    架构角色：
    ┌─────────────┐    入库      ┌──────────┐
    │ Learning    │ ──────────→ │ 藏书阁    │
    │ Pipeline    │             │ (记忆仓库)│
    └──────┬──────┘             └────┬─────┘
           │ 出库(回放)              │ 提取
           ↓                         ↓
    ┌──────────────┐         ┌──────────────┐
    │ ReplayBuffer │ ←────── │ extract_from │
    │ (本模块)     │  经验   │ _library()   │
    └──────┬──────┘         └──────────────┘
           │ 回放
           ↓
    ┌─────────────┐
    │ Learning    │ ← 强化学习
    │ Pipeline    │
    └─────────────┘
    
    双向闭环：
    - 正向：学习 → 入库（已有，通过 LearningPipeline.submit）
    - 反向：藏书阁 → 经验提取 → 回放到学习系统（本模块新增）
    """

    def __init__(self, config: Optional[ReplayConfig] = None):
        self.config = config or ReplayConfig()
        self._buffer: Deque[ReplayEntry] = deque(maxlen=self.config.max_size)
        self._lock = threading.Lock()
        self._last_extract_time: float = 0.0
        self._total_extracts: int = 0
        self._total_replays: int = 0
        self._consumed_ids: set = set()
        
        logger.info("学习经验回放缓冲区初始化完成")

    # ═══════════════════════════════════════════════════════════
    #  核心方法：从藏书阁提取经验
    # ═══════════════════════════════════════════════════════════

    def extract_from_library(
        self,
        library=None,
        force: bool = False,
    ) -> int:
        """
        从藏书阁提取记忆条目填充回放缓冲区。
        
        提取策略（按配置比例分配）：
        1. 高价值记忆（value_score >= 0.7）→ 成功经验
        2. 低分记忆（value_score < 0.3）→ 失败案例
        3. 近期入库记忆（7天内）→ 新鲜经验
        4. 跨域关联记忆 → 迁移模式
        
        Args:
            library: 藏书阁实例（None则自动获取）
            force: 强制提取（忽略间隔限制）
            
        Returns:
            本次提取的条目数
        """
        now = time.time()
        interval_ok = (
            force or
            (now - self._last_extract_time) >= self.config.min_replay_interval_hours * 3600
        )
        if not interval_ok:
            logger.debug("[ReplayBuffer] 跳过提取（距离上次太近）")
            return 0

        # 获取藏书阁
        if library is None:
            try:
                from intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
                library = ImperialLibrary()
            except ImportError:
                logger.error("[ReplayBuffer] 无法加载藏书阁")
                return 0

        with self._lock:
            extracted = 0
            
            # 1. 提取高价值记忆
            extracted += self._extract_high_value(library)
            
            # 2. 提取失败案例（低分记忆）
            extracted += self._extract_failures(library)
            
            # 3. 提取近期记忆
            extracted += self._extract_recent(library)
            
            # 4. 提取跨域关联记忆
            extracted += self._extract_cross_domain(library)

            self._last_extract_time = now
            self._total_extracts += 1

        logger.info(
            f"[ReplayBuffer] 提取完成: {extracted} 条 | "
            f"缓冲区大小: {len(self._buffer)}/{self.config.max_size}"
        )
        return extracted

    def _extract_high_value(self, library) -> int:
        """提取高价值记忆（成功经验）"""
        target_count = max(
            1, int(self.config.extract_batch_size * self.config.high_value_ratio)
        )
        cells = library.query_cells(
            limit=target_count * 3,
            grade=None,
        )
        
        count = 0
        for cell in cells:
            if cell.value_score < 0.7:
                continue
            if len(self._buffer) >= self.config.max_size:
                break
            
            entry = ReplayEntry(
                entry_id=f"rv_hv_{cell.id}",
                source=ReplaySource.LIBRARY_HIGH_VALUE,
                source_cell_id=cell.id,
                content=cell.content[:500],
                full_content=cell.content,
                grade=cell.grade.value,
                tier=getattr(cell, 'tier', None),
                value_score=cell.value_score,
                importance_weight=min(cell.value_score * 1.5, 3.0),
                lesson_type="success",
                tags=list(cell.tags),
                metadata={"wing": cell.wing.value, "shelf": cell.shelf},
            )
            self._buffer.append(entry)
            count += 1
        
        return count

    def _extract_failures(self, library) -> int:
        """提取失败案例（低分记忆）"""
        target_count = max(
            1, int(self.config.extract_batch_size * self.config.failure_ratio)
        )
        cells = library.query_cells(limit=target_count * 5, grade=None)
        
        count = 0
        for cell in cells:
            if cell.value_score >= 0.3:
                continue
            if len(self._buffer) >= self.config.max_size:
                break
            
            entry = ReplayEntry(
                entry_id=f"rv_fl_{cell.id}",
                source=ReplaySource.LIBRARY_LOW_SCORE,
                source_cell_id=cell.id,
                content=cell.content[:500],
                full_content=cell.content,
                grade=cell.grade.value,
                value_score=cell.value_score,
                importance_weight=max(0.5, (1.0 - cell.value_score) * 2.0),
                lesson_type="failure",
                tags=list(cell.tags),
                metadata={
                    "wing": cell.wing.value,
                    "reason": "低价值记忆，需审查是否降级或清理",
                },
            )
            self._buffer.append(entry)
            count += 1
        
        return count

    def _extract_recent(self, library) -> int:
        """提取近期入库的记忆"""
        recent_threshold = time.time() - (self.config.recent_days * 86400)
        target_count = max(
            1, int(self.config.extract_batch_size * 0.25)
        )
        
        # 通过 query_cells 遍历各分馆找近期记录
        from intelligence.dispatcher.wisdom_dispatch._imperial_library import LibraryWing

        all_cells = []
        try:
            for wing_code in ["ARCH", "EXEC", "LEARN", "RESEARCH", "EXTERNAL", "USER"]:
                wing_enum = LibraryWing[wing_code]
                wing_cells = library.query_cells(wing=wing_enum, limit=200)
                if wing_cells:
                    all_cells.extend(wing_cells)
        except Exception:
            all_cells = []
        
        recent = [
            c for c in all_cells
            if c.created_at >= recent_threshold
        ]
        recent.sort(key=lambda c: c.created_at, reverse=True)
        
        count = 0
        for cell in recent[:target_count]:
            if len(self._buffer) >= self.config.max_size:
                break
            entry = ReplayEntry(
                entry_id=f"rv_rc_{cell.id}",
                source=ReplaySource.LIBRARY_RECENT,
                source_cell_id=cell.id,
                content=cell.content[:300],
                full_content=cell.content,
                grade=cell.grade.value,
                value_score=cell.value_score,
                importance_weight=1.0,
                lesson_type="pattern",
                tags=list(cell.tags),
                metadata={"age_days": (time.time() - cell.created_at) / 86400},
            )
            self._buffer.append(entry)
            count += 1
        
        return count

    def _extract_cross_domain(self, library) -> int:
        """提取跨域关联的记忆"""
        target_count = max(
            1, int(self.config.extract_batch_size * self.config.cross_domain_ratio)
        )
        
        # 找有跨域引用的记录
        all_cells = []
        try:
            for wing_code in ["ARCH", "EXEC", "LEARN", "RESEARCH", "EXTERNAL", "USER"]:
                wing_enum = LibraryWing[wing_code]
                wing_cells = library.query_cells(wing=wing_enum, limit=200)
                if wing_cells:
                    all_cells.extend(wing_cells)
        except Exception:
            return 0
        
        cross_domain = [
            c for c in all_cells
            if getattr(c, 'cross_references', None) and len(c.cross_references) > 0
        ]
        
        count = 0
        for cell in cross_domain[:target_count]:
            if len(self._buffer) >= self.config.max_size:
                break
            entry = ReplayEntry(
                entry_id=f"rv_cd_{cell.id}",
                source=ReplaySource.CROSS_DOMAIN,
                source_cell_id=cell.id,
                content=cell.content[:400],
                full_content=cell.content,
                grade=cell.grade.value,
                value_score=cell.value_score,
                importance_weight=1.3,
                lesson_type="pattern",
                tags=list(cell.tags),
                metadata={
                    "cross_refs": list(cell.cross_references),
                    "ref_count": len(cell.cross_references),
                },
            )
            self._buffer.append(entry)
            count += 1
        
        return count

    # ═══════════════════════════════════════════════════════════
    #  核心方法：获取回放批次
    # ═══════════════════════════════════════════════════════════

    def get_replay_batch(
        self,
        batch_size: int = 16,
        balanced: bool = True,
    ) -> Optional[ReplayBatch]:
        """
        获取一批经验回放数据供 LearningPipeline 使用。
        
        Args:
            batch_size: 批次大小
            balanced: 是否平衡采样（确保各类型都有）
            
        Returns:
            ReplayBatch 或 None（缓冲区为空时）
        """
        with self._lock:
            if not self._buffer:
                return None
            
            if balanced:
                entries = self._balanced_sample(batch_size)
            else:
                # 按重要性权重采样
                import random as _random
                weighted = list(self._buffer)
                weights = [e.importance_weight for e in weighted]
                total_w = sum(weights)
                probs = [w / total_w for w in weights]
                
                indices = _random.choices(
                    range(len(weighted)),
                    weights=probs,
                    k=min(batch_size, len(weighted)),
                )
                seen_idx = set()
                entries = []
                for idx in indices:
                    if idx not in seen_idx:
                        seen_idx.add(idx)
                        entries.append(weighted[idx])
            
            if not entries:
                return None
            
            # 标记已消费并更新统计
            for entry in entries:
                entry.replay_count += 1
                entry.last_replayed = time.time()
                entry.importance_weight *= self.config.decay_factor
            self._total_replays += 1
            
            # 统计分布
            dist: Dict[str, int] = {}
            hv = fl = cd = 0
            for e in entries:
                s_name = e.source.name
                dist[s_name] = dist.get(s_name, 0) + 1
                if e.source == ReplaySource.LIBRARY_HIGH_VALUE:
                    hv += 1
                elif e.source == ReplaySource.LIBRARY_LOW_SCORE:
                    fl += 1
                elif e.source == ReplaySource.CROSS_DOMAIN:
                    cd += 1
            
            batch_id = f"RB_{datetime.now().strftime('%Y%m%d%H%M%S')}_{self._total_replays}"
            return ReplayBatch(
                batch_id=batch_id,
                entries=entries,
                total_entries=len(entries),
                high_value_count=hv,
                failure_count=fl,
                cross_domain_count=cd,
                source_distribution=dist,
            )

    def _balanced_sample(self, batch_size: int) -> List[ReplayEntry]:
        """平衡采样：确保各来源类型都有代表性"""
        import random as _random
        
        by_source: Dict[ReplaySource, List[ReplayEntry]] = {}
        for e in self._buffer:
            by_source.setdefault(e.source, []).append(e)
        
        entries = []
        per_source_max = max(1, batch_size // max(len(by_source), 1))
        
        # 每种来源至少取一个
        for source, source_list in by_source.items():
            sample = _random.sample(
                source_list,
                k=min(per_source_max, len(source_list))
            )
            entries.extend(sample)
        
        # 如果还不够，按权重补满
        if len(entries) < batch_size:
            remaining = [e for e in self._buffer if e not in entries]
            if remaining:
                needed = batch_size - len(entries)
                weights = [e.importance_weight for e in remaining]
                extra = _random.choices(remaining, weights=weights, k=needed)
                entries.extend(extra)
        
        _random.shuffle(entries)
        return entries[:batch_size]

    # ═══════════════════════════════════════════════════════════
    #  知识库(DomainNexus)经验迁移
    # ═══════════════════════════════════════════════════════════

    def extract_from_knowledge_base(
        self,
        knowledge_bridge=None,
        focus_tags: Optional[List[str]] = None,
    ) -> int:
        """
        从知识库(DomainNexus)提取知识模式作为学习经验。
        
        这是「藏书阁工作人员管理和迭代知识库」的学习通道：
        - 工作人员通过此接口将知识库中的方法论、策略模式
          注入到回放缓冲区，供学习系统吸收。
        
        Args:
            knowledge_bridge: 知识库桥接器实例
            focus_tags: 关注的标签（过滤用）
            
        Returns:
            提取的条目数
        """
        if knowledge_bridge is None:
            try:
                from intelligence.dispatcher.wisdom_dispatch._library_knowledge_bridge import LibraryKnowledgeBridge
                knowledge_bridge = LibraryKnowledgeBridge()
            except ImportError:
                logger.warning("[ReplayBuffer] 知识库桥接器不可用")
                return 0
        
        with self._lock:
            cells = knowledge_bridge.scan_knowledge_cells()
            count = 0
            
            for cell_id, record in cells.items():
                if len(self._buffer) >= self.config.max_size:
                    break
                
                # 标签过滤
                if focus_tags and not (record.tags & set(focus_tags)):
                    continue
                
                # 只提取激活次数较高的格子（有实践价值的知识）
                if record.activation_count < 1:
                    continue
                
                entry = ReplayEntry(
                    entry_id=f"rv_kb_{cell_id}",
                    source=ReplaySource.KNOWLEDGE_CELL,
                    source_cell_id=cell_id,
                    content=record.content[:600],
                    full_content=record.content,
                    grade="",  # 知识库没有甲乙丙丁分级
                    value_score=min(0.9, 0.5 + record.activation_count * 0.05),
                    importance_weight=1.2,
                    lesson_type="pattern",
                    tags=list(record.tags),
                    metadata={
                        "category": record.category,
                        "activation_count": record.activation_count,
                    },
                )
                self._buffer.append(entry)
                count += 1
            
            logger.info(f"[ReplayBuffer] 知识库提取: {count} 条")
            return count

    # ═══════════════════════════════════════════════════════════
    #  管理 & 统计
    # ═══════════════════════════════════════════════════════════

    def consume_entry(self, entry_id: str, feedback: str = "") -> bool:
        """
        标记一条回放条目为已消费（已被学习系统处理）。
        
        Args:
            entry_id: 条目ID
            feedback: 学习反馈（可选）
            
        Returns:
            是否成功标记
        """
        with self._lock:
            for entry in self._buffer:
                if entry.entry_id == entry_id:
                    entry.is_consumed = True
                    self._consumed_ids.add(entry_id)
                    if feedback:
                        entry.metadata["learning_feedback"] = feedback
                    logger.debug(f"[ReplayBuffer] 已消费: {entry_id}")
                    return True
            return False

    def clear_consumed(self) -> int:
        """清除已消费的条目，释放空间"""
        with self._lock:
            before = len(self._buffer)
            self._buffer = deque(
                (e for e in self._buffer if not e.is_consumed),
                maxlen=self.config.max_size
            )
            cleared = before - len(self._buffer)
            logger.info(f"[ReplayBuffer] 清除已消费: {cleared} 条")
            return cleared

    def add_entry(self, entry: "ReplayEntry") -> bool:
        """
        手动向缓冲区添加一条经验回放条目。
        
        Args:
            entry: ReplayEntry 数据
            
        Returns:
            是否添加成功（容量满时返回 False）
        """
        with self._lock:
            if len(self._buffer) >= self.config.max_size:
                logger.warning("[ReplayBuffer] 缓冲区已满，无法添加条目")
                return False
            self._buffer.append(entry)
            logger.debug(f"[ReplayBuffer] 手动添加: {entry.entry_id}")
            return True

    def get_statistics(self) -> Dict[str, Any]:
        """获取回放缓冲区统计信息"""
        with self._lock:
            source_counts: Dict[str, int] = {}
            lesson_counts: Dict[str, int] = {}
            total_importance = 0.0
            
            for e in self._buffer:
                src = e.source.name
                source_counts[src] = source_counts.get(src, 0) + 1
                lt = e.lesson_type
                lesson_counts[lt] = lesson_counts.get(lt, 0) + 1
                total_importance += e.importance_weight
            
            return {
                "buffer_size": len(self._buffer),
                "max_capacity": self.config.max_size,
                "utilization": round(len(self._buffer) / self.config.max_size, 3),
                "total_extracts": self._total_extracts,
                "total_replays": self._total_replays,
                "consumed_count": len(self._consumed_ids),
                "source_distribution": source_counts,
                "lesson_type_distribution": lesson_counts,
                "avg_importance": round(total_importance / max(len(self._buffer), 1), 3),
                "last_extract_time": self._last_extract_time,
            }


# ═══════════════════════════════════════════════════════════════
#  全局单例
# ═══════════════════════════════════════════════════════════════

_global_buffer: Optional[LearningReplayBuffer] = None


def get_replay_buffer(config: Optional[ReplayConfig] = None) -> LearningReplayBuffer:
    """获取全局回放缓冲区实例"""
    global _global_buffer
    if _global_buffer is None:
        _global_buffer = LearningReplayBuffer(config)
    return _global_buffer


__all__ = [
    'ReplaySource',
    'ReplayEntry',
    'ReplayBatch',
    'ReplayConfig',
    'LearningReplayBuffer',
    'get_replay_buffer',
]
