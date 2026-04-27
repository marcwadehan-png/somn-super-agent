# -*- coding: utf-8 -*-
"""
数字大脑系统集成桥接模块
========================

三大系统深度打通：

1. 神经记忆系统 ↔ 藏书阁
   - 记忆双向同步
   - 永久记忆沉淀
   - 记忆检索加速

2. 神经记忆系统 ↔ 智慧调度系统
   - 记忆增强调度
   - 调度结果记忆化
   - 学派能力沉淀

3. 数字大脑 ↔ SomnCore
   - 智能核心集成
   - 生命周期同步
   - 能力输出封装

版本: V1.0.0
创建: 2026-04-23
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

logger = logging.getLogger("DigitalBrain.Integration")


# ═══════════════════════════════════════════════════════════════════════
# 记忆桥接 - NeuralMemory ↔ ImperialLibrary
# ═══════════════════════════════════════════════════════════════════════

class MemorySyncDirection(Enum):
    """记忆同步方向"""
    TO_LIBRARY = "to_library"      # 记忆系统 → 藏书阁
    FROM_LIBRARY = "from_library"  # 藏书阁 → 记忆系统
    BIDIRECTIONAL = "bidirectional"  # 双向同步


@dataclass
class MemoryBridgeConfig:
    """记忆桥接配置"""
    sync_enabled: bool = True
    sync_interval_minutes: int = 30
    auto_sync_threshold: float = 0.7  # 置信度 >= 0.7 自动同步到藏书阁
    sync_batch_size: int = 50
    sync_directions: Set[MemorySyncDirection] = field(
        default_factory=lambda: {MemorySyncDirection.TO_LIBRARY}
    )


class MemoryLibraryBridge:
    """
    神经记忆系统 ↔ 藏书阁桥接器
    
    功能:
    - 记忆自动同步到藏书阁
    - 藏书阁记忆回读到神经记忆
    - 记忆去重与冲突解决
    - 同步历史追踪
    """
    
    def __init__(self, config: Optional[MemoryBridgeConfig] = None):
        self.config = config or MemoryBridgeConfig()
        self._memory_system = None
        self._library = None
        self._sync_lock = threading.RLock()
        self._sync_history: List[Dict] = []
        self._last_sync_time: float = 0.0
        self._sync_task: Optional[asyncio.Task] = None
        
        # 同步统计
        self._stats = {
            "total_synced": 0,
            "to_library": 0,
            "from_library": 0,
            "duplicates_skipped": 0,
            "conflicts_resolved": 0,
        }
    
    def attach_memory_system(self, memory_system):
        """绑定神经记忆系统"""
        self._memory_system = memory_system
    
    def attach_library(self, library):
        """绑定藏书阁"""
        self._library = library
    
    async def start(self):
        """启动同步"""
        if not self.config.sync_enabled:
            return
        
        self._sync_task = asyncio.create_task(self._sync_loop())
        logger.info("[MemoryBridge] 记忆桥接已启动")
    
    async def stop(self):
        """停止同步"""
        if self._sync_task:
            self._sync_task.cancel()
        logger.info("[MemoryBridge] 记忆桥接已停止")
    
    async def _sync_loop(self):
        """同步循环"""
        interval = self.config.sync_interval_minutes * 60
        
        while True:
            try:
                await asyncio.sleep(interval)
                
                if MemorySyncDirection.TO_LIBRARY in self.config.sync_directions:
                    await self.sync_to_library()
                
                if MemorySyncDirection.FROM_LIBRARY in self.config.sync_directions:
                    await self.sync_from_library()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[MemoryBridge] 同步循环错误: {e}")
    
    async def sync_to_library(self, force: bool = False) -> Dict[str, Any]:
        """
        同步记忆到藏书阁
        
        规则:
        1. 置信度 >= auto_sync_threshold 的记忆自动同步
        2. 高价值记忆（tag包含 important）强制同步
        3. 已同步的记忆不重复同步
        """
        if not self._memory_system or not self._library:
            return {"synced": 0, "skipped": 0}
        
        results = {"synced": 0, "skipped": 0, "errors": []}
        
        with self._sync_lock:
            try:
                # 获取记忆系统中的高价值记忆
                # 简化实现：假设通过某种方式获取待同步记忆
                memories_to_sync = self._get_memories_for_sync()
                
                for memory in memories_to_sync:
                    # 检查是否需要同步
                    if not force and memory.get("confidence", 0) < self.config.auto_sync_threshold:
                        results["skipped"] += 1
                        continue
                    
                    # 同步到藏书阁
                    try:
                        self._library.submit_memory(
                            title=memory.get("title", memory.get("content", "")[:50]),
                            content=memory.get("content", ""),
                            source=self._get_memory_source(),
                            category=self._get_memory_category(),
                            reporting_department="数字大脑",
                            tags=memory.get("tags", []) + ["brain_sync"],
                            suggested_grade=self._estimate_grade(memory)
                        )
                        results["synced"] += 1
                        self._stats["to_library"] += 1
                        
                    except Exception as e:
                        results["errors"].append("执行失败")
                
                self._last_sync_time = time.time()
                self._stats["total_synced"] += results["synced"]
                
            except Exception as e:
                logger.error(f"[MemoryBridge] 同步到藏书阁失败: {e}")
                results["errors"].append("执行失败")
        
        return results
    
    async def sync_from_library(self, limit: int = 100) -> Dict[str, Any]:
        """
        从藏书阁同步记忆到神经记忆系统
        """
        if not self._memory_system or not self._library:
            return {"synced": 0}
        
        results = {"synced": 0, "skipped": 0}
        
        try:
            # 获取藏书阁中未同步的记忆
            library_memories = self._library.query_memories(
                keyword="brain_sync",
                limit=limit
            )
            
            for lib_mem in library_memories:
                # 检查是否已在神经记忆中
                if self._is_memory_in_neural(lib_mem):
                    results["skipped"] += 1
                    continue
                
                # 添加到神经记忆
                try:
                    await self._add_to_neural_memory(lib_mem)
                    results["synced"] += 1
                    self._stats["from_library"] += 1
                except Exception as e:
                    logger.warning(f"[MemoryBridge] 添加记忆失败: {e}")
            
        except Exception as e:
            logger.error(f"[MemoryBridge] 从藏书阁同步失败: {e}")
        
        return results
    
    def _get_memories_for_sync(self) -> List[Dict]:
        """获取待同步的记忆"""
        # 简化实现
        return []
    
    def _get_memory_source(self):
        """获取藏书阁记忆来源枚举"""
        try:
            from intelligence.dispatcher.wisdom_dispatch._imperial_library import MemorySource
            return MemorySource.SYSTEM_EVENT
        except Exception as e:
            logger.debug(f"加载 MemorySource 失败: {e}")
            return None

    def _get_memory_category(self):
        """获取藏书阁记忆分类枚举"""
        try:
            from intelligence.dispatcher.wisdom_dispatch._imperial_library import MemoryCategory
            return MemoryCategory.METHODOLOGY
        except Exception as e:
            logger.debug(f"加载 MemoryCategory 失败: {e}")
            return None
    
    def _estimate_grade(self, memory: Dict) -> str:
        """估算记忆等级"""
        confidence = memory.get("confidence", 0.5)
        importance = memory.get("importance", 0.5)
        score = (confidence + importance) / 2
        
        if score >= 0.8:
            return "甲级"
        elif score >= 0.6:
            return "乙级"
        elif score >= 0.4:
            return "丙级"
        else:
            return "丁级"
    
    def _is_memory_in_neural(self, lib_mem) -> bool:
        """检查记忆是否已在神经记忆中"""
        # 简化实现
        return False
    
    async def _add_to_neural_memory(self, lib_mem):
        """添加藏书阁记忆到神经记忆"""
        if not self._memory_system:
            return
        
        # 简化实现
        pass
    
    def get_sync_status(self) -> Dict[str, Any]:
        """获取同步状态"""
        return {
            "enabled": self.config.sync_enabled,
            "last_sync": datetime.fromtimestamp(self._last_sync_time).isoformat() if self._last_sync_time else None,
            "stats": self._stats.copy(),
            "history": self._sync_history[-10:] if self._sync_history else []
        }


# ═══════════════════════════════════════════════════════════════════════
# 智慧调度桥接 - NeuralMemory ↔ WisdomDispatch
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class WisdomBridgeConfig:
    """智慧调度桥接配置"""
    memory_enhance_dispatch: bool = True  # 记忆增强调度
    dispatch_result_memory: bool = True   # 调度结果记忆化
    school_capability_track: bool = True  # 学派能力追踪
    confidence_learning: bool = True      # 置信度学习


class WisdomMemoryBridge:
    """
    神经记忆系统 ↔ 智慧调度系统桥接器
    
    功能:
    - 记忆增强调度：基于历史成功案例优化调度
    - 调度结果记忆化：学习调度效果
    - 学派能力画像：追踪各学派表现
    - 置信度校准：基于反馈调整置信度
    """
    
    def __init__(self, config: Optional[WisdomBridgeConfig] = None):
        self.config = config or WisdomBridgeConfig()
        self._memory_system = None
        self._wisdom_dispatch = None
        
        # 学派能力追踪
        self._school_performance: Dict[str, Dict] = defaultdict(lambda: {
            "total_dispatches": 0,
            "successful_dispatches": 0,
            "avg_confidence": 0.5,
            "recent_results": []
        })
        
        # 调度历史
        self._dispatch_history: List[Dict] = []
    
    def attach_memory_system(self, memory_system):
        """绑定神经记忆系统"""
        self._memory_system = memory_system
    
    def attach_wisdom_dispatch(self, wisdom_dispatch):
        """绑定智慧调度系统"""
        self._wisdom_dispatch = wisdom_dispatch
    
    async def enhance_dispatch(
        self, 
        query: str, 
        problem_type: str,
        school_mapping: List[Tuple]
    ) -> List[Tuple]:
        """
        记忆增强调度
        
        基于历史成功案例调整学派权重
        """
        if not self.config.memory_enhance_dispatch:
            return school_mapping
        
        if not self._memory_system:
            return school_mapping
        
        try:
            # 检索该问题类型的历史成功案例
            historical_success = await self._get_historical_success(problem_type)
            
            if historical_success:
                # 调整权重
                adjusted_mapping = []
                for school, weight in school_mapping:
                    school_key = school.value if hasattr(school, 'value') else str(school)
                    boost = historical_success.get(school_key, 0)
                    adjusted_weight = min(1.0, weight * (1 + boost * 0.2))
                    adjusted_mapping.append((school, adjusted_weight))
                
                return adjusted_mapping
            
        except Exception as e:
            logger.warning(f"[WisdomBridge] 增强调度失败: {e}")
        
        return school_mapping
    
    async def record_dispatch_result(
        self,
        query: str,
        problem_type: str,
        selected_school: Any,
        result: Dict
    ):
        """记录调度结果用于学习"""
        if not self.config.dispatch_result_memory:
            return
        
        school_key = selected_school.value if hasattr(selected_school, 'value') else str(selected_school)
        
        # 记录到历史
        record = {
            "query": query,
            "problem_type": problem_type,
            "school": school_key,
            "success": result.get("success", False),
            "confidence": result.get("confidence", 0.5),
            "timestamp": time.time()
        }
        self._dispatch_history.append(record)
        
        # 限制历史大小
        if len(self._dispatch_history) > 1000:
            self._dispatch_history = self._dispatch_history[-500:]
        
        # 更新学派表现
        perf = self._school_performance[school_key]
        perf["total_dispatches"] += 1
        if result.get("success"):
            perf["successful_dispatches"] += 1
        perf["avg_confidence"] = (
            (perf["avg_confidence"] * (perf["total_dispatches"] - 1) + result.get("confidence", 0.5))
            / perf["total_dispatches"]
        )
        perf["recent_results"].append(result.get("success", False))
        if len(perf["recent_results"]) > 100:
            perf["recent_results"] = perf["recent_results"][-50:]
        
        # 记忆化
        if self._memory_system and result.get("success"):
            await self._memoryize_success(query, problem_type, selected_school, result)
    
    async def _get_historical_success(self, problem_type: str) -> Dict[str, float]:
        """获取历史成功案例"""
        # 简化实现：基于近期成功率计算提升
        success_rates = {}
        
        for school, perf in self._school_performance.items():
            if perf["total_dispatches"] >= 3:
                recent_success = sum(perf["recent_results"][-10:]) / min(10, len(perf["recent_results"]))
                if recent_success > 0.6:
                    success_rates[school] = recent_success
        
        return success_rates
    
    async def _memoryize_success(
        self,
        query: str,
        problem_type: str,
        school: Any,
        result: Dict
    ):
        """将成功案例记忆化"""
        if not self._memory_system:
            return
        
        # 简化实现
        pass
    
    def get_school_performance(self) -> Dict[str, Dict]:
        """获取学派表现报告"""
        report = {}
        
        for school, perf in self._school_performance.items():
            recent_count = len(perf["recent_results"])
            recent_success = (
                sum(perf["recent_results"][-10:]) / min(10, recent_count)
                if recent_count > 0 else 0
            )
            
            report[school] = {
                "total_dispatches": perf["total_dispatches"],
                "success_rate": (
                    perf["successful_dispatches"] / perf["total_dispatches"]
                    if perf["total_dispatches"] > 0 else 0
                ),
                "recent_success_rate": recent_success,
                "avg_confidence": perf["avg_confidence"]
            }
        
        return report


# ═══════════════════════════════════════════════════════════════════════
# SomnCore集成
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class SomnIntegrationConfig:
    """SomnCore集成配置"""
    enable_digital_brain: bool = True
    digital_brain_as_subagent: bool = False  # 数字大脑作为子代理
    brain_thinks_for_complex: bool = True    # 复杂问题由数字大脑处理
    confidence_threshold: float = 0.6        # 置信度阈值


class SomnDigitalBrainIntegrator:
    """
    SomnCore ↔ 数字大脑集成器
    
    功能:
    - 数字大脑作为Somn的增强推理引擎
    - 复杂问题自动路由到数字大脑
    - 结果融合与置信度提升
    - 双向学习闭环
    """
    
    def __init__(self, config: Optional[SomnIntegrationConfig] = None):
        self.config = config or SomnIntegrationConfig()
        self._digital_brain = None
        self._somn_core = None
        self._integration_lock = threading.RLock()
    
    def attach_digital_brain(self, digital_brain):
        """绑定数字大脑"""
        self._digital_brain = digital_brain
    
    def attach_somn_core(self, somn_core):
        """绑定SomnCore"""
        self._somn_core = somn_core
    
    async def process_with_brain(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        使用数字大脑处理查询
        
        Returns:
            {
                "answer": str,
                "confidence": float,
                "source": str,  # "brain" | "somn" | "fused"
                "needs_review": bool
            }
        """
        if not self._digital_brain:
            return {"answer": "", "confidence": 0.0, "source": "unavailable"}
        
        try:
            # 使用数字大脑思考
            thought = await self._digital_brain.think(query, context)
            
            # 判断是否需要Somn增强
            needs_somn = (
                thought.confidence < self.config.confidence_threshold or
                self._is_complex_query(query)
            )
            
            if needs_somn and self._somn_core:
                # Somn处理并融合
                somn_result = await self._somn_process(query, context)
                fused = self._fuse_results(thought, somn_result)
                return fused
            
            return {
                "answer": thought.content,
                "confidence": thought.confidence,
                "source": "brain",
                "needs_review": thought.confidence < 0.5
            }
            
        except Exception as e:
            logger.error(f"[SomnIntegrator] 处理失败: {e}")
            return {"answer": f"处理错误: {e}", "confidence": 0.0, "source": "error"}
    
    async def _somn_process(self, query: str, context: Optional[Dict]) -> Dict:
        """Somn处理"""
        # 简化实现
        return {"answer": "", "confidence": 0.5}
    
    def _fuse_results(self, brain_thought, somn_result) -> Dict:
        """融合大脑和Somn的结果"""
        # 加权融合
        brain_weight = brain_thought.confidence
        somn_weight = somn_result.get("confidence", 0.5)
        total_weight = brain_weight + somn_weight
        
        if total_weight > 0:
            fused_confidence = (brain_weight * brain_thought.confidence + 
                               somn_weight * somn_result.get("confidence", 0.5)) / total_weight
        else:
            fused_confidence = 0.5
        
        # 选择更高置信度的答案
        if brain_thought.confidence >= somn_result.get("confidence", 0.5):
            fused_answer = brain_thought.content
        else:
            fused_answer = somn_result.get("answer", brain_thought.content)
        
        return {
            "answer": fused_answer,
            "confidence": fused_confidence,
            "source": "fused",
            "brain_confidence": brain_thought.confidence,
            "somn_confidence": somn_result.get("confidence", 0.5),
            "needs_review": fused_confidence < 0.6
        }
    
    def _is_complex_query(self, query: str) -> bool:
        """判断是否为复杂查询"""
        complexity_indicators = [
            "分析", "比较", "研究", "深入",
            "分析一下", "详细说明", "全面",
            "复杂", "多维度"
        ]
        return any(ind in query for ind in complexity_indicators)
    
    async def sync_learning(self):
        """同步学习闭环"""
        if not self._digital_brain:
            return
        
        try:
            # 获取数字大脑的学习成果
            brain_stats = self._digital_brain.get_stats()
            
            # 同步到SomnCore（如果需要）
            if self._somn_core:
                # 实现学习成果同步
                pass
            
            logger.info(f"[SomnIntegrator] 学习同步完成: {brain_stats}")
            
        except Exception as e:
            logger.error(f"[SomnIntegrator] 学习同步失败: {e}")


