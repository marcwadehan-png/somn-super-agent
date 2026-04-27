# -*- coding: utf-8 -*-
"""
朝廷岗位体系 V4.2.0
_court_positions.py

基于神之架构V4.2.0，"全贤就位，百官齐备，决策为纲"。

重构说明（V6.2）：
  - 枚举定义已提取到 court_enums.py
  - Position/DepartmentPositionTree 已提取到 court_models.py
  - 辅助函数(_p, _zheng_cong_pair, _specialist_batch) 已提取到 court_helpers.py
  - 各系统岗位构建函数已提取到 positions_*.py
  - 本文件仅保留 CourtPositionRegistry 和模块级便捷接口
"""

from typing import Any, Dict, List, Optional, Tuple

# 导入枚举定义
from .court_enums import (
    NobilityRank, PinRank, PositionType, SystemType, SageType,
    _NOBILITY_NAMES, _NOBILITY_AUTHORITY,
    _PIN_NAMES, _SAGE_TYPE_SYMBOLS,
    _PRACTITIONER_QUOTA,
    is_zheng_pin, is_cong_pin, get_pin_level,
)

# 导入数据模型
from .court_models import Position, DepartmentPositionTree

# 导入辅助函数
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch

# 导入各系统岗位构建函数
from .positions_royal import build_royal_positions
from .positions_wenzhi import build_wenzhi_positions
from .positions_economy import build_economy_positions
from .positions_military import build_military_positions
from .positions_standard import build_standard_positions
from .positions_chuangxin import build_chuangxin_positions
from .positions_review import build_review_positions
from .positions_library import build_library_positions
from .positions_congress import build_congress_positions
from .positions_specialist import build_specialist_leaders
from .positions_supplement import build_supplement_positions


# ═══════════════════════════════════════════════════════════════
#  八、岗位注册中心
# ═══════════════════════════════════════════════════════════════

