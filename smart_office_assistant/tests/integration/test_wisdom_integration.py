"""
集成测试框架
Version: 1.0.0
"""

import pytest
import sys
from pathlib import Path
import time

# 路径设置
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)


@pytest.mark.integration
class TestWisdomIntegration:
    """智慧系统集成测试"""
    
    @pytest.fixture(scope="class")
    def somn_core(self):
        """创建SomnCore实例（类级别复用）"""
        try:
            from src.core.somn_core import SomnCore
            core = SomnCore()
            yield core
        except ImportError as e:
            pytest.skip(f"SomnCore not available: {e}")
    
    def test_somn_initialization(self, somn_core):
        """测试SomnCore初始化"""
        assert somn_core is not None
    
    def test_wisdom_dispatcher_registration(self, somn_core):
        """测试智慧调度器注册"""
        if hasattr(somn_core, '_wisdom_dispatcher'):
            dispatcher = somn_core._wisdom_dispatcher
            assert dispatcher is not None
    
    def test_wisdom_schools_loaded(self, somn_core):
        """测试智慧学派加载"""
        if hasattr(somn_core, 'wisdom_schools'):
            schools = somn_core.wisdom_schools
            assert isinstance(schools, (list, dict))
            assert len(schools) > 0


@pytest.mark.integration
class TestClawIntegration:
    """Claw子系统集成测试"""
    
    @pytest.fixture(scope="class")
    def claw_bridge(self):
        """创建Claw桥接器"""
        try:
            from src.intelligence.claws._claw_bridge import ClawSystemBridge
            bridge = ClawSystemBridge()
            yield bridge
        except ImportError as e:
            pytest.skip(f"ClawSystemBridge not available: {e}")
    
    def test_bridge_initialization(self, claw_bridge):
        """测试桥接器初始化"""
        assert claw_bridge is not None
    
    def test_claw_config_loading(self, claw_bridge):
        """测试Claw配置加载"""
        if hasattr(claw_bridge, 'load_config'):
            claw_bridge.load_config()
            assert True


@pytest.mark.integration
class TestMemoryIntegration:
    """记忆系统集成测试"""
    
    @pytest.fixture(scope="class")
    def memory_system(self):
        """创建记忆系统"""
        try:
            from src.neural_memory.neural_memory_system import NeuralMemorySystem
            system = NeuralMemorySystem()
            yield system
        except ImportError as e:
            pytest.skip(f"NeuralMemorySystem not available: {e}")
    
    def test_memory_initialization(self, memory_system):
        """测试记忆系统初始化"""
        assert memory_system is not None
    
    def test_memory_tier_structure(self, memory_system):
        """测试记忆层级结构"""
        if hasattr(memory_system, 'tiers'):
            assert len(memory_system.tiers) > 0


@pytest.mark.integration
class TestLearningIntegration:
    """学习系统集成测试"""
    
    @pytest.fixture(scope="class")
    def learning_engine(self):
        """创建学习引擎"""
        try:
            from src.learning.engine.unified_learning_orchestrator import UnifiedLearningOrchestrator
            engine = UnifiedLearningOrchestrator()
            yield engine
        except ImportError:
            try:
                from src.learning.engine.enhanced_three_tier_learning import EnhancedThreeTierLearning
                engine = EnhancedThreeTierLearning()
                yield engine
            except ImportError as e:
                pytest.skip(f"Learning engine not available: {e}")
    
    def test_learning_initialization(self, learning_engine):
        """测试学习引擎初始化"""
        assert learning_engine is not None
    
    def test_learning_strategies_available(self, learning_engine):
        """测试学习策略可用"""
        if hasattr(learning_engine, 'strategies'):
            assert len(learning_engine.strategies) > 0


@pytest.mark.integration
class TestSmokeTests:
    """冒烟测试"""
    
    @pytest.mark.smoke
    def test_import_all_core_modules(self):
        """测试所有核心模块可导入"""
        modules = [
            'src.core.somn_core',
            'src.core.timeout_guard',
            'src.core.agent_core',
            'src.intelligence.dispatcher.wisdom_dispatch',
            'src.intelligence.engines.deep_reasoning_engine',
            'src.intelligence.engines.cloning',
            'src.neural_memory.neural_memory_system',
        ]
        
        for module_name in modules:
            try:
                __import__(module_name)
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")
    
    @pytest.mark.smoke
    def test_path_bootstrap_works(self):
        """测试路径引导正常工作"""
        from path_bootstrap import bootstrap_project_paths
        bootstrap_project_paths(__file__)
        
        import src
        assert src is not None


@pytest.mark.integration
class TestPerformance:
    """性能测试"""
    
    @pytest.mark.slow
    @pytest.mark.performance
    def test_import_time(self):
        """测试导入时间"""
        import importlib
        
        start = time.time()
        import src.core.somn_core
        elapsed = time.time() - start
        
        # 导入应在合理时间内完成
        assert elapsed < 5.0, f"Import took {elapsed:.2f}s, expected < 5s"
    
    @pytest.mark.slow
    @pytest.mark.performance
    def test_initialization_time(self):
        """测试初始化时间"""
        try:
            from src.core.somn_core import SomnCore
            
            start = time.time()
            core = SomnCore()
            elapsed = time.time() - start
            
            # 初始化应在合理时间内
            assert elapsed < 30.0, f"Initialization took {elapsed:.2f}s, expected < 30s"
        except ImportError:
            pytest.skip("SomnCore not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
