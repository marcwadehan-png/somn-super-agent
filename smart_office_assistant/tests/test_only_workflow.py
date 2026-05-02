"""只运行 test_cross_module_workflow"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)

from integration.unified_orchestrator import (
    UnifiedOrchestrator, WorkflowType, WorkflowStatus
)
from integration.module_coordinator import ModuleType

async def test_cross_module_workflow():
    """测试跨模块工作流"""
    print("开始 test_cross_module_workflow...")
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
    
    print(f"已注册模块: {list(orchestrator.coordinator._modules.keys())}")
    print(f"EVOLUTION_ENGINE: {orchestrator.coordinator.get_module(ModuleType.EVOLUTION_ENGINE)}")
    
    # 触发全周期优化工作流
    print("触发工作流...")
    workflow_id = await orchestrator.trigger_workflow(
        WorkflowType.FULL_CYCLE_OPTIMIZATION,
        {}
    )
    print(f"Workflow ID: {workflow_id}")
    
    # 等待工作流完成
    await asyncio.sleep(0.5)
    
    workflow = orchestrator.get_workflow_status(workflow_id)
    print(f"Workflow status: {workflow.status}")
    if workflow.steps:
        for step in workflow.steps:
            print(f"  Step {step.step_id}: {step.status}, error={step.error}")
    
    assert workflow is not None, "工作流不应该为None"
    assert workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED], \
        f"工作流状态应该是COMPLETED或FAILED，实际是{workflow.status}"
    print("✓ 跨模块工作流测试通过")

async def main():
    print("=" * 60)
    print("只测试跨模块工作流")
    print("=" * 60)
    await test_cross_module_workflow()

asyncio.run(main())
