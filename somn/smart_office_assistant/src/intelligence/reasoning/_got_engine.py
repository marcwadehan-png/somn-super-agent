# -*- coding: utf-8 -*-
"""
GoT图推理引擎模块
Graph-of-Thoughts Reasoning Engine

提供图网络推理能力，支持：
- 思维图表示
- 图注意力机制
- 多跳关系推理
- 路径搜索

作者: Somn AI
版本: V1.0.0
日期: 2026-04-24
"""

from __future__ import annotations

import uuid
import time
import logging
import heapq
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
from collections import defaultdict, deque
import threading
import math

logger = logging.getLogger(__name__)


class GraphReasoningMode(Enum):
    """图推理模式"""
    LINEAR = "linear"                     # 线性推理
    BRANCHING = "branching"              # 分支推理
    CYCLIC = "cyclic"                    # 循环推理
    HYBRID = "hybrid"                    # 混合推理


@dataclass
class ThoughtGraphNode:
    """思维图节点"""
    node_id: str
    content: str                         # 推理内容
    reasoning_type: str = "analysis"     # 推理类型: analysis/synthesis/evaluation/conclusion
    
    # 关联关系
    parent_ids: List[str] = field(default_factory=list)   # 父节点列表（支持多父节点）
    child_ids: List[str] = field(default_factory=list)    # 子节点列表
    related_ids: List[str] = field(default_factory=list)  # 关联节点（非父子关系）
    
    # 评估分数
    relevance_score: float = 0.5         # 相关性评分 0-1
    coherence_score: float = 0.5         # 连贯性评分 0-1
    novelty_score: float = 0.5           # 新颖性评分 0-1
    combined_score: float = 0.5          # 综合评分
    
    # 状态
    depth: int = 0                      # 图深度
    status: str = "pending"             # pending/expanded/evaluated/final
    expanded: bool = False
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'content': self.content[:100] + '...' if len(self.content) > 100 else self.content,
            'reasoning_type': self.reasoning_type,
            'depth': self.depth,
            'status': self.status,
            'scores': {
                'relevance': self.relevance_score,
                'coherence': self.coherence_score,
                'novelty': self.novelty_score,
                'combined': self.combined_score
            },
            'parent_count': len(self.parent_ids),
            'child_count': len(self.child_ids),
            'related_count': len(self.related_ids)
        }


@dataclass
class ThoughtEdge:
    """思维图边"""
    edge_id: str
    source_id: str                      # 源节点
    target_id: str                       # 目标节点
    relation_type: str = "derives"       # 关系类型: derives/supports/challenges/related
    
    # 边属性
    weight: float = 1.0                 # 边权重
    confidence: float = 1.0              # 置信度
    description: str = ""                # 关系描述
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'edge_id': self.edge_id,
            'source': self.source_id,
            'target': self.target_id,
            'relation': self.relation_type,
            'weight': self.weight,
            'confidence': self.confidence
        }


