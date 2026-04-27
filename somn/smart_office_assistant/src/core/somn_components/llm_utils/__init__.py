"""LLM工具模块 - 提供LLM调用和JSON解析能力"""

from __future__ import annotations
from typing import Any

__all__ = ['LLMParser']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'LLMParser':
        from .parser import LLMParser
        return LLMParser
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
