# -*- coding: utf-8 -*-
"""
RefuteCore v3.0.3 全局 A/B 测试
覆盖所有 8 个模块 × 多场景 × 多输入类型，发现所有隐藏问题

测试矩阵:
  模块: ArgumentParser, RefutationStrategist, StrengthAssessor,
        DebateArena, ArgumentRepair, SolutionGenerator, BatchRefuter,
        MarkdownOutput, QuickFunctions
  场景: 商业/投资/管理/技术/个人/人际  (6领域)
  输入: 正常/空/短/长/特殊字符/无前提/强逻辑/弱逻辑 (8类型)
"""

import sys, os, traceback
sys.path.insert(0, os.path.dirname(__file__))

from refute_core import (
    RefuteCoreEngine, quick_refute, quick_refute_md, refute_and_solve, batch_refute,
    RefuteDimension, ArgumentType, FallacyType,
    ArgumentParser, ParsedArgument,
    RefutationStrategist, MultiDimensionRefutation,
    ArgumentStrengthAssessor, StrengthAssessment,
    DebateArena, DebateResult,
    ArgumentRepair, RepairedArgument,
    SolutionGenerator, SolutionSet,
    BatchRefuter, BatchResult,
)

PASS = 0
FAIL = 0
WARN = 0
results = []


def check(condition, msg, severity="FAIL"):
    global PASS, FAIL, WARN
    if condition:
        PASS += 1
        results.append(("PASS", msg))
    else:
        if severity == "FAIL":
            FAIL += 1
        else:
            WARN += 1
        results.append((severity, msg))


# ═══════════════════════════════════════════════════════════════
# A1: ArgumentParser — 6领域 × 多输入类型
# ═══════════════════════════════════════════════════════════════
def test_parser_domains():
    """A1: 论证解析器 — 领域识别覆盖度"""
    parser = ArgumentParser()
    cases = [
        ("投资理财", "应该重仓买入这只股票，因为数据表明它会涨"),
        ("企业管理", "公司必须裁掉30%员工才能提高效率"),
        ("市场营销", "只要加大投放预算就能获得更多用户"),
        ("商业竞争", "竞争对手降价了所以我们必须跟着降价"),
        ("产品开发", "应该尽快上线所有功能来抢占市场"),
        ("技术选型", "系统应该用Rust重写以获得极致性能"),
        ("个人决策", "我应该立刻辞职去追求梦想"),
        ("人际社交", "朋友之间借钱是应该的，不借不够义气"),
    ]
    for expected, text in cases:
        p = parser.parse(text)
        check(p.context_domain == expected,
              f"领域识别: '{text[:20]}' → 期望'{expected}' 实际'{p.context_domain}'")
        check(p.argument_type != ArgumentType.MIXED or p.context_domain != "通用",
              f"类型非空混: '{text[:15]}' → {p.argument_type.value}", "WARN")


def test_parser_edge_cases():
    """A2: 论证解析器 — 边界输入"""
    parser = ArgumentParser()
    
    # 空输入
    p_empty = parser.parse("")
    check(p_empty is not None, "空输入不crash")
    check(len(p_empty.core_claim) > 0, "空输入有core_claim")
    
    # None 输入
    p_none = parser.parse(None)
    check(p_none is not None, "None输入不crash")
    
    # 极短
    p_short = parser.parse("好")
    check(p_short.core_claim, "极短输入有core_claim")
    
    # 纯标点
    p_punct = parser.parse("！！！？？？")
    check(p_punct is not None, "纯标点不crash")
    
    # 超长
    long_text = "我们应该" + "非常" * 100 + "重视这个问题"
    p_long = parser.parse(long_text)
    check(p_long is not None, "超长输入不crash")
    check(len(p_long.core_claim) > 0, "超长输入有core_claim")
    
    # 无逻辑连接词的纯陈述
    p_plain = parser.parse("今天天气不错适合出门散步")
    check(p_plain.context_domain in ("通用", "个人决策"), 
          f"纯陈述领域: {p_plain.context_domain}", "WARN")
    
    # 数字和英文混合
    p_mixed = parser.parse("The ROI is 300%, 一定要投资这个Web3项目")
    check(p_mixed.context_domain == "投资理财",
          f"英文混合领域: {p_mixed.context_domain}")
    
    # 多个否定
    p_multi_neg = parser.parse("不可能不不应该不做这件事")
    check(p_multi_neg.negated_claim, f"多重否定有否定主张: {p_multi_neg.negated_claim}")


