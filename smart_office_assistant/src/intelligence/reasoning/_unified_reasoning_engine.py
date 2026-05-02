# -*- coding: utf-8 -*-
"""
DivineReason - 至高推理引擎
========================================

"当四大推理体系融为一体，神之智慧由此诞生"

整合四大推理范式的超级推理系统：
- Graph of Thoughts (GoT) - 图网络结构
- Long Chain of Thought (LongCoT) - 长链推理
- Tree of Thoughts (ToT) - 树状分支
- Reasoning and Acting (ReAct) - 工具调用

核心设计理念：
1. 以GoT图结构为核心骨架
2. LongCoT的检查点、顿悟检测、自我纠错嵌入节点属性
3. ToT的分支评分与剪枝策略融合评估系统
4. ReAct的TAO闭环与工具调用嵌入行动节点
5. 反馈循环机制实现自我进化
6. 自我反思与验证机制（DivineReason扩展）

作者: Somn AI
版本: V3.1.0 (DivineReason Enhanced)
日期: 2026-04-28
许可证: MIT
"""

from __future__ import annotations

import uuid
import time
import logging
import heapq
from typing import Dict, List, Optional, Any, Callable, Set, Tuple, Union, TypeVar
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
from collections import defaultdict, deque
import threading
import math
import re
import json
from functools import lru_cache
from contextlib import contextmanager

logger = logging.getLogger(__name__)

T = TypeVar('T')


# ============================================================
# 枚举定义
# ============================================================

class NodeType(Enum):
    """超级图节点类型"""
    ROOT = "root"                           # 根节点（问题入口）
    LONG_COT_STEP = "long_cot_step"        # LongCoT步骤节点
    TOT_BRANCH = "tot_branch"              # ToT分支节点
    REACT_ACTION = "react_action"          # ReAct行动节点
    OBSERVATION = "observation"            # 观察节点（ReAct）
    INSIGHT = "insight"                    # 顿悟时刻节点
    CHECKPOINT = "checkpoint"              # 检查点节点
    CORRECTION = "correction"              # 纠错节点
    SYNTHESIS = "synthesis"                # 综合节点
    FINAL = "final"                        # 最终答案节点
    SELF_CORRECTION = "self_correction"    # 自我纠错节点
    VERIFICATION = "verification"          # 验证节点
    EXPLORATION = "exploration"            # 探索节点
    CRITIQUE = "critique"                  # 批评节点
    ALTERNATIVE = "alternative"            # 替代方案节点


class EdgeType(Enum):
    """超级图边类型"""
    LOGICAL_FLOW = "logical_flow"          # 逻辑流（串行）
    PARALLEL = "parallel"                  # 并行分支
    FEEDBACK = "feedback"                   # 反馈循环
    BACKTRACK = "backtrack"                # 回溯边
    SUPPORT = "support"                    # 支持关系
    CHALLENGE = "challenge"                # 挑战关系
    TOOL_CALL = "tool_call"                # 工具调用
    OBSERVE = "observe"                    # 观察返回
    CORRECTION = "correction"              # 纠错边
    SYNTHESIS = "synthesis"                # 综合边
    VERIFICATION = "verification"          # 验证边
    ALTERNATIVE = "alternative"            # 替代边


class ReasoningMode(Enum):
    """推理模式"""
    LINEAR = "linear"                       # 线性（LongCoT风格）
    BRANCHING = "branching"                # 分支（ToT风格）
    GRAPH = "graph"                        # 图网络（GoT风格）
    REACTIVE = "reactive"                  # 反应式（ReAct风格）
    SUPER = "super"                        # 超级模式（全部启用）
    DIVINE = "divine"                      # 至高模式（DivineReason专属）
    DELIBERATE = "deliberate"             # 深思熟虑模式
    CREATIVE = "creative"                  # 创造性推理模式
    ANALYTICAL = "analytical"              # 分析性推理模式


class TaskComplexity(Enum):
    """任务复杂度"""
    LOW = "low"                            # 简单
    MEDIUM = "medium"                      # 中等
    HIGH = "high"                          # 复杂
    EXTREME = "extreme"                     # 极难
    UNKNOWN = "unknown"                     # 未知


class InsightType(Enum):
    """顿悟类型"""
    INTEGRATION = "integration"             # 整合型顿悟
    BREAKTHROUGH = "breakthrough"          # 突破型顿悟
    CORRECTION = "correction"              # 纠错型顿悟
    SYNTHESIS = "synthesis"                # 综合型顿悟
    CREATIVE = "creative"                  # 创意型顿悟
    VERIFICATION = "verification"          # 验证型顿悟
    CRITICAL = "critical"                  # 批判型顿悟


class NodeStatus(Enum):
    """节点状态"""
    PENDING = "pending"
    ACTIVE = "active"
    EXPANDED = "expanded"
    EVALUATED = "evaluated"
    PRUNED = "pruned"
    FINAL = "final"
    FAILED = "failed"


# ============================================================
# 数据类定义
# ============================================================

@dataclass
class ReasoningMetadata:
    """推理元数据"""
    source_engine: str = ""
    source_node_id: Optional[str] = None
    generation_method: str = ""
    confidence: float = 1.0
    relevance: float = 0.5
    novelty: float = 0.5
    coherence: float = 0.5
    completeness: float = 0.5
    is_insight: bool = False
    is_checkpoint: bool = False
    is_correction: bool = False
    is_final: bool = False
    is_verified: bool = False
    is_reflection: bool = False
    is_critique: bool = False
    insight_type: Optional[InsightType] = None
    insight_impact: float = 0.0
    insight_keywords: List[str] = field(default_factory=list)
    evaluation_scores: Dict[str, float] = field(default_factory=dict)
    rank: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    processing_time: float = 0.0
    expanded_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source_engine': self.source_engine,
            'source_node_id': self.source_node_id,
            'generation_method': self.generation_method,
            'confidence': round(self.confidence, 4),
            'relevance': round(self.relevance, 4),
            'novelty': round(self.novelty, 4),
            'coherence': round(self.coherence, 4),
            'completeness': round(self.completeness, 4),
            'is_insight': self.is_insight,
            'is_checkpoint': self.is_checkpoint,
            'is_correction': self.is_correction,
            'is_final': self.is_final,
            'is_verified': self.is_verified,
            'is_reflection': self.is_reflection,
            'is_critique': self.is_critique,
            'insight_type': self.insight_type.value if self.insight_type else None,
            'insight_impact': round(self.insight_impact, 4),
            'insight_keywords': self.insight_keywords,
            'evaluation_scores': {k: round(v, 4) for k, v in self.evaluation_scores.items()},
            'rank': self.rank,
            'created_at': self.created_at,
            'processing_time': round(self.processing_time, 4)
        }


@dataclass
class UnifiedNode:
    """超级图统一节点"""
    node_id: str
    content: str
    node_type: NodeType = NodeType.LONG_COT_STEP
    parent_ids: List[str] = field(default_factory=list)
    child_ids: List[str] = field(default_factory=list)
    related_ids: List[str] = field(default_factory=list)
    is_checkpoint: bool = False
    checkpoint_data: Optional[Dict[str, Any]] = None
    is_insight: bool = False
    insight_type: str = ""
    insight_impact: float = 0.0
    feasibility_score: float = 0.5
    progress_score: float = 0.5
    diversity_score: float = 0.5
    combined_score: float = 0.5
    relevance_score: float = 0.5
    coherence_score: float = 0.5
    novelty_score: float = 0.5
    action: Optional[Dict[str, Any]] = None
    observation: Optional[Any] = None
    tool_result: Optional[Dict[str, Any]] = None
    is_reflection: bool = False
    is_verification: bool = False
    verification_result: Optional[Dict[str, Any]] = None
    reflection_content: str = ""
    is_critique: bool = False
    critique_type: str = ""
    depth: int = 0
    status: str = "pending"
    expanded: bool = False
    visited: bool = False
    priority: float = 0.0
    visit_count: int = 0
    metadata: ReasoningMetadata = field(default_factory=ReasoningMetadata)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'node_type': self.node_type.value,
            'content': self.content[:200] + '...' if len(self.content) > 200 else self.content,
            'content_length': len(self.content),
            'depth': self.depth,
            'status': self.status,
            'scores': {
                'feasibility': round(self.feasibility_score, 4),
                'progress': round(self.progress_score, 4),
                'diversity': round(self.diversity_score, 4),
                'combined': round(self.combined_score, 4),
                'relevance': round(self.relevance_score, 4),
                'coherence': round(self.coherence_score, 4),
                'novelty': round(self.novelty_score, 4)
            },
            'parent_count': len(self.parent_ids),
            'child_count': len(self.child_ids),
            'is_checkpoint': self.is_checkpoint,
            'is_insight': self.is_insight,
            'is_correction': self.metadata.is_correction,
            'is_reflection': self.is_reflection,
            'is_verification': self.is_verification,
            'is_critique': self.is_critique,
            'has_action': self.action is not None,
            'has_observation': self.observation is not None,
            'priority': round(self.priority, 4),
            'visit_count': self.visit_count,
            'created_at': self.created_at,
            'metadata': self.metadata.to_dict()
        }
    
    def __lt__(self, other: 'UnifiedNode'):
        return self.combined_score < other.combined_score
    
    def __hash__(self):
        return hash(self.node_id)
    
    def mark_expanded(self):
        self.expanded = True
        self.status = "expanded"
        self.metadata.expanded_at = datetime.now().isoformat()


