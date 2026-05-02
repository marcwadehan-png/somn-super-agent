"""验证引擎 - 单元测试

迁移自 validation_engine.py 第685行的 if __name__ == "__main__" 自测块
"""

import pytest


class TestValidationEngine:
    """验证引擎测试"""

    @pytest.fixture
    def engine(self):
        from src.neural_memory.validation_engine import ValidationEngine
        return ValidationEngine()

    def test_construction(self, engine):
        assert engine is not None

    def test_create_validation_plan(self, engine):
        hypothesis = {
            "假设ID": "HYP_001",
            "假设内容": "慢节奏音乐导致顾客停留时长增加",
            "置信度": 0.70,
        }
        plan = engine.create_validation_plan(hypothesis)
        assert plan is not None
        assert plan.plan_id  # 计划 ID 非空

    def test_execute_validation(self, engine):
        hypothesis = {
            "假设ID": "HYP_002",
            "假设内容": "测试假设",
            "置信度": 0.70,
        }
        plan = engine.create_validation_plan(hypothesis)

        data = {
            "实验组": {"均值": 28, "标准差": 8, "样本量": 250},
            "对照组": {"均值": 22, "标准差": 7, "样本量": 250},
            "原置信度": 0.70,
        }

        result = engine.execute_validation(plan, data)
        assert result is not None

    def test_format_validation_report(self, engine):
        hypothesis = {"假设ID": "HYP_003", "假设内容": "格式化测试", "置信度": 0.5}
        plan = engine.create_validation_plan(hypothesis)
        data = {
            "实验组": {"均值": 25, "标准差": 5, "样本量": 100},
            "对照组": {"均值": 20, "标准差": 5, "样本量": 100},
            "原置信度": 0.5,
        }
        result = engine.execute_validation(plan, data)
        report = engine.format_validation_report(result)
        assert isinstance(report, str)
        assert len(report) > 0
