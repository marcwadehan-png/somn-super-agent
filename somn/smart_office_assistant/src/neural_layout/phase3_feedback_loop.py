"""
__all__ = [
    'adjust_weights',
    'calculate_adjustment',
    'collect_execution_result',
    'collect_from_all_modules',
    'generate_insights',
    'get_adjustment_summary',
    'get_all_performance',
    'get_feedback_status',
    'get_insights',
    'get_module_performance',
    'get_phase3_feedback_loop',
    'get_status',
    'process_feedback',
    'record_execution',
    'record_module_execution',
    'register_collector',
    'register_insight_generator',
    'register_processor',
    'start',
    'stop',
    'submit_feedback',
    'to_dict',
]

Phase 3: 反馈回路闭环 - 深度整合与跨模块洞察

构建完整的反馈回路系统，实现：
1. 执行结果自动采集
2. 反馈信号生成与传播
3. 跨模块洞察生成
4. 网络权重动态调整
"""

import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

class NeuralFeedbackType(Enum):
    """神经网络布局反馈类型（区别于其他模块的FeedbackType）"""
    EXECUTION_RESULT = auto()      # 执行结果反馈
    PERFORMANCE_METRIC = auto()    # 性能指标反馈
    ERROR_REPORT = auto()          # 错误报告
    USER_FEEDBACK = auto()         # 用户反馈
    CROSS_MODULE_INSIGHT = auto()  # 跨模块洞察
    ADAPTATION_SIGNAL = auto()     # 自适应信号

class FeedbackPriority(Enum):
    """反馈优先级"""
    CRITICAL = 1    # 关键反馈，立即处理
    HIGH = 2        # 高优先级
    NORMAL = 3      # 正常优先级
    LOW = 4         # 低优先级
    BACKGROUND = 5  # 后台处理

@dataclass
class FeedbackSignal:
    """反馈信号"""
    signal_id: str
    feedback_type: NeuralFeedbackType
    source_module: str              # 来源模块
    target_modules: List[str]       # 目标模块
    data: Dict[str, Any]
    priority: FeedbackPriority = FeedbackPriority.NORMAL
    timestamp: float = field(default_factory=time.time)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "signal_id": self.signal_id,
            "feedback_type": self.feedback_type.name,
            "source_module": self.source_module,
            "target_modules": self.target_modules,
            "data": self.data,
            "priority": self.priority.name,
            "timestamp": self.timestamp,
            "context": self.context
        }

@dataclass
class ExecutionResult:
    """执行结果"""
    execution_id: str
    module_name: str
    success: bool
    output: Any
    metrics: Dict[str, float]
    duration_ms: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CrossModuleInsight:
    """跨模块洞察"""
    insight_id: str
    insight_type: str
    description: str
    source_modules: List[str]
    confidence: float
    impact_score: float
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "insight_id": self.insight_id,
            "insight_type": self.insight_type,
            "description": self.description,
            "source_modules": self.source_modules,
            "confidence": self.confidence,
            "impact_score": self.impact_score,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp
        }

class FeedbackCollector:
    """反馈采集器 - 从各模块采集执行结果"""
    
    def __init__(self) -> None:
        self.execution_history: List[ExecutionResult] = []
        self.module_stats: Dict[str, Dict] = defaultdict(lambda: {
            "total_executions": 0,
            "success_count": 0,
            "failure_count": 0,
            "avg_duration_ms": 0.0,
            "last_execution": None
        })
        self._collectors: Dict[str, Callable] = {}
        self._lock = asyncio.Lock()
    
    def register_collector(self, module_name: str, collector: Callable):
        """注册模块采集器"""
        self._collectors[module_name] = collector
    
    async def collect_execution_result(self, result: ExecutionResult):
        """采集执行结果"""
        async with self._lock:
            self.execution_history.append(result)
            
            # 更新模块统计
            stats = self.module_stats[result.module_name]
            stats["total_executions"] += 1
            if result.success:
                stats["success_count"] += 1
            else:
                stats["failure_count"] += 1
            
            # 更新平均耗时
            total = stats["total_executions"]
            stats["avg_duration_ms"] = (
                (stats["avg_duration_ms"] * (total - 1) + result.duration_ms) / total
            )
            stats["last_execution"] = result.timestamp
    
    async def collect_from_all_modules(self) -> List[ExecutionResult]:
        """从所有注册模块采集"""
        results = []
        for module_name, collector in self._collectors.items():
            try:
                if asyncio.iscoroutinefunction(collector):
                    result = await collector()
                else:
                    result = collector()
                if result:
                    await self.collect_execution_result(result)
                    results.append(result)
            except Exception as e:
                logger.warning(f"[FeedbackCollector] 采集 {module_name} 失败: {e}")
        return results
    
    def get_module_performance(self, module_name: str) -> Dict:
        """获取模块性能统计"""
        stats = self.module_stats[module_name].copy()
        if stats["total_executions"] > 0:
            stats["success_rate"] = stats["success_count"] / stats["total_executions"]
        else:
            stats["success_rate"] = 0.0
        return stats
    
    def get_all_performance(self) -> Dict[str, Dict]:
        """获取所有模块性能"""
        return {
            name: self.get_module_performance(name)
            for name in self.module_stats.keys()
        }

