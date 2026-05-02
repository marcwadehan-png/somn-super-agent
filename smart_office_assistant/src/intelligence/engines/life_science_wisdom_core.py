"""生命科学核心模块."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

__all__ = [
    'analyze',
    'get_evidence_for_claim',
    'get_frontier_problems',
    'query',
]

class LifeScienceWisdomCore:
    """面向分子生物学,演化,生态,基因组学与神经科学的轻量知识核心."""

    VERSION = "6.2.0"

    def __init__(self) -> None:
        self._knowledge_base: Dict[str, Dict[str, Any]] = {
            "central_dogma": {
                "domain": "molecular_bio",
                "title": "中心法则",
                "summary": "遗传信息通常沿 DNA -> RNA -> 蛋白质 的方向流动,转录与翻译构成生命表达的基础流程.",
                "mechanisms": ["DNA 复制", "RNA 转录", "核糖体翻译"],
                "keywords": ["DNA", "RNA", "蛋白质", "转录", "翻译", "中心法则", "细胞"],
                "sources": ["分子生物学", "细胞生物学"],
                "evidence": ["分子实验可直接测定转录与翻译产物", "遗传突变与蛋白表达变化存在稳定对应关系"],
                "related_concepts": ["基因表达", "突变", "表观遗传"],
            },
            "genomics_regulation": {
                "domain": "genomics",
                "title": "基因组与调控网络",
                "summary": "基因组不只是编码序列集合,更包含调控元件,染色质结构与细胞状态切换逻辑.",
                "mechanisms": ["增强子调控", "染色质开放性", "转录因子网络"],
                "keywords": ["基因组", "基因", "调控", "表观遗传", "测序", "染色质"],
                "sources": ["基因组学", "系统生物学"],
                "evidence": ["高通量测序可以绘制调控图谱", "不同细胞类型共享基因组但表达程序不同"],
                "related_concepts": ["单细胞测序", "调控网络", "发育生物学"],
            },
            "evolution_selection": {
                "domain": "evolution",
                "title": "演化与自然选择",
                "summary": "演化来自变异,遗传与选择的叠加,适应并非朝着完美进化,而是局部环境下的筛选结果.",
                "mechanisms": ["随机变异", "自然选择", "遗传漂变"],
                "keywords": ["进化", "演化", "物种", "自然选择", "适应", "突变"],
                "sources": ["演化生物学", "群体遗传学"],
                "evidence": ["化石序列与分子钟共同支持谱系分化", "抗生素耐药演化是可观测的实时案例"],
                "related_concepts": ["适应度", "系统发育", "共演化"],
            },
            "ecology_resilience": {
                "domain": "ecology",
                "title": "生态系统韧性",
                "summary": "生态系统由物种网络,能量流动和环境扰动共同塑形,韧性取决于多样性,冗余与反馈结构.",
                "mechanisms": ["食物网反馈", "生态位分化", "扰动恢复"],
                "keywords": ["生态", "生态系统", "物种", "气候", "食物网", "韧性"],
                "sources": ["生态学", "复杂系统科学"],
                "evidence": ["生物多样性越高的系统通常恢复力更强", "营养级联现象能显著改写系统稳定性"],
                "related_concepts": ["生物多样性", "生态位", "系统韧性"],
            },
            "neuroscience_plasticity": {
                "domain": "neuroscience",
                "title": "神经可塑性",
                "summary": "神经系统会随经验,训练与损伤重组连接强度,可塑性是学习,记忆与康复的基础.",
                "mechanisms": ["突触可塑性", "长时程增强", "网络重组"],
                "keywords": ["神经", "大脑", "神经元", "突触", "意识", "学习", "记忆"],
                "sources": ["神经科学", "认知科学"],
                "evidence": ["电生理与成像实验持续支持可塑性变化", "康复训练能够驱动功能重mapping"],
                "related_concepts": ["记忆巩固", "脑网络", "意识"],
            },
        }

        self._frontier_problems = {
            "molecular_bio": ["生命起源前化学到自复制的关键跃迁", "多尺度细胞调控的unified模型"],
            "genomics": ["非编码区功能的系统解释", "复杂性状的全链路因果拆解"],
            "evolution": ["重大演化创新如何快速跃迁", "文化演化与生物演化的耦合机制"],
            "ecology": ["气候变化下生态系统临界转变预测", "多物种网络的稳定性边界"],
            "neuroscience": ["意识的可检验机制模型", "记忆存储与提取的精确编码规则"],
        }

    def query(self, question: str, domain: Optional[str] = None) -> Dict[str, Any]:
        matched = self._rank_concepts(question, domain)
        if not matched:
            return {
                "answer": f"生命科学核心中暂未直接命中 '{question}' 的条目,但它仍可按实验设计,机制链条和演化背景继续拆解.",
                "domain": domain or "molecular_bio",
                "confidence": 0.35,
                "sources": ["生命科学核心内置知识库"],
                "related_concepts": [],
            }

        best = self._knowledge_base[matched[0]]
        return {
            "answer": f"{best['title']}:{best['summary']} 关键机制包括{','.join(best['mechanisms'][:3])}.",
            "domain": domain or best["domain"],
            "confidence": min(0.58 + 0.08 * len(matched), 0.9),
            "sources": best["sources"],
            "related_concepts": best["related_concepts"],
        }

    def analyze(self, topic: str, depth: str = "standard") -> Dict[str, Any]:
        matched = self._rank_concepts(topic)
        focus = [self._knowledge_base[key] for key in matched[:3]] or [self._knowledge_base["central_dogma"]]
        detail_map = {"basic": 1, "standard": 2, "deep": 3}
        detail_level = detail_map.get(depth, 2)

        mechanisms: List[str] = []
        related: List[str] = []
        evidence: List[str] = []
        for item in focus:
            mechanisms.extend(item["mechanisms"][:detail_level])
            related.extend(item["related_concepts"][:detail_level])
            evidence.extend(item["evidence"][:detail_level])

        domains = sorted({item["domain"] for item in focus})
        return {
            "topic": topic,
            "depth": depth,
            "summary": ";".join(item["summary"] for item in focus),
            "domain_focus": domains,
            "core_mechanisms": mechanisms,
            "evidence_chain": evidence,
            "related_concepts": list(dict.fromkeys(related)),
            "frontier_questions": self.get_frontier_problems(domains[0] if len(domains) == 1 else None),
            "practical_meaning": [
                "把生命科学问题拆成机制层,系统层,演化层三层结构",
                "给unified调度器补上可落地的生命科学解释接口",
            ],
            "confidence": min(0.62 + 0.07 * len(focus), 0.92),
        }

    def get_frontier_problems(self, domain: Optional[str] = None) -> Dict[str, Any]:
        if domain:
            return {"domain": domain, "problems": self._frontier_problems.get(domain, [])}
        return {"domain": "life_science", "problems": self._frontier_problems}

    def get_evidence_for_claim(self, claim: str) -> Dict[str, Any]:
        matched = self._rank_concepts(claim)
        if not matched:
            return {
                "claim": claim,
                "supported": False,
                "confidence": 0.25,
                "domain": "life_science",
                "evidence_points": ["当前生命科学核心知识库未检索到直接支持项"],
                "sources": [],
            }

        best = self._knowledge_base[matched[0]]
        return {
            "claim": claim,
            "supported": True,
            "confidence": 0.74,
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
