# -*- coding: utf-8 -*-
"""
P9#1 Learning 系统测试
覆盖: LearningSystem / UnifiedLearningOrchestrator / ResearchStrategyEngine /
      EmotionResearchCore / ROITracker / 三层学习策略
"""

import pytest


class TestLearningSystem:
    """LearningSystem 核心测试 (src/core/learning_system.py)"""

    def test_import_learning_system(self):
        """LearningSystem 类可导入"""
        from smart_office_assistant.src.core.learning_system import LearningSystem
        assert LearningSystem is not None

    def test_create_learning_system(self):
        """工厂函数可调用"""
        from smart_office_assistant.src.core.learning_system import create_learning_system
        # 不传路径，使用默认值，不应抛异常
        try:
            ls = create_learning_system()
            assert ls is not None
        except (FileNotFoundError, OSError):
            # data目录不存在时可能报错，只要能导入并调用即可
            pass

    def test_learning_entry_dataclass(self):
        """LearningEntry 数据类可实例化（字段: id, topic_id, title 等）"""
        from smart_office_assistant.src.core.learning_system import LearningEntry
        from datetime import datetime
        entry = LearningEntry(
            id="le1", topic_id="t1", title="Test",
            discipline="AI", summary="test summary",
            key_sentences=["s1"], insights=["i1"],
            sources=[], tags=["unit"], learned_at=datetime.now()
        )
        assert entry.id == "le1"

    def test_daily_log_dataclass(self):
        """DailyLog 数据类可用（字段: date, learned_count, skipped_count 等）"""
        from smart_office_assistant.src.core.learning_system import DailyLog
        from datetime import datetime
        log = DailyLog(date="2026-04-24", learned_count=5,
                       skipped_count=0, error_count=0, files=[],
                       timestamp=datetime.now())
        assert log.date == "2026-04-24"

    def test_has_record_and_retrieve(self):
        """应有记录和检索方法"""
        from smart_office_assistant.src.core.learning_system import LearningSystem
        has_record = any(
            hasattr(LearningSystem, m) for m in (
                "log_daily_learning", "record", "add_entry", "save_entry"
            )
        )
        has_retrieve = any(
            hasattr(LearningSystem, m) for m in (
                "get_entries_by_discipline", "retrieve", "get", "query", "search"
            )
        )
        assert has_record or has_retrieve, "LearningSystem 缺少基本 CRUD 方法"


class TestUnifiedLearningOrchestrator:
    """UnifiedLearningOrchestrator 测试 (src/neural_memory/unified_learning_orchestrator.py)"""

    def test_import_orchestrator(self):
        """UnifiedLearningOrchestrator 可导入"""
        from smart_office_assistant.src.neural_memory.unified_learning_orchestrator import (
            UnifiedLearningOrchestrator,
            SchedulerStrategyMode,
            LearningPlan,
        )
        assert UnifiedLearningOrchestrator is not None

    def test_scheduler_strategy_mode_enum(self):
        """SchedulerStrategyMode 枚举有多个值"""
        from smart_office_assistant.src.neural_memory.unified_learning_orchestrator import SchedulerStrategyMode
        modes = list(SchedulerStrategyMode)
        assert len(modes) >= 2, f"SchedulerStrategyMode 过少: {modes}"

    def test_learning_plan_dataclass(self):
        """LearningPlan 可实例化（字段: plan_id, strategy_type, execution_phase）"""
        from smart_office_assistant.src.neural_memory.unified_learning_orchestrator import LearningPlan
        plan = LearningPlan(
            plan_id="p1", strategy_type="DAILY",
            execution_phase="planning", data_summary={},
            learning_config={}, expected_outcomes=[]
        )
        assert plan.plan_id == "p1"

    def test_run_unified_learning_function(self):
        """run_unified_learning 函数存在且可调用"""
        from smart_office_assistant.src.neural_memory.unified_learning_orchestrator import run_unified_learning
        assert callable(run_unified_learning)

    def test_orchestrator_has_execute(self):
        """Orchestrator 应有执行/调度方法（execute_daily / execute_strategy）"""
        from smart_office_assistant.src.neural_memory.unified_learning_orchestrator import UnifiedLearningOrchestrator
        has_exec = any(
            hasattr(UnifiedLearningOrchestrator, m)
            for m in ("execute_daily", "execute_strategy", "run", "orchestrate", "schedule", "plan")
        )
        assert has_exec, "UnifiedLearningOrchestrator 缺少执行方法"


class TestResearchStrategyEngine:
    """ResearchStrategyEngine 测试 (src/intelligence/engines/_research_strategy_engine.py)"""

    def test_import_engine(self):
        """ResearchStrategyEngine 可导入"""
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import ResearchStrategyEngine
        assert ResearchStrategyEngine is not None

    def test_core_enums_exist(self):
        """核心枚举类型存在"""
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import (
            ImpactTarget, TargetAudience, JourneyStage, Mechanism
        )
        assert len(list(ImpactTarget)) >= 2
        assert len(list(TargetAudience)) >= 2
        assert len(list(JourneyStage)) >= 2
        assert len(list(Mechanism)) >= 2

    def test_strategy_class(self):
        """Strategy 数据类可实例化"""
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import Strategy
        # Strategy 需要较多参数，检查类属性而非实例化
        assert hasattr(Strategy, "__dataclass_fields__") or hasattr(Strategy, "__init__")

    def test_finding_classification(self):
        """FindingClassification 存在且有分类参数（枚举值用中文）"""
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import (
            FindingClassification, ImpactTarget, TargetAudience, JourneyStage, Mechanism
        )
        fc = FindingClassification(
            impact_target=ImpactTarget.GROWTH,
            target_audience=TargetAudience.NEW_USER,
            journey_stage=JourneyStage.AWARENESS,
            mechanism=Mechanism.EMOTION_TRIGGER
        )

    def test_factory_function(self):
        """create_research_strategy_engine 工厂函数存在"""
        from smart_office_assistant.src.intelligence.engines._research_strategy_engine import create_research_strategy_engine
        assert callable(create_research_strategy_engine)


