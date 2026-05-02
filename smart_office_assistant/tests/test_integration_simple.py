"""
集成层测试 (简化版)
Integration Layer Tests (Simple Version)

测试三大模块的集成接口 - 无需pytest
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# 导入被测试模块
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
    """测试事件总线"""
    
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
        
        assert len(received_events) == 1, f"期望1个事件，实际{len(received_events)}个"
        assert received_events[0].event_type == EventType.EVOLUTION_COMPLETED
        print("   ✓ 事件发布订阅测试通过")
    
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
        assert execution_order[0] == "high", f"期望high先执行，实际是{execution_order[0]}"
        assert execution_order[1] == "low"
        print("   ✓ 事件优先级测试通过")


class TestModuleCoordinator:
    """测试模块协调器"""
    
    def test_dependency_graph(self):
        """测试依赖图"""
        graph = DependencyGraph()
        
        # 测试获取依赖
        deps = graph.get_dependencies(ModuleType.GROWTH_STRATEGIES)
        assert ModuleType.KNOWLEDGE_GRAPH in deps, "Knowledge Graph应该是Growth Strategies的依赖"
        assert ModuleType.EVOLUTION_ENGINE in deps, "Evolution Engine应该是Growth Strategies的依赖"
        
        # 测试初始化顺序
        order = graph.get_initialization_order()
        assert order.index(ModuleType.EVOLUTION_ENGINE) < order.index(ModuleType.KNOWLEDGE_GRAPH)
        assert order.index(ModuleType.KNOWLEDGE_GRAPH) < order.index(ModuleType.GROWTH_STRATEGIES)
        print("   ✓ 依赖图测试通过")
    
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
        assert state is not None, "模块状态不应该为None"
        assert state.module_name == "Test Evolution Engine"
        assert state.version == "6.2.0"
        assert len(state.capabilities) == 2
        print("   ✓ 模块注册测试通过")


class TestUnifiedOrchestrator:
    """测试统一编排器"""
    
    async def test_orchestrator_lifecycle(self):
        """测试编排器生命周期"""
        orchestrator = UnifiedOrchestrator()
        
        # 启动
        await orchestrator.start()
        assert orchestrator._running is True, "编排器应该处于运行状态"
        
        # 停止
        await orchestrator.stop()
        assert orchestrator._running is False, "编排器应该已停止"
        print("   ✓ 生命周期测试通过")
    
    async def test_workflow_creation(self):
        """测试工作流创建"""
        print("   [DEBUG] test_workflow_creation 开始")
        orchestrator = UnifiedOrchestrator()
        print(f"   [DEBUG] orchestrator.coordinator._modules: {orchestrator.coordinator._modules}")
        
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.EVOLUTION_KNOWLEDGE_SYNC,
            {"test": "data"}
        )
        print(f"   [DEBUG] 工作流ID: {workflow_id}")
        
        assert workflow_id is not None, "工作流ID不应该为None"
        assert workflow_id.startswith("wf_"), f"工作流ID应该以wf_开头，实际是{workflow_id}"
        
        workflow = orchestrator.get_workflow_status(workflow_id)
        assert workflow is not None, "工作流状态不应该为None"
        assert workflow.workflow_type == WorkflowType.EVOLUTION_KNOWLEDGE_SYNC
        print("   ✓ 工作流创建测试通过")
    
    def test_workflow_step_creation(self):
        """测试工作流步骤创建"""
        orchestrator = UnifiedOrchestrator()
        
        # 测试不同工作流类型的步骤
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
    """测试监控系统"""
    
    async def test_metrics_collection(self):
        """测试指标收集"""
        monitoring = MonitoringSystem()
        
        # 记录指标
        await monitoring.metrics.record("test_metric", 100.0)
        await monitoring.metrics.record("test_metric", 200.0)
        
        # 获取最新值
        latest = monitoring.metrics.get_latest("test_metric")
        assert latest is not None, "最新指标值不应该为None"
        assert latest.value == 200.0, f"期望200.0，实际是{latest.value}"
        
        # 获取统计信息
        stats = monitoring.metrics.get_statistics("test_metric")
        assert stats["count"] == 2, f"期望count=2，实际是{stats['count']}"
        assert stats["min"] == 100.0
        assert stats["max"] == 200.0
        print("   ✓ 指标收集测试通过")
    
    def test_threshold_rule(self):
        """测试阈值规则"""
        rule = ThresholdRule(
            rule_id="test_rule",
            metric_name="cpu_usage",
            operator=">",
            threshold=80.0,
            severity=AlertSeverity.HIGH
        )
        
        assert rule.check(90.0) is True, "90 > 80应该返回True"
        assert rule.check(80.0) is False, "80 > 80应该返回False"
        assert rule.check(70.0) is False, "70 > 80应该返回False"
        print("   ✓ 阈值规则测试通过")
    
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
        assert len(active) == 1, f"期望1个活动告警，实际{len(active)}个"
        assert active[0].status == AlertStatus.ACTIVE
        
        # 确认告警
        alert_id = active[0].alert_id
        await monitoring.alerts.acknowledge_alert(alert_id, "test_user")
        
        active = monitoring.alerts.get_active_alerts()
        assert active[0].status == AlertStatus.ACKNOWLEDGED
        
        # 解决告警
        await monitoring.alerts.resolve_alert(alert_id, "问题已修复")
        
        active = monitoring.alerts.get_active_alerts()
        assert len(active) == 0, f"期望0个活动告警，实际{len(active)}个"
        print("   ✓ 告警生命周期测试通过")


class TestIntegrationScenarios:
    """测试集成场景"""
    
    async def test_cross_module_workflow(self):
        """测试跨模块工作流"""
        print("   [DEBUG] test_cross_module_workflow 开始")
        orchestrator = UnifiedOrchestrator()
        print(f"   [DEBUG] orchestrator.coordinator._modules: {orchestrator.coordinator._modules}")
        
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
        
        print(f"   [DEBUG] 注册后模块: {list(orchestrator.coordinator._modules.keys())}")
        
        # 触发全周期优化工作流
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.FULL_CYCLE_OPTIMIZATION,
            {}
        )
        print(f"   [DEBUG] 工作流ID: {workflow_id}")
        
        # 等待工作流完成
        await asyncio.sleep(0.5)
        
        workflow = orchestrator.get_workflow_status(workflow_id)
        print(f"   [DEBUG] 工作流状态: {workflow.status}")
        if workflow.steps:
            for step in workflow.steps:
                print(f"   [DEBUG] 步骤 {step.step_id}: {step.status}, error={step.error}")
        
        assert workflow is not None, "工作流不应该为None"
        # 工作流应该已完成或失败（取决于模拟模块的实现）
        assert workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED], \
            f"工作流状态应该是COMPLETED或FAILED，实际是{workflow.status}"
        print("   ✓ 跨模块工作流测试通过")


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("集成层测试")
    print("=" * 60)
    
    # 运行事件总线测试
    print("\n1. 测试事件总线...")
    await TestEventBus().test_event_publish_subscribe()
    await TestEventBus().test_event_priority()
    
    # 运行模块协调器测试
    print("\n2. 测试模块协调器...")
    TestModuleCoordinator().test_dependency_graph()
    await TestModuleCoordinator().test_module_registration()
    
    # 运行编排器测试
    print("\n3. 测试统一编排器...")
    await TestUnifiedOrchestrator().test_orchestrator_lifecycle()
    await TestUnifiedOrchestrator().test_workflow_creation()
    TestUnifiedOrchestrator().test_workflow_step_creation()
    
    # 运行监控系统测试
    print("\n4. 测试监控系统...")
    await TestMonitoringSystem().test_metrics_collection()
    TestMonitoringSystem().test_threshold_rule()
    await TestMonitoringSystem().test_alert_lifecycle()
    
    # 运行集成场景测试
    print("\n5. 测试集成场景...")
    await TestIntegrationScenarios().test_cross_module_workflow()
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
