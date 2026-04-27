# -*- coding: utf-8 -*-
"""自然参与系统 - 数据类定义"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

__all__ = [
    'add_behavior_event',
    'add_interaction',
    'get_engagement_score',
    'get_recent_behaviors',
    'is_expired',
    'update_cognitive_load',
]

@dataclass
class Reminder:
    """提醒"""
    id: str
    type: str  # ReminderType
    priority: str  # ReminderPriority
    title: str
    content: str
    action_text: Optional[str] = None
    action_url: Optional[str] = None
    dismissible: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

@dataclass
class PersonalizationRule:
    """个性化规则"""
    rule_id: str
    condition: Dict[str, Any]
    action: str
    priority: int = 0
    enabled: bool = True

@dataclass
class UserDataProfile:
    """用户数据画像"""
    user_id: str
    behavior_data: Dict[str, Any] = field(default_factory=dict)
    behavior_sequence: List[Dict] = field(default_factory=list)
    multimodal_data: Dict[str, Any] = field(default_factory=dict)
    emotional_signals: Dict[str, Any] = field(default_factory=dict)
    context_data: Dict[str, Any] = field(default_factory=dict)
    external_factors: Dict[str, Any] = field(default_factory=dict)
    unified_representation: Dict[str, Any] = field(default_factory=dict)

    def add_behavior_event(self, event_type: str, event_data: Dict, timestamp: Optional[datetime] = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.behavior_sequence.append({
            "type": event_type,
            "data": event_data,
            "timestamp": timestamp.isoformat()
        })

    def get_recent_behaviors(self, hours: int = 24) -> List[Dict]:
        cutoff = datetime.now() - timedelta(hours=hours)
        return [b for b in self.behavior_sequence
                if datetime.fromisoformat(b["timestamp"]) > cutoff]

@dataclass
class UserDynamicProfile:
    """动态用户画像"""
    user_id: str
    static_tags: Dict[str, Any] = field(default_factory=dict)
    dynamic_tags: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    engagement_history: List[Dict] = field(default_factory=list)
    learning_progress: Dict[str, float] = field(default_factory=dict)
    cognitive_load: float = 0.0
    emotional_state: str = "neutral"
    last_interaction: Optional[datetime] = None

    def add_interaction(self, interaction_type: str, quality_score: float):
        self.engagement_history.append({
            "type": interaction_type,
            "quality_score": quality_score,
            "timestamp": datetime.now().isoformat()
        })

    def update_cognitive_load(self, load: float):
        self.cognitive_load = max(0.0, min(1.0, load))

    def get_engagement_score(self) -> float:
        if not self.engagement_history:
            return 0.5
        return sum(e.get("quality_score", 0.5) for e in self.engagement_history[-10:]) / min(10, len(self.engagement_history))
