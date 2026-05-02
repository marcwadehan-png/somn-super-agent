# -*- coding: utf-8 -*-
"""
NeuralMemory 快速加载模块 v1.0
neural_memory_fast_load.py

设计目标：预加载+懒加载的快速加载模式

架构策略：
┌─────────────────────────────────────────────────────────────────────┐
│                        NeuralMemory 系统                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────┐     ┌────────────────┐    ┌────────────────┐  │
│  │   预加载层      │     │   懒加载层      │    │   按需加载层    │  │
│  │ (毫秒级启动)   │     │ (首次访问)     │    │ (功能调用时)   │  │
│  ├────────────────┼─────┼────────────────┼────┼────────────────┤  │
│  │ 1. 类型定义    │     │ 3. Imperial    │    │ 5. V3子系统   │  │
│  │ 2. 核心接口    │     │    Library     │    │ 6. V5超级记忆 │  │
│  │ 3. 轻量工具    │     │ 4. Encoder    │    │ 7. 知识库桥接  │  │
│  │               │     │ 5. ReplayBuffer│    │               │  │
│  └────────────────┘     └────────────────┘    └────────────────┘  │
│                                                                      │
│  加载时机：                                                          │
│  - 导入模块: 仅类型+轻量接口 (~0.1ms)                               │
│  - 首次API调用: 核心组件懒加载 (~10ms)                              │
│  - 深度功能调用: 按需加载子组件 (~50ms)                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

版本: v1.0.0
创建: 2026-04-28
"""

from __future__ import annotations

import time
import logging
from typing import Dict, Any, Optional, List, Set, TYPE_CHECKING
from dataclasses import dataclass, field
from collections import OrderedDict
from threading import Lock
import threading

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
#  加载策略配置
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class FastLoadConfig:
    """
    快速加载配置
    
    控制各组件的加载策略和时机：
    - EAGER: 启动时立即加载
    - LAZY: 首次访问时加载
    - ON_DEMAND: 功能调用时加载
    """
    # 核心组件加载策略
    library_strategy: str = "LAZY"      # ImperialLibrary
    encoder_strategy: str = "LAZY"      # SemanticEncoder
    replay_buffer_strategy: str = "ON_DEMAND"  # LearningReplayBuffer
    staff_registry_strategy: str = "ON_DEMAND"  # 权限注册表
    knowledge_bridge_strategy: str = "ON_DEMAND"  # 知识库桥接
    
    # V3 系统加载策略
    v3_system_strategy: str = "ON_DEMAND"  # NeuralMemorySystemV3
    v5_system_strategy: str = "ON_DEMAND"  # SuperNeuralMemory
    unified_interface_strategy: str = "ON_DEMAND"  # 统一接口
    
    # 缓存配置
    enable_component_cache: bool = True  # 组件缓存（进程级）
    cache_ttl_seconds: float = 300       # 缓存TTL（秒）
    
    # 预加载优化
    preload_lightweight: bool = True     # 预加载轻量级组件


class LoadStrategy:
    """加载策略枚举"""
    EAGER = "EAGER"       # 立即加载
    LAZY = "LAZY"         # 首次访问时加载
    ON_DEMAND = "ON_DEMAND"  # 按需加载


# ═══════════════════════════════════════════════════════════════════════════
#  加载状态追踪
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ComponentLoadState:
    """组件加载状态"""
    name: str
    loaded: bool = False
    loading: bool = False
    load_time: float = 0.0
    load_start: float = 0.0
    access_count: int = 0
    error: Optional[str] = None
    
    def start_load(self):
        self.loading = True
        self.load_start = time.time()
    
    def finish_load(self, success: bool = True, error: Optional[str] = None):
        self.loaded = success
        self.loading = False
        self.load_time = time.time() - self.load_start
        self.error = error


