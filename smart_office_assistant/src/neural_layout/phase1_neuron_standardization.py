"""
__all__ = [
    'activate',
    'activate_async',
    'add_incoming_synapse',
    'add_outgoing_synapse',
    'create_input_neuron',
    'create_memory_neuron',
    'create_output_neuron',
    'create_processing_neuron',
    'create_wisdom_neuron',
    'get_activation_history',
    'get_profile',
    'get_stats',
    'remove_synapse',
    'reset',
]

Phase 1: 神经元节点标准化
标准化激活接口，统一所有神经元的处理模式
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable, Set, Tuple, Union
import uuid
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .signal import Signal, SignalType, SignalBatch, SignalPriority
from .synapse_connection import SynapseConnection, ConnectionType

class ActivationMode(Enum):
    """激活模式"""
    SYNCHRONOUS = auto()      # 同步激活
    ASYNCHRONOUS = auto()     # 异步激活
    BATCH = auto()            # 批量激活
    CONDITIONAL = auto()      # 条件激活

class ActivationState(Enum):
    """激活状态"""
    IDLE = auto()             # 空闲
    PROCESSING = auto()       # 处理中
    COMPLETED = auto()        # 完成
    FAILED = auto()           # 失败
    TIMEOUT = auto()          # 超时

@dataclass
class ActivationContext:
    """激活上下文 - 标准化激活参数"""
    # 基础参数
    input_data: Any = None
    signal_type: SignalType = SignalType.DATA
    priority: SignalPriority = SignalPriority.NORMAL
    strength: float = 1.0
    
    # 控制参数
    activation_mode: ActivationMode = ActivationMode.SYNCHRONOUS
    timeout_ms: int = 5000
    max_retries: int = 0
    
    # 路由参数
    target_neurons: Optional[List[str]] = None
    exclude_neurons: Optional[List[str]] = None
    
    # 上下文传递
    parent_context_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # 追踪
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ActivationResult:
    """激活结果 - 标准化输出格式"""
    # 标识
    context_id: str
    neuron_id: str
    
    # 状态
    state: ActivationState
    success: bool
    
    # 数据
    output_data: Any = None
    output_signal: Optional[Signal] = None
    
    # 性能指标
    processing_time_ms: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # 追踪
    signal_trace: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

class StandardizedNeuron(ABC):
    """
    标准化神经元基类
    
    所有神经元的统一接口规范，支持：
    - 标准化激活接口
    - 多模式激活（同步/异步/批量/条件）
    - 统一的上下文和结果格式
    - 性能监控和追踪
    """
    
    def __init__(
        self,
        neuron_id: str,
        neuron_type: str,
        name: str = "",
        description: str = ""
    ):
        self.neuron_id = neuron_id
        self.neuron_type = neuron_type
        self.name = name or neuron_id
        self.description = description
        
        # 状态管理
        self._state = ActivationState.IDLE
        self._activation_level = 0.0
        self._threshold = 0.5
        
        # 连接管理
        self._incoming_synapses: Dict[str, SynapseConnection] = {}
        self._outgoing_synapses: Dict[str, SynapseConnection] = {}
        
        # 性能统计
        self._stats = {
            "total_activations": 0,
            "successful_activations": 0,
            "failed_activations": 0,
            "total_processing_time_ms": 0.0,
            "avg_processing_time_ms": 0.0,
            "peak_activation_level": 0.0
        }
        
        # 线程安全
        self._lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=2)
        
        # 历史记录
        self._activation_history: List[Dict] = []
        self._max_history_size = 100
        
        # 画像
        self._profile = {
            "capabilities": [],
            "keywords": [],
            "input_schema": None,
            "output_schema": None,
            "typical_processing_time_ms": 100
        }
    
    # ============ 标准化激活接口 ============
    
    def activate(self, context: ActivationContext) -> ActivationResult:
        """
        标准化激活接口 - 同步入口
        
        Args:
            context: 激活上下文
            
        Returns:
            ActivationResult: 标准化的激活结果
        """
        start_time = datetime.now()
        
        with self._lock:
            self._state = ActivationState.PROCESSING
            self._stats["total_activations"] += 1
        
        try:
            # 根据激活模式选择处理方式
            if context.activation_mode == ActivationMode.SYNCHRONOUS:
                result = self._activate_sync(context)
            elif context.activation_mode == ActivationMode.ASYNCHRONOUS:
                result = self._activate_async(context)
            elif context.activation_mode == ActivationMode.BATCH:
                result = self._activate_batch(context)
            elif context.activation_mode == ActivationMode.CONDITIONAL:
                result = self._activate_conditional(context)
            else:
                result = self._activate_sync(context)
            
            # 更新统计
            self._update_stats(result)
            
            return result
            
        except Exception as e:
            return self._create_error_result(context, "神经元标准化失败", start_time)
    
    async def activate_async(self, context: ActivationContext) -> ActivationResult:
        """异步激活入口"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self.activate, context)
    
    @abstractmethod
    def _process(self, context: ActivationContext) -> Tuple[Any, Optional[Signal]]:
        """
        子类必须实现的核心处理逻辑
        
        Args:
            context: 激活上下文
            
        Returns:
            Tuple[output_data, output_signal]: 输出数据和信号
        """
        pass
    
    # ============ 内部激活实现 ============
    
    def _activate_sync(self, context: ActivationContext) -> ActivationResult:
        """同步激活实现"""
        start_time = datetime.now()
        
        # 执行核心处理
        output_data, output_signal = self._process(context)
        
        # 传播到下游神经元
        propagated_signals = []
        if output_signal:
            propagated_signals = self._propagate_signal(output_signal, context)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        return ActivationResult(
            context_id=context.context_id,
            neuron_id=self.neuron_id,
            state=ActivationState.COMPLETED,
            success=True,
            output_data=output_data,
            output_signal=output_signal,
            processing_time_ms=processing_time,
            start_time=start_time,
            end_time=end_time,
            signal_trace=[self.neuron_id] + [s.source_id for s in propagated_signals],
            metadata={"propagated_count": len(propagated_signals)}
        )
    
    def _activate_async(self, context: ActivationContext) -> ActivationResult:
        """异步激活实现（内部使用）"""
        # 异步模式下转为同步处理，但返回Future
        return self._activate_sync(context)
    
    def _evaluate_condition(self, condition: Dict[str, Any], context: ActivationContext) -> bool:
        """评估激活条件"""
        condition_type = condition.get("type", "always")
        
        if condition_type == "threshold":
            return self._activation_level >= condition.get("value", self._threshold)
        elif condition_type == "signal_type":
            return context.signal_type.name == condition.get("value")
        elif condition_type == "custom":
            evaluator = condition.get("evaluator")
            if evaluator and callable(evaluator):
                return evaluator(context)
        
        return True
    
    def _activate_batch(self, context: ActivationContext) -> ActivationResult:
        """批量激活实现"""
        # 批量处理输入数据
        input_batch = context.input_data
        if not isinstance(input_batch, list):
            input_batch = [input_batch]
        
        results = []
        for item in input_batch:
            batch_context = ActivationContext(
                input_data=item,
                signal_type=context.signal_type,
                priority=context.priority,
                strength=context.strength,
                activation_mode=ActivationMode.SYNCHRONOUS,
                parent_context_id=context.context_id
            )
            result = self._activate_sync(batch_context)
            results.append(result)
        
        # 合并结果
        return ActivationResult(
            context_id=context.context_id,
            neuron_id=self.neuron_id,
            state=ActivationState.COMPLETED,
            success=all(r.success for r in results),
            output_data=[r.output_data for r in results],
            output_signal=None,
            processing_time_ms=sum(r.processing_time_ms for r in results),
            metadata={"batch_size": len(results), "batch_results": results}
        )
    
    def _activate_conditional(self, context: ActivationContext) -> ActivationResult:
        """条件激活实现"""
        # 检查激活条件
        condition = context.metadata.get("activation_condition")
        if condition and not self._evaluate_condition(condition, context):
            return ActivationResult(
                context_id=context.context_id,
                neuron_id=self.neuron_id,
                state=ActivationState.IDLE,
                success=True,
                output_data=None,
                metadata={"skipped": True, "reason": "condition_not_met"}
            )
        
        return self._activate_sync(context)
    
    def _evaluate_condition(self, condition: Dict, context: ActivationContext) -> bool:
        """评估激活条件"""
        condition_type = condition.get("type", "always")
        
        if condition_type == "threshold":
            return self._activation_level >= condition.get("value", self._threshold)
        elif condition_type == "signal_type":
            return context.signal_type.name == condition.get("value")
        elif condition_type == "custom":
            evaluator = condition.get("evaluator")
            if evaluator and callable(evaluator):
                return evaluator(context)
        
        return True
    
    def _propagate_signal(
        self,
        signal: Signal,
        context: ActivationContext
    ) -> List[Signal]:
        """传播信号到下游神经元"""
        propagated: List[Signal] = []
        
        # 路由目标预计算
        target_set = set(context.target_neurons) if context.target_neurons else None
        exclude_set = set(context.exclude_neurons) if context.exclude_neurons else None
        
        for synapse in self._outgoing_synapses.values():
            # 排除检查
            if exclude_set and synapse.target_id in exclude_set:
                continue
            # 目标白名单检查
            if target_set and synapse.target_id not in target_set:
                continue
            
            # 通过突触传递信号
            transmitted = synapse.transmit(signal)
            if transmitted:
                propagated.append(transmitted)
        
        return propagated
    
    def _create_error_result(
        self,
        context: ActivationContext,
        error: str,
        start_time: datetime
    ) -> ActivationResult:
        """创建错误结果"""
        with self._lock:
            self._state = ActivationState.FAILED
            self._stats["failed_activations"] += 1
        
        return ActivationResult(
            context_id=context.context_id,
            neuron_id=self.neuron_id,
            state=ActivationState.FAILED,
            success=False,
            errors=[error],
            processing_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            start_time=start_time,
            end_time=datetime.now()
        )
    
    def _update_stats(self, result: ActivationResult) -> None:
        """更新统计信息"""
        with self._lock:
            # 更新成功/失败计数
            if result.success:
                self._stats["successful_activations"] += 1
            else:
                self._stats["failed_activations"] += 1
            
            # 更新处理时间统计
            total_time = self._stats["total_processing_time_ms"] + result.processing_time_ms
            self._stats["total_processing_time_ms"] = total_time
            self._stats["avg_processing_time_ms"] = total_time / max(1, self._stats["total_activations"])
            
            self._state = ActivationState.IDLE
            
            # 记录历史（带截断）
            self._activation_history.append({
                "context_id": result.context_id,
                "success": result.success,
                "processing_time_ms": result.processing_time_ms,
                "timestamp": datetime.now().isoformat()
            })
            
            # 限制历史大小
            if len(self._activation_history) > self._max_history_size:
                del self._activation_history[:-self._max_history_size]
    
    # ============ 连接管理 ============
    
    def add_incoming_synapse(self, synapse: SynapseConnection) -> None:
        """添加入连接"""
        with self._lock:
            self._incoming_synapses[synapse.synapse_id] = synapse
    
    def add_outgoing_synapse(self, synapse: SynapseConnection) -> None:
        """添加出连接"""
        with self._lock:
            self._outgoing_synapses[synapse.synapse_id] = synapse
    
    def remove_synapse(self, synapse_id: str) -> bool:
        """移除连接"""
        with self._lock:
            if synapse_id in self._incoming_synapses:
                del self._incoming_synapses[synapse_id]
                return True
            if synapse_id in self._outgoing_synapses:
                del self._outgoing_synapses[synapse_id]
                return True
            return False
    
    # ============ 查询接口 ============
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._lock:
            return {
                "neuron_id": self.neuron_id,
                "neuron_type": self.neuron_type,
                "state": self._state.name,
                "activation_level": round(self._activation_level, 4),
                "threshold": self._threshold,
                **self._stats,
                "incoming_connections": len(self._incoming_synapses),
                "outgoing_connections": len(self._outgoing_synapses),
                "history_count": len(self._activation_history)
            }
    
    def get_profile(self) -> Dict:
        """获取神经元画像"""
        return {
            "neuron_id": self.neuron_id,
            "name": self.name,
            "description": self.description,
            **self._profile
        }
    
    def get_activation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取激活历史"""
        with self._lock:
            return self._activation_history[-limit:]
    
    def reset(self) -> None:
        """重置神经元状态"""
        with self._lock:
            self._state = ActivationState.IDLE
            self._activation_level = 0.0
            self._activation_history.clear()

# ============ 具体神经元类型实现 ============

class StandardizedInputNeuron(StandardizedNeuron):
    """标准化输入神经元"""
    
    def __init__(self, neuron_id: str, name: str = "", description: str = ""):
        super().__init__(neuron_id, "INPUT", name, description)
        self._threshold = 0.1
        self._profile["capabilities"] = ["input_processing", "data_validation", "format_conversion"]
    
    def _process(self, context: ActivationContext) -> Tuple[Any, Optional[Signal]]:
        """处理输入数据"""
        input_data = context.input_data
        
        # 标准化输入格式
        if isinstance(input_data, dict):
            normalized = input_data
        elif isinstance(input_data, str):
            normalized = {"text": input_data, "type": "string"}
        else:
            normalized = {"data": input_data, "type": type(input_data).__name__}
        
        # 创建输出信号
        output_signal = Signal(
            source_id=self.neuron_id,
            signal_type=context.signal_type,
            data=normalized,
            strength=context.strength,
            priority=context.priority,
            metadata={
                "input_processed": True,
                "original_type": type(input_data).__name__,
                "context_id": context.context_id
            }
        )
        
        return normalized, output_signal

class StandardizedOutputNeuron(StandardizedNeuron):
    """标准化输出神经元"""
    
    def __init__(self, neuron_id: str, name: str = "", description: str = ""):
        super().__init__(neuron_id, "OUTPUT", name, description)
        self._threshold = 0.3
        self._profile["capabilities"] = ["output_formatting", "response_generation", "result_aggregation"]
        self._output_history: List[Dict] = []
    
    def _process(self, context: ActivationContext) -> Tuple[Any, Optional[Signal]]:
        """处理输出数据"""
        input_data = context.input_data
        
        # 格式化输出
        if isinstance(input_data, dict):
            formatted = {
                "result": input_data,
                "timestamp": datetime.now().isoformat(),
                "neuron_id": self.neuron_id
            }
        else:
            formatted = {
                "result": input_data,
                "timestamp": datetime.now().isoformat(),
                "neuron_id": self.neuron_id
            }
        
        # 记录输出历史
        self._output_history.append({
            "timestamp": datetime.now().isoformat(),
            "data_summary": str(input_data)[:200] if input_data else None
        })
        
        # 限制历史大小
        if len(self._output_history) > 50:
            self._output_history = self._output_history[-50:]
        
        # 创建输出信号
        output_signal = Signal(
            source_id=self.neuron_id,
            signal_type=SignalType.OUTPUT,
            data=formatted,
            strength=context.strength,
            priority=context.priority,
            metadata={
                "final_output": True,
                "context_id": context.context_id
            }
        )
        
        return formatted, output_signal

class StandardizedProcessingNeuron(StandardizedNeuron):
    """标准化处理神经元"""
    
    def __init__(
        self,
        neuron_id: str,
        name: str = "",
        description: str = "",
        processor: Optional[Callable[[Any], Any]] = None
    ):
        super().__init__(neuron_id, "PROCESSING", name, description)
        self._processor = processor
        self._threshold = 0.4
        self._profile["capabilities"] = ["data_processing", "transformation", "computation"]
    
    def _process(self, context: ActivationContext) -> Tuple[Any, Optional[Signal]]:
        """处理数据"""
        input_data = context.input_data
        
        # 使用自定义处理器或默认处理
        if self._processor and callable(self._processor):
            try:
                output_data = self._processor(input_data)
            except Exception as e:
                return {"error": "操作失败"}, None
        else:
            # 默认处理：透传
            output_data = input_data
        
        # 创建输出信号
        output_signal = Signal(
            source_id=self.neuron_id,
            signal_type=SignalType.DATA,
            data=output_data,
            strength=context.strength * 0.95,  # 轻微衰减
            priority=context.priority,
            metadata={
                "processed": True,
                "context_id": context.context_id
            }
        )
        
        return output_data, output_signal

class StandardizedWisdomNeuron(StandardizedNeuron):
    """标准化智慧神经元 - 封装智慧学派"""
    
    def __init__(
        self,
        neuron_id: str,
        school_id: str,
        name: str = "",
        description: str = ""
    ):
        super().__init__(neuron_id, "WISDOM", name, description)
        self.school_id = school_id
        self._threshold = 0.35
        self._profile["capabilities"] = ["wisdom_application", "school_reasoning", "insight_generation"]
        self._wisdom_cache: Dict[str, Any] = {}
    
    def _process(self, context: ActivationContext) -> Tuple[Any, Optional[Signal]]:
        """处理智慧请求"""
        query = context.input_data
        
        if isinstance(query, dict):
            query_text = query.get("query", "")
        else:
            query_text = str(query)
        
        # 模拟智慧处理结果
        wisdom_result = {
            "school_id": self.school_id,
            "query": query_text,
            "insights": [f"{self.name}智慧洞察: 基于{self.school_id}学派的分析"],
            "recommendations": ["建议1", "建议2"],
            "confidence": context.strength
        }
        
        # 创建输出信号
        output_signal = Signal(
            source_id=self.neuron_id,
            signal_type=SignalType.DATA,
            data=wisdom_result,
            strength=context.strength,
            priority=context.priority,
            metadata={
                "wisdom_processed": True,
                "school": self.school_id,
                "context_id": context.context_id
            }
        )
        
        return wisdom_result, output_signal

class StandardizedMemoryNeuron(StandardizedNeuron):
    """标准化记忆神经元"""
    
    def __init__(self, neuron_id: str, name: str = "", description: str = ""):
        super().__init__(neuron_id, "MEMORY", name, description)
        self._threshold = 0.2
        self._profile["capabilities"] = ["memory_storage", "memory_retrieval", "pattern_recognition"]
        self._memory_store: Dict[str, Any] = {}
    
    def _process(self, context: ActivationContext) -> Tuple[Any, Optional[Signal]]:
        """处理记忆操作"""
        operation = context.metadata.get("memory_operation", "query")
        
        if operation == "store":
            key = context.metadata.get("memory_key", str(uuid.uuid4()))
            self._memory_store[key] = context.input_data
            result = {"operation": "store", "key": key, "success": True}
        
        elif operation == "retrieve":
            key = context.metadata.get("memory_key")
            data = self._memory_store.get(key) if key else None
            result = {"operation": "retrieve", "key": key, "data": data, "found": data is not None}
        
        elif operation == "search":
            query = context.input_data
            matches = []
            for key, value in self._memory_store.items():
                if query in str(key) or query in str(value):
                    matches.append({"key": key, "value": value})
            result = {"operation": "search", "query": query, "matches": matches, "count": len(matches)}
        
        else:  # query
            result = {
                "operation": "query",
                "memory_count": len(self._memory_store),
                "keys": list(self._memory_store.keys())[:10]
            }
        
        # 创建输出信号
        output_signal = Signal(
            source_id=self.neuron_id,
            signal_type=SignalType.DATA,
            data=result,
            strength=context.strength,
            priority=context.priority,
            metadata={
                "memory_processed": True,
                "operation": operation,
                "context_id": context.context_id
            }
        )
        
        return result, output_signal

# ============ 工厂函数 ============

def create_input_neuron(neuron_id: str, name: str = "", description: str = "") -> StandardizedInputNeuron:
    """创建输入神经元"""
    return StandardizedInputNeuron(neuron_id, name, description)

def create_output_neuron(neuron_id: str, name: str = "", description: str = "") -> StandardizedOutputNeuron:
    """创建输出神经元"""
    return StandardizedOutputNeuron(neuron_id, name, description)

def create_processing_neuron(
    neuron_id: str,
    name: str = "",
    description: str = "",
    processor: Optional[Callable[[Any], Any]] = None
) -> StandardizedProcessingNeuron:
    """创建处理神经元"""
    return StandardizedProcessingNeuron(neuron_id, name, description, processor)

def create_wisdom_neuron(
    neuron_id: str,
    school_id: str,
    name: str = "",
    description: str = ""
) -> StandardizedWisdomNeuron:
    """创建智慧神经元"""
    return StandardizedWisdomNeuron(neuron_id, school_id, name, description)

def create_memory_neuron(neuron_id: str, name: str = "", description: str = "") -> StandardizedMemoryNeuron:
    """创建记忆神经元"""
    return StandardizedMemoryNeuron(neuron_id, name, description)
