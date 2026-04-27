# -*- coding: utf-8 -*-
"""
智慧记忆增强系统 v5.5.0
Wisdom Memory Enhancement System

融入儒家十经,素书,道德经等经典语录的智能记忆编码系统
fusion神经科学原理,增强记忆的深度与持久性

版本: v5.5.0
日期: 2026-04-02
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import re

# 懒加载数据
from ._wisdom_data import get_quotes_data, get_wisdom_graph_data

class WisdomCategory(Enum):
    """智慧类别"""
    # 儒家五常
    REN = "仁"          # 仁爱
    YI = "义"          # 适宜
    LI = "礼"          # 秩序
    ZHI = "智"         # 明智
    XIN = "信"         # 诚信
    
    # 素书五德
    DAO = "道"          # 规律
    DE = "德"          # 品行
    REN_SUFU = "仁"     # 仁爱
    YI_SUFU = "义"      # 适宜
    LI_SUFU = "礼"      # 规范
    
    # 道家
    ZIRAN = "自然"      # 道法自然
    WUWEI = "无为"      # 无为而治
    
    # 佛家
    KONG = "空"         # 缘起性空
    HUI = "慧"          # 般若智慧
    
    # 兵法
    ZHENG = "正"        # 正面
    QI = "奇"           # 出奇制胜
    
    # 成长
    GROWTH = "成长"     # 成长型思维
    LOOP = "闭环"       # 闭环迭代

@dataclass
class WisdomQuote:
    """智慧语录"""
    text: str
    source: str              # 来源经典
    category: WisdomCategory
    meaning: str             # 现代解读
    application: str          # 应用场景
    keywords: List[str]

@dataclass
class MemoryNode:
    """记忆节点"""
    id: str
    content: str
    encoding_type: str
    wisdom_tags: List[WisdomCategory]
    classical_associations: List[str]
    neural_priming: float     # 神经激活潜能
    memory_strength: float    # 记忆强度
    last_accessed: datetime
    access_count: int = 0

class WisdomMemoryEncoder:
    """
    智慧记忆编码器
    
    功能:
    1. 将智慧语录编码为可检索记忆
    2. 建立经典与现代的关联mapping
    3. 神经科学增强的记忆巩固
    4. 多维度智慧检索
    """
    
    def __init__(self):
        self.quotes_database = self._build_quotes_database()
        self.memory_index: Dict[str, MemoryNode] = {}
        self.wisdom_graph = self._build_wisdom_graph()
    
    def _build_quotes_database(self) -> Dict[str, List[WisdomQuote]]:
        """构建智慧语录数据库（懒加载）"""
        raw_data = get_quotes_data()
        result = {}
        for category, quotes in raw_data.items():
            result[category] = []
            for q in quotes:
                # 转换category字符串到枚举
                cat_val = q.get("category", "ZHI")
                if isinstance(cat_val, str):
                    try:
                        cat_val = WisdomCategory[cat_val]
                    except KeyError:
                        cat_val = WisdomCategory.ZHI
                q["category"] = cat_val
                result[category].append(WisdomQuote(**q))
        return result
    
    def _build_wisdom_graph(self) -> Dict[WisdomCategory, List[WisdomCategory]]:
        """构建智慧关联图谱（懒加载）"""
        return get_wisdom_graph_data()
    
    def encode_wisdom(self, quote: WisdomQuote) -> MemoryNode:
        """编码智慧语录"""
        node_id = hashlib.md5(
            f"{quote.text}{quote.source}".encode()
        ).hexdigest()[:12]
        
        # 计算神经激活潜能(基于语义的丰富度)
        neural_priming = len(quote.keywords) * 0.1 + 0.5
        
        node = MemoryNode(
            id=node_id,
            content=f"{quote.text}\n--{quote.source}",
            encoding_type="wisdom_classical",
            wisdom_tags=[quote.category],
            classical_associations=[quote.source],
            neural_priming=neural_priming,
            memory_strength=0.9,  # 经典语录初始强度高
            last_accessed=datetime.now(),
            access_count=1
        )
        
        self.memory_index[node_id] = node
        return node
    
    def retrieve_wisdom(
        self, 
        query: str, 
        category: Optional[WisdomCategory] = None,
        top_k: int = 5
    ) -> List[MemoryNode]:
        """检索智慧语录"""
        results = []
        
        query_lower = query.lower()
        query_keywords = set(query_lower.split())
        
        for node in self.memory_index.values():
            score = 0.0
            
            # 关键词匹配
            for kw in query_keywords:
                if kw in node.content.lower():
                    score += 0.3
            
            # 类别匹配
            if category and category in node.wisdom_tags:
                score += 0.5
            
            # 标签匹配
            for tag in node.wisdom_tags:
                if tag.value in query_lower:
                    score += 0.3
            
            if score > 0:
                results.append((node, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:top_k]]
    
    def get_related_wisdom(
        self, category: WisdomCategory, depth: int = 1
    ) -> List[WisdomCategory]:
        """get关联智慧"""
        related = set()
        current = {category}
        
        for _ in range(depth):
            next_level = set()
            for cat in current:
                if cat in self.wisdom_graph:
                    next_level.update(self.wisdom_graph[cat])
            related.update(next_level)
            current = next_level
        
        return list(related)
    
    def get_random_wisdom(self, category: Optional[WisdomCategory] = None) -> WisdomQuote:
        """get随机智慧语录"""
        all_quotes = []
        
        for quotes in self.quotes_database.values():
            if category:
                all_quotes.extend([q for q in quotes if q.category == category])
            else:
                all_quotes.extend(quotes)
        
        return all_quotes[hashlib.md5(
            str(datetime.now()).encode()
        ).hexdigest()[0:4], 16 % len(all_quotes)]
    
    def build_all_index(self):
        """构建全部语录索引"""
        count = 0
        for quotes in self.quotes_database.values():
            for quote in quotes:
                self.encode_wisdom(quote)
                count += 1
        return count
    
    def get_statistics(self) -> Dict[str, Any]:
        """get统计信息"""
        by_source = {}
        by_category = {}
        
        for quotes in self.quotes_database.values():
            source = quotes[0].source.split("·")[0] if quotes else ""
            by_source[source] = len(quotes)
            
            for q in quotes:
                cat = q.category.value
                by_category[cat] = by_category.get(cat, 0) + 1
        
        return {
            "total_quotes": sum(len(v) for v in self.quotes_database.values()),
            "sources": len(self.quotes_database),
            "by_source": by_source,
            "by_category": by_category,
            "indexed_nodes": len(self.memory_index)
        }

def quick_retrieve(query: str, top_k: int = 3) -> str:
    """
    快速检索智慧语录
    
    用法:
    >>> quick_retrieve("如何培养人才")
    """
    encoder = WisdomMemoryEncoder()
    encoder.build_all_index()
    
    results = encoder.retrieve_wisdom(query, top_k=top_k)
    
    if not results:
        return "未找到相关智慧语录"
    
    output = ["📚 智慧语录检索结果:\n"]
    for i, node in enumerate(results, 1):
        output.append(f"{i}. {node.content}")
        output.append(f"   标签: {[t.value for t in node.wisdom_tags]}\n")
    
    return "\n".join(output)

def daily_wisdom(category: Optional[str] = None) -> str:
    """
    get每日智慧
    
    用法:
    >>> daily_wisdom("仁")
    """
    encoder = WisdomMemoryEncoder()
    encoder.build_all_index()
    
    cat = None
    if category:
        try:
            cat = WisdomCategory(category)
        except ValueError:
            pass
    
    import random
    quotes = []
    for q_list in encoder.quotes_database.values():
        if cat:
            quotes.extend([q for q in q_list if q.category == cat])
        else:
            quotes.extend(q_list)
    
    if not quotes:
        return "未找到相关语录"
    
    quote = random.choice(quotes)
    return f"""
🌅 每日智慧

"{quote.text}"
--{quote.source}

📖 解读: {quote.meaning}
💡 应用: {quote.application}
🏷️ 分类: {quote.category.value}
"""

# 导出
__all__ = [
    'WisdomMemoryEncoder',
    'WisdomQuote',
    'MemoryNode',
    'WisdomCategory',
    'quick_retrieve',
    'daily_wisdom'
]
