# -*- coding: utf-8 -*-
"""
DivineReason - 至高推理引擎测试 V3.1.0
"""

import sys
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

from intelligence.reasoning._unified_reasoning_engine import (
    DivineReason, UnifiedConfig, SuperGraph, UnifiedNode, UnifiedEdge,
    NodeType, EdgeType, ReasoningMode, InsightType, ReasoningMetadata,
    GraphStatistics, UnifiedEvaluator, UnifiedGenerator, create_divine_engine,
    solve_with_divine, ReasoningResult, ThoughtPath,
    create_super_engine, solve_with_super_engine
)


def test_engine_creation():
    """测试引擎创建"""
    print("\n" + "="*60)
    print("测试 1: DivineReason V3.1.0 引擎创建")
    print("="*60)
    
    engine = DivineReason()
    print(f"✓ 引擎: {engine.ENGINE_NAME}")
    print(f"✓ 版本: {engine.VERSION}")
    print(f"✓ 模式: {engine.config.default_mode.value}")
    print(f"✓ 缓存: {engine.config.enable_cache}")
    print(f"✓ 批评: {engine.config.enable_critique}")
    
    assert engine.ENGINE_NAME == "DivineReason"
    assert engine.VERSION == "6.2.0"
    print("\n✅ 通过")


def test_node_types():
    """测试节点类型"""
    print("\n" + "="*60)
    print("测试 2: 节点类型 (15种)")
    print("="*60)
    
    types = [t.value for t in NodeType]
    print(f"✓ 类型: {len(types)}种")
    for t in types:
        print(f"    {t}")
    
    assert len(types) >= 13  # 至少13种
    print("\n✅ 通过")


def test_reasoning_modes():
    """测试推理模式"""
    print("\n" + "="*60)
    print("测试 3: 推理模式 (9种)")
    print("="*60)
    
    modes = [m.value for m in ReasoningMode]
    print(f"✓ 模式: {len(modes)}种")
    for m in modes:
        print(f"    {m}")
    
    assert len(modes) == 9
    print("\n✅ 通过")


def test_super_graph():
    """测试超级图"""
    print("\n" + "="*60)
    print("测试 4: 超级图创建")
    print("="*60)
    
    graph = SuperGraph("测试问题")
    root = graph.create_root("根节点")
    
    # 添加多种节点
    n1 = graph.add_node("LongCoT节点", NodeType.LONG_COT_STEP, [root.node_id], depth=1)
    n2 = graph.add_node("ToT分支", NodeType.TOT_BRANCH, [root.node_id], depth=1)
    n3 = graph.add_node("顿悟时刻", NodeType.INSIGHT, [n1.node_id], depth=2, is_insight=True, insight_type="breakthrough", insight_impact=0.95)
    n4 = graph.add_node("反思节点", NodeType.SELF_CORRECTION, [n3.node_id], depth=3, is_reflection=True)
    n5 = graph.add_node("批评节点", NodeType.CRITIQUE, [n2.node_id], depth=2, is_critique=True)
    n6 = graph.add_node("最终答案", NodeType.FINAL, [n4.node_id], depth=4)
    
    stats = graph.get_statistics()
    print(f"✓ 节点: {stats.total_nodes}")
    print(f"✓ 边数: {stats.total_edges}")
    print(f"✓ 顿悟: {stats.insights_count}")
    print(f"✓ 反思: {stats.reflections_count}")
    print(f"✓ 批评: {stats.critiques_count}")
    print(f"✓ 深度: {stats.max_depth}")
    
    # 测试路径
    best_path = graph.get_best_path()
    print(f"✓ 最佳路径: {best_path.length}个节点")
    print(f"✓ 路径评分: {best_path.total_score:.3f}")
    
    assert stats.total_nodes >= 6
    print("\n✅ 通过")


def test_evaluator():
    """测试评估器"""
    print("\n" + "="*60)
    print("测试 5: 评估器")
    print("="*60)
    
    config = UnifiedConfig()
    evaluator = UnifiedEvaluator(config)
    
    node = UnifiedNode(
        node_id="test",
        content="这是一个关键的分析：突然意识到问题的本质是整合所有资源。",
        depth=2
    )
    
    scores = evaluator.evaluate_node(node, {'problem': '测试问题'})
    print(f"✓ 评分维度: {len(scores)}个")
    for k, v in scores.items():
        print(f"    {k}: {v:.3f}")
    print(f"✓ 综合评分: {node.combined_score:.3f}")
    
    # 顿悟检测
    insight = evaluator.detect_insight(node.content)
    if insight:
        print(f"✓ 顿悟检测: {insight[0]} (impact={insight[1]:.2f})")
    
    # 缓存测试
    scores2 = evaluator.evaluate_node(node, {'problem': '测试问题'})
    assert scores == scores2
    print(f"✓ 缓存工作: ✓")
    
    print("\n✅ 通过")


def test_divine_solve():
    """测试DivineReason解决"""
    print("\n" + "="*60)
    print("测试 6: DivineReason解决问題")
    print("="*60)
    
    engine = DivineReason(config=UnifiedConfig(max_nodes=30, max_depth=5))
    result = engine.solve("如何提高团队的工作效率？", mode=ReasoningMode.DIVINE)
    
    print(f"✓ 成功: {result.success}")
    print(f"✓ 模式: {result.mode}")
    print(f"✓ 质量: {result.quality_score:.3f}")
    
    stats = result.statistics
    print(f"✓ 统计:")
    print(f"    节点: {stats.total_nodes}")
    print(f"    边数: {stats.total_edges}")
    print(f"    深度: {stats.max_depth}")
    print(f"    顿悟: {stats.insights_count}")
    print(f"    反思: {stats.reflections_count}")
    print(f"    批评: {stats.critiques_count}")
    
    # 结果字典
    result_dict = result.to_dict()
    print(f"\n✓ 结果结构:")
    print(f"    engine: {result_dict['engine']}")
    print(f"    version: {result_dict['version']}")
    print(f"    success: {result_dict['success']}")
    print(f"    quality_score: {result_dict['quality_score']}")
    
    assert result.success
    print("\n✅ 通过")


