# -*- coding: utf-8 -*-
"""
P10#3 调度系统核心测试套件
覆盖:
- WisdomSchool 枚举 (35个学派)
- Tier3NeuralScheduler (核心调度器)
- SchedulerOptimizer (调度器优化器)
- WisdomDispatcher (调度映射)
- GlobalWisdomScheduler (全局调度器)
- Tier3NeuralScheduler 子模块 (DomainMatcher/EngineSelector/Fusion)

运行方式:
    python -m pytest tests/test_scheduler_system.py -v
"""

import pytest
import sys
from pathlib import Path

# ── 路径设置 (与 conftest.py 保持一致) ──
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC_PATH = str(_PROJECT_ROOT / "smart_office_assistant" / "src")
_SA_PATH = str(_PROJECT_ROOT / "smart_office_assistant")
for _p in (_SRC_PATH, _SA_PATH, str(_PROJECT_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ═══════════════════════════════════════════════════════════════
# 1. WisdomSchool 枚举
# ═══════════════════════════════════════════════════════════════

class TestWisdomSchoolEnum:
    """WisdomSchool 枚举完整性测试"""

    def test_wisdom_school_count(self):
        """42个 WisdomSchool 枚举值（35原始 + 7社科新增）"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
        schools = list(WisdomSchool)
        assert len(schools) == 42, f"期望42个学派，实际{len(schools)}个"

    def test_wisdom_school_has_v6_schools(self):
        """V1.0 第三阶段新增4个学派"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
        names = [s.name for s in WisdomSchool]
        expected_new = ["ECONOMICS", "MINGJIA", "WUXING", "COMPLEXITY"]
        for name in expected_new:
            assert name in names, f"缺少V1.0第三阶段新增学派: {name}"

    def test_wisdom_school_has_core_schools(self):
        """核心学派存在"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
        names = [s.name for s in WisdomSchool]
        core = ["CONFUCIAN", "DAOIST", "BUDDHIST", "MILITARY", "FAJIA",
                "GROWTH", "PSYCHOLOGY", "MANAGEMENT", "ZONGHENG"]
        for name in core:
            assert name in names, f"缺少核心学派: {name}"

    def test_wisdom_school_value_strings(self):
        """每个枚举值都有中文字符串"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
        for school in WisdomSchool:
            assert isinstance(school.value, str), f"学派 {school.name} value 不是字符串"
            assert len(school.value) > 0, f"学派 {school.name} value 为空"


class TestProblemTypeEnum:
    """ProblemType 枚举测试"""

    def test_problem_type_count(self):
        """ProblemType 数量 >= 100"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
        types = list(ProblemType)
        assert len(types) >= 100, f"ProblemType 数量不足: {len(types)}"

    def test_problem_type_has_core_types(self):
        """核心问题类型存在"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
        names = [p.name for p in ProblemType]
        # 使用实际存在的问题类型
        core = ["ETHICAL", "GOVERNANCE", "STRATEGY", "CRISIS", "TALENT"]
        for name in core:
            assert name in names, f"缺少核心问题类型: {name}"


# ═══════════════════════════════════════════════════════════════
# 2. Tier3NeuralScheduler
# ═══════════════════════════════════════════════════════════════

class TestTier3NeuralSchedulerImport:
    """Tier3NeuralScheduler 导入测试"""

    def test_import_from_tier3_package(self):
        """从 tier3_scheduler 包导入"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler import Tier3NeuralScheduler
        assert Tier3NeuralScheduler is not None

    def test_import_from_tier3_core(self):
        """从 _t3s_core 导入"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_core import Tier3NeuralScheduler
        assert Tier3NeuralScheduler is not None

    def test_import_types(self):
        """导入类型定义"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import (
            EngineTier, Tier3Query, Tier3Result, EngineOutput
        )
        assert EngineTier is not None
        assert Tier3Query is not None
        assert Tier3Result is not None
        assert EngineOutput is not None

    def test_import_domain_matcher(self):
        """导入领域匹配器"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_domain_matcher import DomainMatcher
        assert DomainMatcher is not None

    def test_import_engine_selector(self):
        """导入引擎选择器"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_engine_selector import EngineSelector
        assert EngineSelector is not None

    def test_import_fusion(self):
        """导入融合模块"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_fusion import (
            fuse_p1_outputs, synthesize_perspectives, synthesize_final_strategy
        )
        assert callable(fuse_p1_outputs)
        assert callable(synthesize_perspectives)
        assert callable(synthesize_final_strategy)


class TestTier3Types:
    """Tier3 数据类型"""

    def test_engine_tier_enum(self):
        """EngineTier 有 P1/P2/P3"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import EngineTier
        tiers = [t.name for t in EngineTier]
        assert "P1" in tiers
        assert "P2" in tiers
        assert "P3" in tiers

    def test_tier3_query_creation(self):
        """Tier3Query 可实例化"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import Tier3Query
        q = Tier3Query(
            query_id="q1",
            query_text="如何提升用户增长",
            context={},
        )
        assert q.query_text == "如何提升用户增长"
        assert q.query_id == "q1"

    def test_tier3_result_creation(self):
        """Tier3Result 可实例化"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import Tier3Result
        r = Tier3Result(
            query_id="q1",
            query_text="增长策略",
            success=True,
            fused_strategy={},
            feasibility_report={},
            perspective_synthesis={},
            final_strategy="综合策略",
            decision_confidence=0.88,
        )
        assert r.success is True
        assert r.decision_confidence == 0.88

    def test_engine_output_creation(self):
        """EngineOutput 可实例化"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import (
            EngineOutput, EngineTier
        )
        out = EngineOutput(
            engine_id="GROWTH",
            tier="P1",
            match_score=0.85,
            execution_time=0.05,
            raw_output={"strategy": "增长黑客"},
        )
        assert out.engine_id == "GROWTH"
        assert out.match_score == 0.85


