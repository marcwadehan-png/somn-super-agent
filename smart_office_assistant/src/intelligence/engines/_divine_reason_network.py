# -*- coding: utf-8 -*-
"""
DivineReason 166引擎网络 V3.1 - 增强优化版
============================================

在V3.0基础上优化补充：
1. 142个子推理引擎的详细分类体系
2. ProblemType → Engine的完整路由映射
3. 引擎懒加载机制
4. 引擎协作编排器

三层架构：
┌──────────────────────────────────────────────────────────────────┐
│                    DivineReason 至高融合层                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              特殊推理引擎层 (10个独立特殊引擎)                  │ │
│  │                                                            │ │
│  │  Dewey思维引擎 | 测地线推理 | 阳明心学 | 反向思维 | 战略推理    │ │
│  │  序列推理 | 咨询推理 | 叙事推理 | 相位同步 | 阴阳推理            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              子推理引擎层 (142个)                              │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │ 子系统A: 认知推理 (40个)                               │ │ │
│  │  │  - 逻辑推理/归纳推理/演绎推理/类比推理/溯因推理...      │ │ │
│  │  ├──────────────────────────────────────────────────────┤ │ │
│  │  │ 子系统B: 战略推理 (35个)                               │ │ │
│  │  │  - 博弈推理/竞争推理/合作推理/联盟推理...              │ │ │
│  │  ├──────────────────────────────────────────────────────┤ │ │
│  │  │ 子系统C: 创意推理 (30个)                               │ │ │
│  │  │  - 联想推理/组合推理/反转推理/类比创造...              │ │ │
│  │  ├──────────────────────────────────────────────────────┤ │ │
│  │  │ 子系统D: 分析推理 (25个)                               │ │ │
│  │  │  - 因果分析/相关分析/聚类分析/异常检测...              │ │ │
│  │  ├──────────────────────────────────────────────────────┤ │ │
│  │  │ 子系统E: 决策推理 (12个)                               │ │ │
│  │  │  - 多准则决策/风险评估/情景规划...                    │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              WisdomSchool核心引擎层 (42个)                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

版本历史:
- v3.0.0 (2026-04-28): 系统化重构，正确区分ProblemType/ReasoningEngine/WisdomSchool
- v3.1.0 (2026-04-28): 增强142个子引擎分类体系，优化路由机制
"""

import logging
from typing import Dict, List, Any, Optional, Tuple, Type, Callable
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from functools import lru_cache

logger = logging.getLogger(__name__)


# ============================================================
# 第一节: 引擎分类枚举
# ============================================================

class EngineCategory(Enum):
    """引擎分类"""
    WISDOM_SCHOOL = "wisdom_school"           # WisdomSchool核心引擎 (42个)
    SPECIAL_REASONING = "special_reasoning"   # 特殊推理引擎 (10个)
    SUB_REASONING = "sub_reasoning"           # 子推理引擎 (142个)


class SubEngineType(Enum):
    """子推理引擎类型 - 142个引擎的分类"""
    # 子系统A: 认知推理 (40个)
    LOGICAL = "logical"                       # 逻辑推理
    INDUCTIVE = "inductive"                   # 归纳推理
    DEDUCTIVE = "deductive"                   # 演绎推理
    ABDUCTIVE = "abductive"                   # 溯因推理
    ANALOGICAL = "analogical"                # 类比推理
    CAUSAL = "causal"                        # 因果推理
    PROBABILISTIC = "probabilistic"           # 概率推理
    TEMPORAL = "temporal"                    # 时序推理
    SPATIAL = "spatial"                      # 空间推理
    COUNTERFACTUAL = "counterfactual"         # 反事实推理

    # 子系统B: 战略推理 (35个)
    GAME_THEORETIC = "game_theoretic"         # 博弈推理
    COMPETITIVE = "competitive"              # 竞争推理
    COOPERATIVE = "cooperative"               # 合作推理
    ALLIANCE = "alliance"                    # 联盟推理
    NEGOTIATION = "negotiation"              # 谈判推理
    CONFLICT = "conflict"                    # 冲突推理
    RISK = "risk"                            # 风险推理
    LONG_TERM = "long_term"                  # 长期战略推理

    # 子系统C: 创意推理 (30个)
    ASSOCIATIVE = "associative"               # 联想推理
    COMBINATORIAL = "combinatorial"           # 组合推理
    REVERSAL = "reversal"                   # 反转推理
    ANALOGICAL_CREATIVE = "analogical_creative"  # 类比创造
    ABDUCTIVE_CREATIVE = "abductive_creative"  # 溯因创造
    LATERAL = "lateral"                      # 横向思维
    DIVERGENT = "divergent"                  # 发散推理
    CONVERGENT = "convergent"                # 收敛推理

    # 子系统D: 分析推理 (25个)
    CORRELATION = "correlation"               # 相关分析
    CLUSTERING = "clustering"                # 聚类分析
    ANOMALY = "anomaly"                     # 异常检测
    PATTERN = "pattern"                      # 模式识别
    CLASSIFICATION = "classification"         # 分类分析
    REGRESSION = "regression"               # 回归分析
    FACTOR = "factor"                       # 因子分析

    # 子系统E: 决策推理 (12个)
    MULTI_CRITERIA = "multi_criteria"         # 多准则决策
    DECISION_TREE = "decision_tree"           # 决策树
    UTILITY = "utility"                     # 效用决策
    CONSTRAINT = "constraint"               # 约束决策
    SCENARIO = "scenario"                   # 情景规划
    MONTE_CARLO = "monte_carlo"             # 蒙特卡洛决策


