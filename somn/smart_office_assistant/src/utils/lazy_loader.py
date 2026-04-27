# -*- coding: utf-8 -*-
"""
全局懒加载管理器 v1.0
=====================

提供统一的懒加载接口、加载失败降级方案、启动时间测量。

核心功能:
1. LazyLoader: 通用的懒加载装饰器/类
2. GracefulDegradation: 优雅降级处理器
3. StartupTimer: 启动时间测量
4. ModuleHealthCheck: 模块健康检查

使用方式:
    from src.utils.lazy_loader import LazyLoader, graceful_fallback, measure_startup

    # 1. 懒加载函数
    @LazyLoader.import_on_demand("heavy_module")
    def use_heavy_module():
        from heavy_module import HeavyClass
        return HeavyClass()

    # 2. 降级处理
    @graceful_fallback(default=None, error_log="加载失败，启用降级方案")
    def load_with_fallback():
        from unavailable_module import Something
        return Something()

    # 3. 启动计时
    with measure_startup("模块初始化"):
        # 初始化代码
        pass

版本: v1.0.0
日期: 2026-04-24
"""

import sys
import time
import logging
import traceback
from typing import Any, Callable, Optional, TypeVar, Dict, List
from functools import wraps
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

T = TypeVar('T')


# ═══════════════════════════════════════════════════════════════════════════════
# 启动计时器
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class StartupMetrics:
    """启动性能指标"""
    module_name: str
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    success: bool = True
    error: Optional[str] = None


