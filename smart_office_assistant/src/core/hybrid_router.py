# -*- coding: utf-8 -*-
"""
__all__ = [
    'create_hybrid_router',
    'get_statistics',
    'route',
]

Somn 混合路由引擎 v1.0
Hybrid Router - 简单对话走 LLM 直答,专业分析走 Somn 智慧链路

设计原则:
- 不试图让 Somn 在所有场景都和豆包一样,而是在专业领域做到更深
- 简单对话 → LLM 直答(快速,自然)
- 专业分析 → Somn 智慧链路(深度,多学派fusion)
- 边界可配置,用户/系统可调整路由阈值

路由decision维度:
1. 问题复杂度(长度,实体数量,追问深度)
2. 话题领域(商业/哲学/日常/技术)
3. 用户历史偏好(学习型 vs 效率型)

版本: v1.0
日期: 2026-04-04
"""

import re
import json
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger

class RouteType(Enum):
    """路由类型"""
    LLM_DIRECT = "llm_direct"           # LLM 直答(简单对话,常识问题)
    SOMN_WISDOM = "somn_wisdom"         # Somn 智慧链路(论证型,哲学问题)
    SOMN_WORKFLOW = "somn_workflow"     # Somn 工作流(任务型,strategygenerate)
    CONVERSATIONAL = "conversational"   # 简单寒暄(直接回复)

@dataclass
class RouteDecision:
    """路由decision结果"""
    route_type: RouteType
    confidence: float                    # 路由置信度 0~1
    reasoning: str                       # decision理由
    complexity_score: float = 0.0        # 问题复杂度分数 0~1
    domain_score: float = 0.0            # 专业领域匹配度 0~1
    detail: Dict[str, Any] = field(default_factory=dict)

