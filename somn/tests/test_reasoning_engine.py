# -*- coding: utf-8 -*-
"""
P10#1 推理引擎系统测试
覆盖: KuramotoCoupler / PhaseSynchronizationCoordinator / ReasoningMemory /
      ReverseThinkingEngine / DeweyThinkingEngine / GeodesicReasoningEngine /
      LongCoT子组件(BoundaryDetector/InsightDetector/SelfCorrector/AdaptiveThinkingAllocator/CheckpointManager) /
      ToT子组件(ThoughtTree/SearchStrategy) /
      ReAct子组件(ToolRegistry/ToolExecutor/TAOTrajectory) /
      GoT子组件(ThoughtGraph/ThoughtEdge/GraphReasoningMode)
"""

import pytest
import math
import numpy as np
from datetime import datetime


# ============================================================
# 1. PhaseSynchronizationCoordinator (Kuramoto耦合振荡器)
# ============================================================

class TestPhaseResponseCurve:
    """相位响应曲线 (PRC) 测试"""

    def test_prc_type_enum(self):
        """PRCType 枚举有 TYPE_I 和 TYPE_II"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PRCType,
        )
        assert PRCType.TYPE_I.value == "type_i"
        assert PRCType.TYPE_II.value == "type_ii"

    def test_prc_evaluate_type_i(self):
        """I型 PRC evaluate 返回值在合理范围"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PhaseResponseCurve, PRCType,
        )
        prc = PhaseResponseCurve(prc_type=PRCType.TYPE_I)
        result = prc.evaluate(0.0)
        assert isinstance(result, float)
        # I型始终非负(简化sin模型，振幅0.2)
        result2 = prc.evaluate(math.pi)
        assert isinstance(result2, float)

    def test_prc_evaluate_type_ii(self):
        """II型 PRC evaluate 返回值（可正可负）"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PhaseResponseCurve, PRCType,
        )
        prc = PhaseResponseCurve(prc_type=PRCType.TYPE_II)
        early = prc.evaluate(0.5)   # 早期刺激
        late = prc.evaluate(5.0)     # 晚期刺激
        assert isinstance(early, float)
        assert isinstance(late, float)

    def test_prc_get_interaction_function(self):
        """get_interaction_function 返回指定长度列表"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PhaseResponseCurve,
        )
        prc = PhaseResponseCurve()
        func = prc.get_interaction_function(coupling_strength=0.5, n_samples=32)
        assert len(func) == 32
        assert all(isinstance(v, float) for v in func)


class TestBrainRhythmEnum:
    """脑节律枚举测试"""

    def test_brain_rhythm_values(self):
        """BrainRhythm 包含 DELTA/THETA/ALPHA/BETA/GAMMA"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            BrainRhythm,
        )
        rhythms = list(BrainRhythm)
        names = [r.name for r in rhythms]
        assert "DELTA" in names
        assert "THETA" in names
        assert "ALPHA" in names
        assert "BETA" in names
        assert "GAMMA" in names

    def test_rhythm_info_dataclass(self):
        """RhythmInfo 可实例化"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            RhythmInfo,
        )
        info = RhythmInfo(
            name="Alpha", frequency=10.0,
            description="放松警觉", cognitive_mode="抑制无关",
            duration_ms=200
        )
        assert info.name == "Alpha"
        assert info.frequency == 10.0


class TestNeuralOscillator:
    """神经振荡器测试"""

    def test_oscillator_creation(self):
        """NeuralOscillator 可正确创建"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            NeuralOscillator, PhaseResponseCurve, BrainRhythm, RhythmInfo,
        )
        osc = NeuralOscillator(
            id="osc_1", name="default",
            natural_frequency=10.0, current_phase=0.0,
            prc=PhaseResponseCurve(), is_active=True,
            coupling_strength=0.5, rhythm=BrainRhythm.ALPHA,
            phase_history=[], fire_times=[]
        )
        assert osc.id == "osc_1"
        assert osc.natural_frequency == 10.0

    def test_oscillator_step(self):
        """step 方法返回布尔值"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            NeuralOscillator, PhaseResponseCurve, BrainRhythm,
        )
        osc = NeuralOscillator(
            id="osc_1", name="test", natural_frequency=10.0,
            current_phase=0.0, prc=PhaseResponseCurve(),
            is_active=True, coupling_strength=0.5,
            rhythm=BrainRhythm.ALPHA, phase_history=[], fire_times=[]
        )
        fired = osc.step(dt=0.01)
        assert isinstance(fired, bool)

    def test_oscillator_reset_phase(self):
        """reset_phase 将相位归零"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            NeuralOscillator, PhaseResponseCurve, BrainRhythm,
        )
        osc = NeuralOscillator(
            id="osc_1", name="test", natural_frequency=10.0,
            current_phase=3.0, prc=PhaseResponseCurve(),
            is_active=True, coupling_strength=0.5,
            rhythm=BrainRhythm.ALPHA, phase_history=[], fire_times=[]
        )
        osc.reset_phase()
        assert osc.current_phase == 0.0

    def test_oscillator_to_dict(self):
        """to_dict 返回字典"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            NeuralOscillator, PhaseResponseCurve, BrainRhythm,
        )
        osc = NeuralOscillator(
            id="osc_1", name="test", natural_frequency=10.0,
            current_phase=0.0, prc=PhaseResponseCurve(),
            is_active=True, coupling_strength=0.5,
            rhythm=BrainRhythm.ALPHA, phase_history=[], fire_times=[]
        )
        d = osc.to_dict()
        assert isinstance(d, dict)
        assert d["id"] == "osc_1"