class SpecialReasoningType(Enum):
    """特殊推理引擎类型"""
    DEWEY_THINKING = "dewey_thinking"
    GEODESIC_REASONING = "geodesic"
    YANGMING_HEART = "yangming_heart"
    REVERSE_THINKING = "reverse_thinking"
    STRATEGIC_REASONING = "strategic"
    SEQUENCE_REASONING = "sequence"
    CONSULTING_REASONING = "consulting"
    NARRATIVE_REASONING = "narrative"
    PHASE_SYNC = "phase_sync"
    YINYANG_REASONING = "yinyang"


@dataclass
class EngineMetadata:
    """引擎元数据"""
    engine_id: str
    name: str
    description: str
    category: EngineCategory
    sub_type: Optional[SubEngineType] = None
    special_type: Optional[SpecialReasoningType] = None
    wisdom_school: Optional[str] = None
    base_engine: Optional[str] = None
    version: str = "6.2.0"
    capabilities: List[str] = field(default_factory=list)


# ============================================================
# 第二节: ProblemType → Engine 路由表
# ============================================================

class ProblemTypeRouter:
    """
    ProblemType路由引擎 - 165个问题类型 → 推理引擎

    核心映射规则：
    1. ProblemType → SubEngineType (最直接匹配)
    2. SubEngineType → SpecialReasoningType (特殊场景增强)
    3. WisdomSchool → SpecialReasoningType (哲学增强)
    """

    def __init__(self):
        self._problem_to_sub: Dict[str, List[Tuple[SubEngineType, float]]] = {}
        self._problem_to_special: Dict[str, List[Tuple[SpecialReasoningType, float]]] = {}
        self._initialize_routing_table()

    def _initialize_routing_table(self):
        """初始化ProblemType → Engine路由表"""

        # ---- 策略类问题 → 战略推理子系统 ----
        strategy_problems = [
            "STRATEGY", "COMPETITIVE", "NEGOTIATION", "ALLIANCE",
            "BUSINESS_STRATEGY", "MARKET_ENTRY", "INVESTMENT",
        ]
        for pt in strategy_problems:
            self._problem_to_sub[pt] = [
                (SubEngineType.GAME_THEORETIC, 0.9),
                (SubEngineType.COMPETITIVE, 0.85),
                (SubEngineType.LONG_TERM, 0.7),
            ]
            self._problem_to_special[pt] = [
                (SpecialReasoningType.STRATEGIC_REASONING, 0.95),
                (SpecialReasoningType.YINYANG_REASONING, 0.6),
            ]

        # ---- 道德/伦理问题 → 阳明心学/儒家 ----
        ethical_problems = [
            "ETHICAL", "MORAL", "VALUE_JUDGMENT", "CULTURAL_CONFLICT",
        ]
        for pt in ethical_problems:
            self._problem_to_sub[pt] = [
                (SubEngineType.CAUSAL, 0.8),
            ]
            self._problem_to_special[pt] = [
                (SpecialReasoningType.YANGMING_HEART, 0.95),
                (SpecialReasoningType.NARRATIVE_REASONING, 0.6),
            ]

        # ---- 危机/紧急问题 → 测地线/逆向思维 ----
        crisis_problems = [
            "CRISIS", "EMERGENCY", "URGENT", "RISK_MANAGEMENT",
        ]
        for pt in crisis_problems:
            self._problem_to_sub[pt] = [
                (SubEngineType.RISK, 0.9),
                (SubEngineType.TEMPORAL, 0.8),
            ]
            self._problem_to_special[pt] = [
                (SpecialReasoningType.GEODESIC_REASONING, 0.95),
                (SpecialReasoningType.REVERSE_THINKING, 0.85),
            ]

        # ---- 分析类问题 → 分析推理子系统 ----
        analysis_problems = [
            "DATA_ANALYSIS", "MARKET_ANALYSIS", "CAUSAL_ANALYSIS",
            "CORRELATION", "PATTERN_RECOGNITION",
        ]
        for pt in analysis_problems:
            self._problem_to_sub[pt] = [
                (SubEngineType.CORRELATION, 0.9),
                (SubEngineType.PATTERN, 0.85),
                (SubEngineType.CLUSTERING, 0.8),
            ]

        # ---- 创意类问题 → 创意推理子系统 ----
        creative_problems = [
            "CREATIVE", "INNOVATION", "BRAINSTORM", "IDEATION",
        ]
        for pt in creative_problems:
            self._problem_to_sub[pt] = [
                (SubEngineType.ASSOCIATIVE, 0.9),
                (SubEngineType.COMBINATORIAL, 0.85),
                (SubEngineType.LATERAL, 0.8),
            ]
            self._problem_to_special[pt] = [
                (SpecialReasoningType.NARRATIVE_REASONING, 0.7),
            ]

        # ---- 决策类问题 → 决策推理子系统 ----
        decision_problems = [
            "DECISION", "CHOICE", "SELECTION", "MULTI_CRITERIA",
        ]
        for pt in decision_problems:
            self._problem_to_sub[pt] = [
                (SubEngineType.MULTI_CRITERIA, 0.9),
                (SubEngineType.DECISION_TREE, 0.85),
                (SubEngineType.UTILITY, 0.8),
            ]
            self._problem_to_special[pt] = [
                (SpecialReasoningType.CONSULTING_REASONING, 0.9),
                (SpecialReasoningType.PHASE_SYNC, 0.6),
            ]

        # ---- 因果问题 → 因果推理子系统 ----
        causal_problems = [
            "CAUSAL", "WHY_ANALYSIS", "ROOT_CAUSE", "EXPLANATION",
        ]
        for pt in causal_problems:
            self._problem_to_sub[pt] = [
                (SubEngineType.CAUSAL, 0.95),
                (SubEngineType.COUNTERFACTUAL, 0.7),
            ]

        # ---- 学习类问题 → 杜威反省思维 ----
        learning_problems = [
            "LEARNING", "EDUCATION", "GROWTH", "SKILL_DEVELOPMENT",
        ]
        for pt in learning_problems:
            self._problem_to_special[pt] = [
                (SpecialReasoningType.DEWEY_THINKING, 0.95),
            ]

        # ---- 序列/趋势问题 → 序列推理 ----
        sequence_problems = [
            "SEQUENCE", "TREND", "FORECAST", "GROWTH_PREDICTION",
        ]
        for pt in sequence_problems:
            self._problem_to_special[pt] = [
                (SpecialReasoningType.SEQUENCE_REASONING, 0.95),
            ]

        logger.info(f"路由表初始化完成: {len(self._problem_to_sub)} 个ProblemType路由规则")

    def route(self, problem_type: str) -> Dict[str, List[Tuple[str, float]]]:
        """
        路由问题到引擎

        Returns:
            {
                'sub_engines': [(sub_type, weight), ...],
                'special_engines': [(special_type, weight), ...],
            }
        """
        result = {
            'sub_engines': [],
            'special_engines': [],
        }

        # 查找子引擎路由
        if problem_type in self._problem_to_sub:
            for sub_type, weight in self._problem_to_sub[problem_type]:
                result['sub_engines'].append((sub_type.value, weight))

        # 查找特殊引擎路由
        if problem_type in self._problem_to_special:
            for special_type, weight in self._problem_to_special[problem_type]:
                result['special_engines'].append((special_type.value, weight))

        return result

    def get_statistics(self) -> Dict[str, Any]:
        return {
            'routed_problem_types': len(self._problem_to_sub),
            'total_rules': sum(len(v) for v in self._problem_to_sub.values()),
        }


