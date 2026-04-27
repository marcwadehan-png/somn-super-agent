# -*- coding: utf-8 -*-
"""
深度推理引擎类型定义模块
Deep Reasoning Engine Types Module

提供推理引擎所需的数据类型、枚举和常量定义。
与主模块分离以支持更好的模块化和延迟导入。

v2.0 - 从 deep_reasoning_engine.py 提取 (2026-04-06)
"""

import logging
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# ── ReasoningMode 枚举 ─────────────────────────────────────────────────────────

class ReasoningMode(Enum):
    """推理模式枚举"""
    CHAIN_OF_THOUGHT = "chain_of_thought"  # 链式推理
    TREE_OF_THOUGHTS = "tree_of_thoughts"  # 树推理
    GRAPH_OF_THOUGHTS = "graph_of_thoughts"  # 图推理
    META_REASONING = "meta_reasoning"      # 元推理
    NARRATIVE_REASONING = "narrative_reasoning"  # 叙事推理(文学智能增强)
    CONSULTING_REASONING = "consulting_reasoning"  # 咨询推理(增长咨询增强)
    YINYANG_DIALECTICAL = "yinyang_dialectical"  # 阴阳辩证推理 [v5.0.0 道家哲学增强]
    NEURODYNAMICS = "neurodynamics"  # 神经动力学推理 [v5.1.0 神经科学增强]
    SEQUENCE_REASONING = "sequence_reasoning"  # 数列推理 [v6.0.0 数学智慧增强]
    GRAPH_THEORY_REASONING = "graph_theory_reasoning"  # 图论推理 [v6.0.0 数学智慧增强]
    COMBINATORIAL_OPTIMIZATION = "combinatorial_optimization"  # 组合优化推理 [v6.0.0 数学智慧增强]
    XINMIND_THINKING = "xinmind_thinking"  # xinxue思维推理 [v7.0.0 xinxue增强]
    DEWEY_THINKING = "dewey_thinking"  # 杜威反省思维推理 [v7.0.0 思维训练增强]
    TOP_METHODS_THINKING = "top_methods_thinking"  # 顶级思维法推理 [v7.0.0 思维方法增强]

# ── ThoughtNode 数据类 ─────────────────────────────────────────────────────────

@dataclass
class ThoughtNode:
    """推理节点"""
    id: str
    content: str
    reasoning_mode: ReasoningMode
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    # 评估
    confidence: float = 0.0
    completeness: float = 0.0
    validity: float = 0.0
    
    # 状态
    status: str = "pending"  # pending, processing, completed, failed
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'reasoning_mode': getattr(self.reasoning_mode, 'value', self.reasoning_mode),
            'parent_id': self.parent_id,
            'children_ids': self.children_ids,
            'confidence': self.confidence,
            'completeness': self.completeness,
            'validity': self.validity,
            'status': self.status,
            'metadata': self.metadata,
            'created_at': self.created_at
        }

# ── ReasoningResult 数据类 ─────────────────────────────────────────────────────

@dataclass
class ReasoningResult:
    """推理结果"""
    result_id: str
    problem: str
    reasoning_mode: ReasoningMode
    success: bool
    
    # 推理过程
    reasoning_trace: List[ThoughtNode]
    final_answer: str
    
    # 评估
    confidence: float = 0.0
    steps_count: int = 0
    
    # 性能
    execution_time: float = 0.0
    
    # 建议
    suggestions: List[str] = field(default_factory=list)
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'result_id': self.result_id,
            'problem': self.problem,
            'reasoning_mode': getattr(self.reasoning_mode, 'value', self.reasoning_mode),
            'success': self.success,
            'reasoning_trace': [node.to_dict() if hasattr(node, 'to_dict') else node for node in self.reasoning_trace],
            'final_answer': self.final_answer,
            'confidence': self.confidence,
            'steps_count': self.steps_count,
            'execution_time': self.execution_time,
            'suggestions': self.suggestions,
            'metadata': self.metadata
        }

# ── 导出列表 ──────────────────────────────────────────────────────────────────

__all__ = [
    'ReasoningMode',
    'ThoughtNode',
    'ReasoningResult',
]
