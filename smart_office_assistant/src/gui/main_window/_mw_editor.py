# -*- coding: utf-8 -*-
"""主窗口 - 编辑器模块

__all__ = [
    'create_editor_widget',
]

处理文档编辑器界面
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel

def create_editor_widget(main_window) -> QWidget:
    """
    创建文档编辑器界面

    Args:
        main_window: MainWindow 实例

    Returns:
        QWidget: 编辑器组件
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    # 工具栏
    toolbar = QHBoxLayout()

    toolbar.addWidget(QLabel("文档标题:"))
    main_window.doc_title_input = QLineEdit()
    main_window.doc_title_input.setPlaceholderText("输入文档标题...")
    toolbar.addWidget(main_window.doc_title_input)

    save_btn = QPushButton("保存")
    save_btn.clicked.connect(main_window._on_save_document)
    toolbar.addWidget(save_btn)

    export_btn = QPushButton("导出")
    export_btn.clicked.connect(main_window._on_export_document)
    toolbar.addWidget(export_btn)

    layout.addLayout(toolbar)

    # 编辑器
    main_window.editor = QTextEdit()
    main_window.editor.setPlaceholderText("在此编辑文档内容...")
    layout.addWidget(main_window.editor)

    return widget
