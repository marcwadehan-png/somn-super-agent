# -*- coding: utf-8 -*-
"""
RSS订阅源连接器 - 从RSS/Atom订阅源抓取更新内容

功能:
- RSS 2.0 / Atom 1.0 解析
- 订阅源管理与健康检查
- 增量更新（基于GUID/时间戳去重）
- 自动轮询与过期清理
- 内容摘要提取

版本: v1.0.0
创建: 2026-04-23
"""

from __future__ import annotations
import asyncio
import hashlib
import re
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import OrderedDict

from ._openclaw_core import DataSourceConnector, DataSourceType, KnowledgeItem


@dataclass
class RssFeedConfig:
    """RSS订阅源配置"""
    feed_urls: List[str] = field(default_factory=list)
    poll_interval: int = 3600          # 轮询间隔（秒）
    max_items_per_feed: int = 20       # 每个源最大抓取数
    item_max_age_days: int = 30        # 条目最大保留天数
    timeout: int = 30
    user_agent: str = "OpenClaw/1.0 (Smart Office Assistant)"
    headers: Dict[str, str] = field(default_factory=dict)
    # 内容过滤
    required_keywords: List[str] = field(default_factory=list)   # 必须包含的关键词
    excluded_keywords: List[str] = field(default_factory=list)   # 排除的关键词
    # 摘要配置
    summary_max_length: int = 500


@dataclass
class RssFeedStatus:
    """单个订阅源状态"""
    url: str
    title: str = ""
    description: str = ""
    language: str = ""
    last_poll: Optional[datetime] = None
    last_status: str = "unknown"       # ok / error / timeout
    item_count: int = 0
    error_count: int = 0
    avg_items_per_poll: float = 0.0
    etag: str = ""                      # HTTP ETag（条件请求）
    last_modified: str = ""             # Last-Modified


@dataclass
class RssItem:
    """RSS条目解析结果"""
    title: str = ""
    link: str = ""
    description: str = ""
    content: str = ""                   # 完整内容（如果可用）
    author: str = ""
    category: str = ""
    pub_date: Optional[datetime] = None
    guid: str = ""
    feed_title: str = ""                # 所属订阅源标题
    feed_url: str = ""                  # 所属订阅源URL


