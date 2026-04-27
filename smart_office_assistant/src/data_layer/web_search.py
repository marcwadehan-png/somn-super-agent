"""
__all__ = [
    'get_search_insights',
    'quick_search',
    'search',
    'to_dict',
]

全网搜索引擎 - 多源搜索与内容提取
支持: 通用搜索,新闻搜索,学术搜索,社交媒体
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from src.core.paths import SEARCH_CACHE_DIR
import hashlib

logger = logging.getLogger(__name__)

class SearchSource(Enum):
    """搜索来源"""
    GENERAL = "general"           # 通用搜索
    NEWS = "news"                 # 新闻
    ACADEMIC = "academic"         # 学术
    SOCIAL = "social"             # 社交媒体
    INDUSTRY = "industry"         # 行业报告
    PATENT = "patent"             # 专利

class SearchIntent(Enum):
    """搜索意图"""
    MARKET_RESEARCH = "market_research"       # 市场研究
    COMPETITOR_ANALYSIS = "competitor_analysis"  # 竞品分析
    TREND_ANALYSIS = "trend_analysis"         # 趋势分析
    USER_RESEARCH = "user_research"           # 用户研究
    TECHNOLOGY = "technology"                 # 技术调研
    REGULATION = "regulation"                 # 政策法规

@dataclass
class SearchQuery:
    """搜索查询"""
    keywords: List[str]           # 关键词列表
    intent: SearchIntent = SearchIntent.MARKET_RESEARCH
    sources: List[SearchSource] = field(default_factory=lambda: [SearchSource.GENERAL])
    time_range: Optional[str] = None  # 时间范围: 1d, 7d, 30d, 1y, all
    region: Optional[str] = None  # 地区限制
    language: str = "zh"
    max_results: int = 10
    filters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'keywords': self.keywords,
            'intent': self.intent.value,
            'sources': [s.value for s in self.sources],
            'time_range': self.time_range,
            'region': self.region,
            'language': self.language,
            'max_results': self.max_results,
            'filters': self.filters
        }

@dataclass
class SearchResult:
    """搜索结果"""
    result_id: str
    title: str
    url: str
    snippet: str
    source: SearchSource
    published_date: Optional[str] = None
    author: Optional[str] = None
    domain: Optional[str] = None
    relevance_score: float = 0.0
    content_type: str = "webpage"  # webpage, pdf, video, image
    metadata: Dict[str, Any] = field(default_factory=dict)
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'result_id': self.result_id,
            'title': self.title,
            'url': self.url,
            'snippet': self.snippet,
            'source': self.source.value,
            'published_date': self.published_date,
            'author': self.author,
            'domain': self.domain,
            'relevance_score': self.relevance_score,
            'content_type': self.content_type,
            'metadata': self.metadata,
            'fetched_at': self.fetched_at
        }

@dataclass
class SearchSession:
    """搜索会话"""
    session_id: str
    query: SearchQuery
    results: List[SearchResult] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'query': self.query.to_dict(),
            'results': [r.to_dict() for r in self.results],
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

class WebSearchEngine:
    """全网搜索引擎"""
    
    def __init__(self, base_path: str = None, api_keys: Dict = None):
        self.base_path = Path(base_path) if base_path else SEARCH_CACHE_DIR
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.api_keys = api_keys or {}
        self.sessions: Dict[str, SearchSession] = {}
        
        # 搜索源配置
        self.source_configs = {
            SearchSource.GENERAL: {
                'enabled': True,
                'apis': ['serper', 'bing', 'google'],
                'fallback': 'mock'
            },
            SearchSource.NEWS: {
                'enabled': True,
                'apis': ['newsapi', 'gnews'],
                'fallback': 'mock'
            },
            SearchSource.ACADEMIC: {
                'enabled': True,
                'apis': ['semantic_scholar', 'arxiv'],
                'fallback': 'mock'
            },
            SearchSource.SOCIAL: {
                'enabled': True,
                'apis': ['twitter', 'reddit'],
                'fallback': 'mock'
            }
        }
        
        # 延迟加载会话（首次搜索时触发）
        self._sessions_loaded = False

    
    def search(self, query: SearchQuery, use_cache: bool = True) -> SearchSession:
        """执行搜索"""
        # generate会话ID
        session_id = self._generate_session_id(query)
        
        # 检查缓存
        if use_cache and session_id in self.sessions:
            cached = self.sessions[session_id]
            # 检查缓存是否过期(24小时)
            cached_time = datetime.fromisoformat(cached.created_at)
            if datetime.now() - cached_time < timedelta(hours=24):
                logger.debug(f"使用缓存结果: {session_id}")
                return cached
        
        # 创建新会话
        session = SearchSession(session_id=session_id, query=query)
        
        # 执行多源搜索
        all_results = []
        for source in query.sources:
            results = self._search_single_source(query, source)
            all_results.extend(results)
        
        # 去重和排序
        session.results = self._deduplicate_and_rank(all_results, query)
        session.completed_at = datetime.now().isoformat()
        
        # 保存会话
        self.sessions[session_id] = session
        self._save_session(session)
        
        return session
    
    def _search_single_source(self, query: SearchQuery, source: SearchSource) -> List[SearchResult]:
        """
        搜索单一来源 [v10.1 重试优化]

        支持指数退避重试（最多3次），针对网络超时/429限流/5xx错误自动重试。
        熔断器隔离各来源，避免单源故障影响全局。
        """
        config = self.source_configs.get(source, {})

        # 这里实现实际的API调用
        # 目前使用模拟数据演示架构
        if config.get('fallback') == 'mock':
            return self._mock_search(query, source)

        # [v10.1] 重试包装：对于真实API来源
        return self._search_with_retry(query, source)

    def _search_with_retry(
        self, query: SearchQuery, source: SearchSource, max_retries: int = 3
    ) -> List[SearchResult]:
        """
        [v10.1] 带重试的搜索封装。

        Args:
            query: 搜索查询
            source: 搜索来源
            max_retries: 最大重试次数

        Returns:
            搜索结果列表，重试耗尽后返回空列表
        """
        import time as _time
        from src.utils.retry_utils import get_circuit_breaker

        cb = get_circuit_breaker(f"search-{source.value}", failure_threshold=5, recovery_timeout=30.0)
        last_error: Optional[Exception] = None

        for _attempt in range(1, max_retries + 1):
            if not cb.is_available():
                logger.warning(f"[搜索-{source.value}] 熔断器 OPEN，跳过搜索")
                return []

            try:
                results = self._do_search(query, source)
                cb.record_success()
                return results
            except Exception as e:
                last_error = e
                cb.record_failure()

                # 判断是否值得重试
                retryable = False
                status_code = getattr(e, "code", None) if hasattr(e, "code") else None
                if status_code in (429, 500, 502, 503, 504):
                    retryable = True
                elif isinstance(e, (ConnectionError, TimeoutError, OSError)):
                    retryable = True

                if retryable and _attempt < max_retries:
                    delay = min(1.5 * (2 ** (_attempt - 1)), 10.0)
                    import random
                    delay = delay * (0.5 + random.random())
                    logger.warning(
                        f"[搜索-{source.value}] 第{_attempt}次失败: {type(e).__name__}，"
                        f"{delay:.1f}s后重试..."
                    )
                    _time.sleep(delay)
                else:
                    logger.warning(
                        f"[搜索-{source.value}] 搜索失败（已达最大重试）: {e}"
                    )
                    break

        return []

    def _do_search(self, query: SearchQuery, source: SearchSource) -> List[SearchResult]:
        """
        执行实际搜索（由子类或外部API实现）。
        此处为基类实现，返回空列表。
        """
        return []
    
    def _mock_search(self, query: SearchQuery, source: SearchSource) -> List[SearchResult]:
        """模拟搜索(演示用)"""
        mock_data = {
            SearchSource.GENERAL: [
                {
                    'title': f"{' '.join(query.keywords)} 市场研究报告 2024",
                    'url': "https://example.com/market-report",
                    'snippet': "本报告深入分析了当前市场格局,竞争态势和发展趋势...",
                    'domain': 'example.com'
                },
                {
                    'title': f"{' '.join(query.keywords)} 行业最佳实践",
                    'url': "https://example.com/best-practices",
                    'snippet': "总结了行业内领先企业的成功经验和可复用的方法论...",
                    'domain': 'example.com'
                }
            ],
            SearchSource.NEWS: [
                {
                    'title': f"{' '.join(query.keywords)} 行业最新动态",
                    'url': "https://news.example.com/latest",
                    'snippet': "近日,该领域迎来重大政策调整,预计将对市场产生深远影响...",
                    'published_date': datetime.now().isoformat(),
                    'domain': 'news.example.com'
                }
            ],
            SearchSource.ACADEMIC: [
                {
                    'title': f"Research on {' '.join(query.keywords)}: A Comprehensive Study",
                    'url': "https://arxiv.org/abs/1234.5678",
                    'snippet': "This paper presents a comprehensive analysis of growth strategies...",
                    'author': "J. Smith et al.",
                    'domain': 'arxiv.org'
                }
            ]
        }
        
        results = []
        for i, data in enumerate(mock_data.get(source, [])):
            result = SearchResult(
                result_id=f"{source.value}_{i}_{hashlib.md5(data['url'].encode()).hexdigest()[:8]}",
                title=data['title'],
                url=data['url'],
                snippet=data['snippet'],
                source=source,
                published_date=data.get('published_date'),
                author=data.get('author'),
                domain=data.get('domain'),
                relevance_score=0.9 - (i * 0.1)
            )
            results.append(result)
        
        return results[:query.max_results]
    
    def _deduplicate_and_rank(self, results: List[SearchResult], query: SearchQuery) -> List[SearchResult]:
        """去重和排序"""
        # 基于URL去重
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url_key = result.url.split('?')[0]  # 去除参数
            if url_key not in seen_urls:
                seen_urls.add(url_key)
                unique_results.append(result)
        
        # 计算相关性分数
        for result in unique_results:
            score = result.relevance_score
            
            # 关键词匹配加分
            title_lower = result.title.lower()
            snippet_lower = result.snippet.lower()
            for keyword in query.keywords:
                kw_lower = keyword.lower()
                if kw_lower in title_lower:
                    score += 0.1
                if kw_lower in snippet_lower:
                    score += 0.05
            
            # 时效性加分
            if result.published_date:
                try:
                    pub_date = datetime.fromisoformat(result.published_date)
                    days_old = (datetime.now() - pub_date).days
                    if days_old < 7:
                        score += 0.1
                    elif days_old < 30:
                        score += 0.05
                except (ValueError, TypeError) as e:
                    logger.warning(f"日期解析失败: {result.published_date}, {e}")
                except Exception as e:
                    logger.error(f"日期计算错误: {type(e).__name__} - {e}")
            
            result.relevance_score = min(score, 1.0)
        
        # 按分数排序
        unique_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return unique_results[:query.max_results]
    
    def _generate_session_id(self, query: SearchQuery) -> str:
        """generate会话ID"""
        content = json.dumps(query.to_dict(), sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _ensure_sessions(self):
        """懒加载历史会话（首次搜索时调用）"""
        if self._sessions_loaded:
            return
        self._load_sessions()
        self._sessions_loaded = True

    def _save_session(self, session: SearchSession):
        """保存会话"""
        session_file = self.base_path / f"{session.session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)
    
    def _load_sessions(self):
        """加载历史会话"""
        if not self.base_path.exists():
            return
        
        for session_file in self.base_path.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 简化加载,实际应完整解析
                    pass
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logger.warning(f"会话文件解析失败 {session_file}: {e}")
            except OSError as e:
                logger.warning(f"读取会话文件失败 {session_file}: {e}")
            except Exception as e:
                logger.error(f"加载会话文件时发生意外错误 {session_file}: {type(e).__name__} - {e}")
    
    def get_search_insights(self, session_id: str) -> Dict[str, Any]:
        """get搜索洞察"""
        session = self.sessions.get(session_id)
        if not session:
            return {}
        
        # 分析搜索结果
        sources_dist = {}
        domain_dist = {}
        timeline = []
        
        for result in session.results:
            # 来源分布
            source = result.source.value
            sources_dist[source] = sources_dist.get(source, 0) + 1
            
            # 域名分布
            domain = result.domain or 'unknown'
            domain_dist[domain] = domain_dist.get(domain, 0) + 1
            
            # 时间线
            if result.published_date:
                timeline.append(result.published_date)
        
        return {
            'total_results': len(session.results),
            'sources_distribution': sources_dist,
            'domains_distribution': dict(sorted(domain_dist.items(), 
                                               key=lambda x: x[1], 
                                               reverse=True)[:10]),
            'timeline_range': {
                'earliest': min(timeline) if timeline else None,
                'latest': max(timeline) if timeline else None
            },
            'avg_relevance': sum(r.relevance_score for r in session.results) / len(session.results) if session.results else 0
        }
    
    def quick_search(self, keywords: str, intent: str = "market_research") -> List[SearchResult]:
        """快速搜索"""
        query = SearchQuery(
            keywords=keywords.split(),
            intent=SearchIntent(intent),
            max_results=5
        )
        session = self.search(query)
        return session.results
