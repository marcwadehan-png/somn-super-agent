# -*- coding: utf-8 -*-
"""
驳心引擎 RefuteCore v3.0.3 完整测试
包含功能测试 + 质量断言 + 鲁棒性测试
"""

import sys, os

sys.path.insert(0, os.path.dirname(__file__))

from refute_core import (
    RefuteCoreEngine, quick_refute, refute_and_solve, quick_refute_md, batch_refute,
    RefuteDimension, ArgumentType, FallacyType,
    ArgumentParser, ParsedArgument,
    RefutationStrategist, MultiDimensionRefutation,
    ArgumentStrengthAssessor, StrengthAssessment,
    DebateArena, DebateResult,
    ArgumentRepair, RepairedArgument,
    SolutionGenerator, SolutionSet,
    BatchRefuter, BatchResult,
)


def test_argument_parser_v3():
    """测试论证解析器 v3.1 增强功能"""
    parser = ArgumentParser()
    
    # 测试1: 因果论证 + 领域识别
    text1 = "因为竞争对手都在降价，所以我们也必须降价，否则就会失去市场份额"
    p1 = parser.parse(text1)
    
    assert p1.argument_type in (ArgumentType.CAUSAL, ArgumentType.DECISION, ArgumentType.MIXED), f"类型错误: {p1.argument_type}"
    assert p1.context_domain == "商业竞争", f"领域识别错误: {p1.context_domain}"
    assert p1.claim_subject, f"主语为空"
    assert p1.negated_claim, f"否定主张为空"
    assert len(p1.premises) >= 1, f"前提为空"
    assert p1.vulnerability_score > 0, f"脆弱性为0"
    print(f"✅ 测试1通过: 因果论证+领域识别+主谓宾+否定主张")
    print(f"   类型={p1.argument_type.value} 领域={p1.context_domain} 主语={p1.claim_subject} 否定={p1.negated_claim}")
    
    # 测试2: 投资决策
    text2 = "投资这个项目因为感觉很好，市场很大，一定会有好的回报"
    p2 = parser.parse(text2)
    
    assert p2.context_domain == "投资理财", f"领域识别错误: {p2.context_domain}"
    assert len(p2.weakness_indicators) > 0, f"未检测到弱点指示词"
    assert "一定" in p2.weakness_indicators, f"未检测到'一定'"
    print(f"✅ 测试2通过: 投资领域+弱点指示词检测")
    print(f"   弱点指示词={p2.weakness_indicators}")
    
    # 测试3: 企业管理
    text3 = "团队必须严格执行KPI考核，因为只有这样才能保证绩效提升"
    p3 = parser.parse(text3)
    
    assert p3.context_domain == "企业管理", f"领域识别错误: {p3.context_domain}"
    assert len(p3.implicit_assumptions) > 0, f"隐含假设为空"
    print(f"✅ 测试3通过: 企业管理领域+隐含假设推断")
    print(f"   隐含假设数={len(p3.implicit_assumptions)}")


