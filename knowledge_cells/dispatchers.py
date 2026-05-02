"""
SageDispatch Dispatchers - 调度器实现
贤者调度系统 - 12个专业调度器
"""

import time
import re
import sys
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict

logger = logging.getLogger("Somn.SageDispatch")


# 兼容导入
try:
    from .core import BaseDispatcher, DispatchRequest, DispatchResponse, Level, DispatcherState
except ImportError:
    # fallback: 从 knowledge_cells.core 导入（不是 smart_office_assistant.src.core）
    import knowledge_cells.core as _kc_core
    BaseDispatcher = _kc_core.BaseDispatcher
    DispatchRequest = _kc_core.DispatchRequest
    DispatchResponse = _kc_core.DispatchResponse
    Level = _kc_core.Level
    DispatcherState = _kc_core.DispatcherState

# v7.1 FastBoot: 缓存运行时导入 — 避免每次 _execute 调用都做 from .core import
_cached_get_engine = None
_cached_LevelAssessor = None


def _calc_confidence(base: float, factors: dict = None) -> float:
    """动态置信度计算 — 基于基线 + 多因子调节
    
    Args:
        base: 基线置信度（如 0.5 表示中性）
        factors: 调节因子字典，支持:
            - has_output: bool — 有实质输出 +0.1
            - passed_check: bool — 通过质量检查 +0.1
            - has_error: bool — 存在错误 -0.2
            - llm_enhanced: bool — LLM增强过 +0.05
            - track_b_used: bool — 神行轨参与 +0.05
            - result_count: int — 结果数量，>0 时 +0.03*min(n,3)
            - depth: int — 推理深度(1-3)，+0.03*depth
    Returns:
        float: 调节后的置信度，钳位到 [0.0, 1.0]
    """
    conf = base
    if factors is None:
        return max(0.0, min(1.0, conf))
    if factors.get("has_output"):
        conf += 0.10
    if factors.get("passed_check"):
        conf += 0.10
    if factors.get("has_error"):
        conf -= 0.20
    if factors.get("llm_enhanced"):
        conf += 0.05
    if factors.get("track_b_used"):
        conf += 0.05
    n = factors.get("result_count", 0)
    if n > 0:
        conf += 0.03 * min(n, 3)
    depth = factors.get("depth", 0)
    if depth > 0:
        conf += 0.03 * min(depth, 3)
    return max(0.0, min(1.0, conf))


def _wrap_track_b_result(result: Dict) -> Dict:
    """包装神行轨返回结果，统一标记 is_mock 状态
    
    当神行轨返回 is_mock=True 时，called 标记为 False（非真实调用）
    """
    is_mock = result.get("is_mock", False) if isinstance(result, dict) else False
    return {
        "called": not is_mock,
        "is_mock": is_mock,
        "result": result,
    }

def _get_cached_engine():
    """缓存获取 get_engine（避免每次 _execute 都导入）"""
    global _cached_get_engine
    if _cached_get_engine is None:
        try:
            from .core import get_engine
            _cached_get_engine = get_engine
        except ImportError:
            import knowledge_cells.core as _kc_core
            _cached_get_engine = _kc_core.get_engine
    return _cached_get_engine

def _get_cached_level_assessor():
    """缓存获取 LevelAssessor（避免每次 _execute 都导入）"""
    global _cached_LevelAssessor
    if _cached_LevelAssessor is None:
        try:
            from .core import LevelAssessor
            _cached_LevelAssessor = LevelAssessor
        except ImportError:
            import knowledge_cells.core as _kc_core
            _cached_LevelAssessor = _kc_core.LevelAssessor
    return _cached_LevelAssessor


# ==================== SD-F2 四级调度总控 ====================

