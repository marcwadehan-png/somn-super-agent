# -*- coding: utf-8 -*-
"""
Agent Components - AgentCore 模块化拆分产物

已拆分的子模块:
- intent_handler: 意图理解和分类
- file_operations: 文件扫描和清理
"""

from __future__ import annotations
from typing import Any

__all__ = [
    'IntentClassifier',
    'FileScanner',
    'FileCleaner',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'IntentClassifier':
        from .intent_handler import IntentClassifier
        return IntentClassifier
    if name == 'FileScanner':
        from .file_operations import FileScanner
        return FileScanner
    if name == 'FileCleaner':
        from .file_operations import FileCleaner
        return FileCleaner
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
