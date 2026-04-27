"""
神经网络布局模块

将Somn系统的所有功能模块映射到神经网络布局，实现全局主链路打通。

核心组件:
- Signal: 神经信号定义
- SynapseConnection: 突触连接定义
- NeuronNode: 神经元节点定义
- NeuralNetwork: 神经网络核心
- NetworkLayoutManager: 网络布局管理器
- GlobalNeuralBridge: 全局神经桥梁
- NetworkVisualizer: 网络可视化器
- NetworkVerifier: 网络验证器
- NeuralLayoutIntegration: 系统集成器

新增串联优化组件:
- OrchestratorBridge: 主线集成器 ↔ UnifiedOrchestrator 桥梁
- AutonomyFeedbackFusionEngine: 自主层 ↔ 反馈层融合
- SchoolExecutionOptimizer: 学派层 → 执行层优化
- CrossModuleInsightGenerator: 跨模块洞察生成

使用方法:
    from src.neural_layout import (
        get_neural_integration,
        process_with_neural_layout
    )
    
    # 处理输入
    result = process_with_neural_layout({"query": "如何制定策略"})
"""

from .signal import Signal, SignalType, SignalPriority, SignalBatch
from .synapse_connection import SynapseConnection, ConnectionType
from .neuron_node import (
    NeuronNode, NeuronType, NeuronState, NeuronProfile,
    InputNeuron, OutputNeuron, WisdomNeuron, MemoryNeuron
)
from .neural_network import NeuralNetwork
from .network_layout_manager import NetworkLayoutManager, PhaseSystemStatus
from .global_neural_bridge import GlobalNeuralBridge, get_global_neural_bridge
from .visualizer import NetworkVisualizer, visualize_network
from .verifier import NetworkVerifier, verify_network
from .integration import (
    NeuralLayoutIntegration,
    get_neural_integration,
    process_with_neural_layout,
    integrate_with_somn_core,
    integrate_with_agent_core
)

# 新增串联优化组件
from .orchestrator_bridge import (
    OrchestratorBridge,
    get_orchestrator_bridge
)
from .autonomy_feedback_fusion import (
    AutonomyFeedbackFusionEngine,
    get_autonomy_feedback_fusion_engine
)
from .school_execution_optimizer import (
    SchoolExecutionOptimizer,
    SchoolType, ExecutionStrategy, SchoolOutput, OptimizedExecutionPlan,
    get_school_execution_optimizer
)
from .cross_module_insight_generator import (
    CrossModuleInsightGenerator,
    CrossModuleInsight, InsightType, ModuleSource,
    get_cross_module_insight_generator
)
from .neural_layout_manager import NeuralLayoutManager, LayoutConfig, get_layout_manager
from .cluster_optimizer import ClusterOptimizer, ClusterConfig, OptimizationResult, get_cluster_optimizer
from .global_neural_bridge import get_bound_modules

__all__ = [
    # 信号
    'Signal', 'SignalType', 'SignalPriority', 'SignalBatch',
    # 连接
    'SynapseConnection', 'ConnectionType',
    # 神经元
    'NeuronNode', 'NeuronType', 'NeuronState', 'NeuronProfile',
    'InputNeuron', 'OutputNeuron', 'WisdomNeuron', 'MemoryNeuron',
    # 网络
    'NeuralNetwork',
    # 管理器
    'NetworkLayoutManager', 'NeuralLayoutManager', 'PhaseSystemStatus',
    # 集群优化
    'ClusterOptimizer', 'ClusterConfig', 'OptimizationResult', 'get_cluster_optimizer',
    # 桥梁
    'GlobalNeuralBridge', 'get_global_neural_bridge', 'get_bound_modules',
    # 可视化
    'NetworkVisualizer', 'visualize_network',
    # 验证
    'NetworkVerifier', 'verify_network',
    # 集成
    'NeuralLayoutIntegration', 'get_neural_integration',
    'process_with_neural_layout',
    'integrate_with_somn_core', 'integrate_with_agent_core',
    # 新增: 编排器桥梁
    'OrchestratorBridge', 'get_orchestrator_bridge',
    # 新增: 自主-反馈融合
    'AutonomyFeedbackFusionEngine', 'get_autonomy_feedback_fusion_engine',
    # 新增: 学派执行优化
    'SchoolExecutionOptimizer', 'SchoolType', 'ExecutionStrategy',
    'SchoolOutput', 'OptimizedExecutionPlan', 'get_school_execution_optimizer',
    # 新增: 跨模块洞察
    'CrossModuleInsightGenerator', 'CrossModuleInsight', 'InsightType', 'ModuleSource',
    'get_cross_module_insight_generator',
]

__version__ = "1.1.0"
