"""Somn GUI - 资源模块

提供主题切换、QSS 加载等资源管理功能。
自动扫描 resources/ 目录下的 .qss 文件作为可用主题。
"""

from __future__ import annotations

import ctypes
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QApplication

# 资源目录
_RESOURCES_DIR = Path(__file__).parent.resolve()

# 主题名称 → QSS 文件（自动扫描补充）
_THEME_MAP: dict[str, str] = {
    "light": "light.qss",
    "dark": "dark.qss",
}

# 自动扫描所有 .qss 文件
for _qss in _RESOURCES_DIR.glob("*.qss"):
    _name = _qss.stem  # e.g., "ocean_blue"
    if _name not in _THEME_MAP:
        _THEME_MAP[_name] = _qss.name

# 主题名称 → 显示标签（用于菜单）
_THEME_LABELS = {
    "light": "☀️ 亮色",
    "dark": "🌙 暗色",
    "ocean_blue": "🌊 海洋蓝",
    "forest_green": "🌲 森林绿",
    "royal_purple": "👑 皇家紫",
}


def detect_system_dark_mode() -> bool:
    """检测操作系统是否处于深色模式"""
    import platform
    system = platform.system()
    if system == "Windows":
        try:
            reg = ctypes.windll.advapi32
            hkey = ctypes.c_void_p()
            reg.RegOpenKeyExW(
                0x80000001,  # HKEY_CURRENT_USER
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                0, 0x20019,
                ctypes.byref(hkey),
            )
            value = ctypes.c_int()
            size = ctypes.c_int(4)
            reg.RegQueryValueExW(
                hkey, "AppsUseLightTheme", None, None,
                ctypes.byref(value), ctypes.byref(size),
            )
            reg.RegCloseKey(hkey)
            return value.value == 0
        except Exception:
            return False
    return False


def resolve_theme(theme_setting: str) -> str:
    """解析主题设置 → 实际主题名（如 'light', 'ocean_blue'）"""
    if theme_setting == "auto":
        return "dark" if detect_system_dark_mode() else "light"
    # 校验主题是否存在，不存在则回退到 light
    if theme_setting not in _THEME_MAP:
        return "light"
    return theme_setting


def apply_qss_theme(app: QApplication, theme_name: str) -> str:
    """应用 QSS 主题，返回实际使用的主题名"""
    qss_file = _THEME_MAP.get(theme_name)
    if qss_file:
        qss_path = _RESOURCES_DIR / qss_file
        if qss_path.exists():
            app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
            return theme_name

    # 回退到 light
    fallback = _RESOURCES_DIR / "light.qss"
    if fallback.exists():
        app.setStyleSheet(fallback.read_text(encoding="utf-8"))
    return "light"


def list_available_themes() -> list[dict]:
    """列出可用的主题，返回 [{name, label, file}, ...]"""
    result = []
    for name, qss_file in _THEME_MAP.items():
        if (_RESOURCES_DIR / qss_file).exists():
            label = _THEME_LABELS.get(name, f"🎨 {name}")
            result.append({"name": name, "label": label, "file": qss_file})
    return result


def get_theme_label(theme_name: str) -> str:
    """获取主题的显示标签"""
    return _THEME_LABELS.get(theme_name, f"🎨 {theme_name}")


# 便捷别名（供 main_window import 使用）
_detect_system_dark = detect_system_dark_mode
_apply_qss_theme = apply_qss_theme
