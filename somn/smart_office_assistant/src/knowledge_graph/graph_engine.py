"""知识图谱引擎 - 核心图数据库管理
__all__ = [
    'add_concept',
    'add_edge',
    'add_node',
    'add_relation',
    'add_rule',
    'export_to_json',
    'find_path',
    'find_related',
    'get_statistics',
    'get_subgraph',
    'import_from_json',
    'query',
    'query_concept',
    'query_relation',
    'query_rule',
    'update_confidence',
]

基于 NetworkX + 持久化存储
兼容层 - 委托实现至子模块
"""

# 类型定义
from ._ge_types import (
    NodeType,
    EdgeType,
    GraphNode,
    GraphEdge,
    GraphQuery,
)

# 导入子模块实现
from . import _ge_compat as compat
from . import _ge_graph as graph_ops
from . import _ge_io as io_ops

# 兼容层函数（供委托调用）
from ._ge_compat import (
    _ensure_list,
    _normalize_rule_type,
    _resolve_node_type,
    _generate_relation_id,
    build_compat_concept_dict,
    build_compat_rule_dict,
    build_relation_dict,
    find_rule_node,
    upsert_rule_store,
    upsert_rule_node,
    sync_rule_relationships,
    match_rule,
)

# 图操作函数
from ._ge_graph import (
    _generate_id,
    add_node_impl,
    add_edge_impl,
    query_impl,
    find_related_impl,
    find_path_impl,
    get_subgraph_impl,
    get_statistics_impl,
)

# I/O函数
from ._ge_io import (
    save_graph_impl,
    load_graph_impl,
    export_to_json_impl,
    import_from_json_impl,
)

import json
from pathlib import Path
from src.core.paths import KNOWLEDGE_GRAPH_DIR
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict

