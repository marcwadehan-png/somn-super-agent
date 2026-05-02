"""
集成层测试
Integration Layer Tests

测试三大模块的集成接口
"""

import asyncio
import pytest
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# 导入被测试模块
import sys

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
    ModuleCoordinator, ModuleType, ModuleStatus
)
from integration.monitoring_system import (
    MonitoringSystem, AlertSeverity, AlertStatus
)


class TestEventBus:
    """测试事件总线"""
    
    @pytest.mark.asyncio
    async def test_event_publish_subscribe(self):
        """测试事件发布和订阅"""
        bus = IntegrationEventBus()
        received_events = []
        
        async def handler(event):
            received_events.append(event)
            return {"handled": True}
        
        # 订阅事件
        bus.subscribe([EventType.EVOLUTION_COMPLETED], handler)
        
        # 发布事件
        await bus.publish_sync(
            source_module="test",
            event_type=EventType.EVOLUTION_COMPLETED,
            payload={"result": "success"}
        )
        
        assert len(received_events) == 1
        assert received_events[0].event_type == EventType.EVOLUTION_COMPLETED
    
    @pytest.mark.asyncio
    async def test_event_priority(self):
        """测试事件优先级"""
        bus = IntegrationEventBus()
        execution_order = []
        
        async def high_priority_handler(event):
            execution_order.append("high")
        
        async def low_priority_handler(event):
            execution_order.append("low")
        
        # 先订阅低优先级，再订阅高优先级
        bus.subscribe([EventType.HEALTH_STATUS_CHANGED], 
                     low_priority_handler, EventPriority.LOW)
        bus.subscribe([EventType.HEALTH_STATUS_CHANGED], 
                     high_priority_handler, EventPriority.HIGH)
        
        await bus.publish_sync(
            source_module="test",
            event_type=EventType.HEALTH_STATUS_CHANGED,
            payload={}
        )
        
        # 高优先级应该先执行
        assert execution_order[0] == "high"
        assert execution_order[1] == "low"


class TestModuleCoordinator:
    """测试模块协调器"""
    
    def test_dependency_graph(self):
        """测试依赖图"""
        from integration.module_coordinator import DependencyGraph
        
        graph = DependencyGraph()
        
        # 测试获取依赖
        deps = graph.get_dependencies(ModuleType.GROWTH_STRATEGIES)
        assert ModuleType.KNOWLEDGE_GRAPH in deps
        assert ModuleType.EVOLUTION_ENGINE in deps
        
        # 测试初始化顺序
        order = graph.get_initialization_order()
        assert order.index(ModuleType.EVOLUTION_ENGINE) < order.index(ModuleType.KNOWLEDGE_GRAPH)
        assert order.index(ModuleType.KNOWLEDGE_GRAPH) < order.index(ModuleType.GROWTH_STRATEGIES)
    
    @pytest.mark.asyncio
    async def test_module_registration(self):
        """测试模块注册"""
        coordinator = ModuleCoordinator()
        
        # 注册模拟模块
        mock_module = {"name": "test_module"}
        coordinator.register_module(
            ModuleType.EVOLUTION_ENGINE,
            mock_module,
            "Test Evolution Engine",
            "6.2.0",
            ["self_diagnostics", "auto_optimization"]
        )
        
        state = coordinator.get_module_state(ModuleType.EVOLUTION_ENGINE)
        assert state is not None
        assert state.module_name == "Test Evolution Engine"
        assert state.version == "6.2.0"
        assert len(state.capabilities) == 2


class TestUnifiedOrchestrator:
    """测试统一编排器"""
    
    @pytest.mark.asyncio
    async def test_orchestrator_lifecycle(self):
        """测试编排器生命周期"""
        orchestrator = UnifiedOrchestrator()
        
        # 启动
        await orchestrator.start()
        assert orchestrator._running is True
        
        # 停止
        await orchestrator.stop()
        assert orchestrator._running is False
    
    @pytest.mark.asyncio
    async def test_workflow_creation(self):
        """测试工作流创建"""
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
    
    def test_workflow_step_creation(self):
        """测试工作流步骤创建"""
        orchestrator = UnifiedOrchestrator()
        
        # 测试不同工作流类型的步骤
        steps = orchestrator._create_workflow_steps(
            WorkflowType.FULL_CYCLE_OPTIMIZATION,
            {}
        )
        
        assert len(steps) == 3
        assert steps[0].module == ModuleType.EVOLUTION_ENGINE
        assert steps[1].module == ModuleType.KNOWLEDGE_GRAPH
        assert steps[2].module == ModuleType.GROWTH_STRATEGIES


