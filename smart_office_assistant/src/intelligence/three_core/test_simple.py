# -*- coding: utf-8 -*-
"""
三核联动整合器 - 隔离测试 v1.0.0
"""

import sys
import os

# 设置项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)
os.chdir(project_root)

def test_imports():
    """测试导入"""
    print("=" * 80)
    print("测试: 模块导入")
    print("=" * 80)
    
    try:
        # 只导入三核联动模块自身
        from src.intelligence.three_core import (
            ThreeCoreIntegration,
            ResearchLevel,
            ResearchDepth,
            ResearchDimension,
            ComplexityLevel,
            MainLine,
            SagePhase,
        )
        print("✓ 三核联动模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_enums():
    """测试枚举"""
    print("\n" + "=" * 80)
    print("测试: 枚举定义")
    print("=" * 80)
    
    from src.intelligence.three_core import (
        ResearchLevel,
        ResearchDepth,
        ResearchDimension,
        ComplexityLevel,
        MainLine,
        SagePhase,
    )
    
    print(f"研究层级: {len([e for e in ResearchLevel])}个")
    for e in ResearchLevel:
        print(f"  - {e.value}")
    
    print(f"\n研究深度: {len([e for e in ResearchDepth])}个")
    for e in ResearchDepth:
        print(f"  - {e.value}")
    
    print(f"\n研究维度: {len([e for e in ResearchDimension])}个")
    for e in ResearchDimension:
        print(f"  - {e.value}")
    
    print(f"\n复杂度等级: {len([e for e in ComplexityLevel])}个")
    for e in ComplexityLevel:
        print(f"  - {e.value}")
    
    print(f"\n主线: {len([e for e in MainLine])}条")
    for e in MainLine:
        print(f"  - {e.value}")
    
    print(f"\n五层链路: {len([e for e in SagePhase])}个")
    for e in SagePhase:
        print(f"  - {e.value}")

def test_basic_flow():
    """测试基本流程"""
    print("\n" + "=" * 80)
    print("测试: 基本流程")
    print("=" * 80)
    
    from src.intelligence.three_core import (
        ThreeCoreIntegration,
        ResearchLevel,
        ResearchDepth,
        MainLine,
    )
    
    integration = ThreeCoreIntegration()
    
    test_cases = [
        "如何提升品牌认知度",
        "分析消费者情绪与购买决策",
        "制定季度增长策略",
        "评估市场竞争格局",
    ]
    
    for query in test_cases:
        print(f"\n查询: {query}")
        print("-" * 60)
        
        result = integration.three_core_dispatch(query)
        
        print(f"研究层级: {result.research_plan.level.value}")
        print(f"研究深度: {result.research_plan.depth.value}")
        print(f"ICE评分: {result.research_plan.ice_score} ({result.research_plan.priority})")
        print(f"主导主线: {result.dispatch_allocation.main_line.value}")
        print(f"协同主线: {[l.value for l in result.dispatch_allocation.secondary_lines]}")
        print(f"学学派: {result.wisdom_injection.schools[:3]}")
        print(f"链路: {result.wisdom_injection.phase_chain.value}")

def test_mapping_matrices():
    """测试映射矩阵"""
    print("\n" + "=" * 80)
    print("测试: 映射矩阵")
    print("=" * 80)
    
    from src.intelligence.three_core import (
        RESEARCH_LEVEL_MAINLINE_MATRIX,
        DEPTH_PHASE_MATRIX,
        DIMENSION_SCHOOL_MATRIX,
        SAGE_MAINLINE_MATRIX,
    )
    
    print(f"\n研究层级×主线映射: {len(RESEARCH_LEVEL_MAINLINE_MATRIX)}条")
    for level, (lines, complexity) in list(RESEARCH_LEVEL_MAINLINE_MATRIX.items())[:3]:
        print(f"  {level.value[:10]} → {[l.value[:8] for l in lines]}")
    
    print(f"\n深度×链路映射: {len(DEPTH_PHASE_MATRIX)}条")
    for depth, phase in list(DEPTH_PHASE_MATRIX.items())[:3]:
        print(f"  {depth.value[:10]} → {phase.value[:20]}")
    
    print(f"\n维度×学派映射: {len(DIMENSION_SCHOOL_MATRIX)}条")
    for dim, schools in list(DIMENSION_SCHOOL_MATRIX.items())[:3]:
        print(f"  {dim.value[:15]} → {schools[:2]}")
    
    print(f"\n七贤×主线映射: {len(SAGE_MAINLINE_MATRIX)}条")
    for sage, (line, weight) in SAGE_MAINLINE_MATRIX.items():
        print(f"  {sage} → {line.value[:8]} (权重: {weight})")

def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("Somn项目·三核联动整合器 v1.0.0")
    print("Three-Core Integration Test")
    print("=" * 80)
    
    success = test_imports()
    if not success:
        print("\n模块导入失败，退出测试")
        return
    
    test_enums()
    test_basic_flow()
    test_mapping_matrices()
    
    print("\n" + "=" * 80)
    print("测试完成!")
    print("=" * 80)

if __name__ == "__main__":
    main()
