# -*- coding: utf-8 -*-
"""
朝廷岗位体系 V1.0.0
_court_positions.py

基于神之架构V4.2.0，"全贤就位，百官齐备，决策为纲"。

## V1.0.0 核心变更（2026-04-11）
  - 架构文档全面升级为V4.2.0，完整输出377岗全量数据
  - 修正注释中"11岗"为"6岗"（专员领班实际为6部门各1岗）
  - 所有岗位信息与代码实现完全一致

## V1.0.0 核心变更（2026-04-11）
  - 全面升级为神之架构V4.0.0
  - 862位贤者100%自动任命完成（覆盖率100%）
  - 364个岗位全部到位，实战派指标全部达标
  - 版本号体系统一：_court_positions V1.0.0
  - 锦衣卫五级卫从体系稳定运行（57岗完整配置）
  - 皇家藏书阁独立记忆体系（王爵扬雄·5岗）
  - 翰林院审核体系（7岗·韩非子/墨子/慎到/荀子/邹衍/公孙龙/惠施）

## v1.0.0 核心变更
  - 锦衣卫五级卫从体系：指挥使->四司(正从四品)->百户(正从五品)->总旗(正从六品)->小旗(正七品)->力士(从七品~九品)
  - 锦衣卫4司各配完整执行链：监控司/暗察司/合规司/效能司
  - 锦衣卫从军政通用专员中独立，专属专员按司分配
  - 锦衣卫岗位总量：1(指挥使) + 16(四司) + 8(百户) + 8(总旗) + 8(小旗) + 16(力士) = 57岗

## v3.3 核心变更
  - 新增皇家藏书阁（独立记忆体系，王爵扬雄）
  - 新增PositionType.TEAM_LEADER（专员领班）
  - 七人决策代表大会成员重构
  - 西方贤者名称规范化

## v3.2 核心变更
  - 新增SystemType.REVIEW（审核系统）
  - 新增PositionType.AUDIT（翰林院审核岗）
  - 新增翰林院7岗位（韩非子/墨子/慎到/荀子/邹衍/公孙龙/惠施）

## v3.1 核心变更
  - 爵位从18人扩至24人（新增6位实战派伯爵）
  - 新增SageType枚举（PRACTITIONER/THEORIST/DUAL_TYPE）
  - 经济/创新系统关键岗位任命实战派
  - 新增盐铁司、数字市易司、货币金融司、增长引擎、农学工程等机构
  - 实战派权益：爵位优先提名权 + 经济决策一票否决权
  - 专员层细化分工

## 等级体系：爵位 + 品秩 双轨制

### 爵位（决策权维度）
  王爵  - 最高决策权，皇家系统2人（孔子+司马迁）
  公爵  - 等于一品，决策权 > 一品，皇家+军政系统各1人
  侯爵  - 等于一品（品秩同），决策权介于一品~二品之间，3人
  伯爵  - 等于三品（品秩同），决策权介于三品~二品之间，18人

### 实战派标识（v3.1新增）
  PRACTITIONER - 实战派：有可量化实战成果，享爵位优先提名+经济决策否决权
  THEORIST     - 理论派：以思想建构/学术研究见长
  DUAL_TYPE    - 复合型：兼具理论与实践

### 锦衣卫五级卫从体系（v1.0.0新增）
  指挥使(伯爵·正三品) -> 四司指挥(正从四品) -> 百户(正从五品)
  -> 总旗(正从六品) -> 小旗·领班(正七品) -> 力士/校尉(从七品~九品)
  四司：监控司 / 暗察司 / 合规司 / 效能司

### 系统决策层规则
  皇家系统：1人（王爵），独裁制
  军政系统：1人（公爵），独裁制，实战派>=50%
  文治系统：3人（1正一品+2从一品），共议制，实战派>=1人
  经济系统：3人（1正一品+2从一品），共议制，实战派>=2人
  标准系统：2人（1正二品+1从二品），双人制，实战派>=1人
  创新系统：2人（双人决策），双人制，实战派>=2人

### 管理层：一正一副双岗制
### 执行层：7-9品为专员岗（多人）

### 岗位容量
  王爵/公爵岗：1人
  侯爵岗：1人
  伯爵岗：1人
  正/从一品：按系统规则
  正/从二品：一正一副（2人）
  正/从三品：一正一副（2人）
  正/从四品：一正一副（2人）
  正/从五品：一正一副（2人）
  正/从六品：一正一副（2人）
  七品~九品专员：多人（容量999）
"""

from enum import Enum, IntEnum
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════════════════════
#  一、爵位枚举
# ═══════════════════════════════════════════════════════════════════════════════

class NobilityRank(IntEnum):
    """爵位等级（决策权维度）"""
    WANGJUE = 0     # 王爵 - 最高决策权
    GONGJUE = 1     # 公爵 - 等于一品，决策权 > 一品
    HOUJUE = 2      # 侯爵 - 等于一品品秩，决策权介于一品~二品
    BOJUE = 3       # 伯爵 - 等于三品品秩，决策权介于三品~二品
    NOBLE_NONE = 99 # 无爵位

# 爵位显示名
_NOBILITY_NAMES = {
    NobilityRank.WANGJUE: "王爵",
    NobilityRank.GONGJUE: "公爵",
    NobilityRank.HOUJUE: "侯爵",
    NobilityRank.BOJUE: "伯爵",
    NobilityRank.NOBLE_NONE: "无",
}

# 爵位决策权排序值（越小决策权越大）
_NOBILITY_AUTHORITY = {
    NobilityRank.WANGJUE: 0,
    NobilityRank.GONGJUE: 1,
    NobilityRank.HOUJUE: 2,   # 介于正一品和正二品之间
    NobilityRank.BOJUE: 5,    #介于正三品和正二品之间
    NobilityRank.NOBLE_NONE: 99,
}


# ═══════════════════════════════════════════════════════════════════════════════
#  1.5 贤者类型枚举（v3.1新增）
# ═══════════════════════════════════════════════════════════════════════════════

class SageType(str, Enum):
    """贤者能力类型（v3.1新增）"""
    PRACTITIONER = "practitioner"   # 实战派：有可量化实战成果
    THEORIST = "theorist"           # 理论派：以思想建构/学术研究见长
    DUAL_TYPE = "dual_type"         # 复合型：兼具理论与实践

# 贤者类型显示名
_SAGE_TYPE_NAMES = {
    SageType.PRACTITIONER: "实战派",
    SageType.THEORIST: "理论派",
    SageType.DUAL_TYPE: "复合型",
}

# 贤者类型符号
_SAGE_TYPE_SYMBOLS = {
    SageType.PRACTITIONER: "⚔",
    SageType.THEORIST: "📚",
    SageType.DUAL_TYPE: "⚔📚",
}


# 各系统实战派占比要求
_PRACTITIONER_QUOTA = {
    "royal": None,          # 皇家系统：无要求
    "military": 0.5,        # 军政系统：>=50%（实战派+复合型占比）
    "wenzhi": None,         # 文治系统：无强制要求（天然偏理论）
    "economy": 2,           # 经济系统：>=2人（v3.1重点）
    "standard": 1,          # 标准系统：>=1人
    "innovation": 2,        # 创新系统：>=2人（v3.1最高要求）
}


# ═══════════════════════════════════════════════════════════════════════════════
#  二、品秩枚举
# ═══════════════════════════════════════════════════════════════════════════════

class PinRank(IntEnum):
    """品秩（行政维度，正从各九品）"""
    ZHENG_1PIN = 10   # 正一品
    CONG_1PIN = 11    # 从一品
    ZHENG_2PIN = 20   # 正二品
    CONG_2PIN = 21    # 从二品
    ZHENG_3PIN = 30   # 正三品
    CONG_3PIN = 31    # 从三品
    ZHENG_4PIN = 40   # 正四品
    CONG_4PIN = 41    # 从四品
    ZHENG_5PIN = 50   # 正五品
    CONG_5PIN = 51    # 从五品
    ZHENG_6PIN = 60   # 正六品
    CONG_6PIN = 61    # 从六品
    ZHENG_7PIN = 70   # 正七品
    CONG_7PIN = 71    # 从七品
    ZHENG_8PIN = 80   # 正八品
    CONG_8PIN = 81    # 从八品
    ZHENG_9PIN = 90   # 正九品
    CONG_9PIN = 91    # 从九品

# 品秩显示名
_PIN_NAMES = {
    PinRank.ZHENG_1PIN: "正一品", PinRank.CONG_1PIN: "从一品",
    PinRank.ZHENG_2PIN: "正二品", PinRank.CONG_2PIN: "从二品",
    PinRank.ZHENG_3PIN: "正三品", PinRank.CONG_3PIN: "从三品",
    PinRank.ZHENG_4PIN: "正四品", PinRank.CONG_4PIN: "从四品",
    PinRank.ZHENG_5PIN: "正五品", PinRank.CONG_5PIN: "从五品",
    PinRank.ZHENG_6PIN: "正六品", PinRank.CONG_6PIN: "从六品",
    PinRank.ZHENG_7PIN: "正七品", PinRank.CONG_7PIN: "从七品",
    PinRank.ZHENG_8PIN: "正八品", PinRank.CONG_8PIN: "从八品",
    PinRank.ZHENG_9PIN: "正九品", PinRank.CONG_9PIN: "从九品",
}


def is_zheng_pin(pin: PinRank) -> bool:
    """是否为正品"""
    return pin.value % 10 == 0


def is_cong_pin(pin: PinRank) -> bool:
    """是否为从品"""
    return pin.value % 10 == 1


def get_pin_level(pin: PinRank) -> int:
    """获取品级数字（1-9）"""
    return pin.value // 10


# ═══════════════════════════════════════════════════════════════════════════════
#  三、岗位类型
# ═══════════════════════════════════════════════════════════════════════════════

class PositionType(Enum):
    """岗位类型"""
    SUPREME_SINGLE = "supreme_single"   # 王爵/公爵：1人独裁
    SUPREME_TRIPLE = "supreme_triple"   # 三人共议（文治/经济系统）
    SUPREME_DUAL = "supreme_dual"       # 两人决策（其他系统）
    MANAGEMENT = "management"           # 管理层：一正一副（2人）
    EXECUTION = "execution"             # 执行岗：1人
    SPECIALIST = "specialist"           # 专员岗：多人（7-9品）
    AUDIT = "audit"                     # v3.2 审核岗：翰林院专用
    TEAM_LEADER = "team_leader"         # v3.3 专员领班：各级专员团队正七品


# ═══════════════════════════════════════════════════════════════════════════════
#  四、系统类型
# ═══════════════════════════════════════════════════════════════════════════════

class SystemType(Enum):
    """系统类型（决定最高决策层配置） v3.3"""
    ROYAL = "royal"           # 皇家系统：1人（王爵/公爵），独裁制
    MILITARY = "military"     # 军政系统：1人（王爵/公爵），独裁制
    WENZHI = "wenzhi"         # 文治系统：3人（1正一品 + 2从一品），共议制
    ECONOMY = "economy"       # 经济系统：3人（1正一品 + 2从一品），共议制
    STANDARD = "standard"     # 标准系统：2人（1正二品 + 1从二品），双人制
    INNOVATION = "innovation" # 创新系统：2人（双人决策），双人制，实战派>=2人
    REVIEW = "review"         # v3.2 审核系统（翰林院）：独立于六部，不参与决策生成
    CANGSHUGE = "cangshuge"   # v3.3 皇家藏书阁：独立于所有体系之外，王爵独立管理


# ═══════════════════════════════════════════════════════════════════════════════
#  五、岗位数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Position:
    """
    朝廷岗位

    双轨制：爵位（决策权） + 品秩（行政级别）
    v3.1新增：sage_type（贤者类型标识）

    Attributes:
        id: 岗位唯一标识
        name: 岗位名称
        department: 所属部门
        system_type: 所属系统类型（决定决策层配置）
        nobility: 爵位等级
        pin: 品秩等级
        position_type: 岗位类型（决定容量）
        capacity: 最大可任命人数
        is_zheng: 是否为正品（True=正品, False=从品）
        domain: 职能领域
        si_name: 所属司/局/院名称
        track: 所属轨道 (wenzhi/chuangxin/both)
        dispatch_path: 调度路径
        suitable_schools: 适合该岗位的学派列表
        assigned_sages: 已任命的贤者列表
        description: 岗位职责描述
        sage_type: 贤者能力类型（v3.1新增，实战派/理论派/复合型）
        practitioner_quota: 实战派占比要求（v3.1新增）
    """
    id: str
    name: str
    department: str
    system_type: SystemType = SystemType.STANDARD
    nobility: NobilityRank = NobilityRank.NOBLE_NONE
    pin: PinRank = PinRank.CONG_7PIN
    position_type: PositionType = PositionType.EXECUTION
    capacity: int = 1
    is_zheng: bool = True       # 正品=True, 从品=False
    domain: str = ""
    si_name: str = ""
    track: str = "both"
    dispatch_path: str = ""
    suitable_schools: List[str] = field(default_factory=list)
    assigned_sages: List[str] = field(default_factory=list)
    description: str = ""
    sage_type: Optional[SageType] = None  # v3.1: 岗位期望的贤者类型
    practitioner_quota: int = 0           # v3.1: 实战派最少人数要求

    @property
    def display_rank(self) -> str:
        """显示用的完整等级信息"""
        parts = []
        if self.nobility != NobilityRank.NOBLE_NONE:
            parts.append(_NOBILITY_NAMES[self.nobility])
        parts.append(_PIN_NAMES.get(self.pin, str(self.pin.value)))
        return " ".join(parts)

    @property
    def authority_value(self) -> int:
        """决策权数值（越小权力越大）"""
        noble_auth = _NOBILITY_AUTHORITY[self.nobility]
        # 如果有爵位，决策权 = 爵位决策权（覆盖品秩）
        # 如果无爵位，决策权 = 品秩值
        if self.nobility != NobilityRank.NOBLE_NONE:
            return noble_auth
        return self.pin.value

    @property
    def sage_type_display(self) -> str:
        """显示贤者类型标识"""
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


