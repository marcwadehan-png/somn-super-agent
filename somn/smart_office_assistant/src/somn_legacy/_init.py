"""
__all__ = [
    'init_layer1',
    'init_layer2',
    'init_layer3',
    'init_layer4',
    'init_layer5',
    'init_narrative_layer',
]

Somn 初始化逻辑 - 从 somn.py 拆分
包含各层初始化方法
"""

import logging

logger = logging.getLogger(__name__)

def init_layer1(self):
    """init基础层"""
    from src.tool_layer import ToolRegistry, LLMService

    logger.info("[Layer 1] init基础层...")
    self._layers['tool_registry'] = ToolRegistry()
    self._layers['llm_service'] = LLMService()
    logger.info("[Layer 1] 基础层init完成")

def init_kg_engine(self):
    """init知识图谱引擎（独立懒加载）"""
    if 'kg_engine' in self._layers:
        return
    from src.knowledge_graph import KnowledgeGraphEngine, ConceptManager, IndustryKnowledgeBase
    if self.config.enable_knowledge_graph:
        self._layers['kg_engine'] = KnowledgeGraphEngine()
        self._layers['concept_manager'] = ConceptManager()
        self._layers['industry_knowledge'] = IndustryKnowledgeBase()
        logger.info("  - 知识图谱引擎: 已启用")


def init_web_search(self):
    """init全网搜索（独立懒加载）"""
    if 'web_search' in self._layers:
        return
    from src.data_layer import WebSearchEngine, DataCollector
    if self.config.enable_web_search:
        self._layers['web_search'] = WebSearchEngine()
        self._layers['data_collector'] = DataCollector()
        logger.info("  - 全网搜索: 已启用")


def init_memory_system(self):
    """init神经记忆系统（独立懒加载）"""
    if 'memory_system' in self._layers:
        return
    from src.neural_memory import NeuralMemorySystem
    if self.config.enable_neural_memory:
        self._layers['memory_system'] = NeuralMemorySystem()
        logger.info("  - 神经记忆系统: 已启用")


def init_layer2(self):
    """init数据层（兼容包装器，依次调用三个独立初始化）"""
    logger.info("[Layer 2] init数据层...")
    init_kg_engine(self)
    init_web_search(self)
    init_memory_system(self)
    logger.info("[Layer 2] 数据层init完成")

def init_layer3(self):
    """init智能层"""
    from src.ml_engine import UserClassifier, TimeSeriesForecaster

    logger.info("[Layer 3] init智能层...")

    if self.config.enable_ml_engine:
        self._layers['user_classifier'] = UserClassifier()
        self._layers['time_series_forecaster'] = TimeSeriesForecaster()
        logger.info("  - ML引擎: 已启用")

    logger.info("[Layer 3] 智能层init完成")

def init_layer4(self):
    """init能力层"""
    from src.growth_engine import DemandAnalyzer, UserJourneyMapper, FunnelOptimizer

    logger.info("[Layer 4] init能力层...")

    self._layers['demand_analyzer'] = DemandAnalyzer()
    logger.info("  - 需求分析引擎: 已启用")

    self._layers['journey_mapper'] = UserJourneyMapper()
    logger.info("  - 用户旅程mapping器: 已启用")

    self._layers['funnel_optimizer'] = FunnelOptimizer()
    logger.info("  - 漏斗优化器: 已启用")

    logger.info("[Layer 4] 能力层init完成")

def init_layer5(self):
    """init应用层"""
    from src.growth_engine import GrowthStrategyEngine, SolutionTemplateLibrary
    from src.industry_engine import IndustryAdapter

    logger.info("[Layer 5] init应用层...")

    self._layers['growth_engine'] = GrowthStrategyEngine()
    logger.info("  - 增长strategy引擎: 已启用")

    self._layers['industry_adapter'] = IndustryAdapter()
    logger.info("  - 行业适配引擎: 已启用")

    self._layers['solution_library'] = SolutionTemplateLibrary()
    logger.info("  - 解决方案模板库: 已启用 (20种解决方案,含人文品牌叙事)")

    logger.info("[Layer 5] 应用层init完成")

def init_narrative_layer(self):
    """
    init叙事智能层 [v1.0.0 文学智能增强]
    """
    logger.info("[叙事智能层] init叙事智能层...")

    try:
        from src.intelligence.engines.narrative_intelligence_engine import NarrativeIntelligenceEngine
        self._layers['narrative_engine'] = NarrativeIntelligenceEngine()
        logger.info("  - 叙事智能引擎: 已启用")
    except ImportError:
        logger.warning("  - 叙事智能引擎: 模块未找到,跳过")
    except Exception as e:
        logger.warning(f"  - 叙事智能引擎: init失败 - {e}")

    try:
        from src.intelligence.reasoning.deep_reasoning_engine import (
            DeepReasoningEngine, ReasoningMode
        )
        self._layers['reasoning_engine'] = DeepReasoningEngine()
        self._layers['narrative_reasoning_mode'] = ReasoningMode.NARRATIVE_REASONING
        self._layers['consulting_reasoning_mode'] = ReasoningMode.CONSULTING_REASONING
        logger.info("  - 深度推理引擎: 已启用(含咨询推理+叙事推理)")
    except Exception as e:
        self._layers['reasoning_engine'] = None
        logger.warning(f"  - 深度推理引擎: init失败 - {e}")

    try:
        from src.growth_engine.growth_engine import SolutionEngineV2
        self._layers['solution_engine_v2'] = SolutionEngineV2()
        logger.info("  - 解决方案引擎V2: 已启用(含动态效果评估)")
    except Exception as e:
        self._layers['solution_engine_v2'] = None
        logger.warning(f"  - 解决方案引擎V2: init失败 - {e}")

    logger.info("[叙事智能层] 叙事智能层init完成")
