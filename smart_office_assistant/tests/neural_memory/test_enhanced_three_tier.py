# -*- coding: utf-8 -*-
"""
Tests for enhanced_three_tier_learning.py
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

from unittest.mock import patch, MagicMock
import pytest


# ──────────────────────────────────────────────────────────────
# 模块导入检查
# ──────────────────────────────────────────────────────────────

class TestEnhancedThreeTierModule:
    """模块基础检查"""

    def test_module_imports(self):
        from src.neural_memory.enhanced_three_tier_learning import EnhancedThreeTierLearner
        assert EnhancedThreeTierLearner is not None

    def test_v2_route_callable(self):
        from src.neural_memory.enhanced_three_tier_learning import (
            run_enhanced_three_tier_learning_v2,
        )
        assert callable(run_enhanced_three_tier_learning_v2)


# ──────────────────────────────────────────────────────────────
# EnhancedThreeTierLearner
# ──────────────────────────────────────────────────────────────

class TestEnhancedThreeTierLearner:
    """测试增强型三层学习器"""

    def test_learner_creation(self):
        from src.neural_memory.enhanced_three_tier_learning import EnhancedThreeTierLearner
        learner = EnhancedThreeTierLearner()
        assert learner is not None

    def test_learner_has_execute_method(self):
        from src.neural_memory.enhanced_three_tier_learning import EnhancedThreeTierLearner
        assert hasattr(EnhancedThreeTierLearner, "execute_learning_cycle")