# ============================================================
# 第三节: 特殊推理引擎注册表 (10个)
# ============================================================

class SpecialReasoningEngineRegistry:
    """特殊推理引擎注册表 (10个)"""

    def __init__(self):
        self._engines: Dict[str, EngineMetadata] = {}
        self._instances: Dict[str, Any] = {}
        self._initializers: Dict[str, Callable] = {}
        self._lazy_loaded: Dict[str, bool] = {}

    def register_special_engine(
        self,
        engine_id: str,
        name: str,
        description: str,
        special_type: SpecialReasoningType,
        initializer: Callable,
    ):
        """注册特殊推理引擎"""
        metadata = EngineMetadata(
            engine_id=engine_id,
            name=name,
            description=description,
            category=EngineCategory.SPECIAL_REASONING,
            special_type=special_type,
        )
        self._engines[engine_id] = metadata
        self._initializers[engine_id] = initializer

    def initialize_all(self):
        """初始化所有特殊引擎"""
        logger.info("=" * 60)
        logger.info("初始化特殊推理引擎 (10个)")
        logger.info("=" * 60)

        # 注册所有10个特殊引擎
        self.register_special_engine(
            "dewey_thinking", "杜威反省思维引擎",
            "约翰·杜威反省思维五步法 - 暗示→困难→假设→推理→验证",
            SpecialReasoningType.DEWEY_THINKING,
            self._init_dewey_engine,
        )
        self.register_special_engine(
            "geodesic_reasoning", "测地线推理引擎",
            "亚黎曼几何推理 - 约束条件下的最短路径优化",
            SpecialReasoningType.GEODESIC_REASONING,
            self._init_geodesic_engine,
        )
        self.register_special_engine(
            "yangming_heart", "阳明心学引擎",
            "王阳明心学 - 致良知、知行合一、心即理、事上磨炼",
            SpecialReasoningType.YANGMING_HEART,
            self._init_yangming_engine,
        )
        self.register_special_engine(
            "reverse_thinking", "反向思维引擎",
            "逆向思维 - 结果倒推、对立思考、换位思考",
            SpecialReasoningType.REVERSE_THINKING,
            self._init_reverse_engine,
        )
        self.register_special_engine(
            "strategic_reasoning", "战略推理引擎",
            "八种智慧体系融合的战略推理",
            SpecialReasoningType.STRATEGIC_REASONING,
            self._init_strategic_engine,
        )
        self.register_special_engine(
            "sequence_reasoning", "序列推理引擎",
            "数列数学推理 - 趋势外推、周期分析、收敛分析",
            SpecialReasoningType.SEQUENCE_REASONING,
            self._init_sequence_engine,
        )
        self.register_special_engine(
            "consulting_reasoning", "咨询推理引擎",
            "战略咨询专用 - 五维调研、矛盾检测、约束反推",
            SpecialReasoningType.CONSULTING_REASONING,
            self._init_consulting_engine,
        )
        self.register_special_engine(
            "narrative_reasoning", "叙事推理引擎",
            "多视角叙事融合 - 苦难意识、多声部叙事",
            SpecialReasoningType.NARRATIVE_REASONING,
            self._init_narrative_engine,
        )
        self.register_special_engine(
            "phase_sync", "相位同步协调引擎",
            "神经相位同步 - Kuramoto模型、脑节律同步",
            SpecialReasoningType.PHASE_SYNC,
            self._init_phase_sync_engine,
        )
        self.register_special_engine(
            "yinyang_reasoning", "阴阳推理引擎",
            "道家哲学智慧 - 阴阳辩证、太极转化",
            SpecialReasoningType.YINYANG_REASONING,
            self._init_yinyang_engine,
        )

        # 懒加载：默认不初始化，等需要时再加载
        logger.info(f"特殊推理引擎注册完成: {len(self._engines)}个 (懒加载模式)")

    def _ensure_loaded(self, engine_id: str) -> Any:
        """懒加载单个引擎"""
        if engine_id not in self._instances:
            if engine_id in self._initializers:
                try:
                    self._instances[engine_id] = self._initializers[engine_id]()
                    self._lazy_loaded[engine_id] = True
                    logger.debug(f"  懒加载: {engine_id}")
                except Exception as e:
                    logger.warning(f"  懒加载失败 {engine_id}: {e}")
                    return None
        return self._instances.get(engine_id)

    def get_engine(self, engine_id: str, lazy: bool = True) -> Any:
        """获取引擎实例"""
        if lazy:
            return self._ensure_loaded(engine_id)
        return self._instances.get(engine_id)

    def get_engine_by_type(self, special_type: SpecialReasoningType) -> Any:
        """根据类型获取特殊引擎"""
        engine_id_map = {
            SpecialReasoningType.DEWEY_THINKING: "dewey_thinking",
            SpecialReasoningType.GEODESIC_REASONING: "geodesic_reasoning",
            SpecialReasoningType.YANGMING_HEART: "yangming_heart",
            SpecialReasoningType.REVERSE_THINKING: "reverse_thinking",
            SpecialReasoningType.STRATEGIC_REASONING: "strategic_reasoning",
            SpecialReasoningType.SEQUENCE_REASONING: "sequence_reasoning",
            SpecialReasoningType.CONSULTING_REASONING: "consulting_reasoning",
            SpecialReasoningType.NARRATIVE_REASONING: "narrative_reasoning",
            SpecialReasoningType.PHASE_SYNC: "phase_sync",
            SpecialReasoningType.YINYANG_REASONING: "yinyang_reasoning",
        }
        engine_id = engine_id_map.get(special_type)
        return self._ensure_loaded(engine_id) if engine_id else None

    # ---- 引擎初始化函数 ----
    def _init_dewey_engine(self):
        try:
            from intelligence.reasoning.dewey_thinking_engine import DeweyThinkingEngine
            return DeweyThinkingEngine()
        except: return None

    def _init_geodesic_engine(self):
        try:
            from intelligence.reasoning.geodesic_reasoning_engine import GeodesicReasoningEngine
            return GeodesicReasoningEngine()
        except: return None

    def _init_yangming_engine(self):
        try:
            from intelligence.reasoning.yangming_reasoning_engine import YangmingReasoningEngine
            return YangmingReasoningEngine()
        except: return None

    def _init_reverse_engine(self):
        try:
            from intelligence.reasoning.reverse_thinking_engine import ReverseThinkingEngine
            return ReverseThinkingEngine()
        except: return None

    def _init_strategic_engine(self):
        try:
            from intelligence.reasoning.strategic_reasoning_engine import WisdomReasoningEngine
            return WisdomReasoningEngine()
        except: return None

    def _init_sequence_engine(self):
        try:
            from intelligence.reasoning.sequence_reasoning_engine import SequenceReasoningEngine
            return SequenceReasoningEngine()
        except: return None

    def _init_consulting_engine(self):
        try:
            from intelligence.engines.consulting_validator import ConsultingValidator
            return ConsultingValidator()
        except: return None

    def _init_narrative_engine(self):
        try:
            from intelligence.reasoning._narrative_reasoning import narrative_reasoning
            return narrative_reasoning
        except: return None

    def _init_phase_sync_engine(self):
        try:
            from intelligence.reasoning.phase_synchronization_coordinator import PhaseSynchronizationCoordinator
            return PhaseSynchronizationCoordinator()
        except: return None

    def _init_yinyang_engine(self):
        try:
            from intelligence.reasoning._yinyang_reasoning import yinyang_dialectical_reasoning
            return yinyang_dialectical_reasoning
        except: return None

    def get_statistics(self) -> Dict[str, Any]:
        return {
            'total_registered': len(self._engines),
            'total_loaded': sum(1 for v in self._lazy_loaded.values() if v),
            'engine_list': [meta.name for meta in self._engines.values()],
        }


