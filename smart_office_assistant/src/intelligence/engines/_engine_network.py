# -*- coding: utf-8 -*-
"""
DivineReason 引擎网络化部署系统 V1.0
====================================

将100+推理引擎部署为 DivineReason 的节点，实现全局调用和网络化应用。

架构：
┌─────────────────────────────────────────────────────────────────────────┐
│                      DivineReason 网络化引擎                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   EngineNetwork (引擎网络)                        │   │
│  │  ┌─────────────────────────────────────────────────────────────┐ │   │
│  │  │                 EngineRegistry (引擎注册表)                  │ │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │ │   │
│  │  │  │哲学引擎  │ │军事引擎  │ │心理引擎  │ │管理引擎  │ ...   │ │   │
│  │  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │ │   │
│  │  └───────┼────────────┼────────────┼────────────┘              │ │   │
│  └──────────┼────────────┼────────────┼───────────────────────────┘ │   │
│             ▼            ▼            ▼                              │   │
│  ┌─────────────────────────────────────────────────────────────┐     │   │
│  │                 EngineRouter (智能路由器)                    │     │   │
│  └─────────────────────────────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                 DivineReason (超级推理引擎)                       │   │
│  │  引擎作为节点，通过边连接，支持并行/串行/投票等多种融合模式        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

版本: V1.0.0
创建: 2026-04-28
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import hashlib
import time
import uuid

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════════════════════════

class EngineCategory(Enum):
    """引擎分类"""
    PHILOSOPHY = "philosophy"
    MILITARY = "military"
    PSYCHOLOGY = "psychology"
    MANAGEMENT = "management"
    ECONOMICS = "economics"
    LITERATURE = "literature"
    SCIENCE = "science"
    HISTORY = "history"
    POLITICS = "politics"
    RELIGION = "religion"
    MATH = "math"
    NEURO = "neuro"
    CULTURE = "culture"
    CROSS_CULTURE = "cross_culture"
    COMPOSITE = "composite"
    REASONING = "reasoning"
    LEARNING = "learning"
    MEMORY = "memory"
    CLONING = "cloning"
    COORDINATOR = "coordinator"
    FUSION = "fusion"
    ANALYZER = "analyzer"


class EngineStatus(Enum):
    """引擎状态"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    DISABLED = "disabled"
    WARMING = "warming"


class FusionStrategy(Enum):
    """融合策略"""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    VOTING = "voting"
    WEIGHTED = "weighted"
    CHAIN = "chain"
    HIERARCHICAL = "hierarchical"


class InvocationMode(Enum):
    """调用模式"""
    SINGLE = "single"
    MULTIPLE = "multiple"
    CHAIN = "chain"
    CONDITIONAL = "conditional"


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class EngineMetadata:
    """引擎元数据"""
    engine_id: str
    name: str
    display_name: str
    description: str
    category: EngineCategory
    subcategory: str = ""
    file_path: str = ""
    capabilities: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    input_types: List[str] = field(default_factory=list)
    output_types: List[str] = field(default_factory=list)
    quality_score: float = 0.5
    reliability: float = 0.8
    latency_ms: float = 100.0
    status: EngineStatus = EngineStatus.IDLE
    invocations: int = 0
    failures: int = 0
    last_used: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    synergies: Dict[str, float] = field(default_factory=dict)
    weight: float = 1.0
    category_weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'engine_id': self.engine_id,
            'name': self.name,
            'display_name': self.display_name,
            'category': self.category.value,
            'quality_score': round(self.quality_score, 3),
            'reliability': round(self.reliability, 3),
            'status': self.status.value,
            'invocations': self.invocations,
            'weight': round(self.weight, 3)
        }


