"""
SageDispatch Quick Load Module - 快速加载模块
=====================================

设计原则：
1. 预加载：轻量级资源（正则、配置、索引）→ ~5ms
2. 懒加载：重量级资源（知识库、模型）→ 按需加载
3. 缓存复用：类级别缓存，避免重复初始化

加载层级：
┌─────────────────────────────────────────────────────────┐
│  L0: 零级（< 1ms）                                       │
│  - 常量、枚举、类定义                                      │
│  - 调度器注册表                                            │
├─────────────────────────────────────────────────────────┤
│  L1: 一级预加载（< 5ms）                                   │
│  - 编译正则表达式                                          │
│  - 关键词库                                               │
│  - 格子索引                                               │
├─────────────────────────────────────────────────────────┤
│  L2: 二级懒加载（首次10-50ms，之后< 1ms）                    │
│  - DomainNexus 知识库                                    │
│  - 调度器实例                                             │
│  - DivineReason 模型资源                                  │
├─────────────────────────────────────────────────────────┤
│  L3: 三级懒加载（按需50-200ms）                            │
│  - Track B 神行轨                                         │
│  - 外部API                                               │
└─────────────────────────────────────────────────────────┘

Version: S1.0
"""

import time
import re
import threading
from typing import Dict, Any, Optional, Callable, Set, List
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache


# ==================== L0: 零级（瞬时加载） ====================

class QuickLoadLevel(Enum):
    """加载级别枚举"""
    ZERO = 0      # 零级：常量、枚举
    ONE = 1       # 一级：预加载资源
    TWO = 2       # 二级：懒加载资源
    THREE = 3     # 三级：按需加载


# ==================== L1: 一级预加载（< 5ms） ====================

