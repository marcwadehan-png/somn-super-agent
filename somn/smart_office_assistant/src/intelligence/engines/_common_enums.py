# -*- coding: utf-8 -*-
"""
intelligence/engines 通用枚举定义
Common enumerations shared across intelligence engines.

迁移自:
  - main_chain/cross_weaver.py (FeedbackType)
  - intelligence/engines/research_phase_manager.py (TaskStatus)
"""

from enum import Enum


class FeedbackType(Enum):
    """反馈类型 - 跨模块通用"""
    POSITIVE = "positive"      # 正向反馈（增强）
    NEGATIVE = "negative"      # 负向反馈（抑制）
    NEUTRAL = "neutral"        # 中性反馈（信息）
    ADAPTIVE = "adaptive"       # 自适应反馈（调节）


class TaskStatus(Enum):
    """任务状态 - 跨模块通用"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# ============================================================
# 注意: StrategyType 未纳入此文件
# 原因: 项目中存在4处 StrategyType 定义，语义各不相同:
#   1. military_strategy/_ms_enums.py   — 三十六计策略
#   2. de_zhi_planner.py                — 德治战略
#   3. cross_scale_thinking_engine/_cst_strategy.py — 跨尺度策略
#   4. growth_engine/growth_strategy.py — AARRR增长策略
# 这些同名不同义的枚举应保持在各自模块内，不应强制合并。
# ============================================================
