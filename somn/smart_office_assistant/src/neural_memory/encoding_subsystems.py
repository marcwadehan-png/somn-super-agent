"""
__all__ = [
    'align_modalities',
    'compute_similarity',
    'cross_attention',
    'encode_abstraction',
    'encode_causal',
    'encode_contrastive',
    'encode_dynamic',
    'encode_metacognition',
    'encode_semantic_field',
    'encode_with_attention',
    'get_abstraction_similarity',
    'query_semantic_field',
    'trace_causality',
]

记忆编码系统 - 子编码器模块
Encoding Subsystems: 8 specialized encoders.

从 memory_encoding_system_v3.py 拆分而来 (2026-04-06 S3b)
单一职责: 8 个子编码器类，每个负责一种编码方式
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from loguru import logger

from .encoding_types import EncodingContext, EncodingGranularity

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch未安装,高级编码功能将不可用")

class ContrastiveEncoder:
    """对比编码器 - 增强相似度和差异性recognize"""
    
    def __init__(self, model: "Optional[SentenceTransformer]" = None):  # type: ignore
        self.model = model
        self.temperature = 0.07  # 对比学习温度参数
        self.similarity_cache: Dict[str, np.ndarray] = {}
    
    def encode_contrastive(self, 
                         content: str,
                         positive_samples: List[str],
                         negative_samples: List[str]) -> np.ndarray:
        """
        对比编码
        
        Args:
            content: 主要内容
            positive_samples: 正样本(相似内容)
            negative_samples: 负样本(不相似内容)
        
        Returns:
            np.ndarray: 对比编码向量
        """
        if not self.model:
            # 简化版编码
            return self._simple_contrastive_encoding(content, positive_samples, negative_samples)
        
        # get所有样本的编码
        all_texts = [content] + positive_samples + negative_samples
        embeddings = self.model.encode(all_texts)
        
        # 主内容编码
        main_embedding = embeddings[0]
        positive_embeddings = embeddings[1:len(positive_samples)+1]
        negative_embeddings = embeddings[len(positive_samples)+1:]
        
        # 计算对比损失
        contrastive_vector = self._compute_contrastive_vector(
            main_embedding,
            positive_embeddings,
            negative_embeddings
        )
        
        return contrastive_vector
    
    def _compute_contrastive_vector(self,
                                    main: np.ndarray,
                                    positives: np.ndarray,
                                    negatives: np.ndarray) -> np.ndarray:
        """计算对比向量"""
        # 正样本相似度
        pos_similarities = [
            F.cosine_similarity(
                torch.tensor(main).unsqueeze(0),
                torch.tensor(pos).unsqueeze(0)
            ).item()
            for pos in positives
        ]
        
        # 负样本相似度
        neg_similarities = [
            F.cosine_similarity(
                torch.tensor(main).unsqueeze(0),
                torch.tensor(neg).unsqueeze(0)
            ).item()
            for neg in negatives
        ]
        
        # 构建对比向量
        pos_contribution = np.mean(positives, axis=0) * np.mean(pos_similarities)
        neg_contribution = np.mean(negatives, axis=0) * np.mean(neg_similarities)
        
        contrastive_vector = main + 0.5 * (pos_contribution - neg_contribution)
        
        return contrastive_vector
    
    def _simple_contrastive_encoding(self,
                                     content: str,
                                     positives: List[str],
                                     negatives: List[str]) -> np.ndarray:
        """简化版对比编码"""
        # 使用简单的词频向量
        all_words = set()
        for text in [content] + positives + negatives:
            all_words.update(text.split())
        
        # 主内容向量
        main_vector = np.array([1.0 if word in content.split() else 0.0 
                               for word in all_words])
        
        # 正样本影响
        pos_vector = np.array([
            np.mean([1.0 if word in pos.split() else 0.0 for pos in positives])
            for word in all_words
        ])
        
        # 负样本影响
        neg_vector = np.array([
            np.mean([1.0 if word in neg.split() else 0.0 for neg in negatives])
            for word in all_words
        ])
        
        # 对比编码
        contrastive = main_vector + 0.3 * pos_vector - 0.2 * neg_vector
        
        return contrastive
    
    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算相似度"""
        if TORCH_AVAILABLE:
            return float(F.cosine_similarity(
                torch.tensor(vec1).unsqueeze(0),
                torch.tensor(vec2).unsqueeze(0)
            ).item())
        else:
            # 余弦相似度
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

