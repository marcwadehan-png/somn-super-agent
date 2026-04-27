"""
__all__ = [
    'anchor_solution_users',
    'consulting_bottom_up_check',
    'consulting_constraint_reverse',
    'consulting_contradiction_detection',
    'consulting_fallacy_check',
    'consulting_reasoning',
    'consulting_reasoning_with_rules',
    'consulting_research_scan',
    'consulting_user_anchoring',
    'detect_solution_constraints',
    'detect_solution_contradictions',
    'synthesize_consulting_answer',
]

咨询推理模块
战略咨询专用推理链 - 五维调研 + 矛盾检测 + 约束反推 + 用户锚定 + 执行反推 + 谬误自检
"""
import logging
import re
from typing import Dict, List, Optional, Any

from ._deep_reasoning_types import ReasoningMode, ThoughtNode, ReasoningResult

logger = logging.getLogger(__name__)
def consulting_reasoning(
    problem: str,
    result_id: str,
    context: Dict,
    consulting_validator: Any = None,
    fallacy_detector: Any = None,
) -> ReasoningResult:
    """
    咨询推理 - 战略咨询专用推理链 [v1.0.0 增长咨询增强]

    基于企业增长战略咨询全过程的方法论抽象.
    遵循"调研→思考→分析→验证"四阶段推理链.

    推理步骤:
    1. 五维调研扫描 - 企业/用户/竞争/市场/风险
    2. 核心矛盾recognize - 找到根本不相容的要素
    3. 约束反推目标 - 不问能做多大,问资源能撑多大
    4. 用户需求锚定 - 验证"用户为什么买单"
    5. 执行层反推 - 从最小执行单元向上累加
    6. 谬误自检 - 逻辑谬误+战略咨询谬误双重检测

    Args:
        problem: 问题描述
        result_id: 推理结果 ID
        context: 上下文字典
        consulting_validator: 咨询验证器实例(可选)
        fallacy_detector: 谬误检测器实例(可选)
    """
    reasoning_trace = []

    # 步骤1: 五维调研扫描
    research_scan = consulting_research_scan(problem, context)
    node1 = ThoughtNode(
        id=f"{result_id}_research",
        content=f"五维调研扫描: {research_scan['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        confidence=0.80,
        completeness=research_scan.get('completeness', 0.5),
        validity=0.85,
        metadata={
            "dimensions_covered": research_scan.get('dimensions', []),
            "gaps": research_scan.get('gaps', [])
        },
        status="completed"
    )
    reasoning_trace.append(node1)

    # 步骤2: 核心矛盾recognize
    contradiction_analysis = consulting_contradiction_detection(problem, context)
    node2 = ThoughtNode(
        id=f"{result_id}_contradiction",
        content=f"核心矛盾recognize: 发现 {len(contradiction_analysis.get('contradictions', []))} 个潜在矛盾",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node1.id,
        confidence=0.82,
        completeness=1.0,
        validity=0.85,
        metadata=contradiction_analysis,
        status="completed"
    )
    reasoning_trace.append(node2)

    # 步骤3: 约束反推目标
    constraint_analysis = consulting_constraint_reverse(problem, context)
    node3 = ThoughtNode(
        id=f"{result_id}_constraint",
        content=f"约束反推: {constraint_analysis['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node2.id,
        confidence=0.78,
        completeness=constraint_analysis.get('completeness', 0.7),
        validity=0.85,
        metadata=constraint_analysis,
        status="completed"
    )
    reasoning_trace.append(node3)

    # 步骤4: 用户需求锚定
    user_anchor = consulting_user_anchoring(problem, context)
    node4 = ThoughtNode(
        id=f"{result_id}_user_anchor",
        content=f"用户锚定: {user_anchor['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node3.id,
        confidence=0.80,
        completeness=user_anchor.get('completeness', 0.7),
        validity=0.82,
        metadata=user_anchor,
        status="completed"
    )
    reasoning_trace.append(node4)

    # 步骤5: 执行层反推
    execution_check = consulting_bottom_up_check(problem, context)
    node5 = ThoughtNode(
        id=f"{result_id}_execution",
        content=f"执行反推: {execution_check['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node4.id,
        confidence=0.78,
        completeness=execution_check.get('completeness', 0.6),
        validity=0.80,
        metadata=execution_check,
        status="completed"
    )
    reasoning_trace.append(node5)

    # 步骤6: 谬误自检(逻辑谬误 + 战略咨询谬误)
    fallacy_check = consulting_fallacy_check(problem, fallacy_detector=fallacy_detector)
    node6 = ThoughtNode(
        id=f"{result_id}_fallacy",
        content=f"谬误自检: 检测到 {len(fallacy_check.get('detections', []))} 个潜在谬误",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node5.id,
        confidence=0.85,
        completeness=1.0,
        validity=0.90,
        metadata=fallacy_check,
        status="completed"
    )
    reasoning_trace.append(node6)

    # synthesize结果
    all_confidences = [n.confidence for n in reasoning_trace]
    avg_confidence = sum(all_confidences) / len(all_confidences)

    # 如果有致命谬误或核心矛盾,降低整体置信度
    critical_count = len(fallacy_check.get('critical', []))
    contradiction_count = len(contradiction_analysis.get('contradictions', []))
    if critical_count > 0:
        avg_confidence *= 0.6
    elif contradiction_count > 0:
        avg_confidence *= 0.75

    # generate最终答案
    final_answer = synthesize_consulting_answer(
        problem, research_scan, contradiction_analysis,
        constraint_analysis, user_anchor, execution_check,
        fallacy_check
    )

    # 接入 consulting_validator 做完整验证
    validation_result = {}
    if consulting_validator:
        try:
            validation_result = consulting_validator.validate_full(
                problem=problem,
                research=research_scan,
                contradictions=contradiction_analysis.get('contradictions', []),
                constraints=constraint_analysis.get('constraints', {}),
                user_anchor=user_anchor,
                execution=execution_check,
                fallacies=fallacy_check.get('detections', [])
            )
        except Exception as e:
            validation_result = {"error": "操作失败"}

    suggestions = []
    if research_scan.get('gaps'):
        suggestions.append(f"调研缺口: 补充{', '.join(research_scan['gaps'][:3])}")
    if contradiction_analysis.get('contradictions'):
        suggestions.append("核心矛盾: 需要在方案中明确解决")
    if fallacy_check.get('critical'):
        suggestions.append(f"致命谬误: {'; '.join(fallacy_check['critical'][:2])}")
    if validation_result and not validation_result.get('error'):
        validation_issues = validation_result.get('issues', [])
        if validation_issues:
            suggestions.append(f"验证问题: {'; '.join(validation_issues[:3])}")
        validation_score = validation_result.get('score', 1.0)
        if validation_score < 0.5:
            avg_confidence *= 0.7

    return ReasoningResult(
        result_id=result_id,
        problem=problem,
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        success=True,
        reasoning_trace=reasoning_trace,
        final_answer=final_answer,
        confidence=avg_confidence,
        steps_count=len(reasoning_trace),
        suggestions=suggestions,
        metadata={
            "consulting_type": "growth_strategy",
            "research_completeness": research_scan.get('completeness', 0),
            "contradictions": contradiction_count,
            "fallacies": len(fallacy_check.get('detections', [])),
            "critical_issues": critical_count,
            "validation": validation_result
        }
    )

