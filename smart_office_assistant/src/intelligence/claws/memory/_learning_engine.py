# Claw记忆驱动学习引擎
# v3.3.0: 记忆驱动学习核心实现
# 动态格子→按需创建 | 关联度→自动连接 | 长term→精选沉淀

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from ._dynamic_cells import DynamicMemorySystem, CellMeta

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 长期记忆管理
# ═══════════════════════════════════════════════════════════════════

class LongTermMemory:
    """
    长期记忆管理器
    
    长term → 精选沉淀
    从动态格子中精选内容沉淀为长期记忆
    """
    
    LONGEVITY_THRESHOLD = 30  # 天数阈值
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.longterm_file = memory_dir / "longterm.md"
        self._entries: List[Dict[str, Any]] = []
        self._load()
    
    def _load(self) -> None:
        """加载长期记忆"""
        if self.longterm_file.exists():
            try:
                content = self.longterm_file.read_text(encoding="utf-8")
                # 简单解析
                self._entries = []
            except Exception as e:
                logger.warning(f"[LongTermMemory] 加载失败: {e}")
    
    def _save(self) -> None:
        """保存长期记忆"""
        md = "# 长期记忆精选\n\n"
        md += f"_更新时间: {datetime.now().strftime('%Y-%m-%d')}_\n\n"
        
        for entry in self._entries:
            md += f"## {entry['title']}\n"
            md += f"- 来源: {entry.get('source', 'N/A')}\n"
            md += f"- 精选时间: {entry.get('精选时间', 'N/A')}\n\n"
            md += f"{entry.get('content', '')}\n\n"
            md += "---\n\n"
        
        self.longterm_file.write_text(md, encoding="utf-8")
    
    def consolidate_from_cell(
        self,
        cell: CellMeta,
        content: str,
        title: Optional[str] = None
    ) -> None:
        """
        从格子精选内容沉淀到长期记忆
        
        Args:
            cell: 格子元信息
            content: 格子内容
            title: 自定义标题
        """
        # 检查是否满足精选条件
        if cell.activated < 5:
            logger.info(f"[LongTermMemory] {cell.cell_id}激活次数不足，跳过精选")
            return
        
        # 检查是否已存在
        for entry in self._entries:
            if entry.get("cell_id") == cell.cell_id:
                logger.info(f"[LongTermMemory] {cell.cell_id}已存在，跳过")
                return
        
        entry = {
            "cell_id": cell.cell_id,
            "title": title or cell.name,
            "content": content[:500],  # 保留前500字
            "source": f"格子{cell.cell_id}",
            "精选时间": datetime.now().strftime("%Y-%m-%d"),
            "activation_count": cell.activated
        }
        
        self._entries.append(entry)
        self._save()
        logger.info(f"[LongTermMemory] 精选格子{cell.cell_id}到长期记忆")
    
    def get_insights(self) -> List[str]:
        """获取长期记忆中的洞察"""
        return [e["title"] for e in self._entries]
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索长期记忆"""
        results = []
        for entry in self._entries:
            if keyword in entry.get("title", "") or keyword in entry.get("content", ""):
                results.append(entry)
        return results


# ═══════════════════════════════════════════════════════════════════
# 关联度引擎
# ═══════════════════════════════════════════════════════════════════

class CorrelationEngine:
    """
    关联度计算引擎
    
    关联度 → 自动连接
    根据内容相似度自动建立格子间的连接
    """
    
    MIN_CORRELATION = 0.3   # 最小关联度阈值
    MERGE_THRESHOLD = 0.85  # 合并阈值
    
    def __init__(self, memory_system: DynamicMemorySystem):
        self.memory = memory_system
    
    def calculate_correlation(
        self,
        cell1: CellMeta,
        cell2: CellMeta
    ) -> float:
        """
        计算两个格子的关联度
        
        Args:
            cell1: 格子1
            cell2: 格子2
            
        Returns:
            float: 关联度 0.0-1.0
        """
        # 基于标签计算
        tags1 = set(cell1.tags)
        tags2 = set(cell2.tags)
        
        if not tags1 or not tags2:
            return 0.0
        
        # Jaccard相似度
        intersection = len(tags1 & tags2)
        union = len(tags1 | tags2)
        
        if union == 0:
            return 0.0
        
        jaccard = intersection / union
        
        # 基于名称相似度
        name_sim = 0.0
        if cell1.name and cell2.name:
            common_chars = set(cell1.name) & set(cell2.name)
            name_sim = len(common_chars) / max(len(cell1.name), len(cell2.name))
        
        # 综合关联度
        correlation = jaccard * 0.7 + name_sim * 0.3
        
        logger.debug(
            f"[Correlation] {cell1.cell_id} vs {cell2.cell_id}: "
            f"tags={jaccard:.2f}, name={name_sim:.2f} → {correlation:.2f}"
        )
        
        return correlation
    
    def auto_connect(self) -> int:
        """
        自动建立格子间的连接
        
        Returns:
            int: 新建立的连接数
        """
        cells = self.memory.list_cells()
        new_connections = 0
        
        for i, cell1 in enumerate(cells):
            for cell2 in cells[i+1:]:
                # 检查是否已有连接
                existing = self.memory.index.get_related(cell1.cell_id, min_corr=0.1)
                if any(t[0] == cell2.cell_id for t in existing):
                    continue
                
                # 计算关联度
                corr = self.calculate_correlation(cell1, cell2)
                
                # 建立连接
                if corr >= self.MIN_CORRELATION:
                    self.memory.add_connection(
                        cell1.cell_id,
                        cell2.cell_id,
                        corr
                    )
                    new_connections += 1
                    logger.info(
                        f"[Correlation] 连接 {cell1.cell_id} ↔ {cell2.cell_id}: {corr:.2f}"
                    )
        
        return new_connections
    
    def find_merge_candidates(self) -> List[Tuple[str, str]]:
        """
        查找可能需要合并的格子
        
        Returns:
            List[Tuple[str, str]]: 需要合并的格子对
        """
        cells = self.memory.list_cells()
        candidates = []
        
        for i, cell1 in enumerate(cells):
            for cell2 in cells[i+1:]:
                corr = self.calculate_correlation(cell1, cell2)
                if corr >= self.MERGE_THRESHOLD:
                    candidates.append((cell1.cell_id, cell2.cell_id))
        
        return candidates


# ═══════════════════════════════════════════════════════════════════
# 按需创建引擎
# ═══════════════════════════════════════════════════════════════════

class OnDemandCreator:
    """
    按需创建引擎
    
    动态格子 → 按需创建
    根据查询需要动态创建新格子
    """
    
    # 常见领域的默认标签
    DEFAULT_TAGS = {
        "营销": ["营销", "增长", "推广"],
        "运营": ["运营", "管理", "流程"],
        "策略": ["策略", "战略", "规划"],
        "教育": ["教育", "教学", "培训"],
        "技术": ["技术", "开发", "架构"],
    }
    
    def __init__(self, memory_system: DynamicMemorySystem):
        self.memory = memory_system
    
    def find_or_create(
        self,
        query: str,
        context: Optional[str] = None
    ) -> str:
        """
        查找或创建格子
        
        Args:
            query: 查询内容
            context: 上下文
            
        Returns:
            str: 格子ID
        """
        # 1. 尝试查找现有格子
        existing = self._find_existing(query)
        if existing:
            logger.info(f"[OnDemand] 找到现有格子: {existing}")
            return existing
        
        # 2. 提取关键词
        keywords = self._extract_keywords(query)
        
        # 3. 确定格子名称
        name = self._determine_name(keywords, context)
        
        # 4. 确定标签
        tags = self._determine_tags(keywords)
        
        # 5. 创建新格子
        cell_id = self.memory.create_cell(name, tags=tags)
        logger.info(f"[OnDemand] 创建新格子: {cell_id} - {name}")
        
        return cell_id
    
    def _find_existing(self, query: str) -> Optional[str]:
        """查找现有格子"""
        query_lower = query.lower()
        
        for cell in self.memory.list_cells():
            if cell.name.lower() in query_lower:
                return cell.cell_id
            if any(t.lower() in query_lower for t in cell.tags):
                return cell.cell_id
        
        return None
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 简单实现：基于常见词
        keywords = []
        
        for default, tags in self.DEFAULT_TAGS.items():
            if any(t in query for t in tags):
                keywords.append(default)
        
        return keywords or ["其他"]
    
    def _determine_name(self, keywords: List[str], context: Optional[str]) -> str:
        """确定格子名称"""
        if context:
            return context
        
        if keywords:
            return keywords[0]
        
        return "新领域"
    
    def _determine_tags(self, keywords: List[str]) -> List[str]:
        """确定标签"""
        tags = []
        
        for kw in keywords:
            if kw in self.DEFAULT_TAGS:
                tags.extend(self.DEFAULT_TAGS[kw])
            else:
                tags.append(kw)
        
        return tags


# ═══════════════════════════════════════════════════════════════
# 记忆驱动学习主引擎
# ═══════════════════════════════════════════════════════════════

class LearningEngine:
    """
    记忆驱动学习主引擎
    
    整合动态格子、关联度、长期记忆
    """
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.memory = DynamicMemorySystem(memory_dir)
        self.longterm = LongTermMemory(memory_dir)
        self.correlation = CorrelationEngine(self.memory)
        self.creator = OnDemandCreator(self.memory)
        
        logger.info(f"[LearningEngine] 初始化完成: {memory_dir}")
    
    def learn(
        self,
        query: str,
        context: Optional[str] = None,
        auto_connect: bool = True
    ) -> Dict[str, Any]:
        """
        执行记忆驱动学习
        
        Args:
            query: 学习内容
            context: 上下文（仅用于日志，不作为格子名称）
            auto_connect: 是否自动建立连接
            
        Returns:
            Dict: 学习结果
        """
        # 1. 按需创建或查找格子（只用query作为名称，避免文件名过长）
        cell_id = self.creator.find_or_create(query)
        
        # 2. 激活格子
        self.memory.activate(cell_id, reason=f"学习: {query[:50]}")
        
        # 3. 自动建立连接
        connections_made = 0
        if auto_connect:
            connections_made = self.correlation.auto_connect()
        
        # 4. 检查是否需要精选到长期记忆
        cell = self.memory.get_cell(cell_id)
        if cell and cell.activated >= 10:
            self.longterm.consolidate_from_cell(
                cell,
                f"从查询'{query}'学习的内容",
                title=cell.name
            )
        
        return {
            "cell_id": cell_id,
            "activated": cell.activated if cell else 0,
            "connections_made": connections_made,
            "consolidated": cell.activated >= 10 if cell else False
        }
    
    def retrieve(
        self,
        query: str,
        min_corr: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        检索记忆
        
        Args:
            query: 查询内容
            min_corr: 最小关联度
            
        Returns:
            List[Dict]: 相关格子列表
        """
        # 1. 查找相关格子
        cell_id = self.creator._find_existing(query)
        
        if not cell_id:
            return []
        
        related = self.memory.get_related(cell_id, min_corr)
        
        results = []
        for rid, corr in related:
            cell = self.memory.get_cell(rid)
            if cell:
                results.append({
                    "cell_id": rid,
                    "name": cell.name,
                    "correlation": corr,
                    "activated": cell.activated
                })
        
        return results
    
    def consolidate(self) -> Dict[str, Any]:
        """
        执行记忆巩固
        
        Returns:
            Dict: 巩固结果
        """
        # 1. 自动建立连接
        connections = self.correlation.auto_connect()
        
        # 2. 查找合并候选
        merge_candidates = self.correlation.find_merge_candidates()
        
        # 3. 精选到长期记忆
        cells = self.memory.list_cells()
        for cell in cells:
            if cell.activated >= 10:
                self.longterm.consolidate_from_cell(
                    cell,
                    f"格子{cell.cell_id}的激活记忆",
                    title=cell.name
                )
        
        return {
            "connections_established": connections,
            "merge_candidates": len(merge_candidates),
            "longterm_entries": len(self.longterm._entries)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        cells = self.memory.list_cells()
        
        return {
            "total_cells": len(cells),
            "wisdom_cells": len([c for c in cells if c.cell_type == "wisdom_core"]),
            "knowledge_cells": len([c for c in cells if c.cell_type == "knowledge"]),
            "longterm_entries": len(self.longterm._entries),
            "most_activated": max([c.activated for c in cells]) if cells else 0
        }


# ═══════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════

__all__ = [
    "LongTermMemory",
    "CorrelationEngine", 
    "OnDemandCreator",
    "LearningEngine",
]