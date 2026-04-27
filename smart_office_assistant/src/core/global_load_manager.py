"""
全局懒加载 + 预加载管理器
实现最快、最高效的启动加载策略
"""
import sys
import time
import threading
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
from loguru import logger
from functools import wraps

class LoadPriority(Enum):
    """加载优先级"""
    CRITICAL = 0    # 启动时必须加载
    HIGH = 1         # 高优先级，预加载
    NORMAL = 2       # 正常优先级，懒加载
    LOW = 3          # 低优先级，按需加载
    BACKGROUND = 4   # 后台加载

class LoadStrategy(Enum):
    """加载策略"""
    EAGER = "eager"          # 立即加载
    LAZY = "lazy"            # 懒加载（首次访问时）
    PRELOAD = "preload"      # 预加载（后台线程）
    ON_DEMAND = "on_demand"  # 按需加载

class GlobalLoadManager:
    """
    全局加载管理器
    - 统一管理系统所有模块的加载
    - 支持懒加载、预加载、并行初始化
    - 智能缓存，避免重复初始化
    """
    
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        # 模块注册表: {name: module_info}
        self._registry: Dict[str, Dict] = {}
        
        # 已加载的模块实例缓存
        self._cache: Dict[str, Any] = {}
        
        # 加载状态追踪
        self._load_status: Dict[str, str] = {}  # 'pending', 'loading', 'loaded', 'failed'
        
        # 依赖图: {name: [依赖列表]}
        self._dependencies: Dict[str, List[str]] = {}
        
        # 预加载线程
        self._preload_thread: Optional[threading.Thread] = None
        self._preload_enabled = True
        
        # 性能统计
        self._load_times: Dict[str, float] = {}
        
        logger.info("[GlobalLoadManager] 初始化完成")
    
    def register(self, 
                 name: str, 
                 factory: Callable,
                 strategy: LoadStrategy = LoadStrategy.LAZY,
                 priority: LoadPriority = LoadPriority.NORMAL,
                 dependencies: List[str] = None,
                 ttl: int = 3600):
        """
        注册一个可加载模块
        
        Args:
            name: 模块名称
            factory: 工厂函数，用于创建模块实例
            strategy: 加载策略
            priority: 加载优先级
            dependencies: 依赖的其他模块
            ttl: 缓存有效期（秒）
        """
        self._registry[name] = {
            'factory': factory,
            'strategy': strategy,
            'priority': priority,
            'dependencies': dependencies or [],
            'ttl': ttl,
            'loaded_at': None,
        }
        self._dependencies[name] = dependencies or []
        logger.debug(f"[GlobalLoadManager] 注册模块: {name}, 策略: {strategy.value}")
    
    def get(self, name: str) -> Any:
        """
        获取模块实例（按需加载）
        
        Returns:
            模块实例
        """
        # 检查缓存
        if name in self._cache:
            return self._cache[name]
        
        # 检查注册表
        if name not in self._registry:
            raise ValueError(f"模块未注册: {name}")
        
        # 加载模块
        return self._load_module(name)
    
    def _load_module(self, name: str) -> Any:
        """加载指定模块"""
        if self._load_status.get(name) == 'loading':
            # 防止递归加载
            raise RuntimeError(f"循环依赖检测: {name}")
        
        self._load_status[name] = 'loading'
        module_info = self._registry[name]
        
        # 先加载依赖
        for dep in module_info['dependencies']:
            if dep not in self._cache:
                self._load_module(dep)
        
        # 加载当前模块
        t0 = time.time()
        try:
            instance = module_info['factory']()
            t1 = time.time()
            elapsed = (t1 - t0) * 1000
            
            self._cache[name] = instance
            self._load_times[name] = elapsed
            self._load_status[name] = 'loaded'
            module_info['loaded_at'] = time.time()
            
            logger.info(f"[GlobalLoadManager] 模块加载完成: {name}, 耗时: {elapsed:.1f}ms")
            return instance
        except Exception as e:
            self._load_status[name] = 'failed'
            logger.error(f"[GlobalLoadManager] 模块加载失败: {name}, 错误: {e}")
            raise
    
    def preload_all(self, max_priority: LoadPriority = LoadPriority.NORMAL):
        """
        预加载所有优先级 >= max_priority 的模块
        
        Args:
            max_priority: 最大预加载优先级
        """
        if not self._preload_enabled:
            return
        
        def _preload_worker():
            """后台预加载工作线程"""
            # 按优先级排序
            modules_to_preload = [
                (name, info) for name, info in self._registry.items()
                if info['strategy'] in [LoadStrategy.PRELOAD, LoadStrategy.EAGER]
                and info['priority'].value <= max_priority.value
                and name not in self._cache
            ]
            modules_to_preload.sort(key=lambda x: x[1]['priority'].value)
            
            for name, info in modules_to_preload:
                if name in self._cache:
                    continue
                try:
                    self._load_module(name)
                except Exception as e:
                    logger.warning(f"[GlobalLoadManager] 预加载失败: {name}, 错误: {e}")
        
        self._preload_thread = threading.Thread(target=_preload_worker, daemon=True)
        self._preload_thread.start()
        logger.info("[GlobalLoadManager] 后台预加载已启动")
    
    def preload_now(self, names: List[str]):
        """立即预加载指定模块（同步）"""
        for name in names:
            if name not in self._cache:
                try:
                    self._load_module(name)
                except Exception as e:
                    logger.warning(f"[GlobalLoadManager] 预加载失败: {name}, 错误: {e}")
    
    def parallel_preload(self, names: List[str]):
        """
        并行预加载多个模块（利用线程池）
        注意：只有无依赖或依赖已满足的模块才能并行
        """
        import concurrent.futures
        
        def _load_wrapper(name):
            if name in self._cache:
                return name, self._cache[name]
            return name, self._load_module(name)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(_load_wrapper, name): name for name in names}
            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.warning(f"[GlobalLoadManager] 并行预加载失败: {name}, 错误: {e}")
    
    def get_stats(self) -> Dict:
        """获取加载统计信息"""
        return {
            'registered': len(self._registry),
            'loaded': len(self._cache),
            'load_times': self._load_times,
            'status': self._load_status,
        }
    
    def clear_cache(self):
        """清空缓存（用于测试）"""
        self._cache.clear()
        self._load_status.clear()
        self._load_times.clear()

# 全局实例
_global_load_manager = None

def get_global_load_manager() -> GlobalLoadManager:
    """获取全局加载管理器实例"""
    global _global_load_manager
    if _global_load_manager is None:
        _global_load_manager = GlobalLoadManager()
    return _global_load_manager

def lazy_load(name: str, priority: LoadPriority = LoadPriority.NORMAL):
    """
    装饰器：将类或函数标记为懒加载
    
    Usage:
        @lazy_load('my_module', LoadPriority.HIGH)
        def create_my_module():
            return MyModule()
    """
    def decorator(factory_func):
        mgr = get_global_load_manager()
        mgr.register(name, factory_func, LoadStrategy.LAZY, priority)
        
        @wraps(factory_func)
        def wrapper(*args, **kwargs):
            return mgr.get(name)
        return wrapper
    return decorator

def preloadable(name: str, priority: LoadPriority = LoadPriority.HIGH):
    """
    装饰器：将类或函数标记为可预加载
    """
    def decorator(factory_func):
        mgr = get_global_load_manager()
        mgr.register(name, factory_func, LoadStrategy.PRELOAD, priority)
        return factory_func
    return decorator