def consulting_reasoning_with_rules(
    problem: str,
    result_id: str,
    context: Dict,
    solution_type: str,
    solution_contradiction_rules: Dict,
    solution_constraint_dimensions: Dict,
    solution_user_anchor_dimensions: Dict,
    consulting_validator: Any = None,
    fallacy_detector: Any = None,
) -> ReasoningResult:
    """
    使用定制化规则执行咨询推理

    与通用 consulting_reasoning 共享框架,但使用特定解决方案的矛盾规则,
    约束维度和用户锚定维度.

    Args:
        solution_type: 解决方案类型
        solution_contradiction_rules: 从常量模块传入的矛盾规则字典
        solution_constraint_dimensions: 从常量模块传入的约束维度字典
        solution_user_anchor_dimensions: 从常量模块传入的用户锚定维度字典
        consulting_validator: 咨询验证器实例(可选)
        fallacy_detector: 谬误检测器实例(可选)
    """
    reasoning_trace = []

    # 步骤1: 五维调研扫描
    research_scan = consulting_research_scan(problem, context)
    node1 = ThoughtNode(
        id=f"{result_id}_research",
        content=f"五维调研扫描: {research_scan['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        confidence=0.80,
        completeness=research_scan.get('completeness', 0.5),
        validity=0.85,
        metadata={"dimensions_covered": research_scan.get('dimensions', []),
                  "gaps": research_scan.get('gaps', [])},
        status="completed"
    )
    reasoning_trace.append(node1)

    # 步骤2: 核心矛盾recognize(使用该解决方案的定制化规则)
    contradiction_analysis = detect_solution_contradictions(
        problem, context, solution_type, solution_contradiction_rules
    )
    node2 = ThoughtNode(
        id=f"{result_id}_contradiction",
        content=f"核心矛盾recognize: 发现 {len(contradiction_analysis.get('contradictions', []))} 个潜在矛盾",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node1.id,
        confidence=0.82,
        completeness=1.0,
        validity=0.85,
        metadata=contradiction_analysis,
        status="completed"
    )
    reasoning_trace.append(node2)

    # 步骤3: 约束反推目标(使用该解决方案的定制化约束维度)
    constraint_analysis = detect_solution_constraints(
        problem, context, solution_type, solution_constraint_dimensions
    )
    node3 = ThoughtNode(
        id=f"{result_id}_constraint",
        content=f"约束反推: {constraint_analysis['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node2.id,
        confidence=0.78,
        completeness=constraint_analysis.get('completeness', 0.7),
        validity=0.85,
        metadata=constraint_analysis,
        status="completed"
    )
    reasoning_trace.append(node3)

    # 步骤4: 用户需求锚定(使用该解决方案的定制化锚定维度)
    user_anchor = anchor_solution_users(
        problem, context, solution_type, solution_user_anchor_dimensions
    )
    node4 = ThoughtNode(
        id=f"{result_id}_user_anchor",
        content=f"用户锚定: {user_anchor['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node3.id,
        confidence=0.80,
        completeness=user_anchor.get('completeness', 0.7),
        validity=0.82,
        metadata=user_anchor,
        status="completed"
    )
    reasoning_trace.append(node4)

    # 步骤5: 执行层反推
    execution_check = consulting_bottom_up_check(problem, context)
    node5 = ThoughtNode(
        id=f"{result_id}_execution",
        content=f"执行反推: {execution_check['summary']}",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node4.id,
        confidence=0.78,
        completeness=execution_check.get('completeness', 0.6),
        validity=0.80,
        metadata=execution_check,
        status="completed"
    )
    reasoning_trace.append(node5)

    # 步骤6: 谬误自检
    fallacy_check = consulting_fallacy_check(problem, fallacy_detector=fallacy_detector)
    node6 = ThoughtNode(
        id=f"{result_id}_fallacy",
        content=f"谬误自检: 检测到 {len(fallacy_check.get('detections', []))} 个潜在谬误",
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        parent_id=node5.id,
        confidence=0.85,
        completeness=1.0,
        validity=0.90,
        metadata=fallacy_check,
        status="completed"
    )
    reasoning_trace.append(node6)

    # synthesize结果
    all_confidences = [n.confidence for n in reasoning_trace]
    avg_confidence = sum(all_confidences) / len(all_confidences)

    critical_count = len(fallacy_check.get('critical', []))
    contradiction_count = len(contradiction_analysis.get('contradictions', []))
    if critical_count > 0:
        avg_confidence *= 0.6
    elif contradiction_count > 0:
        avg_confidence *= 0.75

    # 接入 consulting_validator
    validation_result = {}
    if consulting_validator:
        try:
            validation_result = consulting_validator.validate_full(
                problem=problem,
                research=research_scan,
                contradictions=contradiction_analysis.get('contradictions', []),
                constraints=constraint_analysis.get('constraints', {}),
                user_anchor=user_anchor,
                execution=execution_check,
                fallacies=fallacy_check.get('detections', [])
            )
        except Exception as e:
            validation_result = {"error": "操作失败"}

    final_answer = synthesize_consulting_answer(
        problem, research_scan, contradiction_analysis,
        constraint_analysis, user_anchor, execution_check,
        fallacy_check
    )

    suggestions = []
    if research_scan.get('gaps'):
        suggestions.append(f"调研缺口: 补充{', '.join(research_scan['gaps'][:3])}")
    if contradiction_analysis.get('contradictions'):
        suggestions.append("核心矛盾: 需要在方案中明确解决")
    if fallacy_check.get('critical'):
        suggestions.append(f"致命谬误: {'; '.join(fallacy_check['critical'][:2])}")
    if validation_result and not validation_result.get('error'):
        validation_issues = validation_result.get('issues', [])
        if validation_issues:
            suggestions.append(f"验证问题: {'; '.join(validation_issues[:3])}")
        validation_score = validation_result.get('score', 1.0)
        if validation_score < 0.5:
            avg_confidence *= 0.7

    return ReasoningResult(
        result_id=result_id,
        problem=problem,
        reasoning_mode=ReasoningMode.CONSULTING_REASONING,
        success=True,
        reasoning_trace=reasoning_trace,
        final_answer=final_answer,
        confidence=avg_confidence,
        steps_count=len(reasoning_trace),
        suggestions=suggestions,
        metadata={
            "consulting_type": "solution_consulting",
            "solution_type": solution_type,
            "research_completeness": research_scan.get('completeness', 0),
            "contradictions": contradiction_count,
            "fallacies": len(fallacy_check.get('detections', [])),
            "critical_issues": critical_count,
            "validation": validation_result
        }
    )

