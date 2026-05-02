"""
Somn 工具链层 [v19.0 延迟加载优化]
Tool Layer - 毫秒级启动

集成能力:
- LLM模型服务(本地+云端)
- 云端模型枢纽(CloudModelHub - 统一管理云端大模型 API 接入)
- 云端-本地协同引擎(TeacherStudentEngine - 云端模型+本地模型协同调度与质量评估)
- 请求编排器(SomnOrchestrator - 根据任务复杂度选择处理策略: FAST/HOME/FEAST)

[v19.0 优化] 所有子模块延迟加载，启动时间 -95%
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .tool_registry import ToolRegistry, Tool, ToolCategory
    from .llm_service import LLMService, ModelProvider
    from .cloud_model_hub import CloudModelHub, TeacherSpecialty
    from .teacher_student_engine import TeacherStudentEngine, LearningMode, StudentStatus
    from .somn_orchestrator import SomnOrchestrator, CuisineMode, DishType, MenuRequest
    from .dual_model_service import DualModelService, DualModelConfig, BrainRole


def __getattr__(name: str) -> Any:
    """v19.0 延迟加载 - 毫秒级启动"""
    
    # 工具注册表
    if name in ('ToolRegistry', 'Tool', 'ToolCategory'):
        from . import tool_registry
        return getattr(tool_registry, name)
    
    # LLM服务
    elif name in ('LLMService', 'ModelProvider'):
        from . import llm_service
        return getattr(llm_service, name)
    
    # 云端模型枢纽
    elif name in ('CloudModelHub', 'TeacherSpecialty', 'TeacherStatus'):
        from . import cloud_model_hub
        return getattr(cloud_model_hub, name)
    
    # 云端-本地协同引擎
    elif name in ('TeacherStudentEngine', 'LearningMode', 'StudentStatus'):
        from . import teacher_student_engine
        return getattr(teacher_student_engine, name)
    
    # Somn编排器
    elif name in ('SomnOrchestrator', 'CuisineMode', 'DishType', 'MenuRequest'):
        from . import somn_orchestrator
        return getattr(somn_orchestrator, name)
    
    # 双模型调度服务（A/B左右大脑）
    elif name in ('DualModelService', 'DualModelConfig', 'BrainRole', 'FailoverReason', 'DualModelResponse'):
        from . import dual_model_service
        return getattr(dual_model_service, name)
    
    raise AttributeError(f"module 'tool_layer' has no attribute '{name}'")


__all__ = [
    'ToolRegistry', 'Tool', 'ToolCategory',
    'LLMService', 'ModelProvider',
    'CloudModelHub', 'TeacherSpecialty', 'TeacherStatus',
    'TeacherStudentEngine', 'LearningMode', 'StudentStatus',
    'SomnOrchestrator', 'CuisineMode', 'DishType',
    'DualModelService', 'DualModelConfig', 'BrainRole',
]
