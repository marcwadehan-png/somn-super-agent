"""
__all__ = [
    'init_autonomous_agent',
    'init_cloud_learning_system',
    'init_learning_coordinator',
    'init_main_chain_integration',
]

SomnCore 智慧层初始化模块
各子系统初始化逻辑统一管理。
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def init_main_chain_integration(base_path) -> Any:
    """
    init主线集成器 -- v1.4 主线组件接入

    主线集成器职责:
    1. 协调 ParallelRouter 并形路由
    2. 协调 CrossWeaver 交叉织网
    3. 提供统一的主线执行入口
    4. 动态模式选择
    """
    try:
        from ..main_chain.main_chain_integration import get_main_chain_integration
        _main_chain_integration = get_main_chain_integration()
        status = _main_chain_integration.get_status()
        if status.get("parallel_router_available"):
            logger.info("ParallelRouter 并形路由加载成功")
        if status.get("cross_weaver_available"):
            logger.info("CrossWeaver 交叉织网加载成功")
        return _main_chain_integration
    except Exception as e:
        logger.warning(f"    ⚠️ 主线集成器加载失败: {e}")
        return None

def init_learning_coordinator(base_path) -> Any:
    """
    init学习协调器 -- v14.1.0 主线接入

    LearningCoordinator 职责:
    1. unified管理所有学习引擎
    2. 智能调度学习任务
    3. 优先级管理
    4. 资源优化
    5. 进度监控
    """
    try:
        from ..learning.coordinator import LearningCoordinator
        coordinator = LearningCoordinator(max_workers=4)
        logger.info("LearningCoordinator 加载成功")
        return coordinator
    except Exception as e:
        logger.warning(f"    ⚠️ LearningCoordinator 加载失败: {e}")
        return None

def init_autonomous_agent(base_path) -> Any:
    """
    init自主智能体 -- v14.1.0 主线接入

    AutonomousAgent 职责:
    1. 目标系统 - 长期目标追踪
    2. 调度器 - 周期性任务执行
    3. 反思引擎 - 从经验中学习
    4. 状态管理 - 智能体状态追踪
    5. 价值系统 - decision评估
    """
    try:
        from ..autonomous_core.autonomous_agent import AutonomousAgent, AgentConfig
        config = AgentConfig(
            enable_autonomous_mode=True,
            enable_yangming=True,
            check_interval=60,
            max_concurrent_tasks=3,
            storage_path=str(base_path / "data/autonomous")
        )
        agent = AutonomousAgent(config=config)
        logger.info("AutonomousAgent 加载成功")
        return agent
    except Exception as e:
        logger.warning(f"    ⚠️ AutonomousAgent 加载失败: {e}")
        return None

def init_cloud_learning_system(base_path, llm_service, print_fn=print) -> dict:
    """
    init云端老师-本地学生-编排器体系 -- v14.0.0 全局打通

    核心理念:
    - 云端大模型 = 老师:知识渊博,视野开阔,擅长解答,但不懂 Somn
    - 本地大模型 = 学生:正在学习,效率高,成本低,隐私好
    - Somn = 教务主任:调配资源,决定何时问老师,何时让学生答,评估学习效果

    三模块联动:
    - CloudModelHub:管理所有云端模型 API
    - TeacherStudentEngine:协调师生学习过程
    - SomnOrchestrator:智能编排,决定烹饪模式
    """
    print_fn("  📦 init云端老师-本地学生体系...")

    result = {}

    # CloudModelHub
    try:
        from ..tool_layer.cloud_model_hub import CloudModelHub
        cloud_model_hub = CloudModelHub(str(base_path / "data/cloud_hub"))
        teacher_count = len(cloud_model_hub.list_teachers())
        print_fn(f"    ✅ CloudModelHub 加载成功({teacher_count} 位预设老师)")
        result["cloud_model_hub"] = cloud_model_hub
    except Exception as e:
        logger.warning(f"    ⚠️ CloudModelHub 加载失败: {e}")
        result["cloud_model_hub"] = None

    # TeacherStudentEngine
    try:
        from ..tool_layer.teacher_student_engine import TeacherStudentEngine
        teacher_student_engine = TeacherStudentEngine(
            base_path=str(base_path / "data/teacher_student"),
            cloud_hub=result["cloud_model_hub"],
            llm_service=llm_service,
        )
        perf = teacher_student_engine.student_performance
        total = perf.get("total_tasks", 0)
        avg_q = perf.get("avg_quality", 0.0)
        print_fn(f"    ✅ TeacherStudentEngine 加载成功(历史任务{total}个,平均质量{avg_q:.2f})")
        result["teacher_student_engine"] = teacher_student_engine
    except Exception as e:
        logger.warning(f"    ⚠️ TeacherStudentEngine 加载失败: {e}")
        result["teacher_student_engine"] = None

    # SomnOrchestrator
    try:
        from ..tool_layer.somn_orchestrator import SomnOrchestrator
        somn_orchestrator = SomnOrchestrator(
            cloud_hub=result["cloud_model_hub"],
            teacher_student_engine=result["teacher_student_engine"],
            llm_service=llm_service,
        )
        print_fn("    ✅ SomnOrchestrator 加载成功(3种烹饪模式就绪)")
        result["somn_orchestrator"] = somn_orchestrator
    except Exception as e:
        logger.warning(f"    ⚠️ SomnOrchestrator 加载失败: {e}")
        result["somn_orchestrator"] = None

    print_fn("  📦 云端老师-本地学生体系init完成")
    return result
