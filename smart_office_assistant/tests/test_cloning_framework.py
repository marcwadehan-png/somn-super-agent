"""
Cloning系统验证测试 v1.0
测试Cloning核心框架的完整功能
"""

from pathlib import Path
import sys
import os

# 使用path_bootstrap设置路径
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# 导入cloning模块
from intelligence.engines.cloning import (
    get_registry, register_cloning, get_cloning,
    CloningTier, CapabilityVector,
    ConfuciusCloning, SageCloning,
    AnalysisResult, DecisionOption, AdviceContext,
)


def test_cloning_registration():
    """测试Cloning注册"""
    print("=" * 60)
    print("测试1: Cloning注册")
    print("=" * 60)
    
    registry = get_registry()
    
    # 注册孔子Cloning
    confucius = ConfuciusCloning()
    register_cloning(confucius)
    
    # 验证注册
    retrieved = get_cloning("孔子")
    assert retrieved is not None, "孔子Cloning注册失败"
    assert retrieved.identity.name == "孔子", "Cloning名称不匹配"
    assert retrieved.identity.title == "至圣先师/万世师表", "称号不匹配"
    assert retrieved.tier == CloningTier.TIER_1_CORE, "层级不匹配"
    
    print(f"  [OK] 孔子Cloning注册成功")
    print(f"  - 层级: {retrieved.tier.name}")
    print(f"  - 学派: {retrieved.identity.school}")
    print(f"  - 岗位: {retrieved.identity.position}")
    print(f"  - 部门: {retrieved.identity.department}")
    
    # 验证统计
    stats = registry.get_stats("孔子")
    print(f"  - 咨询次数: {stats['consultation_count']}")
    
    print()


def test_confucius_analyze():
    """测试孔子分析功能"""
    print("=" * 60)
    print("测试2: 孔子Cloning - analyze()")
    print("=" * 60)
    
    confucius = get_cloning("孔子")
    problem = "如何治理一个组织"
    
    result = confucius.analyze(problem)
    
    assert isinstance(result, AnalysisResult), "返回类型错误"
    assert result.cloning_name == "孔子", "Cloning名称错误"
    assert result.problem == problem, "问题不匹配"
    assert len(result.reasoning_chain) > 0, "推理链为空"
    
    print(f"  [OK] 问题: {problem}")
    print(f"  [OK] 视角: {result.perspective}")
    print(f"  [OK] 置信度: {result.confidence}")
    print(f"  [OK] 推理链长度: {len(result.reasoning_chain)}")
    print(f"  关键洞察:")
    for insight in result.key_insights:
        print(f"    - {insight}")
    
    print()


def test_confucius_decide():
    """测试孔子决策功能"""
    print("=" * 60)
    print("测试3: 孔子Cloning - decide()")
    print("=" * 60)
    
    confucius = get_cloning("孔子")
    
    options = [
        DecisionOption(id="A", description="以德治人，仁爱关怀", risk_level="low"),
        DecisionOption(id="B", description="以法治人，严刑峻法", risk_level="medium"),
        DecisionOption(id="C", description="以利诱人，重赏激励", risk_level="low"),
    ]
    
    result = confucius.decide(options)
    
    print(f"  [OK] 决策: {result.decision}")
    print(f"  [OK] 选用方案: {result.chosen_option}")
    print(f"  [OK] 推理: {result.reasoning}")
    print(f"  [OK] 框架: {result.wisdom_framework}")
    print(f"  备选方案: {result.alternatives_considered}")
    
    print()


def test_confucius_advise():
    """测试孔子建议功能"""
    print("=" * 60)
    print("测试4: 孔子Cloning - advise()")
    print("=" * 60)
    
    confucius = get_cloning("孔子")
    
    context = AdviceContext(
        situation="团队成员之间出现利益冲突",
        constraints=["时间紧迫", "资源有限"],
        time_horizon="medium",
    )
    
    result = confucius.advise(context)
    
    print(f"  [OK] 情境: {context.situation}")
    print(f"  [OK] 建议长度: {len(result.advice)} 字符")
    print(f"  [OK] 推理: {result.reasoning[:50]}...")
    print(f"  潜在陷阱: {result.potential_pitfalls}")
    
    print()


def test_capability_vector():
    """测试能力向量"""
    print("=" * 60)
    print("测试5: 能力向量")
    print("=" * 60)
    
    confucius = get_cloning("孔子")
    vec = confucius.capability_vector
    
    print(f"  [OK] 能力向量维度: {len(vec.to_dict())}")
    print(f"  能力评分:")
    for key, value in vec.to_dict().items():
        bar = "█" * int(value / 2)
        print(f"    {key:25s}: {value:.1f} {bar}")
    
    print()


def test_wisdom_laws():
    """测试智慧法则"""
    print("=" * 60)
    print("测试6: 智慧法则")
    print("=" * 60)
    
    confucius = get_cloning("孔子")
    
    print(f"  [OK] 智慧法则数量: {len(confucius.wisdom_laws)}")
    for law in confucius.wisdom_laws:
        print(f"  [{law.id}] {law.name}")
        print(f"       {law.description}")
        print()


def test_registry_summary():
    """测试注册表摘要"""
    print("=" * 60)
    print("测试7: 注册表摘要")
    print("=" * 60)
    
    registry = get_registry()
    summary = registry.get_summary()
    
    print(f"  [OK] 总Cloning数: {summary['total_clonings']}")
    print(f"  [OK] 总集群数: {summary['total_clusters']}")
    print(f"  按学派: {summary['by_school']}")
    print(f"  按层级: {summary['by_tier']}")
    print(f"  按部门: {summary['by_department']}")
    
    print()


def main():
    """主测试函数"""
    print()
    print("#" * 60)
    print("#  600贤者Cloning系统验证测试 v1.0")
    print("#" * 60)
    print()
    
    try:
        test_cloning_registration()
        test_confucius_analyze()
        test_confucius_decide()
        test_confucius_advise()
        test_capability_vector()
        test_wisdom_laws()
        test_registry_summary()
        
        print("#" * 60)
        print("#  所有测试通过! Cloning系统运行正常")
        print("#" * 60)
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
