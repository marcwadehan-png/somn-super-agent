# -*- coding: utf-8 -*-
"""
neural_layout 核心模块独立单元测试
覆盖: ClusterOptimizer, NetworkLayoutManager, NeuralLayoutManager, neuron_node, synapse_connection
"""

import sys
import os
import logging

logging.basicConfig(level=logging.ERROR)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 设置包路径
pkg_root = os.path.join(PROJECT_ROOT, "smart_office_assistant")
if pkg_root not in sys.path:
    sys.path.insert(0, pkg_root)


# ═══════════════════════════════════════════════════════════
# ClusterOptimizer 单元测试
# ═══════════════════════════════════════════════════════════

class TestClusterOptimizer:
    """集群优化器单元测试"""

    def test_init(self):
        from src.neural_layout.cluster_optimizer import ClusterOptimizer
        opt = ClusterOptimizer()
        assert opt is not None
        assert len(opt.list_clusters()) == 0

    def test_register_cluster(self):
        from src.neural_layout.cluster_optimizer import ClusterOptimizer, ClusterConfig
        opt = ClusterOptimizer()
        cfg = ClusterConfig(cluster_id="test_c1", nodes=["n1", "n2", "n3"])
        ok = opt.register_cluster(cfg)
        assert ok
        assert "test_c1" in opt.list_clusters()

    def test_optimize_without_network(self):
        """无网络引用时优化应返回结果（使用默认值）"""
        from src.neural_layout.cluster_optimizer import ClusterOptimizer, ClusterConfig
        opt = ClusterOptimizer()
        opt.register_cluster(ClusterConfig(cluster_id="c1", nodes=["n1", "n2"]))
        result = opt.optimize("c1")
        assert result is not None
        assert result.cluster_id == "c1"
        assert isinstance(result.improvement, float)
        assert isinstance(result.details, dict)

    def test_optimize_empty_cluster(self):
        """空节点集群应返回 improvement=0"""
        from src.neural_layout.cluster_optimizer import ClusterOptimizer, ClusterConfig
        opt = ClusterOptimizer()
        opt.register_cluster(ClusterConfig(cluster_id="empty", nodes=[]))
        result = opt.optimize("empty")
        assert result is not None
        assert result.improvement == 0.0

    def test_optimize_nonexistent_cluster(self):
        """不存在的集群应返回 None"""
        from src.neural_layout.cluster_optimizer import ClusterOptimizer
        opt = ClusterOptimizer()
        assert opt.optimize("nonexistent") is None

    def test_optimize_all(self):
        """批量优化所有集群"""
        from src.neural_layout.cluster_optimizer import ClusterOptimizer, ClusterConfig
        opt = ClusterOptimizer()
        opt.register_cluster(ClusterConfig(cluster_id="c1", nodes=["a", "b"]))
        opt.register_cluster(ClusterConfig(cluster_id="c2", nodes=["x", "y", "z"]))
        results = opt.optimize_all()
        assert len(results) == 2

    def test_get_cluster(self):
        """获取集群信息"""
        from src.neural_layout.cluster_optimizer import ClusterOptimizer, ClusterConfig
        opt = ClusterOptimizer()
        opt.register_cluster(ClusterConfig(cluster_id="c1", nodes=["a", "b"]))
        info = opt.get_cluster("c1")
        assert info is not None
        assert "c1" in str(info)

    def test_get_cluster_nonexistent(self):
        from src.neural_layout.cluster_optimizer import ClusterOptimizer
        opt = ClusterOptimizer()
        assert opt.get_cluster("nope") is None

    def test_get_optimization_summary_empty(self):
        """无优化历史时摘要应返回 0"""
        from src.neural_layout.cluster_optimizer import ClusterOptimizer
        opt = ClusterOptimizer()
        summary = opt.get_optimization_summary()
        assert summary["total_optimizations"] == 0
        assert summary["avg_improvement"] == 0.0


# ═══════════════════════════════════════════════════════════
# NeuronNode 单元测试
# ═══════════════════════════════════════════════════════════