class AttentionEncoder:
    """注意力编码器 - 动态权重分配"""
    
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        
        if TORCH_AVAILABLE:
            self.attention_layer = nn.MultiheadAttention(
                embed_dim=embedding_dim,
                num_heads=8,
                dropout=0.1
            )
            self.feed_forward = nn.Sequential(
                nn.Linear(embedding_dim, 4 * embedding_dim),
                nn.ReLU(),
                nn.Linear(4 * embedding_dim, embedding_dim),
                nn.Dropout(0.1)
            )
            self.layer_norm = nn.LayerNorm(embedding_dim)
        else:
            logger.warning("PyTorch未安装,使用简化注意力机制")
    
    def encode_with_attention(self,
                              content_chunks: List[np.ndarray],
                              context: EncodingContext) -> Tuple[np.ndarray, List[float]]:
        """
        使用注意力编码
        
        Args:
            content_chunks: 内容分块的编码列表
            context: 编码上下文
        
        Returns:
            Tuple[np.ndarray, List[float]]: (编码向量, 注意力权重)
        """
        if not TORCH_AVAILABLE:
            return self._simple_attention_encoding(content_chunks, context)
        
        # 转换为tensor
        chunks_tensor = torch.tensor(content_chunks, dtype=torch.float32)
        
        # 自注意力
        attended_output, attention_weights = self.attention_layer(
            chunks_tensor, chunks_tensor, chunks_tensor
        )
        
        # 前馈网络
        output = self.feed_forward(attended_output)
        output = self.layer_norm(output + attended_output)
        
        # 平均池化
        final_encoding = output.mean(dim=0).detach().numpy()
        attention_scores = attention_weights.mean(dim=(0, 1)).detach().numpy().tolist()
        
        return final_encoding, attention_scores
    
    def _simple_attention_encoding(self,
                                   content_chunks: List[np.ndarray],
                                   context: EncodingContext) -> Tuple[np.ndarray, List[float]]:
        """简化注意力编码"""
        # 基于上下文焦点计算权重
        if context.attention_focus:
            weights = []
            for i, chunk in enumerate(content_chunks):
                # 简单的相似度计算
                focus_match = sum(1 for focus in context.attention_focus if focus in str(chunk))
                weight = 1.0 / (i + 1) + 0.3 * focus_match
                weights.append(weight)
        else:
            # 递减权重(位置重要性)
            weights = [1.0 / (i + 1) for i in range(len(content_chunks))]
        
        # 归一化
        weights = np.array(weights)
        weights = weights / weights.sum()
        
        # 加权平均
        final_encoding = np.zeros_like(content_chunks[0])
        for i, chunk in enumerate(content_chunks):
            final_encoding += weights[i] * chunk
        
        return final_encoding, weights.tolist()
    
    def cross_attention(self,
                        query: np.ndarray,
                        keys_values: List[np.ndarray]) -> np.ndarray:
        """
        交叉注意力
        
        Args:
            query: 查询向量
            keys_values: 键值对列表
        
        Returns:
            np.ndarray: 加权后的向量
        """
        if not TORCH_AVAILABLE:
            return self._simple_cross_attention(query, keys_values)
        
        query_tensor = torch.tensor(query, dtype=torch.float32).unsqueeze(0)
        kv_tensor = torch.tensor(keys_values, dtype=torch.float32)
        
        # 交叉注意力
        output, _ = self.attention_layer(query_tensor, kv_tensor, kv_tensor)
        
        return output.squeeze(0).detach().numpy()
    
    def _simple_cross_attention(self,
                                query: np.ndarray,
                                keys_values: List[np.ndarray]) -> np.ndarray:
        """简化交叉注意力"""
        # 计算相似度作为注意力权重
        similarities = []
        for kv in keys_values:
            sim = np.dot(query, kv) / (np.linalg.norm(query) * np.linalg.norm(kv))
            similarities.append(sim)
        
        # 归一化
        weights = np.array(similarities)
        weights = (weights - weights.min()) / (weights.max() - weights.min() + 1e-8)
        weights = weights / weights.sum()
        
        # 加权求和
        result = np.zeros_like(query)
        for i, kv in enumerate(keys_values):
            result += weights[i] * kv
        
        return result

