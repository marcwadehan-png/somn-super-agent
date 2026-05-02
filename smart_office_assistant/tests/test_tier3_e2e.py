# -*- coding: utf-8 -*-
"""
三级神经网络调度器 - 端到端使用测试
=========================================

模拟真实场景：用户提交自然语言任务 → 系统自动路由 →
三级神经网络调度 → 多引擎协作分析 → 最终策略输出

测试重点：
1. 自然语言问题的域识别
2. P1/P2/P3 三层引擎的随机序列调度
3. 策略融合与可行性论证
4. 最终策略输出质量

入口: python tests/test_tier3_e2e.py
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)
sys.stdout.reconfigure(encoding="utf-8")


# ===================== 第0步：导入 =====================
from src.intelligence.tier3_neural_scheduler import (
    Tier3NeuralScheduler,
    Tier3Query,
    Tier3Result,
    TierSelection,
    EngineTier,
    tier3_analyze,
    get_tier3_scheduler,
)

from src.intelligence.global_wisdom_scheduler import (
    tier3_wisdom_analyze,
    tier3_quick,
    tier3_full_report,
)
from src.intelligence.unified_intelligence_coordinator import (
    UnifiedIntelligenceCoordinator,
    TaskType,
)


class StubROITracker:
    """端到端测试用的ROI桩对象。"""

    def __init__(self, strategy_scores=None, workflow_scores=None, combo_scores=None):
        self.strategy_scores = strategy_scores or {}
        self.workflow_scores = workflow_scores or {}
        self.combo_scores = combo_scores or {}

    def get_strategy_roi(self, strategy):
        return self.strategy_scores.get(strategy, {"status": "no_data"})

    def get_workflow_roi(self, workflow_id):
        return self.workflow_scores.get(workflow_id, {"status": "no_data"})

    def get_strategy_combo_roi(self, strategy_combo_id="", strategy_combo=None):
        combo_key = tuple(sorted(strategy_combo or []))
        return self.combo_scores.get(combo_key, {
            "status": "no_data",
            "strategy_combo_id": strategy_combo_id,
            "strategy_combo": list(combo_key),
        })


# ===================== 工具函数 =====================

def print_sep(char="=", width=80):
    print(f"\n{char * width}\n")

def print_section(title):
    print_sep("=")
    print(f"  {title}")
    print_sep("=")

def print_sub(title):
    print_sep("-")
    print(f"  {title}")
    print_sep("-")

def print_result(tier_name, outputs, max_show=2):
    print(f"\n【{tier_name}】共 {len(outputs)} 个引擎:")
    for i, o in enumerate(outputs, 1):
        print(f"  {i}. [{o.engine_id}]")
        if o.strategy_content:
            content = str(o.strategy_content)[:120].replace('\n', ' ')
            print(f"     → {content}...")
    if len(outputs) > max_show:
        print(f"  ... 其余 {len(outputs) - max_show} 个引擎输出省略")

def print_fusion(title, fusion_data, indent=2):
    prefix = " " * indent
    print(f"\n{prefix}【{title}】")
    if isinstance(fusion_data, dict):
        for key, value in fusion_data.items():
            if isinstance(value, list):
                print(f"{prefix}  • {key}: {len(value)} 项")
                for v in value[:3]:
                    print(f"{prefix}    - {str(v)[:80]}...")
            elif isinstance(value, str):
                print(f"{prefix}  • {key}: {value[:80]}...")
            elif isinstance(value, (int, float)):
                print(f"{prefix}  • {key}: {value}")
            else:
                print(f"{prefix}  • {key}: {str(value)[:60]}...")
    else:
        print(f"{prefix}  {str(fusion_data)[:200]}")

def print_full_strategy(result: Tier3Result):
    print_sep("=")
    print("  最终策略输出")
    print_sep("=")
    print(f"\n决策置信度: {result.decision_confidence:.1%}")
    print(f"协同度: {result.synergy_score:.2f}  |  层级平衡: {result.tier_balance:.2f}  |  域覆盖: {result.coverage:.2f}")
    print(f"执行引擎: P1={len(result.p1_outputs)} / P3={len(result.p3_outputs)} / P2={len(result.p2_outputs)}")
    print(f"总耗时: {result.processing_time:.2f}s")

    print(f"\n{'─' * 60}")
    print("【最终策略】")
    print(f"{'─' * 60}")
    print(result.final_strategy)

    if result.key_insights:
        print(f"\n{'─' * 60}")
        print("【关键洞察】")
        print(f"{'─' * 60}")
        for i, ins in enumerate(result.key_insights, 1):
            print(f"  {i}. {ins}")

    if result.risk_warnings:
        print(f"\n{'─' * 60}")
        print("【风险预警】")
        print(f"{'─' * 60}")
        for w in result.risk_warnings:
            print(f"  ⚠ {w}")


# ===================== 场景定义 =====================
SCENARIOS = [
    {
        "id": 1,
        "title": "企业生死突围",
        "query": "公司连续亏损6个月，账上现金流只够维持3个月，员工士气低落，大客户被竞对挖走，如何绝地反击？",
        "seed": 42,
        "context": {"urgency": "critical", "role": "CEO"},
    },
    {
        "id": 2,
        "title": "个人成长抉择",
        "query": "30岁面临人生重大选择：接受大厂高P offer稳定但天花板明显，创业团队更有成长性但风险极高，该如何决策？",
        "seed": 123,
        "context": {"urgency": "high", "role": "个人"},
    },
    {
        "id": 3,
        "title": "团队文化重建",
        "query": "团队扩张3倍后文化稀释严重，老员工抱怨新人不靠谱，新人觉得老员工守旧，创新氛围消失，如何重建？",
        "seed": 777,
        "context": {"urgency": "medium", "role": "CTO"},
    },
]


# ===================== 测试函数 =====================
def test_scenario(scenario: dict, use_coordinator: bool = False):
    """运行单个场景的端到端测试"""
    print_section(f"场景 {scenario['id']}: {scenario['title']}")

    print(f"\n📥 用户输入:")
    print(f"   \"{scenario['query']}\"")
    print(f"   [context: {scenario['context']}] [seed: {scenario['seed']}]")

    # ========== 第1步：域识别 ==========
    print_sub("第1步: 域识别")

    scheduler = get_tier3_scheduler()
    domains = scheduler.domain_matcher.extract_domains(scenario['query'])
    print(f"   识别到问题域 ({len(domains)}个): {domains}")

    # ========== 第2步：引擎调度 ==========
    print_sub("第2步: 三级神经网络调度")

    t0 = time.time()
    if use_coordinator:
        result = tier3_wisdom_analyze(
            query_text=scenario['query'],
            context=scenario['context'],
            p1_count=6, p3_count=4, p2_count=4,
            random_seed=scenario['seed'],
        )
    else:
        result = tier3_analyze(
            query_text=scenario['query'],
            context=scenario['context'],
            p1_count=6, p3_count=4, p2_count=4,
            random_seed=scenario['seed'],
        )
    elapsed = time.time() - t0

    print(f"   P1引擎 ({len(result.p1_outputs)}个): {[o.engine_id for o in result.p1_outputs]}")
    print(f"   P3引擎 ({len(result.p3_outputs)}个): {[o.engine_id for o in result.p3_outputs]}")
    print(f"   P2引擎 ({len(result.p2_outputs)}个): {[o.engine_id for o in result.p2_outputs]}")
    print(f"   执行耗时: {elapsed:.2f}s")

    # ========== 第3步：各层输出展示 ==========
    print_sub("第3步: 各层引擎输出")
    print_result("P1 核心策略", result.p1_outputs)
    print_result("P3 可行性论证", result.p3_outputs)
    print_result("P2 多元视角", result.p2_outputs)

    # ========== 第4步：融合结果 ==========
    print_sub("第4步: 三层融合结果")
    print_fusion("P1策略融合", result.fused_strategy)
    print_fusion("P3可行性报告", result.feasibility_report)
    print_fusion("P2视角综合", result.perspective_synthesis)

    # ========== 第5步：最终策略 ==========
    print_full_strategy(result)

    # ========== 质量评估 ==========
    print_sep("=")
    print(f"  质量评估 | 置信度={result.decision_confidence:.1%} | 协同={result.synergy_score:.2f} | 平衡={result.tier_balance:.2f} | 覆盖={result.coverage:.2f}")
    status = "✅ 优秀" if result.decision_confidence > 0.7 and result.synergy_score > 0.5 else "⚠️ 一般" if result.decision_confidence > 0.5 else "❌ 需优化"
    print(f"  综合评定: {status}")
    print_sep("=")

    return result


def test_programmatic():
    """测试程序化调用接口"""
    print_section("程序化调用接口演示")

    print("\n【接口1: tier3_quick - 快速策略提取】")
    quick = tier3_quick(
        "公司面临生死危机，如何绝地反击？",
        p1_count=6, p3_count=4, p2_count=4,
        random_seed=42
    )
    print(f"返回类型: {type(quick).__name__}")
    print(f"内容预览: {quick[:150]}...")

    print("\n【接口2: tier3_full_report - 完整报告字典】")
    report = tier3_full_report(
        "公司面临生死危机，如何绝地反击？",
        random_seed=42
    )
    print(f"返回字段: {list(report.keys())}")
    print(f"  - p1_engines: {report['p1_engines']}")
    print(f"  - decision_confidence: {report['decision_confidence']:.2f}")
    print(f"  - tier_balance: {report['tier_balance']:.2f}")

    print("\n【接口3: 通过 UnifiedIntelligenceCoordinator 调用】")
    coord = UnifiedIntelligenceCoordinator()
    task_result = coord.execute_task(
        task_type=TaskType.TIER3_ANALYSIS,
        input_data={
            "problem": "个人成长和自我提升的方法",
            "p1_count": 6,
            "p3_count": 4,
            "p2_count": 4,
            "random_seed": 42,
        }
    )
    print(f"   success: {task_result.success}")
    print(f"   confidence: {task_result.confidence:.2f}")
    print(f"   modules_used ({len(task_result.modules_used)}个): {task_result.modules_used}")


def test_randomness():
    """测试随机序列特性"""
    print_section("随机序列特性验证")

    query = "如何在竞争中保持战略优势，同时维护团队和谐？"

    print(f"\n查询: \"{query}\"")

    results = {}
    seeds = [1, 42, 99, 2026, 8888]
    for seed in seeds:
        r = tier3_analyze(query, random_seed=seed)
        p1_ids = tuple(o.engine_id for o in r.p1_outputs)
        results[seed] = p1_ids
        print(f"  seed={seed}: {list(p1_ids)}")

    # 验证不同seed产生不同组合
    unique_combos = set(results.values())
    print(f"\n  不同组合数: {len(unique_combos)}/{len(seeds)}")
    print(f"  随机多样性: {'✅ 良好' if len(unique_combos) > len(seeds)*0.6 else '⚠️ 需注意'}")

    # 验证相同seed可复现
    r1 = tier3_analyze(query, random_seed=42)
    r2 = tier3_analyze(query, random_seed=42)
    p1_r1 = [o.engine_id for o in r1.p1_outputs]
    p1_r2 = [o.engine_id for o in r2.p1_outputs]
    print(f"\n  seed=42 第一次: {p1_r1}")
    print(f"  seed=42 第二次: {p1_r2}")
    print(f"  可复现性: {'✅ 完全一致' if p1_r1 == p1_r2 else '❌ 不一致'}")


def test_quality_metrics():
    """测试质量指标计算"""
    print_section("质量指标计算验证")

    scheduler = get_tier3_scheduler()

    query = "企业面临生死危机，如何绝地反击？"
    result = tier3_analyze(query, random_seed=42)

    print(f"\n【指标计算验证】")
    print(f"  决策置信度: {result.decision_confidence:.3f}")
    print(f"  协同度: {result.synergy_score:.3f}")
    print(f"  层级平衡: {result.tier_balance:.3f}")
    print(f"  域覆盖度: {result.coverage:.3f}")
    print(f"  执行时间: {result.processing_time:.3f}s")

    # 统计各引擎覆盖
    all_outputs = result.p1_outputs + result.p3_outputs + result.p2_outputs
    covered_engines = [o.engine_id for o in all_outputs]
    print(f"\n  引擎总数: {len(covered_engines)}")
    print(f"  引擎列表: {covered_engines}")

    # 验证p1层有策略内容
    p1_with_strategy = [o for o in result.p1_outputs if o.strategy_content]
    print(f"\n  P1层有策略内容: {len(p1_with_strategy)}/{len(result.p1_outputs)}")

    # 验证p3层有论证内容
    p3_with_论证 = [o for o in result.p3_outputs if o.论证_content]
    print(f"  P3层有论证内容: {len(p3_with_论证)}/{len(result.p3_outputs)}")

    # 验证p2层有多元视角
    p2_with_perspective = [o for o in result.p2_outputs if o.perspective_content]
    print(f"  P2层有多元视角: {len(p2_with_perspective)}/{len(result.p2_outputs)}")


def test_context_awareness():
    """测试上下文感知能力"""
    print_section("上下文感知能力")

    base_query = "如何提升团队绩效？"

    contexts = [
        {"urgency": "high", "role": "CEO"},
        {"urgency": "medium", "role": "CTO"},
        {"urgency": "low", "role": "TeamLead"},
    ]

    for ctx in contexts:
        r = tier3_analyze(base_query, context=ctx, random_seed=42)
        print(f"\n  [context: {ctx}]")
        print(f"    P1: {[o.engine_id for o in r.p1_outputs[:3]]}")
        print(f"    置信度: {r.decision_confidence:.2f}")


def test_roi_guided_selection_path():
    """验证调度层会沿 workflow/combo ROI 做连续选择。"""
    print_section("ROI驱动的连续选择路径")

    scheduler = Tier3NeuralScheduler()
    scheduler.p1_pool = {
        "ALPHA": {"weight": 0.6, "domains": ["growth"]},
        "BETA": {"weight": 0.05, "domains": ["culture"]},
    }
    scheduler.p2_pool = {
        "ALPHA_P2": {"weight": 0.6, "domains": ["finance"]},
        "BETA_P2": {"weight": 0.05, "domains": ["myth"]},
    }

    scheduler._roi_tracker = StubROITracker(
        strategy_scores={
            "ALPHA": {"status": "ok", "avg_efficiency_score": 0.96, "sample_count": 18, "confidence": 0.92},
            "BETA": {"status": "ok", "avg_efficiency_score": 0.2, "sample_count": 3, "confidence": 0.15},
            "ALPHA_P2": {"status": "ok", "avg_efficiency_score": 0.8, "sample_count": 10, "confidence": 0.86},
            "BETA_P2": {"status": "ok", "avg_efficiency_score": 0.25, "sample_count": 4, "confidence": 0.22},
        },
        workflow_scores={
            "wf::roi-path::P1::ALPHA": {"status": "ok", "avg_efficiency_score": 0.9, "confidence": 0.88},
            "wf::roi-path::P2::ALPHA_P2": {"status": "ok", "avg_efficiency_score": 0.82, "confidence": 0.8},
        },
        combo_scores={
            tuple(sorted(["ALPHA", "ALPHA_P2"])): {"status": "ok", "avg_efficiency_score": 0.97, "confidence": 0.91},
            tuple(sorted(["ALPHA", "BETA_P2"])): {"status": "ok", "avg_efficiency_score": 0.18, "confidence": 0.2},
        }
    )
    scheduler._roi_tracker_init_attempted = True

    query = Tier3Query(
        query_id="roi-path",
        query_text="增长竞争战略",
        context={"workflow_reference_id": "wf::roi-path", "role": "CEO", "urgency": "high"},
        p1_count=1,
        p2_count=1,
        random_seed=42,
    )
    domains = {"增长": 1.0, "竞争": 0.9}
    p1_selected = scheduler._select_p1_engines(query, domains, random.Random(42))
    p2_selected = scheduler._select_p2_engines(query, domains, random.Random(42), p1_selected)

    print(f"  P1选择: {[item.engine_id for item in p1_selected]}")
    print(f"  P2选择: {[item.engine_id for item in p2_selected]}")
    print(f"  P2理由: {p2_selected[0].reason}")

    assert p1_selected[0].engine_id == "ALPHA", "P1应优先选择高历史ROI引擎"
    assert p2_selected[0].engine_id == "ALPHA_P2", "P2应沿高combo ROI路径继续补充"
    assert "comboROI(0.97)" in p2_selected[0].reason, "P2理由中应暴露combo ROI信号"


def test_workflow_reference_stability():
    """验证显式与自动工作流参考ID都可稳定复用。"""
    print_section("工作流参考ID稳定性")

    scheduler = Tier3NeuralScheduler()
    explicit_query = Tier3Query(query_id="explicit", query_text="增长战略", context={"workflow_reference_id": "wf::stable"})
    auto_query = Tier3Query(query_id="auto", query_text="增长战略", context={"role": "CEO", "urgency": "high"})

    explicit_ref = scheduler._build_workflow_reference_base(explicit_query, {"增长": 1.0})
    auto_ref_1 = scheduler._build_workflow_reference_base(auto_query, {"增长": 1.0, "竞争": 0.8})
    auto_ref_2 = scheduler._build_workflow_reference_base(auto_query, {"增长": 1.0, "竞争": 0.8})

    print(f"  显式reference: {explicit_ref}")
    print(f"  自动reference: {auto_ref_1}")

    assert explicit_ref == "wf::stable", "显式workflow_reference_id应原样透传"
    assert auto_ref_1 == auto_ref_2, "相同输入应得到稳定的自动reference"
    assert auto_ref_1.startswith("tier3wf::"), "自动reference格式应以tier3wf开头"


# ===================== 主入口 =====================
def main():

    print_sep("=")
    print("  Somn v8.4.0 - 三级神经网络调度器")
    print("  端到端使用测试 | 自然语言任务 → 三级调度 → 策略输出")
    print_sep("=")

    print(f"\n⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  预计耗时: ~60秒")

    # ========== 核心场景测试 ==========
    print_section("【阶段一】核心场景端到端测试")

    results = []
    for scenario in SCENARIOS:
        r = test_scenario(scenario)
        results.append(r)

    # ========== 程序化接口测试 ==========
    print_section("【阶段二】程序化调用接口测试")
    test_programmatic()

    # ========== 随机性验证 ==========
    print_section("【阶段三】随机序列特性验证")
    test_randomness()

    # ========== 质量指标 ==========
    print_section("【阶段四】质量指标验证")
    test_quality_metrics()

    # ========== 上下文感知 ==========
    print_section("【阶段五】上下文感知测试")
    test_context_awareness()

    # ========== ROI连续选择 ==========
    print_section("【阶段六】ROI驱动连续选择")
    test_roi_guided_selection_path()
    test_workflow_reference_stability()

    # ========== 最终总结 ==========

    print_sep("=")
    print("  测试完成总结")
    print_sep("=")

    total_engines = sum(
        len(r.p1_outputs) + len(r.p3_outputs) + len(r.p2_outputs)
        for r in results
    )
    avg_confidence = sum(r.decision_confidence for r in results) / len(results)
    avg_synergy = sum(r.synergy_score for r in results) / len(results)
    avg_balance = sum(r.tier_balance for r in results) / len(results)
    avg_coverage = sum(r.coverage for r in results) / len(results)

    print(f"\n  场景数: {len(results)}")
    print(f"  总调用引擎: {total_engines} 个")
    print(f"  平均置信度: {avg_confidence:.1%}")
    print(f"  平均协同度: {avg_synergy:.2f}")
    print(f"  平均层级平衡: {avg_balance:.2f}")
    print(f"  平均域覆盖: {avg_coverage:.2f}")

    print(f"\n  ✅ 端到端测试全部完成")
    print(f"  ⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_sep("=")

    print("""
    使用方式速查:
    ─────────────────────────────────────────
    # 快速策略
    from src.intelligence.global_wisdom_scheduler import tier3_quick
    quick = tier3_quick("你的问题", random_seed=42)

    # 完整结果对象
    from src.intelligence.tier3_neural_scheduler import tier3_analyze
    result = tier3_analyze("你的问题", random_seed=42)
    print(result.final_strategy)
    print(result.key_insights)

    # 程序化报告
    from src.intelligence.global_wisdom_scheduler import tier3_full_report
    report = tier3_full_report("你的问题")
    """)


if __name__ == "__main__":
    main()
