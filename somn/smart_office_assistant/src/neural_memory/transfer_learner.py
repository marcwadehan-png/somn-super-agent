"""
__all__ = [
    'create_transfer_hypothesis',
    'find_transferable_knowledge',
    'get_transfer_report',
    'learning_engine',
    'register_knowledge',
    'register_scenario',
    'report_validation_result',
]

迁移学习场景匹配器
Transfer Learner - 发现可迁移知识并触发 learn_by_transfer

填补技术债务:learning_engine.learn_by_transfer() 框架就绪但从未被触发.
本模块负责:
1. 维护知识-场景索引(哪些知识在哪些场景验证过)
2. 扫描新场景,judge是否有可迁移的高置信度知识
3. 自动generate迁移假设并触发验证
4. 与 ROI 追踪器联动,用验证结果更新知识置信度
"""

import logging
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)
@dataclass
class KnowledgeNode:
    """知识节点"""
    knowledge_id: str
    concept: str
    domain: str
    confidence: float
    applicability: List[str]
    source_scenarios: List[str]
    validation_count: int
    success_count: int
    failure_count: int
    last_validated: str
    tags: List[str]
    created_at: str

@dataclass
class ScenarioProfile:
    """场景画像"""
    scenario_id: str
    name: str
    industry: str
    keywords: List[str]
    features: Dict[str, Any]
    size: str = "unknown"
    stage: str = "unknown"

@dataclass
class TransferHypothesis:
    """迁移假设"""
    hypothesis_id: str
    source_knowledge_id: str
    target_scenario_id: str
    transfer_confidence: float
    validation_required: bool
    validation_plan: Dict
    status: str = "pending"
    actual_result: Optional[float] = None
    created_at: str = ""

