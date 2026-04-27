# -*- coding: utf-8 -*-
"""
__all__ = [
    'index_files_to_kb',
    'scan_workspace',
]

文件扫描与索引操作 - main_window 子模块
"""
import os
from pathlib import Path
from loguru import logger

# 延迟导入避免循环依赖
_imported = False
_QApplication = None
_QMessageBox = None

def _lazy_import():
    global _imported, _QApplication, _QMessageBox
    if not _imported:
        from PySide6.QtWidgets import QApplication, QMessageBox
        _QApplication = QApplication
        _QMessageBox = QMessageBox
        _imported = True

def scan_workspace(window):
    """
    扫描工作空间文件，输出到聊天显示。
    委托自 MainWindow._on_scan_files
    """
    _lazy_import()

    window.add_system_message("🔍 开始扫描文件系统...")
    window.status_bar.showMessage("扫描中...")
    window.progress_bar.setVisible(True)
    window.progress_bar.setRange(0, 0)

    try:
        files = list(window.current_workspace.rglob("*"))
        total = len(files)
        window.progress_bar.setRange(0, total)

        count = 0
        for i, f in enumerate(files):
            if f.is_file():
                count += 1
            if i % 100 == 0:
                window.progress_bar.setValue(i)
                _QApplication.instance().processEvents()

        window.progress_bar.setValue(total)
        window.progress_bar.setVisible(False)
        window.status_bar.showMessage("扫描完成")
        window._refresh_file_tree()

        window.add_system_message(
            f"✅ 扫描完成!\n"
            f"  总项目: {total}\n"
            f"  文件: {count}\n"
            f"  目录: {total - count}"
        )
    except Exception as e:
        window.progress_bar.setVisible(False)
        logger.error(f"扫描失败: {e}")
        window.add_system_message(f"❌ 扫描失败: {e}")

def index_files_to_kb(window):
    """
    将工作空间中的文本文件索引到知识库。
    委托自 MainWindow._on_index_files
    """
    _lazy_import()

    window.add_system_message("📁 开始索引文件...")
    window.status_bar.showMessage("索引中...")
    window.progress_bar.setVisible(True)
    window.progress_bar.setRange(0, 0)

    try:
        files = list(window.current_workspace.rglob("*.txt"))[:100]
        total = len(files)
        window.progress_bar.setRange(0, max(total, 1))

        for i, f in enumerate(files):
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as pf:
                    content = pf.read()[:500]
                window.knowledge_base.add_entry(
                    title=f.name,
                    content=content,
                    category="文件系统",
                    source=str(f)
                )
            except Exception:
                pass  # )失败时静默忽略
            if i % 10 == 0:
                window.progress_bar.setValue(i)
                _QApplication.instance().processEvents()

        window.progress_bar.setVisible(False)
        window._update_kb_stats()
        window._refresh_kb_list()
        window.status_bar.showMessage("索引完成")
        window.add_system_message(f"✅ 已索引 {total} 个文件到知识库")

    except Exception as e:
        window.progress_bar.setVisible(False)
        logger.error(f"索引失败: {e}")
        window.add_system_message(f"❌ 索引失败: {e}")
