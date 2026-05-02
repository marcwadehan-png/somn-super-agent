"""
Somn API Server - FastAPI 应用入口
提供 RESTful API + WebSocket 实时通信服务
"""

from __future__ import annotations

import json
import logging
import os
import sys
import tempfile
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    """FastAPI lifespan: 管理启动和关闭"""
    # ── 启动 ──
    _registry_cfg = getattr(app.state, "_registry_cfg", {})
    if _registry_cfg.get("auto_register", True):
        _project_root = getattr(app.state, "_project_root", None)
        _config = getattr(app.state, "_config", {})
        if _project_root:
            _register_service(_project_root, _config)

    yield

    # ── 关闭 ──
    _unregister_service()
    
    # 关闭应用状态（停止系统监控等）
    _app_state = getattr(app.state, "_app_state", None)
    if _app_state:
        try:
            _app_state.shutdown()
            logger.info("[生命周期] 应用状态已关闭")
        except Exception as e:
            logger.warning(f"[生命周期] 关闭应用状态时出错: {e}")


def create_app(project_root: Path = None, config: dict = None) -> "FastAPI":
    """
    创建 FastAPI 应用实例

    Args:
        project_root: Somn 项目根目录 (自动检测)
        config: 服务器配置字典 (从 server_config.yaml 加载)

    Returns:
        FastAPI 应用实例
    """
    # ── 检测项目根 ──
    if project_root is None:
        project_root = _detect_project_root()

    # 确保 smart_office_assistant/src 能被导入
    soa_root = project_root / "smart_office_assistant"
    if soa_root.exists() and str(soa_root) not in sys.path:
        sys.path.insert(0, str(soa_root))

    # ── 加载配置 ──
    if config is None:
        config = _load_server_config(project_root)

    server_cfg = config.get("server", {})
    cors_origins = server_cfg.get("cors_origins", ["*"])

    # ── 创建 FastAPI 应用 ──
    try:
        from fastapi import FastAPI
    except ImportError:
        logger.error("FastAPI 未安装，请执行: pip install fastapi uvicorn")
        sys.exit(1)

    app = FastAPI(
        title="Somn API Server",
        description="Somn 智能助手 - 后端API服务",
        version="v6.2.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # ── 配置中间件 ──
    from .middleware import setup_cors_middleware, request_timing_middleware
    setup_cors_middleware(app, cors_origins)
    app.middleware("http")(request_timing_middleware)
    
    # 添加超时保护、请求频率限制、内存泄漏检测中间件
    from .middleware import setup_middlewares
    setup_middlewares(app)

    # ── 初始化应用状态 ──
    from .deps import init_app_state
    app_state = init_app_state(project_root, config)

    # 将配置存到 app.state 供 lifespan 使用
    app.state._project_root = project_root
    app.state._config = config
    app.state._registry_cfg = config.get("registry", {})

    # ── 预热 SomnCore (设置 sys.path) ──
    try:
        _ = app_state.get_somn_core()
    except Exception as e:
        logger.warning(f"SomnCore 预热失败 (将在首次请求时重试): {e}")

    # ── 注册所有路由 ──
    from .routes import register_all_routes
    register_all_routes(app, app_state)

    # ── 保存 app_state 到 app.state ──
    app.state._app_state = app_state

    # ── 挂载静态文件 + 前端页面 ──
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles

    static_dir = project_root / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    async def serve_index():
        """前端单页应用入口"""
        index_path = project_root / "static" / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"message": "Somn API Server v6.2.0", "docs": "/api/docs"}

    # ── 详细健康检查端点 ──
    @app.get("/api/v1/health/detail")
    async def health_check_detail():
        """详细健康检查端点"""
        import os
        import time
        
        result = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": time.time() - app_state.start_time if app_state.start_time else -1,
        }
        
        # 尝试获取系统信息（需要 psutil）
        try:
            import psutil
            
            # 系统信息
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            result["system"] = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": memory.available / 1024 / 1024,
                "disk_percent": disk.percent,
            }
            
            # 进程信息
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info()
            
            result["process"] = {
                "pid": os.getpid(),
                "memory_mb": process_memory.rss / 1024 / 1024,
                "cpu_percent": process.cpu_percent(interval=0.1),
                "threads": process.num_threads(),
            }
        except ImportError:
            # psutil 未安装，提供简化信息
            result["system"] = {"note": "psutil not installed, system info unavailable"}
            result["process"] = {"pid": os.getpid()}
        
        # 初始化状态
        result["initialization"] = {
            "somn_core_loaded": app_state._somn_core is not None,
            "agent_core_loaded": app_state._agent_core is not None,
        }
        
        # 系统资源监控状态
        try:
            from src.system_monitor import get_system_monitor
            monitor = get_system_monitor()
            result["system_resources"] = monitor.get_status()
        except Exception as e:
            result["system_resources"] = {"error": str(e)}
        
        return result

    # ── 系统资源监控端点 ──
    @app.get("/api/v1/system/resources")
    async def get_system_resources():
        """获取系统资源使用情况"""
        try:
            from src.system_monitor import get_system_monitor
            monitor = get_system_monitor()
            return {
                "success": True,
                "data": monitor.get_status(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    # ── 更新系统资源阈值端点 ──
    @app.post("/api/v1/system/resources/thresholds")
    async def update_resource_thresholds(
        cpu_percent: float = None,
        memory_percent: float = None,
        disk_percent: float = None,
        memory_available_mb: float = None,
    ):
        """更新系统资源阈值"""
        try:
            from src.system_monitor import get_system_monitor
            monitor = get_system_monitor()
            monitor.update_thresholds(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                memory_available_mb=memory_available_mb,
            )
            return {
                "success": True,
                "message": "阈值已更新",
                "data": monitor.get_status(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    return app


def _detect_project_root() -> Path:
    """自动检测 Somn 项目根目录"""
    current = Path(__file__).resolve()
    root = current.parent.parent
    if (root / "smart_office_assistant").exists():
        return root
    cwd = Path.cwd()
    if (cwd / "smart_office_assistant").exists():
        return cwd
    raise RuntimeError(
        f"无法检测 Somn 项目根目录。"
        f"请从 Somn 项目根目录运行，或通过 --project-root 指定。"
        f"当前: {root}, CWD: {cwd}"
    )


def _load_server_config(project_root: Path) -> dict:
    """加载服务器配置"""
    import yaml

    config_paths = [
        project_root / "config" / "server_config.yaml",
    ]

    for cfg_path in config_paths:
        if cfg_path.exists():
            with open(cfg_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                logger.info(f"加载服务器配置: {cfg_path}")
                return config

    logger.warning("未找到服务器配置文件，使用默认配置")
    return {"server": {"host": "127.0.0.1", "port": 8964}}


def _register_service(project_root: Path, config: dict):
    """注册服务到系统临时目录 (供前端自动发现)"""
    server_cfg = config.get("server", {})
    host = server_cfg.get("host", "127.0.0.1")
    port = server_cfg.get("port", 8964)

    if host in ("127.0.0.1", "localhost", "0.0.0.0"):
        url = f"http://127.0.0.1:{port}"
    else:
        url = f"http://{host}:{port}"

    registry = {
        "version": "6.2.0",
        "server_url": url,
        "api_prefix": "/api/v1",
        "ws_url": f"ws://127.0.0.1:{port}/api/v1/ws",
        "somn_root": str(project_root),
        "pid": os.getpid(),
        "started_at": datetime.now().isoformat(),
        "instance_id": str(uuid.uuid4()),
        "admin_endpoints": {
            "dashboard": "/api/v1/admin/dashboard",
            "load_manager": "/api/v1/admin/load-manager/status",
            "llm": "/api/v1/admin/llm/status",
            "chain": "/api/v1/admin/chain/full-status",
            "evolution": "/api/v1/admin/evolution/report",
            "memory": "/api/v1/admin/memory/health",
            "claw": "/api/v1/admin/claw/stats",
            "system": "/api/v1/admin/system/components",
            "neural": "/api/v1/admin/neural/status",
        },
        "docs_url": f"{url}/api/docs",
    }

    registry_file = Path(tempfile.gettempdir()) / "somn_server_registry.json"
    try:
        with open(registry_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
        logger.info(f"服务已注册: {registry_file}")
        logger.info(f"API地址: {url}")
        logger.info(f"API文档: {url}/api/docs")
    except Exception as e:
        logger.error(f"服务注册失败: {e}")


def _unregister_service():
    """注销服务"""
    registry_file = Path(tempfile.gettempdir()) / "somn_server_registry.json"
    try:
        if registry_file.exists():
            with open(registry_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("pid") == os.getpid():
                registry_file.unlink()
                logger.info("服务已注销")
    except Exception as e:
        logger.warning(f"服务注销失败: {e}")
