# -*- coding: utf-8 -*-
"""
Claw-主系统集成桥接层
======================

Phase 4: Claw子系统与Somn主系统的集成接口。

提供:
1. WisdomDispatcher → ClawsCoordinator 的调度对接
2. SomnCore → ClawSystem 的生命周期管理
3. OpenClaw → ClawMemoryAdapter 的知识注入
4. NeuralMemorySystem ↔ ClawMemoryAdapter 的记忆同步

版本: v1.0.0
创建: 2026-04-22
"""

from __future__ import annotations

import logging
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class IntegrationLevel(Enum):
    """集成级别"""
    STANDBONE = "standalone"       # 独立运行（默认）
    DISPATCHER = "dispatcher"      # 接入WisdomDispatcher
    SOMNCORE = "somncore"          # 接入SomnCore生命周期
    FULL = "full"                  # 全集成（所有）


@dataclass
class IntegrationConfig:
    """集成配置"""
    level: IntegrationLevel = IntegrationLevel.STANDBONE
    auto_register_dispatcher: bool = False   # 自动注册到WisdomDispatcher
    enable_openclaw: bool = True            # 启用OpenClaw知识注入
    memory_sync_interval: int = 300         # 记忆同步间隔(秒)
    max_concurrent_claws: int = 5           # 最大并发Claw数
    default_fallback_claw: str = "孔子"     # 默认兜底Claw


@dataclass
class DispatchRequest:
    """
    调度请求（从WisdomDispatcher传入）。
    
    这是Claw子系统与主系统调度的核心数据结构。
    将ProblemType/Department/WisdomSchool映射为Claw选择。
    """
    query: str
    problem_type: Optional[str] = None
    department: Optional[str] = None
    wisdom_schools: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    priority: str = "normal"  # high / normal / low
    source: str = "user"      # user / system / scheduled
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DispatchResponse:
    """调度响应（返回给WisdomDispatcher）"""
    success: bool
    answer: str = ""
    claw_name: str = ""
    collaborators: List[str] = field(default_factory=list)
    confidence: float = 0.0
    steps_count: int = 0
    elapsed_seconds: float = 0.0
    error: str = ""
    react_trace: Optional[List[Dict[str, Any]]] = None


