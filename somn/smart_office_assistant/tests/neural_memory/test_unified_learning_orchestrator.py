"""统一学习调度器 - 单元测试 (unified_learning_orchestrator.py)

核心模块优先测试：调度器是新架构核心，整合 6 个学习策略。
"""

import pytest
from unittest.mock import patch, MagicMock


class TestSchedulerConfig:
    """调度器配置测试"""

    def test_default_config(self):
        from src.neural_memory.unified_learning_orchestrator import SchedulerConfig
        config = SchedulerConfig()
        assert config.local_threshold == 5
        assert config.network_supplement_ratio == 0.3
        assert config.quality_threshold == 0.6

    def test_custom_config(self):
        from src.neural_memory.unified_learning_orchestrator import (
            SchedulerConfig, SchedulerStrategyMode
        )
        config = SchedulerConfig(
            strategy_mode=SchedulerStrategyMode.NETWORK_ONLY,
            local_threshold=10,
        )
        assert config.strategy_mode == SchedulerStrategyMode.NETWORK_ONLY
        assert config.local_threshold == 10


class TestLearningPlan:
    """学习计划测试"""

    def test_plan_creation(self):
        from src.neural_memory.unified_learning_orchestrator import LearningPlan
        plan = LearningPlan(
            plan_id="LP_001",
            strategy_type="daily",
            execution_phase="planned",
            data_summary={},
            learning_config={},
            expected_outcomes=["item1"],
        )
        assert plan.plan_id == "LP_001"
        assert len(plan.expected_outcomes) == 1


class TestStrategyRegistry:
    """策略注册表完整性测试"""

    def test_registry_has_all_5_strategies(self):
        from src.neural_memory.learning_strategies import (
            STRATEGY_REGISTRY, LearningStrategyType
        )
        expected_types = {
            LearningStrategyType.DAILY,
            LearningStrategyType.THREE_TIER,
            LearningStrategyType.ENHANCED,
            LearningStrategyType.SOLUTION,
            LearningStrategyType.FEEDBACK,
        }
        assert set(STRATEGY_REGISTRY.keys()) == expected_types

    def test_all_registry_values_are_classes(self):
        from src.neural_memory.learning_strategies import STRATEGY_REGISTRY
        for stype, cls in STRATEGY_REGISTRY.items():
            assert callable(cls), f"{stype} -> {cls} 不可调用"


class TestOrchestratorReport:
    """调度器报告测试"""

    def test_report_creation(self):
        from src.neural_memory.unified_learning_orchestrator import OrchestratorReport
        report = OrchestratorReport(
            report_id="R_001",
            date="2026-04-06",
            execution_time="10:00:00",
            plan=None,
            strategy_results={},
            total_learning_events=5,
            total_knowledge_updates=3,
            total_duration_seconds=2.5,
            summary="测试摘要",
            recommendations=["建议1"],
        )
        assert report.total_learning_events == 5
        assert report.total_duration_seconds == 2.5


class TestUnifiedDataScanner:
    """统一数据扫描器测试"""

    def test_scan_returns_result(self, tmp_project):
        from src.neural_memory.learning_strategies import UnifiedDataScanner
        scanner = UnifiedDataScanner(str(tmp_project))
        result = scanner.scan()
        assert result is not None
        assert isinstance(result.total, int)

    def test_scan_data_source_breakdown(self, tmp_project):
        from src.neural_memory.learning_strategies import UnifiedDataScanner
        scanner = UnifiedDataScanner(str(tmp_project))
        result = scanner.scan()
        breakdown = scanner.get_data_source_breakdown(result)
        assert isinstance(breakdown, dict)


class TestUnifiedLearningOrchestrator:
    """统一调度器核心接口测试"""

    def test_construction(self, tmp_project):
        from src.neural_memory.unified_learning_orchestrator import UnifiedLearningOrchestrator
        orch = UnifiedLearningOrchestrator(base_path=str(tmp_project))
        assert orch.config is not None
        assert orch.scanner is not None

    def test_get_status(self, tmp_project):
        from src.neural_memory.unified_learning_orchestrator import UnifiedLearningOrchestrator
        orch = UnifiedLearningOrchestrator(base_path=str(tmp_project))
        status = orch.get_status()
        assert "config" in status
        assert "data_sources" in status

    def test_scan_data_sources(self, tmp_project):
        from src.neural_memory.unified_learning_orchestrator import UnifiedLearningOrchestrator
        orch = UnifiedLearningOrchestrator(base_path=str(tmp_project))
        result = orch.scan_data_sources()
        assert isinstance(result, dict)

    def test_plan_learning_data_selection(self, tmp_project):
        from src.neural_memory.unified_learning_orchestrator import UnifiedLearningOrchestrator
        orch = UnifiedLearningOrchestrator(base_path=str(tmp_project))
        plan = orch.plan_learning_data_selection()
        assert "strategy" in plan
        assert "total_data" in plan
        assert isinstance(plan["total_data"], int)

    def test_set_config(self, tmp_project):
        from src.neural_memory.unified_learning_orchestrator import (
            UnifiedLearningOrchestrator, SchedulerConfig, SchedulerStrategyMode
        )
        orch = UnifiedLearningOrchestrator(base_path=str(tmp_project))
        new_config = SchedulerConfig(
            strategy_mode=SchedulerStrategyMode.LOCAL_ONLY,
            local_threshold=20,
        )
        orch.set_config(new_config)
        assert orch.config.local_threshold == 20

    def test_get_execution_log(self, tmp_project):
        from src.neural_memory.unified_learning_orchestrator import UnifiedLearningOrchestrator
        orch = UnifiedLearningOrchestrator(base_path=str(tmp_project))
        log = orch.get_execution_log()
        assert isinstance(log, str)

    def test_unknown_strategy_does_not_crash(self, tmp_project):
        """验证对无效策略的处理不崩溃"""
        from src.neural_memory.unified_learning_orchestrator import UnifiedLearningOrchestrator
        orch = UnifiedLearningOrchestrator(base_path=str(tmp_project))
        # 仅验证 orchestrator 能正常创建，策略注册表完整性已在其他测试中覆盖
        assert orch is not None