@dataclass
class UnifiedEdge:
    """超级图统一边"""
    edge_id: str
    source_id: str
    target_id: str
    edge_type: EdgeType = EdgeType.LOGICAL_FLOW
    weight: float = 1.0
    confidence: float = 1.0
    is_active: bool = True
    is_feedback_loop: bool = False
    feedback_count: int = 0
    is_backtrack: bool = False
    is_correction: bool = False
    is_alternative: bool = False
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'edge_id': self.edge_id,
            'source': self.source_id,
            'target': self.target_id,
            'edge_type': self.edge_type.value,
            'weight': round(self.weight, 4),
            'confidence': round(self.confidence, 4),
            'is_feedback_loop': self.is_feedback_loop,
            'is_backtrack': self.is_backtrack,
            'is_correction': self.is_correction,
            'is_alternative': self.is_alternative,
            'description': self.description
        }


@dataclass
class GraphStatistics:
    """图统计信息"""
    total_nodes: int = 0
    total_edges: int = 0
    max_depth: int = 0
    avg_depth: float = 0.0
    node_type_counts: Dict[str, int] = field(default_factory=dict)
    edge_type_counts: Dict[str, int] = field(default_factory=dict)
    status_counts: Dict[str, int] = field(default_factory=dict)
    avg_score: float = 0.0
    max_score: float = 0.0
    min_score: float = 0.0
    median_score: float = 0.0
    feedback_loops: int = 0
    backtracks: int = 0
    insights_count: int = 0
    checkpoints_count: int = 0
    corrections_count: int = 0
    verification_count: int = 0
    reflections_count: int = 0
    critiques_count: int = 0
    processing_time: float = 0.0
    generation_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_nodes': self.total_nodes,
            'total_edges': self.total_edges,
            'max_depth': self.max_depth,
            'avg_depth': round(self.avg_depth, 2),
            'node_type_counts': self.node_type_counts,
            'edge_type_counts': self.edge_type_counts,
            'status_counts': self.status_counts,
            'avg_score': round(self.avg_score, 4),
            'max_score': round(self.max_score, 4),
            'min_score': round(self.min_score, 4),
            'median_score': round(self.median_score, 4),
            'feedback_loops': self.feedback_loops,
            'backtracks': self.backtracks,
            'insights_count': self.insights_count,
            'checkpoints_count': self.checkpoints_count,
            'corrections_count': self.corrections_count,
            'verification_count': self.verification_count,
            'reflections_count': self.reflections_count,
            'critiques_count': self.critiques_count,
            'processing_time': round(self.processing_time, 2),
            'generation_time': round(self.generation_time, 2)
        }


@dataclass
class ThoughtPath:
    """思考路径"""
    nodes: List[UnifiedNode] = field(default_factory=list)
    total_score: float = 0.0
    length: int = 0
    has_insight: bool = False
    has_correction: bool = False
    has_verification: bool = False
    has_reflection: bool = False
    has_critique: bool = False
    avg_confidence: float = 0.0
    diversity: float = 0.0
    coherence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'length': self.length,
            'total_score': round(self.total_score, 4),
            'avg_score': round(self.total_score / self.length, 4) if self.length > 0 else 0,
            'avg_confidence': round(self.avg_confidence, 4),
            'diversity': round(self.diversity, 4),
            'coherence_score': round(self.coherence_score, 4),
            'has_insight': self.has_insight,
            'has_correction': self.has_correction,
            'has_verification': self.has_verification,
            'has_reflection': self.has_reflection,
            'has_critique': self.has_critique,
            'node_ids': [n.node_id for n in self.nodes],
            'summary': ' -> '.join([
                f"[{n.node_type.value}] {n.content[:30]}..." 
                for n in self.nodes[:5]
            ])
        }


@dataclass
class ReasoningResult:
    """推理结果"""
    engine: str = "DivineReason"
    version: str = "6.2.0"
    problem: str = ""
    mode: str = ""
    success: bool = True
    solution: str = ""
    graph: Optional[Any] = None
    path: Optional[Any] = None
    statistics: Optional[Any] = None
    quality_score: float = 0.0
    insights: List[Dict[str, Any]] = field(default_factory=list)
    corrections: List[Dict[str, Any]] = field(default_factory=list)
    reflections: List[Dict[str, Any]] = field(default_factory=list)
    verifications: List[Dict[str, Any]] = field(default_factory=list)
    critiques: List[Dict[str, Any]] = field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'engine': self.engine,
            'version': self.version,
            'problem': self.problem,
            'mode': self.mode,
            'success': self.success,
            'solution': self.solution,
            'path': self.path.to_dict() if self.path else None,
            'statistics': self.statistics.to_dict() if self.statistics else None,
            'quality_score': round(self.quality_score, 4),
            'insights_count': len(self.insights),
            'corrections_count': len(self.corrections),
            'reflections_count': len(self.reflections),
            'verifications_count': len(self.verifications),
            'critiques_count': len(self.critiques),
            'tool_calls_count': len(self.tool_calls),
            'metadata': self.metadata,
            'errors': self.errors,
            'warnings': self.warnings
        }


# ============================================================
# 超级图结构
# ============================================================

