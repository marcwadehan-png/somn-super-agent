#!/usr/bin/env python
"""
双轨架构简单测试
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def test_imports():
    """测试1: 导入模块"""
    print("测试1: 导入模块...")
    try:
        from src.intelligence.dual_track.track_a import DivineGovernanceTrack
        from src.intelligence.dual_track.track_b import DivineExecutionTrack
        from src.intelligence.dual_track.bridge import TrackBridge
        print("  ✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"  ✗ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_system():
    """测试2: 创建双轨系统"""
    print("\n测试2: 创建双轨系统...")
    try:
        from src.intelligence.dual_track.bridge import TrackBridge
        
        bridge = TrackBridge()
        system = bridge.create_system()
        
        print(f"  ✓ 双轨系统创建成功")
        print(f"  - A轨: {system.track_a is not None}")
        print(f"  - B轨: {system.track_b is not None}")
        return True
    except Exception as e:
        print(f"  ✗ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_a_to_b_call():
    """测试3: A轨调用B轨"""
    print("\n测试3: A轨调用B轨...")
    try:
        from src.intelligence.dual_track.bridge import TrackBridge
        
        bridge = TrackBridge()
        system = bridge.create_system()
        
        # A轨处理请求
        result = system.track_a.process_request(
            query="测试请求",
            context={"test": True},
        )
        
        print(f"  ✓ A轨调用B轨成功")
        print(f"  - 成功: {result.get('success')}")
        return True
    except Exception as e:
        print(f"  ✗ 调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_direct_department_call():
    """测试4: 直接部门调用 (跳过多余环节)"""
    print("\n测试4: 直接部门调用...")
    try:
        from src.intelligence.dual_track.bridge import TrackBridge
        
        bridge = TrackBridge()
        _ = bridge.create_system()
        
        # 直接调用B轨的兵部
        result = bridge.direct_department_call(
            caller_track="A",
            department_name="兵部",
            task_data={"task": "分析竞争"},
        )
        
        print(f"  ✓ 直接部门调用成功")
        print(f"  - 部门: {result.get('department')}")
        print(f"  - 成功: {result.get('success')}")
        return True
    except Exception as e:
        print(f"  ✗ 直接调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_b_cannot_call_a():
    """测试5: B轨不能调用A轨"""
    print("\n测试5: B轨不能调用A轨...")
    try:
        from src.intelligence.dual_track.bridge import TrackBridge
        
        bridge = TrackBridge()
        _ = bridge.create_system()
        
        # 验证B→A调用应被拒绝
        is_valid = bridge.validate_call_direction("B", "A")
        
        if not is_valid:
            print("  ✓ B轨调用A轨被正确拒绝")
            return True
        else:
            print("  ✗ B轨调用A轨未被拒绝 (错误！)")
            return False
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("双轨架构简单测试")
    print("=" * 60)
    
    tests = [
        ("导入模块", test_imports),
        ("创建双轨系统", test_create_system),
        ("A轨调用B轨", test_a_to_b_call),
        ("直接部门调用", test_direct_department_call),
        ("B轨不能调用A轨", test_b_cannot_call_a),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, "PASS" if passed else "FAIL"))
        except Exception as e:
            print(f"  ✗ 测试异常: {e}")
            results.append((name, f"ERROR: {e}"))
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    for name, status in results:
        icon = "✓" if status == "PASS" else "✗"
        print(f"  {icon} {name}: {status}")
    
    passed = sum(1 for _, s in results if s == "PASS")
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