class FeedbackProcessor:
    """反馈处理器 - 处理反馈信号并生成洞察"""
    
    def __init__(self) -> None:
        self.processors: Dict[NeuralFeedbackType, Callable] = {}
        self.insight_generators: List[Callable] = []
        self.processing_history: List[Dict] = []
    
    def register_processor(self, feedback_type: NeuralFeedbackType, processor: Callable):
        """注册反馈类型处理器"""
        self.processors[feedback_type] = processor
    
    def register_insight_generator(self, generator: Callable):
        """注册洞察生成器"""
        self.insight_generators.append(generator)
    
    async def process_feedback(self, signal: FeedbackSignal) -> Dict:
        """处理反馈信号"""
        processor = self.processors.get(signal.feedback_type)
        
        if processor:
            try:
                if asyncio.iscoroutinefunction(processor):
                    result = await processor(signal)
                else:
                    result = processor(signal)
                
                self.processing_history.append({
                    "signal_id": signal.signal_id,
                    "feedback_type": signal.feedback_type.name,
                    "processed": True,
                    "timestamp": time.time()
                })
                
                return {"status": "processed", "result": result}
            except Exception as e:
                return {"status": "error", "error": "操作失败"}
        
        return {"status": "no_processor"}
    
    async def generate_insights(self, context: Dict) -> List[CrossModuleInsight]:
        """生成跨模块洞察"""
        insights = []
        
        for generator in self.insight_generators:
            try:
                if asyncio.iscoroutinefunction(generator):
                    generated = await generator(context)
                else:
                    generated = generator(context)
                
                if generated:
                    if isinstance(generated, list):
                        insights.extend(generated)
                    else:
                        insights.append(generated)
            except Exception as e:
                logger.warning(f"[FeedbackProcessor] 洞察生成失败: {e}")
        
        return insights

class WeightAdjuster:
    """权重调整器 - 根据反馈动态调整网络权重"""
    
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.adjustment_history: List[Dict] = []
        self.min_weight = 0.1
        self.max_weight = 10.0
    
    def calculate_adjustment(
        self,
        current_weight: float,
        performance_delta: float,
        feedback_strength: float
    ) -> float:
        """计算权重调整量"""
        # 基于性能变化和反馈强度计算调整
        adjustment = self.learning_rate * performance_delta * feedback_strength
        
        # 应用边界
        new_weight = current_weight + adjustment
        new_weight = max(self.min_weight, min(self.max_weight, new_weight))
        
        return new_weight - current_weight
    
    def adjust_weights(
        self,
        weights: Dict[str, float],
        performance_metrics: Dict[str, float]
    ) -> Dict[str, float]:
        """调整权重"""
        adjusted = {}
        
        for key, current_weight in weights.items():
            performance = performance_metrics.get(key, 0.0)
            
            # 计算性能变化（相对于0.5的基准）
            performance_delta = performance - 0.5
            
            # 反馈强度基于性能绝对值
            feedback_strength = abs(performance)
            
            adjustment = self.calculate_adjustment(
                current_weight, performance_delta, feedback_strength
            )
            
            adjusted[key] = current_weight + adjustment
            
            self.adjustment_history.append({
                "key": key,
                "old_weight": current_weight,
                "new_weight": adjusted[key],
                "adjustment": adjustment,
                "performance": performance,
                "timestamp": time.time()
            })
        
        return adjusted
    
    def get_adjustment_summary(self) -> Dict:
        """获取调整摘要"""
        if not self.adjustment_history:
            return {"total_adjustments": 0}
        
        recent = self.adjustment_history[-100:]  # 最近100次
        
        return {
            "total_adjustments": len(self.adjustment_history),
            "recent_adjustments": len(recent),
            "avg_adjustment": sum(a["adjustment"] for a in recent) / len(recent),
            "max_increase": max(a["adjustment"] for a in recent),
            "max_decrease": min(a["adjustment"] for a in recent)
        }