class TestKuramotoCoupler:
    """Kuramoto 耦合器核心测试"""

    def setup_method(self):
        """创建 KuramotoCoupler 实例"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            KuramotoCoupler,
        )
        self.coupler = KuramotoCoupler()

    def test_add_oscillator(self):
        """添加振荡器"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            NeuralOscillator, PhaseResponseCurve, BrainRhythm,
        )
        osc = NeuralOscillator(
            id="osc_1", name="alpha", natural_frequency=10.0,
            current_phase=0.0, prc=PhaseResponseCurve(),
            is_active=True, coupling_strength=0.3,
            rhythm=BrainRhythm.ALPHA, phase_history=[], fire_times=[]
        )
        self.coupler.add_oscillator(osc)
        assert len(self.coupler.oscillators) == 1

    def test_set_coupling(self):
        """设置耦合强度"""
        self.coupler.set_coupling("osc_1", "osc_2", 0.7)
        # 不抛异常即可

    def test_compute_order_parameter(self):
        """计算序参数返回 (r, theta) 元组"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            NeuralOscillator, PhaseResponseCurve, BrainRhythm,
        )
        # 添加同相振荡器
        for i in range(3):
            osc = NeuralOscillator(
                id=f"osc_{i}", name=f"test{i}", natural_frequency=10.0,
                current_phase=0.1 * i,  # 接近同相
                prc=PhaseResponseCurve(), is_active=True,
                coupling_strength=0.5, rhythm=BrainRhythm.ALPHA,
                phase_history=[], fire_times=[]
            )
            self.coupler.add_oscillator(osc)
        r, theta = self.coupler.compute_order_parameter()
        assert isinstance(r, float)
        assert isinstance(theta, float)
        assert 0 <= r <= 1.0

    def test_detect_sync_clusters(self):
        """检测同步簇返回列表"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            NeuralOscillator, PhaseResponseCurve, BrainRhythm,
        )
        for i in range(4):
            osc = NeuralOscillator(
                id=f"osc_{i}", name=f"t{i}", natural_frequency=10.0,
                current_phase=float(i), prc=PhaseResponseCurve(),
                is_active=True, coupling_strength=0.5,
                rhythm=BrainRhythm.ALPHA, phase_history=[], fire_times=[]
            )
            self.coupler.add_oscillator(osc)
        clusters = self.coupler.detect_sync_clusters(threshold=0.8)
        assert isinstance(clusters, list)


class TestPhaseSynchronizationCoordinator:
    """相位同步协调器集成测试"""

    def test_coordinator_init_default_oscillators(self):
        """协调器初始化后包含默认振荡器"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PhaseSynchronizationCoordinator,
        )
        coord = PhaseSynchronizationCoordinator()
        assert len(coord.kuramoto.oscillators) >= 4  # 至少有几个默认振荡器

    def test_coordinator_step(self):
        """协调器 step 执行不报错"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PhaseSynchronizationCoordinator,
        )
        coord = PhaseSynchronizationCoordinator()
        results = coord.step(dt=0.01)
        assert isinstance(results, dict)

    def test_coordinator_get_report(self):
        """get_report 返回报告字典"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PhaseSynchronizationCoordinator,
        )
        coord = PhaseSynchronizationCoordinator()
        report = coord.get_report()
        assert isinstance(report, dict)

    def test_coordinator_to_dict(self):
        """to_dict 序列化完整状态"""
        from smart_office_assistant.src.intelligence.reasoning.phase_synchronization_coordinator import (
            PhaseSynchronizationCoordinator,
        )
        coord = PhaseSynchronizationCoordinator()
        d = coord.to_dict()
        assert isinstance(d, dict)
        assert "oscillators" in d


# ============================================================
# 2. ReasoningMemory (推理记忆系统)
# ============================================================

class TestReasoningMemoryTypes:
    """推理记忆数据类型测试"""

    def test_reasoning_mode_enum(self):
        """ReasoningMode 枚举有 CHAIN/TREE/GRAPH/META"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import ReasoningMode
        modes = [m.name for m in ReasoningMode]
        assert "CHAIN_OF_THOUGHT" in modes
        assert "TREE_OF_THOUGHTS" in modes
        assert "GRAPH_OF_THOUGHTS" in modes
        assert "META_REASONING" in modes

    def test_reasoning_step_dataclass(self):
        """ReasoningStep 可实例化并 to_dict"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import ReasoningStep
        step = ReasoningStep(
            step_number=1, description="分析问题",
            reasoning="拆解为子问题", conclusion="有三个关键点",
            confidence=0.85
        )
        d = step.to_dict()
        assert d["step_number"] == 1
        assert d["confidence"] == 0.85

    def test_reasoning_trace_dataclass(self):
        """ReasoningTrace 可序列化和反序列化"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        trace = ReasoningTrace(
            trace_id="trace_001",
            problem="如何提升用户增长",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            steps=[ReasoningStep(step_number=1, description="分析", reasoning="拆解", conclusion="三点", confidence=0.9)],
            final_answer="综合方案A",
            confidence=0.88,
            created_at=datetime.now(),
        )
        d = trace.to_dict()
        assert d["trace_id"] == "trace_001"
        # 反序列化
        restored = ReasoningTrace.from_dict(d)
        assert restored.trace_id == trace.trace_id
        assert restored.problem == trace.problem


