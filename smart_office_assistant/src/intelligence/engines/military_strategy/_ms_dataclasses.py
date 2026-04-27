"""
三十六计数据类定义
"""



__all__ = [
    'StrategyInfo',
    'StrategyApplication',
]
from dataclasses import dataclass
from typing import List

from ._ms_enums import StrategyCategory, StrategyType

@dataclass
class StrategyInfo:
    """计谋信息"""
    name: str
    category: StrategyCategory
    original_text: str
    explanation: str
    principles: List[str]
    applications: List[str]
    historical_cases: List[str]

@dataclass
class StrategyApplication:
    """策略应用"""
    strategy: StrategyType
    confidence: float  # 置信度 0-1
    reasoning: str     # 推理过程
    steps: List[str]   # 执行步骤
    risks: List[str]   # 风险提示
    benefits: List[str]  # 收益预期