@dataclass
class EngineResult:
    """引擎执行结果"""
    engine_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    confidence: float = 0.0
    quality_score: float = 0.0
    relevance: float = 0.0
    latency_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)
    reasoning_trace: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EngineNode:
    """引擎节点"""
    node_id: str
    metadata: EngineMetadata
    content: str = ""
    depth: int = 0
    combined_score: float = 0.0
    executor: Optional[Callable] = None
    preprocessor: Optional[Callable] = None
    postprocessor: Optional[Callable] = None
    is_active: bool = True
    divine_node_id: Optional[str] = None
    cache: Dict[str, EngineResult] = field(default_factory=dict)

    def execute(self, input_data: Any, **kwargs) -> EngineResult:
        """执行引擎"""
        cache_key = self._generate_cache_key(input_data)
        
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            logger.debug(f"Engine {self.metadata.name} cache hit")
            return cached
        
        self.metadata.status = EngineStatus.BUSY
        self.metadata.invocations += 1
        
        start_time = time.time()
        try:
            processed_input = input_data
            if self.preprocessor:
                processed_input = self.preprocessor(input_data)
            
            if self.executor:
                output = self.executor(processed_input, **kwargs)
            else:
                output = processed_input
            
            if self.postprocessor:
                output = self.postprocessor(output)
            
            result = EngineResult(
                engine_id=self.metadata.engine_id,
                success=True,
                output=output,
                confidence=kwargs.get('confidence', 0.8),
                quality_score=self.metadata.quality_score,
                relevance=kwargs.get('relevance', 0.8),
                latency_ms=(time.time() - start_time) * 1000
            )
            
            self.metadata.status = EngineStatus.IDLE
            self.metadata.last_used = time.time()
            
        except Exception as e:
            self.metadata.status = EngineStatus.ERROR
            self.metadata.failures += 1
            logger.error(f"Engine {self.metadata.name} failed: {e}")
            
            result = EngineResult(
                engine_id=self.metadata.engine_id,
                success=False,
                error=str(e),
                latency_ms=(time.time() - start_time) * 1000
            )
        
        self.cache[cache_key] = result
        return result
    
    def _generate_cache_key(self, input_data: Any) -> str:
        data_str = str(input_data)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'engine_id': self.metadata.engine_id,
            'name': self.metadata.name,
            'category': self.metadata.category.value,
            'is_active': self.is_active,
            'status': self.metadata.status.value,
            'quality_score': round(self.metadata.quality_score, 3),
            'invocations': self.metadata.invocations
        }


@dataclass
class EngineFusionResult:
    """引擎融合结果"""
    success: bool
    strategy: FusionStrategy
    output: Any = None
    error: Optional[str] = None
    engines_used: List[str] = field(default_factory=list)
    individual_results: List[EngineResult] = field(default_factory=list)
    fused_confidence: float = 0.0
    fused_quality: float = 0.0
    agreement_score: float = 0.0
    total_latency_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass 
class NetworkConfig:
    """网络配置"""
    max_parallel_engines: int = 5
    max_chain_length: int = 10
    timeout_ms: float = 5000.0
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600
    max_cache_size: int = 1000
    default_fusion_strategy: FusionStrategy = FusionStrategy.WEIGHTED
    min_agreement_score: float = 0.5
    enable_smart_routing: bool = True
    routing_method: str = "hybrid"
    min_engine_confidence: float = 0.3
    min_quality_threshold: float = 0.4
    enable_monitoring: bool = True
    log_level: str = "INFO"


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎注册表
# ═══════════════════════════════════════════════════════════════════════════════