class CourtPositionRegistry:
    """
    朝廷岗位注册中心 v2.0

    管理所有部门的完整岗位树，提供岗位查询、贤者分配、
    调度链路验证等功能。

    双轨制：爵位（决策权） + 品秩（行政级别）
    """

    _instance: Optional['CourtPositionRegistry'] = None
    _initialized: bool = False

    def __new__(cls) -> 'CourtPositionRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if CourtPositionRegistry._initialized:
            return
        CourtPositionRegistry._initialized = True

        self._positions: Dict[str, Position] = {}
        self._departments: Dict[str, DepartmentPositionTree] = {}
        self._school_position_map: Dict[str, List[str]] = {}
        self._sage_position_map: Dict[str, str] = {}
        self._position_sage_map: Dict[str, List[str]] = {}
        self._total_sage_count: int = 862

        self._build_all_positions()
        self._refresh_total_sage_count()

    # -------- 内部方法 --------

    def _refresh_total_sage_count(self) -> None:
        """动态获取贤者总数，替代硬编码"""
        try:
            from ._sage_registry_full import get_registry_stats
            stats = get_registry_stats()
            count = stats.get("total", 0) if isinstance(stats, dict) else 0
            if count and count > 0:
                self._total_sage_count = count
        except (ImportError, AttributeError, TypeError):
            pass

    def _build_all_positions(self) -> None:
        """构建所有系统的岗位树"""
        builders = [
            ("七人代表大会", build_congress_positions),
            ("皇家", build_royal_positions),
            ("文治系统", build_wenzhi_positions),
            ("经济系统", build_economy_positions),
            ("军政系统", build_military_positions),
            ("标准系统", build_standard_positions),
            ("创新系统", build_chuangxin_positions),
            ("审核系统", build_review_positions),
            ("皇家藏书阁", build_library_positions),
            ("专员领班", build_specialist_leaders),
            ("岗位补充", build_supplement_positions),
        ]

        for dept_name, builder in builders:
            positions = builder()
            tree = DepartmentPositionTree(department=dept_name)
            for pos in positions:
                tree.add_position(pos)
                self._positions[pos.id] = pos

                for school in pos.suitable_schools:
                    if school not in self._school_position_map:
                        self._school_position_map[school] = []
                    self._school_position_map[school].append(pos.id)

            self._departments[dept_name] = tree

    # -------- 查询接口 --------

    def get_position(self, position_id: str) -> Optional[Position]:
        return self._positions.get(position_id)

    def get_all_departments(self) -> List[str]:
        return list(self._departments.keys())

    def get_positions_by_department(self, department: str) -> List[Position]:
        tree = self._departments.get(department)
        if tree:
            return list(tree.positions.values())
        return [p for p in self._positions.values() if p.department == department]

    def get_positions_by_pin(self, pin: PinRank) -> List[Position]:
        return [p for p in self._positions.values() if p.pin == pin]

    def get_positions_by_nobility(self, nobility: NobilityRank) -> List[Position]:
        return [p for p in self._positions.values() if p.nobility == nobility]

    def get_positions_by_school(self, school: str) -> List[Position]:
        ids = self._school_position_map.get(school, [])
        return [self._positions[i] for i in ids if i in self._positions]

    def get_best_position_for_sage(
        self,
        sage_name: str,
        school: str = "",
        tier: Any = None,
        expertise: List[str] = None,
    ) -> Optional[Position]:
        """为贤者匹配最佳岗位"""
        from ._sage_registry_full import get_sage
        sage = get_sage(sage_name)
        if sage:
            school = sage.school
            expertise = sage.expertise
            tier = sage.tier

        suitable = self.get_positions_by_school(school)
        if not suitable:
            suitable = [p for p in self._positions.values() if "儒家" in p.suitable_schools]

        if not suitable:
            return None

        fixed = [p for p in suitable if p.capacity != 999]
        specialists = [p for p in suitable if p.capacity == 999]

        fixed.sort(key=lambda p: p.authority_value)
        for pos in fixed:
            filled = len(self._position_sage_map.get(pos.id, []))
            if filled < pos.capacity:
                return pos

        non_wenzhi_spec = [p for p in specialists if p.system_type != SystemType.WENZHI]
        if non_wenzhi_spec:
            non_wenzhi_spec.sort(key=lambda p: p.pin.value)
            return non_wenzhi_spec[0]

        if specialists:
            specialists.sort(key=lambda p: p.pin.value)
            return specialists[0]

        return None

    # -------- 分配接口 --------

    def assign_sage(self, sage_name: str, position_id: str) -> bool:
        """将贤者分配到指定岗位"""
        pos = self._positions.get(position_id)
        if not pos:
            return False

        filled = len(self._position_sage_map.get(position_id, []))
        if pos.capacity != 999 and filled >= pos.capacity:
            return False

        if sage_name in self._sage_position_map:
            old_pos_id = self._sage_position_map[sage_name]
            if old_pos_id in self._position_sage_map:
                self._position_sage_map[old_pos_id] = [
                    n for n in self._position_sage_map[old_pos_id] if n != sage_name
                ]

        self._sage_position_map[sage_name] = position_id
        if position_id not in self._position_sage_map:
            self._position_sage_map[position_id] = []
        self._position_sage_map[position_id].append(sage_name)
        pos.assigned_sages.append(sage_name)

        return True

    def auto_assign_all_sages(self) -> Dict[str, Any]:
        """自动为所有贤者分配岗位"""
        from ._sage_registry_full import ALL_SAGES

        stats = {
            "total": 0, "assigned": 0, "failed": 0,
            "by_department": {}, "by_system": {}, "by_nobility": {},
            "by_pin": {},
            "failed_sages": [],
        }

        for school, sages in ALL_SAGES.items():
            for sage in sages:
                stats["total"] += 1
                pos = self.get_best_position_for_sage(
                    sage.name, sage.school, sage.tier, sage.expertise
                )
                if pos:
                    if self.assign_sage(sage.name, pos.id):
                        stats["assigned"] += 1
                        dept = pos.department
                        stats["by_department"][dept] = stats["by_department"].get(dept, 0) + 1
                        sys_type = pos.system_type.value
                        stats["by_system"][sys_type] = stats["by_system"].get(sys_type, 0) + 1
                        if pos.nobility != NobilityRank.NOBLE_NONE:
                            noble_name = _NOBILITY_NAMES[pos.nobility]
                            stats["by_nobility"][noble_name] = stats["by_nobility"].get(noble_name, 0) + 1
                        pin_name = _PIN_NAMES.get(pos.pin, str(pos.pin.value))
                        stats["by_pin"][pin_name] = stats["by_pin"].get(pin_name, 0) + 1
                    else:
                        stats["failed"] += 1
                        stats["failed_sages"].append(sage.name)
                else:
                    stats["failed"] += 1
                    stats["failed_sages"].append(sage.name)

        return stats

    def get_sage_position(self, sage_name: str) -> Optional[Tuple[str, Position]]:
        """获取贤者的岗位信息"""
        pos_id = self._sage_position_map.get(sage_name)
        if pos_id:
            return pos_id, self._positions[pos_id]
        return None

    # -------- 升级同步 --------

    def sync_sage_upgrade(
        self,
        sage_name: str,
        new_tier: Any,
        new_capabilities: Optional[List[str]] = None,
    ) -> bool:
        """贤者升级时同步岗位"""
        current = self.get_sage_position(sage_name)
        if not current:
            from ._sage_registry_full import get_sage
            sage = get_sage(sage_name)
            if sage:
                pos = self.get_best_position_for_sage(sage.name, sage.school, new_tier)
                if pos:
                    return self.assign_sage(sage.name, pos.id)
            return False

        pos_id, pos = current

        from ._sage_registry_full import SageTier
        target_max_authority = 99
        if new_tier == SageTier.FOUNDER:
            target_max_authority = 2
        elif new_tier == SageTier.MASTER:
            target_max_authority = 3
        elif new_tier == SageTier.SCHOLAR:
            target_max_authority = 40

        if pos.authority_value > target_max_authority:
            from ._sage_registry_full import get_sage
            sage = get_sage(sage_name)
            if sage:
                better_pos = self.get_best_position_for_sage(
                    sage.name, sage.school, new_tier
                )
                if better_pos and better_pos.authority_value < pos.authority_value:
                    return self.assign_sage(sage.name, better_pos.id)

        return True

    # -------- 统计接口 --------

    def get_stats(self) -> Dict[str, Any]:
        """获取岗位体系统计信息"""
        total_positions = len(self._positions)
        total_capacity = sum(
            p.capacity if p.capacity != 999 else 0
            for p in self._positions.values()
        )
        specialist_count = sum(
            1 for p in self._positions.values()
            if p.position_type == PositionType.SPECIALIST
        )
        noble_count = sum(
            1 for p in self._positions.values()
            if p.nobility != NobilityRank.NOBLE_NONE
        )
        total_assigned = len(self._sage_position_map)

        by_dept = {}
        by_system = {}
        by_nobility = {}
        by_pin = {}
        for pos in self._positions.values():
            dept = pos.department
            by_dept[dept] = by_dept.get(dept, 0) + 1
            sys_val = pos.system_type.value
            by_system[sys_val] = by_system.get(sys_val, 0) + 1
            if pos.nobility != NobilityRank.NOBLE_NONE:
                n = _NOBILITY_NAMES[pos.nobility]
                by_nobility[n] = by_nobility.get(n, 0) + 1
            pn = _PIN_NAMES.get(pos.pin, str(pos.pin.value))
            by_pin[pn] = by_pin.get(pn, 0) + 1

        return {
            "total_positions": total_positions,
            "total_fixed_capacity": total_capacity,
            "specialist_positions": specialist_count,
            "noble_positions": noble_count,
            "total_assigned_sages": total_assigned,
            "departments": len(self._departments),
            "by_department": by_dept,
            "by_system": by_system,
            "by_nobility": by_nobility,
            "by_pin": by_pin,
            "coverage_pct": (total_assigned / self._total_sage_count * 100) if self._total_sage_count > 0 else 0,
        }

    def get_department_tree(self, department: str) -> Optional[Dict[str, Any]]:
        """获取部门完整岗位树"""
        tree = self._departments.get(department)
        if not tree:
            return None

        result = {
            "department": department,
            "positions": {},
            "si_groups": tree.si_groups,
        }

        for pos_id, pos in tree.positions.items():
            assigned = self._position_sage_map.get(pos_id, [])
            result["positions"][pos_id] = {
                "name": pos.name,
                "display_rank": pos.display_rank,
                "nobility": _NOBILITY_NAMES.get(pos.nobility, "无"),
                "pin": _PIN_NAMES.get(pos.pin, str(pos.pin.value)),
                "is_zheng": pos.is_zheng,
                "type": pos.position_type.value,
                "system": pos.system_type.value,
                "capacity": pos.capacity,
                "assigned": len(assigned),
                "sages": assigned,
                "domain": pos.domain,
                "authority_value": pos.authority_value,
            }

        return result

    def validate_dispatch_coverage(self) -> Dict[str, Any]:
        """验证调度覆盖率"""
        issues = []

        for pos_id, pos in self._positions.items():
            if not pos.dispatch_path and pos.pin.value <= PinRank.ZHENG_4_PIN.value:
                issues.append(f"岗位 {pos.name}({pos_id}) 缺少调用链路")

        from ._sage_registry_full import ALL_SAGES
        unassigned = []
        for school, sages in ALL_SAGES.items():
            for sage in sages:
                if sage.name not in self._sage_position_map:
                    unassigned.append(f"{sage.name}({sage.school})")

        return {
            "total_positions": len(self._positions),
            "positions_without_dispatch": len([i for i in issues if "调用链路" in i]),
            "unassigned_sages": len(unassigned),
            "issues": issues[:20],
            "unassigned_list": unassigned[:20],
            "coverage_ok": len(issues) == 0 and len(unassigned) == 0,
        }

    def get_nobility_overview(self) -> List[Dict[str, Any]]:
        """获取所有爵位岗位的概况"""
        result = []
        for nobility in [NobilityRank.WANGJUE, NobilityRank.GONGJUE,
                         NobilityRank.HOUJUE, NobilityRank.BOJUE]:
            positions = self.get_positions_by_nobility(nobility)
            for pos in positions:
                assigned = self._position_sage_map.get(pos.id, [])
                result.append({
                    "nobility": _NOBILITY_NAMES[nobility],
                    "position_name": pos.name,
                    "department": pos.department,
                    "pin": _PIN_NAMES.get(pos.pin, str(pos.pin.value)),
                    "system": pos.system_type.value,
                    "capacity": pos.capacity,
                    "assigned": len(assigned),
                    "sages": assigned,
                    "domain": pos.domain,
                    "sage_type": _SAGE_TYPE_NAMES.get(pos.sage_type, "") if pos.sage_type else "",
                    "sage_type_symbol": _SAGE_TYPE_SYMBOLS.get(pos.sage_type, "") if pos.sage_type else "",
                })
        return result

    def get_practitioner_stats(self) -> Dict[str, Any]:
        """获取实战派统计信息"""
        practitioner_positions = []
        theorist_positions = []
        dual_type_positions = []

        for pos in self._positions.values():
            if pos.sage_type == SageType.PRACTITIONER:
                practitioner_positions.append({
                    "name": pos.name,
                    "department": pos.department,
                    "nobility": _NOBILITY_NAMES.get(pos.nobility, "无"),
                    "domain": pos.domain,
                })
            elif pos.sage_type == SageType.THEORIST:
                theorist_positions.append({
                    "name": pos.name,
                    "department": pos.department,
                    "nobility": _NOBILITY_NAMES.get(pos.nobility, "无"),
                })
            elif pos.sage_type == SageType.DUAL_TYPE:
                dual_type_positions.append({
                    "name": pos.name,
                    "department": pos.department,
                    "nobility": _NOBILITY_NAMES.get(pos.nobility, "无"),
                })

        return {
            "practitioner_count": len(practitioner_positions),
            "theorist_count": len(theorist_positions),
            "dual_type_count": len(dual_type_positions),
            "practitioner_positions": practitioner_positions,
            "theorist_positions": theorist_positions,
            "dual_type_positions": dual_type_positions,
        }

    def check_practitioner_quota(self) -> Dict[str, Any]:
        """检查各系统实战派占比是否达标"""
        results = {}
        for sys_type in SystemType:
            sys_name = sys_type.value
            quota = _PRACTITIONER_QUOTA.get(sys_name)
            if quota is None:
                results[sys_name] = {"status": "skip", "reason": "无实战派要求"}
                continue

            sys_positions = [
                p for p in self._positions.values()
                if p.system_type == sys_type
                and p.nobility != NobilityRank.NOBLE_NONE
            ]
            practitioner_count = sum(
                1 for p in sys_positions
                if p.sage_type == SageType.PRACTITIONER
            )
            dual_count = sum(
                1 for p in sys_positions
                if p.sage_type == SageType.DUAL_TYPE
            )
            effective_count = practitioner_count + dual_count

            results[sys_name] = {
                "quota": quota,
                "practitioner": practitioner_count,
                "dual_type": dual_count,
                "effective": effective_count,
                "status": "pass" if effective_count >= quota else "fail",
            }
        return results


# ═══════════════════════════════════════════════════════════════
#  九、模块级便捷接口
# ═══════════════════════════════════════════════════════════════

_registry_instance: Optional[CourtPositionRegistry] = None


def get_court_registry() -> CourtPositionRegistry:
    """获取岗位注册中心单例"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = CourtPositionRegistry()
    return _registry_instance


def get_sage_court_position(sage_name: str) -> Optional[Position]:
    """获取贤者的朝廷岗位"""
    registry = get_court_registry()
    result = registry.get_sage_position(sage_name)
    if result:
        return result[1]
    return None


def auto_assign_all() -> Dict[str, Any]:
    """自动为所有贤者分配岗位"""
    return get_court_registry().auto_assign_all_sages()
