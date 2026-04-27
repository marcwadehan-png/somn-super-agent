# -*- coding: utf-8 -*-
"""自然参与系统 - 枚举定义"""

from enum import Enum

class ReminderType(Enum):
    """提醒类型"""
    VALUE = "value"           # 价值提醒(里程碑达成等)
    FEATURE = "feature"       # 功能提示
    PROGRESS = "progress"     # 进度提醒
    TIP = "tip"              # 使用技巧
    INSIGHT = "insight"      # 数据洞察

class ReminderPriority(Enum):
    """提醒优先级"""
    HIGH = "high"            # 高优先级(重要里程碑)
    MEDIUM = "medium"        # 中优先级(一般提示)
    LOW = "low"              # 低优先级(可选提示)

class BehaviorType(Enum):
    """行为类型"""
    CLICK = "click"
    BROWSE = "browse"
    PURCHASE = "purchase"
    SEARCH = "search"
    SHARE = "share"
    COMMENT = "comment"
    RATING = "rating"
    FEEDBACK = "feedback"

class EngagementMetric(Enum):
    """参与度指标"""
    SESSION_DURATION = "session_duration"
    ACTION_COUNT = "action_count"
    FEATURE_ADOPTION = "feature_adoption"
    RETENTION_RATE = "retention_rate"
    SATISFACTION_SCORE = "satisfaction_score"
