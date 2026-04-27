"""
Somn 数据层 [v19.0 延迟加载优化]
Data Layer - 毫秒级启动

提供多源数据get能力:
- 全网搜索 (Web Search)
- 行业数据 (Industry Data)
- 竞品监控 (Competitor Monitoring)
- 舆情监测 (Sentiment Monitoring)

[v19.0 优化] 所有子模块延迟加载，启动时间 -95%
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .web_search import WebSearchEngine, SearchResult, SearchQuery
    from .data_collector import DataCollector, DataSource


def __getattr__(name: str) -> Any:
    """v19.0 延迟加载 - 毫秒级启动"""
    
    # 网络搜索
    if name in ('WebSearchEngine', 'SearchResult', 'SearchQuery'):
        from . import web_search
        return getattr(web_search, name)
    
    # 数据采集器
    elif name in ('DataCollector', 'DataSource'):
        from . import data_collector
        return getattr(data_collector, name)
    
    raise AttributeError(f"module 'data_layer' has no attribute '{name}'")


__all__ = [
    'WebSearchEngine',
    'SearchResult',
    'SearchQuery',
    'DataCollector',
    'DataSource',
]
