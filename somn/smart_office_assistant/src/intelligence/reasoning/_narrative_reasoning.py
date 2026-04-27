"""
__all__ = [
    'build_narrative_perspectives',
    'narrative_reasoning',
    'narrative_suffering_diagnosis',
    'narrative_timeline_analysis',
    'reason_from_perspective',
    'synthesize_narrative',
]

叙事推理模块
多视角叙事fusion推理 - 莫言多声部叙事 + 路遥线性叙事 + 苦难意识
"""
from typing import Dict, List

from ._deep_reasoning_types import ReasoningMode, ThoughtNode, ReasoningResult

def narrative_reasoning(
    problem: str,
    result_id: str,
    context: Dict,
    reasoning_mode: ReasoningMode = ReasoningMode.NARRATIVE_REASONING,
) -> ReasoningResult:
    """
    叙事推理 - 多视角叙事fusion推理 [v1.0.0 文学智能增强]

    """
    reasoning_trace = []

    # 步骤1: 多视角构建
    perspectives = build_narrative_perspectives(problem, context)
    node1 = ThoughtNode(
        id=f"{result_id}_perspectives",
        content=f"构建 {len(perspectives)} 个叙事视角: {', '.join(p['name'] for p in perspectives)}",
        reasoning_mode=reasoning_mode,
        confidence=0.85,
        completeness=0.8,
        validity=0.9,
        metadata={"perspectives": [p['name'] for p in perspectives]},
        status="completed"
    )
    reasoning_trace.append(node1)

    # 步骤2: 多视角并行推理
    perspective_results = []
    for i, perspective in enumerate(perspectives):
        view_result = reason_from_perspective(
            perspective, problem, context
        )
        perspective_results.append(view_result)

        node = ThoughtNode(
            id=f"{result_id}_view_{i}",
            content=f"[{perspective['name']}] {view_result['summary']}",
            reasoning_mode=reasoning_mode,
            parent_id=node1.id,
            confidence=view_result.get("confidence", 0.75),
            completeness=view_result.get("completeness", 0.8),
            validity=view_result.get("validity", 0.8),
            metadata={
                "perspective": perspective['name'],
                "key_findings": view_result.get("key_findings", []),
                "blind_spots": view_result.get("blind_spots", [])
            },
            status="completed"
        )
        reasoning_trace.append(node)
        node1.children_ids.append(node.id)

    # 步骤3: 时间轴推演
    timeline = narrative_timeline_analysis(problem, perspective_results, context)
    node_timeline = ThoughtNode(
        id=f"{result_id}_timeline",
        content=f"时间轴推演: 过去({len(timeline.get('past', []))}个因果) → "
                f"现在({len(timeline.get('present', []))}个状态) → "
                f"未来({len(timeline.get('future', []))}个预测)",
        reasoning_mode=reasoning_mode,
        parent_id=node1.id,
        confidence=0.82,
        completeness=0.85,
        validity=0.85,
        metadata={"timeline": timeline},
        status="completed"
    )
    reasoning_trace.append(node_timeline)

    # 步骤4: 苦难诊断
    suffering_diagnosis = narrative_suffering_diagnosis(
        problem, perspective_results, timeline, context
    )
    node_suffering = ThoughtNode(
        id=f"{result_id}_suffering",
        content=f"苦难诊断: 发现 {len(_get_rc_list(suffering_diagnosis))} 个深层困境根源",
        reasoning_mode=reasoning_mode,
        parent_id=node_timeline.id,
        confidence=0.80,
        completeness=0.9,
        validity=0.85,
        metadata=suffering_diagnosis,
        status="completed"
    )
    reasoning_trace.append(node_suffering)

    # 步骤5: 叙事synthesize
    narrative_synthesis = synthesize_narrative(
        problem, perspective_results, timeline, suffering_diagnosis, context
    )
    node_synthesis = ThoughtNode(
        id=f"{result_id}_synthesis",
        content=f"叙事synthesize: {narrative_synthesis['narrative_arc']}",
        reasoning_mode=reasoning_mode,
        parent_id=node_suffering.id,
        confidence=narrative_synthesis.get("confidence", 0.85),
        completeness=1.0,
        validity=narrative_synthesis.get("validity", 0.88),
        metadata=narrative_synthesis,
        status="completed"
    )
    reasoning_trace.append(node_synthesis)

    # 计算synthesize置信度
    all_confidences = [n.confidence for n in reasoning_trace]
    avg_confidence = sum(all_confidences) / len(all_confidences)

    return ReasoningResult(
        result_id=result_id,
        problem=problem,
        reasoning_mode=reasoning_mode,
        success=True,
        reasoning_trace=reasoning_trace,
        final_answer=narrative_synthesis.get("final_answer", ""),
        confidence=avg_confidence,
        steps_count=len(reasoning_trace),
        suggestions=narrative_synthesis.get("suggestions", []),
        metadata={
            "narrative_type": "multi_perspective_temporal",
            "perspectives_count": len(perspectives),
            "root_causes_count": len(_get_rc_list(suffering_diagnosis))
        }
    )

