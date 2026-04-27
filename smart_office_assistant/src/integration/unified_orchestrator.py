"""
__all__ = [
    'get_all_workflows',
    'get_insights',
    'get_system_status',
    'get_workflow_status',
    'start',
    'stop',
    'to_dict',
    'trigger_workflow',
]

unified编排器
Unified Orchestrator

协调三大模块的协同工作,实现智能decision和自动化流程
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import uuid

# 导入事件总线和协调器
from .integration_events import (
    IntegrationEventBus, EventType, EventPriority, IntegrationEvent
)
from .module_coordinator import (
    ModuleCoordinator, ModuleType, ModuleStatus
)

logger = logging.getLogger(__name__)

class WorkflowType(Enum):
    """工作流类型"""
    EVOLUTION_KNOWLEDGE_SYNC = "evolution_knowledge_sync"  # 进化-知识同步
    KNOWLEDGE_GROWTH_RECOMMEND = "knowledge_growth_recommend"  # 知识-增长推荐
    FULL_CYCLE_OPTIMIZATION = "full_cycle_optimization"  # 全周期优化
    ANOMALY_RESPONSE = "anomaly_response"  # 异常响应
    STRATEGY_VALIDATION = "strategy_validation"  # strategy验证

class WorkflowStatus(Enum):
    """工作流状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowStep:
    """工作流步骤"""
    step_id: str
    name: str
    module: ModuleType
    action: str
    params: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class Workflow:
    """工作流"""
    workflow_id: str
    workflow_type: WorkflowType
    steps: List[WorkflowStep]
    status: WorkflowStatus
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None

@dataclass
class CrossModuleInsight:
    """跨模块洞察"""
    insight_id: str
    insight_type: str
    source_modules: List[ModuleType]
    description: str
    confidence: float
    recommendations: List[Dict]
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "insight_id": self.insight_id,
            "insight_type": self.insight_type,
            "source_modules": [m.value for m in self.source_modules],
            "description": self.description,
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "generated_at": self.generated_at.isoformat()
        }

