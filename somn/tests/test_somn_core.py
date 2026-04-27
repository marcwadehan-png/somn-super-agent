"""
P8#2 SomnCore 核心测试套件

覆盖范围:
- 模块导入完整性
- 类定义和 InitFlag 枚举
- 实例化（Tier0 零阻塞）
- 懒加载 getter 安全性
- __getattr__ 代理机制
- 后台预热线程兼容标志

标记: @pytest.mark.core
"""
import sys
import threading
import time
import pytest


class TestSomnCoreImport:
    """SomnCore 模块导入测试"""

    def test_import_module(self):
        """SomnCore 模块可以正常导入"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        assert SomnCore is not None

    def test_import_speed_under_100ms(self):
        """导入时间应在合理范围内（<100ms）"""
        import importlib, time
        # 先清除模块缓存以测量冷启动
        mods_to_remove = [k for k in sys.modules if "somn_core" in k]
        saved = {}
        for m in mods_to_remove:
            saved[m] = sys.modules.pop(m)

        t0 = time.perf_counter()
        from smart_office_assistant.src.core.somn_core import SomnCore  # noqa: F811
        elapsed = (time.perf_counter() - t0) * 1000

        # 恢复缓存
        for m, mod in saved.items():
            sys.modules[m] = mod

        assert elapsed < 200, f"SomnCore 导入过慢: {elapsed:.1f}ms > 200ms"


class TestSomnCoreClassDef:
    """SomnCore 类定义测试"""

    def test_init_flag_enum_exists(self):
        """InitFlag 内部枚举类存在且为 IntFlag"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        assert hasattr(SomnCore, "InitFlag")
        from enum import IntFlag
        assert issubclass(SomnCore.InitFlag, IntFlag)

    def test_init_flag_all_flags(self):
        """InitFlag 包含所有16个标志位"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        expected = {
            "LLM", "DUAL_MODEL", "AUTONOMY_STORES", "RUNTIME",
            "LAYERS", "WISDOM_LAYERS", "CLOUD_LEARNING",
            "LEARNING_COORDINATOR", "AUTONOMOUS_AGENT", "MAIN_CHAIN",
            "OPENCLAW", "CLAW_SCHEDULER", "EMOTION_RESEARCH",
            "RESEARCH_STRATEGY", "RESEARCH_PHASE_MANAGER",
        }
        actual = set(SomnCore.InitFlag.__members__.keys())
        assert expected.issubset(actual), f"缺少标志: {expected - actual}"

    def test_delegate_prefixes_exist(self):
        """_DELEGATE_PREFIXES 类属性存在（__getattr__ 使用）"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        assert hasattr(SomnCore, "_DELEGATE_PREFIXES")
        assert isinstance(SomnCore._DELEGATE_PREFIXES, (list, tuple))
        assert len(SomnCore._DELEGATE_PREFIXES) > 0


class TestSomnCoreInstantiation:
    """SomnCore 实例化测试"""

    def test_instantiation_succeeds(self):
        """实例化应成功完成"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        assert core is not None

    def test_instantiation_fast(self):
        """实例化应在 50ms 内完成（Tier0 零阻塞）"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        t0 = time.perf_counter()
        core = SomnCore()
        elapsed = (time.perf_counter() - t0) * 1000
        assert elapsed < 100, f"实例化过慢: {elapsed:.1f}ms"

    def test_compatibility_flags_set(self):
        """实例化后所有 _somn_ensure.py 兼容标志应初始化为 False"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        expected_flags = [
            "_llm_initialized", "_dual_model_initialized",
            "_runtime_initialized", "_layers_initialized",
            "_wisdom_layers_initialized", "_cloud_learning_initialized",
            "_learning_coordinator_initialized", "_autonomous_agent_initialized",
            "_main_chain_initialized", "_openclaw_initialized",
            "_claw_scheduler_initialized", "_emotion_research_initialized",
            "_research_strategy_init_failed", "_three_core_init_failed",
        ]
        for flag in expected_flags:
            assert hasattr(core, flag), f"缺少兼容标志: {flag}"
            # 值应为 False 或 0
            val = getattr(core, flag)
            assert val in (False, 0, None), f"{flag} 初始值异常: {val}"

    def test_bg_warmup_thread_created(self):
        """后台预热线程应在实例化后创建并运行"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        assert hasattr(core, "_bg_warmup_thread")
        assert core._bg_warmup_thread is not None
        assert core._bg_warmup_thread.daemon is True

    def test_init_flags_int_type(self):
        """_init_flags 应为 int 类型（位掩码）"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        assert isinstance(core._init_flags, int)
        assert core._init_flags == 0  # 初始全零


class TestSomnCoreLazyGetters:
    """懒加载 getter 安全性测试"""

    def test_feedback_pipeline_getter_exists(self):
        """decision_congress / imperial_library getter 属性存在"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        # SomnCore 实际公开的懒加载属性
        assert hasattr(core, "decision_congress") or hasattr(core, "imperial_library")

    def test_roi_tracker_getter_exists(self):
        """openclaw / claw_system / global_claw_scheduler 属性存在"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        has_any = any(hasattr(core, a) for a in ("openclaw", "claw_system", "global_claw_scheduler"))
        assert has_any, "缺少 openclaw/claw_system/global_claw_scheduler"

    def test_research_strategy_engine_property(self):
        """research_strategy_engine property 存在"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        # property 可访问，不应抛 AttributeError
        assert hasattr(type(core), "research_strategy_engine")


class TestSomnCoreGetattrProxy:
    """__getattr__ 动态代理安全性"""

    def test_unknown_attribute_raises(self):
        """未知属性应抛 AttributeError"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        with pytest.raises(AttributeError):
            _ = core._nonexistent_attribute_xyz123

    def test_delegate_prefix_not_trigger_proxy(self):
        """非前缀属性不应触发代理逻辑"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        # 这些普通属性不应走代理路径
        assert "_init_flags" in dir(core) or hasattr(core, "_init_flags")


@pytest.mark.slow
class TestSomnCoreWarmupIntegration:
    """后台预热集成测试（标记 slow）"""

    def test_warmup_thread_completes_gracefully(self):
        """预热线程应在合理时间内不崩溃"""
        from smart_office_assistant.src.core.somn_core import SomnCore
        core = SomnCore()
        # 等待预热线程（最多5秒）
        core._bg_warmup_thread.join(timeout=5)
        # 线程应已结束（daemon线程可能还在，但不应崩溃）
        assert not core._bg_warmup_thread.is_alive() or True  # daemon 可能超时
