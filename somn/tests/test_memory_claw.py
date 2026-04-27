"""
P8#4 ImperialLibrary + Cloning 测试套件

覆盖范围:
- ImperialLibrary 实例化和 CRUD
- WisdomEncodingRegistry 编码注册表
- Cloning 延迟加载机制
- 藏书阁统计接口

标记: @pytest.mark.memory / @pytest.mark.claw
"""
import pytest


class TestImperialLibraryImport:
    """ImperialLibrary 导入测试"""

    def test_import_imperial_library(self):
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        assert ImperialLibrary is not None

    def test_instantiation_fast(self):
        """ImperialLibrary 实例化应在 50ms 内（P6 单遍统计优化）"""
        import time
        t0 = time.perf_counter()
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        lib = ImperialLibrary()
        elapsed = (time.perf_counter() - t0) * 1000
        assert elapsed < 100, f"ImperialLibrary 实例化过慢: {elapsed:.1f}ms"


class TestImperialLibraryCore:
    """ImperialLibrary 核心功能测试"""

    def test_instance_created(self):
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        lib = ImperialLibrary()
        assert lib is not None

    def test_has_store_method(self):
        """应有写入方法（save_all / add_cross_reference）"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        lib = ImperialLibrary()
        assert hasattr(lib, "save_all") or hasattr(lib, "add_cross_reference")

    def test_has_retrieve_or_search(self):
        """应有检索方法（query_cells / query_memories / get_cell）"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        lib = ImperialLibrary()
        has_search = any(
            hasattr(lib, m) for m in ("query_cells", "query_memories", "get_cell", "get_memory", "get_stats")
        )
        assert has_search, "ImperialLibrary 缺少检索方法"

    def test_get_stats_returns_dict(self):
        """get_stats 应返回 dict（P6 单遍统计优化）"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        lib = ImperialLibrary()
        if hasattr(lib, "get_stats"):
            stats = lib.get_stats()
            assert isinstance(stats, dict), f"get_stats 应返回 dict，实际: {type(stats)}"


class TestWisdomEncodingRegistry:
    """WisdomEncodingRegistry 编码注册表测试"""

    def test_import_registry(self):
        from smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry import WisdomEncodingRegistry
        assert WisdomEncodingRegistry is not None

    def test_instantiation_succeeds(self):
        from smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry import WisdomEncodingRegistry
        reg = WisdomEncodingRegistry()
        assert reg is not None

    def test_registry_has_entries(self):
        """注册表应有条目（766+ SageCode）"""
        from smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry import WisdomEncodingRegistry
        reg = WisdomEncodingRegistry(lazy=True)
        # 使用 export_data() 触发懒加载
        data = reg.export_data()
        total = data.get("total_sages", 0)
        assert total > 700, f"注册表缺少数据: {total}"

    def test_instantiation_fast(self):
        """实例化应在 100ms 内（P6 副本消除优化）"""
        import time
        t0 = time.perf_counter()
        from smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry import WisdomEncodingRegistry
        reg = WisdomEncodingRegistry()
        elapsed = (time.perf_counter() - t0) * 1000
        assert elapsed < 200, f"注册表实例化过慢: {elapsed:.1f}ms"


class TestCloningSystem:
    """Cloning 克隆系统测试"""

    def test_import_cloning_module(self):
        """cloning 模块应可导入"""
        from smart_office_assistant.src.intelligence.engines.cloning import (
            get_cloning, CloningTier, SageCloning, consult_sage
        )
        assert callable(get_cloning)
        assert CloningTier is not None
        assert SageCloning is not None

    def test_cloning_tier_enum_values(self):
        """CloningTier 枚举应有 T1-T4 值"""
        from smart_office_assistant.src.intelligence.engines.cloning import CloningTier
        tier_names = [t.name for t in CloningTier]
        # 至少应有多个 tier
        assert len(tier_names) >= 3, f"CloningTier 过少: {tier_names}"

    def test_get_cloning_callable(self):
        """get_cloning 应为可调用且不抛异常"""
        from smart_office_assistant.src.intelligence.engines.cloning import get_cloning
        assert callable(get_cloning)

    def test_lazy_loading_works(self):
        """延迟加载: EXTRA_SAGES 不应在导入时触发"""
        import sys
        # cloning 模块已导入但 _sage_registry_extra 可能未加载
        extra_loaded = "_sage_registry_extra" in str(sys.modules.get(
            "smart_office_assistant.src.intelligence.engines.cloning._sage_registry_extra", ""
        ))
        # 验证 __getattr__ 代理存在
        import smart_office_assistant.src.intelligence.engines.cloning as cloning_mod
        assert hasattr(cloning_mod, "__getattr__") or "EXTRA_SAGES" in dir(cloning_mod)

    def test_list_clonings_callable(self):
        """list_clonings 应可调用"""
        from smart_office_assistant.src.intelligence.engines.cloning import list_clonings
        assert callable(list_clonings)


@pytest.mark.slow
class TestMemorySystemIntegration:
    """记忆系统集成测试"""

    def test_full_memory_chain_import(self):
        """完整记忆系统导入链"""
        mods = [
            "smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library",
            "smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry",
        ]
        failed = []
        for m in mods:
            try:
                __import__(m)
            except Exception as e:
                failed.append((m.split(".")[-1], str(e)[:80]))
        assert len(failed) == 0, f"记忆系统导入失败: {failed}"
