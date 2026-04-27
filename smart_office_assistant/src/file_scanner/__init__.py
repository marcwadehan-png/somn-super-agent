"""
文件扫描清理工具模块
用于知识库文件管理和系统清理
"""

from __future__ import annotations
from typing import Any

__all__ = ['FileScanner', 'FileCleaner']


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'FileScanner':
        from .scanner import FileScanner
        return FileScanner
    if name == 'FileCleaner':
        from .cleaner import FileCleaner
        return FileCleaner
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
