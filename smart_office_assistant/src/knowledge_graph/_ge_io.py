"""知识图谱引擎 - 持久化与I/O"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from ._ge_types import GraphNode

__all__ = [
    'export_to_json_impl',
    'import_from_json_impl',
    'load_graph_impl',
    'save_graph_impl',
]

def save_graph_impl(core):
    """保存图谱"""
    # 保存节点
    nodes_file = core.base_path / "nodes.json"
    with open(nodes_file, 'w', encoding='utf-8') as f:
        json.dump({
            node_id: node.to_dict() 
            for node_id, node in core.node_index.items()
        }, f, ensure_ascii=False, indent=2)
    
    # 保存边
    edges_file = core.base_path / "edges.json"
    edges_data = []
    for source, target, data in core.graph.edges(data=True):
        edges_data.append({
            'source': source,
            'target': target,
            **data
        })
    with open(edges_file, 'w', encoding='utf-8') as f:
        json.dump(edges_data, f, ensure_ascii=False, indent=2)

def load_graph_impl(core):
    """加载图谱"""
    # 直接操作 _graph 而非通过 graph property，避免 _ensure_graph 递归
    _nx_graph = core._graph
    nodes_file = core.base_path / "nodes.json"
    if nodes_file.exists():
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes_data = json.load(f)
            for node_id, data in nodes_data.items():
                node = GraphNode.from_dict(data)
                core.node_index[node_id] = node
                core.type_index[node.node_type].add(node_id)
                _nx_graph.add_node(node_id, **data)
    
    edges_file = core.base_path / "edges.json"
    if edges_file.exists():
        with open(edges_file, 'r', encoding='utf-8') as f:
            edges_data = json.load(f)
            for edge in edges_data:
                source = edge.pop('source')
                target = edge.pop('target')
                _nx_graph.add_edge(source, target, **edge)

def export_to_json_impl(core, filepath: str):
    """导出为JSON"""
    from ._ge_graph import get_statistics_impl
    data = {
        'nodes': [node.to_dict() for node in core.node_index.values()],
        'edges': [
            {
                'source': source,
                'target': target,
                **data
            }
            for source, target, data in core.graph.edges(data=True)
        ],
        'statistics': get_statistics_impl(core),
        'exported_at': datetime.now().isoformat()
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def import_from_json_impl(core, filepath: str):
    """从JSON导入"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 导入节点
    for node_data in data.get('nodes', []):
        node = GraphNode.from_dict(node_data)
        core.node_index[node.node_id] = node
        core.type_index[node.node_type].add(node.node_id)
        core.graph.add_node(node.node_id, **node_data)
    
    # 导入边
    for edge_data in data.get('edges', []):
        source = edge_data.pop('source')
        target = edge_data.pop('target')
        core.graph.add_edge(source, target, **edge_data)
