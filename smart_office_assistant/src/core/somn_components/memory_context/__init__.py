"""记忆上下文模块 - 提供上下文检索和缓存能力"""

from __future__ import annotations
from typing import Any

__all__ = ['MemoryRetriever', 'SearchCache']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'MemoryRetriever':
        from .retrieval import MemoryRetriever
        return MemoryRetriever
    if name == 'SearchCache':
        from .cache import SearchCache
        return SearchCache
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
