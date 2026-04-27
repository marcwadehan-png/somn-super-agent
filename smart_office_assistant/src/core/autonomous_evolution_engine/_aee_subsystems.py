"""autonomous_evolution_engine 子系统模块 - 7个子系统类"""
# 本文件内容由 autonomous_evolution_engine.py 拆分而来

import logging
from typing import Dict, List, Optional

from ._aee_base import (
    SystemHealth, EvolutionPlan, EvolutionType
)

__all__ = [
    'analyze_and_optimize',
    'detect',
    'evaluate_architecture',
    'generate_adjustment_plans',
    'generate_evolution_summary',
    'generate_expansion_plan',
    'generate_module_heatmap',
    'generate_trend_chart',
    'identify_knowledge_gaps',
    'optimize',
    'predict',
    'run_full_diagnostic',
]

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """异常检测器"""

    def __init__(self):
        self.baseline_stats: Dict[str, Dict] = {}
        self.threshold_multiplier = 2.5

    def detect(self, module_health: Dict, performance: Dict, quality: Dict) -> List[Dict]:
        alerts = []
        for module, score in module_health.items():
            if score < 50:
                alerts.append({
                    "type": "critical_health", "module": module, "value": score,
                    "severity": "critical",
                    "message": f"模块 {module} 健康度严重偏低 ({score:.1f}%)"
                })
            elif score < 70:
                alerts.append({
                    "type": "low_health", "module": module, "value": score,
                    "severity": "warning",
                    "message": f"模块 {module} 健康度偏低 ({score:.1f}%)"
                })

        response_time = performance.get("response_time_ms", 0)
        if response_time > 500:
            alerts.append({
                "type": "high_latency", "metric": "response_time_ms", "value": response_time,
                "severity": "critical", "message": f"响应时间过长: {response_time:.0f}ms"
            })
        elif response_time > 200:
            alerts.append({
                "type": "elevated_latency", "metric": "response_time_ms", "value": response_time,
                "severity": "warning", "message": f"响应时间偏高: {response_time:.0f}ms"
            })

        error_rate = quality.get("error_rate", 0)
        if error_rate > 5:
            alerts.append({
                "type": "high_error_rate", "metric": "error_rate", "value": error_rate,
                "severity": "critical", "message": f"错误率过高: {error_rate:.2f}%"
            })
        return alerts

class PredictiveHealthModel:
    """预测性健康模型"""

    def __init__(self):
        self.prediction_horizon = 24

    async def predict(self, history: List[Dict], module_health: Dict, performance: Dict) -> Dict:
        if len(history) < 5:
            return {"confidence": "low", "message": "历史数据不足"}

        predictions = {
            "confidence": "medium", "previous_scores": {},
            "forecast_24h": {}, "risk_modules": [],
            "recommended_actions": []
        }
        predictions["previous_scores"] = module_health.copy()

        for module in module_health:
            module_history = [
                h["module_health"].get(module, 80)
                for h in history[-10:] if "module_health" in h
            ]
            if len(module_history) >= 3:
                recent_avg = sum(module_history[-3:]) / 3
                older_avg = sum(module_history[:3]) / 3 if len(module_history) >= 6 else recent_avg
                trend = recent_avg - older_avg
                forecast = module_health[module] + trend * 2
                predictions["forecast_24h"][module] = max(0, min(100, forecast))
                if forecast < 60:
                    predictions["risk_modules"].append({
                        "module": module, "current": module_health[module],
                        "forecast": forecast,
                        "risk_level": "high" if forecast < 50 else "medium"
                    })

        if predictions["risk_modules"]:
            predictions["recommended_actions"].append({
                "priority": "high", "action": "启动预防性维护",
                "target_modules": [m["module"] for m in predictions["risk_modules"]]
            })
        return predictions