class RssDataSource(DataSourceConnector):
    """RSS订阅源数据连接器

    支持RSS 2.0和Atom 1.0格式的订阅源，提供增量更新、健康检查和内容过滤能力。

    示例:
        config = RssFeedConfig(
            feed_urls=[
                "https://example.com/rss.xml",
                "https://another.com/atom.xml",
            ],
            poll_interval=1800,
            required_keywords=["AI", "technology"],
        )
        source = RssDataSource(config)
        await source.connect()
        items = await source.fetch("latest AI news")
    """

    def __init__(self, config: RssFeedConfig):
        super().__init__(DataSourceType.RSS, config.__dict__)
        self.config = config
        self._session = None
        self._seen_guids: OrderedDict[str, datetime] = OrderedDict()  # GUID -> 首次发现时间
        self._feed_status: Dict[str, RssFeedStatus] = {}
        self._max_cache_size = 10000  # 最大缓存GUID数

    async def connect(self) -> bool:
        """建立连接并验证所有订阅源"""
        try:
            import aiohttp
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            headers = {"User-Agent": self.config.user_agent}
            headers.update(self.config.headers)
            self._session = aiohttp.ClientSession(headers=headers, timeout=timeout)

            # 验证订阅源
            valid = 0
            for url in self.config.feed_urls:
                status = await self._check_feed(url)
                self._feed_status[url] = status
                if status.last_status == "ok":
                    valid += 1

            self.connected = valid > 0
            return self.connected
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

    async def fetch(self, query: str) -> List[KnowledgeItem]:
        """从所有订阅源抓取最新内容

        流程:
        1. 遍历所有已注册的订阅源
        2. 逐个拉取并解析RSS/Atom
        3. 根据query进行关键词过滤
        4. 去重（基于GUID）
        5. 转换为KnowledgeItem列表
        """
        if not self.connected:
            await self.connect()

        all_items = []
        query_lower = query.lower()

        for url in self.config.feed_urls:
            try:
                rss_items = await self._fetch_feed(url)
                filtered = self._filter_items(rss_items, query_lower)

                for item in filtered:
                    # 去重检查
                    if item.guid and item.guid in self._seen_guids:
                        continue

                    # 记录GUID
                    if item.guid:
                        self._seen_guids[item.guid] = datetime.now()
                        self._trim_cache()

                    ki = self._to_knowledge_item(item)
                    if ki:
                        all_items.append(ki)

            except Exception as e:
                status = self._feed_status.get(url)
                if status:
                    status.error_count += 1
                    status.last_status = "error"

        return all_items

    async def add_feed(self, url: str) -> bool:
        """动态添加订阅源"""
        if url not in self.config.feed_urls:
            self.config.feed_urls.append(url)
        status = await self._check_feed(url)
        self._feed_status[url] = status
        return status.last_status == "ok"

    def remove_feed(self, url: str) -> bool:
        """移除订阅源"""
        if url in self.config.feed_urls:
            self.config.feed_urls.remove(url)
            self._feed_status.pop(url, None)
            return True
        return False

    def get_feed_status(self, url: Optional[str] = None) -> Any:
        """获取订阅源状态"""
        if url:
            return self._feed_status.get(url)
        return {
            url: {
                "title": s.title,
                "status": s.last_status,
                "items": s.item_count,
                "last_poll": s.last_poll.isoformat() if s.last_poll else None,
            }
            for url, s in self._feed_status.items()
        }

    # ─────────────────────────────────────────
    # RSS/Atom 解析
    # ─────────────────────────────────────────

    async def _fetch_feed(self, url: str) -> List[RssItem]:
        """抓取并解析单个订阅源"""
        try:
            headers = {}
            status = self._feed_status.get(url)
            if status:
                if status.etag:
                    headers["If-None-Match"] = status.etag
                if status.last_modified:
                    headers["If-Modified-Since"] = status.last_modified

            async with self._session.get(url, headers=headers or None) as resp:
                status_obj = self._feed_status.get(url)
                if not status_obj:
                    status_obj = RssFeedStatus(url=url)
                    self._feed_status[url] = status_obj

                status_obj.last_poll = datetime.now()

                # 保存条件请求头
                status_obj.etag = resp.headers.get("ETag", "")
                status_obj.last_modified = resp.headers.get("Last-Modified", "")

                if resp.status == 304:
                    status_obj.last_status = "ok"
                    return []  # 内容未变

                if resp.status != 200:
                    status_obj.last_status = "error"
                    status_obj.error_count += 1
                    return []

                raw = await resp.text()

                # 判断格式并解析
                if "<feed" in raw[:500].lower() and "atom" in raw[:500].lower():
                    items = self._parse_atom(raw, url)
                else:
                    items = self._parse_rss(raw, url)

                status_obj.last_status = "ok"
                status_obj.item_count = len(items)
                status_obj.avg_items_per_poll = (
                    (status_obj.avg_items_per_poll * (status_obj.error_count + status_obj.item_count) + len(items))
                    / (status_obj.error_count + status_obj.item_count + 1)
                ) if (status_obj.error_count + status_obj.item_count) > 0 else len(items)

                return items[:self.config.max_items_per_feed]

        except asyncio.TimeoutError:
            status_obj = self._feed_status.get(url)
            if status_obj:
                status_obj.last_status = "timeout"
                status_obj.error_count += 1
            return []
        except Exception as e:
            status_obj = self._feed_status.get(url)
            if status_obj:
                status_obj.last_status = "error"
                status_obj.error_count += 1
            return []

    def _parse_rss(self, raw: str, feed_url: str) -> List[RssItem]:
        """解析 RSS 2.0 格式"""
        try:
            import xml.etree.ElementTree as ET
            # 移除命名空间前缀以简化解析
            raw_clean = re.sub(r'xmlns[:\w]*=["\'][^"\']*["\']', '', raw)
            root = ET.fromstring(raw_clean)

            items = []
            feed_title = self._text_safe(root.find(".//channel/title"), "")

            for entry in root.findall(".//channel/item"):
                item = RssItem()
                item.feed_title = feed_title
                item.feed_url = feed_url
                item.title = self._text_safe(entry.find("title"))
                item.link = self._text_safe(entry.find("link"))
                item.description = self._text_safe(entry.find("description"))
                item.author = self._text_safe(entry.find("author")) or self._text_safe(entry.find(".//dc:creator"))
                item.category = self._text_safe(entry.find("category"))
                item.guid = self._text_safe(entry.find("guid")) or hashlib.md5((item.title + item.link).encode()).hexdigest()

                # 解析日期
                date_str = self._text_safe(entry.find("pubDate"))
                if date_str:
                    item.pub_date = self._parse_date(date_str)

                # 尝试获取完整内容
                content_elem = entry.find(".//content:encoded")
                if content_elem is not None and content_elem.text:
                    item.content = content_elem.text

                items.append(item)

            return items
        except Exception:
            return []

    def _parse_atom(self, raw: str, feed_url: str) -> List[RssItem]:
        """解析 Atom 1.0 格式"""
        try:
            import xml.etree.ElementTree as ET
            raw_clean = re.sub(r'xmlns[:\w]*=["\'][^"\']*["\']', '', raw)
            root = ET.fromstring(raw_clean)

            items = []
            feed_title = self._text_safe(root.find(".//title"), "Atom Feed")

            for entry in root.findall(".//entry"):
                item = RssItem()
                item.feed_title = feed_title
                item.feed_url = feed_url
                item.title = self._text_safe(entry.find("title"))
                item.link = ""
                link_elem = entry.find("link")
                if link_elem is not None:
                    item.link = link_elem.get("href", "")
                item.description = self._text_safe(entry.find("summary"))
                item.author = self._text_safe(entry.find(".//author/name"))
                item.category = self._text_safe(entry.find(".//category"))
                item.guid = self._text_safe(entry.find("id")) or hashlib.md5((item.title + item.link).encode()).hexdigest()

                # 解析日期
                date_str = self._text_safe(entry.find("published")) or self._text_safe(entry.find("updated"))
                if date_str:
                    item.pub_date = self._parse_date(date_str)

                # 完整内容
                content_elem = entry.find("content")
                if content_elem is not None and content_elem.text:
                    item.content = content_elem.text

                items.append(item)

            return items
        except Exception:
            return []

    # ─────────────────────────────────────────
    # 过滤与转换
    # ─────────────────────────────────────────

    def _filter_items(self, items: List[RssItem], query: str) -> List[RssItem]:
        """根据配置和查询过滤条目"""
        now = datetime.now()
        max_age = timedelta(days=self.config.item_max_age_days)
        filtered = []

        for item in items:
            # 时间过滤
            if item.pub_date and (now - item.pub_date) > max_age:
                continue

            # 必须包含关键词
            text = f"{item.title} {item.description} {item.content}".lower()
            if self.config.required_keywords:
                if not any(kw.lower() in text for kw in self.config.required_keywords):
                    continue

            # 排除关键词
            if self.config.excluded_keywords:
                if any(kw.lower() in text for kw in self.config.excluded_keywords):
                    continue

            # 查询相关性（加分项，不强制）
            if query and query not in ("", "*"):
                query_words = query.lower().split()
                relevance = sum(1 for w in query_words if w in text)
                if relevance == 0:
                    continue  # 查询词完全不相关则跳过

            filtered.append(item)

        return filtered

    def _to_knowledge_item(self, item: RssItem) -> Optional[KnowledgeItem]:
        """将RssItem转换为KnowledgeItem"""
        if not item.title and not item.description:
            return None

        # 摘要提取：优先用description，其次用content前N字符
        summary = item.description or ""
        if not summary and item.content:
            summary = item.content[:self.config.summary_max_length]

        # 构建结构化内容
        content_parts = [f"标题: {item.title}"]
        if item.author:
            content_parts.append(f"作者: {item.author}")
        if item.category:
            content_parts.append(f"分类: {item.category}")
        if item.pub_date:
            content_parts.append(f"日期: {item.pub_date.strftime('%Y-%m-%d %H:%M')}")
        content_parts.append(f"\n{summary}")
        if item.link:
            content_parts.append(f"\n来源: {item.link}")

        full_content = "\n".join(content_parts)

        return KnowledgeItem(
            id=f"rss_{hashlib.md5(item.guid.encode()).hexdigest()[:12]}",
            content=full_content,
            source=item.feed_url,
            timestamp=item.pub_date or datetime.now(),
            metadata={
                "title": item.title,
                "link": item.link,
                "author": item.author,
                "category": item.category,
                "feed_title": item.feed_title,
                "format": "rss",
            },
            confidence=0.8,  # RSS内容置信度默认0.8
        )

    # ─────────────────────────────────────────
    # 辅助方法
    # ─────────────────────────────────────────

    async def _check_feed(self, url: str) -> RssFeedStatus:
        """检查订阅源可用性"""
        status = RssFeedStatus(url=url)
        try:
            if not self._session:
                import aiohttp
                timeout = aiohttp.ClientTimeout(total=10)
                self._session = aiohttp.ClientSession(timeout=timeout)

            async with self._session.get(url) as resp:
                if resp.status == 200:
                    raw = await resp.text()
                    status.last_status = "ok"
                    # 提取标题
                    import xml.etree.ElementTree as ET
                    raw_clean = re.sub(r'xmlns[:\w]*=["\'][^"\']*["\']', '', raw)
                    root = ET.fromstring(raw_clean)
                    title_elem = root.find(".//channel/title") or root.find(".//title")
                    status.title = self._text_safe(title_elem)
                else:
                    status.last_status = "error"
                    status.error_count += 1
        except Exception:
            status.last_status = "error"
            status.error_count += 1

        return status

    @staticmethod
    def _text_safe(elem, default: str = "") -> str:
        """安全提取XML元素文本"""
        if elem is not None and elem.text:
            return elem.text.strip()
        return default

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        """解析常见日期格式"""
        from email.utils import parsedate_to_datetime
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%a, %d %b %Y %H:%M:%S %z",     # RFC 2822
            "%a, %d %b %Y %H:%M:%S",
            "%Y-%m-%d",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        try:
            return parsedate_to_datetime(date_str)
        except Exception:
            return None

    def _trim_cache(self):
        """清理过期的GUID缓存"""
        while len(self._seen_guids) > self._max_cache_size:
            self._seen_guids.popitem(last=False)


