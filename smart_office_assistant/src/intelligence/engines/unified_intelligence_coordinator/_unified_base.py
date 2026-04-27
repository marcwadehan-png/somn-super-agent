"""unified_intelligence_coordinator base: enums & dataclasses v1.0"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

__all__ = [
    'update_performance',
]

logger = logging.getLogger(__name__)

_MODULE_REGISTRY = [
    ("deep_reasoning", ".deep_reasoning_engine", "DeepReasoningEngine", "deep_reasoning"),
    ("sufu_wisdom", ".sufu_wisdom_core", "SufuWisdomCore", "sufu_wisdom"),
    ("military_strategy", ".military_strategy_engine", "MilitaryStrategyEngine", "military_strategy"),
    ("hongming_wisdom", ".hongming_wisdom_core", "HongmingWisdomCore", "hongming_wisdom"),
    ("consulting_validator", ".consulting_validator", "ConsultingValidator", "consulting_validator"),
    ("ancient_wisdom_fusion", ".ancient_wisdom_fusion_core", "AncientWisdomFusionCore", "ancient_wisdom_fusion"),
    ("cross_wisdom_analyzer", ".cross_wisdom_analyzer", "CrossWisdomAnalyzer", "cross_wisdom_analyzer"),
    ("supreme_decision", ".supreme_decision_fusion_engine", "SupremeDecisionFusionEngine", None),
    ("wisdom_reasoning", ".wisdom_reasoning_engine", "WisdomReasoningEngine", None),
    ("enterprise_strategy", ".enterprise_strategy_system", "EnterpriseStrategySystem", None),
    ("talent_assessor", ".wisdom_talent_assessor", "WisdomTalentAssessor", None),
    ("risk_warning", ".wisdom_risk_warning", "WisdomRiskWarningSystem", None),
    ("wisdom_memory_enhancer", "..neural_memory.wisdom_memory_enhancer", "WisdomMemoryEncoder", "wisdom_memory_enhancer"),
    ("wisdom_growth_engine", "..growth_engine.wisdom_growth_engine", "WisdomGrowthEngine", "wisdom_growth_engine"),
    ("metaphysics_wisdom", ".metaphysics_wisdom_unified", "MetaphysicsWisdomUnified", "metaphysics_wisdom"),
    ("civilization_wisdom", ".civilization_wisdom_core", "CivilizationWisdomCore", "civilization_wisdom"),
    ("civilization_war_economy", ".civilization_war_economy_core", "CivilizationWarEconomyCore", "civilization_war_economy"),
    ("mythology_wisdom", ".mythology_wisdom_engine", "MythologyWisdomEngine", "mythology_wisdom"),
    ("literary_narrative", ".literary_narrative_engine", "LiteraryNarrativeEngine", "literary_narrative"),
    ("anthropology_wisdom", ".anthropology_wisdom_engine", "AnthropologyWisdomEngine", "anthropology_wisdom"),
    ("behavior_shaping", ".behavior_shaping_engine", "BehaviorShapingEngine", "behavior_shaping"),
    ("science_thinking", ".science_thinking_engine", "ScienceThinkingEngine", "science_thinking"),
    ("social_science", ".social_science_engine", "SocialScienceWisdomEngine", "social_science"),
    ("yangming_xinxue", ".philosophy.yangming_xinxue_engine", "YangmingXinxueEngine", "yangming_xinxue"),
    ("dewey_thinking", ".dewey_thinking_engine", "DeweyThinkingEngine", "dewey_thinking"),
    ("top_thinking", ".top_thinking_engine", "TopThinkingEngine", "top_thinking"),
    ("supreme_wisdom_coordinator", ".supreme_wisdom_coordinator", "SupremeWisdomCoordinator", "supreme_wisdom_coordinator"),
    ("natural_science", ".natural_science_unified", "NaturalScienceUnified", "natural_science"),
    ("sanjiao_fusion", ".sanjiao_fusion_engine", "SanjiaoFusionEngine", "sanjiao_fusion"),
    ("psychology_pioneer_fusion", ".psychology_pioneer_fusion", "PsychologyPioneerFusionEngine", "psychology_pioneer_fusion"),
    ("dao_wisdom", ".dao_wisdom_core", "DaoWisdomCore", "dao_wisdom"),
    ("tang_song_poetry_fusion", ".tang_song_poetry_fusion", "唐诗宋词fusion模块", "tang_song_poetry_fusion"),
    ("buddha_wisdom", ".buddha_wisdom_core", "BuddhaWisdomCore", "buddha_wisdom"),
    ("growth_engine", "..growth_engine.growth_engine", "SolutionEngineV2", "growth_engine"),
    ("memory_encoding", "..neural_memory.memory_encoding_system_v31", "MemoryEncodingSystemV31", "memory_encoding"),
    ("learning_system", "..learning.unified_learning_system", "UnifiedLearningSystem", "learning_system"),
    # ── 新增推理引擎 v1.0.0 (2026-04-24) ──────────────────────────────────────
    ("long_cot_reasoning", "src.intelligence.reasoning._long_cot_engine", "LongCoTReasoningEngine", "long_cot_reasoning"),
    ("tot_reasoning", "src.intelligence.reasoning._tot_engine", "TreeOfThoughtsEngine", "tot_reasoning"),
    ("react_reasoning", "src.intelligence.reasoning._react_engine", "ReActEngine", "react_reasoning"),
    ("got_reasoning", "src.intelligence.reasoning._got_engine", "GraphOfThoughtsEngine", "got_reasoning"),
]

_LAZY_IMPORT_CACHE: Dict[str, Any] = {}

class TaskType(Enum):
    STRATEGIC_DECISION = "strategic_decision"
    TACTICAL_EXECUTION = "tactical_execution"
    PROBLEM_SOLVING = "problem_solving"
    RISK_ASSESSMENT = "risk_assessment"
    TALENT_EVALUATION = "talent_evaluation"
    GROWTH_PLANNING = "growth_planning"
    CONSULTING_VALIDATION = "consulting_validation"
    LEARNING_OPTIMIZATION = "learning_optimization"
    TIER3_ANALYSIS = "tier3_analysis"

class TaskPriority(Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    BACKGROUND = 4

@dataclass
class TaskContext:
    task_id: str
    task_type: TaskType
    priority: TaskPriority
    user_id: str
    session_id: str
    domain: str = "general"
    industry: Optional[str] = None
    deadline: Optional[datetime] = None
    input_data: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class TaskResult:
    task_id: str
    success: bool
    primary_output: Any
    secondary_outputs: Dict[str, Any] = field(default_factory=dict)
    modules_used: List[str] = field(default_factory=list)
    reasoning_trace: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    execution_time: float = 0.0
    suggestions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    completed_at: str = field(default_factory=lambda: datetime.now().isoformat())

class ModuleCapabilityProfile:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.capabilities = {
            "strategic_decision": 0.0, "tactical_execution": 0.0,
            "problem_solving": 0.0, "risk_assessment": 0.0,
            "talent_evaluation": 0.0, "growth_planning": 0.0,
            "consulting_validation": 0.0, "learning_optimization": 0.0,
        }
        self.domain_expertise = {}
        self.performance_metrics = {}
        self.reliability_score = 0.8

    def update_performance(self, task_type: str, success: bool, execution_time: float):
        if task_type in self.capabilities:
            success_bonus = 0.1 if success else -0.05
            time_factor = 1.0 if execution_time < 5.0 else 0.5
            self.capabilities[task_type] = max(0.0, min(1.0, self.capabilities[task_type] + success_bonus * time_factor))
        self.reliability_score = max(0.1, min(1.0, self.reliability_score + (0.05 if success else -0.1)))
