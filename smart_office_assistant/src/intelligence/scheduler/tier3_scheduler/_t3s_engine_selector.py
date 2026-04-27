# -*- coding: utf-8 -*-
"""
__all__ = [
    'select_p1_engines',
    'select_p2_engines',
    'select_p3_engines',
]

Tier3 调度器 - 引擎选择模块
处理P1/P2/P3三层引擎的选择逻辑
"""

from typing import Dict, List, Any, Optional
import random
import logging

from ._t3s_types import Tier3Query, TierSelection, EngineTier
from ._t3s_domain_matcher import DomainMatcher

logger = logging.getLogger(__name__)

class EngineSelector:
    """引擎选择器"""

    def __init__(
        self,
        p1_pool: Dict[str, Any],
        p2_pool: Dict[str, Any],
        p3_pool: Dict[str, Any],
        domain_matcher: DomainMatcher,
        roi_tracker: Any = None
    ):
        self.p1_pool = p1_pool
        self.p2_pool = p2_pool
        self.p3_pool = p3_pool
        self.domain_matcher = domain_matcher
        self.roi_tracker = roi_tracker

    def select_p1_engines(
        self,
        query: Tier3Query,
        domains: Dict[str, float],
        rng: random.Random
    ) -> List[TierSelection]:
        """选择P1核心策略引擎"""
        candidates = []
        workflow_reference_base = self._build_workflow_reference_base(query, domains)

        # 过滤排除的引擎
        pool = {k: v for k, v in self.p1_pool.items() if k not in query.excluded_engines}

        for engine_id, engine_info in pool.items():
            score, matched_domains = self.domain_matcher.match_engine(
                engine_id, domains, pool
            )
            base_weight = self._get_engine_weight(engine_id, engine_info)

            # ROI 分数计算
            strategy_roi_score = 0.5
            workflow_roi_score = 0.5
            historical_confidence = 0.0

            if self.roi_tracker:
                strategy_roi_raw = self.roi_tracker.get_strategy_roi(engine_id)
                strategy_roi_score = self._clamp_unit_score(
                    strategy_roi_raw.get("avg_efficiency_score"), 0.5
                )
                strategy_sample_count = int(strategy_roi_raw.get("sample_count", 0) or 0)

                workflow_reference_id = self._build_engine_workflow_reference(
                    workflow_reference_base, "P1", engine_id
                )
                workflow_roi_raw = self.roi_tracker.get_workflow_roi(workflow_reference_id)
                if workflow_roi_raw.get("status") == "no_data":
                    workflow_roi_raw = self.roi_tracker.get_workflow_roi(workflow_reference_base)
                workflow_roi_score = self._clamp_unit_score(
                    workflow_roi_raw.get("avg_efficiency_score"), 0.5
                )

                historical_confidence = self._clamp_unit_score(
                    max(
                        float(strategy_roi_raw.get("confidence", 0.0) or 0.0),
                        float(workflow_roi_raw.get("confidence", 0.0) or 0.0),
                        min(1.0, strategy_sample_count / 20.0) if strategy_sample_count > 0 else 0.0,
                    ),
                    0.0,
                )

            final_score = self._clamp_unit_score(
                score * 0.35
                + base_weight * 0.3
                + strategy_roi_score * 0.15
                + workflow_roi_score * 0.1
                + historical_confidence * 0.1,
                0.5,
            )

            reason = (
                f"域匹配({score:.2f}) + 权重({base_weight:.2f}) + "
                f"策略ROI({strategy_roi_score:.2f}) + workflowROI({workflow_roi_score:.2f}) + "
                f"历史置信度({historical_confidence:.2f})"
            )

            candidates.append(TierSelection(
                tier=EngineTier.P1,
                engine_id=engine_id,
                match_score=final_score,
                domains=matched_domains,
                reason=reason
            ))

        # 强制包含
        for req_id in query.required_engines:
            if req_id in pool and not any(c.engine_id == req_id for c in candidates):
                candidates.append(TierSelection(
                    tier=EngineTier.P1,
                    engine_id=req_id,
                    match_score=1.0,
                    domains=[],
                    reason="强制包含"
                ))

        return self._weighted_ranked_selection(candidates, query.p1_count, rng)

    def select_p2_engines(
        self,
        query: Tier3Query,
        domains: Dict[str, float],
        rng: random.Random,
        p1_selected: List[TierSelection]
    ) -> List[TierSelection]:
        """选择P2交叉验证引擎"""
        candidates = []
        workflow_reference_base = self._build_workflow_reference_base(query, domains)
        pool = {k: v for k, v in self.p2_pool.items() if k not in query.excluded_engines}

        p1_domains_used = set()
        p1_engine_ids = []
        for p1 in p1_selected:
            p1_domains_used.update(p1.domains)
            p1_engine_ids.append(p1.engine_id)

        for engine_id, engine_info in pool.items():
            score, matched_domains = self.domain_matcher.match_engine(
                engine_id, domains, pool
            )
            base_weight = self._get_engine_weight(engine_id, engine_info)
            engine_domains = self._get_engine_domains(engine_id, engine_info)

            diversity_bonus = 0.12 if not self.domain_matcher.domains_overlap(
                p1_domains_used, engine_domains
            ) else 0.02

            # ROI 计算
            strategy_roi_score = 0.5
            workflow_roi_score = 0.5
            combo_roi_score = 0.5
            historical_confidence = 0.0

            if self.roi_tracker:
                strategy_roi_raw = self.roi_tracker.get_strategy_roi(engine_id)
                strategy_roi_score = self._clamp_unit_score(
                    strategy_roi_raw.get("avg_efficiency_score"), 0.5
                )
                strategy_sample_count = int(strategy_roi_raw.get("sample_count", 0) or 0)

                workflow_reference_id = self._build_engine_workflow_reference(
                    workflow_reference_base, "P2", engine_id
                )
                workflow_roi_raw = self.roi_tracker.get_workflow_roi(workflow_reference_id)
                if workflow_roi_raw.get("status") == "no_data":
                    workflow_roi_raw = self.roi_tracker.get_workflow_roi(workflow_reference_base)
                workflow_roi_score = self._clamp_unit_score(
                    workflow_roi_raw.get("avg_efficiency_score"), 0.5
                )

                combo_roi_raw = self.roi_tracker.get_strategy_combo_roi(
                    strategy_combo=[*p1_engine_ids, engine_id]
                ) if len(p1_engine_ids) >= 1 else {"status": "no_data"}
                combo_roi_score = self._clamp_unit_score(
                    combo_roi_raw.get("avg_efficiency_score"), 0.5
                )

                historical_confidence = self._clamp_unit_score(
                    max(
                        float(strategy_roi_raw.get("confidence", 0.0) or 0.0),
                        float(workflow_roi_raw.get("confidence", 0.0) or 0.0),
                        float(combo_roi_raw.get("confidence", 0.0) or 0.0),
                        min(1.0, strategy_sample_count / 20.0) if strategy_sample_count > 0 else 0.0,
                    ),
                    0.0,
                )

            final_score = self._clamp_unit_score(
                score * 0.22
                + base_weight * 0.18
                + strategy_roi_score * 0.12
                + workflow_roi_score * 0.08
                + combo_roi_score * 0.25
                + diversity_bonus
                + historical_confidence * 0.05,
                0.5,
            )

            reason = (
                f"域匹配({score:.2f}) + 权重({base_weight:.2f}) + 多样性({diversity_bonus:.2f}) + "
                f"策略ROI({strategy_roi_score:.2f}) + workflowROI({workflow_roi_score:.2f}) + "
                f"comboROI({combo_roi_score:.2f}) + 历史置信度({historical_confidence:.2f})"
            )

            candidates.append(TierSelection(
                tier=EngineTier.P2,
                engine_id=engine_id,
                match_score=final_score,
                domains=matched_domains,
                reason=reason
            ))

        # 强制包含
        for req_id in query.required_engines:
            if req_id in pool and not any(c.engine_id == req_id for c in candidates):
                candidates.append(TierSelection(
                    tier=EngineTier.P2,
                    engine_id=req_id,
                    match_score=1.0,
                    domains=[],
                    reason="强制包含"
                ))

        return self._weighted_ranked_selection(candidates, query.p2_count, rng)

    def select_p3_engines(
        self,
        query: Tier3Query,
        domains: Dict[str, float],
        rng: random.Random
    ) -> List[TierSelection]:
        """选择P3可行性论证引擎"""
        candidates = []
        pool = {k: v for k, v in self.p3_pool.items() if k not in query.excluded_engines}

        for engine_id, engine_info in pool.items():
            score, matched_domains = self.domain_matcher.match_engine(
                engine_id, domains, pool
            )
            base_weight = self._get_engine_weight(engine_id, engine_info)

            final_score = self._clamp_unit_score(
                score * 0.6 + base_weight * 0.4,
                0.5
            )

            reason = f"域匹配({score:.2f}) + 权重({base_weight:.2f})"

            candidates.append(TierSelection(
                tier=EngineTier.P3,
                engine_id=engine_id,
                match_score=final_score,
                domains=matched_domains,
                reason=reason
            ))

        # 强制包含
        for req_id in query.required_engines:
            if req_id in pool and not any(c.engine_id == req_id for c in candidates):
                candidates.append(TierSelection(
                    tier=EngineTier.P3,
                    engine_id=req_id,
                    match_score=1.0,
                    domains=[],
                    reason="强制包含"
                ))

        return self._weighted_ranked_selection(candidates, query.p3_count, rng)

    def _weighted_ranked_selection(
        self,
        candidates: List[TierSelection],
        count: int,
        rng: random.Random
    ) -> List[TierSelection]:
        """加权随机选择"""
        if not candidates:
            return []

        # 按分数排序
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x.match_score,
            reverse=True
        )

        # 如果候选数量少于需要数量，返回全部
        if len(sorted_candidates) <= count:
            return sorted_candidates

        # 加权随机选择
        selected = []
        remaining = sorted_candidates.copy()

        for _ in range(count):
            if not remaining:
                break

            # 计算权重
            weights = [c.match_score for c in remaining]
            total_weight = sum(weights)

            if total_weight == 0:
                # 等概率选择
                idx = rng.randint(0, len(remaining) - 1)
            else:
                # 加权随机
                r = rng.random() * total_weight
                cumsum = 0
                idx = 0
                for i, w in enumerate(weights):
                    cumsum += w
                    if r <= cumsum:
                        idx = i
                        break

            selected.append(remaining.pop(idx))

        return selected

    def _get_engine_weight(self, engine_id: str, engine_info: Any) -> float:
        """获取引擎权重"""
        if isinstance(engine_info, dict):
            return float(engine_info.get("weight", 0.5))
        return 0.5

    def _get_engine_domains(self, engine_id: str, engine_info: Any) -> set:
        """获取引擎领域"""
        if isinstance(engine_info, dict):
            domains = engine_info.get("domains", [])
            return set(d.lower() for d in domains) if domains else set()
        return set()

    def _build_workflow_reference_base(
        self,
        query: Tier3Query,
        domains: Dict[str, float]
    ) -> str:
        """构建工作流引用基础"""
        domain_str = "_".join(sorted(domains.keys())[:3]) if domains else "general"
        return f"tier3_{domain_str}_{hash(query.query_text) % 10000}"

    def _build_engine_workflow_reference(
        self,
        base: str,
        tier: str,
        engine_id: str
    ) -> str:
        """构建引擎工作流引用"""
        return f"{base}_{tier}_{engine_id}"

    def _clamp_unit_score(self, value: Any, default: float = 0.5) -> float:
        """将值限制在0-1范围内"""
        try:
            if value is None:
                return default
            v = float(value)
            if v < 0 or v > 1:
                return default
            return v
        except (TypeError, ValueError):
            return default
