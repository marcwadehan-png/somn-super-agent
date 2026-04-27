# -*- coding: utf-8 -*-
"""Somn GUI - 主窗口

前后端分离架构：不直接导入 Somn 核心模块，
通过 AppState + SomnAPIClient 与后端 REST API 通信。
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QStatusBar,
    QStyle,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from loguru import logger

from somngui.core.config import GUIConfig
from somngui.core.state import AppState, ConnectionStatus
from somngui.core.plugin_manager import PluginManager
from somngui.gui import (
    WELCOME_MESSAGE,
    TrayAwareMainWindow,
    format_agent_message,
    format_system_message,
    format_user_message,
    is_text_file,
)
from somngui.gui._ui_templates import (
    STATUS_ERROR_STYLE,
    STATUS_READY_STYLE,
    STATUS_THINKING_STYLE,
)


# ---------------------------------------------------------------------------
# 后端连接工作线程
# ---------------------------------------------------------------------------

class ConnectionWorker(QThread):
    """后台连接后端服务"""

    connected = pyqtSignal(bool, str)   # success, url_or_error
    disconnected = pyqtSignal()

    def __init__(self, state: AppState):
        super().__init__()
        self._state = state

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(self._state.connect_backend())
            loop.close()
            url = self._state.backend_url if success else "连接失败"
            self.connected.emit(success, url)
        except Exception as e:
            self.connected.emit(False, str(e))


# ---------------------------------------------------------------------------
# API 请求工作线程
# ---------------------------------------------------------------------------

class ApiWorker(QThread):
    """通用 API 请求工作线程"""

    result_ready = pyqtSignal(object)   # dict
    error_occurred = pyqtSignal(str)

    def __init__(self, coro_func, *args, **kwargs):
        super().__init__()
        self._coro_func = coro_func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self._coro_func(*self._args, **self._kwargs)
            )
            loop.close()
            self.result_ready.emit(result)
        except Exception as e:
            logger.error(f"API 请求失败: {e}")
            self.error_occurred.emit(str(e))


# ---------------------------------------------------------------------------
# MainWindow
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    """Somn 主窗口"""

    def __init__(self, config: GUIConfig | None = None):
        super().__init__()

        self.setWindowTitle("Somn - 汇千古之智，向未知而生")
        self.setMinimumSize(1200, 800)

        # ── 全局状态 ──
        self._config = config or GUIConfig()
        self._state = AppState(self._config)
        self._workspace = Path(self._config.get("workspace", ".")).resolve()
        self._workspace.mkdir(parents=True, exist_ok=True)

        # ── 初始化 UI ──
        self._setup_menu()
        self._setup_ui()
        self._setup_status_bar()
        self._setup_shortcuts()
        # v1.0.0: 托盘延迟到事件循环启动后初始化，避免启动时加载 LOGO.jpg 阻塞
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self._setup_tray)

        # ── 插件系统（v1.0.0: 延迟到后端连接后加载，避免启动阻塞） ──
        plugins_dir = Path(__file__).parent.parent.parent / "plugins"
        self._plugin_manager = PluginManager(plugins_dir)
        # _load_plugins() 在 _on_backend_connected 中执行

        # ── 连接状态指示 ──
        self._state.connection_status_changed.connect(self._on_connection_status_changed)
        self._state.chat_message_received.connect(self._on_chat_message_from_state)
        self._state.error_occurred.connect(self._on_global_error)

        # ── 后台连接后端 ──
        self._connect_worker = ConnectionWorker(self._state)
        self._connect_worker.connected.connect(self._on_backend_connected)
        self._connect_worker.start()

        logger.info("主窗口初始化完成（后端连接中...）")

    # ==================================================================
    # UI 构建
    # ==================================================================

    def _setup_menu(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")

        new_doc_action = QAction("新建文档", self)
        new_doc_action.setShortcut(QKeySequence(QKeySequence.StandardKey.New))
        new_doc_action.triggered.connect(self._on_new_document)
        file_menu.addAction(new_doc_action)

        open_action = QAction("打开文件", self)
        open_action.setShortcut(QKeySequence(QKeySequence.StandardKey.Open))
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = QAction("保存文档", self)
        save_action.setShortcut(QKeySequence(QKeySequence.StandardKey.Save))
        save_action.triggered.connect(self._on_save_document)
        file_menu.addAction(save_action)

        export_action = QAction("导出文档(本地)", self)
        export_action.triggered.connect(self._on_export_document_local)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence(QKeySequence.StandardKey.Quit))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 工具菜单
        tools_menu = menubar.addMenu("工具(&T)")

        for label, slot in [
            ("🔍 扫描文件", self._on_scan_files),
            ("🧹 清理文件", self._on_clean_files),
            ("📁 索引文件", self._on_index_files),
            ("📚 知识库统计", self._on_kb_stats),
        ]:
            act = QAction(label, self)
            act.triggered.connect(slot)
            tools_menu.addAction(act)

        tools_menu.addSeparator()

        gen_report_action = QAction("📊 生成报告", self)
        gen_report_action.triggered.connect(self._on_generate_report)
        tools_menu.addAction(gen_report_action)

        gen_strategy_action = QAction("🎯 制定策略", self)
        gen_strategy_action.triggered.connect(self._on_create_strategy)
        tools_menu.addAction(gen_strategy_action)

        # 管理菜单
        admin_menu = menubar.addMenu("管理(&M)")

        open_admin_action = QAction("⚙️ 系统管理面板", self)
        open_admin_action.setShortcut("F8")
        open_admin_action.triggered.connect(self._open_admin_panel)
        admin_menu.addAction(open_admin_action)

        admin_menu.addSeparator()

        # 管理子菜单 — 快捷跳转到各子面板
        # 注意: 这里只定义 key，不导入 AdminPanel（延迟加载）
        for label, key in [
            ("📊 全局概览", "dashboard"),
            ("🚀 服务启停", "startup"),
            ("⚙️ 配置管理", "config"),
            ("🔧 引擎加载管理", "load"),
            ("🧠 LLM双脑管理", "llm"),
            ("🔗 主链路监控", "chain"),
            ("🧬 自主进化引擎", "evolution"),
            ("💾 记忆生命周期", "memory"),
            ("🦀 Claw调度管理", "claw"),
            ("🖥️ 系统组件健康", "system"),
            ("🧠 神经网络布局", "neural"),
        ]:
            act = QAction(label, self)
            act.triggered.connect(lambda checked, k=key: self._open_admin_panel(k))
            admin_menu.addAction(act)

    # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

        # 视图菜单
        view_menu = menubar.addMenu("视图(&V)")

        theme_menu = view_menu.addMenu("主题")
        self._theme_actions = {}

        # auto 选项
        auto_action = QAction("🔄 跟随系统", self)
        auto_action.setCheckable(True)
        auto_action.triggered.connect(lambda: self._switch_theme("auto"))
        theme_menu.addAction(auto_action)
        self._theme_actions["auto"] = auto_action

        theme_menu.addSeparator()

        # v1.0.0: 延迟加载主题列表 — 菜单首次显示时才扫描 .qss 文件
        self._theme_menu_populated = False
        theme_menu.aboutToShow.connect(self._populate_theme_menu)

        # 设置当前主题的勾选状态
        current_theme = self._config.get("ui.theme", "auto")
        self._theme_actions.get(current_theme, auto_action).setChecked(True)

        view_menu.addSeparator()

        refresh_action = QAction("刷新界面", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_all)
        view_menu.addAction(refresh_action)

    def _setup_ui(self):
        """创建主界面布局（三栏：左-文件树/操作 | 中-标签页 | 右-状态）"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        splitter.addWidget(self._create_left_panel())
        splitter.addWidget(self._create_center_panel())
        splitter.addWidget(self._create_right_panel())
        splitter.setSizes([250, 700, 250])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

    # ---- 左侧面板：文件树 + 快速操作 ----

    def _create_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setMaximumWidth(300)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)

        nav_label = QLabel("📁 工作空间")
        nav_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(nav_label)

        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setColumnCount(1)
        self.file_tree.itemClicked.connect(self._on_file_selected)
        layout.addWidget(self.file_tree)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        quick_label = QLabel("⚡ 快速操作")
        quick_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(quick_label)

        for text, slot in [
            ("📄 新建 Word", self._on_new_word),
            ("📊 新建 PPT", self._on_new_ppt),
            ("📑 新建 PDF", self._on_new_pdf),
            ("📈 新建 Excel", self._on_new_excel),
            ("🔍 扫描目录", self._on_scan_files),
            ("🧹 清理文件", self._on_clean_files),
            ("⚙️ 系统管理", self._open_admin_panel),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

        layout.addStretch()
        return panel

    # ---- 中央面板：标签页 ----

    def _create_center_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self._create_chat_tab(), "💬 智能对话")
        self.tab_widget.addTab(self._create_editor_tab(), "📝 文档编辑")
        self.tab_widget.addTab(self._create_kb_tab(), "📚 知识库")

        # 系统管理面板（隐藏式 — 通过菜单或快捷键打开全屏管理视图）
        # v1.0.0: 延迟创建 AdminPanel，首次打开时才实例化
        self._admin_panel = None

        layout.addWidget(self.tab_widget)
        return panel

    def _create_chat_tab(self) -> QWidget:
        """创建对话标签页（含历史面板）"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # ---- 左侧：历史对话面板 ----
        history_panel = QWidget()
        history_panel.setMaximumWidth(220)
        history_panel.setMinimumWidth(160)
        hist_layout = QVBoxLayout(history_panel)
        hist_layout.setContentsMargins(6, 6, 2, 6)

        hist_label = QLabel("📋 历史对话")
        hist_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        hist_layout.addWidget(hist_label)

        # 搜索历史
        hist_search_layout = QHBoxLayout()
        self.history_search_input = QLineEdit()
        self.history_search_input.setPlaceholderText("搜索...")
        self.history_search_input.textChanged.connect(self._on_history_search)
        hist_search_layout.addWidget(self.history_search_input)
        hist_layout.addLayout(hist_search_layout)

        # 历史列表
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self._on_history_item_clicked)
        self.history_list.itemDoubleClicked.connect(self._on_history_item_dblclicked)
        self.history_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self._on_history_context_menu)
        hist_layout.addWidget(self.history_list)

        # 历史操作按钮
        hist_btn_layout = QHBoxLayout()
        new_chat_btn = QPushButton("➕")
        new_chat_btn.setToolTip("新建对话")
        new_chat_btn.setFixedWidth(36)
        new_chat_btn.clicked.connect(self._on_new_chat)
        hist_btn_layout.addWidget(new_chat_btn)

        del_chat_btn = QPushButton("🗑️")
        del_chat_btn.setToolTip("删除当前对话")
        del_chat_btn.setFixedWidth(36)
        del_chat_btn.clicked.connect(self._on_delete_current_chat)
        hist_btn_layout.addWidget(del_chat_btn)
        hist_layout.addLayout(hist_btn_layout)

        # ---- 右侧：对话主区域 ----
        chat_area = QWidget()
        chat_layout = QVBoxLayout(chat_area)
        chat_layout.setSpacing(8)
        chat_layout.setContentsMargins(2, 6, 6, 6)

        # 消息显示
        self.chat_display = QTextBrowser()
        self.chat_display.setOpenExternalLinks(True)
        chat_layout.addWidget(self.chat_display)

        # 输入区
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("输入消息... (Enter 发送)")
        self.chat_input.returnPressed.connect(self._on_send_message)
        input_layout.addWidget(self.chat_input)

        send_btn = QPushButton("发送")
        send_btn.clicked.connect(self._on_send_message)
        input_layout.addWidget(send_btn)
        chat_layout.addLayout(input_layout)

        # 快速命令按钮
        from somngui.gui._types import QUICK_COMMANDS
        cmd_layout = QHBoxLayout()
        for cmd in QUICK_COMMANDS:
            btn = QPushButton(cmd)
            btn.clicked.connect(lambda checked, c=cmd: self._on_quick_command(c))
            cmd_layout.addWidget(btn)
        chat_layout.addLayout(cmd_layout)

        # 表情上传按钮
        sticker_btn = QPushButton("📷 上传表情包")
        sticker_btn.clicked.connect(self._on_upload_sticker)
        chat_layout.addWidget(sticker_btn)

        # 组装
        layout.addWidget(history_panel)
        layout.addWidget(chat_area, 1)

        return widget

    def _create_editor_tab(self) -> QWidget:
        """创建文档编辑标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 标题输入
        title_layout = QHBoxLayout()
        title_label = QLabel("文档标题:")
        self.doc_title_input = QLineEdit()
        self.doc_title_input.setPlaceholderText("输入文档标题...")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.doc_title_input)
        layout.addLayout(title_layout)

        # 编辑器
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("在此编辑文档内容...")
        layout.addWidget(self.editor)

        return widget

    def _create_kb_tab(self) -> QWidget:
        """创建知识库标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 搜索区
        search_layout = QHBoxLayout()
        self.kb_search_input = QLineEdit()
        self.kb_search_input.setPlaceholderText("搜索知识库...")
        self.kb_search_input.returnPressed.connect(self._on_search_kb)
        search_layout.addWidget(self.kb_search_input)

        search_btn = QPushButton("搜索")
        search_btn.clicked.connect(self._on_search_kb)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # 知识列表
        self.kb_list = QListWidget()
        self.kb_list.itemClicked.connect(self._on_kb_item_selected)
        layout.addWidget(self.kb_list)

        # 底部操作
        bottom_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self._refresh_kb_list)
        bottom_layout.addWidget(refresh_btn)

        stats_btn = QPushButton("📊 统计")
        stats_btn.clicked.connect(self._on_kb_stats)
        bottom_layout.addWidget(stats_btn)
        layout.addLayout(bottom_layout)

        return widget

    # ---- 右侧面板：状态 ----

    def _create_right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setMaximumWidth(300)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)

        # 连接状态
        conn_label = QLabel("🔗 连接状态")
        conn_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(conn_label)

        self.conn_status_label = QLabel("连接中...")
        self.conn_status_label.setStyleSheet(STATUS_THINKING_STYLE)
        layout.addWidget(self.conn_status_label)

        # 智能体状态
        agent_label = QLabel("🤖 智能体状态")
        agent_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(agent_label)

        self.agent_status = QLabel("就绪")
        self.agent_status.setStyleSheet(STATUS_READY_STYLE)
        layout.addWidget(self.agent_status)

        # 记忆统计（通过 API 获取）
        memory_label = QLabel("🧠 记忆统计")
        memory_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(memory_label)

        self.memory_stats = QLabel("短期记忆: -\n长期记忆: -")
        self.memory_stats.setStyleSheet("padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        layout.addWidget(self.memory_stats)

        # 最近记忆
        recent_label = QLabel("📋 最近记忆")
        recent_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(recent_label)

        self.recent_memories = QListWidget()
        layout.addWidget(self.recent_memories)

        # 知识库统计
        kb_label = QLabel("📚 知识库")
        kb_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(kb_label)

        self.kb_stats_label = QLabel("条目: -\n概念: -")
        self.kb_stats_label.setStyleSheet("padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        layout.addWidget(self.kb_stats_label)

        layout.addStretch()
        return panel

    def _setup_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("后端连接中...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _setup_shortcuts(self):
        """设置快捷键"""
        clear_action = QAction("清空对话", self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.triggered.connect(self._on_clear_chat)
        self.addAction(clear_action)

        admin_action = QAction("系统管理面板", self)
        admin_action.setShortcut("F8")
        admin_action.triggered.connect(lambda: self._open_admin_panel())
        self.addAction(admin_action)

    # ==================================================================
    # 系统管理面板
    # ==================================================================

    def _open_admin_panel(self, panel_key: str = None):
        """打开系统管理面板（全屏覆盖模式）
        
        v1.0.0: 延迟创建 AdminPanel，首次调用时才实例化。
        """
        # 延迟创建 AdminPanel
        if self._admin_panel is None:
            from somngui.gui.admin_panel import AdminPanel
            self._admin_panel = AdminPanel(self._state)
            self._admin_panel.panel_changed.connect(self._on_admin_panel_changed)

        # 保存当前中央部件
        self._saved_central = self.centralWidget()

        # 用管理面板替换中央部件
        if panel_key:
            self._admin_panel._switch_panel(panel_key)
        else:
            self._admin_panel.show_dashboard()
        self.setCentralWidget(self._admin_panel)

        # 更新窗口标题
        self.setWindowTitle("Somn - 系统管理")

    def _close_admin_panel(self):
        """关闭管理面板，恢复主界面"""
        if hasattr(self, '_saved_central') and self._saved_central:
            self.setCentralWidget(self._saved_central)
            self._saved_central = None
            self.setWindowTitle("Somn - 汇千古之智，向未知而生")

    def _on_admin_panel_changed(self, key: str):
        """管理面板切换回调"""
        if key == "__back__":
            self._close_admin_panel()

    # ==================================================================
    # 系统托盘（组合 TrayAwareMainWindow）
    # ==================================================================

    def _setup_tray(self):
        """设置系统托盘（组合 TrayAwareMainWindow）"""
        from somngui.gui.tray_icon import TrayAwareMainWindow
        # 将 Mixin 的方法绑定到 self
        for attr_name in (
            "setup_tray_icon", "_tray_close_event", "_on_tray_quit",
            "_on_tray_quick_action", "_show_settings_dialog",
            "show_tray_notification",
        ):
            if hasattr(TrayAwareMainWindow, attr_name):
                method = getattr(TrayAwareMainWindow, attr_name)
                if callable(method):
                    setattr(self, attr_name, method.__get__(self, type(self)))

        # 初始化托盘
        self.setup_tray_icon("Somn")

    # ==================================================================
    # 后端连接
    # ==================================================================

    def _on_backend_connected(self, success: bool, message: str):
        """后端连接完成回调"""
        if success:
            self.conn_status_label.setText(f"已连接\n{message}")
            self.conn_status_label.setStyleSheet(STATUS_READY_STYLE)
            self.status_bar.showMessage("后端已连接", 3000)
            # 加载初始数据
            self._load_initial_data()
            # 建立 WebSocket 连接
            self._connect_websocket()
            # v1.0.0: 延迟加载插件（启动时不阻塞）
            self._load_plugins()
        else:
            self.conn_status_label.setText(f"离线模式\n{message}")
            self.conn_status_label.setStyleSheet(STATUS_ERROR_STYLE)
            self._state.cache.set_offline(True)
            self.status_bar.showMessage("离线模式 - 使用缓存数据", 5000)
            # 从缓存加载已有数据
            self._load_cached_data()
            # 仍然显示欢迎消息
            self._show_welcome()

    def _on_connection_status_changed(self, status: ConnectionStatus):
        """连接状态变更"""
        styles = {
            ConnectionStatus.CONNECTED: ("已连接", STATUS_READY_STYLE),
            ConnectionStatus.CONNECTING: ("连接中...", STATUS_THINKING_STYLE),
            ConnectionStatus.RECONNECTING: ("重连中...", STATUS_THINKING_STYLE),
            ConnectionStatus.DISCONNECTED: ("未连接", STATUS_ERROR_STYLE),
            ConnectionStatus.ERROR: ("连接错误", STATUS_ERROR_STYLE),
        }
        text, style = styles.get(status, ("未知", STATUS_ERROR_STYLE))
        self.conn_status_label.setText(text)
        self.conn_status_label.setStyleSheet(style)

    # ==================================================================
    # 初始数据加载
    # ==================================================================

    def _load_initial_data(self):
        """加载初始数据（通过 API）"""
        self._show_welcome()
        self._refresh_file_tree()
        self._update_memory_stats()
        self._update_kb_stats()
        self._refresh_history_list()

    def _load_cached_data(self):
        """从缓存加载离线数据"""
        cache = self._state.cache

        # 尝试从缓存加载知识库
        cached_kb = cache.get_preloaded("knowledge_index")
        if cached_kb:
            items = cached_kb.get("items", []) if isinstance(cached_kb, dict) else cached_kb
            if isinstance(items, list) and items:
                self._state.set_knowledge_cache(items)
                self.kb_list.clear()
                for item in items[:20]:
                    self.kb_list.addItem(f"📄 {item.get('title', '无标题')}")
                logger.info(f"离线模式: 从缓存加载 {len(items)} 条知识")

        # 尝试从缓存加载系统状态
        cached_status = cache.get_preloaded("status")
        if cached_status:
            version = cached_status.get("version", "?")
            self.kb_stats_label.setText(f"条目: (缓存) 版本: {version}")

        # 文件树仍可用（本地文件系统）
        self._refresh_file_tree()
        logger.info("离线模式: 缓存数据已加载")

    # ── WebSocket 实时对话 ──

    def _connect_websocket(self):
        """建立 WebSocket 连接"""
        try:
            ws_base = self._state.connection.ws_base
            ws_url = f"{ws_base}/ws"
            from somngui.client.websocket_client import SomnWebSocketClient
            self._ws_client = SomnWebSocketClient(ws_url)
            self._ws_client.set_callbacks(
                on_message=self._on_ws_message,
                on_status=self._on_ws_status,
                on_error=self._on_ws_error,
                on_connected=self._on_ws_connected,
                on_disconnected=self._on_ws_disconnected,
            )
            self._ws_client.connect()
            logger.info(f"WebSocket 正在连接: {ws_url}")
        except Exception as e:
            logger.warning(f"WebSocket 初始化失败 (将使用 HTTP): {e}")
            self._ws_client = None

    def _on_ws_connected(self):
        """WebSocket 连接成功"""
        logger.info("WebSocket 已连接，实时对话已启用")

    def _on_ws_disconnected(self):
        """WebSocket 断开"""
        logger.warning("WebSocket 已断开，降级到 HTTP")

    def _on_ws_status(self, content: str, session_id: str):
        """收到状态消息（如"正在处理..."）"""
        # 可在状态栏显示
        self.status_bar.showMessage(f"AI: {content}", 5000)

    def _on_ws_message(self, content: str, session_id: str, msg: dict):
        """收到 WebSocket 回复"""
        self._set_agent_status("ready")
        if session_id and not self._state.current_session_id:
            self._state.set_session_id(session_id)
        self.chat_display.append(format_agent_message(content))
        self._state.add_chat_message("agent", content)

    def _on_ws_error(self, error: str):
        """WebSocket 错误"""
        self._set_agent_status("ready")
        self.chat_display.append(format_system_message(f"⚠️ WebSocket 错误: {error}"))

    def _show_welcome(self):
        """显示欢迎消息"""
        self.chat_display.append(format_system_message(WELCOME_MESSAGE))

    # ── 插件系统 ──

    def _load_plugins(self):
        """加载所有插件"""
        try:
            app_context = {
                "main_window": self,
                "state": self._state,
                "config": self._config,
            }
            loaded = self._plugin_manager.load_all(app_context)
            if loaded > 0:
                self.chat_display.append(
                    format_system_message(f"🔌 已加载 {loaded} 个插件")
                )
        except Exception as e:
            logger.warning(f"插件加载失败: {e}")

    def _notify_plugins_chat(self, role: str, content: str):
        """通知插件有新聊天消息"""
        extras = self._plugin_manager.notify_chat_message(role, content)
        for extra in extras:
            self.chat_display.append(format_system_message(f"🔌 {extra}"))

    # ── 历史对话面板 ──

    def _refresh_history_list(self, search_query: str = ""):
        """刷新历史对话列表"""
        self.history_list.clear()
        try:
            db = self._state.chat_db
            if search_query:
                sessions = db.list_sessions(limit=50)
                # 本地过滤标题
                sessions = [s for s in sessions if search_query.lower() in s.get("title", "").lower()]
            else:
                sessions = db.list_sessions(limit=50)

            for s in sessions:
                title = s.get("title", "无标题")
                msg_count = s.get("message_count", 0)
                updated = s.get("updated_at", 0)
                from datetime import datetime as dt
                time_str = dt.fromtimestamp(updated).strftime("%m/%d %H:%M") if updated else ""
                is_pinned = s.get("is_pinned", 0)

                display = f"{'📌 ' if is_pinned else ''}{title} ({msg_count})"
                item = QListWidgetItem(display)
                item.setData(Qt.ItemDataRole.UserRole, s["id"])
                item.setData(Qt.ItemDataRole.UserRole + 1, title)
                item.setToolTip(f"{title}\n消息数: {msg_count}\n时间: {time_str}")
                self.history_list.addItem(item)
        except Exception as e:
            logger.warning(f"刷新历史列表失败: {e}")

    @pyqtSlot()
    def _on_history_search(self, text: str):
        """搜索历史对话"""
        if len(text) >= 1:
            self._refresh_history_list(text)
        else:
            self._refresh_history_list()

    @pyqtSlot()
    def _on_history_item_clicked(self, item: QListWidgetItem):
        """点击历史对话 — 预览"""
        session_id = item.data(Qt.ItemDataRole.UserRole)
        if not session_id:
            return
        try:
            messages = self._state.chat_db.get_messages(session_id, limit=3)
            if messages:
                preview = "\n".join(
                    f"[{m.get('role', '?')}] {m.get('content', '')[:60]}"
                    for m in messages
                )
                self.status_bar.showMessage(f"📄 {item.data(Qt.ItemDataRole.UserRole + 1)}: {len(messages)} 条消息")
            else:
                self.status_bar.showMessage(f"📄 {item.data(Qt.ItemDataRole.UserRole + 1)}: 空对话")
        except Exception as e:
            logger.warning(f"预览历史对话失败: {e}")

    @pyqtSlot()
    def _on_history_item_dblclicked(self, item: QListWidgetItem):
        """双击历史对话 — 加载到聊天区"""
        session_id = item.data(Qt.ItemDataRole.UserRole)
        if not session_id:
            return
        try:
            messages = self._state.chat_db.get_messages(session_id, limit=200)
            self.chat_display.clear()
            self._show_welcome()
            from somngui.gui._types import ChatMessage
            self._state._chat_history.clear()
            self._state._current_session_id = session_id

            for msg in messages:
                role = msg.get("role", "system")
                content = msg.get("content", "")
                if role == "user":
                    self.chat_display.append(format_user_message(content))
                elif role == "agent":
                    self.chat_display.append(format_agent_message(content))
                else:
                    self.chat_display.append(format_system_message(content))
                self._state._chat_history.append(
                    ChatMessage(role=role, content=content, timestamp="")
                )

            self.status_bar.showMessage(f"已加载对话: {item.data(Qt.ItemDataRole.UserRole + 1)} ({len(messages)} 条)")
            logger.info(f"已加载历史对话: {session_id}, {len(messages)} 条消息")
        except Exception as e:
            logger.error(f"加载历史对话失败: {e}")

    def _on_history_context_menu(self, pos):
        """历史对话右键菜单"""
        item = self.history_list.itemAt(pos)
        if not item:
            return
        session_id = item.data(Qt.ItemDataRole.UserRole)

        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)

        pin_action = menu.addAction("📌 置顶/取消置顶")
        rename_action = menu.addAction("✏️ 重命名")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️ 删除")

        action = menu.exec(self.history_list.mapToGlobal(pos))
        if action == pin_action:
            self._state.chat_db.pin_session(session_id)
            self._refresh_history_list()
        elif action == rename_action:
            new_title, ok = QInputDialog.getText(
                self, "重命名对话", "新标题:",
                text=item.data(Qt.ItemDataRole.UserRole + 1)
            )
            if ok and new_title.strip():
                self._state.chat_db.update_session_title(session_id, new_title.strip())
                self._refresh_history_list()
        elif action == delete_action:
            reply = QMessageBox.question(
                self, "删除对话", f"确定删除对话「{item.data(Qt.ItemDataRole.UserRole + 1)}」？\n此操作不可恢复。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._state.chat_db.delete_session(session_id)
                self._refresh_history_list()
                if self._state.current_session_id == session_id:
                    self.chat_display.clear()
                    self._show_welcome()

    @pyqtSlot()
    def _on_new_chat(self):
        """新建对话"""
        self._state.clear_chat_history()
        self.chat_display.clear()
        self._show_welcome()
        self.status_bar.showMessage("新对话已创建", 2000)

    @pyqtSlot()
    def _on_delete_current_chat(self):
        """删除当前对话"""
        session_id = self._state.current_session_id
        if not session_id:
            self.status_bar.showMessage("没有当前对话可删除", 2000)
            return
        reply = QMessageBox.question(
            self, "删除对话", "确定删除当前对话？\n此操作不可恢复。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._state.delete_current_session()
            self.chat_display.clear()
            self._show_welcome()
            self._refresh_history_list()
            self.status_bar.showMessage("对话已删除", 2000)

    # ==================================================================
    # 对话功能
    # ==================================================================

    @pyqtSlot()
    def _on_send_message(self):
        """发送消息"""
        user_input = self.chat_input.text().strip()
        if not user_input:
            return

        # 显示用户消息
        self.chat_display.append(format_user_message(user_input))
        self._state.add_chat_message("user", user_input)
        self.chat_input.clear()

        # 通知插件
        self._notify_plugins_chat("user", user_input)

        # 更新状态
        self._set_agent_status("thinking")

        # 优先 WebSocket，降级到 HTTP
        if hasattr(self, '_ws_client') and self._ws_client and self._ws_client.is_connected:
            sid = self._state.current_session_id or ""
            self._ws_client.send_chat(user_input, sid)
        else:
            worker = ApiWorker(self._state.api.chat, user_input,
                               session_id=self._state.current_session_id)
            worker.result_ready.connect(self._on_chat_response)
            worker.error_occurred.connect(self._on_chat_error)
            worker.start()

    def _on_chat_response(self, result: dict):
        """收到 API 回复"""
        self._set_agent_status("ready")

        if result.get("success", False):
            content = result.get("response", result.get("content", ""))
            if isinstance(content, dict):
                content = str(content)
            self.chat_display.append(format_agent_message(content))
            self._state.add_chat_message("agent", content)

            # 保存 session_id
            session_id = result.get("session_id")
            if session_id:
                self._state.set_session_id(session_id)
        else:
            error = result.get("error", "未知错误")
            self.chat_display.append(format_system_message(f"❌ 错误: {error}"))
            self._state.add_chat_message("system", f"错误: {error}")

    def _on_chat_error(self, error: str):
        """对话请求失败"""
        self._set_agent_status("error")
        self.chat_display.append(format_system_message(f"❌ 请求失败: {error}"))

    def _set_agent_status(self, status: str):
        """更新智能体状态标签"""
        mapping = {
            "ready": ("就绪", STATUS_READY_STYLE),
            "thinking": ("思考中...", STATUS_THINKING_STYLE),
            "error": ("错误", STATUS_ERROR_STYLE),
        }
        text, style = mapping.get(status, ("就绪", STATUS_READY_STYLE))
        self.agent_status.setText(text)
        self.agent_status.setStyleSheet(style)
        self._state.set_chat_status(status)

    @pyqtSlot(str)
    def _on_quick_command(self, command: str):
        """快速命令"""
        self.chat_input.setText(command)
        self._on_send_message()

    @pyqtSlot()
    def _on_clear_chat(self):
        """清空对话"""
        self.chat_display.clear()
        self._state.clear_chat_history()
        self._show_welcome()

    def _on_upload_sticker(self):
        """上传表情包"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择表情包图片", str(Path.home()),
            "图片文件 (*.png *.jpg *.jpeg *.gif *.webp *.bmp)"
        )
        if not file_path:
            return
        # TODO: 实现表情包 API 上传
        self.chat_display.append(format_system_message(f"📷 表情包功能开发中..."))

    def _on_chat_message_from_state(self, msg):
        """从 AppState 收到新消息（外部触发时）"""
        if msg.role == "user":
            self.chat_display.append(format_user_message(msg.content))
        elif msg.role == "agent":
            self.chat_display.append(format_agent_message(msg.content))
        elif msg.role == "system":
            self.chat_display.append(format_system_message(msg.content))

    def _on_global_error(self, error_msg: str):
        """全局错误处理"""
        self.status_bar.showMessage(f"错误: {error_msg}", 5000)

    # ==================================================================
    # 文件操作
    # ==================================================================

    @pyqtSlot()
    def _on_new_document(self):
        self.tab_widget.setCurrentIndex(1)
        self.doc_title_input.clear()
        self.editor.clear()

    @pyqtSlot()
    def _on_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", str(self._workspace),
            "所有文件 (*.*);;文档 (*.docx *.pdf *.txt);;演示文稿 (*.pptx)"
        )
        if file_path:
            self._open_file(file_path)

    def _open_file(self, file_path: str):
        """打开文件到编辑器"""
        from somngui.utils.file_ops import extract_file_content

        path = Path(file_path)
        try:
            content = extract_file_content(path)
            self.doc_title_input.setText(path.stem)
            self.editor.setPlainText(content)
            self.tab_widget.setCurrentIndex(1)
            self.status_bar.showMessage(f"已打开: {file_path}")
        except Exception as e:
            QMessageBox.warning(self, "打开失败", f"无法打开文件: {e}")

    @pyqtSlot()
    def _on_save_document(self):
        title = self.doc_title_input.text().strip() or "未命名"
        content = self.editor.toPlainText()
        file_path = self._workspace / f"{title}.txt"
        try:
            file_path.write_text(content, encoding="utf-8")
            self.status_bar.showMessage(f"已保存: {file_path}")
            self._refresh_file_tree()
        except Exception as e:
            QMessageBox.warning(self, "保存失败", f"无法保存文件: {e}")

    @pyqtSlot()
    def _on_export_document(self):
        """导出文档（通过 API）"""
        title = self.doc_title_input.text().strip() or "未命名"
        content = self.editor.toPlainText()

        if not content.strip():
            QMessageBox.warning(self, "导出失败", "文档内容为空")
            return

        # 弹出格式选择
        dialog = QDialog(self)
        dialog.setWindowTitle("导出文档")
        form = QFormLayout(dialog)
        fmt_combo = QComboBox()
        fmt_combo.addItems(["docx", "pdf", "pptx", "xlsx"])
        form.addRow("格式:", fmt_combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            fmt = fmt_combo.currentText()
            self._set_agent_status("thinking")
            worker = ApiWorker(
                self._state.api.generate_document, "custom", title,
                format=fmt, context={"content": content}
            )
            worker.result_ready.connect(lambda r: self._on_export_done(r, fmt))
            worker.error_occurred.connect(self._on_chat_error)
            worker.start()

    def _on_export_done(self, result: dict, fmt: str):
        self._set_agent_status("ready")
        if result.get("success"):
            file_path = result.get("file_path", "")
            self.chat_display.append(format_system_message(f"✅ 文档已导出: {fmt}"))
            self.status_bar.showMessage(f"已导出: {file_path}")
        else:
            error = result.get("error", "导出失败")
            self.chat_display.append(format_system_message(f"❌ 导出失败: {error}"))

    @pyqtSlot()
    def _on_export_document_local(self):
        """本地文件导出（不经过后端 API）"""
        from somngui.utils.doc_export import EXPORT_FORMATS, export_document

        title = self.doc_title_input.text().strip() or "未命名"
        content = self.editor.toPlainText()

        if not content.strip():
            QMessageBox.warning(self, "导出失败", "文档内容为空")
            return

        # 弹出格式选择
        dialog = QDialog(self)
        dialog.setWindowTitle("导出文档")
        form = QFormLayout(dialog)
        filename_input = QLineEdit(title)
        form.addRow("文件名:", filename_input)
        fmt_combo = QComboBox()
        fmt_combo.addItems([f"{label} ({ext})" for ext, (label, _) in EXPORT_FORMATS.items()])
        form.addRow("格式:", fmt_combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 从显示文本提取扩展名
            display = fmt_combo.currentText()
            import re
            ext_match = re.search(r'(\.\w+)', display)
            ext = ext_match.group(1) if ext_match else ".txt"
            filename = filename_input.text().strip() or "未命名"
            if not filename.endswith(ext):
                filename += ext

            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出文档", str(self._workspace / filename),
                f"所有文件 (*.*)"
            )
            if file_path:
                try:
                    export_document(file_path, content, fmt=ext, title=title)
                    self.status_bar.showMessage(f"已导出: {file_path}")
                    self.chat_display.append(format_system_message(f"✅ 文档已导出: {file_path}"))
                except Exception as e:
                    QMessageBox.warning(self, "导出失败", str(e))

    @pyqtSlot()
    def _on_file_selected(self, item: QTreeWidgetItem, column: int):
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path:
            self._open_file(file_path)

    # ---- 文件树 ----

    def _refresh_file_tree(self):
        self.file_tree.clear()
        root = QTreeWidgetItem(self.file_tree)
        root.setText(0, "工作空间")
        root.setIcon(0, self.style().standardIcon(QStyle.SP_DirHomeIcon))
        # v1.0.0: 限制递归深度为 2，避免大工作空间启动慢
        self._populate_tree(root, self._workspace, max_depth=2)
        self.file_tree.expandItem(root)

    def _populate_tree(self, parent: QTreeWidgetItem, path: Path, max_depth: int = 2, _depth: int = 0):
        try:
            for item in sorted(path.iterdir()):
                # 跳过隐藏文件和 __pycache__
                if item.name.startswith(".") or item.name == "__pycache__":
                    continue
                tree_item = QTreeWidgetItem(parent)
                tree_item.setText(0, item.name)
                if item.is_dir():
                    tree_item.setIcon(0, self.style().standardIcon(QStyle.SP_DirIcon))
                    if _depth < max_depth:
                        self._populate_tree(tree_item, item, max_depth, _depth + 1)
                else:
                    tree_item.setIcon(0, self.style().standardIcon(QStyle.SP_FileIcon))
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, str(item))
        except PermissionError:
            pass

    # ==================================================================
    # 知识库
    # ==================================================================

    @pyqtSlot()
    def _on_search_kb(self):
        query = self.kb_search_input.text().strip()
        if not query:
            return
        worker = ApiWorker(self._state.api.search_knowledge, query)
        worker.result_ready.connect(self._on_kb_search_done)
        worker.error_occurred.connect(self._on_chat_error)
        worker.start()

    def _on_kb_search_done(self, result: dict):
        if result.get("success"):
            items = result.get("results", [])
            self._state.set_knowledge_cache(items)
            self.kb_list.clear()
            for item in items:
                self.kb_list.addItem(f"📄 {item.get('title', '无标题')}")
            self.status_bar.showMessage(f"找到 {len(items)} 条结果")
        else:
            QMessageBox.warning(self, "搜索失败", result.get("error", "搜索失败"))

    @pyqtSlot()
    def _on_kb_item_selected(self, item: QListWidgetItem):
        index = self.kb_list.row(item)
        cache = self._state.knowledge_cache
        if 0 <= index < len(cache):
            entry = cache[index]
            detail = (
                f"标题: {entry.get('title', '无标题')}\n\n"
                f"内容: {entry.get('content', '无内容')}\n\n"
                f"类别: {entry.get('category', '未分类')}\n"
                f"来源: {entry.get('source', '未知')}"
            )
            QMessageBox.information(self, "知识详情", detail)

    def _refresh_kb_list(self):
        """刷新知识库列表"""
        worker = ApiWorker(self._state.api.list_knowledge)
        worker.result_ready.connect(self._on_kb_list_refreshed)
        worker.error_occurred.connect(self._on_chat_error)
        worker.start()

    def _on_kb_list_refreshed(self, result: dict):
        if result.get("success"):
            items = result.get("items", [])
            self._state.set_knowledge_cache(items)
            self.kb_list.clear()
            for item in items:
                self.kb_list.addItem(f"📄 {item.get('title', '无标题')}")
            self.status_bar.showMessage(f"知识库: {len(items)} 条")

    @pyqtSlot()
    def _on_kb_stats(self):
        """知识库统计"""
        worker = ApiWorker(self._state.api.get_status)
        worker.result_ready.connect(self._on_kb_stats_done)
        worker.error_occurred.connect(self._on_chat_error)
        worker.start()

    def _on_kb_stats_done(self, result: dict):
        if result.get("success"):
            data = result.get("data", {})
            self.kb_stats_label.setText(
                f"状态: {data.get('status', '未知')}\n"
                f"版本: {data.get('version', '?')}"
            )
            self.status_bar.showMessage("知识库统计已更新")

    # ==================================================================
    # 工具功能
    # ==================================================================

    @pyqtSlot()
    def _on_scan_files(self):
        """扫描工作空间文件"""
        from somngui.utils.file_ops import scan_directory

        self.chat_display.append(format_system_message("🔍 正在扫描工作空间..."))
        stats = scan_directory(self._workspace)
        top_exts = list(stats["by_ext"].items())[:5]
        ext_summary = "\n".join(f"  {ext}: {count}" for ext, count in top_exts)
        self.chat_display.append(format_system_message(
            f"✅ 扫描完成:\n"
            f"  文件: {stats['files']}\n"
            f"  目录: {stats['dirs']}\n"
            f"  总计: {stats['total']}\n\n"
            f"TOP 5 类型:\n{ext_summary}"
        ))
        self._refresh_file_tree()

    @pyqtSlot()
    def _on_clean_files(self):
        QMessageBox.information(
            self, "清理文件",
            "文件清理功能正在开发中。\n\n"
            "后续版本将支持:\n"
            "• 临时文件清理\n"
            "• 重复文件检测\n"
            "• 大文件分析"
        )

    @pyqtSlot()
    def _on_index_files(self):
        """索引文件到知识库（通过 API）"""
        self.chat_display.append(format_system_message("📁 正在索引文件..."))
        self._set_agent_status("thinking")
        # 暂无专用索引 API，用添加知识的方式
        self.chat_display.append(format_system_message(
            "📁 文件索引功能将通过后端 API 实现"
        ))
        self._set_agent_status("ready")

    @pyqtSlot()
    def _on_generate_report(self):
        """生成报告"""
        topic, ok = QInputDialog.getText(self, "生成报告", "请输入报告主题:")
        if ok and topic.strip():
            self.chat_input.setText(f"请生成一份关于 {topic.strip()} 的报告")
            self._on_send_message()

    @pyqtSlot()
    def _on_create_strategy(self):
        """制定策略"""
        desc, ok = QInputDialog.getText(self, "制定策略", "请描述需要制定的策略:")
        if ok and desc.strip():
            self._set_agent_status("thinking")
            worker = ApiWorker(self._state.api.strategy_analysis, desc.strip())
            worker.result_ready.connect(self._on_strategy_done)
            worker.error_occurred.connect(self._on_chat_error)
            worker.start()

    def _on_strategy_done(self, result: dict):
        self._set_agent_status("ready")
        if result.get("success"):
            content = result.get("strategy", result.get("response", ""))
            self.chat_display.append(format_agent_message(str(content)))
        else:
            error = result.get("error", "策略制定失败")
            self.chat_display.append(format_system_message(f"❌ {error}"))

    # ---- 文档创建快捷方式 ----

    @pyqtSlot()
    def _on_new_word(self):
        self.doc_title_input.setText("新建Word文档")
        self.editor.clear()
        self.tab_widget.setCurrentIndex(1)

    @pyqtSlot()
    def _on_new_ppt(self):
        self.doc_title_input.setText("新建PPT演示文稿")
        self.editor.clear()
        self.tab_widget.setCurrentIndex(1)

    @pyqtSlot()
    def _on_new_pdf(self):
        self.doc_title_input.setText("新建PDF文档")
        self.editor.clear()
        self.tab_widget.setCurrentIndex(1)

    @pyqtSlot()
    def _on_new_excel(self):
        self.doc_title_input.setText("新建Excel表格")
        self.editor.clear()
        self.tab_widget.setCurrentIndex(1)

    # ==================================================================
    # 统计更新
    # ==================================================================

    def _update_memory_stats(self):
        """通过 API 更新记忆统计"""
        worker = ApiWorker(self._state.api.list_memories, page_size=5)
        worker.result_ready.connect(self._on_memory_stats_done)
        # 不显示错误，静默处理
        worker.start()

    def _on_memory_stats_done(self, result: dict):
        if result.get("success"):
            data = result.get("data", {})
            memories = data.get("memories", data.get("items", []))
            total = data.get("total", len(memories))
            self.memory_stats.setText(f"记忆条目: {total}")
            self.recent_memories.clear()
            for mem in memories[:5]:
                ts = mem.get("timestamp", "")
                content = mem.get("content", "")
                preview = content[:30] + "..." if len(content) > 30 else content
                self.recent_memories.addItem(f"[{ts}] {preview}")

    def _update_kb_stats(self):
        """通过 API 更新知识库统计"""
        worker = ApiWorker(self._state.api.list_knowledge, page_size=1)
        worker.result_ready.connect(self._on_kb_stats_list_done)
        worker.start()

    def _on_kb_stats_list_done(self, result: dict):
        if result.get("success"):
            data = result.get("data", result)
            total = data.get("total", 0)
            self.kb_stats_label.setText(f"条目: {total}")

    # ==================================================================
    # 主题切换
    # ==================================================================

    def _populate_theme_menu(self):
        """v1.0.0: 首次展开主题菜单时，扫描可用主题（延迟加载）"""
        if self._theme_menu_populated:
            return
        self._theme_menu_populated = True

        from somngui.resources import list_available_themes
        # 找到 theme_menu（通过 sender）
        menu = self.sender()
        if menu is None:
            return

        current_theme = self._config.get("ui.theme", "auto")
        for theme_info in list_available_themes():
            name = theme_info["name"]
            label = theme_info["label"]
            action = QAction(label, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, n=name: self._switch_theme(n))
            if name == current_theme:
                action.setChecked(True)
                self._theme_actions.get("auto").setChecked(False)
            menu.addAction(action)
            self._theme_actions[name] = action

    def _switch_theme(self, theme: str):
        """切换界面主题 (light/dark/auto)"""
        from somngui.resources import _apply_qss_theme

        self._config.set("ui.theme", theme)

        # 更新菜单勾选
        for name, action in self._theme_actions.items():
            action.setChecked(name == theme)

        # 解析实际主题
        if theme == "auto":
            actual = _detect_system_dark() and "dark" or "light"
        else:
            actual = theme

        _apply_qss_theme(QApplication.instance(), actual)
        self._config.set("ui.active_theme", actual)
        logger.info(f"主题切换: 设置={theme}, 实际={actual}")

    def _refresh_all(self):
        """刷新所有数据"""
        self._refresh_file_tree()
        self._update_memory_stats()
        self._update_kb_stats()
        self.status_bar.showMessage("界面已刷新", 2000)

    # ==================================================================
    # 关于 & 关闭
    # ==================================================================

    @pyqtSlot()
    def _on_about(self):
        QMessageBox.about(
            self,
            "关于 Somn",
            "<h3>Somn v1.0</h3>"
            "<p>汇千古之智，向未知而生</p>"
            "<p>基于大模型与多智能体系统构建</p>"
            "<p>前后端分离架构，通过 REST API 通信</p>"
        )

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 断开 WebSocket
        if hasattr(self, '_ws_client') and self._ws_client:
            self._ws_client.disconnect()

        # 关闭缓存
        if hasattr(self, '_state') and self._state._cache is not None:
            self._state.cache.close()

        # 关闭对话历史数据库
        if hasattr(self, '_state') and self._state._chat_db is not None:
            self._state.chat_db.close()

        # TrayAwareMainWindow 的 _tray_close_event 会接管
        # 如果没有初始化 tray_manager，直接关闭
        if not hasattr(self, 'tray_manager'):
            event.accept()
            return
        # 调用 Mixin 的关闭逻辑
        self._tray_close_event(event)