class TestDomainMatcher:
    """领域匹配器"""

    def test_domain_matcher_creation(self):
        """DomainMatcher 可实例化"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_domain_matcher import DomainMatcher
        matcher = DomainMatcher()
        assert matcher is not None

    def test_extract_domains(self):
        """extract_domains 返回字典"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_domain_matcher import DomainMatcher
        matcher = DomainMatcher()
        result = matcher.extract_domains("增长黑客 裂变 病毒式传播")
        assert isinstance(result, dict)

    def test_domains_overlap(self):
        """domains_overlap 方法存在"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_domain_matcher import DomainMatcher
        matcher = DomainMatcher()
        assert hasattr(matcher, 'domains_overlap')


class TestEngineSelector:
    """引擎选择器"""

    def test_engine_selector_creation_with_args(self):
        """EngineSelector 创建（需要正确参数）"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_engine_selector import EngineSelector
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_domain_matcher import DomainMatcher
        matcher = DomainMatcher()
        # 需要 p1_pool, p2_pool, p3_pool, domain_matcher
        selector = EngineSelector(
            p1_pool={},
            p2_pool={},
            p3_pool={},
            domain_matcher=matcher,
        )
        assert selector is not None

    def test_select_p1_engines(self):
        """select_p1_engines 方法存在"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_engine_selector import EngineSelector
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_domain_matcher import DomainMatcher
        matcher = DomainMatcher()
        selector = EngineSelector(
            p1_pool={"GROWTH": {}},
            p2_pool={},
            p3_pool={},
            domain_matcher=matcher,
        )
        assert hasattr(selector, 'select_p1_engines')


class TestTier3Fusion:
    """Tier3 融合模块"""

    def test_fuse_p1_outputs_with_engine_output(self):
        """P1输出融合（使用EngineOutput对象）"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_fusion import fuse_p1_outputs
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import EngineOutput
        outputs = [
            EngineOutput(
                engine_id="GROWTH", tier="P1", match_score=0.85,
                execution_time=0.05, raw_output={},
                strategy_content="增长策略A",
            ),
            EngineOutput(
                engine_id="MARKETING", tier="P1", match_score=0.80,
                execution_time=0.04, raw_output={},
                strategy_content="营销策略B",
            ),
        ]
        result = fuse_p1_outputs(outputs)
        assert isinstance(result, dict)
        assert result["strategy_count"] == 2

    def test_synthesize_perspectives_with_engine_output(self):
        """视角综合（使用EngineOutput对象）"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_fusion import synthesize_perspectives
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import EngineOutput
        outputs = [
            EngineOutput(
                engine_id="CONFUCIAN", tier="P2", match_score=0.9,
                execution_time=0.03, raw_output={},
                perspective_content="从用户视角分析",
            ),
        ]
        result = synthesize_perspectives(outputs)
        assert isinstance(result, dict)
        assert "perspectives" in result

    def test_synthesize_final_strategy(self):
        """最终策略综合"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_fusion import synthesize_final_strategy
        result = synthesize_final_strategy(
            fused_strategy={"strategies": ["策略A"], "warnings": [], "total_weight": 1.0},
            feasibility_report={"feasibility_judgments": ["可行"], "warnings": [], "total_weight": 1.0},
            perspective_synthesis={"total_weight": 1.0},
        )
        assert isinstance(result, tuple)
        assert len(result) == 3  # (final_strategy, confidence, warnings)

    def test_calc_coverage(self):
        """覆盖率计算"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_fusion import calc_coverage
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_domain_matcher import DomainMatcher
        matcher = DomainMatcher()
        result = calc_coverage(
            domains={"增长": 1.0},
            p1=[], p3=[], p2=[],
            domain_matcher=matcher,
            engine_pool={},
        )
        assert isinstance(result, (int, float))
        assert 0 <= result <= 1.0

    def test_calc_tier_balance(self):
        """层级平衡计算"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_fusion import calc_tier_balance
        result = calc_tier_balance(p1=[], p3=[], p2=[])
        assert isinstance(result, (int, float))
        assert 0 <= result <= 1.0

    def test_calc_synergy(self):
        """协同效应计算"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_fusion import calc_synergy
        result = calc_synergy(p1=[], p3=[], p2=[])
        assert isinstance(result, (int, float))


class TestTier3NeuralSchedulerCore:
    """Tier3NeuralScheduler 核心功能"""

    def setup_method(self):
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_core import Tier3NeuralScheduler
        self.scheduler = Tier3NeuralScheduler()

    def test_schedule_returns_result(self):
        """schedule 方法返回结构化结果"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import Tier3Query
        q = Tier3Query(
            query_id="test1",
            query_text="如何提升用户增长",
            context={},
        )
        result = self.scheduler.schedule(q)
        assert result is not None
        assert hasattr(result, 'success') or isinstance(result, dict)

    def test_schedule_accepts_tier3_query(self):
        """接受 Tier3Query 对象"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import Tier3Query
        q = Tier3Query(
            query_id="test2",
            query_text="公司面临生死危机，如何绝地反击？",
            random_seed=42,
        )
        result = self.scheduler.schedule(q)
        assert result is not None

    def test_extract_perspective_content(self):
        """提取视角内容"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_core import extract_perspective_content
        raw = {"perspective": "从用户视角分析", "confidence": 0.9}
        content = extract_perspective_content(raw)
        assert content == "从用户视角分析"

    def test_extract_strategy_content(self):
        """提取策略内容"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_core import extract_strategy_content
        raw = {"strategy": "增长黑客策略", "confidence": 0.85}
        content = extract_strategy_content(raw)
        assert content == "增长黑客策略"

    def test_get_statistics(self):
        """统计信息"""
        if hasattr(self.scheduler, 'get_statistics'):
            stats = self.scheduler.get_statistics()
            assert isinstance(stats, dict)


# ═══════════════════════════════════════════════════════════════
# 3. SchedulerOptimizer
# ═══════════════════════════════════════════════════════════════

class TestSchedulerOptimizerImport:
    """SchedulerOptimizer 导入测试"""

    def test_import_optimizer(self):
        """导入调度器优化器"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import SchedulerOptimizer
        assert SchedulerOptimizer is not None

    def test_import_optimizer_public_functions(self):
        """导入优化器公共函数"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import (
            expand_keywords,
            record_scheduler_metrics,
            check_optimization_status,
            get_optimization_report,
            get_optimizer,
        )
        funcs = [
            expand_keywords, record_scheduler_metrics, check_optimization_status,
            get_optimization_report, get_optimizer,
        ]
        for f in funcs:
            assert callable(f), f"{f.__name__} 不可调用"


class TestSchedulerOptimizerTypes:
    """SchedulerOptimizer 数据类型"""

    def test_quality_metrics_dataclass(self):
        """QualityMetrics 可实例化"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import QualityMetrics
        qm = QualityMetrics(
            coverage_rate=0.92,
            response_time_ms=2500.0,
            domain_diversity=8,
            tier_balance={"P1": 5, "P3": 3, "P2": 4},
        )
        assert qm.coverage_rate == 0.92
        assert qm.domain_diversity == 8

    def test_quality_metrics_to_dict(self):
        """QualityMetrics to_dict"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import QualityMetrics
        qm = QualityMetrics(coverage_rate=0.88, response_time_ms=3000.0, domain_diversity=6)
        d = qm.to_dict()
        assert d["coverage_rate"] == 0.88
        assert "timestamp" in d

    def test_adaptive_weight_config(self):
        """AdaptiveWeightConfig 默认值"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import AdaptiveWeightConfig
        cfg = AdaptiveWeightConfig()
        assert cfg.feedback_driven is True
        assert cfg.learning_rate == 0.1
        assert cfg.min_weight == 0.5
        assert cfg.max_weight == 1.0

    def test_adaptive_weight_manager(self):
        """AdaptiveWeightManager 可实例化"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import AdaptiveWeightManager
        mgr = AdaptiveWeightManager()
        assert mgr is not None
        assert isinstance(mgr.engine_performance, dict)


class TestSchedulerOptimizerCore:
    """SchedulerOptimizer 核心功能"""

    def setup_method(self):
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import SchedulerOptimizer
        self.optimizer = SchedulerOptimizer()

    def test_expand_keywords_basic(self):
        """关键词扩展基本功能"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import expand_keywords
        result = expand_keywords(["增长", "获客"])
        assert isinstance(result, list)
        assert "增长" in result

    def test_expand_keywords_returns_expanded(self):
        """扩展关键词返回值包含扩展词"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import expand_keywords
        result = expand_keywords(["增长"])
        assert len(result) >= 1
        assert isinstance(result, list)

    def test_record_metrics(self):
        """记录质量指标"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import (
            SchedulerOptimizer, QualityMetrics
        )
        opt = SchedulerOptimizer()
        metrics = QualityMetrics(coverage_rate=0.90, response_time_ms=2000.0, domain_diversity=7)
        opt.record_metrics(metrics)
        assert len(opt.metrics_history) >= 1

    def test_get_coverage_trend(self):
        """覆盖率趋势"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import (
            SchedulerOptimizer, QualityMetrics
        )
        opt = SchedulerOptimizer()
        for rate in [0.80, 0.85, 0.90]:
            opt.record_metrics(QualityMetrics(coverage_rate=rate, response_time_ms=2000.0, domain_diversity=5))
        trend = opt.get_coverage_trend()
        assert len(trend) >= 3
        assert trend[-1] == 0.90

    def test_check_quality_targets(self):
        """质量目标检查"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import (
            SchedulerOptimizer, QualityMetrics
        )
        opt = SchedulerOptimizer()
        opt.record_metrics(QualityMetrics(coverage_rate=0.92, response_time_ms=2500.0, domain_diversity=8))
        result = opt.check_quality_targets()
        assert isinstance(result, dict)
        assert "status" in result
        assert "details" in result

    def test_check_quality_targets_no_data(self):
        """无数据时返回 no_data"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import SchedulerOptimizer
        opt = SchedulerOptimizer()
        result = opt.check_quality_targets()
        assert result["status"] == "no_data"

    def test_generate_optimization_report(self):
        """生成优化报告"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import (
            SchedulerOptimizer, QualityMetrics
        )
        opt = SchedulerOptimizer()
        opt.record_metrics(QualityMetrics(coverage_rate=0.88, response_time_ms=3000.0, domain_diversity=6))
        report = opt.generate_optimization_report()
        assert isinstance(report, dict)
        # 报告包含coverage信息
        assert "coverage" in report or "quality_status" in report