def test_parser_spo():
    """A3: 主谓宾解析质量"""
    parser = ArgumentParser()
    cases = [
        # (text, 期望主语不为停用词)
        ("竞争对手都在降价所以我们也必须降价", True),
        ("KPI考核是保证绩效的唯一手段", True),
        ("AI技术将会改变整个行业格局", True),
        ("我们必须做出正确的战略选择", True),
        ("这个项目一定会成功因为团队很好", True),
        ("投资回报率决定了是否值得投入", True),
        ("用户体验是产品的核心竞争力", True),
    ]
    stop_words = {"我们", "我", "你", "他", "她", "它", "也", "都", "不", "很", "太", "最", "是"}
    for text, expect_entity in cases:
        p = parser.parse(text)
        subject_ok = p.claim_subject not in stop_words and len(p.claim_subject) >= 2
        check(subject_ok, 
              f"SPO主语非停用词: '{text[:15]}' → '{p.claim_subject}'", 
              "WARN" if not expect_entity else "FAIL")
        check(p.claim_predicate, f"SPO有谓语: '{text[:15]}' → '{p.claim_predicate}'")
        check(p.negated_claim and len(p.negated_claim) > 2,
              f"否定主张有效: '{text[:15]}' → '{p.negated_claim[:20]}'")


def test_parser_premises():
    """A4: 前提提取"""
    parser = ArgumentParser()
    
    # 因果句有前提
    p1 = parser.parse("因为市场在增长所以我们应该扩大规模")
    check(len(p1.premises) >= 1, f"因果句有前提: {p1.premises}")
    
    # 无连接词的因果句
    p2 = parser.parse("我们应该扩大规模因为市场在快速增长")
    check(len(p2.premises) >= 1, f"无后置连接词因果句有前提: {p2.premises}")
    
    # 无前提的纯主张
    p3 = parser.parse("这个世界是公平的")
    check(p3.premises is not None, "纯主张不crash")
    
    # 多前提
    p4 = parser.parse("因为用户需求在变化，所以必须迭代产品。如果不对齐市场就会失败")
    check(len(p4.premises) >= 2, f"多前提场景: {len(p4.premises)}个 → 期望>=2")


def test_parser_weakness_detection():
    """A5: 弱点/强度指示词检测"""
    parser = ArgumentParser()
    
    p_strong = parser.parse("绝对必须一定永远所有人都必然要这样做")
    check(len(p_strong.weakness_indicators) >= 3,
          f"强绝对化文本弱点词: {p_strong.weakness_indicators}")
    check(p_strong.vulnerability_score > 0.3,
          f"绝对化脆弱性>0.3: {p_strong.vulnerability_score:.2f}")
    
    p_weak = parser.parse("可能也许大概感觉似乎不太确定")
    strength_found = any("[中]" in s or "[弱]" in s for s in p_weak.strength_indicators)
    check(strength_found, f"弱表达有[中]/[弱]标记: {p_weak.strength_indicators}", "WARN")
    
    # "不"字在不同上下文中
    p_neutral = parser.parse("不仅不同不断不如不过")
    # 这些都应该是中性的，不应该被大量计入否定
    check(p_neutral.vulnerability_score < 0.5,
          f"中性'不'词不误判: 脆弱性={p_neutral.vulnerability_score:.2f}")


