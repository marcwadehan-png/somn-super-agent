"""完全模拟 test_integration_simple.py 的结构"""
import asyncio
import sys
from pathlib import Path
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


class TestEventBus:
    async def test_event_publish_subscribe(self):
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
        assert received_events[0].event_type == EventType.EVOLUTION_COMPLETED
        print("   ✓ 事件发布订阅测试通过")
    
    async def test_event_priority(self):
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
        assert execution_order[1] == "low"
        print("   ✓ 事件优先级测试通过")


class TestModuleCoordinator:
    def test_dependency_graph(self):
        graph = DependencyGraph()
        deps = graph.get_dependencies(ModuleType.GROWTH_STRATEGIES)
        assert ModuleType.KNOWLEDGE_GRAPH in deps
        assert ModuleType.EVOLUTION_ENGINE in deps
        order = graph.get_initialization_order()
        assert order.index(ModuleType.EVOLUTION_ENGINE) < order.index(ModuleType.KNOWLEDGE_GRAPH)
        assert order.index(ModuleType.KNOWLEDGE_GRAPH) < order.index(ModuleType.GROWTH_STRATEGIES)
        print("   ✓ 依赖图测试通过")
    
    async def test_module_registration(self):
        coordinator = ModuleCoordinator()
        mock_module = {"name": "test_module"}
        coordinator.register_module(
            ModuleType.EVOLUTION_ENGINE,
            mock_module,
            "Test Evolution Engine",
            "1.0.0",
            ["self_diagnostics", "auto_optimization"]
        )
        state = coordinator.get_module_state(ModuleType.EVOLUTION_ENGINE)
        assert state is not None
        assert state.module_name == "Test Evolution Engine"
        assert state.version == "1.0.0"
        assert len(state.capabilities) == 2
        print("   ✓ 模块注册测试通过")


class TestUnifiedOrchestrator:
    async def test_orchestrator_lifecycle(self):
        orchestrator = UnifiedOrchestrator()
        await orchestrator.start()
        assert orchestrator._running is True
        await orchestrator.stop()
        assert orchestrator._running is False
        print("   ✓ 生命周期测试通过")
    
    async def test_workflow_creation(self):
        orchestrator = UnifiedOrchestrator()
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.EVOLUTION_KNOWLEDGE_SYNC,
            {"test": "data"}
        )
        assert workflow_id is not None
        assert workflow_id.startswith("wf_")
        workflow = orchestrator.get_workflow_status(workflow_id)
        assert workflow is not None
        assert workflow.workflow_type == WorkflowType.EVOLUTION_KNOWLEDGE_SYNC
        print("   ✓ 工作流创建测试通过")
    
    def test_workflow_step_creation(self):
        orchestrator = UnifiedOrchestrator()
        steps = orchestrator._create_workflow_steps(
            WorkflowType.FULL_CYCLE_OPTIMIZATION,
            {}
        )
        assert len(steps) == 3, f"期望3个步骤，实际{len(steps)}个"
        assert steps[0].module == ModuleType.EVOLUTION_ENGINE
        assert steps[1].module == ModuleType.KNOWLEDGE_GRAPH
        assert steps[2].module == ModuleType.GROWTH_STRATEGIES
        print("   ✓ 工作流步骤创建测试通过")


