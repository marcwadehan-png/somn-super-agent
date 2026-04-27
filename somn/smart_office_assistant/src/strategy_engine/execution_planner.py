"""
__all__ = [
    'add_resource',
    'assign_resource',
    'auto_assign_resources',
    'create_execution_planner',
    'create_schedule',
    'create_task',
    'decompose_task',
    'export_plan',
    'get_execution_status',
    'is_critical',
    'is_overdue',
    'optimize_schedule',
    'update_task_progress',
    'visit',
]

执行规划模块 - 从abyss AI迁移
功能:任务分解,资源分配,进度跟踪
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

class PlannerTaskStatus(Enum):
    """执行规划任务状态（区别于其他模块的TaskStatus）"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"  # 任务被阻塞
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Resource:
    """资源定义"""
    id: str
    name: str
    type: str  # 'human', 'tool', 'budget', 'time'
    capacity: float = 1.0  # 容量/可用性
    cost_per_unit: float = 0.0
    skills: List[str] = field(default_factory=list)
    availability: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Task:
    """任务定义"""
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
        """是否关键任务"""
        return self.priority == TaskPriority.CRITICAL
    
    @property
    def is_overdue(self) -> bool:
        """是否逾期"""
        if self.end_time is None or self.status == PlannerTaskStatus.COMPLETED:
            return False
        return datetime.now() > self.end_time