class HybridRouter:
    """
    混合路由器
    
    核心逻辑:
    - 简单问题(短,日常话题,无深度追问)→ LLM 直答
    - 论证型问题(哲学追问,观点探讨)→ Somn 智慧板块
    - 任务型问题(strategy,分析,generate)→ Somn 工作流
    - 寒暄/自我介绍 → 直接回复
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # ═══ 路由阈值(可调) ═══
        self.complexity_threshold = self.config.get("complexity_threshold", 0.35)
        self.domain_threshold = self.config.get("domain_threshold", 0.3)
        self.llm_direct_max_length = self.config.get("llm_direct_max_length", 25)
        
        # ═══ 对话型关键词(不需要任何智慧链路) ═══
        self.conversational_patterns = [
            r'^(你好|您好|hello|hi|hey|嗨|早安|晚安|下午好|早上好|晚上好)[\s!!..]*$',
            r'^(谢谢|感谢|多谢|thanks|thx)[\s!!..]*$',
            r'^(嗯|哦|好|ok|OK|行|好的|明白|了解了)[\s!!..]*$',
            r'^(你是谁|你叫什么|什么名字|介绍一下你)',
            r'^(再见|拜拜|bye|goodbye)[\s!!..]*$',
            r'^[??]$',
        ]
        
        # ═══ 专业领域词(高权重,偏向 Somn 链路) ═══
        self.somn_domain_words = {
            # 商业/增长(最高权重)
            "growth": [
                '增长', '转化', '留存', '获客', '漏斗', 'ROI', 'ROI', 'GMV', 'ARPU',
                '留存率', '复购', '私域', '公域', '裂变', '增长黑客', 'AARRR', 'LTV',
                '用户增长', '收入增长', '利润增长', '市场份额',
            ],
            # strategy/管理
            "strategy": [
                'strategy', '战略', '规划', '路径', '方案', '目标分解', '执行计划',
                '里程碑', '大秦指标', 'KPI', '北极星metrics', '护城河', '壁垒',
            ],
            # 营销/品牌
            "marketing": [
                '营销', '品牌', '定位', '传播', '广告', '推广', '内容营销',
                '社交媒体', '口碑', '粉丝', 'IP', 'KOL', 'KOC',
            ],
            # 产品/技术
            "tech": [
                '产品', '功能', '交互', '体验', '架构', '系统设计',
                '智能体', 'Agent', 'AI', '人工智能', '大模型', 'LLM',
            ],
            # 哲学/智慧(走智慧板块)
            "wisdom": [
                '意义', '人生', '存在', '价值', '幸福', '本质', '真理',
                '道德', '伦理', '灵魂', '自由', '命运', '善恶', '美丑',
                '道', '德', '仁', '义', '礼', '智', '信',
                '无为', '自然', '阴阳', '五行', '八卦',
                '佛', '禅', '空', '缘', '因果', '轮回',
                'xinxue', '良知', '知行合一', '致良知',
                # 学派/思想体系
                '儒家', '道家', '佛家', '法家', '墨家', '兵家', '名家',
                '素书', '论语', '孟子', '老子', '庄子', '孙子兵法',
                '朱熹', '王阳明', '辜鸿铭', '鲁迅', '胡适',
                # 哲学概念
                '思想', '文化', '文明', '传统', '哲学', '智慧',
                '宇宙', '意识', '认知', '理性', '感性',
                '自由意志', '决定论', '唯心', '唯物',
                '人文', '精神', '信仰', '宗教',
            ],
            # 行业/公司(走工作流)
            "industry": [
                '茅台', '五粮液', '腾讯', '阿里', '字节', '百度', '华为', '小米',
                '苹果', '谷歌', '微软', '亚马逊', '特斯拉', '比亚迪', '宁德时代',
                '京东', '拼多多', '美团', '抖音', '快手', '微信', '淘宝',
                '电商', '直播', '房地产', '股市', '基金', '新能源', '芯片', '半导体',
            ],
        }
        
        # ═══ LLM 直答偏好词(低权重,偏向 LLM 直答) ═══
        self.llm_direct_words = [
            '天气', '时间', '几点', '日期', '节日', '放假',
            '翻译', '怎么读', '什么意思', '用英语怎么说',
            '笑话', '段子', '搞笑',
            '推荐', '好看', '好吃', '好玩',
            '聊天', '陪我', '无聊',
        ]
        
        # ═══ 论证追问词 ═══
        self.argumentative_markers = [
            '为什么', '怎么理解', '如何看', '怎样看待', '是不是',
            '你认为', '你怎么看', '什么原因', '根源', '本质是什么',
            '深层', '背后', '逻辑', '关系',
            '是什么', '是什么意思', '怎么解释', '怎么理解',
            '有何', '有哪些', '区别是什么', '和.*的区别',
            # 主观追问(你觉得/你觉得...吗)
            '你觉得', '你认为', '在你看来', '依你看',
            # 启发/影响/反思类
            '启发', 'revelations', '有什么影响', '有什么意义',
            '如何看待', '如何评价', '怎么看待', '有何意义',
        ]
        
        # ═══ 任务驱动词 ═══
        self.task_markers = [
            '帮我', '给我', 'generate', '制定', '执行', '完成', '创建',
            '写', '分析', '评估', '优化', '解决', '计算', '总结',
        ]
        
        logger.info(f"混合路由器init完成 (complexity_threshold={self.complexity_threshold})")
    
    def route(self, user_input: str, context: Optional[Dict] = None) -> RouteDecision:
        """
        核心路由方法:决定输入走哪条链路
        
        Args:
            user_input: 用户输入
            context: 对话上下文
            
        Returns:
            RouteDecision 路由decision
        """
        if not user_input or not user_input.strip():
            return RouteDecision(
                route_type=RouteType.CONVERSATIONAL,
                confidence=0.9,
                reasoning="空输入,直接回复",
            )
        
        input_stripped = user_input.strip()
        input_lower = input_stripped.lower()
        
        # ═══ 第1层:对话型拦截 ═══
        for pattern in self.conversational_patterns:
            if re.match(pattern, input_stripped, re.IGNORECASE):
                return RouteDecision(
                    route_type=RouteType.CONVERSATIONAL,
                    confidence=0.95,
                    reasoning=f"匹配寒暄/简短回复模式: {pattern[:20]}",
                )
        
        # ═══ 第2层:极短输入 → 对话型 ═══
        if len(input_stripped) <= 4:
            return RouteDecision(
                route_type=RouteType.CONVERSATIONAL,
                confidence=0.8,
                reasoning=f"极短输入({len(input_stripped)}字),走对话型",
            )
        
        # ═══ 第3层:计算复杂度分数和领域分数 ═══
        complexity = self._calc_complexity(input_stripped)
        domain_match = self._calc_domain_match(input_stripped)
        
        # ═══ 第4层:根据分数做路由decision ═══
        
        # 4.1 任务驱动型 → 工作流
        if self._has_task_marker(input_stripped):
            # 如果有任务词 + 高领域匹配 → 工作流
            if domain_match.score > self.domain_threshold:
                return RouteDecision(
                    route_type=RouteType.SOMN_WORKFLOW,
                    confidence=min(0.9, domain_match.score + 0.2),
                    reasoning=f"任务驱动({domain_match.matched_words[:3]}) + 领域匹配({domain_match.category})",
                    complexity_score=complexity,
                    domain_score=domain_match.score,
                    detail={"matched_category": domain_match.category, "matched_words": domain_match.matched_words},
                )
            # 有任务词但领域不明确 → 也走工作流(用户要做事)
            return RouteDecision(
                route_type=RouteType.SOMN_WORKFLOW,
                confidence=0.7,
                reasoning=f"任务驱动词匹配: {self._matched_task_marker(input_stripped)}",
                complexity_score=complexity,
                domain_score=domain_match.score,
            )
        
        # 4.2 论证追问型 → 智慧板块
        if self._has_argumentative_marker(input_stripped):
            # 哲学追问 + 智慧领域 → 智慧板块
            if domain_match.category in ("wisdom", "growth", "strategy", "marketing"):
                return RouteDecision(
                    route_type=RouteType.SOMN_WISDOM,
                    confidence=min(0.9, domain_match.score + 0.3),
                    reasoning=f"论证追问({self._matched_argumentative_marker(input_stripped)}) + 智慧领域({domain_match.category})",
                    complexity_score=complexity,
                    domain_score=domain_match.score,
                    detail={"matched_category": domain_match.category},
                )
            # 论证追问 + 行业领域 → 工作流
            if domain_match.category == "industry":
                return RouteDecision(
                    route_type=RouteType.SOMN_WORKFLOW,
                    confidence=0.8,
                    reasoning=f"论证追问 + 行业实体({domain_match.matched_words[:3]})",
                    complexity_score=complexity,
                    domain_score=domain_match.score,
                )
            # 纯论证追问(无明确领域) → 智慧板块
            return RouteDecision(
                route_type=RouteType.SOMN_WISDOM,
                confidence=0.7,
                reasoning=f"论证追问: {self._matched_argumentative_marker(input_stripped)}",
                complexity_score=complexity,
                domain_score=domain_match.score,
            )
        
        # 4.3 高领域匹配 → Somn 链路
        if domain_match.score > self.domain_threshold:
            # 智慧/哲学领域 → 智慧板块
            if domain_match.category in ("wisdom",):
                return RouteDecision(
                    route_type=RouteType.SOMN_WISDOM,
                    confidence=domain_match.score,
                    reasoning=f"智慧领域匹配: {domain_match.matched_words[:3]}",
                    complexity_score=complexity,
                    domain_score=domain_match.score,
                )
            # 商业/行业领域 → 工作流
            if domain_match.category in ("growth", "strategy", "marketing", "tech", "industry"):
                return RouteDecision(
                    route_type=RouteType.SOMN_WORKFLOW,
                    confidence=domain_match.score,
                    reasoning=f"专业领域匹配({domain_match.category}): {domain_match.matched_words[:3]}",
                    complexity_score=complexity,
                    domain_score=domain_match.score,
                )
        
        # 4.4 高复杂度 → 智慧板块
        if complexity > self.complexity_threshold:
            return RouteDecision(
                route_type=RouteType.SOMN_WISDOM,
                confidence=complexity,
                reasoning=f"高复杂度({complexity:.2f}) → 智慧板块论证",
                complexity_score=complexity,
                domain_score=domain_match.score,
            )
        
        # 4.5 低复杂度 + 低领域匹配 + LLM直答词 → LLM 直答
        if any(w in input_lower for w in self.llm_direct_words):
            return RouteDecision(
                route_type=RouteType.LLM_DIRECT,
                confidence=0.8,
                reasoning=f"日常话题匹配,走 LLM 直答",
                complexity_score=complexity,
                domain_score=domain_match.score,
            )
        
        # 4.6 中等长度但无明确信号 → LLM 直答(兜底)
        # 这样"今天心情不好"这类话不会强制走智慧板块
        if len(input_stripped) <= self.llm_direct_max_length and complexity < 0.3:
            return RouteDecision(
                route_type=RouteType.LLM_DIRECT,
                confidence=0.6,
                reasoning=f"中等长度({len(input_stripped)}字) + 低复杂度({complexity:.2f}) → LLM 直答",
                complexity_score=complexity,
                domain_score=domain_match.score,
            )
        
        # 4.7 兜底:较长输入 → 智慧板块
        return RouteDecision(
            route_type=RouteType.SOMN_WISDOM,
            confidence=0.5,
            reasoning=f"兜底路由(长度={len(input_stripped)}, 复杂度={complexity:.2f})",
            complexity_score=complexity,
            domain_score=domain_match.score,
        )
    
    def _calc_complexity(self, text: str) -> float:
        """
        计算问题复杂度分数
        
        维度:
        - 长度(越长越复杂,但有上限)
        - 逗号/句号数(越多说明论述越复杂)
        - 问号数(越多说明追问越多)
        - 连词数(因为,所以,但是,而且...说明逻辑关系越复杂)
        """
        score = 0.0
        
        # 长度维度 (0~0.3)
        length = len(text)
        score += min(0.3, length / 200 * 0.3)
        
        # 标点维度 (0~0.25)
        punctuation_score = 0.0
        punctuation_score += min(0.1, text.count(',') / 5 * 0.1)  # 逗号
        punctuation_score += min(0.1, text.count('.') / 3 * 0.1)  # 句号
        punctuation_score += min(0.05, text.count('?') / 2 * 0.05)  # 问号
        score += punctuation_score
        
        # 逻辑连词维度 (0~0.25)
        logical_connectors = [
            '因为', '所以', '但是', '然而', '不过', '而且', '或者',
            '如果', '那么', '既然', '虽然', '尽管', '不但', '不仅',
            '另一方面', '与此同时', '换句话说', '也就是说', '实际上',
            '本质上', '从根本上', '归根结底',
        ]
        connector_count = sum(1 for c in logical_connectors if c in text)
        score += min(0.25, connector_count / 5 * 0.25)
        
        # 抽象概念维度 (0~0.2)
        abstract_concepts = [
            '本质', '规律', '内在', '外在', '深层', '根源', '逻辑',
            '原因', '结果', '动机', '目的', '意义', '价值',
            '关系', '影响', '作用', '机制', '原理',
        ]
        abstract_count = sum(1 for c in abstract_concepts if c in text)
        score += min(0.2, abstract_count / 4 * 0.2)
        
        return min(1.0, score)
    
    def _calc_domain_match(self, text: str) -> 'DomainMatchResult':
        """计算领域匹配度"""
        best_category = None
        best_score = 0.0
        best_words = []
        
        for category, words in self.somn_domain_words.items():
            matched = [w for w in words if w in text]
            if matched:
                # 匹配越多,词越长 → 分数越高
                score = len(matched) / max(len(words), 1)
                score += sum(len(w) for w in matched) / 100  # 长词加分
                score = min(1.0, score)
                
                if score > best_score:
                    best_score = score
                    best_category = category
                    best_words = matched
        
        return DomainMatchResult(
            category=best_category or "none",
            score=best_score,
            matched_words=best_words,
        )
    
    def _has_task_marker(self, text: str) -> bool:
        return any(m in text for m in self.task_markers)
    
    def _matched_task_marker(self, text: str) -> str:
        for m in self.task_markers:
            if m in text:
                return m
        return ""
    
    def _has_argumentative_marker(self, text: str) -> bool:
        return any(m in text for m in self.argumentative_markers)
    
    def _matched_argumentative_marker(self, text: str) -> str:
        for m in self.argumentative_markers:
            if m in text:
                return m
        return ""
    
    def get_statistics(self) -> Dict[str, Any]:
        """get路由统计"""
        return {
            "complexity_threshold": self.complexity_threshold,
            "domain_threshold": self.domain_threshold,
            "llm_direct_max_length": self.llm_direct_max_length,
            "domain_categories": list(self.somn_domain_words.keys()),
        }

@dataclass
class DomainMatchResult:
    """领域匹配结果"""
    category: str
    score: float
    matched_words: List[str]

# 便捷函数
def create_hybrid_router(config: Optional[Dict] = None) -> HybridRouter:
    """创建混合路由器实例"""
    return HybridRouter(config=config)