# ═══════════════════════════════════════════════════════════════════════════════
#  六、岗位构建辅助函数
# ═══════════════════════════════════════════════════════════════════════════════

def _p(
    id: str, name: str, department: str,
    pin: PinRank = PinRank.CONG_7PIN,
    nobility: NobilityRank = NobilityRank.NOBLE_NONE,
    position_type: PositionType = PositionType.EXECUTION,
    capacity: int = 1,
    is_zheng: bool = True,
    system_type: SystemType = SystemType.STANDARD,
    domain: str = "",
    si_name: str = "",
    track: str = "both",
    dispatch_path: str = "",
    suitable_schools: List[str] = None,
    description: str = "",
    sage_type: SageType = None,
    practitioner_quota: int = 0,
) -> Position:
    """快速创建Position的工厂函数"""
    return Position(
        id=id, name=name, department=department,
        system_type=system_type,
        nobility=nobility, pin=pin,
        position_type=position_type,
        capacity=capacity, is_zheng=is_zheng,
        domain=domain, si_name=si_name,
        track=track, dispatch_path=dispatch_path,
        suitable_schools=suitable_schools or [],
        description=description,
        sage_type=sage_type,
        practitioner_quota=practitioner_quota,
    )


def _zheng_cong_pair(
    base_id: str, base_name: str, department: str,
    pin_level: int,  # 2-6
    domain: str = "",
    si_name: str = "",
    track: str = "both",
    dispatch_path_prefix: str = "",
    suitable_schools: List[str] = None,
    description_prefix: str = "",
    system_type: SystemType = SystemType.STANDARD,
    sage_type: SageType = None,  # V1.0: 管理层sage_type支持
) -> List[Position]:
    """
    创建一正一副双岗（管理层标准配置）

    pin_level: 品级数字(2-6)，自动生成 正X品 + 从X品
    sage_type: V1.0新增，为正从双岗统一设置贤者类型
    """
    pin_zheng = PinRank(pin_level * 10)
    pin_cong = PinRank(pin_level * 10 + 1)
    pin_name = f"正{pin_level}品" if pin_level >= 2 else "正一品"
    cong_name = f"从{pin_level}品"

    positions = []
    # 正品
    positions.append(_p(
        id=f"{base_id}_Z", name=f"{base_name}（正{pin_level}品）",
        department=department,
        pin=pin_zheng, position_type=PositionType.MANAGEMENT,
        capacity=1, is_zheng=True, system_type=system_type,
        domain=domain, si_name=si_name, track=track,
        dispatch_path=dispatch_path_prefix,
        suitable_schools=suitable_schools,
        description=f"{description_prefix}（正品）" if description_prefix else "",
        sage_type=sage_type,
    ))
    # 从品
    positions.append(_p(
        id=f"{base_id}_C", name=f"{base_name}（从{pin_level}品）",
        department=department,
        pin=pin_cong, position_type=PositionType.MANAGEMENT,
        capacity=1, is_zheng=False, system_type=system_type,
        domain=domain, si_name=si_name, track=track,
        dispatch_path=dispatch_path_prefix,
        suitable_schools=suitable_schools,
        description=f"{description_prefix}（从品）" if description_prefix else "",
        sage_type=sage_type,
    ))
    return positions


def _specialist_batch(
    base_id: str, department: str,
    pin: PinRank = PinRank.ZHENG_7PIN,
    track: str = "both",
    items: List[Tuple[str, str, List[str]]] = None,
) -> List[Position]:
    """
    批量创建专员岗位

    items: [(name, domain, suitable_schools), ...]
    """
    positions = []
    for i, (name, domain, schools) in enumerate(items or [], 1):
        positions.append(_p(
            id=f"{base_id}_{i:02d}", name=f"{department}·{name}",
            department=department,
            pin=pin, position_type=PositionType.SPECIALIST,
            capacity=999, track=track,
            domain=domain, suitable_schools=schools,
            description=f"{department}{domain}专员",
        ))
    return positions


# ═══════════════════════════════════════════════════════════════════════════════
#  七、各部门岗位定义
# ═══════════════════════════════════════════════════════════════════════════════

