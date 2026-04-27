"""咨询验证器 - 类型定义"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

__all__ = [
    'to_dict',
]

class ResearchDimension(Enum):
    """调研维度"""
    ENTERPRISE = "企业自身"
    USER = "用户画像"
    COMPETITION = "竞争格局"
    MARKET = "市场环境"
    RISK = "风险全景"

class ReasoningStep(Enum):
    """推理步骤"""
    CORE_CONTRADICTION = "recognize核心矛盾"
    CONSTRAINT_REVERSE = "从约束反推可能"
    USER_ANCHORING = "用户需求锚定"
    PATH_EXCLUSIVITY = "路径互斥性检验"
    BOTTOM_UP_VALIDATION = "执行层反推验证"
    COUNTERFACTUAL_TEST = "反事实压力测试"

class AntiPatternType(Enum):
    """反模式类型"""
    # 认知反模式
    GOAL_DRIVEN = "C-01 目标驱动型规划"
    CONFIRMATION_BIAS = "C-02 确认偏差"
    ANCHORING = "C-03 锚定效应"
    AVAILABILITY_BIAS = "C-04 可得性偏差"
    FALSE_ANALOGY = "C-05 错误类比"
    NARRATIVE_BLINDNESS = "C-06 叙事蒙蔽"
    # 输出反模式
    CONCEPT_STACKING = "O-01 概念堆砌"
    NUMBER_GAME = "O-02 数字游戏"
    SLOGAN_PLANNING = "O-03 口号式规划"
    HOLLOW_RISK = "O-04 空洞风控"
    FAKE_VALIDATION = "O-05 走过场验证"

class SeverityLevel(Enum):
    """严重程度"""
    CRITICAL = "致命"
    MAJOR = "重大"
    MODERATE = "中等"
    MINOR = "轻微"

class QualityDimension(Enum):
    """质量维度"""
    USER_ANALYSIS = "用户分析"
    COMPETITION_ANALYSIS = "竞争分析"
    DATA_ARGUMENTATION = "数据论证"
    EXECUTION_DETAIL = "执行细节"
    RISK_MANAGEMENT = "风险管控"
    LOGICAL_CONSISTENCY = "逻辑自洽"
    FINANCIAL_CLOSURE = "财务闭环"

@dataclass
class ResearchCheckItem:
    """调研检查项"""
    dimension: ResearchDimension
    item_name: str
    is_present: bool
    quality_score: float  # 0-1
    evidence: str = ""
    suggestion: str = ""

@dataclass
class ContradictionDetection:
    """矛盾检测结果"""
    description: str
    element_a: str       # 矛盾要素A
    element_b: str       # 矛盾要素B
    severity: SeverityLevel
    suggestion: str = ""

@dataclass
class AntiPatternDetection:
    """反模式检测结果"""
    pattern_type: AntiPatternType
    severity: SeverityLevel
    description: str
    evidence: str = ""
    fix_suggestion: str = ""

@dataclass
class QualityScoreDetail:
    """质量评分详情"""
    dimension: QualityDimension
    score: float              # 0-100
    minimum_standard: float
    ideal_standard: float
    gap_analysis: str = ""

@dataclass
class ValidationIssue:
    """验证问题"""
    id: str
    category: str            # 所属类别
    severity: SeverityLevel
    description: str
    evidence: str = ""
    fix_suggestion: str = ""

@dataclass
class ConsultingValidationResult:
    """咨询验证总结果"""
    validation_id: str
    solution_name: str
    total_quality_score: float          # 0-100
    dimension_scores: List[QualityScoreDetail]
    issues: List[ValidationIssue]
    contradictions: List[ContradictionDetection]
    anti_patterns: List[AntiPatternDetection]
    research_completeness: float        # 0-1
    reasoning_completeness: float       # 0-1
    overall_verdict: str                # 总体judge
    key_strengths: List[str]
    critical_fixes: List[str]           # 必须修正的致命问题
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            'validation_id': self.validation_id,
            'solution_name': self.solution_name,
            'total_quality_score': self.total_quality_score,
            'dimension_scores': [
                {'dimension': d.dimension.value, 'score': d.score,
                 'minimum': d.minimum_standard, 'ideal': d.ideal_standard,
                 'gap': d.gap_analysis}
                for d in self.dimension_scores
            ],
            'issues': [
                {'id': i.id, 'category': i.category,
                 'severity': i.severity.value, 'description': i.description,
                 'evidence': i.evidence, 'fix': i.fix_suggestion}
                for i in self.issues
            ],
            'contradictions': [
                {'description': c.description, 'a': c.element_a,
                 'b': c.element_b, 'severity': c.severity.value,
                 'suggestion': c.suggestion}
                for c in self.contradictions
            ],
            'anti_patterns': [
                {'type': p.pattern_type.value, 'severity': p.severity.value,
                 'description': p.description, 'evidence': p.evidence,
                 'fix': p.fix_suggestion}
                for p in self.anti_patterns
            ],
            'research_completeness': self.research_completeness,
            'reasoning_completeness': self.reasoning_completeness,
            'overall_verdict': self.overall_verdict,
            'key_strengths': self.key_strengths,
            'critical_fixes': self.critical_fixes,
            'validated_at': self.validated_at
        }
