# -*- coding: utf-8 -*-
"""
藏书阁工作人员动态注册表 v1.0
_library_staff_registry.py

将藏书阁的硬编码人员名单改为运行时动态注册制：
- 启动时从配置/神之架构岗位表加载基础人员
- 运行时各子系统通过桥接动态注册/注销
- 支持按职务、分馆、权限查询
- 与 ImperialLibrary 的权限检查无缝对接

替代原 _imperial_library.py 中的:
- _LIBRARY_STAFF (硬编码集合)
- WING_PERMISSIONS (静态权限表)
- _check_permission() (简单集合匹配)

版本: v1.0.0
创建: 2026-04-28
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# 延迟导入避免循环依赖
def _get_library_enums():
    """获取 LibraryPermission/LibraryWing 枚举（延迟）"""
    result = {}
    try:
        from ._imperial_library import LibraryPermission, LibraryWing, MemoryGrade
        result["LibraryPermission"] = LibraryPermission
        result["LibraryWing"] = LibraryWing
    except ImportError:
        pass
    return result


# ═══════════════════════════════════════════════════════════════════
#  职务枚举
# ═══════════════════════════════════════════════════════════════════

class StaffRole(Enum):
    """藏书阁内部职务层级（从高到低）"""
    CHANCELLOR = auto()   # 大学士 / 馆长 — ADMIN 权限，独享
    SHILANG = auto()      # 侍郎 / 分馆长 — WRITE + 分馆管理
    XIUXIU = auto()       # 编修 / 格子编写审核 — WRITE
    JAOLI = auto()        # 校理 / 格子校对维护 — WRITE
    LINGBAN = auto()      # 领班 / 日常运维 — WRITE


class StaffType(Enum):
    """工作人员类型"""
    HUMAN = "human"              # 真人（历史人物角色）
    AGENT = "agent"              # AI智能体（Claw贤者）
    TEAM = "team"                # 团队（专员团队等）
    SYSTEM = "system"            # 系统（自动进程）


# 职务对应的默认权限
ROLE_DEFAULT_PERMISSIONS: Dict[StaffRole, List[str]] = {
    StaffRole.CHANCELLOR: ["admin", "write", "delete", "submit", "read_only"],
    StaffRole.SHILANG:      ["write", "delete", "submit", "read_only"],
    StaffRole.XIUXIU:       ["write", "submit", "read_only"],
    StaffRole.JAOLI:        ["write", "submit", "read_only"],
    StaffRole.LINGBAN:       ["write", "submit", "read_only"],
}

# 职务中文名称
ROLE_NAMES: Dict[StaffRole, str] = {
    StaffRole.CHANCELLOR: "大学士",
    StaffRole.SHILANG: "侍郎",
    StaffRole.XIUXIU: "编修",
    StaffRole.JAOLI: "校理",
    StaffRole.LINGBAN: "领班",
}


# ═══════════════════════════════════════════════════════════════════
#  数据结构
# ═══════════════════════════════════════════════════════════════════

@dataclass
class LibraryStaffRecord:
    """藏书阁工作人员记录"""
    name: str                              # 姓名/标识（唯一）
    role: StaffRole                        # 职务
    staff_type: StaffType = StaffType.HUMAN # 类型
    claw_id: str = ""                      # 关联Claw ID（staff_type=AGENT时）
    position: str = ""                     # 神之架构岗位名称
    assigned_wing: str = ""                # 负责分馆（LibraryWing.name 或 ""=全部分馆）
    permissions: List[str] = field(default_factory=list)  # 权限列表
    description: str = ""                  # 职责描述
    registered_at: float = field(default_factory=time.time)
    registered_by: str = ""                # 注册者（谁注册了这个人员）
    is_active: bool = True                 # 是否在职
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["role"] = self.role.name
        d["staff_type"] = self.staff_type.value
        return d


# ═══════════════════════════════════════════════════════════════════
#  核心注册表
# ═══════════════════════════════════════════════════════════════════

class LibraryStaffRegistry:
    """
    藏书阁工作人员动态注册表
    
    功能:
    - register(): 注册新工作人员
    - deregister(): 注销（软删除，保留历史）
    - check_permission(): 检查某人对某操作的权限
    - get_staff_by_role(): 按职务查询
    - get_staff_for_wing(): 查询负责某分馆的人员
    - load_defaults(): 加载默认基础人员
    - export/import: 序列化支持
    """
    
    def __init__(self):
        self._staff: Dict[str, LibraryStaffRecord] = {}  # name → record
        self._initialized = False
        
    def ensure_initialized(self) -> None:
        """懒加载：首次使用时加载默认人员"""
        if not self._initialized:
            self._load_default_staff()
            self._initialized = True
            logger.info(f"藏书阁工作人员注册表初始化完成: {len(self._staff)} 人")
    
    # ──────────────────────────────────────────────────────
    #  默认基础人员（对应原硬编码名单）
    # ──────────────────────────────────────────────────────
    
    def _load_default_staff(self) -> None:
        """加载默认的基础人员（原 _LIBRARY_STAFF 成员）"""
        defaults = [
            # 大学士（最高管理者）
            LibraryStaffRecord(
                name="司马迁",
                role=StaffRole.CHANCELLOR,
                staff_type=StaffType.HUMAN,
                position="藏书阁大学士·王爵",
                assigned_wing="",  # 全部分馆
                permissions=["admin", "write", "delete", "submit", "read_only"],
                description="太史公，藏书阁最高长官。记录一切有价值之记忆。",
            ),
            # 侍郎（分馆长级）
            LibraryStaffRecord(
                name="左丘明",
                role=StaffRole.SHILANG,
                staff_type=StaffType.HUMAN,
                position="左史·贤者分馆长",
                assigned_wing="SAGE",
                permissions=["write", "delete", "submit", "read_only"],
                description="负责贤者分馆的管理工作。",
            ),
            LibraryStaffRecord(
                name="班固",
                role=StaffRole.SHILANG,
                staff_type=StaffType.HUMAN,
                position="汉书·学习研究分馆长",
                assigned_wing="LEARN",
                permissions=["write", "delete", "submit", "read_only"],
                description="负责学习分馆和研究分馆的管理工作。",
            ),
            LibraryStaffRecord(
                name="司马光",
                role=StaffRole.SHILANG,
                staff_type=StaffType.HUMAN,
                position="资治通鉴·执行分馆长",
                assigned_wing="EXEC",
                permissions=["write", "delete", "submit", "read_only"],
                description="负责执行分馆和用户分馆的管理工作。",
            ),
            LibraryStaffRecord(
                name="扬雄",
                role=StaffRole.SHILANG,
                staff_type=StaffType.HUMAN,
                position="法言·外部与架构分馆长",
                assigned_wing="ARCH",
                permissions=["write", "delete", "submit", "read_only"],
                description="负责架构分馆、外部分馆和情绪分馆的管理工作。",
            ),
            # 团队账号
            LibraryStaffRecord(
                name="藏书阁专员团队",
                role=StaffRole.LINGBAN,
                staff_type=StaffType.TEAM,
                position="日常运维团队",
                assigned_wing="",  # 全部分馆
                permissions=["write", "submit", "read_only"],
                description="负责日常运维、记忆入库出库。",
            ),
        ]
        
        for record in defaults:
            self._staff[record.name] = record
    
    # ──────────────────────────────────────────────────────
    #  注册 / 注销
    # ──────────────────────────────────────────────────────
    
    def register(
        self,
        name: str,
        role: StaffRole,
        staff_type: StaffType = StaffType.AGENT,
        claw_id: str = "",
        position: str = "",
        assigned_wing: str = "",
        permissions: Optional[List[str]] = None,
        description: str = "",
        registered_by: str = "system",
    ) -> LibraryStaffRecord:
        """
        注册新的藏书阁工作人员。
        
        Args:
            name: 姓名/标识（如 Claw 名字或角色名）
            role: 职务（CHANCELLOR/SHILANG/XIUXIU/JAOLI/LINGBAN）
            staff_type: 类型（HUMAN/AGENT/TEAM/SYSTEM）
            claw_id: 关联的 Claw ID
            position: 神之架构岗位名称
            assigned_wing: 负责的分馆（空字符串=全部）
            permissions: 自定义权限列表（None则使用职务默认权限）
            description: 职责描述
            registered_by: 注册者
            
        Returns:
            创建的 LibraryStaffRecord
            
        Raises:
            ValueError: 如果已存在同名且在职人员
        """
        self.ensure_initialized()
        
        existing = self._staff.get(name)
        if existing and existing.is_active:
            logger.warning(f"工作人员 '{name}' 已存在且在职，将更新其信息")
        
        if permissions is None:
            permissions = ROLE_DEFAULT_PERMISSIONS.get(role, ["read_only"]).copy()
        
        record = LibraryStaffRecord(
            name=name,
            role=role,
            staff_type=staff_type,
            claw_id=claw_id,
            position=position,
            assigned_wing=assigned_wing,
            permissions=permissions,
            description=description,
            registered_by=registered_by,
            is_active=True,
        )
        
        self._staff[name] = record
        logger.info(f"藏书阁注册工作人员: [{role_names_cn(role)}] {name} ({staff_type.value})")
        return record
    
    def deregister(self, name: str, reason: str = "", operator: str = "") -> bool:
        """
        注销工作人员（软删除，保留历史记录）。
        
        Args:
            name: 要注销的人员名
            reason: 注销原因
            operator: 操作者
        """
        self.ensure_initialized()
        
        record = self._staff.get(name)
        if not record:
            logger.warning(f"注销失败: '{name}' 不在注册表中")
            return False
        
        if record.role == StaffRole.CHANCELLOR:
            logger.error(f"禁止注销大学士: {name}")
            return False
        
        record.is_active = False
        record.description += f"\n[于 {time.strftime('%Y-%m-%d %H:%M')} 被 {operator} 注销: {reason}]"
        logger.info(f"藏书阁注销工作人员: {name} - {reason}")
        return True
    
    # ──────────────────────────────────────────────────────
    #  权限检查（替代原 _LIBRARY_STAFF 集合匹配）
    # ──────────────────────────────────────────────────────
    
    def check_permission(self, name: str, required_permission: str) -> bool:
        """
        检查某人的权限。
        
        Args:
            name: 工作人员姓名（空字符串表示系统调用，默认通过）
            required_permission: 需要的权限 (admin/write/delete/submit/read_only)
            
        Returns:
            是否有权限
        """
        if not name:
            return True  # 系统内部调用，允许
        
        self.ensure_initialized()
        
        record = self._staff.get(name)
        if not record:
            # 不在注册表中 → 无写权限（但可读可提交）
            return required_permission in ("read_only", "submit")
        
        if not record.is_active:
            return required_permission == "read_only"
        
        return required_permission in record.permissions
    
    def has_admin_privilege(self, name: str) -> bool:
        """是否有 ADMIN 权限（仅大学士）"""
        return self.check_permission(name, "admin")
    
    def has_write_privilege(self, name: str) -> bool:
        """是否有 WRITE 权限"""
        return self.check_permission(name, "write")
    
    def has_delete_privilege(self, name: str) -> bool:
        """是否有 DELETE 权限"""
        return self.check_permission(name, "delete")
    
    def can_manage_wing(self, name: str, wing_code: str) -> bool:
        """是否能管理指定分馆"""
        self.ensure_initialized()
        record = self._staff.get(name)
        if not record or not record.is_active:
            return False
        # assigned_wing 为空表示管理全部分馆
        if not record.assigned_wing:
            return self.has_write_privilege(name)
        return record.assigned_wing == wing_code and self.has_write_privilege(name)
    
    # ──────────────────────────────────────────────────────
    #  查询接口
    # ──────────────────────────────────────────────────────
    
    def get_staff(self, name: str) -> Optional[LibraryStaffRecord]:
        """获取单条人员记录"""
        self.ensure_initialized()
        return self._staff.get(name)
    
    def get_active_staff(self) -> List[LibraryStaffRecord]:
        """获取所有在职人员"""
        self.ensure_initialized()
        return [r for r in self._staff.values() if r.is_active]
    
    def get_staff_by_role(self, role: StaffRole) -> List[LibraryStaffRecord]:
        """按职务查询"""
        self.ensure_initialized()
        return [r for r in self._staff.values() if r.role == role and r.is_active]
    
    def get_staff_for_wing(self, wing_code: str) -> List[LibraryStaffRecord]:
        """查询负责某分馆的人员（含全局人员）"""
        self.ensure_initialized()
        result = []
        for r in self._staff.values():
            if not r.is_active:
                continue
            if not r.assigned_wing or r.assigned_wing == wing_code:
                result.append(r)
        return result
    
    def get_agent_staff(self) -> List[LibraryStaffRecord]:
        """获取所有 AGENT 类型的在职人员（Claw贤者）"""
        self.ensure_initialized()
        return [r for r in self._staff.values() 
                if r.staff_type == StaffType.AGENT and r.is_active]
    
    def list_all_names_with_write(self) -> Set[str]:
        """返回所有有写权限的在职人员名字集合（兼容旧接口）"""
        self.ensure_initialized()
        return {r.name for r in self._staff.values() 
                if r.is_active and "write" in r.permissions}
    
    # ──────────────────────────────────────────────────────
    #  统计 & 导出
    # ──────────────────────────────────────────────────────
    
    def get_stats(self) -> Dict[str, Any]:
        """获取注册表统计信息"""
        self.ensure_initialized()
        active = [r for r in self._staff.values() if r.is_active]
        by_role = {}
        by_type = {}
        for r in active:
            role_name = role_names_cn(r.role)
            by_role[role_name] = by_role.get(role_name, 0) + 1
            by_type[r.staff_type.value] = by_type.get(r.staff_type.value, 0) + 1
        
        return {
            "total_registered": len(self._staff),
            "total_active": len(active),
            "by_role": by_role,
            "by_type": by_type,
            "agent_count": len(self.get_agent_staff()),
        }
    
    def export_records(self) -> List[Dict[str, Any]]:
        """导出所有记录（用于持久化）"""
        self.ensure_initialized()
        return [r.to_dict() for r in self._staff.values()]
    
    def __repr__(self) -> str:
        self.ensure_initialized()
        active_count = sum(1 for r in self._staff.values() if r.is_active)
        return f"<LibraryStaffRegistry {active_count} active / {len(self._staff)} total>"


# ═══════════════════════════════════════════════════════════════════
#  便捷函数
# ═══════════════════════════════════════════════════════════════════

_registry_instance: Optional[LibraryStaffRegistry] = None


def get_staff_registry() -> LibraryStaffRegistry:
    """获取全局注册表单例"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = LibraryStaffRegistry()
    return _registry_instance


def role_names_cn(role: StaffRole) -> str:
    """获取职务中文名"""
    return ROLE_NAMES.get(role, role.name)


def register_claw_as_staff(
    claw_name: str,
    claw_id: str,
    position: str = "",
    role: StaffRole = StaffRole.XIUXIU,
    assigned_wing: str = "",
    description: str = "",
) -> LibraryStaffRecord:
    """
    便捷函数：将一个 Claw 贤者注册为藏书阁工作人员。
    
    用于子系统启动时自动注册其 Claw 为知识库管理人员。
    """
    registry = get_staff_registry()
    return registry.register(
        name=claw_name,
        role=role,
        staff_type=StaffType.AGENT,
        claw_id=claw_id,
        position=position or f"Claw贤者·{claw_name}",
        assigned_wing=assigned_wing,
        description=description or f"{claw_name} — 通过 Claw 贤者任职机制自动注册",
        registered_by="claw_auto_register",
    )
