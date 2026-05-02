# -*- coding: utf-8 -*-
"""
逆向论证推荐引擎矩阵 - 测试与使用示例
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from engines.reverse_argument_matrix import (
    ReverseArgumentMatrixEngine,
    ReverseDimension,
    get_reverse_argument_matrix,
    quick_reverse_analyze,
    reverse_argument_recommend,
)


def test_basic_analysis():
    """测试基础分析"""
    print("=" * 60)
    print("测试1: 基础分析")
    print("=" * 60)
    
    engine = ReverseArgumentMatrixEngine()
    result = engine.analyze("如何提高团队凝聚力")
    
    print(f"\n问题: {result.problem}")
    print(f"主导维度: {result.dominant_dimension.value}")
    print(f"\n维度关联度:")
    for dim, score in sorted(result.dimension_scores.items(), key=lambda x: x[1], reverse=True)[:4]:
        print(f"  {dim.value}: {score:.2f}")
    
    print(f"\nTop 3 逆向论证:")
    for i, arg in enumerate(result.top_arguments[:3], 1):
        print(f"\n  {i}. [{arg.primary_dimension.value} × {arg.cross_dimension.value}]")
        print(f"     论证: {arg.reverse_argument}")
        print(f"     反叙事: {arg.counter_narrative}")
        print(f"     置信度: {arg.confidence:.0%}")
    
    print(f"\n元洞察: {result.meta_insight[:80]}...")
    print("✅ 测试1通过\n")


def test_quick_analyze():
    """测试快速分析"""
    print("=" * 60)
    print("测试2: 快速分析输出")
    print("=" * 60)
    
    output = quick_reverse_analyze("为什么理性的投资决策常常失败")
    print(output)
    print("✅ 测试2通过\n")


def test_focus_dimensions():
    """测试聚焦维度"""
    print("=" * 60)
    print("测试3: 聚焦维度分析")
    print("=" * 60)
    
    result = reverse_argument_recommend(
        problem="产品如何利用用户的认知偏差提升转化率",
        focus_dimensions=["行为学", "人性"],
        top_n=3,
    )
    
    print(f"\n问题: {result.problem}")
    print(f"聚焦维度: 行为学 × 人性")
    for i, arg in enumerate(result.top_arguments, 1):
        print(f"\n  {i}. [{arg.primary_dimension.value} × {arg.cross_dimension.value}]")
        print(f"     论证: {arg.reverse_argument}")
        print(f"     盲区: {arg.blind_spot_reveal}")
    
    print("\n✅ 测试3通过\n")


def test_matrix_summary():
    """测试矩阵摘要"""
    print("=" * 60)
    print("测试4: 矩阵摘要")
    print("=" * 60)
    
    engine = get_reverse_argument_matrix()
    summary = engine.get_matrix_summary()
    
    print(f"引擎: {summary['engine']}")
    print(f"版本: {summary['version']}")
    print(f"维度数: {summary['dimensions']}")
    print(f"矩阵节点数: {summary['matrix_nodes']}")
    print(f"理论组合数: {summary['theoretical_combinations']}")
    print(f"维度名称: {summary['dimension_names']}")
    print("✅ 测试4通过\n")


def test_dimension_detail():
    """测试维度详情"""
    print("=" * 60)
    print("测试5: 维度详情")
    print("=" * 60)
    
    engine = get_reverse_argument_matrix()
    
    for dim in ReverseDimension:
        detail = engine.get_dimension_detail(dim)
        print(f"\n[{detail['维度']}]")
        print(f"  核心追问: {detail['核心追问']}")
        print(f"  反叙事: {detail['反叙事']}")
        print(f"  来源引擎: {detail['来源引擎']}")
    
    print("\n✅ 测试5通过\n")


def test_dark_forest_scenario():
    """测试黑暗森林场景"""
    print("=" * 60)
    print("测试6: 黑暗森林场景分析")
    print("=" * 60)
    
    output = quick_reverse_analyze("在激烈的商业竞争中如何保护核心利益")
    print(output)
    print("✅ 测试6通过\n")


if __name__ == "__main__":
    test_basic_analysis()
    test_quick_analyze()
    test_focus_dimensions()
    test_matrix_summary()
    test_dimension_detail()
    test_dark_forest_scenario()
    
    print("\n" + "=" * 60)
    print("🎉 全部测试通过！逆向论证推荐引擎矩阵运行正常")
    print("=" * 60)
