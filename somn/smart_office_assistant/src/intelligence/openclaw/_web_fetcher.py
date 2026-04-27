# -*- coding: utf-8 -*-
"""
网页深度抓取器 - 智能提取网页核心内容

功能:
- 多策略内容提取（Readability/正文提取/结构化提取）
- 链接发现与深度爬取（BFS/DFS）
- 反爬处理（User-Agent轮换、延迟、重试）
- 内容去重与相似度检测
- robots.txt 遵守
- 抓取深度与广度控制

版本: v1.0.0
创建: 2026-04-23
"""

from __future__ import annotations
import asyncio
import hashlib
import re
import time
import random
from typing import Dict, List, Optional, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
from urllib.parse import urljoin, urlparse, urlunparse

try:
    import aiohttp
except ImportError:
    aiohttp = None

from ._openclaw_core import KnowledgeItem


@dataclass
class FetchConfig:
    """抓取配置"""
    max_depth: int = 2                    # 最大抓取深度
    max_pages: int = 50                   # 单次最大页面数
    timeout: int = 30                     # 单页超时
    delay_range: Tuple[float, float] = (0.5, 2.0)  # 请求延迟范围
    max_retries: int = 3
    backoff_factor: float = 2.0
    respect_robots_txt: bool = True       # 遵守robots.txt
    # User-Agent轮换
    user_agents: List[str] = field(default_factory=lambda: [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ])
    # 内容提取
    max_content_length: int = 50000       # 单页最大内容长度
    min_content_length: int = 100         # 最小有效内容长度
    extract_strategy: str = "auto"        # auto / readability / structured / raw
    # 链接过滤
    allowed_domains: Set[str] = field(default_factory=set)   # 允许的域名（空=不限）
    excluded_patterns: Set[str] = field(default_factory=lambda: {
        r"/login", r"/signup", r"/logout", r"/account",
        r"javascript:", r"mailto:", r"tel:",
        r"\.(jpg|jpeg|png|gif|svg|css|js|woff|ttf)(\?|$)",
    })
    url_pattern: str = ""                 # URL正则匹配（可选）
    # 去重
    dedup_enabled: bool = True
    similarity_threshold: float = 0.9     # 内容相似度阈值


@dataclass
class FetchResult:
    """抓取结果"""
    url: str
    title: str = ""
    content: str = ""
    content_type: str = "text"
    depth: int = 0
    status_code: int = 0
    elapsed: float = 0.0
    links_found: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrawlStats:
    """爬取统计"""
    pages_attempted: int = 0
    pages_succeeded: int = 0
    pages_failed: int = 0
    pages_skipped: int = 0               # robots.txt/重复/过滤
    total_links_found: int = 0
    unique_content: int = 0
    duplicates: int = 0
    total_time: float = 0.0


