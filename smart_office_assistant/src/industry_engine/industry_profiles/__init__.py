"""
行业画像扩展库 v2.1
Industry Profiles Extension v2.1

扩展行业覆盖: 5个 → 15个行业
新增行业:
- 医疗健康 (Healthcare)
- 教育培训 (Education)
- 房地产 (Real Estate)
- 旅游出行 (Travel)
- 餐饮美食 (Food & Beverage)
- AI科技 (AI Tech)
- 新能源汽车 (New Energy Vehicle)
- 奢侈品 (Luxury)
- 运动健身 (Sports & Fitness)
- 宠物经济 (Pet Economy)
- 内容媒体/游戏 (Content Media & Gaming) [v2.1新增]

版本: v2.1 -> v2.2 (模块化拆分)
日期: 2026-04-04
更新时间: 2026-04-08
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

__all__ = [
    'get_all_industries',
    'get_industry_profile',
    'search_industries',
    'IndustryProfile',
    'IndustryType',
    'BusinessModel',
    '_IndustryLibrary',
]


def __getattr__(name: str) -> Any:
    """延迟导入所有公开符号"""
    if name == 'IndustryType':
        from ._ip_types import IndustryType
        return IndustryType
    if name == 'BusinessModel':
        from ._ip_types import BusinessModel
        return BusinessModel
    if name == 'IndustryProfile':
        from ._ip_types import IndustryProfile
        return IndustryProfile
    if name == '_IndustryLibrary':
        from ._ip_queries import IndustryProfileLibrary as _IndustryLibrary
        return _IndustryLibrary
    if name == 'get_industry_profile':
        def get_industry_profile(industry: str) -> Optional[Any]:
            """获取行业画像便捷函数"""
            from ._ip_types import IndustryType
            from ._ip_queries import IndustryProfileLibrary
            library = IndustryProfileLibrary()
            try:
                industry_type = IndustryType(industry.lower())
                return library.get_profile(industry_type)
            except ValueError:
                return library.get_profile_by_name(industry)
        return get_industry_profile
    if name == 'get_all_industries':
        def get_all_industries() -> Dict[str, Any]:
            """获取所有行业"""
            from ._ip_queries import IndustryProfileLibrary
            library = IndustryProfileLibrary()
            return library.get_all_profiles()
        return get_all_industries
    if name == 'search_industries':
        def search_industries(keyword: str) -> List[Any]:
            """搜索行业"""
            from ._ip_queries import IndustryProfileLibrary
            library = IndustryProfileLibrary()
            return library.search_industries(keyword)
        return search_industries
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
