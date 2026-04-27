"""添加 print 追踪"""
import asyncio
import sys
from pathlib import Path
sys.stdout.reconfigure(line_buffering=True)  # 强制立即输出

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)

from integration.unified_orchestrator import (
    UnifiedOrchestrator, WorkflowType, WorkflowStatus
)
from integration.integration_events import (
    IntegrationEventBus, EventType, EventPriority, IntegrationEvent
)
from integration.module_coordinator import (
    ModuleCoordinator, ModuleType, ModuleStatus, DependencyGraph
)
from integration.monitoring_system import (
    MonitoringSystem, AlertSeverity, AlertStatus, ThresholdRule
)

print(">>> 开始运行测试...", flush=True)

class TestEventBus:
    async def test_event_publish_subscribe(self):
        print(">>> TestEventBus.test_event_publish_subscribe 开始", flush=True)
        bus = IntegrationEventBus()
        received_events = []
        
        async def handler(event):
            received_events.append(event)
            return {"handled": True}
        
        bus.subscribe([EventType.EVOLUTION_COMPLETED], handler)
        await bus.publish_sync(
            source_module="test",
            event_type=EventType.EVOLUTION_COMPLETED,
            payload={"result": "success"}
        )
        assert len(received_events) == 1
        print(">>> TestEventBus.test_event_publish_subscribe 结束", flush=True)
    
    async def test_event_priority(self):
        print(">>> TestEventBus.test_event_priority 开始", flush=True)
        bus = IntegrationEventBus()
        execution_order = []
        
        async def high_priority_handler(event):
            execution_order.append("high")
        
        async def low_priority_handler(event):
            execution_order.append("low")
        
        bus.subscribe([EventType.HEALTH_STATUS_CHANGED], 
                     low_priority_handler, EventPriority.LOW)
        bus.subscribe([EventType.HEALTH_STATUS_CHANGED], 
                     high_priority_handler, EventPriority.HIGH)
        
        await bus.publish_sync(
            source_module="test",
            event_type=EventType.HEALTH_STATUS_CHANGED,
            payload={}
        )
        assert execution_order[0] == "high"
        print(">>> TestEventBus.test_event_priority 结束", flush=True)

print(">>> TestEventBus 类定义完成", flush=True)

class TestModuleCoordinator:
    def test_dependency_graph(self):
        print(">>> TestModuleCoordinator.test_dependency_graph 开始", flush=True)
        graph = DependencyGraph()
        deps = graph.get_dependencies(ModuleType.GROWTH_STRATEGIES)
        assert ModuleType.KNOWLEDGE_GRAPH in deps
        print(">>> TestModuleCoordinator.test_dependency_graph 结束", flush=True)
    
    async def test_module_registration(self):
        print(">>> TestModuleCoordinator.test_module_registration 开始", flush=True)
        coordinator = ModuleCoordinator()
        mock_module = {"name": "test_module"}
        coordinator.register_module(
            ModuleType.EVOLUTION_ENGINE,
            mock_module,
            "Test Evolution Engine",
            "1.0.0",
            ["self_diagnostics", "auto_optimization"]
        )
        print(">>> TestModuleCoordinator.test_module_registration 结束", flush=True)

print(">>> TestModuleCoordinator 类定义完成", flush=True)

class TestUnifiedOrchestrator:
    async def test_orchestrator_lifecycle(self):
        print(">>> TestUnifiedOrchestrator.test_orchestrator_lifecycle 开始", flush=True)
        orchestrator = UnifiedOrchestrator()
        await orchestrator.start()
        assert orchestrator._running is True
        await orchestrator.stop()
        assert orchestrator._running is False
        print(">>> TestUnifiedOrchestrator.test_orchestrator_lifecycle 结束", flush=True)
    
    async def test_workflow_creation(self):
        print(">>> TestUnifiedOrchestrator.test_workflow_creation 开始", flush=True)
        orchestrator = UnifiedOrchestrator()
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.EVOLUTION_KNOWLEDGE_SYNC,
            {"test": "data"}
        )
        print(f">>> 工作流ID: {workflow_id}", flush=True)
        workflow = orchestrator.get_workflow_status(workflow_id)
        assert workflow is not None
        print(">>> TestUnifiedOrchestrator.test_workflow_creation 结束", flush=True)
    
    def test_workflow_step_creation(self):
        print(">>> TestUnifiedOrchestrator.test_workflow_step_creation 开始", flush=True)
        orchestrator = UnifiedOrchestrator()
        steps = orchestrator._create_workflow_steps(
            WorkflowType.FULL_CYCLE_OPTIMIZATION,
            {}
        )
        print(f">>> 步骤数量: {len(steps)}", flush=True)
        print(">>> TestUnifiedOrchestrator.test_workflow_step_creation 结束", flush=True)