class Preloader:
    """
    预加载器 - L1级快速加载
    
    在模块导入时立即执行，仅加载轻量级资源：
    1. 正则表达式编译
    2. 关键词库
    3. 调度器注册表
    """
    
    # 类级别缓存（所有实例共享）
    _PRELOADED = False
    _PRELOAD_TIME = 0.0
    
    # 编译好的正则表达式
    COMPILED_PATTERNS: Dict[str, re.Pattern] = {}
    
    # 关键词库（分片懒加载 — 只在 get_keywords() 首次访问对应 category 时才构建）
    _KEYWORD_LIB_RAW: Optional[Dict[str, List[str]]] = None
    KEYWORD_LIB: Dict[str, List[str]] = {}
    _KEYWORD_LOADED_CATEGORIES: set = set()
    
    # 调度器注册表
    DISPATCHER_REGISTRY: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def preload(cls) -> float:
        """
        执行预加载 - 返回加载时间
        
        Returns:
            预加载耗时（毫秒）
        """
        if cls._PRELOADED:
            return cls._PRELOAD_TIME
        
        start = time.perf_counter()
        
        # 1. 编译正则表达式
        cls._compile_patterns()
        
        # 2. 关键词库改为按需加载（不再在 preload 时全量构建）
        #    只初始化原始数据引用，实际 dict 构建延迟到 get_keywords() 调用
        
        # 3. 初始化调度器注册表
        cls._init_dispatcher_registry()
        
        cls._PRELOADED = True
        cls._PRELOAD_TIME = (time.perf_counter() - start) * 1000
        
        return cls._PRELOAD_TIME
    
    @classmethod
    def _compile_patterns(cls):
        """编译正则表达式（避免运行时重复编译）"""
        cls.COMPILED_PATTERNS = {
            # 基础文本提取
            "chinese_word": re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,}'),
            "chinese_char": re.compile(r'[\u4e00-\u9fa5]'),
            
            # 因果关系
            "causal": re.compile(r'(因为|所以|导致|造成|由于|因此|故)'),
            
            # 假设条件
            "hypothesis": re.compile(r'(如果|假设|假如|倘若|倘若)'),
            
            # 证据支持
            "evidence": re.compile(r'(支持|反对|证据|数据|研究|表明|显示)'),
            
            # 时间表达
            "time": re.compile(r'(年|月|日|时|分|秒|周|天|小时|分钟)'),
            
            # 数字提取
            "number": re.compile(r'\d+(?:\.\d+)?(?:[万亿千百十])?'),
            
            # 问题标记
            "question": re.compile(r'[？?]'),
            
            # URL
            "url": re.compile(r'https?://[^\s]+'),
            
            # 邮件
            "email": re.compile(r'\w+@\w+\.\w+'),
        }
    
    @classmethod
    def _load_keyword_lib(cls):
        """加载关键词库原始数据（仅构建 dict 一次）"""
        if cls._KEYWORD_LIB_RAW is not None:
            return
        cls._KEYWORD_LIB_RAW = {
            # 因果标记词
            "causal_markers": [
                "因为", "所以", "导致", "造成", "由于", "因此", "故", 
                "既然", "则", "因而", "于是", "故而"
            ],
            
            # 推理标记词
            "reasoning_markers": [
                "分析", "推理", "判断", "论证", "评估", "推断", 
                "演绎", "归纳", "类比", "总结", "概括"
            ],
            
            # 不确定性标记词
            "uncertainty_markers": [
                "可能", "也许", "或许", "大概", "估计", "应该",
                "似乎", "好像", "看来", "不确定", "风险"
            ],
            
            # 问题类型标记词
            "problem_type_markers": {
                "information": ["是什么", "如何", "怎么", "多少", "谁", "哪里", "查询", "告诉"],
                "analysis": ["分析", "评估", "判断", "检验", "研究"],
                "planning": ["战略", "规划", "策划", "设计", "布局", "方案"],
                "decision": ["决策", "选择", "决定", "定夺", "取舍"],
                "execution": ["执行", "实施", "落地", "操作", "操作"],
                "innovation": ["创新", "变革", "突破", "转型", "颠覆"]
            },
            
            # 紧急程度标记词
            "urgency_markers": {
                "high": ["紧急", "立即", "马上", "立刻", "刻不容缓", "十万火急"],
                "medium": ["尽快", "优先", "重要", "急", "速"],
                "normal": []
            },
            
            # 调度级别标记词
            "level_markers": {
                "L1": ["是什么", "如何", "怎么", "查询", "时间", "天气", "多少", "几点"],
                "L2": ["分析", "推理", "判断", "论证", "评估", "逻辑", "为什么"],
                "L3": ["战略", "规划", "策划", "全面", "深度", "系统", "设计", "架构"],
                "L4": ["创新", "突破", "颠覆", "创造", "本质", "哲学", "智慧", "极致"]
            },
            
            # 谬误检测标记词
            "fallacy_markers": {
                "ad_hominem": ["你这个人", "他这种人", "谁让你"],
                "straw_man": ["你说的是", "你的意思就是", "你不过是想"],
                "appeal_to_authority": ["专家说", "权威认为", "某某名人说过"],
                "false_dilemma": ["要么", "不是", "只能"],
                "slippery_slope": ["如果", "就会", "最终导致", "必然"],
                "circular_reasoning": ["因为", "所以", "所以说", "换句话说"],
                "hasty_generalization": ["所有", "都", "从来不", "总是"],
                "red_herring": ["说起这个", "不过", "另外", "其实"]
            },
            
            # 学派标记词
            "school_markers": {
                "daoism": ["无为", "自然", "道"],
                "confucianism": ["仁义", "礼", "君子"],
                "buddhism": ["因果", "缘", "空"],
                "military": ["谋略", "权变", "战略"],
                "philosophy": ["本体", "认识", "价值"],
                "science": ["实验", "假设", "验证"],
                "economics": ["供需", "成本", "效益"],
                "psychology": ["动机", "认知", "行为"],
                "systems": ["系统", "反馈", "整体"],
                "complexity": ["涌现", "混沌", "自组织"],
                "game_theory": ["策略", "均衡", "竞合"],
                "yinyang": ["阴阳", "辩证", "对立"]
            }
        }
    
    @classmethod
    def _init_dispatcher_registry(cls):
        """初始化调度器注册表"""
        cls.DISPATCHER_REGISTRY = {
            # 四级调度总控
            "SD-F2": {
                "name": "四级调度总控",
                "priority": 0,
                "level": QuickLoadLevel.ZERO,
                "preload_required": ["patterns", "keywords"],
                "lazy_load": ["sub_dispatchers"]
            },
            
            # 问题调度（核心树干）
            "SD-P1": {
                "name": "问题调度",
                "priority": 1,
                "level": QuickLoadLevel.ONE,
                "preload_required": ["patterns", "keywords"],
                "lazy_load": ["domain_nexus"]
            },
            
            # 三层推理监管
            "SD-R1": {
                "name": "三层推理监管",
                "priority": 2,
                "level": QuickLoadLevel.ONE,
                "preload_required": ["patterns"],
                "lazy_load": []
            },
            
            # 谬误检测
            "SD-R2": {
                "name": "谬误检测",
                "priority": 3,
                "level": QuickLoadLevel.ONE,
                "preload_required": ["patterns", "fallacy_markers"],
                "lazy_load": ["track_b"]
            },
            
            # 学派融合
            "SD-F1": {
                "name": "25学派融合",
                "priority": 4,
                "level": QuickLoadLevel.ONE,
                "preload_required": ["patterns", "school_markers"],
                "lazy_load": ["track_b", "wisdom_tree"]
            },
            
            # 深度推理系列
            "SD-D1": {
                "name": "轻量深度推理",
                "priority": 5,
                "level": QuickLoadLevel.ONE,
                "preload_required": ["patterns"],
                "lazy_load": ["divine_reason_layer1"]
            },
            "SD-D2": {
                "name": "标准深度推理",
                "priority": 6,
                "level": QuickLoadLevel.TWO,
                "preload_required": ["patterns"],
                "lazy_load": ["divine_reason_layer2"]
            },
            "SD-D3": {
                "name": "极致深度推理",
                "priority": 7,
                "level": QuickLoadLevel.TWO,
                "preload_required": ["patterns"],
                "lazy_load": ["divine_reason_layer3"]
            },
            
            # 决策系列
            "SD-C1": {
                "name": "太极阴阳决策",
                "priority": 8,
                "level": QuickLoadLevel.ONE,
                "preload_required": ["patterns", "yinyang_keywords"],
                "lazy_load": []
            },
            "SD-C2": {
                "name": "神之架构决策",
                "priority": 9,
                "level": QuickLoadLevel.TWO,
                "preload_required": ["patterns"],
                "lazy_load": ["divine_architecture", "track_b"]
            },
            
            # 执行
            "SD-E1": {
                "name": "五步主链执行",
                "priority": 10,
                "level": QuickLoadLevel.ONE,
                "preload_required": [],
                "lazy_load": ["track_b"]
            },
            
            # 学习进化
            "SD-L1": {
                "name": "学习进化",
                "priority": 11,
                "level": QuickLoadLevel.ONE,
                "preload_required": [],
                "lazy_load": ["track_b"]
            }
        }
    
    @classmethod
    def is_preloaded(cls) -> bool:
        """检查是否已预加载"""
        return cls._PRELOADED
    
    @classmethod
    def get_load_time(cls) -> float:
        """获取预加载耗时"""
        return cls._PRELOAD_TIME
    
    @classmethod
    def get_pattern(cls, name: str) -> Optional[re.Pattern]:
        """获取编译好的正则表达式"""
        return cls.COMPILED_PATTERNS.get(name)
    
    @classmethod
    def get_keywords(cls, category: str) -> List[str]:
        """获取关键词库（按需懒加载对应分类）"""
        # 如果该分类已经加载过，直接返回
        if category in cls._KEYWORD_LOADED_CATEGORIES:
            return cls.KEYWORD_LIB.get(category, [])
        
        # 首次访问：确保原始数据已构建
        cls._load_keyword_lib()
        
        # 加载该分类
        if category in cls._KEYWORD_LIB_RAW:
            cls.KEYWORD_LIB[category] = cls._KEYWORD_LIB_RAW[category]
            cls._KEYWORD_LOADED_CATEGORIES.add(category)
        
        return cls.KEYWORD_LIB.get(category, [])
    
    @classmethod
    def get_dispatcher_info(cls, dispatcher_id: str) -> Optional[Dict]:
        """获取调度器信息"""
        return cls.DISPATCHER_REGISTRY.get(dispatcher_id)


