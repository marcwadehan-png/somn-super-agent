# -*- coding: utf-8 -*-
"""
DivineReason 引擎网络融合系统
==============================

将 EngineNetwork 集成到 DivineReason，形成超级推理引擎网络。

架构：
┌─────────────────────────────────────────────────────────────────────────┐
│                    🔮 DivineReason 超级引擎网络                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   EngineNetwork (引擎网络)                        │   │
│  │                                                                   │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │   │
│  │  │哲学引擎│ │军事引擎│ │心理引擎│ │管理引擎│ │经济引擎│       │   │
│  │  │  (12)  │ │  (15)  │ │  (18)  │ │  (14)  │ │  (11)  │       │   │
│  │  └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘       │   │
│  │      └──────────┴──────────┴──────────┴──────────┘           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                   │
│                                    ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              DivineReasonEngineNode                              │   │
│  │                   (引擎作为推理节点)                               │   │
│  │                                                                   │   │
│  │  ┌────────────────────────────────────────────────────────────┐  │   │
│  │  │                     Fusion Layer                            │  │   │
│  │  │  - 引擎选择      - 结果融合      - 质量评估                  │  │   │
│  │  │  - 路由决策      - 协同编排      - 回溯优化                  │  │   │
│  │  └────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

功能：
- 引擎作为 DivineReason 节点
- 全局引擎路由
- 多引擎协同推理
- 引擎结果融合
- 动态引擎编排

版本: V1.0.0
创建: 2026-04-28
"""

import logging
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import hashlib
import time
import uuid

from ..reasoning._unified_reasoning_engine import (
    DivineReason,
    UnifiedConfig,
    UnifiedNode,
    NodeType,
    EdgeType,
    ReasoningMode,
    ReasoningResult,
    ThoughtPath,
    GraphStatistics
)

from ._engine_network import (
    EngineNetwork,
    EngineNode,
    EngineCategory,
    EngineResult,
    EngineFusionResult,
    FusionStrategy,
    InvocationMode,
    NetworkConfig,
    EngineMetadata,
    create_engine_network
)

from ._engine_discovery import (
    EngineScanner,
    EngineNetworkBuilder,
    build_engine_network
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class EngineInvokeNode:
    """
    引擎调用节点 - 封装引擎调用为 DivineReason 节点
    
    属性：
    - engine_id: 引擎ID
    - query: 查询内容
    - mode: 调用模式
    - strategy: 融合策略
    - result: 调用结果
    - divine_node: 对应的 DivineReason 节点
    """
    node_id: str
    engine_id: str
    query: str
    mode: InvocationMode = InvocationMode.SINGLE
    strategy: FusionStrategy = FusionStrategy.WEIGHTED
    
    # DivineReason 集成
    divine_node_id: Optional[str] = None
    parent_node_ids: List[str] = field(default_factory=list)
    
    # 结果
    result: Optional[EngineFusionResult] = None
    success: bool = False
    error: Optional[str] = None
    
    # 质量指标
    confidence: float = 0.0
    quality_score: float = 0.0
    latency_ms: float = 0.0
    
    def to_divine_node(self) -> UnifiedNode:
        """转换为 DivineReason 节点"""
        content = f"[Engine: {self.engine_id}] {self.query}"
        if self.result and self.result.success:
            content += f"\nOutput: {str(self.result.output)[:200]}"
        
        return UnifiedNode(
            node_id=self.divine_node_id or self.node_id,
            content=content,
            node_type=NodeType.INSIGHT if self.success else NodeType.CRITIQUE,
            depth=1,
            combined_score=self.quality_score * self.confidence,
            metadata=ReasoningMetadata(
                source_engine="engine_network",
                generation_method="invoke"
            )
        )


@dataclass
class EngineInvocationPlan:
    """引擎调用计划"""
    plan_id: str
    query: str
    planned_invocations: List[EngineInvokeNode] = field(default_factory=list)
    
    # 依赖关系
    dependencies: Dict[str, List[str]] = field(default_factory=dict)  # node_id -> depends_on
    
    # 优化信息
    estimated_latency_ms: float = 0.0
    estimated_quality: float = 0.0
    
    def to_divine_graph(self) -> Dict[str, Any]:
        """转换为 DivineReason 图结构"""
        nodes = []
        edges = []
        
        for invoke_node in self.planned_invocations:
            divine_node = invoke_node.to_divine_node()
            nodes.append(divine_node)
            
            # 添加边
            for parent_id in invoke_node.parent_node_ids:
                edges.append({
                    'source': parent_id,
                    'target': divine_node.node_id,
                    'edge_type': EdgeType.SUPPORT.value
                })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'plan_id': self.plan_id
        }


