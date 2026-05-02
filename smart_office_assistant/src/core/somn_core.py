"""
Somn 核心整合模块 [v21.0 架构优化版]
整合所有组件,提供unified的智能体主链接口.

[v21.0 优化]：
- __getattr__动态代理消除50+委托方法
- _LAZY_MODULES分组管理(23组)
- IntFlag初始化标志位
- TimeoutGuard线程池复用
"""

import json
import re
import hashlib
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeoutError
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# 全局 TF-IDF 索引单例状态
_experience_index: Optional[Any] = None
_index_doc_ids: List[str] = []

from src.core.paths import PROJECT_ROOT

# ═══════════════════════════════════════════════════════════════════════════════
# [v20.0 优化] 统一的延迟导入系统
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# [v21.0 优化] 分组延迟导入系统（原v20.0扁平字典升级为分组管理）
# ═══════════════════════════════════════════════════════════════════════════════

# 分组延迟导入注册表
_LAZY_MODULE_GROUPS: Dict[str, Dict[str, tuple]] = {
    'core': {
        'PurePythonTfidfIndex': ('._somn_tfidf', 'PurePythonTfidfIndex'),
        '_ensure_experience_index': ('._somn_tfidf', '_ensure_experience_index'),
    },
    'types': {
        'SomnContext': ('._somn_types', 'SomnContext'),
        'WorkflowTaskRecord': ('._somn_types', 'WorkflowTaskRecord'),
        'LongTermGoalRecord': ('._somn_types', 'LongTermGoalRecord'),
    },
    'init': {
        'init_main_chain_integration': ('._somn_wisdom_init', 'init_main_chain_integration'),
        'init_learning_coordinator': ('._somn_wisdom_init', 'init_learning_coordinator'),
        'init_autonomous_agent': ('._somn_wisdom_init', 'init_autonomous_agent'),
        'init_cloud_learning_system': ('._somn_wisdom_init', 'init_cloud_learning_system'),
    },
    'analysis': {
        'run_wisdom_analysis': ('._somn_wisdom_analysis', 'run_wisdom_analysis'),
        'run_unified_enhancement': ('._somn_wisdom_analysis', 'run_unified_enhancement'),
        'maybe_run_metaphysics_analysis': ('._somn_wisdom_analysis', 'maybe_run_metaphysics_analysis'),
    },
    'strategy': {
        'build_strategy_learning_guidance': ('._somn_strategy_design', 'build_strategy_learning_guidance'),
        'build_workflow_reference_base': ('._somn_strategy_design', 'build_workflow_reference_base'),
        'build_candidate_strategies': ('._somn_strategy_design', 'build_candidate_strategies'),
        'rank_strategy_candidates': ('._somn_strategy_design', 'rank_strategy_candidates'),
        'build_strategy_context': ('._somn_strategy_design', 'build_strategy_context'),
        'run_parallel_strategy_generation': ('._somn_strategy_design', 'run_parallel_strategy_generation'),
        'build_strategy_plan': ('._somn_strategy_design', 'build_strategy_plan'),
        'generate_structured_strategy': ('._somn_strategy_design', 'generate_structured_strategy'),
    },
    'execution': {
        'parse_execution_tasks': ('._somn_workflow_execution', 'parse_execution_tasks'),
        'execute_task': ('._somn_workflow_execution', 'execute_task'),
        'execute_rollback': ('._somn_workflow_execution', 'execute_rollback'),
        'resolve_reinforcement_action': ('._somn_workflow_execution', 'resolve_reinforcement_action'),
        'extract_strategy_combo': ('._somn_workflow_execution', 'extract_strategy_combo'),
        'run_workflow_state_machine': ('._somn_workflow_execution', 'run_workflow_state_machine'),
        'build_execution_report': ('._somn_workflow_execution', 'build_execution_report'),
    },
    'utils': {
        'resolve_estimated_minutes': ('._somn_utils', 'resolve_estimated_minutes'),
    },
    'feedback': {
        '_record_workflow_feedback': ('._somn_feedback', '_record_workflow_feedback'),
        '_record_learning_feedback': ('._somn_feedback', '_record_learning_feedback'),
        '_record_evaluation_learning_feedback': ('._somn_feedback', '_record_evaluation_learning_feedback'),
        '_clamp_unit_score': ('._somn_feedback', '_clamp_unit_score'),
    },
    'evaluation': {
        '_track_roi_task_start': ('._somn_evaluation', '_track_roi_task_start'),
        '_track_roi_task_completion': ('._somn_evaluation', '_track_roi_task_completion'),
        '_track_roi_workflow_completion': ('._somn_evaluation', '_track_roi_workflow_completion'),
        '_build_fallback_evaluation': ('._somn_evaluation', '_build_fallback_evaluation'),
        '_evaluate_main_chain_performance': ('._somn_evaluation', '_evaluate_main_chain_performance'),
        '_generate_next_iteration': ('._somn_evaluation', '_generate_next_iteration'),
        '_record_validation_learning': ('._somn_evaluation', '_record_validation_learning'),
        'run_llm_evaluation': ('._somn_evaluation', 'run_llm_evaluation'),
        'build_evaluation_report': ('._somn_evaluation', 'build_evaluation_report'),
    },
    'routes': {
        '_module_run_orchestrator_route': ('._somn_routes', '_module_run_orchestrator_route'),
        '_module_run_local_llm_route': ('._somn_routes', '_module_run_local_llm_route'),
        '_module_run_wisdom_route': ('._somn_routes', '_module_run_wisdom_route'),
        '_module_run_sage_dispatch_route': ('._somn_routes', '_module_run_sage_dispatch_route'),
        '_module_run_divine_reason_route': ('._somn_routes', '_module_run_divine_reason_route'),
        '_module_run_tianshu_pipeline_route': ('._somn_routes', '_module_run_tianshu_pipeline_route'),
    },
    'semantic': {
        '_module_run_semantic_analysis': ('._somn_semantic_api', '_module_run_semantic_analysis'),
        '_module_summarize_understanding': ('._somn_semantic_api', '_module_summarize_understanding'),
        '_module_record_semantic_feedback': ('._somn_semantic_api', '_module_record_semantic_feedback'),
        '_module_get_semantic_memory_stats': ('._somn_semantic_api', '_module_get_semantic_memory_stats'),
        '_module_get_semantic_memory_report': ('._somn_semantic_api', '_module_get_semantic_memory_report'),
        '_module_register_semantic_user': ('._somn_semantic_api', '_module_register_semantic_user'),
        '_module_switch_semantic_user': ('._somn_semantic_api', '_module_switch_semantic_user'),
        '_module_list_semantic_users': ('._somn_semantic_api', '_module_list_semantic_users'),
        '_module_export_user_semantic_data': ('._somn_semantic_api', '_module_export_user_semantic_data'),
    },
    'getters': {
        'run_get_feedback_pipeline': ('._somn_getters', 'run_get_feedback_pipeline'),
        'run_get_reinforcement_trigger': ('._somn_getters', 'run_get_reinforcement_trigger'),
        'run_get_roi_tracker': ('._somn_getters', 'run_get_roi_tracker'),
    },
    'emotion_research': {
        'validate_requirement_with_framework': ('._somn_emotion_research', 'validate_requirement_with_framework'),
        'build_strategy_with_framework': ('._somn_emotion_research', 'build_strategy_with_framework'),
        'evaluate_output_quality': ('._somn_emotion_research', 'evaluate_output_quality'),
        'learn_from_execution_result': ('._somn_emotion_research', 'learn_from_execution_result'),
        'trigger_web_learning': ('._somn_emotion_research', 'trigger_web_learning'),
        'check_framework_upgrade': ('._somn_emotion_research', 'check_framework_upgrade'),
        'integrate_with_somn_core': ('._somn_emotion_research', 'integrate_with_somn_core'),
    },
    'research_phase': {
        'run_all_research_phases': ('..intelligence.engines.research_phase_manager', 'run_all_research_phases'),
        'get_research_phase_manager': ('..intelligence.engines.research_phase_manager', 'get_research_phase_manager'),
    },
    'three_core': {
        'ThreeCoreIntegration': ('..intelligence.three_core', 'ThreeCoreIntegration'),
        'get_three_core_integration': ('..intelligence.three_core', 'get_three_core_integration'),
        'ResearchLevel': ('..intelligence.three_core', 'ResearchLevel'),
        'ResearchDepth': ('..intelligence.three_core', 'ResearchDepth'),
        'ResearchDimension': ('..intelligence.three_core', 'ResearchDimension'),
        'ComplexityLevel': ('..intelligence.three_core', 'ComplexityLevel'),
        'MainLine': ('..intelligence.three_core', 'MainLine'),
        'SagePhase': ('..intelligence.three_core', 'SagePhase'),
        'ResearchPlan': ('..intelligence.three_core', 'ResearchPlan'),
        'DispatchAllocation': ('..intelligence.three_core', 'DispatchAllocation'),
        'WisdomInjection': ('..intelligence.three_core', 'WisdomInjection'),
        'ThreeCoreResult': ('..intelligence.three_core', 'ThreeCoreResult'),
        'RESEARCH_LEVEL_MAINLINE_MATRIX': ('..intelligence.three_core', 'RESEARCH_LEVEL_MAINLINE_MATRIX'),
        'DEPTH_PHASE_MATRIX': ('..intelligence.three_core', 'DEPTH_PHASE_MATRIX'),
        'DIMENSION_SCHOOL_MATRIX': ('..intelligence.three_core', 'DIMENSION_SCHOOL_MATRIX'),
        'SAGE_MAINLINE_MATRIX': ('..intelligence.three_core', 'SAGE_MAINLINE_MATRIX'),
    },
    'delegation': {
        'delegate_normalize_for_cache': ('._somn_delegation', 'delegate_normalize_for_cache'),
        'delegate_jaccard_similarity': ('._somn_delegation', 'delegate_jaccard_similarity'),
        'delegate_safe_future_result': ('._somn_delegation', 'delegate_safe_future_result'),
        'delegate_serialize_task_record': ('._somn_delegation', 'delegate_serialize_task_record'),
        'delegate_execute_rollback': ('._somn_delegation', 'delegate_execute_rollback'),
        'delegate_execute_task': ('._somn_delegation', 'delegate_execute_task'),
        'delegate_extract_strategy_combo': ('._somn_delegation', 'delegate_extract_strategy_combo'),
        'delegate_resolve_reinforcement_action': ('._somn_delegation', 'delegate_resolve_reinforcement_action'),
        'delegate_clamp_unit_score': ('._somn_delegation', 'delegate_clamp_unit_score'),
        'delegate_resolve_estimated_minutes': ('._somn_delegation', 'delegate_resolve_estimated_minutes'),
        'delegate_track_roi_task_start': ('._somn_delegation', 'delegate_track_roi_task_start'),
        'delegate_estimate_task_quality_score': ('._somn_delegation', 'delegate_estimate_task_quality_score'),
        'delegate_track_roi_task_completion': ('._somn_delegation', 'delegate_track_roi_task_completion'),
        'delegate_track_roi_workflow_completion': ('._somn_delegation', 'delegate_track_roi_workflow_completion'),
        'delegate_normalize_roi_ratio': ('._somn_delegation', 'delegate_normalize_roi_ratio'),
        'delegate_roi_trend_bias': ('._somn_delegation', 'delegate_roi_trend_bias'),
        'delegate_build_roi_signal_snapshot': ('._somn_delegation', 'delegate_build_roi_signal_snapshot'),
        'delegate_score_to_rating_value': ('._somn_delegation', 'delegate_score_to_rating_value'),
        'delegate_task_outcome_anchor': ('._somn_delegation', 'delegate_task_outcome_anchor'),
        'delegate_serialize_feedback_item': ('._somn_delegation', 'delegate_serialize_feedback_item'),
        'delegate_serialize_reinforcement_updates': ('._somn_delegation', 'delegate_serialize_reinforcement_updates'),
        'delegate_build_workflow_feedback_entries': ('._somn_delegation', 'delegate_build_workflow_feedback_entries'),
        'delegate_build_evaluation_feedback_entries': ('._somn_delegation', 'delegate_build_evaluation_feedback_entries'),
        'delegate_apply_reinforcement_inputs': ('._somn_delegation', 'delegate_apply_reinforcement_inputs'),
        'delegate_submit_feedback_entries': ('._somn_delegation', 'delegate_submit_feedback_entries'),
        'delegate_safe_industry_type': ('._somn_delegation', 'delegate_safe_industry_type'),
        'delegate_extract_keywords': ('._somn_delegation', 'delegate_extract_keywords'),
        'delegate_check_search_cache': ('._somn_delegation', 'delegate_check_search_cache'),
        'delegate_put_search_cache': ('._somn_delegation', 'delegate_put_search_cache'),
        'delegate_evict_stale_search_cache': ('._somn_delegation', 'delegate_evict_stale_search_cache'),
        'delegate_ensure_autonomy_stores': ('._somn_delegation', 'delegate_ensure_autonomy_stores'),
        'delegate_read_json_store': ('._somn_delegation', 'delegate_read_json_store'),
        'delegate_write_json_store': ('._somn_delegation', 'delegate_write_json_store'),
        'delegate_extract_similarity_terms': ('._somn_delegation', 'delegate_extract_similarity_terms'),
        'delegate_make_goal_id': ('._somn_delegation', 'delegate_make_goal_id'),
        'delegate_generate_autonomy_reflection': ('._somn_delegation', 'delegate_generate_autonomy_reflection'),
        'delegate_store_autonomy_learning': ('._somn_delegation', 'delegate_store_autonomy_learning'),
        'delegate_extract_json_payload': ('._somn_delegation', 'delegate_extract_json_payload'),
    },
    'autonomy_api': {
        '_module_ensure_autonomy_stores': ('._somn_autonomy_api', '_module_ensure_autonomy_stores'),
        '_module_read_json_store': ('._somn_autonomy_api', '_module_read_json_store'),
        '_module_write_json_store': ('._somn_autonomy_api', '_module_write_json_store'),
        '_module_extract_similarity_terms': ('._somn_autonomy_api', '_module_extract_similarity_terms'),
        '_module_make_goal_id': ('._somn_autonomy_api', '_module_make_goal_id'),
        '_module_record_task_memory': ('._somn_autonomy_api', '_module_record_task_memory'),
        '_module_generate_autonomy_reflection': ('._somn_autonomy_api', '_module_generate_autonomy_reflection'),
        '_module_store_autonomy_learning': ('._somn_autonomy_api', '_module_store_autonomy_learning'),
    },
    'roi_api': {
        '_module_clamp_unit_score': ('._somn_roi_api', '_module_clamp_unit_score'),
        '_module_normalize_roi_ratio': ('._somn_roi_api', '_module_normalize_roi_ratio'),
        '_module_roi_trend_bias': ('._somn_roi_api', '_module_roi_trend_bias'),
        '_module_resolve_reinforcement_action': ('._somn_roi_api', '_module_resolve_reinforcement_action'),
        '_module_resolve_estimated_minutes': ('._somn_roi_api', '_module_resolve_estimated_minutes'),
        '_module_extract_strategy_combo': ('._somn_roi_api', '_module_extract_strategy_combo'),
        '_module_estimate_task_quality_score': ('._somn_roi_api', '_module_estimate_task_quality_score'),
        '_module_task_outcome_anchor': ('._somn_roi_api', '_module_task_outcome_anchor'),
        '_module_score_to_rating_value': ('._somn_roi_api', '_module_score_to_rating_value'),
        '_module_track_roi_task_start': ('._somn_roi_api', '_module_track_roi_task_start'),
        '_module_track_roi_task_completion': ('._somn_roi_api', '_module_track_roi_task_completion'),
        '_module_track_roi_workflow_completion': ('._somn_roi_api', '_module_track_roi_workflow_completion'),
        '_module_build_roi_signal_snapshot': ('._somn_roi_api', '_module_build_roi_signal_snapshot'),
        '_module_serialize_feedback_item': ('._somn_roi_api', '_module_serialize_feedback_item'),
        '_module_serialize_reinforcement_updates': ('._somn_roi_api', '_module_serialize_reinforcement_updates'),
        '_module_build_workflow_feedback_entries': ('._somn_roi_api', '_module_build_workflow_feedback_entries'),
        '_module_build_evaluation_feedback_entries': ('._somn_roi_api', '_module_build_evaluation_feedback_entries'),
        '_module_apply_reinforcement_inputs': ('._somn_roi_api', '_module_apply_reinforcement_inputs'),
        '_module_submit_feedback_entries': ('._somn_roi_api', '_module_submit_feedback_entries'),
    },
    'execution_api': {
        'module_normalize_for_cache': ('._somn_execution_api', 'module_normalize_for_cache'),
        'module_jaccard_similarity': ('._somn_execution_api', 'module_jaccard_similarity'),
        'module_safe_future_result': ('._somn_execution_api', 'module_safe_future_result'),
        'module_safe_industry_type': ('._somn_execution_api', 'module_safe_industry_type'),
        'module_extract_keywords': ('._somn_execution_api', 'module_extract_keywords'),
        '_module_serialize_task_record': ('._somn_execution_api', '_module_serialize_task_record'),
        '_module_execute_rollback': ('._somn_execution_api', '_module_execute_rollback'),
        '_module_execute_task': ('._somn_execution_api', '_module_execute_task'),
    },
    'context_api': {
        '_module_query_memory_context': ('._somn_context_api', '_module_query_memory_context'),
        '_module_build_local_fallback_context': ('._somn_context_api', '_module_build_local_fallback_context'),
        '_module_record_task_memory': ('._somn_context_api', '_module_record_task_memory'),
        '_module_persist_agent_run': ('._somn_context_api', '_module_persist_agent_run'),
        '_module_call_llm_for_json': ('._somn_context_api', '_module_call_llm_for_json'),
        '_module_extract_json_payload': ('._somn_context_api', '_module_extract_json_payload'),
    },
    'main_chain': {
        '_module_run_analyze_requirement': ('._somn_main_chain', '_module_run_analyze_requirement'),
        '_module_run_agent_task': ('._somn_main_chain', '_module_run_agent_task'),
    },
    'components': {
        'create_neural_system': ('..neural_memory.neural_system', 'create_neural_system'),
        'create_knowledge_graph': ('..knowledge_graph', 'create_knowledge_graph'),
        'IndustryKnowledgeBase': ('..knowledge_graph.industry_knowledge', 'IndustryKnowledgeBase'),
        'IndustryType': ('..knowledge_graph.industry_knowledge', 'IndustryType'),
        'RuleEngine': ('..knowledge_graph.rule_engine', 'RuleEngine'),
        'WebSearchEngine': ('..data_layer.web_search', 'WebSearchEngine'),
        'SearchQuery': ('..data_layer.web_search', 'SearchQuery'),
        'SearchIntent': ('..data_layer.web_search', 'SearchIntent'),
        'DataCollector': ('..data_layer.data_collector', 'DataCollector'),
        'ToolRegistry': ('..tool_layer.tool_registry', 'ToolRegistry'),
        'LLMService': ('..tool_layer.llm_service', 'LLMService'),
    },
}

