# -*- coding: utf-8 -*-
"""
__all__ = [
    'xinmind_reasoning',
]

王阳明心学推理模块
xinmind_reasoning standalone 函数

核心原理: 知行合一,致良知
- 心即理: 万事万物之理不在心外,吾心即宇宙
- 知行合一: 知而不行,只是未知;行而后知,真知
- 致良知: 扩充恻隐之心,去除私欲遮蔽
- 事上磨练: 在具体事务中修炼心性
"""

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ._dre_base import DeepReasoningEngine

def xinmind_reasoning(
    engine: "DeepReasoningEngine",
    problem: str,
    result_id: str,
    context: Dict,
):
    """
    王阳明心学思维推理 [v7.0.0]

    推理步骤:
    1. 诚意正心 - 去除私欲,显良知本体
    2. 格物致知 - 在事上穷理,触发直觉洞见
    3. 知行互发 - 知驱动行,行深化知
    4. 事上磨练 - 将领悟付诸实践验证
    5. 致其良知 - 最终答案由良知自然流露
    """
    from ._dre_types import ReasoningMode, ThoughtNode, ReasoningResult

    reasoning_trace = []

    # ---- 步骤1: 诚意正心 ----
    distractions = []
    for kw in ['焦虑', '担忧', '恐惧', '犹豫', '纠结', '患得患失']:
        if kw in problem:
            distractions.append(kw)

    clean_problem = problem
    if distractions:
        clean_problem = f"[去除{','.join(distractions)}遮蔽后] {problem}"

    node1 = ThoughtNode(
        id=f"{result_id}_chengyi",
        content=f"诚意正心: recognize并去除{len(distractions)}种私欲遮蔽,"
                f"显良知本体" if distractions else "心体澄明,无私欲遮蔽",
        reasoning_mode=ReasoningMode.XINMIND_THINKING,
        confidence=0.9, completeness=0.9, validity=0.95,
        metadata={"distractions_removed": distractions},
        status="completed"
    )
    reasoning_trace.append(node1)

    # ---- 步骤2: 格物致知 ----
    sub_issues = engine._decompose_problem(clean_problem)
    intuitive_insights = []

    for issue in sub_issues:
        insight_types = [
            f"此问题之'理'不在外--向内探求,答案已在吾心",
            f"此事应从{len(sub_issues)}个维度应对,但根本在'心'",
            f"问题即道场,磨砺处即成长处",
            f"若致良知,此事当如何处置?"
        ]
        intuitive_insights.append({
            "issue": issue,
            "insight": insight_types[len(intuitive_insights) % len(insight_types)]
        })

    node2 = ThoughtNode(
        id=f"{result_id}_gewu",
        content=f"格物致知: 从{len(sub_issues)}个角度穷究事物之理,"
                f"触发直觉洞见",
        reasoning_mode=ReasoningMode.XINMIND_THINKING,
        parent_id=node1.id,
        confidence=0.8, completeness=0.85, validity=0.88,
        metadata={"intuitions": intuitive_insights},
        status="completed"
    )
    reasoning_trace.append(node2)

    # ---- 步骤3: 知行互发 ----
    knowledge_action_pairs = []
    for i, insight in enumerate(intuitive_insights):
        pair = {
            "insight": insight["insight"],
            "action": f"action{i+1}: 依此洞见调整认知与行为"
        }
        knowledge_action_pairs.append(pair)

    node3 = ThoughtNode(
        id=f"{result_id}_zhixing",
        content=f"知行互发: {len(knowledge_action_pairs)}组知行对相互激发,"
                f"知→行→真知循环",
        reasoning_mode=ReasoningMode.XINMIND_THINKING,
        parent_id=node2.id,
        confidence=0.82, completeness=0.8, validity=0.85,
        metadata={"pairs": knowledge_action_pairs},
        status="completed"
    )
    reasoning_trace.append(node3)

    # ---- 步骤4: 事上磨练 ----
    practical_tests = []
    for pair in knowledge_action_pairs:
        test = {
            "scenario": "在具体实践中检验此认知",
            "expected": "action带来新的认知深化",
            "method": "切实践行,不离事上磨练"
        }
        practical_tests.append(test)

    node4 = ThoughtNode(
        id=f"{result_id}_moyan",
        content=f"事上磨练: 在{len(practical_tests)}个实践场景中验证洞见,"
                f"知与行在事中合一",
        reasoning_mode=ReasoningMode.XINMIND_THINKING,
        parent_id=node3.id,
        confidence=0.85, completeness=0.85, validity=0.88,
        metadata={"tests": practical_tests},
        status="completed"
    )
    reasoning_trace.append(node4)

    # ---- 步骤5: 致其良知 ----
    core_answer = f"致良知而解此难--心体澄明时,答案自现."
    if sub_issues:
        core_answer += f"\n根本之道: {'; '.join([f'{i+1}.{issue}' for i, issue in enumerate(sub_issues[:3])])}"
    if intuitive_insights:
        key_insight = intuitive_insights[0].get("insight", "")
        if key_insight:
            core_answer += f"\n核心洞见: {key_insight}"

    node5 = ThoughtNode(
        id=f"{result_id}_liangzhi",
        content="致其良知: 私欲尽去,良知本体呈现,"
                "答案如镜中影,自然而然",
        reasoning_mode=ReasoningMode.XINMIND_THINKING,
        parent_id=node4.id,
        confidence=0.9, completeness=0.95, validity=0.92,
        status="completed"
    )
    reasoning_trace.append(node5)

    return ReasoningResult(
        result_id=result_id,
        problem=problem,
        reasoning_mode=ReasoningMode.XINMIND_THINKING,
        success=True,
        reasoning_trace=reasoning_trace,
        final_answer=core_answer,
        confidence=0.88,
        steps_count=len(reasoning_trace),
        suggestions=[
            "知而不行,只是未知--立即action验证此洞见",
            "在具体事务中磨练,不离事上用功",
            "每日省察,去除私欲,致其良知",
            "此问题若出自良知,应如何应对?"
        ],
        metadata={
            "xinmind_principles": [
                "心即理 - 万事之理不在心外",
                "知行合一 - 知是行的开始,行是知的完成",
                "致良知 - 去除私欲遮蔽,良知自然呈现",
                "事上磨练 - 在具体实践中验证和深化认知"
            ],
            "practical_tests_count": len(practical_tests),
            "intuitions_count": len(intuitive_insights)
        }
    )
