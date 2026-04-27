"""知识图谱引擎 - 核心图操作"""
import hashlib
import networkx as nx
from datetime import datetime
from typing import Dict, List, Any, Optional
from ._ge_types import NodeType, EdgeType, GraphNode, GraphQuery
from ._ge_compat import (
    _resolve_node_type, _generate_relation_id, _ensure_list,
    build_compat_concept_dict, build_compat_rule_dict,
    find_rule_node, upsert_rule_store, upsert_rule_node,
    sync_rule_relationships, match_rule
)

__all__ = [
    'add_edge_impl',
    'add_node_impl',
    'find_path_impl',
    'find_related_impl',
    'get_statistics_impl',
    'get_subgraph_impl',
    'query_impl',
]

def _generate_id(name: str, node_type: NodeType) -> str:
    """generate节点ID"""
    content = f"{node_type.value}:{name}"
    return hashlib.md5(content.encode()).hexdigest()[:12]

def add_node_impl(core, name: str, node_type: NodeType,
                  properties: Dict[str, Any] = None,
                  source: str = "manual",
                  confidence: float = 1.0) -> GraphNode:
    """添加节点"""
    node_id = _generate_id(name, node_type)
    
    if node_id in core.node_index:
        # 更新现有节点
        node = core.node_index[node_id]
        node.properties.update(properties or {})
        node.confidence = max(node.confidence, confidence)
        node.updated_at = datetime.now().isoformat()
    else:
        # 创建新节点
        node = GraphNode(
            node_id=node_id,
            node_type=node_type,
            name=name,
            properties=properties or {},
            source=source,
            confidence=confidence
        )
        core.node_index[node_id] = node
        core.type_index[node_type].add(node_id)
    
    # 同步到 NetworkX
    core.graph.add_node(node_id, **node.to_dict())
    
    return node

def add_edge_impl(core, source_name: str, source_type: NodeType,
                  target_name: str, target_type: NodeType,
                  edge_type: EdgeType,
                  properties: Dict[str, Any] = None,
                  weight: float = 1.0,
                  confidence: float = 1.0) -> bool:
    """添加边"""
    source_id = _generate_id(source_name, source_type)
    target_id = _generate_id(target_name, target_type)
    
    # 确保节点存在
    if source_id not in core.node_index:
        add_node_impl(core, source_name, source_type)
    if target_id not in core.node_index:
        add_node_impl(core, target_name, target_type)
    
    # 添加边
    edge_data = {
        'edge_type': edge_type.value,
        'properties': properties or {},
        'weight': weight,
        'confidence': confidence,
        'created_at': datetime.now().isoformat()
    }
    
    core.graph.add_edge(source_id, target_id, **edge_data)
    return True

def query_impl(core, query: GraphQuery) -> List[GraphNode]:
    """查询节点"""
    results = []
    
    # 按类型过滤
    candidate_ids = set()
    if query.node_types:
        for nt in query.node_types:
            candidate_ids.update(core.type_index.get(nt, set()))
    else:
        candidate_ids = set(core.node_index.keys())
    
    # 按属性过滤
    for node_id in candidate_ids:
        node = core.node_index[node_id]
        
        # 置信度过滤
        if node.confidence < query.min_confidence:
            continue
        
        # 名称模式过滤
        if query.name_pattern and query.name_pattern.lower() not in node.name.lower():
            continue
        
        # 属性过滤
        if query.node_properties:
            match = True
            for key, value in query.node_properties.items():
                if node.properties.get(key) != value:
                    match = False
                    break
            if not match:
                continue
        
        results.append(node)
    
    # 限制数量
    return results[:query.limit]

def find_related_impl(core, node_id: str, edge_types: List[EdgeType] = None,
                      depth: int = 1) -> Dict[str, List[Dict]]:
    """查找相关节点"""
    if node_id not in core.node_index:
        return {}
    
    related = {'outgoing': [], 'incoming': []}
    
    # 出边
    if node_id in core.graph:
        for target_id, edge_data in core.graph[node_id].items():
            if edge_types and edge_data.get('edge_type') not in [et.value for et in edge_types]:
                continue
            if target_id in core.node_index:
                related['outgoing'].append({
                    'node': core.node_index[target_id].to_dict(),
                    'edge': edge_data
                })
    
    # 入边
    for source_id in core.graph.predecessors(node_id):
        edge_data = core.graph[source_id][node_id]
        if edge_types and edge_data.get('edge_type') not in [et.value for et in edge_types]:
            continue
        if source_id in core.node_index:
            related['incoming'].append({
                'node': core.node_index[source_id].to_dict(),
                'edge': edge_data
            })
    
    return related

def find_path_impl(core, source_id: str, target_id: str) -> Optional[List[Dict]]:
    """查找两节点间路径"""
    try:
        path = nx.shortest_path(core.graph, source_id, target_id)
        return [core.node_index[n].to_dict() for n in path if n in core.node_index]
    except nx.NetworkXNoPath:
        return None

def get_subgraph_impl(core, center_node_id: str, depth: int = 2) -> Dict:
    """get子图"""
    if center_node_id not in core.graph:
        return {}
    
    # BFSget邻居
    nodes = {center_node_id}
    edges = []
    current_level = {center_node_id}
    
    for _ in range(depth):
        next_level = set()
        for node_id in current_level:
            if node_id in core.graph:
                for neighbor in core.graph.neighbors(node_id):
                    if neighbor not in nodes:
                        next_level.add(neighbor)
                        edges.append((node_id, neighbor))
                for predecessor in core.graph.predecessors(node_id):
                    if predecessor not in nodes:
                        next_level.add(predecessor)
                        edges.append((predecessor, node_id))
        nodes.update(next_level)
        current_level = next_level
    
    return {
        'nodes': [core.node_index[n].to_dict() for n in nodes if n in core.node_index],
        'edges': [{'source': s, 'target': t} for s, t in edges]
    }

def get_statistics_impl(core) -> Dict[str, Any]:
    """get图谱统计,并兼容神经记忆系统的知识统计结构."""
    concept_type_stats: Dict[str, int] = {}
    for node_id in core.type_index.get(NodeType.CONCEPT, set()):
        node = core.node_index.get(node_id)
        if not node:
            continue
        concept_type = str(node.properties.get("概念类型", node.properties.get("category", "通用概念")))
        concept_type_stats[concept_type] = concept_type_stats.get(concept_type, 0) + 1

    rule_type_stats: Dict[str, int] = {}
    for rule in core.compat_rule_store:
        rule_type = str(rule.get("规则类型", "通用规则"))
        rule_type_stats[rule_type] = rule_type_stats.get(rule_type, 0) + 1

    total_nodes = len(core.node_index)
    total_edges = core.graph.number_of_edges()
    return {
        'total_nodes': total_nodes,
        'total_edges': total_edges,
        'node_type_distribution': {
            t.value: len(ids) for t, ids in core.type_index.items()
        },
        'avg_degree': sum(dict(core.graph.degree()).values()) / max(total_nodes, 1),
        'density': nx.density(core.graph),
        '概念统计': concept_type_stats,
        '规则统计': rule_type_stats,
        '关系统计': {
            '图谱关系': total_edges
        },
        '总体统计': {
            '概念总数': sum(concept_type_stats.values()),
            '规则总数': len(core.compat_rule_store),
            '关系总数': total_edges,
            '知识密度': round(sum(concept_type_stats.values()) / max(1, total_edges), 4)
        }
    }
