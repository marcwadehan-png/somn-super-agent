"""发放率注意力系统 - 单元测试

迁移自 firing_rate_attention.py 第570行的 if __name__ == "__main__" 自测块
"""

import pytest


class TestFiringRateAttention:
    """发放率注意力分配系统测试"""

    @pytest.fixture
    def attention(self):
        from src.neural_memory.firing_rate_attention import create_attention_system
        return create_attention_system(capacity=100)

    @pytest.fixture
    def loaded_attention(self, attention):
        """加载 5 个知识项目"""
        items = [
            ("brand_strategy", "品牌strategy", 10.0, 0.9),
            ("private_domain", "私域运营", 8.0, 0.8),
            ("user_growth", "用户增长", 12.0, 0.95),
            ("content_marketing", "内容营销", 6.0, 0.7),
            ("data_analysis", "数据分析", 9.0, 0.85),
        ]
        for name, content, base_rate, priority in items:
            attention.add_item(name, content, base_rate, priority)
        return attention

    def test_create_system(self, attention):
        assert attention is not None

    def test_add_items(self, loaded_attention):
        stats = loaded_attention.get_statistics()
        assert stats is not None

    def test_update_and_weights(self, loaded_attention):
        inputs = {
            "brand_strategy": 0.9, "private_domain": 0.7,
            "user_growth": 1.0, "content_marketing": 0.5,
            "data_analysis": 0.8,
        }
        loaded_attention.update(inputs, dt=1.0)
        weights = loaded_attention.get_attention_weights()
        assert isinstance(weights, dict)
        assert len(weights) > 0
        # 验证权重均为正数且总和为1
        assert all(w > 0 for w in weights.values())
        assert abs(sum(weights.values()) - 1.0) < 0.01

    def test_get_statistics(self, loaded_attention):
        inputs = {"user_growth": 1.0, "data_analysis": 0.8}
        loaded_attention.update(inputs, dt=1.0)
        stats = loaded_attention.get_statistics()
        assert isinstance(stats, dict)

    def test_visualize_attention(self, loaded_attention):
        inputs = {"user_growth": 1.0}
        loaded_attention.update(inputs, dt=1.0)
        viz = loaded_attention.visualize_attention()
        assert viz is not None
        assert 'winners' in viz
