"""
Somn GUI - 后端连接管理器
实现动态路径发现: 无论Somn后端在哪个路径，前端都能自动发现并连接
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class BackendConnection:
    """
    后端连接管理器

    发现策略 (按优先级):
    1. 手动配置 (gui_config.yaml 中的 backend.server_url)
    2. 服务注册文件 (%TEMP%/somn_server_registry.json)
    3. 默认地址探测 (127.0.0.1:8964)
    4. 用户手动输入
    """

    DEFAULT_PORT = 8964
    REGISTRY_FILE = Path(tempfile.gettempdir()) / "somn_server_registry.json"
    DEFAULT_URL = "http://127.0.0.1:8964"

    def __init__(self, config: dict = None):
        self._config = config or {}
        backend_cfg = self._config.get("backend", {})
        self._manual_url = backend_cfg.get("server_url", "").strip()
        self._api_prefix = backend_cfg.get("api_prefix", "/api/v1")
        self._connect_timeout = backend_cfg.get("connect_timeout", 3)
        self._request_timeout = backend_cfg.get("request_timeout", 30)
        self._retry_count = backend_cfg.get("retry_count", 2)
        self._retry_delay = backend_cfg.get("retry_delay", 1)

        self._server_url: Optional[str] = None
        self._client: Optional[Any] = None  # v1.0.0: 避免顶层 httpx 导入
        self._ws_url: Optional[str] = None
        self._connected = False

    async def discover(self) -> str:
        """
        发现后端服务地址（并行探测优化）

        v1.0.0: 并行探测所有候选地址，取最快响应。

        Returns:
            后端服务URL

        Raises:
            ConnectionError: 所有发现策略均失败
        """
        import asyncio

        # 收集所有候选地址
        candidates = []
        if self._manual_url:
            candidates.append(("手动配置", self._manual_url))
        registry_url = self._read_registry()
        if registry_url:
            candidates.append(("注册文件", registry_url))
        candidates.append(("默认地址", self.DEFAULT_URL))

        if not candidates:
            raise ConnectionError("无可用后端地址")

        # v1.0.0: 并行探测所有候选地址
        async def _try_connect(name: str, url: str):
            try:
                if await self.check_health(url):
                    return (name, url)
            except Exception:
                pass
            return None

        tasks = [_try_connect(name, url) for name, url in candidates]
        results = await asyncio.gather(*tasks)

        # 优先使用手动配置 → 注册文件 → 默认地址
        for result in results:
            if result is not None:
                name, url = result
                self._set_connected(url)
                logger.info(f"通过[{name}]发现后端: {url}")
                return self._server_url

        # 全部失败
        raise ConnectionError(
            "无法连接到Somn后端服务。\n"
            "请确保后端已启动 (python start_server.py)，\n"
            "或在 config/gui_config.yaml 中手动指定 backend.server_url。"
        )

    async def check_health(self, url: str) -> bool:
        """检查后端是否可达"""
        import httpx  # v1.0.0: 延迟导入
        try:
            async with httpx.AsyncClient(timeout=self._connect_timeout) as client:
                resp = await client.get(f"{url}/api/v1/health")
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("success", False)
        except Exception as e:
            logger.debug(f"健康检查失败 ({url}): {e}")
        return False

    def _read_registry(self) -> Optional[str]:
        """读取服务注册文件"""
        try:
            if self.REGISTRY_FILE.exists():
                with open(self.REGISTRY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # 验证进程是否存活
                pid = data.get("pid")
                if pid:
                    try:
                        os.kill(pid, 0)  # 检查进程是否存在
                    except (OSError, ProcessLookupError):
                        logger.info(f"注册的进程 {pid} 已不存在")
                        return None
                return data.get("server_url")
        except Exception as e:
            logger.debug(f"读取注册文件失败: {e}")
        return None

    def _set_connected(self, url: str):
        """设置已连接状态"""
        import httpx  # v1.0.0: 延迟导入
        self._server_url = url.rstrip("/")
        self._ws_url = self._server_url.replace("http://", "ws://").replace("https://", "wss://")
        self._connected = True

        # 创建HTTP客户端 (base_url 设为 API 根路径含前缀)
        self._client = httpx.AsyncClient(
            base_url=f"{self._server_url}{self._api_prefix}",
            timeout=httpx.Timeout(self._request_timeout),
        )

    @property
    def api_base(self) -> str:
        """获取API基础URL"""
        if not self._server_url:
            raise ConnectionError("后端未连接")
        return f"{self._server_url}{self._api_prefix}"

    @property
    def ws_base(self) -> str:
        """获取WebSocket基础URL"""
        if not self._ws_url:
            raise ConnectionError("后端未连接")
        return f"{self._ws_url}{self._api_prefix}"

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def client(self) -> Any:  # v1.0.0: 返回类型改为 Any，避免顶层 httpx 导入
        """获取HTTP客户端"""
        if not self._client:
            raise ConnectionError("后端未连接，请先调用 discover()")
        return self._client

    async def get(self, path: str, **kwargs) -> dict:
        """发送GET请求"""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, json_data: dict = None, **kwargs) -> dict:
        """发送POST请求"""
        return await self._request("POST", path, json_data=json_data, **kwargs)

    async def delete(self, path: str, **kwargs) -> dict:
        """发送DELETE请求"""
        return await self._request("DELETE", path, **kwargs)

    async def _request(self, method: str, path: str, json_data: dict = None, **kwargs) -> dict:
        """发送请求 (带重试), base_url 已包含 API 前缀"""
        import httpx  # v1.0.0: 延迟导入
        # path 已是相对于 API 前缀的路径，如 /health, /chat
        url = path
        last_error = None

        for attempt in range(self._retry_count):
            try:
                resp = await self.client.request(
                    method, url,
                    json=json_data,
                    **kwargs,
                )
                resp.raise_for_status()
                return resp.json()
            except httpx.ConnectError as e:
                last_error = e
                self._connected = False
                logger.warning(f"连接失败 (尝试 {attempt + 1}/{self._retry_count}): {e}")
                if attempt < self._retry_count - 1:
                    import asyncio
                    await asyncio.sleep(self._retry_delay)
                    # 尝试重新发现（仅首次重试，避免递归风暴）
                    if attempt == 0:
                        try:
                            await self.discover()
                        except ConnectionError:
                            continue
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_error = e
                logger.warning(f"网络/超时错误 (尝试 {attempt + 1}/{self._retry_count}): {e}")
                if attempt < self._retry_count - 1:
                    import asyncio
                    await asyncio.sleep(self._retry_delay)
                    continue
            except Exception as e:
                last_error = e
                logger.error(f"请求失败: {method} {url} - {e}")
                break

        return {
            "success": False,
            "error": str(last_error),
            "error_code": "REQUEST_FAILED",
        }

    async def close(self):
        """关闭连接"""
        if self._client:
            await self._client.aclose()
            self._client = None
        self._connected = False