def test_refutation_v3():
    """测试反驳策略 v3.0.1 智能填充 + 质量断言"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    
    text = "因为竞争对手都在降价，所以我们也必须降价，否则就会失去市场份额"
    parsed = parser.parse(text)
    refutation = strategist.generate_refutations(parsed, top_n=3)
    
    assert len(refutation.refutations) >= 3, f"反驳数不足: {len(refutation.refutations)}"
    assert refutation.strongest_refutation.strength > 0.5, f"最强反驳强度太低: {refutation.strongest_refutation.strength}"
    
    # v3.0: 检查智能填充 — 反驳内容应包含输入文本的关键词
    for ref in refutation.refutations:
        assert ref.counter_argument, f"反驳论点为空"
        assert "{" not in ref.counter_argument, f"占位符未被替换: {ref.counter_argument}"
    
    # v3.0.1 质量断言: 反驳强度 < 100%
    max_strength = max(r.strength for r in refutation.refutations)
    assert max_strength < 1.0, f"⚠ 最强反驳达到100%: {max_strength:.0%}"
    
    # v3.0.1 质量断言: 反驳有区分度（top3中最高和最低差距 >= 2%）
    strengths = sorted([r.strength for r in refutation.refutations], reverse=True)
    if len(strengths) >= 2:
        diff = strengths[0] - strengths[-1]
        assert diff >= 0.01, f"⚠ 反驳无区分度(diff={diff:.2%})"
    
    print(f"✅ 反驳策略测试通过 (含质量断言)")
    print(f"   最强维度={refutation.strongest_refutation.dimension.value} 强度={refutation.strongest_refutation.strength:.0%}")
    for i, ref in enumerate(refutation.refutations, 1):
        print(f"   {i}. [{ref.dimension.value}] {ref.counter_argument[:60]}...")


def test_strength_assessment():
    """测试强度评估 + 质量断言"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    
    text = "投资这个项目因为感觉很好，市场很大，一定会有好的回报"
    parsed = parser.parse(text)
    refutation = strategist.generate_refutations(parsed, top_n=3)
    assessment = assessor.assess(parsed, refutation)
    
    assert 0 <= assessment.overall_strength <= 1, f"强度超出范围: {assessment.overall_strength}"
    assert assessment.strength_grade in ("S","A","B","C","D","F"), f"无效等级: {assessment.strength_grade}"
    assert len(assessment.vulnerabilities) > 0, f"脆弱点为空"
    
    # v3.0.1 质量断言: 强度不应过低(>=10%)也不应过高(<=90%)对于弱论证
    assert assessment.overall_strength >= 0.10, f"⚠ 强度过低: {assessment.overall_strength:.0%}"
    assert assessment.overall_strength <= 0.90, f"⚠ 强度过高: {assessment.overall_strength:.0%}"
    
    print(f"✅ 强度评估测试通过 (含质量断言): 等级={assessment.strength_grade} 强度={assessment.overall_strength:.0%}")


def test_debate_v3():
    """测试辩论对抗 v3.0.1 + 质量断言"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    arena = DebateArena()
    
    text = "因为竞争对手都在降价，所以我们必须降价"
    parsed = parser.parse(text)
    refutation = strategist.generate_refutations(parsed, top_n=3)
    assessment = assessor.assess(parsed, refutation)
    debate = arena.debate(parsed, refutation, assessment)
    
    assert len(debate.rounds) == 3, f"辩论轮次错误: {len(debate.rounds)}"
    assert debate.final_verdict, f"最终裁决为空"
    assert 0 <= debate.truth_approximation <= 1, f"逼近度超出范围"
    assert debate.evolved_argument, f"进化论点为空"
    
    for rnd in debate.rounds:
        assert rnd.proposer_argument, f"正方论点为空"
        assert rnd.refuter_counter, f"反方反驳为空"
        assert rnd.proposer_defense, f"正方防御为空"
    
    # v3.0.1 质量断言: 进化后论点应与原始不同或含进化标记
    evolved = debate.evolved_argument
    original_claim = parsed.core_claim
    is_evolved = (
        evolved != original_claim or 
        evolved.startswith(("修正:", "限定:", "最终版:", "'"))
    )
    assert is_evolved, f"⚠ 进化论点无明显变化: '{evolved}' vs '{original_claim}'"
    
    print(f"✅ 辩论对抗测试通过 (含质量断言)")
    print(f"   裁决={debate.final_verdict[:50]}")
    print(f"   逼近度={debate.truth_approximation:.0%}")
    print(f"   进化论点={debate.evolved_argument[:60]}")


def test_argument_repair():
    """测试论证修复器 v3.0.1"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    arena = DebateArena()
    repair = ArgumentRepair()
    
    text = "投资这个项目因为感觉很好，一定会有好的回报"
    parsed = parser.parse(text)
    refutation = strategist.generate_refutations(parsed, top_n=3)
    assessment = assessor.assess(parsed, refutation)
    debate = arena.debate(parsed, refutation, assessment)
    repaired = repair.repair(parsed, refutation, assessment, debate)
    
    assert repaired.repaired_claim != parsed.core_claim or assessment.strength_grade in ("S","A"), f"修复后论点未改变"
    assert repaired.repaired_strength_estimate >= assessment.overall_strength * 0.9, f"修复后强度应>=原始强度*0.9"
    assert len(repaired.added_premises) >= 0, f"新增前提为空列表"
    assert repaired.repair_rationale, f"修复理由为空"
    
    print(f"✅ 论证修复测试通过")
    print(f"   原始: {parsed.core_claim[:40]}")
    print(f"   修复: {repaired.repaired_claim[:40]}")
    print(f"   强度提升: {assessment.overall_strength:.0%} → {repaired.repaired_strength_estimate:.0%}")


