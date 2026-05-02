"""
八层智能处理管道 v5.1 - 真实调度器集成测试
验证八层管道与 SageDispatch 真实调度器 + RefuteCore 驳心引擎的集成
"""

import sys
import time
import traceback

sys.path.insert(0, ".")

from eight_layer_pipeline import (
    EightLayerPipeline,
    ProcessingGrade,
    DomainCategory,
    PipelineStage,
    _call_dispatcher,
    _call_dispatcher_chain,
    _call_refute_core,
    _get_dispatch_engine,
)


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_dispatcher_bridge():
    """测试0: 调度器桥接 - 验证真实调度器可调用"""
    print_header("TEST 0: 真实调度器桥接")
    checks = []

    # 测试单个调度器调用
    for dispatcher_id in ["SD-P1", "SD-F2", "SD-C1", "SD-C2", "SD-R1", "SD-R2", "SD-E1", "SD-L1"]:
        result = _call_dispatcher(dispatcher_id, "测试调度器调用")
        called = result.get("called", False)
        conf = result.get("confidence", 0.0)
        ok = called and conf > 0
        status = f"✓ {dispatcher_id}: called={called}, conf={conf:.2f}" if ok else f"✗ {dispatcher_id}: {result.get('error', 'unknown')}"
        print(f"  {status}")
        checks.append((dispatcher_id, ok))

    # 测试链式调用
    chain_results = _call_dispatcher_chain("测试链式调度", ["SD-P1", "SD-F2"])
    chain_ok = len(chain_results) == 2 and all(r.get("called") for r in chain_results)
    print(f"  {'✓' if chain_ok else '✗'} 链式调用: {len(chain_results)}个结果")
    checks.append(("链式调用", chain_ok))

    # 测试 RefuteCore 驳心引擎桥接
    rc_result = _call_refute_core("我们应该投资这个项目因为市场很大")
    rc_called = rc_result.get("called", False)
    rc_ok = rc_called
    print(f"  {'✓' if rc_ok else '✗'} RefuteCore T2引擎: called={rc_called}, version={rc_result.get('version', 'N/A')}")
    if rc_called:
        print(f"    强度: {rc_result.get('strength_grade', '?')}级, 风险: {rc_result.get('risk_level', '?')}")
    else:
        print(f"    错误: {rc_result.get('error', 'N/A')}")
    checks.append(("RefuteCore-T2", rc_ok))

    passed = sum(1 for _, ok in checks if ok)
    return passed, len(checks)