class CausalEncoder:
    """因果编码器 - 捕捉因果关系"""
    
    def __init__(self):
        self.causal_patterns = {
            'because': 0.8,
            'since': 0.8,
            'due to': 0.7,
            'as a result': 0.9,
            'therefore': 0.85,
            'consequently': 0.85,
            'thus': 0.8,
            'hence': 0.8,
            'because of': 0.8,
            'owing to': 0.7,
            # 中文因果词
            '因为': 0.8,
            '由于': 0.8,
            '因此': 0.85,
            '所以': 0.85,
            '导致': 0.9,
            '造成': 0.85,
            '结果是': 0.9,
            '从而': 0.8,
            '由此可见': 0.85
        }
    
    def encode_causal(self, 
                     content: str,
                     context: EncodingContext) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        因果编码
        
        Args:
            content: 内容
            context: 上下文
        
        Returns:
            Tuple[np.ndarray, List[Dict]]: (因果编码向量, 因果链接列表)
        """
        # 提取因果关系
        causal_links = self._extract_causal_relationships(content, context)
        
        # 构建因果编码向量
        causal_vector = self._build_causal_vector(content, causal_links)
        
        return causal_vector, causal_links
    
    def _extract_causal_relationships(self,
                                      content: str,
                                      context: EncodingContext) -> List[Dict[str, Any]]:
        """提取因果关系"""
        import re
        causal_links = []
        
        # 基于模式匹配
        sentences = re.split(r'[..!!??;;]', content)
        
        for i, sentence in enumerate(sentences):
            for pattern, confidence in self.causal_patterns.items():
                if pattern in sentence.lower():
                    # 尝试分割原因和结果
                    parts = sentence.split(pattern, 1)
                    if len(parts) == 2:
                        cause = parts[0].strip()
                        effect = parts[1].strip()
                        
                        causal_links.append({
                            'cause': cause,
                            'effect': effect,
                            'connector': pattern,
                            'confidence': confidence,
                            'position': i
                        })
        
        # 合并上下文中的因果关系
        if context.causal_relationships:
            causal_links.extend(context.causal_relationships)
        
        return causal_links
    
    def _build_causal_vector(self,
                            content: str,
                            causal_links: List[Dict[str, Any]]) -> np.ndarray:
        """构建因果编码向量"""
        # 使用词频构建基础向量
        words = content.split()
        vocabulary = sorted(set(words))
        vector = np.zeros(len(vocabulary))
        
        # 基于因果链增强向量
        for link in causal_links:
            cause_words = set(link['cause'].split())
            effect_words = set(link['effect'].split())
            
            # 提升原因和结果的权重
            for word in cause_words & set(vocabulary):
                idx = vocabulary.index(word)
                vector[idx] += link['confidence']
            
            for word in effect_words & set(vocabulary):
                idx = vocabulary.index(word)
                vector[idx] += link['confidence']
        
        # 归一化
        if np.linalg.norm(vector) > 0:
            vector = vector / np.linalg.norm(vector)
        
        return vector
    
    def trace_causality(self, 
                       start_node: str,
                       causal_links: List[Dict[str, Any]]) -> List[str]:
        """
        追踪因果链
        
        Args:
            start_node: 起始节点
            causal_links: 因果链接列表
        
        Returns:
            List[str]: 因果链
        """
        chain = [start_node]
        visited = set(chain)
        
        _max_causal_iters = len(causal_links) + 1  # [v9.0] 安全上限
        _ci = 0
        while True:
            _ci += 1
            if _ci > _max_causal_iters:  # [v9.0] 防御性保护
                break
            found = False
            for link in causal_links:
                if link['cause'] in visited and link['effect'] not in visited:
                    chain.append(link['effect'])
                    visited.add(link['effect'])
                    found = True
                    break
            
            if not found:
                break
        
        return chain

class AbstractionEncoder:
    """抽象编码器 - 多级抽象层次"""
    
    def __init__(self, model: "Optional[SentenceTransformer]" = None):  # type: ignore
        self.model = model
        self.abstraction_levels = {
            0: "concrete",   # 具体
            1: "moderate",   # 中等
            2: "abstract"    # 抽象
        }
    
    def encode_abstraction(self,
                          content: str,
                          context: EncodingContext) -> Dict[int, np.ndarray]:
        """
        多级抽象编码
        
        Args:
            content: 内容
            context: 上下文
        
        Returns:
            Dict[int, np.ndarray]: 不同抽象层级的编码
        """
        encodings = {}
        
        for level in range(3):
            abstracted_content = self._abstract_content(content, level)
            
            if self.model:
                encodings[level] = self.model.encode(abstracted_content)
            else:
                encodings[level] = self._simple_encoding(abstracted_content)
        
        return encodings
    
    def _abstract_content(self, content: str, level: int) -> str:
        """
        抽象内容
        
        Args:
            content: 原始内容
            level: 抽象层级 (0=具体, 1=中等, 2=抽象)
        
        Returns:
            str: 抽象后的内容
        """
        if level == 0:
            # 具体级别:保留细节
            return content
        
        elif level == 1:
            # 中等级别:提取关键短语
            words = content.split()
            # 保留名词和动词
            keywords = [w for w in words if len(w) > 3]
            return ' '.join(keywords[:min(50, len(keywords))])
        
        elif level == 2:
            # 抽象级别:提取核心概念
            words = content.split()
            # 保留长词(通常是概念)
            concepts = [w for w in words if len(w) > 5]
            return ' '.join(concepts[:min(20, len(concepts))])
        
        return content
    
    def _simple_encoding(self, content: str) -> np.ndarray:
        """简化编码"""
        # 使用词频向量
        words = content.split()
        vocabulary = sorted(set(words))
        return np.array([words.count(w) for w in vocabulary])
    
    def get_abstraction_similarity(self,
                                   vec1: np.ndarray,
                                   vec2: np.ndarray,
                                   level1: int,
                                   level2: int) -> float:
        """
        计算不同抽象层级的相似度
        
        Args:
            vec1: 向量1
            vec2: 向量2
            level1: 向量1的抽象层级
            level2: 向量2的抽象层级
        
        Returns:
            float: 相似度
        """
        # 基础相似度
        if TORCH_AVAILABLE:
            base_sim = float(F.cosine_similarity(
                torch.tensor(vec1).unsqueeze(0),
                torch.tensor(vec2).unsqueeze(0)
            ).item())
        else:
            base_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        # 抽象层级差异惩罚
        level_diff = abs(level1 - level2)
        penalty = 0.1 * level_diff
        
        return max(0, base_sim - penalty)

class CrossModalEncoder:
    """跨模态对齐编码器"""
    
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        
        if TORCH_AVAILABLE:
            self.alignment_net = nn.Sequential(
                nn.Linear(embedding_dim * 2, embedding_dim),
                nn.ReLU(),
                nn.Linear(embedding_dim, 1),
                nn.Sigmoid()
            )
        else:
            logger.warning("PyTorch未安装,使用简化跨模态对齐")
    
    def align_modalities(self,
                         text_vec: np.ndarray,
                         image_vec: Optional[np.ndarray] = None,
                         audio_vec: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        跨模态对齐
        
        Args:
            text_vec: 文本编码
            image_vec: 图像编码
            audio_vec: 音频编码
        
        Returns:
            Dict[str, Any]: 对齐结果
        """
        alignments = {}
        
        if image_vec is not None:
            alignments['text_image'] = self._compute_alignment(text_vec, image_vec)
        
        if audio_vec is not None:
            alignments['text_audio'] = self._compute_alignment(text_vec, audio_vec)
        
        if image_vec is not None and audio_vec is not None:
            alignments['image_audio'] = self._compute_alignment(image_vec, audio_vec)
        
        return alignments
    
    def _compute_alignment(self, vec1: np.ndarray, vec2: np.ndarray) -> Dict[str, float]:
        """计算模态对齐度"""
        # 相似度
        if TORCH_AVAILABLE:
            similarity = float(F.cosine_similarity(
                torch.tensor(vec1).unsqueeze(0),
                torch.tensor(vec2).unsqueeze(0)
            ).item())
        else:
            similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        # 对齐分数
        if TORCH_AVAILABLE:
            concat = np.concatenate([vec1, vec2])
            alignment_score = float(self.alignment_net(
                torch.tensor(concat, dtype=torch.float32).unsqueeze(0)
            ).item())
        else:
            # 简化对齐分数
            alignment_score = similarity
        
        return {
            'similarity': similarity,
            'alignment_score': alignment_score
        }

