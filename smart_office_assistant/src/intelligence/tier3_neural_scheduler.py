# -*- coding: utf-8 -*-
"""
intelligence/ 目录 - tier3_neural_scheduler 兼容转发
=================================================

为保持向后兼容,从新位置重新导出所有接口.

新位置: src.intelligence.scheduler.tier3_neural_scheduler
原始导入: src.intelligence.tier3_neural_scheduler

版本: v1.1
日期: 2026-04-06
"""

# 转发到新位置
from src.intelligence.scheduler.tier3_neural_scheduler import (
    # 常量
    TIER_CLASSIFICATION,
    P1_CANDIDATES,
    P3_CANDIDATES,
    P2_CANDIDATES,
    DOMAIN_ENGINE_KEYWORDS,
    DOMAIN_KEYWORD_TO_ENG,
    SEMANTIC_TO_ENG_DOMAINS,
    # 类型
    EngineTier,
    TierSelection,
    Tier3Query,
    EngineOutput,
    Tier3Result,
    # 组件
    DomainMatcher,
    Tier3NeuralScheduler,
    ROIMixin,
    # 函数
    get_tier3_scheduler,
    tier3_analyze,
    # 知识库
    ENGINE_KNOWLEDGE,
    default_p1_output,
    default_p3_output,
    default_p2_output,
    extract_strategy_content,
    extract_argument_content,
    extract_perspective_content,
)

__all__ = [
    "TIER_CLASSIFICATION",
    "P1_CANDIDATES",
    "P3_CANDIDATES",
    "P2_CANDIDATES",
    "DOMAIN_ENGINE_KEYWORDS",
    "DOMAIN_KEYWORD_TO_ENG",
    "SEMANTIC_TO_ENG_DOMAINS",
    "EngineTier",
    "TierSelection",
    "Tier3Query",
    "EngineOutput",
    "Tier3Result",
    "DomainMatcher",
    "Tier3NeuralScheduler",
    "ROIMixin",
    "get_tier3_scheduler",
    "tier3_analyze",
    "ENGINE_KNOWLEDGE",
    "default_p1_output",
    "default_p3_output",
    "default_p2_output",
    "extract_strategy_content",
    "extract_argument_content",
    "extract_perspective_content",
]
