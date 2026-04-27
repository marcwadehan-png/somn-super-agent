"""
神经记忆系统 [v1.0 学习系统升级]
================================

核心组件 (V3 主线):
- NeuralMemorySystem: 神经记忆系统 V3 (高性能向量索引版)
- MemoryEngine: 记忆管理引擎
- KnowledgeEngine: 知识库引擎
- ReasoningEngine: 逻辑推理引擎
- LearningEngine: 自主学习引擎
- ValidationEngine: 验证引擎

扩展组件:
- SuperNeuralMemory: 超级记忆 V5 (贤者记忆集成)
- MemoryEngineV2: 高性能 V2 (HNSW 索引)

[v1.0 学习系统升级]
1. AdaptiveStrategyEngine: 自适应策略引擎 - 根据场景自动选择策略
2. ReinforcementBridge: 强化学习桥接器 - 深度集成反馈与RL
3. MemoryLifecycleManager: 记忆生命周期管理器 - 知识衰减与进化
4. LearningPipeline: 学习流水线 - 端到端学习流程编排

[v1.0]
1. V3 升级为主线版本
2. V1 保留为兼容层 (DEPRECATED)
3. V5 超级记忆正式集成
4. 统一类型系统解决多版本冲突

版本: v1.0.0
更新: 2026-04-23
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # 统一类型
    from .memory_types import (
        MemoryTier,
        MemoryType,
        MemoryStatus,
        UnifiedMemoryTier,
    )
    
    # V3 主线
    from .neural_memory_system_v3 import (
        NeuralMemorySystemV3,
        NeuralMemoryConfig,
        MemoryOperation,
        MemoryOperationResult,
    )
    
    # V1 兼容层
    from .neural_system import NeuralMemorySystem
    
    # V5 超级记忆
    from .intelligence.engines._super_neural_memory import (
        SuperNeuralMemory,
        MemoryEntry,
        MemoryQuery,
        MemoryResult,
        MemorySource,
    )
    
    # 引擎
    from .memory_engine import MemoryEngine
    from .knowledge_engine import KnowledgeEngine
    from .reasoning_engine import ReasoningEngine, Premise, Conclusion, ReasoningType
    from .learning_engine import LearningEngine, LearningType, LearningEvent
    from .validation_engine import ValidationEngine, ValidationType, ValidationStatus, ValidationPlan, ValidationResult
    from .memory_engine_v2 import MemoryEngineV2
    
    # v1.0 学习系统升级
    from .adaptive_strategy_engine import (
        AdaptiveStrategyEngine,
        LearningScene,
        SceneAnalysis,
        StrategyPerformance,
        StrategyRecommendation,
    )
    from .reinforcement_bridge import (
        ReinforcementBridge,
        RLExperience,
        PatternUpdate,
        DQNConfig,
    )
    from .memory_lifecycle_manager import (
        MemoryLifecycleManager,
        KnowledgeEntry,
        HealthReport,
        ReviewTask,
        KnowledgeStatus,
    )
    from .learning_pipeline import (
        LearningPipeline,
        PipelineConfig,
        PipelineResult,
    )


def __getattr__(name):
    """v1.0 延迟加载 - 毫秒级启动"""
    
    # ── 统一类型 ──────────────────────────────────────────────
    if name == 'MemoryTier':
        from .memory_types import MemoryTier
        return MemoryTier
    
    elif name == 'MemoryType':
        from .memory_types import MemoryType
        return MemoryType
    
    elif name == 'MemoryStatus':
        from .memory_types import MemoryStatus
        return MemoryStatus
    
    elif name == 'UnifiedMemoryTier':
        from .memory_types import UnifiedMemoryTier
        return UnifiedMemoryTier
    
    # ── V3 主线 ──────────────────────────────────────────────
    elif name == 'NeuralMemorySystemV3':
        from . import neural_memory_system_v3
        return neural_memory_system_v3.NeuralMemorySystemV3
    
    elif name == 'NeuralMemoryConfig':
        from . import neural_memory_system_v3
        return neural_memory_system_v3.NeuralMemoryConfig
    
    elif name in ('MemoryOperation', 'MemoryOperationResult'):
        from . import neural_memory_system_v3
        return getattr(neural_memory_system_v3, name)
    
    # ── V3 别名 (向后兼容) ─────────────────────────────────────
    elif name == 'NeuralMemorySystem':
        from . import neural_memory_system_v3
        return neural_memory_system_v3.NeuralMemorySystemV3
    
    elif name == 'create_neural_system':
        from . import neural_memory_system_v3
        return lambda config=None: neural_memory_system_v3.NeuralMemorySystemV3(config)
    
    # ── V1 兼容层 (DEPRECATED) ─────────────────────────────────
    elif name == 'NeuralMemorySystemV1':
        import warnings
        warnings.warn(
            "NeuralMemorySystemV1 已弃用，请使用 NeuralMemorySystemV3",
            DeprecationWarning,
            stacklevel=2
        )
        from . import neural_system
        return neural_system.NeuralMemorySystem
    
    # ── V5 超级记忆 ──────────────────────────────────────────
    elif name == 'SuperNeuralMemory':
        from .intelligence.engines import _super_neural_memory
        return _super_neural_memory.SuperNeuralMemory
    
    elif name in ('MemoryEntry', 'MemoryQuery', 'MemoryResult', 'MemorySource'):
        from .intelligence.engines import _super_neural_memory
        return getattr(_super_neural_memory, name)
    
    elif name == 'recall':
        from .intelligence.engines import _super_neural_memory
        return _super_neural_memory.recall
    
    elif name == 'get_super_memory':
        from .intelligence.engines import _super_neural_memory
        return _super_neural_memory.get_super_memory
    
    # ── V2 高性能引擎 ─────────────────────────────────────────
    elif name == 'MemoryEngineV2':
        from . import memory_engine_v2
        return memory_engine_v2.MemoryEngineV2
    
    # ── 引擎 ─────────────────────────────────────────────────
    elif name == 'MemoryEngine':
        from . import memory_engine
        return memory_engine.MemoryEngine
    
    elif name == 'KnowledgeEngine':
        from . import knowledge_engine
        return knowledge_engine.KnowledgeEngine
    
    elif name in ('ReasoningEngine', 'Premise', 'Conclusion', 'ReasoningType'):
        from . import reasoning_engine
        return getattr(reasoning_engine, name)
    
    elif name in ('LearningEngine', 'LearningType', 'LearningEvent'):
        from . import learning_engine
        return getattr(learning_engine, name)
    
    elif name in ('ValidationEngine', 'ValidationType', 'ValidationStatus', 'ValidationPlan', 'ValidationResult'):
        from . import validation_engine
        return getattr(validation_engine, name)
    
    # ── v1.0 学习系统升级 ────────────────────────────────────
    elif name == 'AdaptiveStrategyEngine':
        from . import adaptive_strategy_engine
        return adaptive_strategy_engine.AdaptiveStrategyEngine
    
    elif name == 'ReinforcementBridge':
        from . import reinforcement_bridge
        return reinforcement_bridge.ReinforcementBridge
    
    elif name == 'MemoryLifecycleManager':
        from . import memory_lifecycle_manager
        return memory_lifecycle_manager.MemoryLifecycleManager
    
    elif name == 'LearningPipeline':
        from . import learning_pipeline
        return learning_pipeline.LearningPipeline
    
    elif name == 'PipelineConfig':
        from . import learning_pipeline
        return learning_pipeline.PipelineConfig
    
    elif name == 'PipelineResult':
        from . import learning_pipeline
        return learning_pipeline.PipelineResult
    
    elif name in ('SceneAnalysis', 'StrategyPerformance', 'StrategyRecommendation', 'LearningScene'):
        from . import adaptive_strategy_engine
        return getattr(adaptive_strategy_engine, name)
    
    elif name in ('RLExperience', 'PatternUpdate', 'DQNConfig'):
        from . import reinforcement_bridge
        return getattr(reinforcement_bridge, name)
    
    elif name in ('KnowledgeEntry', 'HealthReport', 'ReviewTask', 'KnowledgeStatus'):
        from . import memory_lifecycle_manager
        return getattr(memory_lifecycle_manager, name)
    
    # ── 统一接口 ───────────────────────────────────────────────
    elif name == 'UnifiedMemoryInterface':
        from . import unified_memory_interface
        return unified_memory_interface.UnifiedMemoryInterface
    
    elif name in ('UnifiedMemoryEntry', 'UnifiedMemoryQuery', 'UnifiedMemoryResult'):
        from . import unified_memory_interface
        return getattr(unified_memory_interface, name)
    
    elif name == 'get_unified_memory':
        from . import unified_memory_interface
        return unified_memory_interface.get_unified_memory
    
    # ── v1.0 便捷函数 ────────────────────────────────────────
    elif name == 'execute_learning_pipeline':
        from . import learning_pipeline
        return learning_pipeline.execute_learning_pipeline
    
    elif name == 'get_pipeline_status':
        from . import learning_pipeline
        return learning_pipeline.get_pipeline_status
    
    elif name == 'get_adaptive_engine':
        from . import adaptive_strategy_engine
        return adaptive_strategy_engine.get_adaptive_engine
    
    elif name == 'get_reinforcement_bridge':
        from . import reinforcement_bridge
        return reinforcement_bridge.get_reinforcement_bridge
    
    elif name == 'get_knowledge_registry':
        from . import memory_lifecycle_manager
        return memory_lifecycle_manager.get_knowledge_registry
    
    raise AttributeError(f"module 'neural_memory' has no attribute '{name}'")


__all__ = [
    # ── 版本标识 ──────────────────────────────────────────────
    '__version__',
    
    # ── V3 主线 (推荐使用) ─────────────────────────────────────
    'NeuralMemorySystem',        # V3 默认别名
    'NeuralMemorySystemV3',     # V3 显式版本
    'NeuralMemoryConfig',
    'create_neural_system',
    'MemoryOperation',
    'MemoryOperationResult',
    
    # ── V5 超级记忆 ───────────────────────────────────────────
    'SuperNeuralMemory',
    'get_super_memory',
    'recall',
    'MemoryEntry',
    'MemoryQuery',
    'MemoryResult',
    'MemorySource',
    
    # ── V2 高性能引擎 ─────────────────────────────────────────
    'MemoryEngineV2',
    
    # ── V1 兼容层 (DEPRECATED) ─────────────────────────────────
    'NeuralMemorySystemV1',
    
    # ── 引擎 ──────────────────────────────────────────────────
    'MemoryEngine',
    'KnowledgeEngine',
    'ReasoningEngine',
    'LearningEngine',
    'ValidationEngine',
    
    # ── 统一类型 ──────────────────────────────────────────────
    'MemoryTier',
    'MemoryType',
    'MemoryStatus',
    'UnifiedMemoryTier',
    
    # ── 统一接口 ──────────────────────────────────────────────
    'UnifiedMemoryInterface',
    'UnifiedMemoryEntry',
    'UnifiedMemoryQuery',
    'UnifiedMemoryResult',
    'get_unified_memory',
    
    # ── 子类型 ────────────────────────────────────────────────
    'Premise',
    'Conclusion',
    'ReasoningType',
    'LearningType',
    'LearningEvent',
    'ValidationType',
    'ValidationStatus',
    'ValidationPlan',
    'ValidationResult',
    
    # ── v1.0 学习系统升级 ─────────────────────────────────────
    'AdaptiveStrategyEngine',
    'ReinforcementBridge',
    'MemoryLifecycleManager',
    'LearningPipeline',
    'PipelineConfig',
    'PipelineResult',
    
    # ── v1.0 类型 ─────────────────────────────────────────────
    'SceneAnalysis',
    'StrategyPerformance',
    'StrategyRecommendation',
    'LearningScene',
    'RLExperience',
    'PatternUpdate',
    'DQNConfig',
    'KnowledgeEntry',
    'HealthReport',
    'ReviewTask',
    'KnowledgeStatus',
    
    # ── v1.0 便捷函数 ─────────────────────────────────────────
    'execute_learning_pipeline',
    'get_pipeline_status',
    'get_adaptive_engine',
    'get_reinforcement_bridge',
    'get_knowledge_registry',
]


__version__ = '21.0.0'
