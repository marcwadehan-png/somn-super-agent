# -*- coding: utf-8 -*-
"""
语义向量编码器 v1.0
_semantic_encoder.py

[架构定位] 神经记忆系统 v2.0 G-5 核心组件。

为藏书阁 CellRecord 提供语义向量生成能力：
- 轻量级 TF-IDF + Hashing 编码（无外部模型依赖）
- 支持可配置维度（64/128/256/768）
- L2 归一化输出
- 未来可替换为 embedding 模型 API（如 OpenAI/sentence-transformers）

使用方式:
  - 独立调用: SemanticEncoder().encode(text)
  - 入库自动编码: submit_cell() 内部自动触发
  - 批量编码: batch_encode(texts)

版本: v1.0.0
创建: 2026-04-28
依赖: Python 3.10+ (无第三方库依赖)
"""

from __future__ import annotations

import hashlib
import logging
import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
#  配置 & 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class EncoderConfig:
    """语义编码器配置"""
    dimension: int = 128              # 向量维度
    hash_positions: int = 3           # 每个词哈希到几个位置
    enable_tfidf_weighting: bool = True   # TF-IDF 加权
    normalize_l2: bool = True         # L2 归一化
    min_word_length_cn: int = 2       # 中文最小词长
    min_word_length_en: int = 3       # 英文最小词长
    # 停用词表
    stopwords_cn: Tuple[str, ...] = (
        "的", "是", "在", "了", "和", "与", "如何", "怎么",
        "什么", "这", "那", "个", "中", "上", "下", "也", "很",
        "就", "都", "能", "会", "要", "可以", "对", "但", "或",
        "及", "以", "等", "为", "从", "到", "被", "让", "把",
        "给", "比", "不", "没有", "而", "且", "其", "之", "于",
    )
    stopwords_en: Tuple[str, ...] = (
        "the", "a", "an", "is", "are", "was", "were", "be",
        "to", "of", "in", "for", "on", "with", "at", "by",
        "from", "and", "or", "not", "it", "this", "that",
        "as", "but", "if", "then", "so", "no", "we", "you",
    )


@dataclass
class EncodingResult:
    """编码结果"""
    vector: List[float]
    dimension: int
    token_count: int          # 分词数量
    unique_tokens: int        # 唯一词数量
    encoding_time_ms: float   # 编码耗时(ms)
    method: str = "tfidf_hashing"


# ═══════════════════════════════════════════════════════════════
#  核心类：SemanticEncoder
# ═══════════════════════════════════════════════════════════════


