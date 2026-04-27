"""
方法论检查器 v1.0
================
确保每个分析都遵守方法论纪律

功能：
- 诊断清单检查
- 框架前置验证
- 数据优先提醒
- 质量评分

来源：基于D:\open方法论迁移
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum


class QualityLevel(Enum):
    """质量等级"""
    EXCELLENT = "优秀"
    GOOD = "良好"
    NEEDS_IMPROVEMENT = "需改进"
    POOR = "较差"


@dataclass
class MethodCheckResult:
    """方法论检查结果"""
    passed: bool
    score: float  # 0-100
    level: QualityLevel
    issues: List[str]
    suggestions: List[str]
    passed_checks: List[str]


class MethodChecker:
    """方法论检查器"""
    
    # 诊断清单
    DIAGNOSIS_CHECKLIST = [
        "问题本质是什么？（表象 vs 根因）",
        "相关数据有哪些？",
        "利益相关方是谁？",
        "类似案例有参考吗？",
        "约束条件是什么？",
    ]
    
    # 常用框架
    FRAMEWORKS = [
        "SWOT分析",
        "波特五力",
        "4P营销",
        "AARRR漏斗",
        "用户旅程地图",
        "金字塔原理",
        "MECE法则",
        "二八法则",
    ]
    
    def __init__(self):
        self.checks_done: Set[str] = set()
    
    def check_diagnosis(self, context: str = "") -> MethodCheckResult:
        """检查诊断阶段"""
        issues = []
        suggestions = []
        passed_checks = []
        
        # 检查是否有诊断关键词
        diagnosis_keywords = ["诊断", "分析", "现状", "问题", "原因"]
        has_diagnosis = any(kw in context.lower() for kw in diagnosis_keywords)
        
        if has_diagnosis:
            passed_checks.append("✓ 已进入诊断阶段")
        else:
            issues.append("⚠️ 未明确进入诊断阶段")
            suggestions.append("建议先进行问题诊断，再给出方案")
        
        return MethodCheckResult(
            passed=has_diagnosis,
            score=50 if not has_diagnosis else 80,
            level=QualityLevel.NEEDS_IMPROVEMENT if not has_diagnosis else QualityLevel.GOOD,
            issues=issues,
            suggestions=suggestions,
            passed_checks=passed_checks
        )
    
    def check_framework(self, response: str) -> MethodCheckResult:
        """检查框架使用"""
        issues = []
        suggestions = []
        passed_checks = []
        
        # 检查是否使用了框架
        frameworks_used = []
        for fw in self.FRAMEWORKS:
            if fw in response:
                frameworks_used.append(fw)
        
        if frameworks_used:
            passed_checks.append(f"✓ 使用了框架: {', '.join(frameworks_used)}")
            score = 90
            level = QualityLevel.EXCELLENT
        else:
            issues.append("⚠️ 未检测到框架分析")
            suggestions.append(f"建议使用以下框架之一: {', '.join(self.FRAMEWORKS[:3])}")
            score = 40
            level = QualityLevel.POOR
        
        return MethodCheckResult(
            passed=bool(frameworks_used),
            score=score,
            level=level,
            issues=issues,
            suggestions=suggestions,
            passed_checks=passed_checks
        )
    
    def check_data_priority(self, response: str) -> MethodCheckResult:
        """检查数据优先"""
        issues = []
        suggestions = []
        passed_checks = []
        
        # 检查数据相关关键词
        data_keywords = ["数据", "根据", "显示", "统计", "分析", "指标", "比例", "%"]
        weak_phrases = ["我觉得", "大概", "可能", "也许", "估计", "应该"]
        
        data_count = sum(1 for kw in data_keywords if kw in response.lower())
        weak_count = sum(1 for ph in weak_phrases if ph in response.lower())
        
        if data_count >= 3:
            passed_checks.append("✓ 有足够的数据支撑")
            score = 90
            level = QualityLevel.EXCELLENT
        elif data_count >= 1 and weak_count <= 1:
            passed_checks.append("✓ 有一定数据支撑")
            score = 70
            level = QualityLevel.GOOD
        elif weak_count >= 2:
            issues.append("⚠️ 使用了模糊表述")
            suggestions.append("用具体数据替代'我觉得'、'大概'等模糊表述")
            score = 50
            level = QualityLevel.NEEDS_IMPROVEMENT
        else:
            issues.append("⚠️ 数据支撑不足")
            suggestions.append("补充具体数据或说明数据来源")
            score = 40
            level = QualityLevel.POOR
        
        return MethodCheckResult(
            passed=data_count >= 1,
            score=score,
            level=level,
            issues=issues,
            suggestions=suggestions,
            passed_checks=passed_checks
        )
    
    def check_logic(self, response: str) -> MethodCheckResult:
        """检查逻辑性"""
        issues = []
        suggestions = []
        passed_checks = []
        
        # 检查逻辑连接词
        logic_keywords = ["因为", "所以", "因此", "导致", "由于", "然而", "但是", "虽然"]
        has_logic = any(kw in response for kw in logic_keywords)
        
        # 检查结论标志
        conclusion_keywords = ["结论", "建议", "方案", "总之", "综上所述"]
        has_conclusion = any(kw in response for kw in conclusion_keywords)
        
        if has_logic and has_conclusion:
            passed_checks.append("✓ 有清晰的逻辑推导")
            score = 85
            level = QualityLevel.GOOD
        elif has_logic:
            passed_checks.append("✓ 有逻辑连接")
            score = 70
            level = QualityLevel.GOOD
        else:
            issues.append("⚠️ 逻辑连接不明显")
            suggestions.append("使用'因为...所以...'等逻辑连接词")
            score = 50
            level = QualityLevel.NEEDS_IMPROVEMENT
        
        return MethodCheckResult(
            passed=has_logic,
            score=score,
            level=level,
            issues=issues,
            suggestions=suggestions,
            passed_checks=passed_checks
        )
    
    def check_analogy(self, response: str) -> MethodCheckResult:
        """检查举一反三"""
        issues = []
        suggestions = []
        passed_checks = []
        
        # 检查类比关键词
        analogy_keywords = ["类似", "如同", "就像", "相当于", "举一反三", "类比"]
        has_analogy = any(kw in response for kw in analogy_keywords)
        
        # 检查反面思考
        contrary_keywords = ["但是", "然而", "反过来说", "不过", "另一方面"]
        has_contrary = any(kw in response for kw in contrary_keywords)
        
        if has_analogy and has_contrary:
            passed_checks.append("✓ 有类比和反面思考")
            score = 95
            level = QualityLevel.EXCELLENT
        elif has_analogy or has_contrary:
            passed_checks.append("✓ 有多角度思考")
            score = 75
            level = QualityLevel.GOOD
        else:
            issues.append("⚠️ 缺少多角度思考")
            suggestions.append("添加类比或反面观点")
            score = 50
            level = QualityLevel.NEEDS_IMPROVEMENT
        
        return MethodCheckResult(
            passed=has_analogy or has_contrary,
            score=score,
            level=level,
            issues=issues,
            suggestions=suggestions,
            passed_checks=passed_checks
        )
    
    def full_check(self, response: str, context: str = "") -> Dict:
        """完整方法论检查"""
        results = {
            "diagnosis": self.check_diagnosis(context),
            "framework": self.check_framework(response),
            "data": self.check_data_priority(response),
            "logic": self.check_logic(response),
            "analogy": self.check_analogy(response),
        }
        
        # 计算总分
        total_score = sum(r.score for r in results.values()) / len(results)
        
        # 确定等级
        if total_score >= 85:
            level = QualityLevel.EXCELLENT
        elif total_score >= 70:
            level = QualityLevel.GOOD
        elif total_score >= 50:
            level = QualityLevel.NEEDS_IMPROVEMENT
        else:
            level = QualityLevel.POOR
        
        return {
            "overall_score": round(total_score, 1),
            "level": level.value,
            "checks": results,
            "summary": self._generate_summary(results, total_score)
        }
    
    def _generate_summary(self, results: Dict, score: float) -> str:
        """生成检查摘要"""
        lines = ["📋 方法论检查结果", "=" * 30]
        
        for name, result in results.items():
            status = "✅" if result.passed else "❌"
            lines.append(f"{status} {name}: {result.score:.0f}分")
        
        lines.append("")
        lines.append(f"总分: {score:.0f}/100 ({results['diagnosis'].level.value})")
        
        return "\n".join(lines)


# 全局实例
_checker: Optional[MethodChecker] = None

def get_method_checker() -> MethodChecker:
    """获取方法论检查器单例"""
    global _checker
    if _checker is None:
        _checker = MethodChecker()
    return _checker


def check_response(response: str, context: str = "") -> Dict:
    """快速检查响应"""
    checker = get_method_checker()
    return checker.full_check(response, context)


if __name__ == "__main__":
    # 测试
    checker = MethodChecker()
    
    test_response = """
    根据数据分析（CTR=2.3%, 转化率=4.5%），当前问题主要是：
    
    1. 诊断：落地页与广告创意不匹配
    2. 框架：使用AARRR漏斗分析，Activation环节流失严重
    3. 类比：就像实体店的门脸和店内装修风格不一致
    4. 建议：优化落地页内容，使其与广告承诺一致
    
    但是需要注意，反过来说，也可能是流量质量问题。
    """
    
    result = checker.full_check(test_response, "广告投放效果分析")
    print(result["summary"])
