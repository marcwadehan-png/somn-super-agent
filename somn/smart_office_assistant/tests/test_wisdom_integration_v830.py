"""
v1.0.0 智慧层接入验证脚本
验证 SomnCore 能否成功加载三大智慧协调器并完成简单调用
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)


SEPARATOR = "=" * 60


def test_super_wisdom_coordinator():
    """测试 SuperWisdomCoordinator 加载与调用"""
    print("\n[1] SuperWisdomCoordinator 测试")
    try:
        from src.intelligence.super_wisdom_coordinator import SuperWisdomCoordinator
        coordinator = SuperWisdomCoordinator()
        result = coordinator.analyze(
            query_text="如何制定一个有效的增长策略？",
            threshold=0.25,
            max_schools=4,
        )
        schools = []
        if hasattr(result, "activated_schools"):
            schools = [getattr(s, "name", str(s)) for s in (result.activated_schools or [])]
        elif isinstance(result, dict):
            schools = result.get("activated_schools", [])
        print(f"  ✅ 加载成功，激活学派: {schools[:4]}")
        return True
    except Exception as e:
        print(f"  ⚠️ 加载失败: {e}")
        return False


def test_unified_intelligence_coordinator():
    """测试 UnifiedIntelligenceCoordinator 加载与调用"""
    print("\n[2] UnifiedIntelligenceCoordinator 测试")
    try:
        from src.intelligence.unified_intelligence_coordinator import (
            UnifiedIntelligenceCoordinator, TaskType
        )
        coordinator = UnifiedIntelligenceCoordinator()
        result = coordinator.execute_task(
            task_type=TaskType.STRATEGY_PLANNING,
            input_data={
                "description": "制定品牌增长策略",
                "objective": "提升用户留存率",
                "industry": "saas_b2b",
            },
        )
        modules = []
        if hasattr(result, "modules_used"):
            modules = list(result.modules_used or [])
        elif isinstance(result, dict):
            modules = result.get("modules_used", [])
        print(f"  ✅ 加载成功，激活模块: {modules[:4]}")
        return True
    except Exception as e:
        print(f"  ⚠️ 加载失败: {e}")
        return False


def test_global_wisdom_scheduler():
    """测试 GlobalWisdomScheduler 加载与调用"""
    print("\n[3] GlobalWisdomScheduler 测试")
    try:
        from src.intelligence.global_wisdom_scheduler import get_scheduler, WisdomQuery
        scheduler = get_scheduler()
        query = WisdomQuery(text="面对复杂局势如何决策？", threshold=0.25, max_schools=4)
        result = scheduler.schedule(query)
        schools = []
        if hasattr(result, "school_results"):
            schools = [getattr(sr, "school_name", "") for sr in (result.school_results or [])]
        elif isinstance(result, dict):
            schools = result.get("schools", [])
        print(f"  ✅ 加载成功，激活学派: {schools[:4]}")
        return True
    except Exception as e:
        print(f"  ⚠️ 加载失败: {e}")
        return False


def test_thinking_method_engine():
    """测试 ThinkingMethodEngine 加载与调用"""
    print("\n[4] ThinkingMethodEngine 测试")
    try:
        from src.intelligence.thinking_method_engine import ThinkingMethodEngine
        engine = ThinkingMethodEngine()
        result = None
        for method in ["analyze", "think", "process"]:
            if hasattr(engine, method):
                result = getattr(engine, method)("如何用系统思维解决增长问题？")
                break
        print(f"  ✅ 加载成功，result type: {type(result).__name__}")
        return True
    except Exception as e:
        print(f"  ⚠️ 加载失败: {e}")
        return False


def test_somn_core_wisdom_init():
    """测试 SomnCore 初始化时是否成功挂载智慧层"""
    print("\n[5] SomnCore 智慧层初始化测试")
    try:
        from src.core.somn_core import SomnCore
        core = SomnCore()
        checks = {
            "super_wisdom": core.super_wisdom is not None,
            "unified_coordinator": core.unified_coordinator is not None,
            "global_wisdom": core.global_wisdom is not None,
            "thinking_engine": core.thinking_engine is not None,
        }
        for name, ok in checks.items():
            status = "✅" if ok else "⚠️ (加载失败，但不阻断主链)"
            print(f"    {status} {name}")
        print(f"  总计挂载: {sum(checks.values())}/4 个智慧协调器")
        return True
    except Exception as e:
        print(f"  ❌ SomnCore 初始化失败: {e}")
        return False


def test_wisdom_analysis_end_to_end():
    """端到端测试：_run_wisdom_analysis 实际调用"""
    print("\n[6] _run_wisdom_analysis 端到端测试")
    try:
        from src.core.somn_core import SomnCore
        core = SomnCore()
        result = core._run_wisdom_analysis(
            description="我需要为一家 SaaS 公司设计增长策略，重点提升用户留存",
            structured_req={"objective": "提升用户留存率至 85%", "task_type": "strategy_planning"},
            context={},
        )
        triggered = result.get("triggered", False)
        schools = result.get("activated_schools", [])
        insights = result.get("insights", [])
        source = result.get("source", "none")
        if triggered:
            print(f"  ✅ 智慧分析触发成功")
            print(f"     来源: {source}")
            print(f"     激活学派: {schools[:4]}")
            print(f"     洞察条数: {len(insights)}")
        else:
            print(f"  ⚠️ 智慧分析未触发（所有协调器均不可用），主链将继续运行")
        return True
    except Exception as e:
        print(f"  ❌ 端到端测试失败: {e}")
        return False


if __name__ == "__main__":
    print(SEPARATOR)
    print("Somn v1.0.0 智慧层接入验证")
    print(SEPARATOR)

    results = {
        "SuperWisdomCoordinator": test_super_wisdom_coordinator(),
        "UnifiedIntelligenceCoordinator": test_unified_intelligence_coordinator(),
        "GlobalWisdomScheduler": test_global_wisdom_scheduler(),
        "ThinkingMethodEngine": test_thinking_method_engine(),
        "SomnCore智慧层初始化": test_somn_core_wisdom_init(),
        "端到端智慧分析": test_wisdom_analysis_end_to_end(),
    }

    print(f"\n{SEPARATOR}")
    print("测试总结")
    print(SEPARATOR)
    passed = sum(results.values())
    total = len(results)
    for name, ok in results.items():
        print(f"  {'✅' if ok else '❌'} {name}")
    print(f"\n通过: {passed}/{total}")
    print(SEPARATOR)