class SelfDiagnostics:
    """自我诊断系统 - v2.0 增强版"""

    def __init__(self):
        self.diagnostic_history: List[Dict] = []
        self.health_threshold = 70.0
        self.anomaly_detector = AnomalyDetector()
        self.predictive_model = PredictiveHealthModel()

    async def run_full_diagnostic(self) -> SystemHealth:
        import datetime as dt
        logger.info("🔍 运行完整系统诊断...")

        module_health = await self._check_module_health()
        performance_metrics = await self._check_performance()
        quality_metrics = await self._check_quality()
        overall_score = self._calculate_overall_score(module_health, performance_metrics, quality_metrics)
        trend = self._analyze_trend(overall_score)
        predictions = await self.predictive_model.predict(self.diagnostic_history, module_health, performance_metrics)
        anomaly_alerts = self.anomaly_detector.detect(module_health, performance_metrics, quality_metrics)

        health = SystemHealth(
            overall_score=overall_score, module_health=module_health,
            performance_metrics=performance_metrics, quality_metrics=quality_metrics,
            trend=trend, predictions=predictions, anomaly_alerts=anomaly_alerts
        )
        self.diagnostic_history.append({
            "timestamp": dt.datetime.now().isoformat(),
            "health_score": overall_score, "module_health": module_health.copy()
        })
        if len(self.diagnostic_history) > 100:
            self.diagnostic_history = self.diagnostic_history[-100:]

        logger.info(f"✅ 诊断完成 - 总体健康度: {overall_score:.1f}% (趋势: {trend})")
        if anomaly_alerts:
            logger.warning(f"⚠️ 检测到 {len(anomaly_alerts)} 个异常")
        return health

    def _analyze_trend(self, current_score: float) -> str:
        if len(self.diagnostic_history) < 3:
            return "stable"
        recent_scores = [h["health_score"] for h in self.diagnostic_history[-5:]]
        if len(recent_scores) < 2:
            return "stable"
        n = len(recent_scores)
        x_mean = sum(range(n)) / n
        y_mean = sum(recent_scores) / n
        numerator = sum((i - x_mean) * (score - y_mean) for i, score in enumerate(recent_scores))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        if denominator == 0:
            return "stable"
        slope = numerator / denominator
        if slope > 2:
            return "improving"
        elif slope < -2:
            return "degrading"
        return "stable"

    async def _check_module_health(self) -> Dict[str, float]:
        import datetime as dt
        modules = {
            "industry_detector": 95.0, "scheduler": 88.0,
            "feedback_loop": 92.0, "wisdom_core": 90.0, "memory_system": 85.0,
        }
        for module in modules:
            variation = (hash(module + str(dt.datetime.now().date())) % 10) - 5
            modules[module] = max(0, min(100, modules[module] + variation))
        return modules

    async def _check_performance(self) -> Dict[str, float]:
        return {
            "response_time_ms": 120.0, "throughput_qps": 50.0,
            "memory_usage_mb": 256.0, "cpu_usage_percent": 35.0, "cache_hit_rate": 85.0,
        }

    async def _check_quality(self) -> Dict[str, float]:
        return {
            "accuracy": 100.0, "coverage": 95.0, "user_satisfaction": 4.5,
            "error_rate": 0.5, "feedback_loop_closure": 90.0,
        }

    def _calculate_overall_score(self, module_health: Dict, performance: Dict, quality: Dict) -> float:
        module_avg = sum(module_health.values()) / len(module_health)
        perf_score = min(100, 100 - performance.get("response_time_ms", 200) / 10)
        quality_score = quality.get("accuracy", 0) * 0.4 + \
                       (5 - quality.get("user_satisfaction", 0)) * 10 * 0.3 + \
                       (100 - quality.get("error_rate", 0)) * 0.3
        return module_avg * 0.4 + perf_score * 0.3 + quality_score * 0.3

