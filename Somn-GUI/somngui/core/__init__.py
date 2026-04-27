"""
Somn GUI - 核心模块

v1.0.0: 延迟导入 — AppState / ConnectionStatus 首次访问时才加载，
避免 import somngui.core 时触发 state.py 的整条导入链
（state.py → SomnAPIClient → CacheManager → ChatHistoryDB → sqlite3）。
GUIConfig / BackendConnection 保留即时导入（轻量，启动必用）。
"""
from .config import GUIConfig
from .connection import BackendConnection


def __getattr__(name):
    """延迟导入 AppState / ConnectionStatus — 仅在首次访问时加载"""
    _lazy = {
        "AppState": ".state",
        "ConnectionStatus": ".state",
    }
    if name in _lazy:
        import importlib
        mod = importlib.import_module(_lazy[name], __package__)
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["GUIConfig", "BackendConnection", "AppState", "ConnectionStatus"]
