# -*- coding: utf-8 -*-
"""
__all__ = [
    'neurodynamics_reasoning',
]

神经动力学推理模块
neurodynamics_reasoning standalone 函数
"""

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ._dre_base import DeepReasoningEngine

def neurodynamics_reasoning(
    engine: "DeepReasoningEngine",
    problem: str,
    result_id: str,
    context: Dict,
):
    """
    神经动力学推理 - 模拟大脑节律的深度思考 [v1.0.0]

    推理步骤:
    1. 节律init - 确定各模块的工作节律模式
    2. 发散探索(静默期) - 广泛收集信息,注入噪声激发创意
    3. 聚焦推理(放电期) - 高强度深度推理
    4. 相位协调 - 同步各模块的推理结果
    5. 突触巩固 - 通过STDP强化关键关联
    6. E-I诊断 - 检查系统平衡状态
    """
    from ._dre_types import ReasoningMode, ThoughtNode, ReasoningResult

    reasoning_trace = []

    if not getattr(engine, "neurodynamics", None):
        return ReasoningResult(
            result_id=result_id, problem=problem,
            reasoning_mode=ReasoningMode.NEURODYNAMICS,
            success=False, reasoning_trace=[],
            final_answer="神经动力学系统未加载"
        )

    # ---- 步骤1: 节律init ----
    rhythm_mode = "creative" if any(k in problem for k in ['创新', '创造', '新', '突破']) else "focused"
    phase_coord = getattr(engine, "phase_coordinator", None)
    if phase_coord:
        phase_coord.set_rhythm_mode(rhythm_mode)

    node1 = ThoughtNode(
        id=f"{result_id}_rhythm_init",
        content=f"节律init: 切换到'{rhythm_mode}'模式, "
                f"各模块开始协调工作",
        reasoning_mode=ReasoningMode.NEURODYNAMICS,
        confidence=0.9, completeness=1.0, validity=0.95,
        metadata={"rhythm_mode": rhythm_mode},
        status="completed"
    )
    reasoning_trace.append(node1)

    # ---- 步骤2: 发散探索(静默期) ----
    sub_problems = engine._decompose_problem(problem)
    divergent_insights = []

    neuro = getattr(engine, "neurodynamics", None)
    for sp in sub_problems:
        if neuro:
            sr_result = neuro.enhance_signal(0.3)
            if sr_result.enhanced:
                divergent_insights.append(f"[随机共振] {sp} → 发现新的关联角度")
            else:
                divergent_insights.append(f"[常规] {sp}")

    node2 = ThoughtNode(
        id=f"{result_id}_divergent",
        content=f"发散探索: generate{len(divergent_insights)}个探索方向, "
                f"其中随机共振增强{sum(1 for i in divergent_insights if '随机共振' in i)}个",
        reasoning_mode=ReasoningMode.NEURODYNAMICS,
        parent_id=node1.id,
        confidence=0.75, completeness=0.8, validity=0.7,
        metadata={"insights": divergent_insights},
        status="completed"
    )
    reasoning_trace.append(node2)

    # ---- 步骤3: 聚焦推理(放电期) ----
    solutions = []
    for sub_problem in sub_problems:
        solution = engine._solve_sub_problem(sub_problem, context)
        solutions.append(solution)
        if neuro:
            neuro.stimulate("reasoning", 0.8)

    node3 = ThoughtNode(
        id=f"{result_id}_focused",
        content=f"聚焦推理: 完成{len(sub_problems)}个子问题求解, "
                f"深度思考激活",
        reasoning_mode=ReasoningMode.NEURODYNAMICS,
        parent_id=node2.id,
        confidence=0.85, completeness=0.9, validity=0.85,
        metadata={"solutions_count": len(solutions)},
        status="completed"
    )
    reasoning_trace.append(node3)

    # ---- 步骤4: 相位协调 ----
    sync_report = {}
    if phase_coord:
        for _ in range(5):
            phase_coord.step()
        sync_report = phase_coord.get_report()

    node4 = ThoughtNode(
        id=f"{result_id}_sync",
        content=f"相位协调: 同步序参量={sync_report.get('order_parameter', 'N/A')}, "
                f"状态={sync_report.get('sync_status', 'N/A')}",
        reasoning_mode=ReasoningMode.NEURODYNAMICS,
        parent_id=node3.id,
        confidence=0.8, completeness=0.85, validity=0.8,
        metadata=sync_report,
        status="completed"
    )
    reasoning_trace.append(node4)

    # ---- 步骤5: 突触巩固 ----
    plasticity_report = {}
    synaptic = getattr(engine, "synaptic_engine", None)
    if synaptic:
        for i in range(min(3, len(sub_problems))):
            synaptic.co_activate(
                "reasoning", "memory",
                pre_activation=0.8, post_activation=0.7,
                learning_rule="stdp"
            )
        plasticity_report = synaptic.get_plasticity_report()

    node5 = ThoughtNode(
        id=f"{result_id}_consolidation",
        content=f"突触巩固: 通过STDP强化推理-记忆关联, "
                f"突触数={plasticity_report.get('total_synapses', 0)}",
        reasoning_mode=ReasoningMode.NEURODYNAMICS,
        parent_id=node4.id,
        confidence=0.8, completeness=0.8, validity=0.85,
        metadata=plasticity_report,
        status="completed"
    )
    reasoning_trace.append(node5)

    # ---- 步骤6: E-I平衡诊断 ----
    ei_diagnosis = {}
    if neuro:
        neuro.update_ei_balance(0.2, -0.1)
        ei_state = neuro.ei_balancer.get_regime_diagnosis()
        ei_diagnosis = ei_state

    node6 = ThoughtNode(
        id=f"{result_id}_ei_balance",
        content=f"E-I平衡诊断: {ei_diagnosis.get('current_regime', 'N/A')}, "
                f"E/I比率={ei_diagnosis.get('balance_ratio', 'N/A')}",
        reasoning_mode=ReasoningMode.NEURODYNAMICS,
        parent_id=node5.id,
        confidence=0.85, completeness=0.85, validity=0.9,
        metadata=ei_diagnosis,
        status="completed"
    )
    reasoning_trace.append(node6)

    # ---- synthesize答案 ----
    final_answer = engine._synthesize_answer(problem, solutions)

    if ei_diagnosis.get('recommendation'):
        final_answer += f"\n\n[神经动力学诊断] {ei_diagnosis['recommendation']}"

    dynamics_report = {}
    if neuro:
        dynamics_report = neuro.get_system_dynamics_report()

    return ReasoningResult(
        result_id=result_id,
        problem=problem,
        reasoning_mode=ReasoningMode.NEURODYNAMICS,
        success=True,
        reasoning_trace=reasoning_trace,
        final_answer=final_answer,
        confidence=0.85,
        steps_count=len(reasoning_trace),
        suggestions=[
            "考虑使用簇放电模式进行更深层次的思考循环",
            "通过调整E-I平衡可以切换探索/利用strategy",
            "随机共振机制可以帮助发现弱信号中的隐藏关联"
        ],
        metadata={
            "dynamics_report": dynamics_report,
            "rhythm_mode": rhythm_mode,
            "neuroscience_foundations": [
                "Ch.5 簇放电振荡 - 聚焦/发散节律",
                "Ch.8 Kuramoto耦合 - 多模块相位同步",
                "Ch.10 随机共振 - 噪声增强弱信号",
                "Ch.9 Wilson-Cowan - E-I兴奋抑制平衡",
                "Ch.7 STDP - 脉冲时序依赖可塑性"
            ]
        }
    )
