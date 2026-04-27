# -*- coding: utf-8 -*-
"""
模式学习器 - 从用户反馈中学习深层模式

功能:
- 语义模式挖掘（超越简单关键词匹配）
- 用户偏好画像构建
- 主题-贤者关联学习
- 时间序列模式（使用时段/频率偏好）
- 质量评估模式（什么反馈关联高质量回答）
- 冷启动与在线学习

版本: v1.0.0
创建: 2026-04-23
"""

from __future__ import annotations
import math
import re
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict

from ._feedback import FeedbackItem


@dataclass
class UserPreference:
    """用户偏好画像"""
    user_id: str
    preferred_sages: Dict[str, float] = field(default_factory=lambda: defaultdict(float))
    preferred_topics: Dict[str, float] = field(default_factory=lambda: defaultdict(float))
    preferred_style: Dict[str, float] = field(default_factory=lambda: defaultdict(float))
    # 风格维度
    detail_preference: float = 0.0     # -1(简洁) ~ +1(详细)
    formality_preference: float = 0.0  # -1(随意) ~ +1(正式)
    example_preference: float = 0.0    # -1(少例子) ~ +1(多例子)
    total_feedbacks: int = 0
    last_active: Optional[datetime] = None


@dataclass
class TopicSageAssociation:
    """主题-贤者关联强度"""
    topic: str
    sage_name: str
    strength: float = 0.0             # -1.0 ~ +1.0（负值=不推荐）
    sample_count: int = 0
    avg_rating: float = 0.0
    last_updated: Optional[datetime] = None


@dataclass
class QualityPattern:
    """质量评估模式"""
    pattern_id: str
    description: str
    features: Dict[str, float] = field(default_factory=dict)  # 特征值
    outcome_avg: float = 0.0          # 平均评分
    sample_count: int = 0


@dataclass
class TimePattern:
    """时间使用模式"""
    hour: int                          # 0-23
    usage_count: int = 0
    preferred_sages: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    avg_rating: float = 0.0
    query_types: Dict[str, int] = field(default_factory=lambda: defaultdict(int))


