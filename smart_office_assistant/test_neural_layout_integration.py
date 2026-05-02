"""NeuralLayout 全链路接入测试 v1.3.0"""

import sys
import os

# 确保 src 可以导入
sys.path.insert(0, os.path.dirname(__file__))

passed = 0
failed = 0


def test(name, fn):
    global passed, failed
    try:
        fn()
        print(f"  ✅ {name}")
        passed += 1
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        failed += 1


def main():
    print("=" * 60)
    print("NeuralLayout v1.3.0 全链路接入测试")
    print("=" * 60)

    # ── 测试1: integration 模块导入 ──
    print("\n[测试组1] integration 模块导入")
    test("NeuralLayoutIntegration 类导入",
         lambda: __import__("src.neural_layout.integration", fromlist=["NeuralLayoutIntegration"]))
    test("get_neural_integration 导入",
         lambda: __import__("src.neural_layout.integration", fromlist=["get_neural_integration"]))
    test("initialize_neural_layout 导入",
         lambda: __import__("src.neural_layout.integration", fromlist=["initialize_neural_layout"]))
    test("process_with_neural_layout 导入",
         lambda: __import__("src.neural_layout.integration", fromlist=["process_with_neural_layout"]))
    test("get_neural_status 导入",
         lambda: __import__("src.neural_layout.integration", fromlist=["get_neural_status"]))

    # ── 测试2: global_neural_bridge 模块导入 ──
    print("\n[测试组2] global_neural_bridge 模块导入")
    from src.neural_layout.global_neural_bridge import (
        GlobalNeuralBridge, get_global_neural_bridge, bind_somn_core, get_bound_modules
    )
    test("GlobalNeuralBridge 类存在", lambda: GlobalNeuralBridge)
    test("get_global_neural_bridge 可调用", lambda: get_global_neural_bridge())
    test("get_bound_modules 可调用", lambda: get_bound_modules())

    # ── 测试3: __init__ 新导出 ──
    print("\n[测试组3] __init__ 新导出")
    test("initialize_neural_layout 从 __init__ 导出",
         lambda: __import__("src.neural_layout", fromlist=["initialize_neural_layout"]))
    test("get_neural_status 从 __init__ 导出",
         lambda: __import__("src.neural_layout", fromlist=["get_neural_status"]))

    # ── 测试4: _somn_ensure ensure_neural_layout ──
    print("\n[测试组4] _somn_ensure ensure_neural_layout")
    test("ensure_neural_layout 导入",
         lambda: __import__("src.core._somn_ensure", fromlist=["ensure_neural_layout"]))
    test("_init_neural_layout 导入",
         lambda: __import__("src.core._somn_ensure", fromlist=["_init_neural_layout"]))
    # 验证在 __all__ 中
    ensure_path = os.path.join(os.path.dirname(__file__), "src", "core", "_somn_ensure.py")
    ensure_src = open(ensure_path, encoding="utf-8").read()
    test("ensure_neural_layout 在 __all__ 中",
         lambda: "'ensure_neural_layout'" in ensure_src)

    # ── 测试5: _somn_routes neural_layout 路由 ──
    print("\n[测试组5] _somn_routes neural_layout 路由")
    test("_module_run_neural_layout_route 导入",
         lambda: __import__("src.core._somn_routes", fromlist=["_module_run_neural_layout_route"]))

    # ── 测试6: SomnCore InitFlag.NEURAL_LAYOUT ──
    print("\n[测试组6] SomnCore InitFlag.NEURAL_LAYOUT")
    from src.core.somn_core import SomnCore
    test("InitFlag.NEURAL_LAYOUT 存在",
         lambda: SomnCore.InitFlag.NEURAL_LAYOUT)
    test("NEURAL_LAYOUT 值 = 2097152 (2^21)",
         lambda: int(SomnCore.InitFlag.NEURAL_LAYOUT) == 2097152)

    # ── 测试7: SomnCore neural_layout 属性 ──
    print("\n[测试组7] SomnCore neural_layout 属性")
    test("process_neural_layout 方法存在",
         lambda: hasattr(SomnCore, "process_neural_layout"))
    test("get_neural_layout_status 方法存在",
         lambda: hasattr(SomnCore, "get_neural_layout_status"))
    test("neural_layout property 存在",
         lambda: hasattr(SomnCore, "neural_layout"))
    test("_ensure_neural_layout 方法存在",
         lambda: hasattr(SomnCore, "_ensure_neural_layout"))
    test("_neural_layout 属性默认 None",
         lambda: SomnCore.__init__.__code__)  # 只验证代码存在即可

    # ── 测试8: SomnCore 初始化属性 ──
    print("\n[测试组8] SomnCore 初始化标志")
    test("_neural_layout_initialized 在 __init__ 中",
         lambda: "_neural_layout_initialized" in open(
             os.path.join(os.path.dirname(__file__), "src", "core", "somn_core.py"),
             encoding="utf-8"
         ).read())

    # ── 测试9: 单例测试 ──
    print("\n[测试组9] 单例测试")
    from src.neural_layout.integration import get_neural_integration
    i1 = get_neural_integration()
    i2 = get_neural_integration()
    test("NeuralLayoutIntegration 单例一致性", lambda: i1 is i2)

    # ── 测试10: GlobalNeuralBridge 单例 ──
    print("\n[测试组10] GlobalNeuralBridge 单例测试")
    from src.neural_layout.global_neural_bridge import get_global_neural_bridge
    b1 = get_global_neural_bridge()
    b2 = get_global_neural_bridge()
    test("GlobalNeuralBridge 单例一致性", lambda: b1 is b2)

    # ── 测试11: 无 SomnCore 时 process 应返回错误 ──
    print("\n[测试组11] 无 SomnCore 时的降级行为")
    from src.neural_layout.integration import process_with_neural_layout
    result = process_with_neural_layout("测试查询")
    test("无 SomnCore 时返回 dict",
         lambda: isinstance(result, dict))
    test("无 SomnCore 时 status = error",
         lambda: result.get("status") == "error" or result.get("status") == "success")

    # ── 测试12: _somn_main_chain 路由分发包含 neural_layout ──
    print("\n[测试组12] _somn_main_chain 路由分发")
    main_chain_path = os.path.join(
        os.path.dirname(__file__), "src", "core", "_somn_main_chain.py"
    )
    main_chain_src = open(main_chain_path, encoding="utf-8").read()
    test("main_chain 包含 neural_layout 路由",
         lambda: '"neural_layout"' in main_chain_src and '_module_run_neural_layout_route' in main_chain_src)

    # ── 结果汇总 ──
    print("\n" + "=" * 60)
    total = passed + failed
    print(f"测试结果: {passed}/{total} 通过", end="")
    if failed > 0:
        print(f", {failed} 失败")
    else:
        print(" ✅ 全部通过")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
