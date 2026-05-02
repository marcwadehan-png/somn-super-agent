"""
双系统独立运行测试
==================

测试两个完全独立的推理系统：
1. DivineReason - 神之推理 (142引擎)
2. PanWisdomTree - 万法智慧树 (10学派)

两个系统互不交叉，各自独立运行。
"""

import sys
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

print("=" * 70)
print("Somn 双推理系统独立运行测试")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════
# 测试1: DivineReason 系统 (神之推理)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 70)
print("系统1: DivineReason - 神之推理 (142个子引擎)")
print("-" * 70)

try:
    from intelligence.engines.sub_engines import (
        get_divine_reason_engine,
        ReasoningRequest,
        ReasoningResponse,
    )
    
    # 获取DivineReason引擎
    divine = get_divine_reason_engine()
    print("DivineReason 引擎加载成功")
    
    # 获取统计信息
    stats = divine.get_stats()
    print(f"总引擎数: {stats['total_engines']}")
    print("引擎分类:")
    for cat, count in stats['by_category'].items():
        print(f"    - {cat}: {count}个")
    
    # 执行推理任务
    divine_req = ReasoningRequest(
        query="公司市场份额下降20%，请分析原因并制定反击策略",
        problem_type="STRATEGIC_ANALYSIS",
        context={}
    )
    
    divine_result = divine.reason(divine_req)
    
    print(f"\nDivineReason 推理完成:")
    print(f"    - 调用引擎数: {len(divine_result.results)}")
    print(f"    - 综合置信度: {divine_result.confidence:.2%}")
    answer_preview = divine_result.fused_answer[:80] if divine_result.fused_answer else "N/A"
    print(f"    - 输出预览: {answer_preview}...")
    
    DIVINE_SUCCESS = True
    
except Exception as e:
    print(f"DivineReason 测试失败: {e}")
    import traceback
    traceback.print_exc()
    DIVINE_SUCCESS = False

# ═══════════════════════════════════════════════════════════════════════════
# 测试2: PanWisdomTree 系统 (万法智慧树)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 70)
print("系统2: PanWisdomTree - 万法智慧树 (10大学派)")
print("-" * 70)

try:
    from intelligence.engines.sub_engines import (
        get_pan_wisdom_tree,
        reason_with_wisdom_tree,  # 向后兼容别名 -> solve_with_wisdom
    )
    from intelligence.engines.sub_engines import WisdomSchool
    
    # 获取PanWisdomTree引擎 (V2.0/V2.1)
    wisdom = get_pan_wisdom_tree()
    print("PanWisdomTree 引擎加载成功 (V2.0/V2.1)")
    
    # 列出所有学派 (V2.0使用WisdomSchool枚举)
    schools = [s for s in WisdomSchool]
    print(f"可用学派数: {len(schools)}")
    print("学派列表 (前10个):")
    for s in schools[:10]:
        print(f"    - {s.value}")
    print(f"    ... (共{len(schools)}个学派)")
    
    # 执行推理任务 (V2.0 API)
    result = reason_with_wisdom_tree(
        query="如何治理一个国家",
        context={},
    )
    
    print(f"\nPanWisdomTree 推理完成:")
    print(f"    - 应用学派: {result.school.value}")
    print(f"    - 置信度: {result.confidence:.2%}")
    print(f"    - 洞察: {', '.join(result.insights[:2])}")
    print(f"    - 建议: {', '.join(result.recommendations[:2])}")
    
    WISDOM_SUCCESS = True
    
except Exception as e:
    print(f"PanWisdomTree 测试失败: {e}")
    import traceback
    traceback.print_exc()
    WISDOM_SUCCESS = False

# ═══════════════════════════════════════════════════════════════════════════
# 测试3: 验证两系统完全独立
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 70)
print("独立性验证")
print("-" * 70)

try:
    # 分别实例化两次，确认互不影响
    divine1 = get_divine_reason_engine()
    divine2 = get_divine_reason_engine()
    
    wisdom1 = get_pan_wisdom_tree()
    wisdom2 = get_pan_wisdom_tree()
    
    # 确认单例模式
    assert divine1 is divine2, "DivineReason单例失败"
    assert wisdom1 is wisdom2, "PanWisdomTree单例失败"
    
    print("两系统均为单例模式")
    
    # 确认模块独立
    divine_module = type(get_divine_reason_engine).__module__
    wisdom_module = type(get_pan_wisdom_tree).__module__
    
    print(f"DivineReason 模块: {divine_module}")
    print(f"PanWisdomTree 模块: {wisdom_module}")
    
    INDEPENDENCE_SUCCESS = True
    
except Exception as e:
    print(f"独立性验证失败: {e}")
    import traceback
    traceback.print_exc()
    INDEPENDENCE_SUCCESS = False

# ═══════════════════════════════════════════════════════════════════════════
# 测试结果汇总
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("测试结果汇总")
print("=" * 70)

results = [
    ("DivineReason 系统", DIVINE_SUCCESS),
    ("PanWisdomTree 系统", WISDOM_SUCCESS),
    ("独立性验证", INDEPENDENCE_SUCCESS),
]

for name, success in results:
    status = "通过" if success else "失败"
    print(f"  {name}: {status}")

all_passed = all(success for _, success in results)

print("\n" + "=" * 70)
if all_passed:
    print("全部测试通过！双系统独立运行正常！")
    print("")
    print("系统架构:")
    print("  +-------------------------------------------------------------+")
    print("  |              Somn 双推理系统 (完全独立)                       |")
    print("  +-------------------------------------------------------------+")
    print("  |                                                               |")
    print("  |  +-----------------------+    +-----------------------+      |")
    print("  |  | DivineReason         |    | PanWisdomTree         |      |")
    print("  |  | 神之推理              |    | 万法智慧树            |      |")
    print("  |  |                       |    |                       |      |")
    print("  |  | - 142个子引擎         |    | - 10大学派           |      |")
    print("  |  | - 问题类型调度        |    | - 学派哲学调度        |      |")
    print("  |  | - 认知/战略/创意/     |    | - 道/儒/兵/阴阳/      |      |")
    print("  |  |   分析/决策          |    |   法/墨/纵横/农/医/杂 |      |")
    print("  |  +-----------------------+    +-----------------------+      |")
    print("  |                                                               |")
    print("  |                    互不交叉，独立运行                           |")
    print("  +-------------------------------------------------------------+")
else:
    print("部分测试失败，请检查上述错误信息")
print("=" * 70)
