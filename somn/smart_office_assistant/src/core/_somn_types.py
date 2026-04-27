"""
__all__ = [
    'to_dict',
]

SomnCore 数据类型定义
所有 dataclass 集中管理。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

@dataclass
class SomnContext:
    """Somn 执行上下文"""
    task_id: str
    task_type: str
    industry: Optional[str] = None
    stage: Optional[str] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    intermediate_results: List[Dict[str, Any]] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    status: str = "running"

@dataclass
class WorkflowTaskRecord:
    """工作流任务状态记录."""
    task_name: str
    tool: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    expected_output: str = ""
    depends_on: List[str] = field(default_factory=list)
    rollback_tasks: List[Dict[str, Any]] = field(default_factory=list)
    max_retries: int = 0
    status: str = "queued"
    attempts: int = 0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    last_error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_name": self.task_name,
            "tool": self.tool,
            "parameters": self.parameters,
            "expected_output": self.expected_output,
            "depends_on": self.depends_on,
            "rollback_tasks": self.rollback_tasks,
            "max_retries": self.max_retries,
            "status": self.status,
            "attempts": self.attempts,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "last_error": self.last_error,
            "result": self.result
        }

@dataclass
class LongTermGoalRecord:
    """长期目标对象,承载跨任务自治信息."""
    goal_id: str
    objective: str
    success_definition: str = "形成稳定可复用结果"
    priority: str = "medium"
    constraints: List[str] = field(default_factory=list)
    task_type: str = "general_analysis"
    status: str = "active"
    progress: float = 0.0
    execution_count: int = 0
    last_score: float = 0.0
    last_run_task_id: Optional[str] = None
    next_focus: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal_id": self.goal_id,
            "objective": self.objective,
            "success_definition": self.success_definition,
            "priority": self.priority,
            "constraints": self.constraints,
            "task_type": self.task_type,
            "status": self.status,
            "progress": self.progress,
            "execution_count": self.execution_count,
            "last_score": self.last_score,
            "last_run_task_id": self.last_run_task_id,
            "next_focus": self.next_focus,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
