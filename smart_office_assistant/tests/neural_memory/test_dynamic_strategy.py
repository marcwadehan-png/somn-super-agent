"""动态策略引擎 - 单元测试

迁移自 dynamic_strategy_engine.py 第518行的 if __name__ == "__main__" 自测块
"""

import pytest


class TestDynamicStrategyEngine:
    """动态学习策略引擎测试"""

    @pytest.fixture
    def engine(self):
        from src.neural_memory.dynamic_strategy_engine import DynamicStrategyEngine
        return DynamicStrategyEngine()

    def test_construction(self, engine):
        assert engine is not None

    def test_identify_stable_scenario(self, engine):
        context = engine.identify_scenario(
            local_data_count=15,
            local_data_growth_rate=0.05,
            network_availability=0.95,
            data_quality_trend="stable",
            urgency="normal",
            depth_requirement="deep",
        )
        assert context is not None
        # 稳定期数据充足
        assert "scenario_type" in dir(context) or hasattr(context, "scenario_type")

    def test_identify_crisis_scenario(self, engine):
        context = engine.identify_scenario(
            local_data_count=0,
            local_data_growth_rate=0.0,
            network_availability=0.90,
            data_quality_trend="unknown",
            urgency="urgent",
            depth_requirement="shallow",
        )
        assert context is not None

    def test_identify_growth_scenario(self, engine):
        context = engine.identify_scenario(
            local_data_count=25,
            local_data_growth_rate=0.40,
            network_availability=0.95,
            data_quality_trend="improving",
            urgency="normal",
            depth_requirement="medium",
        )
        assert context is not None

    def test_select_strategy(self, engine):
        context = engine.identify_scenario(
            local_data_count=15,
            local_data_growth_rate=0.05,
            network_availability=0.95,
            data_quality_trend="stable",
            urgency="normal",
            depth_requirement="deep",
        )
        strategy = engine.select_strategy(context)
        assert strategy is not None
        assert strategy.name  # 策略名非空

    def test_optimize_strategy_parameters(self, engine):
        context = engine.identify_scenario(
            local_data_count=15,
            local_data_growth_rate=0.05,
            network_availability=0.95,
            data_quality_trend="stable",
            urgency="normal",
            depth_requirement="deep",
        )
        strategy = engine.select_strategy(context)
        insights = {
            "average_data_quality": 0.88,
            "local_coverage_rate": 0.85,
            "network_value_rate": 0.72,
            "new_patterns_found": 5,
            "execution_time": 250,
        }
        optimized = engine.optimize_strategy_parameters(strategy, insights)
        assert optimized is not None
