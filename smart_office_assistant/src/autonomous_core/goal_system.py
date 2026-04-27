"""
__all__ = [
    'add_dependency',
    'block_goal',
    'check_dependencies_satisfied',
    'complete_goal',
    'create_goal',
    'days_until_deadline',
    'decompose_goal',
    'delete_goal',
    'fail_goal',
    'from_dict',
    'generate_report',
    'get_active_goals',
    'get_goal',
    'get_goal_tree',
    'get_goals_by_priority',
    'get_goals_by_tag',
    'get_next_goal',
    'get_overdue_goals',
    'get_pending_goals',
    'get_ready_goals',
    'get_statistics',
    'get_sub_goals',
    'is_active',
    'is_blocked',
    'is_completed',
    'is_overdue',
    'is_ready',
    'pause_goal',
    'remove_dependency',
    'start_goal',
    'to_dict',
    'update_goal',
    'update_progress',
]

目标系统 - Goal System

实现智能体的目标驱动能力:
- 目标设定与分解
- 目标优先级管理
- 目标依赖关系
- 目标执行追踪
- 目标完成评估
"""

import json
import uuid
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict
from pathlib import Path

from loguru import logger

class GoalStatus(Enum):
    """目标状态"""
    PENDING = "pending"          # 待开始
    ACTIVE = "active"            # 执行中
    BLOCKED = "blocked"          # 被阻塞
    PAUSED = "paused"            # 暂停
    COMPLETED = "completed"      # 已完成
    FAILED = "failed"            # 失败
    CANCELLED = "cancelled"      # 已取消

class GoalPriority(Enum):
    """目标优先级"""
    CRITICAL = 1    # 关键 - 必须完成
    HIGH = 2        # 高 - 重要目标
    MEDIUM = 3      # 中 - 一般目标
    LOW = 4         # 低 - 可选目标
    TRIVIAL = 5     # 琐碎 - 有空再做

@dataclass
class Goal:
    """目标定义"""
    # 基本信息
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    
    # 状态管理
    status: GoalStatus = GoalStatus.PENDING
    priority: GoalPriority = GoalPriority.MEDIUM
    
    # 时间属性
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    deadline: Optional[str] = None
    completed_at: Optional[str] = None
    
    # 目标结构
    parent_id: Optional[str] = None           # 父目标ID
    sub_goals: List[str] = field(default_factory=list)  # 子目标ID列表
    dependencies: List[str] = field(default_factory=list)  # 依赖的目标ID
    
    # 执行属性
    progress: float = 0.0                     # 进度 0-100
    estimated_effort: float = 1.0             # 预估工作量(小时)
    actual_effort: float = 0.0                # 实际工作量
    
    # 成功标准
    success_criteria: List[str] = field(default_factory=list)
    
    # 元数据
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'deadline': self.deadline,
            'completed_at': self.completed_at,
            'parent_id': self.parent_id,
            'sub_goals': self.sub_goals,
            'dependencies': self.dependencies,
            'progress': self.progress,
            'estimated_effort': self.estimated_effort,
            'actual_effort': self.actual_effort,
            'success_criteria': self.success_criteria,
            'context': self.context,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Goal':
        """从字典创建"""
        return cls(
            id=data.get('id', str(uuid.uuid4())[:8]),
            title=data.get('title', ''),
            description=data.get('description', ''),
            status=GoalStatus(data.get('status', 'pending')),
            priority=GoalPriority(data.get('priority', 3)),
            created_at=data.get('created_at', datetime.now().isoformat()),
            started_at=data.get('started_at'),
            deadline=data.get('deadline'),
            completed_at=data.get('completed_at'),
            parent_id=data.get('parent_id'),
            sub_goals=data.get('sub_goals', []),
            dependencies=data.get('dependencies', []),
            progress=data.get('progress', 0.0),
            estimated_effort=data.get('estimated_effort', 1.0),
            actual_effort=data.get('actual_effort', 0.0),
            success_criteria=data.get('success_criteria', []),
            context=data.get('context', {}),
            tags=data.get('tags', [])
        )
    
    def is_ready(self) -> bool:
        """检查目标是否准备好执行"""
        return self.status == GoalStatus.PENDING
    
    def is_active(self) -> bool:
        """检查目标是否活跃"""
        return self.status == GoalStatus.ACTIVE
    
    def is_completed(self) -> bool:
        """检查目标是否完成"""
        return self.status == GoalStatus.COMPLETED
    
    def is_blocked(self) -> bool:
        """检查目标是否被阻塞"""
        return self.status == GoalStatus.BLOCKED
    
    def days_until_deadline(self) -> Optional[int]:
        """计算距离截止日期的天数"""
        if not self.deadline:
            return None
        try:
            deadline = datetime.fromisoformat(self.deadline)
            now = datetime.now()
            return (deadline - now).days
        except Exception:
            return None
    
    def is_overdue(self) -> bool:
        """检查是否逾期"""
        days = self.days_until_deadline()
        return days is not None and days < 0

