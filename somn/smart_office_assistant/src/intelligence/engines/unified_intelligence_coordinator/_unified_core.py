"""unified_intelligence_coordinator core init & lazy loading v1.0"""
import logging
from typing import Dict, List, Any, Optional
from ._unified_base import _MODULE_REGISTRY, _LAZY_IMPORT_CACHE, TaskContext, TaskPriority

__all__ = [
    'coordinator_init',
    'get_system_status',
]

logger = logging.getLogger(__name__)

_MODULE_MAPPING_TEMPLATE = {
    "deep_reasoning": {"module": None, "capabilities": ["problem_solving", "strategic_decision"], "domains": ["general", "technical", "business"]},
    "sufu_wisdom": {"module": None, "capabilities": ["strategic_decision", "risk_assessment", "talent_evaluation"], "domains": ["business", "leadership", "ethics"]},
    "military_strategy": {"module": None, "capabilities": ["tactical_execution", "strategic_decision"], "domains": ["competition", "marketing", "strategy"]},
    "hongming_wisdom": {"module": None, "capabilities": ["talent_evaluation", "strategic_decision"], "domains": ["culture", "leadership", "ethics"]},
    "growth_engine": {"module": None, "capabilities": ["growth_planning", "consulting_validation"], "domains": ["business", "marketing", "sales"]},
    "consulting_validator": {"module": None, "capabilities": ["consulting_validation", "risk_assessment"], "domains": ["consulting", "business", "strategy"]},
    "memory_encoding": {"module": None, "capabilities": ["learning_optimization"], "domains": ["general"]},
    "learning_system": {"module": None, "capabilities": ["learning_optimization"], "domains": ["general"]},
    "ancient_wisdom_fusion": {"module": None, "capabilities": ["strategic_decision", "problem_solving", "consulting_validation"], "domains": ["ethics", "governance", "talent", "strategy", "crisis", "culture", "growth", "harmony"]},
    "cross_wisdom_analyzer": {"module": None, "capabilities": ["problem_solving", "strategic_decision"], "domains": ["general", "ethics", "culture"]},
    "wisdom_memory_enhancer": {"module": None, "capabilities": ["learning_optimization", "consulting_validation"], "domains": ["ethics", "governance", "culture", "strategy"]},
    "wisdom_growth_engine": {"module": None, "capabilities": ["growth_planning", "strategic_decision"], "domains": ["business", "marketing", "sales", "competition"]},
    "metaphysics_wisdom": {"module": None, "capabilities": ["strategic_decision", "risk_assessment", "problem_solving"], "domains": ["general", "strategy", "culture", "environment", "timing", "risk"]},
    "civilization_wisdom": {"module": None, "capabilities": ["strategic_decision", "risk_assessment", "problem_solving"], "domains": ["civilization", "history", "culture", "strategy", "governance"]},
    "civilization_war_economy": {"module": None, "capabilities": ["strategic_decision", "risk_assessment", "consulting_validation"], "domains": ["war", "economy", "civilization", "competition", "strategy"]},
    "mythology_wisdom": {"module": None, "capabilities": ["strategic_decision", "problem_solving", "risk_assessment"], "domains": ["culture", "narrative", "strategy", "philosophy", "creation"]},
    "literary_narrative": {"module": None, "capabilities": ["problem_solving", "consulting_validation"], "domains": ["culture", "narrative", "literature", "growth"]},
    "anthropology_wisdom": {"module": None, "capabilities": ["strategic_decision", "risk_assessment", "problem_solving"], "domains": ["culture", "cross_culture", "ritual", "social"]},
    "behavior_shaping": {"module": None, "capabilities": ["growth_planning", "problem_solving"], "domains": ["behavior", "habit", "self_management", "growth"]},
    "science_thinking": {"module": None, "capabilities": ["problem_solving", "strategic_decision", "consulting_validation"], "domains": ["science", "analysis", "evidence", "system"]},
    "social_science": {"module": None, "capabilities": ["growth_planning", "strategic_decision", "risk_assessment", "consulting_validation"], "domains": ["marketing", "economics", "social", "growth", "business"]},
    "yangming_xinxue": {"module": None, "capabilities": ["strategic_decision", "problem_solving", "consulting_validation"], "domains": ["inner_growth", "ethics", "governance", "wisdom", "self_cultivation"]},
    "dewey_thinking": {"module": None, "capabilities": ["problem_solving", "learning_optimization"], "domains": ["thinking", "learning", "reflection", "practice", "innovation"]},
    "top_thinking": {"module": None, "capabilities": ["strategic_decision", "problem_solving", "creative_innovation"], "domains": ["strategy", "complex", "innovation", "cross_domain"]},
    "supreme_wisdom_coordinator": {"module": None, "capabilities": ["strategic_decision", "problem_solving", "risk_assessment", "consulting_validation"], "domains": ["general", "complex", "multi_domain"]},
    "natural_science": {"module": None, "capabilities": ["problem_solving", "strategic_decision", "risk_assessment", "consulting_validation"], "domains": ["science", "physics", "chemistry", "biology", "earth", "cosmos", "complex_system", "cross_scale", "evolution", "neuroscience"]},
    "sanjiao_fusion": {"module": None, "capabilities": ["strategic_decision", "problem_solving", "consulting_validation"], "domains": ["ethics", "governance", "wisdom", "harmony", "culture"]},
    "psychology_pioneer_fusion": {"module": None, "capabilities": ["problem_solving", "strategic_decision", "consulting_validation"], "domains": ["psychology", "marketing", "user_insight", "behavior"]},
    "dao_wisdom": {"module": None, "capabilities": ["strategic_decision", "problem_solving", "risk_assessment"], "domains": ["nature", "harmony", "wisdom", "health", "philosophy"]},
    "tang_song_poetry_fusion": {"module": None, "capabilities": ["problem_solving", "strategic_decision"], "domains": ["culture", "wisdom", "aesthetics", "emotion"]},
    "buddha_wisdom": {"module": None, "capabilities": ["problem_solving", "consulting_validation"], "domains": ["spirituality", "wisdom", "compassion", "inner_peace"]},
    # ── 新增推理引擎 v1.0.0 (2026-04-24) ──────────────────────────────────────
    "long_cot_reasoning": {"module": None, "capabilities": ["problem_solving", "strategic_decision", "tier3_analysis"], "domains": ["general", "complex", "multi_step", "deep_analysis"]},
    "tot_reasoning": {"module": None, "capabilities": ["problem_solving", "strategic_decision", "tier3_analysis"], "domains": ["general", "strategy", "planning", "multi_option", "comparison"]},
    "react_reasoning": {"module": None, "capabilities": ["problem_solving", "tier3_analysis"], "domains": ["general", "knowledge", "fact_check", "calculation", "search"]},
}

