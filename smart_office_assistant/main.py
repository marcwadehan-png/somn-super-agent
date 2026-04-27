#!/usr/bin/env python3
"""
Somn - 汇千古之智，向未知而生
主入口文件（GUI模式，依赖PySide6）
"""

import sys
import os
from pathlib import Path

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

from loguru import logger


def setup_logging():
    """配置日志"""
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置 loguru
    logger.add(
        log_dir / "smartoffice_{time}.log",
        rotation="10 MB",
        retention="30 days",
        encoding="utf-8",
        level="INFO"
    )
    
    # 控制台输出
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )


def main():
    """主函数 — GUI入口，需要 PySide6"""
    if not _PYSIDE6_AVAILABLE:
        print("Error: PySide6 未安装，无法启动GUI。")
        print("  安装命令: pip install PySide6")
        print("  CLI入口: python -m smart_office_assistant.src")
        sys.exit(1)

    from src.gui.main_window import MainWindow

    # 配置日志
    setup_logging()
    logger.info("=" * 50)
    logger.info("SmartOffice AI 启动中...")
    logger.info("=" * 50)
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("SmartOffice AI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SmartOffice")
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 设置全局字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    # 设置高DPI支持
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    logger.info("主窗口已显示")
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
