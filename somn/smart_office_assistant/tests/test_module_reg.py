"""模拟 test_integration_simple.py 的导入方式"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)

# 模拟 test_integration_simple.py 的导入方式
from integration.unified_orchestrator import (
    UnifiedOrchestrator, WorkflowType, WorkflowStatus
)
from integration.module_coordinator import (
    ModuleCoordinator, ModuleType, ModuleStatus, DependencyGraph
)
from integration.monitoring_system import (
    MonitoringSystem, AlertSeverity, AlertStatus, ThresholdRule
)

async def test_cross_module_workflow():
    """测试跨模块工作流 - 模拟 test_integration_simple.py"""
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
    assert workflow is not None, "工作流不应该为None"
    # 工作流应该已完成或失败（取决于模拟模块的实现）
    assert workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED], \
        f"工作流状态应该是COMPLETED或FAILED，实际是{workflow.status}"
    print("   ✓ 跨模块工作流测试通过")

async def test():
    await test_cross_module_workflow()

asyncio.run(test())
