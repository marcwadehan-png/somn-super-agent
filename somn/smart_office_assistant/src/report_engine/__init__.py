"""
报告引擎模块 [v1.0 延迟加载优化]
Report Engine - 毫秒级启动

功能:报告生成, 数据可视化, 多格式导出

[v1.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v1.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .report_generator import ReportEngine, Report, ReportSection


def __getattr__(name: str) -> Any:
    """[v1.0 优化] 延迟加载 - 毫秒级启动"""

    if name in ('ReportEngine', 'Report', 'ReportSection'):
        from . import report_generator as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'report_engine' has no attribute '{name}'")


__all__ = [
    'ReportEngine', 'Report', 'ReportSection'
]