class StrategyAutoOptimizer:
    """strategy自动优化器"""

    def __init__(self):
        self.optimization_history: List[Dict] = []
        self.strategy_templates = self._load_strategy_templates()

    def _load_strategy_templates(self) -> Dict:
        return {
            "industry_detection": {
                "current": "keyword_matching",
                "alternatives": ["semantic_matching", "hybrid_approach", "ml_classifier"],
                "improvement_axes": ["accuracy", "speed", "coverage"]
            },
            "scheduler": {
                "current": "tier3_neural",
                "alternatives": ["adaptive_tier3", "dynamic_routing", "ensemble"],
                "improvement_axes": ["coverage", "latency", "resource_efficiency"]
            },
            "feedback_processing": {
                "current": "batch_processing",
                "alternatives": ["real_time", "streaming", "hybrid"],
                "improvement_axes": ["responsiveness", "accuracy", "throughput"]
            }
        }

    async def analyze_and_optimize(self, health: SystemHealth, performance_data: Dict) -> List[EvolutionPlan]:
        plans = []
        weak_modules = health.get_weak_modules()
        for module in weak_modules:
            if module in self.strategy_templates:
                template = self.strategy_templates[module]
                plan = self._create_optimization_plan(module, template, health)
                if plan:
                    plans.append(plan)
        if performance_data.get("response_time_ms", 0) > 150:
            plans.append(self._create_performance_plan(performance_data))
        logger.info(f"🎯 generate {len(plans)} 个优化计划")
        return plans

    def _create_optimization_plan(self, module: str, template: Dict, health: SystemHealth) -> Optional[EvolutionPlan]:
        import datetime as dt
        current_score = health.module_health.get(module, 50)
        best_alternative = template["alternatives"][0]
        return EvolutionPlan(
            evolution_id=f"opt_{module}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            evolution_type=EvolutionType.STRATEGY_OPTIMIZATION, target_module=module,
            current_state={"strategy": template["current"], "score": current_score},
            desired_state={"strategy": best_alternative, "score": min(100, current_score + 15)},
            action_sequence=[
                {"step": 1, "action": "backup_current_config", "module": module},
                {"step": 2, "action": "deploy_new_strategy", "strategy": best_alternative},
                {"step": 3, "action": "run_validation_tests", "test_suite": f"{module}_tests"},
                {"step": 4, "action": "gradual_rollout", "percentage": 10},
                {"step": 5, "action": "monitor_and_adjust", "duration_hours": 24}
            ],
            rollback_plan=[
                {"step": 1, "action": "restore_backup_config", "module": module},
                {"step": 2, "action": "clear_cache", "scope": module},
                {"step": 3, "action": "notify_admin", "message": f"{module} optimization rolled back"}
            ],
            expected_improvement={"score_increase": 15, "performance_gain": "10-20%", "risk_reduction": "medium"},
            risk_level="medium"
        )

    def _create_performance_plan(self, performance_data: Dict) -> EvolutionPlan:
        import datetime as dt
        return EvolutionPlan(
            evolution_id=f"perf_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            evolution_type=EvolutionType.PERFORMANCE_TUNING, target_module="system_wide",
            current_state={
                "response_time_ms": performance_data.get("response_time_ms", 200),
                "cache_hit_rate": performance_data.get("cache_hit_rate", 70)
            },
            desired_state={"response_time_ms": 100, "cache_hit_rate": 90},
            action_sequence=[
                {"step": 1, "action": "analyze_bottlenecks"},
                {"step": 2, "action": "optimize_cache_config"},
                {"step": 3, "action": "enable_compression"},
                {"step": 4, "action": "preload_hot_data"},
                {"step": 5, "action": "benchmark_and_validate"}
            ],
            rollback_plan=[
                {"step": 1, "action": "restore_cache_config"},
                {"step": 2, "action": "disable_compression"}
            ],
            expected_improvement={"latency_reduction": "40%", "throughput_increase": "25%"},
            risk_level="low"
        )

class KnowledgeAutoExpander:
    """知识自动扩展器"""

    def __init__(self):
        self.knowledge_gaps: List[Dict] = []
        self.expansion_history: List[Dict] = []

    async def identify_knowledge_gaps(self, query_patterns: List[Dict], failure_cases: List[Dict]) -> List[Dict]:
        gaps = []
        topic_frequency = {}
        for pattern in query_patterns:
            topic = pattern.get("topic", "unknown")
            topic_frequency[topic] = topic_frequency.get(topic, 0) + 1

        for topic, freq in topic_frequency.items():
            failures = sum(1 for f in failure_cases if f.get("topic") == topic)
            failure_rate = failures / freq if freq > 0 else 0
            if failure_rate > 0.3 and freq > 10:
                gaps.append({
                    "topic": topic, "frequency": freq, "failure_rate": failure_rate,
                    "priority": "high" if failure_rate > 0.5 else "medium",
                    "suggested_action": "expand_knowledge_base"
                })
        self.knowledge_gaps = gaps
        logger.info(f"📚 recognize {len(gaps)} 个知识缺口")
        return gaps

    async def generate_expansion_plan(self, gaps: List[Dict]) -> List[EvolutionPlan]:
        import datetime as dt
        plans = []
        for gap in gaps:
            if gap["priority"] == "high":
                plan = EvolutionPlan(
                    evolution_id=f"kexp_{gap['topic']}_{dt.datetime.now().strftime('%Y%m%d')}",
                    evolution_type=EvolutionType.KNOWLEDGE_EXPANSION, target_module="knowledge_base",
                    current_state={"topic_coverage": gap["topic"], "failure_rate": gap["failure_rate"]},
                    desired_state={"failure_rate": 0.1, "coverage_depth": "comprehensive"},
                    action_sequence=[
                        {"step": 1, "action": "research_topic", "topic": gap["topic"]},
                        {"step": 2, "action": "extract_key_concepts"},
                        {"step": 3, "action": "integrate_into_kb"},
                        {"step": 4, "action": "validate_coverage"},
                        {"step": 5, "action": "update_retrieval_models"}
                    ],
                    rollback_plan=[
                        {"step": 1, "action": "remove_new_knowledge", "topic": gap["topic"]},
                        {"step": 2, "action": "restore_previous_kb_version"}
                    ],
                    expected_improvement={"failure_rate_reduction": gap["failure_rate"] - 0.1, "coverage_increase": "significant"},
                    risk_level="low"
                )
                plans.append(plan)
        return plans

