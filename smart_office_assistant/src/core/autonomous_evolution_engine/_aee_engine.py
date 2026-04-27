"""autonomous_evolution_engine 主引擎模块 - AutonomousEvolutionEngine主类"""
# 本文件内容由 autonomous_evolution_engine.py 拆分而来

import asyncio
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

from ._aee_base import EvolutionPlan, EvolutionType, SystemHealth
from ._aee_subsystems import (
    SelfDiagnostics, StrategyAutoOptimizer, KnowledgeAutoExpander,
    ArchitectureSelfAdjuster, MultiObjectiveOptimizer, EvolutionVisualizer
)

__all__ = [
    'create_and_start_engine',
    'execute_evolution_plan',
    'get_evolution_report',
    'get_evolution_visualizations',
    'handle_knowledge_expansion',
    'run_diagnostic_cycle',
    'start',
    'stop',
]

logger = logging.getLogger(__name__)

class AutonomousEvolutionEngine:
    """
    自主进化引擎主类 - v2.0 增强版

    实现系统的完全自主优化能力
    - 预测性维护
    - 多目标优化
    - 进化历史可视化
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.diagnostics = SelfDiagnostics()
        self.strategy_optimizer = StrategyAutoOptimizer()
        self.knowledge_expander = KnowledgeAutoExpander()
        self.architecture_adjuster = ArchitectureSelfAdjuster()
        self.multi_objective_optimizer = MultiObjectiveOptimizer()
        self.visualizer = EvolutionVisualizer()

        self.active_plans: List[EvolutionPlan] = []
        self.evolution_history: List[Dict] = []
        self.is_running = False
        self.evolution_thread: Optional[threading.Thread] = None

        self.diagnostic_interval = self.config.get("diagnostic_interval_minutes", 60)
        self.auto_evolution = self.config.get("auto_evolution", True)
        self.risk_threshold = self.config.get("risk_threshold", "medium")
        self.enable_predictive = self.config.get("enable_predictive_maintenance", True)
        self.enable_multi_objective = self.config.get("enable_multi_objective", True)

    async def start(self):
        logger.info("🚀 启动自主进化引擎...")
        self.is_running = True
        await self.run_diagnostic_cycle()
        if self.auto_evolution:
            asyncio.create_task(self._evolution_loop())
        logger.info("✅ 自主进化引擎已启动")

    async def stop(self):
        logger.info("🛑 停止自主进化引擎...")
        self.is_running = False
        logger.info("✅ 自主进化引擎已停止")

    async def _evolution_loop(self):
        while self.is_running:
            try:
                await self.run_diagnostic_cycle()
                await asyncio.sleep(self.diagnostic_interval * 60)
            except Exception as e:
                logger.error(f"进化循环错误: {e}")
                await asyncio.sleep(60)

    async def run_diagnostic_cycle(self):
        logger.info("🔄 运行诊断周期...")
        health = await self.diagnostics.run_full_diagnostic()

        if self.enable_predictive and health.predictions.get("risk_modules"):
            risk_modules = health.predictions["risk_modules"]
            logger.info(f"🔮 预测到 {len(risk_modules)} 个模块存在风险,启动预防性维护")
            for risk in risk_modules:
                plan = self._create_predictive_maintenance_plan(risk)
                self.active_plans.append(plan)

        if not health.is_healthy():
            logger.warning(f"⚠️ 系统健康度不足 ({health.overall_score:.1f}%),启动优化流程")
            strategy_plans = await self.strategy_optimizer.analyze_and_optimize(
                health, health.performance_metrics
            )
            self.active_plans.extend(strategy_plans)
            arch_eval = await self.architecture_adjuster.evaluate_architecture(health.performance_metrics)
            arch_plans = await self.architecture_adjuster.generate_adjustment_plans(arch_eval)
            self.active_plans.extend(arch_plans)

        if health.anomaly_alerts:
            for alert in health.anomaly_alerts:
                if alert["severity"] == "critical":
                    plan = self._create_anomaly_response_plan(alert)
                    self.active_plans.append(plan)

        if self.enable_multi_objective and len(self.active_plans) > 1:
            self.active_plans = self._prioritize_plans_multi_objective(self.active_plans)

        self.evolution_history.append({
            "timestamp": datetime.now().isoformat(),
            "health_score": health.overall_score,
            "trend": health.trend,
            "plans_generated": len(self.active_plans),
            "weak_modules": health.get_weak_modules(),
            "anomaly_count": len(health.anomaly_alerts),
            "risk_modules": len(health.predictions.get("risk_modules", []))
        })

        logger.info(f"✅ 诊断周期完成 - 活跃计划数: {len(self.active_plans)}, 趋势: {health.trend}")
        return health

    def _create_predictive_maintenance_plan(self, risk: Dict) -> EvolutionPlan:
        return EvolutionPlan(
            evolution_id=f"pred_maint_{risk['module']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            evolution_type=EvolutionType.PREDICTIVE_MAINTENANCE,
            target_module=risk["module"],
            current_state={
                "health_score": risk["current"],
                "forecast_score": risk["forecast"],
                "risk_level": risk["risk_level"]
            },
            desired_state={"health_score": 80, "risk_level": "low"},
            action_sequence=[
                {"step": 1, "action": "diagnose_module", "module": risk["module"]},
                {"step": 2, "action": "identify_root_cause"},
                {"step": 3, "action": "apply_preventive_fix"},
                {"step": 4, "action": "validate_improvement"},
                {"step": 5, "action": "schedule_follow_up", "delay_hours": 24}
            ],
            rollback_plan=[
                {"step": 1, "action": "restore_module_state", "module": risk["module"]},
                {"step": 2, "action": "notify_admin", "message": f"预测性维护回滚: {risk['module']}"}
            ],
            expected_improvement={"score_increase": 80 - risk["current"], "risk_mitigation": "high"},
            risk_level="low" if risk["risk_level"] == "medium" else "medium",
            priority=2 if risk["risk_level"] == "high" else 4
        )

    def _create_anomaly_response_plan(self, alert: Dict) -> EvolutionPlan:
        return EvolutionPlan(
            evolution_id=f"anomaly_{alert['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            evolution_type=EvolutionType.QUALITY_IMPROVEMENT,
            target_module=alert.get("module", "system_wide"),
            current_state={
                "alert_type": alert["type"],
                "value": alert["value"],
                "severity": alert["severity"]
            },
            desired_state={"status": "resolved", "value_normalized": True},
            action_sequence=[
                {"step": 1, "action": "acknowledge_alert", "alert": alert},
                {"step": 2, "action": "isolate_affected_component"},
                {"step": 3, "action": "apply_emergency_fix"},
                {"step": 4, "action": "verify_resolution"},
                {"step": 5, "action": "post_incident_review"}
            ],
            rollback_plan=[
                {"step": 1, "action": "revert_emergency_fix"},
                {"step": 2, "action": "escalate_to_manual"}
            ],
            expected_improvement={"issue_resolved": True, "prevention_measures": 1},
            risk_level="high",
            priority=1
        )

    def _prioritize_plans_multi_objective(self, plans: List[EvolutionPlan]) -> List[EvolutionPlan]:
        candidates = []
        for plan in plans:
            candidate = {
                "plan": plan,
                "objective_scores": {
                    "performance": self._estimate_performance_impact(plan),
                    "reliability": self._estimate_reliability_impact(plan),
                    "cost_efficiency": self._estimate_cost_efficiency(plan),
                    "maintainability": self._estimate_maintainability_impact(plan)
                }
            }
            candidates.append(candidate)
        optimized = self.multi_objective_optimizer.optimize(candidates)
        return [c["plan"] for c in optimized]

    def _estimate_performance_impact(self, plan: EvolutionPlan) -> float:
        if plan.evolution_type == EvolutionType.PERFORMANCE_TUNING:
            return 0.9
        elif plan.evolution_type == EvolutionType.STRATEGY_OPTIMIZATION:
            return 0.7
        return 0.5

    def _estimate_reliability_impact(self, plan: EvolutionPlan) -> float:
        if plan.evolution_type in [EvolutionType.PREDICTIVE_MAINTENANCE, EvolutionType.QUALITY_IMPROVEMENT]:
            return 0.9
        return 0.6

    def _estimate_cost_efficiency(self, plan: EvolutionPlan) -> float:
        risk_score = {"low": 0.8, "medium": 0.6, "high": 0.4}.get(plan.risk_level, 0.5)
        duration_factor = max(0, 1 - plan.estimated_duration_minutes / 120)
        return (risk_score + duration_factor) / 2

    def _estimate_maintainability_impact(self, plan: EvolutionPlan) -> float:
        if plan.evolution_type == EvolutionType.ARCHITECTURE_ADJUSTMENT:
            return 0.8
        elif plan.evolution_type == EvolutionType.KNOWLEDGE_EXPANSION:
            return 0.7
        return 0.5

    def get_evolution_visualizations(self) -> Dict:
        return {
            "trend_chart": self.visualizer.generate_trend_chart(self.evolution_history),
            "module_heatmap": self.visualizer.generate_module_heatmap(self.evolution_history),
            "plan_summary": self.visualizer.generate_evolution_summary(self.active_plans)
        }

    async def execute_evolution_plan(self, plan: EvolutionPlan) -> Dict:
        logger.info(f"▶️ 执行进化计划: {plan.evolution_id} (优先级: {plan.priority})")
        plan.status = "executing"
        results = []
        start_time = time.time()

        try:
            for dep_id in plan.dependencies:
                dep_plan = next((p for p in self.active_plans if p.evolution_id == dep_id), None)
                if dep_plan and dep_plan.status not in ["completed", "failed", "rolled_back"]:
                    logger.info(f"⏳ 等待依赖计划完成: {dep_id}")

            for action in plan.action_sequence:
                logger.info(f"  步骤 {action['step']}: {action['action']}")
                result = await self._simulate_action_execution(action)
                results.append(result)
                if not result["success"]:
                    raise RuntimeError(f"步骤 {action['step']} 失败: {result.get('error')}")

            plan.status = "completed"
            execution_time = time.time() - start_time
            plan.actual_results = {
                "execution_time_seconds": execution_time,
                "steps_completed": len(results),
                "completed_at": datetime.now().isoformat()
            }
            plan.lessons_learned.append(f"成功执行,耗时 {execution_time:.1f} 秒")
            logger.info(f"✅ 进化计划完成: {plan.evolution_id} (耗时: {execution_time:.1f}s)")

        except Exception as e:
            logger.error(f"❌ 进化计划失败: {e}")
            plan.status = "failed"
            plan.lessons_learned.append("执行失败")
            await self._rollback_plan(plan)

        return {
            "plan_id": plan.evolution_id,
            "status": plan.status,
            "results": results,
            "execution_time": plan.actual_results.get("execution_time_seconds", 0),
            "lessons_learned": plan.lessons_learned
        }

    async def _simulate_action_execution(self, action: Dict) -> Dict:
        await asyncio.sleep(0.1)
        return {"action": action["action"], "success": True, "timestamp": datetime.now().isoformat()}

    async def _rollback_plan(self, plan: EvolutionPlan):
        logger.warning(f"⏮️ 回滚进化计划: {plan.evolution_id}")
        for action in plan.rollback_plan:
            logger.info(f"  回滚步骤: {action['action']}")
            await asyncio.sleep(0.05)
        plan.status = "rolled_back"
        logger.info(f"✅ 回滚完成: {plan.evolution_id}")

    async def handle_knowledge_expansion(self, query_patterns: List[Dict], failure_cases: List[Dict]) -> List[EvolutionPlan]:
        gaps = await self.knowledge_expander.identify_knowledge_gaps(query_patterns, failure_cases)
        plans = await self.knowledge_expander.generate_expansion_plan(gaps)
        self.active_plans.extend(plans)
        return plans

    def get_evolution_report(self) -> Dict:
        return {
            "total_plans": len(self.active_plans),
            "completed": sum(1 for p in self.active_plans if p.status == "completed"),
            "failed": sum(1 for p in self.active_plans if p.status == "failed"),
            "pending": sum(1 for p in self.active_plans if p.status == "pending"),
            "executing": sum(1 for p in self.active_plans if p.status == "executing"),
            "evolution_history": self.evolution_history[-10:],
            "latest_health": self.evolution_history[-1] if self.evolution_history else None
        }

# ==================== 便捷函数 ====================

async def create_and_start_engine(config: Optional[Dict] = None) -> AutonomousEvolutionEngine:
    """创建并启动自主进化引擎"""
    engine = AutonomousEvolutionEngine(config)
    await engine.start()
    return engine
