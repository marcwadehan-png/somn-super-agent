# Claw动态格子记忆系统
# 版本: v3.3.0
# 源自D:\open/memory/_cell_system.md设计

from __future__ import annotations

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════════════

class CellType(Enum):
    """格子类型"""
    WISDOM_CORE = "wisdom_core"     # 智慧核心格
    KNOWLEDGE = "knowledge"        # 知识域格
    PROJECT = "project"           # 项目格
    ARCHIVE = "archive"          # 归档格


class LearnDepth(Enum):
    """学习深度"""
    INITIAL = "initial"      # 初学
    UNDERSTAND = "understand"  # 理解
    MASTER = "master"         # 掌握
    EXPERT = "expert"        # 精通


# ═══════════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════════

@dataclass
class CellMeta:
    """格子元信息"""
    cell_id: str = ""
    name: str = ""
    cell_type: str = "knowledge"
    created: str = ""           # YYYY-MM-DD
    updated: str = ""           # YYYY-MM-DD
    activated: int = 0         # 激活次数
    depth: str = "initial"      # 学习深度
    connections: int = 0      # 连接数
    last_activation: Optional[str] = None  # 上次激活时间
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CellMeta":
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class CellContent:
    """格子内容"""
    cell_id: str = ""
    name: str = ""
    
    # 核心摘要
    summary: str = ""          # 用自己的话总结
    key_points: List[str] = field(default_factory=list)  # 核心要点3-5条
    my_view: str = ""          # 我怎么看
    
    # 详细笔记
    sources: List[str] = field(default_factory=list)  # 来源资料
    understanding: str = ""   # 我的理解
    cases: List[str] = field(default_factory=list)   # 案例
    
    # 思维模型
    thinking_model: str = ""  # 核心思维框架
    usage: str = ""           # 怎么用
    
    # 待探索
    questions: List[str] = field(default_factory=list)  # 疑问
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CellContent":
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class Connection:
    """格子连接"""
    target_id: str = ""
    correlation: float = 0.0   # 0.0-1.0
    last_updated: str = ""


# ══════��════════════════════════════════════════════════════════════
# 索引管理
# ═══════════════════════════════════════════════════════════════════

