# -*- coding: utf-8 -*-
"""
超级神经记忆系统 V5.0 - 贤者记忆集成
=====================================

整合贤者工程记忆能力：
1. 贤者记忆（768位贤者的智慧）
2. 蒸馏记忆（760份蒸馏文档）
3. Claw记忆（763个Claw的经验）
4. 协作记忆（多Claw协作历史）
5. 项目记忆（任务执行记忆）

核心能力：
- 四级记忆分级
- 语义检索
- 记忆联想
- 持续学习

[v20.0 升级] 使用统一 MemoryTier 枚举

版本: V5.0.0
创建: 2026-04-22
更新: 2026-04-23 (v20.0)
"""

import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import yaml

logger = logging.getLogger(__name__)

# 路径配置
PROJECT_ROOT = Path(__file__).resolve().parents[4]


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构 (使用统一类型系统)
# ═══════════════════════════════════════════════════════════════════════════════

# 使用统一的 MemoryTier (v20.0)
try:
    from src.neural_memory.memory_types import MemoryTier
except ImportError:
    # 兼容：若统一类型不可用，使用 V5 本地定义
    class MemoryTier(Enum):
        ETERNAL = "eternal"        # 永恒级 - 贤者智慧核心
        LONG_TERM = "long_term"    # 长期级 - 蒸馏知识
        WORKING = "working"        # 工作级 - 项目经验
        EPISODIC = "episodic"       # 情景级 - 临时交互


class MemorySource(Enum):
    """记忆来源"""
    SAGE = "sage"              # 贤者（wisdom_encoding）
    DISTILLATION = "distillation"  # 蒸馏文档
    CLAW = "claw"              # Claw子智能体
    COLLABORATION = "collaboration"  # 协作历史
    PROJECT = "project"        # 项目执行
    USER = "user"              # 用户交互


@dataclass
class MemoryEntry:
    """记忆条目"""
    entry_id: str
    tier: str
    source: str
    source_name: str           # 贤者名/Claw名/项目名
    
    # 内容
    content: str               # 核心内容
    summary: str               # 摘要
    keywords: List[str] = field(default_factory=list)
    
    # 元信息
    created_at: str = ""
    updated_at: str = ""
    access_count: int = 0
    last_accessed: str = ""
    
    # 关联
    related_entries: List[str] = field(default_factory=list)
    related_sages: List[str] = field(default_factory=list)
    related_schools: List[str] = field(default_factory=list)
    
    # 评分
    importance: float = 5.0     # 重要性 0-10
    utility: float = 5.0        # 实用性 0-10
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MemoryQuery:
    """记忆查询"""
    query_text: str
    tiers: List[MemoryTier] = field(default_factory=list)
    sources: List[MemorySource] = field(default_factory=list)
    related_sage: str = ""      # 关联特定贤者
    related_school: str = ""    # 关联特定学派
    min_importance: float = 0.0
    limit: int = 10


@dataclass
class MemoryResult:
    """记忆查询结果"""
    entries: List[MemoryEntry]
    total_count: int
    search_time: float
    suggestions: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# 超级神经记忆系统
# ═══════════════════════════════════════════════════════════════════════════════

