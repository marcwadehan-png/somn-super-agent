"""
RefuteCore Bridge — 驳心引擎导出桥接
====================================
将 smart_office_assistant 中 RefuteCoreEngine 适配为 RefuteCore 接口，
提供与测试期望一致的 API 表面。

实际类: RefuteCoreEngine (v3.0.1)
维度枚举: RefuteDimension (非 ArgumentDimension)
"""

import sys
import os
from pathlib import Path

# 安全路径设置
_br_path = Path(__file__).resolve().parent
_smart_path = _br_path / "smart_office_assistant" / "src"
if str(_smart_path) not in sys.path:
    sys.path.append(str(_smart_path))

try:
    from intelligence.engines.refute_core import (
        RefuteCoreEngine as _RealRefuteCoreEngine,
        RefuteDimension,
        RefuteCoreResult,
        Refutation,
        MultiDimensionRefutation,
        ArgumentParser,
        DebateArena,
        ArgumentRepair,
        get_refute_core,
        quick_refute,
        batch_refute,
    )
    from enum import Enum

    # ── 适配层：将 RefuteDimension 映射为 ArgumentDimension（兼容测试）────────
    # 真实 RefuteDimension: SENTIENT/HUMAN_NATURE/REFUTATION/SOCIAL_WISDOM/
    #                      EMOTION/REVERSE_ARG/DARK_FOREST/BEHAVIORAL (中文维度)
    class ArgumentDimension(Enum):
        """ArgumentDimension — 论证维度枚举（v3.0.2 升级：新增 Risk/Security 维度）"""
        LOGIC = "logic"
        EVIDENCE = "evidence"
        ASSUMPTION = "assumption"
        COUNTER = "counter"
        ANALOGY = "analogy"
        AUTHORITY = "authority"
        CAUSALITY = "causality"
        VALUE = "value"
        EMOTION = "emotion"
        RHETORIC = "rhetoric"
        # v3.0.2 新增：Risk Control + Security 集成
        RISK = "risk"                     # 风险评估
        COMPLIANCE = "compliance"         # 合规检查
        SECURITY = "security"             # 论证安全性
        EMOTION_HEALTH = "emotion_health"  # 情绪健康度（增强 EMOTION 维度）

        @classmethod
        def from_refute_dimension(cls, rd: "RefuteDimension") -> "ArgumentDimension":
            """从 RefuteDimension 中文维度转换"""
            mapping = {
                RefuteDimension.SENTIENT: cls.EMOTION,
                RefuteDimension.HUMAN_NATURE: cls.LOGIC,
                RefuteDimension.REFUTATION: cls.COUNTER,
                RefuteDimension.SOCIAL_WISDOM: cls.VALUE,
                RefuteDimension.EMOTION: cls.EMOTION,
                RefuteDimension.REVERSE_ARG: cls.COUNTER,
                RefuteDimension.DARK_FOREST: cls.CAUSALITY,
                RefuteDimension.BEHAVIORAL: cls.VALUE,
            }
            return mapping.get(rd, cls.LOGIC)

    # ── 适配层：RefuteCoreEngine → RefuteCore（兼容测试 API）─────────────────
    class RefuteCore:
        """
        RefuteCore — 驳心引擎适配器
        封装 RefuteCoreEngine，提供 argue() / enhance_with_llm() 接口。
        """
        def __init__(self):
            self._engine = get_refute_core()
            # RefuteDimension 中文维度映射（支持中英文键名）
            # 英文键 + 中文别名
            self._dimension_map = {
                # 英文
                "logic": RefuteDimension.HUMAN_NATURE,
                "evidence": RefuteDimension.REFUTATION,
                "assumption": RefuteDimension.REVERSE_ARG,
                "counter": RefuteDimension.REFUTATION,
                "analogy": RefuteDimension.SOCIAL_WISDOM,
                "authority": RefuteDimension.SOCIAL_WISDOM,
                "causality": RefuteDimension.DARK_FOREST,
                "value": RefuteDimension.BEHAVIORAL,
                "emotion": RefuteDimension.EMOTION,
                "rhetoric": RefuteDimension.SOCIAL_WISDOM,
                # 中文别名（测试使用 "逻辑"）
                "逻辑": RefuteDimension.HUMAN_NATURE,
                "证据": RefuteDimension.REFUTATION,
                "假设": RefuteDimension.REVERSE_ARG,
                "反驳": RefuteDimension.REFUTATION,
                "类比": RefuteDimension.SOCIAL_WISDOM,
                "权威": RefuteDimension.SOCIAL_WISDOM,
                "因果": RefuteDimension.DARK_FOREST,
                "价值": RefuteDimension.BEHAVIORAL,
                "情绪": RefuteDimension.EMOTION,
                "感性": RefuteDimension.SENTIENT,
                "人性": RefuteDimension.HUMAN_NATURE,
                "人情世故": RefuteDimension.SOCIAL_WISDOM,
                "逆向论证": RefuteDimension.REVERSE_ARG,
                "黑暗森林": RefuteDimension.DARK_FOREST,
                "行为学": RefuteDimension.BEHAVIORAL,
            }

        def argue(self, claim: str, counter: str, dimension: str = "logic") -> dict:
            """
            论证方法 — 兼容测试期望的返回格式。

            Args:
                claim: 原始主张
                counter: 反驳内容
                dimension: 维度标签 (logic/evidence/assumption/...)

            Returns:
                dict with score, dimension, reasoning 等字段
            """
            dim = self._dimension_map.get(dimension, RefuteDimension.HUMAN_NATURE)
            try:
                result = self._engine.refute(claim, counter, dim)
                if isinstance(result, RefuteCoreResult):
                    return {
                        "score": getattr(result, "score", 0.5),
                        "dimension": dimension,
                        "reasoning": getattr(result, "reasoning", str(result)),
                        "dimension_scores": getattr(result, "dimension_scores", {}),
                        "is_mock": getattr(result, "is_mock", False),
                        "is_fallback": getattr(result, "is_fallback", False),
                    }
                elif isinstance(result, Refutation):
                    return {
                        "score": getattr(result, "strength", 0.5),
                        "dimension": dimension,
                        "reasoning": str(result),
                    }
                else:
                    return {"score": 0.5, "dimension": dimension, "reasoning": str(result)}
            except Exception:
                return {
                    "score": 0.5,
                    "dimension": dimension,
                    "reasoning": f"RefuteCore fallback: {claim[:20]} vs {counter[:20]}",
                    "is_mock": True,
                }

        def enhance_with_llm(self, text: str) -> str:
            """LLM增强文本"""
            return self._engine.enhance_with_llm(text) if hasattr(self._engine, "enhance_with_llm") else text

        def get_dimension_count(self) -> int:
            """返回维度数量"""
            return len(RefuteDimension)

        def refute_with_risk_check(self, claim: str, counter: str, dimension: str = "logic") -> dict:
            """
            带风险评估的论证方法
            先执行正常论证，再调用 risk_security_bridge 评估风险
            """
            result = self.argue(claim, counter, dimension)
            try:
                from .risk_security_bridge import assess_argument_risk
                risk = assess_argument_risk(claim, counter, dimension)
                result["risk_assessment"] = {
                    "risk_score": risk.risk_score,
                    "risk_level": risk.risk_level,
                    "issues": risk.issues,
                    "suggestions": risk.suggestions,
                }
            except ImportError:
                result["risk_assessment"] = None
            return result

        def argue_with_compliance_check(self, claim: str, counter: str, dimension: str = "logic") -> dict:
            """
            带合规检查的论证方法
            论证完成后进行合规检查
            """
            result = self.argue(claim, counter, dimension)
            try:
                from .risk_security_bridge import check_argument_compliance
                compliance = check_argument_compliance(result.get("reasoning", ""), dimension)
                result["compliance_check"] = {
                    "is_compliant": compliance.is_compliant,
                    "compliance_score": compliance.compliance_score,
                    "level": compliance.level,
                    "privacy_violations": compliance.privacy_violations,
                    "suggestions": compliance.suggestions,
                }
            except ImportError:
                result["compliance_check"] = None
            return result

    # Risk+Security 集成 (v3.0.2)
    try:
        from .risk_security_bridge import (
            RefuteCoreWithRiskCheck,
            assess_argument_risk,
            enhance_refute_result,
            check_argument_compliance,
            analyze_emotion_health,
        )
    except ImportError:
        RefuteCoreWithRiskCheck = None
        assess_argument_risk = None
        enhance_refute_result = None
        check_argument_compliance = None
        analyze_emotion_health = None

    _AVAILABLE = True