def coordinator_init(self, config=None):
    from ._unified_base import TaskResult, ModuleCapabilityProfile
    self.config = config or {}
    self.modules = {}
    self.module_profiles = {}
    self.module_mapping = {k: v.copy() for k, v in _MODULE_MAPPING_TEMPLATE.items()}
    self.task_history = []
    self.performance_log = []
    self._module_loaded = {}
    self._load_failed = {}
    logger.info("unified智能协调器init完成(懒加载模式)")
    self._log_system_status()

def _lazy_import(self, import_path: str, class_name: str):
    from importlib import import_module
    cache_key = f"{import_path}:{class_name}"
    if cache_key in _LAZY_IMPORT_CACHE:
        return _LAZY_IMPORT_CACHE[cache_key]
    try:
        pkg_name = import_path.lstrip(".")
        if import_path.startswith(".."):
            mod = import_module(pkg_name, package="src.neural_memory")
        elif import_path.startswith("."):
            mod = import_module(pkg_name, package="src.intelligence")
        else:
            mod = import_module(import_path)
        cls = getattr(mod, class_name)
        _LAZY_IMPORT_CACHE[cache_key] = cls
        return cls
    except (ImportError, AttributeError) as e:
        logger.warning(f"延迟导入失败 {import_path}.{class_name}: {e}")
        return None

def _get_module(self, module_key: str):
    from ._unified_base import _MODULE_REGISTRY
    from ._unified_base import ModuleCapabilityProfile
    if module_key in self.modules:
        return self.modules.get(module_key)
    for reg_key, import_path, class_name, mapping_key in _MODULE_REGISTRY:
        if reg_key == module_key:
            if module_key in self._load_failed:
                return None
            factory = _lazy_import(self, import_path, class_name)
            if factory is None:
                self._load_failed[module_key] = True
                return None
            try:
                instance = factory()
                self.modules[module_key] = instance
                if mapping_key and mapping_key in self.module_mapping:
                    self.module_mapping[mapping_key]["module"] = instance
                self._module_loaded[module_key] = True
                if module_key not in self.module_profiles:
                    self.module_profiles[module_key] = ModuleCapabilityProfile(module_key)
                logger.debug(f"懒加载模块成功: {module_key}")
                return instance
            except Exception as e:
                self._load_failed[module_key] = "模块加载失败"
                logger.warning(f"懒加载模块失败 {module_key}: {e}")
                return None
    return None

