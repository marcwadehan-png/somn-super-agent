# -*- coding: utf-8 -*-
"""
NeuralMemory v7.0 - 神经网络执行层
=====================================

[品牌定位]
NeuralExecutor 是 NeuralMemory 的执行核心，
负责记忆存储/检索、生命周期管理、藏书阁同步、学习强化等具体操作。
不参与策略决策，只执行策略层（DigitalStrategy）的委托。

[架构角色]
  DigitalStrategy (策略层)
      │
      │ 委托调用
      ▼
  NeuralExecutor (执行层) ← 本文件
      │
      ├──► NeuralMemorySystemV3  — 向量存储/检索
      ├──► MemoryLifecycleManager — 生命周期管理
      ├──► MemoryLibraryBridge  — 藏书阁同步
      ├──► LearningPipeline   — 学习流水线
      └──► 各Engine            — 编码/推理/学习/验证

[快速加载 - v7.0]
- 执行层懒加载: NeuralMemorySystemV3/各Engine首次使用时才初始化
- 加载时间: <1ms (不含实际执行)

版本: v7.0.0
更新: 2026-04-30
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor

if TYPE_CHECKING:
    from .digital_strategy import StrategyConfig

logger = logging.getLogger("NeuralMemory.NeuralExecutor")


# ═══════════════════════════════════════════════════════════════
#  执行层配置
# ═══════════════════════════════════════════════════════════════

@dataclass
class ExecutorConfig:
    """执行层配置"""
    # 向量存储
    encoding_dim: int = 384
    max_workers: int = 4
    
    # 生命周期
    memory_ttl_hours: int = 24 * 7  # 默认7天
    auto_decay_enabled: bool = True
    
    # 藏书阁同步
    library_sync_enabled: bool = True
    library_sync_interval_minutes: int = 30
    auto_sync_threshold: float = 0.7
    
    # 学习流水线
    learning_enabled: bool = True
    replay_buffer_size: int = 1000


# ═══════════════════════════════════════════════════════════════
#  执行结果
# ═══════════════════════════════════════════════════════════════

@dataclass
class ExecutorOperation:
    """执行操作记录"""
    operation_id: str
    operation_type: str  # "retrieve", "add", "update", "delete"
    duration_ms: float
    success: bool
    items_processed: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutorHealth:
    """执行层健康状态"""
    score: float  # 0-100
    memory_system_ready: bool
    lifecycle_manager_ready: bool
    library_bridge_ready: bool
    learning_pipeline_ready: bool
    
    total_memories: int = 0
    total_operations: int = 0
    uptime_seconds: float = 0.0
    
    anomalies: List[Dict] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
#  执行层核心
# ═══════════════════════════════════════════════════════════════

class NeuralExecutor:
    """
    神经网络执行层 (v7.0)
    
    职责:
    1. 记忆的存储与检索
    2. 记忆生命周期管理
    3. 藏书阁同步
    4. 学习强化流水线
    
    设计原则:
    - 不参与策略决策
    - 只执行策略层的委托
    - 所有操作可追踪
    """

    _instance: Optional['NeuralExecutor'] = None
    _lock = threading.Lock()

    def __init__(self, config: Optional[ExecutorConfig] = None):
        self.config = config or ExecutorConfig()
        self._start_time = time.time()
        
        # 子系统 (懒加载)
        self._memory_system = None
        self._lifecycle_manager = None
        self._library_bridge = None
        self._learning_pipeline = None
        
        # 线程池
        self._executor = ThreadPoolExecutor(max_workers=self.config.max_workers)
        
        # 操作统计
        self._operation_count = 0
        self._operation_lock = threading.Lock()
        
        # 同步任务
        self._sync_task: Optional[asyncio.Task] = None
        
        logger.info("[NeuralExecutor] 执行层初始化中...")

    # ═══════════════════════════════════════════════════════════════
    #  子系统懒加载
    # ═══════════════════════════════════════════════════════════════

    @property
    def memory_system(self):
        """获取记忆系统 (懒加载)"""
        if self._memory_system is None:
            with self._lock:
                if self._memory_system is None:
                    try:
                        from .neural_memory_system_v3 import NeuralMemorySystemV3
                        self._memory_system = NeuralMemorySystemV3()
                        logger.info("[NeuralExecutor] 记忆系统已加载")
                    except Exception as e:
                        logger.warning(f"[NeuralExecutor] 记忆系统加载失败: {e}")
                        self._memory_system = None
        return self._memory_system

    @property
    def lifecycle_manager(self):
        """获取生命周期管理 (懒加载)"""
        if self._lifecycle_manager is None:
            with self._lock:
                if self._lifecycle_manager is None:
                    try:
                        from .memory_lifecycle_manager import MemoryLifecycleManager
                        self._lifecycle_manager = MemoryLifecycleManager()
                        logger.info("[NeuralExecutor] 生命周期管理已加载")
                    except Exception as e:
                        logger.warning(f"[NeuralExecutor] 生命周期管理加载失败: {e}")
                        self._lifecycle_manager = None
        return self._lifecycle_manager

    @property
    def library_bridge(self):
        """获取藏书阁桥接 (懒加载)"""
        if self._library_bridge is None:
            with self._lock:
                if self._library_bridge is None:
                    try:
                        from ..digital_brain.digital_brain_integration import MemoryLibraryBridge
                        self._library_bridge = MemoryLibraryBridge()
                        logger.info("[NeuralExecutor] 藏书阁桥接已加载")
                    except Exception as e:
                        logger.warning(f"[NeuralExecutor] 藏书阁桥接加载失败: {e}")
                        self._library_bridge = None
        return self._library_bridge

    @property
    def learning_pipeline(self):
        """获取学习流水线 (懒加载)"""
        if self._learning_pipeline is None:
            with self._lock:
                if self._learning_pipeline is None:
                    try:
                        from .learning_pipeline import LearningPipeline
                        self._learning_pipeline = LearningPipeline()
                        logger.info("[NeuralExecutor] 学习流水线已加载")
                    except Exception as e:
                        logger.warning(f"[NeuralExecutor] 学习流水线加载失败: {e}")
                        self._learning_pipeline = None
        return self._learning_pipeline

    # ═══════════════════════════════════════════════════════════════
    #  核心执行接口
    # ═══════════════════════════════════════════════════════════════

    async def retrieve(
        self,
        query: str,
        top_k: int = 10,
        context: Optional[Dict] = None
    ) -> List[Dict]:
        """
        检索记忆 (委托执行)
        
        Args:
            query: 查询内容
            top_k: 返回数量
            context: 上下文
            
        Returns:
            List[Dict]: 记忆列表
        """
        try:
            ms = self.memory_system
            if ms is None:
                return []
            
            # 调用记忆系统检索 (async方法，直接await)
            result = await ms.retrieve_memory(query=query, context=context or {}, top_k=top_k)
            
            # 提取结果数据
            if hasattr(result, 'result_data'):
                records = result.result_data
            elif isinstance(result, list):
                records = result
            else:
                records = []
            
            self._record_operation("retrieve", True, len(records))
            
            return records
            
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 记忆检索失败: {e}")
            self._record_operation("retrieve", False, 0)
            return []

    async def add(
        self,
        content: str,
        query: str = "",
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        添加记忆 (委托执行)
        
        Args:
            content: 记忆内容
            query: 原始查询 (用于context构建)
            metadata: 元数据 (用于context.metadata)
        
        Returns:
            bool: 是否成功
        """
        try:
            ms = self.memory_system
            if ms is None:
                return False
            
            # 构建context对象 (与NeuralMemorySystemV3.add_memory签名对齐)
            from .encoding_types import EncodingContext
            context = EncodingContext(
                user_id="neural_executor",
                session_id=f"session_{int(time.time())}",
                task_type="memory_add"
            )
            if metadata:
                context.metadata = metadata
            
            # 调用记忆系统添加 (使用正确的签名: content, context, encode, granularize)
            # add_memory是async方法，直接await即可
            result = await ms.add_memory(
                content=content,
                context=context,
                encode=True,
                granularize=True
            )
            
            success = getattr(result, 'success', True) if result else True
            self._record_operation("add", success, 1)
            
            # 触发生命周期管理
            if success and self.lifecycle_manager:
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        self._executor,
                        lambda: self.lifecycle_manager.record_access(content)
                    )
                except Exception:
                    pass
            
            return success
            
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 记忆添加失败: {e}")
            self._record_operation("add", False, 0)
            return False

    async def update(
        self,
        memory_id: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """更新记忆"""
        try:
            ms = self.memory_system
            if ms is None:
                return False
            
            result = await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: ms.update_memory(
                    memory_id=memory_id,
                    content=content,
                    metadata=metadata or {}
                )
            )
            
            success = getattr(result, 'success', True) if result else True
            self._record_operation("update", success, 1)
            return success
            
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 记忆更新失败: {e}")
            self._record_operation("update", False, 0)
            return False

    async def delete(self, memory_id: str) -> bool:
        """删除记忆"""
        try:
            ms = self.memory_system
            if ms is None:
                return False
            
            result = await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: ms.delete_memory(memory_id=memory_id)
            )
            
            success = getattr(result, 'success', True) if result else True
            self._record_operation("delete", success, 1)
            return success
            
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 记忆删除失败: {e}")
            self._record_operation("delete", False, 0)
            return False

    async def record_operation(self, operation_type: str) -> Dict:
        """记录操作"""
        op = ExecutorOperation(
            operation_id=f"op_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            operation_type=operation_type,
            duration_ms=0.0,
            success=True
        )
        return {"operation_id": op.operation_id, "operation_type": operation_type}

    # ═══════════════════════════════════════════════════════════════
    #  生命周期管理
    # ═══════════════════════════════════════════════════════════════

    async def get_lifecycle_report(self) -> Optional[Dict]:
        """获取生命周期报告"""
        lm = self.lifecycle_manager
        if lm is None:
            return None
        
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: lm.get_knowledge_health()
            )
            return result
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 生命周期报告获取失败: {e}")
            return None

    async def trigger_decay(self) -> bool:
        """触发记忆衰减"""
        lm = self.lifecycle_manager
        if lm is None:
            return False
        
        try:
            await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: lm.trigger_decay() if hasattr(lm, 'trigger_decay') else None
            )
            return True
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 记忆衰减失败: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════
    #  藏书阁同步
    # ═══════════════════════════════════════════════════════════════

    async def sync_to_library(self) -> int:
        """同步记忆到藏书阁"""
        lb = self.library_bridge
        if lb is None:
            return 0
        
        try:
            count = await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: lb.sync_to_library() if hasattr(lb, 'sync_to_library') else 0
            )
            return count
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 藏书阁同步失败: {e}")
            return 0

    async def load_from_library(self, query: str) -> List[Dict]:
        """从藏书阁加载记忆"""
        lb = self.library_bridge
        if lb is None:
            return []
        
        try:
            results = await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: lb.load_from_library(query) if hasattr(lb, 'load_from_library') else []
            )
            return results
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 藏书阁加载失败: {e}")
            return []

    # ═══════════════════════════════════════════════════════════════
    #  学习流水线
    # ═══════════════════════════════════════════════════════════════

    async def run_learning(self, content: str, context: Optional[Dict] = None) -> Optional[Dict]:
        """运行学习流水线"""
        lp = self.learning_pipeline
        if lp is None:
            return None
        
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: lp.run(content, context) if hasattr(lp, 'run') else None
            )
            return result
        except Exception as e:
            logger.warning(f"[NeuralExecutor] 学习流水线失败: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════
    #  健康检查
    # ═══════════════════════════════════════════════════════════════

    async def get_health(self) -> Dict:
        """获取执行层健康状态"""
        total = self._operation_count
        
        # 计算各子系统状态
        memory_ready = self._memory_system is not None
        lifecycle_ready = self._lifecycle_manager is not None
        library_ready = self._library_bridge is not None
        learning_ready = self._learning_pipeline is not None
        
        # 基础分
        base_score = 60.0
        if memory_ready:
            base_score += 20.0
        if lifecycle_ready:
            base_score += 10.0
        if library_ready:
            base_score += 5.0
        if learning_ready:
            base_score += 5.0
        
        score = min(100.0, base_score)
        
        return {
            "score": score,
            "memory_system_ready": memory_ready,
            "lifecycle_manager_ready": lifecycle_ready,
            "library_bridge_ready": library_ready,
            "learning_pipeline_ready": learning_ready,
            "total_operations": total,
            "uptime_seconds": time.time() - self._start_time
        }

    # ═══════════════════════════════════════════════════════════════
    #  统计与工具
    # ═══════════════════════════════════════════════════════════════

    def _record_operation(self, operation_type: str, success: bool, items: int):
        """记录操作统计"""
        with self._operation_lock:
            self._operation_count += 1

    def get_stats(self) -> Dict:
        """获取执行统计"""
        return {
            "total_operations": self._operation_count,
            "uptime_seconds": time.time() - self._start_time,
            "subsystems_loaded": {
                "memory_system": self._memory_system is not None,
                "lifecycle_manager": self._lifecycle_manager is not None,
                "library_bridge": self._library_bridge is not None,
                "learning_pipeline": self._learning_pipeline is not None,
            }
        }

    def shutdown(self):
        """关闭执行层"""
        self._executor.shutdown(wait=False)
        logger.info("[NeuralExecutor] 执行层已关闭")
