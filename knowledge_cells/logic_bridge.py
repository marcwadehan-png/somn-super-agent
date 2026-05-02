"""
Logic 模块 → DivineReason 整合桥接模块
==========================================
将 Logic 模块的谬误检测能力接入 DivineReason，
对 DivineReason 实现升级。

整合内容（提炼自 logic/fallacy_detector/）：
  1. FallacyCategory 谬误类别（7类）
  2. FallacyDetection 谬误检测结果数据结构
  3. 核心检测函数：detect_formal_fallacies / detect_informal_fallacies
  4. 论证质量分析：analyze_argument_quality / suggest_improvements
  5. 战略咨询谬误检测（v5.1 新增）

升级 DivineReason：
  - 推理完成后自动进行谬误检测
  - 论证质量评分融入推理置信度
  - 改进建议注入推理结果
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
#  Section 1：从 Logic/FallacyDetector 提炼核心类型
# ═══════════════════════════════════════════════════════════════

class FallacyCategory(Enum):
    """谬误类别（提炼自 _fd_types.py）"""
    FORMAL = "形式谬误"
    INFORMAL = "非形式谬误"
    AMBIGUITY = "歧义谬误"
    RELEVANCE = "相关性谬误"
    PRESUMPTION = "预设谬误"
    CAUSATION = "因果谬误"
    STRATEGIC = "战略咨询谬误"  # v5.1 增长咨询专用


@dataclass
class FallacyDetection:
    """谬误检测结果（提炼自 _fd_types.py）"""
    fallacy_name: str                   # 谬误名称
    category: FallacyCategory          # 类别
    description: str                   # 描述
    severity: str                      # 严重程度（critical/major/minor）
    confidence: float                # 置信度（0.0-1.0）
    suggestion: str                   # 改进建议
    detected_at: datetime             # 检测时间


# ═══════════════════════════════════════════════════════════════
#  Section 2：懒加载 Logic 模块
# ═══════════════════════════════════════════════════════════════

_FALLACY_DETECTOR = None
_FALLACY_LOADED = False


def _get_fallacy_detector():
    """懒加载 FallacyDetector（避免启动时的重导入）"""
    global _FALLACY_DETECTOR, _FALLACY_LOADED
    if _FALLACY_LOADED:
        return _FALLACY_DETECTOR

    try:
        import sys, os
        # 将 smart_office_assistant/src 加入路径
        sa_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "smart_office_assistant", "src"
        )
        if sa_path not in sys.path:
            sys.path.append(sa_path)

        from logic.fallacy_detector import FallacyDetector
        _FALLACY_DETECTOR = FallacyDetector()
        _FALLACY_LOADED = True
        return _FALLACY_DETECTOR
    except Exception as e:
        _FALLACY_LOADED = True
        _FALLACY_DETECTOR = None
        return None


# ═══════════════════════════════════════════════════════════════
#  Section 3：整合接口 — 供 DivineReason 调用
# ═══════════════════════════════════════════════════════════════

def detect_reasoning_fallacies(reasoning_text: str) -> List[Dict]:
    """
    对推理过程进行谬误检测（供 DivineReason 调用）
    
    Args:
        reasoning_text: 推理过程文本（DivineReason 的输出）
    
    Returns:
        [{"fallacy_name": ..., "category": ..., "severity": ..., "suggestion": ...}, ...]
    """
    detector = _get_fallacy_detector()
    if detector is None:
        return []

    detections = detector.detect_informal_fallacies(reasoning_text)
    # 转换为可序列化字典
    result = []
    for d in detections:
        result.append({
            "fallacy_name": d.fallacy_name,
            "category": d.category.value if hasattr(d.category, "value") else str(d.category),
            "description": d.description,
            "severity": d.severity,
            "confidence": d.confidence,
            "suggestion": d.suggestion,
        })
    return result


def analyze_reasoning_quality(reasoning_text: str) -> Dict[str, Any]:
    """
    分析推理质量（供 DivineReason 调用）
    
    Returns:
        {"quality_score": ..., "issues": [...], "suggestions": [...], "assessment": ...}
    """
    detector = _get_fallacy_detector()
    if detector is None:
        return {"quality_score": 0.5, "issues": [], "suggestions": [], "assessment": "unknown"}

    analysis = detector.analyze_argument_quality(reasoning_text)
    return {
        "quality_score": analysis.get("quality_score", 0.5),
        "issue_count": analysis.get("issue_count", 0),
        "critical_issues": analysis.get("critical_issues", []),
        "major_issues": analysis.get("major_issues", []),
        "minor_issues": analysis.get("minor_issues", []),
        "suggestions": analysis.get("suggestions", []),
        "overall_assessment": analysis.get("overall_assessment", "unknown"),
    }


def suggest_reasoning_improvements(reasoning_text: str) -> List[str]:
    """
    生成推理改进建议（供 DivineReason 调用）
    """
    detector = _get_fallacy_detector()
    if detector is None:
        return []

    return detector.suggest_improvements(reasoning_text)


def enhance_reasoning_result(reasoning_result: Dict) -> Dict:
    """
    对 DivineReason 推理结果进行谬误增强
    
    Args:
        reasoning_result: DivineReason 的原始推理结果字典
    
    Returns:
        增强后的推理结果（新增 fallacy_check / quality_report 字段）
    """
    # 提取推理文本
    reasoning_text = ""
    if isinstance(reasoning_result, dict):
        # 尝试从结果中提取推理过程
        reasoning_text = reasoning_result.get("reasoning_process", "")
        if not reasoning_text:
            reasoning_text = reasoning_result.get("final_answer", "")
        if not reasoning_text:
            # 将整个结果转为字符串
            import json
            try:
                reasoning_text = json.dumps(reasoning_result, ensure_ascii=False, indent=2)
            except Exception:
                reasoning_text = str(reasoning_result)

    # 谬误检测
    fallacies = detect_reasoning_fallacies(reasoning_text)
    quality = analyze_reasoning_quality(reasoning_text)
    suggestions = suggest_reasoning_improvements(reasoning_text)

    # 注入结果
    enhanced = dict(reasoning_result) if isinstance(reasoning_result, dict) else {"original": reasoning_result}
    enhanced["fallacy_check"] = {
        "detected_fallacies": fallacies,
        "fallacy_count": len(fallacies),
        "critical_count": sum(1 for f in fallacies if f.get("severity") == "critical"),
        "major_count": sum(1 for f in fallacies if f.get("severity") == "major"),
    }
    enhanced["quality_report"] = quality
    enhanced["improvement_suggestions"] = suggestions

    # 修正置信度：检测到严重谬误时降低置信度
    original_confidence = enhanced.get("confidence", 0.5)
    penalty = 0.0
    for f in fallacies:
        if f.get("severity") == "critical":
            penalty += 0.15
        elif f.get("severity") == "major":
            penalty += 0.08
        elif f.get("severity") == "minor":
            penalty += 0.03
    enhanced["confidence"] = max(0.1, original_confidence - penalty)
    enhanced["fallacy_penalty_applied"] = penalty

    return enhanced


# ═══════════════════════════════════════════════════════════════
#  Section 4：DivineReason 集成包装器
# ═══════════════════════════════════════════════════════════════

class DivineReasonWithFallacyCheck:
    """
    DivineReason + 谬误检测 集成包装器
    对 DivineReason 的推理结果自动进行谬误检测和质量分析
    """
    
    def __init__(self, divine_reason_engine):
        """
        Args:
            divine_reason_engine: DivineReason 引擎实例
        """
        self._engine = divine_reason_engine
    
    def reason_with_fallacy_check(self, problem: str, **kwargs) -> Dict:
        """
        执行推理 + 谬误检测
        
        工作流程：
        1. 调用 DivineReason 进行推理
        2. 对推理过程进行谬误检测
        3. 生成质量报告
        4. 修正置信度
        5. 返回增强结果
        """
        # 1. DivineReason 推理
        result = self._engine.reason(problem, **kwargs)
        
        # 2. 谬误增强
        enhanced = enhance_reasoning_result(result)
        
        return enhanced
    
    def batch_reason_with_check(self, problems: List[str], **kwargs) -> List[Dict]:
        """批量推理 + 谬误检测"""
        results = []
        for problem in problems:
            results.append(self.reason_with_fallacy_check(problem, **kwargs))
        return results


# 模块版本
__version__ = "1.0.0"
__source__ = "Logic Module (fallacy_detector) + DivineReason 集成"