class ClawSystemBridge:
    """
    Claw子系统与主系统的桥接器。
    
    架构位置:
        SomnCore / WisdomDispatcher
                │
          ┌─────▼─────┐
          │   Bridge   │ ← ClawSystemBridge (本模块)
          └─────┬─────┘
        ┌──────────────┐
        │ ClawSystem   │
        │ Coordinator  │
        │ Architect×N │
        └──────────────┘
    
    用法:
        >>> bridge = ClawSystemBridge(IntegrationConfig(level=IntegrationLevel.FULL))
        >>> await bridge.initialize()
        >>> response = await bridge.dispatch(DispatchRequest(query="什么是仁？"))
        >>> print(response.answer)
        >>> await bridge.shutdown()
    """
    
    def __init__(self, config: Optional[IntegrationConfig] = None):
        from .claw import ClawSystem
        
        self.config = config or IntegrationConfig()
        self.system: Optional[ClawSystem] = None
        self._initialized = False
        self._openclaw_core = None
        
        # 调度统计
        self._dispatch_stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "avg_time": 0.0,
            "by_school": {},
        }
        
        # 回调钩子
        self._on_before_dispatch: List[Callable] = []
        self._on_after_dispatch: List[Callable] = []
    
    async def initialize(self) -> Dict[str, Any]:
        """
        初始化桥接器和整个Claw子系统。
        
        Returns:
            初始化结果字典
        """
        from .claw import ClawSystem
        
        self.system = ClawSystem()
        init_result = await self.system.start()
        self._initialized = True
        
        # 设置默认兜底
        if self.config.default_fallback_claw:
            if hasattr(self.system.coordinator, 'gateway'):
                self.system.coordinator.gateway.set_fallback(
                    self.config.default_fallback_claw
                )
        
        # 初始化OpenClaw（如果启用）
        if self.config.enable_openclaw:
            try:
                from ..openclaw._openclaw_core import OpenClawCore
                self._openclaw_core = OpenClawCore()
                logger.info("[ClawBridge] OpenClaw core initialized")
            except Exception as e:
                logger.warning(f"[ClawBridge] OpenClaw init failed: {e}")
        
        logger.info(f"[ClawBridge] Initialized at {self.config.level.value} level")
        return {**init_result, "bridge_level": self.config.level.value}
    
    async def dispatch(self, request: DispatchRequest) -> DispatchResponse:
        """
        处理调度请求（核心入口）。
        
        这是WisdomDispatcher/SomnCore调用Claw子系统的唯一接口。
        
        Args:
            request: 调度请求
            
        Returns:
            调度响应
        """
        import time
        if not self._initialized:
            await self.initialize()
        
        t0 = time.monotonic()
        self._dispatch_stats["total"] += 1

        # 调用前置回调
        for cb in self._on_before_dispatch:
            try:
                # ★ v1.1 修复: 区分同步/异步回调
                if asyncio.iscoroutinefunction(cb):
                    await cb(request)
                else:
                    cb(request)
            except Exception as e:
                logger.debug(f"[ClawBridge] before_dispatch callback error: {e}")

        dispatch_response: Optional[DispatchResponse] = None
        try:
            # 根据请求信息确定目标Claw
            target_claw = None
            context = request.context or {}
            
            # 策略1：如果指定了学派，按学派路由
            if request.wisdom_schools and len(request.wisdom_schools) > 0:
                school = request.wisdom_schools[0]
                candidates = self.system.coordinator.find_by_school(school)
                if candidates:
                    target_claw = candidates[0]
            
            # 策略2：直接通过系统路由
            response = await self.system.ask(
                request.query,
                target=target_claw,
                context=context,
            )
            
            elapsed = time.monotonic() - t0
            
            if response.success:
                self._dispatch_stats["success"] += 1
                
                # 统计学派分布
                school = getattr(
                    getattr(
                        self.system.coordinator.claws.get(response.routed_to), 
                        'metadata', None
                    ), 
                    'school', 'unknown'
                ) if response.routed_to in self.system.coordinator.claws else 'unknown'
                self._dispatch_stats["by_school"][school] = \
                    self._dispatch_stats["by_school"].get(school, 0) + 1
                
                # 更新平均时间
                s = self._dispatch_stats["success"]
                self._dispatch_stats["avg_time"] = (
                    (self._dispatch_stats["avg_time"] * (s - 1) + elapsed) / s
                )
                
                dispatch_response = DispatchResponse(
                    success=True,
                    answer=response.answer,
                    claw_name=response.routed_to,
                    collaborators=response.collaborators,
                    confidence=response.confidence,
                    steps_count=response.steps_count,
                    elapsed_seconds=elapsed,
                    react_trace=[
                        {"step": i+1, "thought": s.thought[:100], "action": s.action}
                        for i, s in enumerate(response.steps)
                    ] if response.steps else [],
                )
            else:
                self._dispatch_stats["failed"] += 1
                dispatch_response = DispatchResponse(
                    success=False,
                    error=response.error,
                    elapsed_seconds=elapsed,
                )
                
        except Exception as e:
            self._dispatch_stats["failed"] += 1
            logger.error(f"[ClawBridge] Dispatch error: {e}")
            dispatch_response = DispatchResponse(success=False, error="执行失败")

        # 调用后置回调
        for cb in self._on_after_dispatch:
            try:
                # ★ v1.1 修复: 区分同步/异步回调
                if asyncio.iscoroutinefunction(cb):
                    await cb(request, dispatch_response)
                else:
                    cb(request, dispatch_response)
            except Exception as e:
                logger.debug(f"[ClawBridge] after_dispatch callback error: {e}")

        return dispatch_response
    
    # ★ v10.0 修复: 批量分发超时保护
    BATCH_TIMEOUT_SECONDS = 300  # 整批最大5分钟
    DISPATCH_TIMEOUT_PER_ITEM = 60.0  # 单项分发超时60秒

    async def dispatch_batch(
        self,
        requests: List[DispatchRequest],
        max_concurrent: Optional[int] = None,
    ) -> List[DispatchResponse]:
        """
        [v10.0 修复] 批量处理调度请求（并发执行，带超时保护）。

        Args:
            requests: 调度请求列表
            max_concurrent: 最大并发数

        Returns:
            响应列表（超时项返回错误响应）
        """
        import time
        t0 = time.monotonic()
        sem = asyncio.Semaphore(max_concurrent or self.config.max_concurrent_claws)

        async def _process(req: DispatchRequest) -> DispatchResponse:
            async with sem:
                try:
                    # ★ 单项分发独立超时保护
                    return await asyncio.wait_for(
                        self.dispatch(req),
                        timeout=self.DISPATCH_TIMEOUT_PER_ITEM
                    )
                except asyncio.TimeoutError:
                    logger.warning(
                        f"[dispatch_batch] 单项超时({self.DISPATCH_TIMEOUT_PER_ITEM}s): "
                        f"{req.query[:50]}"
                    )
                    return DispatchResponse(
                        success=False,
                        error=f"单项处理超时({self.DISPATCH_TIMEOUT_PER_ITEM}s)",
                        elapsed_seconds=self.DISPATCH_TIMEOUT_PER_ITEM,
                    )

        tasks = [_process(r) for r in requests]

        # ★ 整批超时保护
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=self.BATCH_TIMEOUT_SECONDS
            )
            # 处理异常返回
            processed = []
            for i, r in enumerate(results):
                if isinstance(r, Exception):
                    processed.append(DispatchResponse(
                        success=False,
                        error=str(r)[:200],
                        elapsed_seconds=0.0,
                    ))
                else:
                    processed.append(r)
            return processed
        except asyncio.TimeoutError:
            elapsed = time.monotonic() - t0
            logger.error(f"[dispatch_batch] 整批超时({self.BATCH_TIMEOUT_SECONDS}s, elapsed={elapsed:.1f}s)")
            return []
    
    async def inject_knowledge(self, query: str, claw_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        通过OpenClaw抓取外部知识并注入到指定Claw的记忆。
        
        Args:
            query: 搜索查询
            claw_names: 目标Claw名称列表，None=全部已加载的Claw
            
        Returns:
            注入结果统计
        """
        if not self._openclaw_core:
            return {"error": "OpenClaw not enabled"}
        
        targets = claw_names or list(self.system.coordinator.claws.keys())
        results = {"targeted": len(targets), "injected": {}, "total_injected": 0}
        
        try:
            # 从所有连接的数据源抓取
            items = await self._openclaw_core.fetch_knowledge(query)
            
            if not items:
                results["fetched"] = 0
                return results
            
            results["fetched"] = len(items)
            
            # 注入到每个目标Claw
            for name in targets:
                claw = self.system.coordinator.get_claw(name)
                if claw is None:
                    continue
                    
                injected = await self._openclaw_core.inject_to_claw(claw.memory, items)
                if injected > 0:
                    results["injected"][name] = injected
                    results["total_injected"] += injected
            
            # 更新知识库
            update_result = await self._openclaw_core.update_knowledge(items)
            results["update_result"] = {
                "added": update_result.added,
                "errors": len(update_result.errors),
            }
            
        except Exception as e:
            results["error"] = "执行失败"
        
        return results
    
    async def submit_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """提交用户反馈并学习"""
        if not self._openclaw_core:
            return {"error": "OpenClaw not enabled"}
        
        learned = await self._openclaw_core.learn_feedback(feedback_data)
        return learned
    
    def get_bridge_status(self) -> Dict[str, Any]:
        """获取桥接器完整状态"""
        base = {
            "initialized": self._initialized,
            "integration_level": self.config.level.value,
            "loaded_claws": len(self.system.coordinator.claws) if self.system else 0,
            "openclaw_enabled": self._openclaw_core is not None,
            "dispatch_stats": dict(self._dispatch_stats),
        }
        
        if self._openclaw_core:
            base["openclaw_status"] = self._openclaw_core.get_status()
        
        if self.system:
            base["system_stats"] = self.system.get_stats()
        
        return base
    
    async def shutdown(self) -> None:
        """关闭桥接器及所有子系统"""
        if self.system:
            await self.system.shutdown()
        self._initialized = False
        logger.info("[ClawBridge] Shutdown complete")


__all__ = [
    "ClawSystemBridge",
    "IntegrationConfig", 
    "IntegrationLevel",
    "DispatchRequest",
    "DispatchResponse",
]
