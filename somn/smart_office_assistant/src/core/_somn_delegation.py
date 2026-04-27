"""
__all__ = [
    'delegate_apply_reinforcement_inputs',
    'delegate_build_evaluation_feedback_entries',
    'delegate_build_roi_signal_snapshot',
    'delegate_build_workflow_feedback_entries',
    'delegate_check_search_cache',
    'delegate_clamp_unit_score',
    'delegate_ensure_autonomy_stores',
    'delegate_estimate_task_quality_score',
    'delegate_evict_stale_search_cache',
    'delegate_execute_rollback',
    'delegate_execute_task',
    'delegate_extract_json_payload',
    'delegate_extract_keywords',
    'delegate_extract_similarity_terms',
    'delegate_extract_strategy_combo',
    'delegate_generate_autonomy_reflection',
    'delegate_jaccard_similarity',
    'delegate_make_goal_id',
    'delegate_normalize_for_cache',
    'delegate_normalize_roi_ratio',
    'delegate_put_search_cache',
    'delegate_read_json_store',
    'delegate_resolve_estimated_minutes',
    'delegate_resolve_reinforcement_action',
    'delegate_roi_trend_bias',
    'delegate_safe_future_result',
    'delegate_safe_industry_type',
    'delegate_score_to_rating_value',
    'delegate_serialize_feedback_item',
    'delegate_serialize_reinforcement_updates',
    'delegate_serialize_task_record',
    'delegate_store_autonomy_learning',
    'delegate_submit_feedback_entries',
    'delegate_task_outcome_anchor',
    'delegate_track_roi_task_completion',
    'delegate_track_roi_task_start',
    'delegate_track_roi_workflow_completion',
    'delegate_write_json_store',
]

SomnCore 完全委托模块
批量处理所有简单的单行委托方法
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .somn_core import SomnCore, WorkflowTaskRecord

# ==================== 执行API委托 ====================

def delegate_normalize_for_cache(text: str) -> str:
    """标准化文本用于缓存 key 生成 -- 委托自 _somn_execution_api."""
    from ._somn_execution_api import module_normalize_for_cache
    return module_normalize_for_cache(text)

def delegate_jaccard_similarity(set_a: set, set_b: set) -> float:
    """计算两个集合的 Jaccard 相似度 -- 委托自 _somn_execution_api."""
    from ._somn_execution_api import module_jaccard_similarity
    return module_jaccard_similarity(set_a, set_b)

def delegate_safe_future_result(future, timeout: float, fallback: Any, label: str = "") -> Any:
    """安全地从 Future 取结果 -- 委托自 _somn_execution_api."""
    from ._somn_execution_api import module_safe_future_result
    return module_safe_future_result(future, timeout, fallback, label)

def delegate_serialize_task_record(core, record: "WorkflowTaskRecord") -> Dict[str, Any]:
    """输出可持久化的任务状态 -- 委托自 _somn_execution_api."""
    from ._somn_execution_api import _module_serialize_task_record
    return _module_serialize_task_record(core, record)

def delegate_execute_rollback(core, record: "WorkflowTaskRecord", state_history: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """执行失败后的回滚任务 -- 委托自 _somn_execution_api."""
    from ._somn_execution_api import _module_execute_rollback
    return _module_execute_rollback(core, record, state_history)

def delegate_execute_task(core, task: Dict[str, Any]) -> Dict[str, Any]:
    """执行单个任务 -- 委托自 _somn_execution_api."""
    from ._somn_execution_api import _module_execute_task
    return _module_execute_task(core, task)

# ==================== ROI API委托 ====================

def delegate_extract_strategy_combo(task_entries: List[Any]) -> List[str]:
    """从任务记录中提取本次工作流实际使用的strategy组合 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_extract_strategy_combo
    return _module_extract_strategy_combo(task_entries)

