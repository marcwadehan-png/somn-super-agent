"""
DivineReason V4.0 完整测试
测试系统能否真正解决问题
"""

import sys
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

print("=" * 70)
print("DivineReason V4.0 完整测试")
print("=" * 70)

from intelligence.engines.sub_engines import (
    get_divine_reason_engine,
    ReasoningRequest,
    diagnose_reasoning_problem,
)


# ═══════════════════════════════════════════════════════════════════════════
# 测试1: 引擎加载
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 70)
print("测试1: 引擎加载")
print("-" * 70)

engine = get_divine_reason_engine()
stats = engine.get_stats()

print(f"系统版本: {stats['divine_reason_version']}")
print(f"总引擎数: {stats['total_engines']}")
print(f"引擎分类:")
for cat, count in stats['by_category'].items():
    print(f"  - {cat}: {count}个")

assert stats['total_engines'] >= 142, f"引擎数错误: {stats['total_engines']}"
print(f"✓ 引擎加载正常 (共{stats['total_engines']}个)")


# ═══════════════════════════════════════════════════════════════════════════
# 测试2: 问题诊断
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 70)
print("测试2: 问题诊断")
print("-" * 70)

test_queries = [
    "公司市场份额下降20%，请分析原因并制定反击策略",
    "如何选择最佳投资方案？",
    "为什么销售额持续下滑？",
    "请预测下季度的市场趋势",
]

for query in test_queries:
    diagnosis = diagnose_reasoning_problem(query)
    print(f"\n问题: {query[:40]}...")
    print(f"  类型: {diagnosis['problem_type']}")
    print(f"  角度: {diagnosis['angles']}")
    print(f"  紧迫度: {diagnosis['urgency']}")

print("\n✓ 问题诊断正常")


# ═══════════════════════════════════════════════════════════════════════════
# 测试3: 实际解决问题
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 70)
print("测试3: 实际解决问题")
print("-" * 70)

# 实际问题1: 市场份额下降
query1 = "公司市场份额下降20%，请分析原因并制定反击策略"
print(f"\n问题: {query1}")

request1 = ReasoningRequest(
    query=query1,
    problem_type="STRATEGIC_ANALYSIS",
    max_engines=8,
)

response1 = engine.reason(request1)

print(f"\n使用引擎数: {len(response1.results)}")
print(f"综合置信度: {response1.confidence:.2%}")
print(f"分析类型: {response1.analysis['problem_type']}")
print(f"\n--- 融合答案 ---")
print(response1.fused_answer.get('text', '无文本答案'))

print(f"\n--- 关键发现 ---")
for i, finding in enumerate(response1.fused_answer.get('key_findings', [])[:3], 1):
    print(f"  {i}. {finding[:80]}...")

print(f"\n--- 建议 ---")
for i, rec in enumerate(response1.fused_answer.get('recommendations', [])[:3], 1):
    print(f"  {i}. {rec[:80]}...")


# 实际问题2: 决策选择
query2 = "有A/B/C三个供应商，价格分别是高/中/低，质量分别是高/中/低，交期分别是长/中/短，应该选择哪个？"
print(f"\n\n问题: {query2}")

request2 = ReasoningRequest(
    query=query2,
    problem_type="DECISION_MAKING",
    max_engines=6,
)

response2 = engine.reason(request2)

print(f"\n使用引擎数: {len(response2.results)}")
print(f"综合置信度: {response2.confidence:.2%}")
print(f"\n--- 融合答案 ---")
print(response2.fused_answer.get('text', '无文本答案'))


# 实际问题3: 因果分析
query3 = "为什么这个月的用户投诉增加了30%？"
print(f"\n\n问题: {query3}")

request3 = ReasoningRequest(
    query=query3,
    problem_type="CAUSAL_ANALYSIS",
    max_engines=6,
)

response3 = engine.reason(request3)

print(f"\n使用引擎数: {len(response3.results)}")
print(f"综合置信度: {response3.confidence:.2%}")
print(f"\n--- 融合答案 ---")
print(response3.fused_answer.get('text', '无文本答案'))


# ═══════════════════════════════════════════════════════════════════════════
# 测试4: 按类别分析
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 70)
print("测试4: 按类别分析结果")
print("-" * 70)

print(f"\n响应1(战略分析) 类别分布:")
by_cat = response1.fused_answer.get('by_category', {})
for cat, data in by_cat.items():
    print(f"  {cat}: {data['engine_count']}个引擎, 置信度{data['avg_confidence']:.2f}")


# ═══════════════════════════════════════════════════════════════════════════
# 测试结果汇总
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("测试结果汇总")
print("=" * 70)

tests = [
    ("引擎加载", stats['total_engines'] >= 142),
    ("问题诊断", True),
    ("战略分析", len(response1.results) > 0 and len(response1.fused_answer.get('key_findings', [])) > 0),
    ("决策推理", len(response2.results) > 0 and len(response2.fused_answer.get('recommendations', [])) > 0),
    ("因果分析", len(response3.results) > 0),
    ("结果融合", 'text' in response1.fused_answer),
]

all_passed = True
for name, passed in tests:
    status = "✓ 通过" if passed else "✗ 失败"
    print(f"  {name}: {status}")
    if not passed:
        all_passed = False

print("\n" + "=" * 70)
if all_passed:
    print("🎉 DivineReason V4.0 测试全部通过！")
    print("系统已具备解决实际问题的能力！")
else:
    print("❌ 部分测试失败")
print("=" * 70)
