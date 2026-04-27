# -*- coding: utf-8 -*-
"""
__all__ = [
    'dewey_thinking_reasoning',
]

杜威反省思维推理模块
dewey_thinking_reasoning standalone 函数

核心原理: 约翰·杜威<我们如何思维>
- 反省思维 = 连续性检验与重构的思维过程
- 五步法: 困难→问题→假设→推理→检验
"""

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ._dre_base import DeepReasoningEngine

def dewey_thinking_reasoning(
    engine: "DeepReasoningEngine",
    problem: str,
    result_id: str,
    context: Dict,
):
    """
    杜威反省思维推理 [v1.0.0]

    推理步骤:
    1. 感知困难 - 发现思维卡点
    2. 界定问题 - 精确化问题
    3. 提出假设 - 多元假设generate
    4. 演绎推理 - 假设→逻辑推论
    5. 实验检验 - 用action/数据验证
    6. 修正迭代 - 基于反馈优化
    """
    from ._dre_types import ReasoningMode, ThoughtNode, ReasoningResult

    reasoning_trace = []

    # ---- 步骤1: 感知困难 ----
    difficulty_keywords = ['困难', '卡', '难', '不知', '矛盾', '冲突', '痛点']
    detected_difficulty = any(k in problem for k in difficulty_keywords)

    node1 = ThoughtNode(
        id=f"{result_id}_difficulty",
        content=f"感知困难: 发现思维卡点,"
                f"问题存在实质性困难需要解决",
        reasoning_mode=ReasoningMode.DEWEY_THINKING,
        confidence=0.9 if detected_difficulty else 0.7,
        completeness=0.85, validity=0.9,
        metadata={"difficulty_detected": detected_difficulty},
        status="completed"
    )
    reasoning_trace.append(node1)

    # ---- 步骤2: 界定问题 ----
    sub_problems = engine._decompose_problem(problem)
    problem_definition = f"核心问题: {problem}"
    if len(sub_problems) > 1:
        problem_definition += f"\n分解为{len(sub_problems)}个子问题"

    node2 = ThoughtNode(
        id=f"{result_id}_define",
        content=f"界定问题: 将模糊困难精确化,"
                f"形成{len(sub_problems)}个可操作的问题单元",
        reasoning_mode=ReasoningMode.DEWEY_THINKING,
        parent_id=node1.id,
        confidence=0.88, completeness=0.9, validity=0.9,
        metadata={"sub_problems": sub_problems},
        status="completed"
    )
    reasoning_trace.append(node2)

    # ---- 步骤3: 提出假设 ----
    hypotheses = []
    actions = ["采取保守strategy", "引入新方法", "重构问题框架", "寻求外部资源"]
    for i, sub in enumerate(sub_problems[:4]):
        hyp = {
            "id": f"H{i+1}",
            "description": f"假设{i+1}: {sub}",
            "action": actions[i % len(actions)],
            "confidence": 0.7 + (0.05 * (3 - i))
        }
        hypotheses.append(hyp)

    node3 = ThoughtNode(
        id=f"{result_id}_hypothesis",
        content=f"提出假设: generate{len(hypotheses)}个候选假设,"
                f"为每种可能性提供action方向",
        reasoning_mode=ReasoningMode.DEWEY_THINKING,
        parent_id=node2.id,
        confidence=0.8, completeness=0.85, validity=0.82,
        metadata={"hypotheses": hypotheses},
        status="completed"
    )
    reasoning_trace.append(node3)

    # ---- 步骤4: 演绎推理 ----
    deductions = []
    for hyp in hypotheses:
        deduction = {
            "from": hyp["id"],
            "if_true": f"若{hyp['action']},则预期出现可观测的改善",
            "then": f"问题将得到部分/完全解决"
        }
        deductions.append(deduction)

    node4 = ThoughtNode(
        id=f"{result_id}_deduction",
        content=f"演绎推理: 从{len(hypotheses)}个假设推演逻辑结论,"
                f"建立假设→结论的推理链",
        reasoning_mode=ReasoningMode.DEWEY_THINKING,
        parent_id=node3.id,
        confidence=0.82, completeness=0.85, validity=0.85,
        metadata={"deductions": deductions},
        status="completed"
    )
    reasoning_trace.append(node4)

    # ---- 步骤5: 实验检验 ----
    verifications = []
    for i, (hyp, ded) in enumerate(zip(hypotheses, deductions)):
        verification = {
            "test_hypothesis": hyp["id"],
            "method": f"设计实验验证: 对假设{i+1}进行小范围实验",
            "success_criteria": ded["then"],
            "expected_outcome": "通过数据或实践结果验证假设成立性"
        }
        verifications.append(verification)

    node5 = ThoughtNode(
        id=f"{result_id}_verification",
        content=f"实验检验: 设计{len(verifications)}个验证方案,"
                f"通过小规模实验get数据",
        reasoning_mode=ReasoningMode.DEWEY_THINKING,
        parent_id=node4.id,
        confidence=0.8, completeness=0.8, validity=0.88,
        metadata={"verifications": verifications},
        status="completed"
    )
    reasoning_trace.append(node5)

    # ---- 步骤6: 修正迭代 ----
    refinement_note = "根据实验结果,修正或确认假设,形成螺旋上升的认知"

    node6 = ThoughtNode(
        id=f"{result_id}_refine",
        content=f"修正迭代: 接纳检验结果,迭代优化认知框架,"
                f"确保思维持续精进",
        reasoning_mode=ReasoningMode.DEWEY_THINKING,
        parent_id=node5.id,
        confidence=0.82, completeness=0.8, validity=0.85,
        metadata={"refinement": refinement_note},
        status="completed"
    )
    reasoning_trace.append(node6)

    # synthesize答案
    final_answer = f"[杜威反省思维]\n{problem_definition}\n\n"
    final_answer += f"核心假设(H1推荐): {hypotheses[0]['description']}\n"
    final_answer += f"action: {hypotheses[0]['action']}\n"
    final_answer += f"验证: {verifications[0]['method']}\n\n"
    final_answer += "反省思维精髓: 不是找正确答案,而是通过系统性检验不断提升认知"

    return ReasoningResult(
        result_id=result_id,
        problem=problem,
        reasoning_mode=ReasoningMode.DEWEY_THINKING,
        success=True,
        reasoning_trace=reasoning_trace,
        final_answer=final_answer,
        confidence=0.85,
        steps_count=len(reasoning_trace),
        suggestions=[
            f"优先检验H1假设(置信度最高: {hypotheses[0]['confidence']:.0%})",
            "在真实环境中小范围验证后再大规模推广",
            "将检验结果记录,为后续迭代提供数据",
            "杜威五步法可循环迭代,每次迭代深化认知"
        ],
        metadata={
            "dewey_methodology": [
                "1. 感知困难 - 发现并承认问题存在",
                "2. 界定问题 - 精确化问题的边界和性质",
                "3. 提出假设 - 多元假设generate,不急于定论",
                "4. 演绎推理 - 从假设推演可检验的结论",
                "5. 实验检验 - 通过action或数据验证假设"
            ],
            "hypotheses_count": len(hypotheses),
            "verifications_count": len(verifications)
        }
    )
