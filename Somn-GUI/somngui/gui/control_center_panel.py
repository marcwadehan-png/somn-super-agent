#!/usr/bin/env python3
"""
Somn 全局控制中心面板 - PyQt6 集成版
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QTabWidget, QGroupBox, QScrollArea, QFrame,
    QProgressBar, QTextEdit, QLineEdit, QComboBox,
    QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QBrush, QColor

logger = logging.getLogger(__name__)


class ControlCenterPanel(QWidget):
    """Somn 全局控制中心面板"""

    def __init__(self, parent=None, api_url: str = None):
        super().__init__(parent)
        from somngui.core.connection import BackendConnection
        self.api_url = api_url or BackendConnection.DEFAULT_URL
        self.init_ui()
        self.start_monitoring()

    def init_ui(self):
        """初始化UI"""
        self.setMinimumSize(1000, 700)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 标题栏
        title_bar = self._create_title_bar()
        main_layout.addWidget(title_bar)

        # 选项卡
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_dashboard_tab(), "📊 仪表板")
        self.tabs.addTab(self._create_modules_tab(), "📦 模块")
        self.tabs.addTab(self._create_engines_tab(), "⚙️ 引擎")
        self.tabs.addTab(self._create_claws_tab(), "🦷 Claw")
        self.tabs.addTab(self._create_neural_tab(), "🧠 神经网络")
        self.tabs.addTab(self._create_logs_tab(), "📋 日志")
        self.tabs.addTab(self._create_config_tab(), "⚡ 配置")

        main_layout.addWidget(self.tabs)

        # 状态栏
        self.status_bar = self._create_status_bar()
        main_layout.addWidget(self.status_bar)

    def _create_title_bar(self) -> QWidget:
        """标题栏"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 5)

        title = QLabel("🧠 Somn V1.0 全局控制中心")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00c853;")
        layout.addWidget(title)

        layout.addStretch()

        # 快捷按钮
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)

        return widget

    def _create_dashboard_tab(self) -> QWidget:
        """仪表板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 统计卡片
        cards_layout = QGridLayout()

        # 模块卡片
        self.module_card = self._create_stat_card(
            "📦 模块", "32", "28 运行中",
            ["系统模块", "应用模块", "工具模块"]
        )
        cards_layout.addWidget(self.module_card, 0, 0)

        # 引擎卡片
        self.engine_card = self._create_stat_card(
            "⚙️ 智慧引擎", "45+", "38 活跃",
            ["哲学引擎", "科学引擎", "社会学引擎"]
        )
        cards_layout.addWidget(self.engine_card, 0, 1)

        # Claw卡片
        self.claw_card = self._create_stat_card(
            "🦷 Claw代理", "776", "150 活跃",
            ["哲学派", "兵家派", "道家派", "儒家派"]
        )
        cards_layout.addWidget(self.claw_card, 0, 2)

        # 神经网络卡片
        self.neural_card = self._create_stat_card(
            "🧠 神经网络", "57 神经元", "74 突触",
            ["Phase 1-5", "4 集群"]
        )
        cards_layout.addWidget(self.neural_card, 1, 0)

        # 调度器卡片
        self.scheduler_card = self._create_stat_card(
            "📅 全局调度器", "运行中", "0 队列",
            ["智慧分析", "Claw调度", "学习系统"]
        )
        cards_layout.addWidget(self.scheduler_card, 1, 1)

        # 健康状态卡片
        self.health_card = self._create_stat_card(
            "💚 健康检查", "正常", "0 警告",
            ["后端服务", "API响应", "内存使用"]
        )
        cards_layout.addWidget(self.health_card, 1, 2)

        layout.addLayout(cards_layout)
        layout.addStretch()
        return widget

    def _create_stat_card(self, title: str, main_value: str, sub_value: str, details: list) -> QWidget:
        """统计卡片"""
        card = QGroupBox(title)
        card.setFixedHeight(140)
        card.setStyleSheet("""
            QGroupBox {
                background: #252526;
                border: 1px solid #3e3e42;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(card)

        main = QLabel(main_value)
        main.setStyleSheet("font-size: 24px; color: #00c853;")
        main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(main)

        sub = QLabel(sub_value)
        sub.setStyleSheet("color: #d4d4d4;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub)

        details_widget = QWidget()
        details_layout = QHBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 5, 0, 0)
        for d in details[:3]:
            label = QLabel(d)
            label.setStyleSheet("color: #858585; font-size: 10px;")
            details_layout.addWidget(label)
        layout.addWidget(details_widget)

        return card

    def _create_modules_tab(self) -> QWidget:
        """模块管理"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 工具栏
        toolbar = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("🔍 搜索模块...")
        toolbar.addWidget(search)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # 模块表格
        self.module_table = QTableWidget()
        self.module_table.setColumnCount(5)
        self.module_table.setHorizontalHeaderLabels(["模块名称", "类型", "状态", "加载时间", "操作"])
        self.module_table.horizontalHeader().setStretchLastSection(True)
        self._populate_modules_table()
        layout.addWidget(self.module_table)

        return widget

    def _populate_modules_table(self):
        """填充模块表格"""
        modules = [
            ("src.somn", "核心", "✅ 运行中", "2.3s", "停用"),
            ("src.intelligence", "智能", "✅ 运行中", "1.8s", "停用"),
            ("src.intelligence.engines", "引擎", "✅ 运行中", "0.5s", "停用"),
            ("src.intelligence.dispatcher", "调度", "✅ 运行中", "0.3s", "停用"),
            ("src.intelligence.claws", "Claw", "✅ 运行中", "0.8s", "停用"),
            ("src.intelligence.scheduler", "调度器", "✅ 运行中", "0.4s", "停用"),
            ("src.neural_layout", "神经网络", "✅ 运行中", "0.6s", "停用"),
            ("src.evolution", "进化", "✅ 运行中", "1.2s", "停用"),
            ("src.memory", "记忆", "✅ 运行中", "0.7s", "停用"),
            ("src.learning", "学习", "✅ 运行中", "0.9s", "停用"),
        ]
        self.module_table.setRowCount(len(modules))
        for i, m in enumerate(modules):
            for j, val in enumerate(m):
                item = QTableWidgetItem(val)
                if j == 2:
                    item.setForeground(QBrush(QColor("green")))
                self.module_table.setItem(i, j, item)

    def _create_engines_tab(self) -> QWidget:
        """引擎监控"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.engine_table = QTableWidget()
        self.engine_table.setColumnCount(5)
        self.engine_table.setHorizontalHeaderLabels(["学派", "引擎", "状态", "请求数", "平均延迟"])
        self.engine_table.horizontalHeader().setStretchLastSection(True)
        self._populate_engines_table()
        layout.addWidget(self.engine_table)

        return widget

    def _populate_engines_table(self):
        """填充引擎表格"""
        engines = [
            ("儒家", "RuWisdomCore", "✅ 运行中", "1,234", "12ms"),
            ("道家", "DaoWisdomCore", "✅ 运行中", "987", "15ms"),
            ("兵家", "BingWisdomCore", "✅ 运行中", "756", "18ms"),
            ("经济学", "JingjiWisdomCore", "✅ 运行中", "654", "20ms"),
            ("心理学", "XinliWisdomCore", "✅ 运行中", "543", "16ms"),
            ("社会学", "ShehuiWisdomCore", "✅ 运行中", "432", "14ms"),
            ("政治学", "ZhengzhiWisdomCore", "✅ 运行中", "321", "19ms"),
            ("人类学", "RenleiWisdomCore", "✅ 运行中", "210", "17ms"),
        ]
        self.engine_table.setRowCount(len(engines))
        for i, e in enumerate(engines):
            for j, val in enumerate(e):
                item = QTableWidgetItem(val)
                if j == 2:
                    item.setForeground(QBrush(QColor("green")))
                self.engine_table.setItem(i, j, item)

    def _create_claws_tab(self) -> QWidget:
        """Claw管理"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 统计行
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(QLabel("总代理: 776"))
        stats_layout.addWidget(QLabel("活跃: 150"))
        stats_layout.addWidget(QLabel("学派: 35"))
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        self.claw_table = QTableWidget()
        self.claw_table.setColumnCount(4)
        self.claw_table.setHorizontalHeaderLabels(["学派", "代理数量", "活跃数", "操作"])
        self._populate_claws_table()
        layout.addWidget(self.claw_table)

        return widget

    def _populate_claws_table(self):
        """填充Claw表格"""
        claws = [
            ("CONFUCIAN", "120", "45", "管理"),
            ("DAOIST", "98", "38", "管理"),
            ("BUDDHIST", "85", "32", "管理"),
            ("MILITARY", "72", "28", "管理"),
            ("LEGALIST", "65", "25", "管理"),
            ("ECONOMICS", "58", "22", "管理"),
            ("PSYCHOLOGY", "52", "20", "管理"),
            ("OTHER", "226", "85", "管理"),
        ]
        self.claw_table.setRowCount(len(claws))
        for i, c in enumerate(claws):
            for j, val in enumerate(c):
                self.claw_table.setItem(i, j, QTableWidgetItem(val))

    def _create_neural_tab(self) -> QWidget:
        """神经网络"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 网络信息
        info_layout = QGridLayout()
        info_layout.addWidget(QLabel("神经元: 57"), 0, 0)
        info_layout.addWidget(QLabel("突触: 74"), 0, 1)
        info_layout.addWidget(QLabel("集群: 4"), 0, 2)
        info_layout.addWidget(QLabel("当前阶段: Phase 3"), 1, 0)
        info_layout.addWidget(QLabel("活跃度: 85%"), 1, 1)
        layout.addLayout(info_layout)

        # 可视化区域
        viz = QLabel("🧠 神经网络可视化区域")
        viz.setMinimumHeight(300)
        viz.setStyleSheet("background: #1e1e1e; border: 1px solid #3e3e42; border-radius: 8px;")
        viz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        viz.setText("""
        <pre style="color: #00c853; font-family: monospace;">
        Phase 1: [████████████████] 100%
        Phase 2: [██████████████░░░] 85%
        Phase 3: [█████████░░░░░░░░░] 52%
        Phase 4: [██░░░░░░░░░░░░░░░] 12%
        Phase 5: [░░░░░░░░░░░░░░░░░] 0%
        </pre>
        """)
        layout.addWidget(viz)
        layout.addStretch()

        return widget

    def _create_logs_tab(self) -> QWidget:
        """日志查看"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("日志级别:"))
        level_combo = QComboBox()
        level_combo.addItems(["全部", "DEBUG", "INFO", "WARNING", "ERROR"])
        toolbar.addWidget(level_combo)
        toolbar.addStretch()

        clear_btn = QPushButton("清空")
        toolbar.addWidget(clear_btn)

        layout.addLayout(toolbar)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("font-family: Consolas; background: #1e1e1e;")
        self._populate_sample_logs()
        layout.addWidget(self.log_view)

        return widget

    def _populate_sample_logs(self):
        """填充示例日志"""
        logs = [
            f"[2026-04-26 00:10:15] INFO  - 系统启动完成",
            f"[2026-04-26 00:10:16] INFO  - 加载模块: src.somn",
            f"[2026-04-26 00:10:17] INFO  - 初始化智慧引擎: 45+",
            f"[2026-04-26 00:10:18] INFO  - 注册Claw代理: 776",
            f"[2026-04-26 00:10:19] INFO  - 神经网络Phase 1-5就绪",
            f"[2026-04-26 00:10:20] INFO  - API服务就绪: :8964",
        ]
        self.log_view.setText("\n".join(logs))

    def _create_config_tab(self) -> QWidget:
        """配置管理"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 配置项
        config_group = QGroupBox("系统配置")
        config_layout = QGridLayout(config_group)

        config_layout.addWidget(QLabel("LLM模型:"), 0, 0)
        config_layout.addWidget(QLineEdit("gemma4-local-b"), 0, 1)

        config_layout.addWidget(QLabel("最大并发:"), 1, 0)
        config_layout.addWidget(QLineEdit("4"), 1, 1)

        config_layout.addWidget(QLabel("延迟加载:"), 2, 0)
        lazy_combo = QComboBox()
        lazy_combo.addItems(["启用", "禁用"])
        config_layout.addWidget(lazy_combo, 2, 1)

        config_layout.addWidget(QLabel("调试模式:"), 3, 0)
        debug_combo = QComboBox()
        debug_combo.addItems(["禁用", "启用"])
        config_layout.addWidget(debug_combo, 3, 1)

        layout.addWidget(config_group)

        # 按钮
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 保存配置")
        save_btn.setStyleSheet("background: #00c853; color: white; padding: 8px;")
        reload_btn = QPushButton("🔄 重载系统")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(reload_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()
        return widget

    def _create_status_bar(self) -> QWidget:
        """状态栏"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 0)

        self.status_label = QLabel("🟢 连接正常")
        self.status_label.setStyleSheet("color: #00c853;")

        layout.addWidget(self.status_label)
        layout.addStretch()

        self.time_label = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        layout.addWidget(self.time_label)

        return widget

    def start_monitoring(self):
        """启动监控"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

    def update_status(self):
        """更新状态"""
        self.is_online = self.check_backend()
        
        if self.is_online:
            self.status_label.setText("🟢 后端在线")
            self.status_label.setStyleSheet("color: #00c853;")
            self._refresh_dashboard_data()
        else:
            self.status_label.setText("🔴 后端离线")
            self.status_label.setStyleSheet("color: #ff5252;")

        self.time_label.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _refresh_dashboard_data(self):
        """刷新仪表板数据"""
        # 从API获取真实数据
        data = self.api_client._get("/api/v1/neural/status")
        if data:
            # 更新神经网络卡片
            self.neural_count_label.setText(f"{data.get('neuron_count', 57)} 神经元")
            self.synapse_count_label.setText(f"{data.get('synapse_count', 74)} 突触")
        
        claw_data = self.api_client._get("/api/v1/claw/status")
        if claw_data:
            self.claw_active_label.setText(f"{claw_data.get('active_count', 150)} 活跃")

    def check_backend(self) -> bool:
        """检查后端是否在线"""
        import socket
        from urllib.parse import urlparse
        try:
            sock = socket.socket()
            sock.settimeout(1)
            parsed = urlparse(self.api_url)
            sock.connect((parsed.hostname, parsed.port or 80))
            sock.close()
            return True
        except (OSError, ConnectionRefusedError, TimeoutError) as e:
            logger.debug(f"后端健康检查失败: {e}")
            return False

    def refresh_all(self):
        """刷新所有"""
        self._populate_modules_table()
        self._populate_engines_table()
        self._populate_claws_table()