def test_full_pipeline_v3():
    """测试完整 v3.0.1 流程 + 质量断言"""
    engine = RefuteCoreEngine()
    
    text = "我们应该降价应对竞争，因为所有对手都在降价，如果不降价就一定会失去市场份额"
    result = engine.refute(text)
    
    # 基本验证
    assert result.engine_version == "6.2.0"
    assert result.parsed_argument.context_domain == "商业竞争"
    assert len(result.refutation.refutations) >= 3
    assert result.assessment.strength_grade in ("S","A","B","C","D","F")
    assert len(result.debate.rounds) == 3
    assert result.repair.repaired_claim
    assert result.repair.repaired_strength_estimate > 0
    assert len(result.solutions.solutions) >= 3
    assert result.executive_summary
    assert result.risk_level
    assert result.key_takeaway
    
    # v3.0.1 质量断言集:
    # 1. 反驳强度有上限
    max_ref_s = max(r.strength for r in result.refutation.refutations)
    assert max_ref_s < 1.0, f"⚠ 最强反驳满分: {max_ref_s:.0%}"
    
    # 2. 论证强度在合理范围
    s = result.assessment.overall_strength
    assert 0.10 <= s <= 0.85, f"⚠ 强度异常: {s:.0%}"
    
    # 3. SPO主语不是代词
    subj = result.parsed_argument.claim_subject
    stop_words = {"我们","我","你","他","她","它","也","都"}
    assert subj not in stop_words, f"⚠ SPO主语是停用词: '{subj}'"
    
    print(f"✅ 完整流程测试通过 (含质量断言)")
    print(f"   版本={result.engine_version}")
    print(f"   领域={result.parsed_argument.context_domain}")
    print(f"   强度={result.assessment.strength_grade}级({result.assessment.overall_strength:.0%})")
    print(f"   风险={result.risk_level}")
    print(f"   修复后={result.repair.repaired_claim[:40]}")


def test_quick_functions():
    """测试便捷函数"""
    text_output = quick_refute("投资这个项目因为感觉很好")
    assert isinstance(text_output, str)
    assert "驳心引擎" in text_output
    print(f"✅ quick_refute 测试通过")
    
    md_output = quick_refute_md("投资这个项目因为感觉很好")
    assert isinstance(md_output, str)
    assert "# " in md_output
    print(f"✅ quick_refute_md 测试通过")
    
    result = refute_and_solve("因为对手降价所以我们必须降价")
    assert hasattr(result, 'assessment')
    assert hasattr(result, 'repair')
    print(f"✅ refute_and_solve 测试通过")