def _build_royal_positions() -> List[Position]:
    """
    皇家系统岗位（最高决策层）

    规则：最高决策人1人（王爵或公爵）
    - 王爵·太师：1人，全局最高决策
    - 公爵·太傅：1人，副最高决策
    - 正一品~从一品中枢岗位
    - 二品~六品管理层
    - 七品~九品专员
    """
    positions = []

    # ── 王爵（全局最高，1人）──
    positions.append(_p(
        id="HJ_WJ_01", name="太师·王爵", department="皇家",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.WANGJUE,
        position_type=PositionType.SUPREME_SINGLE, capacity=1,
        system_type=SystemType.ROYAL,
        si_name="孔子",
        domain="全局最高决策与最终裁决",
        dispatch_path="皇帝→太师·王爵→孔子",
        suitable_schools=["儒家", "道家", "思想家", "哲学家"],
        description="全局最高决策人，王爵独裁，拥有最终裁决权，由孔子担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 公爵（副最高，1人）──
    positions.append(_p(
        id="HJ_GJ_01", name="太傅·公爵", department="皇家",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.GONGJUE,
        position_type=PositionType.SUPREME_SINGLE, capacity=1,
        system_type=SystemType.ROYAL,
        domain="全局战略与次高决策",
        dispatch_path="皇帝→太傅·公爵",
        suitable_schools=["儒家", "道家", "兵家", "法家"],
        description="公爵，全局战略决策，决策权大于一品，由孟子担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 侯爵（等于一品品秩，决策权介于一品~二品）──
    positions.append(_p(
        id="HJ_HJ_01", name="太保·侯爵", department="皇家",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.HOUJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ROYAL,
        domain="战略顾问与皇家事务",
        dispatch_path="皇帝→太保·侯爵",
        suitable_schools=["儒家", "道家", "佛家", "思想家"],
        description="侯爵，品秩等同一品，决策权介于正一品和正二品之间，由荀子担任",
        sage_type=SageType.DUAL_TYPE,
    ))

    # ── 伯爵（等于三品品秩，决策权介于三品~二品）──
    positions.append(_p(
        id="HJ_BJ_01", name="伯爵·皇家侍读", department="皇家",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ROYAL,
        domain="皇家文书与侍读顾问",
        dispatch_path="皇帝→伯爵·皇家侍读",
        suitable_schools=["儒家", "文学家", "思想家"],
        description="伯爵，品秩等同三品，决策权介于正三品和正二品之间，由郑玄担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 中枢管理层（正从各品，一正一副）──
    positions += _zheng_cong_pair(
        "HJ_2_01", "枢密使", "皇家", pin_level=2,
        system_type=SystemType.ROYAL,
        domain="中枢机密与信息总管",
        dispatch_path_prefix="皇帝→枢密使",
        suitable_schools=["兵家", "纵横家", "法家"],
        description_prefix="中枢机密管理",
    )

    positions += _zheng_cong_pair(
        "HJ_3_01", "翰林院掌院", "皇家", pin_level=3,
        system_type=SystemType.ROYAL,
        domain="翰林院学术总管",
        dispatch_path_prefix="皇帝→翰林院掌院",
        suitable_schools=["儒家", "文学家", "史家", "哲学家"],
        description_prefix="翰林院学术管理",
    )

    positions += _zheng_cong_pair(
        "HJ_4_01", "通政使司", "皇家", pin_level=4,
        system_type=SystemType.ROYAL,
        domain="内外奏章与信息通传",
        dispatch_path_prefix="皇帝→通政使司",
        suitable_schools=["儒家", "法家", "兵家"],
        description_prefix="奏章通传管理",
    )

    positions += _zheng_cong_pair(
        "HJ_5_01", "詹事府", "皇家", pin_level=5,
        system_type=SystemType.ROYAL,
        domain="皇家教育与辅导",
        dispatch_path_prefix="皇帝→詹事府",
        suitable_schools=["儒家", "教育家", "道家"],
        description_prefix="皇家教育管理",
    )

    positions += _zheng_cong_pair(
        "HJ_6_01", "太仆寺", "皇家", pin_level=6,
        system_type=SystemType.ROYAL,
        domain="皇家仪仗与车马",
        dispatch_path_prefix="皇帝→太仆寺",
        suitable_schools=["儒家", "法家"],
        description_prefix="皇家仪仗管理",
    )

    # ── 专员（v3.1细化分工）──
    positions += _specialist_batch(
        "HJ_P7", "皇家", PinRank.ZHENG_7PIN,
        items=[
            ("皇家文书专员", "经典抄写、文献校对、诏令起草", ["儒家", "文学家"]),
            ("经学研究员", "经典注疏、训诂研究、经义考辨", ["儒家", "思想家"]),
            ("礼仪典制专员", "朝廷礼仪、祭祀典制、文书格式", ["儒家", "思想家"]),
            ("史籍校勘专员", "史书校勘、文献考证、版本比对", ["史家", "儒家"]),
            ("文字训诂专员", "文字学研究、音韵考据、方言记录", ["儒家", "科学家"]),
            ("皇家教育专员", "皇子教育、学术传承、礼仪教学", ["儒家", "教育家", "道家"]),
            ("侍卫专员", "皇家安全、军事护卫、战时征调", ["兵家", "法家"]),
            ("天文历法专员", "天文观测、历法推算、星象记录", ["科学家", "数学"]),
        ],
    )

    return positions


def _build_wenzhi_positions() -> List[Position]:
    """
    文治系统岗位（内阁/吏部/礼部）

    规则：最高决策人3人（1正一品 + 2从一品）
    - 正一品首辅：1人（正品决策长）
    - 从一品次辅：2人（从品决策副）
    - 以下：一正一副双岗制到六品
    - 七品~九品专员
    """
    positions = []

    # ── 内阁最高决策层（3人共议）──
    # 正一品（1人）
    positions.append(_p(
        id="WZ_NG_Z1", name="内阁首辅（正一品）", department="内阁",
        pin=PinRank.ZHENG_1PIN, position_type=PositionType.SUPREME_TRIPLE,
        capacity=1, is_zheng=True,
        system_type=SystemType.WENZHI,
        domain="全局智慧协调与最高决策",
        track="wenzhi",
        dispatch_path="皇帝→SuperWisdomCoordinator→内阁首辅",
        suitable_schools=["儒家", "道家", "思想家"],
        description="文治系统最高决策人（正品），统领全局智慧协调",
    ))
    # 从一品（2人）
    positions.append(_p(
        id="WZ_NG_C1A", name="内阁次辅甲（从一品）", department="内阁",
        pin=PinRank.CONG_1PIN, position_type=PositionType.SUPREME_TRIPLE,
        capacity=1, is_zheng=False,
        system_type=SystemType.WENZHI,
        domain="智慧资源调度与学派分配",
        track="wenzhi",
        dispatch_path="皇帝→SuperWisdomCoordinator→内阁次辅甲",
        suitable_schools=["儒家", "道家", "佛家", "素书"],
        description="文治系统决策副（从品甲），统筹23个智慧学派调度",
    ))
    positions.append(_p(
        id="WZ_NG_C1B", name="内阁次辅乙（从一品）", department="内阁",
        pin=PinRank.CONG_1PIN, position_type=PositionType.SUPREME_TRIPLE,
        capacity=1, is_zheng=False,
        system_type=SystemType.WENZHI,
        domain="思维融合与统一智能",
        track="wenzhi",
        dispatch_path="皇帝→SuperWisdomCoordinator→内阁次辅乙",
        suitable_schools=["儒家", "王阳明", "杜威", "顶级思维法"],
        description="文治系统决策副（从品乙），融合思维方法与统一智能",
    ))

    # ── 内阁侯爵（等于一品品秩）──
    positions.append(_p(
        id="WZ_NG_HJ", name="内阁学士·侯爵", department="内阁",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.HOUJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.WENZHI,
        domain="内阁学士与票拟",
        track="wenzhi",
        dispatch_path="皇帝→内阁→学士·侯爵",
        suitable_schools=["儒家", "思想家", "哲学家"],
        description="内阁学士，侯爵品位，负责票拟草诏，由董仲舒担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 内阁伯爵（等于三品品秩）──
    positions.append(_p(
        id="WZ_NG_BJ", name="中书舍人·伯爵", department="内阁",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.WENZHI,
        domain="智慧分发与六部调度",
        track="wenzhi",
        dispatch_path="皇帝→内阁→中书舍人→WisdomDispatcher",
        suitable_schools=["儒家", "兵家", "法家"],
        description="中书舍人，伯爵品位，负责将内阁票拟分发至六部，由刘向担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 吏部（能力层）──
    # 伯爵·吏部尚书
    positions.append(_p(
        id="WZ_LB_BJ", name="吏部尚书·伯爵", department="吏部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.WENZHI,
        domain="学派注册/权重调度/融合决策/工匠评级",
        dispatch_path="皇帝→内阁→吏部尚书→WisdomDispatcher",
        suitable_schools=["儒家", "法家", "兵家"],
        description="吏部尚书，伯爵品位，统领能力层，由刘歆担任",
        sage_type=SageType.THEORIST,
    ))

    # 吏部管理层（正从四品~六品）
    libu_si = [
        ("文选清吏司", "学派推荐与选拔", ["儒家", "法家", "兵家"]),
        ("考功清吏司", "权重映射与考核", ["儒家", "法家", "素书"]),
        ("验封清吏司", "学派注册与枚举", ["儒家", "名家"]),
        ("稽勋清吏司", "智慧融合决策", ["道家", "佛家", "顶级思维法"]),
        ("工匠司", "工匠评级(1-9级)", ["科学家", "墨家", "企业家"]),
    ]
    for i, (si_name, domain, schools) in enumerate(libu_si, 1):
        positions += _zheng_cong_pair(
            f"WZ_LB_4_{i:02d}", f"吏部{si_name}", "吏部", pin_level=4,
            system_type=SystemType.WENZHI,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→内阁→吏部→{si_name}",
            suitable_schools=schools,
            description_prefix=f"吏部{si_name}，负责{domain}",
        )

    for i, (name, domain, schools) in enumerate([
        ("学派管理主事", "学派日常管理", ["儒家", "法家"]),
        ("权重调整主事", "学派权重微调", ["素书", "道家"]),
        ("融合审核主事", "融合决策审核", ["顶级思维法", "科学思维"]),
        ("工匠考核主事", "工匠评级执行", ["墨家", "科学家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"WZ_LB_6_{i:02d}", f"吏部·{name}", "吏部", pin_level=6,
            system_type=SystemType.WENZHI,
            domain=domain, suitable_schools=schools,
        )

    # ── 礼部（记忆层）──
    # 伯爵·礼部尚书
    positions.append(_p(
        id="WZ_LL_BJ", name="礼部尚书·伯爵", department="礼部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.WENZHI,
        domain="记忆系统/学习系统/文学/科举2.0",
        dispatch_path="皇帝→内阁→礼部尚书→NeuralMemorySystem/LearningCoordinator",
        suitable_schools=["儒家", "道家", "佛家", "文学家"],
        description="礼部尚书，伯爵品位，统领记忆层，由班固担任",
        sage_type=SageType.THEORIST,
    ))

    # 礼部管理层
    libu_li_si = [
        ("仪制司·记忆引擎", "记忆存储引擎", ["佛家", "道家", "科学家"]),
        ("仪制司·知识引擎", "知识检索引擎", ["儒家", "科学家", "哲学家"]),
        ("仪制司·推理引擎", "推理引擎", ["儒家", "顶级思维法", "科学家"]),
        ("仪制司·学习引擎", "学习引擎", ["增长思维", "教育家", "科学家"]),
        ("仪制司·验证引擎", "输出验证引擎", ["法家", "科学家", "顶级思维法"]),
        ("祠祭司·智能学习", "智能学习引擎", ["教育家", "增长思维", "科学家"]),
        ("祠祭司·科举考核", "智慧资质考核", ["儒家", "教育家", "法家"]),
        ("祠祭司·科举晋升", "克隆晋升评估", ["儒家", "法家", "企业家"]),
    ]
    for i, (si_name, domain, schools) in enumerate(libu_li_si, 1):
        positions += _zheng_cong_pair(
            f"WZ_LL_4_{i:02d}", f"礼部{si_name}", "礼部", pin_level=4,
            system_type=SystemType.WENZHI,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→内阁→礼部→{si_name}",
            suitable_schools=schools,
            description_prefix=f"礼部{si_name}，负责{domain}",
        )

    for i, (name, domain, schools) in enumerate([
        ("记忆管理主事", "记忆日常管理", ["佛家", "道家"]),
        ("学习管理主事", "学习进程管理", ["教育家", "增长思维"]),
        ("科举管理主事", "科举考试管理", ["儒家", "法家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"WZ_LL_6_{i:02d}", f"礼部·{name}", "礼部", pin_level=6,
            system_type=SystemType.WENZHI,
            domain=domain, suitable_schools=schools,
        )

    # ── 文治系统专员 ──
    positions += _specialist_batch("WZ_P7", "文治系统", PinRank.ZHENG_7PIN, items=[
        ("学派专员", "学派具体事务", ["儒家", "道家", "佛家", "法家", "墨家", "兵家"]),
        ("评级专员", "能力评级辅助", ["科学家", "社会学家", "心理学家"]),
        ("调度专员", "智慧调度执行", ["兵家", "纵横家", "法家"]),
        ("文学专员", "文学相关事务", ["文学家", "神话", "文学叙事"]),
        ("儒学专员", "儒学研究与应用", ["儒家"]),
        ("道学专员", "道学研究与应用", ["道家"]),
        ("佛学专员", "佛学研究与应用", ["佛家"]),
        ("史学专员", "历史研究与借鉴", ["史家", "儒家"]),
        ("哲学专员", "哲学思辨应用", ["哲学家", "思想家"]),
        ("艺术专员", "艺术鉴赏与创作", ["艺术家"]),
        ("教育专员", "教育方法研究", ["教育家", "儒家"]),
        ("记忆专员", "记忆系统维护", ["科学家", "佛家", "道家"]),
        ("茶道专员", "茶文化与品质", ["茶道家"]),
        ("名家专员", "名家逻辑研究", ["名家"]),
        ("杂家专员", "杂家综合研究", ["杂家"]),
        ("阴阳专员", "阴阳家象数研究", ["阴阳家"]),
        ("纵横专员", "纵横家策略研究", ["纵横家"]),
        ("农家专员", "农家技术实践", ["农家"]),
        ("逻辑专员", "逻辑学与辩证法", ["名家", "哲学家"]),
        ("批评专员", "文学批评研究", ["文学批评家"]),
    ])

    return positions


def _build_economy_positions() -> List[Position]:
    """
    经济系统岗位（户部）—— v3.1实战派重镇

    规则：最高决策人3人（1正一品 + 2从一品），实战派>=2人
    v3.1变更：
      - 户部尚书→伯爵·管仲（实战派晋升）
      - 新增盐铁司（产业政策与市场调控）
      - 新增数字市易司·伯爵·郦道元（实战派）
      - 新增货币与金融·伯爵·格雷厄姆（实战派）
    """
    positions = []

    # ── 户部最高决策层（3人共议）──
    positions.append(_p(
        id="JJ_HB_Z1", name="户部尚书（正一品）", department="户部",
        pin=PinRank.ZHENG_1PIN, position_type=PositionType.SUPREME_TRIPLE,
        capacity=1, is_zheng=True,
        system_type=SystemType.ECONOMY,
        domain="经济数据与产业政策总管",
        dispatch_path="皇帝→内阁→户部尚书→DataCollector/WebSearchEngine",
        suitable_schools=["经济学家", "社会学家", "科学家", "法家"],
        description="经济系统最高决策人（正品），掌管钱粮数据与产业政策",
        practitioner_quota=2,
    ))
    positions.append(_p(
        id="JJ_HB_C1A", name="户部侍郎甲（从一品）", department="户部",
        pin=PinRank.CONG_1PIN, position_type=PositionType.SUPREME_TRIPLE,
        capacity=1, is_zheng=False,
        system_type=SystemType.ECONOMY,
        domain="全网数据采集与清洗",
        dispatch_path="皇帝→内阁→户部→侍郎甲→数据采集",
        suitable_schools=["科学家", "经济学家", "数学"],
        description="经济系统决策副（从品甲），负责数据采集",
    ))
    positions.append(_p(
        id="JJ_HB_C1B", name="户部侍郎乙（从一品）", department="户部",
        pin=PinRank.CONG_1PIN, position_type=PositionType.SUPREME_TRIPLE,
        capacity=1, is_zheng=False,
        system_type=SystemType.ECONOMY,
        domain="知识图谱与行业知识",
        dispatch_path="皇帝→内阁→户部→侍郎乙→知识图谱",
        suitable_schools=["科学家", "哲学家", "企业家"],
        description="经济系统决策副（从品乙），负责知识图谱",
    ))

    # ── 户部尚书·伯爵（v3.1: 管仲·实战派晋升）──
    positions.append(_p(
        id="JJ_HB_BJ", name="户部尚书·伯爵", department="户部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ECONOMY,
        domain="经济数据与产业政策总管",
        dispatch_path="皇帝→内阁→户部尚书·伯爵→管仲",
        suitable_schools=["经济学家", "法家", "政治家"],
        description="户部尚书·伯爵，v3.1由管仲担任（实战派），春秋第一相，九合诸侯一匡天下",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 数字市易司·伯爵（v3.1新增: 郦道元·实战派）──
    positions.append(_p(
        id="JJ_SY_BJ", name="数字市易司·伯爵", department="户部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ECONOMY,
        domain="数字市易与数据市场总管",
        dispatch_path="皇帝→内阁→户部→数字市易司·伯爵→郦道元",
        suitable_schools=["科学家", "地理学家", "法家"],
        description="数字市易司·伯爵，v3.1由郦道元担任（实战派），著《水经注》，实地考察经验丰富",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 货币与金融·伯爵（v3.1新增: 格雷厄姆·实战派）──
    positions.append(_p(
        id="JJ_HB_BJ2", name="货币与金融·伯爵", department="户部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ECONOMY,
        domain="货币金融与价值评估总管",
        dispatch_path="皇帝→内阁→户部→货币与金融·伯爵→格雷厄姆",
        suitable_schools=["投资家", "经济学家", "科学家"],
        description="货币与金融·伯爵，v3.1由格雷厄姆担任（实战派），价值投资之父，巴菲特之师",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 户部管理层（v3.1新增盐铁司）──
    hubu_si = [
        ("本司·网络搜索", "全网信息搜索采集", ["科学家", "经济学家", "社会学家"]),
        ("本司·数据采集", "数据采集与清洗", ["科学家", "数学"]),
        ("户籍司·知识图谱", "知识图谱构建", ["科学家", "哲学家"]),
        ("户籍司·概念管理", "概念库管理", ["哲学家", "名家"]),
        ("户籍司·规则引擎", "推理规则管理", ["法家", "科学家"]),
        ("户籍司·行业知识", "行业知识库维护", ["经济学家", "社会学家", "企业家"]),
        ("仓场司·行业适配", "行业引擎适配", ["企业家", "经济学家", "增长思维"]),
        ("仓场司·行业识别", "行业自动识别", ["科学家", "经济学家"]),
        ("数字市易司·实时监控", "数据质量实时监控", ["科学家", "数学"]),
        ("数字市易司·市场动态", "市场动态追踪", ["经济学家", "投资家", "企业家"]),
        ("盐铁司·产业政策", "产业政策与市场调控", ["法家", "经济学家", "政治家"]),
        ("盐铁司·资源分配", "战略资源分配与调度", ["经济学家", "科学家", "投资家"]),
    ]
    for i, (si_name, domain, schools) in enumerate(hubu_si, 1):
        positions += _zheng_cong_pair(
            f"JJ_HB_4_{i:02d}", f"户部{si_name}", "户部", pin_level=4,
            system_type=SystemType.ECONOMY,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→内阁→户部→{si_name}",
            suitable_schools=schools,
            description_prefix=f"户部{si_name}，负责{domain}",
        )

    for i, (name, domain, schools) in enumerate([
        ("数据管理主事", "数据日常管理", ["科学家", "经济学家"]),
        ("行业管理主事", "行业分析管理", ["企业家", "社会学家"]),
        ("市场监控主事", "市场情报管理", ["经济学家", "投资家", "增长思维"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"JJ_HB_6_{i:02d}", f"户部·{name}", "户部", pin_level=6,
            system_type=SystemType.ECONOMY,
            domain=domain, suitable_schools=schools,
        )

    # ── 专员（v3.1细化分工）──
    positions += _specialist_batch("JJ_P7", "户部", PinRank.ZHENG_7PIN, items=[
        ("数据采集专员", "数据采集与清洗执行", ["科学家", "数学"]),
        ("数据处理专员", "数据格式化与质量控制", ["科学家", "数学"]),
        ("行业分析专员", "行业趋势研究与报告", ["经济学家", "社会学家", "企业家"]),
        ("市场情报专员", "市场动态与竞品监控", ["经济学家", "投资家", "增长思维"]),
        ("产业政策专员", "产业政策分析与建议", ["法家", "经济学家", "政治家"]),
        ("资源调度专员", "战略资源分配辅助", ["经济学家", "科学家", "投资家"]),
        ("金融分析专员", "货币与金融分析", ["投资家", "经济学家"]),
        ("质量监控专员", "数据质量实时监控", ["科学家", "数学"]),
    ])

    return positions


def _build_military_positions() -> List[Position]:
    """
    军政系统岗位（兵部+五军都督府+厂卫）

    规则：最高决策人1人（王爵或公爵）
    """
    positions = []

    # ── 兵部最高决策层（1人，公爵）──
    positions.append(_p(
        id="JU_BB_GJ", name="兵部尚书·公爵", department="兵部",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.GONGJUE,
        position_type=PositionType.SUPREME_SINGLE, capacity=1,
        system_type=SystemType.MILITARY,
        domain="主线调度/神经网络布局/驿道云",
        dispatch_path="皇帝→兵部尚书·公爵→MainChain/NeuralLayout",
        suitable_schools=["兵家", "道家", "法家"],
        description="军政系统最高决策人，公爵，统领调度层与神经网络，由老子担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 兵部侯爵 ──
    positions.append(_p(
        id="JU_BB_HJ", name="兵部侍郎·侯爵", department="兵部",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.HOUJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.MILITARY,
        domain="军事战略副决策",
        dispatch_path="皇帝→兵部→侍郎·侯爵",
        suitable_schools=["兵家", "道家", "法家"],
        description="兵部侍郎，侯爵品位，军事战略副决策，由庄子担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 兵部伯爵 ──
    positions.append(_p(
        id="JU_BB_BJ", name="兵部郎中·伯爵", department="兵部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.MILITARY,
        domain="军令调度执行总管",
        dispatch_path="皇帝→兵部→郎中·伯爵",
        suitable_schools=["兵家", "法家", "纵横家"],
        description="兵部郎中，伯爵品位，军令调度执行总管，由孙武担任",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 兵部管理层 ──
    bingbu_si = [
        ("武选司·主线调度", "主链路调度控制", ["兵家", "法家"]),
        ("武选司·子系统调度", "子系统协同调度", ["兵家", "道家"]),
        ("武库司·神经网络", "神经网络布局", ["科学家", "道家"]),
        ("武库司·信号传递", "神经信号传递优化", ["科学家", "兵家"]),
        ("职方司·问题路由", "ProblemType路由", ["兵家", "法家", "纵横家"]),
        ("职方司·学派调度", "WisdomSchool调度", ["儒家", "兵家"]),
    ]
    for i, (si_name, domain, schools) in enumerate(bingbu_si, 1):
        positions += _zheng_cong_pair(
            f"JU_BB_4_{i:02d}", f"兵部{si_name}", "兵部", pin_level=4,
            system_type=SystemType.MILITARY,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→兵部→{si_name}",
            suitable_schools=schools,
            description_prefix=f"兵部{si_name}，负责{domain}",
        )

    for i, (name, domain, schools) in enumerate([
        ("军事调度主事", "军事问题调度", ["兵家"]),
        ("危机调度主事", "危机应对调度", ["兵家", "道家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"JU_BB_6_{i:02d}", f"兵部·{name}", "兵部", pin_level=6,
            system_type=SystemType.MILITARY,
            domain=domain, suitable_schools=schools,
        )

    # ── 五军都督府 ──
    # 伯爵·大都督
    positions.append(_p(
        id="JU_WJ_BJ", name="大都督·伯爵", department="五军都督府",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.MILITARY,
        domain="神经网络总布局/57神经元/74突触",
        dispatch_path="皇帝→五军都督府→大都督·伯爵→NeuralLayout",
        suitable_schools=["科学家", "道家", "哲学家"],
        description="五军都督府大都督，伯爵品位，掌管神经网络全局布局，由列子担任",
        sage_type=SageType.THEORIST,
    ))

    for i, (name, domain, schools) in enumerate([
        ("编排桥接使", "orchestrator_bridge信号桥接", ["科学家", "数学"]),
        ("自治反馈使", "autonomy_feedback_fusion反馈融合", ["科学家", "心理学家"]),
        ("学派执行使", "school_execution_optimizer学派优化", ["科学家", "顶级思维法"]),
        ("跨模块洞察使", "cross_module_insight_generator跨模块洞察", ["哲学家", "科学家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"JU_WJ_4_{i:02d}", f"五军都督府·{name}", "五军都督府", pin_level=4,
            system_type=SystemType.MILITARY,
            domain=domain,
            dispatch_path_prefix=f"皇帝→五军都督府→{name}",
            suitable_schools=schools,
        )

    # ── 厂卫（锦衣卫）──
    # 架构：指挥使(正三品·伯爵) + 同知(从三品)
    #       → 四司司官(正从四品) → 百户(正从五品) → 总旗(正从六品)
    #       → 小旗领班(正七品) → 力士(从七品~正九品)
    # 四司：监控司 / 暗察司 / 合规司 / 效能司
    #
    # 职责全覆盖：
    #   监控司：系统运行监控 + 性能瓶颈分析
    #   暗察司：异常行为检测 + 安全日志审计
    #   合规司：全局合规检举 + 合法性审查
    #   效能司：行政之鞭执行 + 大秦指标效能扫描 + 效能档案管理

    # ── 指挥使（正三品·伯爵）──
    positions.append(_p(
        id="JU_CW_BJ", name="锦衣卫指挥使·伯爵", department="厂卫",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.MILITARY,
        domain="锦衣卫全盘指挥/系统监控/性能优化/异常检测/合规检举/合法性督促/效能驱动",
        dispatch_path="皇帝→厂卫→指挥使·伯爵→四司",
        suitable_schools=["兵家", "法家", "纵横家"],
        description="锦衣卫指挥使，伯爵品位，直通皇帝。统领监控/暗察/合规/效能四司，负责全局监控、合规检举、效能驱动，由秦始皇担任",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 同知（从三品·副指挥使）──
    positions.append(_p(
        id="JU_CW_TZ", name="锦衣卫同知", department="厂卫",
        pin=PinRank.CONG_3PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.MILITARY,
        domain="锦衣卫副指挥/四司协调/情报汇总/异常上报/指挥使缺位时代理",
        dispatch_path="皇帝→厂卫→同知→四司",
        suitable_schools=["法家", "兵家", "纵横家"],
        description="锦衣卫同知，从三品，副指挥使。协助指挥使统筹四司日常运作，负责情报汇总与异常上报，指挥使缺位时代行指挥权",
        sage_type=SageType.DUAL_TYPE,
    ))

    # ── 锦衣卫四司（正从四品）──
    changwei_si = [
        ("监控司·系统监控", "全系统运行监控", ["科学家", "数学"]),
        ("监控司·性能优化", "性能分析与优化", ["科学家", "数学", "墨家"]),
        ("暗察司·异常检测", "异常行为检测", ["法家", "兵家", "纵横家"]),
        ("暗察司·安全审计", "安全日志审计", ["法家", "科学家"]),
        ("合规司·检举督察", "检举全局违规行为，督促各部门合规合法", ["法家", "纵横家", "兵家"]),
        ("合规司·合法性审查", "审查系统操作合法性，确保执行流程合规", ["法家", "政治家"]),
        ("合规司·制度审查", "审查制度文档合规性，确保制度之间无冲突", ["法家", "儒家", "纵横家"]),
        # 效能司（行政之鞭+大秦指标执行机构）
        ("效能司·行政之鞭", "执行行政之鞭机制，效能扫描与双向鞭策令生成执行", ["法家", "兵家", "纵横家"]),
        ("效能司·指标采集", "大秦指标数据采集、汇总与效能评估", ["科学家", "法家", "数学"]),
        ("效能司·效能档案", "管理效能档案，考核数据归档与趋势分析", ["科学家", "法家", "数学"]),
    ]
    for i, (si_name, domain, schools) in enumerate(changwei_si, 1):
        positions += _zheng_cong_pair(
            f"JU_CW_4_{i:02d}", f"锦衣卫{si_name}", "厂卫", pin_level=4,
            system_type=SystemType.MILITARY,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→厂卫→{si_name}",
            suitable_schools=schools,
        )

    # ── v1.0.0 锦衣卫百户（正从五品）——各司执行主管 ──
    changwei_baihu = [
        ("监控百户", "监控司执行主管，统筹系统监控与性能优化执行", "监控司", ["科学家", "数学", "墨家"]),
        ("暗察百户", "暗察司执行主管，统筹异常检测与安全审计执行", "暗察司", ["法家", "兵家", "纵横家"]),
        ("合规百户", "合规司执行主管，统筹检举督察/合法性审查/制度审查执行", "合规司", ["法家", "政治家", "纵横家"]),
        ("效能百户", "效能司执行主管，统筹行政之鞭/指标采集/效能档案管理", "效能司", ["法家", "兵家", "科学家"]),
    ]
    for i, (name, domain, si_name, schools) in enumerate(changwei_baihu, 1):
        positions += _zheng_cong_pair(
            f"JU_CW_5_{i:02d}", f"锦衣卫{name}", "厂卫", pin_level=5,
            system_type=SystemType.MILITARY,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→厂卫→{si_name}",
            suitable_schools=schools,
        )

    # ── v1.0.0 锦衣卫总旗（正从六品）——各百户下辖执行组长 ──
    changwei_zongqi = [
        ("监控总旗·系统", "系统监控执行组长，带领力士执行全系统运行监控", "监控司", ["科学家", "数学"]),
        ("监控总旗·性能", "性能优化执行组长，带领力士执行性能分析与优化", "监控司", ["科学家", "数学", "墨家"]),
        ("暗察总旗·异常", "异常检测执行组长，带领力士执行异常行为检测与报告", "暗察司", ["法家", "兵家", "纵横家"]),
        ("暗察总旗·安全", "安全审计执行组长，带领力士执行安全日志审计", "暗察司", ["法家", "科学家"]),
        ("合规总旗·检举", "检举督察执行组长，带领力士执行全局违规检举", "合规司", ["法家", "纵横家", "兵家"]),
        ("合规总旗·审查", "合法性审查执行组长，带领力士执行操作合法性审查", "合规司", ["法家", "政治家"]),
        ("合规总旗·制度", "制度审查执行组长，带领力士执行制度文档合规审查", "合规司", ["法家", "儒家"]),
        ("效能总旗·鞭策", "行政之鞭执行组长，带领力士执行双向鞭策令", "效能司", ["法家", "兵家", "纵横家"]),
        ("效能总旗·指标", "大秦指标采集组长，带领力士执行指标数据采集与汇总", "效能司", ["科学家", "数学"]),
        ("效能总旗·档案", "效能档案执行组长，带领力士执行考核数据归档", "效能司", ["科学家", "法家", "数学"]),
    ]
    for i, (name, domain, si_name, schools) in enumerate(changwei_zongqi, 1):
        positions += _zheng_cong_pair(
            f"JU_CW_6_{i:02d}", f"锦衣卫{name}", "厂卫", pin_level=6,
            system_type=SystemType.MILITARY,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→厂卫→{si_name}",
            suitable_schools=schools,
        )

    # ── v1.0.0 锦衣卫小旗（正七品领班）——各总旗下辖执行领班 ──
    changwei_xiaoqi = [
        ("小旗·系统监控", "系统监控力士领班，管理监控力士日常巡检", "监控司", ["科学家", "数学"]),
        ("小旗·性能优化", "性能优化力士领班，管理优化力士日常执行", "监控司", ["科学家", "数学", "墨家"]),
        ("小旗·异常检测", "异常检测力士领班，管理暗探力士日常巡查", "暗察司", ["法家", "兵家", "纵横家"]),
        ("小旗·安全审计", "安全审计力士领班，管理审计力士日常检查", "暗察司", ["法家", "科学家"]),
        ("小旗·检举督察", "检举督察力士领班，管理合规力士日常检举", "合规司", ["法家", "纵横家", "兵家"]),
        ("小旗·合法性审查", "合法性审查力士领班，管理审查力士日常核查", "合规司", ["法家", "政治家"]),
        ("小旗·制度审查", "制度审查力士领班，管理制度审查力士日常执行", "合规司", ["法家", "儒家"]),
        ("小旗·行政之鞭", "行政之鞭力士领班，管理鞭策力士日常执行", "效能司", ["法家", "兵家", "纵横家"]),
        ("小旗·指标采集", "指标采集力士领班，管理采集力士日常数据收集", "效能司", ["科学家", "数学"]),
        ("小旗·效能档案", "效能档案力士领班，管理档案力士日常记录", "效能司", ["科学家", "法家", "数学"]),
    ]
    for i, (name, domain, si_name, schools) in enumerate(changwei_xiaoqi, 1):
        positions.append(_p(
            id=f"JU_CW_XQ_{i:02d}", name=f"锦衣卫{name}",
            department="厂卫",
            pin=PinRank.ZHENG_7PIN,
            position_type=PositionType.TEAM_LEADER,
            capacity=1, is_zheng=True,
            system_type=SystemType.MILITARY,
            domain=domain, si_name=si_name,
            dispatch_path=f"皇帝→厂卫→{si_name}→力士团队",
            suitable_schools=schools,
            description=f"锦衣卫{name}领班，{domain}",
        ))



    # ── 军政系统专员（v1.0.0：锦衣卫专员已独立为JU_CW_L7系列）──
    # 注：原"暗探情报专员""性能监控专员"已归属锦衣卫力士序列
    positions += _specialist_batch("JU_P7", "军政系统", PinRank.ZHENG_7PIN, items=[
        ("兵法研究专员", "兵法策略研究与兵书整理", ["兵家"]),
        ("调度执行专员", "调度执行与指令传达", ["兵家", "法家", "纵横家"]),
        ("神经布局专员", "神经网络节点维护", ["科学家", "数学"]),
        ("神经元维护专员", "神经元与突触连接维护", ["科学家", "数学", "哲学家"]),
        ("军事情报专员", "敌情分析与战略侦察", ["兵家", "纵横家"]),
        ("信号优化专员", "神经信号传递效率优化", ["科学家", "数学", "兵家"]),
        ("军事工程专员", "军事工程与防御体系维护", ["墨家", "科学家", "兵家"]),
        ("战略规划专员", "军事战略规划与兵棋推演", ["兵家", "纵横家", "法家"]),
    ])

    return positions


def _build_standard_positions() -> List[Position]:
    """
    其他系统岗位（刑部/工部/三法司）

    规则：最高决策人2人（1正二品 + 1从二品）
    - 以下：一正一副双岗制到六品
    - 七品~九品专员
    """
    positions = []

    # ════ 刑部 ════
    # 正二品+从二品决策层
    positions += _zheng_cong_pair(
        "TD_XB_2_01", "刑部尚书", "刑部", pin_level=2,
        system_type=SystemType.STANDARD,
        domain="风控/安全合规/内容审核/经济防控",
        dispatch_path_prefix="皇帝→内阁→刑部尚书→RiskController/DefenseDepth",
        suitable_schools=["法家", "儒家", "兵家"],
        description_prefix="监察层最高长官，掌管刑罚与律法",
    )

    # 伯爵·刑部侍郎
    positions.append(_p(
        id="TD_XB_BJ", name="刑部侍郎·伯爵", department="刑部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.STANDARD,
        domain="刑罚执行总管",
        dispatch_path="皇帝→内阁→刑部→侍郎·伯爵",
        suitable_schools=["法家", "兵家", "素书"],
        description="刑部侍郎，伯爵品位，刑罚执行总管，由孙膑担任",
        sage_type=SageType.PRACTITIONER,
    ))

    xingbu_si = [
        ("刑部·风险总控", "全局风险控制", ["法家", "兵家", "素书"]),
        ("刑部·情绪分析", "情绪健康分析", ["心理学家", "佛家"]),
        ("刑部·合规检查", "合规性审查", ["法家", "儒家"]),
        ("刑部·内容审核", "输出内容审核", ["法家", "儒家"]),
        ("安全·数据混淆", "数据脱敏混淆", ["科学家", "数学"]),
        ("安全·纵深防御", "安全纵深防御", ["法家", "兵家"]),
        ("防控·通胀预警", "模型通胀预警", ["经济学家", "投资家", "科学家"]),
        ("防控·质量调控", "输出质量调控", ["科学家", "社会学家"]),
    ]
    for i, (si_name, domain, schools) in enumerate(xingbu_si, 1):
        positions += _zheng_cong_pair(
            f"TD_XB_4_{i:02d}", f"刑部{si_name}", "刑部", pin_level=4,
            system_type=SystemType.STANDARD,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→内阁→刑部→{si_name}",
            suitable_schools=schools,
        )

    # ════ 工部 ════
    positions += _zheng_cong_pair(
        "TD_GB_2_01", "工部尚书", "工部", pin_level=2,
        system_type=SystemType.STANDARD,
        domain="核心执行/增长引擎/工具链/专利",
        dispatch_path_prefix="皇帝→内阁→工部尚书→SomnCore/AgentCore",
        suitable_schools=["企业家", "墨家", "科学家", "投资家"],
        description_prefix="执行层最高长官，掌管工程与营造",
    )

    positions.append(_p(
        id="TD_GB_BJ", name="工部侍郎·伯爵", department="工部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.STANDARD,
        si_name="德鲁克（Peter Drucker）",
        domain="工程执行总管",
        dispatch_path="皇帝→内阁→工部→侍郎·伯爵",
        suitable_schools=["企业家", "墨家", "科学家"],
        description="工部侍郎，伯爵品位，工程执行总管，V1.0由德鲁克担任（西方贤者·复合型），现代管理学之父，目标管理(MBO)创始人",
        sage_type=SageType.DUAL_TYPE,
    ))

    gongbu_si = [
        ("营缮司·核心总管", "AgentCore核心管理", ["企业家", "法家", "兵家"]),
        ("营缮司·执行总司", "SomnCore执行管理", ["企业家", "墨家", "科学家"]),
        ("营缮司·混合路由", "混合路由引擎", ["科学家", "数学"]),
        ("营缮司·检索增强", "RAG检索增强", ["科学家", "哲学家"]),
        ("屯田司·增长策略", "增长策略引擎", ["企业家", "投资家", "经济学家"]),
        ("屯田司·需求分析", "需求分析引擎", ["社会学家", "经济学家", "中国消费文化"]),
        ("屯田司·漏斗优化", "用户漏斗优化", ["科学家", "心理学家", "企业家"]),
        ("屯田司·方案评估", "方案评估框架", ["法家", "科学家", "企业家"]),
        ("水部司·LLM服务", "大语言模型服务", ["科学家", "数学"]),
        ("水部司·工具注册", "工具注册管理", ["科学家", "墨家"]),
        ("虞衡司·目标系统", "自主目标系统", ["企业家", "儒家"]),
        ("虞衡司·自主调度", "自主调度引擎", ["企业家", "兵家", "科学家"]),
        ("虞衡司·反思引擎", "自我反思引擎", ["哲学家", "顶级思维法", "王阳明"]),
        ("专利司·模板注册", "方案模板注册", ["法家", "企业家"]),
        ("专利司·创新奖励", "创新奖励追踪", ["企业家", "投资家", "经济学家"]),
    ]
    for i, (si_name, domain, schools) in enumerate(gongbu_si, 1):
        positions += _zheng_cong_pair(
            f"TD_GB_4_{i:02d}", f"工部{si_name}", "工部", pin_level=4,
            system_type=SystemType.STANDARD,
            domain=domain, si_name=si_name,
            dispatch_path_prefix=f"皇帝→内阁→工部→{si_name}",
            suitable_schools=schools,
        )

    for i, (name, domain, schools) in enumerate([
        ("执行管理主事", "核心执行管理", ["企业家", "墨家"]),
        ("增长管理主事", "增长引擎管理", ["企业家", "投资家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"TD_GB_6_{i:02d}", f"工部·{name}", "工部", pin_level=6,
            system_type=SystemType.STANDARD,
            domain=domain, suitable_schools=schools,
        )

    # ════ 三法司 ════
    positions += _zheng_cong_pair(
        "TD_SF_2_01", "都察院·左都御史", "三法司", pin_level=2,
        system_type=SystemType.STANDARD,
        domain="反馈管道监控/用户反馈分析",
        dispatch_path_prefix="皇帝→三法司→都察院→FeedbackPipeline",
        suitable_schools=["儒家", "法家", "社会学家"],
        description_prefix="都察院最高长官，反馈收集与处理",
    )

    # ── 都察院·伯爵（v3.1新增: 诸葛亮·复合型晋升）──
    positions.append(_p(
        id="TD_DC_BJ", name="都察院·伯爵", department="三法司",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.STANDARD,
        domain="反馈监察总管",
        dispatch_path="皇帝→三法司→都察院·伯爵→诸葛亮",
        suitable_schools=["政治家", "兵家", "法家", "儒家"],
        description="都察院·伯爵，v3.1由诸葛亮担任（复合型），鞠躬尽瘁、六出祁山、治理蜀国",
        sage_type=SageType.DUAL_TYPE,
    ))

    # ── 增长引擎·伯爵（v3.1新增: 商鞅·实战派）──
    positions.append(_p(
        id="TD_ZZ_BJ", name="增长引擎·伯爵", department="工部",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.STANDARD,
        domain="增长策略与产业执行总管",
        dispatch_path="皇帝→内阁→工部→增长引擎·伯爵→商鞅",
        suitable_schools=["法家", "政治家", "经济学家"],
        description="增长引擎·伯爵，v3.1由商鞅担任（实战派），商鞅变法、秦国强大、统一六国基础",
        sage_type=SageType.PRACTITIONER,
    ))

    positions += _zheng_cong_pair(
        "TD_SF_2_02", "大理寺·卿", "三法司", pin_level=2,
        system_type=SystemType.STANDARD,
        domain="结果验证/逻辑审计",
        dispatch_path_prefix="皇帝→三法司→大理寺→ValidationEngine",
        suitable_schools=["法家", "科学家", "顶级思维法"],
        description_prefix="大理寺最高长官，输出验证与审计",
    )

    positions += _zheng_cong_pair(
        "TD_SF_3_01", "三法司·ROI御史", "三法司", pin_level=3,
        system_type=SystemType.STANDARD,
        domain="ROI追踪/效果评估",
        dispatch_path_prefix="皇帝→三法司→ROITracker",
        suitable_schools=["投资家", "经济学家", "科学家"],
        description_prefix="ROI御史，效果追踪",
    )

    # ── 其他系统专员 ──
    positions += _specialist_batch("TD_P7", "标准系统", PinRank.ZHENG_7PIN, items=[
        ("风控专员", "风险监控执行", ["法家", "兵家", "素书"]),
        ("安全专员", "安全防护执行", ["法家", "科学家"]),
        ("合规专员", "合规检查执行", ["法家", "儒家"]),
        ("工程专员", "核心工程执行", ["墨家", "科学家", "数学"]),
        ("增长专员", "增长策略执行", ["企业家", "投资家", "经济学家", "增长思维"]),
        ("工具专员", "工具链维护", ["科学家", "墨家"]),
        ("产业专员", "产业适配研究", ["企业家", "经济学家", "社会学家"]),
        ("反馈专员", "反馈收集与处理", ["社会学家", "心理学家", "经济学家"]),
        ("验证专员", "结果验证执行", ["科学家", "法家", "顶级思维法"]),
        ("政治研究专员", "政治学研究", ["政治家", "法家"]),
        ("心理专员", "心理学应用", ["心理学家"]),
        ("治理专员", "治理战略研究", ["治理战略家"]),
        ("经济研究专员", "经济学研究", ["经济学家"]),
        ("医理专员", "医学理论研究", ["医家"]),
        ("社会研究专员", "社会学研究", ["社会学家"]),
        ("创新研究专员", "创新实验研究", ["企业家", "科学家"]),
        ("文化研究专员", "文化传播研究", ["文学家", "人类学", "思想家"]),
    ])

    return positions


def _build_chuangxin_positions() -> List[Position]:
    """
    创新系统岗位（皇家科学院/经济战略司/文化输出局）—— v3.1实战派重镇

    规则：双人决策制（1正二品 + 1从二品），实战派>=2人
    v3.1变更：
      - 皇家科学院掌院→伯爵·张衡（实战派晋升）
      - 经济战略司·伯爵→桑弘羊（实战派晋升）
      - 新增农学与工程·伯爵·沈括（实战派）
      - system_type改为INNOVATION
    """
    positions = []

    # ── 创新系统决策层（正二+从二）──
    positions.append(_p(
        id="CX_2_01_Z", name="皇家科学院·掌院（正二品）", department="内阁",
        pin=PinRank.ZHENG_2PIN, position_type=PositionType.SUPREME_DUAL,
        capacity=1, is_zheng=True,
        system_type=SystemType.INNOVATION,
        domain="基础/应用/转化研究总管",
        track="chuangxin",
        dispatch_path="皇帝→内阁→创新系统→皇家科学院掌院",
        suitable_schools=["科学家", "哲学家", "道家"],
        description="皇家科学院最高长官（正品）",
        practitioner_quota=2,
    ))
    positions.append(_p(
        id="CX_2_01_C", name="皇家科学院·掌院（从二品）", department="内阁",
        pin=PinRank.CONG_2PIN, position_type=PositionType.SUPREME_DUAL,
        capacity=1, is_zheng=False,
        system_type=SystemType.INNOVATION,
        domain="基础/应用/转化研究总管",
        track="chuangxin",
        dispatch_path="皇帝→内阁→创新系统→皇家科学院掌院",
        suitable_schools=["科学家", "哲学家", "道家"],
        description="皇家科学院最高长官（从品）",
    ))

    # ── 皇家科学院·伯爵（v3.1: 张衡·实战派晋升）──
    positions.append(_p(
        id="CX_KX_BJ", name="皇家科学院·伯爵", department="内阁",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.INNOVATION,
        domain="科学研究院总管",
        track="chuangxin",
        dispatch_path="皇帝→内阁→创新系统→皇家科学院·伯爵→张衡",
        suitable_schools=["科学家", "天文学家", "数学"],
        description="皇家科学院·伯爵，v3.1由张衡担任（实战派），发明地动仪、浑天仪",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 经济战略司·伯爵（v3.1: 桑弘羊·实战派晋升）──
    positions.append(_p(
        id="CX_HB_BJ", name="经济战略司·伯爵", department="内阁",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.INNOVATION,
        domain="经济战略与市场调控总管",
        track="chuangxin",
        dispatch_path="皇帝→内阁→创新系统→经济战略司·伯爵→桑弘羊",
        suitable_schools=["经济学家", "法家", "政治家"],
        description="经济战略司·伯爵，v3.1由桑弘羊担任（实战派），盐铁专卖、均输平准、统一币制",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 文化输出局·伯爵 ──
    positions.append(_p(
        id="CX_WH_BJ", name="文化输出局·伯爵", department="内阁",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.INNOVATION,
        domain="文化输出与知识推广总管",
        track="chuangxin",
        dispatch_path="皇帝→内阁→创新系统→文化输出局·伯爵",
        suitable_schools=["文学家", "儒家", "思想家"],
        description="文化输出局长，伯爵品位，由枚乘担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 农学与工程·伯爵（v3.1新增: 沈括·实战派）──
    positions.append(_p(
        id="CX_NG_BJ", name="农学与工程·伯爵", department="内阁",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.INNOVATION,
        domain="农学工程与技术转化总管",
        track="chuangxin",
        dispatch_path="皇帝→内阁→创新系统→农学与工程·伯爵→沈括",
        suitable_schools=["科学家", "医家", "天文学家", "数学"],
        description="农学与工程·伯爵，v3.1由沈括担任（实战派），《梦溪笔谈》，博学多才",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 皇家科学院管理层 ──
    kexue_si = [
        ("火器院", "基础科学研究(ML/算法)", ["科学家", "科学思维", "道家"]),
        ("蒸汽机院", "应用技术研究(策略/产业适配)", ["科学家", "儒家", "兵家"]),
        ("农学院", "量产转化(方案评估/学习落地)", ["儒家", "法家", "墨家"]),
    ]
    for i, (si_name, domain, schools) in enumerate(kexue_si, 1):
        positions += _zheng_cong_pair(
            f"CX_KX_4_{i:02d}", f"皇家科学院{si_name}", "内阁",
            pin_level=4,
            system_type=SystemType.INNOVATION,
            domain=domain, si_name=si_name, track="chuangxin",
            dispatch_path_prefix=f"皇帝→内阁→创新系统→皇家科学院→{si_name}",
            suitable_schools=schools,
        )

    # ── 经济战略司管理层 ──
    for i, (si_name, domain, schools) in enumerate([
        ("经济战略司·市场监管", "反垄断/合规审查", ["法家", "经济学家", "社会学家"]),
        ("经济战略司·数据中枢", "全国商业大数据分析", ["科学家", "社会学家", "经济学家"]),
        ("经济战略司·增长策略", "增长策略设计与A/B测试", ["企业家", "投资家", "经济学家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"CX_HB_4_{i:02d}", si_name, "内阁",
            pin_level=4,
            system_type=SystemType.INNOVATION,
            domain=domain, track="chuangxin",
            dispatch_path_prefix=f"皇帝→内阁→创新系统→{si_name}",
            suitable_schools=schools,
        )

    # ── 文化输出局管理层 ──
    for i, (si_name, domain, schools) in enumerate([
        ("文化输出局·文学叙事", "知识输出包装/叙事构建", ["文学家", "神话", "文学叙事"]),
        ("文化输出局·知识推广", "学习推广/知识可视化", ["儒家", "增长思维", "教育家"]),
        ("文化输出局·Cloning推广", "贤者智慧输出/克隆代理服务", ["儒家", "道家", "佛家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"CX_WH_4_{i:02d}", si_name, "内阁",
            pin_level=4,
            system_type=SystemType.INNOVATION,
            domain=domain, track="chuangxin",
            dispatch_path_prefix=f"皇帝→内阁→创新系统→{si_name}",
            suitable_schools=schools,
        )

    # ── 农学与工程管理层（v3.1新增）──
    for i, (si_name, domain, schools) in enumerate([
        ("农学工程·技术转化", "科研成果→技术转化", ["科学家", "墨家", "企业家"]),
        ("农学工程·工程标准", "工程建设标准化", ["科学家", "法家", "墨家"]),
        ("农学工程·农学研究", "农业科学与农技推广", ["科学家", "农家", "医家"]),
    ], 1):
        positions += _zheng_cong_pair(
            f"CX_NG_4_{i:02d}", si_name, "内阁",
            pin_level=4,
            system_type=SystemType.INNOVATION,
            domain=domain, track="chuangxin",
            dispatch_path_prefix=f"皇帝→内阁→创新系统→{si_name}",
            suitable_schools=schools,
        )

    # ── 创新系统专员（v3.1细化分工）──
    positions += _specialist_batch("CX_P7", "创新系统", PinRank.ZHENG_7PIN,
        track="chuangxin",
        items=[
            ("科研专员·算法", "算法设计与优化", ["科学家", "数学"]),
            ("科研专员·模型", "ML模型训练与评估", ["科学家", "科学思维"]),
            ("科研专员·策略", "策略方案设计", ["企业家", "投资家", "经济学家"]),
            ("推广专员·教育", "知识推广与教育", ["儒家", "教育家"]),
            ("推广专员·文化", "文化传播与交流", ["文学家", "人类学", "思想家"]),
            ("推广专员·文学", "文学创作与编辑", ["文学家", "文学叙事"]),
            ("研究专员·综合", "综合研究", ["思想家", "哲学家"]),
            ("研究专员·历史", "历史研究辅助", ["史家"]),
            ("研究专员·思想", "思想综合研究", ["思想家", "哲学家"]),
            ("工程专员·转化", "技术转化执行", ["科学家", "墨家", "企业家"]),
            ("农学专员·种植", "农业技术研究", ["科学家", "农家", "医家"]),
            ("农学专员·水利", "水利工程研究", ["科学家", "数学"]),
        ],
    )

    return positions


# ═══════════════════════════════════════════════════════════════════════════════


def _build_review_positions() -> List[Position]:
    """
    审核系统岗位（翰林院）—— v3.2新增

    翰林院独立于六部之外，不参与决策生成，只参与决策审核。
    审核流程：逻辑论证检测 -> 多视角反驳 -> 综合评审

    人员配置：
      掌院: 韩非子（正三品）——逻辑论证总管
      学士甲: 墨子（正四品）——经济可行性
      学士乙: 慎到（正四品）——社会稳定
      学士丙: 荀子（正四品）——心理学
      学士丁: 邹衍（正四品）——伦理合规
      侍读甲: 公孙龙（从四品）——形式逻辑
      侍读乙: 惠施（从四品）——非形式谬误
    """
    positions = []

    # -- 翰林院掌院（正三品）韩非子 --
    positions.append(_p(
        id="HL_ZY", name="翰林院掌院", department="翰林院",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.AUDIT, capacity=1,
        system_type=SystemType.REVIEW,
        si_name="韩非子",
        dispatch_path="翰林院掌院->韩非子",
        suitable_schools=["法家", "名家", "顶级思维法"],
        description="翰林院掌院，韩非子担任，刑名之学精确推演，逻辑论证总管",
        sage_type=SageType.DUAL_TYPE,
    ))

    # -- 翰林院学士甲（正四品）墨子 --
    positions.append(_p(
        id="HL_XS_A", name="翰林院学士甲", department="翰林院",
        pin=PinRank.ZHENG_4PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.AUDIT, capacity=1,
        system_type=SystemType.REVIEW,
        si_name="墨子",
        dispatch_path="翰林院掌院->学士甲->墨子",
        suitable_schools=["墨家", "经济学家", "投资家"],
        description="翰林院学士甲，墨子担任，经济可行性审核，节用成本效益分析",
        sage_type=SageType.PRACTITIONER,
    ))

    # -- 翰林院学士乙（正四品）慎到 --
    positions.append(_p(
        id="HL_XS_B", name="翰林院学士乙", department="翰林院",
        pin=PinRank.ZHENG_4PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.AUDIT, capacity=1,
        system_type=SystemType.REVIEW,
        si_name="慎到",
        dispatch_path="翰林院掌院->学士乙->慎到",
        suitable_schools=["法家", "社会学家", "政治家"],
        description="翰林院学士乙，慎到担任，社会稳定风险评估，权势衡平",
        sage_type=SageType.THEORIST,
    ))

    # -- 翰林院学士丙（正四品）荀子 --
    positions.append(_p(
        id="HL_XS_C", name="翰林院学士丙", department="翰林院",
        pin=PinRank.ZHENG_4PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.AUDIT, capacity=1,
        system_type=SystemType.REVIEW,
        si_name="荀子",
        dispatch_path="翰林院掌院->学士丙->荀子",
        suitable_schools=["儒家", "心理学家", "行为塑造"],
        description="翰林院学士丙，荀子担任，心理学视角审核，性恶论行为分析",
        sage_type=SageType.THEORIST,
    ))

    # -- 翰林院学士丁（正四品）邹衍 --
    positions.append(_p(
        id="HL_XS_D", name="翰林院学士丁", department="翰林院",
        pin=PinRank.ZHENG_4PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.AUDIT, capacity=1,
        system_type=SystemType.REVIEW,
        si_name="邹衍",
        dispatch_path="翰林院掌院->学士丁->邹衍",
        suitable_schools=["阴阳家", "道家", "儒家"],
        description="翰林院学士丁，邹衍担任，伦理合规审查，五行系统平衡",
        sage_type=SageType.THEORIST,
    ))

    # -- 翰林院侍读甲（从四品）公孙龙 --
    positions.append(_p(
        id="HL_SD_A", name="翰林院侍读甲", department="翰林院",
        pin=PinRank.CONG_4PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.AUDIT, capacity=1,
        system_type=SystemType.REVIEW,
        si_name="公孙龙",
        dispatch_path="翰林院掌院->侍读甲->公孙龙",
        suitable_schools=["名家", "顶级思维法", "科学思维"],
        description="翰林院侍读甲，公孙龙担任，形式逻辑检测，白马非马精确概念分析",
        sage_type=SageType.THEORIST,
    ))

    # -- 翰林院侍读乙（从四品）惠施 --
    positions.append(_p(
        id="HL_SD_B", name="翰林院侍读乙", department="翰林院",
        pin=PinRank.CONG_4PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.AUDIT, capacity=1,
        system_type=SystemType.REVIEW,
        si_name="惠施",
        dispatch_path="翰林院掌院->侍读乙->惠施",
        suitable_schools=["名家", "道家", "顶级思维法"],
        description="翰林院侍读乙，惠施担任，非形式谬误检测，合同异概念辨析",
        sage_type=SageType.THEORIST,
    ))

    return positions


def _build_library_positions() -> List[Position]:
    """
    皇家藏书阁岗位 —— v3.3新增

    皇家藏书阁独立于所有体系之外，王爵扬雄管理。
    所有部门工作结果、人才能力都需汇报藏书阁记录。
    藏书阁自行决策保留有价值、有用的记忆。
    不受任何团队管理。
    """
    positions = []

    # -- 藏书阁大学士（王爵）扬雄 --
    positions.append(_p(
        id="LIB_DXS", name="藏书阁大学士", department="皇家藏书阁",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.WANGJUE,
        position_type=PositionType.SUPREME_SINGLE, capacity=1,
        system_type=SystemType.CANGSHUGE,
        si_name="扬雄",
        dispatch_path="皇帝->藏书阁大学士->扬雄",
        suitable_schools=["历史思想", "史家", "文学家"],
        description="藏书阁大学士，扬雄担任（王爵），独立记忆体系最高长官，记录一切有价值之记忆",
        sage_type=SageType.DUAL_TYPE,
    ))

    # -- 藏书阁侍郎（正二品）左丘明 --
    positions.append(_p(
        id="LIB_SL", name="藏书阁侍郎", department="皇家藏书阁",
        pin=PinRank.ZHENG_2PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.MANAGEMENT, capacity=1,
        system_type=SystemType.CANGSHUGE,
        si_name="左丘明",
        dispatch_path="藏书阁大学士->侍郎->左丘明",
        suitable_schools=["史家", "儒家", "文学家"],
        description="藏书阁侍郎，左丘明担任，《左传》《国语》作者，辅助记忆收录与整理",
        sage_type=SageType.THEORIST,
    ))

    # -- 藏书阁编修（正三品）班固 --
    positions.append(_p(
        id="LIB_BX", name="藏书阁编修", department="皇家藏书阁",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.MANAGEMENT, capacity=1,
        system_type=SystemType.CANGSHUGE,
        si_name="班固",
        dispatch_path="藏书阁大学士->编修->班固",
        suitable_schools=["史家", "文学家", "历史思想"],
        description="藏书阁编修，班固担任，《汉书》作者，负责记忆质量审核与分级",
        sage_type=SageType.THEORIST,
    ))

    # -- 藏书阁校理（正四品）司马光 --
    positions.append(_p(
        id="LIB_XL", name="藏书阁校理", department="皇家藏书阁",
        pin=PinRank.ZHENG_4PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.CANGSHUGE,
        si_name="司马光",
        dispatch_path="藏书阁大学士->校理->司马光",
        suitable_schools=["史家", "儒家", "历史思想"],
        description="藏书阁校理，司马光担任，《资治通鉴》作者，负责记忆检索与校对",
        sage_type=SageType.DUAL_TYPE,
    ))

    # -- 藏书阁领班（正七品） --
    positions.append(_p(
        id="LIB_LB", name="藏书阁专员领班", department="皇家藏书阁",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.CANGSHUGE,
        si_name="藏书阁专员团队",
        dispatch_path="藏书阁大学士->专员领班",
        suitable_schools=["史家", "文学家"],
        description="藏书阁专员团队领班，负责专员日常管理和任务分配",
    ))

    return positions


def _build_congress_positions() -> List[Position]:
    """
    七人决策代表大会岗位 —— V1.0.0 新增纳入岗位体系

    七人代表大会驾临在所有系统之上（包括皇家藏书阁），
    采用投票决策制：4票及以上通过。

    成员配置（与 config/court_config.yaml 一致）：
      孔子  - CHIEF      - 王爵·太师·皇家系统（首席代表）
      管仲  - ECONOMY    - 伯爵·户部尚书（经济代表）
      韦伯  - SOCIOLOGY  - 伯爵·礼部尚书（社会学代表）
      德鲁克 - MANAGEMENT - 伯爵·工部尚书（管理学代表）
      孟子  - DEBATE     - 公爵·太傅·皇家系统（辩论质疑代表）
      张衡  - SPECIALIST_A - 专员·皇家科学院团队（科学技术代表）
      范蠡  - WHITE_CLOTH - 无任何任职（白衣代表）
    """
    positions = []

    # ── 孔子：首席代表 ──
    positions.append(_p(
        id="DH_ZX", name="代表大会首席代表", department="七人代表大会",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.WANGJUE,
        position_type=PositionType.SUPREME_SINGLE, capacity=1,
        system_type=SystemType.ROYAL,
        si_name="孔子",
        domain="代表大会首席决策与最终裁决",
        dispatch_path="皇帝→七人代表大会→首席代表→孔子",
        suitable_schools=["儒家", "教育家", "伦理"],
        description="七人决策代表大会首席代表，王爵·太师，由孔子担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 管仲：经济代表 ──
    positions.append(_p(
        id="DH_JJ", name="代表大会经济代表", department="七人代表大会",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ECONOMY,
        si_name="管仲",
        domain="宏观经济与产业政策决策",
        dispatch_path="皇帝→七人代表大会→经济代表→管仲",
        suitable_schools=["经济学家", "宏观经济", "国家治理"],
        description="七人决策代表大会经济代表，伯爵·户部尚书，由管仲担任",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 韦伯：社会学代表（V1.0: 西方贤者进入管理层）──
    positions.append(_p(
        id="DH_SH", name="代表大会社会学代表", department="七人代表大会",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.WENZHI,
        si_name="韦伯（Max Weber）",
        domain="社会学系统管理与组织理论",
        dispatch_path="皇帝→七人代表大会→社会学代表→韦伯",
        suitable_schools=["社会学家", "系统管理", "官僚制理论", "组织管理"],
        description="七人决策代表大会社会学代表，V1.0由韦伯担任（西方贤者），社会系统理论奠基人",
        sage_type=SageType.THEORIST,
    ))

    # ── 德鲁克：管理学代表（V1.0: 西方贤者进入管理层）──
    positions.append(_p(
        id="DH_GL", name="代表大会管理学代表", department="七人代表大会",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.BOJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.STANDARD,
        si_name="德鲁克（Peter Drucker）",
        domain="现代管理学与组织效能",
        dispatch_path="皇帝→七人代表大会→管理学代表→德鲁克",
        suitable_schools=["系统管理", "现代管理学之父", "组织效能"],
        description="七人决策代表大会管理学代表，V1.0由德鲁克担任（西方贤者），现代管理学之父",
        sage_type=SageType.DUAL_TYPE,
    ))

    # ── 孟子：辩论质疑代表 ──
    positions.append(_p(
        id="DH_BL", name="代表大会辩论质疑代表", department="七人代表大会",
        pin=PinRank.ZHENG_1PIN, nobility=NobilityRank.GONGJUE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ROYAL,
        si_name="孟子",
        domain="辩论质疑与仁政审查",
        dispatch_path="皇帝→七人代表大会→辩论质疑代表→孟子",
        suitable_schools=["儒家", "辩论质疑", "性善论", "仁政"],
        description="七人决策代表大会辩论质疑代表，公爵·太傅，由孟子担任",
        sage_type=SageType.THEORIST,
    ))

    # ── 张衡：科学技术代表 ──
    positions.append(_p(
        id="DH_KJ", name="代表大会科学技术代表", department="七人代表大会",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.INNOVATION,
        si_name="张衡",
        domain="科技创新与科学决策",
        dispatch_path="皇帝→七人代表大会→科学技术代表→张衡",
        suitable_schools=["科学家", "天文学", "科技创新"],
        description="七人决策代表大会科学技术代表，由张衡担任",
        sage_type=SageType.PRACTITIONER,
    ))

    # ── 范蠡：白衣代表 ──
    positions.append(_p(
        id="DH_BY", name="代表大会白衣代表", department="七人代表大会",
        pin=PinRank.ZHENG_3PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.EXECUTION, capacity=1,
        system_type=SystemType.ECONOMY,
        si_name="范蠡",
        domain="商业智慧与经济周期独立审查",
        dispatch_path="皇帝→七人代表大会→白衣代表→范蠡",
        suitable_schools=["商业智慧", "经济周期", "韬略"],
        description="七人决策代表大会白衣代表，无任何部门任职，由范蠡担任",
        sage_type=SageType.PRACTITIONER,
    ))

    return positions


def _build_specialist_leaders() -> List[Position]:
    """
    非锦衣卫专员团队领班 —— V1.0.0 新增

    为除锦衣卫（已有小旗领班序列）和藏书阁（已有专员领班）外的
    各部门专员团队增设TEAM_LEADER领班岗。

    新增领班：
      皇家系统：1岗（皇家专员团队领班）
      文治系统：1岗（文治专员团队领班）
      经济系统：1岗（户部专员团队领班）
      军政系统：1岗（军政专员团队领班）
      标准系统：1岗（标准专员团队领班）
      创新系统：1岗（创新专员团队领班）
    """
    positions = []

    # ── 皇家专员团队领班 ──
    positions.append(_p(
        id="HJ_LB_01", name="皇家专员团队领班", department="皇家",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.ROYAL,
        si_name="皇家专员团队",
        domain="皇家8类专员团队日常管理与任务分配",
        dispatch_path="皇帝→皇家→专员团队领班",
        suitable_schools=["儒家", "法家", "文学家"],
        description="皇家专员团队领班，管理文书/经学/礼仪/史籍/训诂/教育/侍卫/天文8类专员",
    ))

    # ── 文治专员团队领班 ──
    positions.append(_p(
        id="WZ_LB_01", name="文治专员团队领班", department="内阁",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.WENZHI,
        si_name="文治专员团队",
        domain="文治系统20类专员团队日常管理与任务分配",
        dispatch_path="皇帝→内阁→文治专员团队领班",
        suitable_schools=["儒家", "法家", "教育家"],
        description="文治专员团队领班，管理学派/评级/调度/文学/儒道佛史哲等20类专员",
    ))

    # ── 户部专员团队领班 ──
    positions.append(_p(
        id="JJ_LB_01", name="户部专员团队领班", department="户部",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.ECONOMY,
        si_name="户部专员团队",
        domain="户部8类专员团队日常管理与任务分配",
        dispatch_path="皇帝→内阁→户部→专员团队领班",
        suitable_schools=["经济学家", "科学家", "法家"],
        description="户部专员团队领班，管理数据采集/处理/行业分析/市场情报等8类专员",
    ))

    # ── 军政专员团队领班 ──
    positions.append(_p(
        id="JU_LB_01", name="军政专员团队领班", department="兵部",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.MILITARY,
        si_name="军政专员团队",
        domain="军政系统8类专员团队日常管理与任务分配",
        dispatch_path="皇帝→兵部→军政专员团队领班",
        suitable_schools=["兵家", "法家", "科学家"],
        description="军政专员团队领班，管理兵法/调度/神经布局/情报/信号/工程/战略等8类专员",
    ))

    # ── 标准专员团队领班 ──
    positions.append(_p(
        id="TD_LB_01", name="标准专员团队领班", department="标准系统",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.STANDARD,
        si_name="标准专员团队",
        domain="标准系统17类专员团队日常管理与任务分配",
        dispatch_path="皇帝→内阁→标准专员团队领班",
        suitable_schools=["法家", "科学家", "社会学家"],
        description="标准专员团队领班，管理风控/安全/合规/工程/增长/工具/产业/反馈/验证/研究等17类专员",
    ))

    # ── 创新专员团队领班 ──
    positions.append(_p(
        id="CX_LB_01", name="创新专员团队领班", department="内阁",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.INNOVATION,
        si_name="创新专员团队",
        domain="创新系统12类专员团队日常管理与任务分配",
        dispatch_path="皇帝→内阁→创新系统→创新专员团队领班",
        suitable_schools=["科学家", "企业家", "教育家"],
        description="创新专员团队领班，管理科研/推广/研究/工程/农学等12类专员",
    ))

    return positions


def _build_supplement_positions() -> List[Position]:
    """
    岗位体系补充 —— V1.0 新增45个专员岗/领班岗

    目标: 不修改现有377岗位，仅补充，确保：
    1. 每个学派至少有1个专员岗覆盖
    2. 过载岗位(>20人)拆分增加同类岗
    3. 传统六部补充基础专员岗
    4. 皇家藏书阁补充分类专员岗
    """
    positions = []

    # ═══════════════════════════════════════════════════════════════
    # 一、文治系统补充 (+12个专员岗) — 拆分过载 + 覆盖新学派
    # ═══════════════════════════════════════════════════════════════
    positions += _specialist_batch("WZ_P7S", "文治系统", PinRank.ZHENG_7PIN, items=[
        ("儒家研究专员", "儒学深度研究与应用推广", ["儒家"]),
        ("佛学禅修专员", "佛学禅修实践研究", ["佛家"]),
        ("佛学经典专员", "佛学经典翻译与研究", ["佛家"]),
        ("文学创作专员", "文学创作实践", ["文学家"]),
        ("文学评论专员", "文学批评与鉴赏", ["文学家", "文学批评家"]),
        ("史学编撰专员", "历史编撰与考证", ["史家"]),
        ("艺术书画专员", "书画艺术研究", ["艺术家"]),
        ("艺术音乐专员", "音乐与表演艺术", ["艺术家", "音乐家"]),
        ("西学专员", "西方哲学与思想研究", ["西方哲学", "英国哲学", "哲学"]),
        ("史学评论专员", "史学评论与史学理论", ["史家", "史学"]),
        ("道教专员", "道教修炼与研究", ["道家", "道教/武术"]),
        ("思潮专员", "综合思潮研究", ["思想家", "哲学家", "哲学", "其他"]),
        ("杂学专员", "杂学与心理学综合", ["其他", "心理学家", "心理学"]),
    ])

    # ═══════════════════════════════════════════════════════════════
    # 二、标准系统补充 (+6个专员岗) — 覆盖未覆盖学派
    # ═══════════════════════════════════════════════════════════════
    positions += _specialist_batch("TD_P7S", "标准系统", PinRank.ZHENG_7PIN, items=[
        ("文化批评专员", "文化批评与文学评论", ["文学家", "文学批评家", "文学"]),
        ("政治学专员", "政治学研究与分析", ["政治家", "政治"]),
        ("管理学专员", "管理学理论与实践", ["企业家", "管理", "管理学"]),
        ("科学专员", "自然科学综合研究", ["科学家", "科学", "科学思维"]),
        ("经济分析专员", "经济数据分析研究", ["经济学家", "经济"]),
        ("医学专员", "医学理论与实践研究", ["医家", "医学", "心理学家"]),
    ])

    # ═══════════════════════════════════════════════════════════════
    # 三、创新系统补充 (+4个专员岗) — 覆盖"政治"/"科学"/"文学"/"医学"
    # ═══════════════════════════════════════════════════════════════
    positions += _specialist_batch("CX_P7S", "创新系统", PinRank.ZHENG_7PIN,
        track="chuangxin",
        items=[
            ("政治创新专员", "政治制度创新研究", ["政治家", "政治", "治理战略家"]),
            ("科学实验专员", "科学实验与验证", ["科学家", "科学"]),
            ("文学创新专员", "文学体裁创新实验", ["文学家", "文学"]),
            ("医学研究专员", "医学创新研究", ["医家", "医学"]),
        ],
    )

    # ═══════════════════════════════════════════════════════════════
    # 四、六部补充专员岗 (+14个) — 传统六部原本只有管理层
    # ═══════════════════════════════════════════════════════════════
    positions += _specialist_batch("LB_P7", "礼部", PinRank.ZHENG_7PIN, items=[
        ("礼制专员", "礼仪制度研究与执行", ["儒家"]),
        ("经学专员", "经学典籍整理研究", ["儒家", "史家"]),
        ("文学侍从专员", "文学侍从与文书撰写", ["文学家", "诗人"]),
    ])
    positions += _specialist_batch("LP_P7", "吏部", PinRank.ZHENG_7PIN, items=[
        ("铨选专员", "人才选拔与考核辅助", ["法家", "政治家"]),
        ("考功专员", "政绩考核与能力评估", ["法家", "科学家"]),
    ])
    positions += _specialist_batch("XP_P7", "刑部", PinRank.ZHENG_7PIN, items=[
        ("刑律专员", "刑律条文研究与适用", ["法家", "政治家"]),
        ("狱政专员", "司法实践与案件分析", ["法家", "兵家"]),
    ])
    positions += _specialist_batch("BB_P7", "兵部", PinRank.ZHENG_7PIN, items=[
        ("兵制专员", "兵制建设与军事行政", ["兵家", "政治家"]),
        ("军需专员", "军需物资调配管理", ["科学家", "数学"]),
    ])
    positions += _specialist_batch("GB_P7", "工部", PinRank.ZHENG_7PIN, items=[
        ("营造专员", "工程营造与建筑", ["科学家", "墨家", "数学"]),
        ("水利专员", "水利工程规划管理", ["科学家", "数学"]),
    ])
    positions += _specialist_batch("WJ_P7", "五军都督府", PinRank.ZHENG_7PIN, items=[
        ("训练专员", "军队训练方案设计", ["兵家", "法家"]),
        ("军情专员", "军事情报分析汇总", ["纵横家", "兵家"]),
    ])
    positions += _specialist_batch("SF_P7", "三法司", PinRank.ZHENG_7PIN, items=[
        ("刑侦专员", "刑侦案件调查辅助", ["法家", "兵家"]),
    ])

    # ═══════════════════════════════════════════════════════════════
    # 五、皇家藏书阁补充 (+5个专员岗) — 四部典籍分类专员
    # ═══════════════════════════════════════════════════════════════
    positions += _specialist_batch("CS_P7", "皇家藏书阁", PinRank.ZHENG_7PIN, items=[
        ("藏书阁·经部专员", "经部典籍整理校注", ["儒家", "思想家"]),
        ("藏书阁·史部专员", "史部典籍整理编纂", ["史家"]),
        ("藏书阁·子部专员", "子部典籍整理研究", ["哲学家", "思想家", "科学家"]),
        ("藏书阁·集部专员", "集部文学典籍整理", ["文学家", "诗人", "艺术家"]),
        ("藏书阁·道藏专员", "道藏佛藏整理研究", ["道家", "佛家"]),
    ])

    # ═══════════════════════════════════════════════════════════════
    # 六、补充专员领班 (+3个)
    # ═══════════════════════════════════════════════════════════════
    positions.append(_p(
        id="LB_LB_01", name="礼部专员团队领班", department="礼部",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.STANDARD,
        si_name="礼部专员团队",
        domain="礼部3类专员团队日常管理与任务分配",
        dispatch_path="皇帝→礼部→礼部专员团队领班",
        suitable_schools=["儒家", "法家"],
        description="礼部专员团队领班，管理礼制/经学/文学侍从3类专员",
    ))
    positions.append(_p(
        id="GB_LB_01", name="工部专员团队领班", department="工部",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.STANDARD,
        si_name="工部专员团队",
        domain="工部2类专员团队日常管理与任务分配",
        dispatch_path="皇帝→工部→工部专员团队领班",
        suitable_schools=["科学家", "墨家"],
        description="工部专员团队领班，管理营造/水利2类专员",
    ))
    positions.append(_p(
        id="SF_LB_01", name="三法司专员团队领班", department="三法司",
        pin=PinRank.ZHENG_7PIN, nobility=NobilityRank.NOBLE_NONE,
        position_type=PositionType.TEAM_LEADER, capacity=1,
        system_type=SystemType.STANDARD,
        si_name="三法司专员团队",
        domain="三法司1类专员团队日常管理与任务分配",
        dispatch_path="皇帝→三法司→三法司专员团队领班",
        suitable_schools=["法家", "兵家"],
        description="三法司专员团队领班，管理刑侦专员",
    ))

    return positions









#  八、岗位注册中心
# ═══════════════════════════════════════════════════════════════════════════════

class CourtPositionRegistry:
    """
    朝廷岗位注册中心 v1.0

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
        self._total_sage_count: int = 862  # 动态获取，初始默认值

        self._build_all_positions()
        self._refresh_total_sage_count()

    def _refresh_total_sage_count(self) -> None:
        """动态获取贤者总数，替代硬编码"""
        try:
            from ..engines.cloning._sage_registry_full import get_registry_stats
            stats = get_registry_stats()
            count = stats.get("total", 0) if isinstance(stats, dict) else 0
            if count and count > 0:
                self._total_sage_count = count
        except (ImportError, AttributeError, TypeError):
            pass  # 保持默认值862

    def _build_all_positions(self) -> None:
        """构建所有系统的岗位树"""
        builders = [
            ("七人代表大会", _build_congress_positions),   # V1.0: 七人代表大会纳入岗位体系
            ("皇家", _build_royal_positions),
            ("文治系统", _build_wenzhi_positions),
            ("经济系统", _build_economy_positions),
            ("军政系统", _build_military_positions),
            ("标准系统", _build_standard_positions),
            ("创新系统", _build_chuangxin_positions),
            ("审核系统", _build_review_positions),  # v3.2 翰林院
            ("皇家藏书阁", _build_library_positions),  # v3.3 独立记忆体系
            ("专员领班", _build_specialist_leaders),  # V1.0: 非锦衣卫专员领班
            ("岗位补充", _build_supplement_positions),  # V1.0: 专员岗补充(+45)
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

    # ── 查询接口 ─────────────────────────────────────

    def get_position(self, position_id: str) -> Optional[Position]:
        return self._positions.get(position_id)

    def get_all_departments(self) -> List[str]:
        return list(self._departments.keys())

    def get_positions_by_department(self, department: str) -> List[Position]:
        # 优先按部门树键名查询
        tree = self._departments.get(department)
        if tree:
            return list(tree.positions.values())
        # 回退：按岗位自身department字段全局搜索（支持"厂卫"等子部门查询）
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
        school: str,
        tier: Any = None,
        expertise: List[str] = None,
    ) -> Optional[Position]:
        """
        为贤者匹配最佳岗位

        优先级：
        1. 精确匹配学派 → 岗位（排除已满岗位）
        2. 容量未满的岗位（按决策权从高到低）
        3. 专员岗位兜底（优先非文治系统的专员）
        """
        from ..engines.cloning._sage_registry_full import get_sage
        sage = get_sage(sage_name)
        if sage:
            school = sage.school
            expertise = sage.expertise
            tier = sage.tier

        # 按学派找适合岗位
        suitable = self.get_positions_by_school(school)
        if not suitable:
            # 回退：找包含儒家的通用岗位
            suitable = [
                p for p in self._positions.values()
                if "儒家" in p.suitable_schools
            ]

        if not suitable:
            return None

        # 分离固定容量和专员岗位
        fixed = [p for p in suitable if p.capacity != 999]
        specialists = [p for p in suitable if p.capacity == 999]

        # 按决策权从高到低排列固定容量岗位
        fixed.sort(key=lambda p: p.authority_value)
        for pos in fixed:
            filled = len(self._position_sage_map.get(pos.id, []))
            if filled < pos.capacity:
                return pos

        # 固定岗位都满了，找专员岗位
        non_wenzhi_spec = [
            p for p in specialists
            if p.system_type != SystemType.WENZHI
        ]
        if non_wenzhi_spec:
            non_wenzhi_spec.sort(key=lambda p: p.pin.value)
            return non_wenzhi_spec[0]

        if specialists:
            specialists.sort(key=lambda p: p.pin.value)
            return specialists[0]

        return None

    # ── 分配接口 ─────────────────────────────────────

    def assign_sage(self, sage_name: str, position_id: str) -> bool:
        """将贤者分配到指定岗位"""
        pos = self._positions.get(position_id)
        if not pos:
            return False

        filled = len(self._position_sage_map.get(position_id, []))
        if pos.capacity != 999 and filled >= pos.capacity:
            return False

        # 如果已有岗位，先移除
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
        from ..engines.cloning._sage_registry_full import ALL_SAGES

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
                        # 统计（用department字段）
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

    # ── 升级同步 ─────────────────────────────────────

    def sync_sage_upgrade(
        self,
        sage_name: str,
        new_tier: Any,
        new_capabilities: Optional[List[str]] = None,
    ) -> bool:
        """贤者升级时同步岗位"""
        current = self.get_sage_position(sage_name)
        if not current:
            from ..engines.cloning._sage_registry_full import get_sage
            sage = get_sage(sage_name)
            if sage:
                pos = self.get_best_position_for_sage(sage.name, sage.school, new_tier)
                if pos:
                    return self.assign_sage(sage_name, pos.id)
            return False

        pos_id, pos = current

        # Tier1 FOUNDER → 伯爵+或侯爵+（正一品/正三品）
        # Tier2 MASTER → 伯爵（正三品）或管理层（正四品）
        # Tier3 SCHOLAR → 管理层（正四~六品）
        # Tier4 PRACTITIONER → 专员（七品）

        from ..engines.cloning._sage_registry_full import SageTier
        target_max_authority = 99  # 默认不升级
        if new_tier == SageTier.FOUNDER:
            target_max_authority = 2   # 侯爵级
        elif new_tier == SageTier.MASTER:
            target_max_authority = 3   # 伯爵级
        elif new_tier == SageTier.SCHOLAR:
            target_max_authority = 40  # 正四品

        # 如果当前岗位决策权低于目标，尝试升级
        if pos.authority_value > target_max_authority:
            from ..engines.cloning._sage_registry_full import get_sage
            sage = get_sage(sage_name)
            if sage:
                better_pos = self.get_best_position_for_sage(
                    sage.name, sage.school, new_tier
                )
                if better_pos and better_pos.authority_value < pos.authority_value:
                    return self.assign_sage(sage_name, better_pos.id)

        return True

    # ── 统计接口 ─────────────────────────────────────

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
            if not pos.dispatch_path and pos.pin.value <= PinRank.ZHENG_4PIN.value:
                issues.append(f"岗位 {pos.name}({pos_id}) 缺少调用链路")

        from ..engines.cloning._sage_registry_full import ALL_SAGES
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
        """获取实战派统计信息（v3.1新增）"""
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
        """检查各系统实战派占比是否达标（v3.1新增）"""
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


# ═══════════════════════════════════════════════════════════════════════════════
#  九、模块级便捷接口
# ═══════════════════════════════════════════════════════════════════════════════

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



# [P0修复] 命令行入口已禁用，统一通过 somn.py 入口调用