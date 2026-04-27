import sys
sys.path.insert(0, '.')
from src.neural_memory.neural_system import create_neural_system

ns = create_neural_system()
report = ns.generate_system_report()
health = report.get('系统健康度', {})
knowledge = report.get('知识系统', {})

print('=== 修复后系统健康度 ===')
keys = ['记忆完整性', '知识覆盖率', '推理能力', '学习活跃度', '总体评分']
for k in keys:
    v = health.get(k, 0)
    print(f'{k}: {v:.2f}')
print()
print('=== 知识系统统计 ===')
stats = knowledge.get('总体统计', {})
print('概念总数:', stats.get('概念总数', 0))
print('规则总数:', stats.get('规则总数', 0))
print('关系总数:', stats.get('关系总数', 0))
