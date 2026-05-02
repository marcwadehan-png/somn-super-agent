# -*- coding: utf-8 -*-
"""独立测试智慧编码系统"""

import sys
from pathlib import Path

# 直接添加路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# 直接导入wisdom_encoding，绕过intelligence的复杂导入
from intelligence.wisdom_encoding import (
    get_wisdom_registry,
    WisdomEncodingRegistry,
    SageCode,
    CognitiveDimension,
    ProblemCategory,
)


def test_registry():
    """测试注册表"""
    print("测试注册表创建...")
    registry = get_wisdom_registry()
    stats = registry.get_statistics()
    print(f"✓ 统计信息: {stats}")
    return registry


def test_wisdom_laws(registry):
    """测试智慧法则"""
    print("\n测试智慧法则...")
    laws = registry._wisdom_laws
    print(f"✓ 智慧法则数量: {len(laws)}")
    for lid, law in list(laws.items())[:3]:
        print(f"  - {lid}: {law.name}")


def test_sages(registry):
    """测试贤者"""
    print("\n测试贤者注册...")
    sages = registry._sage_codes
    print(f"✓ 贤者数量: {len(sages)}")
    for sid, sage in list(sages.items())[:3]:
        print(f"  - {sid}: {sage.name} ({sage.school})")


def test_query(registry):
    """测试查询"""
    print("\n测试问题查询...")
    query = "如何治理一个组织"
    results = registry.query_by_problem(query, top_k=3)
    print(f"✓ 查询 '{query}' 结果:")
    for sage, score in results:
        print(f"  - {sage.name} [匹配度: {score:.2f}]")


def test_blend(registry):
    """测试认知混合"""
    print("\n测试认知维度混合...")
    blend = registry.get_cognitive_blend(ProblemCategory.SOCIAL_GOVERNANCE)
    print(f"✓ 问题类别: {blend.problem_category.value}")
    print(f"✓ 维度数量: {len(blend.dimension_weights)}")
    if blend.primary_sages:
        print(f"✓ 主要贤者: {[s[0].name for s in blend.primary_sages[:3]]}")


def test_dispatch(registry):
    """测试分发"""
    print("\n测试智慧分发...")
    query = "如何做好战略规划"
    blend = registry.get_cognitive_blend(ProblemCategory.BUSINESS_STRATEGY)
    response = registry.dispatch_wisdom(blend, query)
    print(f"✓ 查询: {response['query']}")
    print(f"✓ 推荐贤者: {response['primary_sages']}")
    print(f"✓ 推荐: {response['recommendation']}")


if __name__ == "__main__":
    print("=" * 60)
    print("智慧编码系统独立测试")
    print("=" * 60)

    registry = test_registry()
    test_wisdom_laws(registry)
    test_sages(registry)
    test_query(registry)
    test_blend(registry)
    test_dispatch(registry)

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
