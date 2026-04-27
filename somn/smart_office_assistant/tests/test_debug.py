"""调试测试 - 只运行前几个测试"""
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

async def test_event_publish_subscribe():
    print("   [DEBUG] test_event_publish_subscribe 开始")
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
    
    assert len(received_events) == 1, f"期望1个事件，实际{len(received_events)}个"
    print("   ✓ 事件发布订阅测试通过")

async def test_event_priority():
    print("   [DEBUG] test_event_priority 开始")
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

def test_dependency_graph():
    print("   [DEBUG] test_dependency_graph 开始")
    graph = DependencyGraph()
    deps = graph.get_dependencies(ModuleType.GROWTH_STRATEGIES)
    assert ModuleType.KNOWLEDGE_GRAPH in deps
    assert ModuleType.EVOLUTION_ENGINE in deps
    order = graph.get_initialization_order()
    assert order.index(ModuleType.EVOLUTION_ENGINE) < order.index(ModuleType.KNOWLEDGE_GRAPH)
    print("   ✓ 依赖图测试通过")

async def test_module_registration():
    print("   [DEBUG] test_module_registration 开始")
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
    print("   ✓ 模块注册测试通过")

async def test_orchestrator_lifecycle():
    print("   [DEBUG] test_orchestrator_lifecycle 开始")
    orchestrator = UnifiedOrchestrator()
    await orchestrator.start()
    assert orchestrator._running is True
    await orchestrator.stop()
    assert orchestrator._running is False
    print("   ✓ 生命周期测试通过")

async def test_workflow_creation():
    print("   [DEBUG] test_workflow_creation 开始")
    orchestrator = UnifiedOrchestrator()
    print(f"   [DEBUG] orchestrator.coordinator._modules: {orchestrator.coordinator._modules}")
    
    workflow_id = await orchestrator.trigger_workflow(
        WorkflowType.EVOLUTION_KNOWLEDGE_SYNC,
        {"test": "data"}
    )
    print(f"   [DEBUG] 工作流ID: {workflow_id}")
    
    assert workflow_id is not None
    assert workflow_id.startswith("wf_")
    
    workflow = orchestrator.get_workflow_status(workflow_id)
    assert workflow is not None
    print("   ✓ 工作流创建测试通过")

async def test_metrics_collection():
    print("   [DEBUG] test_metrics_collection 开始")
    monitoring = MonitoringSystem()
    await monitoring.metrics.record("test_metric", 100.0)
    await monitoring.metrics.record("test_metric", 200.0)
    latest = monitoring.metrics.get_latest("test_metric")
    assert latest is not None
    assert latest.value == 200.0, f"期望200.0，实际是{latest.value}"
    print("   ✓ 指标收集测试通过")

def test_threshold_rule():
    print("   [DEBUG] test_threshold_rule 开始")
    rule = ThresholdRule(
        rule_id="test_rule",
        metric_name="cpu_usage",
        operator=">",
        threshold=80.0,
        severity=AlertSeverity.HIGH
    )
    assert rule.check(90.0) is True
    print("   ✓ 阈值规则测试通过")

async def test_alert_lifecycle():
    print("   [DEBUG] test_alert_lifecycle 开始")
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
    print(f"   [DEBUG] 活动告警数: {len(active)}")
    assert len(active) == 1
    assert active[0].status == AlertStatus.ACTIVE
    print("   ✓ 告警生命周期测试通过")

async def run_all_tests():
    print("=" * 60)
    print("调试测试")
    print("=" * 60)
    
    try:
        print("\n1. 测试事件总线...")
        await test_event_publish_subscribe()
        await test_event_priority()
    except Exception as e:
        print(f"[ERROR] 事件总线测试失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n2. 测试模块协调器...")
        test_dependency_graph()
        await test_module_registration()
    except Exception as e:
        print(f"[ERROR] 模块协调器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n3. 测试统一编排器...")
        await test_orchestrator_lifecycle()
        await test_workflow_creation()
    except Exception as e:
        print(f"[ERROR] 编排器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n4. 测试监控系统...")
        await test_metrics_collection()
        test_threshold_rule()
        await test_alert_lifecycle()
    except Exception as e:
        print(f"[ERROR] 监控系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)

asyncio.run(run_all_tests())
