"""
__all__ = [
    'create_capability_engine_mapping',
    'execute_learning',
    'execute_with_timeout',
    'learn_with_core',
    'learn_with_meta',
    'learn_with_narrative',
    'learn_with_neural',
    'learn_with_smart',
    'learn_with_unified',
]

超级学习引擎 - 路由和执行模块
"""

import time
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FutureTimeoutError

from ._sle_types import LearningRequest, LearningResult, LearningCapability
from ._sle_engines import create_capability_engine_map
from . import _sle_narrative as narrative_module

def create_capability_engine_mapping():
    """创建能力到首选引擎的映射"""
    cap_map = create_capability_engine_map()
    return {
        capability: engines[0]
        for capability, engines in cap_map.items()
        if engines
    }

def execute_with_timeout(engine_self, request: LearningRequest, engine_name: str, timeout: Optional[float]):
    """带超时控制地执行学习任务"""
    if timeout is None or timeout <= 0:
        return execute_learning(engine_self, request, engine_name)
    
    with ThreadPoolExecutor(max_workers=1) as timeout_executor:
        future = timeout_executor.submit(execute_learning, engine_self, request, engine_name)
        try:
            return future.result(timeout=timeout)
        except FutureTimeoutError as exc:
            future.cancel()
            raise TimeoutError(f"学习执行超时({timeout}s)") from exc

def execute_learning(engine_self, request: LearningRequest, engine_name: str) -> LearningResult:
    """执行学习任务"""
    # 根据引擎类型调用相应方法
    if engine_name == "unified":
        return learn_with_unified(engine_self, request)
    elif engine_name == "neural":
        return learn_with_neural(engine_self, request)
    elif engine_name == "smart":
        return learn_with_smart(engine_self, request)
    elif engine_name == "core":
        return learn_with_core(engine_self, request)
    elif engine_name == "super":
        return learn_with_meta(engine_self, request)
    elif engine_name == "narrative":
        return learn_with_narrative(engine_self, request)
    else:
        raise ValueError(f"未知的引擎: {engine_name}")

def learn_with_unified(engine_self, request: LearningRequest) -> LearningResult:
    """使用unified学习系统学习"""
    engine = engine_self.engines["unified"]
    
    if request.capability == LearningCapability.LOCAL_DATA_LEARNING:
        success = engine.start_learning()
        return LearningResult(
            request_id=request.request_id,
            capability=request.capability,
            success=success,
            data={
                "files_processed": engine.config.max_files_per_batch,
                "learning_mode": "batch"
            },
            engine_used="unified",
            confidence=0.85 if success else 0.0,
            next_actions=["继续学习下一个批次", "检查学习质量"] if success else ["检查错误原因"]
        )
    
    elif request.capability in [LearningCapability.TRANSFER_LEARNING, 
                               LearningCapability.CONTINUOUS_LEARNING]:
        result = engine.generate_learning_report()
        return LearningResult(
            request_id=request.request_id,
            capability=request.capability,
            success=True,
            data=result,
            engine_used="unified",
            confidence=0.80,
            next_actions=["分析学习报告", "优化学习strategy"]
        )
    
    else:
        return LearningResult(
            request_id=request.request_id,
            capability=request.capability,
            success=True,
            data={"message": "unified学习系统已处理"},
            engine_used="unified",
            confidence=0.75
        )

def learn_with_neural(engine_self, request: LearningRequest) -> LearningResult:
    """使用神经记忆学习引擎学习"""
    from src.neural_memory.learning_engine import LearningType as NeuralLearningType
    
    engine = engine_self.engines["neural"]
    
    learning_type_map = {
        LearningCapability.INSTANCE_LEARNING: NeuralLearningType.INSTANCE,
        LearningCapability.VALIDATION_LEARNING: NeuralLearningType.VALIDATION,
        LearningCapability.ERROR_LEARNING: NeuralLearningType.ERROR,
        LearningCapability.ASSOCIATION_LEARNING: NeuralLearningType.ASSOCIATION,
        LearningCapability.REINFORCEMENT_LEARNING: NeuralLearningType.REINFORCEMENT,
    }
    
    neural_type = learning_type_map.get(request.capability, NeuralLearningType.INSTANCE)
    
    engine.learn(
        learning_type=neural_type,
        data=request.input_data,
        context=request.context
    )
    
    return LearningResult(
        request_id=request.request_id,
        capability=request.capability,
        success=True,
        data={
            "learning_type": neural_type.value,
            "memory_updated": True
        },
        engine_used="neural",
        confidence=0.90,
        next_actions=["验证学习效果", "强化相关知识"]
    )

