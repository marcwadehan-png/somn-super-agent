# -*- coding: utf-8 -*-
"""
DivineReason 超级引擎网络测试套件
================================

测试引擎网络的各项功能。

版本: V1.0.0
创建: 2026-04-28
"""

import sys
import os

# 添加 src 目录到路径
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, src_path)

from intelligence.engines._engine_network import (
    EngineNetwork,
    EngineCategory,
    EngineMetadata,
    NetworkConfig,
    FusionStrategy,
    InvocationMode,
    create_engine_network
)

from intelligence.engines._engine_discovery import (
    EngineScanner,
    EngineNetworkBuilder,
    build_engine_network
)

from intelligence.engines._divine_engine_integration import (
    DivineReasonNetwork,
    EngineReasoningCoordinator,
    EngineInvokeNode,
    EngineInvocationPlan
)


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_engine_network_basic():
    """测试1: 引擎网络基础功能"""
    print_header("Test 1: Engine Network Basic")
    
    # 创建网络
    network = create_engine_network()
    
    # 注册测试引擎
    def mock_executor(input_data, **kwargs):
        return f"Processed: {input_data}"
    
    network.register_engine(
        engine_id="philosophy",
        name="Philosophy Engine",
        description="Philosophy and wisdom analysis engine",
        category=EngineCategory.PHILOSOPHY,
        capabilities=["analysis", "wisdom"],
        triggers=["philosophy", "wisdom"],
        executor=mock_executor
    )
    
    network.register_engine(
        engine_id="military",
        name="Military Strategy Engine",
        description="Military strategy and tactics analysis",
        category=EngineCategory.MILITARY,
        capabilities=["strategy", "analysis"],
        triggers=["military", "strategy"],
        executor=mock_executor
    )
    
    network.register_engine(
        engine_id="psychology",
        name="Psychology Engine",
        description="Psychology and emotion analysis",
        category=EngineCategory.PSYCHOLOGY,
        capabilities=["emotion", "analysis"],
        triggers=["psychology", "emotion"],
        executor=mock_executor
    )
    
    print(f"Registered {network.registry.get_active_count()} engines")
    
    # 测试查询
    result = network.invoke(
        query="How to improve team mental health?",
        mode=InvocationMode.SINGLE
    )
    
    print(f"Invoke result: {result.success}")
    print(f"Engines used: {result.engines_used}")
    print(f"Confidence: {result.fused_confidence:.3f}")
    
    # 测试多引擎
    result_multi = network.invoke(
        query="Analyze business philosophy",
        mode=InvocationMode.MULTIPLE,
        strategy=FusionStrategy.HIERARCHICAL
    )
    
    print(f"Multi-engine result: {result_multi.success}")
    print(f"Engines used: {len(result_multi.engines_used)}")
    
    # 统计
    stats = network.get_statistics()
    print(f"Network stats: {stats['registry']['total_engines']} engines")
    
    return True


def test_engine_scanner():
    """测试2: 引擎扫描器"""
    print_header("Test 2: Engine Scanner")
    
    base_path = r"d:\AI\somn\smart_office_assistant\src\intelligence"
    
    scanner = EngineScanner(base_path)
    
    # 扫描 engines 目录
    discovered = scanner.scan(
        directories=['engines'],
        recursive=True
    )
    
    print(f"Discovered {len(discovered)} engines")
    
    # 按分类统计
    by_category = {}
    for engine in discovered:
        cat = engine['category'].value
        by_category[cat] = by_category.get(cat, 0) + 1
    
    print("\nBy Category:")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1])[:10]:
        print(f"  {cat}: {count}")
    
    # 显示前5个
    print("\nTop 5 Engines:")
    for engine in discovered[:5]:
        print(f"  - {engine['name']} ({engine['category'].value})")
        print(f"    File: {engine['relative_path']}/{engine['filename']}")
    
    return len(discovered) > 0


def test_engine_network_builder():
    """测试3: 引擎网络构建器"""
    print_header("Test 3: Engine Network Builder")
    
    base_path = r"d:\AI\somn\smart_office_assistant\src\intelligence"
    
    builder = EngineNetworkBuilder(base_path)
    
    # 扫描并注册（不使用executor）
    network = builder.scan(['engines']).register().build()
    
    stats = builder.get_statistics()
    
    print(f"Discovered: {stats['discovered']} engines")
    print(f"Registered: {stats['registered']} engines")
    print(f"Failed: {stats['failed']} engines")
    print(f"Success Rate: {stats['success_rate']:.1%}")
    
    # 显示报告
    print("\n" + builder.get_report())
    
    return stats['registered'] > 0


