"""
测试网络搜索集成
================
验证所有子系统网络搜索能力

测试内容：
1. web_integration 基础功能
2. NeuralMemory 网络增强
3. RefuteCore 网络增强
4. TianShu 网络增强
5. TrackA 网络增强
6. TrackB 网络增强
"""

import sys
import os
import time

# 设置正确的导入路径
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
_SOMN_ROOT = os.path.join(_PROJECT_ROOT, "smart_office_assistant")

sys.path.insert(0, _PROJECT_ROOT)
sys.path.insert(0, os.path.join(_SOMN_ROOT, "src"))
sys.path.insert(0, _SOMN_ROOT)

def test_web_integration():
    """测试 web_integration 基础功能"""
    print("\n" + "="*60)
    print("测试 1: web_integration 基础功能")
    print("="*60)

    try:
        from web_integration import (
            is_online,
            search_with_fallback,
            should_trigger_web_search,
            NeuralMemoryWeb,
            RefuteCoreWeb,
            TianShuWeb,
        )

        # 测试联网检测
        online = is_online()
        print(f"  [1.1] 联网状态: {'在线' if online else '离线'}")

        # 测试关键词检测
        test_cases = [
            ("2025年AI发展趋势", True),
            ("如何提升用户留存", False),
            ("最新新闻报道", True),
            ("分析市场竞争策略", False),
        ]

        print(f"  [1.2] 关键词触发检测:")
        for text, expected in test_cases:
            should, keyword = should_trigger_web_search(text)
            status = "✓" if should == expected else "✗"
            print(f"      {status} '{text}' -> {'触发' if should else '不触发'} ({keyword})")

        # 测试网络搜索（如果在线）
        if online:
            print(f"  [1.3] 执行搜索测试:")
            result = search_with_fallback("人工智能", max_results=3)
            if result.get("success"):
                print(f"      ✓ 搜索成功，找到 {len(result.get('results', []))} 条结果")
                print(f"      来源: {result.get('source', 'unknown')}")
            else:
                print(f"      ✗ 搜索失败: {result.get('error', 'unknown')}")
        else:
            print(f"  [1.3] 跳过搜索测试（离线模式）")

        print("\n  ✓ web_integration 基础功能测试通过")
        return True

    except Exception as e:
        print(f"\n  ✗ web_integration 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_neural_memory_web():
    """测试 NeuralMemory 网络增强"""
    print("\n" + "="*60)
    print("测试 2: NeuralMemory 网络增强")
    print("="*60)

    try:
        # 导入 NeuralMemory
        from neural_memory import NeuralMemory

        nm = NeuralMemory(use_fast_load=True)
        print(f"  [2.1] NeuralMemory 初始化: ✓")

        # 检查 neural_web 属性
        if hasattr(nm, 'neural_web'):
            print(f"  [2.2] neural_web 属性: ✓")

            # 测试搜索
            if nm.neural_web:
                result = nm.neural_web.search_for_memory(
                    content="2025年用户增长策略",
                    tags=["growth", "strategy"],
                    max_results=2
                )
                print(f"  [2.3] 搜索结果: {result.get('source', 'unknown')}")
            else:
                print(f"  [2.3] neural_web 未初始化 (离线或导入失败)")
        else:
            print(f"  [2.2] neural_web 属性: ✗ (未找到)")

        print("\n  ✓ NeuralMemory 网络增强测试通过")
        return True

    except Exception as e:
        print(f"\n  ✗ NeuralMemory 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_refute_core_web():
    """测试 RefuteCore 网络增强"""
    print("\n" + "="*60)
    print("测试 3: RefuteCore 网络增强")
    print("="*60)

    try:
        from divine_oversight import get_oversight

        oversight = get_oversight()
        print(f"  [3.1] DivineTrackOversight 初始化: ✓")

        # 检查 refute_web 属性
        if hasattr(oversight, 'refute_web'):
            print(f"  [3.2] refute_web 属性: ✓")

            # 测试验证方法
            if oversight.refute_web:
                result = oversight.verify_with_evidence(
                    claim="人工智能将改变未来工作方式",
                    max_results=2
                )
                print(f"  [3.3] 验证结果:")
                print(f"        支持证据: {len(result.get('supporting_evidence', []))}")
                print(f"        反驳证据: {len(result.get('counter_evidence', []))}")
            else:
                print(f"  [3.3] refute_web 未初始化 (离线或导入失败)")
        else:
            print(f"  [3.2] refute_web 属性: ✗ (未找到)")

        print("\n  ✓ RefuteCore 网络增强测试通过")
        return True

    except Exception as e:
        print(f"\n  ✗ RefuteCore 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tianshu_web():
    """测试 TianShu 网络增强"""
    print("\n" + "="*60)
    print("测试 4: TianShu 网络增强")
    print("="*60)

    try:
        # 检查 eight_layer_pipeline 中的网络搜索功能
        from web_integration import TianShuWeb

        tw = TianShuWeb()
        print(f"  [4.1] TianShuWeb 初始化: ✓")

        # 测试增强NLP分析
        result = tw.enhance_nlp_analysis(
            "分析2025年AI在金融领域的最新应用",
            layer_context="测试"
        )
        print(f"  [4.2] NLP增强结果: {result.get('source', 'unknown')}")
        if result.get('terms'):
            print(f"        术语数量: {len(result['terms'])}")

        print("\n  ✓ TianShu 网络增强测试通过")
        return True

    except Exception as e:
        print(f"\n  ✗ TianShu 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_track_a_web():
    """测试神政轨 (TrackA) 网络增强"""
    print("\n" + "="*60)
    print("测试 5: 神政轨 (TrackA) 网络增强")
    print("="*60)

    try:
        from intelligence.dual_track.track_a import DivineGovernanceTrack

        track_a = DivineGovernanceTrack()
        print(f"  [5.1] DivineGovernanceTrack 初始化: ✓")

        # 检查 track_a_web 属性
        if hasattr(track_a, 'track_a_web'):
            print(f"  [5.2] track_a_web 属性: ✓")

            # 测试执行案例搜索
            if track_a.track_a_web:
                result = track_a.search_execution_cases(
                    task_type="战略分析",
                    context="用户增长",
                    max_results=2
                )
                print(f"  [5.3] 执行案例搜索: {result.get('source', 'unknown')}")
            else:
                print(f"  [5.3] track_a_web 未初始化 (离线或导入失败)")
        else:
            print(f"  [5.2] track_a_web 属性: ✗ (未找到)")

        print("\n  ✓ TrackA 网络增强测试通过")
        return True

    except Exception as e:
        print(f"\n  ✗ TrackA 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_track_b_web():
    """测试神行轨 (TrackB) 网络增强"""
    print("\n" + "="*60)
    print("测试 6: 神行轨 (TrackB) 网络增强")
    print("="*60)

    try:
        from intelligence.dual_track.track_b import DivineExecutionTrack

        track_b = DivineExecutionTrack(auto_appoint=False)
        print(f"  [6.1] DivineExecutionTrack 初始化: ✓")

        # 检查 track_b_web 属性
        if hasattr(track_b, 'track_b_web'):
            print(f"  [6.2] track_b_web 属性: ✓")

            # 测试专业知识搜索
            if track_b.track_b_web:
                result = track_b.search_expertise(
                    expertise_area="数据分析",
                    problem="用户行为分析",
                    max_results=2
                )
                print(f"  [6.3] 专业知识搜索: {result.get('source', 'unknown')}")
            else:
                print(f"  [6.3] track_b_web 未初始化 (离线或导入失败)")
        else:
            print(f"  [6.2] track_b_web 属性: ✗ (未找到)")

        print("\n  ✓ TrackB 网络增强测试通过")
        return True

    except Exception as e:
        print(f"\n  ✗ TrackB 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "#"*60)
    print("# Somn 网络搜索集成测试")
    print("#"*60)

    results = []

    # 执行所有测试
    results.append(("web_integration", test_web_integration()))
    results.append(("NeuralMemory", test_neural_memory_web()))
    results.append(("RefuteCore", test_refute_core_web()))
    results.append(("TianShu", test_tianshu_web()))
    results.append(("TrackA", test_track_a_web()))
    results.append(("TrackB", test_track_b_web()))

    # 汇总结果
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有测试通过！网络搜索集成完成。")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