class KnowledgeGraphEngine:
    """知识图谱引擎"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else KNOWLEDGE_GRAPH_DIR
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 延迟初始化：networkx 图改为懒加载
        self._graph = None
        self._nx_graph = None
        self._graph_loaded = False
        
        # 索引
        self.node_index: Dict[str, GraphNode] = {}
        self.type_index: Dict[NodeType, Set[str]] = {t: set() for t in NodeType}
        self.compat_rules_path = self.base_path / "rules_compat.json"
        self.compat_rule_store: List[Dict[str, Any]] = []

        # 延迟加载标志（图数据和规则引导推迟到首次访问）
        self._rules_loaded = False

    def _ensure_graph(self):
        """懒初始化 networkx 图和索引（首次使用时调用）"""
        if self._graph_loaded:
            return
        import networkx as nx
        self._graph = nx.DiGraph()
        self._nx_graph = self._graph
        self._load_graph()
        self._graph_loaded = True

    def _ensure_rules(self):
        """懒加载规则和视图引导（首次使用时调用）"""
        if self._rules_loaded:
            return
        self._load_compat_rules()
        self._bootstrap_rule_views()
        self._rules_loaded = True
    
    @property
    def graph(self):
        """懒加载图（首次访问时自动初始化）"""
        self._ensure_graph()
        return self._graph

    @graph.setter
    def graph(self, value):
        """允许显式设置图对象"""
        self._graph = value

    def _load_compat_rules(self):
        """加载兼容神经记忆系统的规则存储."""
        compat._load_compat_rules_impl(self)
    
    def _save_compat_rules(self):
        """保存兼容神经记忆系统的规则存储."""
        compat._save_compat_rules_impl(self)
    
    def _ensure_list(self, value: Any) -> List[Any]:
        """把任意值标准化为列表."""
        return compat._ensure_list(value)
    
    def _normalize_rule_type(self, rule_type: Any) -> Tuple[str, str]:
        """unified规则类型的中英文字段."""
        return compat._normalize_rule_type(rule_type)
    
    def _resolve_node_type(self, node_type_value: Any, default: NodeType = NodeType.CONCEPT) -> NodeType:
        """把字符串节点类型解析为枚举."""
        return compat._resolve_node_type(node_type_value, default)
    
    def _generate_relation_id(self, source_id: str, target_id: str, edge_type: str, scope: str = "") -> str:
        """为图谱关系generate稳定ID."""
        return compat._generate_relation_id(source_id, target_id, edge_type, scope)
    
    def _build_compat_concept_dict(self, node: GraphNode) -> Dict[str, Any]:
        """把图谱概念节点转换为神经记忆系统兼容结构."""
        return compat.build_compat_concept_dict(node)
    
    def _build_compat_rule_dict(self, rule_data: Dict[str, Any], graph_node_id: str = None) -> Dict[str, Any]:
        """把 RuleEngine / 兼容存储unified转换为神经记忆系统兼容结构."""
        return compat.build_compat_rule_dict(self, rule_data, graph_node_id)
    
    def _build_relation_dict(self, source_id: str, target_id: str, edge_data: Dict[str, Any]) -> Dict[str, Any]:
        """把图谱边转换为关系兼容结构."""
        return compat.build_relation_dict(self, source_id, target_id, edge_data)
    
    def _find_rule_node(self, rule_id: str = None, rule_name: str = None) -> Optional[GraphNode]:
        """按规则ID或名称查找规则节点."""
        return compat.find_rule_node(self, rule_id, rule_name)
    
    def _upsert_rule_store(self, rule_entry: Dict[str, Any]):
        """把规则写入兼容规则存储."""
        compat.upsert_rule_store(self, rule_entry)
    
    def _upsert_rule_node(self, rule_entry: Dict[str, Any]) -> GraphNode:
        """把规则写入图谱规则节点."""
        return compat.upsert_rule_node(self, rule_entry)
    
    def _sync_rule_relationships(self, rule_node: GraphNode, rule_entry: Dict[str, Any]):
        """把规则的行业/阶段/metrics/动作目标写回到图谱关系."""
        compat.sync_rule_relationships(self, rule_node, rule_entry)
    
    def _match_rule(self, rule_entry: Dict[str, Any], rule_id: str = None,
                    rule_type: str = None, applicable_scenario: str = None) -> bool:
        """规则兼容过滤."""
        return compat.match_rule(self, rule_entry, rule_id, rule_type, applicable_scenario)
    
    def _bootstrap_rule_views(self):
        """启动时把规则兼容存储与规则节点双向对齐."""
        compat.bootstrap_rule_views(self)
    
    def add_concept(self, concept_type: str, concept_data: Dict[str, Any]) -> str:
        """兼容神经记忆系统的概念写入接口."""
        return compat.add_concept_impl(self, concept_type, concept_data)
    
    def query_concept(self, concept_id: str = None, concept_name: str = None,
                      concept_type: str = None) -> List[Dict[str, Any]]:
        """兼容神经记忆系统的概念查询接口."""
        return compat.query_concept_impl(self, concept_id, concept_name, concept_type)
    
    def add_rule(self, rule_type: str, rule_data: Dict[str, Any]) -> str:
        """兼容神经记忆系统的规则写入接口,并同步成规则节点与关系."""
        return compat.add_rule_impl(self, rule_type, rule_data)
    
    def add_relation(self, relation_type: str, relation_data: Dict[str, Any]) -> str:
        """兼容神经记忆系统的关系写入接口."""
        return compat.add_relation_impl(self, relation_type, relation_data)
    
    def query_rule(self, rule_id: str = None, rule_type: str = None,
                   applicable_scenario: str = None) -> List[Dict[str, Any]]:
        """兼容神经记忆系统的规则查询接口."""
        return compat.query_rule_impl(self, rule_id, rule_type, applicable_scenario)
    
    def query_relation(self, relation_id: str = None, concept_id: str = None,
                       relation_type: str = None) -> List[Dict[str, Any]]:
        """兼容神经记忆系统的关系查询接口."""
        return compat.query_relation_impl(self, relation_id, concept_id, relation_type)
    
    def update_confidence(self, entity_type: str, entity_id: str,
                          new_confidence: float, evidence: str = ""):
        """兼容神经记忆系统的置信度更新接口."""
        return compat.update_confidence_impl(self, entity_type, entity_id, new_confidence, evidence)
    
    def _generate_id(self, name: str, node_type: NodeType) -> str:
        """generate节点ID"""
        return graph_ops._generate_id(name, node_type)
    
    def add_node(self, name: str, node_type: NodeType, 
                 properties: Dict[str, Any] = None,
                 source: str = "manual",
                 confidence: float = 1.0) -> GraphNode:
        """添加节点"""
        return graph_ops.add_node_impl(self, name, node_type, properties, source, confidence)
    
    def add_edge(self, source_name: str, source_type: NodeType,
                 target_name: str, target_type: NodeType,
                 edge_type: EdgeType,
                 properties: Dict[str, Any] = None,
                 weight: float = 1.0,
                 confidence: float = 1.0) -> bool:
        """添加边"""
        return graph_ops.add_edge_impl(self, source_name, source_type, target_name, target_type,
                                       edge_type, properties, weight, confidence)
    
    def query(self, query: GraphQuery) -> List[GraphNode]:
        """查询节点"""
        return graph_ops.query_impl(self, query)
    
    def find_related(self, node_id: str, edge_types: List[EdgeType] = None,
                     depth: int = 1) -> Dict[str, List[Dict]]:
        """查找相关节点"""
        return graph_ops.find_related_impl(self, node_id, edge_types, depth)
    
    def find_path(self, source_id: str, target_id: str) -> Optional[List[Dict]]:
        """查找两节点间路径"""
        return graph_ops.find_path_impl(self, source_id, target_id)
    
    def get_subgraph(self, center_node_id: str, depth: int = 2) -> Dict:
        """get子图"""
        return graph_ops.get_subgraph_impl(self, center_node_id, depth)
    
    def get_statistics(self) -> Dict[str, Any]:
        """get图谱统计,并兼容神经记忆系统的知识统计结构."""
        return graph_ops.get_statistics_impl(self)
    
    def _save_graph(self):
        """保存图谱"""
        io_ops.save_graph_impl(self)
    
    def _load_graph(self):
        """加载图谱"""
        io_ops.load_graph_impl(self)
    
    def export_to_json(self, filepath: str):
        """导出为JSON"""
        io_ops.export_to_json_impl(self, filepath)
    
    def import_from_json(self, filepath: str):
        """从JSON导入"""
        io_ops.import_from_json_impl(self, filepath)
