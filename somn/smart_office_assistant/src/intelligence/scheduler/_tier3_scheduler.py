# -*- coding: utf-8 -*-
"""
Tier3 神经网络调度器 - 兼容层

⚠️  警告：此文件已拆分为包结构
原文件内容已迁移至 tier3_scheduler/ 目录下：

包结构：
- tier3_scheduler/
  ├── __init__.py              # 包导出
  ├── _t3s_types.py            # 类型定义
  ├── _t3s_domain_matcher.py   # 领域匹配
  ├── _t3s_engine_selector.py  # 引擎选择器
  ├── _t3s_fusion.py           # 融合逻辑
  └── _t3s_core.py             # 核心调度器实现

此文件仅保留向后兼容的导入，所有实现已委托给子模块。
新代码应直接从包导入：
    from src.intelligence.scheduler.tier3_scheduler import Tier3NeuralScheduler
"""

# 从包中重新导出所有公共API
from .tier3_scheduler import (
    # 类型
    EngineTier,
    Tier3Query,
    TierSelection,
    EngineOutput,
    Tier3Result,
    # 领域匹配
    DomainMatcher,
    DOMAIN_KEYWORD_TO_ENG,
    # 引擎选择
    EngineSelector,
    # 融合函数
    fuse_p1_outputs,
    build_feasibility_report,
    synthesize_perspectives,
    synthesize_final_strategy,
    extract_key_insights,
    calc_tier_balance,
    calc_coverage,
    calc_synergy,
    # 核心调度器
    Tier3NeuralScheduler,
)

# 保持向后兼容的导出
__all__ = [
    'EngineTier',
    'Tier3Query',
    'TierSelection',
    'EngineOutput',
    'Tier3Result',
    'DomainMatcher',
    'DOMAIN_KEYWORD_TO_ENG',
    'EngineSelector',
    'fuse_p1_outputs',
    'build_feasibility_report',
    'synthesize_perspectives',
    'synthesize_final_strategy',
    'extract_key_insights',
    'calc_tier_balance',
    'calc_coverage',
    'calc_synergy',
    'Tier3NeuralScheduler',
]