class EngineRegistry:
    """引擎注册表"""
    
    def __init__(self):
        self._engines: Dict[str, EngineMetadata] = {}
        self._nodes: Dict[str, EngineNode] = {}
        self._category_index: Dict[EngineCategory, List[str]] = defaultdict(list)
        self._keyword_index: Dict[str, List[str]] = defaultdict(list)
        self._name_index: Dict[str, str] = {}
        self._total_invocations = 0
        logger.info("EngineRegistry initialized")
    
    def register_engine(self, metadata: EngineMetadata, 
                       executor: Optional[Callable] = None,
                       preprocessor: Optional[Callable] = None,
                       postprocessor: Optional[Callable] = None) -> EngineNode:
        """注册引擎"""
        node = EngineNode(
            node_id=f"engine_{metadata.engine_id}",
            metadata=metadata,
            executor=executor,
            preprocessor=preprocessor,
            postprocessor=postprocessor,
            content=f"{metadata.name}: {metadata.description}"
        )
        
        self._engines[metadata.engine_id] = metadata
        self._nodes[node.node_id] = node
        self._name_index[metadata.name.lower()] = metadata.engine_id
        self._category_index[metadata.category].append(metadata.engine_id)
        for keyword in metadata.triggers:
            self._keyword_index[keyword.lower()].append(metadata.engine_id)
        
        logger.info(f"Registered engine: {metadata.name} ({metadata.engine_id})")
        return node
    
    def unregister_engine(self, engine_id: str) -> bool:
        """注销引擎"""
        if engine_id not in self._engines:
            return False
        
        metadata = self._engines[engine_id]
        self._category_index[metadata.category].remove(engine_id)
        for keyword in metadata.triggers:
            if engine_id in self._keyword_index[keyword.lower()]:
                self._keyword_index[keyword.lower()].remove(engine_id)
        
        del self._name_index[metadata.name.lower()]
        del self._engines[engine_id]
        
        node_id = f"engine_{engine_id}"
        if node_id in self._nodes:
            del self._nodes[node_id]
        
        logger.info(f"Unregistered engine: {metadata.name}")
        return True
    
    def get_engine(self, engine_id: str) -> Optional[EngineNode]:
        """获取引擎节点"""
        node_id = f"engine_{engine_id}"
        return self._nodes.get(node_id)
    
    def get_by_name(self, name: str) -> Optional[EngineNode]:
        """通过名称获取引擎"""
        engine_id = self._name_index.get(name.lower())
        if engine_id:
            return self.get_engine(engine_id)
        return None
    
    def get_by_category(self, category: EngineCategory) -> List[EngineNode]:
        """获取指定分类的所有引擎"""
        engine_ids = self._category_index.get(category, [])
        return [self.get_engine(eid) for eid in engine_ids if self.get_engine(eid)]
    
    def find_by_keywords(self, keywords: List[str]) -> List[EngineNode]:
        """通过关键词查找引擎"""
        engine_ids = set()
        for keyword in keywords:
            engine_ids.update(self._keyword_index.get(keyword.lower(), []))
        return [self.get_engine(eid) for eid in engine_ids if self.get_engine(eid)]
    
    def find_similar(self, query: str, top_k: int = 5) -> List[Tuple[EngineNode, float]]:
        """查找相似引擎"""
        scores = defaultdict(float)
        query_words = set(query.lower().split())
        
        for engine_id, metadata in self._engines.items():
            keyword_matches = sum(1 for w in query_words if w in metadata.description.lower())
            trigger_matches = sum(1 for t in metadata.triggers if t.lower() in query.lower())
            total_score = keyword_matches * 0.3 + trigger_matches * 0.7
            if total_score > 0:
                scores[engine_id] = total_score
        
        sorted_engines = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        return [(self.get_engine(eid), score) for eid, score in sorted_engines if self.get_engine(eid)]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self._engines)
        by_category = {cat.value: len(engines) for cat, engines in self._category_index.items()}
        total_invocations = sum(e.invocations for e in self._engines.values())
        total_failures = sum(e.failures for e in self._engines.values())
        
        return {
            'total_engines': total,
            'by_category': by_category,
            'total_invocations': total_invocations,
            'total_failures': total_failures,
            'success_rate': (total_invocations - total_failures) / max(total_invocations, 1)
        }
    
    def list_all(self) -> List[EngineMetadata]:
        """列出所有引擎元数据"""
        return list(self._engines.values())
    
    def get_active_count(self) -> int:
        """获取活跃引擎数量"""
        return sum(1 for n in self._nodes.values() if n.is_active)


# ═══════════════════════════════════════════════════════════════════════════════
# 智能路由器
# ═══════════════════════════════════════════════════════════════════════════════