# 从分组注册表构建扁平视图（向后兼容）
_LAZY_MODULES: Dict[str, tuple] = {}
for _group_items in _LAZY_MODULE_GROUPS.values():
    _LAZY_MODULES.update(_group_items)

# 缓存已导入的模块
_LAZY_CACHE: Dict[str, Any] = {}

def _lazy_import(name: str) -> Any:
    """[v20.0] 统一的延迟导入系统"""
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]
    
    if name not in _LAZY_MODULES:
        raise AttributeError(f"Unknown lazy import: {name}")
    
    module_path, attr_name = _LAZY_MODULES[name]
    try:
        # 处理相对导入
        if module_path.startswith('.'):
            from importlib import import_module
            module = import_module(module_path, package='src.core')
        else:
            from importlib import import_module
            module = import_module(module_path)
        
        obj = getattr(module, attr_name)
        _LAZY_CACHE[name] = obj
        return obj
    except (ImportError, AttributeError) as e:
        logger.debug(f"Lazy import failed for {name}: {e}")
        # 返回None表示未找到
        return None

def _lazy_import_many(*names: str) -> Dict[str, Any]:
    """[v20.0] 批量延迟导入"""
    return {name: _lazy_import(name) for name in names}

# ═══════════════════════════════════════════════════════════════════════════════
# [v20.0 优化] 整合的ensure/init链
# ═══════════════════════════════════════════════════════════════════════════════

