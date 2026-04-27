"""
Somn API Server - 知识库路由
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def register_knowledge_routes(app, app_state):
    """注册知识库相关路由"""

    @app.get("/api/v1/knowledge", tags=["知识库"])
    async def list_knowledge(
        page: int = 1,
        page_size: int = 20,
        category: Optional[str] = None,
    ):
        """获取知识库列表"""
        try:
            agent = app_state.get_agent_core()
            items = []

            # AgentCore 的知识库属性名是 self.kb
            kb = agent.kb if hasattr(agent, 'kb') else None
            if kb is not None:
                stats = kb.get_stats() if hasattr(kb, 'get_stats') else {}
                total = stats.get("knowledge_entries", 0)
                # search_knowledge 参数: query, category, tags, limit
                all_items = kb.search_knowledge("", limit=total) if hasattr(kb, 'search_knowledge') else []
                items = all_items
            else:
                total = 0

            # 分页
            offset = (page - 1) * page_size
            paged = items[offset:offset + page_size] if isinstance(items, list) else []

            return {
                "success": True,
                "message": "知识库列表",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "total": total if total else len(items),
                    "page": page,
                    "page_size": page_size,
                    "items": [i.to_dict() if hasattr(i, 'to_dict') else i for i in paged],
                }
            }
        except Exception as e:
            logger.error(f"获取知识列表失败: {e}", exc_info=True)
            return _error_response("获取知识列表失败")

    @app.post("/api/v1/knowledge/search", tags=["知识库"])
    async def search_knowledge(request_body: dict):
        """搜索知识库"""
        query = request_body.get("query", "").strip()
        top_k = request_body.get("top_k", 10)

        if not query:
            return _error_response("搜索关键词不能为空", "EMPTY_QUERY")

        try:
            agent = app_state.get_agent_core()
            results = []

            # AgentCore 属性名是 self.kb
            kb = agent.kb if hasattr(agent, 'kb') else None
            if kb is not None and hasattr(kb, 'search_knowledge'):
                results = kb.search_knowledge(query=query, limit=top_k)

            return {
                "success": True,
                "message": "搜索完成",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "results": [r.to_dict() if hasattr(r, 'to_dict') else r for r in results] if isinstance(results, list) else [],
                    "total": len(results) if isinstance(results, list) else 0,
                }
            }
        except Exception as e:
            logger.error(f"知识搜索失败: {e}", exc_info=True)
            return _error_response("知识搜索失败")

    @app.post("/api/v1/knowledge/add", tags=["知识库"])
    async def add_knowledge(request_body: dict):
        """添加知识条目"""
        title = request_body.get("title", "").strip()
        content = request_body.get("content", "").strip()

        if not title or not content:
            return _error_response("标题和内容不能为空", "INVALID_INPUT")

        try:
            agent = app_state.get_agent_core()
            entry_id = "unknown"

            # AgentCore 属性名是 self.kb
            kb = agent.kb if hasattr(agent, 'kb') else None
            if kb is not None and hasattr(kb, 'add_knowledge'):
                entry = kb.add_knowledge(
                    title=title,
                    content=content,
                    category=request_body.get("category"),
                    source=request_body.get("source"),
                )
                entry_id = entry.id if hasattr(entry, 'id') else str(entry)

            return {
                "success": True,
                "message": "知识添加成功",
                "timestamp": datetime.now().isoformat(),
                "data": {"entry_id": entry_id},
            }
        except Exception as e:
            logger.error(f"添加知识失败: {e}", exc_info=True)
            return _error_response("添加知识失败")


def _error_response(error: str, code: str = "ERROR") -> dict:
    from ..utils import error_response
    return error_response(error, code)