# ═══════════════════════════════════════════════════════════════
# B1: RefutationStrategist — 模板填充质量
# ═══════════════════════════════════════════════════════════════
def test_refutation_template_fill():
    """B1: 反驳模板填充 — 无残留占位符"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    
    # 测试所有领域
    domain_texts = {
        "投资理财": "应该All-in这个AI项目因为市场很大",
        "企业管理": "团队必须996才能保证绩效",
        "市场营销": "只要加大投放就能获客",
        "商业竞争": "对手降价我们必须跟进",
        "产品开发": "必须尽快上线MVP抢占先发优势",
        "技术选型": "应该用Go重构后端因为性能更好",
        "个人决策": "我应该辞职创业因为不创业就没机会",
        "人际社交": "朋友之间必须两肋插刀够义气",
    }
    
    placeholder_count = 0
    for domain, text in domain_texts.items():
        parsed = parser.parse(text)
        refutation = strategist.generate_refutations(parsed, top_n=8)
        
        check(len(refutation.refutations) >= 3,
              f"[{domain}] 反驳数>=3: {len(refutation.refutations)}")
        
        for ref in refutation.refutations:
            # 检查无残留占位符
            has_placeholder = "{" in ref.counter_argument or "}" in ref.counter_argument
            if has_placeholder:
                placeholder_count += 1
            check(not has_placeholder,
                  f"[{domain}] 无残留占位符: {ref.counter_argument[:50]}")
            
            # 反驳内容非空且有意义
            check(len(ref.counter_argument) > 10,
                  f"[{domain}] 反驳内容>10字符", "WARN")
            check(ref.evidence and len(ref.evidence) > 10,
                  f"[{domain}] 证据>10字符", "WARN")
            check(ref.logical_structure and len(ref.logical_structure) > 5,
                  f"[{domain}] 逻辑链>5字符", "WARN")
        
        # 关键字段非空
        check(refutation.key_insight and len(refutation.key_insight) > 10,
              f"[{domain}] 关键洞察非空")
        check(refutation.critical_flaw and len(refutation.critical_flaw) > 5,
              f"[{domain}] 关键缺陷非空")
    
    check(placeholder_count == 0, f"所有领域0个残留占位符")


def test_refutation_strength_distribution():
    """B2: 反驳强度分布 — 不应有满分/区分度"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    
    text = "我们必须all-in AI项目因为这是未来趋势"
    parsed = parser.parse(text)
    
    # top_n=8 获取所有8个维度的反驳
    refutation = strategist.generate_refutations(parsed, top_n=8)
    strengths = [r.strength for r in refutation.refutations]
    
    check(len(strengths) >= 8, f"8维度全覆盖: {len(strengths)}")
    
    # 无满分
    check(all(s < 1.0 for s in strengths), "所有维度反驳<100%")
    
    # 有区分度 (最高-最低 >= 5%)
    if strengths:
        diff = max(strengths) - min(strengths)
        check(diff >= 0.05, f"反驳区分度>=5%: max={max(strengths):.2f} min={min(strengths):.2f} diff={diff:.2f}", "WARN")
    
    # 强度在合理范围 (0.5-0.95)
    check(all(0.5 <= s <= 0.96 for s in strengths),
          f"反驳强度在[0.5,0.96]: min={min(strengths):.2f} max={max(strengths):.2f}")
    
    # combined_strength合理
    check(0.5 <= refutation.combined_strength <= 0.95,
          f"combined_strength合理: {refutation.combined_strength:.2f}")
    
    # 维度覆盖率
    check(refutation.dimension_coverage > 0.8,
          f"维度覆盖率>80%: {refutation.dimension_coverage:.0%}")


def test_refutation_topn_consistency():
    """B3: top_n 参数一致性"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    parsed = parser.parse("应该投资这个项目因为市场很大")
    
    for n in [1, 3, 5, 8]:
        ref = strategist.generate_refutations(parsed, top_n=n)
        check(len(ref.refutations) == n,
              f"top_n={n} 返回{n}个反驳: 实际{len(ref.refutations)}")
        # strongest 应该始终是 refutations 中的第一个（已排序）
        check(ref.strongest_refutation == ref.refutations[0],
              f"top_n={n} strongest是第一个")
        check(ref.strongest_refutation.strength >= 0.5,
              f"top_n={n} strongest>=0.5: {ref.strongest_refutation.strength:.2f}")


def test_refutation_focus_dimensions():
    """B4: focus_dimensions 参数"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    parsed = parser.parse("应该投资这个项目因为市场很大")
    
    focus = [RefuteDimension.REFUTATION, RefuteDimension.BEHAVIORAL]
    ref = strategist.generate_refutations(parsed, top_n=5, focus_dimensions=focus)
    
    dims_returned = set(r.dimension for r in ref.refutations)
    check(dims_returned == set(focus),
          f"focus维度: 期望{[d.value for d in focus]} 实际{[d.value for d in dims_returned]}")


