"""
行业知识图谱系统 v2.0
Industry Knowledge Graph System v2.0

拆分后版本:
- _ikg_types.py: 类型定义
- _ikg_inference.py: 关系推理引擎
- _ikg_autocomplete.py: 知识自动补全器
- _ikg_comparator.py: 行业对比分析器
- _ikg_core.py: 核心类和便捷函数

版本: v2.0
日期: 2026-04-08
"""

# 类型定义
from ._ikg_types import (
    EntityType,
    RelationType,
    Entity,
    Relation,
    CaseStudy,
)

# 核心类
from ._ikg_core import (
    IndustryKnowledgeGraph,
    create_default_knowledge_graph,
)

# 保持向后兼容: 直接从主类暴露
__all__ = [
    # 类型
    "EntityType",
    "RelationType",
    "Entity",
    "Relation",
    "CaseStudy",
    # 类
    "IndustryKnowledgeGraph",
    # 函数
    "create_default_knowledge_graph",
]