class MetacognitiveEncoder:
    """元认知编码器 - 编码过程的元信息"""
    
    def __init__(self):
        self.encoding_history: List[Dict[str, Any]] = []
    
    def encode_metacognition(self,
                            content: str,
                            context: EncodingContext,
                            encoding_process: Dict[str, Any]) -> Dict[str, Any]:
        """
        元认知编码
        
        Args:
            content: 内容
            context: 上下文
            encoding_process: 编码过程信息
        
        Returns:
            Dict[str, Any]: 元认知信息
        """
        from datetime import datetime
        meta_info = {
            'encoding_timestamp': datetime.now().isoformat(),
            'content_length': len(content),
            'encoding_types_used': [t.value for t in context.metadata.get('encoding_types', [])],
            'processing_time': encoding_process.get('processing_time', 0),
            'encoding_success': encoding_process.get('success', True),
            'confidence_level': context.encoding_confidence,
            'difficulty_score': self._estimate_difficulty(content, context),
            'novelty_score': self._estimate_novelty(content),
            'relevance_score': context.metadata.get('relevance', 0.5),
            'attention_focus': context.attention_focus
        }
        
        # 记录历史
        self.encoding_history.append(meta_info)
        
        return meta_info
    
    def _estimate_difficulty(self, content: str, context: EncodingContext) -> float:
        """估计编码难度"""
        # 基于内容长度
        length_factor = min(1.0, len(content) / 1000)
        
        # 基于抽象层级
        abstraction_factor = context.abstraction_level / 2.0
        
        # 基于领域(简单实现)
        domain_difficulty = {
            'general': 0.3,
            'business': 0.5,
            'technical': 0.7,
            'academic': 0.8
        }
        domain_factor = domain_difficulty.get(context.domain, 0.5)
        
        return (length_factor + abstraction_factor + domain_factor) / 3.0
    
    def _estimate_novelty(self, content: str) -> float:
        """估计新颖性"""
        if not self.encoding_history:
            return 1.0
        
        # 与历史编码比较
        novel_count = 0
        for history in self.encoding_history[-10:]:  # 比较最近10次
            # 简单比较(实际应使用向量相似度)
            if len(set(content.split()) & set(history.get('content_words', []))) < 3:
                novel_count += 1
        
        return novel_count / min(10, len(self.encoding_history))

