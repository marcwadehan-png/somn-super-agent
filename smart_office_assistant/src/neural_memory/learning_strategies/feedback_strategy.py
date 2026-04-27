"""
__all__ = [
    'execute',
    'get_description',
    'should_execute',
    'strategy_type',
]

反馈闭环学习策略 - Feedback Loop Learning Strategy
从 daily_learning.py 的闭环逻辑中独立提取：
- 仅执行反馈整合 + 迁移学习（不包含实例/验证/错误/关联学习）
- 适合高频轻量调度，与 DailyLearningStrategy 互补
"""

from __future__ import annotations

from typing import Any, Dict

from .base_strategy import (
    BaseLearningStrategy,
    DataScanResult,
    LearningResult,
    LearningStrategyType,
)
from .daily_strategy import DailyLearningStrategy

class FeedbackLoopStrategy(BaseLearningStrategy):
    """
    反馈闭环学习策略。

    差异化能力：
    - 仅执行强化学习闭环（FeedbackPipeline → ROITracker → ReinforcementTrigger）
    - 仅执行迁移学习（TransferLearner）
    - 不执行实例/验证/错误/关联学习（轻量快速）
    """

    @property
    def strategy_type(self) -> LearningStrategyType:
        return LearningStrategyType.FEEDBACK

    def get_description(self) -> str:
        return "反馈闭环策略：强化学习 Q 值更新 + 迁移知识注册（轻量调度）"

    def should_execute(self, scan_result: DataScanResult) -> bool:
        """反馈策略不依赖扫描数据"""
        return True

    def execute(self, scan_result: DataScanResult, context: Dict[str, Any]) -> LearningResult:
        import time
        t0 = time.time()
        result = LearningResult(strategy_type=self.strategy_type.value)

        # 复用 DailyLearningStrategy 的闭环方法
        _daily = DailyLearningStrategy(self.base_path)
        _daily._execute_feedback_integration(result)
        result.phases_completed.append("反馈整合")

        _daily._execute_transfer_learning(result)
        result.phases_completed.append("迁移学习")

        result.duration_seconds = round(time.time() - t0, 2)
        result.summary = (
            f"反馈闭环完成：RL 更新 {len(result.rl_updates)} 条，"
            f"迁移假设 {len(result.transfer_hypotheses)} 个，"
            f"注册知识 {len(result.registered_knowledge)} 条。"
        )
        return result
