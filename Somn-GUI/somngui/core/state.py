# -*- coding: utf-8 -*-
"""Somn GUI - 应用状态管理

集中管理 GUI 全局状态，通过 Signal 通知 UI 更新。
GUI 子模块通过 AppState 访问/修改状态，不直接调用 API。
"""

from __future__ import annotations

import asyncio
import threading
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from loguru import logger

# v1.0.0: 重型模块延迟导入 — 避免启动时触发 httpx/sqlite3/yaml 导入链
# 只在类型检查时导入，运行时按需加载
if TYPE_CHECKING:
    from somngui.client.api_client import SomnAPIClient
    from somngui.core.connection import BackendConnection
    from somngui.cache.cache_manager import CacheManager
    from somngui.cache.chat_history import ChatHistoryDB
    from somngui.gui._types import ChatMessage, DocumentInfo


# ---------------------------------------------------------------------------
# 连接状态枚举
# ---------------------------------------------------------------------------

class ConnectionStatus(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


# ---------------------------------------------------------------------------
# AppState — 全局 GUI 状态
# ---------------------------------------------------------------------------

class AppState(QObject):
    """GUI 全局应用状态

    所有 GUI 子模块共享同一个 AppState 实例。
    通过 Signal 驱动 UI 刷新，无需子模块间直接引用。
    """

    # ── 连接状态信号 ──
    connection_status_changed = pyqtSignal(object)  # ConnectionStatus
    backend_url_changed = pyqtSignal(str)

    # ── 聊天状态信号 ──
    chat_message_received = pyqtSignal(object)  # ChatMessage
    chat_history_cleared = pyqtSignal()
    chat_status_changed = pyqtSignal(str)  # "ready" | "thinking" | "error"

    # ── 知识库信号 ──
    knowledge_updated = pyqtSignal()
    knowledge_search_results = pyqtSignal(object)  # list[dict]

    # ── 文档信号 ──
    current_document_changed = pyqtSignal(object)  # DocumentInfo | None

    # ── 记忆/分析信号 ──
    memory_updated = pyqtSignal()
    analysis_result = pyqtSignal(object)  # dict

    # ── 系统管理信号 ──
    admin_dashboard_updated = pyqtSignal(object)  # dict: 全局仪表盘数据
    admin_component_updated = pyqtSignal(str, object)  # (component_name, data)
    admin_operation_result = pyqtSignal(str, bool, str)  # (operation, success, message)
    admin_error = pyqtSignal(str)  # error_message
    admin_panel_navigate = pyqtSignal(str)  # (panel_key,) 面板导航请求
    admin_panel_history_navigate = pyqtSignal(str)  # (panel_key,) 面包屑历史导航


    # ── 通用通知信号 ──
    notification = pyqtSignal(str, str)  # (title, message)
    error_occurred = pyqtSignal(str)  # error_message

    def __init__(self, config: 'GUIConfig' | None = None):
        super().__init__()
        # v1.0.0: config 延迟导入
        if config is None:
            from somngui.core.config import GUIConfig
            config = GUIConfig()
        self._config = config

        # v1.0.0: 缓存和数据库延迟初始化，减少启动耗时
        self._cache: 'CacheManager' | None = None
        self._chat_db: 'ChatHistoryDB' | None = None

        # v1.0.0: 后端连接延迟初始化 — AppState() 不再同步创建 BackendConnection
        self._connection: 'BackendConnection' | None = None
        self._api: 'SomnAPIClient' | None = None
        self._connection_status = ConnectionStatus.DISCONNECTED
        self._backend_url = ""

        # 聊天状态
        self._chat_history: List[Any] = []  # v1.0.0: 避免 __init__ 内导入 ChatMessage
        self._chat_status = "ready"  # ready | thinking | error
        self._current_session_id: Optional[str] = None

        # 文档状态
        self._current_document: Any = None  # v1.0.0: 避免 __init__ 内导入 DocumentInfo
        self._documents: List[Any] = []

        # 知识库缓存
        self._knowledge_cache: List[Dict[str, Any]] = []

        # v1.0.0: 面板导航历史栈
        self._panel_history: List[str] = []  # 历史记录（不含当前）
        self._current_panel_key: str = 'dashboard'  # 当前面板

    # ── 属性 ──

    @property
    def config(self) -> GUIConfig:
        return self._config

    @property
    def cache(self) -> 'CacheManager':
        """缓存管理器（延迟初始化）"""
        if self._cache is None:
            from somngui.cache.cache_manager import CacheManager  # v1.0.0
            self._cache = CacheManager(self._config.raw)
        return self._cache

    @property
    def chat_db(self) -> 'ChatHistoryDB':
        """对话历史数据库（延迟初始化）"""
        if self._chat_db is None:
            from somngui.cache.chat_history import ChatHistoryDB  # v1.0.0
            db_path = self._config.get("chat_history.db_path", "cache_data/chat_history.db")
            self._chat_db = ChatHistoryDB(db_path)
        return self._chat_db

    @property
    def connection(self) -> 'BackendConnection':
        """后端连接（延迟初始化）"""
        if self._connection is None:
            from somngui.core.connection import BackendConnection  # v1.0.0
            self._connection = BackendConnection(config=self._config.raw)
        return self._connection

    @property
    def api(self) -> SomnAPIClient:
        if self._api is None:
            raise RuntimeError("API 客户端未初始化，请先调用 connect_backend()")
        return self._api

    @property
    def connection_status(self) -> ConnectionStatus:
        return self._connection_status

    @property
    def backend_url(self) -> str:
        return self._backend_url

    @property
    def chat_history(self) -> List[ChatMessage]:
        return list(self._chat_history)

    @property
    def chat_status(self) -> str:
        return self._chat_status

    @property
    def current_session_id(self) -> Optional[str]:
        return self._current_session_id

    @property
    def current_document(self) -> DocumentInfo | None:
        return self._current_document

    @property
    def knowledge_cache(self) -> List[Dict[str, Any]]:
        return list(self._knowledge_cache)

    # ── 连接管理 ──

    async def connect_backend(self) -> bool:
        """连接后端服务"""
        self._set_connection_status(ConnectionStatus.CONNECTING)
        try:
            conn = self.connection  # v6.9.x: 使用属性触发延迟初始化
            url = await conn.discover()
            self._backend_url = url
            from somngui.client.api_client import SomnAPIClient  # v1.0.0: 延迟导入
            self._api = SomnAPIClient(conn)
            self.cache.set_offline(False)
            self._set_connection_status(ConnectionStatus.CONNECTED)
            self.backend_url_changed.emit(url)
            logger.info(f"后端已连接: {url}")
            # 后台预加载缓存 + 广播仪表盘数据
            self.run_async(self.cache.preload_data())
            self.refresh_dashboard_on_connect()
            return True
        except ConnectionError as e:
            self._set_connection_status(ConnectionStatus.ERROR)
            self.cache.set_offline(True)
            self.error_occurred.emit(str(e))
            logger.error(f"后端连接失败: {e}")
            return False
        except Exception as e:
            self._set_connection_status(ConnectionStatus.ERROR)
            self.cache.set_offline(True)
            self.error_occurred.emit(f"连接异常: {e}")
            logger.exception(f"后端连接异常: {e}")
            return False

    async def disconnect_backend(self):
        """断开后端连接"""
        if self._connection is not None:
            await self._connection.close()
        self._api = None
        self._backend_url = ""
        self._set_connection_status(ConnectionStatus.DISCONNECTED)
        logger.info("后端已断开")

    async def ensure_connected(self) -> bool:
        """确保后端已连接，必要时自动重连"""
        if self._connection_status == ConnectionStatus.CONNECTED:
            return True
        return await self.connect_backend()

    # ── 聊天状态 ──

    def add_chat_message(self, role: str, content: str, timestamp: str = "") -> ChatMessage:
        """添加聊天消息并发出信号"""
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M:%S")
        from somngui.gui._types import ChatMessage  # v6.9.x: 延迟导入避免循环依赖
        msg = ChatMessage(role=role, content=content, timestamp=timestamp)
        self._chat_history.append(msg)
        self.chat_message_received.emit(msg)

        # 持久化到历史数据库
        try:
            session_id = self._current_session_id or "default"
            # 自动创建会话
            if not self.chat_db.get_session(session_id):
                self.chat_db.create_session(session_id)
            self.chat_db.add_message(session_id, role, content)
            self.chat_db.update_session_timestamp(session_id)
        except Exception as e:
            logger.warning(f"对话历史持久化失败: {e}")

        return msg

    def set_chat_status(self, status: str):
        """设置聊天状态 (ready/thinking/error)"""
        if self._chat_status != status:
            self._chat_status = status
            self.chat_status_changed.emit(status)

    def clear_chat_history(self):
        """清空当前聊天历史（显示层面）"""
        self._chat_history.clear()
        self._current_session_id = None
        self.chat_history_cleared.emit()

    def delete_current_session(self):
        """删除当前会话的所有持久化消息"""
        session_id = self._current_session_id or "default"
        self.chat_db.delete_session(session_id)
        self._chat_history.clear()
        self._current_session_id = None
        self.chat_history_cleared.emit()

    def set_session_id(self, session_id: str):
        """设置当前会话 ID"""
        self._current_session_id = session_id

    # ── 文档状态 ──

    def set_current_document(self, doc: DocumentInfo | None):
        """设置当前文档"""
        self._current_document = doc
        self.current_document_changed.emit(doc)

    def add_document(self, doc: DocumentInfo):
        """添加文档到列表"""
        self._documents.append(doc)

    @property
    def documents(self) -> List[DocumentInfo]:
        return list(self._documents)

    # ── 知识库缓存 ──

    def set_knowledge_cache(self, items: List[Dict[str, Any]]):
        """更新知识库缓存"""
        self._knowledge_cache = items
        self.knowledge_updated.emit()

    # ── 通知 ──

    def notify(self, title: str, message: str):
        """发出通用通知"""
        self.notification.emit(title, message)

    def notify_error(self, message: str):
        """发出错误通知"""
        self.error_occurred.emit(message)

    # ── 内部方法 ──

    def _set_connection_status(self, status: ConnectionStatus):
        """更新连接状态并发出信号"""
        self._connection_status = status
        self.connection_status_changed.emit(status)

    # ── 异步工具 ──

    # v1.0.0: 复用后台 event_loop，避免每次 run_async 创建新线程和 loop
    _bg_loop: asyncio.AbstractEventLoop | None = None
    _bg_thread: threading.Thread | None = None

    @classmethod
    def _get_bg_loop(cls) -> asyncio.AbstractEventLoop:
        """获取或创建后台事件循环（单例）"""
        if cls._bg_loop is None or cls._bg_loop.is_closed():
            cls._bg_loop = asyncio.new_event_loop()
            cls._bg_thread = threading.Thread(
                target=cls._bg_loop.run_forever, daemon=True
            )
            cls._bg_thread.start()
        return cls._bg_loop

    @staticmethod
    def run_async(coro, callback: Callable = None):
        """在后台线程中运行异步协程（复用 event_loop）

        Args:
            coro: 要执行的协程
            callback: 完成后的回调函数 callback(result)
        """
        loop = AppState._get_bg_loop()

        def _done(fut):
            try:
                result = fut.result()
                if callback:
                    callback(result)
            except Exception as e:
                logger.error(f"异步任务失败: {e}")

        future = asyncio.run_coroutine_threadsafe(coro, loop)
        future.add_done_callback(_done)
        return future

    # ── 全局仪表盘数据广播 ──

    def broadcast_admin_dashboard(self):
        """
        获取全局仪表盘数据并广播给所有订阅的子面板。

        单次 API 调用获取完整 dashboard 数据，其他面板无需独立请求。
        广播后各子面板通过 admin_dashboard_updated 信号自动更新。
        """
        async def _fetch():
            try:
                if self._api is None:
                    return None
                resp = await self._api.get("/admin/dashboard")
                if resp.get("success"):
                    data = resp.get("data", {})
                    # 广播给所有订阅者
                    self.admin_dashboard_updated.emit(data)
                    # 同时广播各组件更新 (v1.0.0: 修复 - dashboard是扁平结构)
                    component_keys = ["load_manager", "llm", "chain", "evolution",
                                     "memory", "claw", "system", "neural"]
                    for comp_name in component_keys:
                        if comp_name in data:
                            self.admin_component_updated.emit(comp_name, data[comp_name])
                    return data
            except Exception as e:
                logger.warning(f"广播仪表盘数据失败: {e}")
                self.admin_error.emit(f"仪表盘数据获取失败: {e}")
            return None

        self.run_async(_fetch())

    def refresh_dashboard_on_connect(self):

        
        # ── v1.0.0 面板历史管理 ──
    
        @property
        def panel_history(self) -> list:
            """返回导航历史（只读）"""
            return list(self._panel_history)
    
        @property
        def current_panel_key(self) -> str:
            return self._current_panel_key
    
        def push_panel_history(self, new_key: str):
            """推入新面板到历史栈，并发出导航信号"""
            if self._current_panel_key != new_key:
                self._panel_history.append(self._current_panel_key)
                self._current_panel_key = new_key
                # 限制历史长度
                if len(self._panel_history) > 20:
                    self._panel_history = self._panel_history[-20:]
    
        def pop_panel_history(self) -> str | None:
            """弹出上一个面板（用于面包屑点击返回）"""
            if self._panel_history:
                # 回到上一个
                previous = self._panel_history[-1]
                self._current_panel_key = previous
                self._panel_history = self._panel_history[:-1]
                return previous
            return None
    
        def get_breadcrumb_path(self) -> list:
            """返回面包屑路径 [root, ..., current]"""
            return self._panel_history + [self._current_panel_key]
    
        """
        连接成功后刷新仪表盘数据并广播。

        在 connect_backend 成功返回后调用，
        确保 DashboardOverview 和所有子面板立即获得数据。
        """
        # 使用 QTimer 避免阻塞 GUI 线程
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(500, self.broadcast_admin_dashboard)  # 500ms 后执行
