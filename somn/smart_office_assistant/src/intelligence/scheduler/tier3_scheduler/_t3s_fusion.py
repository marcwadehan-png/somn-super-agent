# -*- coding: utf-8 -*-
"""
Tier3 调度器 - 融合模块
处理三层输出融合和结果生成
"""

__all__ = [
    'build_feasibility_report',
    'calc_coverage',
    'calc_synergy',
    'calc_tier_balance',
    'extract_key_insights',
    'fuse_p1_outputs',
    'synthesize_final_strategy',
    'synthesize_perspectives',
]

from typing import Dict, List, Any, Tuple

from ._t3s_types import EngineOutput

def fuse_p1_outputs(outputs: List[EngineOutput]) -> Dict[str, Any]:
    """融合P1核心策略输出"""
    strategies = [o.strategy_content for o in outputs if o.strategy_content]
    all_warnings = []
    for o in outputs:
        all_warnings.extend(o.warnings)

    return {
        "engines_used": [o.engine_id for o in outputs],
        "strategy_count": len(strategies),
        "strategies": strategies,
        "total_weight": sum(o.match_score for o in outputs),
        "avg_execution_time": sum(o.execution_time for o in outputs) / max(1, len(outputs)),
        "warnings": list(set(all_warnings))
    }

def build_feasibility_report(p3_outputs: List[EngineOutput],
                              p1_outputs: List[EngineOutput]) -> Dict[str, Any]:
    """构建P3可行性报告"""
    arguments = [o.论证_content for o in p3_outputs if o.论证_content]
    all_warnings = [w for o in p3_outputs for w in o.warnings]

    # 提取可行性判断
    feasibility_judgments = []
    for o in p3_outputs:
        raw = o.raw_output
        if isinstance(raw, dict):
            judgment = raw.get("feasibility", raw.get("可行性", ""))
            if judgment:
                feasibility_judgments.append(judgment)

    # 综合可行性评分
    feasible_keywords = ["可行", "支撑", "合理", "有效", "positive", "feasible"]
    infeasible_keywords = ["不可行", "风险", "问题", "缺陷", "negative", "infeasible"]

    feasible_count = sum(
        1 for j in feasibility_judgments
        if any(kw in str(j).lower() for kw in feasible_keywords)
    )
    infeasible_count = sum(
        1 for j in feasibility_judgments
        if any(kw in str(j).lower() for kw in infeasible_keywords)
    )

    total = feasible_count + infeasible_count
    if total > 0:
        feasibility_score = feasible_count / total
    else:
        feasibility_score = 0.5

    return {
        "engines_used": [o.engine_id for o in p3_outputs],
        "arguments": arguments,
        "feasibility_judgments": feasibility_judgments,
        "feasibility_score": feasibility_score,
        "total_weight": sum(o.match_score for o in p3_outputs),
        "warnings": list(set(all_warnings)),
        "risk_level": "high" if feasibility_score < 0.4 else "medium" if feasibility_score < 0.7 else "low"
    }

def synthesize_perspectives(p2_outputs: List[EngineOutput]) -> Dict[str, Any]:
    """综合P2多元视角"""
    perspectives = []
    challenging_args = []
    supporting_args = []

    for o in p2_outputs:
        if o.perspective_content:
            perspectives.append({
                "engine": o.engine_id,
                "perspective": o.perspective_content,
                "weight": o.match_score
            })

        raw = o.raw_output
        if isinstance(raw, dict):
            challenges = raw.get("challenging_arguments", raw.get("质疑", []))
            if challenges:
                challenging_args.extend(challenges[:2])

            supports = raw.get("supporting_arguments", raw.get("支持", []))
            if supports:
                supporting_args.extend(supports[:2])

    # 生成综合视角
    synthesis_points = []
    if challenging_args:
        synthesis_points.append(f"需关注: {'; '.join(challenging_args[:3])}")
    if supporting_args:
        synthesis_points.append(f"有支撑: {'; '.join(supporting_args[:3])}")

    return {
        "engines_used": [o.engine_id for o in p2_outputs],
        "perspectives": perspectives,
        "challenging_args": challenging_args,
        "supporting_args": supporting_args,
        "synthesis": "\n".join(synthesis_points),
        "total_weight": sum(o.match_score for o in p2_outputs)
    }

