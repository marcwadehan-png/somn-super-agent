"""
__all__ = [
    'execute',
    'get_description',
    'should_execute',
    'strategy_type',
]

增强学习策略 - Enhanced Learning Strategy
提取自 enhanced_three_tier_learning.py 的差异化能力：
- 场景识别 + 动态策略选择（DynamicStrategyEngine）
- 浏览器自动化采集（BrowserNetworkLearner，异步）
- 数据权威性评估与过滤（DataSourceValidator）
- 性能评估 + 参数自动调整（ParameterAdjustmentSystem）
- 综合报告生成（包含权威性分布、性能评分）
"""

from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger(__name__)
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_strategy import (
    BaseLearningStrategy,
    DataScanResult,
    LearningResult,
    LearningStrategyType,
)

class EnhancedLearningStrategy(BaseLearningStrategy):
    """
    增强三层学习策略。

    差异化能力（仅此策略独有）：
    1. DynamicStrategyEngine：场景识别 → 策略选择 → 参数生成
    2. 浏览器自动化（async）：BrowserNetworkLearner
    3. 数据权威性评估与过滤（quality_score ≥ 0.60）
    4. ParameterAdjustmentSystem：性能评估 + 自动调参
    5. 交叉融合洞察（权威性分布 + 质量分析）
    """

    def __init__(self, base_path: str = None):
        super().__init__(base_path)
        self._strategy_engine: Optional[Any] = None
        self._browser_learner: Optional[Any] = None
        self._param_system: Optional[Any] = None
        self._subsystems_loaded = False

    @property
    def strategy_type(self) -> LearningStrategyType:
        return LearningStrategyType.ENHANCED

    def get_description(self) -> str:
        return "增强三层学习策略：场景识别+动态策略+浏览器自动化+性能自适应调参"

    def should_execute(self, scan_result: DataScanResult) -> bool:
        """增强策略始终可执行（浏览器采集不依赖本地数据）"""
        return True

    def execute(self, scan_result: DataScanResult, context: Dict[str, Any]) -> LearningResult:
        """
        同步入口：在事件循环中调用 _execute_async。

        context 可选包含：
            research_topic: str
            target_sources: List[Dict]
            local_data_context: Dict（data_count / growth_rate / quality_trend）
            priority: str
            urgency: str
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 若在已有事件循环中（如 Jupyter），使用 run_coroutine_threadsafe
                import concurrent.futures
                future = concurrent.futures.Future()

                async def _run():
                    try:
                        r = await self._execute_async(scan_result, context)
                        future.set_result(r)
                    except Exception as exc:
                        future.set_exception(exc)

                asyncio.ensure_future(_run())
                return future.result(timeout=120)
            else:
                return loop.run_until_complete(self._execute_async(scan_result, context))
        except RuntimeError:
            # 没有 event loop，新建一个
            return asyncio.run(self._execute_async(scan_result, context))

    async def _execute_async(
        self, scan_result: DataScanResult, context: Dict[str, Any]
    ) -> LearningResult:
        import time
        t0 = time.time()
        result = LearningResult(strategy_type=self.strategy_type.value)

        self._load_subsystems()

        research_topic = context.get("research_topic", "AI智能办公研究")
        target_sources = context.get("target_sources", [])
        local_ctx = context.get("local_data_context", {
            "data_count": scan_result.local_count,
            "growth_rate": 0.0,
            "quality_trend": "stable",
        })
        priority = context.get("priority", "medium")
        urgency = context.get("urgency", "normal")

        # 阶段1：场景识别 + 策略选择
        exec_params: Dict = {}
        strategy_obj = None
        scenario_obj = None
        if self._strategy_engine:
            try:
                scenario_obj = self._strategy_engine.identify_scenario(
                    local_data_count=local_ctx.get("data_count", 0),
                    local_data_growth_rate=local_ctx.get("growth_rate", 0.0),
                    network_availability=local_ctx.get("network_availability", 0.95),
                    data_quality_trend=local_ctx.get("quality_trend", "stable"),
                    priority=priority,
                    urgency=urgency,
                    depth_requirement="deep" if urgency == "urgent" else "medium",
                )
                strategy_obj = self._strategy_engine.select_strategy(scenario_obj)
                exec_params = self._strategy_engine.generate_execution_params(strategy_obj)
                result.extra["scenario"] = scenario_obj.scenario_type.value if scenario_obj else None
                result.extra["strategy_name"] = strategy_obj.name if strategy_obj else None
                logger.info(f"场景识别: {result.extra['scenario']} | 策略: {result.extra['strategy_name']}")
            except Exception as e:
                logger.warning(f"场景识别失败: {e}")
        result.phases_completed.append("场景识别")

        # 阶段2：浏览器网络学习（必须）
        valid_findings: List[Any] = []
        if self._browser_learner and (not strategy_obj or strategy_obj.network_learning_enabled):
            try:
                browser_session = await self._browser_learner.learn_from_sources(
                    research_topic=research_topic,
                    target_sources=target_sources,
                    research_goal="通过浏览器自动化获取权威网络数据",
                )
                for point in browser_session.data_collected:
                    if getattr(getattr(point, "metadata", None), "has_data_source", False) and \
                            getattr(point, "quality_score", 0) >= 0.60:
                        valid_findings.append(point)
                        result.learning_events.append({
                            "type": "browser_finding",
                            "quality": getattr(point, "quality_score", 0),
                        })
                logger.info(f"网络学习完成: {len(valid_findings)} 条有效数据")
            except Exception as e:
                logger.warning(f"浏览器学习失败: {e}")
                result.error_messages.append(f"浏览器学习失败: {e}")
        result.phases_completed.append("网络学习")

        # 阶段3：本地学习（可选）
        local_loaded = 0
        local_count = local_ctx.get("data_count", 0)
        local_threshold = exec_params.get("local_data_threshold", 3) if exec_params else 3
        if strategy_obj and strategy_obj.local_learning_enabled and local_count >= local_threshold:
            local_loaded = min(local_count, 50)
            logger.info(f"本地学习: 加载 {local_loaded} 条")
        else:
            logger.info(f"本地学习跳过 (data={local_count}, threshold={local_threshold})")
        result.phases_completed.append("本地学习")

        # 阶段4：性能评估
        metrics = None
        if self._param_system and exec_params:
            try:
                learning_results = {
                    "data_points": valid_findings,
                    "patterns": [],
                    "insights": [],
                    "execution_time": time.time() - t0,
                    "errors": result.error_messages,
                }
                metrics = self._param_system.record_learning_result(learning_results, exec_params)
                result.extra["performance_score"] = getattr(metrics, "overall_score", 0)
                result.extra["satisfaction"] = getattr(metrics, "satisfaction_level", "unknown")
                logger.info(f"性能评估: {result.extra['performance_score']:.2f} ({result.extra['satisfaction']})")
            except Exception as e:
                logger.warning(f"性能评估失败: {e}")
        result.phases_completed.append("性能评估")

        # 阶段5：参数调整
        if self._param_system and metrics and exec_params:
            try:
                _, adjustments = self._param_system.adjust_parameters(
                    exec_params, metrics, aggressive=(urgency == "urgent")
                )
                result.extra["param_adjustments"] = [
                    {"param": a.parameter_name, "old": a.old_value,
                     "new": a.new_value, "reason": a.reason}
                    for a in adjustments
                ]
                logger.info(f"参数调整: {len(adjustments)} 处修改")
            except Exception as e:
                logger.warning(f"参数调整失败: {e}")
        result.phases_completed.append("参数调整")

        # 阶段6：交叉融合
        if valid_findings and local_loaded > 0 and (not strategy_obj or strategy_obj.cross_learning_enabled):
            insights = self._perform_cross_learning(valid_findings, local_loaded)
            result.cross_insights = insights
            logger.info(f"交叉融合: {len(insights)} 条洞察")
        else:
            logger.info(f"交叉融合跳过 (network={len(valid_findings)}, local={local_loaded})")
        result.phases_completed.append("交叉融合")

        result.duration_seconds = round(time.time() - t0, 2)
        result.summary = (
            f"增强学习完成：网络 {len(valid_findings)} 条有效数据，"
            f"本地 {local_loaded} 条，"
            f"交叉洞察 {len(result.cross_insights)} 条。"
        )
        return result

    # ─────────────────────────────────────────────────
    # 差异化：交叉融合分析
    # ─────────────────────────────────────────────────

    def _perform_cross_learning(
        self, network_findings: List[Any], local_data_count: int
    ) -> List[Dict]:
        """分析权威性分布 + 质量分布，生成洞察"""
        insights: List[Dict] = []
        authority_dist: Dict[str, int] = {}
        for f in network_findings:
            auth = getattr(getattr(f, "metadata", None), "authority", None)
            auth_val = getattr(auth, "value", str(auth)) if auth else "未知"
            authority_dist[auth_val] = authority_dist.get(auth_val, 0) + 1

        if authority_dist.get("权威", 0) >= len(network_findings) * 0.5:
            insights.append({
                "type": "authority_positive",
                "content": "网络数据以权威来源为主，数据可信度高",
                "confidence": 0.95,
            })

        quality_scores = [getattr(f, "quality_score", 0) for f in network_findings]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        if avg_quality >= 0.75:
            insights.append({
                "type": "quality_positive",
                "content": f"网络数据质量优良 (平均{avg_quality:.2f})",
                "confidence": 0.90,
            })

        if local_data_count > len(network_findings):
            insights.append({
                "type": "data_fusion",
                "content": (f"本地数据({local_data_count}) > 网络数据({len(network_findings)})，"
                            "建议优先使用本地数据，网络数据作为验证"),
                "confidence": 0.85,
            })
        return insights

    # ─────────────────────────────────────────────────
    # 子系统懒加载
    # ─────────────────────────────────────────────────

    def _load_subsystems(self):
        if self._subsystems_loaded:
            return
        try:
            from ..browser_automation_learning import BrowserNetworkLearner
            from ..dynamic_strategy_engine import DynamicStrategyEngine
            from ..intelligent_parameter_system import ParameterAdjustmentSystem

            self._strategy_engine = DynamicStrategyEngine()
            self._browser_learner = BrowserNetworkLearner()
            self._param_system = ParameterAdjustmentSystem()
        except ImportError as e:
            logger.warning(f"增强学习子系统加载失败（部分功能降级）: {e}")
        self._subsystems_loaded = True
