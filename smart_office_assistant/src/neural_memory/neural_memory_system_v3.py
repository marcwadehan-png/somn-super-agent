"""
__all__ = [
    'add_memory',
    'adjust_granularity',
    'close',
    'evaluate_richness',
    'get_richness_trend',
    'get_stats',
    'identify_gaps',
    'retrieve_memory',
    'save_all',
]

神经记忆系统 v6.2.0 - 集成版本
Neural Memory System v6.2.0 - Integrated Version

核心集成:
1. 记忆编码系统 - 多模态,细粒度,上下文感知
2. 强化学习系统 - Q-Learning,Deep Q-Network
3. 记忆丰满度系统 - 7维度评估
4. 记忆颗粒度系统 - 8层级管理
5. 神经记忆系统v2 - HNSW索引,三层存储

版本: v3.0
更新: 2026-03-31 23:25
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

# v7.1: 延迟导入重模块 — 避免import时加载50-100ms
try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# v7.1: numpy 延迟导入 — 仅在真正需要向量计算时加载
_np = None
def _get_numpy():
    """延迟导入 numpy（仅首次调用时加载）"""
    global _np
    if _np is None:
        try:
            import numpy as _np_mod
            _np = _np_mod
        except ImportError:
            _np = None
    return _np

# v7.1: 延迟导入路径模块 — 避免模块级依赖
_DATA_DIR = None
def _get_data_dir():
    """延迟获取 DATA_DIR"""
    global _DATA_DIR
    if _DATA_DIR is None:
        try:
            from src.core.paths import DATA_DIR
            _DATA_DIR = DATA_DIR
        except ImportError:
            _DATA_DIR = Path(__file__).parent.parent.parent / "data"
    return _DATA_DIR

# v7.1 FastBoot: 子系统延迟导入 — 避免模块加载时50-200ms开销
# 所有子模块在首次使用时才真正导入，import 本身只需 <1ms

# 延迟导入缓存
_lazy_imports = {}

def _lazy_import_encoding():
    """延迟导入编码子系统（首次使用时加载，含 sentence-transformers 约500-2000ms）"""
    key = 'encoding'
    if key not in _lazy_imports:
        try:
            from src.neural_memory.memory_encoding_system_v3 import (
                MemoryEncoderV3, MemoryEncoding, EncodingContext,
                EncodingGranularity, EncodingModality, EncodingType
            )
            _lazy_imports[key] = {
                'MemoryEncoderV3': MemoryEncoderV3, 'MemoryEncoding': MemoryEncoding,
                'EncodingContext': EncodingContext, 'EncodingGranularity': EncodingGranularity,
                'EncodingModality': EncodingModality, 'EncodingType': EncodingType,
            }
        except ImportError:
            # 后备定义
            from dataclasses import dataclass as _dc_dataclass
            @_dc_dataclass
            class EncodingContext:
                user_id: str = "default"
                session_id: str = "default"
                timestamp: str = ""
                metadata: dict = None
                def __post_init__(self):
                    if self.metadata is None:
                        self.metadata = {}
            _lazy_imports[key] = {
                'MemoryEncoderV3': None, 'MemoryEncoding': None,
                'EncodingContext': EncodingContext, 'EncodingGranularity': None,
                'EncodingModality': None, 'EncodingType': None,
            }
    return _lazy_imports[key]

def _lazy_import_rl():
    """延迟导入强化学习子系统"""
    key = 'rl'
    if key not in _lazy_imports:
        try:
            from src.neural_memory.reinforcement_learning_v3 import (
                ReinforcementLearningSystemV3, LearningState,
                LearningAction, LearningExperience, LearningType
            )
            _lazy_imports[key] = {
                'ReinforcementLearningSystemV3': ReinforcementLearningSystemV3,
                'LearningState': LearningState, 'LearningAction': LearningAction,
                'LearningExperience': LearningExperience, 'LearningType': LearningType,
            }
        except ImportError:
            _lazy_imports[key] = {
                'ReinforcementLearningSystemV3': None,
                'LearningState': None, 'LearningAction': None,
                'LearningExperience': None, 'LearningType': None,
            }
    return _lazy_imports[key]

def _lazy_import_richness():
    """延迟导入丰满度子系统"""
    key = 'richness'
    if key not in _lazy_imports:
        try:
            from src.neural_memory.memory_richness_v3 import (
                MemoryRichnessSystemV3, MemoryRichnessMetrics, MemoryGap
            )
            _lazy_imports[key] = {
                'MemoryRichnessSystemV3': MemoryRichnessSystemV3,
                'MemoryRichnessMetrics': MemoryRichnessMetrics,
                'MemoryGap': MemoryGap,
            }
        except ImportError:
            from dataclasses import dataclass as _dc_dataclass
            @_dc_dataclass
            class MemoryRichnessMetrics:
                completeness: float = 0.0
                depth: float = 0.0
                relevance: float = 0.0
            @_dc_dataclass
            class MemoryGap:
                gap_type: str = ""
                severity: float = 0.0
            _lazy_imports[key] = {
                'MemoryRichnessSystemV3': None,
                'MemoryRichnessMetrics': MemoryRichnessMetrics,
                'MemoryGap': MemoryGap,
            }
    return _lazy_imports[key]

def _lazy_import_granularity():
    """延迟导入颗粒度子系统"""
    key = 'granularity'
    if key not in _lazy_imports:
        try:
            from src.neural_memory.memory_granularity_v3 import (
                MemoryGranularitySystemV3, GranularMemory, GranularityLevel
            )
            _lazy_imports[key] = {
                'MemoryGranularitySystemV3': MemoryGranularitySystemV3,
                'GranularMemory': GranularMemory, 'GranularityLevel': GranularityLevel,
            }
        except ImportError:
            class GranularityLevel(Enum):
                SENTENCE = "sentence"
                PARAGRAPH = "paragraph"
                DOCUMENT = "document"
            class GranularMemory:
                content: str = ""
                level: GranularityLevel = GranularityLevel.SENTENCE
            _lazy_imports[key] = {
                'MemoryGranularitySystemV3': None,
                'GranularMemory': GranularMemory, 'GranularityLevel': GranularityLevel,
            }
    return _lazy_imports[key]

def _lazy_import_v2():
    """延迟导入v2.0核心（保留兼容性）"""
    key = 'v2'
    if key not in _lazy_imports:
        try:
            from .memory_engine_v2 import MemoryEngineV2, Memory, MemoryType, MemoryTier
            _lazy_imports[key] = {
                'MemoryEngineV2': MemoryEngineV2, 'Memory': Memory,
                'MemoryType': MemoryType, 'MemoryTier': MemoryTier,
                'available': True,
            }
        except ImportError as e:
            logger.warning(f"memory_engine_v2 导入失败: {e}")
            _lazy_imports[key] = {'available': False}
    return _lazy_imports[key]

# 模块级兼容变量 — 从延迟导入中提取，首次访问时触发加载
# 注意：这些只在 NeuralMemoryConfig 默认值等场景使用，不影响运行时性能

# GranularityLevel 需要用于 NeuralMemoryConfig 默认值，提前轻量加载
_gl = _lazy_import_granularity()
GranularityLevel = _gl.get('GranularityLevel')

# LearningType 需要用于 NeuralMemoryConfig 默认值，提前轻量加载
_rl = _lazy_import_rl()
LearningType = _rl.get('LearningType')

# 以下变量延迟到首次使用时通过 _lazy_import_*() 获取
MemoryEncoderV3 = None  # 通过 _lazy_import_encoding()['MemoryEncoderV3'] 获取
MemoryEncoding = None
EncodingContext = None
EncodingGranularity = None
EncodingModality = None
EncodingType = None
ReinforcementLearningSystemV3 = None
MemoryRichnessSystemV3 = None
MemoryRichnessMetrics = None
MemoryGap = None
MemoryGranularitySystemV3 = None
GranularMemory = None
MemoryEngineV2 = None
Memory = None
MemoryType = None
MemoryTier = None
MEMORY_V2_AVAILABLE = False  # 运行时通过 _lazy_import_v2()['available'] 获取

class MemoryOperation(Enum):
    """记忆操作类型"""
    ADD = "add"                 # 添加记忆
    RETRIEVE = "retrieve"        # 检索记忆
    UPDATE = "update"             # 更新记忆
    DELETE = "delete"             # 删除记忆
    ENCODE = "encode"             # 编码记忆
    LEARN = "learn"               # 学习
    EVALUATE = "evaluate"         # 评估
    AGGREGATE = "aggregate"       # 聚合
    DECOMPOSE = "decompose"       # 分解

@dataclass
class NeuralMemoryConfig:
    """神经记忆系统配置"""
    # 基础配置
    base_path: str = None
    
    # 编码系统配置
    enable_encoding: bool = True
    embedding_dim: int = 384
    encoding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # 强化学习配置
    enable_rl: bool = True
    rl_learning_type: Optional[Any] = None  # 运行时解析，避免模块级导入失败
    rl_learning_rate: float = 0.001
    rl_epsilon: float = 1.0
    
    # 丰满度配置
    enable_richness: bool = True
    richness_evaluation_interval: int = 100  # 每100次操作评估一次
    
    # 颗粒度配置
    enable_granularity: bool = True
    default_granularity: Optional[Any] = None  # 运行时解析，避免模块级导入失败
    
    # 性能配置
    max_workers: int = 4
    async_enabled: bool = True
    
    # [v22.0] 防内存泄漏配置
    max_operation_history: int = 1000   # 操作历史最大保留条数（FIFO淘汰）
    memory_ttl_seconds: float = 0       # 记忆TTL(秒), 0=不自动过期
    max_total_memories: int = 0         # 最大记忆总数, 0=无限制
    
    # v2.0兼容性
    enable_v2_compatibility: bool = True
    
    def __post_init__(self):
        """运行时解析枚举默认值，避免模块级导入失败"""
        # 解析 rl_learning_type
        if self.rl_learning_type is None:
            _rl = _lazy_import_rl()
            lt = _rl.get('LearningType')
            self.rl_learning_type = lt.DEEP_Q_NETWORK if lt else None
        
        # 解析 default_granularity
        if self.default_granularity is None:
            _gl = _lazy_import_granularity()
            gl = _gl.get('GranularityLevel')
            self.default_granularity = gl.SENTENCE if gl else None


@dataclass
class MemoryOperationResult:
    """记忆操作结果"""
    operation: MemoryOperation
    success: bool
    result_data: Any = None
    error_message: str = ""
    
    # 性能metrics
    execution_time: float = 0.0
    encoding_time: float = 0.0
    rl_learning_time: float = 0.0
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # 时间信息
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class NeuralMemorySystemV3:
    """
    神经记忆系统v3.0 - 集成版本
    
    核心集成:
    1. 记忆编码系统 - 多模态,细粒度,上下文感知
    2. 强化学习系统 - 基于反馈优化
    3. 记忆丰满度系统 - 7维度评估
    4. 记忆颗粒度系统 - 8层级管理
    5. 神经记忆系统v2 - 高性能存储和检索
    
    核心优势:
    - 智能编码: 多模态,细粒度,上下文感知
    - 自主学习: 基于反馈的强化学习
    - 全面评估: 7维度丰满度评估
    - 灵活管理: 8个颗粒度层级
    - 高性能: HNSW索引,三层存储
    """
    
    def __init__(self, config: Optional[NeuralMemoryConfig] = None):
        self.config = config or NeuralMemoryConfig()
        self.base_path = Path(self.config.base_path) if self.config.base_path else _get_data_dir() / "memory"
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # v7.1 FastBoot: 延迟初始化 — 子系统在首次使用时才创建
        self._v3_initialized = False
        self._v2_initialized = False
        self._init_lock = threading.RLock()
        
        # 占位：子系统实例（延迟到 _ensure_initialized 时创建）
        self.encoder = None
        self.rl_system = None
        self.richness_system = None
        self.granularity_system = None
        self.memory_v2 = None
        
        # 线程池（轻量，即时创建）
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_workers)
        
        # 锁
        self.operation_lock = threading.RLock()
        
        # 操作统计
        self.operation_stats = {
            "total_operations": 0,
            "by_operation": {op.value: 0 for op in MemoryOperation},
            "total_encoding_time": 0.0,
            "total_rl_time": 0.0,
            "avg_encoding_time": 0.0,
            "avg_rl_time": 0.0,
            "success_rate": 0.0,
            "total_success": 0
        }
        
        # 操作历史
        self.operation_history: List[MemoryOperationResult] = []
        
        logger.info("神经记忆系统v3.0 FastBoot init完成（子系统延迟加载）")
    
    def _ensure_initialized(self):
        """确保子系统已初始化（线程安全，双重检查锁）"""
        if self._v3_initialized:
            return
        with self._init_lock:
            if self._v3_initialized:
                return
            self._init_v3_components()
            self._init_v2_compatibility()
            self._v3_initialized = True
            self._v2_initialized = True
            logger.info("神经记忆系统v3.0子系统延迟加载完成")
    
    def _init_v3_components(self):
        """initv3.0组件（延迟调用，从 _lazy_imports 获取类）"""
        # 编码系统 — 含 sentence-transformers，最重（500-2000ms）
        if self.config.enable_encoding:
            enc_mod = _lazy_import_encoding()
            EncoderCls = enc_mod.get('MemoryEncoderV3')
            if EncoderCls is not None:
                self.encoder = EncoderCls(
                    model_name=self.config.encoding_model,
                    embedding_dim=self.config.embedding_dim,
                    base_path=str(self.base_path / "encodings")
                )
            else:
                self.encoder = None
        else:
            self.encoder = None
        
        # 强化学习系统
        if self.config.enable_rl:
            rl_mod = _lazy_import_rl()
            RLCls = rl_mod.get('ReinforcementLearningSystemV3')
            if RLCls is not None:
                self.rl_system = RLCls(
                    learning_type=self.config.rl_learning_type,
                    learning_rate=self.config.rl_learning_rate,
                    epsilon=self.config.rl_epsilon,
                    base_path=str(self.base_path / "reinforcement_learning")
                )
            else:
                self.rl_system = None
        else:
            self.rl_system = None
        
        # 丰满度系统
        if self.config.enable_richness:
            rich_mod = _lazy_import_richness()
            RichCls = rich_mod.get('MemoryRichnessSystemV3')
            if RichCls is not None:
                self.richness_system = RichCls(
                    base_path=str(self.base_path / "richness")
                )
            else:
                self.richness_system = None
        else:
            self.richness_system = None
        
        # 颗粒度系统
        if self.config.enable_granularity:
            gran_mod = _lazy_import_granularity()
            GranCls = gran_mod.get('MemoryGranularitySystemV3')
            if GranCls is not None:
                self.granularity_system = GranCls(
                    base_path=str(self.base_path / "granularity")
                )
            else:
                self.granularity_system = None
        else:
            self.granularity_system = None
    
    def _init_v2_compatibility(self):
        """initv2.0兼容层（延迟调用）"""
        if self.config.enable_v2_compatibility:
            v2_mod = _lazy_import_v2()
            if v2_mod.get('available', False):
                try:
                    MemoryEngineV2Cls = v2_mod['MemoryEngineV2']
                    self.memory_v2 = MemoryEngineV2Cls(
                        base_path=str(self.base_path / "memory_v2")
                    )
                    logger.info("v2.0兼容层init成功")
                except Exception as e:
                    logger.warning(f"v2.0兼容层init失败: {e}")
                    self.memory_v2 = None
            else:
                self.memory_v2 = None
        else:
            self.memory_v2 = None
    
    async def add_memory(self,
                        content: str,
                        context=None,
                        encode: bool = True,
                        granularize: bool = True) -> MemoryOperationResult:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            context: 编码上下文
            encode: 是否编码
            granularize: 是否颗粒化
        
        Returns:
            MemoryOperationResult: 操作结果
        """
        self._ensure_initialized()
        # 延迟获取 EncodingContext 默认值
        if context is None:
            enc_mod = _lazy_import_encoding()
            ContextCls = enc_mod.get('EncodingContext')
            if ContextCls is not None:
                context = ContextCls()
        
        start_time = datetime.now()
        
        try:
            # 编码
            encoding = None
            encoding_time = 0.0
            
            if encode and self.encoder:
                encode_start = datetime.now()
                # 延迟获取 EncodingGranularity / EncodingModality
                _eg = _lazy_import_encoding().get('EncodingGranularity')
                _em = _lazy_import_encoding().get('EncodingModality')
                gran_arg = _eg.MULTI if (_eg and granularize) else (_eg.DOCUMENT if _eg else None)
                mod_arg = _em.TEXT if _em else None
                encoding = self.encoder.encode(
                    content=content,
                    context=context,
                    granularity=gran_arg,
                    modality=mod_arg
                )
                encoding_time = (datetime.now() - encode_start).total_seconds()
            
            # 颗粒化
            granular_memories = []
            granularity_time = 0.0
            
            if granularize and self.granularity_system:
                granular_start = datetime.now()
                
                suggested_level = self.granularity_system.suggest_granularity(
                    content, task_type=context.task_type
                )
                
                granular_memories = self.granularity_system.granularize_content(
                    content,
                    suggested_level,
                    parent_id=encoding.id if encoding else None
                )
                
                granularity_time = (datetime.now() - granular_start).total_seconds()
            
            # 添加到v2.0系统(如果启用)
            v2_success = False
            if self.memory_v2:
                v2_memory = Memory(
                    id=encoding.id if encoding else f"mem_{datetime.now().timestamp()}",
                    content=content,
                    memory_type=MemoryType.SEMANTIC,
                    tier=MemoryTier.WARM,
                    importance=context.priority / 10.0,
                    confidence=encoding.confidence if encoding else 0.8,
                    context=context.metadata
                )
                self.memory_v2.add(v2_memory)
                v2_success = True
            
            # 强化学习:添加经验
            rl_time = 0.0
            if self.rl_system and encoding:
                rl_start = datetime.now()
                
                state = LearningState(
                    state_id=f"state_add_{datetime.now().timestamp()}",
                    state_vector=encoding.encoded_vectors.get('document', []),
                    description="添加记忆状态",
                    context=context.__dict__
                )
                
                action = LearningAction(
                    action_id=f"action_add_{datetime.now().timestamp()}",
                    action_vector=[1.0],  # 添加动作
                    description="添加记忆",
                    action_type="add_memory"
                )
                
                experience = LearningExperience(
                    experience_id=f"exp_add_{datetime.now().timestamp()}",
                    state=state,
                    action=action,
                    reward=0.5,  # 初始奖励
                    next_state=None,
                    done=True
                )
                
                self.rl_system.add_experience(experience)
                self.rl_system.learn()
                
                rl_time = (datetime.now() - rl_start).total_seconds()
            
            # 计算执行时间
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # 创建结果
            result = MemoryOperationResult(
                operation=MemoryOperation.ADD,
                success=True,
                result_data={
                    'encoding_id': encoding.id if encoding else None,
                    'granular_count': len(granular_memories),
                    'v2_success': v2_success
                },
                encoding_time=encoding_time,
                rl_learning_time=rl_time,
                execution_time=execution_time,
                metadata={
                    'suggested_granularity': self.granularity_system.suggest_granularity(content, context.task_type).name if self.granularity_system else None,
                    'encoding_quality': encoding.quality_score if encoding else None
                }
            )
            
            # 更新统计
            self._update_stats(result)
            
            # 保存编码
            if encoding and self.encoder:
                self.encoder.save_encoding(encoding)
            
            return result
            
        except Exception as e:
            logger.error(f"添加记忆失败: {e}")
            return MemoryOperationResult(
                operation=MemoryOperation.ADD,
                success=False,
                error_message="处理失败",
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def retrieve_memory(self,
                             query: str,
                             context=None,
                             top_k: int = 10,
                             granularity=None) -> MemoryOperationResult:
        """
        检索记忆
        
        Args:
            query: 查询内容
            context: 编码上下文
            top_k: 返回结果数
            granularity: 颗粒度
        
        Returns:
            MemoryOperationResult: 操作结果
        """
        self._ensure_initialized()
        start_time = datetime.now()
        
        try:
            # v2.0检索
            v2_results = []
            if self.memory_v2:
                v2_results = self.memory_v2.retrieve(
                    query=query,
                    top_k=top_k
                )
            
            # 编码查询
            query_encoding = None
            encoding_time = 0.0
            
            if self.encoder:
                encode_start = datetime.now()
                _eg = _lazy_import_encoding().get('EncodingGranularity')
                _em = _lazy_import_encoding().get('EncodingModality')
                gran_arg = _eg.SENTENCE if _eg else None
                mod_arg = _em.TEXT if _em else None
                query_encoding = self.encoder.encode(
                    content=query,
                    context=context,
                    granularity=gran_arg,
                    modality=mod_arg
                )
                encoding_time = (datetime.now() - encode_start).total_seconds()
            
            # 颗粒度检索
            granularity_results = []
            if self.granularity_system and granularity:
                # 按指定颗粒度检索
                level_memories = self.granularity_system.level_index.get(granularity, [])
                
                for mem_id in level_memories[:top_k]:
                    memory = self.granularity_system.memories.get(mem_id)
                    if memory:
                        granularity_results.append({
                            'id': memory.id,
                            'content': memory.content,
                            'level': memory.level.name,
                            'depth': memory.depth
                        })
            
            # 强化学习:选择检索动作
            rl_time = 0.0
            if self.rl_system and query_encoding:
                rl_start = datetime.now()
                
                state = LearningState(
                    state_id=f"state_retrieve_{datetime.now().timestamp()}",
                    state_vector=query_encoding.encoded_vectors.get('document', []),
                    description="检索记忆状态",
                    context=context.__dict__
                )
                
                action = self.rl_system.choose_action(state, training=False)
                
                # 添加反馈
                self.rl_system.add_feedback(
                    query_encoding.id if query_encoding else "",
                    {
                        'retrieval_relevance': 0.8,
                        'user_satisfaction': 0.0,  # 等待用户反馈
                        'task_success': True
                    }
                )
                
                rl_time = (datetime.now() - rl_start).total_seconds()
            
            # 合并结果
            results = []
            
            # v2.0结果
            for memory in v2_results:
                results.append({
                    'source': 'v2',
                    'id': memory.id,
                    'content': memory.content,
                    'similarity': memory.confidence
                })
            
            # 颗粒度结果
            results.extend(granularity_results)
            
            # 计算执行时间
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # 创建结果
            result = MemoryOperationResult(
                operation=MemoryOperation.RETRIEVE,
                success=True,
                result_data=results[:top_k],
                encoding_time=encoding_time,
                rl_learning_time=rl_time,
                execution_time=execution_time,
                metadata={
                    'query_encoded': query_encoding.id if query_encoding else None,
                    'granularity_used': granularity.name if granularity else None
                }
            )
            
            # 更新统计
            self._update_stats(result)
            
            return result
            
        except Exception as e:
            logger.error(f"检索记忆失败: {e}")
            return MemoryOperationResult(
                operation=MemoryOperation.RETRIEVE,
                success=False,
                error_message="处理失败",
                execution_time=(datetime.now() - start_time).total_seconds()
            )

    async def search_memory(
        self,
        query: str,
        top_k: int = 10,
        memory_tier: str = "all"
    ) -> List[Dict[str, Any]]:
        """
        简化版记忆搜索（不需要手动创建 context）

        Args:
            query: 查询内容
            top_k: 返回结果数
            memory_tier: 记忆层级 ("all", "eternal", "warm", "working")

        Returns:
            记忆列表
        """
        self._ensure_initialized()
        # 创建默认上下文（延迟获取 EncodingContext）
        enc_mod = _lazy_import_encoding()
        ContextCls = enc_mod.get('EncodingContext')
        if ContextCls is not None:
            context = ContextCls(
                user_id="neural_memory",
                session_id="search",
                timestamp=datetime.now().isoformat()
            )
        else:
            context = None

        # 调用原有 retrieve_memory
        result = await self.retrieve_memory(
            query=query,
            context=context,
            top_k=top_k
        )

        if result.success:
            return result.memories or []
        else:
            # fallback: 使用 v2 搜索
            if self.memory_v2:
                v2_results = self.memory_v2.retrieve(query=query, top_k=top_k)
                return [
                    {
                        "id": r.record.id,
                        "content": r.record.content,
                        "title": r.record.title,
                        "score": r.similarity,
                        "source": "v2"
                    }
                    for r in v2_results
                ]
            return []

    def evaluate_richness(self,
                           memories: List[Any],
                           domain: str = "general"):
        """
        评估记忆丰满度
        
        Args:
            memories: 记忆列表
            domain: 领域
        
        Returns:
            MemoryRichnessMetrics: 丰满度metrics
        """
        self._ensure_initialized()
        if not self.richness_system:
            logger.warning("丰满度系统未启用")
            return None
        
        return self.richness_system.evaluate_richness(memories, domain)
    
    def get_richness_trend(self, days: int = 30) -> Dict[str, Any]:
        """get丰满度趋势"""
        self._ensure_initialized()
        if not self.richness_system:
            return {'message': '丰满度系统未启用'}
        
        return self.richness_system.get_trend(days)
    
    def identify_gaps(self,
                       metrics=None,
                       memories: List[Any] = None):
        """recognize记忆缺口"""
        self._ensure_initialized()
        if not self.richness_system:
            return []
        
        return self.richness_system.identify_gaps(metrics, memories)
    
    def adjust_granularity(self,
                            memory_id: str,
                            target_level=None):
        """
        调整记忆颗粒度
        
        Args:
            memory_id: 记忆ID
            target_level: 目标级别
        
        Returns:
            GranularMemory: 调整后的记忆
        """
        self._ensure_initialized()
        if not self.granularity_system:
            logger.warning("颗粒度系统未启用")
            return None
        
        memory = self.granularity_system.memories.get(memory_id)
        if not memory:
            logger.warning(f"记忆不存在: {memory_id}")
            return None
        
        if target_level > memory.level:
            # 聚合
            return self.granularity_system.aggregate_memory(memory_id, target_level)
        else:
            # 分解
            decomposed = self.granularity_system.decompose_memory(memory_id, target_level)
            return decomposed[0] if decomposed else None
    
    def _update_stats(self, result: MemoryOperationResult):
        """更新操作统计"""
        with self.operation_lock:
            self.operation_stats["total_operations"] += 1
            self.operation_stats["by_operation"][result.operation.value] += 1
            
            if result.success:
                self.operation_stats["total_success"] += 1
                self.operation_stats["total_encoding_time"] += result.encoding_time
                self.operation_stats["total_rl_time"] += result.rl_learning_time
            
            # 更新平均时间
            total = self.operation_stats["total_operations"]
            if total > 0:
                self.operation_stats["avg_encoding_time"] = (
                    self.operation_stats["total_encoding_time"] / total
                )
                self.operation_stats["avg_rl_time"] = (
                    self.operation_stats["total_rl_time"] / total
                )
                self.operation_stats["success_rate"] = (
                    self.operation_stats["total_success"] / total
                )
        
        # 添加到历史
        self.operation_history.append(result)
        # [v22.0] 使用配置的容量上限，默认1000条（原硬编码10000）
        max_hist = self.config.max_operation_history or 1000
        if len(self.operation_history) > max_hist:
            keep = max_hist // 2
            self.operation_history = self.operation_history[-keep:]
    
    def get_stats(self) -> Dict[str, Any]:
        """get统计信息"""
        self._ensure_initialized()
        stats = {
            'operation_stats': self.operation_stats.copy(),
            'v3_components': {
                'encoding': self.encoder is not None,
                'rl': self.rl_system is not None,
                'richness': self.richness_system is not None,
                'granularity': self.granularity_system is not None
            },
            'v2_compatibility': self.memory_v2 is not None
        }
        
        # 各组件统计
        if self.encoder:
            stats['encoding_stats'] = self.encoder.get_stats()
        
        if self.rl_system:
            stats['rl_stats'] = self.rl_system.get_stats()
        
        if self.richness_system:
            stats['richness_stats'] = {
                'evaluations': len(self.richness_system.evaluation_history)
            }
        
        if self.granularity_system:
            stats['granularity_stats'] = self.granularity_system.get_stats()
        
        if self.memory_v2:
            stats['v2_stats'] = self.memory_v2.stats
        
        return stats
    
    def save_all(self):
        """保存所有数据"""
        self._ensure_initialized()
        if self.rl_system:
            self.rl_system.save_model()
        
        if self.encoder:
            pass  # 编码已在添加时保存
        
        if self.richness_system:
            # 保存最近一次评估
            if self.richness_system.evaluation_history:
                self.richness_system.save_evaluation(
                    self.richness_system.evaluation_history[-1]
                )
        
        if self.granularity_system:
            pass  # 颗粒化记忆已在添加时保存
        
        if self.memory_v2:
            pass  # v2.0自动保存
        
        logger.info("所有数据已保存")
    
    def close(self):
        """关闭系统"""
        self.save_all()
        
        if self.executor:
            self.executor.shutdown(wait=True)
        
        logger.info("神经记忆系统v3.0已关闭")

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

# 向后兼容别名
NeuralMemorySystem = NeuralMemorySystemV3
