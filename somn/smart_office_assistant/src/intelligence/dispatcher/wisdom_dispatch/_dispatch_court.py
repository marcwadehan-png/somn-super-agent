"""
神之架构 - 朝廷部门调度层 V1.0.0
_dispatch_court.py

25门通识能力 → 六部/厂卫/三法司/五军都督府 + 翰林院 + 皇家藏书阁 跨部门调度
基于神之架构V4.0.0 "全贤就位，百官齐备" 实现

核心概念:
- 25个智慧学派是朝廷通用能力库，不属于任何部门独占
- 吏部（WisdomDispatcher）负责学派的注册、权重、调度与考核
- 六部、厂卫、三法司、五军都督府按业务场景跨部门调用
- 翰林院独立于六部之外，对所有决策进行审核和反驳
- 皇家藏书阁独立于所有体系之外，不受任何团队管理
- 调度路径: ProblemType → Department → School组合
- V1.0.0: 全面升级版本号，862贤者100%任命到位
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from ._dispatch_enums import WisdomSchool, ProblemType


class Department(Enum):
    """神之架构六部 + 厂卫 + 三法司 + 五军都督府 + 翰林院(v3.2) + 皇家藏书阁(v3.3)"""
    LIBU = "吏部"          # 能力层 - 学派注册/权重/调度/考核
    HUBU = "户部"          # 数据层 - 数据采集/知识图谱/行业知识
    LIBU_LI = "礼部"       # 记忆层 - 记忆系统/学习系统/文学
    BINGBU = "兵部"        # 调度层 - 主线调度/神经网络布局
    XINGBU = "刑部"        # 监察层 - 风控/安全/内容审核
    GONGBU = "工部"        # 执行层 - 核心执行/增长引擎/工具链
    CHANGWEI = "厂卫"      # 秘密监控 - 系统监控/性能优化/主线监控
    SANFASI = "三法司"     # 独立监察 - 反馈/验证/ROI
    WUJUN = "五军都督府"   # 神经网络 - 网络布局/信号传递/突触连接
    HANLIN = "翰林院"      # v3.2 决策审核 - 逻辑论证/多视角反驳/综合评审
    CANGSHUGE = "皇家藏书阁"  # v3.3 独立记忆体系 - 不受任何部门管理


class DepartmentRole(Enum):
    """部门在能力调用中的角色"""
    PRIMARY = "primary"    # 主调度部门（权重>=0.5）
    SECONDARY = "secondary" # 辅调度部门（权重<0.5）


# ═══════════════════════════════════════════════════════════════
#  跨部门能力调用矩阵（懒加载模式）
#  格式: ProblemType → List[(Department, DepartmentRole, Set[WisdomSchool])]
# ═══════════════════════════════════════════════════════════════

# 缓存已加载的数据
_cached_matrix = None


def _get_department_school_matrix() -> Dict[ProblemType, List[Tuple[Department, DepartmentRole, List[Tuple[WisdomSchool, float]]]]]:
    """
    获取 DEPARTMENT_SCHOOL_MATRIX 数据（懒加载模式）。

    首次调用时从 _dispatch_matrix_data 模块加载，
    之后使用缓存避免重复导入。
    """
    global _cached_matrix
    if _cached_matrix is None:
        from ._dispatch_matrix_data import get_matrix_data
        _cached_matrix = get_matrix_data()
    return _cached_matrix


def __getattr__(name: str):
    """支持懒加载访问 DEPARTMENT_SCHOOL_MATRIX"""
    if name == "DEPARTMENT_SCHOOL_MATRIX":
        return _get_department_school_matrix()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# ═══════════════════════════════════════════════════════════════
#  部门路由核心函数
# ═══════════════════════════════════════════════════════════════

def resolve_departments(
    problem_type: ProblemType,
    problem_school_mapping: Dict[ProblemType, List[Tuple[WisdomSchool, float]]],
) -> List[Tuple[Department, DepartmentRole, List[Tuple[WisdomSchool, float]]]]:
    """
    根据问题类型，确定需要调度的部门及其对应的能力组合。

    优先使用 DEPARTMENT_SCHOOL_MATRIX 中的显式部门路由；
    若问题类型未在部门矩阵中注册，则根据 problem_school_mapping
    自动推断最匹配的部门。

    Args:
        problem_type: 问题类型
        problem_school_mapping: 原有问题→学派映射矩阵（WisdomDispatcher.problem_school_mapping）

    Returns:
        按优先级排序的 [(Department, DepartmentRole, [(WisdomSchool, weight)])] 列表
    """
    matrix = _get_department_school_matrix()

    # 1. 显式路由：部门矩阵中有定义
    if problem_type in matrix:
        return matrix[problem_type]

    # 2. 自动推断：根据 problem_school_mapping 反推部门
    school_dept_affinity = _build_school_department_affinity()
    school_weights = problem_school_mapping.get(problem_type, [])
    if not school_weights:
        return [(Department.LIBU, DepartmentRole.PRIMARY, school_weights)]

    # 统计每个部门的加权匹配分
    dept_scores: Dict[Department, float] = {}
    for school, weight in school_weights:
        for dept in school_dept_affinity.get(school, []):
            dept_scores[dept] = dept_scores.get(dept, 0.0) + weight

    if not dept_scores:
        return [(Department.LIBU, DepartmentRole.PRIMARY, school_weights)]

    # 排序取最高分的部门
    sorted_depts = sorted(dept_scores.items(), key=lambda x: x[1], reverse=True)
    primary_dept = sorted_depts[0][0]
    return [(primary_dept, DepartmentRole.PRIMARY, school_weights)]


def _build_school_department_affinity() -> Dict[WisdomSchool, List[Department]]:
    """
    构建学派→部门的亲和力表。
    反向推导自 DEPARTMENT_SCHOOL_MATRIX：
    如果某学派在某个部门的调用场景中权重>=0.5，则该学派对该部门有亲和力。
    """
    matrix = _get_department_school_matrix()
    affinity: Dict[WisdomSchool, Set[Department]] = {}
    for pt, dispatches in matrix.items():
        for dept, role, schools in dispatches:
            for school, weight in schools:
                if weight >= 0.5:
                    if school not in affinity:
                        affinity[school] = set()
                    affinity[school].add(dept)
    return {s: list(depts) for s, depts in affinity.items()}


def get_department_for_problem(
    problem_type: ProblemType,
) -> Tuple[Department, str]:
    """
    快速获取问题类型对应的主调度部门及其调用理由。

    Returns:
        (主调度部门, 调用理由)
    """
    matrix = _get_department_school_matrix()
    dispatches = matrix.get(problem_type, [])
    if dispatches:
        primary = dispatches[0]
        dept = primary[0]
        schools_str = " + ".join(f"{s[0].value}({s[1]:.1f})" for s in primary[2])
        reason = f"{dept.value}调度: {schools_str}"
        return dept, reason
    return Department.LIBU, f"吏部默认调度: {problem_type.value}"


def get_all_departments_for_school(school: WisdomSchool) -> List[Department]:
    """获取调用指定学派的所有部门（按亲和力排序）"""
    affinity = _build_school_department_affinity()
    return affinity.get(school, [])


def get_school_heatmap() -> Dict[str, Dict[str, str]]:
    """
    生成能力跨部门热度图。
    Returns: {学派名: {部门名: 角色标识}}
    """
    matrix = _get_department_school_matrix()
    heatmap: Dict[str, Dict[str, str]] = {}
    for school in WisdomSchool:
        heatmap[school.value] = {}
    for pt, dispatches in matrix.items():
        for dept, role, schools in dispatches:
            for school, weight in schools:
                marker = "star" if weight >= 0.5 and role == DepartmentRole.PRIMARY else "circle"
                dept_name = dept.value
                if dept_name not in heatmap[school.value] or marker == "star":
                    heatmap[school.value][dept_name] = marker
    return heatmap


# ═══════════════════════════════════════════════════════════════
# v1.0.0 岗位体系集成（爵位+品秩+实战派三轨制）
# 将 ProblemType → Department 路由扩展为
# ProblemType → Department → System → Position → Sage (+SageType)
# ═══════════════════════════════════════════════════════════════

# Department枚举值 → (系统名, 部门名) 的统一映射（v1.0.0 合并冗余表）
_DEPT_INFO_MAP = {
    Department.LIBU.value:       ("文治系统", "吏部"),
    Department.LIBU_LI.value:    ("文治系统", "礼部"),
    Department.HUBU.value:       ("经济系统", "户部"),
    Department.BINGBU.value:     ("军政系统", "兵部"),
    Department.CHANGWEI.value:   ("军政系统", "厂卫"),
    Department.WUJUN.value:      ("军政系统", "五军都督府"),
    Department.XINGBU.value:     ("标准系统", "刑部"),
    Department.GONGBU.value:     ("标准系统", "工部"),
    Department.SANFASI.value:    ("标准系统", "三法司"),
    Department.HANLIN.value:     ("审核系统", "翰林院"),       # v3.2
    Department.CANGSHUGE.value:  ("藏书阁系统", "皇家藏书阁"),  # v3.3
}


def _dept_system(dept_value: str) -> str:
    """获取部门对应的系统名"""
    info = _DEPT_INFO_MAP.get(dept_value)
    return info[0] if info else ""


def _dept_name(dept_value: str) -> str:
    """获取部门对应的部门名"""
    info = _DEPT_INFO_MAP.get(dept_value)
    return info[1] if info else dept_value


def _get_court_positions_for_dept(dept_value: str, system_filter: str = "") -> list:
    """
    根据Department枚举值获取对应的岗位列表。

    v3.1新增: system_filter 支持按 SystemType 枚举值精确过滤，
    解决"内阁"同时包含文治/创新两个系统的问题。

    Args:
        dept_value: Department枚举值的中文部门名
        system_filter: SystemType枚举值，如 "innovation"/"wenzhi"，空则不过滤
    """
    try:
        from src.intelligence.engines.cloning._court_positions import get_court_registry
    except ImportError:
        return []
    registry = get_court_registry()
    # 优先按系统名查找
    system_name = _dept_system(dept_value)
    if system_name:
        positions = registry.get_positions_by_department(system_name)
        if positions:
            # v3.1: 如果需要按 system_type 过滤（如创新系统）
            if system_filter:
                positions = [p for p in positions if p.system_type.value == system_filter]
            if positions:
                return positions
    # 回退：按部门名查找
    dept_name = _dept_name(dept_value)
    positions = registry.get_positions_by_department(dept_name)
    if system_filter and positions:
        positions = [p for p in positions if p.system_type.value == system_filter]
    return positions


def _apply_practitioner_boost(positions: list) -> list:
    """
    v3.1: 对实战派岗位应用权重加成，返回排序后的岗位列表。

    实战派岗位按 authority_value * boost_factor 排序，
    使其在调度结果中优先级更高。
    """
    def _boosted_authority(pos):
        base = pos.authority_value
        system_val = pos.system_type.value if hasattr(pos, 'system_type') else ""
        boost = _PRACTITIONER_WEIGHT_BOOST.get(system_val, 1.0)
        # 实战派或复合型岗位获得加成
        if hasattr(pos, 'sage_type') and pos.sage_type is not None:
            if pos.sage_type.value in ("practitioner", "dual_type"):
                return base * boost
        return base

    return sorted(positions, key=_boosted_authority)


# 实战派权重加成系数（按系统类型）
_PRACTITIONER_WEIGHT_BOOST = {
    "economy": 1.15,     # 经济系统：实战派优先级最高
    "military": 1.10,    # 军政系统：实战派重要
    "innovation": 1.10,  # 创新系统：实战驱动
    "standard": 1.05,    # 标准系统：略高
    "wenzhi": 1.0,       # 文治系统：不额外加成
    "royal": 1.0,        # 皇家系统：不加成
    "censor": 1.0,       # 审核系统：不加成
    "library": 1.0,      # 藏书阁：不加成
}


def resolve_positions_for_problem(
    problem_type: ProblemType,
    problem_school_mapping: Optional[Dict] = None,
) -> List[Dict[str, Any]]:
    """
    根据问题类型，解析出完整的调度链路（v3.1: 含SageType）：
    ProblemType → Department → System → Position → Sage (+SageType)

    v3.1变更:
    - 返回值新增 "sage_type" 字段（实战派/理论派/复合型）
    - 返回值新增 "practitioner_boost" 字段（实战派加成系数）
    - 实战派岗位在排序中获得权重加成

    Returns:
        [{
            "department": "兵部",
            "system": "military",
            "position_id": "JU_BB_GJ",
            "position_name": "兵部尚书·公爵",
            "display_rank": "公爵 正一品",
            "nobility": "公爵",
            "pin": "正一品",
            "assigned_sages": ["孙武", "老子", ...],
            "schools": ["兵家(0.9)", "道家(0.5)"],
            "dispatch_path": "皇帝→兵部尚书·公爵→...",
            "role": "primary",
            "sage_type": "practitioner",        # v3.1新增
            "sage_type_display": "⚔",          # v3.1新增
            "practitioner_boost": 1.10,         # v3.1新增
            "authority_value": 1,
        }, ...]
    """
    try:
        from src.intelligence.engines.cloning._court_positions import (
            get_court_registry, _NOBILITY_NAMES, _PIN_NAMES,
            SageType, _SAGE_TYPE_NAMES, _SAGE_TYPE_SYMBOLS,
        )
    except ImportError:
        return []

    registry = get_court_registry()
    dispatches = DEPARTMENT_SCHOOL_MATRIX.get(problem_type, [])
    if not dispatches:
        return []

    results = []
    for dept, role, schools in dispatches:
        # v3.1: 尝试同时获取文治和创新系统岗位（仅对内阁部门需要）
        dept_name = dept.value
        dept_positions = _get_court_positions_for_dept(dept_name)

        # v3.1: 如果是内阁部门，额外获取创新系统岗位
        if dept_name == "内阁":
            innovation_positions = _get_court_positions_for_dept(dept_name, system_filter="innovation")
            if innovation_positions:
                # 去重
                existing_ids = {p.id for p in dept_positions}
                for ip in innovation_positions:
                    if ip.id not in existing_ids:
                        dept_positions = list(dept_positions) + [ip]

        if not dept_positions:
            continue

        # v3.1: 应用实战派权重加成排序
        dept_positions = _apply_practitioner_boost(list(dept_positions))

        for pos in dept_positions[:5]:
            assigned = registry._position_sage_map.get(pos.id, [])
            schools_str = " + ".join(f"{s[0].value}({s[1]:.1f})" for s in schools)

            # v3.1: 提取 sage_type 信息
            sage_type_val = ""
            sage_type_display = ""
            practitioner_boost = 1.0
            if hasattr(pos, 'sage_type') and pos.sage_type is not None:
                sage_type_val = pos.sage_type.value
                sage_type_display = _SAGE_TYPE_SYMBOLS.get(pos.sage_type, "")
                system_val = pos.system_type.value if hasattr(pos, 'system_type') else ""
                practitioner_boost = _PRACTITIONER_WEIGHT_BOOST.get(system_val, 1.0)

            results.append({
                "department": dept.value,
                "system": pos.system_type.value,
                "position_id": pos.id,
                "position_name": pos.name,
                "display_rank": pos.display_rank,
                "nobility": _NOBILITY_NAMES.get(pos.nobility, "无"),
                "pin": _PIN_NAMES.get(pos.pin, str(pos.pin.value)),
                "is_zheng": pos.is_zheng,
                "assigned_sages": assigned[:10],
                "total_assigned": len(assigned),
                "schools": schools_str,
                "dispatch_path": pos.dispatch_path,
                "domain": pos.domain,
                "role": role.value,
                "authority_value": pos.authority_value,
                # v3.1 新增字段
                "sage_type": sage_type_val,
                "sage_type_display": sage_type_display,
                "practitioner_boost": practitioner_boost,
            })

    return results


def get_sage_court_info(sage_name: str) -> Optional[Dict[str, Any]]:
    """
    获取贤者在朝廷岗位体系中的完整信息（v3.1 三轨制）。

    v3.1变更:
    - 返回值新增 "sage_type" 和 "sage_type_display" 字段

    Returns:
        {
            "sage_name": "孔子",
            "position_id": "WZ_NG_Z1",
            "position_name": "内阁首辅（正一品）",
            "display_rank": "正一品",
            "nobility": "无",
            "pin": "正一品",
            "is_zheng": True,
            "system": "wenzhi",
            "department": "内阁",
            "authority_value": 10,
            "dispatch_path": "...",
            "coworkers": ["孟子", "朱熹"],
            "sage_type": "theorist",           # v3.1新增
            "sage_type_display": "📚",         # v3.1新增
        }
    """
    try:
        from src.intelligence.engines.cloning._court_positions import (
            get_court_registry, _NOBILITY_NAMES, _PIN_NAMES,
            SageType, _SAGE_TYPE_NAMES, _SAGE_TYPE_SYMBOLS,
        )
    except ImportError:
        return None

    registry = get_court_registry()
    result = registry.get_sage_position(sage_name)
    if not result:
        return None

    pos_id, pos = result
    coworkers = [
        name for name in registry._position_sage_map.get(pos_id, [])
        if name != sage_name
    ]

    # v3.1: 提取 sage_type
    sage_type_val = ""
    sage_type_display = ""
    if hasattr(pos, 'sage_type') and pos.sage_type is not None:
        sage_type_val = pos.sage_type.value
        sage_type_display = _SAGE_TYPE_SYMBOLS.get(pos.sage_type, "")

    return {
        "sage_name": sage_name,
        "position_id": pos_id,
        "position_name": pos.name,
        "display_rank": pos.display_rank,
        "nobility": _NOBILITY_NAMES.get(pos.nobility, "无"),
        "pin": _PIN_NAMES.get(pos.pin, str(pos.pin.value)),
        "is_zheng": pos.is_zheng,
        "system": pos.system_type.value,
        "department": pos.department,
        "type": pos.position_type.value,
        "capacity": pos.capacity,
        "authority_value": pos.authority_value,
        "domain": pos.domain,
        "dispatch_path": pos.dispatch_path,
        "suitable_schools": pos.suitable_schools,
        "coworkers": coworkers,
        # v3.1 新增
        "sage_type": sage_type_val,
        "sage_type_display": sage_type_display,
    }


def get_full_court_stats() -> Dict[str, Any]:
    """
    获取完整的朝廷岗位体系统计信息（v3.1 三轨制）。
    """
    try:
        from src.intelligence.engines.cloning._court_positions import get_court_registry
    except ImportError:
        return {"error": "CourtPositionRegistry not available"}

    registry = get_court_registry()
    if registry.get_stats()["total_assigned_sages"] == 0:
        registry.auto_assign_all_sages()

    return registry.get_stats()


def get_practitioner_stats() -> Dict[str, Any]:
    """
    v3.1新增: 获取实战派分布统计。

    Returns:
        {
            "total_nobility": 24,
            "practitioner_count": 11,
            "theorist_count": 11,
            "dual_type_count": 2,
            "by_system": {
                "economy": {"practitioner": 2, "total": 3},
                "innovation": {"practitioner": 4, "total": 7},
                ...
            },
            "quota_check": {
                "economy": "PASS",    # >=2
                "innovation": "PASS", # >=2
                "standard": "PASS",   # >=1
                "military": "PASS",   # >=50%
            }
        }
    """
    try:
        from src.intelligence.engines.cloning._court_positions import (
            get_court_registry, SageType, _PRACTITIONER_QUOTA,
        )
    except ImportError:
        return {"error": "CourtPositionRegistry not available"}

    registry = get_court_registry()
    stats = registry.get_stats()

    # 收集所有爵位岗位的 sage_type
    nobility_positions = []
    for dept_tree in registry._departments.values():
        for pos in dept_tree.positions.values():
            if hasattr(pos, 'nobility') and pos.nobility.value < 99:  # 有爵位
                nobility_positions.append(pos)

    practitioner_count = sum(
        1 for p in nobility_positions
        if hasattr(p, 'sage_type') and p.sage_type == SageType.PRACTITIONER
    )
    theorist_count = sum(
        1 for p in nobility_positions
        if hasattr(p, 'sage_type') and p.sage_type == SageType.THEORIST
    )
    dual_count = sum(
        1 for p in nobility_positions
        if hasattr(p, 'sage_type') and p.sage_type == SageType.DUAL_TYPE
    )

    # 按系统统计
    by_system: Dict[str, Dict[str, int]] = {}
    for p in nobility_positions:
        sys_val = p.system_type.value if hasattr(p, 'system_type') else "unknown"
        if sys_val not in by_system:
            by_system[sys_val] = {"practitioner": 0, "theorist": 0, "dual_type": 0, "total": 0}
        by_system[sys_val]["total"] += 1
        if hasattr(p, 'sage_type') and p.sage_type:
            st = p.sage_type.value
            if st in by_system[sys_val]:
                by_system[sys_val][st] += 1

    # 占比检查
    quota_check: Dict[str, str] = {}
    for sys_name, quota in _PRACTITIONER_QUOTA.items():
        if quota is None:
            quota_check[sys_name] = "N/A"
            continue
        sys_data = by_system.get(sys_name, {})
        if isinstance(quota, float):
            # 百分比要求 (如 military >= 50%)
            total = sys_data.get("total", 0)
            prac = sys_data.get("practitioner", 0) + sys_data.get("dual_type", 0)
            if total > 0 and (prac / total) >= quota:
                quota_check[sys_name] = "PASS"
            else:
                quota_check[sys_name] = "FAIL"
        else:
            # 人数要求 (如 economy >= 2)
            prac = sys_data.get("practitioner", 0) + sys_data.get("dual_type", 0)
            quota_check[sys_name] = "PASS" if prac >= quota else "FAIL"

    return {
        "total_nobility": len(nobility_positions),
        "practitioner_count": practitioner_count,
        "theorist_count": theorist_count,
        "dual_type_count": dual_count,
        "by_system": by_system,
        "quota_check": quota_check,
    }


# ═══════════════════════════════════════════════════════════════
# v1.0.0 翰林院决策审核集成
# 所有决策必须经过翰林院三轮审核（逻辑论证→多视角反驳→综合评审）
# 才能输出最终结果
# ═══════════════════════════════════════════════════════════════

def get_hanlin_reviewers() -> List[Dict[str, Any]]:
    """
    v3.2新增: 获取翰林院审核团队成员。

    Returns:
        [
            {"position": "翰林院掌院", "sage": "韩非子", "role": "逻辑论证总管",
             "pin": "正三品", "sage_type": "dual_type"},
            {"position": "翰林院学士甲", "sage": "墨子", "role": "经济可行性",
             "pin": "正四品", "sage_type": "practitioner"},
            ...
        ]
    """
    try:
        from src.intelligence.engines.cloning._court_positions import get_court_registry, _SAGE_TYPE_NAMES
    except ImportError:
        return []

    registry = get_court_registry()
    positions = registry.get_positions_by_department("审核系统")
    if not positions:
        return []

    reviewers = []
    for pos in positions:
        sage_type_val = pos.sage_type.value if hasattr(pos, 'sage_type') and pos.sage_type else ""
        reviewers.append({
            "position": pos.name,
            "sage": pos.si_name,
            "role": pos.description.split(",")[0] if pos.description else "",
            "pin": pos.display_rank,
            "sage_type": sage_type_val,
            "sage_type_display": _SAGE_TYPE_NAMES.get(sage_type_val, ""),
        })
    return sorted(reviewers, key=lambda x: x["pin"])


def submit_for_hanlin_review(
    decision: str,
    problem_type: str = "",
    context: str = "",
    strictness: str = "standard",
) -> Dict[str, Any]:
    """
    v3.2新增: 将决策提交翰林院审核。

    翰林院审核流程（三轮）:
      第一轮: 逻辑论证检测 —— 韩非子（掌院）检查论证完整性
      第二轮: 多视角反驳 —— 6位学士/侍读从不同角度反驳
      第三轮: 综合评审 —— 掌院汇总，给出通过/有条件通过/否决

    Args:
        decision: 待审核的决策文本
        problem_type: 问题类型（用于定位审核重点）
        context: 决策上下文
        strictness: 审核严格度 "lenient"/"standard"/"strict"

    Returns:
        {
            "passed": True/False,
            "verdict": "通过"/"有条件通过"/"否决",
            "overall_score": 0.85,
            "rounds": {
                "logic_check": {"score": ..., "issues": [...]},
                "multi_perspective": {"score": ..., "challenges": [...]},
                "final_review": {"score": ..., "conditions": [...]}
            },
            "hanlin_members": [...],
        }
    """
    try:
        from ._hanlin_review import HanlinReviewEngine
    except ImportError:
        return {"error": "HanlinReviewEngine not available", "passed": False, "verdict": "否决"}

    chamber = HanlinReviewEngine()

    # 构建翰林院审核上下文
    review_context = {
        "problem_type": problem_type,
        "context": context,
        "strictness": strictness,
    }

    result = chamber.review_decision(
        decision_text=decision,
        decision_context=review_context if problem_type or context else None,
    )

    # 将 HanlinReviewResult 转为字典格式
    result_dict = {
        "passed": getattr(result, 'passed', False),
        "verdict": getattr(result, 'verdict', '否决'),
        "overall_score": getattr(result, 'overall_score', 0.0),
        "rounds": {},
    }

    # 提取三轮审核详情
    for round_name in ['logic_check', 'multi_perspective', 'final_review']:
        round_result = getattr(result, round_name, None)
        if round_result:
            result_dict["rounds"][round_name] = {
                "score": getattr(round_result, 'score', 0.0),
                "issues": getattr(round_result, 'issues', []),
                "challenges": getattr(round_result, 'challenges', []),
                "conditions": getattr(round_result, 'conditions', []),
            }

    # 附带翰林院成员信息
    result_dict["hanlin_members"] = get_hanlin_reviewers()

    # v1.0.0: 自动将审核结果提交到藏书阁
    try:
        review_summary = (
            f"等级: {result_dict.get('verdict', '')}, "
            f"综合分: {result_dict.get('overall_score', 0):.3f}\n"
        )
        for round_name, round_data in result_dict.get("rounds", {}).items():
            review_summary += f"  {round_name}: {round_data.get('score', 0):.3f}\n"
        if result_dict["rounds"].get("multi_perspective", {}).get("challenges"):
            review_summary += "反驳意见:\n"
            for ch in result_dict["rounds"]["multi_perspective"]["challenges"]:
                review_summary += f"  - {ch}\n"

        library_record = submit_to_imperial_library(
            title=f"翰林院审核: {decision[:60]}",
            content=f"决策摘要: {decision[:200]}\n\n{review_summary}",
            source="翰林院审核记录",
            category="审核记录",
            reporting_department="翰林院",
            tags=["翰林院", "审核", problem_type],
            metadata={
                "verdict": result_dict.get("verdict", ""),
                "overall_score": result_dict.get("overall_score", 0),
                "passed": result_dict.get("passed", False),
            },
        )
        result_dict["library_record"] = library_record
    except Exception:
        pass  # 藏书阁集成失败不影响审核流程

    return result_dict


def should_require_hanlin_review(problem_type: ProblemType, source: str = "") -> bool:
    """
    v3.2新增: 判断某个问题类型是否需要翰林院审核。
    v2.0更新: 代表大会决策豁免翰林院审核。

    规则:
    - 代表大会决策（source="七人决策代表大会"或"代表大会决策"）: 免审
    - 营销类（MARKETING, CONSUMER_MARKETING, BRAND_STRATEGY）: 必须
    - 社会影响类（SOCIAL_STABILITY, PUBLIC_INTEREST, ETHICAL）: 必须
    - 战略类（STRATEGY, CHANGE, COMPETITION）: 推荐
    - 其他: 可选
    """
    # v1.0: 代表大会决策不受翰林院审核
    if source in ("七人决策代表大会", "代表大会决策", "圣旨"):
        return False

    _MANDATORY_TYPES = {
        ProblemType.MARKETING, ProblemType.CONSUMER_MARKETING,
        ProblemType.BRAND_STRATEGY, ProblemType.SOCIAL_STABILITY,
        ProblemType.PUBLIC_INTEREST, ProblemType.ETHICAL,
    }
    _RECOMMENDED_TYPES = {
        ProblemType.STRATEGY, ProblemType.CHANGE, ProblemType.COMPETITION,
        ProblemType.RISK, ProblemType.NEGOTIATION,
    }

    if problem_type in _MANDATORY_TYPES:
        return True
    if problem_type in _RECOMMENDED_TYPES:
        return True  # 推荐也默认需要审核
    return False


# ═══════════════════════════════════════════════════════════════
# v1.0.0 集成层：藏书阁 / 代表大会 / 大秦指标 / 行政之鞭
# 解决 v3.3 新增模块与调度层的集成断裂问题
# ═══════════════════════════════════════════════════════════════

def submit_to_imperial_library(
    title: str,
    content: str,
    source: str,
    category: str,
    reporting_department: str,
    tags: list = None,
    metadata: dict = None,
    suggested_grade: str = "",
) -> Optional[Dict[str, Any]]:
    """
    v1.0.0新增: 提交记忆到皇家藏书阁。

    所有系统模块产生的有价值记录，都应通过此接口提交藏书阁。
    藏书阁会自主评估价值并决定保留等级。

    Args:
        title: 记忆标题
        content: 记忆内容
        source: 来源枚举值（MemorySource.value）
        category: 分类枚举值（MemoryCategory.value）
        reporting_department: 汇报部门
        tags: 标签列表
        metadata: 元数据
        suggested_grade: 建议等级（MemoryGrade.value），可空

    Returns:
        收录结果字典，或 None（藏书阁不可用时）
    """
    try:
        from ._imperial_library import (
            get_imperial_library, MemorySource, MemoryCategory, MemoryGrade,
        )
    except ImportError:
        return {"error": "ImperialLibrary not available"}

    library = get_imperial_library()

    # 枚举映射
    source_map = {s.value: s for s in MemorySource}
    category_map = {c.value: c for c in MemoryCategory}
    grade_map = {g.value: g for g in MemoryGrade}

    src = source_map.get(source, MemorySource.SYSTEM_EVENT)
    cat = category_map.get(category, MemoryCategory.OTHER)
    grade = grade_map.get(suggested_grade, None)

    record = library.submit_memory(
        title=title,
        content=content,
        source=src,
        category=cat,
        reporting_department=reporting_department,
        tags=tags or [],
        metadata=metadata or {},
        suggested_grade=grade,
    )

    return {
        "id": record.id,
        "title": record.title,
        "grade": record.grade.value,
        "value_score": round(record.value_score, 3),
    }


def query_imperial_library(
    grade: str = "",
    category: str = "",
    source: str = "",
    department: str = "",
    keyword: str = "",
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """
    v1.0.0新增: 查询皇家藏书阁记忆。

    Returns:
        记忆列表（按价值评分降序）
    """
    try:
        from ._imperial_library import (
            get_imperial_library, MemoryGrade, MemoryCategory, MemorySource,
        )
    except ImportError:
        return []

    library = get_imperial_library()

    grade_map = {g.value: g for g in MemoryGrade}
    category_map = {c.value: c for c in MemoryCategory}
    source_map = {s.value: s for s in MemorySource}

    records = library.query_memories(
        grade=grade_map.get(grade, None),
        category=category_map.get(category, None),
        source=source_map.get(source, None),
        department=department or None,
        keyword=keyword or None,
        limit=limit,
    )

    return [
        {
            "id": r.id,
            "title": r.title,
            "grade": r.grade.value,
            "value_score": round(r.value_score, 3),
            "source": r.source.value,
            "category": r.category.value,
            "department": r.reporting_department,
            "created_at": r.created_at,
            "tags": r.tags,
        }
        for r in records
    ]


def submit_to_decision_congress(
    command: str,
    target_department: str = "",
    command_type: str = "regular",
    context: str = "",
    auto_record_to_library: bool = True,
) -> Dict[str, Any]:
    """
    v1.0.0新增: 向七人决策代表大会提交皇帝命令。

    代表大会将进行投票决策（4票通过），投票结果自动记录到藏书阁。

    Args:
        command: 皇帝命令内容
        target_department: 目标执行部门
        command_type: "regular"(常规) / "major"(重大) / "urgent"(紧急·先执行后补审) / "imperial_edict"(圣旨·绕过)
        context: 命令上下文
        auto_record_to_library: 是否自动将投票结果提交到藏书阁（默认True）

    Returns:
        投票结果字典
    """
    try:
        from ._decision_congress import get_decision_congress
    except ImportError:
        return {"error": "DecisionCongress not available", "passed": False}

    congress = get_decision_congress()
    result = congress.submit_imperial_command(
        command=command,
        target_department=target_department,
        command_type=command_type,
        context=context,
    )

    # 圣旨不记录到藏书阁（已是最高意志）
    if command_type == "imperial_edict":
        return result

    # 紧急决策不立即记录，等补审后再记录
    if command_type == "urgent":
        return result

    # 自动将投票结果提交到藏书阁
    if auto_record_to_library:
        library_result = submit_to_imperial_library(
            title=f"代表大会投票记录: {command[:50]}",
            content=(
                f"命令: {command}\n"
                f"目标部门: {target_department}\n"
                f"命令类型: {command_type}\n"
                f"结果: {result['result']}\n"
                f"赞成票: {result['approve_count']}/{len(result['votes'])}\n"
                f"投票详情:\n"
                + "\n".join(
                    f"  - {v['voter']}: {'赞成' if v['approved'] else '反对'} ({v['reason']})"
                    for v in result["votes"]
                )
            ),
            source="代表大会投票记录",
            category="架构决策",
            reporting_department="七人决策代表大会",
            tags=["代表大会", "投票", command_type],
            metadata={"cmd_id": result.get("cmd_id", ""), "result": result["result"]},
        )
        result["library_record"] = library_result

    return result


def retroactive_review_urgent_command(
    cmd_id: str, execution_result: str = "", success: bool = True
) -> Dict[str, Any]:
    """
    v2.0新增: 紧急决策追溯性审核。

    紧急命令先执行后补审，执行完毕后调用此接口进行回溯投票。
    """
    try:
        from ._decision_congress import get_decision_congress
    except ImportError:
        return {"error": "DecisionCongress not available"}

    return get_decision_congress().retroactive_review(cmd_id, execution_result, success)


def get_congress_global_report() -> Dict[str, Any]:
    """
    v2.0新增: 获取七人决策代表大会全局执行情况报告。

    用于月度/按需向皇帝汇报。
    """
    try:
        from ._decision_congress import get_decision_congress
    except ImportError:
        return {"error": "DecisionCongress not available"}
    return get_decision_congress().generate_global_report()


def get_daqin_metrics_status(owner: str, quarter: str) -> Dict[str, Any]:
    """
    v1.0.0新增: 获取某成员的大秦指标状态。

    Args:
        owner: 成员名称
        quarter: 季度（如"2026-Q2"）

    Returns:
        指标状态字典
    """
    try:
        from ._daqin_metrics import DaqinMetricsEngine
    except ImportError:
        return {"error": "DaqinMetricsEngine not available"}

    engine = DaqinMetricsEngine()
    return engine.get_owner_status(owner, quarter)


def submit_daqin_evaluation(
    owner: str, quarter: str,
    self_score: float = 0, manager_score: float = 0, peer_score: float = 0,
    manager_feedback: str = "", improvement_plan: str = "",
    auto_record_to_library: bool = True,
) -> Dict[str, Any]:
    """
    v1.0.0新增: 提交大秦指标季度评估。

    评估结果自动记录到藏书阁。

    Args:
        owner: 成员名称
        quarter: 季度
        self_score/manager_score/peer_score: 三维评分
        manager_feedback: 主管反馈
        improvement_plan: 改进计划
        auto_record_to_library: 是否自动记录到藏书阁

    Returns:
        评估结果字典
    """
    try:
        from ._daqin_metrics import DaqinMetricsEngine
    except ImportError:
        return {"error": "DaqinMetricsEngine not available"}

    engine = DaqinMetricsEngine()
    evaluation = engine.submit_evaluation(
        owner=owner, quarter=quarter,
        self_score=self_score, manager_score=manager_score, peer_score=peer_score,
        manager_feedback=manager_feedback, improvement_plan=improvement_plan,
    )
    result = evaluation.get_evaluation_result()

    # 自动记录到藏书阁
    if auto_record_to_library:
        library_result = submit_to_imperial_library(
            title=f"大秦指标评估: {owner} ({quarter})",
            content=(
                f"成员: {owner}\n"
                f"季度: {quarter}\n"
                f"自评: {result['self_score']}\n"
                f"主管评: {result['manager_score']}\n"
                f"互评: {result['peer_score']}\n"
                f"综合分: {result['final_score']}\n"
                f"结果: {result['result']}\n"
                f"主管反馈: {result['feedback']}"
            ),
            source="部门工作结果",
            category="人才画像",
            reporting_department="大秦指标考核系统",
            tags=["大秦指标", "评估", quarter, owner],
            metadata={"owner": owner, "quarter": quarter, "final_score": result["final_score"]},
        )
        result["library_record"] = library_result

    return result


def execute_whip_scan(
    quarter: str = "",
    auto_record_to_library: bool = True,
) -> Dict[str, Any]:
    """
    v1.0.0新增: 执行行政之鞭全系统效能扫描。

    从大秦指标引擎获取全员进度数据，评估信号灯，
    生成鞭策令。结果自动记录到藏书阁。

    Args:
        quarter: 季度（如"2026-Q2"），空则扫描全部季度
        auto_record_to_library: 是否自动记录到藏书阁

    Returns:
        扫描结果（含信号灯分布、鞭策令列表）
    """
    try:
        from ._whip_engine import WhipEngine, WhipTarget, KRProgress, WhipTier
        from ._daqin_metrics import DaqinMetricsEngine
    except ImportError as e:
        return {"error": f"Module not available: {e}"}

    metrics_engine = DaqinMetricsEngine()
    whip_engine = WhipEngine()

    # 从大秦指标获取全量数据
    all_sets = metrics_engine._metrics_sets.values()
    if quarter:
        all_sets = [s for s in all_sets if s.quarter == quarter]

    if not all_sets:
        return {"error": f"未找到大秦指标数据（quarter={quarter or '全部'}）"}

    # 构建 WhipTarget 和 KRProgress
    targets = []
    metrics_data = {}
    for ms in all_sets:
        # 估算品级和部门（基于 MetricsLevel）
        tier_map = {
            "帝国级": WhipTier.HIGH,
            "系统级": WhipTier.HIGH,
            "部门级": WhipTier.MEDIUM,
            "个人级": WhipTier.BASE,
        }
        target = WhipTarget(
            name=ms.owner,
            department=ms.objectives[0].department if ms.objectives else "",
            pin_rank=ms.level.value,
            tier=tier_map.get(ms.level.value, WhipTier.BASE),
        )
        targets.append(target)

        # 提取KR进度
        kr_list = []
        for obj in ms.objectives:
            for kr in obj.krs:
                # 计算速度比（简化：score / 期望进度）
                days_in_quarter = 45  # 默认季度中间
                expected_progress = days_in_quarter / 90  # 季度天数
                speed_ratio = kr.score / expected_progress if expected_progress > 0 else kr.score
                kr_list.append(KRProgress(
                    kr_id=kr.kr_id,
                    description=kr.description,
                    target_value=kr.target_value,
                    current_value=kr.current_value,
                    score=kr.score,
                    speed_ratio=min(speed_ratio, 2.0),
                    days_in_quarter=days_in_quarter,
                ))
        if kr_list:
            metrics_data[ms.owner] = kr_list

    # 执行扫描
    scan_results = whip_engine.scan_all_targets(targets, metrics_data)

    # 获取看板
    dashboard = whip_engine.get_whip_dashboard()

    result = {
        "targets_scanned": len(targets),
        "dashboard": dashboard,
        "actions": scan_results,
    }

    # 记录到藏书阁
    if auto_record_to_library and scan_results:
        action_summary = "\n".join(
            f"  - {a.get('type', '')}: {a.get('target', '')} ({a.get('message', '')[:80]})"
            for a in scan_results[:20]
        )
        library_result = submit_to_imperial_library(
            title=f"行政之鞭效能扫描 ({quarter or '全部'})",
            content=(
                f"扫描目标数: {len(targets)}\n"
                f"信号灯分布: {dashboard['signal_distribution']}\n"
                f"活跃鞭策令: {dashboard['active_orders']}\n"
                f"执行动作:\n{action_summary}"
            ),
            source="部门工作结果",
            category="执行日志",
            reporting_department="锦衣卫·效能司",
            tags=["行政之鞭", "效能扫描", quarter or "全部"],
            metadata={
                "targets_scanned": len(targets),
                "signal_distribution": dashboard["signal_distribution"],
            },
        )
        result["library_record"] = library_result

    return result


def get_imperial_library_stats() -> Dict[str, Any]:
    """
    v1.0.0新增: 获取皇家藏书阁统计信息。
    """
    try:
        from ._imperial_library import get_imperial_library
    except ImportError:
        return {"error": "ImperialLibrary not available"}
    return get_imperial_library().get_stats()


def get_decision_congress_stats() -> Dict[str, Any]:
    """
    v1.0.0新增: 获取七人决策代表大会统计信息。
    """
    try:
        from ._decision_congress import get_decision_congress
    except ImportError:
        return {"error": "DecisionCongress not available"}
    return get_decision_congress().get_stats()


def get_daqin_metrics_dashboard(quarter: str) -> Dict[str, Any]:
    """
    v1.0.0新增: 获取大秦指标季度看板。
    """
    try:
        from ._daqin_metrics import DaqinMetricsEngine
    except ImportError:
        return {"error": "DaqinMetricsEngine not available"}
    return DaqinMetricsEngine().get_dashboard(quarter)


def get_whip_dashboard() -> Dict[str, Any]:
    """
    v1.0.0新增: 获取行政之鞭看板。
    """
    try:
        from ._whip_engine import WhipEngine
    except ImportError:
        return {"error": "WhipEngine not available"}
    return WhipEngine().get_whip_dashboard()