# ---------------------------------------------------------------------------
# 咨询推理子函数
# ---------------------------------------------------------------------------

def consulting_research_scan(problem: str, context: Dict) -> Dict:
    """五维调研扫描"""
    dimensions = ['企业自身', '用户画像', '竞争格局', '市场环境', '风险全景']
    covered = []
    gaps = []

    dim_keywords = {
        '企业自身': ['营收', '利润', '产能', '团队', '渠道', '品牌'],
        '用户画像': ['用户', '客群', '消费者', '客户', '画像'],
        '竞争格局': ['竞品', '竞争', '对手', '对标', '市场份额'],
        '市场环境': ['市场', '行业', '规模', '增速', '趋势'],
        '风险全景': ['风险', '合规', '供应链', '政策'],
    }

    for dim, keywords in dim_keywords.items():
        if any(kw in problem for kw in keywords):
            covered.append(dim)
        else:
            gaps.append(dim)

    completeness = len(covered) / len(dimensions)

    return {
        'dimensions': covered,
        'gaps': gaps,
        'completeness': completeness,
        'summary': f"覆盖{len(covered)}/5维度" + (f",缺失: {', '.join(gaps)}" if gaps else ",覆盖完整")
    }

def consulting_contradiction_detection(problem: str, context: Dict) -> Dict:
    """核心矛盾检测"""
    contradictions = []

    # 矛盾规则对
    rules = [
        ((r'高端|奢侈品|稀缺|非遗|收藏', r'高端/稀缺心智'),
         (r'规模化|大众|代工|量产|平价', r'规模化/大众增长'),
         '品牌心智与增长来源矛盾'),
        ((r'线上|电商|直播', r'线上渠道'),
         (r'线下|门店|体验店', r'线下渠道'),
         '全渠道价格冲突风险'),
        ((r'聚焦|专注|深耕', r'聚焦strategy'),
         (r'扩展|多元|多线|品类扩展', r'多元化扩张'),
         '聚焦与多元化矛盾'),
    ]

    for (pattern_a, name_a), (pattern_b, name_b), desc in rules:
        match_a = bool(re.search(pattern_a, problem))
        match_b = bool(re.search(pattern_b, problem))
        if match_a and match_b:
            contradictions.append({
                'name': desc,
                'element_a': name_a,
                'element_b': name_b
            })

    return {
        'contradictions': contradictions,
        'summary': f"发现{len(contradictions)}个潜在矛盾" if contradictions else "未发现明显矛盾"
    }