class GoalSystem:
    """
    目标系统 - 管理智能体的所有目标
    
    核心功能:
    1. 目标CRUD
    2. 目标分解与组合
    3. 依赖管理
    4. 优先级调度
    5. 进度追踪
    """
    
    def __init__(self, storage_path: str = "data/goals"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # 目标存储
        self._goals: Dict[str, Goal] = {}
        
        # 索引
        self._active_goals: Set[str] = set()
        self._pending_goals: Set[str] = set()
        self._completed_goals: Set[str] = set()
        
        # 加载已有目标
        self._load_goals()
        
        logger.info(f"目标系统init完成,已加载 {len(self._goals)} 个目标")
    
    def _load_goals(self):
        """从存储加载目标（空文件/损坏时优雅降级）"""
        goals_file = self.storage_path / "goals.json"
        if goals_file.exists():
            try:
                with open(goals_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if not content:
                    logger.info("goals.json 为空，初始化为空目标列表")
                    return
                data = json.loads(content)
                for goal_data in data.get('goals', []):
                    goal = Goal.from_dict(goal_data)
                    self._goals[goal.id] = goal
                    self._update_index(goal)
                logger.info(f"已加载 {len(self._goals)} 个目标")
            except json.JSONDecodeError as e:
                logger.warning(f"goals.json 格式损坏 ({e})，初始化为空目标列表")
            except Exception as e:
                logger.warning(f"加载目标失败 ({e})，初始化为空目标列表")
    
    def _save_goals(self):
        """保存目标到存储"""
        goals_file = self.storage_path / "goals.json"
        try:
            data = {
                'updated_at': datetime.now().isoformat(),
                'goals': [goal.to_dict() for goal in self._goals.values()]
            }
            with open(goals_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存目标失败: {e}")
    
    def _update_index(self, goal: Goal):
        """更新索引"""
        # 从所有集合中移除
        self._active_goals.discard(goal.id)
        self._pending_goals.discard(goal.id)
        self._completed_goals.discard(goal.id)
        
        # 添加到对应集合
        if goal.status == GoalStatus.ACTIVE:
            self._active_goals.add(goal.id)
        elif goal.status == GoalStatus.PENDING:
            self._pending_goals.add(goal.id)
        elif goal.status == GoalStatus.COMPLETED:
            self._completed_goals.add(goal.id)
    
    # ========== 目标CRUD ==========
    
    def create_goal(
        self,
        title: str,
        description: str = "",
        priority: GoalPriority = GoalPriority.MEDIUM,
        deadline: Optional[str] = None,
        parent_id: Optional[str] = None,
        success_criteria: Optional[List[str]] = None,
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> Goal:
        """
        创建新目标
        
        Args:
            title: 目标标题
            description: 目标描述
            priority: 优先级
            deadline: 截止日期 (ISO格式)
            parent_id: 父目标ID
            success_criteria: 成功标准列表
            context: 上下文信息
            tags: 标签列表
        
        Returns:
            创建的目标对象
        """
        goal = Goal(
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            parent_id=parent_id,
            success_criteria=success_criteria or [],
            context=context or {},
            tags=tags or []
        )
        
        self._goals[goal.id] = goal
        self._pending_goals.add(goal.id)
        
        # 如果有父目标,更新父目标的子目标列表
        if parent_id and parent_id in self._goals:
            parent = self._goals[parent_id]
            if goal.id not in parent.sub_goals:
                parent.sub_goals.append(goal.id)
        
        self._save_goals()
        logger.info(f"创建目标: [{goal.id}] {title}")
        
        return goal
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """get目标"""
        return self._goals.get(goal_id)
    
    def update_goal(self, goal_id: str, **kwargs) -> Optional[Goal]:
        """更新目标属性"""
        goal = self._goals.get(goal_id)
        if not goal:
            return None
        
        for key, value in kwargs.items():
            if hasattr(goal, key):
                setattr(goal, key, value)
        
        self._update_index(goal)
        self._save_goals()
        
        return goal
    
    def delete_goal(self, goal_id: str) -> bool:
        """删除目标"""
        if goal_id not in self._goals:
            return False
        
        goal = self._goals[goal_id]
        
        # 从父目标的子目标列表中移除
        if goal.parent_id and goal.parent_id in self._goals:
            parent = self._goals[goal.parent_id]
            if goal_id in parent.sub_goals:
                parent.sub_goals.remove(goal_id)
        
        # 从依赖它的目标中移除
        for g in self._goals.values():
            if goal_id in g.dependencies:
                g.dependencies.remove(goal_id)
        
        # 删除目标
        del self._goals[goal_id]
        self._active_goals.discard(goal_id)
        self._pending_goals.discard(goal_id)
        self._completed_goals.discard(goal_id)
        
        self._save_goals()
        logger.info(f"删除目标: {goal_id}")
        
        return True
    
    # ========== 目标分解 ==========
    
    def decompose_goal(
        self,
        parent_id: str,
        sub_goals_data: List[Dict[str, Any]]
    ) -> List[Goal]:
        """
        将目标分解为子目标
        
        Args:
            parent_id: 父目标ID
            sub_goals_data: 子目标数据列表
        
        Returns:
            创建的子目标列表
        """
        parent = self._goals.get(parent_id)
        if not parent:
            logger.warning(f"父目标不存在: {parent_id}")
            return []
        
        created_goals = []
        for data in sub_goals_data:
            sub_goal = self.create_goal(
                title=data['title'],
                description=data.get('description', ''),
                priority=GoalPriority(data.get('priority', parent.priority.value)),
                deadline=data.get('deadline'),
                parent_id=parent_id,
                success_criteria=data.get('success_criteria', []),
                context=data.get('context', {}),
                tags=data.get('tags', [])
            )
            created_goals.append(sub_goal)
        
        logger.info(f"目标 [{parent_id}] 分解为 {len(created_goals)} 个子目标")
        return created_goals
    
    def get_sub_goals(self, goal_id: str) -> List[Goal]:
        """get子目标列表"""
        goal = self._goals.get(goal_id)
        if not goal:
            return []
        return [self._goals[sid] for sid in goal.sub_goals if sid in self._goals]
    
    def get_goal_tree(self, goal_id: str) -> Dict[str, Any]:
        """get目标树结构"""
        goal = self._goals.get(goal_id)
        if not goal:
            return {}
        
        return {
            'goal': goal.to_dict(),
            'sub_goals': [self.get_goal_tree(sid) for sid in goal.sub_goals if sid in self._goals]
        }
    
    # ========== 依赖管理 ==========
    
    def add_dependency(self, goal_id: str, depends_on: str) -> bool:
        """添加目标依赖"""
        if goal_id not in self._goals or depends_on not in self._goals:
            return False
        
        goal = self._goals[goal_id]
        if depends_on not in goal.dependencies:
            goal.dependencies.append(depends_on)
            self._save_goals()
        
        return True
    
    def remove_dependency(self, goal_id: str, depends_on: str) -> bool:
        """移除目标依赖"""
        if goal_id not in self._goals:
            return False
        
        goal = self._goals[goal_id]
        if depends_on in goal.dependencies:
            goal.dependencies.remove(depends_on)
            self._save_goals()
        
        return True
    
    def check_dependencies_satisfied(self, goal_id: str) -> bool:
        """检查目标依赖是否全部满足"""
        goal = self._goals.get(goal_id)
        if not goal:
            return False
        
        for dep_id in goal.dependencies:
            dep = self._goals.get(dep_id)
            if not dep or not dep.is_completed():
                return False
        
        return True
    
    # ========== 状态管理 ==========
    
    def start_goal(self, goal_id: str) -> bool:
        """开始执行目标"""
        goal = self._goals.get(goal_id)
        if not goal:
            return False
        
        # 检查依赖
        if not self.check_dependencies_satisfied(goal_id):
            logger.warning(f"目标 [{goal_id}] 依赖未满足,无法开始")
            return False
        
        goal.status = GoalStatus.ACTIVE
        goal.started_at = datetime.now().isoformat()
        self._update_index(goal)
        self._save_goals()
        
        logger.info(f"开始执行目标: [{goal_id}] {goal.title}")
        return True
    
    def pause_goal(self, goal_id: str, reason: str = "") -> bool:
        """暂停目标"""
        goal = self._goals.get(goal_id)
        if not goal:
            return False
        
        goal.status = GoalStatus.PAUSED
        goal.context['pause_reason'] = reason
        goal.context['paused_at'] = datetime.now().isoformat()
        self._update_index(goal)
        self._save_goals()
        
        logger.info(f"暂停目标: [{goal_id}] {goal.title} - {reason}")
        return True
    
    def block_goal(self, goal_id: str, reason: str = "") -> bool:
        """阻塞目标"""
        goal = self._goals.get(goal_id)
        if not goal:
            return False
        
        goal.status = GoalStatus.BLOCKED
        goal.context['block_reason'] = reason
        goal.context['blocked_at'] = datetime.now().isoformat()
        self._update_index(goal)
        self._save_goals()
        
        logger.info(f"阻塞目标: [{goal_id}] {goal.title} - {reason}")
        return True
    
    def complete_goal(self, goal_id: str, notes: str = "") -> bool:
        """完成目标"""
        goal = self._goals.get(goal_id)
        if not goal:
            return False
        
        goal.status = GoalStatus.COMPLETED
        goal.progress = 100.0
        goal.completed_at = datetime.now().isoformat()
        goal.context['completion_notes'] = notes
        self._update_index(goal)
        self._save_goals()
        
        # 更新父目标进度
        if goal.parent_id and goal.parent_id in self._goals:
            self._update_parent_progress(goal.parent_id)
        
        logger.info(f"完成目标: [{goal_id}] {goal.title}")
        return True
    
    def fail_goal(self, goal_id: str, reason: str = "") -> bool:
        """标记目标失败"""
        goal = self._goals.get(goal_id)
        if not goal:
            return False
        
        goal.status = GoalStatus.FAILED
        goal.context['failure_reason'] = reason
        goal.context['failed_at'] = datetime.now().isoformat()
        self._update_index(goal)
        self._save_goals()
        
        logger.info(f"目标失败: [{goal_id}] {goal.title} - {reason}")
        return True
    
    def update_progress(self, goal_id: str, progress: float) -> bool:
        """更新目标进度"""
        goal = self._goals.get(goal_id)
        if not goal:
            return False
        
        goal.progress = max(0.0, min(100.0, progress))
        
        # 如果进度达到100%,自动完成
        if goal.progress >= 100.0:
            return self.complete_goal(goal_id)
        
        self._save_goals()
        return True
    
    def _update_parent_progress(self, parent_id: str):
        """更新父目标进度"""
        parent = self._goals.get(parent_id)
        if not parent:
            return
        
        sub_goals = self.get_sub_goals(parent_id)
        if not sub_goals:
            return
        
        total_progress = sum(g.progress for g in sub_goals)
        avg_progress = total_progress / len(sub_goals)
        
        parent.progress = avg_progress
        
        # 如果所有子目标都完成,父目标也完成
        if all(g.is_completed() for g in sub_goals):
            self.complete_goal(parent_id, "所有子目标已完成")
        
        self._save_goals()
    
    # ========== 查询接口 ==========
    
    def get_active_goals(self) -> List[Goal]:
        """get活跃目标"""
        return [self._goals[gid] for gid in self._active_goals if gid in self._goals]
    
    def get_pending_goals(self) -> List[Goal]:
        """get待处理目标"""
        return [self._goals[gid] for gid in self._pending_goals if gid in self._goals]
    
    def get_ready_goals(self) -> List[Goal]:
        """get准备好执行的目标(依赖已满足)"""
        ready = []
        for goal in self.get_pending_goals():
            if self.check_dependencies_satisfied(goal.id):
                ready.append(goal)
        return ready
    
    def get_overdue_goals(self) -> List[Goal]:
        """get逾期目标"""
        overdue = []
        for goal in self._goals.values():
            if not goal.is_completed() and goal.is_overdue():
                overdue.append(goal)
        return overdue
    
    def get_goals_by_priority(self, priority: GoalPriority) -> List[Goal]:
        """按优先级get目标"""
        return [g for g in self._goals.values() if g.priority == priority]
    
    def get_goals_by_tag(self, tag: str) -> List[Goal]:
        """按标签get目标"""
        return [g for g in self._goals.values() if tag in g.tags]
    
    def get_next_goal(self) -> Optional[Goal]:
        """
        get下一个应该执行的目标
        
        优先级:
        1. 逾期的高优先级目标
        2. 关键优先级且准备好的目标
        3. 高优先级且准备好的目标
        4. 其他准备好的目标(按优先级排序)
        """
        ready_goals = self.get_ready_goals()
        if not ready_goals:
            return None
        
        # 按优先级排序
        ready_goals.sort(key=lambda g: (g.priority.value, g.deadline or '9999'))
        
        return ready_goals[0]
    
    # ========== 统计与报告 ==========
    
    def get_statistics(self) -> Dict[str, Any]:
        """get目标统计信息"""
        total = len(self._goals)
        active = len(self._active_goals)
        pending = len(self._pending_goals)
        completed = len(self._completed_goals)
        
        by_status = {status.value: 0 for status in GoalStatus}
        for goal in self._goals.values():
            by_status[goal.status.value] += 1
        
        by_priority = {priority.name: 0 for priority in GoalPriority}
        for goal in self._goals.values():
            by_priority[goal.priority.name] += 1
        
        overdue = len(self.get_overdue_goals())
        
        return {
            'total': total,
            'active': active,
            'pending': pending,
            'completed': completed,
            'failed': by_status.get('failed', 0),
            'overdue': overdue,
            'by_status': by_status,
            'by_priority': by_priority,
            'completion_rate': completed / total if total > 0 else 0.0
        }
    
    def generate_report(self) -> str:
        """generate目标系统报告"""
        stats = self.get_statistics()
        
        report = f"""
# 目标系统报告

## 统计概览
- 总目标数: {stats['total']}
- 活跃中: {stats['active']}
- 待处理: {stats['pending']}
- 已完成: {stats['completed']}
- 失败: {stats['failed']}
- 逾期: {stats['overdue']}
- 完成率: {stats['completion_rate']:.1%}

## 活跃目标
"""
        for goal in self.get_active_goals():
            report += f"- [{goal.id}] {goal.title} ({goal.progress:.0f}%)\n"
        
        report += "\n## 待处理目标\n"
        for goal in self.get_ready_goals()[:10]:  # 最多显示10个
            deadline = goal.deadline or "无截止日期"
            report += f"- [{goal.id}] {goal.title} (截止: {deadline})\n"
        
        if stats['overdue'] > 0:
            report += "\n## ⚠️ 逾期目标\n"
            for goal in self.get_overdue_goals():
                report += f"- [{goal.id}] {goal.title} (已逾期 {abs(goal.days_until_deadline())} 天)\n"
        
        return report
