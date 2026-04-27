# -*- coding: utf-8 -*-
"""复合智能增长 - CompoundIntelligence类

__all__ = [
    'apply_knowledge',
    'get_intelligence_report',
    'learn',
]

智能的复利效应:今天的学习成为明天的基础
"""

import logging
import random
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)

class CompoundIntelligence:
    """
    复合智能增长
    
    智能的复利效应:今天的学习成为明天的基础
    """
    
    def __init__(self):
        self.knowledge_base = {}  # 知识库
        self.learning_rate = 0.1  # 基础学习率
        self.compound_factor = 1.05  # 复利因子
        self.intelligence_score = 100  # 智能分数
        
    def learn(self, domain: str, knowledge: Dict):
        """学习新知识"""
        if domain not in self.knowledge_base:
            self.knowledge_base[domain] = []
        
        self.knowledge_base[domain].append({
            "knowledge": knowledge,
            "learned_at": datetime.now(),
            "mastery_level": 0.1
        })
        
        # 智能分数增长 (复利效应)
        self.intelligence_score *= self.compound_factor
        
        logger.info(f"🧠 学习新知识: {domain}, 智能分数: {self.intelligence_score:.0f}")
    
    def apply_knowledge(self, domain: str, problem: Dict) -> Dict:
        """应用知识解决问题"""
        if domain not in self.knowledge_base:
            return {"success": False, "reason": "知识领域不存在"}
        
        # 计算可用知识量
        available_knowledge = len(self.knowledge_base[domain])
        avg_mastery = sum(k["mastery_level"] for k in self.knowledge_base[domain]) / available_knowledge
        
        # 问题解决能力 = 知识量 × 掌握程度 × 智能分数因子
        problem_solving_ability = available_knowledge * avg_mastery * (self.intelligence_score / 100)
        
        # 成功概率
        success_probability = min(0.95, problem_solving_ability / 10)
        
        # 如果成功,提升掌握程度
        if random.random() < success_probability:
            for k in self.knowledge_base[domain]:
                k["mastery_level"] = min(1.0, k["mastery_level"] + 0.05)
        
        return {
            "success": random.random() < success_probability,
            "confidence": success_probability,
            "knowledge_applied": available_knowledge,
            "mastery_level": avg_mastery
        }
    
    def get_intelligence_report(self) -> Dict:
        """get智能报告"""
        total_knowledge = sum(len(kb) for kb in self.knowledge_base.values())
        
        return {
            "intelligence_score": int(self.intelligence_score),
            "knowledge_domains": len(self.knowledge_base),
            "total_knowledge_items": total_knowledge,
            "learning_rate": self.learning_rate,
            "compound_factor": self.compound_factor,
            "domains": {
                domain: {
                    "items": len(items),
                    "avg_mastery": sum(k["mastery_level"] for k in items) / len(items)
                }
                for domain, items in self.knowledge_base.items()
            }
        }
