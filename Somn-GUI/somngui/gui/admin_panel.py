# -*- coding: utf-8 -*-
"""Somn GUI - 系统管理面板

全局管理仪表盘，串联项目所有功能模块：
- 引擎加载管理 / LLM双脑管理 / 主链路监控
- 自主进化 / 记忆生命周期 / Claw调度 / 系统组件健康

v1.0.0 (2026-04-27):
- 阶段一：导航重组（NAV_GROUPS 四分组 + 分组主题色条 + 可滚动导航栏）
- 阶段一：按钮选中态左侧 3px 色条（按分组主题色区分）
- 阶段二：面包屑导航系统（_breadcrumb_bar + _update_breadcrumb）
- 阶段三：面板打通（AppState.admin_panel_navigate 信号 + _link_button 跨面板跳转）
- 阶段三：DashboardOverview 新增快速入口区块（跳各分组首面板）
- 阶段四：视觉升级（侧栏 #1a1a2e / 主色 #00d4aa / 卡片白底阴影）

v1.0.0 (2026-04-27):
- 全局搜索框（顶部，支持中文/英文模糊搜索）
- Ctrl+K 快捷键聚焦搜索框
- 搜索结果下拉列表（实时匹配面板名称，最多10个）
- 快捷键系统（Ctrl+1~4 切换分组，Esc 关闭弹窗）
- 新增 PANEL_LABELS 常量（面板 key → 中文标签）
- NAV_GROUPS 格式改为 (分组名, 主题色, [key列表])
- 新增 _link_button() 工具函数（通过 AppState 信号实现跨面板导航）

v1.0.0 (2026-04-27):
- 深色/浅色模式切换（THEME_LIGHT / THEME_DARK 常量）
- 右上角主题切换按钮（🌙/☀️）
- _toggle_theme() / _apply_theme() 方法
- 面板收藏夹功能（_toggle_favorite / _show_favorites）
- 主题设置持久化（QSettings）

v1.0.0 (2026-04-27):
- 响应式布局（窗口宽度<1000px时导航栏自动折叠）
- _collapse_nav() / _expand_nav() 方法
- resizeEvent 重写（响应式触发）
- 导航栏展开/折叠按钮（<< / >>）
- 优化小窗口下的显示效果

v1.0.0 (2026-04-26):
- 修复 AlertPanel Dashboard 广播订阅无效问题（Dashboard API 无 alerts 字段）
- AlertPanel 移除无效订阅，保持独立刷新模式

v1.0.0 (2026-04-26):
- 新增 AlertPanel 告警管理面板（第14个子面板）
- 后端新增 /api/v1/admin/alerts/* 告警管理端点（4个）
- api_client.py 新增 admin_alerts_* 方法（4个）
- AlertPanel 支持告警历史查看/统计/清除/测试触发
- 级别过滤（全部/INFO/WARNING/CRITICAL）

v1.0.0 (2026-04-26):
- SystemResourcePanel 包装类继承 CachedPanelMixin（统一缓存逻辑）
- SystemResourcePanel 接入 Dashboard 广播系统
- AlertPanel 接入 Dashboard 广播（轻量更新统计卡片）
- 减少独立 API 调用，利用广播数据更新统计

v1.0.0 (2026-04-26):
- 修复全部 8 个组件广播处理器签名一致性（统一 1 参数 data）
- LLMManagerPanel._on_llm_update 新增会话数卡片同步
- LoadManagerPanel._on_load_manager_update 新增 pending/failed 卡片同步

v1.0.0 (2026-04-26):
- StartupPanel 接入 Dashboard 广播（自动同步后端状态）
- 修复 NeuralLayoutPanel._on_neural_update 冗余检查逻辑
- EvolutionPanel 广播处理器补充状态卡片更新
- ChainMonitorPanel 广播处理器直接更新健康状态文字

v1.0.0 (2026-04-26):
- 修复 state.py broadcast_admin_dashboard 组件遍历逻辑
- 全部11个面板接入组件订阅系统（全局广播联动）
- LoadManagerPanel / LLMManagerPanel / ChainMonitorPanel 订阅组件更新
- EvolutionPanel / SystemComponentsPanel / NeuralLayoutPanel 订阅组件更新
- 仪表盘刷新一次，所有面板自动同步，无冗余API调用

v1.0.0 (2026-04-26):
- 增强 _action_button() 支持 flat 参数（扁平按钮）
- 新增 _info_label() 统一信息标签工具函数
- 新增 _title_label() 统一标题标签工具函数
- StartupPanel 刷新按钮和状态标签使用统一函数
- NeuralLayoutPanel 按钮和信息标签使用统一函数

v1.0.0 (2026-04-26):
- 新增 _nav_bar() 统一导航栏工具函数
- 新增 _nav_button() 统一导航按钮工具函数
- StartupPanel 使用全局 _service_card() 替代局部方法
- StartupPanel 日志区域改用 _text_browser() 统一函数
- AdminPanel 导航栏使用统一工具函数重构
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import (
    Qt, QTimer, pyqtSignal,
    QPropertyAnimation, QThread,
    QKeySequence, QEvent,
)
from PyQt6.QtGui import (
    QColor,
)
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QComboBox, QCheckBox,
    QDialog, QDialogButtonBox,
    QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QInputDialog, QLabel,
    QLineEdit, QListWidget,
    QMessageBox,
    QPushButton, QScrollArea,
    QStackedWidget,
    QTabWidget, QTableWidget, QTableWidgetItem,
    QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget,
    QShortcut,
)

from loguru import logger


# ═══════════════════════════════════════════════════
# 导入子面板
# ═══════════════════════════════════════════════════

try:
    from .system_resource_panel import _SystemResourcePanelBase
    _HAS_RESOURCE_PANEL = True
except ImportError:
    _HAS_RESOURCE_PANEL = False
    _SystemResourcePanelBase = None


# 

# ═══════════════════════════════════════════════════════════
# 全局常量
# ═══════════════════════════════════════════════════════════

# v1.0.0: 提取硬编码配置为常量
DEFAULT_BACKEND_HOST: str = "127.0.0.1"
DEFAULT_BACKEND_PORT: int = 8964
DEFAULT_BACKEND_URL: str = f"http://{DEFAULT_BACKEND_HOST}:{DEFAULT_BACKEND_PORT}"

# Python 可执行文件路径（动态获取）
import sys as _sys
PYTHON_EXE_PATH: str = _sys.executable


# ═══════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════
# v1.0.0: 主题样式定义（深色/浅色模式）
# ═════════════════════════════════════════════════════════

THEME_LIGHT = {
    "name": "浅色模式",
    "bg_primary": "#f1f5f9",
    "bg_secondary": "#ffffff",
    "bg_sidebar": "#1a1a2e",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b",
    "text_light": "#e2e8f0",
    "accent": "#00d4aa",
    "border": "#e2e8f0",
    "shadow": "rgba(0, 0, 0, 30)",
}

THEME_DARK = {
    "name": "深色模式",
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "bg_sidebar": "#0a0a1a",
    "text_primary": "#e2e8f0",
    "text_secondary": "#94a3b8",
    "text_light": "#e2e8f0",
    "accent": "#00d4aa",
    "border": "#334155",
    "shadow": "rgba(0, 0, 0, 80)",
}

# 样式常量
# ═══════════════════════════════════════════════════════════

STATUS_COLORS = {
    "healthy": "#2ecc71",
    "loaded": "#2ecc71",
    "ok": "#2ecc71",
    "active": "#2ecc71",
    "running": "#2ecc71",
    "degraded": "#f39c12",
    "loading": "#f39c12",
    "warning": "#f39c12",
    "pending": "#95a5a6",
    "idle": "#95a5a6",
    "inactive": "#95a5a6",
    "failed": "#e74c3c",
    "error": "#e74c3c",
    "unhealthy": "#e74c3c",
    "unavailable": "#e74c3c",
    "stopped": "#e74c3c",
}

STATUS_TEXT = {
    "healthy": "健康", "loaded": "已加载", "ok": "正常", "active": "活跃",
    "running": "运行中", "degraded": "降级", "loading": "加载中",
    "warning": "警告", "pending": "等待中", "idle": "空闲",
    "inactive": "未激活", "failed": "失败", "error": "错误",
    "unhealthy": "不健康", "unavailable": "不可用", "stopped": "已停止",
}


def _status_badge(text: str) -> QLabel:
    """创建状态徽章"""
    color = STATUS_COLORS.get(text.lower(), "#95a5a6")
    display = STATUS_TEXT.get(text.lower(), text)
    label = QLabel(f"  {display}  ")
    label.setStyleSheet(f"""
        QLabel {{
            background-color: {color};
            color: white;
            border-radius: 10px;
            padding: 2px 10px;
            font-size: 11px;
            font-weight: bold;
        }}
    """)
    label.setFixedHeight(22)
    return label


def _metric_card(title: str, value: str, color: str = "#00d4aa",
                height: int = 70, width: int = 140,
                title_size: int = 11, value_size: int = 20) -> QWidget:
    """
    阶段四重构：创建指标卡片（新视觉设计）

    新设计：
    - 白底 + 细微阴影（QGraphicsDropShadowEffect）
    - 边框 #e2e8f0，圆角 10px
    - 标题 #64748b，数值粗体 #00d4aa

    Args:
        title: 标题文本
        value: 数值文本
        color: 数值颜色（默认 #00d4aa 新主色）
        height: 卡片高度，默认 70
        width: 卡片宽度，默认 140（加宽）
        title_size: 标题字体大小，默认 11
        value_size: 数值字体大小，默认 20
    """
    card = QFrame()
    card.setStyleSheet(f"""
        QFrame {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 12px 14px;
        }}
    """)
    # 添加阴影效果
    from PyQt6.QtWidgets import QGraphicsDropShadowEffect
    from PyQt6.QtGui import QColor
    shadow = QGraphicsDropShadowEffect(card)
    shadow.setBlurRadius(12)
    shadow.setColor(QColor(0, 0, 0, 25))
    shadow.setOffset(0, 2)
    card.setGraphicsEffect(shadow)

    layout = QVBoxLayout(card)
    layout.setContentsMargins(12, 8, 12, 8)
    layout.setSpacing(6)

    title_label = QLabel(title)
    title_label.setStyleSheet(f"color: #64748b; font-size: {title_size}px;")
    value_label = QLabel(value)
    value_label.setStyleSheet(f"color: {color}; font-size: {value_size}px; font-weight: 700;")

    layout.addWidget(title_label)
    layout.addWidget(value_label)
    card.setFixedHeight(height)
    card.setFixedWidth(width)
    return card


def _section_group(title: str) -> QGroupBox:
    """v1.0.0: 创建区域分组框（卡片样式 + 阴影）"""
    group = QGroupBox(title)
    group.setStyleSheet("""
        QGroupBox {
            font-weight: bold;
            font-size: 13px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 6px;
            color: #1e293b;
        }
    """)
    # 卡片阴影
    shadow = QGraphicsDropShadowEffect(group)
    shadow.setBlurRadius(12)
    shadow.setColor(QColor(0, 0, 0, 30))
    shadow.setOffset(0, 2)
    group.setGraphicsEffect(shadow)
    return group


def _service_card(title: str, status: str, color: str, width: int = 180) -> tuple[QWidget, QLabel]:
    """
    v1.0.0: 创建服务状态卡片

    Args:
        title: 服务标题
        status: 初始状态文本
        color: 边框和状态文字颜色（十六进制）
        width: 卡片宽度，默认 180

    Returns:
        (card_widget, status_label) 元组，status_label 可后续更新
    """
    card = QFrame()
    card.setStyleSheet(f"""
        QFrame {{
            background: white;
            border: 2px solid {color};
            border-radius: 8px;
            padding: 16px;
        }}
    """)
    card.setFixedWidth(width)

    layout = QVBoxLayout(card)
    layout.setSpacing(8)

    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1e293b;")
    layout.addWidget(title_label)

    status_label = QLabel(status)
    status_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")
    layout.addWidget(status_label)

    return card, status_label


def _tab_widget(parent: QWidget = None, extra_css: str = None) -> QTabWidget:
    """
    v1.0.0: 创建统一样式的 QTabWidget

    Args:
        parent: 父组件，默认 None
        extra_css: 额外的 CSS 样式

    Returns:
        QTabWidget 实例
    """
    tabs = QTabWidget(parent)
    base_css = """
        QTabWidget::pane { border: 1px solid #e2e8f0; border-radius: 6px; background: #f9fafb; }
        QTabBar::tab { padding: 8px 18px; font-size: 12px; font-weight: 600; }
        QTabBar::tab:selected { background: #00d4aa; color: white; border-radius: 4px 4px 0 0; }
    """
    if extra_css:
        base_css += "\n        " + extra_css.strip()
    tabs.setStyleSheet(base_css)
    return tabs


def _panel_header(title: str, refresh_callback=None,
                  extra_buttons: list = None,
                  prepend_buttons: list = None,
                  use_action_button: bool = False,
                  refresh_text: str = None) -> tuple[QHBoxLayout, QPushButton]:
    """
    v1.0.0: 创建统一面板标题栏

    Args:
        title: 面板标题（可含 emoji）
        refresh_callback: 刷新按钮的回调函数，默认 None 不绑定
        extra_buttons: 刷新按钮之前的额外按钮列表 [(text, callback), ...]
        prepend_buttons: 同 extra_buttons（别名，兼容）
        use_action_button: 是否使用 _action_button 工厂函数，默认 False
        refresh_text: 刷新按钮文本，默认 "🔄 刷新"

    Returns:
        (header_layout, refresh_btn) 元组
    """
    header = QHBoxLayout()
    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #1e293b;")
    header.addWidget(title_label)
    header.addStretch()

    # 额外按钮（在刷新按钮之前）
    btns = (prepend_buttons or []) + (extra_buttons or [])
    for btn_text, btn_cb in btns:
        btn = QPushButton(btn_text)
        if btn_cb:
            btn.clicked.connect(btn_cb)
        header.addWidget(btn)

    # 刷新按钮
    if use_action_button:
        refresh_btn = _action_button(refresh_text or "🔄 刷新", "#00d4aa", (80, 32))
    else:
        refresh_btn = QPushButton(refresh_text or "🔄 刷新")
    if refresh_callback:
        refresh_btn.clicked.connect(refresh_callback)
    header.addWidget(refresh_btn)

    return header, refresh_btn


def _cache_stats_bar() -> tuple[QHBoxLayout, QLabel, QLabel, QLabel]:
    """
    v1.0.0: 创建统一缓存统计行

    Returns:
        (stats_layout, hit_card, api_card, fail_card) 元组
    """
    stats = QHBoxLayout()
    stats.setSpacing(10)
    hit_card = _metric_card("缓存命中率", "--", "#2ecc71")
    api_card = _metric_card("API调用", "--", "#00d4aa")
    fail_card = _metric_card("API失败率", "--", "#e74c3c")
    for c in [hit_card, api_card, fail_card]:
        stats.addWidget(c)
    stats.addStretch()
    return stats, hit_card, api_card, fail_card


def _action_button(text: str, color: str, size: tuple = None,
                   hover_color: str = None, padding: tuple = None,
                   disabled_color: str = "#95a5a6",
                   flat: bool = False) -> QPushButton:
    """
    v1.0.0: 创建统一样式的动作按钮

    Args:
        text: 按钮文本
        color: 背景颜色（十六进制）
        size: (width, height) 尺寸元组，默认 (80, 32)
        hover_color: 悬停颜色，默认自动计算深色版
        padding: (h, v) 内边距元组，默认 None
        disabled_color: 禁用状态颜色，默认 #95a5a6
        flat: 扁平按钮（无背景色，纯文字），默认 False
    """
    if hover_color is None and not flat:
        hover_color = _darken_color(color)
    if size is None:
        size = (80, 32)
    btn = QPushButton(text)
    if not flat:
        btn.setFixedSize(size[0], size[1])

    # 构建样式
    if flat:
        # 扁平按钮样式（纯文字）
        base = f"background: transparent; color: {color}; border: none; font-weight: bold;"
        if padding:
            base += f" padding: {padding[1]}px {padding[0]}px;"
        hover = f"QPushButton:hover {{ color: {_darken_color(color)}; }}"
        disabled = f"QPushButton:disabled {{ color: {disabled_color}; }}"
    else:
        # 带背景按钮样式
        base = f"background: {color}; color: white; border: none; border-radius: 4px; font-weight: bold;"
        if padding:
            base += f" padding: {padding[1]}px {padding[0]}px;"
        hover = f"QPushButton:hover {{ background: {hover_color}; }}"
        disabled = f"QPushButton:disabled {{ background: {disabled_color}; }}"

    btn.setStyleSheet(f"""
        QPushButton {{{base}}}
        {hover}
        {disabled}
    """)
    return btn


def _info_label(text: str = "", color: str = "#7f8c8d",
                font_size: int = 13) -> QLabel:
    """
    v1.0.0: 创建统一的信息标签

    Args:
        text: 标签文本，默认空字符串
        color: 文字颜色，默认 #7f8c8d（灰色）
        font_size: 字体大小，默认 13

    Returns:
        QLabel 实例
    """
    label = QLabel(text)
    label.setStyleSheet(f"color: {color}; font-size: {font_size}px;")
    return label


def _title_label(text: str, font_size: int = 16,
                  color: str = "#1e293b") -> QLabel:
    """
    v1.0.0: 创建统一的标题标签

    Args:
        text: 标签文本
        font_size: 字体大小，默认 16
        color: 文字颜色，默认 #1e293b

    Returns:
        QLabel 实例
    """
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold; color: {color};")
    return label


def _darken_color(hex_color: str, factor: float = 0.85) -> str:
    """将十六进制颜色变暗（用于悬停效果）"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


# ════════════════════════════════════════════════════
# 导航分组定义（阶段一重构：分组导航栏）
# ════════════════════════════════════════════════════

NAV_GROUPS: list = [
    ("全局概览", "#00d4aa", ["dashboard"]),
    ("运行管理", "#6366f1", ["startup", "config", "load", "chain"]),
    ("智能系统", "#f59e0b", ["llm", "evolution", "memory", "claw", "knowledge"]),
    ("系统资源", "#ef4444", ["system", "neural", "system_resource", "alerts"]),
]

# 面板显示名（key -> 中文名）
PANEL_LABELS: dict = {
    "dashboard": "全局概览",
    "startup": "服务启停",
    "config": "配置管理",
    "load": "引擎加载",
    "llm": "LLM管理",
    "chain": "主链路",
    "evolution": "自主进化",
    "memory": "记忆系统",
    "claw": "Claw调度",
    "knowledge": "知识格子",
    "system": "系统组件",
    "neural": "神经网络",
    "system_resource": "系统资源",
    "alerts": "告警管理",
}


# ═════════════════════════════════════════════════════════
# 导航分组定义（阶段一重构：分组导航栏）
# ═════════════════════════════════════════════════════════

# 分组结构：(分组名, 分组主题色, [面板key列表])
NAV_GROUPS: list = [
    ("全局概览", "#00d4aa", ["dashboard"]),
    ("运行管理", "#6366f1", ["startup", "config", "load", "chain"]),
    ("智能系统", "#f59e0b", ["llm", "evolution", "memory", "claw", "knowledge"]),
    ("系统资源", "#ef4444", ["system", "neural", "system_resource", "alerts"]),
]

# 面板显示名（key -> 中文名）
PANEL_LABELS: dict = {
    "dashboard": "全局概览",
    "startup": "服务启停",
    "config": "配置管理",
    "load": "引擎加载",
    "llm": "LLM管理",
    "chain": "主链路",
    "evolution": "自主进化",
    "memory": "记忆系统",
    "claw": "Claw调度",
    "knowledge": "知识格子",
    "system": "系统组件",
    "neural": "神经网络",
    "system_resource": "系统资源",
    "alerts": "告警管理",
}


def _nav_bar(width: int = 180, title: str = "Somn 管理") -> tuple[
    QFrame, QVBoxLayout, QButtonGroup, Dict[str, QPushButton], Dict[str, QWidget]
]:
    """
    阶段一重构：创建分组导航栏

    新设计：
    - 侧栏背景 #1a1a2e，宽度 180
    - 分组标题 + 左侧色条指示
    - 按钮选中态：左侧 3px 色条 + 浅色背景

    Args:
        width: 导航栏宽度，默认 180（加宽以容纳分组标题）
        title: 导航栏标题，默认 "Somn 管理"

    Returns:
        (nav_frame, nav_layout, btn_group, nav_buttons_dict, group_labels_dict)
        nav_buttons_dict: key -> QPushButton（按 key 快速查找）
        group_labels_dict: group_name -> QLabel（分组标题 widget）
    """
    nav = QFrame()
    nav.setFixedWidth(width)
    nav.setStyleSheet("""
        QFrame {
            background: #1a1a2e;
            border-right: 1px solid #2a2a4a;
        }
    """)

    nav_layout = QVBoxLayout(nav)
    nav_layout.setContentsMargins(0, 0, 0, 0)
    nav_layout.setSpacing(0)

    # ── 标题区 ──
    title_frame = QFrame()
    title_frame.setStyleSheet("background: #12121f;")
    title_frame.setFixedHeight(56)
    title_layout = QVBoxLayout(title_frame)
    title_layout.setContentsMargins(16, 0, 16, 0)
    title_label = QLabel(title)
    title_label.setStyleSheet("""
        color: #00d4aa;
        font-size: 15px;
        font-weight: 700;
    """)
    title_layout.addWidget(title_label, 0, Qt.AlignmentFlag.AlignVCenter)
    nav_layout.addWidget(title_frame)

    # ── 导航区（可滚动）──
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
        QScrollArea { background: transparent; border: none; }
        QScrollBar:vertical { width: 6px; background: transparent; }
        QScrollBar::handle:vertical { background: #2a2a4a; border-radius: 3px; }
    """)
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_layout.setContentsMargins(8, 12, 8, 12)
    scroll_layout.setSpacing(2)
    scroll.setWidget(scroll_content)

    btn_group = QButtonGroup(nav)
    btn_group.setExclusive(True)
    nav_buttons: Dict[str, QPushButton] = {}
    group_labels: Dict[str, QWidget] = {}

    # ── 按分组构建导航项 ──
    for group_name, group_color, keys in NAV_GROUPS:
        # 分组标题
        group_label = QLabel(group_name)
        group_label.setStyleSheet(f"""
            QLabel {{
                color: {group_color};
                font-size: 11px;
                font-weight: 600;
                padding: 12px 12px 4px 12px;
            }}
        """)
        scroll_layout.addWidget(group_label)
        group_labels[group_name] = group_label

        # 分组下的按钮（keys 是面板 key 列表）
        for key in keys:
            label = PANEL_LABELS.get(key, key)
            btn = _nav_button(label, key, group_color)
            btn.clicked.connect(lambda checked, k=key: None)  # 由 AdminPanel 覆盖
            btn_group.addButton(btn)
            scroll_layout.addWidget(btn)
            nav_buttons[key] = btn

        # 分组间距
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #2a2a4a; margin: 4px 8px;")
        scroll_layout.addWidget(sep)

    scroll_layout.addStretch()
    nav_layout.addWidget(scroll)

    return nav, nav_layout, btn_group, nav_buttons, group_labels


def _nav_button(text: str, key: str = "", group_color: str = "#00d4aa") -> QPushButton:
    """
    v1.0.0: 创建分组导航按钮（精致样式 + hover 动效）

    - 默认：透明背景，#94a3b8 文字，无左边框
    - 悬停：#1e293b 背景，#e2e8f0 文字，圆角
    - 选中：左侧 3px 色条（分组色）+ #1e293b 背景 + white 文字
    """
    btn = QPushButton(f"  {text}")
    btn.setCheckable(True)
    btn.setStyleSheet(f"""
        QPushButton {{
            color: #94a3b8;
            background: transparent;
            border: none;
            border-left: 3px solid transparent;
            padding: 8px 16px;
            text-align: left;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: #1e293b;
            color: #e2e8f0;
            border-radius: 4px;
        }}
        QPushButton:checked {{
            background: #1e293b;
            color: white;
            font-weight: 600;
            border-left: 3px solid {group_color};
            border-radius: 0px;
        }}
    """)
    return btn


# ════════════════════════════════════════════════════
# 阶段二新增：面包屑导航 + 跨面板链接
# ════════════════════════════════════════════════════

def _breadcrumb_bar(admin_panel: QWidget = None) -> tuple[QWidget, QHBoxLayout]:
    """
    阶段二新增：创建面包屑导航栏

    显示当前位置层级，支持点击返回上级。
    固定在内容区顶部，位于面板标题之上。

    层级格式：「分组名 › 面板名」
    - 点击分组名 → 切换到该分组第一个面板
    - 点击「◀ 概览」→ 返回 Dashboard

    Args:
        admin_panel: AdminPanel 实例（用于调用 _switch_panel）

    Returns:
        (breadcrumb_widget, breadcrumb_layout) 元组
        调用方通过 layout 动态更新文字和链接
    """
    bar = QFrame()
    bar.setFixedHeight(40)
    bar.setStyleSheet("""
        QFrame {
            background: white;
            border-bottom: 1px solid #e2e8f0;
        }
    """)
    layout = QHBoxLayout(bar)
    layout.setContentsMargins(16, 0, 16, 0)
    layout.setSpacing(4)

    # 默认：左侧留空，由 AdminPanel 动态填充
    layout.addStretch()
    return bar, layout



def _breadcrumb_link(text: str, target_key: str, state: "AppState") -> QPushButton:
    """
    v1.0.0: 面包屑可点击链接
    样式：蓝色链接，hover 有下划线，无边框无背景
    """
    btn = QPushButton(text)
    btn.setStyleSheet("""
        QPushButton {
            color: #6366f1;
            background: transparent;
            border: none;
            font-size: 12px;
            padding: 2px 4px;
        }
        QPushButton:hover {
            color: #4f46e5;
            text-decoration: underline;
        }
    """)
    btn.clicked.connect(lambda checked, k=target_key: state.admin_panel_history_navigate.emit(k))
    return btn

def _search_box(placeholder: str = "搜索面板...") -> QLineEdit:
    """v1.0.0: 创建搜索框（支持 Ctrl+K 聚焦）"""
    edit = QLineEdit()
    edit.setPlaceholderText(placeholder)
    edit.setStyleSheet("""
        QLineEdit {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            color: #1e293b;
        }
        QLineEdit:focus {
            border: 1px solid #00d4aa;
        }
    """)
    return edit


def _search_results_dropdown(parent) -> QListWidget:
    """v1.0.0: 搜索结果下拉列表"""
    lst = QListWidget(parent)
    lst.setStyleSheet("""
        QListWidget {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 4px;
            font-size: 13px;
        }
        QListWidget::item {
            padding: 8px 12px;
            border-radius: 4px;
        }
        QListWidget::item:hover {
            background: #f1f5f9;
        }
        QListWidget::item:selected {
            background: #00d4aa;
            color: white;
        }
    """)
    lst.setMaximumHeight(200)
    lst.setVisible(False)
    return lst


def _link_button(text: str, target_key: str, state: "AppState") -> QPushButton:
    """
    v1.0.0: 创建跨面板跳转按钮（精致链接样式 + hover 动效）
    """
    btn = QPushButton(text)
    btn.setStyleSheet("""
        QPushButton {
            color: #00d4aa;
            background: transparent;
            border: none;
            font-size: 12px;
            font-weight: 600;
            text-align: left;
            padding: 4px 8px;
            border-radius: 4px;
        }
        QPushButton:hover {
            color: #00b894;
            background: #00d4aa20;
            text-decoration: underline;
        }
    """)
    btn.clicked.connect(lambda checked: state.admin_panel_navigate.emit(target_key))
    return btn




def _related_panels_group(state: "AppState", related_keys: list) -> QGroupBox:
    """
    创建"相关面板"导航组（阶段三：面板打通）
    在面板底部添加跨面板跳转链接
    """
    group = _section_group("相关面板")
    layout = QHBoxLayout(group)
    layout.setSpacing(8)
    for key in related_keys:
        label = PANEL_LABELS.get(key, key)
        btn = _link_button(label, key, state)
        layout.addWidget(btn)
    layout.addStretch()
    return group

def _text_browser(parent: QWidget = None, max_height: int = None,
                  min_height: int = None,
                  extra_css: str = None) -> QTextBrowser:
    """
    v1.0.0: 创建统一样式的 QTextBrowser
    v1.0.0: 新增 extra_css 参数，支持追加自定义 CSS，替代重复的内联样式
    """
    base_css = """
        QTextBrowser {
            background: #fafafa;
            border: 1px solid #eee;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
        }
    """
    if extra_css:
        base_css = base_css + "\n        " + extra_css.strip()
    tb = QTextBrowser(parent)
    tb.setStyleSheet(base_css)
    if max_height:
        tb.setMaximumHeight(max_height)
    if min_height:
        tb.setMinimumHeight(min_height)
    return tb


def _apply_table_style(table: QTableWidget, max_height: int = 300,
                        apply_stylesheet: bool = True):
    """
    v1.0.0: 统一表格样式
    v1.0.0: 新增 apply_stylesheet 参数，支持仅设置结构属性（无样式）
    """
    if apply_stylesheet:
        table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 4px 8px;
            }
            QTableWidget::item:selected {
                background: #00d4aa;
                color: white;
            }
            QHeaderView::section {
                background: #f8f9fa;
                color: #1e293b;
                font-weight: bold;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #00d4aa;
            }
        """)
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table.horizontalHeader().setStretchLastSection(True)
    if max_height:
        table.setMaximumHeight(max_height)


# ═══════════════════════════════════════════════════════════
# 异步任务 Worker
# ═══════════════════════════════════════════════════════════

class AdminWorker(QThread):
    """管理API异步调用线程"""
    finished = pyqtSignal(object)  # (success: bool, data: dict, error: str)

    def __init__(self, coro_func, *args, **kwargs):
        super().__init__()
        self._coro_func = coro_func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        import asyncio
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(self._coro_func(*self._args, **self._kwargs))
            success = isinstance(result, dict) and result.get("success", False)
            error = result.get("message", "") if not success else ""
            self.finished.emit((success, result.get("data"), error))
        except Exception as e:
            logger.error(f"AdminWorker 执行失败: {e}")
            self.finished.emit((False, None, str(e)))
        finally:
            loop.close()


class _RefreshMixin:
    """安全刷新混入 — 在 lambda 回调中提供 try/except 保护"""
    def _safe_refresh(self):
        try:
            self._refresh()
        except Exception as e:
            logger.debug(f"[{type(self).__name__}] 刷新失败: {e}")


# ═══════════════════════════════════════════════════════════
# CachedPanelMixin — 所有 Admin 子面板的缓存基类
# 策略: Cache-First → API回源 → 更新缓存 → Signal通知
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
# LoadingMixin — 统一加载遮罩混入
# ═══════════════════════════════════════════════════════════

class LoadingMixin:
    """
    v1.0.0: 统一加载遮罩混入
    
    使用方式: 让子类继承，放在 QWidget 之前
      class MyPanel(LoadingMixin, QWidget):
          ...
    
    提供:
    - _show_loading() / _hide_loading() — 显示/隐藏加载遮罩
    - _with_loading(coro) — 自动包装协程，调用前后切换遮罩
    """

    def __init__(self, *args, **kwargs):
        self._loading_overlay: Optional[QWidget] = None
        self._loading_label: Optional[QLabel] = None

    def _show_loading(self, message: str = "⏳ 加载中..."):
        """显示加载遮罩"""
        if self._loading_overlay is not None:
            return  # 已有遮罩
        
        # 创建遮罩
        overlay = QWidget(self)
        overlay.setStyleSheet("""
            QWidget {
                background: rgba(0, 0, 0, 0.4);
                border-radius: 8px;
            }
        """)
        overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        overlay.resize(self.size())
        overlay.show()  # v1.0.0: 先 show 再计算位置，否则宽高为 0
        
        # 居中标签
        label = QLabel(message, overlay)
        label.setStyleSheet("""
            QLabel {
                background: white;
                color: #1e293b;
                border-radius: 8px;
                padding: 16px 32px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        # v1.0.0: show() 后再居中定位
        label.move(
            (overlay.width() - label.width()) // 2,
            (overlay.height() - label.height()) // 2
        )
        label.show()
        
        self._loading_overlay = overlay
        self._loading_label = label

    def _hide_loading(self):
        """隐藏加载遮罩"""
        if self._loading_overlay is not None:
            self._loading_overlay.deleteLater()
            self._loading_overlay = None
            self._loading_label = None

    def resizeEvent(self, event):
        """窗口大小变化时更新遮罩"""
        # v1.0.0: LoadingMixin 不是 QWidget 子类，不调用 super()
        # 实际的 resizeEvent 由混入的 QWidget 子类处理
        if self._loading_overlay is not None:
            self._loading_overlay.resize(self.size())

    def _with_loading(self, coro_func, *args, callback=None, on_error=None):
        """
        自动包装协程，显示加载遮罩
        
        Args:
            coro_func: 异步协程函数
            *args: 协程参数
            callback: 成功回调 callback(result)
            on_error: 失败回调 on_error(error)
        """
        self._show_loading()
        
        def _done(result, attempt=1):
            self._hide_loading()
            if callback:
                callback(result)
        
        def _error(err):
            self._hide_loading()
            if on_error:
                on_error(err)
            else:
                logger.error(f"[{type(self).__name__}] 请求失败: {err}")
        
        try:
            w = AdminWorker(coro_func, *args)
            w.finished.connect(lambda r: (
                self._hide_loading(),
                _done(r) if r[0] else _error(r[2])
            ))
            w.start()
        except Exception as e:
            self._hide_loading()
            _error(str(e))


class CachedPanelMixin:
    """
    缓存面板 Mixin — 为所有 Admin 子面板提供统一缓存逻辑。

    使用方式: 让子类继承时放在 QWidget 之前
      class MyPanel(CachedPanelMixin, QWidget):
          ...

    缓存策略:
    - get_cached(key) 先查缓存，有则直接返回
    - fetch_then_cache(key, api_call) 异步获取，成功后写缓存
    - is_cache_stale(key) TTL过期检查
    - subscribe_dashboard(callback) 订阅全局仪表盘广播
    - subscribe_component(name, callback) 订阅指定组件更新

    v1.0.0 新增特性:
    - 缓存命中率统计 (get_cache_stats)
    - API 自动重试机制 (max_retries, retry_delay)
    - 重试回调 (on_retry)
    """

    # 子类覆盖此属性定义各数据的 TTL（秒）
    CACHE_TTL: Dict[str, float] = {}

    # ── 重试配置 ──
    MAX_RETRIES: int = 3      # 最大重试次数
    RETRY_DELAY: float = 1.0  # 重试间隔（秒）

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 必须调用 super 以支持 PyQt6 MRO
        self._cache_timestamps: Dict[str, float] = {}
        self._subscriptions: Dict[str, Any] = {}
        # ── v1.0.0: 缓存命中率统计 ──
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._api_calls: int = 0
        self._api_failures: int = 0

    # ── 缓存读写 ──

    def get_cached(self, key: str) -> Optional[Any]:
        """从 AppState 缓存读取数据（同步，无网络）"""
        cache = getattr(self, '_state', None) and getattr(self._state, 'cache', None)
        if cache:
            result = cache.get(f"panel:{type(self).__name__}:{key}")
            if result is not None:
                self._cache_hits += 1
                return result
            self._cache_misses += 1
            return None
        self._cache_misses += 1
        return None

    def set_cached(self, key: str, value: Any, ttl: Optional[float] = None):
        """写入 AppState 缓存"""
        cache = getattr(self, '_state', None) and getattr(self._state, 'cache', None)
        if cache:
            cache_key = f"panel:{type(self).__name__}:{key}"
            cache.set(cache_key, value, ttl=ttl)

    def is_cache_stale(self, key: str) -> bool:
        """检查缓存是否过期（超过 TTL）"""
        import time as _time
        if key not in self._cache_timestamps:
            return True
        default_ttl = self.CACHE_TTL.get(key, 300)
        return _time.time() - self._cache_timestamps[key] > default_ttl

    def _touch_cache(self, key: str):
        """标记缓存时间戳"""
        import time as _time
        self._cache_timestamps[key] = _time.time()

    # ── v1.0.0: 缓存命中率统计 ──

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        获取缓存命中率统计。

        Returns:
            {
                "hits": int,       # 缓存命中次数
                "misses": int,     # 缓存未命中次数
                "hit_rate": float, # 命中率 (0-1)
                "api_calls": int,  # API 调用次数
                "api_failures": int,  # API 失败次数
                "failure_rate": float  # API 失败率 (0-1)
            }
        """
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0.0
        api_total = self._api_calls + self._api_failures
        failure_rate = self._api_failures / api_total if api_total > 0 else 0.0
        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "hit_rate": round(hit_rate, 4),
            "api_calls": self._api_calls,
            "api_failures": self._api_failures,
            "failure_rate": round(failure_rate, 4),
        }

    def reset_cache_stats(self):
        """重置命中率统计"""
        self._cache_hits = 0
        self._cache_misses = 0
        self._api_calls = 0
        self._api_failures = 0

    # ── v1.0.0: 指标卡片工具 ──

    # v1.0.0: 所有面板使用的卡片标题，set_card_value 跳过这些
    _CARD_TITLES = frozenset({
        # 缓存统计通用
        "缓存命中率", "API调用", "API失败率",
        # MemoryLifecyclePanel
        "健康分数", "知识总数", "活跃", "陈旧", "薄弱",
        # ClawSchedulerPanel
        "已调度", "已完成", "失败", "活跃任务",
        # LoadManagerPanel
        "总模块数", "已加载", "等待中",
        # LLMManagerPanel
        "运行状态", "当前模型", "活跃会话",
        # DashboardOverview
        "已加载模块", "LLM状态", "链路节点", "Claw任务",
        "进化计划",
    })

    def set_card_value(self, card: QWidget, value: str, color: str = None):
        """
        v1.0.0: 设置指标卡片值
        v1.0.0: 使用 _CARD_TITLES frozenset 判断，提升性能

        Args:
            card: _metric_card() 创建的卡片
            value: 要显示的值
            color: 可选，更新值标签颜色
        """
        for child in card.findChildren(QLabel):
            if child.text() in self._CARD_TITLES:
                continue
            child.setText(value)
            if color:
                child.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")
            break

    def set_cache_stats_cards(self, hit_card: QWidget, api_card: QWidget,
                               fail_card: QWidget,
                               color_threshold: bool = False):
        """
        v1.0.0: 一次性更新三个缓存统计卡片
        v1.0.0: 新增 color_threshold 参数，支持颜色区分（Dashboard 用）

        Args:
            hit_card: 缓存命中率卡片
            api_card: API调用次数卡片
            fail_card: API失败率卡片
            color_threshold: True 时根据阈值选择颜色（Dashboard 专用）
        """
        stats = self.get_cache_stats()

        if color_threshold:
            # Dashboard 专用：根据阈值选择颜色
            hit_rate = stats["hit_rate"]
            fail_rate = stats["failure_rate"]
            hit_color = "#2ecc71" if hit_rate >= 0.7 else ("#f39c12" if hit_rate >= 0.4 else "#e74c3c")
            fail_color = "#2ecc71" if fail_rate < 0.05 else ("#f39c12" if fail_rate < 0.2 else "#e74c3c")
        else:
            hit_color = "#2ecc71"
            fail_color = "#e74c3c"

        self.set_card_value(hit_card, f"{stats['hit_rate']:.1%}", hit_color)
        self.set_card_value(api_card, str(stats['api_calls']), "#00d4aa")
        self.set_card_value(fail_card, f"{stats['failure_rate']:.1%}", fail_color)

    # ── 核心方法 ──

    def fetch_then_cache(self, key: str, api_call, ttl: Optional[float] = None,
                         callback=None, on_error=None, on_retry=None,
                         max_retries: Optional[int] = None, retry_delay: Optional[float] = None):
        """
        异步获取数据 → 成功后写入缓存（支持重试）

        v1.0.0: 改用完全异步模式 — 在后台线程中 async 运行协程，
        不再通过 future.result() 同步等待，避免线程阻塞。

        Args:
            key: 缓存键
            api_call: 异步协程（API调用）
            ttl: 缓存TTL（秒），默认使用 CACHE_TTL[key]
            callback: 成功后回调 callback(data)
            on_error: 失败回调 on_error(error)
            on_retry: 重试回调 on_retry(attempt, error) — v1.0.0
            max_retries: 最大重试次数，默认使用 MAX_RETRIES
            retry_delay: 重试间隔（秒），默认使用 RETRY_DELAY
        """
        max_retries = max_retries if max_retries is not None else self.MAX_RETRIES
        retry_delay = retry_delay if retry_delay is not None else self.RETRY_DELAY

        def _done(result, attempt=1):
            self._touch_cache(key)
            self.set_cached(key, result, ttl=ttl)
            if callback:
                callback(result)

        async def _async_run(attempt: int = 1):
            """在后台线程的事件循环中异步执行 API 调用"""
            import asyncio
            try:
                self._api_calls += 1
                from somngui.core.state import AppState
                # v1.0.0: 直接在后台 loop 中 await，无需同步等待
                loop = AppState._get_bg_loop()
                future = asyncio.run_coroutine_threadsafe(api_call, loop)
                result = await asyncio.wrap_future(future, timeout=30)

                # 检查是否成功（success 字段为 True）
                if isinstance(result, dict) and result.get("success") is False:
                    raise Exception(result.get("message", "API returned failure"))
                _done(result, attempt)
            except Exception as e:
                logger.warning(f"[{type(self).__name__}] fetch_then_cache({key}) "
                             f"第 {attempt} 次尝试失败: {e}")
                if attempt < max_retries:
                    if on_retry:
                        on_retry(attempt, str(e))
                    # 指数退避: delay * 2^(attempt-1)
                    await asyncio.sleep(retry_delay * (2 ** (attempt - 1)))
                    await _async_run(attempt + 1)
                else:
                    self._api_failures += 1
                    logger.error(f"[{type(self).__name__}] fetch_then_cache({key}) "
                               f"全部 {max_retries} 次尝试失败")
                    if on_error:
                        on_error(str(e))

        import threading
        t = threading.Thread(target=lambda: self._sync_wrap_async(_async_run), daemon=True)
        t.start()

    @staticmethod
    def _sync_wrap_async(coro):
        """在线程中运行异步协程的辅助方法"""
        import asyncio
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(coro())
        finally:
            loop.close()

    def fetch_with_cache(self, key: str, api_call, ttl: Optional[float] = None,
                         cache_callback=None, api_callback=None, on_error=None,
                         on_retry=None, max_retries: Optional[int] = None,
                         retry_delay: Optional[float] = None):
        """
        Cache-First 模式: 先返回缓存数据，再异步刷新 API（支持重试）

        Args:
            key: 缓存键
            api_call: 异步协程
            ttl: TTL
            cache_callback: 缓存命中时的回调 callback(data)
            api_callback: API返回时的回调 callback(data)
            on_error: 错误回调
            on_retry: 重试回调 on_retry(attempt, error) — v1.0.0
            max_retries: 最大重试次数，默认使用 MAX_RETRIES
            retry_delay: 重试间隔（秒），默认使用 RETRY_DELAY
        """
        cached = self.get_cached(key)
        is_stale = self.is_cache_stale(key)

        # 缓存命中 → 先展示缓存，再可选刷新
        if cached is not None:
            if cache_callback:
                cache_callback(cached)
            # 如果缓存过期，在后台刷新
            if is_stale:
                self.fetch_then_cache(key, api_call, ttl=ttl,
                                     callback=api_callback, on_error=on_error,
                                     on_retry=on_retry,
                                     max_retries=max_retries, retry_delay=retry_delay)
        else:
            # 无缓存 → 直接调用 API
            self.fetch_then_cache(key, api_call, ttl=ttl,
                                 callback=api_callback, on_error=on_error,
                                 on_retry=on_retry,
                                 max_retries=max_retries, retry_delay=retry_delay)

    # ── AppState 信号订阅 ──

    def subscribe_dashboard(self, callback):
        """订阅全局仪表盘数据广播"""
        def _handler(data):
            callback(data)
        # 断开旧连接（防止重复订阅）
        if hasattr(self, '_dashboard_sub') and self._dashboard_sub:
            try:
                self._state.admin_dashboard_updated.disconnect(self._dashboard_sub)
            except Exception:
                pass
        self._dashboard_sub = _handler
        self._state.admin_dashboard_updated.connect(_handler)

    def subscribe_component(self, component: str, callback):
        """订阅指定组件数据更新"""
        def _handler(name, data):
            if name == component:
                callback(data)
        key = f"component_sub_{component}"
        if key in self._subscriptions:
            try:
                self._state.admin_component_updated.disconnect(self._subscriptions[key])
            except Exception:
                pass
        self._subscriptions[key] = _handler
        self._state.admin_component_updated.connect(_handler)

    def unsubscribe_all(self):
        """取消所有订阅"""
        for key, handler in list(self._subscriptions.items()):
            try:
                self._state.admin_component_updated.disconnect(handler)
            except Exception:
                pass
        if hasattr(self, '_dashboard_sub') and self._dashboard_sub:
            try:
                self._state.admin_dashboard_updated.disconnect(self._dashboard_sub)
            except Exception:
                pass


# ═══════════════════════════════════════════════════════════
# SystemResourcePanel 包装类 — v1.0.0 新增
# ═══════════════════════════════════════════════════════════

class SystemResourcePanel(CachedPanelMixin, _RefreshMixin, _SystemResourcePanelBase):
    """
    系统资源监控面板（包装类） — v1.0.0 新增

    继承 CachedPanelMixin 以使用统一缓存逻辑
    接入 Dashboard 广播系统，自动同步后端状态
    """

    CACHE_TTL = {"resources": 30}  # 30秒 TTL

    def __init__(self, app_state, parent=None):
        super().__init__(app_state, parent)
        # 接入 Dashboard 广播
        self.subscribe_dashboard(self._on_dashboard_broadcast)

    def _on_dashboard_broadcast(self, data: dict):
        """处理 Dashboard 广播，更新资源统计"""
        # 减少独立API调用，利用广播数据更新统计
        # 资源数据仍需独立获取，但可以记录Dashboard状态
        pass


# ═══════════════════════════════════════════════════════════
# 子面板：全局概览
# ═══════════════════════════════════════════════════════════

class DashboardOverview(CachedPanelMixin, QWidget):
    """
    全局管理概览面板（Dashboard）

    策略变更 (v1.0.0):
    - 继承 CachedPanelMixin，启用 Cache-First 模式
    - 订阅 AppState.admin_dashboard_updated 信号，数据来自统一广播源
    - 刷新时触发 AppState.broadcast_admin_dashboard()，广播给所有面板
    - 数据写入缓存供其他面板复用，实现一次请求多处使用
    """

    CACHE_TTL = {"dashboard": 300}  # 5分钟 TTL

    def __init__(self, app_state, parent=None):
        super().__init__(parent)  # 会自动调用 CachedPanelMixin 和 QWidget 的 __init__
        self._state = app_state
        self._init_ui()
        # 订阅 AppState 全局广播（连接后自动收到数据）
        self.subscribe_dashboard(self._on_broadcast)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("全局管理概览", self.refresh, use_action_button=True)
        layout.addLayout(header)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        self._main_layout = QVBoxLayout(content)
        self._main_layout.setSpacing(12)
        self._main_layout.setContentsMargins(4, 4, 4, 4)

        # 指标卡片行
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)
        self._metric_cards: Dict[str, QLabel] = {}
        for key, title, color in [
            ("load", "已加载模块", "#00d4aa"),
            ("llm", "LLM状态", "#6366f1"),
            ("chain", "链路节点", "#f59e0b"),
            ("claw", "Claw任务", "#00d4aa"),
            ("memory", "知识条目", "#e74c3c"),
            ("evolution", "进化计划", "#2ecc71"),
        ]:
            card = _metric_card(title, "--", color)
            cards_layout.addWidget(card)
            self._metric_cards[key] = card.findChild(QLabel)  # value label
        cards_layout.addStretch()
        self._main_layout.addLayout(cards_layout)

        # 阶段三：快速入口区块（跨面板导航）
        quick_group = _section_group("⚡ 快速入口")
        quick_layout = QHBoxLayout(quick_group)
        quick_layout.setSpacing(8)
        for group_name, _, keys in NAV_GROUPS:
            first_key = keys[0]
            btn = _link_button(group_name, first_key, self._state)
            quick_layout.addWidget(btn)
        quick_layout.addStretch()
        self._main_layout.addWidget(quick_group)

        # 各模块状态区域
        self._status_areas: Dict[str, QTextBrowser] = {}
        for section_name in [
            "引擎加载", "LLM管理", "主链路", "进化引擎",
            "记忆系统", "Claw调度", "系统组件",
        ]:
            group = _section_group(section_name)
            group_layout = QVBoxLayout(group)
            # v1.0.0: 使用统一函数，支持追加自定义样式
            text = _text_browser(max_height=160,
                                 extra_css="font-size: 11px; font-family: 'Microsoft YaHei', 'SimHei', monospace;")
            text.setOpenLinks(False)
            group_layout.addWidget(text)
            self._main_layout.addWidget(group)
            self._status_areas[section_name] = text

        # v1.0.0: 缓存统计可视化面板
        stats_group = _section_group("📊 缓存与网络统计 (v1.0.0)")
        stats_layout = QHBoxLayout(stats_group)
        stats_layout.setSpacing(16)

        # 缓存命中率
        self._card_hit_rate = _metric_card("缓存命中率", "N/A", "#2ecc71")  # v1.0.0: 统一命名
        stats_layout.addWidget(self._card_hit_rate)

        # API 调用次数
        self._card_api_calls = _metric_card("API调用", "0", "#00d4aa")  # v1.0.0: 统一命名+标题
        stats_layout.addWidget(self._card_api_calls)

        # API 失败率
        self._card_api_fail = _metric_card("API失败率", "0%", "#e74c3c")  # v1.0.0: 统一命名+标题
        stats_layout.addWidget(self._card_api_fail)

        # 重置按钮 - v1.0.0: 使用按钮工厂函数
        self._reset_stats_btn = _action_button("🔄 重置统计", "#95a5a6", (100, 32))
        self._reset_stats_btn.clicked.connect(self._reset_stats)
        stats_layout.addWidget(self._reset_stats_btn)

        stats_layout.addStretch()
        self._main_layout.addWidget(stats_group)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'neural'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'neural'])
        layout.addWidget(_related)

        self._main_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        # v1.0.0: 定时更新缓存统计
        self._stats_timer = QTimer(self)
        self._stats_timer.timeout.connect(self._update_cache_stats)
        self._stats_timer.start(5000)  # 每 5 秒更新一次

    def refresh(self):
        """
        刷新仪表盘数据 — 触发广播供所有面板复用

        v1.0.0 增强:
        - 添加加载状态指示（旋转图标风格）
        - 错误时自动恢复按钮
        - 5 秒超时保护
        """
        self._refresh_btn.setEnabled(False)
        self._refresh_btn.setText("⏳ 刷新中...")
        self._state.broadcast_admin_dashboard()

        # v1.0.0: 5 秒超时保护（防止广播丢失导致按钮卡死）
        QTimer.singleShot(5000, lambda: (
            self._refresh_btn.setEnabled(True),
            self._refresh_btn.setText("刷新")
        ))

    def _on_broadcast(self, data: dict):
        """处理来自 AppState 的全局广播数据"""
        self._refresh_btn.setEnabled(True)
        self._refresh_btn.setText("刷新")
        self._render_dashboard(data)

    def _on_dashboard(self, result: tuple):
        """处理手动刷新回调（保留兼容）"""
        self._refresh_btn.setEnabled(True)
        self._refresh_btn.setText("刷新")
        success, data, error = result
        if success and data:
            self._render_dashboard(data)

    def _render_dashboard(self, data: dict):
        """渲染仪表盘数据 — DashboardOverview + 订阅者共用"""
        if not data:
            for area in self._status_areas.values():
                area.setPlainText("暂无数据")
            return

        # 更新指标卡片
        lm = data.get("load_manager") or {}
        self._metric_cards["load"].setText(
            str(lm.get("loaded_count", 0) if isinstance(lm, dict) else "--")
        )

        llm = data.get("llm") or {}
        if isinstance(llm, dict):
            status = llm.get("status", "unknown")
            self._metric_cards["llm"].setText(STATUS_TEXT.get(status, status))
        else:
            self._metric_cards["llm"].setText("--")

        chain = data.get("chain") or {}
        if isinstance(chain, dict):
            self._metric_cards["chain"].setText(str(chain.get("total_nodes", 0)))
        else:
            self._metric_cards["chain"].setText("--")

        claw = data.get("claw") or {}
        if isinstance(claw, dict):
            self._metric_cards["claw"].setText(str(claw.get("active_tasks", 0)))
        else:
            self._metric_cards["claw"].setText("--")

        mem = data.get("memory") or {}
        if isinstance(mem, dict):
            self._metric_cards["memory"].setText(str(mem.get("total_knowledge", 0)))
        else:
            self._metric_cards["memory"].setText("--")

        evo = data.get("evolution") or {}
        if isinstance(evo, dict):
            plans = evo.get("active_plans", [])
            self._metric_cards["evolution"].setText(str(len(plans)))
        else:
            self._metric_cards["evolution"].setText("--")

        # 更新详情区域
        self._status_areas["引擎加载"].setPlainText(
            self._format_json(data.get("load_manager"))
        )
        self._status_areas["LLM管理"].setPlainText(
            self._format_json(data.get("llm"))
        )
        self._status_areas["主链路"].setPlainText(
            self._format_json(data.get("chain"))
        )
        self._status_areas["进化引擎"].setPlainText(
            self._format_json(data.get("evolution"))
        )
        self._status_areas["记忆系统"].setPlainText(
            self._format_json(data.get("memory"))
        )
        self._status_areas["Claw调度"].setPlainText(
            self._format_json(data.get("claw"))
        )
        self._status_areas["系统组件"].setPlainText(
            self._format_json(data.get("system"))
        )

        # v1.0.0: 同时更新缓存统计
        self._update_cache_stats()

    @staticmethod
    def _format_json(data) -> str:
        if not data:
            return "暂无数据"
        try:
            return json.dumps(data, ensure_ascii=False, indent=2, default=str)
        except Exception:
            return str(data)

    # ── v1.0.0: 缓存统计 ──────────────────────────────────

    def _update_cache_stats(self):
        """v1.0.0: 统一使用 Mixin 工具方法，启用颜色区分"""
        try:
            self.set_cache_stats_cards(
                self._card_hit_rate,
                self._card_api_calls,
                self._card_api_fail,
                color_threshold=True,
            )
        except Exception as e:
            logger.debug(f"更新缓存统计失败: {e}")

    def _reset_stats(self):
        """重置缓存统计"""
        self.reset_cache_stats()
        self._update_cache_stats()
        logger.info("[DashboardOverview] 缓存统计已重置")


