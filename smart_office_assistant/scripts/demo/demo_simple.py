"""v8.1.0 超级智慧协调器 - 快速体验"""
import warnings

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

warnings.filterwarnings('ignore')

from intelligence.super_wisdom_coordinator import SuperWisdomCoordinator, OutputStyle


print('=' * 70)
print('v8.1.0 超级智慧协调器 - 实际调用体验')
print('=' * 70)

coordinator = SuperWisdomCoordinator()

query = '公司在快速扩张期，核心员工纷纷离职，如何留住人才同时保持创新活力？'
print(f'\n>>> 用户问题: {query}')
print('-' * 70)

result = coordinator.analyze(
    query_text=query,
    context='企业人才管理',
    output_style=OutputStyle.COMPREHENSIVE
)

print(f'\n📊 分析概览:')
print(f'   置信度: {result.confidence:.1%}')
print(f'   激活学派: {result.schools_contributed}个')
print(f'   处理层级: {", ".join(result.layers_processed)}')
print(f'   综合评分: {result.overall_score:.2f}')

print(f'\n💡 主洞察:')
print(f'   {result.primary_insight}')

print(f'\n🔍 次级洞察:')
for i, ins in enumerate(result.secondary_insights[:3], 1):
    print(f'   {i}. {ins}')

print(f'\n⚡ 行动建议:')
for rec in result.action_recommendations[:3]:
    print(f'   • {rec}')

print(f'\n📜 古智引用:')
for q in result.ancient_wisdom_quotes[:2]:
    print(f'   「{q}」')

print(f'\n七维度分析:')
for dim in result.dimensions[:4]:
    insights = dim.insights[0] if dim.insights else 'N/A'
    print(f'   [{dim.name}] 得分:{dim.score:.2f}')
    print(f'      {insights[:70]}...' if len(insights) > 70 else f'      {insights}')

print('\n' + '=' * 70)
print('✅ 体验完成')
