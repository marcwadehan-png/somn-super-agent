"""
翰林院决策审核模块 v1.0.0
_hanlin_review.py

神之架构v3.2 "经济为命脉，翰林为喉舌" 的核心实现。
翰林院独立于六部之外，对所有决策进行三论审核：
  第一轮：逻辑论证检测（复用 fallacy_detector）
  第二轮：多视角反驳论证（经济/社会/心理/伦理四维）
  第三轮：综合评审（通过/驳回/修改后通过）

审核等级：甲等(>=0.9) / 乙等(0.7~0.9) / 丙等(0.5~0.7) / 丁等(<0.5)
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
#  类型定义
# ═══════════════════════════════════════════════════════════════

class ReviewGrade(Enum):
    """审核等级"""
    JIA = "甲等"      # >= 0.9, 直接通过
    YI = "乙等"       # 0.7 ~ 0.9, 通过但附注建议
    BING = "丙等"     # 0.5 ~ 0.7, 驳回修改
    DING = "丁等"     # < 0.5, 严重驳回


class ReviewDimension(Enum):
    """审核维度"""
    LOGIC = "逻辑论证"          # 顶级思维法+科学思维, 权重30%
    ECONOMY = "经济可行性"       # 经济学家+投资家, 权重25%
    SOCIAL = "社会稳定"          # 社会学家+政治家, 权重20%
    PSYCHOLOGY = "心理学"        # 心理学家+行为塑造, 权重15%
    ETHICS = "伦理合规"          # 儒家+法家, 权重10%


class ReviewAction(Enum):
    """审核动作"""
    PASS = "通过"
    PASS_WITH_NOTES = "通过（附注建议）"
    REVISE = "驳回修改"
    REJECT = "严重驳回"


@dataclass
class DimensionReview:
    """单维度审核结果"""
    dimension: ReviewDimension
    score: float                    # 0.0 ~ 1.0
    weight: float                   # 该维度权重
    findings: List[str]             # 发现的问题
    counter_arguments: List[str]    # 反驳意见
    reviewer: str                   # 审核人（翰林院学士）


@dataclass
class HanlinReviewResult:
    """翰林院审核结果"""
    # 基本信息
    reviewed_at: datetime
    decision_summary: str           # 被审核决策的摘要

    # 审核结果
    grade: ReviewGrade
    action: ReviewAction
    overall_score: float            # 加权总分

    # 分维度详情
    dimension_reviews: List[DimensionReview]

    # 综合意见
    counter_arguments: List[str]    # 未回应的反驳
    risk_warnings: List[str]        # 风险警告
    improvement_suggestions: List[str]  # 改进建议

    # 元信息
    hanlin_certified: bool = False  # 是否获"翰林院认证"
    bypass_requested: bool = False  # 是否被皇帝绕过


# ═══════════════════════════════════════════════════════════════
#  翰林院人员配置
# ═══════════════════════════════════════════════════════════════

_HANLIN_PERSONNEL = {
    "掌院": {
        "name": "韩非子",
        "title": "翰林院掌院·正三品",
        "role": "逻辑论证总管",
        "dimension": ReviewDimension.LOGIC,
        "sage_type": "复合型",
    },
    "学士甲": {
        "name": "墨子",
        "title": "翰林院学士甲·正四品",
        "role": "经济可行性审核",
        "dimension": ReviewDimension.ECONOMY,
        "sage_type": "实战派",
    },
    "学士乙": {
        "name": "慎到",
        "title": "翰林院学士乙·正四品",
        "role": "社会稳定风险评估",
        "dimension": ReviewDimension.SOCIAL,
        "sage_type": "理论派",
    },
    "学士丙": {
        "name": "荀子",
        "title": "翰林院学士丙·正四品",
        "role": "心理学视角审核",
        "dimension": ReviewDimension.PSYCHOLOGY,
        "sage_type": "理论派",
    },
    "学士丁": {
        "name": "邹衍",
        "title": "翰林院学士丁·正四品",
        "role": "伦理合规审查",
        "dimension": ReviewDimension.ETHICS,
        "sage_type": "理论派",
    },
    "侍读甲": {
        "name": "公孙龙",
        "title": "翰林院侍读甲·从四品",
        "role": "形式逻辑检测",
        "dimension": ReviewDimension.LOGIC,
        "sage_type": "理论派",
    },
    "侍读乙": {
        "name": "惠施",
        "title": "翰林院侍读乙·从四品",
        "role": "非形式谬误检测",
        "dimension": ReviewDimension.LOGIC,
        "sage_type": "理论派",
    },
}

# 维度 → 权重
_DIMENSION_WEIGHTS = {
    ReviewDimension.LOGIC: 0.30,
    ReviewDimension.ECONOMY: 0.25,
    ReviewDimension.SOCIAL: 0.20,
    ReviewDimension.PSYCHOLOGY: 0.15,
    ReviewDimension.ETHICS: 0.10,
}

# 维度 → 主审人
_DIMENSION_REVIEWER = {
    ReviewDimension.LOGIC: "韩非子",
    ReviewDimension.ECONOMY: "墨子",
    ReviewDimension.SOCIAL: "慎到",
    ReviewDimension.PSYCHOLOGY: "荀子",
    ReviewDimension.ETHICS: "邹衍",
}


# ═══════════════════════════════════════════════════════════════
#  核心审核引擎
# ═══════════════════════════════════════════════════════════════

class HanlinReviewEngine:
    """翰林院决策审核引擎"""

    def __init__(self):
        self._fallacy_detector = None
        self._initialized = False

    def _ensure_init(self):
        """懒加载初始化（复用 fallacy_detector）"""
        if self._initialized:
            return
        try:
            from logic.fallacy_detector import analyze_argument_quality
            self._fallacy_detector = analyze_argument_quality
            logger.debug("翰林院: fallacy_detector 加载成功")
        except (ImportError, NameError):
            logger.warning("翰林院: fallacy_detector 不可用，使用内置逻辑检测")
            self._fallacy_detector = None
        self._initialized = True

    def review_decision(
        self,
        decision_text: str,
        decision_context: Optional[Dict[str, Any]] = None,
        bypass: bool = False,
    ) -> HanlinReviewResult:
        """
        审核决策（主入口）

        Args:
            decision_text: 决策文本（论点+论证过程+结论）
            decision_context: 决策上下文（问题类型、学派、部门等）
            bypass: 是否被皇帝绕过审核

        Returns:
            HanlinReviewResult: 审核结果
        """
        self._ensure_init()

        ctx = decision_context or {}
        summary = decision_text[:200] if len(decision_text) > 200 else decision_text

        # 三轮审核
        dim_reviews = []

        # 第一轮：逻辑论证检测
        logic_review = self._review_logic(decision_text, ctx)
        dim_reviews.append(logic_review)

        # 第二轮：多视角反驳
        economy_review = self._review_economy(decision_text, ctx)
        dim_reviews.append(economy_review)

        social_review = self._review_social_stability(decision_text, ctx)
        dim_reviews.append(social_review)

        psych_review = self._review_psychology(decision_text, ctx)
        dim_reviews.append(psych_review)

        ethics_review = self._review_ethics(decision_text, ctx)
        dim_reviews.append(ethics_review)

        # 第三轮：综合评审
        result = self._synthesize(dim_reviews, summary, bypass)

        if bypass:
            result.bypass_requested = True

        return result

    # ───────────────────────────────────────────────────────────
    #  第一轮：逻辑论证检测（韩非子+公孙龙+惠施）
    # ───────────────────────────────────────────────────────────

    def _review_logic(
        self, decision_text: str, ctx: Dict[str, Any]
    ) -> DimensionReview:
        """逻辑论证检测维度"""
        findings = []
        counter_args = []
        score = 0.7  # 基础分

        # 尝试使用 fallacy_detector
        if self._fallacy_detector:
            try:
                arg_dict = {
                    "type": "general",
                    "text": decision_text,
                    "conclusion": decision_text[-200:] if len(decision_text) > 200 else decision_text,
                }
                quality = self._fallacy_detector(arg_dict)
                if isinstance(quality, dict):
                    score = quality.get("quality_score", 0.7)
                    fallacies = quality.get("fallacies", [])
                    for f in fallacies:
                        sev = f.get("severity", "minor")
                        if sev == "critical":
                            findings.append(f"[严重] {f.get('description', '')}")
                            counter_args.append(f"逻辑漏洞: {f.get('suggestion', '需要补充论证')}")
                            score -= 0.15
                        elif sev == "major":
                            findings.append(f"[重要] {f.get('description', '')}")
                            score -= 0.08
                        else:
                            findings.append(f"[轻微] {f.get('description', '')}")
                            score -= 0.03
            except Exception as e:
                logger.warning(f"翰林院逻辑检测异常: {e}")

        # 内置基本检查（补充）
        score = self._builtin_logic_checks(decision_text, score, findings, counter_args)

        score = max(0.0, min(1.0, score))

        return DimensionReview(
            dimension=ReviewDimension.LOGIC,
            score=score,
            weight=_DIMENSION_WEIGHTS[ReviewDimension.LOGIC],
            findings=findings,
            counter_arguments=counter_args,
            reviewer="韩非子",
        )

    def _builtin_logic_checks(
        self, text: str, score: float, findings: List[str], counter_args: List[str]
    ) -> float:
        """内置逻辑检查（不依赖外部模块）"""
        # 检查论证长度——过短的决策缺乏论证
        if len(text) < 100:
            findings.append("论证过短（不足100字），缺乏充分推理")
            counter_args.append("请展开论证过程，补充前提和推理链")
            score -= 0.15

        # 检查是否有明确结论
        conclusion_markers = ["因此", "综上", "结论是", "建议", "应该", "必须"]
        has_conclusion = any(m in text for m in conclusion_markers)
        if not has_conclusion:
            findings.append("缺少明确结论或建议")
            score -= 0.10

        # 检查是否有数据支撑
        data_markers = ["数据", "比例", "%", "统计", "调查", "研究", "实验"]
        has_data = any(m in text for m in data_markers)
        if not has_data and len(text) > 200:
            findings.append("论证缺少数据支撑，建议补充量化依据")
            score -= 0.05

        return score

    # ───────────────────────────────────────────────────────────
    #  第二轮：多视角反驳论证
    # ───────────────────────────────────────────────────────────

    def _review_economy(
        self, decision_text: str, ctx: Dict[str, Any]
    ) -> DimensionReview:
        """经济可行性审核（墨子）"""
        findings = []
        counter_args = []
        score = 0.7  # 基础分

        # 检查成本考量
        cost_markers = ["成本", "费用", "预算", "投入", "ROI", "回报", "收益"]
        has_cost = any(m in decision_text for m in cost_markers)
        if not has_cost:
            findings.append("未涉及成本效益分析")
            counter_args.append("[墨子] 节用为民——请补充成本估算和投资回报分析")
            score -= 0.15

        # 检查市场影响
        market_markers = ["市场", "竞争", "份额", "用户", "消费者", "客户"]
        has_market = any(m in decision_text for m in market_markers)
        if has_market:
            score += 0.05
        else:
            findings.append("未评估市场影响")
            counter_args.append("[墨子] 兼爱非攻——请考虑决策对市场和竞争格局的影响")
            score -= 0.10

        # 营销相关问题额外加权
        problem_type = ctx.get("problem_type", "")
        if problem_type in ("CONSUMER_MARKETING", "BRAND_STRATEGY", "MARKETING"):
            if has_cost and has_market:
                score += 0.10
                findings.append("营销决策包含完整的成本和市场分析")

        return DimensionReview(
            dimension=ReviewDimension.ECONOMY,
            score=max(0.0, min(1.0, score)),
            weight=_DIMENSION_WEIGHTS[ReviewDimension.ECONOMY],
            findings=findings,
            counter_arguments=counter_args,
            reviewer="墨子",
        )

    def _review_social_stability(
        self, decision_text: str, ctx: Dict[str, Any]
    ) -> DimensionReview:
        """社会稳定风险评估（慎到）"""
        findings = []
        counter_args = []
        score = 0.75  # 基础分（社会稳定默认通过）

        # 检查负面风险
        risk_markers = ["风险", "隐患", "争议", "反对", "抵制", "负面"]
        has_risk_mentioned = any(m in decision_text for m in risk_markers)
        if has_risk_mentioned:
            score += 0.05  # 主动识别风险，加分
            findings.append("已识别潜在社会风险")
        else:
            findings.append("未进行社会风险评估")
            counter_args.append("[慎到] 势治之要——请评估可能引发的公众反应和舆情风险")

        # 检查合规性
        compliance_markers = ["合规", "法律", "法规", "政策", "监管"]
        has_compliance = any(m in decision_text for m in compliance_markers)
        if has_compliance:
            score += 0.05
        else:
            counter_args.append("[慎到] 请确认决策符合现行法规和政策要求")

        # 社会稳定相关问题
        if problem_type := ctx.get("problem_type", ""):
            if problem_type == "SOCIAL_STABILITY":
                if not has_risk_mentioned:
                    score -= 0.15
                    counter_args.append("[慎到] 社会稳定类问题必须包含风险评估！")

        return DimensionReview(
            dimension=ReviewDimension.SOCIAL,
            score=max(0.0, min(1.0, score)),
            weight=_DIMENSION_WEIGHTS[ReviewDimension.SOCIAL],
            findings=findings,
            counter_arguments=counter_args,
            reviewer="慎到",
        )

    def _review_psychology(
        self, decision_text: str, ctx: Dict[str, Any]
    ) -> DimensionReview:
        """心理学视角审核（荀子）"""
        findings = []
        counter_args = []
        score = 0.65  # 基础分（心理学维度偏严格）

        # 检查用户心理考量
        psych_markers = ["用户", "消费者", "心理", "感知", "体验", "情感", "认知", "需求"]
        has_psych = any(m in decision_text for m in psych_markers)
        if has_psych:
            score += 0.15
            findings.append("已考虑用户心理因素")
        else:
            findings.append("未分析目标用户的心理预期和行为模式")
            counter_args.append("[荀子] 性恶论——不能假设用户会理性响应，请分析认知偏差和情感因素")

        # 检查行为设计
        behavior_markers = ["习惯", "行为", "激励", "奖励", "动机", "触发"]
        has_behavior = any(m in decision_text for m in behavior_markers)
        if has_behavior:
            score += 0.05

        # 营销/C端问题严格要求
        problem_type = ctx.get("problem_type", "")
        if problem_type in ("CONSUMER_MARKETING", "PSYCHOLOGICAL_INSIGHT", "NUDGE", "HABIT"):
            if not has_psych:
                score -= 0.15
                counter_args.append("[荀子] C端营销必须深入分析消费者心理！")

        return DimensionReview(
            dimension=ReviewDimension.PSYCHOLOGY,
            score=max(0.0, min(1.0, score)),
            weight=_DIMENSION_WEIGHTS[ReviewDimension.PSYCHOLOGY],
            findings=findings,
            counter_arguments=counter_args,
            reviewer="荀子",
        )

    def _review_ethics(
        self, decision_text: str, ctx: Dict[str, Any]
    ) -> DimensionReview:
        """伦理合规审查（邹衍）"""
        findings = []
        counter_args = []
        score = 0.8  # 基础分（伦理维度默认较高）

        # 检查伦理考量
        ethics_markers = ["道德", "伦理", "责任", "公正", "公平", "诚信", "透明"]
        has_ethics = any(m in decision_text for m in ethics_markers)
        if has_ethics:
            score += 0.05
            findings.append("已包含伦理考量")

        # 检查潜在操控
        manipulation_markers = ["诱导", "操控", "欺骗", "误导", "隐瞒"]
        has_manipulation = any(m in decision_text for m in manipulation_markers)
        if has_manipulation:
            score -= 0.20
            findings.append("[警告] 检测到可能涉及操控性内容")
            counter_args.append("[邹衍] 五德终始——操控性营销虽然短期有效，长期必遭反噬")

        # 检查社会责任
        social_resp_markers = ["社会", "公益", "环保", "可持续", "社区"]
        has_social_resp = any(m in decision_text for m in social_resp_markers)
        if not has_social_resp:
            counter_args.append("[邹衍] 请考虑决策的社会责任和可持续发展影响")

        return DimensionReview(
            dimension=ReviewDimension.ETHICS,
            score=max(0.0, min(1.0, score)),
            weight=_DIMENSION_WEIGHTS[ReviewDimension.ETHICS],
            findings=findings,
            counter_arguments=counter_args,
            reviewer="邹衍",
        )

    # ───────────────────────────────────────────────────────────
    #  第三轮：综合评审
    # ───────────────────────────────────────────────────────────

    def _synthesize(
        self,
        dim_reviews: List[DimensionReview],
        decision_summary: str,
        bypass: bool,
    ) -> HanlinReviewResult:
        """综合评审——计算加权总分、确定等级、汇总意见"""
        weighted_score = 0.0
        all_counter_args = []
        all_warnings = []
        all_suggestions = []

        for dr in dim_reviews:
            weighted_score += dr.score * dr.weight
            all_counter_args.extend(dr.counter_arguments)
            all_warnings.extend([f"[{dr.reviewer}] {f}" for f in dr.findings])

            # 生成改进建议
            if dr.score < 0.6:
                all_suggestions.append(
                    f"[{dr.dimension.value}] 得分{dr.score:.2f}偏低，"
                    f"建议补充{dr.dimension.value}相关论证"
                )

        weighted_score = round(weighted_score, 4)

        # 确定审核等级
        if weighted_score >= 0.9:
            grade = ReviewGrade.JIA
            action = ReviewAction.PASS
        elif weighted_score >= 0.7:
            grade = ReviewGrade.YI
            action = ReviewAction.PASS_WITH_NOTES
        elif weighted_score >= 0.5:
            grade = ReviewGrade.BING
            action = ReviewAction.REVISE
        else:
            grade = ReviewGrade.DING
            action = ReviewAction.REJECT

        certified = (grade == ReviewGrade.JIA)

        return HanlinReviewResult(
            reviewed_at=datetime.now(),
            decision_summary=decision_summary,
            grade=grade,
            action=action,
            overall_score=weighted_score,
            dimension_reviews=dim_reviews,
            counter_arguments=all_counter_args,
            risk_warnings=all_warnings,
            improvement_suggestions=all_suggestions,
            hanlin_certified=certified,
            bypass_requested=bypass,
        )


# ═══════════════════════════════════════════════════════════════
#  公共接口
# ═══════════════════════════════════════════════════════════════

_engine: Optional[HanlinReviewEngine] = None


def review_decision(
    decision_text: str,
    decision_context: Optional[Dict[str, Any]] = None,
    bypass: bool = False,
) -> HanlinReviewResult:
    """
    翰林院决策审核（公共接口）

    Args:
        decision_text: 决策文本
        decision_context: 决策上下文
        bypass: 皇帝绕过审核

    Returns:
        HanlinReviewResult
    """
    global _engine
    if _engine is None:
        _engine = HanlinReviewEngine()
    return _engine.review_decision(decision_text, decision_context, bypass)


def get_hanlin_personnel() -> Dict[str, Dict[str, str]]:
    """获取翰林院人员配置"""
    return {
        k: {"name": v["name"], "title": v["title"], "role": v["role"]}
        for k, v in _HANLIN_PERSONNEL.items()
    }


def format_review_result(result: HanlinReviewResult) -> str:
    """
    格式化审核结果为可读文本

    Args:
        result: HanlinReviewResult

    Returns:
        格式化的审核报告文本
    """
    bypass_mark = " [皇帝绕过]" if result.bypass_requested else ""
    certified_mark = " [翰林院认证]" if result.hanlin_certified else ""

    lines = [
        f"═══ 翰林院审核报告 ═══",
        f"等级: {result.grade.value}{certified_mark}{bypass_mark}",
        f"总分: {result.overall_score:.4f}",
        f"动作: {result.action.value}",
        f"时间: {result.reviewed_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        "── 分维度评分 ──",
    ]

    for dr in result.dimension_reviews:
        lines.append(
            f"  {dr.dimension.value}({dr.reviewer}): "
            f"{dr.score:.2f} (权重{dr.weight:.0%})"
        )
        for f in dr.findings:
            lines.append(f"    - {f}")

    if result.counter_arguments:
        lines.append("")
        lines.append("── 反驳意见 ──")
        for ca in result.counter_arguments:
            lines.append(f"  ! {ca}")

    if result.risk_warnings:
        lines.append("")
        lines.append("── 风险警告 ──")
        for w in result.risk_warnings:
            lines.append(f"  [!] {w}")

    if result.improvement_suggestions:
        lines.append("")
        lines.append("── 改进建议 ──")
        for s in result.improvement_suggestions:
            lines.append(f"  -> {s}")

    return "\n".join(lines)