class SuperNeuralMemory:
    """
    超级神经记忆系统 V5.0
    
    整合所有记忆源的超级记忆系统
    """
    
    def __init__(self):
        self._memories: Dict[str, MemoryEntry] = {}
        self._index_by_keyword: Dict[str, Set[str]] = {}
        self._index_by_sage: Dict[str, Set[str]] = {}
        self._index_by_school: Dict[str, Set[str]] = {}
        self._index_by_tier: Dict[str, Set[str]] = {}
        self._initialized = False
        self._init_lock = threading.Lock()
    
    def initialize(self) -> None:
        """初始化所有记忆源（线程安全）"""
        if self._initialized:
            return
        
        with self._init_lock:
            if self._initialized:
                return
            
            logger.info("[SuperNeuralMemory] 初始化超级神经记忆系统...")
        
            # 1. 加载贤者记忆
            self._load_sage_memories()
            
            # 2. 加载蒸馏记忆
            self._load_distillation_memories()
            
            # 3. 加载Claw记忆
            self._load_claw_memories()
            
            # 4. 加载协作记忆
            self._load_collaboration_memories()
            
            self._build_indexes()
            
            self._initialized = True
            logger.info(f"[SuperNeuralMemory] 初始化完成，共 {len(self._memories)} 条记忆")
    
    def _load_sage_memories(self) -> None:
        """加载贤者智慧记忆"""
        try:
            from .wisdom_encoding.wisdom_encoding_registry import COGNITIVE_DIMENSION_SCORES
            
            count = 0
            for sage_id, code_data in COGNITIVE_DIMENSION_SCORES.items():
                name = code_data.get("name", sage_id)
                
                # 构建记忆条目
                entry = MemoryEntry(
                    entry_id=f"sage_{sage_id}",
                    tier=MemoryTier.ETERNAL.value,
                    source=MemorySource.SAGE.value,
                    source_name=name,
                    content=str(code_data),
                    summary=f"{name}的智慧核心",
                    keywords=code_data.get("triggers", [])[:10],
                    created_at="2026-01-01",
                    importance=8.0,
                    utility=8.0,
                )
                
                self._memories[entry.entry_id] = entry
                count += 1
            
            logger.info(f"[SuperNeuralMemory] 加载了 {count} 条贤者记忆")
            
        except Exception as e:
            logger.warning(f"[SuperNeuralMemory] 贤者记忆加载失败: {e}")
    
    def _load_distillation_memories(self) -> None:
        """加载蒸馏文档记忆"""
        try:
            dist_dir = PROJECT_ROOT / "docs" / "蒸馏卷"
            
            if not dist_dir.exists():
                logger.warning(f"[SuperNeuralMemory] 蒸馏目录不存在: {dist_dir}")
                return
            
            count = 0
            for md_file in dist_dir.glob("**/*.md"):
                try:
                    # 读取文件前2000字符作为摘要
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read(2000)
                    
                    # 提取文件名作为名称
                    name = md_file.stem
                    
                    # 提取学派
                    school = md_file.parent.name
                    
                    entry = MemoryEntry(
                        entry_id=f"dist_{count:04d}",
                        tier=MemoryTier.LONG_TERM.value,
                        source=MemorySource.DISTILLATION.value,
                        source_name=name,
                        content=content,
                        summary=f"{name}的蒸馏知识",
                        keywords=[school],
                        related_schools=[school],
                        created_at="2026-01-01",
                        importance=7.0,
                        utility=7.0,
                    )
                    
                    self._memories[entry.entry_id] = entry
                    count += 1
                    
                except Exception as e:
                    logger.debug(f"count += 1失败: {e}")
            
            logger.info(f"[SuperNeuralMemory] 加载了 {count} 条蒸馏记忆")
            
        except Exception as e:
            logger.warning(f"[SuperNeuralMemory] 蒸馏记忆加载失败: {e}")
    
    def _load_claw_memories(self) -> None:
        """加载Claw记忆"""
        try:
            claw_configs_dir = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "claws" / "configs"
            
            if not claw_configs_dir.exists():
                logger.warning(f"[SuperNeuralMemory] Claw配置目录不存在")
                return
            
            count = 0
            for yaml_file in claw_configs_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                    
                    name = config.get("name", yaml_file.stem)
                    school = config.get("school", "")
                    triggers = config.get("triggers", [])
                    
                    entry = MemoryEntry(
                        entry_id=f"claw_{name}",
                        tier=MemoryTier.WORKING.value,
                        source=MemorySource.CLAW.value,
                        source_name=name,
                        content=str(config),
                        summary=f"{name}的配置和能力",
                        keywords=triggers[:10],
                        related_schools=[school],
                        created_at="2026-04-22",
                        importance=6.0,
                        utility=8.0,
                    )
                    
                    self._memories[entry.entry_id] = entry
                    count += 1
                    
                except Exception as e:
                    logger.debug(f"count += 1失败: {e}")
            
            logger.info(f"[SuperNeuralMemory] 加载了 {count} 条Claw记忆")
            
        except Exception as e:
            logger.warning(f"[SuperNeuralMemory] Claw记忆加载失败: {e}")
    
    def _load_collaboration_memories(self) -> None:
        """加载协作历史记忆"""
        # 从V3.0协作协议获取历史
        # 简化实现：预留接口
        logger.info("[SuperNeuralMemory] 协作记忆待初始化")
    
    def _build_indexes(self) -> None:
        """构建索引"""
        logger.info("[SuperNeuralMemory] 构建索引...")
        
        self._index_by_keyword.clear()
        self._index_by_sage.clear()
        self._index_by_school.clear()
        self._index_by_tier.clear()
        
        for entry_id, entry in self._memories.items():
            # 按层级
            if entry.tier not in self._index_by_tier:
                self._index_by_tier[entry.tier] = set()
            self._index_by_tier[entry.tier].add(entry_id)
            
            # 按关键词
            for kw in entry.keywords:
                kw_lower = kw.lower()
                if kw_lower not in self._index_by_keyword:
                    self._index_by_keyword[kw_lower] = set()
                self._index_by_keyword[kw_lower].add(entry_id)
            
            # 按贤者
            for sage in entry.related_sages:
                if sage not in self._index_by_sage:
                    self._index_by_sage[sage] = set()
                self._index_by_sage[sage].add(entry_id)
            
            # 按学派
            for school in entry.related_schools:
                if school not in self._index_by_school:
                    self._index_by_school[school] = set()
                self._index_by_school[school].add(entry_id)
        
        logger.info(f"[SuperNeuralMemory] 索引构建完成")
    
    # ── 核心方法 ─────────────────────────────────────────────────────────────
    
    def query(self, memory_query: MemoryQuery) -> MemoryResult:
        """
        查询记忆
        
        Args:
            memory_query: 记忆查询
            
        Returns:
            MemoryResult
        """
        import time
        start_time = time.time()
        
        self.initialize()
        
        # 1. 获取候选集合
        candidate_ids = None
        
        # 按关键词
        if memory_query.query_text:
            query_lower = memory_query.query_text.lower()
            keywords = query_lower.split()
            
            for kw in keywords:
                kw_matches = self._index_by_keyword.get(kw.lower(), set())
                if candidate_ids is None:
                    candidate_ids = kw_matches.copy()
                else:
                    candidate_ids &= kw_matches
        
        # 按贤者
        if memory_query.related_sage:
            sage_matches = self._index_by_sage.get(memory_query.related_sage, set())
            if candidate_ids is None:
                candidate_ids = sage_matches.copy()
            else:
                candidate_ids &= sage_matches
        
        # 按学派
        if memory_query.related_school:
            school_matches = self._index_by_school.get(memory_query.related_school, set())
            if candidate_ids is None:
                candidate_ids = school_matches.copy()
            else:
                candidate_ids &= school_matches
        
        # 按层级
        if memory_query.tiers:
            tier_matches = set()
            for tier in memory_query.tiers:
                tier_matches |= self._index_by_tier.get(tier.value, set())
            if candidate_ids is None:
                candidate_ids = tier_matches.copy()
            else:
                candidate_ids &= tier_matches
        
        # 按来源
        if memory_query.sources:
            source_matches = set()
            for entry_id, entry in self._memories.items():
                if entry.source in [s.value for s in memory_query.sources]:
                    source_matches.add(entry_id)
            if candidate_ids is None:
                candidate_ids = source_matches.copy()
            else:
                candidate_ids &= source_matches
        
        # 全量候选
        if candidate_ids is None:
            candidate_ids = set(self._memories.keys())
        
        # 2. 评分排序
        results = []
        for entry_id in candidate_ids:
            entry = self._memories[entry_id]
            
            # 过滤重要性
            if entry.importance < memory_query.min_importance:
                continue
            
            # 计算相关性分数
            score = self._calculate_relevance(entry, memory_query)
            
            results.append((entry, score))
        
        # 排序
        results.sort(key=lambda x: -x[1])
        
        # 3. 构建结果
        entries = [r[0] for r in results[:memory_query.limit]]
        
        # 生成建议
        suggestions = self._generate_suggestions(memory_query, entries)
        
        elapsed = time.time() - start_time
        
        return MemoryResult(
            entries=entries,
            total_count=len(results),
            search_time=elapsed,
            suggestions=suggestions,
        )
    
    def _calculate_relevance(
        self,
        entry: MemoryEntry,
        query: MemoryQuery,
    ) -> float:
        """计算相关性分数"""
        score = entry.importance * 0.3 + entry.utility * 0.3
        
        # 关键词匹配加分
        if query.query_text:
            query_lower = query.query_text.lower()
            for kw in entry.keywords:
                if kw.lower() in query_lower:
                    score += 1.0
        
        # 访问次数加权
        score += min(entry.access_count * 0.01, 1.0)
        
        return score
    
    def _generate_suggestions(
        self,
        query: MemoryQuery,
        results: List[MemoryEntry],
    ) -> List[str]:
        """生成搜索建议"""
        suggestions = []
        
        # 从结果中提取相关贤者
        sages = set()
        schools = set()
        for entry in results[:5]:
            sages.update(entry.related_sages)
            schools.update(entry.related_schools)
        
        # 生成建议
        for sage in list(sages)[:3]:
            suggestions.append(f"查看{sage}的更多智慧")
        
        for school in list(schools)[:2]:
            suggestions.append(f"探索{school}学派的智慧")
        
        return suggestions
    
    # ── 记忆写入 ─────────────────────────────────────────────────────────────
    
    def store(
        self,
        content: str,
        source: MemorySource,
        source_name: str,
        tier: MemoryTier = MemoryTier.EPISODIC,
        keywords: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """
        存储新记忆
        
        Args:
            content: 内容
            source: 来源
            source_name: 来源名
            tier: 层级
            keywords: 关键词
            metadata: 元数据
            
        Returns:
            entry_id
        """
        entry_id = f"{source.value}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        entry = MemoryEntry(
            entry_id=entry_id,
            tier=tier.value,
            source=source.value,
            source_name=source_name,
            content=content,
            summary=content[:200],
            keywords=keywords or [],
            created_at=datetime.now().isoformat(),
            importance=metadata.get("importance", 5.0) if metadata else 5.0,
            utility=metadata.get("utility", 5.0) if metadata else 5.0,
        )
        
        self._memories[entry_id] = entry
        self._build_indexes()  # 重建索引
        
        return entry_id
    
    def remember(
        self,
        entry_id: str,
    ) -> Optional[MemoryEntry]:
        """
        访问记忆（更新访问计数）
        
        Args:
            entry_id: 记忆ID
            
        Returns:
            MemoryEntry
        """
        if entry_id in self._memories:
            entry = self._memories[entry_id]
            entry.access_count += 1
            entry.last_accessed = datetime.now().isoformat()
            return entry
        return None
    
    # ── 统计方法 ─────────────────────────────────────────────────────────────
    
    def get_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        self.initialize()
        
        tier_counts = {}
        source_counts = {}
        
        for entry in self._memories.values():
            tier_counts[entry.tier] = tier_counts.get(entry.tier, 0) + 1
            source_counts[entry.source] = source_counts.get(entry.source, 0) + 1
        
        return {
            "total_memories": len(self._memories),
            "by_tier": tier_counts,
            "by_source": source_counts,
            "keywords_indexed": len(self._index_by_keyword),
            "sages_indexed": len(self._index_by_sage),
            "schools_indexed": len(self._index_by_school),
        }
    
    def get_related_memories(
        self,
        entry_id: str,
        limit: int = 5,
    ) -> List[MemoryEntry]:
        """获取相关记忆"""
        if entry_id not in self._memories:
            return []
        
        entry = self._memories[entry_id]
        
        # 构建查询
        query = MemoryQuery(
            query_text="",
            related_sage=entry.source_name if entry.source == "sage" else "",
            related_school=entry.related_schools[0] if entry.related_schools else "",
            limit=limit + 1,
        )
        
        result = self.query(query)
        
        # 排除自己
        return [e for e in result.entries if e.entry_id != entry_id][:limit]


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

_memory: Optional[SuperNeuralMemory] = None

def get_super_memory() -> SuperNeuralMemory:
    """获取全局超级记忆实例"""
    global _memory
    if _memory is None:
        _memory = SuperNeuralMemory()
    return _memory


def recall(query: str, limit: int = 10) -> List[MemoryEntry]:
    """
    便捷记忆检索函数
    
    Args:
        query: 查询文本
        limit: 返回数量
        
    Returns:
        MemoryEntry列表
    """
    memory = get_super_memory()
    result = memory.query(MemoryQuery(query_text=query, limit=limit))
    return result.entries


__all__ = [
    "SuperNeuralMemory",
    "MemoryTier",
    "MemorySource",
    "MemoryEntry",
    "MemoryQuery",
    "MemoryResult",
    "get_super_memory",
    "recall",
]