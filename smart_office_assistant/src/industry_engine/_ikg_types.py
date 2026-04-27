"""行业知识图谱 - 类型定义"""
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any

__all__ = [
    'to_dict',
]

class EntityType(Enum):
    """实体类型"""
    INDUSTRY = "industry"           # 行业
    COMPANY = "company"             # 公司
    PRODUCT = "product"             # 产品
    STRATEGY = "strategy"           # strategy
    METRIC = "metric"               # metrics
    TREND = "trend"                 # 趋势
    CHALLENGE = "challenge"         # 挑战
    BEST_PRACTICE = "best_practice" # 最佳实践
    TECHNOLOGY = "technology"       # 技术
    MARKET = "market"               # 市场

class RelationType(Enum):
    """关系类型"""
    BELONGS_TO = "belongs_to"           # 属于
    COMPETES_WITH = "competes_with"     # 竞争
    PARTNERS_WITH = "partners_with"     # 合作
    USES = "uses"                       # 使用
    IMPLEMENTS = "implements"           # 实施
    MEASURED_BY = "measured_by"         # 通过...衡量
    INFLUENCED_BY = "influenced_by"     # 受...影响
    LEADS_TO = "leads_to"               # 导致
    SIMILAR_TO = "similar_to"           # 相似
    DEPENDS_ON = "depends_on"           # 依赖

@dataclass
class Entity:
    """知识图谱实体"""
    id: str
    name: str
    entity_type: EntityType
    attributes: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "entity_type": self.entity_type.value,
            "attributes": self.attributes,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

@dataclass
class Relation:
    """知识图谱关系"""
    source_id: str
    target_id: str
    relation_type: RelationType
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type.value,
            "weight": self.weight,
            "attributes": self.attributes,
            "created_at": self.created_at.isoformat()
        }

@dataclass
class CaseStudy:
    """案例研究"""
    id: str
    title: str
    industry: str
    company: str
    challenge: str
    solution: str
    results: Dict[str, Any]
    key_learnings: List[str]
    tags: List[str]
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "industry": self.industry,
            "company": self.company,
            "challenge": self.challenge,
            "solution": self.solution,
            "results": self.results,
            "key_learnings": self.key_learnings,
            "tags": self.tags,
            "created_at": self.created_at.isoformat()
        }
