# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 统一聚合模块 V1.0
==================================
将 court_enums / court_models / court_helpers 及 11 个 positions_*.py 
聚合为 CourtPositionRegistry，供全局导入。

使用方式:
    from intelligence.engines.cloning._court_positions import (
        CourtPositionRegistry, get_court_registry,
        PinRank, NobilityRank, PositionType, SageType,
        _NOBILITY_NAMES, _PIN_NAMES, _SAGE_TYPE_NAMES, _SAGE_TYPE_SYMBOLS,
        _PRACTITIONER_QUOTA,
    )
"""

import logging
import threading
from typing import Dict, List, Optional, Tuple, Any

# ═══════════════════════════════════════════════════════════════════════════════
# 一、枚举 & 模型 — 直接从子模块重导出
# ═══════════════════════════════════════════════════════════════════════════════

from .court_enums import (
    NobilityRank, PinRank, PositionType, SystemType, SageType,
    _NOBILITY_NAMES, _NOBILITY_AUTHORITY,
    _PIN_NAMES, _SAGE_TYPE_NAMES, _SAGE_TYPE_SYMBOLS,
    _PRACTITIONER_QUOTA,
)
from .court_models import Position, DepartmentPositionTree
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch

logger = logging.getLogger("CourtPositions")


# ═══════════════════════════════════════════════════════════════════════════════
# 二、岗位注册表 — 核心类
# ═══════════════════════════════════════════════════════════════════════════════

class CourtPositionRegistry:
    """
    朝廷岗位注册表 — 管理全部岗位的增删改查与贤者分配。

    方法:
        get_positions_by_department(dept_name) -> List[Position]
        get_sage_position(sage_name) -> Optional[Tuple[str, Position]]
        auto_assign_all_sages() -> int
        get_stats() -> Dict[str, Any]
    """

    def __init__(self):
        self._departments: Dict[str, DepartmentPositionTree] = {}
        self._all_positions: Dict[str, Position] = {}
        self._position_sage_map: Dict[str, List[str]] = {}
        self._sage_position_map: Dict[str, str] = {}
        self._build_all_positions()

    # ─── 构建 ──────────────────────────────────────────────────────────────

    def _build_all_positions(self):
        """从 11 个 positions_*.py 构建完整岗位体系"""
        from . import (
            positions_royal, positions_military, positions_wenzhi,
            positions_economy, positions_congress, positions_library,
            positions_review, positions_specialist, positions_standard,
            positions_supplement, positions_chuangxin,
        )

        builder_map = {
            "皇家": positions_royal.build_royal_positions,
            "军事": positions_military.build_military_positions,
            "文治": positions_wenzhi.build_wenzhi_positions,
            "经济": positions_economy.build_economy_positions,
            "议事": positions_congress.build_congress_positions,
            "藏书阁": positions_library.build_library_positions,
            "审核": positions_review.build_review_positions,
            "专家": positions_specialist.build_specialist_leaders,
            "标准": positions_standard.build_standard_positions,
            "补充": positions_supplement.build_supplement_positions,
            "创新": positions_chuangxin.build_chuangxin_positions,
        }

        total = 0
        for dept_name, builder in builder_map.items():
            try:
                positions = builder()
                tree = self._departments.get(dept_name)
                if tree is None:
                    tree = DepartmentPositionTree(department=dept_name)
                    self._departments[dept_name] = tree
                for pos in positions:
                    if not isinstance(pos, Position):
                        continue
                    tree.add_position(pos)
                    self._all_positions[pos.id] = pos
                    if pos.id not in self._position_sage_map:
                        self._position_sage_map[pos.id] = []
                    total += 1
            except Exception as e:
                logger.warning(f"构建 {dept_name} 岗位失败: {e}")

        logger.info(f"朝廷岗位体系构建完成: {total} 个岗位, {len(self._departments)} 个部门")

    # ─── 查询 ──────────────────────────────────────────────────────────────

    def get_positions_by_department(self, dept_name: str) -> List[Position]:
        """按部门名查询岗位列表（模糊匹配）"""
        results = []
        for key, tree in self._departments.items():
            if dept_name in key or key in dept_name:
                results.extend(tree.positions.values())
        return results

    def get_sage_position(self, sage_name: str) -> Optional[Tuple[str, Position]]:
        """查询贤者所在岗位"""
        # 先从映射表查
        pos_id = self._sage_position_map.get(sage_name)
        if pos_id and pos_id in self._all_positions:
            return (pos_id, self._all_positions[pos_id])
        # 遍历查
        for pid, pos in self._all_positions.items():
            if sage_name in pos.assigned_sages or sage_name == pos.si_name:
                self._sage_position_map[sage_name] = pid
                return (pid, pos)
        return None

    def get_all_positions(self) -> Dict[str, Position]:
        """返回全部岗位字典"""
        return dict(self._all_positions)

    def get_departments(self) -> Dict[str, DepartmentPositionTree]:
        """返回全部部门树"""
        return dict(self._departments)

    # ─── 贤者分配 ──────────────────────────────────────────────────────────

    def auto_assign_all_sages(self) -> int:
        """自动将贤者分配到对应岗位（基于 si_name 匹配）"""
        assigned = 0
        for pid, pos in self._all_positions.items():
            if pos.si_name:
                if pos.si_name not in self._position_sage_map[pid]:
                    self._position_sage_map[pid].append(pos.si_name)
                    self._sage_position_map[pos.si_name] = pid
                    assigned += 1
        return assigned

    # ─── 统计 ──────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """返回岗位统计信息"""
        total_positions = len(self._all_positions)
        total_assigned = sum(
            len(sages) for sages in self._position_sage_map.values()
        )
        return {
            "total_positions": total_positions,
            "total_departments": len(self._departments),
            "total_assigned_sages": total_assigned,
            "departments": {
                name: tree.get_regular_capacity()
                for name, tree in self._departments.items()
            },
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 三、工具函数
# ═══════════════════════════════════════════════════════════════════════════════

def get_sage_court_position(sage_name: str) -> Optional[Dict[str, Any]]:
    """
    获取贤者的岗位信息（便捷函数）。

    Returns:
        岗位信息字典，包含 position_id, name, department, pin 等；
        未找到则返回 None。
    """
    registry = get_court_registry()
    result = registry.get_sage_position(sage_name)
    if result is None:
        return None
    pos_id, pos = result
    return {
        "position_id": pos_id,
        "name": pos.name,
        "department": pos.department,
        "pin": pos.pin.value if pos.pin is not None else None,
        "nobility": pos.nobility.value if pos.nobility is not None else None,
        "domain": pos.domain,
        "suitable_schools": pos.suitable_schools,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 四、单例管理
# ═══════════════════════════════════════════════════════════════════════════════

_registry_instance: Optional[CourtPositionRegistry] = None
_registry_lock = threading.Lock()


def get_court_registry() -> CourtPositionRegistry:
    """获取 CourtPositionRegistry 单例"""
    global _registry_instance
    if _registry_instance is None:
        with _registry_lock:
            if _registry_instance is None:
                _registry_instance = CourtPositionRegistry()
    return _registry_instance


__all__ = [
    # 核心类
    "CourtPositionRegistry",
    "DepartmentPositionTree",
    "Position",
    # 枚举
    "NobilityRank", "PinRank", "PositionType", "SystemType", "SageType",
    # 名称映射
    "_NOBILITY_NAMES", "_NOBILITY_AUTHORITY",
    "_PIN_NAMES", "_SAGE_TYPE_NAMES", "_SAGE_TYPE_SYMBOLS",
    "_PRACTITIONER_QUOTA",
    # 辅助
    "_p", "_zheng_cong_pair", "_specialist_batch",
    # 单例 & 工具
    "get_court_registry", "get_sage_court_position",
]