def delegate_resolve_reinforcement_action(record: Any) -> str:
    """把执行记录或任务结果mapping为可复用的强化学习动作标识 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_resolve_reinforcement_action
    return _module_resolve_reinforcement_action(record)

def delegate_clamp_unit_score(value: Any, default: float = 0.0) -> float:
    """把分值限制在 0~1,避免异常评估污染反馈 -- 委托自 _somn_feedback."""
    from ._somn_feedback import _clamp_unit_score as _module_clamp_unit_score
    return _module_clamp_unit_score(value, default)

def delegate_resolve_estimated_minutes(core, record: Any, execution_config: Dict[str, Any]) -> float:
    """尽量从任务参数或执行配置中推断 ROI 所需的预估耗时 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_resolve_estimated_minutes
    return _module_resolve_estimated_minutes(core, record, execution_config)

def delegate_track_roi_task_start(core, workflow_task_id: str, record: "WorkflowTaskRecord", execution_config: Dict[str, Any]) -> None:
    """在任务真正开跑时，把 ROI 投入侧也一起记账 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_track_roi_task_start
    _module_track_roi_task_start(core, workflow_task_id, record, execution_config)

def delegate_estimate_task_quality_score(core, record: Any) -> float:
    """把执行记录粗折算为 ROI 可消费的质量分 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_estimate_task_quality_score
    return _module_estimate_task_quality_score(core, record)

def delegate_track_roi_task_completion(core, workflow_task_id: str, record: "WorkflowTaskRecord") -> Optional[str]:
    """在任务收束时把效率/收益结果写入 ROITracker -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_track_roi_task_completion
    return _module_track_roi_task_completion(core, workflow_task_id, record)

def delegate_track_roi_workflow_completion(core, workflow_task_id: str, task_records: List["WorkflowTaskRecord"], execution_report: Dict[str, Any]) -> Dict[str, Any]:
    """在工作流收束时，把任务级 ROI 向上聚合到 workflow / strategy_combo -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_track_roi_workflow_completion
    return _module_track_roi_workflow_completion(core, workflow_task_id, task_records, execution_report)

def delegate_normalize_roi_ratio(core, value: Any, default: float = 0.5) -> float:
    """把 ROI ratio 平滑压到 0~1 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_normalize_roi_ratio
    return _module_normalize_roi_ratio(core, value, default)

def delegate_roi_trend_bias(core, trend: Any) -> float:
    """给 ROI 趋势一个小幅偏置 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_roi_trend_bias
    return _module_roi_trend_bias(core, trend)

def delegate_build_roi_signal_snapshot(core, execution_report: Dict[str, Any]) -> Dict[str, Any]:
    """把 ROITracker 里的效率/收益数据整理成评估层可直接消费的结构 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_build_roi_signal_snapshot
    return _module_build_roi_signal_snapshot(core, execution_report)

def delegate_score_to_rating_value(core, score: float) -> float:
    """把 0~1 分数折算为 feedback_pipeline 可消费的 1~5 评分 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_score_to_rating_value
    return _module_score_to_rating_value(core, score)

def delegate_task_outcome_anchor(core, task_status: str) -> float:
    """把任务状态mapping为评估反馈的基准锚点 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_task_outcome_anchor
    return _module_task_outcome_anchor(core, task_status)

def delegate_serialize_feedback_item(core, feedback: Any) -> Dict[str, Any]:
    """把反馈对象转成可落盘/可回传结构 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_serialize_feedback_item
    return _module_serialize_feedback_item(core, feedback)

def delegate_serialize_reinforcement_updates(updates: List[Any]) -> List[Dict[str, Any]]:
    """把强化更新序列化为可记录结构 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_serialize_reinforcement_updates
    return _module_serialize_reinforcement_updates(updates)

def delegate_build_workflow_feedback_entries(core, workflow_task_id: str, task_records: List["WorkflowTaskRecord"]) -> List[Dict[str, Any]]:
    """把任务执行状态翻译成反馈管道可消费的原始反馈 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_build_workflow_feedback_entries
    return _module_build_workflow_feedback_entries(core, workflow_task_id, task_records)

def delegate_build_evaluation_feedback_entries(core, execution_report: Dict[str, Any], evaluation_report: Dict[str, Any]):
    """把效果评估结果折算成可学习反馈 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_build_evaluation_feedback_entries
    return _module_build_evaluation_feedback_entries(core, execution_report, evaluation_report)

def delegate_apply_reinforcement_inputs(core, rl_inputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """把反馈管道路由出的奖励信号写入强化学习 Q 表 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_apply_reinforcement_inputs
    return _module_apply_reinforcement_inputs(core, rl_inputs)

