# -*- coding: utf-8 -*-
"""
API数据源连接器 - 从外部REST/GraphQL API抓取结构化数据

功能:
- REST API 调用（GET/POST）
- GraphQL 查询
- 响应解析（JSON/XML/CSV）
- 自动分页处理
- 速率限制与重试
- 认证管理（API Key / Bearer Token / OAuth2）

版本: v1.0.0
创建: 2026-04-23
"""

from __future__ import annotations
import asyncio
import json
import re
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ._openclaw_core import DataSourceConnector, DataSourceType, KnowledgeItem


class AuthType(Enum):
    """认证类型"""
    NONE = "none"
    API_KEY = "api_key"          # URL参数或Header中的API Key
    BEARER = "bearer"            # Authorization: Bearer <token>
    BASIC = "basic"              # Basic Auth
    CUSTOM_HEADER = "custom_header"  # 自定义Header认证


class ResponseFormat(Enum):
    """响应格式"""
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    TEXT = "text"
    HTML = "html"


@dataclass
class PaginationConfig:
    """分页配置"""
    enabled: bool = True
    type: str = "offset"         # offset / cursor / link / page
    page_param: str = "page"
    page_size_param: str = "page_size"
    page_size: int = 50
    max_pages: int = 10
    cursor_field: str = "cursor"
    link_header: str = "Link"


@dataclass
class RateLimitConfig:
    """速率限制配置"""
    requests_per_minute: int = 60
    burst: int = 10
    retry_delay: float = 1.0
    max_retries: int = 3
    backoff_factor: float = 2.0


