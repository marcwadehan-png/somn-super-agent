"""行业知识图谱 - 关系推理引擎"""
import logging
from typing import Dict, List, TYPE_CHECKING

__all__ = [
    'infer_relations',
]

if TYPE_CHECKING:
    from .industry_knowledge_graph import IndustryKnowledgeGraph, Entity, Relation, RelationType, EntityType

logger = logging.getLogger(__name__)

class RelationInferenceEngine:
    """关系推理引擎"""

    def __init__(self, knowledge_graph: 'IndustryKnowledgeGraph'):
        self.kg = knowledge_graph
        self.inference_rules: List[Dict] = []
        self._initialize_rules()

    def _initialize_rules(self):
        """init推理规则"""
        self.inference_rules = [
            {
                "name": "传递性规则",
                "description": "如果A属于B,B属于C,则A属于C",
                "apply": self._apply_transitivity_rule
            },
            {
                "name": "竞争性传递",
                "description": "如果A与B竞争,B与C竞争,则A与C可能存在竞争关系",
                "apply": self._apply_competition_rule
            },
            {
                "name": "相似性扩展",
                "description": "如果A与B相似,B与C相似,则A与C可能相似",
                "apply": self._apply_similarity_rule
            },
            {
                "name": "技术采用链",
                "description": "如果公司A采用技术X,公司B与A相似,则B可能采用X",
                "apply": self._apply_tech_adoption_rule
            }
        ]

    def infer_relations(self, entity_id: str, max_depth: int = 2) -> List['Relation']:
        """推理新关系"""
        from ._ikg_types import Relation, RelationType
        inferred = []

        for rule in self.inference_rules:
            try:
                new_relations = rule["apply"](entity_id, max_depth)
                inferred.extend(new_relations)
            except Exception as e:
                logger.warning(f"规则 {rule['name']} 应用失败: {e}")

        return inferred

    def _apply_transitivity_rule(self, entity_id: str, max_depth: int) -> List['Relation']:
        """应用传递性规则"""
        from ._ikg_types import Relation, RelationType
        inferred = []

        # get实体属于的关系
        belongs_to = self.kg.get_related_entities(entity_id, RelationType.BELONGS_TO)

        for parent, rel in belongs_to:
            # 检查父实体是否也属于其他实体
            parent_belongs = self.kg.get_related_entities(parent.id, RelationType.BELONGS_TO)
            for grandparent, _ in parent_belongs:
                # 检查是否已存在直接关系
                exists = any(
                    r.source_id == entity_id and r.target_id == grandparent.id
                    for r in self.kg.relations
                )
                if not exists:
                    inferred.append(Relation(
                        source_id=entity_id,
                        target_id=grandparent.id,
                        relation_type=RelationType.BELONGS_TO,
                        weight=0.6,
                        attributes={"inferred": True, "rule": "transitivity"}
                    ))

        return inferred

    def _apply_competition_rule(self, entity_id: str, max_depth: int) -> List['Relation']:
        """应用竞争性传递规则"""
        from ._ikg_types import Relation, RelationType
        inferred = []

        competitors = self.kg.get_related_entities(entity_id, RelationType.COMPETES_WITH)

        for comp1, _ in competitors:
            comp1_competitors = self.kg.get_related_entities(comp1.id, RelationType.COMPETES_WITH)
            for comp2, _ in comp1_competitors:
                if comp2.id != entity_id:
                    exists = any(
                        (r.source_id == entity_id and r.target_id == comp2.id) or
                        (r.source_id == comp2.id and r.target_id == entity_id)
                        for r in self.kg.relations
                    )
                    if not exists:
                        inferred.append(Relation(
                            source_id=entity_id,
                            target_id=comp2.id,
                            relation_type=RelationType.COMPETES_WITH,
                            weight=0.4,
                            attributes={"inferred": True, "rule": "competition_transitivity"}
                        ))

        return inferred

    def _apply_similarity_rule(self, entity_id: str, max_depth: int) -> List['Relation']:
        """应用相似性扩展规则"""
        from ._ikg_types import Relation, RelationType
        inferred = []

        similar = self.kg.get_related_entities(entity_id, RelationType.SIMILAR_TO)

        for sim1, _ in similar:
            sim1_similar = self.kg.get_related_entities(sim1.id, RelationType.SIMILAR_TO)
            for sim2, _ in sim1_similar:
                if sim2.id != entity_id:
                    exists = any(
                        (r.source_id == entity_id and r.target_id == sim2.id) or
                        (r.source_id == sim2.id and r.target_id == entity_id)
                        for r in self.kg.relations
                    )
                    if not exists:
                        inferred.append(Relation(
                            source_id=entity_id,
                            target_id=sim2.id,
                            relation_type=RelationType.SIMILAR_TO,
                            weight=0.5,
                            attributes={"inferred": True, "rule": "similarity_transitivity"}
                        ))

        return inferred

    def _apply_tech_adoption_rule(self, entity_id: str, max_depth: int) -> List['Relation']:
        """应用技术采用链规则"""
        from ._ikg_types import Relation, RelationType, EntityType
        inferred = []

        entity = self.kg.get_entity(entity_id)
        if not entity or entity.entity_type != EntityType.COMPANY:
            return inferred

        # get公司使用的技术
        technologies = self.kg.get_related_entities(entity_id, RelationType.USES)

        # get相似公司
        similar_companies = self.kg.get_related_entities(entity_id, RelationType.SIMILAR_TO)

        for tech, _ in technologies:
            for sim_company, _ in similar_companies:
                # 检查相似公司是否已使用该技术
                already_uses = any(
                    r.source_id == sim_company.id and r.target_id == tech.id
                    for r in self.kg.relations
                )
                if not already_uses:
                    inferred.append(Relation(
                        source_id=sim_company.id,
                        target_id=tech.id,
                        relation_type=RelationType.USES,
                        weight=0.5,
                        attributes={
                            "inferred": True,
                            "rule": "tech_adoption",
                            "source_company": entity_id
                        }
                    ))

        return inferred