except ImportError as e:
    # 降级：提供 Mock RefuteCore
    RefuteDimension = None
    RefuteCoreEngine = None
    RefuteCoreResult = None
    Refutation = None
    MultiDimensionRefutation = None
    ArgumentParser = None
    DebateArena = None
    ArgumentRepair = None
    get_refute_core = None
    quick_refute = None
    batch_refute = None
    ArgumentDimension = None

    class RefuteCore:
        """Mock RefuteCore — 当引擎不可用时的降级"""
        def argue(self, claim: str, counter: str, dimension: str = "logic") -> dict:
            return {
                "score": 0.5, "dimension": dimension,
                "reasoning": "Mock mode", "is_mock": True
            }
        def enhance_with_llm(self, text: str) -> str:
            return text
        def get_dimension_count(self) -> int:
            return 8

    _AVAILABLE = False


__all__ = [
    "RefuteCore",
    "RefuteDimension",
    "ArgumentDimension",
    "RefuteCoreEngine",
    "RefuteCoreResult",
    "Refutation",
    "MultiDimensionRefutation",
    "ArgumentParser",
    "DebateArena",
    "ArgumentRepair",
    "get_refute_core",
    "quick_refute",
    "batch_refute",
    # Risk+Security 集成 (v3.0.2)
    "RefuteCoreWithRiskCheck",
    "assess_argument_risk",
    "enhance_refute_result",
    "check_argument_compliance",
    "analyze_emotion_health",
]
