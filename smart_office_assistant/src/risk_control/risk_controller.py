"""
__all__ = [
    'batch_evaluate',
    'check_content',
    'evaluate',
    'get_summary_report',
]

风险控制器 - Risk Controller

整合所有风险检测模块,提供unified的风险控制接口
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from .emotion_analyzer import EmotionHealthAnalyzer, RiskLevel
from .compliance_checker import ComplianceChecker, ComplianceLevel

class FinalRiskLevel(Enum):
    """最终风险等级 - 风控放宽后"""
    APPROVED = "通过"           # 可直接发布
    APPROVED_WITH_WARNING = "通过(有警告)"  # 可通过但建议优化
    NEEDS_REVIEW = "需审核"     # 需要人工审核
    REJECTED = "拒绝"           # 禁止发布
    SAFE = "安全"               # P4级 - 夸张修辞允许

@dataclass
class RiskControlResult:
    """风险控制结果"""
    final_level: FinalRiskLevel
    passed: bool
    emotion_result: Dict
    compliance_result: Dict
    overall_score: float
    blocking_issues: List[Dict]
    warnings: List[Dict]
    recommendations: List[str]

class RiskController:
    """风险控制器"""
    
    def __init__(self):
        self.emotion_analyzer = EmotionHealthAnalyzer()
        self.compliance_checker = ComplianceChecker()
        
        # 风险阈值配置
        self.thresholds = {
            "emotion_health_min": 60,      # 情绪健康度最低要求
            "compliance_score_min": 70,     # 合规分数最低要求
        }
    
    def evaluate(self, content: str, context: Optional[Dict] = None) -> RiskControlResult:
        """
        评估内容风险
        
        Args:
            content: 待评估的内容
            context: 可选的上下文信息,可包含 industry 字段指定行业类型
            
        Returns:
            RiskControlResult: 风险控制结果
        """
        context = context or {}
        industry = context.get("industry", "general")
        
        # 执行各项检查
        emotion_result = self.emotion_analyzer.analyze(content)
        compliance_result = self.compliance_checker.check(content, industry)
        
        # 计算synthesize评分
        overall_score = self._calculate_overall_score(
            emotion_result.health_score,
            compliance_result.score
        )
        
        # 确定最终风险等级
        final_level = self._determine_final_level(
            emotion_result.risk_level,
            compliance_result.level
        )
        
        # 整理问题列表
        blocking_issues, warnings = self._categorize_issues(
            emotion_result, compliance_result
        )
        
        # generate建议
        recommendations = self._generate_recommendations(
            emotion_result, compliance_result, final_level
        )
        
        return RiskControlResult(
            final_level=final_level,
            passed=final_level in [FinalRiskLevel.APPROVED, FinalRiskLevel.APPROVED_WITH_WARNING, FinalRiskLevel.SAFE],
            emotion_result={
                "health_score": emotion_result.health_score,
                "risk_level": emotion_result.risk_level.value,
                "anxiety_score": emotion_result.anxiety_score,
                "fear_score": emotion_result.fear_score,
                "solution_focus": emotion_result.solution_focus,
                "hope_score": emotion_result.hope_score,
                "detected_issues": emotion_result.detected_issues,
                "suggestions": emotion_result.suggestions
            },
            compliance_result={
                "score": compliance_result.score,
                "level": compliance_result.level.value,
                "privacy_violations": compliance_result.privacy_violations,
                "discrimination_violations": compliance_result.discrimination_violations,
                "legal_violations": compliance_result.legal_violations,
                "advertising_violations": compliance_result.advertising_violations,
                "falsifiability_violations": compliance_result.falsifiability_violations,
                "suggestions": compliance_result.suggestions
            },
            overall_score=overall_score,
            blocking_issues=blocking_issues,
            warnings=warnings,
            recommendations=recommendations
        )
    
    def _calculate_overall_score(self, emotion_score: float, 
                                 compliance_score: float) -> float:
        """计算synthesize风险评分"""
        # 合规权重更高
        return emotion_score * 0.4 + compliance_score * 0.6
    
    def _determine_final_level(self, emotion_risk: RiskLevel,
                               compliance_level: ComplianceLevel) -> FinalRiskLevel:
        """确定最终风险等级 - 风控放宽后"""
        # P0级或严重违规 = 拒绝(仅安全/质量/功效虚假声明)
        if emotion_risk == RiskLevel.P0 or compliance_level == ComplianceLevel.SEVERE:
            return FinalRiskLevel.REJECTED
        
        # P1级或违规 = 需审核
        if emotion_risk == RiskLevel.P1 or compliance_level == ComplianceLevel.VIOLATION:
            return FinalRiskLevel.NEEDS_REVIEW
        
        # P2级或警告 = 通过但有警告
        if emotion_risk == RiskLevel.P2 or compliance_level == ComplianceLevel.WARNING:
            return FinalRiskLevel.APPROVED_WITH_WARNING
        
        # P4级 = 安全(夸张修辞允许)
        if emotion_risk == RiskLevel.P4:
            return FinalRiskLevel.SAFE
        
        # 其他 = 通过
        return FinalRiskLevel.APPROVED
    
    def _categorize_issues(self, emotion_result, compliance_result):
        """分类整理问题"""
        blocking_issues = []
        warnings = []
        
        # 情绪相关问题
        for issue in emotion_result.detected_issues:
            if issue["level"] == "P1":
                blocking_issues.append({
                    "type": "情绪健康",
                    "level": "P1",
                    "description": issue["description"],
                    "keywords": issue.get("keywords", [])
                })
            else:
                warnings.append({
                    "type": "情绪健康",
                    "level": issue["level"],
                    "description": issue["description"]
                })
        
        # 合规相关问题
        for violation in (compliance_result.privacy_violations + 
                         compliance_result.legal_violations):
            if violation.get("level") == "P0":
                blocking_issues.append({
                    "type": "合规",
                    "level": "P0",
                    "description": violation["description"],
                    "action": violation["action"]
                })
            else:
                warnings.append({
                    "type": "合规",
                    "level": violation.get("level", "P1"),
                    "description": violation["description"]
                })
        
        # 歧视和广告违规作为警告
        for violation in (compliance_result.discrimination_violations + 
                         compliance_result.advertising_violations):
            warnings.append({
                "type": "合规",
                "level": "P1",
                "description": violation["description"]
            })
        
        return blocking_issues, warnings
    
    def _generate_recommendations(self, emotion_result, compliance_result,
                                  final_level: FinalRiskLevel) -> List[str]:
        """generatesynthesize建议"""
        recommendations = []
        
        # 检查是否有政治内容违规
        political_violations = [
            v for v in compliance_result.legal_violations
            if v.get("subtype") in ["政治敏感", "政治点评", "政治人物"]
        ]
        
        if political_violations:
            recommendations.append("🔴 [政治内容红线]内容涉及政治敏感话题,绝对禁止发布")
            recommendations.append("   仅允许传播客观存在的政策制度,禁止任何形式的点评")
        elif final_level == FinalRiskLevel.REJECTED:
            recommendations.append("🔴 内容存在严重违规(安全/质量/功效虚假声明),必须修改后才能发布")
        elif final_level == FinalRiskLevel.NEEDS_REVIEW:
            recommendations.append("🟠 内容需要人工审核,请提交审核流程")
        elif final_level == FinalRiskLevel.APPROVED_WITH_WARNING:
            recommendations.append("🟡 内容可以通过,但建议根据警告项进行优化")
        elif final_level == FinalRiskLevel.SAFE:
            recommendations.append("⚪ 内容使用夸张修辞,属于正常营销表达,可以发布")
        else:
            recommendations.append("🟢 内容健康合规,可以发布")
        
        # 添加具体建议
        if emotion_result.health_score < 80:
            recommendations.append(f"情绪健康度{emotion_result.health_score:.1f}分,建议提升至80分以上")
        
        if compliance_result.score < 90:
            recommendations.append(f"合规分数{compliance_result.score:.1f}分,建议优化合规性")
        
        return recommendations
    
    def batch_evaluate(self, contents: List[str]) -> List[RiskControlResult]:
        """批量评估"""
        return [self.evaluate(content) for content in contents]
    
    def get_summary_report(self, results: List[RiskControlResult]) -> Dict:
        """generate评估汇总报告"""
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        rejected = sum(1 for r in results if r.final_level == FinalRiskLevel.REJECTED)
        needs_review = sum(1 for r in results if r.final_level == FinalRiskLevel.NEEDS_REVIEW)
        with_warning = sum(1 for r in results if r.final_level == FinalRiskLevel.APPROVED_WITH_WARNING)
        
        avg_score = sum(r.overall_score for r in results) / total if total > 0 else 0
        
        return {
            "total": total,
            "passed": passed,
            "rejected": rejected,
            "needs_review": needs_review,
            "with_warning": with_warning,
            "pass_rate": passed / total * 100 if total > 0 else 0,
            "average_score": avg_score,
            "risk_distribution": {
                "通过": passed - with_warning,
                "通过(有警告)": with_warning,
                "需审核": needs_review,
                "拒绝": rejected
            }
        }

# 便捷函数
def check_content(content: str) -> Dict:
    """
    快速检查内容风险
    
    Args:
        content: 待检查的内容
        
    Returns:
        检查结果字典
    """
    controller = RiskController()
    result = controller.evaluate(content)
    
    return {
        "passed": result.passed,
        "level": result.final_level.value,
        "overall_score": result.overall_score,
        "blocking_issues_count": len(result.blocking_issues),
        "warnings_count": len(result.warnings),
        "recommendations": result.recommendations
    }