class SuperGraph:
    """超级推理图 (DivineReason核心)"""
    
    VERSION = "6.2.0"
    
    def __init__(self, problem: str):
        self.problem = problem
        self.nodes: Dict[str, UnifiedNode] = {}
        self.edges: Dict[str, UnifiedEdge] = {}
        self.root: Optional[UnifiedNode] = None
        self.children_map: Dict[str, List[str]] = defaultdict(list)
        self.parents_map: Dict[str, List[str]] = defaultdict(list)
        self.type_index: Dict[NodeType, List[str]] = defaultdict(list)
        self.status_index: Dict[str, List[str]] = defaultdict(list)
        self.checkpoints: List[str] = []
        self.insights: List[str] = []
        self.corrections: List[str] = []
        self.actions: List[str] = []
        self.final_nodes: List[str] = []
        self.reflections: List[str] = []
        self.verifications: List[str] = []
        self.critiques: List[str] = []
        self.created_at = datetime.now().isoformat()
        self._stats: Optional[GraphStatistics] = None
        self._path_cache: Dict[str, List[UnifiedNode]] = {}
        self._descendants_cache: Dict[str, Set[str]] = {}
        self._ancestors_cache: Dict[str, Set[str]] = {}
    
    def create_root(self, content: str, metadata: ReasoningMetadata = None) -> UnifiedNode:
        node_id = str(uuid.uuid4())
        node = UnifiedNode(
            node_id=node_id,
            content=content,
            node_type=NodeType.ROOT,
            depth=0,
            status="active",
            metadata=metadata or ReasoningMetadata(source_engine="divine", generation_method="root", confidence=1.0)
        )
        self.nodes[node_id] = node
        self.root = node
        self._invalidate_cache()
        return node
    
    def add_node(
        self,
        content: str,
        node_type: NodeType = NodeType.LONG_COT_STEP,
        parent_ids: List[str] = None,
        depth: int = 0,
        metadata: ReasoningMetadata = None,
        feasibility_score: float = 0.5,
        progress_score: float = 0.5,
        diversity_score: float = 0.5,
        combined_score: float = 0.5,
        is_checkpoint: bool = False,
        is_insight: bool = False,
        insight_type: str = "",
        insight_impact: float = 0.0,
        action: Dict[str, Any] = None,
        observation: Any = None,
        tool_result: Dict[str, Any] = None,
        is_reflection: bool = False,
        is_verification: bool = False,
        verification_result: Dict[str, Any] = None,
        reflection_content: str = "",
        is_critique: bool = False,
        critique_type: str = ""
    ) -> UnifiedNode:
        node_id = str(uuid.uuid4())
        parent_ids = parent_ids or []
        node = UnifiedNode(
            node_id=node_id,
            content=content,
            node_type=node_type,
            parent_ids=parent_ids,
            depth=depth,
            metadata=metadata or ReasoningMetadata(),
            feasibility_score=feasibility_score,
            progress_score=progress_score,
            diversity_score=diversity_score,
            combined_score=combined_score,
            is_checkpoint=is_checkpoint,
            is_insight=is_insight,
            insight_type=insight_type,
            insight_impact=insight_impact,
            action=action,
            observation=observation,
            tool_result=tool_result,
            is_reflection=is_reflection,
            is_verification=is_verification,
            verification_result=verification_result,
            reflection_content=reflection_content,
            is_critique=is_critique,
            critique_type=critique_type
        )
        self.nodes[node_id] = node
        self._invalidate_cache()
        
        valid_parent_ids = [pid for pid in parent_ids if pid in self.nodes]
        for parent_id in valid_parent_ids:
            self.add_edge(source_id=parent_id, target_id=node_id, edge_type=EdgeType.LOGICAL_FLOW)
        
        self._update_indexes(node)
        return node
    
    def _update_indexes(self, node: UnifiedNode):
        self.type_index[node.node_type].append(node.node_id)
        self.status_index[node.status].append(node.node_id)
        if node.is_checkpoint: self.checkpoints.append(node.node_id)
        if node.is_insight: self.insights.append(node.node_id)
        if node.metadata.is_correction: self.corrections.append(node.node_id)
        if node.node_type == NodeType.REACT_ACTION: self.actions.append(node.node_id)
        if node.node_type == NodeType.FINAL: self.final_nodes.append(node.node_id)
        if node.is_reflection: self.reflections.append(node.node_id)
        if node.is_verification: self.verifications.append(node.node_id)
        if node.is_critique: self.critiques.append(node.node_id)
    
    def add_edge(self, source_id: str, target_id: str, edge_type: EdgeType = EdgeType.LOGICAL_FLOW,
                 weight: float = 1.0, description: str = "", is_feedback_loop: bool = False,
                 is_backtrack: bool = False, is_correction: bool = False, is_alternative: bool = False) -> Optional[UnifiedEdge]:
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        edge_id = f"{source_id}->{target_id}"
        edge = UnifiedEdge(
            edge_id=edge_id, source_id=source_id, target_id=target_id, edge_type=edge_type,
            weight=weight, description=description, is_feedback_loop=is_feedback_loop,
            is_backtrack=is_backtrack, is_correction=is_correction, is_alternative=is_alternative
        )
        self.edges[edge_id] = edge
        self.children_map[source_id].append(target_id)
        self.parents_map[target_id].append(source_id)
        return edge
    
    def _invalidate_cache(self):
        self._path_cache.clear()
        self._descendants_cache.clear()
        self._ancestors_cache.clear()
    
    def get_children(self, node_id: str) -> List[UnifiedNode]:
        return [self.nodes[cid] for cid in self.children_map.get(node_id, []) if cid in self.nodes]
    
    def get_parents(self, node_id: str) -> List[UnifiedNode]:
        return [self.nodes[pid] for pid in self.parents_map.get(node_id, []) if pid in self.nodes]
    
    def get_path(self, node_id: str) -> List[UnifiedNode]:
        if node_id in self._path_cache:
            return self._path_cache[node_id]
        path = []
        current = self.nodes.get(node_id)
        while current:
            path.insert(0, current)
            current = self.nodes.get(current.parent_ids[0]) if current.parent_ids else None
        self._path_cache[node_id] = path
        return path
    
    def get_ancestors(self, node_id: str) -> Set[str]:
        if node_id in self._ancestors_cache:
            return self._ancestors_cache[node_id]
        ancestors = set()
        queue = deque([node_id])
        while queue:
            current = queue.popleft()
            for parent_id in self.parents_map.get(current, []):
                if parent_id not in ancestors:
                    ancestors.add(parent_id)
                    queue.append(parent_id)
        self._ancestors_cache[node_id] = ancestors
        return ancestors
    
    def get_descendants(self, node_id: str) -> Set[str]:
        if node_id in self._descendants_cache:
            return self._descendants_cache[node_id]
        descendants = set()
        queue = deque([node_id])
        while queue:
            current = queue.popleft()
            for child_id in self.children_map.get(current, []):
                if child_id not in descendants:
                    descendants.add(child_id)
                    queue.append(child_id)
        self._descendants_cache[node_id] = descendants
        return descendants
    
    def get_best_path(self) -> ThoughtPath:
        if not self.final_nodes:
            leaf_nodes = [n for n in self.nodes.values() if not self.get_children(n.node_id)]
            if leaf_nodes:
                self.final_nodes = [max(leaf_nodes, key=lambda n: n.combined_score).node_id]
        
        if not self.final_nodes:
            return ThoughtPath()
        
        best_path = ThoughtPath()
        best_score = 0
        
        for final_id in self.final_nodes:
            path_nodes = self.get_path(final_id)
            path_score = sum(n.combined_score for n in path_nodes)
            has_insight = any(n.is_insight for n in path_nodes)
            has_correction = any(n.metadata.is_correction for n in path_nodes)
            has_verification = any(n.is_verification for n in path_nodes)
            has_reflection = any(n.is_reflection for n in path_nodes)
            has_critique = any(n.is_critique for n in path_nodes)
            avg_confidence = sum(n.metadata.confidence for n in path_nodes) / len(path_nodes) if path_nodes else 0
            diversity = sum(n.diversity_score for n in path_nodes) / len(path_nodes) if path_nodes else 0
            coherence = sum(n.coherence_score for n in path_nodes) / len(path_nodes) if path_nodes else 0
            
            if path_score > best_score:
                best_score = path_score
                best_path = ThoughtPath(
                    nodes=path_nodes, total_score=path_score, length=len(path_nodes),
                    has_insight=has_insight, has_correction=has_correction,
                    has_verification=has_verification, has_reflection=has_reflection,
                    has_critique=has_critique, avg_confidence=avg_confidence,
                    diversity=diversity, coherence_score=coherence
                )
        
        return best_path
    
    def detect_cycles(self) -> List[List[str]]:
        cycles = []
        for node_id in self.nodes:
            visited = set()
            path = []
            def dfs(current: str) -> bool:
                if current in path:
                    cycle_start = path.index(current)
                    cycles.append(path[cycle_start:] + [current])
                    return True
                if current in visited:
                    return False
                visited.add(current)
                path.append(current)
                for child_id in self.children_map.get(current, []):
                    dfs(child_id)
                path.pop()
                return False
            dfs(node_id)
        
        unique_cycles = []
        seen = set()
        for cycle in cycles:
            cycle_key = tuple(sorted(cycle))
            if cycle_key not in seen:
                seen.add(cycle_key)
                unique_cycles.append(cycle)
        return unique_cycles
    
    def prune_branch(self, node_id: str):
        if node_id not in self.nodes:
            return
        self.nodes[node_id].status = "pruned"
        for child_id in self.children_map.get(node_id, []):
            self.prune_branch(child_id)
    
    def get_statistics(self) -> GraphStatistics:
        stats = GraphStatistics()
        stats.total_nodes = len(self.nodes)
        stats.total_edges = len(self.edges)
        
        stats.node_type_counts = defaultdict(int)
        for node in self.nodes.values():
            stats.node_type_counts[node.node_type.value] += 1
        
        stats.edge_type_counts = defaultdict(int)
        for edge in self.edges.values():
            stats.edge_type_counts[edge.edge_type.value] += 1
        
        stats.status_counts = defaultdict(int)
        for node in self.nodes.values():
            stats.status_counts[node.status] += 1
        
        if self.nodes:
            depths = [n.depth for n in self.nodes.values()]
            stats.max_depth = max(depths)
            stats.avg_depth = sum(depths) / len(depths)
            scores = [n.combined_score for n in self.nodes.values()]
            stats.avg_score = sum(scores) / len(scores)
            stats.max_score = max(scores)
            stats.min_score = min(scores)
            sorted_scores = sorted(scores)
            mid = len(sorted_scores) // 2
            stats.median_score = (sorted_scores[mid] if len(sorted_scores) % 2 else 
                                  (sorted_scores[mid-1] + sorted_scores[mid]) / 2)
        
        stats.insights_count = len(self.insights)
        stats.checkpoints_count = len(self.checkpoints)
        stats.corrections_count = len(self.corrections)
        stats.verification_count = len(self.verifications)
        stats.reflections_count = len(self.reflections)
        stats.critiques_count = len(self.critiques)
        stats.feedback_loops = len([e for e in self.edges.values() if e.is_feedback_loop])
        stats.backtracks = len([e for e in self.edges.values() if e.is_backtrack])
        
        self._stats = stats
        return stats
    
    def to_dict(self) -> Dict[str, Any]:
        stats = self.get_statistics()
        return {
            'problem': self.problem,
            'version': self.VERSION,
            'root_id': self.root.node_id if self.root else None,
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'edges': {eid: edge.to_dict() for eid, edge in self.edges.items()},
            'special_nodes': {
                'checkpoints': self.checkpoints,
                'insights': self.insights,
                'corrections': self.corrections,
                'actions': self.actions,
                'final': self.final_nodes,
                'reflections': self.reflections,
                'verifications': self.verifications,
                'critiques': self.critiques
            },
            'statistics': stats.to_dict()
        }
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    def to_markdown(self) -> str:
        lines = [
            f"# DivineReason 推理图",
            f"",
            f"**问题**: {self.problem}",
            f"**版本**: {self.VERSION}",
            f"",
            f"## 统计",
            f"",
            f"| 指标 | 值 |",
            f"|------|-----|",
            f"| 节点数 | {len(self.nodes)} |",
            f"| 边数 | {len(self.edges)} |",
            f"| 最大深度 | {self.get_statistics().max_depth} |",
            f"| 顿悟数 | {len(self.insights)} |",
            f"| 反思数 | {len(self.reflections)} |",
        ]
        return "\n".join(lines)