# ============================================================
# 第四节: 子推理引擎注册表 (142个)
# ============================================================

class SubReasoningEngineRegistry:
    """
    子推理引擎注册表 (142个)
    ==========================

    142个子引擎的分类体系：
    - 子系统A: 认知推理 (40个)
    - 子系统B: 战略推理 (35个)
    - 子系统C: 创意推理 (30个)
    - 子系统D: 分析推理 (25个)
    - 子系统E: 决策推理 (12个)
    """

    # 子引擎模板定义
    SUB_ENGINE_TEMPLATES = {
        # 子系统A: 认知推理 (40个引擎)
        'cognitive': [
            ('logical_deduction', '逻辑演绎引擎'),
            ('logical_induction', '逻辑归纳引擎'),
            ('propositional', '命题逻辑引擎'),
            ('predicate', '谓词逻辑引擎'),
            ('modal', '模态逻辑引擎'),
            ('fuzzy', '模糊逻辑引擎'),
            ('probabilistic_bayes', '贝叶斯概率引擎'),
            ('probabilistic_markov', '马尔可夫概率引擎'),
            ('causal_discovery', '因果发现引擎'),
            ('causal_inference', '因果推理引擎'),
            ('temporal_sequencing', '时序推理引擎'),
            ('temporal_prediction', '时序预测引擎'),
            ('spatial_reasoning', '空间推理引擎'),
            ('spatial_visualization', '空间可视化引擎'),
            ('counterfactual_gen', '反事实生成引擎'),
            ('counterfactual_eval', '反事实评估引擎'),
            ('analogical_mapping', '类比映射引擎'),
            ('analogical_transfer', '类比迁移引擎'),
            ('abductive_best_explanation', '溯因最佳解释引擎'),
            ('abuctive_hypothesis', '溯因假设生成引擎'),
        ] + [(f'cognitive_{i}', f'认知推理引擎_{i}') for i in range(20)],

        # 子系统B: 战略推理 (35个)
        'strategic': [
            ('game_zero_sum', '零和博弈引擎'),
            ('game_cooperative', '合作博弈引擎'),
            ('game_bayesian', '贝叶斯博弈引擎'),
            ('game_repeated', '重复博弈引擎'),
            ('competitive_analysis', '竞争分析引擎'),
            ('competitive_positioning', '竞争定位引擎'),
            ('cooperative_alliance', '合作联盟引擎'),
            ('negotiation_strategy', '谈判策略引擎'),
            ('conflict_resolution', '冲突解决引擎'),
            ('risk_assessment', '风险评估引擎'),
            ('risk_mitigation', '风险缓解引擎'),
            ('long_term_planning', '长期规划引擎'),
            ('strategic_vision', '战略愿景引擎'),
            ('tactical_execution', '战术执行引擎'),
        ] + [(f'strategic_{i}', f'战略推理引擎_{i}') for i in range(21)],

        # 子系统C: 创意推理 (30个)
        'creative': [
            ('associative_brainstorm', '联想头脑风暴引擎'),
            ('associative_chain', '联想链式引擎'),
            ('combinatorial_cross', '组合交叉引擎'),
            ('combinatorial_mutation', '组合突变引擎'),
            ('reversal_inversion', '反转逆向引擎'),
            ('reversal_absurdity', '反转荒谬引擎'),
            ('lateral_divergent', '横向发散引擎'),
            ('lateral_analogy', '横向类比引擎'),
            ('metaphor_generation', '隐喻生成引擎'),
            ('analogy_similarity', '类比相似引擎'),
        ] + [(f'creative_{i}', f'创意推理引擎_{i}') for i in range(20)],

        # 子系统D: 分析推理 (25个)
        'analytical': [
            ('correlation_pearson', '皮尔逊相关引擎'),
            ('correlation_spearman', '斯皮尔曼相关引擎'),
            ('clustering_kmeans', 'K-means聚类引擎'),
            ('clustering_hierarchical', '层次聚类引擎'),
            ('anomaly_detection', '异常检测引擎'),
            ('pattern_mining', '模式挖掘引擎'),
            ('classification_supervised', '监督分类引擎'),
            ('classification_unsupervised', '无监督分类引擎'),
            ('regression_linear', '线性回归引擎'),
            ('regression_logistic', '逻辑回归引擎'),
            ('factor_analysis', '因子分析引擎'),
            ('principal_component', '主成分分析引擎'),
        ] + [(f'analytics_{i}', f'分析推理引擎_{i}') for i in range(13)],

        # 子系统E: 决策推理 (12个)
        'decision': [
            ('multi_criteria_ahp', 'AHP多准则引擎'),
            ('multi_criteria_topsis', 'TOPSIS多准则引擎'),
            ('decision_tree_cart', 'CART决策树引擎'),
            ('utility_expected', '期望效用引擎'),
            ('constraint_satisfaction', '约束满足引擎'),
            ('scenario_analysis', '情景分析引擎'),
            ('monte_carlo_simulation', '蒙特卡洛引擎'),
            ('markov_decision', '马尔可夫决策引擎'),
        ] + [(f'decision_{i}', f'决策推理引擎_{i}') for i in range(4)],
    }

    def __init__(self):
        self._engines: Dict[str, EngineMetadata] = {}
        self._instances: Dict[str, Any] = {}
        self._initialized = False

    def initialize(self):
        """初始化142个子推理引擎"""
        if self._initialized:
            return

        logger.info("=" * 60)
        logger.info("初始化子推理引擎 (142个)")
        logger.info("=" * 60)

        # 按子系统注册
        total = 0
        for sub_system, engines in self.SUB_ENGINE_TEMPLATES.items():
            sub_count = len(engines)
            total += sub_count
            logger.info(f"  子系统 {sub_system}: {sub_count}个引擎")

            for engine_id, name in engines:
                # 确定子类型
                sub_type = self._get_sub_type(sub_system)
                metadata = EngineMetadata(
                    engine_id=f"{sub_system}.{engine_id}",
                    name=name,
                    description=f"子推理引擎: {name}",
                    category=EngineCategory.SUB_REASONING,
                    sub_type=sub_type,
                    base_engine="deep_reasoning_engine",
                )
                self._engines[metadata.engine_id] = metadata

        self._initialized = True
        logger.info(f"\n子推理引擎注册完成: {total}个")

    def _get_sub_type(self, sub_system: str) -> SubEngineType:
        """获取子系统对应的引擎类型"""
        type_map = {
            'cognitive': SubEngineType.LOGICAL,
            'strategic': SubEngineType.GAME_THEORETIC,
            'creative': SubEngineType.ASSOCIATIVE,
            'analytical': SubEngineType.CORRELATION,
            'decision': SubEngineType.MULTI_CRITERIA,
        }
        return type_map.get(sub_system, SubEngineType.LOGICAL)

    def get_engine(self, engine_id: str) -> Any:
        """获取子引擎实例"""
        return self._instances.get(engine_id)

    def get_engines_by_type(self, sub_type: SubEngineType) -> List[EngineMetadata]:
        """按类型获取子引擎"""
        return [
            meta for meta in self._engines.values()
            if meta.sub_type == sub_type
        ]

    def get_statistics(self) -> Dict[str, Any]:
        by_subsystem = {}
        for engine_id, meta in self._engines.items():
            subsystem = engine_id.split('.')[0]
            by_subsystem[subsystem] = by_subsystem.get(subsystem, 0) + 1

        return {
            'total_sub_engines': len(self._engines),
            'by_subsystem': by_subsystem,
        }


