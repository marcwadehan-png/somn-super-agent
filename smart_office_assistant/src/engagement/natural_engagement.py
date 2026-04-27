# -*- coding: utf-8 -*-
"""自然参与系统 - 兼容层 (v2.0)

重构后主文件仅保留向后兼容导入。
子模块: _ne_enums / _ne_dataclasses / _ne_profiles / _ne_reminders / _ne_core
"""

from ._ne_enums import (
    ReminderType,
    ReminderPriority,
    BehaviorType,
    EngagementMetric,
)
from ._ne_dataclasses import (
    Reminder,
    PersonalizationRule,
    UserDataProfile,
    UserDynamicProfile,
)
from ._ne_profiles import (
    CrossSceneContext,
    PersonalizationEngine,
    UserCognitiveProfile,
)
from ._ne_core import NaturalEngagementSystem

# 保持向后兼容 — Personalization 类定义（P6: 移除不可达的 `Personalization = None` 赋值）
class Personalization:
    """个性化配置 (v2.0 简版)"""

    def __init__(self):
        self.configs: dict = {}

    def set_config(self, user_id: str, key: str, value):
        if user_id not in self.configs:
            self.configs[user_id] = {}
        self.configs[user_id][key] = value

    def get_config(self, user_id: str, key: str, default=None):
        return self.configs.get(user_id, {}).get(key, default)

    def get_all_configs(self, user_id: str) -> dict:
        return self.configs.get(user_id, {}).copy()

__all__ = [
    "ReminderType",
    "ReminderPriority",
    "BehaviorType",
    "EngagementMetric",
    "Reminder",
    "PersonalizationRule",
    "UserDataProfile",
    "UserDynamicProfile",
    "CrossSceneContext",
    "PersonalizationEngine",
    "UserCognitiveProfile",
    "NaturalEngagementSystem",
    "Personalization",
]