# ═══════════════════════════════════════════════════════════════
# C1: StrengthAssessor — 评分合理性
# ═══════════════════════════════════════════════════════════════
def test_strength_assessment():
    """C1: 强度评估 — 评分分布合理性"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    
    # 弱论证（绝对化+无数据+无前提）
    weak_parsed = parser.parse("这个项目一定会赚钱因为感觉很好")
    weak_ref = strategist.generate_refutations(weak_parsed, top_n=3)
    weak_assess = assessor.assess(weak_parsed, weak_ref)
    
    check(0.10 <= weak_assess.overall_strength <= 0.75,
          f"弱论证强度合理: {weak_assess.overall_strength:.2f} ({weak_assess.strength_grade})")
    check(weak_assess.strength_grade in ("C", "D", "F"),
          f"弱论证等级低: {weak_assess.strength_grade}", "WARN")
    check(len(weak_assess.vulnerabilities) > 0, "弱论证有脆弱点")
    
    # 强论证（有数据+多前提）
    strong_parsed = parser.parse("根据2024年第三季度财报数据，企业营收同比增长23%，利润率提升5个百分点")
    strong_ref = strategist.generate_refutations(strong_parsed, top_n=3)
    strong_assess = assessor.assess(strong_parsed, strong_ref)
    
    check(0.15 <= strong_assess.overall_strength <= 0.90,
          f"强论证强度合理: {strong_assess.overall_strength:.2f} ({strong_assess.strength_grade})")
    
    # 子项评分范围
    for name, value in [("前提", weak_assess.premise_strength), ("推理", weak_assess.reasoning_strength),
                        ("证据", weak_assess.evidence_strength), ("假设", weak_assess.assumption_strength)]:
        check(0.05 <= value <= 1.0, f"{name}强度范围: {value:.2f}")
    
    # 所有有效等级
    all_grades = set()
    test_texts = [
        "一定必然",  # 极弱
        "感觉可能也许",  # 弱
        "数据显示增长",  # 中等
        "因为研究表明",  # 中等偏上
    ]
    for t in test_texts:
        p = parser.parse(t)
        r = strategist.generate_refutations(p, top_n=3)
        a = assessor.assess(p, r)
        all_grades.add(a.strength_grade)
    
    check(len(all_grades) >= 2, f"有区分度: 使用了{len(all_grades)}个等级 {all_grades}", "WARN")


def test_assessment_improvements():
    """C2: 改进建议质量"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    
    p = parser.parse("所有互联网公司都必然会失败因为大家都在亏钱")
    r = strategist.generate_refutations(p, top_n=3)
    a = assessor.assess(p, r)
    
    check(len(a.improvement_suggestions) > 0, "有改进建议")
    check(len(a.detected_fallacies) > 0, "检测到谬误（有绝对化+以偏概全）")
    
    # 改进建议不空
    for imp in a.improvement_suggestions:
        check(len(imp) > 5, f"改进建议非空: {imp[:30]}")