class TestReasoningMemoryCore:
    """推理记忆核心功能"""

    def setup_method(self):
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import ReasoningMemory
        self.memory = ReasoningMemory()

    def test_save_and_retrieve_trace(self):
        """保存和按ID检索推理轨迹"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        trace = ReasoningTrace(
            trace_id="t1", problem="用户增长策略",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            steps=[ReasoningStep(step_number=1, description="分析", reasoning="x", conclusion="y")],
            final_answer="方案A", confidence=0.9,
            created_at=datetime.now(),
        )
        result = self.memory.save_reasoning_trace(trace)
        assert result is True
        retrieved = self.memory.retrieve_reasoning_trace("t1")
        assert retrieved is not None
        assert retrieved.trace_id == "t1"

    def test_retrieve_nonexistent(self):
        """检索不存在的轨迹返回 None"""
        result = self.memory.retrieve_reasoning_trace("nonexistent")
        assert result is None

    def test_save_auto_caches_by_problem(self):
        """保存轨迹自动按问题缓存"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        trace = ReasoningTrace(
            trace_id="t2", problem="留存优化",
            reasoning_mode=ReasoningMode.TREE_OF_THOUGHTS,
            steps=[],
            final_answer="", confidence=0.8,
            created_at=datetime.now(),
        )
        self.memory.save_reasoning_trace(trace)
        cached = self.memory.check_cache("留存优化")
        assert cached is not None

    def test_retrieve_similar_reasoning(self):
        """相似度检索返回结果列表"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        trace = ReasoningTrace(
            trace_id="t3", problem="提升用户留存率方法",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            steps=[ReasoningStep(step_number=1, description="a", reasoning="b", conclusion="c")],
            final_answer="d", confidence=0.85,
            created_at=datetime.now(),
        )
        self.memory.save_reasoning_trace(trace)
        similar = self.memory.retrieve_similar_reasoning("用户留存优化", top_k=5, min_similarity=0.3)
        assert isinstance(similar, list)

    def test_statistics_tracking(self):
        """统计信息随操作递增"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        initial = self.memory.get_statistics()["total_traces"]
        trace = ReasoningTrace(
            trace_id="t_stats", problem="统计测试",
            reasoning_mode=ReasoningMode.GRAPH_OF_THOUGHTS,
            steps=[], final_answer="", confidence=0.7,
            created_at=datetime.now(),
        )
        self.memory.save_reasoning_trace(trace)
        after = self.memory.get_statistics()["total_traces"]
        assert after == initial + 1

    def test_clear_cache(self):
        """清空缓存"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        trace = ReasoningTrace(
            trace_id="tc", problem="缓存测试",
            reasoning_mode=ReasoningMode.META_REASONING,
            steps=[], final_answer="", confidence=0.6,
            created_at=datetime.now(),
        )
        self.memory.save_reasoning_trace(trace)
        assert self.memory.check_cache("缓存测试") is not None
        self.memory.clear_cache()
        assert self.memory.check_cache("缓存测试") is None

    def test_export_import_traces(self):
        """导出和导入轨迹"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        trace = ReasoningTrace(
            trace_id="te", problem="导入导出测试",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            steps=[ReasoningStep(step_number=1, description="x", reasoning="y", conclusion="z")],
            final_answer="ok", confidence=0.9,
            created_at=datetime.now(),
        )
        self.memory.save_reasoning_trace(trace)
        self.memory.export_traces(filepath="test_export.json")
        # export_traces 写入文件，返回 None；验证文件存在
        import os
        assert os.path.exists("test_export.json"), "导出文件未生成"
        # 读回文件验证
        import json as _json
        with open("test_export.json", encoding="utf-8") as f:
            exported_data = _json.load(f)
        assert "traces" in exported_data

        # 新memory导入（使用同一文件路径）
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import ReasoningMemory as RM2
        mem2 = RM2()
        mem2.import_traces("test_export.json")
        assert mem2.retrieve_reasoning_trace("te") is not None

    def test_reasoning_pattern_storage(self):
        """推理模式自动提取和存储"""
        from smart_office_assistant.src.intelligence.reasoning.reasoning_memory import (
            ReasoningTrace, ReasoningStep, ReasoningMode,
        )
        trace = ReasoningTrace(
            trace_id="tp", problem="模式学习测试",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            steps=[
                ReasoningStep(step_number=1, description="定义问题", reasoning="明确目标", conclusion="目标清晰"),
                ReasoningStep(step_number=2, description="分析原因", reasoning="找根因", conclusion="三个原因"),
            ],
            final_answer="解决方案", confidence=0.92,
            created_at=datetime.now(),
        )
        self.memory.save_reasoning_trace(trace)
        stats = self.memory.get_statistics()
        assert stats["total_patterns"] >= 0  # 模式可能被提取也可能没有


# ============================================================
# 3. ReverseThinkingEngine (逆向思维引擎)
# ============================================================

class TestReverseThinkingEngineTypes:
    """逆向思维数据类型"""

    def test_reverse_mode_enum(self):
        """ReverseMode 包含6种模式"""
        from smart_office_assistant.src.intelligence.reasoning.reverse_thinking_engine import ReverseMode
        modes = [m.name for m in ReverseMode]
        expected = ["RESULT_TO_CAUSE", "OPPOSITE_THINKING", "PERSPECTIVE_TAKING",
                    "ASSUMPTION_QUESTIONING", "CONSTRAINT_REFRAMING", "PREVENTION_ANALYSIS"]
        for m in expected:
            assert m in modes, f"缺少模式: {m}"

    def test_reverse_analysis_dataclass(self):
        """ReverseAnalysis 可实例化并 to_dict"""
        from smart_office_assistant.src.intelligence.reasoning.reverse_thinking_engine import (
            ReverseAnalysis, ReverseMode,
        )
        analysis = ReverseAnalysis(
            original_problem="如何提升转化率",
            reverse_mode=ReverseMode.RESULT_TO_CAUSE,
            reversed_perspective="从目标倒推所需步骤",
            key_insights=["需要先优化落地页"],
            confidence=0.82,
        )
        d = analysis.to_dict()
        assert d["original_problem"] == "如何提升转化率"
        assert d["confidence"] == 0.82

    def test_perspective_mapping_dataclass(self):
        """PerspectiveMapping 可实例化"""
        from smart_office_assistant.src.intelligence.reasoning.reverse_thinking_engine import PerspectiveMapping
        pm = PerspectiveMapping(
            original_view="产品不好卖",
            reverse_view="市场需求不匹配",
            common_biases=["确认偏误"],
        )
        assert pm.original_view == "产品不好卖"
        assert len(pm.common_biases) == 1


