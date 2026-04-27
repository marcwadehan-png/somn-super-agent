# ClawContext - 完整上下文能力
# v1.0.0: 每个Claw独立的完整上下文
# 系统级 + 会话级 + Claw级 + 环境

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from ._claw_engine import ClawIndependentWorker

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 上下文类型枚举
# ═══════════════════════════════════════════════════════════════════

class ContextLevel(Enum):
    """上下文级别"""
    SYSTEM = "system"        # 系统级
    SESSION = "session"    # 会话级
    CLAW = "claw"           # Claw级
    USER = "user"           # 用户级


# ═══════════════════════════════════════════════════════════════════
# 系统级上下文
# ═══════════════════════════════════════════════════════════════════

@dataclass
class SystemContext:
    """
    系统级上下文
    
    包含：
    - 时间（当前时间、时段）
    - 地点（时区）
    - 系统信息
    """
    current_time: str = ""           # ISO格式时间
    current_date: str = ""          # YYYY-MM-DD
    timezone: str = "Asia/Shanghai"  # 时区
    hour: int = 0                    # 小时 0-23
    season: str = ""                 # 季节
    weekday: str = ""                # 星期几
    
    @classmethod
    def create(cls) -> "SystemContext":
        """创建系统上下文"""
        now = datetime.now()
        hour = now.hour
        
        # 时段
        if 5 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 14:
            period = "noon"
        elif 14 <= hour < 18:
            period = "afternoon"
        elif 18 <= hour < 22:
            period = "evening"
        else:
            period = "night"
        
        # 季节
        month = now.month
        if month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        elif month in [9, 10, 11]:
            season = "autumn"
        else:
            season = "winter"
        
        return cls(
            current_time=now.isoformat(),
            current_date=now.strftime("%Y-%m-%d"),
            hour=hour,
            season=season,
            weekday=now.strftime("%A")
        )
    
    def get_greeting(self) -> str:
        """根据时段获取问候语"""
        if self.hour < 6:
            return "夜深了"
        elif self.hour < 9:
            return "早上好"
        elif self.hour < 12:
            return "上午好"
        elif self.hour < 14:
            return "中午好"
        elif self.hour < 18:
            return "下午好"
        elif self.hour < 22:
            return "晚上好"
        else:
            return "夜深了"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "time": self.current_time,
            "date": self.current_date,
            "timezone": self.timezone,
            "hour": self.hour,
            "season": self.season,
            "weekday": self.weekday,
            "greeting": self.get_greeting()
        }


# ═══════════════════════════════════════════════════════════════════
# 会话级上下文
# ═══════════════════════════════════════════════════════════════════

