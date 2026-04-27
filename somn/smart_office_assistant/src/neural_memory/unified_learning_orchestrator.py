"""
__all__ = [
    'execute_daily',
    'execute_strategy',
    'get_execution_log',
    'get_status',
    'plan_and_execute',
    'plan_learning_data_selection',
    'run_integrated_learning',
    'run_unified_learning',
    'scan_data_sources',
    'set_config',
]

统一学习调度器 - Unified Learning Orchestrator
v1.0.0

整合 6 个碎片化学习文件为单一调度核心：
  daily_learning.py           → DailyLearningStrategy
  three_tier_learning.py      → ThreeTierLearningStrategy
  enhanced_three_tier_learning.py → EnhancedLearningStrategy
  integrated_learning.py      → IntegratedLearningMode（计划+执行+报告）
  solution_daily_learning.py  → SolutionLearningStrategy
  learning_scheduler.py       → SchedulerConfig + UnifiedDataScanner

架构：
  UnifiedLearningOrchestrator
    ├── UnifiedDataScanner            （数据扫描，消除重复）
    ├── STRATEGY_REGISTRY             （策略注册表）
    └── _execute_strategy()           （统一执行入口）

单文件行数 ≤ 800。差异化能力全部在 learning_strategies/ 目录。
"""

from __future__ import annotations

import logging
import json
import yaml
from datetime import datetime
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.paths import LEARNING_DIR, PROJECT_ROOT

from .learning_strategies import (
    STRATEGY_REGISTRY,
    BaseLearningStrategy,
    DataScanResult,
    DailyLearningStrategy,
    EnhancedLearningStrategy,
    FeedbackLoopStrategy,
    LearningResult,
    LearningStrategyType,
    SolutionLearningStrategy,
    ThreeTierLearningStrategy,
    UnifiedDataScanner,
)

# ═══════════════════════════════════════════════════════════════
# 调度器配置（整合 learning_scheduler.LearningSchedule）
# ═══════════════════════════════════════════════════════════════

logger = logging.getLogger(__name__)
class SchedulerStrategyMode(Enum):
    LOCAL_ONLY            = "本地只读"
    LOCAL_FIRST           = "本地优先"
    LOCAL_NETWORK_HYBRID  = "混合学习"
    NETWORK_ONLY          = "网络只读"

@dataclass
class SchedulerConfig:
    """调度器配置（合并自 learning_scheduler.LearningSchedule）"""
    strategy_mode: SchedulerStrategyMode = SchedulerStrategyMode.LOCAL_FIRST
    local_threshold: int = 5
    network_supplement_ratio: float = 0.3
    max_local_data: int = 50
    max_network_data: int = 15
    quality_threshold: float = 0.6
    recency_threshold: int = 30

# ═══════════════════════════════════════════════════════════════
# 执行计划（整合 integrated_learning.IntegratedLearningPlan）
# ═══════════════════════════════════════════════════════════════

@dataclass
class LearningPlan:
    """学习计划（整合 integrated_learning.IntegratedLearningPlan）"""
    plan_id: str
    strategy_type: str
    execution_phase: str
    data_summary: Dict
    learning_config: Dict
    expected_outcomes: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

# ═══════════════════════════════════════════════════════════════
# 执行报告
# ═══════════════════════════════════════════════════════════════

@dataclass
class OrchestratorReport:
    """调度器执行报告"""
    report_id: str
    date: str
    execution_time: str
    plan: Optional[LearningPlan]
    strategy_results: Dict[str, Any]  # strategy_type → LearningResult 摘要
    total_learning_events: int
    total_knowledge_updates: int
    total_duration_seconds: float
    summary: str
    recommendations: List[str]
    raw_results: List[LearningResult] = field(default_factory=list)

# ═══════════════════════════════════════════════════════════════
# 主调度器
# ═══════════════════════════════════════════════════════════════

