"""
NeuralMemory — Somn 三层神经记忆架构 [v6.2.0]
================================================

[品牌定位]
NeuralMemory 是 Somn 的三层神经记忆系统，品牌名称即为 NeuralMemory。
核心概念：
  - 三层记忆架构 (书架): 记忆的分层存储体系 (MemoryTier ↔ 藏书阁甲乙丙丁分级)
  - 藏书阁 (记忆仓库): ImperialLibrary，记忆的持久化仓库
  - NeuralMemory (管理工具): 门面类，仓库的统一操作入口
  - 藏书阁工作人员 (主管): LibraryStaffRegistry，Claw贤者职务架构
  - 学习系统 (管理制度): LearningReplayBuffer，出入库管理体系
  - 知识域格子 (知识库): DomainNexus，与记忆系统打通

核心组件:
- NeuralMemorySystem: 神经记忆系统 (高性能向量索引版)
- NeuralMemory: 三层神经记忆架构统一门面
- MemoryEngine: 记忆管理引擎
- KnowledgeEngine: 知识库引擎
- ReasoningEngine: 逻辑推理引擎
- LearningEngine: 自主学习引擎
- ValidationEngine: 验证引擎

扩展组件:
- SuperNeuralMemory: 超级记忆 (贤者记忆集成)
- MemoryEngineV2: 高性能引擎 (HNSW 索引)

[快速加载模式 - 2026-04-28]
1. NeuralMemoryFastLoader: 预加载+懒加载混合架构，毫秒级启动
2. FastLoadConfig: 组件级加载策略配置（EAGER/LAZY/ON_DEMAND）
3. LoadTracker: 组件加载状态追踪与性能监控
4. LazyLoader: 并发安全的懒加载管理器
5. NeuralMemory: 门面类支持快速加载模式（use_fast_load=True）

[学习系统升级]
1. AdaptiveStrategyEngine: 自适应策略引擎 - 根据场景自动选择策略
2. ReinforcementBridge: 强化学习桥接器 - 深度集成反馈与RL
3. MemoryLifecycleManager: 记忆生命周期管理器 - 知识衰减与进化
4. LearningPipeline: 学习流水线 - 端到端学习流程编排

版本: v6.2.0
更新: 2026-04-29
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
    
    # V5 超级记忆 (路径修正: src/intelligence/engines/)
    from src.intelligence.engines._super_neural_memory import (
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
    
    # v2.0 学习系统升级
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
    """v20.0 延迟加载 - 毫秒级启动"""
    
    # ── v7.0 统一入口 (优先) ────────────────────────────────
    # 注意: v2 的 NeuralMemory/get_neural_memory 已迁移到 v7
    if name in ('NeuralMemory', 'get_neural_memory'):
        from . import neural_memory_v7
        return getattr(neural_memory_v7, name)
    
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
        # v7 独立配置，不依赖有问题的 neural_memory_system_v3
        from . import neural_memory_v7
        return neural_memory_v7.NeuralMemoryConfig
    
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
        from src.intelligence.engines import _super_neural_memory
        return _super_neural_memory.SuperNeuralMemory
    
    elif name in ('MemoryEntry', 'MemoryQuery', 'MemoryResult', 'MemorySource'):
        from src.intelligence.engines import _super_neural_memory
        return getattr(_super_neural_memory, name)
    
    elif name == 'recall':
        from src.intelligence.engines import _super_neural_memory
        return _super_neural_memory.recall
    
    elif name == 'get_super_memory':
        from src.intelligence.engines import _super_neural_memory
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
    
    # ── v2.0 学习系统升级 ────────────────────────────────────
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
    
    # ── v2.0 便捷函数 ────────────────────────────────────────
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
    
    # ── v22.0 快速加载 ────────────────────────────────────────
    elif name == 'FastLoadConfig':
        from .neural_memory_fast_load import FastLoadConfig
        return FastLoadConfig
    
    elif name == 'LoadStrategy':
        from .neural_memory_fast_load import LoadStrategy
        return LoadStrategy
    
    elif name == 'LoadTracker':
        from .neural_memory_fast_load import LoadTracker
        return LoadTracker
    
    elif name == 'LazyLoader':
        from .neural_memory_fast_load import LazyLoader
        return LazyLoader
    
    elif name == 'NeuralMemoryFastLoader':
        from .neural_memory_fast_load import NeuralMemoryFastLoader
        return NeuralMemoryFastLoader
    
    elif name == 'get_fast_loader':
        from .neural_memory_fast_load import get_fast_loader
        return get_fast_loader
    
    elif name == 'get_load_tracker':
        from .neural_memory_fast_load import get_load_tracker
        return get_load_tracker
    
    elif name == 'quick_load_summary':
        from .neural_memory_fast_load import quick_load_summary
        return quick_load_summary
    
    elif name == 'preload_memory_components':
        from .neural_memory_fast_load import preload_memory_components
        return preload_memory_components
    
    # ── v7.0 统一架构 (DigitalBrain + NeuralMemory 整合) ──────────────
    elif name == 'NeuralMemory':
        # v7.0 优先返回新统一架构
        from . import neural_memory_v7
        return neural_memory_v7.NeuralMemory

    elif name == 'get_neural_memory':
        # v7.0 优先返回新统一架构
        from . import neural_memory_v7
        return neural_memory_v7.get_neural_memory

    elif name == 'NeuralMemoryConfig':
        # v7 独立配置，不依赖有问题的 neural_memory_system_v3
        from . import neural_memory_v7
        return neural_memory_v7.NeuralMemoryConfig

    elif name == 'ThinkResult':
        from . import neural_memory_v7
        return neural_memory_v7.ThinkResult

    elif name == 'DigitalStrategy':
        from . import digital_strategy
        return digital_strategy.DigitalStrategy

    elif name == 'NeuralExecutor':
        from . import neural_executor
        return neural_executor.NeuralExecutor

    elif name in ('MemoryLevel', 'BrainState', 'StrategyThought', 'StrategyEvolution', 'StrategyHealth', 'StrategyConfig'):
        from . import digital_strategy
        return getattr(digital_strategy, name)

    elif name in ('ExecutorConfig', 'ExecutorOperation', 'ExecutorHealth'):
        from . import neural_executor
        return getattr(neural_executor, name)

    raise AttributeError(f"module 'neural_memory' has no attribute '{name}'")


__all__ = [
    # ── v7.0 统一入口（优先）───────────────────
    # NeuralMemory / get_neural_memory 由 __getattr__ 提供 (v7.0)

    # ── 版本标识 ──────────────────────────────────────────────
    '__version__',
    
    # ── V3 主线 (推荐使用) ─────────────────────────────────────
    'NeuralMemorySystem',        # V3 默认别名
    'NeuralMemorySystemV3',     # V3 显式版本
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
    
    # ── v2.0 学习系统升级 ─────────────────────────────────────
    'AdaptiveStrategyEngine',
    'ReinforcementBridge',
    'MemoryLifecycleManager',
    'LearningPipeline',
    'PipelineConfig',
    'PipelineResult',
    
    # ── v2.0 类型 ─────────────────────────────────────────────
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
    
    # ── v2.0 便捷函数 ─────────────────────────────────────────
    'execute_learning_pipeline',
    'get_pipeline_status',
    'get_adaptive_engine',
    'get_reinforcement_bridge',
    'get_knowledge_registry',
    
    # ── v22.0 快速加载模块 ────────────────────────────────────
    'FastLoadConfig',
    'LoadStrategy',
    'LoadTracker',
    'LazyLoader',
    'NeuralMemoryFastLoader',
    'get_fast_loader',
    'get_load_tracker',
    'quick_load_summary',
    'preload_memory_components',
    
    # ── v7.0 统一架构 (DigitalBrain + NeuralMemory 整合) ──────────────
    # 注意: NeuralMemory/NeuralMemoryConfig等类通过 __getattr__ 懒加载
    # 不在 __all__ 中直接列出，避免 "from neural_memory import X" 失败
    # 使用: from neural_memory import NeuralMemory (走 __getattr__)
]


__version__ = 'v7.0'