class ExecutionPlanner:
    """执行规划器"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.resources: Dict[str, Resource] = {}
        self.schedules: Dict[str, List[Dict]] = {}
    
    def create_task(
        self,
        name: str,
        description: str,
        duration_hours: float,
        priority: str = "medium",
        dependencies: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """创建任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.tasks)}"
        
        task = Task(
            id=task_id,
            name=name,
            description=description,
            duration_hours=duration_hours,
            priority=TaskPriority[priority.upper()],
            dependencies=dependencies or [],
            tags=tags or []
        )
        
        self.tasks[task_id] = task
        return task
    
    def decompose_task(self, task_id: str, subtasks_config: List[Dict]) -> List[Task]:
        """分解任务为子任务"""
        if task_id not in self.tasks:
            return []
        
        parent_task = self.tasks[task_id]
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
            
            # 添加父任务依赖
            if i == 0:
                subtask.dependencies.append(task_id)
            else:
                subtask.dependencies.append(subtasks[-1].id)
            
            subtasks.append(subtask)
            parent_task.subtasks.append(subtask.id)
        
        return subtasks
    
    def add_resource(
        self,
        name: str,
        resource_type: str,
        capacity: float = 1.0,
        cost_per_unit: float = 0.0,
        skills: Optional[List[str]] = None
    ) -> Resource:
        """添加资源"""
        resource_id = f"res_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.resources)}"
        
        resource = Resource(
            id=resource_id,
            name=name,
            type=resource_type,
            capacity=capacity,
            cost_per_unit=cost_per_unit,
            skills=skills or []
        )
        
        self.resources[resource_id] = resource
        return resource
    
    def assign_resource(self, task_id: str, resource_id: str) -> bool:
        """分配资源给任务"""
        if task_id not in self.tasks or resource_id not in self.resources:
            return False
        
        task = self.tasks[task_id]
        resource = self.resources[resource_id]
        
        # 检查资源技能匹配
        if task.tags and resource.skills:
            matching_skills = set(task.tags) & set(resource.skills)
            if not matching_skills:
                return False
        
        task.assigned_resources.append(resource_id)
        return True
    
    def auto_assign_resources(self, task_id: str) -> List[str]:
        """自动分配资源"""
        if task_id not in self.tasks:
            return []
        
        task = self.tasks[task_id]
        assigned = []
        
        # 根据任务标签匹配资源技能
        for res_id, resource in self.resources.items():
            if res_id in task.assigned_resources:
                continue
            
            # 技能匹配
            if task.tags and resource.skills:
                matching = set(task.tags) & set(resource.skills)
                if matching and resource.capacity > 0:
                    task.assigned_resources.append(res_id)
                    assigned.append(res_id)
        
        return assigned
    
    def create_schedule(
        self,
        task_ids: List[str],
        start_date: Optional[datetime] = None,
        consider_dependencies: bool = True
    ) -> Dict[str, Any]:
        """创建执行计划"""
        if start_date is None:
            start_date = datetime.now()
        
        schedule_id = f"sched_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        schedule = []
        
        # 按优先级和依赖排序任务
        sorted_tasks = self._sort_tasks_by_priority(task_ids, consider_dependencies)
        
        current_time = start_date
        
        for task_id in sorted_tasks:
            if task_id not in self.tasks:
                continue
            
            task = self.tasks[task_id]
            
            # 考虑依赖任务的完成时间
            if consider_dependencies and task.dependencies:
                dep_end_times = []
                for dep_id in task.dependencies:
                    if dep_id in self.tasks:
                        dep_task = self.tasks[dep_id]
                        if dep_task.end_time:
                            dep_end_times.append(dep_task.end_time)
                
                if dep_end_times:
                    current_time = max(current_time, max(dep_end_times))
            
            # 设置任务时间
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
            
            # 下一个任务可以并行开始(如果有资源)
            current_time = task.end_time
        
        self.schedules[schedule_id] = schedule
        
        return {
            'schedule_id': schedule_id,
            'start_date': start_date.isoformat(),
            'end_date': schedule[-1]['end_time'] if schedule else start_date.isoformat(),
            'total_duration_hours': sum(s['duration_hours'] for s in schedule),
            'tasks': schedule,
            'critical_path': self._identify_critical_path(task_ids)
        }
    
    def _sort_tasks_by_priority(
        self,
        task_ids: List[str],
        consider_dependencies: bool
    ) -> List[str]:
        """按优先级排序任务"""
        task_list = [
            (tid, self.tasks[tid]) 
            for tid in task_ids 
            if tid in self.tasks
        ]
        
        # 按优先级排序
        sorted_tasks = sorted(
            task_list,
            key=lambda x: (x[1].priority.value, -x[1].duration_hours)
        )
        
        result = [t[0] for t in sorted_tasks]
        
        # 如果需要考虑依赖,进行拓扑排序
        if consider_dependencies:
            result = self._topological_sort(result)
        
        return result
    
    def _topological_sort(self, task_ids: List[str]) -> List[str]:
        """拓扑排序(处理依赖关系)"""
        # 简化的拓扑排序
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
    
    def _identify_critical_path(self, task_ids: List[str]) -> List[str]:
        """recognize关键路径"""
        # 简化的关键路径recognize
        critical_tasks = []
        
        for tid in task_ids:
            if tid in self.tasks:
                task = self.tasks[tid]
                if task.is_critical or task.priority == TaskPriority.HIGH:
                    critical_tasks.append(tid)
        
        return critical_tasks
    
    def update_task_progress(self, task_id: str, progress: float) -> bool:
        """更新任务进度"""
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
        """get执行状态"""
        if task_ids is None:
            task_ids = list(self.tasks.keys())
        
        tasks_info = []
        total_progress = 0
        completed_count = 0
        
        for tid in task_ids:
            if tid not in self.tasks:
                continue
            
            task = self.tasks[tid]
            tasks_info.append({
                'id': task.id,
                'name': task.name,
                'status': task.status.value,
                'progress': task.progress,
                'priority': task.priority.name,
                'is_overdue': task.is_overdue,
                'assigned_to': [
                    self.resources[rid].name 
                    for rid in task.assigned_resources
                    if rid in self.resources
                ]
            })
            
            total_progress += task.progress
            if task.status == PlannerTaskStatus.COMPLETED:
                completed_count += 1
        
        total_tasks = len(tasks_info)
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_count,
            'in_progress_tasks': sum(1 for t in tasks_info if t['status'] == 'in_progress'),
            'blocked_tasks': sum(1 for t in tasks_info if t['status'] == 'blocked'),
            'overall_progress': total_progress / total_tasks if total_tasks > 0 else 0,
            'tasks': tasks_info,
            'bottlenecks': self._identify_bottlenecks(task_ids)
        }
    
    def _identify_bottlenecks(self, task_ids: List[str]) -> List[Dict]:
        """recognize瓶颈"""
        bottlenecks = []
        
        for tid in task_ids:
            if tid not in self.tasks:
                continue
            
            task = self.tasks[tid]
            
            # 检查阻塞的任务
            if task.status == PlannerTaskStatus.BLOCKED:
                bottlenecks.append({
                    'task_id': tid,
                    'task_name': task.name,
                    'type': 'blocked',
                    'reason': '任务被阻塞'
                })
            
            # 检查逾期的关键任务
            elif task.is_critical and task.is_overdue:
                bottlenecks.append({
                    'task_id': tid,
                    'task_name': task.name,
                    'type': 'overdue_critical',
                    'reason': '关键任务逾期'
                })
            
            # 检查没有资源的任务
            elif not task.assigned_resources and task.status == PlannerTaskStatus.PENDING:
                bottlenecks.append({
                    'task_id': tid,
                    'task_name': task.name,
                    'type': 'no_resources',
                    'reason': '未分配资源'
                })
        
        return bottlenecks
    
    def optimize_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """优化计划"""
        if schedule_id not in self.schedules:
            return {'error': 'Schedule not found'}
        
        schedule = self.schedules[schedule_id]
        optimizations = []
        
        # 检查资源冲突
        resource_usage = {}
        for task_schedule in schedule:
            for resource in task_schedule.get('assigned_resources', []):
                if resource not in resource_usage:
                    resource_usage[resource] = []
                resource_usage[resource].append(task_schedule['task_id'])
        
        # recognize资源过载
        for resource, tasks in resource_usage.items():
            if len(tasks) > 3:  # 假设一个资源最多3个并行任务
                optimizations.append({
                    'type': 'resource_overload',
                    'resource': resource,
                    'tasks': tasks,
                    'suggestion': f'考虑为资源"{resource}"减负或增加资源'
                })
        
        # 检查任务并行机会
        sequential_tasks = []
        for i in range(len(schedule) - 1):
            current = schedule[i]
            next_task = schedule[i + 1]
            
            # 检查是否可以并行
            if not self._has_dependency(current['task_id'], next_task['task_id']):
                sequential_tasks.append((current['task_id'], next_task['task_id']))
        
        if sequential_tasks:
            optimizations.append({
                'type': 'parallelization_opportunity',
                'pairs': sequential_tasks,
                'suggestion': '这些任务可以并行执行以缩短总时间'
            })
        
        return {
            'schedule_id': schedule_id,
            'optimizations': optimizations,
            'estimated_time_save': len(optimizations) * 2  # 粗略估计
        }
    
    def _has_dependency(self, task_id1: str, task_id2: str) -> bool:
        """检查任务间是否有依赖关系"""
        if task_id1 not in self.tasks or task_id2 not in self.tasks:
            return False
        
        task1 = self.tasks[task_id1]
        task2 = self.tasks[task_id2]
        
        return (task_id2 in task1.dependencies or 
                task_id1 in task2.dependencies)
    
    def export_plan(self, format_type: str = 'json') -> str:
        """导出执行计划"""
        plan_data = {
            'tasks': [
                {
                    'id': t.id,
                    'name': t.name,
                    'description': t.description,
                    'status': t.status.value,
                    'progress': t.progress,
                    'priority': t.priority.name,
                    'duration_hours': t.duration_hours,
                    'assigned_resources': t.assigned_resources,
                    'dependencies': t.dependencies
                }
                for t in self.tasks.values()
            ],
            'resources': [
                {
                    'id': r.id,
                    'name': r.name,
                    'type': r.type,
                    'capacity': r.capacity,
                    'skills': r.skills
                }
                for r in self.resources.values()
            ],
            'export_time': datetime.now().isoformat()
        }
        
        if format_type == 'json':
            return json.dumps(plan_data, ensure_ascii=False, indent=2)
        
        return str(plan_data)

# 便捷函数
def create_execution_planner() -> ExecutionPlanner:
    """创建执行规划器"""
    return ExecutionPlanner()