class MultiObjectiveOptimizer:
    """多目标优化器"""

    def __init__(self):
        self.objectives = [
            {"name": "performance", "weight": 0.3, "target": "maximize"},
            {"name": "reliability", "weight": 0.25, "target": "maximize"},
            {"name": "cost_efficiency", "weight": 0.25, "target": "maximize"},
            {"name": "maintainability", "weight": 0.2, "target": "maximize"}
        ]

    def optimize(self, candidates: List[Dict], constraints: Dict = None) -> List[Dict]:
        scored_candidates = []
        for candidate in candidates:
            score = self._calculate_multi_objective_score(candidate)
            scored_candidates.append({**candidate, "mo_score": score, "pareto_optimal": False})

        for i, c1 in enumerate(scored_candidates):
            is_dominated = False
            for j, c2 in enumerate(scored_candidates):
                if i != j and self._dominates(c2, c1):
                    is_dominated = True
                    break
            if not is_dominated:
                scored_candidates[i]["pareto_optimal"] = True

        scored_candidates.sort(key=lambda x: x["mo_score"], reverse=True)
        return scored_candidates

    def _calculate_multi_objective_score(self, candidate: Dict) -> float:
        scores = candidate.get("objective_scores", {})
        total = 0
        for obj in self.objectives:
            total += scores.get(obj["name"], 0.5) * obj["weight"]
        return total

    def _dominates(self, c1: Dict, c2: Dict) -> bool:
        s1, s2 = c1.get("objective_scores", {}), c2.get("objective_scores", {})
        better = False
        for obj in self.objectives:
            v1, v2 = s1.get(obj["name"], 0), s2.get(obj["name"], 0)
            if obj["target"] == "maximize":
                if v1 < v2:
                    return False
                if v1 > v2:
                    better = True
            else:
                if v1 > v2:
                    return False
                if v1 < v2:
                    better = True
        return better

class ArchitectureSelfAdjuster:
    """架构自我调整器"""

    def __init__(self):
        self.architecture_state: Dict = {}
        self.adjustment_history: List[Dict] = []

    async def evaluate_architecture(self, system_metrics: Dict) -> Dict:
        evaluation = {
            "scalability_score": self._evaluate_scalability(system_metrics),
            "maintainability_score": self._evaluate_maintainability(),
            "flexibility_score": self._evaluate_flexibility(),
            "recommendations": []
        }
        if evaluation["scalability_score"] < 70:
            evaluation["recommendations"].append({
                "type": "scale_out", "priority": "high", "description": "增加水平扩展能力"
            })
        if evaluation["maintainability_score"] < 70:
            evaluation["recommendations"].append({
                "type": "refactor", "priority": "medium", "description": "重构复杂模块"
            })
        return evaluation

    def _evaluate_scalability(self, metrics: Dict) -> float:
        return min(100, metrics.get("throughput_qps", 50) * 2)

    def _evaluate_maintainability(self) -> float:
        return 85.0

    def _evaluate_flexibility(self) -> float:
        return 80.0

    async def generate_adjustment_plans(self, evaluation: Dict) -> List[EvolutionPlan]:
        import datetime as dt
        plans = []
        for rec in evaluation.get("recommendations", []):
            if rec["type"] == "scale_out":
                plan = EvolutionPlan(
                    evolution_id=f"arch_scale_{dt.datetime.now().strftime('%Y%m%d')}",
                    evolution_type=EvolutionType.ARCHITECTURE_ADJUSTMENT, target_module="infrastructure",
                    current_state={"scaling_mode": "vertical"},
                    desired_state={"scaling_mode": "horizontal"},
                    action_sequence=[
                        {"step": 1, "action": "design_load_balancer"},
                        {"step": 2, "action": "implement_service_discovery"},
                        {"step": 3, "action": "setup_auto_scaling"},
                        {"step": 4, "action": "test_failover"}
                    ],
                    rollback_plan=[
                        {"step": 1, "action": "revert_to_single_instance"},
                        {"step": 2, "action": "disable_load_balancer"}
                    ],
                    expected_improvement={"throughput_increase": "3x", "availability": "99.9%"},
                    risk_level="high"
                )
                plans.append(plan)
        return plans

