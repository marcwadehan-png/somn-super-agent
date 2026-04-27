# -*- coding: utf-8 -*-
"""
__all__ = [
    'run',
]

主窗口 - 兼容层 (v3.0)

将大型 MainWindow 类拆分委托给子模块，保持 Qt signal/slot 不变。

子模块:
  _mw_chat      - 对话界面与消息
  _mw_editor    - 文档编辑器
  _mw_kb        - 知识库界面
  _mw_kb_ops    - 知识库操作(搜索/选择/刷新/统计)
  _mw_file_ops  - 文件操作
  _mw_export    - 文档导出
  _mw_scan      - 文件扫描与索引
  _mw_tools     - 报告生成与策略制定

迁移进度: 1771行 -> 643行 (减少63.7%)
  [done] widget创建   -> 子模块
  [done] 消息方法     -> _mw_chat
  [done] 文档编辑     -> _mw_editor
  [done] 知识库界面   -> _mw_kb
  [done] KB操作       -> _mw_kb_ops
  [done] 文件操作     -> _mw_file_ops
  [done] 文档导出     -> _mw_export
  [done] 扫描/索引   -> _mw_scan
  [done] 报告/策略   -> _mw_tools
"""

import sys
from pathlib import Path
from typing import Optional
import subprocess
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QSplitter,
    QTreeWidget, QTreeWidgetItem, QTabWidget, QStatusBar,
    QMenuBar, QMenu, QFileDialog, QMessageBox, QProgressBar,
    QDockWidget, QListWidget, QListWidgetItem, QFrame,
    QApplication, QSystemTrayIcon, QStyle, QDialog,
    QDialogButtonBox, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt, QSize, Signal, Slot, QThread, QObject
from PySide6.QtGui import QAction, QIcon, QFont, QKeySequence
from loguru import logger

from core.memory_system import MemorySystem
from core.knowledge_base import KnowledgeBase
from core.agent_core import AgentCore
from gui.tray_icon import TrayIconManager

# ---- 子模块委托 ----
from gui.main_window._mw_chat import (
    create_chat_widget,
    add_user_message as _mw_add_user,
    add_agent_message as _mw_add_agent,
    add_system_message as _mw_add_sys,
)
from gui.main_window._mw_editor import create_editor_widget
from gui.main_window._mw_kb import (
    create_kb_widget,
    show_knowledge_detail as _mw_kb_detail,
    edit_knowledge_entry as _mw_kb_edit,
    delete_knowledge_entry as _mw_kb_del,
)
from gui.main_window._mw_file_ops import (
    open_file as _mw_fo_open,
    new_word_doc as _mw_fo_word,
    new_ppt_doc as _mw_fo_ppt,
    new_pdf_doc as _mw_fo_pdf,
    new_excel_doc as _mw_fo_excel,
)
from gui.main_window._mw_export import export_document as _mw_export_doc
from gui.main_window._mw_scan import scan_workspace, index_files_to_kb
from gui.main_window._mw_kb_ops import (
    search_knowledge as _mw_kb_search,
    on_kb_item_selected as _mw_kb_select,
    refresh_kb_list as _mw_kb_refresh,
    show_kb_stats as _mw_kb_stats,
)
from gui.main_window._mw_tools import generate_report, create_strategy

