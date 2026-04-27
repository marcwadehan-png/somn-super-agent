"""unified_intelligence_coordinator package v1.0"""

__all__ = [
    'execute_task',
    'get_system_status',
]

from ._unified_base import (
    TaskType, TaskPriority, TaskContext, TaskResult,
    ModuleCapabilityProfile, _MODULE_REGISTRY
)
from ._unified_core import (
    coordinator_init, _lazy_import, _get_module, _ensure_module,
    _preload_modules, _log_system_status, _assess_problem_complexity,
    _update_performance_metrics, _analyze_historical_performance,
    _calculate_recent_success_rate, get_system_status
)
from . import _unified_core as _core_mod
from . import _unified_execute as _exec_mod
from . import _unified_module as _mod_mod

class UnifiedIntelligenceCoordinator:
    def __init__(self, config=None):
        self.config = None
        self.modules = {}
        self.module_profiles = {}
        self.module_mapping = {}
        self.task_history = []
        self.performance_log = []
        self._module_loaded = {}
        self._load_failed = {}
        self.coordination_strategies = {
            "sequential": self._execute_sequential,
            "parallel": self._execute_parallel,
            "ensemble": self._execute_ensemble,
            "adaptive": self._execute_adaptive
        }
        _core_mod.coordinator_init(self, config)

    def _lazy_import(self, import_path, class_name):
        return _core_mod._lazy_import(self, import_path, class_name)

    def _get_module(self, module_key):
        return _core_mod._get_module(self, module_key)

    def _ensure_module(self, module_key):
        return _core_mod._ensure_module(self, module_key)

    def _preload_modules(self, module_keys=None):
        _core_mod._preload_modules(self, module_keys)

    def _log_system_status(self):
        _core_mod._log_system_status(self)

    def _assess_problem_complexity(self, input_data):
        return _core_mod._assess_problem_complexity(self, input_data)

    def _update_performance_metrics(self, task_id, success, execution_time):
        _core_mod._update_performance_metrics(self, task_id, success, execution_time)

    def _analyze_historical_performance(self, task_type):
        return _core_mod._analyze_historical_performance(self, task_type)

    def _calculate_recent_success_rate(self):
        return _core_mod._calculate_recent_success_rate(self)

    def get_system_status(self):
        return _core_mod.get_system_status(self)

    def execute_task(self, task_type, input_data, context=None):
        return _exec_mod.execute_task(self, task_type, input_data, context)

    def _select_coordination_strategy(self, task_type, context):
        return _exec_mod._select_coordination_strategy(self, task_type, context)

    def _execute_sequential(self, task_type, input_data, context):
        return _exec_mod._execute_sequential(self, task_type, input_data, context)

    def _execute_parallel(self, task_type, input_data, context):
        return _exec_mod._execute_parallel(self, task_type, input_data, context)

    def _execute_ensemble(self, task_type, input_data, context):
        return _exec_mod._execute_ensemble(self, task_type, input_data, context)

    def _execute_adaptive(self, task_type, input_data, context):
        return _exec_mod._execute_adaptive(self, task_type, input_data, context)

    def _execute_tier3(self, task_type, input_data, context):
        return _exec_mod._execute_tier3(self, task_type, input_data, context)

    def _select_best_module(self, task_type, context):
        return _exec_mod._select_best_module(self, task_type, context)

    def _select_suitable_modules(self, task_type, context, max_modules=3):
        return _exec_mod._select_suitable_modules(self, task_type, context, max_modules)

    def _execute_module(self, module_name, task_type, input_data, context):
        return _mod_mod._execute_module(self, module_name, task_type, input_data, context)

    def _execute_deep_reasoning(self, module, input_data, context):
        return _mod_mod._execute_deep_reasoning(self, module, input_data, context)

    def _execute_sufu_wisdom(self, module, input_data, context):
        return _mod_mod._execute_sufu_wisdom(self, module, input_data, context)

    def _execute_military_strategy(self, module, input_data, context):
        return _mod_mod._execute_military_strategy(self, module, input_data, context)

    def _execute_growth_engine(self, module, input_data, context):
        return _mod_mod._execute_growth_engine(self, module, input_data, context)

    def _execute_consulting_validator(self, module, input_data, context):
        return _mod_mod._execute_consulting_validator(self, module, input_data, context)

    def _select_reasoning_mode(self, problem, context):
        return _mod_mod._select_reasoning_mode(self, problem, context)

    def _get_wisdom_output(self, module_name, task_type, input_data, context):
        return _mod_mod._get_wisdom_output(self, module_name, task_type, input_data, context)

    def _fuse_parallel_results(self, module_results, task_type):
        return _mod_mod._fuse_parallel_results(self, module_results, task_type)

    def _fuse_wisdom_outputs(self, wisdom_outputs, task_type):
        return _mod_mod._fuse_wisdom_outputs(self, wisdom_outputs, task_type)
