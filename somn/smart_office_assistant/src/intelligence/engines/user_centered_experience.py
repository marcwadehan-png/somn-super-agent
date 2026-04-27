"""
用户中心体验系统 - User-Centered Experience System
体验设计框架

版本: v1.0.0
创建: 2026-04-02
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class RogersPrinciple(Enum):
    """罗杰斯核心原则"""
    UNCONDITIONAL_POSITIVE_REGARD = "unconditional_positive_regard"
    EMPATHIC_UNDERSTANDING = "empathic_understanding"
    CONGRUENCE = "congruence"
    PERSON_CENTERED = "person_centered"

@dataclass
class UserExperienceProfile:
    """用户体验档案"""
    user_id: str
    user_name: str
    actualizing_tendency: float = 0.5
    experience_openness: float = 0.5
    psychological_needs: Dict[str, float] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class UserCenteredExperienceEngine:
    """
    用户中心体验引擎
    """
    
    def __init__(self):
        self.user_profiles: Dict[str, UserExperienceProfile] = {}
    
    def create_profile(self, user_id: str, user_name: str) -> UserExperienceProfile:
        """创建用户体验档案"""
        profile = UserExperienceProfile(user_id=user_id, user_name=user_name)
        self.user_profiles[user_id] = profile
        return profile
    
    def apply_unconditional_positive_regard(self, user_id: str, content: str) -> str:
        """应用无条件积极关注原则"""
        return f"感谢你的分享,我们理解每个人都有自己的独特需求.{content}"
    
    def apply_empathic_understanding(self, user_id: str, user_message: str) -> str:
        """应用共情理解原则"""
        return f"我能感受到{user_message[:20]}...你的感受是完全合理的."
    
    def apply_congruence(self, content: str) -> str:
        """应用真诚一致原则"""
        return f"关于这个话题,我们的真实想法是:{content}"

__all__ = ['UserCenteredExperienceEngine', 'RogersPrinciple', 'UserExperienceProfile']