class TestNeuronNode:
    """神经元节点单元测试"""

    def test_base_neuron_creation(self):
        from src.neural_layout.neuron_node import (
            NeuronNode, NeuronType, NeuronState
        )
        # NeuronNode 是抽象类，使用子类 InputNeuron
        from src.neural_layout.neuron_node import InputNeuron
        n = InputNeuron("test_input", "测试输入")
        assert n.neuron_id == "test_input"
        assert n.neuron_type == NeuronType.INPUT
        assert n.state == NeuronState.DORMANT

    def test_subclass_types(self):
        from src.neural_layout.neuron_node import (
            InputNeuron, OutputNeuron, WisdomNeuron, MemoryNeuron, NeuronType
        )
        i = InputNeuron("i", "input")
        assert i.neuron_type == NeuronType.INPUT
        o = OutputNeuron("o", "output")
        assert o.neuron_type == NeuronType.OUTPUT
        m = MemoryNeuron("m", "memory")
        assert m.neuron_type == NeuronType.MEMORY
        w = WisdomNeuron("w", "CONFUCIAN", "wisdom")
        assert w.neuron_type == NeuronType.WISDOM
        assert w.school_id == "CONFUCIAN"

    def test_add_synapses(self):
        from src.neural_layout.neuron_node import InputNeuron
        from src.neural_layout.synapse_connection import SynapseConnection
        n = InputNeuron("n1", "test")
        s = SynapseConnection("n1", "n2")
        n.add_outgoing_synapse(s)
        assert s.synapse_id in n.outgoing_synapses
        n.add_incoming_synapse(s)
        assert s.synapse_id in n.incoming_synapses

    def test_reset(self):
        from src.neural_layout.neuron_node import InputNeuron, NeuronState
        n = InputNeuron("n1")
        n.activation_level = 0.8
        n.reset()
        assert n.activation_level == 0.0
        assert n.state == NeuronState.DORMANT

    def test_get_stats(self):
        from src.neural_layout.neuron_node import InputNeuron
        n = InputNeuron("n1")
        stats = n.get_stats()
        assert "neuron_id" in stats
        assert "activation_count" in stats


# ═══════════════════════════════════════════════════════════
# SynapseConnection 单元测试
# ═══════════════════════════════════════════════════════════

class TestSynapseConnection:
    """突触连接单元测试"""

    def test_creation(self):
        from src.neural_layout.synapse_connection import SynapseConnection
        s = SynapseConnection("src", "tgt", weight=0.8)
        assert s.source_id == "src"
        assert s.target_id == "tgt"
        assert s.weight == 0.8
        assert s.synapse_id  # 自动生成

    def test_strengthen_weaken(self):
        from src.neural_layout.synapse_connection import SynapseConnection
        s = SynapseConnection("a", "b", weight=0.5)
        s.strengthen(0.2)
        assert s.weight > 0.5
        old_w = s.weight
        s.weaken(0.1)
        assert s.weight < old_w

    def test_weight_bounds(self):
        """权重不应超过上下限"""
        from src.neural_layout.synapse_connection import SynapseConnection
        s = SynapseConnection("a", "b", weight=1.99)
        s.strengthen(1.0)
        assert s.weight <= 2.0
        s.weaken(10.0)
        assert s.weight >= 0.0

    def test_disable_plasticity(self):
        """关闭可塑性后权重不应变化"""
        from src.neural_layout.synapse_connection import SynapseConnection
        s = SynapseConnection("a", "b", weight=0.5)
        s.plasticity_enabled = False
        s.strengthen(1.0)
        assert s.weight == 0.5

    def test_get_stats(self):
        from src.neural_layout.synapse_connection import SynapseConnection
        s = SynapseConnection("a", "b")
        stats = s.get_stats()
        assert "synapse_id" in stats
        assert "weight" in stats


# ═══════════════════════════════════════════════════════════
# NetworkLayoutManager 单元测试
# ═══════════════════════════════════════════════════════════

