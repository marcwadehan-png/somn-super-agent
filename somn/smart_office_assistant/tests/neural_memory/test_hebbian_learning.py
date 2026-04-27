"""Hebbian 学习引擎 - 单元测试

迁移自 hebbian_learning_engine.py 第459行的 if __name__ == "__main__" 自测块
"""

import pytest
import numpy as np


class TestHebbianLearningEngine:
    """Hebbian 关联学习引擎测试"""

    @pytest.fixture
    def engine(self):
        from src.neural_memory.hebbian_learning_engine import HebbianLearningEngine
        return HebbianLearningEngine(learning_rate=0.1)

    @pytest.fixture
    def loaded_engine(self, engine):
        """加载 6 个概念并学习 2 对关联"""
        concepts = [
            ("brand", "Brand"), ("marketing", "Marketing"),
            ("private_domain", "Private Domain"), ("growth", "Growth"),
            ("user", "User"), ("repurchase", "Repurchase"),
        ]
        for cid, name in concepts:
            engine.add_concept(cid, name)
        return engine

    def test_construction(self, engine):
        assert engine is not None

    def test_add_concepts(self, loaded_engine):
        stats = loaded_engine.get_network_statistics()
        assert stats['num_concepts'] == 6

    def test_learn_changes_weight(self, loaded_engine):
        r = loaded_engine.learn("brand", "marketing", pre_activity=0.9, post_activity=0.8)
        assert r is not None
        assert r.old_weight is not None
        assert r.new_weight is not None
        # 学习后权重应增加（Hebb 规则）
        assert r.new_weight >= r.old_weight

    def test_learn_multiple_pairs(self, loaded_engine):
        r1 = loaded_engine.learn("private_domain", "user",
                                 pre_activity=0.8, post_activity=0.9)
        r2 = loaded_engine.learn("brand", "marketing",
                                 pre_activity=0.9, post_activity=0.8)
        assert r1 is not None and r2 is not None

    def test_get_associated_concepts(self, loaded_engine):
        loaded_engine.learn("private_domain", "user",
                            pre_activity=0.8, post_activity=0.9)
        associations = loaded_engine.get_associated_concepts("user", top_k=5)
        assert isinstance(associations, list)
        assert len(associations) <= 5

    def test_network_statistics(self, loaded_engine):
        loaded_engine.learn("brand", "marketing", pre_activity=0.9, post_activity=0.8)
        stats = loaded_engine.get_network_statistics()
        assert 'num_concepts' in stats
        assert 'num_synapses' in stats
        assert stats['num_concepts'] == 6
        assert stats['num_synapses'] >= 1
