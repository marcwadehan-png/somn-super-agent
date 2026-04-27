"""咨询验证器 - 核心控制器"""
import logging
from datetime import datetime
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

from ._cv_types import (
    ConsultingValidationResult,
    SeverityLevel,
)

__all__ = [
    'generate_checklist',
    'quick_check',
    'validate_full',
]
from ._cv_research import ResearchCompletenessChecker
from ._cv_reasoning import StrategicReasoningValidator
from ._cv_antipattern import AntiPatternDetector
from ._cv_scorer import SolutionQualityScorer

class ConsultingValidator:
    """
    增长咨询智能验证引擎 - 总控制器

    整合所有子模块,提供完整的方案验证能力.

    使用示例:
        validator = ConsultingValidator()

        # 验证一份方案
        result = validator.validate_full({
            'solution_name': '企业增长战略解决方案',
            'full_text': open('solution.md').read(),
            '企业自身': {...},
            '用户画像': {...},
            # ... 其他维度数据
        })

        # 查看结果
        logger.info(f"质量评分: {result.total_quality_score}/100")
        logger.info(f"调研完整性: {result.research_completeness:.0%}")
        logger.info(f"推理完整性: {result.reasoning_completeness:.0%}")
        logger.info(f"总体judge: {result.overall_verdict}")
        logger.info(f"致命问题:")
        for issue in result.critical_fixes:
            logger.info(f"  - {issue}")
    """

    def __init__(self):
        """init各子模块"""
        self.research_checker = ResearchCompletenessChecker()
        self.reasoning_validator = StrategicReasoningValidator()
        self.anti_pattern_detector = AntiPatternDetector()
        self.quality_scorer = SolutionQualityScorer()

    def validate_full(self, solution_data: Dict[str, Any]) -> ConsultingValidationResult:
        """
        执行完整的方案验证

        Args:
            solution_data: 方案数据字典,至少包含:
                - solution_name: 方案名称
                - full_text: 方案全文

        Returns:
            ConsultingValidationResult 完整验证结果
        """
        solution_name = solution_data.get('solution_name', '未命名方案')
        full_text = solution_data.get('full_text', '')

        # 1. 调研完整性检查
        research_items = self.research_checker.check(solution_data)
        research_completeness = sum(
            1 for item in research_items if item.is_present
        ) / max(1, len(research_items))

        # 2. 战略推理验证
        reasoning_result = self.reasoning_validator.validate(solution_data)
        reasoning_completeness = reasoning_result['completeness_score']

        # 3. 反模式检测
        anti_patterns = self.anti_pattern_detector.detect(solution_data)

        # 4. 质量评分
        total_score, dimension_scores = self.quality_scorer.score(solution_data)

        # 5. 汇总问题
        issues = self._collect_issues(
            research_items, reasoning_result, anti_patterns
        )

        # 6. 矛盾检测
        contradictions = reasoning_result.get('contradictions', [])

        # 7. generate总体judge
        verdict, strengths, critical_fixes = self._generate_verdict(
            total_score, research_completeness, reasoning_completeness,
            contradictions, issues, anti_patterns
        )

        return ConsultingValidationResult(
            validation_id=f"CV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            solution_name=solution_name,
            total_quality_score=total_score,
            dimension_scores=dimension_scores,
            issues=issues,
            contradictions=contradictions,
            anti_patterns=anti_patterns,
            research_completeness=research_completeness,
            reasoning_completeness=reasoning_completeness,
            overall_verdict=verdict,
            key_strengths=strengths,
            critical_fixes=critical_fixes
        )

    def _collect_issues(self, research_items, reasoning_result,
                       anti_patterns) -> List:
        """汇总所有验证问题"""
        from ._cv_types import ValidationIssue
        issues = []
        issue_id = 0

        # 调研缺失
        for item in research_items:
            if not item.is_present:
                issue_id += 1
                issues.append(ValidationIssue(
                    id=f'R-{issue_id:02d}',
                    category=f'调研缺失-{item.dimension.value}',
                    severity=SeverityLevel.MAJOR,
                    description=f"缺失'{item.item_name}'调研",
                    fix_suggestion=item.suggestion
                ))

        # 推理问题
        all_gaps = (
            reasoning_result.get('user_anchor_issues', []) +
            reasoning_result.get('bottom_up_gaps', []) +
            reasoning_result.get('stress_test_gaps', [])
        )
        for gap in all_gaps:
            issues.append(gap)

        # 反模式
        for ap in anti_patterns:
            if ap.severity in (SeverityLevel.CRITICAL, SeverityLevel.MAJOR):
                issue_id += 1
                issues.append(ValidationIssue(
                    id=f'AP-{issue_id:02d}',
                    category=f'反模式-{ap.pattern_type.value}',
                    severity=ap.severity,
                    description=ap.description,
                    evidence=ap.evidence,
                    fix_suggestion=ap.fix_suggestion
                ))

        # 按严重程度排序
        severity_order = {SeverityLevel.CRITICAL: 0, SeverityLevel.MAJOR: 1,
                         SeverityLevel.MODERATE: 2, SeverityLevel.MINOR: 3}
        issues.sort(key=lambda x: severity_order.get(x.severity, 4))

        return issues

    def _generate_verdict(self, total_score, research_completeness,
                          reasoning_completeness, contradictions,
                          issues, anti_patterns) -> Tuple[str, List[str], List[str]]:
        """generate总体judge"""
        strengths = []
        critical_fixes = []

        # 收集致命问题
        critical_issues = [
            i for i in issues if i.severity == SeverityLevel.CRITICAL
        ]
        major_issues = [
            i for i in issues if i.severity == SeverityLevel.MAJOR
        ]

        # 收集优势
        if research_completeness >= 0.8:
            strengths.append("调研覆盖全面,五维信息架构完整")
        if reasoning_completeness >= 0.8:
            strengths.append("战略推理链条完整,六步验证到位")
        if total_score >= 75:
            strengths.append("方案质量优秀,可进入执行阶段")
        if not contradictions:
            strengths.append("无核心逻辑矛盾")
        if len(anti_patterns) == 0:
            strengths.append("未检测到认知反模式")

        # 收集致命修复项
        for c in contradictions:
            critical_fixes.append(f"[核心矛盾] {c.description} → {c.suggestion}")
        for i in critical_issues:
            critical_fixes.append(f"[{i.severity.value}] {i.description} → {i.fix_suggestion}")

        # generate总体judge
        if total_score >= 80 and not contradictions and not critical_issues:
            verdict = ("优秀方案:逻辑自洽,调研充分,执行可落地."
                      f"建议进入执行阶段,并建立月度复盘机制持续优化.")
        elif total_score >= 60 and len(critical_issues) <= 2:
            verdict = ("合格方案:整体框架合理,但存在需要修正的不足."
                      f"建议修正{len(critical_issues)}个致命问题和{len(major_issues)}个重大问题后重新评审.")
        elif total_score >= 40:
            verdict = ("方案存在系统性不足:核心逻辑或关键模块存在缺陷."
                      f"不建议直接执行,需要全维度重写."
                      f"共{len(critical_issues)}个致命问题,{len(major_issues)}个重大问题.")
        else:
            verdict = ("方案不可用:基础框架存在根本性缺陷,调研,推理,执行均不达标."
                      f"建议从需求理解开始重新构建.")

        return verdict, strengths, critical_fixes

    def quick_check(self, full_text: str) -> ConsultingValidationResult:
        """
        快速检查模式 - 仅检测最致命的问题

        适用于方案初稿的快速诊断.
        """
        return self.validate_full({
            'solution_name': '快速检查',
            'full_text': full_text
        })

    def generate_checklist(self) -> str:
        """generate方案交付前的自检清单"""
        return """
## 方案交付前自检清单(基于企业咨询经验):

### 必过项(缺一不可)
- [ ] 核心矛盾是否recognize并解决?
- [ ] 增长目标是否有约束条件反推(非拍脑袋)?
- [ ] 用户画像是否覆盖至少2类客群?
- [ ] 竞品分析是否有至少3个深度拆解?
- [ ] 每个数据点是否可溯源?
- [ ] 每个增长引擎是否有执行细节(团队/预算/KPI/时间)?
- [ ] 风险recognize是否覆盖合规/供应链/人才/财务/品牌(至少10项)?
- [ ] 是否有情景分析(好/中/差三种情景)?
- [ ] 是否有止损机制和触发条件?
- [ ] 内部各章节是否存在逻辑矛盾?

### 推荐项
- [ ] 渠道规划是否有量化模型(单店营收/单客价值/转化率)?
- [ ] 产品矩阵是否有SKU/价格/上市节奏规划?
- [ ] 资金规划是否有来源/使用/现金流测算?
- [ ] 对标案例是否有底层逻辑适配性分析?
- [ ] 品牌定位与增长来源是否一致?
- [ ] 是否有三重交叉论证(逻辑/数据/对标)?
"""
