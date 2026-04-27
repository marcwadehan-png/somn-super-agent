"""
__all__ = [
    'create_tray_icon',
    'hide',
    'set_tooltip',
    'setup_tray_icon',
    'show',
    'show_error',
    'show_message',
    'show_notification',
    'show_tray_notification',
    'show_warning',
]

系统托盘图标 - System Tray Icon
提供系统托盘支持和后台运行功能
"""

from PySide6.QtWidgets import (
    QSystemTrayIcon, QMenu, QAction, QApplication,
    QMessageBox, QWidget
)
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from loguru import logger
from pathlib import Path

# 全局 LOGO 路径常量 - 指向 Somn-GUI 的 LOGO
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SOMN_GUI_ROOT = _PROJECT_ROOT.parent / "Somn-GUI"
DEFAULT_ICON_PATH = _SOMN_GUI_ROOT / "LOGO.jpg"

class TrayIconManager(QObject):
    """
    系统托盘图标管理器
    
    功能:
    - 显示系统托盘图标
    - 提供快捷菜单
    - 支持最小化到托盘
    - 显示通知气泡
    """
    
    # 信号
    show_window_requested = Signal()
    quit_requested = Signal()
    quick_action_triggered = Signal(str)
    
    def __init__(self, parent: QWidget = None, app_name: str = "SmartOffice AI"):
        super().__init__(parent)
        self.app_name = app_name
        self.parent_window = parent
        self.tray_icon = None
        self.tray_menu = None
        
        self._setup_tray_icon()
        
    def _setup_tray_icon(self):
        """设置系统托盘图标"""
        # 创建图标
        icon = self._create_default_icon()
        
        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(icon, self.parent_window)
        self.tray_icon.setToolTip(f"{self.app_name}\n点击显示主窗口")
        
        # 创建菜单
        self._create_menu()
        
        # 连接信号
        self.tray_icon.activated.connect(self._on_tray_activated)
        
        logger.info("系统托盘图标已init")
    
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
        painter.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        painter.drawText(pixmap.rect(), 0x84, "S")  # 居中对齐
        painter.end()
        
        return QIcon(pixmap)
    
    def _create_menu(self):
        """创建托盘菜单"""
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
            ("📊 generate报告", "gen_report"),
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
        
        # 设置菜单
        self.tray_icon.setContextMenu(self.tray_menu)
    
    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason):
        """托盘图标被激活"""
        if reason == QSystemTrayIcon.DoubleClick:
            self._on_show_window()
        elif reason == QSystemTrayIcon.Trigger:
            # 单击也显示窗口
            self._on_show_window()
    
    def _on_show_window(self):
        """显示主窗口"""
        self.show_window_requested.emit()
        if self.parent_window:
            self.parent_window.show()
            self.parent_window.raise_()
            self.parent_window.activateWindow()
    
    def _on_quick_action(self, action_id: str):
        """快捷操作"""
        self.quick_action_triggered.emit(action_id)
        
        # 同时显示窗口
        self._on_show_window()
        
        logger.debug(f"托盘快捷操作: {action_id}")
    
    def _on_quit(self):
        """退出应用"""
        self.quit_requested.emit()
    
    def show(self):
        """显示托盘图标"""
        if self.tray_icon:
            self.tray_icon.show()
            logger.info("系统托盘图标已显示")
    
    def hide(self):
        """隐藏托盘图标"""
        if self.tray_icon:
            self.tray_icon.hide()
    
    def show_message(
        self,
        title: str,
        message: str,
        icon: QSystemTrayIcon.MessageIcon = QSystemTrayIcon.Information,
        duration: int = 3000
    ):
        """
        显示托盘通知
        
        Args:
            title: 通知标题
            message: 通知内容
            icon: 图标类型
            duration: 显示时长(毫秒)
        """
        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon, duration)
            logger.debug(f"托盘通知: {title} - {message}")
    
    def show_notification(self, title: str, message: str):
        """显示信息通知"""
        self.show_message(title, message, QSystemTrayIcon.Information)
    
    def show_warning(self, title: str, message: str):
        """显示警告通知"""
        self.show_message(title, message, QSystemTrayIcon.Warning)
    
    def show_error(self, title: str, message: str):
        """显示错误通知"""
        self.show_message(title, message, QSystemTrayIcon.Critical)
    
    def set_tooltip(self, tooltip: str):
        """设置托盘提示文本"""
        if self.tray_icon:
            self.tray_icon.setToolTip(tooltip)

class TrayAwareMainWindow:
    """
    支持系统托盘的主窗口混入类
    
    使用示例:
        class MainWindow(QMainWindow, TrayAwareMainWindow):
            def __init__(self):
                super().__init__()
                self.setup_tray_icon()
    """
    
    def setup_tray_icon(self, app_name: str = "SmartOffice AI"):
        """设置系统托盘支持"""
        self.tray_manager = TrayIconManager(self, app_name)
        
        # 连接信号
        self.tray_manager.show_window_requested.connect(self.show)
        self.tray_manager.quit_requested.connect(self._on_tray_quit)
        self.tray_manager.quick_action_triggered.connect(self._on_tray_quick_action)
        
        # 显示托盘图标
        self.tray_manager.show()
        
        # 保存原始关闭事件
        self._original_close_event = self.closeEvent
        self.closeEvent = self._tray_close_event
    
    def _tray_close_event(self, event):
        """处理关闭事件 - 最小化到托盘"""
        # 检查配置是否启用最小化到托盘
        minimize_to_tray = getattr(self, 'config', {}).get('ui', {}).get('minimize_to_tray', True)
        
        if minimize_to_tray and self.tray_manager.tray_icon.isVisible():
            # 隐藏窗口而不是关闭
            self.hide()
            self.tray_manager.show_notification(
                "SmartOffice AI",
                "应用已最小化到系统托盘,点击图标可恢复"
            )
            event.ignore()
        else:
            # 真正退出
            self._original_close_event(event)
    
    def _on_tray_quit(self):
        """从托盘退出"""
        # 保存配置
        if hasattr(self, 'memory_system'):
            self.memory_system.consolidate_memories()
        
        # 退出应用
        QApplication.quit()
    
    def _on_tray_quick_action(self, action_id: str):
        """处理托盘快捷操作"""
        if action_id == "new_doc":
            if hasattr(self, '_on_new_document'):
                self._on_new_document()
        elif action_id == "search_kb":
            if hasattr(self, 'tab_widget'):
                self.tab_widget.setCurrentIndex(2)  # 切换到知识库标签
        elif action_id == "gen_report":
            if hasattr(self, '_on_generate_report'):
                self._on_generate_report()
        elif action_id == "clean_files":
            if hasattr(self, '_on_clean_files'):
                self._on_clean_files()
        elif action_id == "settings":
            # 显示设置对话框
            self._show_settings_dialog()
    
    def _show_settings_dialog(self):
        """显示设置对话框"""
        QMessageBox.information(
            self,
            "设置",
            "设置功能开发中...\n\n请在 config.yaml 中手动配置."
        )
    
    def show_tray_notification(self, title: str, message: str):
        """显示托盘通知"""
        if hasattr(self, 'tray_manager'):
            self.tray_manager.show_notification(title, message)

# 兼容性函数
def create_tray_icon(parent: QWidget = None, app_name: str = "SmartOffice AI") -> TrayIconManager:
    """
    创建系统托盘图标
    
    Args:
        parent: 父窗口
        app_name: 应用名称
    
    Returns:
        TrayIconManager 实例
    """
    return TrayIconManager(parent, app_name)