class StartupTimer:
    """
    启动时间测量器
    
    用法:
        timer = StartupTimer()
        timer.start("module_a")
        # ... 代码 ...
        timer.end("module_a")
        
        timer.start("module_b")
        # ... 代码 ...
        timer.end("module_b")
        
        # 打印报告
        timer.print_report()
    """
    
    _instance: Optional['StartupTimer'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._metrics: Dict[str, StartupMetrics] = {}
            cls._instance._active: Dict[str, float] = {}
        return cls._instance
    
    def start(self, module_name: str) -> None:
        """开始计时"""
        self._active[module_name] = time.perf_counter()
        self._metrics[module_name] = StartupMetrics(
            module_name=module_name,
            start_time=time.time()
        )
    
    def end(self, module_name: str, success: bool = True, error: Optional[str] = None) -> Optional[float]:
        """结束计时，返回耗时(ms)"""
        if module_name not in self._active:
            logger.warning(f"[StartupTimer] 模块 '{module_name}' 未调用 start()")
            return None
        
        start_time = self._active.pop(module_name)
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        
        if module_name in self._metrics:
            self._metrics[module_name].end_time = time.time()
            self._metrics[module_name].duration_ms = duration_ms
            self._metrics[module_name].success = success
            self._metrics[module_name].error = error
        
        return duration_ms
    
    def get_total_time(self) -> float:
        """获取总耗时(ms)"""
        return sum(
            m.duration_ms or 0 
            for m in self._metrics.values() 
            if m.success
        )
    
    def get_metrics(self) -> Dict[str, StartupMetrics]:
        """获取所有指标"""
        return self._metrics.copy()
    
    def print_report(self) -> None:
        """打印启动时间报告"""
        print("\n" + "=" * 60)
        print("🚀 启动时间报告")
        print("=" * 60)
        
        total = 0
        sorted_metrics = sorted(
            self._metrics.items(),
            key=lambda x: x[1].duration_ms or 0,
            reverse=True
        )
        
        for name, m in sorted_metrics:
            duration = m.duration_ms or 0
            total += duration
            status = "✅" if m.success else "❌"
            error_info = f" ({m.error})" if m.error else ""
            print(f"  {status} {name:30s}: {duration:8.2f} ms{error_info}")
        
        print("-" * 60)
        print(f"  总计: {total:8.2f} ms")
        print("=" * 60)
    
    def reset(self) -> None:
        """重置计时器"""
        self._metrics.clear()
        self._active.clear()


# 上下文管理器形式的计时器
class measure_startup:
    """
    启动时间测量上下文管理器
    
    用法:
        with measure_startup("模块初始化"):
            # 初始化代码
            pass
    """
    
    def __init__(self, name: str, verbose: bool = True):
        self.name = name
        self.verbose = verbose
        self.timer = StartupTimer()
        self.duration_ms: Optional[float] = None
    
    def __enter__(self):
        self.timer.start(self.name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        error = None
        success = True
        if exc_type is not None:
            success = False
            error = f"{exc_type.__name__}: {exc_val}"
        
        self.duration_ms = self.timer.end(self.name, success, error)
        
        if self.verbose and self.duration_ms is not None:
            status = "✅" if success else "❌"
            print(f"  {status} {self.name}: {self.duration_ms:.2f} ms")


# ═══════════════════════════════════════════════════════════════════════════════
# 懒加载装饰器
# ═══════════════════════════════════════════════════════════════════════════════

class LazyLoader:
    """
    懒加载装饰器类
    
    用法:
        # 装饰器形式
        @LazyLoader.import_on_demand("heavy_module")
        def get_heavy_class():
            from heavy_module import HeavyClass
            return HeavyClass
        
        # 上下文管理器形式
        with LazyLoader("optional_module") as loader:
            if loader.loaded:
                # 使用模块
                pass
        
        # 延迟属性形式
        class MyClass:
            heavy = LazyLoader.lazy_property("heavy_module", "HeavyClass")
    """
    
    _cache: Dict[str, Any] = {}
    
    @staticmethod
    def import_on_demand(module_path: str):
        """
        装饰器: 按需导入模块
        
        用法:
            @LazyLoader.import_on_demand("my_package.heavy_module")
            def get_something():
                from my_package.heavy_module import Something
                return Something
        """
        def decorator(func: Callable[[], T]) -> Callable[[], T]:
            _cached_key = f"{module_path}:{func.__name__}"
            
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                return func(*args, **kwargs)
            
            wrapper._lazy_module = module_path
            wrapper._lazy_key = _cached_key
            return wrapper
        return decorator
    
    @staticmethod
    def lazy_property(module_path: str, class_name: str):
        """
        装饰器: 懒加载属性
        
        用法:
            class MyClass:
                HeavyModule = LazyLoader.lazy_property("heavy_module", "HeavyClass")
        """
        attr_name = class_name
        
        @property
        def lazy_prop(self):
            if attr_name not in LazyLoader._cache:
                module = __import__(module_path, fromlist=[class_name])
                LazyLoader._cache[attr_name] = getattr(module, class_name)
            return LazyLoader._cache[attr_name]
        
        return lazy_prop
    
    @staticmethod
    def get_cached(name: str, factory: Callable[[], T]) -> T:
        """
        获取缓存值，不存在则调用工厂函数
        
        用法:
            result = LazyLoader.get_cached(
                "expensive_result",
                lambda: compute_expensive_thing()
            )
        """
        if name not in LazyLoader._cache:
            LazyLoader._cache[name] = factory()
        return LazyLoader._cache[name]
    
    @staticmethod
    def clear_cache():
        """清空缓存"""
        LazyLoader._cache.clear()


class LazyImport:
    """
    延迟导入上下文管理器
    
    用法:
        with LazyImport("optional_package") as (success, module):
            if success:
                # 使用 module
                pass
            else:
                # 降级处理
                pass
    """
    
    def __init__(self, module_path: str, required: bool = False):
        self.module_path = module_path
        self.required = required
        self.success = False
        self.module: Optional[Any] = None
        self.error: Optional[str] = None
    
    def __enter__(self):
        try:
            import importlib
            self.module = importlib.import_module(self.module_path)
            self.success = True
        except ImportError as e:
            self.success = False
            self.error = "操作失败"
            if self.required:
                logger.error(f"[LazyImport] 必需模块 '{self.module_path}' 导入失败: {e}")
        except Exception as e:
            self.success = False
            self.error = f"{type(e).__name__}: {e}"
            logger.error(f"[LazyImport] 模块 '{self.module_path}' 加载异常: {e}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False  # 不抑制异常


# ═══════════════════════════════════════════════════════════════════════════════
# 优雅降级处理器
# ═══════════════════════════════════════════════════════════════════════════════

class DegradationLevel(Enum):
    """降级级别"""
    FULL = "full"           # 完全可用
    REDUCED = "reduced"     # 功能降级
    MINIMAL = "minimal"     # 最小可用
    UNAVAILABLE = "unavailable"  # 完全不可用


@dataclass
class DegradationConfig:
    """降级配置"""
    enabled: bool = True
    log_errors: bool = True
    fallback_values: Dict[str, Any] = field(default_factory=dict)
    max_retries: int = 3
    retry_delay_ms: int = 100


class GracefulDegradation:
    """
    优雅降级处理器
    
    用法:
        gd = GracefulDegradation()
        
        # 方式1: 装饰器
        @gd.handle("cache_module")
        def get_cache():
            from cache import Cache
            return Cache()
        
        # 方式2: 上下文管理器
        with gd.fallback("database", default={}) as result:
            from db import Database
            result["conn"] = Database()
        
        # 方式3: 直接调用
        value = gd.get_with_fallback(
            key="api_key",
            factory=lambda: load_api_key(),
            default="DEMO_KEY"
        )
    """
    
    def __init__(self, config: Optional[DegradationConfig] = None):
        self.config = config or DegradationConfig()
        self._status: Dict[str, DegradationLevel] = {}
        self._fallback_values: Dict[str, Any] = {}
    
    def handle(self, module_name: str, default: Any = None):
        """
        装饰器: 为函数添加降级处理
        
        用法:
            degrader = GracefulDegradation()
            
            @degrader.handle("cache")
            def get_cache():
                from cache import Cache
                return Cache()
        """
        def decorator(func: Callable[[], T]) -> Callable[[], T]:
            _fallback_key = f"{module_name}_fallback"
            
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                try:
                    result = func(*args, **kwargs)
                    self._status[module_name] = DegradationLevel.FULL
                    return result
                except Exception as e:
                    if self.config.log_errors:
                        logger.warning(
                            f"[GracefulDegradation] 模块 '{module_name}' 降级: {type(e).__name__}: {e}"
                        )
                    self._status[module_name] = DegradationLevel.REDUCED
                    
                    # 尝试使用缓存的降级值
                    if _fallback_key in self._fallback_values:
                        return self._fallback_values[_fallback_key]
                    return default
            return wrapper
        return decorator
    
    def get_with_fallback(
        self,
        key: str,
        factory: Callable[[], T],
        default: T
    ) -> T:
        """
        带降级的获取值
        
        用法:
            value = degrader.get_with_fallback(
                key="config",
                factory=lambda: load_config(),
                default=DEFAULT_CONFIG
            )
        """
        try:
            result = factory()
            self._status[key] = DegradationLevel.FULL
            return result
        except Exception as e:
            if self.config.log_errors:
                logger.warning(f"[GracefulDegradation] 获取 '{key}' 失败: {e}")
            self._status[key] = DegradationLevel.REDUCED
            return default
    
    def fallback(self, module_name: str, default: Any = None):
        """
        上下文管理器: 包装可能失败的代码
        
        用法:
            with degrader.fallback("optional_api", default={}) as ctx:
                if ctx.failed:
                    print(f"降级: {ctx.error}")
                else:
                    ctx.result = load_api()
        """
        return _FallbackContext(self, module_name, default)
    
    def get_status(self, module_name: str) -> DegradationLevel:
        """获取模块的降级状态"""
        return self._status.get(module_name, DegradationLevel.FULL)
    
    def get_all_status(self) -> Dict[str, DegradationLevel]:
        """获取所有模块的降级状态"""
        return self._status.copy()
    
    def is_healthy(self) -> bool:
        """检查是否所有模块都处于完全可用状态"""
        return all(
            status == DegradationLevel.FULL 
            for status in self._status.values()
        )
    
    def get_health_report(self) -> Dict[str, Any]:
        """获取健康报告"""
        return {
            "healthy": self.is_healthy(),
            "modules": {
                name: status.value 
                for name, status in self._status.items()
            },
            "summary": {
                "total": len(self._status),
                "full": sum(1 for s in self._status.values() if s == DegradationLevel.FULL),
                "reduced": sum(1 for s in self._status.values() if s == DegradationLevel.REDUCED),
                "minimal": sum(1 for s in self._status.values() if s == DegradationLevel.MINIMAL),
                "unavailable": sum(1 for s in self._status.values() if s == DegradationLevel.UNAVAILABLE),
            }
        }


class _FallbackContext:
    """降级上下文的内部实现"""
    
    def __init__(self, degrader: GracefulDegradation, module_name: str, default: Any):
        self.degrader = degrader
        self.module_name = module_name
        self.default = default
        self.failed = False
        self.error: Optional[str] = None
        self.result: Any = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.failed = True
            self.error = f"{exc_type.__name__}: {exc_val}"
            if self.degrader.config.log_errors:
                logger.warning(f"[GracefulDegradation] {self.module_name}: {self.error}")
            self.result = self.default
            self.degrader._status[self.module_name] = DegradationLevel.REDUCED
            return True  # 抑制异常
        else:
            self.result = self.default
            self.degrader._status[self.module_name] = DegradationLevel.FULL
            return False


# 全局降级处理器实例
_global_degrader = GracefulDegradation()


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷装饰器
# ═══════════════════════════════════════════════════════════════════════════════

def graceful_fallback(
    default: Any = None,
    error_log: Optional[str] = None,
    module_name: Optional[str] = None
):
    """
    装饰器: 为函数添加降级处理（便捷版本）
    
    用法:
        @graceful_fallback(default=None, error_log="模块加载失败")
        def load_module():
            from heavy_module import Something
            return Something()
    """
    def decorator(func: Callable[[], T]) -> Callable[[], T]:
        _name = module_name or func.__module__
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_msg = error_log or f"加载失败: {type(e).__name__}: {e}"
                logger.warning(f"[graceful_fallback] {log_msg}")
                _global_degrader._status[_name] = DegradationLevel.REDUCED
                return default
        return wrapper
    return decorator


def measure_time(name: str):
    """
    装饰器: 测量函数执行时间
    
    用法:
        @measure_time("数据处理")
        def process_data():
            # 处理逻辑
            pass
    """
    def decorator(func: Callable[[], T]) -> Callable[[], T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration_ms = (time.perf_counter() - start) * 1000
                logger.debug(f"[{name}] 执行耗时: {duration_ms:.2f} ms")
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════════════════════
# 模块健康检查
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ModuleHealth:
    """模块健康状态"""
    name: str
    loaded: bool
    load_time_ms: Optional[float] = None
    error: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)


class ModuleHealthCheck:
    """
    模块健康检查器
    
    用法:
        checker = ModuleHealthCheck()
        
        # 检查单个模块
        health = checker.check("my_module")
        print(f"状态: {health.loaded}, 耗时: {health.load_time_ms}ms")
        
        # 检查多个模块
        results = checker.check_all([
            "src.core",
            "src.intelligence", 
            "src.neural_memory"
        ])
        
        # 批量检查
        checker.batch_check()
    """
    
    def __init__(self):
        self._health_cache: Dict[str, ModuleHealth] = {}
    
    def check(self, module_path: str) -> ModuleHealth:
        """
        检查单个模块的健康状态
        
        用法:
            health = checker.check("src.intelligence")
        """
        start = time.perf_counter()
        try:
            import importlib
            importlib.import_module(module_path)
            duration_ms = (time.perf_counter() - start) * 1000
            
            health = ModuleHealth(
                name=module_path,
                loaded=True,
                load_time_ms=duration_ms
            )
            self._health_cache[module_path] = health
            return health
            
        except Exception as e:
            duration_ms = (time.perf_counter() - start) * 1000
            health = ModuleHealth(
                name=module_path,
                loaded=False,
                load_time_ms=duration_ms,
                error=f"{type(e).__name__}: {e}"
            )
            self._health_cache[module_path] = health
            return health
    
    def check_all(self, modules: List[str]) -> Dict[str, ModuleHealth]:
        """批量检查多个模块"""
        return {name: self.check(name) for name in modules}
    
    def batch_check(self, base_package: str = "src") -> Dict[str, ModuleHealth]:
        """
        批量检查包下的所有子模块
        
        用法:
            results = checker.batch_check("src")
        """
        import importlib
        import pkgutil
        
        results = {}
        try:
            base = importlib.import_module(base_package)
            base_path = base.__path__[0]
            
            for importer, modname, ispkg in pkgutil.iter_modules([base_path]):
                full_path = f"{base_package}.{modname}"
                results[full_path] = self.check(full_path)
        except Exception as e:
            logger.error(f"批量检查失败: {e}")
        
        return results
    
    def get_report(self) -> Dict[str, Any]:
        """获取健康检查报告"""
        if not self._health_cache:
            return {"status": "no_data", "modules": {}}
        
        loaded = [h for h in self._health_cache.values() if h.loaded]
        failed = [h for h in self._health_cache.values() if not h.loaded]
        
        total_time = sum(h.load_time_ms or 0 for h in loaded)
        
        return {
            "summary": {
                "total": len(self._health_cache),
                "loaded": len(loaded),
                "failed": len(failed),
                "total_load_time_ms": total_time,
                "avg_load_time_ms": total_time / len(loaded) if loaded else 0,
            },
            "modules": {
                name: {
                    "loaded": h.loaded,
                    "load_time_ms": h.load_time_ms,
                    "error": h.error
                }
                for name, h in self._health_cache.items()
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # 启动计时
    'StartupTimer',
    'StartupMetrics', 
    'measure_startup',
    
    # 懒加载
    'LazyLoader',
    'LazyImport',
    
    # 降级处理
    'GracefulDegradation',
    'DegradationLevel',
    'DegradationConfig',
    'graceful_fallback',
    
    # 健康检查
    'ModuleHealthCheck',
    'ModuleHealth',
    
    # 工具
    'measure_time',
]
