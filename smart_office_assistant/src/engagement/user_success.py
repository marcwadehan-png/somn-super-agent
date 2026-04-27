"""
__all__ = [
    'create_goal',
    'detect_obstacles',
    'get_goal',
    'get_goal_dashboard',
    'get_progress_history',
    'get_progress_percentage',
    'get_success_insights',
    'get_user_goals',
    'get_velocity',
    'is_on_track',
    'on_goal_completed',
    'record_progress',
    'suggest_goal_breakdown',
    'update_goal_progress',
]

用户成功导向体系 - 帮助用户达成目标

核心理念:产品的成功体现在用户的成功上
"""

from typing import Dict, List, Optional, Any, Callable
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

class GoalStatus(Enum):
    """目标状态"""
    ACTIVE = "active"         # 进行中
    COMPLETED = "completed"   # 已完成
    PAUSED = "paused"        # 已暂停
    ABANDONED = "abandoned"  # 已放弃

class GoalType(Enum):
    """目标类型"""
    SHORT_TERM = "short_term"    # 短期(1周内)
    MEDIUM_TERM = "medium_term"  # 中期(1个月内)
    LONG_TERM = "long_term"      # 长期(1个月以上)

@dataclass
class Goal:
    """目标"""
    id: str
    user_id: str
    title: str
    description: str
    type: GoalType
    target_value: int
    current_value: int = 0
    unit: str = ""
    status: GoalStatus = GoalStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    target_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_progress_percentage(self) -> int:
        if self.target_value == 0:
            return 0
        return min(100, int(self.current_value / self.target_value * 100))
    
    def is_on_track(self) -> bool:
        """检查是否按计划进行"""
        if not self.target_date or self.status != GoalStatus.ACTIVE:
            return True
        
        total_days = (self.target_date - self.created_at).days
        if total_days == 0:
            return True
        
        days_passed = (datetime.now() - self.created_at).days
        expected_progress = days_passed / total_days
        actual_progress = self.current_value / self.target_value if self.target_value > 0 else 0
        
        return actual_progress >= expected_progress * 0.8  # 允许20%的偏差

@dataclass
class ProgressUpdate:
    """进度更新"""
    goal_id: str
    old_value: int
    new_value: int
    update_time: datetime
    note: str = ""

class ProgressTracker:
    """进度追踪器"""
    
    def __init__(self):
        self.updates: Dict[str, List[ProgressUpdate]] = {}
    
    def record_progress(self, goal_id: str, old_value: int, new_value: int, note: str = ""):
        """记录进度更新"""
        if goal_id not in self.updates:
            self.updates[goal_id] = []
        
        update = ProgressUpdate(
            goal_id=goal_id,
            old_value=old_value,
            new_value=new_value,
            update_time=datetime.now(),
            note=note
        )
        
        self.updates[goal_id].append(update)
    
    def get_progress_history(self, goal_id: str) -> List[ProgressUpdate]:
        """get进度历史"""
        return self.updates.get(goal_id, [])
    
    def get_velocity(self, goal_id: str, days: int = 7) -> float:
        """
        计算进度速度(最近N天)
        
        Returns:
            平均每天完成的量
        """
        updates = self.updates.get(goal_id, [])
        if not updates:
            return 0.0
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_updates = [u for u in updates if u.update_time > cutoff_date]
        
        if len(recent_updates) < 2:
            return 0.0
        
        first = recent_updates[0]
        last = recent_updates[-1]
        
        value_change = last.new_value - first.old_value
        day_change = (last.update_time - first.update_time).days or 1
        
        return value_change / day_change