@dataclass
class ReasoningMetadata:
    """推理元数据（与 DivineReason 保持一致）"""
    source_engine: str = "engine_network"
    generation_method: str = "invoke"
    is_correction: bool = False
    is_reflection: bool = False


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎推理协调器
# ═══════════════════════════════════════════════════════════════════════════════

class EngineReasoningCoordinator:
    """
    引擎推理协调器 - 协调 EngineNetwork 和 DivineReason
    
    职责：
    1. 接收推理请求
    2. 制定引擎调用计划
    3. 执行引擎调用
    4. 将结果融入 DivineReason 图
    5. 生成最终推理结果
    """
    
    def __init__(self,
                 divine_reason: Optional[DivineReason] = None,
                 engine_network: Optional[EngineNetwork] = None,
                 config: Optional[NetworkConfig] = None):
        """
        初始化协调器
        
        Args:
            divine_reason: DivineReason 实例
            engine_network: EngineNetwork 实例
            config: 网络配置
        """
        # 创建或使用提供的实例
        if divine_reason is None:
            divine_config = UnifiedConfig(
                max_nodes=500,
                max_depth=20,
                enable_cache=True
            )
            self.divine = DivineReason(config=divine_config)
        else:
            self.divine = divine_reason
        
        if engine_network is None:
            self.network = create_engine_network(config)
        else:
            self.network = engine_network
        
        # 统计
        self.total_invocations = 0
        self.total_fusions = 0
        
        logger.info("EngineReasoningCoordinator initialized")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 核心推理方法
    # ═══════════════════════════════════════════════════════════════════════════
    
    def solve(self,
              query: str,
              mode: InvocationMode = InvocationMode.MULTIPLE,
              strategy: FusionStrategy = FusionStrategy.HIERARCHICAL,
              problem_type: Optional[str] = None,
              engine_ids: Optional[List[str]] = None,
              max_engines: int = 5,
              use_divine: bool = True) -> ReasoningResult:
        """
        解决查询 - 整合引擎网络和 DivineReason
        
        Args:
            query: 用户查询
            mode: 调用模式
            strategy: 融合策略
            problem_type: 问题类型
            engine_ids: 指定引擎ID
            max_engines: 最大引擎数
            use_divine: 是否使用 DivineReason 图结构
        
        Returns:
            ReasoningResult
        """
        start_time = time.time()
        
        # 1. 引擎调用
        engine_result = self.network.invoke(
            query=query,
            mode=mode,
            strategy=strategy,
            problem_type=problem_type,
            engine_ids=engine_ids
        )
        
        self.total_invocations += 1
        
        # 2. 如果使用 DivineReason，添加引擎结果到图
        if use_divine:
            self._add_engine_result_to_graph(query, engine_result)
            
            # 3. 生成最终推理结果
            divine_result = self.divine.solve(
                problem=query,
                mode=ReasoningMode.DIVINE
            )
            
            # 合并结果
            final_result = self._merge_results(query, divine_result, engine_result)
        else:
            final_result = self._engine_result_to_reasoning_result(query, engine_result)
        
        final_result.latency_ms = (time.time() - start_time) * 1000
        return final_result
    
    def solve_with_plan(self,
                       query: str,
                       plan: EngineInvocationPlan) -> ReasoningResult:
        """
        按照计划执行引擎调用
        
        Args:
            query: 查询
            plan: 调用计划
        
        Returns:
            ReasoningResult
        """
        start_time = time.time()
        
        # 按依赖顺序执行
        executed = set()
        results: Dict[str, EngineFusionResult] = {}
        
        for invoke_node in plan.planned_invocations:
            # 检查依赖是否完成
            deps_met = all(dep in executed for dep in plan.dependencies.get(invoke_node.node_id, []))
            
            if not deps_met:
                logger.warning(f"Dependencies not met for {invoke_node.node_id}")
                continue
            
            # 执行引擎
            engine_result = self.network.invoke(
                query=invoke_node.query,
                mode=invoke_node.mode,
                strategy=invoke_node.strategy,
                engine_ids=[invoke_node.engine_id] if invoke_node.engine_id else None
            )
            
            invoke_node.result = engine_result
            invoke_node.success = engine_result.success
            invoke_node.confidence = engine_result.fused_confidence
            invoke_node.quality_score = engine_result.fused_quality
            invoke_node.latency_ms = engine_result.total_latency_ms
            
            executed.add(invoke_node.node_id)
            results[invoke_node.node_id] = engine_result
        
        # 融合所有结果
        all_engine_results = [
            r for result in results.values() 
            for r in result.individual_results
        ]
        
        final_fusion = self.network.fusion.fuse(
            all_engine_results,
            FusionStrategy.HIERARCHICAL,
            query
        )
        
        self.total_fusions += 1
        
        # 转换为 ReasoningResult
        reasoning_result = self._engine_result_to_reasoning_result(query, final_fusion)
        reasoning_result.latency_ms = (time.time() - start_time) * 1000
        
        return reasoning_result
    
    def create_plan(self,
                   query: str,
                   max_engines: int = 5,
                   problem_type: Optional[str] = None) -> EngineInvocationPlan:
        """
        创建引擎调用计划
        
        Args:
            query: 查询
            max_engines: 最大引擎数
            problem_type: 问题类型
        
        Returns:
            EngineInvocationPlan
        """
        plan = EngineInvocationPlan(
            plan_id=str(uuid.uuid4()),
            query=query
        )
        
        # 路由选择引擎
        selected_nodes = self.network.router.route(
            query=query,
            problem_type=problem_type,
            mode=InvocationMode.MULTIPLE,
            top_k=max_engines
        )
        
        # 创建调用节点
        for i, node in enumerate(selected_nodes):
            invoke_node = EngineInvokeNode(
                node_id=f"invoke_{i}_{node.metadata.engine_id}",
                engine_id=node.metadata.engine_id,
                query=query,
                mode=InvocationMode.SINGLE,
                divine_node_id=node.node_id
            )
            plan.planned_invocations.append(invoke_node)
            
            # 估计延迟和质量
            plan.estimated_latency_ms += node.metadata.latency_ms
            plan.estimated_quality += node.metadata.quality_score
        
        # 标准化质量
        if plan.planned_invocations:
            plan.estimated_quality /= len(plan.planned_invocations)
        
        return plan
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 辅助方法
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _add_engine_result_to_graph(self, query: str, engine_result: EngineFusionResult):
        """将引擎结果添加到 DivineReason 图"""
        # 添加根节点
        root = self.divine.graph.add_node(
            content=f"Query: {query}",
            node_type=NodeType.ROOT,
            depth=0
        )
        
        # 添加引擎节点
        for i, individual_result in enumerate(engine_result.individual_results):
            engine_node = self.divine.graph.add_node(
                content=f"[Engine Result] {str(individual_result.output)[:100]}...",
                node_type=NodeType.INSIGHT,
                depth=1,
                combined_score=individual_result.quality_score * individual_result.confidence,
                metadata=ReasoningMetadata(
                    source_engine=individual_result.engine_id,
                    generation_method="engine_invoke"
                )
            )
            
            # 添加边
            self.divine.graph.add_edge(
                source_id=root.node_id,
                target_id=engine_node.node_id,
                edge_type=EdgeType.SUPPORT
            )
        
        # 添加融合节点
        if engine_result.success:
            fusion_content = f"[Fusion: {engine_result.strategy.value}]\n"
            fusion_content += f"Confidence: {engine_result.fused_confidence:.2f}\n"
            fusion_content += f"Quality: {engine_result.fused_quality:.2f}\n"
            fusion_content += f"Engines: {', '.join(engine_result.engines_used)}"
            
            fusion_node = self.divine.graph.add_node(
                content=fusion_content,
                node_type=NodeType.SYNTHESIS,
                depth=2,
                combined_score=engine_result.fused_quality * engine_result.fused_confidence,
                metadata=ReasoningMetadata(
                    source_engine="fusion",
                    generation_method=engine_result.strategy.value
                )
            )
            
            # 连接所有引擎节点到融合节点
            for individual_result in engine_result.individual_results:
                self.divine.graph.add_edge(
                    source_id=individual_result.engine_id,
                    target_id=fusion_node.node_id,
                    edge_type=EdgeType.SYNTHESIS
                )
    
    def _merge_results(self,
                      query: str,
                      divine_result: ReasoningResult,
                      engine_result: EngineFusionResult) -> ReasoningResult:
        """合并 DivineReason 和引擎结果"""
        # 使用 DivineReason 结果作为基础
        final_result = divine_result
        
        # 添加引擎信息
        if hasattr(final_result, 'metadata'):
            final_result.metadata['engine_network'] = {
                'engines_used': engine_result.engines_used,
                'fusion_strategy': engine_result.strategy.value,
                'fused_confidence': engine_result.fused_confidence,
                'fused_quality': engine_result.fused_quality,
                'agreement_score': engine_result.agreement_score
            }
        
        # 更新质量评分
        if hasattr(final_result, 'quality_score'):
            # 综合 DivineReason 和引擎网络的评分
            engine_weight = 0.4
            divine_weight = 0.6
            final_result.quality_score = (
                final_result.quality_score * divine_weight +
                engine_result.fused_quality * engine_weight
            )
        
        return final_result
    
    def _engine_result_to_reasoning_result(self, query: str, engine_result: EngineFusionResult) -> ReasoningResult:
        return ReasoningResult(
            problem=query,
            success=engine_result.success,
            solution=str(engine_result.output) if engine_result.output else '',
            quality_score=engine_result.fused_quality,
            insights=[{'engine': r.engine_id, 'confidence': r.confidence, 'output': str(r.output)} for r in engine_result.individual_results],
            reflections=[{'engine': r.engine_id, 'relevance': r.relevance} for r in engine_result.individual_results],
            critiques=[],
            metadata={
                'engine_network': True,
                'fusion_strategy': engine_result.strategy.value,
                'engines_used': engine_result.engines_used,
                'fused_confidence': engine_result.fused_confidence
            },
            errors=[engine_result.error] if engine_result.error else []
        )

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'total_invocations': self.total_invocations,
            'total_fusions': self.total_fusions,
            'network': self.network.get_statistics(),
            'divine': {
                'graph_nodes': len(self.divine.current_graph._nodes) if hasattr(self.divine, 'current_graph') and self.divine.current_graph is not None else 0
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            'divine': self.divine is not None,
            'network': self.network is not None,
            'network_health': self.network.health_check(),
            'engines_registered': self.network.registry.get_active_count()
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 超级引擎网络（主类）
# ═══════════════════════════════════════════════════════════════════════════════

class DivineReasonNetwork:
    """
    DivineReason 超级引擎网络 - 完整集成系统
    
    这是主入口类，整合了：
    - DivineReason 超级推理引擎
    - EngineNetwork 引擎网络
    - EngineReasoningCoordinator 推理协调器
    
    用法:
        # 方式1: 自动构建
        network = DivineReasonNetwork.auto_build('/path/to/project')
        result = network.solve("分析AI发展趋势")
        
        # 方式2: 手动构建
        network = DivineReasonNetwork()
        network.load_engines('/path/to/engines')
        result = network.solve("制定战略计划")
        
        # 方式3: 指定引擎
        result = network.solve("...", engine_ids=['philosophy_engine', 'strategy_engine'])
    """
    
    def __init__(self, config: Optional[NetworkConfig] = None):
        """
        初始化
        
        Args:
            config: 网络配置
        """
        self.config = config or NetworkConfig()
        
        # 组件
        self.divine: Optional[DivineReason] = None
        self.network: Optional[EngineNetwork] = None
        self.coordinator: Optional[EngineReasoningCoordinator] = None
        
        # 状态
        self._initialized = False
        self._engine_count = 0
        
        logger.info("DivineReasonNetwork initialized (not built)")
    
    @classmethod
    def auto_build(cls,
                  base_path: str,
                  directories: Optional[List[str]] = None,
                  config: Optional[NetworkConfig] = None) -> 'DivineReasonNetwork':
        """
        自动构建引擎网络
        
        Args:
            base_path: 项目根目录
            directories: 要扫描的目录
            config: 网络配置
        
        Returns:
            构建好的 DivineReasonNetwork
        """
        instance = cls(config)
        instance.build(base_path, directories)
        return instance
    
    def build(self,
             base_path: str,
             directories: Optional[List[str]] = None) -> 'DivineReasonNetwork':
        """
        构建引擎网络
        
        Args:
            base_path: 项目根目录
            directories: 要扫描的目录
        """
        logger.info(f"Building DivineReasonNetwork from {base_path}")
        
        # 1. 构建引擎网络
        if directories is None:
            directories = [
                'smart_office_assistant/src/intelligence/engines',
                'smart_office_assistant/src/intelligence/reasoning'
            ]
        
        builder = EngineNetworkBuilder(base_path, self.config)
        self.network = builder.scan(directories).register().build()
        
        # 2. 创建 DivineReason
        divine_config = UnifiedConfig(
            max_nodes=500,
            max_depth=20,
            enable_cache=True,
            enable_critique=True
        )
        self.divine = DivineReason(config=divine_config)
        
        # 3. 创建协调器
        self.coordinator = EngineReasoningCoordinator(
            divine_reason=self.divine,
            engine_network=self.network,
            config=self.config
        )
        
        # 4. 将引擎节点添加到 DivineReason
        self._sync_engine_nodes()
        
        self._initialized = True
        self._engine_count = self.network.registry.get_active_count()
        
        logger.info(f"DivineReasonNetwork built with {self._engine_count} engines")
        return self
    
    def _sync_engine_nodes(self):
        """同步引擎节点到 DivineReason"""
        for engine_node in self.network.to_divine_reason_nodes():
            # 添加为 DivineReason 节点
            divine_node = self.divine.graph.add_node(
                content=f"[Engine: {engine_node.metadata.name}] {engine_node.metadata.description[:100]}",
                node_type=NodeType.INSIGHT,
                depth=0,
                combined_score=engine_node.metadata.quality_score,
                metadata=ReasoningMetadata(
                    source_engine=engine_node.metadata.engine_id,
                    generation_method="engine_node"
                )
            )
            
            # 记录映射
            engine_node.divine_node_id = divine_node.node_id
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 核心方法
    # ═══════════════════════════════════════════════════════════════════════════
    
    def solve(self,
            query: str,
            mode: InvocationMode = InvocationMode.MULTIPLE,
            strategy: FusionStrategy = FusionStrategy.HIERARCHICAL,
            problem_type: Optional[str] = None,
            engine_ids: Optional[List[str]] = None,
            use_divine: bool = True,
            **kwargs) -> ReasoningResult:
        """
        解决查询
        
        Args:
            query: 用户查询
            mode: 调用模式
            strategy: 融合策略
            problem_type: 问题类型
            engine_ids: 指定引擎ID
            use_divine: 是否使用 DivineReason
        
        Returns:
            ReasoningResult
        """
        self._ensure_initialized()
        
        return self.coordinator.solve(
            query=query,
            mode=mode,
            strategy=strategy,
            problem_type=problem_type,
            engine_ids=engine_ids,
            use_divine=use_divine,
            **kwargs
        )
    
    def invoke(self,
              query: str,
              engine_ids: List[str],
              mode: InvocationMode = InvocationMode.SINGLE,
              strategy: FusionStrategy = FusionStrategy.WEIGHTED) -> EngineFusionResult:
        """
        直接调用引擎
        
        Args:
            query: 查询
            engine_ids: 引擎ID列表
            mode: 调用模式
            strategy: 融合策略
        
        Returns:
            EngineFusionResult
        """
        self._ensure_initialized()
        
        return self.network.invoke(
            query=query,
            engine_ids=engine_ids,
            mode=mode,
            strategy=strategy
        )
    
    def create_plan(self,
                   query: str,
                   max_engines: int = 5,
                   problem_type: Optional[str] = None) -> EngineInvocationPlan:
        """创建调用计划"""
        self._ensure_initialized()
        return self.coordinator.create_plan(query, max_engines, problem_type)
    
    def solve_with_plan(self,
                       query: str,
                       plan: EngineInvocationPlan) -> ReasoningResult:
        """按计划执行"""
        self._ensure_initialized()
        return self.coordinator.solve_with_plan(query, plan)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 工具方法
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _ensure_initialized(self):
        """确保已初始化"""
        if not self._initialized:
            raise RuntimeError("DivineReasonNetwork not initialized. Call build() or auto_build() first.")
    
    def get_engines(self, 
                   category: Optional[EngineCategory] = None) -> List[EngineMetadata]:
        """获取引擎列表"""
        self._ensure_initialized()
        return self.network.list_engines(category)
    
    def find_engines(self, query: str, top_k: int = 5) -> List[Tuple[EngineMetadata, float]]:
        """查找相关引擎"""
        self._ensure_initialized()
        nodes = self.network.router.route(query, top_k=top_k)
        return [(n.metadata, n.metadata.quality_score) for n in nodes]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        self._ensure_initialized()
        return {
            'engine_count': self._engine_count,
            'coordinator': self.coordinator.get_statistics()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        if not self._initialized:
            return {'initialized': False}
        return {
            'initialized': True,
            'engine_count': self._engine_count,
            'network_health': self.network.health_check() if self.network else None
        }
    
    def export_network(self) -> Dict[str, Any]:
        """导出网络结构"""
        self._ensure_initialized()
        return self.network.export_network()
    
    def __repr__(self) -> str:
        if self._initialized:
            return f"DivineReasonNetwork(engines={self._engine_count})"
        return "DivineReasonNetwork(not initialized)"


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

def create_divine_reason_network(
    base_path: str,
    directories: Optional[List[str]] = None,
    config: Optional[NetworkConfig] = None
) -> DivineReasonNetwork:
    """
    创建 DivineReason 超级引擎网络
    
    一站式函数。
    """
    return DivineReasonNetwork.auto_build(base_path, directories, config)


# ═══════════════════════════════════════════════════════════════════════════════
# 别名
# ═══════════════════════════════════════════════════════════════════════════════

SuperEngineNetwork = DivineReasonNetwork
