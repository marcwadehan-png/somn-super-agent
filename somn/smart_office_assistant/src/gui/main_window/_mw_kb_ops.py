# -*- coding: utf-8 -*-
"""
__all__ = [
    'on_kb_item_selected',
    'refresh_kb_list',
    'search_knowledge',
    'show_kb_stats',
]

知识库操作 - main_window 子模块
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QMessageBox

# 延迟导入避免循环依赖
_imported = False
_QApplication = None

def _lazy_import():
    global _imported, _QApplication
    if not _imported:
        from PySide6.QtWidgets import QApplication
        _QApplication = QApplication
        _imported = True

def search_knowledge(window):
    """
    搜索知识库，委托自 MainWindow._on_search_kb
    """
    query = window.kb_search.text().strip()
    if not query:
        return

    results = window.knowledge_base.search(query)
    window.kb_list.clear()

    if not results:
        window.kb_detail.setPlainText("未找到相关知识条目")
        return

    for entry in results:
        item = QListWidgetItem(entry.get("title", "无标题"))
        item.setData(Qt.UserRole, entry.get("id", ""))
        window.kb_list.addItem(item)

    if results:
        first = results[0]
        window.kb_detail.setPlainText(
            f"标题: {first.get('title', '无标题')}\n\n"
            f"类别: {first.get('category', '未知')}\n\n"
            f"内容预览:\n{first.get('content', '')[:200]}..."
        )

def on_kb_item_selected(window, item: QListWidgetItem):
    """
    选择知识库条目，委托自 MainWindow._on_kb_item_selected
    """
    entry_id = item.data(Qt.UserRole)
    if entry_id:
        window._show_knowledge_detail(entry_id)

def refresh_kb_list(window):
    """
    刷新知识库列表，委托自 MainWindow._refresh_kb_list
    """
    entries = window.knowledge_base.get_all_entries()
    window.kb_list.clear()
    for entry in entries:
        item = QListWidgetItem(entry.get("title", "无标题"))
        item.setData(Qt.UserRole, entry.get("id", ""))
        window.kb_list.addItem(item)

def show_kb_stats(window):
    """
    显示知识库统计，委托自 MainWindow._on_kb_stats
    """
    stats = window.knowledge_base.get_stats()
    QMessageBox.information(
        window, "知识库统计",
        f"📚 知识库统计\n\n"
        f"总条目: {stats['knowledge_entries']}\n"
        f"概念数: {stats['concepts']}\n"
        f"索引文件: {stats['indexed_files']}"
    )
