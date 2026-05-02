"""学习引擎 - 单元测试

迁移自 learning_engine.py 第601行的 if __name__ == "__main__" 自测块
"""

import pytest


class TestLearningEngine:
    """自主学习引擎测试"""

    @pytest.fixture
    def engine(self):
        from src.neural_memory.learning_engine import LearningEngine
        return LearningEngine()

    def test_construction(self, engine):
        assert engine is not None

    def test_learn_from_instance(self, engine):
        instances = [
            {"场景": "零售门店", "strategy": "慢节奏音乐", "效果": "停留+25%", "置信度": 0.82},
            {"场景": "零售门店", "strategy": "慢节奏音乐", "效果": "停留+28%", "置信度": 0.85},
            {"场景": "零售门店", "strategy": "慢节奏音乐", "效果": "停留+22%", "置信度": 0.80},
            {"场景": "零售门店", "strategy": "慢节奏音乐", "效果": "停留+30%", "置信度": 0.88},
            {"场景": "零售门店", "strategy": "慢节奏音乐", "效果": "停留+26%", "置信度": 0.83},
        ]
        pattern, event = engine.learn_from_instance(instances, "门店音乐strategy")
        assert pattern is not None or event is not None  # 至少有一个返回
