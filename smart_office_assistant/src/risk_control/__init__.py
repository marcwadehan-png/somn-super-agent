"""
风险控制模块 [v21.0 延迟加载优化]
Risk Control Module - 毫秒级启动

本模块提供完整的情绪营销风险控制能力:
- 情绪健康度分析
- 合规检查
- 内容审核
- 风险案例管理

[v21.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v21.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .emotion_analyzer import EmotionHealthAnalyzer, EmotionAnalysisResult
    from .compliance_checker import ComplianceChecker
    from .content_auditor import ContentAuditor, AuditRecord, ContentPackage, AuditLevel, AuditStatus
    from .compliance_checklist import ComplianceChecklist, CheckItem, CheckResult, CheckPriority, CheckCategory
    from .risk_case_library import RiskCaseLibrary, RiskCase, RiskType, RiskLevel
    from .risk_controller import RiskController, RiskControlResult


def __getattr__(name: str) -> Any:
    """[v21.0 优化] 延迟加载 - 毫秒级启动"""

    # 情绪分析
    if name in ('EmotionHealthAnalyzer', 'EmotionAnalysisResult'):
        from . import emotion_analyzer as _m
        return getattr(_m, name)

    # 合规检查
    elif name in ('ComplianceChecker', 'ComplianceChecklist', 'CheckItem',
                  'CheckResult', 'CheckPriority', 'CheckCategory'):
        from . import compliance_checker as _m
        return getattr(_m, name)

    # 内容审核
    elif name in ('ContentAuditor', 'AuditRecord', 'ContentPackage', 'AuditLevel', 'AuditStatus'):
        from . import content_auditor as _m
        return getattr(_m, name)

    # 风险案例
    elif name in ('RiskCaseLibrary', 'RiskCase', 'RiskType', 'RiskLevel'):
        from . import risk_case_library as _m
        return getattr(_m, name)

    # 风险控制器
    elif name in ('RiskController', 'RiskControlResult'):
        from . import risk_controller as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'risk_control' has no attribute '{name}'")


__all__ = [
    # 情绪分析
    "EmotionHealthAnalyzer", "EmotionAnalysisResult",
    # 合规检查
    "ComplianceChecker", "ComplianceChecklist", "CheckItem",
    "CheckResult", "CheckPriority", "CheckCategory",
    # 内容审核
    "ContentAuditor", "AuditRecord", "ContentPackage", "AuditLevel", "AuditStatus",
    # 风险案例
    "RiskCaseLibrary", "RiskCase", "RiskType", "RiskLevel",
    # 风险控制器
    "RiskController", "RiskControlResult",
]

__version__ = "21.0.0"
