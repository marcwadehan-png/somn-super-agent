"""
__all__ = [
    'apply_reinforcement_inputs',
    'get_trigger',
    'resolve_reinforcement_action',
    'score_to_rating_value',
    'task_outcome_anchor',
]

强化学习器 - 提供强化学习信号处理能力
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ReinforcementLearner:
    """强化学习器封装类"""

    def __init__(self, trigger=None):
        self._trigger = trigger

    def get_trigger(self):
        """获取底层触发器"""
        return self._trigger

    def apply_reinforcement_inputs(self, feedback_entries: List[Dict[str, Any]]):
        """把反馈管道路由出的奖励信号写入强化学习 Q 表"""
        if not self._trigger or not feedback_entries:
            return
        try:
            for entry in feedback_entries:
                self._trigger.process_feedback(entry)
        except Exception as e:
            logger.warning(f"应用强化输入失败: {e}")

    @staticmethod
    def resolve_reinforcement_action(record: Any) -> str:
        """把执行记录映射为可复用的强化学习动作标识"""
        if record is None:
            return "unknown"
        tool = getattr(record, 'tool', None)
        task_name = getattr(record, 'task_name', 'unknown')
        if tool:
            return f"{tool}:{task_name}"
        elif task_name:
            return task_name
        return "default_action"

    @staticmethod
    def score_to_rating_value(score: float) -> int:
        """把 0~1 分数折算为 1~5 评分"""
        if score >= 0.9: return 5
        elif score >= 0.7: return 4
        elif score >= 0.5: return 3
        elif score >= 0.3: return 2
        return 1

    @staticmethod
    def task_outcome_anchor(status: str) -> str:
        """把任务状态映射为评估反馈的基准锚点"""
        status_lower = str(status or '').lower()
        return {
            "completed": "anchor_success",
            "failed": "anchor_failure",
            "blocked": "anchor_blocked",
            "pending": "anchor_pending",
        }.get(status_lower, "anchor_unknown")