class Phase3FeedbackLoop:
    """
    Phase 3: 反馈回路闭环主类
    
    整合反馈采集、处理、洞察生成和权重调整
    """
    
    def __init__(self) -> None:
        self.collector = FeedbackCollector()
        self.processor = FeedbackProcessor()
        self.weight_adjuster = WeightAdjuster()
        
        self.feedback_queue: asyncio.Queue = asyncio.Queue()
        self.insights_cache: List[CrossModuleInsight] = []
        self.running = False
        self._processing_task: Optional[asyncio.Task] = None
        
        # 注册默认处理器
        self._register_default_processors()
    
    def _register_default_processors(self):
        """注册默认反馈处理器"""
        self.processor.register_processor(
            NeuralFeedbackType.EXECUTION_RESULT,
            self._process_execution_result
        )
        self.processor.register_processor(
            NeuralFeedbackType.PERFORMANCE_METRIC,
            self._process_performance_metric
        )
        self.processor.register_processor(
            NeuralFeedbackType.ERROR_REPORT,
            self._process_error_report
        )
    
    async def _process_execution_result(self, signal: FeedbackSignal) -> Dict:
        """处理执行结果反馈"""
        data = signal.data
        
        # 提取性能指标
        metrics = {
            "success": 1.0 if data.get("success") else 0.0,
            "duration": data.get("duration_ms", 0) / 1000.0,  # 转为秒
            "output_quality": data.get("quality_score", 0.5)
        }
        
        return {
            "processed": True,
            "metrics": metrics,
            "source": signal.source_module
        }
    
    async def _process_performance_metric(self, signal: FeedbackSignal) -> Dict:
        """处理性能指标反馈"""
        return {
            "processed": True,
            "metrics": signal.data,
            "source": signal.source_module
        }
    
    async def _process_error_report(self, signal: FeedbackSignal) -> Dict:
        """处理错误报告"""
        return {
            "processed": True,
            "error_type": signal.data.get("error_type"),
            "severity": signal.data.get("severity"),
            "requires_attention": True
        }
    
    async def start(self):
        """启动反馈回路"""
        self.running = True
        self._processing_task = asyncio.create_task(self._feedback_loop())
        logger.info("[Phase3] 反馈回路已启动")
    
    async def stop(self):
        """停止反馈回路"""
        self.running = False
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
        logger.info("[Phase3] 反馈回路已停止")
    
    async def _feedback_loop(self):
        """反馈处理主循环"""
        while self.running:
            try:
                # 获取反馈信号
                signal = await asyncio.wait_for(
                    self.feedback_queue.get(),
                    timeout=1.0
                )
                
                # 处理反馈
                await self.processor.process_feedback(signal)
                
                # 定期生成洞察
                if len(self.processor.processing_history) % 10 == 0:
                    context = self._build_insight_context()
                    insights = await self.processor.generate_insights(context)
                    self.insights_cache.extend(insights)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.warning(f"[Phase3] 反馈处理错误: {e}")
    
    def _build_insight_context(self) -> Dict:
        """构建洞察上下文"""
        return {
            "module_performance": self.collector.get_all_performance(),
            "processing_history": self.processor.processing_history[-50:],
            "adjustment_summary": self.weight_adjuster.get_adjustment_summary(),
            "timestamp": time.time()
        }
    
    async def submit_feedback(self, signal: FeedbackSignal):
        """提交反馈信号"""
        await self.feedback_queue.put(signal)
    
    async def record_execution(
        self,
        module_name: str,
        success: bool,
        output: Any,
        duration_ms: float,
        metrics: Optional[Dict[str, float]] = None
    ):
        """记录执行结果"""
        result = ExecutionResult(
            execution_id=f"exec_{int(time.time() * 1000)}",
            module_name=module_name,
            success=success,
            output=output,
            metrics=metrics or {},
            duration_ms=duration_ms
        )
        
        await self.collector.collect_execution_result(result)
        
        # 生成反馈信号
        signal = FeedbackSignal(
            signal_id=f"fb_{int(time.time() * 1000)}",
            feedback_type=NeuralFeedbackType.EXECUTION_RESULT,
            source_module=module_name,
            target_modules=["all"],
            data={
                "success": success,
                "output": str(output)[:200],
                "duration_ms": duration_ms,
                "metrics": metrics
            }
        )
        
        await self.submit_feedback(signal)
    
    def get_insights(self, min_confidence: float = 0.0) -> List[CrossModuleInsight]:
        """获取跨模块洞察"""
        return [
            i for i in self.insights_cache
            if i.confidence >= min_confidence
        ]
    
    def get_status(self) -> Dict:
        """获取反馈回路状态"""
        return {
            "running": self.running,
            "queue_size": self.feedback_queue.qsize(),
            "total_executions": len(self.collector.execution_history),
            "total_insights": len(self.insights_cache),
            "module_performance": self.collector.get_all_performance(),
            "weight_adjustments": self.weight_adjuster.get_adjustment_summary()
        }

# 全局实例
_phase3_instance: Optional[Phase3FeedbackLoop] = None

def get_phase3_feedback_loop() -> Phase3FeedbackLoop:
    """获取Phase 3反馈回路实例"""
    global _phase3_instance
    if _phase3_instance is None:
        _phase3_instance = Phase3FeedbackLoop()
    return _phase3_instance

# 便捷函数
async def record_module_execution(
    module_name: str,
    success: bool,
    output: Any,
    duration_ms: float,
    metrics: Optional[Dict[str, float]] = None
):
    """记录模块执行结果"""
    phase3 = get_phase3_feedback_loop()
    await phase3.record_execution(module_name, success, output, duration_ms, metrics)

def get_feedback_status() -> Dict:
    """获取反馈状态"""
    return get_phase3_feedback_loop().get_status()
