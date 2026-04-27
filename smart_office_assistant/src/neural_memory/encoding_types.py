"""
__all__ = [
    'to_dict',
]

记忆编码系统 - 类型定义
Encoding Types, Context, and MemoryEncoding data structures.

从 memory_encoding_system_v3.py 拆分而来 (2026-04-06 S3b)
单一职责: 仅包含枚举和数据结构定义
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class EncodingGranularity(Enum):
    """编码颗粒度"""
    CHARACTER = "character"     # 字符级别
    WORD = "word"                # 词级别
    PHRASE = "phrase"           # 短语级别
    SENTENCE = "sentence"        # 句子级别
    PARAGRAPH = "paragraph"      # 段落级别
    SECTION = "section"          # 节级别
    DOCUMENT = "document"        # 文档级别
    MULTI = "multi"              # 多层级

class EncodingModality(Enum):
    """编码模态"""
    TEXT = "text"                # 文本
    IMAGE = "image"              # 图像
    AUDIO = "audio"              # 音频
    VIDEO = "video"              # 视频
    MULTI = "multi"              # 多模态

class EncodingType(Enum):
    """编码类型 - v3.1增强版 + v3.2 咨询经验编码"""
    SEMANTIC = "semantic"              # 语义编码
    SYNTACTIC = "syntactic"            # 句法编码
    CONTEXT = "context"                # 上下文编码
    EMOTION = "emotion"                # 情感编码
    TEMPORAL = "temporal"              # 时序编码
    KNOWLEDGE = "knowledge"            # 知识图谱编码
    HYBRID = "hybrid"                  # 混合编码
    # v3.1新增
    CONTRASTIVE = "contrastive"        # 对比编码
    ATTENTION = "attention"            # 注意力编码
    CAUSAL = "causal"                  # 因果编码
    ABSTRACTION = "abstraction"        # 抽象编码
    CROSS_MODAL = "cross_modal"        # 跨模态对齐
    METACOGNITIVE = "metacognitive"    # 元认知编码
    SEMANTIC_FIELD = "semantic_field"  # 语义场编码
    DYNAMIC = "dynamic"                # 动态编码
    # v3.2新增: 咨询经验编码
    CONSULTING_EXPERIENCE = "consulting_experience"  # 咨询经验编码
    STRATEGIC_PATTERN = "strategic_pattern"          # 战略模式编码
    ANTI_PATTERN = "anti_pattern"                    # 反模式编码
    METHODOLOGY = "methodology"                      # 方法论编码

@dataclass
class EncodingContext:
    """编码上下文 - 增强版"""
    user_id: str
    session_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 场景信息
    scenario: str = "general"
    task_type: str = "general"
    domain: str = "general"  # 新增: 领域
    
    # 情感信息
    emotion: str = "neutral"
    emotion_intensity: float = 0.0
    
    # 优先级
    priority: int = 5  # 1-10
    
    # v3.1新增
    attention_focus: List[str] = field(default_factory=list)  # 注意力焦点
    causal_relationships: List[Dict[str, str]] = field(default_factory=list)  # 因果关系
    abstraction_level: int = 0  # 抽象层级 (0=具体, 1=中等, 2=抽象)
    
    # 元认知信息
    encoding_confidence: float = 0.8  # 编码置信度
    feedback_received: List[float] = field(default_factory=list)  # 收到的反馈
    
    # v3.2新增: 咨询场景信息
    consulting_phase: str = ""        # 咨询阶段: research/think/analyze/validate
    consulting_domain: str = ""       # 咨询领域: growth/brand/channel/product
    verified: bool = False            # 是否经过验证
    lesson_source: str = ""           # 经验来源: 案例名/项目名
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MemoryEncoding:
    """记忆编码 - 增强版"""
    id: str
    original_content: str
    encoded_vectors: Dict[str, List[float]]  # 不同类型的编码向量
    
    # 编码信息
    granularity: EncodingGranularity
    modality: EncodingModality
    encoding_types: List[EncodingType]
    
    # 上下文
    context: EncodingContext
    
    # 质量metrics
    quality_score: float = 0.8
    confidence: float = 0.8
    
    # v3.1新增
    attention_weights: Optional[List[float]] = None  # 注意力权重
    causal_links: Optional[List[Dict[str, Any]]] = None  # 因果链接
    abstraction_levels: Optional[Dict[str, float]] = None  # 抽象层级分数
    semantic_field: Optional[Dict[str, float]] = None  # 语义场
    
    # 关联信息
    related_memories: List[str] = field(default_factory=list)
    knowledge_graph_nodes: List[str] = field(default_factory=list)
    
    # 跨模态信息
    cross_modal_alignments: Optional[Dict[str, Any]] = None  # 跨模态对齐
    
    # 时序信息
    temporal_sequence: int = 0
    temporal_dependencies: List[str] = field(default_factory=list)
    
    # 元认知信息
    encoding_process: Optional[Dict[str, Any]] = None  # 编码过程元信息
    
    # 动态调整
    dynamic_adjustments: List[Dict[str, Any]] = field(default_factory=list)  # 动态调整历史
    
    # 统计信息
    access_count: int = 0
    last_accessed: str = field(default_factory=lambda: datetime.now().isoformat())
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'original_content': self.original_content,
            'encoded_vectors': self.encoded_vectors,
            'granularity': self.granularity.value,
            'modality': self.modality.value,
            'encoding_types': [t.value for t in self.encoding_types],
            'context': {
                'user_id': self.context.user_id,
                'session_id': self.context.session_id,
                'timestamp': self.context.timestamp,
                'scenario': self.context.scenario,
                'task_type': self.context.task_type,
                'domain': self.context.domain,
                'emotion': self.context.emotion,
                'emotion_intensity': self.context.emotion_intensity,
                'priority': self.context.priority,
                'attention_focus': self.context.attention_focus,
                'causal_relationships': self.context.causal_relationships,
                'abstraction_level': self.context.abstraction_level,
                'encoding_confidence': self.context.encoding_confidence,
                'feedback_received': self.context.feedback_received,
                'metadata': self.context.metadata
            },
            'quality_score': self.quality_score,
            'confidence': self.confidence,
            'attention_weights': self.attention_weights,
            'causal_links': self.causal_links,
            'abstraction_levels': self.abstraction_levels,
            'semantic_field': self.semantic_field,
            'related_memories': self.related_memories,
            'knowledge_graph_nodes': self.knowledge_graph_nodes,
            'cross_modal_alignments': self.cross_modal_alignments,
            'temporal_sequence': self.temporal_sequence,
            'temporal_dependencies': self.temporal_dependencies,
            'encoding_process': self.encoding_process,
            'dynamic_adjustments': self.dynamic_adjustments,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed,
            'created_at': self.created_at
        }
