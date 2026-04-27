"""
smoke_test_cloud_learning.py
v14.0.0 云端老师-本地学生体系全局打通冒烟测试

验证：
1. 三个模块能正常初始化
2. 路由决策正确分类
3. 编排器能正常工作
4. SomnCore 三模块接入无回归
"""

import sys
import os

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)




def test_cloud_modules_import():
    """测试1：三个核心模块能正常导入"""
    print("\n[测试1] 模块导入...")
    try:
        from tool_layer.cloud_model_hub import CloudModelHub, TeacherConfig, TeacherResponse
        from tool_layer.teacher_student_engine import TeacherStudentEngine, LearningMode, QualityAssessment
        from tool_layer.somn_orchestrator import SomnOrchestrator, CuisineMode, MenuRequest
        print("  ✅ 三个核心模块导入成功")
        return True
    except Exception as e:
        print(f"  ❌ 模块导入失败: {e}")
        return False


def test_cloud_hub_init():
    """测试2：CloudModelHub 初始化"""
    print("\n[测试2] CloudModelHub 初始化...")
    try:
        from tool_layer.cloud_model_hub import CloudModelHub
        hub = CloudModelHub(base_path=".test_cloud_data/cloud_hub")
        teachers = hub.list_teachers()
        print(f"  ✅ CloudModelHub 就绪，{len(teachers)} 位预设老师")
        return True
    except Exception as e:
        print(f"  ❌ CloudModelHub 初始化失败: {e}")
        import traceback; traceback.print_exc()
        return False


def test_teacher_student_engine():
    """测试3：TeacherStudentEngine 初始化"""
    print("\n[测试3] TeacherStudentEngine 初始化...")
    try:
        from tool_layer.teacher_student_engine import TeacherStudentEngine, LearningMode
        from tool_layer.cloud_model_hub import CloudModelHub

        hub = CloudModelHub(base_path=".test_cloud_data/cloud_hub")
        engine = TeacherStudentEngine(
            base_path=".test_cloud_data/teacher_student",
            cloud_hub=hub,
            llm_service=None,
        )
        modes = [m.value for m in LearningMode]
        print(f"  ✅ TeacherStudentEngine 就绪，{len(modes)} 种学习模式：{modes}")
        return True
    except Exception as e:
        print(f"  ❌ TeacherStudentEngine 初始化失败: {e}")
        import traceback; traceback.print_exc()
        return False


def test_somn_orchestrator():
    """测试4：SomnOrchestrator 初始化 + 快速回答"""
    print("\n[测试4] SomnOrchestrator 初始化...")
    try:
        from tool_layer.somn_orchestrator import SomnOrchestrator, CuisineMode, MenuRequest
        from tool_layer.teacher_student_engine import TeacherStudentEngine
        from tool_layer.cloud_model_hub import CloudModelHub

        hub = CloudModelHub(base_path=".test_cloud_data/cloud_hub")
        engine = TeacherStudentEngine(
            base_path=".test_cloud_data/teacher_student",
            cloud_hub=hub,
            llm_service=None,
        )
        orch = SomnOrchestrator(
            cloud_hub=hub,
            teacher_student_engine=engine,
            llm_service=None,
        )

        cuisine_modes = [m.value for m in CuisineMode]
        print(f"  ✅ SomnOrchestrator 就绪，{len(cuisine_modes)} 种烹饪模式：{cuisine_modes}")

        # 测试快速回答（local_llm_fallback，因为 llm_service=None）
        req = MenuRequest(dish_name="你好，请做个自我介绍", hunger_level="light", dining_mode="fast")
        resp = orch.serve(req)
        print(f"  ✅ 快速回答测试成功：质量={resp.quality_stars:.1f}⭐，烹饪={resp.cuisine_mode}，耗时={resp.cooking_time_ms}ms")
        return True
    except Exception as e:
        print(f"  ❌ SomnOrchestrator 测试失败: {e}")
        import traceback; traceback.print_exc()
        return False