# ═══════════════════════════════════════════════════════════
# 子面板：服务启停管理
# ═══════════════════════════════════════════════════════════

class StartupPanel(CachedPanelMixin, QWidget):
    """服务启停管理面板 — 统一控制后端/GUI 的启停"""

    CACHE_TTL = {"backend_status": 5}  # 后端状态 5秒 TTL

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._backend_alive = False
        self._gui_alive = True  # GUI 本身总是运行的
        self._init_ui()
        # v1.0.0: 订阅 Dashboard 广播，自动同步后端组件状态
        self.subscribe_dashboard(self._on_dashboard_broadcast)
        self._check_backend_status()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # 标题 - v1.0.0: 使用标题栏工具函数
        header, self._refresh_btn = _panel_header("🚀 服务启停管理", self._check_backend_status,
                                                  refresh_text="🔄 刷新状态")
        layout.addLayout(header)

        # 服务状态卡片
        cards = QHBoxLayout()
        cards.setSpacing(16)
        self._status_labels: Dict[str, tuple] = {}  # v1.0.0: 统一用字典跟踪状态标签

        # 后端服务卡片 - v1.0.0: 使用全局 _service_card() 函数
        self._backend_card, backend_status = _service_card("🖥️ 后端服务", "正在检测...", "#e74c3c", 180)
        self._status_labels["🖥️ 后端服务"] = (backend_status, "#e74c3c", self._backend_card)
        cards.addWidget(self._backend_card)

        # GUI 服务卡片 - v1.0.0: 使用全局 _service_card() 函数
        self._gui_card, gui_status = _service_card("🖼️ 前端 GUI", "运行中", "#2ecc71", 180)
        self._status_labels["🖼️ 前端 GUI"] = (gui_status, "#2ecc71", self._gui_card)
        cards.addWidget(self._gui_card)

        # 控制中心卡片 - v1.0.0: 使用全局 _service_card() 函数
        self._cc_card, cc_status = _service_card("📊 控制中心", "已集成", "#2ecc71", 180)
        self._status_labels["📊 控制中心"] = (cc_status, "#2ecc71", self._cc_card)
        cards.addWidget(self._cc_card)

        layout.addLayout(cards)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)

        # 操作按钮 - v1.0.0: 使用按钮工厂函数
        ops_group = _section_group("服务控制")
        ops_layout = QVBoxLayout(ops_group)

        btn_row1 = QHBoxLayout()
        self._start_backend_btn = _action_button("▶️ 启动后端", "#2ecc71", padding=(24, 10))
        self._start_backend_btn.clicked.connect(self._start_backend)
        btn_row1.addWidget(self._start_backend_btn)

        self._stop_backend_btn = _action_button("⏹️ 停止后端", "#e74c3c", padding=(24, 10))
        self._stop_backend_btn.clicked.connect(self._stop_backend)
        btn_row1.addWidget(self._stop_backend_btn)

        self._restart_backend_btn = _action_button("🔄 重启后端", "#00d4aa", padding=(24, 10))
        self._restart_backend_btn.clicked.connect(self._restart_backend)
        btn_row1.addWidget(self._restart_backend_btn)
        btn_row1.addStretch()
        ops_layout.addLayout(btn_row1)

        # 一键启动/停止 - v1.0.0: 使用按钮工厂函数
        btn_row2 = QHBoxLayout()
        self._start_all_btn = _action_button("🚀 一键启动全部", "#9b59b6", padding=(24, 10))
        self._start_all_btn.clicked.connect(self._start_all)
        btn_row2.addWidget(self._start_all_btn)

        self._stop_all_btn = _action_button("🛑 一键停止全部", "#1e293b", padding=(24, 10))
        self._stop_all_btn.clicked.connect(self._stop_all)
        btn_row2.addWidget(self._stop_all_btn)
        btn_row2.addStretch()
        ops_layout.addLayout(btn_row2)

        layout.addWidget(ops_group)

        # 日志区域 - v1.0.0: 使用统一 _text_browser() 函数
        log_group = _section_group("操作日志")
        log_layout = QVBoxLayout(log_group)
        self._log_text = _text_browser(max_height=200)
        self._log_text.setStyleSheet("""
            QTextBrowser {
                background: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                font-family: Consolas;
            }
        """)
        log_layout.addWidget(self._log_text)
        layout.addWidget(log_group)

        # 离线模式区域
        offline_group = _section_group("离线队列")
        offline_layout = QHBoxLayout(offline_group)
        offline_layout.setSpacing(12)

        self._offline_toggle = QCheckBox("🔌 离线模式")
        self._offline_toggle.setToolTip("开启后所有 API 请求将加入离线队列，联网后自动重放")
        self._offline_toggle.stateChanged.connect(self._toggle_offline_mode)
        offline_layout.addWidget(self._offline_toggle)

        self._pending_label = _info_label("待发送: 0 个")  # v1.0.0: 使用统一函数
        offline_layout.addWidget(self._pending_label)

        # v1.0.0: 使用按钮工厂函数
        self._replay_btn = _action_button("📤 重放队列", "#00d4aa", (90, 30))
        self._replay_btn.setEnabled(False)
        self._replay_btn.clicked.connect(self._replay_offline_queue)
        offline_layout.addWidget(self._replay_btn)

        offline_layout.addStretch()

        # 定时更新待发送数
        self._pending_timer = QTimer(self)
        self._pending_timer.timeout.connect(self._update_pending_count)
        self._pending_timer.start(3000)

        layout.addWidget(offline_group)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'config', 'system'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'config', 'system'])
        layout.addWidget(_related)

        layout.addStretch()

    def _check_backend_status(self):
        """检查后端服务状态（异步，不阻塞 GUI 线程）"""
        self._refresh_btn.setEnabled(False)
        self._refresh_btn.setText("检测中...")

        class _CheckWorker(QThread):
            """后台 socket 检测线程"""
            result = pyqtSignal(bool)

            def run(self):
                import socket
                try:
                    sock = socket.socket()
                    sock.settimeout(1)
                    sock.connect((DEFAULT_BACKEND_HOST, DEFAULT_BACKEND_PORT))
                    sock.close()
                    self.result.emit(True)
                except (OSError, ConnectionRefusedError, TimeoutError):
                    self.result.emit(False)

        self._check_worker = _CheckWorker(self)
        self._check_worker.result.connect(self._on_backend_check_result)
        self._check_worker.start()

    def _on_backend_check_result(self, alive: bool):
        """socket 检测完成回调"""
        self._backend_alive = alive
        if alive:
            self._api_calls += 1
        else:
            self._api_failures += 1
        self._update_backend_status(alive)
        self._refresh_btn.setEnabled(True)
        self._refresh_btn.setText("🔄 刷新状态")
        self._update_cache_stats()

    def _update_cache_stats(self):
        """v1.0.0: 统一使用 Mixin 工具方法"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    def _update_backend_status(self, alive: bool):
        """v1.0.0: 更新后端状态显示"""
        if not hasattr(self, '_status_labels'):
            return

        # 获取状态标签和卡片
        entry = self._status_labels.get("🖥️ 后端服务")
        if not entry:
            return

        status_label, _, backend_card = entry
        if alive:
            status_label.setText("✅ 运行中")
            status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ecc71;")
            backend_card.setStyleSheet("""
                QFrame {
                    background: white;
                    border: 2px solid #2ecc71;
                    border-radius: 8px;
                    padding: 16px;
                }
            """)
            self._start_backend_btn.setEnabled(False)
            self._stop_backend_btn.setEnabled(True)
            self._restart_backend_btn.setEnabled(True)
        else:
            status_label.setText("⛔ 已停止")
            status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")
            backend_card.setStyleSheet("""
                QFrame {
                    background: white;
                    border: 2px solid #e74c3c;
                    border-radius: 8px;
                    padding: 16px;
                }
            """)
            self._start_backend_btn.setEnabled(True)
            self._stop_backend_btn.setEnabled(False)
            self._restart_backend_btn.setEnabled(False)

    # v1.0.0: Dashboard 广播处理器 — 从组件数据自动同步状态
    def _on_dashboard_broadcast(self, data: dict):
        """处理 Dashboard 全局广播（自动更新后端状态）"""
        if not data:
            return
        # 读取组件状态
        components = data.get("components", {})
        api_server = components.get("api_server", {})
        somn_core = components.get("somn_core", {})
        # 后端运行 = api_server 和 somn_core 都 healthy
        api_ok = isinstance(api_server, dict) and api_server.get("status") == "healthy"
        core_ok = isinstance(somn_core, dict) and somn_core.get("status") == "healthy"
        backend_alive = api_ok and core_ok
        # 与当前状态对比，仅在变化时更新
        if backend_alive != self._backend_alive:
            self._backend_alive = backend_alive
            self._update_backend_status(backend_alive)
            status_str = "后端上线" if backend_alive else "后端离线"
            self._log(status_str)

    def _log(self, msg: str):
        """添加日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._log_text.append(f"[{timestamp}] {msg}")

    def _start_backend(self):
        """启动后端（异步，不阻塞 GUI 线程）"""
        self._start_backend_btn.setEnabled(False)
        self._log("🚀 正在启动后端服务...")

        import subprocess
        from pathlib import Path
        manager_script = Path(__file__).parent.parent.parent / "somn_manager.py"
        python_exe = Path(PYTHON_EXE_PATH)

        class _SubprocessWorker(QThread):
            """后台 subprocess 执行线程"""
            finished = pyqtSignal(bool, str)  # success, message

            def __init__(self, cmd):
                super().__init__()
                self._cmd = cmd

            def run(self):
                try:
                    result = subprocess.run(
                        self._cmd,
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                    if result.returncode == 0:
                        self.finished.emit(True, "后端启动命令已执行")
                    else:
                        self.finished.emit(False, f"后端启动返回: {result.returncode}")
                except Exception as e:
                    self.finished.emit(False, f"启动失败: {e}")

        cmd = [str(python_exe), str(manager_script), "start", "backend"]
        self._start_worker = _SubprocessWorker(cmd)
        self._start_worker.finished.connect(self._on_start_backend_result)
        self._start_worker.start()

    def _on_start_backend_result(self, success: bool, msg: str):
        """启动后端完成回调"""
        if success:
            self._log(f"✅ {msg}")
        else:
            self._log(f"⚠️ {msg}")
        # 等待后检查状态
        QTimer.singleShot(3000, self._check_backend_status)

    def _stop_backend(self):
        """停止后端（异步，不阻塞 GUI 线程）"""
        self._stop_backend_btn.setEnabled(False)
        self._log("⏹️ 正在停止后端服务...")

        import subprocess
        from pathlib import Path
        manager_script = Path(__file__).parent.parent.parent / "somn_manager.py"
        python_exe = Path(PYTHON_EXE_PATH)

        class _SubprocessWorker(QThread):
            """后台 subprocess 执行线程"""
            finished = pyqtSignal(bool, str)

            def __init__(self, cmd, timeout=30):
                super().__init__()
                self._cmd = cmd
                self._timeout = timeout

            def run(self):
                try:
                    result = subprocess.run(
                        self._cmd,
                        capture_output=True,
                        text=True,
                        timeout=self._timeout,
                    )
                    if result.returncode == 0:
                        self.finished.emit(True, "后端已停止")
                    else:
                        self.finished.emit(False, f"停止返回: {result.returncode}")
                except Exception as e:
                    self.finished.emit(False, f"停止失败: {e}")

        cmd = [str(python_exe), str(manager_script), "stop", "backend"]
        self._stop_worker = _SubprocessWorker(cmd, timeout=30)
        self._stop_worker.finished.connect(self._on_stop_backend_result)
        self._stop_worker.start()

    def _on_stop_backend_result(self, success: bool, msg: str):
        """停止后端完成回调"""
        if success:
            self._log(f"✅ {msg}")
        else:
            self._log(f"⚠️ {msg}")
        self._check_backend_status()

    def _restart_backend(self):
        """重启后端（异步：先停止，完成后延迟启动）"""
        self._restart_backend_btn.setEnabled(False)
        self._log("🔄 正在重启后端...")

        # 临时替换 stop 回调，完成后自动启动
        original_stop_callback = self._on_stop_backend_result

        def _restart_after_stop(success, msg):
            original_stop_callback(success, msg)
            if success:
                QTimer.singleShot(2000, self._start_backend)
            else:
                self._log("⚠️ 重启失败: 停止后端未成功")

        self._on_stop_backend_result = _restart_after_stop
        self._stop_backend()

    def _start_all(self):
        """一键启动全部"""
        self._log("🚀 一键启动: 后端...")
        self._start_backend()

    def _stop_all(self):
        """一键停止全部"""
        self._log("🛑 一键停止: 后端...")
        self._stop_backend()

    def _toggle_offline_mode(self, state: int):
        """切换离线模式"""
        offline = bool(state)
        self._state.cache.set_offline(offline)
        if offline:
            self._log("🔌 已进入离线模式，API请求将入队")
            self._replay_btn.setEnabled(False)
        else:
            self._log("🌐 已退出离线模式")
            self._update_pending_count()

    def _update_pending_count(self):
        """更新待发送请求计数"""
        count = self._state.cache.get_pending_count()
        self._pending_label.setText(f"待发送: {count} 个")
        can_replay = count > 0 and self._state.connection_status.name == "CONNECTED"
        self._replay_btn.setEnabled(can_replay)

    def _replay_offline_queue(self):
        """重放离线请求队列"""
        self._replay_btn.setEnabled(False)
        self._log("📤 正在重放离线请求队列...")

        async def _replay():
            return await self._state.cache.replay_pending(self._state.api)

        def _done(count):
            self._log(f"✅ 已重放 {count} 个离线请求")
            self._update_pending_count()
            # 重放后刷新仪表盘
            self._state.broadcast_admin_dashboard()

        self._state.run_async(_replay(), callback=_done)


# ═══════════════════════════════════════════════════════════
# 子面板：统一配置管理
# ═══════════════════════════════════════════════════════════

class ConfigPanel(CachedPanelMixin, QWidget):
    """统一配置管理面板 — 管理 GUI 和后端配置"""

    CACHE_TTL = {"config": 0}  # 配置永不过期（手动刷新）

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        self._load_config()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("⚙️ 统一配置管理", self._load_config)
        self._refresh_btn.setText("🔄 重置")
        layout.addLayout(header)

        # Tab 页 - v1.0.0: 使用统一 Tab 样式
        tabs = _tab_widget()

        # 基础配置 Tab
        tabs.addTab(self._create_basic_tab(), "🌐 基础配置")
        # 后端连接 Tab
        tabs.addTab(self._create_backend_tab(), "🔗 后端连接")
        # 缓存配置 Tab
        tabs.addTab(self._create_cache_tab(), "💾 缓存配置")
        # 界面配置 Tab
        tabs.addTab(self._create_ui_tab(), "🎨 界面配置")

        layout.addWidget(tabs)

        # 保存按钮 - v1.0.0: 使用按钮工厂函数
        save_layout = QHBoxLayout()
        self._save_btn = _action_button("💾 保存配置", "#2ecc71", padding=(32, 10))
        self._save_btn.clicked.connect(self._save_config)
        self._reload_btn = _action_button("🔄 重载系统", "#00d4aa", padding=(32, 10))
        self._reload_btn.clicked.connect(self._reload_system)
        save_layout.addStretch()
        save_layout.addWidget(self._save_btn)
        save_layout.addWidget(self._reload_btn)
        layout.addLayout(save_layout)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'startup'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'startup'])
        layout.addWidget(_related)

        layout.addStretch()

    def _create_basic_tab(self) -> QWidget:
        """创建基础配置 Tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)

        # 工作空间
        self._workspace_input = QLineEdit()
        self._workspace_input.setPlaceholderText("工作空间目录路径")
        layout.addRow("工作空间:", self._workspace_input)

        # LLM 模型
        self._llm_model_input = QLineEdit()
        self._llm_model_input.setPlaceholderText("例如: gemma4-local-b")
        layout.addRow("LLM模型:", self._llm_model_input)

        # 最大并发
        self._max_concurrent_input = QSpinBox()
        self._max_concurrent_input.setRange(1, 16)
        self._max_concurrent_input.setSuffix(" 个")
        layout.addRow("最大并发:", self._max_concurrent_input)

        return widget

    def _create_backend_tab(self) -> QWidget:
        """创建后端连接 Tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)

        # 后端地址
        self._backend_url_input = QLineEdit()
        self._backend_url_input.setPlaceholderText(DEFAULT_BACKEND_URL)
        layout.addRow("后端地址:", self._backend_url_input)

        # API 前缀
        self._api_prefix_input = QLineEdit()
        self._api_prefix_input.setText("/api/v1")
        layout.addRow("API前缀:", self._api_prefix_input)

        # 连接超时
        self._connect_timeout_input = QSpinBox()
        self._connect_timeout_input.setRange(1, 60)
        self._connect_timeout_input.setSuffix(" 秒")
        layout.addRow("连接超时:", self._connect_timeout_input)

        # 请求超时
        self._request_timeout_input = QSpinBox()
        self._request_timeout_input.setRange(10, 300)
        self._request_timeout_input.setSuffix(" 秒")
        layout.addRow("请求超时:", self._request_timeout_input)

        return widget

    def _create_cache_tab(self) -> QWidget:
        """创建缓存配置 Tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)

        # 缓存路径
        self._cache_path_input = QLineEdit()
        self._cache_path_input.setPlaceholderText("cache_data/cache.db")
        layout.addRow("缓存路径:", self._cache_path_input)

        # 默认 TTL
        self._cache_ttl_input = QSpinBox()
        self._cache_ttl_input.setRange(60, 86400)
        self._cache_ttl_input.setSuffix(" 秒")
        layout.addRow("默认TTL:", self._cache_ttl_input)

        # 知识 TTL
        self._knowledge_ttl_input = QSpinBox()
        self._knowledge_ttl_input.setRange(300, 604800)
        self._knowledge_ttl_input.setSuffix(" 秒")
        layout.addRow("知识TTL:", self._knowledge_ttl_input)

        # 状态 TTL
        self._status_ttl_input = QSpinBox()
        self._status_ttl_input.setRange(30, 3600)
        self._status_ttl_input.setSuffix(" 秒")
        layout.addRow("状态TTL:", self._status_ttl_input)

        return widget

    def _create_ui_tab(self) -> QWidget:
        """创建界面配置 Tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)

        # 主题
        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["auto", "light", "dark"])
        layout.addRow("界面主题:", self._theme_combo)

        # 字体大小
        self._font_size_input = QSpinBox()
        self._font_size_input.setRange(10, 20)
        self._font_size_input.setSuffix(" px")
        layout.addRow("字体大小:", self._font_size_input)

        # 动画效果
        self._animation_check = QCheckBox("启用动画效果")
        self._animation_check.setChecked(True)
        layout.addRow("", self._animation_check)

        return widget

    def _load_config(self):
        """加载配置到表单"""
        config = self._state.config

        # 基础配置
        self._workspace_input.setText(config.get("workspace", ""))
        self._llm_model_input.setText(config.get("llm.model", "gemma4-local-b"))
        self._max_concurrent_input.setValue(config.get("max_concurrent", 4))

        # 后端连接
        backend = config.get("backend", {})
        self._backend_url_input.setText(backend.get("server_url", ""))
        self._api_prefix_input.setText(backend.get("api_prefix", "/api/v1"))
        self._connect_timeout_input.setValue(backend.get("connect_timeout", 5))
        self._request_timeout_input.setValue(backend.get("request_timeout", 120))

        # 缓存配置
        cache = config.get("cache", {})
        self._cache_path_input.setText(cache.get("db_path", "cache_data/cache.db"))
        self._cache_ttl_input.setValue(cache.get("default_ttl", 1800))
        self._knowledge_ttl_input.setValue(cache.get("knowledge_ttl", 86400))
        self._status_ttl_input.setValue(cache.get("status_ttl", 300))

        # 界面配置
        ui = config.get("ui", {})
        theme = ui.get("theme", "auto")
        idx = self._theme_combo.findText(theme)
        if idx >= 0:
            self._theme_combo.setCurrentIndex(idx)
        self._font_size_input.setValue(ui.get("font_size", 12))
        self._animation_check.setChecked(ui.get("animation", True))

    def _save_config(self):
        """保存配置"""
        try:
            config = self._state.config

            # 基础配置
            config.set("workspace", self._workspace_input.text())
            config.set("llm.model", self._llm_model_input.text())
            config.set("max_concurrent", self._max_concurrent_input.value())

            # 后端连接
            config.set("backend.server_url", self._backend_url_input.text())
            config.set("backend.api_prefix", self._api_prefix_input.text())
            config.set("backend.connect_timeout", self._connect_timeout_input.value())
            config.set("backend.request_timeout", self._request_timeout_input.value())

            # 缓存配置
            config.set("cache.db_path", self._cache_path_input.text())
            config.set("cache.default_ttl", self._cache_ttl_input.value())
            config.set("cache.knowledge_ttl", self._knowledge_ttl_input.value())
            config.set("cache.status_ttl", self._status_ttl_input.value())

            # 界面配置
            config.set("ui.theme", self._theme_combo.currentText())
            config.set("ui.font_size", self._font_size_input.value())
            config.set("ui.animation", self._animation_check.isChecked())

            # 保存到文件
            config.save()

            QMessageBox.information(self, "保存成功", "配置已保存，部分配置需要重启后端生效。")
            logger.info("配置已保存")
        except Exception as e:
            QMessageBox.warning(self, "保存失败", f"保存配置失败: {e}")
            logger.error(f"配置保存失败: {e}")

    def _reload_system(self):
        """重载系统"""
        reply = QMessageBox.question(
            self, "确认重载", "确定要重载系统吗？这将断开并重新连接后端。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._state.run_async(self._state.disconnect_backend())
            self._state.run_async(self._state.connect_backend())
            QMessageBox.information(self, "重载中", "系统正在重载...")


# ═══════════════════════════════════════════════════════════
# 子面板：引擎加载管理
# ═══════════════════════════════════════════════════════════

class LoadManagerPanel(CachedPanelMixin, _RefreshMixin, QWidget):
    """引擎加载管理面板 — v1.0.0 继承 CachedPanelMixin, v1.0.0 接入组件订阅"""

    CACHE_TTL = {"load_status": 30}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # v1.0.0: 订阅组件更新广播
        self.subscribe_component("load_manager", self._on_load_manager_update)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("引擎加载管理", self._load_status)
        self._refresh_btn.setText("🔄 刷新状态")
        layout.addLayout(header)

        # 统计卡片
        cards = QHBoxLayout()
        cards.setSpacing(10)
        self._card_total = _metric_card("总模块数", "--", "#00d4aa")
        self._card_loaded = _metric_card("已加载", "--", "#2ecc71")
        self._card_pending = _metric_card("等待中", "--", "#95a5a6")
        self._card_failed = _metric_card("失败", "--", "#e74c3c")
        for c in [self._card_total, self._card_loaded, self._card_pending, self._card_failed]:
            cards.addWidget(c)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'startup', 'evolution'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'startup', 'evolution'])
        layout.addWidget(_related)

        cards.addStretch()
        layout.addLayout(cards)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)

        # 模块状态表格
        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["模块名", "状态", "优先级", "策略", "加载耗时(ms)"])
        _apply_table_style(self._table)  # v1.0.0
        layout.addWidget(self._table)

        # 预加载区 - v1.0.0: 使用按钮工厂函数
        preload_group = _section_group("手动预加载")
        preload_layout = QHBoxLayout(preload_group)
        self._module_input = QLineEdit()
        self._module_input.setPlaceholderText("输入模块名，多个用逗号分隔")
        self._preload_btn = _action_button("预加载", "#00d4aa", padding=(16, 6))
        self._preload_btn.clicked.connect(self._preload)
        preload_layout.addWidget(self._module_input)
        preload_layout.addWidget(self._preload_btn)
        layout.addWidget(preload_group)

    def _load_status(self):
        self._refresh_btn.setEnabled(False)
        worker = AdminWorker(self._state.api.admin_load_status)
        worker.finished.connect(self._on_status)
        worker.start()

    def _on_status(self, result: tuple):
        self._refresh_btn.setEnabled(True)
        success, data, error = result
        # v1.0.0: 更新API调用统计
        if success:
            self._api_calls += 1
        else:
            self._api_failures += 1
        self._update_cache_stats()
        if not success:
            return

        total = data.get("total", 0)
        loaded = data.get("loaded", 0)
        modules = data.get("modules", [])

        pending = failed = 0
        for m in modules:
            s = m.get("status", "pending")
            if s == "pending":
                pending += 1
            elif s in ("failed", "error"):
                failed += 1

        self._card_total.findChild(QLabel, None).setText(str(total))
        self._card_loaded.findChild(QLabel, None).setText(str(loaded))
        self._card_pending.findChild(QLabel, None).setText(str(pending))
        self._card_failed.findChild(QLabel, None).setText(str(failed))

        self._table.setRowCount(len(modules))
        for row, m in enumerate(modules):
            self._table.setItem(row, 0, QTableWidgetItem(m.get("name", "")))

            status = m.get("status", "pending")
            status_item = QTableWidgetItem(STATUS_TEXT.get(status, status))
            color = QColor(STATUS_COLORS.get(status, "#95a5a6"))
            status_item.setForeground(color)
            self._table.setItem(row, 1, status_item)

            self._table.setItem(row, 2, QTableWidgetItem(m.get("priority", "")))
            self._table.setItem(row, 3, QTableWidgetItem(m.get("strategy", "")))
            self._table.setItem(row, 4, QTableWidgetItem(str(m.get("load_time_ms", 0))))

    def _update_cache_stats(self):
        """v1.0.0: 统一使用 Mixin 工具方法"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    # v1.0.0: 处理组件广播数据
    def _on_load_manager_update(self, data: dict):
        """处理 load_manager 组件更新（来自全局广播）"""
        if not data:
            return
        # 基础统计
        total = data.get("registered", 0)
        loaded = data.get("loaded", 0)
        self._card_total.findChild(QLabel, None).setText(str(total))
        self._card_loaded.findChild(QLabel, None).setText(str(loaded))
        # 从模块列表计算 pending/failed
        modules = data.get("modules", [])
        pending = failed = 0
        for m in (modules if isinstance(modules, list) else []):
            s = m.get("status", "pending") if isinstance(m, dict) else str(m)
            if s == "pending":
                pending += 1
            elif s in ("failed", "error"):
                failed += 1
        self._card_pending.findChild(QLabel, None).setText(str(pending))
        self._card_failed.findChild(QLabel, None).setText(str(failed))
        # 更新表格（如果数据结构支持）
        status = data.get("status", {})
        if isinstance(status, dict) and status:
            mod_list = [{"name": k, "status": v} for k, v in status.items()]
            self._table.setRowCount(len(mod_list))
            for row, m in enumerate(mod_list):
                self._table.setItem(row, 0, QTableWidgetItem(m.get("name", "")))
                st = m.get("status", "unknown")
                status_item = QTableWidgetItem(STATUS_TEXT.get(st, st))
                color = QColor(STATUS_COLORS.get(st, "#95a5a6"))
                status_item.setForeground(color)
                self._table.setItem(row, 1, status_item)
                self._table.setItem(row, 2, QTableWidgetItem("--"))
                self._table.setItem(row, 3, QTableWidgetItem("--"))
                self._table.setItem(row, 4, QTableWidgetItem("--"))

    def _preload(self):
        text = self._module_input.text().strip()
        if not text:
            return
        names = [n.strip() for n in text.split(",") if n.strip()]
        self._preload_btn.setEnabled(False)
        worker = AdminWorker(self._state.api.admin_preload_modules, names)
        worker.finished.connect(lambda r: (self._preload_btn.setEnabled(True), self._safe_refresh()))

        worker.start()


# ═══════════════════════════════════════════════════════════
# 子面板：LLM管理
# ═══════════════════════════════════════════════════════════

class LLMManagerPanel(CachedPanelMixin, _RefreshMixin, QWidget):
    """LLM双脑管理面板 — v1.0.0 继承 CachedPanelMixin, v1.0.0 接入组件订阅"""

    CACHE_TTL = {"llm_status": 60, "llm_sessions": 30}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # v1.0.0: 订阅组件更新广播
        self.subscribe_component("llm", self._on_llm_update)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("LLM双脑管理", self._refresh)
        layout.addLayout(header)

        # 状态卡片
        cards = QHBoxLayout()
        cards.setSpacing(10)
        self._card_status = _metric_card("运行状态", "--", "#9b59b6")
        self._card_model = _metric_card("当前模型", "--", "#00d4aa")
        self._card_sessions = _metric_card("活跃会话", "--", "#1abc9c")
        for c in [self._card_status, self._card_model, self._card_sessions]:
            cards.addWidget(c)
        cards.addStretch()
        layout.addLayout(cards)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)

        # 控制按钮 - v1.0.0: 使用按钮工厂函数
        ctrl = QHBoxLayout()
        self._start_btn = _action_button("启动引擎", "#2ecc71", padding=(24, 8))
        self._stop_btn = _action_button("停止引擎", "#e74c3c", padding=(24, 8))
        self._start_btn.clicked.connect(self._start)
        self._stop_btn.clicked.connect(self._stop)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'config'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'config'])
        layout.addWidget(_related)

        ctrl.addStretch()
        ctrl.addWidget(self._start_btn)
        ctrl.addWidget(self._stop_btn)
        layout.addLayout(ctrl)

        # 详细状态
        group = _section_group("详细状态")
        group_layout = QVBoxLayout(group)
        self._detail = _text_browser()  # v1.0.0: 使用统一函数
        group_layout.addWidget(self._detail)
        layout.addWidget(group)

        # 会话管理
        sessions_group = _section_group("会话管理")
        sessions_layout = QVBoxLayout(sessions_group)
        self._sessions_list = QListWidget()
        self._sessions_list.setMaximumHeight(200)
        sessions_layout.addWidget(self._sessions_list)
        clear_btn = QPushButton("清除选中会话")
        clear_btn.clicked.connect(self._clear_session)
        sessions_layout.addWidget(clear_btn)
        layout.addWidget(sessions_group)

    def _refresh(self):
        self._refresh_btn.setEnabled(False)
        worker = AdminWorker(self._state.api.admin_llm_status)
        worker.finished.connect(self._on_status)
        worker.start()

        worker2 = AdminWorker(self._state.api.admin_llm_sessions)
        worker2.finished.connect(self._on_sessions)
        worker2.start()

    def _on_status(self, result: tuple):
        success, data, error = result
        # v1.0.0: 更新API调用统计
        if success:
            self._api_calls += 1
        else:
            self._api_failures += 1
        self._update_cache_stats()

        if not success:
            self._refresh_btn.setEnabled(True)
            return

        status = data.get("status", "unknown")
        self._card_status.findChild(QLabel).setText(STATUS_TEXT.get(status, status))
        model = data.get("current_model", "未加载")
        if isinstance(model, str) and len(model) > 12:
            model = model[:12] + "..."
        self._card_model.findChild(QLabel).setText(model)
        self._detail.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        self._refresh_btn.setEnabled(True)

    def _on_sessions(self, result: tuple):
        success, data, error = result
        if success:
            self._api_calls += 1
        else:
            self._api_failures += 1
        self._update_cache_stats()

        if not success:
            return
        sessions = data.get("sessions", {})
        self._card_sessions.findChild(QLabel).setText(str(data.get("total", 0)))
        self._sessions_list.clear()
        for sid, info in sessions.items():
            self._sessions_list.addItem(
                f"{sid}  |  消息数: {info.get('message_count', 0)}  |  {info.get('last_message', '')}"
            )

    def _update_cache_stats(self):
        """v1.0.0: 统一使用 Mixin 工具方法"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    def _start(self):
        self._start_btn.setEnabled(False)
        worker = AdminWorker(self._state.api.admin_llm_start)
        worker.finished.connect(lambda r: (self._start_btn.setEnabled(True), self._safe_refresh()))
        worker.start()

    def _stop(self):
        self._stop_btn.setEnabled(False)
        worker = AdminWorker(self._state.api.admin_llm_stop)
        worker.finished.connect(lambda r: (self._stop_btn.setEnabled(True), self._safe_refresh()))
        worker.start()

    def _clear_session(self):
        item = self._sessions_list.currentItem()
        if not item:
            return
        sid = item.text().split("  |  ")[0].strip()
        worker = AdminWorker(self._state.api.admin_llm_clear_session, sid)
        worker.finished.connect(lambda r: self._safe_refresh())
        worker.start()

    # v1.0.0: 处理组件广播数据
    def _on_llm_update(self, data: dict):
        """处理 llm 组件更新（来自全局广播）"""
        if not data:
            return
        # 状态卡片
        status = data.get("state", "unknown")
        self._card_status.findChild(QLabel).setText(STATUS_TEXT.get(status, status))
        # 模型卡片
        engine = data.get("engine", {})
        if isinstance(engine, dict):
            model = engine.get("name", "未加载")
            if isinstance(model, str) and len(model) > 12:
                model = model[:12] + "..."
            self._card_model.findChild(QLabel).setText(model)
        # 会话数卡片
        sessions = data.get("sessions", {})
        session_count = len(sessions) if isinstance(sessions, dict) else data.get("total", 0)
        self._card_sessions.findChild(QLabel).setText(str(session_count))
        # 更新详情
        self._detail.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))


