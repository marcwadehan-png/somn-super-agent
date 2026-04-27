"""写入文件进行调试"""
import asyncio
import sys
import os
from pathlib import Path

# 获取测试文件所在目录
TEST_DIR = Path(__file__).resolve().parent
DEBUG_FILE = TEST_DIR / "debug_log.txt"

def log(msg):
    with open(DEBUG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")
    print(f"[LOG] {msg}", flush=True)

log(">>> 开始")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)
log(">>> 导入完成")

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

log(">>> 所有导入完成")

class TestUnifiedOrchestrator:
    async def test_workflow_creation(self):
        log(">>> test_workflow_creation 开始")
        orchestrator = UnifiedOrchestrator()
        log(f">>> orchestrator id: {id(orchestrator)}")
        log(f">>> orchestrator.coordinator id: {id(orchestrator.coordinator)}")
        workflow_id = await orchestrator.trigger_workflow(
            WorkflowType.EVOLUTION_KNOWLEDGE_SYNC,
            {"test": "data"}
        )
        log(f">>> 工作流ID: {workflow_id}")
        workflow = orchestrator.get_workflow_status(workflow_id)
        log(f">>> workflow.status: {workflow.status}")
        log(">>> test_workflow_creation 结束")

async def run():
    log(">>> run 开始")
    await TestUnifiedOrchestrator().test_workflow_creation()
    log(">>> run 结束")

log(">>> asyncio.run(run) 之前")
asyncio.run(run())
log(">>> asyncio.run(run) 之后")
