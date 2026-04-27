# -*- coding: utf-8 -*-
"""自然参与系统 - 提醒模块"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from ._ne_dataclasses import Reminder, PersonalizationRule

__all__ = [
    'create_feature_tip_impl',
    'create_reminder_impl',
    'create_value_reminder_impl',
    'get_active_reminders_impl',
    'should_send_reminder_impl',
]

def should_send_reminder_impl(core, user_id: str, reminder: Reminder) -> bool:
    """检查是否应该发送提醒"""
    prefs = core.user_preferences.get(user_id, {})

    # 检查全局免打扰
    if prefs.get("do_not_disturb", False):
        return False

    # 检查免打扰时段
    now = datetime.now()
    quiet_start = prefs.get("quiet_hours_start", 22)
    quiet_end = prefs.get("quiet_hours_end", 8)
    current_hour = now.hour

    if quiet_start <= quiet_end:
        if quiet_start <= current_hour or current_hour < quiet_end:
            return False
    else:
        if quiet_end <= current_hour < quiet_start:
            return False

    # 检查提醒类型偏好
    allowed_types = prefs.get("reminder_types", [])
    if allowed_types and reminder.type not in allowed_types:
        return False

    # 检查频率限制
    frequency = prefs.get("reminder_frequency", "medium")
    if frequency == "off":
        return False

    # 检查是否过期
    if reminder.is_expired():
        return False

    return True

def create_reminder_impl(core, user_id: str, reminder: Reminder) -> bool:
    """创建提醒"""
    if not should_send_reminder_impl(core, user_id, reminder):
        return False

    if user_id not in core.reminders:
        core.reminders[user_id] = []

    core.reminders[user_id].append(reminder)

    # 记录历史
    if user_id not in core.reminder_history:
        core.reminder_history[user_id] = []

    core.reminder_history[user_id].append({
        "reminder_id": reminder.id,
        "type": reminder.type,
        "title": reminder.title,
        "sent_at": datetime.now().isoformat()
    })

    return True

def create_value_reminder_impl(core, user_id: str, milestone_name: str,
                              value_message: str) -> bool:
    """创建价值提醒"""
    from ._ne_dataclasses import Reminder
    from ._ne_enums import ReminderType, ReminderPriority

    reminder = Reminder(
        id=f"value_{datetime.now().timestamp()}",
        type=ReminderType.VALUE.value,
        priority=ReminderPriority.HIGH.value,
        title="恭喜达成新成就!",
        content=value_message,
        dismissible=True,
        expires_at=datetime.now() + timedelta(days=7)
    )

    return create_reminder_impl(core, user_id, reminder)

def create_feature_tip_impl(core, user_id: str, feature_name: str,
                            tip_content: str, action_text: str = "试试看") -> bool:
    """创建功能提示"""
    from ._ne_dataclasses import Reminder
    from ._ne_enums import ReminderType, ReminderPriority

    reminder = Reminder(
        id=f"feature_{datetime.now().timestamp()}",
        type=ReminderType.FEATURE.value,
        priority=ReminderPriority.MEDIUM.value,
        title=f"功能提示:{feature_name}",
        content=tip_content,
        action_text=action_text,
        dismissible=True,
        expires_at=datetime.now() + timedelta(days=3)
    )

    return create_reminder_impl(core, user_id, reminder)

def get_active_reminders_impl(core, user_id: str) -> List[Reminder]:
    """获取活跃提醒"""
    from ._ne_dataclasses import Reminder
    from ._ne_enums import ReminderPriority

    if user_id not in core.reminders:
        return []

    # 过滤掉已过期的提醒
    active = [r for r in core.reminders[user_id] if not r.is_expired()]
    core.reminders[user_id] = active

    # 按优先级排序
    priority_order = {ReminderPriority.HIGH.value: 0, ReminderPriority.MEDIUM.value: 1, ReminderPriority.LOW.value: 2}
    active.sort(key=lambda r: priority_order.get(r.priority, 3))

    return active
