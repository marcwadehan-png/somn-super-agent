"""unified_intelligence_coordinator execution methods v1.0"""
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from ._unified_base import TaskType, TaskPriority, TaskContext, TaskResult

__all__ = [
    'execute_task',
]

logger = logging.getLogger(__name__)

def execute_task(self, task_type: TaskType, input_data: Dict[str, Any], context: Optional[TaskContext] = None) -> TaskResult:
    start_time = time.time()
    if not context:
        task_id = f"task_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}"
        context = TaskContext(
            task_id=task_id, task_type=task_type, priority=TaskPriority.MEDIUM,
            user_id="system", session_id="session_001", input_data=input_data
        )
    logger.info(f"开始执行任务: {context.task_id} - {task_type.value}")
    try:
        strategy = self._select_coordination_strategy(task_type, context)
        result = strategy(task_type, input_data, context)
        execution_time = time.time() - start_time
        result.execution_time = execution_time
        self._update_performance_metrics(context.task_id, result.success, execution_time)
        self.task_history.append({
            "task_id": context.task_id, "task_type": task_type.value,
            "success": result.success, "execution_time": execution_time,
            "modules_used": result.modules_used,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        logger.info(f"任务完成: {context.task_id} - 成功: {result.success} - 耗时: {execution_time:.2f}s")
        return result
    except Exception as e:
        logger.error(f"任务执行失败: {context.task_id} - {str(e)}")
        return TaskResult(
            task_id=context.task_id, success=False,
            primary_output="任务执行失败",
            warnings=["执行异常"]
        )

def _select_coordination_strategy(self, task_type: TaskType, context: TaskContext) -> callable:
    if task_type == TaskType.STRATEGIC_DECISION:
        return self.coordination_strategies["ensemble"]
    elif task_type == TaskType.TACTICAL_EXECUTION:
        return self.coordination_strategies["parallel"]
    elif task_type == TaskType.PROBLEM_SOLVING:
        complexity = self._assess_problem_complexity(context.input_data)
        return self.coordination_strategies["adaptive"] if complexity > 0.7 else self.coordination_strategies["sequential"]
    elif context.priority == TaskPriority.CRITICAL:
        return self.coordination_strategies["adaptive"]
    elif task_type == TaskType.TIER3_ANALYSIS:
        return self._execute_tier3
    else:
        return self.coordination_strategies["sequential"]

def _execute_sequential(self, task_type: TaskType, input_data: Dict, context: TaskContext) -> TaskResult:
    best_module = self._select_best_module(task_type, context)
    if not best_module:
        return TaskResult(task_id=context.task_id, success=False, primary_output="未找到合适的处理模块", warnings=["无可用模块"])
    module_result = self._execute_module(best_module, task_type, input_data, context)
    return TaskResult(task_id=context.task_id, success=True, primary_output=module_result, modules_used=[best_module])

def _execute_parallel(self, task_type: TaskType, input_data: Dict, context: TaskContext) -> TaskResult:
    suitable_modules = self._select_suitable_modules(task_type, context, max_modules=3)
    if not suitable_modules:
        return TaskResult(task_id=context.task_id, success=False, primary_output="未找到合适的处理模块", warnings=["无可用模块"])
    module_results = []
    for module_name in suitable_modules:
        result = self._execute_module(module_name, task_type, input_data, context)
        module_results.append((module_name, result))
    fused_result = self._fuse_parallel_results(module_results, task_type)
    return TaskResult(
        task_id=context.task_id, success=True, primary_output=fused_result, modules_used=suitable_modules,
        reasoning_trace=[{"module": name, "result": str(result)[:100]} for name, result in module_results]
    )

def _execute_ensemble(self, task_type: TaskType, input_data: Dict, context: TaskContext) -> TaskResult:
    try:
        from ..super_wisdom_coordinator import get_super_wisdom_coordinator
        coordinator = get_super_wisdom_coordinator()
        query_text = input_data.get("problem", "") or input_data.get("query", "")
        if query_text and coordinator:
            result = coordinator.coordinate(query_text, context.__dict__ if hasattr(context, '__dict__') else {})
            return TaskResult(
                task_id=context.task_id, success=True, primary_output=result,
                modules_used=["super_wisdom_coordinator"],
                reasoning_trace=[{"coordinator": "super_wisdom_coordinator"}]
            )
    except ImportError:
        logger.debug("超级协调器未安装,使用直接fusion模式")
    except Exception as e:
        logger.warning(f"超级协调器执行失败: {e},回退到直接fusion模式")
    return self._execute_ensemble_direct(task_type, input_data, context)

def _execute_ensemble_direct(self, task_type: TaskType, input_data: Dict, context: TaskContext) -> TaskResult:
    wisdom_modules = [
        "sufu_wisdom", "military_strategy", "hongming_wisdom",
        "ancient_wisdom_fusion", "cross_wisdom_analyzer", "metaphysics_wisdom",
        "mythology_wisdom", "literary_narrative", "anthropology_wisdom",
        "behavior_shaping", "science_thinking", "natural_science",
        "sanjiao_fusion", "psychology_pioneer_fusion", "dao_wisdom",
        "tang_song_poetry_fusion", "buddha_wisdom",
    ]
    available_modules = [m for m in wisdom_modules if self._ensure_module(m)]
    if not available_modules:
        return self._execute_sequential(task_type, input_data, context)
    wisdom_outputs = []
    for module_name in available_modules:
        try:
            output = self._get_wisdom_output(module_name, task_type, input_data, context)
            wisdom_outputs.append((module_name, output))
        except Exception as e:
            logger.warning(f"智慧模块 {module_name} 执行失败: {e}")
    if not wisdom_outputs:
        return TaskResult(task_id=context.task_id, success=False, primary_output="所有智慧模块执行失败", warnings=["智慧系统不可用"])
    fused_wisdom = self._fuse_wisdom_outputs(wisdom_outputs, task_type)
    if self._ensure_module("deep_reasoning"):
        final_result = self._execute_module("deep_reasoning", task_type, {
            "problem": input_data.get("problem", ""),
            "wisdom_inputs": wisdom_outputs, "fused_wisdom": fused_wisdom
        }, context)
    else:
        final_result = fused_wisdom
    return TaskResult(
        task_id=context.task_id, success=True, primary_output=final_result,
        modules_used=available_modules + (["deep_reasoning"] if self._ensure_module("deep_reasoning") else []),
        reasoning_trace=[{"module": name, "output": str(output)[:100]} for name, output in wisdom_outputs]
    )

def _execute_adaptive(self, task_type: TaskType, input_data: Dict, context: TaskContext) -> TaskResult:
    historical_performance = self._analyze_historical_performance(task_type)
    if historical_performance.get("ensemble", {}).get("success_rate", 0) > 0.8:
        return self._execute_ensemble(task_type, input_data, context)
    elif historical_performance.get("parallel", {}).get("avg_time", 10) < 5.0:
        return self._execute_parallel(task_type, input_data, context)
    else:
        return self._execute_sequential(task_type, input_data, context)

def _execute_tier3(self, task_type: TaskType, input_data: Dict, context: TaskContext) -> TaskResult:
    try:
        from ...scheduler.global_wisdom_scheduler import tier3_wisdom_analyze
        query_text = input_data.get("problem", "") or input_data.get("query", "")
        if not query_text:
            return TaskResult(task_id=context.task_id, success=False, primary_output="查询文本为空", warnings=["无法执行三级分析"])
        tier3_result = tier3_wisdom_analyze(
            query_text=query_text, context=context.__dict__,
            p1_count=input_data.get("p1_count", 6), p3_count=input_data.get("p3_count", 4),
            p2_count=input_data.get("p2_count", 4), random_seed=input_data.get("random_seed")
        )
        return TaskResult(
            task_id=context.task_id, success=tier3_result.success,
            primary_output={
                "final_strategy": tier3_result.final_strategy,
                "decision_confidence": tier3_result.decision_confidence,
                "key_insights": tier3_result.key_insights,
                "p1_strategies": [o.strategy_content for o in tier3_result.p1_outputs if o.strategy_content],
                "p3_arguments": [getattr(o, '论证_content', '') for o in tier3_result.p3_outputs if getattr(o, '论证_content', '')],
                "p2_perspectives": [o.perspective_content for o in tier3_result.p2_outputs if o.perspective_content],
                "processing_time": tier3_result.processing_time,
            },
            modules_used=[o.engine_id for o in tier3_result.p1_outputs] + [o.engine_id for o in tier3_result.p3_outputs] + [o.engine_id for o in tier3_result.p2_outputs],
            confidence=tier3_result.decision_confidence,
            warnings=tier3_result.risk_warnings
        )
    except ImportError as e:
        logger.warning(f"三级调度器未安装: {e}")
        return TaskResult(task_id=context.task_id, success=False, primary_output="三级调度器不可用", warnings=["tier3_neural_scheduler 未安装"])
    except Exception as e:
        logger.error(f"三级分析执行失败: {e}")
        return TaskResult(task_id=context.task_id, success=False, primary_output="三级分析失败", warnings=["执行异常"])

def _select_best_module(self, task_type: TaskType, context: TaskContext) -> Optional[str]:
    suitable_modules = []
    for module_name, mapping in self.module_mapping.items():
        if not self._ensure_module(module_name):
            continue
        if task_type.value in mapping["capabilities"]:
            if context.domain in mapping["domains"] or "general" in mapping["domains"]:
                capability_score = self.module_profiles[module_name].capabilities.get(task_type.value, 0.5)
                reliability = self.module_profiles[module_name].reliability_score
                total_score = capability_score * 0.7 + reliability * 0.3
                suitable_modules.append((module_name, total_score))
    if not suitable_modules:
        return None
    suitable_modules.sort(key=lambda x: x[1], reverse=True)
    return suitable_modules[0][0]

def _select_suitable_modules(self, task_type: TaskType, context: TaskContext, max_modules: int = 3) -> List[str]:
    suitable_modules = []
    for module_name, mapping in self.module_mapping.items():
        if not self._ensure_module(module_name):
            continue
        if task_type.value in mapping["capabilities"]:
            if context.domain in mapping["domains"] or "general" in mapping["domains"]:
                capability_score = self.module_profiles[module_name].capabilities.get(task_type.value, 0.5)
                suitable_modules.append((module_name, capability_score))
    suitable_modules.sort(key=lambda x: x[1], reverse=True)
    return [mod[0] for mod in suitable_modules[:max_modules]]