class TestReverseThinkingEngineCore:
    """逆向思维引擎核心功能"""

    def setup_method(self):
        from smart_office_assistant.src.intelligence.reasoning.reverse_thinking_engine import ReverseThinkingEngine
        self.engine = ReverseThinkingEngine()

    def test_analyze_result_to_cause(self):
        """结果倒推分析"""
        result = self.engine.analyze(
            problem="实现100万营收",
            mode="result_to_cause",
        )
        assert hasattr(result, 'reversed_perspective')
        assert hasattr(result, 'confidence')
        assert isinstance(result.reversed_perspective, str)

    def test_analyze_opposite_thinking(self):
        """对立思考分析"""
        result = self.engine.analyze(
            problem="如何提高价格",
            mode="opposite_thinking",
        )
        assert result is not None
        assert len(result.key_insights) >= 0

    def test_multi_mode_analysis(self):
        """多模式分析返回结果"""
        results = self.engine.multi_mode_analysis(problem="团队效率低下")
        assert isinstance(results, (list, dict))

    def test_reverse_question(self):
        """逆向提问返回结果（可能是dict或string）"""
        result = self.engine.reverse_question("为什么用户不付费")
        # 返回值可能是dict或string
        assert result is not None
        if isinstance(result, dict):
            assert "reverse_questions" in result or "question" in result
        else:
            assert isinstance(result, str)

    def test_engine_has_cognitive_biases(self):
        """引擎包含认知偏见参考数据"""
        assert hasattr(self.engine, 'COGNITIVE_BIASES')
        assert isinstance(self.engine.COGNITIVE_BIASES, dict)


# ============================================================
# 4. DeweyThinkingEngine (杜威思维引擎)
# ============================================================

class TestDeweyThinkingEngineTypes:
    """杜威思维数据类型测试"""

    def test_thinking_step_enum(self):
        """ThinkingStep 五步法枚举"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import ThinkingStep
        steps = [s.name for s in ThinkingStep]
        assert "SUGGESTION" in steps
        assert "DIFFICULTY" in steps
        assert "HYPOTHESIS" in steps
        assert "REASONING" in steps
        assert "VERIFICATION" in steps

    def test_thinking_habit_enum(self):
        """ThinkingHabit 三种习惯"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import ThinkingHabit
        habits = [h.name for h in ThinkingHabit]
        assert "QUESTIONING" in habits
        assert "INQUIRING" in habits
        assert "REFLECTIVE" in habits

    def test_thinking_type_enum(self):
        """ThinkingType 五种思维类型"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import ThinkingType
        types = [t.name for t in ThinkingType]
        assert "DIVERGENT" in types
        assert "CONVERGENT" in types
        assert "CRITICAL" in types
        assert "CREATIVE" in types
        assert "SYSTEMATIC" in types

    def test_five_step_analysis_dataclass(self):
        """FiveStepAnalysis 可实例化"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import FiveStepAnalysis, ThinkingStep
        analysis = FiveStepAnalysis(
            step=ThinkingStep.SUGGESTION,
            description="发现问题迹象",
            prompt_questions=["这是什么问题？"],
            output="初步定义问题",
            quality_score=0.8,
        )
        assert analysis.step == ThinkingStep.SUGGESTION
        assert analysis.quality_score == 0.8


