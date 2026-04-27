"""
智能体核心 - Agent Core
整合记忆,知识库,ML引擎,strategy引擎,报告generate和文件扫描能力
实现持续学习和成长的超级智能体

拆分后结构:
- _agent_types.py: 模块级常量和类型定义
- agent_core.py: AgentCore 主类
"""

import logging
import json
import re
import sys
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable

from loguru import logger

# 从拆分模块导入常量和类型
from ._agent_types import (
    AgentResponse,
    SOMN_CORE_AVAILABLE,
    MIGRATED_MODULES_AVAILABLE,
    LEARNING_SYSTEM_AVAILABLE,
    PERSONA_AVAILABLE,
)

# 从拆分模块导入
from ._agent_lifecycle import (
    agent_ensure_component as _ensure_component,
    agent_background_warmup as _background_warmup,
)
from ._agent_input_processor import (
    agent_process_input,
)
from ._agent_action_executor import (
    agent_execute_action,
    agent_extract_task_response,
)
from ._agent_learning import (
    agent_run_daily_learning,
    agent_get_learning_summary,
    agent_trigger_learning,
    agent_get_learning_status,
    agent_learn_from_interaction,
)

from .memory_system import MemorySystem, MemoryEntry
from .knowledge_base import KnowledgeBase

# 延迟导入 SomnCore(避免循环依赖)
_get_somn_core = None
if SOMN_CORE_AVAILABLE:
    try:
        from .somn_core import get_somn_core as _get_somn_core
    except Exception as e:
        logger.debug(f"SomnCore导入失败: {e}")

# 延迟导入迁移模块
_ml_engine_cls = None
_content_predictor_cls = None
_strategy_engine_cls = None
_execution_planner_cls = None
_report_generator_cls = None
_file_scanner_cls = None
_file_cleaner_cls = None
if MIGRATED_MODULES_AVAILABLE:
    try:
        from ml_engine.ml_core import MLEngine as _ml_engine_cls
        from ml_engine.predictor import ContentPredictor as _content_predictor_cls
        from strategy_engine.strategy_core import StrategyEngine as _strategy_engine_cls
        from strategy_engine.execution_planner import ExecutionPlanner as _execution_planner_cls
        from report_engine.report_generator import ReportGenerator as _report_generator_cls
        from file_scanner.scanner import FileScanner as _file_scanner_cls
        from file_scanner.cleaner import FileCleaner as _file_cleaner_cls
    except Exception as e:
        logger.debug(f"迁移模块导入失败: {e}")

# 延迟导入学习系统
_learning_system_cls = None
_daily_learning_task_cls = None
if LEARNING_SYSTEM_AVAILABLE:
    try:
        from .learning_system import LearningSystem as _learning_system_cls
        from .daily_learning_task import DailyLearningTask as _daily_learning_task_cls
    except Exception as e:
        logger.debug(f"学习系统导入失败: {e}")

# 延迟导入人设引擎
_somn_persona_cls = None
if PERSONA_AVAILABLE:
    try:
        from src.intelligence.engines.persona_core import SomnPersona as _somn_persona_cls
    except Exception as e:
        logger.debug(f"人设引擎导入失败: {e}")

