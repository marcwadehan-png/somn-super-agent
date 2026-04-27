"""AgentCore 生命周期与初始化模块 [v9.0 优化]

__all__ = [
    'agent_background_warmup',
    'agent_ensure_component',
]

已从 agent_core.py 提取，负责组件懒加载与后台预热。

[v1.0 优化] 首调优化：
- 后台预热未完成时，首调会等待（带超时）而非立即同步加载
- 减少首调卡顿，提升用户体验
"""

import threading
import time
from loguru import logger

# [v1.0 优化] 首调等待超时（秒）
_FIRST_CALL_TIMEOUT = 5.0

def agent_ensure_component(agent_core, flag_name: str, init_fn):
    """
    通用 double-check 懒加载 [v1.0 优化]

    优化策略：
    1. 如果标志已设置，直接返回（快速路径）
    2. 如果后台预热正在运行且组件即将就绪，等待而非立即加载
    3. 只有确认组件确实未初始化时才同步加载
    """
    # 快速路径：已初始化
    if getattr(agent_core, flag_name, False):
        return

    # [v1.0 优化] 检查后台预热状态
    if (hasattr(agent_core, '_bg_warmup_thread') and
        agent_core._bg_warmup_thread.is_alive()):

        # 等待后台预热完成（带超时）
        wait_start = time.time()
        while agent_core._bg_warmup_thread.is_alive():
            if time.time() - wait_start > _FIRST_CALL_TIMEOUT:
                break
            time.sleep(0.05)  # 短暂等待

        # 检查是否在等待期间已初始化
        if getattr(agent_core, flag_name, False):
            return

    # 同步初始化（兜底）
    with agent_core._init_lock:
        # 双重检查
        if getattr(agent_core, flag_name, False):
            return
        try:
            init_fn()
        except Exception as e:
            logger.warning(f"[懒加载] {flag_name} 失败: {e}")
        finally:
            setattr(agent_core, flag_name, True)

def agent_background_warmup(agent_core):
    """daemon 线程：顺序预热全部组件，不阻塞主线程."""
    try:
        logger.info("[AgentCore 后台预热] 开始...")
        _warmup_migrated_modules(agent_core)
        _warmup_learning_system(agent_core)
        _warmup_somn_core(agent_core)
        _warmup_persona(agent_core)
        _warmup_emotion_wave(agent_core)
        _warmup_hybrid_router(agent_core)
        _warmup_rag_engine(agent_core)
        logger.info("[AgentCore 后台预热] 全部组件就绪")
    except Exception as e:
        logger.error(f"[AgentCore 后台预热] 异常: {e}")

def _warmup_migrated_modules(agent_core):
    """预热迁移模块：ML引擎、策略引擎、报告生成器、文件扫描器."""
    if agent_core._migrated_initialized:
        return
    try:
        if agent_core.ml_engine is None and agent_core._ml_engine_cls:
            agent_core.ml_engine = agent_core._ml_engine_cls()
        if agent_core.content_predictor is None and agent_core._content_predictor_cls:
            agent_core.content_predictor = agent_core._content_predictor_cls()
        if agent_core.strategy_engine is None and agent_core._strategy_engine_cls:
            agent_core.strategy_engine = agent_core._strategy_engine_cls()
        if agent_core.execution_planner is None and agent_core._execution_planner_cls:
            agent_core.execution_planner = agent_core._execution_planner_cls()
        if agent_core.report_generator is None and agent_core._report_generator_cls:
            agent_core.report_generator = agent_core._report_generator_cls()
        if agent_core.file_scanner is None and agent_core._file_scanner_cls:
            agent_core.file_scanner = agent_core._file_scanner_cls()
        if agent_core.file_cleaner is None and agent_core._file_cleaner_cls:
            agent_core.file_cleaner = agent_core._file_cleaner_cls()
        logger.info("[AgentCore] 迁移模块预热完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 迁移模块预热失败: {e}")

def _warmup_learning_system(agent_core):
    """预热学习系统."""
    if agent_core._learning_initialized:
        return
    try:
        # 先初始化 learning_system (只接受 data_path 参数)
        if agent_core.learning_system is None and agent_core._learning_system_cls:
            agent_core.learning_system = agent_core._learning_system_cls()
        # 等 learning_system 就绪后再初始化 daily_learning
        if agent_core.learning_system is not None and agent_core.daily_learning is None and agent_core._daily_learning_task_cls:
            agent_core.daily_learning = agent_core._daily_learning_task_cls(
                learning_system=agent_core.learning_system
            )
        agent_core._learning_initialized = True
        logger.info("[AgentCore] 学习系统预热完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 学习系统预热失败: {e}")