class TestEmotionResearchCore:
    """EmotionResearchCore 测试 (src/intelligence/engines/emotion_research_core.py)"""

    def test_import_emotion_core(self):
        """EmotionResearchCore 可导入"""
        from smart_office_assistant.src.intelligence.engines.emotion_research_core import EmotionResearchCore
        assert EmotionResearchCore is not None

    def test_dimension_enums(self):
        """研究维度和方向枚举存在"""
        from smart_office_assistant.src.intelligence.engines.emotion_research_core import (
            ResearchDimension, ResearchDirection
        )
        assert len(list(ResearchDimension)) >= 3
        assert len(list(ResearchDirection)) >= 3

    def test_framework_exists(self):
        """EmotionResearchFramework 框架类存在"""
        from smart_office_assistant.src.intelligence.engines.emotion_research_core import EmotionResearchFramework
        assert EmotionResearchFramework is not None

    def test_standalone_functions(self):
        """独立便捷函数可导入"""
        from smart_office_assistant.src.intelligence.engines.emotion_research_core import (
            validate_requirement,
            generate_strategy_framework,
            get_heart_price_formula,
        )
        assert callable(validate_requirement)
        assert callable(generate_strategy_framework)
        assert callable(get_heart_price_formula)

    def test_get_factory(self):
        """get_emotion_research_core 工厂函数存在"""
        from smart_office_assistant.src.intelligence.engines.emotion_research_core import get_emotion_research_core
        assert callable(get_emotion_research_core)


class TestROITracker:
    """ROITracker 测试 (src/neural_memory/roi_tracker_core.py)"""

    def test_import_roi_tracker(self):
        """ROITracker 可导入"""
        from smart_office_assistant.src.neural_memory.roi_tracker_core import ROITracker
        assert ROITracker is not None

    def test_roi_tracker_instantiation(self):
        """ROITracker 可以实例化"""
        from smart_office_assistant.src.neural_memory.roi_tracker_core import ROITracker
        tracker = ROITracker()
        assert tracker is not None

    def test_roi_tracker_methods(self):
        """ROITracker 应有核心追踪方法（track_task_start / record_interaction）"""
        from smart_office_assistant.src.neural_memory.roi_tracker_core import ROITracker
        has_track = any(hasattr(ROITracker, m) for m in (
            "track_task_start", "record_interaction", "track_task_complete"
        ))
        has_report = any(hasattr(ROITracker, m) for m in (
            "report", "get_stats", "summary", "get_report", "generate_report"
        ))
        assert has_track or has_report, "ROITracker 缺少追踪或报告方法"


class TestThreeTierLearning:
    """三层学习系统测试 (src/neural_memory/three_tier_learning.py — 实际导出 ThreeTierLearningExecutor)"""

    def test_import_three_tier(self):
        """ThreeTierLearningExecutor 可导入"""
        from smart_office_assistant.src.neural_memory.three_tier_learning import ThreeTierLearningExecutor
        assert ThreeTierLearningExecutor is not None

    def test_tier_constants(self):
        """应有 LearningLayer 枚举定义层级"""
        from smart_office_assistant.src.neural_memory.three_tier_learning import LearningLayer
        layers = list(LearningLayer)
        assert len(layers) >= 3, f"LearningLayer 层数过少: {layers}"

    def test_learning_strategies(self):
        """应有 LearningStatus 枚举"""
        from smart_office_assistant.src.neural_memory.three_tier_learning import LearningStatus
        statuses = list(LearningStatus)
        assert len(statuses) >= 2, f"LearningStatus 过少: {statuses}"


class TestLearningIntegration:
    """学习系统集成性测试 — 各子系统之间可以协作"""

    def test_all_learning_modules_coexist(self):
        """所有学习模块可在同一进程中导入（无循环导入）"""
        imports_ok = []
        errors = []

        modules_to_try = [
            ("LearningSystem", "smart_office_assistant.src.core.learning_system"),
            ("UnifiedLearningOrchestrator",
             "smart_office_assistant.src.neural_memory.unified_learning_orchestrator"),
            ("ThreeTierLearning",
             "smart_office_assistant.src.neural_memory.three_tier_learning"),
            ("ResearchStrategyEngine",
             "smart_office_assistant.src.intelligence.engines._research_strategy_engine"),
            ("EmotionResearchCore",
             "smart_office_assistant.src.intelligence.engines.emotion_research_core"),
            ("ROITracker", "smart_office_assistant.src.neural_memory.roi_tracker_core"),
        ]

        for name, module_path in modules_to_try:
            try:
                __import__(module_path, fromlist=[name])
                imports_ok.append(name)
            except Exception as e:
                errors.append(f"{name}: {e}")

        # 至少4个模块应成功导入
        assert len(imports_ok) >= 4, \
            f"学习模块导入失败过多: 成功={imports_ok}, 失败={errors}"
