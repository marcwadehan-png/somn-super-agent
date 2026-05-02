"""
Risk Control + Security → RefuteCore 整合桥接模块
==================================================

将 risk_control 和 security 模块的有价值内容接入 RefuteCore，
对 RefuteCore 实现升级。

整合内容（提炼自 risk_control/ 和 security/）：
  1. EmotionHealthAnalyzer 情绪健康度分析（增强 EMOTION 维度）
  2. ComplianceChecker 合规检查（新增 COMPLIANCE 维度）
  3. RiskController 风险评估（新增 RISK 维度）
  4. DefenseDepth 多 layer 防御（新增 SECURITY 维度）
  5. DataObfuscation 数据脱敏（隐私保护）

升级 RefuteCore：
  - 新增 RISK / COMPLIANCE / SECURITY 三个论证维度
  - 增强 EMOTION 维度（情绪健康度分析）
  - 论证结果自动进行风险评分和合规检查
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
#  Section 1：从 Risk Control / Security 提炼核心类型
# ═══════════════════════════════════════════════════════════════

class RiskDimension(Enum):
    """风险维度枚举（新增 — 用于 RefuteCore 论证分析）"""
    RISK = "risk"                     # 风险评估
    COMPLIANCE = "compliance"         # 合规检查
    SECURITY = "security"             # 论证安全性
    EMOTION_HEALTH = "emotion_health"  # 情绪健康度


@dataclass
class RiskAssessment:
    """风险评估结果"""
    dimension: RiskDimension
    risk_score: float              # 风险评分 0-100
    risk_level: str                # low / medium / high / critical
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ComplianceCheck:
    """合规检查结果"""
    is_compliant: bool
    compliance_score: float         # 0-100
    level: str                    # compliant / warning / violation / severe
    privacy_violations: List[str] = field(default_factory=list)
    discrimination_violations: List[str] = field(default_factory=list)
    legal_violations: List[str] = field(default_factory=list)
    advertising_violations: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class SecurityAssessment:
    """安全评估结果"""
    threat_level: str               # safe / low / medium / high / critical
    defense_score: float           # 防御评分 0-100
    passed_layers: int = 0
    total_layers: int = 5
    blocked: bool = False
    block_reason: str = ""


# ═══════════════════════════════════════════════════════════════
#  Section 2：懒加载 Risk Control + Security 模块
# ═══════════════════════════════════════════════════════════════

_RISK_SECURITY_LOADED: bool = False
_RISK_CONTROLLER = None
_COMPLIANCE_CHECKER = None
_DEFENSE_DEPTH = None


def _get_risk_controller():
    """懒加载 RiskController"""
    global _RISK_CONTROLLER, _RISK_SECURITY_LOADED
    if _RISK_CONTROLLER is not None:
        return _RISK_CONTROLLER

    try:
        import sys, os
        sa_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "smart_office_assistant", "src"
        )
        if sa_path not in sys.path:
            sys.path.append(sa_path)

        from risk_control.risk_controller import RiskController
        _RISK_CONTROLLER = RiskController()
    except Exception as e:
        _RISK_CONTROLLER = None
        import logging
        logging.getLogger("Somn.RiskSecurity").warning(f"RiskController load failed: {e}")

    return _RISK_CONTROLLER


def _get_compliance_checker():
    """懒加载 ComplianceChecker"""
    global _COMPLIANCE_CHECKER
    if _COMPLIANCE_CHECKER is not None:
        return _COMPLIANCE_CHECKER

    try:
        import sys, os
        sa_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "smart_office_assistant", "src"
        )
        if sa_path not in sys.path:
            sys.path.append(sa_path)

        from risk_control.compliance_checker import ComplianceChecker
        _COMPLIANCE_CHECKER = ComplianceChecker()
    except Exception as e:
        _COMPLIANCE_CHECKER = None
        import logging
        logging.getLogger("Somn.RiskSecurity").warning(f"ComplianceChecker load failed: {e}")

    return _COMPLIANCE_CHECKER


def _get_emotion_analyzer():
    """懒加载 EmotionHealthAnalyzer"""
    try:
        import sys, os
        sa_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "smart_office_assistant", "src"
        )
        if sa_path not in sys.path:
            sys.path.append(sa_path)

        from risk_control.emotion_analyzer import EmotionHealthAnalyzer
        return EmotionHealthAnalyzer()
    except Exception as e:
        import logging
        logging.getLogger("Somn.RiskSecurity").warning(f"EmotionHealthAnalyzer load failed: {e}")
        return None


def _get_defense_depth():
    """懒加载 DefenseDepth 系统"""
    try:
        import sys, os
        sa_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "smart_office_assistant", "src"
        )
        if sa_path not in sys.path:
            sys.path.append(sa_path)

        from security.defense_depth import DefenseDepthSystem
        return DefenseDepthSystem()
    except Exception as e:
        import logging
        logging.getLogger("Somn.RiskSecurity").warning(f"DefenseDepth load failed: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
#  Section 3：整合接口 — 供 RefuteCore 调用
# ═══════════════════════════════════════════════════════════════

def assess_argument_risk(argument: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    对论证内容进行风险评估（供 RefuteCore 调用）

    Returns:
        {
            "risk_score": 0-100,
            "risk_level": "low" | "medium" | "high" | "critical",
            "emotion_health": {...},
            "compliance": {...},
            "security": {...},
            "overall_risk": float,
        }
    """
    result = {
        "risk_score": 0.0,
        "risk_level": "low",
        "emotion_health": None,
        "compliance": None,
        "security": None,
        "overall_risk": 0.0,
        "issues": [],
        "suggestions": [],
    }

    # 1. 情绪健康度分析
    emotion_analyzer = _get_emotion_analyzer()
    if emotion_analyzer:
        try:
            eh_result = emotion_analyzer.analyze(argument)
            result["emotion_health"] = {
                "health_score": eh_result.health_score,
                "risk_level": eh_result.risk_level.value if hasattr(eh_result.risk_level, "value") else str(eh_result.risk_level),
                "anxiety_score": eh_result.anxiety_score,
                "fear_score": eh_result.fear_score,
                "solution_focus": eh_result.solution_focus,
                "hope_score": eh_result.hope_score,
                "detected_issues": eh_result.detected_issues,
                "suggestions": eh_result.suggestions,
            }
            # 情绪健康度低 → 风险评分提高
            if eh_result.health_score < 60:
                result["risk_score"] += 30.0
                result["issues"].append(f"情绪健康度低: {eh_result.health_score}")
        except Exception:
            pass

    # 2. 合规检查
    compliance_checker = _get_compliance_checker()
    if compliance_checker:
        try:
            industry = (context or {}).get("industry", "general")
            cc_result = compliance_checker.check(argument, industry)
            result["compliance"] = {
                "score": cc_result.score,
                "level": cc_result.level.value if hasattr(cc_result.level, "value") else str(cc_result.level),
                "privacy_violations": cc_result.privacy_violations,
                "discrimination_violations": cc_result.discrimination_violations,
                "legal_violations": cc_result.legal_violations,
                "advertising_violations": cc_result.advertising_violations,
                "suggestions": cc_result.suggestions,
            }
            # 合规分数低 → 风险评分提高
            if cc_result.score < 70:
                result["risk_score"] += (70 - cc_result.score) * 0.5
                if cc_result.privacy_violations:
                    result["issues"].extend(cc_result.privacy_violations)
        except Exception:
            pass

    # 3. 防御深度评估（论证安全性）
    defense = _get_defense_depth()
    if defense:
        try:
            # 构建安全请求
            from security.defense_depth import SecurityRequest, ThreatLevel
            req = SecurityRequest(
                user_id=None,
                ip_address="0.0.0.0",
                user_agent="RefuteCore",
                path="/argument/check",
                method="ANALYZE",
                headers={},
                body={"argument": argument[:500]},
                timestamp=datetime.now(),
            )
            response = defense.process_request(req)
            result["security"] = {
                "allowed": response.allowed,
                "threat_level": response.threat_level.value if hasattr(response.threat_level, "value") else str(response.threat_level),
                "metadata": response.metadata,
            }
            if not response.allowed:
                result["risk_score"] += 40.0
                result["issues"].append(f"安全拦截: {response.error_message}")
        except Exception:
            pass

    # 综合风险等级
    result["risk_score"] = min(100.0, max(0.0, result["risk_score"]))
    if result["risk_score"] >= 80:
        result["risk_level"] = "critical"
    elif result["risk_score"] >= 60:
        result["risk_level"] = "high"
    elif result["risk_score"] >= 30:
        result["risk_level"] = "medium"
    else:
        result["risk_level"] = "low"

    result["overall_risk"] = result["risk_score"] / 100.0
    return result


