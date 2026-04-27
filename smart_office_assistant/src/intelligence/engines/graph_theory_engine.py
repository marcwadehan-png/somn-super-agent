"""
图论分析引擎 - Graph Theory Engine
=================================

基于图论的实体关系分析与网络优化引擎

v6.0.0 新增功能:
- 图的构建与分析:BFS/DFS,最短路,网络拓扑
- 中心性分析:度中心性,介数中心性,接近中心性
- 社区检测:基于图分割的社区发现
- 网络优化:关键节点recognize,冗余边检测
- GNN模拟:简化版图神经网络推理

核心能力:
1. 关系网络构建 - 从实体关系构建图结构
2. 路径分析 - 最短路径,关键路径
3. 影响力分析 - 基于中心性的节点重要性
4. 结构优化 - 网络冗余,脆弱点检测
"""

import math
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import deque, defaultdict
import heapq
import networkx as nx

from .math_wisdom_core import GraphAnalyzer, GraphType, GraphAnalysis

class CentralityType(Enum):
    """中心性类型"""
    DEGREE = "degree"                     # 度中心性
    BETWEENNESS = "betweenness"           # 介数中心性
    CLOSENESS = "closeness"               # 接近中心性
    EIGENVECTOR = "eigenvector"           # characteristics向量中心性
    PAGERANK = "pagerank"                 # PageRank

class CommunityDetectionMethod(Enum):
    """社区检测方法"""
    LABEL_PROPAGATION = "label_propagation"  # 标签传播
    GREEDY_MODULARITY = "greedy_modularity"  # 贪心模块度
    LOUVAIN = "louvain"                      # Louvain算法

@dataclass
class PathAnalysis:
    """路径分析结果"""
    source: str
    target: str
    
    shortest_path: List[str] = field(default_factory=list)
    shortest_distance: float = 0.0
    
    all_paths: List[List[str]] = field(default_factory=list)
    path_count: int = 0
    
    # 路径属性
    average_weight: float = 0.0
    path_reliability: float = 0.0

@dataclass
class InfluenceAnalysis:
    """影响力分析结果"""
    node: str
    centrality_score: float
    
    centrality_type: CentralityType
    
    # 详细metrics
    degree: int = 0
    in_degree: int = 0
    out_degree: int = 0
    
    # 排名
    rank: int = 0
    percentile: float = 0.0
    
    # 影响力描述
    influence_level: str = ""  # 高/中/低

@dataclass
class Community:
    """社区"""
    community_id: int
    nodes: List[str]
    size: int
    
    # 社区属性
    internal_edges: int = 0
    external_edges: int = 0
    density: float = 0.0
    
    # 核心节点
    core_nodes: List[str] = field(default_factory=list)

@dataclass
class NetworkVulnerability:
    """网络脆弱性分析"""
    critical_nodes: List[str] = field(default_factory=list)  # 关键节点
    bridge_edges: List[Tuple[str, str]] = field(default_factory=list)  # 桥接边
    
    # 评估metrics
    connectivity: float = 0.0  # 连通度
    redundancy: float = 0.0  # 冗余度
    efficiency: float = 0.0  # 网络效率
    
    # 脆弱性评估
    vulnerability_score: float = 0.0
    vulnerability_level: str = ""  # 高/中/低

@dataclass
class GraphTheoryInsight:
    """图论智慧洞察"""
    insight_type: str
    title: str
    description: str
    
    # 分析结果
    network_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # 关键发现
    key_findings: List[str] = field(default_factory=list)
    
    # 建议
    recommendations: List[str] = field(default_factory=list)
    
    # 置信度
    confidence: float = 0.0

