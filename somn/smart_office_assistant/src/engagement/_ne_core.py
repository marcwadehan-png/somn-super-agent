# -*- coding: utf-8 -*-
"""自然参与系统 - 核心系统"""

from typing import Dict, List, Any, Optional

__all__ = [
    'get_personalization_rules',
    'get_personalized_recommendations',
    'update_user_preference',
]

class NaturalEngagementSystem:
    """
    自然参与系统 - 支持千人千面智能化

    提供有价值的提醒和个性化体验,而非打扰式的推送
    """

    def __init__(self):
        self.reminders: Dict[str, List] = {}
        self.personalization_rules: List = []
        self.user_preferences: Dict[str, Dict[str, Any]] = {}
        self.reminder_history: Dict[str, List[Dict]] = {}

        # 千人千面核心组件
        self.cognitive_profiles: Dict[str, Any] = {}
        self.user_behavior_patterns: Dict[str, Dict[str, Any]] = {}
        self.data_profiles: Dict[str, Any] = {}
        self.dynamic_profiles: Dict[str, Any] = {}
        self.cross_scene_contexts: Dict[str, Any] = {}
        self.personalization_engines: Dict[str, Any] = {}

        self._initialize_default_rules()
        self._initialize_thousand_faces_system()

    def _initialize_thousand_faces_system(self):
        """初始化千人千面系统"""
        from ._ne_profiles import PersonalizationEngine
        self.default_engine = PersonalizationEngine(
            engine_id="default_engine",
            multimodal_enabled=True,
            reasoning_enabled=True,
            generation_enabled=True,
            reinforcement_learning_enabled=True,
            ab_testing_enabled=True,
            user_control_enabled=True
        )

    def _initialize_default_rules(self):
        """初始化默认个性化规则"""
        from ._ne_dataclasses import PersonalizationRule
        self.personalization_rules = [
            PersonalizationRule(
                rule_id="new_user_onboarding",
                condition={"user_days": "< 7", "feature_usage": "< 3"},
                action="show_onboarding_tips",
                priority=10
            ),
            PersonalizationRule(
                rule_id="engaged_user_advanced",
                condition={"usage_days": "> 30", "engagement_score": "> 0.7"},
                action="show_advanced_features",
                priority=8
            ),
        ]

    def get_personalization_rules(self) -> List:
        """获取个性化规则"""
        return self.personalization_rules

    def update_user_preference(self, user_id: str, key: str, value: Any):
        """更新用户偏好"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        self.user_preferences[user_id][key] = value

    def get_personalized_recommendations(self, user_id: str,
                                        user_behavior: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取个性化推荐"""
        recommendations = []

        # 基于使用时长推荐
        usage_days = user_behavior.get("usage_days", 0)
        feature_count = user_behavior.get("features_used", 0)

        if usage_days < 7 and feature_count < 3:
            recommendations.append({
                "type": "onboarding",
                "title": "新手指引",
                "content": "建议您先尝试这3个核心功能",
                "priority": "high"
            })

        return recommendations
