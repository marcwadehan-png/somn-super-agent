"""
神经网络布局管理器
负责将Somn系统的所有功能模块映射到神经网络布局

V2.0: 集成 Phase 1-5 引擎 + ClusterOptimizer + 实时反馈回路
"""

from typing import Any, Dict, List, Optional, Callable, Tuple
import logging
import threading
import asyncio
import time
from dataclasses import dataclass, field
import sys
from pathlib import Path

# 确保 timeout_utils 在 sys.path 中
_src_root = Path(__file__).resolve().parent.parent
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))
from timeout_utils import run_with_timeout, TimeoutException

__all__ = [
    'FunctionNeuron',
    'NetworkLayoutManager',
    'PhaseSystemStatus',
    'activate_main_chain',
    'find_optimal_path',
    'get_layout_status',
    'initialize_global_layout',
]

logger = logging.getLogger(__name__)

from .signal import Signal, SignalType, SignalPriority
from .synapse_connection import SynapseConnection, ConnectionType
from .neuron_node import (
    NeuronNode, NeuronType, NeuronState,
    InputNeuron, OutputNeuron, WisdomNeuron, MemoryNeuron
)
from .neural_network import NeuralNetwork


@dataclass
class PhaseSystemStatus:
    """Phase 系统状态"""
    phase3_running: bool = False
    phase3_executions: int = 0
    phase3_insights: int = 0
    phase4_classifications: int = 0
    phase4_active_subnetworks: int = 0
    phase5_last_score: float = 0.0
    cluster_count: int = 0
    cluster_optimization_history: int = 0

# 类型别名
NeuronID = str
SchoolID = str

# ============ 连接权重常量 ============
class ConnectionWeight:
    """连接权重常量定义"""
    LOWEST = 0.5
    LOW = 0.6
    MEDIUM = 0.7
    HIGH = 0.8
    HIGHER = 0.9
    MAX = 1.0


# ============ 连接链定义 (数据驱动) ============
# 格式: (源ID, 目标ID, 权重)
_CONNECTION_DEFINITIONS: List[Tuple[str, str, float]] = [
    # 输入层 -> 核心层
    ("input_user", "neuron_agent_core", ConnectionWeight.MAX),
    ("input_context", "neuron_somn_core", ConnectionWeight.HIGH),
    
    # 核心层 -> 协调层
    ("neuron_agent_core", "neuron_super_wisdom", ConnectionWeight.MAX),
    ("neuron_somn_core", "neuron_unified_intel", ConnectionWeight.MAX),
    
    # 协调层内部连接
    ("neuron_super_wisdom", "neuron_global_scheduler", ConnectionWeight.MAX),
    ("neuron_unified_intel", "neuron_global_scheduler", ConnectionWeight.HIGH),
    ("neuron_global_scheduler", "neuron_wisdom_dispatcher", ConnectionWeight.MAX),
    
    # 思维融合 -> 深度推理
    ("neuron_thinking_fusion", "neuron_deep_reasoning", ConnectionWeight.MAX),
    
    # 深度推理 -> 叙事智能
    ("neuron_deep_reasoning", "neuron_narrative_intel", ConnectionWeight.HIGHER),
    
    # 叙事智能 -> 学习协调
    ("neuron_narrative_intel", "neuron_learning_coord", ConnectionWeight.MEDIUM),
    
    # 学习协调 -> 自主智能体
    ("neuron_learning_coord", "neuron_autonomous_agent", ConnectionWeight.MEDIUM),
    
    # 记忆层连接
    ("neuron_neural_memory", "neuron_deep_reasoning", ConnectionWeight.MEDIUM),
    ("neuron_semantic_memory", "neuron_thinking_fusion", ConnectionWeight.LOW),
    
    # 强化连接
    ("neuron_autonomous_agent", "neuron_reinforcement", ConnectionWeight.MEDIUM),
    ("neuron_reinforcement", "neuron_learning_coord", ConnectionWeight.LOW),
    
    # ROI追踪
    ("neuron_autonomous_agent", "neuron_roi_tracker", ConnectionWeight.LOWEST),
    
    # 输出层连接
    ("neuron_narrative_intel", "output_response", ConnectionWeight.MAX),
    ("neuron_autonomous_agent", "output_action", ConnectionWeight.HIGHER),
    ("neuron_learning_coord", "output_learning", ConnectionWeight.MEDIUM),
    ("neuron_reinforcement", "output_feedback", ConnectionWeight.MEDIUM),
    
    # 反馈循环
    ("output_feedback", "input_feedback", ConnectionWeight.LOWEST),
    ("input_feedback", "neuron_learning_coord", ConnectionWeight.LOW),
]