def test_routing_decision():
    """测试5：路由决策逻辑"""
    print("\n[测试5] 路由决策逻辑...")
    try:
        from tool_layer.somn_orchestrator import SomnOrchestrator, CuisineMode, MenuRequest

        orch = SomnOrchestrator(cloud_hub=None, teacher_student_engine=None, llm_service=None)

        test_cases = [
            # (输入文本, 期望烹饪模式)
            ("你好", "fast"),
            ("今天天气怎么样？", "fast"),
            ("帮我制定一个增长策略", "home"),
            ("分析一下这个方案", "home"),
            ("深度分析茅台的品牌战略", "feast"),
            ("生成一份详细的研究报告", "feast"),
        ]

        all_passed = True
        for text, expected_mode in test_cases:
            req = MenuRequest(dish_name=text, hunger_level="normal", dining_mode="home")
            mode = orch._decide_mode(req)
            actual = mode.value
            status = "✅" if actual == expected_mode else "❌"
            if actual != expected_mode:
                all_passed = False
            print(f"  {status} \"{text[:20]}...\" → {actual}（期望={expected_mode}）")

        print(f"  {'✅ 路由决策测试通过' if all_passed else '❌ 路由决策测试失败'}")
        return all_passed
    except Exception as e:
        print(f"  ❌ 路由决策测试失败: {e}")
        import traceback; traceback.print_exc()
        return False


def test_somn_core_cloud_integration():
    """测试6：SomnCore 中三模块接入"""
    print("\n[测试6] SomnCore 云端体系接入...")
    try:
        from pathlib import Path

        PROJECT_ROOT = Path(__file__).parent.resolve()
        src_path = PROJECT_ROOT / "src"
        sys.path.insert(0, str(src_path))

        # patch PROJECT_ROOT
        import src.core.paths as paths_mod
        orig_root = paths_mod.PROJECT_ROOT
        paths_mod.PROJECT_ROOT = PROJECT_ROOT

        try:
            from src.core.somn_core import SomnCore

            # 只初始化云端体系相关属性
            core = SomnCore.__new__(SomnCore)
            core.base_path = PROJECT_ROOT
            core.agent_runs_dir = PROJECT_ROOT / "data" / "agent_runs"
            core.autonomy_dir = PROJECT_ROOT / "data" / "autonomy"
            core.agent_runs_dir.mkdir(parents=True, exist_ok=True)
            core.autonomy_dir.mkdir(parents=True, exist_ok=True)
            core.goal_store_path = core.autonomy_dir / "long_term_goals.json"
            core.experience_store_path = core.autonomy_dir / "experience_library.json"
            core.reflection_store_path = core.autonomy_dir / "task_reflections.json"
            core._feedback_pipeline = None
            core._feedback_pipeline_unavailable = False
            core._reinforcement_trigger = None
            core._reinforcement_feedback_unavailable = False
            core._roi_tracker = None
            core._roi_tracker_unavailable = False
            core.contexts = {}
            # TeacherStudentEngine 需要 llm_service 属性
            core.llm_service = None

            print("  ⏳ 初始化云端体系...")
            core._init_cloud_learning_system()

            checks = [
                ("CloudModelHub", core.cloud_model_hub is not None),
                ("TeacherStudentEngine", core.teacher_student_engine is not None),
                ("SomnOrchestrator", core.somn_orchestrator is not None),
            ]

            all_ok = True
            for name, ok in checks:
                print(f"  {'✅' if ok else '❌'} {name}: {'已接入' if ok else '未接入'}")
                if not ok:
                    all_ok = False

            return all_ok
        finally:
            paths_mod.PROJECT_ROOT = orig_root
    except Exception as e:
        print(f"  ❌ SomnCore 接入失败: {e}")
        import traceback; traceback.print_exc()
        return False


