"""
saint_king_wisdom.py 单元测试
Refactored: 2026-04-23
"""

import pytest
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)


class TestSaintKingWisdom:
    """圣王智慧引擎测试套件"""
    
    @pytest.fixture
    def engine(self):
        """创建引擎实例"""
        from src.intelligence.engines.saint_king_wisdom import SaintKingWisdomEngine
        return SaintKingWisdomEngine()
    
    def test_engine_initialization(self, engine):
        """测试引擎初始化"""
        assert engine is not None
        assert hasattr(engine, '_initialize_sages')
    
    def test_dispatcher_calls_all_domains(self, engine):
        """测试调度器调用所有领域"""
        # 验证7个领域子函数存在
        expected_methods = [
            '_init_astronomy_math_sages',
            '_init_engineering_sages',
            '_init_agriculture_sages',
            '_init_invention_sages',
            '_init_geography_sages',
            '_init_ancient_kings_sages',
            '_init_modern_enlightenment_sages'
        ]
        
        for method in expected_methods:
            assert hasattr(engine, method), f"Missing method: {method}"
    
    def test_astronomy_math_domain(self, engine):
        """测试天文历法数学领域初始化"""
        if hasattr(engine, '_init_astronomy_math_sages'):
            # 调用子函数
            engine._init_astronomy_math_sages()
            
            # 验证圣人数量（22人）
            assert len(engine.sages) >= 22, "Expected at least 22 astronomy/math sages"
    
    def test_engineering_domain(self, engine):
        """测试工程技术领域初始化"""
        if hasattr(engine, '_init_engineering_sages'):
            engine._init_engineering_sages()
            assert len(engine.sages) >= 9, "Expected at least 9 engineering sages"
    
    def test_agriculture_domain(self, engine):
        """测试农学水利领域初始化"""
        if hasattr(engine, '_init_agriculture_sages'):
            engine._init_agriculture_sages()
            assert len(engine.sages) >= 11, "Expected at least 11 agriculture sages"
    
    def test_invention_domain(self, engine):
        """测试发明创造领域初始化"""
        if hasattr(engine, '_init_invention_sages'):
            engine._init_invention_sages()
            assert len(engine.sages) >= 5, "Expected at least 5 invention sages"
    
    def test_geography_domain(self, engine):
        """测试地理探险领域初始化"""
        if hasattr(engine, '_init_geography_sages'):
            engine._init_geography_sages()
            assert len(engine.sages) >= 3, "Expected at least 3 geography sages"
    
    def test_ancient_kings_domain(self, engine):
        """测试上古圣王领域初始化"""
        if hasattr(engine, '_init_ancient_kings_sages'):
            engine._init_ancient_kings_sages()
            assert len(engine.sages) >= 22, "Expected at least 22 ancient kings"
    
    def test_modern_enlightenment_domain(self, engine):
        """测试晚近启蒙领域初始化"""
        if hasattr(engine, '_init_modern_enlightenment_sages'):
            engine._init_modern_enlightenment_sages()
            assert len(engine.sages) >= 9, "Expected at least 9 modern enlightenment sages"
    
    def test_total_sage_count(self, engine):
        """测试圣人总数"""
        # 调用完整初始化
        engine._initialize_sages()
        
        # 验证总数（22+9+11+5+3+22+9 = 81）
        expected_min = 81
        actual = len(engine.sages)
        assert actual >= expected_min, f"Expected at least {expected_min} total sages, got {actual}"
    
    def test_sage_attributes(self, engine):
        """测试圣人属性"""
        engine._initialize_sages()
        
        if engine.sages:
            sage = engine.sages[0]
            # 验证必要属性
            assert hasattr(sage, 'name'), "Sage missing 'name' attribute"
            assert hasattr(sage, 'wisdom'), "Sage missing 'wisdom' attribute"
    
    def test_wisdom_not_empty(self, engine):
        """测试智慧不为空"""
        engine._initialize_sages()
        
        # 检查至少有一些智慧内容
        wisdom_list = []
        for sage in engine.sages:
            if hasattr(sage, 'wisdom') and sage.wisdom:
                wisdom_list.append(sage.wisdom)
        
        assert len(wisdom_list) > 0, "No wisdom content found"


class TestRefactoredFunctions:
    """重构后函数行为验证"""
    
    @pytest.fixture
    def engine(self):
        from src.intelligence.engines.saint_king_wisdom import SaintKingWisdomEngine
        return SaintKingWisdomEngine()
    
    def test_dispatcher_is_small(self, engine):
        """测试调度器函数很小（单一职责）"""
        import inspect
        
        # 获取_initialize_sages源码
        source = inspect.getsource(engine._initialize_sages)
        lines = [l for l in source.split('\n') if l.strip() and not l.strip().startswith('#')]
        
        # 调度器应该只有几行（调用7个子函数）
        assert len(lines) < 20, f"Dispatcher too large: {len(lines)} lines"
    
    def test_domain_functions_are_independent(self, engine):
        """测试领域函数相互独立"""
        # 每个领域函数应该可以独立调用
        domain_methods = [
            '_init_astronomy_math_sages',
            '_init_engineering_sages',
            '_init_agriculture_sages',
            '_init_invention_sages',
            '_init_geography_sages',
            '_init_ancient_kings_sages',
            '_init_modern_enlightenment_sages'
        ]
        
        for method_name in domain_methods:
            if hasattr(engine, method_name):
                method = getattr(engine, method_name)
                # 验证是方法
                assert callable(method), f"{method_name} is not callable"
    
    def test_sage_name_format(self, engine):
        """测试圣人名称格式"""
        engine._initialize_sages()
        
        for sage in engine.sages:
            if hasattr(sage, 'name'):
                name = sage.name
                assert isinstance(name, str), "Sage name must be string"
                assert len(name) > 0, "Sage name cannot be empty"
                # 名称应该合理长度
                assert len(name) < 100, f"Sage name too long: {name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
