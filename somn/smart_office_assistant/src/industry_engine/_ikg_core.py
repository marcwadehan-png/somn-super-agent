"""行业知识图谱 - 核心模块"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import networkx as nx

from ._ikg_types import Entity, EntityType, Relation, RelationType, CaseStudy
from ._ikg_inference import RelationInferenceEngine
from ._ikg_autocomplete import KnowledgeAutoCompleter
from ._ikg_comparator import IndustryComparator

__all__ = [
    'add_case',
    'add_entity',
    'add_relation',
    'compare_industries',
    'complete_knowledge',
    'create_default_knowledge_graph',
    'find_path',
    'find_similar_entities',
    'generate_industry_report',
    'get_entity',
    'get_industry_insights',
    'get_related_entities',
    'get_statistics',
    'infer_relations',
    'load',
    'recommend_strategies',
    'save',
    'search_cases',
]

logger = logging.getLogger(__name__)

class IndustryKnowledgeGraph:
    """
    行业知识图谱 - v1.0 增强版

    管理行业实体,关系和案例库
    - 关系推理引擎
    - 知识自动补全
    - 行业对比分析
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.graph = nx.DiGraph()
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self.cases: Dict[str, CaseStudy] = {}

        self.storage_path = Path(storage_path) if storage_path else None

        # init增强组件
        self.inference_engine = RelationInferenceEngine(self)
        self.auto_completer = KnowledgeAutoCompleter(self)
        self.comparator = IndustryComparator(self)

        # init15个行业的知识图谱
        self._initialize_industries()

    def _initialize_industries(self):
        """init15个行业的基础知识"""
        industries = [
            ("saas_b2b", "SaaS B2B", "企业级软件服务"),
            ("saas_b2c", "SaaS B2C", "消费级软件服务"),
            ("ecommerce", "电商零售", "在线零售与电商平台"),
            ("fintech", "金融科技", "金融服务科技"),
            ("healthcare", "医疗健康", "医疗服务与健康科技"),
            ("education", "教育培训", "在线教育与培训"),
            ("real_estate", "房地产", "房地产开发与服务"),
            ("travel", "旅游出行", "旅游与出行服务"),
            ("food_beverage", "餐饮美食", "餐饮服务"),
            ("ai_tech", "AI科技", "人工智能技术与应用"),
            ("new_energy", "新能源汽车", "新能源汽车产业"),
            ("luxury", "奢侈品", "奢侈品零售"),
            ("sports_fitness", "运动健身", "运动与健身服务"),
            ("pet", "宠物经济", "宠物产品与服务"),
            ("content_gaming", "内容媒体/游戏", "内容创作与游戏"),
        ]

        for ind_id, name, desc in industries:
            self.add_entity(Entity(
                id=ind_id,
                name=name,
                entity_type=EntityType.INDUSTRY,
                description=desc,
                attributes={"established": True}
            ))

        logger.info(f"✅ init {len(industries)} 个行业实体")

    def add_entity(self, entity: Entity) -> bool:
        """添加实体"""
        if entity.id in self.entities:
            logger.warning(f"实体已存在: {entity.id}")
            return False

        self.entities[entity.id] = entity
        self.graph.add_node(
            entity.id,
            name=entity.name,
            type=entity.entity_type.value,
            **entity.attributes
        )
        return True

    def add_relation(self, relation: Relation) -> bool:
        """添加关系"""
        if relation.source_id not in self.entities:
            logger.error(f"源实体不存在: {relation.source_id}")
            return False
        if relation.target_id not in self.entities:
            logger.error(f"目标实体不存在: {relation.target_id}")
            return False

        self.relations.append(relation)
        self.graph.add_edge(
            relation.source_id,
            relation.target_id,
            relation_type=relation.relation_type.value,
            weight=relation.weight,
            **relation.attributes
        )
        return True

    def add_case(self, case: CaseStudy) -> bool:
        """添加案例"""
        if case.id in self.cases:
            logger.warning(f"案例已存在: {case.id}")
            return False

        self.cases[case.id] = case

        # 创建案例实体并关联到行业
        case_entity = Entity(
            id=f"case_{case.id}",
            name=case.title,
            entity_type=EntityType.BEST_PRACTICE,
            description=f"{case.company}的{case.industry}案例",
            attributes={"company": case.company, "industry": case.industry}
        )
        self.add_entity(case_entity)

        # 建立与行业的关系
        industry_id = case.industry.lower().replace(" ", "_")
        if industry_id in self.entities:
            self.add_relation(Relation(
                source_id=case_entity.id,
                target_id=industry_id,
                relation_type=RelationType.BELONGS_TO,
                weight=1.0
            ))

        return True

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """get实体"""
        return self.entities.get(entity_id)

    def get_related_entities(
        self,
        entity_id: str,
        relation_type: Optional[RelationType] = None
    ) -> List[Tuple[Entity, Relation]]:
        """get相关实体"""
        if entity_id not in self.entities:
            return []

        related = []
        for rel in self.relations:
            if rel.source_id == entity_id:
                if relation_type is None or rel.relation_type == relation_type:
                    target = self.entities.get(rel.target_id)
                    if target:
                        related.append((target, rel))

        return related

    def find_path(
        self,
        source_id: str,
        target_id: str,
        max_length: int = 5
    ) -> Optional[List[str]]:
        """查找实体间的路径"""
        try:
            path = nx.shortest_path(
                self.graph,
                source=source_id,
                target=target_id
            )
            if len(path) <= max_length + 1:
                return path
        except nx.NetworkXNoPath:
            pass
        return None

    def find_similar_entities(
        self,
        entity_id: str,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """查找相似实体"""
        if entity_id not in self.graph:
            return []

        # 基于共同邻居计算相似度
        similarities = []
        entity = self.entities[entity_id]

        for other_id, other in self.entities.items():
            if other_id == entity_id:
                continue
            if other.entity_type != entity.entity_type:
                continue

            # 计算Jaccard相似度
            neighbors1 = set(self.graph.neighbors(entity_id))
            neighbors2 = set(self.graph.neighbors(other_id))

            if neighbors1 or neighbors2:
                intersection = len(neighbors1 & neighbors2)
                union = len(neighbors1 | neighbors2)
                similarity = intersection / union if union > 0 else 0

                if similarity > 0:
                    similarities.append((other_id, similarity))

        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def search_cases(
        self,
        industry: Optional[str] = None,
        tags: Optional[List[str]] = None,
        keyword: Optional[str] = None
    ) -> List[CaseStudy]:
        """搜索案例"""
        results = list(self.cases.values())

        if industry:
            results = [c for c in results if c.industry == industry]

        if tags:
            results = [c for c in results if any(t in c.tags for t in tags)]

        if keyword:
            keyword_lower = keyword.lower()
            results = [
                c for c in results
                if keyword_lower in c.title.lower()
                or keyword_lower in c.challenge.lower()
                or keyword_lower in c.solution.lower()
            ]

        return results

    def recommend_strategies(
        self,
        industry_id: str,
        challenge_type: Optional[str] = None
    ) -> List[Dict]:
        """基于知识图谱推荐strategy"""
        recommendations = []

        # 1. get行业相关实体
        industry = self.entities.get(industry_id)
        if not industry:
            return recommendations

        # 2. 查找最佳实践
        related = self.get_related_entities(industry_id, RelationType.HAS_PRACTICE)
        for entity, rel in related:
            if entity.entity_type == EntityType.BEST_PRACTICE:
                recommendations.append({
                    "type": "best_practice",
                    "entity": entity,
                    "relevance": rel.weight,
                    "reason": f"{industry.name}的行业最佳实践"
                })

        # 3. 查找相似行业的strategy
        similar = self.find_similar_entities(industry_id, top_k=3)
        for sim_id, similarity in similar:
            sim_industry = self.entities.get(sim_id)
            if sim_industry:
                # get相似行业的成功案例
                cases = self.search_cases(industry=sim_industry.name)
                for case in cases[:2]:  # 每个相似行业取2个案例
                    recommendations.append({
                        "type": "cross_industry",
                        "case": case,
                        "source_industry": sim_industry.name,
                        "similarity": similarity,
                        "reason": f"与{sim_industry.name}相似度{similarity:.2f}"
                    })

        # 按相关性排序
        recommendations.sort(key=lambda x: x.get("relevance", 0) + x.get("similarity", 0), reverse=True)
        return recommendations[:10]

    def infer_relations(self, entity_id: str, max_depth: int = 2) -> List[Relation]:
        """基于规则推理新关系 - v1.0 使用推理引擎"""
        return self.inference_engine.infer_relations(entity_id, max_depth)

    def complete_knowledge(self, entity_id: str) -> Dict:
        """自动补全实体知识"""
        return self.auto_completer.suggest_completions(entity_id)

    def compare_industries(self, industry_id1: str, industry_id2: str) -> Dict:
        """对比两个行业"""
        return self.comparator.compare_industries(industry_id1, industry_id2)

    def generate_industry_report(self, industry_id: str) -> Dict:
        """generate行业分析报告"""
        return self.comparator.generate_industry_report(industry_id)

    def get_industry_insights(self, industry_id: str) -> Dict:
        """get行业洞察"""
        industry = self.entities.get(industry_id)
        if not industry:
            return {}

        # 统计信息
        related_entities = self.get_related_entities(industry_id)

        entity_counts = {}
        for entity, _ in related_entities:
            etype = entity.entity_type.value
            entity_counts[etype] = entity_counts.get(etype, 0) + 1

        # 相关案例
        cases = self.search_cases(industry=industry.name)

        # 相关趋势
        trends = [
            e for e, _ in related_entities
            if e.entity_type == EntityType.TREND
        ]

        # 关键metrics
        metrics = [
            e for e, _ in related_entities
            if e.entity_type == EntityType.METRIC
        ]

        return {
            "industry": industry.to_dict(),
            "entity_statistics": entity_counts,
            "case_count": len(cases),
            "trends": [t.name for t in trends],
            "key_metrics": [m.name for m in metrics],
            "related_industries": [
                self.entities[e.id].name
                for e, r in related_entities
                if e.entity_type == EntityType.INDUSTRY
            ]
        }

    def save(self, path: Optional[str] = None):
        """保存知识图谱"""
        save_path = Path(path) if path else self.storage_path
        if not save_path:
            logger.error("未指定存储路径")
            return False

        save_path.mkdir(parents=True, exist_ok=True)

        # 保存实体
        entities_data = {eid: e.to_dict() for eid, e in self.entities.items()}
        with open(save_path / "entities.json", "w", encoding="utf-8") as f:
            json.dump(entities_data, f, ensure_ascii=False, indent=2)

        # 保存关系
        relations_data = [r.to_dict() for r in self.relations]
        with open(save_path / "relations.json", "w", encoding="utf-8") as f:
            json.dump(relations_data, f, ensure_ascii=False, indent=2)

        # 保存案例
        cases_data = {cid: c.to_dict() for cid, c in self.cases.items()}
        with open(save_path / "cases.json", "w", encoding="utf-8") as f:
            json.dump(cases_data, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ 知识图谱已保存到: {save_path}")
        return True

    def load(self, path: Optional[str] = None):
        """加载知识图谱"""
        load_path = Path(path) if path else self.storage_path
        if not load_path or not load_path.exists():
            logger.error(f"路径不存在: {load_path}")
            return False

        try:
            # 加载实体
            with open(load_path / "entities.json", "r", encoding="utf-8") as f:
                entities_data = json.load(f)
                for eid, edata in entities_data.items():
                    self.entities[eid] = Entity(
                        id=edata["id"],
                        name=edata["name"],
                        entity_type=EntityType(edata["entity_type"]),
                        attributes=edata.get("attributes", {}),
                        description=edata.get("description", "")
                    )

            # 加载关系
            with open(load_path / "relations.json", "r", encoding="utf-8") as f:
                relations_data = json.load(f)
                for rdata in relations_data:
                    self.relations.append(Relation(
                        source_id=rdata["source_id"],
                        target_id=rdata["target_id"],
                        relation_type=RelationType(rdata["relation_type"]),
                        weight=rdata.get("weight", 1.0),
                        attributes=rdata.get("attributes", {})
                    ))

            # 加载案例
            with open(load_path / "cases.json", "r", encoding="utf-8") as f:
                cases_data = json.load(f)
                for cid, cdata in cases_data.items():
                    self.cases[cid] = CaseStudy(
                        id=cdata["id"],
                        title=cdata["title"],
                        industry=cdata["industry"],
                        company=cdata["company"],
                        challenge=cdata["challenge"],
                        solution=cdata["solution"],
                        results=cdata.get("results", {}),
                        key_learnings=cdata.get("key_learnings", []),
                        tags=cdata.get("tags", [])
                    )

            logger.info(f"✅ 知识图谱已从 {load_path} 加载")
            return True

        except Exception as e:
            logger.error(f"加载知识图谱失败: {e}")
            return False

    def get_statistics(self) -> Dict:
        """get统计信息"""
        entity_type_counts = {}
        for entity in self.entities.values():
            etype = entity.entity_type.value
            entity_type_counts[etype] = entity_type_counts.get(etype, 0) + 1

        return {
            "total_entities": len(self.entities),
            "total_relations": len(self.relations),
            "total_cases": len(self.cases),
            "entity_types": entity_type_counts,
            "graph_density": nx.density(self.graph),
            "connected_components": nx.number_weakly_connected_components(self.graph)
        }

# ==================== 便捷函数 ====================

def create_default_knowledge_graph() -> IndustryKnowledgeGraph:
    """创建默认知识图谱(含示例数据)"""
    kg = IndustryKnowledgeGraph()

    # 添加一些示例公司
    companies = [
        Entity("comp_tesla", "特斯拉", EntityType.COMPANY,
               {"founded": 2003, "market_cap": "800B+"}, "电动汽车与清洁能源公司"),
        Entity("comp_bytedance", "字节跳动", EntityType.COMPANY,
               {"founded": 2012, "products": ["抖音", "TikTok"]}, "内容平台公司"),
        Entity("comp_alibaba", "阿里巴巴", EntityType.COMPANY,
               {"founded": 1999, "business": ["电商", "云计算"]}, "电商与科技公司"),
    ]

    for comp in companies:
        kg.add_entity(comp)

    # 添加关系
    kg.add_relation(Relation("comp_tesla", "new_energy", RelationType.BELONGS_TO, 1.0))
    kg.add_relation(Relation("comp_bytedance", "content_gaming", RelationType.BELONGS_TO, 1.0))
    kg.add_relation(Relation("comp_alibaba", "ecommerce", RelationType.BELONGS_TO, 1.0))

    # 添加示例案例
    case = CaseStudy(
        id="tesla_growth_001",
        title="特斯拉直销模式创新",
        industry="new_energy",
        company="特斯拉",
        challenge="传统汽车经销模式成本高,体验差",
        solution="建立直营店+线上预订的直销模式",
        results={
            "cost_reduction": "30%",
            "customer_satisfaction": "4.8/5",
            "sales_growth": "50% YoY"
        },
        key_learnings=[
            "直营模式提升用户体验",
            "线上预订降低运营成本",
            "品牌一致性更易维护"
        ],
        tags=["直销", "DTC", "用户体验", "成本控制"]
    )
    kg.add_case(case)

    return kg