def consulting_constraint_reverse(problem: str, context: Dict) -> Dict:
    """约束反推"""
    constraints = {
        '产能': '产能' in problem,
        '人才': any(kw in problem for kw in ['人才', '团队', '招聘']),
        '资金': any(kw in problem for kw in ['资金', '融资', '预算', '投入']),
        '市场': any(kw in problem for kw in ['市场天花板', '市场份额', 'TAM']),
    }

    has_reverse = any(kw in problem for kw in ['反推', '约束', '天花板', '合理', '边界'])
    covered = sum(constraints.values())

    return {
        'constraints': {k: v for k, v in constraints.items() if v},
        'has_reverse_engineering': has_reverse,
        'completeness': covered / len(constraints),
        'summary': f"{'有' if has_reverse else '缺'}约束反推分析,覆盖{covered}/4约束维度"
    }

def consulting_user_anchoring(problem: str, context: Dict) -> Dict:
    """用户需求锚定"""
    has_profile = any(kw in problem for kw in ['用户画像', '目标用户', '客群', '消费者'])
    has_decision = any(kw in problem for kw in ['decision', '购买动机', '为什么买', '需求'])
    has_differentiation = any(kw in problem for kw in ['差异化', '竞争优势', '为什么选择'])

    items = [('用户画像', has_profile), ('decision因素', has_decision), ('差异化', has_differentiation)]
    covered = sum(v for _, v in items)
    gaps = [name for name, has in items if not has]

    return {
        'completeness': covered / len(items),
        'gaps': gaps,
        'summary': f"用户锚定{'充分' if covered >= 2 else '不足'}" + (f",缺: {', '.join(gaps)}" if gaps else "")
    }

