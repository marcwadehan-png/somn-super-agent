"""
__all__ = [
    'MemoryTier',
    'MemoryType', 
    'MemoryStatus',
    'UnifiedMemoryTier',
    'TIER_TO_GRADE_NAME',
    'GRADE_TO_TIER_NAMES',
    'UNIFIED_TIER_TO_GRADE',
    'tier_to_grade',
    'grade_to_tiers',
    'auto_assign_tier',
    'tier_to_unified',
    'get_tier_priority',
]

统一记忆类型系统 V2.0
=====================

[NeuralMemory 架构定位]
本模块定义 NeuralMemory（三层神经记忆架构）的核心类型系统：
  - MemoryTier: 三层记忆架构的书架分层（ETERNAL → EPISODIC，共7层）
  - MemoryGrade: 藏书阁的甲乙丙丁分级（通过 tier_to_grade 映射）

解决多版本 MemoryTier 冲突:
- V1 (memory_engine.py): EPISODIC, SEMANTIC, PROCEDURAL, WORKING
- V5 (_super_neural_memory.py): ETERNAL, LONG_TERM, WORKING, EPISODIC
- memory_manager: HOT, WARM, COLD

[v2.0 新增]
- MemoryTier ↔ MemoryGrade 双向映射（NeuralMemory 三层书架 ↔ 藏书阁分级统一）
- CellRecord.tier 自动推导
- 三层记忆架构(COLD/WARM/HOT)与甲乙丙丁分级深度绑定

版本: v2.0.0
更新: 2026-04-29
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Set


# ═══════════════════════════════════════════════════════════════
#  前向引用：MemoryGrade 定义在 _imperial_library.py 中
#  本模块提供映射常量，运行时解析引用
# ═══════════════════════════════════════════════════════════════


class MemoryTier(Enum):
    """
    统一记忆层级
    
    七层架构:
    - ETERNAL: 永恒级 - 核心智慧，不会遗忘
    - ARCHIVED: 归档级 - 长期存储，低频访问
    - LONG_TERM: 长期级 - 蒸馏知识，稳定保留
    - WARM: 温级 - 偶尔访问，保持激活
    - HOT: 热级 - 高频访问，内存缓存
    - WORKING: 工作级 - 当前任务相关
    - EPISODIC: 情景级 - 临时交互，短期保留
    """
    ETERNAL = "eternal"        # 永恒级 - 核心智慧
    ARCHIVED = "archived"      # 归档级 - 长期存储
    LONG_TERM = "long_term"    # 长期级 - 蒸馏知识
    WARM = "warm"             # 温级 - 偶尔访问
    HOT = "hot"               # 热级 - 高频访问
    WORKING = "working"       # 工作级 - 当前任务
    EPISODIC = "episodic"     # 情景级 - 临时交互


class UnifiedMemoryTier(Enum):
    """
    简化记忆层级（兼容旧系统）
    
    映射关系:
    - ETERNAL/ARCHIVED/LONG_TERM -> COLD (冷存储)
    - WARM -> WARM (温存储)
    - HOT -> HOT (热存储)
    - WORKING/EPISODIC -> EPISODIC (情景/工作)
    """
    COLD = "cold"             # 冷存储
    WARM = "warm"            # 温存储
    HOT = "hot"              # 热存储
    EPISODIC = "episodic"    # 情景/工作记忆


class MemoryType(Enum):
    """
    记忆内容类型
    """
    EPISODIC = "episodic"       # 情景记忆 - 具体事件和经历
    SEMANTIC = "semantic"       # 语义记忆 - 知识和概念
    PROCEDURAL = "procedural"   # 程序记忆 - 技能和操作
    WORKING = "working"        # 工作记忆 - 当前任务相关
    METACOGNITIVE = "metacognitive"  # 元认知 - 学习如何学习


class MemoryStatus(Enum):
    """记忆状态"""
    ACTIVE = "active"         # 活跃
    INACTIVE = "inactive"    # 不活跃
    ARCHIVED = "archived"    # 已归档
    DELETED = "deleted"     # 已删除
    CONSOLIDATING = "consolidating"  # 巩固中


# ─────────────────────────────────────────────────────────────────────────────
# 兼容层别名
# ─────────────────────────────────────────────────────────────────────────────

# V1/V3 兼容
V1_MemoryType = MemoryType
V1_MemoryStatus = MemoryStatus

# V5 兼容
V5_MemoryTier = MemoryTier

# memory_manager 兼容
MM_MemoryTier = UnifiedMemoryTier


# ─────────────────────────────────────────────────────────────────────────────
# 层级转换函数
# ─────────────────────────────────────────────────────────────────────────────

def tier_to_unified(tier: MemoryTier) -> UnifiedMemoryTier:
    """将统一层级转换为简化层级"""
    mapping = {
        MemoryTier.ETERNAL: UnifiedMemoryTier.COLD,
        MemoryTier.ARCHIVED: UnifiedMemoryTier.COLD,
        MemoryTier.LONG_TERM: UnifiedMemoryTier.COLD,
        MemoryTier.WARM: UnifiedMemoryTier.WARM,
        MemoryTier.HOT: UnifiedMemoryTier.HOT,
        MemoryTier.WORKING: UnifiedMemoryTier.EPISODIC,
        MemoryTier.EPISODIC: UnifiedMemoryTier.EPISODIC,
    }
    return mapping.get(tier, UnifiedMemoryTier.COLD)


def get_tier_priority(tier: MemoryTier) -> int:
    """获取层级优先级（数字越大越重要）"""
    priority = {
        MemoryTier.ETERNAL: 100,
        MemoryTier.ARCHIVED: 70,
        MemoryTier.LONG_TERM: 60,
        MemoryTier.WARM: 40,
        MemoryTier.HOT: 80,
        MemoryTier.WORKING: 50,
        MemoryTier.EPISODIC: 20,
    }
    return priority.get(tier, 0)


# ═══════════════════════════════════════════════════════════════
#  v2.0: MemoryTier ↔ MemoryGrade 统一映射
#  （神经记忆三层架构的书架 ↔ 藏书阁的甲乙丙丁分级）
# ═══════════════════════════════════════════════════════════════

# 字符串常量映射（避免循环导入，使用字符串枚举值）
TIER_TO_GRADE_NAME: Dict[str, str] = {
    "eternal": "甲级",       # 永恒级 → 甲级（永不遗忘）
    "hot": "甲级",            # 热级 → 甲级（高频高价值）
    "archived": "乙级",       # 归档级 → 乙级（长期存储）
    "long_term": "乙级",      # 长期级 → 乙级（稳定保留）
    "working": "丙级",        # 工作级 → 丙级（当前任务）
    "warm": "丙级",           # 温级 → 丙级（偶尔访问）
    "episodic": "丁级",       # 情景级 → 丁级（短期临时）
}

GRADE_TO_TIER_NAMES: Dict[str, List[str]] = {
    "甲级": ["eternal", "hot"],
    "乙级": ["archived", "long_term"],
    "丙级": ["working", "warm"],
    "丁级": ["episodic"],
}

# 三层简化映射 (UnifiedMemoryTier ↔ MemoryGrade)
UNIFIED_TIER_TO_GRADE: Dict[str, str] = {
    "cold": "甲级",     # COLD包含 eternal/archived/long_term → 对应甲级为主
    "warm": "丙级",     # WARM包含 warm → 对应丙级
    "hot": "甲级",      # HOT包含 hot/working/episodic → 对应甲级为主(含高频)
    "episodic": "丁级", # EPISODIC → 丁级
}


def tier_to_grade(tier: MemoryTier) -> str:
    """
    将 MemoryTier 映射为 MemoryGrade 的值名称。

    这是神经记忆系统"书架"到藏书阁"仓库"的核心桥梁：
    - 三层记忆架构的7层Tier → 藏书阁4级Grade

    >>> from .memory_types import MemoryTier
    >>> tier_to_grade(MemoryTier.ETERNAL)
    '甲级'
    >>> tier_to_grade(MemoryTier.EPISODIC)
    '丁级'
    """
    return TIER_TO_GRADE_NAME.get(tier.value, "丁级")


def grade_to_tiers(grade_name: str) -> List[MemoryTier]:
    """
    将 MemoryGrade 反向映射为 MemoryTier 列表。

    >>> grade_to_tiers("甲级")
    [MemoryTier.ETERNAL, MemoryTier.HOT]
    """
    tier_names = GRADE_TO_TIER_NAMES.get(grade_name, ["episodic"])
    result = []
    for name in tier_names:
        try:
            result.append(MemoryTier(name))
        except ValueError:
            continue
    return result


def auto_assign_tier(
    access_count: int = 0,
    age_days: float = 0.0,
    importance: float = 0.5,
    is_frequent: bool = False,
) -> MemoryTier:
    """
    基于使用模式自动分配 MemoryTier。

    用于神经记忆系统入库时自动确定书架位置：

    Args:
        access_count: 累计访问次数
        age_days: 创建天数
        importance: 重要性评分 0-1
        is_frequent: 是否高频访问

    Returns:
        推荐的 MemoryTier

    规则:
        - importance >= 0.8 或 access_count > 50 → ETERNAL/HOT
        - age_days > 180 且 access_count < 5 → ARCHIVED
        - age_days > 30 且 access_count < 3 → WARM
        - is_frequent → HOT
        - 默认 → WORKING / EPISODIC
    """
    if importance >= 0.8 or access_count > 50:
        return MemoryTier.ETERNAL if importance >= 0.9 else MemoryTier.HOT

    if is_frequent:
        return MemoryTier.HOT

    if age_days > 180 and access_count < 5:
        return MemoryTier.ARCHIVED

    if age_days > 30 and access_count < 3:
        return MemoryTier.WARM

    if importance >= 0.6 or access_count > 10:
        return MemoryTier.LONG_TERM

    if access_count > 3:
        return MemoryTier.WORKING

    return MemoryTier.EPISODIC


__version__ = "6.2.0"
