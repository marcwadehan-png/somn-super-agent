"""
PPTstyle智能学习系统
基于智能学习引擎的PPT设计style学习系统

核心特性:
1. 智能评估 - 自动评估PPT设计原则,配色方案,排版模式的质量
2. 逻辑judge - judge哪些style值得学习,哪些需要调整或拒绝
3. 择优decision - 在冲突的设计原则中择优选择
4. 持续进化 - 从用户反馈和实际效果中学习和优化
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import os

from .smart_learning_engine import (
    SmartLearningEngine,
    KnowledgeItem,
    KnowledgeQuality,
    RelevanceLevel,
    DecisionType,
    create_knowledge_item
)

logger = logging.getLogger(__name__)

@dataclass
class DesignPrinciple:
    """设计原则"""
    name: str                       # 原则名称
    description: str                # 描述
    source: str                     # 来源平台
    category: str                   # 类别(视觉/内容/动画)
    quality: int                    # 质量评分 (1-5)
    evidence: List[str]             # 证据
    conflicts: List[str] = None     # 冲突的原则
    application_count: int = 0      # 应用次数
    success_rate: float = 0.0       # 成功率

@dataclass
class ColorScheme:
    """配色方案"""
    name: str                       # 方案名称
    primary: str                    # 主色
    secondary: str                  # 辅色
    accent: str                     # 强调色
    background: str                 # 背景色
    text: str                       # 文字色
    source: str                     # 来源平台
    harmony_score: float = 0.0      # 和谐度评分
    usage_count: int = 0            # 使用次数
    user_rating: float = 0.0        # 用户评分

@dataclass
class LayoutPattern:
    """排版模式"""
    name: str                       # 模式名称
    description: str                # 描述
    source: str                     # 来源平台
    structure: Dict                 # 结构定义
    use_cases: List[str]            # 适用场景
    quality: int                    # 质量评分 (1-5)
    usage_count: int = 0            # 使用次数
    effectiveness: float = 0.0       # 效果评分

class PPTStyleLearner:
    """
    PPTstyle智能学习系统
    
    核心功能:
    1. 设计原则学习 - 从各平台学习优质设计原则
    2. 配色方案学习 - 学习和评估配色方案
    3. 排版模式学习 - 学习各种排版模式
    4. 效果评估 - 评估学习效果
    5. 持续优化 - 基于反馈持续优化
    """

    def __init__(self, learning_engine: SmartLearningEngine,
                 knowledge_base_path: Optional[str] = None):
        self.learning_engine = learning_engine
        self.knowledge_base_path = knowledge_base_path
        
        # 知识库
        self.design_principles: List[DesignPrinciple] = []
        self.color_schemes: List[ColorScheme] = []
        self.layout_patterns: List[LayoutPattern] = []
        
        # 学习统计
        self.learning_stats = {
            "total_principles_learned": 0,
            "total_schemes_learned": 0,
            "total_layouts_learned": 0,
            "total_decisions_made": 0,
            "avg_success_rate": 0.0
        }
        
        if knowledge_base_path and os.path.exists(knowledge_base_path):
            self._load_knowledge_base()

    def learn_design_principle(self, principle: DesignPrinciple) -> bool:
        """
        学习设计原则
        
        Args:
            principle: 设计原则
            
        Returns:
            是否成功学习
        """
        # 创建知识项
        knowledge = create_knowledge_item(
            source=principle.source,
            content={
                "name": principle.name,
                "description": principle.description,
                "category": principle.category,
                "evidence": principle.evidence
            },
            quality=principle.quality,
            relevance=self._assess_principle_relevance(principle),
            confidence=0.7,  # 默认置信度
            evidence=principle.evidence,
            tags=["design_principle", principle.category, principle.source]
        )
        
        # 使用学习引擎评估和decision
        decision = self.learning_engine.make_decision(
            knowledge,
            domain="design_principles"
        )
        
        # 记录decision
        self.learning_stats["total_decisions_made"] += 1
        
        if decision.decision in [DecisionType.ACCEPT, DecisionType.MERGE]:
            self.design_principles.append(principle)
            self.learning_stats["total_principles_learned"] += 1
            logger.info(f"✅ 学习设计原则: {principle.name} (来源: {principle.source})")
            return True
        else:
            logger.info(f"❌ 拒绝设计原则: {principle.name} - {decision.reason}")
            return False

    def learn_color_scheme(self, scheme: ColorScheme) -> bool:
        """
        学习配色方案
        
        Args:
            scheme: 配色方案
            
        Returns:
            是否成功学习
        """
        # 计算和谐度
        harmony_score = self._calculate_color_harmony(scheme)
        scheme.harmony_score = harmony_score
        
        # 创建知识项
        knowledge = create_knowledge_item(
            source=scheme.source,
            content={
                "name": scheme.name,
                "primary": scheme.primary,
                "secondary": scheme.secondary,
                "accent": scheme.accent,
                "background": scheme.background,
                "text": scheme.text,
                "harmony_score": harmony_score
            },
            quality=5 if harmony_score > 0.8 else 4 if harmony_score > 0.6 else 3,
            relevance=self._assess_scheme_relevance(scheme),
            confidence=harmony_score,  # 和谐度即置信度
            tags=["color_scheme", scheme.source]
        )
        
        # 使用学习引擎评估和decision
        decision = self.learning_engine.make_decision(
            knowledge,
            domain="color_schemes"
        )
        
        # 记录decision
        self.learning_stats["total_decisions_made"] += 1
        
        if decision.decision in [DecisionType.ACCEPT, DecisionType.MERGE]:
            self.color_schemes.append(scheme)
            self.learning_stats["total_schemes_learned"] += 1
            logger.info(f"✅ 学习配色方案: {scheme.name} (和谐度: {harmony_score:.2f})")
            return True
        else:
            logger.info(f"❌ 拒绝配色方案: {scheme.name} - {decision.reason}")
            return False

    def learn_layout_pattern(self, pattern: LayoutPattern) -> bool:
        """
        学习排版模式
        
        Args:
            pattern: 排版模式
            
        Returns:
            是否成功学习
        """
        # 创建知识项
        knowledge = create_knowledge_item(
            source=pattern.source,
            content={
                "name": pattern.name,
                "description": pattern.description,
                "structure": pattern.structure,
                "use_cases": pattern.use_cases
            },
            quality=pattern.quality,
            relevance=self._assess_layout_relevance(pattern),
            confidence=0.7,
            tags=["layout_pattern", pattern.source]
        )
        
        # 使用学习引擎评估和decision
        decision = self.learning_engine.make_decision(
            knowledge,
            domain="layout_patterns"
        )
        
        # 记录decision
        self.learning_stats["total_decisions_made"] += 1
        
        if decision.decision in [DecisionType.ACCEPT, DecisionType.MERGE]:
            self.layout_patterns.append(pattern)
            self.learning_stats["total_layouts_learned"] += 1
            logger.info(f"✅ 学习排版模式: {pattern.name} (来源: {pattern.source})")
            return True
        else:
            logger.info(f"❌ 拒绝排版模式: {pattern.name} - {decision.reason}")
            return False

    def _assess_principle_relevance(self, principle: DesignPrinciple) -> int:
        """评估设计原则相关性"""
        # 关键类别的原则相关性更高
        high_relevance_categories = ["视觉", "内容", "配色"]
        if principle.category in high_relevance_categories:
            return 5
        elif principle.category in ["动画", "交互"]:
            return 4
        else:
            return 3

    def _assess_scheme_relevance(self, scheme: ColorScheme) -> int:
        """评估配色方案相关性"""
        # 基于和谐度和来源评估
        if scheme.harmony_score > 0.8:
            return 5
        elif scheme.harmony_score > 0.6:
            return 4
        else:
            return 3

    def _assess_layout_relevance(self, pattern: LayoutPattern) -> int:
        """评估排版模式相关性"""
        # 基于使用场景数量和质量评估
        if len(pattern.use_cases) >= 3 and pattern.quality >= 4:
            return 5
        elif len(pattern.use_cases) >= 2:
            return 4
        else:
            return 3

    def _calculate_color_harmony(self, scheme: ColorScheme) -> float:
        """
        计算配色和谐度
        
        Args:
            scheme: 配色方案
            
        Returns:
            和谐度评分 [0.0-1.0]
        """
        # 简化版:基于60-30-10法则和对比度
        # 实际实现需要更复杂的色彩理论计算
        
        score = 0.5  # 基础分
        
        # 60-30-10法则奖励
        if scheme.primary and scheme.secondary and scheme.accent:
            score += 0.3
        
        # 对比度检查(简化版)
        if scheme.text and scheme.background:
            score += 0.2
        
        return min(score, 1.0)

    def record_feedback(self, knowledge_type: str,
                       knowledge_name: str,
                       is_effective: bool,
                       feedback: str = ""):
        """
        记录学习效果反馈
        
        Args:
            knowledge_type: 知识类型
            knowledge_name: 知识名称
            is_effective: 是否有效
            feedback: 反馈内容
        """
        # 找到对应的知识项
        knowledge = None
        if knowledge_type == "principle":
            knowledge = next(
                (p for p in self.design_principles if p.name == knowledge_name),
                None
            )
        elif knowledge_type == "scheme":
            knowledge = next(
                (s for s in self.color_schemes if s.name == knowledge_name),
                None
            )
        elif knowledge_type == "layout":
            knowledge = next(
                (l for l in self.layout_patterns if l.name == knowledge_name),
                None
            )
        
        if knowledge:
            knowledge.application_count += 1
            if is_effective:
                # 更新成功率
                current_rate = knowledge.success_rate
                new_rate = (current_rate * (knowledge.application_count - 1) + 1) / knowledge.application_count
                knowledge.success_rate = new_rate
            else:
                new_rate = (knowledge.success_rate * (knowledge.application_count - 1)) / knowledge.application_count
                knowledge.success_rate = new_rate
            
            logger.info(f"📊 反馈记录: {knowledge_name} - "
                       f"有效率={is_effective}, "
                       f"成功率={knowledge.success_rate:.2%}")
        
        # 更新整体统计
        effective_count = sum(
            1 for k in self.design_principles + self.color_schemes + self.layout_patterns
            if k.application_count > 0
        )
        if effective_count > 0:
            self.learning_stats["avg_success_rate"] = (
                sum(k.success_rate for k in self.design_principles + self.color_schemes + self.layout_patterns
                    if k.application_count > 0) / effective_count
            )

    def optimize_knowledge_base(self):
        """
        优化知识库
        
        基于学习效果反馈,优化知识库:
        1. 移除低效的知识
        2. 提升高效知识的优先级
        3. 标记待优化的知识
        """
        logger.info("🔄 开始优化知识库...")
        
        # 移除低效的设计原则(成功率<30%且应用次数>=5)
        self.design_principles = [
            p for p in self.design_principles
            if not (p.application_count >= 5 and p.success_rate < 0.3)
        ]
        
        # 移除低效的配色方案(用户评分<3且使用次数>=5)
        self.color_schemes = [
            s for s in self.color_schemes
            if not (s.usage_count >= 5 and s.user_rating < 3)
        ]
        
        # 移除低效的排版模式(效果评分<3且使用次数>=5)
        self.layout_patterns = [
            l for l in self.layout_patterns
            if not (l.usage_count >= 5 and l.effectiveness < 3)
        ]
        
        logger.info(f"✅ 知识库优化完成: "
                   f"设计原则={len(self.design_principles)}, "
                   f"配色方案={len(self.color_schemes)}, "
                   f"排版模式={len(self.layout_patterns)}")

    def get_learning_summary(self) -> Dict[str, Any]:
        """get学习总结"""
        summary = {
            "learning_stats": self.learning_stats,
            "knowledge_counts": {
                "design_principles": len(self.design_principles),
                "color_schemes": len(self.color_schemes),
                "layout_patterns": len(self.layout_patterns)
            },
            "top_principles": sorted(
                self.design_principles,
                key=lambda x: x.success_rate * x.application_count,
                reverse=True
            )[:5],
            "top_schemes": sorted(
                self.color_schemes,
                key=lambda x: (x.user_rating * x.usage_count + x.harmony_score * 10),
                reverse=True
            )[:5],
            "top_layouts": sorted(
                self.layout_patterns,
                key=lambda x: x.effectiveness * x.usage_count,
                reverse=True
            )[:5]
        }
        
        return summary

    def export_knowledge_base(self, filepath: str):
        """导出知识库"""
        export_data = {
            "design_principles": [
                {
                    "name": p.name,
                    "description": p.description,
                    "source": p.source,
                    "category": p.category,
                    "quality": p.quality,
                    "application_count": p.application_count,
                    "success_rate": p.success_rate
                }
                for p in self.design_principles
            ],
            "color_schemes": [
                {
                    "name": s.name,
                    "primary": s.primary,
                    "secondary": s.secondary,
                    "accent": s.accent,
                    "background": s.background,
                    "text": s.text,
                    "source": s.source,
                    "harmony_score": s.harmony_score,
                    "usage_count": s.usage_count,
                    "user_rating": s.user_rating
                }
                for s in self.color_schemes
            ],
            "layout_patterns": [
                {
                    "name": l.name,
                    "description": l.description,
                    "source": l.source,
                    "use_cases": l.use_cases,
                    "quality": l.quality,
                    "usage_count": l.usage_count,
                    "effectiveness": l.effectiveness
                }
                for l in self.layout_patterns
            ],
            "learning_stats": self.learning_stats,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"知识库导出至: {filepath}")

    def _load_knowledge_base(self):
        """加载知识库"""
        with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 加载设计原则
            for p_data in data.get("design_principles", []):
                principle = DesignPrinciple(
                    name=p_data["name"],
                    description=p_data["description"],
                    source=p_data["source"],
                    category=p_data["category"],
                    quality=p_data["quality"],
                    evidence=[],
                    application_count=p_data["application_count"],
                    success_rate=p_data["success_rate"]
                )
                self.design_principles.append(principle)
            
            # 加载配色方案
            for s_data in data.get("color_schemes", []):
                scheme = ColorScheme(
                    name=s_data["name"],
                    primary=s_data["primary"],
                    secondary=s_data["secondary"],
                    accent=s_data["accent"],
                    background=s_data["background"],
                    text=s_data["text"],
                    source=s_data["source"],
                    harmony_score=s_data["harmony_score"],
                    usage_count=s_data["usage_count"],
                    user_rating=s_data["user_rating"]
                )
                self.color_schemes.append(scheme)
            
            # 加载排版模式
            for l_data in data.get("layout_patterns", []):
                pattern = LayoutPattern(
                    name=l_data["name"],
                    description=l_data["description"],
                    source=l_data["source"],
                    structure=l_data.get("structure", {}),
                    use_cases=l_data["use_cases"],
                    quality=l_data["quality"],
                    usage_count=l_data["usage_count"],
                    effectiveness=l_data["effectiveness"]
                )
                self.layout_patterns.append(pattern)
            
            # 加载统计
            self.learning_stats = data.get("learning_stats", self.learning_stats)
            
            logger.info("知识库加载完成")

# 便捷函数
def create_principle(name: str, description: str, source: str,
                     category: str, quality: int = 4) -> DesignPrinciple:
    """创建设计原则"""
    return DesignPrinciple(
        name=name,
        description=description,
        source=source,
        category=category,
        quality=quality,
        evidence=[]
    )

def create_color_scheme(name: str, primary: str, secondary: str,
                        accent: str, background: str, text: str,
                        source: str) -> ColorScheme:
    """创建配色方案"""
    return ColorScheme(
        name=name,
        primary=primary,
        secondary=secondary,
        accent=accent,
        background=background,
        text=text,
        source=source
    )

def create_layout_pattern(name: str, description: str, source: str,
                          use_cases: List[str], structure: Dict = None,
                          quality: int = 4) -> LayoutPattern:
    """创建排版模式"""
    return LayoutPattern(
        name=name,
        description=description,
        source=source,
        structure=structure or {},
        use_cases=use_cases,
        quality=quality
    )

__all__ = [
    'DesignPrinciple', 'ColorScheme', 'LayoutPattern',
    'PPTStyleLearner', 'create_principle',
    'create_color_scheme', 'create_layout_pattern',
]
