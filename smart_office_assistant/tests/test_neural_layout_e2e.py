# -*- coding: utf-8 -*-
"""Phase 1→5 全链路端到端集成验证测试（静默版）"""

import sys
import os
import traceback
import logging

# 抑制 Phase3 的刷屏日志
logging.basicConfig(level=logging.ERROR)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def test_1_init():
    """NetworkLayoutManager 初始化 + Phase 自动启动"""
    print("\n[1/7] NetworkLayoutManager 初始化...")
    from src.neural_layout import NetworkLayoutManager, PhaseSystemStatus
    mgr = NetworkLayoutManager()
    ok = mgr.initialize_global_layout()
    assert ok, "布局初始化失败"
    assert isinstance(mgr._phase_status, PhaseSystemStatus)
    topo = mgr.network.get_network_topology()
    n_count = topo.get("neuron_count", 0)
    assert n_count > 0, f"神经元数量为 0"
    ps = mgr.get_phase_status()
    print(f"  OK: neurons={n_count}, synapses={topo.get('synapse_count',0)}, "
          f"phase3_running={ps.get('phase3',{}).get('running',False)}, "
          f"clusters={ps.get('clusters',{}).get('count',0)}")
    return mgr


def test_2_layout_crud(mgr):
    """NeuralLayoutManager 布局管理"""
    print("\n[2/7] NeuralLayoutManager CRUD...")
    from src.neural_layout import NeuralLayoutManager
    from src.neural_layout.neural_layout_manager import LayoutConfig
    lm = NeuralLayoutManager()
    lm.initialize_global_layout()
    config = LayoutConfig(layout_id="test_layout", name="测试布局")
    layout = lm.create_layout(config)
    assert layout, "创建布局失败"
    layouts = lm.list_layouts()
    assert isinstance(layouts, list) and len(layouts) >= 1
    detail = lm.get_layout("somn_global_layout")
    assert detail
    summary = lm.get_manager_summary()
    assert summary
    result = lm.optimize_layout("somn_global_layout")
    print(f"  OK: layouts={len(layouts)}, id={layout.get('layout_id',layout.get('id','?'))}")


def test_3_bridge():
    """GlobalNeuralBridge 模块绑定"""
    print("\n[3/7] GlobalNeuralBridge 模块绑定...")
    from src.neural_layout.global_neural_bridge import (
        bind_real_module, unbind_real_module, get_bound_modules,
        get_global_neural_bridge,
    )
    class MockMod:
        def process(self, data): return {"mock": True}
    bind_real_module("test_mod", MockMod())
    bound = get_bound_modules()
    assert "test_mod" in bound
    unbind_real_module("test_mod")
    bound2 = get_bound_modules()
    assert "test_mod" not in bound2
    bridge = get_global_neural_bridge()
    status = bridge.get_bridge_status()
    print(f"  OK: bind/unbind 验证通过, status keys={list(status.keys())[:5]}")


def test_4_clusters(mgr):
    """ClusterOptimizer 集群优化"""
    print("\n[4/7] ClusterOptimizer...")
    results = mgr.optimize_clusters()
    print(f"  OK: {len(results)} 个集群优化完成")


def test_5_activate(mgr):
    """激活主链路"""
    print("\n[5/7] 激活主链路...")
    result = mgr.activate_main_chain({"query": "端到端测试", "context": {}})
    history = mgr.get_execution_history(limit=5)
    ps = mgr.get_phase_status()
    p4c = ps.get("phase4", {}).get("classifications", 0)
    p3e = ps.get("phase3", {}).get("executions", 0)
    print(f"  OK: history={len(history)}, p4_classifications={p4c}, p3_executions={p3e}")


def test_6_visualizer(mgr):
    """Visualizer 拓扑 + 热力图"""
    print("\n[6/7] Visualizer...")
    from src.neural_layout.visualizer import NetworkVisualizer
    viz = NetworkVisualizer(mgr.network)
    ps = mgr.get_phase_status()
    topo_html = viz.generate_realtime_topology_html(phase_status=ps)
    assert len(topo_html) > 1000 and "<svg" in topo_html
    heatmap_html = viz.generate_activation_heatmap_html()
    assert len(heatmap_html) > 500 and "热力图" in heatmap_html
    mermaid = viz.generate_mermaid_graph()
    assert "graph TD" in mermaid
    report = viz.generate_topology_report()
    metrics = report.get("metrics", {})
    print(f"  OK: topo={len(topo_html)}ch, heatmap={len(heatmap_html)}ch, "
          f"mermaid={len(mermaid.splitlines())}L, density={metrics.get('network_density',0)}")


def test_7_shutdown(mgr):
    """优雅关闭"""
    print("\n[7/7] 优雅关闭...")
    mgr.shutdown_phase_systems()
    print("  OK: 关闭完成")


def main():
    print("=" * 55)
    print("  Somn 神经网络布局 — Phase 1→5 端到端验证")
    print("=" * 55)
    passed = failed = 0
    mgr = None
    try:
        mgr = test_1_init(); passed += 1
    except Exception as e:
        print(f"  FAIL: {e}"); traceback.print_exc(); failed += 1

    for name, fn in [
        ("布局管理", lambda: test_2_layout_crud(mgr)),
        ("Bridge", test_3_bridge),
        ("集群优化", lambda: test_4_clusters(mgr)),
        ("激活主链路", lambda: test_5_activate(mgr)),
        ("Visualizer", lambda: test_6_visualizer(mgr)),
        ("关闭", lambda: test_7_shutdown(mgr)),
    ]:
        try:
            fn(); passed += 1
        except Exception as e:
            print(f"  FAIL [{name}]: {e}"); traceback.print_exc(); failed += 1

    print("\n" + "=" * 55)
    print(f"  结果: {passed}/{passed+failed} 通过")
    if failed == 0:
        print("  🎉 Phase 1→5 全链路验证成功！")
    print("=" * 55)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
