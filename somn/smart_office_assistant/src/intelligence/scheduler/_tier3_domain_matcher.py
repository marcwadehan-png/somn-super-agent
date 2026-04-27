# -*- coding: utf-8 -*-
"""
__all__ = [
    'extract_domains',
    'match_engine',
]

三级神经网络调度器 - 领域匹配模块
Tier-3 Neural Scheduler Domain Matcher
=======================================

领域匹配器，负责:
1. 从查询文本中提取问题域
2. 计算引擎与问题域的匹配分数
3. 扩展关键词关联

版本: v1.0
日期: 2026-04-06
"""

from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

class DomainMatcher:
    """领域匹配器"""

    def __init__(self, optimizer=None):
        # 延迟导入避免循环依赖
        from ._tier3_constants import DOMAIN_ENGINE_KEYWORDS, DOMAIN_KEYWORD_TO_ENG
        self.domain_keywords = DOMAIN_ENGINE_KEYWORDS
        self.keyword_to_eng = DOMAIN_KEYWORD_TO_ENG
        self.optimizer = optimizer

    def extract_domains(self, query_text: str) -> Dict[str, float]:
        """从查询文本中提取问题域,并接入优化器关键词扩展."""
        query_lower = query_text.lower()
        domains = defaultdict(float)

        for domain_key, engine_list in self.domain_keywords.items():
            if domain_key in query_lower:
                # 计算域权重(包含的关键词越多,权重越高)
                domains[domain_key] += 1.0

        if self.optimizer is not None:
            for keyword in self.optimizer.expansion_keywords.keys():
                if keyword in query_text:
                    domains[keyword] += 1.0

        # 语义标签二次提取
        semantic_domains = self._extract_semantic_tags(query_text)
        for sd in semantic_domains:
            domains[sd] += 0.5

        if self.optimizer is not None and domains:
            expanded_terms = self.optimizer.expand_keywords(list(domains.keys()))
            for term in expanded_terms:
                if term not in domains:
                    domains[term] += 0.35

        return dict(domains)

    def _extract_semantic_tags(self, query: str) -> List[str]:
        """提取语义标签"""
        tags = []
        query_lower = query.lower()

        # 延迟导入避免循环依赖
        from ._tier3_constants import SEMANTIC_TO_ENG_DOMAINS

        semantic_map = {
            "战略相关": ["战略", "strategy", "规划", "谋", "策"],
            "危机相关": ["危机", "风险", "危", "险", "亏损", "生死", "绝地", "翻盘", "困境"],
            "伦理相关": ["道德", "仁义", "善", "恶"],
            "人心相关": ["心态", "心理", "心", "情绪", "士气", "意志"],
            "成长相关": ["成长", "学习", "提升", "进步"],
            "文化相关": ["文化", "传统", "传承", "历史"],
            "自然相关": ["自然", "物理", "科学", "宇宙"],
            "市场相关": ["市场", "营销", "品牌", "用户"],
            "竞争相关": ["竞争", "博弈", "对手", "竞品", "竞对"],
            "管理相关": ["管理", "团队", "组织", "制度"],
        }

        for tag, keywords in semantic_map.items():
            if any(kw in query_lower for kw in keywords):
                tags.append(tag)

        return tags

    def _get_engine_domains(self, engine_id: str, candidates: Dict[str, Dict]) -> List[str]:
        """get增强后的引擎域标签."""
        engine_info = candidates.get(engine_id, {})
        if not engine_info:
            return []

        engine_domains = list(engine_info.get("domains", []))
        if self.optimizer is not None:
            engine_domains = self.optimizer.enhance_engine_domains(engine_id, engine_domains)
        return engine_domains

    def match_engine(self, engine_id: str, domains: Dict[str, float],
                     candidates: Dict[str, Dict]) -> Tuple[float, List[str]]:
        """计算引擎与问题域的匹配分数 - 支持中文→英文跨语言mapping"""
        engine_info = candidates.get(engine_id, {})
        if not engine_info:
            return 0.0, []

        engine_domains = self._get_engine_domains(engine_id, candidates)
        matched = []

        for domain_key in domains:
            # 路径A:中文关键词直接匹配英文域(substrings双方都试试)
            for ed in engine_domains:
                if domain_key in ed.lower() or ed.lower() in domain_key:
                    score = domains[domain_key]
                    matched.append((domain_key, score))
                    break

            # 路径B:中文关键词通过 DOMAIN_KEYWORD_TO_ENG mapping到英文,再匹配引擎域
            if not any(d == domain_key for d, _ in matched):
                eng_terms = self.keyword_to_eng.get(domain_key, [])
                for ed in engine_domains:
                    ed_lower = ed.lower()
                    if any(term in ed_lower for term in eng_terms):
                        score = domains[domain_key]
                        matched.append((domain_key, score))
                        break

        # 去重并归并分数
        domain_scores = defaultdict(float)
        for d, s in matched:
            domain_scores[d] = max(domain_scores[d], s)

        total_score = sum(domain_scores.values()) if domain_scores else 0.0
        # 归一化到 [0, 1]
        normalized_score = min(1.0, total_score / max(1.0, len(domains) * 0.5))

        return normalized_score, list(domain_scores.keys())
