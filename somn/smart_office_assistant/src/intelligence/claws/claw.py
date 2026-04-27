# -*- coding: utf-8 -*-
"""
claw.py - Claw子系统统一入口
============================

提供简洁的API供外部模块使用。

版本: v1.0.0
创建: 2026-04-22

快速开始:
    >>> from src.intelligence.claws.claw import ClawSystem
    >>> system = ClawSystem()
    >>> await system.start()  # 加载所有Claw
    >>> result = await system.ask("什么是仁？")
    >>> print(result.answer)
    >>> await system.shutdown()
"""

from __future__ import annotations

import logging
from typing import Optional, List, Dict, Any

from ._claw_architect import (
    ClawArchitect, ClawMetadata, ReActResult,
    load_claw_config, create_claw, list_all_configs,
)
from ._claws_coordinator import (
    ClawsCoordinator, GatewayRouter,
    RouteStrategy, ProcessResult,
)
from ._claw_agent_wrapper import (
    ClawAgentWrapper, ClawAgentPool,
    AgentTaskInfo, SpawnOptions, TaskStatus,
    get_global_agent_pool, spawn_claw_task, spawn_multi_claw_tasks,
)

logger = logging.getLogger(__name__)


class ClawSystem:
    """
    Claw子系统统一入口。

    封装ClawsCoordinator，提供更简单的同步/异步API。
    """

    def __init__(self, claw_names: Optional[List[str]] = None):
        """
        Args:
            claw_names: 要加载的Claw名称列表。None=全部加载
        """
        self.coordinator = ClawsCoordinator()
        self._claw_names = claw_names
        self._initialized = False

    async def start(self) -> Dict[str, Any]:
        """启动系统：加载所有Claw配置"""
        init_result = await self.coordinator.initialize(names=self._claw_names)
        self._initialized = True
        logger.info(f"[ClawSystem] Started with {init_result['loaded']} claws")
        return init_result

    async def ask(
        self,
        query: str,
        target: Optional[str] = None,
        **kwargs
    ) -> "ClawResponse":
        """
        提问（主入口）。

        Args:
            query: 问题文本
            target: 指定目标Claw名称（可选）
            **kwargs: 传递给process的额外参数

        Returns:
            ClawResponse包装对象
        """
        if not self._initialized:
            await self.start()

        result = await self.coordinator.process(query, target_claw=target, **kwargs)
        return ClawResponse(result)

    async def ask_batch(
        self,
        queries: List[str],
        target: Optional[str] = None,
    ) -> List["ClawResponse"]:
        """批量提问"""
        if not self._initialized:
            await self.start()
        results = await self.coordinator.process_batch(queries, target_claw=target)
        return [ClawResponse(r) for r in results]

    async def shutdown(self) -> None:
        """关闭系统：持久化所有记忆"""
        for name, claw in self.coordinator.claws.items():
            try:
                claw.memory.persist()
            except Exception as e:
                logger.warning(f"[ClawSystem] Failed to persist {name} memory: {e}")
        logger.info("[ClawSystem] Shutdown complete")

    def list_available(self) -> List[str]:
        """列出所有可用Claw名称"""
        return list_all_configs()

    def list_loaded(self) -> List[Dict[str, Any]]:
        """列出已加载的Claw详情"""
        return self.coordinator.list_claws()

    def find_claw(self, text: str) -> List[str]:
        """根据触发词查找匹配的Claw"""
        return self.coordinator.find_by_trigger(text)

    def get_stats(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        base = self.coordinator.get_stats()
        base["initialized"] = self._initialized
        return base


class ClawResponse:
    """
 Claw响应包装器。

    提供便捷属性访问ReActResult和ProcessResult的内容。
    """

    def __init__(self, process_result: ProcessResult):
        self._result = process_result

    @property
    def success(self) -> bool:
        return self._result.success

    @property
    def answer(self) -> str:
        if self._result.react_result:
            return self._result.react_result.final_answer
        return ""

    @property
    def routed_to(self) -> str:
        return self._result.routed_to

    @property
    def collaborators(self) -> List[str]:
        return self._result.collaborators_used

    @property
    def confidence(self) -> float:
        return self._result.route_confidence

    @property
    def elapsed(self) -> float:
        return self._result.elapsed_seconds

    @property
    def error(self) -> str:
        return self._result.error

    @property
    def steps_count(self) -> int:
        if self._result.react_result and self._result.react_result.steps:
            return len(self._result.react_result.steps)
        return 0

    @property
    def steps(self) -> list:
        if self._result.react_result:
            return self._result.react_result.steps
        return []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "answer": self.answer,
            "routed_to": self.routed_to,
            "collaborators": self.collaborators,
            "confidence": self.confidence,
            "elapsed": self.elapsed,
            "error": self.error,
            "steps_count": self.steps_count,
        }

    def __repr__(self) -> str:
        status = "OK" if self.success else f"ERR: {self.error[:50]}"
        return f"<ClawResponse [{status}] → {self.routed_to} ({self.elapsed:.2f}s)>"


# ═══════════════════════════════════════════════════════════════
# 便捷异步运行函数
# ═══════════════════════════════════════════════════════════════

async def quick_ask(query: str, target: Optional[str] = None) -> ClawResponse:
    """
    一次性提问函数（自动管理生命周期）。

    用法:
        >>> response = await quick_ask("什么是道？", target="老子")
        >>> print(response.answer)
    """
    system = ClawSystem()
    try:
        await system.start()
        return await system.ask(query, target=target)
    finally:
        await system.shutdown()


__all__ = [
    # 核心类
    "ClawSystem", "ClawResponse",
    "ClawArchitect", "ClawsCoordinator",
    "ClawAgentWrapper", "ClawAgentPool",
    # 数据类
    "AgentTaskInfo", "SpawnOptions", "TaskStatus",
    # 便捷函数
    "load_claw_config", "create_claw", "list_all_configs",
    "quick_ask",
    "get_global_agent_pool", "spawn_claw_task", "spawn_multi_claw_tasks",
]
