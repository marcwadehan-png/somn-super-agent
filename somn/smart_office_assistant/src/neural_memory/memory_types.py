"""
__all__ = [
    'MemoryTier',
    'MemoryType', 
    'MemoryStatus',
    'UnifiedMemoryTier',
]

统一记忆类型系统 V1.0
=====================

解决多版本 MemoryTier 冲突:
- V1 (memory_engine.py): EPISODIC, SEMANTIC, PROCEDURAL, WORKING
- V5 (_super_neural_memory.py): ETERNAL, LONG_TERM, WORKING, EPISODIC
- memory_manager: HOT, WARM, COLD

本模块提供统一枚举，并保留各版本的兼容别名。

版本: v1.0.0
创建: 2026-04-23
"""

from enum import Enum
from typing import Dict, Any


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


__version__ = "1.0.0"
