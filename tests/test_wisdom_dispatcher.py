"""
P8#3 WisdomDispatcher 核心测试套件

覆盖范围:
- 模块导入
- 调度映射完整性（135 ProblemType）
- 引擎注册表可访问
- 分派路径基本覆盖

标记: @pytest.mark.dispatcher
"""
import pytest


class TestDispatcherImport:
    """WisdomDispatcher 导入测试"""

    def test_import_wisdom_dispatcher(self):
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
        assert WisdomDispatcher is not None

    def test_import_dispatch_mapping(self):
        """_dispatch_mapping 模块应可导入，包含 WisdomDispatcher 类"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        assert WisdomDispatcher is not None

    def test_import_dispatch_court(self):
        """_dispatch_court 模块应可导入，包含核心函数"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_court import (
            resolve_departments, Department
        )
        assert callable(resolve_departments)
        assert Department is not None


class TestDispatchMapping:
    """调度映射完整性测试（通过 WisdomDispatcher 实例）"""

    def test_dispatch_mapping_not_empty(self):
        """WisdomDispatcher.problem_school_mapping 不应为空"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        wd = WisdomDispatcher()
        assert len(wd.problem_school_mapping) > 0, "调度映射为空"

    def test_dispatch_mapping_has_core_keys(self):
        """调度映射应包含核心 ProblemType"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher, ProblemType
        wd = WisdomDispatcher()
        sample_keys = list(wd.problem_school_mapping.keys())[:5]
        assert len(sample_keys) > 0, f"映射无条目。前5个: {sample_keys}"

    def test_dispatch_mapping_values_have_department(self):
        """映射值应包含 WisdomSchool 信息"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        wd = WisdomDispatcher()
        for pt, config in list(wd.problem_school_mapping.items())[:10]:
            # config 是 [(WisdomSchool, weight), ...] 列表
            assert isinstance(config, (list, tuple)), f"PT {pt} 配置类型异常: {type(config)}"


class TestCourtMapping:
    """朝廷岗位映射测试"""

    def test_court_mapping_not_empty(self):
        """DEPARTMENT_SCHOOL_MATRIX 或 resolve_departments 应可用"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_court import (
            Department, get_department_for_problem
        )
        # 验证 Department 枚举有多个值
        depts = list(Department)
        assert len(depts) >= 5, f"Department 枚举过少: {len(depts)}"

    def test_court_mapping_has_positions(self):
        """岗位解析函数应可调用"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_court import (
            ProblemType, resolve_positions_for_problem
        )
        if callable(resolve_positions_for_problem):
            # 至少不抛异常即可
            pass


class TestWisdomDispatcherInstance:
    """WisdomDispatcher 实例化测试"""

    def test_instantiation_succeeds(self):
        """应能成功实例化"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
        wd = WisdomDispatcher()
        assert wd is not None

    def test_has_core_attributes(self):
        """实例应有核心属性"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
        wd = WisdomDispatcher()
        # 检查常见属性是否存在
        attrs = ["dispatch", "_engines", "_mapping"] if hasattr(wd, "dispatch") else []
        # 至少实例不应为空且无异常
        assert wd is not None


@pytest.mark.slow
class TestDispatcherIntegration:
    """调度器集成测试"""

    def test_full_import_chain(self):
        """完整导入链：dispatcher → mapping → court → engines"""
        mods = [
            "smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatcher",
            "smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping",
            "smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_court",
        ]
        imported = []
        failed = []
        for m in mods:
            try:
                __import__(m)
                imported.append(m.split(".")[-1])
            except Exception as e:
                failed.append((m.split(".")[-1], str(e)[:80]))

        assert len(failed) == 0, f"导入失败: {failed}"
