# -*- coding: utf-8 -*-
"""
Somn RAG 引擎 v1.0
Retrieval-Augmented Generation Engine

核心功能:
1. 文档加载与分块(支持 txt/md/pdf/docx)
2. TF-IDF 向量化(零外部依赖,无需 sentence-transformers)
3. 语义检索(余弦相似度)
4. 上下文增强generate(将检索结果注入 LLM prompt)

设计原则:
- 零外部 NLP 依赖(不强制 sentence-transformers/chromadb/faiss)
- 用 TF-IDF + 余弦相似度做第一版,后续可升级为 embedding 模型
- 支持增量索引:新增文档无需全量重建
- 本地存储,不上传云端

版本: v1.0
日期: 2026-04-04
"""

import os
import re
import json
import math
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import Counter, defaultdict
from loguru import logger
import threading

# ═══════════════════════════════════════════════════════════════
#  文本处理工具
# ═══════════════════════════════════════════════════════════════

class ChineseTokenizer:
    """
    中文分词器(轻量级,基于字符 n-gram + 常见词切割)
    
    不依赖 jieba,用正则 + 规则实现基本中文分词.
    质量不如 jieba/ pkuseg,但零外部依赖.
    """
    
    # 常见中文停用词
    STOP_WORDS = set(
        '的了是在我有和就不人都一上也很到说要去你会着没有看好自己这他她它们那'
        '吗吧呢啊哦呀嗯哈嘛啦呗哎哟么什么怎么为什么如何怎样这个那个一个'
        '可以已经还能但是因为所以如果虽然然而不过而且或者以及对于关于通过'
        '进行使用实现包括目前需要根据由于因此同时之后之前之间'
        'the a an is are was were be been have has had do does did will would '
        'shall should can could may might must to of in for on with at by from '
        'as into through during before after above below between out off over '
        'under again further then once here there when where why how all both '
        'each few more most other some such no nor not only own same so than '
        'too very s t can will just don should now d ll m re ve y ain aren couldn '
        'didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn '
        'weren won wouldn'.split()
    )
    
    # 中文常用二字词(高频)
    COMMON_BIGRAMS = {
        '增长', 'strategy', '分析', '用户', '市场', '品牌', '产品', '营销',
        '管理', '数据', '技术', '服务', '模式', '价值', '创新', '竞争',
        '渠道', '内容', '客户', '消费', '体验', '设计', '运营', '优化',
        '转化', '留存', '获客', '流量', '收入', '成本', '利润', '效率',
        '平台', '系统', '功能', '需求', '目标', '方案', '执行', '结果',
        '问题', '方法', '过程', '因素', '环境', '资源', '能力', '水平',
        '规模', '趋势', '机会', '风险', '投资', '发展', '行业', '企业',
        '智慧', '哲学', '文化', '思想', '道德', '伦理', '人生', '意义',
        '自由', '命运', '真理', '知识', '科学', '自然', '社会', '历史',
        '智慧', '国学', '儒家', '道家', '佛家', 'xinxue', '兵法', '素书',
        '茅台', '腾讯', '阿里', '百度', '华为', '小米', '苹果', '谷歌',
        '电商', '直播', '短视频', '新能源', '芯片', '人工智能', '大模型',
        '智能体', '神经网络', '深度学习', '机器学习', '强化学习',
    }
    
    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        """
        分词:混合strategy
        1. 先用正则切分出中文字符序列,英文单词,数字
        2. 对中文序列:优先匹配常见词,剩余做字符级切分
        3. 过滤停用词和单字(除非是关键单字)
        """
        if not text:
            return []
        
        tokens = []
        
        # 1. 正则切分:中文连续序列 / 英文单词 / 数字
        segments = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+[a-zA-Z0-9]*|\d+', text.lower())
        
        for segment in segments:
            if re.match(r'^[a-zA-Z]', segment):
                # 英文单词
                if segment not in cls.STOP_WORDS and len(segment) > 1:
                    tokens.append(segment)
            elif re.match(r'^\d+$', segment):
                # 数字,转成通用 token
                tokens.append(f"NUM_{len(segment)}")
            else:
                # 中文序列:贪心匹配常见词
                remaining = segment
                i = 0
                while i < len(remaining):
                    matched = False
                    # 尝试匹配 4字词 -> 3字词 -> 2字词
                    for word_len in [4, 3, 2]:
                        if i + word_len <= len(remaining):
                            candidate = remaining[i:i + word_len]
                            if candidate in cls.COMMON_BIGRAMS:
                                tokens.append(candidate)
                                i += word_len
                                matched = True
                                break
                    if not matched:
                        # 单字:保留非停用词
                        char = remaining[i]
                        if char not in cls.STOP_WORDS:
                            tokens.append(char)
                        i += 1
        
        return tokens
    
    @classmethod
    def extract_keywords(cls, text: str, top_k: int = 10) -> List[str]:
        """提取关键词(基于词频)"""
        tokens = cls.tokenize(text)
        freq = Counter(tokens)
        # 过滤停用词和单字
        filtered = Counter({w: c for w, c in freq.items() if w not in cls.STOP_WORDS and len(w) > 1})
        return [w for w, _ in filtered.most_common(top_k)]