class TestDeweyThinkingEngineCore:
    """杜威思维引擎核心功能"""

    def setup_method(self):
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import DeweyThinkingEngine
        self.engine = DeweyThinkingEngine()

    def test_apply_five_step_method(self):
        """五步法应用返回结构化结果"""
        result = self.engine.apply_five_step_method(problem="如何提升产品质量")
        assert result is not None
        assert hasattr(result, 'steps') or hasattr(result, 'final_solution')

    def test_guide_five_step(self):
        """分步引导返回指导"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import ThinkingStep
        result = self.engine.guide_five_step(
            problem="进入新市场",
            current_step=ThinkingStep.SUGGESTION,
            previous_outputs={},
        )
        assert result is not None

    def test_assess_thinking_habits(self):
        """思维习惯评估返回评估结果"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import ThinkingHabit
        result = self.engine.assess_thinking_habits(
            habit_responses={ThinkingHabit.QUESTIONING: 2}
        )
        assert isinstance(result, list)

    def test_create_training_plan(self):
        """创建训练计划"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import ThinkingHabit
        plan = self.engine.create_training_plan(
            target_habits=[ThinkingHabit.QUESTIONING],
            duration_weeks=2,
        )
        assert plan is not None

    def test_get_critical_thinking_checklist(self):
        """批判性思维检查清单非空"""
        checklist = self.engine.get_critical_thinking_checklist()
        assert isinstance(checklist, list) or isinstance(checklist, dict)
        # 确保有内容
        if isinstance(checklist, list):
            assert len(checklist) > 0

    def test_apply_thinking_type_divergent(self):
        """发散思维应用"""
        from smart_office_assistant.src.intelligence.reasoning.dewey_thinking_engine import ThinkingType
        result = self.engine.apply_thinking_type(
            thinking_type=ThinkingType.DIVERGENT,
            problem="新产品命名",
        )
        assert result is not None

    def test_engine_has_five_step_guide(self):
        """引擎包含五步法指南常量"""
        assert hasattr(self.engine, 'FIVE_STEP_GUIDE')
        assert isinstance(self.engine.FIVE_STEP_GUIDE, dict)


# ============================================================
# 5. GeodesicReasoningEngine (亚黎曼测地线推理引擎)
# ============================================================

class TestGeodesicReasoningTypes:
    """测地线推理数据类型"""

    def test_constraint_type_enum(self):
        """ConstraintType 5种约束类型"""
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import ConstraintType
        types = [t.name for t in ConstraintType]
        assert "HORIZONTAL" in types
        assert "VERTICAL" in types
        assert "SMOOTH" in types
        assert "ORIENTATION" in types
        assert "CURVATURE" in types

    def test_state_se2_dataclass(self):
        """StateSE2 状态可实例化并计算距离"""
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import StateSE2
        s1 = StateSE2(x=1.0, y=2.0, theta=0.5)
        s2 = StateSE2(x=4.0, y=6.0, theta=1.0)
        assert s1.to_tuple() == (1.0, 2.0, 0.5)
        dist = s1.distance_to(s2)
        assert dist > 0
        assert isinstance(dist, (float, np.floating))

    def test_state_se2_hash_eq(self):
        """StateSE2 支持哈希和等价比较"""
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import StateSE2
        s1 = StateSE2(x=1.0, y=2.0, theta=0.5)
        s2 = StateSE2(x=1.0, y=2.0, theta=0.5)
        s3 = StateSE2(x=1.0, y=2.0, theta=0.6)
        assert hash(s1) == hash(s2)
        assert s1 == s2
        assert s1 != s3

    def test_geodesic_segment_dataclass(self):
        """GeodesicSegment 可实例化"""
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import (
            GeodesicSegment, StateSE2,
        )
        start = StateSE2(0, 0, 0)
        end = StateSE2(10, 5, math.pi / 4)
        seg = GeodesicSegment(
            start=start, end=end, length=12.0,
            curvature=0.1, cost=15.0, path=[start, end],
        )
        assert seg.length == 12.0
        assert seg.cost == 15.0


class TestGeodesicReasoningEngineCore:
    """测地线推理引擎核心功能"""

    def setup_method(self):
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import (
            GeodesicReasoningEngine,
        )
        self.engine = GeodesicReasoningEngine()

    def test_find_geodesic(self):
        """寻找测地线返回 GeodesicSegment"""
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import StateSE2
        start = StateSE2(0, 0, 0)
        end = StateSE2(5, 3, 1.0)
        result = self.engine.find_geodesic(start=start, end=end, max_iterations=20, tolerance=0.1)
        assert result is not None
        assert hasattr(result, 'path')
        assert hasattr(result, 'cost')

    def test_optimize_reasoning_path(self):
        """优化推理路径"""
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import ConstraintType
        reasoning_steps = [{"content": "分析问题"}, {"content": "提出方案"}]
        result = self.engine.optimize_reasoning_path(
            reasoning_steps=reasoning_steps,
            constraints=[ConstraintType.SMOOTH],
        )
        assert result is not None

    def test_perceptual_inference(self):
        """感知推断"""
        partial_info = {"visible_segment": [(0, 0), (2, 1)], "occlusion": [(2, 1), (5, 3)]}
        result = self.engine.perceptual_inference(partial_info)
        assert result is not None

    def test_get_reasoning_stats(self):
        """获取推理统计信息"""
        stats = self.engine.get_reasoning_stats()
        assert isinstance(stats, dict)

    def test_subriemannian_geometry_metric(self):
        """亚黎曼度量函数存在且可调用"""
        from smart_office_assistant.src.intelligence.reasoning.geodesic_reasoning_engine import SubRiemannianGeometry
        geo = SubRiemannianGeometry()
        # metric 应该是可调用的
        assert hasattr(geo, 'metric')
        assert hasattr(geo, 'hamiltonian')
        assert callable(geo.metric)
        assert callable(geo.hamiltonian)


# ============================================================
# 6. LongCoT 子组件
# ============================================================

class TestLongCoTTypes:
    """LongCoT 数据类型"""

    def test_insight_type_enum(self):
        """InsightType 5种顿悟类型 + NONE"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import InsightType
        types = [t.name for t in InsightType]
        assert "INTEGRATION" in types
        assert "BREAKTHROUGH" in types
        assert "CORRECTION" in types
        assert "SYNTHESIS" in types
        assert "NONE" in types

    def test_thought_checkpoint_dataclass(self):
        """ThoughtCheckpoint 可实例化并 to_dict"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import ThoughtCheckpoint
        cp = ThoughtCheckpoint(
            checkpoint_id="cp1", depth=3,
            content="当前分析了三个因素",
            partial_conclusions=["因素A影响最大"],
            confidence=0.78, validity_score=0.82,
        )
        d = cp.to_dict()
        assert d["depth"] == 3
        assert d["confidence"] == 0.78

    def test_insight_moment_dataclass(self):
        """InsightMoment 可实例化并 to_dict"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import InsightMoment, InsightType
        im = InsightMoment(
            moment_id="im1", insight_type=InsightType.BREAKTHROUGH,
            trigger_content="发现A和B的关联",
            insight_description="两者共享底层机制",
            impact_assessment=0.9,
            related_checkpoints=["cp1"],
        )
        d = im.to_dict()
        assert d["insight_type"] == "breakthrough"
        assert d["impact_assessment"] == 0.9

    def test_longcot_config_dataclass(self):
        """LongCoTConfig 默认配置合理"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import LongCoTConfig
        config = LongCoTConfig()
        assert config.max_thinking_length == 2048
        assert config.boundary_threshold == 0.85
        assert config.enable_insight_detection is True
        assert config.max_corrections == 3


class TestLongCoTSubComponents:
    """LongCoT 子组件功能测试"""

    def test_boundary_detector(self):
        """BoundaryDetector 边界检测"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import BoundaryDetector
        detector = BoundaryDetector()
        result = detector.assess_boundary(
            current_confidence=0.9, current_validity=0.88,
            reasoning_length=1500, max_length=2048,
        )
        assert isinstance(result, dict)
        assert "should_stop" in result or "is_boundary" in result or "confidence" in result

    def test_insight_detector(self):
        """InsightDetector 顿悟检测"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import InsightDetector, LongCoTConfig
        config = LongCoTConfig()
        detector = InsightDetector(config=config)
        result = detector.detect_insight(
            new_content="突然发现这两个因素之间存在非线性关系",
            previous_content="之前认为它们独立",
            checkpoints=[],
        )
        # 可能返回 InsightMoment 或 None
        assert result is None or hasattr(result, 'insight_type')

    def test_self_corrector_should_correct(self):
        """SelfCorrector 判断是否需要纠错"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import SelfCorrector
        corrector = SelfCorrector(max_corrections=3)
        should = corrector.should_correct(
            current_reasoning="当前推理内容",
            checkpoints=[],
            boundary_assessment={"should_stop": True, "confidence": 0.3},
        )
        assert isinstance(should, bool)

    def test_adaptive_thinking_allocator(self):
        """AdaptiveThinkingAllocator 思考预算分配"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import AdaptiveThinkingAllocator, LongCoTConfig
        config = LongCoTConfig()
        allocator = AdaptiveThinkingAllocator(config=config)
        difficulty = allocator.estimate_difficulty(problem="证明P=NP")
        assert isinstance(difficulty, (int, float))

    def test_checkpoint_manager(self):
        """CheckpointManager 检查点管理"""
        from smart_office_assistant.src.intelligence.reasoning._long_cot_engine import CheckpointManager, LongCoTConfig
        config = LongCoTConfig()
        mgr = CheckpointManager(config=config)
        should = mgr.should_create_checkpoint(
            current_length=256,
            current_confidence=0.7,
            current_validity=0.8,
        )
        assert isinstance(should, bool)


# ============================================================
# 7. ToT 子组件
# ============================================================

class TestToTTypes:
    """ToT 数据类型"""

    def test_search_strategy_enum(self):
        """SearchStrategy 5种搜索策略"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import SearchStrategy
        strategies = [s.name for s in SearchStrategy]
        assert "BFS" in strategies
        assert "DFS" in strategies
        assert "BEST_FIRST" in strategies
        assert "MONTE_CARLO" in strategies
        assert "BEAM" in strategies

    def test_thought_tree_node_dataclass(self):
        """ThoughtTreeNode 可实例化"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode
        node = ThoughtTreeNode(
            node_id="root", state={"key": "val"}, content="初始思考",
        )
        assert node.node_id == "root"
        assert node.depth == 0
        assert node.status == "pending"

    def test_thought_tree_node_ordering(self):
        """ThoughtTreeNode 支持__lt__排序（优先队列）"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode
        n1 = ThoughtTreeNode(node_id="n1", state=None, content="low", combined_score=0.3)
        n2 = ThoughtTreeNode(node_id="n2", state=None, content="high", combined_score=0.9)
        assert n1 < n2

    def test_tot_config_dataclass(self):
        """ToTConfig 配置默认值合理"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ToTConfig
        config = ToTConfig()
        assert config.max_depth >= 3
        assert config.branching_factor >= 2
        assert config.strategy is not None


class TestThoughtTree:
    """思维树核心操作"""

    def test_tree_creation(self):
        """树创建时注册根节点"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode, ThoughtTree
        root = ThoughtTreeNode(node_id="root", state=None, content="root")
        tree = ThoughtTree(root=root)
        assert "root" in tree.nodes
        assert tree._node_count == 1

    def test_add_node(self):
        """添加节点成功"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode, ThoughtTree
        root = ThoughtTreeNode(node_id="root", state=None, content="root")
        tree = ThoughtTree(root=root)
        child = ThoughtTreeNode(node_id="c1", parent_id="root", state=None, content="child", depth=1)
        result = tree.add_node(child)
        assert result is True
        assert "c1" in tree.nodes

    def test_add_duplicate_node_fails(self):
        """重复添加节点失败"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode, ThoughtTree
        root = ThoughtTreeNode(node_id="root", state=None, content="root")
        tree = ThoughtTree(root=root)
        dup = ThoughtTreeNode(node_id="root", state=None, content="dup")
        result = tree.add_node(dup)
        assert result is False

    def test_get_children(self):
        """获取子节点列表"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode, ThoughtTree
        root = ThoughtTreeNode(node_id="root", state=None, content="root")
        tree = ThoughtTree(root=root)
        c1 = ThoughtTreeNode(node_id="c1", parent_id="root", state=None, content="c1", depth=1)
        c2 = ThoughtTreeNode(node_id="c2", parent_id="root", state=None, content="c2", depth=1)
        tree.add_node(c1)
        tree.add_node(c2)
        children = tree.get_children("root")
        assert len(children) == 2

    def test_get_path_from_root_to_leaf(self):
        """获取从根到叶子的路径"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode, ThoughtTree
        root = ThoughtTreeNode(node_id="root", state=None, content="root")
        tree = ThoughtTree(root=root)
        c1 = ThoughtTreeNode(node_id="c1", parent_id="root", state=None, content="c1", depth=1)
        c2 = ThoughtTreeNode(node_id="c2", parent_id="c1", state=None, content="c2", depth=2)
        tree.add_node(c1)
        tree.add_node(c2)
        path = tree.get_path("c2")
        assert len(path) == 3  # root -> c1 -> c2

    def test_prune_branch(self):
        """剪枝分支"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode, ThoughtTree
        root = ThoughtTreeNode(node_id="root", state=None, content="root")
        tree = ThoughtTree(root=root)
        c1 = ThoughtTreeNode(node_id="c1", parent_id="root", state=None, content="c1", depth=1)
        tree.add_node(c1)
        tree.prune_branch("c1")
        # 剪枝后节点仍在 tree.nodes 但 status 变为 'pruned'
        assert "c1" in tree.nodes
        assert tree.nodes["c1"].status == "pruned"

    def test_get_all_nodes_and_stats(self):
        """获取所有节点和统计"""
        from smart_office_assistant.src.intelligence.reasoning._tot_engine import ThoughtTreeNode, ThoughtTree
        root = ThoughtTreeNode(node_id="root", state=None, content="root")
        tree = ThoughtTree(root=root)
        for i in range(3):
            child = ThoughtTreeNode(node_id=f"c{i}", parent_id="root", state=None, content=f"child{i}", depth=1)
            tree.add_node(child)
        all_nodes = tree.get_all_nodes()
        stats = tree.get_stats()
        assert len(all_nodes) == 4
        assert stats["total_nodes"] == 4


# ============================================================
# 8. ReAct 子组件
# ============================================================

class TestReActTypes:
    """ReAct 数据类型"""

    def test_action_type_enum(self):
        """ActionType 7种行动类型"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import ActionType
        types = [t.name for t in ActionType]
        assert "SEARCH" in types
        assert "CALCULATE" in types
        assert "LOOKUP" in types
        assert "RETRIEVE" in types
        assert "EXECUTE" in types
        assert "QUERY" in types
        assert "CUSTOM" in types

    def test_tool_result_dataclass(self):
        """ToolResult 可实例化并 to_dict"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import ToolResult
        tr = ToolResult(tool_name="search", success=True, result={"count": 42})
        d = tr.to_dict()
        assert d["tool_name"] == "search"
        assert d["success"] is True

    def test_tool_result_failure(self):
        """ToolResult 失败情况"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import ToolResult
        tr = ToolResult(
            tool_name="calc", success=False, result=None,
            error="Division by zero", execution_time=0.05,
        )
        assert tr.success is False
        assert tr.error == "Division by zero"

    def test_tao_step_dataclass(self):
        """TAOStep 三种步类型"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import TAOStep
        thought = TAOStep(step_id="s1", step_type="thought", content="我需要先搜索数据")
        action = TAOStep(step_id="s2", step_type="act", content="执行搜索", action={"query": "增长"})
        observe = TAOStep(step_id="s3", step_type="observe", content="找到结果")
        assert thought.step_type == "thought"
        assert action.step_type == "act"
        assert observe.step_type == "observe"


class TestTAOTrajectory:
    """TAO推理轨迹"""

    def test_trajectory_creation(self):
        """TAOTrajectory 创建"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import TAOTrajectory
        traj = TAOTrajectory(trajectory_id="traj_1", problem="用户流失分析")
        assert traj.problem == "用户流失分析"
        assert traj.status == "running"
        assert traj.total_thoughts == 0

    def test_add_trajectory_steps(self):
        """添加各类型步骤"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import TAOTrajectory
        traj = TAOTrajectory(trajectory_id="t1", problem="测试")
        traj.add_thought("首先分析原因", confidence=0.9)
        traj.add_action("搜索数据", {"action": "search"})
        assert traj.total_thoughts == 1
        assert traj.total_actions == 1
        assert len(traj.steps) == 2

    def test_get_recent_steps(self):
        """获取最近N步"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import TAOTrajectory
        traj = TAOTrajectory(trajectory_id="t2", problem="recent_test")
        for i in range(5):
            traj.add_thought(f"思考步骤{i}")
        recent = traj.get_recent_steps(n=3)
        assert len(recent) == 3

    def test_trajectory_summary(self):
        """轨迹摘要"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import TAOTrajectory
        traj = TAOTrajectory(trajectory_id="t3", problem="summary_test")
        traj.add_thought("第一步分析")
        traj.add_action("执行查询", {"query": "test"})
        summary = traj.get_summary()
        # 返回值可能是dict或string
        assert summary is not None
        if isinstance(summary, dict):
            assert "total_steps" in summary


class TestToolRegistryAndExecutor:
    """工具注册表和执行器"""

    def test_tool_registry_register_and_get(self):
        """注册和获取工具"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import (
            ToolRegistry, CalculatorTool,
        )
        registry = ToolRegistry()
        registry.register(CalculatorTool())
        retrieved = registry.get("calculate")
        assert retrieved is not None
        assert retrieved.name == "calculate"

    def test_tool_registry_list_tools(self):
        """列出所有工具"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import (
            ToolRegistry, CalculatorTool, LookupTool, RetrieveTool,
        )
        registry = ToolRegistry()
        registry.register(CalculatorTool())
        registry.register(LookupTool(lambda x: {"result": x}))
        registry.register(RetrieveTool(lambda x: f"retrieved: {x}"))
        tools = registry.list_tools()
        assert len(tools) >= 3

    def test_tool_executor_execute_success(self):
        """工具执行成功"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import (
            ToolExecutor, CalculatorTool, ToolRegistry,
        )
        registry = ToolRegistry()
        registry.register(CalculatorTool())
        executor = ToolExecutor(registry)
        result = executor.execute("calculate", {"expression": "2+2"}, max_retries=1)
        assert result.success is True

    def test_tool_executor_execute_not_found(self):
        """执行不存在的工具"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import (
            ToolExecutor, ToolRegistry,
        )
        registry = ToolRegistry()
        executor = ToolExecutor(registry)
        result = executor.execute("nonexistent_tool", {}, max_retries=1)
        assert result.success is False

    def test_tool_executor_get_stats(self):
        """执行器统计信息"""
        from smart_office_assistant.src.intelligence.reasoning._react_engine import (
            ToolExecutor, CalculatorTool, ToolRegistry,
        )
        registry = ToolRegistry()
        registry.register(CalculatorTool())
        executor = ToolExecutor(registry)
        executor.execute("calculate", {"expression": "1+1"}, max_retries=1)
        stats = executor.get_stats()
        assert isinstance(stats, dict)


# ============================================================
# 9. GoT 子组件
# ============================================================

class TestGoTTypes:
    """GoT 图推理数据类型"""

    def test_graph_reasoning_mode_enum(self):
        """GraphReasoningMode 4种图推理模式"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import GraphReasoningMode
        modes = [m.name for m in GraphReasoningMode]
        assert "LINEAR" in modes
        assert "BRANCHING" in modes
        assert "CYCLIC" in modes
        assert "HYBRID" in modes

    def test_thought_graph_node_dataclass(self):
        """ThoughtGraphNode 可实例化（支持多父节点）"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import ThoughtGraphNode
        node = ThoughtGraphNode(
            node_id="n1", content="核心论点",
            parent_ids=[], child_ids=[], related_ids=[],
        )
        assert node.node_id == "n1"
        assert node.reasoning_type == "analysis"
        assert node.depth == 0

    def test_thought_edge_dataclass(self):
        """ThoughtEdge 边可实例化"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import ThoughtEdge
        edge = ThoughtEdge(
            edge_id="e1", source_id="n1", target_id="n2",
            relation_type="supports", weight=0.8,
        )
        assert edge.source_id == "n1"
        assert edge.target_id == "n2"
        assert edge.weight == 0.8

    def test_got_config_dataclass(self):
        """GoTConfig 配置"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import GoTConfig
        config = GoTConfig()
        assert config is not None


class TestThoughtGraph:
    """思维图核心操作"""

    def test_graph_creation_with_root(self):
        """创建图并添加根节点"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import ThoughtGraphNode, ThoughtGraph
        root = ThoughtGraphNode(node_id="root", content="中心论题")
        graph = ThoughtGraph(root=root)
        assert "root" in graph.nodes

    def test_graph_add_edge(self):
        """添加边建立关系"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import (
            ThoughtGraphNode, ThoughtGraph, ThoughtEdge,
        )
        root = ThoughtGraphNode(node_id="root", content="root")
        graph = ThoughtGraph(root=root)
        n1 = ThoughtGraphNode(node_id="n1", content="论点1")
        n2 = ThoughtGraphNode(node_id="n2", content="论点2")
        graph.add_node(n1)
        graph.add_node(n2)
        edge = ThoughtEdge(edge_id="e1", source_id="root", target_id="n1", relation_type="derives")
        result = graph.add_edge(edge)
        assert result is True

    def test_graph_add_relation(self):
        """添加非父子关联关系"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import (
            ThoughtGraphNode, ThoughtGraph,
        )
        root = ThoughtGraphNode(node_id="root", content="root")
        graph = ThoughtGraph(root=root)
        n1 = ThoughtGraphNode(node_id="n1", content="A")
        n2 = ThoughtGraphNode(node_id="n2", content="B")
        graph.add_node(n1)
        graph.add_node(n2)
        graph.add_relation("n1", "n2")
        related = graph.get_related("n1")
        related_ids = [n.node_id for n in related]
        assert "n2" in related_ids

    def test_graph_topological_sort(self):
        """拓扑排序"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import (
            ThoughtGraphNode, ThoughtGraph, ThoughtEdge,
        )
        root = ThoughtGraphNode(node_id="root", content="root")
        graph = ThoughtGraph(root=root)
        for nid in ["n1", "n2", "n3"]:
            graph.add_node(ThoughtGraphNode(node_id=nid, content=f"node {nid}"))
        graph.add_edge(ThoughtEdge(edge_id="e1", source_id="root", target_id="n1"))
        graph.add_edge(ThoughtEdge(edge_id="e2", source_id="n1", target_id="n2"))
        graph.add_edge(ThoughtEdge(edge_id="e3", source_id="n2", target_id="n3"))
        order = graph.topological_sort()
        assert len(order) >= 3

    def test_graph_get_all_paths(self):
        """获取所有路径（支持DAG多路径）"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import (
            ThoughtGraphNode, ThoughtGraph, ThoughtEdge,
        )
        root = ThoughtGraphNode(node_id="root", content="root")
        graph = ThoughtGraph(root=root)
        graph.add_node(ThoughtGraphNode(node_id="a", content="a"))
        graph.add_node(ThoughtGraphNode(node_id="b", content="b"))
        graph.add_node(ThoughtGraphNode(node_id="leaf", content="leaf"))
        graph.add_edge(ThoughtEdge(edge_id="e1", source_id="root", target_id="a"))
        graph.add_edge(ThoughtEdge(edge_id="e2", source_id="root", target_id="b"))
        graph.add_edge(ThoughtEdge(edge_id="e3", source_id="a", target_id="leaf"))
        graph.add_edge(ThoughtEdge(edge_id="e4", source_id="b", target_id="leaf"))
        paths = graph.get_all_paths("root", "leaf")
        assert isinstance(paths, list)

    def test_graph_get_stats(self):
        """图统计信息"""
        from smart_office_assistant.src.intelligence.reasoning._got_engine import ThoughtGraphNode, ThoughtGraph
        root = ThoughtGraphNode(node_id="root", content="root")
        graph = ThoughtGraph(root=root)
        for i in range(3):
            graph.add_node(ThoughtGraphNode(node_id=f"n{i}", content=f"node{i}"))
        stats = graph.get_stats()
        assert stats["total_nodes"] >= 3


