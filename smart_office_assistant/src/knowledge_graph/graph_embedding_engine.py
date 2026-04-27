"""
__all__ = [
    'add_edge',
    'add_node',
    'compute_graph_embedding',
    'compute_similarity',
    'find_related_by_path',
    'find_similar_nodes',
    'get_node_embedding',
    'get_statistics',
    'get_subgraph_embeddings',
    'train_node_embeddings',
    'visualize_embeddings',
]

图嵌入引擎 - 知识图谱向量化和语义理解

功能:
- Node2Vec节点嵌入
- 图神经网络 (GNN) 支持
- 图语义检索
- 图相似度计算

作者: Somn AI
版本: v4.0.0
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, deque
import random
import logging
import json

logger = logging.getLogger(__name__)

class GraphEmbeddingEngine:
    """
    图嵌入引擎
    
    核心算法:
    1. Node2Vec - 保留图结构信息
    2. Random Walk - generate节点序列
    3. Skip-gram - 训练嵌入向量
    4. 图相似度计算
    """
    
    def __init__(self, embedding_dim: int = 128):
        """
        init图嵌入引擎
        
        Args:
            embedding_dim: 嵌入维度
        """
        self.embedding_dim = embedding_dim
        
        # 图结构
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.node_embeddings: Dict[str, np.ndarray] = {}
        
        # Node2Vec参数
        self.node2vec_params = {
            'walk_length': 40,      # 随机游走长度
            'num_walks': 10,        # 每个节点的游走次数
            'p': 1.0,              # 回参参数
            'q': 1.0,              # 进出参数
            'window_size': 5       # Skip-gram窗口大小
        }
        
        # 训练参数
        self.learning_rate = 0.025
        self.num_epochs = 10
        
        logger.info(f"图嵌入引擎init完成 (维度: {embedding_dim})")
    
    def add_node(self, node_id: str, node_type: str = "default", 
                 attributes: Optional[Dict] = None):
        """
        添加节点
        
        Args:
            node_id: 节点ID
            node_type: 节点类型
            attributes: 节点属性
        """
        if node_id not in self.graph:
            self.graph[node_id] = []
        
        # init节点属性
        if not hasattr(self, 'node_attributes'):
            self.node_attributes = {}
        
        self.node_attributes[node_id] = {
            'type': node_type,
            'attributes': attributes or {}
        }
    
    def add_edge(self, source: str, target: str, 
                 edge_type: str = "default", weight: float = 1.0):
        """
        添加边
        
        Args:
            source: 源节点
            target: 目标节点
            edge_type: 边类型
            weight: 边权重
        """
        if source not in self.graph:
            self.add_node(source)
        if target not in self.graph:
            self.add_node(target)
        
        self.graph[source].append(target)
        self.graph[target].append(source)  # 无向图
        
        # 记录边信息
        if not hasattr(self, 'edge_attributes'):
            self.edge_attributes = {}
        
        edge_key = tuple(sorted([source, target]))
        self.edge_attributes[edge_key] = {
            'type': edge_type,
            'weight': weight
        }
    
    def train_node_embeddings(self, method: str = "node2vec") -> Dict[str, np.ndarray]:
        """
        训练节点嵌入
        
        Args:
            method: 嵌入方法 ('node2vec', 'random')
            
        Returns:
            节点嵌入字典
        """
        logger.info(f"开始训练节点嵌入 (方法: {method})...")
        
        if method == "node2vec":
            self._train_node2vec()
        elif method == "random":
            self._train_random()
        else:
            raise ValueError(f"未知嵌入方法: {method}")
        
        logger.info(f"节点嵌入训练完成 (节点数: {len(self.node_embeddings)})")
        return self.node_embeddings
    
    def _train_node2vec(self):
        """使用Node2Vec算法训练"""
        # generate随机游走序列
        walks = self._generate_random_walks()
        
        # init嵌入
        nodes = list(self.graph.keys())
        for node in nodes:
            self.node_embeddings[node] = np.random.randn(self.embedding_dim) * 0.01
        
        # Skip-gram训练 (简化版)
        for epoch in range(self.num_epochs):
            for walk in walks:
                self._update_embeddings(walk, epoch)
        
        logger.info(f"Node2Vec训练完成 (游走数: {len(walks)})")
    
    def _generate_random_walks(self) -> List[List[str]]:
        """generate随机游走序列"""
        walks = []
        nodes = list(self.graph.keys())
        
        for node in nodes:
            for _ in range(self.node2vec_params['num_walks']):
                walk = self._random_walk(node)
                walks.append(walk)
        
        return walks
    
    def _random_walk(self, start_node: str) -> List[str]:
        """执行一次随机游走"""
        walk = [start_node]
        current_node = start_node
        
        for _ in range(self.node2vec_params['walk_length'] - 1):
            neighbors = self.graph[current_node]
            
            if not neighbors:
                break
            
            # 简化的邻居选择 (可以扩展为Node2Vec的biased walk)
            next_node = random.choice(neighbors)
            walk.append(next_node)
            current_node = next_node
        
        return walk
    
    def _update_embeddings(self, walk: List[str], epoch: int):
        """
        Skip-gram更新嵌入 (简化版)
        
        Args:
            walk: 随机游走序列
            epoch: 当前轮次
        """
        # 动态学习率
        current_lr = self.learning_rate * (1 - epoch / self.num_epochs)
        
        for i, center_node in enumerate(walk):
            # get上下文窗口
            start = max(0, i - self.node2vec_params['window_size'])
            end = min(len(walk), i + self.node2vec_params['window_size'] + 1)
            context = walk[start:i] + walk[i+1:end]
            
            # 更新中心节点和上下文节点
            if center_node not in self.node_embeddings:
                self.node_embeddings[center_node] = np.random.randn(self.embedding_dim) * 0.01
            
            center_emb = self.node_embeddings[center_node]
            
            for context_node in context:
                if context_node not in self.node_embeddings:
                    self.node_embeddings[context_node] = np.random.randn(self.embedding_dim) * 0.01
                
                context_emb = self.node_embeddings[context_node]
                
                # 计算相似度
                similarity = np.dot(center_emb, context_emb)
                
                # 简化的梯度更新
                error = 1.0 - similarity
                grad = error * context_emb
                
                # 更新中心节点
                self.node_embeddings[center_node] += current_lr * grad
                
                # 归一化
                self.node_embeddings[center_node] /= np.linalg.norm(
                    self.node_embeddings[center_node]
                )
    
    def _train_random(self):
        """随机init嵌入 (用于测试)"""
        for node in self.graph.keys():
            self.node_embeddings[node] = np.random.randn(self.embedding_dim)
        
        logger.info("随机嵌入init完成")
    
    def get_node_embedding(self, node_id: str) -> Optional[np.ndarray]:
        """
        get节点嵌入向量
        
        Args:
            node_id: 节点ID
            
        Returns:
            嵌入向量
        """
        return self.node_embeddings.get(node_id)
    
    def compute_similarity(self, node1: str, node2: str) -> float:
        """
        计算两个节点的相似度 (余弦相似度)
        
        Args:
            node1: 节点1
            node2: 节点2
            
        Returns:
            相似度分数 (0-1)
        """
        emb1 = self.node_embeddings.get(node1)
        emb2 = self.node_embeddings.get(node2)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        # 余弦相似度
        similarity = np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        )
        
        return float(similarity)
    
    def find_similar_nodes(self, node_id: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        找到最相似的节点
        
        Args:
            node_id: 查询节点
            top_k: 返回前k个
            
        Returns:
            (节点ID, 相似度)列表
        """
        if node_id not in self.node_embeddings:
            return []
        
        query_emb = self.node_embeddings[node_id]
        similarities = []
        
        for other_node, other_emb in self.node_embeddings.items():
            if other_node != node_id:
                similarity = np.dot(query_emb, other_emb) / (
                    np.linalg.norm(query_emb) * np.linalg.norm(other_emb)
                )
                similarities.append((other_node, float(similarity)))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def find_related_by_path(self, start_node: str, end_node: str, 
                             max_length: int = 5) -> List[List[str]]:
        """
        基于路径找到相关节点
        
        Args:
            start_node: 起始节点
            end_node: 目标节点
            max_length: 最大路径长度
            
        Returns:
            路径列表
        """
        paths = []
        self._find_all_paths(start_node, end_node, [], paths, max_length)
        
        return paths
    
    def _find_all_paths(self, current: str, target: str, path: List[str], 
                       paths: List[List[str]], max_length: int):
        """递归查找所有路径"""
        path = path + [current]
        
        if current == target:
            paths.append(path)
            return
        
        if len(path) >= max_length:
            return
        
        for neighbor in self.graph[current]:
            if neighbor not in path:
                self._find_all_paths(neighbor, target, path, paths, max_length)
    
    def compute_graph_embedding(self, nodes: Optional[List[str]] = None) -> np.ndarray:
        """
        计算图或子图的嵌入向量
        
        Args:
            nodes: 节点列表 (None表示整个图)
            
        Returns:
            图嵌入向量
        """
        if nodes is None:
            nodes = list(self.graph.keys())
        
        # 聚合节点嵌入 (简单平均)
        embeddings = []
        for node in nodes:
            if node in self.node_embeddings:
                embeddings.append(self.node_embeddings[node])
        
        if embeddings:
            graph_emb = np.mean(embeddings, axis=0)
            return graph_emb
        else:
            return np.zeros(self.embedding_dim)
    
    def get_subgraph_embeddings(self, communities: List[List[str]]) -> Dict[str, np.ndarray]:
        """
        get多个子图的嵌入
        
        Args:
            communities: 社区列表
            
        Returns:
            子图嵌入字典
        """
        subgraph_embs = {}
        
        for i, community in enumerate(communities):
            subgraph_id = f"community_{i}"
            subgraph_embs[subgraph_id] = self.compute_graph_embedding(community)
        
        return subgraph_embs
    
    def visualize_embeddings(self, nodes: Optional[List[str]] = None, 
                           output_file: str = "graph_embeddings.json"):
        """
        导出嵌入用于可视化
        
        Args:
            nodes: 节点列表 (None表示全部)
            output_file: 输出文件
        """
        if nodes is None:
            nodes = list(self.node_embeddings.keys())
        
        visualization_data = {
            'nodes': [],
            'edges': []
        }
        
        # 添加节点
        for node in nodes:
            if node in self.node_embeddings:
                visualization_data['nodes'].append({
                    'id': node,
                    'embedding': self.node_embeddings[node].tolist(),
                    'type': self.node_attributes.get(node, {}).get('type', 'default')
                })
        
        # 添加边
        for node in nodes:
            for neighbor in self.graph[node]:
                if neighbor > node:  # 避免重复
                    visualization_data['edges'].append({
                        'source': node,
                        'target': neighbor
                    })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(visualization_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"嵌入可视化数据已导出: {output_file}")
    
    def get_statistics(self) -> Dict:
        """get统计信息"""
        return {
            'num_nodes': len(self.graph),
            'num_edges': sum(len(neighbors) for neighbors in self.graph.values()) // 2,
            'embedding_dim': self.embedding_dim,
            'trained_nodes': len(self.node_embeddings),
            'avg_degree': sum(len(neighbors) for neighbors in self.graph.values()) / len(self.graph) if self.graph else 0
        }
