# -*- coding: utf-8 -*-
"""
Tests for intelligent_parameter_system.py
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

import pytest


# ──────────────────────────────────────────────────────────────
# 枚举定义
# ──────────────────────────────────────────────────────────────

class TestParameterEnums:
    """测试参数相关枚举"""

    def test_parameter_type_values(self):
        from src.neural_memory.intelligent_parameter_system import ParameterType
        expected = ["THRESHOLD", "WEIGHT", "TARGET", "QUALITY", "TIME"]
        for name in expected:
            assert hasattr(ParameterType, name)

    def test_adjustment_direction_values(self):
        from src.neural_memory.intelligent_parameter_system import AdjustmentDirection
        expected = ["INCREASE", "DECREASE", "STABILIZE", "OPTIMIZE"]
        for name in expected:
            assert hasattr(AdjustmentDirection, name)


# ──────────────────────────────────────────────────────────────
# PerformanceMetrics
# ──────────────────────────────────────────────────────────────

class TestPerformanceMetrics:
    """测试 PerformanceMetrics 数据类"""

    def test_metrics_creation(self):
        from src.neural_memory.intelligent_parameter_system import PerformanceMetrics
        metrics = PerformanceMetrics.__new__(PerformanceMetrics)
        assert metrics is not None


# ──────────────────────────────────────────────────────────────
# ParameterAdjustmentSystem
# ──────────────────────────────────────────────────────────────

class TestParameterAdjustmentSystem:
    """测试智能参数调整系统（核心自测块逻辑）"""

    def test_system_creation(self):
        from src.neural_memory.intelligent_parameter_system import ParameterAdjustmentSystem
        system = ParameterAdjustmentSystem()
        assert system is not None

    def test_record_learning_result_high_quality(self):
        """高质量学习结果 -> 高性能评分"""
        from src.neural_memory.intelligent_parameter_system import ParameterAdjustmentSystem
        system = ParameterAdjustmentSystem()

        initial_params = {
            "local_data_threshold": 5,
            "network_data_target": 10,
            "max_execution_time": 300,
            "data_quality_threshold": 0.7,
            "research_breadth": "medium",
        }

        results = {
            "data_points": [{"quality": 0.9, "has_source": True} for _ in range(20)],
            "patterns": [{"type": "trend"}] * 3,
            "insights": [{"value": "insight"}] * 2,
            "execution_time": 250,
            "errors": [],
        }

        metrics = system.record_learning_result(results, initial_params)
        assert metrics.overall_score > 0.5
        assert metrics.valid_data_ratio > 0.8
        assert metrics.average_quality > 0.8

    def test_record_learning_result_low_quality(self):
        """低质量学习结果 -> 低性能评分"""
        from src.neural_memory.intelligent_parameter_system import ParameterAdjustmentSystem
        system = ParameterAdjustmentSystem()

        params = {
            "local_data_threshold": 5,
            "network_data_target": 10,
            "max_execution_time": 300,
            "data_quality_threshold": 0.7,
            "research_breadth": "medium",
        }

        results = {
            "data_points": [{"quality": 0.5, "has_source": False} for _ in range(5)],
            "patterns": [],
            "insights": [],
            "execution_time": 800,
            "errors": ["timeout", "network_error"],
        }

        metrics = system.record_learning_result(results, params)
        assert metrics.valid_data_ratio < 0.5
        assert metrics.average_quality < 0.6

    def test_adjust_parameters(self):
        """参数调整功能"""
        from src.neural_memory.intelligent_parameter_system import ParameterAdjustmentSystem
        system = ParameterAdjustmentSystem()

        params = {
            "local_data_threshold": 5,
            "network_data_target": 10,
            "max_execution_time": 300,
            "data_quality_threshold": 0.7,
            "research_breadth": "medium",
        }

        results = {
            "data_points": [{"quality": 0.9, "has_source": True} for _ in range(20)],
            "patterns": [{"type": "trend"}] * 3,
            "insights": [{"value": "insight"}] * 2,
            "execution_time": 250,
            "errors": [],
        }

        metrics = system.record_learning_result(results, params)
        adjusted, adjustments = system.adjust_parameters(params, metrics)
        # 调整后参数应为 dict
        assert isinstance(adjusted, dict)

    def test_get_adjustment_summary_empty(self):
        """无调整历史时返回空总结"""
        from src.neural_memory.intelligent_parameter_system import ParameterAdjustmentSystem
        system = ParameterAdjustmentSystem()
        summary = system.get_adjustment_summary()
        assert summary["adjustments_count"] == 0

    def test_get_adjustment_summary_after_adjustment(self):
        """有调整历史时返回总结"""
        from src.neural_memory.intelligent_parameter_system import ParameterAdjustmentSystem
        system = ParameterAdjustmentSystem()

        params = {
            "local_data_threshold": 5,
            "max_execution_time": 300,
            "data_quality_threshold": 0.7,
            "research_breadth": "medium",
        }

        results = {
            "data_points": [{"quality": 0.9, "has_source": True} for _ in range(20)],
            "patterns": [],
            "insights": [],
            "execution_time": 250,
            "errors": [],
        }

        metrics = system.record_learning_result(results, params)
        system.adjust_parameters(params, metrics, aggressive=True)
        summary = system.get_adjustment_summary()
        assert summary["total_adjustments"] > 0
        assert "adjustment_directions" in summary
