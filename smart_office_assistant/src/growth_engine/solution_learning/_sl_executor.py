"""每日学习执行器"""

from pathlib import Path
from typing import Dict

from src.core.paths import SOLUTION_LEARNING_DIR
from ._sl_v1_engine import SolutionLearningEngine

__all__ = [
    'execute_daily_learning',
]

class DailyLearningExecutor:
    """每日学习执行器"""

    def __init__(self):
        self.base_path = Path(SOLUTION_LEARNING_DIR)
        self.engine = SolutionLearningEngine(str(self.base_path))

    def execute_daily_learning(self) -> Dict:
        """执行每日学习"""
        report = self.engine.daily_learning()
        return self._format_report(report)

    def _format_report(self, report: Dict) -> Dict:
        """格式化报告"""
        summary = report.get("learning_summary", {})
        return {"date": report.get("date"), "sessions_created": len(report.get("sessions_created", [])),
                "insights_generated": len(report.get("insights_generated", [])),
                "templates_updated": len(report.get("templates_updated", [])),
                "categories_processed": report.get("categories_processed", []), "summary": summary}