@dataclass
class ApiSourceConfig:
    """API数据源配置"""
    base_url: str = ""
    auth_type: AuthType = AuthType.NONE
    auth_value: str = ""              # API Key / Token / user:pass
    auth_header: str = "Authorization"  # 自定义认证Header名
    api_key_param: str = "api_key"   # URL参数模式下的参数名
    default_headers: Dict[str, str] = field(default_factory=dict)
    response_format: ResponseFormat = ResponseFormat.JSON
    timeout: int = 30
    pagination: PaginationConfig = field(default_factory=PaginationConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    # GraphQL 特有
    graphql_endpoint: str = ""
    # 响应数据提取路径（如 "data.items" 表示从响应JSON中提取 data->items）
    data_path: str = ""
    # 响应中总数字段路径（用于分页判断）
    total_path: str = ""


class ApiDataSource(DataSourceConnector):
    """API数据源连接器

    支持从REST和GraphQL API抓取结构化数据，自动处理分页、速率限制和认证。

    示例:
        config = ApiSourceConfig(
            base_url="https://api.example.com/v1",
            auth_type=AuthType.BEARER,
            auth_value="my_token",
            response_format=ResponseFormat.JSON,
            data_path="data.results",
        )
        source = ApiDataSource(config)
        await source.connect()
        items = await source.fetch("recent papers")
    """

    def __init__(self, config: ApiSourceConfig):
        super().__init__(DataSourceType.API, config.__dict__)
        self.config = config
        self._session = None
        self._request_times: List[float] = []
        self._total_requests = 0
        self._total_errors = 0

    async def connect(self) -> bool:
        """建立连接（验证API可用性）"""
        try:
            import aiohttp
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            headers = self._build_headers()
            self._session = aiohttp.ClientSession(
                headers=headers,
                timeout=timeout,
            )
            # 尝试一个HEAD请求验证连接
            try:
                async with self._session.head(
                    self.config.base_url,
                    allow_redirects=True,
                ) as resp:
                    if resp.status < 500:
                        self.connected = True
                        return True
            except Exception:
                # 即使HEAD失败，也标记为已连接（某些API不支持HEAD）
                self.connected = True
                return True
        except Exception:
            self.connected = False
            return False

    async def disconnect(self) -> bool:
        """断开连接"""
        if self._session:
            await self._session.close()
            self._session = None
        self.connected = False
        return True

    # ─────────────────────────────────────────
    # 核心抓取
    # ─────────────────────────────────────────

    async def fetch(self, query: str) -> List[KnowledgeItem]:
        """根据查询条件从API抓取数据

        对于REST API: 将query附加到base_url后发起GET请求
        对于GraphQL: 将query作为搜索条件构建GraphQL查询
        """
        if not self.connected:
            await self.connect()

        results = []

        if self.config.graphql_endpoint:
            results = await self._fetch_graphql(query)
        else:
            results = await self._fetch_rest(query)

        return results

    async def fetch_endpoint(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        body: Optional[Dict] = None,
    ) -> List[KnowledgeItem]:
        """直接调用指定API端点

        Args:
            path: API路径（如 "/papers/search"）
            params: 查询参数
            method: HTTP方法
            body: 请求体（POST/PUT时使用）
        """
        if not self.connected:
            await self.connect()

        url = self._build_url(path)
        all_items = []

        if self.config.pagination.enabled:
            items = await self._fetch_paginated(url, params, method, body)
            all_items.extend(items)
        else:
            item = await self._single_request(url, params, method, body)
            if item:
                all_items.append(item)

        return all_items

    # ─────────────────────────────────────────
    # REST API
    # ─────────────────────────────────────────

    async def _fetch_rest(self, query: str) -> List[KnowledgeItem]:
        """REST API 抓取"""
        from urllib.parse import quote_plus
        encoded_query = quote_plus(query)
        path = f"/search?q={encoded_query}"
        url = self._build_url(path)
        all_items = []

        if self.config.pagination.enabled:
            all_items = await self._fetch_paginated(url)
        else:
            item = await self._single_request(url)
            if item:
                all_items.append(item)

        return all_items

    async def _fetch_paginated(
        self,
        url: str,
        params: Optional[Dict] = None,
        method: str = "GET",
        body: Optional[Dict] = None,
    ) -> List[KnowledgeItem]:
        """分页抓取"""
        all_items = []
        params = dict(params) if params else {}
        pag = self.config.pagination

        for page in range(1, pag.max_pages + 1):
            # 设置分页参数
            page_params = dict(params)
            if pag.type == "offset":
                page_params[pag.page_param] = page
                page_params[pag.page_size_param] = pag.page_size
            elif pag.type == "page":
                page_params[pag.page_param] = page

            await self._wait_rate_limit()

            item = await self._single_request(url, page_params, method, body)
            if item is None:
                break

            # 提取数据
            extracted = self._extract_data(item.content)
            if isinstance(extracted, list):
                all_items.extend(extracted)
                # 检查是否还有更多数据
                if len(extracted) < pag.page_size:
                    break
            elif isinstance(extracted, dict):
                all_items.append(item)

            # Link Header 分页
            if pag.type == "link" and self._session:
                # 从上一个响应中检查Link header
                break

        return all_items

    # ─────────────────────────────────────────
    # GraphQL
    # ─────────────────────────────────────────

    async def _fetch_graphql(self, query: str) -> List[KnowledgeItem]:
        """GraphQL 查询"""
        if not self.config.graphql_endpoint:
            return []

        gql_query = self._build_graphql_query(query)
        await self._wait_rate_limit()

        try:
            async with self._session.post(
                self.config.graphql_endpoint,
                json={"query": gql_query},
            ) as resp:
                self._total_requests += 1
                if resp.status == 200:
                    data = await resp.json()
                    items_data = self._extract_data(json.dumps(data))
                    if isinstance(items_data, list):
                        return [
                            KnowledgeItem(
                                id=f"api_gql_{hash(str(d)) % (10**8)}",
                                content=json.dumps(d, ensure_ascii=False) if isinstance(d, dict) else str(d),
                                source=self.config.graphql_endpoint,
                                metadata={"format": "graphql", "query": query},
                            )
                            for d in items_data
                        ]
                    elif items_data:
                        return [KnowledgeItem(
                            id=f"api_gql_{hash(str(items_data)) % (10**8)}",
                            content=json.dumps(items_data, ensure_ascii=False) if isinstance(items_data, dict) else str(items_data),
                            source=self.config.graphql_endpoint,
                            metadata={"format": "graphql", "query": query},
                        )]
        except Exception as e:
            self._total_errors += 1

        return []

    def _build_graphql_query(self, query: str) -> str:
        """构建GraphQL查询语句"""
        # 通用搜索查询模板
        return f'''
        query {{
            search(query: "{query}", first: 20) {{
                edges {{
                    node {{
                        id
                        title
                        content
                        updatedAt
                    }}
                }}
            }}
        }}
        '''.strip()

    # ─────────────────────────────────────────
    # HTTP请求基础设施
    # ─────────────────────────────────────────

    async def _single_request(
        self,
        url: str,
        params: Optional[Dict] = None,
        method: str = "GET",
        body: Optional[Dict] = None,
    ) -> Optional[KnowledgeItem]:
        """单次HTTP请求"""
        await self._wait_rate_limit()

        for attempt in range(self.config.rate_limit.max_retries):
            try:
                kw = {}
                if params:
                    kw["params"] = params
                if body and method.upper() in ("POST", "PUT", "PATCH"):
                    kw["json"] = body

                async with self._session.request(method, url, **kw) as resp:
                    self._total_requests += 1

                    if resp.status == 429:
                        # 速率限制，等待后重试
                        retry_after = float(resp.headers.get("Retry-After", self.config.rate_limit.retry_delay))
                        await asyncio.sleep(retry_after)
                        continue

                    if resp.status >= 400:
                        self._total_errors += 1
                        if attempt < self.config.rate_limit.max_retries - 1:
                            delay = self.config.rate_limit.retry_delay * (self.config.rate_limit.backoff_factor ** attempt)
                            await asyncio.sleep(delay)
                            continue
                        return None

                    raw = await resp.text()

                    # 解析格式
                    parsed = self._parse_response(raw)

                    return KnowledgeItem(
                        id=f"api_{hash(url + str(params)) % (10**8)}",
                        content=parsed,
                        source=url,
                        metadata={
                            "format": self.config.response_format.value,
                            "status": resp.status,
                            "url": url,
                            "params": str(params or {}),
                            "timestamp": datetime.now().isoformat(),
                        },
                    )
            except asyncio.TimeoutError:
                self._total_errors += 1
                if attempt < self.config.rate_limit.max_retries - 1:
                    delay = self.config.rate_limit.retry_delay * (self.config.rate_limit.backoff_factor ** attempt)
                    await asyncio.sleep(delay)
                    continue
                return None
            except Exception as e:
                self._total_errors += 1
                return None

        return None

    # ─────────────────────────────────────────
    # 解析与提取
    # ─────────────────────────────────────────

    def _parse_response(self, raw: str) -> str:
        """根据配置解析响应体"""
        fmt = self.config.response_format

        if fmt == ResponseFormat.JSON:
            try:
                data = json.loads(raw)
                if self.config.data_path:
                    extracted = self._extract_data(raw)
                    return json.dumps(extracted, ensure_ascii=False, indent=2) if extracted else raw
                return json.dumps(data, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                return raw

        elif fmt == ResponseFormat.XML:
            try:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(raw)
                return self._xml_to_text(root)
            except Exception:
                return raw

        elif fmt == ResponseFormat.CSV:
            return raw

        return raw

    def _extract_data(self, content: str) -> Any:
        """从响应中按路径提取数据"""
        if not self.config.data_path:
            return content

        try:
            if isinstance(content, str):
                # 尝试JSON解析
                try:
                    data = json.loads(content)
                except (json.JSONDecodeError, TypeError):
                    return content
            else:
                data = content

            # 按"."分割路径逐层提取
            parts = self.config.data_path.split(".")
            current = data
            for part in parts:
                if isinstance(current, dict):
                    current = current.get(part)
                elif isinstance(current, list) and part.isdigit():
                    idx = int(part)
                    current = current[idx] if idx < len(current) else None
                else:
                    return None
                if current is None:
                    return None
            return current
        except Exception:
            return content

    def _xml_to_text(self, element) -> str:
        """将XML元素转为可读文本"""
        texts = []
        for child in element:
            texts.append(child.text.strip() if child.text else "")
            if len(child):
                texts.append(self._xml_to_text(child))
        return " ".join(t for t in texts if t)

    # ─────────────────────────────────────────
    # 认证与速率限制
    # ─────────────────────────────────────────

    def _build_headers(self) -> Dict[str, str]:
        """构建请求头（含认证）"""
        headers = dict(self.config.default_headers)
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "OpenClaw/1.0 (Smart Office Assistant)"

        auth = self.config.auth_type
        val = self.config.auth_value

        if auth == AuthType.API_KEY:
            headers[self.config.auth_header] = val
        elif auth == AuthType.BEARER:
            headers["Authorization"] = f"Bearer {val}"
        elif auth == AuthType.BASIC:
            import base64
            headers["Authorization"] = f"Basic {base64.b64encode(val.encode()).decode()}"
        elif auth == AuthType.CUSTOM_HEADER:
            headers[self.config.auth_header] = val

        return headers

    def _build_url(self, path: str) -> str:
        """构建完整URL"""
        from urllib.parse import urljoin
        base = self.config.base_url.rstrip("/")
        return urljoin(base + "/", path.lstrip("/"))

    async def _wait_rate_limit(self):
        """速率限制等待"""
        now = time.time()
        # 清理1分钟前的记录
        self._request_times = [t for t in self._request_times if now - t < 60]

        limit = self.config.rate_limit.requests_per_minute
        if len(self._request_times) >= limit:
            sleep_time = 60.0 - (now - self._request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

        self._request_times.append(time.time())

    # ─────────────────────────────────────────
    # 状态与统计
    # ─────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """获取API数据源统计"""
        return {
            "base_url": self.config.base_url,
            "auth_type": self.config.auth_type.value,
            "response_format": self.config.response_format.value,
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
            "success_rate": (
                (self._total_requests - self._total_errors) / self._total_requests
                if self._total_requests > 0 else 0
            ),
            "rate_limit_remaining": self.config.rate_limit.requests_per_minute - len(self._request_times),
        }

    def get_api_schema(self) -> Dict[str, Any]:
        """获取API配置概要（供OpenClawCore了解数据源能力）"""
        return {
            "type": "api",
            "base_url": self.config.base_url,
            "graphql": bool(self.config.graphql_endpoint),
            "auth": self.config.auth_type.value,
            "format": self.config.response_format.value,
            "pagination": self.config.pagination.type if self.config.pagination.enabled else "none",
            "data_path": self.config.data_path or "(raw)",
        }


__all__ = [
    'ApiDataSource',
    'ApiSourceConfig',
    'AuthType',
    'ResponseFormat',
    'PaginationConfig',
    'RateLimitConfig',
]