print(">>> TestUnifiedOrchestrator 类定义完成", flush=True)

class TestMonitoringSystem:
    async def test_metrics_collection(self):
        print(">>> TestMonitoringSystem.test_metrics_collection 开始", flush=True)
        monitoring = MonitoringSystem()
        await monitoring.metrics.record("test_metric", 100.0)
        await monitoring.metrics.record("test_metric", 200.0)
        latest = monitoring.metrics.get_latest("test_metric")
        assert latest.value == 200.0
        print(">>> TestMonitoringSystem.test_metrics_collection 结束", flush=True)
    
    def test_threshold_rule(self):
        print(">>> TestMonitoringSystem.test_threshold_rule 开始", flush=True)
        rule = ThresholdRule(rule_id="test", metric_name="cpu", operator=">", threshold=80.0)
        assert rule.check(90.0) is True
        print(">>> TestMonitoringSystem.test_threshold_rule 结束", flush=True)
    
    async def test_alert_lifecycle(self):
        print(">>> TestMonitoringSystem.test_alert_lifecycle 开始", flush=True)
        monitoring = MonitoringSystem()
        await monitoring.alerts._trigger_alert(
            ThresholdRule(rule_id="test", metric_name="test", operator=">", threshold=50.0),
            75.0, "test"
        )
        active = monitoring.alerts.get_active_alerts()
        assert len(active) == 1
        print(">>> TestMonitoringSystem.test_alert_lifecycle 结束", flush=True)

print(">>> TestMonitoringSystem 类定义完成", flush=True)

class TestIntegrationScenarios:
    async def test_cross_module_workflow(self):
        print(">>> TestIntegrationScenarios.test_cross_module_workflow 开始", flush=True)
        orchestrator = UnifiedOrchestrator()
        
        class MockEvolutionEngine:
            async def run_diagnostic(self):
                return {"health_score": 85}
        
        orchestrator.coordinator.register_module(
            ModuleType.EVOLUTION_ENGINE,
            MockEvolutionEngine(),
            "Evolution Engine", "1.0.0", ["diagnostics"]
        )
        
        print(f">>> 已注册模块: {list(orchestrator.coordinator._modules.keys())}", flush=True)
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.FULL_CYCLE_OPTIMIZATION, {}
        )
        print(f">>> 工作流ID: {workflow_id}", flush=True)
        await asyncio.sleep(0.5)
        workflow = orchestrator.get_workflow_status(workflow_id)
        print(f">>> 工作流状态: {workflow.status}", flush=True)
        print(">>> TestIntegrationScenarios.test_cross_module_workflow 结束", flush=True)

print(">>> TestIntegrationScenarios 类定义完成", flush=True)

async def run_all_tests():
    print(">>> run_all_tests 开始", flush=True)
    
    print("\n1. 测试事件总线...", flush=True)
    await TestEventBus().test_event_publish_subscribe()
    await TestEventBus().test_event_priority()
    
    print("\n2. 测试模块协调器...", flush=True)
    TestModuleCoordinator().test_dependency_graph()
    await TestModuleCoordinator().test_module_registration()
    
    print("\n3. 测试统一编排器...", flush=True)
    await TestUnifiedOrchestrator().test_orchestrator_lifecycle()
    await TestUnifiedOrchestrator().test_workflow_creation()
    TestUnifiedOrchestrator().test_workflow_step_creation()
    
    print("\n4. 测试监控系统...", flush=True)
    await TestMonitoringSystem().test_metrics_collection()
    TestMonitoringSystem().test_threshold_rule()
    await TestMonitoringSystem().test_alert_lifecycle()
    
    print("\n5. 测试集成场景...", flush=True)
    await TestIntegrationScenarios().test_cross_module_workflow()
    
    print(">>> run_all_tests 结束", flush=True)

print(">>> 准备运行 asyncio.run(run_all_tests())...", flush=True)
asyncio.run(run_all_tests())