# ═══════════════════════════════════════════════════════════════
# D1: DebateArena — 辩论流程
# ═══════════════════════════════════════════════════════════════
def test_debate_flow():
    """D1: 辩论流程完整性"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    arena = DebateArena()
    
    p = parser.parse("公司应该实行996工作制因为竞争激烈")
    r = strategist.generate_refutations(p, top_n=3)
    a = assessor.assess(p, r)
    d = arena.debate(p, r, a)
    
    check(len(d.rounds) == 3, f"辩论3轮: {len(d.rounds)}")
    check(d.final_verdict, "最终裁决非空")
    check(0 <= d.truth_approximation <= 1, f"逼近度范围: {d.truth_approximation:.2f}")
    check(d.evolved_argument, "进化论点非空")
    
    # 每轮完整性
    for rnd in d.rounds:
        check(rnd.proposer_argument, f"R{rnd.round_number}正方非空")
        check(rnd.refuter_counter, f"R{rnd.round_number}反方非空")
        check(rnd.proposer_defense, f"R{rnd.round_number}防御非空")
        check(rnd.round_verdict, f"R{rnd.round_number}裁决非空")
    
    # 进化论点应有变化
    evolved = d.evolved_argument
    orig = p.core_claim
    is_evolved = (
        evolved != orig or
        evolved.startswith(("修正:", "限定:", "最终版:", "'")) or
        "在理想情况下" in evolved or
        "从概率角度" in evolved or
        "限定版" in evolved
    )
    check(is_evolved, f"论点有进化: '{orig[:20]}' → '{evolved[:30]}'", "WARN")


def test_debate_verdict_variety():
    """D2: 裁决多样性"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    arena = DebateArena()
    
    verdicts = set()
    test_texts = [
        "一定会成功因为市场很大",  # 弱 → 反方胜
        "数据显示第三季度增长23%",  # 强 → 正方守住
    ]
    for text in test_texts:
        p = parser.parse(text)
        r = strategist.generate_refutations(p, top_n=3)
        a = assessor.assess(p, r)
        d = arena.debate(p, r, a)
        for rnd in d.rounds:
            # 提取裁决核心（去掉轮次编号）
            verdict_core = rnd.round_verdict.split(")", 1)[-1].strip() if ")" in rnd.round_verdict else rnd.round_verdict
            verdicts.add(verdict_core[:10])
    
    check(len(verdicts) >= 2, f"裁决多样性: {len(verdicts)}种裁决", "WARN")