def enhance_refute_result(refute_result: Dict) -> Dict:
    """
    对 RefuteCore 的论证/反驳结果进行风险增强

    Args:
        refute_result: RefuteCore 的原始论证/反驳结果

    Returns:
        增强后的结果（新增 risk_assessment / compliance_check / security_check 字段）
    """
    argument_text = ""
    if isinstance(refute_result, dict):
        argument_text = refute_result.get("argument", "")
        if not argument_text:
            argument_text = refute_result.get("text", "")
        if not argument_text:
            argument_text = str(refute_result)[:1000]

    # 风险评估
    risk = assess_argument_risk(argument_text)
    enhanced = dict(refute_result) if isinstance(refute_result, dict) else {"original": refute_result}

    enhanced["risk_assessment"] = risk
    enhanced["compliance_check"] = risk.get("compliance")
    enhanced["security_check"] = risk.get("security")

    # 修正置信度：高风险 → 降低置信度
    original_confidence = enhanced.get("confidence", 0.5)
    risk_penalty = risk["overall_risk"] * 0.3  # 风险最高扣 30% 置信度
    enhanced["confidence"] = max(0.1, original_confidence - risk_penalty)
    enhanced["risk_penalty_applied"] = risk_penalty

    return enhanced


def check_argument_compliance(argument: str, industry: str = "general") -> Dict:
    """
    专项合规检查（供 RefuteCore 调用）
    检查广告法禁用词、隐私信息、歧视性内容
    """
    checker = _get_compliance_checker()
    if not checker:
        return {"compliant": True, "score": 80.0, "issues": []}

    try:
        result = checker.check(argument, industry)
        return {
            "compliant": result.is_compliant,
            "score": result.score,
            "level": result.level.value if hasattr(result.level, "value") else str(result.level),
            "privacy_violations": result.privacy_violations,
            "discrimination_violations": result.discrimination_violations,
            "legal_violations": result.legal_violations,
            "advertising_violations": result.advertising_violations,
            "suggestions": result.suggestions,
        }
    except Exception as e:
        return {"compliant": True, "score": 50.0, "error": str(e)}


