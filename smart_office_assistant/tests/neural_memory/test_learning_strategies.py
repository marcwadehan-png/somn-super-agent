# -*- coding: utf-8 -*-
"""
Tests for learning_strategies package
覆盖策略类型、基类、注册表和各策略实现。
"""

import pytest


# ──────────────────────────────────────────────────────────────
# LearningStrategyType 枚举
# ──────────────────────────────────────────────────────────────

class TestLearningStrategyType:
    """测试学习策略类型枚举"""

    def test_all_strategy_types_exist(self):
        from src.neural_memory.learning_strategies import LearningStrategyType
        expected = ["DAILY", "THREE_TIER", "ENHANCED", "SOLUTION", "FEEDBACK"]
        for name in expected:
            assert hasattr(LearningStrategyType, name), f"Missing: {name}"

    def test_type_count(self):
        from src.neural_memory.learning_strategies import LearningStrategyType
        assert len(list(LearningStrategyType)) == 5


# ──────────────────────────────────────────────────────────────
# 基类和数据结构
# ──────────────────────────────────────────────────────────────

class TestBaseLearningStrategy:
    """测试抽象基类"""

    def test_base_class_exists(self):
        from src.neural_memory.learning_strategies import BaseLearningStrategy
        assert BaseLearningStrategy is not None

    def test_learning_result_exists(self):
        from src.neural_memory.learning_strategies import LearningResult
        assert LearningResult is not None

    def test_data_scan_result_exists(self):
        from src.neural_memory.learning_strategies import DataScanResult
        assert DataScanResult is not None


# ──────────────────────────────────────────────────────────────
# 策略注册表
# ──────────────────────────────────────────────────────────────

class TestStrategyRegistry:
    """测试策略注册表"""

    def test_registry_complete(self):
        from src.neural_memory.learning_strategies import STRATEGY_REGISTRY, LearningStrategyType
        assert len(STRATEGY_REGISTRY) == 5
        for st in LearningStrategyType:
            assert st in STRATEGY_REGISTRY, f"Unregistered strategy: {st}"


# ──────────────────────────────────────────────────────────────
# UnifiedDataScanner
# ──────────────────────────────────────────────────────────────

class TestUnifiedDataScanner:
    """测试统一数据扫描器"""

    def test_scanner_class_exists(self):
        from src.neural_memory.learning_strategies import UnifiedDataScanner
        assert UnifiedDataScanner is not None


# ──────────────────────────────────────────────────────────────
# 各策略实现
# ──────────────────────────────────────────────────────────────

class TestDailyLearningStrategy:
    def test_class_exists(self):
        from src.neural_memory.learning_strategies import DailyLearningStrategy
        assert DailyLearningStrategy is not None


class TestThreeTierLearningStrategy:
    def test_class_exists(self):
        from src.neural_memory.learning_strategies import ThreeTierLearningStrategy
        assert ThreeTierLearningStrategy is not None


class TestEnhancedLearningStrategy:
    def test_class_exists(self):
        from src.neural_memory.learning_strategies import EnhancedLearningStrategy
        assert EnhancedLearningStrategy is not None


class TestSolutionLearningStrategy:
    def test_class_exists(self):
        from src.neural_memory.learning_strategies import SolutionLearningStrategy
        assert SolutionLearningStrategy is not None


class TestFeedbackLoopStrategy:
    def test_class_exists(self):
        from src.neural_memory.learning_strategies import FeedbackLoopStrategy
        assert FeedbackLoopStrategy is not None
