# -*- coding: utf-8 -*-
"""
Cloning系统 - 贤者克隆引擎 v7.1.0 (延迟加载优化版)
将600+贤者的核心智慧编码为可调用的Python模块

架构:
- Tier 1: 核心独立Cloning (50人, 独立引擎模块)
- Tier 2: 学派集群Cloning (15个集群, 600+人)
- Tier 3: 五军都督府级 (100人, 领域专家)
- Tier 4: 里甲制微Cloning (按需动态生成)

v7.1.0变更: EXTRA_SAGES改为延迟加载，避免导入时实例化858+SageMeta对象

调用方式:
    from intelligence.engines.cloning import get_cloning, consult_sage

    # 获取单个Cloning
    confucius = get_cloning("孔子")
    result = confucius.analyze("如何治理一个团队")

    # 咨询学派集群
    result = consult_sage("儒家集群", "如何培养人才", method="debate")
"""

from ._cloning_types import (
    CloningTier, CloningIdentity, CloningProfile, CapabilityVector,
    WisdomLaw, AnalysisResult, DecisionResult, AdviceResult, AdviceContext,
    AssessmentResult, ClusterConsultationResult, ClusterResult,
    ConsultationMethod, SageProfile,
    DecisionOption,  # [v6.2.1] 补充导出
)
from ._cloning_base import SageCloning, SchoolCluster, Tier2ClusterCloning
from .tier1.confucius import ConfuciusCloning  # [v6.2.1] 补充导出
from ._cloning_registry import (
    get_cloning, list_clonings, list_clusters,
    consult_sage, register_cloning, get_registry_info,
    get_registry,
)

# ═══════════════════════════════════════════════════════════════════════════════
# 延迟加载：EXTRA_SAGES 及其辅助函数
# 原因：_sage_registry_extra 导入时会触发 _sage_registry_full 加载，
#       导致 858+ 个 SageMeta 数据类在模块导入时同步实例化，
#       造成显著的启动延迟（~200-500ms）。
# 改为按需加载：仅在首次访问 EXTRA_SAGES / get_all_extra_sages 时才导入。
# ═══════════════════════════════════════════════════════════════════════════════

def __getattr__(name: str):
    """延迟加载代理 — 仅在首次访问时导入重量级数据"""
    if name in ("EXTRA_SAGES", "get_all_extra_sages", "get_extra_sages_by_school"):
        from . import _sage_registry_extra as _extra
        # 将属性注入到当前模块，后续访问不再触发此函数
        globals()[name] = getattr(_extra, name)
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    # 类型
    "CloningTier", "CloningIdentity", "CloningProfile", "CapabilityVector",
    "WisdomLaw", "AnalysisResult", "DecisionResult", "AdviceResult", "AdviceContext",
    "AssessmentResult", "ClusterConsultationResult", "ClusterResult",
    "ConsultationMethod", "SageProfile",
    # 基类
    "SageCloning", "SchoolCluster", "Tier2ClusterCloning",
    # 注册表API
    "get_cloning", "list_clonings", "list_clusters",
    "consult_sage", "register_cloning", "get_registry_info", "get_registry",
    # 补充注册表API（延迟加载）
    "get_all_extra_sages", "get_extra_sages_by_school", "EXTRA_SAGES",
]