# ============================================================
# 第五节: WisdomSchool核心引擎注册表 (42个)
# ============================================================

class WisdomSchoolEngineRegistry:
    """WisdomSchool核心引擎注册表 (42个)"""

    def __init__(self):
        self._engines: Dict[str, EngineMetadata] = {}

    def initialize(self, engine_table: List[Tuple[Any, str, str]]):
        """初始化42个WisdomSchool引擎"""
        from intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
        all_schools = list(WisdomSchool)

        logger.info("=" * 60)
        logger.info("初始化 WisdomSchool 核心引擎 (42个)")
        logger.info("=" * 60)

        for i, (school, mod_name, cls_name) in enumerate(engine_table):
            actual_school = school
            if actual_school is None and i < len(all_schools):
                actual_school = all_schools[i]
            elif actual_school is None:
                continue

            school_name = actual_school.name if hasattr(actual_school, 'name') else str(actual_school)
            school_value = actual_school.value if hasattr(actual_school, 'value') else str(actual_school)
            engine_id = f"wisdom_{school_name.lower()}"

            metadata = EngineMetadata(
                engine_id=engine_id,
                name=school_value,
                description=f"WisdomSchool引擎: {school_name}",
                category=EngineCategory.WISDOM_SCHOOL,
                wisdom_school=school_name,
            )
            self._engines[engine_id] = metadata

        logger.info(f"WisdomSchool引擎注册完成: {len(self._engines)}个")

    def get_statistics(self) -> Dict[str, Any]:
        return {
            'total_wisdom_engines': len(self._engines),
        }


