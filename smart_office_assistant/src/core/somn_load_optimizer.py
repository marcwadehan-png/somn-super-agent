"""
Somn 全局加载优化 - 集成 GlobalLoadManager
实现最快、最高效的启动加载
"""
import sys
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import logging

# 路径设置
_project_root = Path(__file__).resolve().parent.parent
_src_path = _project_root / 'src'
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
if str(_src_path) not in sys.path:
    sys.path.insert(0, str(_src_path))

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# 全局加载管理器集成
# ═══════════════════════════════════════════════════════════════════════════════

class SomnLoadOptimizer:
    """
    Somn 加载优化器
    - 集成 GlobalLoadManager
    - 实现智能预加载
    - 提供加载策略配置
    """
    
    # 模块加载策略配置（只保留已注册的模块）
    MODULE_STRATEGIES = {
        # Layer 1: 基础层 - 立即加载（启动时必须）
        'tool_registry': {'strategy': 'eager', 'priority': 0},
        'llm_service': {'strategy': 'lazy', 'priority': 1},
        
        # Layer 2: 数据层 - 独立懒加载
        'kg_engine': {'strategy': 'lazy', 'priority': 2, 'preload_after': 5.0},
        'web_search': {'strategy': 'lazy', 'priority': 2},
        'memory_system': {'strategy': 'lazy', 'priority': 3, 'preload_after': 10.0},
        
        # Layer 3-5: 智能层 - 懒加载
        'user_classifier': {'strategy': 'lazy', 'priority': 2},
        'demand_analyzer': {'strategy': 'lazy', 'priority': 2},
        'strategy_engine': {'strategy': 'lazy', 'priority': 2},
        'narrative_layer': {'strategy': 'lazy', 'priority': 3},
    }
    
    def __init__(self, somn_instance):
        self.somn = somn_instance
        self.load_manager = None  # 将在 init() 中初始化
        self._preload_timers: Dict[str, threading.Timer] = {}
        
    def init(self):
        """初始化加载优化器"""
        from src.core.global_load_manager import (
            GlobalLoadManager, LoadPriority, LoadStrategy
        )
        
        self.load_manager = GlobalLoadManager()
        
        # 注册所有模块
        self._register_all_modules()
        
        # 启动预加载策略（如果启用）
        if hasattr(self.somn, 'config') and getattr(self.somn.config, 'enable_preload', True):
            self._start_preload_strategy()
            logger.info("[SomnLoadOptimizer] 初始化完成，预加载已启用")
        else:
            logger.info("[SomnLoadOptimizer] 初始化完成，预加载已禁用")
    
    def _register_all_modules(self):
        """注册所有模块到 GlobalLoadManager"""
        from src.core.global_load_manager import LoadPriority, LoadStrategy
        
        # Layer 1: 工具注册表
        self.load_manager.register(
            'tool_registry',
            factory=self._create_tool_registry,
            strategy=LoadStrategy.EAGER if self.MODULE_STRATEGIES['tool_registry']['strategy'] == 'eager' else LoadStrategy.LAZY,
            priority=LoadPriority(self.MODULE_STRATEGIES['tool_registry']['priority']),
            dependencies=[]
        )
        
        # Layer 1: LLM 服务
        self.load_manager.register(
            'llm_service',
            factory=self._create_llm_service,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(1),
            dependencies=[]
        )
        
        # Layer 2: 知识图谱引擎
        self.load_manager.register(
            'kg_engine',
            factory=self._create_kg_engine,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(2),
            dependencies=[]
        )
        
        # Layer 2: 网络搜索
        self.load_manager.register(
            'web_search',
            factory=self._create_web_search,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(2),
            dependencies=[]
        )
        
        # Layer 2: 记忆系统
        self.load_manager.register(
            'memory_system',
            factory=self._create_memory_system,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(3),
            dependencies=[]
        )
        
        # Layer 3: 用户分类器
        self.load_manager.register(
            'user_classifier',
            factory=self._create_user_classifier,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(2),
            dependencies=[]
        )
        
        # Layer 4: 需求分析器
        self.load_manager.register(
            'demand_analyzer',
            factory=self._create_demand_analyzer,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(2),
            dependencies=[]
        )
        
        # Layer 5: 策略引擎
        self.load_manager.register(
            'strategy_engine',
            factory=self._create_strategy_engine,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(2),
            dependencies=[]
        )
        
        # Narrative Layer
        self.load_manager.register(
            'narrative_layer',
            factory=self._create_narrative_layer,
            strategy=LoadStrategy.LAZY,
            priority=LoadPriority(3),
            dependencies=[]
        )
        
        logger.info(f"[SomnLoadOptimizer] 已注册 {len(self.MODULE_STRATEGIES)} 个模块")
    
    def _start_preload_strategy(self):
        """启动智能预加载策略"""
        if not hasattr(self.somn, 'config') or not self.somn.config.enable_preload:
            logger.info("[SomnLoadOptimizer] 预加载已禁用")
            return
        
        # 遍历所有模块，启动定时预加载
        for module_name, strategy in self.MODULE_STRATEGIES.items():
            if strategy.get('preload_after'):
                delay = strategy['preload_after']
                self._schedule_preload(module_name, delay)
        
        logger.info("[SomnLoadOptimizer] 预加载策略已启动")
    
    def _schedule_preload(self, module_name: str, delay: float):
        """安排定时预加载"""
        def _preload_task():
            try:
                logger.info(f"[SomnLoadOptimizer] 预加载: {module_name}")
                self.load_manager.preload_now([module_name])
            except Exception as e:
                logger.warning(f"[SomnLoadOptimizer] 预加载失败 {module_name}: {e}")
        
        timer = threading.Timer(delay, _preload_task)
        timer.daemon = True
        timer.start()
        self._preload_timers[module_name] = timer
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # 工厂方法 - 创建各模块实例
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _create_tool_registry(self):
        """创建工具注册表"""
        from src.tool_registry import ToolRegistry
        return ToolRegistry()
    
    def _create_llm_service(self):
        """创建 LLM 服务"""
        from src.tool_layer.llm_service import LLMService
        return LLMService()
    
    def _create_kg_engine(self):
        """创建知识图谱引擎"""
        from src.knowledge_graph.graph_engine import KnowledgeGraphEngine
        return KnowledgeGraphEngine()
    
    def _create_web_search(self):
        """创建网络搜索"""
        from src.data_layer.web_search import WebSearchEngine
        return WebSearchEngine()
    
    def _create_memory_system(self):
        """创建记忆系统"""
        from src.neural_memory.neural_memory_system_v3 import NeuralMemorySystemV3
        return NeuralMemorySystemV3()
    
    def _create_user_classifier(self):
        """创建用户分类器"""
        from src.ml_engine.classifier import UserClassifier
        return UserClassifier()
    
    def _create_demand_analyzer(self):
        """创建需求分析器"""
        from src.growth_engine.demand_analyzer import DemandAnalyzer
        return DemandAnalyzer()
    
    def _create_strategy_engine(self):
        """创建策略引擎"""
        from src.strategy_engine.strategy_core import StrategyEngine
        return StrategyEngine()
    
    def _create_narrative_layer(self):
        """创建叙事层"""
        from src.intelligence.engines.narrative_intelligence_engine import NarrativeIntelligenceEngine
        return NarrativeIntelligenceEngine()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # 公共接口
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def get_module(self, name: str) -> Any:
        """获取模块实例（通过 GlobalLoadManager）"""
        return self.load_manager.get(name)
    
    def preload_now(self, names: List[str]):
        """立即预加载指定模块"""
        self.load_manager.preload_now(names)
    
    def get_stats(self) -> Dict:
        """获取加载统计"""
        return self.load_manager.get_stats()


