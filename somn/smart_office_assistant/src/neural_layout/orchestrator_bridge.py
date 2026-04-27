"""
__all__ = [
    'get_bridge_status',
    'get_orchestrator_bridge',
    'initialize',
    'process_signal',
]

主线集成器 ↔ UnifiedOrchestrator 桥梁模块

打通神经网络布局与统一编排器的深度集成
"""

from typing import Dict, List, Any, Optional, Callable
import logging
from datetime import datetime
import asyncio
import uuid

logger = logging.getLogger(__name__)

from .global_neural_bridge import get_global_neural_bridge
from .signal import Signal, SignalType, SignalPriority

class OrchestratorBridge:
    """
    编排器桥梁
    
    连接神经网络布局与UnifiedOrchestrator，实现：
    1. 神经网络信号 → 编排器工作流触发
    2. 编排器事件 → 神经网络状态更新
    3. 双向数据流同步
    """
    
    def __init__(self):
        self.neural_bridge = get_global_neural_bridge()
        self._orchestrator = None  # 延迟加载避免循环导入
        self._initialized = False
        self._signal_handlers: Dict[str, Callable] = {}
    
    def initialize(self) -> bool:
        """初始化桥梁"""
        if self._initialized:
            return True
        
        # 延迟导入避免循环依赖
        try:
            from src.integration.unified_orchestrator import (
                UnifiedOrchestrator, WorkflowType, EventType, EventPriority
            )
            self._orchestrator = UnifiedOrchestrator()
            self._setup_signal_mapping()
            self._initialized = True
            return True
        except ImportError as e:
            logger.warning(f"编排器桥梁初始化失败: {e}")
            return False
    
    def _setup_signal_mapping(self):
        """设置信号映射"""
        self._signal_handlers = {
            "neuron_agent_core": self._handle_agent_core_signal,
            "neuron_somn_core": self._handle_somn_core_signal,
            "neuron_wisdom_dispatcher": self._handle_wisdom_signal,
            "neuron_autonomous_agent": self._handle_autonomy_signal,
            "neuron_learning_coord": self._handle_learning_signal,
        }
    
    def _handle_agent_core_signal(self, signal: Signal) -> Dict:
        """处理AgentCore信号 → 触发编排器工作流"""
        data = signal.data
        
        # 根据信号类型触发不同工作流
        if signal.signal_type == SignalType.CONTROL:
            # 异步触发工作流
            asyncio.create_task(
                self._trigger_orchestrator_workflow("agent_command", data)
            )
        
        return {
            "handled_by": "orchestrator_bridge",
            "signal_source": signal.source_id,
            "workflow_triggered": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_somn_core_signal(self, signal: Signal) -> Dict:
        """处理SomnCore信号"""
        data = signal.data
        
        # 检测是否需要跨模块协调
        if self._needs_coordination(data):
            asyncio.create_task(
                self._trigger_orchestrator_workflow("cross_module_coordination", data)
            )
        
        return {
            "handled_by": "orchestrator_bridge",
            "coordination_needed": self._needs_coordination(data),
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_wisdom_signal(self, signal: Signal) -> Dict:
        """处理智慧层信号 → 触发学派融合工作流"""
        data = signal.data
        
        # 智慧层输出 → 执行层优化
        if isinstance(data, dict) and "selected_schools" in data:
            asyncio.create_task(
                self._trigger_school_execution_workflow(data)
            )
        
        return {
            "handled_by": "orchestrator_bridge",
            "school_execution_triggered": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_autonomy_signal(self, signal: Signal) -> Dict:
        """处理自主层信号 → 与反馈层整合"""
        data = signal.data
        
        # 自主决策 → 反馈采集
        asyncio.create_task(
            self._trigger_feedback_collection(data)
        )
        
        return {
            "handled_by": "orchestrator_bridge",
            "feedback_collection_triggered": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_learning_signal(self, signal: Signal) -> Dict:
        """处理学习层信号"""
        data = signal.data
        
        # 学习更新 → 跨模块洞察生成
        if isinstance(data, dict) and data.get("insight_generated"):
            asyncio.create_task(
                self._trigger_insight_generation(data)
            )
        
        return {
            "handled_by": "orchestrator_bridge",
            "insight_generation_triggered": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _needs_coordination(self, data: Any) -> bool:
        """判断是否需要跨模块协调"""
        if not isinstance(data, dict):
            return False
        
        # 涉及多个模块的操作需要协调
        multi_module_indicators = [
            "evolution_result",
            "comparison_result",
            "experiment_result",
            "cross_module"
        ]
        
        return any(indicator in data for indicator in multi_module_indicators)
    
    async def _trigger_orchestrator_workflow(self, workflow_name: str, context: Dict):
        """触发编排器工作流"""
        if not self._orchestrator:
            return
        
        try:
            from src.integration.unified_orchestrator import WorkflowType
            
            # 映射工作流名称到类型
            workflow_type_map = {
                "agent_command": WorkflowType.FULL_CYCLE_OPTIMIZATION,
                "cross_module_coordination": WorkflowType.FULL_CYCLE_OPTIMIZATION,
                "evolution_knowledge_sync": WorkflowType.EVOLUTION_KNOWLEDGE_SYNC,
                "knowledge_growth_recommend": WorkflowType.KNOWLEDGE_GROWTH_RECOMMEND,
                "anomaly_response": WorkflowType.ANOMALY_RESPONSE,
            }
            
            workflow_type = workflow_type_map.get(workflow_name, WorkflowType.FULL_CYCLE_OPTIMIZATION)
            
            await self._orchestrator.trigger_workflow(workflow_type, context)
        except Exception as e:
            logger.warning(f"触发工作流失败: {e}")
    
    async def _trigger_school_execution_workflow(self, wisdom_data: Dict):
        """触发学派执行工作流"""
        # 智慧层输出 → 执行层优化
        context = {
            "wisdom_output": wisdom_data,
            "execution_optimization": True,
            "selected_schools": wisdom_data.get("selected_schools", []),
            "query": wisdom_data.get("query", "")
        }
        
        await self._trigger_orchestrator_workflow("cross_module_coordination", context)
    
    async def _trigger_feedback_collection(self, autonomy_data: Dict):
        """触发反馈采集"""
        # 自主层 → 反馈层深度整合
        context = {
            "autonomy_action": autonomy_data,
            "feedback_collection": True,
            "collection_points": ["execution_result", "adoption_signal"]
        }
        
        # 这里可以调用FeedbackLoopIntegrator
        try:
            from src.core.feedback_loop_integration import FeedbackLoopIntegrator
            integrator = FeedbackLoopIntegrator()
            integrator.collect_feedback("autonomy_action", context)
        except ImportError:
            pass
    
    async def _trigger_insight_generation(self, learning_data: Dict):
        """触发跨模块洞察生成"""
        context = {
            "learning_data": learning_data,
            "generate_insight": True,
            "source_modules": ["learning", "memory", "execution"]
        }
        
        await self._trigger_orchestrator_workflow("cross_module_coordination", context)
    
    def process_signal(self, signal: Signal) -> Signal:
        """处理神经网络信号"""
        if not self._initialized:
            self.initialize()
        
        handler = self._signal_handlers.get(signal.source_id)
        
        if handler:
            result = handler(signal)
            return signal.copy_with(
                source_id="orchestrator_bridge",
                data=result,
                metadata={**signal.metadata, "bridge_processed": True}
            )
        
        return signal
    
    def get_bridge_status(self) -> Dict:
        """获取桥梁状态"""
        return {
            "initialized": self._initialized,
            "orchestrator_connected": self._orchestrator is not None,
            "signal_handlers": list(self._signal_handlers.keys()),
            "timestamp": datetime.now().isoformat()
        }

# 全局桥梁实例
_orchestrator_bridge: Optional[OrchestratorBridge] = None

def get_orchestrator_bridge() -> OrchestratorBridge:
    """获取编排器桥梁实例"""
    global _orchestrator_bridge
    if _orchestrator_bridge is None:
        _orchestrator_bridge = OrchestratorBridge()
    return _orchestrator_bridge
