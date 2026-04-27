"""
__all__ = [
    'add_document',
    'search',
]

SomnCore TF-IDF 索引模块
纯 Python 实现的中英文混合 TF-IDF 索引，支持增量构建与余弦相似度检索。
"""

import re
import math
import logging
from collections import Counter
from typing import Dict, List, Tuple, Optional, Any

logger = logging.getLogger(__name__)

class PurePythonTfidfIndex:
    """纯 Python TF-IDF 索引(无外部依赖).支持增量构建与余弦相似度检索."""

    def __init__(self, min_df: int = 1, max_df_ratio: float = 0.95):
        self.min_df = min_df
        self.max_df_ratio = max_df_ratio
        self.doc_count = 0
        self.term_idf: Dict[str, float] = {}
        self.doc_term_counts: List[Tuple[str, Counter]] = []  # (doc_id, Counter)

    # --- 分词(纯 Python) ---
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """中英文混合分词:中文按字符+bigram,英文按单词."""
        tokens = []
        # 英文单词
        tokens.extend(re.findall(r"[a-zA-Z0-9_\-]{2,}", text.lower()))
        # 中文字符 + 二元组
        chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
        for ch in chinese_chars:
            tokens.append(ch)
        for i in range(len(chinese_chars) - 1):
            tokens.append(chinese_chars[i] + chinese_chars[i + 1])
        return tokens

    # --- 增量构建 ---
    def add_document(self, doc_id: str, text: str) -> None:
        """添加一个文档到索引."""
        tokens = self._tokenize(text)
        counts = Counter(tokens)
        self.doc_term_counts.append((doc_id, counts))
        self.doc_count += 1
        self._recompute_idf()

    def _recompute_idf(self) -> None:
        """重新计算所有 term 的 IDF 值."""
        N = self.doc_count
        if N == 0:
            return
        # 统计每个 term 出现在多少个文档中
        df = Counter()
        for _, counts in self.doc_term_counts:
            for term in counts:
                df[term] += 1
        max_df = int(self.max_df_ratio * N)
        self.term_idf = {}
        for term, doc_freq in df.items():
            if doc_freq >= self.min_df and doc_freq <= max_df:
                self.term_idf[term] = math.log(N / (doc_freq + 1)) + 1

    # --- 向量化 ---
    def _tfidf_vector(self, counts: Counter) -> Dict[str, float]:
        """将一个文档的 Counter 转为 TF-IDF 向量(仅含非零项)."""
        total = sum(counts.values())
        if total == 0:
            return {}
        result = {}
        for term, freq in counts.items():
            if term in self.term_idf:
                tf = freq / total
                result[term] = tf * self.term_idf[term]
        return result

    @staticmethod
    def _cosine(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """两向量余弦相似度."""
        if not vec1 or not vec2:
            return 0.0
        dot = sum(vec1.get(t, 0) * vec2.get(t, 0) for t in vec1 if t in vec2)
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    # --- 检索 ---
    def search(self, query_text: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """对查询文本返回相似文档,按余弦相似度降序."""
        query_vec = self._tfidf_vector(Counter(self._tokenize(query_text)))
        results = []
        for doc_id, counts in self.doc_term_counts:
            doc_vec = self._tfidf_vector(counts)
            score = self._cosine(query_vec, doc_vec)
            if score > 0:
                results.append((doc_id, round(score, 4)))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

# ─────────────────────────────────────────────
# 全局 TF-IDF 索引(单例,按需重建)
# ─────────────────────────────────────────────
_experience_index: Optional[PurePythonTfidfIndex] = None
_index_doc_ids: List[str] = []

def _ensure_experience_index(experiences: List[Dict[str, Any]]) -> PurePythonTfidfIndex:
    """构建或复用经验库 TF-IDF 索引."""
    global _experience_index, _index_doc_ids
    current_ids = [exp.get("task_id", str(i)) for i, exp in enumerate(experiences)]
    if _experience_index is None or _index_doc_ids != current_ids:
        _experience_index = PurePythonTfidfIndex(min_df=1)
        _index_doc_ids = current_ids
        for i, exp in enumerate(experiences):
            doc_id = exp.get("task_id", str(i))
            # 拼接多个字段构建检索文本
            search_text = " ".join(filter(None, [
                exp.get("task_description", ""),
                exp.get("task_type", ""),
                " ".join(exp.get("keywords", [])),
                " ".join(exp.get("lessons_learned", [])),
                " ".join(exp.get("reusable_actions", [])),
            ]))
            _experience_index.add_document(doc_id, search_text)
        logger.info(f"[TF-IDF] 索引已重建,共 {len(experiences)} 条经验")
    return _experience_index