class CellsIndex:
    """格子索引管理器"""
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.cells_dir = memory_dir / "cells"
        self.cells_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_file = memory_dir / "cells_index.json"
        self.connections_file = memory_dir / "connections.json"
        
        self._cells: Dict[str, CellMeta] = {}
        self._connections: Dict[str, Dict[str, float]] = {}
        self._next_id = "A1"  # 下一个ID
        
        self._load()
    
    def _load(self) -> None:
        """加载索引"""
        # 加载cells_index.json
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for cid, cdata in data.get("cells", {}).items():
                        self._cells[cid] = CellMeta.from_dict(cdata)
                    self._next_id = data.get("next_cell_id", "A1")
            except Exception as e:
                logger.warning(f"[CellsIndex] 加载索引失败: {e}")
        
        # 加载connections.json
        if self.connections_file.exists():
            try:
                with open(self.connections_file, "r", encoding="utf-8") as f:
                    self._connections = json.load(f).get("connections", {})
            except Exception as e:
                logger.warning(f"[CellsIndex] 加载连接失败: {e}")
    
    def save(self) -> None:
        """保存索引"""
        # 保存cells_index
        index_data = {
            "version": "3.0",
            "cells": {cid: c.to_dict() for cid, c in self._cells.items()},
            "next_cell_id": self._next_id,
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        # 保存connections
        conn_data = {
            "connections": self._connections,
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        with open(self.connections_file, "w", encoding="utf-8") as f:
            json.dump(conn_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"[CellsIndex] 保存完成: {len(self._cells)}格子, {len(self._connections)}连接")
    
    def create_cell(
        self,
        name: str,
        cell_type: str = "knowledge",
        tags: Optional[List[str]] = None
    ) -> str:
        """创建新格子，返回cell_id"""
        cell_id = self._generate_id()
        
        # 清理文件名中的非法字符（v3.3.1修复）
        safe_name = self._sanitize_filename(name)
        
        meta = CellMeta(
            cell_id=cell_id,
            name=name,
            cell_type=cell_type,
            created=datetime.now().strftime("%Y-%m-%d"),
            updated=datetime.now().strftime("%Y-%m-%d"),
            tags=tags or [name]
        )
        
        self._cells[cell_id] = meta
        self._connections[cell_id] = {}
        
        # 保存内容文件（使用安全的文件名）
        content = CellContent(cell_id=cell_id, name=name)
        content_file = self.cells_dir / f"{cell_id}_{safe_name}.md"
        self._save_cell_content(content_file, content)
        
        self._next_id = self._generate_next_id()
        self.save()
        
        logger.info(f"[CellsIndex] 创建格子: {cell_id} - {name}")
        return cell_id
    
    def _generate_id(self) -> str:
        """生成格子ID"""
        return self._next_id
    
    def _sanitize_filename(self, name: str) -> str:
        r"""
        清理文件名中的非法字符（v3.3.1修复）
        
        Windows文件名字符限制：
        - 非法字符: \ / : * ? " < > |
        - 长度限制: 255字符
        """
        import re
        # 替换非法字符为下划线
        safe = re.sub(r'[\\/:*?"<>|]', '_', name)
        # 限制长度
        safe = safe[:100] if len(safe) > 100 else safe
        # 移除首尾空格和点
        safe = safe.strip(' .')
        # 如果为空，使用默认名
        if not safe:
            safe = "unnamed"
        return safe
    
    def _generate_next_id(self) -> str:
        """生成下一个ID"""
        prefix = self._next_id[0]
        num = int(self._next_id[1:]) + 1
        if num > 26:
            prefix = chr(ord(prefix) + 1)
            num = 1
        return f"{prefix}{num}"
    
    def _save_cell_content(self, path: Path, content: CellContent) -> None:
        """保存格子内容"""
        md = f"""# {content.cell_id}_{content.name}

## 元信息
- ID: {content.cell_id}
- 创建时间: {datetime.now().strftime('%Y-%m-%d')}
- 激活次数: 0

## 核心摘要
{content.summary}

## 详细笔记
{content.understanding}

## 关联格子
（自动生成）

## 思维模型
{content.thinking_model}

## 待探索
"""
        path.write_text(md, encoding="utf-8")
    
    def get_cell(self, cell_id: str) -> Optional[CellMeta]:
        """获取格子元信息"""
        return self._cells.get(cell_id)
    
    def list_cells(self, cell_type: Optional[str] = None) -> List[CellMeta]:
        """列出格子"""
        cells = list(self._cells.values())
        if cell_type:
            cells = [c for c in cells if c.cell_type == cell_type]
        return sorted(cells, key=lambda x: x.cell_id)
    
    def activate(self, cell_id: str) -> None:
        """激活格子"""
        if cell_id in self._cells:
            self._cells[cell_id].activated += 1
            self._cells[cell_id].last_activation = datetime.now().strftime("%Y-%m-%d")
            self.save()
            logger.info(f"[CellsIndex] 激活格子: {cell_id}")
    
    def get_related(self, cell_id: str, min_corr: float = 0.3) -> List[tuple]:
        """获取相关格子"""
        related = []
        if cell_id in self._connections:
            for tid, corr in self._connections[cell_id].items():
                if corr >= min_corr:
                    related.append((tid, corr))
        return sorted(related, key=lambda x: x[1], reverse=True)
    
    def add_connection(self, cell_id1: str, cell_id2: str, correlation: float) -> None:
        """添加连接"""
        if cell_id1 not in self._connections:
            self._connections[cell_id1] = {}
        if cell_id2 not in self._connections:
            self._connections[cell_id2] = {}
        
        self._connections[cell_id1][cell_id2] = correlation
        self._connections[cell_id2][cell_id1] = correlation
        
        # 更新连接数
        self._cells[cell_id1].connections = len(self._connections[cell_id1])
        self._cells[cell_id2].connections = len(self._connections[cell_id2])
        
        self.save()


# ═══════════════════════════════════════════════════════════════════
# 激活日志
# ═══════════════════════════════════════════════════════════════════

class ActivationLog:
    """激活日志"""
    
    def __init__(self, memory_dir: Path):
        self.log_file = memory_dir / "activation_log.md"
        self._entries: List[Dict[str, Any]] = []
        self._load()
    
    def _load(self) -> None:
        if self.log_file.exists():
            content = self.log_file.read_text(encoding="utf-8")
            # 简单解析markdown格式的日志
            for line in content.split("\n"):
                if line.startswith("## "):
                    date = line.replace("## ", "").strip()
    
    def log(self, cell_id: str, reason: str = "") -> None:
        """记录激活"""
        entry = {
            "cell_id": cell_id,
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }
        self._entries.append(entry)
        self._save()
    
    def _save(self) -> None:
        """保存日志"""
        md = "# Activation Log\n\n"
        for entry in self._entries[-100:]:  # 保留最近100条
            md += f"## {entry['timestamp']}\n"
            md += f"- Cell: {entry['cell_id']}\n"
            if entry['reason']:
                md += f"- Reason: {entry['reason']}\n"
        self.log_file.write_text(md, encoding="utf-8")
    
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._entries[-limit:]


# ═══════════════════════════════════════════════════════════════════
# 主系统整合
# ═══════════════════════════════════════════════════════════════════

class DynamicMemorySystem:
    """
    动态格子记忆系统主类
    
    用法:
    >>> memory = DynamicMemorySystem(Path("data/claws/RU_001/memory"))
    >>> cell_id = memory.create_cell("营销策略", tags=["营销", "增长"])
    >>> memory.activate(cell_id)
    >>> related = memory.get_related(cell_id)
    """
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.index = CellsIndex(memory_dir)
        self.log = ActivationLog(memory_dir)
        
        logger.info(f"[DynamicMemorySystem] 初始化: {memory_dir}")
    
    def create_cell(
        self,
        name: str,
        cell_type: str = "knowledge",
        tags: Optional[List[str]] = None
    ) -> str:
        """创建新格子"""
        return self.index.create_cell(name, cell_type, tags)
    
    def get_cell(self, cell_id: str) -> Optional[CellMeta]:
        """获取格子"""
        return self.index.get_cell(cell_id)
    
    def list_cells(self, cell_type: Optional[str] = None) -> List[CellMeta]:
        """列出格子"""
        return self.index.list_cells(cell_type)
    
    def activate(self, cell_id: str, reason: str = "") -> None:
        """激活格子"""
        self.index.activate(cell_id)
        self.log.log(cell_id, reason)
    
    def get_related(self, cell_id: str, min_corr: float = 0.3) -> List[tuple]:
        """获取相关格子"""
        return self.index.get_related(cell_id, min_corr)
    
    def add_connection(
        self,
        cell_id1: str,
        cell_id2: str,
        correlation: float
    ) -> None:
        """添加连接"""
        self.index.add_connection(cell_id1, cell_id2, correlation)
    
    def find_or_create(
        self,
        name: str,
        tags: Optional[List[str]] = None,
        min_similarity: float = 0.6
    ) -> str:
        """查找或创建格子"""
        # 先查找相似格子（基于名称匹配）
        for cell in self.index._cells.values():
            if cell.name == name:
                return cell.cell_id
        
        # 无相似格子，创建新格子
        return self.create_cell(name, tags=tags)


# ═══════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════════════════

__all__ = [
    "CellType",
    "LearnDepth", 
    "CellMeta",
    "CellContent",
    "CellsIndex",
    "ActivationLog",
    "DynamicMemorySystem",
]