# -*- coding: utf-8 -*-
"""
Tier3 调度器包

将原 _tier3_scheduler.py 拆分为模块化结构：
- _t3s_types.py: 类型定义
- _t3s_domain_matcher.py: 领域匹配
- _t3s_engine_selector.py: 引擎选择器
- _t3s_fusion.py: 融合逻辑
- _t3s_core.py: 核心调度器（兼容层）
"""

from ._t3s_types import (
    EngineTier,
    Tier3Query,
    TierSelection,
    EngineOutput,
    Tier3Result
)

from ._t3s_domain_matcher import DomainMatcher, DOMAIN_KEYWORD_TO_ENG

from ._t3s_engine_selector import EngineSelector

from ._t3s_fusion import (
    fuse_p1_outputs,
    build_feasibility_report,
    synthesize_perspectives,
    synthesize_final_strategy,
    extract_key_insights,
    calc_tier_balance,
    calc_coverage,
    calc_synergy
)

from ._t3s_core import Tier3NeuralScheduler

__all__ = [
    # 类型
    'EngineTier',
    'Tier3Query',
    'TierSelection',
    'EngineOutput',
    'Tier3Result',
    # 领域匹配
    'DomainMatcher',
    'DOMAIN_KEYWORD_TO_ENG',
    # 引擎选择
    'EngineSelector',
    # 融合函数
    'fuse_p1_outputs',
    'build_feasibility_report',
    'synthesize_perspectives',
    'synthesize_final_strategy',
    'extract_key_insights',
    'calc_tier_balance',
    'calc_coverage',
    'calc_synergy',
    # 核心调度器
    'Tier3NeuralScheduler',
]