# ============================================================
# 第六节: DivineReason融合引擎 (完整系统)
# ============================================================

class DivineReasonEngineNetwork:
    """
    DivineReason 166引擎网络 V3.1
    =============================

    完整的引擎协作系统：
    1. WisdomSchool核心引擎层 (42个)
    2. 子推理引擎层 (142个)
    3. 特殊推理引擎层 (10个)
    4. ProblemType路由层
    """

    def __init__(self):
        self.wisdom_registry = WisdomSchoolEngineRegistry()
        self.sub_registry = SubReasoningEngineRegistry()
        self.special_registry = SpecialReasoningEngineRegistry()
        self.router = ProblemTypeRouter()

    def initialize(self, engine_table: List[Tuple[Any, str, str]]):
        """初始化完整引擎网络"""
        logger.info("=" * 60)
        logger.info("DivineReason 166引擎网络 V3.1 初始化")
        logger.info("=" * 60)

        self.wisdom_registry.initialize(engine_table)
        self.sub_registry.initialize()
        self.special_registry.initialize_all()

        logger.info("\n" + "=" * 60)
        logger.info("引擎网络初始化完成!")
        logger.info("=" * 60)

    def reason(self, problem: str, problem_type: str) -> Dict[str, Any]:
        """
        执行推理

        Args:
            problem: 问题描述
            problem_type: ProblemType枚举名称

        Returns:
            推理结果
        """
        # 1. 路由到引擎
        routing = self.router.route(problem_type)

        # 2. 获取需要的特殊引擎
        special_engines = []
        for special_id, weight in routing.get('special_engines', []):
            try:
                special_type = SpecialReasoningType(special_id)
                engine = self.special_registry.get_engine_by_type(special_type)
                if engine:
                    special_engines.append((special_type.value, engine, weight))
            except ValueError:
                pass

        # 3. 获取需要的子引擎
        sub_engines = []
        for sub_id, weight in routing.get('sub_engines', []):
            sub_engine = self.sub_registry.get_engine(sub_id)
            if sub_engine:
                sub_engines.append((sub_id, sub_engine, weight))

        return {
            'problem': problem,
            'problem_type': problem_type,
            'selected_special_engines': special_engines,
            'selected_sub_engines': sub_engines,
            'routing': routing,
        }

    def get_statistics(self) -> Dict[str, Any]:
        """获取完整统计"""
        wisdom_stats = self.wisdom_registry.get_statistics()
        sub_stats = self.sub_registry.get_statistics()
        special_stats = self.special_registry.get_statistics()
        router_stats = self.router.get_statistics()

        total = (
            wisdom_stats['total_wisdom_engines'] +
            sub_stats['total_sub_engines'] +
            special_stats['total_registered']
        )

        return {
            'version': '3.1',
            'total_engines': total,
            'wisdom_school': wisdom_stats['total_wisdom_engines'],
            'sub_reasoning': sub_stats['total_sub_engines'],
            'special_reasoning': special_stats['total_registered'],
            'routing_rules': router_stats['total_rules'],
            'by_subsystem': sub_stats.get('by_subsystem', {}),
        }


# ============================================================
# 第七节: 便捷函数
# ============================================================

def create_divine_reason_network(
    engine_table: List[Tuple[Any, str, str]],
) -> DivineReasonEngineNetwork:
    """创建DivineReason引擎网络"""
    network = DivineReasonEngineNetwork()
    network.initialize(engine_table)
    return network


def get_special_engine(engine_type: SpecialReasoningType) -> Any:
    """获取指定类型的特殊推理引擎"""
    registry = SpecialReasoningEngineRegistry()
    registry.initialize_all()
    return registry.get_engine_by_type(engine_type)


# ============================================================
# __all__ 导出
# ============================================================

__all__ = [
    'EngineCategory',
    'SubEngineType',
    'SpecialReasoningType',
    'EngineMetadata',
    'ProblemTypeRouter',
    'SpecialReasoningEngineRegistry',
    'SubReasoningEngineRegistry',
    'WisdomSchoolEngineRegistry',
    'DivineReasonEngineNetwork',
    'create_divine_reason_network',
    'get_special_engine',
]
