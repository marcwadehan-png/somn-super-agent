"""
__all__ = [
    'generate_autonomy_reflection',
    'store_learning',
]

自省引擎 - 提供任务复盘和经验总结能力
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ReflectionEngine:
    """自省引擎封装类"""

    def __init__(self, somn_core=None):
        """
        Args:
            somn_core: SomnCore实例引用
        """
        self._core = somn_core

    def generate_autonomy_reflection(
        self,
        requirement: Dict[str, Any],
        execution_report: Dict[str, Any],
        evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        任务完成后自动形成自治复盘

        Args:
            requirement: 需求分析结果
            execution_report: 执行报告
            evaluation: 评估结果

        Returns:
            复盘结果
        """
        reflections = []

        # 分析执行结果
        exec_summary = execution_report.get("execution_summary", {}) or {}
        completed = exec_summary.get("completed", 0)
        failed = exec_summary.get("failed", 0)
        success_ratio = exec_summary.get("success_ratio", 0.0)

        # 生成反思
        if success_ratio >= 0.8:
            reflections.append({
                "type": "success",
                "insight": f"任务执行良好，成功率 {success_ratio:.1%}",
                "recommendation": "继续保持当前策略"
            })
        elif success_ratio >= 0.5:
            reflections.append({
                "type": "partial",
                "insight": f"部分任务失败，{failed} 个任务未完成",
                "recommendation": "分析失败原因，优化执行策略"
            })
        else:
            reflections.append({
                "type": "needs_review",
                "insight": f"执行效果不佳，需要深入分析",
                "recommendation": "重新评估需求和策略"
            })

        # 分析评估结果
        quality_score = evaluation.get("quality_score", 0)
        if quality_score < 0.5:
            reflections.append({
                "type": "quality",
                "insight": f"质量评分较低 ({quality_score:.2f})",
                "recommendation": "关注输出质量，考虑调整方法"
            })

        return {
            "reflections": reflections,
            "summary": self._summarize_reflections(reflections),
            "timestamp": self._get_timestamp()
        }

    def _summarize_reflections(self, reflections: List[Dict[str, Any]]) -> str:
        """生成复盘摘要"""
        if not reflections:
            return "无明显问题"

        types = [r.get("type", "unknown") for r in reflections]
        if "needs_review" in types:
            return "需要深入复盘"
        elif "partial" in types:
            return "部分达成，可优化"
        else:
            return "执行良好"

    @staticmethod
    def _get_timestamp() -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def store_learning(
        self,
        goal_record: Dict[str, Any],
        execution_report: Dict[str, Any],
        reflection: Dict[str, Any]
    ) -> bool:
        """
        存储学习结果到记忆系统

        Args:
            goal_record: 目标记录
            execution_report: 执行报告
            reflection: 复盘结果

        Returns:
            是否成功
        """
        if not self._core:
            return False

        try:
            if hasattr(self._core, 'neural_system') and self._core.neural_system:
                self._core.neural_system.record(
                    event_type="autonomy_learning",
                    data={
                        "goal": goal_record,
                        "execution": execution_report,
                        "reflection": reflection
                    }
                )
                return True
        except Exception as e:
            logger.warning(f"存储学习结果失败: {e}")

        return False
