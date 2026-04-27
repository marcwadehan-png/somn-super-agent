"""咨询验证器 - 六步战略推理验证器"""
import re
from typing import Any, Dict, List

from ._cv_types import (
    ReasoningStep,
    SeverityLevel,
    ContradictionDetection,
    ValidationIssue,
)

__all__ = [
    'validate',
]

class StrategicReasoningValidator:
    """
    六步战略推理验证器

    验证咨询方案是否完成了完整的战略推理链:
    1. recognize核心矛盾 - 方案中根本不相容的要素
    2. 从约束反推可能 - 不问能做多大,问资源能撑多大
    3. 用户需求锚定 - 所有战略假设通过"用户为什么买单"检验
    4. 路径互斥性检验 - 多条路径是否存在互斥关系
    5. 执行层反推验证 - 从具体执action作向上累加
    6. 反事实压力测试 - 假设核心前提不成立
    """

    # 矛盾检测规则
    CONTRADICTION_RULES = [
        {
            'name': '品牌心智与增长来源矛盾',
            'pattern_a': r'(非遗|稀缺|收藏|孤品|高端|手工|匠心)',
            'pattern_b': r'(规模化|大众|入门|代工|量产|平价)',
            'description': '品牌核心心智(高端/稀缺/非遗)与主要增长来源(规模化/大众/代工)不一致',
            'suggestion': '明确品牌核心定位,如果走高端稀缺路线,规模化产品必须与核心资产做深度绑定,或使用完全隔离的子品牌.',
            'severity': SeverityLevel.CRITICAL
        },
        {
            'name': '高端化与渠道下沉矛盾',
            'pattern_a': r'(高端|奢侈品|收藏级|万元)',
            'pattern_b': r'(下沉|二三四线|大众市场|社区店|拼多多|抖音低价)',
            'description': '高端品牌定位与渠道下沉strategy存在矛盾',
            'suggestion': '明确高端品牌的渠道边界,下沉市场应使用独立品牌或独立产品线.',
            'severity': SeverityLevel.MAJOR
        },
        {
            'name': '线上线下价格冲突',
            'pattern_a': r'(线上.*渠道|电商|直播|抖音|天猫)',
            'pattern_b': r'(线下.*渠道|门店|体验店|高端商圈)',
            'check': r'(价格管控|价格体系|渠道冲突|窜货|价格区隔)',
            'description': '线上线下双渠道布局,但未设计价格管控机制',
            'suggestion': '设计完整的渠道价格体系,包括线上线下价格带区隔,渠道专属产品,窜货处罚规则.',
            'severity': SeverityLevel.MAJOR
        },
    ]

    # 互斥路径检测规则
    EXCLUSIVITY_RULES = [
        {
            'name': '品类扩展与品牌聚焦',
            'elements': ['品类扩展', '品牌聚焦', '心智占领'],
            'conflict_when': '品类扩展超过核心品类占比的30%',
            'description': '品类扩展可能稀释品牌核心心智',
            'severity': SeverityLevel.MAJOR
        },
        {
            'name': '多线并行与资源集中',
            'elements': ['同时推进', '多线并行', '全面铺开'],
            'conflict_when': '同时推进3个以上增长方向',
            'description': '有限资源被过度分散,每条线都做不好',
            'severity': SeverityLevel.CRITICAL
        },
    ]

    def validate(self, solution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行完整的六步推理验证

        Returns:
            包含各步骤验证结果的字典
        """
        full_text = solution_data.get('full_text', '')

        results = {
            'steps_completed': [],
            'contradictions': [],
            'exclusivity_issues': [],
            'user_anchor_issues': [],
            'bottom_up_gaps': [],
            'stress_test_gaps': [],
            'completeness_score': 0.0
        }

        # 第一步:recognize核心矛盾
        contradictions = self._detect_contradictions(full_text)
        results['contradictions'] = contradictions
        if contradictions:
            results['steps_completed'].append(ReasoningStep.CORE_CONTRADICTION.value)

        # 第二步:从约束反推
        constraint_check = self._check_constraint_reverse(solution_data)
        if constraint_check.get('has_constraint_analysis'):
            results['steps_completed'].append(ReasoningStep.CONSTRAINT_REVERSE.value)

        # 第三步:用户需求锚定
        user_issues = self._check_user_anchoring(solution_data)
        results['user_anchor_issues'] = user_issues
        if not user_issues:
            results['steps_completed'].append(ReasoningStep.USER_ANCHORING.value)

        # 第四步:路径互斥性检验
        exclusivity = self._check_path_exclusivity(full_text, solution_data)
        results['exclusivity_issues'] = exclusivity

        # 第五步:执行层反推验证
        bottom_up = self._check_bottom_up_validation(solution_data)
        results['bottom_up_gaps'] = bottom_up

        # 第六步:反事实压力测试
        stress_test = self._check_stress_test(solution_data)
        results['stress_test_gaps'] = stress_test

        # 计算完整性
        total_steps = len(ReasoningStep)
        completed = len(results['steps_completed'])
        results['completeness_score'] = completed / total_steps

        return results

    def _detect_contradictions(self, full_text: str) -> List[ContradictionDetection]:
        """检测文本中的核心矛盾"""
        contradictions = []

        for rule in self.CONTRADICTION_RULES:
            match_a = bool(re.search(rule['pattern_a'], full_text))
            match_b = bool(re.search(rule['pattern_b'], full_text))

            if match_a and match_b:
                # 如果有缓解措施(check pattern),检查是否被解决
                if 'check' in rule:
                    has_mitigation = bool(re.search(rule['check'], full_text))
                    if has_mitigation:
                        continue

                contradictions.append(ContradictionDetection(
                    description=rule['description'],
                    element_a=rule['pattern_a'],
                    element_b=rule['pattern_b'],
                    severity=rule['severity'],
                    suggestion=rule['suggestion']
                ))

        return contradictions

    def _check_constraint_reverse(self, solution_data: Dict) -> Dict[str, Any]:
        """检查是否从约束条件反推目标"""
        full_text = solution_data.get('full_text', '')

        constraints = {
            '产能约束': any(kw in full_text for kw in ['产能', '产能瓶颈', '扩产', '产能上限']),
            '人才约束': any(kw in full_text for kw in ['人才', '团队', '招聘', '组织能力']),
            '资金约束': any(kw in full_text for kw in ['资金', '融资', '投入', '预算', '现金流']),
            '市场约束': any(kw in full_text for kw in ['市场天花板', '市场份额', 'TAM', '市场空间']),
        }

        has_constraint_analysis = sum(constraints.values()) >= 3
        has_reverse_engineering = any(
            kw in full_text for kw in ['反推', '约束', '能力边界', '合理目标', '天花板']
        )

        return {
            'has_constraint_analysis': has_constraint_analysis,
            'has_reverse_engineering': has_reverse_engineering,
            'constraints_checked': {k: v for k, v in constraints.items() if v},
            'missing_constraints': [k for k, v in constraints.items() if not v]
        }

    def _check_user_anchoring(self, solution_data: Dict) -> List[ValidationIssue]:
        """检查用户需求锚定"""
        full_text = solution_data.get('full_text', '')
        issues = []

        # 检查用户画像
        has_user_profile = any(kw in full_text for kw in [
            '用户画像', '目标用户', '用户群体', '客群', '消费者画像'
        ])
        if not has_user_profile:
            issues.append(ValidationIssue(
                id='UA-01', category='用户需求锚定',
                severity=SeverityLevel.CRITICAL,
                description='方案中完全缺失用户画像分析,无法验证"用户为什么买单"的核心假设.',
                fix_suggestion='补充至少2类核心用户画像(现有用户+增量用户),包含年龄/收入/购买动机/decision因素/复购周期.'
            ))

        # 检查差异化价值
        has_differentiation = any(kw in full_text for kw in [
            '差异化', '核心优势', '竞争力', '为什么选择', '壁垒'
        ])
        if not has_differentiation:
            issues.append(ValidationIssue(
                id='UA-02', category='用户需求锚定',
                severity=SeverityLevel.MAJOR,
                description='方案未明确消费者为什么选择该品牌而非竞品.',
                fix_suggestion='明确差异化价值主张:与竞品的核心差异是什么?消费者能感知到吗?'
            ))

        return issues

    def _check_path_exclusivity(self, full_text: str,
                                solution_data: Dict) -> List[Dict]:
        """检查路径互斥性"""
        issues = []

        for rule in self.EXCLUSIVITY_RULES:
            elements_found = sum(
                1 for elem in rule['elements'] if elem in full_text
            )
            if elements_found >= 2:
                # 检查是否有风险隔离机制
                has_mitigation = any(
                    kw in full_text for kw in ['风险隔离', '品牌隔离', '资源优先级', '分阶段']
                )
                if not has_mitigation:
                    issues.append({
                        'name': rule['name'],
                        'description': rule['description'],
                        'severity': rule['severity'].value,
                        'conflict_condition': rule['conflict_when'],
                        'suggestion': f"检测到'{','.join(rule['elements'][:2])}'可能存在互斥关系,建议设计风险隔离机制或明确优先级排序."
                    })

        return issues

    def _check_bottom_up_validation(self, solution_data: Dict) -> List[ValidationIssue]:
        """检查执行层反推验证"""
        full_text = solution_data.get('full_text', '')
        gaps = []

        # 检查是否有从执行单元向上累加的验证
        has_unit_model = any(kw in full_text for kw in [
            '单店', '单客', '单品', 'ROI', '转化率', '坪效', '人效'
        ])

        if not has_unit_model:
            gaps.append(ValidationIssue(
                id='BU-01', category='执行层反推',
                severity=SeverityLevel.MAJOR,
                description='方案缺少最小执行单元的量化模型(单店营收/单客价值/单品GMV等).',
                fix_suggestion='建立执行层反推模型:单店营收×门店数=线下营收;单品GMV×SKU×转化率=线上营收.'
            ))

        # 检查目标是否有拆解
        has_target_breakdown = any(kw in full_text for kw in [
            '目标拆解', '贡献', '营收构成', '渠道占比'
        ])
        if not has_target_breakdown:
            gaps.append(ValidationIssue(
                id='BU-02', category='执行层反推',
                severity=SeverityLevel.MAJOR,
                description='增长目标未拆解到可验证的执行单元.',
                fix_suggestion='将总目标拆解到各渠道/各产品线的具体营收贡献,并验证累加值是否合理.'
            ))

        return gaps

    def _check_stress_test(self, solution_data: Dict) -> List[ValidationIssue]:
        """检查反事实压力测试"""
        full_text = solution_data.get('full_text', '')
        gaps = []

        # 检查是否有情景分析
        has_scenario = any(kw in full_text for kw in [
            '情景分析', '最差情景', '压力测试', '悲观', '止损', '应急预案'
        ])

        if not has_scenario:
            gaps.append(ValidationIssue(
                id='CF-01', category='反事实压力测试',
                severity=SeverityLevel.MAJOR,
                description='方案缺少情景分析和压力测试,未验证核心假设失效时的应对方案.',
                fix_suggestion='设计最好/中性/最差三种情景,明确止损触发条件和应对方案.'
            ))

        # 检查止损机制
        has_stop_loss = any(kw in full_text for kw in [
            '止损', '预警', '红线', '退出', '收缩', '触发条件'
        ])
        if not has_stop_loss:
            gaps.append(ValidationIssue(
                id='CF-02', category='反事实压力测试',
                severity=SeverityLevel.MODERATE,
                description='方案未设计止损机制和预警红线.',
                fix_suggestion='设定核心metrics的预警红线和止损触发条件,避免"越亏越投".'
            ))

        return gaps
