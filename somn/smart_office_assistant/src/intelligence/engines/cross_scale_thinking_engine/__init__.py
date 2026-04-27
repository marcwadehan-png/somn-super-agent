# -*- coding: utf-8 -*-
"""
跨尺度思维引擎包

将原 cross_scale_thinking_engine.py 拆分为模块化结构：
- _cst_types.py: 类型定义
- _cst_constants.py: 常量配置
- _cst_analyzer.py: 分析器（微观/宏观/跨尺度）
- _cst_synthesizer.py: 综合器
- _cst_strategy.py: 策略引擎
- _cst_core.py: 核心引擎（兼容层）
"""

from ._cst_types import (
    ScaleLevel,
    MicroElement,
    MacroPattern,
    CrossScaleBridge,
    CrossScaleInsight,
    ThinkingMode
)

from ._cst_analyzer import (
    MicroAnalyzer,
    MacroAnalyzer,
    CrossScaleAnalyzer
)

from ._cst_synthesizer import CrossScaleSynthesizer

from ._cst_strategy import (
    StrategyType,
    CrossScaleStrategy,
    CrossScaleStrategyEngine
)

from ._cst_core import CrossScaleThinkingEngine

__all__ = [
    # 类型
    'ScaleLevel',
    'MicroElement',
    'MacroPattern',
    'CrossScaleBridge',
    'CrossScaleInsight',
    'ThinkingMode',
    'StrategyType',
    'CrossScaleStrategy',
    # 分析器
    'MicroAnalyzer',
    'MacroAnalyzer',
    'CrossScaleAnalyzer',
    # 综合器和策略
    'CrossScaleSynthesizer',
    'CrossScaleStrategyEngine',
    # 核心引擎
    'CrossScaleThinkingEngine',
]
