# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 枚举定义模块

从 _court_positions.py 提取，V4.2.0
"""
from enum import Enum, IntEnum
from typing import Dict


# ══════════════════════════════════════════════════════════════════════════════
#  一、爵位枚举
# ══════════════════════════════════════════════════════════════════════════════

class NobilityRank(IntEnum):
    """爵位等级（决策权维度）"""
    WANGJUE = 0     # 王爵 - 最高决策权
    GONGJUE = 1     # 公爵 - 等于一品，决策权 > 一品
    HOUJUE = 2      # 侯爵 - 等于一品品秩，决策权介于一品~二品
    BOJUE = 3       # 伯爵 - 等于三品品秩，决策权介于三品~二品
    NOBLE_NONE = 99 # 无爵位


# 爵位显示名
_NOBILITY_NAMES: Dict[NobilityRank, str] = {
    NobilityRank.WANGJUE: "王爵",
    NobilityRank.GONGJUE: "公爵",
    NobilityRank.HOUJUE: "侯爵",
    NobilityRank.BOJUE: "伯爵",
    NobilityRank.NOBLE_NONE: "无",
}

# 爵位决策权排序值（越小决策权越大）
_NOBILITY_AUTHORITY: Dict[NobilityRank, int] = {
    NobilityRank.WANGJUE: 0,
    NobilityRank.GONGJUE: 1,
    NobilityRank.HOUJUE: 2,
    NobilityRank.BOJUE: 5,
    NobilityRank.NOBLE_NONE: 99,
}


# ══════════════════════════════════════════════════════════════════════════════
#  1.5 贤者类型枚举
# ══════════════════════════════════════════════════════════════════════════════

class SageType(str, Enum):
    """贤者能力类型"""
    PRACTITIONER = "practitioner"   # 实战派
    THEORIST = "theorist"           # 理论派
    DUAL_TYPE = "dual_type"         # 复合型


_SAGE_TYPE_NAMES: Dict[SageType, str] = {
    SageType.PRACTITIONER: "实战派",
    SageType.THEORIST: "理论派",
    SageType.DUAL_TYPE: "复合型",
}

_SAGE_TYPE_SYMBOLS: Dict[SageType, str] = {
    SageType.PRACTITIONER: "",
    SageType.THEORIST: "",
    SageType.DUAL_TYPE: "",
}

# 各系统实战派占比要求
_PRACTITIONER_QUOTA: Dict[str, object] = {
    "royal": None,
    "military": 0.5,
    "wenzhi": None,
    "economy": 2,
    "standard": 1,
    "innovation": 2,
}


# ══════════════════════════════════════════════════════════════════════════════
#  二、品秩枚举
# ══════════════════════════════════════════════════════════════════════════════

class PinRank(IntEnum):
    """品秩（行政维度，正从各九品）"""
    ZHENG_1_PIN = 10
    CONG_1_PIN = 11
    ZHENG_2_PIN = 20
    CONG_2_PIN = 21
    ZHENG_3_PIN = 30
    CONG_3_PIN = 31
    ZHENG_4_PIN = 40
    CONG_4_PIN = 41
    ZHENG_5_PIN = 50
    CONG_5_PIN = 51
    ZHENG_6_PIN = 60
    CONG_6_PIN = 61
    ZHENG_7_PIN = 70
    CONG_7_PIN = 71
    ZHENG_8_PIN = 80
    CONG_8_PIN = 81
    ZHENG_9_PIN = 90
    CONG_9_PIN = 91


_PIN_NAMES: Dict[PinRank, str] = {
    PinRank.ZHENG_1_PIN: "正一品", PinRank.CONG_1_PIN: "从一品",
    PinRank.ZHENG_2_PIN: "正二品", PinRank.CONG_2_PIN: "从二品",
    PinRank.ZHENG_3_PIN: "正三品", PinRank.CONG_3_PIN: "从三品",
    PinRank.ZHENG_4_PIN: "正四品", PinRank.CONG_4_PIN: "从四品",
    PinRank.ZHENG_5_PIN: "正五品", PinRank.CONG_5_PIN: "从五品",
    PinRank.ZHENG_6_PIN: "正六品", PinRank.CONG_6_PIN: "从六品",
    PinRank.ZHENG_7_PIN: "正七品", PinRank.CONG_7_PIN: "从七品",
    PinRank.ZHENG_8_PIN: "正八品", PinRank.CONG_8_PIN: "从八品",
    PinRank.ZHENG_9_PIN: "正九品", PinRank.CONG_9_PIN: "从九品",
}


def is_zheng_pin(pin: PinRank) -> bool:
    return pin.value % 10 == 0


def is_cong_pin(pin: PinRank) -> bool:
    return pin.value % 10 == 1


def get_pin_level(pin: PinRank) -> int:
    return pin.value // 10


# ══════════════════════════════════════════════════════════════════════════════
#  三、岗位类型
# ══════════════════════════════════════════════════════════════════════════════

class PositionType(Enum):
    SUPREME_SINGLE = "supreme_single"
    SUPREME_TRIPLE = "supreme_triple"
    SUPREME_DUAL = "supreme_dual"
    MANAGEMENT = "management"
    EXECUTION = "execution"
    SPECIALIST = "specialist"
    AUDIT = "audit"
    TEAM_LEADER = "team_leader"


# ══════════════════════════════════════════════════════════════════════════════
#  四、系统类型
# ══════════════════════════════════════════════════════════════════════════════

class SystemType(Enum):
    ROYAL = "royal"
    MILITARY = "military"
    WENZHI = "wenzhi"
    ECONOMY = "economy"
    STANDARD = "standard"
    INNOVATION = "innovation"
    REVIEW = "review"
    CANGSHUGE = "cangshuge"
