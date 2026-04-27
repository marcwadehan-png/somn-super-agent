"""
Utility modules [v1.0 懒加载优化]

包含:
- FileManager: 文件管理器
- ConfigManager: 配置管理器
- lazy_loader: 全局懒加载框架

使用方式:
    from src.utils import FileManager, ConfigManager
    from src.utils.lazy_loader import measure_startup, GracefulDegradation

版本: v1.0.0
日期: 2026-04-24
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .file_manager import FileManager, get_file_manager
    from .config_manager import ConfigManager, get_config
    from .lazy_loader import (
        StartupTimer, LazyLoader, GracefulDegradation, 
        ModuleHealthCheck, measure_startup, graceful_fallback
    )


def __getattr__(name: str) -> Any:
    """懒加载 - 毫秒级启动"""
    
    # 文件管理
    if name in ('FileManager', 'get_file_manager'):
        from . import file_manager
        return getattr(file_manager, name)
    
    # 配置管理
    elif name in ('ConfigManager', 'get_config'):
        from . import config_manager
        return getattr(config_manager, name)
    
    # 懒加载框架 (按需加载)
    elif name in ('StartupTimer', 'LazyLoader', 'GracefulDegradation', 
                  'ModuleHealthCheck', 'measure_startup', 'graceful_fallback'):
        from . import lazy_loader
        return getattr(lazy_loader, name)
    
    raise AttributeError(f"module 'utils' has no attribute '{name}'")


__all__ = [
    # 文件管理
    'FileManager',
    'get_file_manager',
    
    # 配置管理
    'ConfigManager',
    'get_config',
    
    # 懒加载框架
    'StartupTimer',
    'LazyLoader',
    'GracefulDegradation',
    'ModuleHealthCheck',
    'measure_startup',
    'graceful_fallback',
]
