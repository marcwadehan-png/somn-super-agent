# -*- coding: utf-8 -*-
"""Somn GUI - 系统托盘图标管理

提供系统托盘支持、后台运行、通知气泡等功能。
TrayAwareMainWindow 可作为 Mixin 与任何 QMainWindow 子类组合。
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QAction, QColor, QFont, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMenu,
    QMessageBox,
    QSystemTrayIcon,
    QWidget,
)

from loguru import logger

# 全局 LOGO 路径常量
_GUI_ROOT = Path(__file__).parent.parent.parent.resolve()
DEFAULT_ICON_PATH = _GUI_ROOT / "LOGO.jpg"


# ---------------------------------------------------------------------------
# TrayIconManager
# ---------------------------------------------------------------------------

class TrayIconManager(QObject):
    """系统托盘图标管理器

    功能:
    - 显示系统托盘图标
    - 提供快捷菜单（显示窗口 / 快捷操作 / 设置 / 退出）
    - 支持最小化到托盘
    - 显示通知气泡
    """

    # 信号
    show_window_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    quick_action_triggered = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None, app_name: str = "Somn"):
        super().__init__(parent)
        self.app_name = app_name
        self.parent_window = parent
        self.tray_icon: QSystemTrayIcon | None = None
        self.tray_menu: QMenu | None = None

        self._setup_tray_icon()

    # ---- 初始化 ----------------------------------------------------------

    def _setup_tray_icon(self) -> None:
        """设置系统托盘图标"""
        icon = self._create_default_icon()
        self.tray_icon = QSystemTrayIcon(icon, self.parent_window)
        self.tray_icon.setToolTip(f"{self.app_name}\n点击显示主窗口")
        self._create_menu()
        self.tray_icon.activated.connect(self._on_tray_activated)
        logger.info("系统托盘图标已初始化")

    def _create_default_icon(self) -> QIcon:
        """创建默认图标，优先使用 LOGO.jpg"""
        # 优先加载 LOGO 图片
        if DEFAULT_ICON_PATH.exists():
            pixmap = QPixmap(str(DEFAULT_ICON_PATH))
            if not pixmap.isNull():
                # 缩放到合适的托盘图标尺寸
                pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logger.info(f"已加载 LOGO 图标: {DEFAULT_ICON_PATH}")
                return QIcon(pixmap)
        
        # 回退：创建默认图标（蓝色背景 + 白色字母 S）
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor("#007bff"))
        painter = QPainter(pixmap)
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Microsoft YaHei", 24, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), 0x84, "S")
        painter.end()
        return QIcon(pixmap)

    def _create_menu(self) -> None:
        """创建托盘右键菜单"""
        self.tray_menu = QMenu()

        # 显示主窗口
        show_action = QAction("显示主窗口", self)
        show_action.triggered.connect(self._on_show_window)
        self.tray_menu.addAction(show_action)
        self.tray_menu.addSeparator()

        # 快捷操作
        quick_actions = [
            ("📝 新建文档", "new_doc"),
            ("🔍 搜索知识", "search_kb"),
            ("📊 生成报告", "gen_report"),
            ("🧹 清理文件", "clean_files"),
        ]
        for text, action_id in quick_actions:
            action = QAction(text, self)
            action.triggered.connect(lambda checked, aid=action_id: self._on_quick_action(aid))
            self.tray_menu.addAction(action)

        self.tray_menu.addSeparator()

        # 设置
        settings_action = QAction("⚙️ 设置", self)
        settings_action.triggered.connect(lambda: self._on_quick_action("settings"))
        self.tray_menu.addAction(settings_action)

        self.tray_menu.addSeparator()

        # 退出
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self._on_quit)
        self.tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)

    # ---- 事件处理 --------------------------------------------------------

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """托盘图标被激活"""
        if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.Trigger):
            self._on_show_window()

    def _on_show_window(self) -> None:
        """显示主窗口"""
        self.show_window_requested.emit()
        if self.parent_window:
            self.parent_window.show()
            self.parent_window.raise_()
            self.parent_window.activateWindow()

    def _on_quick_action(self, action_id: str) -> None:
        """快捷操作触发"""
        self.quick_action_triggered.emit(action_id)
        self._on_show_window()
        logger.debug(f"托盘快捷操作: {action_id}")

    def _on_quit(self) -> None:
        """退出应用"""
        self.quit_requested.emit()

    # ---- 公共接口 --------------------------------------------------------

    def show(self) -> None:
        """显示托盘图标"""
        if self.tray_icon:
            self.tray_icon.show()
            logger.info("系统托盘图标已显示")

    def hide(self) -> None:
        """隐藏托盘图标"""
        if self.tray_icon:
            self.tray_icon.hide()

    def show_message(
        self,
        title: str,
        message: str,
        icon: QSystemTrayIcon.MessageIcon = QSystemTrayIcon.MessageIcon.Information,
        duration: int = 3000,
    ) -> None:
        """显示托盘通知"""
        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon, duration)
            logger.debug(f"托盘通知: {title} - {message}")

    def show_notification(self, title: str, message: str) -> None:
        self.show_message(title, message, QSystemTrayIcon.Information)

    def show_warning(self, title: str, message: str) -> None:
        self.show_message(title, message, QSystemTrayIcon.Warning)

    def show_error(self, title: str, message: str) -> None:
        self.show_message(title, message, QSystemTrayIcon.Critical)

    def set_tooltip(self, tooltip: str) -> None:
        if self.tray_icon:
            self.tray_icon.setToolTip(tooltip)


# ---------------------------------------------------------------------------
# TrayAwareMainWindow — 混入类
# ---------------------------------------------------------------------------

class TrayAwareMainWindow:
    """支持系统托盘的主窗口混入类

    使用示例::

        class MainWindow(QMainWindow, TrayAwareMainWindow):
            def __init__(self):
                super().__init__()
                self.setup_tray_icon()
    """

    def setup_tray_icon(self, app_name: str = "Somn") -> None:
        """设置系统托盘支持"""
        self.tray_manager = TrayIconManager(self, app_name)

        # 连接信号
        self.tray_manager.show_window_requested.connect(self.show)
        self.tray_manager.quit_requested.connect(self._on_tray_quit)
        self.tray_manager.quick_action_triggered.connect(self._on_tray_quick_action)

        # 显示托盘图标
        self.tray_manager.show()

        # 保存原始关闭事件，替换为托盘关闭行为
        self._original_close_event = self.closeEvent
        self.closeEvent = self._tray_close_event  # type: ignore[assignment]

    def _tray_close_event(self, event) -> None:
        """处理关闭事件 — 最小化到托盘"""
        minimize_to_tray = getattr(self, '_config', None)
        if minimize_to_tray is None:
            # 尝试从 GUIConfig 获取
            cfg = getattr(self, 'config', None)
            if cfg is not None and hasattr(cfg, 'get'):
                minimize_to_tray = cfg.get('ui.minimize_to_tray', True)
            else:
                minimize_to_tray = True
        elif isinstance(minimize_to_tray, dict):
            minimize_to_tray = minimize_to_tray.get('ui', {}).get('minimize_to_tray', True)

        if minimize_to_tray and self.tray_manager.tray_icon.isVisible():
            self.hide()
            self.tray_manager.show_notification("Somn", "应用已最小化到系统托盘，点击图标可恢复")
            event.ignore()
        else:
            self._original_close_event(event)

    def _on_tray_quit(self) -> None:
        """从托盘退出"""
        QApplication.quit()

    def _on_tray_quick_action(self, action_id: str) -> None:
        """处理托盘快捷操作（子类可覆写）"""
        if action_id == "new_doc":
            handler = getattr(self, '_on_new_document', None)
            if handler:
                handler()
        elif action_id == "search_kb":
            tab = getattr(self, 'tab_widget', None)
            if tab:
                tab.setCurrentIndex(2)
        elif action_id == "gen_report":
            handler = getattr(self, '_on_generate_report', None)
            if handler:
                handler()
        elif action_id == "clean_files":
            handler = getattr(self, '_on_clean_files', None)
            if handler:
                handler()
        elif action_id == "settings":
            self._show_settings_dialog()

    def _show_settings_dialog(self) -> None:
        """显示设置对话框"""
        QMessageBox.information(self, "设置", "设置功能开发中...\n\n请在 config.yaml 中手动配置。")

    def show_tray_notification(self, title: str, message: str) -> None:
        """显示托盘通知（供外部调用）"""
        if hasattr(self, 'tray_manager'):
            self.tray_manager.show_notification(title, message)


# ---------------------------------------------------------------------------
# 兼容性工厂函数
# ---------------------------------------------------------------------------

def create_tray_icon(
    parent: QWidget | None = None,
    app_name: str = "Somn",
) -> TrayIconManager:
    """创建 TrayIconManager 实例（向后兼容）"""
    return TrayIconManager(parent, app_name)
