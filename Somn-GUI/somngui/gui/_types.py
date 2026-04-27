# -*- coding: utf-8 -*-
"""Somn GUI - 类型定义和常量

纯 dataclass / Enum 定义，零 Qt 依赖，可被所有 GUI 子模块安全导入。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# 快捷命令
# ---------------------------------------------------------------------------

class QuickCommand(Enum):
    """快捷命令枚举"""
    SUMMARIZE = "总结文档"
    GENERATE_REPORT = "生成报告"
    ANALYZE_DATA = "分析数据"
    CREATE_OUTLINE = "创建大纲"
    SCAN_FILES = "扫描文件"
    CREATE_STRATEGY = "制定策略"
    PREDICT_EFFECT = "预测效果"


QUICK_COMMANDS: List[str] = [c.value for c in QuickCommand]


# ---------------------------------------------------------------------------
# 工具菜单动作  (label, action_id)
# ---------------------------------------------------------------------------

TOOL_ACTIONS: Dict[str, tuple[str, str]] = {
    "scan_files":   ("🔍 扫描文件",   "scan_files"),
    "clean_files":  ("🧹 清理文件",   "clean_files"),
    "gen_report":   ("📊 生成报告",   "generate_report"),
    "gen_strategy": ("🎯 制定策略",   "create_strategy"),
    "index_files":  ("📁 索引文件",   "index_files"),
    "kb_stats":     ("📚 知识库统计", "kb_stats"),
}


# ---------------------------------------------------------------------------
# 文件类型支持
# ---------------------------------------------------------------------------

SUPPORTED_TEXT_FILES: List[str] = [
    '.txt', '.md', '.py', '.js', '.html', '.css',
    '.json', '.yaml', '.yml', '.xml',
]

SUPPORTED_DOC_FILES: List[str] = [
    '.docx', '.pdf', '.pptx', '.ppt', '.xlsx', '.xls', '.csv',
]


# ---------------------------------------------------------------------------
# 文件树图标（Qt Style StandardPixmap 名称）
# ---------------------------------------------------------------------------

FILE_ICONS: Dict[str, str] = {
    "folder": "SP_DirIcon",
    "file":   "SP_FileIcon",
    "home":   "SP_DirHomeIcon",
}


# ---------------------------------------------------------------------------
# 状态栏样式配置
# ---------------------------------------------------------------------------

STATUS_STYLES: Dict[str, Dict[str, str]] = {
    "ready":    {"bg": "#d4edda", "color": "#155724", "text": "就绪"},
    "thinking": {"bg": "#fff3cd", "color": "#856404", "text": "思考中..."},
    "error":    {"bg": "#f8d7da", "color": "#721c24", "text": "错误"},
}


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

@dataclass
class ChatMessage:
    """聊天消息"""
    role: str           # "user" | "agent" | "system"
    content: str
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentInfo:
    """文档信息"""
    title: str
    content: str
    file_path: Optional[str] = None
    modified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