@dataclass
class SessionContext:
    """
    会话级上下文
    
    包含：
    - 会话ID
    - 对话历史
    - 用户信息
    - 偏好设置
    """
    session_id: str = ""
    history: List[Dict[str, str]] = field(default_factory=list)  # [{"role": "user/assistant", "content": "..."}]
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    current_topic: str = ""
    session_start: str = ""
    
    def add_message(self, role: str, content: str) -> None:
        """添加消息"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_history_summary(self, max_messages: int = 5) -> str:
        """获取历史摘要"""
        recent = self.history[-max_messages:]
        return "\n".join([
            f"[{m['role']}]: {m['content'][:50]}..."
            for m in recent
        ])
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "history_count": len(self.history),
            "current_topic": self.current_topic,
            "recent_summary": self.get_history_summary(3)
        }


# ═══════════════════════════════════════════════════════════════════
# 用户级上下文
# ═══════════════════════════════════════════════════════════════════

@dataclass
class UserContext:
    """
    用户级上下文
    
    包含：
    - 用户信息
    - 偏好
    - 历史交互
    """
    user_id: str = ""
    user_name: str = ""
    user_level: str = "normal"  # beginner/normal/expert
    interests: List[str] = field(default_factory=list)
    interaction_count: int = 0
    last_interaction: str = ""
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    
    def update_interaction(self) -> None:
        """更新交互计数"""
        self.interaction_count += 1
        self.last_interaction = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "level": self.user_level,
            "interests": self.interests,
            "interaction_count": self.interaction_count,
            "preferences": self.user_preferences
        }


# ═══════════════════════════════════════════════════════════════════
# Claw级上下文
# ═══════════════════════════════════════════════════════════════════

@dataclass
class ClawContext:
    """
    Claw级上下文
    
    包含：
    - Claw名称/ID
    - 当前状态
    - 独立记忆
    - 协作历史
    """
    claw_name: str = ""
    status: str = "idle"
    activated_count: int = 0
    last_activation: str = ""
    memory_snapshot: Dict[str, Any] = field(default_factory=dict)
    collaboration_history: List[Dict[str, str]] = field(default_factory=list)
    
    def update_activation(self) -> None:
        """更新激活"""
        self.activated_count += 1
        self.last_activation = datetime.now().isoformat()
    
    def add_collaboration(self, collaborator: str, topic: str) -> None:
        """添加协作记录"""
        self.collaboration_history.append({
            "collaborator": collaborator,
            "topic": topic,
            "timestamp": datetime.now().isoformat()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "claw_name": self.claw_name,
            "status": self.status,
            "activated": self.activated_count,
            "memory_snapshot": self.memory_snapshot,
            "collaboration_count": len(self.collaboration_history)
        }


# ═══════════════════════════════════════════════════════════════════
# 完整上下文容器
# ═══════════════════════════════════════════════════════════════════

class ClawContextContainer:
    """
    完整上下文容器
    
    整合所有级别上下文，为Claw提供完整上下文能力
    """
    
    def __init__(self, claw_name: str):
        self.claw_name = claw_name
        
        # 各级别上下文
        self.system = SystemContext.create()
        self.session = SessionContext()
        self.user = UserContext()
        self.claw = ClawContext(claw_name=claw_name)
        
        # 环境变量（Lazy load）
        self._env_vars: Optional[Dict[str, str]] = None
        
        logger.info(f"[ClawContext] {claw_name} 上下文容器初始化")
    
    # ── 系统级访问 ──
    
    def get_system_context(self) -> Dict[str, Any]:
        """获取系统上下文"""
        return self.system.to_dict()
    
    def get_time_context(self) -> Dict[str, Any]:
        """获取时间相关上下文"""
        return {
            "hour": self.system.hour,
            "greeting": self.system.get_greeting(),
            "season": self.system.season,
            "weekday": self.system.weekday
        }
    
    # ── 会话级访问 ──
    
    def set_session(
        self,
        session_id: str,
        current_topic: str = ""
    ) -> None:
        """设置会话"""
        self.session.session_id = session_id
        self.session.current_topic = current_topic
        self.session.session_start = datetime.now().isoformat()
    
    def add_user_message(self, content: str) -> None:
        """添加用户消息"""
        self.session.add_message("user", content)
    
    def add_assistant_message(self, content: str) -> None:
        """添加助手消息"""
        self.session.add_message("assistant", content)
    
    def get_session_context(self) -> Dict[str, Any]:
        """��取会话上下文"""
        return self.session.to_dict()
    
    # ── 用户级访问 ──
    
    def set_user(
        self,
        user_id: str,
        user_name: str = "",
        level: str = "normal"
    ) -> None:
        """设置用户"""
        self.user.user_id = user_id
        self.user.user_name = user_name
        self.user.user_level = level
    
    def update_preference(self, key: str, value: Any) -> None:
        """更新偏好"""
        self.user.user_preferences[key] = value
    
    def get_user_context(self) -> Dict[str, Any]:
        """获取用户上下文"""
        context = self.user.to_dict()
        context["preferences"] = self.user.user_preferences
        return context
    
    # ── Claw级访问 ──
    
    def update_claw_state(
        self,
        status: Optional[str] = None,
        memory_snapshot: Optional[Dict[str, Any]] = None
    ) -> None:
        """更新Claw状态"""
        if status:
            self.claw.status = status
        if memory_snapshot:
            self.claw.memory_snapshot = memory_snapshot
        self.claw.update_activation()
    
    def add_collaboration_record(
        self,
        collaborator: str,
        topic: str
    ) -> None:
        """添加协作记录"""
        self.claw.add_collaboration(collaborator, topic)
    
    def get_claw_context(self) -> Dict[str, Any]:
        """获取Claw上下文"""
        return self.claw.to_dict()
    
    # ── 环境变量访问 ──
    
    def get_env(self, key: str, default: str = "") -> str:
        """获取环境变量"""
        if self._env_vars is None:
            self._load_env_vars()
        return self._env_vars.get(key, default)
    
    def get_env_int(self, key: str, default: int = 0) -> int:
        """获取整型环境变量"""
        try:
            return int(self.get_env(key, str(default)))
        except ValueError:
            return default
    
    def get_env_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔环境变量"""
        val = self.get_env(key, str(default)).lower()
        return val in ("true", "1", "yes", "on")
    
    def _load_env_vars(self) -> None:
        """加载环境变量（OPENCLAW_前缀）"""
        self._env_vars = {}
        for key, value in os.environ.items():
            if key.startswith("OPENCLAW_"):
                self._env_vars[key] = value
            elif key.startswith("CLAW_"):
                self._env_vars[key] = value
    
    # ── 完整上下文 ──
    
    def get_full_context(
        self,
        include_history: bool = False
    ) -> Dict[str, Any]:
        """
        获取完整上下文
        
        Args:
            include_history: 是否包含对话历史
            
        Returns:
            Dict: 完整上下文
        """
        context = {
            # 系统级
            "system": self.system.to_dict(),
            # 时间
            "time": self.get_time_context(),
            # 用户级
            "user": self.get_user_context(),
            # Claw级
            "claw": self.get_claw_context(),
            # 环境变量（敏感信息过滤）
            "env": {
                k: v for k, v in self._env_vars.items()
                if not any(s in k.lower() for s in ["secret", "key", "token", "password"])
            } if self._env_vars else {}
        }
        
        # 会话级（可选择是否包含历史）
        if include_history:
            context["session"] = self.session.to_dict()
        else:
            context["session"] = {
                "session_id": self.session.session_id,
                "current_topic": self.session.current_topic,
                "history_count": len(self.session.history)
            }
        
        return context
    
    def build_system_prompt(
        self,
        query: str,
        style: str = "default"
    ) -> str:
        """
        构建系统提示词
        
        Args:
            query: 用户查询
            style: 响应风格
            
        Returns:
            str: 格式化提示词
        """
        context = self.get_full_context(include_history=False)
        
        prompt = f"""## 当前上下文

### 系统信息
- 时间: {context['time']['greeting']}
- 星期: {context['system']['weekday']}
- 季节: {context['system']['season']}

### Claw信息
- 名称: {context['claw']['claw_name']}
- 激活次数: {context['claw']['activated']}
- 状态: {context['claw']['status']}

### 用户信息
- 用户: {context['user']['user_name'] or '未知'}
- 级别: {context['user']['level']}
- 交互次数: {context['user']['interaction_count']}

## 当前查询
{query}

## 响应要求
- 风格: {style}
- 注意结合上下文提供个性化响应
"""
        return prompt


# ═══════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════

__all__ = [
    "ContextLevel",
    "SystemContext",
    "SessionContext",
    "UserContext",
    "ClawContext",
    "ClawContextContainer",
]