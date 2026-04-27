"""autonomous_evolution_engine 包 - Facade + 向后兼容导出"""
# 本文件内容由 autonomous_evolution_engine.py 拆分而来

from __future__ import annotations
from typing import Any, Optional

__all__ = [
    # enums
    "EvolutionStage", "EvolutionType",
    # dataclasses
    "EvolutionPlan", "SystemHealth",
    # subsystems
    "AnomalyDetector", "PredictiveHealthModel", "SelfDiagnostics",
    "StrategyAutoOptimizer", "KnowledgeAutoExpander",
    "MultiObjectiveOptimizer", "ArchitectureSelfAdjuster", "EvolutionVisualizer",
    # main engine
    "AutonomousEvolutionEngine", "create_and_start_engine",
    # compat alias
    "get_evolution_engine",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'EvolutionStage':
        from ._aee_base import EvolutionStage
        return EvolutionStage
    if name == 'EvolutionType':
        from ._aee_base import EvolutionType
        return EvolutionType
    if name == 'EvolutionPlan':
        from ._aee_base import EvolutionPlan
        return EvolutionPlan
    if name == 'SystemHealth':
        from ._aee_base import SystemHealth
        return SystemHealth
    if name == 'AnomalyDetector':
        from ._aee_subsystems import AnomalyDetector
        return AnomalyDetector
    if name == 'PredictiveHealthModel':
        from ._aee_subsystems import PredictiveHealthModel
        return PredictiveHealthModel
    if name == 'SelfDiagnostics':
        from ._aee_subsystems import SelfDiagnostics
        return SelfDiagnostics
    if name == 'StrategyAutoOptimizer':
        from ._aee_subsystems import StrategyAutoOptimizer
        return StrategyAutoOptimizer
    if name == 'KnowledgeAutoExpander':
        from ._aee_subsystems import KnowledgeAutoExpander
        return KnowledgeAutoExpander
    if name == 'MultiObjectiveOptimizer':
        from ._aee_subsystems import MultiObjectiveOptimizer
        return MultiObjectiveOptimizer
    if name == 'ArchitectureSelfAdjuster':
        from ._aee_subsystems import ArchitectureSelfAdjuster
        return ArchitectureSelfAdjuster
    if name == 'EvolutionVisualizer':
        from ._aee_subsystems import EvolutionVisualizer
        return EvolutionVisualizer
    if name == 'AutonomousEvolutionEngine':
        from ._aee_engine import AutonomousEvolutionEngine
        return AutonomousEvolutionEngine
    if name == 'create_and_start_engine':
        from ._aee_engine import create_and_start_engine
        return create_and_start_engine
    if name == 'get_evolution_engine':
        def get_evolution_engine(config: Optional[Any] = None) -> Any:
            from ._aee_engine import AutonomousEvolutionEngine
            return AutonomousEvolutionEngine(config)
        return get_evolution_engine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