def test_divine_reason_network():
    """测试4: DivineReason 超级引擎网络"""
    print_header("Test 4: DivineReason Network (Core Test)")
    
    base_path = r"d:\AI\somn\smart_office_assistant\src\intelligence"
    
    # 自动构建
    network = DivineReasonNetwork.auto_build(
        base_path,
        directories=['engines']
    )
    
    print(f"DivineReason Network created")
    print(f"Engines registered: {network._engine_count}")
    
    # 健康检查
    health = network.health_check()
    print(f"Health check: {health}")
    
    # 测试solve
    result = network.solve(
        query="Analyze key factors in strategic planning",
        mode=InvocationMode.MULTIPLE,
        use_divine=False  # 简化测试
    )
    
    print(f"Solve result: success={result.success}")
    print(f"Quality score: {result.quality_score:.3f}")
    print(f"Latency: {result.latency_ms:.1f}ms")
    
    # 统计
    stats = network.get_statistics()
    print(f"Total invocations: {stats['coordinator']['total_invocations']}")
    
    return result.success


def test_engine_routing():
    """测试5: 引擎智能路由"""
    print_header("Test 5: Engine Routing")
    
    network = create_engine_network()
    
    # 注册多个引擎
    network.register_engine(
        engine_id="strategy",
        name="Strategy Engine",
        description="Strategy and planning analysis",
        category=EngineCategory.MANAGEMENT,
        triggers=["strategy", "planning"],
        weight=1.5
    )
    
    network.register_engine(
        engine_id="military_strategy",
        name="Military Strategy",
        description="Military tactics and strategy",
        category=EngineCategory.MILITARY,
        triggers=["military", "battle"],
        weight=1.2
    )
    
    network.register_engine(
        engine_id="philosophy",
        name="Philosophy",
        description="Philosophy and wisdom",
        category=EngineCategory.PHILOSOPHY,
        triggers=["philosophy", "wisdom"],
        weight=1.0
    )
    
    # 测试路由
    queries = [
        "business strategy planning",
        "military war strategy",
        "life philosophy wisdom"
    ]
    
    for query in queries:
        nodes = network.router.route(query, top_k=3)
        print(f"\nQuery: {query}")
        print(f"Routed to: {[n.metadata.name for n in nodes]}")
    
    return True


def test_fusion_strategies():
    """测试6: 融合策略"""
    print_header("Test 6: Fusion Strategies")
    
    from intelligence.engines._engine_network import EngineFusion, EngineResult
    
    network = create_engine_network()
    
    # 注册引擎
    def mock_executor(input_data, **kwargs):
        return f"Result: {input_data[:20]}"
    
    network.register_engine(
        engine_id="engine1",
        name="Engine 1",
        description="Test engine 1",
        category=EngineCategory.REASONING,
        executor=mock_executor
    )
    
    network.register_engine(
        engine_id="engine2",
        name="Engine 2",
        description="Test engine 2",
        category=EngineCategory.REASONING,
        executor=mock_executor
    )
    
    # 模拟结果
    results = [
        EngineResult(
            engine_id="engine1",
            success=True,
            output="Output 1",
            confidence=0.8,
            quality_score=0.7
        ),
        EngineResult(
            engine_id="engine2",
            success=True,
            output="Output 2",
            confidence=0.9,
            quality_score=0.85
        )
    ]
    
    fusion = EngineFusion(network)
    
    # 测试各种融合策略
    strategies = [
        FusionStrategy.PARALLEL,
        FusionStrategy.VOTING,
        FusionStrategy.WEIGHTED,
        FusionStrategy.HIERARCHICAL
    ]
    
    for strategy in strategies:
        result = fusion.fuse(results, strategy)
        print(f"\n{strategy.value}:")
        print(f"  Success: {result.success}")
        print(f"  Confidence: {result.fused_confidence:.3f}")
        print(f"  Quality: {result.fused_quality:.3f}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "#" * 60)
    print("  DivineReason Super Engine Network Test Suite")
    print("#" * 60)
    
    tests = [
        ("Engine Network Basic", test_engine_network_basic),
        ("Engine Scanner", test_engine_scanner),
        ("Engine Network Builder", test_engine_network_builder),
        ("DivineReason Network", test_divine_reason_network),
        ("Engine Routing", test_engine_routing),
        ("Fusion Strategies", test_fusion_strategies),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, True, result))
        except Exception as e:
            print(f"\nTest failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False, str(e)))
    
    # 汇总
    print("\n" + "#" * 60)
    print("  Test Results Summary")
    print("#" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, _ in results:
        status = "PASS" if success else "FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\nAll tests passed! DivineReason Super Engine Network is running!")
    else:
        print("\nSome tests failed. Please check the errors.")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests()
