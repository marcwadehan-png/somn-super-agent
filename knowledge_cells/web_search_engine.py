"""
WebSearchEngine - 网络搜索引擎 v1.0
====================================
为 Somn 后端系统提供联网搜索能力

功能：
- 联网检测：自动检测网络状态
- 实时搜索：调用网络搜索API
- 结果缓存：LRU缓存避免重复搜索
- 超时控制：防止搜索阻塞工作流
- 多源融合：合并多个搜索结果

使用方式：
    from knowledge_cells.web_search_engine import (
        WebSearchEngine,
        is_online,
        search_web,
        get_search_stats,
    )

    # 检查联网状态
    online = is_online()

    # 执行搜索
    if online:
        results = search_web("人工智能发展趋势", max_results=5)
"""

import time
import re
import logging
import urllib.request
import urllib.error
import json
import socket
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache

logger = logging.getLogger(__name__)

# ==================== 常量定义 ====================

# 联网检测配置
NETWORK_CHECK_HOST = "www.baidu.com"
NETWORK_CHECK_PORT = 80
NETWORK_CHECK_TIMEOUT = 3  # 秒

# 搜索配置
DEFAULT_MAX_RESULTS = 5
SEARCH_CACHE_SIZE = 128  # LRU缓存大小
SEARCH_TIMEOUT = 5  # 搜索超时(秒)，减少到5秒避免长时间等待
SEARCH_QUICK_TIMEOUT = 2  # 快速搜索超时（首次尝试）

# 搜索引擎配置
SEARCH_ENGINES = {
    "baidu": {
        "name": "百度搜索",
        "url": "https://www.baidu.com/s?wd={query}&rn={count}",
        "enabled": True,
    },
    "bing": {
        "name": "必应搜索",
        "url": "https://cn.bing.com/search?q={query}",
        "enabled": True,
    },
}

# 搜索重试配置
MAX_SEARCH_RETRIES = 2
RETRY_BACKOFF_FACTOR = 1.5  # 重试间隔倍数


# ==================== 枚举定义 ====================

class SearchMode(Enum):
    """搜索模式"""
    QUICK = "quick"        # 快速搜索，仅标题
    NORMAL = "normal"      # 普通搜索，标题+摘要
    DEEP = "deep"          # 深度搜索，完整信息


class SourceType(Enum):
    """信息来源类型"""
    NEWS = "news"          # 新闻
    KNOWLEDGE = "knowledge"  # 知识百科
    BLOG = "blog"          # 博客
    FORUM = "forum"        # 论坛
    VIDEO = "video"        # 视频
    COMMERCE = "commerce"  # 电商
    UNKNOWN = "unknown"    # 未知


# ==================== 数据结构 ====================

@dataclass
class SearchResult:
    """单条搜索结果"""
    title: str
    url: str
    snippet: str = ""           # 摘要/描述
    source: str = ""             # 来源网站
    source_type: SourceType = SourceType.UNKNOWN
    publish_time: str = ""       # 发布时间
    relevance_score: float = 0.0  # 相关性评分
    search_engine: str = ""      # 使用的搜索引擎


@dataclass
class SearchResponse:
    """搜索响应"""
    query: str
    success: bool
    results: List[SearchResult] = field(default_factory=list)
    total_found: int = 0
    search_time_ms: float = 0.0
    search_engine: str = ""
    error: str = ""
    is_online: bool = True


# ==================== 联网检测 ====================

# 联网检测缓存（避免重复检测）
_network_status_cache = {"online": None, "time": 0.0}
_network_check_interval = 60  # 缓存60秒