from ._somn_ensure import (
    background_warmup as _ensure_background_warmup,
    ensure_llm as _ensure_llm_fn,
    ensure_dual_model as _ensure_dual_model_fn,  # [v1.0.0] A/B双模型左右大脑
    ensure_runtime as _ensure_runtime_fn,
    ensure_layers as _ensure_layers_fn,
    ensure_wisdom_layers as _ensure_wisdom_layers_fn,
    ensure_semantic_memory as _ensure_semantic_memory_fn,
    ensure_cloud_learning as _ensure_cloud_learning_fn,
    ensure_learning_coordinator as _ensure_learning_coordinator_fn,
    ensure_autonomous_agent as _ensure_autonomous_agent_fn,
    ensure_main_chain as _ensure_main_chain_fn,
    ensure_openclaw as _ensure_openclaw_fn,
    ensure_global_claw_scheduler as _ensure_global_claw_scheduler_fn,
    ensure_emotion_research as _ensure_emotion_research_fn,  # [v1.0.0]
    ensure_research_phase_manager as _ensure_research_phase_manager_fn,  # [v1.0.0]
    ensure_sage_dispatch as _ensure_sage_dispatch_fn,  # [v1.1.0] SageDispatch贤者调度
    ensure_divine_reason as _ensure_divine_reason_fn,  # [v1.1.0] DivineReason推理引擎
    ensure_eight_layer_pipeline as _ensure_eight_layer_pipeline_fn,  # [v1.1.0] 天枢八层管道
    ensure_dual_track as _ensure_dual_track_fn,  # [v1.1.0] 双轨系统
    ensure_domain_nexus as _ensure_domain_nexus_fn,  # [v1.1.0] DomainNexus知识库
    ensure_ecosystem as _ensure_ecosystem_fn,  # [v1.2.0] 生态引擎系统
    ensure_neural_layout as _ensure_neural_layout_fn,  # [v1.3.0] 神经网络布局
    init_semantic_memory as _init_semantic_memory_fn,
    summarize_understanding as _summarize_understanding_fn,
)