# ═══════════════════════════════════════════════════════════════
# E1: ArgumentRepair — 修复质量
# ═══════════════════════════════════════════════════════════════
def test_repair_quality():
    """E1: 论证修复质量"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    arena = DebateArena()
    repair = ArgumentRepair()
    
    # 弱论证修复
    p = parser.parse("一定必须投资这个项目因为感觉很好")
    r = strategist.generate_refutations(p, top_n=3)
    a = assessor.assess(p, r)
    d = arena.debate(p, r, a)
    rep = repair.repair(p, r, a, d)
    
    check(rep.repaired_claim, "修复后主张非空")
    check(rep.repair_rationale, "修复理由非空")
    check(rep.repaired_strength_estimate >= 0.05, 
          f"修复后强度>=5%: {rep.repaired_strength_estimate:.2f}")
    
    # 绝对化表述应被软化
    softened = rep.repaired_claim
    has_absolutism = any(w in softened for w in ["一定", "必然", "绝对", "不可能", "所有人"])
    check(not has_absolutism, f"绝对化被软化: 修复后含'{[w for w in ['一定','必然','绝对','不可能','所有人'] if w in softened]}'", "WARN")


# ═══════════════════════════════════════════════════════════════
# F1: SolutionGenerator — 解决方案质量
# ═══════════════════════════════════════════════════════════════
def test_solutions_quality():
    """F1: 解决方案生成"""
    parser = ArgumentParser()
    strategist = RefutationStrategist()
    assessor = ArgumentStrengthAssessor()
    arena = DebateArena()
    repair = ArgumentRepair()
    solver = SolutionGenerator()
    
    p = parser.parse("应该All-in这个AI项目因为AI是未来")
    r = strategist.generate_refutations(p, top_n=3)
    a = assessor.assess(p, r)
    d = arena.debate(p, r, a)
    rep = repair.repair(p, r, a, d)
    solutions = solver.generate(p, r, a, d, rep)
    
    check(len(solutions.solutions) >= 3, f"方案数>=3: {len(solutions.solutions)}")
    check(solutions.overall_assessment, "总体评估非空")
    check(solutions.recommended_approach, "推荐方案非空")
    
    for s in solutions.solutions:
        check(s.title, "方案标题非空")
        check(s.description, "方案描述非空")
        check(len(s.actions) > 0, f"方案'{s.title}'有行动项")
        check(s.expected_improvement > 0, f"方案'{s.title}'有预期改善")
    
    # quick_wins 和 deep_fixes
    check(len(solutions.quick_wins) > 0, "有quick_wins")
    check(len(solutions.deep_fixes) > 0, "有deep_fixes")


# ═══════════════════════════════════════════════════════════════
# G1: BatchRefuter — 批量反驳
# ═══════════════════════════════════════════════════════════════
def test_batch_contradiction_detection():
    """G1: 批量矛盾检测"""
    engine = RefuteCoreEngine()
    
    # 明显矛盾的论点集
    contradicting = [
        "我们应该降价应对竞争",
        "我们不应该降价因为降价损害品牌",
        "降价是短期获取市场份额的最佳策略",
        "降价会引发价格战导致两败俱伤",
    ]
    batch = engine.batch_refute(contradicting)
    
    check(len(batch.individual_results) == 4, f"批量4个结果: {len(batch.individual_results)}")
    check(len(batch.contradictions) >= 1, f"检测到矛盾: {len(batch.contradictions)}")
    check(batch.consistency_score < 1.0, f"一致性<100%: {batch.consistency_score:.0%}")
    check(0 <= batch.strongest_argument_index < 4, "最强论点索引有效")
    check(0 <= batch.weakest_argument_index < 4, "最弱论点索引有效")
    check(batch.overall_assessment, "总体评估非空")
    
    # 一致的论点集
    consistent = [
        "投资需要分散风险",
        "不要把所有鸡蛋放在一个篮子里",
        "多元化投资组合更安全",
    ]
    batch2 = engine.batch_refute(consistent)
    check(batch2.consistency_score > 0.5,
          f"一致集一致性>50%: {batch2.consistency_score:.0%}", "WARN")


def test_batch_single_argument():
    """G2: 单个论点批量"""
    engine = RefuteCoreEngine()
    batch = engine.batch_refute(["这个项目一定会成功"])
    check(len(batch.individual_results) == 1, "单个论点批量结果1个")
    check(len(batch.contradictions) == 0, "单论点无矛盾")
    check(batch.consistency_score == 1.0, f"单论点一致性100%: {batch.consistency_score:.0%}")


# ═══════════════════════════════════════════════════════════════
# H1: Markdown 输出
# ═══════════════════════════════════════════════════════════════
def test_markdown_output():
    """H1: Markdown输出格式"""
    engine = RefuteCoreEngine()
    result = engine.refute("应该All-in这个AI项目因为AI是未来趋势")
    md = engine._format_markdown(result)
    
    # 基本格式
    check("# " in md, "Markdown有标题")
    check("## " in md, "Markdown有二级标题")
    check("| " in md, "Markdown有表格")
    check("**" in md, "Markdown有加粗")
    check("反驳结果" in md, "有反驳结果节")
    check("强度评估" in md, "有强度评估节")
    check("辩论结果" in md, "有辩论结果节")
    check("论证修复" in md, "有修复节")
    check("核心结论" in md, "有结论节")
    
    # 截断保护
    max_line = max(len(line) for line in md.split("\n") if line.strip())
    check(max_line < 250, f"Markdown最长行={max_line}字符 < 250")


# ═══════════════════════════════════════════════════════════════
# I1: 便捷函数
# ═══════════════════════════════════════════════════════════════
def test_quick_functions():
    """I1: 便捷函数"""
    text_out = quick_refute("应该投资这个项目")
    check(isinstance(text_out, str), "quick_refute返回字符串")
    check("驳心引擎" in text_out, "quick_refute包含引擎名")
    
    md_out = quick_refute_md("应该投资这个项目")
    check(isinstance(md_out, str), "quick_refute_md返回字符串")
    check("# " in md_out, "quick_refute_md是Markdown")
    
    result = refute_and_solve("应该投资这个项目")
    check(hasattr(result, 'assessment'), "refute_and_solve有assessment")
    check(hasattr(result, 'repair'), "refute_and_solve有repair")
    check(hasattr(result, 'debate'), "refute_and_solve有debate")
    check(result.engine_version == "6.2.0", "refute_and_solve版本正确")
    
    batch = batch_refute(["应该做A", "不应该做A"])
    check(len(batch.individual_results) == 2, "batch_refute返回2个结果")


# ═══════════════════════════════════════════════════════════════
# J1: 完整端到端
# ═══════════════════════════════════════════════════════════════
def test_end_to_end():
    """J1: 端到端 — 6个真实场景"""
    engine = RefuteCoreEngine()
    scenarios = [
        "应该All-in这个AI项目因为AI是未来趋势，不抓住机会就会被淘汰",
        "公司必须实行996工作制，因为只有拼命加班才能在竞争中活下去",
        "这个产品一定会成功因为我们团队最优秀",
        "应该辞职去创业，因为打工永远不可能实现财富自由",
        "只要花钱投广告就能获得用户增长",
        "降价是最有效的竞争策略，因为消费者只看价格",
    ]
    
    for i, text in enumerate(scenarios, 1):
        result = engine.refute(text)
        
        # 基本完整性
        check(result.engine_version == "6.2.0", f"E2E#{i}版本正确")
        check(result.parsed_argument is not None, f"E2E#{i}解析非空")
        check(len(result.refutation.refutations) >= 3, f"E2E#{i}反驳>=3")
        check(result.assessment.strength_grade in ("S","A","B","C","D","F"), f"E2E#{i}等级有效")
        check(len(result.debate.rounds) == 3, f"E2E#{i}辩论3轮")
        check(result.repair.repaired_claim, f"E2E#{i}修复非空")
        check(len(result.solutions.solutions) >= 3, f"E2E#{i}方案>=3")
        check(result.executive_summary, f"E2E#{i}摘要非空")
        check(result.risk_level, f"E2E#{i}风险非空")
        check(result.key_takeaway, f"E2E#{i}结论非空")
        
        # 质量断言
        s = result.assessment.overall_strength
        check(0.10 <= s <= 0.85, f"E2E#{i}强度合理: {s:.0%}", "WARN")
        max_ref = max(r.strength for r in result.refutation.refutations)
        check(max_ref < 1.0, f"E2E#{i}反驳<100%: {max_ref:.0%}")


def test_hedge_claim_determinism():
    """J2: _hedge_claim 确定性（v3.0.3修复验证）"""
    engine = RefuteCoreEngine()
    arena = engine.arena
    
    # 同一论点多次调用应返回相同结果
    from refute_core import ParsedArgument, ArgumentType
    p = ParsedArgument(
        raw_text="应该投资AI项目", argument_type=ArgumentType.DECISION,
        core_claim="应该投资AI项目", premises=[], reasoning_chain=[],
        implicit_assumptions=[], evidence_type="无明确证据", confidence_level=0.5,
        dimension_affinity={}, keywords=[], vulnerability_score=0.3,
        claim_subject="AI项目", claim_predicate="应该", claim_object="投资",
        negated_claim="不应该投资AI项目", context_domain="投资理财",
        strength_indicators=[], weakness_indicators=["应该"]
    )
    
    results = [arena._hedge_claim("应该投资AI项目", p) for _ in range(10)]
    check(len(set(results)) == 1, f"_hedge_claim确定性: 10次调用={set(results)}")


def test_detect_attitude_correctness():
    """J3: _detect_attitude 正确性"""
    engine = RefuteCoreEngine()
    detector = engine.batch_refuter
    
    # 明确支持
    att_pos = detector._detect_attitude("应该必须值得有效成功好重要")
    check(att_pos == "支持", f"支持检测: {att_pos}")
    
    # 明确反对
    att_neg = detector._detect_attitude("不应该不能损害风险失败坏问题缺陷")
    check(att_neg == "反对", f"反对检测: {att_neg}")
    
    # 中性
    att_neutral = detector._detect_attitude("这个问题需要考虑")
    check(att_neutral == "neutral", f"中性检测: {att_neutral}", "WARN")
    
    # "不同""不仅""不断" 不应触发否定
    att_falseneg = detector._detect_attitude("不仅不同不断变化的市场环境")
    check(att_falseneg != "反对", f"假阴性防护: '{att_falseneg}' 不应判为反对")


def test_are_contradictory():
    """J4: _are_contradictory 矛盾检测"""
    engine = RefuteCoreEngine()
    checker = engine.batch_refuter
    
    check(checker._are_contradictory("假设确定成立", "假设不确定"), "确定vs不确定: True")
    check(checker._are_contradictory("假设理性决策", "假设非理性"), "理性vs非理性: True")
    check(not checker._are_contradictory("假设A成立", "假设B成立"), "无关假设: False")


# ═══════════════════════════════════════════════════════════════
# 运行全部测试
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 70)
    print("RefuteCore v3.2.0 全局 A/B 测试")
    print("=" * 70)
    
    test_groups = [
        ("A1: 领域识别覆盖", test_parser_domains),
        ("A2: 边界输入", test_parser_edge_cases),
        ("A3: 主谓宾解析", test_parser_spo),
        ("A4: 前提提取", test_parser_premises),
        ("A5: 弱点检测", test_parser_weakness_detection),
        ("B1: 模板填充", test_refutation_template_fill),
        ("B2: 强度分布", test_refutation_strength_distribution),
        ("B3: top_n一致性", test_refutation_topn_consistency),
        ("B4: focus维度", test_refutation_focus_dimensions),
        ("C1: 评分合理性", test_strength_assessment),
        ("C2: 改进建议", test_assessment_improvements),
        ("D1: 辩论流程", test_debate_flow),
        ("D2: 裁决多样性", test_debate_verdict_variety),
        ("E1: 修复质量", test_repair_quality),
        ("F1: 解决方案", test_solutions_quality),
        ("G1: 批量矛盾", test_batch_contradiction_detection),
        ("G2: 单论点批量", test_batch_single_argument),
        ("H1: Markdown输出", test_markdown_output),
        ("I1: 便捷函数", test_quick_functions),
        ("J1: 端到端", test_end_to_end),
        ("J2: 确定性", test_hedge_claim_determinism),
        ("J3: 态度检测", test_detect_attitude_correctness),
        ("J4: 矛盾检测", test_are_contradictory),
    ]
    
    group_results = {}
    for name, test_fn in test_groups:
        try:
            test_fn()
            group_results[name] = "✅"
        except Exception as e:
            FAIL += 1
            group_results[name] = f"❌ CRASH: {e}"
            results.append(("CRASH", f"{name}: {e}"))
            traceback.print_exc()
    
    # 输出结果
    print(f"\n{'=' * 70}")
    print(f"测试结果: {PASS} PASS / {FAIL} FAIL / {WARN} WARN (共{PASS+FAIL+WARN}项)")
    print(f"{'=' * 70}")
    
    # 分组结果
    print(f"\n{'─' * 70}")
    print("分组结果:")
    print(f"{'─' * 70}")
    for name, status in group_results.items():
        print(f"  {status}  {name}")
    
    # FAIL列表
    fails = [r for r in results if r[0] in ("FAIL", "CRASH")]
    warns = [r for r in results if r[0] == "WARN"]
    
    if fails:
        print(f"\n{'─' * 70}")
        print(f"❌ FAIL 列表 ({len(fails)}项):")
        print(f"{'─' * 70}")
        for severity, msg in fails:
            print(f"  [{severity}] {msg}")
    
    if warns:
        print(f"\n{'─' * 70}")
        print(f"⚠️ WARN 列表 ({len(warns)}项):")
        print(f"{'─' * 70}")
        for severity, msg in warns:
            print(f"  [{severity}] {msg}")
    
    if not fails:
        print(f"\n{'─' * 70}")
        print(f"🎉 全部通过! {PASS} PASS")
        print(f"{'─' * 70}")
    
    print(f"\n{'=' * 70}")
    print(f"最终: {PASS} PASS / {FAIL} FAIL / {WARN} WARN")
    print(f"{'=' * 70}")
