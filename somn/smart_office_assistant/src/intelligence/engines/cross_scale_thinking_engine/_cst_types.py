"""
跨尺度思维引擎 - 类型定义模块
Cross-Scale Thinking Engine - Types Module
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class ScaleLevel(Enum):
    """尺度层级枚举--从量子到宇宙"""
    QUANTUM_FOAM = "quantum_foam"       # 10^-35 m 普朗克尺度
    SUBATOMIC = "subatomic"             # 10^-18 m 原子核
    ATOMIC = "atomic"                   # 10^-10 m 原子
    MOLECULAR = "molecular"             # 10^-9 m 分子
    CELLULAR = "cellular"               # 10^-6 m 细胞
    ORGANISM = "organism"               # 10^0 m 生物体
    PLANETARY = "planetary"             # 10^7 m 行星
    STELLAR = "stellar"                 # 10^11 m 恒星系统
    GALACTIC = "galactic"               # 10^21 m 星系
    COSMOLOGICAL = "cosmological"       # 10^27 m 可观测宇宙

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

class EmergenceType(Enum):
    """涌现类型"""
    WEAK_EMERGENCE = "weak"      # 弱涌现:可原则上还原(如水的湿性)
    STRONG_EMERGENCE = "strong"  # 强涌现:不可还原(如意识?)

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

class ThinkingMode(Enum):
    """思维模式枚举"""
    REDUCTIONIST = "reductionist"         # 还原论：从宏观到微观分解
    EMERGENTIST = "emergentist"           # 涌现论：从微观到宏观整合
    CROSS_SCALE = "cross_scale"           # 跨尺度：多尺度关联分析
    SYSTEMIC = "systemic"                 # 系统论：整体性思维
    ANALOGICAL = "analogical"             # 类比论：跨尺度类比推理

@dataclass
class MicroElement:
    """微观元素 - 最小分析单元"""
    name: str                              # 元素名称
    scale_level: ScaleLevel               # 所属尺度层级
    properties: Dict[str, Any] = field(default_factory=dict)  # 元素属性
    interactions: List[str] = field(default_factory=list)     # 相互作用类型
    energy_state: Optional[float] = None   # 能量状态(eV)
    description: str = ""                   # 描述

@dataclass
class MacroPattern:
    """宏观模式 - 微观元素涌现出的宏观结构"""
    name: str                              # 模式名称
    scale_level: ScaleLevel               # 所属尺度层级
    emergent_from: List[ScaleLevel] = field(default_factory=list)  # 涌现来源层级
    properties: Dict[str, Any] = field(default_factory=dict)       # 模式属性
    stability: float = 0.5                 # 稳定性(0-1)
    predictability: float = 0.5            # 可预测性(0-1)
    description: str = ""                   # 描述

@dataclass
class CrossScaleBridge:
    """跨尺度桥接 - 连接不同尺度的关联"""
    source_level: ScaleLevel               # 源尺度
    target_level: ScaleLevel               # 目标尺度
    source_elements: List[MicroElement] = field(default_factory=list)   # 源微观元素
    target_patterns: List[MacroPattern] = field(default_factory=list)   # 目标宏观模式
    mechanism: str = ""                     # 桥接机制
    strength: float = 0.5                  # 关联强度(0-1)

@dataclass
class CrossScaleInsight:
    """跨尺度洞察 - 跨尺度分析产生的洞察"""
    title: str                             # 洞察标题
    source_scales: List[ScaleLevel] = field(default_factory=list)  # 涉及尺度
    insight_type: str = "cross_scale"      # 洞察类型
    content: str = ""                       # 洞察内容
    confidence: float = 0.5                # 置信度(0-1)
    bridging_mechanisms: List[str] = field(default_factory=list)  # 桥接机制
    implications: List[str] = field(default_factory=list)         # 推论

__all__ = [
    'ScaleLevel',
    'ScaleInfo',
    'EmergenceType',
    'EmergenceExample',
    'PhysicalConstant',
    'ThinkingMode',
    'MicroElement',
    'MacroPattern',
    'CrossScaleBridge',
    'CrossScaleInsight',
]
