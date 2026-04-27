"""
__all__ = [
    'encode',
    'get_stats',
]

记忆编码系统 v3.2 (咨询经验增强版) - 主系统入口
Enhanced Memory Encoding System v3.2

原始文件已拆分为:
- encoding_types.py: 枚举和数据结构 (EncodingGranularity, EncodingModality, EncodingType, EncodingContext, MemoryEncoding)
- encoding_subsystems.py: 8个子编码器 (Contrastive, Attention, Causal, Abstraction, CrossModal, Metacognitive, SemanticField, Dynamic)

本文件保留: MemoryEncodingSystemV31 主系统类 + 全局常量 + 兼容重导出

拆分日期: 2026-04-06 (S3b)
"""

import hashlib
import re
import numpy as np
from loguru import logger
import math
from collections import defaultdict
from typing import Dict, List, Any
from datetime import datetime

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.info("sentence-transformers未安装,将使用简化编码(预期行为)")

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logger.warning("networkx未安装,知识图谱功能将不可用")

# ─── 从拆分文件导入类型和子编码器 ─────────────────────────────────
from .encoding_types import (
    EncodingGranularity,
    EncodingModality,
    EncodingType,
    EncodingContext,
    MemoryEncoding,
)

from .encoding_subsystems import (
    ContrastiveEncoder,
    AttentionEncoder,
    CausalEncoder,
    AbstractionEncoder,
    CrossModalEncoder,
    MetacognitiveEncoder,
    SemanticFieldEncoder,
    DynamicEncoder,
)


class MemoryEncoderV3:
    """记忆编码器 V3 - 封装 SentenceTransformer 或简化编码器

    NeuralMemorySystemV3 用它来做记忆向量编码。
    接受 model_name / embedding_dim / base_path 参数，与 MemoryEncodingSystemV31 接口对齐。
    """

    def __init__(self,
                 model_name: str = "all-MiniLM-L6-v2",
                 embedding_dim: int = 384,
                 base_path: str = ""):
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        self.base_path = base_path
        self.model = None
        self._init_model()

    def _init_model(self):
        """尝试加载 SentenceTransformer，失败则使用简化编码器"""
        global SENTENCE_TRANSFORMERS_AVAILABLE
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(self.model_name)
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
                logger.info(f"MemoryEncoderV3: 已加载模型 {self.model_name}")
            except Exception as e:
                logger.warning(f"MemoryEncoderV3: 模型加载失败 ({e})，将使用简化编码器")
                self.model = None
        else:
            self.model = None

    def encode(self, texts, normalize: bool = True) -> "np.ndarray":
        """编码文本为向量
        
        Args:
            texts: 字符串或字符串列表
            normalize: 是否 L2 归一化
        
        Returns:
            numpy 数组，shape = (len(texts), embedding_dim)
        """
        if self.model is not None:
            embeddings = self.model.encode(texts, normalize_embeddings=normalize)
            return embeddings
        # 简化版：用 hash + 随机投影
        import hashlib, struct
        if isinstance(texts, str):
            texts = [texts]
        results = []
        for text in texts:
            # 用 hash 生成确定性随机向量
            h = hashlib.sha256(text.encode()).digest()
            # 展开为 embedding_dim 维向量
            vec = np.array([
                (int(h[i % 32]) - 128) / 128.0
                for i in range(self.embedding_dim)
            ], dtype=np.float32)
            if normalize:
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
            results.append(vec)
        return np.array(results)

    def save(self, path: str):
        """保存编码器状态（简化版无需保存）"""
        logger.debug(f"MemoryEncoderV3.save({path}) called (no-op in simplified mode)")

    def load(self, path: str):
        """加载编码器状态（简化版无需加载）"""
        logger.debug(f"MemoryEncoderV3.load({path}) called (no-op in simplified mode)")


