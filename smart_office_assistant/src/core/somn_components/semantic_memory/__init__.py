"""语义记忆模块 - 提供多用户语义记忆能力"""

from __future__ import annotations
from typing import Any

__all__ = ['SemanticAnalyzer', 'SemanticMemoryManager']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'SemanticAnalyzer':
        from .analyzer import SemanticAnalyzer
        return SemanticAnalyzer
    if name == 'SemanticMemoryManager':
        from .manager import SemanticMemoryManager
        return SemanticMemoryManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