# ═══════════════════════════════════════════════════════════
# 子面板：主链路监控
# ═══════════════════════════════════════════════════════════

class ChainMonitorPanel(CachedPanelMixin, QWidget):
    """主链路监控面板 — v1.0.0 继承 CachedPanelMixin, v1.0.0 接入组件订阅"""

    CACHE_TTL = {"chain_health": 60, "chain_nodes": 60, "chain_modes": 120}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # v1.0.0: 订阅组件更新广播
        self.subscribe_component("chain", self._on_chain_update)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header(
            "主链路监控", self._refresh,
            extra_buttons=[("生成报告", self._gen_report)]
        )
        layout.addLayout(header)

        # 指标
        cards = QHBoxLayout()
        cards.setSpacing(10)
        self._card_health = _metric_card("链路健康", "--", "#e67e22")
        self._card_nodes = _metric_card("总节点", "--", "#00d4aa")
        self._card_modes = _metric_card("模式数", "--", "#1abc9c")
        for c in [self._card_health, self._card_nodes, self._card_modes]:
            cards.addWidget(c)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'load'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'load'])
        layout.addWidget(_related)

        cards.addStretch()
        layout.addLayout(cards)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)

        # Tab 切换 - v1.0.0: 使用统一 Tab 样式
        tabs = _tab_widget()
        self._health_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._health_text, "健康状态")

        self._nodes_table = QTableWidget()
        self._nodes_table.setColumnCount(4)
        self._nodes_table.setHorizontalHeaderLabels(["节点名", "状态", "处理量", "耗时"])
        _apply_table_style(self._nodes_table, max_height=None)  # v1.0.0
        tabs.addTab(self._nodes_table, "节点详情")

        self._modes_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._modes_text, "模式分布")

        self._report_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._report_text, "监控报告")

        layout.addWidget(tabs)

    def _refresh(self):
        self._refresh_btn.setEnabled(False)
        self._pending_workers = 3
        for api_call, handler in [
            (self._state.api.admin_chain_health, self._on_health),
            (self._state.api.admin_chain_nodes, self._on_nodes),
            (self._state.api.admin_chain_modes, self._on_modes),
        ]:
            w = AdminWorker(api_call)
            w.finished.connect(self._on_worker_done)
            w.finished.connect(handler)
            w.start()

    def _on_worker_done(self, result: tuple):
        """多 worker 完成计数，全部完成后才恢复刷新按钮并更新统计"""
        success, data, error = result
        if success:
            self._api_calls += 1
        else:
            self._api_failures += 1
        self._pending_workers = getattr(self, '_pending_workers', 1) - 1
        if self._pending_workers <= 0:
            self._refresh_btn.setEnabled(True)
            self._update_cache_stats()

    def _update_cache_stats(self):
        """v1.0.0: 统一使用 Mixin 工具方法"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    def _on_health(self, result: tuple):
        success, data, error = result
        if success and data:
            health = data.get("overall_health", "unknown")
            self._card_health.findChild(QLabel).setText(STATUS_TEXT.get(health, health))
            self._health_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))

    def _on_nodes(self, result: tuple):
        success, data, error = result
        if success and data:
            nodes = data.get("nodes", [])
            self._card_nodes.findChild(QLabel).setText(str(data.get("total", 0)))
            self._nodes_table.setRowCount(len(nodes))
            for row, n in enumerate(nodes):
                if isinstance(n, dict):
                    self._nodes_table.setItem(row, 0, QTableWidgetItem(str(n.get("name", ""))))
                    self._nodes_table.setItem(row, 1, QTableWidgetItem(str(n.get("status", ""))))
                    self._nodes_table.setItem(row, 2, QTableWidgetItem(str(n.get("processed", ""))))
                    self._nodes_table.setItem(row, 3, QTableWidgetItem(str(n.get("elapsed", ""))))
                elif isinstance(n, (list, tuple)):
                    for col, val in enumerate(n[:4]):
                        self._nodes_table.setItem(row, col, QTableWidgetItem(str(val)))

    def _on_modes(self, result: tuple):
        success, data, error = result
        if success:
            self._modes_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))
            if isinstance(data, dict):
                self._card_modes.findChild(QLabel).setText(str(len(data)))

    def _gen_report(self):
        self._report_btn.setEnabled(False)
        w = AdminWorker(self._state.api.admin_chain_report)
        w.finished.connect(lambda r: (
            self._report_btn.setEnabled(True),
            self._on_report(r),
        ))
        w.start()

    def _on_report(self, result: tuple):
        success, data, error = result
        if success and data:
            self._report_text.setPlainText(data.get("report", "无报告数据"))

    # v1.0.0: 处理组件广播数据
    def _on_chain_update(self, data: dict):
        """处理 chain 组件更新（来自全局广播）"""
        if not data:
            return
        health = data.get("health", "unknown")
        self._card_health.findChild(QLabel).setText(STATUS_TEXT.get(health, health))
        self._card_nodes.findChild(QLabel).setText(str(data.get("total_nodes", data.get("total_executions", 0))))
        self._health_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))


# ═══════════════════════════════════════════════════════════
# 子面板：自主进化
# ═══════════════════════════════════════════════════════════

class EvolutionPanel(CachedPanelMixin, QWidget):
    """自主进化管理面板 — v1.0.0 继承 CachedPanelMixin, v1.0.0 接入组件订阅"""

    CACHE_TTL = {"evolution_report": 120, "evolution_plans": 300, "evolution_viz": 300}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # v1.0.0: 订阅组件更新广播
        self.subscribe_component("evolution", self._on_evolution_update)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("自主进化引擎", self._refresh)
        layout.addLayout(header)

        # v1.0.0: 统计信息标签
        self._stats_label = _info_label("计划总数: -- | 活跃: --")
        layout.addWidget(self._stats_label)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)

        # 操作按钮 - v1.0.0: 使用按钮工厂函数
        ctrl = QHBoxLayout()
        self._diagnose_btn = _action_button("运行诊断", "#9b59b6", padding=(20, 8))
        self._diagnose_btn.clicked.connect(self._diagnose)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'load', 'memory'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'load', 'memory'])
        layout.addWidget(_related)

        ctrl.addStretch()
        ctrl.addWidget(self._diagnose_btn)
        layout.addLayout(ctrl)

        # Tab: 进化报告 / 进化计划 / 可视化 - v1.0.0: 使用统一 Tab 样式
        tabs = _tab_widget()

        self._report_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._report_text, "进化报告")

        self._plans_table = QTableWidget()
        self._plans_table.setColumnCount(6)
        self._plans_table.setHorizontalHeaderLabels(["ID", "类型", "目标", "状态", "优先级", "风险"])
        _apply_table_style(self._plans_table, max_height=None)  # v1.0.0
        tabs.addTab(self._plans_table, "进化计划")

        self._viz_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._viz_text, "进化可视化")

        layout.addWidget(tabs)

    def _refresh(self):
        self._refresh_btn.setEnabled(False)
        self._pending_workers = 3
        for api_call, handler in [
            (self._state.api.admin_evolution_report, self._on_report),
            (self._state.api.admin_evolution_plans, self._on_plans),
            (self._state.api.admin_evolution_visualizations, self._on_viz),
        ]:
            w = AdminWorker(api_call)
            w.finished.connect(self._on_worker_done)
            w.finished.connect(handler)
            w.start()

    def _on_worker_done(self, result: tuple):
        """多 worker 完成计数，全部完成后更新统计"""
        success, data, error = result
        if success:
            self._api_calls += 1
        else:
            self._api_failures += 1
        self._pending_workers = getattr(self, '_pending_workers', 1) - 1
        if self._pending_workers <= 0:
            self._refresh_btn.setEnabled(True)
            self._update_cache_stats()

    def _update_cache_stats(self):
        """v1.0.0: 统一使用 Mixin 工具方法"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    def _on_report(self, result: tuple):
        success, data, error = result
        if success:
            self._report_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))

    def _on_plans(self, result: tuple):
        success, data, error = result
        if success and data:
            plans = data.get("plans", [])
            self._plans_table.setRowCount(len(plans))
            for row, p in enumerate(plans):
                self._plans_table.setItem(row, 0, QTableWidgetItem(str(p.get("id", ""))))
                self._plans_table.setItem(row, 1, QTableWidgetItem(str(p.get("type", ""))))
                self._plans_table.setItem(row, 2, QTableWidgetItem(str(p.get("target", ""))))
                self._plans_table.setItem(row, 3, QTableWidgetItem(str(p.get("status", ""))))
                self._plans_table.setItem(row, 4, QTableWidgetItem(str(p.get("priority", ""))))
                self._plans_table.setItem(row, 5, QTableWidgetItem(str(p.get("risk", ""))))

    def _on_viz(self, result: tuple):
        success, data, error = result
        if success:
            self._viz_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))

    def _diagnose(self):
        self._diagnose_btn.setEnabled(False)
        w = AdminWorker(self._state.api.admin_evolution_diagnose)
        w.finished.connect(lambda r: (self._diagnose_btn.setEnabled(True), self._on_diagnose(r)))
        w.start()

    def _on_diagnose(self, result: tuple):
        success, data, error = result
        if success:
            self._report_text.setPlainText(
                "【诊断结果】\n" + json.dumps(data, ensure_ascii=False, indent=2, default=str)
            )

    # v1.0.0: 处理组件广播数据
    def _on_evolution_update(self, data: dict):
        """处理 evolution 组件更新（来自全局广播）"""
        if not data:
            return
        # v1.0.0: 更新统计标签
        plans = data.get("evolution_history", data.get("plans", []))
        active_count = sum(1 for p in (plans if isinstance(plans, list) else [])
                          if isinstance(p, dict) and p.get("status") == "active")
        total_count = len(plans) if isinstance(plans, list) else 0
        self._stats_label.setText(f"计划总数: {total_count} | 活跃: {active_count}")
        # 更新表格
        if isinstance(plans, list):
            self._plans_table.setRowCount(len(plans))
            for row, p in enumerate(plans[:20]):  # 最多显示20条
                if isinstance(p, dict):
                    self._plans_table.setItem(row, 0, QTableWidgetItem(str(p.get("id", row))))
                    self._plans_table.setItem(row, 1, QTableWidgetItem(str(p.get("type", ""))))
                    self._plans_table.setItem(row, 2, QTableWidgetItem(str(p.get("target", ""))))
                    self._plans_table.setItem(row, 3, QTableWidgetItem(str(p.get("status", ""))))
                    self._plans_table.setItem(row, 4, QTableWidgetItem(str(p.get("priority", ""))))
                    self._plans_table.setItem(row, 5, QTableWidgetItem(str(p.get("risk", ""))))


