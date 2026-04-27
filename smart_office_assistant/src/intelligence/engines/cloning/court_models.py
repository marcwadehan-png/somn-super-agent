# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 数据模型模块
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from .court_enums import (
    NobilityRank, PinRank, PositionType, SystemType, SageType,
    _NOBILITY_NAMES, _NOBILITY_AUTHORITY,
    _PIN_NAMES, _SAGE_TYPE_SYMBOLS,
)


@dataclass
class Position:
    """朝廷岗位"""
    id: str
    name: str
    department: str
    system_type: SystemType = SystemType.STANDARD
    nobility: NobilityRank = NobilityRank.NOBLE_NONE
    pin: PinRank = PinRank.CONG_7_PIN
    position_type: PositionType = PositionType.EXECUTION
    capacity: int = 1
    is_zheng: bool = True
    domain: str = ""
    si_name: str = ""
    track: str = "both"
    dispatch_path: str = ""
    suitable_schools: List[str] = field(default_factory=list)
    assigned_sages: List[str] = field(default_factory=list)
    description: str = ""
    sage_type: Optional[SageType] = None
    practitioner_quota: int = 0

    @property
    def display_rank(self) -> str:
        parts = []
        if self.nobility != NobilityRank.NOBLE_NONE:
            parts.append(_NOBILITY_NAMES[self.nobility])
        parts.append(_PIN_NAMES.get(self.pin, str(self.pin.value)))
        return " ".join(parts)

    @property
    def authority_value(self) -> int:
        noble_auth = _NOBILITY_AUTHORITY[self.nobility]
        if self.nobility != NobilityRank.NOBLE_NONE:
            return noble_auth
        return self.pin.value

    @property
    def sage_type_display(self) -> str:
        if self.sage_type:
            return _SAGE_TYPE_SYMBOLS.get(self.sage_type, "")
        return ""


@dataclass
class DepartmentPositionTree:
    """部门岗位树"""
    department: str
    system_type: SystemType = SystemType.STANDARD
    positions: Dict[str, Position] = field(default_factory=dict)
    si_groups: Dict[str, List[str]] = field(default_factory=dict)

    def add_position(self, pos: Position) -> None:
        self.positions[pos.id] = pos
        if pos.si_name:
            if pos.si_name not in self.si_groups:
                self.si_groups[pos.si_name] = []
            self.si_groups[pos.si_name].append(pos.id)

    def get_positions_by_pin(self, pin: PinRank) -> List[Position]:
        return [p for p in self.positions.values() if p.pin == pin]

    def get_regular_capacity(self) -> int:
        return sum(
            p.capacity
            for p in self.positions.values()
            if p.position_type != PositionType.SPECIALIST
        )
