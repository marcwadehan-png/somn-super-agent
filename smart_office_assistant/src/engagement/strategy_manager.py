"""
engagement/strategy_manager.py — 策略管理（从 strategy_engine 合并）
================================================
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

# 目标优先级（策略引擎专用，与 user_success.GoalPriority 分开）
class StrategyGoalPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# 目标状态（策略引擎专用）
class StrategyGoalStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class StrategyGoal:
    """策略目标（区别于 user_success.Goal）"""
    id: str
    name: str
    description: str
    target_value: float
    current_value: float = 0.0
    unit: str = ""
    priority: StrategyGoalPriority = StrategyGoalPriority.MEDIUM
    status: StrategyGoalStatus = StrategyGoalStatus.PENDING
    deadline: Optional[datetime] = None
    parent_id: Optional[str] = None
    sub_goals: List[str] = field(default_factory=list)
    metrics: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def progress(self) -> float:
        if self.target_value == 0:
            return 0.0
        return min(1.0, self.current_value / self.target_value)

    @property
    def is_overdue(self) -> bool:
        if self.deadline is None:
            return False
        return datetime.now() > self.deadline

@dataclass
class Strategy:
    """策略定义"""
    id: str
    name: str
    description: str
    goal_id: str
    actions: List[Dict[str, Any]] = field(default_factory=list)
    expected_outcome: Dict[str, float] = field(default_factory=dict)
    required_resources: List[str] = field(default_factory=list)
    timeline_days: int = 30
    dependencies: List[str] = field(default_factory=list)
    risk_level: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'goal_id': self.goal_id,
            'actions': self.actions,
            'expected_outcome': self.expected_outcome,
            'required_resources': self.required_resources,
            'timeline_days': self.timeline_days,
            'risk_level': self.risk_level,
        }

@dataclass
class ActionPlan:
    """行动计划"""
    id: str
    strategy_id: str
    phases: List[Dict[str, Any]] = field(default_factory=list)
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    total_duration_days: int = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class StrategyEngine:
    """策略引擎 — 核心策略生成和管理（合并到 engagement）"""

    def __init__(self):
        self.goals: Dict[str, StrategyGoal] = {}
        self.strategies: Dict[str, Strategy] = {}
        self.action_plans: Dict[str, ActionPlan] = {}
        self.strategy_templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Any]:
        return {
            'growth': {
                'name': '增长策略',
                'phases': [
                    {'name': '分析诊断', 'duration': 7, 'tasks': ['数据分析', '竞品研究']},
                    {'name': '策略制定', 'duration': 5, 'tasks': ['目标设定', '方案设计']},
                    {'name': '执行实施', 'duration': 14, 'tasks': ['内容生产', '渠道投放']},
                    {'name': '优化迭代', 'duration': 7, 'tasks': ['效果监测', '策略调整']}
                ]
            },
            'optimization': {
                'name': '优化策略',
                'phases': [
                    {'name': '现状评估', 'duration': 5, 'tasks': ['性能分析', '问题识别']},
                    {'name': '方案设计', 'duration': 7, 'tasks': ['优化方案', '资源规划']},
                    {'name': '实施优化', 'duration': 10, 'tasks': ['逐步优化', 'A/B测试']},
                    {'name': '效果验证', 'duration': 5, 'tasks': ['数据验证', '总结报告']}
                ]
            },
            'innovation': {
                'name': '创新策略',
                'phases': [
                    {'name': '创意探索', 'duration': 10, 'tasks': ['头脑风暴', '趋势研究']},
                    {'name': '概念验证', 'duration': 7, 'tasks': ['原型开发', '用户测试']},
                    {'name': '产品开发', 'duration': 21, 'tasks': ['功能开发', '迭代优化']},
                    {'name': '市场推广', 'duration': 14, 'tasks': ['发布准备', '市场投放']}
                ]
            }
        }

    def create_goal(self, name: str, description: str,
                       target_value: float, unit: str = "",
                       priority: str = "medium",
                       deadline: Optional[datetime] = None,
                       parent_id: Optional[str] = None) -> StrategyGoal:
        goal_id = f"sg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        goal = StrategyGoal(
            id=goal_id, name=name, description=description,
            target_value=target_value, unit=unit,
            priority=StrategyGoalPriority(priority),
            deadline=deadline, parent_id=parent_id
        )
        self.goals[goal_id] = goal
        if parent_id and parent_id in self.goals:
            self.goals[parent_id].sub_goals.append(goal_id)
        return goal

    def decompose_goal(self, goal_id: str, sub_goals_config: List[Dict]) -> List[StrategyGoal]:
        if goal_id not in self.goals:
            return []
        parent = self.goals[goal_id]
        sub_goals = []
        for config in sub_goals_config:
            sg = self.create_goal(
                name=config['name'],
                description=config.get('description', ''),
                target_value=config['target_value'],
                unit=config.get('unit', parent.unit),
                priority=config.get('priority', 'medium'),
                deadline=config.get('deadline'),
                parent_id=goal_id
            )
            sub_goals.append(sg)
        return sub_goals

    def generate_strategy(self, goal_id: str, strategy_type: str = "growth",
                            constraints: Optional[Dict] = None) -> Optional[Strategy]:
        if goal_id not in self.goals:
            return None
        goal = self.goals[goal_id]
        template = self.strategy_templates.get(strategy_type, self.strategy_templates['growth'])
        strategy_id = f"st_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        actions = self._generate_actions(goal, template, constraints)
        expected_outcome = self._calculate_expected_outcome(goal, actions)
        required_resources = self._identify_resources(actions)
        strategy = Strategy(
            id=strategy_id, name=f"{goal.name} - {template['name']}",
            description=f"为实现'{goal.name}'目标制定的{template['name']}",
            goal_id=goal_id, actions=actions,
            expected_outcome=expected_outcome,
            required_resources=required_resources,
            timeline_days=sum(p['duration'] for p in template['phases'])
        )
        self.strategies[strategy_id] = strategy
        return strategy

    def _generate_actions(self, goal: StrategyGoal, template: Dict,
                           constraints: Optional[Dict]) -> List[Dict]:
        actions = []
        for phase in template['phases']:
            for task in phase['tasks']:
                action = {
                    'name': task,
                    'phase': phase['name'],
                    'duration_days': max(1, phase['duration'] // len(phase['tasks'])),
                    'status': 'pending', 'assigned_to': None, 'dependencies': []
                }
                if '增长' in goal.name or 'growth' in goal.name.lower():
                    if task == '内容生产':
                        action['details'] = '创建高质量内容，目标提升用户参与度'
                    elif task == '渠道投放':
                        action['details'] = '在目标渠道进行精准投放'
                actions.append(action)
        return actions

    def _calculate_expected_outcome(self, goal: StrategyGoal,
                                      actions: List[Dict]) -> Dict[str, float]:
        action_count = len(actions)
        return {
            'target_achievement': min(0.95, 0.7 + action_count * 0.02),
            'timeline_variance_days': max(-7, min(7, action_count - 20)),
            'resource_utilization': 0.85,
            'risk_mitigation': 0.75
        }

    def _identify_resources(self, actions: List[Dict]) -> List[str]:
        resources = set()
        resource_map = {
            '数据分析': ['数据分析师', '分析工具'],
            '竞品研究': ['研究员', '调研预算'],
            '内容生产': ['内容创作者', '设计资源'],
            '渠道投放': ['投放预算', '渠道账号'],
            '用户测试': ['测试用户', '测试环境'],
            '产品开发': ['开发团队', '技术资源']
        }
        for action in actions:
            if action['name'] in resource_map:
                resources.update(resource_map[action['name']])
        return list(resources)

    def create_action_plan(self, strategy_id: str) -> Optional[ActionPlan]:
        if strategy_id not in self.strategies:
            return None
        strategy = self.strategies[strategy_id]
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        phases = []
        milestones = []
        current_date = datetime.now()
        phase_groups: Dict[str, List[Dict]] = {}
        for action in strategy.actions:
            phase_name = action['phase']
            if phase_name not in phase_groups:
                phase_groups[phase_name] = []
            phase_groups[phase_name].append(action)
        for phase_name, phase_actions in phase_groups.items():
            phase_duration = sum(a['duration_days'] for a in phase_actions)
            phase = {
                'name': phase_name,
                'start_date': current_date,
                'end_date': current_date + timedelta(days=phase_duration),
                'actions': phase_actions, 'status': 'pending'
            }
            phases.append(phase)
            milestones.append({
                'name': f"完成{phase_name}",
                'date': phase['end_date'],
                'criteria': [f"完成{a['name']}" for a in phase_actions],
                'status': 'pending'
            })
            current_date = phase['end_date']
        plan = ActionPlan(
            id=plan_id, strategy_id=strategy_id,
            phases=phases, milestones=milestones,
            total_duration_days=strategy.timeline_days,
            start_date=datetime.now(), end_date=current_date
        )
        self.action_plans[plan_id] = plan
        return plan

    def evaluate_strategy(self, strategy_id: str) -> Dict[str, Any]:
        if strategy_id not in self.strategies:
            return {'error': 'Strategy not found'}
        strategy = self.strategies[strategy_id]
        goal = self.goals.get(strategy.goal_id)
        if not goal:
            return {'error': 'Associated goal not found'}
        feasibility_score = self._evaluate_feasibility(strategy, goal)
        risk_assessment = self._assess_risk(strategy)
        return {
            'strategy_id': strategy_id,
            'goal_alignment': 0.85,
            'feasibility': feasibility_score,
            'risk_assessment': risk_assessment,
            'overall_score': (feasibility_score + risk_assessment['score']) / 2,
            'recommendations': []
        }

    def _evaluate_feasibility(self, strategy: Strategy, goal: StrategyGoal) -> float:
        score = 0.7
        if goal.deadline:
            days_available = (goal.deadline - datetime.now()).days
            if days_available >= strategy.timeline_days:
                score += 0.15
            elif days_available >= strategy.timeline_days * 0.8:
                score += 0.05
            else:
                score -= 0.2
        clear_actions = sum(1 for a in strategy.actions if a.get('details'))
        if strategy.actions:
            score += (clear_actions / len(strategy.actions)) * 0.1
        return max(0.0, min(1.0, score))

    def _assess_risk(self, strategy: Strategy) -> Dict[str, Any]:
        risks = []
        if strategy.timeline_days < 14:
            risks.append({'type': 'time', 'level': 'high', 'desc': '时间周期较短'})
        if len(strategy.required_resources) > 5:
            risks.append({'type': 'resource', 'level': 'medium', 'desc': '资源需求较多'})
        risk_score = 1.0
        for risk in risks:
            if risk['level'] == 'high':
                risk_score -= 0.15
            elif risk['level'] == 'medium':
                risk_score -= 0.08
        return {
            'score': max(0.0, risk_score),
            'risks': risks,
            'mitigation_suggestions': ['建立风险监控机制', '准备备选方案']
        }

    def get_goal_status(self, goal_id: str) -> Dict[str, Any]:
        if goal_id not in self.goals:
            return {'error': 'Goal not found'}
        goal = self.goals[goal_id]
        related_strategies = [s for s in self.strategies.values() if s.goal_id == goal_id]
        return {
            'goal': {'id': goal.id, 'name': goal.name, 'progress': goal.progress,
                      'status': goal.status.value, 'is_overdue': goal.is_overdue},
            'strategies': [{'id': s.id, 'name': s.name,
                             'timeline_days': s.timeline_days} for s in related_strategies],
        }

def create_strategy_engine() -> StrategyEngine:
    return StrategyEngine()
