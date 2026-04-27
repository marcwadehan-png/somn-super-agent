"""
__all__ = [
    'add_concept',
    'add_relation',
    'find_concepts',
    'get_category_summary',
    'get_concept',
    'get_concept_network',
    'to_dict',
]

概念管理器 - 管理三层知识架构的概念层
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ConceptCategory(Enum):
    """概念分类"""
    USER = "user"                 # 用户相关
    PRODUCT = "product"           # 产品相关
    MARKET = "market"             # 市场相关
    STRATEGY = "strategy"         # strategy相关
    METRIC = "metric"             # metrics相关
    CHANNEL = "channel"           # 渠道相关
    CONTENT = "content"           # 内容相关
    TECHNOLOGY = "technology"     # 技术相关
    INDUSTRY = "industry"         # 行业相关

class ConceptRelation(Enum):
    """概念关系类型"""
    IS_A = "is_a"                 # 是一种
    HAS_PART = "has_part"         # 有部分
    USED_FOR = "used_for"         # 用于
    LEADS_TO = "leads_to"         # 导致
    DEPENDS_ON = "depends_on"     # 依赖于
    SIMILAR_TO = "similar_to"     # 相似于
    CONTRASTS_WITH = "contrasts_with"  # 对比于
    MEASURES = "measures"         # 衡量
    INFLUENCES = "influences"     # 影响
    PART_OF = "part_of"           # 属于
    APPLIES_TO = "applies_to"     # 应用于
    AFFECTS = "affects"           # 影响
    DETERMINES = "determines"     # 决定
    IMPACTS = "impacts"           # 影响

@dataclass
class Concept:
    """概念定义"""
    concept_id: str
    name: str
    category: ConceptCategory
    definition: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    examples: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    confidence: float = 1.0
    source: str = "manual"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'concept_id': self.concept_id,
            'name': self.name,
            'category': self.category.value,
            'definition': self.definition,
            'attributes': self.attributes,
            'examples': self.examples,
            'related_concepts': self.related_concepts,
            'confidence': self.confidence,
            'source': self.source,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

@dataclass
class ConceptRelationInstance:
    """概念关系实例"""
    relation_type: ConceptRelation
    source_concept: str
    target_concept: str
    strength: float = 1.0  # 关系强度 0-1
    evidence: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class ConceptManager:
    """概念管理器"""
    
    def __init__(self, graph_engine=None):
        self.graph_engine = graph_engine
        self.concepts: Dict[str, Concept] = {}
        self.relations: List[ConceptRelationInstance] = []
        
        # init核心概念
        self._init_core_concepts()
    
    def _init_core_concepts(self):
        """init核心增长概念"""
        core_concepts = [
            # 用户相关
            {
                'name': '用户生命周期',
                'category': ConceptCategory.USER,
                'definition': '用户从首次接触产品到最终流失的完整过程',
                'attributes': {'stages': ['获客', '激活', '留存', '变现', '推荐']}
            },
            {
                'name': '用户画像',
                'category': ConceptCategory.USER,
                'definition': '基于用户行为,属性,偏好构建的用户characteristics描述',
                'attributes': {'dimensions': ['人口属性', '行为characteristics', '兴趣偏好', '消费能力']}
            },
            {
                'name': '用户分层',
                'category': ConceptCategory.USER,
                'definition': '根据用户价值,行为等维度将用户划分为不同群体',
                'attributes': {'models': ['RFM', 'AARRR', 'CLV']}
            },
            
            # 增长相关
            {
                'name': '增长黑客',
                'category': ConceptCategory.STRATEGY,
                'definition': '通过数据驱动,快速实验实现用户增长的strategy方法',
                'attributes': {'principles': ['数据驱动', '快速迭代', '病毒传播', '产品优化']}
            },
            {
                'name': 'AARRR模型',
                'category': ConceptCategory.STRATEGY,
                'definition': '用户生命周期管理的五个关键阶段',
                'attributes': {'stages': ['Acquisition', 'Activation', 'Retention', 'Revenue', 'Referral']}
            },
            {
                'name': '北极星metrics',
                'category': ConceptCategory.METRIC,
                'definition': '能够最准确反映产品核心价值交付的关键metrics',
                'attributes': {'characteristics': ['反映价值', '可action', '可衡量']}
            },
            
            # 渠道相关
            {
                'name': '获客渠道',
                'category': ConceptCategory.CHANNEL,
                'definition': 'get新用户的各种途径和方式',
                'attributes': {'types': ['付费', '自然', '病毒', '合作']}
            },
            {
                'name': '渠道归因',
                'category': ConceptCategory.CHANNEL,
                'definition': '确定用户转化过程中各渠道贡献度的方法',
                'attributes': {'models': ['首次点击', '最后点击', '线性', '时间衰减']}
            },
            
            # 内容相关
            {
                'name': '内容营销',
                'category': ConceptCategory.CONTENT,
                'definition': '通过创造和分发有价值内容吸引和留住目标受众',
                'attributes': {'formats': ['文章', '视频', '音频', '图文']}
            },
            {
                'name': '病毒系数',
                'category': ConceptCategory.METRIC,
                'definition': '每个用户平均带来的新用户数量',
                'attributes': {'threshold': 1.0, 'formula': '邀请人数 × 转化率'}
            },
            
            # 产品相关
            {
                'name': '产品市场契合',
                'category': ConceptCategory.PRODUCT,
                'definition': '产品满足市场需求的程度',
                'attributes': {'indicators': ['留存率', 'NPS', '有机增长']}
            },
            {
                'name': '最小可行产品',
                'category': ConceptCategory.PRODUCT,
                'definition': '用最少资源快速验证核心假设的产品版本',
                'attributes': {'goal': '验证假设', 'method': '快速迭代'}
            },
            
            # 市场相关
            {
                'name': '市场规模',
                'category': ConceptCategory.MARKET,
                'definition': '特定市场的潜在收入或用户总量',
                'attributes': {'metrics': ['TAM', 'SAM', 'SOM']}
            },
            {
                'name': '竞争分析',
                'category': ConceptCategory.MARKET,
                'definition': '系统分析竞争对手的优势,劣势,strategy',
                'attributes': {'frameworks': ['SWOT', '波特五力', '价值链']}
            }
        ]
        
        for concept_data in core_concepts:
            self.add_concept(**concept_data)
        
        # 建立概念关系
        self._build_concept_relations()
    
    def _build_concept_relations(self):
        """建立核心概念关系"""
        relations = [
            ('用户生命周期', ConceptRelation.HAS_PART, '用户分层'),
            ('用户画像', ConceptRelation.USED_FOR, '用户分层'),
            ('AARRR模型', ConceptRelation.IS_A, '用户生命周期'),
            ('增长黑客', ConceptRelation.DEPENDS_ON, '北极星metrics'),
            ('获客渠道', ConceptRelation.LEADS_TO, '用户生命周期'),
            ('内容营销', ConceptRelation.USED_FOR, '获客渠道'),
            ('病毒系数', ConceptRelation.MEASURES, '获客渠道'),
            ('产品市场契合', ConceptRelation.DEPENDS_ON, '用户留存'),
            ('最小可行产品', ConceptRelation.USED_FOR, '产品市场契合'),
        ]
        
        for source, relation, target in relations:
            self.add_relation(source, relation, target)
    
    def add_concept(self, name: str, category: ConceptCategory,
                   definition: str = "", attributes: Dict = None,
                   examples: List[str] = None, confidence: float = 1.0,
                   source: str = "manual") -> Concept:
        """添加概念"""
        concept_id = f"{category.value}:{name}"
        
        concept = Concept(
            concept_id=concept_id,
            name=name,
            category=category,
            definition=definition,
            attributes=attributes or {},
            examples=examples or [],
            confidence=confidence,
            source=source
        )
        
        self.concepts[concept_id] = concept
        
        # 同步到图谱
        if self.graph_engine:
            from .graph_engine import NodeType
            self.graph_engine.add_node(
                name=name,
                node_type=NodeType.CONCEPT,
                properties={
                    'category': category.value,
                    'definition': definition,
                    **(attributes or {})
                },
                source=source,
                confidence=confidence
            )
        
        return concept
    
    def get_concept(self, name: str, category: ConceptCategory = None) -> Optional[Concept]:
        """get概念"""
        if category:
            concept_id = f"{category.value}:{name}"
            return self.concepts.get(concept_id)
        else:
            # 搜索所有分类
            for concept in self.concepts.values():
                if concept.name == name:
                    return concept
        return None
    
    def find_concepts(self, category: ConceptCategory = None,
                     keyword: str = None) -> List[Concept]:
        """查找概念"""
        results = []
        for concept in self.concepts.values():
            if category and concept.category != category:
                continue
            if keyword and keyword.lower() not in concept.name.lower():
                continue
            results.append(concept)
        return results
    
    def add_relation(self, source_name: str, relation: ConceptRelation,
                    target_name: str, strength: float = 1.0,
                    evidence: List[str] = None):
        """添加概念关系"""
        relation_instance = ConceptRelationInstance(
            relation_type=relation,
            source_concept=source_name,
            target_concept=target_name,
            strength=strength,
            evidence=evidence or []
        )
        
        self.relations.append(relation_instance)
        
        # 同步到图谱
        if self.graph_engine:
            from .graph_engine import NodeType, EdgeType
            edge_type_map = {
                ConceptRelation.IS_A: EdgeType.BELONGS_TO,
                ConceptRelation.HAS_PART: EdgeType.BELONGS_TO,
                ConceptRelation.USED_FOR: EdgeType.APPLIES_TO,
                ConceptRelation.LEADS_TO: EdgeType.CAUSES,
                ConceptRelation.DEPENDS_ON: EdgeType.DEPENDS_ON,
                ConceptRelation.SIMILAR_TO: EdgeType.SIMILAR_TO,
            }
            
            edge_type = edge_type_map.get(relation, EdgeType.RELATED_TO)
            self.graph_engine.add_edge(
                source_name, NodeType.CONCEPT,
                target_name, NodeType.CONCEPT,
                edge_type,
                properties={'relation': relation.value, 'strength': strength}
            )
    
    def get_concept_network(self, concept_name: str, depth: int = 2) -> Dict:
        """get概念网络"""
        concept = self.get_concept(concept_name)
        if not concept:
            return {}
        
        # 查找相关关系
        related = {'concepts': [], 'relations': []}
        
        for relation in self.relations:
            if relation.source_concept == concept_name:
                related['concepts'].append(relation.target_concept)
                related['relations'].append({
                    'from': concept_name,
                    'to': relation.target_concept,
                    'type': relation.relation_type.value,
                    'strength': relation.strength
                })
            elif relation.target_concept == concept_name:
                related['concepts'].append(relation.source_concept)
                related['relations'].append({
                    'from': relation.source_concept,
                    'to': concept_name,
                    'type': relation.relation_type.value,
                    'strength': relation.strength
                })
        
        return related
    
    def get_category_summary(self) -> Dict[str, int]:
        """get分类统计"""
        summary = {}
        for category in ConceptCategory:
            count = len([c for c in self.concepts.values() if c.category == category])
            summary[category.value] = count
        return summary
