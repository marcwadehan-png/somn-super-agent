# -*- coding: utf-8 -*-
"""
ClawSemanticSearch - Claw语义搜索模块
=====================================

A.1 Claw记忆搜索升级：从关键词匹配升级为向量语义检索

功能:
- 基于TF-IDF + 余弦相似度的语义向量搜索
- 与ClawCoordinator无缝集成
- 支持混合搜索（语义+关键词）
- 增量索引构建

版本: v1.0.0
创建: 2026-04-24
"""

from __future__ import annotations

import re
import math
import logging
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# TF-IDF 向量引擎
# ═══════════════════════════════════════════════════════════════

class TFIDFVectorizer:
    """
    TF-IDF向量生成器。
    
    支持中英文混合文本，使用jieba分词（如可用）或简单空格/正则分词。
    """

    def __init__(self):
        self._vocab: Dict[str, int] = {}
        self._idf: Dict[str, float] = {}
        self._doc_count: int = 0
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._initialized: bool = False
        self._lock = __import__("threading").Lock()

    def _tokenize(self, text: str) -> List[str]:
        """分词（支持中英文混合）"""
        if not text:
            return []
        
        # 尝试使用jieba
        try:
            import jieba
            tokens = list(jieba.cut(text))
        except ImportError:
            # 降级：简单分词
            # 中文：按标点和空格分割，再按字符n-gram
            tokens = []
            # 英文单词
            for word in re.findall(r'[a-zA-Z]+', text):
                tokens.append(word.lower())
            # 中文词组（2-4字）
            for word in re.findall(r'[\u4e00-\u9fff]{2,4}', text):
                tokens.append(word)
            # 标点分割
            for seg in re.split(r'[,，.。!！?？;；:：、]', text):
                seg = seg.strip()
                if seg:
                    # 3字以上的中文片段
                    for w in re.findall(r'[\u4e00-\u9fff]{3,}', seg):
                        tokens.append(w)
        
        # 过滤停用词
        stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '他',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        }
        return [t for t in tokens if t and len(t) >= 2 and t not in stopwords]

    def _compute_idf(self) -> None:
        """计算IDF值"""
        for term in self._doc_freq:
            self._idf[term] = math.log(
                (self._doc_count + 1) / (self._doc_freq[term] + 1)
            ) + 1

    def fit(self, documents: List[str]) -> 'TFIDFVectorizer':
        """
        构建词汇表和IDF。
        
        Args:
            documents: 文档列表
            
        Returns:
            self
        """
        with self._lock:
            self._doc_count = len(documents)
            self._doc_freq.clear()
            vocab_set: Set[str] = set()
            
            for doc in documents:
                tokens = set(self._tokenize(doc))
                vocab_set.update(tokens)
                for token in tokens:
                    self._doc_freq[token] += 1
            
            # 构建词汇表
            self._vocab = {term: idx for idx, term in enumerate(sorted(vocab_set))}
            self._compute_idf()
            self._initialized = True
            
        logger.info(f"[TFIDF] Built vocab with {len(self._vocab)} terms from {len(documents)} docs")
        return self

    def transform(self, text: str) -> Dict[str, float]:
        """
        将文本转换为TF-IDF向量。
        
        Returns:
            {term: tfidf_score}
        """
        if not self._initialized:
            return {}
        
        tokens = self._tokenize(text)
        if not tokens:
            return {}
        
        # 计算TF
        token_freq = defaultdict(int)
        for token in tokens:
            token_freq[token] += 1
        
        total = len(tokens)
        tfidf = {}
        for token, freq in token_freq.items():
            if token in self._vocab and token in self._idf:
                tfidf[token] = (freq / total) * self._idf[token]
        
        return tfidf

    def fit_transform(self, documents: List[str]) -> List[Dict[str, float]]:
        """fit + transform 快捷方法"""
        self.fit(documents)
        return [self.transform(doc) for doc in documents]