class EngineRouter:
    """智能路由器"""
    
    def __init__(self, registry: EngineRegistry, config: Optional[NetworkConfig] = None):
        self.registry = registry
        self.config = config or NetworkConfig()
        
        self._problem_type_mapping: Dict[str, List[EngineCategory]] = {
            'strategy': [EngineCategory.MILITARY, EngineCategory.MANAGEMENT, EngineCategory.POLITICS],
            'decision': [EngineCategory.MANAGEMENT, EngineCategory.ECONOMICS, EngineCategory.PHILOSOPHY],
            'emotion': [EngineCategory.PSYCHOLOGY, EngineCategory.NEURO],
            'creativity': [EngineCategory.LITERATURE, EngineCategory.PHILOSOPHY],
            'analysis': [EngineCategory.SCIENCE, EngineCategory.ECONOMICS, EngineCategory.HISTORY],
            'learning': [EngineCategory.LEARNING, EngineCategory.NEURO, EngineCategory.PSYCHOLOGY],
            'conflict': [EngineCategory.MILITARY, EngineCategory.PSYCHOLOGY, EngineCategory.POLITICS],
            'relationship': [EngineCategory.PSYCHOLOGY, EngineCategory.CULTURE],
            'planning': [EngineCategory.MANAGEMENT, EngineCategory.MILITARY, EngineCategory.PHILOSOPHY],
            'optimization': [EngineCategory.MATH, EngineCategory.ECONOMICS, EngineCategory.MANAGEMENT],
            'understanding': [EngineCategory.PHILOSOPHY, EngineCategory.PSYCHOLOGY],
        }
        
        logger.info("EngineRouter initialized")
    
    def route(self, query: str, 
              problem_type: Optional[str] = None,
              required_capabilities: Optional[List[str]] = None,
              mode: InvocationMode = InvocationMode.SINGLE,
              top_k: int = 3) -> List[EngineNode]:
        """路由查询到合适的引擎"""
        candidate_nodes: List[EngineNode] = []
        candidate_scores: Dict[str, float] = {}
        
        if problem_type and problem_type in self._problem_type_mapping:
            categories = self._problem_type_mapping[problem_type]
            for cat in categories:
                for node in self.registry.get_by_category(cat):
                    if node.is_active:
                        candidate_nodes.append(node)
                        candidate_scores[node.node_id] = candidate_scores.get(node.node_id, 0) + 0.5
        
        keywords = self._extract_keywords(query)
        keyword_matches = self.registry.find_by_keywords(keywords)
        for node in keyword_matches:
            if node.is_active and node not in candidate_nodes:
                candidate_nodes.append(node)
            candidate_scores[node.node_id] = candidate_scores.get(node.node_id, 0) + 0.4
        
        similar_matches = self.registry.find_similar(query, top_k=top_k)
        for node, score in similar_matches:
            if node.is_active and node not in candidate_nodes:
                candidate_nodes.append(node)
            candidate_scores[node.node_id] = candidate_scores.get(node.node_id, 0) + score * 0.3
        
        if required_capabilities:
            for node in candidate_nodes[:]:
                capabilities_match = sum(1 for cap in required_capabilities if cap in node.metadata.capabilities)
                if capabilities_match == 0:
                    candidate_nodes.remove(node)
                else:
                    candidate_scores[node.node_id] = candidate_scores.get(node.node_id, 0) + capabilities_match * 0.2
        
        if mode == InvocationMode.SINGLE:
            candidate_nodes = candidate_nodes[:1]
        elif mode == InvocationMode.MULTIPLE:
            candidate_nodes = candidate_nodes[:self.config.max_parallel_engines]
        
        candidate_nodes.sort(key=lambda n: -candidate_scores.get(n.node_id, 0))
        
        if candidate_nodes:
            logger.info(f"Routed query to {len(candidate_nodes)} engines")
        
        return candidate_nodes
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                     'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
                     'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
                     'into', 'through', 'during', 'before', 'after', 'above', 'below',
                     'between', 'under', 'again', 'further', 'then', 'once', 'how', 'what'}
        
        words = query.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords[:10]


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎融合器
# ═══════════════════════════════════════════════════════════════════════════════

