# -*- coding: utf-8 -*-
"""
NeuralMemory v7.0 - 统一神经记忆架构
======================================
v7.0.1 升级：集成 Ecology + ML Engine 能力
  - 新增资源感知的记忆管理（内存/存储/Token 优化分配）
  - 新增健康状态监控（记忆系统的健康度评估）
  - 新增预测能力（预测记忆访问频率，优化预加载）
"""

from __future__ import annotations

# Ecology + ML Engine 集成 (v7.0.1)
# 将 knowledge_cells/ecology_ml_bridge.py 的能力接入 NeuralMemory
import sys
from pathlib import Path

# 正确计算knowledge_cells路径
_kb_path = Path(__file__).resolve().parent.parent / "knowledge_cells"
# 使用insert(0)确保优先搜索
if str(_kb_path) not in sys.path:
    sys.path.insert(0, str(_kb_path))

# 使用try-except包装可选导入，允许降级运行
try:
    from ecology_ml_bridge import (
        MemoryResourceOptimizer,
        get_memory_optimizer,
        get_memory_health,
        predict_memory_access,
        enhance_neural_memory_with_ecology,
    )
    _ECOLOGY_AVAILABLE = True
except ImportError:
    # 降级：创建空实现
    class MemoryResourceOptimizer:
        pass
    get_memory_optimizer = None
    get_memory_health = None
    predict_memory_access = None
    enhance_neural_memory_with_ecology = None
    _ECOLOGY_AVAILABLE = False

import asyncio
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger("NeuralMemory")


# ═══════════════════════════════════════════════════════════════
#  统一配置
# ═══════════════════════════════════════════════════════════════

@dataclass
class NeuralMemoryConfig:
    """NeuralMemory v7.0 统一配置"""
    # 策略层配置
    enable_strategy: bool = True
    enable_wisdom_dispatch: bool = True
    enable_llm_enhancement: bool = True
    enable_autonomous_evolution: bool = True
    
    # 执行层配置
    encoding_dim: int = 384
    max_workers: int = 4
    memory_ttl_hours: int = 24 * 7
    
    # 藏书阁同步
    library_sync_enabled: bool = True
    library_sync_interval_minutes: int = 30
    
    # 学习流水线
    learning_enabled: bool = True
    replay_buffer_size: int = 1000


# ═══════════════════════════════════════════════════════════════
#  统一数据类型
# ═══════════════════════════════════════════════════════════════

@dataclass
class MemoryRecord:
    """统一记忆记录"""
    id: str
    title: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    score: float = 0.0
    grade: str = ""
    tier: str = ""
    source: str = ""
    created_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "score": self.score,
            "grade": self.grade,
            "tier": self.tier,
            "source": self.source,
            "memory_type": self.metadata.get("memory_type", ""),
        }


@dataclass
class ThinkResult:
    """策略思考结果 (v7.0)"""
    thought_id: str
    content: str
    source: str
    confidence: float
    processing_time_ms: float
    problem_type: str = ""
    school: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════
#  单例管理
# ═══════════════════════════════════════════════════════════════

_v7_instance: Optional['NeuralMemory'] = None
_v7_lock = threading.Lock()


def get_neural_memory(config: Optional[NeuralMemoryConfig] = None) -> 'NeuralMemory':
    """获取NeuralMemory单例 (v7.0)"""
    global _v7_instance
    if _v7_instance is None:
        with _v7_lock:
            if _v7_instance is None:
                _v7_instance = NeuralMemory(config)
    return _v7_instance


# ═══════════════════════════════════════════════════════════════
#  统一门面
# ═══════════════════════════════════════════════════════════════

