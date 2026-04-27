# -*- coding: utf-8 -*-
"""
跨尺度思维引擎 - 兼容层

⚠️  警告：此文件已拆分为包结构
原文件内容已迁移至 cross_scale_thinking_engine/ 目录下：

包结构：
- cross_scale_thinking_engine/
  ├── __init__.py          # 包导出
  ├── _cst_types.py        # 类型定义
  ├── _cst_constants.py    # 常量配置
  ├── _cst_analyzer.py     # 分析器（微观/宏观/跨尺度）
  ├── _cst_synthesizer.py  # 综合器
  ├── _cst_strategy.py     # 策略引擎
  └── _cst_core.py         # 核心引擎实现

此文件仅保留向后兼容的导入，所有实现已委托给子模块。
新代码应直接从包导入：
    from src.intelligence.engines.cross_scale_thinking_engine import CrossScaleThinkingEngine
"""

# 从包中重新导出所有公共API
from .cross_scale_thinking_engine import (
    # 类型
    ScaleLevel,
    MicroElement,
    MacroPattern,
    CrossScaleBridge,
    CrossScaleInsight,
    ThinkingMode,
    StrategyType,
    CrossScaleStrategy,
    # 分析器
    MicroAnalyzer,
    MacroAnalyzer,
    CrossScaleAnalyzer,
    # 综合器和策略
    CrossScaleSynthesizer,
    CrossScaleStrategyEngine,
    # 核心引擎
    CrossScaleThinkingEngine,
)

# 保持向后兼容的导出
__all__ = [
    'ScaleLevel',
    'MicroElement',
    'MacroPattern',
    'CrossScaleBridge',
    'CrossScaleInsight',
    'ThinkingMode',
    'StrategyType',
    'CrossScaleStrategy',
    'MicroAnalyzer',
    'MacroAnalyzer',
    'CrossScaleAnalyzer',
    'CrossScaleSynthesizer',
    'CrossScaleStrategyEngine',
    'CrossScaleThinkingEngine',
]
