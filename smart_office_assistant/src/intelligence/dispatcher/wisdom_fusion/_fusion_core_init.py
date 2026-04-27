"""wisdom_fusion core init & wisdom_modules v1.0"""
import logging
from typing import Dict, List, Any, Optional

__all__ = [
    'fusion_core_init',
]

logger = logging.getLogger(__name__)

WISDOM_MODULES_AVAILABLE = False
try:
    from ...engines.sufu_wisdom_core import SufuWisdomCore, SufuPrinciple
    from ...engines.military_strategy_engine import MilitaryStrategyEngine
    from ...engines.dao_wisdom_core import DaoWisdomCore
    from ...engines.ru_wisdom_unified import RuWisdomCore
    from ...engines.hongming_wisdom_core import HongmingWisdomCore
    from ...engines.classic_wisdom_core import ClassicWisdomCore
    from ...engines.lvshi_wisdom_engine import LvshiWisdomEngine
    from ...reasoning.deep_reasoning_engine import DeepReasoningEngine
    WISDOM_MODULES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"智慧模块导入失败: {e}")

def fusion_core_init(self):
    from ._fusion_enums import FusionConfig
    self.config = self._config or FusionConfig()
    self.wisdom_modules = {}
    self._initialize_wisdom_modules()
    self.conflict_resolver = None
    self.fusion_history = []
    self.performance_log = []
    self.fusion_cache = {}
    logger.info("智慧fusion核心init完成")
    self._log_system_status()

def _initialize_wisdom_modules(self):
    if not WISDOM_MODULES_AVAILABLE:
        logger.warning("智慧模块不可用,使用简化模式")
        return
    try:
        self.wisdom_modules["sufu_wisdom"] = {
            "module": SufuWisdomCore(),
            "capabilities": ["strategic_decision", "talent_evaluation", "risk_assessment", "ethical_assessment"],
            "domains": ["business", "leadership", "management", "ethics"],
            "weight_adjustment": 1.0
        }
        self.wisdom_modules["military_strategy"] = {
            "module": MilitaryStrategyEngine(),
            "capabilities": ["tactical_execution", "strategic_decision", "risk_management", "competitive_analysis"],
            "domains": ["competition", "marketing", "sales", "strategy"],
            "weight_adjustment": 1.0
        }
        self.wisdom_modules["dao_wisdom"] = {
            "module": DaoWisdomCore(),
            "capabilities": ["strategic_decision", "risk_management", "ethical_assessment", "natural_adaptation"],
            "domains": ["innovation", "sustainability", "long_term_planning", "balance"],
            "weight_adjustment": 1.0
        }
        self.wisdom_modules["ru_wisdom"] = {
            "module": RuWisdomCore(),
            "capabilities": ["ethical_assessment", "social_order", "talent_evaluation", "cultural_adaptation"],
            "domains": ["ethics", "education", "society", "leadership"],
            "weight_adjustment": 1.0
        }
        self.wisdom_modules["hongming_wisdom"] = {
            "module": HongmingWisdomCore(),
            "capabilities": ["cultural_adaptation", "talent_evaluation", "ethical_assessment", "strategic_decision"],
            "domains": ["culture", "international", "diversity", "communication"],
            "weight_adjustment": 1.0
        }
        self.wisdom_modules["classic_wisdom"] = {
            "module": ClassicWisdomCore(),
            "capabilities": ["strategic_decision", "ethical_assessment", "risk_management"],
            "domains": ["general", "traditional", "historical"],
            "weight_adjustment": 1.0
        }
        self.wisdom_modules["lvshi_wisdom"] = {
            "module": LvshiWisdomEngine(),
            "capabilities": ["strategic_decision", "risk_management", "ethical_assessment"],
            "domains": ["governance", "leadership", "policy"],
            "weight_adjustment": 1.0
        }
    except Exception as e:
        logger.error(f"智慧模块init失败: {e}")

def _log_system_status(self):
    logger.info("=" * 60)
    logger.info("智慧fusion核心状态报告")
    logger.info("=" * 60)
    logger.info(f"可用智慧系统: {len(self.wisdom_modules)}")
    logger.info(f"fusion方法: {self.config.method.value}")
    logger.info(f"优先级设置: {self.config.priority.value}")
    logger.info("系统能力:")
    for name, module_info in self.wisdom_modules.items():
        capabilities = module_info.get("capabilities", [])
        logger.info(f"  - {name}: {capabilities}")
    logger.info("=" * 60)

def _calculate_domain_relevance(self, module_name: str, domain: str) -> float:
    domain_mapping = {
        "sufu_wisdom": {"business": 0.9, "leadership": 0.8, "management": 0.8, "ethics": 0.7},
        "military_strategy": {"competition": 0.9, "marketing": 0.8, "sales": 0.7, "strategy": 0.9, "war_economy": 0.75},
        "dao_wisdom": {"innovation": 0.8, "sustainability": 0.9, "long_term_planning": 0.7, "balance": 0.9},
        "ru_wisdom": {"ethics": 0.9, "education": 0.8, "society": 0.7, "leadership": 0.7, "civilization": 0.72},
        "hongming_wisdom": {"culture": 0.9, "international": 0.8, "diversity": 0.9, "communication": 0.8, "civilization": 0.78},
        "civilization_wisdom": {"civilization": 0.96, "culture": 0.88, "history": 0.86, "governance": 0.76, "long_term_planning": 0.84},
        "civilization_war_economy": {"war_economy": 0.96, "strategy": 0.88, "competition": 0.82, "institution": 0.9, "governance": 0.8}
    }
    module_mapping = domain_mapping.get(module_name, {})
    return module_mapping.get(domain, 0.5)

def _get_module_performance(self, module_name: str, task_type: str) -> float:
    return 0.7

def _estimate_problem_complexity(self, context: Dict[str, Any]) -> float:
    problem_text = str(context.get("problem", ""))
    length_factor = min(1.0, len(problem_text) / 500)
    complex_keywords = ["战略", "规划", "系统", "复杂", "多维", "长期"]
    complex_count = sum(1 for kw in complex_keywords if kw in problem_text)
    keyword_factor = min(1.0, complex_count / 3)
    complexity = (length_factor * 0.6 + keyword_factor * 0.4)
    return min(0.95, max(0.2, complexity))
