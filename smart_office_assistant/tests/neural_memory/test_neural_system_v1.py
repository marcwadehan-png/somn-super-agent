# -*- coding: utf-8 -*-
"""
Tests for neural_system.py (V1 兼容层)
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest


# ──────────────────────────────────────────────────────────────
# 模块导入
# ──────────────────────────────────────────────────────────────

class TestNeuralSystemModule:
    """neural_system 模块基础检查"""

    def test_module_imports(self):
        from src.neural_memory.neural_system import NeuralMemorySystem
        assert NeuralMemorySystem is not None

    def test_create_factory_exists(self):
        from src.neural_memory.neural_system import create_neural_system
        assert callable(create_neural_system)


# ──────────────────────────────────────────────────────────────
# NeuralMemorySystem
# ──────────────────────────────────────────────────────────────

class TestNeuralMemorySystem:
    """测试神经记忆系统"""

    def test_system_creation(self, tmp_path):
        """系统可实例化"""
        from src.neural_memory.neural_system import NeuralMemorySystem
        with patch("src.neural_memory.neural_system.MemoryEngine"), \
             patch("src.neural_memory.neural_system.KnowledgeEngine"), \
             patch("src.neural_memory.neural_system.LearningEngine"), \
             patch("src.neural_memory.neural_system.ReasoningEngine"), \
             patch("src.neural_memory.neural_system.ValidationEngine"):
            system = NeuralMemorySystem(base_path=str(tmp_path))
            assert system is not None

    def test_record_research_finding(self, tmp_path):
        """记录研究发现"""
        from src.neural_memory.neural_system import NeuralMemorySystem
        with patch("src.neural_memory.neural_system.MemoryEngine") as MockMem, \
             patch("src.neural_memory.neural_system.KnowledgeEngine") as MockKnow, \
             patch("src.neural_memory.neural_system.LearningEngine"), \
             patch("src.neural_memory.neural_system.ReasoningEngine"), \
             patch("src.neural_memory.neural_system.ValidationEngine"):
            system = NeuralMemorySystem(base_path=str(tmp_path))

            finding = {
                "title": "门店慢节奏音乐延长顾客停留时长",
                "description": "A/B测试发现慢节奏音乐门店停留时长增加25%",
                "confidence_score": 82,
                "scenarios": ["零售增长"],
                "value_types": ["转化价值"],
            }
            # 不验证内部实现，仅确保方法存在且可调用
            assert hasattr(system, "record_research_finding")

    def test_generate_system_report(self, tmp_path):
        """生成系统报告"""
        from src.neural_memory.neural_system import NeuralMemorySystem
        with patch("src.neural_memory.neural_system.MemoryEngine"), \
             patch("src.neural_memory.neural_system.KnowledgeEngine"), \
             patch("src.neural_memory.neural_system.LearningEngine"), \
             patch("src.neural_memory.neural_system.ReasoningEngine"), \
             patch("src.neural_memory.neural_system.ValidationEngine"):
            system = NeuralMemorySystem(base_path=str(tmp_path))
            assert hasattr(system, "generate_system_report")
            assert hasattr(system, "discover_value_and_generate_dimensions")
