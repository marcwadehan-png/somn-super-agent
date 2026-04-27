"""全局实例"""

from pathlib import Path

from ._sl_v1_engine import SolutionLearningEngine
from ._sl_executor import DailyLearningExecutor

# 全局实例
solution_learning_engine = SolutionLearningEngine(str(Path(__file__).parent.parent.parent / "data" / "solution_learning"))
daily_learning_executor = DailyLearningExecutor()