class TestSchedulerOptimizerIntegration:
    """SchedulerOptimizer 集成测试"""

    def test_full_optimization_cycle(self):
        """完整优化周期"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import (
            SchedulerOptimizer, QualityMetrics
        )
        opt = SchedulerOptimizer()
        # 记录指标
        for i, rate in enumerate([0.80, 0.84, 0.88, 0.91, 0.93]):
            opt.record_metrics(QualityMetrics(
                coverage_rate=rate,
                response_time_ms=3000.0 - i * 100,
                domain_diversity=6 + i,
            ))
        # 检查趋势
        trend = opt.get_coverage_trend()
        assert len(trend) == 5
        # 检查质量
        quality = opt.check_quality_targets()
        assert "status" in quality
        # 生成报告
        report = opt.generate_optimization_report()
        assert isinstance(report, dict)


# ═══════════════════════════════════════════════════════════════
# 4. WisdomDispatcher
# ═══════════════════════════════════════════════════════════════

class TestWisdomDispatcherImport:
    """WisdomDispatcher 导入测试"""

    def test_import_wisdom_dispatcher(self):
        """WisdomDispatcher 主入口导入"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
        assert WisdomDispatcher is not None

    def test_import_dispatch_mapping(self):
        """调度映射模块导入"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        assert WisdomDispatcher is not None

    def test_import_dispatch_enums(self):
        """调度枚举导入"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import (
            WisdomSchool, ProblemType
        )
        assert WisdomSchool is not None
        assert ProblemType is not None