# ============ 神经元定义数据 ============
_INPUT_NEURONS: List[Tuple[str, str, str]] = [
    ("input_user", "用户输入", "接收用户原始输入"),
    ("input_context", "上下文输入", "接收环境和上下文信息"),
    ("input_feedback", "反馈输入", "接收系统反馈信号"),
    ("input_external", "外部输入", "接收外部系统数据"),
]

_MAIN_CHAIN_NEURONS: List[Tuple[str, NeuronType, str, str]] = [
    ("neuron_agent_core", NeuronType.HIDDEN, "AgentCore", "智能体核心"),
    ("neuron_somn_core", NeuronType.HIDDEN, "SomnCore", "Somn核心"),
    ("neuron_super_wisdom", NeuronType.HIDDEN, "SuperWisdomCoordinator", "超级智慧协调器"),
    ("neuron_unified_intel", NeuronType.HIDDEN, "UnifiedIntelligenceCoordinator", "统一智能协调器"),
    ("neuron_global_scheduler", NeuronType.HIDDEN, "GlobalWisdomScheduler", "全局智慧调度器"),
    ("neuron_wisdom_dispatcher", NeuronType.WISDOM, "WisdomDispatcher", "智慧分发器"),
    ("neuron_thinking_fusion", NeuronType.HIDDEN, "ThinkingMethodFusionEngine", "思维融合引擎"),
    ("neuron_deep_reasoning", NeuronType.HIDDEN, "DeepReasoningEngine", "深度推理引擎"),
    ("neuron_tier3_scheduler", NeuronType.HIDDEN, "Tier3NeuralScheduler", "Tier3神经调度器"),
    ("neuron_narrative_intel", NeuronType.HIDDEN, "NarrativeIntelligenceEngine", "叙事智能引擎"),
    ("neuron_learning_coord", NeuronType.HIDDEN, "LearningCoordinator", "学习协调器"),
    ("neuron_autonomous_agent", NeuronType.HIDDEN, "AutonomousAgent", "自主智能体"),
    ("neuron_neural_memory", NeuronType.MEMORY, "NeuralMemorySystem", "神经记忆系统"),
    ("neuron_semantic_memory", NeuronType.MEMORY, "SemanticMemoryEngine", "语义记忆引擎"),
    ("neuron_reinforcement", NeuronType.HIDDEN, "ReinforcementTrigger", "强化触发器"),
    ("neuron_roi_tracker", NeuronType.HIDDEN, "ROITracker", "ROI追踪器"),
]

_WISDOM_NEURONS: List[Tuple[str, str, str, str]] = [
    ("wisdom_confucian", "CONFUCIAN", "儒家", "仁义礼智信"),
    ("wisdom_taoist", "TAOIST", "道家", "道法自然"),
    ("wisdom_buddhist", "BUDDHIST", "佛家", "明心见性"),
    ("wisdom_sunzi", "SUNZI", "孙子兵法", "兵者诡道"),
    ("wisdom_sufu", "SUFU", "素书", "五德智慧"),
    ("wisdom_lushi", "LUSHI", "吕氏春秋", "兼容并蓄"),
    ("wisdom_hongming", "HONGMING", "辜鸿铭", "温良精神"),
    ("wisdom_yangming", "YANGMING", "王阳明", "知行合一"),
    ("wisdom_dewey", "DEWEY", "杜威", "反省思维"),
    ("wisdom_top_methods", "TOP_METHODS", "顶级思维", "思维模型"),
    ("wisdom_psychology", "PSYCHOLOGY", "心理营销", "消费者心理"),
    ("wisdom_science", "SCIENCE", "自然科学", "科学方法"),
    ("wisdom_neuroscience", "NEUROSCIENCE", "计算神经", "神经科学"),
    ("wisdom_math", "MATH", "数学", "数学思维"),
    ("wisdom_thinking", "THINKING", "思维融合", "思维方法"),
    ("wisdom_consumer", "CONSUMER", "消费文化", "中国社会消费"),
    ("wisdom_history", "HISTORY", "历史思想", "历史智慧"),
    ("wisdom_social", "SOCIAL", "社会科学", "社会分析"),
    ("wisdom_sanguo", "SANGUO", "三国演义", "三国智慧"),
    ("wisdom_shuihu", "SHUIHU", "水浒传", "水浒智慧"),
    ("wisdom_xiyou", "XIYOU", "西游记", "西游智慧"),
    ("wisdom_honglou", "HONGLOU", "红楼梦", "红楼智慧"),
    ("wisdom_chinese_consumer", "CHINESE_CONSUMER", "中国消费", "中国消费文化"),
]