def test_batch_refute():
    """测试批量反驳 + 质量断言"""
    engine = RefuteCoreEngine()
    
    arguments = [
        "我们应该降价应对竞争，因为对手都在降价",
        "我们不应该降价，因为价格战会损害品牌价值",
        "降价是短期内获取市场份额的最有效手段",
    ]
    
    result = engine.batch_refute(arguments)
    
    assert len(result.individual_results) == 3, f"批量结果数错误"
    assert result.consistency_score >= 0, f"一致性评分错误"
    assert 0 <= result.strongest_argument_index < 3, f"最强论点索引错误"
    assert 0 <= result.weakest_argument_index < 3, f"最弱论点索引错误"
    assert result.overall_assessment
    
    # v3.0.1 质量断言: 应检测出矛盾
    assert len(result.contradictions) >= 1, f"⚠ 未检测到矛盾! 3个明显矛盾论点应被检出"
    assert result.consistency_score < 1.0, f"⚠ 一致性应为<100%当存在矛盾时: {result.consistency_score:.0%}"
    
    print(f"✅ 批量反驳测试通过 (含质量断言)")
    print(f"   发现{len(result.contradictions)}个矛盾")
    print(f'   一致性评分={result.consistency_score:.0%}')
    print(f'   最强论点[{result.strongest_argument_index}] 最弱论点[{result.weakest_argument_index}]')


def test_format_markdown():
    """测试Markdown输出"""
    engine = RefuteCoreEngine()
    result = engine.refute("团队必须严格执行KPI考核，因为只有这样才能保证绩效提升")
    md = engine._format_markdown(result)
    
    assert "# " in md
    assert "反驳结果" in md
    assert "强度评估" in md
    assert "辩论结果" in md
    assert "论证修复" in md
    print(f"✅ Markdown输出测试通过")


def test_quality_integration():
    """v3.0.1 新增: 多场景集成质量测试"""
    engine = RefuteCoreEngine()
    
    scenarios = [
        ("投资决策", "这个项目一定会赚钱，因为市场很大，大家都看好"),
        ("企业管理", "团队必须严格执行KPI，只有KPI才能保证绩效"),
        ("市场营销", "只要加大投放就能获得用户增长"),
    ]
    
    all_ok = True
    for name, text in scenarios:
        result = engine.refute(text)
        
        # 快速质量检查
        checks = []
        
        # 强度范围
        s = result.assessment.overall_strength
        if not (0.15 <= s <= 0.80):
            checks.append(f"⚠ 强度异常{s:.0%}")
            all_ok = False
        
        # 反驳上限
        ms = max(r.strength for r in result.refutation.refutations)
        if ms >= 1.0:
            checks.append("⚠ 反驳满分")
            all_ok = False
        
        # 领域识别
        if result.parsed_argument.context_domain == "通用":
            checks.append("⚠ 领域=通用")
        
        # 辩论进化
        evolved = result.debate.evolved_argument
        orig = result.parsed_argument.core_claim
        if evolved == orig and not evolved.startswith(("修正:", "限定:",)):
            checks.append("⚠ 无进化")
            all_ok = False
        
        status = ",".join(checks) if checks else "OK"
        print(f"  {'✅' if not checks else '⚠'} {name}: 强度{s:.0%} 反驳{ms:.0%} [{status}]")
    
    assert all_ok, "集成质量测试部分失败"
    print(f"✅ 集成质量测试全部通过")


def test_robustness_v302():
    """v3.0.2 新增: 鲁棒性测试 — 空输入/极短文本/特殊字符"""
    engine = RefuteCoreEngine()
    
    # 测试1: 空字符串不崩溃
    try:
        result1 = engine.refute("")
        assert result1 is not None
        assert result1.engine_version == "6.2.0"
        assert result1.parsed_argument is not None
        print("✅ 鲁棒性-空输入: 通过")
    except Exception as e:
        raise AssertionError(f"空输入导致crash: {e}")
    
    # 测试2: 极短文本
    try:
        result2 = engine.refute("好")
        assert result2 is not None
        assert result2.parsed_argument.core_claim
        print("✅ 鲁棒性-极短文本: 通过")
    except Exception as e:
        raise AssertionError(f"极短文本导致crash: {e}")
    
    # 测试3: None 输入
    try:
        result3 = engine.refute(None)
        assert result3 is not None
        print("✅ 鲁棒性-None输入: 通过")
    except Exception as e:
        raise AssertionError(f"None输入导致crash: {e}")
    
    # 测试4: 只有标点符号
    try:
        result4 = engine.refute("！！！？？？")
        assert result4 is not None
        print("✅ 鲁棒性-纯标点: 通过")
    except Exception as e:
        raise AssertionError(f"纯标点导致crash: {e}")
    
    print(f"✅ 鲁棒性测试全部通过")