# ==================== L2: 二级懒加载 ====================

class LazyLoader:
    """
    懒加载器 - L2级按需加载
    
    使用延迟初始化和LRU缓存策略：
    1. 调度器实例缓存
    2. DomainNexus连接
    3. DivineReason模型资源
    """
    
    # 单例实例
    _instance: Optional['LazyLoader'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        """初始化懒加载器状态"""
        self._dispatcher_cache: Dict[str, Any] = {}
        self._domain_nexus = None
        self._divine_reason_cache: Dict[str, Any] = {}
        self._load_stats: Dict[str, Dict] = {}
    
    # ==================== 调度器懒加载 ====================
    
    def get_dispatcher(self, dispatcher_id: str) -> Optional[Any]:
        """
        获取调度器实例（懒加载）
        
        Args:
            dispatcher_id: 调度器ID
            
        Returns:
            调度器实例
        """
        if dispatcher_id in self._dispatcher_cache:
            return self._dispatcher_cache[dispatcher_id]
        
        # 懒加载调度器
        dispatcher = self._lazy_load_dispatcher(dispatcher_id)
        
        if dispatcher:
            self._dispatcher_cache[dispatcher_id] = dispatcher
            self._record_load(dispatcher_id, "dispatcher")
        
        return dispatcher
    
    def _lazy_load_dispatcher(self, dispatcher_id: str) -> Optional[Any]:
        """懒加载调度器实例"""
        try:
            # 延迟导入
            from .dispatchers import (
                FourLevelDispatchController,
                ProblemDispatcher,
                ThreeLayerReasoning,
                FallacyChecker,
                SchoolFusion,
                SuperReasoning,
                YinYangDecision,
                DivineArchitecture,
                ChainExecutor,
                ResultTracker,
            )
            
            dispatcher_map = {
                "SD-F2": FourLevelDispatchController,
                "SD-P1": ProblemDispatcher,
                "SD-R1": ThreeLayerReasoning,
                "SD-R2": FallacyChecker,
                "SD-F1": SchoolFusion,
                "SD-D1": lambda: SuperReasoning("light"),
                "SD-D2": lambda: SuperReasoning("standard"),
                "SD-D3": lambda: SuperReasoning("deep"),
                "SD-C1": YinYangDecision,
                "SD-C2": DivineArchitecture,
                "SD-E1": ChainExecutor,
                "SD-L1": ResultTracker,
            }
            
            factory = dispatcher_map.get(dispatcher_id)
            if factory:
                if callable(factory) and not isinstance(factory, type):
                    return factory()
                return factory()
            
            return None
            
        except ImportError:
            return None
    
    # ==================== DomainNexus懒加载 ====================
    
    def get_domain_nexus(self) -> Any:
        """
        获取DomainNexus实例（懒加载）
        
        Returns:
            DomainNexus实例
        """
        if self._domain_nexus is not None:
            return self._domain_nexus
        
        try:
            from .domain_nexus import get_nexus
            self._domain_nexus = get_nexus()
            self._record_load("DomainNexus", "knowledge")
            return self._domain_nexus
        except ImportError:
            return None
    
    # ==================== DivineReason懒加载 ====================
    
    def get_divine_reason(self, depth: str = "standard") -> Any:
        """
        获取DivineReason实例（懒加载）
        
        Args:
            depth: 推理深度 "light" | "standard" | "deep"
            
        Returns:
            DivineReason实例
        """
        if depth in self._divine_reason_cache:
            return self._divine_reason_cache[depth]
        
        try:
            from .divine_reason import DivineReason
            divine = DivineReason(depth=depth)
            self._divine_reason_cache[depth] = divine
            self._record_load(f"DivineReason-{depth}", "model")
            return divine
        except ImportError:
            return None
    
    # ==================== 统计和缓存管理 ====================
    
    def _record_load(self, resource_id: str, resource_type: str):
        """记录加载统计"""
        self._load_stats[resource_id] = {
            "type": resource_type,
            "loaded_at": time.time(),
            "access_count": 1
        }
    
    def record_access(self, resource_id: str):
        """记录资源访问"""
        if resource_id in self._load_stats:
            self._load_stats[resource_id]["access_count"] += 1
    
    def get_load_stats(self) -> Dict[str, Dict]:
        """获取加载统计"""
        return self._load_stats.copy()
    
    def get_cached_resources(self) -> List[str]:
        """获取已缓存的资源列表"""
        return list(self._dispatcher_cache.keys()) + \
               ([self._domain_nexus.__class__.__name__] if self._domain_nexus else []) + \
               list(self._divine_reason_cache.keys())
    
    def clear_cache(self):
        """清空缓存"""
        self._dispatcher_cache.clear()
        self._domain_nexus = None
        self._divine_reason_cache.clear()
        self._load_stats.clear()


# ==================== L3: 三级按需加载 ====================

class OnDemandLoader:
    """
    按需加载器 - L3级外部资源加载

    用于加载重量级外部资源：
    1. Track B 神行轨
    2. 外部API
    3. 大型模型

    v7.1: 增加线程安全双重检查锁定
    """

    _instance: Optional['OnDemandLoader'] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        """初始化按需加载器状态"""
        self._track_b = None
        self._external_apis: Dict[str, Any] = {}
        self._load_queue: List[str] = []
    
    def get_track_b(self) -> Optional[Any]:
        """获取Track B神行轨（按需加载）"""
        if self._track_b is not None:
            return self._track_b
        
        try:
            from .track_b_adapter import get_track_b_executor
            self._track_b = get_track_b_executor()
            return self._track_b
        except (ImportError, Exception):
            return None
    
    def queue_load(self, resource_id: str):
        """将资源加入加载队列"""
        if resource_id not in self._load_queue:
            self._load_queue.append(resource_id)
    
    def load_queued(self) -> int:
        """
        加载队列中的所有资源
        
        Returns:
            加载的资源数量
        """
        loaded = 0
        for resource_id in self._load_queue:
            if self._load_resource(resource_id):
                loaded += 1
        self._load_queue.clear()
        return loaded
    
    def _load_resource(self, resource_id: str) -> bool:
        """加载单个资源"""
        try:
            if resource_id == "track_b":
                return self.get_track_b() is not None
            return False
        except Exception:
            return False


# ==================== 快捷访问函数 ====================

def preload() -> float:
    """
    执行全局预加载
    
    Returns:
        预加载耗时（毫秒）
    """
    return Preloader.preload()


def is_ready() -> bool:
    """检查系统是否就绪"""
    return Preloader.is_preloaded()


def quick_dispatch(problem: str, dispatcher_id: str = "SD-P1") -> Dict:
    """
    快速调度（最小化加载）
    
    Args:
        problem: 问题描述
        dispatcher_id: 调度器ID
        
    Returns:
        调度结果
    """
    # 确保预加载完成
    preload()
    
    # 懒加载调度器
    loader = LazyLoader()
    dispatcher = loader.get_dispatcher(dispatcher_id)
    
    if not dispatcher:
        return {
            "error": f"调度器 {dispatcher_id} 不可用",
            "dispatcher_id": dispatcher_id
        }
    
    # 构建请求
    from .core import DispatchRequest
    
    request = DispatchRequest(
        problem={"description": problem}
    )
    
    # 执行调度
    return dispatcher.dispatch(request)


def get_load_info() -> Dict[str, Any]:
    """
    获取加载信息
    
    Returns:
        加载状态信息
    """
    loader = LazyLoader()
    
    return {
        "preloaded": Preloader.is_preloaded(),
        "preload_time_ms": Preloader.get_load_time(),
        "cached_dispatchers": list(loader._dispatcher_cache.keys()),
        "domain_nexus_loaded": loader._domain_nexus is not None,
        "divine_reason_cached": list(loader._divine_reason_cache.keys()),
        "total_cached": len(loader.get_cached_resources()),
        "load_stats": loader.get_load_stats()
    }


# ==================== 上下文管理器 ====================

class LoadContext:
    """加载上下文管理器"""
    
    def __init__(self, min_level: QuickLoadLevel = QuickLoadLevel.ONE):
        self.min_level = min_level
        self.loaded_resources: Set[str] = set()
        self.start_time = 0.0
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        preload()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = (time.perf_counter() - self.start_time) * 1000
        self.loaded_resources.add("Preloader")
        
        # 记录加载的调度器
        loader = LazyLoader()
        self.loaded_resources.update(loader.get_cached_resources())
        
        return False
    
    def lazy_load_dispatcher(self, dispatcher_id: str) -> Any:
        """在上下文中懒加载调度器"""
        loader = LazyLoader()
        dispatcher = loader.get_dispatcher(dispatcher_id)
        if dispatcher:
            self.loaded_resources.add(dispatcher_id)
        return dispatcher
    
    def get_elapsed_ms(self) -> float:
        """获取上下文内的总耗时"""
        return (time.perf_counter() - self.start_time) * 1000


# ==================== 性能基准测试 ====================

def benchmark_load_speeds(iterations: int = 10) -> Dict[str, Any]:
    """
    基准测试：测量各环节加载速度
    
    Args:
        iterations: 测试迭代次数
        
    Returns:
        性能测试结果
    """
    results = {
        "L0_import": [],
        "L1_preload": [],
        "L2_lazy_dispatcher": [],
        "L2_lazy_nexus": [],
        "L2_lazy_divine": [],
        "L3_track_b": [],
        "full_pipeline": []
    }
    
    for i in range(iterations):
        # L0: 模块导入（通常由Python缓存，实际测不出来）
        start = time.perf_counter()
        # import knowledge_cells  # 已导入
        results["L0_import"].append((time.perf_counter() - start) * 1000)
        
        # L1: 预加载
        Preloader._PRELOADED = False  # 重置
        start = time.perf_counter()
        Preloader.preload()
        results["L1_preload"].append((time.perf_counter() - start) * 1000)
        
        # L2: 懒加载调度器
        loader = LazyLoader()
        loader._dispatcher_cache.clear()  # 清空缓存
        loader._domain_nexus = None
        loader._divine_reason_cache.clear()
        
        start = time.perf_counter()
        loader.get_dispatcher("SD-P1")
        results["L2_lazy_dispatcher"].append((time.perf_counter() - start) * 1000)
        
        # L2: 懒加载DomainNexus
        loader._domain_nexus = None
        start = time.perf_counter()
        loader.get_domain_nexus()
        results["L2_lazy_nexus"].append((time.perf_counter() - start) * 1000)
        
        # L2: 懒加载DivineReason
        start = time.perf_counter()
        loader.get_divine_reason("standard")
        results["L2_lazy_divine"].append((time.perf_counter() - start) * 1000)
        
        # L3: 按需加载Track B
        on_demand = OnDemandLoader()
        on_demand._track_b = None
        start = time.perf_counter()
        on_demand.get_track_b()
        results["L3_track_b"].append((time.perf_counter() - start) * 1000)
        
        # 全流程
        start = time.perf_counter()
        preload()
        loader = LazyLoader()
        loader.get_dispatcher("SD-P1")
        results["full_pipeline"].append((time.perf_counter() - start) * 1000)
    
    # 计算统计
    def calc_stats(times):
        times = [t for t in times if t > 0]
        if not times:
            return {"avg_ms": 0, "min_ms": 0, "max_ms": 0}
        return {
            "avg_ms": round(sum(times) / len(times), 3),
            "min_ms": round(min(times), 3),
            "max_ms": round(max(times), 3)
        }
    
    return {
        "iterations": iterations,
        "L0_import": calc_stats(results["L0_import"]),
        "L1_preload": calc_stats(results["L1_preload"]),
        "L2_lazy_dispatcher": calc_stats(results["L2_lazy_dispatcher"]),
        "L2_lazy_nexus": calc_stats(results["L2_lazy_nexus"]),
        "L2_lazy_divine": calc_stats(results["L2_lazy_divine"]),
        "L3_track_b": calc_stats(results["L3_track_b"]),
        "full_pipeline": calc_stats(results["full_pipeline"])
    }


# ==================== 导出 ====================

__all__ = [
    # 加载级别
    "QuickLoadLevel",
    
    # 预加载器
    "Preloader",
    
    # 懒加载器
    "LazyLoader",
    
    # 按需加载器
    "OnDemandLoader",
    
    # 上下文管理器
    "LoadContext",
    
    # 快捷函数
    "preload",
    "is_ready",
    "quick_dispatch",
    "get_load_info",
    "benchmark_load_speeds",
]
