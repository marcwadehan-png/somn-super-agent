"""知识图谱引擎 - 类型定义"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

__all__ = [
    'from_dict',
    'to_dict',
]

class NodeType(Enum):
    """节点类型"""
    CONCEPT = "concept"           # 概念
    ENTITY = "entity"             # 实体
    INDUSTRY = "industry"         # 行业
    STRATEGY = "strategy"         # strategy
    METRIC = "metric"             # metrics
    CASE = "case"                 # 案例
    PATTERN = "pattern"           # 模式
    INSIGHT = "insight"           # 洞察
    RULE = "rule"                 # 规则

class EdgeType(Enum):
    """边类型"""
    BELONGS_TO = "belongs_to"     # 属于
    HAS_ATTRIBUTE = "has_attribute"  # 有属性
    RELATED_TO = "related_to"     # 相关
    CAUSES = "causes"             # 导致
    DEPENDS_ON = "depends_on"     # 依赖
    SIMILAR_TO = "similar_to"     # 相似
    APPLIES_TO = "applies_to"     # 应用于
    DERIVED_FROM = "derived_from" # 派生自

@dataclass
class GraphNode:
    """图谱节点"""
    node_id: str
    node_type: NodeType
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    source: str = "manual"        # 来源: manual, learning, import
    confidence: float = 1.0       # 置信度
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'node_id': self.node_id,
            'node_type': self.node_type.value,
            'name': self.name,
            'properties': self.properties,
            'source': self.source,
            'confidence': self.confidence,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GraphNode':
        from datetime import datetime
        return cls(
            node_id=data['node_id'],
            node_type=NodeType(data['node_type']),
            name=data['name'],
            properties=data.get('properties', {}),
            source=data.get('source', 'manual'),
            confidence=data.get('confidence', 1.0),
            created_at=data.get('created_at', datetime.now().isoformat()),
            updated_at=data.get('updated_at', datetime.now().isoformat())
        )

@dataclass
class GraphEdge:
    """图谱边"""
    source_id: str
    target_id: str
    edge_type: EdgeType
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    confidence: float = 1.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'edge_type': self.edge_type.value,
            'properties': self.properties,
            'weight': self.weight,
            'confidence': self.confidence,
            'created_at': self.created_at
        }

@dataclass
class GraphQuery:
    """图谱查询"""
    node_types: Optional[List[NodeType]] = None
    edge_types: Optional[List[EdgeType]] = None
    node_properties: Optional[Dict[str, Any]] = None
    name_pattern: Optional[str] = None
    min_confidence: float = 0.0
    limit: int = 100