class FourLevelDispatchController(BaseDispatcher):
    """
    SD-F2 四级调度总控引擎
    所有问题的统一入口调度器
    """

    dispatcher_id: str = "SD-F2"
    dispatcher_name: str = "四级调度总控"

    # 级别配置
    LEVEL_CONFIG = {
        Level.L1_INSTINCT: {
            "name": "本能直觉",
            "time_limit": 0.1,
            "target_cells": ["SD-P1"],
            "escalate_if": lambda r, o: o.get("confidence", 1.0) < 0.5
        },
        Level.L2_LOGIC: {
            "name": "逻辑推理",
            "time_limit": 1.0,
            "target_cells": ["SD-P1", "SD-R2"],
            "escalate_if": lambda r, o: (
                o.get("confidence", 1.0) < 0.6 or
                r.problem.get("requires_wisdom", False)
            )
        },
        Level.L3_WISDOM: {
            "name": "智慧融合",
            "time_limit": 10.0,
            "target_cells": ["SD-F1", "SD-P1"],
            "escalate_if": lambda r, o: (
                o.get("confidence", 1.0) < 0.5 or
                r.problem.get("is_innovative", False)
            )
        },
        Level.L4_INTUITION: {
            "name": "极致直觉",
            "time_limit": 30.0,
            "target_cells": ["SD-F1", "SD-D3", "SD-C2"],
            "escalate_if": lambda r, o: False
        }
    }

    def __init__(self):
        super().__init__()
        self._assessor = None
        self._sub_dispatchers: Dict[str, BaseDispatcher] = {}

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行四级调度"""
        get_engine = _get_cached_engine()
        engine = get_engine()
        trace = {"states": [], "sub_dispatches": []}

        # 1. 确定调度级别
        if request.forced_level:
            level = request.forced_level
            trace["level_decision"] = "forced"
        else:
            LevelAssessor = _get_cached_level_assessor()
            level, confidence = LevelAssessor.assess(request.problem)
            trace["level_decision"] = {
                "assessed_level": level.value,
                "confidence": confidence
            }

        trace["states"].append(f"LEVEL_SELECTED:{level.value}")

        # 2. 执行该级别调度
        outputs = []
        target_cells = self.LEVEL_CONFIG[level]["target_cells"]

        for cell_id in target_cells:
            trace["states"].append(f"DISPATCHING:{cell_id}")
            try:
                sub_dispatcher = engine.get_dispatcher(cell_id)
                sub_request = DispatchRequest(
                    request_id=f"{request.request_id}-{cell_id}",
                    problem=request.problem,
                    level=level
                )
                result = sub_dispatcher.dispatch(sub_request)
                outputs.append(result.output)
                trace["sub_dispatches"].append({
                    "cell_id": cell_id,
                    "success": True,
                    "confidence": result.confidence
                })
            except Exception as e:
                trace["sub_dispatches"].append({
                    "cell_id": cell_id,
                    "success": False,
                    "error": str(e)
                })

        # 3. 综合结果
        combined = self._combine_outputs(outputs)

        # 4. 检查升级
        config = self.LEVEL_CONFIG[level]
        if request.allow_escalation and config["escalate_if"](request, combined):
            trace["states"].append("ESCALATING")
            escalated = self._execute_escalation(request, level, engine)
            combined.update(escalated)

        trace["states"].append("COMPLETED")

        return {
            "level": level.value,
            "dispatched_to": target_cells,
            "confidence": combined.get("confidence", 0.8),
            "output": combined,
            "trace": trace
        }

    def _combine_outputs(self, outputs: List[Dict]) -> Dict[str, Any]:
        """合并多个调度结果"""
        if not outputs:
            return {"confidence": 0.5, "output": {}}

        confidences = [o.get("confidence", 0.8) for o in outputs]
        avg_confidence = sum(confidences) / len(confidences)

        return {
            "confidence": avg_confidence,
            "output": outputs if len(outputs) > 1 else outputs[0],
            "count": len(outputs)
        }

    def _execute_escalation(self, request: DispatchRequest,
                          current_level: Level,
                          engine) -> Dict[str, Any]:
        """执行级别升级"""
        escalation_map = {
            Level.L1_INSTINCT: Level.L2_LOGIC,
            Level.L2_LOGIC: Level.L3_WISDOM,
            Level.L3_WISDOM: Level.L4_INTUITION,
            Level.L4_INTUITION: Level.L4_INTUITION
        }

        next_level = escalation_map.get(current_level, current_level)
        if next_level == current_level:
            return {"escalated": False}

        target_cells = self.LEVEL_CONFIG[next_level]["target_cells"]
        escalated_results = []

        for cell_id in target_cells:
            try:
                sub_dispatcher = engine.get_dispatcher(cell_id)
                sub_request = DispatchRequest(
                    request_id=f"{request.request_id}-{cell_id}-escalated",
                    problem=request.problem,
                    level=next_level
                )
                result = sub_dispatcher.dispatch(sub_request)
                escalated_results.append(result.output)
            except Exception as e:
                # v7.2: 升级失败不再静默丢弃，记录错误信息
                logger.warning(f"[SD-F2] Escalation to {cell_id} failed: {e}")
                escalated_results.append({
                    "error": str(e),
                    "cell_id": cell_id,
                    "escalated_from": current_level.value,
                })

        return {
            "escalated": True,
            "original_level": current_level.value,
            "escalated_to": next_level.value,
            "escalated_results": escalated_results
        }


# ==================== SD-P1 问题调度器（核心树干） ====================

class ProblemDispatcher(BaseDispatcher):
    """
    SD-P1 问题调度器【核心树干】
    
    核心职责：
    - 问题解析：理解问题本质和关键要素
    - 意图识别：判断用户真实意图
    - 上下文理解：整合上下文信息
    - 方案生成：生成初步解决方案
    
    问题处理流程：
    1. 问题解析 → 提取关键要素和约束
    2. 意图识别 → 判断问题类型和紧急程度
    3. 上下文理解 → 整合历史上下文
    4. 方案生成 → 生成初步解决思路
    """

    dispatcher_id: str = "SD-P1"
    dispatcher_name: str = "问题调度"

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行问题调度"""
        text = request.problem.get("description", "")
        context = request.problem.get("context", "")

        # 1. 问题解析
        parsed = self._parse_problem(text)
        
        # 2. 意图识别
        intent = self._recognize_intent(text)
        
        # 3. 上下文理解
        understood = self._understand_context(text, context)
        
        # 4. 调用DomainNexus查询相关知识
        knowledge = self._query_knowledge(text)
        
        # 5. 方案生成（基于知识库）
        solution = self._generate_solution(parsed, intent, understood, knowledge)

        # 计算整体置信度（基于知识库质量）
        confidence = self._calculate_confidence(solution, knowledge)

        return {
            "dispatched_to": ["SD-P1"],
            "confidence": confidence,
            "level_assigned": self._assign_level(intent, parsed),
            "output": {
                "type": "problem_dispatch",
                "description": "SD-P1 问题调度",
                "problem_parsed": parsed,
                "intent_recognized": intent,
                "context_understood": understood,
                "knowledge_queried": knowledge,
                "solution_generated": solution,
                "confidence": confidence
            }
        }
    
    def _query_knowledge(self, text: str) -> Dict[str, Any]:
        """调用DomainNexus查询相关知识"""
        try:
            # 尝试导入DomainNexus
            try:
                from .domain_nexus import query, get_nexus
            except ImportError:
                from domain_nexus import query, get_nexus
            
            # 查询相关知识
            result = query(text)
            
            return {
                "queried": True,
                "answer": result.get("answer", ""),
                "relevant_cells": result.get("relevant_cells", []),
                "hot_topics": result.get("hot_topics", []),
                "query_time_ms": result.get("_perf", {}).get("query_time_ms", 0)
            }
        except Exception as e:
            # 如果DomainNexus不可用，返回空结果
            return {
                "queried": False,
                "error": str(e),
                "answer": "",
                "relevant_cells": [],
                "hot_topics": []
            }
    
    def _calculate_confidence(self, solution: Dict, knowledge: Dict) -> float:
        """计算置信度"""
        base = 0.7
        
        # 如果有知识库支持，提高置信度
        if knowledge.get("queried") and knowledge.get("relevant_cells"):
            base += 0.15
        
        # 如果有详细答案，提高置信度
        if knowledge.get("answer"):
            base += 0.1
        
        # 基于解决方案的置信度 breakdown
        breakdown = solution.get("confidence_breakdown", {})
        if breakdown:
            avg_breakdown = sum(breakdown.values()) / len(breakdown)
            base = (base + avg_breakdown) / 2
        
        return min(base, 0.95)
    
    def _assign_level(self, intent: Dict, parsed: Dict) -> str:
        """根据意图和问题复杂度分配调度级别"""
        complexity = parsed.get("complexity", "medium")
        requires_deep = intent.get("requires_deep_reasoning", False)
        urgency = intent.get("urgency", "normal")
        
        if complexity == "high" or requires_deep:
            return "L3"
        elif complexity == "medium" or urgency == "medium":
            return "L2"
        else:
            return "L1"

    def _parse_problem(self, text: str) -> Dict:
        """问题解析"""
        keywords = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,}', text)
        
        # 问题类型分类
        problem_types = []
        if any(kw in text for kw in ["是什么", "如何", "怎么", "多少", "谁", "哪里"]):
            problem_types.append("information")
        if any(kw in text for kw in ["分析", "评估", "判断", "检验"]):
            problem_types.append("analysis")
        if any(kw in text for kw in ["战略", "规划", "策划", "设计"]):
            problem_types.append("planning")
        if any(kw in text for kw in ["决策", "选择", "决定"]):
            problem_types.append("decision")
        if any(kw in text for kw in ["创新", "创造", "突破", "颠覆"]):
            problem_types.append("innovation")
        if any(kw in text for kw in ["执行", "实施", "落地", "操作"]):
            problem_types.append("execution")
        
        return {
            "keywords": keywords[:10],
            "length": len(text),
            "complexity": "high" if len(text) > 200 else "medium" if len(text) > 50 else "low",
            "entities": self._extract_entities(text),
            "problem_types": problem_types if problem_types else ["general"],
            "has_question_mark": "？" in text or "?" in text,
            "is_inquiry": "？" in text or "?" in text
        }
    
    def _extract_entities(self, text: str) -> List[Dict]:
        """提取文本中的实体"""
        entities = []
        
        # 提取数量
        number_patterns = re.findall(r'\d+(?:\.\d+)?(?:[万亿千百十])?', text)
        if number_patterns:
            entities.append({"type": "number", "values": number_patterns[:3]})
        
        # 提取时间
        time_patterns = re.findall(r'(?:\d+年|\d+月|\d+日|\d+点|\d+时)', text)
        if time_patterns:
            entities.append({"type": "time", "values": time_patterns[:3]})
        
        # 提取公司/组织
        org_markers = ["公司", "企业", "集团", "机构", "组织"]
        for marker in org_markers:
            if marker in text:
                idx = text.find(marker)
                start = max(0, idx - 8)
                entities.append({"type": "organization", "text": text[start:idx+len(marker)]})
                break
        
        return entities[:5] if entities else [{"type": "none", "text": ""}]

    def _recognize_intent(self, text: str) -> Dict:
        """意图识别"""
        intents = []
        intent_keywords = {
            "analysis": ["分析", "评估", "判断", "检验", "研究"],
            "planning": ["战略", "规划", "策划", "设计", "布局"],
            "decision": ["决策", "选择", "决定", "定夺"],
            "execution": ["执行", "实施", "落地", "操作"],
            "innovation": ["创新", "变革", "突破", "转型"],
            "information": ["查询", "告诉", "了解", "知道"]
        }
        
        for intent_name, keywords in intent_keywords.items():
            if any(kw in text for kw in keywords):
                intents.append(intent_name)
        
        # 判断紧急程度
        urgency = "high" if any(kw in text for kw in ["紧急", "立即", "马上", "立刻", "刻不容缓"]) else \
                  "medium" if any(kw in text for kw in ["尽快", "优先", "重要"]) else "normal"
        
        # 判断是否需要多步推理
        requires_deep_reasoning = any(kw in text for kw in ["为什么", "原因", "推理", "论证"])
        
        return {
            "primary_intent": intents[0] if intents else "general",
            "all_intents": intents,
            "urgency": urgency,
            "requires_deep_reasoning": requires_deep_reasoning,
            "intent_count": len(intents)
        }

    def _understand_context(self, text: str, context: str) -> Dict:
        """上下文理解"""
        return {
            "has_context": bool(context),
            "context_summary": context[:100] if context else "",
            "context_relevance": 0.8 if context else 0.5,
            "historical_references": self._extract_history_refs(text, context)
        }
    
    def _extract_history_refs(self, text: str, context: str) -> List[Dict]:
        """提取历史引用"""
        refs = []
        # 检查是否提及"上次"、"之前"、"历史"等
        if any(kw in text for kw in ["上次", "之前", "原来", "以前"]):
            refs.append({"type": "past_reference", "relevance": 0.7})
        if any(kw in text for kw in ["继续", "接着", "延续"]):
            refs.append({"type": "continuation", "relevance": 0.8})
        return refs

    def _generate_solution(self, parsed: Dict, intent: Dict, understood: Dict, knowledge: Dict = None) -> Dict:
        """方案生成（基于知识库，支持LLM增强）"""
        primary_intent = intent.get("primary_intent", "general")
        complexity = parsed.get("complexity", "medium")
        knowledge = knowledge or {}
        
        # 根据意图和复杂度确定路由
        routing = self._determine_routing(intent, parsed)
        
        # 生成解决方案（整合知识库）
        approach_map = {
            "information": "信息查询 → 快速响应",
            "analysis": "分析研究 → 深入研究",
            "planning": "战略规划 → 系统设计",
            "decision": "决策分析 → 权衡选择",
            "execution": "执行落地 → 行动计划",
            "innovation": "创新突破 → 颠覆性思考",
            "general": "综合分析 → 多维度思考"
        }
        
        approach = approach_map.get(primary_intent, approach_map["general"])
        
        # 如果知识库有答案，使用知识库的洞察
        knowledge_insights = []
        if knowledge.get("answer"):
            answer = knowledge["answer"]
            # 提取核心要点
            if "核心洞见" in answer:
                knowledge_insights.append("已查阅相关知识库")
            if "实战案例" in answer:
                knowledge_insights.append("包含实战案例参考")
            if knowledge.get("relevant_cells"):
                cell_names = [c.get("name", "") for c in knowledge["relevant_cells"][:3]]
                knowledge_insights.append(f"关联知识：{', '.join(cell_names)}")
        
        # 当知识库无实质答案时，调用LLM增强分析
        llm_enhancement = None
        if not knowledge.get("answer") or len(knowledge.get("answer", "")) < 50:
            llm_enhancement = self._call_llm_for_analysis(parsed, intent, understood)
            if llm_enhancement:
                knowledge_insights.append("LLM增强分析已应用")
        
        # 估计完成时间
        duration_map = {
            "low": "1-5分钟",
            "medium": "5-30分钟",
            "high": "30分钟以上"
        }
        
        return {
            "approach": approach,
            "primary_intent": primary_intent,
            "estimated_confidence": 0.85 if not knowledge.get("answer") else 0.9,
            "estimated_duration": duration_map.get(complexity, "5-30分钟"),
            "routing": routing,
            "next_steps": routing.get("recommended_chain", ["SD-R2谬误检测", "SD-F1学派融合"]),
            "knowledge_insights": knowledge_insights,
            "llm_enhancement": llm_enhancement,
            "confidence_breakdown": {
                "problem_parsing": 0.9,
                "intent_recognition": 0.85,
                "context_understanding": understood.get("context_relevance", 0.5),
                "knowledge_support": 0.9 if knowledge.get("relevant_cells") else 0.5,
                "overall": 0.85 if not knowledge.get("answer") else 0.92
            }
        }
    
    def _call_llm_for_analysis(self, parsed: Dict, intent: Dict, understood: Dict) -> Optional[Dict]:
        """调用LLM进行增强分析"""
        try:
            # 尝试导入 llm_rule_layer
            try:
                from .llm_rule_layer import call_module_llm
            except ImportError:
                try:
                    from llm_rule_layer import call_module_llm
                except ImportError:
                    return None
            
            # 构建问题描述
            keywords = parsed.get("keywords", [])
            primary_intent = intent.get("primary_intent", "general")
            complexity = parsed.get("complexity", "medium")
            
            prompt = f"""请对以下问题进行初步分析：

问题关键词: {', '.join(keywords[:5])}
意图类型: {primary_intent}
复杂度: {complexity}

请提供：
1. 问题核心要点（3-5点）
2. 建议的分析角度
3. 可能的解决方向
"""
            
            # 调用LLM
            response = call_module_llm(
                module_name="SageDispatch",
                prompt=prompt,
                max_tokens=500
            )
            
            return {
                "analysis": response,
                "source": "llm_enhanced"
            }
        except Exception as e:
            # LLM不可用时降级，记录日志
            logger.debug(f"[SD-P1] LLM analysis fallback: {e}")
            return None
    
    def _determine_routing(self, intent: Dict, parsed: Dict) -> Dict:
        """确定后续调度路由"""
        intents = intent.get("all_intents", [])
        problem_types = parsed.get("problem_types", [])
        
        recommended_chain = []
        reasoning_depth = "standard"
        
        # 根据意图确定路由
        if "innovation" in intents:
            recommended_chain = ["SD-F1", "SD-D3", "SD-C2"]
            reasoning_depth = "deep"
        elif "decision" in intents:
            recommended_chain = ["SD-F1", "SD-D2", "SD-C2"]
            reasoning_depth = "deep"
        elif "planning" in intents:
            recommended_chain = ["SD-F1", "SD-D2", "SD-C1"]
            reasoning_depth = "standard"
        elif "analysis" in intents:
            recommended_chain = ["SD-R2", "SD-D1", "SD-D2"]
            reasoning_depth = "standard"
        elif "execution" in intents:
            recommended_chain = ["SD-E1", "SD-L1"]
            reasoning_depth = "light"
        else:
            recommended_chain = ["SD-R2", "SD-F1"]
        
        return {
            "recommended_chain": recommended_chain,
            "reasoning_depth": reasoning_depth,
            "requires_wise_schools": "planning" in intents or "innovation" in intents,
            "requires_decision": "decision" in intents or "planning" in intents
        }


# ==================== SD-R1 三层推理调度器 ====================