def consulting_bottom_up_check(problem: str, context: Dict) -> Dict:
    """执行层反推检查"""
    has_unit = any(kw in problem for kw in ['单店', '单客', 'ROI', '转化率', '坪效'])
    has_breakdown = any(kw in problem for kw in ['目标拆解', '营收构成', '渠道占比'])
    has_timeline = any(kw in problem for kw in ['时间表', '里程碑', '阶段', '节奏'])

    items = [('执行单元模型', has_unit), ('目标拆解', has_breakdown), ('时间线', has_timeline)]
    covered = sum(v for _, v in items)
    gaps = [name for name, has in items if not has]

    return {
        'completeness': covered / len(items),
        'gaps': gaps,
        'summary': f"执行细节{'充分' if covered >= 2 else '不足'}" + (f",缺: {', '.join(gaps)}" if gaps else "")
    }

def consulting_fallacy_check(problem: str, fallacy_detector: Any = None) -> Dict:
    """谬误自检(逻辑谬误 + 战略咨询谬误)"""
    detections = []
    critical = []

    if fallacy_detector:
        try:
            all_fallacies = fallacy_detector.detect_informal_fallacies(problem)
            for f in all_fallacies:
                detections.append({
                    'name': f.fallacy_name,
                    'category': f.category.value,
                    'severity': f.severity,
                    'confidence': f.confidence,
                    'suggestion': f.suggestion
                })
                if f.severity == 'critical':
                    critical.append(f.fallacy_name)
        except Exception as e:
            logger.debug(f"咨询推理初始化失败: {e}")

    return {
        'detections': detections,
        'critical': critical,
        'total': len(detections)
    }

def synthesize_consulting_answer(problem: str, research: Dict,
                                  contradiction: Dict, constraint: Dict,
                                  user: Dict, execution: Dict,
                                  fallacy: Dict) -> str:
    """synthesize咨询推理结果"""
    lines = ["基于咨询推理链的分析结果:\n"]

    # 调研评估
    lines.append(f"1. 调研覆盖: {research['summary']}")
    if research.get('gaps'):
        lines.append(f"   → 建议优先补充: {', '.join(research['gaps'][:3])}")

    # 矛盾评估
    lines.append(f"2. 核心矛盾: {contradiction['summary']}")
    for c in contradiction.get('contradictions', []):
        lines.append(f"   → {c['name']}: {c['element_a']} vs {c['element_b']}")

    # 约束评估
    lines.append(f"3. 约束反推: {constraint['summary']}")

    # 用户锚定
    lines.append(f"4. 用户锚定: {user['summary']}")

    # 执行评估
    lines.append(f"5. 执行反推: {execution['summary']}")

    # 谬误汇总
    lines.append(f"6. 谬误检测: {fallacy['total']}个潜在谬误")
    if fallacy.get('critical'):
        lines.append(f"   → 致命: {'; '.join(fallacy['critical'][:3])}")

    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# 解决方案定制化子函数
# ---------------------------------------------------------------------------

