# -*- coding: utf-8 -*-
"""
Web数据源连接器 - 从互联网抓取知识

功能:
- 网页内容抓取
- 搜索结果解析
- 结构化提取

版本: v1.0.0
"""

from __future__ import annotations
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp
import re
from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup

from ._openclaw_core import DataSourceConnector, DataSourceType, KnowledgeItem

logger = logging.getLogger(__name__)


@dataclass
class WebConfig:
    """网页数据源配置"""
    base_url: str = ""
    search_engine: str = "bing"  # bing/google/duckduckgo
    timeout: int = 30
    headers: Dict[str, str] = field(default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })


class WebDataSource(DataSourceConnector):
    """网页数据源连接器"""
    
    def __init__(self, config: WebConfig):
        super().__init__(DataSourceType.WEB, config.__dict__)
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self._cache: Dict[str, List[KnowledgeItem]] = {}
    
    async def connect(self) -> bool:
        """建立连接"""
        try:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(
                headers=self.config.headers,
                timeout=timeout
            )
            self.connected = True
            return True
        except Exception:
            self.connected = False
            return False
    
    async def disconnect(self) -> bool:
        """断开连接"""
        if self.session:
            await self.session.close()
            self.session = None
        self.connected = False
        return True
    
    async def fetch(self, query: str) -> List[KnowledgeItem]:
        """抓取网页数据"""
        if not self.connected:
            await self.connect()
        
        results = []
        
        # 搜索
        search_urls = self._build_search_urls(query)
        for url in search_urls[:3]:
            items = await self._fetch_page(url, query)
            results.extend(items)
        
        return results
    
    def _build_search_urls(self, query: str) -> List[str]:
        """构建搜索URL"""
        encoded = quote_plus(query)
        
        engines = {
            "bing": f"https://www.bing.com/search?q={encoded}",
            "google": f"https://www.google.com/search?q={encoded}",
            "duckduckgo": f"https://duckduckgo.com/?q={encoded}",
        }
        
        base = engines.get(self.config.search_engine, engines["bing"])
        return [base]
    
    async def _fetch_page(self, url: str, query: str) -> List[KnowledgeItem]:
        """抓取单个页面"""
        items = []
        
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 提取标题和内容
                    title = soup.title.string.strip() if soup.title and soup.title.string else "无标题"
                    
                    # 提取正文
                    for p in soup.find_all('p')[:10]:
                        if p.get_text(strip=True):
                            items.append(KnowledgeItem(
                                id=f"web_{hash(url+p.text[:20])}",
                                content=p.text[:500],
                                source=url,
                                metadata={
                                    "title": title,
                                    "query": query,
                                    "url": url
                                }
                            ))
        except Exception as e:
            logger.debug(f"Web数据源扫描异常: {e}")

        return items

    async def fetch_url(self, url: str) -> KnowledgeItem | None:
        """抓取指定URL"""
        if not self.connected:
            await self.connect()

        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.title.string.strip() if soup.title and soup.title.string else "无标题"
                    text = ' '.join(p.text for p in soup.find_all('p')[:20])

                    return KnowledgeItem(
                        id=f"web_{hash(url)}",
                        content=text[:2000],
                        source=url,
                        metadata={"title": title}
                    )
        except Exception as e:
            logger.debug(f"fetch_url异常: {e}")
        return None


__all__ = ['WebDataSource', 'WebConfig']
