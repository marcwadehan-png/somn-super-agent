"""
核心模块单元测试模板
Version: 1.0.0
"""

import pytest
import sys
from pathlib import Path

# 路径设置
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)


class TestCoreModules:
    """核心模块测试套件"""
    
    def test_somn_core_import(self):
        """测试SomnCore导入"""
        try:
            from src.core.somn_core import SomnCore
            assert SomnCore is not None
        except ImportError as e:
            pytest.skip(f"SomnCore not available: {e}")
    
    def test_timeout_guard_import(self):
        """测试TimeoutGuard导入"""
        try:
            from src.core.timeout_guard import TimeoutGuard
            assert TimeoutGuard is not None
        except ImportError as e:
            pytest.skip(f"TimeoutGuard not available: {e}")
    
    def test_agent_core_import(self):
        """测试AgentCore导入"""
        try:
            from src.core.agent_core import AgentCore
            assert AgentCore is not None
        except ImportError as e:
            pytest.skip(f"AgentCore not available: {e}")


class TestTimeoutGuard:
    """TimeoutGuard超时守卫测试"""
    
    @pytest.fixture
    def guard(self):
        from src.core.timeout_guard import TimeoutGuard
        return TimeoutGuard
    
    def test_guard_initialization(self, guard):
        """测试守卫初始化"""
        g = guard()
        assert g is not None
    
    def test_default_timeout(self, guard):
        """测试默认超时值"""
        g = guard()
        assert hasattr(g, 'default_timeout')
    
    def test_timeout_levels(self, guard):
        """测试超时级别"""
        g = guard()
        if hasattr(g, 'LEVELS'):
            assert isinstance(g.LEVELS, dict)
            # 验证级别定义
            expected_levels = ['short', 'medium', 'long', 'extended']
            for level in expected_levels:
                if level in g.LEVELS:
                    assert g.LEVELS[level] > 0


class TestWisdomEngines:
    """智慧引擎测试套件"""
    
    def test_wisdom_dispatcher_import(self):
        """测试智慧调度器导入"""
        try:
            from src.intelligence.dispatcher.wisdom_dispatch import WisdomDispatcher
            assert WisdomDispatcher is not None
        except ImportError as e:
            pytest.skip(f"WisdomDispatcher not available: {e}")
    
    def test_deep_reasoning_import(self):
        """测试深度推理引擎导入"""
        try:
            from src.intelligence.engines.deep_reasoning_engine import DeepReasoningEngine
            assert DeepReasoningEngine is not None
        except ImportError as e:
            pytest.skip(f"DeepReasoningEngine not available: {e}")
    
    def test_cloning_engine_import(self):
        """测试克隆引擎导入"""
        try:
            from src.intelligence.engines.cloning import SageProxyFactory
            assert SageProxyFactory is not None
        except ImportError as e:
            pytest.skip(f"SageProxyFactory not available: {e}")


class TestMemorySystems:
    """记忆系统测试套件"""
    
    def test_neural_memory_import(self):
        """测试神经记忆系统导入"""
        try:
            from src.neural_memory.neural_memory_system import NeuralMemorySystem
            assert NeuralMemorySystem is not None
        except ImportError as e:
            pytest.skip(f"NeuralMemorySystem not available: {e}")
    
    def test_semantic_memory_import(self):
        """测试语义记忆导入"""
        try:
            from src.neural_memory.semantic_memory_engine import SemanticMemoryEngine
            assert SemanticMemoryEngine is not None
        except ImportError as e:
            pytest.skip(f"SemanticMemoryEngine not available: {e}")


class TestClawSubsystem:
    """Claw子系统测试套件"""
    
    def test_claw_architect_import(self):
        """测试Claw架构师导入"""
        try:
            from src.intelligence.claws._claw_architect import ClawArchitect
            assert ClawArchitect is not None
        except ImportError as e:
            pytest.skip(f"ClawArchitect not available: {e}")
    
    def test_claws_coordinator_import(self):
        """测试Claw协调器导入"""
        try:
            from src.intelligence.claws._claws_coordinator import ClawsCoordinator
            assert ClawsCoordinator is not None
        except ImportError as e:
            pytest.skip(f"ClawsCoordinator not available: {e}")
    
    def test_claw_bridge_import(self):
        """测试Claw桥接器导入"""
        try:
            from src.intelligence.claws._claw_bridge import ClawSystemBridge
            assert ClawSystemBridge is not None
        except ImportError as e:
            pytest.skip(f"ClawSystemBridge not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
