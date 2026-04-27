# -*- coding: utf-8 -*-
"""
深度推理引擎核心类
DeepReasoningEngine - Core class with delegation pattern

导入关系:
- _dre_types    -> .._deep_reasoning_types    (类型定义)
- _dre_constants -> .._deep_reasoning_constants (常量)
- _dre_memory   -> .._deep_reasoning_memory   (记忆)
- _dre_subsystems -> .._deep_reasoning_subsystems (子系统)
- _dre_narrative -> .._narrative_reasoning     (叙事)
- _dre_yinyang  -> .._yinyang_reasoning       (阴阳)
- _dre_consulting -> .._consulting_reasoning   (咨询)
"""

__all__ = [
    'consult_solution',
    'get_reasoning_history',
    'get_stats',
    'reason',
]

from pathlib import Path
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import logging

from loguru import logger

# ---- 重新定位导入 ----
from .._deep_reasoning_types import ReasoningMode, ThoughtNode, ReasoningResult
from .._deep_reasoning_constants import (
    SOLUTION_CONTRADICTION_RULES,
    SOLUTION_CONSTRAINT_DIMENSIONS,
    SOLUTION_USER_ANCHOR_DIMENSIONS,
)
from .._deep_reasoning_subsystems import (
    init_logic_system,
    init_consulting_validator,
    init_neurodynamics,
    init_xinmind_system,
    init_dewey_system,
    init_top_thinking_system,
)
from .._deep_reasoning_memory import (
    load_reasoning_memory,
    save_reasoning_memory,
)
from .._narrative_reasoning import narrative_reasoning
from .._yinyang_reasoning import yinyang_dialectical_reasoning
from .._consulting_reasoning import (
    consulting_reasoning,
    consulting_reasoning_with_rules,
    consulting_research_scan,
    consulting_contradiction_detection,
    consulting_constraint_reverse,
    consulting_user_anchoring,
    consulting_bottom_up_check,
    consulting_fallacy_check,
    synthesize_consulting_answer,
    detect_solution_contradictions,
    detect_solution_constraints,
    anchor_solution_users,
)

# ---- 四大推理方法 standalone 函数 ----
from ._dre_neuro import neurodynamics_reasoning
from ._dre_xinmind import xinmind_reasoning
from ._dre_dewey import dewey_thinking_reasoning
from ._dre_top import top_methods_thinking_reasoning

# ── 数据目录延迟导入 ─────────────────────────────────────────────────────────
_DATA_DIR = None

def _get_data_dir():
    global _DATA_DIR
    if _DATA_DIR is None:
        from src.core.paths import DATA_DIR as _DD
        _DATA_DIR = _DD
    return _DATA_DIR