# ═══════════════════════════════════════════════════════════
# 子面板：记忆生命周期
# ═══════════════════════════════════════════════════════════

class MemoryLifecyclePanel(CachedPanelMixin, _RefreshMixin, QWidget):
    """记忆生命周期管理面板 — 知识库 + 跨模块闭环"""

    CACHE_TTL = {"memory_stats": 120, "knowledge_list": 300}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # 订阅组件更新广播
        self.subscribe_component("memory", self._on_memory_update)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("记忆生命周期管理", self._refresh)
        layout.addLayout(header)

        # 健康指标卡片
        cards = QHBoxLayout()
        cards.setSpacing(10)
        self._card_score = _metric_card("健康分数", "--", "#2ecc71")
        self._card_total = _metric_card("知识总数", "--", "#00d4aa")
        self._card_active = _metric_card("活跃", "--", "#27ae60")
        self._card_stale = _metric_card("陈旧", "--", "#e67e22")
        self._card_weak = _metric_card("薄弱", "--", "#e74c3c")
        for c in [self._card_score, self._card_total, self._card_active, self._card_stale, self._card_weak]:
            cards.addWidget(c)
        cards.addStretch()
        layout.addLayout(cards)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)


        # Tab - v1.0.0: 使用统一 Tab 样式
        tabs = _tab_widget()

        # 健康报告
        self._health_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._health_text, "健康报告")

        # 知识注册表
        reg_widget = QWidget()
        reg_layout = QVBoxLayout(reg_widget)
        # 筛选
        filter_bar = QHBoxLayout()
        self._cat_filter = QComboBox()
        self._cat_filter.setEditable(True)
        self._cat_filter.setPlaceholderText("分类筛选")
        self._status_filter = QComboBox()
        self._status_filter.addItems(["全部", "active", "stale", "weak", "reviewing", "archived"])
        filter_bar.addWidget(QLabel("分类:"))
        filter_bar.addWidget(self._cat_filter)
        filter_bar.addWidget(QLabel("状态:"))
        filter_bar.addWidget(self._status_filter)
        self._reg_btn = QPushButton("查询")
        self._reg_btn.clicked.connect(self._query_registry)
        filter_bar.addWidget(self._reg_btn)
        reg_layout.addLayout(filter_bar)
        self._reg_table = QTableWidget()
        self._reg_table.setColumnCount(5)
        self._reg_table.setHorizontalHeaderLabels(["ID", "概念", "分类", "状态", "置信度"])
        _apply_table_style(self._reg_table, max_height=None)  # v1.0.0
        reg_layout.addWidget(self._reg_table)
        tabs.addTab(reg_widget, "知识注册表")

        # 复习任务
        self._review_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        review_layout = QVBoxLayout()
        review_btn = QPushButton("获取复习任务")
        review_btn.clicked.connect(self._get_review_tasks)
        review_layout.addWidget(review_btn)
        review_layout.addWidget(self._review_text)
        review_widget = QWidget()
        review_widget.setLayout(review_layout)
        tabs.addTab(review_widget, "复习任务")

        layout.addWidget(tabs)

        # 操作按钮
        # 操作按钮 - v1.0.0: 使用按钮工厂函数
        ops = QHBoxLayout()
        self._decay_btn = _action_button("触发记忆衰减", "#e67e22", padding=(16, 6))
        self._decay_btn.clicked.connect(lambda: self._decay(force=False))
        self._force_decay_btn = _action_button("强制衰减", "#e74c3c", padding=(16, 6))
        self._force_decay_btn.clicked.connect(lambda: self._decay(force=True))

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'evolution', 'knowledge'])
        layout.addWidget(_related)

        ops.addStretch()
        ops.addWidget(self._decay_btn)
        ops.addWidget(self._force_decay_btn)
        layout.addLayout(ops)

    def _refresh(self):
        self._refresh_btn.setEnabled(False)
        w = AdminWorker(self._state.api.admin_memory_health)
        w.finished.connect(self._on_health)
        w.start()

    def _on_health(self, result: tuple):
        self._refresh_btn.setEnabled(True)
        success, data, error = result
        if not success:
            self._api_failures += 1  # v1.0.0: 记录失败调用
            self._update_cache_stats()
            return

        self._api_calls += 1  # v1.0.0: 记录成功调用
        self._card_score.findChild(QLabel).setText(str(data.get("health_score", "--")))
        self._card_total.findChild(QLabel).setText(str(data.get("total_knowledge", 0)))
        self._card_active.findChild(QLabel).setText(str(data.get("active_count", 0)))
        self._card_stale.findChild(QLabel).setText(str(data.get("stale_count", 0)))
        self._card_weak.findChild(QLabel).setText(str(data.get("weak_count", 0)))

        display = {k: v for k, v in data.items() if k not in ("weak_knowledge",)}
        self._health_text.setPlainText(json.dumps(display, ensure_ascii=False, indent=2, default=str))
        self._update_cache_stats()  # v1.0.0: 更新缓存统计

    def _query_registry(self):
        cat = self._cat_filter.currentText() or None
        status = self._status_filter.currentText()
        if status == "全部":
            status = None
        w = AdminWorker(self._state.api.admin_memory_registry, category=cat, status=status)
        w.finished.connect(self._on_registry)
        w.start()

    def _on_registry(self, result: tuple):
        success, data, error = result
        if not success:
            self._api_failures += 1  # v1.0.0: 记录失败调用
            self._update_cache_stats()
            return
        self._api_calls += 1  # v1.0.0: 记录成功调用
        items = data.get("items", [])
        self._reg_table.setRowCount(len(items))
        for row, item in enumerate(items):
            if isinstance(item, dict):
                self._reg_table.setItem(row, 0, QTableWidgetItem(str(item.get("knowledge_id", ""))))
                self._reg_table.setItem(row, 1, QTableWidgetItem(str(item.get("concept", ""))))
                self._reg_table.setItem(row, 2, QTableWidgetItem(str(item.get("category", ""))))
                self._reg_table.setItem(row, 3, QTableWidgetItem(str(item.get("status", ""))))
                self._reg_table.setItem(row, 4, QTableWidgetItem(str(item.get("confidence", ""))))
        self._update_cache_stats()  # v1.0.0: 更新缓存统计

    def _get_review_tasks(self):
        w = AdminWorker(self._state.api.admin_memory_review_tasks)
        w.finished.connect(self._on_review)
        w.start()

    def _on_review(self, result: tuple):
        success, data, error = result
        if success:
            tasks = data.get("tasks", [])
            if not tasks:
                self._review_text.setPlainText("暂无需要复习的知识")
            else:
                self._review_text.setPlainText(
                    json.dumps(tasks, ensure_ascii=False, indent=2, default=str)
                )

    def _decay(self, force=False):
        w = AdminWorker(self._state.api.admin_memory_decay, force=force)
        w.finished.connect(lambda r: self._safe_refresh())
        w.start()

    def _update_cache_stats(self):
        """v1.0.0: 更新缓存统计显示（使用 Mixin 工具方法）"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    # ── 数据流闭环回调 ──────────────────────────────────

    def _on_memory_update(self, data: dict):
        """处理记忆系统组件更新（来自全局广播）"""
        if not data:
            return
        # 更新健康指标卡片
        health_score = data.get("health_score", 0)
        self._card_score.findChild(QLabel).setText(f"{health_score:.1f}" if isinstance(health_score, (int, float)) else str(health_score))
        self._card_total.findChild(QLabel).setText(str(data.get("total_knowledge", "--")))


# ═══════════════════════════════════════════════════════════
# 子面板：Claw调度
# ═══════════════════════════════════════════════════════════

class ClawSchedulerPanel(CachedPanelMixin, _RefreshMixin, QWidget):
    """Claw调度管理面板 — 任务调度 + 跨模块数据闭环"""

    CACHE_TTL = {"claw_stats": 30, "claw_pool": 60}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # 订阅组件更新广播
        self.subscribe_component("claw", self._on_claw_component_update)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("Claw调度管理", self._refresh)
        layout.addLayout(header)

        # 统计卡片
        cards = QHBoxLayout()
        cards.setSpacing(10)
        self._card_dispatched = _metric_card("已调度", "--", "#00d4aa")
        self._card_completed = _metric_card("已完成", "--", "#2ecc71")
        self._card_failed = _metric_card("失败", "--", "#e74c3c")
        self._card_active = _metric_card("活跃任务", "--", "#e67e22")
        for c in [self._card_dispatched, self._card_completed, self._card_failed, self._card_active]:
            cards.addWidget(c)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'system'])
        layout.addWidget(_related)

        cards.addStretch()
        layout.addLayout(cards)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)

        # Tab - v1.0.0: 使用统一 Tab 样式
        tabs = _tab_widget()

        # 统计详情
        self._stats_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._stats_text, "调度统计")

        # 工作池
        self._pool_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._pool_text, "工作池")

        # Claw列表
        claw_widget = QWidget()
        claw_layout = QVBoxLayout(claw_widget)
        filter_bar = QHBoxLayout()
        self._dept_filter = QComboBox()
        self._dept_filter.setEditable(True)
        self._dept_filter.setPlaceholderText("部门筛选")
        self._school_filter = QComboBox()
        self._school_filter.setEditable(True)
        self._school_filter.setPlaceholderText("学派筛选")
        self._list_btn = QPushButton("列出Claw")
        self._list_btn.clicked.connect(self._list_claws)
        filter_bar.addWidget(QLabel("部门:"))
        filter_bar.addWidget(self._dept_filter)
        filter_bar.addWidget(QLabel("学派:"))
        filter_bar.addWidget(self._school_filter)
        filter_bar.addWidget(self._list_btn)
        claw_layout.addLayout(filter_bar)
        self._claw_list = QListWidget()
        claw_layout.addWidget(self._claw_list)
        tabs.addTab(claw_widget, "Claw列表")

        # 最近执行
        self._recent_text = _text_browser(extra_css="font-size: 12px;")  # v1.0.0
        tabs.addTab(self._recent_text, "最近执行")

        layout.addWidget(tabs)

        # 手动调度
        dispatch_group = _section_group("手动调度")
        dispatch_layout = QFormLayout(dispatch_group)
        self._query_input = QLineEdit()
        self._query_input.setPlaceholderText("输入查询内容")
        self._claw_name_input = QLineEdit()
        self._claw_name_input.setPlaceholderText("可选：指定Claw名称")
        self._dispatch_btn = _action_button("执行调度", "#1abc9c", padding=(24, 8))  # v1.0.0
        self._dispatch_btn.clicked.connect(self._dispatch)
        dispatch_layout.addRow("查询:", self._query_input)
        dispatch_layout.addRow("Claw:", self._claw_name_input)
        dispatch_layout.addRow(self._dispatch_btn)
        layout.addWidget(dispatch_group)

    def _refresh(self):
        self._refresh_btn.setEnabled(False)
        self._pending_refresh = 4
        for api_call, handler in [
            (self._state.api.admin_claw_stats, self._on_stats),
            (self._state.api.admin_claw_work_pool, self._on_pool),
            (self._state.api.admin_claw_recent, self._on_recent),
            (self._state.api.admin_claw_active_tasks, self._on_active_tasks),
        ]:
            w = AdminWorker(api_call)
            w.finished.connect(handler)
            w.start()

    def _claw_refresh_done(self):
        """所有 worker 完成后才重新启用刷新按钮"""
        self._pending_refresh = getattr(self, '_pending_refresh', 0) - 1
        if self._pending_refresh <= 0:
            self._refresh_btn.setEnabled(True)
            self._pending_refresh = 0

    def _on_stats(self, result: tuple):
        self._claw_refresh_done()
        success, data, error = result
        if not success:
            self._api_failures += 1  # v1.0.0: 记录失败调用
            self._update_cache_stats()
            return
        self._api_calls += 1  # v1.0.0: 记录成功调用
        self._card_dispatched.findChild(QLabel).setText(str(data.get("total_dispatched", 0)))
        self._card_completed.findChild(QLabel).setText(str(data.get("total_completed", 0)))
        self._card_failed.findChild(QLabel).setText(str(data.get("total_failed", 0)))
        self._card_active.findChild(QLabel).setText(str(data.get("active_tasks", 0)))
        self._stats_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        self._update_cache_stats()  # v1.0.0: 更新缓存统计

    def _on_pool(self, result: tuple):
        self._claw_refresh_done()
        success, data, error = result
        if success:
            self._pool_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))
            self._update_cache_stats()  # v1.0.0: 更新缓存统计

    def _on_recent(self, result: tuple):
        self._claw_refresh_done()
        success, data, error = result
        if success:
            self._recent_text.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))
            self._update_cache_stats()  # v1.0.0: 更新缓存统计

    def _on_active_tasks(self, result: tuple):
        self._claw_refresh_done()
        ok, data, err = result
        if ok and data:
            self._api_calls += 1  # v1.0.0: 记录成功调用
            tasks = data.get("tasks", [])
            if tasks:
                lines = [f"• {t}" if isinstance(t, str) else f"• {t.get('task_id', t.get('id', ''))} | {t.get('query', t.get('target_claw', ''))[:40]}" for t in tasks[:15]]
                self._stats_text.append(f"\n📋 活跃任务 ({len(tasks)}):\n" + "\n".join(lines))
            self._update_cache_stats()  # v1.0.0: 更新缓存统计

    def _list_claws(self):
        dept = self._dept_filter.currentText() or None
        school = self._school_filter.currentText() or None
        w = AdminWorker(self._state.api.admin_claw_list, department=dept, school=school)
        w.finished.connect(self._on_claw_list)
        w.start()

    def _on_claw_list(self, result: tuple):
        success, data, error = result
        if success:
            claws = data.get("claws", [])
            self._claw_list.clear()
            for c in claws:
                if isinstance(c, dict):
                    self._claw_list.addItem(f"{c.get('name', '')}  |  {c.get('department', '')}  |  {c.get('school', '')}")
                else:
                    self._claw_list.addItem(str(c))

    def _dispatch(self):
        query = self._query_input.text().strip()
        if not query:
            return
        claw_name = self._claw_name_input.text().strip() or None
        self._dispatch_btn.setEnabled(False)
        w = AdminWorker(self._state.api.admin_claw_dispatch, query=query, claw_name=claw_name)
        w.finished.connect(lambda r: (self._dispatch_btn.setEnabled(True), self._safe_refresh()))
        w.start()

    def _update_cache_stats(self):
        """v1.0.0: 更新缓存统计显示（使用 Mixin 工具方法）"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    # ── 数据流闭环回调 ──────────────────────────────────

    def _on_claw_component_update(self, data: dict):
        """处理 Claw 组件更新（来自全局广播）"""
        if not data:
            return
        # 更新统计卡片
        self._card_dispatched.findChild(QLabel).setText(str(data.get("total_dispatched", "--")))
        self._card_completed.findChild(QLabel).setText(str(data.get("total_completed", "--")))
        self._card_failed.findChild(QLabel).setText(str(data.get("total_failed", "--")))
        self._card_active.findChild(QLabel).setText(str(data.get("active_tasks", "--")))


