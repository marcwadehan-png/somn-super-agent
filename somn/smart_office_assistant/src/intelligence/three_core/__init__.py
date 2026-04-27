"""
三核联动整合模块 v1.0.0
Three-Core Integration Module

整合"统一研究体系"(脑) + "神之架构V5"(躯) + "贤者系统"(魂)

架构文档: file/系统文件/三核联动架构文档_v1.0.md

主要导出:
- ThreeCoreIntegration: 三核联动整合器类
- get_three_core_integration: 获取全局单例
- ResearchLevel/ResearchDepth/ResearchDimension: 研究体系枚举
- MainLine/CrossLineSyncType/DecisionSystem: 神之架构枚举
- SagePhase: 贤者系统枚举
"""

from ._three_core_integration import (
    # 三核联动整合器
    ThreeCoreIntegration,
    get_three_core_integration,
    
    # 核心脑: 研究体系枚举
    ResearchLevel,
    ResearchDepth,
    ResearchDimension,
    ResearchDirection,
    ComplexityLevel,
    
    # 核心躯: 神之架构枚举
    MainLine,
    CrossLineSyncType,
    DecisionSystem,
    
    # 核心魂: 贤者系统枚举
    SagePhase,
    
    # 数据结构
    ResearchPlan,
    DispatchAllocation,
    WisdomInjection,
    ThreeCoreResult,
    
    # 映射矩阵
    RESEARCH_LEVEL_MAINLINE_MATRIX,
    DEPTH_PHASE_MATRIX,
    DIMENSION_SCHOOL_MATRIX,
    SAGE_MAINLINE_MATRIX,
    MAINLINE_COMPLEXITY_MATRIX,
    CROSS_SYNC_MATRIX,
)

__version__ = "v1.0.0"
__all__ = [
    # 核心类
    "ThreeCoreIntegration",
    "get_three_core_integration",
    
    # 枚举
    "ResearchLevel",
    "ResearchDepth", 
    "ResearchDimension",
    "ResearchDirection",
    "ComplexityLevel",
    "MainLine",
    "CrossLineSyncType",
    "DecisionSystem",
    "SagePhase",
    
    # 数据结构
    "ResearchPlan",
    "DispatchAllocation",
    "WisdomInjection",
    "ThreeCoreResult",
    
    # 映射矩阵
    "RESEARCH_LEVEL_MAINLINE_MATRIX",
    "DEPTH_PHASE_MATRIX",
    "DIMENSION_SCHOOL_MATRIX",
    "SAGE_MAINLINE_MATRIX",
    "MAINLINE_COMPLEXITY_MATRIX",
    "CROSS_SYNC_MATRIX",
]
