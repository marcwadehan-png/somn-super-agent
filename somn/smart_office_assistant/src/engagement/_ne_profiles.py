# -*- coding: utf-8 -*-
"""自然参与系统 - 用户画像模块"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

__all__ = [
    'add_cognitive_load',
    'add_transition',
    'get_avg_cognitive_load',
    'get_scene_pattern',
]

@dataclass
class CrossSceneContext:
    """跨场景上下文"""
    user_id: str
    current_scene: str = ""
    previous_scene: str = ""
    scene_transitions: List[Dict] = field(default_factory=list)
    shared_context: Dict[str, Any] = field(default_factory=dict)
    last_update: datetime = field(default_factory=datetime.now)

    def add_transition(self, from_scene: str, to_scene: str, trigger: str = ""):
        self.previous_scene = self.current_scene
        self.current_scene = to_scene
        self.scene_transitions.append({
            "from": from_scene,
            "to": to_scene,
            "trigger": trigger,
            "timestamp": datetime.now().isoformat()
        })
        self.last_update = datetime.now()

    def get_scene_pattern(self, hours: int = 24) -> List[str]:
        cutoff = datetime.now() - timedelta(hours=hours)
        return [t["to"] for t in self.scene_transitions
                if datetime.fromisoformat(t["timestamp"]) > cutoff]

@dataclass
class PersonalizationEngine:
    """个性化引擎"""
    engine_id: str
    multimodal_enabled: bool = False
    reasoning_enabled: bool = False
    generation_enabled: bool = False
    reinforcement_learning_enabled: bool = False
    ab_testing_enabled: bool = False
    user_control_enabled: bool = False
    model_config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserCognitiveProfile:
    """用户认知画像"""
    user_id: str
    cognitive_strengths: List[str] = field(default_factory=list)
    cognitive_weaknesses: List[str] = field(default_factory=list)
    learning_preferences: Dict[str, Any] = field(default_factory=dict)
    cognitive_load_history: List[float] = field(default_factory=list)
    comprehension_levels: Dict[str, float] = field(default_factory=dict)
    interaction_complexity_tolerance: float = 0.5
    attention_span_seconds: float = 300.0
    last_profile_update: Optional[datetime] = None

    def add_cognitive_load(self, load: float):
        self.cognitive_load_history.append(load)
        if len(self.cognitive_load_history) > 100:
            self.cognitive_load_history = self.cognitive_load_history[-100:]
        self.last_profile_update = datetime.now()

    def get_avg_cognitive_load(self) -> float:
        if not self.cognitive_load_history:
            return 0.5
        return sum(self.cognitive_load_history) / len(self.cognitive_load_history)
