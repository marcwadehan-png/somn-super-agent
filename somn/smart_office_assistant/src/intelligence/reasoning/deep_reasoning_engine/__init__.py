"""
deep_reasoning_engine 包 - 深度推理引擎模块化拆分
Deep Reasoning Engine - Modular Split

架构：
- _dre_base.py    : 核心类 DeepReasoningEngine（含小方法 + 四大推理委托）
- _dre_neuro.py   : 神经动力学推理 standalone 函数
- _dre_xinmind.py : 王阳明心学推理 standalone 函数
- _dre_dewey.py   : 杜威反省思维推理 standalone 函数
- _dre_top.py     : 顶级思维法推理 standalone 函数
- _dre_types.py   : 类型定义
- _dre_constants.py: 常量定义
- _dre_memory.py  : 记忆管理
- _dre_subsystems.py: 子系统初始化
- _dre_narrative.py : 叙事推理（已存在）
- _dre_yinyang.py  : 阴阳辩证推理（已存在）
- _dre_consulting.py: 咨询推理（已存在）

主文件 deep_reasoning_engine.py 为向后兼容层，重新导出本包内容。
"""

from ._dre_base import DeepReasoningEngine

# 向后兼容别名：允许 from deep_reasoning_engine import ReasoningMode
from ._dre_types import ReasoningMode, ThoughtNode, ReasoningResult
from ._dre_constants import (
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
