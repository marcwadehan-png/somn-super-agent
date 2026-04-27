# -*- coding: utf-8 -*-
"""
三级神经网络调度器 v1.1 - 向后兼容入口
Tier-3 Neural Scheduler (Backward-Compatible Entry)
================================================

本文件为向后兼容入口，实际功能已拆分到以下模块:
- _tier3_constants.py: 常量定义 (TIER_CLASSIFICATION, P1/P3/P2_CANDIDATES, DOMAIN_*_KEYWORDS)
- _tier3_types.py: 类型定义 (EngineTier, TierSelection, Tier3Query, EngineOutput, Tier3Result)
- _tier3_domain_matcher.py: 领域匹配器 (DomainMatcher)
- _tier3_knowledge.py: 引擎知识库与默认输出 (_ENGINE_KNOWLEDGE, default_p1/p2/p3_output)
- _tier3_roi.py: ROI追踪混入类 (ROIMixin)
- _tier3_scheduler.py: 核心调度器 (Tier3NeuralScheduler)
- _tier3_unified.py: 统一入口 (get_tier3_scheduler, tier3_analyze)

版本: v1.1
日期: 2026-04-06
拆分完成
"""

# ==================== 导出所有公共接口 ====================
# 确保与原文件完全兼容,调用方无感知

# 从常量模块导出
from ._tier3_constants import (
    TIER_CLASSIFICATION,
    P1_CANDIDATES,
    P3_CANDIDATES,
    P2_CANDIDATES,
    DOMAIN_ENGINE_KEYWORDS,
    DOMAIN_KEYWORD_TO_ENG,
    SEMANTIC_TO_ENG_DOMAINS,
)

# 从类型模块导出
from ._tier3_types import (
    EngineTier,
    TierSelection,
    Tier3Query,
    EngineOutput,
    Tier3Result,
)

# 从领域匹配器模块导出
from ._tier3_domain_matcher import DomainMatcher

# 从知识库模块导出
from ._tier3_knowledge import (
    ENGINE_KNOWLEDGE,
    default_p1_output,
    default_p3_output,
    default_p2_output,
    extract_strategy_content,
    extract_argument_content,
    extract_perspective_content,
)

# 从ROI模块导出
from ._tier3_roi import ROIMixin

# 从调度器模块导出
from ._tier3_scheduler import Tier3NeuralScheduler

# 从统一入口模块导出
from ._tier3_unified import (
    get_tier3_scheduler,
    tier3_analyze,
)

# ==================== 向后兼容的别名 ====================
# 确保原有导入路径继续工作

# 导出单例获取函数(与原文件名中的导入兼容)
def _get_tier3_scheduler():
    """获取调度器单例 - 向后兼容别名"""
    return get_tier3_scheduler()

# ==================== __all__ 导出列表 ====================
__all__ = [
    # 常量
    "TIER_CLASSIFICATION",
    "P1_CANDIDATES",
    "P3_CANDIDATES",
    "P2_CANDIDATES",
    "DOMAIN_ENGINE_KEYWORDS",
    "DOMAIN_KEYWORD_TO_ENG",
    "SEMANTIC_TO_ENG_DOMAINS",
    # 类型
    "EngineTier",
    "TierSelection",
    "Tier3Query",
    "EngineOutput",
    "Tier3Result",
    # 组件
    "DomainMatcher",
    "Tier3NeuralScheduler",
    "ROIMixin",
    # 函数
    "get_tier3_scheduler",
    "tier3_analyze",
    # 知识库
    "ENGINE_KNOWLEDGE",
    "default_p1_output",
    "default_p3_output",
    "default_p2_output",
    "extract_strategy_content",
    "extract_argument_content",
    "extract_perspective_content",
]

# ==================== 主程序入口(已禁用 - 请使用 tests/ 目录) ====================
# if __name__ == "__main__":
#     test_queries = [
#         "公司面临生死危机,如何绝地反击?",
#         "如何在竞争中保持战略优势,同时维护团队和谐?",
#         "个人成长和自我提升的方法是什么?",
#         "企业面临市场竞争加剧,需要制定长期增长战略",
#     ]
#
#     for q in test_queries:
#         result = tier3_analyze(q, random_seed=42)
#         print(f"查询: {q}")
#         print(f"成功: {result.success}")
#         print(f"置信度: {result.decision_confidence:.2f}")
