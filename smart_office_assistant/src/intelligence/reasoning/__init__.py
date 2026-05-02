# -*- coding: utf-8 -*-
"""
推理层 - reasoning 子模块
目录整理 v1.0 (2026-04-05)
提供向后兼容的 re-export
"""

import logging

logger = logging.getLogger(__name__)

# ── deep_reasoning_engine ─────────────────────────────────────────────────────
try:
    from .deep_reasoning_engine import DeepReasoningEngine, ReasoningMode
except ImportError as e:
    logger.warning(f"DeepReasoningEngine 加载失败: {e}")
    DeepReasoningEngine = None
    ReasoningMode = None

# ── dewey_thinking_engine ─────────────────────────────────────────────────────
try:
    from .dewey_thinking_engine import DeweyThinkingEngine
except ImportError as e:
    logger.warning(f"DeweyThinkingEngine 加载失败: {e}")
    DeweyThinkingEngine = None

# ── geodesic_reasoning_engine ─────────────────────────────────────────────────
try:
    from .geodesic_reasoning_engine import GeodesicReasoningEngine
except ImportError as e:
    logger.warning(f"GeodesicReasoningEngine 加载失败: {e}")
    GeodesicReasoningEngine = None

# ── reasoning_memory ──────────────────────────────────────────────────────────
try:
    from .reasoning_memory import ReasoningMemory
except ImportError as e:
    logger.warning(f"ReasoningMemory 加载失败: {e}")
    ReasoningMemory = None

# ── reverse_thinking_engine ───────────────────────────────────────────────────
try:
    from .reverse_thinking_engine import ReverseThinkingEngine
except ImportError as e:
    logger.warning(f"ReverseThinkingEngine 加载失败: {e}")
    ReverseThinkingEngine = None

# ── sequence_reasoning_engine ─────────────────────────────────────────────────
try:
    from .sequence_reasoning_engine import SequenceReasoningEngine
except ImportError as e:
    logger.warning(f"SequenceReasoningEngine 加载失败: {e}")
    SequenceReasoningEngine = None

# ── strategic_reasoning_engine ────────────────────────────────────────────────
try:
    from .strategic_reasoning_engine import StrategicReasoningEngine
except Exception as e:
    logger.warning(f"StrategicReasoningEngine 加载失败: {e}")
    StrategicReasoningEngine = None

# ── yangming_reasoning_engine ─────────────────────────────────────────────────
try:
    from .yangming_reasoning_engine import YangmingReasoningEngine
except ImportError as e:
    logger.warning(f"YangmingReasoningEngine 加载失败: {e}")
    YangmingReasoningEngine = None

# ── phase_synchronization_coordinator ─────────────────────────────────────────
try:
    from .phase_synchronization_coordinator import PhaseSynchronizationCoordinator
except ImportError as e:
    logger.warning(f"PhaseSynchronizationCoordinator 加载失败: {e}")
    PhaseSynchronizationCoordinator = None

# ── 新增推理引擎 v1.0.0 (2026-04-24) ─────────────────────────────────────

# Long CoT推理引擎
try:
    from ._long_cot_engine import (
        LongCoTReasoningEngine,
        LongCoTConfig,
        BoundaryDetector,
        InsightDetector,
        SelfCorrector,
        AdaptiveThinkingAllocator,
        CheckpointManager,
        ThoughtCheckpoint,
        InsightMoment,
        InsightType,
        get_long_cot_engine,
        create_long_cot_engine,
        reason_with_long_cot,
    )
except ImportError as e:
    logger.warning(f"LongCoTReasoningEngine 加载失败: {e}")
    LongCoTReasoningEngine = None

# ToT树推理引擎
try:
    from ._tot_engine import (
        TreeOfThoughtsEngine,
        ToTConfig,
        TreeSearchCoordinator,
        ThoughtTree,
        ThoughtTreeNode,
        ThoughtGenerator,
        LLMBasedThoughtGenerator,
        StateEvaluator,
        DefaultStateEvaluator,
        SearchStrategy,
        get_tot_engine,
        create_tot_engine,
        solve_with_tot,
    )
except ImportError as e:
    logger.warning(f"TreeOfThoughtsEngine 加载失败: {e}")
    TreeOfThoughtsEngine = None

# ReAct推理引擎
try:
    from ._react_engine import (
        ReActEngine,
        ReActConfig,
        Tool,
        ToolRegistry,
        ToolExecutor,
        ThoughtGenerator,
        ContextManager,
        SearchTool,
        CalculatorTool,
        LookupTool,
        RetrieveTool,
        ToolResult,
        TAOStep,
        TAOTrajectory,
        ActionType,
        get_react_engine,
        create_react_engine,
        reason_with_react,
    )
