"""
双轨架构系统 - Dual Track Architecture v3.4

A轨：神政轨 (管理监管) v3.1.0
B轨：神行轨 (执行) v5.0

实现神之架构的双轨制运行

v3.4 核心变更:
- A轨升级到 v3.1.0: 生产级资源抢占+后台持续监控+演化策略自动执行
- 生态引擎 v4.0: ResourceOptimizer 真实 psutil 资源采集+优先级抢占
- 新增 EcosystemDaemon: 后台守护线程+定时轮询+事件回调+自动响应
- EvolutionEngine: ActionEngine 自动执行策略+反馈闭环
- A轨新增 4 个公共API: start_monitoring/stop_monitoring/get_monitoring_status/get_monitoring_alerts

v3.3 核心变更:
- A轨升级到 v3.0.0: 生态引擎接入 + 系统级全局监管
- 新增 ecosystem 生态监管岗位（第5个监管Claw）
- 监管Claw系统 v2.2: 新增生态监管配置和分析模板

v3.2 核心变更 (极致轻量):
- 【最轻】import dual_track 只加载 track_a.py 一个文件 (<1ms)
- bridge / _divine_execution_bridge / track_b 全部懒加载
- __getattr__ 统一管理所有懒加载符号，透明兼容
- _supervision_claws.py 知识层共享 + 配置类级共享 + __slots__ 优化

v3.1 变更:
- track_b.py 懒加载 + _supervision_engines 共享Factory

v3.0 变更:
- Claw真实贤者 + ClawIndependentWorker
"""

from typing import Dict, Any

# ══════════════════════════════════════════════════════════════════════
# 唯一预加载: A轨核心类定义 (<1ms)
# ══════════════════════════════════════════════════════════════════════

from .track_a import DivineGovernanceTrack

# ══════════════════════════════════════════════════════════════════════
# 懒加载: 所有其他符号统一通过 __getattr__ 分发
# ══════════════════════════════════════════════════════════════════════

# 模块加载状态标记
_loaded_modules: Dict[str, bool] = {}


def _ensure_module(mod_name: str, mod_rel: str) -> Any:
    """按需加载模块并缓存，使用相对导入"""
    global _loaded_modules
    if not _loaded_modules.get(mod_name, False):
        import importlib
        _loaded_modules[mod_name] = True
        return importlib.import_module(mod_rel, __package__)
    import sys as _sys
    full_name = f"{__package__}{mod_rel}" if __package__ else mod_rel.lstrip(".")
    return _sys.modules.get(full_name)


def __getattr__(name):
    """
    统一懒加载入口

    按符号名分派到对应模块，首次访问时加载。
    对现有代码完全兼容，无需修改任何 import 语句。
    """
    # A轨懒加载符号 (bridge 模块)
    _bridge_symbols = {
        "TrackBridge",
        "DualTrackSystem",
        "create_wisdom_tree_branch_executor",
        "create_divine_reason_node_executor",
        "get_divine_execution_bridge",
        "reason_and_execute",
    }
    if name in _bridge_symbols:
        mod = _ensure_module("bridge", ".bridge")
        globals()[name] = getattr(mod, name)
        return globals()[name]

    # DivineExecutionBridge 符号
    _deb_symbols = {
        "DivineExecutionBridge",
        "ExecutableRecommendation",
        "ExecutionReport",
        "DepartmentMapper",
        "RecommendationPriority",
    }
    if name in _deb_symbols:
        mod = _ensure_module("deb", "._divine_execution_bridge")
        globals()[name] = getattr(mod, name)
        return globals()[name]

    # B轨符号 (track_b 模块)
    _track_b_symbols = {
        "DivineExecutionTrack",
        "ClawAppointmentSystem",
        "ClawAppointment",
        "KnowledgeAccessLayer",
        "CallerType",
        "TaskStatus",
        "ExecutionTask",
        "ALL_DEPARTMENTS",
    }
    if name in _track_b_symbols:
        mod = _ensure_module("track_b", ".track_b")
        globals()[name] = getattr(mod, name)
        return globals()[name]

    # 贤者协作规则符号
    _sage_collab_symbols = {
        "SageCollaborationRules",
        "ArbitrationResult",
        "CollaborationCheckResult",
        "ConflictEscalation",
        "ConflictResolution",
        "ConflictStrategy",
        "get_sage_collaboration_rules",
    }
    if name in _sage_collab_symbols:
        mod = _ensure_module("sage_collaboration_rules", ".sage_collaboration_rules")
        globals()[name] = getattr(mod, name)
        return globals()[name]

    raise AttributeError(f"module 'dual_track' has no attribute {name!r}")


def get_loading_stats() -> Dict[str, Any]:
    """获取加载性能统计"""
    return {
        "loaded_modules": list(_loaded_modules.keys()),
        "version": "v3.4",
        "governance_version": "v3.1.0",
        "execution_version": "v5.0",
        "loading_strategy": "preload_a_core_only + lazy_everything_else",
    }


def ensure_track_b_loaded() -> None:
    """预加载B轨模块（可选的主动预热）"""
    _ensure_module("track_b", ".track_b")


__all__ = [
    # A轨核心 (唯一预加载)
    "DivineGovernanceTrack",
    # 桥接器 (懒加载)
    "TrackBridge",
    "DualTrackSystem",
    "create_wisdom_tree_branch_executor",
    "create_divine_reason_node_executor",
    "get_divine_execution_bridge",
    "reason_and_execute",
    # DivineExecutionBridge (懒加载)
    "DivineExecutionBridge",
    "ExecutableRecommendation",
    "ExecutionReport",
    "DepartmentMapper",
    "RecommendationPriority",
    # B轨核心 (懒加载)
    "DivineExecutionTrack",
    "ClawAppointmentSystem",
    "ClawAppointment",
    "KnowledgeAccessLayer",
    "CallerType",
    "TaskStatus",
    "ExecutionTask",
    "ALL_DEPARTMENTS",
    # 加载工具
    "get_loading_stats",
    "ensure_track_b_loaded",
    # 贤者协作规则 (懒加载)
    "SageCollaborationRules",
    "ArbitrationResult",
    "CollaborationCheckResult",
    "ConflictEscalation",
    "ConflictResolution",
    "ConflictStrategy",
    "get_sage_collaboration_rules",
]