class LoadTracker:
    """
    组件加载追踪器
    
    记录每个组件的加载状态、耗时、访问次数
    """
    
    def __init__(self):
        self._states: Dict[str, ComponentLoadState] = {}
        self._lock = Lock()
        
        # 注册所有组件
        self._register_components()
    
    def _register_components(self):
        """注册所有可追踪的组件"""
        components = [
            # 核心组件
            "library",
            "encoder",
            "replay_buffer",
            "staff_registry",
            "knowledge_bridge",
            # V3/V5 系统
            "v3_system",
            "v5_system",
            "unified_interface",
            # V3 子系统
            "v3_encoding",
            "v3_rl",
            "v3_richness",
            "v3_granularity",
            "v3_v2_compat",
            # V5 子系统
            "v5_sage_memories",
            "v5_distillation",
            "v5_claw_memories",
            "v5_indexes",
        ]
        for name in components:
            self._states[name] = ComponentLoadState(name=name)
    
    def start(self, component: str) -> bool:
        """
        开始加载组件
        
        Returns:
            True 如果开始加载，False 如果已经在加载或已加载
        """
        with self._lock:
            if component not in self._states:
                self._states[component] = ComponentLoadState(name=component)
            
            state = self._states[component]
            if state.loaded or state.loading:
                return False
            
            state.start_load()
            return True
    
    def finish(self, component: str, success: bool = True, error: Optional[str] = None):
        """完成组件加载"""
        with self._lock:
            if component in self._states:
                self._states[component].finish_load(success, error)
    
    def access(self, component: str):
        """记录组件访问"""
        with self._lock:
            if component in self._states:
                self._states[component].access_count += 1
    
    def get_state(self, component: str) -> Optional[ComponentLoadState]:
        return self._states.get(component)
    
    def get_all_states(self) -> Dict[str, ComponentLoadState]:
        return self._states.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取加载统计"""
        total_load_time = 0.0
        loaded_count = 0
        with self._lock:
            for state in self._states.values():
                if state.loaded:
                    total_load_time += state.load_time
                    loaded_count += 1
        
        return {
            "total_components": len(self._states),
            "loaded_components": loaded_count,
            "pending_components": len(self._states) - loaded_count,
            "total_load_time_ms": total_load_time * 1000,
            "states": {
                name: {
                    "loaded": s.loaded,
                    "loading": s.loading,
                    "load_time_ms": s.load_time * 1000,
                    "access_count": s.access_count,
                    "error": s.error,
                }
                for name, s in self._states.items()
            }
        }


# ═══════════════════════════════════════════════════════════════════════════
#  全局追踪器
# ═══════════════════════════════════════════════════════════════════════════

# 进程级全局追踪器
_global_tracker: Optional[LoadTracker] = None
_tracker_lock = Lock()


def get_load_tracker() -> LoadTracker:
    """获取全局加载追踪器（单例）"""
    global _global_tracker
    with _tracker_lock:
        if _global_tracker is None:
            _global_tracker = LoadTracker()
        return _global_tracker


# ═══════════════════════════════════════════════════════════════════════════
#  懒加载管理器
# ═══════════════════════════════════════════════════════════════════════════

class LazyLoader:
    """
    懒加载管理器
    
    封装组件的懒加载逻辑：
    1. 首次访问时加载
    2. 并发访问控制（避免重复加载）
    3. 错误处理和恢复
    4. 加载时间追踪
    """
    
    def __init__(
        self,
        component_name: str,
        loader_func: callable,
        strategy: str = LoadStrategy.LAZY,
    ):
        self.component_name = component_name
        self.loader_func = loader_func
        self.strategy = strategy
        self._instance: Any = None
        self._lock = Lock()
        self._tracker = get_load_tracker()
    
    def _load(self) -> Any:
        """执行加载"""
        # 开始追踪
        if not self._tracker.start(self.component_name):
            # 已经在加载中，等待
            if self.strategy == LoadStrategy.LAZY:
                while self._tracker.get_state(self.component_name).loading:
                    time.sleep(0.001)
                return self._instance
            return self._instance
        
        try:
            logger.debug(f"[LazyLoader] 正在加载组件: {self.component_name}")
            self._instance = self.loader_func()
            self._tracker.finish(self.component_name, success=True)
            logger.debug(f"[LazyLoader] 组件加载完成: {self.component_name}")
            return self._instance
        except Exception as e:
            logger.error(f"[LazyLoader] 组件加载失败: {self.component_name} - {e}")
            self._tracker.finish(self.component_name, success=False, error=str(e))
            raise
    
    def get(self) -> Any:
        """
        获取组件实例
        
        根据策略决定何时加载
        """
        # 追踪访问
        self._tracker.access(self.component_name)
        
        # 已加载，直接返回
        if self._instance is not None:
            return self._instance
        
        with self._lock:
            # 双重检查
            if self._instance is not None:
                return self._instance
            
            if self.strategy == LoadStrategy.EAGER:
                return self._load()
            elif self.strategy == LoadStrategy.LAZY:
                return self._load()
            elif self.strategy == LoadStrategy.ON_DEMAND:
                # ON_DEMAND 模式：仅在显式请求时加载
                # 但首次调用时也会加载（因为需要返回值）
                return self._load()
            
            return None
    
    def preload(self) -> None:
        """预加载（供外部调用）"""
        if self._instance is None:
            self._load()
    
    def is_loaded(self) -> bool:
        return self._instance is not None
    
    def get_load_time(self) -> float:
        state = self._tracker.get_state(self.component_name)
        return state.load_time if state else 0.0
    
    def unload(self) -> bool:
        """
        卸载组件（支持LRU淘汰）。
        
        Returns:
            True 如果成功卸载，False 如果组件未加载
        """
        if self._instance is None:
            return False
        
        # 清理追踪器状态
        if self.component_name in self._tracker._states:
            state = self._tracker._states[self.component_name]
            state.loaded = False
            state.loading = False
            state._instance = None if hasattr(state, '_instance') else None
        
        # 释放实例引用（触发GC）
        self._instance = None
        logger.debug(f"[LazyLoader] 组件已卸载: {self.component_name}")
        return True
    
    def get_size_estimate(self) -> int:
        """
        估算组件占用的内存（字节）。
        仅做粗略估算：实例数量 * 平均对象大小。
        """
        if self._instance is None:
            return 0
        
        import sys
        try:
            # 尝试获取对象的近似大小
            return sys.getsizeof(self._instance)
        except Exception:
            # 如果失败，返回一个默认估计值
            return 1024  # 1KB 保守估计


# ═══════════════════════════════════════════════════════════════════════════
#  快速初始化核心
# ═══════════════════════════════════════════════════════════════════════════

class NeuralMemoryFastLoader:
    """
    NeuralMemory 快速加载器
    
    提供 NeuralMemory 各组件的快速初始化：
    1. 毫秒级启动（仅核心接口）
    2. 组件懒加载（按需加载）
    3. 并发控制（避免重复加载）
    4. 加载追踪（性能监控）
    """
    
    def __init__(self, config: Optional[FastLoadConfig] = None):
        self.config = config or FastLoadConfig()
        self._tracker = get_load_tracker()
        
        # 组件加载器
        self._loaders: Dict[str, LazyLoader] = {}
        self._initialized = False
        
        # 初始化加载器
        self._setup_loaders()
    
    def _setup_loaders(self):
        """设置组件加载器"""
        cfg = self.config
        
        # ImperialLibrary - 默认懒加载
        self._loaders["library"] = LazyLoader(
            "library",
            self._create_library,
            cfg.library_strategy,
        )
        
        # SemanticEncoder - 默认懒加载
        self._loaders["encoder"] = LazyLoader(
            "encoder",
            self._create_encoder,
            cfg.encoder_strategy,
        )
        
        # LearningReplayBuffer - 按需加载
        self._loaders["replay_buffer"] = LazyLoader(
            "replay_buffer",
            self._create_replay_buffer,
            cfg.replay_buffer_strategy,
        )
        
        # StaffRegistry - 按需加载
        self._loaders["staff_registry"] = LazyLoader(
            "staff_registry",
            self._create_staff_registry,
            cfg.staff_registry_strategy,
        )
        
        # KnowledgeBridge - 按需加载
        self._loaders["knowledge_bridge"] = LazyLoader(
            "knowledge_bridge",
            self._create_knowledge_bridge,
            cfg.knowledge_bridge_strategy,
        )
        
        # V3 System - 按需加载
        self._loaders["v3_system"] = LazyLoader(
            "v3_system",
            self._create_v3_system,
            cfg.v3_system_strategy,
        )
        
        # V5 System - 按需加载
        self._loaders["v5_system"] = LazyLoader(
            "v5_system",
            self._create_v5_system,
            cfg.v5_system_strategy,
        )
        
        # UnifiedInterface - 按需加载
        self._loaders["unified_interface"] = LazyLoader(
            "unified_interface",
            self._create_unified_interface,
            cfg.unified_interface_strategy,
        )
        
        # 预加载轻量级组件
        if self.config.preload_lightweight:
            self._preload_lightweight()
    
    def _preload_lightweight(self):
        """预加载轻量级组件"""
        logger.debug("[FastLoader] 预加载轻量级组件...")
        # 延迟到后台线程
        threading.Thread(target=self._preload_lightweight_async, daemon=True).start()
    
    def _preload_lightweight_async(self):
        """后台预加载"""
        time.sleep(0.1)  # 等待主线程初始化完成
        # 预加载 encoder（轻量）
        try:
            self.get_encoder()
        except Exception as e:
            logger.debug(f"[FastLoader] encoder 预加载跳过: {e}")
    
    # ═══════════════════════════════════════════════════════════════════
    #  组件创建函数
    # ═══════════════════════════════════════════════════════════════════
    
    def _create_library(self) -> Any:
        """创建 ImperialLibrary"""
        from src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        return ImperialLibrary()
    
    def _create_encoder(self) -> Any:
        """创建 SemanticEncoder"""
        from src.intelligence.dispatcher.wisdom_dispatch._semantic_encoder import get_semantic_encoder
        return get_semantic_encoder()
    
    def _create_replay_buffer(self) -> Any:
        """创建 LearningReplayBuffer"""
        from src.neural_memory.learning_replay_buffer import get_replay_buffer
        return get_replay_buffer()
    
    def _create_staff_registry(self) -> Any:
        """创建 StaffRegistry"""
        from src.intelligence.dispatcher.wisdom_dispatch._library_staff_registry import get_staff_registry
        registry = get_staff_registry()
        registry.ensure_initialized()
        return registry
    
    def _create_knowledge_bridge(self) -> Any:
        """创建 KnowledgeBridge"""
        from src.intelligence.dispatcher.wisdom_dispatch._library_knowledge_bridge import get_knowledge_bridge
        return get_knowledge_bridge()
    
    def _create_v3_system(self) -> Any:
        """创建 NeuralMemorySystemV3"""
        from src.neural_memory.neural_memory_system_v3 import NeuralMemorySystemV3
        return NeuralMemorySystemV3()
    
    def _create_v5_system(self) -> Any:
        """创建 SuperNeuralMemory"""
        from src.intelligence.engines._super_neural_memory import get_super_memory
        return get_super_memory()
    
    def _create_unified_interface(self) -> Any:
        """创建 UnifiedMemoryInterface"""
        from src.neural_memory.unified_memory_interface import UnifiedMemoryInterface
        return UnifiedMemoryInterface()
    
    # ═══════════════════════════════════════════════════════════════════
    #  组件获取接口
    # ═══════════════════════════════════════════════════════════════════
    
    def get_library(self) -> Any:
        """获取 ImperialLibrary"""
        return self._loaders["library"].get()
    
    def get_encoder(self) -> Any:
        """获取 SemanticEncoder"""
        return self._loaders["encoder"].get()
    
    def get_replay_buffer(self) -> Any:
        """获取 LearningReplayBuffer"""
        return self._loaders["replay_buffer"].get()
    
    def get_staff_registry(self) -> Any:
        """获取 StaffRegistry"""
        return self._loaders["staff_registry"].get()
    
    def get_knowledge_bridge(self) -> Any:
        """获取 KnowledgeBridge"""
        return self._loaders["knowledge_bridge"].get()
    
    def get_v3_system(self) -> Any:
        """获取 NeuralMemorySystemV3"""
        return self._loaders["v3_system"].get()
    
    def get_v5_system(self) -> Any:
        """获取 SuperNeuralMemory"""
        return self._loaders["v5_system"].get()
    
    def get_unified_interface(self) -> Any:
        """获取 UnifiedMemoryInterface"""
        return self._loaders["unified_interface"].get()
    
    # ═══════════════════════════════════════════════════════════════════
    #  预热接口
    # ═══════════════════════════════════════════════════════════════════
    
    def warm_up(self, components: Optional[List[str]] = None):
        """
        预热指定组件
        
        Args:
            components: 要预热的组件列表，None 表示全部
        """
        if components is None:
            components = list(self._loaders.keys())
        
        for name in components:
            if name in self._loaders:
                try:
                    self._loaders[name].preload()
                except Exception as e:
                    logger.warning(f"[FastLoader] 预热失败: {name} - {e}")
    
    # ═══════════════════════════════════════════════════════════════════
    #  统计接口
    # ═══════════════════════════════════════════════════════════════════
    
    def get_stats(self) -> Dict[str, Any]:
        """获取加载统计"""
        stats = {
            "config": {
                "library_strategy": self.config.library_strategy,
                "encoder_strategy": self.config.encoder_strategy,
                "replay_buffer_strategy": self.config.replay_buffer_strategy,
                "v3_system_strategy": self.config.v3_system_strategy,
                "v5_system_strategy": self.config.v5_system_strategy,
            },
            "tracker": self._tracker.get_stats(),
            "loaders": {
                name: {
                    "loaded": loader.is_loaded(),
                    "load_time_ms": loader.get_load_time() * 1000,
                }
                for name, loader in self._loaders.items()
            }
        }
        return stats


# ═══════════════════════════════════════════════════════════════════════════
#  全局快速加载器
# ═══════════════════════════════════════════════════════════════════════════

_global_fast_loader: Optional[NeuralMemoryFastLoader] = None
_fast_loader_lock = Lock()


def get_fast_loader(config: Optional[FastLoadConfig] = None) -> NeuralMemoryFastLoader:
    """
    获取全局快速加载器（单例）
    
    Usage:
        loader = get_fast_loader()
        
        # 毫秒级启动
        stats = loader.get_stats()
        
        # 首次访问时懒加载
        library = loader.get_library()
        
        # 预热特定组件
        loader.warm_up(["library", "encoder"])
    """
    global _global_fast_loader
    with _fast_loader_lock:
        if _global_fast_loader is None:
            _global_fast_loader = NeuralMemoryFastLoader(config)
        return _global_fast_loader


# ═══════════════════════════════════════════════════════════════════════════
#  便捷函数
# ═══════════════════════════════════════════════════════════════════════════

def quick_load_summary() -> Dict[str, Any]:
    """
    快速加载摘要（毫秒级）
    
    Returns:
        包含加载状态和统计的字典
    """
    tracker = get_load_tracker()
    return tracker.get_stats()


def preload_memory_components(components: Optional[List[str]] = None):
    """
    预加载指定组件
    
    Args:
        components: ["library", "encoder", "replay_buffer", ...]
    """
    loader = get_fast_loader()
    loader.warm_up(components)


# ═══════════════════════════════════════════════════════════════════════════
#  版本信息
# ═══════════════════════════════════════════════════════════════════════════

__version__ = "6.2.0"
__all__ = [
    "FastLoadConfig",
    "LoadStrategy",
    "LoadTracker",
    "LazyLoader",
    "NeuralMemoryFastLoader",
    "get_fast_loader",
    "get_load_tracker",
    "quick_load_summary",
    "preload_memory_components",
]
