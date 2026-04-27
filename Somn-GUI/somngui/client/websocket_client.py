"""Somn GUI - WebSocket 客户端

实时双向通信，支持流式对话和心跳保活。
协议格式: JSON {"type": str, "content": str, "session_id": str, ...}
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class SomnWebSocketClient:
    """WebSocket 实时客户端

    在独立线程中运行 asyncio 事件循环，通过回调通知 UI。
    """

    def __init__(self, ws_url: str):
        self._ws_url = ws_url
        self._ws = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread = None
        self._running = False
        self._connected = False

        # 回调 (由 MainWindow 设置)
        self._on_message: Optional[Callable] = None
        self._on_status: Optional[Callable] = None
        self._on_error: Optional[Callable] = None
        self._on_connected: Optional[Callable] = None
        self._on_disconnected: Optional[Callable] = None

    @property
    def is_connected(self) -> bool:
        return self._connected

    def set_callbacks(self, on_message=None, on_status=None,
                      on_error=None, on_connected=None, on_disconnected=None):
        """设置回调函数"""
        self._on_message = on_message
        self._on_status = on_status
        self._on_error = on_error
        self._on_connected = on_connected
        self._on_disconnected = on_disconnected

    def connect(self):
        """启动 WebSocket 连接 (后台线程)"""
        if self._running:
            return
        self._running = True
        import threading
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info(f"WebSocket 连接中: {self._ws_url}")

    def disconnect(self):
        """断开 WebSocket"""
        self._running = False
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._close_ws(), self._loop)
        if self._thread:
            self._thread.join(timeout=3)
        logger.info("WebSocket 已断开")

    def send_chat(self, message: str, session_id: str = ""):
        """发送对话消息"""
        self._send_json({
            "type": "chat",
            "content": message,
            "session_id": session_id,
        })

    def send_ping(self):
        """发送心跳"""
        self._send_json({"type": "ping"})

    def _send_json(self, data: dict):
        """线程安全发送 JSON"""
        if self._loop and self._loop.is_running() and self._connected:
            asyncio.run_coroutine_threadsafe(
                self._async_send(data), self._loop
            )

    async def _async_send(self, data: dict):
        try:
            if self._ws:
                await self._ws.send(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            logger.warning(f"WebSocket 发送失败: {e}")

    async def _close_ws(self):
        if self._ws:
            try:
                await self._ws.close()
            except Exception as e:
                logger.debug(f"WebSocket 关闭异常: {e}")

    def _run_loop(self):
        """后台事件循环"""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._connect_and_listen())
        except Exception as e:
            logger.error(f"WebSocket 循环异常: {e}")
        finally:
            self._connected = False
            self._loop.close()

    async def _connect_and_listen(self):
        """连接并持续监听"""
        import websockets
        retry_delay = 1
        max_delay = 30

        while self._running:
            try:
                async with websockets.connect(self._ws_url) as ws:
                    self._ws = ws
                    self._connected = True
                    retry_delay = 1  # 重置重试间隔
                    if self._on_connected:
                        self._on_connected()
                    logger.info("WebSocket 已连接")

                    # 心跳任务
                    ping_task = asyncio.create_task(self._heartbeat())

                    try:
                        async for raw in ws:
                            try:
                                msg = json.loads(raw)
                                self._dispatch(msg)
                            except json.JSONDecodeError:
                                logger.warning(f"无效 WebSocket 消息: {raw[:100]}")
                    except websockets.ConnectionClosed:
                        logger.info("WebSocket 连接已关闭")
                    finally:
                        ping_task.cancel()
                        self._connected = False
                        if self._on_disconnected:
                            self._on_disconnected()

            except Exception as e:
                logger.warning(f"WebSocket 连接失败: {e}, {retry_delay}s 后重试...")
                if self._on_error:
                    self._on_error(str(e))

            # 指数退避重连
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_delay)

    async def _heartbeat(self):
        """心跳保活 (每30秒)"""
        while self._running and self._connected:
            await asyncio.sleep(30)
            try:
                await self._ws.send(json.dumps({"type": "ping"}))
            except Exception:
                break

    def _dispatch(self, msg: dict):
        """分发收到的消息到对应回调"""
        msg_type = msg.get("type", "")
        content = msg.get("content", "")
        session_id = msg.get("session_id", "")

        if msg_type == "pong":
            return

        if msg_type == "status":
            if self._on_status:
                self._on_status(content, session_id)
        elif msg_type == "reply":
            if self._on_message:
                self._on_message(content, session_id, msg)
        elif msg_type == "error":
            if self._on_error:
                self._on_error(content)
        else:
            logger.debug(f"未知 WebSocket 消息类型: {msg_type}")