logger = logging.getLogger(__name__)
class AgentCore:
    """
    智能体核心 - 超级智能体
    
    职责:
    1. 理解用户输入和意图
    2. 调用记忆系统获取上下文
    3. 检索相关知识
    4. 生成响应
    5. 执行操作(文档生成、文件扫描、策略生成等)
    6. ML预测和内容优化
    7. 从交互中持续学习
    
    本类已重构为委托模式，核心逻辑委托至以下子模块:
    - _agent_lifecycle.py: 生命周期与初始化
    - _agent_input_processor.py: 输入处理与意图识别
    - _agent_action_executor.py: 动作执行
    - _agent_learning.py: 学习系统
    """
    
    def __init__(
        self,
        memory_system: MemorySystem,
        knowledge_base: KnowledgeBase,
        config: Optional[Dict[str, Any]] = None
    ):
        self.memory = memory_system
        self.kb = knowledge_base
        self.config = config or {}

        # 会话上下文
        self.session_context: Dict[str, Any] = {
            'start_time': datetime.now(),
            'interaction_count': 0,
            'current_topic': None,
            'user_preferences': {}
        }

        # 学习状态
        self.learning_enabled = self.config.get('auto_learn', True)

        # Tier 0: 零同步开销 - 全部组件占位为 None
        self.ml_engine = None
        self.content_predictor = None
        self.strategy_engine = None
        self.execution_planner = None
        self.report_generator = None
        self.file_scanner = None
        self.file_cleaner = None
        self.learning_system = None
        self.daily_learning = None
        self.somn_core = None
        self.persona = None
        self.emotion_wave = None
        self.hybrid_router = None
        self.rag_engine = None

        # 线程安全
        self._init_lock = threading.Lock()

        # 懒加载完成标志
        self._migrated_initialized = False
        self._learning_initialized = False
        self._somn_initialized = False
        self._persona_initialized = False
        self._emotion_initialized = False
        self._router_initialized = False
        self._rag_initialized = False

        # [v1.0.0] 将模块级延迟导入的类引用复制到实例属性，供后台预热线程访问
        self._ml_engine_cls = _ml_engine_cls
        self._content_predictor_cls = _content_predictor_cls
        self._strategy_engine_cls = _strategy_engine_cls
        self._execution_planner_cls = _execution_planner_cls
        self._report_generator_cls = _report_generator_cls
        self._file_scanner_cls = _file_scanner_cls
        self._file_cleaner_cls = _file_cleaner_cls
        self._learning_system_cls = _learning_system_cls
        self._daily_learning_task_cls = _daily_learning_task_cls
        self._somn_persona_cls = _somn_persona_cls
        self._get_somn_core = _get_somn_core

        # 启动后台预热 daemon
        self._bg_warmup_thread = threading.Thread(
            target=self._background_warmup,
            name="agent_bg_warmup",
            daemon=True,
        )
        self._bg_warmup_thread.start()

        logger.info("AgentCore init 完成(Tier0 零阻塞, 全部组件后台预热中)")

    # ─────────────────────────────────────────────
    # 后台预热入口 (委托自 _agent_lifecycle)
    # ─────────────────────────────────────────────
    def _background_warmup(self) -> None:
        """daemon 线程：顺序预热全部组件，不阻塞主线程."""
        return _background_warmup(self)

    def _ensure_component(self, flag_name: str, init_fn: Callable) -> None:
        """通用 double-check 懒加载."""
        return _ensure_component(self, flag_name, init_fn)

    # ─────────────────────────────────────────────
    # Warmup 方法 (委托自 _agent_lifecycle)
    # ─────────────────────────────────────────────
    def _warmup_migrated_modules(self) -> None:
        from ._agent_lifecycle import _warmup_migrated_modules
        return _warmup_migrated_modules(self)

    def _warmup_learning_system(self) -> None:
        from ._agent_lifecycle import _warmup_learning_system
        return _warmup_learning_system(self)

    def _warmup_somn_core(self) -> None:
        from ._agent_lifecycle import _warmup_somn_core
        return _warmup_somn_core(self)

    def _warmup_persona(self) -> None:
        from ._agent_lifecycle import _warmup_persona
        return _warmup_persona(self)

    def _warmup_emotion_wave(self) -> None:
        from ._agent_lifecycle import _warmup_emotion_wave
        return _warmup_emotion_wave(self)

    def _warmup_hybrid_router(self) -> None:
        from ._agent_lifecycle import _warmup_hybrid_router
        return _warmup_hybrid_router(self)

    def _warmup_rag_engine(self) -> None:
        from ._agent_lifecycle import _warmup_rag_engine
        return _warmup_rag_engine(self)

    # ─────────────────────────────────────────────
    # Init 方法 (委托自 _agent_lifecycle)
    # ─────────────────────────────────────────────
    def _init_persona_only(self) -> None:
        from ._agent_lifecycle import _init_persona_only
        return _init_persona_only(self)

    def _init_learning_system(self) -> None:
        from ._agent_lifecycle import _init_learning_system
        return _init_learning_system(self)

    def _init_somn_core(self) -> None:
        from ._agent_lifecycle import _init_somn_core
        return _init_somn_core(self)

    def _init_emotion_wave_engine(self) -> None:
        from ._agent_lifecycle import _init_emotion_wave_engine
        return _init_emotion_wave_engine(self)

    def _init_hybrid_router(self) -> None:
        from ._agent_lifecycle import _init_hybrid_router
        return _init_hybrid_router(self)

    def _init_rag_engine(self) -> None:
        from ._agent_lifecycle import _init_rag_engine
        return _init_rag_engine(self)

    # ─────────────────────────────────────────────
    # 后台任务 (委托自 _agent_lifecycle)
    # ─────────────────────────────────────────────
    def _background_index(self) -> None:
        """RAG 后台索引 (由 _init_rag_engine 调用)."""
        if self.rag_engine is None:
            return
        try:
            indexed = self.rag_engine.index_directory(
                str(Path(__file__).parent.parent.parent / "文学研究"),
                patterns=['*.md']
            )
            if indexed > 0:
                logger.info(f"[RAG后台] 异步索引完成: {indexed} 篇新增文档")
        except Exception as e:
            logger.warning(f"[RAG后台] 异步索引失败: {e}")

    def _run_somn_chain(self, user_input: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """调用 Somn 主链处理复杂分析/策略任务."""
        if self.somn_core is None:
            return None
        
        # [修复上下文传递] 构建完整的上下文传递给SomnCore
        # 合并外部context和内部session_context
        session_info = self.session_context or {}
        
        # 从记忆系统获取长期记忆
        long_term_memory = []
        if self.memory:
            try:
                memory_results = self.memory.search_memories(
                    query=user_input,
                    memory_type=None,  # 搜索所有类型
                    limit=10
                )
                long_term_memory = [
                    {
                        "content": m.content,
                        "type": m.memory_type,
                        "importance": m.importance,
                        "timestamp": m.timestamp.isoformat() if hasattr(m, 'timestamp') else ""
                    }
                    for m in memory_results
                ]
            except Exception as e:
                logger.debug(f"长期记忆加载失败: {e}")
                long_term_memory = []
        
        somn_context = {
            "recent_memories": context.get("recent_memories", ""),
            "relevant_knowledge": context.get("relevant_knowledge", []),
            "current_topic": context.get("current_topic"),
            "long_term_memory": long_term_memory,  # [修复] 传递完整长期记忆
            "user_preferences": session_info.get("user_preferences", context.get("user_preferences", {})),
            "industry": context.get("industry", session_info.get("current_industry")),
            "agent_session": {
                "interaction_count": session_info.get("interaction_count", 0),
                "current_topic": session_info.get("current_topic"),
                "start_time": session_info.get("start_time", "").isoformat() if hasattr(session_info.get("start_time", ""), "isoformat") else str(session_info.get("start_time", ""))
            }
        }
        return self.somn_core.run_agent_task(user_input, context=somn_context)

    # ─────────────────────────────────────────────
    # 主入口 (委托自 _agent_input_processor)
    # ─────────────────────────────────────────────
    def process_input(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> 'AgentResponse':
        """处理用户输入."""
        return agent_process_input(self, user_input, context)

    # ─────────────────────────────────────────────
    # 学习系统 (委托自 _agent_learning)
    # ─────────────────────────────────────────────
    def _run_daily_learning(self) -> None:
        """执行每日学习."""
        return agent_run_daily_learning(self)

    def get_learning_summary(self) -> str:
        """获取学习摘要."""
        result = agent_get_learning_summary(self)
        return result.get('message', '学习系统未启用')

    def trigger_learning(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """触发学习."""
        return agent_trigger_learning(self, topic)

    def get_learning_status(self) -> Dict[str, Any]:
        """获取学习状态."""
        return agent_get_learning_status(self)

    def _learn_from_interaction(self, user_input: str, intent: Dict, response: Any) -> None:
        """从交互中学习."""
        return agent_learn_from_interaction(self, user_input, intent, response)

    # ─────────────────────────────────────────────
    # 工具方法 (公共 API)
    # ─────────────────────────────────────────────
    def scan_directory(self, path: str = '.', max_depth: int = 3) -> Dict[str, Any]:
        """扫描目录."""
        if self.file_scanner:
            return self.file_scanner.scan(path, max_depth)
        return {'success': False, 'error': '文件扫描器未初始化'}

    def generate_strategy(self, topic: str, context: Dict = None) -> Dict[str, Any]:
        """生成增长策略."""
        if self.strategy_engine:
            return self.strategy_engine.generate(topic, context or {})
        return {'success': False, 'error': '策略引擎未初始化'}

    def predict_content_performance(self, content: str, platform: str = 'auto') -> Dict[str, Any]:
        """预测内容表现."""
        if self.content_predictor:
            return self.content_predictor.predict(content, platform)
        return {'success': False, 'error': '预测器未初始化'}

    def generate_markdown_report(self, title: str, sections: List[Dict]) -> str:
        """生成 Markdown 报告."""
        if self.report_generator:
            return self.report_generator.generate_markdown(title, sections)
        return f"# {title}\n\n报告生成器未初始化"

    # ─────────────────────────────────────────────
    # OpenClaw 开放抓取接口 (v1.0.1 集成激活)
    # ─────────────────────────────────────────────

    @property
    def openclaw(self) -> Optional['OpenClawCore']:
        """获取 OpenClaw 核心引擎（通过 SomnCore 懒加载）"""
        if self.somn_core:
            return self.somn_core.openclaw
        return None

    @property
    def claw_system(self) -> Optional['ClawSystemBridge']:
        """获取 ClawSystemBridge 桥接器（通过 SomnCore 懒加载）"""
        if self.somn_core:
            return self.somn_core.claw_system
        return None

    def fetch_external_knowledge(self, query: str, source_names: list = None) -> list:
        """通过 OpenClaw 从外部数据源抓取知识."""
        if self.somn_core:
            return self.somn_core.fetch_external_knowledge(query, source_names)
        return []

    def inject_knowledge_to_claws(self, query: str, claw_names: list = None) -> dict:
        """抓取外部知识并注入到指定 Claw 的记忆."""
        if self.somn_core:
            return self.somn_core.inject_knowledge_to_claws(query, claw_names)
        return {"error": "SomnCore not initialized"}

    def submit_claw_feedback(self, feedback_data: dict) -> dict:
        """提交用户反馈到 OpenClaw 反馈学习系统."""
        if self.somn_core:
            return self.somn_core.submit_claw_feedback(feedback_data)
        return {"error": "SomnCore not initialized"}

    def get_openclaw_status(self) -> dict:
        """获取 OpenClaw + ClawBridge 的完整状态."""
        if self.somn_core:
            return self.somn_core.get_openclaw_status()
        return {"openclaw_enabled": False, "reason": "SomnCore not initialized"}

# ───────────────────────────────────────────────────────────────
# 模块导出
# ───────────────────────────────────────────────────────────────
__all__ = [
    'AgentCore',
    'AgentResponse',
]
