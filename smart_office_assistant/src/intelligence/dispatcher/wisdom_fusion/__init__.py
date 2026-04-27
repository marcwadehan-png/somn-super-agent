"""wisdom_fusion package v1.4

[v1.3] 修复__all__列表（fuse_wisdom/get_fusion_insights是方法而非函数）
[v1.4] 修复循环导入（_fusion_core_init/rexecute延迟导入到__init__中）
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional, Tuple

__all__ = [
    # 类和枚举
    'WisdomFusionCore',
    'WisdomPriority', 'FusionMethod',
    'WisdomContribution', 'FusionConfig', 'FusionResult',
    'ShangShanFusionMode', 'ShangShanFusionConfig', 'ShangShanResult', 'ComplementarityScore',
    # 冲突解决
    'ConflictResolver',
]

from ._fusion_enums import (
    FusionMethod, WisdomPriority,
    WisdomContribution, FusionConfig, FusionResult,
    ShangShanFusionMode, ShangShanFusionConfig, ShangShanResult, ComplementarityScore
)
from ._fusion_conflict import ConflictResolver
# 注意: _fusion_core_init 和 _fusion_core_execute 延迟导入（避免循环依赖）

WisdomFusionCoreBase = None

class WisdomFusionCore:
    def __init__(self, config=None):
        # 延迟导入避免循环依赖
        from . import _fusion_core_init as _init_mod
        from . import _fusion_core_execute as _exec_mod

        self._config = config
        self.config = None
        self.wisdom_modules = {}
        self.conflict_resolver = None
        self.fusion_history = []
        self.performance_log = []
        self.fusion_cache = {}
        _init_mod.fusion_core_init(self)

    def _initialize_wisdom_modules(self):
        from . import _fusion_core_init as _init_mod
        _init_mod._initialize_wisdom_modules(self)

    def _log_system_status(self):
        from . import _fusion_core_init as _init_mod
        _init_mod._log_system_status(self)

    def _calculate_domain_relevance(self, module_name, domain):
        from . import _fusion_core_init as _init_mod
        return _init_mod._calculate_domain_relevance(self, module_name, domain)

    def _get_module_performance(self, module_name, task_type):
        from . import _fusion_core_init as _init_mod
        return _init_mod._get_module_performance(self, module_name, task_type)

    def _estimate_problem_complexity(self, context):
        from . import _fusion_core_init as _init_mod
        return _init_mod._estimate_problem_complexity(self, context)

    def fuse_wisdom(self, task_type, problem, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod.fuse_wisdom(self, task_type, problem, context)

    def _select_modules_for_task(self, task_type, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._select_modules_for_task(self, task_type, context)

    def _execute_wisdom_module(self, module_name, task_type, problem, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._execute_wisdom_module(self, module_name, task_type, problem, context)

    def _select_sufu_principle(self, problem, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._select_sufu_principle(self, problem, context)

    def _estimate_confidence(self, module_name, task_type, problem):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._estimate_confidence(self, module_name, task_type, problem)

    def _calculate_relevance(self, module_name, task_type, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._calculate_relevance(self, module_name, task_type, context)

    def _calculate_initial_weight(self, module_name, task_type, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._calculate_initial_weight(self, module_name, task_type, context)

    def _apply_fusion_method(self, contributions, task_type, problem, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._apply_fusion_method(self, contributions, task_type, problem, context)

    def _weighted_average_fusion(self, contributions):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._weighted_average_fusion(self, contributions)

    def _majority_vote_fusion(self, contributions):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._majority_vote_fusion(self, contributions)

    def _meta_learning_fusion(self, contributions, task_type, problem, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._meta_learning_fusion(self, contributions, task_type, problem, context)

    def _adaptive_fusion(self, contributions, task_type, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._adaptive_fusion(self, contributions, task_type, context)

    def _hierarchical_fusion(self, contributions):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._hierarchical_fusion(self, contributions)

    def _calculate_fusion_confidence(self, contributions):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._calculate_fusion_confidence(self, contributions)

    def _calculate_consistency_score(self, contributions):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._calculate_consistency_score(self, contributions)

    def _find_common_keywords_in_contributions(self, contributions):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._find_common_keywords_in_contributions(self, contributions)

    def _calculate_diversity_score(self, contributions):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._calculate_diversity_score(self, contributions)

    def _generate_suggestions(self, contributions, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._generate_suggestions(self, contributions, context)

    def _record_fusion_experience(self, task_id, task_type, contributions, result, context):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod._record_fusion_experience(self, task_id, task_type, contributions, result, context)

    def get_fusion_insights(self, task_type=None):
        from . import _fusion_core_execute as _exec_mod
        return _exec_mod.get_fusion_insights(self, task_type)

    # ── v1.2: 道家上善若水融合方法 ──────────────────────────────────

    def shang_shan_fuse(
        self,
        contributions: list,
        mode: "ShangShanFusionMode" = None,
    ) -> "ShangShanResult":
        """
        [上善若水融合核心] 执行上善若水融合策略——"水善利万物而不争"。

        三种融合模式：
        1. HARMONY_ORIENTED：计算各学派建议的互补性，高互补性获得权重加成
        2. BOUNDARY_TRANSCENDENCE：鼓励跨域影响，不同学派在对方领域获得影响力
        3. FLUID_INTEGRATION：迭代加权，逐步收敛到最优融合权重

        [道家解读] 上善若水——好的融合如水，
        不排斥任何一滴水，也不强制改变任何一滴水的特性，
        而是让所有水滴共同形成江河湖海。
        """
        from ._fusion_enums import ShangShanFusionMode, ShangShanResult, ComplementarityScore

        if mode is None:
            mode = self.config.shang_shan.default_mode

        shang_shan_cfg = self.config.shang_shan

        # 步骤1：计算互补性得分（所有学派两两组合）
        comp_scores: List[ComplementarityScore] = []
        if len(contributions) >= 2:
            for i, c1 in enumerate(contributions):
                for c2 in contributions[i + 1:]:
                    comp = self._compute_complementarity(c1, c2, shang_shan_cfg)
                    comp_scores.append(comp)

        # 步骤2：计算和谐度
        if comp_scores:
            harmony_score = sum(c.complementarity for c in comp_scores) / len(comp_scores)
        else:
            harmony_score = 0.5

        # 步骤3：根据模式执行融合
        if mode == ShangShanFusionMode.HARMONY_ORIENTED:
            fused_weights, harmony_bonus = self._shang_shan_harmony_fusion(contributions, comp_scores, shang_shan_cfg)
            harmony_score = max(harmony_score, shang_shan_cfg.complementarity_threshold)
        elif mode == ShangShanFusionMode.BOUNDARY_TRANSCENDENCE:
            fused_weights = self._shang_shan_boundary_fusion(contributions, shang_shan_cfg)
            harmony_score = harmony_score * 1.1  # 边界超越增强和谐感
        elif mode == ShangShanFusionMode.FLUID_INTEGRATION:
            fused_weights, convergence = self._shang_shan_fluid_fusion(contributions, shang_shan_cfg)
        else:
            # 默认：简单加权平均
            fused_weights = {c.module_name: c.weight for c in contributions}

        # 步骤4：计算阴阳平衡
        yin_yang_balance = self._compute_yin_yang_balance(contributions, fused_weights)

        # 步骤5：生成道家评估
        dao_assessment = self._generate_shang_shan_assessment(
            mode, harmony_score, yin_yang_balance, comp_scores
        )

        return ShangShanResult(
            mode_used=mode,
            fused_weights=fused_weights,
            complementarity_scores=comp_scores,
            harmony_score=harmony_score,
            boundary_transcendence_score=1.0 if mode == ShangShanFusionMode.BOUNDARY_TRANSCENDENCE else 0.7,
            fluid_convergence=1.0 if mode == ShangShanFusionMode.FLUID_INTEGRATION else 0.8,
            yin_yang_balance=yin_yang_balance,
            dao_assessment=dao_assessment,
            water_flow_guidance=shang_shan_cfg.dao_proverb,
        )

    def _compute_complementarity(self, c1, c2, cfg) -> "ComplementarityScore":
        """计算两个学派建议的互补性得分"""
        # 简化实现：基于置信度和相关性的差异计算互补性
        conf_diff = abs(c1.confidence - c2.confidence)
        rel_diff = abs(c1.relevance - c2.relevance)
        # 互补性 = 差异度（差异越大，互补可能性越高）
        complementarity = (conf_diff + rel_diff) / 2.0

        # 和谐加分：互补性超过阈值时获得加成
        harmony_bonus = (
            cfg.harmony_bonus_weight
            if complementarity > cfg.complementarity_threshold
            else 0.0
        )

        # 跨域影响：不同类型的学派有正向影响
        cross_influence = cfg.cross_domain_influence * 0.5  # 简化

        assessment = (
            "【互补】两学派关注点不同，可各司其职。"
            if complementarity > cfg.complementarity_threshold
            else "【重叠】两学派关注点相近，建议合并。"
        )

        return ComplementarityScore(
            school_a=c1.module_name,
            school_b=c2.module_name,
            dimension_a="主维度",
            dimension_b="次维度",
            complementarity=complementarity,
            harmony_bonus=harmony_bonus,
            cross_influence=cross_influence,
            assessment=assessment,
        )

    def _shang_shan_harmony_fusion(self, contributions, comp_scores, cfg) -> Tuple[Dict[str, float], float]:
        """和谐导向融合：互补性得分对权重进行加成"""
        base_weights = {c.module_name: c.weight for c in contributions}
        harmony_bonus_total = 0.0

        for comp in comp_scores:
            if comp.complementarity > cfg.complementarity_threshold:
                # 互补学派各获得加成
                bonus = cfg.harmony_bonus_weight * comp.complementarity
                base_weights[comp.school_a] += bonus
                base_weights[comp.school_b] += bonus
                harmony_bonus_total += bonus * 2

        # 归一化
        total = sum(base_weights.values())
        if total > 0:
            fused = {k: v / total for k, v in base_weights.items()}
        else:
            fused = base_weights

        return fused, harmony_bonus_total / len(contributions)

    def _shang_shan_boundary_fusion(self, contributions, cfg) -> Dict[str, float]:
        """边界超越融合：跨域影响"""
        base_weights = {c.module_name: c.weight for c in contributions}

        # 每个学派对其他学派产生正向跨域影响
        for c in contributions:
            influence = cfg.cross_domain_influence
            for other in contributions:
                if other.module_name != c.module_name:
                    base_weights[other.module_name] += influence * c.weight

        # 归一化
        total = sum(base_weights.values())
        if total > 0:
            return {k: v / total for k, v in base_weights.items()}
        return base_weights

    def _shang_shan_fluid_fusion(self, contributions, cfg) -> Tuple[Dict[str, float], float]:
        """流式整合融合：迭代加权收敛"""
        weights = {c.module_name: c.weight for c in contributions}

        for iteration in range(cfg.fluid_iteration_count):
            # 计算当前权重分布的均匀度（越均匀越好）
            values = list(weights.values())
            mean_val = sum(values) / len(values) if values else 1
            variance = sum((v - mean_val) ** 2 for v in values) / len(values) if values else 0

            # 收敛判断
            if variance < cfg.fluid_convergence_threshold:
                break

            # 迭代调整：向均值收敛，同时保留原始差异
            adjustment_factor = 0.5
            for k in weights:
                weights[k] = weights[k] * (1 - adjustment_factor) + mean_val * adjustment_factor

        # 最终归一化
        total = sum(weights.values())
        if total > 0:
            return {k: v / total for k, v in weights.items()}, 1.0 - variance
        return weights, 0.0

    def _compute_yin_yang_balance(self, contributions, fused_weights) -> float:
        """计算融合结果的阴阳平衡度"""
        if not fused_weights:
            return 0.5

        # 简化评估：基于权重分布的均匀度
        values = list(fused_weights.values())
        mean_val = sum(values) / len(values) if values else 1
        if mean_val == 0:
            return 0.5

        # 偏离度（越偏离均值说明越偏重某一学派）
        deviations = [abs(v - mean_val) for v in values]
        avg_deviation = sum(deviations) / len(deviations)
        normalized_deviation = avg_deviation / mean_val if mean_val > 0 else 0

        # 平衡度 = 1 - 偏离度
        balance = max(0.0, min(1.0, 1.0 - normalized_deviation))

        # 阴阳评分：0.5为最平衡
        return 0.3 + balance * 0.4  # 范围0.3-0.7（避免极端）

    def _generate_shang_shan_assessment(
        self, mode, harmony_score, yin_yang_balance, comp_scores
    ) -> str:
        """生成上善若水道家评估"""
        parts = []

        if harmony_score > 0.6:
            parts.append("【上善若水】学派建议互补性强，融合和谐。")
        elif harmony_score > 0.3:
            parts.append("【水波微澜】学派建议有一定互补，可融合。")
        else:
            parts.append("【静水如镜】学派建议重叠较多，需关注重复。")

        if yin_yang_balance > 0.55:
            parts.append("【阳气充盈】融合偏向某些学派，注意包容。")
        elif yin_yang_balance < 0.45:
            parts.append("【阴气内敛】融合较为保守，可适当开放。")
        else:
            parts.append("【阴阳平衡】融合策略较为中道。")

        complementary_pairs = [c for c in comp_scores if c.complementarity > 0.4]
        if complementary_pairs:
            parts.append(f"发现{len(complementary_pairs)}对高互补性学派，建议在后续融合中保持各自特色。")

        return " ".join(parts)

    def get_shang_shan_status(self) -> dict:
        """获取上善若水融合状态"""
        if self.config is None:
            return {"enabled": False}
        return {
            "enabled": self.config.shang_shan.shang_shan_enabled,
            "default_mode": self.config.shang_shan.default_mode.value,
            "dao_proverb": self.config.shang_shan.dao_proverb,
            "config": {
                "complementarity_threshold": self.config.shang_shan.complementarity_threshold,
                "harmony_bonus_weight": self.config.shang_shan.harmony_bonus_weight,
                "cross_domain_influence": self.config.shang_shan.cross_domain_influence,
                "fluid_iteration_count": self.config.shang_shan.fluid_iteration_count,
            },
        }

def get_wisdom_fusion_core():
    return WisdomFusionCore()
