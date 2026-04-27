"""
Somn API Server - 系统管理路由
暴露后端核心管理能力：引擎加载、LLM管理、链路监控、
自主进化、记忆生命周期、Claw调度、系统监控。
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Query

logger = logging.getLogger(__name__)


def register_admin_routes(app, app_state):
    """注册系统管理路由"""

    # ═══════════════════════════════════════════════════════════
    # 1. 引擎加载管理 (GlobalLoadManager)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/load-manager/stats", tags=["管理-加载"])
    async def load_manager_stats():
        """获取加载管理器统计"""
        try:
            from src.core.global_load_manager import get_global_load_manager
            mgr = get_global_load_manager()
            stats = mgr.get_stats()
            return _ok("加载统计", data=stats)
        except Exception as e:
            logger.error(f"获取加载统计失败: {e}")
            return _error(f"获取加载统计失败: {e}")

    @app.get("/api/v1/admin/load-manager/status", tags=["管理-加载"])
    async def load_manager_status():
        """获取所有模块加载状态"""
        try:
            from src.core.global_load_manager import get_global_load_manager
            mgr = get_global_load_manager()
            modules = []
            for name, info in mgr._registry.items():
                modules.append({
                    "name": name,
                    "status": mgr._load_status.get(name, "pending"),
                    "strategy": info["strategy"].value,
                    "priority": info["priority"].name,
                    "loaded_at": info.get("loaded_at"),
                    "load_time_ms": round(mgr._load_times.get(name, 0), 2),
                })
            return _ok("模块状态", data={
                "total": len(modules),
                "loaded": len(mgr._cache),
                "modules": modules,
            })
        except Exception as e:
            logger.error(f"获取模块状态失败: {e}")
            return _error(f"获取模块状态失败: {e}")

    @app.post("/api/v1/admin/load-manager/preload", tags=["管理-加载"])
    async def preload_modules(request_body: dict):
        """预加载指定模块"""
        names = request_body.get("names", [])
        if not names:
            return _error("模块名称列表不能为空")
        try:
            from src.core.global_load_manager import get_global_load_manager
            mgr = get_global_load_manager()
            results = {}
            for name in names:
                try:
                    mgr.preload_now([name])
                    results[name] = "loaded"
                except Exception as e:
                    results[name] = f"failed: {e}"
            return _ok("预加载完成", data=results)
        except Exception as e:
            logger.error(f"预加载失败: {e}")
            return _error(f"预加载失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 2. LLM管理 (LocalLLMManager)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/llm/status", tags=["管理-LLM"])
    async def llm_status():
        """获取LLM管理器状态"""
        try:
            from src.core.local_llm_manager import get_manager
            mgr = get_manager(auto_start=False)
            status = mgr.get_status()
            return _ok("LLM状态", data=status)
        except Exception as e:
            logger.error(f"获取LLM状态失败: {e}")
            return _error(f"获取LLM状态失败: {e}")

    @app.post("/api/v1/admin/llm/start", tags=["管理-LLM"])
    async def llm_start():
        """启动LLM引擎"""
        try:
            from src.core.local_llm_manager import get_manager
            mgr = get_manager(auto_start=False)
            success = await asyncio.to_thread(mgr.start, 30.0)
            return _ok("LLM启动" if success else "LLM启动失败",
                       data={"success": success})
        except Exception as e:
            logger.error(f"LLM启动失败: {e}")
            return _error(f"LLM启动失败: {e}")

    @app.post("/api/v1/admin/llm/stop", tags=["管理-LLM"])
    async def llm_stop():
        """停止LLM引擎"""
        try:
            from src.core.local_llm_manager import get_manager
            mgr = get_manager(auto_start=False)
            mgr.stop()
            return _ok("LLM已停止")
        except Exception as e:
            logger.error(f"LLM停止失败: {e}")
            return _error(f"LLM停止失败: {e}")

    @app.get("/api/v1/admin/llm/sessions", tags=["管理-LLM"])
    async def llm_sessions():
        """获取LLM会话列表"""
        try:
            from src.core.local_llm_manager import get_manager
            mgr = get_manager(auto_start=False)
            sessions = {}
            for sid in list(mgr._conversation_history.keys()):
                history = mgr.get_session_history(sid)
                sessions[sid] = {
                    "message_count": len(history),
                    "last_message": history[-1].get("user", "")[:50] if history else "",
                }
            return _ok("LLM会话", data={"total": len(sessions), "sessions": sessions})
        except Exception as e:
            logger.error(f"获取会话失败: {e}")
            return _error(f"获取会话失败: {e}")

    @app.delete("/api/v1/admin/llm/sessions/{session_id}", tags=["管理-LLM"])
    async def llm_clear_session(session_id: str):
        """清除指定会话"""
        try:
            from src.core.local_llm_manager import get_manager
            mgr = get_manager(auto_start=False)
            mgr.clear_session(session_id)
            return _ok(f"会话 {session_id} 已清除")
        except Exception as e:
            logger.error(f"清除会话失败: {e}")
            return _error(f"清除会话失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 3. 主链路监控 (MainChainMonitor)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/chain/full-status", tags=["管理-链路"])
    async def chain_full_status():
        """获取主链路完整状态"""
        try:
            from src.main_chain.main_chain_monitor import get_main_chain_monitor
            monitor = get_main_chain_monitor()
            status = monitor.get_full_status()
            return _ok("主链路状态", data=status)
        except Exception as e:
            logger.error(f"获取链路状态失败: {e}")
            return _error(f"获取链路状态失败: {e}")

    @app.get("/api/v1/admin/chain/health", tags=["管理-链路"])
    async def chain_health():
        """获取链路健康状态"""
        try:
            from src.main_chain.main_chain_monitor import get_main_chain_monitor
            monitor = get_main_chain_monitor()
            health = monitor.get_chain_health()
            return _ok("链路健康", data=health)
        except Exception as e:
            logger.error(f"获取链路健康失败: {e}")
            return _error(f"获取链路健康失败: {e}")

    @app.get("/api/v1/admin/chain/nodes", tags=["管理-链路"])
    async def chain_nodes():
        """获取节点状态"""
        try:
            from src.main_chain.main_chain_monitor import get_main_chain_monitor
            monitor = get_main_chain_monitor()
            nodes = monitor.get_node_status()
            return _ok("节点状态", data={"nodes": nodes, "total": len(nodes)})
        except Exception as e:
            logger.error(f"获取节点状态失败: {e}")
            return _error(f"获取节点状态失败: {e}")

    @app.get("/api/v1/admin/chain/modes", tags=["管理-链路"])
    async def chain_modes():
        """获取模式分布"""
        try:
            from src.main_chain.main_chain_monitor import get_main_chain_monitor
            monitor = get_main_chain_monitor()
            modes = monitor.get_mode_distribution()
            return _ok("模式分布", data=modes)
        except Exception as e:
            logger.error(f"获取模式分布失败: {e}")
            return _error(f"获取模式分布失败: {e}")

    @app.get("/api/v1/admin/chain/report", tags=["管理-链路"])
    async def chain_report():
        """生成监控报告"""
        try:
            from src.main_chain.main_chain_monitor import get_main_chain_monitor
            monitor = get_main_chain_monitor()
            report = monitor.generate_report()
            return _ok("监控报告", data={"report": report})
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return _error(f"生成报告失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 4. 自主进化 (AutonomousEvolutionEngine)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/evolution/report", tags=["管理-进化"])
    async def evolution_report():
        """获取进化报告"""
        try:
            from src.core.autonomous_evolution_engine import AutonomousEvolutionEngine
            engine = AutonomousEvolutionEngine()
            report = engine.get_evolution_report()
            return _ok("进化报告", data=report)
        except Exception as e:
            logger.error(f"获取进化报告失败: {e}")
            return _error(f"获取进化报告失败: {e}")

    @app.post("/api/v1/admin/evolution/diagnose", tags=["管理-进化"])
    async def evolution_diagnose():
        """运行诊断周期"""
        try:
            from src.core.autonomous_evolution_engine import AutonomousEvolutionEngine
            engine = AutonomousEvolutionEngine()
            health = await asyncio.to_thread(engine.diagnostics.run_full_diagnostic.__wrapped__)
            health_dict = {
                "overall_score": health.overall_score,
                "trend": health.trend,
                "module_health": health.module_health,
                "performance_metrics": health.performance_metrics,
                "quality_metrics": health.quality_metrics,
                "anomaly_alerts": health.anomaly_alerts,
                "predictions": health.predictions,
                "is_healthy": health.is_healthy(),
            }
            return _ok("诊断完成", data=health_dict)
        except Exception as e:
            logger.error(f"运行诊断失败: {e}")
            return _error(f"运行诊断失败: {e}")

    @app.get("/api/v1/admin/evolution/plans", tags=["管理-进化"])
    async def evolution_plans():
        """获取活跃进化计划"""
        try:
            from src.core.autonomous_evolution_engine import AutonomousEvolutionEngine
            engine = AutonomousEvolutionEngine()
            plans = [
                {
                    "id": p.evolution_id,
                    "type": p.evolution_type.value,
                    "target": p.target_module,
                    "status": p.status,
                    "priority": p.priority,
                    "risk": p.risk_level,
                    "created_at": str(p.created_at),
                }
                for p in engine.active_plans
            ]
            return _ok("进化计划", data={"plans": plans, "total": len(plans)})
        except Exception as e:
            logger.error(f"获取进化计划失败: {e}")
            return _error(f"获取进化计划失败: {e}")

    @app.get("/api/v1/admin/evolution/visualizations", tags=["管理-进化"])
    async def evolution_visualizations():
        """获取进化可视化数据"""
        try:
            from src.core.autonomous_evolution_engine import AutonomousEvolutionEngine
            engine = AutonomousEvolutionEngine()
            viz = engine.get_evolution_visualizations()
            return _ok("进化可视化", data=viz)
        except Exception as e:
            logger.error(f"获取可视化失败: {e}")
            return _error(f"获取可视化失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 5. 记忆生命周期 (MemoryLifecycleManager)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/memory/health", tags=["管理-记忆"])
    async def memory_health():
        """获取知识库健康报告"""
        try:
            from src.neural_memory.memory_lifecycle_manager import get_knowledge_registry
            mgr = get_knowledge_registry()
            report = mgr.get_health_report()
            return _ok("记忆健康", data={
                "health_score": report.health_score,
                "health_status": report.health_status,
                "total_knowledge": report.total_knowledge,
                "active_count": report.active_count,
                "stale_count": report.stale_count,
                "weak_count": report.weak_count,
                "reviewing_count": report.reviewing_count,
                "avg_confidence": round(report.avg_confidence, 4),
                "avg_importance": round(report.avg_importance, 4),
                "avg_age_days": round(report.avg_age_days, 1),
                "recommendations": report.recommendations,
                "weak_knowledge": report.weak_knowledge,
            })
        except Exception as e:
            logger.error(f"获取记忆健康失败: {e}")
            return _error(f"获取记忆健康失败: {e}")

    @app.get("/api/v1/admin/memory/registry", tags=["管理-记忆"])
    async def memory_registry(
        category: Optional[str] = None,
        status: Optional[str] = None,
        min_confidence: float = 0.0,
        page: int = 1,
        page_size: int = 20,
    ):
        """获取知识注册表"""
        try:
            from src.neural_memory.memory_lifecycle_manager import (
                get_knowledge_registry, KnowledgeStatus,
            )
            mgr = get_knowledge_registry()

            status_enum = None
            if status:
                try:
                    status_enum = KnowledgeStatus(status)
                except ValueError:
                    pass

            entries = mgr.get_knowledge_registry(
                category=category,
                status=status_enum,
                min_confidence=min_confidence,
            )

            total = len(entries)
            offset = (page - 1) * page_size
            paged = entries[offset:offset + page_size]

            return _ok("知识注册表", data={
                "total": total,
                "page": page,
                "page_size": page_size,
                "items": [e.to_dict() for e in paged],
            })
        except Exception as e:
            logger.error(f"获取知识注册表失败: {e}")
            return _error(f"获取知识注册表失败: {e}")

    @app.get("/api/v1/admin/memory/review-tasks", tags=["管理-记忆"])
    async def memory_review_tasks(
        max_tasks: int = Query(default=10, ge=1, le=50),
        category: Optional[str] = None,
    ):
        """获取复习任务"""
        try:
            from src.neural_memory.memory_lifecycle_manager import get_knowledge_registry
            mgr = get_knowledge_registry()
            tasks = mgr.trigger_review(max_tasks=max_tasks, category=category)
            return _ok("复习任务", data={
                "tasks": [
                    {
                        "knowledge_id": t.knowledge_id,
                        "concept": t.concept,
                        "confidence": t.current_confidence,
                        "days_since": t.days_since_access,
                        "priority": round(t.priority, 3),
                        "reason": t.reason,
                    }
                    for t in tasks
                ],
                "total": len(tasks),
            })
        except Exception as e:
            logger.error(f"获取复习任务失败: {e}")
            return _error(f"获取复习任务失败: {e}")

    @app.post("/api/v1/admin/memory/decay", tags=["管理-记忆"])
    async def memory_apply_decay(request_body: dict):
        """手动触发记忆衰减"""
        force = request_body.get("force", False)
        try:
            from src.neural_memory.memory_lifecycle_manager import get_knowledge_registry
            mgr = get_knowledge_registry()
            results = await asyncio.to_thread(mgr.apply_decay, force=force)
            return _ok("衰减完成", data={
                "affected_count": len(results),
                "results": results,
            })
        except Exception as e:
            logger.error(f"衰减失败: {e}")
            return _error(f"衰减失败: {e}")

    @app.post("/api/v1/admin/memory/reinforce", tags=["管理-记忆"])
    async def memory_reinforce(request_body: dict):
        """强化指定知识"""
        knowledge_id = request_body.get("knowledge_id", "")
        boost = request_body.get("boost", 0.1)
        if not knowledge_id:
            return _error("knowledge_id 不能为空")
        try:
            from src.neural_memory.memory_lifecycle_manager import get_knowledge_registry
            mgr = get_knowledge_registry()
            entry = mgr.reinforce_knowledge(knowledge_id, boost=boost)
            if entry:
                return _ok("知识强化完成", data=entry.to_dict())
            return _error("知识不存在")
        except Exception as e:
            logger.error(f"知识强化失败: {e}")
            return _error(f"知识强化失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 6. Claw调度 (GlobalClawScheduler)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/claw/stats", tags=["管理-Claw"])
    async def claw_stats():
        """获取Claw调度器统计"""
        try:
            from src.intelligence.claws._global_claw_scheduler import get_global_claw_scheduler
            scheduler = get_global_claw_scheduler()
            stats = scheduler.get_stats()
            return _ok("Claw统计", data={
                "total_dispatched": stats.total_dispatched,
                "total_completed": stats.total_completed,
                "total_failed": stats.total_failed,
                "total_collaborative": stats.total_collaborative,
                "total_distributed": stats.total_distributed,
                "total_single": stats.total_single,
                "avg_response_time": round(stats.avg_response_time, 3),
                "active_tasks": stats.active_tasks,
                "pool_size": stats.pool_size,
                "top_claws": sorted(
                    stats.claw_usage_counts.items(),
                    key=lambda x: -x[1]
                )[:10],
            })
        except Exception as e:
            logger.error(f"获取Claw统计失败: {e}")
            return _error(f"获取Claw统计失败: {e}")

    @app.get("/api/v1/admin/claw/work-pool", tags=["管理-Claw"])
    async def claw_work_pool():
        """获取工作池状态"""
        try:
            from src.intelligence.claws._global_claw_scheduler import get_global_claw_scheduler
            scheduler = get_global_claw_scheduler()
            pool = scheduler.get_work_pool_status()
            return _ok("工作池状态", data={
                "total_claws": pool.total_claws,
                "loaded_claws": pool.loaded_claws,
                "active_claws": pool.active_claws,
                "departments": pool.departments,
                "schools": pool.schools,
                "top_busy": pool.top_busy[:10],
            })
        except Exception as e:
            logger.error(f"获取工作池失败: {e}")
            return _error(f"获取工作池失败: {e}")

    @app.get("/api/v1/admin/claw/list", tags=["管理-Claw"])
    async def claw_list(
        department: Optional[str] = None,
        school: Optional[str] = None,
        limit: int = Query(default=50, ge=1, le=200),
    ):
        """列出可用Claw"""
        try:
            from src.intelligence.claws._global_claw_scheduler import get_global_claw_scheduler
            scheduler = get_global_claw_scheduler()
            claws = scheduler.list_available_claws(
                department=department,
                school=school,
                limit=limit,
            )
            return _ok("Claw列表", data={"claws": claws, "total": len(claws)})
        except Exception as e:
            logger.error(f"列出Claw失败: {e}")
            return _error(f"列出Claw失败: {e}")

    @app.get("/api/v1/admin/claw/recent", tags=["管理-Claw"])
    async def claw_recent(limit: int = Query(default=20, ge=1, le=100)):
        """获取最近执行结果"""
        try:
            from src.intelligence.claws._global_claw_scheduler import get_global_claw_scheduler
            scheduler = get_global_claw_scheduler()
            results = scheduler.get_recent_results(limit=limit)
            return _ok("最近结果", data={"results": results, "total": len(results)})
        except Exception as e:
            logger.error(f"获取最近结果失败: {e}")
            return _error(f"获取最近结果失败: {e}")

    @app.get("/api/v1/admin/claw/active-tasks", tags=["管理-Claw"])
    async def claw_active_tasks():
        """获取活跃任务"""
        try:
            from src.intelligence.claws._global_claw_scheduler import get_global_claw_scheduler
            scheduler = get_global_claw_scheduler()
            tasks = scheduler.get_active_tickets()
            return _ok("活跃任务", data={"tasks": tasks, "total": len(tasks)})
        except Exception as e:
            logger.error(f"获取活跃任务失败: {e}")
            return _error(f"获取活跃任务失败: {e}")

    @app.post("/api/v1/admin/claw/dispatch", tags=["管理-Claw"])
    async def claw_dispatch(request_body: dict):
        """调度Claw执行任务"""
        query = request_body.get("query", "").strip()
        claw_name = request_body.get("claw_name")
        department = request_body.get("department")
        school = request_body.get("school")
        collaborators = request_body.get("collaborators")

        if not query:
            return _error("查询内容不能为空")

        try:
            from src.intelligence.claws._global_claw_scheduler import (
                get_global_claw_scheduler, TaskTicket,
            )
            scheduler = get_global_claw_scheduler()

            if not scheduler._initialized:
                await asyncio.to_thread(asyncio.run, scheduler.initialize())

            ticket = TaskTicket.create(
                query=query,
                target_claw=claw_name,
                collaborators=collaborators or [],
                department=department,
                wisdom_school=school,
            )

            result = await asyncio.wait_for(
                scheduler.dispatch(ticket),
                timeout=180.0,
            )
            return _ok("Claw调度完成", data={
                "task_id": result.task_id,
                "success": result.success,
                "claw_used": result.claw_used,
                "answer": result.answer[:500] if result.answer else "",
                "elapsed": round(result.elapsed_seconds, 2),
                "confidence": round(result.confidence, 2),
                "error": result.error,
            })
        except asyncio.TimeoutError:
            return _error("Claw调度超时(180s)")
        except Exception as e:
            logger.error(f"Claw调度失败: {e}")
            return _error(f"Claw调度失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 7. 系统监控 (SystemMonitor)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/status", tags=["管理-系统"])
    async def admin_status():
        """获取系统全局状态（简洁摘要）"""
        try:
            core = app_state.get_somn_core()
            from src.core.somn_components.system_status.monitor import SystemMonitor
            monitor = SystemMonitor(somn_core=core)
            status = monitor.get_status()

            # 额外补充运行时长
            uptime_info = {}
            try:
                from src.core.global_load_manager import get_global_load_manager
                mgr = get_global_load_manager()
                uptime_info = {"loaded_modules": len(mgr._cache), "total_modules": len(mgr._registry)}
            except Exception:
                pass

            return _ok("系统状态", data={
                "uptime": uptime_info,
                "components": status,
            })
        except Exception as e:
            logger.error(f"获取系统状态失败: {e}")
            return _error(f"获取系统状态失败: {e}")

    @app.get("/api/v1/admin/system/components", tags=["管理-系统"])
    async def system_components():
        """获取所有组件状态"""
        try:
            core = app_state.get_somn_core()
            from src.core.somn_components.system_status.monitor import SystemMonitor
            monitor = SystemMonitor(somn_core=core)
            status = monitor.get_status()
            return _ok("组件状态", data=status)
        except Exception as e:
            logger.error(f"获取组件状态失败: {e}")
            return _error(f"获取组件状态失败: {e}")

    @app.get("/api/v1/admin/system/component/{component_name}", tags=["管理-系统"])
    async def system_component_health(component_name: str):
        """获取指定组件健康状态"""
        try:
            core = app_state.get_somn_core()
            from src.core.somn_components.system_status.monitor import SystemMonitor
            monitor = SystemMonitor(somn_core=core)
            health = monitor.get_component_health(component_name)
            return _ok(f"组件 {component_name}", data=health)
        except Exception as e:
            logger.error(f"获取组件健康失败: {e}")
            return _error(f"获取组件健康失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 7.5 神经网络布局管理
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/neural/status", tags=["管理-神经网络"])
    async def neural_layout_status():
        """获取神经网络布局状态（含 Phase 系统）"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            summary = mgr.get_manager_summary()
            return _ok("神经网络布局状态", data=summary)
        except Exception as e:
            logger.error(f"获取布局状态失败: {e}")
            return _error(f"获取布局状态失败: {e}")

    @app.get("/api/v1/admin/neural/topology", tags=["管理-神经网络"])
    async def neural_topology():
        """获取网络拓扑结构"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            if not mgr.initialized:
                mgr.initialize_global_layout()
            topology = mgr.get_layout_status()
            return _ok("网络拓扑", data=topology)
        except Exception as e:
            logger.error(f"获取网络拓扑失败: {e}")
            return _error(f"获取网络拓扑失败: {e}")

    @app.get("/api/v1/admin/neural/phase-status", tags=["管理-神经网络"])
    async def neural_phase_status():
        """获取 Phase 1-5 系统状态"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            phase = mgr.get_phase_status()
            return _ok("Phase 系统状态", data=phase)
        except Exception as e:
            logger.error(f"获取 Phase 状态失败: {e}")
            return _error(f"获取 Phase 状态失败: {e}")

    @app.post("/api/v1/admin/neural/activate", tags=["管理-神经网络"])
    async def neural_activate(request: dict = None):
        """手动激活主链路"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            input_data = request or {"query": "手动激活测试", "timestamp": datetime.now().isoformat()}
            result = mgr.activate_main_chain(input_data)
            return _ok("主链路激活完成", data=result)
        except Exception as e:
            logger.error(f"主链路激活失败: {e}")
            return _error(f"主链路激活失败: {e}")

    @app.post("/api/v1/admin/neural/optimize-clusters", tags=["管理-神经网络"])
    async def neural_optimize_clusters():
        """优化所有集群连接"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            results = mgr.optimize_clusters()
            return _ok("集群优化完成", data={"optimized": len(results), "results": results})
        except Exception as e:
            logger.error(f"集群优化失败: {e}")
            return _error(f"集群优化失败: {e}")

    @app.get("/api/v1/admin/neural/execution-history", tags=["管理-神经网络"])
    async def neural_execution_history(limit: int = Query(20, ge=1, le=100)):
        """获取执行历史"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            history = mgr.get_execution_history(limit)
            return _ok("执行历史", data=history)
        except Exception as e:
            logger.error(f"获取执行历史失败: {e}")
            return _error(f"获取执行历史失败: {e}")

    @app.get("/api/v1/admin/neural/bridge-status", tags=["管理-神经网络"])
    async def neural_bridge_status():
        """获取全局神经桥梁状态"""
        try:
            from src.neural_layout import get_global_neural_bridge, get_bound_modules
            bridge = get_global_neural_bridge()
            status = bridge.get_bridge_status()
            status["bound_real_modules"] = get_bound_modules()
            return _ok("桥梁状态", data=status)
        except Exception as e:
            logger.error(f"获取桥梁状态失败: {e}")
            return _error(f"获取桥梁状态失败: {e}")

    @app.get("/api/v1/admin/neural/layouts", tags=["管理-神经网络"])
    async def neural_list_layouts():
        """列出所有布局"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            layouts = mgr.list_layouts()
            return _ok("布局列表", data=layouts)
        except Exception as e:
            logger.error(f"获取布局列表失败: {e}")
            return _error(f"获取布局列表失败: {e}")

    @app.post("/api/v1/admin/neural/layouts", tags=["管理-神经网络"])
    async def neural_create_layout(request: dict = None):
        """创建新布局"""
        try:
            from src.neural_layout.neural_layout_manager import LayoutConfig, get_layout_manager
            mgr = get_layout_manager()
            config_data = request or {}
            config = LayoutConfig(
                layout_id=config_data.get("layout_id", ""),
                name=config_data.get("name", ""),
                description=config_data.get("description", ""),
                neurons=config_data.get("neurons", []),
                synapses=config_data.get("synapses", []),
                optimization_level=config_data.get("optimization_level", 3),
            )
            result = mgr.create_layout(config)
            return _ok("布局创建成功", data=result)
        except Exception as e:
            logger.error(f"创建布局失败: {e}")
            return _error(f"创建布局失败: {e}")

    @app.put("/api/v1/admin/neural/layouts/{layout_id}/switch", tags=["管理-神经网络"])
    async def neural_switch_layout(layout_id: str):
        """切换活跃布局"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            ok = mgr.switch_layout(layout_id)
            if ok:
                return _ok(f"已切换到布局: {layout_id}", data={"active_layout": layout_id})
            else:
                return _error(f"布局不存在或切换失败: {layout_id}")
        except Exception as e:
            logger.error(f"切换布局失败: {e}")
            return _error(f"切换布局失败: {e}")

    @app.delete("/api/v1/admin/neural/layouts/{layout_id}", tags=["管理-神经网络"])
    async def neural_delete_layout(layout_id: str):
        """删除指定布局（不能删除活跃/默认布局）"""
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            ok = mgr.delete_layout(layout_id)
            if ok:
                return _ok(f"已删除布局: {layout_id}", data={"deleted": layout_id})
            else:
                return _error(f"布局不存在或不可删除: {layout_id}")
        except Exception as e:
            logger.error(f"删除布局失败: {e}")
            return _error(f"删除布局失败: {e}")

    @app.get("/api/v1/admin/neural/visualize", tags=["管理-神经网络"])
    async def neural_visualize(vtype: str = "topology"):
        """生成网络可视化（topology=实时拓扑, heatmap=激活热力图）"""
        try:
            from src.neural_layout import get_layout_manager
            from src.neural_layout.visualizer import NetworkVisualizer

            mgr = get_layout_manager()
            if not mgr.initialized:
                mgr.initialize_global_layout()

            viz = NetworkVisualizer(mgr.network)
            phase_status = None
            try:
                phase_status = mgr.get_phase_status()
            except Exception as e:
                logger.debug(f"可视化获取 phase_status 失败: {e}")

            if vtype == "heatmap":
                html = viz.generate_activation_heatmap_html()
            else:
                html = viz.generate_realtime_topology_html(phase_status=phase_status)

            return _ok("可视化 HTML", data={"html_length": len(html), "type": vtype})
        except Exception as e:
            logger.error(f"生成可视化失败: {e}")
            return _error(f"生成可视化失败: {e}")

    # ═══════════════════════════════════════════════════════════
    # 8. 告警管理 (AlertManager)
    # ═══════════════════════════════════════════════════════════

    @app.get("/api/v1/admin/alerts/history", tags=["管理-告警"])
    async def alerts_history(
        limit: int = Query(default=50, ge=1, le=500),
        level: Optional[str] = Query(default=None, description="WARNING/CRITICAL/INFO"),
    ):
        """获取告警历史"""
        try:
            from smart_office_assistant.src.utils.alert_manager import get_alert_manager, AlertLevel

            mgr = get_alert_manager()
            level_filter = None
            if level:
                try:
                    level_filter = AlertLevel(level.lower())
                except ValueError:
                    pass

            alerts = mgr.get_history(limit=limit, level=level_filter)

            return _ok("告警历史", data={
                "total": len(alerts),
                "alerts": [
                    {
                        "timestamp": a.timestamp,
                        "level": a.level.value,
                        "source": a.source,
                        "message": a.message,
                        "details": a.details,
                    }
                    for a in alerts
                ],
            })
        except Exception as e:
            logger.error(f"获取告警历史失败: {e}")
            return _error(f"获取告警历史失败: {e}")

    @app.get("/api/v1/admin/alerts/stats", tags=["管理-告警"])
    async def alerts_stats():
        """获取告警统计"""
        try:
            from smart_office_assistant.src.utils.alert_manager import get_alert_manager

            mgr = get_alert_manager()
            stats = mgr.get_stats()

            return _ok("告警统计", data=stats)
        except Exception as e:
            logger.error(f"获取告警统计失败: {e}")
            return _error(f"获取告警统计失败: {e}")

    @app.delete("/api/v1/admin/alerts/clear", tags=["管理-告警"])
    async def alerts_clear(
        level: Optional[str] = Query(default=None, description="按级别清除，不传则全部清除"),
    ):
        """清除告警历史"""
        try:
            from smart_office_assistant.src.utils.alert_manager import get_alert_manager, AlertLevel

            mgr = get_alert_manager()
            level_filter = None
            if level:
                try:
                    level_filter = AlertLevel(level.lower())
                except ValueError:
                    pass

            count = mgr.clear_history(level=level_filter)

            return _ok("告警已清除", data={"cleared": count})
        except Exception as e:
            logger.error(f"清除告警失败: {e}")
            return _error(f"清除告警失败: {e}")

    @app.post("/api/v1/admin/alerts/trigger", tags=["管理-告警"])
    async def alerts_trigger(request_body: dict):
        """手动触发告警（测试用）"""
        level = request_body.get("level", "WARNING")
        source = request_body.get("source", "manual")
        message = request_body.get("message", "手动触发测试告警")
        details = request_body.get("details")

        try:
            from smart_office_assistant.src.utils.alert_manager import trigger_alert, AlertLevel

            try:
                alert_level = AlertLevel(level.lower())
            except ValueError:
                alert_level = AlertLevel.WARNING

            # trigger_alert 返回 bool，表示是否成功触发
            triggered = trigger_alert(
                level=alert_level,
                source=source,
                message=message,
                details=details,
                force=True,  # 手动触发使用 force=True 确保必定触发
            )

            if triggered:
                return _ok("告警已触发", data={
                    "level": alert_level.value,
                    "source": source,
                    "message": message,
                })
            else:
                return _ok("告警被冷却限制，未触发", data={"cooldown": True})

        except Exception as e:
            logger.error(f"触发告警失败: {e}")
            return _error(f"触发告警失败: {e}")

    @app.get("/api/v1/admin/dashboard", tags=["管理-概览"])
    async def admin_dashboard():
        """全局管理仪表盘 — 一次性获取所有管理数据摘要"""
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "load_manager": None,
            "llm": None,
            "chain": None,
            "evolution": None,
            "memory": None,
            "claw": None,
            "system": None,
            "neural": None,
        }

        # 加载管理器
        try:
            from src.core.global_load_manager import get_global_load_manager
            dashboard["load_manager"] = get_global_load_manager().get_stats()
        except Exception as e:
            logger.debug(f"Dashboard 加载管理器数据获取失败: {e}")
            dashboard["load_manager"] = {"error": "加载管理器数据获取失败"}

        # LLM
        try:
            from src.core.local_llm_manager import get_manager
            dashboard["llm"] = get_manager(auto_start=False).get_status()
        except Exception as e:
            logger.debug(f"Dashboard LLM 数据获取失败: {e}")
            dashboard["llm"] = {"error": "LLM数据获取失败"}

        # 链路
        try:
            from src.main_chain.main_chain_monitor import get_main_chain_monitor
            dashboard["chain"] = get_main_chain_monitor().get_chain_health()
        except Exception as e:
            logger.debug(f"Dashboard 链路数据获取失败: {e}")
            dashboard["chain"] = {"error": "链路数据获取失败"}

        # 进化
        try:
            from src.core.autonomous_evolution_engine import AutonomousEvolutionEngine
            engine = AutonomousEvolutionEngine()
            dashboard["evolution"] = engine.get_evolution_report()
        except Exception as e:
            logger.debug(f"Dashboard 进化数据获取失败: {e}")
            dashboard["evolution"] = {"error": "进化数据获取失败"}

        # 记忆
        try:
            from src.neural_memory.memory_lifecycle_manager import get_knowledge_registry
            report = get_knowledge_registry().get_health_report()
            dashboard["memory"] = {
                "health_score": report.health_score,
                "health_status": report.health_status,
                "total_knowledge": report.total_knowledge,
                "recommendations": report.recommendations,
            }
        except Exception as e:
            logger.debug(f"Dashboard 记忆数据获取失败: {e}")
            dashboard["memory"] = {"error": "记忆数据获取失败"}

        # Claw
        try:
            from src.intelligence.claws._global_claw_scheduler import get_global_claw_scheduler
            scheduler = get_global_claw_scheduler()
            stats = scheduler.get_stats()
            dashboard["claw"] = {
                "total_dispatched": stats.total_dispatched,
                "total_completed": stats.total_completed,
                "total_failed": stats.total_failed,
                "active_tasks": stats.active_tasks,
            }
        except Exception as e:
            logger.debug(f"Dashboard Claw 数据获取失败: {e}")
            dashboard["claw"] = {"error": "Claw数据获取失败"}

        # 系统组件
        try:
            core = app_state.get_somn_core()
            from src.core.somn_components.system_status.monitor import SystemMonitor
            monitor = SystemMonitor(somn_core=core)
            dashboard["system"] = monitor.get_status()
        except Exception as e:
            logger.debug(f"Dashboard 系统组件数据获取失败: {e}")
            dashboard["system"] = {"error": "系统组件数据获取失败"}

        # 神经网络布局
        try:
            from src.neural_layout import get_layout_manager
            mgr = get_layout_manager()
            dashboard["neural"] = mgr.get_manager_summary()
        except Exception as e:
            logger.debug(f"Dashboard 神经网络数据获取失败: {e}")
            dashboard["neural"] = {"error": "神经网络数据获取失败"}

        return _ok("管理仪表盘", data=dashboard)


# ═══════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════

def _ok(message: str, data: Any = None) -> dict:
    return {
        "success": True,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "data": data,
    }


def _error(error: str, code: str = "ERROR") -> dict:
    return {
        "success": False,
        "message": error,
        "error_code": code,
        "timestamp": datetime.now().isoformat(),
        "data": None,
    }
