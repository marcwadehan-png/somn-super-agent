# -*- coding: utf-8 -*-
"""
P10#5 核心引擎系统测试
覆盖:
  1. _common_enums.py   - FeedbackType / TaskStatus 枚举
  2. _research_strategy_engine.py - ResearchStrategyEngine 研究策略引擎
  3. combinatorial_optimizer.py  - CombinatorialOptimizer 组合优化器
  4. closed_loop_system.py        - ClosedLoopThinkingSystem 闭环思维系统
  5. narrative_intelligence_engine.py - NarrativeIntelligenceEngine 叙事智能引擎

运行方式:
    python -m pytest tests/test_core_engines.py -v
"""

import pytest
import sys
import math
from pathlib import Path

# ── 路径设置 (与 conftest.py / test_scheduler_system.py 保持一致) ──
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC_PATH = str(_PROJECT_ROOT / "smart_office_assistant" / "src")
_SA_PATH = str(_PROJECT_ROOT / "smart_office_assistant")
for _p in (_SRC_PATH, _SA_PATH, str(_PROJECT_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ═══════════════════════════════════════════════════════════════════════
# 1. _common_enums — 通用枚举
# ═══════════════════════════════════════════════════════════════════════

class TestCommonEnums:
    """通用枚举完整性测试"""

    def test_feedback_type_values(self):
        from smart_office_assistant.src.intelligence.engines._common_enums import FeedbackType
        assert FeedbackType.POSITIVE.value == "positive"
        assert FeedbackType.NEGATIVE.value == "negative"
        assert FeedbackType.NEUTRAL.value == "neutral"
        assert FeedbackType.ADAPTIVE.value == "adaptive"
        assert len(FeedbackType) == 4

    def test_task_status_values(self):
        from smart_office_assistant.src.intelligence.engines._common_enums import TaskStatus
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"
        assert TaskStatus.SKIPPED.value == "skipped"
        assert len(TaskStatus) == 5


# ═══════════════════════════════════════════════════════════════════════
# 2. ResearchStrategyEngine — 研究策略引擎
# ═══════════════════════════════════════════════════════════════════════

class TestResearchStrategyEnums:
    """研究策略引擎枚举"""

    def test_impact_target_count(self):
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import ImpactTarget
        assert len(ImpactTarget) == 6

    def test_journey_stage_count(self):
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import JourneyStage
        assert len(JourneyStage) == 6

    def test_mechanism_count(self):
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import Mechanism
        assert len(Mechanism) == 7

    def test_lifecycle_stage_count(self):
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import StrategyLifecycleStage
        assert len(StrategyLifecycleStage) == 7

    def test_validation_status_count(self):
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import ValidationStatus
        assert len(ValidationStatus) == 5


class TestResearchStrategyEngine:
    """ResearchStrategyEngine 功能测试"""

    @pytest.fixture
    def engine(self, tmp_path):
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import (
            ResearchStrategyEngine,
        )
        return ResearchStrategyEngine(data_dir=str(tmp_path / "learning"))

    def test_record_finding_basic(self, engine):
        f = engine.record_finding(
            title="稀缺效应提升转化率",
            description="限时优惠利用稀缺性提升购买意愿",
            source="A/B测试实验",
            evidence=["实验组转化率+15%", "对照组无变化"],
            confidence=0.85,
        )
        assert f.finding_id.startswith("RF_")
        assert f.title == "稀缺效应提升转化率"
        assert f.classification is not None

    def test_record_finding_auto_classification(self, engine):
        """研究发现的分类应能从标题/描述中自动推断"""
        f = engine.record_finding(
            title="会员积分留存策略",
            description="积分体系提升用户复购率",
            source="案例分析",
            confidence=0.7,
        )
        # 自动推断为留存目标
        assert f.classification.impact_target.value in ["留存", "增长", "转化"]
        assert f.classification.target_audience.value in ["存量用户", "新用户", "全量用户"]

    def test_generate_strategy_from_finding(self, engine):
        f = engine.record_finding(
            title="增长黑客策略",
            description="裂变活动实现获客增长",
            source="文献研究",
            confidence=0.9,
            effect_size=0.6,
        )
        strategy = engine.generate_strategy(finding_ids=[f.finding_id])
        assert strategy is not None
        assert strategy.strategy_id.startswith("STR_")
        assert strategy.lifecycle_stage.value == "生成期"
        assert strategy.priority in range(1, 11)

    def test_generate_strategy_auto_naming(self, engine):
        f = engine.record_finding(
            title="情感营销提升转化",
            description="情绪触发提升购买意愿",
            source="实验",
        )
        strategy = engine.generate_strategy(finding_ids=[f.finding_id])
        # 命名格式应为「{作用机制}{影响目标}策略」
        assert "策略" in strategy.name
        assert strategy.confidence >= 0.0

    def test_generate_strategy_empty_finding_ids(self, engine):
        result = engine.generate_strategy(finding_ids=["non_existent_id"])
        assert result is None

    def test_lifecycle_advance(self, engine):
        f = engine.record_finding(title="测试", description="测试", source="测试")
        s = engine.generate_strategy([f.finding_id])
        assert s.lifecycle_stage.value == "生成期"
        next_stage = engine.advance_lifecycle(s.strategy_id)
        assert next_stage.value == "验证期"

    def test_lifecycle_advance_with_validation(self, engine):
        f = engine.record_finding(title="测试", description="测试", source="测试")
        s = engine.generate_strategy([f.finding_id])
        engine.advance_lifecycle(s.strategy_id, {"status": "validated", "effect_data": {"lift": 0.12}})
        updated = engine.get_strategy(s.strategy_id)
        assert updated.validation_status.value == "已验证"

    def test_retire_strategy(self, engine):
        f = engine.record_finding(title="失效策略", description="测试", source="测试")
        s = engine.generate_strategy([f.finding_id])
        result = engine.retire_strategy(s.strategy_id, reason="效果不达预期")
        assert result is True
        retired = engine.get_strategy(s.strategy_id)
        assert retired.lifecycle_stage.value == "退役"

    def test_retire_nonexistent_returns_false(self, engine):
        assert engine.retire_strategy("non_existent") is False

    def test_get_finding(self, engine):
        f = engine.record_finding(title="查询测试", description="desc", source="src")
        found = engine.get_finding(f.finding_id)
        assert found is not None
        assert found.finding_id == f.finding_id

    def test_list_findings(self, engine):
        engine.record_finding(title="A", description="", source="s")
        engine.record_finding(title="B", description="", source="s")
        results = engine.list_findings()
        assert len(results) >= 2

    def test_list_strategies(self, engine):
        f = engine.record_finding(title="S", description="", source="s")
        engine.generate_strategy([f.finding_id])
        results = engine.list_strategies()
        assert len(results) >= 1

    def test_generate_report(self, engine):
        f = engine.record_finding(title="R", description="", source="s")
        engine.generate_strategy([f.finding_id])
        report = engine.generate_report()
        assert "total_findings" in report
        assert "total_strategies" in report
        assert report["total_findings"] >= 1
        assert report["total_strategies"] >= 1


# ═══════════════════════════════════════════════════════════════════════
# 3. CombinatorialOptimizer — 组合优化器
# ═══════════════════════════════════════════════════════════════════════

class TestCombinatorialMath:
    """组合数学基础计算"""

    def test_permutation_count_basic(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        assert CombinatorialOptimizer.permutation_count(5, 3) == 60
        assert CombinatorialOptimizer.permutation_count(4, 2) == 12

    def test_permutation_count_zero(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        assert CombinatorialOptimizer.permutation_count(3, 5) == 0
        assert CombinatorialOptimizer.permutation_count(5, 0) == 1

    def test_combination_count(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        assert CombinatorialOptimizer.combination_count(5, 2) == 10
        assert CombinatorialOptimizer.combination_count(6, 3) == 20

    def test_multinomial_coefficient(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        # C(10; 3, 3, 4) = 10! / (3! 3! 4!) = 4200
        result = CombinatorialOptimizer.multinomial_coefficient(10, 3, 3, 4)
        assert result == 4200

    def test_multinomial_invalid_sum(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        assert CombinatorialOptimizer.multinomial_coefficient(5, 2, 4) == 0

    def test_inclusion_exclusion(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        # |A ∪ B| = |A| + |B| - |A ∩ B|
        sets = [{1, 2, 3}, {2, 3, 4}]
        result = CombinatorialOptimizer.inclusion_exclusion_count(sets)
        assert result == 4  # {1,2,3,4}

    def test_inclusion_exclusion_empty(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        assert CombinatorialOptimizer.inclusion_exclusion_count([]) == 0

    def test_pigeonhole_estimate(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        result = CombinatorialOptimizer.pigeonhole_estimate(10, 3)
        assert result["guaranteed_collision"] is True
        assert result["minimum_items_per_hole"] == 3

    def test_fibonacci_growth(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        assert CombinatorialOptimizer.fibonacci_growth(1) == 1
        assert CombinatorialOptimizer.fibonacci_growth(2) == 1
        assert CombinatorialOptimizer.fibonacci_growth(6) == 8

    def test_golden_ratio_decision(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        result = CombinatorialOptimizer.golden_ratio_decision(("A", 100), ("B", 0))
        assert result["decision"] == "A"
        assert result["confidence"] > 0

    def test_golden_ratio_constant(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        assert abs(CombinatorialOptimizer.GOLDEN_RATIO - 1.618033988749894) < 1e-9


class TestCombinatorialOptimizer:
    """方案评估与优化"""

    def test_evaluate_plan(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer, PlanOption, EvaluationMetric,
        )
        plan = PlanOption(
            id="p1",
            name="激进方案",
            description="高风险高回报",
            metrics={EvaluationMetric.SCORE: 0.9, EvaluationMetric.RISK: 0.3},
        )
        result = CombinatorialOptimizer.evaluate_plan(plan)
        assert result.overall_score > 0
        assert result.plan.id == "p1"

    def test_evaluate_plan_with_weights(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer, PlanOption, EvaluationMetric,
        )
        plan = PlanOption(
            id="p1", name="P1", description="",
            metrics={EvaluationMetric.SCORE: 1.0, EvaluationMetric.RISK: 0.1},
        )
        result = CombinatorialOptimizer.evaluate_plan(
            plan, weights={EvaluationMetric.SCORE: 1.0, EvaluationMetric.RISK: 0.0}
        )
        assert result.overall_score > 0

    def test_optimize_plans_ranking(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer, PlanOption, EvaluationMetric,
        )
        # 显式权重确保所有方案都能被评估
        weights = {
            EvaluationMetric.SCORE: 1.0,
            EvaluationMetric.RISK: 0.0,
            EvaluationMetric.COST: 0.0,
            EvaluationMetric.QUALITY: 0.0,
            EvaluationMetric.TIME: 0.0,
            EvaluationMetric.SATISFACTION: 0.0,
        }
        plans = [
            PlanOption(id="p1", name="A", description="",
                       metrics={EvaluationMetric.SCORE: 0.5}),
            PlanOption(id="p2", name="B", description="",
                       metrics={EvaluationMetric.SCORE: 0.9}),
            PlanOption(id="p3", name="C", description="",
                       metrics={EvaluationMetric.SCORE: 0.7}),
        ]
        result = CombinatorialOptimizer.optimize_plans(plans, weights=weights, top_k=3)
        assert result.optimal_plan.id == "p2"
        assert len(result.rankings) == 3
        assert result.rankings[0].rank == 1
        assert result.optimal_score > 0
        assert result.rankings[0].overall_score >= result.rankings[1].overall_score

    def test_optimize_plans_empty(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        result = CombinatorialOptimizer.optimize_plans([])
        assert result.recommendations == ["无可用方案"]

    def test_sensitivity_analysis(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer, PlanOption, EvaluationMetric,
        )
        plan = PlanOption(
            id="p1", name="P1", description="",
            metrics={EvaluationMetric.SCORE: 0.8, EvaluationMetric.RISK: 0.2},
        )
        result = CombinatorialOptimizer.sensitivity_analysis(
            plan, {EvaluationMetric.SCORE: 0.1}
        )
        assert "score" in result

    def test_resource_allocation_max(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            CombinatorialOptimizer,
        )
        resources = {"工程师": 5, "预算": 100}
        tasks = [
            ("任务A", {"工程师": 2, "预算": 30}),
            ("任务B", {"工程师": 1, "预算": 50}),
            ("任务C", {"工程师": 3, "预算": 40}),
        ]
        result = CombinatorialOptimizer.resource_allocation_optimize(resources, tasks, "max")
        assert "allocated_tasks" in result
        assert result["task_count"] >= 0


class TestInfoTheoryFunctions:
    """信息论辅助函数"""

    def test_calculate_entropy_balanced(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            calculate_entropy,
        )
        # 均匀分布 0.5, 0.5 → H = 1 bit
        h = calculate_entropy([0.5, 0.5])
        assert abs(h - 1.0) < 1e-6

    def test_calculate_entropy_certain(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            calculate_entropy,
        )
        # 确定分布 → H = 0
        h = calculate_entropy([1.0])
        assert h == 0.0

    def test_calculate_gini_impurity(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            calculate_gini_impurity,
        )
        g = calculate_gini_impurity([0.5, 0.5])
        assert abs(g - 0.5) < 1e-6

    def test_calculate_information_gain(self):
        from smart_office_assistant.src.intelligence.engines.combinatorial_optimizer import (
            calculate_information_gain,
        )
        parent = [0.5, 0.5]
        children = [[0.75, 0.25], [0.25, 0.75]]
        ig = calculate_information_gain(parent, children)
        assert ig >= 0


# ═══════════════════════════════════════════════════════════════════════
# 4. ClosedLoopThinkingSystem — 闭环思维系统
# ═══════════════════════════════════════════════════════════════════════

class TestClosedLoopEnums:
    """闭环系统枚举"""

    def test_loop_status_count(self):
        from smart_office_assistant.src.intelligence.engines.closed_loop_system import LoopStatus
        assert len(LoopStatus) == 6

    def test_feedback_type_count(self):
        from smart_office_assistant.src.intelligence.engines.closed_loop_system import (
            ClosedLoopFeedbackType,
        )
        assert len(ClosedLoopFeedbackType) == 4


class TestClosedLoopSystem:
    """闭环思维系统功能测试"""

    @pytest.fixture
    def cls(self):
        from smart_office_assistant.src.intelligence.engines.closed_loop_system import (
            ClosedLoopThinkingSystem,
        )
        return ClosedLoopThinkingSystem()

    def test_create_loop_basic(self, cls):
        loop = cls.create_loop(name="测试闭环", description="测试描述")
        assert loop.loop_id is not None
        assert loop.name == "测试闭环"
        assert not loop.is_closed()

    def test_create_loop_with_template(self, cls):
        loop = cls.create_loop(name="PDCA", template="pdca")
        assert len(loop.nodes) == 4  # P/D/C/A

    def test_create_loop_basic_template(self, cls):
        loop = cls.create_loop(name="Basic", template="basic")
        assert len(loop.nodes) == 4

    def test_add_node(self, cls):
        loop = cls.create_loop(name="Test")
        node = cls.add_node(loop.loop_id, "action", "执行关键操作")
        assert node is not None
        assert node.node_type == "action"
        assert len(loop.nodes) == 5  # 4 template + 1 added

    def test_add_node_invalid_loop(self, cls):
        node = cls.add_node("nonexistent", "action", "测试")
        assert node is None

    def test_complete_node(self, cls):
        loop = cls.create_loop(name="Test", template="basic")
        first_node_id = loop.nodes[0].node_id
        result = cls.complete_node(loop.loop_id, first_node_id)
        assert result is True

    def test_complete_node_invalid(self, cls):
        loop = cls.create_loop(name="Test")
        result = cls.complete_node(loop.loop_id, "nonexistent_node")
        assert result is False

    def test_add_feedback(self, cls):
        from smart_office_assistant.src.intelligence.engines.closed_loop_system import (
            ClosedLoopFeedbackType,
        )
        loop = cls.create_loop(name="Test")
        fb = cls.add_feedback(
            loop_id=loop.loop_id,
            node_id=loop.nodes[0].node_id,
            feedback_type=ClosedLoopFeedbackType.POSITIVE,
            content="进展顺利",
            rating=5,
        )
        assert fb is not None
        assert fb.rating == 5

    def test_add_negative_feedback_creates_improvement_node(self, cls):
        from smart_office_assistant.src.intelligence.engines.closed_loop_system import (
            ClosedLoopFeedbackType,
        )
        loop = cls.create_loop(name="Test")
        initial_count = len(loop.nodes)
        cls.add_feedback(
            loop_id=loop.loop_id,
            node_id=loop.nodes[0].node_id,
            feedback_type=ClosedLoopFeedbackType.NEGATIVE,
            content="发现问题",
        )
        assert len(loop.nodes) == initial_count + 1

    def test_get_loop_status(self, cls):
        loop = cls.create_loop(name="Test")
        status = cls.get_loop_status(loop.loop_id)
        assert status is not None
        assert status["loop_id"] == loop.loop_id
        assert status["progress"] >= 0

    def test_get_loop_status_invalid(self, cls):
        assert cls.get_loop_status("nonexistent") is None

    def test_get_open_loops(self, cls):
        cls.create_loop(name="Loop1")
        cls.create_loop(name="Loop2")
        open_loops = cls.get_open_loops()
        assert len(open_loops) == 2

    def test_get_loop_analytics(self, cls):
        cls.create_loop(name="Test")
        analytics = cls.get_loop_analytics()
        assert analytics["total_loops"] == 1
        assert "closure_rate" in analytics

    def test_generate_report(self, cls):
        loop = cls.create_loop(name="报告测试")
        report = cls.generate_report(loop.loop_id)
        assert "报告测试" in report
        assert "基本信息" in report

    def test_generate_report_invalid(self, cls):
        report = cls.generate_report("nonexistent")
        assert report == "闭环不存在"

    def test_close_stale_loops(self, cls):
        from datetime import datetime, timedelta
        # 创建一个老旧闭环
        loop = cls.create_loop(name="Old")
        loop.created_at = datetime.now() - timedelta(days=10)
        count = cls.close_stale_loops(days=7)
        assert count == 1
        assert loop.is_closed()

    def test_ensure_closed_loop_success(self, cls):
        def executor():
            return 42
        result = cls.ensure_closed_loop("计算任务", executor)
        assert result == 42

    def test_closed_loop_progress(self, cls):
        loop = cls.create_loop(name="Test")
        assert loop.get_progress() == 0.0
        cls.complete_node(loop.loop_id, loop.nodes[0].node_id)
        assert loop.get_progress() > 0.0


# ═══════════════════════════════════════════════════════════════════════
# 5. NarrativeIntelligenceEngine — 叙事智能引擎
# ═══════════════════════════════════════════════════════════════════════

class TestNarrativeIntelligenceEngine:
    """叙事智能引擎功能测试"""

    @pytest.fixture
    def nie(self):
        from smart_office_assistant.src.intelligence.engines.narrative_intelligence_engine import (
            NarrativeIntelligenceEngine,
        )
        return NarrativeIntelligenceEngine()

    def test_analyze_narrative_structure(self, nie):
        result = nie.analyze_narrative_structure(
            description="一个创业者在产品上线前夜遭遇团队分裂",
            context={"genre": "现实主义"},
        )
        assert isinstance(result, dict)

    def test_build_persona_depth(self, nie):
        profile = {"name": "张三", "age": 28, "occupation": "产品经理"}
        result = nie.build_persona_depth(profile)
        assert isinstance(result, dict)

    def test_generate_growth_narrative(self, nie):
        strategy = {"name": "裂变增长", "mechanism": "口碑传播"}
        result = nie.generate_growth_narrative(strategy)
        assert isinstance(result, dict)

    def test_generate_growth_narrative_with_profile(self, nie):
        strategy = {"name": "留存提升"}
        profile = {"name": "李四", "age": 30}
        result = nie.generate_growth_narrative(strategy, profile)
        assert isinstance(result, dict)

    def test_diagnose_dilemma(self, nie):
        result = nie.diagnose_dilemma("产品质量与交付时间的矛盾")
        assert isinstance(result, dict)

    def test_generate_turning_point(self, nie):
        result = nie.generate_turning_point({"context": "增长放缓"})
        assert isinstance(result, dict)

    def test_generate_story_elements(self, nie):
        elements = nie.generate_story_elements("成长", count=3)
        assert isinstance(elements, list)
        assert len(elements) == 3

    def test_compute_emotional_resonance(self, nie):
        score = nie.compute_emotional_resonance(
            "经过三年的努力终于突破百万用户",
            {"emotional_preference": "成就型"},
        )
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_assess_narrative_quality(self, nie):
        narrative = {"content": "测试叙事", "structure": "线性"}
        result = nie.assess_narrative_quality(narrative)
        assert isinstance(result, dict)


class TestNarrativeEnums:
    """叙事引擎枚举和数据类"""

    def test_narrative_mode_enum(self):
        from smart_office_assistant.src.intelligence.engines.narrative_intelligence_engine import (
            NarrativeMode,
        )
        assert len(NarrativeMode) > 0

    def test_narrative_element_type_enum(self):
        from smart_office_assistant.src.intelligence.engines.narrative_intelligence_engine import (
            NarrativeElementType,
        )
        assert len(NarrativeElementType) > 0

    def test_emotional_tone_enum(self):
        from smart_office_assistant.src.intelligence.engines.narrative_intelligence_engine import (
            EmotionalTone,
        )
        assert len(EmotionalTone) > 0
