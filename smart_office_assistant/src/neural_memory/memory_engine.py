# -*- coding: utf-8 -*-
"""
Memory Engine V1 - 兼容门面层
==============================

V1 兼容接口，转发到 MemoryEngineV2。
解决 daily_learning.py 等旧代码的导入依赖。

版本: v1.0.0
创建: 2026-04-30
"""

from __future__ import annotations

from .memory_engine_v2 import (
    MemoryEngineV2 as MemoryEngine,
    Memory,
    MemoryType,
    MemoryTier,
)

__all__ = ['MemoryEngine', 'Memory', 'MemoryType', 'MemoryTier']
