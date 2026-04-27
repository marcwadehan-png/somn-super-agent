"""global_wisdom_scheduler backward compat layer v1.0"""
from src.intelligence.scheduler.global_wisdom_scheduler import (
    GlobalWisdomScheduler,
    SchedulerMode, WisdomOutputFormat, SchedulerConfig,
    WisdomQuery, SchoolOutput, ScheduledResult, WisdomEngineRegistry,
    get_scheduler, wisdom_analyze, wisdom_fusion,
    think_analysis, problem_solve,
    tier3_wisdom_analyze, tier3_quick, tier3_full_report,
)