def delegate_submit_feedback_entries(core, raw_feedbacks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """提交一批反馈到 FeedbackPipeline,并继续路由到强化学习 -- 委托自 _somn_roi_api."""
    from ._somn_roi_api import _module_submit_feedback_entries
    return _module_submit_feedback_entries(core, raw_feedbacks)

# ==================== Helpers委托 ====================

def delegate_safe_industry_type(industry) -> Optional[Any]:
    """安全转换行业枚举 -- 委托自 _somn_helpers."""
    from ._somn_execution_api import module_safe_industry_type
    return module_safe_industry_type(industry)

def delegate_extract_keywords(text: str) -> List[str]:
    """提取关键词 -- 委托自 _somn_helpers."""
    from ._somn_execution_api import module_extract_keywords
    return module_extract_keywords(text)

# ==================== 语义API委托 ====================

def delegate_check_search_cache(core, description: str) -> Optional[List[Dict[str, Any]]]:
    """查询搜索缓存 -- 委托自 _somn_semantic_api."""
    from ._somn_semantic_api import _module_check_search_cache
    return _module_check_search_cache(core, description)

def delegate_put_search_cache(core, description: str, results: List[Dict[str, Any]]) -> None:
    """写入搜索缓存 -- 委托自 _somn_semantic_api."""
    from ._somn_semantic_api import _module_put_search_cache
    _module_put_search_cache(core, description, results)

def delegate_evict_stale_search_cache(core) -> None:
    """清理过期缓存条目 -- 委托自 _somn_semantic_api."""
    from ._somn_semantic_api import _module_evict_stale_search_cache
    _module_evict_stale_search_cache(core)

# ==================== 自主API委托 ====================

def delegate_ensure_autonomy_stores(core):
    """确保自治闭环所需的本地存储存在 -- 委托自 _somn_autonomy_api."""
    from ._somn_autonomy_api import _module_ensure_autonomy_stores
    return _module_ensure_autonomy_stores(core)

def delegate_read_json_store(core, file_path, default):
    """读取本地 JSON 存储 -- 委托自 _somn_autonomy_api."""
    from ._somn_autonomy_api import _module_read_json_store
    return _module_read_json_store(core, file_path, default)

def delegate_write_json_store(core, file_path, data):
    """写入本地 JSON 存储 -- 委托自 _somn_autonomy_api."""
    from ._somn_autonomy_api import _module_write_json_store
    return _module_write_json_store(core, file_path, data)

def delegate_extract_similarity_terms(core, text: str) -> List[str]:
    """提取用于经验召回的关键词 -- 委托自 _somn_autonomy_api."""
    from ._somn_autonomy_api import _module_extract_similarity_terms
    return _module_extract_similarity_terms(core, text)

def delegate_make_goal_id(core, objective: str) -> str:
    """基于目标文本生成稳定 goal_id -- 委托自 _somn_autonomy_api."""
    from ._somn_autonomy_api import _module_make_goal_id
    return _module_make_goal_id(core, objective)

def delegate_generate_autonomy_reflection(core, requirement, execution, evaluation):
    """任务完成后自动形成自治复盘 -- 委托自 _somn_autonomy_api."""
    from ._somn_autonomy_api import _module_generate_autonomy_reflection
    return _module_generate_autonomy_reflection(core, requirement, execution, evaluation)

def delegate_store_autonomy_learning(core, requirement, strategy, execution, evaluation, reflection, current_goal):
    """写回长期目标、经验库和任务复盘 -- 委托自 _somn_autonomy_api."""
    from ._somn_autonomy_api import _module_store_autonomy_learning
    return _module_store_autonomy_learning(core, requirement, strategy, execution, evaluation, reflection, current_goal)

# ==================== Context API委托 ====================

def delegate_extract_json_payload(text: str) -> Any:
    """从模型文本中提取 JSON -- 委托自 _somn_context_api."""
    from ._somn_context_api import _module_extract_json_payload
    return _module_extract_json_payload(text)
