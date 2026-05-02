"""
神政轨快速加载模式 - 性能基准测试
======================================

测试 v2.5.0 / v3.2 极致轻量加载优化的性能指标。

用法:
    cd d:/AI/somn/smart_office_assistant
    python -m pytest src/intelligence/dual_track/test_load_speed.py -v -s
"""

import time
import sys
import subprocess
import pytest


class TestImportColdStart:
    """Test 1: import dual_track 只加载 track_a.py"""

    def test_only_track_a_loaded(self):
        """v3.2: import dual_track 不应加载 bridge/track_b"""
        result = subprocess.run(
            [sys.executable, "-c",
             "from src.intelligence.dual_track import get_loading_stats; "
             "s = get_loading_stats(); "
             "print(f'Modules: {s[\"loaded_modules\"]}')"],
            capture_output=True, text=True, cwd=r"d:\AI\somn\smart_office_assistant"
        )
        assert "Modules: []" in result.stdout, \
            f"Expected no modules loaded on import. stdout={result.stdout!r}"


class TestTrackAInit:
    """Test 2: Track A 初始化应接近空操作"""

    def test_track_a_init_lightweight(self):
        from src.intelligence.dual_track.track_a import DivineGovernanceTrack
        start = time.perf_counter()
        track = DivineGovernanceTrack()
        elapsed = (time.perf_counter() - start) * 1000
        assert track is not None
        assert elapsed < 100, f"Track A init too slow: {elapsed:.1f}ms (expected <100ms)"


class TestSupervisionSystem:
    """Test 3: 监管系统使用共享Factory"""

    def test_shared_factory_mode(self):
        """验证两个引擎共享同一个Factory实例"""
        from src.intelligence.dual_track.track_a import DivineGovernanceTrack
        track = DivineGovernanceTrack()
        track._init_supervision_system()
        assert track._supervision_factory is not None
        assert track._jindu_engine is not None
        assert track._whiplash_engine is not None
        assert id(track._jindu_engine.factory) == id(track._supervision_factory), \
            "JinDuCuJinEngine should share the same factory instance"
        assert id(track._whiplash_engine.factory) == id(track._supervision_factory), \
            "AdministrativeWhipEngine should share the same factory instance"


class TestFactoryCount:
    """Test 4: 只创建1个Factory实例"""

    def test_single_factory_instance(self):
        from src.intelligence.dual_track.track_a import DivineGovernanceTrack
        from src.intelligence.dual_track import _supervision_claws

        orig_init = _supervision_claws.SupervisionClawFactory.__init__
        count = [0]

        def counting_init(self):
            count[0] += 1
            orig_init(self)

        _supervision_claws.SupervisionClawFactory.__init__ = counting_init
        try:
            track = DivineGovernanceTrack()
            track._init_supervision_system()
            track.auto_appoint_all()
        finally:
            _supervision_claws.SupervisionClawFactory.__init__ = orig_init

        assert count[0] == 1, f"Expected 1 Factory, got {count[0]}"


class TestLazyLoading:
    """Test 5: 所有非A轨符号懒加载透明"""

    def test_b_track_symbols_accessible(self):
        """通过__getattr__可以正常访问B轨符号"""
        from src.intelligence.dual_track import (
            DivineExecutionTrack,
            ClawAppointmentSystem,
            CallerType,
            ALL_DEPARTMENTS,
        )
        assert DivineExecutionTrack is not None
        assert CallerType.A_GOVERNANCE.value in [e.value for e in CallerType]
        assert "礼部" in ALL_DEPARTMENTS

    def test_bridge_symbols_accessible(self):
        """通过__getattr__可以正常访问bridge符号"""
        from src.intelligence.dual_track import (
            TrackBridge,
            DualTrackSystem,
            DivineExecutionBridge,
            DepartmentMapper,
        )
        assert TrackBridge is not None
        assert DualTrackSystem is not None
        assert DivineExecutionBridge is not None
        assert DepartmentMapper is not None


class TestFullSystem:
    """Test 6: 完整双轨系统创建"""

    def test_full_system_creation(self):
        from src.intelligence.dual_track.bridge import TrackBridge
        bridge = TrackBridge()
        start = time.perf_counter()
        system = bridge.create_system()
        elapsed = (time.perf_counter() - start) * 1000
        assert system is not None
        assert system.track_a is not None
        assert system.track_b is not None
        print(f"\n  Full system creation: {elapsed:.1f}ms")


class TestVersionInfo:
    """Test 7: 版本号正确"""

    def test_version(self):
        from src.intelligence.dual_track import get_loading_stats
        stats = get_loading_stats()
        assert stats["governance_version"] == "v2.5.0"
        assert stats["version"] == "v3.2"


class TestMemoryOptimization:
    """Test 8: v3.2 内存优化验证"""

    def test_supervision_config_is_class_level(self):
        """_SUPERVISION_CONFIG 应为类级共享"""
        from src.intelligence.dual_track._supervision_claws import SupervisionClaw
        assert isinstance(SupervisionClaw._SUPERVISION_CONFIG, dict)
        assert len(SupervisionClaw._SUPERVISION_CONFIG) == 4

    def test_knowledge_layer_is_shared(self):
        """所有SupervisionClaw应共享同一个知识层"""
        from src.intelligence.dual_track._supervision_claws import (
            SupervisionClaw, SupervisionType, SupervisionLevel
        )
        claw1 = SupervisionClaw("test1", SupervisionType.PROGRESS, "T1", "D1")
        claw2 = SupervisionClaw("test2", SupervisionType.QUALITY, "T2", "D2")
        assert claw1.knowledge_layer is claw2.knowledge_layer, \
            "All SupervisionClaws should share the same KnowledgeLayer instance"