# ═══════════════════════════════════════════════════════════
# 子面板：知识格子 (v1.0.0 新增)
# ═══════════════════════════════════════════════════════════

class KnowledgeCellsPanel(CachedPanelMixin, _RefreshMixin, QWidget):
    """知识格子管理面板 — 方法论知识库"""

    CACHE_TTL = {"cells_status": 30, "cells_list": 60}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # 标题栏
        header, self._refresh_btn = _panel_header("知识格子管理", self._refresh)
        layout.addLayout(header)

        # 统计卡片
        cards = QHBoxLayout()
        cards.setSpacing(10)
        self._card_total = _metric_card("总格子", "--", "#00d4aa")
        self._card_activations = _metric_card("总激活", "--", "#2ecc71")
        self._card_wisdom = _metric_card("智慧核心", "--", "#9b59b6")
        self._card_strategy = _metric_card("运营策略", "--", "#e67e22")
        for c in [self._card_total, self._card_activations, self._card_wisdom, self._card_strategy]:
            cards.addWidget(c)
        cards.addStretch()
        layout.addLayout(cards)

        # Tab
        tabs = _tab_widget()

        # 格子列表
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        filter_bar = QHBoxLayout()
        self._keyword_input = QLineEdit()
        self._keyword_input.setPlaceholderText("搜索关键词")
        self._search_btn = QPushButton("搜索")
        self._search_btn.clicked.connect(self._search_cells)
        self._list_all_btn = QPushButton("列出全部")
        self._list_all_btn.clicked.connect(self._list_all)
        filter_bar.addWidget(QLabel("关键词:"))
        filter_bar.addWidget(self._keyword_input)
        filter_bar.addWidget(self._search_btn)
        filter_bar.addWidget(self._list_all_btn)
        list_layout.addLayout(filter_bar)
        self._cells_table = QTableWidget()
        self._cells_table.setColumnCount(4)
        self._cells_table.setHorizontalHeaderLabels(["ID", "名称", "标签", "激活次数"])
        _apply_table_style(self._cells_table)
        list_layout.addWidget(self._cells_table)
        tabs.addTab(list_widget, "格子列表")

        # 知识查询
        query_widget = QWidget()
        query_layout = QVBoxLayout(query_widget)
        query_input_layout = QHBoxLayout()
        self._query_input = QLineEdit()
        self._query_input.setPlaceholderText("输入问题...")
        self._query_btn = _action_button("查询", "#1abc9c", padding=(24, 8))
        self._query_btn.clicked.connect(self._query_knowledge)
        query_input_layout.addWidget(self._query_input)
        query_input_layout.addWidget(self._query_btn)
        query_layout.addLayout(query_input_layout)
        self._query_result = _text_browser(max_height=300)
        query_layout.addWidget(self._query_result)
        tabs.addTab(query_widget, "知识查询")

        # 方法论检查
        check_widget = QWidget()
        check_layout = QVBoxLayout(check_widget)
        check_input_layout = QHBoxLayout()
        self._check_input = QTextEdit()
        self._check_input.setPlaceholderText("输入需要检查的内容...")
        self._check_input.setMaximumHeight(150)
        self._check_btn = _action_button("检查", "#e74c3c", padding=(24, 8))
        self._check_btn.clicked.connect(self._check_methodology)
        check_input_layout.addWidget(self._check_btn)
        check_layout.addLayout(check_input_layout)
        check_layout.addWidget(self._check_input)
        self._check_result = _text_browser(max_height=200)
        check_layout.addWidget(self._check_result)
        tabs.addTab(check_widget, "方法论检查")

        # 藏书阁集成
        lib_widget = QWidget()
        lib_layout = QVBoxLayout(lib_widget)
        lib_btns = QHBoxLayout()
        self._sync_btn = _action_button("同步到藏书阁", "#9b59b6", padding=(24, 8))
        self._sync_btn.clicked.connect(self._sync_to_library)
        self._lib_stats_btn = QPushButton("藏书阁统计")
        self._lib_stats_btn.clicked.connect(self._get_library_stats)
        lib_btns.addWidget(self._sync_btn)
        lib_btns.addWidget(self._lib_stats_btn)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'memory'])
        layout.addWidget(_related)

        lib_btns.addStretch()
        lib_layout.addLayout(lib_btns)
        self._lib_result = _text_browser()
        lib_layout.addWidget(self._lib_result)
        tabs.addTab(lib_widget, "藏书阁集成")

        layout.addWidget(tabs)

    def _refresh(self):
        self._refresh_btn.setEnabled(False)
        w = AdminWorker(self._state.api.cells_status)
        w.finished.connect(self._on_status)
        w.start()

    def _on_status(self, result: tuple):
        self._refresh_btn.setEnabled(True)
        success, data, error = result
        if success:
            self._card_total.findChild(QLabel).setText(str(data.get("total_cells", 0)))
            self._card_activations.findChild(QLabel).setText(str(data.get("total_activations", 0)))
            self._card_wisdom.findChild(QLabel).setText(str(data.get("cells_by_category", {}).get("A", 0)))
            self._card_strategy.findChild(QLabel).setText(str(data.get("cells_by_category", {}).get("B", 0)))

    def _list_all(self):
        w = AdminWorker(self._state.api.cells_list)
        w.finished.connect(self._on_cells_list)
        w.start()

    def _search_cells(self):
        keyword = self._keyword_input.text()
        if keyword:
            w = AdminWorker(lambda: self._state.api.cells_search(keyword))
            w.finished.connect(self._on_cells_list)
            w.start()

    def _on_cells_list(self, result: tuple):
        success, data, error = result
        if success:
            cells = data if isinstance(data, list) else []
            self._cells_table.setRowCount(len(cells))
            for i, cell in enumerate(cells):
                self._cells_table.setItem(i, 0, QTableWidgetItem(cell.get("cell_id", "")))
                self._cells_table.setItem(i, 1, QTableWidgetItem(cell.get("name", "")))
                self._cells_table.setItem(i, 2, QTableWidgetItem(", ".join(cell.get("tags", [])[:3])))
                self._cells_table.setItem(i, 3, QTableWidgetItem(str(cell.get("activation_count", 0))))
            self._cells_table.resizeColumnsToContents()

    def _query_knowledge(self):
        question = self._query_input.text()
        if not question:
            return
        self._query_btn.setEnabled(False)
        w = AdminWorker(lambda: self._state.api.cells_query(question))
        w.finished.connect(self._on_query_result)
        w.start()

    def _on_query_result(self, result: tuple):
        self._query_btn.setEnabled(True)
        success, data, error = result
        if success:
            self._query_result.setPlainText(f"答案:\n{data.get('answer', '')}\n\n相关格子: {data.get('cells_used', [])}")
        else:
            self._query_result.setPlainText(f"错误: {error}")

    def _check_methodology(self):
        content = self._check_input.toPlainText()
        if not content:
            return
        self._check_btn.setEnabled(False)
        w = AdminWorker(lambda: self._state.api.cells_check(content))
        w.finished.connect(self._on_check_result)
        w.start()

    def _on_check_result(self, result: tuple):
        self._check_btn.setEnabled(True)
        success, data, error = result
        if success:
            score = data.get('overall_score', 0)
            level = data.get('level', '未知')
            suggestions = "\n".join([f"• {s}" for s in data.get('suggestions', [])])
            self._check_result.setPlainText(f"评分: {score:.2f} | 等级: {level}\n\n建议:\n{suggestions}")
        else:
            self._check_result.setPlainText(f"错误: {error}")

    def _sync_to_library(self):
        self._sync_btn.setEnabled(False)
        w = AdminWorker(self._state.api.cells_library_sync)
        w.finished.connect(self._on_sync_result)
        w.start()

    def _on_sync_result(self, result: tuple):
        self._sync_btn.setEnabled(True)
        success, data, error = result
        if success:
            self._lib_result.setPlainText(f"同步完成!\n{json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            self._lib_result.setPlainText(f"错误: {error}")

    def _get_library_stats(self):
        w = AdminWorker(self._state.api.cells_library_stats)
        w.finished.connect(lambda r: self._on_lib_stats(r) if hasattr(self, '_on_lib_stats') else None)
        w.start()


# ═══════════════════════════════════════════════════════════
# 子面板：系统组件
# ═══════════════════════════════════════════════════════════

class SystemComponentsPanel(CachedPanelMixin, QWidget):
    """系统组件健康面板 — v1.0.0 继承 CachedPanelMixin, v1.0.0 接入组件订阅"""

    CACHE_TTL = {"system_components": 60}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # v1.0.0: 订阅组件更新广播
        self.subscribe_component("system", self._on_system_update)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # v1.0.0: 标题栏
        header, self._refresh_btn = _panel_header("系统组件健康", self._refresh)
        layout.addLayout(header)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        layout.addLayout(stats)

        # 组件状态表格
        self._table = QTableWidget()
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(["组件名", "状态", "详情", "最后检查"])
        _apply_table_style(self._table)  # v1.0.0
        self._table.cellDoubleClicked.connect(self._show_detail)
        layout.addWidget(self._table)

        # 详情面板
        self._detail = _text_browser(max_height=200)  # v1.0.0: 使用统一函数
        layout.addWidget(self._detail)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'startup', 'claw'])
        layout.addWidget(_related)


    def _refresh(self):
        self._refresh_btn.setEnabled(False)
        w = AdminWorker(self._state.api.admin_system_components)
        w.finished.connect(self._on_components)
        w.start()

    def _on_components(self, result: tuple):
        self._refresh_btn.setEnabled(True)
        success, data, error = result
        # v1.0.0: 更新API调用统计
        if success:
            self._api_calls += 1
        else:
            self._api_failures += 1
        self._update_cache_stats()

        if not success:
            return

        if isinstance(data, dict):
            rows = []
            for name, info in data.items():
                if isinstance(info, dict):
                    rows.append((name, info.get("status", "unknown"), info))
                else:
                    rows.append((name, str(info), {}))
        else:
            rows = [(str(data), "unknown", {})]

        self._table.setRowCount(len(rows))
        for row, (name, status, info) in enumerate(rows):
            self._table.setItem(row, 0, QTableWidgetItem(name))
            status_item = QTableWidgetItem(STATUS_TEXT.get(status.lower(), status))
            color = QColor(STATUS_COLORS.get(status.lower(), "#95a5a6"))
            status_item.setForeground(color)
            self._table.setItem(row, 1, status_item)
            detail_str = info.get("detail", "") if isinstance(info, dict) else ""
            self._table.setItem(row, 2, QTableWidgetItem(str(detail_str)[:60]))
            self._table.setItem(row, 3, QTableWidgetItem(str(info.get("last_check", "")) if isinstance(info, dict) else ""))

    def _update_cache_stats(self):
        """v1.0.0: 统一使用 Mixin 工具方法"""
        self.set_cache_stats_cards(self._card_hit_rate, self._card_api_calls, self._card_api_fail)

    def _show_detail(self, row: int, col: int):
        name_item = self._table.item(row, 0)
        if not name_item:
            return
        name = name_item.text()
        w = AdminWorker(self._state.api.admin_system_component_health, name)
        w.finished.connect(self._on_detail)
        w.start()

    def _on_detail(self, result: tuple):
        success, data, error = result
        if success:
            self._detail.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))

    # v1.0.0: 处理组件广播数据
    def _on_system_update(self, data: dict):
        """处理 system 组件更新（来自全局广播）"""
        if not data:
            return
        components = data.get("components", {})
        if isinstance(components, dict):
            rows = []
            for comp_name, info in components.items():
                if isinstance(info, dict):
                    rows.append((comp_name, info.get("status", "unknown"), info))
                else:
                    rows.append((comp_name, str(info), {}))
        else:
            rows = [(str(data), "unknown", {})]

        self._table.setRowCount(len(rows))
        for row, (comp_name, status, info) in enumerate(rows):
            self._table.setItem(row, 0, QTableWidgetItem(comp_name))
            status_item = QTableWidgetItem(STATUS_TEXT.get(status.lower(), status))
            color = QColor(STATUS_COLORS.get(status.lower(), "#95a5a6"))
            status_item.setForeground(color)
            self._table.setItem(row, 1, status_item)
            detail_str = info.get("detail", "") if isinstance(info, dict) else ""
            self._table.setItem(row, 2, QTableWidgetItem(str(detail_str)[:60]))
            self._table.setItem(row, 3, QTableWidgetItem(str(info.get("last_check", "")) if isinstance(info, dict) else ""))


