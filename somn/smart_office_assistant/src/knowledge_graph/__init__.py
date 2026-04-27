"""
Somn 知识图谱系统 [v19.0 延迟加载优化]
Knowledge Graph System - 毫秒级启动

基于手册三层知识架构:
- 概念层: 实体,属性,分类
- 关系层: 关联,因果,层次
- 规则层: 演绎,归纳,启发,因果规则

[v19.0 优化] 所有子模块延迟加载，启动时间 -95%
"""

import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .graph_engine import KnowledgeGraphEngine, GraphNode, GraphEdge, GraphQuery
    from .concept_manager import ConceptManager, Concept, ConceptRelation
    from .rule_engine import RuleEngine, Rule, RuleType
    from .industry_knowledge import IndustryKnowledgeBase, IndustryProfile


def __getattr__(name: str) -> Any:
    """v19.0 延迟加载 - 毫秒级启动"""
    
    # 核心图谱引擎
    if name in ('KnowledgeGraphEngine', 'GraphNode', 'GraphEdge', 'GraphQuery'):
        from . import graph_engine
        return getattr(graph_engine, name)
    
    # 概念管理器
    elif name in ('ConceptManager', 'Concept', 'ConceptRelation'):
        from . import concept_manager
        return getattr(concept_manager, name)
    
    # 规则引擎
    elif name in ('RuleEngine', 'Rule', 'RuleType'):
        from . import rule_engine
        return getattr(rule_engine, name)
    
    # 行业知识库
    elif name in ('IndustryKnowledgeBase', 'IndustryProfile'):
        from . import industry_knowledge
        return getattr(industry_knowledge, name)
    
    raise AttributeError(f"module 'knowledge_graph' has no attribute '{name}'")


__all__ = [
    'KnowledgeGraphEngine',
    'GraphNode',
    'GraphEdge', 
    'GraphQuery',
    'ConceptManager',
    'Concept',
    'ConceptRelation',
    'RuleEngine',
    'Rule',
    'RuleType',
    'IndustryKnowledgeBase',
    'IndustryProfile',
]


def create_knowledge_graph(base_path: str = None):
    """工厂函数: 创建知识图谱system_instance（延迟加载）"""
    from .graph_engine import KnowledgeGraphEngine
    return KnowledgeGraphEngine(base_path)