class EngineFusion:
    """引擎融合器"""
    
    def __init__(self, registry: EngineRegistry, config: Optional[NetworkConfig] = None):
        self.registry = registry
        self.config = config or NetworkConfig()
        logger.info("EngineFusion initialized")
    
    def fuse(self, results: List[EngineResult], strategy: FusionStrategy, query: Optional[str] = None) -> EngineFusionResult:
        """融合多个引擎的结果"""
        if not results:
            return EngineFusionResult(success=False, error="No results to fuse", strategy=strategy)
        
        valid_results = [r for r in results if r.success]
        if not valid_results:
            return EngineFusionResult(success=False, error="All engines failed", strategy=strategy,
                                      engines_used=[r.engine_id for r in results])
        
        if strategy == FusionStrategy.PARALLEL:
            return self._fuse_parallel(valid_results, strategy)
        elif strategy == FusionStrategy.VOTING:
            return self._fuse_voting(valid_results, strategy)
        elif strategy == FusionStrategy.WEIGHTED:
            return self._fuse_weighted(valid_results, strategy)
        elif strategy == FusionStrategy.SEQUENTIAL:
            return self._fuse_sequential(valid_results, strategy)
        elif strategy == FusionStrategy.CHAIN:
            return self._fuse_chain(valid_results, strategy)
        elif strategy == FusionStrategy.HIERARCHICAL:
            return self._fuse_hierarchical(valid_results, strategy)
        else:
            return self._fuse_parallel(valid_results, strategy)
    
    def _fuse_parallel(self, results: List[EngineResult], strategy: FusionStrategy) -> EngineFusionResult:
        outputs = [r.output for r in results]
        return EngineFusionResult(
            success=True,
            strategy=strategy,
            output={'type': 'parallel', 'outputs': outputs},
            engines_used=[r.engine_id for r in results],
            individual_results=results,
            fused_confidence=sum(r.confidence for r in results) / len(results),
            fused_quality=sum(r.quality_score for r in results) / len(results),
            agreement_score=0.8,
            total_latency_ms=sum(r.latency_ms for r in results)
        )
    
    def _fuse_voting(self, results: List[EngineResult], strategy: FusionStrategy) -> EngineFusionResult:
        best_result = max(results, key=lambda r: r.confidence * r.quality_score)
        return EngineFusionResult(
            success=True,
            strategy=strategy,
            output=best_result.output,
            engines_used=[r.engine_id for r in results],
            individual_results=results,
            fused_confidence=best_result.confidence,
            fused_quality=best_result.quality_score,
            agreement_score=best_result.confidence,
            total_latency_ms=max(r.latency_ms for r in results)
        )
    
    def _fuse_weighted(self, results: List[EngineResult], strategy: FusionStrategy) -> EngineFusionResult:
        weights = []
        for r in results:
            node = self.registry.get_engine(r.engine_id)
            weight = node.metadata.weight if node else 1.0
            weights.append(weight)
        
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        fused_confidence = sum(r.confidence * w for r, w in zip(results, normalized_weights))
        fused_quality = sum(r.quality_score * w for r, w in zip(results, normalized_weights))
        
        return EngineFusionResult(
            success=True,
            strategy=strategy,
            output={'type': 'weighted', 'outputs': [r.output for r in results], 'weights': normalized_weights},
            engines_used=[r.engine_id for r in results],
            individual_results=results,
            fused_confidence=fused_confidence,
            fused_quality=fused_quality,
            agreement_score=0.7,
            total_latency_ms=max(r.latency_ms for r in results)
        )
    
    def _fuse_sequential(self, results: List[EngineResult], strategy: FusionStrategy) -> EngineFusionResult:
        final_output = results[-1].output if results else None
        return EngineFusionResult(
            success=True,
            strategy=strategy,
            output={'type': 'sequential', 'chain': [r.output for r in results]},
            engines_used=[r.engine_id for r in results],
            individual_results=results,
            fused_confidence=results[-1].confidence if results else 0,
            fused_quality=results[-1].quality_score if results else 0,
            total_latency_ms=sum(r.latency_ms for r in results)
        )
    
    def _fuse_chain(self, results: List[EngineResult], strategy: FusionStrategy) -> EngineFusionResult:
        all_traces = []
        for r in results:
            all_traces.extend(r.reasoning_trace)
        
        combined = {
            'type': 'chain',
            'stages': [r.output for r in results],
            'reasoning_trace': all_traces
        }
        
        return EngineFusionResult(
            success=True,
            strategy=strategy,
            output=combined,
            engines_used=[r.engine_id for r in results],
            individual_results=results,
            fused_confidence=max(r.confidence for r in results),
            fused_quality=max(r.quality_score for r in results),
            agreement_score=0.75,
            total_latency_ms=sum(r.latency_ms for r in results)
        )
    
    def _fuse_hierarchical(self, results: List[EngineResult], strategy: FusionStrategy) -> EngineFusionResult:
        by_category: Dict[str, List[EngineResult]] = defaultdict(list)
        for r in results:
            node = self.registry.get_engine(r.engine_id)
            if node:
                cat = node.metadata.category.value
                by_category[cat].append(r)
        
        category_fused = []
        for cat, cat_results in by_category.items():
            cat_fused = self._fuse_voting(cat_results, strategy)
            category_fused.append(cat_fused)
        
        return EngineFusionResult(
            success=True,
            strategy=strategy,
            output={'type': 'hierarchical', 'categories': {k: v.output for k, v in zip(by_category.keys(), category_fused)}},
            engines_used=[r.engine_id for r in results],
            individual_results=results,
            fused_confidence=sum(f.fused_confidence for f in category_fused) / len(category_fused) if category_fused else 0,
            fused_quality=sum(f.fused_quality for f in category_fused) / len(category_fused) if category_fused else 0,
            total_latency_ms=sum(r.latency_ms for r in results)
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎网络
# ═══════════════════════════════════════════════════════════════════════════════

class EngineNetwork:
    """引擎网络"""
    
    def __init__(self, config: Optional[NetworkConfig] = None):
        self.config = config or NetworkConfig()
        self.registry = EngineRegistry()
        self.router = EngineRouter(self.registry, self.config)
        self.fusion = EngineFusion(self.registry, self.config)
        self.engine_graph: Dict[str, List[str]] = defaultdict(list)
        self._result_cache: Dict[str, EngineFusionResult] = {}
        logger.info("EngineNetwork initialized")
    
    def register_engine(self, engine_id: str, name: str, description: str, category: EngineCategory,
                       capabilities: Optional[List[str]] = None, triggers: Optional[List[str]] = None,
                       executor: Optional[Callable] = None, **kwargs) -> EngineNode:
        """注册引擎"""
        metadata = EngineMetadata(
            engine_id=engine_id,
            name=name,
            display_name=name,
            description=description,
            category=category,
            capabilities=capabilities or [],
            triggers=triggers or [],
            file_path=kwargs.get('file_path', ''),
            quality_score=kwargs.get('quality_score', 0.5),
            reliability=kwargs.get('reliability', 0.8),
            weight=kwargs.get('weight', 1.0),
            dependencies=kwargs.get('dependencies', [])
        )
        
        return self.registry.register_engine(metadata=metadata, executor=executor,
                                              preprocessor=kwargs.get('preprocessor'),
                                              postprocessor=kwargs.get('postprocessor'))
    
    def batch_register(self, engine_configs: List[Dict[str, Any]]) -> int:
        """批量注册引擎"""
        registered = 0
        for config in engine_configs:
            try:
                self.register_engine(**config)
                registered += 1
            except Exception as e:
                logger.error(f"Failed to register {config.get('name', 'unknown')}: {e}")
        return registered
    
    def get_engine(self, engine_id: str) -> Optional[EngineNode]:
        """获取引擎"""
        return self.registry.get_engine(engine_id)
    
    def list_engines(self, category: Optional[EngineCategory] = None) -> List[EngineMetadata]:
        """列出引擎"""
        if category:
            return [n.metadata for n in self.registry.get_by_category(category)]
        return self.registry.list_all()
    
    def invoke(self, query: str, mode: InvocationMode = InvocationMode.SINGLE,
              strategy: Optional[FusionStrategy] = None, problem_type: Optional[str] = None,
              engine_ids: Optional[List[str]] = None, **kwargs) -> EngineFusionResult:
        """调用引擎网络处理查询"""
        start_time = time.time()
        
        if engine_ids:
            engines = [self.registry.get_engine(eid) for eid in engine_ids if self.registry.get_engine(eid)]
        else:
            engines = self.router.route(query=query, problem_type=problem_type, mode=mode, **kwargs)
        
        if not engines:
            return EngineFusionResult(success=False, error="No suitable engines found",
                                      strategy=strategy or self.config.default_fusion_strategy)
        
        results = []
        for engine in engines:
            result = engine.execute(query, **kwargs)
            results.append(result)
        
        fusion_strategy = strategy or self.config.default_fusion_strategy
        fused_result = self.fusion.fuse(results, fusion_strategy, query)
        fused_result.total_latency_ms = (time.time() - start_time) * 1000
        
        return fused_result
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取网络统计"""
        return {
            'registry': self.registry.get_statistics(),
            'config': {
                'max_parallel': self.config.max_parallel_engines,
                'enable_cache': self.config.enable_cache,
                'default_strategy': self.config.default_fusion_strategy.value
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        all_engines = self.registry.list_all()
        healthy = sum(1 for e in all_engines if e.status == EngineStatus.IDLE or e.status == EngineStatus.BUSY)
        errors = sum(1 for e in all_engines if e.status == EngineStatus.ERROR)
        
        return {
            'healthy': healthy,
            'errors': errors,
            'total': len(all_engines),
            'health_ratio': healthy / max(len(all_engines), 1)
        }
    
    def to_divine_reason_nodes(self) -> List[EngineNode]:
        """导出为DivineReason节点列表"""
        return list(self.registry._nodes.values())
    
    def export_network(self) -> Dict[str, Any]:
        """导出网络结构"""
        return {
            'nodes': [node.to_dict() for node in self.registry._nodes.values()],
            'edges': [{'from': k, 'to': v} for k, v in self.engine_graph.items()],
            'statistics': self.get_statistics()
        }


def create_engine_network(config: Optional[NetworkConfig] = None) -> EngineNetwork:
    """创建引擎网络"""
    return EngineNetwork(config)


# 别名
EngineNet = EngineNetwork
