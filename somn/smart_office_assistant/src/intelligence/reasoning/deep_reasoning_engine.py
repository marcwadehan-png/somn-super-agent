# -*- coding: utf-8 -*-
"""
deep_reasoning_engine.py - 向后兼容层

真实实现已拆分到 deep_reasoning_engine/ 包中:
- deep_reasoning_engine/_dre_base.py    : DeepReasoningEngine 核心类
- deep_reasoning_engine/_dre_neuro.py   : 神经动力学推理
- deep_reasoning_engine/_dre_xinmind.py : 王阳明心学推理
- deep_reasoning_engine/_dre_dewey.py   : 杜威反省思维推理
- deep_reasoning_engine/_dre_top.py     : 顶级思维法推理
- 以及 _deep_reasoning_types/constants/memory/subsystems/narrative/yinyang/consulting 子模块

本文件通过从包重导出，保持所有旧导入路径不变。
任何 `from .deep_reasoning_engine import X` 或
`from intelligence.reasoning.deep_reasoning_engine import X` 均无需修改。
"""

from .deep_reasoning_engine import (
    DeepReasoningEngine,
    ReasoningMode,
    ThoughtNode,
    ReasoningResult,
    SOLUTION_CONTRADICTION_RULES,
    SOLUTION_CONSTRAINT_DIMENSIONS,
    SOLUTION_USER_ANCHOR_DIMENSIONS,
)

__all__ = [
    "DeepReasoningEngine",
    "ReasoningMode",
    "ThoughtNode",
    "ReasoningResult",
    "SOLUTION_CONTRADICTION_RULES",
    "SOLUTION_CONSTRAINT_DIMENSIONS",
    "SOLUTION_USER_ANCHOR_DIMENSIONS",
]
