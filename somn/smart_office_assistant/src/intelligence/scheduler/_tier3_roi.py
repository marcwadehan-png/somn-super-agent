# -*- coding: utf-8 -*-
"""
三级神经网络调度器 - ROI追踪模块
Tier-3 Neural Scheduler ROI Tracking
====================================

包含ROI追踪相关方法:
- ROI Tracker惰性加载
- ROI outcome构建
- ROI trace记录
- workflow reference构建

版本: v1.0
日期: 2026-04-06
"""

from typing import Dict, List, Any, Optional
import json
import hashlib
import logging

logger = logging.getLogger(__name__)

class ROIMixin:
    """ROI追踪混入类 - 为调度器提供ROI功能"""

    def _get_roi_tracker(self):
        """惰性get ROITracker,调度层只在需要历史表现时触发."""
        if self._roi_tracker_init_attempted:
            return self._roi_tracker

        self._roi_tracker_init_attempted = True
        try:
            from ..neural_memory.roi_tracker import ROITracker
            self._roi_tracker = ROITracker()
        except Exception as exc:
            logger.warning(f"[Tier3] ROITracker init失败,回退为纯规则调度: {exc}")
            self._roi_tracker = None
        return self._roi_tracker

    def _clamp_unit_score(self, value: Any, default: float = 0.0) -> float:
        """把任意分值压到 0~1,避免异常值污染调度排序."""
        try:
            score = float(value)
        except (TypeError, ValueError):
            score = float(default)
        return max(0.0, min(1.0, score))

    def _normalize_reference_key(self, value: Any, default: str = "general") -> str:
        """把工作流参考字段压缩成稳定可复用的 key."""
        text = str(value or "").strip().lower()
        if not text:
            return default
        normalized = "".join(
            ch if ch.isalnum() or ('\u4e00' <= ch <= '\u9fff') else "_"
            for ch in text
        ).strip("_")
        return normalized[:32] or default

    def _build_workflow_reference_base(self, query: Any, domains: Dict[str, float]) -> str:
        """为 Tier3 调度构建稳定工作流参考ID,供 workflow/combo ROI 复用."""
        context = query.context if hasattr(query, 'context') and isinstance(query.context, dict) else {}
        explicit = str(
            context.get("workflow_reference_id")
            or context.get("workflow_reference_base")
            or ""
        ).strip()
        if explicit:
            return explicit

        ranked_domains = sorted((domains or {}).items(), key=lambda item: item[1], reverse=True)
        top_domains = [name for name, _ in ranked_domains[:4]]
        signature_payload = {
            "query_text": str(query.query_text or "").strip()[:160],
            "role": str(context.get("role") or ""),
            "urgency": str(context.get("urgency") or ""),
            "domains": top_domains,
        }
        signature_text = json.dumps(signature_payload, ensure_ascii=False, sort_keys=True)
        digest = hashlib.sha1(signature_text.encode("utf-8")).hexdigest()[:12]
        primary_domain = self._normalize_reference_key(top_domains[0] if top_domains else "general")
        role_key = self._normalize_reference_key(context.get("role") or "general")
        return f"tier3wf::{role_key}::{primary_domain}::{digest}"

    def _build_engine_workflow_reference(self, workflow_reference_base: str, tier: str, engine_id: str) -> str:
        """为具体层级引擎构建可复用的工作流参考ID."""
        return f"{workflow_reference_base}::{tier}::{engine_id}"

    def _supports_roi_writeback(self, roi_tracker: Any) -> bool:
        """检测 ROITracker 是否具备完整写回能力."""
        required_methods = ("track_task_start", "track_task_complete", "track_workflow_completion")
        return roi_tracker is not None and all(hasattr(roi_tracker, method) for method in required_methods)

    def _build_strategy_combo(self,
                               p1_selected: List[Any],
                               p3_selected: List[Any],
                               p2_selected: List[Any]) -> List[str]:
        """按执行顺序generate本次 Tier3 的strategy组合."""
        ordered_combo: List[str] = []
        seen = set()
        for selection in [*p1_selected, *p3_selected, *p2_selected]:
            engine_id = str(selection.engine_id or "").strip()
            if not engine_id or engine_id in seen:
                continue
            ordered_combo.append(engine_id)
            seen.add(engine_id)
        return ordered_combo

    def _build_engine_roi_outcome(self, output: Any) -> Dict[str, Any]:
        """把单引擎执行结果压缩为 ROI 可消费的 outcome."""
        # 获取content - 支持多种属性名
        content = (
            getattr(output, 'strategy_content', None)
            or getattr(output, '论证_content', None)
            or getattr(output, 'perspective_content', None)
            or ""
        )
        warnings = getattr(output, 'warnings', []) or []
        match_score = getattr(output, 'match_score', 0.5)
        success = getattr(output, 'success', True)
        execution_time = getattr(output, 'execution_time', 0)
        engine_id = getattr(output, 'engine_id', 'unknown')
        tier = getattr(output, 'tier', 'unknown')

        warning_penalty = min(len(warnings), 3) * 0.08
        content_bonus = 0.08 if content else 0.0
        success_bonus = 0.27 if success else 0.0
        quality_score = self._clamp_unit_score(
            match_score * 0.55 + success_bonus + content_bonus - warning_penalty,
            0.0,
        )
        error_count = 0 if success else max(1, len(warnings) or 1)
        return {
            "completed": success,
            "failed": 0 if success else 1,
            "blocked": 0,
            "success_ratio": 1.0 if success else 0.0,
            "quality_score": quality_score,
            "actual_minutes": max(execution_time / 60.0, 0.01),
            "time_saved_minutes": 0.0,
            "outputs": {
                "engine_id": engine_id,
                "tier": tier,
                "content_preview": str(content)[:160],
            },
            "adopted": success and bool(content),
            "error_count": error_count,
            "strategy_combo": [engine_id],
        }

    def _build_workflow_roi_outcome(self,
                                    result: Any,
                                    strategy_combo: List[str]) -> Dict[str, Any]:
        """把 Tier3 最终结果压缩为 workflow / combo 级 ROI outcome."""
        p1_outputs = getattr(result, 'p1_outputs', []) or []
        p3_outputs = getattr(result, 'p3_outputs', []) or []
        p2_outputs = getattr(result, 'p2_outputs', []) or []
        all_outputs = [*p1_outputs, *p3_outputs, *p2_outputs]
        total_engines = len(all_outputs)
        succeeded = sum(1 for output in all_outputs if getattr(output, 'success', False))
        failed = total_engines - succeeded
        risk_warnings = getattr(result, 'risk_warnings', []) or []
        decision_confidence = getattr(result, 'decision_confidence', 0)
        synergy_score = getattr(result, 'synergy_score', 0)
        coverage = getattr(result, 'coverage', 0)
        tier_balance = getattr(result, 'tier_balance', 0)
        success = getattr(result, 'success', False)
        final_strategy = getattr(result, 'final_strategy', '')
        processing_time = getattr(result, 'processing_time', 0)
        key_insights = getattr(result, 'key_insights', []) or []

        warning_penalty = min(len(risk_warnings), 4) * 0.05
        quality_score = self._clamp_unit_score(
            decision_confidence * 0.5
            + synergy_score * 0.2
            + coverage * 0.15
            + tier_balance * 0.15
            - warning_penalty,
            0.0,
        )
        return {
            "completed": 1 if success else 0,
            "failed": failed,
            "blocked": 0,
            "success_ratio": round(succeeded / max(total_engines, 1), 4),
            "quality_score": quality_score,
            "actual_minutes": max(processing_time / 60.0, 0.01),
            "time_saved_minutes": 0.0,
            "outputs": {
                "final_strategy_preview": str(final_strategy)[:240],
                "insight_count": len(key_insights),
                "engine_count": total_engines,
            },
            "adopted": success and bool(final_strategy),
            "error_count": failed + len(risk_warnings),
            "strategy_combo": strategy_combo,
        }

    def _record_engine_roi_trace(self,
                                 query: Any,
                                 workflow_reference_base: str,
                                 outputs: List[Any],
                                 roi_tracker: Any) -> List[Dict[str, Any]]:
        """把单引擎执行结果写回 ROITracker,并返回可观察 trace."""
        if not self._supports_roi_writeback(roi_tracker) or not workflow_reference_base:
            return []

        trace_entries: List[Dict[str, Any]] = []
        for output in outputs:
            engine_workflow_id = self._build_engine_workflow_reference(
                workflow_reference_base,
                getattr(output, 'tier', 'unknown'),
                getattr(output, 'engine_id', 'unknown'),
            )
            engine_task_id = f"{query.query_id}::{getattr(output, 'tier', 'unknown')}::{getattr(output, 'engine_id', 'unknown')}"
            estimated_minutes = max(0.1, round(getattr(output, 'execution_time', 0) / 60.0 + 0.1, 3))

            try:
                roi_tracker.track_task_start(
                    task_id=engine_task_id,
                    task_type="tier3_engine_execution",
                    strategy=getattr(output, 'engine_id', 'unknown'),
                    estimated_minutes=estimated_minutes,
                    workflow_id=engine_workflow_id,
                    strategy_combo=[getattr(output, 'engine_id', 'unknown')],
                )
                if hasattr(roi_tracker, "record_interaction"):
                    roi_tracker.record_interaction(
                        engine_task_id,
                        f"{str(getattr(output, 'tier', 'unknown')).lower()}_engine_execution",
                        duration_seconds=getattr(output, 'execution_time', 0),
                        metadata={
                            "match_score": getattr(output, 'match_score', 0),
                            "success": getattr(output, 'success', False),
                        },
                    )

                outcome = self._build_engine_roi_outcome(output)
                task_record_id = roi_tracker.track_task_complete(engine_task_id, outcome) or ""
                workflow_record = (
                    roi_tracker.track_workflow_completion(
                        engine_workflow_id,
                        outcome,
                        strategy_combo=[getattr(output, 'engine_id', 'unknown')],
                    )
                    if task_record_id
                    else {"status": "task_record_missing", "workflow_id": engine_workflow_id}
                )
                trace_entries.append({
                    "engine_id": getattr(output, 'engine_id', 'unknown'),
                    "tier": getattr(output, 'tier', 'unknown'),
                    "task_id": engine_task_id,
                    "workflow_id": engine_workflow_id,
                    "task_record_id": task_record_id,
                    "workflow_record": workflow_record,
                    "success": getattr(output, 'success', False),
                })
            except Exception as exc:
                logger.warning(f"[Tier3] ROI 写回失败({getattr(output, 'tier', 'unknown')}/{getattr(output, 'engine_id', 'unknown')}): {exc}")
                trace_entries.append({
                    "engine_id": getattr(output, 'engine_id', 'unknown'),
                    "tier": getattr(output, 'tier', 'unknown'),
                    "task_id": engine_task_id,
                    "workflow_id": engine_workflow_id,
                    "success": False,
                    "error": str(exc),
                })

        return trace_entries
