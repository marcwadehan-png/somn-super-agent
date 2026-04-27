# -*- coding: utf-8 -*-
"""主窗口 - 知识库模块

__all__ = [
    'create_kb_widget',
    'delete_knowledge_entry',
    'edit_knowledge_entry',
    'show_knowledge_detail',
]

处理知识库界面、搜索、条目管理
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QTextEdit, QDialog, QLabel,
    QFormLayout, QFrame
)
from PySide6.QtCore import Qt, Slot

def create_kb_widget(main_window) -> QWidget:
    """
    创建知识库界面

    Args:
        main_window: MainWindow 实例

    Returns:
        QWidget: 知识库组件
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    # 搜索栏
    search_layout = QHBoxLayout()
    main_window.kb_search = QLineEdit()
    main_window.kb_search.setPlaceholderText("搜索知识库...")
    main_window.kb_search.returnPressed.connect(main_window._on_search_kb)
    search_layout.addWidget(main_window.kb_search)

    search_btn = QPushButton("搜索")
    search_btn.clicked.connect(main_window._on_search_kb)
    search_layout.addWidget(search_btn)

    layout.addLayout(search_layout)

    # 知识条目列表
    main_window.kb_list = QListWidget()
    main_window.kb_list.itemClicked.connect(main_window._on_kb_item_selected)
    layout.addWidget(main_window.kb_list)

    # 知识详情
    main_window.kb_detail = QTextEdit()
    main_window.kb_detail.setReadOnly(True)
    main_window.kb_detail.setMaximumHeight(200)
    layout.addWidget(main_window.kb_detail)

    return widget

def show_knowledge_detail(main_window, entry_id: str):
    """显示知识详情对话框"""
    # 获取知识条目
    entry = main_window.knowledge_base.get_entry(entry_id)
    if not entry:
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.warning(main_window, "错误", "找不到该知识条目")
        return

    # 创建详情对话框
    dialog = QDialog(main_window)
    dialog.setWindowTitle(f"知识详情 - {entry.title}")
    dialog.setMinimumSize(700, 500)

    layout = QVBoxLayout(dialog)

    # 标题
    title_label = QLabel(f"<h2>{entry.title}</h2>")
    title_label.setTextFormat(Qt.RichText)
    layout.addWidget(title_label)

    # 元信息
    meta_info = f"""
    <b>类别:</b> {entry.category} |
    <b>来源:</b> {entry.source or '未知'} |
    <b>创建时间:</b> {entry.created_at[:19] if entry.created_at else '未知'}
    """
    meta_label = QLabel(meta_info)
    meta_label.setTextFormat(Qt.RichText)
    layout.addWidget(meta_label)

    # 分隔线
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("background-color: #ccc;")
    layout.addWidget(line)

    # 内容
    content_edit = QTextEdit()
    content_edit.setPlainText(entry.content)
    content_edit.setReadOnly(True)
    layout.addWidget(content_edit)

    # 按钮区域
    button_layout = QHBoxLayout()

    # 编辑按钮
    edit_btn = QPushButton("编辑")
    edit_btn.clicked.connect(lambda: edit_knowledge_entry(main_window, entry_id, dialog))
    button_layout.addWidget(edit_btn)

    # 删除按钮
    delete_btn = QPushButton("删除")
    delete_btn.setStyleSheet("color: red;")
    delete_btn.clicked.connect(lambda: delete_knowledge_entry(main_window, entry_id, dialog))
    button_layout.addWidget(delete_btn)

    button_layout.addStretch()

    # 关闭按钮
    close_btn = QPushButton("关闭")
    close_btn.clicked.connect(dialog.accept)
    button_layout.addWidget(close_btn)

    layout.addLayout(button_layout)

    dialog.exec()

def edit_knowledge_entry(main_window, entry_id: str, parent_dialog: QDialog):
    """编辑知识条目"""
    from PySide6.QtWidgets import QDialogButtonBox, QMessageBox

    entry = main_window.knowledge_base.get_entry(entry_id)
    if not entry:
        return

    # 创建编辑对话框
    dialog = QDialog(main_window)
    dialog.setWindowTitle(f"编辑知识 - {entry.title}")
    dialog.setMinimumSize(600, 400)

    layout = QVBoxLayout(dialog)

    # 表单
    form_layout = QFormLayout()

    title_input = QLineEdit(entry.title)
    form_layout.addRow("标题:", title_input)

    category_input = QLineEdit(entry.category)
    form_layout.addRow("类别:", category_input)

    source_input = QLineEdit(entry.source or "")
    form_layout.addRow("来源:", source_input)

    layout.addLayout(form_layout)

    # 内容编辑
    layout.addWidget(QLabel("内容:"))
    content_edit = QTextEdit()
    content_edit.setPlainText(entry.content)
    layout.addWidget(content_edit)

    # 按钮
    button_box = QDialogButtonBox(
        QDialogButtonBox.Save | QDialogButtonBox.Cancel
    )
    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)
    layout.addWidget(button_box)

    if dialog.exec() == QDialog.Accepted:
        # 更新知识条目
        main_window.knowledge_base.update_entry(
            entry_id,
            title=title_input.text(),
            category=category_input.text(),
            source=source_input.text(),
            content=content_edit.toPlainText()
        )

        # 刷新列表
        main_window._refresh_kb_list()

        # 关闭父对话框
        parent_dialog.accept()

        # 重新打开详情
        show_knowledge_detail(main_window, entry_id)

        main_window.status_bar.showMessage(f"已更新知识条目: {entry_id}")

def delete_knowledge_entry(main_window, entry_id: str, dialog: QDialog):
    """删除知识条目"""
    from PySide6.QtWidgets import QMessageBox

    reply = QMessageBox.question(
        main_window,
        "确认删除",
        "确定要删除这条知识条目吗？此操作不可撤销。",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        if main_window.knowledge_base.delete_entry(entry_id):
            main_window._refresh_kb_list()
            dialog.accept()
            main_window.status_bar.showMessage(f"已删除知识条目: {entry_id}")
        else:
            QMessageBox.warning(main_window, "错误", "删除失败")
