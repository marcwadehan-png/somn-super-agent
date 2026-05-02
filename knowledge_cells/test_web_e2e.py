#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端 web 集成测试
"""

import sys
sys.path.insert(0, 'd:/AI/somn')
sys.path.insert(0, 'd:/AI/somn/knowledge_cells')

print("=" * 70)
print("Somn Web 集成系统 - 端到端测试")
print("=" * 70)

# 1. 测试 divine_oversight.refute_web
print("\n[1] 测试 DivineTrackOversight.refute_web")
print("-" * 70)
from divine_oversight import get_oversight

oversight = get_oversight()
print(f"  get_oversight() 返回: {type(oversight).__name__}")
print(f"  refute_web 属性存在: {hasattr(oversight, 'refute_web')}")

if hasattr(oversight, 'refute_web'):
    rw = oversight.refute_web
    print(f"  refute_web 值: {rw}")
    if rw:
        print(f"  refute_web.is_enabled(): {rw.is_enabled()}")

        # 测试搜索证据功能
        print("\n  测试 verify_with_evidence():")
        evidence = oversight.verify_with_evidence(
            claim="人工智能将改变教育行业",
            context="教育科技",
            max_results=2
        )
        print(f"    claim: {evidence.get('claim')}")
        print(f"    supporting_evidence count: {len(evidence.get('supporting_evidence', []))}")
        print(f"    counter_evidence count: {len(evidence.get('counter_evidence', []))}")
        print(f"    web_available: {evidence.get('web_available')}")
    else:
        print("  [WARN] refute_web 为 None")

# 2. 测试 RefuteCoreWeb 直接使用
print("\n[2] 测试 RefuteCoreWeb 直接使用")
print("-" * 70)
from web_integration import RefuteCoreWeb

rcw = RefuteCoreWeb()
print(f"  RefuteCoreWeb() 实例化成功")
print(f"  is_enabled(): {rcw.is_enabled()}")

print("\n  测试 search_supporting_evidence():")
support = rcw.search_supporting_evidence("AI教育", max_results=2)
print(f"    success: {support.get('success')}")
print(f"    results count: {len(support.get('results', []))}")

print("\n  测试 search_counter_evidence():")
counter = rcw.search_counter_evidence("AI教育", max_results=2)
print(f"    success: {counter.get('success')}")
print(f"    results count: {len(counter.get('results', []))}")

# 3. 测试 NeuralMemoryWeb
print("\n[3] 测试 NeuralMemoryWeb")
print("-" * 70)
from web_integration import NeuralMemoryWeb

nm_web = NeuralMemoryWeb()
print(f"  NeuralMemoryWeb() 实例化成功")
print(f"  is_enabled(): {nm_web.is_enabled()}")

print("\n  测试 search_for_memory():")
result = nm_web.search_for_memory(
    content="2025年人工智能发展趋势分析",
    tags=["AI", "趋势"],
    max_results=2
)
print(f"    success: {result.get('success')}")
print(f"    source: {result.get('source')}")
print(f"    results count: {len(result.get('results', []))}")

# 4. 测试 TianShuWeb
print("\n[4] 测试 TianShuWeb")
print("-" * 70)
from web_integration import TianShuWeb

ts_web = TianShuWeb()
print(f"  TianShuWeb() 实例化成功")
print(f"  is_enabled(): {ts_web.is_enabled()}")

print("\n  测试 enhance_nlp_analysis():")
result = ts_web.enhance_nlp_analysis(
    "分析2025年AI在金融领域的最新应用",
    layer_context="测试"
)
print(f"    success: {result.get('success')}")
print(f"    source: {result.get('source')}")
print(f"    terms count: {len(result.get('terms', []))}")

# 5. 测试 search_with_fallback
print("\n[5] 测试 search_with_fallback")
print("-" * 70)
from web_integration import search_with_fallback

result = search_with_fallback("人工智能最新发展", max_results=3)
print(f"  success: {result.get('success')}")
print(f"  source: {result.get('source')}")
print(f"  online: {result.get('online')}")
print(f"  results count: {len(result.get('results', []))}")

if result.get('results'):
    print("\n  搜索结果:")
    for i, r in enumerate(result['results'][:3]):
        print(f"    [{i+1}] {r.get('title', 'N/A')[:50]}...")
        print(f"        来源: {r.get('source', 'N/A')}")
        print(f"        snippet: {r.get('snippet', 'N/A')[:50]}...")

# 6. 测试 should_trigger_web_search
print("\n[6] 测试 should_trigger_web_search 触发检测")
print("-" * 70)
from web_integration import should_trigger_web_search

test_cases = [
    ("2025年AI发展趋势", True, "应触发"),
    ("如何提升用户留存", False, "不应触发"),
    ("最新新闻报道", True, "应触发"),
    ("分析市场竞争策略", False, "不应触发"),
    ("现在比特币价格", True, "应触发（现在）"),
    ("今日股市行情", True, "应触发（今日）"),
]

all_passed = True
for text, expected, desc in test_cases:
    should, keyword = should_trigger_web_search(text)
    status = "PASS" if should == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"  [{status}] '{text}' -> 触发:{should}, 关键词:'{keyword}' ({desc})")

print("\n" + "=" * 70)
if all_passed:
    print("✅ 所有测试通过！")
else:
    print("⚠️ 部分测试失败")
print("=" * 70)
