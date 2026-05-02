"""
Somn API Server - 路由注册入口
"""

from .health import register_health_routes
from .chat import register_chat_routes
from .knowledge import register_knowledge_routes
from .analysis import (
    register_analysis_routes,
    register_document_routes,
    register_wisdom_routes,
    register_memory_routes,
    register_learning_routes,
)
from .admin import register_admin_routes
from .knowledge_cells import router as knowledge_cells_router
from .outputs import register_outputs_routes


def register_all_routes(app, app_state):
    """注册所有API路由"""
    register_health_routes(app, app_state)
    register_chat_routes(app, app_state)
    register_knowledge_routes(app, app_state)
    register_analysis_routes(app, app_state)
    register_document_routes(app, app_state)
    register_wisdom_routes(app, app_state)
    register_memory_routes(app, app_state)
    register_learning_routes(app, app_state)
    register_admin_routes(app, app_state)
    register_outputs_routes(app, app_state)
    
    # 知识格子路由 (独立路由，无需 app_state)
    app.include_router(knowledge_cells_router)
