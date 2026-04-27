# -*- coding: utf-8 -*-
"""
Tests for integrated_learning.py
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

from unittest.mock import patch, MagicMock
import pytest


# ──────────────────────────────────────────────────────────────
# 模块导入
# ──────────────────────────────────────────────────────────────

class TestIntegratedLearningModule:
    """integrated_learning 模块基础检查"""

    def test_module_imports(self):
        from src.neural_memory.integrated_learning import IntegratedLearningExecutor
        assert IntegratedLearningExecutor is not None

    def test_run_integrated_learning_callable(self):
        from src.neural_memory.integrated_learning import run_integrated_learning
        assert callable(run_integrated_learning)

    def test_plan_dataclass_exists(self):
        from src.neural_memory.integrated_learning import IntegratedLearningPlan
        assert IntegratedLearningPlan is not None


# ──────────────────────────────────────────────────────────────
# IntegratedLearningPlan
# ──────────────────────────────────────────────────────────────

class TestIntegratedLearningPlan:
    """测试集成学习计划数据类"""

    def test_plan_creation(self):
        from src.neural_memory.integrated_learning import IntegratedLearningPlan
        plan = IntegratedLearningPlan.__new__(IntegratedLearningPlan)
        assert plan is not None