class GraphTheoryEngine:
    """
    图论分析引擎
    
    提供基于图论的实体关系分析能力,
    支持知识图谱,供应链,社交网络等场景
    """
    
    def __init__(self):
        self.graph: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.reverse_graph: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.nodes: Set[str] = set()
        self.edges: Set[Tuple[str, str]] = set()
        self.is_directed: bool = False
        self.weights: Dict[Tuple[str, str], float] = {}
    
    def add_node(self, node: str):
        """添加节点"""
        self.nodes.add(node)
    
    def add_edge(self, from_node: str, to_node: str, weight: float = 1.0):
        """添加边"""
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        self.graph[from_node].append((to_node, weight))
        self.reverse_graph[to_node].append((from_node, weight))
        self.edges.add((from_node, to_node))
        self.weights[(from_node, to_node)] = weight
        
        if not self.is_directed:
            self.graph[to_node].append((from_node, weight))
            self.reverse_graph[from_node].append((to_node, weight))
            self.edges.add((to_node, from_node))
            self.weights[(to_node, from_node)] = weight
    
    def build_from_relations(self, relations: List[Tuple[str, str, float]]):
        """
        从关系列表构建图
        
        Args:
            relations: [(实体1, 实体2, 权重), ...]
        """
        for r in relations:
            if len(r) == 3:
                self.add_edge(r[0], r[1], r[2])
            else:
                self.add_edge(r[0], r[1])
    
    def bfs(self, start: str) -> List[str]:
        """广度优先搜索"""
        if start not in self.nodes:
            return []
        
        visited = set()
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            result.append(node)
            
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start: str) -> List[str]:
        """深度优先搜索"""
        if start not in self.nodes:
            return []
        
        visited = set()
        stack = [start]
        result = []
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            result.append(node)
            
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return result
    
    def dijkstra(self, start: str, end: str = None) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Dijkstra最短路径算法
        
        Returns:
            distances: 到所有节点的最短距离
            predecessors: 前驱节点(用于路径重建)
        """
        distances = {node: float('inf') for node in self.nodes}
        predecessors = {node: None for node in self.nodes}
        distances[start] = 0
        
        pq = [(0, start)]
        
        while pq:
            dist, node = heapq.heappop(pq)
            
            if dist > distances[node]:
                continue
            
            for neighbor, weight in self.graph.get(node, []):
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = node
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return distances, predecessors
    
    def find_shortest_path(self, start: str, end: str) -> PathAnalysis:
        """找最短路径"""
        distances, predecessors = self.dijkstra(start, end)
        
        # 重建路径
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors.get(current)
        path.reverse()
        
        if path[0] != start:
            path = []
            distance = float('inf')
        else:
            distance = distances.get(end, float('inf'))
        
        return PathAnalysis(
            source=start,
            target=end,
            shortest_path=path,
            shortest_distance=distance
        )
    
    def find_all_shortest_paths(self, start: str, end: str, max_paths: int = 10) -> PathAnalysis:
        """找所有最短路径(BFS变体)"""
        distances, _ = self.dijkstra(start, end)
        target_distance = distances.get(end, float('inf'))
        
        if target_distance == float('inf'):
            return PathAnalysis(source=start, target=end, path_count=0)
        
        # BFS找所有等长路径
        paths = []
        queue = deque([(start, [start])])
        
        while queue and len(paths) < max_paths:
            node, path = queue.popleft()
            
            if node == end:
                paths.append(path)
                continue
            
            for neighbor, weight in self.graph.get(node, []):
                if distances.get(neighbor, float('inf')) == distances[node] + weight:
                    if neighbor not in path:  # 避免循环
                        queue.append((neighbor, path + [neighbor]))
        
        avg_weight = sum(
            sum(self.weights.get((path[i], path[i+1]), 1) for i in range(len(path)-1)) / len(path)
            for path in paths
        ) / len(paths) if paths else 0
        
        return PathAnalysis(
            source=start,
            target=end,
            shortest_path=paths[0] if paths else [],
            shortest_distance=target_distance,
            all_paths=paths,
            path_count=len(paths),
            average_weight=avg_weight
        )
    
    def calculate_degree_centrality(self) -> Dict[str, float]:
        """计算度中心性"""
        n = len(self.nodes)
        if n <= 1:
            return {node: 0.0 for node in self.nodes}
        
        centrality = {}
        
        if self.is_directed:
            for node in self.nodes:
                degree = len(self.graph.get(node, [])) + len(self.reverse_graph.get(node, []))
                centrality[node] = degree / (2 * (n - 1))
        else:
            for node in self.nodes:
                degree = len(self.graph.get(node, []))
                centrality[node] = degree / (n - 1)
        
        return centrality
    
    def calculate_betweenness_centrality(self, sample_size: int = None) -> Dict[str, float]:
        """计算介数中心性(Brandes算法简化版)"""
        centrality = {node: 0.0 for node in self.nodes}
        nodes_to_process = list(self.nodes)
        
        if sample_size and sample_size < len(nodes_to_process):
            import random
            nodes_to_process = random.sample(nodes_to_process, sample_size)
        
        for source in nodes_to_process:
            # BFS找所有节点的最短路径
            distances, predecessors = self._bfs_all(source)
            
            if not distances or all(d == float('inf') for d in distances.values()):
                continue
            
            # 计算依赖数
            dependency = {node: 0.0 for node in self.nodes}
            dependency[source] = 1.0
            
            # 逆拓扑顺序累加
            nodes_sorted = sorted([n for n in distances if distances[n] != float('inf')], 
                                key=lambda x: distances[x], reverse=True)
            
            for w in nodes_sorted:
                if predecessors.get(w):
                    for v in predecessors[w]:
                        dependency[v] += dependency[w]
            
            for node in nodes_to_process:
                if node != source:
                    centrality[node] += dependency[node]
        
        # 归一化
        n = len(self.nodes)
        if n > 2:
            norm = 2.0 / ((n - 1) * (n - 2))
            centrality = {k: v * norm for k, v in centrality.items()}
        
        return centrality
    
    def _bfs_all(self, start: str) -> Tuple[Dict[str, float], Dict[str, List[str]]]:
        """BFS返回距离和前驱"""
        distances = {node: float('inf') for node in self.nodes}
        predecessors = defaultdict(list)
        distances[start] = 0
        
        queue = deque([start])
        
        while queue:
            node = queue.popleft()
            d = distances[node]
            
            for neighbor, _ in self.graph.get(node, []):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = d + 1
                    queue.append(neighbor)
                if distances[neighbor] == d + 1:
                    predecessors[neighbor].append(node)
        
        return distances, dict(predecessors)
    
    def calculate_closeness_centrality(self) -> Dict[str, float]:
        """计算接近中心性"""
        centrality = {}
        
        for node in self.nodes:
            distances, _ = self.dijkstra(node)
            reachable = [d for d in distances.values() if d != float('inf') and d > 0]
            
            if reachable:
                avg_distance = sum(reachable) / len(reachable)
                centrality[node] = len(reachable) / sum(reachable) if sum(reachable) > 0 else 0
            else:
                centrality[node] = 0
        
        return centrality
    
    def pagerank(self, damping: float = 0.85, iterations: int = 100, tol: float = 1e-6) -> Dict[str, float]:
        """PageRank算法"""
        n = len(self.nodes)
        if n == 0:
            return {}
        
        nodes_list = list(self.nodes)
        
        # init
        ranks = {node: 1.0 / n for node in nodes_list}
        
        for _ in range(iterations):
            new_ranks = {}
            
            for node in nodes_list:
                # 收集所有指向该节点的节点的贡献
                contribution = 0
                for source in nodes_list:
                    if source == node:
                        continue
                    out_links = [e[0] for e in self.graph.get(source, [])]
                    if out_links and node in out_links:
                        contribution += damping * ranks[source] / len(out_links)
                
                # 随机跳转
                new_ranks[node] = (1 - damping) / n + contribution
            
            # 检查收敛
            diff = sum(abs(new_ranks[n] - ranks[n]) for n in nodes_list)
            ranks = new_ranks
            
            if diff < tol:
                break
        
        return ranks
    
    def detect_communities_label_propagation(self) -> List[Community]:
        """标签传播社区检测"""
        labels = {node: i for i, node in enumerate(self.nodes)}
        
        for _ in range(10):  # 迭代次数
            nodes_shuffled = list(self.nodes)
            import random
            random.shuffle(nodes_shuffled)
            
            for node in nodes_shuffled:
                neighbors = [e[0] for e in self.graph.get(node, [])]
                if not neighbors:
                    continue
                
                # 统计邻居标签
                label_counts = defaultdict(int)
                for neighbor in neighbors:
                    label_counts[labels[neighbor]] += 1
                
                # 选择最多的标签
                labels[node] = max(label_counts, key=label_counts.get)
        
        # 整理社区
        community_map = defaultdict(list)
        for node, label in labels.items():
            community_map[label].append(node)
        
        communities = []
        for i, (label, nodes) in enumerate(community_map.items()):
            community = Community(
                community_id=i,
                nodes=nodes,
                size=len(nodes),
                internal_edges=self._count_internal_edges(nodes),
                density=0.0
            )
            communities.append(community)
        
        return communities
    
    def _count_internal_edges(self, nodes: Set[str]) -> int:
        """计算内部边数"""
        count = 0
        for node in nodes:
            for neighbor, _ in self.graph.get(node, []):
                if neighbor in nodes:
                    count += 1
        return count // 2
    
    def analyze_vulnerability(self) -> NetworkVulnerability:
        """分析网络脆弱性"""
        # 找桥接边(删除后会导致不连通的边)
        bridges = self._find_bridges()
        
        # 找关键节点(度中心性高的节点)
        degree_centrality = self.calculate_degree_centrality()
        critical = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        critical_nodes = [n[0] for n in critical[:3]]
        
        # 计算网络metrics
        connectivity = self._calculate_connectivity()
        redundancy = self._calculate_redundancy()
        efficiency = self._calculate_efficiency()
        
        # 脆弱性评分
        vulnerability = (1 - connectivity) * 0.4 + (1 - redundancy) * 0.3 + len(bridges) * 0.3
        vulnerability = min(1.0, vulnerability)
        
        level = "高" if vulnerability > 0.6 else "中" if vulnerability > 0.3 else "低"
        
        return NetworkVulnerability(
            critical_nodes=critical_nodes,
            bridge_edges=bridges,
            connectivity=connectivity,
            redundancy=redundancy,
            efficiency=efficiency,
            vulnerability_score=vulnerability,
            vulnerability_level=level
        )
    
    def _find_bridges(self) -> List[Tuple[str, str]]:
        """找桥接边(Tarjan算法简化版)"""
        if not self.is_directed:
            return self._find_bridges_undirected()
        return []
    
    def _find_bridges_undirected(self) -> List[Tuple[str, str]]:
        """无向图找桥"""
        bridges = []
        visited = set()
        disc = {}
        low = {}
        parent = {}
        time = [0]
        
        def dfs(u):
            visited.add(u)
            disc[u] = low[u] = time[0]
            time[0] += 1
            
            for v, _ in self.graph.get(u, []):
                if v not in visited:
                    parent[v] = u
                    dfs(v)
                    low[u] = min(low[u], low[v])
                    
                    if low[v] > disc[u]:
                        bridges.append((min(u, v), max(u, v)))
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])
        
        for node in self.nodes:
            if node not in visited:
                dfs(node)
        
        return bridges
    
    def _calculate_connectivity(self) -> float:
        """计算连通度"""
        if not self.nodes:
            return 0.0
        
        # 使用BFS计算连通分量
        visited = set()
        components = 0
        
        for node in self.nodes:
            if node not in visited:
                self._bfs_collect(node, visited)
                components += 1
        
        if components == 1:
            return 1.0
        
        # 连通度 = 最小割边数 / 节点数
        return max(0, 1.0 - (components - 1) / len(self.nodes))
    
    def _bfs_collect(self, start: str, visited: set):
        """BFS收集可达节点"""
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
    
    def _calculate_redundancy(self) -> float:
        """计算冗余度"""
        n = len(self.nodes)
        if n < 2:
            return 0.0
        
        max_edges = n * (n - 1) / 2
        actual_edges = len(self.edges) / (2 if not self.is_directed else 1)
        
        return actual_edges / max_edges if max_edges > 0 else 0
    
    def _calculate_efficiency(self) -> float:
        """计算网络效率"""
        if not self.nodes:
            return 0.0
        
        total_distance = 0
        pairs = 0
        
        for source in self.nodes:
            distances, _ = self.dijkstra(source)
            for target, dist in distances.items():
                if source != target and dist != float('inf'):
                    total_distance += 1 / dist
                    pairs += 1
        
        if pairs == 0:
            return 0.0
        
        return total_distance / pairs
    
    def analyze_entity_relationships(self, entity: str) -> GraphTheoryInsight:
        """
        分析实体关系
        
        Args:
            entity: 目标实体
            
        Returns:
            图论智慧洞察
        """
        if entity not in self.nodes:
            return GraphTheoryInsight(
                insight_type="entity_analysis",
                title=f"实体 {entity} 不存在",
                description="该实体未在关系网络中找到",
                confidence=0.0
            )
        
        # 基本信息
        neighbors = [e[0] for e in self.graph.get(entity, [])]
        in_neighbors = [e[0] for e in self.reverse_graph.get(entity, [])]
        degree = len(neighbors) + len(in_neighbors)
        
        # 中心性
        degree_centrality = self.calculate_degree_centrality()
        betweenness = self.calculate_betweenness_centrality()
        pagerank_scores = self.pagerank()
        
        # 网络位置分析
        distances, _ = self.dijkstra(entity)
        avg_distance = sum(d for d in distances.values() if d != float('inf')) / len(distances)
        
        # 影响力评估
        influence_score = (
            degree_centrality.get(entity, 0) * 0.3 +
            betweenness.get(entity, 0) * 0.3 +
            pagerank_scores.get(entity, 0) * 0.4
        )
        
        level = "高" if influence_score > 0.3 else "中" if influence_score > 0.1 else "低"
        
        # 关键发现
        findings = [
            f"直接关联实体: {len(neighbors)} 个",
            f"被关联实体: {len(in_neighbors)} 个",
            f"网络中心性得分: {influence_score:.4f}",
            f"平均距离: {avg_distance:.2f}"
        ]
        
        # 建议
        recommendations = [
            f"该实体在网络中处于{level}影响力位置",
            "建议加强与核心节点的连接" if influence_score < 0.2 else "可作为关键枢纽发挥连接作用"
        ]
        
        return GraphTheoryInsight(
            insight_type="entity_analysis",
            title=f"实体 {entity} 关系分析",
            description=f"度={degree}, 影响力={level}",
            network_metrics={
                "degree": degree,
                "centrality": influence_score,
                "pagerank": pagerank_scores.get(entity, 0),
                "avg_distance": avg_distance
            },
            key_findings=findings,
            recommendations=recommendations,
            confidence=0.9
        )
    
    def compare_entities(self, entities: List[str]) -> Dict[str, Any]:
        """
        比较多个实体的网络位置
        
        Args:
            entities: 实体列表
            
        Returns:
            比较结果
        """
        degree_centrality = self.calculate_degree_centrality()
        betweenness = self.calculate_betweenness_centrality()
        pagerank_scores = self.pagerank()
        
        comparisons = []
        
        for entity in entities:
            if entity not in self.nodes:
                continue
            
            comparisons.append({
                "entity": entity,
                "degree": len(self.graph.get(entity, [])) + len(self.reverse_graph.get(entity, [])),
                "degree_centrality": degree_centrality.get(entity, 0),
                "betweenness": betweenness.get(entity, 0),
                "pagerank": pagerank_scores.get(entity, 0),
                "influence": (
                    degree_centrality.get(entity, 0) * 0.3 +
                    betweenness.get(entity, 0) * 0.3 +
                    pagerank_scores.get(entity, 0) * 0.4
                )
            })
        
        # 排序
        comparisons.sort(key=lambda x: x["influence"], reverse=True)
        
        return {
            "rankings": comparisons,
            "most_influential": comparisons[0] if comparisons else None,
            "least_influential": comparisons[-1] if comparisons else None
        }
    
    def get_network_summary(self) -> Dict[str, Any]:
        """get网络摘要"""
        degree_centrality = self.calculate_degree_centrality()
        
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "density": len(self.edges) / (len(self.nodes) * (len(self.nodes) - 1)) if len(self.nodes) > 1 else 0,
            "avg_degree": sum(len(self.graph.get(n, [])) for n in self.nodes) / len(self.nodes) if self.nodes else 0,
            "max_degree": max(len(self.graph.get(n, [])) for n in self.nodes) if self.nodes else 0,
            "is_directed": self.is_directed
        }

# ==================== 导出 ====================

__all__ = [
    'GraphTheoryEngine',
    'CentralityType',
    'CommunityDetectionMethod',
    'PathAnalysis',
    'InfluenceAnalysis',
    'Community',
    'NetworkVulnerability',
    'GraphTheoryInsight',
]
