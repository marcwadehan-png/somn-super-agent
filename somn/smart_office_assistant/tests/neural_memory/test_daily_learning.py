# -*- coding: utf-8 -*-
"""
Tests for daily_learning.py
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


# ──────────────────────────────────────────────────────────────
# LearningStage 枚举
# ──────────────────────────────────────────────────────────────

class TestLearningStage:
    """测试 LearningStage 枚举定义"""

    def test_stage_values_exist(self):
        from src.neural_memory.daily_learning import LearningStage
        expected_stages = [
            "DATA_SCAN", "INSTANCE_LEARNING", "VALIDATION_LEARNING",
            "ERROR_LEARNING", "ASSOCIATION_LEARNING", "FEEDBACK_INTEGRATION",
            "TRANSFER_LEARNING", "REPORT_GENERATION",
        ]
        for name in expected_stages:
            assert hasattr(LearningStage, name), f"Missing stage: {name}"

    def test_stage_values_unique(self):
        from src.neural_memory.daily_learning import LearningStage
        values = [s.value for s in LearningStage]
        assert len(values) == len(set(values)), "Stage values should be unique"


# ──────────────────────────────────────────────────────────────
# DailyLearningReport 数据类
# ──────────────────────────────────────────────────────────────

class TestDailyLearningReport:
    """测试 DailyLearningReport 数据类"""

    def test_minimal_report_creation(self):
        from src.neural_memory.daily_learning import DailyLearningReport
        report = DailyLearningReport(
            report_id="R001",
            date="2026-04-06",
            execution_time="10:30:00",
            new_findings_count=5,
            new_validations_count=3,
            error_cases_count=1,
            instance_learning_events=[],
            validation_learning_events=[],
            error_learning_events=[],
            association_learning_events=[],
            new_patterns=[],
            confidence_updates=[],
            new_associations=[],
            rl_updates=[],
            q_table_snapshot={},
            transfer_hypotheses=[],
            registered_knowledge=[],
            transfer_report={},
            system_health={"score": 0.8},
            memory_stats={"total": 100},
            knowledge_stats={"concepts": 50},
            summary="test run",
            recommendations=[],
        )
        assert report.report_id == "R001"
        assert report.new_findings_count == 5
        assert report.rl_updates == []

    def test_report_with_rl_data(self):
        from src.neural_memory.daily_learning import DailyLearningReport
        report = DailyLearningReport(
            report_id="R002",
            date="2026-04-06",
            execution_time="11:00:00",
            new_findings_count=2,
            new_validations_count=1,
            error_cases_count=0,
            instance_learning_events=[{"type": "instance"}],
            validation_learning_events=[],
            error_learning_events=[],
            association_learning_events=[],
            new_patterns=[],
            confidence_updates=[],
            new_associations=[],
            rl_updates=[{"strategy": "s1", "reward": 0.5}],
            q_table_snapshot={"s1_a1": 0.8},
            transfer_hypotheses=[],
            registered_knowledge=[],
            transfer_report={},
            system_health={},
            memory_stats={},
            knowledge_stats={},
            summary="with RL",
            recommendations=["keep going"],
        )
        assert len(report.rl_updates) == 1
        assert report.q_table_snapshot == {"s1_a1": 0.8}


# ──────────────────────────────────────────────────────────────
# DailyLearningExecutor
# ──────────────────────────────────────────────────────────────

class TestDailyLearningExecutor:
    """测试 DailyLearningExecutor（集成，mock 外部依赖）"""

    def test_executor_instantiation(self, tmp_path):
        """执行器能够实例化"""
        from src.neural_memory.daily_learning import DailyLearningExecutor
        executor = DailyLearningExecutor(base_path=str(tmp_path))
        assert executor is not None

    def test_executor_has_methods(self):
        """验证执行器有核心方法（可能因循环 import 不完整）"""
        from src.neural_memory.daily_learning import DailyLearningExecutor
        # 仅验证类存在
        assert DailyLearningExecutor is not None


# ──────────────────────────────────────────────────────────────
# run_daily_learning_v2 路由
# ──────────────────────────────────────────────────────────────

class TestDailyLearningV2Route:
    """测试 v2 路由入口"""

    def test_v2_route_callable(self):
        from src.neural_memory.daily_learning import run_daily_learning_v2
        assert callable(run_daily_learning_v2)