class WebFetcher:
    """网页深度抓取器

    提供智能化的网页内容抓取能力，支持深度爬取、内容提取和去重。

    示例:
        config = FetchConfig(max_depth=2, max_pages=20)
        fetcher = WebFetcher(config)
        items = await fetcher.fetch("https://example.com/article")
        # 或深度爬取
        items = await fetcher.crawl("https://example.com", query="人工智能")
    """

    def __init__(self, config: Optional[FetchConfig] = None):
        self.config = config or FetchConfig()
        self._session = None
        self._visited: Set[str] = set()
        self._content_hashes: Set[str] = set()
        self._robots_cache: Dict[str, Set[str]] = {}
        self._stats = CrawlStats()
        self._start_time: float = 0

    async def fetch(self, url: str, depth: int = 0) -> List[KnowledgeItem]:
        """抓取单个URL（不爬取链接）

        Args:
            url: 目标URL
            depth: 当前深度（仅用于标记）

        Returns:
            KnowledgeItem列表（通常1个）
        """
        self._start_time = time.time()
        self._ensure_session()

        try:
            result = await self._fetch_single(url, depth)
            items = []

            if result and result.content and len(result.content) >= self.config.min_content_length:
                ki = self._to_knowledge_item(result)
                if ki:
                    items.append(ki)

            self._stats.total_time = time.time() - self._start_time
            return items
        finally:
            # ★ v1.2 修复: 非 crawl 模式的 fetch 调用后自动关闭 session，防止资源泄露
            # crawl 模式由调用方管理 session 生命周期
            await self.close()

    async def crawl(self, start_url: str, query: str = "") -> List[KnowledgeItem]:
        """深度爬取（从起始URL出发，沿链接递归抓取）

        Args:
            start_url: 起始URL
            query: 查询关键词（用于内容相关性判断）

        Returns:
            所有抓取到的KnowledgeItem列表
        """
        self._start_time = time.time()
        self._ensure_session()
        self._visited.clear()

        start_domain = urlparse(start_url).netloc
        if not self.config.allowed_domains:
            self.config.allowed_domains = {start_domain}

        items = []
        queue = deque([(start_url, 0)])
        query_words = set(query.lower().split()) if query else set()

        try:
            while queue and len(items) < self.config.max_pages:
                url, depth = queue.popleft()

                # 检查限制
                if depth > self.config.max_depth:
                    continue
                if url in self._visited:
                    continue

                self._visited.add(url)
                self._stats.pages_attempted += 1

                # robots.txt检查
                if self.config.respect_robots_txt:
                    allowed = await self._is_allowed(url)
                    if not allowed:
                        self._stats.pages_skipped += 1
                        continue

                # URL模式匹配
                if self.config.url_pattern and not re.search(self.config.url_pattern, url):
                    self._stats.pages_skipped += 1
                    continue

                # 抓取
                await self._random_delay()
                result = await self._fetch_single(url, depth)

                if not result or not result.content:
                    self._stats.pages_failed += 1
                    continue

                self._stats.pages_succeeded += 1

                # 去重
                if self.config.dedup_enabled:
                    content_hash = hashlib.md5(result.content.encode()).hexdigest()
                    if content_hash in self._content_hashes:
                        self._stats.duplicates += 1
                        continue
                    self._content_hashes.add(content_hash)

                # 查询相关性检查（有query时）
                if query_words:
                    content_lower = result.content.lower()
                    relevance = sum(1 for w in query_words if w in content_lower)
                    if relevance == 0:
                        self._stats.pages_skipped += 1
                        continue

                ki = self._to_knowledge_item(result)
                if ki:
                    items.append(ki)
                    self._stats.unique_content += 1

                # 发现链接并入队
                if depth < self.config.max_depth:
                    links = result.metadata.get("_links", [])
                    for link in links:
                        if link not in self._visited:
                            queue.append((link, depth + 1))
                            self._stats.total_links_found += 1
        finally:
            # ★ v1.2 修复: crawl 结束后自动关闭 session，防止资源泄露
            await self.close()

        self._stats.total_time = time.time() - self._start_time
        return items

    def get_stats(self) -> Dict[str, Any]:
        """获取爬取统计"""
        return {
            "pages_attempted": self._stats.pages_attempted,
            "pages_succeeded": self._stats.pages_succeeded,
            "pages_failed": self._stats.pages_failed,
            "pages_skipped": self._stats.pages_skipped,
            "unique_content": self._stats.unique_content,
            "duplicates": self._stats.duplicates,
            "total_links_found": self._stats.total_links_found,
            "total_time": round(self._stats.total_time, 2),
        }

    def reset(self):
        """重置状态"""
        self._visited.clear()
        self._content_hashes.clear()
        self._robots_cache.clear()
        self._stats = CrawlStats()

    # ─────────────────────────────────────────
    # 核心抓取
    # ─────────────────────────────────────────

    async def _fetch_single(self, url: str, depth: int = 0) -> Optional[FetchResult]:
        """抓取单个页面"""
        for attempt in range(self.config.max_retries):
            try:
                headers = {
                    "User-Agent": random.choice(self.config.user_agents),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                }

                start = time.time()
                async with self._session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=self.config.timeout)) as resp:
                    elapsed = time.time() - start

                    if resp.status != 200:
                        continue

                    html = await resp.text()
                    content, links = self._extract_content(html, url)

                    return FetchResult(
                        url=url,
                        title=self._extract_title(html),
                        content=content,
                        depth=depth,
                        status_code=resp.status,
                        elapsed=elapsed,
                        links_found=len(links),
                        metadata={"_links": links},
                    )

            except asyncio.TimeoutError:
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.backoff_factor ** attempt)
                    continue
            except Exception:
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.backoff_factor ** attempt)
                    continue

        return None

    # ─────────────────────────────────────────
    # 内容提取策略
    # ─────────────────────────────────────────

    def _extract_content(self, html: str, url: str) -> Tuple[str, List[str]]:
        """提取网页正文和链接"""
        strategy = self.config.extract_strategy

        if strategy == "raw":
            return self._extract_raw(html), self._extract_links(html, url)
        elif strategy == "structured":
            return self._extract_structured(html), self._extract_links(html, url)
        elif strategy == "readability":
            return self._extract_readability(html), self._extract_links(html, url)
        else:  # auto
            content = self._extract_readability(html)
            if len(content) < self.config.min_content_length:
                content = self._extract_structured(html)
            return content, self._extract_links(html, url)

    def _extract_readability(self, html: str) -> str:
        """Readability风格正文提取（基于启发式规则）

        不依赖readability-lxml外部库，使用纯Python启发式算法。
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            # 移除噪声元素
            for tag in soup.find_all(["script", "style", "nav", "header", "footer",
                                       "aside", "iframe", "noscript", "form",
                                       "[role=navigation]", "[role=banner]",
                                       "[role=complementary]", "[role=contentinfo]"]):
                tag.decompose()

            # 移除隐藏元素
            for tag in soup.find_all(style=re.compile(r"display:\s*none|visibility:\s*hidden", re.I)):
                tag.decompose()

            # 候选段落评分
            candidates = []
            for tag in soup.find_all(["article", "main", "section", "div", "td"]):
                text = tag.get_text(strip=True)
                if not text or len(text) < self.config.min_content_length:
                    continue

                # 评分
                score = 0.0
                # 段落数量和长度
                paragraphs = tag.find_all("p")
                score += len(paragraphs) * 5
                text_len = len(text)
                score += min(text_len / 100, 50)

                # 标题加分
                for h in tag.find_all(["h1", "h2", "h3"]):
                    score += 10

                # 列表加分
                for _ in tag.find_all(["ul", "ol"]):
                    score += 5

                # ID/Class暗示
                tag_id = (tag.get("id") or "").lower()
                tag_class = " ".join(tag.get("class", [])).lower()
                positive_ids = ["article", "content", "post", "entry", "text", "body", "main", "story"]
                negative_ids = ["comment", "sidebar", "footer", "header", "nav", "ad", "sponsor", "social"]

                for pid in positive_ids:
                    if pid in tag_id or pid in tag_class:
                        score += 20
                for nid in negative_ids:
                    if nid in tag_id or nid in tag_class:
                        score -= 20

                candidates.append((score, tag))

            if not candidates:
                # 降级：直接提取所有段落
                return self._extract_structured(html)

            # 取最高分候选
            candidates.sort(key=lambda x: x[0], reverse=True)
            best = candidates[0][1]

            # 提取最终文本
            parts = []
            for p in best.find_all(["p", "h1", "h2", "h3", "h4", "li"]):
                text = p.get_text(strip=True)
                if text:
                    parts.append(text)

            content = "\n\n".join(parts)
            return content[:self.config.max_content_length]

        except ImportError:
            return self._extract_structured(html)
        except Exception:
            return ""

    def _extract_structured(self, html: str) -> str:
        """结构化提取：提取标题+段落+列表"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            parts = []
            # 标题
            for h in soup.find_all(["h1", "h2", "h3"]):
                text = h.get_text(strip=True)
                if text:
                    parts.append(f"## {text}")

            # 段落
            for p in soup.find_all("p"):
                text = p.get_text(strip=True)
                if text and len(text) > 10:
                    parts.append(text)

            content = "\n\n".join(parts)
            return content[:self.config.max_content_length]
        except Exception:
            return ""

    def _extract_raw(self, html: str) -> str:
        """原始HTML文本提取"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            return soup.get_text(separator="\n", strip=True)[:self.config.max_content_length]
        except Exception:
            return re.sub(r"<[^>]+>", "", html)[:self.config.max_content_length]

    def _extract_title(self, html: str) -> str:
        """提取页面标题"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title
            if title and title.string:
                return title.string.strip()
            # og:title
            og = soup.find("meta", property="og:title")
            if og and og.get("content"):
                return og["content"].strip()
        except Exception:
            pass  # return og['content'].strip()失败时静默忽略
        return ""

    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """提取页面中的有效链接"""
        links = []
        base_domain = urlparse(base_url).netloc

        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if not href or href.startswith("#"):
                    continue

                # 解析为绝对URL
                full_url = urljoin(base_url, href)
                parsed = urlparse(full_url)

                # 过滤
                skip = False
                for pattern in self.config.excluded_patterns:
                    if re.search(pattern, full_url, re.I):
                        skip = True
                        break
                if skip:
                    continue

                # 域名限制
                if self.config.allowed_domains and parsed.netloc and parsed.netloc not in self.config.allowed_domains:
                    continue

                # 只保留http/https
                if parsed.scheme not in ("http", "https"):
                    continue

                links.append(full_url)

        except Exception:
            pass  # links.append(full_url)失败时静默忽略

        return links

    # ─────────────────────────────────────────
    # robots.txt 与辅助
    # ─────────────────────────────────────────

    async def _is_allowed(self, url: str) -> bool:
        """检查URL是否被robots.txt允许"""
        parsed = urlparse(url)
        domain = parsed.netloc

        if domain not in self._robots_cache:
            self._robots_cache[domain] = await self._fetch_robots(domain)

        disallowed = self._robots_cache[domain]
        path = parsed.path or "/"

        for pattern in disallowed:
            if path.startswith(pattern):
                return False

        return True

    async def _fetch_robots(self, domain: str) -> Set[str]:
        """获取robots.txt中的禁止路径"""
        disallowed = set()
        try:
            url = f"https://{domain}/robots.txt"
            async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    in_user_agent = False
                    for line in text.splitlines():
                        line = line.strip().lower()
                        if line.startswith("user-agent:"):
                            agent = line.split(":", 1)[1].strip()
                            in_user_agent = (agent == "*" or "openclaw" in agent)
                        elif in_user_agent and line.startswith("disallow:"):
                            path = line.split(":", 1)[1].strip()
                            if path:
                                disallowed.add(path)
        except Exception:
            pass  # disallowed.add(path)失败时静默忽略
        return disallowed

    def _to_knowledge_item(self, result: FetchResult) -> Optional[KnowledgeItem]:
        """将FetchResult转换为KnowledgeItem"""
        if not result.content or len(result.content) < self.config.min_content_length:
            return None

        return KnowledgeItem(
            id=f"fetch_{hashlib.md5(result.url.encode()).hexdigest()[:12]}",
            content=result.content,
            source=result.url,
            metadata={
                "title": result.title,
                "depth": result.depth,
                "format": "web_page",
                "status_code": result.status_code,
                "elapsed": result.elapsed,
                "links_found": result.links_found,
            },
            confidence=0.75,
        )

    def _ensure_session(self):
        """确保HTTP会话"""
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def _random_delay(self):
        """随机延迟"""
        low, high = self.config.delay_range
        delay = random.uniform(low, high)
        await asyncio.sleep(delay)

    async def close(self):
        """关闭会话"""
        if self._session:
            await self._session.close()
            self._session = None


__all__ = [
    'WebFetcher',
    'FetchConfig',
    'FetchResult',
    'CrawlStats',
]