_MEMORY_NEURONS: List[Tuple[str, str, str]] = [
    ("memory_episodic", "情景记忆", "存储具体经历"),
    ("memory_semantic", "语义记忆", "存储概念知识"),
    ("memory_procedural", "程序记忆", "存储技能方法"),
    ("memory_working", "工作记忆", "临时信息处理"),
    ("memory_user_profile", "用户画像", "用户偏好特征"),
    ("memory_conversation", "对话历史", "对话上下文"),
]

_AUTONOMY_NEURONS: List[Tuple[str, NeuronType, str, str]] = [
    ("autonomy_goal", NeuronType.HIDDEN, "目标管理", "自主目标设定"),
    ("autonomy_plan", NeuronType.HIDDEN, "规划执行", "自主规划执行"),
    ("autonomy_reflection", NeuronType.HIDDEN, "反思学习", "自主反思学习"),
    ("autonomy_adaptation", NeuronType.HIDDEN, "适应调整", "自主适应调整"),
]

_OUTPUT_NEURONS: List[Tuple[str, str, str]] = [
    ("output_response", "响应输出", "生成用户响应"),
    ("output_action", "行动输出", "执行具体行动"),
    ("output_learning", "学习输出", "更新学习状态"),
    ("output_feedback", "反馈输出", "产生系统反馈"),
]


class FunctionNeuron(NeuronNode):
    """
    功能神经元 - 封装具体功能模块
    
    继承自NeuronNode，添加函数处理器能力，
    可以在接收到信号时调用实际的功能逻辑。
    """
    
    def __init__(
        self,
        neuron_id: str,
        neuron_type: NeuronType,
        name: str,
        description: str,
        *,
        function_handler: Optional[Callable] = None
    ):
        super().__init__(neuron_id, neuron_type, name, description)
        self.function_handler = function_handler
    
    def __repr__(self) -> str:
        return f"FunctionNeuron(id={self.neuron_id!r}, name={self.name!r}, handler={self.function_handler is not None})"
    
    def set_handler(self, handler: Callable) -> None:
        """设置功能处理器"""
        self.function_handler = handler
    
    def process(self, signal: Signal) -> Signal:
        """处理信号 - 调用实际功能"""
        if self.function_handler:
            try:
                result = self.function_handler(signal.data)
                return signal.copy_with(
                    source_id=self.neuron_id,
                    data=result,
                    metadata={**signal.metadata, "processed_by": self.name}
                )
            except Exception as e:
                return signal.copy_with(
                    source_id=self.neuron_id,
                    data={"error": "操作失败"},
                    signal_type=SignalType.ERROR
                )
        
        # 默认处理 - 透传信号
        return signal.copy_with(
            source_id=self.neuron_id,
            metadata={**signal.metadata, "passed_through": self.name}
        )