def detect_solution_contradictions(
    problem: str,
    context: Dict,
    solution_type: str,
    solution_contradiction_rules: Dict,
) -> Dict:
    """
    检测特定解决方案类型的定制化矛盾

    先用该解决方案的专属规则,再用通用规则兜底
    """
    contradictions = []

    # 1. 该解决方案的专属矛盾规则
    solution_rules = solution_contradiction_rules.get(solution_type, [])

    # 2. 通用矛盾规则
    general_rules = solution_contradiction_rules.get("_general", [])

    all_rules = solution_rules + general_rules

    for (pattern_a, name_a), (pattern_b, name_b), desc in all_rules:
        match_a = bool(re.search(pattern_a, problem))
        match_b = bool(re.search(pattern_b, problem))
        if match_a and match_b:
            contradictions.append({
                'name': desc,
                'element_a': name_a,
                'element_b': name_b,
                'rule_scope': 'solution_specific' if (pattern_a, name_a, desc) in
                    [(r[0], r[1], r[2]) for r in solution_rules] else 'general'
            })

    return {
        'contradictions': contradictions,
        'solution_type': solution_type,
        'rules_used': len(solution_rules),
        'general_rules_used': len(general_rules),
        'summary': f"发现{len(contradictions)}个矛盾({len(solution_rules)}条专属规则+{len(general_rules)}条通用规则)"
                   if contradictions else "未发现明显矛盾"
    }

def detect_solution_constraints(
    problem: str,
    context: Dict,
    solution_type: str,
    solution_constraint_dimensions: Dict,
) -> Dict:
    """
    检测特定解决方案类型的定制化约束维度
    """
    # get该解决方案的定制化约束维度
    constraint_config = solution_constraint_dimensions.get(solution_type, {})
    constraint_items = constraint_config.get('约束', {})

    detected_constraints = {}
    covered = 0

    if constraint_items:
        for dim_name, keywords in constraint_items.items():
            detected = any(kw in problem for kw in keywords)
            if detected:
                detected_constraints[dim_name] = True
                covered += 1
            else:
                detected_constraints[dim_name] = False
    else:
        # 无定制化约束,使用通用约束
        detected_constraints = {
            '产能': '产能' in problem,
            '人才': any(kw in problem for kw in ['人才', '团队', '招聘']),
            '资金': any(kw in problem for kw in ['资金', '融资', '预算', '投入']),
            '市场': any(kw in problem for kw in ['市场天花板', '市场份额', 'TAM']),
        }
        covered = sum(detected_constraints.values())

    total = len(detected_constraints) if detected_constraints else 1

    return {
        'constraints': {k: v for k, v in detected_constraints.items() if v},
        'all_constraints': detected_constraints,
        'has_reverse_engineering': any(kw in problem for kw in ['反推', '约束', '天花板', '合理', '边界']),
        'completeness': covered / total if total > 0 else 0,
        'is_custom': bool(constraint_config),
        'solution_type': solution_type,
        'summary': f"{'有' if any(detected_constraints.values()) else '缺'}约束分析,覆盖{covered}/{total}维度" +
                  (f"({solution_type}专属维度)" if constraint_config else "(通用维度)")
    }

def anchor_solution_users(
    problem: str,
    context: Dict,
    solution_type: str,
    solution_user_anchor_dimensions: Dict,
) -> Dict:
    """
    特定解决方案类型的用户需求锚定
    """
    # get该解决方案的定制化锚定维度
    anchor_items = solution_user_anchor_dimensions.get(solution_type, [])

    if not anchor_items:
        # 无定制化锚定,使用通用锚定
        return consulting_user_anchoring(problem, context)

    covered = []
    gaps = []

    for anchor_name, keywords in anchor_items:
        has = any(kw in problem for kw in keywords)
        if has:
            covered.append(anchor_name)
        else:
            gaps.append(anchor_name)

    return {
        'completeness': len(covered) / len(anchor_items),
        'gaps': gaps,
        'covered': covered,
        'is_custom': True,
        'solution_type': solution_type,
        'summary': f"用户锚定{'充分' if len(covered) >= 2 else '不足'}" +
                  (f",缺: {', '.join(gaps)}" if gaps else "") +
                  (f"({solution_type}专属维度)" if gaps else f"({solution_type}专属维度)")
    }