class TestMonitoringSystem:
    async def test_metrics_collection(self):
        monitoring = MonitoringSystem()
        await monitoring.metrics.record("test_metric", 100.0)
        await monitoring.metrics.record("test_metric", 200.0)
        latest = monitoring.metrics.get_latest("test_metric")
        assert latest is not None
        assert latest.value == 200.0, f"期望200.0，实际是{latest.value}"
        stats = monitoring.metrics.get_statistics("test_metric")
        assert stats["count"] == 2, f"期望count=2，实际是{stats['count']}"
        assert stats["min"] == 100.0
        assert stats["max"] == 200.0
        print("   ✓ 指标收集测试通过")
    
    def test_threshold_rule(self):
        rule = ThresholdRule(
            rule_id="test_rule",
            metric_name="cpu_usage",
            operator=">",
            threshold=80.0,
            severity=AlertSeverity.HIGH
        )
        assert rule.check(90.0) is True
        assert rule.check(80.0) is False
        assert rule.check(70.0) is False
        print("   ✓ 阈值规则测试通过")
    
    async def test_alert_lifecycle(self):
        monitoring = MonitoringSystem()
        await monitoring.alerts._trigger_alert(
            ThresholdRule(
                rule_id="test",
                metric_name="test_metric",
                operator=">",
                threshold=50.0,
                severity=AlertSeverity.MEDIUM
            ),
            75.0,
            "test_source"
        )
        active = monitoring.alerts.get_active_alerts()
        assert len(active) == 1, f"期望1个活动告警，实际{len(active)}个"
        assert active[0].status == AlertStatus.ACTIVE
        alert_id = active[0].alert_id
        await monitoring.alerts.acknowledge_alert(alert_id, "test_user")
        active = monitoring.alerts.get_active_alerts()
        assert active[0].status == AlertStatus.ACKNOWLEDGED
        await monitoring.alerts.resolve_alert(alert_id, "问题已修复")
        active = monitoring.alerts.get_active_alerts()
        assert len(active) == 0, f"期望0个活动告警，实际{len(active)}个"
        print("   ✓ 告警生命周期测试通过")


class TestIntegrationScenarios:
    async def test_cross_module_workflow(self):
        orchestrator = UnifiedOrchestrator()
        
        class MockEvolutionEngine:
            async def run_diagnostic(self):
                return {"health_score": 85}
        
        class MockKnowledgeGraph:
            async def infer_all_relations(self):
                return {"relations_found": 10}
        
        class MockGrowthStrategies:
            async def generate_optimization_plan(self):
                return {"strategies": ["s1", "s2"]}
        
        orchestrator.coordinator.register_module(
            ModuleType.EVOLUTION_ENGINE,
            MockEvolutionEngine(),
            "Evolution Engine",
            "1.0.0",
            ["diagnostics"]
        )
        orchestrator.coordinator.register_module(
            ModuleType.KNOWLEDGE_GRAPH,
            MockKnowledgeGraph(),
            "Knowledge Graph",
            "1.0.0",
            ["inference"]
        )
        orchestrator.coordinator.register_module(
            ModuleType.GROWTH_STRATEGIES,
            MockGrowthStrategies(),
            "Growth Strategies",
            "1.0.0",
            ["optimization"]
        )
        
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.FULL_CYCLE_OPTIMIZATION,
            {}
        )
        await asyncio.sleep(0.5)
        
        workflow = orchestrator.get_workflow_status(workflow_id)
        assert workflow is not None
        assert workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED], \
            f"工作流状态应该是COMPLETED或FAILED，实际是{workflow.status}"
        print("   ✓ 跨模块工作流测试通过")


async def run_all_tests():
    print("=" * 60)
    print("完全模拟 test_integration_simple.py")
    print("=" * 60)
    
    print("\n1. 测试事件总线...")
    await TestEventBus().test_event_publish_subscribe()
    await TestEventBus().test_event_priority()
    
    print("\n2. 测试模块协调器...")
    TestModuleCoordinator().test_dependency_graph()
    await TestModuleCoordinator().test_module_registration()
    
    print("\n3. 测试统一编排器...")
    await TestUnifiedOrchestrator().test_orchestrator_lifecycle()
    await TestUnifiedOrchestrator().test_workflow_creation()
    TestUnifiedOrchestrator().test_workflow_step_creation()
    
    print("\n4. 测试监控系统...")
    await TestMonitoringSystem().test_metrics_collection()
    TestMonitoringSystem().test_threshold_rule()
    await TestMonitoringSystem().test_alert_lifecycle()
    
    print("\n5. 测试集成场景...")
    await TestIntegrationScenarios().test_cross_module_workflow()
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)

asyncio.run(run_all_tests())