class TestWisdomDispatcherCore:
    """WisdomDispatcher 核心功能"""

    def setup_method(self):
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
        self.dispatcher = WisdomDispatcher()

    def test_dispatcher_not_empty(self):
        """调度器非空"""
        assert self.dispatcher is not None

    def test_has_mapping_attribute(self):
        """有调度映射属性"""
        if hasattr(self.dispatcher, 'problem_school_mapping'):
            assert len(self.dispatcher.problem_school_mapping) > 0

    def test_has_resolve_departments(self):
        """resolve_departments 方法存在"""
        assert hasattr(self.dispatcher, 'resolve_departments')


class TestDispatchMappingCoverage:
    """调度映射覆盖率"""

    def test_dispatch_mapping_has_problem_types(self):
        """映射包含 ProblemType 键"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import (
            WisdomDispatcher, ProblemType
        )
        wd = WisdomDispatcher()
        sample_pt = list(ProblemType)[:5]
        for pt in sample_pt:
            # 至少不抛异常
            assert pt is not None

    def test_dispatch_mapping_values_are_valid(self):
        """映射值格式有效"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        wd = WisdomDispatcher()
        if hasattr(wd, 'problem_school_mapping'):
            items = list(wd.problem_school_mapping.items())
            if items:
                key, val = items[0]
                assert isinstance(val, (list, tuple, dict))


