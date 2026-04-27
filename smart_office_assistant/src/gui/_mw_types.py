# -*- coding: utf-8 -*-
"""主窗口 - 类型定义和常量"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class QuickCommand(Enum):
    """快捷命令枚举"""
    SUMMARIZE = "总结文档"
    GENERATE_REPORT = "生成报告"
    ANALYZE_DATA = "分析数据"
    CREATE_OUTLINE = "创建大纲"
    SCAN_FILES = "扫描文件"
    CREATE_STRATEGY = "制定策略"
    PREDICT_EFFECT = "预测效果"

@dataclass
class ChatMessage:
    """聊天消息"""
    role: str  # "user", "agent", "system"
    content: str
    timestamp: str = ""

@dataclass
class DocumentInfo:
    """文档信息"""
    title: str
    content: str
    file_path: Optional[str] = None
    modified: bool = False

# 快速命令列表
QUICK_COMMANDS = [
    "总结文档", "生成报告", "分析数据", "创建大纲",
    "扫描文件", "制定策略", "预测效果"
]

# 工具菜单动作
TOOL_ACTIONS = {
    "scan_files": ("🔍 扫描文件", "scan_files"),
    "clean_files": ("🧹 清理文件", "clean_files"),
    "gen_report": ("📊 生成报告", "generate_report"),
    "gen_strategy": ("🎯 制定策略", "create_strategy"),
    "index_files": ("📁 索引文件", "index_files"),
    "kb_stats": ("📚 知识库统计", "kb_stats"),
}

# 文件树图标映射
FILE_ICONS = {
    "folder": "SP_DirIcon",
    "file": "SP_FileIcon",
    "home": "SP_DirHomeIcon",
}

# 支持的文件类型
SUPPORTED_TEXT_FILES = [
    '.txt', '.md', '.py', '.js', '.html', '.css',
    '.json', '.yaml', '.yml', '.xml'
]

SUPPORTED_DOC_FILES = ['.docx', '.pdf', '.pptx', '.ppt', '.xlsx', '.xls', '.csv']

# 状态栏样式
STATUS_STYLES = {
    "ready": {
        "bg": "#d4edda",
        "color": "#155724",
        "text": "就绪"
    },
    "thinking": {
        "bg": "#fff3cd",
        "color": "#856404",
        "text": "思考中..."
    },
    "error": {
        "bg": "#f8d7da",
        "color": "#721c24",
        "text": "错误"
    }
}
