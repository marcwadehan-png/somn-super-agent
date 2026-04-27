# -*- coding: utf-8 -*-
"""跨尺度思维引擎 - 枚举定义

包含:
- ScaleLevel: 尺度层级枚举
- EmergenceType: 涌现类型枚举
"""

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

class EmergenceType(Enum):
    """涌现类型"""
    WEAK_EMERGENCE = "weak"      # 弱涌现:可原则上还原(如水的湿性)
    STRONG_EMERGENCE = "strong"  # 强涌现:不可还原(如意识?)

# 类型别名
__all__ = ['ScaleLevel', 'EmergenceType']