class CosineSimilarity:
    """余弦相似度计算器"""

    @staticmethod
    def compute(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        计算两个TF-IDF向量的余弦相似度。
        
        Args:
            vec1, vec2: {term: tfidf_score}
            
        Returns:
            0-1之间的相似度分数
        """
        if not vec1 or not vec2:
            return 0.0
        
        # 找交集
        common = set(vec1.keys()) & set(vec2.keys())
        if not common:
            return 0.0
        
        # 计算点积
        dot_product = sum(vec1[t] * vec2[t] for t in common)
        
        # 计算模长
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


# ═══════════════════════════════════════════════════════════════
# Claw语义索引
# ═══════════════════════════════════════════════════════════════

@dataclass
class SemanticIndexEntry:
    """语义索引条目"""
    claw_name: str
    content: str          # 原始内容（触发词 + 描述 + 领域）
    tfidf_vector: Dict[str, float] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)
    school: str = ""


class ClawSemanticIndex:
    """
    Claw语义搜索索引。
    
    使用TF-IDF + 余弦相似度实现语义搜索，
    支持增量构建和混合搜索。
    
    用法:
        index = ClawSemanticIndex(coordinator)
        index.build()  # 首次构建
        
        # 搜索
        results = index.search("如何治理国家", top_k=5)
    """

    def __init__(self, coordinator=None):
        self.coordinator = coordinator
        self._vectorizer = TFIDFVectorizer()
        self._entries: Dict[str, SemanticIndexEntry] = {}
        self._built: bool = False
        self._lock = __import__("threading").Lock()

    def build(self, claws: Dict[str, Any] = None) -> int:
        """
        构建语义索引。
        
        Args:
            claws: Claw字典（如果为None，从coordinator获取）
            
        Returns:
            索引条目数量
        """
        with self._lock:
            if claws is None and self.coordinator is not None:
                claws = self.coordinator.claws
            
            if claws is None:
                logger.warning("[SemanticIndex] No claws provided")
                return 0
            
            # 收集文档内容
            docs = []
            names = []
            
            for name, claw in claws.items():
                # 构建内容字符串
                parts = []
                
                # 触发词
                if hasattr(claw, 'metadata'):
                    meta = claw.metadata
                    if hasattr(meta, 'triggers') and meta.triggers:
                        parts.extend(meta.triggers)
                    if hasattr(meta, 'description') and meta.description:
                        parts.append(meta.description)
                    if hasattr(meta, 'school') and meta.school:
                        parts.append(meta.school)
                    if hasattr(meta, 'wisdom_school') and meta.wisdom_school:
                        parts.append(meta.wisdom_school)
                    school = getattr(meta, 'school', '') or getattr(meta, 'wisdom_school', '')
                else:
                    school = ""
                
                content = " ".join(parts)
                if not content.strip():
                    content = name  # 回退到名称
                
                docs.append(content)
                names.append(name)
                self._entries[name] = SemanticIndexEntry(
                    claw_name=name,
                    content=content,
                    keywords=self._vectorizer._tokenize(content),
                    school=school,
                )
            
            # TF-IDF训练
            if docs:
                vectors = self._vectorizer.fit_transform(docs)
                for name, vec in zip(names, vectors):
                    self._entries[name].tfidf_vector = vec
            
            self._built = True
            logger.info(f"[SemanticIndex] Built with {len(self._entries)} entries")
            
        return len(self._entries)

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.1,
        school_filter: str = None,
        hybrid: bool = True,
    ) -> List[Tuple[str, float, str]]:
        """
        语义搜索Claw。
        
        Args:
            query: 查询文本
            top_k: 返回数量
            min_score: 最低分数阈值
            school_filter: 学派过滤（可选）
            hybrid: 是否启用混合搜索（语义 + 关键词）
            
        Returns:
            [(claw_name, score, school)]
        """
        if not self._built:
            logger.warning("[SemanticIndex] Index not built yet")
            return []
        
        # 查询向量
        query_vec = self._vectorizer.transform(query)
        if not query_vec:
            # 纯关键词搜索
            return self._keyword_search(query, top_k, school_filter)
        
        # 语义搜索
        results = []
        cosine = CosineSimilarity()
        
        for name, entry in self._entries.items():
            if school_filter and entry.school != school_filter:
                continue
            
            score = cosine.compute(query_vec, entry.tfidf_vector)
            
            # 混合增强：关键词匹配加分
            if hybrid:
                keywords = entry.keywords
                query_tokens = set(self._vectorizer._tokenize(query))
                keyword_overlap = len(query_tokens & set(keywords))
                if keyword_overlap > 0:
                    score += 0.1 * min(keyword_overlap, 3)  # 最多+0.3
            
            if score >= min_score:
                results.append((name, score, entry.school))
        
        # 排序
        results.sort(key=lambda x: -x[1])
        return results[:top_k]

    def _keyword_search(
        self,
        query: str,
        top_k: int,
        school_filter: str = None,
    ) -> List[Tuple[str, float, str]]:
        """纯关键词搜索（fallback）"""
        tokens = set(self._vectorizer._tokenize(query))
        results = []
        
        for name, entry in self._entries.items():
            if school_filter and entry.school != school_filter:
                continue
            
            overlap = len(tokens & set(entry.keywords))
            if overlap > 0:
                score = overlap / max(len(tokens), 1)
                results.append((name, score, entry.school))
        
        results.sort(key=lambda x: -x[1])
        return results[:top_k]

    def update_entry(self, claw_name: str, content: str) -> bool:
        """
        更新单个条目（增量更新）。
        
        Returns:
            是否成功
        """
        with self._lock:
            if claw_name not in self._entries:
                return False
            
            vec = self._vectorizer.transform(content)
            entry = self._entries[claw_name]
            entry.content = content
            entry.tfidf_vector = vec
            entry.keywords = self._vectorizer._tokenize(content)
            
        logger.debug(f"[SemanticIndex] Updated entry: {claw_name}")
        return True

    def add_entry(self, claw_name: str, content: str, school: str = "") -> bool:
        """添加新条目"""
        with self._lock:
            if claw_name in self._entries:
                return self.update_entry(claw_name, content)
            
            vec = self._vectorizer.transform(content)
            self._entries[claw_name] = SemanticIndexEntry(
                claw_name=claw_name,
                content=content,
                tfidf_vector=vec,
                keywords=self._vectorizer._tokenize(content),
                school=school,
            )
            
        logger.debug(f"[SemanticIndex] Added entry: {claw_name}")
        return True

    def get_stats(self) -> Dict:
        """获取索引统计"""
        return {
            "total_entries": len(self._entries),
            "built": self._built,
            "vocab_size": len(self._vectorizer._vocab),
        }


# ═══════════════════════════════════════════════════════════════
# 增强型GatewayRouter
# ═══════════════════════════════════════════════════════════════

class SemanticRouter:
    """
    语义增强路由器。
    
    在原有GatewayRouter基础上增加语义搜索能力。
    """

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._semantic_index: Optional[ClawSemanticIndex] = None
        self._index_ready: bool = False

    def build_index(self) -> int:
        """构建语义索引"""
        if self._semantic_index is None:
            self._semantic_index = ClawSemanticIndex(self.coordinator)
        
        count = self._semantic_index.build(self.coordinator.claws)
        self._index_ready = count > 0
        return count

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        school: str = None,
    ) -> List[Tuple[str, float]]:
        """
        语义搜索Claw。
        
        Returns:
            [(claw_name, score)]
        """
        if not self._index_ready:
            self.build_index()
        
        results = self._semantic_index.search(
            query=query,
            top_k=top_k,
            school_filter=school,
            hybrid=True,
        )
        
        return [(name, score) for name, score, _ in results]

    def route_with_semantic(
        self,
        query: str,
        min_semantic_score: float = 0.3,
    ) -> Tuple[Optional[str], float, List[Tuple[str, float]]]:
        """
        语义增强路由。
        
        Args:
            query: 查询文本
            min_semantic_score: 语义分数阈值
            
        Returns:
            (primary_claw, semantic_score, [(claw, score)...])
        """
        if not self._index_ready:
            self.build_index()
        
        # 语义搜索
        candidates = self.semantic_search(query, top_k=5)
        
        if candidates and candidates[0][1] >= min_semantic_score:
            primary, score = candidates[0]
            return primary, score, candidates
        
        # 分数不足，返回None触发降级
        return None, 0.0, candidates