class AgentWorker(QThread):
    """智能体工作线程"""
    response_ready = Signal(str)
    thinking = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, agent_core: AgentCore, user_input: str, context: dict = None):
        super().__init__()
        self.agent_core = agent_core
        self.user_input = user_input
        self.context = context or {}

    def run(self):
        try:
            self.thinking.emit("思考中...")
            response = self.agent_core.process_input(
                self.user_input,
                context=self.context
            )
            self.response_ready.emit(response)
        except Exception as e:
            logger.error(f"Agent processing error: {e}")
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    """Somn 主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Somn - 汇千古之智，向未知而生")
        self.setMinimumSize(1200, 800)

        # [v9.0 优化] 快速初始化：先创建UI占位，再后台加载核心
        self.memory_system = None
        self.knowledge_base = None
        self.agent_core = None
        self.current_workspace = PROJECT_ROOT
        self.current_workspace.mkdir(parents=True, exist_ok=True)

        # 初始化状态
        self._init_status = "loading"  # loading | ready | error
        self._pending_initial_data = True

        # 快速设置UI（不阻塞）
        self._setup_menu()
        self._setup_ui()
        self._setup_status_bar()
        self._setup_shortcuts()
        self._setup_tray_icon()

        # [v9.0 优化] 后台线程加载核心组件
        self._init_thread = QThread()
        self._init_worker = CoreInitWorker()
        self._init_worker.moveToThread(self._init_thread)
        self._init_thread.started.connect(self._init_worker.run)
        self._init_worker.init_complete.connect(self._on_core_init_complete)
        self._init_worker.init_error.connect(self._on_core_init_error)
        self._init_thread.start()

        logger.info("主窗口init完成(核心组件后台加载中)")

    def _on_core_init_complete(self, memory, kb, agent):
        """核心组件初始化完成"""
        self.memory_system = memory
        self.knowledge_base = kb
        self.agent_core = agent
        self._init_status = "ready"

        # 加载初始数据
        if self._pending_initial_data:
            self._load_initial_data()
            self._pending_initial_data = False

        self.statusBar().showMessage("就绪", 3000)
        logger.info("核心组件加载完成")

        # 清理线程
        self._init_thread.quit()
        self._init_worker.deleteLater()

    def _on_core_init_error(self, error_msg):
        """核心组件初始化失败"""
        self._init_status = "error"
        logger.error(f"核心组件初始化失败: {error_msg}")
        self.statusBar().showMessage(f"初始化失败: {error_msg}", 5000)

        # 清理线程
        self._init_thread.quit()
        self._init_worker.deleteLater()

    def _ensure_core_ready(self):
        """确保核心组件就绪（首调优化）"""
        if self._init_status == "loading":
            # 等待后台初始化完成（最多等待5秒）
            if self._init_thread.isRunning():
                self._init_thread.wait(5000)
        return self._init_status == "ready"


class CoreInitWorker(QObject):
    """[v9.0 优化] 核心组件后台初始化工作器"""
    init_complete = Signal(object, object, object)  # memory, kb, agent
    init_error = Signal(str)

    def run(self):
        """后台初始化核心组件"""
        try:
            # 初始化记忆系统（默认不加载ChromaDB）
            memory = MemorySystem()
            kb = KnowledgeBase()
            agent = AgentCore(memory, kb)

            self.init_complete.emit(memory, kb, agent)
        except Exception as e:
            self.init_error.emit(str(e))

    def _setup_tray_icon(self):
        try:
            self.tray_manager = TrayIconManager(self, "SmartOffice AI")
            self.tray_manager.show_window_requested.connect(self.show)
            self.tray_manager.quit_requested.connect(self._on_tray_quit)
            self.tray_manager.quick_action_triggered.connect(self._on_tray_quick_action)
            self.tray_manager.show()
            logger.info("系统托盘图标已设置")
        except Exception as e:
            logger.warning(f"系统托盘设置失败: {e}")

    def _on_tray_quit(self):
        if hasattr(self, 'agent_workers'):
            for worker in self.agent_workers:
                try:
                    worker.wait(5000)
                except Exception as e:
                    logger.warning(f"等待工作线程完成失败: {e}")
        self.memory_system.consolidate_memories()
        logger.info("从托盘退出应用")
        QApplication.quit()

    def _on_tray_quick_action(self, action_id: str):
        if action_id == "new_doc":
            self._on_new_document()
        elif action_id == "search_kb":
            self.tab_widget.setCurrentIndex(2)
        elif action_id == "gen_report":
            self._on_generate_report()
        elif action_id == "clean_files":
            self._on_clean_files()
        elif action_id == "settings":
            QMessageBox.information(
                self, "设置",
                "设置功能开发中...\n\n请在 config.yaml 中手动配置."
            )

    def _setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("文件(&F)")
        new_doc_action = QAction("新建文档", self)
        new_doc_action.setShortcut(QKeySequence.New)
        new_doc_action.triggered.connect(self._on_new_document)
        file_menu.addAction(new_doc_action)
        open_action = QAction("打开文件", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        tools_menu = menubar.addMenu("工具(&T)")
        scan_files_action = QAction("🔍 扫描文件", self)
        scan_files_action.triggered.connect(self._on_scan_files)
        tools_menu.addAction(scan_files_action)
        clean_files_action = QAction("🧹 清理文件", self)
        clean_files_action.triggered.connect(self._on_clean_files)
        tools_menu.addAction(clean_files_action)
        tools_menu.addSeparator()
        gen_report_action = QAction("📊 生成报告", self)
        gen_report_action.triggered.connect(self._on_generate_report)
        tools_menu.addAction(gen_report_action)
        gen_strategy_action = QAction("🎯 制定策略", self)
        gen_strategy_action.triggered.connect(self._on_create_strategy)
        tools_menu.addAction(gen_strategy_action)
        tools_menu.addSeparator()
        index_files_action = QAction("📁 索引文件", self)
        index_files_action.triggered.connect(self._on_index_files)
        tools_menu.addAction(index_files_action)
        kb_stats_action = QAction("📚 知识库统计", self)
        kb_stats_action.triggered.connect(self._on_kb_stats)
        tools_menu.addAction(kb_stats_action)

        help_menu = menubar.addMenu("帮助(&H)")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        splitter.addWidget(self._create_left_panel())
        splitter.addWidget(self._create_center_panel())
        splitter.addWidget(self._create_right_panel())
        splitter.setSizes([250, 700, 250])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

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

        quick_label = QLabel("⚡ 快速操作")
        quick_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(quick_label)

        quick_buttons = [
            ("📄 新建 Word", self._on_new_word),
            ("📊 新建 PPT", self._on_new_ppt),
            ("📑 新建 PDF", self._on_new_pdf),
            ("📈 新建 Excel", self._on_new_excel),
            ("🔍 扫描目录", self._on_scan_files),
            ("🧹 清理文件", self._on_clean_files),
        ]

        for text, callback in quick_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()
        return panel

    def _create_center_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self._create_chat_widget(), "💬 智能对话")
        self.tab_widget.addTab(self._create_editor_widget(), "📝 文档编辑")
        self.tab_widget.addTab(self._create_kb_widget(), "📚 知识库")
        layout.addWidget(self.tab_widget)
        return panel

    # ---- 委托: widget 创建 ----
    def _create_chat_widget(self) -> QWidget:
        return create_chat_widget(self)

    def _create_editor_widget(self) -> QWidget:
        return create_editor_widget(self)

    def _create_kb_widget(self) -> QWidget:
        return create_kb_widget(self)

    def _create_right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setMaximumWidth(300)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)

        status_label = QLabel("🤖 智能体状态")
        status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(status_label)

        self.agent_status = QLabel("就绪")
        self.agent_status.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.agent_status)

        memory_label = QLabel("🧠 记忆统计")
        memory_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(memory_label)

        self.memory_stats = QLabel("短期记忆: 0\n长期记忆: 0")
        self.memory_stats.setStyleSheet("padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        layout.addWidget(self.memory_stats)

        recent_label = QLabel("📋 最近记忆")
        recent_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(recent_label)

        self.recent_memories = QListWidget()
        layout.addWidget(self.recent_memories)

        kb_stats_label = QLabel("📚 知识库")
        kb_stats_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(kb_stats_label)

        self.kb_stats_label = QLabel("条目: 0\n概念: 0")
        self.kb_stats_label.setStyleSheet("padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        layout.addWidget(self.kb_stats_label)

        layout.addStretch()
        return panel

    def _setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _setup_shortcuts(self):
        clear_action = QAction("清空对话", self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.triggered.connect(self._on_clear_chat)
        self.addAction(clear_action)

    def _load_initial_data(self):
        self._update_memory_stats()
        self._update_kb_stats()
        self._refresh_file_tree()
        self._add_system_message(
            "👋 欢迎使用 Somn!\n\n"
            "汇千古之智，向未知而生。\n\n"
            "我能帮你：\n"
            "• 📄 生成各类文档(Word/PPT/PDF/Excel)\n"
            "• 🔍 管理和检索知识\n"
            "• 💡 回答问题,提供建议\n"
            "• 📊 分析数据和撰写报告\n"
            "• 🔍 扫描和分析文件系统\n"
            "• 🎯 制定执行策略\n"
            "• 📈 ML预测分析\n\n"
            "有什么我可以帮你的吗?"
        )

    # ===== 事件处理 =====
    @Slot()
    def _on_send_message(self):
        user_input = self.chat_input.text().strip()
        if not user_input:
            return
        self._add_user_message(user_input)
        self.chat_input.clear()

        self.agent_status.setText("思考中...")
        self.agent_status.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
            }
        """)

        self.worker = AgentWorker(self.agent_core, user_input)
        self.worker.response_ready.connect(self._on_agent_response)
        self.worker.error_occurred.connect(self._on_agent_error)
        self.worker.start()

    @Slot(str)
    def _on_agent_response(self, response: str):
        self._add_agent_message(response)
        self.agent_status.setText("就绪")
        self.agent_status.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self._update_memory_stats()

    @Slot(str)
    def _on_agent_error(self, error: str):
        self._add_system_message(f"❌ 错误: {error}")

    def _on_upload_sticker(self):
        try:
            from PySide6.QtWidgets import QFileDialog
            from PySide6.QtGui import QPixmap
            from pathlib import Path
        except ImportError:
            QMessageBox.warning(self, "错误", "无法导入文件对话框")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择表情包图片", str(Path.home()),
            "图片文件 (*.png *.jpg *.jpeg *.gif *.webp *.bmp)"
        )
        if not file_path:
            return

        try:
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.warning(self, "错误", "无法读取图片文件")
                return

            from src.intelligence.sticker_saver import get_sticker_saver
            saver = get_sticker_saver()
            result = saver.save_from_file(file_path)

            if result.success:
                self._add_system_message(
                    f"✅ 表情包已保存!\n"
                    f"  ID: {result.sticker_id}\n"
                    f"  尺寸: {result.info.get('width', '?')}x{result.info.get('height', '?')}\n"
                    f"  路径: {result.info.get('file_path', '')}\n\n"
                    f"后续聊天中可以直接使用该表情包."
                )
                self.status_bar.showMessage(f"表情包已保存: {result.sticker_id}")
            else:
                QMessageBox.warning(self, "保存失败", result.message)

        except Exception as e:
            logger.error(f"上传表情包失败: {e}")
            QMessageBox.warning(self, "错误", f"上传失败: {e}")

        self.agent_status.setText("错误")
        self.agent_status.setStyleSheet("""
            QLabel {
                background-color: #f8d7da;
                color: #721c24;
                padding: 10px;
                border-radius: 5px;
            }
        """)

    @Slot(str)
    def _on_quick_command(self, command: str):
        self.chat_input.setText(command)
        self._on_send_message()

    # ---- 委托: 消息方法 ----
    def _add_user_message(self, message: str):
        _mw_add_user(self, message)

    def _add_agent_message(self, message: str):
        _mw_add_agent(self, message)

    def _add_system_message(self, message: str):
        _mw_add_sys(self, message)

    @Slot()
    def _on_clear_chat(self):
        self.chat_display.clear()

    def _update_memory_stats(self):
        stats = self.memory_system.get_stats()
        self.memory_stats.setText(
            f"短期记忆: {stats.get('short_term', 0)}\n"
            f"长期记忆: {stats.get('long_term', 0)}\n"
            f"情景记忆: {stats.get('episodic', 0)}"
        )
        self.recent_memories.clear()
        recent = self.memory_system.short_term_memory[-5:]
        for mem in reversed(recent):
            item_text = f"[{mem.timestamp.strftime('%H:%M')}] {mem.content[:30]}..."
            self.recent_memories.addItem(item_text)

    def _update_kb_stats(self):
        stats = self.knowledge_base.get_stats()
        self.kb_stats_label.setText(
            f"条目: {stats['knowledge_entries']}\n"
            f"概念: {stats['concepts']}\n"
            f"索引文件: {stats['indexed_files']}"
        )

    def _refresh_file_tree(self):
        self.file_tree.clear()
        root_item = QTreeWidgetItem(self.file_tree)
        root_item.setText(0, "工作空间")
        root_item.setIcon(0, self.style().standardIcon(QStyle.SP_DirHomeIcon))
        self._populate_tree(root_item, self.current_workspace)
        self.file_tree.expandItem(root_item)

    def _populate_tree(self, parent_item: QTreeWidgetItem, path: Path):
        try:
            for item in sorted(path.iterdir()):
                tree_item = QTreeWidgetItem(parent_item)
                tree_item.setText(0, item.name)
                if item.is_dir():
                    tree_item.setIcon(0, self.style().standardIcon(QStyle.SP_DirIcon))
                    self._populate_tree(tree_item, item)
                else:
                    tree_item.setIcon(0, self.style().standardIcon(QStyle.SP_FileIcon))
                    tree_item.setData(0, Qt.UserRole, str(item))
        except PermissionError:
            pass

    # ===== 文件操作 =====
    @Slot()
    def _on_new_document(self):
        self.tab_widget.setCurrentIndex(1)
        self.doc_title_input.clear()
        self.editor.clear()

    @Slot()
    def _on_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", str(self.current_workspace),
            "所有文件 (*.*);;文档 (*.docx *.pdf *.txt);;演示文稿 (*.pptx)"
        )
        if file_path:
            self._open_file(file_path)

    def _open_file(self, file_path: str):
        _mw_fo_open(self, file_path)

    @Slot()
    def _on_new_word(self):
        _mw_fo_word(self)

    @Slot()
    def _on_new_ppt(self):
        _mw_fo_ppt(self)

    @Slot()
    def _on_new_pdf(self):
        _mw_fo_pdf(self)

    @Slot()
    def _on_new_excel(self):
        _mw_fo_excel(self)

    @Slot()
    def _on_save_document(self):
        title = self.doc_title_input.text() or "未命名"
        content = self.editor.toPlainText()
        file_path = self.current_workspace / f"{title}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.status_bar.showMessage(f"已保存: {file_path}")
        self._refresh_file_tree()

    @Slot()
    def _on_export_document(self):
        _mw_export_doc(self)

    @Slot()
    def _on_file_selected(self, item: QTreeWidgetItem):
        file_path = item.data(0, Qt.UserRole)
        if file_path:
            self._open_file(file_path)

    @Slot()
    def _on_scan_files(self):
        scan_workspace(self)

    @Slot()
    def _on_clean_files(self):
        self._add_system_message("🧹 文件清理功能开发中...")
        QMessageBox.information(
            self, "清理文件",
            "文件清理功能正在开发中。\n\n"
            "后续版本将支持:\n"
            "• 临时文件清理\n"
            "• 重复文件检测\n"
            "• 大文件分析"
        )

    # ===== 知识库管理（委托）=====
    @Slot()
    def _on_search_kb(self):
        _mw_kb_search(self)

    @Slot()
    def _on_kb_item_selected(self, item: QListWidgetItem):
        _mw_kb_select(self, item)

    def _show_knowledge_detail(self, entry_id: str):
        _mw_kb_detail(self, entry_id)

    def _refresh_kb_list(self):
        _mw_kb_refresh(self)

    @Slot()
    def _on_index_files(self):
        index_files_to_kb(self)

    @Slot()
    def _on_kb_stats(self):
        _mw_kb_stats(self)

    # ===== 报告与策略（委托）=====
    @Slot()
    def _on_generate_report(self):
        generate_report(self)

    @Slot()
    def _on_create_strategy(self):
        create_strategy(self)

    @Slot()
    def _on_about(self):
        QMessageBox.about(
            self,
            "关于 Somn",
            "<h3>Somn v1.0</h3>"
            "<p>汇千古之智，向未知而生</p>"
            "<p>基于大模型与多智能体系统构建</p>"
            "<p>支持文档处理、知识管理、数据分析等功能</p>"
        )