def synthesize_final_strategy(
    fused_strategy: Dict[str, Any],
    feasibility_report: Dict[str, Any],
    perspective_synthesis: Dict[str, Any]
) -> Tuple[str, float, List[str]]:
    """综合生成最终策略"""
    warnings = []
    warnings.extend(fused_strategy.get("warnings", []))
    warnings.extend(feasibility_report.get("warnings", []))

    # 判断策略可行性
    judgments = feasibility_report.get("feasibility_judgments", [])
    feasible_count = sum(1 for j in judgments if "可行" in str(j) or "支撑" in str(j) or "合理" in str(j))
    feasibility_ratio = feasible_count / max(1, len(judgments))

    # 计算综合置信度
    p1_weight = fused_strategy.get("total_weight", 0)
    p3_weight = feasibility_report.get("total_weight", 0)
    p2_weight = perspective_synthesis.get("total_weight", 0)

    total_weight = p1_weight + p3_weight * 0.8 + p2_weight * 0.6
    confidence = min(1.0, total_weight / max(1, p1_weight + p3_weight + p2_weight) * feasibility_ratio)

    # 生成最终策略文本
    strategies = fused_strategy.get("strategies", [])
    if strategies:
        top_strategy = strategies[0]
    else:
        top_strategy = "需要进一步分析"

    challenges = perspective_synthesis.get("challenging_args", [])
    if challenges:
        final_strategy = f"{top_strategy}\n\n⚠️ 需注意: {';'.join(challenges[:2])}"
    else:
        final_strategy = top_strategy

    return final_strategy, confidence, warnings

def extract_key_insights(p1: List[EngineOutput],
                         p3: List[EngineOutput],
                         p2: List[EngineOutput]) -> List[str]:
    """提取关键洞察"""
    insights = []

    # P1核心洞察
    for o in p1[:2]:
        if o.strategy_content:
            insights.append(f"[{o.engine_id}] {o.strategy_content[:100]}")

    # P3论证洞察
    for o in p3[:1]:
        if o.论证_content:
            insights.append(f"[{o.engine_id}论证] {o.论证_content[:100]}")

    # P2视角洞察
    challenges = []
    for o in p2:
        raw = o.raw_output
        if isinstance(raw, dict):
            for c in raw.get("challenging_arguments", [])[:2]:
                challenges.append(c)
    if challenges:
        insights.append(f"[多元质疑] {';'.join(challenges[:2])}")

    return insights[:6]

def calc_tier_balance(p1: List[EngineOutput], p3: List[EngineOutput],
                      p2: List[EngineOutput]) -> float:
    """计算层级平衡度"""
    counts = [len(p1), len(p3), len(p2)]
    if not counts or max(counts) == 0:
        return 0.0
    expected = sum(counts) / len(counts)
    if expected == 0:
        return 0.0
    balance = 1 - (max(counts) - min(counts)) / (2 * expected)
    return max(0.0, balance)

def calc_coverage(domains: Dict, p1: List[EngineOutput],
                  p3: List[EngineOutput], p2: List[EngineOutput],
                  domain_matcher, engine_pool: Dict) -> float:
    """计算域覆盖度"""
    all_outputs = p1 + p3 + p2
    if not domains or not all_outputs:
        return 0.0

    covered = set()
    for domain in domains:
        for o in all_outputs:
            score, matched = domain_matcher.match_engine(
                o.engine_id, {domain: domains[domain]}, engine_pool
            )
            if matched:
                covered.add(domain)
                break

        # 兜底：中文关键词直接匹配
        if domain not in covered:
            for o in all_outputs:
                ed_domains = domain_matcher._get_engine_domains(
                    o.engine_id, engine_pool.get(o.engine_id, {})
                )
                if domain.lower() in ed_domains or domain in ed_domains:
                    covered.add(domain)
                    break

    return len(covered) / len(domains)

def calc_synergy(p1: List[EngineOutput], p3: List[EngineOutput],
                 p2: List[EngineOutput]) -> float:
    """计算三层协同度"""
    all_outputs = p1 + p3 + p2
    if len(all_outputs) < 2:
        return 0.5

    total_score = sum(o.match_score for o in all_outputs)
    avg_score = total_score / len(all_outputs)

    # 三层都有效 = 高协同
    active_tiers = sum([
        any(o.success for o in p1),
        any(o.success for o in p3),
        any(o.success for o in p2)
    ])

    synergy = (avg_score * 0.4 + active_tiers / 3 * 0.6)
    return min(1.0, synergy)