def _get_rc_list(suffering: Dict) -> List:
    """安全提取 root_causes 列表"""
    rc = suffering.get("root_causes", [])
    return rc if isinstance(rc, list) else []

def build_narrative_perspectives(problem: str, context: Dict) -> List[Dict]:
    """
    构建叙事视角 - 莫言多声部叙事方法论

    默认5个核心视角:
    1. 用户视角  2. 企业视角  3. 市场视角  4. 竞争视角  5. 社会视角
    """
    default_perspectives = [
        {"name": "用户视角", "role": "消费者/客户",
         "focus": "需求痛点,使用体验,情感诉求,decision路径",
         "question_prefix": "从用户的切身感受出发", "weight": 0.25},
        {"name": "企业视角", "role": "经营decision者",
         "focus": "资源约束,战略目标,组织能力,商业模式",
         "question_prefix": "从企业经营的实际情况出发", "weight": 0.25},
        {"name": "市场视角", "role": "行业观察者",
         "focus": "趋势变化,市场规模,政策环境,技术革新",
         "question_prefix": "从宏观市场环境出发", "weight": 0.20},
        {"name": "竞争视角", "role": "竞争分析者",
         "focus": "竞争格局,差异化优势,护城河,替代威胁",
         "question_prefix": "从竞争对手的角度出发", "weight": 0.15},
        {"name": "社会视角", "role": "社会文化解读",
         "focus": "文化变迁,价值观演进,社会责任,长期影响",
         "question_prefix": "从社会文化趋势出发", "weight": 0.15}
    ]

    # 根据行业动态调整
    industry = (context or {}).get("industry", "")
    if industry:
        if "医疗" in industry or "健康" in industry:
            default_perspectives.insert(2, {
                "name": "监管视角", "role": "合规审视者",
                "focus": "政策法规,医疗合规,医保控费,行业准入",
                "question_prefix": "从医疗监管环境出发", "weight": 0.20
            })
        elif "金融" in industry or "银行" in industry or "保险" in industry:
            default_perspectives.insert(2, {
                "name": "风险视角", "role": "风险管理者",
                "focus": "金融风险,合规要求,监管政策,信用风险",
                "question_prefix": "从金融风险角度出发", "weight": 0.20
            })

    return default_perspectives

def reason_from_perspective(perspective: Dict, problem: str, context: Dict) -> Dict:
    """从单一视角进行推理"""
    focus_areas = perspective["focus"].split(",")

    relevant_findings = []
    blind_spots = []

    for area in focus_areas:
        problem_lower = problem.lower()
        area_keywords = area

        if any(kw in problem_lower for kw in area_keywords):
            relevant_findings.append(f'发现与"{area}"相关的核心问题')
        else:
            blind_spots.append(f'可能忽略了"{area}"维度')

    if not relevant_findings:
        relevant_findings.append(
            f"{perspective['question_prefix']},{perspective['role']}最关注: "
            f"{perspective['focus']}"
        )

    return {
        "perspective": perspective["name"],
        "summary": f"{perspective['role']}视角下发现 {len(relevant_findings)} 个关键洞察",
        "key_findings": relevant_findings,
        "blind_spots": blind_spots[:3],
        "confidence": min(0.90, 0.70 + len(relevant_findings) * 0.05),
        "completeness": max(0.6, 1.0 - len(blind_spots) * 0.1),
        "validity": 0.85
    }

