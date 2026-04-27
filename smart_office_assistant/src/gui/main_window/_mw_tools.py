# -*- coding: utf-8 -*-
"""
__all__ = [
    'create_strategy',
    'generate_report',
]

工具类操作 - 报告生成与策略制定
"""
from loguru import logger

def generate_report(window):
    """委托自 MainWindow._on_generate_report"""
    window.add_system_message("📊 正在生成报告，请稍候...")
    try:
        from src.intelligence.report_generator import generate_report as gen_report
        report = gen_report(window.current_workspace)
        window.doc_title_input.setText("分析报告")
        window.editor.setPlainText(report)
        window.tab_widget.setCurrentIndex(1)
        window.add_system_message("✅ 报告已生成！")
    except ImportError:
        window.add_system_message("⚠️ 报告生成模块暂不可用")
    except Exception as e:
        logger.error(f"报告生成失败: {e}")
        window.add_system_message(f"❌ 报告生成失败: {e}")

def create_strategy(window):
    """委托自 MainWindow._on_create_strategy"""
    window.add_system_message("🎯 正在制定策略，请稍候...")
    try:
        from src.intelligence.strategy_engine import create_strategy as mk_strategy
        strategy = mk_strategy(window.current_workspace)
        window.doc_title_input.setText("执行策略")
        window.editor.setPlainText(strategy)
        window.tab_widget.setCurrentIndex(1)
        window.add_system_message("✅ 策略已生成！")
    except ImportError:
        window.add_system_message("⚠️ 策略生成模块暂不可用")
    except Exception as e:
        logger.error(f"策略生成失败: {e}")
        window.add_system_message(f"❌ 策略生成失败: {e}")
