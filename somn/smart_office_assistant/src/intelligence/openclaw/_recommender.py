# -*- coding: utf-8 -*-
"""
智能推荐器 - 基于学习模式的贤者推荐引擎

功能:
- 多维度贤者推荐（查询语义 + 用户画像 + 主题关联 + 时间模式）
- 推荐解释（为什么推荐这个贤者）
- 推荐多样性控制（避免推荐过于集中）
- 冷启动策略（无反馈数据时的兜底推荐）
- A/B测试接口（推荐策略对比）
- 推荐效果追踪与自适应

版本: v1.0.0
创建: 2026-04-23
"""

from __future__ import annotations
import math
import re
import logging
from typing import Dict, List, Optional, Any, Tuple, Set, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

from ._pattern_learner import PatternLearner, UserPreference, TimePattern
from ._feedback import FeedbackItem


@dataclass
class Recommendation:
    """推荐结果"""
    sage_name: str
    score: float                      # 综合得分 0-1
    reasons: List[str] = field(default_factory=list)  # 推荐理由
    dimensions: Dict[str, float] = field(default_factory=dict)  # 各维度得分
    is_cold_start: bool = False       # 是否冷启动推荐


@dataclass
class RecommendationResult:
    """推荐结果集"""
    recommendations: List[Recommendation] = field(default_factory=list)
    query: str = ""
    user_id: str = ""
    strategy: str = "hybrid"           # 使用的策略
    total_candidates: int = 0          # 候选总数
    elapsed_ms: float = 0.0


@dataclass
class RecommenderConfig:
    """推荐器配置"""
    # 维度权重
    w_global_quality: float = 0.2      # 全局贤者质量权重
    w_topic_relevance: float = 0.3     # 主题关联权重
    w_user_preference: float = 0.25    # 用户偏好权重
    w_time_pattern: float = 0.05       # 时间模式权重
    w_diversity: float = 0.1           # 多样性权重
    w_recency: float = 0.1             # 时效性权重
    # 输出控制
    top_k: int = 5                     # 默认返回数量
    max_candidates: int = 50           # 最大候选数
    min_score_threshold: float = 0.05  # 最低分数阈值
    diversity_penalty: float = 0.3     # 学派重复惩罚系数
    cold_start_default: str = "孔子"   # 冷启动默认贤者
    # 解释
    explain: bool = True               # 是否生成推荐理由


