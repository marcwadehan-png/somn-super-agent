# -*- coding: utf-8 -*-
"""
智慧调度层 - scheduler 子模块
目录整理 v1.0 (2026-04-05)
提供向后兼容的 re-export
"""

import logging

logger = logging.getLogger(__name__)

# ── global_wisdom_scheduler ──────────────────────────────────────────────────
try:
    from .global_wisdom_scheduler import (
        GlobalWisdomScheduler,
        get_scheduler,
    )
except ImportError as e:
    logger.warning(f"GlobalWisdomScheduler 加载失败: {e}")
    GlobalWisdomScheduler = None
    get_scheduler = None

# ── tier3_neural_scheduler ────────────────────────────────────────────────────
try:
    from .tier3_neural_scheduler import Tier3NeuralScheduler
except ImportError as e:
    logger.warning(f"Tier3NeuralScheduler 加载失败: {e}")
    Tier3NeuralScheduler = None

# ── scheduler_optimizer ───────────────────────────────────────────────────────
try:
    from .scheduler_optimizer import SchedulerOptimizer
except ImportError as e:
    logger.warning(f"SchedulerOptimizer 加载失败: {e}")
    SchedulerOptimizer = None

# ── scheduler_optimizer_integration ──────────────────────────────────────────
try:
    from .scheduler_optimizer_integration import SchedulerOptimizerIntegration
except Exception as e:
    logger.warning(f"SchedulerOptimizerIntegration 加载失败: {e}")
    SchedulerOptimizerIntegration = None

# ── thinking_method_engine ────────────────────────────────────────────────────
try:
    from .thinking_method_engine import ThinkingMethodFusionEngine
except ImportError as e:
    logger.warning(f"ThinkingMethodFusionEngine 加载失败: {e}")
    ThinkingMethodFusionEngine = None

__all__ = [
    "GlobalWisdomScheduler",
    "get_scheduler",
    "Tier3NeuralScheduler",
    "SchedulerOptimizer",
    "SchedulerOptimizerIntegration",
    "ThinkingMethodFusionEngine",
]
