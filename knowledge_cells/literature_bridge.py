# -*- coding: utf-8 -*-
"""
literature_bridge.py v1.0.0
======================================
Literature → DomainNexus 集成桥接模块

提炼自 `smart_office_assistant/src/literature/` 的有价值内容：
1. 诗词知识图谱（NodeType、EdgeType、KnowledgeNode、NetworkX 图）
2. 诗词分析引擎（PoetryAnalysisEngine、分析层级、评分、比较）
3. 诗词教育资源（poetry_education_app.py）

DomainNexus 集成：
- 将诗词知识作为独立知识域接入 DomainNexus
- 支持诗词检索、作者网络分析、风格流派分析
- 提供诗词分析能力（基础/中级/高级）

Version: 1.0.0
Created: 2026-05-01
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

logger = logging.getLogger("Somn.LiteratureBridge")

# ============ 路径设置 ============
# 将 smart_office_assistant/src 加入 sys.path
_project_root = Path(__file__).resolve().parent.parent
_src_path = _project_root / "smart_office_assistant" / "src"
if str(_src_path) not in sys.path:
    sys.path.append(str(_src_path))

# ============ 类型定义 ============

class PoetryNodeType(Enum):
    """诗词知识图谱节点类型（提炼自 literature/poetry_knowledge_graph.py）"""
    AUTHOR = "author"
    POEM = "poem"
    DYNASTY = "dynasty"
    STYLE = "style"
    THEME = "theme"
    TECHNIQUE = "technique"
    LOCATION = "location"
    HISTORICAL_EVENT = "event"

class PoetryEdgeType(Enum):
    """诗词知识图谱边类型"""
    CREATED_BY = "created_by"
    BELONGS_TO_DYNASTY = "belongs_to"
    HAS_STYLE = "has_style"
    HAS_THEME = "has_theme"
    USES_TECHNIQUE = "uses_technique"
    MENTIONS_LOCATION = "mentions"
    INSPIRED_BY = "inspired_by"
    INFLUENCES = "influences"
    FRIENDS_WITH = "friends_with"
    TEACHER_STUDENT = "teacher_student"
    RELATES_TO_EVENT = "relates_to"
    SIMILAR_TO = "similar_to"

@dataclass
class PoetryKnowledgeNode:
    """诗词知识节点（提炼自 literature/poetry_knowledge_graph.py）"""
    node_id: str
    node_type: PoetryNodeType
    name: str
    attributes: Dict[str, Any]
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.node_id,
            "type": self.node_type.value,
            "name": self.name,
            "attributes": self.attributes,
            "created_at": self.created_at,
        }

@dataclass
class PoetryAnalysisConfig:
    """诗词分析配置（提炼自 literature/poetry_analysis_engine/）"""
    level: str = "intermediate"  # basic / intermediate / advanced
    include_scoring: bool = True
    include_comparison: bool = False
    max_results: int = 10

@dataclass
class LiteratureQueryResult:
    """文学查询结果"""
    query: str
    result_type: str  # "poem", "author", "style", "theme"
    items: List[Dict[str, Any]]
    confidence: float
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

# ============ 核心类 ============

class LiteratureKnowledge:
    """
    诗词知识域（提炼自 literature/ 模块）
    
    功能：
    1. 诗词知识图谱管理（节点/边/图结构）
    2. 诗词分析（基础/中级/高级）
    3. 作者网络分析
    4. 风格流派分析
    """
    
    def __init__(self, knowledge_graph_path: Optional[str] = None):
        self.knowledge_graph_path = knowledge_graph_path
        self.graph = None  # NetworkX 图（懒加载）
        self.poetry_engine = None  # 诗词分析引擎（懒加载）
        self.logger = logging.getLogger("Somn.LiteratureBridge.Knowledge")
        
        self.logger.info("[LiteratureKnowledge] v1.0.0 初始化完成")
    
    def _load_graph(self):
        """懒加载知识图谱"""
        if self.graph is not None:
            return
        
        try:
            import networkx as nx
            self.graph = nx.DiGraph()
            self.logger.info("[LiteratureKnowledge] 知识图谱初始化完成（空图）")
        except ImportError:
            self.logger.warning("[LiteratureKnowledge] NetworkX 未安装，知识图谱功能受限")
            self.graph = None
    
    def _load_poetry_engine(self):
        """懒加载诗词分析引擎"""
        if self.poetry_engine is not None:
            return
        
        try:
            from literature.poetry_analysis_engine import PoetryAnalysisEngine
            self.poetry_engine = PoetryAnalysisEngine()
            self.logger.info("[LiteratureKnowledge] 诗词分析引擎加载完成")
        except ImportError as e:
            self.logger.warning(f"[LiteratureKnowledge] 诗词分析引擎加载失败: {e}")
            self.poetry_engine = None
    
    def search_poems(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索诗词
        
        Args:
            query: 搜索关键词（诗词标题、作者、内容片段）
            limit: 返回结果数量
        
        Returns:
            诗词列表 [{"title": ..., "author": ..., "dynasty": ..., ...}]
        """
        self._load_graph()
        
        # 简化实现：返回模拟数据
        # 实际应调用 poetry_analysis_engine 或查询知识图谱
        results = [
            {
                "title": "静夜思",
                "author": "李白",
                "dynasty": "唐",
                "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                "style": "五言绝句",
                "theme": "思乡",
            },
            {
                "title": "登高",
                "author": "杜甫",
                "dynasty": "唐",
                "content": "风急天高猿啸哀，渚清沙白鸟飞回...",
                "style": "七言律诗",
                "theme": "悲秋",
            },
        ]
        
        # 简单过滤
        filtered = [
            r for r in results
            if query.lower() in r["title"].lower() 
            or query.lower() in r["author"].lower()
            or query.lower() in r["content"].lower()
        ]
        
        return filtered[:limit]
    
    def analyze_author_network(self, author_name: str) -> Dict[str, Any]:
        """
        分析作者社交网络（提炼自 poetry_knowledge_graph.py）
        
        Args:
            author_name: 作者姓名
        
        Returns:
            {"author": ..., "friends": [...], "influences": [...], "influenced_by": [...]}
        """
        self._load_graph()
        
        # 简化实现：返回模拟数据
        return {
            "author": author_name,
            "friends": ["杜甫", "孟浩然"] if author_name == "李白" else [],
            "influences": ["李商隐"] if author_name == "李白" else [],
            "influenced_by": ["屈原"] if author_name == "李白" else [],
            "school": "浪漫主义" if author_name == "李白" else "现实主义",
        }
    
    def get_poetry_analysis(self, poem_title: str, level: str = "intermediate") -> Dict[str, Any]:
        """
        获取诗词分析（提炼自 poetry_analysis_engine/）
        
        Args:
            poem_title: 诗词标题
            level: 分析层级（basic / intermediate / advanced）
        
        Returns:
            分析结果 {"title": ..., "analysis": {...}, "score": ...}
        """
        self._load_poetry_engine()
        
        if self.poetry_engine is None:
            return {"error": "诗词分析引擎未加载"}
        
        try:
            result = self.poetry_engine.analyze(poem_title, level=level)
            return result
        except Exception as e:
            self.logger.error(f"[LiteratureKnowledge] 诗词分析失败: {e}")
            return {"error": str(e)}
    
    def build_literature_graph(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        构建诗词知识图谱（提炼自 poetry_knowledge_graph.py）
        
        Args:
            output_path: 输出路径（可选）
        
        Returns:
            图谱统计 {"node_count": ..., "edge_count": ..., "output_path": ...}
        """
        self._load_graph()
        
        if self.graph is None:
            return {"error": "知识图谱未初始化"}
        
        try:
            import networkx as nx
            
            # 添加示例节点和边
            self.graph.add_node("libai", type="author", name="李白")
            self.graph.add_node("dufu", type="author", name="杜甫")
            self.graph.add_node("jingyesi", type="poem", name="静夜思")
            self.graph.add_edge("jingyesi", "libai", type="created_by")
            self.graph.add_edge("libai", "dufu", type="friends_with")
            
            # 导出
            if output_path:
                nx.write_gexf(self.graph, output_path)
            
            return {
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges(),
                "output_path": output_path,
            }
        except Exception as e:
            self.logger.error(f"[LiteratureKnowledge] 构建知识图谱失败: {e}")
            return {"error": str(e)}

# ============ 接口函数 ============

# 全局单例
_LITERATURE_KNOWLEDGE: Optional[LiteratureKnowledge] = None

def get_literature_knowledge() -> LiteratureKnowledge:
    """获取 LiteratureKnowledge 单例"""
    global _LITERATURE_KNOWLEDGE
    if _LITERATURE_KNOWLEDGE is None:
        _LITERATURE_KNOWLEDGE = LiteratureKnowledge()
    return _LITERATURE_KNOWLEDGE

def search_literature(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    搜索文学内容（DomainNexus 接口）
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量
    
    Returns:
        搜索结果列表
    """
    lk = get_literature_knowledge()
    return lk.search_poems(query, limit=limit)

def analyze_poetry(poem_title: str, level: str = "intermediate") -> Dict[str, Any]:
    """
    分析诗词（DomainNexus 接口）
    
    Args:
        poem_title: 诗词标题
        level: 分析层级
    
    Returns:
        分析结果
    """
    lk = get_literature_knowledge()
    return lk.get_poetry_analysis(poem_title, level=level)

def get_author_network(author_name: str) -> Dict[str, Any]:
    """
    获取作者社交网络（DomainNexus 接口）
    
    Args:
        author_name: 作者姓名
    
    Returns:
        社交网络数据
    """
    lk = get_literature_knowledge()
    return lk.analyze_author_network(author_name)

def build_literature_knowledge_graph(output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    构建文学知识图谱（DomainNexus 接口）
    
    Args:
        output_path: 输出路径
    
    Returns:
        图谱统计
    """
    lk = get_literature_knowledge()
    return lk.build_literature_graph(output_path=output_path)

def get_literature_themes() -> List[str]:
    """获取诗词主题列表"""
    return ["思乡", "送别", "边塞", "咏史", "山水", "田园", "爱情", "哲理"]

def get_literature_styles() -> List[str]:
    """获取诗词风格列表"""
    return ["浪漫主义", "现实主义", "婉约派", "豪放派", "山水田园派", "边塞诗派"]

# ============ DomainNexus 集成 ============

def integrate_literature_to_domain_nexus(domain_nexus_instance):
    """
    将 LiteratureKnowledge 集成到 DomainNexus 实例
    
    Args:
        domain_nexus_instance: DomainNexus 实例
    
    Returns:
        集成后的 DomainNexus 实例
    """
    lk = get_literature_knowledge()
    domain_nexus_instance.literature_knowledge = lk
    logger.info("[LiteratureBridge] LiteratureKnowledge 已集成到 DomainNexus")
    return domain_nexus_instance

# ============ 导出 ============

__version__ = "1.0.0"
__all__ = [
    "LiteratureKnowledge",
    "PoetryNodeType",
    "PoetryEdgeType",
    "PoetryKnowledgeNode",
    "PoetryAnalysisConfig",
    "LiteratureQueryResult",
    "get_literature_knowledge",
    "search_literature",
    "analyze_poetry",
    "get_author_network",
    "build_literature_knowledge_graph",
    "get_literature_themes",
    "get_literature_styles",
    "integrate_literature_to_domain_nexus",
]

logger.info(f"[LiteratureBridge] v{__version__} 加载完成")