class SemanticEncoder:
    """
    语义向量编码器
    
    使用轻量级算法生成文本的固定维度向量表示：
    
    1. 分词（中文按字/英文按词）
    2. 词频统计
    3. Hashing 投影到语义空间（模拟词嵌入效果）
    4. TF-IDF 式加权
    5. L2 归一化
    
    设计原则：
    - 零外部依赖（纯 Python 标准库）
    - 确定性输出（相同输入 → 相同向量）
    - 高效（单条文本 < 10ms）
    """

    def __init__(self, config: Optional[EncoderConfig] = None):
        self.config = config or EncoderConfig()
        # 合并停用词集合
        self._stopwords: set = set(self.config.stopwords_cn) | set(self.config.stopwords_en)
        
        # 编码缓存（最近 N 条结果，避免重复计算）
        self._cache: Dict[str, EncodingResult] = {}
        self._cache_max_size = 1000
        
        logger.info(
            f"[SemanticEncoder] 初始化完成 "
            f"(dim={self.config.dimension}, hash_pos={self.config.hash_positions})"
        )

    # ──────────────────────────────────────────────────
    #  公共接口
    # ──────────────────────────────────────────────────

    def encode(self, text: str) -> List[float]:
        """
        对文本进行语义编码。
        
        Args:
            text: 输入文本
            
        Returns:
            长度为 config.dimension 的浮点向量（L2归一化）
        """
        result = self.encode_with_details(text)
        return result.vector

    def encode_with_details(self, text: EncodingResult | str) -> EncodingResult:
        """
        对文本进行语义编码（含详细信息）。
        
        Args:
            text: 输入文本
            
        Returns:
            EncodingResult（含统计信息）
        """
        import time as _time
        start = _time.time()
        
        if isinstance(text, EncodingResult):
            return text
            
        # 查缓存
        cache_key = hashlib.md5(text[:500].encode()).hexdigest()[:16]
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            return cached
        
        # 分词
        tokens = self._tokenize(text)
        token_count = len(tokens)
        
        # 统计词频
        word_freq: Dict[str, int] = {}
        for token in tokens:
            word_freq[token] = word_freq.get(token, 0) + 1
        
        unique_tokens = len(word_freq)
        
        # Hashing 投影到语义空间
        vector = self._project_to_vector(word_freq, token_count)
        
        # L2 归一化
        if self.config.normalize_l2 and vector:
            norm = math.sqrt(sum(v * v for v in vector))
            if norm > 0:
                vector = [v / norm for v in vector]
        
        elapsed = (_time.time() - start) * 1000
        
        result = EncodingResult(
            vector=vector,
            dimension=self.config.dimension,
            token_count=token_count,
            unique_tokens=unique_tokens,
            encoding_time_ms=round(elapsed, 3),
        )
        
        # 存缓存
        if len(self._cache) >= self._cache_max_size:
            # 简单淘汰：清空一半
            keys = list(self._cache.keys())
            for k in keys[:len(keys) // 2]:
                del self._cache[k]
        self._cache[cache_key] = result
        
        return result

    def batch_encode(self, texts: List[str]) -> List[EncodingResult]:
        """
        批量编码多条文本。
        
        Returns:
            EncodingResult 列表（与输入等长）
        """
        results = []
        for text in texts:
            result = self.encode_with_details(text)
            results.append(result)
        logger.info(f"[SemanticEncoder] 批量编码完成: {len(texts)}条")
        return results

    def similarity(
        self, vec_a: List[float], vec_b: List[float], method: str = "cosine"
    ) -> float:
        """
        计算两个向量的相似度。
        
        Args:
            vec_a: 向量A
            vec_b: 向量B
            method: "cosine" / "dot" / "euclidean"
            
        Returns:
            相似度分数 [0, 1]
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0
        
        if method == "cosine":
            dot = sum(a * b for a, b in zip(vec_a, vec_b))
            norm_a = math.sqrt(sum(a * a for a in vec_a))
            norm_b = math.sqrt(sum(b * b for b in vec_b))
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return dot / (norm_a * norm_b)
        
        elif method == "dot":
            return max(0.0, sum(a * b for a, b in zip(vec_a, vec_b)))
        
        elif method == "euclidean":
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))
            return max(0.0, 1.0 / (1.0 + dist))
        
        return 0.0

    # ──────────────────────────────────────────────────
    #  分词
    # ──────────────────────────────────────────────────

    def _tokenize(self, text: str) -> List[str]:
        """
        轻量级分词（无需 jieba）。
        
        规则：
        - 中文：连续汉字序列（≥min_word_length_cn 字）
        - 英文：连续字母/数字序列（≥min_word_length_en 字）
        - 混合：分别提取后合并
        """
        # 中文分词：连续2+汉字作为一个 token
        cn_tokens = re.findall(r'[\u4e00-\u9fff]{2,}', text.lower())
        en_tokens = re.findall(r'[a-zA-Z]{3,}', text.lower())
        num_tokens = re.findall(r'\d{2,}', text)
        
        all_tokens = cn_tokens + en_tokens + num_tokens
        
        # 过滤停用词
        filtered = [t for t in all_tokens if t not in self._stopwords]
        
        return filtered

    # ──────────────────────────────────────────────────
    #  向量投影（Hashing Trick 变体）
    # ──────────────────────────────────────────────────

    def _project_to_vector(
        self, word_freq: Dict[str, int], total_tokens: int
    ) -> List[float]:
        """
        将词频字典投影到固定维度的向量空间。
        
        算法（TF-IDF + Hashing）：
        1. 对每个词，计算 MD5 哈希值
        2. 将哈希值映射到 dimension 维空间的多个位置
        3. 按 TF-IDF 权重累加贡献
        4. 返回 dense 向量
        
        这是一种 locality-sensitive hashing 的简化形式，
        能够将不同语义的文本映射到不同的向量方向。
        """
        dim = self.config.dimension
        vector: List[float] = [0.0] * dim
        
        if not word_freq:
            return vector
        
        for word, freq in word_freq.items():
            # MD5 哈希
            h = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
            
            # 映射到多个位置（增加鲁棒性）
            positions = [
                h % dim,
                (h >> 8) % dim,
                (h >> 16) % dim,
            ][:self.config.hash_positions]
            
            # TF-IDF 式权重
            if self.config.enable_tfidf_weighting:
                # Term Frequency (对数平滑)
                tf = 1.0 + math.log(freq)
                
                # Inverse Document Frequency（简化版，基于全局频率估计）
                idf_smooth = 1.0 / (1.0 + math.log(total_tokens / max(freq, 1)))
                
                weight = tf * idf_smooth
            else:
                weight = float(freq)
            
            # 累加到各位置（递减权重模拟位置衰减）
            for i, pos in enumerate(positions):
                decay_factor = 1.0 / (i + 1)
                vector[pos] += weight * decay_factor
        
        return vector

    # ──────────────────────────────────────────────────
    #  辅助方法
    # ──────────────────────────────────────────────────

    def clear_cache(self) -> None:
        """清除编码缓存"""
        self._cache.clear()

    @property
    def cache_size(self) -> int:
        return len(self._cache)

    @property
    def dimension(self) -> int:
        return self.config.dimension

    def get_stats(self) -> Dict[str, Any]:
        """获取编码器统计信息"""
        return {
            "dimension": self.config.dimension,
            "hash_positions": self.config.hash_positions,
            "cache_size": len(self._cache),
            "cache_max_size": self._cache_max_size,
            "tfidf_enabled": self.config.enable_tfidf_weighting,
            "l2_normalize": self.config.normalize_l2,
        }


# ═══════════════════════════════════════════════════════════════
#  全局单例 & 便捷函数
# ═══════════════════════════════════════════════════════════════

_global_encoder: Optional[SemanticEncoder] = None


def get_semantic_encoder(config: Optional[EncoderConfig] = None) -> SemanticEncoder:
    """获取全局语义编码器实例"""
    global _global_encoder
    if _global_encoder is None:
        _global_encoder = SemanticEncoder(config)
    return _global_encoder


def encode_text(text: str, dimension: int = 128) -> List[float]:
    """
    便捷函数：对单条文本编码。
    
    兼容 LibraryKnowledgeBridge.encode_semantic() 的签名。
    """
    encoder = get_semantic_encoder()
    if encoder.dimension != dimension:
        # 如果维度不一致，创建临时编码器
        encoder = SemanticEncoder(EncoderConfig(dimension=dimension))
    return encoder.encode(text)


def batch_encode_texts(
    texts: List[str], dimension: int = 128
) -> List[List[float]]:
    """便捷函数：批量编码"""
    encoder = get_semantic_encoder()
    if encoder.dimension != dimension:
        encoder = SemanticEncoder(EncoderConfig(dimension=dimension))
    return [r.vector for r in encoder.batch_encode(texts)]


__all__ = [
    'SemanticEncoder',
    'EncoderConfig',
    'EncodingResult',
    'get_semantic_encoder',
    'encode_text',
    'batch_encode_texts',
]
