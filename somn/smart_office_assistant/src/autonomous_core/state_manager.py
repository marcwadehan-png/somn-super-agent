"""
__all__ = [
    'add_topic',
    'complete_task',
    'from_dict',
    'get_current_state',
    'get_welcome_back_message',
    'increment_interactions',
    'set_mode',
    'start_task',
    'to_dict',
]

持续状态管理 - State Manager
实现智能体的持续运行能力: 会话状态持久化,当前任务追踪,上下文连续性
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from loguru import logger

class SessionStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ENDED = "ended"

class AgentMode(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    LEARNING = "learning"
    REFLECTING = "reflecting"
    WAITING = "waiting"

@dataclass
class CurrentTask:
    task_id: str = ""
    task_name: str = ""
    progress: float = 0.0
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'progress': self.progress,
            'started_at': self.started_at
        }

@dataclass
class AgentState:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    session_status: SessionStatus = SessionStatus.ACTIVE
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active_at: str = field(default_factory=lambda: datetime.now().isoformat())
    mode: AgentMode = AgentMode.IDLE
    current_task: Optional[CurrentTask] = None
    recent_topics: List[str] = field(default_factory=list)
    active_goals: List[str] = field(default_factory=list)
    total_interactions: int = 0
    
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'session_status': self.session_status.value,
            'created_at': self.created_at,
            'last_active_at': self.last_active_at,
            'mode': self.mode.value,
            'current_task': self.current_task.to_dict() if self.current_task else None,
            'recent_topics': self.recent_topics,
            'active_goals': self.active_goals,
            'total_interactions': self.total_interactions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentState':
        state = cls(
            session_id=data.get('session_id', str(uuid.uuid4())[:8]),
            session_status=SessionStatus(data.get('session_status', 'active')),
            created_at=data.get('created_at', datetime.now().isoformat()),
            last_active_at=data.get('last_active_at', datetime.now().isoformat()),
            mode=AgentMode(data.get('mode', 'idle')),
            recent_topics=data.get('recent_topics', []),
            active_goals=data.get('active_goals', []),
            total_interactions=data.get('total_interactions', 0)
        )
        if data.get('current_task'):
            t = data['current_task']
            state.current_task = CurrentTask(
                task_id=t.get('task_id', ''),
                task_name=t.get('task_name', ''),
                progress=t.get('progress', 0.0),
                started_at=t.get('started_at', datetime.now().isoformat())
            )
        return state

class StateManager:
    """状态管理器 - 管理智能体的持续状态"""
    
    def __init__(self, storage_path: str = "data/state"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._current_state: Optional[AgentState] = None
        self._load_state()
        logger.info("状态管理器init完成")
    
    def _load_state(self):
        """加载状态（空文件/损坏时优雅降级，生成新session）"""
        state_file = self.storage_path / "current_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if not content:
                    logger.info("current_state.json 为空，生成新 session")
                    self._current_state = AgentState()
                    return
                data = json.loads(content)
                self._current_state = AgentState.from_dict(data)
                logger.info(f"恢复状态: session {self._current_state.session_id}")
            except json.JSONDecodeError as e:
                logger.warning(f"current_state.json 格式损坏 ({e})，生成新 session")
                self._current_state = AgentState()
            except Exception as e:
                logger.warning(f"加载状态失败 ({e})，生成新 session")
                self._current_state = AgentState()
    
    def _save_state(self):
        if self._current_state:
            self._current_state.last_active_at = datetime.now().isoformat()
            try:
                state_file = self.storage_path / "current_state.json"
                with open(state_file, 'w', encoding='utf-8') as f:
                    json.dump(self._current_state.to_dict(), f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"保存状态失败: {e}")
    
    def get_current_state(self) -> AgentState:
        if not self._current_state:
            self._current_state = AgentState()
            self._save_state()
        return self._current_state
    
    def set_mode(self, mode: AgentMode):
        state = self.get_current_state()
        state.mode = mode
        self._save_state()
    
    def start_task(self, task_id: str, task_name: str):
        state = self.get_current_state()
        state.current_task = CurrentTask(task_id=task_id, task_name=task_name)
        state.mode = AgentMode.EXECUTING
        self._save_state()
        logger.info(f"开始任务: [{task_id}] {task_name}")
    
    def complete_task(self):
        state = self.get_current_state()
        if state.current_task:
            logger.info(f"完成任务: [{state.current_task.task_id}] {state.current_task.task_name}")
            state.current_task = None
        state.mode = AgentMode.IDLE
        self._save_state()
    
    def add_topic(self, topic: str):
        state = self.get_current_state()
        if topic not in state.recent_topics:
            state.recent_topics.insert(0, topic)
            state.recent_topics = state.recent_topics[:20]
            self._save_state()
    
    def increment_interactions(self):
        state = self.get_current_state()
        state.total_interactions += 1
        self._save_state()
    
    def get_welcome_back_message(self) -> str:
        state = self.get_current_state()
        if state.current_task:
            return f"欢迎回来.我正在进行: {state.current_task.task_name} (进度: {state.current_task.progress:.0f}%)"
        if state.recent_topics:
            return f"欢迎回来.我们上次聊到: {state.recent_topics[0]}"
        return "欢迎回来"
