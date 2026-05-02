"""神经编码核心 - 单元测试

迁移自 neural_encoding_core.py 第641行的 if __name__ == "__main__" 自测块
"""

import pytest
import numpy as np


class TestNeuralEncodingCore:
    """神经编码核心系统测试"""

    def test_create_system(self):
        from src.neural_memory.neural_encoding_core import create_neural_coding_system
        system = create_neural_coding_system()
        assert system is not None

    def test_encode_knowledge(self):
        from src.neural_memory.neural_encoding_core import create_neural_coding_system
        system = create_neural_coding_system()

        knowledge_items = [
            {'id': 'k1', 'content': '私域流量运营strategy', 'priority': 8,
             'relevance': 0.9, 'freshness': 0.8},
            {'id': 'k2', 'content': '品牌营销方法论', 'priority': 7,
             'relevance': 0.7, 'freshness': 0.6},
            {'id': 'k3', 'content': '产品设计原则', 'priority': 6,
             'relevance': 0.5, 'freshness': 0.9},
        ]

        for k in knowledge_items:
            result = system.encode(k)
            assert result is not None

    def test_retrieve_by_feature(self):
        from src.neural_memory.neural_encoding_core import create_neural_coding_system
        system = create_neural_coding_system()

        system.encode({'id': 'r1', 'content': '增长策略', 'priority': 8,
                       'relevance': 0.9, 'freshness': 0.8})
        system.encode({'id': 'r2', 'content': '品牌定位', 'priority': 7,
                       'relevance': 0.7, 'freshness': 0.6})

        results = system.retrieve({'feature_value': 0.75}, top_k=3)
        assert isinstance(results, list)
        assert len(results) <= 3
        if results:
            # 验证按 score 排序
            scores = [r.get('score', 0) for r in results]
            assert scores == sorted(scores, reverse=True)

    def test_get_statistics(self):
        from src.neural_memory.neural_encoding_core import create_neural_coding_system
        system = create_neural_coding_system()
        system.encode({'id': 's1', 'content': '测试', 'priority': 5,
                       'relevance': 0.5, 'freshness': 0.5})
        stats = system.get_statistics()
        assert 'total_encodings' in stats
        assert 'avg_intensity' in stats
        assert stats['total_encodings'] >= 1


class TestReceptiveField:
    """感受野测试"""

    def test_gaussian_response(self):
        from src.neural_memory.neural_encoding_core import ReceptiveField, TuningCurveType
        rf = ReceptiveField(
            stimulus_dimension="price",
            preferred_value=100.0,
            bandwidth=20.0,
            curve_type=TuningCurveType.GAUSSIAN,
        )
        resp = rf.get_response(100.0)
        assert resp == pytest.approx(1.0, abs=0.01)  # 最优值处响应最高

    def test_gaussian_response_falloff(self):
        from src.neural_memory.neural_encoding_core import ReceptiveField, TuningCurveType
        rf = ReceptiveField(
            stimulus_dimension="price",
            preferred_value=100.0,
            bandwidth=20.0,
            curve_type=TuningCurveType.GAUSSIAN,
        )
        resp_center = rf.get_response(100.0)
        resp_far = rf.get_response(200.0)
        assert resp_center > resp_far