class NeuralMemory:
    """
    NeuralMemory v7.0 - 统一神经记忆架构
    
    整合 DigitalStrategy (策略层) + NeuralExecutor (执行层)
    
    使用方式:
        nm = get_neural_memory()
        
        # 方式1: 策略思考 (数字大脑模式)
        result = await nm.think("如何提升用户增长?")
        
        # 方式2: 直接执行
        await nm.add_memory("用户增长策略", query="增长策略")
        memories = await nm.retrieve_memory("增长")
        
        # 方式3: 组合使用
        result = await nm.think("分析市场趋势")
        await nm.sync_to_library()
    """

    _instance: Optional['NeuralMemory'] = None
    _init_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[NeuralMemoryConfig] = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.config = config or NeuralMemoryConfig()
        self._initialized = True
        self._start_time = time.time()
        
        # 初始化执行层 (核心)
        from .neural_executor import NeuralExecutor, ExecutorConfig
        
        executor_cfg = ExecutorConfig(
            encoding_dim=self.config.encoding_dim,
            max_workers=self.config.max_workers,
            memory_ttl_hours=self.config.memory_ttl_hours,
            library_sync_enabled=self.config.library_sync_enabled,
            library_sync_interval_minutes=self.config.library_sync_interval_minutes,
            learning_enabled=self.config.learning_enabled,
            replay_buffer_size=self.config.replay_buffer_size,
        )
        self._executor = NeuralExecutor(executor_cfg)
        
        # 初始化策略层 (可选)
        self._strategy = None
        if self.config.enable_strategy:
            from .digital_strategy import DigitalStrategy, StrategyConfig
            
            strategy_cfg = StrategyConfig(
                enable_wisdom_dispatch=self.config.enable_wisdom_dispatch,
                enable_llm_enhancement=self.config.enable_llm_enhancement,
                enable_autonomous_evolution=self.config.enable_autonomous_evolution,
            )
            self._strategy = DigitalStrategy(strategy_cfg, self._executor)

        # 初始化 Ecology + ML Engine 集成 (v7.0.1)
        try:
            enhance_neural_memory_with_ecology(self)
            # 初始化资源优化器
            optimizer = get_memory_optimizer()
            self._resource_optimizer = optimizer
            logger.info("[NeuralMemory] v7.0.1 Ecology+ML 集成完成!")
        except Exception as e:
            logger.warning(f"[NeuralMemory] Ecology+ML 集成失败: {e}")

        logger.info("[NeuralMemory] v7.0 统一架构初始化完成!")

    # ═══════════════════════════════════════════════════════════════
    #  策略思考入口 (v7.0 新增)
    # ═══════════════════════════════════════════════════════════════

    async def think(self, query: str, context: Optional[Dict] = None) -> ThinkResult:
        """策略思考入口 — 数字大脑模式"""
        if not self._strategy:
            # 降级到纯执行模式
            memories = await self._executor.retrieve(query, top_k=10)
            return ThinkResult(
                thought_id=f"fallback_{int(time.time())}",
                content=f"[执行模式] 检索到 {len(memories)} 条相关记忆",
                source="executor",
                confidence=0.5,
                processing_time_ms=0.0,
                problem_type="FALLBACK",
            )
        
        thought = await self._strategy.think(query, context)
        
        return ThinkResult(
            thought_id=thought.thought_id,
            content=thought.content,
            source=thought.source,
            confidence=thought.confidence,
            processing_time_ms=thought.processing_time_ms,
            problem_type=getattr(thought.metadata.get("problem_type", ""), 'name', str(thought.metadata.get("problem_type", ""))),
            school=thought.metadata.get("wisdom", {}).get("school", ""),
            metadata=thought.metadata,
        )

    # ═══════════════════════════════════════════════════════════════
    #  执行层接口 (兼容原有API)
    # ═══════════════════════════════════════════════════════════════

    async def add_memory(
        self,
        content: str,
        query: str = "",
        metadata: Optional[Dict] = None
    ) -> bool:
        """添加记忆 (执行层)"""
        return await self._executor.add(content, query, metadata)

    async def retrieve_memory(
        self,
        query: str,
        context: Optional[Dict] = None,
        top_k: int = 10
    ) -> List[MemoryRecord]:
        """检索记忆 (执行层)"""
        results = await self._executor.retrieve(query, top_k, context)
        
        records = []
        for r in results:
            if isinstance(r, dict):
                records.append(MemoryRecord(
                    id=r.get("id", ""),
                    title=r.get("title", ""),
                    content=r.get("content", ""),
                    tags=r.get("tags", []),
                    score=r.get("score", 0.0),
                    grade=r.get("grade", ""),
                    tier=r.get("tier", ""),
                    source=r.get("source", ""),
                    metadata=r.get("metadata", {}),
                ))
            elif hasattr(r, 'id'):
                records.append(r)
        
        return records

    async def update_memory(
        self,
        memory_id: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """更新记忆"""
        return await self._executor.update(memory_id, content, metadata)

    async def delete_memory(self, memory_id: str) -> bool:
        """删除记忆"""
        return await self._executor.delete(memory_id)

    # ═══════════════════════════════════════════════════════════════
    #  藏书阁同步
    # ═══════════════════════════════════════════════════════════════

    async def sync_to_library(self) -> int:
        """同步到藏书阁"""
        return await self._executor.sync_to_library()

    async def load_from_library(self, query: str) -> List[Dict]:
        """从藏书阁加载"""
        return await self._executor.load_from_library(query)

    # ═══════════════════════════════════════════════════════════════
    #  学习流水线
    # ═══════════════════════════════════════════════════════════════

    async def run_learning(self, content: str, context: Optional[Dict] = None) -> Optional[Dict]:
        """运行学习流水线"""
        return await self._executor.run_learning(content, context)

    # ═══════════════════════════════════════════════════════════════
    #  健康检查
    # ═══════════════════════════════════════════════════════════════

    async def get_health(self) -> Dict:
        """获取健康状态"""
        executor_health = await self._executor.get_health()

        strategy_health = None
        if self._strategy:
            try:
                h = await self._strategy.get_health()
                strategy_health = {
                    "score": h.overall_score,
                    "state": h.strategy_health,
                    "active_thoughts": h.active_thoughts,
                }
            except Exception:
                pass

        # 获取资源健康状态 (v7.0.1 新增)
        resource_health = None
        try:
            resource_health = get_memory_health()
        except Exception as e:
            logger.warning(f"[NeuralMemory] 获取资源健康状态失败: {e}")

        return {
            "version": "v7.0.1",
            "strategy": strategy_health,
            "executor": executor_health,
            "resource": resource_health,  # 新增：Ecology+ML 资源健康
            "subsystem_count": len([k for k, v in executor_health.get("subsystems_loaded", {}).items() if v]),
        }

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "version": "v7.0.0",
            "uptime_seconds": time.time() - self._start_time,
            "executor_stats": self._executor.get_stats(),
            "strategy_enabled": self._strategy is not None,
        }

    # ═══════════════════════════════════════════════════════════════
    #  生命周期
    # ═══════════════════════════════════════════════════════════════

    async def close(self):
        """关闭NeuralMemory"""
        if self._strategy:
            await self._strategy.shutdown()
        self._executor.shutdown()
        logger.info("[NeuralMemory] v7.0 已关闭")

    # ═══════════════════════════════════════════════════════════════
    #  别名
    # ═══════════════════════════════════════════════════════════════

    async def remember(self, content: str, query: str = "") -> bool:
        """remember 是 add_memory 的别名"""
        return await self.add_memory(content, query)

    async def recall(self, query: str, top_k: int = 10) -> List[MemoryRecord]:
        """recall 是 retrieve_memory 的别名"""
        return await self.retrieve_memory(query, top_k=top_k)

    def get_thought_history(self, limit: int = 10) -> List[Any]:
        """获取策略层思维历史"""
        if self._strategy:
            return self._strategy.get_thought_history(limit)
        return []

    def get_evolution_history(self, limit: int = 10) -> List[Any]:
        """获取进化历史"""
        if self._strategy:
            return self._strategy.get_evolution_history(limit)
        return []
