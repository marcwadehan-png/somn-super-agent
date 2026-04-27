# -*- coding: utf-8 -*-
"""系统资源监控面板 [v1.0 新增]"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from PyQt6.QtCore import QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QProgressBar, QFrame,
    QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDoubleSpinBox,
    QFormLayout, QSlider,
)

# v1.0.0: AppState 延迟导入 — 避免启动时触发 httpx/sqlite3 导入链
if TYPE_CHECKING:
    from somngui.core.state import AppState


# ═══════════════════════════════════════════════════════
# 系统资源监控面板
# ═══════════════════════════════════════════════════════

class _SystemResourcePanelBase(QWidget):
    """
    系统资源监控面板 [v1.0]
    
    功能：
    - 显示 CPU、内存、磁盘使用情况
    - 显示资源告警状态
    - 支持手动刷新
    - 支持修改资源阈值
    """

    def __init__(self, app_state: "AppState", parent=None):  # v1.0.0: 字符串注解避免运行时导入
        super().__init__(parent)
        self._state = app_state
        self._init_ui()
        
        # 定时器：自动刷新（每10秒）
        self._timer = QTimer()
        self._timer.timeout.connect(self.refresh)
        self._timer.start(10000)  # 10秒
        
        # 立即刷新一次
        self.refresh()

    # ── UI 初始化 ──────────────────────────────────────────

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 标题
        title = QLabel("⚡ 系统资源监控")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding-bottom: 10px;
            }
        """)
        layout.addWidget(title)

        # 资源概览卡片
        layout.addWidget(self._create_overview_cards())

        # 详细信息组
        layout.addWidget(self._create_detail_group())

        # 阈值设置组
        layout.addWidget(self._create_threshold_group())

        # 按钮行
        layout.addWidget(self._create_button_row())

        layout.addStretch(1)

    def _create_overview_cards(self) -> QWidget:
        """创建资源概览卡片"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # CPU 卡片
        self._cpu_card = self._create_metric_card("CPU", "0%", "#3498db")
        layout.addWidget(self._cpu_card)

        # 内存卡片
        self._mem_card = self._create_metric_card("内存", "0%", "#2ecc71")
        layout.addWidget(self._mem_card)

        # 磁盘卡片
        self._disk_card = self._create_metric_card("磁盘", "0%", "#e74c3c")
        layout.addWidget(self._disk_card)

        # 告警状态卡片
        self._warning_card = self._create_metric_card("告警", "正常", "#95a5a6")
        layout.addWidget(self._warning_card)

        return widget

    def _create_metric_card(self, title: str, value: str, color: str) -> QFrame:
        """创建指标卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }}
            QFrame:hover {{
                border: 2px solid {color};
            }}
        """)
        card.setFixedHeight(100)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(title_label)

        # 值
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(value_label)
        layout.addStretch(1)

        # 保存值标签的引用
        if title == "CPU":
            self._cpu_value = value_label
        elif title == "内存":
            self._mem_value = value_label
        elif title == "磁盘":
            self._disk_value = value_label
        elif title == "告警":
            self._warning_value = value_label

        return card

    def _create_detail_group(self) -> QGroupBox:
        """创建详细信息组"""
        group = QGroupBox("📊 详细信息")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding-top: 10px;
            }
        """)

        layout = QFormLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # CPU 详情
        self._cpu_detail = QLabel("--")
        layout.addRow("CPU 使用率：", self._cpu_detail)

        # 内存详情
        self._mem_detail = QLabel("--")
        layout.addRow("内存使用：", self._mem_detail)

        # 内存可用
        self._mem_avail = QLabel("--")
        layout.addRow("内存可用：", self._mem_avail)

        # 磁盘详情
        self._disk_detail = QLabel("--")
        layout.addRow("磁盘使用：", self._disk_detail)

        # 进程内存
        self._process_mem = QLabel("--")
        layout.addRow("进程内存：", self._process_mem)

        # 进程 CPU
        self._process_cpu = QLabel("--")
        layout.addRow("进程 CPU：", self._process_cpu)

        # 线程数
        self._thread_count = QLabel("--")
        layout.addRow("线程数：", self._thread_count)

        return group

    def _create_threshold_group(self) -> QGroupBox:
        """创建阈值设置组"""
        group = QGroupBox("⚙️ 阈值设置")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding-top: 10px;
            }
        """)

        layout = QFormLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # CPU 阈值
        self._cpu_threshold = QDoubleSpinBox()
        self._cpu_threshold.setRange(0.0, 100.0)
        self._cpu_threshold.setValue(80.0)
        self._cpu_threshold.setSuffix("%")
        layout.addRow("CPU 告警阈值：", self._cpu_threshold)

        # 内存阈值
        self._mem_threshold = QDoubleSpinBox()
        self._mem_threshold.setRange(0.0, 100.0)
        self._mem_threshold.setValue(85.0)
        self._mem_threshold.setSuffix("%")
        layout.addRow("内存告警阈值：", self._mem_threshold)

        # 磁盘阈值
        self._disk_threshold = QDoubleSpinBox()
        self._disk_threshold.setRange(0.0, 100.0)
        self._disk_threshold.setValue(90.0)
        self._disk_threshold.setSuffix("%")
        layout.addRow("磁盘告警阈值：", self._disk_threshold)

        # 可用内存阈值
        self._mem_avail_threshold = QDoubleSpinBox()
        self._mem_avail_threshold.setRange(0.0, 10000.0)
        self._mem_avail_threshold.setValue(500.0)
        self._mem_avail_threshold.setSuffix(" MB")
        layout.addRow("可用内存告警阈值：", self._mem_avail_threshold)

        # 保存按钮
        save_btn = QPushButton("保存阈值")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        save_btn.clicked.connect(self._save_thresholds)
        layout.addRow("", save_btn)

        return group

    def _create_button_row(self) -> QWidget:
        """创建按钮行"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #27ae60;
            }
        """)
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)

        # 自动刷新开关
        self._auto_refresh_btn = QPushButton("⏸️ 暂停自动刷新")
        self._auto_refresh_btn.setCheckable(True)
        self._auto_refresh_btn.setChecked(True)
        self._auto_refresh_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:checked {
                background: #3498db;
            }
            QPushButton:!checked {
                background: #95a5a6;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        self._auto_refresh_btn.clicked.connect(self._toggle_auto_refresh)
        layout.addWidget(self._auto_refresh_btn)

        layout.addStretch(1)

        return widget

    # ── 数据刷新 ──────────────────────────────────────────

    @pyqtSlot()
    def refresh(self):
        """刷新系统资源数据"""
        try:
            # 调用后端API
            response = self._state.get_backend()
            if not response:
                self._show_error("未连接到后端")
                return

            # 发送请求
            from somngui.core.connection import get_connection
            conn = get_connection()
            result = conn.get("/api/v1/system/resources")
            
            if not result or not result.get("success"):
                self._show_error(result.get("error", "获取系统资源失败"))
                return

            data = result.get("data", {})
            self._update_ui(data)

        except Exception as e:
            self._show_error(f"刷新失败: {e}")

    def _update_ui(self, data: Dict):
        """更新UI显示"""
        # 更新 CPU
        cpu_percent = data.get("cpu_percent", 0.0)
        self._cpu_value.setText(f"{cpu_percent:.1f}%")
        self._cpu_detail.setText(f"{cpu_percent:.1f}%")

        # 更新内存
        mem_percent = data.get("memory_percent", 0.0)
        self._mem_value.setText(f"{mem_percent:.1f}%")
        self._mem_detail.setText(f"{mem_percent:.1f}%")

        mem_avail = data.get("memory_available_mb", 0.0)
        self._mem_avail.setText(f"{mem_avail:.1f} MB")

        # 更新磁盘
        disk_percent = data.get("disk_percent", 0.0)
        self._disk_value.setText(f"{disk_percent:.1f}%")
        self._disk_detail.setText(f"{disk_percent:.1f}%")

        # 更新进程信息
        process = data.get("process", {})
        if process:
            proc_mem = process.get("memory_mb", 0.0)
            self._process_mem.setText(f"{proc_mem:.1f} MB")

            proc_cpu = process.get("cpu_percent", 0.0)
            self._process_cpu.setText(f"{proc_cpu:.1f}%")

            thread_count = process.get("threads", 0)
            self._thread_count.setText(str(thread_count))

        # 更新告警状态
        warning = data.get("warning", False)
        warning_msg = data.get("warning_message", "")
        
        if warning:
            self._warning_value.setText("⚠️ 告警")
            self._warning_value.setStyleSheet("""
                QLabel {
                    font-size: 28px;
                    font-weight: bold;
                    color: #e74c3c;
                }
            """)
            
            # 显示告警消息
            if warning_msg:
                QMessageBox.warning(self, "系统资源告警", warning_msg)
        else:
            self._warning_value.setText("✅ 正常")
            self._warning_value.setStyleSheet("""
                QLabel {
                    font-size: 28px;
                    font-weight: bold;
                    color: #2ecc71;
                }
            """)

    def _show_error(self, message: str):
        """显示错误信息"""
        self._warning_value.setText("❌ 错误")
        self._warning_value.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #e74c3c;
            }
        """)

    # ── 阈值设置 ──────────────────────────────────────────

    @pyqtSlot()
    def _save_thresholds(self):
        """保存阈值设置"""
        try:
            thresholds = {
                "cpu_percent": self._cpu_threshold.value(),
                "memory_percent": self._mem_threshold.value(),
                "disk_percent": self._disk_threshold.value(),
                "memory_available_mb": self._mem_avail_threshold.value(),
            }

            # 调用后端API
            from somngui.core.connection import get_connection
            conn = get_connection()
            result = conn.post("/api/v1/system/resources/thresholds", json=thresholds)

            if result and result.get("success"):
                QMessageBox.information(self, "成功", "阈值已保存")
            else:
                QMessageBox.warning(
                    self, "失败",
                    result.get("error", "保存阈值失败")
                )

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存阈值失败: {e}")

    # ── 自动刷新 ──────────────────────────────────────────

    @pyqtSlot(bool)
    def _toggle_auto_refresh(self, checked: bool):
        """切换自动刷新"""
        if checked:
            self._auto_refresh_btn.setText("⏸️ 暂停自动刷新")
            self._timer.start(10000)
        else:
            self._auto_refresh_btn.setText("▶️ 恢复自动刷新")
            self._timer.stop()