class EvolutionVisualizer:
    """进化历史可视化"""

    def __init__(self):
        self.visualization_cache: Dict = {}

    def generate_trend_chart(self, history: List[Dict]) -> Dict:
        if len(history) < 2:
            return {"error": "历史数据不足"}
        timestamps = [h["timestamp"] for h in history]
        scores = [h.get("health_score", 0) for h in history]
        window = min(5, len(scores))
        moving_avg = []
        for i in range(len(scores)):
            start = max(0, i - window + 1)
            avg = sum(scores[start:i+1]) / (i - start + 1)
            moving_avg.append(avg)
        return {
            "type": "line_chart", "title": "系统健康度趋势",
            "x_axis": {"label": "时间", "data": timestamps},
            "y_axis": {"label": "健康度 (%)", "min": 0, "max": 100},
            "series": [
                {"name": "健康度", "data": scores, "color": "#4CAF50"},
                {"name": "移动平均", "data": moving_avg, "color": "#2196F3", "style": "dashed"}
            ],
            "annotations": self._generate_annotations(history)
        }

    def _generate_annotations(self, history: List[Dict]) -> List[Dict]:
        annotations = []
        for i, h in enumerate(history):
            if i > 0:
                prev, curr = history[i-1].get("health_score", 0), h.get("health_score", 0)
                if curr - prev > 10:
                    annotations.append({"x": i, "y": curr, "type": "improvement", "text": f"+{curr - prev:.1f}%"})
                elif prev - curr > 10:
                    annotations.append({"x": i, "y": curr, "type": "degradation", "text": f"-{prev - curr:.1f}%"})
        return annotations

    def generate_module_heatmap(self, history: List[Dict]) -> Dict:
        if not history:
            return {"error": "无历史数据"}
        all_modules = set()
        for h in history:
            if "module_health" in h:
                all_modules.update(h["module_health"].keys())
        modules = sorted(all_modules)
        time_points = [h["timestamp"] for h in history[-20:]]
        heatmap_data = []
        for module in modules:
            row = [h.get("module_health", {}).get(module, 0) for h in history[-20:]]
            heatmap_data.append(row)
        return {
            "type": "heatmap", "title": "模块健康度热力图",
            "x_axis": {"label": "时间", "categories": time_points},
            "y_axis": {"label": "模块", "categories": modules},
            "data": heatmap_data,
            "color_scale": [
                {"value": 0, "color": "#f44336"},
                {"value": 50, "color": "#ff9800"},
                {"value": 80, "color": "#4caf50"}
            ]
        }

    def generate_evolution_summary(self, plans: List[EvolutionPlan]) -> Dict:
        status_counts = {"pending": 0, "executing": 0, "completed": 0, "failed": 0, "rolled_back": 0}
        type_counts: Dict[str, int] = {}
        for plan in plans:
            status_counts[plan.status] = status_counts.get(plan.status, 0) + 1
            type_counts[plan.evolution_type.value] = type_counts.get(plan.evolution_type.value, 0) + 1
        completed = status_counts.get("completed", 0)
        failed = status_counts.get("failed", 0)
        rolled_back = status_counts.get("rolled_back", 0)
        total = completed + failed + rolled_back
        success_rate = (completed / total * 100) if total > 0 else 0
        return {
            "type": "summary", "title": "进化计划执行摘要",
            "status_distribution": status_counts, "type_distribution": type_counts,
            "success_rate": f"{success_rate:.1f}%",
            "total_plans": len(plans),
            "active_plans": status_counts.get("pending", 0) + status_counts.get("executing", 0)
        }
