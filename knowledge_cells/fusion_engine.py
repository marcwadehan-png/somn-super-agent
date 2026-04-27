"""
知识融合器 v1.0
==============
整合多个格子的知识，生成综合回答

功能：
- 多格子知识融合
- 举一反三自动触发
- 框架推荐
- 方法论自动注入

来源：基于legacy格子系统设计
"""

from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
import re


@dataclass
class KnowledgeFragment:
    """知识碎片"""
    cell_id: str
    cell_name: str
    content: str
    weight: float
    source_type: str  # "core" / "domain"


@dataclass
class FusionResult:
    """融合结果"""
    answer: str
    cells_used: List[str]
    frameworks: List[str]
    analogies: List[str]
    data_points: List[str]
    quality_score: float


class KnowledgeFusion:
    """知识融合器"""
    
    # 框架关键词映射
    FRAMEWORK_KEYWORDS = {
        "AARRR": ["获取", "激活", "留存", "变现", "推荐"],
        "SWOT": ["优势", "劣势", "机会", "威胁"],
        "4P": ["产品", "价格", "渠道", "促销"],
        "用户旅程": ["认知", "考虑", "购买", "使用", "忠诚"],
        "漏斗": ["转化", "流失", "优化", "提升"],
    }
    
    # 数据关键词
    DATA_KEYWORDS = ["数据", "显示", "表明", "统计", "指标", "比例", "%", "率"]
    
    # 类比触发词
    ANALOGY_TRIGGERS = ["就像", "如同", "相当于", "比如", "像", "类似"]
    
    def __init__(self, engine=None):
        self.engine = engine
    
    def set_engine(self, engine):
        """设置知识格子引擎"""
        self.engine = engine
    
    def find_relevant_cells(self, query: str) -> List[Tuple[str, float]]:
        """查找相关格子"""
        if not self.engine:
            return []
        
        query_lower = query.lower()
        results = []
        
        # 按内容搜索（使用完整查询和关键词）
        keywords = self._extract_keywords(query_lower)
        
        # 首先尝试完整查询
        content_results = self.engine.search_by_content(query)
        for cell in content_results:
            results.append((cell.cell_id, 0.9))
        
        # 然后使用关键词搜索
        for kw in keywords:
            if len(kw) >= 2:  # 忽略单字符
                kw_results = self.engine.search_by_content(kw)
                for cell in kw_results:
                    if cell.cell_id not in [r[0] for r in results]:
                        results.append((cell.cell_id, 0.7))
        
        # 按标签搜索
        tag_results = self.engine.search_by_tags(keywords)
        for cell in tag_results:
            if cell.cell_id not in [r[0] for r in results]:
                results.append((cell.cell_id, 0.6))
        
        return results
    
    def _extract_keywords(self, query: str) -> Set[str]:
        """提取关键词"""
        keywords = set()
        
        # 首先提取连续的中文词组
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', query)
        keywords.update(words)
        
        # 如果词组太少或太长，使用 n-gram 补充短词
        if len(words) == 0 or all(len(w) > 4 for w in words):
            # 提取 2-4 字的子串
            for length in range(2, min(5, len(query) + 1)):
                for i in range(len(query) - length + 1):
                    substr = query[i:i+length]
                    if re.match(r'^[\u4e00-\u9fa5]+$', substr):
                        keywords.add(substr)
        
        # 限制关键词数量
        if len(keywords) > 15:
            # 优先选择较短的词
            keywords = set(sorted(keywords, key=len)[:15])
        
        return keywords
    
    def get_cell_knowledge(self, cell_id: str) -> Optional[KnowledgeFragment]:
        """获取格子知识"""
        if not self.engine:
            return None
        
        cell = self.engine.get_cell(cell_id)
        if not cell:
            return None
        
        content = []
        if "what" in cell.content:
            content.append(f"【{cell.name}】{cell.content['what']}")
        if "points" in cell.content:
            content.append(cell.content['points'])
        
        return KnowledgeFragment(
            cell_id=cell.cell_id,
            cell_name=cell.name,
            content="\n".join(content),
            weight=cell.associations.get(cell.name, 0.5),
            source_type="core" if cell_id.startswith("A") else "domain"
        )
    
    def get_analogy(self, cell_id: str) -> Optional[str]:
        """获取举一反三"""
        if not self.engine:
            return None
        return self.engine.get_analogy(cell_id)
    
    def recommend_frameworks(self, query: str, cells_used: List[str]) -> List[str]:
        """推荐框架"""
        frameworks = []
        query_lower = query.lower()
        
        for fw, keywords in self.FRAMEWORK_KEYWORDS.items():
            if any(kw in query_lower for kw in keywords):
                frameworks.append(fw)
        
        cell_ids = set(cells_used)
        if {"B1", "B2", "B3"}.intersection(cell_ids):
            frameworks.append("AARRR")
        if {"C2", "B9"}.intersection(cell_ids):
            frameworks.append("漏斗分析")
        if {"B6", "C4"}.intersection(cell_ids):
            frameworks.append("4P")
        
        return list(set(frameworks))
    
    def extract_data_points(self, text: str) -> List[str]:
        """提取数据点"""
        data_points = []
        percentages = re.findall(r'[\d.]+%', text)
        data_points.extend(percentages)
        ratios = re.findall(r'[\d.]+(?:倍|次|人|个|元)', text)
        data_points.extend(ratios)
        return list(set(data_points))
    
    def extract_analogies(self, cells_used: List[str]) -> List[str]:
        """提取类比"""
        analogies = []
        for cell_id in cells_used:
            analogy = self.get_analogy(cell_id)
            if analogy:
                analogies.append(analogy)
        return analogies
    
    def fuse(self, query: str, context: str = "") -> FusionResult:
        """融合知识生成回答"""
        relevant_cells = self.find_relevant_cells(query)
        
        if not relevant_cells:
            return FusionResult(
                answer="未找到相关知识库内容，请提供更多背景信息。",
                cells_used=[],
                frameworks=[],
                analogies=[],
                data_points=[],
                quality_score=0
            )
        
        fragments = []
        cells_used = []
        for cell_id, weight in relevant_cells[:5]:
            fragment = self.get_cell_knowledge(cell_id)
            if fragment:
                fragments.append(fragment)
                cells_used.append(cell_id)
        
        analogies = self.extract_analogies(cells_used)
        frameworks = self.recommend_frameworks(query, cells_used)
        
        answer_parts = []
        
        if fragments:
            answer_parts.append("【知识整合】")
            for f in fragments[:3]:
                answer_parts.append(f"- {f.cell_name}: {f.content[:100]}...")
            answer_parts.append("")
        
        if frameworks:
            answer_parts.append("【建议框架】")
            answer_parts.append(f"推荐使用: {', '.join(frameworks)}")
            answer_parts.append("")
        
        if analogies:
            answer_parts.append("【举一反三】")
            for a in analogies[:2]:
                answer_parts.append(f"- {a}")
            answer_parts.append("")
        
        quality = 60
        quality += 10 if fragments else 0
        quality += 10 if frameworks else 0
        quality += 10 if analogies else 0
        quality += 10 if self.extract_data_points(" ".join(f.content for f in fragments)) else 0
        
        return FusionResult(
            answer="\n".join(answer_parts),
            cells_used=cells_used,
            frameworks=frameworks,
            analogies=analogies,
            data_points=self.extract_data_points(" ".join(f.content for f in fragments)),
            quality_score=min(quality, 100)
        )


_fusion: Optional[KnowledgeFusion] = None

def get_fusion_engine(engine=None) -> KnowledgeFusion:
    """获取融合引擎"""
    global _fusion
    if _fusion is None:
        _fusion = KnowledgeFusion(engine)
    elif engine:
        _fusion.set_engine(engine)
    return _fusion


if __name__ == "__main__":
    from cell_engine import get_knowledge_engine
    
    engine = get_knowledge_engine()
    fusion = get_fusion_engine(engine)
    
    result = fusion.fuse("如何提升用户增长")
    print("回答质量:", result.quality_score)
    print("使用格子:", result.cells_used)
    print("推荐框架:", result.frameworks)
    print("\n" + result.answer)
