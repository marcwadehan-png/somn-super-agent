# -*- coding: utf-8 -*-
"""
Tests for solution_daily_learning.py
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

from unittest.mock import patch
import pytest


# ──────────────────────────────────────────────────────────────
# 模块导入与函数检查
# ──────────────────────────────────────────────────────────────

class TestSolutionDailyLearningModule:
    """solution_daily_learning 模块基础检查"""

    def test_run_daily_learning_callable(self):
        """run_daily_learning 可调用"""
        from src.neural_memory.solution_daily_learning import run_daily_learning
        assert callable(run_daily_learning)

    def test_run_daily_learning_v2_callable(self):
        """run_daily_learning_v2 路由可调用"""
        from src.neural_memory.solution_daily_learning import run_daily_learning_v2
        assert callable(run_daily_learning_v2)

    @patch("src.neural_memory.solution_daily_learning.run_daily_learning")
    @patch("src.neural_memory.solution_daily_learning.run_daily_learning_v2")
    def test_v2_route_callable(self, mock_v2_func, mock_v1):
        """run_daily_learning_v2 路由可调用（直接测试可调用性）"""
        from src.neural_memory.solution_daily_learning import run_daily_learning_v2
        assert callable(run_daily_learning_v2)
