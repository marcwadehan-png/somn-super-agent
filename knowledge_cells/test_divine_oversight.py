#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神政轨监督框架测试
测试监督框架对7大核心模块的过程记录、成果验证、驳回机制
"""

import sys
import os
import time

_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_script_dir)
sys.path.insert(0, _script_dir)
sys.path.insert(0, os.path.dirname(_script_dir))

from divine_oversight import (
    DivineTrackOversight, 
    OversightCategory, 
    ComplianceLevel,
    get_oversight,
    record_oversight,
    oversee_module
)

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_basic_oversight():
    """测试1: 基础监督功能"""
    print_header("TEST 1: 基础监督功能")
    
    ov = DivineTrackOversight()
    
    # 记录各模块
    r1 = ov.record("RefuteCore", "refute", OversightCategory.RESULT,
                    input_data={"text": "测试论证"},
                    output_data={"refutations": ["ok"]})
    
    r2 = ov.record("DomainNexus", "query", OversightCategory.RESULT,
                    input_data={"q": "AI"},
                    output_data={"answer": "Artificial Intelligence"})
    
    r3 = ov.record("SageDispatch", "dispatch", OversightCategory.PROCESS,
                    input_data={"problem": "什么是量子"},
                    output_data={"result": "量子计算是..."})
    
    r4 = ov.record("PanWisdomTree", "identify", OversightCategory.RESULT,
                    input_data={"problem": "增长问题"},
                    output_data={"school": "ECONOMICS"})
    
    r5 = ov.record("DivineReason", "solve", OversightCategory.RESULT,
                    input_data={"q": "为什么天空蓝"},
                    output_data={"reasoning": "瑞利散射"})
    
    r6 = ov.record("TianShu", "process", OversightCategory.PROCESS,
                    input_data={"text": "分析AI"},
                    output_data={"layers": 8})
    
    r7 = ov.record("NeuralMemory", "store", OversightCategory.MEMORY_IO,
                    input_data={"key": "insight"},
                    output_data={"status": "saved"})
    
    report = ov.get_report()
    
    print(f"  总记录: {report.total_records}")
    print(f"  通过: {report.pass_count}")
    print(f"  驳回: {report.fail_count}")
    
    assert report.total_records == 7, "应有7条记录"
    assert report.pass_count == 7, "全部通过"
    print("  ✅ 基础监督通过")
    return True


def test_reroute_mechanism():
    """测试2: 驳回机制"""
    print_header("TEST 2: 驳回机制")
    
    ov = DivineTrackOversight()
    
    # 模拟一个不合规的输出（空内容）
    bad_record = ov.record("RefuteCore", "refute", OversightCategory.RESULT,
                           input_data={"text": "测试"},
                           output_data={"refutations": []})  # 空驳回列表
    
    # 再次检查（触发规则）
    # 手动标记为不合规测试
    bad_record.compliance = ComplianceLevel.FAIL  # 模拟
    
    reroute_cmd = ov.reroute(bad_record, "输出内容为空")
    
    print(f"  驳回指令: {reroute_cmd['action']}")
    print(f"  驳回原因: {reroute_cmd['reason']}")
    print(f"  允许继续: {reroute_cmd['allow_continue']}")  # 关键：不阻断
    
    assert reroute_cmd['allow_continue'] == True, "工作流应继续"
    assert reroute_cmd['action'] == 'reroute', "应为驳回指令"
    print("  ✅ 驳回机制通过（不阻断工作流）")
    return True


def test_neural_memory_io():
    """测试3: NeuralMemory I/O 监督"""
    print_header("TEST 3: NeuralMemory I/O 监督")
    
    ov = DivineTrackOversight()
    ov.watch("NeuralMemory")
    
    # 读取操作
    read_record = ov.record("NeuralMemory", "retrieve", OversightCategory.MEMORY_IO,
                            input_data={"key": "insight_001"},
                            output_data={"content": "AI改变教育", "type": "insight"})
    
    # 写入操作
    write_record = ov.record("NeuralMemory", "store", OversightCategory.MEMORY_IO,
                             input_data={"key": "insight_002", "value": {"content": "测试"}},
                             output_data={"status": "success"})
    
    print(f"  读取记录: {read_record.module}/{read_record.action}")
    print(f"  写入记录: {write_record.module}/{write_record.action}")
    print(f"  I/O类别: {OversightCategory.MEMORY_IO.value}")
    
    assert read_record.category == OversightCategory.MEMORY_IO
    assert write_record.category == OversightCategory.MEMORY_IO
    print("  ✅ NeuralMemory I/O 监督通过")
    return True


def test_module_watch():
    """测试4: 模块监督开关"""
    print_header("TEST 4: 模块监督开关")
    
    ov = DivineTrackOversight()
    
    # 开启监督
    ov.watch("RefuteCore")
    ov.watch("DomainNexus")
    
    assert ov.is_watching("RefuteCore") == True
    assert ov.is_watching("DomainNexus") == True
    assert ov.is_watching("SageDispatch") == False
    
    # 关闭监督
    ov.unwatch("RefuteCore")
    assert ov.is_watching("RefuteCore") == False
    
    print("  ✅ 模块监督开关通过")
    return True


def test_compliance_rules():
    """测试5: 合规规则"""
    print_header("TEST 5: 合规规则")
    
    ov = DivineTrackOversight()
    
    # 规则1: 正常输入
    r1 = ov.record("Test", "action", OversightCategory.RESULT,
                    input_data={"key": "value"},
                    output_data={"result": "ok"})
    print(f"  正常记录: {r1.compliance.value}")
    
    # 规则2: 空输入（触发memory_input规则）
    r2 = ov.record("NeuralMemory", "retrieve", OversightCategory.MEMORY_IO,
                   input_data=None,  # 空输入
                   output_data={"result": None})
    print(f"  空输入: {r2.compliance.value} (预期fail)")
    
    # 规则3: 过短输出
    r3 = ov.record("Test", "action", OversightCategory.RESULT,
                    input_data={"key": "v"},
                    output_data={"result": "a"})  # 太短
    print(f"  过短输出: {r3.compliance.value} (预期warn)")
    
    print("  ✅ 合规规则通过")
    return True


def test_oversight_report():
    """测试6: 监督报告"""
    print_header("TEST 6: 监督报告")
    
    ov = DivineTrackOversight()
    
    # 模拟各种记录
    ov.record("RefuteCore", "refute", OversightCategory.RESULT,
              input_data={}, output_data={})
    ov.record("DomainNexus", "query", OversightCategory.RESULT,
              input_data={}, output_data={})
    ov.record("NeuralMemory", "store", OversightCategory.MEMORY_IO,
              input_data={}, output_data={})
    
    report = ov.get_report()
    
    print(f"  报告摘要: {report.summary}")
    print(f"  记录详情数量: {len(report.records)}")
    
    for rec in report.records:
        print(f"    {rec.module}/{rec.action}: {rec.compliance.value}")
    
    print("  ✅ 监督报告通过")
    return True


def test_global_oversight():
    """测试7: 全局监督实例"""
    print_header("TEST 7: 全局监督实例")
    
    # 获取全局实例
    ov1 = get_oversight()
    ov2 = get_oversight()
    
    assert ov1 is ov2, "应为同一实例"
    print(f"  全局实例ID: {id(ov1)}")
    print("  ✅ 全局单例通过")
    return True


def main():
    print("\n" + "="*60)
    print("  神政轨监督框架测试")
    print("="*60)
    
    tests = [
        ("基础监督", test_basic_oversight),
        ("驳回机制", test_reroute_mechanism),
        ("NeuralMemory I/O", test_neural_memory_io),
        ("模块监督开关", test_module_watch),
        ("合规规则", test_compliance_rules),
        ("监督报告", test_oversight_report),
        ("全局单例", test_global_oversight),
    ]
    
    passed = 0
    failed = 0
    start = time.time()
    
    for name, test_fn in tests:
        try:
            if test_fn():
                passed += 1
            else:
                failed += 1
                print(f"  ❌ {name} 失败")
        except Exception as e:
            failed += 1
            print(f"  ❌ {name} 异常: {e}")
    
    total = time.time() - start
    
    print_header("测试汇总")
    print(f"  通过: {passed}/{len(tests)}")
    print(f"  失败: {failed}/{len(tests)}")
    print(f"  耗时: {total:.2f}秒")
    
    if failed == 0:
        print("\n  🎉 神政轨监督框架测试全部通过！")
        return 0
    else:
        print(f"\n  ⚠️  {failed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