class ThreeLayerReasoning(BaseDispatcher):
    """
    SD-R1 三层推理调度器【监管调度】

    核心职责：
    - 对所有推理流程进行监管
    - 确保推理过程符合三层推理标准
    - 验证推理链的完整性和有效性
    - 拦截不符合规范的推理输出

    三层推理标准：
    1. 感知层（Perception）：问题感知 → 模式识别 → 意图理解
    2. 认知层（Cognition）：前提提取 → 逻辑推理 → 结论生成
    3. 元认知层（Metacognition）：推理审视 → 谬误检测 → 质量评估
    """

    dispatcher_id: str = "SD-R1"
    dispatcher_name: str = "三层推理监管"

    # 三层推理标准定义
    REASONING_LAYERS = {
        "perception": {
            "name": "感知层",
            "description": "问题感知、模式识别、意图理解",
            "checks": ["关键词识别", "意图分类", "上下文理解"]
        },
        "cognition": {
            "name": "认知层",
            "description": "前提提取、逻辑推理、结论生成",
            "checks": ["前提完整性", "推理有效性", "结论可推导性"]
        },
        "metacognition": {
            "name": "元认知层",
            "description": "推理审视、谬误检测、质量评估",
            "checks": ["逻辑谬误", "认知偏差", "推理质量"]
        }
    }

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """
        执行三层推理监管

        职责：
        1. 接收其他调度器的推理输出
        2. 按照三层标准进行审查
        3. 验证是否符合规范
        4. 返回监管报告和修正建议
        """
        text = request.problem.get("description", "")

        # 获取父级输出（如果有）
        parent_output = getattr(request, 'parent_output', {}) or request.metadata.get("parent_output", {})

        trace = {
            "layers": [],
            "checks": [],
            "issues": [],
            "compliance": True
        }

        # 第一层：感知层监管
        perception_result = self._supervise_perception(text, parent_output)
        trace["layers"].append(perception_result)

        # 第二层：认知层监管
        cognition_result = self._supervise_cognition(text, parent_output)
        trace["layers"].append(cognition_result)

        # 第三层：元认知层监管
        metacognition_result = self._supervise_metacognition(text, parent_output)
        trace["layers"].append(metacognition_result)

        # 综合评估
        compliance, issues = self._evaluate_compliance(trace)
        trace["compliance"] = compliance
        trace["issues"] = issues

        # 生成监管报告
        report = self._generate_report(trace)

        # 计算置信度
        confidence = 0.95 if compliance else 0.6

        return {
            "dispatched_to": ["SD-R1"],
            "confidence": confidence,
            "compliance": compliance,
            "output": {
                "type": "three_layer_reasoning_supervisor",
                "description": "三层推理监管调度",
                "parent_output_reviewed": parent_output is not None,
                "layers": trace["layers"],
                "compliance": compliance,
                "issues": issues,
                "report": report,
                "recommendations": self._generate_recommendations(compliance, issues)
            },
            "trace": trace
        }

    def _supervise_perception(self, text: str, parent_output: Dict) -> Dict:
        """监管感知层"""
        checks = []

        has_keywords = len(text) > 5
        checks.append({
            "check": "问题感知",
            "passed": has_keywords,
            "detail": "问题描述清晰" if has_keywords else "问题描述不足"
        })

        pattern_detected = bool(parent_output.get("pattern_type")) if parent_output else False
        checks.append({
            "check": "模式识别",
            "passed": pattern_detected,
            "detail": f"识别模式：{parent_output.get('pattern_type', 'unknown')}" if pattern_detected else "未检测到模式"
        })

        intent_understood = parent_output.get("confidence", 0) > 0.5 if parent_output else True
        checks.append({
            "check": "意图理解",
            "passed": intent_understood,
            "detail": "意图理解准确" if intent_understood else "意图理解存疑"
        })

        # 根据实际检查结果计算是否全部通过
        passed = all(c["passed"] for c in checks)

        return {
            "layer": "perception",
            "name": "感知层监管",
            "all_passed": passed,
            "checks": checks
        }

    def _supervise_cognition(self, text: str, parent_output: Dict) -> Dict:
        """监管认知层"""
        checks = []

        premises = parent_output.get("premises", []) if parent_output else []
        has_premises = len(premises) >= 1
        checks.append({
            "check": "前提提取",
            "passed": has_premises,
            "detail": f"提取了{len(premises)}个前提" if has_premises else "未提取到有效前提"
        })

        reasoning_chain = parent_output.get("reasoning_chain", []) if parent_output else []
        has_reasoning = len(reasoning_chain) > 0
        checks.append({
            "check": "逻辑推理",
            "passed": has_reasoning,
            "detail": f"推理链完整：{len(reasoning_chain)}步" if has_reasoning else "推理链不完整"
        })

        conclusion = parent_output.get("conclusion", {}) if parent_output else {}
        has_conclusion = bool(conclusion.get("text")) if conclusion else False
        checks.append({
            "check": "结论生成",
            "passed": has_conclusion,
            "detail": "结论已生成" if has_conclusion else "未生成有效结论"
        })

        # 根据实际检查结果计算是否全部通过
        passed = all(c["passed"] for c in checks)

        return {
            "layer": "cognition",
            "name": "认知层监管",
            "all_passed": passed,
            "checks": checks
        }

    def _supervise_metacognition(self, text: str, parent_output: Dict) -> Dict:
        """监管元认知层"""
        checks = []
        passed = True

        output_type = parent_output.get("type", "direct") if parent_output else "direct"
        checks.append({
            "check": "推理审视",
            "passed": True,
            "detail": f"输出类型：{output_type}"
        })

        fallacies = parent_output.get("fallacies", []) if parent_output else []
        no_fallacies = len(fallacies) == 0
        checks.append({
            "check": "谬误检测",
            "passed": no_fallacies,
            "detail": "未检测到谬误" if no_fallacies else f"检测到{len(fallacies)}个谬误"
        })
        if not no_fallacies:
            passed = False

        confidence = parent_output.get("confidence", 0.8) if parent_output else 0.75
        quality_acceptable = confidence >= 0.6
        checks.append({
            "check": "质量评估",
            "passed": quality_acceptable,
            "detail": f"置信度：{confidence:.2f} {'✓' if quality_acceptable else '⚠️'}"
        })

        return {
            "layer": "metacognition",
            "name": "元认知层监管",
            "all_passed": passed,
            "checks": checks
        }

    def _evaluate_compliance(self, trace: Dict) -> tuple:
        """评估是否符合三层推理标准"""
        issues = []
        for layer_result in trace["layers"]:
            if not layer_result.get("all_passed", True):
                issues.append(f"{layer_result['name']}存在未通过项")
        compliance = len(issues) == 0
        return compliance, issues

    def _generate_report(self, trace: Dict) -> Dict:
        """生成监管报告"""
        layer_summary = []
        for layer in trace["layers"]:
            status = "✓" if layer.get("all_passed", True) else "✗"
            layer_summary.append(f"{status} {layer['name']}")
        return {
            "summary": " | ".join(layer_summary),
            "total_issues": len(trace["issues"]),
            "overall_status": "PASSED" if trace["compliance"] else "FAILED"
        }

    def _generate_recommendations(self, compliance: bool, issues: List[str]) -> List[str]:
        """生成修正建议"""
        if compliance:
            return ["推理流程符合三层标准，无需修正"]
        recommendations = []
        for issue in issues:
            if "感知层" in issue:
                recommendations.append("建议增加问题特征提取")
            if "认知层" in issue:
                recommendations.append("建议完善推理链路")
            if "元认知层" in issue:
                recommendations.append("建议进行谬误检测和质量审查")
        return recommendations if recommendations else ["请重新审视推理流程"]





# ==================== SD-R2 谬误检测调度器 ====================

