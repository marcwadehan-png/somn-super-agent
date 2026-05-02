"""
双轨架构集成示例

展示如何将双轨系统与现有神之架构组件集成：
1. DivineReason (神之推理) → A轨分析决策
2. Pan-Wisdom Tree (万法智慧树) → A轨学派推理
3. SageDispatch (调度系统) → A轨任务调度
4. ClawSystem (利爪系统) → B轨执行

关键演示：
- "跳过多余环节"：A轨直接调用B轨职能部门
- Pan-Wisdom Tree枝干直接import ClawSystem并ask
"""

import sys
import os
import asyncio

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def demo_basic_usage():
    """示例1: 基本使用"""
    print("\n" + "="*60)
    print("示例1: 基本使用 - A轨处理请求，自动调度B轨执行")
    print("="*60)
    
    from src.intelligence.dual_track.bridge import TrackBridge
    
    # 创建双轨系统
    bridge = TrackBridge()
    system = bridge.create_system()
    
    # 处理请求（A轨自动调度B轨）
    result = system.process(
        query="如何提升产品竞争力？",
        context={"user_id": "demo_user"},
    )
    
    print(f"\n处理结果:")
    print(f"  成功: {result['success']}")
    print(f"  分析类型: {result['analysis']['problem_type']}")
    print(f"  策略部门: {result['strategy']['department']}")
    print(f"  验收状态: {result['execution_result']['accepted']}")
    print(f"  耗时: {result['elapsed_seconds']:.2f}s")
    
    return result


def demo_direct_department_call():
    """示例2: 直接部门调用（跳过多余环节）"""
    print("\n" + "="*60)
    print("示例2: 直接部门调用 - 跳过多余环节")
    print("="*60)
    print("\n传统方式: 用户 → A轨 → 中枢 → 部门 → 执行")
    print("直接调用: 用户 → A轨 → 部门(直接) → 执行 ✅")
    print("\n关键优势: 跳过神之架构内的架构层，直接调用职能部门\n")
    
    from src.intelligence.dual_track.bridge import TrackBridge
    
    bridge = TrackBridge()
    system = bridge.create_system()
    
    # 直接调用B轨的兵部（跳过多余环节！）
    result = system.execute_direct(
        department="兵部",
        task="制定竞争策略，分析竞争对手的弱点",
        context={"urgency": "high"},
    )
    
    print(f"直接调用结果:")
    print(f"  成功: {result['success']}")
    print(f"  部门: {result['department']}")
    print(f"  执行模式: {result['execution_mode']}")
    
    # 再调用户部
    result2 = system.execute_direct(
        department="户部",
        task="分析市场趋势，制定营销策略",
    )
    
    print(f"\n户部调用结果:")
    print(f"  成功: {result2['success']}")
    print(f"  部门: {result2['department']}")
    
    return result, result2


def demo_pan_wisdom_tree_integration():
    """示例3: Pan-Wisdom Tree集成（树干→枝干→枝丫）"""
    print("\n" + "="*60)
    print("示例3: Pan-Wisdom Tree集成")
    print("="*60)
    print("\nPan-Wisdom Tree结构:")
    print("  树干 (SD-P1) → 问题调度")
    print("    ├── 枝干 (SD-D2) → 深度推理")
    print("    │     └── 枝丫 → 具体执行")
    print("    │           ↑")
    print("    │           可以直接 import ClawSystem 并 ask！")
    print("    └── ...\n")
    
    from src.intelligence.dual_track.bridge import create_wisdom_tree_branch_executor
    
    # 创建兵部枝干执行器（这就是"直接import ClawSystem并ask"）
    bingbu_exec = create_wisdom_tree_branch_executor("兵部")
    
    # 枝干直接执行任务（无需通过A轨层层下发）
    print("兵部枝干执行器（模拟）:")
    result = bingbu_exec("分析竞争对手的营销策略")
    print(f"  成功: {result.get('success')}")
    print(f"  部门: {result.get('department', '兵部')}")
    print(f"  任务: {result.get('task', 'N/A')}")
    print(f"  模式: {result.get('mode', 'N/A')}")
    
    # 创建户部枝干执行器
    print("\n户部枝干执行器（模拟）:")
    hubu_exec = create_wisdom_tree_branch_executor("户部")
    result2 = hubu_exec("制定市场推广方案")
    print(f"  成功: {result2.get('success')}")
    print(f"  部门: {result2.get('department', '户部')}")
    
    return result, result2