class NetworkLayoutManager:
    """
    网络布局管理器
    
    将Somn系统的所有功能模块映射到神经网络布局，实现：
    1. 主链路节点神经元化
    2. 智慧学派神经元化
    3. 记忆系统神经元化
    4. 自主系统神经元化
    5. 全链路自动连接
    
    Attributes:
        network: 神经网络实例
        main_chain_mapping: 主链路节点映射 (模块名 -> 神经元ID)
        wisdom_mapping: 智慧学派映射 (学派ID -> 神经元ID)
        memory_mapping: 记忆节点映射 (记忆类型 -> 神经元ID)
        autonomy_mapping: 自主功能映射 (功能名 -> 神经元ID)
    """
    
    def __init__(self, network_name: str = "somn_global_layout") -> None:
        self.network = NeuralNetwork(network_name)
        self.initialized = False
        self._lock = threading.RLock()
        self._connection_stats: Dict[str, int] = {"success": 0, "failed": 0}
        
        # 节点映射表
        self.main_chain_mapping: Dict[str, str] = {}
        self.wisdom_mapping: Dict[str, str] = {}
        self.memory_mapping: Dict[str, str] = {}
        self.autonomy_mapping: Dict[str, str] = {}
        
        # Phase 系统集成（延迟初始化）
        self._phase3 = None       # Phase3FeedbackLoop
        self._phase4 = None       # Phase4DynamicActivation
        self._phase5 = None       # Phase5EmergenceVerification
        self._cluster_optimizer = None  # ClusterOptimizer
        self._phase3_thread = None
        self._phase_status = PhaseSystemStatus()
        self._execution_history: List[Dict] = []  # 执行历史记录
    
    def __repr__(self) -> str:
        return (
            f"NetworkLayoutManager(initialized={self.initialized}, "
            f"main_chain={len(self.main_chain_mapping)}, "
            f"wisdom={len(self.wisdom_mapping)}, "
            f"memory={len(self.memory_mapping)})"
        )
    
    def initialize_global_layout(self, timeout: float = 120.0) -> bool:
        """
        初始化全局神经网络布局（修复版：添加超时保护和进度反馈）
        
        将Somn系统的所有功能模块映射到神经网络
        
        Args:
            timeout: 超时时间（秒），默认120秒
        """
        import time
        from ...timeout_utils import run_with_timeout, TimeoutException
        
        with self._lock:
            if self.initialized:
                return True
            
            start_time = time.time()
            logger.info(f"[神经网络] 开始初始化全局布局（超时: {timeout}s）...")
            
            try:
                # 使用超时保护执行初始化
                def _do_initialize():
                    """内部初始化函数"""
                    # 1. 创建输入层
                    logger.info("[神经网络] Step 1/8: 创建输入层...")
                    self._create_input_layer()
                    
                    # 2. 创建主链路层
                    logger.info("[神经网络] Step 2/8: 创建主链路层...")
                    self._create_main_chain_layer()
                    
                    # 3. 创建智慧学派层
                    logger.info("[神经网络] Step 3/8: 创建智慧学派层...")
                    self._create_wisdom_layer()
                    
                    # 4. 创建记忆层
                    logger.info("[神经网络] Step 4/8: 创建记忆层...")
                    self._create_memory_layer()
                    
                    # 5. 创建自主系统层
                    logger.info("[神经网络] Step 5/8: 创建自主系统层...")
                    self._create_autonomy_layer()
                    
                    # 6. 创建输出层
                    logger.info("[神经网络] Step 6/8: 创建输出层...")
                    self._create_output_layer()
                    
                    # 7. 建立全链路连接
                    logger.info("[神经网络] Step 7/8: 建立全链路连接...")
                    self._establish_full_chain_connections()
                    
                    # 8. 启动 Phase 子系统（独立异常处理，不影响布局初始化）
                    logger.info("[神经网络] Step 8/8: 启动 Phase 子系统...")
                    try:
                        self._init_phase_systems()
                    except Exception as e:
                        logger.warning(f"[LayoutManager] Phase 子系统启动异常（不影响布局）: {e}")
                
                # 使用超时保护执行初始化
                from ..timeout_utils import run_with_timeout, TimeoutException
                run_with_timeout(_do_initialize, timeout=timeout, description="神经网络布局初始化")
                
                self.initialized = True
                elapsed = time.time() - start_time
                logger.info(
                    f"[神经网络] ✅ 全局布局初始化完成（耗时 {elapsed:.1f}s）: "
                    f"{len(self.main_chain_mapping)}个主链路节点, "
                    f"{len(self.wisdom_mapping)}个智慧学派, "
                    f"{len(self.memory_mapping)}个记忆节点, "
                    f"{len(self.autonomy_mapping)}个自主功能"
                )
                
                return True
                
            except TimeoutException as e:
                elapsed = time.time() - start_time
                logger.error(f"[神经网络] ❌ 初始化超时（耗时 {elapsed:.1f}s）: {e}")
                return False
            except Exception as e:
                elapsed = time.time() - start_time
                logger.exception(f"[神经网络] ❌ 初始化失败（耗时 {elapsed:.1f}s）: {e}")
                return False
    
    def _create_input_layer(self) -> None:
        """创建输入层神经元"""
        for neuron_id, name, desc in _INPUT_NEURONS:
            neuron = InputNeuron(neuron_id, name, desc)
            self.network.register_neuron(neuron)
    
    def _create_main_chain_layer(self) -> None:
        """创建主链路层神经元"""
        for neuron_id, neuron_type, name, desc in _MAIN_CHAIN_NEURONS:
            neuron = self._create_function_neuron(neuron_id, neuron_type, name, desc)
            self.network.register_neuron(neuron)
            self.main_chain_mapping[name] = neuron_id
    
    def _create_wisdom_layer(self) -> None:
        """创建智慧学派层神经元"""
        for neuron_id, school_id, name, desc in _WISDOM_NEURONS:
            neuron = WisdomNeuron(neuron_id, school_id, name, desc)
            self.network.register_neuron(neuron)
            self.wisdom_mapping[school_id] = neuron_id
    
    def _create_memory_layer(self) -> None:
        """创建记忆层神经元"""
        for neuron_id, name, desc in _MEMORY_NEURONS:
            neuron = MemoryNeuron(neuron_id, name, desc)
            self.network.register_neuron(neuron)
            self.memory_mapping[name] = neuron_id
    
    def _create_autonomy_layer(self) -> None:
        """创建自主系统层神经元"""
        for neuron_id, neuron_type, name, desc in _AUTONOMY_NEURONS:
            neuron = self._create_function_neuron(neuron_id, neuron_type, name, desc)
            self.network.register_neuron(neuron)
            self.autonomy_mapping[name] = neuron_id
    
    def _create_output_layer(self) -> None:
        """创建输出层神经元"""
        for neuron_id, name, desc in _OUTPUT_NEURONS:
            neuron = OutputNeuron(neuron_id, name, desc)
            self.network.register_neuron(neuron)
    
    def _create_function_neuron(
        self,
        neuron_id: NeuronID,
        neuron_type: NeuronType,
        name: str,
        description: str,
        *,
        handler: Optional[Callable] = None
    ) -> FunctionNeuron:
        """
        创建功能神经元
        
        Args:
            neuron_id: 神经元唯一标识
            neuron_type: 神经元类型
            name: 神经元名称
            description: 神经元描述
            handler: 可选的功能处理器
            
        Returns:
            创建的功能神经元实例
        """
        return FunctionNeuron(neuron_id, neuron_type, name, description, function_handler=handler)
    
    def _connect_safe(
        self,
        source_id: NeuronID,
        target_id: NeuronID,
        connection_type: ConnectionType,
        weight: float
    ) -> bool:
        """安全建立连接，失败时记录警告日志"""
        synapse = self.network.connect(source_id, target_id, connection_type, weight)
        if synapse is None:
            logger.warning(f"连接建立失败: {source_id} -> {target_id} (神经元可能未注册)")
            return False
        return True

    def _establish_full_chain_connections(self) -> None:
        """
        建立全链路连接
        
        使用预定义的连接定义建立所有必要的连接，
        包括到智慧学派和记忆节点的动态连接。
        """
        self._connection_stats = {"success": 0, "failed": 0}
        
        # 1. 建立预定义连接
        for source_id, target_id, weight in _CONNECTION_DEFINITIONS:
            if self._connect_safe(source_id, target_id, ConnectionType.EXCITATORY, weight):
                self._connection_stats["success"] += 1
            else:
                self._connection_stats["failed"] += 1
        
        # 2. 智慧分发器 -> 各智慧学派 (动态连接)
        wisdom_to_dispatcher_weight = ConnectionWeight.MEDIUM
        for school_neuron_id in self.wisdom_mapping.values():
            if self._connect_safe("neuron_wisdom_dispatcher", school_neuron_id, ConnectionType.EXCITATORY, wisdom_to_dispatcher_weight):
                self._connection_stats["success"] += 1
            else:
                self._connection_stats["failed"] += 1

        # 3. 智慧学派 -> 思维融合 (动态连接)
        school_to_fusion_weight = ConnectionWeight.LOW
        for school_neuron_id in self.wisdom_mapping.values():
            if self._connect_safe(school_neuron_id, "neuron_thinking_fusion", ConnectionType.EXCITATORY, school_to_fusion_weight):
                self._connection_stats["success"] += 1
            else:
                self._connection_stats["failed"] += 1

        # 4. 记忆层内部连接 (动态连接)
        memory_to_neural_weight = ConnectionWeight.LOWEST
        for memory_id in self.memory_mapping.values():
            if self._connect_safe(memory_id, "neuron_neural_memory", ConnectionType.EXCITATORY, memory_to_neural_weight):
                self._connection_stats["success"] += 1
            else:
                self._connection_stats["failed"] += 1

        # 记录连接统计
        total = self._connection_stats["success"] + self._connection_stats["failed"]
        if self._connection_stats["failed"] > 0:
            rate = self._connection_stats["success"] / total * 100
            logger.warning(
                f"全链路连接建立: 成功{self._connection_stats['success']}条, "
                f"失败{self._connection_stats['failed']}条, 成功率{rate:.1f}%"
            )
        else:
            logger.debug(f"全链路连接建立完成: 共{self._connection_stats['success']}条连接")
    
    def get_connection_stats(self) -> Dict[str, int]:
        """获取连接统计信息"""
        return self._connection_stats.copy()
    
    def activate_main_chain(self, input_data: Any) -> Dict[str, Any]:
        """
        激活主链路 (V2: 集成 Phase 4 动态激活 + Phase 3 反馈记录)
        
        线程安全的主链路激活方法，使用锁保护初始化状态。
        
        Args:
            input_data: 要处理的输入数据
            
        Returns:
            包含激活结果的字典
        """
        start_time = time.time()
        query_text = ""
        if isinstance(input_data, dict):
            query_text = input_data.get("query", input_data.get("data", ""))
        elif isinstance(input_data, str):
            query_text = input_data
        
        try:
            # 线程安全的初始化检查
            need_init = False
            with self._lock:
                if not self.initialized:
                    need_init = True
            
            if need_init:
                if not self.initialize_global_layout():
                    logger.error("主链路激活失败: 布局初始化失败")
                    return {"error": "layout initialization failed"}
            
            # --- Phase 4: 动态网络激活 (任务分类) ---
            phase4_result = {}
            if self._phase4 and query_text:
                try:
                    # Phase4 是异步的，这里用 asyncio.run 在子线程执行
                    loop = asyncio.new_event_loop()
                    try:
                        phase4_result = loop.run_until_complete(
                            self._phase4.process_task(query_text, input_data if isinstance(input_data, dict) else None)
                        )
                    finally:
                        loop.close()
                    self._phase_status.phase4_classifications = len(
                        self._phase4.classifier.classification_history
                    )
                    self._phase_status.phase4_active_subnetworks = len(
                        self._phase4.active_subnetworks
                    )
                except Exception as e:
                    logger.warning(f"Phase4 动态激活跳过: {e}")
                    phase4_result = {"phase4_error": "Phase4执行失败"}
            
            # 从用户输入开始（传统激活路径）
            signals = self.network.emit_signal(
                "input_user",
                SignalType.DATA,
                input_data,
                strength=ConnectionWeight.MAX,
                priority=SignalPriority.HIGH
            )
            
            # 激活通路
            pathway = self.network.activate_pathway(
                "input_user",
                SignalType.DATA,
                input_data,
                max_depth=10
            )
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # --- Phase 3: 反馈回路记录 ---
            if self._phase3:
                try:
                    loop = asyncio.new_event_loop()
                    try:
                        loop.run_until_complete(
                            self._phase3.record_execution(
                                module_name="main_chain",
                                success=True,
                                output={"signals_emitted": len(signals)},
                                duration_ms=processing_time_ms
                            )
                        )
                    finally:
                        loop.close()
                    self._phase_status.phase3_executions = len(
                        self._phase3.collector.execution_history
                    )
                except Exception as e:
                    logger.debug(f"Phase3 反馈记录跳过: {e}")
            
            # 记录执行历史
            self._execution_history.append({
                "timestamp": time.time(),
                "query": query_text[:100] if query_text else "",
                "signals": len(signals),
                "pathway_steps": len(pathway),
                "processing_ms": round(processing_time_ms, 2),
                "phase4_task_type": phase4_result.get("task_type"),
                "phase4_neurons": phase4_result.get("neurons_activated", 0),
            })
            # 保留最近 200 条
            if len(self._execution_history) > 200:
                self._execution_history = self._execution_history[-200:]
            
            return {
                "signals_emitted": len(signals),
                "pathway": pathway,
                "network_state": self.network.get_network_topology(),
                "connection_stats": self.get_connection_stats(),
                "processing_time_ms": round(processing_time_ms, 2),
                "phase4_activation": phase4_result,
                "execution_history_count": len(self._execution_history),
            }
        except Exception as e:
            logger.exception(f"主链路激活异常: {e}")
            return {"error": "操作失败"}
    
    def get_layout_status(self) -> Dict:
        """获取布局状态"""
        return {
            "initialized": self.initialized,
            "network_topology": self.network.get_network_topology(),
            "main_chain_nodes": len(self.main_chain_mapping),
            "wisdom_nodes": len(self.wisdom_mapping),
            "memory_nodes": len(self.memory_mapping),
            "autonomy_nodes": len(self.autonomy_mapping),
            "neuron_stats": self.network.get_neuron_stats()
        }
    
    def find_optimal_path(self, start_module: str, end_module: str) -> Optional[List[NeuronID]]:
        """
        查找两个模块之间的最优路径
        
        Args:
            start_module: 起始模块名称
            end_module: 目标模块名称
            
        Returns:
            最优路径的神经元ID列表，如果找不到则返回None
        """
        start_id = self.main_chain_mapping.get(start_module)
        end_id = self.main_chain_mapping.get(end_module)
        
        if not start_id or not end_id:
            logger.debug(f"路径查找失败: {start_module}或{end_module}未注册")
            return None
        
        return self.network.find_path(start_id, end_id)
    
    def register_function_handler(self, module_name: str, handler: Callable[[Any], Any]) -> bool:
        """
        为主链路节点注册功能处理器
        
        Args:
            module_name: 模块名称 (如 "SomnCore", "AgentCore" 等)
            handler: 要注册的处理函数
            
        Returns:
            是否注册成功
        """
        neuron_id = self.main_chain_mapping.get(module_name)
        if not neuron_id:
            logger.warning(f"注册失败: 模块 {module_name} 未找到")
            return False
        
        neuron = self.network.get_neuron(neuron_id)
        if neuron is None:
            logger.warning(f"注册失败: 神经元 {neuron_id} 不存在")
            return False
        
        if isinstance(neuron, FunctionNeuron):
            neuron.set_handler(handler)
            logger.debug(f"功能处理器已注册: {module_name}")
            return True
        else:
            logger.warning(f"注册失败: {neuron_id} 不是功能神经元")
            return False
    
    def get_neuron_by_module(self, module_name: str) -> Optional[NeuronNode]:
        """
        根据模块名称获取神经元实例
        
        Args:
            module_name: 模块名称
            
        Returns:
            神经元实例，如果不存在则返回None
        """
        neuron_id = self.main_chain_mapping.get(module_name)
        if neuron_id:
            return self.network.get_neuron(neuron_id)
        return None

    # ==================== Phase 系统集成 ====================

    def _init_phase_systems(self) -> None:
        """初始化 Phase 3/4/5 子系统和 ClusterOptimizer（修复版：添加超时保护）"""
        
        # Phase3 初始化（带超时保护）
        try:
            from .phase3_feedback_loop import get_phase3_feedback_loop
            self._phase3 = get_phase3_feedback_loop()
            
            def _run_phase3():
                """在新线程中运行 Phase3"""
                loop = asyncio.new_event_loop()
                try:
                    # 为 start() 添加超时保护（使用 asyncio.wait_for）
                    logger.info("[LayoutManager] 正在启动 Phase3（超时: 30s）...")
                    try:
                        loop.run_until_complete(
                            asyncio.wait_for(self._phase3.start(), timeout=30.0)
                        )
                        self._phase_status.phase3_running = True
                        logger.info("[LayoutManager] ✅ Phase3 反馈回路已启动")
                    except asyncio.TimeoutError:
                        logger.error("[LayoutManager] ❌ Phase3 启动超时（30s），跳过启动")
                        return
                    except Exception as e:
                        logger.warning(f"[LayoutManager] Phase3 启动失败: {e}")
                    else:
                        # 只有在成功启动后才保持 loop 运行
                        try:
                            loop.run_forever()
                        except Exception as e:
                            logger.debug(f"[LayoutManager] Phase3 事件循环退出: {e}")
                except Exception as e:
                    logger.debug(f"[LayoutManager] Phase3 线程异常: {e}")
                finally:
                    # 确保事件循环关闭
                    if not loop.is_closed():
                        loop.close()
            
            # 在新线程中运行 Phase3
            self._phase3_thread = threading.Thread(
                target=_run_phase3, daemon=True, name="phase3-feedback-loop"
            )
            self._phase3_thread.start()
            logger.info("[LayoutManager] Phase3 线程已启动")
        except Exception as e:
            logger.warning(f"[LayoutManager] Phase3 初始化失败: {e}")

        # Phase4 初始化（带超时保护）
        try:
            def _init_phase4():
                from .phase4_dynamic_activation import get_phase4_dynamic_activation
                self._phase4 = get_phase4_dynamic_activation()
                logger.info("[LayoutManager] Phase4 动态激活引擎就绪")
            
            run_with_timeout(_init_phase4, timeout=30.0, description="Phase4初始化")
        except TimeoutException:
            logger.warning("[LayoutManager] Phase4 初始化超时（30s），跳过")
        except Exception as e:
            logger.warning(f"[LayoutManager] Phase4 初始化失败: {e}")

        # Phase5 初始化（带超时保护）
        try:
            def _init_phase5():
                from .phase5_emergence_verification import get_phase5_verification
                self._phase5 = get_phase5_verification()
                logger.info("[LayoutManager] Phase5 涌现验证引擎就绪")
            
            run_with_timeout(_init_phase5, timeout=30.0, description="Phase5初始化")
        except TimeoutException:
            logger.warning("[LayoutManager] Phase5 初始化超时（30s），跳过")
        except Exception as e:
            logger.warning(f"[LayoutManager] Phase5 初始化失败: {e}")

        # ClusterOptimizer 初始化（带超时保护）
        try:
            def _init_cluster():
                from .cluster_optimizer import get_cluster_optimizer, ClusterConfig
                self._cluster_optimizer = get_cluster_optimizer()
                self._auto_register_clusters()
                logger.info("[LayoutManager] ClusterOptimizer 就绪")
            
            run_with_timeout(_init_cluster, timeout=30.0, description="ClusterOptimizer初始化")
        except TimeoutException:
            logger.warning("[LayoutManager] ClusterOptimizer 初始化超时（30s），跳过")
        except Exception as e:
            logger.warning(f"[LayoutManager] ClusterOptimizer 初始化失败: {e}")

    def _auto_register_clusters(self) -> None:
        """根据节点映射自动注册集群"""
        if not self._cluster_optimizer:
            return

        from .cluster_optimizer import ClusterConfig

        clusters = [
            ("main_chain", list(self.main_chain_mapping.values()), "核心主链路集群"),
            ("wisdom", list(self.wisdom_mapping.values()), "智慧学派集群"),
            ("memory", list(self.memory_mapping.values()), "记忆系统集群"),
            ("autonomy", list(self.autonomy_mapping.values()), "自主系统集群"),
        ]
        
        for cluster_id, nodes, desc in clusters:
            if nodes:
                config = ClusterConfig(
                    cluster_id=cluster_id,
                    nodes=nodes,
                    optimization_level=3,
                    target_density=0.7
                )
                self._cluster_optimizer.register_cluster(config)
        
        self._phase_status.cluster_count = len(clusters)

    def get_phase_status(self) -> Dict[str, Any]:
        """获取 Phase 系统状态"""
        status = {
            "phase3": {
                "running": self._phase_status.phase3_running,
                "executions": self._phase_status.phase3_executions,
                "insights": self._phase_status.phase3_insights,
            },
            "phase4": {
                "classifications": self._phase_status.phase4_classifications,
                "active_subnetworks": self._phase_status.phase4_active_subnetworks,
            },
            "phase5": {
                "last_score": self._phase_status.phase5_last_score,
            },
            "clusters": {
                "count": self._phase_status.cluster_count,
                "optimizations": self._phase_status.cluster_optimization_history,
            },
            "execution_history_count": len(self._execution_history),
        }
        
        # 获取 Phase3 详细状态
        if self._phase3:
            try:
                status["phase3"].update(self._phase3.get_status())
            except Exception as e:
                logger.debug(f"[LayoutManager] 获取 Phase3 状态失败: {e}")
        
        # 获取 Phase4 详细状态
        if self._phase4:
            try:
                status["phase4"].update(self._phase4.get_status())
            except Exception as e:
                logger.debug(f"[LayoutManager] 获取 Phase4 状态失败: {e}")
        
        return status

    def optimize_clusters(self) -> List[Dict[str, Any]]:
        """优化所有集群连接
        
        Returns:
            优化结果列表
        """
        if not self._cluster_optimizer:
            return []
        
        results = self._cluster_optimizer.optimize_all()
        self._phase_status.cluster_optimization_history = len(
            self._cluster_optimizer._optimization_history
        )
        
        return [
            {
                "cluster_id": r.cluster_id,
                "original_cost": r.original_cost,
                "optimized_cost": r.optimized_cost,
                "improvement": f"{r.improvement:.1%}",
            }
            for r in results
        ]

    async def verify_emergence(self, duration: float = 10.0) -> Dict[str, Any]:
        """运行涌现能力验证
        
        Args:
            duration: 每个测试类型的持续时间（秒）
            
        Returns:
            验证结果
        """
        if not self._phase5:
            return {"error": "Phase5 not initialized"}
        
        try:
            result = await self._phase5.run_full_verification(duration)
            # 提取总分
            overall = result.get("overall_score", 0)
            self._phase_status.phase5_last_score = overall
            return result
        except Exception as e:
            return {"error": "操作失败"}

    def get_execution_history(self, limit: int = 20) -> List[Dict]:
        """获取最近的执行历史
        
        Args:
            limit: 返回的最大记录数
            
        Returns:
            执行历史列表
        """
        return self._execution_history[-limit:]

    def shutdown_phase_systems(self) -> None:
        """关闭 Phase 子系统"""
        # 停止 Phase3 反馈回路
        if self._phase3:
            try:
                loop = asyncio.new_event_loop()
                try:
                    loop.run_until_complete(self._phase3.stop())
                finally:
                    loop.close()
                self._phase_status.phase3_running = False
                logger.info("[LayoutManager] Phase3 反馈回路已停止")
            except Exception as e:
                logger.warning(f"[LayoutManager] Phase3 停止失败: {e}")