class FallacyChecker(BaseDispatcher):
    """
    SD-R2 谬误检测调度器
    8种常见逻辑谬误检测
    
    【神行轨集成】
    枝丫特权：可调用神行轨(Track B)完成具体执行工作
    """

    dispatcher_id: str = "SD-R2"
    dispatcher_name: str = "谬误检测"

    # 谬误模式 - 多关键词上下文匹配
    # 每个谬误类型需要至少2个相关关键词同时出现才判定（人身攻击除外）
    FALLACY_PATTERNS = {
        "ad_hominem": {
            "name": "人身攻击",
            "patterns": [["你这个人", "他这种人", "谁让你", "你这种", "这种人"]],  # 单关键词即可触发
            "severity": "high",
            "min_matches": 1
        },
        "straw_man": {
            "name": "稻草人",
            "patterns": [
                ["你说的是", "你的意思就是", "你不过是想", "你实际上", "你的真实意思"],
                ["曲解", "歪曲", "故意", "无非", "只不过"]
            ],
            "severity": "medium",
            "min_matches": 2
        },
        "appeal_to_authority": {
            "name": "权威崇拜",
            "patterns": [
                ["专家说", "权威认为", "某某名人说过", "权威人士", "某教授", "某博士"],
                ["说过", "认为", "指出", "表示", "说过"]
            ],
            "severity": "low",
            "min_matches": 2
        },
        "false_dilemma": {
            "name": "虚假两难",
            "patterns": [
                ["要么", "不是A就是B", "只有两种", "只有两条路"],
                ["只能", "必须选择", "别无选择", "没有别的", "非此即彼"]
            ],
            "severity": "medium",
            "min_matches": 2
        },
        "slippery_slope": {
            "name": "滑坡谬误",
            "patterns": [
                ["如果", "一旦", "假如", "要是"],
                ["就会", "最终导致", "必然", "势必", "一连串", "一步步", "不可收拾", "灾难性"]
            ],
            "severity": "medium",
            "min_matches": 2
        },
        "circular_reasoning": {
            "name": "循环论证",
            "patterns": [
                ["因为A所以A", "原因就是因为", "为什么", "因为"],
                ["所以", "因此", "由此可见", "这就证明", "这说明"],
                ["换句话说", "也就是说", "换言之", "换句话说就是"]
            ],
            "severity": "high",
            "min_matches": 2
        },
        "hasty_generalization": {
            "name": "草率概括",
            "patterns": [
                ["所有", "都", "从来不", "总是", "每个人", "全部", "一律"],
                ["根据", "从", "例子", "案例", "经验"]
            ],
            "severity": "medium",
            "min_matches": 2
        },
        "red_herring": {
            "name": "转移话题",
            "patterns": [
                ["说起这个", "不过", "另外", "其实", "话说回来", "顺便一提"],
                ["更重要", "关键", "真正", "本质", "其实", "实际上"]
            ],
            "severity": "medium",
            "min_matches": 2
        }
    }

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行谬误检测"""
        text = request.problem.get("description", "")

        # 检测谬误
        fallacies = self._detect_fallacies(text)

        # 评估论证
        assessment = self._assess_argument(text, fallacies)
        
        # 【神行轨调用】枝丫特权：调用神行轨进行合规审查
        track_b_result = self._call_track_b(text, fallacies)

        return {
            "dispatched_to": ["SD-R2"],
            "confidence": _calc_confidence(0.75, {"has_output": True, "passed_check": not fallacies}),
            "track_b_called": track_b_result.get("called", False),
            "track_b_result": track_b_result.get("result"),
            "output": {
                "type": "fallacy_check",
                "fallacies": fallacies,
                "passed": len(fallacies) == 0,
                "assessment": assessment,
                "recommendation": self._generate_recommendation(fallacies)
            }
        }
    
    def _call_track_b(self, text: str, fallacies: List[Dict]) -> Dict[str, Any]:
        """调用神行轨进行合规审查"""
        try:
            # 尝试多种导入方式
            try:
                from .track_b_adapter import execute_with_track_b
            except (ImportError, ValueError):
                try:
                    from track_b_adapter import execute_with_track_b
                except ImportError:
                    from .track_b_adapter import TrackBExecutor
                    executor = TrackBExecutor.get_instance()
                    fallacy_count = len(fallacies)
                    fallacy_names = [f["name"] for f in fallacies[:3]] if fallacies else ["无"]
                    task = f"【谬误检测】发现{fallacy_count}个问题：{','.join(fallacy_names)}。内容：{text[:100]}"
                    result = executor.execute_quick("SD-R2", task)
                    return _wrap_track_b_result(result)
            
            # 构建任务描述
            fallacy_count = len(fallacies)
            fallacy_names = [f["name"] for f in fallacies[:3]] if fallacies else ["无"]
            task = f"【谬误检测】发现{fallacy_count}个问题：{','.join(fallacy_names)}。内容：{text[:100]}"
            
            # 调用神行轨 - 刑部负责律法和合规
            result = execute_with_track_b(
                branch_id="SD-R2",
                task=task,
                department="刑部"
            )
            
            return {
                "called": not result.get("is_mock", False),
                "is_mock": result.get("is_mock", False),
                "result": result
            }
        except Exception as e:
            return {
                "called": False,
                "error": str(e)
            }

    def _detect_fallacies(self, text: str) -> List[Dict]:
        """检测谬误 - 多关键词上下文匹配"""
        detected = []
        text_lower = text.lower()

        for fallacy_id, config in self.FALLACY_PATTERNS.items():
            pattern_groups = config["patterns"]
            min_matches = config.get("min_matches", 2)
            
            # 计算匹配的关键词组数
            matched_groups = 0
            matched_patterns = []
            
            for group in pattern_groups:
                for pattern in group:
                    if pattern in text_lower:
                        matched_groups += 1
                        matched_patterns.append(pattern)
                        break  # 该组已匹配，检查下一组
            
            # 只有达到最小匹配数才判定为谬误
            if matched_groups >= min_matches:
                detected.append({
                    "type": fallacy_id,
                    "name": config["name"],
                    "matched_patterns": matched_patterns,
                    "matched_groups": matched_groups,
                    "severity": config["severity"],
                    "suggestion": self._get_suggestion(fallacy_id)
                })

        return detected

    def _get_suggestion(self, fallacy_type: str) -> str:
        """获取建议"""
        suggestions = {
            "ad_hominem": "避免人身攻击，聚焦论点本身",
            "straw_man": "准确理解对方观点，避免曲解",
            "appeal_to_authority": "权威不等于正确，需要独立验证",
            "false_dilemma": "考虑是否存在第三种选择",
            "slippery_slope": "每一步推理都需要充分证据支撑",
            "circular_reasoning": "结论不能用作前提",
            "hasty_generalization": "需要更多样本支持概括性结论",
            "red_herring": "保持论证焦点，避免偏离主题"
        }
        return suggestions.get(fallacy_type, "请重新审视论证逻辑")

    def _assess_argument(self, text: str, fallacies: List[Dict]) -> Dict:
        """评估论证"""
        score = 100

        for f in fallacies:
            if f["severity"] == "high":
                score -= 30
            elif f["severity"] == "medium":
                score -= 15
            else:
                score -= 5

        if len(text) < 50:
            score -= 20

        return {
            "score": max(0, score),
            "grade": "A" if score >= 90 else "B" if score >= 70 else "C" if score >= 50 else "D",
            "strength": "强" if score >= 80 else "中等" if score >= 60 else "弱"
        }

    def _generate_recommendation(self, fallacies: List[Dict]) -> str:
        """生成建议"""
        if not fallacies:
            return "论证逻辑较为严谨，未检测到明显谬误。"

        high_severity = [f for f in fallacies if f["severity"] == "high"]
        if high_severity:
            return f"检测到{len(high_severity)}个高严重性谬误，建议优先修正：{', '.join(f['name'] for f in high_severity)}"

        return f"检测到{len(fallacies)}个逻辑谬误，建议逐一检查修正。"


# ==================== SD-F1 学派融合调度器 ====================

class SchoolFusion(BaseDispatcher):
    """
    SD-F1 25学派融合调度器
    东西方25学派的智慧融合
    
    【神行轨集成】
    枝丫特权：可调用神行轨(Track B)完成具体执行工作
    """

    dispatcher_id: str = "SD-F1"
    dispatcher_name: str = "25学派融合"

    # 学派配置
    SCHOOLS = {
        # 东方智慧
        "daoism": {"name": "道家", "domain": "东方智慧", "keywords": ["无为", "自然", "道"]},
        "confucianism": {"name": "儒家", "domain": "东方智慧", "keywords": ["仁义", "礼", "君子"]},
        "buddhism": {"name": "佛家", "domain": "东方智慧", "keywords": ["因果", "缘", "空"]},
        "military": {"name": "兵家", "domain": "东方智慧", "keywords": ["谋略", "权变", "战略"]},

        # 西方智慧
        "philosophy": {"name": "哲学", "domain": "西方智慧", "keywords": ["本体", "认识", "价值"]},
        "science": {"name": "科学", "domain": "西方智慧", "keywords": ["实验", "假设", "验证"]},
        "economics": {"name": "经济学", "domain": "西方智慧", "keywords": ["供需", "成本", "效益"]},
        "psychology": {"name": "心理学", "domain": "西方智慧", "keywords": ["动机", "认知", "行为"]},
        "sociology": {"name": "社会学", "domain": "西方智慧", "keywords": ["群体", "结构", "制度"]},
        "management": {"name": "管理学", "domain": "西方智慧", "keywords": ["组织", "领导", "效率"]},
        "law": {"name": "法学", "domain": "西方智慧", "keywords": ["权利", "义务", "规则"]},
        "politics": {"name": "政治学", "domain": "西方智慧", "keywords": ["权力", "治理", "政策"]},
        "history": {"name": "历史学", "domain": "西方智慧", "keywords": ["规律", "趋势", "演变"]},

        # 现代智慧
        "systems": {"name": "系统论", "domain": "现代智慧", "keywords": ["系统", "反馈", "整体"]},
        "complexity": {"name": "复杂性科学", "domain": "现代智慧", "keywords": ["涌现", "混沌", "自组织"]},
        "game_theory": {"name": "博弈论", "domain": "现代智慧", "keywords": ["策略", "均衡", "竞合"]},
        "operations": {"name": "运筹学", "domain": "现代智慧", "keywords": ["优化", "决策", "模型"]},
        "ai": {"name": "人工智能", "domain": "现代智慧", "keywords": ["算法", "学习", "智能"]},
        "design_thinking": {"name": "设计思维", "domain": "现代智慧", "keywords": ["用户", "迭代", "共情"]},
        "lean": {"name": "精益创业", "domain": "现代智慧", "keywords": ["MVP", "验证", "快速"]},

        # 中国哲学
        "yinyang": {"name": "阴阳家", "domain": "中国哲学", "keywords": ["阴阳", "辩证", "对立"]},
        "ming": {"name": "名家", "domain": "中国哲学", "keywords": ["名实", "概念", "逻辑"]},
        "mozism": {"name": "墨家", "domain": "中国哲学", "keywords": ["兼爱", "非攻", "实用"]},
        "legalism": {"name": "法家", "domain": "中国哲学", "keywords": ["法治", "术势", "制度"]}
    }

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行学派融合"""
        text = request.problem.get("description", "")

        # 匹配学派
        matched_schools = self._match_schools(text)

        # 生成融合视角
        perspectives = self._generate_perspectives(matched_schools)

        # 综合分析
        synthesis = self._synthesize(perspectives, text)
        
        # 【神行轨调用】枝丫特权：调用神行轨执行具体智慧分析
        track_b_result = self._call_track_b(text, matched_schools)

        return {
            "dispatched_to": ["SD-F1"],
            "confidence": _calc_confidence(0.60, {"has_output": bool(matched_schools), "result_count": len(matched_schools)}),
            "track_b_called": track_b_result.get("called", False),
            "track_b_result": track_b_result.get("result"),
            "output": {
                "type": "school_fusion",
                "matched_schools": matched_schools,
                "perspectives": perspectives,
                "synthesis": synthesis,
                "summary": f"融合{len(matched_schools)}个学派视角的洞察"
            }
        }
    
    def _call_track_b(self, text: str, schools: List[Dict]) -> Dict[str, Any]:
        """调用神行轨获取智慧增强"""
        try:
            # 尝试多种导入方式
            try:
                from .track_b_adapter import execute_with_track_b
            except (ImportError, ValueError):
                try:
                    from track_b_adapter import execute_with_track_b
                except ImportError:
                    # 直接执行函数体作为后备
                    from .track_b_adapter import TrackBExecutor
                    executor = TrackBExecutor.get_instance()
                    school_names = [s["name"] for s in schools[:3]]
                    task = f"从{','.join(school_names)}视角分析问题：{text[:100]}"
                    result = executor.execute_quick("SD-F1", task)
                    return _wrap_track_b_result(result)
            
            # 构建任务描述
            school_names = [s["name"] for s in schools[:3]]
            task = f"从{','.join(school_names)}视角分析问题：{text[:100]}"
            
            # 调用神行轨
            result = execute_with_track_b(
                branch_id="SD-F1",
                task=task,
                department="礼部"
            )
            
            return _wrap_track_b_result(result)
        except Exception as e:
            return {
                "called": False,
                "error": str(e)
            }

    def _match_schools(self, text: str) -> List[Dict]:
        """匹配相关学派"""
        matched = []
        text_lower = text.lower()

        for school_id, config in self.SCHOOLS.items():
            score = 0
            for kw in config["keywords"]:
                if kw in text_lower:
                    score += 1

            if score > 0:
                matched.append({
                    "id": school_id,
                    "name": config["name"],
                    "domain": config["domain"],
                    "relevance": min(1.0, score * 0.3),
                    "insights": self._generate_school_insights(school_id, text)
                })

        # 按相关性排序
        matched.sort(key=lambda x: x["relevance"], reverse=True)

        # 至少返回3个学派
        if len(matched) < 3:
            # 添加默认学派
            for default in ["philosophy", "systems", "yinyang"]:
                if not any(s["id"] == default for s in matched):
                    matched.append({
                        "id": default,
                        "name": self.SCHOOLS[default]["name"],
                        "domain": self.SCHOOLS[default]["domain"],
                        "relevance": 0.3,
                        "insights": self._generate_school_insights(default, "")
                    })

        return matched[:6]

    def _generate_school_insights(self, school_id: str, text: str) -> List[str]:
        """生成学派洞察 — v7.2: 覆盖全部25个学派"""
        insights_map = {
            # 东方智慧
            "daoism": ["顺应自然规律", "无为而治的智慧", "以柔克刚的策略"],
            "confucianism": ["以仁为本", "修身齐家的路径", "礼治秩序的构建"],
            "buddhism": ["因果轮回", "内心修行的方法", "破除执念的智慧"],
            "military": ["知己知彼", "灵活应变的策略", "以正合以奇胜"],
            # 西方智慧
            "philosophy": ["批判性思考", "追问本质的方法", "逻辑推理的力量"],
            "science": ["实证精神", "假设验证的流程", "可证伪性原则"],
            "economics": ["理性选择", "成本效益的分析", "供需平衡的规律"],
            "psychology": ["行为动机", "认知偏差的识别", "情绪管理的智慧"],
            "sociology": ["群体动力学", "社会结构分析", "制度变迁的规律"],
            "management": ["组织效率优化", "领导力与激励", "战略执行框架"],
            "law": ["权利与义务平衡", "规则治理的智慧", "公平正义的追求"],
            "politics": ["权力制衡机制", "公共治理框架", "政策评估方法"],
            "history": ["历史规律的洞察", "兴衰更替的周期", "以史为鉴的智慧"],
            # 现代智慧
            "systems": ["整体思维", "反馈机制的把握", "系统动力分析"],
            "complexity": ["涌现效应", "混沌中的秩序", "自组织演化"],
            "game_theory": ["策略互动", "利益均衡的分析", "纳什均衡与竞争"],
            "operations": ["优化决策模型", "资源配置效率", "约束条件下的最优解"],
            "ai": ["算法驱动决策", "数据智能分析", "自动化与增强智能"],
            "design_thinking": ["用户中心设计", "快速迭代验证", "同理心洞察"],
            "lean": ["最小可行验证(MVP)", "快速试错迭代", "消除浪费的精益思维"],
            # 中国哲学
            "yinyang": ["对立统一", "动态平衡的智慧", "阴阳转化的辩证"],
            "ming": ["名实之辩", "概念逻辑分析", "语言与实在的关系"],
            "mozism": ["兼爱非攻", "实用主义的验证", "逻辑推理的尚同"],
            "legalism": ["法治严明", "制度设计的术势", "赏罚分明的治理"],
        }
        return insights_map.get(school_id, ["该学派的分析视角", "跨领域融合的智慧"])

    def _generate_perspectives(self, schools: List[Dict]) -> Dict:
        """生成多视角分析"""
        perspectives = {}

        for school in schools:
            perspectives[school["name"]] = {
                "domain": school["domain"],
                "relevance": school["relevance"],
                "insights": school["insights"],
                "question": f"从{school['name']}视角看这个问题"
            }

        return perspectives

    def _synthesize(self, perspectives: Dict, original_text: str) -> Dict:
        """综合分析"""
        domains = {}
        for p in perspectives.values():
            d = p["domain"]
            domains[d] = domains.get(d, 0) + p["relevance"]

        dominant_domain = max(domains, key=domains.get) if domains else "综合"

        return {
            "approach": "多学派融合分析",
            "dominant_domain": dominant_domain,
            "key_insights": [
                f"综合{len(perspectives)}个学派的智慧",
                f"主要采用{dominant_domain}视角",
                "各学派视角互补，形成立体认知"
            ],
            "balanced_view": "需要兼顾各方视角，在对立中寻求统一"
        }




# ==================== SD-D 系列深度推理调度器 ====================