# ═══════════════════════════════════════════════════════════════════════════════
# Somn 配置扩展 - 支持加载优化
# ═══════════════════════════════════════════════════════════════════════════════

def patch_somn_config():
    """给 SomnConfig 添加加载优化配置"""
    from somn_core._types import SomnConfig
    
    # 添加新字段（如果不存在）
    if not hasattr(SomnConfig, 'enable_preload'):
        SomnConfig.enable_preload = True
    
    if not hasattr(SomnConfig, 'preload_delay'):
        SomnConfig.preload_delay = 2.0  # 启动后延迟 2 秒开始预加载
    
    if not hasattr(SomnConfig, 'parallel_preload'):
        SomnConfig.parallel_preload = True  # 是否并行预加载
    
    return SomnConfig


# ═══════════════════════════════════════════════════════════════════════════════
# 使用说明
# ═══════════════════════════════════════════════════════════════════════════════

"""
如何在 Somn 中使用加载优化器：

1. 在 Somn.__init__() 中添加：
   ```python
   def __init__(self, config=None):
       self.config = config or SomnConfig()
       self._init_load_optimizer()
   
   def _init_load_optimizer(self):
       from src.core.somn_load_optimizer import SomnLoadOptimizer
       self._load_optimizer = SomnLoadOptimizer(self)
       self._load_optimizer.init()
   ```
   
2. 修改各层 property，使用 self._load_optimizer.get_module()：
   ```python
   @property
   def kg_engine(self):
       return self._load_optimizer.get_module('kg_engine')
   ```
   
3. 启动后将自动按策略预加载高优先级模块

4. 查看加载统计：
   ```python
   stats = self._load_optimizer.get_stats()
   print(stats)
   ```
"""