class ThoughtGraph:
    """思维图"""
    
    def __init__(self, root: ThoughtGraphNode):
        self.root = root
        self.nodes: Dict[str, ThoughtGraphNode] = {root.node_id: root}
        self.edges: Dict[str, ThoughtEdge] = {}
        
        # 索引
        self.children_map: Dict[str, List[str]] = defaultdict(list)
        self.parents_map: Dict[str, List[str]] = defaultdict(list)
        self.related_map: Dict[str, List[str]] = defaultdict(list)
        
        # 图统计
        self._node_count = 1
        self._edge_count = 0
        
        # 拓扑排序辅助
        self._topo_sorted: Optional[List[str]] = None
    
    def add_node(self, node: ThoughtGraphNode) -> bool:
        """添加节点到图"""
        if node.node_id in self.nodes:
            return False
            
        self.nodes[node.node_id] = node
        self._node_count += 1
        self._topo_sorted = None  # 需要重新排序
        return True
    
    def add_edge(self, edge: ThoughtEdge) -> bool:
        """添加边到图"""
        if edge.edge_id in self.edges:
            return False
        
        # 确保节点存在
        if edge.source_id not in self.nodes or edge.target_id not in self.nodes:
            return False
        
        self.edges[edge.edge_id] = edge
        self._edge_count += 1
        
        # 更新索引
        self.children_map[edge.source_id].append(edge.target_id)
        self.parents_map[edge.target_id].append(edge.source_id)
        
        # 更新节点的关联列表
        if edge.source_id not in self.nodes[edge.target_id].parent_ids:
            self.nodes[edge.target_id].parent_ids.append(edge.source_id)
        if edge.target_id not in self.nodes[edge.source_id].child_ids:
            self.nodes[edge.source_id].child_ids.append(edge.target_id)
        
        self._topo_sorted = None  # 需要重新排序
        return True
    
    def add_relation(self, source_id: str, target_id: str, relation_type: str = "related") -> bool:
        """添加非父子关系（仅关联）"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return False
        
        edge = ThoughtEdge(
            edge_id=f"edge_{uuid.uuid4().hex[:8]}",
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type
        )
        
        self.related_map[source_id].append(target_id)
        if target_id not in self.nodes[source_id].related_ids:
            self.nodes[source_id].related_ids.append(target_id)
        
        return True
    
    def get_node(self, node_id: str) -> Optional[ThoughtGraphNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def get_children(self, node_id: str) -> List[ThoughtGraphNode]:
        """获取子节点列表"""
        child_ids = self.children_map.get(node_id, [])
        return [self.nodes[cid] for cid in child_ids if cid in self.nodes]
    
    def get_parents(self, node_id: str) -> List[ThoughtGraphNode]:
        """获取父节点列表"""
        parent_ids = self.parents_map.get(node_id, [])
        return [self.nodes[pid] for pid in parent_ids if pid in self.nodes]
    
    def get_related(self, node_id: str) -> List[ThoughtGraphNode]:
        """获取关联节点"""
        related_ids = self.related_map.get(node_id, [])
        return [self.nodes[rid] for rid in related_ids if rid in self.nodes]
    
    def get_path(self, node_id: str) -> List[ThoughtGraphNode]:
        """获取从根节点到指定节点的路径"""
        if node_id not in self.nodes:
            return []
        
        # 使用BFS找到最短路径
        queue = deque([(self.root.node_id, [self.root.node_id])])
        visited = {self.root.node_id}
        
        while queue:
            current, path = queue.popleft()
            
            if current == node_id:
                return [self.nodes[nid] for nid in path]
            
            for child_id in self.children_map.get(current, []):
                if child_id not in visited:
                    visited.add(child_id)
                    queue.append((child_id, path + [child_id]))
        
        return []
    
    def get_all_paths(self, start_id: str, end_id: str) -> List[List[ThoughtGraphNode]]:
        """获取两个节点之间的所有路径"""
        if start_id not in self.nodes or end_id not in self.nodes:
            return []
        
        all_paths = []
        
        def dfs(current: str, path: List[str], visited: Set[str]):
            if current == end_id:
                all_paths.append([self.nodes[nid] for nid in path])
                return
            
            for child_id in self.children_map.get(current, []):
                if child_id not in visited:
                    visited.add(child_id)
                    dfs(child_id, path + [child_id], visited)
                    visited.remove(child_id)
        
        visited = {start_id}
        dfs(start_id, [start_id], visited)
        return all_paths
    
    def topological_sort(self) -> List[str]:
        """拓扑排序"""
        if self._topo_sorted is not None:
            return self._topo_sorted
        
        in_degree = defaultdict(int)
        for node_id in self.nodes:
            in_degree[node_id] = len(self.parents_map.get(node_id, []))
        
        queue = deque([node_id for node_id, degree in in_degree.items() if degree == 0])
        sorted_ids = []
        
        while queue:
            current = queue.popleft()
            sorted_ids.append(current)
            
            for child_id in self.children_map.get(current, []):
                in_degree[child_id] -= 1
                if in_degree[child_id] == 0:
                    queue.append(child_id)
        
        self._topo_sorted = sorted_ids
        return sorted_ids
    
    def get_stats(self) -> Dict[str, Any]:
        """获取图统计信息"""
        return {
            'total_nodes': self._node_count,
            'total_edges': self._edge_count,
            'max_depth': max((n.depth for n in self.nodes.values()), default=0),
            'avg_score': sum(n.combined_score for n in self.nodes.values()) / max(1, self._node_count),
            'status_counts': {
                status: len([n for n in self.nodes.values() if n.status == status])
                for status in ['pending', 'expanded', 'evaluated', 'final']
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'root_id': self.root.node_id,
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'edges': {eid: edge.to_dict() for eid, edge in self.edges.items()},
            'stats': self.get_stats()
        }


class GraphAttention:
    """图注意力机制"""
    
    def __init__(self, hidden_size: int = 64):
        self.hidden_size = hidden_size
        self.attention_weights = {}
    
    def compute_attention(
        self,
        source_node: ThoughtGraphNode,
        target_node: ThoughtGraphNode,
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """计算两个节点之间的注意力权重"""
        # 简化的注意力计算
        relevance = source_node.relevance_score * target_node.relevance_score
        coherence = source_node.coherence_score if source_node.reasoning_type == target_node.reasoning_type else 0.5
        depth_penalty = math.exp(-0.1 * abs(source_node.depth - target_node.depth))
        
        attention = relevance * 0.5 + coherence * 0.3 + depth_penalty * 0.2
        
        # 存储注意力权重
        key = f"{source_node.node_id}->{target_node.node_id}"
        self.attention_weights[key] = attention
        
        return attention
    
    def aggregate_node_features(
        self,
        node: ThoughtGraphNode,
        neighbors: List[ThoughtGraphNode],
        mode: str = "mean"
    ) -> Dict[str, float]:
        """聚合邻居节点特征"""
        if not neighbors:
            return {
                'avg_relevance': node.relevance_score,
                'avg_coherence': node.coherence_score,
                'avg_novelty': node.novelty_score
            }
        
        if mode == "mean":
            return {
                'avg_relevance': sum(n.relevance_score for n in neighbors) / len(neighbors),
                'avg_coherence': sum(n.coherence_score for n in neighbors) / len(neighbors),
                'avg_novelty': sum(n.novelty_score for n in neighbors) / len(neighbors)
            }
        elif mode == "max":
            return {
                'avg_relevance': max(n.relevance_score for n in neighbors),
                'avg_coherence': max(n.coherence_score for n in neighbors),
                'avg_novelty': max(n.novelty_score for n in neighbors)
            }
        else:
            return {
                'avg_relevance': node.relevance_score,
                'avg_coherence': node.coherence_score,
                'avg_novelty': node.novelty_score
            }


class GraphTraversalExecutor:
    """图遍历执行器"""
    
    def __init__(self):
        self.visited: Set[str] = set()
        self.path_scores: Dict[str, float] = {}
    
    def reset(self):
        """重置状态"""
        self.visited.clear()
        self.path_scores.clear()
    
    def bfs_traverse(
        self,
        graph: ThoughtGraph,
        start_id: str,
        max_depth: int = 5
    ) -> List[Tuple[List[str], float]]:
        """BFS遍历，返回路径和评分"""
        self.reset()
        
        queue = deque([(start_id, [start_id], 0.0)])
        results = []
        
        while queue:
            current_id, path, score = queue.popleft()
            
            if current_id in self.visited:
                continue
            
            self.visited.add(current_id)
            current_node = graph.get_node(current_id)
            
            if not current_node:
                continue
            
            # 更新评分
            path_score = score + current_node.combined_score
            self.path_scores[current_id] = path_score
            
            # 检查深度
            if len(path) > max_depth:
                results.append((path, path_score))
                continue
            
            # 添加子节点
            for child_id in graph.children_map.get(current_id, []):
                if child_id not in self.visited:
                    queue.append((child_id, path + [child_id], path_score))
            
            # 添加关联节点
            for related_id in graph.related_map.get(current_id, []):
                if related_id not in self.visited:
                    queue.append((related_id, path + [related_id], path_score * 0.8))
        
        return results
    
    def dfs_traverse(
        self,
        graph: ThoughtGraph,
        start_id: str,
        max_depth: int = 10
    ) -> List[Tuple[List[str], float]]:
        """DFS遍历"""
        self.reset()
        
        results = []
        
        def dfs(current_id: str, path: List[str], score: float):
            if current_id in self.visited or len(path) > max_depth:
                if len(path) > 1:
                    results.append((path, score))
                return
            
            self.visited.add(current_id)
            current_node = graph.get_node(current_id)
            
            if not current_node:
                return
            
            path_score = score + current_node.combined_score
            
            # 获取所有可访问节点
            next_nodes = (
                graph.children_map.get(current_id, []) +
                graph.related_map.get(current_id, [])
            )
            
            if not next_nodes:
                results.append((path, path_score))
            else:
                for next_id in next_nodes:
                    dfs(next_id, path + [next_id], path_score)
        
        dfs(start_id, [start_id], 0.0)
        return results
    
    def dijkstra_search(
        self,
        graph: ThoughtGraph,
        start_id: str,
        end_id: str
    ) -> Optional[Tuple[List[str], float]]:
        """Dijkstra最短路径搜索"""
        self.reset()
        
        # 优先队列: (负评分, 节点ID, 路径)
        heap = [(0, start_id, [start_id])]
        distances = {start_id: 0}
        
        while heap:
            neg_dist, current_id, path = heapq.heappop(heap)
            dist = -neg_dist
            
            if current_id == end_id:
                return (path, dist)
            
            if dist > distances.get(current_id, float('inf')):
                continue
            
            current_node = graph.get_node(current_id)
            if not current_node:
                continue
            
            # 探索子节点
            for child_id in graph.children_map.get(current_id, []):
                edge_weight = 1.0
                new_dist = dist + edge_weight - current_node.combined_score
                
                if new_dist < distances.get(child_id, float('inf')):
                    distances[child_id] = new_dist
                    heapq.heappush(heap, (-new_dist, child_id, path + [child_id]))
            
            # 探索关联节点（权重更高）
            for related_id in graph.related_map.get(current_id, []):
                edge_weight = 1.5
                new_dist = dist + edge_weight - current_node.combined_score * 0.8
                
                if new_dist < distances.get(related_id, float('inf')):
                    distances[related_id] = new_dist
                    heapq.heappush(heap, (-new_dist, related_id, path + [related_id]))
        
        return None


@dataclass
class GoTConfig:
    """GoT配置"""
    max_nodes: int = 100                 # 最大节点数
    max_depth: int = 10                  # 最大深度
    max_children: int = 5                # 最大子节点数
    expansion_threshold: float = 0.6     # 扩展阈值
    pruning_threshold: float = 0.3       # 剪枝阈值
    
    # 图注意力配置
    enable_attention: bool = True        # 启用图注意力
    attention_hidden_size: int = 64      # 注意力隐藏层大小
    
    # 搜索配置
    search_strategy: str = "best"       # best/bfs/dfs
    enable_cycle_detection: bool = True  # 启用环检测


class GraphOfThoughtsEngine:
    """图推理引擎"""
    
    def __init__(
        self,
        config: Optional[GoTConfig] = None,
        llm_callable: Optional[Callable] = None
    ):
        self.config = config or GoTConfig()
        self.llm_callable = llm_callable
        
        # 初始化组件
        self.graph_attention = GraphAttention(self.config.attention_hidden_size)
        self.traversal_executor = GraphTraversalExecutor()
        
        # 锁
        self._lock = threading.Lock()
        self._is_reasoning = False
        
        # 统计
        self.stats = {
            'total_searches': 0,
            'solutions_found': 0,
            'average_nodes': 0,
            'average_depth': 0
        }
    
    def solve(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
        goal: Optional[str] = None,
        llm_callable: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        使用GoT解决问題
        
        Args:
            problem: 问题描述
            context: 上下文信息
            goal: 目标描述
            llm_callable: LLM调用函数
            
        Returns:
            Dict包含:
            - graph: ThoughtGraph 完整思维图
            - solution: str 最终解决方案
            - paths: List[Dict] 解决方案路径
            - metadata: Dict 元数据
        """
        with self._lock:
            self._is_reasoning = True
        
        try:
            llm = llm_callable or self.llm_callable
            
            # 创建根节点
            root = ThoughtGraphNode(
                node_id=str(uuid.uuid4()),
                content=f"问题分析：{problem}",
                reasoning_type="analysis",
                depth=0
            )
            
            graph = ThoughtGraph(root)
            
            # 使用LLM或模拟生成初始分析
            if llm:
                initial_analysis = llm(f"分析这个问题：{problem}")
                root.content = f"问题分析：{problem}\n\n{initial_analysis}"
                root.combined_score = 0.8
            
            # 图扩展循环
            current_nodes = [root]
            node_count = 1
            
            while current_nodes and node_count < self.config.max_nodes:
                next_nodes = []
                
                for node in current_nodes:
                    # 检查是否应该扩展
                    if node.combined_score < self.config.expansion_threshold:
                        continue
                    
                    # 生成子节点
                    children = self._expand_node(node, problem, goal, llm)
                    
                    for child in children:
                        if node_count >= self.config.max_nodes:
                            break
                        
                        # 添加到图
                        graph.add_node(child)
                        
                        # 创建边
                        edge = ThoughtEdge(
                            edge_id=f"edge_{uuid.uuid4().hex[:8]}",
                            source_id=node.node_id,
                            target_id=child.node_id,
                            relation_type="derives"
                        )
                        graph.add_edge(edge)
                        
                        # 图注意力更新
                        if self.config.enable_attention:
                            attention = self.graph_attention.compute_attention(node, child, context)
                            child.combined_score *= (0.7 + attention * 0.3)
                        
                        next_nodes.append(child)
                        node_count += 1
                
                current_nodes = next_nodes
            
            # 查找解决方案
            final_nodes = [n for n in graph.nodes.values() if n.status == "final"]
            if not final_nodes:
                # 选择评分最高的叶节点作为解决方案
                leaf_nodes = [
                    n for n in graph.nodes.values()
                    if not graph.get_children(n.node_id) and n.status != "pruned"
                ]
                final_nodes = sorted(leaf_nodes, key=lambda n: n.combined_score, reverse=True)[:3]
            
            # 构建解决方案路径
            solutions = []
            for final_node in final_nodes:
                path = graph.get_path(final_node.node_id)
                solutions.append({
                    'content': final_node.content,
                    'path': [n.to_dict() for n in path],
                    'score': final_node.combined_score
                })
            
            # 更新统计
            self.stats['total_searches'] += 1
            tree_stats = graph.get_stats()
            self.stats['average_nodes'] = (
                (self.stats['average_nodes'] * (self.stats['total_searches'] - 1) + tree_stats['total_nodes'])
                / self.stats['total_searches']
            )
            self.stats['average_depth'] = (
                (self.stats['average_depth'] * (self.stats['total_searches'] - 1) + tree_stats['max_depth'])
                / self.stats['total_searches']
            )
            
            return {
                'graph': graph,
                'graph_dict': graph.to_dict(),
                'solutions': solutions,
                'solution': solutions[0]['content'] if solutions else None,
                'paths': [s['path'] for s in solutions],
                'metadata': {
                    'problem': problem,
                    'goal': goal,
                    'node_count': tree_stats['total_nodes'],
                    'edge_count': tree_stats['total_edges'],
                    'max_depth': tree_stats['max_depth'],
                    'stats': self.stats
                }
            }
        
        finally:
            with self._lock:
                self._is_reasoning = False
    
    def _expand_node(
        self,
        node: ThoughtGraphNode,
        problem: str,
        goal: Optional[str],
        llm: Optional[Callable]
    ) -> List[ThoughtGraphNode]:
        """扩展节点生成子节点"""
        children = []
        
        # 根据推理类型生成不同类型的子节点
        reasoning_types = ["analysis", "synthesis", "evaluation"]
        
        for i, reason_type in enumerate(reasoning_types[:self.config.max_children]):
            child = ThoughtGraphNode(
                node_id=str(uuid.uuid4()),
                content=f"第{node.depth + 1}层推理 ({reason_type})",
                reasoning_type=reason_type,
                depth=node.depth + 1,
                relevance_score=0.5,
                coherence_score=0.6,
                novelty_score=0.5
            )
            child.combined_score = (
                child.relevance_score * 0.4 +
                child.coherence_score * 0.3 +
                child.novelty_score * 0.3
            )
            
            # 检查剪枝阈值
            if child.combined_score < self.config.pruning_threshold:
                child.status = "pruned"
                continue
            
            children.append(child)
        
        return children
    
    def search_path(
        self,
        graph: ThoughtGraph,
        start_id: str,
        end_id: str,
        strategy: str = "dijkstra"
    ) -> Optional[Tuple[List[str], float]]:
        """
        在图中搜索路径
        
        Args:
            graph: 思维图
            start_id: 起始节点ID
            end_id: 目标节点ID
            strategy: 搜索策略 (dijkstra/bfs/dfs)
            
        Returns:
            (路径节点ID列表, 评分) 或 None
        """
        if strategy == "dijkstra":
            return self.traversal_executor.dijkstra_search(graph, start_id, end_id)
        elif strategy == "bfs":
            results = self.traversal_executor.bfs_traverse(graph, start_id)
            if results:
                return max(results, key=lambda x: x[1])
            return None
        elif strategy == "dfs":
            results = self.traversal_executor.dfs_traverse(graph, start_id)
            if results:
                return max(results, key=lambda x: x[1])
            return None
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.stats.copy()


# 快捷函数
def solve_with_got(
    problem: str,
    context: Optional[Dict[str, Any]] = None,
    goal: Optional[str] = None,
    llm_callable: Optional[Callable] = None
) -> Dict[str, Any]:
    """使用GoT解决问题的快捷函数"""
    engine = GraphOfThoughtsEngine(llm_callable=llm_callable)
    return engine.solve(problem, context, goal, llm_callable)
