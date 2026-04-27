# -*- coding: utf-8 -*-
"""
__all__ = [
    'get_tier3_scheduler',
    'tier3_analyze',
]

三级神经网络调度器 - 统一入口模块
Tier-3 Neural Scheduler Unified Entry
====================================

统一调用入口:
- get_tier3_scheduler(): 获取调度器单例
- tier3_analyze(): 三级神经网络分析统一入口

版本: v1.0
日期: 2026-04-06
"""

from typing import Dict, Optional
import uuid

from ._tier3_scheduler import Tier3NeuralScheduler
from ._tier3_types import Tier3Query, Tier3Result

# ==================== 单例模式 ====================
_scheduler: Optional[Tier3NeuralScheduler] = None

def get_tier3_scheduler() -> Tier3NeuralScheduler:
    """获取调度器单例"""
    global _scheduler
    if _scheduler is None:
        _scheduler = Tier3NeuralScheduler()
    return _scheduler

def tier3_analyze(query_text: str,
                  context: Optional[Dict] = None,
                  p1_count: int = 6,
                  p3_count: int = 4,
                  p2_count: int = 4,
                  random_seed: Optional[int] = None) -> Tier3Result:
    """
    三级神经网络分析 - unified入口

    Args:
        query_text: 问题文本
        context: 上下文
        p1_count: P1层引擎数量(默认6)
        p3_count: P3层引擎数量(默认4)
        p2_count: P2层引擎数量(默认4)
        random_seed: 随机种子(可复现)

    Returns:
        Tier3Result: 三层fusion后的完整分析结果

    Example:
        >>> result = tier3_analyze("公司面临竞争压力,如何制定增长战略?")
        >>> print(result.final_strategy)
        >>> print(f"置信度: {result.decision_confidence:.2f}")
    """
    scheduler = get_tier3_scheduler()

    query = Tier3Query(
        query_id=str(uuid.uuid4())[:8],
        query_text=query_text,
        context=context or {},
        p1_count=p1_count,
        p3_count=p3_count,
        p2_count=p2_count,
        random_seed=random_seed
    )

    return scheduler.schedule(query)
