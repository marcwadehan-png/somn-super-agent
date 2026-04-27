# -*- coding: utf-8 -*-
"""
Tier3 调度器 - 核心兼容层

原 _tier3_scheduler.py 的兼容层实现
保持原有API不变，内部委托给子模块
"""

__all__ = [
    'extract_perspective_content',
    'extract_strategy_content',
    'get_statistics',
    'schedule',
]

import time
import random
import logging
from typing import Dict, List, Any, Optional

from ._t3s_types import Tier3Query, Tier3Result, EngineOutput, EngineTier
from ._t3s_domain_matcher import DomainMatcher
from ._t3s_engine_selector import EngineSelector
from ._t3s_fusion import (
    fuse_p1_outputs, build_feasibility_report, synthesize_perspectives,
    synthesize_final_strategy, extract_key_insights,
    calc_tier_balance, calc_coverage, calc_synergy
)

logger = logging.getLogger(__name__)

def extract_perspective_content(raw_output: Any) -> str:
    """从原始输出中提取视角内容"""
    if isinstance(raw_output, dict):
        return raw_output.get("perspective", raw_output.get("观点", ""))
    return ""

def extract_strategy_content(raw_output: Any) -> str:
    """从原始输出中提取策略内容"""
    if isinstance(raw_output, dict):
        return raw_output.get("strategy", raw_output.get("策略", ""))
    return ""

def extract_论证_content(raw_output: Any) -> str:
    """从原始输出中提取论证内容"""
    if isinstance(raw_output, dict):
        return raw_output.get("argument", raw_output.get("论证", ""))
    return ""