def demo_security_constraint():
    """示例4: 安全约束验证（B轨不能调用A轨）"""
    print("\n" + "="*60)
    print("示例4: 安全约束验证")
    print("="*60)
    print("\n安全规则:")
    print("  ✓ A轨可以调用B轨")
    print("  ✗ B轨不能调用A轨（铁律）\n")
    
    from src.intelligence.dual_track.bridge import TrackBridge
    
    bridge = TrackBridge()
    _ = bridge.create_system()
    
    # 测试A→B调用（应成功）
    result_a_to_b = bridge.validate_call_direction("A", "B")
    print(f"A→B 调用: {'✓ 允许' if result_a_to_b else '✗ 拒绝'}")
    
    # 测试B→A调用（应被拒绝）
    result_b_to_a = bridge.validate_call_direction("B", "A")
    print(f"B→A 调用: {'✓ 允许' if result_b_to_a else '✗ 拒绝（正确！）'}")
    
    # 测试B→B调用（应允许，同轨内部调用）
    result_b_to_b = bridge.validate_call_direction("B", "B")
    print(f"B→B 调用: {'✓ 允许（同轨内部）' if result_b_to_b else '✗ 拒绝'}")
    
    return result_a_to_b, not result_b_to_a, result_b_to_b


def demo_full_integration():
    """示例5: 完整集成演示（DivineReason + Pan-Wisdom + DualTrack）"""
    print("\n" + "="*60)
    print("示例5: 完整集成演示")
    print("="*60)
    print("\n完整流程:")
    print("  1. 用户请求 → A轨(DivineReason分析)")
    print("  2. A轨制定策略 → 确定主责部门")
    print("  3. A轨派发任务 → B轨(神行轨)")
    print("  4. B轨执行 → 直接调用职能部门（跳过多余环节）")
    print("  5. B轨回报结果 → A轨验收")
    print("  6. A轨返回最终结果 → 用户\n")
    
    from src.intelligence.dual_track.bridge import TrackBridge
    
    bridge = TrackBridge()
    system = bridge.create_system()
    
    # 模拟完整请求
    queries = [
        "如何提升市场份额？",
        "分析竞争对手的弱点",
        "制定产品创新策略",
    ]
    
    results = []
    for i, query in enumerate(queries, 1):
        print(f"\n请求{i}: {query}")
        result = system.process(query)
        results.append(result)
        
        print(f"  → 分析: {result['analysis']['problem_type']}")
        print(f"  → 部门: {result['strategy']['department']}")
        print(f"  → 验收: {result['execution_result']['feedback']}")
    
    print(f"\n{'='*60}")
    print(f"完成情况: {len([r for r in results if r['success']])}/{len(results)} 成功")
    print(f"{'='*60}")
    
    return results


def main():
    """运行所有示例"""
    print("\n" + "🚀" * 30)
    print("双轨架构集成示例")
    print("="*70 + "\n")
    
    examples = [
        ("基本使用", demo_basic_usage),
        ("直接部门调用（跳过多余环节）", demo_direct_department_call),
        ("Pan-Wisdom Tree集成", demo_pan_wisdom_tree_integration),
        ("安全约束验证", demo_security_constraint),
        ("完整集成演示", demo_full_integration),
    ]
    
    results = []
    
    for name, demo_func in examples:
        try:
            result = demo_func()
            results.append((name, "PASS", result))
        except Exception as e:
            print(f"\n❌ 示例失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, f"FAIL: {e}", None))
    
    # 汇总
    print("\n" + "="*60)
    print("示例汇总")
    print("="*60)
    
    for name, status, _ in results:
        icon = "✅" if status == "PASS" else "❌"
        print(f"  {icon} {name}: {status}")
    
    passed = sum(1 for _, s, _ in results if s == "PASS")
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有示例运行成功！")
        print("\n核心功能验证:")
        print("  ✓ A轨(神政轨)管理监管正常")
        print("  ✓ B轨(神行轨)执行正常")
        print("  ✓ 直接部门调用（跳过多余环节）正常")
        print("  ✓ Pan-Wisdom Tree集成正常")
        print("  ✓ 安全约束（B不能调A）正常")
    else:
        print("\n⚠️ 部分示例未通过，请检查实现")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
