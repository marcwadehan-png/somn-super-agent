"""行业知识图谱 - 行业对比分析器"""
import logging
from typing import Dict, List, TYPE_CHECKING

__all__ = [
    'compare_industries',
    'generate_industry_report',
]

if TYPE_CHECKING:
    from .industry_knowledge_graph import IndustryKnowledgeGraph
    from ._ikg_types import Entity

logger = logging.getLogger(__name__)

class IndustryComparator:
    """行业对比分析器"""

    def __init__(self, knowledge_graph: 'IndustryKnowledgeGraph'):
        self.kg = knowledge_graph

    def compare_industries(self, industry_id1: str, industry_id2: str) -> Dict:
        """对比两个行业"""
        ind1 = self.kg.get_entity(industry_id1)
        ind2 = self.kg.get_entity(industry_id2)

        if not ind1 or not ind2:
            return {"error": "行业不存在"}

        comparison = {
            "industry_1": {"id": industry_id1, "name": ind1.name},
            "industry_2": {"id": industry_id2, "name": ind2.name},
            "similarity_score": self._calculate_similarity(ind1, ind2),
            "common_entities": self._find_common_entities(industry_id1, industry_id2),
            "attribute_comparison": self._compare_attributes(ind1, ind2),
            "competitive_landscape": self._analyze_competition(industry_id1, industry_id2),
            "cross_industry_opportunities": self._find_opportunities(industry_id1, industry_id2)
        }

        return comparison

    def _calculate_similarity(self, ind1: 'Entity', ind2: 'Entity') -> float:
        """计算行业相似度"""
        # 基于属性重叠度计算
        attrs1 = set(ind1.attributes.keys())
        attrs2 = set(ind2.attributes.keys())

        if not attrs1 and not attrs2:
            return 0.0

        intersection = len(attrs1 & attrs2)
        union = len(attrs1 | attrs2)

        return intersection / union if union > 0 else 0.0

    def _find_common_entities(self, ind_id1: str, ind_id2: str) -> List[Dict]:
        """查找两个行业的共同实体"""
        from ._ikg_types import RelationType
        related1 = set(e.id for e, _ in self.kg.get_related_entities(ind_id1))
        related2 = set(e.id for e, _ in self.kg.get_related_entities(ind_id2))

        common = related1 & related2

        return [
            {
                "id": eid,
                "name": self.kg.get_entity(eid).name if self.kg.get_entity(eid) else eid,
                "type": self.kg.get_entity(eid).entity_type.value if self.kg.get_entity(eid) else "unknown"
            }
            for eid in common
        ]

    def _compare_attributes(self, ind1: 'Entity', ind2: 'Entity') -> Dict:
        """对比行业属性"""
        all_attrs = set(ind1.attributes.keys()) | set(ind2.attributes.keys())

        comparison = {}
        for attr in all_attrs:
            val1 = ind1.attributes.get(attr, "N/A")
            val2 = ind2.attributes.get(attr, "N/A")

            comparison[attr] = {
                ind1.name: val1,
                ind2.name: val2,
                "same": val1 == val2 and val1 != "N/A"
            }

        return comparison

    def _analyze_competition(self, ind_id1: str, ind_id2: str) -> Dict:
        """分析行业间竞争关系"""
        from ._ikg_types import EntityType, RelationType
        # get两个行业的公司
        companies1 = [
            e for e, r in self.kg.get_related_entities(ind_id1, RelationType.BELONGS_TO)
            if e.entity_type == EntityType.COMPANY
        ]
        companies2 = [
            e for e, r in self.kg.get_related_entities(ind_id2, RelationType.BELONGS_TO)
            if e.entity_type == EntityType.COMPANY
        ]

        # 检查公司间竞争关系
        cross_competition = []
        for c1 in companies1:
            for c2 in companies2:
                competes = any(
                    (r.source_id == c1.id and r.target_id == c2.id) or
                    (r.source_id == c2.id and r.target_id == c1.id)
                    for r in self.kg.relations
                )
                if competes:
                    cross_competition.append({
                        "company_1": c1.name,
                        "company_2": c2.name
                    })

        return {
            "companies_in_industry_1": len(companies1),
            "companies_in_industry_2": len(companies2),
            "cross_industry_competition": cross_competition,
            "competition_intensity": len(cross_competition) / max(len(companies1) * len(companies2), 1)
        }

    def _find_opportunities(self, ind_id1: str, ind_id2: str) -> List[Dict]:
        """发现跨行业机会"""
        from ._ikg_types import EntityType, RelationType
        opportunities = []

        # get行业使用的技术
        tech1 = [
            e for e, r in self.kg.get_related_entities(ind_id1, RelationType.USES)
            if e.entity_type == EntityType.TECHNOLOGY
        ]
        tech2 = [
            e for e, r in self.kg.get_related_entities(ind_id2, RelationType.USES)
            if e.entity_type == EntityType.TECHNOLOGY
        ]

        # 技术转移机会
        tech1_names = {t.name for t in tech1}
        tech2_names = {t.name for t in tech2}

        tech_diff = tech1_names - tech2_names
        for tech_name in tech_diff:
            opportunities.append({
                "type": "technology_transfer",
                "description": f"将 {tech_name} 从技术密集型行业应用到另一行业",
                "potential_impact": "high"
            })

        return opportunities

    def generate_industry_report(self, industry_id: str) -> Dict:
        """generate行业分析报告"""
        industry = self.kg.get_entity(industry_id)
        if not industry:
            return {"error": "行业不存在"}

        # get相关实体
        related = self.kg.get_related_entities(industry_id)

        # 分类统计
        entity_counts = {}
        for entity, _ in related:
            etype = entity.entity_type.value
            entity_counts[etype] = entity_counts.get(etype, 0) + 1

        # get案例
        cases = self.kg.search_cases(industry=industry.name)

        # 相似行业
        similar = self.kg.find_similar_entities(industry_id, top_k=5)

        return {
            "industry": industry.to_dict(),
            "ecosystem": entity_counts,
            "case_studies": [c.to_dict() for c in cases],
            "similar_industries": [
                {
                    "id": sid,
                    "name": self.kg.get_entity(sid).name if self.kg.get_entity(sid) else sid,
                    "similarity": sim
                }
                for sid, sim in similar
            ],
            "key_metrics": self._extract_key_metrics(industry_id),
            "trends": self._extract_trends(industry_id)
        }

    def _extract_key_metrics(self, industry_id: str) -> List[Dict]:
        """提取关键metrics"""
        from ._ikg_types import EntityType
        metrics = []

        related = self.kg.get_related_entities(industry_id)
        for entity, rel in related:
            if entity.entity_type == EntityType.METRIC:
                metrics.append({
                    "name": entity.name,
                    "value": entity.attributes.get("value"),
                    "unit": entity.attributes.get("unit"),
                    "trend": entity.attributes.get("trend")
                })

        return metrics

    def _extract_trends(self, industry_id: str) -> List[Dict]:
        """提取行业趋势"""
        from ._ikg_types import EntityType
        trends = []

        related = self.kg.get_related_entities(industry_id)
        for entity, rel in related:
            if entity.entity_type == EntityType.TREND:
                trends.append({
                    "name": entity.name,
                    "impact": entity.attributes.get("impact", "medium"),
                    "timeframe": entity.attributes.get("timeframe", "unknown"),
                    "description": entity.description
                })

        return trends
