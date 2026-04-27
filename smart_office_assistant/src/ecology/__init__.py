"""
生态智能系统 [v21.0 延迟加载优化]
Ecosystem Intelligence - 毫秒级启动

基于沙丘生态学思维，提供生态系统智能能力：
- EcosystemManager: 生态系统管理器
- ResourceOptimizer: 资源优化器
- EnvironmentalAdapter: 环境适配器
- EvolutionEngine: 演化引擎
- EcosystemIntelligence: 生态智能系统集成接口

[v21.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v21.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ecosystem_manager import (
        HealthStatus, ResourceType, EcosystemMetric, ResourceAllocation,
        EcosystemManager, ResourceOptimizer, EnvironmentalAdapter,
        EvolutionEngine, EcosystemIntelligence
    )


def __getattr__(name: str) -> Any:
    """[v21.0 优化] 延迟加载 - 毫秒级启动"""

    if name in ('HealthStatus', 'ResourceType', 'EcosystemMetric', 'ResourceAllocation',
                'EcosystemManager', 'ResourceOptimizer', 'EnvironmentalAdapter',
                'EvolutionEngine', 'EcosystemIntelligence'):
        from . import ecosystem_manager as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'ecology' has no attribute '{name}'")


__all__ = [
    'HealthStatus', 'ResourceType', 'EcosystemMetric', 'ResourceAllocation',
    'EcosystemManager', 'ResourceOptimizer', 'EnvironmentalAdapter',
    'EvolutionEngine', 'EcosystemIntelligence'
]

__version__ = '21.0.0'