def learn_with_smart(engine_self, request: LearningRequest) -> LearningResult:
    """使用智能学习引擎学习"""
    engine = engine_self.engines["smart"]
    result = engine.learn(request.input_data, request.context)
    
    return LearningResult(
        request_id=request.request_id,
        capability=request.capability,
        success=True,
        data=result,
        engine_used="smart",
        confidence=0.85,
        next_actions=["分析学习结果", "优化学习参数"]
    )

def learn_with_core(engine_self, request: LearningRequest) -> LearningResult:
    """使用核心学习引擎学习"""
    engine = engine_self.engines["core"]
    result = engine.learn(request.input_data)
    
    return LearningResult(
        request_id=request.request_id,
        capability=request.capability,
        success=True,
        data=result,
        engine_used="core",
        confidence=0.80
    )

def learn_with_meta(engine_self, request: LearningRequest) -> LearningResult:
    """元学习 - 基于学习历史与统计信息优化后续学习strategy"""
    input_data = request.input_data or {}
    history_limit = input_data.get("history_limit", 10)
    history = engine_self.get_learning_history(limit=history_limit)
    stats = engine_self.get_stats()
    target_capability = input_data.get("target_capability")
    
    capability_summary: Dict[str, int] = {}
    for item in history:
        capability_name = item.capability.value
        capability_summary[capability_name] = capability_summary.get(capability_name, 0) + 1
    
    recommendations = []
    if stats["success_rate"] < 0.8:
        recommendations.append("优先排查低成功率学习链路,再扩大样本量")
    if stats["avg_execution_time"] > 60.0:
        recommendations.append("平均执行时间偏长,建议缩小批次或增加并行资源")
    if target_capability and capability_summary.get(target_capability, 0) == 0:
        recommendations.append(f"目标能力 {target_capability} 缺少历史样本,建议先补采案例")
    if not recommendations:
        recommendations.append("当前学习strategy稳定,可继续沿用并增加高质量反馈闭环")
    
    return LearningResult(
        request_id=request.request_id,
        capability=request.capability,
        success=True,
        data={
            "target_capability": target_capability,
            "history_sample_size": len(history),
            "capability_summary": capability_summary,
            "current_stats": stats,
            "recommendations": recommendations,
        },
        engine_used="super",
        confidence=0.88,
        next_actions=recommendations
    )

def learn_with_narrative(engine_self, request: LearningRequest) -> LearningResult:
    """叙事学习引擎"""
    input_data = request.input_data or {}
    
    learning_content = input_data.get("content", input_data.get("text", ""))
    learning_source = input_data.get("source", "unknown")
    learning_type = input_data.get("narrative_type", "general")
    
    narrative_insights = {
        "narrative_structure": narrative_module.analyze_narrative_structure(learning_content, learning_type),
        "emotional_patterns": narrative_module.extract_emotional_patterns(learning_content),
        "perspective_diversity": narrative_module.evaluate_perspective_diversity(learning_content),
        "temporal_dynamics": narrative_module.analyze_temporal_dynamics(learning_content),
    }
    
    structure_score = narrative_insights["narrative_structure"].get("coherence", 0.7)
    emotional_score = narrative_insights["emotional_patterns"].get("resonance_potential", 0.7)
    perspective_score = narrative_insights["perspective_diversity"].get("coverage", 0.7)
    
    overall_confidence = (structure_score + emotional_score + perspective_score) / 3
    
    return LearningResult(
        request_id=request.request_id,
        capability=request.capability,
        success=True,
        data={
            "narrative_insights": narrative_insights,
            "learning_source": learning_source,
            "narrative_type": learning_type,
            "knowledge_extracted": {
                "structures": narrative_insights["narrative_structure"].get("patterns", []),
                "emotions": narrative_insights["emotional_patterns"].get("key_emotions", []),
                "perspectives": narrative_insights["perspective_diversity"].get("perspectives", []),
                "temporal_phases": narrative_insights["temporal_dynamics"].get("phases", [])
            }
        },
        engine_used="narrative",
        confidence=overall_confidence,
        next_actions=[
            "将叙事知识应用到品牌strategy中",
            "分析更多品牌案例的叙事模式",
            "构建行业专属的叙事知识库"
        ]
    )
