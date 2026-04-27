"""行业知识图谱 - 知识自动补全器"""
import logging
from typing import Dict, List, TYPE_CHECKING

__all__ = [
    'identify_gaps',
    'suggest_completions',
]

if TYPE_CHECKING:
    from .industry_knowledge_graph import IndustryKnowledgeGraph
    from ._ikg_types import Entity

logger = logging.getLogger(__name__)

class KnowledgeAutoCompleter:
    """知识自动补全器"""

    def __init__(self, knowledge_graph: 'IndustryKnowledgeGraph'):
        self.kg = knowledge_graph
        self.completion_patterns: Dict[str, List[str]] = {
            "company": ["founded", "headquarters", "employees", "revenue"],
            "product": ["launch_date", "category", "price_range", "features"],
            "industry": ["market_size", "growth_rate", "key_players", "trends"],
            "technology": ["maturity", "adoption_rate", "use_cases", "alternatives"]
        }

    def identify_gaps(self, entity_id: str) -> List[Dict]:
        """recognize实体属性缺口"""
        from ._ikg_types import Entity
        entity = self.kg.get_entity(entity_id)
        if not entity:
            return []

        gaps = []
        expected_attrs = self.completion_patterns.get(entity.entity_type.value, [])

        for attr in expected_attrs:
            if attr not in entity.attributes or entity.attributes[attr] is None:
                gaps.append({
                    "attribute": attr,
                    "importance": "high" if attr in ["founded", "market_size"] else "medium",
                    "suggested_sources": self._suggest_sources(entity, attr)
                })

        return gaps

    def _suggest_sources(self, entity: 'Entity', attribute: str) -> List[str]:
        """建议数据来源"""
        from ._ikg_types import EntityType
        sources = []

        if entity.entity_type == EntityType.COMPANY:
            sources = ["公司官网", "工商信息", "财报", "新闻报道"]
        elif entity.entity_type == EntityType.INDUSTRY:
            sources = ["行业报告", "市场研究", "政府统计", "行业协会"]
        elif entity.entity_type == EntityType.TECHNOLOGY:
            sources = ["技术文档", "GitHub", "学术论文", "技术博客"]

        return sources

    def suggest_completions(self, entity_id: str) -> Dict:
        """建议自动补全"""
        entity = self.kg.get_entity(entity_id)
        if not entity:
            return {"error": "实体不存在"}

        gaps = self.identify_gaps(entity_id)

        # 基于相似实体推断属性
        inferred_values = self._infer_from_similar(entity_id, gaps)

        return {
            "entity_id": entity_id,
            "entity_name": entity.name,
            "gaps": gaps,
            "inferred_values": inferred_values,
            "confidence_scores": self._calculate_confidence(inferred_values)
        }

    def _infer_from_similar(self, entity_id: str, gaps: List[Dict]) -> Dict:
        """从相似实体推断属性值"""
        inferred = {}

        similar = self.kg.find_similar_entities(entity_id, top_k=3)

        for gap in gaps:
            attr = gap["attribute"]
            values = []

            for sim_id, similarity in similar:
                sim_entity = self.kg.get_entity(sim_id)
                if sim_entity and attr in sim_entity.attributes:
                    values.append({
                        "value": sim_entity.attributes[attr],
                        "source": sim_entity.name,
                        "similarity": similarity
                    })

            if values:
                # 选择相似度最高的值
                best = max(values, key=lambda x: x["similarity"])
                inferred[attr] = best

        return inferred

    def _calculate_confidence(self, inferred_values: Dict) -> Dict:
        """计算置信度分数"""
        scores = {}

        for attr, data in inferred_values.items():
            if isinstance(data, dict) and "similarity" in data:
                # 基于相似度和数据源数量计算置信度
                base_confidence = data["similarity"]
                scores[attr] = min(0.9, base_confidence * 1.2)
            else:
                scores[attr] = 0.5

        return scores
