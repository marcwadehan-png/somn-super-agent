"""
智慧引擎unified调度器包 V11.0.0
神之架构V4 - 全贤就位，百官齐备
模块结构:
- _dispatch_enums.py   : 枚举与数据结构
- _dispatch_mapping.py : 初始化+引擎注册+问题-学派映射矩阵
- _dispatch_recommend.py: 问题识别+学派推荐（v10.0 全学派覆盖）
- _dispatch_fusion.py  : 融合决策+评分+单例（v8.0 全学派覆盖）
- _dispatch_court.py   : 神之架构·部门调度层（v1.0.0 皇家藏书阁Department枚举）
- _hanlin_review.py    : v3.2 翰林院决策审核模块
- _imperial_library.py      : V1.0.0 皇家藏书阁·Somn全局记忆中心（格子化）
- _library_upgrade_center.py : V1.0.0 藏书阁智能升级中枢（V1.0 自迭代引擎）
- _decision_congress.py      : v1.0 七人决策代表大会（圣旨/紧急/Cloning投票）
- _daqin_metrics.py    : v3.3 大秦指标考核引擎
- _whip_engine.py      : v3.3 行政之鞭引擎
"""

from ._dispatch_enums import (
    WisdomSchool,
    ProblemType,
    SubSchool,
    SUBSCHOOL_PARENT,
    WisdomRecommendation,
    FusionDecision,
)

# 导入子模块函数（用于绑定到 WisdomDispatcher）
from ._dispatch_mapping import WisdomDispatcher as _WDMapping
# 导出 WisdomDispatcher 名字（_WDMapping用于内部绑定）
WisdomDispatcher = _WDMapping
from ._dispatch_recommend import (
    identify_problem_type,
    get_recommended_schools,
    get_wisdom_recommendation,
)
from ._dispatch_fusion import (
    make_fusion_decision,
    get_system_status,
    get_wisdom_dispatcher,
)

# ── v1.0.0: 神之架构·部门调度导出 ──
from ._dispatch_court import (
    Department,
    DepartmentRole,
    DEPARTMENT_SCHOOL_MATRIX,
    resolve_departments,
    get_department_for_problem,
    get_all_departments_for_school,
    get_school_heatmap,
    # v3.2 新增
    get_hanlin_reviewers,
    submit_for_hanlin_review,
    should_require_hanlin_review,
    get_sage_court_info,
    resolve_positions_for_problem,
    get_practitioner_stats,
    get_full_court_stats,
    # v1.0.0 新增：集成层API
    submit_to_imperial_library,
    query_imperial_library,
    submit_to_decision_congress,
    get_daqin_metrics_status,
    submit_daqin_evaluation,
    execute_whip_scan,
    get_imperial_library_stats,
    get_decision_congress_stats,
    get_daqin_metrics_dashboard,
    get_whip_dashboard,
    # v1.0 新增：圣旨/紧急/全局报告
    retroactive_review_urgent_command,
    get_congress_global_report,
)

# ── v3.3→V1.0: 皇家藏书阁（V1.0 格子化全局记忆中心） ──
from ._imperial_library import (
    ImperialLibrary,
    MemoryGrade,
    MemorySource,
    MemoryCategory,
    MemoryRecord,
    CellRecord,
    LibraryWing,
    LibraryPermission,
    WING_SHELVES,
    WING_PERMISSIONS,
    get_imperial_library,
)

# ── V1.0: 藏书阁智能升级中枢 ────────────────────────────────────
from ._library_upgrade_center import (
    LibraryUpgradeCenter,
    get_library_upgrade_center,
    UpgradeType,
    UpgradePriority,
    UpgradeStatus,
    UpgradeResult,
    UpgradeContext,
    UpgradePlan,
    CodeChange,
    UpgradeRecord,
    SageUpgradeSuggestion,
)

from ._decision_congress import (
    DecisionCongress,
    VoteResult,
    CommandStatus,
    MemberRole,
    get_decision_congress,
    # v1.0.0 动态配置 API
    load_court_config,
    reload_court_config,
    save_runtime_override,
    get_runtime_override_path,
)

# ── v3.3: 大秦指标 + 行政之鞭 ──
from ._daqin_metrics import (
    DaqinMetricsEngine,
    MetricsLevel,
    MetricsSet,
    KeyResult,
    Objective,
    Evaluation,
    KRStatus,
    # 向后兼容别名
    OKRLevel,
    OKRSet,
    OKREngine,
)
from ._whip_engine import (
    WhipEngine,
    WhipLevel,
    WhipDirection,
    WhipStatus,
    WhipTier,
    WhipOrder,
    WhipTarget,
    WhipConfig,
    KRProgress,
    create_whip_engine,
    quick_evaluate,
)

# ── 扩展 WisdomDispatcher ──────────────────────────────────────
# 将子模块中的业务方法作为委托方法绑定到主类
# 注: 这些函数接收 self 参数（即 WisdomDispatcher 实例），
# 绑定后可作为 instance.method() 调用

from ._dispatch_recommend import (
    identify_problem_type as _identify_problem_type,
    get_recommended_schools as _get_recommended_schools,
    get_wisdom_recommendation as _get_wisdom_recommendation,
)
from ._dispatch_fusion import (
    make_fusion_decision as _make_fusion_decision,
    get_system_status as _get_system_status,
)

# V1.0.1: 子学派查询方法（实例方法，已在WisdomDispatcher类上定义，无需委托）

