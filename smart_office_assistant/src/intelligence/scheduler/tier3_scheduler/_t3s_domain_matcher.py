# -*- coding: utf-8 -*-
"""
__all__ = [
    'domains_overlap',
    'extract_domains',
    'get_domain_keywords',
    'match_engine',
]

Tier3 调度器 - 领域匹配模块
处理领域识别和引擎匹配
"""

from typing import Dict, List, Any, Tuple, Set
import re

# 领域关键词映射
DOMAIN_KEYWORDS = {
    "strategy": ["strategy", "战略", "策略", "规划", "计划"],
    "marketing": ["marketing", "营销", "推广", "品牌", "市场"],
    "product": ["product", "产品", "功能", "设计", "用户体验"],
    "operation": ["operation", "运营", "流程", "效率", "管理"],
    "finance": ["finance", "财务", "投资", "成本", "收益"],
    "technology": ["technology", "技术", "架构", "系统", "开发"],
    "team": ["team", "团队", "组织", "人才", "协作"],
    "growth": ["growth", "增长", "扩张", "规模", "发展"],
    "wisdom": ["wisdom", "智慧", "哲学", "思想", "文化"],
    "consulting": ["consulting", "咨询", "诊断", "建议", "方案"],
}

# 中文关键词到英文引擎域的映射
DOMAIN_KEYWORD_TO_ENG = {
    "战略": "strategy",
    "策略": "strategy",
    "营销": "marketing",
    "品牌": "marketing",
    "市场": "marketing",
    "产品": "product",
    "技术": "technology",
    "团队": "team",
    "增长": "growth",
    "智慧": "wisdom",
    "哲学": "wisdom",
    "咨询": "consulting",
    "运营": "operation",
    "财务": "finance",
    "投资": "finance",
}

class DomainMatcher:
    """领域匹配器"""

    def __init__(self):
        self.domain_keywords = DOMAIN_KEYWORDS
        self.keyword_to_eng = DOMAIN_KEYWORD_TO_ENG

    def extract_domains(self, query_text: str) -> Dict[str, float]:
        """从查询文本中提取领域及其权重"""
        domains = {}
        query_lower = query_text.lower()

        for domain, keywords in self.domain_keywords.items():
            score = 0.0
            for keyword in keywords:
                count = query_lower.count(keyword.lower())
                if count > 0:
                    score += count * (1.0 if len(keyword) > 4 else 0.5)

            if score > 0:
                domains[domain] = min(1.0, score)

        # 如果没有识别到领域，默认使用通用领域
        if not domains:
            domains["general"] = 0.5

        return domains

    def match_engine(
        self,
        engine_id: str,
        domains: Dict[str, float],
        engine_pool: Dict[str, Any]
    ) -> Tuple[float, List[str]]:
        """
        匹配引擎与领域

        Returns:
            (匹配分数, 匹配到的领域列表)
        """
        engine_info = engine_pool.get(engine_id, {})
        engine_domains = self._get_engine_domains(engine_id, engine_info)

        matched_domains = []
        total_score = 0.0

        for domain, weight in domains.items():
            # 中文关键词映射到英文
            eng_domain = self.keyword_to_eng.get(domain, domain)

            # 检查引擎是否支持该领域
            if eng_domain in engine_domains:
                matched_domains.append(domain)
                total_score += weight
            elif domain in engine_domains:
                matched_domains.append(domain)
                total_score += weight
            else:
                # 部分匹配检查
                for ed in engine_domains:
                    if self._domain_similar(domain, ed):
                        matched_domains.append(domain)
                        total_score += weight * 0.5
                        break

        # 归一化分数
        if domains:
            final_score = total_score / len(domains)
        else:
            final_score = 0.0

        return min(1.0, final_score), matched_domains

    def _get_engine_domains(self, engine_id: str, engine_info: Any) -> Set[str]:
        """获取引擎支持的领域"""
        if isinstance(engine_info, dict):
            domains = engine_info.get("domains", [])
            if isinstance(domains, (list, tuple)):
                return set(d.lower() for d in domains)
        return set()

    def _domain_similar(self, domain1: str, domain2: str) -> bool:
        """检查两个领域是否相似"""
        d1 = domain1.lower()
        d2 = domain2.lower()

        # 直接包含
        if d1 in d2 or d2 in d1:
            return True

        # 关键词重叠
        keywords1 = set(self.domain_keywords.get(d1, []))
        keywords2 = set(self.domain_keywords.get(d2, []))

        if keywords1 and keywords2:
            overlap = keywords1 & keywords2
            if len(overlap) >= min(len(keywords1), len(keywords2)) * 0.3:
                return True

        return False

    def domains_overlap(self, domains1: Set[str], domains2: Set[str]) -> bool:
        """检查两组领域是否有重叠"""
        if not domains1 or not domains2:
            return False

        for d1 in domains1:
            for d2 in domains2:
                if self._domain_similar(d1, d2):
                    return True

        return False

    def get_domain_keywords(self, domain: str) -> List[str]:
        """获取领域的关键词列表"""
        return self.domain_keywords.get(domain.lower(), [])