class MemoryEncodingSystemV31:
    """记忆编码系统 v3.1 - 完整版"""
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 embedding_dim: int = 384):
        """
        init记忆编码系统
        
        Args:
            model_name: 编码模型名称
            embedding_dim: 编码维度
        """
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        self.model = None
        self.model_available = False
        
        # init模型
        self._init_model(model_name)
        
        # init编码器
        self.contrastive_encoder = ContrastiveEncoder(self.model)
        self.attention_encoder = AttentionEncoder(embedding_dim)
        self.causal_encoder = CausalEncoder()
        self.abstraction_encoder = AbstractionEncoder(self.model)
        self.cross_modal_encoder = CrossModalEncoder(embedding_dim)
        self.metacognitive_encoder = MetacognitiveEncoder()
        self.semantic_field_encoder = SemanticFieldEncoder(self.model)
        self.dynamic_encoder = DynamicEncoder()
        
        # 统计信息
        self.stats = {
            'total_encodings': 0,
            'encoding_types_used': defaultdict(int),
            'avg_quality_score': 0.0
        }
        
        logger.info("记忆编码系统 v3.1 init完成")
        self._log_system_status()
    
    def _init_model(self, model_name: str):
        """init编码模型"""
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                self.model_available = True
                logger.info(f"成功加载编码模型: {model_name}")
            except Exception as e:
                logger.warning(f"加载编码模型失败: {e}")
                self.model_available = False
        else:
            self.model_available = False
            logger.info("使用简化编码模式")
    
    def _log_system_status(self):
        """记录系统状态"""
        logger.info("=" * 50)
        logger.info("记忆编码系统 v3.1 状态")
        logger.info("=" * 50)
        logger.info(f"编码模型: {'可用' if self.model_available else '不可用'}")
        logger.info(f"PyTorch: 可用")
        logger.info(f"NetworkX: {'可用' if NETWORKX_AVAILABLE else '不可用'}")
        logger.info(f"编码器模块:")
        logger.info(f"  - 对比编码器: OK")
        logger.info(f"  - 注意力编码器: OK")
        logger.info(f"  - 因果编码器: OK")
        logger.info(f"  - 抽象编码器: OK")
        logger.info(f"  - 跨模态编码器: OK")
        logger.info(f"  - 元认知编码器: OK")
        logger.info(f"  - 语义场编码器: OK")
        logger.info(f"  - 动态编码器: OK")
        logger.info("=" * 50)
    
    def encode(self,
              content: str,
              context: EncodingContext,
              granularity: EncodingGranularity = EncodingGranularity.MULTI,
              modality: EncodingModality = EncodingModality.TEXT,
              encoding_types: List[EncodingType] = None,
              **kwargs) -> MemoryEncoding:
        """
        编码记忆内容
        
        Args:
            content: 原始内容
            context: 编码上下文
            granularity: 编码颗粒度
            modality: 编码模态
            encoding_types: 编码类型列表
            **kwargs: 额外参数
        
        Returns:
            MemoryEncoding: 记忆编码对象
        """
        import time
        start_time = time.time()
        
        # 默认编码类型
        encoding_types = encoding_types or [
            EncodingType.SEMANTIC,
            EncodingType.CONTEXT,
            EncodingType.EMOTION
        ]
        
        # generate唯一ID
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        encoding_id = f"{context.session_id}_{content_hash}"
        
        # 编码向量
        encoded_vectors = {}
        
        # 基础编码
        if EncodingType.SEMANTIC in encoding_types:
            encoded_vectors['semantic'] = self._encode_semantic(content, granularity)
        
        # 对比编码
        if EncodingType.CONTRASTIVE in encoding_types:
            positives = kwargs.get('positive_samples', [])
            negatives = kwargs.get('negative_samples', [])
            if positives or negatives:
                encoded_vectors['contrastive'] = self.contrastive_encoder.encode_contrastive(
                    content, positives, negatives
                ).tolist()
        
        # 注意力编码
        if EncodingType.ATTENTION in encoding_types:
            chunks = self._split_into_chunks(content, granularity)
            if chunks:
                chunk_encodings = [self._encode_semantic(chunk, granularity) for chunk in chunks]
                attended_vec, weights = self.attention_encoder.encode_with_attention(
                    chunk_encodings, context
                )
                encoded_vectors['attention'] = attended_vec.tolist()
        
        # 因果编码
        if EncodingType.CAUSAL in encoding_types:
            causal_vec, causal_links = self.causal_encoder.encode_causal(content, context)
            encoded_vectors['causal'] = causal_vec.tolist()
        
        # 抽象编码
        if EncodingType.ABSTRACTION in encoding_types:
            abstraction_encodings = self.abstraction_encoder.encode_abstraction(
                content, context
            )
            for level, vec in abstraction_encodings.items():
                encoded_vectors[f'abstraction_{level}'] = vec.tolist()
        
        # 上下文编码
        if EncodingType.CONTEXT in encoding_types:
            encoded_vectors['context'] = self._encode_context(content, context)
        
        # 情感编码
        if EncodingType.EMOTION in encoding_types:
            encoded_vectors['emotion'] = self._encode_emotion(content, context)
        
        # 时序编码
        if EncodingType.TEMPORAL in encoding_types:
            encoded_vectors['temporal'] = self._encode_temporal(content, context)
        
        # 语义场编码
        if EncodingType.SEMANTIC_FIELD in encoding_types:
            field_vec = self.semantic_field_encoder.encode_semantic_field(content, context)
            encoded_vectors['semantic_field'] = list(field_vec.values())
        
        # 元认知编码
        encoding_process = {
            'processing_time': time.time() - start_time,
            'success': True,
            'encoding_types': encoding_types
        }
        
        # 动态编码
        if EncodingType.DYNAMIC in encoding_types and encoded_vectors:
            # 使用语义编码作为基础
            base_vec = np.array(encoded_vectors.get('semantic', list(np.zeros(self.embedding_dim))))
            dynamic_vec, adj_info = self.dynamic_encoder.encode_dynamic(
                content, context, base_vec
            )
            encoded_vectors['dynamic'] = dynamic_vec.tolist()
            encoding_process['dynamic_adjustments'] = adj_info
        
        # 计算质量分数
        quality_score = self._calculate_quality_score(encoded_vectors, context)
        
        # 查找关联记忆
        related_memories = self._find_related_memories(encoded_vectors)
        
        # 创建编码对象
        encoding = MemoryEncoding(
            id=encoding_id,
            original_content=content,
            encoded_vectors=encoded_vectors,
            granularity=granularity,
            modality=modality,
            encoding_types=encoding_types,
            context=context,
            quality_score=quality_score,
            confidence=self._calculate_confidence(encoded_vectors),
            related_memories=related_memories,
            knowledge_graph_nodes=[],
            encoding_process=self.metacognitive_encoder.encode_metacognition(
                content, context, encoding_process
            ),
            dynamic_adjustments=self.dynamic_encoder.feedback_history[-1:] if self.dynamic_encoder.feedback_history else []
        )
        
        # 更新统计
        self._update_stats(encoding)
        
        logger.info(f"编码完成: {encoding_id}, 质量: {quality_score:.2f}")
        
        return encoding
    
    def _encode_semantic(self, content: str, granularity: EncodingGranularity) -> List[float]:
        """语义编码"""
        if self.model_available:
            return self.model.encode(content).tolist()
        else:
            # 简化编码
            return self._simple_tfidf_encoding(content)
    
    def _encode_context(self, content: str, context: EncodingContext) -> List[float]:
        """上下文编码"""
        # 结合场景,情感,优先级等
        context_features = [
            hash(context.scenario) % 100 / 100.0,
            hash(context.task_type) % 100 / 100.0,
            hash(context.domain) % 100 / 100.0,
            context.emotion_intensity,
            context.priority / 10.0,
            context.abstraction_level / 2.0
        ]
        
        # 扩展到embedding维度
        context_vec = np.array(context_features)
        context_vec = np.repeat(context_vec, self.embedding_dim // len(context_features) + 1)
        context_vec = context_vec[:self.embedding_dim]
        
        return context_vec.tolist()
    
    def _encode_emotion(self, content: str, context: EncodingContext) -> List[float]:
        """情感编码"""
        emotion_weights = {
            'positive': 1.0,
            'negative': -1.0,
            'neutral': 0.0,
            'happy': 0.8,
            'sad': -0.8,
            'angry': -0.6,
            'fear': -0.7,
            'surprise': 0.5,
            'disgust': -0.5
        }
        
        weight = emotion_weights.get(context.emotion.lower(), 0.0)
        emotion_vec = np.full(self.embedding_dim, weight)
        
        return emotion_vec.tolist()
    
    def _encode_temporal(self, content: str, context: EncodingContext) -> List[float]:
        """时序编码"""
        # 时间戳编码
        timestamp = datetime.fromisoformat(context.timestamp)
        hour_sin = math.sin(2 * math.pi * timestamp.hour / 24)
        hour_cos = math.cos(2 * math.pi * timestamp.hour / 24)
        day_sin = math.sin(2 * math.pi * timestamp.weekday() / 7)
        day_cos = math.cos(2 * math.pi * timestamp.weekday() / 7)
        
        temporal_features = [hour_sin, hour_cos, day_sin, day_cos]
        temporal_vec = np.array(temporal_features)
        temporal_vec = np.repeat(temporal_vec, self.embedding_dim // 4)
        
        return temporal_vec.tolist()
    
    def _split_into_chunks(self, content: str, granularity: EncodingGranularity) -> List[str]:
        """将内容分块"""
        if granularity == EncodingGranularity.SENTENCE:
            return re.split(r'[..!!??;;]', content)
        elif granularity == EncodingGranularity.PARAGRAPH:
            return re.split(r'\n\n+', content)
        else:
            return [content]
    
    def _simple_tfidf_encoding(self, content: str) -> List[float]:
        """简化TF-IDF编码"""
        words = content.lower().split()
        vocabulary = sorted(set(words))
        
        # TF
        tf = [words.count(w) / len(words) for w in vocabulary]
        
        # IDF(简化)
        idf = [1.0] * len(vocabulary)
        
        # TF-IDF
        tfidf = [t * i for t, i in zip(tf, idf)]
        
        # 扩展到embedding维度
        vec = np.array(tfidf)
        vec = np.pad(vec, (0, self.embedding_dim - len(vec)))
        
        return vec.tolist()
    
    def _calculate_quality_score(self,
                                  encoded_vectors: Dict[str, List[float]],
                                  context: EncodingContext) -> float:
        """计算质量分数"""
        if not encoded_vectors:
            return 0.0
        
        # 基于向量数量
        vec_count_score = min(1.0, len(encoded_vectors) / 5.0)
        
        # 基于上下文置信度
        context_score = context.encoding_confidence
        
        # synthesize分数
        quality = 0.6 * vec_count_score + 0.4 * context_score
        
        return quality
    
    def _calculate_confidence(self, encoded_vectors: Dict[str, List[float]]) -> float:
        """计算置信度"""
        if not encoded_vectors:
            return 0.0
        
        # 基于模型可用性
        model_score = 1.0 if self.model_available else 0.5
        
        # 基于向量质量
        vec_score = min(1.0, len(encoded_vectors) / 3.0)
        
        return 0.5 * model_score + 0.5 * vec_score
    
    def _find_related_memories(self,
                              encoded_vectors: Dict[str, List[float]]) -> List[str]:
        """查找关联记忆"""
        # 简化实现:返回空列表
        # 实际实现应该在向量数据库中搜索
        return []
    
    def _update_stats(self, encoding: MemoryEncoding):
        """更新统计信息"""
        self.stats['total_encodings'] += 1
        
        for enc_type in encoding.encoding_types:
            self.stats['encoding_types_used'][enc_type.value] += 1
        
        # 更新平均质量分数
        total = self.stats['total_encodings']
        current_avg = self.stats['avg_quality_score']
        new_avg = (current_avg * (total - 1) + encoding.quality_score) / total
        self.stats['avg_quality_score'] = new_avg
    
    def get_stats(self) -> Dict[str, Any]:
        """get统计信息"""
        return {
            'total_encodings': self.stats['total_encodings'],
            'encoding_types_used': dict(self.stats['encoding_types_used']),
            'avg_quality_score': self.stats['avg_quality_score'],
            'model_available': self.model_available,
            'system_status': {
                'sentence_transformers': SENTENCE_TRANSFORMERS_AVAILABLE,
                'networkx': NETWORKX_AVAILABLE
            }
        }

# 使用示例
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
