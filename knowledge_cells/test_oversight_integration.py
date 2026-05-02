#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神政轨监督体系集成测试
验证监督框架已正确集成到各核心模块
"""

import sys
import os

_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_script_dir)
sys.path.insert(0, _script_dir)
sys.path.insert(0, os.path.dirname(_script_dir))

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_oversight_import():
    """测试1: 监督框架可从knowledge_cells导入"""
    print_header("TEST 1: 监督框架导入")
    
    try:
        from knowledge_cells import (
            DivineTrackOversight,
            OversightCategory,
            ComplianceLevel,
            get_oversight,
            record_oversight
        )
        print("  ✓ DivineTrackOversight")
        print("  ✓ OversightCategory")
        print("  ✓ ComplianceLevel")
        print("  ✓ get_oversight")
        print("  ✓ record_oversight")
        return True
    except ImportError as e:
        print(f"  ✗ 导入失败: {e}")
        return False


def test_core_oversight():
    """测试2: SageDispatch核心调度监督"""
    print_header("TEST 2: SageDispatch核心调度监督")
    
    from knowledge_cells import dispatch, get_oversight, OversightCategory
    
    # 清空之前的记录
    oversight = get_oversight()
    oversight.clear()
    
    # 执行调度
    result = dispatch("什么是人工智能")
    
    # 检查监督记录
    records = oversight.records
    sage_records = [r for r in records if r.module == "SageDispatch"]
    
    print(f"  调度结果: {result.state.value}")
    print(f"  监督记录数: {len(sage_records)}")
    
    for rec in sage_records:
        print(f"    - {rec.action}: {rec.compliance.value}")
    
    return len(sage_records) >= 1


def test_domain_nexus_oversight():
    """测试3: DomainNexus知识库监督"""
    print_header("TEST 3: DomainNexus知识库监督")
    
    from knowledge_cells import DomainNexus, get_oversight
    
    # 清空之前的记录
    oversight = get_oversight()
    oversight.clear()
    
    # 查询知识库
    nexus = DomainNexus()
    result = nexus.query("什么是机器学习")
    
    # 检查监督记录
    records = oversight.records
    nexus_records = [r for r in records if r.module == "DomainNexus"]
    
    print(f"  查询结果: {bool(result.get('answer'))}")
    print(f"  监督记录数: {len(nexus_records)}")
    
    for rec in nexus_records:
        print(f"    - {rec.action}: {rec.compliance.value}")
        print(f"      输入: {rec.input_summary[:50]}...")
        print(f"      输出: cells_accessed={rec.output_summary}")
    
    return len(nexus_records) >= 1


def test_tianshu_oversight():
    """测试4: 天枢八层管道监督"""
    print_header("TEST 4: 天枢八层管道监督")
    
    from knowledge_cells import EightLayerPipeline, ProcessingGrade, get_oversight
    
    # 清空之前的记录
    oversight = get_oversight()
    oversight.clear()
    
    # 执行管道
    pipeline = EightLayerPipeline()
    result = pipeline.process("分析人工智能的发展趋势", ProcessingGrade.BASIC)
    
    # 检查监督记录
    records = oversight.records
    tianshu_records = [r for r in records if r.module == "TianShu"]
    
    print(f"  管道结果: confidence={result.final_confidence:.2f}")
    print(f"  监督记录数: {len(tianshu_records)}")
    
    for rec in tianshu_records:
        print(f"    - {rec.action}: {rec.compliance.value}")
        if isinstance(rec.output_summary, dict):
            print(f"      grade={rec.output_summary.get('grade', 'N/A')}")
            print(f"      confidence={rec.output_summary.get('final_confidence', 0):.2f}")
        else:
            print(f"      output: {rec.output_summary[:50]}...")
    
    return len(tianshu_records) >= 1


def test_oversight_report():
    """测试5: 监督报告生成"""
    print_header("TEST 5: 监督报告生成")
    
    from knowledge_cells import get_oversight
    
    oversight = get_oversight()
    report = oversight.get_report()
    
    print(f"  总记录数: {report.total_records}")
    print(f"  通过: {report.pass_count}")
    print(f"  警告: {report.warn_count}")
    print(f"  驳回: {report.fail_count}")
    print(f"  汇总: {report.summary}")
    
    # 显示最近3条记录
    print("\n  最近记录:")
    for rec in report.records[-3:]:
        print(f"    {rec.module}/{rec.action}: {rec.compliance.value}")
    
    return report.total_records >= 1


def test_reroute_not_blocking():
    """测试6: 驳回不阻断工作流"""
    print_header("TEST 6: 驳回不阻断工作流")
    
    from knowledge_cells import get_oversight, ComplianceLevel
    
    oversight = get_oversight()
    
    # 手动创建一条驳回记录
    record = oversight.record(
        module="TestModule",
        action="test_action",
        category=1,  # OversightCategory.RESULT
        input_data={"test": "data"},
        output_data={}
    )
    
    # 触发驳回
    reroute_cmd = oversight.reroute(record, "测试驳回")
    
    print(f"  驳回指令: {reroute_cmd['action']}")
    print(f"  驳回原因: {reroute_cmd['reason']}")
    print(f"  允许继续: {reroute_cmd['allow_continue']}")
    
    # 验证工作流继续
    test_result = "工作继续执行"
    if reroute_cmd.get('allow_continue'):
        test_result += " ✓"
    
    print(f"  工作流状态: {test_result}")
    
    return reroute_cmd.get('allow_continue') == True


def test_multi_module_oversight():
    """测试7: 多模块监督"""
    print_header("TEST 7: 多模块监督汇总")
    
    from knowledge_cells import get_oversight
    
    oversight = get_oversight()
    report = oversight.get_report()
    
    # 按模块统计
    modules = {}
    for rec in report.records:
        if rec.module not in modules:
            modules[rec.module] = []
        modules[rec.module].append(rec)
    
    print(f"  监督模块数: {len(modules)}")
    for module, records in modules.items():
        passed = sum(1 for r in records if r.compliance.value == "pass")
        print(f"    {module}: {len(records)}条记录, {passed}通过")
    
    return len(modules) >= 3  # 至少3个模块有记录


def main():
    print("\n" + "="*60)
    print("  神政轨监督体系集成测试")
    print("="*60)
    
    tests = [
        ("监督框架导入", test_oversight_import),
        ("SageDispatch监督", test_core_oversight),
        ("DomainNexus监督", test_domain_nexus_oversight),
        ("天枢管道监督", test_tianshu_oversight),
        ("监督报告", test_oversight_report),
        ("驳回不阻断", test_reroute_not_blocking),
        ("多模块监督", test_multi_module_oversight),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        try:
            if test_fn():
                passed += 1
                print(f"\n  ✅ {name} 通过")
            else:
                failed += 1
                print(f"\n  ❌ {name} 失败")
        except Exception as e:
            failed += 1
            print(f"\n  ❌ {name} 异常: {e}")
            import traceback
            traceback.print_exc()
    
    print_header("测试汇总")
    print(f"  通过: {passed}/{len(tests)}")
    print(f"  失败: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n  🎉 神政轨监督体系集成测试全部通过！")
        print("  监督框架已成功集成到:")
        print("    - SageDispatch 核心调度")
        print("    - DomainNexus 知识库")
        print("    - TianShu 八层管道")
        return 0
    else:
        print(f"\n  ⚠️  {failed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