class SemanticFieldEncoder:
    """语义场编码器 - 上下文语义场建模"""
    
    def __init__(self, model: "Optional[SentenceTransformer]" = None):  # type: ignore
        self.model = model
        self.semantic_fields: Dict[str, List[str]] = {}
    
    def encode_semantic_field(self,
                              content: str,
                              context: EncodingContext) -> Dict[str, float]:
        """
        语义场编码
        
        Args:
            content: 内容
            context: 上下文
        
        Returns:
            Dict[str, float]: 语义场向量
        """
        # 提取关键词
        keywords = self._extract_keywords(content)
        
        # 更新语义场
        field_id = f"{context.scenario}_{context.domain}"
        if field_id not in self.semantic_fields:
            self.semantic_fields[field_id] = []
        
        self.semantic_fields[field_id].extend(keywords)
        
        # 计算语义场向量
        field_vector = self._compute_field_vector(keywords, field_id)
        
        return field_vector
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        # 简单实现:提取长词
        words = content.split()
        keywords = [w for w in words if len(w) > 3 and w.isalpha()]
        return list(set(keywords))
    
    def _compute_field_vector(self, 
                            keywords: List[str],
                            field_id: str) -> Dict[str, float]:
        """计算语义场向量"""
        field_words = self.semantic_fields[field_id]
        
        # 关键词在语义场中的权重
        field_vector = {}
        for keyword in keywords:
            # 出现频率
            frequency = field_words.count(keyword) / len(field_words)
            
            # 位置权重(最近出现的更重要)
            positions = [i for i, w in enumerate(field_words) if w == keyword]
            if positions:
                last_pos = positions[-1]
                pos_weight = 1.0 / (len(field_words) - last_pos + 1)
            else:
                pos_weight = 0
            
            # synthesize权重
            field_vector[keyword] = 0.7 * frequency + 0.3 * pos_weight
        
        return field_vector
    
    def query_semantic_field(self,
                            query: str,
                            field_id: str) -> List[Tuple[str, float]]:
        """
        查询语义场
        
        Args:
            query: 查询词
            field_id: 语义场ID
        
        Returns:
            List[Tuple[str, float]]: 相关词及其相关性分数
        """
        if field_id not in self.semantic_fields:
            return []
        
        field_words = self.semantic_fields[field_id]
        query_words = set(query.split())
        
        # 计算相关性
        relevance_scores = []
        for word in set(field_words):
            # 简单相关性:共同词的交集
            intersection = len(query_words & set([word]))
            if intersection > 0:
                relevance_scores.append((word, 1.0))
            elif any(qw in word or word in qw for qw in query_words):
                relevance_scores.append((word, 0.5))
        
        return sorted(relevance_scores, key=lambda x: x[1], reverse=True)