def _ensure_module(self, module_key: str) -> bool:
    if module_key in self.modules:
        return True
    return _get_module(self, module_key) is not None

def _preload_modules(self, module_keys: List[str] = None):
    from ._unified_base import _MODULE_REGISTRY
    if module_keys is None:
        module_keys = [reg[0] for reg in _MODULE_REGISTRY]
    for key in module_keys:
        _get_module(self, key)

def _log_system_status(self):
    from ._unified_base import _MODULE_REGISTRY
    logger.info("=" * 60)
    logger.info("unified智能协调器状态报告(懒加载模式)")
    logger.info("=" * 60)
    logger.info(f"已注册模块数量: {len(_MODULE_REGISTRY)}")
    logger.info(f"已懒加载模块: {list(self.modules.keys())}")
    logger.info(f"协调strategy: {list(self.coordination_strategies.keys())}")
    logger.info("=" * 60)

def _assess_problem_complexity(self, input_data: Dict[str, Any]) -> float:
    """评估问题复杂度，返回0.0-1.0，并识别推理引擎类型"""
    complexity_factors = []
    reasoning_hints = {"engine_type": "default", "confidence": 0.5}
    
    if isinstance(input_data, dict):
        data_size = len(str(input_data))
        complexity_factors.append(min(1.0, data_size / 10000))
    
    if "problem" in input_data:
        problem_text = input_data["problem"]
        # 复杂度关键词
        complex_keywords = ["战略", "规划", "系统", "长期", "复杂", "多维度", "深入", "论证"]
        simple_keywords = ["简单", "基础", "日常", "常规"]
        complex_count = sum(1 for kw in complex_keywords if kw in problem_text)
        simple_count = sum(1 for kw in simple_keywords if kw in problem_text)
        keyword_factor = min(1.0, max(0.0, (complex_count - simple_count * 0.5) / 3))
        complexity_factors.append(keyword_factor)
        
        # 推理引擎类型识别 v1.0.0 (2026-04-24)
        # Long CoT: 多步骤、深层分析
        if any(kw in problem_text for kw in ["分析", "推理", "论证", "深入", "多步", "详细"]):
            reasoning_hints = {"engine_type": "long_cot_reasoning", "confidence": 0.8}
        # ToT: 多方案比较、选择、权衡
        if any(kw in problem_text for kw in ["方案", "选择", "比较", "权衡", "策略", "规划", "路径"]):
            reasoning_hints = {"engine_type": "tot_reasoning", "confidence": 0.85}
        # ReAct: 需要外部知识、查询、验证
        if any(kw in problem_text for kw in ["查询", "搜索", "查", "验证", "计算", "获取"]):
            reasoning_hints = {"engine_type": "react_reasoning", "confidence": 0.9}
    
    if complexity_factors:
        base_score = sum(complexity_factors) / len(complexity_factors)
        return base_score
    return 0.5

def _update_performance_metrics(self, task_id: str, success: bool, execution_time: float):
    self.performance_log.append({
        "task_id": task_id, "success": success, "execution_time": execution_time,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })
    if len(self.performance_log) > 1000:
        self.performance_log = self.performance_log[-500:]

def _analyze_historical_performance(self, task_type) -> Dict[str, Dict[str, float]]:
    return {
        "sequential": {"success_rate": 0.85, "avg_time": 3.2},
        "parallel": {"success_rate": 0.78, "avg_time": 5.1},
        "ensemble": {"success_rate": 0.92, "avg_time": 8.7},
        "adaptive": {"success_rate": 0.88, "avg_time": 4.5}
    }

def _calculate_recent_success_rate(self) -> float:
    if not self.task_history:
        return 0.0
    recent_tasks = self.task_history[-50:]
    success_count = sum(1 for task in recent_tasks if task.get("success", False))
    return success_count / len(recent_tasks) if recent_tasks else 0.0

def get_system_status(self) -> Dict[str, Any]:
    return {
        "total_modules": len(self.modules),
        "available_modules": list(self.modules.keys()),
        "total_tasks": len(self.task_history),
        "recent_success_rate": _calculate_recent_success_rate(self),
        "module_profiles": {
            name: {"capabilities": profile.capabilities, "reliability": profile.reliability_score}
            for name, profile in self.module_profiles.items()
        }
    }