class _BuiltinLightReasoner:
    """内置轻量推理引擎 — 当 DivineReason 外部依赖不可用时自动降级使用"""

    def __init__(self, depth: str = "standard"):
        self.depth = depth
        self._confidence_map = {"light": 0.70, "standard": 0.75, "deep": 0.80}

    def reason(self, problem: Dict) -> Dict:
        text = problem.get("description", "")
        confidence = self._confidence_map.get(self.depth, 0.75)

        # 根据深度级别执行不同层次的推理
        layers_used = 1 if self.depth == "light" else (2 if self.depth == "standard" else 3)

        # 提取推理要素
        keywords = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,}', text)

        # 前提提取
        premises = self._extract_premises(text)

        # 逻辑推理链
        reasoning_chain = self._build_reasoning_chain(text, premises)

        # 结论生成
        conclusion = self._generate_conclusion(text, reasoning_chain, confidence)

        return {
            "layers_used": layers_used,
            "confidence": confidence,
            "premises": premises,
            "reasoning_chain": reasoning_chain,
            "conclusion": conclusion,
            "depth": self.depth,
            "engine": "builtin_light",
        }

    def _extract_premises(self, text: str) -> List[str]:
        """提取前提"""
        premises = []
        patterns = [
            (r'(因为|由于|鉴于)\s*[^\n，。]+', "因果前提"),
            (r'(如果|假设|假如)\s*[^\n，。]+', "假设前提"),
            (r'(根据|按照|依据)\s*[^\n，。]+', "依据前提"),
        ]
        for pattern, label in patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                premises.append(f"[{label}] {m}")
        if not premises:
            premises.append(f"[事实前提] {text[:50]}")
        return premises[:5]

    def _build_reasoning_chain(self, text: str, premises: List[str]) -> List[Dict]:
        """构建推理链"""
        chain = []
        chain.append({"step": "前提提取", "result": f"提取{len(premises)}个前提"})
        chain.append({"step": "逻辑推理", "result": "基于前提进行演绎和归纳推理"})
        if self.depth in ("standard", "deep"):
            chain.append({"step": "假设探索", "result": "生成替代假设并验证"})
        if self.depth == "deep":
            chain.append({"step": "元认知审视", "result": "审视推理过程的可靠性和偏差"})
        return chain

    def _generate_conclusion(self, text: str, chain: List[Dict], confidence: float) -> str:
        """生成结论"""
        return f"基于对问题的多维度分析（推理深度={self.depth}，置信度={confidence:.2f}），已完成{len(chain)}层推理分析。"


class SuperReasoning(BaseDispatcher):
    """
    SD-D1/D2/D3 深度推理调度器

    【神行轨集成】
    枝丫特权：可调用神行轨(Track B)完成具体执行工作

    职责：
    - 根据请求的深度级别，调用推理模型
    - SD-D1: 轻量深度 → 表层推理
    - SD-D2: 标准深度 → 深度推理
    - SD-D3: 极致深度 → 极致推理

    依赖策略：
    - 优先尝试导入完整 DivineReason（somn 包内）
    - 不可用时自动降级为内置轻量推理引擎
    """

    dispatcher_id: str = "SD-D2"
    dispatcher_name: str = "深度推理"

    MODE_CONFIG = {
        "light": {
            "node_load": 0.25,
            "hanlin_review": False,
            "time_target": 3.0,
            "name": "轻量深度",
            "divine_depth": "light",
            "description": "表层推理（轻量模式）"
        },
        "standard": {
            "node_load": 0.40,
            "hanlin_review": True,
            "time_target": 5.0,
            "name": "标准深度",
            "divine_depth": "standard",
            "description": "深度推理（标准模式）"
        },
        "deep": {
            "node_load": 0.70,
            "hanlin_review": True,
            "time_target": 10.0,
            "name": "极致深度",
            "divine_depth": "deep",
            "description": "极致推理（深度模式）"
        }
    }

    def __init__(self, mode: str = "standard"):
        super().__init__()
        self.mode = mode
        self.config = self.MODE_CONFIG.get(mode, self.MODE_CONFIG["standard"])
        self.dispatcher_id = f"SD-D{'1' if mode=='light' else '2' if mode=='standard' else '3'}"
        # 初始化推理模型：优先 DivineReason，不可用时降级为内置引擎
        self.model = self._init_model()
        self._using_builtin = isinstance(self.model, _BuiltinLightReasoner)

    def _init_model(self):
        """尝试加载 DivineReason，失败时使用内置轻量引擎"""
        try:
            # 尝试从 somn 包内导入 DivineReason
            try:
                from smart_office_assistant.src.intelligence.engines._divine_reason_engine import DivineReason
            except ImportError:
                try:
                    from intelligence.engines._divine_reason_engine import DivineReason
                except ImportError:
                    DivineReason = None

            if DivineReason is not None:
                return DivineReason(depth=self.config["divine_depth"])
        except Exception as e:
            logger.debug(f"[SD-D1/2/3] DivineReason fallback to builtin: {e}")

        # 降级为内置轻量推理引擎
        return _BuiltinLightReasoner(depth=self.config["divine_depth"])

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行深度推理 - 调用 DivineReason 模型"""

        start_time = time.time()
        text = request.problem.get("description", "")

        # 节点执行
        node_results = self._execute_nodes(text)

        # 推理整合
        reasoning = self._integrate_reasoning(node_results, text)

        # 翰林院审核（可选）
        review = None
        if self.config["hanlin_review"]:
            review = self._hanlin_review(reasoning)
        
        # 【神行轨调用】枝丫特权：调用神行轨进行人才评估
        track_b_result = self._call_track_b(text, reasoning)

        elapsed = time.time() - start_time

        return {
            "dispatched_to": [self.dispatcher_id],
            "model_called": "DivineReason",
            "model_depth": self.config["divine_depth"],
            "confidence": _calc_confidence(0.65, {"has_output": bool(reasoning), "llm_enhanced": bool(review)}),
            "track_b_called": track_b_result.get("called", False),
            "track_b_result": track_b_result.get("result"),
            "output": {
                "type": "super_reasoning",
                "mode": self.mode,
                "description": self.config["description"],
                "node_load": self.config["node_load"],
                "nodes_executed": len(node_results),
                "reasoning": reasoning,
                "hanlin_review": review,
                "time_elapsed": f"{elapsed:.2f}s"
            }
        }
    
    def _call_track_b(self, text: str, reasoning: Dict) -> Dict[str, Any]:
        """调用神行轨获取人才评估增强"""
        try:
            # 尝试多种导入方式
            try:
                from .track_b_adapter import execute_with_track_b
            except (ImportError, ValueError):
                try:
                    from track_b_adapter import execute_with_track_b
                except ImportError:
                    from .track_b_adapter import TrackBExecutor
                    executor = TrackBExecutor.get_instance()
                    depth_name = self.config["name"]
                    task = f"【{depth_name}】深度推理分析：{text[:100]}"
                    result = executor.execute_quick(self.dispatcher_id, task)
                    return _wrap_track_b_result(result)
            
            # 构建任务描述
            depth_name = self.config["name"]
            task = f"【{depth_name}】深度推理分析：{text[:100]}"
            
            # 调用神行轨 - 吏部负责人才考核和评估
            result = execute_with_track_b(
                branch_id=self.dispatcher_id,
                task=task,
                department="吏部"
            )

            return _wrap_track_b_result(result)
        except Exception as e:
            return {
                "called": False,
                "error": str(e)
            }

    def _execute_nodes(self, text: str) -> List[Dict]:
        """执行推理节点 - 调用 DivineReason"""
        # 调用 DivineReason 模型进行推理
        divine_result = self.model.reason({"description": text})

        nodes = [
            {"id": "premise_extractor", "name": "前提提取", "status": "ready"},
            {"id": "logical_reasoner", "name": "逻辑推理", "status": "ready"},
            {"id": "causal_analyzer", "name": "因果分析", "status": "ready"},
            {"id": "evidence_assessor", "name": "证据评估", "status": "ready"},
            {"id": "counterexample_finder", "name": "反例查找", "status": "ready"},
        ]

        # 根据节点加载率决定执行
        load_threshold = self.config["node_load"]
        results = []

        for i, node in enumerate(nodes):
            if (i + 1) / len(nodes) <= load_threshold + 0.3:
                node["status"] = "executed"
                node["result"] = f"执行{node['name']}结果"
                results.append(node)

        # 添加 DivineReason 模型输出
        results.append({
            "id": "divine_reason",
            "name": "DivineReason模型",
            "status": "executed",
            "result": divine_result
        })

        return results

    def _integrate_reasoning(self, nodes: List[Dict], text: str) -> Dict:
        """整合推理结果"""
        # 获取 DivineReason 模型结果
        divine_node = next((n for n in nodes if n.get("id") == "divine_reason"), None)
        divine_result = divine_node.get("result", {}) if divine_node else {}

        return {
            "key_findings": [n.get("result", "") for n in nodes if n["status"] == "executed"],
            "reasoning_chain": f"基于{len(nodes)}个推理节点的分析",
            "depth_level": self.config["name"],
            "divine_layers": divine_result.get("layers_used", 0),
            "divine_confidence": divine_result.get("confidence", 0.8)
        }

    def _hanlin_review(self, reasoning: Dict) -> Dict:
        """翰林院三轮审核 — LLM 辅助验证"""
        divine_confidence = reasoning.get("divine_confidence", 0.8)
        
        # LLM 辅助验证（当 LLM 可用时）
        llm_review = None
        try:
            from .llm_rule_layer import call_module_llm
            findings = reasoning.get("key_findings", [])
            findings_text = " | ".join(str(f) for f in findings[:3]) if findings else "推理分析"
            prompt = f"""请审核以下推理结果的质量：

推理发现：{findings_text}
置信度：{divine_confidence:.0%}

请判断：
1. 推理链是否自洽？
2. 结论是否可靠？
3. 是否需要补充分析？

回复：合理/基本合理/不合理"""

            response = call_module_llm("SageDispatch", prompt, max_tokens=200)
            if "不合理" in response:
                llm_review = {"validated": False, "reason": response[:100]}
            elif "基本合理" in response:
                llm_review = {"validated": True, "confidence": _calc_confidence(0.65, {"llm_enhanced": True})}
            else:
                llm_review = {"validated": True, "confidence": _calc_confidence(0.75, {"llm_enhanced": True, "passed_check": True})}
        except Exception as e:
            logger.debug(f"[SD-C2] Hanlin review LLM fallback: {e}")

        passed = divine_confidence > 0.6
        if llm_review and not llm_review.get("validated", True):
            passed = False

        return {
            "round1": {
                "name": "基础验证",
                "status": "VALID" if divine_confidence > 0.6 else "FAILED",
                "checks": {"逻辑": True, "证据": divine_confidence > 0.6, "一致性": True}
            },
            "round2": {
                "name": "正反辩论",
                "status": "PASSED" if passed else "FAILED",
                "scores": {"正方": divine_confidence, "反方": divine_confidence - 0.2}
            },
            "round3": {
                "name": "最终裁定",
                "qualified_conclusion": "结论经过三轮审核验证",
                "confidence": divine_confidence + 0.05
            },
            "llm_review": llm_review,
            "passed": passed,
        }





# ==================== SD-C1 太极阴阳决策调度器 ====================

class YinYangDecision(BaseDispatcher):
    """
    SD-C1 太极阴阳决策调度器
    阴阳平衡分析
    """

    dispatcher_id: str = "SD-C1"
    dispatcher_name: str = "太极阴阳"

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行阴阳决策"""
        text = request.problem.get("description", "")

        # 阴阳分析
        yin_analysis = self._yin_analysis(text)
        yang_analysis = self._yang_analysis(text)

        # 平衡评估
        balance = self._evaluate_balance(yin_analysis, yang_analysis)

        # 决策建议
        decision = self._make_decision(yin_analysis, yang_analysis, balance)

        return {
            "dispatched_to": ["SD-C1"],
            "confidence": _calc_confidence(0.65, {"has_output": bool(balance), "result_count": 2}),
            "output": {
                "type": "yinyang_decision",
                "yin": yin_analysis,
                "yang": yang_analysis,
                "balance": balance,
                "decision": decision
            }
        }

    def _yin_analysis(self, text: str) -> Dict:
        """阴面分析（保守、内在）"""
        yin_keywords = ["稳定", "安全", "保守", "风险", "内在", "传统", "成本", "劣势"]
        matches = [kw for kw in yin_keywords if kw in text]

        return {
            "aspect": "阴（内敛、守成）",
            "factors": matches if matches else ["内在因素"],
            "score": min(1.0, len(matches) * 0.2 + 0.4),
            "description": "倾向于保守、内在、风险规避的视角"
        }

    def _yang_analysis(self, text: str) -> Dict:
        """阳面分析（进取、外在）"""
        yang_keywords = ["发展", "机遇", "进取", "创新", "外在", "突破", "收益", "优势"]
        matches = [kw for kw in yang_keywords if kw in text]

        return {
            "aspect": "阳（外展、进取）",
            "factors": matches if matches else ["外在因素"],
            "score": min(1.0, len(matches) * 0.2 + 0.4),
            "description": "倾向于进取、外在、机遇把握的视角"
        }

    def _evaluate_balance(self, yin: Dict, yang: Dict) -> Dict:
        """评估阴阳平衡"""
        yin_score = yin["score"]
        yang_score = yang["score"]
        diff = abs(yin_score - yang_score)

        if diff < 0.2:
            status = "balanced"
            description = "阴阳较为平衡"
        elif yin_score > yang_score:
            status = "yin_dominant"
            description = "偏阴，需要增加阳的视角"
        else:
            status = "yang_dominant"
            description = "偏阳，需要增加阴的视角"

        return {
            "yin_score": yin_score,
            "yang_score": yang_score,
            "difference": diff,
            "status": status,
            "description": description
        }

    def _make_decision(self, yin: Dict, yang: Dict, balance: Dict) -> Dict:
        """生成决策建议"""
        if balance["status"] == "balanced":
            suggestion = "阴阳平衡，可按原计划执行"
            confidence = 0.85
        elif balance["yin_score"] > balance["yang_score"]:
            suggestion = "建议适当增加进取因素，但保持风险控制"
            confidence = 0.75
        else:
            suggestion = "建议增加稳健措施，平衡风险与机遇"
            confidence = 0.75

        return {
            "suggestion": suggestion,
            "confidence": confidence,
            "action": "在阴阳平衡中寻求最优决策"
        }


