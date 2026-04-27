"""
__all__ = [
    'create_goal',
    'decide',
    'decide_with_yangming',
    'get_cultivation_daily',
    'get_status',
    'get_yangming_summary',
    'start',
    'stop',
    'verify_knowing_and_action',
]

unified自主智能体核心 - Autonomous Agent Core
整合五大核心系统 + 王阳明xinxuefusion
v8.2.0
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from loguru import logger

from .goal_system import GoalSystem, Goal, GoalStatus, GoalPriority
from .autonomous_scheduler import AutonomousScheduler, TaskPriority
from .reflection_engine import ReflectionEngine, ActionType, OutcomeStatus
from .state_manager import StateManager, AgentMode
from .value_system import ValueSystem, DecisionType

# 导入王阳明xinxuefusion引擎（v8.2.0 P0修复：兼容src/和smart_office_assistant/两种Python路径场景）
try:
    from src.intelligence.engines.philosophy.yangming_autonomous_fusion import 王阳明fusion引擎, xinxuedecision模式
    YANGMING_AVAILABLE = True
except ImportError:
    try:
        from intelligence.engines.philosophy.yangming_autonomous_fusion import 王阳明fusion引擎, xinxuedecision模式
        YANGMING_AVAILABLE = True
    except ImportError:
        YANGMING_AVAILABLE = False
        logger.warning("王阳明xinxuefusion模块未加载")

@dataclass
class AgentConfig:
    enable_autonomous_mode: bool = True
    enable_yangming: bool = True       # 启用王阳明xinxue
    check_interval: int = 60
    max_concurrent_tasks: int = 3
    storage_path: str = "data/autonomous"

class AutonomousAgent:
    """自主智能体 - Somn v8.2.0 fusion王阳明xinxue"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.storage_path = Path(self.config.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("=" * 50)
        logger.info("init自主智能体 v8.2.0...")
        logger.info("=" * 50)
        
        # init五大核心系统
        self.goal_system = GoalSystem(str(self.storage_path / "goals"))
        self.scheduler = AutonomousScheduler(
            str(self.storage_path / "scheduler"),
            self.config.check_interval,
            self.config.max_concurrent_tasks
        )
        self.reflection = ReflectionEngine(str(self.storage_path / "reflection"))
        self.state = StateManager(str(self.storage_path / "state"))
        self.value_system = ValueSystem(str(self.storage_path / "values"))
        
        # init王阳明xinxuefusion引擎
        self.yangming_fusion = None
        if YANGMING_AVAILABLE and self.config.enable_yangming:
            try:
                from src.intelligence.engines.philosophy.yangming_autonomous_fusion import 王阳明fusion引擎
                self.yangming_fusion = 王阳明fusion引擎()
                logger.info("王阳明xinxuefusion引擎init完成")
            except Exception as e:
                logger.warning(f"王阳明xinxuefusion引擎init失败: {e}")
        
        self._register_callbacks()
        
        if self.config.enable_autonomous_mode:
            self.start()
        
        logger.info("自主智能体init完成")
    
    def _register_callbacks(self):
        self.scheduler.register_callback("check_goals", self._check_and_execute_goals)
        self.scheduler.register_callback("daily_reflection", self._daily_reflection)
    
    def start(self):
        logger.info("启动自主模式...")
        
        self.scheduler.schedule_periodic(
            name="目标检查",
            func=self._check_and_execute_goals,
            interval_seconds=self.config.check_interval,
            priority=TaskPriority.HIGH
        )
        
        self.scheduler.schedule_periodic(
            name="每日反思",
            func=self._daily_reflection,
            interval_seconds=86400,
            priority=TaskPriority.MEDIUM
        )
        
        self.scheduler.start()
        
        state = self.state.get_current_state()
        if state.current_task:
            logger.info(f"恢复任务: {state.current_task.task_name}")
        
        logger.info("自主模式已启动")
    
    def stop(self):
        logger.info("停止自主模式...")
        self.scheduler.stop()
        logger.info("自主模式已停止")
    
    def create_goal(self, title: str, **kwargs) -> Goal:
        goal = self.goal_system.create_goal(title=title, **kwargs)
        state = self.state.get_current_state()
        state.active_goals.append(goal.id)
        logger.info(f"创建目标: [{goal.id}] {title}")
        return goal
    
    def _check_and_execute_goals(self):
        ready_goals = self.goal_system.get_ready_goals()
        for goal in ready_goals[:self.config.max_concurrent_tasks]:
            if self.goal_system.start_goal(goal.id):
                self.reflection.start_execution(
                    action_type=ActionType.PLANNING,
                    action_name=f"执行目标: {goal.title}",
                    goal_id=goal.id
                )
                self.state.start_task(goal.id, goal.title)
                logger.info(f"开始执行目标: [{goal.id}] {goal.title}")
    
    def _daily_reflection(self):
        logger.info("执行每日反思...")
        patterns = self.reflection.extract_patterns(min_occurrences=2)
        logger.info(f"每日反思完成,提取 {len(patterns)} 个模式")
        return patterns
    
    def decide(self, options: List[Dict[str, Any]], context: Optional[Dict] = None) -> str:
        decision = self.value_system.make_decision(DecisionType.ACTION_SELECTION, options, context)
        return decision.selected_option
    
    def decide_with_yangming(self, situation: str, options: List[Dict[str, Any]], context: Optional[Dict] = None) -> Dict:
        """
        使用王阳明xinxue进行decision
        
        Args:
            situation: 情境描述
            options: 选项列表
            context: 上下文
            
        Returns:
            xinxuedecision结果
        """
        if not self.yangming_fusion:
            # 回退到普通decision
            return {"fallback": True, "result": self.decide(options, context)}
        
        return self.yangming_fusion.make_wisdom_decision(situation, options, context)
    
    def verify_knowing_and_action(self, knowledge: str, action: str, situation: str = "") -> Dict:
        """
        验证知行是否合一
        
        Args:
            knowledge: 所知
            action: 所行
            situation: 情境
            
        Returns:
            验证结果
        """
        if not self.yangming_fusion:
            return {"error": "王阳明xinxuefusion引擎未启用"}
        
        return self.yangming_fusion.verify_and_correct(knowledge, action, situation)
    
    def get_cultivation_daily(self) -> Dict:
        """get每日心性修养功课"""
        if not self.yangming_fusion:
            return {"error": "王阳明xinxuefusion引擎未启用"}
        
        return self.yangming_fusion.get_daily_cultivation()
    
    def get_yangming_summary(self) -> Dict:
        """get王阳明xinxue智慧摘要"""
        if not self.yangming_fusion:
            return {"error": "王阳明xinxuefusion引擎未启用"}
        
        return self.yangming_fusion.get_wisdom_summary()
    
    def get_status(self) -> Dict[str, Any]:
        state = self.state.get_current_state()
        status = {
            'version': 'v8.2.0',
            'session_id': state.session_id,
            'mode': state.mode.value,
            'current_task': state.current_task.to_dict() if state.current_task else None,
            'scheduler_running': self.scheduler._running,
            'goal_stats': self.goal_system.get_statistics(),
            'reflection_stats': self.reflection.get_statistics()
        }
        
        # 王阳明xinxue状态
        if self.yangming_fusion:
            status['yangming'] = {
                'enabled': True,
                'version': self.yangming_fusion.致良知.version,
                'decision_count': len(self.yangming_fusion.decision历史)
            }
        else:
            status['yangming'] = {'enabled': False}
        
        return status
