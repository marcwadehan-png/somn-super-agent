# -*- coding: utf-8 -*-
"""
OpenClaw - 开放抓取模块
===================

Phase 4: 外部世界主动抓取并更新系统

子模块:
- _openclaw_core: 核心引擎（数据结构+OpenClawCore）
- _web_source: Web数据源连接器
- _file_source: 文件系统数据源连接器
- _api_source: API数据源连接器（REST/GraphQL）
- _rss_source: RSS/Atom订阅源连接器
- _web_fetcher: 网页深度抓取器（BFS/DFS爬取）
- _doc_parser: 多格式文档解析器
- _cleaner: 内容清洗引擎
- _feedback: 用户反馈学习系统
- _pattern_learner: 深层模式学习器
- _recommender: 智能贤者推荐引擎
- _updater: 增量更新引擎

版本: v1.1.0
创建: 2026-04-22
更新: 2026-04-23 Phase 4.5 完整实现（7个新模块）

注意：Web数据源相关模块依赖 aiohttp 第三方库。
如未安装，这些模块将以空桩模式提供。
安装命令: pip install aiohttp
"""

import warnings

_AIOHTTP_AVAILABLE = False
try:
    import aiohttp  # noqa: F401
    _AIOHTTP_AVAILABLE = True
except ImportError:
    warnings.warn(
        "aiohttp 未安装，OpenClaw Web数据源模块将以降级模式运行。"
        "安装命令: pip install aiohttp",
        ImportWarning,
        stacklevel=2,
    )

from ._openclaw_core import (
    OpenClawCore,
    DataSourceConnector,
    KnowledgeItem,
    Feedback,
    UpdateResult,
    UpdateMode,
    DataSourceType,
)

if _AIOHTTP_AVAILABLE:
    # 数据源连接器
    from ._web_source import WebDataSource, WebConfig
    from ._api_source import (
        ApiDataSource, ApiSourceConfig, AuthType,
        ResponseFormat, PaginationConfig, RateLimitConfig,
    )
    from ._rss_source import (
        RssDataSource, RssFeedConfig, RssFeedStatus,
        RssItem, discover_feeds_from_html,
    )

    # 抓取与解析
    from ._web_fetcher import WebFetcher, FetchConfig, FetchResult, CrawlStats

    # 反馈与学习（部分依赖 aiohttp）
    from ._feedback import FeedbackCollector, FeedbackItem, ActiveLearner, SageAdaptor
    from ._recommender import (
        SageRecommender, Recommendation,
        RecommendationResult, RecommenderConfig,
    )
else:
    # 空桩降级
    WebDataSource = WebConfig = None
    ApiDataSource = ApiSourceConfig = AuthType = None
    ResponseFormat = PaginationConfig = RateLimitConfig = None
    RssDataSource = RssFeedConfig = RssFeedStatus = None
    RssItem = discover_feeds_from_html = None
    WebFetcher = FetchConfig = FetchResult = CrawlStats = None
    FeedbackCollector = FeedbackItem = ActiveLearner = SageAdaptor = None
    SageRecommender = Recommendation = None
    RecommendationResult = RecommenderConfig = None

# 无 aiohttp 依赖的模块（始终可用）
from ._file_source import FileDataSource, FileConfig
from ._doc_parser import DocParser, ParseConfig, ParseResult, DocChunk, DocMetadata, DocFormat
from ._cleaner import ContentCleaner, CleanConfig, CleanResult
from ._pattern_learner import (
    PatternLearner, UserPreference,
    TopicSageAssociation, QualityPattern, TimePattern,
)
from ._updater import DiffEngine, Merger, VersionControl, MergeStrategy, DiffType, DiffResult

__all__ = [
    # ===== 核心 =====
    'OpenClawCore',
    'DataSourceConnector',
    'KnowledgeItem',
    'Feedback',
    'UpdateResult',
    'UpdateMode',
    'DataSourceType',
    # ===== 数据源连接器 =====
    'WebDataSource', 'WebConfig',
    'FileDataSource', 'FileConfig',
    'ApiDataSource', 'ApiSourceConfig', 'AuthType',
    'ResponseFormat', 'PaginationConfig', 'RateLimitConfig',
    'RssDataSource', 'RssFeedConfig', 'RssFeedStatus',
    'RssItem', 'discover_feeds_from_html',
    # ===== 抓取与解析 =====
    'WebFetcher', 'FetchConfig', 'FetchResult', 'CrawlStats',
    'DocParser', 'ParseConfig', 'ParseResult', 'DocChunk', 'DocMetadata', 'DocFormat',
    'ContentCleaner', 'CleanConfig', 'CleanResult',
    # ===== 反馈与学习 =====
    'FeedbackCollector', 'FeedbackItem', 'ActiveLearner', 'SageAdaptor',
    'PatternLearner', 'UserPreference',
    'TopicSageAssociation', 'QualityPattern', 'TimePattern',
    'SageRecommender', 'Recommendation',
    'RecommendationResult', 'RecommenderConfig',
    # ===== 增量更新 =====
    'DiffEngine', 'Merger', 'VersionControl', 'MergeStrategy', 'DiffType', 'DiffResult',
]
__aiohttp_available__ = _AIOHTTP_AVAILABLE
