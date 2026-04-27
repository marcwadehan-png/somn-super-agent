# -*- coding: utf-8 -*-
"""主窗口 - 对话模块

__all__ = [
    'add_agent_message',
    'add_system_message',
    'add_user_message',
    'create_chat_widget',
]

处理对话界面、消息显示、快捷指令等
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Qt, Slot

def create_chat_widget(main_window) -> QWidget:
    """
    创建对话界面组件

    Args:
        main_window: MainWindow 实例

    Returns:
        QWidget: 对话界面组件
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    # 对话历史显示区
    main_window.chat_display = QTextEdit()
    main_window.chat_display.setReadOnly(True)
    main_window.chat_display.setStyleSheet("""
        QTextEdit {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 10px;
        }
    """)
    layout.addWidget(main_window.chat_display)

    # 输入区域
    input_layout = QHBoxLayout()

    main_window.chat_input = QLineEdit()
    main_window.chat_input.setPlaceholderText("输入您的问题或指令...")
    main_window.chat_input.returnPressed.connect(main_window._on_send_message)
    main_window.chat_input.setStyleSheet("""
        QLineEdit {
            padding: 10px;
            border: 2px solid #dee2e6;
            border-radius: 20px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #007bff;
        }
    """)
    input_layout.addWidget(main_window.chat_input)

    send_btn = QPushButton("发送")
    send_btn.setFixedWidth(80)
    send_btn.clicked.connect(main_window._on_send_message)
    send_btn.setStyleSheet("""
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
    """)
    input_layout.addWidget(send_btn)

    # 表情包上传按钮
    main_window.sticker_upload_btn = QPushButton("📷 上传表情")
    main_window.sticker_upload_btn.setFixedWidth(100)
    main_window.sticker_upload_btn.clicked.connect(main_window._on_upload_sticker)
    main_window.sticker_upload_btn.setStyleSheet("""
        QPushButton {
            background-color: #f0f0f0;
            color: #333;
            border: 1px solid #ccc;
            border-radius: 15px;
            padding: 8px 12px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
    """)
    input_layout.addWidget(main_window.sticker_upload_btn)

    layout.addLayout(input_layout)

    # 快捷指令按钮
    quick_cmds_layout = QHBoxLayout()
    quick_cmds = [
        "总结文档", "生成报告", "分析数据", "创建大纲",
        "扫描文件", "制定策略", "预测效果"
    ]
    for cmd in quick_cmds:
        btn = QPushButton(cmd)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #e9ecef;
                border: 1px solid #ced4da;
                border-radius: 15px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #dee2e6;
            }
        """)
        btn.clicked.connect(lambda checked, c=cmd: main_window._on_quick_command(c))
        quick_cmds_layout.addWidget(btn)
    quick_cmds_layout.addStretch()
    layout.addLayout(quick_cmds_layout)

    return widget

def add_user_message(main_window, message: str):
    """添加用户消息到对话"""
    html = f"""
    <div style="margin: 10px 0; text-align: right;">
        <div style="display: inline-block; background-color: #007bff; color: white;
                    padding: 10px 15px; border-radius: 15px; max-width: 80%;">
            <b>你:</b> {message}
        </div>
    </div>
    """
    main_window.chat_display.append(html)

def add_agent_message(main_window, message: str):
    """添加智能体消息到对话"""
    html = f"""
    <div style="margin: 10px 0;">
        <div style="display: inline-block; background-color: #e9ecef;
                    padding: 10px 15px; border-radius: 15px; max-width: 80%;">
            <b>🤖 AI:</b> {message.replace('\n', '<br>')}
        </div>
    </div>
    """
    main_window.chat_display.append(html)

def add_system_message(main_window, message: str):
    """添加系统消息"""
    html = f"""
    <div style="margin: 10px 0; text-align: center;">
        <div style="display: inline-block; background-color: #f8f9fa; color: #6c757d;
                    padding: 10px 15px; border-radius: 10px; font-size: 12px;">
            {message.replace('\n', '<br>')}
        </div>
    </div>
    """
    main_window.chat_display.append(html)