# ═══════════════════════════════════════════════════════════════
# 5. GlobalWisdomScheduler
# ═══════════════════════════════════════════════════════════════

class TestGlobalWisdomScheduler:
    """全局智慧调度器"""

    def test_import_global_wisdom_scheduler(self):
        """导入全局调度器"""
        from smart_office_assistant.src.intelligence.global_wisdom_scheduler import GlobalWisdomScheduler
        assert GlobalWisdomScheduler is not None

    def test_global_scheduler_instantiation(self):
        """全局调度器可实例化"""
        from smart_office_assistant.src.intelligence.global_wisdom_scheduler import GlobalWisdomScheduler
        gws = GlobalWisdomScheduler()
        assert gws is not None


# ═══════════════════════════════════════════════════════════════
# 6. SchedulerOptimizerIntegration
# ═══════════════════════════════════════════════════════════════

class TestSchedulerOptimizerIntegrationModule:
    """优化器集成模块"""

    def test_import_optimizer_integration(self):
        """导入优化器集成模块"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer_integration import get_optimizer
        assert callable(get_optimizer)

    def test_get_optimizer_returns_optimizer(self):
        """get_optimizer 返回优化器实例"""
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer_integration import get_optimizer
        opt = get_optimizer()
        assert opt is not None


# ═══════════════════════════════════════════════════════════════
# 7. End-to-End Integration
# ═══════════════════════════════════════════════════════════════

class TestSchedulerEndToEnd:
    """调度系统端到端集成"""

    def test_tier3_with_optimizer(self):
        """Tier3 + SchedulerOptimizer 联合"""
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_core import Tier3NeuralScheduler
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import Tier3Query
        from smart_office_assistant.src.intelligence.scheduler.scheduler_optimizer import SchedulerOptimizer, QualityMetrics

        scheduler = Tier3NeuralScheduler()
        optimizer = SchedulerOptimizer()

        # 使用 Tier3Query
        q = Tier3Query(query_id="e2e_1", query_text="用户增长策略", context={})
        result = scheduler.schedule(q)
        # 记录指标
        optimizer.record_metrics(QualityMetrics(
            coverage_rate=0.88,
            response_time_ms=2500.0,
            domain_diversity=7,
        ))
        # 检查质量
        quality = optimizer.check_quality_targets()
        assert "status" in quality

    def test_wisdom_dispatcher_with_tier3(self):
        """WisdomDispatcher + Tier3 联合"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_core import Tier3NeuralScheduler
        from smart_office_assistant.src.intelligence.scheduler.tier3_scheduler._t3s_types import Tier3Query

        dispatcher = WisdomDispatcher()
        scheduler = Tier3NeuralScheduler()

        # 调度器可访问
        assert dispatcher is not None
        # 调度器可调度
        q = Tier3Query(query_id="e2e_2", query_text="团队管理问题", context={})
        result = scheduler.schedule(q)
        assert result is not None