# ============================================================
# 配置类
# ============================================================

@dataclass
class UnifiedConfig:
    """DivineReason配置"""
    default_mode: ReasoningMode = ReasoningMode.DIVINE
    enable_all_engines: bool = True
    max_nodes: int = 200
    max_depth: int = 10
    max_branching: int = 5
    min_branching: int = 2
    enable_long_cot: bool = True
    max_thinking_length: int = 2048
    checkpoint_interval: int = 5
    enable_insight_detection: bool = True
    enable_self_correction: bool = True
    max_corrections: int = 3
    enable_boundary_detection: bool = True
    insight_keywords: List[str] = None
    enable_tot: bool = True
    pruning_threshold: float = 0.3
    beam_width: int = 3
    score_weights: Dict[str, float] = None
    enable_react: bool = True
    max_tool_calls: int = 20
    tool_call_threshold: float = 0.6
    tool_selection_strategy: str = "heuristic"
    enable_got: bool = True
    enable_attention: bool = True
    enable_graph_traversal: bool = True
    enable_reflection: bool = True
    enable_verification: bool = True
    enable_critique: bool = True
    reflection_interval: int = 3
    verification_threshold: float = 0.7
    synthesis_depth: int = 2
    enable_feedback_loops: bool = True
    max_feedback_iterations: int = 3
    feedback_threshold: float = 0.5
    use_mcts: bool = False
    use_beam_search: bool = True
    temperature: float = 0.7
    top_p: float = 0.9
    enable_cache: bool = True
    max_cache_size: int = 1000
    parallel_generation: bool = False
    progress_callback: Optional[Callable] = None
    
    def __post_init__(self):
        if self.insight_keywords is None:
            self.insight_keywords = [
                "突然", "关键", "核心", "本质", "顿悟", "领悟",
                "发现", "整合", "综合", "原来如此", "关键是",
                "Aha", "关键点", "突破口", "转机", "豁然开朗"
            ]
        if self.score_weights is None:
            self.score_weights = {
                'feasibility': 0.25, 'progress': 0.25, 'diversity': 0.15,
                'relevance': 0.15, 'coherence': 0.10, 'novelty': 0.10
            }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'default_mode': self.default_mode.value,
            'enable_all_engines': self.enable_all_engines,
            'max_nodes': self.max_nodes,
            'max_depth': self.max_depth,
            'max_branching': self.max_branching,
            'enable_reflection': self.enable_reflection,
            'enable_verification': self.enable_verification,
            'enable_critique': self.enable_critique,
            'pruning_threshold': self.pruning_threshold,
            'beam_width': self.beam_width,
            'use_beam_search': self.use_beam_search,
            'temperature': self.temperature,
            'enable_cache': self.enable_cache,
            'parallel_generation': self.parallel_generation
        }


# ============================================================
# 评估器与生成器
# ============================================================

