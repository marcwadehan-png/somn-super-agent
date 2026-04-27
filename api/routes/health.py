"""
Somn API Server - 健康检查 & 系统状态路由
"""

from __future__ import annotations

import logging
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ── Pydantic 响应模型 ──────────────────────────────────
class ComponentsStatus(BaseModel):
    api_server: str
    somn_core: Optional[str] = None

class HealthData(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    components: ComponentsStatus

class HealthResponse(BaseModel):
    success: bool
    message: str
    timestamp: str
    data: HealthData


def register_health_routes(app, app_state):
    """注册健康检查与系统状态路由"""

    @app.get(
        "/api/v1/health",
        tags=["系统"],
        response_model=HealthResponse,
        responses={
            200: {"description": "后端健康检查成功"}
        }
    )
    async def health_check():
        """后端健康检查"""
        uptime = time.time() - app_state.start_time if app_state.start_time else 0

        # 检查各组件状态
        components = {"api_server": "healthy"}

        # 检查 SomnCore 是否可用
        try:
            core = app_state.get_somn_core()
            components["somn_core"] = "healthy"
        except Exception as e:
            logger.debug(f"SomnCore 健康检查异常: {e}")
            components["somn_core"] = "unavailable"

        # 确定整体状态
        unhealthy_count = sum(1 for v in components.values() if v != "healthy")
        status = "healthy" if unhealthy_count == 0 else (
            "degraded" if unhealthy_count < 2 else "unhealthy"
        )

        return {
            "success": True,
            "message": "Somn API Server 运行中" if status == "healthy" else "部分组件异常",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "status": status,
                "version": _get_version(app_state),
                "uptime_seconds": round(uptime, 1),
                "components": components,
            }
        }

    @app.get(
        "/api/v1/status",
        tags=["系统"],
        response_model=None,
        responses={200: {"description": "系统详细状态"}}
    )
    async def system_status():
        """获取系统详细状态"""
        version = _get_version(app_state)
        loaded_modules = []
        wisdom_schools = 0
        engine_count = 0
        mem_mb = 0

        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_mb = round(process.memory_info().rss / 1024 / 1024, 1)
        except ImportError:
            mem_mb = 0

        try:
            core = app_state.get_somn_core()
            # 获取已加载模块信息
            if hasattr(core, 'get_capabilities'):
                caps = core.get_capabilities()
                loaded_modules = caps.get("modules", [])
                wisdom_schools = caps.get("wisdom_schools", 0)
                engine_count = caps.get("engines", 0)
        except Exception as e:
            logger.warning(f"获取SomnCore状态失败: {e}")

        return {
            "success": True,
            "message": "系统状态",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "version": version,
                "environment": "standalone",
                "loaded_modules": loaded_modules[:20],  # 限制数量
                "wisdom_schools_count": wisdom_schools,
                "engine_count": engine_count,
                "memory_usage_mb": mem_mb,
            }
        }

    @app.get(
        "/api/v1/config",
        tags=["系统"],
        response_model=None,
        responses={200: {"description": "前端配置"}}
    )
    async def get_config():
        """获取前端可见的安全配置子集"""
        safe_config = app_state.get_safe_config()
        return {
            "success": True,
            "message": "前端配置",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "config": safe_config,
            }
        }


def _get_version(app_state) -> str:
    """获取当前系统版本"""
    try:
        version_file = app_state.project_root / "smart_office_assistant" / "src" / "core" / "_version.py"
        if version_file.exists():
            content = version_file.read_text(encoding="utf-8")
            match = re.search(r'Somn_VERSION\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except Exception as e:
        logger.debug(f"版本读取失败: {e}")
    return "unknown"
