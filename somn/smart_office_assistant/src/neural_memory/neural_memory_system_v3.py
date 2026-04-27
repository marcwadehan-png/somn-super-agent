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

神经记忆系统 v3.0 - 集成版本
Neural Memory System V1.0 - Integrated Version

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
from src.core.paths import DATA_DIR
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
from loguru import logger
import numpy as np

# 导入v3.0组件
try:
    from src.neural_memory.memory_encoding_system_v3 import (
        MemoryEncoderV3,
        MemoryEncoding,
        EncodingContext,
        EncodingGranularity,
        EncodingModality,
        EncodingType
    )
except ImportError:
    # 后备定义
    from dataclasses import dataclass
    @dataclass
    class EncodingContext:
        user_id: str = "default"
        session_id: str = "default"
        timestamp: str = ""
        metadata: dict = None
        def __post_init__(self):
            if self.metadata is None:
                self.metadata = {}
    EncodingGranularity = None
    EncodingModality = None
    EncodingType = None
    MemoryEncoderV3 = None
    MemoryEncoding = None

try:
    from src.neural_memory.reinforcement_learning_v3 import (
        ReinforcementLearningSystemV3,
        LearningState,
        LearningAction,
        LearningExperience,
        LearningType
    )
except ImportError:
    pass

try:
    from src.neural_memory.memory_richness_v3 import (
        MemoryRichnessSystemV3,
        MemoryRichnessMetrics,
        MemoryGap
    )
except ImportError:
    # 占位符类型
    from dataclasses import dataclass
    @dataclass
    class MemoryRichnessMetrics:
        completeness: float = 0.0
        depth: float = 0.0
        relevance: float = 0.0
    @dataclass
    class MemoryGap:
        gap_type: str = ""
        severity: float = 0.0
    MemoryRichnessSystemV3 = None

try:
    from src.neural_memory.memory_granularity_v3 import (
        MemoryGranularitySystemV3,
        GranularMemory,
        GranularityLevel
    )
except ImportError:
    # 占位符类型
    class GranularityLevel(Enum):
        SENTENCE = "sentence"
        PARAGRAPH = "paragraph"
        DOCUMENT = "document"
    class GranularMemory:
        content: str = ""
        level: GranularityLevel = GranularityLevel.SENTENCE
    MemoryGranularitySystemV3 = None

# 导入v2.0核心(保留兼容性)
try:
    from .memory_engine_v2 import MemoryEngineV2, Memory, MemoryType, MemoryTier
    MEMORY_V2_AVAILABLE = True