# ═══════════════════════════════════════════════════════════════
#  文档加载器
# ═══════════════════════════════════════════════════════════════

@dataclass
class Document:
    """文档"""
    doc_id: str
    title: str
    content: str
    source: str                     # 文件路径或来源
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunks: List['Chunk'] = field(default_factory=list)

@dataclass
class Chunk:
    """文档块"""
    chunk_id: str
    doc_id: str
    content: str
    index: int                      # 在原文中的位置索引
    metadata: Dict[str, Any] = field(default_factory=dict)
    tokens: List[str] = field(default_factory=list)
    vector: List[float] = field(default_factory=list)

class DocumentLoader:
    """文档加载器"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_file(self, file_path: str) -> Optional[Document]:
        """从文件加载文档"""
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"文件不存在: {file_path}")
            return None
        
        suffix = path.suffix.lower()
        content = ""
        
        if suffix in ('.txt', '.md', '.csv'):
            try:
                content = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = path.read_text(encoding='gbk')
        elif suffix in ('.yaml', '.yml', '.json'):
            try:
                content = path.read_text(encoding='utf-8')
            except Exception as e:
                logger.warning(f"加载配置文件失败: {e}")
                return None
        elif suffix == '.py':
            try:
                content = path.read_text(encoding='utf-8')
            except Exception:
                return None
        else:
            logger.warning(f"暂不支持的格式: {suffix}")
            return None
        
        if not content.strip():
            return None
        
        doc_id = hashlib.md5(file_path.encode()).hexdigest()[:12]
        doc = Document(
            doc_id=doc_id,
            title=path.stem,
            content=content,
            source=str(path),
            metadata={"file_type": suffix, "file_size": path.stat().st_size},
        )
        
        # 分块
        doc.chunks = self._chunk_text(content, doc_id)
        return doc
    
    def load_text(self, text: str, title: str = "inline", source: str = "inline") -> Document:
        """直接加载文本"""
        doc_id = hashlib.md5(text.encode()).hexdigest()[:12]
        doc = Document(
            doc_id=doc_id,
            title=title,
            content=text,
            source=source,
        )
        doc.chunks = self._chunk_text(text, doc_id)
        return doc
    
    def _chunk_text(self, text: str, doc_id: str) -> List[Chunk]:
        """文本分块"""
        if not text or not text.strip():
            return []
        
        chunks = []
        # 按段落分割
        paragraphs = re.split(r'\n{2,}', text.strip())
        
        current_content = ""
        current_paras = []
        char_count = 0
        chunk_index = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if char_count + len(para) > self.chunk_size and current_content:
                # 保存当前块
                chunk = self._create_chunk(current_content, doc_id, chunk_index)
                chunks.append(chunk)
                chunk_index += 1
                
                # 保留 overlap(最后几段)
                overlap_text = self._get_overlap_text(current_paras, self.chunk_overlap)
                current_content = overlap_text + "\n\n" + para
                current_paras = [p for p in current_paras if p in overlap_text] + [para]
                char_count = len(current_content)
            else:
                current_content = current_content + "\n\n" + para if current_content else para
                current_paras.append(para)
                char_count = len(current_content)
        
        # 最后一部分
        if current_content.strip():
            chunk = self._create_chunk(current_content, doc_id, chunk_index)
            chunks.append(chunk)
        
        return chunks
    
    def _create_chunk(self, content: str, doc_id: str, index: int) -> Chunk:
        """创建文档块"""
        chunk_id = f"{doc_id}_{index:04d}"
        tokens = ChineseTokenizer.tokenize(content)
        return Chunk(
            chunk_id=chunk_id,
            doc_id=doc_id,
            content=content,
            index=index,
            tokens=tokens,
        )
    
    def _get_overlap_text(self, paragraphs: List[str], max_chars: int) -> str:
        """get overlap 文本"""
        text = ""
        for para in reversed(paragraphs):
            if len(text) + len(para) > max_chars:
                break
            text = para + "\n\n" + text if text else para
        return text

# ═══════════════════════════════════════════════════════════════
#  TF-IDF 向量化器
# ═══════════════════════════════════════════════════════════════

class TFIDFVectorizer:
    """
    TF-IDF 向量化器(纯 Python 实现)
    
    支持增量索引:新文档加入时,只需更新 IDF 表
    """
    
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}       # 词 -> 索引
        self.idf: Dict[str, float] = {}             # 词 -> IDF 值
        self.doc_count: int = 0                     # 已索引文档数
        self._lock = threading.Lock()
    
    def fit(self, documents: List[List[str]]) -> None:
        """构建词汇表和 IDF"""
        with self._lock:
            self.doc_count = len(documents)
            df = Counter()  # document frequency
            
            for doc_tokens in documents:
                unique_tokens = set(doc_tokens)
                for token in unique_tokens:
                    df[token] += 1
            
            # 构建 IDF
            for token, freq in df.items():
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)
                self.idf[token] = math.log((self.doc_count + 1) / (freq + 1)) + 1
    
    def partial_fit(self, new_documents: List[List[str]]) -> None:
        """增量更新（v16.1 P1 fix: 移除嵌套锁，避免死锁）"""
        self.fit(documents=new_documents)
    
    def transform(self, tokens: List[str]) -> List[float]:
        """将 token 列表转为 TF-IDF 向量"""
        if not self.vocabulary:
            return []
        
        # 计算 TF
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        
        # 构建 TF-IDF 向量
        vector_size = len(self.vocabulary)
        vector = [0.0] * vector_size
        
        for token, count in tf.items():
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                tf_val = count / total
                idf_val = self.idf.get(token, 1.0)
                vector[idx] = tf_val * idf_val
        
        return vector
    
    def transform_query(self, query: str) -> List[float]:
        """将查询文本转为 TF-IDF 向量"""
        tokens = ChineseTokenizer.tokenize(query)
        return self.transform(tokens)
    
    @staticmethod
    def cosine_similarity(a: List[float], b: List[float]) -> float:
        """余弦相似度"""
        if not a or not b or len(a) != len(b):
            return 0.0
        
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)

# ═══════════════════════════════════════════════════════════════
#  RAG 引擎主体
# ═══════════════════════════════════════════════════════════════

@dataclass
class RetrievalResult:
    """检索结果"""
    chunk: Chunk
    score: float
    doc_title: str = ""
    doc_source: str = ""

class RAGEngine:
    """
    RAG 检索增强generate引擎
    
    工作流程:
    1. 索引文档(自动分块 + TF-IDF 向量化)
    2. 查询时:将用户问题向量化 → 检索最相似的文档块
    3. 将检索结果作为上下文注入 LLM prompt
    """
    
    def __init__(self, index_dir: str = "data/rag_index"):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        self.documents: Dict[str, Document] = {}       # doc_id -> Document
        self.chunks: Dict[str, Chunk] = {}             # chunk_id -> Chunk
        self.chunk_list: List[Chunk] = []              # 有序块列表
        
        self.vectorizer = TFIDFVectorizer()
        self.loader = DocumentLoader(chunk_size=500, chunk_overlap=50)
        
        self._lock = threading.Lock()
        self._vectors_dirty = False  # v16.1 P1: 向量脏标记，延迟重建
        
        # 尝试加载已有索引
        self._load_index()
        
        logger.info(f"RAG 引擎init完成 (文档数={len(self.documents)}, 块数={len(self.chunks)})")
    
    def index_file(self, file_path: str) -> bool:
        """索引单个文件"""
        doc = self.loader.load_file(file_path)
        if not doc:
            return False
        
        return self._index_document(doc)
    
    def index_directory(self, dir_path: str, patterns: List[str] = None) -> int:
        """索引目录（v16.1 P1 增量优化：跳过已索引且未变化的文件，批量重建向量）"""
        if patterns is None:
            patterns = ['*.md', '*.txt', '*.yaml', '*.py']
        
        dir_path = Path(dir_path)
        if not dir_path.exists():
            return 0
        
        count = 0
        for pattern in patterns:
            for file_path in dir_path.rglob(pattern):
                # 跳过隐藏目录和 node_modules 等
                if any(part.startswith('.') or part in ('node_modules', '__pycache__', 'venv', '.venv')
                       for part in file_path.parts):
                    continue
                # v16.1 P1: 增量检测 — 已存在且文件大小未变则跳过
                doc_id = hashlib.md5(str(file_path).encode()).hexdigest()[:12]
                if doc_id in self.documents and file_path.exists():
                    cached_meta = self.documents[doc_id].metadata
                    if cached_meta.get("file_size") == file_path.stat().st_size:
                        continue
                if self.index_file(str(file_path)):
                    count += 1
        
        if count > 0 or self._vectors_dirty:
            self._rebuild_vectors()
            self._vectors_dirty = False
            self._save_index()
        
        return count  # v16.1 P1 fix: 返回实际索引文件数
    
    def index_text(self, text: str, title: str = "inline", source: str = "inline") -> bool:
        """索引文本"""
        doc = self.loader.load_text(text, title, source)
        return self._index_document(doc)
    
    def _index_document(self, doc: Document) -> bool:
        """索引文档（v16.1 P1: 标记脏，不立即全量重建向量）"""
        with self._lock:
            if doc.doc_id in self.documents:
                # 文档已存在,先移除旧块
                old_doc = self.documents[doc.doc_id]
                for chunk in old_doc.chunks:
                    self.chunks.pop(chunk.chunk_id, None)
                self.chunk_list = [c for c in self.chunk_list if c.doc_id != doc.doc_id]
            
            self.documents[doc.doc_id] = doc
            for chunk in doc.chunks:
                chunk.tokens = ChineseTokenizer.tokenize(chunk.content)
                self.chunks[chunk.chunk_id] = chunk
                self.chunk_list.append(chunk)
        
        # v16.1 P1: 标记脏，批量时统一重建
        self._vectors_dirty = True
        self._save_index()
        
        return True
    
    def _rebuild_vectors(self) -> None:
        """重建 TF-IDF 向量"""
        if not self.chunk_list:
            return
        
        all_token_lists = [chunk.tokens for chunk in self.chunk_list]
        self.vectorizer.fit(all_token_lists)
        
        for chunk in self.chunk_list:
            chunk.vector = self.vectorizer.transform(chunk.tokens)
        
        logger.info(f"向量重建完成 (词汇量={len(self.vectorizer.vocabulary)})")
    
    def retrieve(self, query: str, top_k: int = 5, min_score: float = 0.1) -> List[RetrievalResult]:
        """
        检索最相关的文档块
        
        Args:
            query: 查询文本
            top_k: 返回前 k 个结果
            min_score: 最低相似度阈值
            
        Returns:
            检索结果列表
        """
        # v16.1 P1: 查询前检查脏标记，确保向量最新
        if self._vectors_dirty and self.chunk_list:
            self._rebuild_vectors()
            self._vectors_dirty = False
        
        if not self.chunk_list or not self.vectorizer.vocabulary:
            return []
        
        query_vector = self.vectorizer.transform_query(query)
        if not query_vector:
            return []
        
        scored = []
        for chunk in self.chunk_list:
            if not chunk.vector:
                continue
            sim = TFIDFVectorizer.cosine_similarity(query_vector, chunk.vector)
            if sim >= min_score:
                scored.append((chunk, sim))
        
        # 按分数降序排序
        scored.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for chunk, score in scored[:top_k]:
            doc = self.documents.get(chunk.doc_id)
            results.append(RetrievalResult(
                chunk=chunk,
                score=score,
                doc_title=doc.title if doc else "",
                doc_source=doc.source if doc else "",
            ))
        
        return results
    
    def build_context(self, query: str, top_k: int = 3) -> str:
        """
        构建增强上下文
        
        将检索结果格式化为可注入 LLM prompt 的上下文字符串.
        """
        results = self.retrieve(query, top_k=top_k)
        
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[参考资料{i}] (来源: {result.doc_title}, 相关度: {result.score:.2f})\n"
                f"{result.chunk.content}"
            )
        
        return "\n\n---\n\n".join(context_parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """get RAG 统计信息"""
        return {
            "document_count": len(self.documents),
            "chunk_count": len(self.chunks),
            "vocabulary_size": len(self.vectorizer.vocabulary),
            "index_dir": str(self.index_dir),
            "documents": [
                {"doc_id": doc.doc_id, "title": doc.title, "chunks": len(doc.chunks), "source": doc.source}
                for doc in self.documents.values()
            ],
        }
    
    def _save_index(self) -> None:
        """保存索引到磁盘"""
        try:
            meta = {
                "documents": {
                    doc_id: {
                        "doc_id": doc.doc_id,
                        "title": doc.title,
                        "content": doc.content[:200],  # 只存前 200 字做摘要
                        "source": doc.source,
                        "metadata": doc.metadata,
                        "chunk_ids": [c.chunk_id for c in doc.chunks],
                    }
                    for doc_id, doc in self.documents.items()
                },
                "chunks": {
                    chunk_id: {
                        "chunk_id": chunk.chunk_id,
                        "doc_id": chunk.doc_id,
                        "content": chunk.content,
                        "index": chunk.index,
                    }
                    for chunk_id, chunk in self.chunks.items()
                },
                "vocabulary_size": len(self.vectorizer.vocabulary),
                "doc_count": self.vectorizer.doc_count,
            }
            meta_path = self.index_dir / "index_meta.json"
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
            logger.debug(f"索引元数据已保存: {meta_path}")
        except Exception as e:
            logger.warning(f"保存索引失败: {e}")
    
    def _load_index(self) -> None:
        """从磁盘加载索引"""
        meta_path = self.index_dir / "index_meta.json"
        if not meta_path.exists():
            return
        
        try:
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
            
            # 恢复文档和块
            for doc_id, doc_data in meta.get("documents", {}).items():
                doc = Document(
                    doc_id=doc_data["doc_id"],
                    title=doc_data["title"],
                    content="",  # 完整内容需要重新加载
                    source=doc_data["source"],
                    metadata=doc_data.get("metadata", {}),
                )
                self.documents[doc_id] = doc
            
            for chunk_id, chunk_data in meta.get("chunks", {}).items():
                chunk = Chunk(
                    chunk_id=chunk_data["chunk_id"],
                    doc_id=chunk_data["doc_id"],
                    content=chunk_data["content"],
                    index=chunk_data["index"],
                )
                chunk.tokens = ChineseTokenizer.tokenize(chunk.content)
                self.chunks[chunk_id] = chunk
                self.chunk_list.append(chunk)
            
            # 重建向量
            if self.chunk_list:
                self._rebuild_vectors()
            
            logger.info(f"索引已从磁盘恢复 (文档={len(self.documents)}, 块={len(self.chunks)})")
        except Exception as e:
            logger.warning(f"加载索引失败: {e}")

# ═══════════════════════════════════════════════════════════════
#  便捷函数
# ═══════════════════════════════════════════════════════════════

def create_rag_engine(index_dir: str = None) -> RAGEngine:
    """创建 RAG 引擎实例"""
    if index_dir is None:
        index_dir = "data/rag_index"
    return RAGEngine(index_dir=index_dir)

# ═══════════════════════════════════════════════════════════════
#  模块导出
# ═══════════════════════════════════════════════════════════════
__all__ = [
    'ChineseTokenizer',
    'TfidfVectorizer',
    'DocumentChunk',
    'SearchResult',
    'RAGEngine',
    'create_rag_engine',
]
