# -*- coding: utf-8 -*-
"""
三核联动整合器测试脚本 v1.0.0

测试三核联动架构的完整流程

运行方式:
    python -m src.intelligence.three_core.test_three_core
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.intelligence.three_core import (
    ThreeCoreIntegration,
    get_three_core_integration,
    ResearchLevel,
    ResearchDepth,
    ComplexityLevel,
    MainLine,
    SagePhase,
)

def test_three_core_basic():
    """测试基本功能"""
    print("=" * 80)
    print("测试1: 基本三核联动")
    print("=" * 80)
    
    integration = ThreeCoreIntegration()
    
    # 测试查询
    test_queries = [
        "如何提升品牌认知度",
        "分析消费者购买决策的潜意识因素",
        "制定季度增长策略",
        "评估市场竞争格局",
        "设计用户留存机制",
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        print("-" * 60)
        
        # 完整三核联动
        result = integration.three_core_dispatch(query)
        
        print(f"研究层级: {result.research_plan.level.value}")
        print(f"研究深度: {result.research_plan.depth.value}")
        print(f"ICE评分: {result.research_plan.ice_score} ({result.research_plan.priority})")
        print(f"预估耗时: {result.research_plan.estimated_hours}小时")
        print(f"\n交叉研究点: {len(result.research_plan.cross_points)}个")
        for dim in result.research_plan.dimensions:
            print(f"  - {dim.value}")
        
        print(f"\n主导主线: {result.dispatch_allocation.main_line.value}")
        print(f"协同主线: {[l.value for l in result.dispatch_allocation.secondary_lines]}")
        print(f"跨线协同: {result.dispatch_allocation.cross_sync_type.value}")
        print(f"决策制: {result.dispatch_allocation.decision_system.value}")
        
        print(f"\n学学派: {result.wisdom_injection.schools}")
        print(f"链路阶段: {result.wisdom_injection.phase_chain.value}")
        print(f"代表贤者: {result.wisdom_injection.sage_representatives}")

def test_mapping_matrices():
    """测试映射矩阵"""
    print("\n" + "=" * 80)
    print("测试2: 映射矩阵")
    print("=" * 80)
    
    from src.intelligence.three_core import (
        RESEARCH_LEVEL_MAINLINE_MATRIX,
        DEPTH_PHASE_MATRIX,
        DIMENSION_SCHOOL_MATRIX,
        SAGE_MAINLINE_MATRIX,
    )
    
    print("\n研究层级 × 主线映射:")
    for level, (lines, complexity) in RESEARCH_LEVEL_MAINLINE_MATRIX.items():
        print(f"  {level.value} → {[l.value for l in lines]} ({complexity.value})")
    
    print("\n研究深度 × 五层链路:")
    for depth, phase in DEPTH_PHASE_MATRIX.items():
        print(f"  {depth.value} → {phase.value}")
    
    print("\n维度 × 学派映射:")
    for dim, schools in DIMENSION_SCHOOL_MATRIX.items():
        print(f"  {dim.value} → {schools}")
    
    print("\n七贤 × 主线映射:")
    for sage, (line, weight) in SAGE_MAINLINE_MATRIX.items():
        print(f"  {sage} → {line.value} (权重: {weight})")

def test_research_plan():
    """测试研究计划解析"""
    print("\n" + "=" * 80)
    print("测试3: 研究计划解析")
    print("=" * 80)
    
    integration = ThreeCoreIntegration()
    
    # 测试不同类型查询
    test_cases = [
        ("消费者情绪波动与购买决策的关系研究", "情绪+决策研究"),
        ("实时监控市场数据变化", "数字化+实时"),
        ("分析品牌溢价能力", "价值感知"),
        ("制定长期增长战略", "长期+增长"),
    ]
    
    for query, desc in test_cases:
        print(f"\n{desc}: {query}")
        print("-" * 60)
        
        plan = integration.parse_research_depth(query)
        
        print(f"层级: {plan.level.value}")
        print(f"深度: {plan.depth.value}")
        print(f"维度: {[d.value for d in plan.dimensions]}")
        print(f"方向: {[d.value for d in plan.directions]}")
        print(f"ICE: {plan.ice_score} → {plan.priority}")
        print(f"耗时: {plan.estimated_hours}h")

def test_dispatch_allocation():
    """测试调度分配"""
    print("\n" + "=" * 80)
    print("测试4: 调度分配")
    print("=" * 80)
    
    integration = ThreeCoreIntegration()
    
    test_cases = [
        (ResearchLevel.L1_QUANTITATIVE, "定量研究"),
        (ResearchLevel.L2_QUALITATIVE, "定性研究"),
        (ResearchLevel.L4_NEURO, "神经科学研究"),
    ]
    
    for level, desc in test_cases:
        print(f"\n{desc}:")
        print("-" * 60)
        
        complexity = integration._level_to_complexity(level)
        main_lines, sync_type = integration.select_main_lines(complexity)
        
        print(f"复杂度: {complexity.value}")
        print(f"主线: {[l.value for l in main_lines]}")
        print(f"协同类型: {sync_type.value}")

def test_wisdom_injection():
    """测试智慧注入"""
    print("\n" + "=" * 80)
    print("测试5: 智慧注入")
    print("=" * 80)
    
    integration = ThreeCoreIntegration()
    
    from src.intelligence.three_core import (
        ResearchDimension,
        MainLine,
    )
    
    # 模拟调度分配
    mock_dispatch = integration.allocate_positions(
        integration.parse_research_depth("消费者情绪研究"),
        [MainLine.ECONOMIC, MainLine.CIVIL_ADMIN]
    )
    
    mock_research = integration.parse_research_depth("消费者情绪研究")
    
    wisdom = integration.inject_wisdom(mock_dispatch, mock_research)
    
    print(f"学学派: {wisdom.schools}")
    print(f"五层链路: {wisdom.phase_chain.value}")
    print(f"代表贤者: {wisdom.sage_representatives}")
    print(f"Claw配置数: {len(wisdom.claws)}")

def test_fusion_result():
    """测试融合结果"""
    print("\n" + "=" * 80)
    print("测试6: 融合结果")
    print("=" * 80)
    
    integration = ThreeCoreIntegration()
    
    query = "如何利用消费者情绪提升品牌价值"
    result = integration.three_core_dispatch(query)
    
    print(f"\n查询: {query}")
    print("\n融合决策摘要:")
    fusion = result.fusion_decision
    
    for key, value in fusion["summary"].items():
        print(f"  {key}: {value}")
    
    print("\n研究计划:")
    for key, value in fusion["research_plan"].items():
        print(f"  {key}: {value}")
    
    print("\n调度分配:")
    for key, value in fusion["dispatch"].items():
        print(f"  {key}: {value}")
    
    print("\n智慧注入:")
    for key, value in fusion["wisdom"].items():
        print(f"  {key}: {value}")

def test_singleton():
    """测试全局单例"""
    print("\n" + "=" * 80)
    print("测试7: 全局单例")
    print("=" * 80)
    
    instance1 = get_three_core_integration()
    instance2 = get_three_core_integration()
    
    print(f"实例1: {id(instance1)}")
    print(f"实例2: {id(instance2)}")
    print(f"是同一实例: {instance1 is instance2}")

def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 80)
    print("Somn项目·三核联动整合器测试")
    print("Three-Core Integration Test Suite v1.0.0")
    print("=" * 80)
    
    try:
        test_three_core_basic()
        test_mapping_matrices()
        test_research_plan()
        test_dispatch_allocation()
        test_wisdom_injection()
        test_fusion_result()
        test_singleton()
        
        print("\n" + "=" * 80)
        print("全部测试完成!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