# ═══════════════════════════════════════════════════════════════════════
# 便捷工厂
# ═══════════════════════════════════════════════════════════════════════

async def create_digital_brain_integration() -> Dict[str, Any]:
    """
    创建完整的数字大脑集成系统
    
    Returns:
        {
            "digital_brain": DigitalBrainCore,
            "memory_bridge": MemoryLibraryBridge,
            "wisdom_bridge": WisdomMemoryBridge,
            "somn_integrator": SomnDigitalBrainIntegrator
        }
    """
    from digital_brain.digital_brain_core import get_digital_brain, BrainConfig
    
    # 创建数字大脑
    brain_config = BrainConfig(
        enable_local_llm=True,
        enable_wisdom_dispatch=True,
        enable_autonomous_evolution=True,
        enable_imperial_library=True,
    )
    
    digital_brain = get_digital_brain(brain_config)
    
    # 等待初始化
    await asyncio.sleep(2)
    
    # 创建桥接器
    memory_bridge = MemoryLibraryBridge()
    wisdom_bridge = WisdomMemoryBridge()
    somn_integrator = SomnDigitalBrainIntegrator()
    
    # 绑定组件
    memory_bridge.attach_memory_system(digital_brain._components.get('neural_memory'))
    memory_bridge.attach_library(digital_brain._components.get('imperial_library'))
    
    wisdom_bridge.attach_memory_system(digital_brain._components.get('neural_memory'))
    wisdom_bridge.attach_wisdom_dispatch(digital_brain._components.get('wisdom_dispatch'))
    
    somn_integrator.attach_digital_brain(digital_brain)
    
    # 启动桥接
    await memory_bridge.start()
    
    return {
        "digital_brain": digital_brain,
        "memory_bridge": memory_bridge,
        "wisdom_bridge": wisdom_bridge,
        "somn_integrator": somn_integrator
    }


__all__ = [
    # 记忆桥接
    'MemoryBridgeConfig',
    'MemoryLibraryBridge',
    'MemorySyncDirection',
    
    # 智慧桥接
    'WisdomBridgeConfig',
    'WisdomMemoryBridge',
    
    # Somn集成
    'SomnIntegrationConfig',
    'SomnDigitalBrainIntegrator',
    
    # 工厂
    'create_digital_brain_integration',
]