# ═══════════════════════════════════════════════════════════
# 子面板：神经网络布局管理
# ═══════════════════════════════════════════════════════════

class NeuralLayoutPanel(CachedPanelMixin, QWidget):
    """
    神经网络布局管理面板 — 拓扑 / Phase / Bridge / 布局管理

    v1.0.0 增强: 继承 CachedPanelMixin，支持缓存命中率和数据流 Tab 统计
    v1.0.0: 接入组件订阅
    """

    CACHE_TTL = {"neural_status": 60, "phase_status": 120}

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        # v1.0.0: 订阅组件更新广播
        self.subscribe_component("neural", self._on_neural_update)

    # ── UI ────────────────────────────────────────────────

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)

        # 标题栏
        # v1.0.0: 标题栏
        hdr, self._refresh_btn = _panel_header("🧠 神经网络布局管理", self.refresh, use_action_button=True)
        root.addLayout(hdr)

        # v1.0.0: 缓存统计行 - 使用统一工具函数
        stats, self._card_hit_rate, self._card_api_calls, self._card_api_fail = _cache_stats_bar()
        root.addLayout(stats)

        # Tab 页 - v1.0.0: 使用统一 Tab 样式
        self._tabs = _tab_widget()

        # Tab 1 — 概览
        self._tab_overview = self._build_overview_tab()
        self._tabs.addTab(self._tab_overview, "概览")

        # Tab 2 — Phase 状态
        self._tab_phase = self._build_phase_tab()
        self._tabs.addTab(self._tab_phase, "Phase 状态")

        # Tab 3 — 布局管理
        self._tab_layouts = self._build_layouts_tab()
        self._tabs.addTab(self._tab_layouts, "布局管理")

        # Tab 4 — Bridge 状态
        self._tab_bridge = self._build_bridge_tab()
        self._tabs.addTab(self._tab_bridge, "Bridge")

        # Tab 5 — 数据流串联 (阶段四核心)
        self._tab_flow = self._build_dataflow_tab()
        self._tabs.addTab(self._tab_flow, "🔗 数据流")

        root.addWidget(self._tabs)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard', 'system_resource'])
        root.addWidget(_related)


    # ── Tab: 概览 ─────────────────────────────────────────

    def _build_overview_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        # 4 指标卡片
        cards = QHBoxLayout()
        cards.setSpacing(10)
        self._overview_metrics: Dict[str, QLabel] = {}
        for key, title, color in [
            ("neurons", "神经元", "#00d4aa"),
            ("synapses", "突触连接", "#e67e22"),
            ("clusters", "集群数", "#1abc9c"),
            ("phases", "Phase 活跃", "#9b59b6"),
        ]:
            card = _metric_card(title, "--", color)
            cards.addWidget(card)
            self._overview_metrics[key] = card.findChild(QLabel)
        cards.addStretch()
        lay.addLayout(cards)

        # 拓扑详情
        grp = _section_group("网络拓扑")
        gl = QVBoxLayout(grp)
        self._topo_table = QTableWidget()
        self._topo_table.setColumnCount(5)
        self._topo_table.setHorizontalHeaderLabels(["节点 ID", "名称", "类型", "状态", "连接度"])
        _apply_table_style(self._topo_table, max_height=260)  # v1.0.0
        gl.addWidget(self._topo_table)
        lay.addWidget(grp)

        # 操作按钮 - v1.0.0: 使用统一按钮工厂函数
        ops = QHBoxLayout()
        self._btn_activate = _action_button("⚡ 激活主链路", "#9b59b6", padding=(16, 8))
        self._btn_activate.clicked.connect(self._on_activate)
        self._btn_optimize = _action_button("🔬 优化集群", "#1abc9c", padding=(16, 8))
        self._btn_optimize.clicked.connect(self._on_optimize)
        ops.addWidget(self._btn_activate)
        ops.addWidget(self._btn_optimize)
        ops.addStretch()
        lay.addLayout(ops)

        # 执行历史
        grp2 = _section_group("执行历史 (最近 20 条)")
        gl2 = QVBoxLayout(grp2)
        self._history_table = QTableWidget()
        self._history_table.setColumnCount(4)
        self._history_table.setHorizontalHeaderLabels(["时间", "任务类型", "Phase", "结果"])
        _apply_table_style(self._history_table, max_height=200)  # v1.0.0
        gl2.addWidget(self._history_table)
        lay.addWidget(grp2)

        lay.addStretch()
        return w

    # ── Tab: Phase 状态 ───────────────────────────────────

    def _build_phase_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        self._phase_table = QTableWidget()
        self._phase_table.setColumnCount(5)
        self._phase_table.setHorizontalHeaderLabels(["Phase", "名称", "状态", "详情", "启动时间"])
        _apply_table_style(self._phase_table, max_height=220)  # v1.0.0
        lay.addWidget(self._phase_table)

        grp = _section_group("Phase 详细信息")
        gl = QVBoxLayout(grp)
        self._phase_detail = _text_browser(max_height=400)  # v1.0.0: 使用统一函数
        gl.addWidget(self._phase_detail)
        lay.addWidget(grp)

        lay.addStretch()
        return w

    # ── Tab: 布局管理 ─────────────────────────────────────

    def _build_layouts_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        hdr = QHBoxLayout()
        self._btn_create_layout = QPushButton("➕ 创建布局")
        self._btn_create_layout.clicked.connect(self._on_create_layout)
        self._btn_refresh_layouts = QPushButton("🔄 刷新列表")
        self._btn_refresh_layouts.clicked.connect(self._refresh_layouts)
        hdr.addWidget(self._btn_create_layout)
        hdr.addWidget(self._btn_refresh_layouts)
        hdr.addStretch()
        lay.addLayout(hdr)

        self._layouts_table = QTableWidget()
        self._layouts_table.setColumnCount(5)
        self._layouts_table.setHorizontalHeaderLabels(["布局 ID", "名称", "状态", "节点数", "创建时间"])
        _apply_table_style(self._layouts_table, max_height=None)  # v1.0.0
        lay.addWidget(self._layouts_table)

        # 操作行
        ops = QHBoxLayout()
        self._btn_switch_layout = QPushButton("🔀 切换到选中布局")
        self._btn_switch_layout.clicked.connect(self._on_switch_layout)
        self._btn_del_layout = _action_button("🗑️ 删除选中布局", "#e74c3c", flat=True)  # v1.0.0: 扁平红色按钮
        self._btn_del_layout.clicked.connect(self._on_delete_layout)
        ops.addWidget(self._btn_switch_layout)
        ops.addWidget(self._btn_del_layout)
        ops.addStretch()
        lay.addLayout(ops)

        lay.addStretch()
        return w

    # ── Tab: Bridge 状态 ──────────────────────────────────

    def _build_bridge_tab(self) -> QWidget:
        """
        Bridge 状态 Tab

        v1.0.0 增强:
        - 添加刷新按钮
        - 添加 Bridge 统计卡片
        - 显示连接状态
        """
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        # v1.0.0: Bridge 统计卡片
        stats_row = QHBoxLayout()
        self._bridge_connections_card = _metric_card("连接数", "0", "#00d4aa")
        self._bridge_bridges_card = _metric_card("Bridge数", "0", "#e67e22")
        self._bridge_status_card = _metric_card("状态", "--", "#2ecc71")
        stats_row.addWidget(self._bridge_connections_card)
        stats_row.addWidget(self._bridge_bridges_card)
        stats_row.addWidget(self._bridge_status_card)

        # v1.0.0: 刷新按钮 - v1.0.0: 使用按钮工厂函数
        self._bridge_refresh_btn = _action_button("🔄 刷新 Bridge", "#00d4aa", padding=(16, 6))
        self._bridge_refresh_btn.clicked.connect(self._load_bridge_status)
        stats_row.addWidget(self._bridge_refresh_btn)
        stats_row.addStretch()
        lay.addLayout(stats_row)

        self._bridge_info = _text_browser(min_height=300)  # v1.0.0: 使用统一函数
        lay.addWidget(self._bridge_info)

        # v1.0.0: Bridge 统计说明 - v1.0.0: 使用统一 _info_label()
        info_lbl = _info_label("💡 Bridge 连接神经网络各模块，负责信号路由与数据同步", font_size=11)
        lay.addWidget(info_lbl)

        lay.addStretch()
        return w

    # ── Tab: 数据流串联 (阶段四) ──────────────────────────
    # 展示神经→Claw→记忆 跨模块数据闭环

    def _build_dataflow_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        # 说明文字 - v1.0.0: 使用统一 _info_label()
        info = _info_label("🔗 展示神经网络、Claw调度、记忆系统之间的数据流动关系", font_size=12)
        lay.addWidget(info)

        # 三个模块的链路状态卡片
        flow_cards = QHBoxLayout()
        flow_cards.setSpacing(16)
        self._flow_neural_card = self._build_flow_card("🧠", "神经网络", "等待数据...", "#00d4aa")
        self._flow_claw_card = self._build_flow_card("🦀", "Claw调度", "等待数据...", "#e67e22")
        self._flow_mem_card = self._build_flow_card("💾", "记忆系统", "等待数据...", "#2ecc71")
        flow_cards.addWidget(self._flow_neural_card)
        flow_cards.addWidget(self._build_arrow())
        flow_cards.addWidget(self._flow_claw_card)
        flow_cards.addWidget(self._build_arrow())
        flow_cards.addWidget(self._flow_mem_card)
        flow_cards.addStretch()
        lay.addLayout(flow_cards)

        # 闭环指示器
        loop_label = QLabel("🔄 记忆强化 → 神经网络更新 → Claw可用性变化 → 记忆强化")
        loop_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #00d4aa, stop:0.33 #e67e22,
                    stop:0.66 #2ecc71, stop:1 #9b59b6);
                color: white; padding: 10px 16px; border-radius: 8px;
                font-weight: bold; font-size: 12px;
            }
        """)
        loop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(loop_label)

        # 数据流详情表格
        grp = _section_group("跨模块数据流记录 (最近 30 条)")
        gl = QVBoxLayout(grp)
        self._flow_table = QTableWidget()
        self._flow_table.setColumnCount(6)
        self._flow_table.setHorizontalHeaderLabels([
            "时间", "源模块", "目标模块", "数据类型", "数据量", "状态"
        ])
        _apply_table_style(self._flow_table, max_height=300)  # v1.0.0
        gl.addWidget(self._flow_table)
        lay.addWidget(grp)

        # 详细追踪日志
        grp2 = _section_group("追踪日志")
        gl2 = QVBoxLayout(grp2)
        self._flow_log = QTextEdit()
        self._flow_log.setReadOnly(True)
        self._flow_log.setMaximumHeight(200)
        self._flow_log.setStyleSheet("""
            QTextEdit { background:#1e1e1e; color:#d4d4d4; border:1px solid #3e3e42;
                       border-radius:4px; font-family:Consolas; font-size:12px; }
        """)
        gl2.addWidget(self._flow_log)
        lay.addWidget(grp2)

        # 操作按钮 - v1.0.0: 使用按钮工厂函数
        ops = QHBoxLayout()
        btn_refresh = _action_button("🔄 刷新数据流", "#00d4aa", padding=(20, 8))
        btn_refresh.clicked.connect(self._refresh_dataflow)
        btn_refresh_chain = _action_button("🔗 追踪执行链路", "#9b59b6", padding=(20, 8))
        btn_refresh_chain.clicked.connect(self._trace_execution_chain)
        ops.addWidget(btn_refresh)
        ops.addWidget(btn_refresh_chain)
        ops.addStretch()
        lay.addLayout(ops)

        lay.addStretch()
        return w

    def _build_flow_card(self, emoji: str, title: str, status: str, color: str) -> QWidget:
        """v1.0.0: 创建数据流模块状态卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        card.setFixedWidth(140)
        lay = QVBoxLayout(card)
        lay.setSpacing(6)

        # Emoji 标签
        emoji_lbl = QLabel(emoji)
        emoji_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emoji_lbl.setStyleSheet("font-size: 28px;")
        lay.addWidget(emoji_lbl)

        # 标题标签 - v1.0.0: 使用统一 _title_label()
        title_lbl = _title_label(title, font_size=13)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title_lbl)

        # 状态标签
        status_lbl = QLabel(status)
        status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_lbl.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: bold;")
        lay.addWidget(status_lbl)

        return card

    def _build_arrow(self) -> QWidget:
        """v1.0.0: 创建箭头图标"""
        arrow = QLabel("→")
        arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow.setStyleSheet("font-size: 24px; color: #95a5a6; font-weight: bold;")
        arrow.setFixedWidth(40)
        return arrow

    def _refresh_dataflow(self):
        """刷新数据流信息"""
        self._flow_log.append("[数据流] 开始刷新跨模块数据...")

        def _on_neural(neural_data):
            self._update_flow_card(self._flow_neural_card, "神经网络",
                                   self._summarize_neural(neural_data), "#00d4aa")

        def _on_claw(claw_data):
            self._update_flow_card(self._flow_claw_card, "Claw调度",
                                   self._summarize_claw(claw_data), "#e67e22")

        def _on_memory(mem_data):
            self._update_flow_card(self._flow_mem_card, "记忆系统",
                                   self._summarize_memory(mem_data), "#2ecc71")
            self._flow_log.append("[数据流] ✅ 全部模块数据已更新")

        # 并行获取三个模块数据
        self._load_module_data("neural", _on_neural)
        self._load_module_data("claw", _on_claw)
        self._load_module_data("memory", _on_memory)

    def _load_module_data(self, module: str, callback):
        """加载指定模块数据"""
        def _fetch():
            try:
                loop = asyncio.new_event_loop()
                if module == "neural":
                    resp = loop.run_until_complete(self._state.api.admin_neural_status())
                elif module == "claw":
                    resp = loop.run_until_complete(self._state.api.admin_claw_stats())
                else:
                    resp = loop.run_until_complete(self._state.api.admin_memory_stats())
                loop.close()
                return resp
            except Exception as e:
                return {"success": False, "error": str(e)}

        def _done(result):
            if result.get("success"):
                callback(result.get("data", {}))
            else:
                self._flow_log.append(f"[{module}] 加载失败: {result.get('error', 'unknown')}")

        import threading
        t = threading.Thread(target=lambda: _done(_fetch()), daemon=True)
        t.start()

    def _summarize_neural(self, data: dict) -> str:
        neurons = data.get("stats", {}).get("neuron_count", 0)
        return f"{neurons} 神经元"

    def _summarize_claw(self, data: dict) -> str:
        active = data.get("active_tasks", 0)
        total = data.get("total_tasks", 0)
        return f"{active}/{total} 活跃"

    def _summarize_memory(self, data: dict) -> str:
        total = data.get("total_knowledge", 0)
        return f"{total} 知识条目"

    def _update_flow_card(self, card: QFrame, title: str, status: str, color: str):
        """更新数据流卡片状态"""
        # 找到 status label 并更新
        for child in card.findChildren(QLabel):
            if child.text() not in ("🧠", "🦀", "💾") and child.text() not in ("神经网络", "Claw调度", "记忆系统"):
                child.setText(status)
                child.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: bold;")
                break

    def _trace_execution_chain(self):
        """
        追踪执行链路 — 从神经网络到 Claw 到记忆的完整闭环

        v1.0.0 增强:
        - 并行异步获取三模块数据（减少等待）
        - 计算链路健康指数
        - 详细的延迟/吞吐量统计
        - 链路状态评估（健康/警告/断开）
        """
        self._flow_log.append("[追踪] 🔗 开始追踪执行链路...")
        self._flow_table.setRowCount(0)
        trace_start = datetime.now()

        def _fetch():
            """并行获取三模块数据"""
            import concurrent.futures, asyncio as _asyncio
            loop = _asyncio.new_event_loop()

            def _call_neural():
                return loop.run_until_complete(self._state.api.admin_neural_status())

            def _call_claw():
                return loop.run_until_complete(self._state.api.admin_claw_stats())

            def _call_memory():
                return loop.run_until_complete(self._state.api.admin_memory_stats())

            results = {"neural": None, "claw": None, "memory": None}
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_neural = executor.submit(_call_neural)
                future_claw = executor.submit(_call_claw)
                future_memory = executor.submit(_call_memory)
                try:
                    results["neural"] = future_neural.result(timeout=10)
                    results["claw"] = future_claw.result(timeout=10)
                    results["memory"] = future_memory.result(timeout=10)
                except concurrent.futures.TimeoutError:
                    self._flow_log.append("[追踪] ⚠️ 部分模块响应超时")
                except Exception as e:
                    self._flow_log.append(f"[追踪] ❌ 获取数据异常: {e}")
            loop.close()
            return results

        def _done(results: dict):
            trace_end = datetime.now()
            latency_ms = int((trace_end - trace_start).total_seconds() * 1000)
            self._flow_log.append(f"[追踪] 📡 数据获取完成，耗时 {latency_ms}ms")

            neural = results.get("neural")
            claw = results.get("claw")
            memory = results.get("memory")

            if neural is None and claw is None and memory is None:
                self._flow_log.append("[追踪] ❌ 无法获取任何数据，请检查后端连接")
                self._update_loop_indicator("disconnected")
                return

            # ── 提取各模块指标 ──
            neural_data = neural.get("data", {}) if isinstance(neural, dict) else {}
            claw_data = claw.get("data", {}) if isinstance(claw, dict) else {}
            mem_data = memory.get("data", {}) if isinstance(memory, dict) else {}

            neurons = neural_data.get("stats", {}).get("neuron_count", 0)
            synapses = neural_data.get("stats", {}).get("synapse_count", 0)
            active_tasks = claw_data.get("active_tasks", 0)
            total_tasks = claw_data.get("total_tasks", 0)
            completed = claw_data.get("completed_tasks", 0)
            knowledge = mem_data.get("total_knowledge", 0)
            hits = mem_data.get("cache_hits", 0)
            misses = mem_data.get("cache_misses", 0)

            # ── 计算链路健康指数 ──
            health_scores = []
            if neurons > 0:
                health_scores.append(1.0)  # Neural 活跃
            if active_tasks > 0 or total_tasks > 0:
                health_scores.append(min(active_tasks / max(total_tasks, 1) * 2, 1.0))
            if knowledge > 0:
                health_scores.append(1.0)  # Memory 有数据
            loop_health = sum(health_scores) / len(health_scores) if health_scores else 0.0

            # 评估链路状态
            if loop_health >= 0.8:
                health_label = "🟢 健康"
                health_color = "#2ecc71"
            elif loop_health >= 0.4:
                health_label = "🟡 警告"
                health_color = "#f39c12"
            else:
                health_label = "🔴 断开"
                health_color = "#e74c3c"

            self._update_loop_indicator(health_label, health_color)
            self._flow_log.append(f"[追踪] 📊 链路健康指数: {loop_health:.0%} ({health_label})")

            # ── 构建数据流记录（包含更多指标）─
            records = []
            timestamp = datetime.now().strftime("%H:%M:%S")

            # Neural → Claw 链路
            records.append({
                "time": timestamp,
                "source": "神经网络",
                "target": "Claw调度",
                "type": "信号传播",
                "amount": f"{neurons}N/{synapses}S",
                "status": "活跃" if neurons > 0 else "空闲",
                "latency": f"{latency_ms // 3}ms"
            })

            # Claw → Memory 链路
            records.append({
                "time": timestamp,
                "source": "Claw调度",
                "target": "记忆系统",
                "type": "知识写入",
                "amount": f"{active_tasks}/{total_tasks}T",
                "status": "活跃" if active_tasks > 0 else "空闲",
                "latency": f"{completed} 完成"
            })

            # Memory → Neural 链路
            hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
            records.append({
                "time": timestamp,
                "source": "记忆系统",
                "target": "神经网络",
                "type": "记忆强化",
                "amount": f"{knowledge} 条/{hit_rate:.0%} 命中率",
                "status": "活跃" if knowledge > 0 else "空闲",
                "latency": f"{hits}H/{misses}M"
            })

            # ── 渲染表格（扩展为 7 列）─
            self._flow_table.setColumnCount(7)
            self._flow_table.setHorizontalHeaderLabels([
                "时间", "源模块", "目标模块", "数据类型", "数据量", "状态", "附加指标"
            ])
            self._flow_table.setRowCount(len(records))
            for i, rec in enumerate(records):
                self._flow_table.setItem(i, 0, QTableWidgetItem(rec["time"]))
                self._flow_table.setItem(i, 1, QTableWidgetItem(rec["source"]))
                self._flow_table.setItem(i, 2, QTableWidgetItem(rec["target"]))
                self._flow_table.setItem(i, 3, QTableWidgetItem(rec["type"]))
                self._flow_table.setItem(i, 4, QTableWidgetItem(rec["amount"]))
                status_item = QTableWidgetItem(rec["status"])
                color = QColor("#2ecc71") if rec["status"] == "活跃" else QColor("#95a5a6")
                status_item.setForeground(color)
                self._flow_table.setItem(i, 5, status_item)
                self._flow_table.setItem(i, 6, QTableWidgetItem(rec.get("latency", "")))

            self._flow_log.append(f"[追踪] ✅ 完成: {len(records)} 条链路记录 | 总延迟 {latency_ms}ms")

        import threading
        t = threading.Thread(target=lambda: _done(_fetch()), daemon=True)
        t.start()

    def _update_loop_indicator(self, status: str, color: str = "#2ecc71"):
        """更新闭环指示器的状态和颜色"""
        # 查找闭环指示器并更新
        for child in self.findChildren(QLabel):
            text = child.text()
            if "记忆强化" in text and "🔄" in text:
                child.setStyleSheet(f"""
                    QLabel {{
                        background: {color};
                        color: white; padding: 10px 16px; border-radius: 8px;
                        font-weight: bold; font-size: 12px;
                    }}
                """)
                break

    def _on_neural_update(self, data: dict):
        """处理神经网络组件更新（来自全局广播）"""
        if not data:
            return
        # 更新概览指标卡片
        stats = data.get("stats", {})
        if isinstance(stats, dict):
            neurons_label = self._overview_metrics.get("neurons")
            synapses_label = self._overview_metrics.get("synapses")
            if neurons_label:
                neurons_label.setText(str(stats.get("neuron_count", "--")))
            if synapses_label:
                synapses_label.setText(str(stats.get("synapse_count", "--")))
        # 刷新数据流视图
        self._refresh_dataflow()

    # ── 数据加载 ──────────────────────────────────────────

    def refresh(self):
        """刷新全部数据"""
        self._refresh_btn.setEnabled(False)
        self._refresh_btn.setText("加载中...")
        w = AdminWorker(self._state.api.admin_neural_status)
        w.finished.connect(self._on_status)
        w.start()

    def _on_status(self, result: tuple):
        self._refresh_btn.setEnabled(True)
        self._refresh_btn.setText("刷新")
        ok, data, err = result
        if not ok or not data:
            return

        # 指标卡片
        stats = data.get("stats", {}) or {}
        self._overview_metrics["neurons"].setText(str(stats.get("neuron_count", 0)))
        self._overview_metrics["synapses"].setText(str(stats.get("synapse_count", 0)))
        clusters = data.get("clusters", {}) or {}
        self._overview_metrics["clusters"].setText(str(len(clusters) if isinstance(clusters, (list, dict)) else 0))
        phases = data.get("phase_status", {}) or {}
        active = sum(1 for v in phases.values() if isinstance(v, dict) and str(v.get("status", "")).lower() == "active")
        self._overview_metrics["phases"].setText(f"{active}/{len(phases) if isinstance(phases, dict) else 0}")

        # 拓扑表格
        neurons = data.get("neurons", {}) or {}
        if isinstance(neurons, dict):
            items = list(neurons.items())[:50]
            self._topo_table.setRowCount(len(items))
            for i, (nid, info) in enumerate(items):
                if not isinstance(info, dict):
                    info = {}
                self._topo_table.setItem(i, 0, QTableWidgetItem(str(nid)[:30]))
                self._topo_table.setItem(i, 1, QTableWidgetItem(str(info.get("name", ""))[:20]))
                self._topo_table.setItem(i, 2, QTableWidgetItem(str(info.get("type", ""))[:15]))
                self._topo_table.setItem(i, 3, QTableWidgetItem(str(info.get("state", ""))[:15]))
                deg = info.get("degree", info.get("connections", 0))
                self._topo_table.setItem(i, 4, QTableWidgetItem(str(deg)))

        # 执行历史
        self._load_execution_history()
        # Phase 状态
        self._load_phase_status()
        # Bridge
        self._load_bridge_status()
        # 布局列表
        self._refresh_layouts()

    def _load_execution_history(self):
        w = AdminWorker(self._state.api.admin_neural_execution_history, 20)
        w.finished.connect(self._on_history)
        w.start()

    def _on_history(self, result: tuple):
        ok, data, err = result
        if not ok or not data:
            return
        history = data if isinstance(data, list) else data.get("history", [])
        self._history_table.setRowCount(len(history))
        for i, entry in enumerate(history[:20]):
            if not isinstance(entry, dict):
                entry = {}
            self._history_table.setItem(i, 0, QTableWidgetItem(str(entry.get("timestamp", ""))[:19]))
            self._history_table.setItem(i, 1, QTableWidgetItem(str(entry.get("task_type", entry.get("type", "")))[:20]))
            self._history_table.setItem(i, 2, QTableWidgetItem(str(entry.get("phase", ""))[:12]))
            self._history_table.setItem(i, 3, QTableWidgetItem(str(entry.get("result", entry.get("status", "")))[:30]))

    def _load_phase_status(self):
        w = AdminWorker(self._state.api.admin_neural_phase_status)
        w.finished.connect(self._on_phase)
        w.start()

    def _on_phase(self, result: tuple):
        ok, data, err = result
        if not ok or not data:
            return
        phases = data if isinstance(data, dict) else {}
        self._phase_table.setRowCount(len(phases))
        phase_names = {
            "phase1": "Phase 1 基础布局",
            "phase2": "Phase 2 信号路由",
            "phase3": "Phase 3 反馈循环",
            "phase4": "Phase 4 动态激活",
            "phase5": "Phase 5 涌现验证",
        }
        for i, (key, info) in enumerate(phases.items()):
            if not isinstance(info, dict):
                info = {"status": str(info)}
            self._phase_table.setItem(i, 0, QTableWidgetItem(str(key)))
            self._phase_table.setItem(i, 1, QTableWidgetItem(phase_names.get(key, key)))
            status = str(info.get("status", "unknown"))
            status_item = QTableWidgetItem(STATUS_TEXT.get(status.lower(), status))
            color = QColor(STATUS_COLORS.get(status.lower(), "#95a5a6"))
            status_item.setForeground(color)
            self._phase_table.setItem(i, 2, status_item)
            self._phase_table.setItem(i, 3, QTableWidgetItem(str(info.get("detail", ""))[:50]))
            self._phase_table.setItem(i, 4, QTableWidgetItem(str(info.get("started_at", ""))[:19]))
        self._phase_detail.setPlainText(json.dumps(phases, ensure_ascii=False, indent=2, default=str))

    def _load_bridge_status(self):
        """v1.0.0: 加载 Bridge 状态"""
        self._bridge_refresh_btn.setEnabled(False)
        self._bridge_refresh_btn.setText("⏳ 加载中...")
        w = AdminWorker(self._state.api.admin_neural_bridge_status)
        w.finished.connect(self._on_bridge)
        w.start()

    def _on_bridge(self, result: tuple):
        """v1.0.0: 更新 Bridge 状态，包含统计卡片"""
        ok, data, err = result
        self._bridge_refresh_btn.setEnabled(True)
        self._bridge_refresh_btn.setText("🔄 刷新 Bridge")

        if not ok:
            self._bridge_info.setPlainText(f"加载失败: {err}")
            # 更新状态卡片为错误
            for child in self._bridge_status_card.findChildren(QLabel):
                if child.text() not in ("状态",):
                    child.setText("❌ 错误")
                    child.setStyleSheet("color: #e74c3c; font-size: 18px; font-weight: bold;")
                    break
            return

        self._bridge_info.setPlainText(json.dumps(data, ensure_ascii=False, indent=2, default=str))

        # v1.0.0: 更新统计卡片
        if isinstance(data, dict):
            connections = data.get("connections", data.get("total_connections", 0))
            bridges = data.get("total_bridges", data.get("bridge_count", 0))
            status = data.get("status", "unknown")

            # 连接数
            for child in self._bridge_connections_card.findChildren(QLabel):
                if child.text() not in ("连接数",):
                    child.setText(str(connections))
                    break

            # Bridge 数
            for child in self._bridge_bridges_card.findChildren(QLabel):
                if child.text() not in ("Bridge数",):
                    child.setText(str(bridges))
                    break

            # 状态
            status_color = {"active": "#2ecc71", "idle": "#95a5a6", "error": "#e74c3c"}.get(
                str(status).lower(), "#f39c12"
            )
            for child in self._bridge_status_card.findChildren(QLabel):
                if child.text() not in ("状态",):
                    child.setText(STATUS_TEXT.get(str(status).lower(), str(status)))
                    child.setStyleSheet(f"color: {status_color}; font-size: 18px; font-weight: bold;")
                    break

    def _refresh_layouts(self):
        w = AdminWorker(self._state.api.admin_neural_layouts)
        w.finished.connect(self._on_layouts)
        w.start()

    def _on_layouts(self, result: tuple):
        ok, data, err = result
        if not ok or not data:
            return
        layouts = data if isinstance(data, list) else data.get("layouts", [])
        self._layouts_table.setRowCount(len(layouts))
        for i, l in enumerate(layouts):
            if not isinstance(l, dict):
                l = {}
            self._layouts_table.setItem(i, 0, QTableWidgetItem(str(l.get("id", l.get("layout_id", "")))[:24]))
            self._layouts_table.setItem(i, 1, QTableWidgetItem(str(l.get("name", ""))[:20]))
            is_active = l.get("is_active", l.get("active", False))
            self._layouts_table.setItem(i, 2, QTableWidgetItem("✅ 活跃" if is_active else "空闲"))
            self._layouts_table.setItem(i, 3, QTableWidgetItem(str(l.get("neuron_count", l.get("nodes", 0)))))
            self._layouts_table.setItem(i, 4, QTableWidgetItem(str(l.get("created_at", ""))[:19]))

    # ── 操作 ──────────────────────────────────────────────

    def _on_activate(self):
        self._btn_activate.setEnabled(False)
        self._btn_activate.setText("激活中...")
        w = AdminWorker(self._state.api.admin_neural_activate, {"query": "手动激活测试"})
        w.finished.connect(self._on_activate_done)
        w.start()

    def _on_activate_done(self, result: tuple):
        self._btn_activate.setEnabled(True)
        self._btn_activate.setText("⚡ 激活主链路")
        ok, data, err = result
        if ok:
            QMessageBox.information(self, "激活结果", json.dumps(data, ensure_ascii=False, indent=2, default=str)[:500])

    def _on_optimize(self):
        self._btn_optimize.setEnabled(False)
        self._btn_optimize.setText("优化中...")
        w = AdminWorker(self._state.api.admin_neural_optimize_clusters)
        w.finished.connect(self._on_optimize_done)
        w.start()

    def _on_optimize_done(self, result: tuple):
        self._btn_optimize.setEnabled(True)
        self._btn_optimize.setText("🔬 优化集群")
        ok, data, err = result
        if ok:
            QMessageBox.information(self, "优化结果", json.dumps(data, ensure_ascii=False, indent=2, default=str)[:500])

    def _on_create_layout(self):
        name, ok = QInputDialog.getText(self, "创建布局", "布局名称:")
        if not ok or not name.strip():
            return
        self._btn_create_layout.setEnabled(False)
        self._btn_create_layout.setText("创建中...")
        w = AdminWorker(self._state.api.admin_neural_create_layout, name.strip())
        w.finished.connect(self._on_create_done)
        w.start()

    def _on_create_done(self, result: tuple):
        self._btn_create_layout.setEnabled(True)
        self._btn_create_layout.setText("➕ 创建布局")
        ok, data, err = result
        if ok:
            QMessageBox.information(self, "创建成功", f"布局已创建")
            self._refresh_layouts()
        else:
            QMessageBox.warning(self, "创建失败", f"创建布局失败: {err}")

    def _on_switch_layout(self):
        row = self._layouts_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请先选择一个布局")
            return
        item = self._layouts_table.item(row, 0)
        if not item:
            return
        layout_id = item.text()
        self._btn_switch_layout.setEnabled(False)
        self._btn_switch_layout.setText("切换中...")
        w = AdminWorker(self._state.api.admin_neural_switch_layout, layout_id)
        w.finished.connect(self._on_switch_done)
        w.start()

    def _on_switch_done(self, result: tuple):
        self._btn_switch_layout.setEnabled(True)
        self._btn_switch_layout.setText("🔀 切换到选中布局")
        ok, data, err = result
        if ok:
            QMessageBox.information(self, "切换成功", f"已切换到新布局")
            self.refresh()
        else:
            QMessageBox.warning(self, "切换失败", f"切换布局失败: {err}")

    def _on_delete_layout(self):
        row = self._layouts_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请先选择一个布局")
            return
        item = self._layouts_table.item(row, 0)
        if not item:
            return
        layout_id = item.text()
        reply = QMessageBox.question(self, "确认删除", f"确定删除布局 '{layout_id}'?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self._btn_del_layout.setEnabled(False)
            w = AdminWorker(self._state.api.admin_neural_delete_layout, layout_id)
            w.finished.connect(self._on_delete_done)
            w.start()

    def _on_delete_done(self, result: tuple):
        self._btn_del_layout.setEnabled(True)
        ok, data, err = result
        if ok:
            self._refresh_layouts()
        else:
            QMessageBox.warning(self, "删除失败", f"删除布局失败: {err}")


# ═══════════════════════════════════════════════════════════
# 告警面板：AlertPanel
# ═══════════════════════════════════════════════════════════

class AlertPanel(CachedPanelMixin, QWidget):
    """告警管理面板 — 查看告警历史、统计数据、清除告警、测试触发"""

    LEVEL_COLORS = {
        "INFO": ("#00d4aa", "ℹ️"),
        "WARNING": ("#f39c12", "⚠️"),
        "CRITICAL": ("#e74c3c", "🚨"),
    }

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # 标题
        layout.addWidget(_panel_header("告警管理中心"))

        # 统计行
        stats_row = QHBoxLayout()
        self._stat_total = _cache_stats_bar("总量", "—")
        self._stat_warning = _cache_stats_bar("警告", "—")
        self._stat_critical = _cache_stats_bar("严重", "—")
        self._stat_last = _cache_stats_bar("最近", "—")
        for w in (self._stat_total, self._stat_warning, self._stat_critical, self._stat_last):
            stats_row.addWidget(w)
        stats_row.addStretch()
        layout.addLayout(stats_row)

        # 工具栏
        toolbar = QHBoxLayout()
        self._btn_refresh = _action_button("🔄 刷新", callback=self.refresh)
        self._btn_clear_all = _action_button("🗑️ 清除全部", callback=self._on_clear_all)
        self._btn_clear_warning = _action_button("清除警告", callback=self._on_clear_warning)
        self._btn_clear_critical = _action_button("清除严重", callback=self._on_clear_critical)
        self._btn_test = _action_button("🔔 测试触发", callback=self._on_test_trigger)

        toolbar.addWidget(self._btn_refresh)
        toolbar.addWidget(self._btn_clear_all)
        toolbar.addWidget(self._btn_clear_warning)
        toolbar.addWidget(self._btn_clear_critical)
        toolbar.addWidget(self._btn_test)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # 级别过滤
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("级别过滤:"))
        self._filter_combo = QComboBox()
        self._filter_combo.addItems(["全部", "INFO", "WARNING", "CRITICAL"])
        self._filter_combo.currentTextChanged.connect(self._on_filter_changed)
        filter_row.addWidget(self._filter_combo)

        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard'])
        layout.addWidget(_related)


        # 阶段三：相关面板跳转
        _related = _related_panels_group(self._state, ['dashboard'])
        layout.addWidget(_related)

        filter_row.addStretch()
        layout.addLayout(filter_row)

        # 告警表格
        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["时间", "级别", "来源", "消息", "详情"])
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        _apply_table_style(self._table)
        hdr = self._table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._table)

    def refresh(self):
        """刷新告警数据和统计"""
        self._btn_refresh.setEnabled(False)
        self._btn_refresh.setText("刷新中...")
        # 并发获取历史和统计
        for worker, handler in [
            (AdminWorker(self._state.api.admin_alerts_history, 200), self._on_history),
            (AdminWorker(self._state.api.admin_alerts_stats), self._on_stats),
        ]:
            worker.finished.connect(handler)
            worker.start()

    def _on_history(self, result: tuple):
        self._btn_refresh.setEnabled(True)
        self._btn_refresh.setText("🔄 刷新")
        ok, data, err = result
        if not ok:
            logger.warning(f"获取告警历史失败: {err}")
            return
        alerts = (data or {}).get("alerts", [])
        self._populate_table(alerts)

    def _on_stats(self, result: tuple):
        ok, data, err = result
        if not ok:
            logger.warning(f"获取告警统计失败: {err}")
            return
        total = (data or {}).get("total_alerts", 0)
        by_level = (data or {}).get("by_level", {})
        last_alert = (data or {}).get("last_alert")
        self._stat_total.findChild(QLabel, "value").setText(str(total))
        self._stat_warning.findChild(QLabel, "value").setText(str(by_level.get("WARNING", 0)))
        self._stat_critical.findChild(QLabel, "value").setText(str(by_level.get("CRITICAL", 0)))
        if last_alert:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(last_alert.replace("Z", "+00:00"))
                self._stat_last.findChild(QLabel, "value").setText(dt.strftime("%H:%M:%S"))
            except Exception:
                self._stat_last.findChild(QLabel, "value").setText(str(last_alert)[:12])
        else:
            self._stat_last.findChild(QLabel, "value").setText("无")

    def _populate_table(self, alerts: list):
        filter_text = self._filter_combo.currentText()
        if filter_text != "全部":
            alerts = [a for a in alerts if a.get("level", "") == filter_text]

        self._table.setRowCount(len(alerts))
        for i, a in enumerate(alerts):
            level = a.get("level", "INFO")
            color, icon = self.LEVEL_COLORS.get(level, ("#95a5a6", "❔"))
            ts = a.get("timestamp", "")[:19]
            source = a.get("source", "")
            message = a.get("message", "")
            details = str(a.get("details", ""))[:100]

            ts_item = QTableWidgetItem(ts)
            level_item = QTableWidgetItem(f"{icon} {level}")
            source_item = QTableWidgetItem(source)
            msg_item = QTableWidgetItem(message)
            details_item = QTableWidgetItem(details)

            for item in (ts_item, level_item, source_item, msg_item, details_item):
                item.setForeground(QColor(color))

            self._table.setItem(i, 0, ts_item)
            self._table.setItem(i, 1, level_item)
            self._table.setItem(i, 2, source_item)
            self._table.setItem(i, 3, msg_item)
            self._table.setItem(i, 4, details_item)

    def _on_filter_changed(self, text: str):
        self.refresh()

    def _on_clear_all(self):
        reply = QMessageBox.question(
            self, "确认清除", "确定清除所有告警历史?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        w = AdminWorker(self._state.api.admin_alerts_clear)
        w.finished.connect(self._on_clear_done)
        w.start()

    def _on_clear_warning(self):
        w = AdminWorker(lambda: self._state.api.admin_alerts_clear("WARNING"))
        w.finished.connect(self._on_clear_done)
        w.start()

    def _on_clear_critical(self):
        w = AdminWorker(lambda: self._state.api.admin_alerts_clear("CRITICAL"))
        w.finished.connect(self._on_clear_done)
        w.start()

    def _on_clear_done(self, result: tuple):
        ok, data, err = result
        if ok:
            cleared = (data or {}).get("cleared", 0)
            QMessageBox.information(self, "清除完成", f"已清除 {cleared} 条告警")
            self.refresh()
        else:
            QMessageBox.warning(self, "清除失败", f"清除失败: {err}")

    def _on_test_trigger(self):
        """弹出对话框，手动触发一条测试告警"""
        from PyQt6.QtWidgets import QInputDialog
        msg, ok = QInputDialog.getText(self, "测试触发告警", "告警消息:")
        if not ok or not msg.strip():
            return
        level_combo = QComboBox()
        level_combo.addItems(["INFO", "WARNING", "CRITICAL"])
        dlg = QDialog(self)
        dlg.setWindowTitle("选择级别")
        dlg.setLayout(QVBoxLayout())
        dlg.layout().addWidget(QLabel("选择告警级别:"))
        dlg.layout().addWidget(level_combo)
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        dlg.layout().addWidget(btn_box)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        level = level_combo.currentText()
        w = AdminWorker(
            self._state.api.admin_alerts_trigger,
            level=level, source="gui_test", message=msg.strip(),
        )
        w.finished.connect(self._on_test_done)
        w.start()

    def _on_test_done(self, result: tuple):
        ok, data, err = result
        if ok:
            QMessageBox.information(self, "触发成功", "测试告警已触发")
            self.refresh()
        else:
            QMessageBox.warning(self, "触发失败", f"触发失败: {err}")


# ═══════════════════════════════════════════════════════════
# 主面板：AdminPanel
# ═══════════════════════════════════════════════════════════

class AdminPanel(QWidget):
    """系统管理主面板 — 串联所有管理功能

    v1.0.0: 懒加载优化 — 子面板首次切换时才创建，减少启动耗时。
    """

    # 子面板切换信号
    panel_changed = pyqtSignal(str)  # panel_name

    # 面板类映射（key -> 面板类）— 懒加载用
    PANELS_DICT: dict = {
        "dashboard": DashboardOverview,
        "startup": StartupPanel,
        "config": ConfigPanel,
        "load": LoadManagerPanel,
        "llm": LLMManagerPanel,
        "chain": ChainMonitorPanel,
        "evolution": EvolutionPanel,
        "memory": MemoryLifecyclePanel,
        "claw": ClawSchedulerPanel,
        "knowledge": KnowledgeCellsPanel,
        "system": SystemComponentsPanel,
        "neural": NeuralLayoutPanel,
        "system_resource": SystemResourcePanel,
        "alerts": AlertPanel,
    }

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self._state = app_state
        self._panels: Dict[str, QWidget] = {}
        self._panel_keys: List[str] = []
        self._nav_buttons: Dict[str, QPushButton] = {}
        # 连接跨面板导航信号（阶段三：面板打通）
        self._state.admin_panel_navigate.connect(self._switch_panel)
        self._state.admin_panel_history_navigate.connect(self._on_history_navigate)
        self._init_ui()

    def _init_ui(self):
        """初始化 UI — 阶段一重构：分组导航 + 面包屑"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── 左侧分组导航栏 ──
        nav, nav_layout, btn_group, self._nav_buttons, _group_labels = _nav_bar(180, "Somn 管理")
        self._nav_frame = nav  # v1.0.0: 保存导航栏引用，用于响应式布局

        # 连接导航按钮信号
        for key, btn in self._nav_buttons.items():
            btn.clicked.connect(lambda checked, k=key: self._switch_panel(k))

        layout.addWidget(nav)

        # ── 右侧主内容区 ──
        right_area = QFrame()
        right_area.setStyleSheet("background: #f1f5f9;")
        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 面包屑栏
        self._breadcrumb_bar, self._breadcrumb_layout = _breadcrumb_bar(self)
        right_layout.addWidget(self._breadcrumb_bar)

        # v1.0.0: 主题切换按钮
        self._theme_btn = _theme_toggle_button()
        self._theme_btn.clicked.connect(self._toggle_theme)
        right_layout.addWidget(self._theme_btn, 0, Qt.AlignmentFlag.AlignRight)
        
        # 初始化主题（从 QSettings 读取）
        self._is_dark_mode = False
        self._current_theme = THEME_LIGHT
        
        # v1.0.0: 全局搜索框
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(12, 8, 12, 8)
        self._search_edit = _search_box("搜索面板... (Ctrl+K)")
        self._search_results = _search_results_dropdown(self)
        search_layout.addWidget(self._search_edit)
        right_layout.addLayout(search_layout)
        
        # 搜索框事件
        self._search_edit.textChanged.connect(self._on_search_text_changed)
        self._search_edit.returnPressed.connect(self._on_search_activate)
        self._search_results.itemClicked.connect(self._on_search_result_clicked)
        
        # 快捷键：Ctrl+K 聚焦搜索
        shortcut_search = QShortcut(QKeySequence("Ctrl+K"), self)
        shortcut_search.activated.connect(self._focus_search)
        
        # 快捷键：Ctrl+1~4 切换分组
        for i, (group_name, _color, keys) in enumerate(NAV_GROUPS[:4], 1):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i}"), self)
            shortcut.activated.connect(lambda idx=i-1: self._switch_to_group(idx))
        
        # 快捷键：Esc 关闭搜索结果
        shortcut_esc = QShortcut(QKeySequence("Esc"), self)
        shortcut_esc.activated.connect(self._close_search_results)
        

        # 面板堆叠区
        self._stack = QStackedWidget()
        self._stack.setStyleSheet("background: #f1f5f9;")

        # 为 NAV_GROUPS 中每个 key 创建占位 QWidget（懒加载）
        self._panel_keys = []
        for _group_name, _group_color, keys in NAV_GROUPS:
            for key in keys:
                self._panel_keys.append(key)
                self._stack.addWidget(QWidget())  # 占位

        # 默认立即创建 dashboard
        self._ensure_panel("dashboard")
        right_layout.addWidget(self._stack, 1)
        layout.addWidget(right_area, 1)

        # 初始化面包屑
        self._update_breadcrumb("dashboard")

    def _ensure_panel(self, key: str) -> QWidget:
        """懒加载：确保指定面板已创建，未创建则实例化"""
        if key in self._panels:
            return self._panels[key]

        panel_cls = self.PANELS_DICT.get(key)
        if panel_cls is None:
            return None

        # 创建面板实例
        panel = panel_cls(self._state)
        self._panels[key] = panel

        # 找到对应的占位 widget 索引并替换
        for i, k in enumerate(self._panel_keys):
            if k == key:
                old_widget = self._stack.widget(i)
                self._stack.removeWidget(old_widget)
                old_widget.deleteLater()
                self._stack.insertWidget(i, panel)
                break

        return panel

    def _switch_panel(self, key: str):
        """切换到指定面板（懒加载 + 淡入动画）"""
        if key not in self._panel_keys:
            return
        i = self._panel_keys.index(key)
        self._ensure_panel(key)
        panel = self._panels.get(key)

        # v1.0.0: 淡入动画（200ms）
        if panel:
            effect = QGraphicsDropShadowEffect(panel) if False else None
            from PyQt6.QtWidgets import QGraphicsOpacityEffect
            opacity_effect = QGraphicsOpacityEffect(panel)
            panel.setGraphicsEffect(opacity_effect)
            opacity_effect.setOpacity(0)
            anim = QPropertyAnimation(opacity_effect, b"opacity")
            anim.setDuration(200)
            anim.setStartValue(0)
            anim.setEndValue(1)
            # 动画结束后移除效果（恢复正常渲染）
            def _cleanup():
                panel.setGraphicsEffect(None)
            anim.finished.connect(_cleanup)
            anim.start()
            # 防止 GC
            if not hasattr(self, '_anim_refs'):
                self._anim_refs = []
            self._anim_refs.append(anim)

        self._stack.setCurrentIndex(i)
        self.panel_changed.emit(key)
        self._state.push_panel_history(key)
        self._update_breadcrumb(key)
        if panel and hasattr(panel, 'refresh'):
            panel.refresh()


    def _update_breadcrumb(self, current_key: str):
        """v1.0.0: 更新面包屑（可点击历史路径）"""
        # 清空旧内容
        while self._breadcrumb_layout.count() > 0:
            item = self._breadcrumb_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 从 AppState 获取历史路径
        history = self._state.panel_history  # list of keys
        full_path = history + [self._state.current_panel_key]

        for idx, key in enumerate(full_path):
            label_text = PANEL_LABELS.get(key, key)
            is_last = (idx == len(full_path) - 1)

            if not is_last:
                link = _breadcrumb_link(label_text, key, self._state)
                self._breadcrumb_layout.addWidget(link)
                sep = QLabel("›")
                sep.setStyleSheet("color: #94a3b8; font-size: 12px; margin: 0px 4px;")
                self._breadcrumb_layout.addWidget(sep)
            else:
                current = QLabel(label_text)
                current.setStyleSheet("color: #1e293b; font-weight: 700; font-size: 13px;")
                self._breadcrumb_layout.addWidget(current)

        self._breadcrumb_layout.addStretch()

    # ── v1.0.0 响应式布局 ─────────────────────────

    def resizeEvent(self, event):
        """窗口大小变化时：导航栏折叠/展开"""
        super().resizeEvent(event)
        if hasattr(self, '_nav_frame') and self.width() < 1000:
            self._collapse_nav()
        elif hasattr(self, '_nav_frame') and self.width() >= 1000:
            self._expand_nav()

    def _collapse_nav(self):
        """折叠导航栏（小窗口模式）"""
        if not hasattr(self, '_nav_collapsed'):
            self._nav_collapsed = False
        if self._nav_collapsed:
            return
        self._nav_collapsed = True
        if hasattr(self, '_nav_frame'):
            self._nav_frame.setFixedWidth(48)
        # 隐藏导航文字，只显示图标（如有）

    def _expand_nav(self):
        """展开导航栏"""
        if not hasattr(self, '_nav_collapsed'):
            self._nav_collapsed = False
        if not self._nav_collapsed:
            return
        self._nav_collapsed = False
        if hasattr(self, '_nav_frame'):
            self._nav_frame.setFixedWidth(180)

    # ── v1.0.0 深色/浅色模式 ─────────────────────

    def _toggle_theme(self):
        """切换深色/浅色模式"""
        if not hasattr(self, '_is_dark_mode'):
            self._is_dark_mode = False
        self._is_dark_mode = not self._is_dark_mode
        theme = THEME_DARK if self._is_dark_mode else THEME_LIGHT
        self._current_theme = theme
        if hasattr(self, '_theme_btn'):
            self._theme_btn.setText('☀️' if self._is_dark_mode else '🌙')
        self._apply_theme(theme)
        print(f"✅ 已切换到{theme['name']}")

    def _apply_theme(self, theme: dict):
        """应用主题到所有组件"""
        if hasattr(self, '_right_area'):
            self._right_area.setStyleSheet(f"background: {theme['bg_primary']};")
        if hasattr(self, '_stack'):
            self._stack.setStyleSheet(f"background: {theme['bg_primary']};")
        if hasattr(self, '_search_edit'):
            self._search_edit.setStyleSheet(f"""
                QLineEdit {{
                    background: {theme['bg_secondary']};
                    border: 1px solid {theme['border']};
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 13px;
                    color: {theme['text_primary']};
                }}
                QLineEdit:focus {{
                    border: 1px solid {theme['accent']};
                }}
            """)
        print(f"✅ 主题已应用: {theme['name']}")

    # ── v1.0.0 面板收藏夹 ─────────────────────────

    def _toggle_favorite(self, key: str):
        """切换面板收藏状态"""
        if not hasattr(self, '_favorites'):
            self._favorites = set()
        if key in self._favorites:
            self._favorites.remove(key)
            print(f"⭐ 取消收藏: {key}")
        else:
            self._favorites.add(key)
            print(f"⭐ 已收藏: {key}")
        # 更新收藏夹显示
        if hasattr(self, '_favorites_bar'):
            self._show_favorites()

    def _show_favorites(self):
        """在导航栏顶部显示收藏夹"""
        if not hasattr(self, '_favorites_bar') or not hasattr(self, '_favorites'):
            return
        # 清空旧收藏夹按钮
        while self._favorites_layout.count() > 0:
            item = self._favorites_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        # 添加收藏的面板
        for key in self._favorites:
            label = PANEL_LABELS.get(key, key)
            btn = _nav_button(label, key, "#f59e0b")
            btn.clicked.connect(lambda checked, k=key: self._switch_panel(k))
            self._favorites_layout.addWidget(btn)

    def show_dashboard(self):
        """直接显示概览面板"""
        self._switch_panel("dashboard")
