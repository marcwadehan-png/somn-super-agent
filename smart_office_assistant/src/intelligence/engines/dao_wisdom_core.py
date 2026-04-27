"""
道家哲学核心模块 v2.0 - 向后兼容入口
已迁移到 dao_wisdom/ 包
此文件保留以兼容旧的导入路径
"""

# 重新导出所有内容(从新包)
from .dao_wisdom import (
    DaoWisdomCore,
    DaoWisdom,
    DaoDecision,
    TaoistPersona,
    DaoDeJingCore,
    BaGua,
    BaGuaRelation,
    ZhuangziCore,
    DeJingHierarchy,
    DaoThreeRealms,
    WuXing,
    WuXingCycle,
    SiXiang,
    DaoManagement,
    DaoHealth,
    YinYang,
    YinYangPrinciple,
    LuoShu,
    DaoPrinciple,
)

# 向后兼容别名(原文件中定义的)
YinYangBalance = YinYangPrinciple  # 兼容 wisdom_fusion_core.py 导入

__all__ = [
    'DaoWisdomCore',
    'DaoWisdom',
    'DaoDecision',
    'TaoistPersona',
    'DaoDeJingCore',
    'BaGua',
    'BaGuaRelation',
    'YinYang',
    'YinYangPrinciple',
    'LuoShu',
    'ZhuangziCore',
    'DeJingHierarchy',
    'DaoThreeRealms',
    'WuXing',
    'WuXingCycle',
    'SiXiang',
    'DaoManagement',
    'DaoHealth',
    'DaoPrinciple',
]