class UserSuccessSystem:
    """
    用户成功系统
    
    帮助用户设定目标,追踪进度,达成成功
    """
    
    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        self.user_goals: Dict[str, List[str]] = {}  # user_id -> goal_ids
        self.progress_tracker = ProgressTracker()
        self.success_callbacks: List[Callable] = []
        self.obstacle_handlers: Dict[str, Callable] = {}
    
    def create_goal(self, user_id: str, title: str, description: str,
                   goal_type: GoalType, target_value: int, unit: str = "",
                   target_date: Optional[datetime] = None) -> Goal:
        """
        创建目标
        
        Args:
            user_id: 用户ID
            title: 目标标题
            description: 目标描述
            goal_type: 目标类型
            target_value: 目标值
            unit: 单位
            target_date: 目标完成日期
            
        Returns:
            创建的目标
        """
        goal_id = f"goal_{user_id}_{datetime.now().timestamp()}"
        
        # 自动generate里程碑
        milestones = self._generate_milestones(target_value, goal_type)
        
        goal = Goal(
            id=goal_id,
            user_id=user_id,
            title=title,
            description=description,
            type=goal_type,
            target_value=target_value,
            unit=unit,
            target_date=target_date,
            milestones=milestones
        )
        
        self.goals[goal_id] = goal
        
        if user_id not in self.user_goals:
            self.user_goals[user_id] = []
        self.user_goals[user_id].append(goal_id)
        
        return goal
    
    def _generate_milestones(self, target_value: int, goal_type: GoalType) -> List[Dict[str, Any]]:
        """generate里程碑"""
        milestones = []
        
        if goal_type == GoalType.SHORT_TERM:
            # 短期目标:25%, 50%, 75%, 100%
            percentages = [25, 50, 75, 100]
        elif goal_type == GoalType.MEDIUM_TERM:
            # 中期目标:20%, 40%, 60%, 80%, 100%
            percentages = [20, 40, 60, 80, 100]
        else:
            # 长期目标:10%, 25%, 50%, 75%, 90%, 100%
            percentages = [10, 25, 50, 75, 90, 100]
        
        for pct in percentages:
            milestones.append({
                "percentage": pct,
                "value": int(target_value * pct / 100),
                "reached": False,
                "reached_at": None
            })
        
        return milestones
    
    def update_goal_progress(self, goal_id: str, new_value: int, note: str = "") -> Dict[str, Any]:
        """
        更新目标进度
        
        Args:
            goal_id: 目标ID
            new_value: 新进度值
            note: 备注
            
        Returns:
            更新结果,包含触发的里程碑和完成状态
        """
        if goal_id not in self.goals:
            return {"error": "Goal not found"}
        
        goal = self.goals[goal_id]
        old_value = goal.current_value
        goal.current_value = new_value
        
        # 记录进度
        self.progress_tracker.record_progress(goal_id, old_value, new_value, note)
        
        result = {
            "goal_id": goal_id,
            "old_progress": int(old_value / goal.target_value * 100) if goal.target_value > 0 else 0,
            "new_progress": goal.get_progress_percentage(),
            "milestones_reached": [],
            "is_completed": False
        }
        
        # 检查里程碑
        for milestone in goal.milestones:
            if not milestone["reached"] and new_value >= milestone["value"]:
                milestone["reached"] = True
                milestone["reached_at"] = datetime.now().isoformat()
                result["milestones_reached"].append(milestone)
        
        # 检查是否完成
        if new_value >= goal.target_value and goal.status != GoalStatus.COMPLETED:
            goal.status = GoalStatus.COMPLETED
            goal.completed_at = datetime.now()
            result["is_completed"] = True
            
            # 触发成功回调
            self._trigger_success_callbacks(goal)
        
        return result
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """get目标"""
        return self.goals.get(goal_id)
    
    def get_user_goals(self, user_id: str, status: Optional[GoalStatus] = None) -> List[Goal]:
        """
        get用户的目标列表
        
        Args:
            user_id: 用户ID
            status: 筛选状态
            
        Returns:
            目标列表
        """
        goal_ids = self.user_goals.get(user_id, [])
        goals = [self.goals[gid] for gid in goal_ids if gid in self.goals]
        
        if status:
            goals = [g for g in goals if g.status == status]
        
        return goals
    
    def get_goal_dashboard(self, user_id: str) -> Dict[str, Any]:
        """
        get用户目标仪表盘
        
        Args:
            user_id: 用户ID
            
        Returns:
            仪表盘数据
        """
        goals = self.get_user_goals(user_id)
        
        active_goals = [g for g in goals if g.status == GoalStatus.ACTIVE]
        completed_goals = [g for g in goals if g.status == GoalStatus.COMPLETED]
        
        # 计算整体进度
        total_progress = 0
        at_risk_goals = []
        
        for goal in active_goals:
            total_progress += goal.get_progress_percentage()
            if not goal.is_on_track():
                at_risk_goals.append({
                    "id": goal.id,
                    "title": goal.title,
                    "progress": goal.get_progress_percentage(),
                    "reason": "进度落后于计划"
                })
        
        avg_progress = total_progress / len(active_goals) if active_goals else 0
        
        return {
            "summary": {
                "total_goals": len(goals),
                "active_goals": len(active_goals),
                "completed_goals": len(completed_goals),
                "completion_rate": len(completed_goals) / len(goals) * 100 if goals else 0,
                "average_progress": round(avg_progress, 1)
            },
            "active_goals": [
                {
                    "id": g.id,
                    "title": g.title,
                    "progress": g.get_progress_percentage(),
                    "current": g.current_value,
                    "target": g.target_value,
                    "unit": g.unit,
                    "on_track": g.is_on_track(),
                    "days_remaining": (g.target_date - datetime.now()).days if g.target_date else None
                }
                for g in active_goals
            ],
            "recent_completed": [
                {
                    "id": g.id,
                    "title": g.title,
                    "completed_at": g.completed_at.isoformat() if g.completed_at else None
                }
                for g in sorted(completed_goals, key=lambda x: x.completed_at or datetime.min, reverse=True)[:5]
            ],
            "at_risk_goals": at_risk_goals,
            "recommendations": self._generate_recommendations(user_id, active_goals, at_risk_goals)
        }
    
    def _generate_recommendations(self, user_id: str, active_goals: List[Goal], 
                                 at_risk_goals: List[Dict]) -> List[str]:
        """generate建议"""
        recommendations = []
        
        if at_risk_goals:
            recommendations.append(f"您有 {len(at_risk_goals)} 个目标进度落后,建议调整计划或分解任务")
        
        if len(active_goals) > 5:
            recommendations.append("同时进行的目標较多,建议优先完成最重要的2-3个")
        
        if not active_goals:
            recommendations.append("当前没有进行中的目标,建议设定一个新目标")
        
        # 基于进度速度的建议
        for goal in active_goals:
            velocity = self.progress_tracker.get_velocity(goal.id, days=7)
            if velocity > 0 and goal.target_date:
                days_needed = (goal.target_value - goal.current_value) / velocity
                days_remaining = (goal.target_date - datetime.now()).days
                
                if days_needed > days_remaining:
                    recommendations.append(f"目标'{goal.title}'需要加快速度,建议每天多完成 {int((days_needed - days_remaining) / days_remaining * 100)}%")
        
        return recommendations
    
    def detect_obstacles(self, user_id: str) -> List[Dict[str, Any]]:
        """
        检测用户可能遇到的障碍
        
        Returns:
            检测到的障碍列表
        """
        obstacles = []
        goals = self.get_user_goals(user_id, GoalStatus.ACTIVE)
        
        for goal in goals:
            # 检查是否停滞
            history = self.progress_tracker.get_progress_history(goal.id)
            if len(history) >= 2:
                last_update = history[-1].update_time
                days_since_update = (datetime.now() - last_update).days
                
                if days_since_update > 7:
                    obstacles.append({
                        "goal_id": goal.id,
                        "goal_title": goal.title,
                        "type": "stalled",
                        "description": f"目标'{goal.title}'已停滞 {days_since_update} 天",
                        "suggestion": "建议分解为更小的任务,或调整目标难度"
                    })
            
            # 检查是否落后
            if not goal.is_on_track():
                obstacles.append({
                    "goal_id": goal.id,
                    "goal_title": goal.title,
                    "type": "behind_schedule",
                    "description": f"目标'{goal.title}'进度落后于计划",
                    "suggestion": "建议重新评估时间安排,或增加投入时间"
                })
        
        return obstacles
    
    def suggest_goal_breakdown(self, goal_id: str) -> List[Dict[str, Any]]:
        """
        建议目标分解
        
        将大目标分解为可执行的小步骤
        """
        goal = self.goals.get(goal_id)
        if not goal:
            return []
        
        remaining = goal.target_value - goal.current_value
        
        if goal.type == GoalType.LONG_TERM:
            # 长期目标:按月分解
            if goal.target_date:
                months_remaining = max(1, (goal.target_date - datetime.now()).days // 30)
                monthly_target = remaining // months_remaining
                
                return [
                    {
                        "step": f"第{i+1}个月",
                        "target": min(monthly_target, remaining - i * monthly_target),
                        "unit": goal.unit,
                        "focus": f"完成 {min(monthly_target, remaining - i * monthly_target)} {goal.unit}"
                    }
                    for i in range(months_remaining)
                ]
        
        elif goal.type == GoalType.MEDIUM_TERM:
            # 中期目标:按周分解
            weeks = 4
            weekly_target = remaining // weeks
            
            return [
                {
                    "step": f"第{i+1}周",
                    "target": min(weekly_target, remaining - i * weekly_target),
                    "unit": goal.unit,
                    "focus": f"完成 {min(weekly_target, remaining - i * weekly_target)} {goal.unit}"
                }
                for i in range(weeks)
            ]
        
        else:
            # 短期目标:按天分解
            days = 7
            daily_target = max(1, remaining // days)
            
            return [
                {
                    "step": f"第{i+1}天",
                    "target": min(daily_target, remaining - i * daily_target),
                    "unit": goal.unit,
                    "focus": f"完成 {min(daily_target, remaining - i * daily_target)} {goal.unit}"
                }
                for i in range(days) if remaining - i * daily_target > 0
            ]
    
    def on_goal_completed(self, callback: Callable):
        """注册目标完成回调"""
        self.success_callbacks.append(callback)
    
    def _trigger_success_callbacks(self, goal: Goal):
        """触发成功回调"""
        for callback in self.success_callbacks:
            try:
                callback(goal)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def get_success_insights(self, user_id: str) -> Dict[str, Any]:
        """get用户成功洞察"""
        goals = self.get_user_goals(user_id)
        completed = [g for g in goals if g.status == GoalStatus.COMPLETED]
        
        if not completed:
            return {
                "message": "完成第一个目标,开启您的成功之旅!",
                "suggestion": "建议从一个小目标开始"
            }
        
        # 计算平均完成时间
        completion_times = []
        for goal in completed:
            if goal.completed_at and goal.created_at:
                days = (goal.completed_at - goal.created_at).days
                completion_times.append(days)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # 找出最擅长的目标类型
        type_success = {}
        for goal in completed:
            type_success[goal.type.value] = type_success.get(goal.type.value, 0) + 1
        
        best_type = max(type_success, key=type_success.get) if type_success else None
        
        return {
            "total_completed": len(completed),
            "average_completion_days": round(avg_completion_time, 1),
            "best_goal_type": best_type,
            "completion_rate": len(completed) / len(goals) * 100 if goals else 0,
            "strength": f"您擅长完成{best_type}目标" if best_type else "",
            "suggestion": "继续保持,挑战更高难度的目标!"
        }
