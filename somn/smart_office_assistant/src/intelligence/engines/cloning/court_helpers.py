# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 辅助函数模块
"""
from typing import List, Tuple, Optional
from .court_enums import PinRank, NobilityRank, SystemType, SageType, PositionType
from .court_models import Position


# 字符串到枚举的映射
_STR_TO_SYSTEM_TYPE = {e.value: e for e in SystemType}
_STR_TO_SAGE_TYPE = {e.value: e for e in SageType}
_STR_TO_POSITION_TYPE = {
    "execution": PositionType.EXECUTION,
    "management": PositionType.MANAGEMENT,
    "specialist": PositionType.SPECIALIST,
    "supreme_single": PositionType.SUPREME_SINGLE,
}


def _resolve_system_type(v):
    if v is None:
        return SystemType.STANDARD
    if isinstance(v, SystemType):
        return v
    return _STR_TO_SYSTEM_TYPE.get(str(v), SystemType.STANDARD)


def _resolve_sage_type(v):
    if v is None:
        return None
    if isinstance(v, SageType):
        return v
    return _STR_TO_SAGE_TYPE.get(str(v), None)


def _resolve_position_type(v):
    if v is None:
        return PositionType.EXECUTION
    if isinstance(v, PositionType):
        return v
    return _STR_TO_POSITION_TYPE.get(str(v), PositionType.EXECUTION)


def _p(
    id: str, name: str, department: str,
    pin: PinRank = PinRank.CONG_7_PIN,
    nobility=None,  # 可接受NobilityRank或int
    position_type=None,  # 可接受PositionType或str
    capacity: int = 1,
    is_zheng: bool = True,
    system_type=None,  # 可接受SystemType或str
    domain: str = "",
    si_name: str = "",
    track: str = "both",
    dispatch_path: str = "",
    suitable_schools: List[str] = None,
    description: str = "",
    sage_type=None,  # 可接受SageType或str
    practitioner_quota: int = 0,
    # 支持 _str 后缀参数（从positions_*.py传入的字符串版本）
    position_type_str: str = None,
    system_type_str: str = None,
    sage_type_str: str = None,
    nobility_val: int = None,
) -> Position:
    """快速创建Position的工厂函数，支持枚举或字符串参数"""
    # 解析 position_type
    pt = position_type or position_type_str
    position_type_resolved = _resolve_position_type(pt)

    # 解析 system_type
    st = system_type or system_type_str
    system_type_resolved = _resolve_system_type(st)

    # 解析 sage_type
    sg = sage_type or sage_type_str
    sage_type_resolved = _resolve_sage_type(sg)

    # 解析 nobility
    nobility_resolved = nobility
    if nobility_val is not None:
        nobility_resolved = NobilityRank(nobility_val)
    elif nobility is None:
        nobility_resolved = NobilityRank.NOBLE_NONE

    return Position(
        id=id, name=name, department=department,
        system_type=system_type_resolved,
        nobility=nobility_resolved, pin=pin,
        position_type=position_type_resolved,
        capacity=capacity, is_zheng=is_zheng,
        domain=domain, si_name=si_name,
        track=track, dispatch_path=dispatch_path,
        suitable_schools=suitable_schools or [],
        description=description,
        sage_type=sage_type_resolved,
        practitioner_quota=practitioner_quota,
    )


def _zheng_cong_pair(
    base_id: str, base_name: str, department: str,
    pin_level: int,
    domain: str = "",
    si_name: str = "",
    track: str = "both",
    dispatch_path_prefix: str = "",
    suitable_schools: List[str] = None,
    description_prefix: str = "",
    system_type=None,  # 可接受SystemType或str
    sage_type=None,  # 可接受SageType或str
    # 支持 _str 后缀参数
    system_type_str: str = None,
    sage_type_str: str = None,
) -> List[Position]:
    """创建一正一副双岗（管理层标准配置），支持枚举或字符串参数"""
    # 解析 system_type
    st = system_type or system_type_str
    system_type_resolved = _resolve_system_type(st)

    # 解析 sage_type
    sg = sage_type or sage_type_str
    sage_type_resolved = _resolve_sage_type(sg)

    pin_zheng = PinRank(pin_level * 10)
    pin_cong = PinRank(pin_level * 10 + 1)

    positions = []
    # 正品
    pos_z = _p(
        id=f"{base_id}_Z", name=f"{base_name}（正{pin_level}品）",
        department=department,
        pin=pin_zheng,
        position_type="management",
        capacity=1, is_zheng=True, system_type=system_type_resolved,
        domain=domain, si_name=si_name, track=track,
        dispatch_path=dispatch_path_prefix,
        suitable_schools=suitable_schools,
        description=f"{description_prefix}（正品）" if description_prefix else "",
        sage_type=sage_type_resolved,
    )
    positions.append(pos_z)

    # 从品
    pos_c = _p(
        id=f"{base_id}_C", name=f"{base_name}（从{pin_level}品）",
        department=department,
        pin=pin_cong,
        position_type="management",
        capacity=1, is_zheng=False, system_type=system_type_resolved,
        domain=domain, si_name=si_name, track=track,
        dispatch_path=dispatch_path_prefix,
        suitable_schools=suitable_schools,
        description=f"{description_prefix}（从品）" if description_prefix else "",
        sage_type=sage_type_resolved,
    )
    positions.append(pos_c)
    return positions


def _specialist_batch(
    base_id: str, department: str,
    pin: PinRank = None,
    track: str = "both",
    items: List[Tuple[str, str, List[str]]] = None,
    # 支持从positions_*.py传入的参数
    system_type=None,
    system_type_str: str = None,
    pin_level: int = None,  # 整数品级，自动转为PinRank
) -> List[Position]:
    """批量创建专员岗位，支持 pin(PinRank) 或 pin_level(int) 参数"""
    # 解析 pin
    if pin is None:
        if pin_level is not None:
            pin = PinRank(pin_level * 10)  # 正品
        else:
            pin = PinRank.ZHENG_7_PIN

    st = system_type or system_type_str
    system_type_resolved = _resolve_system_type(st)
    positions = []
    for i, (name, domain, schools) in enumerate(items or [], 1):
        positions.append(_p(
            id=f"{base_id}_{i:02d}", name=f"{department}·{name}",
            department=department,
            pin=pin, position_type="specialist",
            capacity=999, track=track,
            domain=domain, suitable_schools=schools,
            description=f"{department}{domain}专员",
            system_type=system_type_resolved,
        ))
    return positions
