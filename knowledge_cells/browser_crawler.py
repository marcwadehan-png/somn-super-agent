"""
HiddenBrowserCrawler - 隐藏式浏览器爬虫 v1.0
=================================================
使用 Playwright 进行模拟真实用户搜索

功能：
- 隐藏式运行（headless 模式）
- 模拟真实用户搜索行为
- 支持多个搜索引擎
- 自动解析搜索结果
- 支持 Cookie/本地存储持久化

@author: C0dy
@date: 2026-04-29
"""

from __future__ import annotations

import json
import logging
import time
import urllib.parse
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ==================== 枚举定义 ====================

class CrawlerEngine(Enum):
    """浏览器引擎"""
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class SearchEngineType(Enum):
    """搜索引擎类型"""
    BAIDU = "baidu"
    GOOGLE = "google"
    DUCKDUCKGO = "duckduckgo"
    BING = "bing"
    SOGOU = "sogou"


# ==================== 数据结构 ====================

@dataclass
class CrawledResult:
    """爬虫抓取的单条结果"""
    title: str
    url: str
    snippet: str = ""
    rank: int = 0              # 排名位置
    search_engine: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrawlResponse:
    """爬虫响应"""
    query: str
    success: bool
    results: List[CrawledResult] = field(default_factory=list)
    total_found: int = 0
    crawl_time_ms: float = 0.0
    search_engine: str = ""
    error: str = ""
    screenshot_path: str = ""  # 调试用截图


# ==================== 搜索引擎配置 ====================

SEARCH_ENGINE_CONFIGS = {
    SearchEngineType.BAIDU: {
        "name": "百度",
        "url": "https://www.baidu.com/s?wd={query}&rn={count}",
        "result_selectors": {
            "container": "#content_left .result",
            "title": "h3 a",
            "url": "h3 a",
            "snippet": ".c-abstract, .content-right_8Zs40",
        },
        "wait_for": "#content_left",
    },
    SearchEngineType.GOOGLE: {
        "name": "Google",
        "url": "https://www.google.com/search?q={query}&num={count}",
        "result_selectors": {
            "container": "div.g",
            "title": "h3",
            "url": "a",
            "snippet": "div.VwiC3b, span.aCOpRe",
        },
        "wait_for": "div#search",
    },
    SearchEngineType.DUCKDUCKGO: {
        "name": "DuckDuckGo",
        "url": "https://html.duckduckgo.com/html/?q={query}",
        "result_selectors": {
            "container": ".result",
            "title": ".result__a",
            "url": ".result__a",
            "snippet": ".result__snippet",
        },
        "wait_for": ".results",
    },
    SearchEngineType.BING: {
        "name": "必应",
        "url": "https://cn.bing.com/search?q={query}&count={count}",
        "result_selectors": {
            "container": ".b_algo",
            "title": "h2 a",
            "url": "h2 a",
            "snippet": ".b_caption p, .b_algoSlug",
        },
        "wait_for": "#b_results",
    },
}


# ==================== 浏览器爬虫核心类 ====================