# ─────────────────────────────────────────
# 模块级别辅助
# ─────────────────────────────────────────

def discover_feeds_from_html(html: str, base_url: str = "") -> List[str]:
    """从HTML页面中自动发现RSS/Atom订阅链接

    Args:
        html: HTML内容
        base_url: 基础URL（用于解析相对路径）

    Returns:
        发现的订阅源URL列表
    """
    feeds = []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # 查找 <link> 标签中的RSS/Atom
        for link in soup.find_all("link", rel=re.compile(r"alternate", re.I)):
            href = link.get("href", "")
            link_type = link.get("type", "").lower()
            title = link.get("title", "")

            if "rss" in link_type or "atom" in link_type or "xml" in link_type:
                if href:
                    if base_url and not href.startswith("http"):
                        from urllib.parse import urljoin
                        href = urljoin(base_url, href)
                    feeds.append(href)

        # 查找页面中的RSS链接
        for a in soup.find_all("a", href=re.compile(r"rss|atom|feed", re.I)):
            href = a.get("href", "")
            if href and href not in feeds:
                if base_url and not href.startswith("http"):
                    from urllib.parse import urljoin
                    href = urljoin(base_url, href)
                feeds.append(href)
    except ImportError:
        # BeautifulSoup不可用时，用正则回退
        patterns = [
            r'<link[^>]+type=["\']application/(rss|atom)\+xml["\'][^>]+href=["\']([^"\']+)["\']',
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+type=["\']application/(rss|atom)\+xml["\']',
        ]
        for pat in patterns:
            for m in re.finditer(pat, html, re.I):
                feeds.append(m.group(2) if m.lastindex >= 2 else m.group(1))

    return feeds


__all__ = [
    'RssDataSource',
    'RssFeedConfig',
    'RssFeedStatus',
    'RssItem',
    'discover_feeds_from_html',
]