def test_basic():
    """测试1: 基础模式"""
    print_header("TEST 1: 基础模式 (BASIC)")
    pipeline = EightLayerPipeline()

    result = pipeline.process(
        "分析用户增长策略中存在的问题",
        grade=ProcessingGrade.BASIC
    )

    print(f"  需求类型: {result.all_layers['nl_analysis'].data.get('demand_type')}")
    print(f"  领域分类: {result.all_layers['nl_analysis'].data.get('domain')}")
    print(f"  处理等级: {result.grade.value}")
    print(f"  最终置信度: {result.final_confidence:.3f}")
    print(f"  总耗时: {result.total_duration_ms:.2f}ms")

    # 分流层真实调度器
    routing_data = result.all_layers['routing'].data
    dispatchers_called = routing_data.get('dispatchers_called', [])
    print(f"  分流层调度器: {dispatchers_called}")

    # 推理层真实调度器
    reasoning_data = result.all_layers['reasoning'].data
    r1_data = reasoning_data.get('r1_supervision', {})
    print(f"  SD-R1监管: {r1_data.get('report', 'N/A')}")
    print(f"  SD-R1真实调用: {r1_data.get('dispatcher_called', False)}")

    reasoning_info = reasoning_data.get('reasoning_result', {})
    print(f"  决策方法: {reasoning_info.get('decision_method')}")
    dispatchers_in_reasoning = reasoning_info.get('dispatchers_called', [])
    print(f"  推理层调度器: {dispatchers_in_reasoning}")

    # 论证层真实调度器
    arg_data = result.all_layers['argumentation'].data
    r2_data = arg_data.get('r2_argumentation', {})
    print(f"  SD-R2真实调用: {r2_data.get('dispatcher_called', False)}")
    print(f"  SD-L1真实调用: {arg_data.get('tracking', {}).get('dispatcher_called', False)}")

    checks = [
        ("基础模式", result.grade == ProcessingGrade.BASIC),
        ("置信度>0", result.final_confidence > 0),
        ("不进神之架构", not routing_data.get('enter_divine_architecture')),
        ("SD-R1监管", bool(r1_data)),
        ("路由路径不为空", len(result.routing_path) > 0),
        ("分流层有真实调度器", len(dispatchers_called) > 0),
        ("推理层有真实调度器", len(dispatchers_in_reasoning) > 0),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")

    return passed, len(checks)


def test_deep():
    """测试2: 深度模式"""
    print_header("TEST 2: 深度模式 (DEEP)")
    pipeline = EightLayerPipeline()

    result = pipeline.process(
        "请设计公司未来三年的全面战略规划，需要综合考虑市场竞争、内部资源和外部环境因素",
        grade=ProcessingGrade.DEEP
    )

    print(f"  需求类型: {result.all_layers['nl_analysis'].data.get('demand_type')}")
    print(f"  处理等级: {result.grade.value}")
    print(f"  最终置信度: {result.final_confidence:.3f}")

    routing_data = result.all_layers['routing'].data
    print(f"  分流层调度器: {routing_data.get('dispatchers_called', [])}")

    reasoning_info = result.all_layers['reasoning'].data.get('reasoning_result', {})
    print(f"  决策方法: {reasoning_info.get('decision_method')}")
    print(f"  推理层调度器: {reasoning_info.get('dispatchers_called', [])}")

    checks = [
        ("深度模式", result.grade == ProcessingGrade.DEEP),
        ("置信度>0", result.final_confidence > 0),
        ("进入神之架构", routing_data.get('enter_divine_architecture')),
        ("Claw讨论", routing_data.get('claw_discussion')),
        ("有翰林院审核", bool(reasoning_info.get('hanlin_review'))),
        ("分流层有真实调度器", len(routing_data.get('dispatchers_called', [])) > 0),
        ("推理层有真实调度器", len(reasoning_info.get('dispatchers_called', [])) > 0),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")

    return passed, len(checks)


def test_super():
    """测试3: 超级模式"""
    print_header("TEST 3: 超级模式 (SUPER)")
    pipeline = EightLayerPipeline()

    result = pipeline.process(
        "基于当前市场环境和公司内部创新能力，提出颠覆性的商业模式创新方案",
        grade=ProcessingGrade.SUPER
    )

    print(f"  处理等级: {result.grade.value}")
    print(f"  最终置信度: {result.final_confidence:.3f}")

    routing_data = result.all_layers['routing'].data
    print(f"  分流层调度器: {routing_data.get('dispatchers_called', [])}")

    reasoning_info = result.all_layers['reasoning'].data.get('reasoning_result', {})
    print(f"  决策方法: {reasoning_info.get('decision_method')}")
    print(f"  推理层调度器: {reasoning_info.get('dispatchers_called', [])}")
    print(f"  翰林院严格: {reasoning_info.get('hanlin_review', {}).get('strict_mode', False)}")

    arg_data = result.all_layers['argumentation'].data
    t2 = arg_data.get('t2_argumentation')
    print(f"  T2论证: {'有' if t2 else '无'}")
    if t2:
        print(f"    T2方法: {t2.get('method', 'N/A')}")
        print(f"    T2引擎调用: {t2.get('engine_called', False)}")
        if t2.get("engine_called"):
            print(f"    RefuteCore版本: {t2.get('version', '?')}")
            print(f"    强度等级: {t2.get('strength_grade', '?')}")
            print(f"    风险等级: {t2.get('risk_level', '?')}")

    checks = [
        ("超级模式", result.grade == ProcessingGrade.SUPER),
        ("置信度>0", result.final_confidence > 0),
        ("进入神之架构", routing_data.get('enter_divine_architecture')),
        ("SD-C1+SD-C2联合", "联合" in reasoning_info.get('decision_method', '')),
        ("SD-D3极致论证", "D3" in reasoning_info.get('argumentation_level', '')),
        ("翰林院严格审核", reasoning_info.get('hanlin_review', {}).get('strict_mode', False)),
        ("T2 RefuteCore论证", t2 is not None),
        ("T2方法含RefuteCore", t2 is not None and "RefuteCore" in t2.get('method', '')),
        ("分流层含SD-F1", "SD-F1" in routing_data.get('dispatchers_called', [])),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")

    return passed, len(checks)


def test_domain_classification():
    """测试4: 领域分类准确性"""
    print_header("TEST 4: 领域分类")

    from eight_layer_pipeline import NLAnalysisLayer, InputLayer
    analyzer = NLAnalysisLayer()
    input_layer = InputLayer()

    test_cases = [
        ("分析社会阶层的流动性和教育公平问题", DomainCategory.SOCIAL_SCIENCE, "社会科学"),
        ("从儒家思想角度解读《论语》中的仁义道德", DomainCategory.LITERATURE_HISTORY, "文学历史"),
        ("解释量子纠缠的物理原理和实验验证方法", DomainCategory.NATURAL_SCIENCE, "自然科学"),
        ("如何使用深度学习算法优化推荐系统的性能", DomainCategory.TECHNOLOGY, "科技"),
        ("分析直播电商的GMV增长策略和ROI优化", DomainCategory.BUSINESS, "商业"),
        ("从道家无为而治的角度探讨现代管理哲学", DomainCategory.PHILOSOPHY, "哲学"),
    ]

    total = len(test_cases)
    passed = 0

    for text, expected_domain, domain_name in test_cases:
        input_r = input_layer.process(text)
        nl_r = analyzer.process(input_r)
        actual = nl_r.data.get("domain", DomainCategory.GENERAL)
        ok = actual == expected_domain
        if ok:
            passed += 1
        print(f"  {'✓' if ok else '✗'} {domain_name}: 期望={expected_domain.value}, 实际={actual.value if isinstance(actual, DomainCategory) else actual}")

    return passed, total


def test_empty_input():
    """测试5: 空输入防护"""
    print_header("TEST 5: 空输入防护")

    pipeline = EightLayerPipeline()
    checks = []

    r1 = pipeline.process("")
    checks.append(("空字符串拦截", r1.final_confidence == 0.0))

    r2 = pipeline.process(None)
    checks.append(("None拦截", r2.final_confidence == 0.0))

    r3 = pipeline.process("   ")
    checks.append(("纯空格拦截", r3.final_confidence == 0.0))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")

    return passed, len(checks)


def test_quick_functions():
    """测试6: 快捷函数"""
    print_header("TEST 6: 快捷函数")

    checks = []

    from eight_layer_pipeline import quick_process
    result = quick_process("分析增长策略")
    checks.append(("quick_process返回字符串", isinstance(result, str) and len(result) > 0))

    from eight_layer_pipeline import deep_process
    r2 = deep_process("设计战略规划")
    checks.append(("deep_process返回PipelineResult", hasattr(r2, 'final_answer')))

    from eight_layer_pipeline import super_process
    r3 = super_process("颠覆性创新方案")
    checks.append(("super_process返回PipelineResult", hasattr(r3, 'final_answer')))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")

    return passed, len(checks)


def test_real_dispatcher_coverage():
    """测试7: 所有12个调度器在三个模式中被覆盖调用"""
    print_header("TEST 7: 调度器全覆盖")

    pipeline = EightLayerPipeline()

    all_dispatchers = set()

    for mode_name, mode_grade in [("基础", ProcessingGrade.BASIC), ("深度", ProcessingGrade.DEEP), ("超级", ProcessingGrade.SUPER)]:
        r = pipeline.process(f"测试{mode_name}模式", grade=mode_grade)

        # 从所有层级收集调度器
        for layer_name, layer_result in r.all_layers.items():
            data = layer_result.data

            # 分流层 dispatchers_called
            if 'dispatchers_called' in data:
                all_dispatchers.update(data['dispatchers_called'])

            # 推理层 dispatchers_called
            if 'reasoning_result' in data:
                ri = data['reasoning_result']
                if isinstance(ri, dict) and 'dispatchers_called' in ri:
                    all_dispatchers.update(ri['dispatchers_called'])

            # 推理层 SD-R1
            if 'r1_supervision' in data:
                r1 = data['r1_supervision']
                if isinstance(r1, dict) and r1.get('dispatcher_called'):
                    all_dispatchers.add('SD-R1')

            # 论证层 SD-R2
            if 'r2_argumentation' in data:
                r2 = data['r2_argumentation']
                if isinstance(r2, dict) and r2.get('dispatcher_called'):
                    all_dispatchers.add('SD-R2')

            # 论证层 SD-L1
            if 'tracking' in data:
                trk = data['tracking']
                if isinstance(trk, dict) and trk.get('dispatcher_called'):
                    all_dispatchers.add('SD-L1')

            # 论证层 RefuteCore-T2
            if 't2_argumentation' in data:
                t2 = data['t2_argumentation']
                if isinstance(t2, dict) and t2.get('engine_called'):
                    all_dispatchers.add('RefuteCore-T2')
            # 从 dispatchers_called 也提取 RefuteCore-T2
            if 'dispatchers_called' in data:
                for d in data['dispatchers_called']:
                    if 'RefuteCore' in d:
                        all_dispatchers.add(d)

    print(f"  三模式总计调用调度器: {sorted(all_dispatchers)}")

    expected = {"SD-P1", "SD-F1", "SD-F2", "SD-C1", "SD-C2", "SD-D1", "SD-D2", "SD-D3",
                 "SD-E1", "SD-R1", "SD-R2", "SD-L1", "RefuteCore-T2"}
    missing = expected - all_dispatchers
    coverage = len(all_dispatchers & expected) / len(expected) * 100

    print(f"  覆盖率: {coverage:.0f}% ({len(all_dispatchers & expected)}/{len(expected)})")
    if missing:
        print(f"  未覆盖: {sorted(missing)}")

    checks = [
        ("SD-P1覆盖", "SD-P1" in all_dispatchers),
        ("SD-F2覆盖", "SD-F2" in all_dispatchers),
        ("SD-R1覆盖", "SD-R1" in all_dispatchers),
        ("SD-R2覆盖", "SD-R2" in all_dispatchers),
        ("SD-C1覆盖", "SD-C1" in all_dispatchers),
        ("SD-C2覆盖", "SD-C2" in all_dispatchers),
        ("SD-D1覆盖", "SD-D1" in all_dispatchers),
        ("SD-D2覆盖", "SD-D2" in all_dispatchers),
        ("SD-D3覆盖", "SD-D3" in all_dispatchers),
        ("SD-E1覆盖", "SD-E1" in all_dispatchers),
        ("SD-L1覆盖", "SD-L1" in all_dispatchers),
        ("RefuteCore-T2覆盖", "RefuteCore-T2" in all_dispatchers),
    ]

    # SD-F1 只在超级模式中调用
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")

    return passed, len(checks)


# ==================== 主流程 ====================

if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║  SageDispatch v5.1 八层管道 - 真实调度器+RefuteCore ║")
    print("╚══════════════════════════════════════════════════════╝")

    tests = [
        ("真实调度器桥接", test_dispatcher_bridge),
        ("基础模式", test_basic),
        ("深度模式", test_deep),
        ("超级模式", test_super),
        ("领域分类", test_domain_classification),
        ("空输入防护", test_empty_input),
        ("快捷函数", test_quick_functions),
        ("调度器全覆盖", test_real_dispatcher_coverage),
    ]

    total_pass = 0
    total_count = 0

    for name, test_fn in tests:
        try:
            p, c = test_fn()
            total_pass += p
            total_count += c
        except Exception as e:
            print(f"  ✗ {name} 异常: {e}")
            traceback.print_exc()
            total_count += 1

    # 汇总
    print_header("测试汇总")
    print(f"  总通过: {total_pass}/{total_count}")
    print(f"  成功率: {total_pass/total_count*100:.1f}%")
    status = "ALL PASS ✓" if total_pass == total_count else f"FAIL ({total_count - total_pass} failures)"
    print(f"  状态: {status}")
    print()