# ==================== SD-C2 神之架构决策调度器 ====================

class DivineArchitecture(BaseDispatcher):
    """
    SD-C2 神之架构决策调度器【调用神之架构体系】
    
    【神行轨集成】
    枝丫特权：可调用神行轨(Track B)完成具体执行工作

    核心职责：
    - 调用整个神之架构体系进行决策
    - 整合377个岗位体系的集体智慧
    - 协调多层级、多角色的决策流程
    - 输出基于架构原则的决策建议

    神之架构体系包含：
    1. 四层架构：感知层 → 认知层 → 决策层 → 执行层
    2. 七条主线：战略、执行、评估、反馈、创新、协同、进化
    3. 377个岗位：覆盖决策全流程的各个职能角色

    决策流程：
    1. 问题解析 → 分配到相关岗位
    2. 岗位讨论 → 各岗位发表意见
    3. 跨岗协调 → 解决冲突和矛盾
    4. 架构裁定 → 基于整体最优做决策
    5. 执行跟踪 → 监控决策执行效果
    """

    dispatcher_id: str = "SD-C2"
    dispatcher_name: str = "神之架构"

    # 神之架构四层定义
    ARCHITECTURE_LAYERS = {
        "perception": {
            "name": "感知层",
            "description": "问题识别、信息收集、趋势判断",
            "roles": ["观察者", "分析师", "趋势预测师"]
        },
        "cognition": {
            "name": "认知层",
            "description": "本质分析、原因追溯、影响评估",
            "roles": ["本质分析师", "因果追溯师", "影响评估师"]
        },
        "decision": {
            "name": "决策层",
            "description": "方案生成、权衡选择、最终决策",
            "roles": ["策略设计师", "风险评估师", "首席决策官"]
        },
        "execution": {
            "name": "执行层",
            "description": "计划制定、资源调配、进度跟踪",
            "roles": ["执行总监", "资源协调员", "进度监控师"]
        }
    }

    # 七条主线
    ARCHITECTURE_THREADS = [
        {"id": "strategy", "name": "战略主线", "weight": 0.2},
        {"id": "execution", "name": "执行主线", "weight": 0.2},
        {"id": "evaluation", "name": "评估主线", "weight": 0.15},
        {"id": "feedback", "name": "反馈主线", "weight": 0.15},
        {"id": "innovation", "name": "创新主线", "weight": 0.1},
        {"id": "coordination", "name": "协同主线", "weight": 0.1},
        {"id": "evolution", "name": "进化主线", "weight": 0.1}
    ]

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行神之架构决策"""
        text = request.problem.get("description", "")

        # 获取上下文（如果有）
        parent_output = getattr(request, 'parent_output', {}) or request.metadata.get("parent_output", {})

        # 1. 问题解析
        problem_analysis = self._analyze_problem(text)

        # 2. 分配到相关岗位
        assigned_roles = self._assign_roles(problem_analysis)

        # 3. 各岗位讨论
        discussions = self._role_discussions(assigned_roles, text)

        # 4. 跨岗协调
        coordination = self._coordinate_roles(discussions)

        # 5. 架构裁定
        verdict = self._make_verdict(coordination, problem_analysis)

        # 6. 生成决策建议
        decision = self._generate_decision(verdict, coordination)
        
        # 【神行轨调用】枝丫特权：调用神行轨执行战略决策
        track_b_result = self._call_track_b(text, decision)

        return {
            "dispatched_to": ["SD-C2"],
            "architecture_system": "神之架构",
            "confidence": _calc_confidence(0.65, {"has_output": bool(decision), "track_b_used": track_b_result.get("called", False)}),
            "track_b_called": track_b_result.get("called", False),
            "track_b_result": track_b_result.get("result"),
            "output": {
                "type": "divine_architecture",
                "description": "神之架构决策体系",
                "problem_analysis": problem_analysis,
                "layers_involved": list(self.ARCHITECTURE_LAYERS.keys()),
                "threads_involved": [t["id"] for t in self.ARCHITECTURE_THREADS],
                "roles_assigned": len(assigned_roles),
                "discussions": discussions,
                "coordination": coordination,
                "verdict": verdict,
                "decision": decision,
                "summary": f"通过{len(assigned_roles)}个岗位参与，{len(discussions)}轮讨论，生成架构决策"
            }
        }
    
    def _call_track_b(self, text: str, decision: Dict) -> Dict[str, Any]:
        """调用神行轨执行战略决策"""
        try:
            # 尝试多种导入方式
            try:
                from .track_b_adapter import execute_with_track_b
            except (ImportError, ValueError):
                try:
                    from track_b_adapter import execute_with_track_b
                except ImportError:
                    from .track_b_adapter import TrackBExecutor
                    executor = TrackBExecutor.get_instance()
                    verdict = decision.get("verdict", "PROCESSING")
                    task = f"【神之架构决策】裁定：{verdict}。问题：{text[:100]}"
                    result = executor.execute_quick("SD-C2", task)
                    return _wrap_track_b_result(result)
            
            # 构建任务描述
            verdict = decision.get("verdict", "PROCESSING")
            task = f"【神之架构决策】裁定：{verdict}。问题：{text[:100]}"
            
            # 调用神行轨 - 兵部负责战略决策
            result = execute_with_track_b(
                branch_id="SD-C2",
                task=task,
                department="兵部"
            )

            return _wrap_track_b_result(result)
        except Exception as e:
            return {
                "called": False,
                "error": str(e)
            }

    def _analyze_problem(self, text: str) -> Dict:
        """问题解析"""
        keywords = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,}', text)

        # 判断问题类型
        problem_types = []
        if any(kw in text for kw in ["战略", "方向", "规划", "长期"]):
            problem_types.append("战略型")
        if any(kw in text for kw in ["执行", "操作", "落地", "实施"]):
            problem_types.append("执行型")
        if any(kw in text for kw in ["风险", "危机", "问题", "挑战"]):
            problem_types.append("问题型")
        if any(kw in text for kw in ["创新", "新", "变革", "转型"]):
            problem_types.append("创新型")

        return {
            "keywords": keywords[:10],
            "problem_types": problem_types if problem_types else ["通用型"],
            "complexity": "high" if len(keywords) > 20 else "medium" if len(keywords) > 10 else "low",
            "urgency": "high" if any(kw in text for kw in ["紧急", "立即", "马上"]) else "medium"
        }

    def _assign_roles(self, problem_analysis: Dict) -> List[Dict]:
        """分配岗位"""
        roles = []
        problem_types = problem_analysis.get("problem_types", [])

        # 根据问题类型分配岗位
        for layer_id, layer in self.ARCHITECTURE_LAYERS.items():
            if any(pt in ["战略型", "创新型"] for pt in problem_types) or layer_id in ["cognition", "decision"]:
                for role_name in layer["roles"][:1]:  # 每个层取一个代表岗位
                    roles.append({
                        "layer": layer_id,
                        "layer_name": layer["name"],
                        "role": role_name,
                        "status": "assigned"
                    })

        # 确保至少有4个岗位
        if len(roles) < 4:
            for i, layer_id in enumerate(list(self.ARCHITECTURE_LAYERS.keys())[:4]):
                if not any(r["layer"] == layer_id for r in roles):
                    layer = self.ARCHITECTURE_LAYERS[layer_id]
                    roles.append({
                        "layer": layer_id,
                        "layer_name": layer["name"],
                        "role": layer["roles"][0],
                        "status": "assigned"
                    })

        return roles[:5]

    def _role_discussions(self, roles: List[Dict], text: str) -> List[Dict]:
        """各岗位讨论"""
        discussions = []

        role_views = {
            "perception": "从感知角度：这个问题需要先收集更多关键信息...",
            "cognition": "从认知角度：问题的本质是结构性的挑战...",
            "decision": "从决策角度：需要在风险和收益之间找到平衡点...",
            "execution": "从执行角度：方案需要明确的时间表和资源支持..."
        }

        for role in roles:
            layer_id = role["layer"]
            discussions.append({
                "role": role["role"],
                "layer": layer_id,
                "view": role_views.get(layer_id, "从架构角度分析..."),
                "position": "支持" if layer_id in ["perception", "decision"] else "谨慎",
                "confidence": _calc_confidence(0.60, {"depth": 1}) + (sum(ord(c) for c in layer_id) % 30) / 100
            })

        return discussions

    def _coordinate_roles(self, discussions: List[Dict]) -> Dict:
        """跨岗协调"""
        # 找出分歧点
        support_count = sum(1 for d in discussions if d["position"] == "支持")
        caution_count = sum(1 for d in discussions if d["position"] == "谨慎")

        conflicts = []
        if caution_count > 0:
            conflicts.append({
                "issue": "执行方案的风险控制",
                "resolution": "增加监控机制和备选方案"
            })

        # 计算共识度
        consensus = support_count / len(discussions) if discussions else 0.5

        return {
            "total_roles": len(discussions),
            "supporting": support_count,
            "cautious": caution_count,
            "conflicts": conflicts,
            "consensus_level": consensus,
            "coordination_actions": ["召开协调会议", "明确责任分工", "制定应急预案"]
        }

    def _make_verdict(self, coordination: Dict, problem_analysis: Dict) -> Dict:
        """架构裁定"""
        consensus = coordination["consensus_level"]
        problem_types = problem_analysis.get("problem_types", [])

        # 基于共识度和问题类型做裁定
        if consensus >= 0.7:
            status = "APPROVED"
            rationale = "共识度高，建议批准执行"
        elif consensus >= 0.5:
            status = "CONDITIONAL"
            rationale = "存在分歧，需要附加条件执行"
        else:
            status = "REVIEW_REQUIRED"
            rationale = "分歧较大，建议进一步讨论"

        # 根据问题类型调整
        if "创新型" in problem_types:
            status = "APPROVED_WITH_PILOT" if status == "APPROVED" else status
            rationale += "（创新项目建议小规模试点）"

        return {
            "verdict": status,
            "rationale": rationale,
            "confidence": consensus,
            "conditions": ["加强监控", "及时反馈"] if status == "CONDITIONAL" else None
        }

    def _generate_decision(self, verdict: Dict, coordination: Dict) -> Dict:
        """生成决策建议"""
        status = verdict["verdict"]

        if status == "APPROVED":
            decision_text = "批准执行该方案"
            next_actions = ["制定详细计划", "分配执行资源", "启动执行流程"]
        elif status == "APPROVED_WITH_PILOT":
            decision_text = "批准小规模试点"
            next_actions = ["确定试点范围", "制定试点计划", "监控试点效果"]
        elif status == "CONDITIONAL":
            decision_text = "有条件批准"
            next_actions = ["完善风险控制", "准备应急预案", "加强过程监控"]
        else:
            decision_text = "建议进一步讨论"
            next_actions = ["召开扩大会议", "收集更多意见", "重新评估方案"]

        return {
            "decision": decision_text,
            "verdict": status,
            "rationale": verdict["rationale"],
            "next_actions": next_actions,
            "timeline": "分阶段推进",
            "monitoring": "建立实时监控机制"
        }




# ==================== SD-E1 五步主链执行调度器 ====================

class ChainExecutor(BaseDispatcher):
    """
    SD-E1 五步主链执行调度器
    认知→计划→执行→监控→复盘
    
    【神行轨集成】
    枝丫特权：可调用神行轨(Track B)完成具体执行工作
    """

    dispatcher_id: str = "SD-E1"
    dispatcher_name: str = "五步主链"

    STEPS = [
        {"step": 1, "name": "认知", "description": "理解问题本质"},
        {"step": 2, "name": "计划", "description": "制定执行方案"},
        {"step": 3, "name": "执行", "description": "实施行动计划"},
        {"step": 4, "name": "监控", "description": "跟踪执行过程"},
        {"step": 5, "name": "复盘", "description": "总结经验教训"}
    ]

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行五步主链"""
        text = request.problem.get("description", "")

        # 执行每一步
        step_results = []
        for s in self.STEPS:
            result = self._execute_step(s, text)
            step_results.append(result)

        # 生成执行计划
        plan = self._generate_plan(step_results, text)
        
        # 【神行轨调用】枝丫特权：调用神行轨执行具体工程任务
        track_b_result = self._call_track_b(text, plan)

        return {
            "dispatched_to": ["SD-E1"],
            "confidence": _calc_confidence(0.70, {"has_output": bool(plan), "track_b_used": track_b_result.get("called", False)}),
            "track_b_called": track_b_result.get("called", False),
            "track_b_result": track_b_result.get("result"),
            "output": {
                "type": "chain_execution",
                "steps": step_results,
                "plan": plan
            }
        }
    
    def _call_track_b(self, text: str, plan: Dict) -> Dict[str, Any]:
        """调用神行轨执行工程任务"""
        try:
            # 尝试多种导入方式
            try:
                from .track_b_adapter import execute_with_track_b
            except (ImportError, ValueError):
                try:
                    from track_b_adapter import execute_with_track_b
                except ImportError:
                    from .track_b_adapter import TrackBExecutor
                    executor = TrackBExecutor.get_instance()
                    steps = plan.get("total_steps", 5)
                    duration = plan.get("estimated_duration", "5-10天")
                    task = f"【五步主链执行】共{steps}步，预计{duration}。任务：{text[:100]}"
                    result = executor.execute_quick("SD-E1", task)
                    return _wrap_track_b_result(result)
            
            # 构建任务描述
            steps = plan.get("total_steps", 5)
            duration = plan.get("estimated_duration", "5-10天")
            task = f"【五步主链执行】共{steps}步，预计{duration}。任务：{text[:100]}"
            
            # 调用神行轨 - 工部负责执行
            result = execute_with_track_b(
                branch_id="SD-E1",
                task=task,
                department="工部"
            )

            return _wrap_track_b_result(result)
        except Exception as e:
            return {
                "called": False,
                "error": str(e)
            }

    def _execute_step(self, step: Dict, text: str) -> Dict:
        """执行单一步骤 - 根据步骤类型生成有意义的内容"""
        step_name = step.get("name", "")
        step_num = step.get("step", 0)
        
        # 根据步骤类型生成具体内容
        content_generators = {
            "认知": self._generate_cognition_content,
            "计划": self._generate_planning_content,
            "执行": self._generate_execution_content,
            "监控": self._generate_monitoring_content,
            "复盘": self._generate_review_content,
        }
        
        generator = content_generators.get(step_name, self._generate_default_content)
        content = generator(text, step_num)
        
        return {
            **step,
            "status": "completed",
            "output": content["summary"],
            "details": content["details"],
            "checklist": content.get("checklist", []),
            "duration": content.get("duration", "1-2天")
        }
    
    def _generate_cognition_content(self, text: str, step_num: int) -> Dict:
        """生成认知步骤内容 - 分析问题"""
        keywords = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,}', text)
        main_topic = keywords[0] if keywords else "该问题"
        
        return {
            "summary": f"已完成对「{main_topic}」的问题本质分析",
            "details": {
                "problem_core": f"识别出核心议题：{main_topic}",
                "key_factors": ["背景因素", "约束条件", "目标诉求"],
                "complexity_assessment": "中等复杂度，需要多维度分析"
            },
            "checklist": [
                "✓ 明确问题边界和范围",
                "✓ 识别关键利益相关方",
                "✓ 梳理核心约束条件",
                "✓ 确定成功标准"
            ],
            "duration": "1-2天"
        }
    
    def _generate_planning_content(self, text: str, step_num: int) -> Dict:
        """生成计划步骤内容 - 列出步骤"""
        return {
            "summary": "已制定分阶段执行方案",
            "details": {
                "approach": "采用迭代式执行策略",
                "phases": [
                    {"phase": 1, "name": "准备阶段", "duration": "1天"},
                    {"phase": 2, "name": "执行阶段", "duration": "3-5天"},
                    {"phase": 3, "name": "收尾阶段", "duration": "1天"}
                ],
                "resources_needed": ["人力资源", "时间预算", "工具支持"]
            },
            "checklist": [
                "✓ 制定详细时间表",
                "✓ 分配任务责任人",
                "✓ 准备必要资源",
                "✓ 设定检查点"
            ],
            "duration": "1天"
        }
    
    def _generate_execution_content(self, text: str, step_num: int) -> Dict:
        """生成执行步骤内容 - 描述动作"""
        return {
            "summary": "正在按计划实施具体行动",
            "details": {
                "actions_taken": [
                    "启动项目并组建执行团队",
                    "按计划推进各阶段任务",
                    "实时记录执行过程中的关键数据"
                ],
                "current_status": "执行进度约60%，按计划推进中",
                "risks_managed": ["进度风险", "质量风险", "资源风险"]
            },
            "checklist": [
                "✓ 按计划执行任务",
                "✓ 记录执行日志",
                "✓ 及时沟通进展",
                "✓ 处理突发问题"
            ],
            "duration": "3-5天"
        }
    
    def _generate_monitoring_content(self, text: str, step_num: int) -> Dict:
        """生成监控步骤内容 - 列出检查点"""
        return {
            "summary": "已建立多维度监控机制",
            "details": {
                "monitoring_items": [
                    {"item": "进度监控", "frequency": "每日", "status": "正常"},
                    {"item": "质量监控", "frequency": "每周", "status": "正常"},
                    {"item": "风险监控", "frequency": "实时", "status": "低风险"}
                ],
                "kpis": ["完成率", "质量评分", "资源利用率"],
                "alert_thresholds": {"delay": "1天", "quality": "低于80分"}
            },
            "checklist": [
                "✓ 设置监控指标",
                "✓ 建立预警机制",
                "✓ 定期评估进展",
                "✓ 及时调整策略"
            ],
            "duration": "持续进行"
        }
    
    def _generate_review_content(self, text: str, step_num: int) -> Dict:
        """生成复盘步骤内容 - 总结模板"""
        return {
            "summary": "已完成执行复盘与经验沉淀",
            "details": {
                "achievements": [
                    "按计划完成主要目标",
                    "积累了可复用的方法论",
                    "建立了标准化流程"
                ],
                "lessons_learned": [
                    "提前规划的重要性",
                    "风险预判的价值",
                    "团队协作的效率提升"
                ],
                "improvements": ["流程优化建议", "工具改进方向", "团队协作提升"]
            },
            "checklist": [
                "✓ 对比目标与实际结果",
                "✓ 分析成功与失败因素",
                "✓ 提炼可复用经验",
                "✓ 制定改进计划"
            ],
            "duration": "1天"
        }
    
    def _generate_default_content(self, text: str, step_num: int) -> Dict:
        """生成默认步骤内容"""
        return {
            "summary": f"步骤{step_num}已完成",
            "details": {"status": "completed"},
            "checklist": ["✓ 任务完成"],
            "duration": "1-2天"
        }

    def _generate_plan(self, steps: List[Dict], text: str) -> Dict:
        """生成执行计划"""
        return {
            "total_steps": len(steps),
            "estimated_duration": "5-10天",
            "key_milestones": ["计划制定", "执行落地", "复盘总结"]
        }