except ImportError as e:
    logger.warning(f"ReActEngine 加载失败: {e}")
    ReActEngine = None

# GoT图推理引擎
try:
    from ._got_engine import (
        GraphOfThoughtsEngine,
        GoTConfig,
        ThoughtGraph,
        ThoughtGraphNode,
        ThoughtEdge,
        GraphAttention,
        GraphTraversalExecutor,
        GraphReasoningMode,
        solve_with_got,
    )
except ImportError as e:
    logger.warning(f"GraphOfThoughtsEngine 加载失败: {e}")
    GraphOfThoughtsEngine = None

# DivineReason 至高推理引擎 v3.0
try:
    from ._unified_reasoning_engine import (
        # 主引擎
        DivineReason,
        UnifiedReasoningEngine,  # 别名（向后兼容）
        
        # 核心组件
        SuperGraph,
        UnifiedConfig,
        UnifiedNode,
        UnifiedEdge,
        ThoughtPath,
        
        # 枚举
        NodeType,
        EdgeType,
        ReasoningMode,
        TaskComplexity,
        InsightType,
        
        # 评估器与生成器
        ReasoningMetadata,
        GraphStatistics,
        UnifiedEvaluator,
        UnifiedGenerator,
        
        # 工厂函数
        create_divine_engine,
        create_super_engine,  # 别名
        solve_with_divine,
        solve_with_super_engine,  # 别名
    )
except ImportError as e:
    logger.warning(f"DivineReason 加载失败: {e}")
    DivineReason = None
    UnifiedReasoningEngine = None

__all__ = [
    # 原有导出
    "DeepReasoningEngine",
    "ReasoningMode",
    "DeweyThinkingEngine",
    "GeodesicReasoningEngine",
    "ReasoningMemory",
    "ReverseThinkingEngine",
    "SequenceReasoningEngine",
    "StrategicReasoningEngine",
    "YangmingReasoningEngine",
    "PhaseSynchronizationCoordinator",
    # 新增导出 - Long CoT
    "LongCoTReasoningEngine",
    "LongCoTConfig",
    "BoundaryDetector",
    "InsightDetector",
    "SelfCorrector",
    "AdaptiveThinkingAllocator",
    "CheckpointManager",
    "ThoughtCheckpoint",
    "InsightMoment",
    "InsightType",
    "get_long_cot_engine",
    "create_long_cot_engine",
    "reason_with_long_cot",
    # 新增导出 - ToT
    "TreeOfThoughtsEngine",
    "ToTConfig",
    "TreeSearchCoordinator",
    "ThoughtTree",
    "ThoughtTreeNode",
    "ThoughtGenerator",
    "LLMBasedThoughtGenerator",
    "StateEvaluator",
    "DefaultStateEvaluator",
    "SearchStrategy",
    "get_tot_engine",
    "create_tot_engine",
    "solve_with_tot",
    # 新增导出 - ReAct
    "ReActEngine",
    "ReActConfig",
    "Tool",
    "ToolRegistry",
    "ToolExecutor",
    "SearchTool",
    "CalculatorTool",
    "LookupTool",
    "RetrieveTool",
    "ToolResult",
    "TAOStep",
    "TAOTrajectory",
    "ActionType",
    "get_react_engine",
    "create_react_engine",
    "reason_with_react",
    # 新增导出 - GoT
    "GraphOfThoughtsEngine",
    "GoTConfig",
    "ThoughtGraph",
    "ThoughtGraphNode",
    "ThoughtEdge",
    "GraphAttention",
    "GraphTraversalExecutor",
    "GraphReasoningMode",
    "solve_with_got",
    # 新增导出 - DivineReason 至高推理引擎 v3.0
    "DivineReason",
    "UnifiedReasoningEngine",  # 向后兼容别名
    "SuperGraph",
    "UnifiedConfig",
    "UnifiedNode",
    "UnifiedEdge",
    "ThoughtPath",
    "NodeType",
    "EdgeType",
    "ReasoningMode",
    "TaskComplexity",
    "InsightType",
    "ReasoningMetadata",
    "GraphStatistics",
    "UnifiedEvaluator",
    "UnifiedGenerator",
    "create_divine_engine",
    "create_super_engine",  # 向后兼容别名
    "solve_with_divine",
    "solve_with_super_engine",  # 向后兼容别名
]
