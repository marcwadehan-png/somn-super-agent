"""
智慧引擎unified调度器 - 向后兼容导出层
============================================

本文件已重构为包 `wisdom_dispatch/`：
- _dispatch_enums.py          : 枚举与数据结构
- _dispatch_mapping.py         : 初始化+引擎注册+映射矩阵
- _dispatch_recommend.py       : 问题识别+学派推荐
- _dispatch_fusion.py          : 融合决策+评分+单例
- _library_upgrade_center.py   : 藏书阁智能升级中枢（V1.0）

所有旧导入路径保持完全兼容。
"""

# 延迟导入，避免循环依赖问题
def __getattr__(name):
    if name == 'WisdomSchool':
        from .wisdom_dispatch import WisdomSchool
        return WisdomSchool
    elif name == 'ProblemType':
        from .wisdom_dispatch import ProblemType
        return ProblemType
    elif name == 'SubSchool':
        from .wisdom_dispatch import SubSchool
        return SubSchool
    elif name == 'SUBSCHOOL_PARENT':
        from .wisdom_dispatch import SUBSCHOOL_PARENT
        return SUBSCHOOL_PARENT
    elif name == 'WisdomRecommendation':
        from .wisdom_dispatch import WisdomRecommendation
        return WisdomRecommendation
    elif name == 'FusionDecision':
        from .wisdom_dispatch import FusionDecision
        return FusionDecision
    elif name == 'WisdomDispatcher':
        from .wisdom_dispatch import WisdomDispatcher
        return WisdomDispatcher
    elif name == 'get_wisdom_dispatcher':
        from .wisdom_dispatch import get_wisdom_dispatcher
        return get_wisdom_dispatcher
    # V1.0 藏书阁V1.0 类型
    elif name == 'ImperialLibrary':
        from .wisdom_dispatch import ImperialLibrary
        return ImperialLibrary
    elif name == 'MemoryGrade':
        from .wisdom_dispatch import MemoryGrade
        return MemoryGrade
    elif name == 'MemorySource':
        from .wisdom_dispatch import MemorySource
        return MemorySource
    elif name == 'MemoryCategory':
        from .wisdom_dispatch import MemoryCategory
        return MemoryCategory
    elif name == 'CellRecord':
        from .wisdom_dispatch import CellRecord
        return CellRecord
    elif name == 'LibraryWing':
        from .wisdom_dispatch import LibraryWing
        return LibraryWing
    elif name == 'LibraryPermission':
        from .wisdom_dispatch import LibraryPermission
        return LibraryPermission
    elif name == 'get_imperial_library':
        from .wisdom_dispatch import get_imperial_library
        return get_imperial_library
    # V1.0 藏书阁智能升级中枢
    elif name == 'LibraryUpgradeCenter':
        from .wisdom_dispatch import LibraryUpgradeCenter
        return LibraryUpgradeCenter
    elif name == 'get_library_upgrade_center':
        from .wisdom_dispatch import get_library_upgrade_center
        return get_library_upgrade_center
    elif name == 'UpgradeType':
        from .wisdom_dispatch import UpgradeType
        return UpgradeType
    elif name == 'UpgradePriority':
        from .wisdom_dispatch import UpgradePriority
        return UpgradePriority
    elif name == 'UpgradeRecord':
        from .wisdom_dispatch import UpgradeRecord
        return UpgradeRecord
    elif name == 'SageUpgradeSuggestion':
        from .wisdom_dispatch import SageUpgradeSuggestion
        return SageUpgradeSuggestion
    raise AttributeError(f"module has no attribute '{name}'")

__all__ = [
    'WisdomSchool',
    'ProblemType',
    'SubSchool',
    'SUBSCHOOL_PARENT',
    'WisdomRecommendation',
    'FusionDecision',
    'WisdomDispatcher',
    'get_wisdom_dispatcher',
    # V1.0 藏书阁V1.0
    'ImperialLibrary',
    'MemoryGrade',
    'MemorySource',
    'MemoryCategory',
    'CellRecord',
    'LibraryWing',
    'LibraryPermission',
    'get_imperial_library',
    # V1.0 藏书阁智能升级中枢
    'LibraryUpgradeCenter',
    'get_library_upgrade_center',
    'UpgradeType',
    'UpgradePriority',
    'UpgradeRecord',
    'SageUpgradeSuggestion',
]
