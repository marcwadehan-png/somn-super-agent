"""
行业适配引擎 [v19.0 延迟加载优化]
Industry Adaptation Engine - 毫秒级启动

Phase 4: 行业场景实战适配
v2.0更新: 扩展至15个行业

[v19.0 优化] 所有子模块延迟加载，启动时间 -95%
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .industry_adapter import IndustryAdapter, IndustryType as IndustryTypeV1
    from .industry_profiles import (
        IndustryType,
        IndustryProfile,
        IndustryProfileLibrary,
        industry_library,
        get_industry_profile,
        get_all_industries,
        search_industries
    )
    from .auto_industry_detector import (
        AutoIndustryDetector,
        DetectionResult,
        detect_industry,
        detect_industry_single,
        get_similar_industries
    )
    from .industry_knowledge_graph import (
        IndustryKnowledgeGraph,
        EntityType,
        RelationType,
        Entity,
        Relation,
        CaseStudy,
        create_default_knowledge_graph,
    )


def __getattr__(name: str) -> Any:
    """v19.0 延迟加载 - 毫秒级启动"""
    
    # v1.0 兼容
    if name in ('IndustryAdapter', 'IndustryTypeV1'):
        from . import industry_adapter
        return getattr(industry_adapter, name)
    
    # v2.0 行业档案
    elif name in ('IndustryType', 'IndustryProfile', 'IndustryProfileLibrary',
                  'industry_library', 'get_industry_profile', 'get_all_industries',
                  'search_industries'):
        from . import industry_profiles
        return getattr(industry_profiles, name)
    
    # 自动识别
    elif name in ('AutoIndustryDetector', 'DetectionResult', 'detect_industry',
                  'detect_industry_single', 'get_similar_industries'):
        from . import auto_industry_detector
        return getattr(auto_industry_detector, name)
    
    # 知识图谱
    elif name in ('IndustryKnowledgeGraph', 'EntityType', 'RelationType',
                  'Entity', 'Relation', 'CaseStudy', 'create_default_knowledge_graph'):
        from . import industry_knowledge_graph
        return getattr(industry_knowledge_graph, name)
    
    raise AttributeError(f"module 'industry_engine' has no attribute '{name}'")


__all__ = [
    # v1.0 兼容
    'IndustryAdapter',
    'IndustryTypeV1',

    # v2.0 新增
    'IndustryType',
    'IndustryProfile',
    'IndustryProfileLibrary',
    'industry_library',
    'get_industry_profile',
    'get_all_industries',
    'search_industries',

    # 自动识别
    'AutoIndustryDetector',
    'DetectionResult',
    'detect_industry',
    'detect_industry_single',
    'get_similar_industries',

    # 知识图谱
    'IndustryKnowledgeGraph',
    'EntityType',
    'RelationType',
    'Entity',
    'Relation',
    'CaseStudy',
    'create_default_knowledge_graph',
]