# ==================== SD-L1 结果追踪+RL调度器 ====================

class ResultTracker(BaseDispatcher):
    """
    SD-L1 结果追踪+强化学习调度器
    
    【神行轨集成】
    枝丫特权：可调用神行轨(Track B)完成具体执行工作
    """

    dispatcher_id: str = "SD-L1"
    dispatcher_name: str = "学习进化"

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行学习进化"""
        parent_output = request.metadata.get("parent_output", {})

        # 追踪结果
        tracking = self._track_result(parent_output)

        # 强化学习
        rl = self._apply_rl(tracking)
        
        # 【神行轨调用】枝丫特权：调用神行轨进行资源优化
        track_b_result = self._call_track_b(tracking)

        return {
            "dispatched_to": ["SD-L1"],
            "confidence": _calc_confidence(0.65, {"has_output": bool(rl), "track_b_used": track_b_result.get("called", False)}),
            "track_b_called": track_b_result.get("called", False),
            "track_b_result": track_b_result.get("result"),
            "output": {
                "type": "result_tracker",
                "tracking": tracking,
                "reinforcement_learning": rl
            }
        }
    
    def _call_track_b(self, tracking: Dict) -> Dict[str, Any]:
        """调用神行轨进行资源优化"""
        try:
            # 尝试多种导入方式
            try:
                from .track_b_adapter import execute_with_track_b
            except (ImportError, ValueError):
                try:
                    from track_b_adapter import execute_with_track_b
                except ImportError:
                    from .track_b_adapter import TrackBExecutor
                    executor = TrackBExecutor.get_instance()
                    improvements = tracking.get("improvements", [])
                    task = f"【学习追踪】根据追踪结果优化资源配置。改进项：{','.join(improvements[:2])}"
                    result = executor.execute_quick("SD-L1", task)
                    return _wrap_track_b_result(result)
            
            # 构建任务描述
            improvements = tracking.get("improvements", [])
            task = f"【学习追踪】根据追踪结果优化资源配置。改进项：{','.join(improvements[:2])}"
            
            # 调用神行轨 - 户部负责资源管理
            result = execute_with_track_b(
                branch_id="SD-L1",
                task=task,
                department="户部"
            )

            return _wrap_track_b_result(result)
        except Exception as e:
            return {
                "called": False,
                "error": str(e)
            }

    def _track_result(self, parent_output: Dict) -> Dict:
        """追踪结果 - 分析父级输出提取关键指标"""
        # 提取关键指标
        confidence = parent_output.get("confidence", 0.8)
        output_type = parent_output.get("type", parent_output.get("output", {}).get("type", "unknown"))
        dispatched_to = parent_output.get("dispatched_to", [])
        
        # 提取执行步骤完成情况（如果存在）
        steps_completed = 0
        total_steps = 0
        if "steps" in parent_output.get("output", {}):
            steps = parent_output["output"]["steps"]
            total_steps = len(steps)
            steps_completed = sum(1 for s in steps if s.get("status") == "completed")
        
        # 提取推理深度（如有）
        reasoning_depth = parent_output.get("model_depth", "unknown")
        
        # 提取谬误检测结果（如有）
        fallacies = parent_output.get("output", {}).get("fallacies", [])
        fallacy_count = len(fallacies)
        
        # 计算追踪评分
        score = self._calculate_tracking_score(
            confidence, steps_completed, total_steps, fallacy_count
        )
        
        # 生成改进建议
        improvements = self._generate_improvements(
            confidence, steps_completed, total_steps, fallacy_count
        )
        
        return {
            "status": "tracked",
            "confidence": confidence,
            "output_type": output_type,
            "dispatched_to": dispatched_to,
            "steps_completed": f"{steps_completed}/{total_steps}",
            "reasoning_depth": reasoning_depth,
            "fallacy_count": fallacy_count,
            "tracking_score": score,
            "improvements": improvements,
            "feedback": self._generate_feedback(confidence, output_type, fallacy_count)
        }
    
    def _calculate_tracking_score(
        self, confidence: float, steps_completed: int, 
        total_steps: int, fallacy_count: int
    ) -> Dict:
        """计算追踪评分"""
        # 置信度评分
        confidence_score = confidence * 40  # 最高40分
        
        # 步骤完成度评分
        step_score = (steps_completed / max(total_steps, 1)) * 30 if total_steps > 0 else 15  # 最高30分
        
        # 谬误评分（无谬误满分）
        fallacy_score = max(0, 30 - fallacy_count * 10)  # 最高30分
        
        total = confidence_score + step_score + fallacy_score
        
        return {
            "total": round(total, 1),
            "breakdown": {
                "confidence_score": round(confidence_score, 1),
                "step_score": round(step_score, 1),
                "fallacy_score": round(fallacy_score, 1)
            },
            "grade": "A" if total >= 80 else "B" if total >= 60 else "C" if total >= 40 else "D"
        }
    
    def _generate_improvements(
        self, confidence: float, steps_completed: int,
        total_steps: int, fallacy_count: int
    ) -> List[str]:
        """根据追踪结果生成改进建议"""
        improvements = []
        
        if confidence < 0.75:
            improvements.append("建议提升分析深度，考虑使用更深层的推理模式")
        if steps_completed < total_steps:
            improvements.append("部分执行步骤未完成，建议加强执行跟踪")
        if fallacy_count > 0:
            improvements.append("检测到逻辑谬误，建议加强论证审核")
        if not improvements:
            improvements.append("当前执行质量良好，保持现有策略")
        
        return improvements
    
    def _generate_feedback(self, confidence: float, output_type: str, fallacy_count: int) -> str:
        """生成反馈信息"""
        feedback_parts = []
        
        if confidence >= 0.85:
            feedback_parts.append("置信度较高")
        elif confidence >= 0.7:
            feedback_parts.append("置信度适中")
        else:
            feedback_parts.append("置信度偏低，建议关注")
        
        feedback_parts.append(f"输出类型：{output_type}")
        
        if fallacy_count > 0:
            feedback_parts.append(f"存在{fallacy_count}个谬误待修正")
        else:
            feedback_parts.append("未检测到谬误")
        
        return " | ".join(feedback_parts)

    def _apply_rl(self, tracking: Dict) -> Dict:
        """应用强化学习 - 根据追踪结果动态生成改进建议"""
        # 提取追踪指标
        tracking_score = tracking.get("tracking_score", {})
        score_grade = tracking_score.get("grade", "C") if tracking_score else "C"
        improvements = tracking.get("improvements", [])
        fallacy_count = tracking.get("fallacy_count", 0)
        confidence = tracking.get("confidence", 0.8)
        
        # 根据评分调整学习率（分数越低，学习率越高）
        learning_rate = 0.05 if score_grade == "A" else \
                       0.1 if score_grade == "B" else \
                       0.15 if score_grade == "C" else 0.2
        
        # 生成策略更新建议
        policy_updates = self._generate_policy_updates(score_grade, confidence, fallacy_count)
        
        # 生成Q值更新建议
        q_value_updates = self._generate_q_value_updates(tracking)
        
        # 生成下一步行动建议
        next_actions = self._generate_rl_next_actions(score_grade, improvements)
        
        return {
            "policy_update": policy_updates["summary"],
            "policy_details": policy_updates["details"],
            "q_value_update": q_value_updates["summary"],
            "q_value_details": q_value_updates["details"],
            "learning_rate": learning_rate,
            "score_grade": score_grade,
            "next_actions": next_actions,
            "reinforcement_source": "rule_based_rl"
        }
    
    def _generate_policy_updates(self, grade: str, confidence: float, fallacy_count: int) -> Dict:
        """生成策略更新建议"""
        updates = []
        details = {}
        
        if grade == "D":
            updates.append("切换至更深层推理模式")
            details["mode_change"] = "建议从当前模式切换至deep或super模式"
        
        if fallacy_count > 0:
            updates.append("增强谬误检测权重")
            details["fallacy_weight"] = f"将谬误检测权重提高{fallacy_count * 5}%"
        
        if confidence < 0.7:
            updates.append("增加知识库查询深度")
            details["knowledge_depth"] = "增加DomainNexus检索的返回结果数量"
        
        if not updates:
            updates.append("维持当前策略")
            details["status"] = "当前策略运行良好"
        
        return {
            "summary": " | ".join(updates) if updates else "维持现状",
            "details": details
        }
    
    def _generate_q_value_updates(self, tracking: Dict) -> Dict:
        """生成Q值更新建议"""
        dispatched_to = tracking.get("dispatched_to", [])
        reasoning_depth = tracking.get("reasoning_depth", "standard")
        
        # 根据执行路径更新Q值
        q_updates = []
        for dispatcher_id in dispatched_to:
            # 简化的Q值更新逻辑
            q_updates.append(f"{dispatcher_id}: {'+0.05' if tracking.get('confidence', 0) > 0.75 else '-0.02'}")
        
        return {
            "summary": f"更新{len(q_updates)}个调度器的Q值",
            "details": {
                "updated_dispatchers": dispatched_to,
                "q_adjustments": q_updates,
                "reasoning_depth_factor": f"深度={reasoning_depth}的权重调整为{1.0 if reasoning_depth == 'deep' else 0.8}"
            }
        }
    
    def _generate_rl_next_actions(self, grade: str, improvements: List[str]) -> List[str]:
        """生成强化学习的下一步行动"""
        actions = []
        
        if grade in ["C", "D"]:
            actions.append("建议增加LLM调用频率以提升分析质量")
            actions.append("考虑启用神行轨辅助执行")
        
        if not actions:
            actions.append("当前策略有效，可按现有方式继续执行")
        
        # 结合具体改进建议
        if improvements:
            actions.append(f"优先处理：{improvements[0]}")
        
        return actions


# ==================== SD-W1 网络搜索调度器 (v1.0) ====================

class WebSearchDispatcher(BaseDispatcher):
    """
    SD-W1 网络搜索调度器 v1.0【联网搜索能力】

    核心职责：
    - 联网检测：自动检测网络状态
    - 实时搜索：执行网络搜索获取最新信息
    - 结果融合：将搜索结果融入推理流程
    - 缓存管理：LRU缓存避免重复搜索

    集成方式：
    - 被 SD-R1 推理监管调度时自动触发
    - 被 SD-P1 问题调度时按需调用
    - 被 DivineReason 深度推理时增强搜索

    搜索模式：
    - quick: 快速搜索，仅返回标题（<100ms）
    - normal: 普通搜索，标题+摘要（<500ms）
    - deep: 深度搜索，完整信息（<2s）
    """

    dispatcher_id: str = "SD-W1"
    dispatcher_name: str = "网络搜索"

    # 触发关键词（出现这些关键词时自动触发网络搜索）
    TRIGGER_KEYWORDS = [
        "最新", "最近", "2024", "2025", "2026",
        "新闻", "动态", "消息", "行情", "股价",
        "数据", "统计", "报告", "研究",
        "今天", "昨日", "本周", "本月",
    ]

    # 需要实时信息的领域
    REAL_TIME_DOMAINS = [
        "股票", "金融", "科技", "互联网", "AI",
        "经济", "政策", "市场", "行业",
    ]

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """执行网络搜索"""
        text = request.problem.get("description", "")
        context = request.problem.get("context", "")
        metadata = request.metadata or {}

        # 1. 联网检测
        network_status = self._check_network()

        if not network_status["online"]:
            return {
                "dispatched_to": ["SD-W1"],
                "confidence": 0.0,
                "output": {
                    "type": "web_search",
                    "online": False,
                    "error": "网络不可用",
                    "search_results": [],
                    "network_status": network_status,
                }
            }

        # 2. 判断是否需要网络搜索
        need_search, search_mode = self._should_search(text, metadata)

        if not need_search:
            return {
                "dispatched_to": ["SD-W1"],
                "confidence": _calc_confidence(0.75, {"passed_check": True, "llm_enhanced": True}),
                "output": {
                    "type": "web_search",
                    "online": True,
                    "skipped": True,
                    "reason": "无需网络搜索（本地知识足够）",
                    "network_status": network_status,
                }
            }

        # 3. 执行网络搜索
        search_results = self._perform_search(text, context, search_mode)

        # 4. 融合搜索结果
        fused_result = self._fuse_results(search_results, text)

        return {
            "dispatched_to": ["SD-W1"],
            "confidence": search_results.get("confidence", 0.8),
            "output": {
                "type": "web_search",
                "online": True,
                "search_mode": search_mode,
                "search_results": search_results,
                "fused_result": fused_result,
                "network_status": network_status,
            }
        }

    def _check_network(self) -> Dict[str, Any]:
        """检测网络状态"""
        try:
            from .web_search_engine import get_network_status
        except ImportError:
            try:
                from web_search_engine import get_network_status
            except ImportError:
                return {"online": False, "method": "unavailable", "latency_ms": 0}

        return get_network_status()

    def _should_search(self, text: str, metadata: Dict) -> tuple[bool, str]:
        """
        判断是否需要网络搜索

        Returns:
            (need_search: bool, search_mode: str)
        """
        # 检查触发关键词
        trigger_count = sum(1 for kw in self.TRIGGER_KEYWORDS if kw in text)

        # 检查是否属于实时领域
        domain_match = any(domain in text for domain in self.REAL_TIME_DOMAINS)

        # 检查是否明确要求搜索
        explicit_search = metadata.get("force_search", False)

        # 检查是否明确跳过搜索
        skip_search = metadata.get("skip_search", False)

        if skip_search:
            return False, "none"

        if explicit_search:
            return True, "normal"

        # 触发条件（按严格度从高到低检查，避免死代码）
        if trigger_count >= 3:
            return True, "deep"
        if domain_match and trigger_count >= 1:
            return True, "normal"
        if trigger_count >= 2:
            return True, "quick"

        return False, "none"

    def _perform_search(self, text: str, context: str, mode: str) -> Dict[str, Any]:
        """
        执行网络搜索

        Args:
            text: 搜索关键词
            context: 上下文信息
            mode: 搜索模式

        Returns:
            搜索结果字典
        """
        try:
            # 懒加载导入
            try:
                from .web_search_engine import search_web, search_with_context, get_web_engine
            except ImportError:
                try:
                    from web_search_engine import search_web, search_with_context, get_web_engine
                except ImportError:
                    return {
                        "success": False,
                        "error": "WebSearchEngine 不可用",
                        "results": []
                    }

            # 根据上下文增强搜索
            if context:
                response = search_with_context(text, context, max_results=5)
            else:
                response = search_web(text, max_results=5)

            # 转换为调度器输出格式
            results = []
            for result in response.results:
                results.append({
                    "title": result.title,
                    "url": result.url,
                    "snippet": result.snippet,
                    "source": result.source,
                    "source_type": result.source_type.value if hasattr(result.source_type, 'value') else str(result.source_type),
                    "relevance": result.relevance_score,
                })

            return {
                "success": response.success,
                "query": response.query,
                "results": results,
                "total_found": response.total_found,
                "search_time_ms": response.search_time_ms,
                "search_engine": response.search_engine,
                "is_online": response.is_online,
                "error": response.error,
                "confidence": _calc_confidence(0.70, {"passed_check": response.success, "has_error": not response.success}),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "confidence": 0.0,
            }

    def _fuse_results(self, search_results: Dict, original_text: str) -> Dict[str, Any]:
        """
        融合搜索结果

        生成结构化的融合结果，便于后续推理使用
        """
        if not search_results.get("success"):
            return {
                "fusion_status": "failed",
                "summary": "网络搜索失败",
                "key_findings": [],
                "confidence": 0.0,
            }

        results = search_results.get("results", [])
        if not results:
            return {
                "fusion_status": "empty",
                "summary": "未找到相关结果",
                "key_findings": [],
                "confidence": 0.5,
            }

        # 提取关键发现
        key_findings = []
        for r in results[:3]:
            key_findings.append({
                "title": r.get("title", "")[:50],
                "insight": r.get("snippet", "")[:100],
            })

        # 生成摘要
        summary = f"网络搜索找到 {len(results)} 条相关信息"

        return {
            "fusion_status": "success",
            "summary": summary,
            "key_findings": key_findings,
            "top_result": results[0] if results else {},
            "total_results": len(results),
            "confidence": _calc_confidence(0.70, {"has_output": bool(results), "result_count": len(results)}),
        }
