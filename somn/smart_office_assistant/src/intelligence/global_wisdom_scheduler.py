# -*- coding: utf-8 -*-
"""
intelligence/ 目录 - global_wisdom_scheduler 兼容转发
=================================================

为保持向后兼容,从新位置重新导出所有接口.

新位置: src.intelligence.scheduler.global_wisdom_scheduler
原始导入: src.intelligence.global_wisdom_scheduler

版本: v1.1
日期: 2026-04-06
"""

# 转发到新位置
from src.intelligence.scheduler.global_wisdom_scheduler import (
    GlobalWisdomScheduler,
    get_scheduler,
    WisdomQuery,
    WisdomOutputFormat,
    SchedulerConfig,
    tier3_wisdom_analyze,
    tier3_quick,
)

__all__ = [
    "GlobalWisdomScheduler",
    "get_scheduler",
    "WisdomQuery",
    "WisdomOutputFormat",
    "SchedulerConfig",
    "tier3_wisdom_analyze",
    "tier3_quick",
]