def _warmup_somn_core(agent_core):
    """预热 Somn 主链."""
    if agent_core._somn_initialized:
        return
    try:
        if agent_core.somn_core is None and agent_core._get_somn_core:
            agent_core.somn_core = agent_core._get_somn_core()
        logger.info("[AgentCore] Somn 主链预热完成")
    except Exception as e:
        logger.warning(f"[AgentCore] Somn 主链预热失败: {e}")

def _warmup_persona(agent_core):
    """预热人设引擎."""
    if agent_core._persona_initialized:
        return
    try:
        if agent_core.persona is None and agent_core._somn_persona_cls:
            agent_core._init_persona_only()
        logger.info("[AgentCore] 人设引擎预热完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 人设引擎预热失败: {e}")

def _warmup_emotion_wave(agent_core):
    """预热情绪波动引擎."""
    if agent_core._emotion_initialized:
        return
    try:
        agent_core._init_emotion_wave_engine()
        logger.info("[AgentCore] 情绪波动引擎预热完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 情绪波动引擎预热失败: {e}")

def _warmup_hybrid_router(agent_core):
    """预热混合路由器."""
    if agent_core._router_initialized:
        return
    try:
        agent_core._init_hybrid_router()
        logger.info("[AgentCore] 混合路由器预热完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 混合路由器预热失败: {e}")

def _warmup_rag_engine(agent_core):
    """预热 RAG 引擎."""
    if agent_core._rag_initialized:
        return
    try:
        agent_core._init_rag_engine()
        logger.info("[AgentCore] RAG 引擎预热完成")
    except Exception as e:
        logger.warning(f"[AgentCore] RAG 引擎预热失败: {e}")

def _init_persona_only(agent_core):
    """仅初始化人设引擎（轻量级，不触发其他组件）."""
    try:
        # [v1.0.0] SomnPersona.__init__() 不接受参数
        agent_core.persona = agent_core._somn_persona_cls()
        agent_core._persona_initialized = True
        logger.info("[AgentCore] 人设引擎初始化完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 人设引擎初始化失败: {e}")

def _init_learning_system(agent_core):
    """初始化学习系统."""
    try:
        if agent_core.learning_system is None and agent_core._learning_system_cls:
            agent_core.learning_system = agent_core._learning_system_cls(
                memory_system=agent_core.memory,
                knowledge_base=agent_core.kb,
                config=agent_core.config.get('learning', {})
            )
        if agent_core.daily_learning is None and agent_core._daily_learning_task_cls:
            agent_core.daily_learning = agent_core._daily_learning_task_cls(
                learning_system=agent_core.learning_system
            )
        agent_core._learning_initialized = True
        logger.info("[AgentCore] 学习系统初始化完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 学习系统初始化失败: {e}")

def _init_somn_core(agent_core):
    """初始化 Somn 主链."""
    try:
        if agent_core.somn_core is None and agent_core._get_somn_core:
            agent_core.somn_core = agent_core._get_somn_core()
        agent_core._somn_initialized = True
        logger.info("[AgentCore] Somn 主链初始化完成")
    except Exception as e:
        logger.warning(f"[AgentCore] Somn 主链初始化失败: {e}")

def _init_emotion_wave_engine(agent_core):
    """初始化情绪波动引擎."""
    try:
        from src.intelligence.engines.emotion_wave_engine import EmotionWaveEngine
        agent_core.emotion_wave = EmotionWaveEngine()
        agent_core._emotion_initialized = True
        logger.info("[AgentCore] 情绪波动引擎初始化完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 情绪波动引擎初始化失败: {e}")

def _init_hybrid_router(agent_core):
    """初始化混合路由器."""
    try:
        from .hybrid_router import HybridRouter
        agent_core.hybrid_router = HybridRouter()
        agent_core._router_initialized = True
        logger.info("[AgentCore] 混合路由器初始化完成")
    except Exception as e:
        logger.warning(f"[AgentCore] 混合路由器初始化失败: {e}")

def _init_rag_engine(agent_core):
    """初始化 RAG 引擎."""
    try:
        from .rag_engine import RAGEngine
        agent_core.rag_engine = RAGEngine()
        agent_core._rag_initialized = True
        logger.info("[AgentCore] RAG 引擎初始化完成")
    except Exception as e:
        logger.warning(f"[AgentCore] RAG 引擎初始化失败: {e}")
