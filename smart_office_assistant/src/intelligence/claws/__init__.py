# -*- coding: utf-8 -*-
"""
Claws - Phase 4 Claw子智能体子系统
==================================

每个贤者作为一个独立的Claw子智能体，具备:
- 感知(Perception) / 推理(Reasoning) / 执行(Execution) / 反馈(Feedback) 四模块
- ReAct闭环推理（SageLoop驱动）
- Skills工具链
- NeuralMemorySystem记忆层
- Gateway多Claw协作调度

模块结构:
├── __init__.py           # 包导出
├── claw.py               # 统一入口 (ClawSystem / ClawResponse)
├── _claw_architect.py    # 核心架构 (ClawArchitect / ReActLoop / SkillsToolChain / ClawMemoryAdapter)
├── _claws_coordinator.py # 协调器 (ClawsCoordinator / GatewayRouter)
└── configs/              # 776个YAML配置文件

版本: v1.1.0
创建: 2026-04-22
"""

from .claw import (
    ClawSystem,
    ClawResponse,
    quick_ask,
)

from ._claw_architect import (
    ClawArchitect,
    ReActLoop,
    SkillsToolChain,
    ClawMemoryAdapter,
    ClawMetadata,
    ClawStatus,
    ClawSoul,
    ClawIdentity,
    CognitiveDimensions,
    ReActConfig,
    MemoryConfig,
    PersonalityProfile,
    CollaborationConfig,
    ReActStep,
    ReActResult,
    MemoryEpisode,
    load_claw_config,
    list_all_configs,
    create_claw,
    create_claws_batch,
)

from ._claws_coordinator import (
    ClawsCoordinator,
    GatewayRouter,
    RouteStrategy,
    RouteDecision,
    CoordinatorStats,
    ProcessResult,
)

from ._claw_bridge import (
    ClawSystemBridge,
    IntegrationLevel,
    IntegrationConfig,
    DispatchRequest,
    DispatchResponse,
)

from ._global_claw_scheduler import (
    GlobalClawScheduler,
    TaskTicket,
    SchedulerStats,
    WorkPoolStatus,
    DispatchMode,
    TaskPriority,
    ClawWorkMode,
    get_global_claw_scheduler,
    ensure_global_scheduler,
    quick_dispatch,
)

# V2.0 独立路由（从 _claw_router_standalone 重导出，供外部 from src.intelligence.claws import ClawRouter 使用）
try:
    from ._claw_router_standalone import (
        ClawRouter,
        get_claw_router,
        route_claw,
        ClawRouteResult,
    )
except ImportError:
    pass

__all__ = [
    # 统一入口
    "ClawSystem", "ClawResponse", "quick_ask",
    # 核心
    "ClawArchitect", "ReActLoop", "SkillsToolChain", "ClawMemoryAdapter",
    # 类型
    "ClawMetadata", "ClawStatus", "ClawSoul", "ClawIdentity",
    "CognitiveDimensions", "ReActConfig", "MemoryConfig",
    "PersonalityProfile", "CollaborationConfig",
    "ReActStep", "ReActResult", "MemoryEpisode",
    # 协调器
    "ClawsCoordinator", "GatewayRouter",
    "RouteStrategy", "RouteDecision", "CoordinatorStats", "ProcessResult",
    # 桥接器
    "ClawSystemBridge", "IntegrationLevel", "IntegrationConfig",
    "DispatchRequest", "DispatchResponse",
    # 全局调度器
    "GlobalClawScheduler", "TaskTicket", "SchedulerStats", "WorkPoolStatus",
    "DispatchMode", "TaskPriority", "ClawWorkMode",
    "get_global_claw_scheduler", "ensure_global_scheduler", "quick_dispatch",
    # 函数
    "load_claw_config", "list_all_configs", "create_claw", "create_claws_batch",
    # V2.0 路由
    "ClawRouter", "get_claw_router", "route_claw", "ClawRouteResult",
]
