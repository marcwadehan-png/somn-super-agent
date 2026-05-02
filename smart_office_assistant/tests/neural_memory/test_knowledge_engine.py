"""知识引擎 - 单元测试

迁移自 knowledge_engine.py 第531行的 if __name__ == "__main__" 自测块
"""

import pytest


class TestKnowledgeEngine:
    """知识库引擎测试"""

    @pytest.fixture
    def engine(self):
        from src.neural_memory.knowledge_engine import KnowledgeEngine
        return KnowledgeEngine()

    def test_construction(self, engine):
        assert engine is not None

    def test_add_concept(self, engine):
        concept_id = engine.add_concept("情绪概念", {
            "概念名": "愉悦情绪",
            "定义": "积极正向的情绪状态",
            "characteristics": ["面部微笑", "语调轻快", "行为活跃"],
            "触发因素": ["奖励", "惊喜", "社交认可"],
            "行为影响": ["购买意愿提升", "分享意愿提升"],
        })
        assert concept_id is not None

    def test_add_rule(self, engine):
        rule_id = engine.add_rule("演绎规则", {
            "名称": "情绪-行为关联规则",
            "前提": ["用户处于特定情绪状态", "情绪强度 > 阈值"],
            "结论": "用户将表现出与该情绪相关的行为倾向",
            "置信度": 0.72,
            "适用范围": ["冲动消费场景", "体验消费场景"],
        })
        assert rule_id is not None

    def test_get_statistics(self, engine):
        engine.add_concept("测试概念", {"定义": "测试"})
        stats = engine.get_statistics()
        assert isinstance(stats, dict)
