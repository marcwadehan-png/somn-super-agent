"""
__all__ = [
    'create_learning_engine',
    'find_similar_patterns',
    'get_learning_report',
    'get_suggestions',
    'learn_from_interaction',
    'record_feedback',
    'run_learning_cycle',
]

学习引擎 - Learning Engine
实现智能体的自主学习和知识进化
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import threading

from loguru import logger

@dataclass
class LearningPattern:
    """学习到的模式"""
    pattern_id: str
    pattern_type: str  # 'intent', 'response', 'workflow'
    trigger: str
    action: str
    confidence: float
    frequency: int
    last_used: datetime
    context: Dict[str, Any]

@dataclass
class FeedbackRecord:
    """反馈记录"""
    record_id: str
    interaction_id: str
    rating: int  # 1-5
    feedback_type: str  # 'positive', 'negative', 'neutral'
    comment: str
    timestamp: datetime
    context: Dict[str, Any]

class LearningEngine:
    """
    学习引擎
    
    功能:
    - 从用户交互中学习
    - recognize和优化行为模式
    - 根据反馈调整strategy
    - 知识自动更新
    """
    
    def __init__(self, data_path: str = "data/learning"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 学习到的模式
        self.patterns: Dict[str, LearningPattern] = {}
        self.pattern_index: Dict[str, List[str]] = defaultdict(list)
        
        # 反馈记录
        self.feedback_history: List[FeedbackRecord] = []
        
        # 性能metrics
        self.metrics = {
            'total_interactions': 0,
            'successful_interactions': 0,
            'average_rating': 0.0,
            'learning_cycles': 0
        }
        
        # 线程锁
        self._lock = threading.RLock()
        
        # 加载已有数据
        self._load_data()
        
        logger.info("学习引擎init完成")
    
    def _load_data(self):
        """加载学习数据"""
        patterns_file = self.data_path / "patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for p_data in data.get('patterns', []):
                    pattern = LearningPattern(
                        pattern_id=p_data['pattern_id'],
                        pattern_type=p_data['pattern_type'],
                        trigger=p_data['trigger'],
                        action=p_data['action'],
                        confidence=p_data['confidence'],
                        frequency=p_data['frequency'],
                        last_used=datetime.fromisoformat(p_data['last_used']),
                        context=p_data['context']
                    )
                    self.patterns[pattern.pattern_id] = pattern
                    self.pattern_index[pattern.pattern_type].append(pattern.pattern_id)
        
        metrics_file = self.data_path / "metrics.json"
        if metrics_file.exists():
            with open(metrics_file, 'r', encoding='utf-8') as f:
                self.metrics = json.load(f)
    
    def _save_data(self):
        """保存学习数据"""
        patterns_data = {
            'patterns': [
                {
                    'pattern_id': p.pattern_id,
                    'pattern_type': p.pattern_type,
                    'trigger': p.trigger,
                    'action': p.action,
                    'confidence': p.confidence,
                    'frequency': p.frequency,
                    'last_used': p.last_used.isoformat(),
                    'context': p.context
                }
                for p in self.patterns.values()
            ]
        }
        
        with open(self.data_path / "patterns.json", 'w', encoding='utf-8') as f:
            json.dump(patterns_data, f, ensure_ascii=False, indent=2)
        
        with open(self.data_path / "metrics.json", 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, ensure_ascii=False, indent=2)
    
    def learn_from_interaction(
        self,
        user_input: str,
        agent_response: str,
        intent: str,
        success: bool,
        context: Dict[str, Any]
    ):
        """
        从交互中学习
        
        Args:
            user_input: 用户输入
            agent_response: 智能体响应
            intent: recognize到的意图
            success: 交互是否成功
            context: 上下文信息
        """
        with self._lock:
            self.metrics['total_interactions'] += 1
            if success:
                self.metrics['successful_interactions'] += 1
            
            # 提取模式
            self._extract_pattern(user_input, agent_response, intent, context)
            
            # 更新意图统计
            self._update_intent_stats(intent, success)
            
            # 定期保存
            if self.metrics['total_interactions'] % 10 == 0:
                self._save_data()
    
    def _extract_pattern(
        self,
        user_input: str,
        agent_response: str,
        intent: str,
        context: Dict[str, Any]
    ):
        """提取交互模式"""
        # [修复] 使用稳定的内容哈希代替Python不稳定的hash()
        # Python的hash()因哈希随机化在不同运行中会产生不同结果
        import hashlib
        
        # 生成稳定的内容指纹
        content_hash = hashlib.md5(f"{intent}:{user_input}".encode()).hexdigest()[:12]
        pattern_key = f"{intent}_{content_hash}"
        
        # 同时存储原始触发词用于相似度匹配
        trigger_key = user_input[:50].lower().strip()
        
        if pattern_key in self.patterns:
            # 更新现有模式
            pattern = self.patterns[pattern_key]
            pattern.frequency += 1
            pattern.last_used = datetime.now()
            # 提高置信度
            pattern.confidence = min(1.0, pattern.confidence + 0.01)
        else:
            # 创建新模式
            pattern = LearningPattern(
                pattern_id=pattern_key,
                pattern_type='intent_response',
                trigger=user_input[:50],  # 保存触发词的前50字符
                action=agent_response[:100],
                confidence=0.5,
                frequency=1,
                last_used=datetime.now(),
                context={'intent': intent, **context}
            )
            self.patterns[pattern_key] = pattern
            self.pattern_index['intent_response'].append(pattern_key)
            
            logger.debug(f"发现新模式: {pattern_key}")
    
    def _update_intent_stats(self, intent: str, success: bool):
        """更新意图统计"""
        # 这里可以实现更复杂的意图成功率统计
        pass
    
    def record_feedback(
        self,
        interaction_id: str,
        rating: int,
        feedback_type: str,
        comment: str = "",
        context: Dict[str, Any] = None
    ):
        """
        记录用户反馈
        
        Args:
            interaction_id: 交互ID
            rating: 评分 1-5
            feedback_type: 反馈类型
            comment: 评论
            context: 上下文
        """
        record = FeedbackRecord(
            record_id=f"feedback_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            interaction_id=interaction_id,
            rating=rating,
            feedback_type=feedback_type,
            comment=comment,
            timestamp=datetime.now(),
            context=context or {}
        )
        
        self.feedback_history.append(record)
        
        # 更新平均评分
        total_ratings = [f.rating for f in self.feedback_history]
        self.metrics['average_rating'] = sum(total_ratings) / len(total_ratings)
        
        # 根据反馈调整
        if feedback_type == 'negative':
            self._handle_negative_feedback(interaction_id, context)
        elif feedback_type == 'positive':
            self._handle_positive_feedback(interaction_id, context)
        
        logger.info(f"记录反馈: {feedback_type}, 评分: {rating}")
    
    def _handle_negative_feedback(self, interaction_id: str, context: Dict[str, Any]):
        """处理负面反馈"""
        # 降低相关模式的置信度
        for pattern in self.patterns.values():
            if pattern.context.get('interaction_id') == interaction_id:
                pattern.confidence = max(0.0, pattern.confidence - 0.1)
                logger.debug(f"降低模式置信度: {pattern.pattern_id}")
    
    def _handle_positive_feedback(self, interaction_id: str, context: Dict[str, Any]):
        """处理正面反馈"""
        # 提高相关模式的置信度
        for pattern in self.patterns.values():
            if pattern.context.get('interaction_id') == interaction_id:
                pattern.confidence = min(1.0, pattern.confidence + 0.05)
    
    def find_similar_patterns(
        self,
        query: str,
        pattern_type: Optional[str] = None,
        min_confidence: float = 0.5
    ) -> List[LearningPattern]:
        """
        查找相似模式
        
        Args:
            query: 查询
            pattern_type: 模式类型筛选
            min_confidence: 最小置信度
        
        Returns:
            匹配的模式列表
        """
        results = []
        
        patterns_to_check = self.patterns.values()
        if pattern_type:
            pattern_ids = self.pattern_index.get(pattern_type, [])
            patterns_to_check = [self.patterns[pid] for pid in pattern_ids if pid in self.patterns]
        
        for pattern in patterns_to_check:
            if pattern.confidence < min_confidence:
                continue
            
            # 简单相似度计算
            similarity = self._calculate_similarity(query, pattern.trigger)
            if similarity > 0.6:
                results.append((pattern, similarity))
        
        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:5]]
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度(简单版本)"""
        # 这里可以使用更复杂的算法,如余弦相似度
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def get_suggestions(self, context: Dict[str, Any]) -> List[str]:
        """
        基于学习到的模式提供建议
        
        Args:
            context: 当前上下文 [修复：现在正确使用context参数]
        
        Returns:
            建议列表
        """
        suggestions = []
        context = context or {}
        
        # 从context中提取关键信息用于过滤建议
        user_id = context.get("user_id", "")
        current_intent = context.get("current_intent", "")
        industry = context.get("industry", "")
        
        # 基于高频模式提供建议
        top_patterns = sorted(
            self.patterns.values(),
            key=lambda p: (p.frequency, p.confidence),
            reverse=True
        )[:10]
        
        # 根据上下文过滤和排序建议
        for pattern in top_patterns:
            if pattern.pattern_type == 'intent_response':
                # 计算上下文匹配度
                match_score = 0
                
                # 检查行业匹配
                if industry and industry in pattern.context.get("industry", ""):
                    match_score += 2
                
                # 检查意图匹配
                if current_intent and current_intent in pattern.context.get("intent", ""):
                    match_score += 3
                
                # 检查用户匹配
                if user_id and user_id in pattern.context.get("user_id", ""):
                    match_score += 1
                
                # 根据匹配度调整建议内容
                trigger_preview = pattern.trigger[:30]
                if match_score >= 3:
                    suggestions.append(f"[推荐] {trigger_preview}...")
                elif match_score >= 1:
                    suggestions.append(f"{trigger_preview}...")
                else:
                    suggestions.append(f"备选: {trigger_preview}...")
        
        return suggestions[:5]
    
    def run_learning_cycle(self):
        """
        运行学习周期
        定期调用以优化学习到的模式
        """
        with self._lock:
            logger.info("运行学习周期...")
            
            # 1. 清理低频模式
            patterns_to_remove = []
            for pattern_id, pattern in self.patterns.items():
                if pattern.frequency < 3 and pattern.confidence < 0.3:
                    patterns_to_remove.append(pattern_id)
            
            for pid in patterns_to_remove:
                del self.patterns[pid]
                logger.debug(f"移除低频模式: {pid}")
            
            # 2. 更新模式索引
            self.pattern_index.clear()
            for pattern in self.patterns.values():
                self.pattern_index[pattern.pattern_type].append(pattern.pattern_id)
            
            # 3. 保存数据
            self._save_data()
            
            self.metrics['learning_cycles'] += 1
            
            logger.info(f"学习周期完成,当前模式数: {len(self.patterns)}")
    
    def get_learning_report(self) -> Dict[str, Any]:
        """
        get学习报告
        
        Returns:
            学习统计报告
        """
        return {
            'metrics': self.metrics,
            'total_patterns': len(self.patterns),
            'pattern_types': {
                ptype: len(pids) 
                for ptype, pids in self.pattern_index.items()
            },
            'top_patterns': [
                {
                    'trigger': p.trigger[:50],
                    'frequency': p.frequency,
                    'confidence': p.confidence
                }
                for p in sorted(
                    self.patterns.values(),
                    key=lambda x: x.frequency,
                    reverse=True
                )[:10]
            ],
            'feedback_summary': {
                'total_feedback': len(self.feedback_history),
                'average_rating': self.metrics['average_rating'],
                'positive_ratio': sum(
                    1 for f in self.feedback_history if f.feedback_type == 'positive'
                ) / max(len(self.feedback_history), 1)
            }
        }

# 便捷函数
def create_learning_engine(data_path: str = "data/learning") -> LearningEngine:
    """创建学习引擎实例"""
    return LearningEngine(data_path)