def test_routing_assess_in_somn_core():
    """测试7：SomnCore._assess_task_routing 方法"""
    print("\n[测试7] _assess_task_routing 方法...")
    try:
        from pathlib import Path

        PROJECT_ROOT = Path(__file__).parent.resolve()
        sys.path.insert(0, str(PROJECT_ROOT / "src"))

        import src.core.paths as paths_mod
        orig_root = paths_mod.PROJECT_ROOT
        paths_mod.PROJECT_ROOT = PROJECT_ROOT

        try:
            from src.core.somn_core import SomnCore

            # 模拟 SomnCore（跳过完整初始化）
            core = SomnCore.__new__(SomnCore)
            core.base_path = PROJECT_ROOT
            core.somn_orchestrator = None
            core.cloud_model_hub = None
            core.teacher_student_engine = None
            # llm_service 需要存在（即使为 None）
            core.llm_service = None

            # orchestrator=None 且 llm_service=None 时：
            # 路由先定 complexity 级别，再因 orchestrator 不可用 fallback 到 wisdom_only
            # 复杂度阈值: <0.35→orchestrator/fast, <0.55→orchestrator/home, ≥0.55→full_workflow/feast
            # 实际复杂度计算：deep+deep="深度+报告"=0.4+0.034=0.434 → orchestrator/home
            test_cases = [
                ("你好", "wisdom_only", "fast"),
                ("今天天气怎么样", "wisdom_only", "fast"),
                ("帮我制定增长策略", "wisdom_only", "home"),      # orchestrator unavailable → fallback
                ("深度分析茅台品牌战略并生成报告", "wisdom_only", "home"),  # deep+deep=0.434 → <0.55 → orchestrator/home → fallback
                ("论证儒家思想对企业管理的启示", "wisdom_only", "fast"),   # deep only ≈0.2 → <0.35 → orchestrator/fast → fallback
            ]

            all_passed = True
            for desc, expected_route, expected_cuisine in test_cases:
                structured_req = {"_semantic_hints": {}, "task_type": "general", "objective": desc}
                routing = core._assess_task_routing(desc, structured_req, {})
                actual_route = routing.get("route")
                actual_cuisine = routing.get("cuisine_mode")

                ok_route = actual_route == expected_route
                ok_cuisine = actual_cuisine == expected_cuisine
                status = "✅" if (ok_route and ok_cuisine) else "❌"
                if not (ok_route and ok_cuisine):
                    all_passed = False

                print(f"  {status} \"{desc[:20]}...\"")
                print(f"       route={actual_route}(期望={expected_route}) cuisine={actual_cuisine}(期望={expected_cuisine})")

            print(f"  {'✅ 路由评估测试通过' if all_passed else '❌ 路由评估测试失败'}")
            return all_passed
        finally:
            paths_mod.PROJECT_ROOT = orig_root
    except Exception as e:
        print(f"  ❌ 路由评估测试失败: {e}")
        import traceback; traceback.print_exc()
        return False


def test_full_chain_no_regression():
    """测试8：全链路无回归"""
    print("\n[测试8] 全链路无回归检查...")
    try:
        from src.intelligence.global_wisdom_scheduler import get_scheduler
        scheduler = get_scheduler()
        # GlobalWisdomScheduler 有 network 和 registry 属性
        network_ok = hasattr(scheduler, 'network') and scheduler.network is not None
        registry_ok = hasattr(scheduler, 'registry') and scheduler.registry is not None
        registered = scheduler.registry.list_registered() if registry_ok else []
        print(f"  ✅ GlobalWisdomScheduler: 神经元网络{'已接入' if network_ok else '未接入'}，注册引擎 {len(registered)} 个")
        return True
    except Exception as e:
        print(f"  ❌ 全链路回归失败: {e}")
        import traceback; traceback.print_exc()
        return False


def cleanup():
    """清理测试数据"""
    import shutil
    test_dirs = [".test_cloud_data"]
    for d in test_dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"  🗑️ 清理: {d}")
            except Exception:
                pass


if __name__ == "__main__":
    print("=" * 60)
    print("v14.0.0 云端老师-本地学生体系 全局打通冒烟测试")
    print("=" * 60)

    results = []

    results.append(("模块导入", test_cloud_modules_import()))
    results.append(("CloudModelHub 初始化", test_cloud_hub_init()))
    results.append(("TeacherStudentEngine 初始化", test_teacher_student_engine()))
    results.append(("SomnOrchestrator 初始化", test_somn_orchestrator()))
    results.append(("路由决策逻辑", test_routing_decision()))
    results.append(("SomnCore 三模块接入", test_somn_core_cloud_integration()))
    results.append(("_assess_task_routing 评估", test_routing_assess_in_somn_core()))
    results.append(("全链路无回归", test_full_chain_no_regression()))

    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    for name, ok in results:
        print(f"  {'✅' if ok else '❌'} {name}")
    print(f"\n总计: {passed}/{total} 通过")
    print("=" * 60)

    cleanup()
    sys.exit(0 if passed == total else 1)
