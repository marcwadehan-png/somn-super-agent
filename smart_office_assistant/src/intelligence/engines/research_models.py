# -*- coding: utf-8 -*-
"""
研究阶段数据模型 — 从 research_phase_manager.py 外置
v2.0 重构：支持数据驱动执行器架构
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Any, Optional


class ResearchPhase(Enum):
    """研究阶段"""
    PHASE1_BASELINE = 1
    PHASE2_DEEP = 2
    PHASE3_APPLICATION = 3
    PHASE4_SYSTEM = 4


class MilestoneStatus(Enum):
    """里程碑状态"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    BLOCKED = "blocked"


@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    task_name: str
    phase: int
    status: str = "pending"
    output_data: Dict[str, Any] = field(default_factory=dict)
    quality_score: float = 0.0
    findings: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class Milestone:
    """里程碑"""
    id: str
    phase: int
    name: str
    criteria: List[str]
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED
    achieved_at: Optional[str] = None
    evidence: List[str] = field(default_factory=list)


@dataclass
class PhaseReport:
    """阶段报告"""
    phase: int
    phase_name: str
    started_at: str
    completed_at: Optional[str] = None
    tasks_total: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    overall_score: float = 0.0
    key_findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    task_results: List[TaskResult] = field(default_factory=list)
