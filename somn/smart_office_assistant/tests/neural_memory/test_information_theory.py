"""信息论检索 - 单元测试

迁移自 information_theory_retrieval.py 第552行的 if __name__ == "__main__" 自测块
"""

import pytest
import numpy as np


class TestInformationTheoryRetrieval:
    """信息论检索系统测试"""

    def test_create_system(self):
        from src.neural_memory.information_theory_retrieval import create_info_retrieval_system
        system = create_info_retrieval_system()
        assert system is not None

    def test_index_and_retrieve(self):
        from src.neural_memory.information_theory_retrieval import create_info_retrieval_system
        system = create_info_retrieval_system()

        knowledge_items = [
            ("k1", "品牌定位是企业在市场中的独特形象和价值主张"),
            ("k2", "私域流量运营需要建立用户信任和长期关系"),
            ("k3", "用户增长strategy包括渠道拓展,转化优化,留存提升"),
            ("k4", "内容营销通过有价值的内容吸引和留住目标用户"),
            ("k5", "数据分析驱动decision,衡量营销效果和用户行为"),
        ]
        for kid, content in knowledge_items:
            system.index_knowledge(kid, content)

        relevance_scores = {
            "k1": 0.1, "k2": 0.2, "k3": 0.95,
            "k4": 0.3, "k5": 0.6,
        }
        results = system.retrieve("用户增长", relevance_scores, top_k=3)
        assert isinstance(results, list)
        assert len(results) <= 3
        # 最相关的应在前面
        if results:
            top_id = results[0].get('knowledge_id')
            assert top_id == "k3"

    def test_get_statistics(self):
        from src.neural_memory.information_theory_retrieval import create_info_retrieval_system
        system = create_info_retrieval_system()
        system.index_knowledge("s1", "测试知识")
        stats = system.get_statistics()
        assert isinstance(stats, dict)


class TestEntropyCalculator:
    """熵计算测试（迁移自原自测块）"""

    def test_entropy_calculation(self):
        from src.neural_memory.information_theory_retrieval import EntropyCalculator
        probs = np.array([0.3, 0.25, 0.2, 0.15, 0.1])
        h = EntropyCalculator.entropy(probs)
        assert isinstance(h, float)
        assert h > 0  # 熵为正

    def test_entropy_uniform(self):
        from src.neural_memory.information_theory_retrieval import EntropyCalculator
        probs = np.array([0.5, 0.5])
        h = EntropyCalculator.entropy(probs)
        assert h == pytest.approx(1.0, abs=0.01)  # 均匀分布熵最大

    def test_mutual_information(self):
        from src.neural_memory.information_theory_retrieval import EntropyCalculator
        p_x = np.array([0.5, 0.5])
        p_y = np.array([0.6, 0.4])
        p_xy = np.array([0.35, 0.15, 0.25, 0.25])
        mi = EntropyCalculator.mutual_information(p_x, p_y, p_xy)
        assert isinstance(mi, (int, float))
        assert mi >= 0  # 互信息非负