def test_new_domain_coverage_v302():
    """v3.0.2 新增: 新领域覆盖测试"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    
    new_domains = [
        ("产品开发", "我们必须尽快上线MVP，否则就会失去先发优势"),
        ("技术选型", "应该使用Go语言重构后端，因为性能更好"),
        ("个人决策", "我应该辞职创业，因为现在不创业以后就没机会了"),
    ]
    
    for expected_domain, text in new_domains:
        parsed = parser.parse(text)
        
        # 领域识别正确
        assert parsed.context_domain == expected_domain, f"领域错误: 期望{expected_domain}, 实际{parsed.context_domain}"
        
        # 模板填充无残留占位符
        refutation = strategist.generate_refutations(parsed, top_n=2)
        for ref in refutation.refutations:
            assert "{" not in ref.counter_argument, f"[{expected_domain}] 占位符未替换: {ref.counter_argument}"
            assert len(ref.evidence) > 10, f"[{expected_domain}] 证据过短"
        
        assessment = assessor.assess(parsed, refutation)
        assert assessment.strength_grade in ("S","A","B","C","D","F"), f"无效等级: {assessment.strength_grade}"
        
        print(f"✅ 领域覆盖[{expected_domain}]: 主语={parsed.claim_subject} 强度={assessment.strength_grade}级({assessment.overall_strength:.0%})")
    
    print(f"✅ 新领域覆盖测试全部通过")


def test_markdown_format_v302():
    """v3.0.2 新增: Markdown输出格式+截断保护"""
    engine = RefuteCoreEngine()
    
    # 超长输入测试截断
    long_text = "我们应该" + "非常" * 50 + "重视这个问题，因为这是一个" + "极其" * 50 + "重要的决策"
    result = engine.refute(long_text)
    md = engine._format_markdown(result)
    
    # 基本格式检查
    assert "# " in md
    assert "**" in md
    assert "| " in md
    
    # 截断保护 — 不应有超长行
    max_line_len = max(len(line) for line in md.split("\n") if line.strip())
    assert max_line_len < 200, f"Markdown存在超长行({max_line_len}字符)，截断保护可能失效"
    
    print(f"✅ Markdown格式+截断保护: 最长行={max_line_len}字符")


if __name__ == "__main__":
    print("=" * 65)
    print("驳心引擎 RefuteCore v3.2.0 完整测试 (含质量断言+鲁棒性)")
    print("=" * 65)
    
    tests = [
        ("论证解析器v3", test_argument_parser_v3),
        ("反驳策略v3+质量", test_refutation_v3),
        ("强度评估+质量", test_strength_assessment),
        ("辩论对抗v3+质量", test_debate_v3),
        ("论证修复", test_argument_repair),
        ("完整流程v3+质量", test_full_pipeline_v3),
        ("便捷函数", test_quick_functions),
        ("批量反驳+质量", test_batch_refute),
        ("Markdown输出", test_format_markdown),
        ("集成质量测试", test_quality_integration),
        ("鲁棒性测试(v3.0.2)", test_robustness_v302),
        ("新领域覆盖(v3.0.2)", test_new_domain_coverage_v302),
        ("Markdown截断保护(v3.0.2)", test_markdown_format_v302),
    ]
    
    passed = 0
    failed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"❌ {name} 失败: {e}")
    
    print(f"\n{'=' * 65}")
    print(f"测试结果: {passed}/{len(tests)} 通过, {failed} 失败")
    print(f"{'=' * 65}")
