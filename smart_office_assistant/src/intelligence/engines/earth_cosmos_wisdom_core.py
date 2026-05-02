"""地球与宇宙核心模块."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

__all__ = [
    'analyze',
    'get_evidence_for_claim',
    'get_frontier_problems',
    'query',
]

class EarthCosmosWisdomEngine:
    """面向地质学,大气科学,海洋学,宇宙学与天体物理的轻量知识核心."""

    VERSION = "6.2.0"

    def __init__(self) -> None:
        self._knowledge_base: Dict[str, Dict[str, Any]] = {
            "plate_tectonics": {
                "domain": "geology",
                "title": "板块构造",
                "summary": "岩石圈并非整体静止,而是由多个板块在软流圈之上缓慢运动,驱动山脉,地震与火山活动.",
                "mechanisms": ["地幔对流", "洋中脊扩张", "俯冲带循环"],
                "keywords": ["地质", "板块", "地震", "火山", "地幔", "岩浆", "地球"],
                "sources": ["地质学", "地球动力学"],
                "evidence": ["海底磁异常条带支持海底扩张", "全球地震与火山分布高度贴合板块边界"],
                "related_concepts": ["地球系统", "地震带", "俯冲"],
            },
            "atmospheric_circulation": {
                "domain": "atmosphere",
                "title": "大气环流",
                "summary": "太阳辐射不均与地球自转共同塑造大气环流,决定风带,降水带与极端天气的背景结构.",
                "mechanisms": ["辐射收支", "科里奥利力", "水汽输送"],
                "keywords": ["大气", "气候", "降水", "风", "温室效应", "天气", "台风"],
                "sources": ["大气科学", "气候动力学"],
                "evidence": ["再分析资料持续验证哈德莱环流和急流结构", "温室气体增加改变能量平衡与极端事件概率"],
                "related_concepts": ["气候变化", "急流", "季风"],
            },
            "ocean_circulation": {
                "domain": "oceanography",
                "title": "海洋环流",
                "summary": "海洋通过风生环流与温盐环流在全球重新分配热量,盐度与碳,直接影响区域气候与生态.",
                "mechanisms": ["风应力驱动", "热盐差异", "上升流与下沉流"],
                "keywords": ["海洋", "洋流", "温盐", "厄尔尼诺", "海气", "潮汐"],
                "sources": ["海洋学", "海气相互作用"],
                "evidence": ["ARGO 浮标长期观测支持热含量变化分析", "ENSO 事件会系统性改写全球降水与温度分布"],
                "related_concepts": ["碳循环", "ENSO", "海气耦合"],
            },
            "cosmology_expansion": {
                "domain": "cosmology",
                "title": "宇宙膨胀与 ΛCDM",
                "summary": "现代宇宙学以 ΛCDM 模型解释宇宙从热大爆炸演化到大尺度结构形成的主线过程.",
                "mechanisms": ["宇宙膨胀", "暗物质引力坍缩", "暗能量驱动加速膨胀"],
                "keywords": ["宇宙", "大爆炸", "膨胀", "暗物质", "暗能量", "哈勃", "宇宙学"],
                "sources": ["观测宇宙学", "理论宇宙学"],
                "evidence": ["宇宙微波背景和重子声学振荡共同支持标准宇宙学框架", "超新星观测支持宇宙加速膨胀"],
                "related_concepts": ["哈勃张力", "宇宙微波背景", "结构形成"],
            },
            "stellar_blackhole": {
                "domain": "astrophysics",
                "title": "恒星演化与黑洞",
                "summary": "恒星质量决定其寿命与终态,高质量恒星可能经历超新星爆发并留下中子星或黑洞.",
                "mechanisms": ["核聚变", "引力坍缩", "辐射压平衡"],
                "keywords": ["恒星", "黑洞", "超新星", "星系", "天体物理", "中子星", "引力波"],
                "sources": ["恒星物理", "高能天体物理"],
                "evidence": ["LIGO 的引力波事件直接支持致密天体并合", "黑洞阴影观测增强了强引力场证据链"],
                "related_concepts": ["引力波", "核合成", "活动星系核"],
            },
        }

        self._frontier_problems = {
            "geology": ["早期板块构造何时启动", "深部地幔过程如何精准约束地表演化"],
            "atmosphere": ["极端天气变化的区域归因", "云反馈对气候敏感度的真实贡献"],
            "oceanography": ["深海热量与碳汇变化的长期边界", "海洋环流临界转变预警"],
            "cosmology": ["哈勃张力是否指向新物理", "暗能量是否随时间演化"],
            "astrophysics": ["超大质量黑洞早期形成机制", "致密天体并合后的物质状态方程"],
        }

    def query(self, question: str, domain: Optional[str] = None) -> Dict[str, Any]:
        matched = self._rank_concepts(question, domain)
        if not matched:
            return {
                "answer": f"地球与宇宙核心中暂未直接命中 '{question}' 的条目,但它很可能需要从系统过程,时空尺度和观测证据三层继续拆解.",
                "domain": domain or "geology",
                "confidence": 0.35,
                "sources": ["地球与宇宙核心内置知识库"],
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
        focus = [self._knowledge_base[key] for key in matched[:3]] or [self._knowledge_base["plate_tectonics"]]
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
                "把地球系统与宇宙学问题unified到可观测证据链上",
                "为调度器提供行星尺度到宇宙尺度的结构化回答入口",
            ],
            "confidence": min(0.62 + 0.07 * len(focus), 0.92),
        }

    def get_frontier_problems(self, domain: Optional[str] = None) -> Dict[str, Any]:
        if domain:
            return {"domain": domain, "problems": self._frontier_problems.get(domain, [])}
        return {"domain": "earth_cosmos", "problems": self._frontier_problems}

    def get_evidence_for_claim(self, claim: str) -> Dict[str, Any]:
        matched = self._rank_concepts(claim)
        if not matched:
            return {
                "claim": claim,
                "supported": False,
                "confidence": 0.25,
                "domain": "earth_cosmos",
                "evidence_points": ["当前地球与宇宙核心知识库未检索到直接支持项"],
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
