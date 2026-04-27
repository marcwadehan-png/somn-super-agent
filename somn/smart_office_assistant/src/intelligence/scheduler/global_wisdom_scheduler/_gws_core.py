"""global_wisdom_scheduler core: init & engine registration v1.0"""
import logging
from typing import Dict, List, Any, Optional
from ._gws_base import SchedulerConfig, WisdomEngineRegistry

__all__ = [
    'get_neuron_wisdom_network',
    'scheduler_init',
]

logger = logging.getLogger(__name__)

def _save_scheduler_config_cache(config: SchedulerConfig):
    """[v1.0 配置缓存] 保存调度器配置到缓存文件"""
    import json
    from pathlib import Path
    try:
        cache_path = Path("data/cache/global_wisdom_scheduler_config.json")
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, ensure_ascii=False, indent=2)
        logger.debug(f"[配置缓存] 已保存调度器配置到: {cache_path}")
    except Exception as e:
        logger.warning(f"[配置缓存] 保存失败: {e}")

def _load_scheduler_config_cache() -> Optional[SchedulerConfig]:
    """[v1.0 配置缓存] 从缓存文件加载调度器配置"""
    import json
    from pathlib import Path
    from ._gws_base import SchedulerConfig
    try:
        cache_path = Path("data/cache/global_wisdom_scheduler_config.json")
        if not cache_path.exists():
            return None
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        config = SchedulerConfig.from_dict(data)
        logger.info(f"[配置缓存] 已加载调度器配置（模式: {config.mode.value}）")
        return config
    except Exception as e:
        logger.warning(f"[配置缓存] 加载失败: {e}")
        return None

def scheduler_init(self, config: Optional[SchedulerConfig] = None):
    from ._gws_base import ScheduledResult, WisdomQuery
    # [v1.0 配置缓存] 优先从缓存加载配置，未命中则使用传入配置或默认配置
    if config is None:
        cached_config = _load_scheduler_config_cache()
        if cached_config:
            self.config = cached_config
        else:
            self.config = SchedulerConfig()
    else:
        self.config = config
    self.network = get_neuron_wisdom_network()
    self.registry = WisdomEngineRegistry()
    self.total_queries = 0
    self.query_history: List[Dict] = []
    self._initialize_engines()
    # [v1.0 配置缓存] 初始化完成后保存配置到缓存
    _save_scheduler_config_cache(self.config)

def _initialize_engines(self):
    def _try_register(school_id, module_path, class_name):
        try:
            from importlib import import_module
            mod = import_module(module_path)
            cls = getattr(mod, class_name)
            self.registry.register_engine(school_id, cls())
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"注册 {school_id} 失败: {e}")

    _try_register("SUFU", "src.intelligence.engines.sufu_wisdom_core", "SufuWisdomCore")
    _try_register("DAOIST", "src.intelligence.engines.dao_wisdom.dao_wisdom_core", "DaoWisdomCore")
    _try_register("CONFUCIAN", "src.intelligence.engines.ru_wisdom_unified", "RuWisdomCore")
    _try_register("BUDDHIST", "src.intelligence.engines.buddha_wisdom_core", "BuddhaWisdomCore")
    _try_register("MILITARY", "src.intelligence.engines.military_strategy_engine", "MilitaryStrategyEngine")
    _try_register("LVSHI", "src.intelligence.engines.lvshi_wisdom_engine", "LvShiWisdomCore")
    _try_register("HONGMING", "src.intelligence.engines.hongming_wisdom_core", "HongmingWisdomCore")
    _try_register("CIVILIZATION", "src.intelligence.engines.civilization_wisdom_core", "CivilizationWisdomCore")
    _try_register("CIV_WAR_ECONOMY", "src.intelligence.engines.civilization_war_economy_core", "CivilizationWarEconomyCore")
    _try_register("METAPHYSICS", "src.intelligence.engines.metaphysics_wisdom_unified", "MetaphysicsWisdomUnified")
    _try_register("GROWTH", "src.intelligence.engines.growth_mindset_evaluator", "GrowthMindsetEvaluator")
    _try_register("SCI_FI", "src.intelligence.engines.thinking_growth_unified", "ThinkingGrowthUnified")
    _try_register("SCIENCE", "src.intelligence.engines.science_thinking_engine", "ScienceThinkingEngine")
    _try_register("NATURAL_SCIENCE", "src.intelligence.engines.natural_science_unified", "NaturalScienceUnified")
    _try_register("MYTHOLOGY", "src.intelligence.engines.mythology_wisdom_engine", "MythologyWisdomEngine")
    _try_register("LITERARY", "src.intelligence.engines.literary_narrative_engine", "LiteraryNarrativeEngine")
    _try_register("ANTHROPOLOGY", "src.intelligence.engines.anthropology_wisdom_engine", "AnthropologyWisdomEngine")
    _try_register("BEHAVIOR", "src.intelligence.engines.behavior_shaping_engine", "BehaviorShapingEngine")
    _try_register("CHINESE_CONSUMER", "src.intelligence.engines.chinese_consumer_culture_engine", "ChineseConsumerCultureEngine")
    _try_register("YANGMING", "src.intelligence.engines.philosophy.yangming_xinxue_engine", "YangmingXinxueEngine")
    _try_register("DEWEY", "src.intelligence.engines.dewey_thinking_engine", "DeweyThinkingEngine")
    _try_register("TOP_METHODS", "src.intelligence.engines.top_thinking_engine", "TopThinkingEngine")
    _try_register("SOCIAL_SCIENCE", "src.intelligence.engines.social_science_engine", "SocialScienceWisdomEngine")
    _try_register("WCC", "src.intelligence.engines.wcc_evolutionary_core", "WCCEvolutionaryCore")
    logger.info("智慧引擎注册完成")

# Lazy-load neuron network
_neuron_network_instance = None

def get_neuron_wisdom_network():
    global _neuron_network_instance
    if _neuron_network_instance is None:
        try:
            from src.intelligence.engines.neuron_wisdom_network import get_neuron_wisdom_network as _gnn
            _neuron_network_instance = _gnn()
        except ImportError:
            from src.intelligence.engines.neuron_wisdom_network import NeuronWisdomNetwork
            _neuron_network_instance = NeuronWisdomNetwork()
    return _neuron_network_instance