class SageRecommender:
    """智能贤者推荐器

    基于PatternLearner学习到的模式，为用户查询推荐最合适的贤者。

    推荐策略:
    1. hybrid（默认）: 多维度加权融合
    2. content_based: 基于内容主题匹配
    3. collaborative: 基于用户画像
    4. popularity: 基于全局质量排名

    示例:
        recommender = SageRecommender(learner)
        result = recommender.recommend("什么是仁义道德", user_id="user_123")
        for rec in result.recommendations:
            logger.info(f"{rec.sage_name}: {rec.score:.2f} - {', '.join(rec.reasons)}")
    """

    def __init__(
        self,
        learner: Optional[PatternLearner] = None,
        config: Optional[RecommenderConfig] = None,
    ):
        self.learner = learner or PatternLearner()
        self.config = config or RecommenderConfig()
        # 推荐效果追踪
        self._recommendation_history: List[Dict[str, Any]] = []
        self._recommendation_feedback: List[Dict[str, Any]] = []

    def recommend(
        self,
        query: str,
        user_id: str = "",
        top_k: Optional[int] = None,
        strategy: str = "hybrid",
        excluded_sages: Optional[Set[str]] = None,
    ) -> RecommendationResult:
        """生成推荐

        Args:
            query: 用户查询
            user_id: 用户ID
            top_k: 返回数量（None用配置默认值）
            strategy: 推荐策略
            excluded_sages: 排除的贤者

        Returns:
            RecommendationResult
        """
        start = datetime.now()
        # ★ v1.2 修复: top_k=0 是合法值（表示不返回结果），不应被替换为默认值
        top_k = self.config.top_k if top_k is None else top_k
        excluded = excluded_sages or set()
        candidates: Dict[str, Dict[str, float]] = {}

        # 根据策略计算候选分
        if strategy == "hybrid":
            candidates = self._score_hybrid(query, user_id)
        elif strategy == "content_based":
            candidates = self._score_content_based(query)
        elif strategy == "collaborative":
            candidates = self._score_collaborative(user_id)
        elif strategy == "popularity":
            candidates = self._score_popularity()
        else:
            candidates = self._score_hybrid(query, user_id)

        # 移除排除项
        for sage in excluded:
            candidates.pop(sage, None)

        # 冷启动检查
        if not candidates:
            return self._cold_start_recommend(query, user_id, top_k, strategy)

        # 多样性调整
        candidates = self._apply_diversity(candidates, top_k)

        # 排序并取TopK
        sorted_candidates = sorted(
            candidates.items(),
            key=lambda x: sum(x[1].values()),
            reverse=True,
        )

        # 构建推荐结果
        recommendations = []
        for sage_name, dims in sorted_candidates[:top_k]:
            total = sum(dims.values())
            if total < self.config.min_score_threshold:
                continue

            rec = Recommendation(
                sage_name=sage_name,
                score=min(1.0, total),
                dimensions=dims,
            )

            # 生成推荐理由
            if self.config.explain:
                rec.reasons = self._generate_reasons(sage_name, query, user_id, dims)

            recommendations.append(rec)

        elapsed = (datetime.now() - start).total_seconds() * 1000

        # 追踪推荐历史
        self._recommendation_history.append({
            "query": query,
            "user_id": user_id,
            "strategy": strategy,
            "recommendations": [(r.sage_name, r.score) for r in recommendations],
            "timestamp": datetime.now().isoformat(),
        })

        return RecommendationResult(
            recommendations=recommendations,
            query=query,
            user_id=user_id,
            strategy=strategy,
            total_candidates=len(candidates),
            elapsed_ms=round(elapsed, 1),
        )

    def record_feedback(
        self,
        query: str,
        user_id: str,
        recommended_sage: str,
        accepted: bool,
        actual_rating: Optional[int] = None,
    ) -> None:
        """记录推荐反馈（用于追踪推荐效果）

        Args:
            query: 原始查询
            user_id: 用户ID
            recommended_sage: 推荐的贤者
            accepted: 用户是否接受了推荐
            actual_rating: 实际评分（1-5）
        """
        self._recommendation_feedback.append({
            "query": query,
            "user_id": user_id,
            "recommended_sage": recommended_sage,
            "accepted": accepted,
            "actual_rating": actual_rating,
            "timestamp": datetime.now().isoformat(),
        })

    # ─────────────────────────────────────────
    # 评分策略
    # ─────────────────────────────────────────

    def _score_hybrid(self, query: str, user_id: str) -> Dict[str, Dict[str, float]]:
        """混合评分（多维度加权融合）"""
        candidates: Dict[str, Dict[str, float]] = {}

        # 1. 全局质量
        for sage_name, quality in self.learner._sage_quality.items():
            if quality["total"] > 0:
                score = quality["strength"] * self.config.w_global_quality
                if sage_name not in candidates:
                    candidates[sage_name] = {}
                candidates[sage_name]["quality"] = score

        # 2. 主题关联
        topics = self.learner._extract_topics(query)
        for topic in topics:
            assocs = self.learner.get_topic_associations(topic, top_k=10)
            for a in assocs:
                if a.strength > 0:
                    if a.sage_name not in candidates:
                        candidates[a.sage_name] = {}
                    current = candidates[a.sage_name].get("topic", 0)
                    candidates[a.sage_name]["topic"] = max(current, a.strength * self.config.w_topic_relevance)

        # 3. 用户偏好
        if user_id:
            profile = self.learner.get_user_profile(user_id)
            if profile:
                for sage_name, pref in profile.preferred_sages.items():
                    if pref > 0:
                        if sage_name not in candidates:
                            candidates[sage_name] = {}
                        candidates[sage_name]["user_pref"] = abs(pref) * self.config.w_user_preference

        # 4. 时间模式
        hour = datetime.now().hour
        tp = self.learner._time_patterns.get(hour)
        if tp and tp.usage_count > 3:
            for sage_name, count in tp.preferred_sages.items():
                if sage_name not in candidates:
                    candidates[sage_name] = {}
                candidates[sage_name]["time"] = (count / tp.usage_count) * self.config.w_time_pattern

        # 5. 时效性（最近活跃的贤者加分）
        for sage_name, quality in self.learner._sage_quality.items():
            if quality["total"] > 0 and sage_name in candidates:
                # 高评分的贤者如果近期有好评，加分
                if quality["avg_rating"] >= 4.0:
                    current = candidates[sage_name].get("recency", 0)
                    candidates[sage_name]["recency"] = max(current, 0.05 * self.config.w_recency)

        return candidates

    def _score_content_based(self, query: str) -> Dict[str, Dict[str, float]]:
        """基于内容的评分"""
        candidates: Dict[str, Dict[str, float]] = {}
        topics = self.learner._extract_topics(query)

        for topic in topics:
            assocs = self.learner.get_topic_associations(topic, top_k=15)
            for a in assocs:
                if a.sage_name not in candidates:
                    candidates[a.sage_name] = {}
                current = candidates[a.sage_name].get("topic", 0)
                candidates[a.sage_name]["topic"] = max(current, a.strength)

        # 关键词直接匹配贤者名
        for sage_name in self.learner._sage_quality:
            if sage_name in query or any(
                kw in query for kw in self.learner._topic_vocabulary.get(sage_name, set())
            ):
                if sage_name not in candidates:
                    candidates[sage_name] = {}
                candidates[sage_name]["name_match"] = 0.8

        return candidates

    def _score_collaborative(self, user_id: str) -> Dict[str, Dict[str, float]]:
        """基于用户画像的评分"""
        candidates: Dict[str, Dict[str, float]] = {}
        profile = self.learner.get_user_profile(user_id)

        if not profile:
            return candidates

        for sage_name, pref in profile.preferred_sages.items():
            if pref > 0:
                candidates[sage_name] = {"user_pref": abs(pref)}

        # 协同过滤：相似用户的偏好
        for other_id, other_profile in self.learner._user_profiles.items():
            if other_id == user_id:
                continue
            similarity = self._user_similarity(profile, other_profile)
            if similarity > 0.3:
                for sage_name, pref in other_profile.preferred_sages.items():
                    if pref > 0 and sage_name not in candidates:
                        candidates[sage_name] = {
                            "collaborative": pref * similarity * 0.5
                        }

        return candidates

    def _score_popularity(self) -> Dict[str, Dict[str, float]]:
        """基于全局质量的评分"""
        candidates: Dict[str, Dict[str, float]] = {}

        for sage_name, quality in self.learner._sage_quality.items():
            if quality["total"] > 0:
                candidates[sage_name] = {"popularity": quality["strength"]}

        return candidates

    # ─────────────────────────────────────────
    # 多样性与冷启动
    # ─────────────────────────────────────────

    def _apply_diversity(self, candidates: Dict[str, Dict[str, float]], top_k: int) -> Dict[str, Dict[str, float]]:
        """应用多样性惩罚（避免推荐同学派贤者过多）"""
        # 学派映射（简化版，实际应从YAML配置中获取）
        school_map = {
            "孔子": "儒家", "孟子": "儒家", "荀子": "儒家", "朱熹": "儒家", "王阳明": "儒家", "二程": "儒家",
            "老子": "道家", "庄子": "道家", "列子": "道家",
            "韩非子": "法家", "商鞅": "法家", "李斯": "法家",
            "孙子": "兵家", "孙膑": "兵家", "吴起": "兵家",
            "墨子": "墨家",
            "管仲": "杂家",
            "白居易": "文学", "李白": "文学", "杜甫": "文学", "苏轼": "文学",
        }

        school_counts: Dict[str, int] = defaultdict(int)
        penalty = self.config.diversity_penalty

        for sage_name in list(candidates.keys()):
            school = school_map.get(sage_name, "")
            # ★ v1.2 修复: 只对已知学派的贤者应用多样性惩罚，避免空学派键无限增长
            if school and school_counts[school] >= 2:
                # 已有2个同学派推荐，对后续的进行惩罚
                total = sum(candidates[sage_name].values())
                candidates[sage_name]["diversity"] = -total * penalty * school_counts[school]
            if school:
                school_counts[school] += 1

        return candidates

    def _cold_start_recommend(self, query: str, user_id: str, top_k: int, strategy: str = "cold_start") -> RecommendationResult:
        """冷启动推荐（无学习数据时的兜底）"""
        default = self.config.cold_start_default

        # 基于查询关键词的简单匹配
        keywords = self.learner._extract_keywords(query)

        # 简单的学派关键词匹配
        school_keywords = {
            "儒家": {"仁", "礼", "德", "君子", "孝", "义", "论语", "孔子", "孟子"},
            "道家": {"道", "无为", "自然", "逍遥", "老子", "庄子", "道德经"},
            "法家": {"法", "术", "势", "法治", "韩非", "商鞅"},
            "兵家": {"兵", "战", "谋略", "孙子", "兵法", "战略"},
            "墨家": {"兼爱", "非攻", "墨子", "尚贤"},
            "佛学": {"佛", "禅", "菩提", "涅槃", "般若"},
            "文学": {"诗", "词", "赋", "文", "小说", "文学"},
        }

        school_to_sage = {
            "儒家": ["孔子", "孟子", "荀子"],
            "道家": ["老子", "庄子"],
            "法家": ["韩非子", "商鞅"],
            "兵家": ["孙子", "孙膑"],
            "墨家": ["墨子"],
            "佛学": ["惠能", "玄奘"],
            "文学": ["白居易", "苏轼", "李白"],
        }

        recommendations = []
        matched_schools = set()

        for kw in keywords:
            for school, kws in school_keywords.items():
                if kw in kws and school not in matched_schools:
                    matched_schools.add(school)
                    for sage in school_to_sage.get(school, []):
                        recommendations.append(Recommendation(
                            sage_name=sage,
                            score=0.5,
                            reasons=[f"关键词'{kw}'匹配{school}学派"],
                            is_cold_start=True,
                        ))
                    break

        # 兜底
        if not recommendations:
            recommendations.append(Recommendation(
                sage_name=default,
                score=0.3,
                reasons=["默认推荐（冷启动模式）"],
                is_cold_start=True,
            ))

        # ★ v1.2 修复: 冷启动推荐结果也记录到历史中
        self._recommendation_history.append({
            "query": query,
            "user_id": user_id,
            "strategy": "cold_start",
            "recommendations": [(r.sage_name, r.score) for r in recommendations],
            "timestamp": datetime.now().isoformat(),
        })

        return RecommendationResult(
            recommendations=recommendations[:top_k],
            query=query,
            user_id=user_id,
            strategy="cold_start",
            total_candidates=len(recommendations),
        )

    # ─────────────────────────────────────────
    # 推荐理由生成
    # ─────────────────────────────────────────

    def _generate_reasons(
        self,
        sage_name: str,
        query: str,
        user_id: str,
        dims: Dict[str, float],
    ) -> List[str]:
        """生成推荐理由"""
        reasons = []

        if "topic" in dims and dims["topic"] > 0.1:
            topics = self.learner._extract_topics(query)
            if topics:
                reasons.append(f"主题'{topics[0]}'与{sage_name}高度关联")
            else:
                reasons.append(f"查询内容与{sage_name}的专业领域匹配")

        if "user_pref" in dims and dims["user_pref"] > 0.05:
            reasons.append(f"基于您的历史偏好（您之前对{sage_name}评价较高）")

        if "quality" in dims and dims["quality"] > 0.1:
            quality = self.learner.get_sage_quality(sage_name)
            avg = quality.get("avg_rating", 0)
            if avg >= 4.0:
                reasons.append(f"{sage_name}综合评分较高（平均{avg:.1f}/5.0）")

        if "time" in dims and dims["time"] > 0.02:
            reasons.append("此时段{sage_name}的回答质量通常较好")

        if "name_match" in dims and dims["name_match"] > 0.1:
            reasons.append(f"您明确提到了{sage_name}")

        if "diversity" in dims and dims["diversity"] < 0:
            reasons.append("为您提供不同视角的参考")

        if not reasons:
            reasons.append("综合评分推荐")

        return reasons

    # ─────────────────────────────────────────
    # 协同过滤辅助
    # ─────────────────────────────────────────

    @staticmethod
    def _user_similarity(a: UserPreference, b: UserPreference) -> float:
        """计算两个用户的余弦相似度"""
        all_sages = set(a.preferred_sages.keys()) | set(b.preferred_sages.keys())
        if not all_sages:
            return 0.0

        dot = sum(
            a.preferred_sages.get(s, 0) * b.preferred_sages.get(s, 0)
            for s in all_sages
        )
        norm_a = math.sqrt(sum(v ** 2 for v in a.preferred_sages.values()))
        norm_b = math.sqrt(sum(v ** 2 for v in b.preferred_sages.values()))

        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    # ─────────────────────────────────────────
    # 统计与评估
    # ─────────────────────────────────────────

    def get_recommendation_stats(self) -> Dict[str, Any]:
        """获取推荐统计"""
        total_recs = len(self._recommendation_history)
        total_feedback = len(self._recommendation_feedback)

        acceptance_rate = 0.0
        if total_feedback > 0:
            accepted = sum(1 for f in self._recommendation_feedback if f["accepted"])
            acceptance_rate = accepted / total_feedback

        avg_rating = 0.0
        rated = [f["actual_rating"] for f in self._recommendation_feedback if f.get("actual_rating")]
        if rated:
            avg_rating = sum(rated) / len(rated)

        # 最常推荐的贤者
        sage_counts: Dict[str, int] = defaultdict(int)
        for rec in self._recommendation_history:
            for sage, _ in rec["recommendations"]:
                sage_counts[sage] += 1

        top_recommended = sorted(sage_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_recommendations": total_recs,
            "total_feedback": total_feedback,
            "acceptance_rate": round(acceptance_rate, 3),
            "avg_actual_rating": round(avg_rating, 2) if rated else 0,
            "top_recommended_sages": top_recommended,
        }

    def get_feedback_summary(self, last_n: int = 50) -> Dict[str, Any]:
        """获取最近的推荐反馈摘要"""
        recent = self._recommendation_feedback[-last_n:]

        if not recent:
            return {"message": "No feedback data yet"}

        by_sage: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"accepted": 0, "rejected": 0, "total": 0, "avg_rating": 0})
        for f in recent:
            sage = f["recommended_sage"]
            by_sage[sage]["total"] += 1
            if f["accepted"]:
                by_sage[sage]["accepted"] += 1
            if f.get("actual_rating"):
                ratings = by_sage[sage].get("_ratings", [])
                ratings.append(f["actual_rating"])
                by_sage[sage]["_ratings"] = ratings
                by_sage[sage]["avg_rating"] = sum(ratings) / len(ratings)

        # 清理内部字段
        for sage, stats in by_sage.items():
            stats.pop("_ratings", None)

        return {
            "period": f"last {len(recent)} feedbacks",
            "by_sage": dict(sorted(by_sage.items(), key=lambda x: x[1]["total"], reverse=True)),
        }


__all__ = [
    'SageRecommender',
    'Recommendation',
    'RecommendationResult',
    'RecommenderConfig',
]