class PatternLearner:
    """模式学习器

    从用户反馈中挖掘深层模式，提供超越简单关键词匹配的智能推荐基础。

    核心能力:
    1. 语义模式挖掘: 从反馈文本中提取主题、意图、情感维度
    2. 用户偏好画像: 构建多维度用户模型
    3. 主题-贤者关联: 学习"什么主题适合哪个贤者回答"
    4. 时间模式: 使用时段与偏好关联
    5. 质量评估: 识别高质量回答的模式特征

    示例:
        learner = PatternLearner()
        for fb in feedbacks:
            learner.learn(fb)
        # 查询用户画像
        profile = learner.get_user_profile("user_123")
        # 查询主题关联
        assocs = learner.get_topic_associations("仁义道德")
    """

    def __init__(self):
        # 用户画像
        self._user_profiles: Dict[str, UserPreference] = {}
        # 主题-贤者关联
        self._topic_sage: Dict[str, Dict[str, TopicSageAssociation]] = defaultdict(dict)
        # 全局贤者质量统计
        self._sage_quality: Dict[str, Dict[str, float]] = defaultdict(lambda: {
            "avg_rating": 0.0,
            "total": 0,
            "positive": 0,
            "negative": 0,
            "strength": 0.0,   # 综合强度 0-1
        })
        # 时间模式
        self._time_patterns: Dict[int, TimePattern] = {h: TimePattern(hour=h) for h in range(24)}
        # 质量模式
        self._quality_patterns: List[QualityPattern] = []
        # 主题词典（从反馈中自动积累）
        self._topic_vocabulary: Dict[str, Set[str]] = defaultdict(set)  # topic -> keywords
        self._total_samples = 0
        # 停用词
        self._stop_words = self._build_stop_words()

    def learn(self, feedback: FeedbackItem) -> None:
        """学习单条反馈

        从反馈中提取多层模式信息:
        1. 更新用户画像
        2. 更新主题-贤者关联
        3. 更新贤者质量统计
        4. 更新时间模式
        5. 更新主题词典
        """
        if not feedback.sage_name:
            return

        self._total_samples += 1

        # 提取主题
        topics = self._extract_topics(feedback.comment)

        # 更新用户画像
        self._update_user_profile(feedback, topics)

        # 更新主题-贤者关联
        for topic in topics:
            self._update_topic_sage(topic, feedback)

        # 更新贤者质量
        self._update_sage_quality(feedback)

        # 更新时间模式
        self._update_time_pattern(feedback)

        # 更新主题词典
        for topic in topics:
            keywords = self._extract_keywords(feedback.comment)
            self._topic_vocabulary[topic].update(keywords)

    # ─────────────────────────────────────────
    # 查询接口
    # ─────────────────────────────────────────

    def get_user_profile(self, user_id: str) -> Optional[UserPreference]:
        """获取用户偏好画像"""
        return self._user_profiles.get(user_id)

    def get_topic_associations(self, topic: str, top_k: int = 5) -> List[TopicSageAssociation]:
        """获取指定主题的贤者关联排序"""
        # 精确匹配
        associations = list(self._topic_sage.get(topic, {}).values())
        if associations:
            associations.sort(key=lambda a: a.strength, reverse=True)
            return associations[:top_k]

        # 模糊匹配：找包含topic关键词的主题
        fuzzy_results = []
        topic_lower = topic.lower()
        for t, sage_map in self._topic_sage.items():
            if topic_lower in t.lower() or t.lower() in topic_lower:
                for assoc in sage_map.values():
                    fuzzy_results.append(assoc)
            # 关键词匹配
            for kw in self._topic_vocabulary.get(t, set()):
                if kw in topic_lower:
                    for assoc in sage_map.values():
                        fuzzy_results.append(assoc)

        fuzzy_results.sort(key=lambda a: a.strength, reverse=True)
        return fuzzy_results[:top_k]

    def get_sage_quality(self, sage_name: str) -> Dict[str, float]:
        """获取贤者质量统计"""
        return dict(self._sage_quality.get(sage_name, {}))

    def get_top_sages(self, topic: str = "", top_k: int = 10) -> List[Tuple[str, float]]:
        """获取综合排名最高的贤者

        Args:
            topic: 主题（有主题时考虑主题关联）
            top_k: 返回数量
        """
        scores = {}
        for sage_name, quality in self._sage_quality.items():
            base_score = quality["strength"]
            if topic:
                # 融合主题关联
                topic_score = 0.0
                assocs = self.get_topic_associations(topic, top_k=3)
                for a in assocs:
                    if a.sage_name == sage_name:
                        topic_score = a.strength
                        break
                # 加权融合: 60%全局 + 40%主题
                scores[sage_name] = 0.6 * base_score + 0.4 * max(topic_score, 0)
            else:
                scores[sage_name] = base_score

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def get_time_recommendation(self, hour: Optional[int] = None) -> TimePattern:
        """获取时间维度推荐"""
        if hour is None:
            hour = datetime.now().hour
        return self._time_patterns.get(hour, TimePattern(hour=hour))

    def recommend_for_query(self, query: str, user_id: str = "") -> List[Tuple[str, float]]:
        """综合推荐：结合用户偏好、主题关联、全局质量

        Args:
            query: 用户查询
            user_id: 用户ID（可选）

        Returns:
            [(sage_name, score), ...] 排序列表
        """
        # 提取查询主题
        query_topics = self._extract_topics(query)

        candidates: Dict[str, float] = defaultdict(float)

        # 1. 全局贤者质量（基础分）
        for sage_name, quality in self._sage_quality.items():
            if quality["total"] > 0:
                candidates[sage_name] += quality["strength"] * 0.3

        # 2. 主题-贤者关联
        for topic in query_topics:
            assocs = self.get_topic_associations(topic, top_k=5)
            for a in assocs:
                candidates[a.sage_name] += a.strength * 0.4

        # 3. 用户偏好
        if user_id:
            profile = self.get_user_profile(user_id)
            if profile:
                for sage_name, pref in profile.preferred_sages.items():
                    if pref > 0:
                        candidates[sage_name] += pref * 0.2
                # 风格匹配
                for sage_name in candidates:
                    style_score = profile.preferred_style.get(sage_name, 0)
                    candidates[sage_name] += style_score * 0.1

        # 4. 时间因子
        hour = datetime.now().hour
        time_pattern = self._time_patterns.get(hour)
        if time_pattern and time_pattern.usage_count > 3:
            for sage_name, count in time_pattern.preferred_sages.items():
                if sage_name in candidates:
                    candidates[sage_name] += (count / time_pattern.usage_count) * 0.05

        # 归一化并排序
        if candidates:
            max_score = max(candidates.values())
            if max_score > 0:
                candidates = {k: v / max_score for k, v in candidates.items()}

        return sorted(candidates.items(), key=lambda x: x[1], reverse=True)

    def get_stats(self) -> Dict[str, Any]:
        """获取学习器统计"""
        return {
            "total_samples": self._total_samples,
            "user_profiles": len(self._user_profiles),
            "topics_learned": len(self._topic_sage),
            "sages_evaluated": len(self._sage_quality),
            "topic_vocabulary_size": sum(len(v) for v in self._topic_vocabulary.values()),
        }

    # ─────────────────────────────────────────
    # 内部更新方法
    # ─────────────────────────────────────────

    def _update_user_profile(self, fb: FeedbackItem, topics: List[str]) -> None:
        """更新用户画像"""
        if fb.user_id not in self._user_profiles:
            self._user_profiles[fb.user_id] = UserPreference(user_id=fb.user_id)

        profile = self._user_profiles[fb.user_id]
        profile.total_feedbacks += 1
        # ★ v1.1 修复: datetime 对象永远 truthy，需显式判 None
        profile.last_active = fb.timestamp if fb.timestamp is not None else datetime.now()

        # 贤者偏好（指数加权移动平均）
        # ★ v1.1 修复: 中性评分(rating=3)不更新偏好，避免信号衰减污染画像
        if fb.rating != 3:
            alpha = 0.3  # 学习率
            current = profile.preferred_sages.get(fb.sage_name, 0)
            rating_signal = (fb.rating - 3.0) / 2.0  # 映射到 [-1, +1]
            profile.preferred_sages[fb.sage_name] = current * (1 - alpha) + rating_signal * alpha

        # 主题偏好
        for topic in topics:
            current_t = profile.preferred_topics.get(topic, 0)
            profile.preferred_topics[topic] = current_t * (1 - alpha) + rating_signal * alpha

        # 风格偏好（从反馈文本推断）
        style_signals = self._infer_style_from_comment(fb.comment)
        for key, signal in style_signals.items():
            current_s = profile.preferred_style.get(key, 0)
            profile.preferred_style[key] = current_s * (1 - alpha) + signal * alpha
            # 更新顶层风格
            if key == "detail":
                profile.detail_preference = profile.preferred_style.get("detail", 0)
            elif key == "formal":
                profile.formality_preference = profile.preferred_style.get("formal", 0)
            elif key == "examples":
                profile.example_preference = profile.preferred_style.get("examples", 0)

    def _update_topic_sage(self, topic: str, fb: FeedbackItem) -> None:
        """更新主题-贤者关联"""
        topic_key = topic.lower()
        if fb.sage_name not in self._topic_sage[topic_key]:
            self._topic_sage[topic_key][fb.sage_name] = TopicSageAssociation(
                topic=topic_key, sage_name=fb.sage_name,
            )

        assoc = self._topic_sage[topic_key][fb.sage_name]
        alpha = 0.2

        # 更新强度（基于评分）
        rating_signal = (fb.rating - 3.0) / 2.0
        assoc.strength = assoc.strength * (1 - alpha) + rating_signal * alpha
        assoc.sample_count += 1

        # 更新平均评分
        total = assoc.avg_rating * (assoc.sample_count - 1) + fb.rating
        assoc.avg_rating = total / assoc.sample_count

        assoc.last_updated = datetime.now()

    def _update_sage_quality(self, fb: FeedbackItem) -> None:
        """更新贤者质量统计"""
        q = self._sage_quality[fb.sage_name]
        q["total"] += 1
        if fb.rating >= 4:
            q["positive"] += 1
        elif fb.rating <= 2:
            q["negative"] += 1

        # 滑动平均评分
        alpha = 0.1
        q["avg_rating"] = q["avg_rating"] * (1 - alpha) + fb.rating * alpha

        # 综合强度: 0-1
        if q["total"] > 0:
            pos_ratio = q["positive"] / q["total"]
            neg_ratio = q["negative"] / q["total"]
            q["strength"] = min(1.0, max(0.0,
                pos_ratio * 0.6 + (q["avg_rating"] / 5.0) * 0.3 + (1 - neg_ratio) * 0.1
            ))

    def _update_time_pattern(self, fb: FeedbackItem) -> None:
        """更新时间模式"""
        hour = fb.timestamp.hour if fb.timestamp else datetime.now().hour
        tp = self._time_patterns[hour]
        tp.usage_count += 1
        tp.preferred_sages[fb.sage_name] = tp.preferred_sages.get(fb.sage_name, 0) + 1

        alpha = 0.15
        tp.avg_rating = tp.avg_rating * (1 - alpha) + fb.rating * alpha

        # 查询类型分类
        if fb.comment:
            q_type = self._classify_query_type(fb.comment)
            tp.query_types[q_type] = tp.query_types.get(q_type, 0) + 1

    # ─────────────────────────────────────────
    # 主题提取与关键词
    # ─────────────────────────────────────────

    def _extract_topics(self, text: str) -> List[str]:
        """从文本中提取主题（基于TF启发式）"""
        if not text:
            return []

        # 提取有意义的关键词
        keywords = self._extract_keywords(text)
        if not keywords:
            return []

        # 按词频排序
        freq = defaultdict(int)
        for kw in keywords:
            freq[kw] += 1

        # 按频率排序，取前5个
        sorted_kws = sorted(freq.items(), key=lambda x: x[1], reverse=True)

        # 组合为主题
        topics = []
        for kw, count in sorted_kws[:5]:
            if count >= 1 and len(kw) >= 2:
                topics.append(kw)

        return topics

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词（中英文混合）"""
        keywords = []

        # 中文：2-4字词组
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        keywords.extend(chinese_words)

        # 英文：单词（去停用词）
        english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())
        keywords.extend(w for w in english_words if w not in self._stop_words)

        return keywords

    def _classify_query_type(self, text: str) -> str:
        """分类查询类型"""
        type_patterns = {
            "factual": [r"是什么|什么是|who\s+is|what\s+is|定义|概念"],
            "howto": [r"怎么|如何|how\s+to|方法|步骤|流程"],
            "comparison": [r"对比|比较|区别|异同|compare|difference|vs"],
            "analysis": [r"分析|评估|评价|为什么|原因|analyze|why"],
            "creative": [r"写|创作|生成|设计|write|create|design"],
            "discussion": [r"讨论|观点|看法|你怎么看|opinion|think"],
        }

        text_lower = text.lower()
        for q_type, patterns in type_patterns.items():
            for pat in patterns:
                if re.search(pat, text_lower):
                    return q_type
        return "general"

    def _infer_style_from_comment(self, comment: str) -> Dict[str, float]:
        """从评论文本推断用户风格偏好"""
        if not comment:
            return {}

        signals = {}
        comment_lower = comment.lower()

        # 太详细了 → 用户偏好简洁
        if any(w in comment_lower for w in ["太长", "太详细", "啰嗦", "简洁", "太复杂", "太啰嗦", "too long", "verbose"]):
            signals["detail"] = -0.5
        elif any(w in comment_lower for w in ["不够详细", "太简单", "再详细", "多说说", "展开", "more detail", "elaborate"]):
            signals["detail"] = 0.5

        # 太正式/太随意
        if any(w in comment_lower for w in ["太正式", "太严肃", "严肃点", "more formal"]):
            signals["formal"] = 0.5
        elif any(w in comment_lower for w in ["太随意", "不专业", "口语化", "casual"]):
            signals["formal"] = -0.5

        # 例子偏好
        if any(w in comment_lower for w in ["举个例子", "具体例子", "实例", "例子", "example", "for instance"]):
            signals["examples"] = 0.5

        return signals

    @staticmethod
    def _build_stop_words() -> Set[str]:
        """构建停用词集合"""
        return {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "shall", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "out", "off", "over",
            "under", "again", "further", "then", "once", "and", "but", "or",
            "nor", "not", "so", "yet", "both", "either", "neither", "each",
            "every", "all", "any", "few", "more", "most", "other", "some",
            "such", "no", "only", "own", "same", "than", "too", "very",
            "just", "because", "if", "when", "where", "how", "what", "which",
            "who", "whom", "this", "that", "these", "those", "it", "its",
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
            "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
            "会", "着", "没有", "看", "好", "自己", "这", "他", "她", "吗",
        }


__all__ = [
    'PatternLearner',
    'UserPreference',
    'TopicSageAssociation',
    'QualityPattern',
    'TimePattern',
]