def narrative_timeline_analysis(
    problem: str,
    perspective_results: List[Dict],
    context: Dict
) -> Dict:
    """
    时间轴推演 - 路遥式线性叙事分析
    将问题置于时间流中: 过去→现在→未来
    """
    timeline = {"past": [], "present": [], "future": []}

    all_findings = []
    for pr in perspective_results:
        all_findings.extend(pr.get("key_findings", []))

    timeline["past"] = [
        f"历史沿革: 该问题的形成有其历史必然性",
        f"积累效应: 当前问题可能是长期积累的结果"
    ]

    timeline["present"] = [
        f"核心矛盾: {problem[:50]}",
        f"多元冲突: 存在 {len(perspective_results)} 个不同视角的诉求差异",
        f"资源约束: 现有资源难以同时满足所有维度的需求"
    ]

    timeline["future"] = [
        "趋势延续: 如果不干预,现有矛盾可能进一步加剧",
        "破局窗口: 存在2-3个可能的战略转折点",
        "最优路径: synthesize多视角需求,存在协同优化的可能"
    ]

    return timeline

def narrative_suffering_diagnosis(
    problem: str,
    perspective_results: List[Dict],
    timeline: Dict,
    context: Dict
) -> Dict:
    """
    苦难诊断 - 路遥"苦难意识"方法论
    诊断维度: 结构性困境 / 认知性困境 / 执行性困境
    """
    root_causes = []
    breakthrough_points = []

    all_blind_spots = []
    for pr in perspective_results:
        all_blind_spots.extend(pr.get("blind_spots", []))

    if len(perspective_results) >= 3:
        root_causes.append({
            "type": "structural",
            "description": "多视角冲突揭示结构性矛盾",
            "severity": "high",
            "evidence": f"{len(perspective_results)}个视角存在诉求差异"
        })

    if all_blind_spots:
        root_causes.append({
            "type": "cognitive",
            "description": f"存在 {len(all_blind_spots)} 个认知盲区",
            "severity": "medium",
            "evidence": "; ".join(all_blind_spots[:3])
        })

    root_causes.append({
        "type": "execution",
        "description": "资源与能力约束",
        "severity": "medium",
        "evidence": "现有执行能力可能不足以支撑全面解决方案"
    })

    if timeline.get("future"):
        breakthrough_points.append("时间窗口: 抓住关键转折期")
    if len(perspective_results) > 1:
        breakthrough_points.append("视角fusion: 将冲突诉求转化为协同优势")
    breakthrough_points.append("渐进突破: 分阶段,分优先级解决困境")

    return {
        "root_causes": root_causes,
        "breakthrough_points": breakthrough_points,
        "overall_severity": "high" if any(
            rc["severity"] == "high" for rc in root_causes
        ) else "medium"
    }

def synthesize_narrative(
    problem: str,
    perspective_results: List[Dict],
    timeline: Dict,
    suffering_diagnosis: Dict,
    context: Dict
) -> Dict:
    """
    叙事synthesize - 将所有分析fusion为一个完整的解决方案叙事
    叙事弧线: 起-承-转-合
    """
    narrative_arc = (
        f"起: {problem[:80]}... "
        f"| 承: 通过{len(perspective_results)}个视角分析,发现深层困境根源 "
        f"| 转: recognize{len(suffering_diagnosis.get('breakthrough_points', []))}个破局点 "
        f"| 合: fusion多维度洞察,构建系统性解决方案"
    )

    key_insights = []
    for pr in perspective_results:
        key_insights.extend(pr.get("key_findings", [])[:1])

    breakthroughs = suffering_diagnosis.get("breakthrough_points", [])

    final_answer = (
        f"基于叙事推理的synthesize分析:\n"
        f"1. 多视角洞察: {'; '.join(key_insights[:3])}\n"
        f"2. 时间轴推演: 该问题有历史积累,当前处于关键转折期\n"
        f"3. 深层诊断: {suffering_diagnosis.get('overall_severity', 'medium')}级别困境, "
        f"{len(suffering_diagnosis.get('root_causes', []))}个根源待解决\n"
        f"4. 破局方向: {'; '.join(breakthroughs[:3])}"
    )

    suggestions = [
        "建议结合链式推理细化执行步骤",
        "可使用树推理探索更多可能路径",
        "建议对关键假设进行元推理验证"
    ]

    return {
        "narrative_arc": narrative_arc,
        "final_answer": final_answer,
        "confidence": 0.85,
        "validity": 0.88,
        "suggestions": suggestions,
        "key_insights": key_insights,
        "breakthrough_points": breakthroughs
    }
