"""
Cloning类型定义 v3.0
贤者Cloning系统的类型定义

基于神之架构 v1.0.0
五次转化模型：博士级深度学习 → Distillation → Codification → Cloning → OpenClaw
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

__all__ = [
    "CloningTier", "ConsultationMethod",
    "CapabilityVector", "WisdomLaw", "CloningIdentity",
    "AnalysisResult", "DecisionOption", "DecisionResult",
    "AdviceContext", "AdviceResult",
    "AssessmentCriteria", "AssessmentResult",
    "ClusterConsultationResult", "ClusterResult",
    "CloningProfile", "SageProfile",
]


class CloningTier(Enum):
    """Cloning层级"""
    TIER_1_CORE = 1      # 核心独立Cloning - 内阁/六部尚书
    TIER_2_CLUSTER = 2   # 学派集群Cloning - 六部/三法司/厂卫
    TIER_3_MINISTRY = 3  # 五军都督府级Cloning
    TIER_4_MICRO = 4     # 里甲制微Cloning - 函数/类级


# 兼容别名（旧版tier1/cluster模块使用）
CloningTier.TIER1_CORE = CloningTier.TIER_1_CORE
CloningTier.TIER2_CLUSTER = CloningTier.TIER_2_CLUSTER
CloningTier.TIER3_MINISTRY = CloningTier.TIER_3_MINISTRY
CloningTier.TIER4_MICRO = CloningTier.TIER_4_MICRO


class ConsultationMethod(Enum):
    """集群咨询方法"""
    LEADER = "leader"          # 仅由领军人物回答
    CONSENSUS = "consensus"    # 多数投票
    DEBATE = "debate"          # 多人辩论后综合
    SYNTHESIS = "synthesis"    # 融合所有人意见


@dataclass
class CapabilityVector:
    """能力向量 - 多维能力画像"""
    # 基础能力维度
    strategic_thinking: float = 0.0     # 战略思维
    ethical_judgment: float = 0.0      # 伦理判断
    dialectical_reasoning: float = 0.0   # 辩证推理
    practical_wisdom: float = 0.0       # 实践智慧
    long_term_vision: float = 0.0       # 长期视野
    crisis_response: float = 0.0        # 危机应对
    governance: float = 0.0             # 治理能力
    innovation: float = 0.0             # 创新能力
    
    # 专业能力维度
    system_thinking: float = 0.0        # 系统思维
    pattern_recognition: float = 0.0    # 模式识别
    evidence_evaluation: float = 0.0   # 证据评估
    narrative_building: float = 0.0     # 叙事构建
    
    # 人际能力维度
    leadership: float = 0.0              # 领导力
    communication: float = 0.0           # 沟通能力
    conflict_resolution: float = 0.0    # 冲突解决
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            'strategic_thinking': self.strategic_thinking,
            'ethical_judgment': self.ethical_judgment,
            'dialectical_reasoning': self.dialectical_reasoning,
            'practical_wisdom': self.practical_wisdom,
            'long_term_vision': self.long_term_vision,
            'crisis_response': self.crisis_response,
            'governance': self.governance,
            'innovation': self.innovation,
            'system_thinking': self.system_thinking,
            'pattern_recognition': self.pattern_recognition,
            'evidence_evaluation': self.evidence_evaluation,
            'narrative_building': self.narrative_building,
            'leadership': self.leadership,
            'communication': self.communication,
            'conflict_resolution': self.conflict_resolution,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'CapabilityVector':
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})
    
    def cosine_similarity(self, other: 'CapabilityVector') -> float:
        """计算与另一个能力向量的余弦相似度"""
        import math
        a = self.to_dict()
        b = other.to_dict()
        
        dot_product = sum(a[k] * b[k] for k in a if k in b)
        norm_a = math.sqrt(sum(a[k] ** 2 for k in a))
        norm_b = math.sqrt(sum(b[k] ** 2 for k in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)


@dataclass
class WisdomLaw:
    """智慧法则 - 已编码的可执行智慧"""
    id: str                          # 法则ID
    name: str                         # 法则名称
    description: str                   # 法则描述
    application_scenario: str          # 应用场景
    example: Optional[str] = None    # 示例
    priority: int = 1                 # 优先级 (1-5)


@dataclass
class CloningIdentity:
    """Cloning身份信息"""
    name: str                         # 姓名（中文）
    name_pinyin: str                  # 拼音
    era: str                          # 时代
    era_range: str                    # 时期范围 (如 "前551-前479")
    title: str                        # 称号/谥号
    school: str                       # 所属学派
    position: str                     # 神之架构中的岗位
    department: str                   # 所属部门
    biography: str                    # 生平简介 (1-2句)
    core_thoughts: List[str]          # 核心思想 (3-5条)


@dataclass
class AnalysisResult:
    """分析结果（兼容新旧两种字段名）"""
    cloning_name: str = ""              # 新版字段
    timestamp: Optional[datetime] = None
    problem: str = ""
    perspective: str = ""                # 新版字段
    analysis_content: str = ""           # 新版字段
    key_insights: List[str] = field(default_factory=list)  # 新版字段
    wisdom_laws_applied: List[str] = field(default_factory=list)  # 兼容字段
    confidence: float = 0.0
    reasoning_chain: List[str] = field(default_factory=list)
    # 兼容旧版字段
    sage_name: str = ""                  # 旧版
    school: str = ""                     # 旧版
    core_insight: str = ""               # 旧版
    recommendations: List[str] = field(default_factory=list)  # 旧版
    warnings: List[str] = field(default_factory=list)  # 兼容

    def __post_init__(self):
        # 自动同步新旧字段
        if self.sage_name and not self.cloning_name:
            self.cloning_name = self.sage_name
        elif self.cloning_name and not self.sage_name:
            self.sage_name = self.cloning_name
        if self.core_insight and not self.analysis_content:
            self.analysis_content = self.core_insight
        elif self.analysis_content and not self.core_insight:
            self.core_insight = self.analysis_content
        if self.recommendations and not self.key_insights:
            self.key_insights = self.recommendations
        if not self.timestamp:
            self.timestamp = datetime.now()


@dataclass
class DecisionOption:
    """决策选项"""
    id: str
    description: str
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    risk_level: str = "medium"
    expected_outcome: str = ""


@dataclass
class DecisionResult:
    """决策结果（兼容新旧两种字段名）"""
    cloning_name: str = ""              # 新版
    timestamp: Optional[datetime] = None
    decision: str = ""                   # 新版
    chosen_option: str = ""              # 新版
    reasoning: str = ""                  # 新版
    alternatives_considered: List[str] = field(default_factory=list)
    risk_assessment: str = ""
    wisdom_framework: str = ""
    confidence: float = 0.0             # 兼容字段
    problem: str = ""                    # 兼容
    sage_name: str = ""                  # 兼容

    def __post_init__(self):
        if self.sage_name and not self.cloning_name:
            self.cloning_name = self.sage_name
        elif self.cloning_name and not self.sage_name:
            self.sage_name = self.cloning_name
        if not self.timestamp:
            self.timestamp = datetime.now()


@dataclass
class AdviceContext:
    """建议上下文"""
    situation: str                   # 情境描述
    constraints: List[str] = field(default_factory=list)  # 约束条件
    stakeholders: List[str] = field(default_factory=list)  # 利益相关者
    time_horizon: str = "medium"     # 时间视野: short/medium/long
    success_criteria: List[str] = field(default_factory=list)  # 成功标准


@dataclass
class AdviceResult:
    """建议结果"""
    cloning_name: str
    timestamp: datetime
    advice: str                      # 建议内容
    reasoning: str                   # 给出建议的理由
    alternative_options: List[str] = field(default_factory=list)
    potential_pitfalls: List[str] = field(default_factory=list)
    historical_precedent: Optional[str] = None  # 历史先例


@dataclass
class AssessmentCriteria:
    """评估标准"""
    dimension: str                   # 评估维度
    metrics: List[str] = field(default_factory=list)  # 具体指标
    weights: Dict[str, float] = field(default_factory=dict)  # 权重


@dataclass
class AssessmentResult:
    """评估结果"""
    cloning_name: str
    timestamp: datetime
    subject: str                     # 被评估对象
    overall_score: float             # 综合评分 (0-100)
    dimension_scores: Dict[str, float] = field(default_factory=dict)  # 各维度评分
    strengths: List[str] = field(default_factory=list)  # 优势
    weaknesses: List[str] = field(default_factory=list)  # 劣势
    recommendations: List[str] = field(default_factory=list)  # 改进建议
    value_framework: str = ""        # 使用的价值框架


@dataclass
class ClusterConsultationResult:
    """集群咨询结果"""
    cluster_name: str
    method: ConsultationMethod
    timestamp: datetime
    primary_advice: str              # 主要建议
    debate_summary: str = ""         # 辩论摘要
    consensus_points: List[str] = field(default_factory=list)  # 共识点
    dissent_points: List[str] = field(default_factory=list)    # 分歧点
    participating_clonings: List[str] = field(default_factory=list)  # 参与的Cloning


@dataclass
class ClusterResult:
    """集群咨询结果 - 简化版"""
    cluster_name: str
    method: str = "leader"
    synthesis: str = ""
    participant_count: int = 0
    leader_analysis: Any = None  # AnalysisResult or None


@dataclass
class CloningProfile:
    """完整Cloning画像"""
    identity: CloningIdentity
    tier: CloningTier
    capability_vector: CapabilityVector
    wisdom_laws: List[WisdomLaw]
    consultation_count: int = 0      # 被咨询次数
    success_rate: float = 0.0        # 成功率
    last_consultation: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)  # 标签


# ── 兼容层：简化接口 ────────────────────────────────────
# tier1/cluster模块使用SageProfile而非CloningIdentity

@dataclass
class SageProfile:
    """简化版人物画像 - tier1/cluster模块使用"""
    name: str = ""
    name_en: str = ""
    era: str = ""
    years: str = ""
    school: str = ""
    tier: Any = None  # CloningTier
    position: str = ""
    department: str = ""
    title: str = ""
    biography: str = ""
    core_works: List[str] = field(default_factory=list)
    wisdom_laws: List[str] = field(default_factory=list)
    capability: Dict[str, int] = field(default_factory=dict)


# 扩展WisdomSchool枚举 - 新增8个学派用于Cloning
EXTENDED_SCHOOLS = {
    "LEGALIST": "法家",              # 韩非子/商鞅/管仲
    "MOHIST": "墨家",               # 墨子/禽滑厘
    "DIPLOMATIST": "纵横家",          # 鬼谷子/苏秦/张仪
    "MEDICAL": "医家",               # 张仲景/华佗/孙思邈
    "AGRICULTURE_ENGINEERING": "农工",  # 贾思勰/鲁班/蔡伦
    "FINANCIAL_INVESTMENT": "金融投资",  # 巴菲特/芒格/达利欧
    "MARKETING_BRAND": "营销品牌",      # 科特勒/奥格威/特劳特
    "INNOVATION_ENTREPRENEURSHIP": "创新创业",  # 马斯克/乔布斯/贝索斯
}
