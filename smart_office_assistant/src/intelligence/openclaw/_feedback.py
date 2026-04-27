# -*- coding: utf-8 -*-
"""
用户反馈学习系统 - 从反馈中学习

功能:
- 反馈收集
- 模式分析（简单关键词匹配 - 兼容层）
- 自适应调整
- 与 PatternLearner 深度学习器协作

版本: v1.1.0
更新: 2026-04-23 修复Set导入缺失，增强ActiveLearner与PatternLearner协作
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from collections import defaultdict
import re


@dataclass
class FeedbackItem:
    """反馈条目"""
    user_id: str
    sage_name: str
    rating: int  # 1-5
    comment: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)


class FeedbackCollector:
    """反馈收集器"""
    
    def __init__(self):
        self.feedbacks: List[FeedbackItem] = []
        self._user_patterns: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    
    def add(self, feedback: FeedbackItem):
        """添加反馈"""
        self.feedbacks.append(feedback)
        self._update_pattern(feedback)
    
    def _update_pattern(self, fb: FeedbackItem):
        """更新用户模式"""
        if fb.rating >= 4:
            self._user_patterns[fb.user_id][fb.sage_name] = self._user_patterns[fb.user_id].get(fb.sage_name, 0) + 0.1
        elif fb.rating <= 2:
            self._user_patterns[fb.user_id][fb.sage_name] = self._user_patterns[fb.user_id].get(fb.sage_name, 0) - 0.1
    
    def get_preferred_sages(self, user_id: str) -> List[str]:
        """获取用户偏好的贤者"""
        prefs = self._user_patterns.get(user_id, {})
        return sorted(prefs.keys(), key=lambda x: prefs[x], reverse=True)[:5]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取反馈统计"""
        if not self.feedbacks:
            return {"total": 0}
        
        ratings = [fb.rating for fb in self.feedbacks]
        return {
            "total": len(self.feedbacks),
            "avg_rating": sum(ratings) / len(ratings),
            "positive": len([r for r in ratings if r >= 4]),
            "negative": len([r for r in ratings if r <= 2]),
        }

    def get_recent(self, n: int = 20) -> List[FeedbackItem]:
        """获取最近的反馈"""
        return self.feedbacks[-n:]


class ActiveLearner:
    """主动学习器（轻量级关键词匹配，兼容层）

    提供简单的关键词→贤者推荐能力。
    对于需要更深层模式挖掘的场景，请使用 _pattern_learner.PatternLearner。
    """

    def __init__(self):
        self.patterns: Dict[str, List[str]] = defaultdict(list)
        self.ignored: Set[str] = set()
        # 可选的深层学习器引用（延迟绑定）
        self._deep_learner = None

    def set_deep_learner(self, learner: Any) -> None:
        """绑定深层学习器（PatternLearner实例）

        绑定后，recommend() 方法会优先使用深层学习器的推荐结果。
        """
        self._deep_learner = learner

    def learn(self, feedback: FeedbackItem):
        """学习反馈模式"""
        # 关键词提取（需要评论文本）
        if feedback.comment:
            keywords = re.findall(r'[\w]{2,}', feedback.comment.lower())
            for kw in keywords:
                if feedback.rating >= 4:
                    if feedback.sage_name not in self.patterns[kw]:
                        self.patterns[kw].append(feedback.sage_name)
                elif feedback.rating <= 2:
                    if feedback.sage_name in self.patterns.get(kw, []):
                        self.patterns[kw].remove(feedback.sage_name)

        # ★ v1.2 修复: 同步到深层学习器不受 comment 门控
        # 纯评分反馈（无评论）也需要传递给 PatternLearner 做画像/质量统计
        if self._deep_learner:
            self._deep_learner.learn(feedback)

    def recommend(self, query: str) -> List[str]:
        """基于模式推荐贤者

        如果已绑定深层学习器，优先使用深层学习器的综合推荐。
        否则回退到简单关键词匹配。
        """
        # 优先使用深层学习器
        if self._deep_learner:
            results = self._deep_learner.recommend_for_query(query)
            if results:
                return [sage for sage, score in results[:5]]

        # 回退：简单关键词匹配
        keywords = re.findall(r'[\w]{2,}', query.lower())

        candidates = defaultdict(float)
        for kw in keywords:
            for sage in self.patterns.get(kw, []):
                candidates[sage] += 1

        return sorted(candidates.keys(), key=lambda x: candidates[x], reverse=True)[:5]

    def get_ignored(self) -> List[str]:
        """获取应忽略的内容"""
        return list(self.ignored)


class SageAdaptor:
    """贤者适配器 - 根据反馈调整响应参数"""
    
    def __init__(self):
        self._params: Dict[str, Dict[str, float]] = defaultdict(lambda: {
            "detail_level": 1.0,
            "tone_formal": 0.5,
            "examples": 3,
            "citation_depth": 2
        })
    
    def adjust(self, sage_name: str, feedback: FeedbackItem):
        """根据反馈调整参数"""
        params = self._params[sage_name]
        
        if feedback.rating <= 2:
            params["detail_level"] = max(0.5, params["detail_level"] - 0.1)
        elif feedback.rating >= 4:
            params["detail_level"] = min(2.0, params["detail_level"] + 0.1)
    
    def get_params(self, sage_name: str) -> Dict[str, float]:
        """获取参数"""
        return self._params.get(sage_name, {"detail_level": 1.0, "tone_formal": 0.5, "examples": 3, "citation_depth": 2})


__all__ = ['FeedbackCollector', 'FeedbackItem', 'ActiveLearner', 'SageAdaptor']