except ImportError as e:
    logger.warning(f"memory_engine_v2 导入失败: {e}")
    MEMORY_V2_AVAILABLE = False

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
    rl_learning_type: LearningType = LearningType.DEEP_Q_NETWORK
    rl_learning_rate: float = 0.001
    rl_epsilon: float = 1.0
    
    # 丰满度配置
    enable_richness: bool = True
    richness_evaluation_interval: int = 100  # 每100次操作评估一次
    
    # 颗粒度配置
    enable_granularity: bool = True
    default_granularity: GranularityLevel = GranularityLevel.SENTENCE
    
    # 性能配置
    max_workers: int = 4
    async_enabled: bool = True
    
    # [v1.0] 防内存泄漏配置
    max_operation_history: int = 1000   # 操作历史最大保留条数（FIFO淘汰）
    memory_ttl_seconds: float = 0       # 记忆TTL(秒), 0=不自动过期
    max_total_memories: int = 0         # 最大记忆总数, 0=无限制
    
    # v2.0兼容性
    enable_v2_compatibility: bool = True

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
        from src.core.paths import MEMORY_DIR
        self.base_path = Path(self.config.base_path) if self.config.base_path else MEMORY_DIR
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # initv3.0组件
        self._init_v3_components()
        
        # initv2.0兼容层
        self._init_v2_compatibility()
        
        # 线程池
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
        
        logger.info("神经记忆系统v3.0init完成")
        logger.info(f"  编码系统: {'启用' if self.config.enable_encoding else '禁用'}")
        logger.info(f"  强化学习: {'启用' if self.config.enable_rl else '禁用'}")
        logger.info(f"  丰满度系统: {'启用' if self.config.enable_richness else '禁用'}")
        logger.info(f"  颗粒度系统: {'启用' if self.config.enable_granularity else '禁用'}")
        logger.info(f"  v2.0兼容: {'启用' if self.config.enable_v2_compatibility else '禁用'}")
    
    def _init_v3_components(self):
        """initv3.0组件"""
        # 编码系统
        if self.config.enable_encoding:
            self.encoder = MemoryEncoderV3(
                model_name=self.config.encoding_model,
                embedding_dim=self.config.embedding_dim,
                base_path=str(self.base_path / "encodings")
            )
        else:
            self.encoder = None
        
        # 强化学习系统
        if self.config.enable_rl:
            self.rl_system = ReinforcementLearningSystemV3(
                learning_type=self.config.rl_learning_type,
                learning_rate=self.config.rl_learning_rate,
                epsilon=self.config.rl_epsilon,
                base_path=str(self.base_path / "reinforcement_learning")
            )
        else:
            self.rl_system = None
        
        # 丰满度系统
        if self.config.enable_richness and MemoryRichnessSystemV3 is not None:
            self.richness_system = MemoryRichnessSystemV3(
                base_path=str(self.base_path / "richness")
            )
        else:
            self.richness_system = None
        
        # 颗粒度系统
        if self.config.enable_granularity and MemoryGranularitySystemV3 is not None:
            self.granularity_system = MemoryGranularitySystemV3(
                base_path=str(self.base_path / "granularity")
            )
        else:
            self.granularity_system = None
    
    def _init_v2_compatibility(self):
        """initv2.0兼容层"""
        if self.config.enable_v2_compatibility and MEMORY_V2_AVAILABLE:
            try:
                self.memory_v2 = MemoryEngineV2(
                    base_path=str(self.base_path / "memory_v2")
                )
                logger.info("v2.0兼容层init成功")
            except Exception as e:
                logger.warning(f"v2.0兼容层init失败: {e}")
                self.memory_v2 = None
        else:
            self.memory_v2 = None
    
    async def add_memory(self,
                        content: str,
                        context: EncodingContext,
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
        start_time = datetime.now()
        
        try:
            # 编码
            encoding = None
            encoding_time = 0.0
            
            if encode and self.encoder:
                encode_start = datetime.now()
                encoding = self.encoder.encode(
                    content=content,
                    context=context,
                    granularity=EncodingGranularity.MULTI if granularize else EncodingGranularity.DOCUMENT,
                    modality=EncodingModality.TEXT
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
                             context: EncodingContext,
                             top_k: int = 10,
                             granularity: Optional[GranularityLevel] = None) -> MemoryOperationResult:
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
                query_encoding = self.encoder.encode(
                    content=query,
                    context=context,
                    granularity=EncodingGranularity.SENTENCE,
                    modality=EncodingModality.TEXT
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
    
    def evaluate_richness(self,
                           memories: List[Any],
                           domain: str = "general") -> MemoryRichnessMetrics:
        """
        评估记忆丰满度
        
        Args:
            memories: 记忆列表
            domain: 领域
        
        Returns:
            MemoryRichnessMetrics: 丰满度metrics
        """
        if not self.richness_system:
            logger.warning("丰满度系统未启用")
            return None
        
        return self.richness_system.evaluate_richness(memories, domain)
    
    def get_richness_trend(self, days: int = 30) -> Dict[str, Any]:
        """get丰满度趋势"""
        if not self.richness_system:
            return {'message': '丰满度系统未启用'}
        
        return self.richness_system.get_trend(days)
    
    def identify_gaps(self,
                       metrics: MemoryRichnessMetrics,
                       memories: List[Any]) -> List[MemoryGap]:
        """recognize记忆缺口"""
        if not self.richness_system:
            return []
        
        return self.richness_system.identify_gaps(metrics, memories)
    
    def adjust_granularity(self,
                            memory_id: str,
                            target_level: GranularityLevel) -> Optional[GranularMemory]:
        """
        调整记忆颗粒度
        
        Args:
            memory_id: 记忆ID
            target_level: 目标级别
        
        Returns:
            GranularMemory: 调整后的记忆
        """
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
        # [v1.0] 使用配置的容量上限，默认1000条（原硬编码10000）
        max_hist = self.config.max_operation_history or 1000
        if len(self.operation_history) > max_hist:
            keep = max_hist // 2
            self.operation_history = self.operation_history[-keep:]
    
    def get_stats(self) -> Dict[str, Any]:
        """get统计信息"""
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
