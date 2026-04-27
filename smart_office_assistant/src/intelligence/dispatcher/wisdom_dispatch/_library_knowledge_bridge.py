# -*- coding: utf-8 -*-
"""
藏书阁-知识格子桥接器 v1.0
_library_knowledge_bridge.py

将独立知识格子系统集成到藏书阁的统一架构中。
知识格子内容作为藏书阁的记忆来源之一（METHODOLOGY分类）。

主要功能:
  - 知识格子 → 藏书阁 CellRecord 转换
  - 藏书阁 → 知识格子 查询接口
  - 方法论检查集成
  - 推理增强接口
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# 知识格子元信息正则
# ═══════════════════════════════════════════════════════════════════

META_BLOCK_PATTERN = re.compile(
    r"<!--\s*元信息\s*-->(.*?)<!--\s*/元信息\s*-->", 
    re.DOTALL | re.IGNORECASE
)

ACTIVATION_PATTERN = re.compile(r'激活次数[：:]\s*(\d+)')
LAST_ACTIVATION_PATTERN = re.compile(r'上次激活[：:]\s*(.+)')
TAGS_PATTERN = re.compile(r'标签[：:]\s*(.+)')

# ═══════════════════════════════════════════════════════════════════
# 知识类别映射
# ═══════════════════════════════════════════════════════════════════

# 藏书阁书架 → 知识格子前缀映射
CELL_PREFIX_TO_SHELF: Dict[str, str] = {
    "A": "methodology_core",      # 智慧核心方法论
    "B": "strategy_operations",    # 运营策略
    "C": "execution_tactics",     # 执行战术
}

# ═══════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════


@dataclass
class KnowledgeCellRecord:
    """知识格子记录"""
    cell_id: str           # e.g. "A1", "B2"
    name: str              # 格子名称
    category: str          # 分类前缀
    activation_count: int = 0
    last_activation: str = ""
    tags: Set[str] = field(default_factory=set)
    related_cells: List[str] = field(default_factory=list)
    content: str = ""
    metadata_block: str = ""


@dataclass
class MethodCheckResult:
    """方法论检查结果"""
    passed: bool
    score: float
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    matched_methodologies: List[str] = field(default_factory=list)


@dataclass
class KnowledgeQueryResult:
    """知识查询结果"""
    question: str
    fused_answer: str
    related_cells: List[Dict[str, Any]] = field(default_factory=list)
    methodology_score: float = 0.0
    suggestions: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════
# 藏书阁知识桥接器
# ═══════════════════════════════════════════════════════════════════


class LibraryKnowledgeBridge:
    """
    藏书阁-知识格子桥接器
    
    将独立知识格子内容集成到藏书阁的统一架构中：
    1. 读取知识格子 Markdown 文件
    2. 转换为 CellRecord 存入藏书阁
    3. 提供知识查询接口
    4. 提供方法论检查接口
    """
    
    # 默认知识格子目录
    DEFAULT_KNOWLEDGE_CELLS_DIR = "knowledge_cells"
    
    def __init__(
        self,
        knowledge_cells_dir: Optional[str] = None
    ):
        """
        Args:
            knowledge_cells_dir: 知识格子目录路径
        """
        self.project_root = self._find_project_root()
        self.cells_dir = Path(
            knowledge_cells_dir or self.DEFAULT_KNOWLEDGE_CELLS_DIR
        )
        if not self.cells_dir.is_absolute():
            self.cells_dir = self.project_root / self.cells_dir
        
        # 缓存
        self._cell_cache: Dict[str, KnowledgeCellRecord] = {}
        
        logger.info(f"[KnowledgeBridge] 初始化，格子目录: {self.cells_dir}")
    
    @staticmethod
    def _find_project_root() -> Path:
        """查找项目根目录"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "smart_office_assistant").exists():
                return parent
            if (parent / "src").exists():
                return parent
        return current.parent.parent.parent
    
    # ──────────────────────────────────────────────────────────
    #  知识格子读取
    # ──────────────────────────────────────────────────────────
    
    def parse_knowledge_cell(self, file_path: Path) -> Optional[KnowledgeCellRecord]:
        """
        解析知识格子 Markdown 文件
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # 提取格子ID和名称
            filename = file_path.stem
            cell_id = filename.split("_")[0] if "_" in filename else filename
            
            # 解析元信息区块
            meta_block = ""
            meta_match = META_BLOCK_PATTERN.search(content)
            if meta_match:
                meta_block = meta_match.group(1).strip()
            
            # 解析元数据
            activation_count = 0
            last_activation = ""
            tags: Set[str] = set()
            
            if act_match := ACTIVATION_PATTERN.search(meta_block):
                activation_count = int(act_match.group(1))
            if last_match := LAST_ACTIVATION_PATTERN.search(meta_block):
                last_activation = last_match.group(1).strip()
            if tags_match := TAGS_PATTERN.search(meta_block):
                tags = set(
                    t.strip() 
                    for t in re.split(r'[,，]', tags_match.group(1)) 
                    if t.strip()
                )
            
            # 提取格子名称
            name = ""
            for line in content.split("\n"):
                if line.startswith("# ") and not name:
                    name = line[2:].strip()
                    name = re.sub(r'^[A-Z]\d[_-]\s*', '', name)
                    break
            
            # 确定分类
            category = cell_id[0] if cell_id else "A"
            
            return KnowledgeCellRecord(
                cell_id=cell_id,
                name=name,
                category=category,
                activation_count=activation_count,
                last_activation=last_activation,
                tags=tags,
                content=content,
                metadata_block=meta_block
            )
            
        except Exception as e:
            logger.error(f"[KnowledgeBridge] 解析格子失败 {file_path}: {e}")
            return None
    
    def scan_knowledge_cells(self) -> Dict[str, KnowledgeCellRecord]:
        """扫描所有知识格子文件"""
        cells: Dict[str, KnowledgeCellRecord] = {}
        
        if not self.cells_dir.exists():
            logger.warning(f"[KnowledgeBridge] 格子目录不存在: {self.cells_dir}")
            return cells
        
        for md_file in self.cells_dir.glob("*.md"):
            filename = md_file.stem
            if not re.match(r'^[A-Z]\d', filename):
                continue
            
            record = self.parse_knowledge_cell(md_file)
            if record:
                cells[record.cell_id] = record
                self._cell_cache[record.cell_id] = record
        
        logger.info(f"[KnowledgeBridge] 扫描到 {len(cells)} 个知识格子")
        return cells
    
    # ──────────────────────────────────────────────────────────
    #  藏书阁同步
    # ──────────────────────────────────────────────────────────
    
    def sync_to_library(self, library=None) -> Dict[str, Any]:
        """
        将所有知识格子同步到藏书阁
        
        Args:
            library: 藏书阁实例（可选）
            
        Returns:
            同步结果统计
        """
        # 延迟导入藏书阁
        if library is None:
            try:
                from ._imperial_library import ImperialLibrary
                library = ImperialLibrary()
            except Exception as e:
                logger.error(f"[KnowledgeBridge] 无法导入藏书阁: {e}")
                return {"error": str(e)}
        
        cells = self.scan_knowledge_cells()
        synced = 0
        skipped = 0
        
        for cell_id, record in cells.items():
            try:
                # 确定目标书架
                shelf = CELL_PREFIX_TO_SHELF.get(
                    record.category, "methodology_core"
                )
                
                # 准备记忆数据
                memory_data = {
                    "title": f"[知识格子] {record.cell_id}_{record.name}",
                    "content": record.content,
                    "category": "METHODOLOGY",
                    "source": "KNOWLEDGE_CELLS",
                    "grade": "YI",
                    "tags": list(record.tags) + ["知识格子", record.category, cell_id],
                    "reporting_system": "knowledge_cells",
                }
                
                # 检查是否已存在
                existing = library.get_cells(tags=["knowledge_cells", cell_id])
                if not existing:
                    library.submit_memory(**memory_data)
                    synced += 1
                else:
                    skipped += 1
                    
            except Exception as e:
                logger.error(f"[KnowledgeBridge] 同步格子失败 {cell_id}: {e}")
        
        result = {
            "total": len(cells),
            "synced": synced,
            "skipped": skipped,
        }
        logger.info(f"[KnowledgeBridge] 同步完成: {result}")
        return result
    
    # ──────────────────────────────────────────────────────────
    #  知识查询
    # ──────────────────────────────────────────────────────────
    
    def query_knowledge(self, question: str) -> KnowledgeQueryResult:
        """查询知识并返回融合答案"""
        cells = self.scan_knowledge_cells()
        keywords = self._extract_keywords(question)
        
        related = []
        for cell_id, record in cells.items():
            score = self._calculate_relevance(record, keywords)
            if score > 0:
                related.append({
                    "cell_id": cell_id,
                    "name": record.name,
                    "score": score,
                    "content": record.content[:500],
                })
        
        related = sorted(related, key=lambda x: x["score"], reverse=True)[:5]
        fused = self._fuse_answer(question, related)
        methodology_score = self._score_methodology(question + fused)
        
        return KnowledgeQueryResult(
            question=question,
            fused_answer=fused,
            related_cells=related,
            methodology_score=methodology_score,
            suggestions=self._generate_suggestions(related)
        )
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """提取关键词"""
        words = re.findall(r'[\w]{2,}', text)
        stopwords = {"的", "是", "在", "了", "和", "与", "如何", "怎么", "什么"}
        return {w for w in words if w not in stopwords}
    
    def _calculate_relevance(
        self, 
        record: KnowledgeCellRecord, 
        keywords: Set[str]
    ) -> float:
        """计算相关性分数"""
        score = 0.0
        
        name_words = set(re.findall(r'[\w]{2,}', record.name))
        score += len(keywords & name_words) * 0.5
        
        score += len(keywords & record.tags) * 0.3
        
        content_words = set(re.findall(r'[\w]{2,}', record.content[:1000]))
        score += len(keywords & content_words) * 0.2
        
        return score
    
    def _fuse_answer(self, question: str, related: List[Dict]) -> str:
        """融合多个格子生成答案"""
        if not related:
            return "未找到相关知识格子。"
        
        parts = [f"根据 {len(related)} 个相关知识格子：\n"]
        
        for i, cell in enumerate(related, 1):
            parts.append(f"{i}. **{cell['name']}** (相关度: {cell['score']:.2f})")
            content = cell.get('content', '')
            paras = [p.strip() for p in content.split('\n\n') if p.strip()]
            if len(paras) > 1:
                parts.append(f"   {paras[1][:200]}...")
            parts.append("")
        
        return "\n".join(parts)
    
    def _score_methodology(self, text: str) -> float:
        """评分方法论完整度"""
        score = 0.0
        keywords = {
            "框架": 0.2, "方法": 0.15, "步骤": 0.15,
            "数据": 0.2, "分析": 0.15, "结论": 0.15,
        }
        text_lower = text.lower()
        for kw, w in keywords.items():
            if kw in text_lower:
                score += w
        return min(score, 1.0)
    
    def _generate_suggestions(self, related: List[Dict]) -> List[str]:
        """生成建议"""
        suggestions = []
        if len(related) < 3:
            suggestions.append("建议扩展相关知识域")
        if related:
            suggestions.append(f"可深入学习: {related[0]['name']}")
        return suggestions
    
    # ──────────────────────────────────────────────────────────
    #  方法论检查
    # ──────────────────────────────────────────────────────────
    
    def check_methodology(self, content: str) -> MethodCheckResult:
        """检查内容是否符合方法论"""
        issues = []
        suggestions = []
        matched = []
        
        has_framework = any(k in content for k in ["框架", "结构", "层次"])
        if not has_framework:
            issues.append("缺少框架/结构描述")
            suggestions.append("建议先建立分析框架")
        
        has_data = any(k in content for k in ["数据", "指标", "数字", "%", "率"])
        if not has_data:
            issues.append("缺少数据支撑")
            suggestions.append("建议补充具体数据和指标")
        
        has_conclusion = any(k in content for k in ["结论", "建议", "因此", "所以"])
        if not has_conclusion:
            issues.append("缺少明确结论")
            suggestions.append("建议添加结论性表述")
        
        cells = self.scan_knowledge_cells()
        keywords = self._extract_keywords(content)
        for cell_id, record in cells.items():
            score = self._calculate_relevance(record, keywords)
            if score > 0.5:
                matched.append(f"{record.cell_id}_{record.name}")
        
        score = 1.0
        if not has_framework:
            score -= 0.3
        if not has_data:
            score -= 0.3
        if not has_conclusion:
            score -= 0.2
        
        return MethodCheckResult(
            passed=len(issues) == 0,
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            matched_methodologies=matched[:5]
        )
    
    # ──────────────────────────────────────────────────────────
    #  统计
    # ──────────────────────────────────────────────────────────
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        cells = self.scan_knowledge_cells()
        total_activation = sum(c.activation_count for c in cells.values())
        
        return {
            "total_cells": len(cells),
            "total_activations": total_activation,
            "cells_by_category": {
                cat: sum(1 for c in cells.values() if c.category == cat)
                for cat in ["A", "B", "C"]
            },
            "cells_directory": str(self.cells_dir),
        }


# ═══════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════════

__all__ = [
    "LibraryKnowledgeBridge",
    "KnowledgeCellRecord",
    "MethodCheckResult",
    "KnowledgeQueryResult",
]