class DynamicEncoder:
    """动态编码器 - 根据反馈动态调整"""
    
    def __init__(self):
        self.feedback_history: List[Dict[str, Any]] = []
        self.adjustment_weights: Dict[str, float] = {}
    
    def encode_dynamic(self,
                      content: str,
                      context: EncodingContext,
                      base_encoding: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        动态编码
        
        Args:
            content: 内容
            context: 上下文
            base_encoding: 基础编码向量
        
        Returns:
            Tuple[np.ndarray, Dict]: (调整后的编码, 调整信息)
        """
        adjustment_info = {
            'adjustments_made': [],
            'feedback_used': context.feedback_received,
            'base_confidence': context.encoding_confidence
        }
        
        # 根据反馈调整
        if context.feedback_received:
            avg_feedback = np.mean(context.feedback_received)
            
            if avg_feedback > 0.7:
                # 正反馈:增强编码
                adjustment_factor = 1.0 + (avg_feedback - 0.5)
                adjusted_encoding = base_encoding * adjustment_factor
                adjustment_info['adjustments_made'].append({
                    'type': 'enhancement',
                    'factor': adjustment_factor
                })
            elif avg_feedback < 0.3:
                # 负反馈:减弱编码
                adjustment_factor = avg_feedback
                adjusted_encoding = base_encoding * adjustment_factor
                adjustment_info['adjustments_made'].append({
                    'type': 'suppression',
                    'factor': adjustment_factor
                })
            else:
                # 中性反馈:保持不变
                adjusted_encoding = base_encoding.copy()
        else:
            # 无反馈:根据历史调整
            adjusted_encoding = self._adjust_by_history(base_encoding, content)
            adjustment_info['adjustments_made'].append({
                'type': 'historical',
                'history_used': len(self.feedback_history)
            })
        
        # 记录调整
        self.feedback_history.append(adjustment_info)
        
        return adjusted_encoding, adjustment_info
    
    def _adjust_by_history(self, encoding: np.ndarray, content: str) -> np.ndarray:
        """根据历史调整"""
        if not self.feedback_history:
            return encoding
        
        # 分析最近的调整模式
        recent_adjustments = self.feedback_history[-10:]
        
        enhancement_count = sum(
            1 for adj in recent_adjustments
            if 'enhancement' in str(adj.get('adjustments_made', []))
        )
        suppression_count = sum(
            1 for adj in recent_adjustments
            if 'suppression' in str(adj.get('adjustments_made', []))
        )
        
        # 应用调整
        if enhancement_count > suppression_count:
            return encoding * 1.1  # 轻微增强
        elif suppression_count > enhancement_count:
            return encoding * 0.9  # 轻微减弱
        else:
            return encoding.copy()