class TestNetworkLayoutManager:
    """网络布局管理器单元测试"""

    def test_init(self):
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        mgr = NetworkLayoutManager()
        assert mgr is not None
        assert not mgr.initialized

    def test_initialize_global_layout(self):
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        mgr = NetworkLayoutManager()
        ok = mgr.initialize_global_layout()
        assert ok
        assert mgr.initialized
        # 验证网络拓扑
        topo = mgr.network.get_network_topology()
        assert topo["neuron_count"] > 0
        assert topo["synapse_count"] > 0

    def test_main_chain_mapping(self):
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        mgr = NetworkLayoutManager()
        mgr.initialize_global_layout()
        assert len(mgr.main_chain_mapping) > 0
        # mapping key 是模块类名（如 "AgentCore"），value 是神经元 ID
        assert "AgentCore" in mgr.main_chain_mapping

    def test_wisdom_mapping(self):
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        mgr = NetworkLayoutManager()
        mgr.initialize_global_layout()
        assert len(mgr.wisdom_mapping) > 0
        assert "CONFUCIAN" in mgr.wisdom_mapping

    def test_get_layout_status(self):
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        mgr = NetworkLayoutManager()
        mgr.initialize_global_layout()
        status = mgr.get_layout_status()
        assert isinstance(status, dict)
        assert "main_chain_nodes" in status

    def test_get_phase_status(self):
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        mgr = NetworkLayoutManager()
        mgr.initialize_global_layout()
        ps = mgr.get_phase_status()
        assert isinstance(ps, dict)
        assert "clusters" in ps

    def test_optimize_clusters(self):
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        mgr = NetworkLayoutManager()
        mgr.initialize_global_layout()
        results = mgr.optimize_clusters()
        assert isinstance(results, list)
        assert len(results) > 0
        for r in results:
            assert "cluster_id" in r

    def test_singleton(self):
        """验证单例行为"""
        from src.neural_layout.network_layout_manager import NetworkLayoutManager
        m1 = NetworkLayoutManager("test_singleton")
        m2 = NetworkLayoutManager("test_singleton")
        assert m1 is not m2  # NetworkLayoutManager 不是单例


# ═══════════════════════════════════════════════════════════
# NeuralLayoutManager (多布局管理) 单元测试
# ═══════════════════════════════════════════════════════════

class TestNeuralLayoutManager:
    """多布局管理器单元测试"""

    def test_singleton(self):
        from src.neural_layout.neural_layout_manager import NeuralLayoutManager
        m1 = NeuralLayoutManager()
        m2 = NeuralLayoutManager()
        assert m1 is m2  # 确认单例

    def test_list_layouts(self):
        from src.neural_layout.neural_layout_manager import NeuralLayoutManager
        lm = NeuralLayoutManager()
        lm.initialize_global_layout()
        layouts = lm.list_layouts()
        assert len(layouts) >= 1
        ids = [l["layout_id"] for l in layouts]
        assert "somn_global_layout" in ids

    def test_create_layout(self):
        from src.neural_layout.neural_layout_manager import NeuralLayoutManager
        from src.neural_layout.neural_layout_manager import LayoutConfig
        lm = NeuralLayoutManager()
        lm.initialize_global_layout()
        cfg = LayoutConfig(name="测试布局", description="单元测试")
        result = lm.create_layout(cfg)
        assert result["status"] == "created"
        assert len(lm.list_layouts()) >= 2

    def test_delete_layout(self):
        from src.neural_layout.neural_layout_manager import NeuralLayoutManager
        from src.neural_layout.neural_layout_manager import LayoutConfig
        lm = NeuralLayoutManager()
        lm.initialize_global_layout()
        cfg = LayoutConfig(name="可删除布局")
        lm.create_layout(cfg)
        assert lm.delete_layout(cfg.layout_id)
        assert len(lm.list_layouts()) >= 1  # 默认布局还在

    def test_cannot_delete_active_layout(self):
        from src.neural_layout.neural_layout_manager import NeuralLayoutManager
        lm = NeuralLayoutManager()
        lm.initialize_global_layout()
        assert not lm.delete_layout("somn_global_layout")

    def test_get_manager_summary(self):
        from src.neural_layout.neural_layout_manager import NeuralLayoutManager
        lm = NeuralLayoutManager()
        lm.initialize_global_layout()
        summary = lm.get_manager_summary()
        assert summary["version"] == "2.0"
        assert summary["initialized"]
        assert summary["active_layout"] == "somn_global_layout"


# ═══════════════════════════════════════════════════════════
# 运行所有测试
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import traceback

    test_classes = [
        TestClusterOptimizer,
        TestNeuronNode,
        TestSynapseConnection,
        TestNetworkLayoutManager,
        TestNeuralLayoutManager,
    ]

    total = 0
    passed = 0
    failed = 0

    for cls in test_classes:
        instance = cls()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        for method_name in methods:
            total += 1
            try:
                getattr(instance, method_name)()
                passed += 1
                print(f"  ✓ {cls.__name__}.{method_name}")
            except Exception as e:
                failed += 1
                print(f"  ✗ {cls.__name__}.{method_name}: {e}")
                traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"单元测试结果: {passed}/{total} 通过, {failed} 失败")
    if failed > 0:
        sys.exit(1)
