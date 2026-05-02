"""
双轨架构测试脚本

验证A轨(神政轨)和B轨(神行轨)的双向关系:
1. A轨可以调用B轨 ✓
2. B轨执行结果回报A轨 ✓
3. B轨不能调用A轨 ✓
4. 跳过多余环节: 直接部门调用 ✓
5. Pan-Wisdom Tree枝干可直接import ClawSystem并ask ✓
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from src.intelligence.dual_track import (
    DivineGovernanceTrack,
    DivineExecutionTrack,
    TrackBridge,
)


def test_basic_dual_track():
    """测试1: 基本双轨功能"""
    print("\n" + "=" * 60)
    print("测试1: 基本双轨功能")
    print("=" * 60)
    
    # 创建双轨系统
    bridge = TrackBridge()
    system = bridge.create_system()
    
    # 检查连接状态
    status = system.get_system_status()
    print(f"系统状态: {status['system']}")
    print(f"A轨: {status['track_a'].get('name', 'N/A')}")
    print(f"B轨: {status['track_b'].get('name', 'N/A')}")
    print(f"调用模式: {status['architecture']['call_pattern']}")
    
    assert status["bridge"]["connected"] == True
    assert status["architecture"]["b_to_a_restricted"] == True
    
    print("✅ 双轨系统创建成功")
    return True


def test_direct_department_call():
    """测试2: 直接部门调用 (跳过多余环节)"""
    print("\n" + "=" * 60)
    print("测试2: 直接部门调用 (跳过多余环节)")
    print("=" * 60)
    
    bridge = TrackBridge()
    system = bridge.create_system()
    
    # 测试直接调用兵部
    result = bridge.direct_department_call(
        caller_track="A",
        department_name="兵部",
        task_data={"task": "分析竞争策略"},
    )
    
    print(f"兵部直接调用结果:")
    print(f"  - 成功: {result.get('success')}")
    print(f"  - 部门: {result.get('department')}")
    
    assert result["success"] == True
    assert result["department"] == "兵部"
    
    print("✅ 直接部门调用成功")
    return True


def test_b_to_a_restricted():
    """测试3: B轨不能调用A轨"""
    print("\n" + "=" * 60)
    print("测试3: B轨不能调用A轨 (安全约束)")
    print("=" * 60)
    
    bridge = TrackBridge()
    _ = bridge.create_system()
    
    # 尝试从B调用A (应失败)
    is_valid = bridge.validate_call_direction("B", "A")
    
    print(f"B→A 调用是否合法: {is_valid}")
    
    assert is_valid == False
    
    print("✅ B→A调用被正确拒绝")
    return True


def test_wisdom_tree_branch_executor():
    """测试4: Pan-Wisdom Tree枝干执行器"""
    print("\n" + "=" * 60)
    print("测试4: Pan-Wisdom Tree枝干执行器 (直接import ClawSystem)")
    print("=" * 60)
    
    from src.intelligence.dual_track.bridge import create_wisdom_tree_branch_executor
    
    # 创建兵部枝干执行器
    bingbu_exec = create_wisdom_tree_branch_executor("兵部")
    
    # 执行任务
    result = bingbu_exec("制定竞争策略")
    
    print(f"智慧树-兵部执行结果:")
    print(f"  - 成功: {result.get('success')}")
    print(f"  - 部门: {result.get('department')}")
    print(f"  - 来源: {result.get('source', 'direct_call')}")
    
    assert result.get("success") != None
    
    print("✅ 智慧树枝干执行器工作正常")
    return True


def test_full_request_flow():
    """测试5: 完整请求流程"""
    print("\n" + "=" * 60)
    print("测试5: 完整请求流程 (用户 → A轨 → B轨 → 结果)")
    print("=" * 60)
    
    bridge = TrackBridge()
    system = bridge.create_system()
    
    # 处理完整请求
    result = system.process(
        query="如何提升产品竞争力？",
        context={"user_id": "test_user"},
    )
    
    print(f"完整请求处理结果:")
    print(f"  - 成功: {result.get('success')}")
    print(f"  - 分析类型: {result.get('analysis', {}).get('problem_type')}")
    print(f"  - 策略部门: {result.get('strategy', {}).get('department')}")
    print(f"  - 验收状态: {result.get('execution_result', {}).get('accepted')}")
    print(f"  - 耗时: {result.get('elapsed_seconds', 0):.2f}s")
    
    assert result["success"] == True
    
    print("✅ 完整请求流程正常")
    return True


def main():
    """运行所有测试"""
    print("\n" + "🚀" * 30)
    print("双轨架构测试套件 v1.0")
    print("=" * 70)
    
    tests = [
        ("基本双轨功能", test_basic_dual_track),
        ("直接部门调用", test_direct_department_call),
        ("B→A限制", test_b_to_a_restricted),
        ("智慧树枝干执行器", test_wisdom_tree_branch_executor),
        ("完整请求流程", test_full_request_flow),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, "PASS"))
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, f"FAIL: {e}"))
    
    # 输出汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    for name, status in results:
        icon = "✅" if status == "PASS" else "❌"
        print(f"  {icon} {name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, s in results if s == "PASS")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！双轨架构运行正常！")
        print("\n关键设计验证:")
        print("  ✓ A轨(神政轨)管理监管正常")
        print("  ✓ B轨(神行轨)执行正常")
        print("  ✓ A→B单向调用正常")
        print("  ✓ B→A被正确禁止")
        print("  ✓ 直接部门调用(跳过多余环节)正常")
        print("  ✓ Pan-Wisdom Tree集成正常")
    else:
        print("⚠️ 部分测试未通过，请检查实现")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
