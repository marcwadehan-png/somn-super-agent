# -*- coding: utf-8 -*-
"""跨尺度思维引擎 - 数据类定义

包含:
- ScaleInfo: 尺度信息数据类
- EmergenceExample: 涌现现象案例
- PhysicalConstant: 物理常数
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from ._cste_enums import ScaleLevel, EmergenceType

@dataclass
class ScaleInfo:
    """尺度信息"""
    level: ScaleLevel
    name_zh: str
    size_range: Tuple[float, float]  # (min, max) meters
    key_theories: List[str]
    key_entities: List[str]
    energy_scale: Optional[float] = None  # eV
    governing_laws: List[str] = field(default_factory=list)

@dataclass
class EmergenceExample:
    """涌现现象案例"""
    name: str
    from_level: ScaleLevel
    to_level: ScaleLevel
    type: EmergenceType
    description: str
    key_mechanism: str

@dataclass
class PhysicalConstant:
    """物理常数"""
    name: str
    symbol: str
    value: float
    unit: str
    fine_tuning_sensitivity: Optional[str] = None  # 精调敏感度描述
    anthropic_relevance: Optional[str] = None     # 人择相关性

__all__ = ['ScaleInfo', 'EmergenceExample', 'PhysicalConstant']
