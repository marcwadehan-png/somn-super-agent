"""
智能学习引擎
基于逻辑judge,择优decision,持续提炼的自主学习系统

核心理念:
1. 智能评估 - 自动recognize知识的相关性,质量,适用性
2. 择优decision - 在多个方案中选择最优
3. 持续进化 - 从反馈中学习和优化
4. 效果追踪 - 量化学习效果
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)

class KnowledgeQuality(Enum):
    """知识质量等级"""
    EXCELLENT = 5  # 优秀 - 权威来源,详细验证,广泛认可
    HIGH = 4       # 高 - 可靠来源,部分验证
    MEDIUM = 3     # 中 - 一般来源,未验证
    LOW = 2        # 低 - 来源不明,需谨慎
    POOR = 1       # 差 - 不可靠,需拒绝

class RelevanceLevel(Enum):
    """相关性等级"""
    CRITICAL = 5   # 关键 - 直接影响系统核心功能
    HIGH = 4       # 高 - 重要功能
    MEDIUM = 3     # 中 - 次要功能
    LOW = 2        # 低 - 边缘功能
    IRRELEVANT = 1 # 不相关 - 不适用

class DecisionType(Enum):
    """decision类型"""
    ACCEPT = "accept"         # 接受知识
    REJECT = "reject"         # 拒绝知识
    MODIFY = "modify"         # 修改后接受
    DELAY = "delay"           # 延迟decision,待验证
    MERGE = "merge"           # 与现有知识fusion

@dataclass
class KnowledgeItem:
    """知识项"""
    source: str                    # 来源
    content: Any                   # 内容
    quality: KnowledgeQuality      # 质量等级
    relevance: RelevanceLevel      # 相关性等级
    confidence: float = 0.0        # 置信度 [0.0-1.0]
    evidence: List[str] = field(default_factory=list)  # 证据列表
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_priority(self) -> float:
        """计算优先级"""
        # synthesize考虑质量,相关性,置信度
        return (self.quality.value * 0.4 +
                self.relevance.value * 0.4 +
                self.confidence * 0.2)

@dataclass
class LearningDecision:
    """学习decision"""
    decision: DecisionType           # decision类型
    knowledge: KnowledgeItem          # 知识项
    reason: str                       # decision理由
    priority: float                   # 优先级
    conflicts: List[str] = field(default_factory=list)  # 冲突的知识
    alternatives: List['KnowledgeItem'] = field(default_factory=list)  # 替代方案
    validation_plan: Optional[str] = None  # 验证计划
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class SmartLearningEngine:
    """
    智能学习引擎
    
    核心功能:
    1. 知识评估 - 评估知识的相关性,质量,置信度
    2. 逻辑judge - 基于多因素做出学习decision
    3. 择优decision - 在多个方案中选择最优
    4. 持续进化 - 从反馈中学习和优化
    """

    def __init__(self, learning_config_path: Optional[str] = None):
        self.learning_config_path = learning_config_path
        self.knowledge_base: Dict[str, List[KnowledgeItem]] = {}
        self.decision_history: List[LearningDecision] = []
        self.feedback_history: List[Dict] = []
        self.performance_metrics = {
            "total_decisions": 0,
            "correct_decisions": 0,
            "accuracy": 0.0,
            "avg_confidence": 0.0
        }
        
        # 学习参数
        self.quality_threshold = KnowledgeQuality.MEDIUM  # 质量阈值
        self.relevance_threshold = RelevanceLevel.MEDIUM  # 相关性阈值
        self.confidence_threshold = 0.6  # 置信度阈值
        
        if learning_config_path and os.path.exists(learning_config_path):
            self._load_learning_config()

    def evaluate_knowledge(self, knowledge: KnowledgeItem) -> Dict[str, Any]:
        """
        评估知识
        
        Args:
            knowledge: 知识项
            
        Returns:
            评估结果字典
        """
        evaluation = {
            "quality_score": knowledge.quality.value,
            "relevance_score": knowledge.relevance.value,
            "confidence": knowledge.confidence,
            "priority": knowledge.calculate_priority(),
            "recommendation": None,
            "reasons": []
        }
        
        # 质量评估
        if knowledge.quality.value < self.quality_threshold.value:
            evaluation["reasons"].append(
                f"质量({knowledge.quality.name})低于阈值({self.quality_threshold.name})"
            )
        
        # 相关性评估
        if knowledge.relevance.value < self.relevance_threshold.value:
            evaluation["reasons"].append(
                f"相关性({knowledge.relevance.name})低于阈值({self.relevance_threshold.name})"
            )
        
        # 置信度评估
        if knowledge.confidence < self.confidence_threshold:
            evaluation["reasons"].append(
                f"置信度({knowledge.confidence:.2f})低于阈值({self.confidence_threshold})"
            )
        
        # synthesizejudge
        if (evaluation["priority"] >= 3.0 and 
            knowledge.confidence >= 0.6):
            evaluation["recommendation"] = DecisionType.ACCEPT
        elif (evaluation["priority"] >= 2.0 and 
              knowledge.confidence >= 0.4):
            evaluation["recommendation"] = DecisionType.DELAY
        elif evaluation["priority"] < 2.0:
            evaluation["recommendation"] = DecisionType.REJECT
        else:
            evaluation["recommendation"] = DecisionType.MODIFY
        
        return evaluation

    def detect_conflicts(self, new_knowledge: KnowledgeItem, 
                        domain: str) -> List[str]:
        """
        检测知识冲突
        
        Args:
            new_knowledge: 新知识
            domain: 知识域
            
        Returns:
            冲突的知识列表
        """
        conflicts = []
        
        if domain not in self.knowledge_base:
            return conflicts
        
        for existing_knowledge in self.knowledge_base[domain]:
            # 检测内容冲突(简化版)
            if isinstance(new_knowledge.content, dict) and \
               isinstance(existing_knowledge.content, dict):
                if self._is_conflicting(new_knowledge.content, 
                                        existing_knowledge.content):
                    conflicts.append(existing_knowledge.source)
        
        return conflicts

    def _is_conflicting(self, content1: Dict, content2: Dict) -> bool:
        """检测内容是否冲突"""
        # 简化版:检查是否有矛盾的键值对
        for key in content1:
            if key in content2 and content1[key] != content2[key]:
                # 检查是否是数字类型且相反
                if isinstance(content1[key], (int, float)) and \
                   isinstance(content2[key], (int, float)):
                    if content1[key] * content2[key] < 0:  # 符号相反
                        return True
        
        return False

    def select_best_alternative(self, 
                                candidates: List[KnowledgeItem]) -> KnowledgeItem:
        """
        选择最佳替代方案(择优)
        
        Args:
            candidates: 候选方案列表
            
        Returns:
            最佳方案
        """
        if not candidates:
            raise ValueError("候选方案列表为空")
        
        # synthesize评分:优先级 + 置信度
        best_candidate = max(
            candidates,
            key=lambda x: x.calculate_priority() + x.confidence * 2
        )
        
        logger.info(f"择优decision: 从{len(candidates)}个方案中选择最佳方案")
        logger.info(f"最佳方案来源: {best_candidate.source}, "
                   f"优先级: {best_candidate.calculate_priority():.2f}")
        
        return best_candidate

    def make_decision(self, knowledge: KnowledgeItem, 
                     domain: str) -> LearningDecision:
        """
        做出学习decision(逻辑judge)
        
        Args:
            knowledge: 知识项
            domain: 知识域
            
        Returns:
            学习decision
        """
        # 1. 评估知识
        evaluation = self.evaluate_knowledge(knowledge)
        
        # 2. 检测冲突
        conflicts = self.detect_conflicts(knowledge, domain)
        
        # 3. 确定decision
        decision_type = evaluation["recommendation"]
        reason = ",".join(evaluation["reasons"])
        
        # 如果存在冲突,需要择优
        if conflicts:
            # 收集冲突的知识
            conflict_candidates = [
                k for k in self.knowledge_base.get(domain, [])
                if k.source in conflicts
            ]
            conflict_candidates.append(knowledge)
            
            # 择优decision
            best = self.select_best_alternative(conflict_candidates)
            
            if best == knowledge:
                decision_type = DecisionType.MERGE
                reason = f"新知识更优,将与{len(conflicts)}个现有知识fusion"
            else:
                decision_type = DecisionType.REJECT
                reason = f"现有知识({best.source})更优,拒绝新知识"
        
        # 4. 构建decision
        decision = LearningDecision(
            decision=decision_type,
            knowledge=knowledge,
            reason=reason,
            priority=evaluation["priority"],
            conflicts=conflicts,
            validation_plan=self._create_validation_plan(knowledge, decision_type)
        )
        
        # 5. 记录decision历史
        self.decision_history.append(decision)
        self.performance_metrics["total_decisions"] += 1
        self.performance_metrics["avg_confidence"] = (
            (self.performance_metrics["avg_confidence"] * 
             (self.performance_metrics["total_decisions"] - 1) +
             knowledge.confidence) / self.performance_metrics["total_decisions"]
        )
        
        logger.info(f"学习decision: {decision_type.value} - {reason}")
        logger.info(f"优先级: {evaluation['priority']:.2f}")
        
        return decision

    def _create_validation_plan(self, knowledge: KnowledgeItem,
                                decision: DecisionType) -> Optional[str]:
        """创建验证计划"""
        if decision == DecisionType.ACCEPT:
            return f"接受{knowledge.source}的知识,需在实践中验证效果"
        elif decision == DecisionType.DELAY:
            return f"延迟decision,需收集更多证据和反馈"
        elif decision == DecisionType.MODIFY:
            return f"修改后接受,需调整内容并验证"
        elif decision == DecisionType.MERGE:
            return f"与现有知识fusion,需解决冲突并验证"
        else:
            return None

    def learn(self, knowledge: KnowledgeItem, domain: str) -> bool:
        """
        执行学习
        
        Args:
            knowledge: 知识项
            domain: 知识域
            
        Returns:
            是否成功学习
        """
        # 1. 做出decision
        decision = self.make_decision(knowledge, domain)
        
        # 2. 执行decision
        if decision.decision == DecisionType.ACCEPT:
            self._add_to_knowledge_base(knowledge, domain)
            return True
        
        elif decision.decision == DecisionType.MERGE:
            # fusion逻辑
            self._merge_knowledge(knowledge, domain)
            return True
        
        elif decision.decision == DecisionType.MODIFY:
            # 修改逻辑(简化版)
            modified_knowledge = self._modify_knowledge(knowledge)
            self._add_to_knowledge_base(modified_knowledge, domain)
            return True
        
        elif decision.decision == DecisionType.DELAY:
            logger.info(f"延迟学习: {knowledge.source}")
            return False
        
        else:  # REJECT
            logger.info(f"拒绝学习: {knowledge.source}")
            return False

    def _add_to_knowledge_base(self, knowledge: KnowledgeItem, domain: str):
        """添加到知识库"""
        if domain not in self.knowledge_base:
            self.knowledge_base[domain] = []
        self.knowledge_base[domain].append(knowledge)
        logger.info(f"添加知识到[{domain}]: {knowledge.source}")

    def _merge_knowledge(self, knowledge: KnowledgeItem, domain: str):
        """fusion知识"""
        if domain not in self.knowledge_base:
            self.knowledge_base[domain] = []
        
        # 简化版:直接添加,标记为fusion
        knowledge.metadata["merged"] = True
        self.knowledge_base[domain].append(knowledge)
        logger.info(f"fusion知识到[{domain}]: {knowledge.source}")

    def _modify_knowledge(self, knowledge: KnowledgeItem) -> KnowledgeItem:
        """修改知识(简化版)"""
        # 这里可以实现具体的修改逻辑
        modified_knowledge = KnowledgeItem(
            source=f"{knowledge.source}(modified)",
            content=knowledge.content,
            quality=knowledge.quality,
            relevance=knowledge.relevance,
            confidence=knowledge.confidence * 0.9,
            evidence=knowledge.evidence.copy(),
            tags=knowledge.tags.copy(),
            metadata={**knowledge.metadata, "modified": True}
        )
        return modified_knowledge

    def record_feedback(self, decision: LearningDecision, 
                        is_correct: bool, feedback: str = ""):
        """
        记录反馈(持续进化)
        
        Args:
            decision: 之前的decision
            is_correct: decision是否正确
            feedback: 反馈内容
        """
        feedback_record = {
            "decision": decision.decision.value,
            "knowledge_source": decision.knowledge.source,
            "is_correct": is_correct,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        
        self.feedback_history.append(feedback_record)
        
        # 更新性能metrics
        if is_correct:
            self.performance_metrics["correct_decisions"] += 1
        
        self.performance_metrics["accuracy"] = (
            self.performance_metrics["correct_decisions"] / 
            self.performance_metrics["total_decisions"]
        )
        
        # 学习和优化
        self._learn_from_feedback(feedback_record)
        
        logger.info(f"记录反馈: 正确={is_correct}, "
                   f"准确率={self.performance_metrics['accuracy']:.2%}")

    def _learn_from_feedback(self, feedback: Dict):
        """从反馈中学习"""
        # 简化版:根据反馈调整阈值
        if not feedback["is_correct"]:
            # 如果decision错误,调整相关阈值
            if feedback["decision"] == "accept":
                # 如果接受的decision错误,提高质量阈值
                self.quality_threshold = KnowledgeQuality(
                    min(5, self.quality_threshold.value + 1)
                )
                logger.info(f"提高质量阈值至: {self.quality_threshold.name}")
            
            elif feedback["decision"] == "reject":
                # 如果拒绝的decision错误,降低质量阈值
                self.quality_threshold = KnowledgeQuality(
                    max(1, self.quality_threshold.value - 1)
                )
                logger.info(f"降低质量阈值至: {self.quality_threshold.name}")

    def get_learning_summary(self) -> Dict[str, Any]:
        """get学习总结"""
        domain_stats = {}
        for domain, knowledge_list in self.knowledge_base.items():
            domain_stats[domain] = {
                "total_knowledge": len(knowledge_list),
                "avg_quality": sum(k.quality.value for k in knowledge_list) / len(knowledge_list),
                "avg_confidence": sum(k.confidence for k in knowledge_list) / len(knowledge_list)
            }
        
        return {
            "performance": self.performance_metrics,
            "domain_stats": domain_stats,
            "decision_history_size": len(self.decision_history),
            "feedback_history_size": len(self.feedback_history)
        }

    def export_knowledge_base(self, filepath: str):
        """导出知识库"""
        export_data = {
            "knowledge_base": {
                domain: [
                    {
                        "source": k.source,
                        "content": k.content,
                        "quality": k.quality.value,
                        "relevance": k.relevance.value,
                        "confidence": k.confidence,
                        "timestamp": k.timestamp,
                        "tags": k.tags,
                        "metadata": k.metadata
                    }
                    for k in knowledge_list
                ]
                for domain, knowledge_list in self.knowledge_base.items()
            },
            "performance_metrics": self.performance_metrics,
            "decision_history": [
                {
                    "decision": d.decision.value,
                    "knowledge_source": d.knowledge.source,
                    "reason": d.reason,
                    "priority": d.priority,
                    "timestamp": d.timestamp
                }
                for d in self.decision_history[-100:]  # 最近100条
            ],
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"知识库导出至: {filepath}")

    def _load_learning_config(self):
        """加载学习配置"""
        with open(self.learning_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.quality_threshold = KnowledgeQuality(
                config.get("quality_threshold", 3)
            )
            self.relevance_threshold = RelevanceLevel(
                config.get("relevance_threshold", 3)
            )
            self.confidence_threshold = config.get(
                "confidence_threshold", 0.6
            )
            logger.info("学习配置加载完成")

# 便捷函数
def create_knowledge_item(source: str, content: Any,
                          quality: int, relevance: int,
                          confidence: float = 0.7,
                          evidence: List[str] = None,
                          tags: List[str] = None) -> KnowledgeItem:
    """
    创建知识项
    
    Args:
        source: 来源
        content: 内容
        quality: 质量等级 (1-5)
        relevance: 相关性等级 (1-5)
        confidence: 置信度 (0.0-1.0)
        evidence: 证据列表
        tags: 标签列表
    
    Returns:
        知识项
    """
    return KnowledgeItem(
        source=source,
        content=content,
        quality=KnowledgeQuality(quality),
        relevance=RelevanceLevel(relevance),
        confidence=confidence,
        evidence=evidence or [],
        tags=tags or []
    )

__all__ = [
    'KnowledgeQuality', 'RelevanceLevel', 'DecisionType',
    'KnowledgeItem', 'LearningDecision', 'SmartLearningEngine',
    'create_knowledge_item',
]
