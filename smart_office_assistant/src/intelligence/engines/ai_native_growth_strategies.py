# -*- coding: utf-8 -*-
"""
AI原生增长策略 v2.0 - 兼容层

本文件已重构为兼容层，所有实现已迁移到 ai_native_growth/ 子包。
旧导入路径仍然完全兼容。

迁移指南:
  旧: from .ai_native_growth_strategies import AINativeGrowthEngine
  新: from .ai_native_growth import AINativeGrowthEngine

子包结构:
  ai_native_growth/
  ├── __init__.py              # Facade + 公开API
  ├── _aing_enums.py           # 枚举与数据类
  ├── _aing_data_flywheel.py   # 数据飞轮
  ├── _aing_network.py         # 智能体网络
  ├── _aing_compound.py        # 复合智能
  ├── _aing_experiment.py      # 实验框架
  ├── _aing_stats.py           # 统计引擎
  ├── _aing_attribution.py     # 归因分析
  └── _aing_engine.py           # 主引擎

版本: v2.0
日期: 2026-04-08
"""

# 本文件仅作为向后兼容的导入桥接层
# 所有实现已迁移到 ai_native_growth/ 子包

import warnings
import logging

logger = logging.getLogger(__name__)

# 向后兼容警告（首次导入时提示一次）
_warned = False

def _maybe_warn():
    global _warned
    if not _warned:
        warnings.warn(
            "ai_native_growth_strategies.py 已重构为兼容层。"
            "请更新导入语句: from .ai_native_growth import AINativeGrowthEngine",
            DeprecationWarning,
            stacklevel=2
        )
        _warned = True

# ============================================================
# 重新导出所有公共API（保持旧导入路径兼容）
# ============================================================

# 枚举与数据类
from .ai_native_growth import (
    GrowthPattern,
    GrowthMetric,
    GrowthStrategy,
    GrowthExperiment,
    AttributionResult,
    ExperimentVariant,
)

# 子系统
from .ai_native_growth import (
    AIDataFlywheel,
    AgentNetworkEffects,
    CompoundIntelligence,
    GrowthExperimentFramework,
    StatisticalEngine,
    AttributionAnalyzer,
)

# 主引擎
from .ai_native_growth import AINativeGrowthEngine

# 便捷函数
from .ai_native_growth import analyze_growth_opportunity

# 测试函数（保持旧路径兼容）
from .ai_native_growth import AINativeGrowthEngine as _Engine

def test_ai_native_growth():
    """测试AI原生增长strategy（兼容旧接口）"""
    _maybe_warn()
    
    logger.info("=" * 60)
    logger.info("AI原生增长strategy测试")
    logger.info("=" * 60)
    
    engine = AINativeGrowthEngine()
    
    # 测试数据飞轮
    logger.info("数据飞轮模拟:")
    engine.data_flywheel.users = 1000
    projections = engine.data_flywheel.project_growth(days=30)
    logger.info(f"  初始: {projections[0]['users']} 用户")
    logger.info(f"  30天后: {projections[-1]['users']} 用户")
    logger.info(f"  增长率: {(projections[-1]['users'] / projections[0]['users'] - 1) * 100:.1f}%")
    
    # 测试智能体网络
    logger.info("智能体网络效应:")
    for i in range(5):
        engine.agent_network.add_agent(f"type_{i}", ["capability"])
    stats = engine.agent_network.get_network_stats()
    logger.info(f"  智能体数: {stats['total_agents']}")
    logger.info(f"  网络价值: {stats['network_value']}")
    logger.info(f"  协作效率: {stats['collaboration_efficiency']}")
    
    # 测试复合智能
    logger.info("复合智能增长:")
    for i in range(5):
        engine.compound_intelligence.learn(f"domain_{i}", {"knowledge": f"data_{i}"})
    report = engine.compound_intelligence.get_intelligence_report()
    logger.info(f"  智能分数: {report['intelligence_score']}")
    logger.info(f"  知识领域: {report['knowledge_domains']}")
    
    # 推荐strategy
    logger.info("strategy推荐 (早期阶段, 预算10万):")
    recommendations = engine.recommend_strategy(
        current_stage="early",
        resources={"budget": 100000},
        priorities=["用户增长"]
    )
    for i, strategy in enumerate(recommendations, 1):
        logger.info(f"  {i}. {strategy.name} ({strategy.pattern.value})")
        logger.info(f"     预期: {strategy.expected_outcomes}")
    
    # 增长路线图
    logger.info("增长路线图:")
    roadmap = engine.generate_growth_roadmap(quarters=4)
    for q in roadmap["quarters"]:
        logger.info(f"  Q{q['quarter']}: {q['focus']}")
        logger.info(f"    strategy: {', '.join(q['strategies'])}")
        logger.info(f"    目标: {q['targets']}")
    
    logger.info("AI原生增长strategy测试完成")
    return engine

# 公开API列表
__all__ = [
    # 枚举与数据类
    "GrowthPattern",
    "GrowthMetric",
    "GrowthStrategy",
    "GrowthExperiment",
    "AttributionResult",
    "ExperimentVariant",
    # 子系统
    "AIDataFlywheel",
    "AgentNetworkEffects",
    "CompoundIntelligence",
    "GrowthExperimentFramework",
    "StatisticalEngine",
    "AttributionAnalyzer",
    # 主引擎
    "AINativeGrowthEngine",
    # 便捷函数
    "analyze_growth_opportunity",
    # 测试
    "test_ai_native_growth",
]