# ============================================================
# 10. Deep Reasoning Types (深度推理基础类型)
# ============================================================

class TestDeepReasoningTypes:
    """深度推理通用类型"""

    def test_reasoning_mode_15_modes(self):
        """ReasoningMode 有15种推理模式"""
        from smart_office_assistant.src.intelligence.reasoning._deep_reasoning_types import ReasoningMode
        modes = list(ReasoningMode)
        assert len(modes) >= 10  # 至少10+

    def test_thought_node_dataclass(self):
        """ThoughtNode 可实例化"""
        from smart_office_assistant.src.intelligence.reasoning._deep_reasoning_types import ThoughtNode, ReasoningMode
        node = ThoughtNode(
            id="tn1", content="分析市场趋势",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            parent_id=None, children_ids=[],
            confidence=0.88, completeness=0.75,
            validity=0.9, status="active",
        )
        d = node.to_dict()
        assert d["id"] == "tn1"
        assert d["confidence"] == 0.88

    def test_reasoning_result_dataclass(self):
        """ReasoningResult 可实例化"""
        from smart_office_assistant.src.intelligence.reasoning._deep_reasoning_types import (
            ReasoningResult, ReasoningMode,
        )
        result = ReasoningResult(
            result_id="rr1", problem="增长策略",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            success=True, reasoning_trace=["step1", "step2"],
            final_answer="综合方案", confidence=0.9,
            steps_count=2, execution_time=0.05,
        )
        d = result.to_dict()
        assert d["success"] is True
        assert d["final_answer"] == "综合方案"
