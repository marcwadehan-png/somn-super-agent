"""数学智慧核心 - 图论分析引擎"""

import heapq
from collections import deque
from typing import Dict, List, Tuple, Set

from ._mw_enums import GraphType
from ._mw_dataclasses import GraphAnalysis

__all__ = [
    'add_edge',
    'add_undirected_edge',
    'analyze',
    'bfs',
    'dfs',
    'find_shortest_path',
]

class GraphAnalyzer:
    """图论分析引擎 - 分析实体关系网络"""
    
    def __init__(self):
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}
        self.nodes: Set[str] = set()
        self.is_directed: bool = False
    
    def add_edge(self, from_node: str, to_node: str, weight: float = 1.0):
        """添加边"""
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        
        if from_node not in self.adjacency_list:
            self.adjacency_list[from_node] = []
        self.adjacency_list[from_node].append((to_node, weight))
    
    def add_undirected_edge(self, node1: str, node2: str, weight: float = 1.0):
        """添加无向边"""
        self.add_edge(node1, node2, weight)
        self.add_edge(node2, node1, weight)
    
    def analyze(self) -> GraphAnalysis:
        """分析图结构"""
        edge_count = sum(len(neighbors) for neighbors in self.adjacency_list.values())
        
        # 如果是有向图,边数要除以2
        if not self.is_directed:
            edge_count //= 2
        
        # 计算密度
        n = len(self.nodes)
        max_edges = n * (n - 1) / 2 if n > 1 else 1
        density = edge_count / max_edges if max_edges > 0 else 0
        
        # BFS检查连通性
        is_connected, components = self._find_connected_components()
        
        # 计算中心性
        centrality = self._calculate_centrality()
        
        # 寻找最短路径
        shortest_paths = self._find_all_shortest_paths()
        
        return GraphAnalysis(
            graph_type=self._determine_graph_type(),
            node_count=n,
            edge_count=edge_count,
            density=density,
            is_connected=is_connected,
            connected_components=components,
            centrality=centrality,
            shortest_paths=shortest_paths
        )
    
    def _find_connected_components(self) -> Tuple[bool, int]:
        """使用BFS找连通分量"""
        if not self.nodes:
            return True, 0
        
        visited = set()
        components = 0
        
        for start in self.nodes:
            if start not in visited:
                # BFS
                queue = deque([start])
                while queue:
                    node = queue.popleft()
                    if node in visited:
                        continue
                    visited.add(node)
                    
                    for neighbor, _ in self.adjacency_list.get(node, []):
                        if neighbor not in visited:
                            queue.append(neighbor)
                    # 对于无向图,也检查反向
                    if not self.is_directed:
                        for neighbor, _ in self.adjacency_list.get(node, []):
                            if neighbor not in visited:
                                queue.append(neighbor)
                
                components += 1
        
        return components == 1, components
    
    def _calculate_centrality(self) -> Dict[str, float]:
        """计算度中心性"""
        centrality = {}
        
        for node in self.nodes:
            # 出度 + 入度(对于无向图就是邻居数)
            degree = len(self.adjacency_list.get(node, []))
            # 如果是无向图,不需要额外计算
            
            n = len(self.nodes)
            if n > 1:
                centrality[node] = degree / (n - 1)
            else:
                centrality[node] = 0
        
        return centrality
    
    def _find_all_shortest_paths(self) -> Dict[Tuple[str, str], float]:
        """使用Dijkstra算法找所有最短路径"""
        shortest_paths = {}
        
        for start in self.nodes:
            dist = {node: float('inf') for node in self.nodes}
            dist[start] = 0
            pq = [(0, start)]
            
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                
                for v, weight in self.adjacency_list.get(u, []):
                    if dist[u] + weight < dist[v]:
                        dist[v] = dist[u] + weight
            
            for target in self.nodes:
                if start != target:
                    shortest_paths[(start, target)] = dist[target]
        
        return shortest_paths
    
    def _determine_graph_type(self) -> GraphType:
        """确定图的类型"""
        n = len(self.nodes)
        edge_count = sum(len(neighbors) for neighbors in self.adjacency_list.values())
        
        # 完全图检查
        max_edges = n * (n - 1) / 2
        if edge_count / max_edges > 0.9:
            return GraphType.COMPLETE
        
        # 树检查
        if edge_count == n - 1 and self._is_connected_dfs():
            return GraphType.TREE
        
        return GraphType.DIRECTED if self.is_directed else GraphType.UNDIRECTED
    
    def _is_connected_dfs(self) -> bool:
        """DFS检查连通性"""
        if not self.nodes:
            return True
        
        visited = set()
        stack = [next(iter(self.nodes))]
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor, _ in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return len(visited) == len(self.nodes)
    
    def bfs(self, start: str) -> List[str]:
        """广度优先搜索"""
        visited = set()
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            result.append(node)
            
            for neighbor, _ in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start: str) -> List[str]:
        """深度优先搜索"""
        visited = set()
        stack = [start]
        result = []
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            result.append(node)
            
            for neighbor, _ in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return result
    
    def find_shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """Dijkstra找最短路径"""
        dist = {node: float('inf') for node in self.nodes}
        prev = {node: None for node in self.nodes}
        dist[start] = 0
        
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            
            if u == end:
                break
            
            for v, weight in self.adjacency_list.get(u, []):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        # 重建路径
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()
        
        if path[0] != start:
            return [], float('inf')
        
        return path, dist[end]
