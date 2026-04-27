"""
集成层模块
Integration Layer Module

unified协调三大核心模块:
- 自主进化引擎 (Autonomous Evolution Engine)
- 行业知识图谱 (Industry Knowledge Graph)
- AI原生增长strategy (AI-Native Growth Strategies)

版本: v1.0
日期: 2026-04-04
"""

from .unified_orchestrator import UnifiedOrchestrator
from .module_coordinator import ModuleCoordinator
from .integration_events import IntegrationEventBus
from .monitoring_system import MonitoringSystem
from .performance_optimizer import PerformanceOptimizer

__all__ = [
    "UnifiedOrchestrator",
    "ModuleCoordinator", 
    "IntegrationEventBus",
    "MonitoringSystem",
    "PerformanceOptimizer"
]
