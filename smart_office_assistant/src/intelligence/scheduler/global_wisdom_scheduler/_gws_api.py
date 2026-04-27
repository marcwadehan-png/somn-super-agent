"""global_wisdom_scheduler top-level API v1.0"""
import logging
import uuid
from typing import Dict, List, Optional

__all__ = [
    'get_scheduler',
    'problem_solve',
    'think_analysis',
    'tier3_full_report',
    'tier3_quick',
    'tier3_wisdom_analyze',
    'wisdom_analyze',
    'wisdom_fusion',
]

logger = logging.getLogger(__name__)

_sched_instance: Optional = None

def get_scheduler():
    from . import GlobalWisdomScheduler
    global _sched_instance
    if _sched_instance is None:
        _sched_instance = GlobalWisdomScheduler()
    return _sched_instance

def wisdom_analyze(query_text: str, context: Optional[Dict] = None,
                   threshold: float = 0.25, max_schools: int = 5):
    from ._gws_base import SchedulerConfig, SchedulerMode, WisdomQuery
    scheduler = get_scheduler()
    config = SchedulerConfig(activation_threshold=threshold, max_activated_schools=max_schools, mode=SchedulerMode.AUTO)
    query = WisdomQuery(query_id=str(uuid.uuid4())[:8], query_text=query_text, context=context or {}, config=config)
    return scheduler.schedule(query)

def wisdom_fusion(school_ids: List[str], query_text: str, context: Optional[Dict] = None):
    from ._gws_base import SchedulerConfig, SchedulerMode, WisdomQuery
    scheduler = get_scheduler()
    config = SchedulerConfig(mode=SchedulerMode.FUSION, activation_threshold=0.0, max_activated_schools=len(school_ids))
    query = WisdomQuery(query_id=str(uuid.uuid4())[:8], query_text=query_text, context=context or {}, required_schools=school_ids, config=config)
    return scheduler.schedule(query)

def think_analysis(query_text: str, method: str = "auto", context: Optional[Dict] = None) -> Dict:
    try:
        from .thinking_method_engine import think_comprehensively, solve_problem, apply_reflective_method, select_optimal_thinking
        if method == "reflective":
            return apply_reflective_method(query_text)
        elif method in ("logic", "top7"):
            return select_optimal_thinking(query_text)
        else:
            method_choice = select_optimal_thinking(query_text)
            analysis = think_comprehensively(query_text)
            return {"query": query_text, "recommended_methods": method_choice.get("推荐方法", []), "comprehensive_analysis": analysis, "quick_tips": f"建议: {method_choice.get('推荐方法', [{}])[0].get('方法', '反省思维五步法') if method_choice.get('推荐方法') else '反省思维五步法'}"}
    except ImportError:
        return {"error": "思维方法引擎未安装", "suggestion": "请先安装 thinking_method_engine"}

def problem_solve(problem: str) -> Dict:
    try:
        from .thinking_method_engine import solve_problem
        return solve_problem(problem)
    except ImportError:
        return {"error": "思维方法引擎未安装", "suggestion": "请先安装 thinking_method_engine"}

def tier3_wisdom_analyze(query_text: str, context: Optional[Dict] = None,
                          p1_count: int = 6, p3_count: int = 4, p2_count: int = 4,
                          random_seed: Optional[int] = None):
    from .tier3_neural_scheduler import tier3_analyze
    return tier3_analyze(query_text=query_text, context=context, p1_count=p1_count, p3_count=p3_count, p2_count=p2_count, random_seed=random_seed)

def tier3_quick(query_text: str, p1_count: int = 6, p3_count: int = 4, p2_count: int = 4, random_seed: Optional[int] = None) -> str:
    result = tier3_wisdom_analyze(query_text, p1_count=p1_count, p3_count=p3_count, p2_count=p2_count, random_seed=random_seed)
    return result.final_strategy

def tier3_full_report(query_text: str, context: Optional[Dict] = None, random_seed: Optional[int] = None) -> Dict:
    result = tier3_wisdom_analyze(query_text, context=context, random_seed=random_seed)
    return {
        "query_id": result.query_id, "query_text": result.query_text, "success": result.success,
        "p1_engines": [o.engine_id for o in result.p1_outputs],
        "p3_engines": [o.engine_id for o in result.p3_outputs],
        "p2_engines": [o.engine_id for o in result.p2_outputs],
        "p1_strategies": [o.strategy_content for o in result.p1_outputs if o.strategy_content],
        "p3_arguments": [getattr(o, '论证_content', '') for o in result.p3_outputs if getattr(o, '论证_content', '')],
        "p2_perspectives": [o.perspective_content for o in result.p2_outputs if o.perspective_content],
        "fused_strategy": result.fused_strategy, "feasibility_report": result.feasibility_report,
        "perspective_synthesis": result.perspective_synthesis, "final_strategy": result.final_strategy,
        "decision_confidence": result.decision_confidence, "risk_warnings": result.risk_warnings,
        "key_insights": result.key_insights, "tier_balance": result.tier_balance,
        "coverage": result.coverage, "synergy_score": result.synergy_score,
        "processing_time": result.processing_time, "timestamp": result.timestamp.isoformat()
    }
