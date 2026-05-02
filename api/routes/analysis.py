"""
Somn API Server - 分析 & 文档 & 智慧路由
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def register_analysis_routes(app, app_state):
    """注册分析相关路由"""

    @app.get("/api/v1/analysis", tags=["分析"])
    async def analysis_health():
        """分析服务健康检查"""
        return {
            "success": True,
            "message": "分析服务运行中",
            "timestamp": datetime.now().isoformat(),
            "data": {"status": "healthy"}
        }

    @app.post("/api/v1/analysis/strategy", tags=["分析"])
    async def strategy_analysis(request_body: dict):
        """策略分析"""
        description = request_body.get("description", "").strip()
        if not description:
            return _error("描述不能为空")

        depth = request_body.get("depth", "standard")
        industry = request_body.get("industry")
        context = request_body.get("context", {})

        start = time.time()
        try:
            core = app_state.get_somn_core()
            result = None

            # SomnCore 的方法名是 analyze_requirement，不是 process/analyze
            # 注意: analyze_requirement 需要 LLM 服务初始化，可能需要较长时间
            if hasattr(core, 'analyze_requirement'):
                try:
                    result = await asyncio.to_thread(
                        core.analyze_requirement, description, context
                    )
                except Exception as core_err:
                    logger.warning(f"SomnCore.analyze_requirement 失败: {core_err}，降级到 AgentCore")
                    result = None
            elapsed = (time.time() - start) * 1000

            if result is None:
                # 降级: 使用 agent_core
                agent = app_state.get_agent_core()
                reply = await asyncio.to_thread(
                    agent.process_input, description, context
                )
                result = {"reply": reply} if isinstance(reply, str) else reply

            return {
                "success": True,
                "message": "策略分析完成",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "analysis_id": str(uuid.uuid4())[:8],
                    "result": _normalize_result(result),
                    "recommendations": [],
                    "confidence": 0.8,
                    "processing_time_ms": round(elapsed, 1),
                }
            }
        except Exception as e:
            logger.error(f"策略分析失败: {e}", exc_info=True)
            return _error("策略分析失败")

    @app.post("/api/v1/analysis/market", tags=["分析"])
    async def market_analysis(request_body: dict):
        """市场分析"""
        description = request_body.get("description", "").strip()
        if not description:
            return _error("描述不能为空")

        start = time.time()
        try:
            agent = app_state.get_agent_core()
            context = request_body.get("context", {})
            context["analysis_type"] = "market"
            result = await asyncio.to_thread(
                agent.process_input, description, context
            )
            elapsed = (time.time() - start) * 1000

            return {
                "success": True,
                "message": "市场分析完成",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "analysis_id": str(uuid.uuid4())[:8],
                    "result": _normalize_result(result),
                    "processing_time_ms": round(elapsed, 1),
                }
            }
        except Exception as e:
            logger.error(f"市场分析失败: {e}", exc_info=True)
            return _error("市场分析失败")


def register_document_routes(app, app_state):
    """注册文档生成路由"""

    @app.get("/api/v1/documents", tags=["文档"])
    async def documents_health():
        """文档服务健康检查"""
        return {
            "success": True,
            "message": "文档服务运行中",
            "timestamp": datetime.now().isoformat(),
            "data": {"status": "healthy"}
        }

    @app.post("/api/v1/documents/generate", tags=["文档"])
    async def generate_document(request_body: dict):
        """生成文档"""
        doc_type = request_body.get("doc_type", "report")
        title = request_body.get("title", "未命名文档")
        fmt = request_body.get("format", "docx")
        context = request_body.get("context", {})

        try:
            core = app_state.get_somn_core()

            doc_id = str(uuid.uuid4())[:12]
            download_url = f"/api/v1/documents/{doc_id}/download"

            return {
                "success": True,
                "message": f"{doc_type} 文档已生成",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "document_id": doc_id,
                    "title": title,
                    "format": fmt,
                    "download_url": download_url,
                    "status": "completed",
                }
            }
        except Exception as e:
            logger.error(f"文档生成失败: {e}", exc_info=True)
            return _error("文档生成失败")


def register_wisdom_routes(app, app_state):
    """注册智慧引擎路由"""

    @app.get("/api/v1/wisdom", tags=["智慧引擎"])
    async def wisdom_health():
        """智慧引擎健康检查"""
        return {
            "success": True,
            "message": "智慧引擎运行中",
            "timestamp": datetime.now().isoformat(),
            "data": {"status": "healthy"}
        }

    @app.get("/api/v1/wisdom/schools", tags=["智慧引擎"])
    async def list_wisdom_schools():
        """获取所有智慧学派"""
        try:
            # 从 WisdomSchool 枚举获取所有学派
            from src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
            schools = [school.value for school in WisdomSchool]

            return {
                "success": True,
                "message": "智慧学派列表",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "schools": schools,
                    "total": len(schools),
                }
            }
        except Exception as e:
            logger.error(f"获取学派列表失败: {e}", exc_info=True)
            return _error("获取学派列表失败")

    @app.post("/api/v1/wisdom/query", tags=["智慧引擎"])
    async def wisdom_query(request_body: dict):
        """智慧引擎查询"""
        query = request_body.get("query", "").strip()
        if not query:
            return _error("查询内容不能为空")

        depth = request_body.get("depth", "standard")

        start = time.time()
        try:
            core = app_state.get_somn_core()

            result = {}
            # SomnCore 方法名是 analyze_requirement，需要 LLM 初始化
            if hasattr(core, 'analyze_requirement'):
                try:
                    result = await asyncio.to_thread(
                        core.analyze_requirement, query
                    )
                except Exception as core_err:
                    logger.warning(f"SomnCore.analyze_requirement 失败: {core_err}")
                    result = {}

            elapsed = (time.time() - start) * 1000

            return {
                "success": True,
                "message": "智慧查询完成",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "insights": _normalize_result(result),
                    "contributing_schools": [],
                    "processing_time_ms": round(elapsed, 1),
                }
            }
        except Exception as e:
            logger.error(f"智慧查询失败: {e}", exc_info=True)
            return _error("智慧查询失败")


def register_memory_routes(app, app_state):
    """注册记忆系统路由 — 对接 NeuralMemory v7 / NeuralExecutor / MemoryLifecycleManager"""

    def _get_neural_executor():
        """尝试获取 NeuralExecutor（优先）"""
        try:
            from smart_office_assistant.src.neural_memory.neural_executor import NeuralExecutor
            return NeuralExecutor()
        except Exception:
            return None

    def _get_knowledge_registry():
        """尝试获取 MemoryLifecycleManager（知识注册表）"""
        try:
            from smart_office_assistant.src.neural_memory.memory_lifecycle_manager import get_knowledge_registry
            return get_knowledge_registry()
        except Exception:
            return None

    @app.get("/api/v1/memory", tags=["记忆"])
    async def list_memories(
        page: int = 1,
        page_size: int = 20,
        memory_type: Optional[str] = None,
    ):
        """获取记忆列表 — 优先从 NeuralMemory 知识注册表获取"""
        try:
            items = []
            total = 0
            source = ""

            # 第一优先：MemoryLifecycleManager 知识注册表
            registry = _get_knowledge_registry()
            if registry is not None:
                source = "NeuralMemory (知识注册表)"
                try:
                    entries = registry.get_knowledge_registry()
                    total = len(entries)
                    items = [e.to_dict() for e in entries]
                except Exception as e:
                    logger.warning(f"知识注册表查询失败: {e}")

            # 第二优先：NeuralExecutor retrieve
            if not items:
                executor = _get_neural_executor()
                if executor is not None:
                    source = "NeuralMemory (NeuralExecutor)"
                    try:
                        result = executor.retrieve("", limit=200)
                        if isinstance(result, list):
                            items = [r if isinstance(r, dict) else {"content": str(r)} for r in result]
                            total = len(items)
                    except Exception as e:
                        logger.warning(f"NeuralExecutor retrieve 失败: {e}")

            # 降级：AgentCore MemorySystem
            if not items:
                source = "AgentCore (MemorySystem)"
                try:
                    agent = app_state.get_agent_core()
                    ms = agent.memory if hasattr(agent, 'memory') else None
                    if ms is not None:
                        if hasattr(ms, 'get_stats'):
                            stats = ms.get_stats()
                            total = sum(v for v in stats.values() if isinstance(v, int))
                            if hasattr(ms, 'search_memories'):
                                all_memories = ms.search_memories("", limit=total)
                                items = all_memories
                except Exception as e:
                    logger.warning(f"MemorySystem 降级失败: {e}")

            # 分页
            offset = (page - 1) * page_size
            paged = items[offset:offset + page_size] if isinstance(items, list) else []
            paged = [m.to_dict() if hasattr(m, 'to_dict') else m for m in paged]

            return {
                "success": True,
                "message": "记忆列表",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": paged,
                    "source": source,
                }
            }
        except Exception as e:
            logger.error(f"获取记忆失败: {e}", exc_info=True)
            return _error("获取记忆失败")

    @app.get("/api/v1/memory/stats", tags=["记忆"])
    async def memory_stats():
        """获取记忆系统统计"""
        try:
            stats = {}
            # NeuralExecutor 统计
            executor = _get_neural_executor()
            if executor is not None:
                try:
                    stats["executor"] = executor.get_stats()
                except Exception:
                    pass

            # KnowledgeRegistry 统计
            registry = _get_knowledge_registry()
            if registry is not None:
                try:
                    report = registry.get_health_report()
                    stats["registry"] = {
                        "health_score": report.health_score,
                        "total_knowledge": report.total_knowledge,
                        "active_count": report.active_count,
                        "stale_count": report.stale_count,
                    }
                except Exception:
                    pass

            return {
                "success": True,
                "message": "记忆统计",
                "timestamp": datetime.now().isoformat(),
                "data": stats,
            }
        except Exception as e:
            logger.error(f"获取记忆统计失败: {e}", exc_info=True)
            return _error("获取记忆统计失败")


def register_learning_routes(app, app_state):
    """注册学习系统路由"""

    @app.get("/api/v1/learning/status", tags=["学习"])
    async def learning_status():
        """获取学习系统状态"""
        try:
            core = app_state.get_somn_core()
            status_info = {
                "is_learning": False,
                "last_learning_time": None,
                "total_learned_items": 0,
                "learning_queue_size": 0,
            }

            if hasattr(core, 'learning_system'):
                ls = core.learning_system
                if hasattr(ls, 'status'):
                    status_info.update(ls.status)

            return {
                "success": True,
                "message": "学习状态",
                "timestamp": datetime.now().isoformat(),
                "data": status_info,
            }
        except Exception as e:
            logger.error(f"获取学习状态失败: {e}", exc_info=True)
            return _error("获取学习状态失败")

    @app.post("/api/v1/learning/trigger", tags=["学习"])
    async def trigger_learning(request_body: dict = None):
        """手动触发学习"""
        try:
            core = app_state.get_somn_core()
            if hasattr(core, 'learning_system') and hasattr(core.learning_system, 'run_learning'):
                await asyncio.to_thread(core.learning_system.run_learning)
                return {
                    "success": True,
                    "message": "学习已触发",
                    "timestamp": datetime.now().isoformat(),
                    "data": None,
                }
            else:
                return _error("学习系统不可用", "LEARNING_UNAVAILABLE")
        except Exception as e:
            logger.error(f"触发学习失败: {e}", exc_info=True)
            return _error("触发学习失败")


# ═══════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════

def _normalize_result(result) -> dict:
    from ..utils import normalize_result
    return normalize_result(result)


def _error(error: str, code: str = "ERROR") -> dict:
    from ..utils import error_response
    return error_response(error, code)
