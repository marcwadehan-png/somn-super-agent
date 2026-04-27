"""wisdom_fusion enums & dataclasses v1.2

[v1.2 道家升级] 新增上善若水融合模式（ShangShanFusionMode）——
体现"上善若水，水善利万物而不争"的包容性超越智慧。

核心变更：
  - 新增 ShangShanFusionMode 枚举：HARMONY_ORIENTED / BOUNDARY_TRANSCENDENCE / FLUID_INTEGRATION
  - 新增 ShangShanFusionConfig：上善若水融合配置
  - 新增 ShangShanResult：融合结果分析
  - FusionConfig 增加 shang_shan_enabled 开关和 shang_shan_mode

核心理念：融合不是消灭差异，而是让差异相互成就。
如水善利万物而不争，包容一切而非排斥异己。
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

__all__ = [
    'effective_weight',
]

class FusionMethod(Enum):
    WEIGHTED_AVERAGE = "weighted_average"
    MAJORITY_VOTE = "majority_vote"
    META_LEARNING = "meta_learning"
    HIERARCHICAL = "hierarchical"
    ADAPTIVE = "adaptive"


# ── v1.2: 道家上善若水融合模式 ────────────────────────────────────────

class ShangShanFusionMode(Enum):
    """
    上善若水融合模式——"水善利万物而不争"的包容性超越策略。

    核心理念：融合不是消灭差异，而是让差异相互成就。

    - HARMONY_ORIENTED（和谐导向）：
      优先考虑各学派建议的互补性，而非简单排序。
      如水包容万物，不同建议可以在不同维度上各司其职。

    - BOUNDARY_TRANSCENDENCE（边界超越）：
      鼓励不同学派在对方领域产生正向影响，而非划地盘。
      如水无常形，不被边界限制。

    - FLUID_INTEGRATION（流式整合）：
      采用迭代加权而非一次性分配的方式进行融合。
      如水流不息，融合是持续过程而非一次性事件。
    """
    HARMONY_ORIENTED = "harmony_oriented"         # 和谐导向：互补性超越
    BOUNDARY_TRANSCENDENCE = "boundary_transcendence"  # 边界超越：跨域融合
    FLUID_INTEGRATION = "fluid_integration"        # 流式整合：迭代加权


@dataclass
class ShangShanFusionConfig:
    """
    上善若水融合配置——"上善若水"的系统参数。

    核心理念：融合策略应如水一般，柔韧、包容、顺势。
    """
    # 总开关
    shang_shan_enabled: bool = True

    # 默认融合模式
    default_mode: ShangShanFusionMode = ShangShanFusionMode.HARMONY_ORIENTED

    # 和谐导向参数
    complementarity_threshold: float = 0.3  # 互补性阈值（超过此值触发和谐融合）
    harmony_bonus_weight: float = 0.2       # 互补性得分对最终权重的加成

    # 边界超越参数
    boundary_transcendence_enabled: bool = True
    cross_domain_influence: float = 0.15    # 跨域影响力系数

    # 流式整合参数
    fluid_iteration_count: int = 3          # 流式整合迭代次数
    fluid_convergence_threshold: float = 0.01  # 收敛阈值

    # 阴阳平衡参数
    yin_yang_balance_check: bool = True     # 是否进行阴阳平衡检查
    balance_threshold: float = 0.3         # 平衡偏离阈值

    # 道家谚语
    dao_proverb: str = "上善若水，水善利万物而不争，处众人之所恶，故几于道。"


@dataclass
class ComplementarityScore:
    """互补性得分——评估不同学派建议之间的互补程度"""
    school_a: str
    school_b: str
    dimension_a: str   # 建议A的关注维度
    dimension_b: str   # 建议B的关注维度
    complementarity: float  # 互补性得分（0-1）
    harmony_bonus: float   # 和谐加分
    cross_influence: float  # 跨域影响
    assessment: str = ""   # 道家评估


@dataclass
class ShangShanResult:
    """上善若水融合结果"""
    mode_used: ShangShanFusionMode
    fused_weights: Dict[str, float]       # 最终融合权重
    complementarity_scores: List[ComplementarityScore]  # 互补性分析
    harmony_score: float = 0.0            # 和谐度（0-1）
    boundary_transcendence_score: float = 0.0  # 边界超越度
    fluid_convergence: float = 0.0        # 流式收敛度
    yin_yang_balance: float = 0.5        # 阴阳平衡度（0=极阴，1=极阳）
    # 道家分析
    dao_assessment: str = ""
    water_flow_guidance: str = ""
    warnings: List[str] = field(default_factory=list)

class WisdomPriority(Enum):
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    ETHICAL = "ethical"
    NATURAL = "natural"
    CULTURAL = "cultural"
    BALANCED = "balanced"

@dataclass
class WisdomContribution:
    module_name: str
    output: Any
    confidence: float = 0.5
    relevance: float = 0.5
    reliability: float = 0.8
    weight: float = 0.0

    def effective_weight(self) -> float:
        return self.weight * self.confidence * self.reliability

@dataclass
class FusionConfig:
    method: FusionMethod = FusionMethod.ADAPTIVE
    priority: WisdomPriority = WisdomPriority.BALANCED
    enable_conflict_resolution: bool = True
    enable_adaptive_weights: bool = True
    enable_learning: bool = True

    # [v1.2 道家升级] 上善若水融合配置
    shang_shan: ShangShanFusionConfig = field(default_factory=ShangShanFusionConfig)

    default_weights: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "strategic_decision": {
            "sufu_wisdom": 0.28, "military_strategy": 0.14,
            "dao_wisdom": 0.12, "ru_wisdom": 0.12,
            "hongming_wisdom": 0.08, "civilization_wisdom": 0.14,
            "civilization_war_economy": 0.12
        },
        "tactical_execution": {
            "military_strategy": 0.34, "sufu_wisdom": 0.16,
            "dao_wisdom": 0.15, "ru_wisdom": 0.08,
            "hongming_wisdom": 0.07, "civilization_war_economy": 0.20
        },
        "ethical_assessment": {
            "ru_wisdom": 0.32, "sufu_wisdom": 0.22,
            "hongming_wisdom": 0.18, "dao_wisdom": 0.08,
            "civilization_wisdom": 0.20
        },
        "risk_management": {
            "sufu_wisdom": 0.22, "dao_wisdom": 0.18,
            "military_strategy": 0.15, "ru_wisdom": 0.12,
            "civilization_war_economy": 0.18, "civilization_wisdom": 0.15
        },
        "cultural_adaptation": {
            "hongming_wisdom": 0.34, "ru_wisdom": 0.14,
            "sufu_wisdom": 0.10, "dao_wisdom": 0.10,
            "civilization_wisdom": 0.32
        },
        "problem_solving": {
            "civilization_wisdom": 0.22, "civilization_war_economy": 0.18,
            "sufu_wisdom": 0.18, "military_strategy": 0.14,
            "dao_wisdom": 0.12, "ru_wisdom": 0.10, "hongming_wisdom": 0.06
        },
        "consulting_validation": {
            "civilization_wisdom": 0.20, "civilization_war_economy": 0.16,
            "hongming_wisdom": 0.14, "ru_wisdom": 0.14,
            "sufu_wisdom": 0.14, "dao_wisdom": 0.10, "military_strategy": 0.12
        }
    })

@dataclass
class FusionResult:
    task_id: str
    success: bool
    fused_output: Any
    contributions: list
    fusion_method: FusionMethod
    confidence: float = 0.0
    consistency_score: float = 0.0
    diversity_score: float = 0.0
    execution_time: float = 0.0
    suggestions: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: __import__('datetime').datetime.now().isoformat())

    # [v1.2 道家升级] 上善若水融合结果
    shang_shan_result: Optional["ShangShanResult"] = None
    yin_yang_balance: float = 0.5  # 阴阳平衡度（0=极阴，1=极阳）
