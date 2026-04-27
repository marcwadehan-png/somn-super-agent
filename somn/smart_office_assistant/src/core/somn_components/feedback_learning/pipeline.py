"""
__all__ = [
    'build_workflow_feedback_entries',
    'get_pipeline',
    'record_user_feedback',
    'serialize_feedback_item',
    'submit_entries',
]

反馈管道 - 提供反馈收集和处理能力
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class FeedbackPipeline:
    """反馈管道封装类"""

    def __init__(self, pipeline=None):
        """
        Args:
            pipeline: 底层反馈管道
        """
        self._pipeline = pipeline

    def get_pipeline(self):
        """获取底层管道"""
        return self._pipeline

    def submit_entries(
        self,
        feedback_entries: List[Dict[str, Any]],
        apply_func=None
    ) -> Dict[str, Any]:
        """
        提交反馈条目到管道

        Args:
            feedback_entries: 反馈条目列表
            apply_func: 应用强化的函数

        Returns:
            提交结果
        """
        if not self._pipeline or not feedback_entries:
            return {"status": "skipped", "reason": "no_pipeline_or_entries"}

        try:
            for entry in feedback_entries:
                self._pipeline.record(entry)

            if apply_func:
                apply_func(feedback_entries)

            return {"status": "success", "count": len(feedback_entries)}
        except Exception as e:
            logger.warning(f"提交反馈失败: {e}")
            return {"status": "error", "reason": "提交反馈失败"}

    def build_workflow_feedback_entries(
        self,
        task_records: List[Any],
        quality_score_func=None
    ) -> List[Dict[str, Any]]:
        """
        把任务执行状态翻译成反馈管道可消费的原始反馈

        Args:
            task_records: 任务记录列表
            quality_score_func: 质量评分函数

        Returns:
            反馈条目列表
        """
        entries = []
        for record in task_records:
            status = getattr(record, 'status', '') or ''
            quality = quality_score_func(record) if quality_score_func else 0.5

            entry = {
                "type": "workflow_execution",
                "task_name": getattr(record, 'task_name', 'unknown'),
                "tool": getattr(record, 'tool', 'unknown'),
                "status": status,
                "quality_score": quality,
                "attempts": getattr(record, 'attempts', 0) or 0,
                "error": getattr(record, 'last_error', None),
            }
            entries.append(entry)

        return entries

    def serialize_feedback_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        把反馈对象转成可落盘/可回传结构

        Args:
            item: 反馈条目

        Returns:
            序列化后的反馈
        """
        return {
            "type": item.get("type", "unknown"),
            "task_name": item.get("task_name", "unknown"),
            "quality_score": item.get("quality_score", 0.5),
            "status": item.get("status", ""),
            "timestamp": item.get("timestamp", ""),
        }

    def record_user_feedback(
        self,
        task_id: str,
        user_id: str,
        rating: int,
        comment: str = "",
        adopted: bool = True
    ) -> bool:
        """
        记录用户显式反馈

        Args:
            task_id: 任务ID
            user_id: 用户ID
            rating: 评分 1-5
            comment: 评价
            adopted: 是否采纳

        Returns:
            是否成功
        """
        if not self._pipeline:
            return False

        try:
            entry = {
                "type": "user_feedback",
                "task_id": task_id,
                "user_id": user_id,
                "rating": rating,
                "comment": comment,
                "adopted": adopted,
            }
            self._pipeline.record(entry)
            return True
        except Exception as e:
            logger.warning(f"记录用户反馈失败: {e}")
            return False
