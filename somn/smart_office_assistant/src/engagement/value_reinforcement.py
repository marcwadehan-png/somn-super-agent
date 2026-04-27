"""
__all__ = [
    'generate_weekly_report',
    'get_dashboard',
    'is_reached',
    'is_unlocked',
    'update_metrics',
]

价值强化系统 - 让用户清晰感知产品价值
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

class AchievementType(Enum):
    """成就类型"""
    USAGE = "usage"           # 使用成就
    EXPLORATION = "exploration"  # 功能探索
    EFFICIENCY = "efficiency"    # 效率提升
    SOCIAL = "social"         # 社交贡献
    MASTERY = "mastery"       # 技能掌握

@dataclass
class Achievement:
    """成就"""
    id: str
    name: str
    description: str
    type: AchievementType
    icon: str
    condition: Dict[str, Any]  # 触发条件
    value_message: str  # 价值展示文案
    unlocked_at: Optional[datetime] = None
    
    def is_unlocked(self) -> bool:
        return self.unlocked_at is not None

@dataclass
class Milestone:
    """里程碑"""
    id: str
    name: str
    description: str
    threshold: int  # 阈值
    unit: str  # 单位
    value_message: str
    reached_at: Optional[datetime] = None
    
    def is_reached(self, current_value: int) -> bool:
        return current_value >= self.threshold

@dataclass
class ValueMetrics:
    """价值metrics"""
    time_saved_minutes: int = 0
    tasks_completed: int = 0
    efficiency_score: float = 0.0
    streak_days: int = 0
    last_used: Optional[datetime] = None

class ValueReinforcementSystem:
    """
    价值强化系统
    
    通过可视化展示用户获得的价值,强化用户对产品的正面认知
    """
    
    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.milestones: List[Milestone] = []
        self.user_metrics: Dict[str, ValueMetrics] = {}
        self._initialize_default_achievements()
        self._initialize_default_milestones()
    
    def _initialize_default_achievements(self):
        """init默认成就"""
        default_achievements = [
            Achievement(
                id="first_use",
                name="初次体验",
                description="完成首次任务",
                type=AchievementType.USAGE,
                icon="🎯",
                condition={"tasks_completed": 1},
                value_message="迈出了效率提升的第一步!"
            ),
            Achievement(
                id="week_warrior",
                name="周度达人",
                description="连续使用7天",
                type=AchievementType.USAGE,
                icon="🔥",
                condition={"streak_days": 7},
                value_message="连续7天使用,好习惯正在养成!"
            ),
            Achievement(
                id="efficiency_master",
                name="效率大师",
                description="累计节省50小时",
                type=AchievementType.EFFICIENCY,
                icon="⚡",
                condition={"time_saved_minutes": 3000},
                value_message="您已节省50小时,相当于多读了10本书!"
            ),
            Achievement(
                id="feature_explorer",
                name="功能探索者",
                description="使用了80%的功能",
                type=AchievementType.EXPLORATION,
                icon="🔍",
                condition={"feature_usage_rate": 0.8},
                value_message="您已掌握产品的大部分功能!"
            ),
            Achievement(
                id="productivity_pro",
                name="效率专家",
                description="完成100个任务",
                type=AchievementType.MASTERY,
                icon="🏆",
                condition={"tasks_completed": 100},
                value_message="100个任务完成,您已是效率专家!"
            ),
        ]
        
        for achievement in default_achievements:
            self.achievements[achievement.id] = achievement
    
    def _initialize_default_milestones(self):
        """init默认里程碑"""
        self.milestones = [
            Milestone(
                id="time_10h",
                name="时间节省者",
                description="累计节省10小时",
                threshold=600,
                unit="分钟",
                value_message="已节省10小时,可以看完一部经典电影了!"
            ),
            Milestone(
                id="time_50h",
                name="效率先锋",
                description="累计节省50小时",
                threshold=3000,
                unit="分钟",
                value_message="已节省50小时,相当于多读了10本书!"
            ),
            Milestone(
                id="time_100h",
                name="时间大师",
                description="累计节省100小时",
                threshold=6000,
                unit="分钟",
                value_message="已节省100小时,相当于完成一个短期课程!"
            ),
            Milestone(
                id="tasks_10",
                name="任务新手",
                description="完成10个任务",
                threshold=10,
                unit="个",
                value_message="已完成10个任务,效率提升看得见!"
            ),
            Milestone(
                id="tasks_100",
                name="任务达人",
                description="完成100个任务",
                threshold=100,
                unit="个",
                value_message="已完成100个任务,您的工作效率已大幅提升!"
            ),
        ]
    
    def update_metrics(self, user_id: str, **kwargs) -> Dict[str, Any]:
        """
        更新用户metrics
        
        Args:
            user_id: 用户ID
            **kwargs: 更新的metrics
            
        Returns:
            触发的成就和里程碑
        """
        if user_id not in self.user_metrics:
            self.user_metrics[user_id] = ValueMetrics()
        
        metrics = self.user_metrics[user_id]
        
        # 更新metrics
        if "time_saved_minutes" in kwargs:
            metrics.time_saved_minutes += kwargs["time_saved_minutes"]
        if "tasks_completed" in kwargs:
            metrics.tasks_completed += kwargs["tasks_completed"]
        if "efficiency_score" in kwargs:
            metrics.efficiency_score = kwargs["efficiency_score"]
        if "streak_days" in kwargs:
            metrics.streak_days = kwargs["streak_days"]
        
        metrics.last_used = datetime.now()
        
        # 检查成就和里程碑
        triggered = self._check_triggers(user_id, metrics)
        
        return triggered
    
    def _check_triggers(self, user_id: str, metrics: ValueMetrics) -> Dict[str, Any]:
        """检查触发的成就和里程碑"""
        triggered = {
            "achievements": [],
            "milestones": []
        }
        
        # 检查成就
        for achievement_id, achievement in self.achievements.items():
            if achievement.is_unlocked():
                continue
            
            condition = achievement.condition
            unlocked = False
            
            if "tasks_completed" in condition:
                if metrics.tasks_completed >= condition["tasks_completed"]:
                    unlocked = True
            if "time_saved_minutes" in condition:
                if metrics.time_saved_minutes >= condition["time_saved_minutes"]:
                    unlocked = True
            if "streak_days" in condition:
                if metrics.streak_days >= condition["streak_days"]:
                    unlocked = True
            
            if unlocked:
                achievement.unlocked_at = datetime.now()
                triggered["achievements"].append(achievement)
        
        # 检查里程碑
        for milestone in self.milestones:
            if milestone.reached_at:
                continue
            
            current_value = 0
            if "time" in milestone.id:
                current_value = metrics.time_saved_minutes
            elif "tasks" in milestone.id:
                current_value = metrics.tasks_completed
            
            if milestone.is_reached(current_value):
                milestone.reached_at = datetime.now()
                triggered["milestones"].append(milestone)
        
        return triggered
    
    def get_dashboard(self, user_id: str) -> Dict[str, Any]:
        """
        get用户价值仪表盘
        
        Args:
            user_id: 用户ID
            
        Returns:
            仪表盘数据
        """
        metrics = self.user_metrics.get(user_id, ValueMetrics())
        
        # 计算等效价值
        hours_saved = metrics.time_saved_minutes / 60
        days_saved = hours_saved / 8  # 按8小时工作日计算
        
        return {
            "summary": {
                "time_saved_hours": round(hours_saved, 1),
                "time_saved_days": round(days_saved, 1),
                "tasks_completed": metrics.tasks_completed,
                "efficiency_score": round(metrics.efficiency_score, 1),
                "current_streak": metrics.streak_days
            },
            "equivalencies": self._calculate_equivalencies(hours_saved),
            "achievements": self._get_user_achievements(user_id),
            "next_milestones": self._get_next_milestones(metrics),
            "progress": self._calculate_progress(metrics)
        }
    
    def _calculate_equivalencies(self, hours_saved: float) -> List[Dict[str, str]]:
        """计算等效价值"""
        equivalencies = []
        
        if hours_saved >= 1:
            equivalencies.append({
                "icon": "📚",
                "text": f"相当于读了 {int(hours_saved / 5)} 本书"
            })
        if hours_saved >= 2:
            equivalencies.append({
                "icon": "🎬",
                "text": f"相当于看了 {int(hours_saved / 2)} 部电影"
            })
        if hours_saved >= 8:
            equivalencies.append({
                "icon": "🏖️",
                "text": f"相当于多休了 {int(hours_saved / 8)} 天假"
            })
        if hours_saved >= 40:
            equivalencies.append({
                "icon": "🎓",
                "text": f"相当于完成一个 {int(hours_saved / 40)} 周的课程"
            })
        
        return equivalencies
    
    def _get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """get用户成就"""
        return [
            {
                "id": a.id,
                "name": a.name,
                "description": a.description,
                "icon": a.icon,
                "unlocked": a.is_unlocked(),
                "unlocked_at": a.unlocked_at.isoformat() if a.unlocked_at else None
            }
            for a in self.achievements.values()
        ]
    
    def _get_next_milestones(self, metrics: ValueMetrics) -> List[Dict[str, Any]]:
        """get下一个里程碑"""
        next_milestones = []
        
        for milestone in self.milestones:
            if milestone.reached_at:
                continue
            
            current_value = 0
            if "time" in milestone.id:
                current_value = metrics.time_saved_minutes
            elif "tasks" in milestone.id:
                current_value = metrics.tasks_completed
            
            progress = min(100, int(current_value / milestone.threshold * 100))
            
            next_milestones.append({
                "id": milestone.id,
                "name": milestone.name,
                "description": milestone.description,
                "progress": progress,
                "remaining": milestone.threshold - current_value
            })
        
        # 按进度排序,返回前3个
        next_milestones.sort(key=lambda x: x["progress"], reverse=True)
        return next_milestones[:3]
    
    def _calculate_progress(self, metrics: ValueMetrics) -> Dict[str, Any]:
        """计算整体进度"""
        total_achievements = len(self.achievements)
        unlocked_achievements = sum(1 for a in self.achievements.values() if a.is_unlocked())
        
        total_milestones = len(self.milestones)
        reached_milestones = sum(1 for m in self.milestones if m.reached_at)
        
        return {
            "achievement_progress": {
                "current": unlocked_achievements,
                "total": total_achievements,
                "percentage": int(unlocked_achievements / total_achievements * 100)
            },
            "milestone_progress": {
                "current": reached_milestones,
                "total": total_milestones,
                "percentage": int(reached_milestones / total_milestones * 100)
            }
        }
    
    def generate_weekly_report(self, user_id: str) -> Dict[str, Any]:
        """generate周报"""
        metrics = self.user_metrics.get(user_id, ValueMetrics())
        
        return {
            "period": "本周",
            "highlights": [
                f"完成 {metrics.tasks_completed} 个任务",
                f"节省 {metrics.time_saved_minutes // 60} 小时",
                f"连续使用 {metrics.streak_days} 天"
            ],
            "achievements_unlocked": [
                a.name for a in self.achievements.values() 
                if a.is_unlocked() and a.unlocked_at and 
                (datetime.now() - a.unlocked_at).days <= 7
            ],
            "next_week_goals": [
                "继续使用,保持效率提升",
                "探索新功能,发现更多价值",
                f"距离下一个里程碑还需XX {self.milestones[0].unit}"
            ]
        }
