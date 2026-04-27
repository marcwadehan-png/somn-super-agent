# -*- coding: utf-8 -*-
"""
智慧分发层 - dispatcher 子模块
目录整理 v1.0 (2026-04-05)
提供向后兼容的 re-export
"""

from __future__ import annotations
from typing import Any, Optional

import logging

logger = logging.getLogger(__name__)

__all__ = [
    "WisdomDispatcher",
    "WisdomSchool",
    "ProblemType",
    "SubSchool",
    "SUBSCHOOL_PARENT",
    "get_wisdom_dispatcher",
    "FusionDecision",
    "WisdomFusionCore",
    # V1.0 藏书阁V1.0
    "ImperialLibrary",
    "MemoryGrade",
    "MemorySource",
    "MemoryCategory",
    "CellRecord",
    "LibraryWing",
    "LibraryPermission",
    "get_imperial_library",
    # V1.0 藏书阁智能升级中枢
    "LibraryUpgradeCenter",
    "get_library_upgrade_center",
    "UpgradeType",
    "UpgradePriority",
    "UpgradeStatus",
    "UpgradeResult",
    "UpgradeContext",
    "UpgradePlan",
    "CodeChange",
    "UpgradeRecord",
    "SageUpgradeSuggestion",
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    # ── wisdom_dispatcher ─────────────────────────────────────────────────────────
    if name == 'WisdomDispatcher':
        try:
            from .wisdom_dispatcher import WisdomDispatcher
            return WisdomDispatcher
        except ImportError as e:
            logger.warning(f"wisdom_dispatcher 加载失败: {e}")
            return None
    if name == 'WisdomSchool':
        try:
            from .wisdom_dispatcher import WisdomSchool
            return WisdomSchool
        except ImportError:
            return None
    if name == 'ProblemType':
        try:
            from .wisdom_dispatcher import ProblemType
            return ProblemType
        except ImportError:
            return None
    if name == 'SubSchool':
        try:
            from .wisdom_dispatcher import SubSchool
            return SubSchool
        except ImportError:
            return None
    if name == 'SUBSCHOOL_PARENT':
        try:
            from .wisdom_dispatcher import SUBSCHOOL_PARENT
            return SUBSCHOOL_PARENT
        except ImportError:
            return None
    if name == 'get_wisdom_dispatcher':
        try:
            from .wisdom_dispatcher import get_wisdom_dispatcher
            return get_wisdom_dispatcher
        except ImportError:
            return None
    if name == 'FusionDecision':
        try:
            from .wisdom_dispatcher import FusionDecision
            return FusionDecision
        except ImportError:
            return None
    # ── wisdom_dispatch（藏书阁V1.0类型） ────────────────────────────────
    if name == 'ImperialLibrary':
        try:
            from .wisdom_dispatch import ImperialLibrary
            return ImperialLibrary
        except ImportError:
            return None
    if name == 'MemoryGrade':
        try:
            from .wisdom_dispatch import MemoryGrade
            return MemoryGrade
        except ImportError:
            return None
    if name == 'MemorySource':
        try:
            from .wisdom_dispatch import MemorySource
            return MemorySource
        except ImportError:
            return None
    if name == 'MemoryCategory':
        try:
            from .wisdom_dispatch import MemoryCategory
            return MemoryCategory
        except ImportError:
            return None
    if name == 'CellRecord':
        try:
            from .wisdom_dispatch import CellRecord
            return CellRecord
        except ImportError:
            return None
    if name == 'LibraryWing':
        try:
            from .wisdom_dispatch import LibraryWing
            return LibraryWing
        except ImportError:
            return None
    if name == 'LibraryPermission':
        try:
            from .wisdom_dispatch import LibraryPermission
            return LibraryPermission
        except ImportError:
            return None
    if name == 'get_imperial_library':
        try:
            from .wisdom_dispatch import get_imperial_library
            return get_imperial_library
        except ImportError:
            return None
    # ── V1.0 藏书阁智能升级中枢 ─────────────────────────────────────────
    if name == 'LibraryUpgradeCenter':
        try:
            from .wisdom_dispatch import LibraryUpgradeCenter
            return LibraryUpgradeCenter
        except ImportError:
            return None
    if name == 'get_library_upgrade_center':
        try:
            from .wisdom_dispatch import get_library_upgrade_center
            return get_library_upgrade_center
        except ImportError:
            return None
    if name == 'UpgradeType':
        try:
            from .wisdom_dispatch import UpgradeType
            return UpgradeType
        except ImportError:
            return None
    if name == 'UpgradePriority':
        try:
            from .wisdom_dispatch import UpgradePriority
            return UpgradePriority
        except ImportError:
            return None
    if name == 'UpgradeStatus':
        try:
            from .wisdom_dispatch import UpgradeStatus
            return UpgradeStatus
        except ImportError:
            return None
    if name == 'UpgradeResult':
        try:
            from .wisdom_dispatch import UpgradeResult
            return UpgradeResult
        except ImportError:
            return None
    if name == 'UpgradeContext':
        try:
            from .wisdom_dispatch import UpgradeContext
            return UpgradeContext
        except ImportError:
            return None
    if name == 'UpgradePlan':
        try:
            from .wisdom_dispatch import UpgradePlan
            return UpgradePlan
        except ImportError:
            return None
    if name == 'CodeChange':
        try:
            from .wisdom_dispatch import CodeChange
            return CodeChange
        except ImportError:
            return None
    if name == 'UpgradeRecord':
        try:
            from .wisdom_dispatch import UpgradeRecord
            return UpgradeRecord
        except ImportError:
            return None
    if name == 'SageUpgradeSuggestion':
        try:
            from .wisdom_dispatch import SageUpgradeSuggestion
            return SageUpgradeSuggestion
        except ImportError:
            return None
    # ── wisdom_fusion_core ───────────────────────────────────────────────────────
    if name == 'WisdomFusionCore':
        try:
            from .wisdom_fusion_core import WisdomFusionCore
            return WisdomFusionCore
        except ImportError as e:
            logger.warning(f"WisdomFusionCore 加载失败: {e}")
            return None
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
