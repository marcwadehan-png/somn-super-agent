# -*- coding: utf-8 -*-
"""
智慧编码系统验证脚本

测试 WisdomEncodingRegistry 的核心功能

运行:
    python -m tests.wisdom_encoding_verification

版本: v1.0
创建: 2026-04-10
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.intelligence.wisdom_encoding import (
    get_wisdom_registry,
    WisdomEncodingRegistry,
    SageCode,
    CognitiveDimension,
    ProblemCategory,
)


def test_registry_creation():
    """测试注册表创建"""
    print("=" * 60)
    print("测试1: 注册表创建")
    print("=" * 60)

    registry = get_wisdom_registry()
    stats = registry.get_statistics()

    print(f"✓ 注册表创建成功")
    print(f"  - 贤者总数: {stats['total_sages']}")
    print(f"  - 学派数: {len(stats['schools'])}")
    print(f"  - 智慧法则: {stats['wisdom_laws']}")
    print(f"  - 认知维度: {stats['dimensions']}")
    print(f"  - 问题类别: {stats['categories']}")

    print()
    return registry


def test_sage_queries(registry: WisdomEncodingRegistry):
    """测试贤者查询"""
    print("=" * 60)
    print("测试2: 贤者查询")
    print("=" * 60)

    test_cases = [
        "如何治理一个组织",
        "商业战略规划怎么做",
        "个人成长应该如何修炼",
        "遇到危机应该如何应对",
        "长期规划应该考虑什么",
    ]

    for query in test_cases:
        print(f"\n查询: '{query}'")
        results = registry.query_by_problem(query, top_k=3)
        if results:
            for sage, score in results:
                print(f"  → {sage.name} ({sage.school}) [匹配度: {score:.2f}]")
        else:
            print(f"  → 暂无匹配的贤者")

    print()


def test_cognitive_blend(registry: WisdomEncodingRegistry):
    """测试认知维度混合"""
    print("=" * 60)
    print("测试3: 认知维度混合")
    print("=" * 60)

    categories = [
        ProblemCategory.SOCIAL_GOVERNANCE,
        ProblemCategory.BUSINESS_STRATEGY,
        ProblemCategory.PERSONAL_GROWTH,
        ProblemCategory.CRISIS_RESPONSE,
    ]

    for category in categories:
        blend = registry.get_cognitive_blend(category)

        print(f"\n问题类别: {category.value}")
        print(f"  维度权重:")
        for dim, weight in blend.dimension_weights.items():
            print(f"    - {dim.value}: {weight:.2f}")

        if blend.primary_sages:
            print(f"  主要贤者:")
            for sage, score in blend.primary_sages[:3]:
                print(f"    - {sage.name} ({sage.era})")

    print()


def test_wisdom_dispatch(registry: WisdomEncodingRegistry):
    """测试智慧分发"""
    print("=" * 60)
    print("测试4: 智慧分发")
    print("=" * 60)

    query = "作为一个企业管理者，如何做出更好的战略决策？"
    blend = registry.get_cognitive_blend(ProblemCategory.BUSINESS_STRATEGY)
    response = registry.dispatch_wisdom(blend, query)

    print(f"\n查询: {query}")
    print(f"\n响应:")
    print(f"  问题类别: {response['problem_category']}")
    print(f"  推荐贤者: {', '.join(response['primary_sages'])}")
    print(f"  智慧法则: {', '.join(response['wisdom_laws'])}")
    print(f"  推荐: {response['recommendation']}")

    print()


def test_wisdom_laws(registry: WisdomEncodingRegistry):
    """测试智慧法则"""
    print("=" * 60)
    print("测试5: 十大智慧法则")
    print("=" * 60)

    for law_id, law in list(registry._wisdom_laws.items())[:10]:
        print(f"\n{law_id}: {law.name}")
        print(f"  描述: {law.description}")
        print(f"  来源贤者: {', '.join(law.source_sages[:3])}")
        print(f"  实现模式: {law.implementation_pattern}")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("智慧编码系统验证")
    print("=" * 60 + "\n")

    # 测试注册表创建
    registry = test_registry_creation()

    # 测试贤者查询
    test_sage_queries(registry)

    # 测试认知维度混合
    test_cognitive_blend(registry)

    # 测试智慧分发
    test_wisdom_dispatch(registry)

    # 测试智慧法则
    test_wisdom_laws(registry)

    print("=" * 60)
    print("验证完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
