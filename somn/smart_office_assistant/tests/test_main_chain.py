"""
主线组件单元测试
测试 ParallelRouter, CrossWeaver, MainChainScheduler, MainChainIntegration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestParallelRouter:
    """ParallelRouter 并形路由器测试"""

    def test_init(self):
        """测试 ParallelRouter 初始化"""
        from src.main_chain.parallel_router import ParallelRouter
        router = ParallelRouter()
        assert router is not None
        print("✅ ParallelRouter 初始化")

    def test_get_router(self):
        """测试单例获取"""
        from src.main_chain.parallel_router import get_parallel_router, ParallelRouter
        router1 = get_parallel_router()
        router2 = get_parallel_router()
        assert router1 is router2
        print("✅ ParallelRouter 单例正确")

    def test_execute_parallel(self):
        """测试并行执行"""
        from src.main_chain.parallel_router import get_parallel_router

        router = get_parallel_router()
        context = {
            "task_id": "test_001",
            "task_type": "analysis",
            "complexity": 0.8,
            "multi_dimensional": True
        }

        result = router.execute_main_chain_parallel(context)
        assert result is not None
        assert "total_nodes" in result
        print(f"✅ 并行执行成功: {result.get('total_nodes', 0)} 个节点")


class TestCrossWeaver:
    """CrossWeaver 交叉织网器测试"""

    def test_init(self):
        """测试 CrossWeaver 初始化"""
        from src.main_chain.cross_weaver import CrossWeaver
        weaver = CrossWeaver()
        assert weaver is not None
        print("✅ CrossWeaver 初始化")

    def test_get_weaver(self):
        """测试单例获取"""
        from src.main_chain.cross_weaver import get_cross_weaver, CrossWeaver
        weaver1 = get_cross_weaver()
        weaver2 = get_cross_weaver()
        assert weaver1 is weaver2
        print("✅ CrossWeaver 单例正确")

    def test_cross_network(self):
        """测试交叉网络结构"""
        from src.main_chain.cross_weaver import get_cross_weaver
        weaver = get_cross_weaver()
        network = weaver.get_cross_network()
        assert "total_links" in network
        assert "modules" in network
        print(f"✅ 交叉网络: {network['total_links']} 条链接, {len(network['modules'])} 个模块")

    def test_signal_sending(self):
        """测试信号发送"""
        from src.main_chain.cross_weaver import get_cross_weaver
        weaver = get_cross_weaver()
        sig_id = weaver.send_signal("wisdom_dispatcher", "deep_reasoning", {"test": True})
        assert sig_id is not None
        print(f"✅ 信号发送成功: {sig_id}")

    def test_broadcast(self):
        """测试广播"""
        from src.main_chain.cross_weaver import get_cross_weaver
        weaver = get_cross_weaver()
        sig_ids = weaver.broadcast("learning_coordinator", {"source": "test"})
        assert len(sig_ids) > 0
        print(f"✅ 广播成功: {len(sig_ids)} 个信号")

    def test_propagate(self):
        """测试信号传播"""
        from src.main_chain.cross_weaver import get_cross_weaver
        weaver = get_cross_weaver()
        sig_ids = weaver.propagate("wisdom_dispatcher", {"test": True}, max_hops=2)
        assert len(sig_ids) > 0
        print(f"✅ 传播成功: {len(sig_ids)} 个信号")

    def test_execute_cross(self):
        """测试交叉执行"""
        from src.main_chain.cross_weaver import get_cross_weaver
        weaver = get_cross_weaver()
        result = weaver.execute_main_chain_cross(
            {"strategy": "test"},
            {"task_id": "test_001", "task_type": "growth"}
        )
        assert result is not None
        print(f"✅ 交叉执行: {result.get('total_signals', 0)} 个信号")


class TestMainChainScheduler:
    """MainChainScheduler 主线调度器测试"""

    def test_init(self):
        """测试 MainChainScheduler 初始化"""
        from src.main_chain.main_chain_scheduler import MainChainScheduler
        scheduler = MainChainScheduler()
        assert scheduler is not None
        print("✅ MainChainScheduler 初始化")

    def test_run_modes(self):
        """测试运行模式枚举"""
        from src.main_chain.main_chain_scheduler import RunMode
        assert RunMode.SERIAL is not None
        assert RunMode.PARALLEL is not None
        assert RunMode.CROSS is not None
        assert RunMode.AUTO is not None
        print("✅ 运行模式枚举正确")

    def test_determine_mode(self):
        """测试模式自动选择"""
        from src.main_chain.main_chain_scheduler import MainChainScheduler, RunMode

        scheduler = MainChainScheduler()

        # 高复杂度 → PARALLEL
        context = scheduler.ChainContext(
            context_id="test_001",
            user_input="多维度全面分析增长策略",
            task_type="strategy",
            wisdom_mode=RunMode.AUTO
        )
        mode = scheduler._determine_mode(context)
        assert mode == RunMode.PARALLEL

        # 反思关键词 → CROSS
        context2 = scheduler.ChainContext(
            context_id="test_002",
            user_input="反思改进优化反馈",
            task_type="growth",
            wisdom_mode=RunMode.AUTO
        )
        mode2 = scheduler._determine_mode(context2)
        assert mode2 == RunMode.CROSS

        print("✅ 模式自动选择正确")

    def test_get_status(self):
        """测试状态获取"""
        from src.main_chain.main_chain_scheduler import MainChainScheduler
        scheduler = MainChainScheduler()
        status = scheduler.get_status()
        assert "mode" in status
        assert "execution_count" in status
        print(f"✅ 状态获取: {status['mode']}")


class TestMainChainIntegration:
    """MainChainIntegration 主线集成器测试"""

    def test_init(self):
        """测试 MainChainIntegration 初始化"""
        from src.main_chain.main_chain_integration import get_main_chain_integration
        integration = get_main_chain_integration()
        assert integration is not None
        print("✅ MainChainIntegration 初始化")

    def test_status(self):
        """测试状态检查"""
        from src.main_chain.main_chain_integration import get_main_chain_integration
        integration = get_main_chain_integration()
        status = integration.get_status()
        assert status["parallel_router_available"] is True
        assert status["cross_weaver_available"] is True
        print(f"✅ 状态检查: ParallelRouter={status['parallel_router_available']}, CrossWeaver={status['cross_weaver_available']}")

    def test_determine_mode(self):
        """测试模式决策"""
        from src.main_chain.main_chain_integration import get_main_chain_integration, ChainRunMode

        integration = get_main_chain_integration()

        # 高复杂度
        req1 = {
            "task_id": "test_001",
            "routing_decision": {"complexity": 0.8},
            "raw_description": "分析增长策略",
            "task_type": "strategy"
        }
        mode1 = integration.determine_mode(req1)
        assert mode1 == ChainRunMode.PARALLEL

        # 反思关键词
        req2 = {
            "task_id": "test_002",
            "routing_decision": {"complexity": 0.5},
            "raw_description": "反思改进方案",
            "task_type": "growth"
        }
        mode2 = integration.determine_mode(req2)
        assert mode2 == ChainRunMode.CROSS

        print("✅ 模式决策正确")

    def test_build_chain_context(self):
        """测试上下文构建"""
        from src.main_chain.main_chain_integration import get_main_chain_integration

        integration = get_main_chain_integration()
        requirement = {
            "task_id": "test_001",
            "routing_decision": {"complexity": 0.7},
            "raw_description": "测试任务",
            "task_type": "analysis"
        }

        context = integration.build_chain_context(requirement)
        assert context is not None
        assert context.task_id == "test_001"
        assert context.wisdom_mode.value in ["parallel", "serial", "cross", "auto"]
        print(f"✅ 上下文构建: {context.task_id}, 模式={context.wisdom_mode.value}")

    def test_execute_serial(self):
        """测试串联执行"""
        from src.main_chain.main_chain_integration import get_main_chain_integration

        integration = get_main_chain_integration()
        requirement = {
            "task_id": "test_serial",
            "routing_decision": {"complexity": 0.3, "route": "orchestrator"},
            "raw_description": "快速查询",
            "task_type": "query"
        }

        result = integration.execute(requirement)
        assert result is not None
        assert result.mode.value == "serial"
        print(f"✅ 串联执行: {result.mode.value}")

    def test_execute_parallel(self):
        """测试并形执行"""
        from src.main_chain.main_chain_integration import get_main_chain_integration

        integration = get_main_chain_integration()
        requirement = {
            "task_id": "test_parallel",
            "routing_decision": {"complexity": 0.8},
            "raw_description": "多维度全面分析增长策略",
            "task_type": "strategy"
        }

        result = integration.execute(requirement)
        assert result is not None
        assert result.mode.value == "parallel"
        print(f"✅ 并形执行: {result.mode.value}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("主线组件单元测试")
    print("=" * 60)

    test_classes = [
        TestParallelRouter,
        TestCrossWeaver,
        TestMainChainScheduler,
        TestMainChainIntegration
    ]

    passed = 0
    failed = 0

    for test_class in test_classes:
        print(f"\n【{test_class.__name__}】")
        instance = test_class()
        methods = [m for m in dir(instance) if m.startswith("test_")]

        for method_name in methods:
            try:
                method = getattr(instance, method_name)
                method()
                passed += 1
            except Exception as e:
                print(f"❌ {method_name}: {e}")
                failed += 1

    print("\n" + "=" * 60)
    print(f"测试结果: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
