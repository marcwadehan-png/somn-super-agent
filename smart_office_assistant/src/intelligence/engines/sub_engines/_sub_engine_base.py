"""
增长推理引擎系统 - 子推理引擎基类和注册表
DivineReason Network v3.1 - Sub-Reasoning Engine Base

142个子推理引擎分类:
- 认知推理引擎 (Cognitive): 40个 - 逻辑/归纳/演绎/因果等
- 战略推理引擎 (Strategic): 35个 - 博弈/竞争/风险等
- 创意推理引擎 (Creative): 30个 - 联想/组合/反转等
- 分析推理引擎 (Analytical): 25个 - 相关/聚类/模式识别等
- 决策推理引擎 (Decision): 12个 - 多准则/AHP/决策树等
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
import hashlib
import re

logger = logging.getLogger(__name__)


class EngineCategory(Enum):
    """引擎大类"""
    COGNITIVE = "cognitive"           # 认知推理 (40个)
    STRATEGIC = "strategic"          # 战略推理 (35个)
    CREATIVE = "creative"            # 创意推理 (30个)
    ANALYTICAL = "analytical"        # 分析推理 (25个)
    DECISION = "decision"            # 决策推理 (12个)


class CognitiveSubType(Enum):
    """认知推理子类型 (40个)"""
    # 逻辑推理 (8个)
    DEDUCTIVE = "deductive"              # 演绎推理
    INDUCTIVE = "inductive"              # 归纳推理
    ABDUCTIVE = "abductive"              # 溯因推理
    SYLLOGISTIC = "syllogistic"          # 三段论推理
    PROPOSITIONAL = "propositional"     # 命题逻辑
    PREDICATE = "predicate"              # 谓词逻辑
    MODAL = "modal"                     # 模态逻辑
    TEMPORAL_LOGICAL = "temporal_logical"  # 时序逻辑

    # 因果推理 (8个)
    CAUSAL_CHAIN = "causal_chain"        # 因果链
    CAUSAL_GRAPH = "causal_graph"        # 因果图
    COUNTERFACTUAL = "counterfactual"    # 反事实推理
    INTERVENTION = "intervention"        # 干预分析
    CAUSAL_INFERENCE = "causal_inference"  # 因果推断
    EXPLANATION = "explanation"         # 解释推理
    ATTRIBUTION = "attribution"         #归因推理
    MECHANISM = "mechanism"             # 机制推理

    # 类比推理 (6个)
    STRUCTURAL_ANALOGY = "structural_analogy"  # 结构类比
    FUNCTIONAL_ANALOGY = "functional_analogy"  # 功能类比
    SURFACE_ANALOGY = "surface_analogy"   # 表面类比
    METAPHORICAL = "metaphorical"         # 隐喻推理
    CASE_BASED = "case_based"             # 案例类比
    ANALOGICAL_TRANSFER = "analogical_transfer"  # 类比迁移

    # 概率推理 (6个)
    BAYESIAN = "bayesian"                # 贝叶斯推理
    PROBABILISTIC_GRAPH = "probabilistic_graph"  # 概率图
    MARKOV = "markov"                    # 马尔可夫推理
    MONTE_CARLO = "monte_carlo"          # 蒙特卡洛
    VARIATIONAL = "variational"          # 变分推理
    ENSEMBLE = "ensemble"                # 集成推理

    # 时序推理 (6个)
    TEMPORAL_SEQUENCE = "temporal_sequence"  # 时序推理
    TREND_EXTRAPOLATION = "trend_extrapolation"  # 趋势外推
    SEASONAL = "seasonal"                # 季节性分析
    CYCLIC = "cyclic"                    # 周期推理
    CAUSAL_TEMPORAL = "causal_temporal"  # 因果时序
    FORECASTING = "forecasting"          # 预测推理

    # 空间推理 (3个)
    SPATIAL_RELATION = "spatial_relation"  # 空间关系
    TOPOLOGICAL = "topological"          # 拓扑推理
    GEOMETRIC = "geometric"              # 几何推理

    # 模糊推理 (3个)
    FUZZY_INFERENCE = "fuzzy_inference"  # 模糊推理
    APPROXIMATE = "approximate"          # 近似推理
    LINGUISTIC = "linguistic"            # 语言模糊推理


class StrategicSubType(Enum):
    """战略推理子类型 (35个)"""
    # 博弈论 (8个)
    ZERO_SUM = "zero_sum"                # 零和博弈
    COOPERATIVE = "cooperative"          # 合作博弈
    NON_COOPERATIVE = "non_cooperative"  # 非合作博弈
    EVOLUTIONARY = "evolutionary"        # 演化博弈
    AUCTION = "auction"                  # 拍卖理论
    BARGAINING = "bargaining"            # 议价博弈
    SIGNALING = "signaling"              # 信号博弈
    REPEATED = "repeated"                # 重复博弈

    # 竞争分析 (6个)
    COMPETITIVE_POSITION = "competitive_position"  # 竞争定位
    FIVE_FORCES = "five_forces"          # 五力分析
    SWOT = "swot"                        # SWOT分析
    COMPETITOR_MAP = "competitor_map"    # 竞品地图
    MARKET_STRUCTURE = "market_structure"  # 市场结构
    BARRIER_ANALYSIS = "barrier_analysis"  # 壁垒分析

    # 风险推理 (8个)
    RISK_IDENTIFICATION = "risk_identification"  # 风险识别
    RISK_ASSESSMENT = "risk_assessment"  # 风险评估
    RISK_MITIGATION = "risk_mitigation"  # 风险缓解
    SCENARIO_PLANNING = "scenario_planning"  # 情景规划
    STRESS_TEST = "stress_test"          # 压力测试
    CONTINGENCY = "contingency"          # 应急预案
    MONITORING = "monitoring"            # 风险监控
    HEDGING = "hedging"                  # 对冲策略

    # 长期战略 (7个)
    LONG_TERM_PLANNING = "long_term_planning"  # 长期规划
    VISION_BUILDING = "vision_building"  # 愿景构建
    STRATEGIC_FIT = "strategic_fit"      # 战略匹配
    STAKEHOLDER = "stakeholder"          # 利益相关者
    ROADMAP = "roadmap"                  # 战略路线图
    MILESTONE = "milestone"              # 里程碑规划
    SUSTAINABILITY = "sustainability"    # 可持续战略

    # 联盟与合作 (6个)
    ALLIANCE_FORMATION = "alliance_formation"  # 联盟形成
    PARTNERSHIP = "partnership"          # 合作关系
    SYNERGY = "synergy"                  # 协同效应
    INTEGRATION = "integration"          # 整合战略
    JOINT_VENTURE = "joint_venture"      # 合资企业
    NETWORK_EFFECT = "network_effect"    # 网络效应


class CreativeSubType(Enum):
    """创意推理子类型 (30个)"""
    # 联想思维 (8个)
    ASSOCIATIVE_BRAINSTORM = "associative_brainstorm"  # 联想头脑风暴
    FREE_ASSOCIATION = "free_association"  # 自由联想
    WORD_ASSOCIATION = "word_association"  # 词汇联想
    SEMANTIC_NETWORK = "semantic_network"  # 语义网络
    CONCEPT_MAPPING = "concept_mapping"   # 概念映射
    MIND_MAPPING = "mind_mapping"         # 思维导图
    MEMETIC = "memetic"                   # 模因联想
    CREATIVE_ABSTRACTION = "creative_abstraction"  # 创意抽象

    # 组合创新 (7个)
    COMBINATORIAL = "combinatorial"       # 组合创新
    CROSS_DOMAIN = "cross_domain"        # 跨域组合
    FEATURE_COMBINATION = "feature_combination"  # 特征组合
    ANALOGICAL_COMBINATION = "analogical_combination"  # 类比组合
    UNEXPECTED_COMBINATION = "unexpected_combination"  # 意外组合
    RECOMBINATION = "recombination"      # 重组创新
    HYBRIDIZATION = "hybridization"       # 杂交创新

    # 逆向思维 (5个)
    REVERSE_ANALYSIS = "reverse_analysis"  # 逆向分析
    INVERSE_PROBLEM = "inverse_problem"  # 逆向求解
    CONTRARIAN = "contrarian"            # 反向思考
    WHAT_IF = "what_if"                  # 反向假设
    BACKWARD_INDUCTION = "backward_induction"  # 逆向归纳

    # 横向思维 (5个)
    LATERAL_THINKING = "lateral_thinking"  # 横向思维
    PROVOCATION = "provocation"          # 激发思考
    RANDOM_INPUT = "random_input"        # 随机输入
    ESCAPE = "escape"                    # 逃脱思维
    CHALLENGE_ASSUMPTIONS = "challenge_assumptions"  # 挑战假设

    # 收敛思维 (5个)
    CONVERGENT = "convergent"            # 收敛思维
    SELECTION = "selection"              # 选择收敛
    EVALUATION = "evaluation"            # 评估收敛
    PRIORITIZATION = "prioritization"    # 优先级收敛
    SYNTHESIS = "synthesis"              # 综合收敛


class AnalyticalSubType(Enum):
    """分析推理子类型 (25个)"""
    # 统计推断 (6个)
    CORRELATION = "correlation"          # 相关分析
    REGRESSION = "regression"            # 回归分析
    HYPOTHESIS_TEST = "hypothesis_test"   # 假设检验
    CONFIDENCE = "confidence"            # 置信区间
    SIGNIFICANCE = "significance"         # 显著性分析
    INFERENCE = "statistical_inference"  # 统计推断

    # 模式识别 (6个)
    PATTERN_RECOGNITION = "pattern_recognition"  # 模式识别
    ANOMALY_DETECTION = "anomaly_detection"  # 异常检测
    SEQUENCE_PATTERN = "sequence_pattern"  # 序列模式
    BEHAVIORAL_PATTERN = "behavioral_pattern"  # 行为模式
    TEMPORAL_PATTERN = "temporal_pattern"  # 时序模式
    SPATIAL_PATTERN = "spatial_pattern"    # 空间模式

    # 聚类分析 (4个)
    CLUSTERING = "clustering"             # 聚类分析
    SEGMENTATION = "segmentation"        # 分段分析
    CLASSIFICATION = "classification"     # 分类分析
    TAXONOMY = "taxonomy"                # 分类学分析

    # 因子分析 (4个)
    FACTOR_ANALYSIS = "factor_analysis"  # 因子分析
    PCA = "pca"                         # 主成分分析
    DIMENSIONALITY = "dimensionality"    # 降维分析
    LATENT_VARIABLE = "latent_variable"  # 潜变量分析

    # 数据挖掘 (5个)
    ASSOCIATION_RULES = "association_rules"  # 关联规则
    SEQUENCE_MINING = "sequence_mining"  # 序列挖掘
    TEXT_MINING = "text_mining"          # 文本挖掘
    SOCIAL_NETWORK = "social_network"   # 社交网络分析
    GRAPH_ANALYSIS = "graph_analysis"    # 图分析


class DecisionSubType(Enum):
    """决策推理子类型 (12个)"""
    # 多准则决策 (4个)
    MULTI_CRITERIA = "multi_criteria"    # 多准则决策
    AHP = "ahp"                         # 层次分析法
    TOPSIS = "topsis"                   # TOPSIS法
    VIKOR = "vikor"                     # VIKOR法

    # 决策树方法 (3个)
    DECISION_TREE = "decision_tree"      # 决策树
    CART = "cart"                       # CART算法
    CHAID = "chaid"                     # CHAID算法

    # 效用分析 (3个)
    UTILITY_ANALYSIS = "utility_analysis"  # 效用分析
    EXPECTED_VALUE = "expected_value"    # 期望值分析
    RISK_ADJUSTED = "risk_adjusted"     # 风险调整

    # 情景决策 (2个)
    SCENARIO_DECISION = "scenario_decision"  # 情景决策
    MONTE_CARLO_DECISION = "monte_carlo_decision"  # 蒙特卡洛决策


@dataclass
class ReasoningResult:
    """推理结果"""
    engine_id: str
    engine_name: str
    category: EngineCategory
    success: bool
    result: Any
    confidence: float = 0.0
    reasoning_chain: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # 扩展字段
    insights: List[str] = field(default_factory=list)  # 关键洞察
    recommendations: List[str] = field(default_factory=list)  # 建议

    def to_dict(self) -> Dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "engine_name": self.engine_name,
            "category": self.category.value,
            "success": self.success,
            "result": self.result,
            "confidence": self.confidence,
            "reasoning_chain": self.reasoning_chain,
            "metadata": self.metadata,
            "insights": self.insights,
            "recommendations": self.recommendations,
        }


class SubReasoningEngine(ABC):
    """
    子推理引擎基类

    所有142个子推理引擎都继承此类，实现统一的推理接口。
    """

    def __init__(
        self,
        engine_id: str,
        engine_name: str,
        category: EngineCategory,
        sub_type: Enum,
        description: str = "",
        version: str = "6.2.0",
        capability_score: float = 0.8  # 引擎能力评分
    ):
        self.engine_id = engine_id
        self.engine_name = engine_name
        self.category = category
        self.sub_type = sub_type
        self.description = description
        self.version = version
        self.capability_score = capability_score  # 引擎能力评分
        self._call_count = 0
        self._total_time = 0.0

    @abstractmethod
    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        """
        执行推理

        Args:
            input_data: 输入数据
            context: 推理上下文

        Returns:
            ReasoningResult: 推理结果
        """
        pass

    def _create_result(
        self,
        success: bool,
        result: Any,
        confidence: float,
        reasoning_chain: List[str],
        metadata: Optional[Dict[str, Any]] = None,
        insights: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None
    ) -> ReasoningResult:
        """创建标准推理结果"""
        return ReasoningResult(
            engine_id=self.engine_id,
            engine_name=self.engine_name,
            category=self.category,
            success=success,
            result=result,
            confidence=confidence,
            reasoning_chain=reasoning_chain,
            metadata=metadata or {},
            insights=insights or [],
            recommendations=recommendations or []
        )

    def get_info(self) -> Dict[str, Any]:
        """获取引擎信息"""
        return {
            "engine_id": self.engine_id,
            "engine_name": self.engine_name,
            "category": self.category.value,
            "sub_type": self.sub_type.value if isinstance(self.sub_type, Enum) else self.sub_type,
            "description": self.description,
            "version": self.version,
            "call_count": self._call_count,
        }


class EngineRegistry:
    """
    引擎注册表

    管理142个子推理引擎的注册、查询和调用。
    """

    def __init__(self):
        self._engines: Dict[str, SubReasoningEngine] = {}
        self._engines_by_category: Dict[EngineCategory, List[SubReasoningEngine]] = {
            cat: [] for cat in EngineCategory
        }
        self._engines_by_subtype: Dict[str, SubReasoningEngine] = {}

    def register(self, engine: SubReasoningEngine) -> None:
        """注册引擎"""
        self._engines[engine.engine_id] = engine
        self._engines_by_category[engine.category].append(engine)
        # 处理 sub_type 为 None 的情况
        if engine.sub_type is not None:
            try:
                self._engines_by_subtype[engine.sub_type.value] = engine
            except (AttributeError, TypeError):
                pass
        logger.debug(f"注册引擎: {engine.engine_id} ({engine.engine_name})")

    def get(self, engine_id: str) -> Optional[SubReasoningEngine]:
        """获取引擎"""
        return self._engines.get(engine_id)

    def get_by_subtype(self, subtype: str) -> Optional[SubReasoningEngine]:
        """通过子类型获取引擎"""
        return self._engines_by_subtype.get(subtype)

    def get_by_category(self, category: EngineCategory) -> List[SubReasoningEngine]:
        """获取某类别的所有引擎"""
        return self._engines_by_category.get(category, [])

    def list_all(self) -> List[SubReasoningEngine]:
        """列出所有引擎"""
        return list(self._engines.values())

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计"""
        return {
            "total_engines": len(self._engines),
            "by_category": {
                cat.value: len(engines)
                for cat, engines in self._engines_by_category.items()
            }
        }


# 全局引擎注册表
GLOBAL_ENGINE_REGISTRY = EngineRegistry()


def register_engine(engine: SubReasoningEngine):
    """全局注册引擎的装饰器/函数"""
    GLOBAL_ENGINE_REGISTRY.register(engine)
    return engine


__all__ = [
    # 枚举
    'EngineCategory',
    'CognitiveSubType',
    'StrategicSubType',
    'CreativeSubType',
    'AnalyticalSubType',
    'DecisionSubType',
    # 数据类
    'ReasoningResult',
    # 基类
    'SubReasoningEngine',
    'EngineRegistry',
    # 全局
    'GLOBAL_ENGINE_REGISTRY',
    'register_engine',
]