class UnifiedOrchestrator:
    """unified编排器"""
    
    def __init__(self):
        self.event_bus = IntegrationEventBus()
        self.coordinator = ModuleCoordinator()
        self._workflows: Dict[str, Workflow] = {}
        self._insights: List[CrossModuleInsight] = []
        self._running = False
        self._main_loop_task: Optional[asyncio.Task] = None
        self._workflow_handlers: Dict[WorkflowType, Callable] = {}
        
        # 注册默认工作流处理器
        self._register_default_handlers()
        # 设置事件监听
        self._setup_event_listeners()
    
    def _register_default_handlers(self):
        """注册默认工作流处理器"""
        self._workflow_handlers[WorkflowType.EVOLUTION_KNOWLEDGE_SYNC] = self._handle_evolution_knowledge_sync
        self._workflow_handlers[WorkflowType.KNOWLEDGE_GROWTH_RECOMMEND] = self._handle_knowledge_growth_recommend
        self._workflow_handlers[WorkflowType.FULL_CYCLE_OPTIMIZATION] = self._handle_full_cycle_optimization
        self._workflow_handlers[WorkflowType.ANOMALY_RESPONSE] = self._handle_anomaly_response
    
    def _setup_event_listeners(self):
        """设置事件监听器"""
        # 监听进化引擎事件
        self.event_bus.subscribe(
            [EventType.EVOLUTION_COMPLETED, EventType.ANOMALY_DETECTED],
            self._on_evolution_event
        )
        
        # 监听知识图谱事件
        self.event_bus.subscribe(
            [EventType.KNOWLEDGE_UPDATED, EventType.INDUSTRY_COMPARED],
            self._on_knowledge_event
        )
        
        # 监听增长strategy事件
        self.event_bus.subscribe(
            [EventType.EXPERIMENT_COMPLETED, EventType.GROWTH_MILESTONE],
            self._on_growth_event
        )
    
    async def _on_evolution_event(self, event: IntegrationEvent):
        """处理进化引擎事件"""
        if event.event_type == EventType.EVOLUTION_COMPLETED:
            # 进化完成后,触发知识图谱更新
            await self.trigger_workflow(
                WorkflowType.EVOLUTION_KNOWLEDGE_SYNC,
                {"evolution_result": event.payload}
            )
        elif event.event_type == EventType.ANOMALY_DETECTED:
            # 检测到异常,触发异常响应
            await self.trigger_workflow(
                WorkflowType.ANOMALY_RESPONSE,
                {"anomaly": event.payload}
            )
    
    async def _on_knowledge_event(self, event: IntegrationEvent):
        """处理知识图谱事件"""
        if event.event_type == EventType.INDUSTRY_COMPARED:
            # 行业对比后,generate增长strategy推荐
            await self.trigger_workflow(
                WorkflowType.KNOWLEDGE_GROWTH_RECOMMEND,
                {"comparison_result": event.payload}
            )
    
    async def _on_growth_event(self, event: IntegrationEvent):
        """处理增长strategy事件"""
        if event.event_type == EventType.EXPERIMENT_COMPLETED:
            # 实验完成后,generate洞察
            insight = CrossModuleInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                insight_type="growth_experiment_result",
                source_modules=[ModuleType.GROWTH_STRATEGIES],
                description=f"增长实验完成: {event.payload.get('experiment_name', 'Unknown')}",
                confidence=event.payload.get('confidence', 0.8),
                recommendations=event.payload.get('recommendations', [])
            )
            self._insights.append(insight)
    
    async def start(self):
        """启动编排器"""
        if self._running:
            return
        
        self._running = True
        logger.info("unified编排器已启动")
        
        # 发布启动事件
        await self.event_bus.publish_sync(
            source_module="unified_orchestrator",
            event_type=EventType.WORKFLOW_TRIGGERED,
            payload={"action": "orchestrator_started"},
            priority=EventPriority.NORMAL
        )
    
    async def stop(self):
        """停止编排器"""
        self._running = False
        if self._main_loop_task:
            self._main_loop_task.cancel()
            try:
                await self._main_loop_task
            except asyncio.CancelledError:
                pass
        logger.info("unified编排器已停止")
    
    async def trigger_workflow(self, workflow_type: WorkflowType,
                              context: Dict[str, Any]) -> str:
        """触发工作流"""
        workflow_id = f"wf_{uuid.uuid4().hex[:12]}"
        correlation_id = self.event_bus.create_correlation_id()
        
        # 创建工作流
        workflow = Workflow(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            steps=self._create_workflow_steps(workflow_type, context),
            status=WorkflowStatus.PENDING,
            correlation_id=correlation_id,
            metadata=context
        )
        
        self._workflows[workflow_id] = workflow
        
        # 发布工作流触发事件
        await self.event_bus.publish_sync(
            source_module="unified_orchestrator",
            event_type=EventType.WORKFLOW_TRIGGERED,
            payload={
                "workflow_id": workflow_id,
                "workflow_type": workflow_type.value,
                "context": context
            },
            correlation_id=correlation_id
        )
        
        # 执行工作流
        asyncio.create_task(self._execute_workflow(workflow_id))
        
        logger.info(f"工作流已触发: {workflow_id} ({workflow_type.value})")
        return workflow_id
    
    def _create_workflow_steps(self, workflow_type: WorkflowType,
                               context: Dict[str, Any]) -> List[WorkflowStep]:
        """创建工作流步骤"""
        steps = []
        
        if workflow_type == WorkflowType.EVOLUTION_KNOWLEDGE_SYNC:
            steps = [
                WorkflowStep(
                    step_id="step_1",
                    name="get进化结果",
                    module=ModuleType.EVOLUTION_ENGINE,
                    action="get_evolution_result",
                    params={"evolution_id": context.get("evolution_result", {}).get("evolution_id")}
                ),
                WorkflowStep(
                    step_id="step_2",
                    name="更新知识图谱",
                    module=ModuleType.KNOWLEDGE_GRAPH,
                    action="add_entity",
                    params={"entity_data": context.get("evolution_result")},
                    depends_on=["step_1"]
                )
            ]
        elif workflow_type == WorkflowType.KNOWLEDGE_GROWTH_RECOMMEND:
            steps = [
                WorkflowStep(
                    step_id="step_1",
                    name="分析行业洞察",
                    module=ModuleType.KNOWLEDGE_GRAPH,
                    action="infer_relations",
                    params={"entity_id": context.get("comparison_result", {}).get("industry_id")}
                ),
                WorkflowStep(
                    step_id="step_2",
                    name="generate增长strategy",
                    module=ModuleType.GROWTH_STRATEGIES,
                    action="recommend_strategies",
                    params={"insights": context.get("comparison_result")},
                    depends_on=["step_1"]
                )
            ]
        elif workflow_type == WorkflowType.FULL_CYCLE_OPTIMIZATION:
            steps = [
                WorkflowStep(
                    step_id="step_1",
                    name="系统健康诊断",
                    module=ModuleType.EVOLUTION_ENGINE,
                    action="run_diagnostic",
                    params={}
                ),
                WorkflowStep(
                    step_id="step_2",
                    name="知识图谱推理",
                    module=ModuleType.KNOWLEDGE_GRAPH,
                    action="infer_all_relations",
                    params={},
                    depends_on=["step_1"]
                ),
                WorkflowStep(
                    step_id="step_3",
                    name="generate优化strategy",
                    module=ModuleType.GROWTH_STRATEGIES,
                    action="generate_optimization_plan",
                    params={},
                    depends_on=["step_2"]
                )
            ]
        elif workflow_type == WorkflowType.ANOMALY_RESPONSE:
            steps = [
                WorkflowStep(
                    step_id="step_1",
                    name="评估异常影响",
                    module=ModuleType.EVOLUTION_ENGINE,
                    action="assess_anomaly",
                    params={"anomaly": context.get("anomaly")}
                ),
                WorkflowStep(
                    step_id="step_2",
                    name="查询相关知识",
                    module=ModuleType.KNOWLEDGE_GRAPH,
                    action="find_related_cases",
                    params={"anomaly_type": context.get("anomaly", {}).get("type")},
                    depends_on=["step_1"]
                ),
                WorkflowStep(
                    step_id="step_3",
                    name="制定响应strategy",
                    module=ModuleType.GROWTH_STRATEGIES,
                    action="create_response_strategy",
                    params={},
                    depends_on=["step_2"]
                )
            ]
        
        return steps
    
    async def _execute_workflow(self, workflow_id: str):
        """执行工作流"""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return
        
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        try:
            # 构建依赖图
            step_results = {}
            pending_steps = {s.step_id: s for s in workflow.steps}
            completed_steps = set()
            
            while pending_steps:
                # 找出可以执行的步骤(依赖已满足)
                executable = [
                    s for s in pending_steps.values()
                    if all(dep in completed_steps for dep in s.depends_on)
                ]
                
                if not executable:
                    raise RuntimeError("工作流死锁:存在循环依赖或无法完成的步骤")
                
                # 并行执行可执行的步骤
                tasks = [self._execute_step(step, step_results) for step in executable]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for step, result in zip(executable, results):
                    if isinstance(result, Exception):
                        step.status = "failed"
                        step.error = str(result)
                        workflow.status = WorkflowStatus.FAILED
                        logger.error(f"工作流步骤失败 {step.step_id}: {result}")
                        return
                    else:
                        step.status = "completed"
                        step.result = result
                        completed_steps.add(step.step_id)
                        del pending_steps[step.step_id]
            
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.now()
            
            # generate跨模块洞察
            await self._generate_insights(workflow)
            
            logger.info(f"工作流完成: {workflow_id}")
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.now()
            logger.error(f"工作流执行失败 {workflow_id}: {e}")
    
    async def _execute_step(self, step: WorkflowStep, 
                           step_results: Dict[str, Any]) -> Any:
        """执行单个步骤"""
        step.status = "running"
        step.started_at = datetime.now()
        
        module = self.coordinator.get_module(step.module)
        if not module:
            raise RuntimeError(f"模块未就绪: {step.module.value}")
        
        # 调用模块方法
        method = getattr(module, step.action, None)
        if not method:
            raise RuntimeError(f"模块 {step.module.value} 没有方法 {step.action}")
        
        if asyncio.iscoroutinefunction(method):
            result = await method(**step.params)
        else:
            result = method(**step.params)
        
        step.completed_at = datetime.now()
        return result
    
    async def _generate_insights(self, workflow: Workflow):
        """generate跨模块洞察"""
        # 收集所有步骤的结果
        all_results = {s.step_id: s.result for s in workflow.steps if s.result}
        
        # 基于工作流类型generate洞察
        if workflow.workflow_type == WorkflowType.FULL_CYCLE_OPTIMIZATION:
            insight = CrossModuleInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                insight_type="full_cycle_optimization",
                source_modules=[ModuleType.EVOLUTION_ENGINE, ModuleType.KNOWLEDGE_GRAPH, ModuleType.GROWTH_STRATEGIES],
                description="全周期优化分析完成",
                confidence=0.85,
                recommendations=[
                    {"type": "optimization", "description": "基于系统健康度和知识图谱的synthesize优化建议"}
                ]
            )
            self._insights.append(insight)
    
    # 工作流处理器实现
    async def _handle_evolution_knowledge_sync(self, context: Dict) -> Dict:
        """处理进化-知识同步"""
        return {"status": "completed", "synced_items": context.get("evolution_result", {})}
    
    async def _handle_knowledge_growth_recommend(self, context: Dict) -> Dict:
        """处理知识-增长推荐"""
        return {"status": "completed", "recommendations_generated": True}
    
    async def _handle_full_cycle_optimization(self, context: Dict) -> Dict:
        """处理全周期优化"""
        return {"status": "completed", "optimization_applied": True}
    
    async def _handle_anomaly_response(self, context: Dict) -> Dict:
        """处理异常响应"""
        return {"status": "completed", "response_strategy_created": True}
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Workflow]:
        """get工作流状态"""
        return self._workflows.get(workflow_id)
    
    def get_all_workflows(self) -> List[Workflow]:
        """get所有工作流"""
        return list(self._workflows.values())
    
    def get_insights(self, limit: int = 10) -> List[CrossModuleInsight]:
        """get跨模块洞察"""
        return sorted(
            self._insights,
            key=lambda x: x.generated_at,
            reverse=True
        )[:limit]
    
    def get_system_status(self) -> Dict[str, Any]:
        """get系统整体状态"""
        return {
            "orchestrator_running": self._running,
            "module_health": self.coordinator.get_system_health(),
            "active_workflows": sum(1 for w in self._workflows.values() if w.status == WorkflowStatus.RUNNING),
            "completed_workflows": sum(1 for w in self._workflows.values() if w.status == WorkflowStatus.COMPLETED),
            "failed_workflows": sum(1 for w in self._workflows.values() if w.status == WorkflowStatus.FAILED),
            "recent_insights": len(self._insights),
            "event_bus_stats": self.event_bus.get_handler_stats()
        }

# 全局编排器实例
orchestrator = UnifiedOrchestrator()