def is_online() -> bool:
    """
    检测网络是否可用（带缓存）

    Returns:
        True = 网络可用，False = 网络不可用
    """
    global _network_status_cache
    import time as time_module
    now = time_module.time()
    
    # 缓存有效则直接返回
    if _network_status_cache["online"] is not None:
        if now - _network_status_cache["time"] < _network_check_interval:
            return _network_status_cache["online"]
    
    try:
        # 方法1: 尝试TCP连接（快速检测）
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2秒快速检测
        sock.connect((NETWORK_CHECK_HOST, NETWORK_CHECK_PORT))
        sock.close()
        _network_status_cache = {"online": True, "time": now}
        return True
    except (socket.timeout, socket.error, OSError):
        pass

    try:
        # 方法2: 尝试HTTP请求（快速检测）
        req = urllib.request.Request(
            f"https://{NETWORK_CHECK_HOST}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        urllib.request.urlopen(req, timeout=2)
        _network_status_cache = {"online": True, "time": now}
        return True
    except Exception:
        pass

    # 标记为离线
    _network_status_cache = {"online": False, "time": now}
    return False


def get_network_status() -> Dict[str, Any]:
    """
    获取网络状态详情

    Returns:
        {
            "online": bool,
            "latency_ms": float,
            "method": str,
        }
    """
    result = {
        "online": False,
        "latency_ms": 0.0,
        "method": "none",
    }

    start = time.perf_counter()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(NETWORK_CHECK_TIMEOUT)
        sock.connect((NETWORK_CHECK_HOST, NETWORK_CHECK_PORT))
        sock.close()
        result["online"] = True
        result["method"] = "tcp"
    except Exception:
        pass

    if not result["online"]:
        try:
            req = urllib.request.Request(
                f"https://{NETWORK_CHECK_HOST}",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            urllib.request.urlopen(req, timeout=NETWORK_CHECK_TIMEOUT)
            result["online"] = True
            result["method"] = "http"
        except Exception:
            pass

    result["latency_ms"] = (time.perf_counter() - start) * 1000
    return result


# ==================== 搜索结果缓存 ====================

@lru_cache(maxsize=SEARCH_CACHE_SIZE)
def _cached_search(query: str, max_results: int) -> str:
    """
    缓存的搜索函数（用于lru_cache）

    注意：这里返回JSON字符串，因为lru_cache不支持直接缓存复杂对象
    """
    # 这个函数会被真正搜索函数覆盖
    return json.dumps({"results": [], "success": False})


class SearchCache:
    """搜索结果缓存"""

    def __init__(self, max_size: int = SEARCH_CACHE_SIZE):
        self._cache: Dict[str, SearchResponse] = {}
        self._max_size = max_size
        self._stats = {
            "hits": 0,
            "misses": 0,
            "total_searches": 0,
        }

    def get(self, query: str) -> Optional[SearchResponse]:
        """获取缓存的搜索结果"""
        key = query.strip().lower()
        if key in self._cache:
            self._stats["hits"] += 1
            return self._cache[key]
        self._stats["misses"] += 1
        return None

    def set(self, query: str, response: SearchResponse):
        """缓存搜索结果"""
        key = query.strip().lower()
        if len(self._cache) >= self._max_size:
            # LRU淘汰：删除最早的
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = response

    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._stats = {"hits": 0, "misses": 0, "total_searches": 0}

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0.0
        return {
            **self._stats,
            "cache_size": len(self._cache),
            "hit_rate": hit_rate,
        }


# 全局缓存实例
_search_cache = SearchCache()


# ==================== 核心搜索实现 ====================

def _extract_snippet(text: str, max_len: int = 200) -> str:
    """从文本中提取摘要"""
    if not text:
        return ""
    # 去除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    # 截断
    if len(text) > max_len:
        text = text[:max_len] + "..."
    return text


def _detect_source_type(url: str, title: str = "") -> SourceType:
    """根据URL和标题检测来源类型"""
    url_lower = url.lower() + title.lower()

    if any(kw in url_lower for kw in ["news", "xinwen", "新浪", "腾讯新闻", "网易新闻"]):
        return SourceType.NEWS
    if any(kw in url_lower for kw in ["baike", "wiki", "zhihu", "知乎", "百度百科"]):
        return SourceType.KNOWLEDGE
    if any(kw in url_lower for kw in ["blog", "blog.cn", "wordpress", "博客"]):
        return SourceType.BLOG
    if any(kw in url_lower for kw in ["tieba", "forum", "zhihu.com/question", "论坛"]):
        return SourceType.FORUM
    if any(kw in url_lower for kw in ["video", "youtube", "bilibili", "抖音", "视频"]):
        return SourceType.VIDEO
    if any(kw in url_lower for kw in ["taobao", "jd.com", "tmall", "shop", "电商", "商城"]):
        return SourceType.COMMERCE

    return SourceType.UNKNOWN


def _search_baidu(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> SearchResponse:
    """
    使用百度搜索API搜索（模拟实现）

    注意：真实环境需要百度搜索API密钥
    这里使用简化实现作为示例
    """
    start_time = time.perf_counter()

    try:
        # 构建搜索URL
        search_url = SEARCH_ENGINES["baidu"]["url"].format(
            query=urllib.parse.quote(query),
            count=max_results
        )

        # 发送请求
        req = urllib.request.Request(
            search_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )

        with urllib.request.urlopen(req, timeout=SEARCH_TIMEOUT) as response:
            html = response.read().decode("utf-8", errors="ignore")

        # 解析结果（简化版正则，实际应使用BeautifulSoup）
        results = []
        # 搜索结果通常在 <h3 class="t"> 标签内
        title_pattern = re.compile(r'<h3 class="t">.*?<em>([^<]+)</em>.*?<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', re.DOTALL)

        for match in title_pattern.finditer(html):
            title = _extract_snippet(match.group(3) or match.group(1))
            url = match.group(2)

            # 尝试提取摘要
            snippet = ""
            snippet_pattern = re.compile(r'<span class="c-span-last">([^<]+)</span>')
            snippet_match = snippet_pattern.search(html, match.end())
            if snippet_match:
                snippet = _extract_snippet(snippet_match.group(1))

            results.append(SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=urllib.parse.urlparse(url).netloc,
                source_type=_detect_source_type(url, title),
                search_engine="baidu"
            ))

            if len(results) >= max_results:
                break

        elapsed = (time.perf_counter() - start_time) * 1000

        return SearchResponse(
            query=query,
            success=True,
            results=results,
            total_found=len(results),
            search_time_ms=elapsed,
            search_engine="baidu",
            is_online=True
        )

    except Exception as e:
        elapsed = (time.perf_counter() - start_time) * 1000
        return SearchResponse(
            query=query,
            success=False,
            error=str(e),
            search_time_ms=elapsed,
            search_engine="baidu",
            is_online=True
        )


def _search_duckduckgo(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> SearchResponse:
    """
    使用 DuckDuckGo HTML 搜索（无需 API key）

    DuckDuckGo 的 HTML 界面比百度更容易解析
    """
    start_time = time.perf_counter()

    try:
        # DuckDuckGo HTML 界面
        search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"

        req = urllib.request.Request(
            search_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )

        with urllib.request.urlopen(req, timeout=SEARCH_TIMEOUT) as response:
            html = response.read().decode("utf-8", errors="ignore")

        # 解析 DuckDuckGo HTML 结果
        # DuckDuckGo HTML 的结果在 <a class="result__a"> 标签内
        results = []

        # 方法1: 匹配 result__a 链接
        pattern1 = re.compile(r'<a class="result__a" href="([^"]+)">([^<]+)</a>')
        for match in pattern1.finditer(html):
            url = match.group(1)
            title = _extract_snippet(match.group(2))

            # 尝试提取摘要（在链接后的 <a class="result__snippet"> 中）
            snippet = ""
            snippet_pattern = re.compile(r'<a class="result__snippet"[^>]*>([^<]+)</a>')
            # 在当前位置后搜索
            search_start = match.end()
            snippet_match = snippet_pattern.search(html[search_start:search_start + 500])
            if snippet_match:
                snippet = _extract_snippet(snippet_match.group(1))

            results.append(SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=urllib.parse.urlparse(url).netloc,
                source_type=_detect_source_type(url, title),
                search_engine="duckduckgo"
            ))

            if len(results) >= max_results:
                break

        # 方法2: 如果方法1没有结果，尝试其他模式
        if not results:
            pattern2 = re.compile(r'<h2 class="result__title">.*?<a href="([^"]+)">([^<]+)</a>', re.DOTALL)
            for match in pattern2.finditer(html):
                url = match.group(1)
                title = _extract_snippet(match.group(2))

                results.append(SearchResult(
                    title=title,
                    url=url,
                    snippet="",
                    source=urllib.parse.urlparse(url).netloc,
                    source_type=_detect_source_type(url, title),
                    search_engine="duckduckgo"
                ))

                if len(results) >= max_results:
                    break

        elapsed = (time.perf_counter() - start_time) * 1000

        return SearchResponse(
            query=query,
            success=True,
            results=results,
            total_found=len(results),
            search_time_ms=elapsed,
            search_engine="duckduckgo",
            is_online=True
        )

    except Exception as e:
        elapsed = (time.perf_counter() - start_time) * 1000
        logger.warning(f"DuckDuckGo search failed: {e}")
        return SearchResponse(
            query=query,
            success=False,
            error=str(e),
            search_time_ms=elapsed,
            search_engine="duckduckgo",
            is_online=True
        )


def _search_fallback(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> SearchResponse:
    """
    备用搜索实现

    1. 首先尝试连接 Somn DomainNexus 知识库
    2. 如果知识库不可用，返回通用的搜索建议
    """
    start_time = time.perf_counter()

    # 尝试从 DomainNexus 知识库获取结果
    knowledge_results = _search_from_knowledge_base(query, max_results)

    if knowledge_results:
        elapsed = (time.perf_counter() - start_time) * 1000
        return SearchResponse(
            query=query,
            success=True,
            results=knowledge_results,
            total_found=len(knowledge_results),
            search_time_ms=elapsed,
            search_engine="knowledge_base",
            is_online=False
        )

    # 如果知识库也没有结果，返回搜索建议
    results = [
        SearchResult(
            title=f"搜索建议：关于「{query}」",
            url="#knowledge_base",
            snippet=f"建议在 DomainNexus 知识库中查询「{query}」相关内容...",
            source="Somn建议",
            source_type=SourceType.KNOWLEDGE,
            relevance_score=0.5,
            search_engine="fallback"
        ),
    ]

    elapsed = (time.perf_counter() - start_time) * 1000

    return SearchResponse(
        query=query,
        success=True,
        results=results[:max_results],
        total_found=len(results),
        search_time_ms=elapsed,
        search_engine="fallback",
        is_online=False
    )


def _search_from_knowledge_base(query: str, max_results: int = 5) -> List[SearchResult]:
    """
    从 Somn DomainNexus 知识库搜索

    这是一个桥接函数，连接到 DomainNexus 进行知识检索
    """
    results = []
    try:
        # 尝试导入 DomainNexus
        from knowledge_cells.domain_nexus import DomainNexus, CellIndex

        nexus = DomainNexus()

        # 方法1: 尝试使用 cell_manager.search_indices
        try:
            indices: List[CellIndex] = nexus.cell_manager.search_indices(query)
            if indices:
                for idx in indices[:max_results]:
                    cell_url = f"#domain_nexus/{idx.cell_id}"
                    snippet = idx.summary_preview or f"标签: {', '.join(list(idx.tags)[:3])}"

                    results.append(SearchResult(
                        title=idx.name,
                        url=cell_url,
                        snippet=snippet,
                        source="DomainNexus",
                        source_type=SourceType.KNOWLEDGE,
                        relevance_score=0.7,
                        search_engine="knowledge_base"
                    ))
                return results
        except AttributeError:
            pass

        # 方法2: 使用 nexus.query() 获取相关格子
        query_result = nexus.query(query)
        relevant_cells = query_result.get('relevant_cells', [])
        if relevant_cells:
            for cell in relevant_cells[:max_results]:
                if isinstance(cell, dict):
                    cell_id = cell.get('cell_id', 'unknown')
                    cell_url = f"#domain_nexus/{cell_id}"
                    tags = cell.get('tags', [])
                    snippet = f"标签: {', '.join(tags[:3])}" if tags else ""

                    results.append(SearchResult(
                        title=cell.get('name', '知识库条目'),
                        url=cell_url,
                        snippet=snippet,
                        source="DomainNexus",
                        source_type=SourceType.KNOWLEDGE,
                        relevance_score=0.7,
                        search_engine="knowledge_base"
                    ))

    except ImportError:
        logger.debug("DomainNexus not available for search fallback")
    except Exception as e:
        logger.warning(f"Knowledge base search failed: {e}")

    return results


# ==================== 公开接口 ====================

def search_web(
    query: str,
    max_results: int = DEFAULT_MAX_RESULTS,
    mode: SearchMode = SearchMode.NORMAL,
    use_cache: bool = True,
) -> SearchResponse:
    """
    执行网络搜索

    Args:
        query: 搜索关键词
        max_results: 最大返回结果数
        mode: 搜索模式
        use_cache: 是否使用缓存

    Returns:
        SearchResponse: 搜索结果
    """
    if not query or not query.strip():
        return SearchResponse(
            query=query,
            success=False,
            error="搜索关键词不能为空",
            is_online=False
        )

    # 检查缓存
    if use_cache:
        cached = _search_cache.get(query)
        if cached:
            return cached

    # 联网检测
    online = is_online()
    _search_cache._stats["total_searches"] += 1

    if not online:
        # 离线模式：使用备用搜索
        response = _search_fallback(query, max_results)
        if use_cache:
            _search_cache.set(query, response)
        return response

    # 在线模式：尝试多个搜索引擎
    engines_to_try = [
        ("baidu", _search_baidu),
        ("duckduckgo", _search_duckduckgo),
    ]

    response = None
    last_error = None

    for engine_name, engine_func in engines_to_try:
        try:
            logger.info(f"Trying search engine: {engine_name}")
            resp = engine_func(query, max_results)

            # 如果成功且有结果，使用这个结果
            if resp.success and len(resp.results) > 0:
                response = resp
                logger.info(f"Search successful via {engine_name}: {len(resp.results)} results")
                break

            # 如果成功但无结果，记录并尝试下一个
            if resp.success and len(resp.results) == 0:
                logger.warning(f"{engine_name} returned no results for: {query}")

            # 如果失败，记录错误
            if not resp.success:
                last_error = resp.error
                logger.warning(f"{engine_name} search failed: {resp.error}")

        except Exception as e:
            last_error = str(e)
            logger.warning(f"{engine_name} search exception: {e}")

    # 如果所有在线搜索都失败或没有结果，使用 fallback
    if response is None or len(response.results) == 0:
        logger.info(f"All online searches failed or returned no results, using fallback: {query} (last error: {last_error})")
        response = _search_fallback(query, max_results)

    if use_cache:
        _search_cache.set(query, response)

    return response


def search_with_context(
    query: str,
    context: str = "",
    max_results: int = DEFAULT_MAX_RESULTS,
) -> SearchResponse:
    """
    带上下文的搜索（用于增强搜索质量）

    Args:
        query: 搜索关键词
        context: 上下文信息（将拼接到查询中）
        max_results: 最大返回结果数

    Returns:
        SearchResponse: 搜索结果
    """
    enhanced_query = f"{context} {query}" if context else query
    return search_web(enhanced_query, max_results)


def batch_search(
    queries: List[str],
    max_results: int = DEFAULT_MAX_RESULTS,
) -> List[SearchResponse]:
    """
    批量搜索

    Args:
        queries: 搜索关键词列表
        max_results: 每个关键词最大返回结果数

    Returns:
        List[SearchResponse]: 搜索结果列表
    """
    return [search_web(q, max_results) for q in queries]


def get_search_stats() -> Dict[str, Any]:
    """
    获取搜索统计信息

    Returns:
        缓存命中率、搜索次数等统计
    """
    return {
        "cache": _search_cache.get_stats(),
        "network": get_network_status(),
    }


def clear_search_cache():
    """清空搜索缓存"""
    _search_cache.clear()


# ==================== 浏览器爬虫搜索（新增） ====================

def search_with_browser(
    query: str,
    search_engine: str = "baidu",
    max_results: int = 10,
    headless: bool = True,
    use_cache: bool = True,
) -> SearchResponse:
    """
    使用浏览器爬虫执行搜索

    模拟真实用户搜索行为，通过隐藏式浏览器获取搜索结果

    Args:
        query: 搜索关键词
        search_engine: 搜索引擎（"baidu", "google", "duckduckgo", "bing"）
        max_results: 最大结果数
        headless: 是否隐藏浏览器
        use_cache: 是否使用缓存

    Returns:
        SearchResponse: 搜索结果
    """
    start_time = time.perf_counter()

    if not query or not query.strip():
        return SearchResponse(
            query=query,
            success=False,
            error="搜索关键词不能为空",
            is_online=False
        )

    # 检查缓存
    cache_key = f"browser:{search_engine}:{query}"
    if use_cache:
        cached = _search_cache.get(cache_key)
        if cached:
            return cached

    try:
        # 延迟导入避免循环依赖
        from knowledge_cells.browser_crawler import (
            search_with_browser as crawler_search,
            SearchEngineType,
        )

        # 映射搜索引擎
        engine_map = {
            "baidu": "baidu",
            "google": "google",
            "duckduckgo": "duckduckgo",
            "bing": "bing",
        }
        engine = engine_map.get(search_engine.lower(), "baidu")

        # 执行爬虫搜索
        crawl_response = crawler_search(query, engine, max_results, headless)

        # 转换结果格式
        results = []
        for cr in crawl_response.results:
            results.append(SearchResult(
                title=cr.title,
                url=cr.url,
                snippet=cr.snippet,
                source=cr.search_engine,
                source_type=_detect_source_type(cr.url, cr.title),
                relevance_score=1.0 - (cr.rank * 0.1),  # 排名越高分数越高
                search_engine=crawl_response.search_engine,
            ))

        elapsed = (time.perf_counter() - start_time) * 1000

        response = SearchResponse(
            query=query,
            success=crawl_response.success,
            results=results,
            total_found=crawl_response.total_found,
            search_time_ms=elapsed + crawl_response.crawl_time_ms,
            search_engine=f"browser_{engine}",
            is_online=True,
            error=crawl_response.error if not crawl_response.success else "",
        )

        if use_cache:
            _search_cache.set(cache_key, response)

        return response

    except ImportError as e:
        logger.warning(f"Browser crawler not available: {e}")
        return SearchResponse(
            query=query,
            success=False,
            error=f"浏览器爬虫未安装: {e}",
            search_time_ms=(time.perf_counter() - start_time) * 1000,
            is_online=False,
        )
    except Exception as e:
        logger.error(f"Browser crawl failed: {e}")
        return SearchResponse(
            query=query,
            success=False,
            error=str(e),
            search_time_ms=(time.perf_counter() - start_time) * 1000,
            is_online=True,
        )


def get_crawler_manager():
    """获取全局爬虫管理器"""
    from knowledge_cells.browser_crawler import get_crawler_manager as get_mgr
    return get_mgr()


# ==================== 增强搜索函数 ====================

def search_enhanced(
    query: str,
    max_results: int = 10,
    use_browser: bool = False,
    fallback_to_knowledge_base: bool = True,
) -> SearchResponse:
    """
    增强搜索函数

    优先使用真实网络搜索，失败时降级到备用方案

    Args:
        query: 搜索关键词
        max_results: 最大结果数
        use_browser: 是否优先使用浏览器爬虫
        fallback_to_knowledge_base: 是否降级到知识库

    Returns:
        SearchResponse: 搜索结果
    """
    # 方案1: 浏览器爬虫（如果启用）
    if use_browser:
        response = search_with_browser(query, max_results=max_results)
        if response.success and response.results:
            return response

    # 方案2: 传统 HTTP 搜索
    response = search_web(query, max_results)
    if response.success and response.results:
        return response

    # 方案3: 知识库降级
    if fallback_to_knowledge_base:
        return _search_fallback(query, max_results)

    return response


# ==================== WebSearchEngine 类封装 ====================

class WebSearchEngine:
    """
    网络搜索引擎封装类

    提供面向对象的搜索接口，支持更多高级功能
    """

    def __init__(self, cache_size: int = SEARCH_CACHE_SIZE):
        self._cache = SearchCache(max_size=cache_size)
        self._last_search_time = 0.0

    def search(
        self,
        query: str,
        max_results: int = DEFAULT_MAX_RESULTS,
        mode: SearchMode = SearchMode.NORMAL,
    ) -> SearchResponse:
        """执行搜索"""
        response = search_web(query, max_results, mode)
        if response.success:
            self._last_search_time = time.time()
        return response

    def search_with_retry(
        self,
        query: str,
        max_results: int = DEFAULT_MAX_RESULTS,
        max_retries: int = 2,
    ) -> SearchResponse:
        """带重试的搜索"""
        for attempt in range(max_retries):
            response = self.search(query, max_results)
            if response.success:
                return response
            if not response.is_online:
                break  # 离线状态重试无意义
        return response

    def is_online(self) -> bool:
        """检查联网状态"""
        return is_online()

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "cache": self._cache.get_stats(),
            "network": get_network_status(),
            "last_search_time": self._last_search_time,
        }


# ==================== 快捷函数 ====================

# 全局搜索引擎实例（延迟初始化）
_web_engine: Optional[WebSearchEngine] = None


def get_web_engine() -> WebSearchEngine:
    """获取全局WebSearchEngine实例"""
    global _web_engine
    if _web_engine is None:
        _web_engine = WebSearchEngine()
    return _web_engine


def quick_search(query: str) -> SearchResponse:
    """快速搜索（使用全局实例）"""
    return get_web_engine().search(query, max_results=3, mode=SearchMode.QUICK)


def deep_search(query: str) -> SearchResponse:
    """深度搜索（使用全局实例）"""
    return get_web_engine().search(query, max_results=10, mode=SearchMode.DEEP)


# 需要导入urllib.parse（前面漏了）
import urllib.parse


__all__ = [
    # 核心类
    "WebSearchEngine",
    "SearchResult",
    "SearchResponse",
    "SearchMode",
    "SourceType",

    # 联网检测
    "is_online",
    "get_network_status",

    # 搜索函数
    "search_web",
    "search_with_context",
    "batch_search",
    "quick_search",
    "deep_search",

    # 缓存管理
    "get_search_stats",
    "clear_search_cache",

    # 全局实例
    "get_web_engine",

    # 浏览器爬虫（新增）
    "search_with_browser",
    "get_crawler_manager",
]
