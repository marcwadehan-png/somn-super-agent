"""
agent_core 模块级常量和类型定义
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List

# ─────────────────────────────────────────────
# 模块级可用性标志
# ─────────────────────────────────────────────

import sys
from pathlib import Path
from loguru import logger

# 导入迁移的功能模块
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__)

# Somn 主链可用性
SOMN_CORE_AVAILABLE = False
try:
    from .somn_core import get_somn_core
    SOMN_CORE_AVAILABLE = True
except Exception as e:
    logger.warning(f"SomnCore 未加载: {e}")

# 迁移功能模块可用性
MIGRATED_MODULES_AVAILABLE = False
try:
    from ml_engine.ml_core import MLEngine
    from ml_engine.predictor import ContentPredictor
    from strategy_engine.strategy_core import StrategyEngine
    from strategy_engine.execution_planner import ExecutionPlanner
    from report_engine.report_generator import ReportGenerator
    from file_scanner.scanner import FileScanner
    from file_scanner.cleaner import FileCleaner
    MIGRATED_MODULES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"部分迁移模块未加载: {e}")

# 学习系统可用性
LEARNING_SYSTEM_AVAILABLE = False
try:
    from .learning_system import LearningSystem
    from .daily_learning_task import DailyLearningTask
    LEARNING_SYSTEM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"学习系统未加载: {e}")

# 人设引擎可用性
PERSONA_AVAILABLE = False
try:
    from src.intelligence.engines.persona_core import SomnPersona
    PERSONA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"人设引擎未加载: {e}")

# ─────────────────────────────────────────────
# 类型定义
# ─────────────────────────────────────────────

@dataclass
class AgentResponse:
    """智能体响应"""
    content: str = ""
    action: Optional[str] = None
    action_params: Optional[Dict[str, Any]] = None
    confidence: float = 1.0
    # 兼容字段（handler 中使用）
    success: bool = True
    message: str = ""
    data: Optional[Dict[str, Any]] = None
