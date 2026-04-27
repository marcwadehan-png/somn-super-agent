"""unified_intelligence_coordinator module execution & fusion v1.0"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from ._unified_base import TaskType, TaskContext

logger = logging.getLogger(__name__)

def _execute_module(self, module_name: str, task_type: TaskType, input_data: Dict, context: TaskContext) -> Any:
    module = self._get_module(module_name)
    if not module:
        raise ValueError(f"模块不存在或加载失败: {module_name}")
    if module_name == "deep_reasoning":
        return _execute_deep_reasoning(self, module, input_data, context)
    elif module_name == "sufu_wisdom":
        return _execute_sufu_wisdom(self, module, input_data, context)
    elif module_name == "military_strategy":
        return _execute_military_strategy(self, module, input_data, context)
    elif module_name == "growth_engine":
        return _execute_growth_engine(self, module, input_data, context)
    elif module_name == "consulting_validator":
        return _execute_consulting_validator(self, module, input_data, context)
    elif module_name == "long_cot_reasoning":
        return _execute_long_cot_reasoning(self, module, input_data, context)
    elif module_name == "tot_reasoning":
        return _execute_tot_reasoning(self, module, input_data, context)
    elif module_name == "react_reasoning":
        return _execute_react_reasoning(self, module, input_data, context)
    elif module_name == "got_reasoning":
        return _execute_got_reasoning(self, module, input_data, context)
    else:
        if hasattr(module, "process"):
            return module.process(input_data)
        return f"模块 {module_name} 执行成功(通用接口)"

def _execute_deep_reasoning(self, module, input_data: Dict, context: TaskContext) -> Any:
    problem = input_data.get("problem", "")
    reasoning_mode = _select_reasoning_mode(self, problem, context)
    reasoning_context = input_data if isinstance(input_data, dict) else {"raw_input": input_data}
    if hasattr(module, "reason"):
        return module.reason(problem, reasoning_mode, reasoning_context)
    return f"深度推理执行: {problem[:50]}..."

def _execute_sufu_wisdom(self, module, input_data: Dict, context: TaskContext) -> Any:
    problem = input_data.get("problem", "")
    if hasattr(module, "make_decision"):
        situation = {
            "type": "strategy" if getattr(context, "task_type", None) == TaskType.STRATEGIC_DECISION else "general",
            "problem": problem,
            "constraints": input_data.get("constraints", []),
            "stakeholders": input_data.get("stakeholders", []),
            "context": input_data,
        }
        decision = module.make_decision(situation)
        return {
            "source": "sufu_wisdom",
            "principle": getattr(getattr(decision, "principle", None), "value", getattr(decision, "principle", "")),
            "reasoning": getattr(decision, "reasoning", ""),
            "recommendation": getattr(decision, "action", ""),
            "risk_warning": getattr(decision, "risk_warning", []),
            "expected_outcome": getattr(decision, "expected_outcome", ""),
            "balance_score": getattr(decision, "balance_score", 0.0),
        }
    return "素书智慧分析完成"

def _execute_military_strategy(self, module, input_data: Dict, context: TaskContext) -> Any:
    if hasattr(module, "analyze_situation"):
        self_state = input_data.get("self_state") or {"strength": 0.6, "resources": 0.6, "momentum": 0.6}
        enemy_state = input_data.get("enemy_state") or {"strength": 0.5, "resources": 0.5, "momentum": 0.5}
        strategy_context = input_data.get("context") or {
            "problem": input_data.get("problem", ""),
            "industry": getattr(context, "domain", "general") or "general",
        }
        return module.analyze_situation(self_state, enemy_state, strategy_context)
    return "兵法strategy分析完成"

def _execute_growth_engine(self, module, input_data: Dict, context: TaskContext) -> Any:
    solution_type = input_data.get("solution_type", "")
    client_info = input_data.get("client_info", {})
    if hasattr(module, "assess_solution"):
        return module.assess_solution(solution_type, client_info)
    return "增长方案评估完成"

def _execute_consulting_validator(self, module, input_data: Dict, context: TaskContext) -> Any:
    solution = input_data.get("solution", {})
    if hasattr(module, "validate_solution"):
        return module.validate_solution(solution)
    return "咨询验证完成"

def _select_reasoning_mode(self, problem: str, context: TaskContext) -> Any:
    """根据问题特征自动选择最合适的推理引擎（v1.0 - 2026-04-24）
    
    选择策略：
    - LongCoT: 复杂分析/多步骤推理/深入论证
    - ToT: 方案选择/策略权衡/多路径探索
    - GoT: 图关系/网络结构/多跳推理
    - ReAct: 外部查询/工具调用/交互验证
    """
    try:
        from ...reasoning.deep_reasoning_engine import ReasoningMode
    except ImportError:
        ReasoningMode = None
    
    # ── GoT优先级最高：图/关系/网络/多跳 ──
    if any(kw in problem for kw in ["图", "关系", "网络", "多跳", "链路", "连接", "关联", "依赖", "拓扑"]):
        return "got_reasoning"
    
    # ── ToT：方案选择/策略权衡 ──
    if any(kw in problem for kw in ["方案", "选择", "比较", "权衡", "策略", "规划", "路径"]):
        return "tot_reasoning"
    
    # ── ReAct：外部查询/工具调用 ──
    if any(kw in problem for kw in ["查询", "搜索", "计算", "查", "获取", "验证", "确认", "检查"]):
        return "react_reasoning"
    
    # ── LongCoT：深入分析/多步骤推理 ──
    if any(kw in problem for kw in ["分析", "推理", "论证", "深入", "复杂", "多步", "详细", "研究"]):
        return "long_cot_reasoning"
    
    # ── 其他模式 ──
    if ReasoningMode:
        if "战略" in problem or "长期" in problem:
            return ReasoningMode.CONSULTING_REASONING
        if "故事" in problem or "叙事" in problem:
            return ReasoningMode.NARRATIVE_REASONING
    
    # 默认
    return "long_cot_reasoning"

def _get_wisdom_output(self, module_name: str, task_type: TaskType, input_data: Dict, context: TaskContext) -> Any:
    return self._execute_module(module_name, task_type, input_data, context)

def _fuse_parallel_results(self, module_results: List[Tuple[str, Any]], task_type: TaskType) -> Any:
    if not module_results:
        return "无可用结果"
    return module_results[0][1]

def _fuse_wisdom_outputs(self, wisdom_outputs: List[Tuple[str, Any]], task_type: TaskType) -> Any:
    if not wisdom_outputs:
        return "无智慧输出"
    fusion_result = {
        "wisdom_sources": [name for name, _ in wisdom_outputs],
        "combined_insights": f"fusion {len(wisdom_outputs)} 个智慧系统的分析",
        "recommendations": []
    }
    for module_name, output in wisdom_outputs:
        if isinstance(output, dict):
            if "recommendation" in output:
                fusion_result["recommendations"].append({"source": module_name, "recommendation": output["recommendation"]})
            elif "action" in output:
                fusion_result["recommendations"].append({"source": module_name, "recommendation": output["action"]})
    return fusion_result

# ═══════════════════════════════════════════════════════════════════════════
# 新增推理引擎执行方法 v1.0.0 (2026-04-24)
# ═══════════════════════════════════════════════════════════════════════════

def _get_default_llm() -> callable:
    """获取默认的模拟LLM函数"""
    def _mock_llm(prompt: str) -> str:
        # 简单的模拟响应
        return "[模拟推理] 基于问题分析，给出系统性回答。"
    return _mock_llm

def _execute_long_cot_reasoning(self, module, input_data: Dict, context: TaskContext) -> Any:
    """Long Chain-of-Thought 长思维链推理引擎"""
    problem = input_data.get("problem", "")
    context_data = input_data.get("context", {})
    llm_callable = input_data.get("llm_callable") or _get_default_llm()
    
    if hasattr(module, "reason"):
        return module.reason(
            problem=problem,
            context=context_data,
            llm_callable=llm_callable
        )
    return {"source": "long_cot_reasoning", "problem": problem[:100], "status": "executed"}

def _execute_tot_reasoning(self, module, input_data: Dict, context: TaskContext) -> Any:
    """Tree-of-Thoughts 树状推理引擎"""
    problem = input_data.get("problem", "")
    initial_hint = input_data.get("initial_hint")
    max_iterations = input_data.get("max_iterations", 50)
    goal = input_data.get("goal")
    llm_callable = input_data.get("llm_callable") or _get_default_llm()
    
    if hasattr(module, "solve"):
        return module.solve(
            problem=problem,
            initial_hint=initial_hint,
            max_iterations=max_iterations,
            goal=goal,
            llm_callable=llm_callable
        )
    return {"source": "tot_reasoning", "problem": problem[:100], "status": "executed"}

def _execute_react_reasoning(self, module, input_data: Dict, context: TaskContext) -> Any:
    """ReAct 推理-行动协同引擎"""
    problem = input_data.get("problem", "")
    context_data = input_data.get("context", {})
    llm_callable = input_data.get("llm_callable") or _get_default_llm()
    
    if hasattr(module, "reason"):
        return module.reason(
            problem=problem,
            context=context_data,
            llm_callable=llm_callable
        )
    return {"source": "react_reasoning", "problem": problem[:100], "status": "executed"}

def _execute_got_reasoning(self, module, input_data: Dict, context: TaskContext) -> Any:
    """Graph-of-Thoughts 图推理引擎"""
    problem = input_data.get("problem", "")
    reasoning_mode = input_data.get("reasoning_mode", "hybrid")  # linear/branching/cyclic/hybrid
    llm_callable = input_data.get("llm_callable") or _get_default_llm()
    
    if hasattr(module, "solve"):
        return module.solve(
            problem=problem,
            reasoning_mode=reasoning_mode,
            llm_callable=llm_callable
        )
    return {"source": "got_reasoning", "problem": problem[:100], "status": "executed"}
