"""
Somn GUI - 缓存系统

v1.0.0: 延迟导入 — CacheDB / CacheManager 首次访问时才加载，
减少启动时 sqlite3 等模块的导入开销。
"""

def __getattr__(name):
    _lazy = {
        "CacheDB": ".cache_db",
        "CacheManager": ".cache_manager",
    }
    if name in _lazy:
        import importlib
        mod = importlib.import_module(_lazy[name], __package__)
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["CacheDB", "CacheManager"]
