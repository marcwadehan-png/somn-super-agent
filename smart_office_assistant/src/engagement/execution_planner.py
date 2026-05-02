"""
engagement/execution_planner.py — 执行规划（从 strategy_engine 合并）
================================================
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

class PlannerTaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Resource:
    id: str
    name: str
    type: str  # 'human', 'tool', 'budget', 'time'
    capacity: float = 1.0
    cost_per_unit: float = 0.0
    skills: List[str] = field(default_factory=list)
    availability: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Task:
    id: str
    name: str
    description: str
    duration_hours: float
    priority: TaskPriority = TaskPriority.MEDIUM
    status: PlannerTaskStatus = PlannerTaskStatus.PENDING
    assigned_resources: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    progress: float = 0.0
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def is_critical(self) -> bool:
        return self.priority == TaskPriority.CRITICAL

    @property
    def is_overdue(self) -> bool:
        if self.end_time is None or self.status == PlannerTaskStatus.COMPLETED:
            return False
        return datetime.now() > self.end_time

class ExecutionPlanner:
    """执行规划器（合并到 engagement）"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.resources: Dict[str, Resource] = {}
        self.schedules: Dict[str, List[Dict]] = {}

    def create_task(self, name: str, description: str,
                       duration_hours: float,
                       priority: str = "medium",
                       dependencies: Optional[List[str]] = None,
                       tags: Optional[List[str]] = None) -> Task:
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.tasks)}"
        task = Task(
            id=task_id, name=name, description=description,
            duration_hours=duration_hours,
            priority=TaskPriority[priority.upper()],
            dependencies=dependencies or [],
            tags=tags or []
        )
        self.tasks[task_id] = task
        return task

    def decompose_task(self, task_id: str,
                             subtasks_config: List[Dict]) -> List[Task]:
        if task_id not in self.tasks:
            return []
        parent = self.tasks[task_id]
        subtasks = []
        for i, config in enumerate(subtasks_config):
            subtask = self.create_task(
                name=config['name'],
                description=config.get('description', ''),
                duration_hours=config['duration_hours'],
                priority=config.get('priority', 'medium'),
                dependencies=config.get('dependencies', []),
                tags=config.get('tags', [])
            )
            if i == 0:
                subtask.dependencies.append(task_id)
            else:
                subtask.dependencies.append(subtasks[-1].id)
            subtasks.append(subtask)
            parent.subtasks.append(subtask.id)
        return subtasks

    def add_resource(self, name: str, resource_type: str,
                            capacity: float = 1.0,
                            cost_per_unit: float = 0.0,
                            skills: Optional[List[str]] = None) -> Resource:
        resource_id = f"res_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.resources)}"
        resource = Resource(
            id=resource_id, name=name, type=resource_type,
            capacity=capacity, cost_per_unit=cost_per_unit,
            skills=skills or []
        )
        self.resources[resource_id] = resource
        return resource

    def assign_resource(self, task_id: str, resource_id: str) -> bool:
        if task_id not in self.tasks or resource_id not in self.resources:
            return False
        task = self.tasks[task_id]
        if resource_id not in task.assigned_resources:
            task.assigned_resources.append(resource_id)
        return True

    def auto_assign_resources(self, task_id: str) -> List[str]:
        if task_id not in self.tasks:
            return []
        task = self.tasks[task_id]
        assigned = []
        for res_id, resource in self.resources.items():
            if res_id in task.assigned_resources:
                continue
            if task.tags and resource.skills:
                if set(task.tags) & set(resource.skills) and resource.capacity > 0:
                    task.assigned_resources.append(res_id)
                    assigned.append(res_id)
        return assigned

    def create_schedule(self, task_ids: List[str],
                            start_date: Optional[datetime] = None,
                            consider_dependencies: bool = True) -> Dict[str, Any]:
        if start_date is None:
            start_date = datetime.now()
        schedule_id = f"sched_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        schedule = []
        sorted_tasks = self._sort_tasks_by_priority(task_ids, consider_dependencies)
        current_time = start_date
        for task_id in sorted_tasks:
            if task_id not in self.tasks:
                continue
            task = self.tasks[task_id]
            if consider_dependencies and task.dependencies:
                dep_end_times = [
                    self.tasks[d].end_time for d in task.dependencies
                    if d in self.tasks and self.tasks[d].end_time
                ]
                if dep_end_times:
                    current_time = max(current_time, max(dep_end_times))
            task.start_time = current_time
            task.end_time = current_time + timedelta(hours=task.duration_hours)
            schedule.append({
                'task_id': task_id,
                'task_name': task.name,
                'start_time': task.start_time.isoformat(),
                'end_time': task.end_time.isoformat(),
                'duration_hours': task.duration_hours,
                'assigned_resources': [
                    self.resources[rid].name for rid in task.assigned_resources
                    if rid in self.resources
                ]
            })
            current_time = task.end_time
        self.schedules[schedule_id] = schedule
        return {
            'schedule_id': schedule_id,
            'start_date': start_date.isoformat(),
            'end_date': schedule[-1]['end_time'] if schedule else start_date.isoformat(),
            'total_duration_hours': sum(s['duration_hours'] for s in schedule),
            'tasks': schedule,
        }

    def _sort_tasks_by_priority(self, task_ids: List[str],
                                   consider_dependencies: bool) -> List[str]:
        task_list = [(tid, self.tasks[tid]) for tid in task_ids if tid in self.tasks]
        sorted_tasks = sorted(task_list, key=lambda x: (x[1].priority.value, x[1].duration_hours))
        result = [t[0] for t in sorted_tasks]
        if consider_dependencies:
            result = self._topological_sort(result)
        return result

    def _topological_sort(self, task_ids: List[str]) -> List[str]:
        visited = set()
        result = []
        def visit(tid):
            if tid in visited:
                return
            visited.add(tid)
            if tid in self.tasks:
                task = self.tasks[tid]
                for dep_id in task.dependencies:
                    if dep_id in self.tasks:
                        visit(dep_id)
            result.append(tid)
        for tid in task_ids:
            visit(tid)
        return result

    def update_task_progress(self, task_id: str, progress: float) -> bool:
        if task_id not in self.tasks:
            return False
        task = self.tasks[task_id]
        task.progress = max(0.0, min(1.0, progress))
        if task.progress >= 1.0:
            task.status = PlannerTaskStatus.COMPLETED
        elif task.progress > 0:
            task.status = PlannerTaskStatus.IN_PROGRESS
        return True

    def get_execution_status(self, task_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        if task_ids is None:
            task_ids = list(self.tasks.keys())
        tasks_info = []
        for tid in task_ids:
            if tid not in self.tasks:
                continue
            task = self.tasks[tid]
            tasks_info.append({
                'id': task.id, 'name': task.name,
                'status': task.status.value, 'progress': task.progress,
                'priority': task.priority.name,
                'is_overdue': task.is_overdue,
            })
        return {
            'total_tasks': len(tasks_info),
            'completed_tasks': sum(1 for t in tasks_info if t['status'] == 'completed'),
            'in_progress_tasks': sum(1 for t in tasks_info if t['status'] == 'in_progress'),
            'blocked_tasks': sum(1 for t in tasks_info if t['status'] == 'blocked'),
            'overall_progress': sum(t['progress'] for t in tasks_info) / max(len(tasks_info), 1),
            'tasks': tasks_info,
        }

def create_execution_planner() -> ExecutionPlanner:
    return ExecutionPlanner()