# 使用描述符协议替代直接猴子补丁，支持IDE补全和类型检查
class _DispatcherMethod:
    """方法委托描述符，将模块级函数绑定到 WisdomDispatcher"""
    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__qualname__ = f"WisdomDispatcher.{func.__name__}"
        self.__doc__ = func.__doc__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        import types
        return types.MethodType(self._func, obj)

_WDMapping.identify_problem_type = _DispatcherMethod(_identify_problem_type)
_WDMapping.get_recommended_schools = _DispatcherMethod(_get_recommended_schools)
_WDMapping.get_wisdom_recommendation = _DispatcherMethod(_get_wisdom_recommendation)
_WDMapping.make_fusion_decision = _DispatcherMethod(_make_fusion_decision)
_WDMapping.get_system_status = _DispatcherMethod(_get_system_status)

# ── V2.0 V1.0 V1.0: Claw路由与智能体 ───────────────────────────────
try:
    from ._dispatch_claw import (
        ClawRouter,
        ClawInfo,
        ClawRouteResult,
        get_claw_router,
        route_claw,
    )
    from ._dispatch_collaboration import (
        CollaborationProtocol,
        CollaborationRole,
        CollaborationResult,
        get_collaboration_protocol,
        collaborate_claws,
    )
    from ._dispatch_agents import (
        SomnAgent,
        AgentContext,
        AgentResult,
        ProcessStatus,
        ProblemTypeClassifier,
        get_somn_agent,
        process_query,
        process_queries,
    )
    _HAS_V4 = True
except ImportError as e:
    _HAS_V4 = False
    import logging
    logging.getLogger(__name__).warning(f"[wisdom_dispatch] V1.0模块导入失败: {e}")

__all__ = [
    # 枚举与数据结构
    'WisdomSchool',
    'ProblemType',
    'SubSchool',
    'SUBSCHOOL_PARENT',
    'WisdomRecommendation',
    'FusionDecision',
    # 核心类
    'WisdomDispatcher',
    'get_wisdom_dispatcher',
    # v1.0.0 部门调度 + 翰林院审核
    'Department',
    'DepartmentRole',
    'DEPARTMENT_SCHOOL_MATRIX',
    'resolve_departments',
    'get_department_for_problem',
    'get_all_departments_for_school',
    'get_school_heatmap',
    # v3.2 翰林院审核
    'get_hanlin_reviewers',
    'submit_for_hanlin_review',
    'should_require_hanlin_review',
    # v3.1 岗位体系
    'get_sage_court_info',
    'resolve_positions_for_problem',
    'get_practitioner_stats',
    'get_full_court_stats',
    # V1.0 藏书阁V1.0（格子化全局记忆中心）
    'ImperialLibrary',
    'MemoryGrade',
    'MemorySource',
    'MemoryCategory',
    'MemoryRecord',
    'CellRecord',
    'LibraryWing',
    'LibraryPermission',
    'WING_SHELVES',
    'WING_PERMISSIONS',
    'get_imperial_library',
    # V1.0 藏书阁智能升级中枢
    'LibraryUpgradeCenter',
    'get_library_upgrade_center',
    'UpgradeType',
    'UpgradePriority',
    'UpgradeStatus',
    'UpgradeResult',
    'UpgradeContext',
    'UpgradePlan',
    'CodeChange',
    'UpgradeRecord',
    'SageUpgradeSuggestion',
    # v3.0 七人决策代表大会（动态配置）
    'DecisionCongress',
    'VoteResult',
    'CommandStatus',
    'MemberRole',
    'get_decision_congress',
    # v3.0 动态配置 API
    'load_court_config',
    'reload_court_config',
    'save_runtime_override',
    'get_runtime_override_path',
    # v3.3 大秦指标
    'DaqinMetricsEngine',
    'MetricsLevel',
    'MetricsSet',
    'KeyResult',
    'Objective',
    'Evaluation',
    'KRStatus',
    # 向后兼容
    'OKRLevel',
    'OKRSet',
    'OKREngine',
    # v3.3 行政之鞭
    'WhipEngine',
    'WhipLevel',
    'WhipDirection',
    'WhipStatus',
    'WhipTier',
    'WhipOrder',
    'WhipTarget',
    'WhipConfig',
    'KRProgress',
    'create_whip_engine',
    'quick_evaluate',
    # v1.0.0 集成层API
    'submit_to_imperial_library',
    'query_imperial_library',
    'submit_to_decision_congress',
    'get_daqin_metrics_status',
    'submit_daqin_evaluation',
    'execute_whip_scan',
    'get_imperial_library_stats',
    'get_decision_congress_stats',
    'get_daqin_metrics_dashboard',
    'get_whip_dashboard',
    # v1.0 代表大会升级
    'retroactive_review_urgent_command',
    'get_congress_global_report',
    # V2.0 V1.0 V1.0: Claw路由与智能体
    'ClawRouter',
    'ClawInfo',
    'ClawRouteResult',
    'get_claw_router',
    'route_claw',
    'CollaborationProtocol',
    'CollaborationRole',
    'CollaborationResult',
    'get_collaboration_protocol',
    'collaborate_claws',
    'SomnAgent',
    'AgentContext',
    'AgentResult',
    'ProcessStatus',
    'ProblemTypeClassifier',
    'get_somn_agent',
    'process_query',
    'process_queries',
]
