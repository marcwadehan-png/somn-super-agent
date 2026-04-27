"""
__all__ = [
    'add_knowledge',
    'coding_efficiency',
    'compression_ratio',
    'compute_knowledge_probability',
    'compute_mutual_information',
    'compute_retrieval_metrics',
    'conditional_entropy',
    'create_info_retrieval_system',
    'entropy',
    'estimate_information_rate',
    'get_information_metrics',
    'get_statistics',
    'huffman_like_length',
    'index_knowledge',
    'joint_entropy',
    'mutual_information',
    'normalized_mutual_information',
    'optimize_index',
    'optimize_knowledge_probability',
    'quick_retrieve',
    'retrieve',
    'retrieve_by_mutual_info',
    'self_information',
]

信息论检索优化模块 v1.0
Information Theory Retrieval System v1.0

核心概念mapping:
- 熵 (Entropy) → 知识不确定性
- 互信息 (Mutual Information) → 查询-结果相关度
- 信息率 (Information Rate) → 检索效率
- 编码效率 → 知识压缩比

作者: Somn AI System
日期: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import math
from collections import defaultdict
import hashlib

@dataclass
class KnowledgeDistribution:
    """知识分布"""
    knowledge_id: str
    content: str
    
    # 概率分布
    probability: float = 0.0           # 先验概率
    
    # 信息量
    self_information: float = 0.0      # 自信息 I(x) = -log₂P(x)
    
    # 编码
    code_length: int = 0               # 编码长度
    encoded_content: Optional[str] = None
    
    # 统计
    access_count: int = 0
    last_access: Optional[datetime] = None
    
    # 互信息
    mutual_info_with_query: Dict[str, float] = field(default_factory=dict)

@dataclass
class InformationMetrics:
    """信息论metrics"""
    entropy: float = 0.0              # 熵 H(X)
    joint_entropy: float = 0.0        # 联合熵 H(X,Y)
    conditional_entropy: float = 0.0   # 条件熵 H(X|Y)
    mutual_information: float = 0.0   # 互信息 I(X;Y)
    
    # 编码metrics
    coding_efficiency: float = 0.0     # 编码效率
    redundancy: float = 0.0           # 冗余度
    compression_ratio: float = 0.0    # 压缩比
    
    # 检索metrics
    precision: float = 0.0            # 精确率
    recall: float = 0.0              # 召回率
    f1_score: float = 0.0             # F1分数

class EntropyCalculator:
    """
    熵计算器
    
    熵的物理意义: 衡量不确定性或信息量的大小
    
    H(X) = -Σ p(x) log₂ p(x)
    """
    
    @staticmethod
    def entropy(probabilities: np.ndarray, base: float = 2.0) -> float:
        """
        计算香农熵
        
        Args:
            probabilities: 概率分布
            base: 对数底 (2=bits, e=nats, 10=bans)
            
        Returns:
            熵值
        """
        # 过滤掉0概率
        p = probabilities[probabilities > 0]
        if len(p) == 0:
            return 0.0
        
        return -np.sum(p * np.log(p) / np.log(base))
    
    @staticmethod
    def joint_entropy(distributions: List[np.ndarray]) -> float:
        """
        计算联合熵
        
        H(X,Y) = -Σ p(x,y) log₂ p(x,y)
        """
        # 展平为联合分布
        joint = np.zeros(1)
        for dist in distributions:
            joint = np.outer(joint, dist) if len(joint) > 1 else dist
        
        return EntropyCalculator.entropy(joint.flatten())
    
    @staticmethod
    def conditional_entropy(p_xy: np.ndarray, p_y: np.ndarray) -> float:
        """
        计算条件熵
        
        H(X|Y) = H(X,Y) - H(Y)
        """
        joint = EntropyCalculator.joint_entropy([p_xy, p_y])
        h_y = EntropyCalculator.entropy(p_y)
        return max(0, joint - h_y)
    
    @staticmethod
    def mutual_information(p_x: np.ndarray, p_y: np.ndarray, 
                         p_xy: np.ndarray) -> float:
        """
        计算互信息
        
        I(X;Y) = H(X) + H(Y) - H(X,Y)
             = H(X) - H(X|Y)
             = H(Y) - H(Y|X)
        """
        h_x = EntropyCalculator.entropy(p_x)
        h_y = EntropyCalculator.entropy(p_y)
        h_xy = EntropyCalculator.joint_entropy([p_x, p_y])
        
        return max(0, h_x + h_y - h_xy)
    
    @staticmethod
    def normalized_mutual_information(p_x: np.ndarray, p_y: np.ndarray,
                                    p_xy: np.ndarray) -> float:
        """
        归一化互信息 (0-1)
        
        NMI = I(X;Y) / sqrt(H(X) * H(Y))
        """
        mi = EntropyCalculator.mutual_information(p_x, p_y, p_xy)
        h_x = EntropyCalculator.entropy(p_x)
        h_y = EntropyCalculator.entropy(p_y)
        
        if h_x * h_y == 0:
            return 0.0
        
        return mi / np.sqrt(h_x * h_y)

class InformationCoding:
    """
    信息编码 - 基于信息论的压缩编码
    
    核心原理:
    1. 高概率事件用短码
    2. 低概率事件用长码
    3. 编码效率接近熵
    """
    
    @staticmethod
    def self_information(probability: float, base: float = 2.0) -> float:
        """
        计算自信息
        
        I(x) = -log₂ P(x)
        
        物理意义: 事件x发生所带来的信息量
        """
        if probability <= 0:
            return float('inf')
        return -math.log(probability, base)
    
    @staticmethod
    def huffman_like_length(frequency: float, total: float) -> float:
        """
        计算类似Huffman的编码长度
        
        简化模型: length ≈ -log₂(frequency/total)
        """
        if frequency <= 0 or total <= 0:
            return float('inf')
        
        p = frequency / total
        return math.ceil(-math.log(p, 2)) if p > 0 else float('inf')
    
    @staticmethod
    def coding_efficiency(actual_length: float, entropy: float) -> float:
        """
        计算编码效率
        
        η = H(X) / L
        
        其中 H(X) 是熵, L 是平均码长
        """
        if actual_length == 0:
            return 0.0
        return min(1.0, entropy / actual_length)
    
    @staticmethod
    def compression_ratio(original: int, compressed: int) -> float:
        """计算压缩比"""
        if compressed == 0:
            return 0.0
        return original / compressed

class MutualInformationRetrieval:
    """
    互信息检索 - 基于互信息的知识检索
    
    原理:
    I(Query; Knowledge) = H(Knowledge) - H(Knowledge | Query)
    
    互信息越大, 查询与知识的关联越强
    """
    
    def __init__(self, knowledge_base: Optional[List[KnowledgeDistribution]] = None):
        self.knowledge_base = knowledge_base or []
        self.query_history: List[Dict] = []
        
        # 统计
        self.total_entropy = 0.0
        self.average_mutual_info = 0.0
    
    def add_knowledge(self, knowledge: KnowledgeDistribution):
        """添加知识"""
        self.knowledge_base.append(knowledge)
    
    def compute_knowledge_probability(self) -> np.ndarray:
        """计算知识的概率分布"""
        if not self.knowledge_base:
            return np.array([0.0])
        
        total_access = sum(k.access_count for k in self.knowledge_base)
        
        if total_access == 0:
            # 均匀分布
            n = len(self.knowledge_base)
            return np.ones(n) / n
        
        # 基于访问频率的概率
        probs = np.array([k.access_count / total_access for k in self.knowledge_base])
        return probs
    
    def compute_mutual_information(self, query: str,
                                  relevance_scores: Dict[str, float]) -> Dict[str, float]:
        """
        计算查询与各知识的互信息
        
        Args:
            query: 查询字符串
            relevance_scores: {knowledge_id: relevance_score}
            
        Returns:
            {knowledge_id: mutual_information}
        """
        if not self.knowledge_base:
            return {}
        
        # 计算知识分布的熵
        knowledge_probs = self.compute_knowledge_probability()
        knowledge_entropy = EntropyCalculator.entropy(knowledge_probs)
        
        # 计算给定查询后的条件熵
        mutual_infos = {}
        
        for i, knowledge in enumerate(self.knowledge_base):
            kid = knowledge.knowledge_id
            
            # 计算查询-知识的相关度
            relevance = relevance_scores.get(kid, 0.0)
            
            # 简化的互信息计算
            # I(Q;K) ≈ -log(1 - relevance) for small relevance
            if relevance < 1.0:
                mi = -math.log2(1 - relevance + 1e-10)
            else:
                mi = float('inf')  # 完全相关
            
            mutual_infos[kid] = min(mi, knowledge_entropy)
        
        # 更新统计
        self.total_entropy = knowledge_entropy
        if mutual_infos:
            self.average_mutual_info = np.mean(list(mutual_infos.values()))
        
        return mutual_infos
    
    def retrieve_by_mutual_info(self, query: str,
                               relevance_scores: Dict[str, float],
                               top_k: int = 10) -> List[Tuple[str, float]]:
        """
        基于互信息的检索
        
        互信息越大, 表示查询与知识的关联越强
        """
        mutual_infos = self.compute_mutual_information(query, relevance_scores)
        
        # 排序
        sorted_items = sorted(
            mutual_infos.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_items[:top_k]
    
    def optimize_knowledge_probability(self) -> np.ndarray:
        """
        优化知识概率分布
        
        基于最大化互信息的目标, 调整知识的重要性
        """
        probs = self.compute_knowledge_probability()
        
        # get各知识的自信息
        self_info = [
            InformationCoding.self_information(p) 
            for p in probs
        ]
        
        # 高自信息的知识应该获得更高的概率(需要更多访问)
        # 这里使用一个简单的指数mapping
        weights = np.exp(-np.array(self_info) / 10)
        new_probs = weights / weights.sum()
        
        return new_probs
    
    def get_information_metrics(self) -> InformationMetrics:
        """get信息论metrics"""
        probs = self.compute_knowledge_probability()
        
        return InformationMetrics(
            entropy=EntropyCalculator.entropy(probs),
            mutual_information=self.average_mutual_info,
            coding_efficiency=self.average_mutual_info / max(1, self.total_entropy) 
                              if self.total_entropy > 0 else 0
        )

class InformationTheoryRetrievalSystem:
    """
    信息论检索系统
    
    整合<Theoretical Neuroscience>Ch4的信息论理论与知识检索:
    
    1. 熵 (Entropy) - 衡量知识的不确定性
    2. 互信息 (Mutual Information) - 衡量查询-知识的关联
    3. 自信息 (Self-Information) - 衡量单条知识的信息量
    4. 编码效率 - 衡量知识表示的效率
    5. 信息率 - 衡量检索效率
    """
    
    def __init__(self):
        self.knowledge: Dict[str, KnowledgeDistribution] = {}
        self.query_history: List[Dict[str, Any]] = []
        
        # 组件
        self.entropy_calc = EntropyCalculator()
        self.coding = InformationCoding()
        self.mi_retrieval = MutualInformationRetrieval()
        
        # 统计
        self.total_retrievals = 0
        self.total_information_retrieved = 0.0
    
    def index_knowledge(self, knowledge_id: str, content: str):
        """索引知识"""
        # 计算先验概率 (基于内容长度)
        total_len = sum(len(k.content) for k in self.knowledge.values())
        prob = len(content) / max(1, total_len) if total_len > 0 else 1.0 / max(1, len(self.knowledge))
        
        # 计算自信息
        self_info = InformationCoding.self_information(prob)
        
        kd = KnowledgeDistribution(
            knowledge_id=knowledge_id,
            content=content,
            probability=prob,
            self_information=self_info
        )
        
        self.knowledge[knowledge_id] = kd
        self.mi_retrieval.add_knowledge(kd)
    
    def retrieve(self, query: str, 
                relevance_scores: Dict[str, float],
                top_k: int = 10) -> List[Dict[str, Any]]:
        """
        检索
        
        使用互信息排序
        """
        # 基于互信息检索
        mi_results = self.mi_retrieval.retrieve_by_mutual_info(
            query, relevance_scores, top_k
        )
        
        # 构建结果
        results = []
        for kid, mi in mi_results:
            if kid in self.knowledge:
                kd = self.knowledge[kid]
                
                # 更新访问统计
                kd.access_count += 1
                kd.last_access = datetime.now()
                
                results.append({
                    'knowledge_id': kid,
                    'content': kd.content,
                    'mutual_information': mi,
                    'self_information': kd.self_information,
                    'access_count': kd.access_count,
                    'relevance': relevance_scores.get(kid, 0.0)
                })
        
        self.total_retrievals += 1
        
        return results
    
    def compute_retrieval_metrics(self, results: List[Dict],
                                 relevant_ids: List[str]) -> InformationMetrics:
        """
        计算检索metrics
        
        基于信息论:
        - 精确率: P(relevant | retrieved)
        - 召回率: P(retrieved | relevant)
        - F1: 调和平均
        """
        if not results or not relevant_ids:
            return InformationMetrics()
        
        retrieved_ids = [r['knowledge_id'] for r in results]
        
        true_positives = len(set(retrieved_ids) & set(relevant_ids))
        
        precision = true_positives / len(retrieved_ids) if retrieved_ids else 0
        recall = true_positives / len(relevant_ids) if relevant_ids else 0
        
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        # 信息论metrics
        mi = self.mi_retrieval.get_information_metrics()
        
        return InformationMetrics(
            precision=precision,
            recall=recall,
            f1_score=f1,
            entropy=mi.entropy,
            mutual_information=mi.mutual_information,
            coding_efficiency=mi.coding_efficiency
        )
    
    def estimate_information_rate(self, retrieval_time: float) -> float:
        """
        估算信息率
        
        R = I / T
        
        I: get的信息量
        T: 检索时间
        """
        avg_info = self.total_information_retrieved / max(1, self.total_retrievals)
        return avg_info / max(0.001, retrieval_time)
    
    def optimize_index(self) -> Dict[str, Any]:
        """
        优化索引
        
        基于信息论原理优化知识表示
        """
        # 重新计算概率分布
        total_access = sum(k.access_count for k in self.knowledge.values())
        
        for kid, kd in self.knowledge.items():
            if total_access > 0:
                kd.probability = kd.access_count / total_access
            kd.self_information = InformationCoding.self_information(kd.probability)
        
        # 优化结果
        return {
            'total_knowledge': len(self.knowledge),
            'total_accesses': total_access,
            'entropy': self.entropy_calc.entropy(
                np.array([k.probability for k in self.knowledge.values()])
            ),
            'average_self_info': np.mean([
                k.self_information for k in self.knowledge.values()
            ])
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """get统计"""
        mi_metrics = self.mi_retrieval.get_information_metrics()
        
        return {
            'total_knowledge': len(self.knowledge),
            'total_retrievals': self.total_retrievals,
            'entropy': mi_metrics.entropy,
            'average_mutual_info': mi_metrics.mutual_information,
            'coding_efficiency': mi_metrics.coding_efficiency
        }

# ============ 便捷函数 ============

def create_info_retrieval_system() -> InformationTheoryRetrievalSystem:
    """创建信息论检索系统"""
    return InformationTheoryRetrievalSystem()

def quick_retrieve(query: str, 
                  knowledge_items: List[Tuple[str, str]],
                  relevance_fn: Optional[Callable] = None) -> List[Dict]:
    """快速检索"""
    system = create_info_retrieval_system()
    
    # 索引
    for kid, content in knowledge_items:
        system.index_knowledge(kid, content)
    
    # 计算相关度
    relevance_scores = {}
    if relevance_fn:
        for kid, content in knowledge_items:
            relevance_scores[kid] = relevance_fn(query, content)
    else:
        # 简单的关键词匹配
        for kid, content in knowledge_items:
            common = len(set(query) & set(content))
            relevance_scores[kid] = common / max(1, len(set(content)))
    
    # 检索
    return system.retrieve(query, relevance_scores)

# ============ 示例使用 ============

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
