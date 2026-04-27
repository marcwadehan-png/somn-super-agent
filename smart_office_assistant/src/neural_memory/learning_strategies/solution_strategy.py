"""
__all__ = [
    'execute',
    'get_description',
    'should_execute',
    'strategy_type',
]

解决方案学习策略 - Solution Learning Strategy
提取自 solution_daily_learning.py 的差异化能力：
- 调用 growth_engine.daily_learning_executor 执行解决方案学习
- 生成带元数据的 YAML 报告（SOLUTION_LEARNING_DIR）
- 将学习摘要写入工作记忆日志（data/daily_memory/*.md）[v2.0 独立运行版]
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

import yaml

from .base_strategy import (
    BaseLearningStrategy,
    DataScanResult,
    LearningResult,
    LearningStrategyType,
)

class SolutionLearningStrategy(BaseLearningStrategy):
    """
    解决方案每日学习策略。

    差异化能力（仅此策略独有）：
    1. 调用 growth_engine.daily_learning_executor 执行服务商方案学习
    2. 生成带 report_metadata 的 YAML 报告
    3. 将摘要追加写入 data/daily_memory/<date>.md 工作记忆日志 [v2.0 独立运行版]
    """

    @property
    def strategy_type(self) -> LearningStrategyType:
        return LearningStrategyType.SOLUTION

    def get_description(self) -> str:
        return "解决方案学习策略：growth_engine 服务商学习 + YAML 报告 + 工作记忆写入"

    def should_execute(self, scan_result: DataScanResult) -> bool:
        """解决方案学习不依赖扫描数据，始终可执行"""
        return True

    def execute(self, scan_result: DataScanResult, context: Dict[str, Any]) -> LearningResult:
        import time
        t0 = time.time()
        result = LearningResult(strategy_type=self.strategy_type.value)

        # 1. 调用 growth_engine 执行每日学习
        raw_report: Dict = {}
        try:
            from growth_engine import daily_learning_executor
            raw_report = daily_learning_executor.execute_daily_learning()
            result.phases_completed.append("growth_engine学习")
            logger.info("解决方案学习执行完成")
        except Exception as e:
            result.error_messages.append(f"growth_engine学习失败: {e}")
            logger.warning(f"growth_engine学习失败: {e}")

        # 2. 生成 YAML 报告
        if raw_report:
            try:
                report_path = self._generate_yaml_report(raw_report)
                result.extra["yaml_report"] = str(report_path)
                result.phases_completed.append("YAML报告生成")
                logger.info(f"详细报告已保存: {report_path}")
            except Exception as e:
                logger.warning(f"YAML报告保存失败: {e}")

        # 3. 写入工作记忆日志
        if raw_report:
            try:
                memory_file = self._update_neural_memory(raw_report)
                result.extra["memory_file"] = str(memory_file)
                result.phases_completed.append("工作记忆写入")
                logger.info(f"神经记忆已更新: {memory_file}")
            except Exception as e:
                logger.warning(f"工作记忆更新失败: {e}")

        # 4. 汇总结果
        result.duration_seconds = round(time.time() - t0, 2)
        result.extra["raw_report"] = raw_report
        result.summary = self._build_summary(raw_report)
        return result

    # ─────────────────────────────────────────────────
    # 差异化：YAML 报告生成
    # ─────────────────────────────────────────────────

    def _generate_yaml_report(self, report: Dict) -> Path:
        """生成带元数据的 YAML 报告"""
        try:
            from src.core.paths import SOLUTION_LEARNING_DIR
            report_dir = Path(SOLUTION_LEARNING_DIR) / "reports"
        except ImportError:
            report_dir = Path(self.base_path or ".") / "solution_learning" / "reports"

        report_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y%m%d")
        report_file = report_dir / f"daily_report_{date_str}.yaml"

        report_copy = dict(report)
        report_copy["report_metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "report_type": "daily_learning",
            "system_version": "v2.2.0",
            "engine": "SolutionLearningEngine",
        }
        with open(report_file, "w", encoding="utf-8") as f:
            yaml.dump(report_copy, f, allow_unicode=True, default_flow_style=False)
        return report_file

    # ─────────────────────────────────────────────────
    # 差异化：写入工作记忆日志
    # ─────────────────────────────────────────────────

    def _update_neural_memory(self, report: Dict) -> Path:
        """将学习摘要追加写入 data/daily_memory/<date>.md [v2.0 独立运行版]"""
        # 定位项目根
        try:
            from src.core.paths import DAILY_MEMORY_DIR
            memory_dir = Path(DAILY_MEMORY_DIR)
        except ImportError:
            # 回退逻辑：使用传统路径
            try:
                from src.core.paths import PROJECT_ROOT
                root = Path(PROJECT_ROOT)
            except ImportError:
                root = Path(self.base_path or ".").resolve()
                while root.parent != root and not (root / "data").exists():
                    root = root.parent
            memory_dir = root / "data" / "daily_memory"

        memory_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        memory_file = memory_dir / f"{date_str}.md"

        def _count(v):
            if isinstance(v, int):
                return v
            if isinstance(v, (list, dict)):
                return len(v)
            return 0

        learning_log = (
            f"\n\n## 解决方案智能学习 ({datetime.now().strftime('%H:%M')})\n\n"
            f"**学习范围**: {', '.join(report.get('categories_processed', []))}\n"
            f"**学习成果**:\n"
            f"- 学习会话: {_count(report.get('sessions_created', 0))} 个\n"
            f"- 生成洞察: {_count(report.get('insights_generated', 0))} 个\n"
            f"- 更新模板: {_count(report.get('templates_updated', 0))} 个\n\n"
            f"**学习摘要**:\n"
            f"{yaml.dump(report.get('learning_summary', {}), allow_unicode=True, default_flow_style=False)}\n"
        )

        with open(memory_file, "a", encoding="utf-8") as f:
            f.write(learning_log)
        return memory_file

    # ─────────────────────────────────────────────────
    # 辅助
    # ─────────────────────────────────────────────────

    @staticmethod
    def _build_summary(report: Dict) -> str:
        if not report:
            return "解决方案学习：未获取到报告数据。"

        def _count(v):
            if isinstance(v, int):
                return v
            if isinstance(v, (list, dict)):
                return len(v)
            return 0

        return (
            f"解决方案学习完成："
            f"学习会话 {_count(report.get('sessions_created', 0))} 个，"
            f"生成洞察 {_count(report.get('insights_generated', 0))} 个，"
            f"更新模板 {_count(report.get('templates_updated', 0))} 个。"
        )
