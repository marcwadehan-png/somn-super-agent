# -*- coding: utf-8 -*-
"""
DivineReason 166引擎网络 V3.1 - 测试
======================================

验证142个子引擎分类体系
"""

import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, src_path)
os.chdir(src_path)


def test_concept_structure():
    """测试概念结构"""
    print("=" * 70)
    print("测试 1: 概念结构 - V3.1增强")
    print("=" * 70)

    from _divine_reason_network import (
        EngineCategory, SubEngineType, SpecialReasoningType,
        SubReasoningEngineRegistry
    )

    # 统计子引擎模板
    registry = SubReasoningEngineRegistry()
    templates = registry.SUB_ENGINE_TEMPLATES

    print("\n142个子推理引擎分类:")
    total = 0
    for subsystem, engines in templates.items():
        count = len(engines)
        total += count
        print(f"  {subsystem:15s}: {count:3d}个")

    print(f"\n  总计: {total}个子推理引擎")

    assert total == 142, f"子引擎总数应为142，实际为{total}"
    print("\n✅ 概念结构测试通过!")


def test_routing():
    """测试路由机制"""
    print("\n" + "=" * 70)
    print("测试 2: ProblemType路由机制")
    print("=" * 70)

    from _divine_reason_network import ProblemTypeRouter

    router = ProblemTypeRouter()
    stats = router.get_statistics()

    print(f"\n路由规则统计:")
    print(f"  - 路由的ProblemType数: {stats['routed_problem_types']}")
    print(f"  - 总路由规则数: {stats['total_rules']}")

    # 测试几个典型路由
    test_cases = [
        ("STRATEGY", "战略问题"),
        ("ETHICAL", "伦理问题"),
        ("CRISIS", "危机问题"),
        ("CREATIVE", "创意问题"),
        ("LEARNING", "学习问题"),
    ]

    print(f"\n路由示例:")
    for pt, desc in test_cases:
        routing = router.route(pt)
        print(f"  {pt:20s} ({desc}):")
        for sub in routing.get('sub_engines', [])[:2]:
            print(f"    - 子引擎: {sub[0]} ({sub[1]:.0%})")
        for special in routing.get('special_engines', [])[:2]:
            print(f"    - 特殊引擎: {special[0]} ({special[1]:.0%})")

    assert stats['routed_problem_types'] > 0, "应有路由规则"
    print("\n✅ 路由机制测试通过!")


def test_special_engines():
    """测试特殊引擎注册"""
    print("\n" + "=" * 70)
    print("测试 3: 特殊推理引擎 (10个)")
    print("=" * 70)

    from _divine_reason_network import SpecialReasoningEngineRegistry

    registry = SpecialReasoningEngineRegistry()
    registry.initialize_all()

    stats = registry.get_statistics()
    print(f"\n特殊推理引擎:")
    for name in stats['engine_list']:
        print(f"  - {name}")

    assert stats['total_registered'] == 10, "应有10个特殊引擎"
    print("\n✅ 特殊引擎注册测试通过!")


def test_full_network():
    """测试完整引擎网络"""
    print("\n" + "=" * 70)
    print("测试 4: DivineReason 166引擎网络 V3.1")
    print("=" * 70)

    from intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
    from _divine_reason_network import create_divine_reason_network

    network = create_divine_reason_network(
        engine_table=WisdomDispatcher._ENGINE_TABLE,
    )

    stats = network.get_statistics()

    print(f"\n引擎网络统计 (V{stats['version']}):")
    print(f"  - WisdomSchool核心引擎: {stats['wisdom_school']}个")
    print(f"  - 子推理引擎: {stats['sub_reasoning']}个")
    print(f"  - 特殊推理引擎: {stats['special_reasoning']}个")
    print(f"  - 总计: {stats['total_engines']}个")
    print(f"  - 路由规则: {stats['routing_rules']}条")

    print(f"\n子引擎分布:")
    for subsystem, count in stats['by_subsystem'].items():
        print(f"  {subsystem:15s}: {count:3d}个")

    # 验证总数
    expected = stats['wisdom_school'] + stats['sub_reasoning'] + stats['special_reasoning']
    assert expected == 194, f"预期总数应为194，实际为{expected}"

    print("\n✅ 完整引擎网络测试通过!")


def test_reasoning():
    """测试推理流程"""
    print("\n" + "=" * 70)
    print("测试 5: 推理流程")
    print("=" * 70)

    from intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
    from _divine_reason_network import create_divine_reason_network

    network = create_divine_reason_network(
        engine_table=WisdomDispatcher._ENGINE_TABLE,
    )

    # 测试战略问题推理
    result = network.reason(
        problem="公司面临竞争对手的挑战，应该如何应对？",
        problem_type="STRATEGY"
    )

    print(f"\n推理请求:")
    print(f"  问题: {result['problem'][:30]}...")
    print(f"  问题类型: {result['problem_type']}")

    print(f"\n选择的引擎:")
    print(f"  特殊引擎 ({len(result['selected_special_engines'])}个):")
    for name, engine, weight in result['selected_special_engines'][:3]:
        print(f"    - {name} ({weight:.0%})")

    print(f"  子引擎 ({len(result['selected_sub_engines'])}个):")
    for name, engine, weight in result['selected_sub_engines'][:3]:
        print(f"    - {name} ({weight:.0%})")

    print("\n✅ 推理流程测试通过!")


def main():
    print("\n" + "=" * 70)
    print(" DivineReason 166引擎网络 V3.1 - 增强优化测试")
    print("=" * 70)

    try:
        test_concept_structure()
        test_routing()
        test_special_engines()
        test_full_network()
        test_reasoning()

        print("\n" + "=" * 70)
        print(" 🎉 所有测试通过! V3.1架构验证成功!")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