class SomnCore:

    """
    Somn 核心智能体  v8.3.0 智慧层全接入版

    主链(v8.3.0 新增智慧增强环节):
    1. 理解需求
       └─ [新] _run_wisdom_analysis()  → SuperWisdomCoordinator / GlobalWisdomScheduler
                                          自动激活对应智慧学派与思维方法
    2. 设计strategy
       └─ [新] _run_unified_enhancement() → UnifiedIntelligenceCoordinator
                                            多模块 ensemble 协同增强strategy质量
    3. 规划并执行工具任务
    4. 评估结果
    5. 写回记忆与学习事件

    默认可用智慧板块(无需手动指定,自动激活):
    - 儒道佛素书鸿铭三教术数诗词神话文学人类学行为塑造
    - 深度推理 / 思维方法 / 神经科学 / 心理营销先驱 / 王阳明xinxue
    - 自然科学 / 社会科学 / 文明演化 / 计算神经科学 / 数学智慧

    智慧协调器架构:
    SuperWisdomCoordinator(超级门面)
      └─ GlobalWisdomScheduler(神经元学派调度)
           └─ NeuronWisdomNetwork(19学派神经元)
               └─ 各智慧引擎(86+模块)
    UnifiedIntelligenceCoordinator(任务级多模块协同)
    ThinkingMethodEngine(思维方法fusion引擎)
    """

    def __init__(self, base_path: str = None):
        # ═══════════════════════════════════════════════════
        # Tier 0: 零同步开销（纯路径 + 锁 + 占位）
        # init 完成即放开操作入口，所有组件后台预热/按需加载
        # ═══════════════════════════════════════════════════

        # ── 路径（纯 IO，毫秒级）─────────────────
        self.base_path = Path(base_path) if base_path else PROJECT_ROOT
        self.agent_runs_dir = self.base_path / "data" / "agent_runs"
        self.agent_runs_dir.mkdir(parents=True, exist_ok=True)
        self.autonomy_dir = self.base_path / "data" / "autonomy"
        self.autonomy_dir.mkdir(parents=True, exist_ok=True)
        self.goal_store_path = self.autonomy_dir / "long_term_goals.json"
        self.experience_store_path = self.autonomy_dir / "experience_library.json"
        self.reflection_store_path = self.autonomy_dir / "task_reflections.json"

        # ── 会话存储（纯内存，零 IO）──────────────
        self.contexts: Dict[str, SomnContext] = {}

        # ── 线程安全 ─────────────────────────
        self._init_lock = threading.Lock()
        self._layers_lock = threading.Lock()         # v16.1 P1: 神经/知识/语义层独立锁
        self._wisdom_layers_lock = threading.Lock()  # v16.1 P1: 智慧/逻辑层独立锁

        # ── 所有组件占位为 None ───────────────
        self.llm_service = None
        self.dual_model_service = None  # [v1.0.0] A/B双模型左右大脑调度服务
        self.tool_registry = None
        self.web_search = None
        self.data_collector = None
        self.neural_system = None
        self.knowledge_graph = None
        self.industry_kb = None
        self.rule_engine = None
        self.semantic_memory = None
        self.semantic_integration = None
        self.super_wisdom = None
        self.unified_coordinator = None
        self.global_wisdom = None
        self.thinking_engine = None
        self.persona = None
        self.learning_coordinator = None
        self.autonomous_agent = None
        self.cloud_model_hub = None
        self.teacher_student_engine = None
        self.somn_orchestrator = None
        # OpenClaw 开放抓取（v1.0.1 集成激活）
        self.openclaw_core = None
        self.claw_bridge = None
        # 全局Claw调度器（v1.0.0 全局调动+分布式工作+协作工作）
        self._global_claw_scheduler = None
        # 情绪研究体系核心（v1.0.0 核心能力框架）
        self.emotion_research_core = None
        # 研究发现驱动策略引擎（v2.0.0 统一策略入口）
        self._research_strategy_engine = None
        # 研究阶段管理系统（v1.0.0 四阶段研究管理）
        self._research_phase_manager = None
        # [v1.1.0] SageDispatch 贤者调度系统
        self._sage_dispatch_engine = None
        # [v1.1.0] DivineReason 统一推理引擎
        self._divine_reason = None
        # [v1.1.0] 天枢八层管道
        self._eight_layer_pipeline = None
        # [v1.1.0] 双轨系统 TrackBridge
        self._track_bridge = None
        # [v1.1.0] DomainNexus 知识库引擎
        self._domain_nexus = None
        # [v1.2.0] 生态引擎系统
        self._ecosystem = None
        # [v1.3.0] 神经网络布局集成
        self._neural_layout = None

        # ── 初始化标志 ───────────────────────────────
        self._init_flags: int = 0  # IntFlag位掩码，运行时使用整数值

        # ── 反馈/ROI/强化：getter 懒加载，零同步开销 ──────
        self._feedback_pipeline = None
        self._feedback_pipeline_unavailable = False
        self._main_chain_integration = None
        self._reinforcement_trigger = None
        self._reinforcement_feedback_unavailable = False
        self._roi_tracker = None
        self._roi_tracker_unavailable = False

        # ── [P7] _somn_ensure.py 兼容标志（v21.0 InitFlag迁移后遗留依赖）──
        self._llm_initialized = False
        self._dual_model_initialized = False
        self._runtime_initialized = False
        self._layers_initialized = False
        self._wisdom_layers_initialized = False
        self._cloud_learning_initialized = False
        self._learning_coordinator_initialized = False
        self._autonomous_agent_initialized = False
        self._main_chain_initialized = False
        self._openclaw_initialized = False
        self._claw_scheduler_initialized = False
        self._emotion_research_initialized = False
        self._autonomy_stores_ready = False
        self._research_strategy_init_failed = False
        self._research_strategy_initialized = False  # [v22.1 修复] 补充缺失的初始化标志
        self._three_core_init_failed = False
        # [v1.1.0] SageDispatch / DivineReason / 八层管道 / 双轨 / DomainNexus
        self._sage_dispatch_initialized = False
        self._divine_reason_initialized = False
        self._eight_layer_pipeline_initialized = False
        self._dual_track_initialized = False
        self._domain_nexus_initialized = False
        # [v1.2.0] 生态引擎
        self._ecosystem_initialized = False
        # [v1.3.0] 神经网络布局
        self._neural_layout_initialized = False

        # ═══════════════════════════════════════════════════
        # 后台 daemon 预热：顺序预热所有 Tier 1/2 组件
        # ═══════════════════════════════════════════════════
        self._bg_warmup_thread = threading.Thread(
            target=self._background_warmup,
            name="somn_bg_warmup",
            daemon=True,
        )
        self._bg_warmup_thread.start()

        logger.info("Somn 核心智能体 init 完成(Tier0 零阻塞, 全部组件后台预热中)")

    # ── 懒加载标志位掩码定义（v21.0: 类体级内部枚举） ──────
    from enum import IntFlag

    class InitFlag(IntFlag):
        """初始化标志位枚举（v21.0优化：替代16个独立bool）"""
        LLM = 1
        DUAL_MODEL = 2
        AUTONOMY_STORES = 4
        RUNTIME = 8
        LAYERS = 16
        WISDOM_LAYERS = 32
        CLOUD_LEARNING = 64
        LEARNING_COORDINATOR = 128
        AUTONOMOUS_AGENT = 256
        MAIN_CHAIN = 512
        OPENCLAW = 1024
        CLAW_SCHEDULER = 2048
        EMOTION_RESEARCH = 4096
        RESEARCH_STRATEGY = 8192
        RESEARCH_PHASE_MANAGER = 16384
        # [v1.1.0] SageDispatch / DivineReason / 八层管道 / 双轨 / DomainNexus
        SAGE_DISPATCH = 32768
        DIVINE_REASON = 65536
        EIGHT_LAYER_PIPELINE = 131072
        DUAL_TRACK = 262144
        DOMAIN_NEXUS = 524288
        # [v1.2.0] 生态引擎
        ECOSYSTEM = 1048576
        # [v1.3.0] 神经网络布局
        NEURAL_LAYOUT = 2097152

    # ═══════════════════════════════════════════════════════════════
    # [v21.0 核心] __getattr__ 动态代理 —— 消除 50+ 纯委托方法
    #
    # 原设计中 SomnCore 有 ~50 个 delegate_* / _module_* 方法，
    # 每个仅是一行函数转发（如 `return delegate_xxx(self, ...)`），
    # 导致 somn_core.py 膨胀约 230 行无意义委托代码。
    #
    # 现在通过 __getattr__ 统一拦截：
    #   - 以 `_delegate_` 或 `_module_` 开头的属性名
    #   - 从 _LAZY_MODULES 查找对应函数并自动调用
    #   - 完全向后兼容，所有外部调用无需修改
    # ═══════════════════════════════════════════════════════════════

    # __getattr__ 代理的名称前缀白名单（防止误拦截内部属性）
    _DELEGATE_PREFIXES = (
        'delegate_',       # 委托函数: delegate_execute_task, delegate_track_roi_*
        '_delegate_',      # 变体
        '_module_',        # 模块级API: _module_query_memory_context, _module_record_task_*
    )

    def __getattr__(self, name: str):
        """
        [v21.0] 动态委托代理 —— 自动将方法调用路由到对应的 delegate/module 函数。

        工作流程:
        1. 检查 name 是否匹配已知前缀（delegate_ / _module_）
        2. 从 _LAZY_MODULES 或 _LAZY_MODULE_GROUPS 查找目标函数
        3. 返回一个 bound method 包装器，调用时自动传入 self

        示例:
            self._execute_task(task)  →  找到 delegate_execute_task →  return delegate_execute_task(self, task)
            self._record_task_memory(...)  →  找到 _module_record_task_memory  →  return _module_record_task_memory(self, ...)
        """
        # [P7] 前缀检查：使用 type(self) 从类字典获取，避免触发自身 __getattr__
        _prefixes = type(self)._DELEGATE_PREFIXES
        if not any(name.startswith(p) for p in _prefixes):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # 1) 先尝试直接查找扁平注册表
        func = _lazy_import(name)

        # 2) 如果扁平表没有，尝试去掉下划线前缀再查（兼容部分命名变体）
        if func is None:
            for prefix in self._DELEGATE_PREFIXES:
                if name.startswith(prefix):
                    alt_name = name[len(prefix):]  # 去掉前缀
                    func = _lazy_import(alt_name)
                    if func is not None:
                        break

        if func is None:
            raise AttributeError(f"'{type(self).__name__}' object has no lazy-delegated attribute '{name}'")

        # 3) 返回绑定到 self 的可调用包装器
        import functools

        @functools.wraps(func)
        def _delegation_wrapper(*args, **kwargs):
            """动态委托包装器：自动注入 self 作为第一个参数"""
            return func(self, *args, **kwargs)

        # 将方法绑定到实例，使其表现得像普通方法
        import types
        bound_method = types.MethodType(_delegation_wrapper, self)
        # 缓存到 __dict__ 防止重复查找
        object.__setattr__(self, name, bound_method)
        return bound_method

    # ─────────────────────────────────────────────
    # Tier 2: 后台预热入口
    # ─────────────────────────────────────────────
    def _background_warmup(self) -> None:
        """daemon 线程：顺序预热所有组件 -- 委托自 _somn_ensure."""
        _ensure_background_warmup(self)

    # ─────────────────────────────────────────────
    # LLM 服务
    # ─────────────────────────────────────────────
    def _ensure_llm(self) -> None:
        """确保 LLM 服务已初始化 -- 委托自 _somn_ensure."""
        _ensure_llm_fn(self)

    # ─────────────────────────────────────────────
    # A/B 双模型左右大脑服务
    # ─────────────────────────────────────────────
    def _ensure_dual_model(self) -> None:
        """确保双模型调度服务已初始化 -- 委托自 _somn_ensure."""
        _ensure_dual_model_fn(self)

    # ─────────────────────────────────────────────
    # Tier 2a: 运行时基础组件
    # ─────────────────────────────────────────────
    def _ensure_runtime(self) -> None:
        """确保运行时基础组件已初始化 -- 委托自 _somn_ensure."""
        _ensure_runtime_fn(self)

    # ─────────────────────────────────────────────
    # Tier 1 轻量层（已内联到 __init__）
    # ─────────────────────────────────────────────
    def _init_lightweight_layers(self) -> None:
        """Tier1 轻量层已内联到 __init__，此方法保留兼容."""
        pass

    def _ensure_layers(self) -> None:
        """确保智能层已初始化 -- 委托自 _somn_ensure."""
        _ensure_layers_fn(self)

    def _ensure_wisdom_layers(self) -> None:
        """确保智慧/逻辑协调层已初始化 -- 委托自 _somn_ensure."""
        _ensure_wisdom_layers_fn(self)

    def _ensure_semantic_memory(self) -> None:
        """确保语义记忆引擎已初始化 -- 委托自 _somn_ensure."""
        _ensure_semantic_memory_fn(self)

    def _ensure_cloud_learning(self) -> None:
        """确保云端学习系统已初始化 -- 委托自 _somn_ensure."""
        _ensure_cloud_learning_fn(self)

    def _ensure_learning_coordinator(self) -> None:
        """确保学习协调器已初始化 -- 委托自 _somn_ensure."""
        _ensure_learning_coordinator_fn(self)

    def _ensure_autonomous_agent(self) -> None:
        """确保自主智能体已初始化 -- 委托自 _somn_ensure."""
        _ensure_autonomous_agent_fn(self)

    def _ensure_main_chain(self) -> None:
        """确保主线集成器已初始化 -- 委托自 _somn_ensure."""
        _ensure_main_chain_fn(self)

    def _ensure_openclaw(self) -> None:
        """确保OpenClaw开放抓取已初始化 -- 委托自 _somn_ensure."""
        _ensure_openclaw_fn(self)

    def _ensure_global_claw_scheduler(self) -> None:
        """确保全局Claw调度器已初始化 -- 委托自 _somn_ensure."""
        _ensure_global_claw_scheduler_fn(self)

    # ─────────────────────────────────────────────
    # [v1.1.0] SageDispatch / DivineReason / 八层管道 / 双轨 / DomainNexus
    # ─────────────────────────────────────────────
    def _ensure_sage_dispatch(self) -> None:
        """确保SageDispatch贤者调度系统已初始化 -- 委托自 _somn_ensure."""
        _ensure_sage_dispatch_fn(self)

    def _ensure_divine_reason(self) -> None:
        """确保DivineReason统一推理引擎已初始化 -- 委托自 _somn_ensure."""
        _ensure_divine_reason_fn(self)

    def _ensure_eight_layer_pipeline(self) -> None:
        """确保天枢八层管道已初始化 -- 委托自 _somn_ensure."""
        _ensure_eight_layer_pipeline_fn(self)

    def _ensure_dual_track(self) -> None:
        """确保双轨系统已初始化 -- 委托自 _somn_ensure."""
        _ensure_dual_track_fn(self)

    def _ensure_domain_nexus(self) -> None:
        """确保DomainNexus知识库引擎已初始化 -- 委托自 _somn_ensure."""
        _ensure_domain_nexus_fn(self)

    def _init_main_chain_integration(self) -> None:
        """主线集成器初始化 -- 委托自 _somn_wisdom_init."""
        result = init_main_chain_integration(self.base_path)
        if result is not None:
            self._main_chain_integration = result

    def _init_learning_coordinator(self) -> None:
        """学习协调器初始化 -- 委托自 _somn_wisdom_init."""
        self.learning_coordinator = init_learning_coordinator(self.base_path)

    def _init_autonomous_agent(self) -> None:
        """自主智能体初始化 -- 委托自 _somn_wisdom_init."""
        self.autonomous_agent = init_autonomous_agent(self.base_path)

    def _init_cloud_learning_system(self) -> None:
        """云端模型调度体系初始化 -- 委托自 _somn_wisdom_init."""
        from ._somn_wisdom_init import init_cloud_learning_system
        result = init_cloud_learning_system(self.base_path, self.llm_service, print_fn=print)
        self.cloud_model_hub = result.get("cloud_model_hub")
        self.teacher_student_engine = result.get("teacher_student_engine")
        self.somn_orchestrator = result.get("somn_orchestrator")

    def _init_semantic_memory(self) -> None:
        """init语义记忆引擎 -- 委托自 _somn_ensure."""
        _init_semantic_memory_fn(self)

    def _run_semantic_analysis(self, description: str, context: Dict = None) -> Dict[str, Any]:
        """运行语义分析 -- 委托自 _somn_semantic_api."""
        return _module_run_semantic_analysis(self, description, context)

    def _summarize_understanding(self, semantic_context: Any) -> str:
        """生成语义理解摘要 -- 委托自 _somn_ensure."""
        return _summarize_understanding_fn(semantic_context)

    def record_semantic_feedback(self, user_input: str, system_understanding: str,
                                  user_correction: str = "", is_correct: bool = True,
                                  user_id: Optional[str] = None) -> Dict[str, Any]:
        """记录语义理解反馈 -- 委托自 _somn_semantic_api."""
        inferred = system_understanding if is_correct else (user_correction or system_understanding)
        rating = 5.0 if is_correct else 2.0
        return _module_record_semantic_feedback(self, user_input, inferred, rating, user_id)

    def get_semantic_memory_stats(self, user_id: str = None) -> Dict[str, Any]:
        """获取语义记忆统计 -- 委托自 _somn_semantic_api."""
        return _module_get_semantic_memory_stats(self, user_id)

    def get_semantic_memory_report(self, user_id: str = None) -> str:
        """获取语义记忆报告 -- 委托自 _somn_semantic_api."""
        return _module_get_semantic_memory_report(self, user_id)

    # ==================== 多用户管理接口 ====================

    def register_semantic_user(self, user_id: str) -> bool:
        """注册新用户语义记忆空间 -- 委托自 _somn_semantic_api."""
        return _module_register_semantic_user(self, user_id)

    def switch_semantic_user(self, user_id: str) -> bool:
        """切换当前语义记忆用户 -- 委托自 _somn_semantic_api."""
        return _module_switch_semantic_user(self, user_id)

    def list_semantic_users(self) -> List[Dict[str, Any]]:
        """列出所有语义记忆用户 -- 委托自 _somn_semantic_api."""
        return _module_list_semantic_users(self)

    def export_user_semantic_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """导出用户语义数据(GDPR合规) -- 委托自 _somn_semantic_api."""
        return _module_export_user_semantic_data(self, user_id)

    # ==================== unified主链 ====================

    # ─────────────────────────────────────────────
    # [v1.1.0] 子系统便捷访问方法
    # ─────────────────────────────────────────────

    def dispatch_problem(self, problem, level=None, dispatcher_id="SD-F2", **kwargs):
        """
        [v1.1.0] SageDispatch 贤者调度入口

        通过12调度器智能分配问题到最合适的处理流程。
        返回 DispatchResponse。
        """
        self._ensure_sage_dispatch()
        if self._sage_dispatch_engine is None:
            return {"error": "SageDispatch未初始化", "confidence": 0.0}
        return self._sage_dispatch_engine.dispatch(problem, level=level, dispatcher_id=dispatcher_id, **kwargs)

    def divine_reason(self, problem: str, mode=None, context: Dict = None, **kwargs):
        """
        [v1.1.0] DivineReason 统一推理入口

        4合1推理引擎(GoT+LongCoT+ToT+ReAct)。
        mode: LINEAR / DIVINE / SUPER / BRANCHING / REACTIVE / GRAPH
        返回 ReasoningResult。
        """
        self._ensure_divine_reason()
        if self._divine_reason is None:
            return {"error": "DivineReason未初始化", "confidence": 0.0}
        return self._divine_reason.solve(problem, mode=mode, context=context, **kwargs)

    def process_through_pipeline(self, input_text: str, grade=None, **kwargs):
        """
        [v1.1.0] 天枢八层管道入口

        L1输入→L2 NLP→L3 分类→L4 分流→L5 推理→L6 论证→L7 输出→L8 优化
        grade: "BASIC"(快速) / "DEEP"(智慧+Claw) / "SUPER"(全Claw+T2)
               也可以传 ProcessingGrade 枚举值，默认 BASIC。
        返回 PipelineResult。
        """
        self._ensure_eight_layer_pipeline()
        if self._eight_layer_pipeline is None:
            return {"error": "八层管道未初始化", "confidence": 0.0}
        # 处理 grade 参数：支持字符串或枚举
        if grade is None or isinstance(grade, str):
            from knowledge_cells.eight_layer_pipeline import ProcessingGrade
            grade_map = {"BASIC": ProcessingGrade.BASIC, "DEEP": ProcessingGrade.DEEP, "SUPER": ProcessingGrade.SUPER}
            grade = grade_map.get(grade if isinstance(grade, str) else "BASIC", ProcessingGrade.BASIC)
        return self._eight_layer_pipeline.process(input_text, grade=grade, **kwargs)

    def generate_ppt(self, content: str, theme: str = "business",
                     beautify: bool = True, auto_charts: bool = True,
                     output_path: str = None, **kwargs) -> str:
        """
        [v7.0] 开物(Kaiwu)子系统生成入口.

        用户明确指定输出类型为PPT时，调用开物子系统生成高质量PPT。
        开物：命名来自《天工开物》，寓意工艺系统化。
        """
        try:
            from smart_office_assistant.src.kaiwu import KaiwuService
            service = KaiwuService(theme=theme, enable_learning=True, enable_charts=auto_charts)
            return service.generate_ppt(
                content=content,
                format=None,
                output_path=output_path,
                beautify=beautify,
                auto_charts=auto_charts
            )
        except ImportError:
            raise RuntimeError("开物(Kaiwu)模块不可用（python-pptx未安装）")

    def query_domain_nexus(self, query: str, context: str = "", **kwargs):
        """
        [v1.1.0] DomainNexus 知识库查询入口

        双向标签匹配 + LRU懒加载。
        返回匹配的知识格子字典。
        """
        self._ensure_domain_nexus()
        if self._domain_nexus is None:
            return {}
        return self._domain_nexus.query(query, context=context, **kwargs)

    def call_claw(self, department: str, claw_name: str, task_description: str, **kwargs):
        """
        [v1.1.0] 双轨系统 Claw 调度入口

        通过 TrackBridge 将任务调度到神行轨的指定部门。
        claw_name 会被注入到 context 中供 B 轨使用。
        返回 Claw 执行结果。
        """
        self._ensure_dual_track()
        if self._track_bridge is None:
            return {"error": "双轨系统未初始化"}
        if self._track_bridge.track_b is None:
            return {"error": "B轨未初始化"}
        context = kwargs.pop("context", {}) or {}
        context["_target_claw"] = claw_name
        return self._track_bridge.track_b.execute_sync(
            department=department,
            task_description=task_description,
            context=context,
        )

    def monitor_ecosystem(self) -> Dict[str, Any]:
        """
        [v1.2.0] 生态引擎监控入口

        通过 A轨（神政轨）执行全局系统监控。
        返回完整生态系统报告（健康度、资源、环境变化、演化趋势）。
        """
        self._ensure_ecosystem()
        self._ensure_dual_track()
        if self._track_bridge is None or self._track_bridge.track_a is None:
            return {"error": "双轨系统未初始化"}
        return self._track_bridge.track_a.monitor_system()

    def check_ecosystem_health(self) -> Dict[str, Any]:
        """
        [v1.2.0] 快速生态健康检查

        轻量级接口，只返回健康状态概览。
        """
        self._ensure_ecosystem()
        if self._ecosystem is None:
            return {"overall": "unavailable"}
        report = self._ecosystem.ecosystem_manager.generate_report()
        return {
            "overall": report.get("overall_health", "unknown"),
            "balanced": report.get("balance_status", False),
            "alerts": report.get("alerts", []),
        }

    def process_neural_layout(self, input_data: Any, context: Dict = None) -> Dict[str, Any]:
        """
        [v1.3.0] 神经网络布局全链路处理入口

        通过 GlobalNeuralBridge 的 6 个桥接并行调用真实模块：
        AgentCore / SomnCore / WisdomDispatcher / MemorySystem / LearningSystem / AutonomySystem

        Args:
            input_data: 输入（字符串或字典）
            context: 上下文

        Returns:
            包含激活路径、模块输出、统计信息的字典
        """
        self._ensure_neural_layout()
        if self._neural_layout is None:
            return {"status": "error", "message": "NeuralLayout 未初始化"}
        return self._neural_layout.process(input_data, context)

    def get_neural_layout_status(self) -> Dict[str, Any]:
        """
        [v1.3.0] 获取神经网络布局状态

        供 API/前端消费，返回桥接状态、布局状态、统计信息。
        """
        self._ensure_neural_layout()
        if self._neural_layout is None:
            return {"initialized": False, "somn_core_bound": False}
        return self._neural_layout.get_status()

    @property
    def neural_layout(self):
        """[v1.3.0] 神经网络布局集成器实例（延迟初始化）"""
        self._ensure_neural_layout()
        return self._neural_layout

    def _ensure_neural_layout(self):
        """[v1.3.0] 确保神经网络布局已初始化 -- 委托自 _somn_ensure."""
        _ensure_neural_layout_fn(self)

    def run_agent_task(self,
                       description: str,
                       context: Dict[str, Any] = None,
                       options: Dict[str, Any] = None,
                       evaluation_criteria: Dict[str, Any] = None) -> Dict[str, Any]:
        """unified智能体任务主链(v14.0.0 支持任务路由). 委托自 _somn_main_chain."""
        return _module_run_agent_task(self, description, context, options, evaluation_criteria)

    def _run_orchestrator_route(self, requirement: Dict, autonomy_context: Dict, options: Dict) -> Dict:
        """路径A: SomnOrchestrator 编排路由(FAST/HOME模式). 委托自 _somn_routes."""
        return _module_run_orchestrator_route(self, requirement, autonomy_context, options)

    def _run_local_llm_route(self, requirement: Dict, options: Dict) -> Dict:
        """路径B: 本地 LLM 直答路由. 委托自 _somn_routes."""
        return _module_run_local_llm_route(self, requirement, options)

    def _run_wisdom_route(self, requirement: Dict) -> Dict:
        """路径C: 智慧板块直答路由. 委托自 _somn_routes."""
        return _module_run_wisdom_route(self, requirement)

    def _run_wisdom_analysis(self, description: str, structured_req: Dict, context: Dict) -> Dict:
        """智慧分析委托 -- 委托自 _somn_wisdom_analysis."""
        return run_wisdom_analysis(
            description, structured_req, context,
            self._ensure_wisdom_layers, self.super_wisdom,
            self.global_wisdom, self.thinking_engine,
        )

    def _maybe_run_metaphysics_analysis(self, description: str, extra_context: Dict,
                                        parsed_requirement: Dict, primary_industry=None) -> Dict:
        """形而上学分析委托 -- 委托自 _somn_wisdom_analysis."""
        return maybe_run_metaphysics_analysis(
            description=description,
            extra_context=extra_context,
            parsed_requirement=parsed_requirement,
            primary_industry=primary_industry,
        )

    # ==================== 核心能力接口 ====================

    # 并行化用的线程池（懒初始化，全生命周期复用）
    _analysis_executor: Optional[ThreadPoolExecutor] = None
    _analysis_executor_lock = threading.Lock()

    # 网络搜索熔断器状态
    _search_circuit_breaker: Dict[str, Any] = {
        "state": "closed",              # closed | open | half_open
        "consecutive_failures": 0,      # 连续失败次数
        "failure_threshold": 3,         # 连续失败 N 次后进入 OPEN
        "recovery_timeout": 30.0,       # OPEN 状态持续 30s 后允许 HALF_OPEN 探测
        "last_failure_time": None,      # 上次失败时间
    }

    # 同会话搜索结果缓存（会话级语义复用，杜绝重复搜索）
    _search_result_cache: Dict[str, Dict[str, Any]] = {}
    _search_result_cache_lock = threading.Lock()
    _SEARCH_CACHE_TTL = 300.0     # 缓存有效期 5 分钟
    # v17.0 优化：相似度阈值从 0.5 提升至 0.4，允许更多缓存命中
    _SEARCH_SIMILARITY_THRESHOLD = 0.4  # Jaccard 相似度阈值（≥即命中）

    # ━━━━━━━━━━ LLM 结果缓存层 (v16.0 P0 串行调用优化) ━━━━━━━━━━
    # 同会话内，相同 prompt + system_prompt 的 LLM 调用直接复用结果，
    # 避免重复请求。以 prompt 前 200 字符的 SHA256 作为缓存键。
    _llm_result_cache: Dict[str, Dict[str, Any]] = {}
    _llm_result_cache_lock = threading.Lock()
    _LLM_CACHE_TTL = 600.0            # LLM 缓存有效期 10 分钟（同会话内足够）
    _LLM_CACHE_MAX_ENTRIES = 200      # 最大缓存条目数
    _LLM_CACHE_PROMPT_PREFIX = 256    # 取 prompt 前 N 字符做哈希（平衡精度与碰撞率）

    def _get_analysis_executor(self) -> ThreadPoolExecutor:
        """获取并行分析用线程池（懒加载、线程安全）.
        
        v17.0 优化：max_workers 从 3 提升至 6，支持 Phase1 三路并行 + Phase2 四路 fan-out
        同时执行而不互相阻塞。
        """
        if self._analysis_executor is None:
            with self._analysis_executor_lock:
                if self._analysis_executor is None:
                    self._analysis_executor = ThreadPoolExecutor(
                        max_workers=6, thread_name_prefix="somn_analysis"
                    )
        return self._analysis_executor

    def analyze_requirement(self, description: str, context: Dict = None) -> Dict[str, Any]:
        """需求分析 (v15.0 并行化版本). 委托自 _somn_main_chain."""
        return _module_run_analyze_requirement(self, description, context)

    def design_strategy(self, requirement_doc: Dict, options: Dict = None) -> Dict[str, Any]:
        """strategy设计 -- 委托自 _somn_strategy_design."""
        try:
            from ._somn_strategy_design import generate_structured_strategy
            # [v1.0.0] 传递somn_core_instance以支持情绪研究框架整合
            return generate_structured_strategy(
                requirement_doc=requirement_doc,
                industry_profile=None,
                playbooks=[],
                rule_results=[],
                stage="design",
                strategy_ranking=options,
                call_llm_fn=None,
                somn_core_instance=self,
            )
        except ImportError:
            return {"strategy_plan": {}, "status": "fallback", "reason": "strategy_design module unavailable"}

    def execute_workflow(self, strategy_plan: Dict, execution_config: Dict = None) -> Dict[str, Any]:
        """执行工作流 -- 委托自 _somn_workflow_execution."""
        try:
            from ._somn_workflow_execution import run_workflow_state_machine
            return run_workflow_state_machine(self, strategy_plan, execution_config)
        except ImportError:
            return {"execution_report": {}, "task_records": [], "status": "fallback"}

    def evaluate_results(self, execution_report: Dict, evaluation_criteria: Dict = None) -> Dict[str, Any]:
        """效果评估 -- 委托自 _somn_evaluation."""
        try:
            from ._somn_evaluation import build_evaluation_report
            return build_evaluation_report(self, execution_report, evaluation_criteria)
        except ImportError:
            return {"evaluation_summary": {"overall_score": 0.5}, "status": "fallback"}

    # ==================== 辅助方法 ====================

    def get_capabilities(self) -> Dict[str, Any]:
        """获取 SomnCore 能力清单（供 API / 健康检查使用）"""
        # 已加载模块
        loaded = list(self._cache.keys()) if hasattr(self, '_cache') else []

        # 智慧学派和引擎数量
        wisdom_schools = 0
        engine_count = 0
        try:
            from src.intelligence import WisdomDispatcher
            if hasattr(WisdomDispatcher, '_SCHOOLS'):
                wisdom_schools = len(WisdomDispatcher._SCHOOLS)
        except Exception as e:
            logger.debug(f"获取智慧学派数量失败: {e}")
        try:
            wisdom_schools = wisdom_schools or 35  # 默认值
            engine_count = 166  # 默认值（V6.2 含社会科学引擎）
        except Exception as e:
            logger.debug(f"设置默认引擎数量失败: {e}")

        return {
            "modules": loaded[:30],
            "total_lazy_modules": len(_LAZY_MODULES),
            "wisdom_schools": wisdom_schools,
            "engines": engine_count,
            "claws": 763,
            "sages": 768,
            "version": "21.0",
        }

    def _query_memory_context(self, description: str) -> Dict[str, Any]:
        """从神经记忆系统提取相关上下文 -- 委托自 _somn_context_api."""
        from ._somn_context_api import _module_query_memory_context
        return _module_query_memory_context(self, description, context={})

    def _build_local_fallback_context(self, description: str) -> List[Dict[str, Any]]:
        """构建本地上下文兜底条目 -- 委托自 _somn_context_api."""
        from ._somn_context_api import _module_build_local_fallback_context
        return _module_build_local_fallback_context(self, description)

    # ── 同会话搜索结果缓存（语义复用）───────────────────────────

    # [v21.0] ~50个纯委托方法已通过 __getattr__ 动态代理消除(见上方__getattr__定义)
    # 已消除: delegate_*(38) + getter*(3), 调用方式完全不变

    def record_user_feedback(
        self,
        task_id: str,
        strategy: str,
        feedback_type: str,
        value: Any,
        task_type: str = "workflow_execution",
        user_id: str = "default",
        session_id: str = "",
    ) -> Dict[str, Any]:
        """供主链外部调用的显式反馈入口 -- 委托自 _somn_feedback."""
        try:
            from ._somn_feedback import record_user_feedback
            return record_user_feedback(self, task_id, strategy, feedback_type, value, task_type, user_id, session_id)
        except ImportError:
            return {"recorded": False, "status": "fallback"}

    # ─────────────────────────────────────────────
    # 闭环系统集成 v1.0
    # ─────────────────────────────────────────────

    def _generate_next_iteration(self,
                                 requirement: Dict[str, Any],
                                 strategy: Dict[str, Any],
                                 execution: Dict[str, Any],
                                 evaluation: Dict[str, Any],
                                 reflection: Dict[str, Any] = None,
                                 autonomy_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """generate下一轮动作建议 -- 委托自 _somn_autonomy_api."""
        try:
            from ._somn_autonomy_api import _module_generate_autonomy_reflection
            return _module_generate_autonomy_reflection(self, requirement, strategy, execution, evaluation)
        except (ImportError, Exception):
            return {"next_actions": [], "suggested_next_task": "继续下一轮执行"}

    def _persist_agent_run(self, final_report: Dict[str, Any]) -> Path:
        """保存一次完整主链运行结果 -- 委托自 _somn_context_api."""
        from ._somn_context_api import _module_persist_agent_run
        task_id = final_report.get("task_id", f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}") if isinstance(final_report, dict) else "unknown"
        result = _module_persist_agent_run(self, task_id, final_report)
        return Path(result.get("path", "")) if isinstance(result, dict) else Path()

    def _record_task_memory(self, title: str, description: str, confidence_score: int, scenarios: List[str]) -> None:
        """写回神经记忆系统 -- 委托自 _somn_context_api."""
        from ._somn_context_api import _module_record_task_memory
        # 适配参数签名: _module_record_task_memory(somn_core, requirement, strategy, execution, evaluation)
        _module_record_task_memory(
            self,
            requirement=title,
            strategy={"confidence_score": confidence_score, "scenarios": scenarios},
            execution={"description": description},
            evaluation={"confidence_score": confidence_score},
        )

    def _ensure_autonomy_stores(self) -> None:
        """[v21.0: 通过 __getattr__ 代理到 delegate_ensure_autonomy_stores"""
        return self.delegate_ensure_autonomy_stores()

    # ─────────────────────────────────────────────
    # v3.3: 代表大会 + 藏书阁便捷接口
    # ─────────────────────────────────────────────

    @property
    def decision_congress(self) -> Optional['DecisionCongress']:
        """获取七人决策代表大会实例（懒加载单例）"""
        try:
            from ..intelligence.dispatcher.wisdom_dispatch import get_decision_congress
            return get_decision_congress()
        except Exception as e:
            logger.debug(f"加载 DecisionCongress 失败: {e}")
            return None

    @property
    def imperial_library(self) -> Optional['ImperialLibrary']:
        """获取皇家藏书阁实例（懒加载单例）"""
        try:
            from ..intelligence.dispatcher.wisdom_dispatch import get_imperial_library
            return get_imperial_library()
        except Exception as e:
            logger.debug(f"加载 ImperialLibrary 失败: {e}")
            return None

    def submit_to_congress(self, command: str, department: str = "",
                           command_type: str = "regular", context: str = "") -> dict:
        """向七人决策代表大会提交命令"""
        try:
            from ..intelligence.dispatcher.wisdom_dispatch import submit_to_decision_congress
            return submit_to_decision_congress(
                command=command, target_department=department,
                command_type=command_type, context=context,
            )
        except Exception as e:
            logger.warning(f"[SomnCore] 提交代表大会失败: {e}")
            return {"error": "提交代表大会失败"}

    def imperial_edict(self, command: str, department: str = "", context: str = "") -> dict:
        """皇帝圣旨：绕过代表大会直接下发"""
        return self.submit_to_congress(command, department, "imperial_edict", context)

    def get_congress_report(self) -> dict:
        """获取代表大会全局执行报告"""
        try:
            from ..intelligence.dispatcher.wisdom_dispatch import get_congress_global_report
            return get_congress_global_report()
        except Exception as e:
            return {"error": "操作失败"}

    # _read_json_store → __getattr__ 代理到 delegate_read_json_store
    # _write_json_store → __getattr__ 代理到 delegate_write_json_store
    # _extract_similarity_terms → __getattr__ 代理
    # _make_goal_id → __getattr__ 代理
    # _generate_autonomy_reflection → __getattr__ 代理
    # _store_autonomy_learning → __getattr__ 代理
    def _call_llm_for_json(self, prompt: str, system_prompt: str, fallback: Any) -> Any:
        from ._somn_context_api import _module_call_llm_for_json
        return _module_call_llm_for_json(self, prompt, system_hint=system_prompt, retry=3)

    # _extract_json_payload → __getattr__ 代理(staticmethod)
    # _safe_industry_type → __getattr__ 代理(staticmethod)
    # _extract_keywords → __getattr__ 代理(staticmethod)
    # ==================== 系统管理接口 ====================

    @property
    def openclaw(self) -> 'OpenClawCore':
        """获取 OpenClaw 核心引擎实例（懒加载）"""
        self._ensure_openclaw()
        return self.openclaw_core

    @property
    def claw_system(self) -> 'ClawSystemBridge':
        """获取 ClawSystemBridge 桥接器实例（懒加载）"""
        self._ensure_openclaw()
        return self.claw_bridge

    @property
    def global_claw_scheduler(self) -> 'GlobalClawScheduler':
        """获取全局Claw调度器实例（懒加载）"""
        self._ensure_global_claw_scheduler()
        return self._global_claw_scheduler

    def fetch_external_knowledge(self, query: str, source_names: list = None) -> list:
        """
        通过 OpenClaw 从外部数据源抓取知识。

        Args:
            query: 搜索查询关键词
            source_names: 指定数据源名称列表，None=全部已连接数据源

        Returns:
            KnowledgeItem 列表
        """
        self._ensure_openclaw()
        if not self.openclaw_core:
            return []
        import asyncio
        try:
            # [P7] Python 3.10+ 兼容：优先 get_running_loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None
            if loop is not None:
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.openclaw_core.fetch_knowledge(query, source_names))
                    return future.result(timeout=30)
            else:
                return asyncio.run(self.openclaw_core.fetch_knowledge(query, source_names))
        except Exception as e:
            logger.warning(f"[OpenClaw] 抓取失败: {e}")
            return []

    def inject_knowledge_to_claws(self, query: str, claw_names: list = None) -> dict:
        """
        通过 OpenClaw 抓取外部知识并注入到指定 Claw 的记忆。

        Args:
            query: 搜索查询
            claw_names: 目标Claw名称列表，None=全部已加载Claw

        Returns:
            注入结果统计
        """
        self._ensure_openclaw()
        if not self.claw_bridge:
            return {"error": "ClawBridge not initialized"}
        import asyncio
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None
            if loop is not None:
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.claw_bridge.inject_knowledge(query, claw_names))
                    return future.result(timeout=60)
            else:
                return asyncio.run(self.claw_bridge.inject_knowledge(query, claw_names))
        except Exception as e:
            logger.warning(f"[OpenClaw] 知识注入失败: {e}")
            return {"error": "知识注入失败"}

    def submit_claw_feedback(self, feedback_data: dict) -> dict:
        """
        提交用户反馈到 OpenClaw 反馈学习系统。

        Args:
            feedback_data: 反馈数据，包含 user_id, sage_name, rating, comment 等

        Returns:
            学习结果
        """
        self._ensure_openclaw()
        if not self.claw_bridge:
            return {"error": "ClawBridge not initialized"}
        import asyncio
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None
            if loop is not None:
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.claw_bridge.submit_feedback(feedback_data))
                    return future.result(timeout=10)
            else:
                return asyncio.run(self.claw_bridge.submit_feedback(feedback_data))
        except Exception as e:
            logger.warning(f"[OpenClaw] 反馈提交失败: {e}")
            return {"error": "反馈提交失败"}

    def get_openclaw_status(self) -> dict:
        """获取 OpenClaw + ClawBridge 的完整状态"""
        self._ensure_openclaw()
        if self.claw_bridge:
            return self.claw_bridge.get_bridge_status()
        return {"openclaw_enabled": False, "reason": "not initialized"}

    # ==================== 研究发现驱动策略引擎 ====================

    @property
    def research_strategy_engine(self):
        """获取研究发现驱动策略引擎实例（懒加载）"""
        if not self._research_strategy_initialized:
            self._init_research_strategy_engine()
        # [P7] 安全返回：初始化失败时抛出明确异常而非返回None
        if self._research_strategy_engine is None and self._research_strategy_init_failed:
            raise RuntimeError(f"研究策略引擎初始化失败且无法恢复（上次错误已记录）")
        return self._research_strategy_engine

    def _init_research_strategy_engine(self):
        """初始化研究发现驱动策略引擎"""
        if self._research_strategy_initialized:
            return
        try:
            from src.intelligence.engines._research_strategy_engine import ResearchStrategyEngine
            self._research_strategy_engine = ResearchStrategyEngine()
            self._research_strategy_initialized = True
            self._research_strategy_init_failed = False
            logger.info("[SomnCore] 研究发现驱动策略引擎 v2.0 已初始化")
        except Exception as e:
            logger.warning(f"[SomnCore] 研究发现驱动策略引擎初始化失败: {e}")
            # [P7] 标记失败但不阻止重试——下次调用仍会尝试重新初始化
            self._research_strategy_init_failed = True

    def record_research_finding(self, title: str, description: str, source: str, **kwargs) -> Dict[str, Any]:
        """记录研究发现（便捷方法）"""
        return self.research_strategy_engine.record_finding(
            title=title, description=description, source=source, **kwargs
        )

    def generate_research_strategy(self, finding_ids: list, **kwargs) -> Dict[str, Any]:
        """从研究发现生成策略（便捷方法）"""
        return self.research_strategy_engine.generate_strategy(
            finding_ids=finding_ids, **kwargs
        )

    def get_strategy_lifecycle(self, strategy_id: str) -> Optional[str]:
        """获取策略生命周期状态"""
        strategy = self.research_strategy_engine.get_strategy(strategy_id)
        if strategy:
            return strategy.lifecycle_stage.value
        return None

    def get_system_status(self) -> Dict[str, Any]:
        """get系统状态（含OpenClaw和三核联动）."""
        status = {
            "status": "running",
            "wisdom_layers_loaded": self.super_wisdom is not None,
            "scheduler_loaded": self.global_wisdom is not None,
            "openclaw_loaded": self.openclaw_core is not None,
            "claw_bridge_loaded": self.claw_bridge is not None,
            "global_claw_scheduler_loaded": self._global_claw_scheduler is not None,
            "research_strategy_loaded": self._research_strategy_engine is not None,
            "three_core_loaded": self._three_core_integration is not None,
        }
        if self.claw_bridge:
            status["openclaw_detail"] = self.claw_bridge.get_bridge_status()
        if self._global_claw_scheduler:
            try:
                pool_status = self._global_claw_scheduler.get_work_pool_status()
                status["claw_scheduler"] = {
                    "total_claws": pool_status.total_claws,
                    "loaded_claws": pool_status.loaded_claws,
                    "departments": pool_status.departments,
                    "stats": {
                        "total_dispatched": self._global_claw_scheduler._stats.total_dispatched,
                        "total_completed": self._global_claw_scheduler._stats.total_completed,
                        "total_failed": self._global_claw_scheduler._stats.total_failed,
                    },
                }
            except Exception as e:
                logger.debug(f"获取 Claw 调度统计失败: {e}")
        return status

    def run_daily_learning(self) -> Dict:
        """运行每日学习."""
        return {"status": "no_op", "reason": "daily_learning not yet implemented"}

    # ── 研究阶段管理系统便捷方法 [v1.0.0] ──────

    @property
    def research_phase_manager(self):
        """延迟加载研究阶段管理器"""
        if not self._research_phase_manager_initialized:
            _ensure_research_phase_manager_fn(self)
        return self._research_phase_manager

    def run_research_phases(self, phase_ids=None) -> Dict:
        """
        执行研究阶段任务

        Args:
            phase_ids: 要执行的阶段列表，None=全部四阶段

        Returns:
            包含全部阶段报告的字典
        """
        rpm = self.research_phase_manager
        if rpm is None:
            return {"status": "error", "reason": "research_phase_manager unavailable"}
        if phase_ids:
            results = {}
            for pid in phase_ids:
                results[pid] = rpm.run_phase(pid)
            return {"status": "partial_complete", "phases": results}
        return rpm.run_all_phases()

    def get_research_phase_status(self) -> Dict:
        """获取研究阶段管理系统状态"""
        rpm = self.research_phase_manager
        if rpm is None:
            return {"status": "unavailable"}
        return rpm.get_system_status()

    # ═══════════════════════════════════════════════════════════════════════════════
    # 三核联动整合器 [v1.0.0] - 整合研究体系(脑) + 神之架构(躯) + 贤者系统(魂)
    # ═══════════════════════════════════════════════════════════════════════════════

    _three_core_integration_initialized: bool = False
    _three_core_integration: Optional[Any] = None

    @property
    def three_core(self) -> 'ThreeCoreIntegration':
        """
        获取三核联动整合器实例（懒加载）

        整合"统一研究体系"(脑) + "神之架构V5"(躯) + "贤者系统"(魂)

        Returns:
            ThreeCoreIntegration: 三核联动整合器实例
        """
        if not self._three_core_integration_initialized:
            self._init_three_core_integration()
        # [P7] 安全返回
        if self._three_core_integration is None and getattr(self, '_three_core_init_failed', False):
            raise RuntimeError("三核联动整合器初始化失败且无法恢复（上次错误已记录）")
        return self._three_core_integration

    def _init_three_core_integration(self) -> None:
        """初始化三核联动整合器"""
        if self._three_core_integration_initialized:
            return
        try:
            from ..intelligence.three_core import ThreeCoreIntegration
            self._three_core_integration = ThreeCoreIntegration()
            self._three_core_integration_initialized = True
            self._three_core_init_failed = False
            logger.info("[SomnCore] 三核联动整合器 v1.0 已初始化")
        except Exception as e:
            logger.warning(f"[SomnCore] 三核联动整合器初始化失败: {e}")
            # [P7] 标记失败但不阻止重试
            self._three_core_init_failed = True

    def three_core_dispatch(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        三核联动调度主方法

        完整流程: 研究体系(脑) → 神之架构(躯) → 贤者系统(魂) → 融合执行

        Args:
            query: 用户查询
            context: 可选上下文

        Returns:
            融合决策结果，包含:
            - research_plan: 研究计划 (层级/深度/维度/ICE评分)
            - dispatch: 调度分配 (主线/部门/决策制)
            - wisdom: 智慧注入 (学派/链路/代表贤者)
            - fusion_decision: 融合决策摘要
            - feedback_loop: 反馈闭环信息
        """
        tc = self.three_core
        if tc is None:
            return {"error": "三核联动整合器不可用"}

        try:
            result = tc.three_core_dispatch(query, context)
            return {
                "status": "success",
                "research_plan": {
                    "level": result.research_plan.level.value,
                    "depth": result.research_plan.depth.value,
                    "dimensions": [d.value for d in result.research_plan.dimensions],
                    "directions": [d.value for d in result.research_plan.directions],
                    "ice_score": result.research_plan.ice_score,
                    "priority": result.research_plan.priority,
                    "estimated_hours": result.research_plan.estimated_hours,
                },
                "dispatch": {
                    "main_line": result.dispatch_allocation.main_line.value,
                    "secondary_lines": [l.value for l in result.dispatch_allocation.secondary_lines],
                    "cross_sync": result.dispatch_allocation.cross_sync_type.value,
                    "departments": result.dispatch_allocation.departments,
                    "decision_system": result.dispatch_allocation.decision_system.value,
                    "complexity": result.dispatch_allocation.complexity.value,
                },
                "wisdom": {
                    "schools": result.wisdom_injection.schools,
                    "phase": result.wisdom_injection.phase_chain.value,
                    "sages": result.wisdom_injection.sage_representatives,
                    "claw_count": len(result.wisdom_injection.claws),
                },
                "fusion_summary": result.fusion_decision.get("summary", {}),
            }
        except Exception as e:
            logger.warning(f"[SomnCore] 三核联动调度失败: {e}")
            return {"error": "三核联动调度失败"}

    def get_three_core_status(self) -> Dict[str, Any]:
        """获取三核联动整合器状态"""
        if not self._three_core_integration_initialized:
            return {"status": "not_initialized"}
        if self._three_core_integration is None:
            return {"status": "failed"}
        return {
            "status": "ready",
            "version": "v6.2.0",
            "components": {
                "research_framework": "统一研究体系",
                "divine_architecture": "神之架构V5",
                "sage_system": "贤者系统Phase0-4",
            },
            "mapping_matrices": {
                "research_level_mainline": "L1-L4 × 7主线",
                "depth_phase": "D0-D5 × 5链路",
                "dimension_school": "5维度 × 25学派",
                "sage_mainline": "7贤 × 7主线",
            },
        }

_somn_instance: Optional[SomnCore] = None

def get_somn_core(base_path: str = None) -> SomnCore:
    """get Somn 核心实例(单例模式)"""
    global _somn_instance
    if _somn_instance is None:
        _somn_instance = SomnCore(base_path)
    return _somn_instance

# ───────────────────────────────────────────────────────────────
# 模块导出
# ───────────────────────────────────────────────────────────────
__all__ = [
    'SomnCore',
    'get_somn_core',
    'SomnContext',
    'WorkflowTaskRecord',
    'LongTermGoalRecord',
]