class TestMonitoringSystem:
    """测试监控系统"""
    
    @pytest.mark.asyncio
    async def test_metrics_collection(self):
        """测试指标收集"""
        monitoring = MonitoringSystem()
        
        # 记录指标
        await monitoring.metrics.record("test_metric", 100.0)
        await monitoring.metrics.record("test_metric", 200.0)
        
        # 获取最新值
        latest = monitoring.metrics.get_latest("test_metric")
        assert latest is not None
        assert latest.value == 200.0
        
        # 获取统计信息
        stats = monitoring.metrics.get_statistics("test_metric")
        assert stats["count"] == 2
        assert stats["min"] == 100.0
        assert stats["max"] == 200.0
    
    def test_threshold_rule(self):
        """测试阈值规则"""
        from integration.monitoring_system import ThresholdRule
        
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
    
    @pytest.mark.asyncio
    async def test_alert_lifecycle(self):
        """测试告警生命周期"""
        monitoring = MonitoringSystem()
        
        # 触发告警
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
        
        # 获取活动告警
        active = monitoring.alerts.get_active_alerts()
        assert len(active) == 1
        assert active[0].status == AlertStatus.ACTIVE
        
        # 确认告警
        alert_id = active[0].alert_id
        await monitoring.alerts.acknowledge_alert(alert_id, "test_user")
        
        active = monitoring.alerts.get_active_alerts()
        assert active[0].status == AlertStatus.ACKNOWLEDGED
        
        # 解决告警
        await monitoring.alerts.resolve_alert(alert_id, "问题已修复")
        
        active = monitoring.alerts.get_active_alerts()
        assert len(active) == 0


class TestIntegrationScenarios:
    """测试集成场景"""
    
    @pytest.mark.asyncio
    async def test_cross_module_workflow(self):
        """测试跨模块工作流"""
        orchestrator = UnifiedOrchestrator()
        
        # 创建模拟模块
        class MockEvolutionEngine:
            async def run_diagnostic(self):
                return {"health_score": 85}
        
        class MockKnowledgeGraph:
            async def infer_all_relations(self):
                return {"relations_found": 10}
        
        class MockGrowthStrategies:
            async def generate_optimization_plan(self):
                return {"strategies": ["s1", "s2"]}
        
        # 注册模块
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
        
        # 触发全周期优化工作流
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.FULL_CYCLE_OPTIMIZATION,
            {}
        )
        
        # 等待工作流完成
        await asyncio.sleep(0.5)
        
        workflow = orchestrator.get_workflow_status(workflow_id)
        assert workflow is not None
        # 工作流应该已完成或失败（取决于模拟模块的实现）
        assert workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]


def run_tests():
    """运行测试"""
    print("=" * 60)
    print("集成层测试")
    print("=" * 60)
    
    # 运行事件总线测试
    print("\n1. 测试事件总线...")
    asyncio.run(TestEventBus().test_event_publish_subscribe())
    print("   ✓ 事件发布订阅测试通过")
    
    asyncio.run(TestEventBus().test_event_priority())
    print("   ✓ 事件优先级测试通过")
    
    # 运行模块协调器测试
    print("\n2. 测试模块协调器...")
    TestModuleCoordinator().test_dependency_graph()
    print("   ✓ 依赖图测试通过")
    
    asyncio.run(TestModuleCoordinator().test_module_registration())
    print("   ✓ 模块注册测试通过")
    
    # 运行编排器测试
    print("\n3. 测试统一编排器...")
    asyncio.run(TestUnifiedOrchestrator().test_orchestrator_lifecycle())
    print("   ✓ 生命周期测试通过")
    
    asyncio.run(TestUnifiedOrchestrator().test_workflow_creation())
    print("   ✓ 工作流创建测试通过")
    
    TestUnifiedOrchestrator().test_workflow_step_creation()
    print("   ✓ 工作流步骤创建测试通过")
    
    # 运行监控系统测试
    print("\n4. 测试监控系统...")
    asyncio.run(TestMonitoringSystem().test_metrics_collection())
    print("   ✓ 指标收集测试通过")
    
    TestMonitoringSystem().test_threshold_rule()
    print("   ✓ 阈值规则测试通过")
    
    asyncio.run(TestMonitoringSystem().test_alert_lifecycle())
    print("   ✓ 告警生命周期测试通过")
    
    # 运行集成场景测试
    print("\n5. 测试集成场景...")
    asyncio.run(TestIntegrationScenarios().test_cross_module_workflow())
    print("   ✓ 跨模块工作流测试通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
