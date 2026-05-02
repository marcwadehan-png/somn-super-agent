# -*- coding: utf-8 -*-
"""
藏书阁-知识格子桥接器 v2.0
_library_knowledge_bridge.py

将独立知识格子系统集成到藏书阁的统一架构中。
知识格子内容作为藏书阁的记忆来源之一（METHODOLOGY分类）。

主要功能:
  - 知识格子 → 藏书阁 CellRecord 转换
  - 藏书阁 → 知识格子 查询接口
  - 方法论检查集成
  - 推理增强接口

[v2.0 新增]
  - G-4: 知识库管理接口（创建/更新/归档/迭代格子）
  - G-5: 语义向量编码器集成（自动填充 semantic_embedding）
  - G-6: 自动跨域关联（基于标签/内容相似度）

版本: v6.2.0
更新: 2026-04-28
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
                from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import (
                    MemorySource, MemoryGrade, MemoryCategory, LibraryWing,
                )

                memory_data = {
                    "title": f"[知识格子] {record.cell_id}_{record.name}",
                    "content": record.content,
                    "category": MemoryCategory.METHODOLOGY,
                    "source": MemorySource.KNOWLEDGE_CELLS,
                    "grade": MemoryGrade.YI,
                    "tags": list(record.tags) + ["知识格子", record.category, cell_id],
                    "reporting_system": "knowledge_cells",
                }
                
                # 检查是否已存在
                existing = library.query_cells(tags=["knowledge_cells", cell_id], limit=1)
                if not existing:
                    library.submit_cell(
                        title=memory_data["title"],
                        content=memory_data["content"],
                        wing=LibraryWing.LEARN,
                        shelf="knowledge_sync",
                        grade=MemoryGrade.YI,
                        source=MemorySource.KNOWLEDGE_CELLS,
                        category=MemoryCategory.METHODOLOGY,
                        tags=memory_data["tags"],
                        reporting_system="knowledge_cells",
                    )
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

    def manage_knowledge_cell(
        self,
        action: str,
        cell_id: str = "",
        name: str = "",
        content: str = "",
        tags: Optional[List[str]] = None,
        category: str = "A",
        operator: str = "",
        reason: str = "",
        **kwargs,
    ) -> Dict[str, Any]:
        """
        统一管理知识格子（创建/更新/归档）。
        
        Args:
            action: 操作类型 "create" / "update" / "archive"
            cell_id: 格子ID (如 "A1")
            name: 格子名称（create/update 时使用）
            content: 格子内容
            tags: 标签列表
            operator: 操作人
            reason: 原因（archive 时使用）
            
        Returns:
            操作结果字典
        """
        if action == "create":
            return self.create_cell(
                cell_id=cell_id, name=name, content=content,
                tags=tags, category=category, operator=operator,
                **kwargs,
            )
        elif action == "update":
            return self.update_cell(
                cell_id=cell_id, content=content,
                tags=tags, operator=operator, **kwargs,
            )
        elif action == "archive":
            return self.archive_cell(
                cell_id=cell_id,
                reason=reason or "统一管理操作",
                operator=operator,
            )
        else:
            return {"error": f"未知操作: {action}", "cell_id": cell_id}

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

    # ═══════════════════════════════════════════════════════════════
    #  v2.0 G-4: 知识库管理接口（藏书阁工作人员管理格子用）
    # ═══════════════════════════════════════════════════════════════

    def create_cell(
        self,
        cell_id: str,
        title: str,
        content: str,
        category: str = "A",
        tags: Optional[List[str]] = None,
        operator: str = "",
    ) -> KnowledgeCellRecord:
        """
        创建新的知识格子 Markdown 文件。
        
        需要 WRITE 权限。由藏书阁工作人员调用。
        
        Args:
            cell_id: 格子ID (如 "D1", "E3")
            title: 格子名称
            content: Markdown 内容
            category: 分类前缀 (A=智慧核心, B=知识域策略, C=执行战术)
            tags: 标签列表
            operator: 操作者（用于权限记录）
            
        Returns:
            创建的 KnowledgeCellRecord
            
        Raises:
            FileExistsError: 如果格子文件已存在
            PermissionError: 如果操作者没有写权限
        """
        # 权限检查
        if operator:
            try:
                from ._library_staff_registry import get_staff_registry
                registry = get_staff_registry()
                if not registry.has_write_privilege(operator):
                    raise PermissionError(f"'{operator}' 没有知识库写权限")
            except ImportError:
                pass  # 注册表不可用时跳过检查
        
        file_path = self.cells_dir / f"{cell_id}.md"
        if file_path.exists():
            raise FileExistsError(f"知识格子已存在: {cell_id}")
        
        # 构建 Markdown 内容（含元信息区块）
        now_str = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
        meta_block = f"""<!-- 元信息 -->