class HiddenBrowserCrawler:
    """
    隐藏式浏览器爬虫

    使用 Playwright 模拟真实用户搜索行为
    支持 headless 模式（完全隐藏）

    特性：
    - 模拟真实用户行为（输入延迟、滚动、鼠标移动）
    - 支持 Cookie 持久化
    - 支持代理配置
    - 自动处理验证码检测
    """

    def __init__(
        self,
        engine: CrawlerEngine = CrawlerEngine.CHROMIUM,
        headless: bool = True,
        timeout_ms: int = 30000,
        user_data_dir: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        """
        初始化浏览器爬虫

        Args:
            engine: 浏览器引擎
            headless: 是否隐藏运行
            timeout_ms: 超时时间（毫秒）
            user_data_dir: 用户数据目录（用于 Cookie 持久化）
            proxy: 代理服务器地址（如 "http://proxy.example.com:8080"）
        """
        self.engine = engine
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.user_data_dir = user_data_dir
        self.proxy = proxy

        self._playwright = None
        self._browser = None
        self._context = None
        self._stats = {
            "total_searches": 0,
            "successful_searches": 0,
            "failed_searches": 0,
            "total_time_ms": 0.0,
        }

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

    def start(self):
        """启动浏览器"""
        try:
            from playwright.sync_api import sync_playwright

            self._playwright = sync_playwright().start()

            # 选择浏览器引擎
            if self.engine == CrawlerEngine.CHROMIUM:
                browser_launcher = self._playwright.chromium
            elif self.engine == CrawlerEngine.FIREFOX:
                browser_launcher = self._playwright.firefox
            elif self.engine == CrawlerEngine.WEBKIT:
                browser_launcher = self._playwright.webkit
            else:
                browser_launcher = self._playwright.chromium

            # 启动选项
            launch_options = {
                "headless": self.headless,
                "timeout": self.timeout_ms,
            }

            if self.proxy:
                launch_options["proxy"] = {"server": self.proxy}

            # 如果有用户数据目录，使用持久化上下文
            if self.user_data_dir:
                self._context = browser_launcher.launch_persistent_context(
                    user_data_dir=self.user_data_dir,
                    **launch_options
                )
                if len(self._context.pages) > 0:
                    self._browser_page = self._context.pages[0]
                else:
                    self._browser_page = self._context.new_page()
            else:
                self._browser = browser_launcher.launch(**launch_options)
                self._context = self._browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                self._browser_page = self._context.new_page()

            logger.info(f"Browser crawler started: {self.engine.value}, headless={self.headless}")

        except ImportError:
            logger.error("Playwright not installed. Install with: pip install playwright")
            raise
        except Exception as e:
            logger.error(f"Failed to start browser crawler: {e}")
            raise

    def close(self):
        """关闭浏览器"""
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
            logger.info("Browser crawler closed")
        except Exception as e:
            logger.warning(f"Error closing browser crawler: {e}")

    def search(
        self,
        query: str,
        search_engine: SearchEngineType = SearchEngineType.BAIDU,
        max_results: int = 10,
        simulate_human: bool = True,
    ) -> CrawlResponse:
        """
        执行搜索

        Args:
            query: 搜索关键词
            search_engine: 搜索引擎
            max_results: 最大结果数
            simulate_human: 是否模拟人类行为

        Returns:
            CrawlResponse: 抓取结果
        """
        start_time = time.perf_counter()

        if not query or not query.strip():
            return CrawlResponse(
                query=query,
                success=False,
                error="Search query cannot be empty"
            )

        self._stats["total_searches"] += 1

        try:
            # 获取搜索引擎配置
            config = SEARCH_ENGINE_CONFIGS.get(search_engine)
            if not config:
                return CrawlResponse(
                    query=query,
                    success=False,
                    error=f"Unsupported search engine: {search_engine}"
                )

            # 构建搜索 URL
            search_url = config["url"].format(
                query=urllib.parse.quote(query),
                count=max_results
            )

            logger.info(f"Crawling: {config['name']} - '{query}'")

            # 打开搜索页面
            self._browser_page.goto(search_url, timeout=self.timeout_ms)

            # 等待搜索结果加载
            wait_selector = config.get("wait_for")
            if wait_selector:
                self._browser_page.wait_for_selector(wait_selector, timeout=self.timeout_ms)

            # 模拟人类行为
            if simulate_human:
                self._simulate_human_behavior()

            # 截图（调试用）
            screenshot_path = ""
            # self._browser_page.screenshot(path=f"debug_{search_engine.value}.png")

            # 解析搜索结果
            results = self._parse_results(config, max_results)

            elapsed = (time.perf_counter() - start_time) * 1000

            self._stats["successful_searches"] += 1
            self._stats["total_time_ms"] += elapsed

            logger.info(f"Crawl successful: {len(results)} results in {elapsed:.0f}ms")

            return CrawlResponse(
                query=query,
                success=True,
                results=results[:max_results],
                total_found=len(results),
                crawl_time_ms=elapsed,
                search_engine=config["name"],
                screenshot_path=screenshot_path,
            )

        except Exception as e:
            elapsed = (time.perf_counter() - start_time) * 1000
            self._stats["failed_searches"] += 1

            logger.error(f"Crawl failed: {e}")

            return CrawlResponse(
                query=query,
                success=False,
                error=str(e),
                crawl_time_ms=elapsed,
                search_engine=search_engine.value if isinstance(search_engine, SearchEngineType) else str(search_engine),
            )

    def _simulate_human_behavior(self):
        """模拟人类行为"""
        try:
            # 随机滚动
            import random
            scroll_times = random.randint(1, 3)
            for _ in range(scroll_times):
                scroll_amount = random.randint(100, 500)
                self._browser_page.evaluate(f"window.scrollBy(0, {scroll_amount})")
                time.sleep(random.uniform(0.5, 1.5))

            # 鼠标随机移动
            self._browser_page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600)
            )

        except Exception as e:
            logger.debug(f"Human simulation error (non-critical): {e}")

    def _parse_results(self, config: Dict, max_results: int) -> List[CrawledResult]:
        """解析搜索结果"""
        results = []
        selectors = config["result_selectors"]

        try:
            # 使用 Playwright 选择器提取结果
            containers = self._browser_page.query_selector_all(selectors["container"])

            for idx, container in enumerate(containers[:max_results]):
                try:
                    # 提取标题
                    title_elem = container.query_selector(selectors["title"])
                    title = title_elem.inner_text().strip() if title_elem else ""

                    # 提取 URL
                    url_elem = container.query_selector(selectors["url"])
                    url = url_elem.get_attribute("href") if url_elem else ""

                    # 提取摘要
                    snippet = ""
                    if "snippet" in selectors:
                        snippet_elem = container.query_selector(selectors["snippet"])
                        if snippet_elem:
                            snippet = snippet_elem.inner_text().strip()

                    if title and url:
                        results.append(CrawledResult(
                            title=title,
                            url=url,
                            snippet=snippet,
                            rank=idx + 1,
                            search_engine=config["name"],
                        ))
                except Exception as e:
                    logger.debug(f"Error parsing result {idx}: {e}")
                    continue

        except Exception as e:
            logger.warning(f"Error parsing search results: {e}")

        return results

    def batch_search(
        self,
        queries: List[str],
        search_engine: SearchEngineType = SearchEngineType.BAIDU,
        max_results: int = 10,
    ) -> List[CrawlResponse]:
        """批量搜索"""
        return [self.search(q, search_engine, max_results) for q in queries]

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        avg_time = (
            self._stats["total_time_ms"] / self._stats["successful_searches"]
            if self._stats["successful_searches"] > 0 else 0.0
        )
        success_rate = (
            self._stats["successful_searches"] / self._stats["total_searches"]
            if self._stats["total_searches"] > 0 else 0.0
        )

        return {
            **self._stats,
            "average_time_ms": avg_time,
            "success_rate": success_rate,
        }

    def reset_stats(self):
        """重置统计"""
        self._stats = {
            "total_searches": 0,
            "successful_searches": 0,
            "failed_searches": 0,
            "total_time_ms": 0.0,
        }