def analyze_emotion_health(argument: str) -> Dict:
    """
    专项情绪健康度分析（供 RefuteCore EMOTION 维度调用）
    """
    analyzer = _get_emotion_analyzer()
    if not analyzer:
        return {"health_score": 80.0, "risk_level": "low"}

    try:
        result = analyzer.analyze(argument)
        return {
            "health_score": result.health_score,
            "risk_level": result.risk_level.value if hasattr(result.risk_level, "value") else str(result.risk_level),
            "anxiety_score": result.anxiety_score,
            "fear_score": result.fear_score,
            "solution_focus": result.solution_focus,
            "hope_score": result.hope_score,
            "detected_issues": result.detected_issues,
            "suggestions": result.suggestions,
        }
    except Exception as e:
        return {"health_score": 80.0, "risk_level": "low", "error": str(e)}


# ═══════════════════════════════════════════════════════════════
#  Section 4：RefuteCore 集成包装器
# ═══════════════════════════════════════════════════════════════

class RefuteCoreWithRiskCheck:
    """
    RefuteCore + 风险/合规/安全 集成包装器
    对 RefuteCore 的论证/反驳结果自动进行风险评估
    """

    def __init__(self, refute_core_engine):
        """
        Args:
            refute_core_engine: RefuteCore 引擎实例
        """
        self._engine = refute_core_engine

    def refute_with_risk_check(self, argument: str, **kwargs) -> Dict:
        """
        执行反驳 + 风险评估

        工作流程：
        1. 调用 RefuteCore 进行反驳分析
        2. 对反驳结果进行风险评估
        3. 进行合规检查
        4. 修正置信度
        5. 返回增强结果
        """
        # 1. RefuteCore 反驳
        result = self._engine.refute(argument, **kwargs)

        # 2. 风险增强
        enhanced = enhance_refute_result(result)
        return enhanced

    def argue_with_risk_check(self, topic: str, **kwargs) -> Dict:
        """执行论证 + 风险评估"""
        result = self._engine.argue(topic, **kwargs)
        enhanced = enhance_refute_result(result)
        return enhanced


# 模块版本
__version__ = "1.0.0"
__source__ = "Risk Control + Security → RefuteCore 集成"
