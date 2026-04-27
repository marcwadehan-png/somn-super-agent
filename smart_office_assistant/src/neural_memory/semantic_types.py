"""
__all__ = [
    'from_dict',
    'to_dict',
]

语义记忆类型定义 - 多用户语义记忆引擎的数据结构
Semantic Memory Types - Data structures for Multi-User Semantic Memory Engine
"""

from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, field, asdict

# ==================== 多用户数据结构 ====================

@dataclass
class KeywordMapping:
    """关键词-语义mapping条目"""
    keyword: str
    semantic_meanings: List[str] = field(default_factory=list)
    primary_meaning: str = ""
    frequency: int = 0
    contexts: List[str] = field(default_factory=list)
    confidence: float = 0.5
    examples: List[Dict[str, str]] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    verified: bool = False
    # v2.0 新增:来源追踪
    source: str = "learning"  # learning | feedback | system

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'KeywordMapping':
        return cls(**data)

@dataclass
class UserSemanticProfile:
    """用户语义画像"""
    user_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())
    total_inputs: int = 0
    total_learnings: int = 0
    total_clarifications: int = 0
    dominant_intents: Dict[str, int] = field(default_factory=dict)  # 意图分布
    avg_confidence: float = 0.0
    understanding_accuracy: float = 0.0  # 反馈正确率

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserSemanticProfile':
        return cls(**data)

@dataclass
class SemanticContext:
    """语义理解上下文"""
    user_id: str                           # v2.0 新增
    raw_input: str
    tokens: List[str] = field(default_factory=list)
    keywords_extracted: List[str] = field(default_factory=list)
    inferred_intent: str = "unknown"
    intent_confidence: float = 0.0
    reasoning_chain: List[str] = field(default_factory=list)
    needs_clarification: bool = False
    clarification_question: str = ""
    matched_mappings: List[Dict] = field(default_factory=list)
    personalization_applied: bool = False  # v2.0 新增:是否使用了用户个性化

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        return result

@dataclass
class UserFeedback:
    """用户反馈记录"""
    user_id: str                           # v2.0 新增
    input_text: str
    system_understanding: str
    user_correction: str = ""
    is_correct: bool = True
    feedback_time: str = field(default_factory=lambda: datetime.now().isoformat())
    intent_before: str = ""
    intent_after: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserFeedback':
        return cls(**data)
