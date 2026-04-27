"""
Somn GUI - 界面层

v1.0.0: 延迟导入优化 — tray_icon 在首次使用时才加载，
避免启动时创建 QSystemTrayIcon 等 Qt 资源。
"""

from somngui.gui._types import (
    ChatMessage,
    DocumentInfo,
    FILE_ICONS,
    QuickCommand,
    QUICK_COMMANDS,
    STATUS_STYLES,
    SUPPORTED_DOC_FILES,
    SUPPORTED_TEXT_FILES,
    TOOL_ACTIONS,
)
from somngui.gui._ui_templates import (
    CHAT_AGENT_STYLE,
    CHAT_SYSTEM_STYLE,
    CHAT_USER_STYLE,
    STATUS_ERROR_STYLE,
    STATUS_READY_STYLE,
    STATUS_THINKING_STYLE,
    WELCOME_MESSAGE,
    format_agent_message,
    format_system_message,
    format_user_message,
    is_supported_doc,
    is_text_file,
)


def __getattr__(name):
    """延迟导入 tray_icon 模块 — 仅在首次访问时加载"""
    _lazy_names = {
        "TrayAwareMainWindow", "TrayIconManager", "create_tray_icon",
    }
    if name in _lazy_names:
        from somngui.gui import tray_icon
        return getattr(tray_icon, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    # types
    "ChatMessage", "DocumentInfo", "QuickCommand",
    "QUICK_COMMANDS", "TOOL_ACTIONS", "FILE_ICONS",
    "SUPPORTED_TEXT_FILES", "SUPPORTED_DOC_FILES", "STATUS_STYLES",
    # stubs
    "format_user_message", "format_agent_message", "format_system_message",
    "is_text_file", "is_supported_doc",
    "CHAT_USER_STYLE", "CHAT_AGENT_STYLE", "CHAT_SYSTEM_STYLE",
    "STATUS_READY_STYLE", "STATUS_THINKING_STYLE", "STATUS_ERROR_STYLE",
    "WELCOME_MESSAGE",
    # tray
    "TrayIconManager", "TrayAwareMainWindow", "create_tray_icon",
]
