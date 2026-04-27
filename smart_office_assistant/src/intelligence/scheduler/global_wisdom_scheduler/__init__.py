"""global_wisdom_scheduler package v1.0"""

__all__ = [
    'get_scheduler',
    'get_statistics',
    'problem_solve',
    'schedule',
    'think_analysis',
    'tier3_full_report',
    'tier3_quick',
    'tier3_wisdom_analyze',
    'wisdom_analyze',
    'wisdom_fusion',
]

from ._gws_base import (
    SchedulerMode, WisdomOutputFormat, SchedulerConfig,
    WisdomQuery, SchoolOutput, ScheduledResult, WisdomEngineRegistry
)
from . import _gws_core as _core_mod
from . import _gws_execute as _exec_mod
from . import _gws_api as _api_mod

GlobalWisdomScheduler = None

class GlobalWisdomScheduler:
    def __init__(self, config=None):
        _core_mod.scheduler_init(self, config)
        # [v22.5 调度优化] 神经网络激活结果缓存
        self._activation_cache = {}  # 键: (query_text, context_hash), 值: activations
        self._activation_cache_hits = 0
        self._activation_cache_misses = 0
        self._max_activation_cache_size = 1000  # 最大缓存条目数

    def _initialize_engines(self):
        _core_mod._initialize_engines(self)

    def schedule(self, query):
        return _exec_mod.schedule(self, query)

    def _apply_rules(self, activated, query):
        return _exec_mod._apply_rules(self, activated, query)

    def _call_schools(self, activated, query):
        return _exec_mod._call_schools(self, activated, query)

    def _call_engine(self, engine, school_id, query):
        return _exec_mod._call_engine(self, engine, school_id, query)

    def _normalize_engine_output(self, output, school_id):
        return _exec_mod._normalize_engine_output(self, output, school_id)

    def _default_school_output(self, school_id, query):
        return _exec_mod._default_school_output(self, school_id, query)

    def _extract_insights(self, output):
        return _exec_mod._extract_insights(self, output)

    def _extract_warnings(self, output):
        return _exec_mod._extract_warnings(self, output)

    def _fuse_wisdom(self, outputs, query):
        return _exec_mod._fuse_wisdom(self, outputs, query)

    def _generate_insight(self, outputs, fused):
        return _exec_mod._generate_insight(self, outputs, fused)

    def _calculate_synergy(self, outputs):
        return _exec_mod._calculate_synergy(self, outputs)

    def _record_query(self, query, result):
        _exec_mod._record_query(self, query, result)

    def get_statistics(self):
        return _exec_mod.get_statistics(self)

def get_scheduler():
    return _api_mod.get_scheduler()

def wisdom_analyze(query_text, context=None, threshold=0.25, max_schools=5):
    return _api_mod.wisdom_analyze(query_text, context, threshold, max_schools)

def wisdom_fusion(school_ids, query_text, context=None):
    return _api_mod.wisdom_fusion(school_ids, query_text, context)

def think_analysis(query_text, method="auto", context=None):
    return _api_mod.think_analysis(query_text, method, context)

def problem_solve(problem):
    return _api_mod.problem_solve(problem)

def tier3_wisdom_analyze(query_text, context=None, p1_count=6, p3_count=4, p2_count=4, random_seed=None):
    return _api_mod.tier3_wisdom_analyze(query_text, context, p1_count, p3_count, p2_count, random_seed)

def tier3_quick(query_text, p1_count=6, p3_count=4, p2_count=4, random_seed=None):
    return _api_mod.tier3_quick(query_text, p1_count, p3_count, p2_count, random_seed)

def tier3_full_report(query_text, context=None, random_seed=None):
    return _api_mod.tier3_full_report(query_text, context, random_seed)