class DeepReasoningEngine:
    """
    深度推理引擎 - 支持多种推理模式

    核心能力:
    1. 链式推理 - 逐步分解和解决复杂问题
    2. 树推理 - 探索多种可能的推理路径
    3. 图推理 - 构建复杂的推理网络
    4. 元推理 - 反思和优化推理过程
    5. 叙事推理 - 多视角叙事fusion推理
    6. 咨询推理 - 战略咨询专用推理
    7. 神经动力学推理 - 模拟大脑节律的深度思考
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.reasoning_history: List[ReasoningResult] = []

        self.reasoning_memory_path = Path(self.config.get(
            "memory_path", str(_get_data_dir() / "reasoning_memory.json")
        ))
        self.reasoning_memory: Dict[str, ReasoningResult] = {}
        self._load_reasoning_memory()

        self.executor = ThreadPoolExecutor(max_workers=4)

        init_logic_system(self)
        init_consulting_validator(self)
        init_neurodynamics(self)
        init_xinmind_system(self)
        init_dewey_system(self)
        init_top_thinking_system(self)

        self.stats = {
            "total_reasoning": 0,
            "successful_reasoning": 0,
            "failed_reasoning": 0,
            "avg_steps": 0,
            "avg_confidence": 0.0,
            "mode_usage": {}
        }

        logger.info("深度推理引擎init完成")
        logger.info(f"  支持的推理模式: {len(ReasoningMode)}")

    def _load_reasoning_memory(self):
        self.reasoning_memory = load_reasoning_memory(self.reasoning_memory_path, 100)
        if self.reasoning_memory:
            logger.info(f"  加载推理记忆: {len(self.reasoning_memory)} 条")

    def _save_reasoning_memory(self):
        save_reasoning_memory(self.reasoning_memory_path, self.reasoning_memory)

    def _dict_to_result(self, data: Dict) -> ReasoningResult:
        from .._deep_reasoning_memory import _dict_to_result as _mem_d2r
        return _mem_d2r(data)

    def reason(self, problem: str, mode: ReasoningMode = None,
               context: Dict = None) -> ReasoningResult:
        """执行推理"""
        import time
        start_time = time.time()
        from datetime import datetime

        result_id = f"reasoning_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        logger.info(f"开始推理: {problem} [模式: {mode.value if mode else 'auto'}]")

        if mode is None:
            mode = self._auto_select_mode(problem, context or {})

        if mode == ReasoningMode.CHAIN_OF_THOUGHT:
            result = self._chain_of_thought(problem, result_id, context)
        elif mode == ReasoningMode.TREE_OF_THOUGHTS:
            result = self._tree_of_thoughts(problem, result_id, context)
        elif mode == ReasoningMode.GRAPH_OF_THOUGHTS:
            result = self._graph_of_thoughts(problem, result_id, context)
        elif mode == ReasoningMode.META_REASONING:
            result = self._meta_reasoning(problem, result_id, context)
        elif mode == ReasoningMode.NARRATIVE_REASONING:
            result = self._narrative_reasoning(problem, result_id, context)
        elif mode == ReasoningMode.CONSULTING_REASONING:
            result = self._consulting_reasoning(problem, result_id, context)
        elif mode == ReasoningMode.YINYANG_DIALECTICAL:
            result = self._yinyang_dialectical_reasoning(problem, result_id, context)
        elif mode == ReasoningMode.NEURODYNAMICS:
            result = self._neurodynamics_reasoning(problem, result_id, context)
        elif mode == ReasoningMode.XINMIND_THINKING:
            result = self._xinmind_reasoning(problem, result_id, context)
        elif mode == ReasoningMode.DEWEY_THINKING:
            result = self._dewey_thinking_reasoning(problem, result_id, context)
        elif mode == ReasoningMode.TOP_METHODS_THINKING:
            result = self._top_methods_thinking_reasoning(problem, result_id, context)
        else:
            result = ReasoningResult(
                result_id=result_id, problem=problem,
                reasoning_mode=mode, success=False,
                reasoning_trace=[], final_answer="未知推理模式"
            )

        execution_time = time.time() - start_time
        result.execution_time = execution_time
        self._update_stats(result)

        self.reasoning_memory[result_id] = result
        if len(self.reasoning_memory) > 1000:
            oldest = min(self.reasoning_memory.items(),
                         key=lambda x: x[1].metadata.get('created_at', ''))
            del self.reasoning_memory[oldest[0]]
        self._save_reasoning_memory()

        logger.info(f"推理完成: {problem} [耗时: {execution_time:.2f}s, 置信度: {result.confidence:.2f}]")
        return result

    def _auto_select_mode(self, problem: str, context: Dict) -> ReasoningMode:
        """自动选择推理模式"""
        yinyang_keywords = ['阴阳', '矛盾', '对立', '转化', '平衡', '刚柔',
                          '强弱', '进退', '攻守', '盈亏', '危机', '困境',
                          '两难', '取舍', '太极', '道法自然', '无为']
        if any(kw in problem for kw in yinyang_keywords):
            return ReasoningMode.YINYANG_DIALECTICAL

        neuro_keywords = ['深度分析', '系统优化', '认知', '神经网络', '学习机制',
                         '动态演化', '复杂系统', '自适应', '涌现', '模式recognize',
                         '记忆机制', '注意力', '创造性', '神经', '大脑', '脑',
                         '联想', '启发', '直觉', '灵感']
        if any(kw in problem for kw in neuro_keywords):
            return ReasoningMode.NEURODYNAMICS

        consulting_keywords = ['增长', '战略', '解决方案', '营收', '市场', '品牌',
                              '竞争', '渠道', '用户', '获客', '转化', '复购',
                              '目标', '十倍', '规模化', '咨询', '方案']
        if any(kw in problem for kw in consulting_keywords):
            if context.get('scenario') == 'consulting' or \
               any(kw in problem for kw in ['方案', '战略', '咨询', '解决方案']):
                return ReasoningMode.CONSULTING_REASONING

        if any(kw in problem for kw in ['战略', '困境', '品牌', '转型', '破局']):
            return ReasoningMode.NARRATIVE_REASONING

        if len(problem) < 100 and '?' in problem:
            return ReasoningMode.CHAIN_OF_THOUGHT
        if any(kw in problem.lower() for kw in ['可能', '或许', '或者']):
            return ReasoningMode.TREE_OF_THOUGHTS
        if any(kw in problem.lower() for kw in ['关系', '依赖', '影响']):
            return ReasoningMode.GRAPH_OF_THOUGHS
        return ReasoningMode.CHAIN_OF_THOUGHT

    # ── 核心推理方法 ──────────────────────────────────────────────────────────

    def _chain_of_thought(self, problem: str, result_id: str,
                          context: Dict) -> ReasoningResult:
        """链式推理 - 逐步分解和解决"""
        reasoning_trace = []
        node1 = ThoughtNode(
            id=f"{result_id}_step1",
            content=f"理解问题: {problem}",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            confidence=0.9, completeness=1.0, validity=0.95, status="completed"
        )
        reasoning_trace.append(node1)

        sub_problems = self._decompose_problem(problem)
        node2 = ThoughtNode(
            id=f"{result_id}_step2",
            content=f"分解问题为 {len(sub_problems)} 个子问题",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            parent_id=node1.id, confidence=0.85, completeness=1.0,
            validity=0.9, metadata={"sub_problems": sub_problems}, status="completed"
        )
        reasoning_trace.append(node2)

        solutions = []
        for i, sp in enumerate(sub_problems):
            sol = self._solve_sub_problem(sp, context)
            solutions.append(sol)
            reasoning_trace.append(ThoughtNode(
                id=f"{result_id}_step3_{i}",
                content=f"解决子问题: {sp}",
                reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
                parent_id=node2.id, confidence=0.8, completeness=0.9,
                validity=0.85, metadata={"solution": sol}, status="completed"
            ))

        final_answer = self._synthesize_answer(problem, solutions)
        node4 = ThoughtNode(
            id=f"{result_id}_step4",
            content=f"综合答案: {final_answer}",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            parent_id=node2.id, confidence=0.85, completeness=1.0,
            validity=0.9, status="completed"
        )
        reasoning_trace.append(node4)

        avg_confidence = sum(n.confidence for n in reasoning_trace) / len(reasoning_trace)
        return ReasoningResult(
            result_id=result_id, problem=problem,
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            success=True, reasoning_trace=reasoning_trace,
            final_answer=final_answer, confidence=avg_confidence,
            steps_count=len(reasoning_trace),
            suggestions=["可以尝试更深入的分解", "考虑使用树推理探索其他路径"]
        )

    def _tree_of_thoughts(self, problem: str, result_id: str,
                          context: Dict) -> ReasoningResult:
        """树推理 - 探索多条推理路径"""
        reasoning_trace = []
        initial_thoughts = self._generate_initial_thoughts(problem, count=3)
        node1 = ThoughtNode(
            id=f"{result_id}_root",
            content=f"生成 {len(initial_thoughts)} 个初始想法",
            reasoning_mode=ReasoningMode.TREE_OF_THOUGHTS,
            confidence=0.8, completeness=0.5, validity=0.85,
            metadata={"initial_thoughts": initial_thoughts}, status="completed"
        )
        reasoning_trace.append(node1)

        all_paths = []
        for i, thought in enumerate(initial_thoughts):
            path_nodes = []
            expanded = self._expand_thought(thought, depth=2)
            for j, step in enumerate(expanded):
                node = ThoughtNode(
                    id=f"{result_id}_branch{i}_step{j}",
                    content=step,
                    reasoning_mode=ReasoningMode.TREE_OF_THOUGHTS,
                    parent_id=path_nodes[-1].id if j > 0 else node1.id,
                    confidence=0.75 + (j * 0.05),
                    completeness=0.8, validity=0.8, status="completed"
                )
                path_nodes.append(node)
                reasoning_trace.append(node)
                node1.children_ids.append(node.id)

            all_paths.append({
                "thought": thought, "steps": expanded,
                "confidence": 0.75 + len(expanded) * 0.05
            })

        best_path = max(all_paths, key=lambda p: p["confidence"])
        reasoning_trace.append(ThoughtNode(
            id=f"{result_id}_evaluate",
            content=f"评估 {len(all_paths)} 条路径,选择最佳路径",
            reasoning_mode=ReasoningMode.TREE_OF_THOUGHTS,
            parent_id=node1.id, confidence=best_path["confidence"],
            completeness=1.0, validity=0.9,
            metadata={"best_path": best_path["thought"],
                      "all_confidences": [p["confidence"] for p in all_paths]},
            status="completed"
        ))

        final_answer = f"基于最佳路径的答案: {best_path['steps'][-1]}"
        return ReasoningResult(
            result_id=result_id, problem=problem,
            reasoning_mode=ReasoningMode.TREE_OF_THOUGHTS,
            success=True, reasoning_trace=reasoning_trace,
            final_answer=final_answer, confidence=best_path["confidence"],
            steps_count=len(reasoning_trace),
            suggestions=["可以增加初始想法的数量", "可以加深展开深度"]
        )

    def _graph_of_thoughts(self, problem: str, result_id: str,
                           context: Dict) -> ReasoningResult:
        """图推理 - 构建推理图"""
        import networkx as nx
        reasoning_trace = []

        concepts = self._extract_concepts(problem)
        node1 = ThoughtNode(
            id=f"{result_id}_concepts",
            content=f"识别 {len(concepts)} 个关键概念",
            reasoning_mode=ReasoningMode.GRAPH_OF_THOUGHTS,
            confidence=0.85, completeness=0.8, validity=0.9,
            metadata={"concepts": concepts}, status="completed"
        )
        reasoning_trace.append(node1)

        relations = self._extract_relations(concepts, problem)
        node2 = ThoughtNode(
            id=f"{result_id}_relations",
            content=f"建立 {len(relations)} 个概念关系",
            reasoning_mode=ReasoningMode.GRAPH_OF_THOUGHTS,
            parent_id=node1.id, confidence=0.8, completeness=0.9,
            validity=0.85, metadata={"relations": relations}, status="completed"
        )
        reasoning_trace.append(node2)

        graph = nx.DiGraph()
        for concept in concepts:
            graph.add_node(concept)
        for relation in relations:
            graph.add_edge(relation[0], relation[1], type=relation[2])

        node3 = ThoughtNode(
            id=f"{result_id}_graph",
            content=f"构建推理图: {graph.number_of_nodes()} 节点, {graph.number_of_edges()} 边",
            reasoning_mode=ReasoningMode.GRAPH_OF_THOUGHTS,
            parent_id=node2.id, confidence=0.85, completeness=1.0, validity=0.9,
            metadata={"nodes": graph.number_of_nodes(),
                      "edges": graph.number_of_edges(),
                      "density": nx.density(graph)},
            status="completed"
        )
        reasoning_trace.append(node3)

        reasoning_path = self._traverse_graph(graph, concepts[0])
        final_answer = f"基于图推理的结论: {reasoning_path[-1]}"

        return ReasoningResult(
            result_id=result_id, problem=problem,
            reasoning_mode=ReasoningMode.GRAPH_OF_THOUGHTS,
            success=True, reasoning_trace=reasoning_trace,
            final_answer=final_answer, confidence=0.88,
            steps_count=len(reasoning_trace),
            suggestions=["可以增加概念数量", "可以细化关系类型"]
        )

    def _meta_reasoning(self, problem: str, result_id: str,
                        context: Dict) -> ReasoningResult:
        """元推理 - 反思和优化推理过程"""
        reasoning_trace = []
        similar_reasonings = self._retrieve_similar_reasoning(problem, k=3)
        node1 = ThoughtNode(
            id=f"{result_id}_retrieve",
            content=f"检索到 {len(similar_reasonings)} 个相似推理",
            reasoning_mode=ReasoningMode.META_REASONING,
            confidence=0.9, completeness=1.0, validity=0.95,
            metadata={"similar_reasonings": [r.problem for r in similar_reasonings]},
            status="completed"
        )
        reasoning_trace.append(node1)

        if similar_reasonings:
            best_mode = max(similar_reasonings, key=lambda r: r.confidence).reasoning_mode
            mode_success_rate = sum(
                1 for r in similar_reasonings
                if r.reasoning_mode == best_mode and r.success
            ) / len(similar_reasonings)
        else:
            best_mode = ReasoningMode.CHAIN_OF_THOUGHT
            mode_success_rate = 0.8

        node2 = ThoughtNode(
            id=f"{result_id}_analyze",
            content=f"分析推理模式: 推荐 {best_mode.value} (成功率: {mode_success_rate:.2%})",
            reasoning_mode=ReasoningMode.META_REASONING,
            parent_id=node1.id, confidence=0.85, completeness=1.0, validity=0.9,
            metadata={"recommended_mode": best_mode.value, "success_rate": mode_success_rate},
            status="completed"
        )
        reasoning_trace.append(node2)

        result = self.reason(problem, mode=best_mode, context=context)

        return ReasoningResult(
            result_id=result_id, problem=problem,
            reasoning_mode=ReasoningMode.META_REASONING,
            success=result.success,
            reasoning_trace=reasoning_trace + result.reasoning_trace,
            final_answer=f"元推理结论: {result.final_answer}",
            confidence=(node1.confidence + node2.confidence + result.confidence) / 3,
            steps_count=len(reasoning_trace) + result.steps_count,
            suggestions=["可以增加相似推理的检索数量", "可以学习失败的推理模式"]
        )

    def _narrative_reasoning(self, problem: str, result_id: str,
                             context: Dict) -> ReasoningResult:
        """叙事推理 - 委托给 _narrative_reasoning 模块"""
        return narrative_reasoning(problem, result_id, context)

    def _yinyang_dialectical_reasoning(self, problem: str, result_id: str,
                                       context: Dict) -> ReasoningResult:
        """阴阳辩证推理 - 委托给 _yinyang_reasoning 模块"""
        return yinyang_dialectical_reasoning(problem, result_id, context)

    def _consulting_reasoning(self, problem: str, result_id: str,
                              context: Dict) -> ReasoningResult:
        """咨询推理 - 委托给 _consulting_reasoning 模块"""
        return consulting_reasoning(
            problem, result_id, context,
            consulting_validator=getattr(self, "consulting_validator", None),
            fallacy_detector=getattr(self, "fallacy_detector", None),
        )

    # ── 四大推理方法（委托给 standalone 函数）─────────────────────────────────

    def _neurodynamics_reasoning(self, problem: str, result_id: str,
                                 context: Dict) -> ReasoningResult:
        """神经动力学推理 - 委托给 _dre_neuro 模块"""
        return neurodynamics_reasoning(self, problem, result_id, context)

    def _xinmind_reasoning(self, problem: str, result_id: str,
                           context: Dict) -> ReasoningResult:
        """王阳明心学推理 - 委托给 _dre_xinmind 模块"""
        return xinmind_reasoning(self, problem, result_id, context)

    def _dewey_thinking_reasoning(self, problem: str, result_id: str,
                                  context: Dict) -> ReasoningResult:
        """杜威反省思维推理 - 委托给 _dre_dewey 模块"""
        return dewey_thinking_reasoning(self, problem, result_id, context)

    def _top_methods_thinking_reasoning(self, problem: str, result_id: str,
                                        context: Dict) -> ReasoningResult:
        """顶级思维法推理 - 委托给 _dre_top 模块"""
        return top_methods_thinking_reasoning(self, problem, result_id, context)

    # ── 解决方案专用咨询接口 ──────────────────────────────────────────────────

    def consult_solution(self,
                         solution_type: str,
                         problem_context: Dict,
                         client_info: Dict = None) -> Dict:
        """解决方案专用咨询推理接口"""
        client_info = client_info or {}
        problem_text = self._build_problem_text(solution_type, problem_context, client_info)
        context = {
            "scenario": "solution_consulting",
            "solution_type": solution_type,
            **problem_context,
            **client_info
        }
        result_id = f"sol_consult_{solution_type}"
        reasoning_result = self._consulting_reasoning_with_rules(
            problem_text, result_id, context, solution_type
        )
        return {
            "solution_type": solution_type,
            "problem": problem_text,
            "reasoning_result": reasoning_result.to_dict(),
            "summary": reasoning_result.final_answer,
            "confidence": reasoning_result.confidence,
            "suggestions": reasoning_result.suggestions,
            "steps": self._extract_step_summaries(reasoning_result),
        }

    def _consulting_reasoning_with_rules(self, problem: str, result_id: str,
                                         context: Dict, solution_type: str) -> ReasoningResult:
        """使用定制化规则执行咨询推理"""
        return consulting_reasoning_with_rules(
            problem, result_id, context, solution_type,
            solution_contradiction_rules=SOLUTION_CONTRADICTION_RULES,
            solution_constraint_dimensions=SOLUTION_CONSTRAINT_DIMENSIONS,
            solution_user_anchor_dimensions=SOLUTION_USER_ANCHOR_DIMENSIONS,
            consulting_validator=getattr(self, "consulting_validator", None),
            fallacy_detector=getattr(self, "fallacy_detector", None),
        )

    def _build_problem_text(self, solution_type: str,
                           problem_context: Dict, client_info: Dict) -> str:
        """构建完整的问题描述文本"""
        parts = [f"解决方案类型: {solution_type}"]
        for key in ['industry', 'stage', 'scale', 'goals', 'description', 'business_context']:
            val = problem_context.get(key)
            if val:
                parts.append(f"{key}: {', '.join(str(v) for v in val) if isinstance(val, list) else val}")
        for key in ['industry', 'pain_points', 'avg_order_value', 'execution_capability',
                     'business_description', 'current_challenges', 'growth_target']:
            val = client_info.get(key)
            if val:
                parts.append(f"{key}: {', '.join(str(v) for v in val) if isinstance(val, list) else val}")
        return '\n'.join(parts)

    def _detect_solution_contradictions(self, problem: str, context: Dict,
                                        solution_type: str) -> Dict:
        return detect_solution_contradictions(problem, context, solution_type, SOLUTION_CONTRADICTION_RULES)

    def _detect_solution_constraints(self, problem: str, context: Dict,
                                     solution_type: str) -> Dict:
        return detect_solution_constraints(problem, context, solution_type, SOLUTION_CONSTRAINT_DIMENSIONS)

    def _anchor_solution_users(self, problem: str, context: Dict,
                              solution_type: str) -> Dict:
        return anchor_solution_users(problem, context, solution_type, SOLUTION_USER_ANCHOR_DIMENSIONS)

    def _extract_step_summaries(self, reasoning_result: ReasoningResult) -> List[Dict]:
        step_names = {
            'research': '五维调研扫描',
            'contradiction': '核心矛盾recognize',
            'constraint': '约束反推目标',
            'user_anchor': '用户需求锚定',
            'execution': '执行层反推',
            'fallacy': '谬误自检'
        }
        steps = []
        for node in reasoning_result.reasoning_trace:
            step_key = next((k for k, n in step_names.items() if k in node.id), None)
            if step_key:
                steps.append({
                    "step": step_names[step_key],
                    "content": node.content,
                    "confidence": round(node.confidence, 2),
                    "validity": round(node.validity, 2),
                    "metadata": node.metadata
                })
        return steps

    # ── 辅助方法 ──────────────────────────────────────────────────────────────

    def _decompose_problem(self, problem: str) -> List[str]:
        sub_problems = []
        sentences = [s.strip() for s in problem.replace('?', '.').split('.')]
        sentences = [s for s in sentences if s]
        if len(sentences) == 1 and ',' in problem:
            sub_problems = [s.strip() for s in problem.split(',') if s.strip()]
        else:
            sub_problems = sentences
        return sub_problems if sub_problems else [problem]

    def _solve_sub_problem(self, sub_problem: str, context: Dict) -> str:
        return f"解决方案: {sub_problem}"

    def _synthesize_answer(self, problem: str, solutions: List[str]) -> str:
        if not solutions:
            return "无法解决问题"
        return "综合解决方案: " + "; ".join(solutions)

    def _generate_initial_thoughts(self, problem: str, count: int = 3) -> List[str]:
        return [f"想法{i+1}: 关于{problem[:20]}的思考" for i in range(count)]

    def _expand_thought(self, thought: str, depth: int = 2) -> List[str]:
        return [f"步骤{i+1}: 深入思考{thought[:10]}" for i in range(depth)]

    def _extract_concepts(self, problem: str) -> List[str]:
        words = problem.split()
        concepts = [w for w in words if len(w) > 2]
        return concepts[:10] if concepts else ["概念"]

    def _extract_relations(self, concepts: List[str],
                         problem: str) -> List:
        relations = []
        for i in range(len(concepts) - 1):
            relations.append((concepts[i], concepts[i+1], "related"))
        return relations

    def _traverse_graph(self, graph, start: str) -> List[str]:
        import networkx as nx
        path = []
        try:
            for node in nx.bfs_tree(graph, start):
                path.append(node)
        except Exception:
            path = list(graph.nodes())[:5]
        return path

    def _retrieve_similar_reasoning(self, problem: str, k: int = 3) -> List[ReasoningResult]:
        similar = []
        problem_words = set(problem.lower().split())
        for result in self.reasoning_memory.values():
            result_words = set(result.problem.lower().split())
            overlap = len(problem_words & result_words)
            if overlap > 0:
                similar.append((result, overlap))
        similar.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in similar[:k]]

    def _update_stats(self, result: ReasoningResult):
        self.stats["total_reasoning"] += 1
        if result.success:
            self.stats["successful_reasoning"] += 1
        else:
            self.stats["failed_reasoning"] += 1
        n = self.stats["total_reasoning"]
        self.stats["avg_steps"] = (self.stats["avg_steps"] * (n - 1) + result.steps_count) / n
        self.stats["avg_confidence"] = (self.stats["avg_confidence"] * (n - 1) + result.confidence) / n
        mode = result.reasoning_mode.value
        self.stats["mode_usage"][mode] = self.stats["mode_usage"].get(mode, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        n = self.stats["total_reasoning"]
        return {
            "total_reasoning": n,
            "successful_reasoning": self.stats["successful_reasoning"],
            "failed_reasoning": self.stats["failed_reasoning"],
            "success_rate": self.stats["successful_reasoning"] / n if n > 0 else 0,
            "avg_steps": self.stats["avg_steps"],
            "avg_confidence": self.stats["avg_confidence"],
            "mode_usage": self.stats["mode_usage"]
        }

    def get_reasoning_history(self, limit: int = 10) -> List[ReasoningResult]:
        return self.reasoning_history[-limit:]
