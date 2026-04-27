"""
v8.1.0 智慧系统实际调用体验
演示统一默认调用接口的输出效果
"""
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from intelligence.super_wisdom_coordinator import (

    SuperWisdomCoordinator,
    OutputStyle
)

def demo_super_wisdom():
    print("=" * 70)
    print("v8.1.0 超级智慧协调器 - 实际调用体验")
    print("=" * 70)

    coordinator = SuperWisdomCoordinator()

    # 测试用例 - 不同领域的实际问题
    test_cases = [
        {
            "query": "公司在快速扩张期，核心员工纷纷离职，如何留住人才同时保持创新活力？",
            "context": "企业人才管理"
        },
        {
            "query": "面对人生重大抉择，既想追求梦想又担心风险太大，该如何决策？",
            "context": "个人重大决策"
        },
        {
            "query": "商业谈判中如何既坚持原则又达成双赢？有什么古老智慧可以借鉴？",
            "context": "商业谈判策略"
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"【场景 {i}】{case['context']}")
        print(f"{'='*70}")
        print(f"\n>>> 用户问题: {case['query']}")
        print("\n" + "-" * 70)

        result = coordinator.analyze(
            query_text=case['query'],
            context=case.get('context'),
            output_style=OutputStyle.COMPREHENSIVE
        )

        print(f"\n📊 分析概览:")
        print(f"   综合置信度: {result.confidence:.1%}")
        print(f"   激活学派数: {result.schools_contributed}")
        print(f"   处理层级: {' / '.join(result.layers_processed)}")
        print(f"   综合评分: {result.overall_score:.2f}")

        if result.activated_schools:
            schools = result.activated_schools[:5]
            print(f"   主要学派: {' / '.join(schools)}")

        print(f"\n💡 主洞察 (Primary Insight):")
        print(f"   {result.primary_insight[:150]}...")
        
        if result.secondary_insights:
            print(f"\n🔍 次级洞察:")
            for idx, insight in enumerate(result.secondary_insights[:2], 1):
                print(f"   {idx}. {insight[:80]}...")

        if result.action_recommendations:
            print(f"\n⚡ 行动建议:")
            for rec in result.action_recommendations[:3]:
                print(f"   • {rec[:80]}...")

        if result.ancient_wisdom_quotes:
            print(f"\n📜 古典智慧引用:")
            for quote in result.ancient_wisdom_quotes[:2]:
                print(f"   「{quote[:60]}...」")

        print(f"\n七维度分析:")
        for dim in result.dimensions[:4]:
            print(f"   [{dim.name}] 得分:{dim.score:.2f} | {dim.insights[0][:50] if dim.insights else 'N/A'}...")

        print("-" * 70)

    print("\n\n" + "=" * 70)
    print("✅ 统一默认调用体验完成")
    print("=" * 70)
    print("\n调用方式:")
    print("  from intelligence.super_wisdom_coordinator import SuperWisdomCoordinator")
    print("  coordinator = SuperWisdomCoordinator()")
    print("  result = coordinator.analyze('你的问题')")

if __name__ == "__main__":
    demo_super_wisdom()