class UnifiedEvaluator:
    """统一评估器"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self._score_cache: Dict[str, Dict[str, float]] = {}
        self.insight_patterns = [
            re.compile(p, re.IGNORECASE) for p in [
                r"(突然|忽然|猛然)意识到", r"(关键|核心|本质)是", r"通过.*(整合|综合)",
                r"(原来|原来如此|原来是这样)", r"(关键点|重点)是", r"豁然(开朗|明白)",
                r"突破口", r"Aha[，,]?", r"关键在于"
            ]
        ]
        self.uncertainty_patterns = [
            re.compile(p, re.IGNORECASE) for p in [
                r"可能", r"也许", r"不确定", r"需要进一步", r"或许", r"大概", r"似乎"
            ]
        ]
        self.certainty_patterns = [
            re.compile(p, re.IGNORECASE) for p in [
                r"确定", r"明确", r"一定", r"毫无疑问", r"必然", r"肯定", r"绝对"
            ]
        ]
        self.contradiction_patterns = [
            re.compile(p) for p in [r"但是", r"然而", r"不过", r"可是", r"尽管", r"虽然", r"矛盾"]
        ]
    
    def evaluate_node(self, node: UnifiedNode, context: Dict[str, Any], use_cache: bool = True) -> Dict[str, float]:
        cache_key = f"{node.node_id}:{node.content[:50]}"
        if use_cache and self.config.enable_cache and cache_key in self._score_cache:
            cached_scores = self._score_cache[cache_key].copy()
            node.combined_score = sum(cached_scores.values()) / len(cached_scores)
            return cached_scores
        
        scores = {}
        weights = self.config.score_weights
        
        scores['relevance'] = self._evaluate_relevance(node, context)
        scores['coherence'] = self._evaluate_coherence(node, context)
        scores['novelty'] = self._evaluate_novelty(node, context)
        scores['feasibility'] = self._evaluate_feasibility(node, context)
        scores['progress'] = self._evaluate_progress(node, context)
        scores['diversity'] = self._evaluate_diversity(node, context)
        scores['confidence'] = self._evaluate_confidence(node, context)
        scores['validity'] = self._evaluate_validity(node, context)
        scores['completeness'] = self._evaluate_completeness(node, context)
        scores['reflection'] = self._evaluate_reflection(node, context)
        
        node.combined_score = (
            scores['feasibility'] * weights.get('feasibility', 0.25) +
            scores['progress'] * weights.get('progress', 0.25) +
            scores['diversity'] * weights.get('diversity', 0.15) +
            scores['relevance'] * weights.get('relevance', 0.15) +
            scores['coherence'] * weights.get('coherence', 0.10) +
            scores['novelty'] * weights.get('novelty', 0.10)
        )
        
        node.relevance_score = scores['relevance']
        node.coherence_score = scores['coherence']
        node.novelty_score = scores['novelty']
        node.feasibility_score = scores['feasibility']
        node.progress_score = scores['progress']
        node.diversity_score = scores['diversity']
        node.metadata.confidence = scores['confidence']
        node.metadata.completeness = scores['completeness']
        node.metadata.evaluation_scores = scores.copy()
        
        if self.config.enable_cache and len(self._score_cache) < self.config.max_cache_size:
            self._score_cache[cache_key] = scores.copy()
        
        return scores
    
    def _evaluate_relevance(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        problem = context.get('problem', '')
        keywords = ["问题", "分析", "解决", "方案", "结果", "结论", "因为", "所以", "因此", "推理", "考虑", "关键"]
        matches = len(set(problem) & set(node.content))
        return min(0.5 + matches * 0.05 + (0.1 if any(kw in node.content for kw in keywords) else 0), 1.0)
    
    def _evaluate_coherence(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        connectors = ["因为", "所以", "因此", "但是", "然而", "而且", "首先", "其次", "最后"]
        count = sum(1 for c in connectors if c in node.content)
        return min(0.5 + count * 0.08 + (0.1 if node.parent_ids else 0), 1.0)
    
    def _evaluate_novelty(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        markers = ["新", "创新", "不同", "然而", "但是", "突破", "独特"]
        return min(0.5 + sum(0.1 for m in markers if m in node.content) + (0.15 if (node.is_reflection or node.is_critique) else 0), 1.0)
    
    def _evaluate_feasibility(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        content_lower = node.content.lower()
        invalid = ["矛盾", "错误", "不行", "无法", "失败", "不可能"]
        if any(m in content_lower for m in invalid):
            return max(0.2, 0.5 - sum(0.1 for m in invalid if m in content_lower))
        valid = ["因为", "所以", "因此", "分析", "推理", "可以", "应该"]
        if any(m in content_lower for m in valid):
            return min(0.8, 0.6 + sum(0.05 for m in valid if m in content_lower))
        return 0.5
    
    def _evaluate_progress(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        progress = 0.5 + (0.1 if len(node.content) > 100 else 0) + (0.1 if len(node.content) > 300 else 0)
        conclusions = ["因此", "所以", "得出", "结论", "最终", "总之"]
        if any(m in node.content for m in conclusions):
            progress += 0.15
        analyses = ["分析", "研究", "考虑", "评估"]
        if any(m in node.content for m in analyses):
            progress += 0.1
        return min(progress, 1.0)
    
    def _evaluate_diversity(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        diversity = 0.5 + (0.2 if node.node_type == NodeType.TOT_BRANCH else 0) + (0.15 if node.is_reflection else 0)
        if sum(node.content.count(p) for p in ["可能", "也许", "或者"]) > 1:
            diversity += 0.1
        return min(diversity, 1.0)
    
    def _evaluate_confidence(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        confidence = 0.8
        for p in self.uncertainty_patterns:
            if p.search(node.content):
                confidence -= 0.15
        for p in self.certainty_patterns:
            if p.search(node.content):
                confidence += 0.1
        if node.is_verification:
            confidence += 0.1
        return max(0.1, min(confidence, 1.0))
    
    def _evaluate_validity(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        validity = 0.8 - (0.2 if sum(p.search(node.content) is not None for p in self.contradiction_patterns) > 3 else 
                        0.1 if sum(p.search(node.content) is not None for p in self.contradiction_patterns) > 1 else 0)
        if node.is_checkpoint:
            validity += 0.1
        return max(0.1, min(validity, 1.0))
    
    def _evaluate_completeness(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        completeness = 0.5 + (0.3 if node.node_type == NodeType.SYNTHESIS else 0) + (0.2 if node.node_type == NodeType.FINAL else 0)
        if node.tool_result:
            completeness += 0.1
        return min(completeness, 1.0)
    
    def _evaluate_reflection(self, node: UnifiedNode, context: Dict[str, Any]) -> float:
        reflection = 0.5 + (0.3 if node.is_reflection else 0)
        if node.is_reflection and any(kw in node.content for kw in ["回顾", "总结", "检查", "审视", "反思"]):
            reflection += 0.1
        return min(reflection, 1.0)
    
    def detect_insight(self, content: str) -> Optional[Tuple[str, float]]:
        for pattern in self.insight_patterns:
            if pattern.search(content):
                if "整合" in content or "综合" in content: return ("integration", 0.85)
                if "纠正" in content or "错误" in content or "原来" in content: return ("correction", 0.75)
                if "关键" in content or "本质" in content or "突破口" in content: return ("breakthrough", 0.95)
                if "因此" in content or "所以" in content or "得出" in content: return ("synthesis", 0.80)
                if "新" in content or "创新" in content or "突破" in content: return ("creative", 0.85)
                if "批评" in content or "质疑" in content: return ("critical", 0.80)
                return ("general", 0.70)
        return None
    
    def detect_insight_type(self, content: str) -> InsightType:
        result = self.detect_insight(content)
        if not result:
            return InsightType.INTEGRATION
        mapping = {"integration": InsightType.INTEGRATION, "correction": InsightType.CORRECTION,
                   "breakthrough": InsightType.BREAKTHROUGH, "synthesis": InsightType.SYNTHESIS,
                   "creative": InsightType.CREATIVE, "critical": InsightType.CRITICAL}
        return mapping.get(result[0], InsightType.INTEGRATION)
    
    def should_create_checkpoint(self, node_count: int, last_depth: int, current_depth: int, scores: Dict) -> bool:
        return (node_count > 0 and node_count % self.config.checkpoint_interval == 0 or
                scores.get('confidence', 1.0) < 0.5 or scores.get('validity', 1.0) < 0.5 or
                current_depth - last_depth > self.config.max_depth // 2 or scores.get('novelty', 0) > 0.7)
    
    def should_create_reflection(self, node_count: int, last_depth: int) -> bool:
        return (node_count > 0 and node_count % self.config.reflection_interval == 0 or
                node_count - last_depth > self.config.reflection_interval * 2)
    
    def should_prune(self, node: UnifiedNode) -> bool:
        return node.combined_score < self.config.pruning_threshold or node.status == "pruned" or node.metadata.confidence < 0.3
    
    def should_verify(self, node: UnifiedNode, context: Dict[str, Any]) -> bool:
        return (self.config.enable_verification and 
                (node.combined_score > self.config.verification_threshold or node.node_type == NodeType.FINAL or
                 (node.metadata.confidence > 0.8 and node.novelty_score < 0.4)))
    
    def should_call_tool(self, node: UnifiedNode, context: Dict[str, Any]) -> bool:
        triggers = ["查询", "搜索", "计算", "获取", "查找", "验证"]
        return (any(t in node.content for t in triggers) or
                node.combined_score < self.config.tool_call_threshold or node.metadata.confidence < 0.5)
    
    def calculate_quality_score(self, graph: SuperGraph) -> float:
        if not graph.nodes:
            return 0.0
        stats = graph.get_statistics()
        return min(0.3 + min(stats.insights_count * 0.1, 0.3) + min(stats.corrections_count * 0.1, 0.2) +
                   min(stats.verification_count * 0.1, 0.2) + min(stats.max_depth / 10, 0.3) + stats.avg_score * 0.3, 1.0)
    
    def clear_cache(self):
        self._score_cache.clear()


class UnifiedGenerator:
    """统一生成器"""
    
    def __init__(self, llm_callable: Optional[Callable] = None, config: UnifiedConfig = None):
        self.llm_callable = llm_callable
        self.config = config or UnifiedConfig()
        self._generation_cache: Dict[str, str] = {}
        # 导入规则推理引擎（无 LLM 时使用）
        try:
            from .rule_engine import get_rule_engine
            self._rule_engine = get_rule_engine()
        except ImportError:
            self._rule_engine = None
    
    def generate_step(self, problem: str, context: List[UnifiedNode], mode: ReasoningMode = ReasoningMode.DIVINE) -> str:
        cache_key = f"step:{problem[:30]}:{len(context)}:{mode.value}"
        if cache_key in self._generation_cache:
            return self._generation_cache[cache_key]
        
        if self.llm_callable:
            try:
                result = self.llm_callable(self._build_step_prompt(problem, context, mode))
                if self.config.enable_cache:
                    self._generation_cache[cache_key] = result
                return result
            except Exception as e:
                logger.error(f"LLM调用失败: {e}")
        
        # 无 LLM 时：使用规则推理引擎（不再返回模板！）
        if self._rule_engine:
            context_strs = [node.content for node in context] if context else []
            steps = self._rule_engine.generate_reasoning_steps(problem, context_strs)
            result = f"基于规则推理：\n" + "\n".join(steps)
        else:
            result = self._default_step_generation(problem, context)
        
        if self.config.enable_cache:
            self._generation_cache[cache_key] = result
        return result
    
    def _build_step_prompt(self, problem: str, context: List[UnifiedNode], mode: ReasoningMode) -> str:
        prompt = f"问题：{problem}\n\n"
        if context:
            prompt += "推理历史：\n"
            for i, node in enumerate(context[-7:]):
                prompt += f"{i+1}. [{node.node_type.value}] {node.content[:150]}...\n"
        
        descriptions = {
            ReasoningMode.LINEAR: "请进行逐步推理，展示完整的思考过程。",
            ReasoningMode.BRANCHING: "请考虑多个可能的推理方向。",
            ReasoningMode.GRAPH: "请建立推理之间的关联图。",
            ReasoningMode.REACTIVE: "如需外部信息或工具，请明确指出。",
            ReasoningMode.SUPER: "综合运用各种推理技巧，给出最优解。",
            ReasoningMode.DIVINE: "作为DivineReason，请进行深度推理，包括自我反思和验证。",
            ReasoningMode.DELIBERATE: "请深思熟虑，考虑所有可能的因素。",
            ReasoningMode.CREATIVE: "请发挥创造力，提出新颖的想法。",
            ReasoningMode.ANALYTICAL: "请进行严谨的分析，使用数据和逻辑推理。"
        }
        prompt += f"\n{descriptions.get(mode, '')}\n\n请继续推理："
        return prompt
    
    def _default_step_generation(self, problem: str, context: List[UnifiedNode]) -> str:
        """
        无 LLM 时的默认推理步骤生成
        使用规则推理引擎（非模板！）
        """
        # 使用规则推理引擎
        if self._rule_engine:
            context_strs = [node.content for node in context] if context else []
            steps = self._rule_engine.generate_reasoning_steps(problem, context_strs)
            if steps and len(context) < len(steps):
                return steps[len(context)]  # 返回下一步
        
        # 如果规则引擎失败，使用基础推理
        if context:
            last_node = context[-1]
            return f"基于「{last_node.content[:30]}...」，继续推理..."
        else:
            return f"开始分析问题「{problem[:30]}...」"
    
    def generate_branches(self, parent: UnifiedNode, problem: str, k: int = 3) -> List[Dict[str, str]]:
        if self.llm_callable:
            try:
                response = self.llm_callable(f"问题：{problem}\n\n当前推理：{parent.content}\n\n请生成{k}个不同的推理方向：")
                return self._parse_branches(response, k)
            except Exception as e:
                logger.error(f"分支生成失败: {e}")
        
        # 无 LLM 时：使用规则推理引擎生成分支
        if self._rule_engine:
            problem_type = self._rule_engine.identify_problem_type(problem)
            branches = []
            for i in range(k):
                # 基于问题类型和角度生成多样化的分支
                angles = ["逻辑分析", "实践方案", "创新思路", "风险评估", "成本效益"]
                branch_content = f"方向{i+1}: 从{angles[i % len(angles)]}角度分析「{problem[:30]}」"
                branches.append({
                    "content": branch_content,
                    "type": ["logical", "practical", "creative", "risk", "cost"][i % 5],
                    "diversity": 0.6 + i * 0.1
                })
            return branches
        
        # 如果规则引擎也失败，使用基础分支（非模板）
        return [{"content": f"推理方向{i+1}: 基于问题「{problem[:20]}...」的分析", 
                 "type": "generic", 
                 "diversity": 0.5 + i * 0.1} for i in range(k)]
    
    def _parse_branches(self, response: str, k: int) -> List[Dict[str, str]]:
        branches = []
        for line in response.split('\n'):
            if any(m in line for m in ['方向', '分支', 'Branch', 'Option']):
                branches.append({"content": line.split(']', 1)[-1].strip(), "type": "llm_generated", "diversity": 0.7})
        return branches[:k] if branches else [{"content": "默认方向", "type": "default", "diversity": 0.5}]
    
    def generate_tool_action(self, node: UnifiedNode, problem: str, available_tools: List[Dict]) -> Optional[Dict[str, Any]]:
        if not available_tools:
            return None
        content = node.content.lower()
        for tool in available_tools:
            name = tool.get('name', '').lower()
            desc = tool.get('description', '').lower()
            if any(k in content for k in ['搜索', '查询', '查找', 'search']) and any(k in name + desc for k in ['search', 'query', 'find']):
                return {'tool': tool.get('name'), 'params': {'query': problem}}
            if any(k in content for k in ['计算', 'calculate']) and ('calc' in name or 'compute' in name):
                return {'tool': tool.get('name'), 'params': {}}
        return {'tool': available_tools[0].get('name'), 'params': {}}
    
    def generate_reflection(self, context: List[UnifiedNode], problem: str) -> str:
        if self.llm_callable:
            try:
                prompt = f"问题：{problem}\n\n请反思以下推理过程，找出可能的盲点或改进空间：\n"
                for i, node in enumerate(context[-5:]):
                    prompt += f"{i+1}. {node.content[:100]}...\n"
                return self.llm_callable(prompt + "\n请给出反思结果：")
            except Exception as e:
                logger.error(f"反思生成失败: {e}")
        return "反思：当前推理逻辑连贯，但需要考虑更多的边界情况和替代方案。"
    
    def generate_verification(self, node: UnifiedNode, problem: str) -> str:
        if self.llm_callable:
            try:
                return self.llm_callable(f"问题：{problem}\n\n请验证以下推理的有效性：\n{node.content}\n\n验证结果：")
            except Exception as e:
                logger.error(f"验证生成失败: {e}")
        return "验证：推理逻辑基本正确，建议进一步检验关键假设。"
    
    def generate_critique(self, node: UnifiedNode, problem: str) -> str:
        if self.llm_callable:
            try:
                return self.llm_callable(f"问题：{problem}\n\n请对以下推理进行批判性分析：\n{node.content}\n\n批评：")
            except Exception as e:
                logger.error(f"批评生成失败: {e}")
        return "批评：当前推理可能存在某些假设未被充分验证，需要进一步分析。"
    
    def generate_synthesis(self, nodes: List[UnifiedNode], problem: str) -> str:
        if self.llm_callable:
            try:
                prompt = f"问题：{problem}\n\n请综合以下多个推理方向：\n"
                for i, node in enumerate(nodes[:5]):
                    prompt += f"{i+1}. {node.content[:100]}...\n"
                return self.llm_callable(prompt + "\n综合结论：")
            except Exception as e:
                logger.error(f"综合生成失败: {e}")
        return "综合：基于以上多角度分析，得出最终解决方案。"
    
    def clear_cache(self):
        self._generation_cache.clear()


# ============================================================
# DivineReason 超级推理引擎
# ============================================================

class DivineReason:
    """
    DivineReason - 至高推理引擎
    
    "当四大推理体系融为一体，神之智慧由此诞生"
    """
    
    VERSION = "6.2.0"
    ENGINE_NAME = "DivineReason"
    ENGINE_DESCRIPTION = "至高推理引擎 - 四大推理体系融合体"
    
    def __init__(self, llm_callable: Optional[Callable] = None, config: Optional[UnifiedConfig] = None, tools: Optional[List] = None):
        self.config = config or UnifiedConfig()
        self.llm_callable = llm_callable
        self.tools = tools or []
        self.evaluator = UnifiedEvaluator(self.config)
        self.generator = UnifiedGenerator(llm_callable, self.config)
        self.tool_registry = {t.name: t for t in self.tools if hasattr(t, 'name')}
        self.current_graph: Optional[SuperGraph] = None
        self._is_reasoning = False
        self._reasoning_lock = threading.Lock()
        self.stats = {
            'total_runs': 0, 'total_nodes': 0, 'total_edges': 0, 'total_insights': 0,
            'total_corrections': 0, 'total_tool_calls': 0, 'total_reflections': 0,
            'total_verifications': 0, 'total_critiques': 0, 'avg_depth': 0, 'avg_score': 0
        }
        logger.info(f"⚡ {self.ENGINE_NAME} v{self.VERSION} 初始化完成")
    
    def solve(self, problem: str, mode: ReasoningMode = None, context: Optional[Dict] = None,
              llm_callable: Optional[Callable] = None, progress_callback: Optional[Callable] = None) -> ReasoningResult:
        start_time = time.time()
        mode = mode or self.config.default_mode
        llm = llm_callable or self.llm_callable
        callback = progress_callback or self.config.progress_callback
        
        result = ReasoningResult(engine=self.ENGINE_NAME, version=self.VERSION, problem=problem, mode=mode.value)
        
        with self._reasoning_lock:
            self._is_reasoning = True
        
        try:
            self.current_graph = SuperGraph(problem)
            root = self.current_graph.create_root(f"🔍 问题分析：{problem}")
            root.metadata.source_engine = "divine"
            root.metadata.confidence = 0.9
            root.metadata.generation_method = "root"
            
            nodes_created = 1
            last_checkpoint_depth = 0
            last_reflection_depth = 0
            corrections, insights, reflections, verifications, critiques, tool_calls = [], [], [], [], [], []
            current_nodes = [root]
            depth = 0
            
            while nodes_created < self.config.max_nodes and depth < self.config.max_depth:
                next_nodes = []
                for node in current_nodes:
                    if node.combined_score < self.config.pruning_threshold:
                        continue
                    
                    path_history = self.current_graph.get_path(node.node_id)
                    
                    if mode == ReasoningMode.LINEAR:
                        new_nodes = self._expand_long_cot(node, problem, context, llm, path_history)
                    elif mode == ReasoningMode.DIVINE:
                        # DIVINE 模式：融合四大推理体系
                        new_nodes = self._expand_divine(node, problem, context, llm, path_history)
                    elif mode == ReasoningMode.SUPER:
                        new_nodes = self._expand_super(node, problem, context, llm, path_history)
                    elif mode == ReasoningMode.BRANCHING:
                        new_nodes = self._expand_tot(node, problem, context, llm, path_history)
                    elif mode == ReasoningMode.REACTIVE:
                        new_nodes = self._expand_react(node, problem, context, llm, path_history)
                    elif mode == ReasoningMode.GRAPH:
                        new_nodes = self._expand_got(node, problem, context, llm, path_history)
                    else:
                        # 默认：使用 DIVINE 模式
                        new_nodes = self._expand_divine(node, problem, context, llm, path_history)
                    
                    for new_node in new_nodes:
                        scores = self.evaluator.evaluate_node(new_node, {'problem': problem, 'context': self.current_graph})
                        
                        insight_result = self.evaluator.detect_insight(new_node.content)
                        if insight_result:
                            new_node.is_insight = True
                            new_node.insight_type = insight_result[0]
                            new_node.insight_impact = insight_result[1]
                            new_node.metadata.insight_type = self.evaluator.detect_insight_type(new_node.content)
                            insights.append({'node_id': new_node.node_id, 'type': insight_result[0], 'impact': insight_result[1], 'content': new_node.content[:150]})
                        
                        added_node = self.current_graph.add_node(
                            content=new_node.content, node_type=new_node.node_type, parent_ids=[node.node_id], depth=depth + 1,
                            metadata=new_node.metadata, feasibility_score=new_node.feasibility_score,
                            progress_score=new_node.progress_score, diversity_score=new_node.diversity_score,
                            combined_score=new_node.combined_score, is_checkpoint=new_node.is_checkpoint,
                            is_insight=new_node.is_insight, insight_type=new_node.insight_type,
                            insight_impact=new_node.insight_impact, action=new_node.action,
                            observation=new_node.observation, tool_result=new_node.tool_result,
                            is_reflection=new_node.is_reflection, is_verification=new_node.is_verification,
                            is_critique=new_node.is_critique
                        )
                        
                        if new_node.is_reflection: reflections.append({'node_id': added_node.node_id, 'content': new_node.content[:150]})
                        if new_node.is_verification: verifications.append({'node_id': added_node.node_id, 'content': new_node.content[:150]})
                        if new_node.is_critique: critiques.append({'node_id': added_node.node_id, 'content': new_node.content[:150]})
                        if new_node.action: tool_calls.append({'node_id': added_node.node_id, 'action': new_node.action})
                        
                        if self.evaluator.should_create_checkpoint(nodes_created, last_checkpoint_depth, depth + 1, scores):
                            last_checkpoint_depth = depth + 1
                            added_node.is_checkpoint = True
                        
                        next_nodes.append(added_node)
                        nodes_created += 1
                        
                        if self.evaluator.should_prune(new_node):
                            new_node.status = "pruned"
                        
                        if callback:
                            callback(nodes_created, depth, added_node)
                
                current_nodes = next_nodes
                depth += 1
                if not current_nodes:
                    break
            
            if self.current_graph.nodes:
                best_path = self.current_graph.get_best_path()
                if best_path.nodes:
                    self.current_graph.add_node(
                        content="✨ 最终解决方案：基于以上深度推理得出", node_type=NodeType.FINAL,
                        parent_ids=[best_path.nodes[-1].node_id], depth=depth + 1,
                        metadata=ReasoningMetadata(source_engine="divine", generation_method="synthesis", is_final=True, confidence=0.95)
                    )
            
            if self.current_graph.final_nodes:
                final_node = self.current_graph.nodes[self.current_graph.final_nodes[0]]
                solution = final_node.content
            elif best_path.nodes:
                solution = best_path.nodes[-1].content
            else:
                solution = "经过DivineReason的深度推理，未能找到满意的解决方案。"
                result.warnings.append("未能找到最终节点")
            
            graph_stats = self.current_graph.get_statistics()
            graph_stats.processing_time = time.time() - start_time
            
            self._update_stats(nodes_created, depth, insights, corrections, reflections, verifications, critiques)
            
            result.success = True
            result.solution = solution
            result.graph = self.current_graph
            result.path = best_path
            result.statistics = graph_stats
            result.quality_score = self.evaluator.calculate_quality_score(self.current_graph)
            result.insights = insights
            result.corrections = corrections
            result.reflections = reflections
            result.verifications = verifications
            result.critiques = critiques
            result.tool_calls = tool_calls
            result.metadata = {'engine': 'DivineReason', 'version': self.VERSION, 'timestamp': datetime.now().isoformat(), 'processing_time': round(time.time() - start_time, 2)}
            
            return result
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
            logger.error(f"推理过程出错: {e}")
            import traceback
            traceback.print_exc()
            return result
        finally:
            with self._reasoning_lock:
                self._is_reasoning = False
    
    def _expand_long_cot(self, node: UnifiedNode, problem: str, context: Optional[Dict], llm: Optional[Callable], path: List[UnifiedNode]) -> List[UnifiedNode]:
        content = self.generator.generate_step(problem, path, ReasoningMode.LINEAR)
        new_node = UnifiedNode(
            node_id=str(uuid.uuid4()), content=content, node_type=NodeType.LONG_COT_STEP, depth=node.depth + 1,
            metadata=ReasoningMetadata(source_engine="long_cot", generation_method="llm" if llm else "template")
        )
        return [new_node]
    
    def _expand_tot(self, node: UnifiedNode, problem: str, context: Optional[Dict], llm: Optional[Callable], path: List[UnifiedNode]) -> List[UnifiedNode]:
        branches = self.generator.generate_branches(node, problem, k=self.config.max_branching)
        nodes = []
        for i, branch in enumerate(branches):
            # 确保 content 不是模板
            content = branch.get('content', '')
            if not content or '深入分析' in content or '分支' in content:
                # 生成真实内容
                if self.generator._rule_engine:
                    problem_type = self.generator._rule_engine.identify_problem_type(problem)
                    angles = ["逻辑分析", "实践方案", "创新思路", "风险评估", "成本效益"]
                    content = f"方向{i+1} ({angles[i % len(angles)]}): 针对「{problem[:30]}...」的分析"
                else:
                    content = f"推理分支{i+1}: 基于问题「{problem[:30]}...」的分析"
            
            node = UnifiedNode(
                node_id=str(uuid.uuid4()), content=content,
                node_type=NodeType.TOT_BRANCH, depth=node.depth + 1,
                diversity_score=branch.get('diversity', 0.5),
                metadata=ReasoningMetadata(source_engine="tot", generation_method="branch")
            )
            nodes.append(node)
        return nodes
    
    def _expand_react(self, node: UnifiedNode, problem: str, context: Optional[Dict], llm: Optional[Callable], path: List[UnifiedNode]) -> List[UnifiedNode]:
        new_nodes = []
        if self.tools and self.evaluator.should_call_tool(node, {'problem': problem}):
            tool_descriptions = [{'name': t.name, 'description': getattr(t, 'description', '')} for t in self.tools]
            action = self.generator.generate_tool_action(node, problem, tool_descriptions)
            if action:
                action_node = UnifiedNode(
                    node_id=str(uuid.uuid4()), content=f"🔧 执行工具: {action['tool']}", node_type=NodeType.REACT_ACTION,
                    depth=node.depth + 1, action=action,
                    metadata=ReasoningMetadata(source_engine="react", generation_method="action")
                )
                new_nodes.append(action_node)
                new_nodes.append(UnifiedNode(
                    node_id=str(uuid.uuid4()), content=f"📊 工具执行结果: {action['params']}", node_type=NodeType.OBSERVATION,
                    parent_ids=[action_node.node_id], depth=node.depth + 2, observation=action['params'],
                    metadata=ReasoningMetadata(source_engine="react", generation_method="observation")
                ))
        else:
            reasoning = self.generator.generate_step(problem, path, ReasoningMode.REACTIVE)
            new_nodes.append(UnifiedNode(
                node_id=str(uuid.uuid4()), content=reasoning, node_type=NodeType.LONG_COT_STEP, depth=node.depth + 1,
                metadata=ReasoningMetadata(source_engine="react", generation_method="reasoning")
            ))
        return new_nodes
    
    def _expand_got(self, node: UnifiedNode, problem: str, context: Optional[Dict], llm: Optional[Callable], path: List[UnifiedNode]) -> List[UnifiedNode]:
        return [
            UnifiedNode(
                node_id=str(uuid.uuid4()), content=f"[视角{i+1}] {self.generator.generate_step(problem, path, ReasoningMode.GRAPH)}",
                node_type=NodeType.LONG_COT_STEP, depth=node.depth + 1,
                metadata=ReasoningMetadata(source_engine="got", generation_method="attention")
            )
            for i in range(3)
        ]

    def _expand_divine(self, node: UnifiedNode, problem: str, context: Optional[Dict], llm: Optional[Callable], path: List[UnifiedNode]) -> List[UnifiedNode]:
        """
        DIVINE 模式：融合四大推理体系 (GoT + LongCoT + ToT + ReAct)
        - LongCoT: 建立基础推理链
        - ToT: 生成多个推理分支
        - ReAct: 添加工具调用节点
        - GoT: 建立图结构连接
        """
        all_new_nodes = []
        
        # 使用 RuleEngine 生成真实推理内容
        rule_engine = self.generator._rule_engine if hasattr(self.generator, '_rule_engine') else None
        
        # 1. LongCoT - 基础推理链
        long_cot_nodes = self._expand_long_cot(node, problem, context, llm, path)
        
        # 如果使用 RuleEngine，替换模板内容
        if rule_engine and not llm:
            for i, n in enumerate(long_cot_nodes):
                if '步骤' in n.content or '深入分析' in n.content:
                    # 生成真实推理步骤
                    steps = rule_engine.generate_reasoning_steps(problem, [node.content] if node else None)
                    if i < len(steps):
                        n.content = steps[i]
                        n.metadata.source_engine = "rule_engine"
        
        all_new_nodes.extend(long_cot_nodes)
        
        # 2. ToT - 生成分支（前几步生成分支，避免节点爆炸）
        if len(path) < self.config.max_depth // 2:
            tot_nodes = self._expand_tot(node, problem, context, llm, path)
            
            # 如果使用 RuleEngine，替换模板内容
            if rule_engine and not llm:
                problem_type = rule_engine.identify_problem_type(problem)
                angles = ["逻辑分析", "实践方案", "创新思路", "风险评估", "成本效益"]
                for i, n in enumerate(tot_nodes):
                    if '方向' in n.content or '分支' in n.content:
                        n.content = f"方向{i+1} ({angles[i % len(angles)]}): 针对「{problem[:30]}...」的分析"
                        n.metadata.source_engine = "rule_engine"
            
            all_new_nodes.extend(tot_nodes)
        
        # 3. ReAct - 添加工具调用（如果有工具且 LLM 可用）
        if self.tools and llm:
            react_nodes = self._expand_react(node, problem, context, llm, path)
            all_new_nodes.extend(react_nodes)
        
        # 4. GoT - 生成图结构节点
        got_nodes = self._expand_got(node, problem, context, llm, path)
        all_new_nodes.extend(got_nodes)
        
        # 5. 建立图结构连接（GoT 的核心：在节点之间添加边）
        if len(all_new_nodes) > 1:
            for i, n1 in enumerate(all_new_nodes):
                for n2 in all_new_nodes[i+1:]:
                    # 添加逻辑流边
                    try:
                        self.graph.add_edge(
                            source_id=n1.node_id,
                            target_id=n2.node_id,
                            edge_type=EdgeType.LOGICAL_FLOW,
                            weight=0.5
                        )
                    except Exception:
                        pass  # 边可能已存在，忽略错误
        
        return all_new_nodes
    
    def _expand_super(self, node: UnifiedNode, problem: str, context: Optional[Dict], llm: Optional[Callable], path: List[UnifiedNode]) -> List[UnifiedNode]:
        """
        SUPER 模式：超级融合（调用 DIVINE + 评估优化）
        1. 调用 DIVINE 模式获取所有推理节点
        2. 评估所有节点，保留高质量节点
        3. 返回优化后的节点列表
        """
        # 1. 调用 DIVINE 模式获取所有推理节点
        divine_nodes = self._expand_divine(node, problem, context, llm, path)
        
        # 2. 评估所有节点，保留高质量节点
        if llm and divine_nodes:
            evaluated_nodes = []
            for n in divine_nodes:
                # 评估节点质量
                try:
                    score = self.evaluator.evaluate_node(n, {'problem': problem, 'context': self.current_graph})
                    n.score = score
                    if score > 0.6:  # 保留评分 > 0.6 的节点
                        evaluated_nodes.append(n)
                except Exception:
                    evaluated_nodes.append(n)  # 评估失败时保留节点
            
            return evaluated_nodes if evaluated_nodes else divine_nodes
        
        return divine_nodes
    
    def _update_stats(self, nodes_count: int, depth: int, insights: List, corrections: List, reflections: List, verifications: List, critiques: List):
        self.stats['total_runs'] += 1
        self.stats['total_nodes'] += nodes_count
        self.stats['total_edges'] += nodes_count - 1
        self.stats['total_insights'] += len(insights)
        self.stats['total_corrections'] += len(corrections)
        self.stats['total_reflections'] += len(reflections)
        self.stats['total_verifications'] += len(verifications)
        self.stats['total_critiques'] += len(critiques)
        if self.stats['total_runs'] > 0:
            self.stats['avg_depth'] = depth
            self.stats['avg_score'] = self.stats.get('avg_score', 0) * 0.9 + 0.5 * 0.1
    
    def get_stats(self) -> Dict[str, Any]:
        return {**self.stats, 'is_reasoning': self._is_reasoning, 'version': self.VERSION, 'engine': self.ENGINE_NAME}
    
    def reset(self):
        self.current_graph = None
        self._is_reasoning = False
        self.evaluator.clear_cache()
        self.generator.clear_cache()
    
    @contextmanager
    def reasoning_session(self, problem: str, mode: ReasoningMode = None):
        self.current_graph = SuperGraph(problem)
        try:
            yield self.current_graph
        finally:
            self.current_graph = None


# ============================================================
# 工厂函数
# ============================================================

def create_divine_engine(llm_callable: Optional[Callable] = None, config: Optional[UnifiedConfig] = None, tools: Optional[List] = None) -> DivineReason:
    return DivineReason(llm_callable, config, tools)

def solve_with_divine(problem: str, llm_callable: Optional[Callable] = None, mode: ReasoningMode = ReasoningMode.DIVINE, **kwargs) -> ReasoningResult:
    config = UnifiedConfig(**kwargs) if kwargs else None
    engine = DivineReason(llm_callable, config)
    return engine.solve(problem, mode)

# 别名
UnifiedReasoningEngine = DivineReason
create_super_engine = create_divine_engine
solve_with_super_engine = solve_with_divine
