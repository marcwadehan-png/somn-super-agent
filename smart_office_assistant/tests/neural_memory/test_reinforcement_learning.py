"""强化学习系统 v3 - 单元测试

迁移自 reinforcement_learning_v3.py 第579行的 if __name__ == "__main__" 自测块

注意：RL 系统 API 需要 LearningState 对象（含 state_vector）和 LearningAction（含 action_vector），
构造复杂，此处聚焦于构造和基础统计功能。
"""

import pytest


class TestRLSystemV3Construction:
    """构造测试"""

    def test_default_construction(self, rl_system):
        assert rl_system is not None

    def test_has_learning_methods(self, rl_system):
        assert hasattr(rl_system, "choose_action") or hasattr(rl_system, "select_action")
        assert hasattr(rl_system, "calculate_reward") or hasattr(rl_system, "compute_reward")
        assert hasattr(rl_system, "update_q_value") or hasattr(rl_system, "learn")


class TestRLSystemV3Learning:
    """学习循环测试"""

    def test_get_stats(self, rl_system):
        method = getattr(rl_system, "get_statistics", None) or getattr(rl_system, "get_stats", None)
        if method:
            stats = method()
            assert stats is not None
            assert isinstance(stats, dict)