class UnifiedLearningOrchestrator:
    """
    统一学习调度器。

    公共接口：
        execute_daily()                  → 执行每日完整学习（最常用）
        execute_strategy(strategy_type)  → 执行单一策略
        plan_and_execute()               → 计划 → 执行（integrated_learning 兼容）
        set_config(config)               → 更新调度配置
        get_status()                     → 获取系统状态
    """

    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = str(PROJECT_ROOT)
        self.base_path = Path(base_path)
        self.config = self._load_config()
        self.scanner = UnifiedDataScanner(str(self.base_path))
        self._registered_strategies: Dict[LearningStrategyType, BaseLearningStrategy] = {}
        self._reports_path = self.base_path / "unified_learning_reports"
        self._reports_path.mkdir(parents=True, exist_ok=True)
        self._execution_log: List[str] = []

    # ─────────────────────────────────────────────────
    # 公共接口
    # ─────────────────────────────────────────────────

    def execute_daily(
        self,
        strategy_types: Optional[List[LearningStrategyType]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> OrchestratorReport:
        """
        执行每日完整学习流程。

        Args:
            strategy_types: 要执行的策略列表。None → 默认 [DAILY]。
            context: 传给策略的上下文（neural_system、learning_engine 等）。

        Returns:
            OrchestratorReport
        """
        if strategy_types is None:
            strategy_types = [LearningStrategyType.DAILY]
        if context is None:
            context = self._build_default_context()

        start_time = datetime.now()
        self._log(f"开始每日学习流程... 策略: {[s.value for s in strategy_types]}")

        # 数据扫描（网络学习幂等触发）
        self._log("[1/3] 扫描数据...")
        scan_result = self.scanner.scan_with_network(trigger_fetch=True)
        self._log(f"  扫描完成: 总计 {scan_result.total} 条 "
                  f"（本地 {scan_result.local_count}，网络 {scan_result.network_count}）")

        # 执行各策略
        self._log("[2/3] 执行学习策略...")
        raw_results: List[LearningResult] = []
        for stype in strategy_types:
            self._log(f"  → 执行策略: {stype.value}")
            result = self._execute_strategy(stype, scan_result, context)
            raw_results.append(result)
            self._log(f"    完成: {result.summary}")

        # 生成报告
        self._log("[3/3] 生成报告...")
        report = self._build_report(start_time, raw_results, scan_result)
        self._save_report(report)

        total = (datetime.now() - start_time).total_seconds()
        self._log(f"✅ 每日学习完成！耗时: {total:.2f}s")
        return report

    def execute_strategy(
        self,
        strategy_type: LearningStrategyType,
        context: Optional[Dict[str, Any]] = None,
        scan_result: Optional[DataScanResult] = None,
    ) -> LearningResult:
        """执行单一策略。"""
        if context is None:
            context = self._build_default_context()
        if scan_result is None:
            scan_result = self.scanner.scan()
        return self._execute_strategy(strategy_type, scan_result, context)

    def plan_and_execute(
        self,
        strategy_type: LearningStrategyType = LearningStrategyType.DAILY,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        计划 → 执行完整周期（兼容 integrated_learning.execute_full_cycle）。

        Returns:
            {'plan': LearningPlan, 'report': OrchestratorReport, 'success': bool}
        """
        if context is None:
            context = self._build_default_context()

        logger.info("\n" + "=" * 60)
        logger.info("🎯 开始完整学习周期")
        logger.info("=" * 60)

        # 计划阶段
        logger.info("\n[1/2] 学习规划...")
        scan_result = self.scanner.scan()
        plan = self._build_plan(scan_result, strategy_type)
        self._print_plan(plan)

        # 执行阶段
        logger.info("\n[2/2] 执行学习...")
        report = self.execute_daily(
            strategy_types=[strategy_type], context=context
        )

        summary = {
            "plan": asdict(plan),
            "report": asdict(report) if hasattr(report, "__dataclass_fields__") else report,
            "success": report.total_learning_events >= 0,
        }
        self._print_summary(summary, report)
        return summary

    def set_config(self, config: SchedulerConfig):
        """更新调度配置并持久化"""
        self.config = config
        self._save_config(config)
        logger.info(f"✅ 调度配置已更新: {config.strategy_mode.value}")

    def get_status(self) -> Dict[str, Any]:
        """返回系统状态（兼容 learning_scheduler 输出格式）"""
        scan = self.scanner.scan(recent_only=False)
        breakdown = self.scanner.get_data_source_breakdown(scan)
        return {
            "config": {
                "strategy_mode": self.config.strategy_mode.value,
                "local_threshold": self.config.local_threshold,
                "network_supplement_ratio": self.config.network_supplement_ratio,
            },
            "data_sources": breakdown,
            "registered_strategies": [s.value for s in self._registered_strategies],
            "reports_dir": str(self._reports_path),
        }

    def scan_data_sources(self) -> Dict[str, Any]:
        """扫描数据源（兼容 LearningScheduler.scan_data_sources）"""
        scan = self.scanner.scan(recent_only=False)
        return self.scanner.get_data_source_breakdown(scan)

    def plan_learning_data_selection(self) -> Dict[str, Any]:
        """规划数据选择（兼容 LearningScheduler.plan_learning_data_selection）"""
        scan = self.scanner.scan()
        plan = self._build_plan(scan, LearningStrategyType.DAILY)
        return {
            "strategy": self.config.strategy_mode.value,
            "local_data": scan.findings + scan.validations + scan.learning_events,
            "network_data": scan.network_research,
            "total_data": scan.total,
            "data_source_breakdown": self.scanner.get_data_source_breakdown(scan),
            "recommendations": self._get_recommendations(scan),
            "timestamp": datetime.now().isoformat(),
        }

    # ─────────────────────────────────────────────────
    # 策略执行核心
    # ─────────────────────────────────────────────────

    def _execute_strategy(
        self,
        strategy_type: LearningStrategyType,
        scan_result: DataScanResult,
        context: Dict[str, Any],
    ) -> LearningResult:
        strategy = self._get_strategy(strategy_type)
        if not strategy.should_execute(scan_result):
            result = LearningResult(
                success=True,
                strategy_type=strategy_type.value,
                summary=f"策略 {strategy_type.value} 判断无需执行（数据不足）",
            )
            return result
        try:
            return strategy.execute(scan_result, context)
        except Exception as e:
            result = LearningResult(success=False, strategy_type=strategy_type.value)
            result.error_messages.append("执行失败")
            result.summary = f"策略 {strategy_type.value} 执行异常: {e}"
            return result

    def _get_strategy(self, strategy_type: LearningStrategyType) -> BaseLearningStrategy:
        if strategy_type not in self._registered_strategies:
            cls = STRATEGY_REGISTRY.get(strategy_type)
            if cls is None:
                raise ValueError(f"未知策略类型: {strategy_type}")
            self._registered_strategies[strategy_type] = cls(str(self.base_path))
        return self._registered_strategies[strategy_type]

    # ─────────────────────────────────────────────────
    # 计划 & 报告
    # ─────────────────────────────────────────────────

    def _build_plan(
        self, scan_result: DataScanResult, strategy_type: LearningStrategyType
    ) -> LearningPlan:
        local_count = scan_result.local_count
        net_count = scan_result.network_count

        outcomes = []
        if local_count >= 5:
            outcomes.extend(["✅ 完整的实例学习流程", "✅ 新模式提取", "✅ 关联学习"])
        elif local_count >= 3:
            outcomes.extend(["⚠️ 受限的学习流程", "✅ 关联学习"])
        else:
            outcomes.append("ℹ️ 补充性网络学习")
        if net_count > 0:
            outcomes.append("🌐 网络知识补充")

        return LearningPlan(
            plan_id=f"ULP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            strategy_type=strategy_type.value,
            execution_phase="规划完成",
            data_summary=self.scanner.get_data_source_breakdown(scan_result),
            learning_config={
                "strategy_mode": self.config.strategy_mode.value,
                "local_threshold": self.config.local_threshold,
                "quality_threshold": self.config.quality_threshold,
            },
            expected_outcomes=outcomes,
        )

    def _build_report(
        self,
        start_time: datetime,
        raw_results: List[LearningResult],
        scan_result: DataScanResult,
    ) -> OrchestratorReport:
        total_events = sum(r.total_events for r in raw_results)
        total_updates = sum(r.total_knowledge_updates for r in raw_results)
        total_duration = sum(r.duration_seconds for r in raw_results)

        strategy_results = {
            r.strategy_type: {
                "success": r.success,
                "phases": r.phases_completed,
                "events": r.total_events,
                "updates": r.total_knowledge_updates,
                "duration": r.duration_seconds,
                "summary": r.summary,
            }
            for r in raw_results
        }

        recommendations = self._get_recommendations(scan_result)

        return OrchestratorReport(
            report_id=f"ULR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            date=datetime.now().strftime("%Y-%m-%d"),
            execution_time=datetime.now().strftime("%H:%M:%S"),
            plan=None,
            strategy_results=strategy_results,
            total_learning_events=total_events,
            total_knowledge_updates=total_updates,
            total_duration_seconds=total_duration,
            summary=self._build_summary(raw_results, scan_result),
            recommendations=recommendations,
            raw_results=raw_results,
        )

    def _build_summary(
        self, raw_results: List[LearningResult], scan_result: DataScanResult
    ) -> str:
        parts = [f"数据: 本地 {scan_result.local_count} + 网络 {scan_result.network_count}。"]
        for r in raw_results:
            parts.append(f"[{r.strategy_type}] {r.summary}")
        return " ".join(parts)

    def _get_recommendations(self, scan_result: DataScanResult) -> List[str]:
        recs = []
        if scan_result.local_count < self.config.local_threshold:
            recs.append(f"本地数据不足 {self.config.local_threshold} 条，建议录入更多实例")
        if scan_result.network_count == 0:
            recs.append("未检测到网络研究数据，建议执行浏览器网络学习")
        if len(scan_result.errors) > 3:
            recs.append(f"错误案例较多 ({len(scan_result.errors)})，建议审查验证流程")
        if not recs:
            recs.append("系统运行正常，继续保持数据录入")
        return recs

    def _save_report(self, report: OrchestratorReport):
        report_dict = {
            "report_id": report.report_id,
            "date": report.date,
            "execution_time": report.execution_time,
            "strategy_results": report.strategy_results,
            "total_learning_events": report.total_learning_events,
            "total_knowledge_updates": report.total_knowledge_updates,
            "total_duration_seconds": report.total_duration_seconds,
            "summary": report.summary,
            "recommendations": report.recommendations,
        }
        yaml_path = self._reports_path / f"{report.report_id}.yaml"
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(report_dict, f, allow_unicode=True, default_flow_style=False)
        json_path = self._reports_path / f"{report.report_id}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)

    # ─────────────────────────────────────────────────
    # 上下文 & 配置
    # ─────────────────────────────────────────────────

    def _build_default_context(self) -> Dict[str, Any]:
        """构建默认上下文（尝试加载 neural_system）"""
        ctx: Dict[str, Any] = {}
        try:
            from .neural_system import create_neural_system
            neural_system = create_neural_system(str(self.base_path))
            ctx["neural_system"] = neural_system
            ctx["learning_engine"] = neural_system.learning
        except Exception as e:
            logger.debug(f"加载编排器状态失败: {e}")
        return ctx

    def _load_config(self) -> SchedulerConfig:
        config_path = self.base_path / "learning_schedule.yaml"
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                return SchedulerConfig(
                    strategy_mode=SchedulerStrategyMode[
                        data.get("strategy", "LOCAL_FIRST")
                    ],
                    local_threshold=data.get("local_threshold", 5),
                    network_supplement_ratio=data.get("network_supplement_ratio", 0.3),
                    max_local_data=data.get("max_local_data", 50),
                    max_network_data=data.get("max_network_data", 15),
                    quality_threshold=data.get("quality_threshold", 0.6),
                    recency_threshold=data.get("recency_threshold", 30),
                )
            except Exception as e:
                logger.error(f"⚠️ 加载调度配置失败: {e}，使用默认配置")
        return SchedulerConfig()

    def _save_config(self, config: SchedulerConfig):
        config_path = self.base_path / "learning_schedule.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump({
                "strategy": config.strategy_mode.name,
                "local_threshold": config.local_threshold,
                "network_supplement_ratio": config.network_supplement_ratio,
                "max_local_data": config.max_local_data,
                "max_network_data": config.max_network_data,
                "quality_threshold": config.quality_threshold,
                "recency_threshold": config.recency_threshold,
                "last_updated": datetime.now().isoformat(),
            }, f, allow_unicode=True, default_flow_style=False)

    # ─────────────────────────────────────────────────
    # 打印辅助
    # ─────────────────────────────────────────────────

    def _print_plan(self, plan: LearningPlan):
        logger.info(f"\n   计划ID: {plan.plan_id}")
        logger.info(f"   策略: {plan.strategy_type}")
        logger.info(f"   数据分布: {plan.data_summary}")
        logger.info(f"   预期成果: {len(plan.expected_outcomes)} 项")
        for o in plan.expected_outcomes:
            logger.info(f"     {o}")

    def _print_summary(self, summary: Dict, report: OrchestratorReport):
        logger.info("\n" + "=" * 60)
        logger.info("📊 学习周期总结")
        logger.info("=" * 60)
        logger.info(f"\n报告ID: {report.report_id}")
        logger.info(f"学习事件: {report.total_learning_events}")
        logger.info(f"知识更新: {report.total_knowledge_updates}")
        logger.info(f"总耗时: {report.total_duration_seconds:.2f}s")
        logger.info(f"\n总结: {report.summary}")
        logger.info("\n建议:")
        for r in report.recommendations:
            logger.info(f"  • {r}")
        logger.info("=" * 60 + "\n")

    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        self._execution_log.append(line)
        logger.info(line)

    def get_execution_log(self) -> str:
        return "\n".join(self._execution_log)

# ═══════════════════════════════════════════════════════════════
# 模块级快速入口（兼容原 run_* 函数签名）
# ═══════════════════════════════════════════════════════════════

def run_unified_learning(
    base_path: str = None,
    strategy_types: Optional[List[LearningStrategyType]] = None,
) -> OrchestratorReport:
    """快速启动统一学习流程"""
    orchestrator = UnifiedLearningOrchestrator(base_path)
    return orchestrator.execute_daily(strategy_types=strategy_types)

def run_integrated_learning(base_path: str = None) -> Dict[str, Any]:
    """兼容 integrated_learning.run_integrated_learning"""
    orchestrator = UnifiedLearningOrchestrator(base_path)
    return orchestrator.plan_and_execute()
