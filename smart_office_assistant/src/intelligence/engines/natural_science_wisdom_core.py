"""自然科学核心模块(物理 / 化学)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

__all__ = [
    'analyze',
    'get_evidence_for_claim',
    'get_frontier_problems',
    'query',
]

class NaturalScienceWisdomCore:
    """面向物理,化学,量子,热力学,相对论,粒子物理的轻量知识核心."""

    VERSION = "6.2.0"

    def __init__(self) -> None:
        self._knowledge_base: Dict[str, Dict[str, Any]] = {
            "quantum_entanglement": {
                "domain": "quantum",
                "title": "量子纠缠",
                "summary": "纠缠态意味着多个粒子的量子态不能拆成彼此独立的乘积态,相关性超出经典局域隐变量模型.",
                "mechanisms": ["贝尔不等式违背", "测量关联", "退相干限制"],
                "keywords": ["量子", "纠缠", "叠加", "贝尔", "量子信息"],
                "sources": ["量子力学", "量子信息科学"],
                "evidence": ["贝尔实验持续支持非经典相关性", "量子通信与量子计算实验可重复利用纠缠资源"],
                "related_concepts": ["量子态", "退相干", "量子通信"],
            },
            "thermodynamics_entropy": {
                "domain": "thermodynamics",
                "title": "热力学与熵",
                "summary": "熵衡量系统可实现微观状态数,第二定律说明孤立系统总熵倾向增加,宏观不可逆性由此出现.",
                "mechanisms": ["统计分布", "能量耗散", "不可逆过程"],
                "keywords": ["热力学", "熵", "温度", "平衡", "能量", "不可逆"],
                "sources": ["统计物理", "经典热力学"],
                "evidence": ["热机效率受卡诺极限约束", "扩散与热传导过程体现熵增方向"],
                "related_concepts": ["自由能", "平衡态", "卡诺循环"],
            },
            "relativity_spacetime": {
                "domain": "relativity",
                "title": "相对论时空",
                "summary": "狭义相对论unified时空与光速不变,广义相对论把引力描述为时空几何弯曲.",
                "mechanisms": ["洛伦兹变换", "时空曲率", "等效原理"],
                "keywords": ["相对论", "时空", "引力", "光速", "黑洞", "广义相对论"],
                "sources": ["狭义相对论", "广义相对论"],
                "evidence": ["GPS 必须校正相对论效应", "引力透镜与引力波观测持续验证理论"],
                "related_concepts": ["引力波", "黑洞", "宇宙学"],
            },
            "particle_standard_model": {
                "domain": "particle",
                "title": "粒子物理标准模型",
                "summary": "标准模型unified描述夸克,轻子及三种规范相互作用,并以希格斯机制解释部分粒子质量来源.",
                "mechanisms": ["规范对称性", "自发对称性破缺", "场量子化"],
                "keywords": ["粒子", "夸克", "轻子", "希格斯", "标准模型", "中微子"],
                "sources": ["量子场论", "高能物理"],
                "evidence": ["大型强子对撞机发现希格斯玻色子", "高能散射实验与标准模型预言高度一致"],
                "related_concepts": ["希格斯机制", "中微子振荡", "大unified理论"],
            },
            "chemical_bonding": {
                "domain": "chemistry",
                "title": "化学键与分子结构",
                "summary": "化学键是电子分布重构后的稳定结果,决定分子的几何结构,反应活性与物质性质.",
                "mechanisms": ["共价与离子成键", "轨道杂化", "分子轨道重叠"],
                "keywords": ["化学", "化学键", "分子", "轨道", "元素", "周期表"],
                "sources": ["量子化学", "结构化学"],
                "evidence": ["光谱学与晶体学可直接支持分子结构judge", "反应热与键能数据互相印证"],
                "related_concepts": ["催化", "反应路径", "电子云"],
            },
            "catalysis_reaction": {
                "domain": "chemistry",
                "title": "催化与反应路径",
                "summary": "催化剂通过改变反应路径降低活化能,不改变平衡常数,但显著加快达到平衡的速度.",
                "mechanisms": ["活化能降低", "过渡态稳定", "表面吸附与解吸"],
                "keywords": ["催化", "反应", "活化能", "表面", "工业化学"],
                "sources": ["物理化学", "催化化学"],
                "evidence": ["工业哈柏法与汽车尾气净化都依赖催化机制", "动力学实验可测得催化前后速率差异"],
                "related_concepts": ["反应速率", "平衡常数", "表面化学"],
            },
        }

        self._domain_labels = {
            "physics": "物理学",
            "chemistry": "化学",
            "quantum": "量子物理",
            "thermodynamics": "热力学",
            "relativity": "相对论",
            "particle": "粒子物理",
        }

        self._frontier_problems = {
            "physics": ["量子引力的可检验理论形式", "暗物质的微观本质"],
            "chemistry": ["高选择性绿色催化的unified设计原则", "复杂体系反应网络的可解释建模"],
            "quantum": ["大规模容错量子计算", "退相干抑制与量子纠错的工程极限"],
            "thermodynamics": ["非平衡统计物理的unified框架", "生命体系中的熵流与信息流耦合"],
            "relativity": ["黑洞信息悖论的完备答案", "广义相对论与量子理论unified"],
            "particle": ["中微子质量起源", "物质-反物质不对称机制"],
        }

    def query(self, question: str, domain: Optional[str] = None) -> Dict[str, Any]:
        matched = self._rank_concepts(question, domain)
        if not matched:
            label = self._domain_labels.get(domain or "physics", "自然科学")
            return {
                "answer": f"当前物理/化学核心中未直接命中 '{question}' 的条目,但它更可能属于{label}问题.",
                "domain": domain or "physics",
                "confidence": 0.35,
                "sources": ["自然科学核心内置知识库"],
                "related_concepts": [],
            }

        best_key = matched[0]
        item = self._knowledge_base[best_key]
        answer = (
            f"{item['title']}:{item['summary']} "
            f"关键机制包括{','.join(item['mechanisms'][:3])}."
        )
        return {
            "answer": answer,
            "domain": domain or item["domain"],
            "confidence": min(0.55 + 0.1 * len(matched), 0.9),
            "sources": item["sources"],
            "related_concepts": item["related_concepts"],
        }

    def analyze(self, topic: str, depth: str = "standard") -> Dict[str, Any]:
        matched = self._rank_concepts(topic)
        focus = [self._knowledge_base[key] for key in matched[:3]] or [self._knowledge_base["thermodynamics_entropy"]]

        detail_map = {
            "basic": 1,
            "standard": 2,
            "deep": 3,
        }
        detail_level = detail_map.get(depth, 2)

        core_mechanisms: List[str] = []
        related: List[str] = []
        for item in focus:
            core_mechanisms.extend(item["mechanisms"][:detail_level])
            related.extend(item["related_concepts"][:detail_level])

        domains = sorted({item["domain"] for item in focus})
        return {
            "topic": topic,
            "depth": depth,
            "summary": ";".join(item["summary"] for item in focus),
            "core_mechanisms": core_mechanisms,
            "related_concepts": list(dict.fromkeys(related)),
            "domain_focus": domains,
            "frontier_questions": self.get_frontier_problems(domains[0] if len(domains) == 1 else None),
            "practical_meaning": [
                "把抽象物理量转成机制解释,而不只给概念定义",
                "为跨学科调度提供物理/化学侧证据入口",
            ],
            "confidence": min(0.6 + 0.08 * len(focus), 0.92),
        }

    def get_frontier_problems(self, domain: Optional[str] = None) -> Dict[str, Any]:
        if domain:
            return {"domain": domain, "problems": self._frontier_problems.get(domain, [])}
        return {"domain": "physics_chemistry", "problems": self._frontier_problems}

    def get_evidence_for_claim(self, claim: str) -> Dict[str, Any]:
        matched = self._rank_concepts(claim)
        if not matched:
            return {
                "claim": claim,
                "supported": False,
                "confidence": 0.25,
                "domain": "physics",
                "evidence_points": ["当前物理/化学核心知识库未检索到直接支持项"],
                "sources": [],
            }

        best = self._knowledge_base[matched[0]]
        return {
            "claim": claim,
            "supported": True,
            "confidence": 0.72,
            "domain": best["domain"],
            "evidence_points": best["evidence"],
            "sources": best["sources"],
            "related_concepts": best["related_concepts"],
        }

    def _rank_concepts(self, text: str, domain: Optional[str] = None) -> List[str]:
        text_lower = text.lower()
        scores: Dict[str, int] = {}

        for key, item in self._knowledge_base.items():
            score = 0
            if domain and item["domain"] == domain:
                score += 2
            for keyword in item["keywords"]:
                if keyword.lower() in text_lower:
                    score += 1
            if score:
                scores[key] = score

        return [key for key, _ in sorted(scores.items(), key=lambda pair: pair[1], reverse=True)]