class TransferLearner:
    """
    迁移学习场景匹配器

    核心逻辑:
    1. 知识注册:高质量知识进入知识库(置信度 >= 0.65)
    2. 场景扫描:新场景出现时,扫描知识库寻找可迁移知识
    3. 相似度计算:基于领域/关键词/标签计算迁移可行性
    4. 假设generate:为高可行性迁移创建假设
    5. 验证路由:将假设送往验证系统
    """

    INDUSTRY_KEYWORDS = {
        "电商": ["电商", "零售", "GMV", "转化率", "客单价", "复购", "私域", "选品", "流量", "种草"],
        "金融": ["金融", "风控", "信贷", "理财", "保险", "支付", "征信", "逾期", "资产"],
        "内容": ["内容", "创作", "UGC", "PGC", "社区", "互动", "完播率", "点赞", "粉丝", "达人"],
        "SaaS": ["SaaS", "续费率", "ARR", "MRR", "流失", "激活", "Onboarding", "NPS"],
        "教育": ["教育", "续费", "完课率", "学习", "课程", "师资", "招生", "转化", "留存"],
        "医疗": ["医疗", "患者", "诊疗", "处方", "慢病", "随访", "医疗AI"],
        "制造": ["制造", "产能", "供应链", "库存", "精益", "MES"],
        "通用": ["增长", "获客", "留存", "变现", "品牌", "数据驱动", "数字化", "AI"],
    }

    FEATURE_WEIGHTS = {
        "industry": 0.45,
        "keywords": 0.55,
    }

    def __init__(self, base_path: str = None):
        from src.core.paths import LEARNING_DIR
        self.base_path = Path(base_path) if base_path else LEARNING_DIR / "transfer_learner"
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.knowledge_path = self.base_path / "knowledge"
        self.scenarios_path = self.base_path / "scenarios"
        self.hypotheses_path = self.base_path / "hypotheses"
        for p in [self.knowledge_path, self.scenarios_path, self.hypotheses_path]:
            p.mkdir(exist_ok=True)

        self.params = {
            "min_confidence_to_register": 0.65,
            "min_transfer_confidence": 0.40,
            "similarity_threshold": 0.4,
        }

        self._knowledge: Dict[str, KnowledgeNode] = {}
        self._scenarios: Dict[str, ScenarioProfile] = {}
        self._hypotheses: Dict[str, TransferHypothesis] = {}
        self._learning_engine = None
        self._load_all()

    @property
    def learning_engine(self):
        if self._learning_engine is None:
            from .learning_engine import LearningEngine
            self._learning_engine = LearningEngine(str(self.base_path.parent.parent))
        return self._learning_engine

    def register_knowledge(self, concept: str, domain: str,
                           confidence: float, source_scenario: str,
                           tags: List[str] = None) -> str:
        """注册高质量知识到知识库"""
        if confidence < self.params["min_confidence_to_register"]:
            return ""

        existing = self._find_by_concept(concept, domain)
        if existing:
            self._update_knowledge(existing, confidence, source_scenario)
            return existing

        k_id = f"KN_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        tags = tags or self._infer_tags(concept, domain)
        node = KnowledgeNode(
            knowledge_id=k_id,
            concept=concept,
            domain=domain,
            confidence=confidence,
            applicability=[source_scenario],
            source_scenarios=[source_scenario],
            validation_count=1,
            success_count=1 if confidence >= 0.7 else 0,
            failure_count=0,
            last_validated=datetime.now().isoformat(),
            tags=tags,
            created_at=datetime.now().isoformat(),
        )
        self._knowledge[k_id] = node
        self._save_knowledge(node)
        return k_id

    def _find_by_concept(self, concept: str, domain: str) -> Optional[str]:
        for k_id, node in self._knowledge.items():
            if node.concept == concept and node.domain == domain:
                return k_id
        return None

    def _update_knowledge(self, k_id: str, new_confidence: float, new_scenario: str):
        node = self._knowledge[k_id]
        n = node.validation_count
        node.confidence = (n * node.confidence + new_confidence) / (n + 1)
        node.validation_count += 1
        if new_scenario not in node.source_scenarios:
            node.source_scenarios.append(new_scenario)
        node.last_validated = datetime.now().isoformat()
        self._save_knowledge(node)

    def register_scenario(self, scenario: ScenarioProfile) -> str:
        self._scenarios[scenario.scenario_id] = scenario
        self._save_scenario(scenario)
        return scenario.scenario_id

    def find_transferable_knowledge(self, target_scenario: ScenarioProfile,
                                    top_k: int = 5) -> List[Tuple[KnowledgeNode, float]]:
        """查找可迁移到目标场景的知识"""
        candidates = []
        for k_id, knowledge in self._knowledge.items():
            domain_sim = self._industry_similarity(knowledge.domain, target_scenario.industry)
            kw_sim = self._keyword_similarity(knowledge.tags, target_scenario.keywords)
            total_sim = (
                domain_sim * self.FEATURE_WEIGHTS["industry"] +
                kw_sim * self.FEATURE_WEIGHTS["keywords"]
            )
            if total_sim >= self.params["similarity_threshold"]:
                candidates.append((knowledge, total_sim))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_k]

    def create_transfer_hypothesis(self, source_knowledge: KnowledgeNode,
                                   target_scenario: ScenarioProfile) -> Optional[TransferHypothesis]:
        """为知识-场景对创建迁移假设"""
        candidates = self.find_transferable_knowledge(target_scenario, top_k=20)
        match_entry = next(
            (c for c in candidates if c[0].knowledge_id == source_knowledge.knowledge_id),
            None
        )
        if match_entry:
            transfer_conf = match_entry[1] * source_knowledge.confidence
        else:
            domain_sim = self._industry_similarity(source_knowledge.domain, target_scenario.industry)
            transfer_conf = domain_sim * source_knowledge.confidence * 0.85

        if transfer_conf < self.params["min_transfer_confidence"]:
            return None

        h_id = f"TH_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        hypothesis = TransferHypothesis(
            hypothesis_id=h_id,
            source_knowledge_id=source_knowledge.knowledge_id,
            target_scenario_id=target_scenario.scenario_id,
            transfer_confidence=transfer_conf,
            validation_required=transfer_conf < 0.6,
            validation_plan={
                "method": "A/B测试" if transfer_conf < 0.6 else "快速验证",
                "sample_size": 200 if transfer_conf < 0.6 else 50,
                "metrics": ["转化率", "采纳率"],
                "period": "2周" if transfer_conf < 0.6 else "3天",
            },
            status="pending",
            created_at=datetime.now().isoformat(),
        )
        self._hypotheses[h_id] = hypothesis
        self._save_hypothesis(hypothesis)

        try:
            source_kw = {
                "concept": source_knowledge.concept,
                "confidence": source_knowledge.confidence,
                "applicable_scenarios": source_knowledge.applicability,
                "domain": source_knowledge.domain,
            }
            target = {
                "场景名": target_scenario.name,
                "characteristics": target_scenario.keywords,
                "差异点": [f"领域迁移: {source_knowledge.domain} -> {target_scenario.industry}"],
            }
            event = self.learning_engine.learn_by_transfer(source_kw, target)
            if event:
                self.learning_engine.save_learning_event(event)
        except Exception as e:
            logger.debug(f"加载迁移学习数据失败: {e}")

        return hypothesis

    def report_validation_result(self, hypothesis_id: str, result: Dict[str, Any]) -> None:
        """报告验证结果"""
        if hypothesis_id not in self._hypotheses:
            return
        h = self._hypotheses[hypothesis_id]
        h.status = "validated" if result["passed"] else "falsified"
        h.actual_result = result.get("effect_size", 0)

        k_id = h.source_knowledge_id
        if k_id in self._knowledge:
            node = self._knowledge[k_id]
            if result["passed"]:
                node.success_count += 1
                node.confidence = min(0.99, node.confidence + 0.05)
            else:
                node.failure_count += 1
                node.confidence = max(0.1, node.confidence - 0.1)
            node.last_validated = datetime.now().isoformat()
            self._save_knowledge(node)
        self._save_hypothesis(h)

    def _infer_tags(self, concept: str, domain: str) -> List[str]:
        tags = [domain]
        text = concept.lower()
        for ind, keywords in self.INDUSTRY_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    tags.append(ind)
        return list(set(tags))

    def _industry_similarity(self, domain_a: str, domain_b: str) -> float:
        if domain_a == domain_b:
            return 1.0
        if domain_a == "通用" or domain_b == "通用":
            return 0.6
        similar_groups = [
            {"电商", "零售", "本地生活"},
            {"金融", "保险", "支付"},
            {"内容", "教育", "社区"},
            {"SaaS", "企业软件"},
        ]
        for group in similar_groups:
            if domain_a in group and domain_b in group:
                return 0.7
        return 0.1

    def _keyword_similarity(self, tags: List[str], keywords: List[str]) -> float:
        if not tags or not keywords:
            return 0.2
        tag_set = set(t.lower() for t in tags)
        kw_set = set(k.lower() for k in keywords)
        intersection = tag_set & kw_set
        union = tag_set | kw_set
        if not union:
            return 0.2
        return len(intersection) / len(union) * 0.5 + 0.2

    def _save_knowledge(self, node: KnowledgeNode):
        path = self.knowledge_path / f"{node.knowledge_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(asdict(node), f, allow_unicode=True, default_flow_style=False)

    def _save_scenario(self, scenario: ScenarioProfile):
        path = self.scenarios_path / f"{scenario.scenario_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(asdict(scenario), f, allow_unicode=True, default_flow_style=False)

    def _save_hypothesis(self, h: TransferHypothesis):
        path = self.hypotheses_path / f"{h.hypothesis_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(asdict(h), f, allow_unicode=True, default_flow_style=False)

    def _load_all(self):
        for path in self.knowledge_path.glob("*.yaml"):
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                self._knowledge[data["knowledge_id"]] = KnowledgeNode(**data)
            except Exception:
                continue
        for path in self.scenarios_path.glob("*.yaml"):
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                self._scenarios[data["scenario_id"]] = ScenarioProfile(**data)
            except Exception:
                continue
        for path in self.hypotheses_path.glob("*.yaml"):
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                self._hypotheses[data["hypothesis_id"]] = TransferHypothesis(**data)
            except Exception:
                continue

    def get_transfer_report(self) -> Dict[str, Any]:
        validated = [h for h in self._hypotheses.values() if h.status == "validated"]
        falsified = [h for h in self._hypotheses.values() if h.status == "falsified"]
        return {
            "total_knowledge": len(self._knowledge),
            "total_scenarios": len(self._scenarios),
            "total_hypotheses": len(self._hypotheses),
            "validated": len(validated),
            "falsified": len(falsified),
            "pending": sum(1 for h in self._hypotheses.values() if h.status == "pending"),
            "top_knowledge": sorted(
                [(k.concept, round(k.confidence, 3), k.validation_count)
                 for k in self._knowledge.values()],
                key=lambda x: x[1], reverse=True
            )[:10],
        }