class Tier3NeuralScheduler:
    """
    Tier3 神经网络调度器

    实现P1/P2/P3三层引擎调度架构：
    - P1: 核心策略引擎层
    - P2: 交叉验证引擎层
    - P3: 可行性论证引擎层
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化 Tier3 调度器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

        # 引擎池定义
        self.p1_pool: Dict[str, Any] = self._init_p1_pool()
        self.p2_pool: Dict[str, Any] = self._init_p2_pool()
        self.p3_pool: Dict[str, Any] = self._init_p3_pool()

        # 子模块
        self.domain_matcher = DomainMatcher()
        self.engine_selector: Optional[EngineSelector] = None

        # 引擎注册表（延迟初始化）
        self._engine_registry: Dict[str, Any] = {}
        self._initialized = False

        # 统计
        self.total_queries = 0
        self.tier_stats: Dict[str, int] = {"P1": 0, "P2": 0, "P3": 0}
        self.optimizer = None

    def _init_p1_pool(self) -> Dict[str, Any]:
        """初始化P1核心策略引擎池"""
        return {
            "SUFU": {"domains": ["wisdom", "strategy"], "weight": 0.9},
            "MILITARY": {"domains": ["strategy", "competition"], "weight": 0.85},
            "ANCIENT_WISDOM_FUSION": {"domains": ["wisdom", "philosophy"], "weight": 0.8},
            "CROSS_WISDOM_ANALYZER": {"domains": ["wisdom", "analysis"], "weight": 0.75},
            "CONSULTING_VALIDATOR": {"domains": ["consulting", "validation"], "weight": 0.8},
            "CIVILIZATION": {"domains": ["wisdom", "culture"], "weight": 0.7},
            "CIV_WAR_ECONOMY": {"domains": ["strategy", "economy"], "weight": 0.75},
            "SOCIAL_SCIENCE": {"domains": ["social", "behavior"], "weight": 0.8},
            "NATURAL_SCIENCE": {"domains": ["science", "nature"], "weight": 0.75},
            "DAOIST": {"domains": ["philosophy", "wisdom"], "weight": 0.8},
            "CONFUCIAN": {"domains": ["philosophy", "ethics"], "weight": 0.8},
            "BUDDHIST": {"domains": ["philosophy", "mind"], "weight": 0.75},
            "YANGMING": {"domains": ["philosophy", "mind"], "weight": 0.75},
            "GROWTH": {"domains": ["growth", "mindset"], "weight": 0.8},
            "MYTHOLOGY": {"domains": ["culture", "narrative"], "weight": 0.7},
            "LITERARY": {"domains": ["narrative", "culture"], "weight": 0.7},
            "ANTHROPOLOGY": {"domains": ["culture", "behavior"], "weight": 0.75},
            "BEHAVIOR": {"domains": ["behavior", "psychology"], "weight": 0.8},
            "SCIENCE_THINKING": {"domains": ["science", "thinking"], "weight": 0.8},
            "PSYCHOLOGY": {"domains": ["psychology", "behavior"], "weight": 0.85},
            "MARKETING": {"domains": ["marketing", "psychology"], "weight": 0.85},
            "POSITIONING": {"domains": ["marketing", "strategy"], "weight": 0.8},
            "METAPHYSICS": {"domains": ["philosophy", "wisdom"], "weight": 0.7},
            "SCIENTIFIC_AD_VERIFICATION": {"domains": ["validation", "science"], "weight": 0.75},
        }

    def _init_p2_pool(self) -> Dict[str, Any]:
        """初始化P2交叉验证引擎池"""
        return {
            "CRITICAL_THINKING": {"domains": ["thinking", "validation"], "weight": 0.85},
            "SYSTEMS_THINKING": {"domains": ["systems", "analysis"], "weight": 0.8},
            "CROSS_SCALE": {"domains": ["thinking", "scale"], "weight": 0.8},
            "DIALECTICAL": {"domains": ["philosophy", "thinking"], "weight": 0.75},
            "INNOVATION": {"domains": ["innovation", "creativity"], "weight": 0.8},
        }

    def _init_p3_pool(self) -> Dict[str, Any]:
        """初始化P3可行性论证引擎池"""
        return {
            "FEASIBILITY_ANALYZER": {"domains": ["validation", "analysis"], "weight": 0.85},
            "RISK_EVALUATOR": {"domains": ["risk", "validation"], "weight": 0.8},
            "RESOURCE_PLANNER": {"domains": ["planning", "resources"], "weight": 0.75},
            "IMPLEMENTATION_CHECKER": {"domains": ["implementation", "validation"], "weight": 0.8},
        }

    def _initialize_engines(self) -> None:
        """延迟初始化引擎实例"""
        if self._initialized:
            return

        # 引擎选择器初始化（需要ROI tracker）
        roi_tracker = self._get_roi_tracker()
        self.engine_selector = EngineSelector(
            self.p1_pool,
            self.p2_pool,
            self.p3_pool,
            self.domain_matcher,
            roi_tracker
        )

        self._initialized = True
        self.logger.info(f"Tier3调度器初始化完成，P1={len(self.p1_pool)}, P2={len(self.p2_pool)}, P3={len(self.p3_pool)}")

    def _get_roi_tracker(self) -> Any:
        """获取ROI追踪器"""
        try:
            from ...core.roi_tracker_core import get_roi_tracker
            return get_roi_tracker()
        except Exception:
            return None

    def _supports_roi_writeback(self, tracker: Any) -> bool:
        """检查是否支持ROI回写"""
        if tracker is None:
            return False
        return hasattr(tracker, 'record_interaction') and hasattr(tracker, 'track_task_complete')

    def schedule(self, query: Tier3Query) -> Tier3Result:
        """
        执行三级神经网络调度

        Args:
            query: 三级查询

        Returns:
            Tier3Result: 三层融合后的调度结果
        """
        start_time = time.time()
        workflow_reference_id = ""
        strategy_combo: List[str] = []
        roi_trace: Dict[str, Any] = {
            "tracker_available": False,
            "writeback_enabled": False,
            "workflow_reference_id": "",
            "strategy_combo": [],
            "engine_records": [],
            "workflow_record": {},
        }

        self._initialize_engines()

        # 设置随机种子
        rng = random.Random(query.random_seed)

        try:
            # Step 1: 领域识别
            domains = self.domain_matcher.extract_domains(query.query_text)
            workflow_reference_id = self._build_workflow_reference_base(query, domains)
            roi_tracker = self._get_roi_tracker()
            roi_writeback_enabled = self._supports_roi_writeback(roi_tracker)
            roi_trace.update({
                "tracker_available": roi_tracker is not None,
                "writeback_enabled": roi_writeback_enabled,
                "workflow_reference_id": workflow_reference_id,
            })

            # Step 2: 选择P1核心策略引擎
            p1_selected = self.engine_selector.select_p1_engines(query, domains, rng)
            p1_outputs = self._execute_p1_engines(p1_selected, query)
            self.tier_stats["P1"] += len(p1_outputs)

            # Step 3: 选择P3可行性论证引擎
            p3_selected = self.engine_selector.select_p3_engines(query, domains, rng)
            p3_outputs = self._execute_p3_engines(p3_selected, query)
            self.tier_stats["P3"] += len(p3_outputs)

            # Step 4: 选择P2交叉验证引擎
            p2_selected = self.engine_selector.select_p2_engines(query, domains, rng, p1_selected)
            p2_outputs = self._execute_p2_engines(p2_selected, query)
            self.tier_stats["P2"] += len(p2_outputs)

            # Step 5: 三层融合
            fused_strategy = fuse_p1_outputs(p1_outputs)
            feasibility_report = build_feasibility_report(p3_outputs, p1_outputs)
            perspective_synthesis = synthesize_perspectives(p2_outputs)

            # Step 6: 生成最终结果
            final_strategy, confidence, warnings = synthesize_final_strategy(
                fused_strategy, feasibility_report, perspective_synthesis
            )

            # Step 7: 计算指标
            insights = extract_key_insights(p1_outputs, p3_outputs, p2_outputs)
            tier_balance = calc_tier_balance(p1_outputs, p3_outputs, p2_outputs)

            engine_pool = {**self.p1_pool, **self.p2_pool, **self.p3_pool}
            coverage = calc_coverage(domains, p1_outputs, p3_outputs, p2_outputs,
                                      self.domain_matcher, engine_pool)
            synergy = calc_synergy(p1_outputs, p3_outputs, p2_outputs)

            processing_time = time.time() - start_time
            self.total_queries += 1

            strategy_combo = [o.engine_id for o in p1_outputs]

            result = Tier3Result(
                query_id=query.query_id,
                query_text=query.query_text,
                success=True,
                fused_strategy=fused_strategy,
                feasibility_report=feasibility_report,
                perspective_synthesis=perspective_synthesis,
                final_strategy=final_strategy,
                decision_confidence=confidence,
                risk_warnings=warnings,
                key_insights=insights,
                tier_balance=tier_balance,
                coverage=coverage,
                synergy_score=synergy,
                processing_time=processing_time,
                workflow_reference_id=workflow_reference_id,
                strategy_combo=strategy_combo,
                roi_trace=roi_trace,
            )

            if roi_writeback_enabled:
                self._record_roi_data(roi_tracker, query, result, workflow_reference_id, strategy_combo)

            self.logger.info(f"[Tier3] 调度完成，耗时: {processing_time:.2f}s，置信度: {confidence:.2f}")
            return result

        except Exception as e:
            self.logger.error(f"[Tier3] 调度失败: {e}")
            roi_trace["error"] = "ROI分析失败"
            return Tier3Result(
                query_id=query.query_id,
                query_text=query.query_text,
                success=False,
                fused_strategy={},
                feasibility_report={},
                perspective_synthesis={},
                final_strategy="处理失败",
                decision_confidence=0.0,
                tier_balance=0.0,
                coverage=0.0,
                synergy_score=0.0,
                processing_time=time.time() - start_time,
                workflow_reference_id=workflow_reference_id,
                strategy_combo=strategy_combo,
                roi_trace=roi_trace,
            )

    def _execute_p1_engines(self, selected: List[Any], query: Tier3Query) -> List[EngineOutput]:
        """执行P1引擎"""
        outputs = []
        for sel in selected:
            start = time.time()
            try:
                # 模拟引擎调用
                raw = {"strategy": f"策略建议来自 {sel.engine_id}", "confidence": sel.match_score}
                exec_time = time.time() - start

                outputs.append(EngineOutput(
                    engine_id=sel.engine_id,
                    tier="P1",
                    match_score=sel.match_score,
                    execution_time=exec_time,
                    raw_output=raw,
                    perspective_content=extract_perspective_content(raw),
                    strategy_content=extract_strategy_content(raw),
                    success=True
                ))
            except Exception as e:
                outputs.append(EngineOutput(
                    engine_id=sel.engine_id,
                    tier="P1",
                    match_score=sel.match_score,
                    execution_time=0,
                    raw_output={"error": "执行失败"},
                    success=False,
                    warnings=["执行异常"]
                ))
        return outputs

    def _execute_p2_engines(self, selected: List[Any], query: Tier3Query) -> List[EngineOutput]:
        """执行P2引擎"""
        outputs = []
        for sel in selected:
            start = time.time()
            try:
                raw = {"perspective": f"视角分析来自 {sel.engine_id}", "challenging_arguments": []}
                exec_time = time.time() - start

                outputs.append(EngineOutput(
                    engine_id=sel.engine_id,
                    tier="P2",
                    match_score=sel.match_score,
                    execution_time=exec_time,
                    raw_output=raw,
                    perspective_content=extract_perspective_content(raw),
                    success=True
                ))
            except Exception as e:
                outputs.append(EngineOutput(
                    engine_id=sel.engine_id,
                    tier="P2",
                    match_score=sel.match_score,
                    execution_time=0,
                    raw_output={"error": "执行失败"},
                    success=False,
                    warnings=["交叉验证异常"]
                ))
        return outputs

    def _execute_p3_engines(self, selected: List[Any], query: Tier3Query) -> List[EngineOutput]:
        """执行P3引擎"""
        outputs = []
        for sel in selected:
            start = time.time()
            try:
                raw = {"argument": f"可行性论证来自 {sel.engine_id}", "feasibility": "可行"}
                exec_time = time.time() - start

                outputs.append(EngineOutput(
                    engine_id=sel.engine_id,
                    tier="P3",
                    match_score=sel.match_score,
                    execution_time=exec_time,
                    raw_output=raw,
                    论证_content=extract_论证_content(raw),
                    success=True
                ))
            except Exception as e:
                outputs.append(EngineOutput(
                    engine_id=sel.engine_id,
                    tier="P3",
                    match_score=sel.match_score,
                    execution_time=0,
                    raw_output={"error": "执行失败"},
                    success=False,
                    warnings=["论证异常"]
                ))
        return outputs

    def _build_workflow_reference_base(self, query: Tier3Query, domains: Dict[str, float]) -> str:
        """构建工作流引用基础"""
        domain_str = "_".join(sorted(domains.keys())[:3]) if domains else "general"
        return f"tier3_{domain_str}_{hash(query.query_text) % 10000}"

    def _record_roi_data(self, tracker: Any, query: Tier3Query, result: Tier3Result,
                         workflow_reference_id: str, strategy_combo: List[str]) -> None:
        """记录ROI数据"""
        try:
            if hasattr(tracker, "record_interaction"):
                tracker.record_interaction(
                    query.query_id,
                    "tier3_schedule_complete",
                    duration_seconds=result.processing_time,
                    metadata={
                        "decision_confidence": result.decision_confidence,
                        "success": result.success,
                    },
                )
        except Exception as e:
            self.logger.warning(f"ROI记录失败: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """获取调度统计"""
        return {
            "total_queries": self.total_queries,
            "tier_engine_count": {
                "P1": len(self.p1_pool),
                "P2": len(self.p2_pool),
                "P3": len(self.p3_pool)
            },
            "total_engine_invocations": dict(self.tier_stats),
            "registry_size": len(self._engine_registry)
        }