激活次数：0
上次激活：{now_str}
标签：{', '.join(tags or [])}
创建者：{operator or 'system'}
<!-- /元信息 -->
"""
        full_content = f"# {cell_id} {title}\n\n{meta_block}\n\n{content}"
        
        # 写入文件
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(full_content, encoding="utf-8")
        
        record = KnowledgeCellRecord(
            cell_id=cell_id,
            name=title,
            category=category,
            tags=set(tags or []),
            content=full_content,
            metadata_block=meta_block,
        )
        self._cell_cache[cell_id] = record
        
        logger.info(f"[KnowledgeBridge] {operator} 创建了新格子: {cell_id} - {title}")
        return record

    def update_cell(
        self,
        cell_id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        operator: str = "",
        iteration_note: str = "",
    ) -> KnowledgeCellRecord:
        """
        更新现有知识格子的内容或标签。
        
        Args:
            cell_id: 目标格子 ID
            content: 新内容（None 则不更新内容）
            tags: 新标签列表（None 则不更新标签）
            operator: 操作者
            iteration_note: 迭代说明（会追加到文件末尾的迭代历史中）
            
        Returns:
            更新后的 KnowledgeCellRecord
            
        Raises:
            FileNotFoundError: 格子不存在
        """
        file_path = self.cells_dir / f"{cell_id}.md"
        if not file_path.exists():
            raise FileNotFoundError(f"知识格子不存在: {cell_id}")
        
        existing_content = file_path.read_text(encoding="utf-8")
        
        # 更新标签（修改元信息区块）
        if tags is not None:
            new_tags_str = ", ".join(tags)
            # 替换元信息中的标签行
            if "标签[：" in existing_content or "标签[:]" in existing_content:
                import re as _re
                existing_content = _re.sub(
                    r'标签[：:]\s*[^\n]*',
                    f'标签：{new_tags_str}',
                    existing_content
                )
        
        # 更新主体内容（保留元信息区块，替换后面的部分）
        if content is not None:
            # 找到 <!-- /元信息 --> 之后的内容并替换
            end_meta_marker = "<!-- /元信息 -->"
            if end_meta_marker in existing_content:
                meta_part = existing_content[:existing_content.index(end_meta_marker) + len(end_meta_marker)]
                
                # 追加迭代记录
                new_body = content
                if iteration_note:
                    now_str = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
                    iter_record = (
                        f"\n\n---\n\n"
                        f"> **迭代记录** | {now_str} | {operator or 'system'}\n>\n> {iteration_note}\n"
                    )
                    new_body += iter_record
                
                existing_content = meta_part + "\n\n" + new_body
        
        file_path.write_text(existing_content, encoding="utf-8")
        
        # 刷新缓存
        record = self.parse_knowledge_cell(file_path)
        if record:
            self._cell_cache[cell_id] = record
        
        logger.info(f"[KnowledgeBridge] {operator} 更新了格子: {cell_id}" + 
                     (f" - {iteration_note}" if iteration_note else ""))
        return record or self._cell_cache.get(cell_id)

    def archive_cell(self, cell_id: str, reason: str, operator: str = "") -> Dict[str, Any]:
        """
        归档知识格子（不删除，移至归档目录）。
        
        藏书阁原则：绝对禁止删除任何知识点。
        
        Args:
            cell_id: 要归档的格子 ID
            reason: 归档原因
            operator: 操作者
            
        Raises:
            FileNotFoundError: 格子不存在
        """
        file_path = self.cells_dir / f"{cell_id}.md"
        if not file_path.exists():
            raise FileNotFoundError(f"知识格子不存在: {cell_id}")
        
        archive_dir = self.cells_dir / "_archived"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        target_path = archive_dir / f"{cell_id}_{__import__('time').strftime('%Y%m%d_%H%M%S')}.md"
        file_path.rename(target_path)
        
        # 清除缓存
        self._cell_cache.pop(cell_id, None)
        
        result = {
            "cell_id": cell_id,
            "archived_to": str(target_path),
            "reason": reason,
            "operator": operator,
            "archived_at": __import__("time").time(),
        }
        logger.info(f"[KnowledgeBridge] {operator} 归档了格子: {cell_id} - {reason}")
        return result

    def iterate_cell(
        self, cell_id: str, iteration_note: str, operator: str = ""
    ) -> KnowledgeCellRecord:
        """
        迭代一个知识格子的版本（保留完整迭代历史）。
        
        这是知识库管理的核心操作——工作人员通过此接口持续改进知识格子。
        
        Args:
            cell_id: 目标格子
            iteration_note: 本次迭代的说明
            operator: 迭代者
            
        Returns:
            更新后的记录
        """
        return self.update_cell(
            cell_id=cell_id,
            content=None,  # 不改内容，只追加迭代记录
            tags=None,
            operator=operator,
            iteration_note=iteration_note,
        )

    # ═══════════════════════════════════════════════════════════════
    #  v2.0 G-5: 语义向量编码器
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def encode_semantic(content: str, dimension: int = 128) -> List[float]:
        """
        对文本进行语义编码生成向量。
        
        [v2.0 G-5] 委托给独立模块 _semantic_encoder.SemanticEncoder。
        此方法保留为兼容入口，内部调用 SemanticEncoder.encode()。
        
        Args:
            content: 输入文本
            dimension: 向量维度（建议 64/128/256/768）
            
        Returns:
            长度为 dimension 的浮点向量（L2 归一化）
        """
        try:
            # 委托给独立编码器模块
            from ._semantic_encoder import get_semantic_encoder, EncoderConfig
            encoder = get_semantic_encoder(
                config=EncoderConfig(dimension=dimension)
            )
            return encoder.encode(content)
        except ImportError:
            # 降级：如果独立模块不可用，使用内置后备实现
            import hashlib
            import math
            
            words = re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}', content.lower())
            word_freq: Dict[str, int] = {}
            for w in words:
                word_freq[w] = word_freq.get(w, 0) + 1
            
            vector = [0.0] * dimension
            for word, freq in word_freq.items():
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                idx1 = h % dimension
                idx2 = (h >> 8) % dimension
                idx3 = (h >> 16) % dimension
                
                weight = (1.0 + math.log(freq)) * (1.0 / (1.0 + math.log(len(words) / max(word_freq[word], 1))))
                vector[idx1] += weight
                vector[idx2] += weight * 0.5
                vector[idx3] += weight * 0.25
            
            norm = math.sqrt(sum(v * v for v in vector))
            if norm > 0:
                vector = [v / norm for v in vector]
            
            return vector

    def encode_cell_for_library(
        self, cell_record: KnowledgeCellRecord
    ) -> Optional[List[float]]:
        """为知识格子生成语义向量（供 CellRecord.semantic_embedding 使用）"""
        text = f"{cell_record.name} {cell_record.content}"
        return self.encode_semantic(text)

    # ═══════════════════════════════════════════════════════════════
    #  v2.0 G-6: 自动跨域关联
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """计算两个向量的余弦相似度"""
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def find_related_cells(
        self,
        cell_id: str,
        threshold: float = 0.3,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        为指定格子查找相关联的其他格子（用于自动跨域关联）。
        
        基于：
        1. 标签重叠度
        2. 语义向量余弦相似度
        3. 内容关键词匹配
        
        Args:
            cell_id: 源格子 ID
            threshold: 相似度阈值
            top_k: 返回最相关的 K 个
            
        Returns:
            相关格子列表 [{cell_id, score, reason}, ...]
        """
        source = self._cell_cache.get(cell_id)
        if not source:
            # 尝试从磁盘加载
            file_path = self.cells_dir / f"{cell_id}.md"
            if file_path.exists():
                source = self.parse_knowledge_cell(file_path)
                self._cell_cache[cell_id] = source
            else:
                return []
        
        cells = self.scan_knowledge_cells()
        candidates = []
        
        for cid, record in cells.items():
            if cid == cell_id:
                continue
            
            score = 0.0
            reasons = []
            
            # 1. 标签重叠
            tag_overlap = len(source.tags & record.tags)
            if tag_overlap > 0 and source.tags:
                tag_score = tag_overlap / max(len(source.tags), 1)
                score += tag_score * 0.4
                reasons.append(f"标签重合({tag_overlap})")
            
            # 2. 语义向量相似度
            vec_source = self.encode_semantic(source.content[:2000])
            vec_target = self.encode_semantic(record.content[:2000])
            sim = self.cosine_similarity(vec_source, vec_target)
            if sim >= 0.15:
                score += sim * 0.4
                if sim >= 0.3:
                    reasons.append(f"语义相似({sim:.2f})")
            
            # 3. 关键词匹配
            src_kw = set(re.findall(r'[\w]{2,}', source.content[:500]))
            tgt_kw = set(re.findall(r'[\w]{2,}', record.content[:500]))
            kw_overlap = len(src_kw & tgt_kw)
            if kw_overlap > 3:
                kw_score = min(kw_overlap * 0.05, 0.2)
                score += kw_score
                reasons.append(f"关键词重合({kw_overlap})")
            
            if score >= threshold:
                candidates.append({
                    "cell_id": cid,
                    "name": record.name,
                    "score": round(score, 4),
                    "reasons": reasons,
                })
        
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:top_k]

    def auto_cross_reference_all(self, library=None, threshold: float = 0.35) -> Dict[str, Any]:
        """
        对所有知识格子执行自动跨域关联。
        
        将结果写入藏书阁的 cross_references 字段。
        
        Args:
            library: 藏书阁实例（可选）
            threshold: 关联阈值
            
        Returns:
            统计信息
        """
        if library is None:
            try:
                from ._imperial_library import ImperialLibrary
                library = ImperialLibrary()
            except ImportError:
                return {"error": "藏书阁不可用"}
        
        cells = self.scan_knowledge_cells()
        total_links = 0
        
        for cell_id in cells:
            related = self.find_related_cells(cell_id, threshold=threshold)
            if related:
                ref_ids = [r["cell_id"] for r in related]
                # 在藏书阁中查找对应的 CellRecord 并更新 cross_references
                for ref_id in ref_ids:
                    # 构建可能的藏书阁 ID（格式：{WING}_{SHELF}_{SEQ}）
                    # 通过标签搜索找到对应记录
                    matching = library.query_cells(
                        keyword=ref_id, limit=3
                    )
                    for m in matching:
                        if ref_id in m.title or ref_id in m.content[:100]:
                            # 双向建立引用
                            library.add_cross_reference(m.id, f"kb_{cell_id}")
                            total_links += 1
        
        logger.info(f"[KnowledgeBridge] 自动跨域关联完成: {total_links} 条链接")
        return {
            "total_cells": len(cells),
            "cross_references_created": total_links,
            "threshold": threshold,
        }


# ═══════════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════════

_global_bridge: Optional["LibraryKnowledgeBridge"] = None


def get_knowledge_bridge(
    knowledge_cells_dir: Optional[str] = None,
) -> "LibraryKnowledgeBridge":
    """
    获取知识桥接器全局实例。
    
    Args:
        knowledge_cells_dir: 知识格子目录路径（可选）
        
    Returns:
        LibraryKnowledgeBridge 单例实例
    """
    global _global_bridge
    if _global_bridge is None:
        _global_bridge = LibraryKnowledgeBridge(
            knowledge_cells_dir=knowledge_cells_dir
        )
    return _global_bridge


# ═══════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════════

__all__ = [
    "LibraryKnowledgeBridge",
    "KnowledgeCellRecord",
    "MethodCheckResult",
    "KnowledgeQueryResult",
    "get_knowledge_bridge",
]