def test_all_modes():
    """测试所有模式"""
    print("\n" + "="*60)
    print("测试 7: 所有推理模式对比")
    print("="*60)
    
    modes = [
        ReasoningMode.LINEAR,
        ReasoningMode.BRANCHING,
        ReasoningMode.REACTIVE,
        ReasoningMode.GRAPH,
        ReasoningMode.DIVINE,
    ]
    
    print(f"\n{'模式':<12} | {'节点':>5} | {'深度':>4} | {'顿悟':>4} | {'反思':>4} | {'质量':>6}")
    print("-" * 55)
    
    for mode in modes:
        engine = DivineReason(config=UnifiedConfig(max_nodes=15, max_depth=4))
        result = engine.solve("分析人工智能对未来工作的影响", mode=mode)
        stats = result.statistics
        print(f"{mode.value:<12} | {stats.total_nodes:>5} | {stats.max_depth:>4} | "
              f"{stats.insights_count:>4} | {len(result.reflections):>4} | {result.quality_score:>6.3f}")
    
    print("\n✅ 通过")


def test_result_structure():
    """测试结果结构"""
    print("\n" + "="*60)
    print("测试 8: ReasoningResult 结构")
    print("="*60)
    
    result = ReasoningResult(
        engine="DivineReason",
        version="6.2.0",
        problem="测试问题",
        mode="divine",
        success=True,
        solution="测试解决方案",
        quality_score=0.85
    )
    
    result.insights.append({'type': 'breakthrough', 'content': '测试顿悟'})
    result.reflections.append({'content': '测试反思'})
    
    result_dict = result.to_dict()
    print(f"✓ engine: {result_dict['engine']}")
    print(f"✓ version: {result_dict['version']}")
    print(f"✓ success: {result_dict['success']}")
    print(f"✓ solution: {result_dict['solution'][:30]}...")
    print(f"✓ quality_score: {result_dict['quality_score']}")
    print(f"✓ insights_count: {result_dict['insights_count']}")
    print(f"✓ reflections_count: {result_dict['reflections_count']}")
    
    assert result.success
    print("\n✅ 通过")


def test_cache_performance():
    """测试缓存性能"""
    print("\n" + "="*60)
    print("测试 9: 缓存性能")
    print("="*60)
    
    import time
    
    config = UnifiedConfig(enable_cache=True, max_cache_size=100)
    evaluator = UnifiedEvaluator(config)
    generator = UnifiedGenerator(config=config)
    
    node = UnifiedNode(node_id="perf_test", content="性能测试内容", depth=1)
    
    # 第一次评估
    start = time.time()
    for _ in range(100):
        evaluator.evaluate_node(node, {'problem': '测试'})
    first_time = time.time() - start
    
    # 第二次评估（使用缓存）
    start = time.time()
    for _ in range(100):
        evaluator.evaluate_node(node, {'problem': '测试'}, use_cache=True)
    cached_time = time.time() - start
    
    print(f"✓ 首次评估: {first_time*1000:.2f}ms")
    print(f"✓ 缓存评估: {cached_time*1000:.2f}ms")
    print(f"✓ 加速比: {first_time/cached_time:.1f}x")
    
    evaluator.clear_cache()
    generator.clear_cache()
    print(f"✓ 缓存清空: ✓")
    
    print("\n✅ 通过")


def test_factory_functions():
    """测试工厂函数"""
    print("\n" + "="*60)
    print("测试 10: 工厂函数")
    print("="*60)
    
    # create_divine_engine
    engine1 = create_divine_engine()
    print(f"✓ create_divine_engine: {engine1.ENGINE_NAME} v{engine1.VERSION}")
    
    # create_super_engine (别名)
    engine2 = create_super_engine()
    print(f"✓ create_super_engine (别名): {engine2.ENGINE_NAME}")
    
    # solve_with_divine
    result1 = solve_with_divine("测试", max_nodes=10)
    print(f"✓ solve_with_divine: 节点={result1.statistics.total_nodes}")
    
    # solve_with_super_engine (别名)
    result2 = solve_with_super_engine("测试", max_nodes=10)
    print(f"✓ solve_with_super_engine: 节点={result2.statistics.total_nodes}")
    
    print("\n✅ 通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🔮 DivineReason V3.1.0 - 至高推理引擎测试套件")
    print("="*60)
    print(f"版本: V3.1.0")
    print(f"四大体系: GoT + LongCoT + ToT + ReAct + DivineReason扩展")
    print("="*60)
    
    tests = [
        test_engine_creation,
        test_node_types,
        test_reasoning_modes,
        test_super_graph,
        test_evaluator,
        test_divine_solve,
        test_all_modes,
        test_result_structure,
        test_cache_performance,
        test_factory_functions,
    ]
    
    passed = failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n❌ 失败: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 结果: {passed}/{len(tests)} 通过")
    if failed == 0:
        print("🎉 全部通过！ DivineReason V3.1.0 运行正常！")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