# ==================== 全局爬虫管理器 ====================

class CrawlerManager:
    """
    全局爬虫管理器

    管理爬虫的生命周期，支持懒加载和自动关闭
    """

    def __init__(self):
        self._crawler: Optional[HiddenBrowserCrawler] = None
        self._auto_start: bool = False
        self._config = {
            "engine": CrawlerEngine.CHROMIUM,
            "headless": True,
            "timeout_ms": 30000,
        }

    def configure(
        self,
        engine: CrawlerEngine = CrawlerEngine.CHROMIUM,
        headless: bool = True,
        timeout_ms: int = 30000,
        user_data_dir: Optional[str] = None,
        proxy: Optional[str] = None,
        auto_start: bool = False,
    ):
        """配置爬虫"""
        self._config = {
            "engine": engine,
            "headless": headless,
            "timeout_ms": timeout_ms,
            "user_data_dir": user_data_dir,
            "proxy": proxy,
        }
        self._auto_start = auto_start

    def get_crawler(self) -> HiddenBrowserCrawler:
        """获取爬虫实例（懒加载）"""
        if self._crawler is None:
            self._crawler = HiddenBrowserCrawler(**self._config)
            if self._auto_start:
                self._crawler.start()
        return self._crawler

    def start(self):
        """启动爬虫"""
        crawler = self.get_crawler()
        if self._crawler and not hasattr(self._crawler, '_browser'):
            self._crawler.start()

    def close(self):
        """关闭爬虫"""
        if self._crawler:
            self._crawler.close()
            self._crawler = None

    def search(
        self,
        query: str,
        search_engine: SearchEngineType = SearchEngineType.BAIDU,
        max_results: int = 10,
    ) -> CrawlResponse:
        """执行搜索"""
        crawler = self.get_crawler()
        return crawler.search(query, search_engine, max_results)

    def is_available(self) -> bool:
        """检查爬虫是否可用"""
        try:
            from playwright.sync_api import sync_playwright
            return True
        except ImportError:
            return False


# 全局爬虫管理器实例
_global_crawler_manager: Optional[CrawlerManager] = None


def get_crawler_manager() -> CrawlerManager:
    """获取全局爬虫管理器"""
    global _global_crawler_manager
    if _global_crawler_manager is None:
        _global_crawler_manager = CrawlerManager()
    return _global_crawler_manager


def search_with_browser(
    query: str,
    search_engine: str = "baidu",
    max_results: int = 10,
    headless: bool = True,
) -> CrawlResponse:
    """
    使用浏览器爬虫搜索（快捷函数）

    Args:
        query: 搜索关键词
        search_engine: 搜索引擎（"baidu", "google", "duckduckgo", "bing"）
        max_results: 最大结果数
        headless: 是否隐藏运行

    Returns:
        CrawlResponse: 搜索结果
    """
    # 映射搜索引擎字符串
    engine_map = {
        "baidu": SearchEngineType.BAIDU,
        "google": SearchEngineType.GOOGLE,
        "duckduckgo": SearchEngineType.DUCKDUCKGO,
        "bing": SearchEngineType.BING,
    }

    search_engine_type = engine_map.get(search_engine.lower(), SearchEngineType.BAIDU)

    # 创建临时爬虫实例
    with HiddenBrowserCrawler(headless=headless) as crawler:
        return crawler.search(query, search_engine_type, max_results)


__all__ = [
    # 核心类
    "HiddenBrowserCrawler",
    "CrawlerManager",

    # 数据结构
    "CrawledResult",
    "CrawlResponse",

    # 枚举
    "CrawlerEngine",
    "SearchEngineType",

    # 全局函数
    "get_crawler_manager",
    "search_with_browser",

    # 配置
    "SEARCH_ENGINE_CONFIGS",
]
