"""
AutoStarter → CrawlerService - Somn 爬虫后台服务 v1.0
=====================================================
当 Somn 后端启动时，自动启动隐藏式浏览器爬虫

架构：
- Somn 启动时自动初始化（api/deps.py AppState.initialize）
- 懒加载：首次搜索才真正启动浏览器（可配置预热）
- 后台运行，完全隐藏（headless）
- 随 Somn 关闭自动清理（AppState.shutdown）

@author: C0dy
@date: 2026-04-29
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

# ==================== 爬虫服务配置 ====================

CRAWLER_CONFIG = {
    "enabled": True,           # 是否启用爬虫服务
    "headless": True,         # 隐藏式运行（无窗口）
    "lazy_start": True,       # 懒加载：首次搜索才启动浏览器
    "engine": "chromium",     # 浏览器引擎：chromium/firefox/webkit
    "warmup_on_start": False, # Somn 启动时是否预热浏览器
    "default_search_engine": "baidu",  # 默认搜索引擎
    "default_max_results": 10,
}


# ==================== 爬虫服务类 ====================

class CrawlerService:
    """
    Somn 爬虫后台服务

    生命周期：
    - Somn 启动时：AppState.initialize() 调用 init_crawler_service()
    - 懒加载：首次 search() 时才真正启动浏览器
    - Somn 关闭时：AppState.shutdown() 调用 shutdown_crawler_service()

    使用方式：
        # 方式1：通过 AppState（推荐）
        app_state = get_app_state()
        if app_state.crawler_service:
            result = app_state.crawler_service.search("查询")

        # 方式2：直接导入单例
        from knowledge_cells.auto_starter import get_crawler_service
        svc = get_crawler_service()
        result = svc.search("人工智能")
    """

    _instance: Optional["CrawlerService"] = None
    _lock = threading.Lock()

    def __init__(self, config: Dict = None):
        self._config = {**CRAWLER_CONFIG, **(config or {})}
        self._crawler = None       # HiddenBrowserCrawler 实例
        self._crawler_lock = threading.Lock()
        self._started = False
        self._start_time: Optional[float] = None
        self._stats = {
            "total_searches": 0,
            "successful_searches": 0,
            "failed_searches": 0,
        }

        if CrawlerService._instance is not None:
            logger.warning("[CrawlerService] 单例已存在，请使用 get_crawler_service()")

    # ── 单例访问 ──────────────────────────────────────────────

    @classmethod
    def get_instance(cls) -> "CrawlerService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    logger.info("[CrawlerService] 单例已创建")
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """仅用于测试"""
        with cls._lock:
            if cls._instance is not None:
                cls._instance.shutdown()
                cls._instance = None

    # ── 生命周期 ──────────────────────────────────────────────

    def start(self, warmup: bool = None):
        """
        启动爬虫服务

        Args:
            warmup: 是否立即预热浏览器
                    None = 使用配置中的 warmup_on_start
                    True/False = 覆盖配置
        """
        if self._started:
            logger.debug("[CrawlerService] 已启动，跳过")
            return

        with self._crawler_lock:
            if self._started:
                return

            if not self._config.get("enabled", True):
                logger.info("[CrawlerService] 已禁用，不启动")
                return

            self._start_time = time.time()

            warmup = warmup if warmup is not None else self._config.get("warmup_on_start", False)
            if warmup:
                self._do_start_browser()
            else:
                logger.info("[CrawlerService] 懒加载模式，浏览器将在首次搜索时启动")

            self._started = True
            logger.info("[CrawlerService] 服务已就绪")

    def shutdown(self):
        """关闭爬虫服务（随 Somn 关闭时调用）"""
        if not self._started:
            return

        logger.info("[CrawlerService] 正在关闭...")

        with self._crawler_lock:
            if self._crawler is not None:
                try:
                    self._crawler.close()
                    logger.info("[CrawlerService] 浏览器已关闭")
                except Exception as e:
                    logger.warning(f"[CrawlerService] 关闭浏览器时出错: {e}")
                finally:
                    self._crawler = None

            self._started = False
            self._start_time = None

    def _do_start_browser(self):
        """实际启动浏览器（线程安全，内部调用）"""
        try:
            from knowledge_cells.browser_crawler import HiddenBrowserCrawler, CrawlerEngine

            engine_name = self._config.get("engine", "chromium")
            engine_map = {
                "chromium": CrawlerEngine.CHROMIUM,
                "firefox": CrawlerEngine.FIREFOX,
                "webkit": CrawlerEngine.WEBKIT,
            }
            engine = engine_map.get(engine_name, CrawlerEngine.CHROMIUM)

            self._crawler = HiddenBrowserCrawler(
                engine=engine,
                headless=self._config.get("headless", True),
                timeout_ms=30000,
            )
            self._crawler.start()
            elapsed = time.time() - self._start_time
            logger.info(f"[CrawlerService] 浏览器已启动 (engine={engine_name}, headless=True, 耗时={elapsed:.1f}s)")

        except ImportError:
            logger.warning("[CrawlerService] Playwright 未安装，浏览器不可用")
            logger.warning("  安装: pip install playwright && playwright install chromium")
        except Exception as e:
            logger.warning(f"[CrawlerService] 启动浏览器失败: {e}")

    def _ensure_browser(self):
        """确保浏览器已启动（懒加载触发）"""
        if self._crawler is None and self._started:
            self._do_start_browser()

    # ── 搜索接口 ──────────────────────────────────────────────

    def search(
        self,
        query: str,
        search_engine: str = None,
        max_results: int = None,
    ) -> Dict[str, Any]:
        """
        执行爬虫搜索

        Args:
            query: 搜索关键词
            search_engine: 搜索引擎（baidu/google/duckduckgo/bing，默认用配置）
            max_results: 最大结果数（默认用配置）

        Returns:
            {
                "success": bool,
                "results": [{"title","url","snippet","rank"}],
                "source": str,   # "crawler_baidu" / "http_baidu" / "fallback"
                "error": str,
            }
        """
        self._stats["total_searches"] += 1

        if not query or not query.strip():
            return {"success": False, "results": [], "source": "crawler", "error": "搜索关键词不能为空"}

        # 填充默认值
        if search_engine is None:
            search_engine = self._config.get("default_search_engine", "baidu")
        if max_results is None:
            max_results = self._config.get("default_max_results", 10)

        # 检查是否启用
        if not self._config.get("enabled", True):
            return {"success": False, "results": [], "source": "crawler", "error": "爬虫服务已禁用"}

        # 确保浏览器已启动（懒加载）
        self._ensure_browser()

        # 浏览器可用 → 直接爬取
        if self._crawler is not None:
            try:
                from knowledge_cells.browser_crawler import SearchEngineType

                engine_map = {
                    "baidu": SearchEngineType.BAIDU,
                    "google": SearchEngineType.GOOGLE,
                    "duckduckgo": SearchEngineType.DUCKDUCKGO,
                    "bing": SearchEngineType.BING,
                }
                engine_type = engine_map.get(search_engine.lower(), SearchEngineType.BAIDU)

                response = self._crawler.search(
                    query=query,
                    search_engine=engine_type,
                    max_results=max_results,
                    simulate_human=True,
                )

                if response.success and response.results:
                    self._stats["successful_searches"] += 1
                    return {
                        "success": True,
                        "results": [
                            {"title": r.title, "url": r.url, "snippet": r.snippet, "rank": r.rank, "source": r.search_engine}
                            for r in response.results
                        ],
                        "source": f"crawler_{search_engine}",
                        "total_found": response.total_found,
                        "crawl_time_ms": response.crawl_time_ms,
                    }
                else:
                    self._stats["failed_searches"] += 1
                    logger.warning(f"[CrawlerService] 爬虫无结果，降级到 HTTP 搜索: {query}")
                    return self._fallback_http_search(query, search_engine, max_results)

            except Exception as e:
                self._stats["failed_searches"] += 1
                logger.error(f"[CrawlerService] 搜索失败: {e}")
                return self._fallback_http_search(query, search_engine, max_results)

        # 浏览器不可用 → 降级到 HTTP 搜索
        self._stats["failed_searches"] += 1
        return self._fallback_http_search(query, search_engine, max_results)

    def _fallback_http_search(self, query: str, search_engine: str, max_results: int) -> Dict[str, Any]:
        """降级：使用 HTTP 搜索（web_search_engine）"""
        try:
            from knowledge_cells.web_search_engine import search_web

            response = search_web(query, max_results)

            if response.success and response.results:
                return {
                    "success": True,
                    "results": [
                        {"title": r.title, "url": r.url, "snippet": r.snippet, "rank": idx + 1,
                         "source": r.source or r.search_engine}
                        for idx, r in enumerate(response.results)
                    ],
                    "source": f"http_{search_engine}",
                    "total_found": response.total_found,
                    "search_time_ms": response.search_time_ms,
                }
        except Exception as e:
            logger.warning(f"[CrawlerService] HTTP 降级搜索失败: {e}")

        return {"success": False, "results": [], "source": "fallback", "error": "所有搜索方式均失败"}

    def batch_search(
        self,
        queries: List[str],
        search_engine: str = None,
        max_results: int = None,
    ) -> List[Dict[str, Any]]:
        """批量搜索"""
        return [self.search(q, search_engine, max_results) for q in queries]

    # ── 状态查询 ──────────────────────────────────────────────

    def is_ready(self) -> bool:
        """浏览器是否已启动就绪"""
        return self._crawler is not None

    def is_available(self) -> bool:
        """服务是否已启动且启用"""
        return self._started and self._config.get("enabled", True)

    def get_status(self) -> Dict[str, Any]:
        return {
            "enabled": self._config.get("enabled", True),
            "started": self._started,
            "browser_ready": self._crawler is not None,
            "headless": self._config.get("headless", True),
            "engine": self._config.get("engine", "chromium"),
            "lazy_start": self._config.get("lazy_start", True),
            "uptime_seconds": (time.time() - self._start_time) if self._start_time else 0,
            "stats": {**self._stats},
        }

    def get_stats(self) -> Dict[str, Any]:
        total = self._stats["total_searches"]
        success_rate = (self._stats["successful_searches"] / total) if total > 0 else 0.0
        return {**self._stats, "success_rate": round(success_rate, 3)}

    # ── 配置修改 ──────────────────────────────────────────────

    def configure(self, **kwargs):
        """更新配置（仅未启动时有效）"""
        if self._started:
            logger.warning("[CrawlerService] 服务已启动，配置更新将在下次生效")
        self._config.update(kwargs)

    def enable(self):
        self._config["enabled"] = True

    def disable(self):
        self._config["enabled"] = False


# ==================== 全局单例管理函数 ====================

def get_crawler_service() -> CrawlerService:
    """获取爬虫服务单例"""
    return CrawlerService.get_instance()


def init_crawler_service(config: Dict = None) -> CrawlerService:
    """
    初始化爬虫服务（由 api/deps.py AppState.initialize() 调用）

    Args:
        config: 爬虫配置字典，合并到 CRAWLER_CONFIG

    Returns:
        CrawlerService 实例
    """
    svc = get_crawler_service()
    if config:
        svc.configure(**config)

    # 启动服务（懒加载模式：不立即启动浏览器）
    svc.start(warmup=config.get("warmup_on_start", False) if config else False)

    return svc


def shutdown_crawler_service():
    """关闭爬虫服务（由 api/deps.py AppState.shutdown() 调用）"""
    svc = CrawlerService._instance
    if svc:
        svc.shutdown()


# ==================== 快捷搜索函数 ====================

def crawler_search(
    query: str,
    search_engine: str = "baidu",
    max_results: int = 10,
) -> Dict[str, Any]:
    """快捷搜索（自动确保服务已启动）"""
    svc = get_crawler_service()
    if not svc.is_available():
        svc.start()
    return svc.search(query, search_engine, max_results)


# ==================== 导出 ====================

__all__ = [
    # 核心类
    "CrawlerService",
    # 单例管理
    "get_crawler_service",
    "init_crawler_service",
    "shutdown_crawler_service",
    # 快捷函数
    "crawler_search",
    # 配置
    "CRAWLER_CONFIG",
]
